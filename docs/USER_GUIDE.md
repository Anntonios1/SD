# Guía de Usuario - Sistema Distribuido GPU

## 📚 Contenido
1. [Inicio Rápido](#inicio-rápido)
2. [Enviar Jobs](#enviar-jobs)
3. [Monitorear Resultados](#monitorear-resultados)
4. [Ejecutar Benchmarks](#ejecutar-benchmarks)
5. [Casos de Uso](#casos-de-uso)
6. [Tips y Mejores Prácticas](#tips-y-mejores-prácticas)

## 🚀 Inicio Rápido

### Opción 1: Docker (Recomendado)

```powershell
# 1. Iniciar el cluster
docker-compose up -d

# 2. Esperar 30 segundos para que todo esté listo
Start-Sleep -Seconds 30

# 3. Enviar un job de prueba
python client/submit_job.py --job-type matrix-multiply --size 500

# 4. Ver resultados
python client/results_monitor.py
```

### Opción 2: Local

```powershell
# 1. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 2. Iniciar RabbitMQ
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

# 3. Iniciar componentes (cada uno en una terminal)
python scheduler/scheduler.py          # Terminal 1
python workers/gpu_worker.py           # Terminal 2
python workers/cpu_worker.py           # Terminal 3
python client/results_monitor.py       # Terminal 4

# 4. Enviar jobs (nueva terminal)
python client/submit_job.py --job-type matrix-multiply --size 500
```

## 📤 Enviar Jobs

### Comando Básico

```powershell
python client/submit_job.py --job-type <tipo> [opciones]
```

### Tipos de Jobs Disponibles

#### 1. Matrix Multiplication

Multiplica matrices cuadradas de tamaño NxN.

```powershell
# GPU (por defecto)
python client/submit_job.py --job-type matrix-multiply --size 1000 --iterations 10

# CPU
python client/submit_job.py --job-type matrix-multiply --size 1000 --iterations 10 --cpu

# Múltiples jobs
python client/submit_job.py --job-type matrix-multiply --size 2000 --iterations 5 --count 3
```

**Parámetros:**
- `--size`: Tamaño de la matriz (default: 1000)
- `--iterations`: Número de iteraciones (default: 10)

**Cuándo usar:**
- Benchmark de rendimiento GPU vs CPU
- Operaciones de álgebra lineal
- Simulaciones científicas

#### 2. Neural Network Training

Entrena una red neuronal simple.

```powershell
# GPU
python client/submit_job.py --job-type neural-network --epochs 5 --batch-size 64

# CPU
python client/submit_job.py --job-type neural-network --epochs 5 --batch-size 64 --cpu
```

**Parámetros:**
- `--epochs`: Número de épocas (default: 5)
- `--batch-size`: Tamaño del batch (default: 64)

**Cuándo usar:**
- Entrenamiento de modelos
- Benchmark de deep learning
- Evaluación de aceleración GPU

#### 3. Vector Addition

Suma de vectores grandes.

```powershell
# GPU
python client/submit_job.py --job-type vector-add --size 10000000 --iterations 100

# CPU
python client/submit_job.py --job-type vector-add --size 10000000 --iterations 100 --cpu
```

**Parámetros:**
- `--size`: Tamaño del vector (default: 10000000)
- `--iterations`: Número de iteraciones (default: 100)

**Cuándo usar:**
- Operaciones vectoriales simples
- Benchmark de bandwidth de memoria
- Evaluación de overhead GPU

#### 4. Image Processing

Procesamiento de imágenes con convoluciones.

```powershell
# GPU
python client/submit_job.py --job-type image-processing --batch-size 32 --size 224 --iterations 50

# CPU
python client/submit_job.py --job-type image-processing --batch-size 32 --size 224 --iterations 50 --cpu
```

**Parámetros:**
- `--batch-size`: Número de imágenes (default: 32)
- `--size`: Tamaño de imagen (default: 224)
- `--iterations`: Número de iteraciones (default: 50)

**Cuándo usar:**
- Procesamiento de imágenes
- CNNs
- Computer vision

### Opciones Comunes

```powershell
# Preferir CPU en lugar de GPU
--cpu

# Enviar múltiples jobs
--count 5

# Ver ayuda
--help
```

### Ejemplos de Uso

```powershell
# Job rápido para testing
python client/submit_job.py --job-type matrix-multiply --size 100 --iterations 5

# Benchmark intensivo
python client/submit_job.py --job-type matrix-multiply --size 5000 --iterations 20

# Comparación GPU vs CPU
python client/submit_job.py --job-type neural-network --epochs 10
python client/submit_job.py --job-type neural-network --epochs 10 --cpu

# Batch de jobs
python client/submit_job.py --job-type vector-add --size 50000000 --count 10
```

## 📊 Monitorear Resultados

### Iniciar Monitor

```powershell
# Monitorear en tiempo real
python client/results_monitor.py

# Guardar en archivo específico
python client/results_monitor.py --output results/my_results.json
```

### Salida del Monitor

```
📬 Result received: job-a1b2c3d4e5f6
   Status: completed
   Worker: gpu (gpu-worker-12345678)
   Processing time: 2.3456s
   Job type: matrix_multiply

📈 Current Statistics:
   Total results: 5

   matrix_multiply_gpu:
      Jobs: 3
      Avg time: 2.1234s
      Min time: 1.9876s
      Max time: 2.3456s

   matrix_multiply_cpu:
      Jobs: 2
      Avg time: 15.6789s
      Min time: 14.2345s
      Max time: 17.1234s
```

### Archivos de Resultados

Los resultados se guardan en:
- `results/job_results.json`: Todos los resultados con metadata

Estructura del archivo:
```json
{
  "results": [
    {
      "job_id": "job-abc123",
      "job_type": "matrix_multiply",
      "worker_type": "gpu",
      "processing_time": 2.34,
      "status": "completed",
      ...
    }
  ],
  "stats": {
    "matrix_multiply_gpu": {
      "count": 3,
      "total_time": 6.78,
      "min_time": 1.99,
      "max_time": 2.56
    }
  }
}
```

## 📈 Ejecutar Benchmarks

### Suite Completo

```powershell
# 1. Asegurarse de que el cluster está corriendo
docker-compose up -d

# 2. Iniciar monitor en una terminal
python client/results_monitor.py

# 3. En otra terminal, ejecutar benchmarks
python benchmarks/run_benchmarks.py

# 4. Esperar a que completen (5-10 minutos)

# 5. Analizar resultados
python benchmarks/analyze_results.py
```

### Benchmark Rápido

```powershell
# Solo pruebas rápidas
python benchmarks/run_benchmarks.py --quick
```

### Ver Resultados

```powershell
# Ver reporte generado
cat results/BENCHMARK_REPORT.md

# Ver tabla CSV
Import-Csv results/performance_comparison.csv | Format-Table

# Abrir gráfica
start results/performance_comparison.png
```

### Resultados Esperados

Para hardware típico (ejemplo):

| Job Type | GPU Avg (s) | CPU Avg (s) | Speedup |
|----------|-------------|-------------|---------|
| Matrix Multiply (2000x2000) | 0.15 | 8.50 | 56.7x |
| Neural Network (10 epochs) | 1.20 | 25.30 | 21.1x |
| Vector Addition (50M) | 0.08 | 0.65 | 8.1x |
| Image Processing (64x224x224) | 0.45 | 12.80 | 28.4x |

## 💡 Casos de Uso

### Caso 1: Comparación Rápida GPU vs CPU

```powershell
# Enviar mismo job a GPU y CPU
python client/submit_job.py --job-type matrix-multiply --size 1000
python client/submit_job.py --job-type matrix-multiply --size 1000 --cpu

# Monitorear y comparar tiempos
python client/results_monitor.py
```

### Caso 2: Evaluación de Escalabilidad

```powershell
# Jobs pequeños
python client/submit_job.py --job-type matrix-multiply --size 500 --count 10

# Jobs medianos
python client/submit_job.py --job-type matrix-multiply --size 1000 --count 10

# Jobs grandes
python client/submit_job.py --job-type matrix-multiply --size 2000 --count 10

# Analizar throughput
python benchmarks/analyze_results.py
```

### Caso 3: Simulación de Carga Real

```powershell
# Mix de jobs diferentes
for ($i=1; $i -le 5; $i++) {
    python client/submit_job.py --job-type matrix-multiply --size 1000
    python client/submit_job.py --job-type neural-network --epochs 3
    python client/submit_job.py --job-type vector-add --size 10000000
    python client/submit_job.py --job-type image-processing --batch-size 16
}
```

### Caso 4: Benchmark para Informe

```powershell
# 1. Suite completo
python benchmarks/run_benchmarks.py

# 2. Esperar completar

# 3. Generar análisis
python benchmarks/analyze_results.py

# 4. Copiar archivos para informe
cp results/BENCHMARK_REPORT.md informe/
cp results/performance_comparison.png informe/
cp results/performance_comparison.csv informe/
```

## 🎯 Tips y Mejores Prácticas

### Performance

1. **Warm-up**: El primer job puede ser más lento (inicialización)
2. **Batch jobs**: Para muchos jobs, usar `--count` es más eficiente
3. **Tamaño apropiado**: Jobs muy pequeños (<100) tienen overhead alto
4. **Monitoring**: Mantener monitor corriendo para no perder resultados

### Debugging

```powershell
# Ver logs de componentes
docker-compose logs -f scheduler
docker-compose logs -f gpu-worker
docker-compose logs -f cpu-worker

# Ver estado de colas (RabbitMQ UI)
# Abrir: http://localhost:15672
# Usuario: admin, Password: admin123

# Verificar conectividad
python broker/broker_client.py
```

### Optimización

1. **Para GPU**: Usar tamaños grandes (>1000) para ver ventaja
2. **Para CPU**: Limitar concurrencia para evitar thrashing
3. **Para Comparación**: Usar mismos parámetros exactos

### Troubleshooting

```powershell
# Worker no procesa jobs
docker-compose restart gpu-worker

# Cola llena pero no se procesan
docker-compose restart scheduler

# RabbitMQ no responde
docker-compose restart rabbitmq

# Reset completo
docker-compose down
docker-compose up -d
```

### Para el Informe

1. **Capturas**: Usar RabbitMQ UI para mostrar colas
2. **Logs**: Guardar logs de ejecución exitosa
3. **Gráficas**: Generar con diferentes tamaños de datos
4. **Métricas**: Incluir GPU utilization si es posible

```powershell
# Guardar logs
docker-compose logs > informe/system_logs.txt

# Capturar métricas GPU
nvidia-smi --query-gpu=utilization.gpu,utilization.memory --format=csv --loop=1 > gpu_metrics.csv
```

## 🎓 Ejercicios Sugeridos

### Ejercicio 1: Primera Ejecución
- Iniciar cluster con Docker
- Enviar job de cada tipo
- Monitorear y documentar resultados

### Ejercicio 2: Comparación GPU vs CPU
- Ejecutar suite completo de benchmarks
- Generar reporte con gráficas
- Analizar speedups obtenidos

### Ejercicio 3: Escalabilidad
- Escalar workers (aumentar replicas)
- Enviar batch grande de jobs
- Medir throughput y latencia

### Ejercicio 4: Custom Job
- Implementar nuevo tipo de job
- Agregar a JobExecutor
- Probar y comparar GPU vs CPU

## 📞 Soporte

Para problemas o dudas:
1. Revisar logs: `docker-compose logs`
2. Verificar troubleshooting en DEPLOYMENT_GUIDE.md
3. Revisar arquitectura en ARCHITECTURE.md
