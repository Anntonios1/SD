"""
CPU Worker - Executes jobs on CPU (for comparison)
"""
import sys
import os
import time
import uuid
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from broker.broker_client import RabbitMQClient, BrokerConfig
from workers.jobs.job_executor import JobExecutor


class CPUWorker:
    """Worker that processes jobs using CPU"""
    
    def __init__(self, worker_id: str = None):
        self.worker_id = worker_id or os.getenv('WORKER_ID', f'cpu-worker-{uuid.uuid4().hex[:8]}')
        self.broker = RabbitMQClient()
        self.executor = JobExecutor(use_gpu=False)
        self.jobs_processed = 0
        
        print(f"🚀 CPU Worker initialized: {self.worker_id}")
        print(f"   Device: {self.executor.device}")
        
    def process_job(self, job_data: dict):
        """Process a single job"""
        job_id = job_data.get('job_id', 'unknown')
        print(f"\n{'='*60}")
        print(f"📥 Processing job {job_id}")
        print(f"   Type: {job_data.get('job_type')}")
        print(f"   Worker: {self.worker_id}")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        try:
            # Execute the job
            result = self.executor.execute(job_data)
            
            # Add metadata
            result.update({
                'job_id': job_id,
                'worker_id': self.worker_id,
                'worker_type': 'cpu',
                'status': 'completed',
                'start_time': job_data.get('submit_time'),
                'end_time': datetime.now().isoformat(),
                'processing_time': time.time() - start_time
            })
            
            # Send result back
            self.broker.publish_result(result)
            
            self.jobs_processed += 1
            print(f"✅ Job {job_id} completed successfully")
            print(f"   Processing time: {result['processing_time']:.4f}s")
            print(f"   Total jobs processed: {self.jobs_processed}")
            
        except Exception as e:
            print(f"❌ Job {job_id} failed: {str(e)}")
            
            # Send error result
            error_result = {
                'job_id': job_id,
                'worker_id': self.worker_id,
                'worker_type': 'cpu',
                'status': 'failed',
                'error': str(e),
                'processing_time': time.time() - start_time
            }
            self.broker.publish_result(error_result)
    
    def start(self):
        """Start consuming jobs from the queue"""
        print(f"\n🎯 CPU Worker {self.worker_id} is ready!")
        print(f"⏳ Waiting for jobs...\n")
        
        try:
            self.broker.connect()
            config = BrokerConfig()
            self.broker.consume(config.cpu_queue, self.process_job)
        except KeyboardInterrupt:
            print(f"\n👋 CPU Worker {self.worker_id} shutting down...")
            print(f"   Jobs processed: {self.jobs_processed}")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            self.broker.close()


if __name__ == "__main__":
    worker = CPUWorker()
    worker.start()
