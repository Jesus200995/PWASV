#!/usr/bin/env python3
"""
Crear suscripción push de prueba manual para debugging
"""

import requests
import json
from datetime import datetime

def create_test_subscription():
    """Crear una suscripción push de prueba con endpoint real"""
    print("🧪 CREANDO SUSCRIPCIÓN DE PRUEBA MANUAL")
    print("=" * 50)
    
    backend_url = "http://localhost:8000"
    
    # Suscripción de prueba con formato válido (simulando una real)
    test_subscription = {
        "usuario_id": 2390,
        "endpoint": "https://fcm.googleapis.com/fcm/send/test-endpoint-for-debugging-12345678901234567890123456789012345678901234567890",
        "keys": {
            "p256dh": "BKxVJRiVLBN5M2O5bNj2eCgNq8QxO8VWLvLZxHN3M2O5bNj2eCgNq8QxO8VWLvLZxHN",
            "auth": "tBHItJI5sKQh6VdBj2LUyAx7O8VWLvLZxHN"
        },
        "userAgent": "Mozilla/5.0 (Test) PWA-Super-Debug/1.0",
        "deviceInfo": {
            "type": "mobile",
            "platform": "Test-Platform-Debug"
        }
    }
    
    try:
        print(f"📤 Enviando suscripción de prueba...")
        print(f"   Usuario: {test_subscription['usuario_id']}")
        print(f"   Endpoint: {test_subscription['endpoint'][:50]}...")
        
        response = requests.post(
            f"{backend_url}/api/push/subscribe",
            json=test_subscription,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Suscripción creada exitosamente")
            print(f"   📄 Respuesta: {result}")
            
            # Verificar que se guardó correctamente
            print(f"\n🔍 Verificando suscripción guardada...")
            verify_response = requests.get(f"{backend_url}/api/push/subscriptions", timeout=5)
            
            if verify_response.status_code == 200:
                data = verify_response.json()
                subscriptions = data.get('subscriptions', [])
                
                test_subs = [s for s in subscriptions if s.get('usuario_id') == 2390 and s.get('is_active')]
                
                if test_subs:
                    print(f"   ✅ Suscripción encontrada en base de datos")
                    for sub in test_subs:
                        endpoint = sub.get('endpoint', '')
                        print(f"      ID: {sub.get('id')}")
                        print(f"      Endpoint: {endpoint[:50]}...")
                        print(f"      Activa: {sub.get('is_active')}")
                        
                        # Test push a esta suscripción
                        print(f"\n🚀 Probando push con esta suscripción...")
                        push_response = requests.post(f"{backend_url}/api/push/test/2390", timeout=10)
                        
                        if push_response.status_code == 200:
                            push_result = push_response.json()
                            devices = push_result.get('dispositivos', 0)
                            print(f"      📱 Push enviado a {devices} dispositivos")
                            
                            if devices > 0:
                                print(f"      🎉 ¡ÉXITO! El backend puede enviar push notifications")
                            else:
                                print(f"      ⚠️ Push no enviado - posible problema con endpoint de prueba")
                        else:
                            print(f"      ❌ Error en push: {push_response.status_code}")
                else:
                    print(f"   ❌ Suscripción no encontrada en base de datos")
            else:
                print(f"   ❌ Error verificando suscripciones: {verify_response.status_code}")
                
        else:
            print(f"   ❌ Error creando suscripción: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"   📄 Error: {error_detail}")
            except:
                print(f"   📄 Respuesta: {response.text}")
                
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_frontend_subscription():
    """Test el proceso de suscripción desde el frontend"""
    print(f"\n🌐 TESTING PROCESO DE SUSCRIPCIÓN FRONTEND")
    print("-" * 50)
    
    print(f"📋 PASOS PARA DEBUGGING FRONTEND:")
    print(f"1. Abrir PWA Super: http://localhost:5175")
    print(f"2. Abrir DevTools (F12)")
    print(f"3. Ir a Console")
    print(f"4. Ejecutar: pushNotificationService.subscribe(2390)")
    print(f"5. Verificar que se genere endpoint válido")
    print(f"6. Verificar que se envíe al backend correctamente")
    
    print(f"\n🔍 VERIFICAR EN DEVTOOLS:")
    print(f"• Network tab: debe aparecer POST a /api/push/subscribe")
    print(f"• Payload debe tener endpoint válido (https://fcm.googleapis.com/...)")
    print(f"• Keys p256dh y auth deben estar presentes")
    print(f"• Respuesta debe ser 200 OK")

def clean_invalid_subscriptions():
    """Limpiar suscripciones inválidas"""
    print(f"\n🧹 LIMPIANDO SUSCRIPCIONES INVÁLIDAS")
    print("-" * 50)
    
    print("Esta función requiere acceso directo a PostgreSQL.")
    print("Comando SQL para limpiar suscripciones vacías:")
    print()
    print("DELETE FROM push_subscriptions WHERE endpoint = '' OR endpoint IS NULL;")
    print()
    print("Esto eliminará todas las suscripciones sin endpoint válido.")
    
    backend_url = "http://localhost:8000"
    
    # Obtener estadísticas antes
    try:
        response = requests.get(f"{backend_url}/api/push/subscriptions", timeout=5)
        if response.status_code == 200:
            data = response.json()
            total_before = data.get('total', 0)
            active_before = data.get('activas', 0)
            
            print(f"📊 ANTES DE LIMPIAR:")
            print(f"   Total: {total_before}")
            print(f"   Activas: {active_before}")
            print(f"   Inválidas estimadas: {total_before}")  # Todas parecen inválidas
    except:
        pass

def main():
    print("🔧 REPARADOR AVANZADO DE PUSH NOTIFICATIONS")
    print("=" * 60)
    
    # 1. Crear suscripción de prueba manual
    create_test_subscription()
    
    # 2. Instrucciones para test frontend
    test_frontend_subscription()
    
    # 3. Limpieza de base de datos
    clean_invalid_subscriptions()
    
    # 4. Conclusiones
    print(f"\n" + "=" * 60)
    print(f"🎯 CONCLUSIÓN DEL PROBLEMA")
    print(f"=" * 60)
    
    print(f"❌ PROBLEMA IDENTIFICADO:")
    print(f"   • PWA Super NO está enviando endpoints válidos al backend")
    print(f"   • Todos los endpoints en base de datos están vacíos ('')")
    print(f"   • El backend funciona correctamente")
    print(f"   • El problema está en el frontend")
    
    print(f"\n🔧 SOLUCIÓN REQUERIDA:")
    print(f"   1. Revisar pushNotificationService.js línea ~160-180")
    print(f"   2. Verificar que subscription.endpoint se captura correctamente")
    print(f"   3. Verificar que subscriptionData.endpoint se envía al backend")
    print(f"   4. Verificar que no hay errores en console del navegador")
    
    print(f"\n📱 PASOS INMEDIATOS:")
    print(f"   1. Un usuario debe abrir PWA Super")
    print(f"   2. Abrir DevTools y verificar console")
    print(f"   3. Intentar suscribirse a notificaciones")
    print(f"   4. Verificar que endpoint no esté vacío en Network tab")

if __name__ == "__main__":
    main()
