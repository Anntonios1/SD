"""
Broker Configuration and Connection Management
"""
import pika
import json
import os
from typing import Dict, Any, Callable


class BrokerConfig:
    """Configuration for RabbitMQ connection"""
    
    def __init__(self):
        self.host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.port = int(os.getenv('RABBITMQ_PORT', '5672'))
        self.user = os.getenv('RABBITMQ_USER', 'admin')
        self.password = os.getenv('RABBITMQ_PASS', 'admin123')
        
        # Queue names
        self.job_queue = 'gpu_jobs'
        self.result_queue = 'job_results'
        self.gpu_queue = 'gpu_worker_queue'
        self.cpu_queue = 'cpu_worker_queue'


class RabbitMQClient:
    """RabbitMQ client for publishing and consuming messages"""
    
    def __init__(self, config: BrokerConfig = None):
        self.config = config or BrokerConfig()
        self.connection = None
        self.channel = None
        
    def connect(self):
        """Establish connection to RabbitMQ"""
        credentials = pika.PlainCredentials(
            self.config.user, 
            self.config.password
        )
        parameters = pika.ConnectionParameters(
            host=self.config.host,
            port=self.config.port,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )
        
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        
        # Declare queues
        self.channel.queue_declare(queue=self.config.job_queue, durable=True)
        self.channel.queue_declare(queue=self.config.result_queue, durable=True)
        self.channel.queue_declare(queue=self.config.gpu_queue, durable=True)
        self.channel.queue_declare(queue=self.config.cpu_queue, durable=True)
        
        print(f"✓ Connected to RabbitMQ at {self.config.host}:{self.config.port}")
        
    def publish_job(self, job_data: Dict[str, Any], queue_name: str = None):
        """Publish a job to the queue"""
        if not self.channel:
            self.connect()
            
        queue = queue_name or self.config.job_queue
        message = json.dumps(job_data)
        
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
                content_type='application/json'
            )
        )
        
        print(f"✓ Job published to {queue}: {job_data.get('job_id', 'N/A')}")
        
    def publish_result(self, result_data: Dict[str, Any]):
        """Publish job result"""
        self.publish_job(result_data, self.config.result_queue)
        
    def consume(self, queue_name: str, callback: Callable):
        """Consume messages from a queue"""
        if not self.channel:
            self.connect()
            
        def on_message(ch, method, properties, body):
            try:
                message = json.loads(body)
                callback(message)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print(f"✗ Error processing message: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=on_message
        )
        
        print(f"⏳ Waiting for messages in {queue_name}...")
        self.channel.start_consuming()
        
    def close(self):
        """Close connection"""
        if self.connection:
            self.connection.close()
            print("✓ Connection closed")


if __name__ == "__main__":
    # Test connection
    client = RabbitMQClient()
    try:
        client.connect()
        print("✓ Broker connection test successful!")
    except Exception as e:
        print(f"✗ Connection failed: {e}")
    finally:
        client.close()
