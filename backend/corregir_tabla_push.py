#!/usr/bin/env python3
"""
Script para corregir nombres de columnas en push_subscriptions
"""

import psycopg2

# Configuración de la base de datos (igual que main.py)
DB_CONFIG = {
    "host": "31.97.8.51",
    "database": "app_registros", 
    "user": "jesus",
    "password": "2025",
    "port": "5432"
}

def corregir_columnas():
    """Renombrar columnas a los nombres correctos"""
    try:
        # Conectar a PostgreSQL
        print("🔌 Conectando a PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Renombrar columnas
        print("🔧 Renombrando columnas...")
        
        cursor.execute("ALTER TABLE push_subscriptions RENAME COLUMN p256dh_key TO p256dh;")
        cursor.execute("ALTER TABLE push_subscriptions RENAME COLUMN auth_key TO auth;")
        
        # Agregar columnas faltantes
        print("➕ Agregando columnas faltantes...")
        cursor.execute("ALTER TABLE push_subscriptions ADD COLUMN IF NOT EXISTS user_agent TEXT;")
        cursor.execute("ALTER TABLE push_subscriptions ADD COLUMN IF NOT EXISTS dispositivo TEXT;")
        
        # Confirmar cambios
        conn.commit()
        
        print("✅ Columnas corregidas exitosamente")
        
        # Verificar estructura final
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'push_subscriptions'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        print("\n📋 Estructura final de la tabla:")
        for col in columns:
            print(f"  - {col[0]}: {col[1]}")
        
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
    print("🚀 Iniciando corrección de columnas...")
    corregir_columnas()
    print("🏁 Proceso completado")
