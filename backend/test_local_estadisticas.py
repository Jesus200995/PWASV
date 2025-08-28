#!/usr/bin/env python3
"""
Script de prueba para el endpoint local de estadísticas
"""

import requests
import json

# URL del backend local
API_URL = "http://localhost:8000"

def test_local_estadisticas():
    """Probar endpoint de estadísticas localmente"""
    
    print("🔍 Probando endpoint local de estadísticas...")
    print(f"📡 URL: {API_URL}")
    
    try:
        # Obtener notificaciones
        print("\n1️⃣ Obteniendo notificaciones locales...")
        response = requests.get(f"{API_URL}/notificaciones", params={"limit": 5})
        
        if response.status_code != 200:
            print(f"❌ Error obteniendo notificaciones: {response.status_code}")
            return
        
        data = response.json()
        notificaciones = data.get('notificaciones', [])
        
        if not notificaciones:
            print("⚠️ No hay notificaciones locales")
            # Crear una notificación de prueba
            print("📝 Creando notificación de prueba...")
            create_data = {
                'titulo': 'Notificación de Prueba',
                'subtitulo': 'Prueba para estadísticas',
                'descripcion': 'Esta es una notificación para probar las estadísticas',
                'enviada_a_todos': True
            }
            
            create_response = requests.post(f"{API_URL}/notificaciones", data=create_data)
            if create_response.status_code == 200:
                print("✅ Notificación de prueba creada")
                # Volver a obtener notificaciones
                response = requests.get(f"{API_URL}/notificaciones", params={"limit": 5})
                data = response.json()
                notificaciones = data.get('notificaciones', [])
            else:
                print(f"❌ Error creando notificación: {create_response.status_code}")
                return
        
        # Probar estadísticas con la primera notificación
        notificacion_id = notificaciones[0]['id']
        titulo = notificaciones[0]['titulo']
        
        print(f"🎯 Probando estadísticas con notificación ID: {notificacion_id}")
        print(f"   Título: {titulo}")
        
        # Probar endpoint de estadísticas
        print(f"\n2️⃣ Obteniendo estadísticas...")
        
        response = requests.get(f"{API_URL}/notificaciones/{notificacion_id}/estadisticas")
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ ¡Estadísticas obtenidas exitosamente!")
            print(f"   📊 Total usuarios objetivo: {stats['resumen']['total_usuarios_objetivo']}")
            print(f"   ✅ Usuarios que leyeron: {stats['resumen']['usuarios_leido']}")
            print(f"   ⏳ Usuarios que no leyeron: {stats['resumen']['usuarios_no_leido']}")
            print(f"   📈 Porcentaje leído: {stats['resumen']['porcentaje_leido']}%")
            print("\n🎉 ¡El endpoint de estadísticas funciona perfectamente!")
            return True
        else:
            print(f"❌ Error en estadísticas: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_local_estadisticas()
