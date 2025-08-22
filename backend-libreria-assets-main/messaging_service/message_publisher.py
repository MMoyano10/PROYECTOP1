"""
Publicador de mensajes para RabbitMQ
"""

import json
import logging
import time
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass
from enum import Enum

import aio_pika
from aio_pika import Message, DeliveryMode, ExchangeType

from .messaging_client import MessagingClient
from .exceptions import PublishError, MessagingError


class MessagePriority(Enum):
    """Prioridades de mensaje"""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class MessageMetadata:
    """Metadatos del mensaje"""
    message_id: str
    timestamp: float
    source_service: str
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None
    priority: MessagePriority = MessagePriority.NORMAL
    ttl: Optional[int] = None
    headers: Optional[Dict[str, Any]] = None


class MessagePublisher:
    """
    Publicador de mensajes para RabbitMQ
    
    Permite enviar mensajes a exchanges específicos con
    configuraciones de prioridad, TTL y headers personalizados.
    """
    
    def __init__(self, messaging_client: MessagingClient):
        self.client = messaging_client
        self.logger = logging.getLogger(__name__)
        
        # Cache de exchanges
        self._exchanges: Dict[str, aio_pika.Exchange] = {}
        
    async def publish(
        self,
        message: Any,
        routing_key: str,
        exchange_name: Optional[str] = None,
        priority: MessagePriority = MessagePriority.NORMAL,
        ttl: Optional[int] = None,
        headers: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[str] = None,
        reply_to: Optional[str] = None,
        source_service: Optional[str] = None,
        delivery_mode: DeliveryMode = DeliveryMode.PERSISTENT
    ) -> str:
        """
        Publica un mensaje en RabbitMQ
        
        Args:
            message: Contenido del mensaje
            routing_key: Clave de enrutamiento
            exchange_name: Nombre del exchange (opcional)
            priority: Prioridad del mensaje
            ttl: Tiempo de vida en segundos
            headers: Headers adicionales
            correlation_id: ID de correlación
            reply_to: Cola de respuesta
            source_service: Nombre del servicio origen
            delivery_mode: Modo de entrega
            
        Returns:
            ID del mensaje publicado
        """
        try:
            await self.client.ensure_connection()
            
            # Preparar metadatos
            message_id = self._generate_message_id()
            metadata = MessageMetadata(
                message_id=message_id,
                timestamp=time.time(),
                source_service=source_service or "unknown",
                correlation_id=correlation_id,
                reply_to=reply_to,
                priority=priority,
                ttl=ttl,
                headers=headers or {}
            )
            
            # Serializar mensaje
            message_body = self._serialize_message(message, metadata)
            
            # Obtener exchange
            exchange = await self._get_exchange(exchange_name)
            
            # Crear mensaje de RabbitMQ
            rabbitmq_message = Message(
                body=message_body,
                delivery_mode=delivery_mode,
                priority=priority.value,
                headers=self._prepare_headers(metadata),
                expiration=ttl * 1000 if ttl else None,  # RabbitMQ usa milisegundos
                message_id=message_id,
                correlation_id=correlation_id,
                reply_to=reply_to,
                timestamp=time.time()
            )
            
            # Publicar mensaje
            await exchange.publish(
                rabbitmq_message,
                routing_key=routing_key
            )
            
            self.logger.info(
                f"Mensaje publicado exitosamente: {message_id} -> {routing_key} "
                f"(exchange: {exchange.name}, priority: {priority.name})"
            )
            
            return message_id
            
        except Exception as e:
            self.logger.error(f"Error publicando mensaje: {e}")
            raise PublishError(f"No se pudo publicar el mensaje: {e}", e)
    
    async def publish_to_queue(
        self,
        message: Any,
        queue_name: str,
        **kwargs
    ) -> str:
        """
        Publica un mensaje directamente a una cola específica
        
        Args:
            message: Contenido del mensaje
            queue_name: Nombre de la cola
            **kwargs: Argumentos adicionales para publish()
            
        Returns:
            ID del mensaje publicado
        """
        # Para publicar directamente a una cola, usamos el exchange por defecto
        # y la cola como routing key
        return await self.publish(
            message=message,
            routing_key=queue_name,
            **kwargs
        )
    
    async def publish_batch(
        self,
        messages: list[tuple[Any, str]],
        exchange_name: Optional[str] = None,
        **kwargs
    ) -> list[str]:
        """
        Publica múltiples mensajes en lote
        
        Args:
            messages: Lista de tuplas (mensaje, routing_key)
            exchange_name: Nombre del exchange
            **kwargs: Argumentos adicionales para publish()
            
        Returns:
            Lista de IDs de mensajes publicados
        """
        message_ids = []
        
        try:
            await self.client.ensure_connection()
            exchange = await self._get_exchange(exchange_name)
            
            for message, routing_key in messages:
                message_id = await self.publish(
                    message=message,
                    routing_key=routing_key,
                    exchange_name=exchange_name,
                    **kwargs
                )
                message_ids.append(message_id)
                
        except Exception as e:
            self.logger.error(f"Error publicando lote de mensajes: {e}")
            raise PublishError(f"Error en publicación por lotes: {e}", e)
        
        return message_ids
    
    async def _get_exchange(self, exchange_name: Optional[str] = None) -> aio_pika.Exchange:
        """Obtiene o crea un exchange"""
        name = exchange_name or self.client.config.default_exchange
        
        if name not in self._exchanges:
            try:
                exchange = await self.client.channel.declare_exchange(
                    name=name,
                    type=ExchangeType.TOPIC,
                    durable=True,
                    auto_delete=False
                )
                self._exchanges[name] = exchange
                self.logger.debug(f"Exchange '{name}' declarado/obtenido")
            except Exception as e:
                raise MessagingError(f"No se pudo obtener el exchange '{name}': {e}", e)
        
        return self._exchanges[name]
    
    def _serialize_message(self, message: Any, metadata: MessageMetadata) -> bytes:
        """Serializa el mensaje y metadatos"""
        try:
            # Crear estructura del mensaje
            message_data = {
                "data": message,
                "metadata": {
                    "message_id": metadata.message_id,
                    "timestamp": metadata.timestamp,
                    "source_service": metadata.source_service,
                    "correlation_id": metadata.correlation_id,
                    "reply_to": metadata.reply_to,
                    "priority": metadata.priority.name,
                    "ttl": metadata.ttl,
                    "headers": metadata.headers
                }
            }
            
            # Serializar a JSON
            return json.dumps(message_data, default=str).encode('utf-8')
            
        except Exception as e:
            raise MessagingError(f"Error serializando mensaje: {e}", e)
    
    def _prepare_headers(self, metadata: MessageMetadata) -> Dict[str, Any]:
        """Prepara los headers del mensaje"""
        headers = metadata.headers.copy() if metadata.headers else {}
        
        # Agregar headers estándar
        headers.update({
            "source_service": metadata.source_service,
            "priority": metadata.priority.name,
            "timestamp": metadata.timestamp
        })
        
        return headers
    
    def _generate_message_id(self) -> str:
        """Genera un ID único para el mensaje"""
        return f"msg_{int(time.time() * 1000000)}_{id(self)}"
    
    async def close(self):
        """Cierra el publicador y libera recursos"""
        self._exchanges.clear()
        self.logger.info("MessagePublisher cerrado")
    
    def __repr__(self):
        return f"MessagePublisher(client={self.client})"
