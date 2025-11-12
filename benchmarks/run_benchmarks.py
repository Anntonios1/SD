"""
Benchmark script - Compare GPU vs CPU performance
"""
import sys
import os
import json
import time
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.submit_job import JobClient


class BenchmarkSuite:
    """Run benchmarks comparing GPU and CPU performance"""
    
    def __init__(self):
        self.client = JobClient()
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'benchmarks': []
        }
    
    def run_benchmark(self, job_type: str, params: dict, name: str):
        """Run a single benchmark on both GPU and CPU"""
        print(f"\n{'='*70}")
        print(f"🔬 Running benchmark: {name}")
        print(f"{'='*70}")
        
        benchmark_result = {
            'name': name,
            'job_type': job_type,
            'params': params,
            'gpu_job_id': None,
            'cpu_job_id': None
        }
        
        # Submit GPU job
        print("\n🎮 Submitting GPU job...")
        gpu_job_id = self.client.submit_job(job_type, params, prefer_gpu=True)
        benchmark_result['gpu_job_id'] = gpu_job_id
        time.sleep(1)
        
        # Submit CPU job
        print("💻 Submitting CPU job...")
        cpu_job_id = self.client.submit_job(job_type, params, prefer_gpu=False)
        benchmark_result['cpu_job_id'] = cpu_job_id
        
        self.results['benchmarks'].append(benchmark_result)
        
        print(f"\n✓ Benchmark submitted")
        print(f"  GPU Job: {gpu_job_id}")
        print(f"  CPU Job: {cpu_job_id}")
    
    def run_all_benchmarks(self):
        """Run complete benchmark suite"""
        print("\n" + "="*70)
        print("🚀 GPU vs CPU Benchmark Suite")
        print("="*70)
        
        # Benchmark 1: Small matrix multiplication
        self.run_benchmark(
            'matrix_multiply',
            {'size': 500, 'iterations': 20},
            'Small Matrix Multiplication (500x500)'
        )
        time.sleep(2)
        
        # Benchmark 2: Large matrix multiplication
        self.run_benchmark(
            'matrix_multiply',
            {'size': 2000, 'iterations': 10},
            'Large Matrix Multiplication (2000x2000)'
        )
        time.sleep(2)
        
        # Benchmark 3: Neural network training
        self.run_benchmark(
            'neural_network',
            {'epochs': 10, 'batch_size': 128},
            'Neural Network Training (10 epochs)'
        )
        time.sleep(2)
        
        # Benchmark 4: Vector operations
        self.run_benchmark(
            'vector_add',
            {'size': 50000000, 'iterations': 50},
            'Large Vector Addition (50M elements)'
        )
        time.sleep(2)
        
        # Benchmark 5: Image processing
        self.run_benchmark(
            'image_processing',
            {'batch_size': 64, 'image_size': 224, 'iterations': 100},
            'Image Processing (64 images, 224x224)'
        )
        
        # Save benchmark configuration
        output_file = 'results/benchmark_config.json'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n{'='*70}")
        print(f"✅ All benchmarks submitted!")
        print(f"   Configuration saved to: {output_file}")
        print(f"   Total benchmarks: {len(self.results['benchmarks'])}")
        print(f"\n💡 Use results_monitor.py to track results")
        print(f"   Then use analyze_results.py to generate comparison")
        print(f"{'='*70}\n")


def main():
    """Run benchmark suite"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run GPU vs CPU benchmarks')
    parser.add_argument('--quick', action='store_true',
                       help='Run quick benchmarks with smaller sizes')
    
    args = parser.parse_args()
    
    suite = BenchmarkSuite()
    
    if args.quick:
        print("\n⚡ Running quick benchmarks...")
        suite.run_benchmark(
            'matrix_multiply',
            {'size': 500, 'iterations': 5},
            'Quick Matrix Test'
        )
        time.sleep(2)
        suite.run_benchmark(
            'vector_add',
            {'size': 10000000, 'iterations': 10},
            'Quick Vector Test'
        )
    else:
        suite.run_all_benchmarks()


if __name__ == "__main__":
    main()
