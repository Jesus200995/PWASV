#!/usr/bin/env python3
"""
Test completo y automatizado de push notifications
Verifica todo el flujo del sistema
"""

import requests
import json
import time
from datetime import datetime

def test_complete_push_system():
    """Test completo del sistema de push notifications"""
    print("🧪 TEST COMPLETO DE PUSH NOTIFICATIONS")
    print("=" * 60)
    
    backend_url = "http://localhost:8000"
    pwa_url = "http://localhost:5175"
    usuario_test = 2390
    
    results = {
        'backend_ok': False,
        'pwa_ok': False,
        'vapid_ok': False,
        'subscriptions_total': 0,
        'subscriptions_valid': 0,
        'push_test_ok': False,
        'notification_created': False
    }
    
    print(f"🎯 Usuario de prueba: {usuario_test}")
    print(f"🌐 Backend URL: {backend_url}")
    print(f"📱 PWA URL: {pwa_url}")
    print(f"🕒 Hora: {datetime.now().strftime('%H:%M:%S')}")
    
    # 1. Verificar Backend
    print(f"\n1️⃣ VERIFICANDO BACKEND")
    try:
        response = requests.get(f"{backend_url}/health", timeout=3)
        if response.status_code == 404:  # Endpoint no existe, probar otro
            response = requests.get(f"{backend_url}/api/vapid-public-key", timeout=3)
        
        if response.status_code == 200:
            print(f"   ✅ Backend online")
            results['backend_ok'] = True
        else:
            print(f"   ❌ Backend error: {response.status_code}")
            return results
    except Exception as e:
        print(f"   ❌ Backend offline: {e}")
        return results
    
    # 2. Verificar PWA
    print(f"\n2️⃣ VERIFICANDO PWA SUPER")
    try:
        response = requests.get(f"{pwa_url}", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ PWA Super online")
            results['pwa_ok'] = True
        else:
            print(f"   ❌ PWA error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ PWA offline: {e}")
        print(f"   💡 Ejecutar: cd pwasuper && npm run dev")
    
    # 3. Verificar VAPID
    print(f"\n3️⃣ VERIFICANDO CONFIGURACIÓN VAPID")
    try:
        response = requests.get(f"{backend_url}/api/vapid-public-key", timeout=5)
        if response.status_code == 200:
            data = response.json()
            vapid_key = data.get('publicKey', '')
            if vapid_key and len(vapid_key) > 50:
                print(f"   ✅ Clave VAPID disponible: {vapid_key[:20]}...")
                results['vapid_ok'] = True
            else:
                print(f"   ❌ Clave VAPID inválida: {vapid_key}")
        else:
            print(f"   ❌ Error obteniendo VAPID: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error VAPID: {e}")
    
    # 4. Analizar suscripciones
    print(f"\n4️⃣ ANALIZANDO SUSCRIPCIONES")
    try:
        response = requests.get(f"{backend_url}/api/push/subscriptions", timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            # Manejar diferentes formatos de respuesta
            if isinstance(data, dict) and 'subscriptions' in data:
                subscriptions = data['subscriptions']
                total = data.get('total', len(subscriptions))
                active = data.get('activas', 0)
            elif isinstance(data, list):
                subscriptions = data
                total = len(subscriptions)
                active = sum(1 for s in subscriptions if s.get('is_active', True))
            else:
                subscriptions = []
                total = 0
                active = 0
            
            results['subscriptions_total'] = total
            
            print(f"   📊 Total suscripciones: {total}")
            print(f"   ✅ Suscripciones activas: {active}")
            
            # Contar válidas
            valid_count = 0
            user_subs = 0
            
            for sub in subscriptions:
                endpoint = sub.get('endpoint', '')
                user_id = sub.get('usuario_id')
                is_active = sub.get('is_active', True)
                
                if endpoint and len(endpoint) > 50 and endpoint.startswith('https://') and is_active:
                    valid_count += 1
                
                if user_id == usuario_test and is_active:
                    user_subs += 1
                    if endpoint and len(endpoint) > 50:
                        print(f"   🎯 Usuario test tiene suscripción válida")
                    else:
                        print(f"   ⚠️ Usuario test tiene suscripción inválida")
            
            results['subscriptions_valid'] = valid_count
            print(f"   ✅ Suscripciones válidas: {valid_count}")
            
            if valid_count == 0:
                print(f"   💡 NECESARIO: Abrir PWA Super y habilitar notificaciones")
                
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 5. Test de push directo (solo si hay suscripciones válidas)
    print(f"\n5️⃣ TEST DE PUSH NOTIFICATION")
    if results['subscriptions_valid'] > 0:
        try:
            response = requests.post(f"{backend_url}/api/push/test/{usuario_test}", timeout=10)
            if response.status_code == 200:
                result = response.json()
                devices = result.get('dispositivos', 0)
                success = result.get('success', False)
                
                print(f"   📤 Push enviado: {success}")
                print(f"   📱 Dispositivos alcanzados: {devices}")
                
                if devices > 0:
                    print(f"   🎉 ¡Push notification funcionando!")
                    results['push_test_ok'] = True
                else:
                    print(f"   ⚠️ Push enviado pero sin dispositivos")
            else:
                print(f"   ❌ Error test push: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    else:
        print(f"   ⏭️ Saltando (no hay suscripciones válidas)")
    
    # 6. Test de notificación completa
    print(f"\n6️⃣ TEST DE NOTIFICACIÓN COMPLETA")
    if results['subscriptions_valid'] > 0:
        notification_data = {
            "usuario_id": usuario_test,
            "tipo": "test_completo",
            "titulo": f"🧪 Test Completo {datetime.now().strftime('%H:%M:%S')}",
            "mensaje": f"Esta es una prueba completa del sistema de push notifications. Si ves esta notificación, ¡el sistema está funcionando perfectamente! Enviada: {datetime.now().strftime('%H:%M:%S')}",
            "datos_adicionales": {
                "test_type": "complete",
                "timestamp": int(time.time()),
                "priority": "high",
                "action_url": "/notificaciones"
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
                notification_id = result.get('id')
                push_sent = result.get('push_sent', False)
                push_count = result.get('push_count', 0)
                
                print(f"   ✅ Notificación creada: ID {notification_id}")
                print(f"   📤 Push automático: {push_sent}")
                print(f"   📱 Dispositivos: {push_count}")
                
                if push_sent and push_count > 0:
                    print(f"   🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
                    results['notification_created'] = True
                else:
                    print(f"   ⚠️ Notificación creada pero push no enviado")
            else:
                print(f"   ❌ Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    else:
        print(f"   ⏭️ Saltando (no hay suscripciones válidas)")
    
    # Resumen final
    print(f"\n" + "=" * 60)
    print(f"📋 RESUMEN DEL TEST COMPLETO")
    print(f"=" * 60)
    
    score = sum([
        results['backend_ok'],
        results['pwa_ok'], 
        results['vapid_ok'],
        results['subscriptions_valid'] > 0,
        results['push_test_ok'],
        results['notification_created']
    ])
    
    print(f"📊 PUNTUACIÓN: {score}/6")
    print(f"✅ Backend funcionando: {results['backend_ok']}")
    print(f"✅ PWA Super funcionando: {results['pwa_ok']}")
    print(f"✅ VAPID configurado: {results['vapid_ok']}")
    print(f"✅ Suscripciones válidas: {results['subscriptions_valid'] > 0} ({results['subscriptions_valid']} válidas)")
    print(f"✅ Push test funciona: {results['push_test_ok']}")
    print(f"✅ Notificación completa: {results['notification_created']}")
    
    if score == 6:
        print(f"\n🏆 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print(f"🎉 Las notificaciones push están funcionando perfectamente")
        print(f"📱 Los usuarios recibirán notificaciones incluso con la app cerrada")
    elif score >= 4:
        print(f"\n✅ SISTEMA MAYORMENTE FUNCIONAL")
        print(f"🔧 Algunos componentes necesitan atención")
    elif score >= 2:
        print(f"\n⚠️ SISTEMA PARCIALMENTE FUNCIONAL")
        print(f"🛠️ Necesita configuración adicional")
    else:
        print(f"\n❌ SISTEMA REQUIERE CONFIGURACIÓN")
        print(f"🚨 Varios componentes críticos fallan")
    
    # Instrucciones específicas
    print(f"\n💡 PRÓXIMOS PASOS:")
    
    if not results['backend_ok']:
        print(f"   🔧 Iniciar backend: cd backend && python main.py")
    
    if not results['pwa_ok']:
        print(f"   🔧 Iniciar PWA: cd pwasuper && npm run dev")
    
    if results['subscriptions_valid'] == 0:
        print(f"   📱 Abrir http://localhost:5175/test-push-debug.html")
        print(f"   📋 Seguir los 4 pasos para crear suscripción válida")
        print(f"   ✅ Habilitar notificaciones en el navegador")
    
    if score == 6:
        print(f"   🎊 ¡Felicitaciones! El sistema está listo para producción")
        print(f"   📝 Los usuarios pueden habilitar notificaciones en sus dispositivos")
        print(f"   🚀 Las notificaciones funcionarán incluso con la app cerrada")
    
    return results

def main():
    print("🚀 INICIANDO TEST COMPLETO DEL SISTEMA")
    print()
    
    results = test_complete_push_system()
    
    print(f"\n🏁 Test completado")
    
    # Return code para scripts automatizados
    score = sum([
        results['backend_ok'],
        results['pwa_ok'],
        results['vapid_ok'],
        results['subscriptions_valid'] > 0,
        results['push_test_ok'],
        results['notification_created']
    ])
    
    if score == 6:
        print(f"✨ ¡Sistema push 100% funcional!")
        return 0
    else:
        print(f"⚠️ Sistema requiere atención ({score}/6)")
        return 1

if __name__ == "__main__":
    exit(main())
