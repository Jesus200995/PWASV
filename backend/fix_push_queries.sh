#!/bin/bash
# Fix para las queries de push - agregar filtro de p256dh y auth

echo "🔧 Arreglando queries de push_subscriptions en main.py..."

# Backup
cp /var/www/PWASV/backend/main.py /var/www/PWASV/backend/main.py.backup_push_fix

# Fix query 1: enviada_a_todos (línea ~6528)
sed -i 's/WHERE ps.activa = TRUE$/WHERE ps.activa = TRUE AND ps.p256dh IS NOT NULL AND ps.auth IS NOT NULL/' /var/www/PWASV/backend/main.py

# Fix query 2: usuarios específicos (línea ~6537)  
sed -i 's/WHERE ps.activa = TRUE AND ps.usuario_id = ANY/WHERE ps.activa = TRUE AND ps.p256dh IS NOT NULL AND ps.auth IS NOT NULL AND ps.usuario_id = ANY/' /var/www/PWASV/backend/main.py

echo "✅ Queries actualizadas"

# Reiniciar servicio
echo "🔄 Reiniciando servicio apipwa..."
systemctl restart apipwa

echo "⏳ Esperando 3 segundos..."
sleep 3

echo "📊 Estado del servicio:"
systemctl status apipwa | head -15

echo "✅ Fix completado!"
