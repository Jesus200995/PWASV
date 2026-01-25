#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear la tabla de reportes generados
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
    
    print("📋 Creando tabla reportes_generados...")
    
    # Crear tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reportes_generados (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER NOT NULL,
            nombre_reporte VARCHAR(255) NOT NULL,
            mes VARCHAR(20),
            anio INTEGER,
            tipo VARCHAR(10) NOT NULL,
            fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    """)
    
    # Crear índice para búsquedas rápidas
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_reportes_usuario 
        ON reportes_generados(usuario_id, fecha_generacion DESC)
    """)
    
    conn.commit()
    
    print("✅ Tabla reportes_generados creada exitosamente")
    print("📊 Estructura:")
    print("   - id: SERIAL PRIMARY KEY")
    print("   - usuario_id: INTEGER (FK a usuarios)")
    print("   - nombre_reporte: VARCHAR(255)")
    print("   - mes: VARCHAR(20)")
    print("   - anio: INTEGER")
    print("   - tipo: VARCHAR(10) - PDF o CSV")
    print("   - fecha_generacion: TIMESTAMP")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
