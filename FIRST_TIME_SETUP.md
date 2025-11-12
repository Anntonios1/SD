# 🎬 Primera Vez - Setup Completo

Esta guía te llevará desde cero hasta tener el sistema completamente funcional.

## ✅ Pre-requisitos

### Verificar que tienes instalado:

```powershell
# Python 3.9+
python --version

# Docker
docker --version

# Docker Compose
docker-compose --version

# Git (para clonar o versionar)
git --version
```

### Opcional: GPU

```powershell
# Si tienes GPU NVIDIA
nvidia-smi
```

## 📥 Paso 1: Setup del Proyecto

### 1.1 Crear Entorno Virtual Python

```powershell
# Navegar al directorio del proyecto
cd "C:\Users\teamp\Documents\Proyecto final"

# Crear entorno virtual
python -m venv venv

# Activar entorno
.\venv\Scripts\Activate.ps1

# Verificar activación (debería aparecer (venv) en el prompt)
```

### 1.2 Instalar Dependencias

```powershell
# Instalar dependencias básicas
pip install --upgrade pip
pip install -r requirements.txt

# Para GPU (si tienes NVIDIA GPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Para CPU only (si NO tienes GPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 1.3 Verificar Instalación

```powershell
# Test básico
python -c "import pika, torch, numpy; print('✓ Todas las dependencias instaladas')"

# Test GPU (si aplica)
python -c "import torch; print(f'GPU disponible: {torch.cuda.is_available()}')"
```

## 🐳 Paso 2: Setup de Docker

### 2.1 Iniciar Docker Desktop

```powershell
# Si Docker Desktop no está corriendo
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# Esperar a que inicie (verificar en system tray)
```

### 2.2 Verificar Docker

```powershell
# Test Docker
docker run hello-world

# Test Docker Compose
docker-compose version
```

### 2.3 (Opcional) Setup GPU en Docker

Si tienes GPU NVIDIA:

```powershell
# Verificar NVIDIA runtime
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

Si el comando anterior falla, instalar NVIDIA Container Toolkit:
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

## 🚀 Paso 3: Primera Ejecución

### 3.1 Test del Sistema

```powershell
# Ejecutar tests automáticos
python test_system.py
```

Deberías ver:
```
✅ Paquetes Python instalados
✅ GPU disponible (o ⚠️ si no hay GPU)
⚠️ Docker está corriendo (puede fallar si no hay servicios)
⚠️ Servicios docker-compose activos (normal en primera vez)
⚠️ Conexión a RabbitMQ (normal en primera vez)
```

### 3.2 Iniciar Servicios por Primera Vez

```powershell
# Construir e iniciar todos los servicios
docker-compose up -d --build

# Esto puede tomar 5-10 minutos la primera vez
# porque descarga imágenes base y construye
```

### 3.3 Verificar que Todo Inició

```powershell
# Ver estado de contenedores
docker-compose ps
```

Deberías ver todos con estado "Up":
```
NAME                    STATUS
rabbitmq-broker         Up
job-scheduler           Up
gpu-worker-1            Up
cpu-worker-1            Up
metrics-collector       Up
```

### 3.4 Verificar Logs

```powershell
# Ver logs de todos los servicios
docker-compose logs

# Si ves errores, verificar logs individuales:
docker-compose logs rabbitmq
docker-compose logs scheduler
docker-compose logs gpu-worker
```

Logs saludables deben mostrar:
- RabbitMQ: `Server startup complete`
- Scheduler: `✓ Connected to RabbitMQ` y `Waiting for jobs...`
- Workers: `✓ Connected to RabbitMQ` y `Waiting for jobs...`

## 🎯 Paso 4: Primera Prueba

### 4.1 Enviar Primer Job

```powershell
# Abrir una nueva terminal (mantener la anterior)
cd "C:\Users\teamp\Documents\Proyecto final"
.\venv\Scripts\Activate.ps1

# Enviar job simple
python client/submit_job.py --job-type matrix-multiply --size 100
```

