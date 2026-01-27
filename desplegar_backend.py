#!/usr/bin/env python3
"""
Script para desplegar cambios del backend al VPS
Este script copia el archivo main.py al servidor y reinicia el servicio
"""

import subprocess
import sys

VPS_HOST = "31.97.8.51"
VPS_USER = "root"
VPS_BACKEND_PATH = "/root/pwa-backend"
LOCAL_BACKEND_PATH = "backend/main.py"

def ejecutar_comando(comando, descripcion):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n{'=' * 80}")
    print(f"🔄 {descripcion}")
    print(f"{'=' * 80}")
    print(f"Comando: {comando}")
    print()
    
    try:
        resultado = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if resultado.stdout:
            print(resultado.stdout)
        
        if resultado.stderr:
            print("STDERR:", resultado.stderr)
        
        if resultado.returncode == 0:
            print(f"✅ {descripcion} - COMPLETADO")
            return True
        else:
            print(f"❌ {descripcion} - ERROR (código: {resultado.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ {descripcion} - TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ {descripcion} - ERROR: {e}")
        return False

def main():
    print("=" * 80)
    print("🚀 DESPLIEGUE DE BACKEND AL VPS")
    print("=" * 80)
    print()
    print(f"VPS: {VPS_USER}@{VPS_HOST}")
    print(f"Archivo local: {LOCAL_BACKEND_PATH}")
    print(f"Destino VPS: {VPS_BACKEND_PATH}")
    print()
    
    # Paso 1: Copiar main.py al VPS
    comando_scp = f'scp "{LOCAL_BACKEND_PATH}" {VPS_USER}@{VPS_HOST}:{VPS_BACKEND_PATH}/'
    if not ejecutar_comando(comando_scp, "Copiando main.py al VPS"):
        print("\n❌ Error al copiar archivo. Verifica:")
        print("   - Que tengas acceso SSH al servidor")
        print("   - Que la ruta del backend en el VPS sea correcta")
        return False
    
    # Paso 2: Reiniciar servicio del backend
    comando_restart = f'ssh {VPS_USER}@{VPS_HOST} "systemctl restart apipwa"'
    if not ejecutar_comando(comando_restart, "Reiniciando servicio backend"):
        print("\n⚠️ El archivo se copió pero el servicio no se reinició")
        print("   Ejecuta manualmente en el VPS: systemctl restart apipwa")
        return False
    
    # Paso 3: Verificar estado del servicio
    comando_status = f'ssh {VPS_USER}@{VPS_HOST} "systemctl status apipwa --no-pager"'
    ejecutar_comando(comando_status, "Verificando estado del servicio")
    
    print("\n" + "=" * 80)
    print("✅ DESPLIEGUE COMPLETADO")
    print("=" * 80)
    print()
    print("🔄 Próximos pasos:")
    print("   1. Ejecutar: python verificar_supervisores_territoriales.py")
    print("   2. Verificar que los territorios con '/' ahora funcionen")
    print("   3. Ejecutar: python actualizar_supervisores_tecnicos.py")
    print()
    
    return True

if __name__ == "__main__":
    if not main():
        sys.exit(1)
