"""
Clean failed jobs from results
"""
import json
from datetime import datetime

# Load results
with open('results/job_results.json', 'r') as f:
    data = json.load(f)

# Keep only successful jobs
original_count = len(data['results'])
data['results'] = [r for r in data['results'] if r.get('status') != 'failed']
cleaned_count = original_count - len(data['results'])

# Recalculate stats
from collections import defaultdict
stats = defaultdict(lambda: {'count': 0, 'total_time': 0, 'min_time': float('inf'), 'max_time': 0})

for result in data['results']:
    if result.get('status') == 'completed':
        job_type = result.get('job_type', 'unknown')
        worker_type = result.get('worker_type', 'unknown')
        processing_time = result.get('processing_time', 0)
        
        key = f"{job_type}_{worker_type}"
        stats[key]['count'] += 1
        stats[key]['total_time'] += processing_time
        stats[key]['min_time'] = min(stats[key]['min_time'], processing_time)
        stats[key]['max_time'] = max(stats[key]['max_time'], processing_time)

data['stats'] = dict(stats)
data['timestamp'] = datetime.now().isoformat()

# Save cleaned results
with open('results/job_results.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n{'='*70}")
print(f"✅ Resultados Limpiados")
print(f"{'='*70}")
print(f"\n📊 Trabajos eliminados: {cleaned_count}")
print(f"📊 Trabajos restantes: {len(data['results'])}")
print(f"\n✓ Archivo actualizado: results/job_results.json\n")
