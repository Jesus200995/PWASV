#!/usr/bin/env python3
"""
Test simple para verificar el endpoint de registro
"""

import requests
import json
from datetime import datetime
import pytz

# Configuración
API_URL = "http://localhost:8000"
CDMX_TZ = pytz.timezone('America/Mexico_City')

def test_simple():
    print("🧪 TEST SIMPLE: Verificar endpoint /registro")
    print("=" * 50)
    
    # Probar primero con GET a /registros para ver si el servidor responde
    try:
        print("📡 Probando conectividad con /registros...")
        response = requests.get(f"{API_URL}/registros?limit=1", timeout=5)
        print(f"✅ Conectividad OK: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conectividad: {e}")
        return
    
    # Simular timestamp CDMX
    now_cdmx = datetime.now(CDMX_TZ)
    timestamp_cdmx = now_cdmx.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + '-06:00'
    
    print(f"🕐 Timestamp CDMX: {timestamp_cdmx}")
    
    # Datos mínimos para el test
    data = {
        'usuario_id': '1',
        'latitud': '19.4326',
        'longitud': '-99.1332', 
        'descripcion': 'Test simple',
        'tipo_actividad': 'campo',
        'timestamp_offline': timestamp_cdmx
    }
    
    # Crear archivo de imagen mínimo
    import tempfile
    import os
    
    # Crear imagen de 1x1 pixel
    image_data = b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xFF\xDB\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0C\x14\r\x0C\x0B\x0B\x0C\x19\x12\x13\x0F\x14\x1D\x1A\x1F\x1E\x1D\x1A\x1C\x1C $.\' ",#\x1C\x1C(7),01444\x1F\'9=82<.342\xFF\xC0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xFF\xC4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xFF\xC4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xDA\x00\x0C\x03\x01\x00\x02\x11\x03\x11\x00\x3F\x00\xAA\xFF\xD9'
    
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
        tmp_file.write(image_data)
        tmp_file_path = tmp_file.name
    
    try:
        with open(tmp_file_path, 'rb') as f:
            files = {'foto': ('test.jpg', f, 'image/jpeg')}
            
            print("📤 Enviando POST a /registro...")
            response = requests.post(f"{API_URL}/registro", data=data, files=files, timeout=10)
            
            print(f"📝 Status: {response.status_code}")
            print(f"📝 Response: {response.text}")
            
            if response.status_code == 200:
                print("✅ ¡Registro exitoso!")
                
                # Verificar en BD
                print("🔍 Verificando último registro...")
                registros_resp = requests.get(f"{API_URL}/registros?usuario_id=1&limit=1")
                if registros_resp.status_code == 200:
                    registros = registros_resp.json()
                    if registros:
                        ultimo = registros[0]
                        print(f"📊 Último registro:")
                        print(f"   📅 Fecha/hora BD: {ultimo.get('fecha_hora')}")
                        print(f"   📝 Descripción: {ultimo.get('descripcion')}")
                        print(f"   🏷️ Tipo actividad: {ultimo.get('tipo_actividad')}")
                        print(f"   📍 Coordenadas: {ultimo.get('latitud')}, {ultimo.get('longitud')}")
                        
                        # Convertir a CDMX para comparar
                        fecha_bd = ultimo.get('fecha_hora')
                        if fecha_bd:
                            try:
                                # Parsear fecha de BD
                                if fecha_bd.endswith('Z'):
                                    fecha_bd = fecha_bd[:-1] + '+00:00'
                                
                                fecha_utc = datetime.fromisoformat(fecha_bd)
                                if fecha_utc.tzinfo is None:
                                    fecha_utc = fecha_utc.replace(tzinfo=pytz.UTC)
                                
                                fecha_cdmx_bd = fecha_utc.astimezone(CDMX_TZ)
                                
                                print(f"🇲🇽 Fecha BD en CDMX: {fecha_cdmx_bd.strftime('%H:%M:%S %d/%m/%Y')}")
                                print(f"🕐 Timestamp enviado: {now_cdmx.strftime('%H:%M:%S %d/%m/%Y')}")
                                
                                # Calcular diferencia
                                diff = abs((now_cdmx - fecha_cdmx_bd).total_seconds())
                                print(f"⏱️ Diferencia: {diff:.1f} segundos")
                                
                                if diff <= 60:
                                    print("✅ ¡Las horas coinciden! (tolerancia: 1 minuto)")
                                else:
                                    print("❌ Las horas NO coinciden")
                                    
                            except Exception as e:
                                print(f"❌ Error procesando fecha: {e}")
                        
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
    finally:
        # Limpiar archivo temporal
        try:
            os.unlink(tmp_file_path)
        except:
            pass

if __name__ == "__main__":
    test_simple()
