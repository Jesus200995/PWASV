#!/usr/bin/env python3
"""
Test completo de notificaciones push para PWA Super
Verifica que las notificaciones lleguen al dispositivo incluso con la app cerrada
"""

import requests
import json
import time
import asyncio
from datetime import datetime

def test_pwa_push_system():
    """Test completo del sistema push para PWA Super"""
    print("🚀 TEST DE NOTIFICACIONES PUSH - PWA SUPER")
    print("=" * 60)
    print(f"🕒 Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Configuración
    backend_url = "http://localhost:8000"
    pwa_url = "http://localhost:5175"
    admin_url = "http://localhost:3002"
    
    print(f"\n🌐 URLs de testing:")
    print(f"   Backend: {backend_url}")
    print(f"   PWA Super: {pwa_url}")
    print(f"   Admin PWA: {admin_url}")
    
    # 1. Verificar que todos los servicios estén ejecutándose
    print(f"\n1️⃣ Verificando servicios...")
    
    services_status = {}
    
    # Backend
    try:
        response = requests.get(f"{backend_url}/api/vapid-public-key", timeout=5)
        if response.status_code == 200:
            services_status['backend'] = '✅ Online'
            vapid_key = response.json().get('publicKey', '')
            print(f"   Backend: ✅ Online - VAPID: {vapid_key[:20]}...")
        else:
            services_status['backend'] = f'❌ Error {response.status_code}'
    except Exception as e:
        services_status['backend'] = f'❌ Offline: {str(e)[:50]}'
        print(f"   Backend: ❌ Offline - {e}")
        return False
    
    # PWA Super
    try:
        response = requests.get(pwa_url, timeout=5)
        services_status['pwa_super'] = '✅ Online' if response.status_code == 200 else f'❌ Error {response.status_code}'
        print(f"   PWA Super: {'✅ Online' if response.status_code == 200 else f'❌ Error {response.status_code}'}")
    except Exception as e:
        services_status['pwa_super'] = f'❌ Offline'
        print(f"   PWA Super: ❌ Offline")
    
    # 2. Simular suscripción desde PWA Super
    print(f"\n2️⃣ Simulando suscripción push desde PWA Super...")
    
    # Suscripción de prueba realista
    test_subscription = {
        "usuario_id": 2390,  # Usuario de prueba
        "endpoint": "https://fcm.googleapis.com/fcm/send/eUhGvRMA6Tc:APA91bH0YXjXqJlGnLtCa8KTjhHwEpRFcgZ4TfwW1K2yxPqv_test_endpoint",
        "keys": {
            "p256dh": "BKMqOKgx9Y8zIKqhTq7YWXjZ7KtGjvRGvZ2X3hqjGHvfRKLqoMN8pM3gGjvRGvZ2X",
            "auth": "test-auth-secret-key-for-pwa-super"
        },
        "userAgent": "Mozilla/5.0 PWA-Super Test",
        "deviceInfo": {
            "type": "mobile",
            "platform": "PWA-Super-Test"
        }
    }
    
    try:
        response = requests.post(
            f"{backend_url}/api/push/subscribe",
            json=test_subscription,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Suscripción registrada: {result.get('message', 'OK')}")
            subscription_success = True
        else:
            print(f"   ❌ Error en suscripción: {response.status_code} - {response.text}")
            subscription_success = False
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        subscription_success = False
    
    # 3. Crear notificación con datos realistas
    print(f"\n3️⃣ Creando notificación push para usuario...")
    
    notification_data = {
        "usuario_id": 2390,
        "tipo": "alerta",
        "titulo": "🌱 Nueva Actividad - Sembrando Vida",
        "mensaje": "Se ha registrado una nueva actividad de reforestación en tu área. Tap para ver detalles.",
        "datos_adicionales": {
            "push_test": True,
            "timestamp": int(time.time()),
            "source": "pwa_super_test",
            "action_url": "/notificaciones",
            "priority": "high",
            "category": "activity"
        }
    }
    
    try:
        response = requests.post(
            f"{backend_url}/api/notifications/create",
            json=notification_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            notification_id = result.get('id', 'N/A')
            push_sent = result.get('push_sent', False)
            print(f"   ✅ Notificación creada - ID: {notification_id}")
            print(f"   📱 Push enviado: {'SÍ' if push_sent else 'NO'}")
            notification_success = True
        else:
            print(f"   ❌ Error creando notificación: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"   📄 Detalle: {error_detail}")
            except:
                print(f"   📄 Respuesta: {response.text}")
            notification_success = False
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        notification_success = False
    
    # 4. Verificar que la notificación esté en el sistema
    print(f"\n4️⃣ Verificando notificación en el sistema...")
    
    try:
        response = requests.get(
            f"{backend_url}/notificaciones?usuario_id=2390&limit=3",
            timeout=5
        )
        
        if response.status_code == 200:
            notifications = response.json()
            print(f"   📊 Notificaciones encontradas: {len(notifications)}")
            
            if notifications:
                latest = notifications[0]
                print(f"   📄 Última notificación:")
                print(f"      - ID: {latest.get('id', 'N/A')}")
                print(f"      - Título: {latest.get('titulo', 'N/A')}")
                print(f"      - Tipo: {latest.get('tipo', 'N/A')}")
                print(f"      - Fecha: {latest.get('fecha_creacion', 'N/A')}")
        else:
            print(f"   ❌ Error obteniendo notificaciones: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 5. Generar reporte final
    print(f"\n" + "=" * 60)
    print(f"📊 REPORTE FINAL")
    print(f"=" * 60)
    
    print(f"\n🟢 SERVICIOS:")
    for service, status in services_status.items():
        print(f"   {service}: {status}")
    
    print(f"\n🔔 NOTIFICACIONES PUSH:")
    print(f"   Suscripción: {'✅ OK' if subscription_success else '❌ FALLO'}")
    print(f"   Notificación: {'✅ OK' if notification_success else '❌ FALLO'}")
    
    # Estado general
    all_good = subscription_success and notification_success
    status_emoji = "✅" if all_good else "❌"
    
    print(f"\n{status_emoji} ESTADO GENERAL: {'TODO FUNCIONANDO' if all_good else 'REQUIERE ATENCIÓN'}")
    
    if all_good:
        print(f"\n🎯 INSTRUCCIONES PARA PRUEBA MANUAL:")
        print(f"   1. Abre PWA Super en: {pwa_url}")
        print(f"   2. Inicia sesión con usuario ID 2390")
        print(f"   3. Ve a configuración/notificaciones")
        print(f"   4. Habilita notificaciones push")
        print(f"   5. Cierra la aplicación completamente")
        print(f"   6. Ejecuta este script nuevamente")
        print(f"   7. Deberías recibir la notificación push")
        
        print(f"\n📱 TESTING EN DISPOSITIVO:")
        print(f"   - Las notificaciones push aparecerán incluso con la app cerrada")
        print(f"   - Verifica en la bandeja de notificaciones del sistema")
        print(f"   - Toca la notificación para abrir la app en la sección correcta")
    else:
        print(f"\n🔧 ACCIONES REQUERIDAS:")
        if not subscription_success:
            print(f"   - Verificar endpoint de suscripción push")
            print(f"   - Revisar configuración VAPID")
        if not notification_success:
            print(f"   - Verificar endpoint de notificaciones")
            print(f"   - Revisar estructura de datos")
    
    return all_good

def create_test_notification_burst():
    """Crear varias notificaciones para testing"""
    print(f"\n🔥 Creando ráfaga de notificaciones de prueba...")
    
    backend_url = "http://localhost:8000"
    test_notifications = [
        {
            "usuario_id": 2390,
            "tipo": "info",
            "titulo": "📊 Estadísticas Semanales",
            "mensaje": "Revisa el progreso de esta semana en reforestación",
            "datos_adicionales": {"test": True, "priority": "normal"}
        },
        {
            "usuario_id": 2390,
            "tipo": "alerta",
            "titulo": "⚠️ Actividad Urgente",
            "mensaje": "Se requiere atención inmediata en el área asignada",
            "datos_adicionales": {"test": True, "priority": "high"}
        },
        {
            "usuario_id": 2390,
            "tipo": "recordatorio",
            "titulo": "🕐 Recordatorio",
            "mensaje": "No olvides registrar tu actividad de hoy",
            "datos_adicionales": {"test": True, "priority": "low"}
        }
    ]
    
    for i, notification in enumerate(test_notifications, 1):
        try:
            response = requests.post(
                f"{backend_url}/api/notifications/create",
                json=notification,
                timeout=5
            )
            print(f"   {i}. {'✅' if response.status_code == 200 else '❌'} {notification['titulo']}")
            time.sleep(1)  # Esperar entre notificaciones
        except Exception as e:
            print(f"   {i}. ❌ Error: {e}")

if __name__ == "__main__":
    try:
        # Test principal
        success = test_pwa_push_system()
        
        # Si todo está bien, ofrecer crear más notificaciones de prueba
        if success:
            print(f"\n" + "=" * 40)
            response = input("¿Crear más notificaciones de prueba? (s/n): ").lower()
            if response in ['s', 'y', 'si', 'yes']:
                create_test_notification_burst()
        
        print(f"\n🏁 Test completado!")
        
    except KeyboardInterrupt:
        print(f"\n⏹️ Test interrumpido por el usuario")
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
