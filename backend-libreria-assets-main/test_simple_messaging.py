#!/usr/bin/env python3
"""
Prueba simple del módulo de mensajería (sin cancelación)
"""

import asyncio
import logging
from messaging_service import MessagingClient, MessagePublisher, MessageSubscriber, MessagePriority

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_simple_messaging():
    """Prueba simple de mensajería"""
    logger.info("=== PRUEBA SIMPLE DE MENSAJERÍA ===")
    
    client = MessagingClient()
    
    try:
        # Conectar
        await client.connect()
        logger.info("✅ Conexión establecida")
        
        # Health check
        health = await client.health_check()
        logger.info(f"✅ Health check: {health['status']}")
        
        # Crear publicador
        publisher = MessagePublisher(client)
        
        # Publicar mensajes de prueba
        message_id1 = await publisher.publish(
            message={"text": "Hola desde prueba simple", "number": 42},
            routing_key="test.simple",
            source_service="test_simple"
        )
        
        message_id2 = await publisher.publish(
            message={"text": "Mensaje con prioridad", "number": 100},
            routing_key="test.priority",
            priority=MessagePriority.HIGH,
            source_service="test_simple"
        )
        
        logger.info(f"✅ Mensajes publicados exitosamente:")
        logger.info(f"   - Mensaje 1: {message_id1}")
        logger.info(f"   - Mensaje 2: {message_id2}")
        
        # Cerrar publicador
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
    asyncio.run(test_simple_messaging())
