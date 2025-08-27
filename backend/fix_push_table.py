#!/usr/bin/env python3
"""
Script para arreglar la tabla push_subscriptions
"""

import psycopg2

# Conexión a PostgreSQL
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"

def fix_push_subscriptions_table():
    try:
        print("🔧 Conectando a la base de datos...")
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cursor = conn.cursor()
        
        print("✅ Conexión establecida")
        
        # Verificar si la tabla existe
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'push_subscriptions'
            );
        """)
        
        tabla_existe = cursor.fetchone()[0]
        
        if tabla_existe:
            print("🗑️ Eliminando tabla existente...")
            cursor.execute("DROP TABLE IF EXISTS push_subscriptions CASCADE;")
        
        print("🔨 Creando tabla push_subscriptions...")
        cursor.execute("""
            CREATE TABLE push_subscriptions (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER NOT NULL,
                endpoint VARCHAR(500) NOT NULL UNIQUE,
                p256dh_key VARCHAR(200) NOT NULL,
                auth_key VARCHAR(50) NOT NULL,
                user_agent TEXT,
                device_type VARCHAR(50),
                platform VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            );
        """)
        
        print("📊 Creando índices...")
        cursor.execute("""
            CREATE INDEX idx_push_subscriptions_usuario 
            ON push_subscriptions(usuario_id);
        """)
        
        cursor.execute("""
            CREATE INDEX idx_push_subscriptions_active 
            ON push_subscriptions(is_active);
        """)
        
        cursor.execute("""
            CREATE INDEX idx_push_subscriptions_endpoint 
            ON push_subscriptions(endpoint);
        """)
        
        # Commit los cambios
        conn.commit()
        
        print("✅ Tabla push_subscriptions creada exitosamente")
        
        # Verificar estructura
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'push_subscriptions'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        print("\n📋 Estructura de la tabla:")
        for col in columns:
            print(f"  - {col[0]} ({col[1]}) {'NULL' if col[2] == 'YES' else 'NOT NULL'} {col[3] or ''}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Tabla arreglada exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error arreglando tabla: {e}")
        return False

if __name__ == "__main__":
    fix_push_subscriptions_table()
