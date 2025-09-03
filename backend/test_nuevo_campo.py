#!/usr/bin/env python3
"""
Script de prueba para el nuevo campo tipo_actividad
"""
import requests
import json
from io import BytesIO

def test_nuevo_registro():
    """Prueba crear un registro con el nuevo campo tipo_actividad"""
    
    API_URL = "http://127.0.0.1:8000"
    
    # Datos del registro de prueba
    data = {
        'usuario_id': '1',
        'latitud': 19.4326,
        'longitud': -99.1332,
        'descripcion': 'Prueba de registro con tipo de actividad gabinete',
        'tipo_actividad': 'gabinete'  # NUEVO CAMPO
    }
    
    # Crear una imagen de prueba muy simple (1x1 pixel)
    # En formato base64: imagen PNG de 1x1 pixel transparente
    import base64
    
    # PNG de 1x1 pixel transparente en base64 (corregido)
    png_b64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9jd+IKwAAAABJRU5ErkJggg=='
    png_bytes = base64.b64decode(png_b64)
    
    files = {
        'foto': ('test.png', BytesIO(png_bytes), 'image/png')
    }
    
    print("🧪 Enviando registro de prueba con tipo_actividad = 'gabinete'...")
    
    try:
        response = requests.post(f"{API_URL}/registro", data=data, files=files)
        
        if response.status_code == 200:
            print("✅ Registro enviado exitosamente!")
            print("📄 Respuesta:", json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Error al enviar registro: {response.status_code}")
            print("📄 Respuesta:", response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    return True

def test_estadisticas():
    """Prueba el endpoint de estadísticas por tipo"""
    
    API_URL = "http://127.0.0.1:8000"
    
    print("\n📊 Probando estadísticas por tipo de actividad...")
    
    try:
        response = requests.get(f"{API_URL}/estadisticas/tipo-actividad")
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Estadísticas obtenidas:")
            print(json.dumps(stats, indent=2))
        else:
            print(f"❌ Error al obtener estadísticas: {response.status_code}")
            print("📄 Respuesta:", response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    return True

def test_obtener_registros():
    """Prueba obtener los registros para verificar que incluyen tipo_actividad"""
    
    API_URL = "http://127.0.0.1:8000"
    
    print("\n📋 Obteniendo registros para verificar tipo_actividad...")
    
    try:
        response = requests.get(f"{API_URL}/registros?limit=3")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {len(data['registros'])} registros obtenidos:")
            
            for i, registro in enumerate(data['registros'][:3]):
                print(f"  Registro {i+1}:")
                print(f"    ID: {registro.get('id')}")
                print(f"    Usuario: {registro.get('usuario_id')}")
                print(f"    Descripción: {registro.get('descripcion', 'Sin descripción')}")
                print(f"    Tipo Actividad: {registro.get('tipo_actividad', 'No especificado')}")
                print(f"    Fecha: {registro.get('fecha_hora')}")
                print()
        else:
            print(f"❌ Error al obtener registros: {response.status_code}")
            print("📄 Respuesta:", response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🧪 INICIANDO PRUEBAS DEL NUEVO CAMPO tipo_actividad")
    print("=" * 50)
    
    # 1. Crear un registro de prueba
    if test_nuevo_registro():
        # 2. Verificar estadísticas
        test_estadisticas()
        
        # 3. Obtener registros para verificar
        test_obtener_registros()
    
    print("\n🏁 PRUEBAS COMPLETADAS")
