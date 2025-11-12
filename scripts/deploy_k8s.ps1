# PowerShell script to deploy to Kubernetes

Write-Host "☸️  Deploying GPU Cluster to Kubernetes..." -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Create namespace
Write-Host ""
Write-Host "📦 Creating namespace..." -ForegroundColor Yellow
kubectl apply -f kubernetes/namespace.yaml

# Deploy RabbitMQ
Write-Host ""
Write-Host "🐰 Deploying RabbitMQ..." -ForegroundColor Yellow
kubectl apply -f kubernetes/rabbitmq-deployment.yaml

# Wait for RabbitMQ to be ready
Write-Host ""
Write-Host "⏳ Waiting for RabbitMQ to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Deploy Scheduler
Write-Host ""
Write-Host "📋 Deploying Scheduler..." -ForegroundColor Yellow
kubectl apply -f kubernetes/scheduler-deployment.yaml

# Deploy GPU Workers
Write-Host ""
Write-Host "🎮 Deploying GPU Workers..." -ForegroundColor Yellow
kubectl apply -f kubernetes/gpu-worker-deployment.yaml

# Deploy CPU Workers
Write-Host ""
Write-Host "💻 Deploying CPU Workers..." -ForegroundColor Yellow
kubectl apply -f kubernetes/cpu-worker-deployment.yaml

# Deploy Metrics Monitor
Write-Host ""
Write-Host "📊 Deploying Metrics Monitor..." -ForegroundColor Yellow
kubectl apply -f kubernetes/metrics-deployment.yaml

Write-Host ""
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Check status:" -ForegroundColor Cyan
Write-Host "  kubectl get pods -n gpu-cluster" -ForegroundColor White
Write-Host ""
Write-Host "View logs:" -ForegroundColor Cyan
Write-Host "  kubectl logs -f <pod-name> -n gpu-cluster" -ForegroundColor White
Write-Host ""
Write-Host "Access RabbitMQ Management UI:" -ForegroundColor Cyan
Write-Host "  kubectl port-forward -n gpu-cluster svc/rabbitmq 15672:15672" -ForegroundColor White
Write-Host "  Then visit: http://localhost:15672 (admin/admin123)" -ForegroundColor White
