# Arquitectura del Sistema - Sistema Distribuido GPU

## 🎯 Visión General

Este sistema implementa una arquitectura distribuida para procesamiento de jobs que requieren GPU, con capacidad de escalamiento horizontal y balanceo de carga.

## 📐 Diagrama de Arquitectura

```
┌─────────────┐
│   Cliente   │ (Envía jobs)
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│   RabbitMQ Broker   │ (Cola de mensajes)
│   ┌─────────────┐   │
│   │ job_queue   │   │
│   │ gpu_queue   │   │
│   │ cpu_queue   │   │
│   │result_queue │   │
│   └─────────────┘   │
└──────┬──────────────┘
       │
       ▼
┌─────────────┐
│  Scheduler  │ (Distribuye jobs)
└──────┬──────┘
       │
       ├─────────────────┬──────────────┐
       ▼                 ▼              ▼
┌─────────────┐   ┌─────────────┐ ┌─────────────┐
│ GPU Worker  │   │ GPU Worker  │ │ CPU Worker  │
│   (Node 1)  │   │   (Node 2)  │ │   (Node 3)  │
└──────┬──────┘   └──────┬──────┘ └──────┬──────┘
       │                 │              │
       └────────┬────────┴──────────────┘
                ▼
         ┌─────────────┐
         │  Resultados │
         │   Monitor   │
         └─────────────┘
```

## 🧩 Componentes

### 1. Cliente (Client)
**Responsabilidad:** Enviar jobs al sistema

**Archivos:**
- `client/submit_job.py`: CLI para enviar jobs
- `client/results_monitor.py`: Monitor de resultados

**Funciones:**
- Crear jobs con parámetros específicos
- Especificar preferencia GPU/CPU
- Enviar jobs a la cola principal

### 2. Broker (RabbitMQ)
**Responsabilidad:** Gestión de colas de mensajes

**Colas:**
- `job_queue`: Cola principal de entrada
- `gpu_queue`: Cola para workers GPU
- `cpu_queue`: Cola para workers CPU
- `result_queue`: Cola de resultados

**Características:**
- Mensajes persistentes
- Acknowledgments
- Reintento automático en fallos

### 3. Scheduler
**Responsabilidad:** Distribuir jobs a workers apropiados

**Archivos:**
- `scheduler/scheduler.py`

**Estrategia:**
1. Recibe job de `job_queue`
2. Evalúa preferencia GPU/CPU
3. Enruta a cola apropiada
4. Registra asignación

**Mejoras futuras:**
- Balanceo de carga dinámico
- Priorización de jobs
- Estimación de tiempo de ejecución

### 4. Workers

#### GPU Worker
**Responsabilidad:** Ejecutar jobs con aceleración GPU

**Archivos:**
- `workers/gpu_worker.py`
- `workers/jobs/job_executor.py`

**Características:**
- Detecta GPU automáticamente
- Usa PyTorch con CUDA
- Sincronización CUDA para timing preciso
- Manejo de errores robusto

**Jobs Soportados:**
- Matrix Multiplication
- Neural Network Training
- Vector Addition
- Image Processing

#### CPU Worker
**Responsabilidad:** Ejecutar jobs en CPU (comparación)

**Archivos:**
- `workers/cpu_worker.py`
- `workers/jobs/job_executor.py`

**Características:**
- Mismo código que GPU worker
- Usa CPU para ejecución
- Permite comparación de performance

### 5. Job Executor
**Responsabilidad:** Implementación de tipos de jobs

**Archivos:**
- `workers/jobs/job_executor.py`

**Job Types:**

#### Matrix Multiplication
```python
{
    'job_type': 'matrix_multiply',
    'size': 1000,
    'iterations': 10
}
```
- Multiplica matrices NxN
- Benchmark de FLOPS
- Ideal para GPU

#### Neural Network Training
```python
{
    'job_type': 'neural_network',
    'epochs': 5,
    'batch_size': 64,
    'input_size': 784,
    'hidden_size': 256,
    'output_size': 10
}
```
- Red neuronal simple (2 capas)
- Forward + backward pass
- Optimización con Adam

#### Vector Addition
```python
{
    'job_type': 'vector_addition',
    'size': 10000000,
    'iterations': 100
}
```
- Operación elemento a elemento
- Benchmark de bandwidth de memoria
- Overhead de transferencia GPU

#### Image Processing
```python
{
    'job_type': 'image_processing',
    'batch_size': 32,
    'image_size': 224,
    'iterations': 50
}
```
- Convoluciones 2D
- Similar a CNNs
- Operaciones intensivas en GPU

## 🔄 Flujo de Datos

### 1. Envío de Job
```
Cliente → job_queue → Scheduler
```

1. Cliente crea job con parámetros
2. Job se serializa a JSON
3. Se publica en `job_queue`
4. Mensaje se marca como persistente

### 2. Scheduling
```
Scheduler → gpu_queue/cpu_queue
```

1. Scheduler consume de `job_queue`
2. Evalúa `prefer_gpu` flag
3. Enruta a cola apropiada
4. Confirma recepción (ACK)

### 3. Ejecución
```
Worker → Procesamiento → result_queue
```

