@echo off
echo ============================================================
echo    ACTUALIZACION MASIVA DE SUPERVISORES TECNICOS
echo ============================================================
echo.
echo Este script actualizara automaticamente el supervisor de
echo TODOS los tecnicos en la base de datos.
echo.
echo Presiona cualquier tecla para continuar o Ctrl+C para cancelar...
pause > nul

python actualizar_supervisores_tecnicos.py

echo.
echo ============================================================
echo Presiona cualquier tecla para salir...
pause > nul
