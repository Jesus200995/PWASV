#!/usr/bin/env python3
"""
Script para configurar una base de datos PostgreSQL local como respaldo
para el sistema PWA.

Este script:
1. Crea la base de datos local si no existe
2. Crea las tablas necesarias
3. Configura un usuario administrador por defecto

Uso:
    python setup_local_db.py

Requisitos:
- PostgreSQL instalado localmente
- Usuario postgres con acceso
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
from passlib.context import CryptContext

# Configuración de la base de datos local
LOCAL_DB_CONFIG = {
    "host": "localhost",
    "user": "postgres", 
    "password": "admin",
    "database": "app_registros_local"
}

# Configuración para autenticación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def crear_base_datos():
    """Crear la base de datos local si no existe"""
    try:
        # Conectar a postgres para crear la nueva base de datos
        conn = psycopg2.connect(
            host=LOCAL_DB_CONFIG["host"],
            user=LOCAL_DB_CONFIG["user"],
            password=LOCAL_DB_CONFIG["password"],
            database="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar si la base de datos ya existe
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (LOCAL_DB_CONFIG["database"],)
        )
        
        if cursor.fetchone():
            print(f"✅ Base de datos '{LOCAL_DB_CONFIG['database']}' ya existe")
        else:
            # Crear la base de datos
            cursor.execute(f"CREATE DATABASE {LOCAL_DB_CONFIG['database']}")
            print(f"✅ Base de datos '{LOCAL_DB_CONFIG['database']}' creada exitosamente")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error creando base de datos: {e}")
        return False
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

def crear_tablas():
    """Crear las tablas necesarias en la base de datos local"""
    try:
        # Conectar a la nueva base de datos
        conn = psycopg2.connect(
            host=LOCAL_DB_CONFIG["host"],
            user=LOCAL_DB_CONFIG["user"],
            password=LOCAL_DB_CONFIG["password"],
            database=LOCAL_DB_CONFIG["database"]
        )
        cursor = conn.cursor()
        
        # Tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                correo VARCHAR(255) UNIQUE NOT NULL,
                nombre_completo VARCHAR(255) NOT NULL,
                cargo VARCHAR(255) NOT NULL,
                supervisor VARCHAR(255),
                contrasena VARCHAR(255) NOT NULL,
                curp VARCHAR(18) UNIQUE,
                telefono VARCHAR(20),
                rol VARCHAR(10) DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabla 'usuarios' creada/verificada")
        
        # Tabla de admin_users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                rol VARCHAR(20) DEFAULT 'admin' CHECK (rol IN ('admin', 'user')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabla 'admin_users' creada/verificada")
        
        # Tabla de registros
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registros (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
                latitud DECIMAL(10, 8) NOT NULL,
                longitud DECIMAL(11, 8) NOT NULL,
                descripcion TEXT,
                foto_url VARCHAR(500),
                fecha_hora TIMESTAMP NOT NULL,
                tipo_actividad VARCHAR(20) DEFAULT 'campo' CHECK (tipo_actividad IN ('campo', 'gabinete')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabla 'registros' creada/verificada")
        
        # Tabla de asistencias
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS asistencias (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
                fecha DATE NOT NULL,
                hora_entrada TIMESTAMP,
                hora_salida TIMESTAMP,
                latitud_entrada DECIMAL(10, 8),
                longitud_entrada DECIMAL(11, 8),
                latitud_salida DECIMAL(10, 8),
                longitud_salida DECIMAL(11, 8),
                foto_entrada_url VARCHAR(500),
                foto_salida_url VARCHAR(500),
                descripcion_entrada TEXT,
                descripcion_salida TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(usuario_id, fecha)
            )
        """)
        print("✅ Tabla 'asistencias' creada/verificada")
        
        # Tabla de términos de usuario
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios_terminos (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
                aceptado BOOLEAN DEFAULT FALSE,
                fecha_aceptado TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(usuario_id)
            )
        """)
        print("✅ Tabla 'usuarios_terminos' creada/verificada")
        
        # Tabla de notificaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notificaciones (
                id SERIAL PRIMARY KEY,
                titulo VARCHAR(255) NOT NULL,
                subtitulo VARCHAR(255),
                descripcion TEXT,
                enlace_url VARCHAR(500),
                archivo_nombre VARCHAR(255),
                archivo_tipo VARCHAR(100),
                enviada_a_todos BOOLEAN DEFAULT TRUE,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_envio TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabla 'notificaciones' creada/verificada")
        
        # Tabla de notificaciones leídas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notificaciones_leidas (
                id SERIAL PRIMARY KEY,
                notificacion_id INTEGER REFERENCES notificaciones(id) ON DELETE CASCADE,
                usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
                device_id VARCHAR(255),
                fecha_leida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(notificacion_id, usuario_id, device_id)
            )
        """)
        print("✅ Tabla 'notificaciones_leidas' creada/verificada")
        
        # Crear índices para optimizar consultas
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_registros_usuario_fecha ON registros(usuario_id, fecha_hora)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_asistencias_usuario_fecha ON asistencias(usuario_id, fecha)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_usuarios_correo ON usuarios(correo)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_usuarios_curp ON usuarios(curp)")
        print("✅ Índices creados/verificados")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Todas las tablas e índices fueron creados exitosamente")
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error creando tablas: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False
    except Exception as e:
        print(f"❌ Error general: {e}")
        if conn:
            conn.close()
        return False

