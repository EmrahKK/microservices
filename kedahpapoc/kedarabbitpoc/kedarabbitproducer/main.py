from fastapi import FastAPI, HTTPException
import psutil
import time
import pika
import json
import os

app = FastAPI()

# Load RabbitMQ configuration from environment variables
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE', 'keda-produce')
RABBITMQ_ROUTING_KEY = os.getenv('RABBITMQ_ROUTING_KEY', 'keda')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'keda')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'keda')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'kedapassword')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', 'my_vhost')

# RabbitMQ connection setup
def get_rabbitmq_connection():
    
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST,5672,RABBITMQ_VHOST,credentials))
        return connection
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to RabbitMQ: {str(e)}")

# Endpoint 1: Service status and system information
@app.get("/status")
def get_status():
    uptime = time.time() - psutil.boot_time()
    free_memory = psutil.virtual_memory().available
    total_memory = psutil.virtual_memory().total
    cpu_count = psutil.cpu_count()

    return {
        "message": "Service is up and running",
        "uptime": f"{int(uptime)} seconds",
        "system_info": {
            "total_memory": f"{total_memory / 1024 / 1024:.2f} MB",
            "free_memory": f"{free_memory / 1024 / 1024:.2f} MB",
            "cpus": cpu_count,
        }
    }

# Endpoint 2: Publish message to RabbitMQ topic
@app.post("/publish")
def publish_message(message: str):
    # Connect to RabbitMQ
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    # Declare exchange
    channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type='topic', durable=True)

    # Publish message
    try:
        channel.basic_publish(
            exchange=RABBITMQ_EXCHANGE,
            routing_key=RABBITMQ_ROUTING_KEY,
            body=json.dumps({"message": message})
        )
        connection.close()
        return {"message": "Message published to RabbitMQ", "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish message: {str(e)}")

