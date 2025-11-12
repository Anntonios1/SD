@echo off
echo ======================================================================
echo      GPU Job Scheduler - Iniciar Servicios Docker
echo ======================================================================
echo.
echo Iniciando todos los servicios (RabbitMQ, Workers, Scheduler, Metrics)...
echo.

cd /d "%~dp0"
docker-compose up -d

echo.
echo ======================================================================
echo Servicios iniciados correctamente
echo ======================================================================
echo.
echo Verificando estado de los contenedores...
echo.

docker-compose ps

echo.
echo ======================================================================
echo Servicios disponibles:
echo   - RabbitMQ Management: http://localhost:15672 (guest/guest)
echo   - Dashboard Web: Ejecuta start_dashboard.bat
echo ======================================================================
echo.

pause
