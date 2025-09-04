#!/usr/bin/env python3
"""
Test directo a la base de datos para verificar cómo se están guardando los timestamps
"""

import psycopg2
from datetime import datetime
import pytz

# Configuración de base de datos
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"

def verificar_timestamps_bd():
    """Verificar directamente en la BD los timestamps guardados"""
    
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()
        
        print("🔍 === VERIFICACIÓN DIRECTA EN BASE DE DATOS ===")
        print()
        
        # Obtener los registros más recientes del usuario 3258
        cursor.execute("""
            SELECT id, usuario_id, descripcion, fecha_hora, tipo_actividad
            FROM registros 
            WHERE usuario_id = 3258 
            AND descripcion LIKE '%Prueba timestamp CDMX%'
            ORDER BY id DESC 
            LIMIT 3
        """)
        
        registros = cursor.fetchall()
        
        if not registros:
            print("❌ No se encontraron registros de prueba")
            return
        
        cdmx_tz = pytz.timezone('America/Mexico_City')
        utc_tz = pytz.UTC
        
        for i, (id_reg, usuario_id, descripcion, fecha_hora, tipo_actividad) in enumerate(registros):
            print(f"📊 REGISTRO #{i+1} (ID: {id_reg})")
            print(f"   👤 Usuario: {usuario_id}")
            print(f"   📝 Descripción: {descripcion}")
            print(f"   🏷️ Tipo: {tipo_actividad}")
            print(f"   💾 Fecha/hora RAW en BD: {fecha_hora}")
            print(f"   📅 Tipo de dato: {type(fecha_hora)}")
            
            if fecha_hora:
                # Si el datetime no tiene timezone info, asumir que es naive
                if fecha_hora.tzinfo is None:
                    print(f"   🔍 Interpretación: Datetime NAIVE (sin timezone)")
                    
                    # Intentar interpretar como UTC
                    fecha_como_utc = fecha_hora.replace(tzinfo=utc_tz)
                    fecha_utc_a_cdmx = fecha_como_utc.astimezone(cdmx_tz)
                    print(f"   🌍 Si es UTC → CDMX: {fecha_utc_a_cdmx.strftime('%H:%M:%S %d/%m/%Y')}")
                    
                    # Intentar interpretar como CDMX
                    fecha_como_cdmx = fecha_hora.replace(tzinfo=cdmx_tz)
                    print(f"   🇲🇽 Si es CDMX → CDMX: {fecha_como_cdmx.strftime('%H:%M:%S %d/%m/%Y')}")
                    
                else:
                    print(f"   🔍 Interpretación: Datetime con timezone: {fecha_hora.tzinfo}")
                    fecha_en_cdmx = fecha_hora.astimezone(cdmx_tz)
                    print(f"   🇲🇽 Convertido a CDMX: {fecha_en_cdmx.strftime('%H:%M:%S %d/%m/%Y')}")
            
            print()
        
        # También verificar asistencias para comparar
        print("🔍 === COMPARACIÓN CON ASISTENCIAS ===")
        
        cursor.execute("""
            SELECT id, usuario_id, fecha, hora_entrada, hora_salida
            FROM asistencias 
            WHERE usuario_id = 3258 
            ORDER BY id DESC 
            LIMIT 2
        """)
        
        asistencias = cursor.fetchall()
        
        for i, (id_asist, usuario_id, fecha, hora_entrada, hora_salida) in enumerate(asistencias):
            print(f"📊 ASISTENCIA #{i+1} (ID: {id_asist})")
            print(f"   📅 Fecha: {fecha}")
            print(f"   🕐 Hora entrada: {hora_entrada} (tipo: {type(hora_entrada)})")
            if hora_salida:
                print(f"   🕐 Hora salida: {hora_salida} (tipo: {type(hora_salida)})")
            print()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_timestamps_bd()
