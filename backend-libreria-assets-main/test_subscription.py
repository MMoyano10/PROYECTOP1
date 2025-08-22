#!/usr/bin/env python3
"""
Prueba de suscripción del módulo de mensajería
"""

import asyncio
import logging
from messaging_service import MessagingClient, MessagePublisher, MessageSubscriber, MessagePriority

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_subscription():
    """Prueba de suscripción y recepción de mensajes"""
    logger.info("=== PRUEBA DE SUSCRIPCIÓN ===")
    
    client = MessagingClient()
    messages_received = []
    
    try:
        # Conectar
        await client.connect()
        logger.info("✅ Conexión establecida")
        
        # Crear suscriptor
        subscriber = MessageSubscriber(client)
        
        # Manejador de mensajes
        async def message_handler(data, metadata):
            messages_received.append((data, metadata))
            logger.info(f"📨 Mensaje recibido: {data}")
            logger.info(f"📋 Metadatos: {metadata.get('message_id', 'unknown')}")
        
        # Suscribirse a cola de prueba
        await subscriber.subscribe(
            queue_name="test_subscription_queue",
            handler=message_handler,
            routing_keys=["subscription.*"],
            auto_ack=True  # Auto ACK para simplificar
        )
        logger.info("✅ Suscripción configurada")
        
        # Crear publicador
        publisher = MessagePublisher(client)
        
        # Publicar mensajes de prueba
        message_id1 = await publisher.publish(
            message={"text": "Mensaje de suscripción 1", "number": 123},
            routing_key="subscription.test1",
            source_service="test_subscription"
        )
        
        message_id2 = await publisher.publish(
            message={"text": "Mensaje de suscripción 2", "number": 456},
            routing_key="subscription.test2",
            priority=MessagePriority.HIGH,
            source_service="test_subscription"
        )
        
        logger.info(f"✅ Mensajes publicados: {message_id1}, {message_id2}")
        
        # Esperar procesamiento
        logger.info("⏳ Esperando mensajes...")
        await asyncio.sleep(5)
        
        # Verificar mensajes recibidos
        if len(messages_received) >= 2:
            logger.info(f"✅ Todos los mensajes fueron recibidos ({len(messages_received)})")
        else:
            logger.warning(f"⚠️ Solo se recibieron {len(messages_received)} mensajes")
            
        # Cerrar publicador (sin cerrar suscriptor para evitar errores)
        await publisher.close()
        logger.info("✅ Publicador cerrado")
        
    except Exception as e:
        logger.error(f"❌ Error en prueba: {e}")
        raise
    finally:
        # Desconectar
        await client.disconnect()
        logger.info("✅ Cliente desconectado")

if __name__ == "__main__":
    asyncio.run(test_subscription())
