# 🎨 Dashboard Web - Guía de Uso

## 🌐 Acceso
Abre tu navegador en: **http://localhost:5000**

## ✨ Funcionalidades

### 📊 Visualización en Tiempo Real
El dashboard se actualiza automáticamente cada 5 segundos mostrando:
- Total de trabajos procesados
- Trabajos exitosos y fallidos
- Tasa de éxito del sistema
- Gráficas comparativas GPU vs CPU
- Distribución de trabajos por tipo

### 🎮 Botones de Control

#### 🔄 Actualizar Datos
Recarga manualmente todas las métricas y gráficas.

#### ➕ Enviar Trabajo
Abre un formulario interactivo para enviar nuevos trabajos sin usar la terminal.

**Tipos de trabajo disponibles:**
- **Matrix Multiply**: Multiplicación de matrices
  - Parámetros: Tamaño (100-5000), Iteraciones (1-100)
- **Neural Network**: Entrenamiento de red neuronal
  - Parámetros: Epochs (1-50), Batch Size (16-256)
- **Vector Addition**: Suma de vectores
  - Parámetros: Tamaño (1K-100M), Iteraciones (1-100)
- **Image Processing**: Procesamiento de imágenes con convoluciones
  - Parámetros: Batch Size (8-256), Tamaño imagen (64-1024), Iteraciones (1-100)

**Selección de Worker:**
- GPU (RTX 4060) - Recomendado para cargas intensivas
- CPU - Para comparaciones o cargas ligeras

#### ⚡ Benchmark Rápido
Ejecuta 2 pruebas rápidas (matrix multiply y vector add) para verificar el sistema.
- Duración aproximada: 10-15 segundos
- Ideal para pruebas rápidas

#### 🏆 Benchmark Completo
Ejecuta 5 benchmarks intensivos comparando GPU vs CPU:
- Small Matrix (500x500)
- Large Matrix (2000x2000)
- Neural Network (10 epochs)
- Vector Addition (50M elementos)
- Image Processing (64 imágenes 224x224)

**Duración aproximada:** 3-5 minutos

#### 🗑️ Limpiar Errores
Elimina todos los trabajos fallidos del sistema para mantener las estadísticas limpias.

### 📈 Gráficas Interactivas

#### Speedup GPU vs CPU
Muestra cuántas veces más rápido es la GPU comparado con CPU para cada tipo de trabajo.
- 🚀 Verde: Speedup alto (GPU mucho más rápido)
- 🟡 Amarillo: Speedup medio
- 🔵 Azul: Speedup bajo (similar o CPU más rápido)

#### Tiempo Promedio de Procesamiento
Comparación directa de tiempos entre GPU y CPU.

#### Distribución de Trabajos por Tipo
Gráfica de dona mostrando qué tipos de trabajos se han ejecutado más.

#### GPU vs CPU - Trabajos Procesados
Barras comparativas de cuántos trabajos ha procesado cada worker.

### 🏆 Tabla de Benchmarks
Muestra resultados detallados de los benchmarks ejecutados:
- Nombre del benchmark
- Tipo de trabajo
- Tiempo GPU
- Tiempo CPU
- Speedup con código de color

## 💡 Consejos de Uso

1. **Primera vez**: Ejecuta un "Benchmark Rápido" para generar datos iniciales
2. **Testing**: Usa "Enviar Trabajo" para probar trabajos individuales con parámetros específicos
3. **Comparación completa**: Ejecuta "Benchmark Completo" para análisis detallado
4. **Mantenimiento**: Usa "Limpiar Errores" periódicamente si aparecen trabajos fallidos
5. **Monitoreo**: Deja el dashboard abierto para ver resultados en tiempo real

## 🎯 Resultados Esperados

### GPU RTX 4060 - Ventajas
- **Image Processing**: ~18x más rápido que CPU
- **Neural Network**: ~1.3x más rápido que CPU
- **Matrix Multiply (grande)**: Similar o más rápido que CPU

### CPU - Ventajas
- **Operaciones pequeñas**: Vector addition y matrices pequeñas pueden ser más rápidas debido al overhead de transferencia GPU
- **Sin overhead**: No requiere copiar datos a/desde la GPU

## 🔧 Solución de Problemas

### El dashboard no carga
```bash
# Verifica que el servidor esté corriendo
python dashboard/app.py
```

### No aparecen gráficas
- Ejecuta algún benchmark primero para generar datos
- Verifica que `results/job_results.json` exista

### Los benchmarks no se ejecutan
- Verifica que RabbitMQ esté corriendo: `docker ps`
- Verifica que los workers estén activos: `docker-compose ps`

### Errores en los trabajos
- Usa el botón "Limpiar Errores"
- Verifica los logs de los workers: `docker-compose logs gpu-worker`

## 📱 Responsive
El dashboard es responsive y funciona en:
- 💻 Desktop (óptimo)
- 📱 Tablets
- 📱 Móviles (funcionalidad limitada)

## 🚀 Próximos Pasos

1. Abre http://localhost:5000
2. Haz clic en "⚡ Benchmark Rápido"
3. Observa las métricas actualizarse en tiempo real
4. ¡Explora las gráficas y prueba enviar tus propios trabajos!
