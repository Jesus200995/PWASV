#!/usr/bin/env python3
"""
Script de prueba para el endpoint de estadísticas de notificaciones
"""

import requests
import json

# Configuración
API_URL = "http://167.99.236.52:8000"  # URL de producción

def test_estadisticas_notificacion():
    """Probar endpoint de estadísticas de notificación"""
    
    print("🔍 Probando endpoint de estadísticas de notificación...")
    
    # Obtener primero una lista de notificaciones
    try:
        print("\n1️⃣ Obteniendo lista de notificaciones...")
        response = requests.get(f"{API_URL}/notificaciones", params={"limit": 5})
        
        if response.status_code != 200:
            print(f"❌ Error obteniendo notificaciones: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return
        
        data = response.json()
        notificaciones = data.get('notificaciones', [])
        
        if not notificaciones:
            print("⚠️ No hay notificaciones disponibles para probar")
            return
        
        # Tomar la primera notificación
        notificacion_id = notificaciones[0]['id']
        titulo = notificaciones[0]['titulo']
        
        print(f"✅ Notificaciones obtenidas: {len(notificaciones)}")
        print(f"🎯 Probando con notificación ID: {notificacion_id} - '{titulo}'")
        
    except Exception as e:
        print(f"❌ Error obteniendo notificaciones: {e}")
        return
    
    # Probar endpoint de estadísticas
    try:
        print(f"\n2️⃣ Obteniendo estadísticas para notificación {notificacion_id}...")
        
        response = requests.get(f"{API_URL}/notificaciones/{notificacion_id}/estadisticas")
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Estadísticas obtenidas exitosamente:")
            print(f"   📊 Total usuarios objetivo: {data['resumen']['total_usuarios_objetivo']}")
            print(f"   ✅ Usuarios que leyeron: {data['resumen']['usuarios_leido']}")
            print(f"   ⏳ Usuarios que no leyeron: {data['resumen']['usuarios_no_leido']}")
            print(f"   📈 Porcentaje leído: {data['resumen']['porcentaje_leido']}%")
            
            print(f"\n📋 Detalles:")
            print(f"   👤 Usuarios que leyeron (muestra): {len(data['usuarios_que_leyeron'])}")
            print(f"   ❌ Usuarios que no leyeron (muestra): {len(data['usuarios_que_no_leyeron'])}")
            
            return True
            
        elif response.status_code == 404:
            print(f"❌ Notificación no encontrada: {notificacion_id}")
            
        elif response.status_code == 500:
            print(f"❌ Error del servidor: {response.text}")
            
        else:
            print(f"❌ Error inesperado: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
        return False
        
    except Exception as e:
        print(f"❌ Error probando estadísticas: {e}")
        return False

if __name__ == "__main__":
    test_estadisticas_notificacion()
