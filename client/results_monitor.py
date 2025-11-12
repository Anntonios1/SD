"""
Results Monitor - Listen for job results and collect metrics
"""
import sys
import os
import json
from datetime import datetime
from collections import defaultdict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from broker.broker_client import RabbitMQClient, BrokerConfig


class ResultsMonitor:
    """Monitor and collect job results"""
    
    def __init__(self, output_file: str = None):
        self.broker = RabbitMQClient()
        self.config = BrokerConfig()
        self.results = []
        self.stats = defaultdict(lambda: {'count': 0, 'total_time': 0, 'min_time': float('inf'), 'max_time': 0})
        self.output_file = output_file or 'results/job_results.json'
        
        print("📊 Results Monitor initialized")
        
    def process_result(self, result_data: dict):
        """Process a job result"""
        job_id = result_data.get('job_id', 'unknown')
        status = result_data.get('status', 'unknown')
        worker_type = result_data.get('worker_type', 'unknown')
        processing_time = result_data.get('processing_time', 0)
        
        print(f"\n{'='*60}")
        print(f"📬 Result received: {job_id}")
        print(f"   Status: {status}")
        print(f"   Worker: {worker_type} ({result_data.get('worker_id', 'unknown')})")
        print(f"   Processing time: {processing_time:.4f}s")
        
        if status == 'completed':
            job_type = result_data.get('job_type', 'unknown')
            print(f"   Job type: {job_type}")
            
            # Update stats
            key = f"{job_type}_{worker_type}"
            self.stats[key]['count'] += 1
            self.stats[key]['total_time'] += processing_time
            self.stats[key]['min_time'] = min(self.stats[key]['min_time'], processing_time)
            self.stats[key]['max_time'] = max(self.stats[key]['max_time'], processing_time)
        else:
            print(f"   Error: {result_data.get('error', 'Unknown error')}")
        
        print(f"{'='*60}")
        
        # Store result
        self.results.append(result_data)
        
        # Save to file
        self.save_results()
        
        # Print stats
        self.print_stats()
        
    def save_results(self):
        """Save results to file"""
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        with open(self.output_file, 'w') as f:
            json.dump({
                'results': self.results,
                'stats': dict(self.stats),
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
    
    def print_stats(self):
        """Print current statistics"""
        if not self.stats:
            return
            
        print(f"\n📈 Current Statistics:")
        print(f"   Total results: {len(self.results)}")
        
        for key, data in self.stats.items():
            if data['count'] > 0:
                avg_time = data['total_time'] / data['count']
                print(f"\n   {key}:")
                print(f"      Jobs: {data['count']}")
                print(f"      Avg time: {avg_time:.4f}s")
                print(f"      Min time: {data['min_time']:.4f}s")
                print(f"      Max time: {data['max_time']:.4f}s")
        
        print()
        
    def start(self):
        """Start monitoring results"""
        print("\n🎯 Results Monitor is ready!")
        print("⏳ Waiting for results...\n")
        
        try:
            self.broker.connect()
            self.broker.consume(self.config.result_queue, self.process_result)
        except KeyboardInterrupt:
            print(f"\n👋 Monitor shutting down...")
            print(f"   Results collected: {len(self.results)}")
            print(f"   Saved to: {self.output_file}")
        except Exception as e:
            import traceback
            print(f"❌ Error: {e}")
            print(f"🔍 Traceback: {traceback.format_exc()}")
        finally:
            self.broker.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor job results')
    parser.add_argument('--output', type=str, default='results/job_results.json',
                       help='Output file for results')
    
    args = parser.parse_args()
    
    monitor = ResultsMonitor(args.output)
    monitor.start()
