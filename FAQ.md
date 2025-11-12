# FAQ - Preguntas Frecuentes

## 🤔 Preguntas Generales

### ¿Qué es este proyecto?
Un sistema distribuido que ejecuta jobs computacionales en GPU y CPU, comparando performance y gestionando colas de trabajos con RabbitMQ.

### ¿Para qué sirve?
- Demostrar aceleración GPU vs CPU
- Aprender sistemas distribuidos
- Orquestación de trabajos computacionales
- Proyecto final de Sistemas Distribuidos

### ¿Necesito una GPU física?
No es obligatorio. El sistema funciona en modo CPU-only para testing. Los speedups serán menores pero el sistema es completamente funcional.

## 🛠️ Instalación y Configuración

### ¿Cómo instalo las dependencias?

```powershell
# 1. Crear entorno virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Para GPU (opcional)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### ¿Cómo verifico que tengo GPU disponible?

```powershell
# Test 1: NVIDIA SMI
nvidia-smi

# Test 2: PyTorch
python -c "import torch; print(torch.cuda.is_available())"

# Test 3: Script de verificación
python test_system.py
```

### ¿Qué hacer si no tengo GPU?

El sistema funciona perfectamente sin GPU:
- Los workers GPU se ejecutarán en CPU
- Podrás comparar workers optimizados vs no optimizados
- Los speedups serán menores pero funcional

## 🐳 Docker

### ¿Cómo inicio el sistema con Docker?

```powershell
# Iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

### ¿Cómo verifico que los contenedores están corriendo?

```powershell
docker-compose ps
```

Deberías ver:
- `rabbitmq-broker` - Up
- `job-scheduler` - Up
- `gpu-worker-1` - Up
- `cpu-worker-1` - Up
- `metrics-collector` - Up

### ¿Cómo accedo al RabbitMQ Dashboard?

```
URL: http://localhost:15672
Usuario: admin
Password: admin123
```

### Error: "no configuration file provided"

```powershell
# Asegúrate de estar en el directorio raíz del proyecto
cd "C:\Users\teamp\Documents\Proyecto final"
docker-compose up -d
```

### Error: "Cannot connect to the Docker daemon"

```powershell
# Iniciar Docker Desktop
# O desde servicios:
Start-Service docker
```

### Error: "nvidia runtime not found"

Si no tienes GPU, modifica `docker-compose.yml`:

```yaml
# Comentar estas líneas en gpu-worker:
# runtime: nvidia
# deploy:
#   resources:
#     reservations:
#       devices:
#         - driver: nvidia
#           count: 1
#           capabilities: [gpu]
```

## 📤 Enviar Jobs

### ¿Cómo envío mi primer job?

```powershell
python client/submit_job.py --job-type matrix-multiply --size 500
```

### ¿Qué tipos de jobs puedo enviar?

1. `matrix-multiply` - Multiplicación de matrices
2. `neural-network` - Entrenamiento de red neuronal
3. `vector-add` - Suma de vectores
4. `image-processing` - Procesamiento de imágenes

### ¿Cómo especifico GPU o CPU?

```powershell
# GPU (default)
python client/submit_job.py --job-type matrix-multiply --size 1000

# CPU
python client/submit_job.py --job-type matrix-multiply --size 1000 --cpu
```

### ¿Cómo envío múltiples jobs?

```powershell
python client/submit_job.py --job-type matrix-multiply --size 1000 --count 10
```

### ¿Dónde veo los resultados?

```powershell
# Monitor en tiempo real
python client/results_monitor.py

# Archivo de resultados
cat results/job_results.json
```

## 📊 Benchmarks y Resultados

### ¿Cómo ejecuto los benchmarks?

```powershell
# 1. Iniciar monitor (Terminal 1)
python client/results_monitor.py

# 2. Ejecutar benchmarks (Terminal 2)
python benchmarks/run_benchmarks.py

# 3. Esperar a que completen (5-10 min)

# 4. Analizar
python benchmarks/analyze_results.py
```

### ¿Cuánto tiempo toman los benchmarks?

- **Quick mode**: 2-3 minutos
- **Full suite**: 10-15 minutos
- Depende de tu hardware

