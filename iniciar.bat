@echo off
title DeepRead v2.0
echo ====================================
echo  DeepRead v2.0 - Lectura Critica
echo ====================================
echo.
echo [1] Iniciar Backend + Frontend (Desarrollo)
echo [2] Iniciar solo Backend (API)
echo [3] Iniciar solo Frontend
echo [4] Instalar dependencias
echo [5] Salir
echo.
set /p op="Selecciona una opcion: "

if "%op%"=="1" (
    echo.
    echo Instalando dependencias del backend...
    cd backend
    pip install -r requirements.txt >nul 2>&1
    cd ..
    echo Iniciando Backend (API) en http://localhost:5000
    echo Iniciando Frontend (React) en http://localhost:5173
    echo.
    start "DeepRead Backend" cmd /c "cd backend && python app.py"
    start "DeepRead Frontend" cmd /c "cd frontend && npm run dev -- --host"
    pause
)

if "%op%"=="2" (
    cd backend
    pip install -r requirements.txt >nul 2>&1
    echo Iniciando API en http://localhost:5000
    python app.py
    pause
)

if "%op%"=="3" (
    cd frontend
    echo Iniciando Frontend en http://localhost:5173
    npm run dev -- --host
    pause
)

if "%op%"=="4" (
    echo Instalando backend...
    cd backend
    pip install -r requirements.txt
    echo.
    echo Instalando frontend...
    cd ../frontend
    npm install
    echo.
    echo Listo!
    pause
)

if "%op%"=="5" exit
