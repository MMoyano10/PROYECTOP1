#!/usr/bin/env python3
"""
Script de prueba para el módulo de mensajería RabbitMQ

Este script demuestra las funcionalidades principales del módulo
y cómo se integra con los servicios existentes.
"""

import asyncio
import logging
import sys
import os
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from messaging_service import (
    MessagingClient, 
    MessagePublisher, 
    MessageSubscriber,
    MessagePriority
)
from assets_service.messaging_integration import AssetsMessagingIntegration


async def test_basic_messaging():
    """Prueba básica de mensajería"""
    logger.info("=== PRUEBA BÁSICA DE MENSAJERÍA ===")
    
    client = MessagingClient()
    
    try:
        # Conectar
        await client.connect()
        logger.info("✅ Conexión establecida")
        
        # Health check
        health = await client.health_check()
        logger.info(f"✅ Health check: {health['status']}")
        
        # Crear publicador y suscriptor
        publisher = MessagePublisher(client)
        subscriber = MessageSubscriber(client)
        
        # Contador de mensajes recibidos
        messages_received = []
        
        # Manejador de mensajes
        async def message_handler(data, metadata):
            messages_received.append((data, metadata))
            logger.info(f"📨 Mensaje recibido: {data}")
            logger.info(f"📋 Metadatos: {metadata}")
        
        # Suscribirse a cola de prueba
        await subscriber.subscribe(
            queue_name="test_queue",
            handler=message_handler,
            routing_keys=["test.*"]
        )
        logger.info("✅ Suscripción configurada")
        
        # Publicar mensajes de prueba
        message1 = await publisher.publish(
            message={"text": "Hola desde prueba", "number": 42},
            routing_key="test.hello",
            source_service="test_script"
        )
        
        message2 = await publisher.publish(
            message={"text": "Segundo mensaje", "number": 100},
            routing_key="test.second",
            priority=MessagePriority.HIGH,
            source_service="test_script"
        )
        
        logger.info(f"✅ Mensajes publicados: {message1}, {message2}")
        
        # Esperar procesamiento
        await asyncio.sleep(3)
        
        # Verificar mensajes recibidos
        if len(messages_received) == 2:
            logger.info("✅ Todos los mensajes fueron recibidos correctamente")
        else:
            logger.warning(f"⚠️ Solo se recibieron {len(messages_received)} de 2 mensajes")
        
        # Limpiar
        await subscriber.close()
        await publisher.close()
        
    except Exception as e:
        logger.error(f"❌ Error en prueba básica: {e}")
        raise
    finally:
        await client.disconnect()
        logger.info("🔌 Conexión cerrada")


