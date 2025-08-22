#!/usr/bin/env python3
"""
Script de prueba para verificar que las actividades se registren con timestamp CDMX
"""

import requests
import json
from datetime import datetime
import pytz
import io
from PIL import Image
import os

# Configuración
API_URL = "http://localhost:8000"
CDMX_TZ = pytz.timezone("America/Mexico_City")

def crear_imagen_de_prueba():
    """Crear una imagen de prueba pequeña"""
    # Crear imagen de 100x100 píxeles
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

def test_registro_actividad_online():
    """Prueba el registro de actividad en modo online con timestamp"""
    print("🧪 TEST: Registro de actividad ONLINE con timestamp CDMX")
    print("-" * 60)
    
    # Obtener tiempo actual CDMX
    ahora_cdmx = datetime.now(CDMX_TZ)
    timestamp_cliente = ahora_cdmx.isoformat()
    
    print(f"⏰ Hora actual CDMX: {ahora_cdmx.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"📤 Timestamp enviado: {timestamp_cliente}")
    
    # Crear imagen de prueba
    img_bytes = crear_imagen_de_prueba()
    
    # Datos del formulario
    data = {
        'usuario_id': '1',  # Usuario de prueba
        'latitud': '19.432608',  # Ciudad de México
        'longitud': '-99.133209',
        'descripcion': f'Test actividad - {ahora_cdmx.strftime("%H:%M:%S")}',
        'tipo': 'actividad',
        'timestamp_offline': timestamp_cliente
    }
    
    # Archivo
    files = {
        'foto': ('test_actividad.jpg', img_bytes, 'image/jpeg')
    }
    
    try:
        # Enviar request
        response = requests.post(f"{API_URL}/registro", data=data, files=files, timeout=10)
        
        if response.status_code == 200:
            print("✅ Registro enviado exitosamente")
            result = response.json()
            print(f"📄 Respuesta: {json.dumps(result, indent=2)}")
            
            # Verificar en la base de datos
            verificar_ultimo_registro()
            
        else:
            print(f"❌ Error en el registro: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")

def test_registro_actividad_sin_timestamp():
    """Prueba el registro sin timestamp para verificar que use hora CDMX actual"""
    print("\n🧪 TEST: Registro de actividad SIN timestamp (debe usar CDMX actual)")
    print("-" * 60)
    
    # Obtener tiempo actual CDMX para comparar
    ahora_cdmx = datetime.now(CDMX_TZ)
    print(f"⏰ Hora actual CDMX: {ahora_cdmx.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # Crear imagen de prueba
    img_bytes = crear_imagen_de_prueba()
    
    # Datos del formulario SIN timestamp_offline
    data = {
        'usuario_id': '1',  # Usuario de prueba
        'latitud': '19.432608',  # Ciudad de México
        'longitud': '-99.133209',
        'descripcion': f'Test sin timestamp - {ahora_cdmx.strftime("%H:%M:%S")}',
        'tipo': 'actividad'
        # NO enviamos timestamp_offline
    }
    
    # Archivo
    files = {
        'foto': ('test_sin_timestamp.jpg', img_bytes, 'image/jpeg')
    }
    
    try:
        # Enviar request
        response = requests.post(f"{API_URL}/registro", data=data, files=files, timeout=10)
        
        if response.status_code == 200:
            print("✅ Registro enviado exitosamente")
            result = response.json()
            print(f"📄 Respuesta: {json.dumps(result, indent=2)}")
            
            # Verificar en la base de datos
            verificar_ultimo_registro()
            
        else:
            print(f"❌ Error en el registro: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")

def verificar_ultimo_registro():
    """Verificar el último registro en la base de datos"""
    try:
        # Obtener registros del usuario 1
        response = requests.get(f"{API_URL}/registros?usuario_id=1&limit=1", timeout=5)
        
        if response.status_code == 200:
            registros = response.json()
            if registros:
                ultimo = registros[0]
                fecha_hora_bd = ultimo['fecha_hora']
                
                # Parsear la fecha de la BD (viene en UTC)
                fecha_utc = datetime.fromisoformat(fecha_hora_bd.replace('Z', '+00:00'))
                fecha_cdmx = fecha_utc.astimezone(CDMX_TZ)
                
                print(f"📊 ÚLTIMO REGISTRO EN BD:")
                print(f"   🆔 ID: {ultimo['id']}")
                print(f"   📝 Descripción: {ultimo['descripcion']}")
                print(f"   🌍 Fecha UTC (BD): {fecha_hora_bd}")
                print(f"   🇲🇽 Fecha CDMX: {fecha_cdmx.strftime('%Y-%m-%d %H:%M:%S %Z')}")
                print(f"   ⏰ Diferencia con ahora: ~{(datetime.now(CDMX_TZ) - fecha_cdmx).total_seconds():.0f} segundos")
                
            else:
                print("❌ No se encontraron registros")
        else:
            print(f"❌ Error obteniendo registros: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error verificando BD: {e}")

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBAS DE TIMESTAMP CDMX PARA ACTIVIDADES")
    print("=" * 70)
    
    # Verificar que el backend esté corriendo
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        print("✅ Backend disponible")
    except:
        print("❌ Error: Backend no disponible en http://localhost:8000")
        return
    
    # Ejecutar pruebas
    test_registro_actividad_online()
    test_registro_actividad_sin_timestamp()
    
    print("\n" + "=" * 70)
    print("🏁 PRUEBAS COMPLETADAS")

if __name__ == "__main__":
    main()
