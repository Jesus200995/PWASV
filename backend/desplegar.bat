@echo off
echo ================================================================================
echo DESPLIEGUE DEL BACKEND - PASO A PASO
echo ================================================================================
echo.

echo 1. Conectandote al servidor...
echo.

ssh root@31.97.8.51 "echo '=== Buscando main.py ===' && find /root /home -name 'main.py' -type f 2>/dev/null | grep -E 'backend|pwa' | head -3 && echo '' && echo '=== Contenido de /root ===' && ls -la /root | grep -E 'backend|pwa|app'"

echo.
echo ================================================================================
echo.
echo Ahora vamos a hacer el despliegue.
echo.
set /p RUTA="Ingresa la ruta completa del main.py (ej: /root/backend/main.py): "

if "%RUTA%"=="" (
    echo ERROR: Debes proporcionar una ruta
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo 2. Haciendo backup y desplegando cambios...
echo ================================================================================
echo.

ssh root@31.97.8.51 "echo '=== Creando backup ===' && cp %RUTA% %RUTA%.backup_$(date +%%Y%%m%%d_%%H%%M%%S) && echo 'Backup creado' && echo '' && echo '=== Verificando linea actual ===' && grep -n 'join.*condiciones' %RUTA% | head -2 && echo '' && echo '=== Aplicando cambio (AND -> OR) ===' && sed -i \"s/WHERE {' AND '.join(condiciones)}/WHERE {' OR '.join(condiciones)}/g\" %RUTA% && echo 'Cambio aplicado' && echo '' && echo '=== Verificando cambio ===' && grep -n 'OR.*join.*condiciones' %RUTA% && echo '' && echo '=== Reiniciando servicio ===' && pm2 restart all 2>/dev/null || systemctl restart pwa-backend 2>/dev/null || echo 'Reinicia manualmente' && echo '' && echo '=== Verificando proceso ===' && ps aux | grep -E '[u]vicorn|[p]ython.*main' | head -2"

echo.
echo ================================================================================
echo 3. COMPLETADO!
echo ================================================================================
echo.
echo Siguiente paso:
echo   1. Inicia el admin-pwa: cd admin-pwa ^&^& npm run dev
echo   2. Abre: http://localhost:5173/#/debug-buscador
echo   3. Busca: ROCR820619MSLJSB05
echo.
pause
