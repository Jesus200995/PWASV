#!/usr/bin/env python3
"""
Script para actualizar automáticamente los supervisores de TODOS los técnicos.
Llama al endpoint /actualizar-supervisores-tecnicos del backend.
"""

import requests
import json

# URL del backend (ajustar según entorno)
BACKEND_URL = "https://apipwa.sembrandodatos.com"  # Producción VPS con HTTPS
# BACKEND_URL = "http://31.97.8.51:8080"  # VPS IP directa
# BACKEND_URL = "http://localhost:8000"  # Local

def actualizar_supervisores():
    """Actualiza supervisores de todos los técnicos en la base de datos"""
    
    print("=" * 70)
    print("🔄 ACTUALIZACIÓN MASIVA DE SUPERVISORES TÉCNICOS")
    print("=" * 70)
    print()
    
    try:
        url = f"{BACKEND_URL}/actualizar-supervisores-tecnicos"
        print(f"📡 Llamando a: {url}")
        print()
        
        response = requests.post(url, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ ACTUALIZACIÓN COMPLETADA EXITOSAMENTE")
            print("=" * 70)
            print(f"📊 Total de técnicos encontrados: {data.get('total_tecnicos', 0)}")
            print(f"✅ Actualizados correctamente: {data.get('actualizados', 0)}")
            print(f"⚠️  Sin supervisor territorial: {data.get('sin_supervisor', 0)}")
            print(f"❌ Errores: {len(data.get('errores', []))}")
            print()
            
            # Mostrar errores si existen
            errores = data.get('errores', [])
            if errores:
                print("DETALLES DE ERRORES:")
                print("-" * 70)
                for error in errores:
                    if 'razon' in error:
                        print(f"⚠️  {error.get('nombre', 'N/A')} ({error.get('territorio', 'N/A')})")
                        print(f"   Razón: {error.get('razon')}")
                    else:
                        print(f"❌ {error.get('nombre', 'N/A')}: {error.get('error', 'Error desconocido')}")
                    print()
            
            print("=" * 70)
            print(f"💬 {data.get('mensaje', 'Proceso completado')}")
            print("=" * 70)
            
        else:
            print(f"❌ Error HTTP {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al backend")
        print(f"   Verifica que el servidor esté corriendo en {BACKEND_URL}")
    except requests.exceptions.Timeout:
        print("❌ Error: Timeout en la solicitud (más de 60 segundos)")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    actualizar_supervisores()
