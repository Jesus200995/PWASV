#!/usr/bin/env python3
"""
Diagnóstico detallado de push notifications
Para detectar exactamente dónde está fallando el sistema
"""

import requests
import json
import time
from datetime import datetime
import sys

def detailed_push_diagnosis():
    """Diagnóstico completo del sistema push"""
    print("🔍 DIAGNÓSTICO DETALLADO DE PUSH NOTIFICATIONS")
    print("=" * 60)
    
    backend_url = "http://localhost:8000"
    usuario_test = 2390  # Usuario test
    issues_found = []
    
    # 1. Verificar servidor VAPID
    print("\n1️⃣ VERIFICANDO SERVIDOR Y VAPID")
    try:
        response = requests.get(f"{backend_url}/api/vapid-public-key", timeout=5)
        if response.status_code == 200:
            vapid_data = response.json()
            print(f"   ✅ Backend online")
            print(f"   🔐 VAPID key disponible: {vapid_data.get('publicKey', '')[:20]}...")
        else:
            print(f"   ❌ Error backend: {response.status_code}")
            issues_found.append("Backend no responde correctamente")
            return issues_found
    except Exception as e:
        print(f"   ❌ Backend offline: {e}")
        issues_found.append(f"Backend no accesible: {e}")
        return issues_found
    
    # 2. Analizar suscripciones detalladamente
    print(f"\n2️⃣ ANALIZANDO SUSCRIPCIONES PUSH")
    try:
        response = requests.get(f"{backend_url}/api/push/subscriptions", timeout=5)
        if response.status_code == 200:
            data = response.json()
            subscriptions = data.get('subscriptions', [])
            total_subs = data.get('total', 0)
            active_subs = data.get('activas', 0)
            
            print(f"   📊 Total suscripciones: {total_subs}")
            print(f"   ✅ Suscripciones activas: {active_subs}")
            print(f"   ❌ Suscripciones inactivas: {total_subs - active_subs}")
            
            # Buscar problemas en suscripciones
            inactive_count = 0
            endpoint_issues = 0
            
            for sub in subscriptions:
                if not sub.get('is_active'):
                    inactive_count += 1
                
                endpoint = sub.get('endpoint', '')
                if not endpoint or len(endpoint) < 50:
                    endpoint_issues += 1
                    print(f"      ⚠️ Endpoint sospechoso ID {sub.get('id')}: {endpoint[:30]}...")
            
            if inactive_count > 0:
                issues_found.append(f"Hay {inactive_count} suscripciones inactivas")
            
            if endpoint_issues > 0:
                issues_found.append(f"Hay {endpoint_issues} endpoints sospechosos")
                
        else:
            print(f"   ❌ Error obteniendo suscripciones: {response.status_code}")
            issues_found.append("No se pueden obtener suscripciones")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        issues_found.append(f"Error en suscripciones: {e}")
    
    # 3. Test de envío directo
    print(f"\n3️⃣ TEST DE ENVÍO PUSH DIRECTO")
    try:
        response = requests.post(f"{backend_url}/api/push/test/{usuario_test}", timeout=15)
        if response.status_code == 200:
            result = response.json()
            push_success = result.get('success', False)
            devices_reached = result.get('dispositivos', 0)
            
            print(f"   📤 Push enviado: {push_success}")
            print(f"   📱 Dispositivos alcanzados: {devices_reached}")
            
            if not push_success or devices_reached == 0:
                issues_found.append("Push directo falla o no alcanza dispositivos")
                
        else:
            print(f"   ❌ Error en test push: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"   📄 Error: {error_detail}")
                issues_found.append(f"Test push error {response.status_code}: {error_detail}")
            except:
                issues_found.append(f"Test push error {response.status_code}")
                
    except Exception as e:
        print(f"   ❌ Error: {e}")
        issues_found.append(f"Error test push: {e}")
    
    # 4. Test de creación de notificación con push
    print(f"\n4️⃣ TEST DE NOTIFICACIÓN CON PUSH AUTOMÁTICO")
    
    notification_data = {
        "usuario_id": usuario_test,
        "tipo": "diagnostico",
        "titulo": f"🔍 Diagnóstico Push {datetime.now().strftime('%H:%M:%S')}",
        "mensaje": f"Notificación de diagnóstico para detectar problemas de push. Enviada: {datetime.now().strftime('%H:%M:%S')}",
        "datos_adicionales": {
            "diagnostic": True,
            "timestamp": int(time.time()),
            "priority": "high"
        }
    }
    
    try:
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
            
            print(f"   ✅ Notificación creada - ID: {notification_id}")
            print(f"   📱 Push automático enviado: {push_sent}")
            print(f"   📊 Dispositivos notificados: {push_count}")
            
            if not push_sent or push_count == 0:
                issues_found.append("Push automático en notificación falla")
            
        else:
            print(f"   ❌ Error creando notificación: {response.status_code}")
            issues_found.append(f"Error creando notificación: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        issues_found.append(f"Error notificación con push: {e}")
    
    # 5. Verificar logs del servidor (simulado)
    print(f"\n5️⃣ VERIFICANDO CONFIGURACIÓN PYWEBPUSH")
    try:
        # Test básico de conectividad con Google FCM
        import subprocess
        import os
        
        # Verificar si pywebpush está instalado correctamente
        result = subprocess.run([
            sys.executable, '-c', 
            'import pywebpush; print("pywebpush version:", pywebpush.__version__)'
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"   ✅ PyWebPush instalado: {version}")
        else:
            print(f"   ❌ PyWebPush error: {result.stderr}")
            issues_found.append("PyWebPush no funciona correctamente")
            
    except Exception as e:
        print(f"   ⚠️ No se pudo verificar PyWebPush: {e}")
    
    # 6. Test de formato de suscripción
    print(f"\n6️⃣ VALIDANDO FORMATO DE SUSCRIPCIONES")
    try:
        response = requests.get(f"{backend_url}/api/push/subscriptions", timeout=5)
        if response.status_code == 200:
            data = response.json()
            subscriptions = data.get('subscriptions', [])
            
            format_issues = 0
            for sub in subscriptions:
                if not sub.get('is_active'):
                    continue
                    
                # Verificar campos críticos
                endpoint = sub.get('endpoint', '')
                if not endpoint.startswith('https://'):
                    format_issues += 1
                    print(f"      ⚠️ Endpoint no HTTPS: ID {sub.get('id')}")
                
                if sub.get('usuario_id') == usuario_test:
                    print(f"      🎯 Usuario test {usuario_test} tiene suscripción activa: {sub.get('is_active')}")
                    print(f"          Endpoint: {endpoint[:50]}...")
                    print(f"          Plataforma: {sub.get('platform', 'Unknown')}")
            
            if format_issues > 0:
                issues_found.append(f"Hay {format_issues} suscripciones con formato problemático")
        
    except Exception as e:
        print(f"   ❌ Error validando formato: {e}")
    
    # Resumen final
    print(f"\n" + "=" * 60)
    print(f"📋 RESUMEN DEL DIAGNÓSTICO")
    print(f"=" * 60)
    
    if not issues_found:
        print(f"✅ ¡NO SE ENCONTRARON PROBLEMAS TÉCNICOS!")
        print(f"🔍 POSIBLES CAUSAS EXTERNAS:")
        print(f"   • Permisos de notificación revocados en el dispositivo")
        print(f"   • App no registrada correctamente para push")
        print(f"   • Firewall/proxy bloqueando FCM/VAPID endpoints")
        print(f"   • Dispositivos en modo no molestar")
        print(f"   • Service Worker no actualizado en dispositivos")
    else:
        print(f"❌ PROBLEMAS ENCONTRADOS:")
        for i, issue in enumerate(issues_found, 1):
            print(f"   {i}. {issue}")
    
    return issues_found

def test_specific_user_push(usuario_id):
    """Test específico para un usuario"""
    print(f"\n🎯 TEST ESPECÍFICO PARA USUARIO {usuario_id}")
    print("-" * 50)
    
    backend_url = "http://localhost:8000"
    
    # Obtener suscripciones del usuario específico
    try:
        response = requests.get(f"{backend_url}/api/push/subscriptions", timeout=5)
        if response.status_code == 200:
            data = response.json()
            subscriptions = data.get('subscriptions', [])
            
            user_subs = [s for s in subscriptions if s.get('usuario_id') == usuario_id and s.get('is_active')]
            
            print(f"👤 Usuario {usuario_id} tiene {len(user_subs)} suscripciones activas")
            
            for i, sub in enumerate(user_subs, 1):
                endpoint = sub.get('endpoint', '')
                platform = sub.get('platform', 'Unknown')
                created = sub.get('created_at', 'Unknown')
                
                print(f"   {i}. ID:{sub.get('id')} Platform:{platform}")
                print(f"      Endpoint: {endpoint[:60]}...")
                print(f"      Creada: {created}")
                
                # Test individual por suscripción
                print(f"      🧪 Enviando test push individual...")
                
                try:
                    test_response = requests.post(f"{backend_url}/api/push/test/{usuario_id}", timeout=10)
                    if test_response.status_code == 200:
                        result = test_response.json()
                        print(f"         ✅ Push enviado: {result.get('dispositivos', 0)} dispositivos")
                    else:
                        print(f"         ❌ Error: {test_response.status_code}")
                except Exception as e:
                    print(f"         ❌ Error: {e}")
            
            return len(user_subs) > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🚀 DIAGNÓSTICO COMPLETO DE PUSH NOTIFICATIONS")
    print("Este script detectará todos los problemas posibles")
    print()
    
    # Diagnóstico general
    issues = detailed_push_diagnosis()
    
    # Test específico para usuario de prueba
    test_specific_user_push(2390)
    
    # Test con usuarios reales que tienen suscripciones
    print(f"\n🔍 PROBANDO CON USUARIOS REALES...")
    real_users = [815, 2902, 2050, 264, 2357]  # IDs de usuarios con suscripciones activas
    
    for user_id in real_users[:3]:  # Probar solo los primeros 3
        has_subs = test_specific_user_push(user_id)
        if has_subs:
            break
    
    # Recomendaciones
    print(f"\n💡 RECOMENDACIONES:")
    
    if issues:
        print(f"🔧 SOLUCIONES TÉCNICAS:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. Resolver: {issue}")
    
    print(f"\n📱 VERIFICACIONES MANUALES EN DISPOSITIVOS:")
    print(f"   1. Abrir configuración del navegador > Notificaciones")
    print(f"   2. Verificar que el sitio tenga permisos de notificación")
    print(f"   3. Verificar que no esté en modo 'No molestar'")
    print(f"   4. Probar cerrar/abrir la PWA completamente")
    print(f"   5. Verificar conexión a internet del dispositivo")
    
    print(f"\n🌐 VERIFICACIONES DE CONECTIVIDAD:")
    print(f"   • FCM endpoint accesible desde el dispositivo")
    print(f"   • No hay proxy/firewall bloqueando")
    print(f"   • Service Worker actualizado")
    
    print(f"\n🏁 Diagnóstico completado!")

if __name__ == "__main__":
    main()
