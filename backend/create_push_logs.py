#!/usr/bin/env python3
"""Crear tabla push_notification_logs"""
import psycopg2

conn = psycopg2.connect(
    dbname="app_registros",
    user="jesus",
    password="2025",
    host="31.97.8.51"
)
cursor = conn.cursor()

print("🔧 Creando tabla push_notification_logs...")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS push_notification_logs (
        id SERIAL PRIMARY KEY,
        notificacion_id INTEGER NOT NULL,
        usuario_id INTEGER,
        estado VARCHAR(50) NOT NULL,
        endpoint TEXT,
        error_message TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    )
""")

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_push_logs_notificacion ON push_notification_logs(notificacion_id)
""")
cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_push_logs_usuario ON push_notification_logs(usuario_id)
""")
cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_push_logs_created ON push_notification_logs(created_at)
""")

conn.commit()
print("✅ Tabla push_notification_logs creada correctamente")

# Verificar
cursor.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'push_notification_logs'
    ORDER BY ordinal_position
""")
print("\n📋 Columnas de la tabla:")
for row in cursor.fetchall():
    print(f"   {row[0]}: {row[1]}")

conn.close()
