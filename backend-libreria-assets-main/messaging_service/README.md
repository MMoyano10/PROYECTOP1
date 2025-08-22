# Módulo de Mensajería RabbitMQ

Un módulo aislado y reutilizable para la comunicación asíncrona entre microservicios usando RabbitMQ.

## Características

- **Conexión automática y reconexión**: Manejo robusto de conexiones con RabbitMQ
- **Publicación y suscripción**: API simple para enviar y recibir mensajes
- **Manejo de colas y exchanges**: Configuración automática de infraestructura
- **Serialización automática**: JSON automático con metadatos estructurados
- **Prioridades de mensaje**: Soporte para mensajes con diferentes niveles de prioridad
- **TTL configurable**: Tiempo de vida configurable para mensajes
- **Logging integrado**: Sistema de logging completo y configurable
- **Manejo de errores**: Excepciones personalizadas y manejo robusto de errores
- **Health checks**: Verificación del estado de la conexión
- **RPC**: Soporte para comunicación Request-Response

## Instalación

### Dependencias

```bash
pip install -r requirements.txt
```

### Variables de Entorno

Crear un archivo `.env` con la configuración de RabbitMQ:

```env
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VHOST=/
RABBITMQ_CONNECTION_TIMEOUT=30
RABBITMQ_HEARTBEAT=600
RABBITMQ_MAX_RETRIES=5
RABBITMQ_RETRY_DELAY=5
RABBITMQ_DEFAULT_EXCHANGE=libreria_assets
RABBITMQ_QUEUE_PREFIX=
RABBITMQ_MESSAGE_TTL=86400
RABBITMQ_MAX_MESSAGE_SIZE=1048576
RABBITMQ_LOG_LEVEL=INFO
```

## Uso Básico

### 1. Cliente de Mensajería

```python
from messaging_service import MessagingClient

# Crear cliente
client = MessagingClient()

# Conectar a RabbitMQ
await client.connect()

# Verificar estado
health = await client.health_check()
print(f"Estado: {health['status']}")

# Desconectar
await client.disconnect()
```

### 2. Publicación de Mensajes

```python
from messaging_service import MessagePublisher, MessagePriority

# Crear publicador
publisher = MessagePublisher(client)

# Publicar mensaje simple
message_id = await publisher.publish(
    message={"text": "Hola mundo!", "data": 42},
    routing_key="example.hello",
    source_service="mi_servicio"
)

# Publicar con prioridad y TTL
message_id = await publisher.publish(
    message={"text": "Mensaje importante"},
    routing_key="example.important",
    priority=MessagePriority.HIGH,
    ttl=3600,  # 1 hora
    source_service="mi_servicio"
)

# Publicar directamente a cola
message_id = await publisher.publish_to_queue(
    message={"text": "Mensaje directo"},
    queue_name="mi_cola"
)
```

### 3. Suscripción a Mensajes

```python
from messaging_service import MessageSubscriber

# Crear suscriptor
subscriber = MessageSubscriber(client)

# Definir manejador de mensajes
async def message_handler(data, metadata):
    print(f"Mensaje recibido: {data}")
    print(f"Metadatos: {metadata}")

# Suscribirse a cola
await subscriber.subscribe(
    queue_name="mi_cola",
    handler=message_handler,
    routing_keys=["example.*"]
)

# Suscribirse a exchange con cola temporal
queue_name = await subscriber.subscribe_to_exchange(
    exchange_name="mi_exchange",
    handler=message_handler,
    routing_keys=["events.*"]
)
```

### 4. Comunicación RPC

```python
# Servidor RPC
async def rpc_handler(data, metadata):
    result = {"result": data.get("number", 0) * 2}
    
    # Enviar respuesta
    if metadata.get("reply_to"):
        publisher = MessagePublisher(client)
        await publisher.publish(
            message=result,
            routing_key=metadata["reply_to"],
            correlation_id=metadata.get("correlation_id")
        )

# Suscribirse como servidor
await subscriber.subscribe(
    queue_name="rpc_server",
    handler=rpc_handler,
    routing_keys=["rpc.multiply"]
)

# Cliente RPC
response_queue = await subscriber.subscribe_to_exchange(
    exchange_name="libreria_assets",
    handler=lambda data, metadata: print(f"Respuesta: {data}"),
    routing_keys=["rpc.response"]
)

# Enviar solicitud
message_id = await publisher.publish(
    message={"number": 21},
    routing_key="rpc.multiply",
    reply_to=response_queue,
    correlation_id="req_123"
)
```

### 5. Publicación por Lotes

```python
# Preparar mensajes
messages = [
    ({"id": 1, "action": "create"}, "assets.create"),
    ({"id": 2, "action": "update"}, "assets.update"),
    ({"id": 3, "action": "delete"}, "assets.delete"),
]

# Publicar en lote
message_ids = await publisher.publish_batch(
    messages=messages,
    source_service="batch_service"
)
```

## Integración con Microservicios

### Assets Service

```python
# assets_service/main.py
from messaging_service import MessagingClient, MessagePublisher, MessageSubscriber

# Inicializar mensajería
messaging_client = MessagingClient()
publisher = MessagePublisher(messaging_client)
subscriber = MessageSubscriber(messaging_client)

# Suscribirse a eventos de categorías
async def category_event_handler(data, metadata):
    if data.get("action") == "created":
        # Procesar nueva categoría
        pass

await subscriber.subscribe(
    queue_name="assets_category_events",
    handler=category_event_handler,
    routing_keys=["categories.*"]
)

# Publicar eventos de assets
async def notify_asset_created(asset_data):
    await publisher.publish(
        message={"action": "created", "asset": asset_data},
        routing_key="assets.created",
        source_service="assets_service"
    )
```

