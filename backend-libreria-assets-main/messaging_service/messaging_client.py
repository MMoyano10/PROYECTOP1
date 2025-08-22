"""
Cliente principal de mensajería para RabbitMQ
"""

import asyncio
import logging
import json
import time
from typing import Optional, Dict, Any, Callable
from contextlib import asynccontextmanager

import aio_pika
from aio_pika import connect_robust, Message, DeliveryMode
from aio_pika.patterns import RPC

from .config import MessagingConfig
from .exceptions import MessagingConnectionError, MessagingError


class MessagingClient:
    """
    Cliente principal para la comunicación con RabbitMQ
    
    Proporciona métodos para conectar, desconectar y gestionar
    la comunicación asíncrona entre microservicios.
    """
    
    def __init__(self, config: Optional[MessagingConfig] = None):
        self.config = config or MessagingConfig()
        self.logger = logging.getLogger(__name__)
        
        # Estado de la conexión
        self._connection: Optional[aio_pika.Connection] = None
        self._channel: Optional[aio_pika.Channel] = None
        self._rpc: Optional[RPC] = None
        
        # Callbacks de reconexión
        self._reconnect_callbacks: list[Callable] = []
        self._disconnect_callbacks: list[Callable] = []
        
        # Estado de la conexión
        self._is_connected = False
        self._is_connecting = False
        
    async def connect(self) -> None:
        """Establece conexión con RabbitMQ"""
        if self._is_connected or self._is_connecting:
            return
            
        self._is_connecting = True
        
        try:
            self.logger.info(f"Conectando a RabbitMQ en {self.config.rabbitmq_host}:{self.config.rabbitmq_port}")
            
            # Establecer conexión
            self._connection = await connect_robust(
                self.config.connection_url,
                timeout=self.config.connection_timeout,
                heartbeat=self.config.heartbeat
            )
            
            # Crear canal
            self._channel = await self._connection.channel()
            await self._channel.set_qos(prefetch_count=10)
            
            # Configurar RPC
            self._rpc = await RPC.create(self._channel)
            
            # Configurar callbacks de reconexión (si están disponibles)
            if hasattr(self._connection, 'add_close_callback'):
                self._connection.add_close_callback(self._on_connection_closed)
            if hasattr(self._connection, 'add_reconnect_callback'):
                self._connection.add_reconnect_callback(self._on_reconnected)
            
            self._is_connected = True
            self._is_connecting = False
            
            self.logger.info("Conexión establecida exitosamente con RabbitMQ")
            
            # Ejecutar callbacks de reconexión
            await self._execute_callbacks(self._reconnect_callbacks)
            
        except Exception as e:
            self._is_connecting = False
            self.logger.error(f"Error al conectar con RabbitMQ: {e}")
            raise MessagingConnectionError(f"No se pudo conectar a RabbitMQ: {e}", e)
    
    async def disconnect(self) -> None:
        """Cierra la conexión con RabbitMQ"""
        if not self._is_connected:
            return
            
        try:
            self.logger.info("Desconectando de RabbitMQ...")
            
            # Ejecutar callbacks de desconexión
            await self._execute_callbacks(self._disconnect_callbacks)
            
            # Cerrar canal y conexión
            if self._channel:
                await self._channel.close()
                self._channel = None
                
            if self._connection:
                await self._connection.close()
                self._connection = None
                
            self._rpc = None
            self._is_connected = False
            
            self.logger.info("Desconexión completada")
            
        except Exception as e:
            self.logger.error(f"Error al desconectar: {e}")
            raise MessagingError(f"Error al desconectar: {e}", e)
    
    async def ensure_connection(self) -> None:
        """Asegura que la conexión esté establecida"""
        if not self._is_connected:
            await self.connect()
    
    @property
    def is_connected(self) -> bool:
        """Indica si la conexión está establecida"""
        return self._is_connected
    
    @property
    def channel(self) -> Optional[aio_pika.Channel]:
        """Retorna el canal de RabbitMQ"""
        return self._channel
    
    @property
    def rpc(self) -> Optional[RPC]:
        """Retorna el cliente RPC"""
        return self._rpc
    
    def add_reconnect_callback(self, callback: Callable) -> None:
        """Agrega un callback para cuando se reconecte"""
        self._reconnect_callbacks.append(callback)
    
    def add_disconnect_callback(self, callback: Callable) -> None:
        """Agrega un callback para cuando se desconecte"""
        self._disconnect_callbacks.append(callback)
    
    async def _execute_callbacks(self, callbacks: list[Callable]) -> None:
        """Ejecuta una lista de callbacks de forma asíncrona"""
        for callback in callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback()
                else:
                    callback()
            except Exception as e:
                self.logger.error(f"Error ejecutando callback: {e}")
    
    def _on_connection_closed(self, connection: aio_pika.Connection) -> None:
        """Callback cuando se cierra la conexión"""
        self.logger.warning("Conexión con RabbitMQ cerrada")
        self._is_connected = False
        
    async def _on_reconnected(self, connection: aio_pika.Connection) -> None:
        """Callback cuando se reconecta"""
        self.logger.info("Reconectado a RabbitMQ")
        self._is_connected = True
        await self._execute_callbacks(self._reconnect_callbacks)
    
    @asynccontextmanager
    async def get_connection(self):
        """Context manager para obtener una conexión"""
        await self.ensure_connection()
        try:
            yield self
        finally:
            pass  # No desconectamos automáticamente
    
    async def health_check(self) -> Dict[str, Any]:
        """Verifica el estado de salud de la conexión"""
        try:
            if not self._is_connected:
                return {
                    "status": "disconnected",
                    "message": "No hay conexión activa con RabbitMQ"
                }
            
            # Verificar que el canal esté activo
            if self._channel and not self._channel.is_closed:
                return {
                    "status": "healthy",
                    "message": "Conexión activa y funcionando",
                    "host": self.config.rabbitmq_host,
                    "port": self.config.rabbitmq_port,
                    "connected_at": time.time()
                }
            else:
                return {
                    "status": "unhealthy",
                    "message": "Canal cerrado o inactivo"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error en health check: {e}"
            }
    
    def __repr__(self):
        return f"MessagingClient(connected={self._is_connected}, host={self.config.rabbitmq_host})"
