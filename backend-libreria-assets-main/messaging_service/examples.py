"""
Ejemplos de uso del módulo de mensajería RabbitMQ
"""

import asyncio
import logging
from typing import Dict, Any

from .messaging_client import MessagingClient
from .message_publisher import MessagePublisher, MessagePriority
from .message_subscriber import MessageSubscriber
from .config import MessagingConfig


# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def example_basic_pub_sub():
    """Ejemplo básico de publicación y suscripción"""
    logger.info("=== Ejemplo Básico de Pub/Sub ===")
    
    # Crear cliente de mensajería
    client = MessagingClient()
    
    try:
        # Conectar a RabbitMQ
        await client.connect()
        
        # Crear publicador y suscriptor
        publisher = MessagePublisher(client)
        subscriber = MessageSubscriber(client)
        
        # Definir manejador de mensajes
        async def message_handler(data: Dict[str, Any], metadata: Dict[str, Any]):
            logger.info(f"Mensaje recibido: {data}")
            logger.info(f"Metadatos: {metadata}")
        
        # Suscribirse a una cola
        await subscriber.subscribe(
            queue_name="example_queue",
            handler=message_handler,
            routing_keys=["example.*"]
        )
        
        # Publicar mensajes
        message_id1 = await publisher.publish(
            message={"text": "Hola mundo!", "number": 42},
            routing_key="example.hello",
            source_service="example_service"
        )
        
        message_id2 = await publisher.publish(
            message={"text": "Segundo mensaje", "number": 100},
            routing_key="example.second",
            priority=MessagePriority.HIGH,
            source_service="example_service"
        )
        
        logger.info(f"Mensajes publicados: {message_id1}, {message_id2}")
        
        # Esperar un poco para procesar mensajes
        await asyncio.sleep(2)
        
        # Limpiar
        await subscriber.close()
        await publisher.close()
        
    finally:
        await client.disconnect()


async def example_rpc():
    """Ejemplo de comunicación RPC (Request-Response)"""
    logger.info("=== Ejemplo de RPC ===")
    
    client = MessagingClient()
    
    try:
        await client.connect()
        
        # Servidor RPC
        async def rpc_handler(data: Dict[str, Any], metadata: Dict[str, Any]):
            logger.info(f"RPC recibido: {data}")
            
            # Simular procesamiento
            result = {"result": data.get("number", 0) * 2, "processed": True}
            
            # Enviar respuesta usando el reply_to del mensaje
            if metadata.get("reply_to"):
                publisher = MessagePublisher(client)
                await publisher.publish(
                    message=result,
                    routing_key=metadata["reply_to"],
                    correlation_id=metadata.get("correlation_id")
                )
                await publisher.close()
        
        # Suscribirse como servidor RPC
        subscriber = MessageSubscriber(client)
        await subscriber.subscribe(
            queue_name="rpc_server_queue",
            handler=rpc_handler,
            routing_keys=["rpc.multiply"]
        )
        
        # Cliente RPC
        publisher = MessagePublisher(client)
        
        # Crear cola temporal para respuestas
        response_queue = await subscriber.subscribe_to_exchange(
            exchange_name="libreria_assets",
            handler=lambda data, metadata: logger.info(f"Respuesta RPC: {data}"),
            routing_keys=["rpc.response"]
        )
        
        # Enviar solicitud RPC
        message_id = await publisher.publish(
            message={"number": 21, "operation": "multiply"},
            routing_key="rpc.multiply",
            reply_to=response_queue,
            correlation_id="req_123",
            source_service="rpc_client"
        )
        
        logger.info(f"Solicitud RPC enviada: {message_id}")
        
        # Esperar respuesta
        await asyncio.sleep(3)
        
        # Limpiar
        await subscriber.close()
        await publisher.close()
        
    finally:
        await client.disconnect()


async def example_batch_publishing():
    """Ejemplo de publicación por lotes"""
    logger.info("=== Ejemplo de Publicación por Lotes ===")
    
    client = MessagingClient()
    
    try:
        await client.connect()
        publisher = MessagePublisher(client)
        
        # Preparar mensajes en lote
        messages = [
            ({"id": 1, "action": "create", "data": "item1"}, "assets.create"),
            ({"id": 2, "action": "update", "data": "item2"}, "assets.update"),
            ({"id": 3, "action": "delete", "data": "item3"}, "assets.delete"),
        ]
        
        # Publicar en lote
        message_ids = await publisher.publish_batch(
            messages=messages,
            source_service="batch_service",
            priority=MessagePriority.NORMAL
        )
        
        logger.info(f"Mensajes publicados en lote: {message_ids}")
        
        await publisher.close()
        
    finally:
        await client.disconnect()


async def example_priority_messages():
    """Ejemplo de mensajes con prioridad"""
    logger.info("=== Ejemplo de Mensajes con Prioridad ===")
    
    client = MessagingClient()
    
    try:
        await client.connect()
        
        publisher = MessagePublisher(client)
        subscriber = MessageSubscriber(client)
        
        # Manejador que procesa mensajes por prioridad
        async def priority_handler(data: Dict[str, Any], metadata: Dict[str, Any]):
            priority = metadata.get("priority", "NORMAL")
            logger.info(f"Procesando mensaje con prioridad {priority}: {data}")
        
        # Suscribirse a cola de prioridad
        await subscriber.subscribe(
            queue_name="priority_queue",
            handler=priority_handler,
            routing_keys=["priority.*"]
        )
        
        # Publicar mensajes con diferentes prioridades
        priorities = [
            MessagePriority.LOW,
            MessagePriority.NORMAL,
            MessagePriority.HIGH,
            MessagePriority.CRITICAL
        ]
        
        for i, priority in enumerate(priorities):
            await publisher.publish(
                message={"order": i, "content": f"Mensaje {priority.name}"},
                routing_key=f"priority.{priority.name.lower()}",
                priority=priority,
                source_service="priority_service"
            )
        
        # Esperar procesamiento
        await asyncio.sleep(3)
        
        await subscriber.close()
        await publisher.close()
        
    finally:
        await client.disconnect()


async def example_health_check():
    """Ejemplo de verificación de salud de la conexión"""
    logger.info("=== Ejemplo de Health Check ===")
    
    client = MessagingClient()
    
    try:
        # Verificar estado antes de conectar
        health = await client.health_check()
        logger.info(f"Estado antes de conectar: {health}")
        
        # Conectar
        await client.connect()
        
        # Verificar estado después de conectar
        health = await client.health_check()
        logger.info(f"Estado después de conectar: {health}")
        
        # Verificar estado del canal
        if client.channel:
            logger.info(f"Canal activo: {not client.channel.is_closed}")
            logger.info(f"QoS configurado: {client.channel._qos}")
        
    finally:
        await client.disconnect()


async def main():
    """Función principal que ejecuta todos los ejemplos"""
    logger.info("Iniciando ejemplos del módulo de mensajería...")
    
    try:
        # Ejecutar ejemplos
        await example_basic_pub_sub()
        await asyncio.sleep(1)
        
        await example_rpc()
        await asyncio.sleep(1)
        
        await example_batch_publishing()
        await asyncio.sleep(1)
        
        await example_priority_messages()
        await asyncio.sleep(1)
        
        await example_health_check()
        
        logger.info("Todos los ejemplos completados exitosamente!")
        
    except Exception as e:
        logger.error(f"Error ejecutando ejemplos: {e}")


if __name__ == "__main__":
    # Ejecutar ejemplos
    asyncio.run(main())
