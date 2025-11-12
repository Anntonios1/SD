#!/bin/bash
# Build all Docker images for the GPU cluster

echo "🐳 Building Docker images for GPU Cluster..."
echo "=============================================="

# Build Scheduler
echo ""
echo "📦 Building Scheduler..."
docker build -t gpu-cluster/scheduler:latest -f docker/Dockerfile.scheduler .

# Build GPU Worker
echo ""
echo "🎮 Building GPU Worker..."
docker build -t gpu-cluster/gpu-worker:latest -f docker/Dockerfile.gpu .

# Build CPU Worker
echo ""
echo "💻 Building CPU Worker..."
docker build -t gpu-cluster/cpu-worker:latest -f docker/Dockerfile.cpu .

# Build Metrics
echo ""
echo "📊 Building Metrics Monitor..."
docker build -t gpu-cluster/metrics:latest -f docker/Dockerfile.metrics .

echo ""
echo "✅ All images built successfully!"
echo ""
echo "To start the cluster:"
echo "  docker-compose up -d"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
