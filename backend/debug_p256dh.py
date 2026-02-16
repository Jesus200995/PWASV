#!/usr/bin/env python3
"""Verificar valores reales de p256dh"""
import psycopg2

conn = psycopg2.connect(
    dbname="app_registros",
    user="jesus",
    password="2025",
    host="31.97.8.51"
)
cursor = conn.cursor()

cursor.execute("""
    SELECT id, p256dh, p256dh_key
    FROM push_subscriptions 
    WHERE activa = TRUE 
    LIMIT 3
""")

print("Comparando p256dh vs p256dh_key:")
for row in cursor.fetchall():
    print(f"\nID: {row[0]}")
    print(f"  p256dh (len={len(row[1]) if row[1] else 0}): {repr(row[1][:50]) if row[1] else None}")
    print(f"  p256dh_key (len={len(row[2]) if row[2] else 0}): {repr(row[2][:50]) if row[2] else None}")
    

# Verificar si p256dh contiene literal 'NULL'
cursor.execute("""
    SELECT COUNT(*) FROM push_subscriptions WHERE p256dh = 'NULL'
""")
null_string = cursor.fetchone()[0]
print(f"\nSuscripciones con p256dh = 'NULL' (string): {null_string}")

cursor.execute("""
    SELECT COUNT(*) FROM push_subscriptions WHERE p256dh IS NULL
""")
null_real = cursor.fetchone()[0]
print(f"Suscripciones con p256dh IS NULL (real): {null_real}")

cursor.execute("""
    SELECT COUNT(*) FROM push_subscriptions WHERE LENGTH(p256dh) > 10
""")
valid = cursor.fetchone()[0]
print(f"Suscripciones con p256dh válido (len > 10): {valid}")

conn.close()
