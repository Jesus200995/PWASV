#!/usr/bin/env python3
"""
Script de prueba para notificaciones push
"""

import requests
import json
from pywebpush import webpush, WebPushException
import sqlite3
import time

# Configuración
BACKEND_URL = "http://localhost:8000"
TEST_USER_ID = 1  # Cambia esto por un usuario válido

def test_endpoints():
    """Prueba los endpoints de notificaciones push"""
    print("🔍 Probando endpoints de notificaciones push...")
    
    # 1. Probar endpoint de clave VAPID
    try:
        response = requests.get(f"{BACKEND_URL}/api/vapid-public-key")
        if response.status_code == 200:
            vapid_key = response.json()["publicKey"]
            print(f"✅ Clave VAPID obtenida: {vapid_key[:20]}...")
        else:
            print(f"❌ Error obteniendo clave VAPID: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    # 2. Simular suscripción de prueba
    test_subscription = {
        "endpoint": "https://fcm.googleapis.com/fcm/send/test-endpoint-123",
        "keys": {
            "p256dh": "BL7ELmBz1Y5-test-p256dh-key-content",
            "auth": "test-auth-key-content"
        }
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/push/subscribe",
            json={"subscription": test_subscription, "user_id": TEST_USER_ID}
        )
        print(f"🔔 Respuesta de suscripción: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error en suscripción: {e}")
    
    return True

def check_database():
    """Verifica el estado de la base de datos"""
    print("\n📊 Verificando base de datos...")
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('../sembrando_vida_asistencias.db')
        cursor = conn.cursor()
        
        # Verificar tabla de suscripciones push
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='push_subscriptions'
        """)
        
        if cursor.fetchone():
            print("✅ Tabla push_subscriptions existe")
            
            # Contar suscripciones
            cursor.execute("SELECT COUNT(*) FROM push_subscriptions")
            count = cursor.fetchone()[0]
            print(f"📊 Suscripciones registradas: {count}")
            
            if count > 0:
                cursor.execute("SELECT user_id, created_at FROM push_subscriptions LIMIT 5")
                subs = cursor.fetchall()
                print("🔍 Primeras 5 suscripciones:")
                for sub in subs:
                    print(f"   Usuario: {sub[0]}, Creado: {sub[1]}")
        else:
            print("❌ Tabla push_subscriptions no existe")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")

def simulate_notification():
    """Simula el envío de una notificación"""
    print("\n📢 Simulando envío de notificación...")
    
    # Crear una notificación de prueba
    notification_data = {
        "usuario_id": TEST_USER_ID,
        "tipo": "info",
        "titulo": "🧪 Prueba de Push",
        "mensaje": "Esta es una notificación de prueba del sistema push",
        "datos_adicionales": {
            "test": True,
            "timestamp": int(time.time())
        }
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/notificaciones",
            json=notification_data
        )
        print(f"📬 Respuesta de notificación: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Notificación creada con ID: {result.get('id', 'N/A')}")
            
            # Si la notificación incluye push, debería enviarse automáticamente
            if "push_sent" in result:
                print(f"🚀 Push enviado: {result['push_sent']}")
                
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error enviando notificación: {e}")

def check_service_worker():
    """Verifica que el service worker esté funcionando"""
    print("\n🔧 Información sobre Service Worker:")
    print("1. Asegúrate de que el navegador esté abierto en http://localhost:3002")
    print("2. Abre las Herramientas de Desarrollador (F12)")
    print("3. Ve a la pestaña 'Application' o 'Aplicación'")
    print("4. En el menú izquierdo, busca 'Service Workers'")
    print("5. Deberías ver el service worker registrado y activo")
    print("6. Para probar notificaciones, ve a la sección de notificaciones en la app")

def main():
    """Función principal"""
    print("🚀 Test de Sistema de Notificaciones Push")
    print("=" * 50)
    
    # 1. Probar endpoints
    if not test_endpoints():
        print("❌ Error en endpoints básicos")
        return
    
    # 2. Verificar base de datos
    check_database()
    
    # 3. Simular notificación
    simulate_notification()
    
    # 4. Información sobre service worker
    check_service_worker()
    
    print("\n" + "=" * 50)
    print("✅ Test completado!")
    print("\n📋 Próximos pasos:")
    print("1. Abre http://localhost:3002 en tu navegador")
    print("2. Habilita las notificaciones cuando se solicite")
    print("3. Verifica que aparezca el toggle de notificaciones")
    print("4. El sistema debería funcionar automáticamente")

if __name__ == "__main__":
    main()
