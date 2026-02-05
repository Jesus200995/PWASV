#!/usr/bin/env python3
"""
Script para agregar columna 'activo' a la tabla 'usuarios'
Ejecutar este script para habilitar la funcionalidad de desactivar cuentas
"""

import psycopg2
from psycopg2 import sql

# Configuración de conexión al VPS
DB_CONFIG = {
    'host': '31.97.8.51',
    'database': 'app_registros',
    'user': 'jesus',
    'password': input('Ingresa la contraseña de la base de datos: ')
}

def agregar_columna_activo():
    """Agrega la columna 'activo' a la tabla usuarios si no existe"""
    
    try:
        # Conectar a la base de datos
        print(f"🔌 Conectando a {DB_CONFIG['host']}...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("✅ Conexión establecida\n")
        
        # Verificar si la columna ya existe
        print("🔍 Verificando si la columna 'activo' existe en la tabla 'usuarios'...")
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.columns 
                WHERE table_name = 'usuarios' 
                AND column_name = 'activo'
            );
        """)
        
        existe = cursor.fetchone()[0]
        
        if existe:
            print("⚠️  La columna 'activo' ya existe en la tabla 'usuarios'")
        else:
            print("📝 Agregando columna 'activo' a la tabla 'usuarios'...")
            cursor.execute("""
                ALTER TABLE usuarios 
                ADD COLUMN activo BOOLEAN DEFAULT TRUE;
            """)
            conn.commit()
            print("✅ Columna 'activo' agregada exitosamente")
        
        # Actualizar todos los registros existentes
        print("\n🔄 Actualizando registros existentes...")
        cursor.execute("""
            UPDATE usuarios 
            SET activo = TRUE 
            WHERE activo IS NULL;
        """)
        registros_actualizados = cursor.rowcount
        conn.commit()
        print(f"✅ {registros_actualizados} registros actualizados con activo = TRUE")
        
        # Verificar el resultado
        print("\n📊 Estadísticas de usuarios:")
        cursor.execute("""
            SELECT 
                COUNT(*) as total_usuarios, 
                COUNT(*) FILTER (WHERE activo = TRUE) as usuarios_activos,
                COUNT(*) FILTER (WHERE activo = FALSE) as usuarios_inactivos
            FROM usuarios;
        """)
        
        stats = cursor.fetchone()
        print(f"  - Total de usuarios: {stats[0]}")
        print(f"  - Usuarios activos: {stats[1]}")
        print(f"  - Usuarios inactivos: {stats[2]}")
        
        # Cerrar conexión
        cursor.close()
        conn.close()
        
        print("\n✅ ¡Migración completada exitosamente!")
        print("\n💡 Ahora puedes usar el botón de desactivar/activar en UsuariosView.vue")
        
    except psycopg2.Error as e:
        print(f"\n❌ Error de PostgreSQL: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("\n🔌 Conexión cerrada")

if __name__ == "__main__":
    print("=" * 60)
    print("MIGRACIÓN: Agregar columna 'activo' a tabla 'usuarios'")
    print("=" * 60)
    print()
    
    agregar_columna_activo()
