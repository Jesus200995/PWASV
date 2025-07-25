#!/usr/bin/env python3
"""
Script para agregar la columna CURP a la base de datos de producción
IMPORTANTE: Ejecutar este script ANTES de usar el nuevo código
"""

import psycopg2
import sys

# Configuración de la base de datos (misma que en main.py)
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"

def agregar_columna_curp():
    """Agregar la columna CURP a la tabla usuarios"""
    try:
        # Conectar a la base de datos
        print("🔗 Conectando a la base de datos...")
        conn = psycopg2.connect(
            host=DB_HOST, 
            database=DB_NAME, 
            user=DB_USER, 
            password=DB_PASS
        )
        cursor = conn.cursor()
        print("✅ Conexión exitosa")
        
        # Verificar si la columna ya existe
        print("🔍 Verificando si la columna CURP ya existe...")
        cursor.execute("""
            SELECT 1 
            FROM information_schema.columns 
            WHERE table_name = 'usuarios' 
            AND column_name = 'curp'
        """)
        
        if cursor.fetchone():
            print("ℹ️  La columna CURP ya existe en la tabla usuarios")
            return True
        
        # Agregar la columna CURP
        print("➕ Agregando columna CURP...")
        cursor.execute("ALTER TABLE usuarios ADD COLUMN curp VARCHAR(18) UNIQUE")
        
        # Agregar comentario
        cursor.execute("COMMENT ON COLUMN usuarios.curp IS 'Clave Única de Registro de Población - 18 caracteres obligatorios'")
        
        # Crear índice
        print("📊 Creando índice para CURP...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_usuarios_curp ON usuarios(curp)")
        
        # Confirmar cambios
        conn.commit()
        print("✅ Columna CURP agregada exitosamente")
        
        # Verificar estructura final
        print("🔍 Verificando estructura final...")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'usuarios' 
            ORDER BY ordinal_position
        """)
        
        columnas = cursor.fetchall()
        print("\n📋 Estructura de la tabla usuarios:")
        for col in columnas:
            nullable = "NULL" if col[2] == "YES" else "NOT NULL"
            default = f" DEFAULT {col[3]}" if col[3] else ""
            print(f"  - {col[0]}: {col[1]} {nullable}{default}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🚀 Script para agregar columna CURP a la base de datos")
    print("=" * 60)
    
    if agregar_columna_curp():
        print("\n🎉 ¡Columna CURP agregada exitosamente!")
        print("✅ Ahora puedes usar el sistema con CURP obligatoria")
    else:
        print("\n💥 Error al agregar la columna CURP")
        print("❌ Revisar la conexión a la base de datos")
        sys.exit(1)

if __name__ == "__main__":
    main()
