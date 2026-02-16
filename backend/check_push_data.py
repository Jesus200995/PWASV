#!/usr/bin/env python3
"""Verificar datos de suscripciones push"""
import psycopg2

conn = psycopg2.connect(
    dbname="app_registros",
    user="jesus",
    password="2025",
    host="31.97.8.51"
)
cursor = conn.cursor()

print("=" * 60)
print("🔍 VERIFICANDO SUSCRIPCIONES PUSH")
print("=" * 60)

# Ver estructura de la tabla
cursor.execute("""
    SELECT column_name, data_type, is_nullable 
    FROM information_schema.columns 
    WHERE table_name = 'push_subscriptions'
    ORDER BY ordinal_position
""")
print("\n📋 ESTRUCTURA DE LA TABLA:")
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[1]} (nullable: {row[2]})")

# Verificar datos con p256dh y auth NOT NULL
cursor.execute("""
    SELECT id, usuario_id, 
           endpoint,
           p256dh,
           auth,
           p256dh_key,
           auth_key
    FROM push_subscriptions 
    WHERE activa = TRUE
    LIMIT 5
""")
print("\n📊 PRIMERAS 5 SUSCRIPCIONES ACTIVAS:")
for row in cursor.fetchall():
    print(f"\n   ID: {row[0]}")
    print(f"   Usuario: {row[1]}")
    print(f"   Endpoint: {row[2][:60]}...")
    print(f"   p256dh: {row[3][:30] if row[3] else 'NULL'}...")
    print(f"   auth: {row[4][:20] if row[4] else 'NULL'}...")
    print(f"   p256dh_key: {row[5][:30] if row[5] else 'NULL'}...")
    print(f"   auth_key: {row[6][:20] if row[6] else 'NULL'}...")

# Contar cuántas tienen p256dh y auth llenos
cursor.execute("""
    SELECT 
        COUNT(*) FILTER (WHERE p256dh IS NOT NULL AND auth IS NOT NULL) as con_p256dh_auth,
        COUNT(*) FILTER (WHERE p256dh_key IS NOT NULL AND auth_key IS NOT NULL) as con_p256dh_key_auth_key,
        COUNT(*) FILTER (WHERE (p256dh IS NOT NULL OR p256dh_key IS NOT NULL) AND (auth IS NOT NULL OR auth_key IS NOT NULL)) as cualquiera
    FROM push_subscriptions 
    WHERE activa = TRUE
""")
row = cursor.fetchone()
print(f"\n📈 ESTADÍSTICAS:")
print(f"   Con p256dh + auth: {row[0]}")
print(f"   Con p256dh_key + auth_key: {row[1]}")
print(f"   Con cualquier combinación: {row[2]}")

# Verificar los que tienen datos en p256dh_key pero no en p256dh
cursor.execute("""
    SELECT id, usuario_id, 
           p256dh_key, auth_key
    FROM push_subscriptions 
    WHERE activa = TRUE AND p256dh_key IS NOT NULL AND p256dh IS NULL
    LIMIT 5
""")
rows = cursor.fetchall()
print(f"\n📊 SUSCRIPCIONES CON p256dh_key PERO SIN p256dh:")
print(f"   Encontradas: {len(rows)}")
for row in rows:
    print(f"   ID {row[0]}, Usuario {row[1]}")
    print(f"      p256dh_key: {row[2][:30] if row[2] else 'NULL'}...")
    print(f"      auth_key: {row[3][:20] if row[3] else 'NULL'}...")

conn.close()
