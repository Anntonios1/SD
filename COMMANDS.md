# Comandos Útiles - Referencia Rápida

## 🚀 Inicio Rápido

```powershell
# Setup inicial
pip install -r requirements.txt
docker-compose up -d
Start-Sleep -Seconds 30

# Primer job
python client/submit_job.py --job-type matrix-multiply --size 500

# Ver resultados
python client/results_monitor.py
```

## 🐳 Docker

### Gestión de Servicios

```powershell
# Iniciar todo
docker-compose up -d

# Iniciar específico
docker-compose up -d rabbitmq scheduler gpu-worker

# Ver estado
docker-compose ps

# Ver logs
docker-compose logs -f
docker-compose logs -f gpu-worker
docker-compose logs -f scheduler

# Reiniciar servicio
docker-compose restart gpu-worker

# Detener todo
docker-compose down

# Detener y limpiar
docker-compose down -v
```

### Construcción de Imágenes

```powershell
# Construir todas
.\scripts\build_images.ps1

# O con docker-compose
docker-compose build

# Construir específica
docker build -t gpu-cluster/gpu-worker:latest -f docker/Dockerfile.gpu .

# Ver imágenes
docker images | Select-String "gpu-cluster"

# Eliminar imágenes
docker rmi gpu-cluster/gpu-worker:latest
```

### Debugging Docker

```powershell
# Entrar a contenedor
docker-compose exec gpu-worker bash
docker-compose exec scheduler sh

# Ver procesos
docker-compose top

# Ver recursos
docker stats

# Inspeccionar contenedor
docker inspect gpu-worker-1

# Ver networks
docker network ls
docker network inspect proyecto-final_gpu-cluster
```

## 📤 Cliente - Enviar Jobs

### Jobs Básicos

```powershell
# Matrix multiplication
python client/submit_job.py --job-type matrix-multiply --size 1000 --iterations 10

# Neural network
python client/submit_job.py --job-type neural-network --epochs 5 --batch-size 64

# Vector addition
python client/submit_job.py --job-type vector-add --size 10000000 --iterations 100

# Image processing
python client/submit_job.py --job-type image-processing --batch-size 32 --size 224
```

### Opciones Avanzadas

```powershell
# Preferir CPU
python client/submit_job.py --job-type matrix-multiply --size 1000 --cpu

# Múltiples jobs
python client/submit_job.py --job-type matrix-multiply --size 500 --count 10

# Ver ayuda
python client/submit_job.py --help
```

## 📊 Monitoreo y Resultados

### Monitor de Resultados

```powershell
# Monitor en tiempo real
python client/results_monitor.py

# Con archivo específico
python client/results_monitor.py --output results/my_results.json
```

### Ver Resultados

```powershell
# Ver JSON
cat results/job_results.json

# Ver CSV
Import-Csv results/performance_comparison.csv | Format-Table

# Ver reporte
cat results/BENCHMARK_REPORT.md

# Abrir gráfico
start results/performance_comparison.png
```

## 🔬 Benchmarks

### Ejecutar Benchmarks

```powershell
# Suite completo
python benchmarks/run_benchmarks.py

# Modo rápido
python benchmarks/run_benchmarks.py --quick

# Analizar resultados
python benchmarks/analyze_results.py
```

### Demo Automatizado

```powershell
# Demo completo
.\scripts\run_demo.ps1

# O manual:
# Terminal 1
python client/results_monitor.py

# Terminal 2
python benchmarks/run_benchmarks.py
```

## ☸️ Kubernetes

### Despliegue

```powershell
# Deploy completo
.\scripts\deploy_k8s.ps1

# O paso a paso:
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/rabbitmq-deployment.yaml
kubectl apply -f kubernetes/scheduler-deployment.yaml
kubectl apply -f kubernetes/gpu-worker-deployment.yaml
kubectl apply -f kubernetes/cpu-worker-deployment.yaml
kubectl apply -f kubernetes/metrics-deployment.yaml
```

### Gestión de Pods