Deberías ver:
```
📤 Submitting job job-xxxxxxxxxxxx
   Type: matrix_multiply
   Prefer GPU: True
   Parameters: {'size': 100, 'iterations': 10}
✓ Job published to gpu_jobs: job-xxxxxxxxxxxx
✓ Job submitted successfully!
```

### 4.2 Ver Procesamiento

```powershell
# Ver logs del worker GPU
docker-compose logs -f gpu-worker
```

Deberías ver:
```
📥 Processing job job-xxxxxxxxxxxx
   Type: matrix_multiply
   Worker: gpu-worker-xxxxxxxx
Running matrix multiplication: 100x100, 10 iterations
✓ Completed in 0.0234s (avg: 0.0023s)
✅ Job job-xxxxxxxxxxxx completed successfully
```

### 4.3 Monitorear Resultados

```powershell
# En otra terminal
cd "C:\Users\teamp\Documents\Proyecto final"
.\venv\Scripts\Activate.ps1

# Iniciar monitor
python client/results_monitor.py
```

Envía más jobs y ve los resultados en tiempo real!

## 🎨 Paso 5: Explorar el Dashboard

### 5.1 Abrir RabbitMQ Management UI

```
URL: http://localhost:15672
Usuario: admin
Password: admin123
```

### 5.2 Explorar las Colas

1. Click en "Queues" en el menú superior
2. Verás 4 colas:
   - `job_queue` - Cola principal
   - `gpu_queue` - Jobs para GPU
   - `cpu_queue` - Jobs para CPU
   - `result_queue` - Resultados

3. Click en cada cola para ver:
   - Mensajes en cola
   - Consumers activos
   - Rate de mensajes

## 📊 Paso 6: Ejecutar Demo Completo

### 6.1 Demo Automatizado

```powershell
# Script que hace todo automáticamente
.\scripts\run_demo.ps1
```

Este script:
1. Verifica servicios
2. Inicia monitor de resultados
3. Envía varios tipos de jobs
4. Muestra comparación GPU vs CPU

### 6.2 Demo Manual

```powershell
# Terminal 1: Monitor
python client/results_monitor.py

# Terminal 2: Enviar jobs
python client/submit_job.py --job-type matrix-multiply --size 1000
python client/submit_job.py --job-type matrix-multiply --size 1000 --cpu

python client/submit_job.py --job-type neural-network --epochs 5
python client/submit_job.py --job-type neural-network --epochs 5 --cpu

python client/submit_job.py --job-type vector-add --size 10000000
python client/submit_job.py --job-type vector-add --size 10000000 --cpu
```

## 📈 Paso 7: Generar Benchmarks

### 7.1 Ejecutar Suite de Benchmarks

```powershell
# Terminal 1: Monitor (si no está corriendo)
python client/results_monitor.py

# Terminal 2: Benchmarks
python benchmarks/run_benchmarks.py

# Esto toma 10-15 minutos
# Envía múltiples jobs de diferentes tipos y tamaños
```

### 7.2 Analizar Resultados

```powershell
# Después de que completen todos los jobs
python benchmarks/analyze_results.py
```

### 7.3 Ver Resultados

```powershell
# Ver reporte en markdown
cat results/BENCHMARK_REPORT.md

# Ver tabla CSV
Import-Csv results/performance_comparison.csv | Format-Table

# Abrir gráfico
start results/performance_comparison.png
```

## 🎓 Paso 8: Para el Informe

### 8.1 Capturar Screenshots

Necesitarás capturas de:
1. RabbitMQ Dashboard mostrando colas
2. Workers procesando jobs (logs)
3. Monitor de resultados
4. Gráficos de performance

### 8.2 Guardar Logs

```powershell
# Guardar logs del sistema
docker-compose logs > informe/system_logs.txt

# Guardar logs específicos
docker-compose logs gpu-worker > informe/gpu_worker.log
docker-compose logs cpu-worker > informe/cpu_worker.log
docker-compose logs scheduler > informe/scheduler.log
```

