#!/usr/bin/env python3
"""Debug: verificar qué está pasando con los valores"""
import psycopg2

conn = psycopg2.connect(
    dbname="app_registros",
    user="jesus",
    password="2025",
    host="31.97.8.51"
)
cursor = conn.cursor()

# Ver si hay valores vacíos
cursor.execute("""
    SELECT p256dh, LENGTH(p256dh) as len_p256dh, p256dh_key, LENGTH(p256dh_key) as len_key
    FROM push_subscriptions 
    WHERE activa = TRUE 
    LIMIT 3
""")

print("🔍 Verificando valores de columnas:")
for row in cursor.fetchall():
    print(f"  p256dh = {repr(row[0])}, len={row[1]}")
    print(f"  p256dh_key = {repr(row[2][:30] if row[2] else None)}..., len={row[3]}")
    print()

# Contar por tipo de valor
cursor.execute("""
    SELECT 
        COUNT(*) FILTER (WHERE p256dh = '') as p256dh_empty,
        COUNT(*) FILTER (WHERE p256dh IS NULL) as p256dh_null,
        COUNT(*) FILTER (WHERE p256dh_key IS NOT NULL AND LENGTH(p256dh_key) > 10) as p256dh_key_valid
    FROM push_subscriptions 
    WHERE activa = TRUE
""")
row = cursor.fetchone()
print(f"📊 Estadísticas:")
print(f"   p256dh vacío (string ''): {row[0]}")
print(f"   p256dh NULL: {row[1]}")
print(f"   p256dh_key válido (len>10): {row[2]}")

# Actualizar con COALESCE
print("\n🔧 Actualizando p256dh desde p256dh_key (donde p256dh está vacío)...")
cursor.execute("""
    UPDATE push_subscriptions 
    SET p256dh = p256dh_key
    WHERE (p256dh IS NULL OR p256dh = '' OR LENGTH(p256dh) < 10) 
          AND p256dh_key IS NOT NULL AND LENGTH(p256dh_key) > 10
""")
print(f"   Actualizados p256dh: {cursor.rowcount}")

cursor.execute("""
    UPDATE push_subscriptions 
    SET auth = auth_key
    WHERE (auth IS NULL OR auth = '' OR LENGTH(auth) < 10) 
          AND auth_key IS NOT NULL AND LENGTH(auth_key) > 10
""")
print(f"   Actualizados auth: {cursor.rowcount}")

conn.commit()

# Verificar
cursor.execute("""
    SELECT id, p256dh, auth
    FROM push_subscriptions 
    WHERE activa = TRUE AND LENGTH(p256dh) > 10 AND LENGTH(auth) > 10
    LIMIT 3
""")
print("\n✅ Verificación después del update:")
for row in cursor.fetchall():
    print(f"   ID {row[0]}: p256dh={row[1][:30]}..., auth={row[2][:20]}...")

cursor.execute("""
    SELECT COUNT(*) FROM push_subscriptions 
    WHERE activa = TRUE AND LENGTH(p256dh) > 10 AND LENGTH(auth) > 10
""")
print(f"\n🎯 Total suscripciones VÁLIDAS: {cursor.fetchone()[0]}")

conn.close()
