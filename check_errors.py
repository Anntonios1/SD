"""
Check failed jobs
"""
import json

with open('results/job_results.json', 'r') as f:
    data = json.load(f)

failed = [r for r in data['results'] if r.get('status') == 'failed']

print(f"\n{'='*70}")
print(f"❌ Trabajos Fallidos: {len(failed)}")
print(f"{'='*70}\n")

for r in failed:
    print(f"Job ID: {r.get('job_id')}")
    print(f"Job Type: {r.get('job_type', 'N/A')}")
    print(f"Worker: {r.get('worker_id', 'N/A')}")
    print(f"Error: {r.get('error')}")
    print(f"{'-'*70}\n")
