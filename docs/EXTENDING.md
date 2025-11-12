# Cómo Extender el Sistema

## 🔧 Agregar Nuevo Tipo de Job

### Paso 1: Implementar el Job en JobExecutor

Editar `workers/jobs/job_executor.py`:

```python
def custom_computation(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ejemplo: Computación personalizada
    """
    # Obtener parámetros
    data_size = job_data.get('data_size', 1000)
    complexity = job_data.get('complexity', 10)
    
    print(f"Running custom computation: size={data_size}, complexity={complexity}")
    
    # Crear datos de entrada
    data = torch.randn(data_size, data_size, device=self.device)
    
    start_time = time.time()
    
    # Tu computación aquí
    for _ in range(complexity):
        result = torch.matmul(data, data.T)
        result = torch.sigmoid(result)
        if self.use_gpu:
            torch.cuda.synchronize()
    
    elapsed = time.time() - start_time
    
    # Retornar resultado
    return {
        'job_type': 'custom_computation',
        'data_size': data_size,
        'complexity': complexity,
        'processing_time': elapsed,
        'device': str(self.device),
        'result_mean': result.mean().item()
    }
```

### Paso 2: Registrar en el Método `execute()`

Agregar en `execute()` dentro de `job_executor.py`:

```python
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
    elif job_type == 'custom_computation':  # NUEVO
        return self.custom_computation(job_data)
    else:
        raise ValueError(f"Unknown job type: {job_type}")
```

### Paso 3: Agregar Helper en el Cliente

Editar `client/submit_job.py`, agregar método en la clase `JobClient`:

```python
def submit_custom_computation(self, data_size: int = 1000, 
                              complexity: int = 10, 
                              prefer_gpu: bool = True):
    """Submit a custom computation job"""
    return self.submit_job('custom_computation', {
        'data_size': data_size,
        'complexity': complexity
    }, prefer_gpu)
```

### Paso 4: Agregar Opción en CLI

En la función `main()` de `client/submit_job.py`:

```python
parser.add_argument('--job-type', type=str, required=True,
                   choices=['matrix-multiply', 'neural-network', 
                           'vector-add', 'image-processing',
                           'custom-computation'],  # NUEVO
                   help='Type of job to submit')

# En el código de ejecución:
if args.job_type == 'custom-computation':
    job_id = client.submit_custom_computation(
        args.data_size, 
        args.complexity, 
        prefer_gpu
    )
```

### Paso 5: Usar el Nuevo Job

```powershell
# Enviar job GPU
python client/submit_job.py --job-type custom-computation --data-size 1000 --complexity 10

# Enviar job CPU para comparar
python client/submit_job.py --job-type custom-computation --data-size 1000 --complexity 10 --cpu
```

## 🎯 Ejemplos de Jobs Adicionales

### 1. FFT (Fast Fourier Transform)

```python
def fft_computation(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
    """FFT computation"""
    size = job_data.get('size', 1000000)
    
    signal = torch.randn(size, device=self.device)
    
    start_time = time.time()
    
    # FFT
    spectrum = torch.fft.fft(signal)
    if self.use_gpu:
        torch.cuda.synchronize()
    
    elapsed = time.time() - start_time
    
    return {
        'job_type': 'fft_computation',
        'size': size,
        'processing_time': elapsed,
        'device': str(self.device)
    }
```

### 2. Eigenvalue Decomposition

```python
def eigenvalue_computation(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
    """Eigenvalue decomposition"""
    size = job_data.get('size', 500)
    
    # Crear matriz simétrica
    A = torch.randn(size, size, device=self.device)
    A = A + A.T  # Hacer simétrica
    
    start_time = time.time()
    
    eigenvalues = torch.linalg.eigvalsh(A)
    if self.use_gpu:
        torch.cuda.synchronize()
    
    elapsed = time.time() - start_time
    
    return {
        'job_type': 'eigenvalue_computation',
        'size': size,
        'processing_time': elapsed,
        'device': str(self.device),
        'max_eigenvalue': eigenvalues.max().item()
    }
```

### 3. Monte Carlo Simulation

```python
def monte_carlo_simulation(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
    """Monte Carlo simulation for Pi estimation"""
    samples = job_data.get('samples', 10000000)
    
    start_time = time.time()
    
    # Generar puntos aleatorios
    x = torch.rand(samples, device=self.device)
    y = torch.rand(samples, device=self.device)
    
    # Calcular distancia al origen
    distances = x**2 + y**2
    inside_circle = (distances <= 1.0).sum().item()
    
    pi_estimate = 4.0 * inside_circle / samples
    
    if self.use_gpu:
        torch.cuda.synchronize()
    
    elapsed = time.time() - start_time
    
    return {
        'job_type': 'monte_carlo_simulation',
        'samples': samples,
        'processing_time': elapsed,
        'device': str(self.device),
        'pi_estimate': pi_estimate
    }
```

### 4. K-Means Clustering

```python
def kmeans_clustering(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
    """K-Means clustering"""
    n_samples = job_data.get('n_samples', 10000)
    n_features = job_data.get('n_features', 128)
    n_clusters = job_data.get('n_clusters', 10)
    iterations = job_data.get('iterations', 100)
    
    # Generar datos
    data = torch.randn(n_samples, n_features, device=self.device)
    
    # Inicializar centroides aleatoriamente
    centroids = data[torch.randperm(n_samples)[:n_clusters]]
    
    start_time = time.time()
    
    for _ in range(iterations):
        # Asignar puntos a centroides
        distances = torch.cdist(data, centroids)
        assignments = distances.argmin(dim=1)
        
        # Actualizar centroides
        for k in range(n_clusters):
            mask = assignments == k
            if mask.sum() > 0:
                centroids[k] = data[mask].mean(dim=0)
        
        if self.use_gpu:
            torch.cuda.synchronize()
    
    elapsed = time.time() - start_time
    
    return {
        'job_type': 'kmeans_clustering',
        'n_samples': n_samples,
        'n_features': n_features,
        'n_clusters': n_clusters,
        'iterations': iterations,
        'processing_time': elapsed,
        'device': str(self.device)
    }
```

