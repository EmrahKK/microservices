FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set default environment variables
ENV RABBITMQ_HOST=localhost
ENV RABBITMQ_EXCHANGE=my_exchange
ENV RABBITMQ_QUEUE=my_queue
ENV RABBITMQ_ROUTING_KEY="#"

# Command to run the consumer
CMD ["python", "main.py"]