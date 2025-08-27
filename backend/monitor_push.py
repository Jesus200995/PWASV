#!/usr/bin/env python3
"""
Monitor en tiempo real de suscripciones push
Para detectar cuando se cree una nueva suscripción
"""

import requests
import time
import json
from datetime import datetime

def monitor_subscriptions():
    """Monitorear nuevas suscripciones en tiempo real"""
    print("🔍 MONITOR DE SUSCRIPCIONES PUSH EN TIEMPO REAL")
    print("=" * 60)
    
    backend_url = "http://localhost:8000"
    last_count = 0
    
    print("📱 INSTRUCCIONES:")
    print("1. Mantener este script ejecutándose")
    print("2. Abrir PWA Super: http://localhost:5175")
    print("3. Habilitar notificaciones push")
    print("4. Este monitor detectará automáticamente la nueva suscripción")
    print("5. Presiona Ctrl+C para detener")
    print()
    print("🕐 Monitoreando... (actualizando cada 2 segundos)")
    print("-" * 60)
    
    try:
        while True:
            try:
                response = requests.get(f"{backend_url}/api/push/subscriptions", timeout=3)
                if response.status_code == 200:
                    data = response.json()
                    subscriptions = data.get('subscriptions', [])
                    current_count = len(subscriptions)
                    active_count = data.get('activas', 0)
                    
                    # Detectar cambios
                    if current_count != last_count:
                        timestamp = datetime.now().strftime('%H:%M:%S')
                        print(f"🔔 [{timestamp}] ¡CAMBIO DETECTADO!")
                        print(f"   Suscripciones: {last_count} → {current_count}")
                        print(f"   Activas: {active_count}")
                        
                        # Analizar nuevas suscripciones
                        if current_count > last_count:
                            print(f"   🆕 ¡Nueva suscripción creada!")
                            
                            # Obtener la más reciente
                            latest_subs = sorted(subscriptions, key=lambda x: x.get('id', 0))[-1:]
                            
                            for sub in latest_subs:
                                sub_id = sub.get('id')
                                user_id = sub.get('usuario_id')
                                endpoint = sub.get('endpoint', '')
                                is_active = sub.get('is_active')
                                platform = sub.get('platform', 'Unknown')
                                
                                print(f"   📄 Suscripción ID: {sub_id}")
                                print(f"   👤 Usuario ID: {user_id}")
                                print(f"   ✅ Activa: {is_active}")
                                print(f"   🖥️ Plataforma: {platform}")
                                
                                if endpoint and len(endpoint) > 50:
                                    print(f"   ✅ Endpoint VÁLIDO: {endpoint[:50]}...")
                                    
                                    # Test inmediato de push
                                    print(f"   🚀 Probando push inmediatamente...")
                                    test_push_response = requests.post(f"{backend_url}/api/push/test/{user_id}", timeout=10)
                                    
                                    if test_push_response.status_code == 200:
                                        test_result = test_push_response.json()
                                        devices = test_result.get('dispositivos', 0)
                                        
                                        if devices > 0:
                                            print(f"   🎉 ¡ÉXITO! Push enviado a {devices} dispositivos")
                                        else:
                                            print(f"   ⚠️ Push no enviado (0 dispositivos)")
                                    else:
                                        print(f"   ❌ Error en test push: {test_push_response.status_code}")
                                        
                                else:
                                    print(f"   ❌ Endpoint INVÁLIDO: '{endpoint}'")
                                    print(f"   🔧 ¡PROBLEMA ENCONTRADO! El endpoint sigue vacío")
                        
                        last_count = current_count
                        print("-" * 60)
                    
                    # Mostrar estado cada 30 segundos
                    if int(time.time()) % 30 == 0:
                        timestamp = datetime.now().strftime('%H:%M:%S')
                        
                        # Contar válidas
                        valid_subs = 0
                        for sub in subscriptions:
                            endpoint = sub.get('endpoint', '')
                            if endpoint and len(endpoint) > 50 and sub.get('is_active'):
                                valid_subs += 1
                        
                        print(f"📊 [{timestamp}] Estado: {current_count} total, {active_count} activas, {valid_subs} válidas")
                
                else:
                    print(f"❌ Error API: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Error de conexión: {e}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print(f"\n⏹️ Monitor detenido")
        
        # Estado final
        try:
            response = requests.get(f"{backend_url}/api/push/subscriptions", timeout=3)
            if response.status_code == 200:
                data = response.json()
                subscriptions = data.get('subscriptions', [])
                
                valid_count = 0
                for sub in subscriptions:
                    endpoint = sub.get('endpoint', '')
                    if endpoint and len(endpoint) > 50 and sub.get('is_active'):
                        valid_count += 1
                
                print(f"\n📋 ESTADO FINAL:")
                print(f"   Total suscripciones: {len(subscriptions)}")
                print(f"   Suscripciones válidas: {valid_count}")
                
                if valid_count > 0:
                    print(f"   🎉 ¡HAY SUSCRIPCIONES VÁLIDAS!")
                    print(f"   ✅ Sistema de push notifications funcionando")
                else:
                    print(f"   ❌ No hay suscripciones válidas")
                    print(f"   🔧 El problema persiste en el frontend")
        except:
            pass

def test_current_state():
    """Test del estado actual antes de monitorear"""
    print("🔍 ESTADO ACTUAL DE SUSCRIPCIONES")
    print("-" * 40)
    
    backend_url = "http://localhost:8000"
    
    try:
        response = requests.get(f"{backend_url}/api/push/subscriptions", timeout=5)
        if response.status_code == 200:
            data = response.json()
            subscriptions = data.get('subscriptions', [])
            
            print(f"📊 Suscripciones actuales: {len(subscriptions)}")
            
            valid_count = 0
            for sub in subscriptions:
                endpoint = sub.get('endpoint', '')
                if endpoint and len(endpoint) > 50:
                    valid_count += 1
                elif sub.get('is_active'):
                    print(f"   ⚠️ Suscripción ID {sub.get('id')} activa pero endpoint inválido")
            
            print(f"✅ Suscripciones válidas: {valid_count}")
            print(f"❌ Suscripciones inválidas: {len(subscriptions) - valid_count}")
            
            return len(subscriptions)
        else:
            print(f"❌ Error: {response.status_code}")
            return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 0

def main():
    print("👀 MONITOR DE PUSH NOTIFICATIONS")
    print()
    
    # Estado inicial
    initial_count = test_current_state()
    
    print(f"\n🚀 Iniciando monitoreo desde {initial_count} suscripciones...")
    print("💡 Abre PWA Super y habilita notificaciones para ver el debugging en vivo")
    print()
    
    # Monitorear
    monitor_subscriptions()

if __name__ == "__main__":
    main()
