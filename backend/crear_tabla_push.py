#!/usr/bin/env python3
"""
Script para crear la tabla de suscripciones push
"""

import sqlite3
import os

def crear_tabla_push_subscriptions():
    """Crea la tabla de suscripciones push en la base de datos"""
    
    db_path = 'sembrando_vida_asistencias.db'
    
    print(f"🔍 Buscando base de datos: {db_path}")
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada en: {os.path.abspath(db_path)}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear tabla push_subscriptions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS push_subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                endpoint TEXT NOT NULL,
                p256dh TEXT NOT NULL,
                auth TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # Crear índices para mejorar rendimiento
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_push_user_id ON push_subscriptions(user_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_push_active ON push_subscriptions(is_active)
        ''')
        
        conn.commit()
        
        # Verificar que la tabla se creó correctamente
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='push_subscriptions'")
        if cursor.fetchone():
            print("✅ Tabla push_subscriptions creada exitosamente")
            
            # Mostrar estructura de la tabla
            cursor.execute("PRAGMA table_info(push_subscriptions)")
            columns = cursor.fetchall()
            print("📊 Estructura de la tabla:")
            for col in columns:
                print(f"   - {col[1]} ({col[2]})")
            
            return True
        else:
            print("❌ Error: No se pudo crear la tabla")
            return False
            
    except Exception as e:
        print(f"❌ Error creando tabla: {e}")
        return False
    finally:
        conn.close()

def verificar_tablas_existentes():
    """Verifica qué tablas existen en la base de datos"""
    
    db_path = 'sembrando_vida_asistencias.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        print("\n📋 Tablas existentes en la base de datos:")
        for table in tables:
            print(f"   - {table[0]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")

if __name__ == "__main__":
    print("🚀 Creando tabla de suscripciones push...")
    print("=" * 50)
    
    # Verificar tablas existentes
    verificar_tablas_existentes()
    
    # Crear tabla push_subscriptions
    if crear_tabla_push_subscriptions():
        print("\n✅ ¡Tabla creada exitosamente!")
        
        # Verificar nuevamente
        verificar_tablas_existentes()
        
        print("\n📋 La tabla está lista para usar con el sistema de notificaciones push")
    else:
        print("\n❌ Error creando la tabla")
