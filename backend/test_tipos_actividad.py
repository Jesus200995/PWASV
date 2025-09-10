#!/usr/bin/env python3
"""
Script para verificar los tipos de actividad en el backend
"""
import requests
import json
from datetime import datetime

def test_backend_tipos_actividad():
    """Prueba que el backend esté enviando correctamente los tipos de actividad"""
    
    # URLs del backend
    BASE_URL = 'https://apipwa.sembrandodatos.com'
    
    endpoints = [
        '/registros',
        '/asistencias'
    ]
    
    print("🔍 Verificando tipos de actividad en el backend...")
    print("=" * 60)
    
    for endpoint in endpoints:
        print(f"\n📡 Probando endpoint: {endpoint}")
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Respuesta exitosa")
                print(f"📊 Tipo de datos recibidos: {type(data)}")
                
                # Manejar diferentes formatos de respuesta
                registros_list = []
                
                if isinstance(data, list):
                    registros_list = data
                elif isinstance(data, dict):
                    # Para /registros
                    if 'registros' in data:
                        registros_list = data['registros']
                        print(f"📋 {len(registros_list)} registros encontrados")
                        print(f"📄 Total: {data.get('total', 'N/A')}")
                    # Para /asistencias
                    elif 'asistencias' in data:
                        registros_list = data['asistencias']
                        print(f"📋 {len(registros_list)} asistencias encontradas")
                    else:
                        print(f"🔑 Claves disponibles: {list(data.keys())}")
                        return
                
                if registros_list:
                    # Analizar tipos de actividad
                    tipos_encontrados = {}
                    registros_con_tipo = 0
                    
                    for i, registro in enumerate(registros_list):  # Revisar todos los registros
                        if i >= 10:  # Solo mostrar detalles de los primeros 10
                            break
                        
                        if not isinstance(registro, dict):
                            print(f"⚠️ Registro {i+1} no es un diccionario: {type(registro)}")
                            continue
                        
                        tipo_actividad = registro.get('tipo_actividad', 'N/A')
                        if tipo_actividad != 'N/A':
                            registros_con_tipo += 1
                        
                        if tipo_actividad not in tipos_encontrados:
                            tipos_encontrados[tipo_actividad] = 0
                        tipos_encontrados[tipo_actividad] += 1
                        
                        print(f"  📋 Registro {i+1}:")
                        print(f"    - ID: {registro.get('id', 'N/A')}")
                        print(f"    - Usuario: {registro.get('usuario', 'N/A')}")
                        print(f"    - Usuario ID: {registro.get('usuario_id', 'N/A')}")
                        print(f"    - Tipo actividad: {tipo_actividad}")
                        print(f"    - Fecha: {registro.get('fecha_hora', registro.get('fecha', 'N/A'))}")
                        
                        # Buscar específicamente campo/gabinete
                        if tipo_actividad in ['campo', 'gabinete']:
                            print(f"    ⭐ ENCONTRADO: {tipo_actividad.upper()}")
                    
                    print(f"\n📊 Resumen de tipos encontrados:")
                    for tipo, cantidad in tipos_encontrados.items():
                        print(f"  - {tipo}: {cantidad} registros")
                    
                    print(f"\n📈 Estadísticas:")
                    print(f"  - Total registros revisados: {min(10, len(registros_list))}")
                    print(f"  - Registros con tipo_actividad: {registros_con_tipo}")
                    
                    # Buscar específicamente registros de campo y gabinete
                    campo_count = sum(1 for r in registros_list if isinstance(r, dict) and r.get('tipo_actividad') == 'campo')
                    gabinete_count = sum(1 for r in registros_list if isinstance(r, dict) and r.get('tipo_actividad') == 'gabinete')
                    
                    print(f"\n🎯 Búsqueda específica en todos los registros:")
                    print(f"  - Registros de CAMPO: {campo_count}")
                    print(f"  - Registros de GABINETE: {gabinete_count}")
                    
                    if campo_count > 0:
                        print("\n🟢 Ejemplos de registros de CAMPO:")
                        campo_ejemplos = [r for r in registros_list if isinstance(r, dict) and r.get('tipo_actividad') == 'campo'][:3]
                        for ejemplo in campo_ejemplos:
                            print(f"    - ID {ejemplo.get('id')}: Usuario {ejemplo.get('usuario_id')} - {ejemplo.get('fecha_hora', ejemplo.get('fecha'))}")
                    
                    if gabinete_count > 0:
                        print("\n🔵 Ejemplos de registros de GABINETE:")
                        gabinete_ejemplos = [r for r in registros_list if isinstance(r, dict) and r.get('tipo_actividad') == 'gabinete'][:3]
                        for ejemplo in gabinete_ejemplos:
                            print(f"    - ID {ejemplo.get('id')}: Usuario {ejemplo.get('usuario_id')} - {ejemplo.get('fecha_hora', ejemplo.get('fecha'))}")
                else:
                    print(f"📄 No se encontraron registros en el formato esperado")
                
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error al conectar con {endpoint}: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Verificación completada")

if __name__ == "__main__":
    test_backend_tipos_actividad()
