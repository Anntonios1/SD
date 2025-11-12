"""
Scheduler - Distributes jobs to GPU or CPU workers
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from broker.broker_client import RabbitMQClient, BrokerConfig


class JobScheduler:
    """Simple scheduler that routes jobs to GPU or CPU workers"""
    
    def __init__(self):
        self.broker = RabbitMQClient()
        self.config = BrokerConfig()
        self.jobs_scheduled = 0
        
        print("🎛️  Job Scheduler initialized")
        
    def schedule_job(self, job_data: dict):
        """Schedule a job to the appropriate worker queue"""
        job_id = job_data.get('job_id', 'unknown')
        prefer_gpu = job_data.get('prefer_gpu', True)
        
        # Simple scheduling: prefer GPU if requested
        target_queue = self.config.gpu_queue if prefer_gpu else self.config.cpu_queue
        
        print(f"\n📋 Scheduling job {job_id}")
        print(f"   Type: {job_data.get('job_type')}")
        print(f"   Target: {'GPU' if prefer_gpu else 'CPU'} queue")
        
        # Forward to appropriate worker queue
        self.broker.publish_job(job_data, target_queue)
        
        self.jobs_scheduled += 1
        print(f"✓ Job scheduled (total: {self.jobs_scheduled})")
        
    def start(self):
        """Start consuming jobs from the main queue"""
        print("\n🎯 Scheduler is ready!")
        print("⏳ Waiting for jobs to schedule...\n")
        
        try:
            self.broker.connect()
            self.broker.consume(self.config.job_queue, self.schedule_job)
        except KeyboardInterrupt:
            print(f"\n👋 Scheduler shutting down...")
            print(f"   Jobs scheduled: {self.jobs_scheduled}")
        except Exception as e:
            import traceback
            print(f"❌ Error: {e}")
            print(f"🔍 Traceback: {traceback.format_exc()}")
        finally:
            self.broker.close()


if __name__ == "__main__":
    scheduler = JobScheduler()
    scheduler.start()
