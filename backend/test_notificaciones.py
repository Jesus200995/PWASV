#!/usr/bin/env python3
"""
Script de prueba para el sistema de notificaciones
Prueba todos los endpoints y funcionalidades del sistema
"""

import requests
import json
from datetime import datetime, timedelta
import time

# Configuración del servidor
BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, expected_status=200):
    """Función auxiliar para probar endpoints"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        print(f"🔗 {method} {endpoint}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == expected_status:
            print("   ✅ SUCCESS")
            if response.content:
                try:
                    result = response.json()
                    print(f"   📝 Response: {json.dumps(result, indent=2, default=str)[:200]}...")
                    return result
                except:
                    print(f"   📝 Response: {response.text[:100]}...")
                    return response.text
        else:
            print(f"   ❌ FAILED - Expected {expected_status}, got {response.status_code}")
            print(f"   📝 Response: {response.text}")
            return None
    
    except Exception as e:
        print(f"   💥 ERROR: {e}")
        return None

def main():
    """Ejecutar todas las pruebas"""
    print("🚀 Iniciando pruebas del sistema de notificaciones")
    print("=" * 60)
    
    # 1. Probar estadísticas iniciales
    print("\n📊 1. PROBANDO ESTADÍSTICAS INICIALES")
    stats = test_endpoint("GET", "/notifications/stats")
    
    # 2. Listar notificaciones (debería estar vacío inicialmente)
    print("\n📋 2. LISTANDO NOTIFICACIONES")
    notifications = test_endpoint("GET", "/notifications")
    
    # 3. Crear notificación para todos los usuarios
    print("\n📝 3. CREANDO NOTIFICACIÓN GLOBAL")
    notification_data = {
        "title": "Notificación de Prueba Global",
        "body": "Esta es una notificación de prueba para todos los usuarios del sistema",
        "type": "info",
        "audience": "all",
        "metadata": {
            "priority": "normal",
            "category": "test"
        },
        "status": "draft"
    }
    
    created_notification = test_endpoint("POST", "/notifications", notification_data, 200)
    global_notification_id = created_notification.get("id") if created_notification else None
    
    # 4. Crear notificación para usuarios específicos
    print("\n👥 4. CREANDO NOTIFICACIÓN PARA USUARIOS ESPECÍFICOS")
    user_notification_data = {
        "title": "Notificación Personalizada",
        "body": "Esta notificación es solo para usuarios específicos",
        "type": "warning",
        "audience": "users",
        "user_ids": [1, 2],  # IDs de usuarios específicos
        "status": "draft"
    }
    
    created_user_notification = test_endpoint("POST", "/notifications", user_notification_data, 200)
    user_notification_id = created_user_notification.get("id") if created_user_notification else None
    
    # 5. Obtener detalles de notificación específica
    if global_notification_id:
        print(f"\n🔍 5. OBTENIENDO DETALLES DE NOTIFICACIÓN {global_notification_id}")
        test_endpoint("GET", f"/notifications/{global_notification_id}")
    
    # 6. Listar notificaciones con filtros
    print("\n🔍 6. LISTANDO NOTIFICACIONES CON FILTROS")
    test_endpoint("GET", "/notifications?status=draft&limit=10")
    
    # 7. Probar suscripción de dispositivo
    print("\n📱 7. PROBANDO SUSCRIPCIÓN DE DISPOSITIVO")
    subscription_data = {
        "user_id": 1,
        "endpoint": "https://fcm.googleapis.com/fcm/send/test-endpoint-123",
        "p256dh": "test-p256dh-key",
        "auth": "test-auth-key",
        "user_agent": "Mozilla/5.0 (Test Browser)"
    }
    
    test_endpoint("POST", "/push/subscribe", subscription_data, 200)
    
    # 8. Probar notificación de prueba
    print("\n🧪 8. ENVIANDO NOTIFICACIÓN DE PRUEBA")
    test_endpoint("GET", "/push/test/1", expected_status=200)
    
    # 9. Marcar notificación como leída
    if global_notification_id:
        print(f"\n📖 9. MARCANDO NOTIFICACIÓN {global_notification_id} COMO LEÍDA")
        test_endpoint("POST", f"/notifications/{global_notification_id}/read?user_id=1", expected_status=200)
    
    # 10. Enviar notificación programada
    if user_notification_id:
        print(f"\n📤 10. ENVIANDO NOTIFICACIÓN {user_notification_id}")
        test_endpoint("POST", f"/notifications/{user_notification_id}/send", expected_status=200)
    
    # 11. Estadísticas finales
    print("\n📊 11. ESTADÍSTICAS FINALES")
    test_endpoint("GET", "/notifications/stats")
    
    # 12. Desuscribir dispositivo
    print("\n📱 12. DESUSCRIBIENDO DISPOSITIVO")
    test_endpoint("POST", "/push/unsubscribe", {"endpoint": "https://fcm.googleapis.com/fcm/send/test-endpoint-123"}, 200)
    
    # 13. Eliminar notificación (opcional)
    if global_notification_id:
        print(f"\n🗑️ 13. ELIMINANDO NOTIFICACIÓN {global_notification_id}")
        test_endpoint("DELETE", f"/notifications/{global_notification_id}", expected_status=200)
    
    print("\n" + "=" * 60)
    print("✅ PRUEBAS COMPLETADAS")
    print("💡 Revisa los logs del servidor para más detalles")

if __name__ == "__main__":
    print("⏳ Esperando 2 segundos para que el servidor esté listo...")
    time.sleep(2)
    main()
