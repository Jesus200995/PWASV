#!/usr/bin/env python3
"""
Script para probar el nuevo endpoint de estadísticas
"""

import requests
import json

def test_estadisticas():
    """Probar el endpoint de estadísticas"""
    try:
        url = "http://localhost:8000/estadisticas"
        print(f"🧪 Probando endpoint: {url}")
        
        response = requests.get(url)
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Respuesta exitosa:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Verificar que tenemos las estadísticas esperadas
            estadisticas = data.get('estadisticas', {})
            campos_esperados = [
                'total_registros',
                'total_usuarios', 
                'registros_hoy',
                'total_asistencias',
                'asistencias_hoy',
                'usuarios_presentes'
            ]
            
            print("\n🔍 Verificando campos esperados:")
            for campo in campos_esperados:
                if campo in estadisticas:
                    valor = estadisticas[campo]
                    print(f"  ✅ {campo}: {valor}")
                else:
                    print(f"  ❌ {campo}: NO ENCONTRADO")
            
            print(f"\n🎯 TOTAL ACTIVIDADES: {estadisticas.get('total_registros', 'N/A')}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor. ¿Está el backend corriendo en http://localhost:8000?")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_estadisticas()
