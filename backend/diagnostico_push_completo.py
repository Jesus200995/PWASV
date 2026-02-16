#!/usr/bin/env python3
"""
Diagnóstico completo del sistema de Push Notifications
Ejecutar con: python diagnostico_push_completo.py
"""

import sys
import json

print("=" * 60)
print("🔔 DIAGNÓSTICO SISTEMA PUSH NOTIFICATIONS")
print("=" * 60)

# 1. Verificar pywebpush
print("\n1️⃣ Verificando pywebpush...")
try:
    from pywebpush import webpush, WebPushException
    print("   ✅ pywebpush instalado correctamente")
    WEBPUSH_OK = True
except ImportError as e:
    print(f"   ❌ pywebpush NO está instalado: {e}")
    print("   💡 Ejecuta: pip install pywebpush py-vapid")
    WEBPUSH_OK = False

# 2. Verificar py-vapid
print("\n2️⃣ Verificando py-vapid...")
try:
    from py_vapid import Vapid
    print("   ✅ py-vapid instalado correctamente")
    VAPID_OK = True
except ImportError as e:
    print(f"   ❌ py-vapid NO está instalado: {e}")
    print("   💡 Ejecuta: pip install py-vapid")
    VAPID_OK = False

# 3. Verificar push_service
print("\n3️⃣ Verificando módulo push_service...")
try:
    from push_service import push_service, VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, WEBPUSH_AVAILABLE
    print("   ✅ push_service importado correctamente")
    print(f"   📝 VAPID Public Key: {VAPID_PUBLIC_KEY[:40]}...")
    print(f"   📝 VAPID Private Key: {VAPID_PRIVATE_KEY[:20]}...")
    print(f"   📝 WEBPUSH_AVAILABLE: {WEBPUSH_AVAILABLE}")
    PUSH_SERVICE_OK = True
except ImportError as e:
    print(f"   ❌ Error importando push_service: {e}")
    PUSH_SERVICE_OK = False

# 4. Verificar conexión a base de datos
print("\n4️⃣ Verificando conexión a base de datos...")
try:
    import psycopg2
    conn = psycopg2.connect(
        host="31.97.8.51",
        database="app_registros",
        user="jesus",
        password="2025",
        connect_timeout=5
    )
    cursor = conn.cursor()
    print("   ✅ Conexión a base de datos exitosa")
    DB_OK = True
except Exception as e:
    print(f"   ❌ Error conectando a BD: {e}")
    DB_OK = False
    conn = None
    cursor = None

# 5. Verificar tabla push_subscriptions
if DB_OK:
    print("\n5️⃣ Verificando tabla push_subscriptions...")
    try:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'push_subscriptions'
            )
        """)
        existe = cursor.fetchone()[0]
        if existe:
            print("   ✅ Tabla push_subscriptions existe")
            
            # Contar registros
            cursor.execute("SELECT COUNT(*) FROM push_subscriptions WHERE activa = TRUE")
            count = cursor.fetchone()[0]
            print(f"   📊 Suscripciones activas: {count}")
            
            if count > 0:
                cursor.execute("""
                    SELECT usuario_id, 
                           LEFT(endpoint, 50) as endpoint_preview,
                           fecha_creacion
                    FROM push_subscriptions 
                    WHERE activa = TRUE 
                    ORDER BY fecha_creacion DESC 
                    LIMIT 5
                """)
                print("   📱 Últimas suscripciones:")
                for row in cursor.fetchall():
                    print(f"      - Usuario {row[0]}: {row[1]}...")
            TABLE_OK = True
        else:
            print("   ❌ Tabla push_subscriptions NO existe")
            print("   💡 Ejecuta: psql -f push_notifications_setup.sql")
            TABLE_OK = False
    except Exception as e:
        print(f"   ❌ Error verificando tabla: {e}")
        TABLE_OK = False
else:
    TABLE_OK = False

# 6. Prueba de envío (simulado)
print("\n6️⃣ Prueba de creación de notificación...")
if PUSH_SERVICE_OK:
    try:
        from push_service import PushNotification, PushSubscription
        
        notification = PushNotification(
            titulo="Test",
            mensaje="Mensaje de prueba",
            tipo="success",
            prioridad="normal"
        )
        
        payload = notification.to_payload()
        data = json.loads(payload)
        print("   ✅ Notificación creada correctamente")
        print(f"   📝 Título: {data.get('title')}")
        print(f"   📝 Body: {data.get('body')}")
        print(f"   📝 Tipo: {data.get('tipo')}")
        print(f"   📝 Tag: {data.get('tag')}")
        NOTIFICATION_OK = True
    except Exception as e:
        print(f"   ❌ Error creando notificación: {e}")
        NOTIFICATION_OK = False
else:
    NOTIFICATION_OK = False

# Resumen
print("\n" + "=" * 60)
print("📋 RESUMEN DEL DIAGNÓSTICO")
print("=" * 60)

checks = [
    ("pywebpush", WEBPUSH_OK),
    ("py-vapid", VAPID_OK),
    ("push_service", PUSH_SERVICE_OK),
    ("Base de Datos", DB_OK),
    ("Tabla push_subscriptions", TABLE_OK),
    ("Crear Notificación", NOTIFICATION_OK)
]

all_ok = True
for name, status in checks:
    icon = "✅" if status else "❌"
    print(f"   {icon} {name}: {'OK' if status else 'FALLO'}")
    if not status:
        all_ok = False

print("\n" + "=" * 60)
if all_ok:
    print("🎉 SISTEMA LISTO PARA PUSH NOTIFICATIONS")
else:
    print("⚠️  HAY PROBLEMAS QUE RESOLVER")
print("=" * 60)

if conn:
    conn.close()