## 🔄 Modificar Estrategia de Scheduling

### Scheduler con Prioridades

Editar `scheduler/scheduler.py`:

```python
class JobScheduler:
    def schedule_job(self, job_data: dict):
        """Schedule with priority"""
        job_id = job_data.get('job_id', 'unknown')
        prefer_gpu = job_data.get('prefer_gpu', True)
        priority = job_data.get('priority', 'normal')  # high, normal, low
        
        # Determinar cola basado en prioridad
        if priority == 'high':
            # Jobs de alta prioridad siempre a GPU
            target_queue = self.config.gpu_queue
        elif prefer_gpu:
            target_queue = self.config.gpu_queue
        else:
            target_queue = self.config.cpu_queue
        
        print(f"📋 Scheduling job {job_id} (priority: {priority})")
        self.broker.publish_job(job_data, target_queue)
```

### Scheduler con Load Balancing

```python
class LoadBalancingScheduler:
    def __init__(self):
        self.broker = RabbitMQClient()
        self.gpu_load = 0
        self.cpu_load = 0
    
    def schedule_job(self, job_data: dict):
        """Schedule based on current load"""
        job_id = job_data.get('job_id')
        
        # Decidir basado en carga
        if self.gpu_load < self.cpu_load * 2:  # GPU es ~2x más rápido
            target_queue = self.config.gpu_queue
            self.gpu_load += 1
        else:
            target_queue = self.config.cpu_queue
            self.cpu_load += 1
        
        self.broker.publish_job(job_data, target_queue)
```

## 📊 Agregar Nuevas Métricas

### GPU Utilization Monitor

Crear `monitoring/gpu_monitor.py`:

```python
import subprocess
import time
import json

def monitor_gpu_utilization(duration=60, interval=1):
    """Monitor GPU utilization"""
    results = []
    
    for _ in range(duration):
        try:
            output = subprocess.check_output([
                'nvidia-smi',
                '--query-gpu=utilization.gpu,utilization.memory,temperature.gpu',
                '--format=csv,noheader,nounits'
            ]).decode()
            
            gpu_util, mem_util, temp = map(float, output.strip().split(','))
            
            results.append({
                'timestamp': time.time(),
                'gpu_utilization': gpu_util,
                'memory_utilization': mem_util,
                'temperature': temp
            })
            
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(interval)
    
    # Guardar resultados
    with open('results/gpu_utilization.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return results
```

### Queue Length Monitor

```python
def monitor_queue_lengths(rabbitmq_url, duration=60, interval=5):
    """Monitor RabbitMQ queue lengths"""
    import requests
    
    results = []
    
    for _ in range(duration // interval):
        try:
            response = requests.get(
                f"{rabbitmq_url}/api/queues",
                auth=('admin', 'admin123')
            )
            
            queues = response.json()
            
            snapshot = {
                'timestamp': time.time(),
                'queues': {}
            }
            
            for queue in queues:
                snapshot['queues'][queue['name']] = {
                    'messages': queue.get('messages', 0),
                    'consumers': queue.get('consumers', 0)
                }
            
            results.append(snapshot)
            
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(interval)
    
    return results
```

## 🎨 Personalizar Visualizaciones

### Gráfico de Utilización GPU

```python
import matplotlib.pyplot as plt
import json

def plot_gpu_utilization(data_file='results/gpu_utilization.json'):
    """Plot GPU utilization over time"""
    with open(data_file) as f:
        data = json.load(f)
    
    timestamps = [d['timestamp'] for d in data]
    gpu_util = [d['gpu_utilization'] for d in data]
    mem_util = [d['memory_utilization'] for d in data]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    ax1.plot(timestamps, gpu_util, label='GPU Utilization')
    ax1.set_ylabel('Utilization (%)')
    ax1.set_title('GPU Utilization Over Time')
    ax1.legend()
    ax1.grid(True)
    
    ax2.plot(timestamps, mem_util, label='Memory Utilization', color='orange')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Utilization (%)')
    ax2.set_title('GPU Memory Utilization Over Time')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('results/gpu_utilization.png')
```

## 🚀 Mejoras Futuras Sugeridas

### 1. Auto-Scaling
- Implementar scaling automático de workers
- Basado en longitud de cola
- Integración con Kubernetes HPA

### 2. Fault Tolerance
- Retry automático de jobs fallidos
- Dead letter queues
- Health checks de workers

### 3. Multi-GPU Support
- Workers con múltiples GPUs
- Data parallelism
- Model parallelism

### 4. Advanced Scheduling
- Machine learning para predecir tiempos
- Cost-based scheduling
- SLA-aware scheduling

### 5. Web Dashboard
- Dashboard en tiempo real
- Visualización de colas
- Control de jobs

### 6. Profiling
- Integración con NVIDIA Nsight
- Profiling automático
- Optimización sugerida

## 📚 Referencias para Extensiones

- **PyTorch CUDA**: https://pytorch.org/docs/stable/cuda.html
- **RabbitMQ Advanced**: https://www.rabbitmq.com/tutorials/tutorial-six-python.html
- **Kubernetes HPA**: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
- **NVIDIA Profiling**: https://developer.nvidia.com/nsight-systems
