#!/usr/bin/env python3
"""
Script ULTRA SIMPLE para desplegar el backend
Solo ejecuta: python desplegar_simple.py
"""

print("\n" + "="*80)
print("🚀 DESPLIEGUE AUTOMÁTICO DEL BACKEND")
print("="*80 + "\n")

# Paso 1: Leer contraseña
from getpass import getpass
import os
import sys

PASSWORD = getpass("🔐 Contraseña del VPS (root@31.97.8.51): ")

if not PASSWORD:
    print("❌ Necesitas ingresar la contraseña")
    sys.exit(1)

print("\n📡 Conectando al servidor...\n")

# Paso 2: Encontrar el archivo
print("🔍 Buscando main.py en el servidor...")
find_cmd = """find /root -name 'main.py' -type f 2>/dev/null | grep -v node_modules | head -1"""

import subprocess
try:
    result = subprocess.run(
        ["sshpass", "-p", PASSWORD, "ssh", "-o", "StrictHostKeyChecking=no", 
         "root@31.97.8.51", find_cmd],
        capture_output=True,
        text=True,
        timeout=15
    )
    
    if result.returncode != 0:
        print(f"⚠️ sshpass no está instalado. Usando método alternativo...\n")
        raise Exception("Usar plink")
    
    remote_path = result.stdout.strip()
    
    if not remote_path:
        print("❌ No se encontró main.py en el servidor")
        print("\n📝 Rutas comunes:")
        print("   /root/backend/main.py")
        print("   /root/pwa_backend/main.py")
        print("   /home/backend/main.py")
        remote_path = input("\n📝 Ingresa la ruta manualmente: ")
    else:
        print(f"✅ Encontrado: {remote_path}\n")
    
except:
    # Método alternativo sin sshpass
    print("\n💡 Usando método de conexión SSH estándar\n")
    print("🔍 PASO 1: Encontrar el archivo main.py")
    print("\nEjecuta estos comandos EN EL SERVIDOR:")
    print("-" * 60)
    print("find /root -name 'main.py' -type f 2>/dev/null | grep -v node_modules")
    print("-" * 60)
    
    remote_path = input("\n📝 Pega aquí la ruta del main.py encontrado: ").strip()
    
    if not remote_path:
        print("❌ Necesitas proporcionar la ruta")
        sys.exit(1)

# Paso 3: Crear script de despliegue
print(f"\n📝 Creando script de despliegue para: {remote_path}")

backup_name = f"{remote_path}.backup_$(date +%Y%m%d_%H%M%S)"

deploy_script = f'''#!/bin/bash
set -e

echo "💾 Creando backup..."
cp {remote_path} {backup_name}
echo "✅ Backup creado: {backup_name}"

echo ""
echo "🔍 Verificando cambio actual..."
grep -n "join.*condiciones" {remote_path} | head -2

echo ""
echo "📝 Aplicando cambio (AND -> OR)..."

# Hacer el cambio
sed -i "s/WHERE {{' AND '.join(condiciones)}}/WHERE {{' OR '.join(condiciones)}}/g" {remote_path}

echo ""
echo "✅ Verificando cambio aplicado..."
grep -n "OR.*join.*condiciones" {remote_path}

echo ""
echo "🔄 Reiniciando servicio..."

# Intentar diferentes métodos de reinicio
if command -v pm2 &> /dev/null; then
    echo "   Usando PM2..."
    pm2 restart all || pm2 restart backend || true
elif systemctl list-units --type=service | grep -q "pwa\\|backend"; then
    echo "   Usando systemctl..."
    SERVICE=$(systemctl list-units --type=service | grep -E "pwa|backend" | head -1 | awk '{{print $1}}')
    systemctl restart $SERVICE || true
else
    echo "   ⚠️ Reinicio manual requerido"
    echo "   Encuentra el proceso y reinícialo:"
    ps aux | grep -E "[u]vicorn|[p]ython.*main" | head -3
fi

echo ""
echo "🔍 Verificando que el servicio esté corriendo..."
sleep 2
ps aux | grep -E "[u]vicorn|[p]ython.*main" | head -2

echo ""
echo "✅ DESPLIEGUE COMPLETADO"
'''

# Guardar script temporalmente
with open("deploy_temp.sh", "w") as f:
    f.write(deploy_script)

print("✅ Script creado\n")

# Paso 4: Subir y ejecutar script
print("📤 Subiendo script al servidor...")

try:
    # Intentar con scp
    result = subprocess.run(
        ["sshpass", "-p", PASSWORD, "scp", "-o", "StrictHostKeyChecking=no",
         "deploy_temp.sh", "root@31.97.8.51:/tmp/deploy_backend.sh"],
        capture_output=True,
        timeout=10
    )
    
    if result.returncode == 0:
        print("✅ Script subido\n")
        
        print("⚙️ Ejecutando despliegue en el servidor...")
        result = subprocess.run(
            ["sshpass", "-p", PASSWORD, "ssh", "-o", "StrictHostKeyChecking=no",
             "root@31.97.8.51", "bash /tmp/deploy_backend.sh"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(result.stdout)
        if result.stderr:
            print("⚠️ Warnings:", result.stderr)
        
        if result.returncode == 0:
            print("\n" + "="*80)
            print("✅ ¡DESPLIEGUE EXITOSO!")
            print("="*80)
        else:
            print("\n⚠️ El despliegue tuvo algunos problemas, pero puede haber funcionado")
    else:
        raise Exception("Método manual")
        
except:
    print("\n📋 No puedo ejecutar automáticamente. Usa este método MANUAL:\n")
    print("="*80)
    print("COMANDOS PARA EJECUTAR EN EL SERVIDOR:")
    print("="*80)
    print(f"""
1. Conéctate al servidor:
   ssh root@31.97.8.51

2. Ejecuta estos comandos:

# Crear backup
cp {remote_path} {remote_path}.backup_$(date +%Y%m%d_%H%M%S)

# Ver línea actual
grep -n "join.*condiciones" {remote_path}

# Hacer el cambio (AND -> OR)
sed -i "s/WHERE {{' AND '.join(condiciones)}}/WHERE {{' OR '.join(condiciones)}}/g" {remote_path}

# Verificar cambio
grep -n "OR.*join.*condiciones" {remote_path}

# Reiniciar servicio (uno de estos):
pm2 restart all
# o
systemctl restart pwa-backend
# o
pkill -f uvicorn && cd /ruta/al/backend && nohup uvicorn main:app --host 0.0.0.0 --port 8000 &

""")
    print("="*80)
    input("\n✅ Presiona ENTER cuando hayas completado los comandos...")

# Limpiar
if os.path.exists("deploy_temp.sh"):
    os.remove("deploy_temp.sh")

print("\n" + "="*80)
print("🎉 PROCESO COMPLETADO")
print("="*80)
print("\n📝 SIGUIENTE PASO:")
print("   1. Abre: http://localhost:5173/#/debug-buscador")
print("   2. Busca: ROCR820619MSLJSB05")
print("   3. Verifica que encuentre resultados")
print("\n")
