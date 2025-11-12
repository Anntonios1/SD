@echo off
echo ======================================================================
echo      GPU Job Scheduler - Detener Servicios
echo ======================================================================
echo.
echo Deteniendo todos los servicios Docker...
echo.

cd /d "%~dp0"
docker-compose down

echo.
echo ======================================================================
echo Servicios detenidos correctamente
echo ======================================================================
echo.

pause
