#!/usr/bin/env python3
"""
Prueba manual de registro directo en BD para verificar timestamp
"""

import psycopg2
from datetime import datetime
import pytz

# Configuración de BD
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"  
DB_USER = "jesus"
DB_PASS = "2025"

CDMX_TZ = pytz.timezone("America/Mexico_City")

def registrar_actividad_manual_cdmx():
    """Registrar una actividad de prueba con timestamp CDMX"""
    print("📝 REGISTRANDO ACTIVIDAD MANUAL CON TIMESTAMP CDMX")
    print("-" * 60)
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cursor = conn.cursor()
        
        # Obtener tiempo actual CDMX
        ahora_cdmx = datetime.now(CDMX_TZ)
        # Convertir a UTC para guardar en BD
        ahora_utc = ahora_cdmx.astimezone(pytz.UTC).replace(tzinfo=None)
        
        print(f"⏰ Tiempo CDMX: {ahora_cdmx.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        print(f"🌍 Tiempo UTC para BD: {ahora_utc}")
        
        # Insertar registro de prueba
        cursor.execute("""
            INSERT INTO registros (usuario_id, latitud, longitud, descripcion, foto_url, fecha_hora) 
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            93,  # usuario_id de prueba (Jess)
            19.432608,  # latitud CDMX
            -99.133209,  # longitud CDMX
            f"TEST MANUAL TIMESTAMP CDMX - {ahora_cdmx.strftime('%H:%M:%S')}",
            "test_manual.jpg",
            ahora_utc
        ))
        
        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        
        print(f"✅ Registro insertado con ID: {nuevo_id}")
        
        # Verificar el registro recién insertado
        cursor.execute("""
            SELECT id, descripcion, fecha_hora
            FROM registros 
            WHERE id = %s
        """, (nuevo_id,))
        
        registro = cursor.fetchone()
        if registro:
            fecha_bd = registro[2]
            if fecha_bd.tzinfo is None:
                fecha_bd = fecha_bd.replace(tzinfo=pytz.UTC)
            
            fecha_cdmx_recuperada = fecha_bd.astimezone(CDMX_TZ)
            diferencia = (ahora_cdmx - fecha_cdmx_recuperada).total_seconds()
            
            print(f"📊 VERIFICACIÓN DEL REGISTRO:")
            print(f"   🆔 ID: {registro[0]}")
            print(f"   📝 Descripción: {registro[1]}")
            print(f"   🌍 En BD (UTC): {fecha_bd}")
            print(f"   🇲🇽 Convertido a CDMX: {fecha_cdmx_recuperada.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            print(f"   ⏰ Diferencia: {diferencia:.1f} segundos")
            
            if abs(diferencia) < 5:  # Menos de 5 segundos de diferencia
                print("✅ TIMESTAMP CORRECTO - Se guardó en horario CDMX")
            else:
                print("❌ TIMESTAMP INCORRECTO - Diferencia mayor a 5 segundos")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    registrar_actividad_manual_cdmx()
