import sqlite3

conn = sqlite3.connect('sembrando_vida_asistencias.db')
cursor = conn.cursor()

# Ver tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tablas:", [t[0] for t in tables])

# Ver suscripciones
try:
    cursor.execute("SELECT COUNT(*) FROM push_subscriptions")
    count = cursor.fetchone()[0]
    print(f"Suscripciones: {count}")
    
    if count > 0:
        cursor.execute("SELECT user_id, endpoint, created_at FROM push_subscriptions LIMIT 3")
        subs = cursor.fetchall()
        print("Últimas suscripciones:")
        for sub in subs:
            print(f"  - Usuario {sub[0]}: {sub[1][:50]}... ({sub[2]})")
            
except Exception as e:
    print(f"Error: {e}")

conn.close()
