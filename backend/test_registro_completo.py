#!/usr/bin/env python3
"""
Script para probar específicamente la creación de usuarios
y el registro automático de términos
"""

import requests
import json
import hashlib
import time

# URL de la API
API_URL = "https://apipwa.sembrandodatos.com"

def crear_usuario_prueba_terminos():
    """Crear un usuario de prueba y verificar que se registren los términos automáticamente"""
    
    # Generar datos únicos para el usuario
    timestamp = str(int(time.time()))
    unique_id = hashlib.md5(timestamp.encode()).hexdigest()[:8]
    
    test_user = {
        "correo": f"test_terminos_{unique_id}@example.com",
        "nombre_completo": f"Usuario Términos {unique_id}",
        "cargo": "Técnico de Prueba",
        "supervisor": "Supervisor Prueba",
        "contrasena": "test123456",
        "curp": f"TEST{unique_id.upper()}1234AB"[:18].ljust(18, '0')
    }
    
    print(f"🧪 Creando usuario de prueba: {test_user['correo']}")
    print(f"📋 CURP: {test_user['curp']}")
    
    try:
        # Crear usuario
        response = requests.post(f"{API_URL}/usuarios", json=test_user, timeout=15)
        
        if response.status_code == 200 or response.status_code == 201:
            user_data = response.json()
            user_id = user_data.get('id')
            print(f"✅ Usuario creado exitosamente (ID: {user_id})")
            
            # Verificar que se registraron los términos automáticamente
            time.sleep(1)  # Esperar un momento
            
            try:
                terms_response = requests.get(f"{API_URL}/usuarios/{user_id}/terminos", timeout=10)
                
                if terms_response.status_code == 200:
                    terms_data = terms_response.json()
                    print(f"✅ Verificación de términos exitosa:")
                    print(f"  - Ha aceptado términos: {terms_data.get('ha_aceptado_terminos')}")
                    print(f"  - Fecha de aceptación: {terms_data.get('fecha_aceptacion')}")
                    
                    if terms_data.get('ha_aceptado_terminos'):
                        print("🎉 ¡ÉXITO! Los términos se registraron automáticamente")
                        return True
                    else:
                        print("❌ Los términos NO se registraron automáticamente")
                        return False
                        
                else:
                    print(f"⚠️  No se pudo verificar términos: {terms_response.status_code}")
                    print(f"    Respuesta: {terms_response.text}")
                    return False
                    
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Error verificando términos: {e}")
                return False
                
        else:
            print(f"❌ Error creando usuario: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en petición: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 PRUEBA COMPLETA - REGISTRO AUTOMÁTICO DE TÉRMINOS")
    print("=" * 65)
    
    print(f"\n🌐 Probando con API: {API_URL}")
    
    # Probar creación de usuario con registro automático de términos
    exito = crear_usuario_prueba_terminos()
    
    print("\n" + "=" * 65)
    
    if exito:
        print("✅ PRUEBA EXITOSA")
        print("\n🔧 RESUMEN:")
        print("- ✅ API de producción conecta correctamente")
        print("- ✅ Usuario se crea sin problemas")
        print("- ✅ Términos se registran automáticamente")
        print("- ✅ Sistema completo funcionando")
    else:
        print("❌ PRUEBA FALLIDA")
        print("\n🔧 POSIBLES CAUSAS:")
        print("- Backend en producción no tiene los cambios")
        print("- Error en la estructura de la base de datos")
        print("- Problema de conectividad")

if __name__ == "__main__":
    main()