### ¿Dónde están los resultados?

```
results/
├── job_results.json              # Datos crudos
├── performance_comparison.csv    # Tabla comparativa
├── performance_comparison.png    # Gráficos
└── BENCHMARK_REPORT.md           # Reporte
```

### ¿Qué speedups son normales?

Depende del hardware, pero típicamente:
- Matrix Multiply: 30-100x
- Neural Network: 20-50x
- Image Processing: 25-60x
- Vector Addition: 5-15x

## ☸️ Kubernetes

### ¿Cómo despliego en Kubernetes?

```powershell
# 1. Construir imágenes
.\scripts\build_images.ps1

# 2. Cargar en Minikube (si usas Minikube)
minikube image load gpu-cluster/scheduler:latest
# ... repetir para todas las imágenes

# 3. Desplegar
.\scripts\deploy_k8s.ps1

# 4. Verificar
kubectl get pods -n gpu-cluster
```

### ¿Cómo etiquetar nodos GPU?

```bash
# Listar nodos
kubectl get nodes

# Etiquetar nodo con GPU
kubectl label nodes <node-name> accelerator=nvidia-gpu

# Verificar
kubectl get nodes --show-labels | grep gpu
```

### ¿Cómo escalar workers?

```bash
# Escalar GPU workers
kubectl scale deployment gpu-worker --replicas=2 -n gpu-cluster

# Escalar CPU workers
kubectl scale deployment cpu-worker --replicas=4 -n gpu-cluster
```

### ¿Cómo ver logs en Kubernetes?

```bash
# Logs de scheduler
kubectl logs -f deployment/scheduler -n gpu-cluster

# Logs de GPU worker
kubectl logs -f deployment/gpu-worker -n gpu-cluster

# Todos los logs
kubectl logs -f -l app=gpu-worker -n gpu-cluster --all-containers
```

## 🐛 Troubleshooting

### Workers no procesan jobs

```powershell
# Verificar que RabbitMQ está corriendo
docker-compose ps rabbitmq

# Reiniciar workers
docker-compose restart gpu-worker cpu-worker

# Ver logs
docker-compose logs -f gpu-worker
```

### "Connection refused" al conectar a RabbitMQ

```powershell
# Esperar 30 segundos después de iniciar
Start-Sleep -Seconds 30

# Verificar que el puerto está abierto
Test-NetConnection -ComputerName localhost -Port 5672

# Reiniciar RabbitMQ
docker-compose restart rabbitmq
```

### Jobs se quedan en la cola sin procesarse

1. Verificar que hay workers corriendo:
   ```powershell
   docker-compose ps
   ```

2. Verificar que el scheduler está corriendo:
   ```powershell
   docker-compose logs scheduler
   ```

3. Verificar colas en RabbitMQ:
   - Ir a http://localhost:15672
   - Ver pestaña "Queues"
   - Verificar consumers activos

### "CUDA out of memory"

```powershell
# Reducir tamaño de jobs
python client/submit_job.py --job-type matrix-multiply --size 500

# O reducir batch size
python client/submit_job.py --job-type neural-network --batch-size 32
```

### Importación de módulos falla

```powershell
# Asegurarte de estar en el directorio raíz
cd "C:\Users\teamp\Documents\Proyecto final"

# Verificar que el módulo existe
ls workers/jobs/job_executor.py

# Ejecutar desde raíz
python client/submit_job.py
```

## 📝 Informe IEEE

### ¿Qué debe incluir el informe?

Ver la guía completa en `docs/IEEE_REPORT_GUIDE.md`

Secciones principales:
1. Abstract
2. Introduction
3. Architecture
4. Implementation
5. Experimental Results
6. Analysis
7. Conclusions

### ¿Qué figuras incluir?

Mínimo:
1. Diagrama de arquitectura
2. Gráfico GPU vs CPU
3. Tabla de resultados
4. Diagrama de flujo
5. Screenshots del sistema

### ¿Cómo genero los resultados para el informe?

