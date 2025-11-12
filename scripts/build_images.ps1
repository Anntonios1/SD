# PowerShell script to build Docker images

Write-Host "🐳 Building Docker images for GPU Cluster..." -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

# Build Scheduler
Write-Host ""
Write-Host "📦 Building Scheduler..." -ForegroundColor Yellow
docker build -t gpu-cluster/scheduler:latest -f docker/Dockerfile.scheduler .

# Build GPU Worker
Write-Host ""
Write-Host "🎮 Building GPU Worker..." -ForegroundColor Yellow
docker build -t gpu-cluster/gpu-worker:latest -f docker/Dockerfile.gpu .

# Build CPU Worker
Write-Host ""
Write-Host "💻 Building CPU Worker..." -ForegroundColor Yellow
docker build -t gpu-cluster/cpu-worker:latest -f docker/Dockerfile.cpu .

# Build Metrics
Write-Host ""
Write-Host "📊 Building Metrics Monitor..." -ForegroundColor Yellow
docker build -t gpu-cluster/metrics:latest -f docker/Dockerfile.metrics .

Write-Host ""
Write-Host "✅ All images built successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the cluster:" -ForegroundColor Cyan
Write-Host "  docker-compose up -d" -ForegroundColor White
Write-Host ""
Write-Host "To view logs:" -ForegroundColor Cyan
Write-Host "  docker-compose logs -f" -ForegroundColor White
