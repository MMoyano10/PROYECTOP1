# Inicio Rápido - Módulo de Mensajería RabbitMQ

## 🚀 Configuración en 5 minutos

### 1. Instalar dependencias

```bash
cd backend-libreria-assets-main
pip install -r messaging_service/requirements.txt
```

### 2. Configurar RabbitMQ

#### Opción A: Docker (Recomendado)
```bash
# Iniciar solo RabbitMQ
docker run -d --name rabbitmq \
  -p 5672:5672 \
  -p 15672:15672 \
  rabbitmq:3-management

# O usar docker-compose
docker-compose up rabbitmq -d
```

#### Opción B: Instalación local
- Descargar e instalar RabbitMQ desde [rabbitmq.com](https://rabbitmq.com/download.html)
- Habilitar el plugin de gestión: `rabbitmq-plugins enable rabbitmq_management`

### 3. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar .env con tu configuración
nano .env
```

### 4. Probar la conexión

```bash
# Ejecutar script de prueba
python test_messaging.py
```

## 📝 Ejemplo básico

```python
import asyncio
from messaging_service import MessagingClient, MessagePublisher, MessageSubscriber

async def main():
    # Crear cliente
    client = MessagingClient()
    await client.connect()
    
    # Crear publicador y suscriptor
    publisher = MessagePublisher(client)
    subscriber = MessageSubscriber(client)
    
    # Manejador de mensajes
    async def handle_message(data, metadata):
        print(f"Mensaje recibido: {data}")
    
    # Suscribirse a cola
    await subscriber.subscribe(
        queue_name="mi_cola",
        handler=handle_message,
        routing_keys=["events.*"]
    )
    
    # Publicar mensaje
    message_id = await publisher.publish(
        message={"text": "Hola mundo!"},
        routing_key="events.hello",
        source_service="mi_servicio"
    )
    
    print(f"Mensaje publicado: {message_id}")
    
    # Esperar y limpiar
    await asyncio.sleep(2)
    await subscriber.close()
    await publisher.close()
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔧 Integración con servicios existentes

### Assets Service

```python
# En assets_service/main.py
from messaging_service import MessagingClient, MessagePublisher

# Inicializar mensajería
messaging_client = MessagingClient()
publisher = MessagePublisher(messaging_client)

# Notificar eventos
async def create_asset(asset_data):
    # Lógica de creación...
    
    # Notificar a otros servicios
    await publisher.publish(
        message={"action": "created", "asset": asset_data},
        routing_key="assets.created",
        source_service="assets_service"
    )
```

### Categories Service

```python
# En categories_service/main.py
from messaging_service import MessagingClient, MessageSubscriber

# Suscribirse a eventos
async def handle_asset_event(data, metadata):
    if data.get("action") == "created":
        # Procesar nuevo asset
        pass

subscriber = MessageSubscriber(messaging_client)
await subscriber.subscribe(
    queue_name="categories_asset_events",
    handler=handle_asset_event,
    routing_keys=["assets.*"]
)
```

## 📊 Monitoreo

### Health Check
```python
health = await client.health_check()
print(f"Estado: {health['status']}")
```

### RabbitMQ Management UI
- URL: http://localhost:15672
- Usuario: guest
- Contraseña: guest

## 🐛 Troubleshooting

### Error de conexión
```bash
# Verificar que RabbitMQ esté ejecutándose
docker ps | grep rabbitmq

# Ver logs
docker logs rabbitmq
```

### Mensajes no recibidos
```python
# Verificar suscripciones
print(f"Colas activas: {subscriber.active_queues}")
print(f"Suscrito: {subscriber.is_subscribed}")
```

### Debug
```python
import logging
logging.getLogger("messaging_service").setLevel(logging.DEBUG)
```

## 📚 Próximos pasos

1. **Leer la documentación completa**: [README.md](README.md)
2. **Explorar ejemplos**: [examples.py](examples.py)
3. **Integrar en tu servicio**: Ver [messaging_integration.py](../assets_service/messaging_integration.py)
4. **Ejecutar pruebas**: `python test_messaging.py`

## 🆘 Soporte

- **Documentación**: [README.md](README.md)
- **Ejemplos**: [examples.py](examples.py)
- **Pruebas**: [test_messaging.py](../test_messaging.py)
- **Integración**: [messaging_integration.py](../assets_service/messaging_integration.py)
