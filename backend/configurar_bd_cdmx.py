#!/usr/bin/env python3
"""
Script para verificar y configurar PostgreSQL para zona horaria CDMX
"""

import psycopg2
from datetime import datetime
import pytz

# Configuración de base de datos
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"

CDMX_TZ = pytz.timezone("America/Mexico_City")

def verificar_bd():
    """Verifica la configuración de la base de datos"""
    print("=== VERIFICACIÓN DE BASE DE DATOS ===")
    
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa a PostgreSQL")
        
        # Verificar timezone actual del servidor
        cursor.execute("SHOW timezone;")
        server_tz = cursor.fetchone()[0]
        print(f"🌍 Timezone del servidor PostgreSQL: {server_tz}")
        
        # Configurar timezone para esta sesión
        cursor.execute("SET timezone = 'America/Mexico_City';")
        conn.commit()
        print("✅ Timezone configurado para esta sesión: America/Mexico_City")
        
        # Verificar timezone de la sesión
        cursor.execute("SHOW timezone;")
        session_tz = cursor.fetchone()[0]
        print(f"🌍 Timezone de la sesión actual: {session_tz}")
        
        # Verificar estructura de la tabla registros
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'registros' AND column_name = 'fecha_hora';
        """)
        
        column_info = cursor.fetchone()
        if column_info:
            print(f"📅 Columna fecha_hora: {column_info[1]} (nullable: {column_info[2]})")
            
            if "timestamp" in column_info[1].lower():
                if "with time zone" in column_info[1].lower():
                    print("✅ La columna fecha_hora es timestamp WITH time zone")
                else:
                    print("⚠️ La columna fecha_hora es timestamp WITHOUT time zone")
                    print("   Recomendación: Cambiar a timestamp WITH time zone")
            else:
                print(f"❌ La columna fecha_hora no es de tipo timestamp: {column_info[1]}")
        else:
            print("❌ No se encontró la columna fecha_hora en la tabla registros")
        
        # Probar inserción y consulta de fecha
        print("\n=== PRUEBA DE FECHA ===")
        
        # Obtener fecha actual en CDMX
        fecha_cdmx = datetime.now(CDMX_TZ)
        print(f"🕐 Fecha CDMX para prueba: {fecha_cdmx}")
        
        # Probar insertar fecha usando NOW() de PostgreSQL
        cursor.execute("SELECT NOW();")
        pg_now = cursor.fetchone()[0]
        print(f"🕐 PostgreSQL NOW(): {pg_now}")
        
        # Verificar que ambas fechas estén en la misma zona horaria
        if pg_now.tzinfo and fecha_cdmx.tzinfo:
            offset_pg = pg_now.utcoffset().total_seconds() / 3600
            offset_cdmx = fecha_cdmx.utcoffset().total_seconds() / 3600
            print(f"⏰ Offset PostgreSQL: UTC{offset_pg:+.0f}")
            print(f"⏰ Offset Python CDMX: UTC{offset_cdmx:+.0f}")
            
            if abs(offset_pg - offset_cdmx) < 1:  # Menos de 1 hora de diferencia
                print("✅ Los offsets coinciden - configuración correcta")
            else:
                print("❌ Los offsets no coinciden - revisar configuración")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def crear_tabla_si_no_existe():
    """Crea la tabla registros si no existe con el tipo correcto"""
    print("\n=== VERIFICACIÓN/CREACIÓN DE TABLA ===")
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cursor = conn.cursor()
        
        # Configurar timezone
        cursor.execute("SET timezone = 'America/Mexico_City';")
        
        # Verificar si la tabla existe
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'registros'
            );
        """)
        
        tabla_existe = cursor.fetchone()[0]
        
        if not tabla_existe:
            print("📝 Creando tabla registros...")
            cursor.execute("""
                CREATE TABLE registros (
                    id SERIAL PRIMARY KEY,
                    usuario_id INTEGER NOT NULL,
                    latitud DECIMAL(10, 8),
                    longitud DECIMAL(11, 8),
                    descripcion TEXT,
                    foto_url VARCHAR(255),
                    fecha_hora TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """)
            conn.commit()
            print("✅ Tabla registros creada con timestamp WITH time zone")
        else:
            print("✅ La tabla registros ya existe")
            
            # Verificar si necesita ser actualizada
            cursor.execute("""
                SELECT data_type 
                FROM information_schema.columns 
                WHERE table_name = 'registros' AND column_name = 'fecha_hora';
            """)
            
            tipo_actual = cursor.fetchone()[0]
            if "without time zone" in tipo_actual.lower():
                print("⚠️ Actualizando columna fecha_hora a timestamp WITH time zone...")
                cursor.execute("""
                    ALTER TABLE registros 
                    ALTER COLUMN fecha_hora TYPE TIMESTAMP WITH TIME ZONE 
                    USING fecha_hora AT TIME ZONE 'America/Mexico_City';
                """)
                conn.commit()
                print("✅ Columna actualizada")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creando/verificando tabla: {e}")
        return False

def main():
    """Función principal"""
    print("CONFIGURACIÓN DE BASE DE DATOS PARA CDMX")
    print("=" * 50)
    
    bd_ok = verificar_bd()
    tabla_ok = crear_tabla_si_no_existe()
    
    if bd_ok and tabla_ok:
        print("\n🎉 ¡Base de datos configurada correctamente!")
        print("\nInstrucciones:")
        print("1. La base de datos está configurada para America/Mexico_City")
        print("2. La tabla registros usa timestamp WITH time zone")
        print("3. Todas las fechas se guardarán en horario CDMX")
        print("4. Reinicia el backend para aplicar los cambios")
    else:
        print("\n❌ Hay problemas en la configuración de la base de datos")

if __name__ == "__main__":
    main()
