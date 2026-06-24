#!/bin/bash
# Deploy bitacora-pwa al VPS en ubicacion.sembrandodatos.com
# Ejecutar desde el directorio bitacora-pwa/

set -e

VPS="31.97.8.51"
VPS_USER="root"
REMOTE_DIR="/var/www/ubicacion"
NGINX_CONF="/etc/nginx/sites-available/ubicacion.sembrandodatos.com"

echo "=== 1. Build local ==="
npm install
npm run build

echo "=== 2. Subir archivos al VPS ==="
ssh $VPS_USER@$VPS "mkdir -p $REMOTE_DIR"
scp -r dist/* $VPS_USER@$VPS:$REMOTE_DIR/

echo "=== 3. Configurar nginx ==="
scp nginx_ubicacion.conf $VPS_USER@$VPS:$NGINX_CONF
ssh $VPS_USER@$VPS "
  ln -sf $NGINX_CONF /etc/nginx/sites-enabled/ubicacion.sembrandodatos.com 2>/dev/null || true
  nginx -t && systemctl reload nginx
"

echo "=== 4. Obtener certificado SSL (si no existe) ==="
ssh $VPS_USER@$VPS "
  if [ ! -f /etc/letsencrypt/live/ubicacion.sembrandodatos.com/fullchain.pem ]; then
    certbot --nginx -d ubicacion.sembrandodatos.com --non-interactive --agree-tos -m jesusgomezmarcas@gmail.com
  else
    echo 'Certificado ya existe, ok'
  fi
"

echo "=== 5. Inicializar telemetría en BD ==="
scp ../backend/init_telemetry.py $VPS_USER@$VPS:/tmp/init_telemetry.py
ssh $VPS_USER@$VPS "cd /opt/pwasv && source venv/bin/activate && python /tmp/init_telemetry.py"

echo "=== 6. Reiniciar backend ==="
ssh $VPS_USER@$VPS "systemctl restart pwasv-backend 2>/dev/null || pm2 restart backend 2>/dev/null || true"

echo ""
echo "✅ Deploy completado!"
echo "🌐 Acceso: https://ubicacion.sembrandodatos.com"
echo "👤 Usuario: adminsv"
echo "🔑 Contraseña: sv2026"
