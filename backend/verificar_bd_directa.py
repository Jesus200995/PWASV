#!/usr/bin/env python3
"""
Script simple para probar solo el endpoint de registro
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import pytz

# Configuración de BD
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"  
DB_USER = "jesus"
DB_PASS = "2025"

CDMX_TZ = pytz.timezone("America/Mexico_City")

def verificar_ultimos_registros():
    """Verificar los últimos registros directamente en la BD"""
    print("🔍 VERIFICANDO ÚLTIMOS REGISTROS EN LA BASE DE DATOS")
    print("-" * 60)
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS,
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        
        # Obtener los últimos 5 registros
        cursor.execute("""
            SELECT id, usuario_id, descripcion, fecha_hora
            FROM registros 
            ORDER BY fecha_hora DESC 
            LIMIT 5
        """)
        
        registros = cursor.fetchall()
        
        if registros:
            print(f"📊 ÚLTIMOS {len(registros)} REGISTROS:")
            print()
            
            for i, reg in enumerate(registros, 1):
                fecha_utc = reg['fecha_hora']
                
                # Si fecha_utc es naive (sin timezone), asumimos UTC
                if fecha_utc.tzinfo is None:
                    fecha_utc = fecha_utc.replace(tzinfo=pytz.UTC)
                
                # Convertir a CDMX
                fecha_cdmx = fecha_utc.astimezone(CDMX_TZ)
                ahora_cdmx = datetime.now(CDMX_TZ)
                diferencia = (ahora_cdmx - fecha_cdmx).total_seconds()
                
                print(f"  {i}. 🆔 ID: {reg['id']}")
                print(f"     👤 Usuario: {reg['usuario_id']}")
                print(f"     📝 Descripción: {reg['descripcion']}")
                print(f"     🌍 Fecha BD (UTC): {fecha_utc}")
                print(f"     🇲🇽 Fecha CDMX: {fecha_cdmx.strftime('%Y-%m-%d %H:%M:%S %Z')}")
                print(f"     ⏰ Hace: {diferencia/60:.1f} minutos")
                print()
        else:
            print("❌ No se encontraron registros")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error conectando a BD: {e}")

def mostrar_tiempo_actual():
    """Mostrar la hora actual en diferentes zonas"""
    print("⏰ TIEMPO ACTUAL EN DIFERENTES ZONAS")
    print("-" * 60)
    
    utc_now = datetime.now(pytz.UTC)
    cdmx_now = datetime.now(CDMX_TZ)
    
    print(f"🌍 UTC: {utc_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"🇲🇽 CDMX: {cdmx_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"📊 Diferencia: {(cdmx_now.utcoffset().total_seconds() / 3600):.0f} horas")
    print()

if __name__ == "__main__":
    mostrar_tiempo_actual()
    verificar_ultimos_registros()