### Categories Service

```python
# categories_service/main.py
from messaging_service import MessagingClient, MessagePublisher

messaging_client = MessagingClient()
publisher = MessagePublisher(messaging_client)

# Notificar creación de categoría
async def create_category(category_data):
    # Lógica de creación...
    
    # Notificar a otros servicios
    await publisher.publish(
        message={"action": "created", "category": category_data},
        routing_key="categories.created",
        source_service="categories_service"
    )
```

## Configuración Avanzada

### Configuración Personalizada

```python
from messaging_service import MessagingConfig, MessagingClient

# Configuración personalizada
config = MessagingConfig(
    rabbitmq_host="rabbitmq.example.com",
    rabbitmq_port=5672,
    rabbitmq_user="myuser",
    rabbitmq_password="mypassword",
    connection_timeout=60,
    heartbeat=300,
    max_retries=10,
    retry_delay=10
)

client = MessagingClient(config)
```

### Callbacks de Reconexión

```python
async def on_reconnect():
    print("Reconectado a RabbitMQ")
    # Reconfigurar suscripciones, etc.

async def on_disconnect():
    print("Desconectado de RabbitMQ")
    # Limpiar recursos, etc.

client.add_reconnect_callback(on_reconnect)
client.add_disconnect_callback(on_disconnect)
```

### Manejo de Errores

```python
from messaging_service.exceptions import MessagingError, ConnectionError, PublishError

try:
    await publisher.publish(message, "routing.key")
except ConnectionError as e:
    print(f"Error de conexión: {e}")
except PublishError as e:
    print(f"Error publicando: {e}")
except MessagingError as e:
    print(f"Error general: {e}")
```

## Estructura de Mensajes

Los mensajes se serializan automáticamente con la siguiente estructura:

```json
{
  "data": {
    // Contenido del mensaje
  },
  "metadata": {
    "message_id": "msg_1234567890_12345",
    "timestamp": 1640995200.0,
    "source_service": "mi_servicio",
    "correlation_id": "corr_123",
    "reply_to": "respuesta_cola",
    "priority": "NORMAL",
    "ttl": 3600,
    "headers": {
      "custom_header": "valor"
    }
  }
}
```

## Patrones de Uso

### 1. Event-Driven Architecture

```python
# Publicar eventos
await publisher.publish(
    message={"event": "user_registered", "user_id": 123},
    routing_key="users.registered",
    source_service="users_service"
)

# Suscribirse a eventos
await subscriber.subscribe(
    queue_name="email_notifications",
    handler=send_welcome_email,
    routing_keys=["users.registered"]
)
```

### 2. Command Pattern

```python
# Enviar comando
await publisher.publish(
    message={"command": "process_image", "image_id": 456},
    routing_key="commands.image_processing",
    priority=MessagePriority.HIGH,
    source_service="web_service"
)

# Procesar comando
await subscriber.subscribe(
    queue_name="image_processor",
    handler=process_image_command,
    routing_keys=["commands.image_processing"]
)
```

### 3. Saga Pattern

```python
# Iniciar saga
await publisher.publish(
    message={"saga_id": "saga_123", "step": "create_order"},
    routing_key="saga.order_creation",
    correlation_id="saga_123",
    source_service="order_service"
)

# Suscribirse a pasos de saga
await subscriber.subscribe(
    queue_name="order_saga_handler",
    handler=handle_order_saga_step,
    routing_keys=["saga.*"]
)
```

## Monitoreo y Logging

### Health Checks

```python
# Verificar estado de la conexión
health = await client.health_check()
if health["status"] == "healthy":
    print("Conexión activa")
else:
    print(f"Problema: {health['message']}")
```

### Logging

El módulo incluye logging automático para:

- Conexiones y desconexiones
- Publicación de mensajes
- Recepción de mensajes
- Errores y excepciones
- Reconexiones automáticas

### Métricas

```python
# Obtener estadísticas
print(f"Colas activas: {subscriber.active_queues}")
print(f"Conectado: {client.is_connected}")
print(f"Suscrito: {subscriber.is_subscribed}")
```

## Docker y Despliegue

### Docker Compose

```yaml
version: '3.8'
services:
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: guest
      RABBITMQ_DEFAULT_PASS: guest
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq

volumes:
  rabbitmq_data:
```

### Variables de Entorno en Producción

```env
RABBITMQ_HOST=rabbitmq.production.com
RABBITMQ_USER=prod_user
RABBITMQ_PASSWORD=prod_password
RABBITMQ_VHOST=/production
RABBITMQ_CONNECTION_TIMEOUT=60
RABBITMQ_HEARTBEAT=300
RABBITMQ_MAX_RETRIES=10
RABBITMQ_LOG_LEVEL=WARNING
```

## Testing

### Ejecutar Ejemplos

```bash
cd messaging_service
python -m examples
```

### Tests Unitarios

```bash
python -m pytest tests/
```

## Troubleshooting

### Problemas Comunes

1. **Error de conexión**: Verificar que RabbitMQ esté ejecutándose
2. **Mensajes perdidos**: Verificar configuración de colas durables
3. **Reconexiones frecuentes**: Ajustar heartbeat y timeout
4. **Mensajes no procesados**: Verificar manejadores y ACK

### Debug

```python
import logging
logging.getLogger("messaging_service").setLevel(logging.DEBUG)
```

## Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
