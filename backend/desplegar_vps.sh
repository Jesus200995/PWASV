#!/bin/bash
# Script de despliegue para /var/www/PWASV/backend/main.py

RUTA="/var/www/PWASV/backend/main.py"

echo "================================================================================"
echo "🚀 DESPLEGANDO CAMBIOS EN EL BACKEND"
echo "================================================================================"
echo ""

echo "=== 1. Verificando archivo ==="
ls -la $RUTA
echo ""

echo "=== 2. Haciendo backup ==="
cp $RUTA $RUTA.backup_$(date +%Y%m%d_%H%M%S)
echo "✅ Backup creado"
echo ""

echo "=== 3. Verificando línea actual ==="
grep -n "join.*condiciones" $RUTA | head -2
echo ""

echo "=== 4. Aplicando cambio (AND -> OR) ==="
sed -i "s/WHERE {' AND '.join(condiciones)}/WHERE {' OR '.join(condiciones)}/g" $RUTA
echo "✅ Cambio aplicado"
echo ""

echo "=== 5. Verificando cambio ==="
grep -n "OR.*join.*condiciones" $RUTA
echo ""

echo "=== 6. Reiniciando servicio ==="
cd /var/www/PWASV/backend

# Intentar diferentes métodos
if command -v pm2 &> /dev/null; then
    echo "Usando PM2..."
    pm2 list
    pm2 restart all || pm2 restart backend || pm2 restart main
elif systemctl list-units --type=service | grep -qE "pwa|backend|uvicorn"; then
    echo "Usando systemctl..."
    SERVICE=$(systemctl list-units --type=service | grep -E "pwa|backend|uvicorn" | head -1 | awk '{print $1}')
    echo "Servicio encontrado: $SERVICE"
    systemctl restart $SERVICE
elif command -v supervisorctl &> /dev/null; then
    echo "Usando supervisord..."
    supervisorctl restart all
else
    echo "⚠️ No se detectó método de reinicio automático"
    echo "Buscando proceso para reinicio manual..."
    ps aux | grep -E '[u]vicorn|[p]ython.*main'
    echo ""
    echo "Para reiniciar manualmente:"
    echo "  pkill -f 'uvicorn main:app'"
    echo "  cd /var/www/PWASV/backend"
    echo "  nohup uvicorn main:app --host 0.0.0.0 --port 8000 &"
fi
echo ""

echo "=== 7. Verificando proceso ==="
ps aux | grep -E '[u]vicorn|[p]ython.*main' | head -3
echo ""

echo "================================================================================"
echo "✅ DESPLIEGUE COMPLETADO"
echo "================================================================================"
echo ""
echo "📝 Siguiente paso:"
echo "   1. En tu máquina local: cd admin-pwa && npm run dev"
echo "   2. Abre: http://localhost:5173/#/debug-buscador"
echo "   3. Busca: ROCR820619MSLJSB05"
echo ""
