#!/usr/bin/env python3
"""Diagnóstico completo de Push Notifications"""
import sys
sys.path.insert(0, '/var/www/PWASV/backend')

# 1. Verificar importación
print("=" * 50)
print("1. VERIFICANDO PUSH_SERVICE")
print("=" * 50)
try:
    from push_service import push_service, PushSubscription, PushNotification, VAPID_PUBLIC_KEY
    print("✅ push_service importado correctamente")
    print(f"   VAPID_PUBLIC_KEY: {VAPID_PUBLIC_KEY[:30]}...")
except ImportError as e:
    print(f"❌ Error importando push_service: {e}")
    sys.exit(1)

# 2. Verificar base de datos
print("\n" + "=" * 50)
print("2. VERIFICANDO SUSCRIPCIONES EN DB")
print("=" * 50)
import psycopg2
conn = psycopg2.connect(
    dbname="app_registros",
    user="jesus",
    password="2025",
    host="31.97.8.51"
)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM push_subscriptions WHERE activa = TRUE")
activas = cursor.fetchone()[0]
print(f"✅ Suscripciones activas: {activas}")

cursor.execute("""
    SELECT usuario_id, endpoint, 
           CASE WHEN p256dh IS NOT NULL THEN 'OK' ELSE 'NULL' END as p256dh,
           CASE WHEN auth IS NOT NULL THEN 'OK' ELSE 'NULL' END as auth
    FROM push_subscriptions 
    WHERE activa = TRUE 
    LIMIT 5
""")
results = cursor.fetchall()
print(f"\nPrimeras 5 suscripciones:")
for row in results:
    print(f"   Usuario {row[0]}: p256dh={row[2]}, auth={row[3]}")

# 3. Intentar envío real
print("\n" + "=" * 50)
print("3. PROBANDO ENVÍO PUSH")
print("=" * 50)

# Obtener una suscripción real
cursor.execute("""
    SELECT endpoint, p256dh, auth, usuario_id
    FROM push_subscriptions
    WHERE activa = TRUE AND p256dh IS NOT NULL AND auth IS NOT NULL
    LIMIT 3
""")
subs_data = cursor.fetchall()

if not subs_data:
    print("❌ No hay suscripciones válidas con p256dh y auth")
else:
    print(f"✅ {len(subs_data)} suscripciones válidas encontradas")
    
    for sub_row in subs_data:
        print(f"\nIntentando enviar a usuario {sub_row[3]}...")
        try:
            subscription = PushSubscription(
                endpoint=sub_row[0],
                p256dh=sub_row[1],
                auth=sub_row[2],
                usuario_id=sub_row[3]
            )
            
            notification = PushNotification(
                titulo="Test Diagnóstico",
                mensaje="Si ves esto, push funciona!",
                tipo="general"
            )
            
            result = push_service.send_to_single(subscription, notification)
            print(f"   Resultado: {result}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

print("\n" + "=" * 50)
print("DIAGNÓSTICO COMPLETADO")
print("=" * 50)
