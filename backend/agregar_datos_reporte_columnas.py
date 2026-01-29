#!/usr/bin/env python3
"""
Script para agregar las columnas necesarias para el nuevo flujo de reportes:
- datos_reporte: JSON con los datos estructurados del reporte
- firma_usuario_base64: Firma digital del usuario que elaboró el reporte
"""

import psycopg2

# Conexión a la base de datos
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"

def agregar_columnas():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()
        
        print("🔄 Verificando y agregando columnas a reportes_generados...")
        
        # Verificar si la columna datos_reporte existe
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'reportes_generados' 
            AND column_name = 'datos_reporte'
        """)
        
        if not cursor.fetchone():
            print("   ➕ Agregando columna datos_reporte (JSONB)...")
            cursor.execute("""
                ALTER TABLE reportes_generados 
                ADD COLUMN datos_reporte JSONB
            """)
            print("   ✅ Columna datos_reporte agregada")
        else:
            print("   ✅ Columna datos_reporte ya existe")
        
        # Verificar si la columna firma_usuario_base64 existe
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'reportes_generados' 
            AND column_name = 'firma_usuario_base64'
        """)
        
        if not cursor.fetchone():
            print("   ➕ Agregando columna firma_usuario_base64 (TEXT)...")
            cursor.execute("""
                ALTER TABLE reportes_generados 
                ADD COLUMN firma_usuario_base64 TEXT
            """)
            print("   ✅ Columna firma_usuario_base64 agregada")
        else:
            print("   ✅ Columna firma_usuario_base64 ya existe")
        
        conn.commit()
        
        # Mostrar estructura final
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'reportes_generados'
            ORDER BY ordinal_position
        """)
        
        print("\n📋 Estructura final de reportes_generados:")
        for col in cursor.fetchall():
            print(f"   - {col[0]}: {col[1]} (nullable: {col[2]})")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Migración completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    agregar_columnas()
