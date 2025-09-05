#!/usr/bin/env python3
"""
Script simple para diagnosticar problemas de conexión PostgreSQL
"""

import psycopg2
import sys

def test_postgres_connection():
    """Probar diferentes configuraciones de PostgreSQL"""
    
    # Configuraciones a probar
    configs = [
        {
            "name": "PostgreSQL Default (postgres/admin)",
            "host": "localhost",
            "user": "postgres", 
            "password": "admin",
            "database": "postgres"
        },
        {
            "name": "PostgreSQL Default (postgres/postgres)",
            "host": "localhost",
            "user": "postgres", 
            "password": "postgres",
            "database": "postgres"
        },
        {
            "name": "PostgreSQL Default (postgres/sin password)",
            "host": "localhost",
            "user": "postgres", 
            "password": "",
            "database": "postgres"
        }
    ]
    
    print("🔍 Diagnosticando conexiones PostgreSQL...")
    print("=" * 50)
    
    for config in configs:
        print(f"\n🧪 Probando: {config['name']}")
        print(f"   Host: {config['host']}")
        print(f"   Usuario: {config['user']}")
        print(f"   Base de datos: {config['database']}")
        
        try:
            conn = psycopg2.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                database=config['database'],
                connect_timeout=5
            )
            cursor = conn.cursor()
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            
            print(f"   ✅ ÉXITO - PostgreSQL conectado")
            print(f"   📝 Versión: {version}")
            
            # Listar bases de datos existentes
            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false")
            databases = cursor.fetchall()
            print(f"   📊 Bases de datos disponibles:")
            for db in databases:
                print(f"      - {db[0]}")
            
            cursor.close()
            conn.close()
            
            print(f"   🎯 CONFIGURACIÓN VÁLIDA ENCONTRADA!")
            return config
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue
    
    print("\n❌ No se pudo conectar con ninguna configuración")
    return None

def check_postgresql_service():
    """Verificar si PostgreSQL está ejecutándose"""
    print("\n🔍 Verificando servicio PostgreSQL...")
    
    try:
        import subprocess
        
        # Verificar si PostgreSQL está ejecutándose
        result = subprocess.run(
            ["sc", "query", "postgresql"], 
            capture_output=True, 
            text=True, 
            shell=True
        )
        
        if "RUNNING" in result.stdout:
            print("✅ Servicio PostgreSQL está ejecutándose")
        else:
            print("❌ Servicio PostgreSQL no está ejecutándose")
            print("💡 Intenta iniciarlo con: net start postgresql")
            
    except Exception as e:
        print(f"⚠️ No se pudo verificar el servicio: {e}")

def main():
    print("🚀 DIAGNÓSTICO DE POSTGRESQL")
    print("=" * 50)
    
    # Verificar servicio
    check_postgresql_service()
    
    # Probar conexiones
    valid_config = test_postgres_connection()
    
    if valid_config:
        print("\n" + "=" * 50)
        print("✅ DIAGNÓSTICO EXITOSO")
        print("=" * 50)
        print("📋 Configuración válida encontrada:")
        print(f"   Host: {valid_config['host']}")
        print(f"   Usuario: {valid_config['user']}")
        print(f"   Contraseña: {'(vacía)' if not valid_config['password'] else valid_config['password']}")
        print(f"   Base de datos: {valid_config['database']}")
        
        print("\n💡 Para usar esta configuración:")
        print("   1. Actualiza DB_CONFIGS en main.py con estos valores")
        print("   2. Ejecuta setup_local_db.py con la configuración correcta")
        
    else:
        print("\n" + "=" * 50)
        print("❌ DIAGNÓSTICO FALLIDO")
        print("=" * 50)
        print("🔧 Posibles soluciones:")
        print("   1. Instalar PostgreSQL: https://www.postgresql.org/download/")
        print("   2. Verificar que el servicio esté ejecutándose")
        print("   3. Verificar usuario y contraseña")
        print("   4. Verificar firewall y configuración de pg_hba.conf")

if __name__ == "__main__":
    main()
