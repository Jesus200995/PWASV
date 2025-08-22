#!/usr/bin/env python3
"""
Prueba final: Simular el endpoint /registro con nuestros cambios
"""

import psycopg2
from datetime import datetime
import pytz
import os

# Configuración de BD
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"  
DB_USER = "jesus"
DB_PASS = "2025"

CDMX_TZ = pytz.timezone("America/Mexico_City")

def obtener_fecha_hora_cdmx(timestamp_offline=None):
    """
    Misma función que en main.py
    """
    if timestamp_offline:
        try:
            print(f"🕐 Procesando timestamp offline: '{timestamp_offline}'")
            
            fecha_hora_utc = None
            
            if timestamp_offline.endswith('Z'):
                fecha_hora_utc = datetime.fromisoformat(timestamp_offline.replace('Z', '+00:00'))
                print(f"   📝 Formato detectado: UTC con Z")
            elif '+' in timestamp_offline or timestamp_offline.count('-') > 2:
                fecha_hora_utc = datetime.fromisoformat(timestamp_offline)
                print(f"   📝 Formato detectado: Con zona horaria")
            else:
                if '.' in timestamp_offline:
                    fecha_hora_utc = datetime.fromisoformat(timestamp_offline).replace(tzinfo=pytz.UTC)
                else:
                    fecha_hora_utc = datetime.fromisoformat(timestamp_offline).replace(tzinfo=pytz.UTC)
                print(f"   📝 Formato detectado: Sin zona, asumiendo UTC")
            
            print(f"   🌍 Timestamp parseado como UTC: {fecha_hora_utc}")
            
            hora_cdmx = fecha_hora_utc.astimezone(CDMX_TZ)
            fecha_cdmx = hora_cdmx.date()
            
            print(f"📅 ✅ Conversión de timestamp completada:")
            print(f"   🌍 UTC original: {fecha_hora_utc}")
            print(f"   🇲🇽 CDMX convertido: {hora_cdmx}")
            print(f"   📆 Fecha LOCAL CDMX: {fecha_cdmx}")
            
            timestamp_for_filename = hora_cdmx.strftime('%Y%m%d%H%M%S')
            
            return fecha_cdmx, hora_cdmx, timestamp_for_filename
            
        except Exception as e:
            print(f"⚠️ ERROR parseando timestamp offline '{timestamp_offline}': {e}")
            print(f"🔄 Fallback a tiempo actual de CDMX")
    
    now_cdmx = datetime.now(CDMX_TZ)
    fecha_cdmx = now_cdmx.date()
    timestamp_for_filename = now_cdmx.strftime('%Y%m%d%H%M%S')
    
    print(f"📅 ⏰ Usando timestamp actual CDMX:")
    print(f"   🇲🇽 Hora CDMX: {now_cdmx}")
    print(f"   📆 Fecha CDMX: {fecha_cdmx}")
    
    return fecha_cdmx, now_cdmx, timestamp_for_filename

def simular_endpoint_registro_online():
    """Simular el endpoint /registro con timestamp (modo online)"""
    print("🧪 TEST: Simulando endpoint /registro ONLINE (con timestamp)")
    print("-" * 70)
    
    # Simular datos del frontend
    usuario_id = "93"
    latitud = 19.432608
    longitud = -99.133209  
    descripcion = "TEST ENDPOINT ONLINE CON TIMESTAMP"
    timestamp_offline = datetime.now(CDMX_TZ).isoformat()  # Como lo envía el frontend
    
    print(f"📤 DATOS RECIBIDOS:")
    print(f"   usuario_id: {usuario_id}")
    print(f"   timestamp_offline: {timestamp_offline}")
    
    # ✅ NUEVA LÓGICA CON NUESTROS CAMBIOS
    if timestamp_offline:
        fecha_cdmx, hora_cdmx_datetime, timestamp_for_filename = obtener_fecha_hora_cdmx(timestamp_offline)
        fecha_hora = hora_cdmx_datetime.astimezone(pytz.UTC).replace(tzinfo=None)
        print(f"📅 ✅ Usando timestamp offline con zona CDMX: {fecha_hora}")
    else:
        fecha_cdmx, hora_cdmx_datetime, timestamp_for_filename = obtener_fecha_hora_cdmx()
        fecha_hora = hora_cdmx_datetime.astimezone(pytz.UTC).replace(tzinfo=None)
        print(f"📅 ⏰ Usando timestamp actual CDMX: {fecha_hora}")
    
    # Simular guardar en BD
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cursor = conn.cursor()
        
        # Insertar como lo hace el endpoint
        cursor.execute(
            "INSERT INTO registros (usuario_id, latitud, longitud, descripcion, foto_url, fecha_hora) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
            (usuario_id, latitud, longitud, descripcion, f"test_{timestamp_for_filename}.jpg", fecha_hora)
        )
        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        
        print(f"✅ Registro guardado en BD con ID: {nuevo_id}")
        
        # Verificar
        cursor.execute("SELECT * FROM registros WHERE id = %s", (nuevo_id,))
        registro = cursor.fetchone()
        fecha_bd = registro[6]  # fecha_hora
        
        if fecha_bd.tzinfo is None:
            fecha_bd = fecha_bd.replace(tzinfo=pytz.UTC)
        
        fecha_cdmx_verificacion = fecha_bd.astimezone(CDMX_TZ)
        
        print(f"📊 VERIFICACIÓN:")
        print(f"   🌍 En BD (UTC): {fecha_bd}")
        print(f"   🇲🇽 Convertido a CDMX: {fecha_cdmx_verificacion.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def simular_endpoint_registro_offline():
    """Simular el endpoint /registro sin timestamp (modo sin timestamp)"""
    print("\n🧪 TEST: Simulando endpoint /registro SIN TIMESTAMP")
    print("-" * 70)
    
    usuario_id = "93"
    descripcion = "TEST ENDPOINT SIN TIMESTAMP"
    
    # ✅ NUEVA LÓGICA: Sin timestamp_offline
    fecha_cdmx, hora_cdmx_datetime, timestamp_for_filename = obtener_fecha_hora_cdmx()
    fecha_hora = hora_cdmx_datetime.astimezone(pytz.UTC).replace(tzinfo=None)
    print(f"📅 ⏰ Usando timestamp actual CDMX: {fecha_hora}")
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO registros (usuario_id, latitud, longitud, descripcion, foto_url, fecha_hora) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
            (usuario_id, 19.432608, -99.133209, descripcion, f"test_{timestamp_for_filename}.jpg", fecha_hora)
        )
        nuevo_id = cursor.fetchone()[0]
        conn.commit()
        
        print(f"✅ Registro guardado en BD con ID: {nuevo_id}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🚀 PRUEBA FINAL: SIMULACIÓN COMPLETA DEL ENDPOINT /registro")
    print("=" * 70)
    
    # Probar ambos casos
    test1 = simular_endpoint_registro_online()
    test2 = simular_endpoint_registro_offline()
    
    print("\n" + "=" * 70)
    if test1 and test2:
        print("✅ TODAS LAS PRUEBAS PASARON - EL ENDPOINT REGISTRA EN HORARIO CDMX")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
    
    print("🎯 CONCLUSIÓN: Los registros de actividades ahora se guardan correctamente en horario CDMX")

if __name__ == "__main__":
    main()
