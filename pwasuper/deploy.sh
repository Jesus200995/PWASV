#!/bin/bash

echo "🚀 Iniciando deployment completo..."

# Ir al directorio correcto
cd /var/www/PWASV/pwasuper

# Pull de los cambios
echo "📥 Descargando cambios de GitHub..."
git pull origin main

# Instalar dependencias si es necesario
echo "📦 Verificando dependencias..."
npm install

# Compilar proyecto
echo "🔨 Compilando proyecto..."
npm run build

# Eliminar COMPLETAMENTE archivos antiguos
echo "🗑️ Eliminando archivos antiguos..."
sudo rm -rf /var/www/app.sembrandodatos.com/*

# Copiar nuevos archivos
echo "📋 Copiando archivos nuevos..."
sudo cp -r dist/* /var/www/app.sembrandodatos.com/

# Establecer permisos correctos
echo "🔐 Estableciendo permisos..."
sudo chown -R www-data:www-data /var/www/app.sembrandodatos.com/
sudo chmod -R 755 /var/www/app.sembrandodatos.com/

# Reiniciar nginx COMPLETAMENTE
echo "🔄 Reiniciando nginx..."
sudo systemctl stop nginx
sleep 2
sudo systemctl start nginx

# Limpiar caché de nginx si existe
if [ -d /var/cache/nginx ]; then
    echo "🧹 Limpiando caché de nginx..."
    sudo rm -rf /var/cache/nginx/*
fi

# Mostrar hash de archivos para verificar
echo ""
echo "✅ Deployment completado!"
echo ""
echo "📊 Hash de archivos principales:"
md5sum /var/www/app.sembrandodatos.com/index.html
ls -lh /var/www/app.sembrandodatos.com/assets/*.js | tail -3

echo ""
echo "🌐 Verifica en el navegador:"
echo "1. Abre DevTools (F12)"
echo "2. Application → Service Workers → Unregister"
echo "3. Application → Cache Storage → Delete all"
echo "4. Ctrl+Shift+Delete → Clear everything"
echo "5. Cierra el navegador COMPLETAMENTE"
echo "6. Abre de nuevo: https://app.sembrandodatos.com"
echo ""
echo "🟢 Debes ver un círculo verde parpadeando en Reportes"
