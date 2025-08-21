#!/usr/bin/env python3
"""
Script para crear tabla de suscripciones push notifications
"""

import psycopg2
from psycopg2.extras import RealDictCursor

# Configuración de la base de datos (igual que main.py)
DB_CONFIG = {
    "host": "31.97.8.51",
    "database": "app_registros", 
    "user": "jesus",
    "password": "2025",
    "port": "5432"
}

def crear_tabla_push_subscriptions():
    """Crear tabla para almacenar suscripciones push"""
    try:
        # Conectar a PostgreSQL
        print("🔌 Conectando a PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Crear tabla push_subscriptions
        print("📝 Creando tabla push_subscriptions...")
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS push_subscriptions (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER NOT NULL,
            endpoint TEXT NOT NULL UNIQUE,
            p256dh TEXT NOT NULL,
            auth TEXT NOT NULL,
            user_agent TEXT,
            dispositivo TEXT,
            activa BOOLEAN DEFAULT TRUE,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        );
        """
        
        cursor.execute(create_table_sql)
        
        # Crear índices para optimización
        print("🔧 Creando índices...")
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_push_subscriptions_usuario_id ON push_subscriptions(usuario_id);",
            "CREATE INDEX IF NOT EXISTS idx_push_subscriptions_endpoint ON push_subscriptions(endpoint);",
            "CREATE INDEX IF NOT EXISTS idx_push_subscriptions_activa ON push_subscriptions(activa);",
        ]
        
        for indice in indices:
            cursor.execute(indice)
        
        # Confirmar cambios
        conn.commit()
        
        print("✅ Tabla push_subscriptions creada exitosamente")
        
        # Verificar estructura de la tabla
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'push_subscriptions'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        print("\n📋 Estructura de la tabla:")
        for col in columns:
            print(f"  - {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        print("🔌 Conexión cerrada")

if __name__ == "__main__":
    print("🚀 Iniciando creación de tabla push_subscriptions...")
    crear_tabla_push_subscriptions()
    print("🏁 Proceso completado")
