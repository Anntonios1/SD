"""
Test script to verify all components are working
"""
import sys
import subprocess
import time


def print_test(name, status):
    """Print test result"""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {name}")
    return status


def test_imports():
    """Test if required packages are installed"""
    try:
        import pika
        import torch
        import numpy
        return True
    except ImportError as e:
        print(f"   Missing package: {e}")
        return False


def test_gpu_available():
    """Test if GPU is available"""
    try:
        import torch
        return torch.cuda.is_available()
    except Exception:
        return False


def test_rabbitmq_connection():
    """Test RabbitMQ connection"""
    try:
        sys.path.append('.')
        from broker.broker_client import RabbitMQClient
        
        client = RabbitMQClient()
        client.connect()
        client.close()
        return True
    except Exception as e:
        print(f"   Error: {e}")
        return False


def test_docker():
    """Test if Docker is running"""
    try:
        result = subprocess.run(['docker', 'ps'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        return result.returncode == 0
    except Exception:
        return False


def test_docker_compose():
    """Test if docker-compose services are running"""
    try:
        result = subprocess.run(['docker-compose', 'ps'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        return 'Up' in result.stdout
    except Exception:
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🔍 Sistema Distribuido GPU - Verificación del Sistema")
    print("="*60 + "\n")
    
    results = []
    
    print("📦 Dependencias:")
    results.append(print_test("Paquetes Python instalados", test_imports()))
    results.append(print_test("GPU disponible", test_gpu_available()))
    
    print("\n🐳 Docker:")
    results.append(print_test("Docker está corriendo", test_docker()))
    results.append(print_test("Servicios docker-compose activos", test_docker_compose()))
    
    print("\n🔗 Conectividad:")
    results.append(print_test("Conexión a RabbitMQ", test_rabbitmq_connection()))
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ Todos los tests pasaron ({passed}/{total})")
        print("\n🎉 Sistema listo para usar!")
        print("\nPróximos pasos:")
        print("  1. Ejecutar demo: .\\scripts\\run_demo.ps1")
        print("  2. O enviar job: python client/submit_job.py --job-type matrix-multiply")
    else:
        print(f"⚠️  Algunos tests fallaron ({passed}/{total} pasaron)")
        print("\nRevisa:")
        print("  - Instalar dependencias: pip install -r requirements.txt")
        print("  - Iniciar Docker: docker-compose up -d")
        print("  - Ver troubleshooting en DEPLOYMENT_GUIDE.md")
    
    print("="*60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
