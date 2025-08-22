#!/usr/bin/env python3
"""
Verificar usuarios disponibles
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
    
    # Obtener algunos usuarios
    cursor.execute("""
        SELECT id, nombre_completo 
        FROM usuarios 
        ORDER BY id 
        LIMIT 10
    """)
    
    usuarios = cursor.fetchall()
    
    print("👥 USUARIOS DISPONIBLES:")
    for usuario in usuarios:
        print(f"   🆔 ID: {usuario['id']} - {usuario['nombre_completo']}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
