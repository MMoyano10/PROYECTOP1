"""
Integración del módulo de mensajería en el servicio de Assets

Este archivo demuestra cómo integrar el módulo de mensajería
para comunicación asíncrona con otros microservicios.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager

# Importar el módulo de mensajería
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from messaging_service import (
    MessagingClient, 
    MessagePublisher, 
    MessageSubscriber,
    MessagePriority
)

logger = logging.getLogger(__name__)


class AssetsMessagingIntegration:
    """
    Integración de mensajería para el servicio de Assets
    
    Maneja la comunicación asíncrona con otros microservicios
    usando RabbitMQ.
    """
    
    def __init__(self):
        self.messaging_client: Optional[MessagingClient] = None
        self.publisher: Optional[MessagePublisher] = None
        self.subscriber: Optional[MessageSubscriber] = None
        
        # Estado de la integración
        self._is_initialized = False
        self._is_subscribed = False
        
    async def initialize(self) -> None:
        """Inicializa la integración de mensajería"""
        try:
            logger.info("Inicializando integración de mensajería...")
            
            # Crear cliente de mensajería
            self.messaging_client = MessagingClient()
            
            # Conectar a RabbitMQ
            await self.messaging_client.connect()
            
            # Crear publicador y suscriptor
            self.publisher = MessagePublisher(self.messaging_client)
            self.subscriber = MessageSubscriber(self.messaging_client)
            
            # Configurar suscripciones
            await self._setup_subscriptions()
            
            self._is_initialized = True
            logger.info("Integración de mensajería inicializada exitosamente")
            
        except Exception as e:
            logger.error(f"Error inicializando mensajería: {e}")
            raise
    
    async def _setup_subscriptions(self) -> None:
        """Configura las suscripciones a eventos de otros servicios"""
        try:
            # Suscribirse a eventos de categorías
            await self.subscriber.subscribe(
                queue_name="assets_category_events",
                handler=self._handle_category_event,
                routing_keys=["categories.*"]
            )
            
            # Suscribirse a eventos de tags
            await self.subscriber.subscribe(
                queue_name="assets_tag_events",
                handler=self._handle_tag_event,
                routing_keys=["tags.*"]
            )
            
            # Suscribirse a eventos de usuarios
            await self.subscriber.subscribe(
                queue_name="assets_user_events",
                handler=self._handle_user_event,
                routing_keys=["users.*"]
            )
            
            self._is_subscribed = True
            logger.info("Suscripciones configuradas exitosamente")
            
        except Exception as e:
            logger.error(f"Error configurando suscripciones: {e}")
            raise
    
    async def _handle_category_event(self, data: Dict[str, Any], metadata: Dict[str, Any]) -> None:
        """Maneja eventos de categorías"""
        try:
            action = data.get("action")
            category_data = data.get("category", {})
            
            logger.info(f"Evento de categoría recibido: {action} - {category_data}")
            
            if action == "created":
                await self._handle_category_created(category_data)
            elif action == "updated":
                await self._handle_category_updated(category_data)
            elif action == "deleted":
                await self._handle_category_deleted(category_data)
            else:
                logger.warning(f"Acción de categoría no reconocida: {action}")
                
        except Exception as e:
            logger.error(f"Error manejando evento de categoría: {e}")
    
    async def _handle_tag_event(self, data: Dict[str, Any], metadata: Dict[str, Any]) -> None:
        """Maneja eventos de tags"""
        try:
            action = data.get("action")
            tag_data = data.get("tag", {})
            
            logger.info(f"Evento de tag recibido: {action} - {tag_data}")
            
            if action == "created":
                await self._handle_tag_created(tag_data)
            elif action == "updated":
                await self._handle_tag_updated(tag_data)
            elif action == "deleted":
                await self._handle_tag_deleted(tag_data)
            else:
                logger.warning(f"Acción de tag no reconocida: {action}")
                
        except Exception as e:
            logger.error(f"Error manejando evento de tag: {e}")
    
    async def _handle_user_event(self, data: Dict[str, Any], metadata: Dict[str, Any]) -> None:
        """Maneja eventos de usuarios"""
        try:
            action = data.get("action")
            user_data = data.get("user", {})
            
            logger.info(f"Evento de usuario recibido: {action} - {user_data}")
            
            if action == "login":
                await self._handle_user_login(user_data)
            elif action == "logout":
                await self._handle_user_logout(user_data)
            else:
                logger.warning(f"Acción de usuario no reconocida: {action}")
                
        except Exception as e:
            logger.error(f"Error manejando evento de usuario: {e}")
    
    # Handlers específicos para eventos de categorías
    async def _handle_category_created(self, category_data: Dict[str, Any]) -> None:
        """Maneja la creación de una nueva categoría"""
        logger.info(f"Nueva categoría creada: {category_data}")
        # Aquí se podría actualizar cache, notificar a otros servicios, etc.
    
    async def _handle_category_updated(self, category_data: Dict[str, Any]) -> None:
        """Maneja la actualización de una categoría"""
        logger.info(f"Categoría actualizada: {category_data}")
        # Aquí se podría invalidar cache, notificar cambios, etc.
    
    async def _handle_category_deleted(self, category_data: Dict[str, Any]) -> None:
        """Maneja la eliminación de una categoría"""
        logger.info(f"Categoría eliminada: {category_data}")
        # Aquí se podría limpiar cache, notificar eliminación, etc.
    
    # Handlers específicos para eventos de tags
    async def _handle_tag_created(self, tag_data: Dict[str, Any]) -> None:
        """Maneja la creación de un nuevo tag"""
        logger.info(f"Nuevo tag creado: {tag_data}")
    
    async def _handle_tag_updated(self, tag_data: Dict[str, Any]) -> None:
        """Maneja la actualización de un tag"""
        logger.info(f"Tag actualizado: {tag_data}")
    
    async def _handle_tag_deleted(self, tag_data: Dict[str, Any]) -> None:
        """Maneja la eliminación de un tag"""
        logger.info(f"Tag eliminado: {tag_data}")
    
    # Handlers específicos para eventos de usuarios
    async def _handle_user_login(self, user_data: Dict[str, Any]) -> None:
        """Maneja el login de un usuario"""
        logger.info(f"Usuario logueado: {user_data}")
    
    async def _handle_user_logout(self, user_data: Dict[str, Any]) -> None:
        """Maneja el logout de un usuario"""
        logger.info(f"Usuario deslogueado: {user_data}")
    
    # Métodos para publicar eventos del servicio de assets
    async def notify_asset_created(self, asset_data: Dict[str, Any]) -> str:
        """Notifica la creación de un nuevo asset"""
        try:
            message_id = await self.publisher.publish(
                message={
                    "action": "created",
                    "asset": asset_data,
                    "timestamp": asset_data.get("created_at")
                },
                routing_key="assets.created",
                source_service="assets_service",
                priority=MessagePriority.NORMAL
            )
            
            logger.info(f"Evento de asset creado publicado: {message_id}")
            return message_id
            
        except Exception as e:
            logger.error(f"Error publicando evento de asset creado: {e}")
            raise
    
    async def notify_asset_updated(self, asset_data: Dict[str, Any]) -> str:
        """Notifica la actualización de un asset"""
        try:
            message_id = await self.publisher.publish(
                message={
                    "action": "updated",
                    "asset": asset_data,
                    "timestamp": asset_data.get("updated_at")
                },
                routing_key="assets.updated",
                source_service="assets_service",
                priority=MessagePriority.NORMAL
            )
            
            logger.info(f"Evento de asset actualizado publicado: {message_id}")
            return message_id
            
        except Exception as e:
            logger.error(f"Error publicando evento de asset actualizado: {e}")
            raise
    
    async def notify_asset_deleted(self, asset_id: int) -> str:
        """Notifica la eliminación de un asset"""
        try:
            message_id = await self.publisher.publish(
                message={
                    "action": "deleted",
                    "asset_id": asset_id,
                    "timestamp": asyncio.get_event_loop().time()
                },
                routing_key="assets.deleted",
                source_service="assets_service",
                priority=MessagePriority.HIGH
            )
            
            logger.info(f"Evento de asset eliminado publicado: {message_id}")
            return message_id
            
        except Exception as e:
            logger.error(f"Error publicando evento de asset eliminado: {e}")
            raise
    
    async def notify_asset_processed(self, asset_data: Dict[str, Any], processing_result: Dict[str, Any]) -> str:
        """Notifica que un asset ha sido procesado"""
        try:
            message_id = await self.publisher.publish(
                message={
                    "action": "processed",
                    "asset": asset_data,
                    "processing_result": processing_result,
                    "timestamp": asyncio.get_event_loop().time()
                },
                routing_key="assets.processed",
                source_service="assets_service",
                priority=MessagePriority.NORMAL
            )
            
            logger.info(f"Evento de asset procesado publicado: {message_id}")
            return message_id
            
        except Exception as e:
            logger.error(f"Error publicando evento de asset procesado: {e}")
            raise
    
    # Métodos de utilidad
    async def health_check(self) -> Dict[str, Any]:
        """Verifica el estado de salud de la integración de mensajería"""
        if not self._is_initialized:
            return {
                "status": "not_initialized",
                "message": "La integración de mensajería no ha sido inicializada"
            }
        
        try:
            # Verificar estado del cliente
            client_health = await self.messaging_client.health_check()
            
            return {
                "status": "healthy" if client_health["status"] == "healthy" else "unhealthy",
                "messaging_client": client_health,
                "is_subscribed": self._is_subscribed,
                "active_queues": self.subscriber.active_queues if self.subscriber else []
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error en health check: {e}"
            }
    
    @asynccontextmanager
    async def get_messaging_context(self):
        """Context manager para operaciones de mensajería"""
        if not self._is_initialized:
            await self.initialize()
        
        try:
            yield self
        finally:
            pass  # No cerramos la conexión automáticamente
    
    async def close(self) -> None:
        """Cierra la integración de mensajería"""
        try:
            if self.subscriber:
                await self.subscriber.close()
            
            if self.publisher:
                await self.publisher.close()
            
            if self.messaging_client:
                await self.messaging_client.disconnect()
            
            self._is_initialized = False
            self._is_subscribed = False
            
            logger.info("Integración de mensajería cerrada")
            
        except Exception as e:
            logger.error(f"Error cerrando integración de mensajería: {e}")
    
    @property
    def is_initialized(self) -> bool:
        """Indica si la integración está inicializada"""
        return self._is_initialized
    
    @property
    def is_subscribed(self) -> bool:
        """Indica si las suscripciones están activas"""
        return self._is_subscribed


# Instancia global de la integración
assets_messaging = AssetsMessagingIntegration()


# Funciones de conveniencia para uso en otros módulos
async def notify_asset_event(event_type: str, asset_data: Dict[str, Any], **kwargs) -> str:
    """Función de conveniencia para notificar eventos de assets"""
    async with assets_messaging.get_messaging_context() as messaging:
        if event_type == "created":
            return await messaging.notify_asset_created(asset_data)
        elif event_type == "updated":
            return await messaging.notify_asset_updated(asset_data)
        elif event_type == "deleted":
            return await messaging.notify_asset_deleted(asset_data.get("id"))
        elif event_type == "processed":
            return await messaging.notify_asset_processed(asset_data, kwargs.get("processing_result", {}))
        else:
            raise ValueError(f"Tipo de evento no reconocido: {event_type}")


async def get_messaging_health() -> Dict[str, Any]:
    """Función de conveniencia para health check"""
    return await assets_messaging.health_check()
