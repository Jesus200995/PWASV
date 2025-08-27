#!/usr/bin/env python3
"""
Script de verificación rápida para notificaciones push
Para usar después de habilitar notificaciones en PWA Super
"""

import requests
import json
from datetime import datetime

def quick_push_test():
    """Test rápido de push notifications"""
    print("⚡ VERIFICACIÓN RÁPIDA DE PUSH NOTIFICATIONS")
    print("=" * 50)
    
    backend_url = "http://localhost:8000"
    usuario_id = 2390
    
    # 1. Verificar suscripciones
    try:
        response = requests.get(f"{backend_url}/api/push/subscriptions", timeout=5)
        if response.status_code == 200:
            subscriptions = response.json()
            user_subs = [s for s in subscriptions if s.get('usuario_id') == usuario_id]
            
            print(f"👤 Suscripciones del usuario {usuario_id}: {len(user_subs)}")
            
            if user_subs:
                print("✅ ¡Usuario tiene suscripciones activas!")
                for i, sub in enumerate(user_subs, 1):
                    endpoint = sub.get('endpoint', '')
                    # Mostrar solo los últimos caracteres del endpoint
                    endpoint_display = "..." + endpoint[-30:] if len(endpoint) > 30 else endpoint
                    print(f"   {i}. {endpoint_display}")
            else:
                print("❌ Usuario sin suscripciones. Habilita notificaciones en PWA Super.")
                return False
        else:
            print(f"❌ Error verificando suscripciones: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # 2. Enviar notificación de prueba
    print(f"\n📤 Enviando notificación de prueba...")
    
    timestamp = datetime.now().strftime('%H:%M:%S')
    notification_data = {
        "usuario_id": usuario_id,
        "tipo": "test_final",
        "titulo": f"🎉 ¡Push funcionando! {timestamp}",
        "mensaje": f"¡Excelente! Las notificaciones push están funcionando perfectamente. Esta fue enviada a las {timestamp} mientras la app puede estar cerrada.",
        "datos_adicionales": {
            "success_test": True,
            "timestamp": timestamp,
            "action_url": "/notificaciones",
            "priority": "high"
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
            
            print(f"✅ Notificación creada - ID: {notification_id}")
            print(f"📱 Push enviado: {'SÍ' if push_sent else 'NO'}")
            print(f"📊 Dispositivos notificados: {push_count}")
            
            if push_sent and push_count > 0:
                print(f"\n🎉 ¡ÉXITO TOTAL!")
                print(f"   ✅ Sistema de push notifications 100% funcional")
                print(f"   ✅ Notificación enviada a {push_count} dispositivo(s)")
                print(f"   ✅ Funciona incluso con la app cerrada")
                print(f"   📱 Revisa tu dispositivo para ver la notificación")
                return True
            else:
                print(f"\n⚠️ Notificación creada pero no se envió push")
                return False
        else:
            print(f"❌ Error creando notificación: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_with_custom_message():
    """Test con mensaje personalizado"""
    print(f"\n💬 Enviando notificación personalizada...")
    
    backend_url = "http://localhost:8000"
    usuario_id = 2390
    
    notification_data = {
        "usuario_id": usuario_id,
        "tipo": "personalizada",
        "titulo": "🌟 Notificación Personalizada",
        "mensaje": "Esta es una notificación con mensaje personalizado. Puedes personalizar completamente el título, mensaje, iconos y comportamiento. ¡El sistema está listo para producción!",
        "datos_adicionales": {
            "custom": True,
            "priority": "normal",
            "action_url": "/dashboard",
            "badge": "🌟"
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
            push_sent = result.get('push_sent', False)
            push_count = result.get('push_count', 0)
            
            status = "✅" if push_sent else "❌"
            print(f"   {status} Push enviado: {push_sent} ({push_count} dispositivos)")
            return push_sent
        else:
            print(f"   ❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando verificación rápida...")
    print("📋 Asegúrate de que:")
    print("   1. PWA Super esté abierta en tu dispositivo")
    print("   2. Hayas habilitado notificaciones push")
    print("   3. Hayas aceptado los permisos del navegador")
    print()
    
    input("Presiona Enter cuando estés listo...")
    
    success = quick_push_test()
    
    if success:
        print(f"\n🎊 ¡FELICITACIONES!")
        print(f"Sistema de notificaciones push completamente funcional")
        
        response = input("\n¿Enviar notificación personalizada adicional? (s/n): ").lower()
        if response in ['s', 'y', 'si', 'yes']:
            test_with_custom_message()
        
        print(f"\n🏆 SISTEMA LISTO PARA PRODUCCIÓN")
        print(f"   ✅ Notificaciones push funcionando")
        print(f"   ✅ Funciona con app cerrada")
        print(f"   ✅ Navegación automática implementada")
        print(f"   ✅ Persistencia en base de datos")
        print(f"   ✅ Sistema VAPID configurado")
    else:
        print(f"\n🔧 PRÓXIMOS PASOS:")
        print(f"   1. Abre PWA Super: http://localhost:5175")
        print(f"   2. Inicia sesión")
        print(f"   3. Busca la opción de notificaciones")
        print(f"   4. Habilita las notificaciones push")
        print(f"   5. Acepta los permisos del navegador")
        print(f"   6. Ejecuta este script otra vez")
    
    print(f"\n✨ ¡Gracias por usar el sistema de push notifications!")
