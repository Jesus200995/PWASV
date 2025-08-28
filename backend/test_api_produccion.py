#!/usr/bin/env python3
"""
Script de prueba simplificado para verificar conectividad con la API de producción
"""

import requests
import json

# URL de la API de producción
API_URL = "https://apipwa.sembrandodatos.com"

def test_api_connection():
    """Probar conexión básica con la API"""
    
    print("🔍 Probando conexión con API de producción...")
    print(f"📡 URL: {API_URL}")
    
    try:
        # Probar endpoint básico
        print("\n1️⃣ Probando endpoint de salud...")
        response = requests.get(f"{API_URL}/health", timeout=10)
        
        if response.status_code == 200:
            print("✅ API responde correctamente")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"⚠️ API responde con código: {response.status_code}")
            
    except requests.exceptions.ConnectTimeout:
        print("❌ Timeout de conexión - El servidor puede estar ocupado")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión - Verificar URL o servidor")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

    # Probar endpoint de notificaciones
    try:
        print("\n2️⃣ Probando endpoint de notificaciones...")
        response = requests.get(f"{API_URL}/notificaciones", params={"limit": 1}, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Notificaciones endpoint funciona")
            print(f"   Total notificaciones: {data.get('total', 0)}")
            
            if data.get('notificaciones') and len(data['notificaciones']) > 0:
                notif_id = data['notificaciones'][0]['id']
                print(f"   Primera notificación ID: {notif_id}")
                
                # Probar endpoint de estadísticas
                print(f"\n3️⃣ Probando estadísticas para notificación {notif_id}...")
                stats_response = requests.get(f"{API_URL}/notificaciones/{notif_id}/estadisticas", timeout=10)
                
                if stats_response.status_code == 200:
                    stats_data = stats_response.json()
                    print("✅ Endpoint de estadísticas funciona perfectamente!")
                    print(f"   Total usuarios: {stats_data.get('resumen', {}).get('total_usuarios_objetivo', 'N/A')}")
                    print(f"   Usuarios leído: {stats_data.get('resumen', {}).get('usuarios_leido', 'N/A')}")
                else:
                    print(f"❌ Error en estadísticas: {stats_response.status_code}")
                    print(f"   Respuesta: {stats_response.text}")
            else:
                print("⚠️ No hay notificaciones para probar estadísticas")
                
        else:
            print(f"❌ Error en notificaciones: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error probando notificaciones: {e}")

if __name__ == "__main__":
    test_api_connection()
