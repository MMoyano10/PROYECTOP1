"""
Excepciones personalizadas para el módulo de mensajería
"""


class MessagingError(Exception):
    """Excepción base para todos los errores de mensajería"""
    
    def __init__(self, message: str, original_error: Exception = None):
        super().__init__(message)
        self.original_error = original_error
        self.message = message
    
    def __str__(self):
        if self.original_error:
            return f"{self.message} (Original: {self.original_error})"
        return self.message


class MessagingConnectionError(MessagingError):
    """Error de conexión con RabbitMQ"""
    pass


class PublishError(MessagingError):
    """Error al publicar mensajes"""
    pass


class SubscribeError(MessagingError):
    """Error al suscribirse a colas"""
    pass


class ConfigurationError(MessagingError):
    """Error de configuración"""
    pass


class SerializationError(MessagingError):
    """Error al serializar/deserializar mensajes"""
    pass


class QueueError(MessagingError):
    """Error relacionado con las colas"""
    pass


class ExchangeError(MessagingError):
    """Error relacionado con los exchanges"""
    pass
