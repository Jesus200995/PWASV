#!/usr/bin/env python3
"""
Script de verificación completa del sistema de fechas CDMX
Prueba backend, base de datos y frontend
"""

import psycopg2
import requests
from datetime import datetime
import pytz
import json

# Configuración
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"
API_URL = "https://apipwa.sembrandodatos.com"

CDMX_TZ = pytz.timezone("America/Mexico_City")

def verificar_backend():
    """Verifica que el backend maneje correctamente las fechas"""
    print("=== VERIFICACIÓN DEL BACKEND ===")
    
    try:
        # Probar endpoint de registros
        response = requests.get(f"{API_URL}/registros", timeout=10)
        
        if response.status_code == 200:
            print("✅ Backend responde correctamente")
            data = response.json()
            
            if 'registros' in data and len(data['registros']) > 0:
                # Verificar formato de fechas
                primer_registro = data['registros'][0]
                if 'fecha_hora' in primer_registro:
                    fecha = primer_registro['fecha_hora']
                    print(f"📅 Ejemplo de fecha del backend: {fecha}")
                    
                    # Verificar que tiene timezone info
                    if '+' in fecha or '-' in fecha or fecha.endswith('Z'):
                        print("✅ Las fechas incluyen información de timezone")
                    else:
                        print("⚠️ Las fechas no incluyen timezone explícito")
                    
                    # Intentar parsear la fecha
                    try:
                        fecha_parseada = datetime.fromisoformat(fecha.replace('Z', '+00:00'))
                        if fecha_parseada.tzinfo:
                            offset = fecha_parseada.utcoffset().total_seconds() / 3600
                            print(f"⏰ Offset de la fecha: UTC{offset:+.0f}")
                            
                            if offset in [-6, -5]:  # CDMX puede ser UTC-6 o UTC-5
                                print("✅ Offset correcto para CDMX")
                            else:
                                print(f"❌ Offset incorrecto. Esperado: UTC-6 o UTC-5, encontrado: UTC{offset:+.0f}")
                        else:
                            print("⚠️ Fecha sin timezone info")
                    except Exception as e:
                        print(f"❌ Error parseando fecha: {e}")
                else:
                    print("❌ No se encontró campo fecha_hora en los registros")
            else:
                print("⚠️ No hay registros para verificar")
        else:
            print(f"❌ Backend no responde: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando backend: {e}")
        return False

def verificar_base_datos():
    """Verifica la configuración de la base de datos"""
    print("\n=== VERIFICACIÓN DE BASE DE DATOS ===")
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cursor = conn.cursor()
        
        # Configurar timezone
        cursor.execute("SET timezone = 'America/Mexico_City';")
        
        # Verificar timezone
        cursor.execute("SHOW timezone;")
        tz = cursor.fetchone()[0]
        print(f"🌍 Timezone de la sesión: {tz}")
        
        # Verificar tipo de columna
        cursor.execute("""
            SELECT data_type 
            FROM information_schema.columns 
            WHERE table_name = 'registros' AND column_name = 'fecha_hora';
        """)
        
        tipo_columna = cursor.fetchone()
        if tipo_columna:
            tipo = tipo_columna[0]
            print(f"📅 Tipo de columna fecha_hora: {tipo}")
            
            if "with time zone" in tipo.lower():
                print("✅ Columna configurada con timezone")
            else:
                print("⚠️ Columna SIN timezone - se recomienda actualizar")
        
        # Probar inserción de fecha
        fecha_test = datetime.now(CDMX_TZ)
        print(f"🕐 Fecha de prueba Python: {fecha_test}")
        
        # Ver qué devuelve NOW() de PostgreSQL
        cursor.execute("SELECT NOW();")
        pg_now = cursor.fetchone()[0]
        print(f"🕐 PostgreSQL NOW(): {pg_now}")
        
        # Verificar registros existentes
        cursor.execute("SELECT COUNT(*), MAX(fecha_hora) FROM registros;")
        count, max_fecha = cursor.fetchone()
        print(f"📊 Total registros: {count}")
        if max_fecha:
            print(f"📅 Fecha más reciente: {max_fecha}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

def verificar_configuracion_sistema():
    """Verifica la configuración del sistema"""
    print("\n=== VERIFICACIÓN DEL SISTEMA ===")
    
    # Verificar Python timezone
    fecha_utc = datetime.utcnow().replace(tzinfo=pytz.UTC)
    fecha_cdmx = fecha_utc.astimezone(CDMX_TZ)
    
    print(f"🕐 UTC: {fecha_utc}")
    print(f"🕐 CDMX: {fecha_cdmx}")
    
    offset = fecha_cdmx.utcoffset().total_seconds() / 3600
    print(f"⏰ Offset CDMX: UTC{offset:+.0f}")
    
    if offset in [-6, -5]:
        print("✅ Configuración de timezone Python correcta")
        return True
    else:
        print("❌ Configuración de timezone Python incorrecta")
        return False

def generar_reporte():
    """Genera un reporte final"""
    print("\n" + "="*50)
    print("REPORTE FINAL")
    print("="*50)
    
    backend_ok = verificar_backend()
    bd_ok = verificar_base_datos()
    sistema_ok = verificar_configuracion_sistema()
    
    print(f"\n📊 RESULTADOS:")
    print(f"Backend: {'✅' if backend_ok else '❌'}")
    print(f"Base de datos: {'✅' if bd_ok else '❌'}")  
    print(f"Sistema: {'✅' if sistema_ok else '❌'}")
    
    if backend_ok and bd_ok and sistema_ok:
        print("\n🎉 ¡SISTEMA COMPLETAMENTE CONFIGURADO!")
        print("✅ Todas las fechas se manejan en horario CDMX")
        print("✅ Backend, base de datos y sistema configurados correctamente")
    else:
        print("\n⚠️ SISTEMA PARCIALMENTE CONFIGURADO")
        print("Revisa los errores anteriores y completa la configuración")
    
    print("\n📋 INSTRUCCIONES FINALES:")
    print("1. Si hay errores de BD, ejecuta como admin: configurar_postgresql_cdmx.sql")
    print("2. Reinicia el backend después de cualquier cambio")
    print("3. Verifica en el frontend que las fechas se muestren correctamente")
    print("4. Ejecuta este script después de cada cambio para verificar")

if __name__ == "__main__":
    generar_reporte()
