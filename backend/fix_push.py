#!/usr/bin/env python3
"""
Verificar y reparar suscripciones push en la base de datos
"""

import requests
import json
import os
from dotenv import load_dotenv

def check_push_subscriptions_via_api():
    """Revisar suscripciones a través de la API"""
    print("🔍 REVISANDO SUSCRIPCIONES VÍA API")
    print("-" * 50)
    
    backend_url = "http://localhost:8000"
    
    try:
        response = requests.get(f"{backend_url}/api/push/subscriptions", timeout=5)
        if response.status_code == 200:
            data = response.json()
            subscriptions = data.get('subscriptions', [])
            
            print(f"Total suscripciones: {len(subscriptions)}")
            
            valid_count = 0
            invalid_count = 0
            
            for sub in subscriptions:
                sub_id = sub.get('id')
                user_id = sub.get('usuario_id')
                is_active = sub.get('is_active')
                endpoint = sub.get('endpoint', '')
                
                # Verificar si el endpoint es válido
                if endpoint and len(endpoint) > 50 and endpoint.startswith('https://'):
                    valid_count += 1
                    status = "✅ VÁLIDA"
                else:
                    invalid_count += 1
                    status = "❌ INVÁLIDA"
                
                print(f"ID:{sub_id:2d} User:{user_id:4d} Active:{is_active} {status}")
                if not endpoint or len(endpoint) < 50:
                    print(f"    📄 Endpoint problemático: '{endpoint}'")
                
            print(f"\nResumen:")
            print(f"✅ Suscripciones válidas: {valid_count}")
            print(f"❌ Suscripciones inválidas: {invalid_count}")
            
            return valid_count > 0
        else:
            print(f"❌ Error API: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_real_push_to_valid_subscriptions():
    """Enviar push solo a suscripciones válidas"""
    print(f"\n🚀 ENVIANDO PUSH A SUSCRIPCIONES VÁLIDAS")
    print("-" * 50)
    
    backend_url = "http://localhost:8000"
    
    # Obtener usuarios con suscripciones potencialmente válidas
    real_users = [815, 2902, 2050, 264, 2357, 708, 2261, 2513, 2794, 3484]
    
    for user_id in real_users[:5]:  # Probar los primeros 5
        print(f"\n👤 Probando usuario {user_id}...")
        
        try:
            response = requests.post(f"{backend_url}/api/push/test/{user_id}", timeout=10)
            if response.status_code == 200:
                result = response.json()
                devices = result.get('dispositivos', 0)
                success = result.get('success', False)
                
                if devices > 0:
                    print(f"   ✅ Push enviado a {devices} dispositivos")
                else:
                    print(f"   ❌ Push no enviado (sin dispositivos válidos)")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def create_notification_for_real_users():
    """Crear notificación para usuarios reales"""
    print(f"\n📝 CREANDO NOTIFICACIÓN PARA USUARIOS REALES")
    print("-" * 50)
    
    backend_url = "http://localhost:8000"
    
    # Usuarios que sabemos que tienen suscripciones
    test_users = [815, 2902, 2050]  # Primeros 3 usuarios con suscripciones activas
    
    for user_id in test_users:
        notification_data = {
            "usuario_id": user_id,
            "tipo": "test_urgente",
            "titulo": "🆘 Test Push Crítico",
            "mensaje": f"USUARIO {user_id}: Esta es una prueba crítica para verificar que las notificaciones push lleguen correctamente. Si ves esta notificación, ¡el sistema funciona!",
            "datos_adicionales": {
                "critical_test": True,
                "priority": "high",
                "timestamp": "2025-08-27T22:45:00",
                "action_url": "/notificaciones"
            }
        }
        
        try:
            print(f"📤 Enviando a usuario {user_id}...")
            response = requests.post(
                f"{backend_url}/api/notifications/create",
                json=notification_data,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                notification_id = result.get('id')
                push_sent = result.get('push_sent', False)
                push_count = result.get('push_count', 0)
                
                print(f"   ✅ Notificación {notification_id} creada")
                print(f"   📱 Push enviado: {push_sent}")
                print(f"   📊 Dispositivos: {push_count}")
                
                if push_sent and push_count > 0:
                    print(f"   🎉 ¡ÉXITO! Push enviado correctamente")
                else:
                    print(f"   ⚠️ Push no enviado o sin dispositivos")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def fix_database_endpoints():
    """Intentar limpiar endpoints corruptos"""
    print(f"\n🔧 LIMPIEZA DE BASE DE DATOS")
    print("-" * 50)
    
    backend_url = "http://localhost:8000"
    
    print("Esta función requiere acceso directo a la base de datos.")
    print("Por ahora, se recomienda:")
    print("1. Limpiar suscripciones con endpoints vacíos o corruptos")
    print("2. Forzar re-suscripción de usuarios")
    print("3. Verificar que PWA Super esté generando endpoints válidos")

def main():
    print("🔧 REPARADOR DE PUSH NOTIFICATIONS")
    print("=" * 50)
    
    # 1. Revisar estado actual
    has_valid = check_push_subscriptions_via_api()
    
    if not has_valid:
        print(f"\n❌ NO HAY SUSCRIPCIONES VÁLIDAS")
        print(f"💡 SOLUCIÓN: Los usuarios deben abrir PWA Super y re-habilitar notificaciones")
        return
    
    # 2. Test push directo
    test_real_push_to_valid_subscriptions()
    
    # 3. Test con notificaciones reales
    print(f"\n" + "=" * 50)
    response = input("¿Enviar notificación crítica a usuarios reales? (s/n): ").lower()
    if response in ['s', 'y', 'si', 'yes']:
        create_notification_for_real_users()
    
    # 4. Recomendaciones
    print(f"\n" + "=" * 50)
    print(f"📋 RECOMENDACIONES CRÍTICAS:")
    print(f"=" * 50)
    
    print(f"❌ PROBLEMA PRINCIPAL: Endpoints de suscripción corruptos")
    print(f"🔧 SOLUCIÓN INMEDIATA:")
    print(f"   1. Los usuarios deben abrir PWA Super")
    print(f"   2. Limpiar caché y datos del navegador") 
    print(f"   3. Re-habilitar notificaciones push")
    print(f"   4. Esto generará endpoints válidos nuevos")
    
    print(f"\n🛠️ SOLUCIÓN TÉCNICA:")
    print(f"   1. Limpiar tabla push_subscriptions de endpoints vacíos")
    print(f"   2. Verificar que PWA Super genere endpoints HTTPS válidos")
    print(f"   3. Verificar que las claves VAPID sean correctas")
    
    print(f"\n📱 INSTRUCCIONES PARA USUARIOS:")
    print(f"   1. Abrir PWA Super en el navegador")
    print(f"   2. Ir a Configuración")
    print(f"   3. Habilitar notificaciones push")
    print(f"   4. Aceptar permisos del navegador")
    print(f"   5. Esto regenerará la suscripción correctamente")

if __name__ == "__main__":
    main()
