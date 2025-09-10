import mysql.connector
from datetime import datetime, timedelta
import os

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'sistema_asistencias'
}

def verificar_datos_gabinete():
    """Verifica los datos de gabinete en la base de datos"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        print("🔍 VERIFICANDO DATOS DE GABINETE...")
        print("=" * 50)
        
        # 1. Verificar tabla actividades con tipo 'gabinete'
        print("\n1. REGISTROS EN TABLA 'actividades' CON TIPO 'gabinete':")
        cursor.execute("""
            SELECT id, usuario_id, tipo_actividad, coordenadas, fecha_hora, created_at
            FROM actividades 
            WHERE tipo_actividad = 'gabinete'
            ORDER BY fecha_hora DESC
            LIMIT 10
        """)
        actividades = cursor.fetchall()
        
        if actividades:
            print(f"   Encontrados {len(actividades)} registros de gabinete:")
            for act in actividades:
                print(f"   - ID: {act[0]}, Usuario: {act[1]}, Fecha: {act[4]}, Coords: {act[2]}")
        else:
            print("   ❌ No se encontraron registros de gabinete en la tabla 'actividades'")
        
        # 2. Verificar tabla registros con tipo 'gabinete'
        print("\n2. REGISTROS EN TABLA 'registros' CON TIPO 'gabinete':")
        cursor.execute("""
            SELECT id, usuario_id, tipo_actividad, coordenadas, fecha_hora, created_at
            FROM registros 
            WHERE tipo_actividad = 'gabinete'
            ORDER BY fecha_hora DESC
            LIMIT 10
        """)
        registros = cursor.fetchall()
        
        if registros:
            print(f"   Encontrados {len(registros)} registros de gabinete:")
            for reg in registros:
                print(f"   - ID: {reg[0]}, Usuario: {reg[1]}, Fecha: {reg[4]}, Coords: {reg[2]}")
        else:
            print("   ❌ No se encontraron registros de gabinete en la tabla 'registros'")
        
        # 3. Verificar todos los tipos de actividad únicos
        print("\n3. TIPOS DE ACTIVIDAD ÚNICOS EN LA BASE DE DATOS:")
        cursor.execute("SELECT DISTINCT tipo_actividad FROM actividades WHERE tipo_actividad IS NOT NULL")
        tipos_actividades = cursor.fetchall()
        print("   Tabla 'actividades':", [tipo[0] for tipo in tipos_actividades])
        
        cursor.execute("SELECT DISTINCT tipo_actividad FROM registros WHERE tipo_actividad IS NOT NULL")
        tipos_registros = cursor.fetchall()
        print("   Tabla 'registros':", [tipo[0] for tipo in tipos_registros])
        
        # 4. Verificar los últimos registros de cualquier tipo
        print("\n4. ÚLTIMOS 10 REGISTROS DE CUALQUIER TIPO (para verificar estructura):")
        cursor.execute("""
            SELECT id, usuario_id, tipo_actividad, coordenadas, fecha_hora, created_at
            FROM registros 
            ORDER BY fecha_hora DESC
            LIMIT 10
        """)
        ultimos = cursor.fetchall()
        
        for registro in ultimos:
            print(f"   - ID: {registro[0]}, Usuario: {registro[1]}, Tipo: {registro[2]}, Fecha: {registro[4]}")
        
        # 5. Verificar si hay columnas adicionales que puedan indicar gabinete
        print("\n5. ESTRUCTURA DE LAS TABLAS:")
        cursor.execute("DESCRIBE registros")
        columnas_registros = cursor.fetchall()
        print("   Columnas en 'registros':")
        for col in columnas_registros:
            print(f"   - {col[0]} ({col[1]})")
        
        cursor.execute("DESCRIBE actividades")
        columnas_actividades = cursor.fetchall()
        print("   Columnas en 'actividades':")
        for col in columnas_actividades:
            print(f"   - {col[0]} ({col[1]})")
        
        print("\n" + "=" * 50)
        print("✅ VERIFICACIÓN COMPLETADA")
        
    except mysql.connector.Error as err:
        print(f"❌ Error de base de datos: {err}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    verificar_datos_gabinete()
