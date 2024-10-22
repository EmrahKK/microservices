import pika
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# RabbitMQ connection settings from environment variables
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE', 'keda-produce')
RABBITMQ_ROUTING_KEY = os.getenv('RABBITMQ_ROUTING_KEY', 'keda')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'keda')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'keda')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'kedapassword')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', 'my_vhost')

def callback(ch, method, properties, body):
    """Callback function to process messages received from RabbitMQ."""
    logging.info(f"Received message: {body.decode()}")

def consume_messages():
    """Connect to RabbitMQ and start consuming messages."""
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST,5672,RABBITMQ_VHOST,credentials))
        channel = connection.channel()

        # Declare the exchange if it doesn't exist (topic type)
        channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type='topic', durable=True)

        # Declare the queue and bind it to the exchange with the given routing key
        result = channel.queue_declare(queue=RABBITMQ_QUEUE, exclusive=False, durable=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=RABBITMQ_EXCHANGE, queue=queue_name, routing_key=RABBITMQ_ROUTING_KEY)

        logging.info(f"Connected to RabbitMQ. Consuming messages from exchange '{RABBITMQ_EXCHANGE}' with queue '{queue_name}'.")

        # Start consuming messages
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        logging.info("Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()

    except Exception as e:
        logging.error(f"Error occurred: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    consume_messages()
