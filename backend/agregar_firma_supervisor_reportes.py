#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para agregar columnas de firma de supervisor a la tabla reportes_generados
"""

import psycopg2
from psycopg2.extras import RealDictCursor

# Configuración de BD
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"  
DB_USER = "jesus"
DB_PASS = "2025"

try:
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS,
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    
    print("📋 Agregando columnas de firma de supervisor a reportes_generados...")
    
    # Agregar columna firmado_supervisor (boolean)
    try:
        cursor.execute("""
            ALTER TABLE reportes_generados 
            ADD COLUMN IF NOT EXISTS firmado_supervisor BOOLEAN DEFAULT FALSE
        """)
        print("✅ Columna 'firmado_supervisor' agregada")
    except Exception as e:
        print(f"⚠️ Columna firmado_supervisor: {e}")
    
    # Agregar columna fecha_firma_supervisor (timestamp)
    try:
        cursor.execute("""
            ALTER TABLE reportes_generados 
            ADD COLUMN IF NOT EXISTS fecha_firma_supervisor TIMESTAMP
        """)
        print("✅ Columna 'fecha_firma_supervisor' agregada")
    except Exception as e:
        print(f"⚠️ Columna fecha_firma_supervisor: {e}")
    
    # Agregar columna firma_supervisor_base64 (text para guardar la imagen de la firma)
    try:
        cursor.execute("""
            ALTER TABLE reportes_generados 
            ADD COLUMN IF NOT EXISTS firma_supervisor_base64 TEXT
        """)
        print("✅ Columna 'firma_supervisor_base64' agregada")
    except Exception as e:
        print(f"⚠️ Columna firma_supervisor_base64: {e}")
    
    # Agregar columna nombre_supervisor (quien firmó)
    try:
        cursor.execute("""
            ALTER TABLE reportes_generados 
            ADD COLUMN IF NOT EXISTS nombre_supervisor VARCHAR(255)
        """)
        print("✅ Columna 'nombre_supervisor' agregada")
    except Exception as e:
        print(f"⚠️ Columna nombre_supervisor: {e}")
    
    # Agregar columna supervisor_id (ID del admin que firmó)
    try:
        cursor.execute("""
            ALTER TABLE reportes_generados 
            ADD COLUMN IF NOT EXISTS supervisor_id INTEGER
        """)
        print("✅ Columna 'supervisor_id' agregada")
    except Exception as e:
        print(f"⚠️ Columna supervisor_id: {e}")
    
    conn.commit()
    
    # Verificar las columnas
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = 'reportes_generados'
        ORDER BY ordinal_position
    """)
    
    columnas = cursor.fetchall()
    
    print("\n📊 Estructura actual de reportes_generados:")
    print("-" * 60)
    for col in columnas:
        print(f"   {col['column_name']:30} | {col['data_type']:15} | {col['column_default'] or ''}")
    print("-" * 60)
    
    print("\n✅ Columnas de firma de supervisor agregadas exitosamente")
    print("\n📝 Nuevas columnas:")
    print("   - firmado_supervisor: BOOLEAN (indica si fue firmado)")
    print("   - fecha_firma_supervisor: TIMESTAMP (cuándo se firmó)")
    print("   - firma_supervisor_base64: TEXT (imagen de la firma en base64)")
    print("   - nombre_supervisor: VARCHAR(255) (nombre de quien firmó)")
    print("   - supervisor_id: INTEGER (ID del admin que firmó)")
    
    cursor.close()
    conn.close()

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
