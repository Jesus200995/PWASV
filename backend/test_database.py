#!/usr/bin/env python3
"""
Script para probar la funcionalidad de notificaciones directamente en la base de datos
"""

import psycopg2
import json
from datetime import datetime

# Configuración de conexión (igual que en main.py)
DATABASE_CONFIG = {
    "host": "localhost",
    "database": "asistencias_db",
    "user": "postgres",
    "password": "12345678",
    "port": "5432"
}

def test_database_notifications():
    """Probar inserción directa de notificaciones"""
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()
        
        print("✅ Conectado a la base de datos")
        
        # 1. Verificar que las tablas existen
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name LIKE '%notification%'
        """)
        
        tables = cursor.fetchall()
        print(f"📋 Tablas de notificaciones encontradas: {[t[0] for t in tables]}")
        
        # 2. Insertar una notificación de prueba
        cursor.execute("""
            INSERT INTO notifications (title, body, type, audience, metadata, status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
            RETURNING id
        """, (
            "Notificación de Prueba DB",
            "Esta notificación se creó directamente en la base de datos",
            "info",
            "all",
            json.dumps({"test": True}),
            "draft"
        ))
        
        notification_id = cursor.fetchone()[0]
        conn.commit()
        
        print(f"✅ Notificación creada con ID: {notification_id}")
        
        # 3. Leer la notificación
        cursor.execute("""
            SELECT id, title, body, type, audience, status, created_at
            FROM notifications
            WHERE id = %s
        """, (notification_id,))
        
        notif = cursor.fetchone()
        print(f"📄 Notificación leída: {notif[1]} - {notif[2][:50]}...")
        
        # 4. Contar notificaciones totales
        cursor.execute("SELECT COUNT(*) FROM notifications")
        total = cursor.fetchone()[0]
        print(f"📊 Total de notificaciones en BD: {total}")
        
        # 5. Verificar usuarios para targets
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        users = cursor.fetchone()[0]
        print(f"👥 Total de usuarios disponibles: {users}")
        
        cursor.close()
        conn.close()
        
        print("✅ Prueba de base de datos completada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba de BD: {e}")
        return False

def test_vapid_keys():
    """Probar generación de claves VAPID"""
    try:
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import serialization
        import base64
        
        # Generar claves VAPID
        private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        public_key = private_key.public_key()
        
        # Serializar claves
        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        print("✅ Claves VAPID generadas correctamente")
        print(f"   Private Key: {len(private_key_bytes)} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generando claves VAPID: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Iniciando pruebas de funcionalidad...")
    print("=" * 50)
    
    # Probar base de datos
    print("\n1. PROBANDO BASE DE DATOS")
    db_ok = test_database_notifications()
    
    # Probar VAPID
    print("\n2. PROBANDO GENERACIÓN VAPID")
    vapid_ok = test_vapid_keys()
    
    print("\n" + "=" * 50)
    if db_ok and vapid_ok:
        print("✅ TODAS LAS PRUEBAS PASARON - El sistema de notificaciones está listo")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON - Revisar configuración")
