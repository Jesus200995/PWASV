#!/usr/bin/env python3
"""Test detallado de Push Notifications en el endpoint de notificaciones"""
import sys
sys.path.insert(0, '/var/www/PWASV/backend')

print("=" * 60)
print("🧪 TEST DETALLADO: CREAR NOTIFICACIÓN CON PUSH")
print("=" * 60)

# 1. Verificar PUSH_NOTIFICATIONS_ENABLED
print("\n1. VERIFICANDO VARIABLE PUSH_NOTIFICATIONS_ENABLED...")
try:
    from push_service import push_service, PushSubscription, PushNotification, VAPID_PUBLIC_KEY
    PUSH_NOTIFICATIONS_ENABLED = True
    print(f"   ✅ PUSH_NOTIFICATIONS_ENABLED = {PUSH_NOTIFICATIONS_ENABLED}")
except ImportError as e:
    PUSH_NOTIFICATIONS_ENABLED = False
    print(f"   ❌ PUSH_NOTIFICATIONS_ENABLED = {PUSH_NOTIFICATIONS_ENABLED}")
    print(f"   Error: {e}")

# 2. Conectar a la base de datos
print("\n2. VERIFICANDO SUSCRIPCIONES EN BASE DE DATOS...")
import psycopg2
conn = psycopg2.connect(
    dbname="app_registros",
    user="jesus",
    password="2025",
    host="31.97.8.51"
)
cursor = conn.cursor()

cursor.execute("""
    SELECT COUNT(*) FROM push_subscriptions 
    WHERE activa = TRUE AND p256dh IS NOT NULL AND auth IS NOT NULL
""")
count = cursor.fetchone()[0]
print(f"   📊 Suscripciones válidas con p256dh y auth: {count}")

# 3. Obtener algunas suscripciones de prueba
print("\n3. OBTENIENDO SUSCRIPCIONES PARA TEST...")
cursor.execute("""
    SELECT ps.endpoint, ps.p256dh, ps.auth, ps.usuario_id
    FROM push_subscriptions ps
    WHERE ps.activa = TRUE AND ps.p256dh IS NOT NULL AND ps.auth IS NOT NULL
    LIMIT 5
""")
results = cursor.fetchall()
print(f"   📱 {len(results)} suscripciones obtenidas")

if not results:
    print("   ❌ No hay suscripciones!!! Este es el problema.")
    sys.exit(1)

# 4. Probar envío push directo
print("\n4. PROBANDO ENVÍO PUSH DIRECTO A send_to_multiple...")
subscriptions = [
    PushSubscription(
        endpoint=row[0],
        p256dh=row[1],
        auth=row[2],
        usuario_id=row[3]
    )
    for row in results
]

notification = PushNotification(
    titulo="Test Directo send_to_multiple",
    mensaje="Si ves esto, el backend push FUNCIONA!",
    tipo="general",
    prioridad="normal"
)

print(f"   📤 Enviando a {len(subscriptions)} dispositivos...")
try:
    result = push_service.send_to_multiple(subscriptions, notification)
    print(f"   ✅ Resultado: {result}")
except Exception as e:
    print(f"   ❌ Error en send_to_multiple: {e}")
    import traceback
    traceback.print_exc()

# 5. Simular la función enviar_push_a_destinatarios
print("\n5. SIMULANDO enviar_push_a_destinatarios...")
print("   Este es exactamente lo que hace el endpoint /notificaciones...")

# Mismo query que usa la función
cursor.execute("""
    SELECT ps.endpoint, ps.p256dh, ps.auth, ps.usuario_id
    FROM push_subscriptions ps
    WHERE ps.activa = TRUE
""")
results2 = cursor.fetchall()
print(f"   📊 Query 'enviada_a_todos' devolvió: {len(results2)} filas")

if results2:
    print(f"   Primera fila:")
    print(f"      endpoint: {results2[0][0][:50]}...")
    print(f"      p256dh: {results2[0][1][:30] if results2[0][1] else 'NULL'}...")
    print(f"      auth: {results2[0][2][:20] if results2[0][2] else 'NULL'}...")
    print(f"      usuario_id: {results2[0][3]}")

print("\n" + "=" * 60)
print("🏁 TEST COMPLETADO")
print("=" * 60)
