@echo off
echo ======================================================================
echo           GPU Job Scheduler - Dashboard Web Server
echo ======================================================================
echo.
echo Iniciando servidor Flask en http://localhost:5000
echo.
echo Presiona Ctrl+C para detener el servidor
echo ======================================================================
echo.

cd /d "%~dp0"
python dashboard/app.py

pause
