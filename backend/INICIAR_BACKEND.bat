@echo off
echo 🚀 Iniciando Backend PWASV
echo ============================

cd /d "c:\Users\ASUS\Music\PWASV\PWASV\backend"

echo 📂 Directorio: %cd%
echo.

REM Verificar que main.py existe
if not exist main.py (
    echo ❌ ERROR: main.py no encontrado
    pause
    exit /b 1
)

echo ✅ main.py encontrado
echo.
echo 🔧 Instalando/verificando dependencias...
echo.

REM Instalar requirements si es necesario
pip install -q -r requirements.txt 2>nul

echo.
echo 🚀 Iniciando servidor FastAPI en puerto 8000...
echo.
echo ⏳ Espera a que veas "Application startup complete"
echo.

REM Ejecutar con uvicorn
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause
