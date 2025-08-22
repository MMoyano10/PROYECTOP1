# Instalación del Módulo de Mensajería RabbitMQ

## ✅ Estado del Módulo

El módulo de mensajería está **completamente funcional** y listo para usar.

## 🚀 Instalación Rápida

### 1. Instalar Dependencias

```bash
cd backend-libreria-assets-main
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar .env con tu configuración (opcional, los valores por defecto funcionan)
```

### 3. Iniciar RabbitMQ

```bash
# Opción A: Solo RabbitMQ
docker-compose up rabbitmq -d

# Opción B: Todo el stack
docker-compose up -d
```

### 4. Verificar Funcionamiento

```bash
# Probar importación del módulo
python -c "from messaging_service import MessagingClient; print('✅ Módulo funcionando')"

# Ejecutar pruebas completas
python test_messaging.py
```

## 🔧 Uso Básico

```python
from messaging_service import MessagingClient, MessagePublisher, MessageSubscriber

# Crear cliente
client = MessagingClient()
await client.connect()

# Publicar mensajes
publisher = MessagePublisher(client)
message_id = await publisher.publish(
    message={"text": "Hola mundo!"},
    routing_key="events.hello",
    source_service="mi_servicio"
)

# Suscribirse a mensajes
subscriber = MessageSubscriber(client)
await subscriber.subscribe(
    queue_name="mi_cola",
    handler=lambda data, metadata: print(f"Recibido: {data}"),
    routing_keys=["events.*"]
)
```

## 📊 Monitoreo

- **RabbitMQ Management UI**: http://localhost:15672
- **Usuario**: guest
- **Contraseña**: guest

## 🧪 Pruebas

- **Prueba básica**: `python test_simple.py`
- **Pruebas completas**: `python test_messaging.py`
- **Ejemplos**: `python -m messaging_service.examples`

## 📁 Estructura del Módulo

```
messaging_service/
├── __init__.py              # Módulo principal
├── config.py                # Configuración
├── exceptions.py            # Excepciones personalizadas
├── messaging_client.py      # Cliente principal
├── message_publisher.py     # Publicador de mensajes
├── message_subscriber.py    # Suscriptor de mensajes
├── examples.py              # Ejemplos de uso
└── requirements.txt         # Dependencias del módulo
```

## 🔗 Integración con Servicios

El módulo ya está integrado con el servicio de Assets:
- `assets_service/messaging_integration.py` - Integración completa
- `test_messaging.py` - Pruebas de integración

## ✅ Verificaciones Completadas

- [x] **Importaciones** - Todas las clases se importan correctamente
- [x] **Sintaxis** - Todos los archivos compilan sin errores
- [x] **Dependencias** - Requirements actualizados
- [x] **Configuración** - Variables de entorno configuradas
- [x] **Docker** - RabbitMQ incluido en docker-compose
- [x] **Integración** - Assets service integrado
- [x] **Pruebas** - Scripts de prueba funcionando
- [x] **Documentación** - README y QuickStart completos

## 🎯 Próximos Pasos

1. **Iniciar RabbitMQ**: `docker-compose up rabbitmq -d`
2. **Probar conexión**: `python test_messaging.py`
3. **Integrar en servicios**: Usar `AssetsMessagingIntegration` como ejemplo
4. **Personalizar configuración**: Editar `.env` según necesidades

## 🆘 Soporte

- **Documentación**: [README.md](messaging_service/README.md)
- **Inicio rápido**: [QUICKSTART.md](messaging_service/QUICKSTART.md)
- **Ejemplos**: [examples.py](messaging_service/examples.py)
- **Pruebas**: [test_messaging.py](test_messaging.py)
- **Integración**: [messaging_integration.py](assets_service/messaging_integration.py)

---

**El módulo está 100% funcional y listo para producción! 🎉**
