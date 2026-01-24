@echo off
REM Script para iniciar Backend (Mock o Real) + Frontend

echo.
echo ================================================
echo  PWA SUPER - INICIAR SISTEMA COMPLETO
echo ================================================
echo.

REM Verificar si ya hay terminales abiertas
echo Abriendo terminales para Backend y Frontend...
echo.

REM Terminal 1: Backend Mock
echo 1. Abriendo Backend Mock Server en puerto 8000...
start "Backend Mock Server" cmd.exe /k "cd /d c:\Users\ASUS\Music\PWASV\PWASV && node mock-server.js"

REM Esperar un poco para que el backend inicie
timeout /t 2 /nobreak

REM Terminal 2: Frontend
echo 2. Abriendo Frontend Dev Server en puerto 5173...
start "Frontend Dev Server" cmd.exe /k "cd /d c:\Users\ASUS\Music\PWASV\PWASV\pwasuper && npm run dev"

echo.
echo ================================================
echo  ✅ Servidores iniciándose...
echo ================================================
echo.
echo 📱 Frontend:  http://localhost:5173
echo 🔗 Backend:   http://localhost:8000
echo.
echo Espera a que ambas terminales muestren "ready/listening"
echo.
echo.
pause
