#!/usr/bin/env python3
"""
Script de prueba para verificar las tablas de notificaciones
"""

import psycopg2
from psycopg2.extras import RealDictCursor

# Conexión a PostgreSQL
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"

def verificar_tablas():
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cursor = conn.cursor()
        
        print("🔍 Verificando estructura de tablas de notificaciones...")
        
        # Verificar tabla notificaciones
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'notificaciones' 
            ORDER BY ordinal_position
        """)
        
        columnas_notificaciones = cursor.fetchall()
        
        if columnas_notificaciones:
            print("\n✅ Tabla 'notificaciones' encontrada:")
            for col in columnas_notificaciones:
                print(f"   - {col[0]} ({col[1]}) {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
        else:
            print("❌ Tabla 'notificaciones' NO encontrada")
            return False
        
        # Verificar tabla notificacion_usuarios
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'notificacion_usuarios' 
            ORDER BY ordinal_position
        """)
        
        columnas_nu = cursor.fetchall()
        
        if columnas_nu:
            print("\n✅ Tabla 'notificacion_usuarios' encontrada:")
            for col in columnas_nu:
                print(f"   - {col[0]} ({col[1]}) {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
        else:
            print("❌ Tabla 'notificacion_usuarios' NO encontrada")
            return False
        
        # Verificar relaciones de clave foránea
        cursor.execute("""
            SELECT 
                tc.table_name, 
                kcu.column_name, 
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name 
            FROM 
                information_schema.table_constraints AS tc 
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                  AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                  ON ccu.constraint_name = tc.constraint_name
                  AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY' 
              AND tc.table_name='notificacion_usuarios'
        """)
        
        relaciones = cursor.fetchall()
        
        if relaciones:
            print("\n🔗 Relaciones de clave foránea encontradas:")
            for rel in relaciones:
                print(f"   - {rel[0]}.{rel[1]} -> {rel[2]}.{rel[3]}")
        
        # Contar registros existentes
        cursor.execute("SELECT COUNT(*) FROM notificaciones")
        total_notificaciones = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM notificacion_usuarios")  
        total_nu = cursor.fetchone()[0]
        
        print(f"\n📊 Estado actual:")
        print(f"   - Notificaciones: {total_notificaciones} registros")
        print(f"   - Notificación-usuarios: {total_nu} registros")
        
        conn.close()
        print("\n✅ Verificación completada. Las tablas están listas para usar.")
        return True
        
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
        return False

if __name__ == "__main__":
    verificar_tablas()
