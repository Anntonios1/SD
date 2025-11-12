# Quick Start Guide

## 🚀 Para Empezar en 5 Minutos

### Prerrequisitos
- Docker y Docker Compose instalados
- Python 3.9+

### 🎯 Método 1: Dashboard Web (MÁS FÁCIL)

```powershell
# 1. Instalar dependencias Python
pip install -r requirements.txt

# 2. ¡Un solo comando para iniciar TODO!
.\start_all.bat

# 3. ¡Listo! El navegador se abrirá automáticamente en http://localhost:5000
# - Ver gráficas en tiempo real
# - Enviar jobs con botones
# - Ejecutar benchmarks con un clic
```

### ⌨️ Método 2: Línea de Comandos (Tradicional)

```powershell
# 1. Instalar dependencias Python
pip install -r requirements.txt

# 2. Iniciar el cluster con Docker
docker-compose up -d

# 3. Esperar a que los servicios estén listos (30 segundos)
Start-Sleep -Seconds 30

# 4. Abrir una nueva terminal y monitorear resultados
python client/results_monitor.py

# 5. En otra terminal, enviar un job de prueba
python client/submit_job.py --job-type matrix-multiply --size 1000

# 6. Ver el resultado en el monitor!
```

## 🎨 Dashboard Web

El dashboard incluye:
- 📊 **4 gráficas interactivas** (speedup, tiempos, distribución, comparación)
- 🎮 **Botones interactivos** para enviar jobs y ejecutar benchmarks
- 🔄 **Auto-refresh** cada 5 segundos
- 📈 **Estadísticas en tiempo real** (total jobs, GPU vs CPU, tiempo promedio)

```powershell
# Acceder al dashboard
http://localhost:5000

# Ver documentación del dashboard
cat dashboard/README.md
```

## 📊 Demo Completo

```powershell
# Ejecutar suite de benchmarks GPU vs CPU
.\scripts\run_demo.ps1

# O paso a paso:
docker-compose up -d
python client/results_monitor.py  # Terminal 1
python benchmarks/run_benchmarks.py  # Terminal 2
python benchmarks/analyze_results.py  # Después de completar
```

## 📚 Documentación Completa

- **[USER_GUIDE.md](docs/USER_GUIDE.md)**: Guía completa de usuario
- **[DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)**: Instrucciones de despliegue
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)**: Arquitectura del sistema

## 🎯 Tipos de Jobs Disponibles

1. **Matrix Multiply**: Multiplicación de matrices (ideal para GPU)
2. **Neural Network**: Entrenamiento de redes neuronales
3. **Vector Addition**: Operaciones vectoriales
4. **Image Processing**: Procesamiento de imágenes con convoluciones

## 📈 Ver RabbitMQ Dashboard

```powershell
# Abrir en navegador: http://localhost:15672
# Usuario: admin
# Password: admin123
```

## 🛠️ Comandos Útiles

### Archivos .bat (Windows - MÁS FÁCIL)
```powershell
# Iniciar TODO (servicios + dashboard + navegador)
.\start_all.bat

# Solo iniciar servicios Docker
.\start_services.bat

# Solo iniciar dashboard
.\start_dashboard.bat

# Detener servicios
.\stop_services.bat
```

### Comandos Docker (Manual)
```powershell
# Ver estado de servicios
docker-compose ps

# Ver logs
docker-compose logs -f

# Reiniciar todo
docker-compose restart

# Detener todo
docker-compose down

# Ver ayuda del cliente
python client/submit_job.py --help
```

## 🔧 Troubleshooting Rápido

**Workers no procesan jobs:**
```powershell
docker-compose restart gpu-worker cpu-worker
```

**RabbitMQ no responde:**
```powershell
docker-compose restart rabbitmq
Start-Sleep -Seconds 10
```

**Reset completo:**
```powershell
docker-compose down -v
docker-compose up -d
```

## 📞 Siguiente Paso

Lee la [Guía de Usuario completa](docs/USER_GUIDE.md) para aprender a usar todas las funcionalidades del sistema.
