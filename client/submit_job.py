"""
Client - Submit jobs to the system
"""
import sys
import os
import uuid
from datetime import datetime
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from broker.broker_client import RabbitMQClient, BrokerConfig


class JobClient:
    """Client for submitting jobs to the distributed system"""
    
    def __init__(self):
        self.broker = RabbitMQClient()
        self.config = BrokerConfig()
        
    def submit_job(self, job_type: str, params: dict, prefer_gpu: bool = True):
        """Submit a job to the system"""
        job_id = f"job-{uuid.uuid4().hex[:12]}"
        
        job_data = {
            'job_id': job_id,
            'job_type': job_type,
            'submit_time': datetime.now().isoformat(),
            'prefer_gpu': prefer_gpu,
            **params
        }
        
        print(f"\n📤 Submitting job {job_id}")
        print(f"   Type: {job_type}")
        print(f"   Prefer GPU: {prefer_gpu}")
        print(f"   Parameters: {params}")
        
        self.broker.connect()
        self.broker.publish_job(job_data, self.config.job_queue)
        self.broker.close()
        
        print(f"✓ Job submitted successfully!")
        return job_id
    
    def submit_matrix_multiply(self, size: int = 1000, iterations: int = 10, prefer_gpu: bool = True):
        """Submit a matrix multiplication job"""
        return self.submit_job('matrix_multiply', {
            'size': size,
            'iterations': iterations
        }, prefer_gpu)
    
    def submit_neural_network(self, epochs: int = 5, batch_size: int = 64, prefer_gpu: bool = True):
        """Submit a neural network training job"""
        return self.submit_job('neural_network', {
            'epochs': epochs,
            'batch_size': batch_size,
            'input_size': 784,
            'hidden_size': 256,
            'output_size': 10
        }, prefer_gpu)
    
    def submit_vector_add(self, size: int = 10000000, iterations: int = 100, prefer_gpu: bool = True):
        """Submit a vector addition job"""
        return self.submit_job('vector_add', {
            'size': size,
            'iterations': iterations
        }, prefer_gpu)
    
    def submit_image_processing(self, batch_size: int = 32, image_size: int = 224, 
                               iterations: int = 50, prefer_gpu: bool = True):
        """Submit an image processing job"""
        return self.submit_job('image_processing', {
            'batch_size': batch_size,
            'image_size': image_size,
            'iterations': iterations
        }, prefer_gpu)


def main():
    """Example usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Submit jobs to the GPU cluster')
    parser.add_argument('--job-type', type=str, required=True,
                       choices=['matrix-multiply', 'neural-network', 'vector-add', 'image-processing'],
                       help='Type of job to submit')
    parser.add_argument('--size', type=int, default=1000,
                       help='Size parameter for matrix/vector operations')
    parser.add_argument('--iterations', type=int, default=10,
                       help='Number of iterations')
    parser.add_argument('--epochs', type=int, default=5,
                       help='Number of epochs for neural network')
    parser.add_argument('--batch-size', type=int, default=64,
                       help='Batch size')
    parser.add_argument('--cpu', action='store_true',
                       help='Prefer CPU instead of GPU')
    parser.add_argument('--count', type=int, default=1,
                       help='Number of jobs to submit')
    
    args = parser.parse_args()
    
    client = JobClient()
    prefer_gpu = not args.cpu
    
    print(f"\n{'='*60}")
    print(f"🚀 Job Submission Client")
    print(f"{'='*60}")
    
    job_ids = []
    
    for i in range(args.count):
        if args.count > 1:
            print(f"\nSubmitting job {i+1}/{args.count}...")
            
        if args.job_type == 'matrix-multiply':
            job_id = client.submit_matrix_multiply(args.size, args.iterations, prefer_gpu)
        elif args.job_type == 'neural-network':
            job_id = client.submit_neural_network(args.epochs, args.batch_size, prefer_gpu)
        elif args.job_type == 'vector-add':
            job_id = client.submit_vector_add(args.size, args.iterations, prefer_gpu)
        elif args.job_type == 'image-processing':
            job_id = client.submit_image_processing(args.batch_size, args.size, args.iterations, prefer_gpu)
        
        job_ids.append(job_id)
        
        if i < args.count - 1:
            time.sleep(0.1)  # Small delay between submissions
    
    print(f"\n{'='*60}")
    print(f"✅ All jobs submitted!")
    print(f"   Total jobs: {len(job_ids)}")
    print(f"   Job IDs: {', '.join(job_ids)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