### 8.3 Copiar Resultados

```powershell
# Crear carpeta para informe
mkdir informe

# Copiar resultados
cp results/*.csv informe/
cp results/*.png informe/
cp results/*.md informe/

# Copiar documentación técnica
cp docs/ARCHITECTURE.md informe/
cp docs/DEPLOYMENT_GUIDE.md informe/
```

## ☸️ Paso 9: (Opcional) Desplegar en Kubernetes

Si quieres probar Kubernetes:

### 9.1 Setup Minikube

```powershell
# Iniciar Minikube
minikube start

# Verificar
kubectl cluster-info
```

### 9.2 Construir y Cargar Imágenes

```powershell
# Construir imágenes
.\scripts\build_images.ps1

# Cargar en Minikube
minikube image load gpu-cluster/scheduler:latest
minikube image load gpu-cluster/gpu-worker:latest
minikube image load gpu-cluster/cpu-worker:latest
minikube image load gpu-cluster/metrics:latest
```

### 9.3 Desplegar

```powershell
# Desplegar todo
.\scripts\deploy_k8s.ps1

# Verificar pods
kubectl get pods -n gpu-cluster

# Ver logs
kubectl logs -f deployment/scheduler -n gpu-cluster
```

## 🔧 Paso 10: Troubleshooting

### Problema: Puerto ya en uso

```powershell
# Ver qué está usando el puerto
Get-NetTCPConnection -LocalPort 5672

# Detener proceso
Stop-Process -Id <PID>

# O cambiar puertos en docker-compose.yml
```

### Problema: Docker no responde

```powershell
# Reiniciar Docker
Restart-Service docker

# O reiniciar Docker Desktop
```

### Problema: Workers no procesan jobs

```powershell
# Ver logs
docker-compose logs gpu-worker
docker-compose logs scheduler

# Reiniciar
docker-compose restart gpu-worker scheduler

# Reset completo
docker-compose down
docker-compose up -d
```

### Problema: "Cannot find module"

```powershell
# Asegurarte de estar en directorio raíz
cd "C:\Users\teamp\Documents\Proyecto final"

# Y entorno virtual activado
.\venv\Scripts\Activate.ps1
```

## ✅ Checklist de Verificación

Después del setup, verifica que puedes:

- [ ] Iniciar servicios: `docker-compose up -d`
- [ ] Ver servicios corriendo: `docker-compose ps`
- [ ] Acceder a RabbitMQ UI: `http://localhost:15672`
- [ ] Enviar un job: `python client/submit_job.py ...`
- [ ] Ver logs de workers: `docker-compose logs gpu-worker`
- [ ] Monitorear resultados: `python client/results_monitor.py`
- [ ] Ejecutar benchmarks: `python benchmarks/run_benchmarks.py`
- [ ] Generar análisis: `python benchmarks/analyze_results.py`

## 🎉 ¡Listo!

Tu sistema está completamente configurado y funcional.

### Próximos pasos:

1. **Experimentar**: Probar diferentes tipos de jobs y tamaños
2. **Documentar**: Tomar screenshots y guardar logs
3. **Benchmarks**: Ejecutar suite completo y analizar resultados
4. **Informe**: Usar docs/IEEE_REPORT_GUIDE.md para escribir el informe
5. **Demo**: Practicar la presentación

### Recursos útiles:

- **Inicio rápido**: QUICKSTART.md
- **Guía de usuario**: docs/USER_GUIDE.md
- **Comandos**: COMMANDS.md
- **FAQ**: FAQ.md

### Ayuda:

Si algo no funciona:
1. Revisa FAQ.md
2. Consulta COMMANDS.md para comandos útiles
3. Lee docs/DEPLOYMENT_GUIDE.md sección Troubleshooting

¡Éxito con tu proyecto! 🚀
