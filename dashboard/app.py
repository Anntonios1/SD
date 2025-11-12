"""
Dashboard Web - Visual interface for metrics and benchmarks
"""
import sys
import os
import json
from datetime import datetime
from flask import Flask, render_template, jsonify
from flask_cors import CORS

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)

RESULTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results', 'job_results.json')
BENCHMARK_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'results', 'benchmark_config.json')


def load_results():
    """Load job results from file"""
    try:
        if os.path.exists(RESULTS_FILE):
            with open(RESULTS_FILE, 'r') as f:
                data = json.load(f)
                return data.get('results', []), data.get('stats', {})
        return [], {}
    except Exception as e:
        print(f"Error loading results: {e}")
        return [], {}


def load_benchmarks():
    """Load benchmark configuration"""
    try:
        if os.path.exists(BENCHMARK_FILE):
            with open(BENCHMARK_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading benchmarks: {e}")
        return {}


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/api/stats')
def get_stats():
    """Get current statistics"""
    results, stats = load_results()
    
    # Calculate summary
    total_jobs = len(results)
    successful_jobs = sum(1 for r in results if r.get('status') == 'completed')
    failed_jobs = sum(1 for r in results if r.get('status') == 'failed')
    
    # Get job types distribution
    job_types = {}
    for result in results:
        job_type = result.get('job_type', 'unknown')
        if job_type not in job_types:
            job_types[job_type] = {'gpu': 0, 'cpu': 0}
        worker_type = result.get('worker_type', 'unknown')
        if worker_type in ['gpu', 'cpu']:
            job_types[job_type][worker_type] += 1
    
    return jsonify({
        'total_jobs': total_jobs,
        'successful_jobs': successful_jobs,
        'failed_jobs': failed_jobs,
        'stats': stats,
        'job_types': job_types,
        'last_updated': datetime.now().isoformat()
    })


@app.route('/api/results')
def get_results():
    """Get all job results"""
    results, _ = load_results()
    return jsonify(results)


@app.route('/api/benchmarks')
def get_benchmarks():
    """Get benchmark configuration and results"""
    benchmarks = load_benchmarks()
    results, stats = load_results()
    
    # Match benchmark jobs with results
    benchmark_results = []
    for benchmark in benchmarks.get('benchmarks', []):
        gpu_job_id = benchmark.get('gpu_job_id')
        cpu_job_id = benchmark.get('cpu_job_id')
        
        gpu_result = next((r for r in results if r.get('job_id') == gpu_job_id), None)
        cpu_result = next((r for r in results if r.get('job_id') == cpu_job_id), None)
        
        if gpu_result and cpu_result:
            gpu_time = gpu_result.get('processing_time', 0)
            cpu_time = cpu_result.get('processing_time', 0)
            speedup = cpu_time / gpu_time if gpu_time > 0 else 0
            
            benchmark_results.append({
                'name': benchmark.get('name'),
                'job_type': benchmark.get('job_type'),
                'gpu_time': gpu_time,
                'cpu_time': cpu_time,
                'speedup': speedup,
                'gpu_job_id': gpu_job_id,
                'cpu_job_id': cpu_job_id
            })
    
    return jsonify({
        'benchmarks': benchmark_results,
        'timestamp': benchmarks.get('timestamp')
    })


@app.route('/api/performance')
def get_performance():
    """Get performance comparison data"""
    _, stats = load_results()
    
    performance_data = []
    
    # Group by job type
    job_types = {}
    for key, data in stats.items():
        parts = key.rsplit('_', 1)
        if len(parts) == 2:
            job_type, worker_type = parts
            if job_type not in job_types:
                job_types[job_type] = {}
            job_types[job_type][worker_type] = {
                'avg_time': data['total_time'] / data['count'],
                'count': data['count'],
                'min_time': data['min_time'],
                'max_time': data['max_time']
            }
    
    # Calculate speedups
    for job_type, workers in job_types.items():
        if 'gpu' in workers and 'cpu' in workers:
            speedup = workers['cpu']['avg_time'] / workers['gpu']['avg_time']
            performance_data.append({
                'job_type': job_type,
                'gpu_avg': workers['gpu']['avg_time'],
                'cpu_avg': workers['cpu']['avg_time'],
                'speedup': speedup,
                'gpu_count': workers['gpu']['count'],
                'cpu_count': workers['cpu']['count']
            })
    
    return jsonify(performance_data)


@app.route('/api/failed')
def get_failed_jobs():
    """Get failed jobs details"""
    results, _ = load_results()
    failed = [r for r in results if r.get('status') == 'failed']
    return jsonify(failed)


@app.route('/api/submit_job', methods=['POST'])
def submit_job():
    """Submit a new job"""
    try:
        from flask import request
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from client.submit_job import JobClient
        
        data = request.get_json()
        job_type = data.get('job_type')
        params = data.get('params', {})
        prefer_gpu = data.get('prefer_gpu', True)
        
        client = JobClient()
        job_id = client.submit_job(job_type, params, prefer_gpu)
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'message': f'Job {job_id} submitted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/run_benchmark', methods=['POST'])
def run_benchmark():
    """Run a benchmark test"""
    try:
        from flask import request
        import subprocess
        import threading
        
        data = request.get_json()
        benchmark_type = data.get('type', 'quick')
        
        # Run benchmark in background
        def run_async():
            if benchmark_type == 'quick':
                subprocess.run(['python', 'benchmarks/run_benchmarks.py', '--quick'], 
                             cwd=os.path.dirname(os.path.dirname(__file__)))
            else:
                subprocess.run(['python', 'benchmarks/run_benchmarks.py'], 
                             cwd=os.path.dirname(os.path.dirname(__file__)))
        
        thread = threading.Thread(target=run_async)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': f'Benchmark {benchmark_type} started in background'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/clear_results', methods=['POST'])
def clear_results():
    """Clear failed jobs from results"""
    try:
        import subprocess
        result = subprocess.run(['python', 'clean_results.py'], 
                              cwd=os.path.dirname(os.path.dirname(__file__)),
                              capture_output=True, text=True)
        
        return jsonify({
            'success': True,
            'message': 'Failed jobs cleared successfully',
            'output': result.stdout
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🎨 Dashboard Web Server")
    print("="*70)
    print("\n🌐 Dashboard disponible en: http://localhost:5000")
    print("📊 Actualizando datos en tiempo real...\n")
    print("Presiona Ctrl+C para detener\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
