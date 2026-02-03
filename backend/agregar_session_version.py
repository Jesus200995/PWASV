"""
Script para agregar columna de versión de sesión a la tabla de usuarios
Esto permite invalidar sesiones cuando se cambia la contraseña
"""
import psycopg2
from psycopg2 import Error

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'pwa_db',
    'user': 'postgres',
    'password': 'admin'
}

def agregar_columna_session_version():
    """Agregar columna session_version a las tablas usuarios y admin_users"""
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("=" * 60)
        print("AGREGANDO COLUMNA session_version A LAS TABLAS")
        print("=" * 60)
        
        # Agregar a tabla usuarios
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='usuarios' AND column_name='session_version'
        """)
        
        if cursor.fetchone():
            print("✅ La columna session_version ya existe en usuarios")
        else:
            cursor.execute("""
                ALTER TABLE usuarios 
                ADD COLUMN session_version INTEGER DEFAULT 1
            """)
            print("✅ Columna session_version agregada a usuarios")
        
        # Agregar a tabla admin_users
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='admin_users' AND column_name='session_version'
        """)
        
        if cursor.fetchone():
            print("✅ La columna session_version ya existe en admin_users")
        else:
            cursor.execute("""
                ALTER TABLE admin_users 
                ADD COLUMN session_version INTEGER DEFAULT 1
            """)
            print("✅ Columna session_version agregada a admin_users")
        
        # Crear índices para mejorar el rendimiento
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_usuarios_session_version 
            ON usuarios(id, session_version)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_admin_users_session_version 
            ON admin_users(id, session_version)
        """)
        
        print("✅ Índices creados exitosamente")
        
        # Confirmar cambios
        conn.commit()
        
        # Verificar la estructura
        cursor.execute("""
            SELECT id, correo, session_version 
            FROM usuarios 
            LIMIT 3
        """)
        
        print("\n📊 Primeros 3 usuarios con session_version:")
        for row in cursor.fetchall():
            print(f"   ID: {row[0]}, Correo: {row[1]}, Session Version: {row[2]}")
        
        cursor.execute("""
            SELECT id, username, session_version 
            FROM admin_users 
            LIMIT 3
        """)
        
        print("\n📊 Primeros 3 admin_users con session_version:")
        for row in cursor.fetchall():
            print(f"   ID: {row[0]}, Username: {row[1]}, Session Version: {row[2]}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        
    except Error as e:
        print(f"❌ Error: {e}")
        if conn:
            conn.rollback()

if __name__ == "__main__":
    agregar_columna_session_version()
