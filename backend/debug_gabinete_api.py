#!/usr/bin/env python3
"""
Script para verificar registros de gabinete usando la API - versión corregida
"""

import requests
import json
from datetime import datetime

# URL de la API
API_URL = "https://apipwa.sembrandodatos.com"

def verificar_registros_gabinete():
    """Verificar registros de gabinete usando la API"""
    
    print("🔍 VERIFICANDO REGISTROS DE GABINETE VÍA API...")
    print("=" * 60)
    
    try:
        # 1. Obtener todos los registros
        print("\n1️⃣ Obteniendo todos los registros...")
        response = requests.get(f"{API_URL}/registros", timeout=15)
        
        print(f"Status code: {response.status_code}")
        print(f"Content type: {response.headers.get('content-type', 'N/A')}")
        print(f"Response text (first 200 chars): {response.text[:200]}")
        
        if response.status_code == 200:
            try:
                registros = response.json()
                print(f"✅ Respuesta JSON válida")
                
                if isinstance(registros, list):
                    print(f"✅ Total registros obtenidos: {len(registros)}")
                    
                    # Filtrar por tipo de actividad
                    tipos_actividad = {}
                    registros_gabinete = []
                    
                    for registro in registros:
                        if isinstance(registro, dict):
                            tipo = registro.get('tipo_actividad', 'sin_tipo')
                            tipos_actividad[tipo] = tipos_actividad.get(tipo, 0) + 1
                            
                            if tipo == 'gabinete':
                                registros_gabinete.append(registro)
                        else:
                            print(f"⚠️ Registro no es dict: {type(registro)} - {registro}")
                    
                    print(f"\n📊 DISTRIBUCIÓN POR TIPO DE ACTIVIDAD:")
                    for tipo, cantidad in tipos_actividad.items():
                        print(f"   - {tipo}: {cantidad} registros")
                    
                    print(f"\n🎯 REGISTROS DE GABINETE ENCONTRADOS: {len(registros_gabinete)}")
                    
                    if registros_gabinete:
                        print("\n📋 DETALLES DE REGISTROS DE GABINETE:")
                        for i, reg in enumerate(registros_gabinete[:10]):
                            print(f"\n   Registro {i+1}:")
                            print(f"   - ID: {reg.get('id')}")
                            print(f"   - Usuario ID: {reg.get('usuario_id')}")
                            print(f"   - Fecha: {reg.get('fecha_hora')}")
                            print(f"   - Coordenadas: {reg.get('coordenadas')}")
                            print(f"   - Descripción: {reg.get('descripcion', 'N/A')}")
                    else:
                        print("   ❌ No se encontraron registros de gabinete")
                        
                        # Mostrar algunos registros de muestra
                        print(f"\n🔍 MUESTRA DE REGISTROS (primeros 3):")
                        for i, reg in enumerate(registros[:3]):
                            if isinstance(reg, dict):
                                print(f"\n   Registro {i+1}:")
                                print(f"   - ID: {reg.get('id')}")
                                print(f"   - Usuario ID: {reg.get('usuario_id')}")
                                print(f"   - Tipo: {reg.get('tipo_actividad')}")
                                print(f"   - Fecha: {reg.get('fecha_hora')}")
                                print(f"   - Todas las claves: {list(reg.keys())}")
                            else:
                                print(f"   Registro {i+1}: {reg}")
                else:
                    print(f"⚠️ Respuesta no es una lista: {type(registros)}")
                    print(f"Contenido: {registros}")
                    
            except json.JSONDecodeError as e:
                print(f"❌ Error decodificando JSON: {e}")
                print(f"Respuesta cruda: {response.text[:500]}")
                
        else:
            print(f"❌ Error al obtener registros: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    
    except Exception as e:
        print(f"❌ Error al verificar registros: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verificar_registros_gabinete()
