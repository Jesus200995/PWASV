# -*- coding: utf-8 -*-
import psycopg2

try:
    conn = psycopg2.connect(
        host='localhost',
        database='pwa_db',
        user='postgres',
        password='admin'
    )
    cursor = conn.cursor()
    
    print("=" * 60)
    print("Agregando columna session_version")
    print("=" * 60)
    
    # Usuarios
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='usuarios' AND column_name='session_version'
    """)
    
    if cursor.fetchone():
        print("OK: session_version existe en usuarios")
    else:
        cursor.execute("""
            ALTER TABLE usuarios 
            ADD COLUMN session_version INTEGER DEFAULT 1
        """)
        print("OK: session_version agregada a usuarios")
    
    # Admin users
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='admin_users' AND column_name='session_version'
    """)
    
    if cursor.fetchone():
        print("OK: session_version existe en admin_users")
    else:
        cursor.execute("""
            ALTER TABLE admin_users 
            ADD COLUMN session_version INTEGER DEFAULT 1
        """)
        print("OK: session_version agregada a admin_users")
    
    # Indices
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_usuarios_session_version 
        ON usuarios(id, session_version)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_admin_users_session_version 
        ON admin_users(id, session_version)
    """)
    
    print("OK: Indices creados")
    
    conn.commit()
    
    print("\nPrimeros 3 usuarios:")
    cursor.execute("SELECT id, correo, session_version FROM usuarios LIMIT 3")
    for row in cursor.fetchall():
        print(f"  ID: {row[0]}, Correo: {row[1]}, Version: {row[2]}")
    
    print("\nPrimeros 3 admin_users:")
    cursor.execute("SELECT id, username, session_version FROM admin_users LIMIT 3")
    for row in cursor.fetchall():
        print(f"  ID: {row[0]}, Username: {row[1]}, Version: {row[2]}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("COMPLETADO")
    print("=" * 60)
    
except Exception as e:
    print(f"ERROR: {e}")
    if 'conn' in locals():
        conn.rollback()
