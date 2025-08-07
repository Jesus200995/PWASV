#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la funcionalidad completa de términos y condiciones
ANTES de desplegar en producción.

Autor: Sistema PWA
Fecha: 7 de agosto de 2025
"""

import requests
import json
import sys
from datetime import datetime

# Configuración
BASE_URL_LOCAL = "http://127.0.0.1:8000"
BASE_URL_PROD = "https://apipwa.sembrandodatos.com"

def print_header(titulo):
    print(f"\n{'='*60}")
    print(f"🔍 {titulo}")
    print('='*60)

def print_success(mensaje):
    print(f"✅ {mensaje}")

def print_error(mensaje):
    print(f"❌ {mensaje}")

def print_info(mensaje):
    print(f"📝 {mensaje}")

def test_terminos_local():
    """Prueba la funcionalidad de términos en el servidor local"""
    print_header("PRUEBAS EN SERVIDOR LOCAL")
    
    try:
        # 1. Test endpoint de prueba
        print_info("1. Probando endpoint de prueba...")
        response = requests.get(f"{BASE_URL_LOCAL}/test/terminos")
        if response.status_code == 200:
            print_success(f"Endpoint de prueba: {response.status_code}")
            data = response.json()
            print(f"   Versión: {data.get('version', 'N/A')}")
        else:
            print_error(f"Endpoint de prueba falló: {response.status_code}")
            return False
        
        # 2. Test creación de usuario con términos automáticos
        print_info("2. Probando creación de usuario con términos automáticos...")
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # Sin guión bajo
        # Generar CURP de exactamente 18 caracteres única
        curp_unica = f"TEST{timestamp[-8:]}ABCD01"  # TEST + 8 dígitos + ABCD01 = 4+8+6 = 18 caracteres
        print(f"   CURP generada: {curp_unica} (longitud: {len(curp_unica)})")
        test_user = {
            "correo": f"test_terminos_{timestamp}@test.com",
            "nombre_completo": "Usuario Test Términos",
            "cargo": "Tester",
            "supervisor": "Admin Test",
            "contrasena": "test123456",
            "curp": curp_unica
        }
        
        response = requests.post(f"{BASE_URL_LOCAL}/usuarios", json=test_user)
        if response.status_code == 200:
            data = response.json()
            user_id = data["id"]
            print_success(f"Usuario creado con ID: {user_id}")
            print_success(f"Términos registrados: {data.get('terminos_registrados', False)}")
        else:
            print_error(f"Error creando usuario: {response.status_code} - {response.text}")
            return False
        
        # 3. Test verificación de términos
        print_info("3. Probando verificación de términos...")
        response = requests.get(f"{BASE_URL_LOCAL}/usuarios/{user_id}/terminos")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Términos verificados para usuario {user_id}")
            print(f"   Ha aceptado: {data['ha_aceptado_terminos']}")
            print(f"   Fecha: {data['fecha_aceptacion']}")
            
            if not data['ha_aceptado_terminos']:
                print_error("¡El usuario debería tener términos aceptados automáticamente!")
                return False
        else:
            print_error(f"Error verificando términos: {response.status_code} - {response.text}")
            return False
        
        # 4. Test aceptación manual de términos
        print_info("4. Probando aceptación manual de términos...")
        response = requests.post(f"{BASE_URL_LOCAL}/usuarios/aceptar_terminos", 
                               json={"usuario_id": user_id})
        if response.status_code == 200:
            data = response.json()
            print_success(f"Términos aceptados manualmente: {data['status']}")
        else:
            print_error(f"Error aceptando términos: {response.status_code} - {response.text}")
            return False
        
        print_success("🎉 TODAS LAS PRUEBAS LOCALES PASARON EXITOSAMENTE")
        return True
        
    except requests.exceptions.ConnectionError:
        print_error("No se puede conectar al servidor local. ¿Está ejecutándose en el puerto 8000?")
        return False
    except Exception as e:
        print_error(f"Error inesperado en pruebas locales: {e}")
        return False

def test_terminos_produccion():
    """Prueba si los endpoints de términos existen en producción"""
    print_header("VERIFICACIÓN EN PRODUCCIÓN")
    
    try:
        # 1. Test endpoint de prueba
        print_info("1. Verificando endpoint de prueba en producción...")
        response = requests.get(f"{BASE_URL_PROD}/test/terminos", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_success("✅ Endpoints de términos están ACTIVOS en producción")
            print(f"   Versión: {data.get('version', 'N/A')}")
            return True
        else:
            print_error(f"Endpoint de prueba no existe: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print_error(f"Error conectando a producción: {e}")
        return False

def verificar_usuarios_sin_terminos():
    """Verifica cuántos usuarios en producción no tienen términos aceptados"""
    print_header("VERIFICACIÓN DE USUARIOS SIN TÉRMINOS")
    
    try:
        # Obtener lista de usuarios
        response = requests.get(f"{BASE_URL_PROD}/usuarios", timeout=10)
        if response.status_code != 200:
            print_error("No se pueden obtener usuarios de producción")
            return
        
        usuarios = response.json().get("usuarios", [])
        print_info(f"Total de usuarios en producción: {len(usuarios)}")
        
        usuarios_sin_terminos = []
        usuarios_con_terminos = []
        
        for usuario in usuarios:
            user_id = usuario["id"]
            try:
                response = requests.get(f"{BASE_URL_PROD}/usuarios/{user_id}/terminos", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data["ha_aceptado_terminos"]:
                        usuarios_con_terminos.append(user_id)
                    else:
                        usuarios_sin_terminos.append(user_id)
                else:
                    usuarios_sin_terminos.append(user_id)
            except:
                usuarios_sin_terminos.append(user_id)
        
        print_info(f"Usuarios CON términos: {len(usuarios_con_terminos)}")
        print_info(f"Usuarios SIN términos: {len(usuarios_sin_terminos)}")
        
        if usuarios_sin_terminos:
            print_error(f"Usuarios sin términos: {usuarios_sin_terminos}")
        else:
            print_success("Todos los usuarios tienen términos aceptados")
            
    except Exception as e:
        print_error(f"Error verificando usuarios: {e}")

def main():
    print("🚀 SISTEMA DE PRUEBAS PARA TÉRMINOS Y CONDICIONES")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Paso 1: Probar funcionalidad local
    print_info("Iniciando pruebas en servidor local...")
    if not test_terminos_local():
        print_error("Las pruebas locales fallaron. No continuar con producción.")
        sys.exit(1)
    
    # Paso 2: Verificar estado de producción
    print_info("Verificando estado de producción...")
    if test_terminos_produccion():
        print_success("🎉 Los endpoints YA ESTÁN ACTIVOS en producción")
        verificar_usuarios_sin_terminos()
    else:
        print_error("❌ Los endpoints NO están activos en producción")
        print_info("📋 ACCIONES NECESARIAS:")
        print("   1. Copiar main_produccion_completo.py al servidor de producción")
        print("   2. Hacer backup del main.py actual")
        print("   3. Reemplazar main.py con la nueva versión")
        print("   4. Reiniciar el servicio backend")
        print("   5. Ejecutar este script nuevamente para verificar")
    
    print("\n" + "="*60)
    print("🏁 PRUEBAS COMPLETADAS")
    print("="*60)

if __name__ == "__main__":
    main()
