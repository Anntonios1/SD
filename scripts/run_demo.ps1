# PowerShell script to run complete demo

Write-Host "🎬 Running GPU Cluster Demo" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan

# Check if services are running
Write-Host ""
Write-Host "🔍 Checking services..." -ForegroundColor Yellow
docker-compose ps

Write-Host ""
Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Start results monitor in background
Write-Host ""
Write-Host "📊 Starting results monitor..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python client/results_monitor.py"

Start-Sleep -Seconds 3

# Submit test jobs
Write-Host ""
Write-Host "📤 Submitting test jobs..." -ForegroundColor Yellow
Write-Host ""

# Matrix multiplication
Write-Host "1️⃣  Matrix Multiplication (GPU)..." -ForegroundColor Green
python client/submit_job.py --job-type matrix-multiply --size 1000 --iterations 10
Start-Sleep -Seconds 2

Write-Host "1️⃣  Matrix Multiplication (CPU)..." -ForegroundColor Blue
python client/submit_job.py --job-type matrix-multiply --size 1000 --iterations 10 --cpu
Start-Sleep -Seconds 2

# Neural Network
Write-Host "2️⃣  Neural Network Training (GPU)..." -ForegroundColor Green
python client/submit_job.py --job-type neural-network --epochs 5 --batch-size 64
Start-Sleep -Seconds 2

Write-Host "2️⃣  Neural Network Training (CPU)..." -ForegroundColor Blue
python client/submit_job.py --job-type neural-network --epochs 5 --batch-size 64 --cpu
Start-Sleep -Seconds 2

# Vector addition
Write-Host "3️⃣  Vector Addition (GPU)..." -ForegroundColor Green
python client/submit_job.py --job-type vector-add --size 10000000 --iterations 50
Start-Sleep -Seconds 2

Write-Host "3️⃣  Vector Addition (CPU)..." -ForegroundColor Blue
python client/submit_job.py --job-type vector-add --size 10000000 --iterations 50 --cpu

Write-Host ""
Write-Host "✅ All jobs submitted!" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Monitor results in the other window" -ForegroundColor Cyan
Write-Host "   Press Ctrl+C when all jobs complete" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 After jobs complete, run:" -ForegroundColor Cyan
Write-Host "   python benchmarks/analyze_results.py" -ForegroundColor White
