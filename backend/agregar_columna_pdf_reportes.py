#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para agregar la columna pdf_base64 a la tabla reportes_generados
Esto permite almacenar el PDF generado para su posterior descarga

EJECUTAR EN EL SERVIDOR DE PRODUCCIÓN:
    python agregar_columna_pdf_reportes.py
"""

import psycopg2
from psycopg2.extras import RealDictCursor

# Configuración de BD - Usar localhost si se ejecuta en el servidor
# Para ejecución local, usar la IP del servidor
import sys

# Detectar si estamos en el servidor (localhost) o en desarrollo
if len(sys.argv) > 1 and sys.argv[1] == '--local':
    DB_HOST = "localhost"
else:
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
    
    print("📋 Verificando estructura de tabla reportes_generados...")
    
    # Verificar si la columna ya existe
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'reportes_generados' AND column_name = 'pdf_base64'
    """)
    
    if cursor.fetchone():
        print("✅ La columna pdf_base64 ya existe")
    else:
        print("📝 Agregando columna pdf_base64...")
        cursor.execute("""
            ALTER TABLE reportes_generados 
            ADD COLUMN pdf_base64 TEXT
        """)
        conn.commit()
        print("✅ Columna pdf_base64 agregada exitosamente")
    
    # Mostrar estructura actual
    cursor.execute("""
        SELECT column_name, data_type, character_maximum_length
        FROM information_schema.columns 
        WHERE table_name = 'reportes_generados'
        ORDER BY ordinal_position
    """)
    
    columnas = cursor.fetchall()
    print("\n📊 Estructura actual de la tabla reportes_generados:")
    for col in columnas:
        tipo = col['data_type']
        if col['character_maximum_length']:
            tipo += f"({col['character_maximum_length']})"
        print(f"   - {col['column_name']}: {tipo}")
    
    cursor.close()
    conn.close()
    print("\n✅ Script completado exitosamente")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