```powershell
# 1. Ejecutar benchmarks
python benchmarks/run_benchmarks.py

# 2. Analizar
python benchmarks/analyze_results.py

# 3. Copiar archivos
mkdir informe
cp results/performance_comparison.* informe/
cp results/BENCHMARK_REPORT.md informe/
```

## 🎯 Performance

### ¿Cómo mejoro el rendimiento?

1. **Usar tamaños grandes**: Jobs >1000 aprovechan mejor GPU
2. **Batch jobs**: Enviar múltiples jobs a la vez
3. **Ajustar parámetros**: Experimentar con diferentes configs
4. **Monitorear GPU**: Usar nvidia-smi para ver utilización

### ¿Por qué algunos jobs son lentos en GPU?

- **Overhead de transferencia**: Jobs muy pequeños
- **No paralelizable**: Algunos algoritmos no se benefician
- **Memory bound**: Limitado por bandwidth de memoria

### ¿Cómo monitoreo utilización de GPU?

```powershell
# Consola interactiva
nvidia-smi -l 1

# Guardar a archivo
nvidia-smi --query-gpu=utilization.gpu,utilization.memory --format=csv --loop=1 > gpu_usage.csv
```

## 🔧 Desarrollo

### ¿Cómo agrego un nuevo tipo de job?

Ver guía completa en `docs/EXTENDING.md`

Pasos básicos:
1. Agregar método en `JobExecutor`
2. Registrar en `execute()`
3. Agregar helper en `JobClient`
4. Actualizar CLI

### ¿Cómo modifico el scheduler?

Editar `scheduler/scheduler.py`:
- Implementar nueva estrategia de scheduling
- Agregar prioridades
- Load balancing
- SLA awareness

### ¿Cómo agrego nuevas métricas?

1. Modificar worker para recopilar métrica
2. Incluir en resultado del job
3. Actualizar monitor para procesar
4. Actualizar análisis para visualizar

## 🎓 Para el Proyecto Final

### ¿Es suficiente para aprobar?

Sí. El proyecto incluye:
- ✅ Sistema distribuido funcional
- ✅ Workers GPU/CPU
- ✅ Cola de mensajes (RabbitMQ)
- ✅ Scheduler
- ✅ Containerización (Docker)
- ✅ Orquestación (Kubernetes)
- ✅ Benchmarks y métricas
- ✅ Documentación completa

### ¿Qué mostrar en la demo?

1. **Arquitectura**: Explicar componentes
2. **Despliegue**: Mostrar Docker/K8s
3. **Ejecución**: Enviar jobs en vivo
4. **Resultados**: Mostrar comparación GPU vs CPU
5. **Métricas**: Dashboard de RabbitMQ
6. **Código**: Mostrar implementación clave

### ¿Qué hacer si no funciona en la demo?

1. **Tener video backup**: Grabar demo funcionando
2. **Screenshots**: Capturar todo con anticipación
3. **Logs guardados**: Tener logs de ejecución exitosa
4. **Resultados pre-generados**: Tener benchmarks ya ejecutados

## 💡 Tips Finales

### Antes de la entrega

```powershell
# Test completo del sistema
python test_system.py

# Ejecutar demo completo
.\scripts\run_demo.ps1

# Generar todos los resultados
python benchmarks/run_benchmarks.py
python benchmarks/analyze_results.py

# Verificar documentación
ls docs/
ls results/
```

### Para la presentación

1. Practicar demo varias veces
2. Tener terminal lista con comandos
3. Abrir RabbitMQ dashboard
4. Tener gráficos visibles
5. Preparar explicación de arquitectura

### Recursos útiles

- `QUICKSTART.md` - Inicio rápido
- `PROJECT_STATUS.md` - Estado completo
- `docs/USER_GUIDE.md` - Guía detallada
- `docs/DEPLOYMENT_GUIDE.md` - Troubleshooting

## ❓ ¿Más preguntas?

Revisa la documentación en la carpeta `docs/` o los archivos:
- README.md
- QUICKSTART.md
- PROJECT_STATUS.md
- docs/USER_GUIDE.md
- docs/DEPLOYMENT_GUIDE.md
- docs/ARCHITECTURE.md
- docs/IEEE_REPORT_GUIDE.md
- docs/EXTENDING.md
