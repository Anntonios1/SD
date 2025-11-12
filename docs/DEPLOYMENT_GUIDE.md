# Guía de Despliegue - Sistema Distribuido GPU

## 📋 Tabla de Contenidos
1. [Requisitos](#requisitos)
2. [Instalación Local](#instalación-local)
3. [Despliegue con Docker](#despliegue-con-docker)
4. [Despliegue con Kubernetes](#despliegue-con-kubernetes)
5. [Ejecutar Demo](#ejecutar-demo)
6. [Troubleshooting](#troubleshooting)

## 🔧 Requisitos

### Requisitos Mínimos
- Python 3.9+
- Docker 20.10+
- Docker Compose 2.0+
- 8GB RAM
- 10GB espacio en disco

### Para GPU (Opcional)
- NVIDIA GPU (compute capability 3.5+)
- NVIDIA Driver 470+
- NVIDIA Container Toolkit

### Para Kubernetes
- Kubernetes 1.20+
- kubectl configurado
- NVIDIA Device Plugin (para nodos GPU)

## 🚀 Instalación Local

### 1. Instalar Dependencias Python

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Para GPU (PyTorch con CUDA)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 2. Iniciar RabbitMQ

```powershell
# Usando Docker
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 `
  -e RABBITMQ_DEFAULT_USER=admin `
  -e RABBITMQ_DEFAULT_PASS=admin123 `
  rabbitmq:3-management
```

### 3. Iniciar Componentes

```powershell
# Terminal 1: Scheduler
python scheduler/scheduler.py

# Terminal 2: GPU Worker
python workers/gpu_worker.py

# Terminal 3: CPU Worker
python workers/cpu_worker.py

# Terminal 4: Monitor de Resultados
python client/results_monitor.py
```

### 4. Enviar Jobs

```powershell
# Terminal 5: Cliente
python client/submit_job.py --job-type matrix-multiply --size 1000 --iterations 10
python client/submit_job.py --job-type neural-network --epochs 5
python client/submit_job.py --job-type vector-add --size 10000000
```

## 🐳 Despliegue con Docker

### Verificar GPU Support (Opcional)

```powershell
# Verificar NVIDIA runtime
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

### Construir Imágenes

```powershell
# Opción 1: Usar script
.\scripts\build_images.ps1

# Opción 2: Manual con docker-compose
docker-compose build
```

### Iniciar Cluster

```powershell
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Ver estado
docker-compose ps
```

### Verificar Servicios

```powershell
# RabbitMQ Management UI
# Abrir: http://localhost:15672
# Usuario: admin
# Password: admin123

# Ver logs de worker GPU
docker-compose logs -f gpu-worker

# Ver logs de scheduler
docker-compose logs -f scheduler
```

### Enviar Jobs al Cluster

```powershell
# Enviar job de prueba
python client/submit_job.py --job-type matrix-multiply --size 1000

# Monitorear resultados
python client/results_monitor.py
```

### Detener Cluster

```powershell
docker-compose down

# Con limpieza de volúmenes
docker-compose down -v
```

## ☸️ Despliegue con Kubernetes

### 1. Preparar Cluster Kubernetes

```powershell
# Verificar cluster
kubectl cluster-info

# Verificar nodos GPU (si aplica)
kubectl get nodes -o json | Select-String "nvidia"
```

### 2. Instalar NVIDIA Device Plugin (para GPU)

```powershell
kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.14.0/nvidia-device-plugin.yml
```

### 3. Etiquetar Nodos GPU

```powershell
# Etiquetar nodo con GPU
kubectl label nodes <node-name> accelerator=nvidia-gpu

# Agregar taint para reservar para GPU
kubectl taint nodes <node-name> nvidia.com/gpu=present:NoSchedule
```

### 4. Construir y Cargar Imágenes

```powershell
# Construir imágenes
.\scripts\build_images.ps1

# Para Minikube
minikube image load gpu-cluster/scheduler:latest
minikube image load gpu-cluster/gpu-worker:latest
minikube image load gpu-cluster/cpu-worker:latest
minikube image load gpu-cluster/metrics:latest

# Para registry remoto
docker tag gpu-cluster/scheduler:latest your-registry/scheduler:latest
docker push your-registry/scheduler:latest
# Repetir para todas las imágenes
```

### 5. Desplegar

```powershell
# Opción 1: Usar script
.\scripts\deploy_k8s.ps1

# Opción 2: Manual
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/rabbitmq-deployment.yaml
kubectl apply -f kubernetes/scheduler-deployment.yaml
kubectl apply -f kubernetes/gpu-worker-deployment.yaml
kubectl apply -f kubernetes/cpu-worker-deployment.yaml
kubectl apply -f kubernetes/metrics-deployment.yaml
```

### 6. Verificar Despliegue

```powershell
# Ver pods
kubectl get pods -n gpu-cluster

# Ver logs
kubectl logs -f deployment/scheduler -n gpu-cluster
kubectl logs -f deployment/gpu-worker -n gpu-cluster

# Ver servicios
kubectl get svc -n gpu-cluster
```

### 7. Acceder a RabbitMQ UI

```powershell
kubectl port-forward -n gpu-cluster svc/rabbitmq 15672:15672
# Abrir: http://localhost:15672
```

### 8. Enviar Jobs

```powershell
# Port forward para conectar cliente
kubectl port-forward -n gpu-cluster svc/rabbitmq 5672:5672

# Enviar jobs desde local
python client/submit_job.py --job-type matrix-multiply --size 1000
```

## 🎬 Ejecutar Demo

### Demo Rápido

```powershell
# 1. Iniciar servicios
docker-compose up -d

# 2. Esperar a que estén listos (30 segundos)
Start-Sleep -Seconds 30

# 3. Ejecutar demo automatizado
.\scripts\run_demo.ps1
```

### Demo Completo con Benchmarks

```powershell
# 1. Iniciar servicios
docker-compose up -d

# 2. Iniciar monitor en otra terminal
python client/results_monitor.py

# 3. Ejecutar suite de benchmarks
python benchmarks/run_benchmarks.py

# 4. Esperar a que completen (~5-10 minutos)

# 5. Analizar resultados
python benchmarks/analyze_results.py

# 6. Ver reporte
# Abrir: results/BENCHMARK_REPORT.md
# Ver gráficas: results/performance_comparison.png
```

## 🔍 Troubleshooting

### Problema: Worker no se conecta a RabbitMQ

```powershell
# Verificar que RabbitMQ está corriendo
docker-compose ps rabbitmq

# Ver logs de RabbitMQ
docker-compose logs rabbitmq

# Verificar conexión
curl http://localhost:15672/api/overview
```

### Problema: GPU no detectada

```powershell
# Verificar NVIDIA runtime
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi

# Verificar en worker
docker-compose exec gpu-worker python -c "import torch; print(torch.cuda.is_available())"
```

### Problema: Jobs no se procesan

```powershell
# Verificar colas en RabbitMQ
# Ir a: http://localhost:15672/#/queues

# Ver logs de scheduler
docker-compose logs scheduler

# Ver logs de workers
docker-compose logs gpu-worker
docker-compose logs cpu-worker
```

### Problema: Kubernetes pods no inician

```powershell
# Ver estado de pods
kubectl get pods -n gpu-cluster

# Ver eventos
kubectl get events -n gpu-cluster --sort-by='.lastTimestamp'

# Ver logs de pod específico
kubectl logs <pod-name> -n gpu-cluster

# Describir pod para ver errores
kubectl describe pod <pod-name> -n gpu-cluster
```

### Problema: Sin GPU disponible en Kubernetes

```powershell
# Verificar plugin de GPU
kubectl get pods -n kube-system | Select-String nvidia

# Verificar recursos de nodos
kubectl describe node <node-name> | Select-String -Pattern "nvidia.com/gpu"

# Ver nodos con GPU
kubectl get nodes -o json | Select-String "nvidia.com/gpu"
```

## 📊 Verificar Resultados

```powershell
# Ver resultados en tiempo real
python client/results_monitor.py

# Generar análisis
python benchmarks/analyze_results.py

# Ver archivos de resultados
ls results/

# Ver reporte en markdown
cat results/BENCHMARK_REPORT.md

# Abrir gráfica
start results/performance_comparison.png
```

## 🧹 Limpieza

### Docker

```powershell
# Detener servicios
docker-compose down

# Limpiar volúmenes
docker-compose down -v

# Limpiar imágenes
docker rmi gpu-cluster/scheduler:latest
docker rmi gpu-cluster/gpu-worker:latest
docker rmi gpu-cluster/cpu-worker:latest
docker rmi gpu-cluster/metrics:latest
```

### Kubernetes

```powershell
# Eliminar todos los recursos
kubectl delete namespace gpu-cluster

# O eliminar uno por uno
kubectl delete -f kubernetes/
```

## 📚 Recursos Adicionales

- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [PyTorch GPU Support](https://pytorch.org/get-started/locally/)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
- [Kubernetes GPU Support](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/)
