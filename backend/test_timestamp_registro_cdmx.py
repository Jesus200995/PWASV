#!/usr/bin/env python3
"""
Test para verificar que los registros de actividades se guardan con el timestamp CDMX correcto
"""

import requests
import json
from datetime import datetime
import pytz
import os

# Configuración
API_URL = "http://localhost:8000"
CDMX_TZ = pytz.timezone('America/Mexico_City')

def obtener_hora_cdmx_actual():
    """Obtener la hora actual de CDMX en el mismo formato que la barra verde"""
    now = datetime.now(CDMX_TZ)
    
    # Formato que se muestra en la barra verde
    hora_formato = now.strftime('%H:%M:%S')
    fecha_formato = now.strftime('%d/%m/%Y')
    
    # Formato ISO que se envía al backend
    iso_formato = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '-06:00'
    
    return {
        'hora_barra': hora_formato,
        'fecha_barra': fecha_formato,
        'iso_timestamp': iso_formato,
        'datetime_obj': now
    }

def simular_timestamp_frontend():
    """Simular exactamente cómo el frontend genera el timestamp CDMX"""
    now = datetime.now()
    
    # Simular la lógica del frontend para obtener timestamp CDMX
    # Esto es equivalente a la función obtenerTimestampCDMX() del frontend
    from datetime import timezone, timedelta
    
    # Crear timezone para CDMX (UTC-6)
    cdmx_offset = timedelta(hours=-6)
    cdmx_tz = timezone(cdmx_offset)
    
    # Convertir la hora local a CDMX
    now_cdmx = now.astimezone(CDMX_TZ)
    
    # Formato ISO con zona horaria
    iso_string = now_cdmx.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '-06:00'
    
    return iso_string

def test_registro_con_timestamp_cdmx():
    """Probar el registro de actividad con timestamp CDMX"""
    print("🧪 TEST: Registro con timestamp CDMX")
    print("=" * 50)
    
    # 1. Obtener la hora actual de CDMX (como la muestra la barra)
    tiempo_cdmx = obtener_hora_cdmx_actual()
    timestamp_frontend = simular_timestamp_frontend()
    
    print(f"🕐 Hora actual CDMX (barra verde): {tiempo_cdmx['hora_barra']}")
    print(f"📅 Fecha actual CDMX (barra verde): {tiempo_cdmx['fecha_barra']}")
    print(f"📝 Timestamp ISO enviado: {timestamp_frontend}")
    print(f"📍 Datetime objeto CDMX: {tiempo_cdmx['datetime_obj']}")
    print()
    
    # 2. Crear archivo de imagen de prueba
    test_image_path = "test_image.jpg"
    
    # Crear una imagen mínima de prueba (1x1 pixel)
    test_image_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
    
    with open(test_image_path, 'wb') as f:
        f.write(test_image_data)
    
    try:
        # 3. Preparar datos del registro
        form_data = {
            'usuario_id': '3258',
            'latitud': '19.4326',
            'longitud': '-99.1332',
            'descripcion': f'Prueba timestamp CDMX - {tiempo_cdmx["hora_barra"]} {tiempo_cdmx["fecha_barra"]}',
            'tipo_actividad': 'campo',
            'timestamp_offline': timestamp_frontend
        }
        
        files = {
            'foto': ('test_image.jpg', open(test_image_path, 'rb'), 'image/jpeg')
        }
        
        print("📤 Enviando registro al backend...")
        print(f"   📍 Datos: {form_data}")
        print()
        
        # 4. Enviar registro
        response = requests.post(f"{API_URL}/registro", data=form_data, files=files)
        
        if response.status_code == 200:
            print("✅ Registro enviado exitosamente")
            result = response.json()
            print(f"📝 Respuesta: {result}")
        else:
            print(f"❌ Error en el registro: {response.status_code}")
            print(f"📝 Error: {response.text}")
            return
        
        # 5. Verificar en la base de datos
        print("\n🔍 Verificando en la base de datos...")
        registros_response = requests.get(f"{API_URL}/registros?usuario_id=3258&limit=1")
        
        if registros_response.status_code == 200:
            datos_respuesta = registros_response.json()
            registros = datos_respuesta.get('registros', [])
            if registros:
                ultimo_registro = registros[0]
                fecha_hora_bd = ultimo_registro['fecha_hora']
                
                # Convertir fecha_hora de BD a CDMX para comparar
                try:
                    # La BD guarda en UTC naive, convertir a UTC aware y luego a CDMX
                    fecha_hora_utc = datetime.fromisoformat(fecha_hora_bd.replace('Z', '+00:00') if fecha_hora_bd.endswith('Z') else fecha_hora_bd)
                    if fecha_hora_utc.tzinfo is None:
                        fecha_hora_utc = fecha_hora_utc.replace(tzinfo=pytz.UTC)
                    
                    fecha_hora_cdmx_bd = fecha_hora_utc.astimezone(CDMX_TZ)
                    
                    print(f"📊 RESULTADOS DE LA PRUEBA:")
                    print(f"   🕐 Hora barra verde: {tiempo_cdmx['hora_barra']}")
                    print(f"   📅 Fecha barra verde: {tiempo_cdmx['fecha_barra']}")
                    print(f"   📝 Timestamp enviado: {timestamp_frontend}")
                    print(f"   💾 Fecha/hora en BD (UTC): {fecha_hora_bd}")
                    print(f"   🇲🇽 Fecha/hora BD en CDMX: {fecha_hora_cdmx_bd.strftime('%H:%M:%S %d/%m/%Y')}")
                    print(f"   📊 Descripción en BD: {ultimo_registro.get('descripcion', 'N/A')}")
                    print(f"   🏷️ Tipo actividad: {ultimo_registro.get('tipo_actividad', 'N/A')}")
                    
                    # Verificar si las horas coinciden (con tolerancia de 1 minuto)
                    diferencia = abs((tiempo_cdmx['datetime_obj'] - fecha_hora_cdmx_bd).total_seconds())
                    
                    if diferencia <= 60:  # Tolerancia de 1 minuto
                        print(f"✅ ¡ÉXITO! Las horas coinciden (diferencia: {diferencia:.1f} segundos)")
                    else:
                        print(f"❌ Las horas NO coinciden (diferencia: {diferencia:.1f} segundos)")
                    
                except Exception as e:
                    print(f"❌ Error procesando fecha de BD: {e}")
                    print(f"📝 Fecha raw de BD: {fecha_hora_bd}")
            else:
                print("❌ No se encontraron registros en la BD")
        else:
            print(f"❌ Error obteniendo registros: {registros_response.status_code}")
            
    finally:
        # Limpiar archivo de prueba
        try:
            os.remove(test_image_path)
            print(f"\n🧹 Archivo de prueba eliminado: {test_image_path}")
        except:
            pass

if __name__ == "__main__":
    print("🚀 Iniciando prueba de timestamp CDMX para registros de actividades")
    print("📍 Verificando que la hora guardada coincida con la de la barra verde")
    print()
    
    try:
        test_registro_con_timestamp_cdmx()
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