def crear_usuario_admin():
    """Crear usuario administrador por defecto"""
    try:
        conn = psycopg2.connect(
            host=LOCAL_DB_CONFIG["host"],
            user=LOCAL_DB_CONFIG["user"],
            password=LOCAL_DB_CONFIG["password"],
            database=LOCAL_DB_CONFIG["database"]
        )
        cursor = conn.cursor()
        
        # Verificar si ya existe un usuario admin
        cursor.execute("SELECT COUNT(*) FROM admin_users")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Crear usuario admin por defecto
            default_password = pwd_context.hash("admin123")
            cursor.execute(
                "INSERT INTO admin_users (username, password, rol) VALUES (%s, %s, %s)",
                ("admin", default_password, "admin")
            )
            conn.commit()
            print("✅ Usuario administrador creado: admin/admin123")
        else:
            print("✅ Usuario administrador ya existe")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error creando usuario admin: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False
    except Exception as e:
        print(f"❌ Error general: {e}")
        if conn:
            conn.close()
        return False

def main():
    """Función principal"""
    print("🚀 Configurando base de datos local de respaldo...")
    print(f"📍 Host: {LOCAL_DB_CONFIG['host']}")
    print(f"📊 Base de datos: {LOCAL_DB_CONFIG['database']}")
    print("-" * 50)
    
    # Paso 1: Crear base de datos
    print("📝 Paso 1: Creando base de datos...")
    if not crear_base_datos():
        print("❌ Error creando base de datos. Abortando.")
        sys.exit(1)
    
    # Paso 2: Crear tablas
    print("\n📝 Paso 2: Creando tablas...")
    if not crear_tablas():
        print("❌ Error creando tablas. Abortando.")
        sys.exit(1)
    
    # Paso 3: Crear usuario admin
    print("\n📝 Paso 3: Creando usuario administrador...")
    if not crear_usuario_admin():
        print("❌ Error creando usuario admin. Abortando.")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ CONFIGURACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 50)
    print("📊 Base de datos local configurada y lista para usar")
    print(f"🔗 Conexión: {LOCAL_DB_CONFIG['host']}:{LOCAL_DB_CONFIG['database']}")
    print("👤 Usuario admin: admin")
    print("🔑 Contraseña admin: admin123")
    print("\n💡 Para usar esta base de datos como respaldo:")
    print("   1. Asegúrate de que PostgreSQL esté ejecutándose localmente")
    print("   2. La API automáticamente usará esta DB si la principal falla")
    print("   3. Usa el endpoint /diagnostico para verificar el estado")

if __name__ == "__main__":
    main()
