# Sistema Distribuido de Jobs GPU

Proyecto Final - Sistemas Distribuidos

## 📋 Objetivo
Desplegar un servicio capaz de ejecutar jobs que usan GPU (training/inferencia o kernel CUDA) en instancias con GPU y orquestar colas de jobs.

## 🏗️ Arquitectura
```
Cliente → RabbitMQ (Broker) → Scheduler → Workers GPU/CPU → Resultados
```

### Componentes:
1. **Broker (RabbitMQ)**: Cola de mensajes para jobs
2. **Scheduler**: Asigna jobs a workers disponibles
3. **Workers GPU**: Ejecutan jobs con PyTorch/CUDA
4. **Workers CPU**: Ejecutan jobs sin GPU (comparación)
5. **Dashboard Web**: Interfaz visual con métricas y gráficas en tiempo real
6. **Metrics Collector**: Recopila tiempos y métricas

## 📁 Estructura del Proyecto
```
.
├── broker/                      # Configuración RabbitMQ
│   └── broker_client.py         # Cliente para gestión de colas
├── scheduler/                   # Scheduler de jobs
│   └── scheduler.py             # Distribuidor de jobs
├── workers/                     # Workers GPU/CPU
│   ├── gpu_worker.py            # Worker con GPU
│   ├── cpu_worker.py            # Worker con CPU
│   └── jobs/                    # Definición de jobs
│       └── job_executor.py      # Ejecutor de diferentes tipos de jobs
├── client/                      # Cliente para enviar jobs
│   ├── submit_job.py            # CLI para enviar jobs
│   └── results_monitor.py       # Monitor de resultados en tiempo real
├── docker/                      # Dockerfiles
│   ├── Dockerfile.scheduler     # Imagen del scheduler
│   ├── Dockerfile.gpu           # Imagen GPU worker (CUDA)
│   ├── Dockerfile.cpu           # Imagen CPU worker
│   └── Dockerfile.metrics       # Imagen metrics monitor
├── kubernetes/                  # Manifiestos K8s
│   ├── namespace.yaml
│   ├── rabbitmq-deployment.yaml
│   ├── scheduler-deployment.yaml
│   ├── gpu-worker-deployment.yaml
│   ├── cpu-worker-deployment.yaml
│   └── metrics-deployment.yaml
├── benchmarks/                  # Scripts de medición
│   ├── run_benchmarks.py        # Suite de benchmarks
│   └── analyze_results.py       # Análisis y visualización
├── dashboard/                   # Dashboard Web
│   ├── app.py                   # Servidor Flask con REST API
│   ├── templates/               # Interfaz web HTML
│   │   └── index.html           # Dashboard interactivo
│   ├── static/                  # Assets estáticos
│   └── README.md                # Guía del dashboard
├── scripts/                     # Scripts de automatización
│   ├── build_images.ps1         # Construir imágenes Docker
│   ├── deploy_k8s.ps1           # Desplegar en Kubernetes
│   └── run_demo.ps1             # Demo automatizado
├── start_all.bat                # Iniciar sistema completo (Windows)
├── start_dashboard.bat          # Iniciar solo dashboard
├── start_services.bat           # Iniciar solo Docker services
├── stop_services.bat            # Detener servicios Docker
├── docs/                        # Documentación
│   ├── ARCHITECTURE.md          # Arquitectura del sistema
│   ├── DEPLOYMENT_GUIDE.md      # Guía de despliegue
│   └── USER_GUIDE.md            # Guía de usuario
├── results/                     # Resultados y métricas (generado)
├── docker-compose.yml           # Orquestación Docker
├── requirements.txt             # Dependencias Python
├── QUICKSTART.md                # Inicio rápido
└── README.md                    # Este archivo
```

## 🚀 Inicio Rápido

Ver **[QUICKSTART.md](QUICKSTART.md)** para una guía de inicio en 5 minutos.

### Prerrequisitos
- Docker y Docker Compose
- Python 3.9+
- GPU NVIDIA con CUDA (opcional, funciona sin GPU)

### 🎯 Método 1: Dashboard Web (RECOMENDADO)

```powershell
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Iniciar TODO con un solo comando
.\start_all.bat
# Esto inicia: Docker services + Dashboard Web + Abre navegador

# 3. ¡Usar la interfaz visual!
# http://localhost:5000
```

### ⌨️ Método 2: Línea de Comandos