1. Worker consume de su cola
2. Ejecuta job con JobExecutor
3. Mide tiempos de ejecución
4. Publica resultado con metadata
5. Confirma procesamiento (ACK)

### 4. Resultados
```
result_queue → Monitor → Archivo
```

1. Monitor consume resultados
2. Calcula estadísticas
3. Guarda a archivo JSON
4. Actualiza métricas en tiempo real

## 🐳 Arquitectura Docker

### Redes
- `gpu-cluster`: Red bridge para comunicación entre contenedores

### Volúmenes
- `rabbitmq_data`: Persistencia de RabbitMQ
- `./results`: Resultados compartidos con host

### Servicios

```yaml
rabbitmq:
  - Puerto 5672: AMQP
  - Puerto 15672: Management UI
  
scheduler:
  - Depende de: rabbitmq
  
gpu-worker:
  - Depende de: rabbitmq, scheduler
  - Requiere: nvidia runtime
  - GPU: 1
  
cpu-worker:
  - Depende de: rabbitmq, scheduler
  - CPU: 2 cores
  - RAM: 4GB
  
metrics:
  - Puerto 8000: API
  - Volumen: ./results
```

## ☸️ Arquitectura Kubernetes

### Namespace
- `gpu-cluster`: Aislamiento de recursos

### Deployments

#### RabbitMQ
- Replicas: 1
- Storage: EmptyDir (demo) o PVC (producción)
- Service: ClusterIP

#### Scheduler
- Replicas: 1
- Depends: RabbitMQ ready

#### GPU Workers
- Replicas: 1+ (según GPUs disponibles)
- Node Selector: `accelerator=nvidia-gpu`
- Tolerations: `nvidia.com/gpu:NoSchedule`
- Resources: `nvidia.com/gpu: 1`

#### CPU Workers
- Replicas: 2+
- Resources: 2 CPU, 4GB RAM

#### Metrics Monitor
- Replicas: 1
- PVC: 1GB para resultados
- Service: LoadBalancer (puerto 8000)

### Recursos

```yaml
GPU Worker:
  resources:
    limits:
      nvidia.com/gpu: 1
    requests:
      nvidia.com/gpu: 1

CPU Worker:
  resources:
    limits:
      cpu: "2"
      memory: "4Gi"
    requests:
      cpu: "1"
      memory: "2Gi"
```

## 🔐 Configuración

### Variables de Entorno

```bash
# RabbitMQ
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=admin
RABBITMQ_PASS=admin123

# Worker
WORKER_TYPE=gpu|cpu
WORKER_ID=worker-xxx
```

### Colas RabbitMQ

```python
# Configuración
durable=True           # Persistencia de cola
delivery_mode=2        # Mensajes persistentes
prefetch_count=1       # Un job por worker
acknowledgment=True    # Confirmación manual
```

## 📊 Métricas y Monitoreo

### Métricas por Job
- `job_id`: Identificador único
- `job_type`: Tipo de trabajo
- `worker_id`: Worker que procesó
- `worker_type`: GPU o CPU
- `processing_time`: Tiempo total
- `device`: Dispositivo usado
- `status`: completed/failed

### Métricas Agregadas
- Count por job_type y worker_type
- Avg, min, max processing time
- Speedup GPU vs CPU
- Throughput (jobs/segundo)

### Visualización
- Gráficas comparativas
- Tablas de resultados
- Reporte en Markdown
- Exportación CSV

## 🚀 Escalabilidad

### Horizontal
- Múltiples GPU workers (1 GPU cada uno)
- Múltiples CPU workers
- RabbitMQ cluster (producción)

### Vertical
- Workers con múltiples GPUs
- Batch processing de jobs
- Paralelización interna

### Limitaciones
- RabbitMQ single instance (demo)
- Sin load balancing avanzado
- Sin failover automático

## 🔧 Extensibilidad

### Agregar Nuevo Job Type

1. Añadir método en `JobExecutor`:
```python
def new_job_type(self, job_data):
    # Implementación
    return result
```

2. Registrar en `execute()`:
```python
elif job_type == 'new_job_type':
    return self.new_job_type(job_data)
```

3. Añadir helper en `JobClient`:
```python
def submit_new_job(self, params):
    return self.submit_job('new_job_type', params)
```

### Agregar Nueva Estrategia de Scheduling

1. Modificar `scheduler.py`:
```python
def advanced_schedule(self, job_data):
    # Evaluación de carga
    # Estimación de tiempo
    # Selección de worker óptimo
```

## 🎓 Casos de Uso

### 1. Machine Learning Training
- Dataset grande
- Múltiples épocas
- GPU acelera entrenamiento

### 2. Computación Científica
- Simulaciones numéricas
- Álgebra lineal
- Procesamiento paralelo

### 3. Procesamiento de Imágenes
- Batch de imágenes
- Filtros y transformaciones
- CNNs para análisis

### 4. Análisis de Datos
- Operaciones matriciales
- Agregaciones masivas
- GPU para big data

## 📚 Referencias

- [RabbitMQ Tutorials](https://www.rabbitmq.com/getstarted.html)
- [PyTorch CUDA Semantics](https://pytorch.org/docs/stable/notes/cuda.html)
- [Kubernetes GPU Support](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/)
- [Docker GPU Support](https://docs.docker.com/config/containers/resource_constraints/#gpu)
