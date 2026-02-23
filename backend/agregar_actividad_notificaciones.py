#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para agregar campos de vinculación entre notificaciones y actividades
"""

import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de base de datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'pwasv'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '')
}

def aplicar_cambios():
    """Aplica los cambios de esquema a la base de datos"""
    try:
        print("🔄 Conectando a la base de datos...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("\n📋 Aplicando cambios al esquema...")
        
        # 1. Agregar campo actividad_id
        print("  ➤ Agregando campo actividad_id...")
        cursor.execute("""
            ALTER TABLE notificaciones 
            ADD COLUMN IF NOT EXISTS actividad_id INTEGER 
            REFERENCES reportes_generados(id) ON DELETE SET NULL
        """)
        
        # 2. Agregar campo motivos_atencion
        print("  ➤ Agregando campo motivos_atencion...")
        cursor.execute("""
            ALTER TABLE notificaciones 
            ADD COLUMN IF NOT EXISTS motivos_atencion TEXT[]
        """)
        
        # 3. Crear índice
        print("  ➤ Creando índice...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_notificaciones_actividad 
            ON notificaciones(actividad_id) 
            WHERE actividad_id IS NOT NULL
        """)
        
        # 4. Agregar comentarios
        print("  ➤ Agregando comentarios...")
        cursor.execute("""
            COMMENT ON COLUMN notificaciones.actividad_id IS 
            'ID del reporte/actividad vinculado a esta notificación (para notificaciones contextuales)'
        """)
        cursor.execute("""
            COMMENT ON COLUMN notificaciones.motivos_atencion IS 
            'Array de motivos por los que se envía la notificación (ej: ["Llamar atención", "Corrección requerida"])'
        """)
        
        conn.commit()
        print("\n✅ Cambios aplicados exitosamente!")
        
        # Verificar estructura
        print("\n📊 Estructura actualizada de la tabla notificaciones:")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'notificaciones' 
            AND column_name IN ('actividad_id', 'motivos_atencion')
            ORDER BY ordinal_position
        """)
        
        for row in cursor.fetchall():
            print(f"  • {row[0]:<20} | {row[1]:<15} | Nullable: {row[2]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        raise

if __name__ == "__main__":
    print("="*60)
    print("AGREGAR CAMPOS PARA NOTIFICACIONES DE ACTIVIDADES")
    print("="*60)
    aplicar_cambios()
    print("\n" + "="*60)
    print("✅ PROCESO COMPLETADO")
    print("="*60)
