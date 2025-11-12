"""
Job definitions for GPU/CPU execution
"""
import torch
import numpy as np
import time
from typing import Dict, Any


class JobExecutor:
    """Base class for job execution"""
    
    def __init__(self, use_gpu: bool = False):
        self.use_gpu = use_gpu and torch.cuda.is_available()
        self.device = torch.device('cuda' if self.use_gpu else 'cpu')
        
        if self.use_gpu:
            print(f"✓ GPU available: {torch.cuda.get_device_name(0)}")
        else:
            print("✓ Using CPU")
    
    def execute(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a job based on its type"""
        job_type = job_data.get('job_type')
        
        if job_type == 'matrix_multiply':
            return self.matrix_multiply(job_data)
        elif job_type == 'neural_network':
            return self.neural_network_training(job_data)
        elif job_type == 'vector_add':
            return self.vector_addition(job_data)
        elif job_type == 'image_processing':
            return self.image_processing(job_data)
        else:
            raise ValueError(f"Unknown job type: {job_type}")
    
    def matrix_multiply(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Matrix multiplication benchmark"""
        size = job_data.get('size', 1000)
        iterations = job_data.get('iterations', 10)
        
        print(f"Running matrix multiplication: {size}x{size}, {iterations} iterations")
        
        # Create random matrices
        a = torch.randn(size, size, device=self.device)
        b = torch.randn(size, size, device=self.device)
        
        # Warm-up
        if self.use_gpu:
            torch.cuda.synchronize()
            _ = torch.matmul(a, b)
            torch.cuda.synchronize()
        
        # Benchmark
        start_time = time.time()
        
        for _ in range(iterations):
            c = torch.matmul(a, b)
            if self.use_gpu:
                torch.cuda.synchronize()
        
        elapsed = time.time() - start_time
        avg_time = elapsed / iterations
        
        result = {
            'job_type': 'matrix_multiply',
            'size': size,
            'iterations': iterations,
            'total_time': elapsed,
            'avg_time_per_iteration': avg_time,
            'device': str(self.device),
            'result_shape': list(c.shape),
            'gflops': (2 * size ** 3 * iterations) / (elapsed * 1e9)
        }
        
        print(f"✓ Completed in {elapsed:.4f}s (avg: {avg_time:.4f}s)")
        return result
    
    def neural_network_training(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simple neural network training"""
        batch_size = job_data.get('batch_size', 64)
        input_size = job_data.get('input_size', 784)
        hidden_size = job_data.get('hidden_size', 256)
        output_size = job_data.get('output_size', 10)
        epochs = job_data.get('epochs', 5)
        
        print(f"Training neural network: {epochs} epochs")
        
        # Simple 2-layer network
        model = torch.nn.Sequential(
            torch.nn.Linear(input_size, hidden_size),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_size, output_size)
        ).to(self.device)
        
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        criterion = torch.nn.CrossEntropyLoss()
        
        # Dummy data
        X = torch.randn(batch_size * 100, input_size, device=self.device)
        y = torch.randint(0, output_size, (batch_size * 100,), device=self.device)
        
        start_time = time.time()
        
        for epoch in range(epochs):
            for i in range(0, len(X), batch_size):
                batch_X = X[i:i+batch_size]
                batch_y = y[i:i+batch_size]
                
                optimizer.zero_grad()
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
        
        if self.use_gpu:
            torch.cuda.synchronize()
            
        elapsed = time.time() - start_time
        
        result = {
            'job_type': 'neural_network',
            'epochs': epochs,
            'batch_size': batch_size,
            'training_time': elapsed,
            'device': str(self.device),
            'final_loss': loss.item()
        }
        
        print(f"✓ Training completed in {elapsed:.4f}s")
        return result
    
    def vector_addition(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simple vector addition benchmark"""
        size = job_data.get('size', 10000000)
        iterations = job_data.get('iterations', 100)
        
        print(f"Running vector addition: size={size}, iterations={iterations}")
        
        a = torch.randn(size, device=self.device)
        b = torch.randn(size, device=self.device)
        
        start_time = time.time()
        
        for _ in range(iterations):
            c = a + b
            if self.use_gpu:
                torch.cuda.synchronize()
        
        elapsed = time.time() - start_time
        
        result = {
            'job_type': 'vector_add',
            'size': size,
            'iterations': iterations,
            'total_time': elapsed,
            'device': str(self.device)
        }
        
        print(f"✓ Completed in {elapsed:.4f}s")
        return result
    
    def image_processing(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Image processing with convolutions"""
        batch_size = job_data.get('batch_size', 32)
        image_size = job_data.get('image_size', 224)
        iterations = job_data.get('iterations', 50)
        
        print(f"Running image processing: {batch_size}x{image_size}x{image_size}")
        
        # Create dummy images (batch, channels, height, width)
        images = torch.randn(batch_size, 3, image_size, image_size, device=self.device)
        
        # Simple conv layer
        conv = torch.nn.Conv2d(3, 64, kernel_size=3, padding=1).to(self.device)
        
        start_time = time.time()
        
        for _ in range(iterations):
            output = conv(images)
            if self.use_gpu:
                torch.cuda.synchronize()
        
        elapsed = time.time() - start_time
        
        result = {
            'job_type': 'image_processing',
            'batch_size': batch_size,
            'image_size': image_size,
            'iterations': iterations,
            'total_time': elapsed,
            'device': str(self.device)
        }
        
        print(f"✓ Completed in {elapsed:.4f}s")
        return result
