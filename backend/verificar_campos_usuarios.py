#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar campos de la tabla usuarios
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
    
    # Ver estructura de la tabla
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name='usuarios' 
        ORDER BY ordinal_position
    """)
    
    columnas = cursor.fetchall()
    
    print("📋 ESTRUCTURA DE LA TABLA USUARIOS:")
    for col in columnas:
        print(f"   - {col['column_name']}: {col['data_type']}")
    
    print("\n👤 EJEMPLO DE UN USUARIO:")
    cursor.execute("""
        SELECT * FROM usuarios LIMIT 1
    """)
    
    usuario = cursor.fetchone()
    if usuario:
        for key, value in usuario.items():
            print(f"   {key}: {value}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
