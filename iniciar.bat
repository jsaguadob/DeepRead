@echo off
set PYTHON=C:\Users\jsab0\AppData\Local\Programs\Python\Python314\python.exe
title DeepRead - Servidor de Lectura Critica
color 0A
cls
echo ========================================
echo   DeepRead - Servidor de Lectura Critica
echo ========================================
echo.
echo Servidor iniciando en http://127.0.0.1:5000
echo Presiona CTRL+C para detener el servidor
echo.
echo NO CIERRES esta ventana mientras uses la app
echo.
cd /d "%~dp0"
"%PYTHON%" app.py
echo.
echo Servidor detenido. Presiona cualquier tecla para salir...
pause >nul