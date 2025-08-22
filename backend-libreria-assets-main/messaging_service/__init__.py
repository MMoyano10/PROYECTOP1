"""
Módulo de Mensajería - RabbitMQ
===============================

Este módulo proporciona una capa de abstracción para la comunicación
asíncrona entre microservicios usando RabbitMQ.

Características:
- Conexión automática y reconexión
- Publicación y suscripción de mensajes
- Manejo de colas y exchanges
- Serialización/deserialización automática
- Logging integrado
- Configuración flexible
"""

from .messaging_client import MessagingClient
from .message_publisher import MessagePublisher, MessagePriority
from .message_subscriber import MessageSubscriber
from .config import MessagingConfig
from .exceptions import MessagingError, MessagingConnectionError, PublishError, SubscribeError

__version__ = "1.0.0"
__all__ = [
    "MessagingClient",
    "MessagePublisher",
    "MessagePriority",
    "MessageSubscriber",
    "MessagingConfig",
    "MessagingError",
    "MessagingConnectionError",
    "PublishError",
    "SubscribeError"
]
