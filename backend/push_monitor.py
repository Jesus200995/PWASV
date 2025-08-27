#!/usr/bin/env python3
"""
Monitor de notificaciones push en tiempo real
Permite enviar notificaciones mientras monitoreamos la respuesta del sistema
"""

import requests
import json
import time
from datetime import datetime, timedelta
import threading
import sys

class PushMonitor:
    def __init__(self, backend_url="http://localhost:8000", usuario_id=2390):
        self.backend_url = backend_url
        self.usuario_id = usuario_id
        self.running = False
        self.stats = {
            'total_sent': 0,
            'total_success': 0,
            'total_push_sent': 0,
            'devices_reached': 0,
            'errors': []
        }
    
    def check_system_status(self):
        """Verificar estado del sistema"""
        print("🔍 VERIFICANDO ESTADO DEL SISTEMA...")
        print("-" * 50)
        
        # Backend
        try:
            response = requests.get(f"{self.backend_url}/api/vapid-public-key", timeout=5)
            if response.status_code == 200:
                print("✅ Backend: Online")
            else:
                print(f"❌ Backend: Error {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Backend: Offline - {e}")
            return False
        
        # Suscripciones
        try:
            response = requests.get(f"{self.backend_url}/api/push/subscriptions", timeout=5)
            if response.status_code == 200:
                subscriptions = response.json()
                user_subs = [s for s in subscriptions if s.get('usuario_id') == self.usuario_id]
                
                print(f"📱 Suscripciones totales: {len(subscriptions)}")
                print(f"👤 Suscripciones usuario {self.usuario_id}: {len(user_subs)}")
                
                if not user_subs:
                    print("⚠️ No hay suscripciones activas para este usuario")
                    print("💡 Abre PWA Super y habilita notificaciones primero")
                    
                return len(user_subs) > 0
            else:
                print(f"❌ Suscripciones: Error {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Suscripciones: Error - {e}")
            return False
    
    def send_test_notification(self, custom_message=None):
        """Enviar notificación de prueba"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        notification_data = {
            "usuario_id": self.usuario_id,
            "tipo": "test_push",
            "titulo": f"🧪 Push Test {timestamp}",
            "mensaje": custom_message or f"Notificación de prueba enviada a las {timestamp}. Si la ves, ¡funciona perfecto!",
            "datos_adicionales": {
                "test": True,
                "timestamp": int(time.time()),
                "action_url": "/notificaciones",
                "priority": "high",
                "test_id": f"test_{int(time.time())}"
            }
        }
        
        try:
            response = requests.post(
                f"{self.backend_url}/api/notifications/create",
                json=notification_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            self.stats['total_sent'] += 1
            
            if response.status_code == 200:
                result = response.json()
                notification_id = result.get('id')
                push_sent = result.get('push_sent', False)
                push_count = result.get('push_count', 0)
                
                self.stats['total_success'] += 1
                if push_sent:
                    self.stats['total_push_sent'] += 1
                    self.stats['devices_reached'] += push_count
                
                status = "📱✅" if push_sent else "📱❌"
                print(f"{timestamp} {status} ID:{notification_id} Push:{push_sent} Dispositivos:{push_count}")
                
                return True, f"ID: {notification_id}, Push: {push_sent}, Dispositivos: {push_count}"
            else:
                error_msg = f"HTTP {response.status_code}"
                self.stats['errors'].append(error_msg)
                print(f"{timestamp} ❌ Error: {error_msg}")
                return False, error_msg
                
        except Exception as e:
            error_msg = str(e)
            self.stats['errors'].append(error_msg)
            print(f"{timestamp} ❌ Excepción: {error_msg}")
            return False, error_msg
    
    def auto_sender(self, interval=30):
        """Envío automático cada X segundos"""
        print(f"🔄 Iniciando envío automático cada {interval} segundos...")
        print("Presiona Ctrl+C para detener\n")
        
        self.running = True
        counter = 1
        
        try:
            while self.running:
                message = f"Notificación automática #{counter}. Enviada desde el monitor de push notifications."
                success, details = self.send_test_notification(message)
                
                if success:
                    print(f"   ✅ Notificación #{counter} enviada: {details}")
                else:
                    print(f"   ❌ Falló notificación #{counter}: {details}")
                
                counter += 1
                
                # Esperar con posibilidad de interrupción
                for i in range(interval):
                    if not self.running:
                        break
                    time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n⏹️ Envío automático detenido")
            self.running = False
        except Exception as e:
            print(f"\n💥 Error en envío automático: {e}")
            self.running = False
    
    def show_stats(self):
        """Mostrar estadísticas"""
        print("\n" + "=" * 50)
        print("📊 ESTADÍSTICAS DEL MONITOR")
        print("=" * 50)
        
        print(f"📤 Total enviadas: {self.stats['total_sent']}")
        print(f"✅ Exitosas: {self.stats['total_success']}")
        print(f"📱 Push enviados: {self.stats['total_push_sent']}")
        print(f"📟 Dispositivos alcanzados: {self.stats['devices_reached']}")
        
        success_rate = (self.stats['total_success'] / self.stats['total_sent'] * 100) if self.stats['total_sent'] > 0 else 0
        print(f"📈 Tasa de éxito: {success_rate:.1f}%")
        
        if self.stats['errors']:
            print(f"\n❌ Errores ({len(self.stats['errors'])}):")
            for error in set(self.stats['errors'])[:5]:  # Mostrar máximo 5 errores únicos
                count = self.stats['errors'].count(error)
                print(f"   • {error} ({count}x)")
    
    def interactive_mode(self):
        """Modo interactivo"""
        print("🎮 MODO INTERACTIVO")
        print("Comandos disponibles:")
        print("  's' - Enviar notificación simple")
        print("  'm [mensaje]' - Enviar con mensaje personalizado")
        print("  'a [segundos]' - Iniciar envío automático")
        print("  'stats' - Mostrar estadísticas")
        print("  'q' - Salir")
        print()
        
        while True:
            try:
                cmd = input("Monitor> ").strip().lower()
                
                if cmd == 'q' or cmd == 'quit':
                    break
                elif cmd == 's':
                    success, details = self.send_test_notification()
                    print(f"   Resultado: {details}")
                elif cmd.startswith('m '):
                    message = cmd[2:].strip()
                    if message:
                        success, details = self.send_test_notification(message)
                        print(f"   Resultado: {details}")
                    else:
                        print("   ❌ Mensaje vacío")
                elif cmd.startswith('a '):
                    try:
                        interval = int(cmd[2:].strip())
                        if 5 <= interval <= 300:
                            self.auto_sender(interval)
                        else:
                            print("   ❌ Intervalo debe ser entre 5 y 300 segundos")
                    except ValueError:
                        print("   ❌ Intervalo inválido")
                elif cmd == 'stats':
                    self.show_stats()
                elif cmd == 'help':
                    print("   Comandos: s, m [msg], a [seg], stats, q")
                else:
                    print("   ❌ Comando no reconocido. Usa 'help' para ver comandos")
                    
            except KeyboardInterrupt:
                print("\n⏹️ Saliendo...")
                break
            except Exception as e:
                print(f"   💥 Error: {e}")

def main():
    print("🚀 MONITOR DE NOTIFICACIONES PUSH")
    print("=" * 50)
    
    monitor = PushMonitor()
    
    # Verificar estado inicial
    if not monitor.check_system_status():
        print("\n❌ Sistema no está listo. Verifica:")
        print("   1. Backend corriendo en puerto 8000")
        print("   2. PWA Super con notificaciones habilitadas")
        print("   3. Usuario con suscripciones activas")
        return
    
    print(f"\n✅ Sistema listo para testing")
    print("-" * 50)
    
    # Menú principal
    while True:
        print(f"\n🎯 ¿Qué quieres hacer?")
        print(f"   1. Enviar notificación de prueba")
        print(f"   2. Envío automático cada X segundos")
        print(f"   3. Modo interactivo")
        print(f"   4. Mostrar estadísticas")
        print(f"   5. Salir")
        
        try:
            choice = input("\nSelecciona (1-5): ").strip()
            
            if choice == '1':
                print("\n📤 Enviando notificación de prueba...")
                success, details = monitor.send_test_notification()
                print(f"Resultado: {details}")
                
            elif choice == '2':
                try:
                    interval = int(input("Intervalo en segundos (5-300): "))
                    if 5 <= interval <= 300:
                        monitor.auto_sender(interval)
                    else:
                        print("❌ Intervalo debe ser entre 5 y 300 segundos")
                except ValueError:
                    print("❌ Número inválido")
                    
            elif choice == '3':
                monitor.interactive_mode()
                
            elif choice == '4':
                monitor.show_stats()
                
            elif choice == '5':
                print("👋 ¡Hasta luego!")
                break
                
            else:
                print("❌ Opción inválida")
                
        except KeyboardInterrupt:
            print("\n⏹️ Saliendo...")
            break
        except Exception as e:
            print(f"💥 Error inesperado: {e}")

if __name__ == "__main__":
    main()
