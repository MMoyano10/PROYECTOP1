"""
Configuración del módulo de mensajería
"""

import os
from typing import Optional
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from pydantic import Field


class MessagingConfig(BaseSettings):
    """Configuración para la conexión a RabbitMQ"""
    
    # Configuración de conexión
    rabbitmq_host: str = Field(default="localhost", env="RABBITMQ_HOST")
    rabbitmq_port: int = Field(default=5672, env="RABBITMQ_PORT")
    rabbitmq_user: str = Field(default="guest", env="RABBITMQ_USER")
    rabbitmq_password: str = Field(default="guest", env="RABBITMQ_PASSWORD")
    rabbitmq_vhost: str = Field(default="/", env="RABBITMQ_VHOST")
    
    # Configuración de conexión
    connection_timeout: int = Field(default=30, env="RABBITMQ_CONNECTION_TIMEOUT")
    heartbeat: int = Field(default=600, env="RABBITMQ_HEARTBEAT")
    
    # Configuración de reconexión
    max_retries: int = Field(default=5, env="RABBITMQ_MAX_RETRIES")
    retry_delay: int = Field(default=5, env="RABBITMQ_RETRY_DELAY")
    
    # Configuración de colas
    default_exchange: str = Field(default="libreria_assets", env="RABBITMQ_DEFAULT_EXCHANGE")
    default_queue_prefix: str = Field(default="", env="RABBITMQ_QUEUE_PREFIX")
    
    # Configuración de mensajes
    message_ttl: int = Field(default=86400, env="RABBITMQ_MESSAGE_TTL")  # 24 horas
    max_message_size: int = Field(default=1048576, env="RABBITMQ_MAX_MESSAGE_SIZE")  # 1MB
    
    # Configuración de logging
    log_level: str = Field(default="INFO", env="RABBITMQ_LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def connection_url(self) -> str:
        """URL de conexión a RabbitMQ"""
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}/{self.rabbitmq_vhost}"
    
    @property
    def queue_name(self) -> str:
        """Nombre de la cola con prefijo"""
        return f"{self.default_queue_prefix}libreria_assets_queue"
    
    @property
    def dead_letter_queue(self) -> str:
        """Nombre de la cola de mensajes fallidos"""
        return f"{self.default_queue_prefix}libreria_assets_dlq"


# Configuración por defecto
default_config = MessagingConfig()