```powershell
# Ver pods
kubectl get pods -n gpu-cluster
kubectl get pods -n gpu-cluster -o wide

# Ver logs
kubectl logs -f deployment/scheduler -n gpu-cluster
kubectl logs -f deployment/gpu-worker -n gpu-cluster

# Describir pod
kubectl describe pod <pod-name> -n gpu-cluster

# Ver eventos
kubectl get events -n gpu-cluster --sort-by='.lastTimestamp'
```

### Scaling

```powershell
# Escalar workers
kubectl scale deployment gpu-worker --replicas=2 -n gpu-cluster
kubectl scale deployment cpu-worker --replicas=4 -n gpu-cluster

# Auto-scaling (HPA)
kubectl autoscale deployment cpu-worker --cpu-percent=70 --min=2 --max=10 -n gpu-cluster

# Ver HPA
kubectl get hpa -n gpu-cluster
```

### Port Forwarding

```powershell
# RabbitMQ Management
kubectl port-forward -n gpu-cluster svc/rabbitmq 15672:15672

# RabbitMQ AMQP
kubectl port-forward -n gpu-cluster svc/rabbitmq 5672:5672

# Metrics
kubectl port-forward -n gpu-cluster svc/metrics-monitor 8000:8000
```

### Debugging K8s

```powershell
# Entrar a pod
kubectl exec -it <pod-name> -n gpu-cluster -- /bin/bash

# Ver logs de todos los containers
kubectl logs <pod-name> -n gpu-cluster --all-containers=true

# Ver recursos de nodos
kubectl describe nodes

# Ver GPU en nodos
kubectl describe node <node-name> | Select-String "nvidia"
```

### Limpieza K8s

```powershell
# Eliminar deployment específico
kubectl delete deployment gpu-worker -n gpu-cluster

# Eliminar todo
kubectl delete namespace gpu-cluster

# O con archivos
kubectl delete -f kubernetes/
```

## 🎯 GPU

### Monitoreo GPU

```powershell
# Ver estado
nvidia-smi

# Monitor continuo
nvidia-smi -l 1

# Ver procesos
nvidia-smi pmon -s u

# Guardar métricas
nvidia-smi --query-gpu=timestamp,utilization.gpu,utilization.memory,memory.used --format=csv --loop=1 > gpu_metrics.csv

# Durante 60 segundos
nvidia-smi dmon -s u -c 60 > gpu_utilization.log
```

### Testing GPU

```powershell
# Test PyTorch
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"

# Test CUDA
python -c "import torch; print(torch.version.cuda)"

# Test en Docker
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi

# Test worker GPU
docker-compose exec gpu-worker python -c "import torch; print(torch.cuda.is_available())"
```

## 🔧 RabbitMQ

### Management UI

```
URL: http://localhost:15672
Usuario: admin
Password: admin123
```

### CLI Commands

```powershell
# Ver colas
docker-compose exec rabbitmq rabbitmqctl list_queues

# Ver conexiones
docker-compose exec rabbitmq rabbitmqctl list_connections

# Ver consumers
docker-compose exec rabbitmq rabbitmqctl list_consumers

# Purgar cola
docker-compose exec rabbitmq rabbitmqctl purge_queue gpu_queue

# Ver status
docker-compose exec rabbitmq rabbitmqctl status
```

### API REST

```powershell
# Ver overview
curl http://localhost:15672/api/overview -u admin:admin123

# Ver colas
curl http://localhost:15672/api/queues -u admin:admin123

# Ver connections
curl http://localhost:15672/api/connections -u admin:admin123
```

## 🧪 Testing

### System Tests

```powershell
# Test completo
python test_system.py

# Test conexión broker
python broker/broker_client.py

# Test worker GPU
python workers/gpu_worker.py

# Test scheduler
python scheduler/scheduler.py
```

### Manual Testing

```powershell
# Test 1: Conectividad
Test-NetConnection -ComputerName localhost -Port 5672
Test-NetConnection -ComputerName localhost -Port 15672

# Test 2: Docker
docker ps

# Test 3: GPU
nvidia-smi

# Test 4: Python imports
python -c "import pika, torch, numpy; print('OK')"
```

## 📁 Archivos y Directorios

### Ver Estructura

```powershell
# Tree completo
tree /F

# Solo directorios
tree /A

# Archivos específicos
ls -Recurse *.py
ls -Recurse *.yaml
ls -Recurse Dockerfile*
```