```powershell
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Iniciar servicios con Docker
docker-compose up -d

# 3. Esperar 30 segundos
Start-Sleep -Seconds 30

# 4. Verificar sistema
python test_system.py

# 5. Enviar job de prueba
python client/submit_job.py --job-type matrix-multiply --size 500
```

### Demo Completo

```powershell
# Demo automatizado
.\scripts\run_demo.ps1

# O ejecutar benchmarks completos
python client/results_monitor.py          # Terminal 1
python benchmarks/run_benchmarks.py       # Terminal 2
python benchmarks/analyze_results.py      # Después de completar
```

Ver **[USER_GUIDE.md](docs/USER_GUIDE.md)** para más detalles.

## 📈 Métricas
- Tiempo de ejecución GPU vs CPU
- Throughput de jobs
- Utilización de GPU
- Latencia de cola

## 📦 Entregables

### ✅ Código Fuente
- Sistema distribuido completo
- 4 tipos de jobs GPU/CPU
- Scheduler y broker configurado
- Monitor de métricas en tiempo real

### ✅ Imágenes Docker
- `gpu-cluster/gpu-worker:latest` - Worker con CUDA support
- `gpu-cluster/cpu-worker:latest` - Worker CPU para comparación
- `gpu-cluster/scheduler:latest` - Scheduler de jobs
- `gpu-cluster/metrics:latest` - Monitor de resultados

### ✅ Configuración Kubernetes
- Deployments con taints/tolerations GPU
- Services y networking
- Resource limits y requests
- PersistentVolumeClaims

### ✅ Scripts y Herramientas
- Scripts de build y deployment
- Suite de benchmarks automatizada
- Análisis y visualización de resultados
- Demo automatizado

### ✅ Documentación
- Arquitectura del sistema
- Guías de deployment (Docker/K8s)
- Guía de usuario completa
- Guía para informe IEEE
- Código comentado

### ✅ Resultados
- Benchmarks GPU vs CPU
- Análisis estadístico
- Gráficos comparativos
- Reporte en formato Markdown/CSV

## 🎓 Características Destacadas

- ✨ **Web Dashboard**: Interfaz visual con gráficas interactivas (Chart.js)
- ✨ **One-Click Start**: Archivos .bat para iniciar todo el sistema
- ✨ **Multi-Job Support**: 4 tipos diferentes de jobs
- ✨ **GPU Acceleration**: PyTorch con CUDA
- ✨ **Distributed**: RabbitMQ message broker
- ✨ **Orchestration**: Kubernetes ready
- ✨ **Real-Time Monitoring**: Métricas en vivo con auto-refresh
- ✨ **Automated Benchmarks**: Suite completa con análisis visual
- ✨ **Production-Ready**: Docker containerizado
- ✨ **Well-Documented**: Docs exhaustiva

## 🧪 Testing

```powershell
# Verificar que todo está configurado correctamente
python test_system.py
```

## 📚 Documentación Completa

### � Para Empezar
- **[QUICKSTART.md](QUICKSTART.md)** - Inicio rápido en 5 minutos
- **[FIRST_TIME_SETUP.md](FIRST_TIME_SETUP.md)** - Setup completo desde cero
- **[EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)** - Resumen ejecutivo del proyecto
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Resumen visual con diagramas

### 📖 Guías Principales
- **[USER_GUIDE.md](docs/USER_GUIDE.md)** - Guía completa de usuario
- **[DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)** - Despliegue Docker/Kubernetes
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Arquitectura del sistema

### 📋 Referencias Útiles
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Estado y checklist del proyecto
- **[COMMANDS.md](COMMANDS.md)** - Comandos útiles de referencia rápida
- **[FAQ.md](FAQ.md)** - Preguntas frecuentes y troubleshooting

### 🎓 Para el Proyecto Final
- **[IEEE_REPORT_GUIDE.md](docs/IEEE_REPORT_GUIDE.md)** - Guía completa para el informe IEEE
- **[EXTENDING.md](docs/EXTENDING.md)** - Cómo agregar nuevos jobs y extender el sistema

## 🤝 Contribución

Este proyecto fue desarrollado como proyecto final para la asignatura de Sistemas Distribuidos.

## 📄 Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

## 👥 Autores

Proyecto Final - Sistemas Distribuidos  
Universidad: Unicomfacauca  
Fecha: Octubre 2025
