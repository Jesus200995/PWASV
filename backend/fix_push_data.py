#!/usr/bin/env python3
"""Fix: copiar datos de p256dh_key/auth_key a p256dh/auth"""
import psycopg2

conn = psycopg2.connect(
    dbname="app_registros",
    user="jesus",
    password="2025",
    host="31.97.8.51"
)
cursor = conn.cursor()

print("=" * 60)
print("🔧 FIX: SINCRONIZAR DATOS DE PUSH SUBSCRIPTIONS")
print("=" * 60)

# Verificar cuántos registros tienen datos en p256dh_key pero no en p256dh
cursor.execute("""
    SELECT COUNT(*) FROM push_subscriptions 
    WHERE p256dh_key IS NOT NULL AND (p256dh IS NULL OR p256dh = 'NULL')
""")
count_to_fix = cursor.fetchone()[0]
print(f"\n📊 Registros a actualizar (p256dh): {count_to_fix}")

# Actualizar p256dh desde p256dh_key
cursor.execute("""
    UPDATE push_subscriptions 
    SET p256dh = p256dh_key
    WHERE p256dh_key IS NOT NULL AND (p256dh IS NULL OR p256dh = 'NULL')
""")
updated_p256dh = cursor.rowcount
print(f"✅ Actualizados p256dh: {updated_p256dh}")

# Actualizar auth desde auth_key  
cursor.execute("""
    UPDATE push_subscriptions 
    SET auth = auth_key
    WHERE auth_key IS NOT NULL AND (auth IS NULL OR auth = 'NULL')
""")
updated_auth = cursor.rowcount
print(f"✅ Actualizados auth: {updated_auth}")

conn.commit()

# Verificar resultado
cursor.execute("""
    SELECT id, usuario_id, 
           SUBSTRING(p256dh, 1, 30) as p256dh,
           SUBSTRING(auth, 1, 20) as auth
    FROM push_subscriptions 
    WHERE activa = TRUE AND p256dh IS NOT NULL AND p256dh != 'NULL'
    LIMIT 5
""")
print(f"\n📊 VERIFICACIÓN - Primeras 5 suscripciones actualizadas:")
for row in cursor.fetchall():
    print(f"   ID {row[0]}: Usuario {row[1]}")
    print(f"      p256dh: {row[2]}...")
    print(f"      auth: {row[3]}...")

# Contar suscripciones válidas
cursor.execute("""
    SELECT COUNT(*) FROM push_subscriptions 
    WHERE activa = TRUE AND p256dh IS NOT NULL AND p256dh != 'NULL' 
          AND auth IS NOT NULL AND auth != 'NULL'
""")
valid_count = cursor.fetchone()[0]
print(f"\n🎯 Total suscripciones VÁLIDAS ahora: {valid_count}")

conn.close()
print("\n✅ Fix completado!")