### Buscar en Código

```powershell
# Buscar en archivos Python
Select-String -Path *.py -Pattern "def execute"

# Recursivo
Get-ChildItem -Recurse -Filter *.py | Select-String "job_type"

# En directorio específico
Select-String -Path workers/*.py -Pattern "GPU"
```

## 📊 Análisis de Resultados

### Procesamiento de Datos

```powershell
# Ver últimos resultados
Get-Content results/job_results.json | ConvertFrom-Json | Select-Object -Last 5

# Contar jobs por tipo
(Get-Content results/job_results.json | ConvertFrom-Json).results | Group-Object job_type | Select-Object Name, Count

# Ver tiempos promedio
(Get-Content results/job_results.json | ConvertFrom-Json).results | Measure-Object processing_time -Average
```

### Exportar Datos

```powershell
# Copiar resultados
mkdir informe
cp results/* informe/

# Comprimir
Compress-Archive -Path results/* -DestinationPath results_backup.zip

# Crear backup
$date = Get-Date -Format "yyyyMMdd_HHmmss"
cp results/job_results.json "results/backup_$date.json"
```

## 🔄 Mantenimiento

### Limpieza

```powershell
# Limpiar resultados
rm results/*.json, results/*.csv, results/*.png

# Limpiar Docker
docker-compose down -v
docker system prune -a

# Limpiar Python cache
Get-ChildItem -Recurse -Filter __pycache__ | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Filter *.pyc | Remove-Item -Force
```

### Backup

```powershell
# Backup completo
$date = Get-Date -Format "yyyyMMdd"
Compress-Archive -Path . -DestinationPath "../backup_proyecto_$date.zip" -Force

# Backup solo código
Compress-Archive -Path *.py,*.yaml,*.md,docs,workers,broker,scheduler,client -DestinationPath "../codigo_$date.zip"
```

### Logs

```powershell
# Guardar logs
docker-compose logs > system_logs.txt
docker-compose logs gpu-worker > gpu_worker.log
docker-compose logs scheduler > scheduler.log

# Logs con timestamp
docker-compose logs --timestamps > logs_with_time.txt

# Últimas 100 líneas
docker-compose logs --tail=100
```

## 🎓 Para Demo/Presentación

### Preparación

```powershell
# 1. Test completo
python test_system.py

# 2. Iniciar todo
docker-compose up -d
Start-Sleep -Seconds 30

# 3. Verificar
docker-compose ps
curl http://localhost:15672

# 4. Tener terminales listas
# Terminal 1: python client/results_monitor.py
# Terminal 2: comandos para demo
# Browser: http://localhost:15672
```

### Durante Demo

```powershell
# Mostrar arquitectura
cat docs/ARCHITECTURE.md

# Mostrar código
code workers/gpu_worker.py
code scheduler/scheduler.py

# Enviar jobs en vivo
python client/submit_job.py --job-type matrix-multiply --size 1000
python client/submit_job.py --job-type neural-network --epochs 3

# Mostrar resultados
cat results/job_results.json
```

### Post-Demo

```powershell
# Generar reporte
python benchmarks/analyze_results.py

# Mostrar gráficos
start results/performance_comparison.png

# Guardar todo
docker-compose logs > demo_logs.txt
cp results/* demo_results/
```

## 📚 Referencias Rápidas

```powershell
# Ver versiones
python --version
docker --version
docker-compose --version
kubectl version --client

# Ver ayuda
python client/submit_job.py --help
docker-compose --help
kubectl --help

# Abrir documentación
start README.md
start docs/USER_GUIDE.md
start FAQ.md
```

## 🆘 Troubleshooting One-Liners

```powershell
# Reset completo
docker-compose down -v; docker-compose up -d; Start-Sleep -Seconds 30

# Ver todos los logs
docker-compose logs --tail=50

# Test conectividad completa
python test_system.py

# Ver qué está usando puertos
Get-NetTCPConnection -LocalPort 5672,15672 | Select-Object -Property LocalAddress, LocalPort, State, OwningProcess

# Matar proceso en puerto
Stop-Process -Id (Get-NetTCPConnection -LocalPort 5672).OwningProcess -Force
```
