"""
Suscriptor de mensajes para RabbitMQ
"""

import json
import logging
import asyncio
from typing import Any, Callable, Dict, Optional, Union, Awaitable
from dataclasses import dataclass
from enum import Enum

import aio_pika
from aio_pika import IncomingMessage, Queue, ExchangeType

from .messaging_client import MessagingClient
from .exceptions import SubscribeError, MessagingError


class MessageHandler:
    """Manejador de mensajes recibidos"""
    
    def __init__(self, callback: Callable[[Dict[str, Any], Dict[str, Any]], Awaitable[None]]):
        self.callback = callback
        self.logger = logging.getLogger(__name__)
    
    async def handle(self, message_data: Dict[str, Any], metadata: Dict[str, Any]) -> None:
        """Ejecuta el callback del manejador"""
        try:
            await self.callback(message_data, metadata)
        except Exception as e:
            self.logger.error(f"Error en manejador de mensaje: {e}")
            raise


class MessageSubscriber:
    """
    Suscriptor de mensajes para RabbitMQ
    
    Permite suscribirse a colas específicas y procesar
    mensajes entrantes de forma asíncrona.
    """
    
    def __init__(self, messaging_client: MessagingClient):
        self.client = messaging_client
        self.logger = logging.getLogger(__name__)
        
        # Colas y suscripciones activas
        self._queues: Dict[str, Queue] = {}
        self._consumers: Dict[str, aio_pika.Consumer] = {}
        self._handlers: Dict[str, MessageHandler] = {}
        
        # Estado de suscripción
        self._is_subscribed = False
        
    async def subscribe(
        self,
        queue_name: str,
        handler: Callable[[Dict[str, Any], Dict[str, Any]], Awaitable[None]],
        exchange_name: Optional[str] = None,
        routing_keys: Optional[list[str]] = None,
        auto_ack: bool = False,
        prefetch_count: int = 10
    ) -> None:
        """
        Suscribe a una cola específica
        
        Args:
            queue_name: Nombre de la cola
            handler: Función manejadora del mensaje
            exchange_name: Nombre del exchange (opcional)
            routing_keys: Claves de enrutamiento para binding
            auto_ack: Si se debe hacer ACK automático
            prefetch_count: Número de mensajes a procesar simultáneamente
        """
        try:
            await self.client.ensure_connection()
            
            # Crear o obtener cola (resuelve exchange por defecto internamente)
            queue = await self._create_queue(queue_name, exchange_name, routing_keys)
            
            # Configurar QoS
            await self.client.channel.set_qos(prefetch_count=prefetch_count)
            
            # Crear manejador
            message_handler = MessageHandler(handler)
            
            # Crear consumidor
            consumer = await queue.consume(
                callback=lambda message: self._process_message(message, message_handler, auto_ack),
                no_ack=auto_ack
            )
            
            # Guardar referencias
            self._queues[queue_name] = queue
            self._consumers[queue_name] = consumer
            self._handlers[queue_name] = message_handler
            
            self._is_subscribed = True
            
            effective_exchange = exchange_name or self.client.config.default_exchange
            self.logger.info(
                f"Suscripción exitosa a cola '{queue_name}' "
                f"(exchange: {effective_exchange}, routing_keys: {routing_keys or ['#']})"
            )
            
        except Exception as e:
            self.logger.error(f"Error suscribiéndose a cola '{queue_name}': {e}")
            raise SubscribeError(f"No se pudo suscribir a la cola: {e}", e)
    
    async def subscribe_to_exchange(
        self,
        exchange_name: str,
        handler: Callable[[Dict[str, Any], Dict[str, Any]], Awaitable[None]],
        routing_keys: Optional[list[str]] = None,
        queue_suffix: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Suscribe a un exchange con una cola temporal
        
        Args:
            exchange_name: Nombre del exchange
            handler: Función manejadora del mensaje
            routing_keys: Claves de enrutamiento
            queue_suffix: Sufijo para la cola temporal
            **kwargs: Argumentos adicionales para subscribe()
            
        Returns:
            Nombre de la cola creada
        """
        # Crear nombre de cola temporal
        queue_name = f"temp_{exchange_name}_{queue_suffix or int(asyncio.get_event_loop().time())}"
        
        await self.subscribe(
            queue_name=queue_name,
            handler=handler,
            exchange_name=exchange_name,
            routing_keys=routing_keys,
            **kwargs
        )
        
        return queue_name
    
    async def unsubscribe(self, queue_name: str) -> None:
        """Desuscribe de una cola específica"""
        if queue_name not in self._consumers:
            return
            
        try:
            # Cancelar consumidor usando el consumer tag
            consumer_tag = self._consumers[queue_name]
            queue = self._queues[queue_name]
            
            # Cancelar el consumer usando la cola
            await queue.cancel(consumer_tag)
            
            # Limpiar referencias
            del self._consumers[queue_name]
            del self._handlers[queue_name]
            
            # Solo eliminar la cola si es temporal
            if queue_name.startswith("temp_"):
                await queue.delete()
                del self._queues[queue_name]
            
            self.logger.info(f"Desuscripción exitosa de cola '{queue_name}'")
            
        except Exception as e:
            self.logger.error(f"Error desuscribiéndose de cola '{queue_name}': {e}")
            raise SubscribeError(f"Error al desuscribirse: {e}", e)
    
    async def unsubscribe_all(self) -> None:
        """Desuscribe de todas las colas"""
        queue_names = list(self._consumers.keys())
        for queue_name in queue_names:
            await self.unsubscribe(queue_name)
        
        self._is_subscribed = False
        self.logger.info("Desuscripción de todas las colas completada")
    
    async def _create_queue(
        self,
        queue_name: str,
        exchange_name: Optional[str] = None,
        routing_keys: Optional[list[str]] = None
    ) -> Queue:
        """Crea o obtiene una cola y la vincula al exchange"""
        try:
            # Crear cola
            queue = await self.client.channel.declare_queue(
                name=queue_name,
                durable=True,
                auto_delete=queue_name.startswith("temp_"),
                arguments={
                    "x-message-ttl": self.client.config.message_ttl * 1000,
                    "x-max-length": 10000
                }
            )
            
            # Resolver exchange efectivo (por defecto el configurado)
            effective_exchange_name = exchange_name or self.client.config.default_exchange
            
            # Declarar exchange y hacer binding
            exchange = await self.client.channel.declare_exchange(
                name=effective_exchange_name,
                type=ExchangeType.TOPIC,
                durable=True
            )
            
            # Binding con routing keys
            if routing_keys:
                for routing_key in routing_keys:
                    await queue.bind(exchange, routing_key)
            else:
                # Binding por defecto con wildcard
                await queue.bind(exchange, "#")
            
            return queue
            
        except Exception as e:
            raise MessagingError(f"No se pudo crear la cola '{queue_name}': {e}", e)
    
    async def _process_message(
        self,
        message: IncomingMessage,
        handler: MessageHandler,
        auto_ack: bool
    ) -> None:
        """Procesa un mensaje entrante"""
        try:
            # Deserializar mensaje
            message_data, metadata = self._deserialize_message(message)
            
            # Ejecutar manejador
            await handler.handle(message_data, metadata)
            
            # ACK del mensaje si no es automático
            if not auto_ack:
                await message.ack()
                
            self.logger.debug(f"Mensaje procesado exitosamente: {metadata.get('message_id', 'unknown')}")
            
        except Exception as e:
            self.logger.error(f"Error procesando mensaje: {e}")
            
            # Rechazar mensaje en caso de error
            if not auto_ack:
                await message.reject(requeue=False)
            
            # Re-lanzar excepción para logging
            raise
    
    def _deserialize_message(self, message: IncomingMessage) -> tuple[Dict[str, Any], Dict[str, Any]]:
        """Deserializa un mensaje de RabbitMQ"""
        try:
            # Decodificar cuerpo del mensaje
            body = message.body.decode('utf-8')
            message_data = json.loads(body)
            
            # Extraer datos y metadatos
            data = message_data.get("data", {})
            metadata = message_data.get("metadata", {})
            
            # Agregar metadatos adicionales de RabbitMQ
            metadata.update({
                "delivery_tag": message.delivery_tag,
                "redelivered": message.redelivered,
                "exchange": message.exchange,
                "routing_key": message.routing_key,
                "priority": message.priority,
                "timestamp": message.timestamp,
                "expiration": message.expiration
            })
            
            return data, metadata
            
        except Exception as e:
            raise MessagingError(f"Error deserializando mensaje: {e}", e)
    
    @property
    def is_subscribed(self) -> bool:
        """Indica si hay suscripciones activas"""
        return self._is_subscribed
    
    @property
    def active_queues(self) -> list[str]:
        """Retorna la lista de colas activas"""
        return list(self._queues.keys())
    
    async def close(self):
        """Cierra el suscriptor y libera recursos"""
        await self.unsubscribe_all()
        self.logger.info("MessageSubscriber cerrado")
    
    def __repr__(self):
        return f"MessageSubscriber(client={self.client}, subscribed={self._is_subscribed})"