async def test_assets_messaging_integration():
    """Prueba de integración con el servicio de assets"""
    logger.info("=== PRUEBA DE INTEGRACIÓN CON ASSETS SERVICE ===")
    
    try:
        # Inicializar integración
        assets_messaging = AssetsMessagingIntegration()
        await assets_messaging.initialize()
        logger.info("✅ Integración de assets inicializada")
        
        # Health check
        health = await assets_messaging.health_check()
        logger.info(f"✅ Health check de assets: {health['status']}")
        
        # Simular eventos de assets
        asset_data = {
            "id": 1,
            "name": "Imagen de prueba",
            "description": "Descripción de prueba",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Notificar creación de asset
        message_id = await assets_messaging.notify_asset_created(asset_data)
        logger.info(f"✅ Evento de asset creado: {message_id}")
        
        # Notificar actualización de asset
        asset_data["description"] = "Descripción actualizada"
        asset_data["updated_at"] = datetime.now().isoformat()
        message_id = await assets_messaging.notify_asset_updated(asset_data)
        logger.info(f"✅ Evento de asset actualizado: {message_id}")
        
        # Notificar eliminación de asset
        message_id = await assets_messaging.notify_asset_deleted(asset_data["id"])
        logger.info(f"✅ Evento de asset eliminado: {message_id}")
        
        # Esperar un poco para procesar mensajes
        await asyncio.sleep(2)
        
        # Cerrar integración
        await assets_messaging.close()
        logger.info("✅ Integración de assets cerrada")
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de integración: {e}")
        raise


async def test_rpc_communication():
    """Prueba de comunicación RPC"""
    logger.info("=== PRUEBA DE COMUNICACIÓN RPC ===")
    
    client = MessagingClient()
    
    try:
        await client.connect()
        
        # Servidor RPC
        async def rpc_handler(data, metadata):
            logger.info(f"🔄 RPC recibido: {data}")
            
            # Simular procesamiento
            number = data.get("number", 0)
            result = {"result": number * 2, "processed": True, "timestamp": datetime.now().isoformat()}
            
            # Enviar respuesta
            if metadata.get("reply_to"):
                publisher = MessagePublisher(client)
                await publisher.publish(
                    message=result,
                    routing_key=metadata["reply_to"],
                    correlation_id=metadata.get("correlation_id"),
                    source_service="rpc_server"
                )
                await publisher.close()
                logger.info(f"📤 Respuesta RPC enviada: {result}")
        
        # Suscribirse como servidor RPC
        subscriber = MessageSubscriber(client)
        await subscriber.subscribe(
            queue_name="rpc_server_queue",
            handler=rpc_handler,
            routing_keys=["rpc.multiply"]
        )
        logger.info("✅ Servidor RPC configurado")
        
        # Cliente RPC
        publisher = MessagePublisher(client)
        
        # Crear cola temporal para respuestas
        response_queue = await subscriber.subscribe_to_exchange(
            exchange_name="libreria_assets",
            handler=lambda data, metadata: logger.info(f"📨 Respuesta RPC recibida: {data}"),
            routing_keys=["rpc.response"]
        )
        
        # Enviar solicitudes RPC
        test_numbers = [10, 25, 50]
        for number in test_numbers:
            message_id = await publisher.publish(
                message={"number": number, "operation": "multiply"},
                routing_key="rpc.multiply",
                reply_to=response_queue,
                correlation_id=f"req_{number}",
                source_service="rpc_client"
            )
            logger.info(f"📤 Solicitud RPC enviada para {number}: {message_id}")
        
        # Esperar respuestas
        await asyncio.sleep(5)
        
        # Limpiar
        await subscriber.close()
        await publisher.close()
        
    except Exception as e:
        logger.error(f"❌ Error en prueba RPC: {e}")
        raise
    finally:
        await client.disconnect()


async def test_priority_messages():
    """Prueba de mensajes con prioridad"""
    logger.info("=== PRUEBA DE MENSAJES CON PRIORIDAD ===")
    
    client = MessagingClient()
    
    try:
        await client.connect()
        
        publisher = MessagePublisher(client)
        subscriber = MessageSubscriber(client)
        
        # Manejador que procesa mensajes por prioridad
        async def priority_handler(data, metadata):
            priority = metadata.get("priority", "NORMAL")
            logger.info(f"🎯 Procesando mensaje con prioridad {priority}: {data}")
        
        # Suscribirse a cola de prioridad
        await subscriber.subscribe(
            queue_name="priority_test_queue",
            handler=priority_handler,
            routing_keys=["priority.*"]
        )
        
        # Publicar mensajes con diferentes prioridades
        priorities = [
            (MessagePriority.LOW, "baja"),
            (MessagePriority.NORMAL, "normal"),
            (MessagePriority.HIGH, "alta"),
            (MessagePriority.CRITICAL, "crítica")
        ]
        
        for priority, name in priorities:
            await publisher.publish(
                message={"order": priorities.index((priority, name)), "content": f"Mensaje {name}"},
                routing_key=f"priority.{name}",
                priority=priority,
                source_service="priority_test"
            )
            logger.info(f"📤 Mensaje con prioridad {name} enviado")
        
        # Esperar procesamiento
        await asyncio.sleep(3)
        
        await subscriber.close()
        await publisher.close()
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de prioridades: {e}")
        raise
    finally:
        await client.disconnect()


async def test_batch_publishing():
    """Prueba de publicación por lotes"""
    logger.info("=== PRUEBA DE PUBLICACIÓN POR LOTES ===")
    
    client = MessagingClient()
    
    try:
        await client.connect()
        publisher = MessagePublisher(client)
        
        # Preparar mensajes en lote
        messages = [
            ({"id": 1, "action": "create", "data": "item1"}, "batch.create"),
            ({"id": 2, "action": "update", "data": "item2"}, "batch.update"),
            ({"id": 3, "action": "delete", "data": "item3"}, "batch.delete"),
            ({"id": 4, "action": "process", "data": "item4"}, "batch.process"),
        ]
        
        # Publicar en lote
        message_ids = await publisher.publish_batch(
            messages=messages,
            source_service="batch_test_service",
            priority=MessagePriority.NORMAL
        )
        
        logger.info(f"✅ Mensajes publicados en lote: {message_ids}")
        
        await publisher.close()
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de lotes: {e}")
        raise
    finally:
        await client.disconnect()


async def main():
    """Función principal que ejecuta todas las pruebas"""
    logger.info("🚀 Iniciando pruebas del módulo de mensajería...")
    
    try:
        # Ejecutar pruebas en secuencia
        await test_basic_messaging()
        await asyncio.sleep(1)
        
        await test_assets_messaging_integration()
        await asyncio.sleep(1)
        
        await test_rpc_communication()
        await asyncio.sleep(1)
        
        await test_priority_messages()
        await asyncio.sleep(1)
        
        await test_batch_publishing()
        
        logger.info("🎉 Todas las pruebas completadas exitosamente!")
        
    except Exception as e:
        logger.error(f"💥 Error ejecutando pruebas: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Ejecutar pruebas
    asyncio.run(main())
