#!/usr/bin/env python3
"""
Limpiar suscripciones inválidas de la base de datos
"""

import requests
import os
import sys
import subprocess

def clean_database():
    """Limpiar suscripciones con endpoints vacíos"""
    print("🧹 LIMPIANDO BASE DE DATOS DE SUSCRIPCIONES INVÁLIDAS")
    print("=" * 60)
    
    # Usar script Python con psycopg2 directo
    clean_script = '''
import psycopg2
import os
from dotenv import load_dotenv

try:
    # Usar variables de entorno del sistema o valores por defecto
    conn = psycopg2.connect(
        host="localhost",
        database="app_registros", 
        user="postgres",
        password="admin"
    )
    cursor = conn.cursor()
    
    # Contar suscripciones antes
    cursor.execute("SELECT COUNT(*) FROM push_subscriptions")
    total_before = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM push_subscriptions WHERE endpoint = '' OR endpoint IS NULL")
    invalid_before = cursor.fetchone()[0]
    
    print(f"📊 ANTES DE LIMPIAR:")
    print(f"   Total suscripciones: {total_before}")  
    print(f"   Suscripciones inválidas: {invalid_before}")
    
    # Limpiar suscripciones inválidas
    cursor.execute("DELETE FROM push_subscriptions WHERE endpoint = '' OR endpoint IS NULL")
    deleted_count = cursor.rowcount
    
    conn.commit()
    
    # Contar después
    cursor.execute("SELECT COUNT(*) FROM push_subscriptions")
    total_after = cursor.fetchone()[0]
    
    print(f"\\n✅ LIMPIEZA COMPLETADA:")
    print(f"   Suscripciones eliminadas: {deleted_count}")
    print(f"   Suscripciones restantes: {total_after}")
    
    cursor.close()
    conn.close()
    
    print("\\n🎉 Base de datos limpia y lista para nuevas suscripciones")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Ejecutar manualmente: DELETE FROM push_subscriptions WHERE endpoint = '' OR endpoint IS NULL;")
'''
    
    try:
        # Escribir script temporal
        with open('clean_temp.py', 'w') as f:
            f.write(clean_script)
        
        # Ejecutar script
        result = subprocess.run([sys.executable, 'clean_temp.py'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"❌ Error ejecutando limpieza: {result.stderr}")
            print("\n💡 COMANDO MANUAL SQL:")
            print("DELETE FROM push_subscriptions WHERE endpoint = '' OR endpoint IS NULL;")
        
        # Limpiar archivo temporal
        try:
            os.remove('clean_temp.py')
        except:
            pass
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 COMANDO MANUAL SQL:")
        print("DELETE FROM push_subscriptions WHERE endpoint = '' OR endpoint IS NULL;")

def verify_cleanup():
    """Verificar que la limpieza funcionó"""
    print(f"\n🔍 VERIFICANDO LIMPIEZA VÍA API")
    print("-" * 40)
    
    backend_url = "http://localhost:8000"
    
    try:
        response = requests.get(f"{backend_url}/api/push/subscriptions", timeout=5)
        if response.status_code == 200:
            data = response.json()
            subscriptions = data.get('subscriptions', [])
            
            print(f"📊 Suscripciones restantes: {len(subscriptions)}")
            
            valid_count = 0
            for sub in subscriptions:
                endpoint = sub.get('endpoint', '')
                if endpoint and len(endpoint) > 50:
                    valid_count += 1
            
            print(f"✅ Suscripciones válidas: {valid_count}")
            print(f"❌ Suscripciones inválidas: {len(subscriptions) - valid_count}")
            
            if valid_count == len(subscriptions):
                print(f"🎉 ¡Base de datos completamente limpia!")
            else:
                print(f"⚠️ Aún hay suscripciones problemáticas")
                
        else:
            print(f"❌ Error verificando: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🔧 LIMPIADOR DE SUSCRIPCIONES PUSH")
    print()
    
    # 1. Limpiar base de datos
    clean_database()
    
    # 2. Verificar limpieza
    verify_cleanup()
    
    # 3. Instrucciones siguientes
    print(f"\n" + "=" * 60)
    print(f"📋 PRÓXIMOS PASOS")
    print(f"=" * 60)
    
    print(f"1. Base de datos limpia ✅")
    print(f"2. Abrir PWA Super: http://localhost:5175")
    print(f"3. Abrir DevTools (F12)")
    print(f"4. Habilitar notificaciones push")
    print(f"5. Verificar en Console que endpoint NO esté vacío")
    print(f"6. Con debugging añadido, veremos exactamente qué pasa")
    
    print(f"\n🔍 BUSCAR EN CONSOLE:")
    print(f"   • 'DEBUG: Datos de suscripción recibidos'")
    print(f"   • 'ENVIANDO SUSCRIPCIÓN AL SERVIDOR'") 
    print(f"   • 'Endpoint completo: https://...'")
    print(f"   • 'SUSCRIPCIÓN REGISTRADA EXITOSAMENTE'")
    
    print(f"\n⚠️ SI EL ENDPOINT SIGUE VACÍO:")
    print(f"   • El problema está en pushManager.subscribe()")
    print(f"   • Posible problema con VAPID key")
    print(f"   • Posible problema de permisos")
    print(f"   • Posible problema de configuración del navegador")

if __name__ == "__main__":
    main()
