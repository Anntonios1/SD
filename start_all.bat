@echo off
echo ======================================================================
echo      GPU Job Scheduler - Inicio Completo del Sistema
echo ======================================================================
echo.

cd /d "%~dp0"

echo [1/3] Iniciando servicios Docker...
echo.
docker-compose up -d

echo.
echo [2/3] Esperando a que los servicios inicien...
timeout /t 5 /nobreak > nul

echo.
echo [3/3] Abriendo Dashboard en navegador...
start http://localhost:5000

echo.
echo [4/4] Iniciando servidor Flask...
echo.
echo ======================================================================
echo Sistema iniciado correctamente
echo ======================================================================
echo.
echo  Dashboard Web: http://localhost:5000
echo  RabbitMQ UI:   http://localhost:15672 (guest/guest)
echo.
echo Presiona Ctrl+C para detener el servidor Flask
echo (Los servicios Docker seguiran corriendo)
echo ======================================================================
echo.

python dashboard/app.py

pause
