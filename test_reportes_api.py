#!/usr/bin/env python3
"""
Script para probar el endpoint /historial/{usuario_id} con filtros de fechas
"""

import requests
import json
from datetime import datetime, timedelta

# Configuración
API_URL = "http://localhost:8000"  # Cambiar según tu URL
USUARIO_ID = 1  # Cambiar según necesidad

def prueba_historial_sin_filtros():
    """Prueba obtener historial sin filtros"""
    print("\n" + "="*60)
    print("PRUEBA 1: Obtener historial sin filtros")
    print("="*60)
    
    url = f"{API_URL}/historial/{USUARIO_ID}"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Error: {e}")

def prueba_historial_mes_actual():
    """Prueba obtener historial del mes actual"""
    print("\n" + "="*60)
    print("PRUEBA 2: Obtener historial del mes actual")
    print("="*60)
    
    hoy = datetime.now()
    inicio_mes = datetime(hoy.year, hoy.month, 1)
    
    params = {
        "fecha_inicio": inicio_mes.strftime("%Y-%m-%d"),
        "fecha_fin": hoy.strftime("%Y-%m-%d"),
        "limit": 100
    }
    
    url = f"{API_URL}/historial/{USUARIO_ID}"
    
    print(f"URL: {url}")
    print(f"Parámetros: {params}")
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Total de registros: {data.get('total', 0)}")
        
        if data.get('historial'):
            print(f"\nPrimeros 3 registros:")
            for i, actividad in enumerate(data['historial'][:3]):
                print(f"\n  Registro {i+1}:")
                print(f"    Fecha: {actividad.get('fecha')}")
                print(f"    Hora: {actividad.get('hora')}")
                print(f"    Tipo: {actividad.get('tipo')}")
                print(f"    Descripción: {actividad.get('descripcion')}")
        else:
            print("⚠️  No se encontraron registros")
    except Exception as e:
        print(f"❌ Error: {e}")

def prueba_historial_mes_especifico():
    """Prueba obtener historial de un mes específico"""
    print("\n" + "="*60)
    print("PRUEBA 3: Obtener historial de enero 2026")
    print("="*60)
    
    inicio = datetime(2026, 1, 1)
    fin = datetime(2026, 1, 31)
    
    params = {
        "fecha_inicio": inicio.strftime("%Y-%m-%d"),
        "fecha_fin": fin.strftime("%Y-%m-%d"),
        "limit": 100
    }
    
    url = f"{API_URL}/historial/{USUARIO_ID}"
    
    print(f"URL: {url}")
    print(f"Parámetros: {params}")
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Total de registros: {data.get('total', 0)}")
        
        if data.get('historial'):
            print(f"\nPrimeros 3 registros:")
            for i, actividad in enumerate(data['historial'][:3]):
                print(f"\n  Registro {i+1}:")
                print(f"    Fecha: {actividad.get('fecha')}")
                print(f"    Hora: {actividad.get('hora')}")
                print(f"    Tipo: {actividad.get('tipo')}")
        else:
            print("⚠️  No se encontraron registros para enero 2026")
    except Exception as e:
        print(f"❌ Error: {e}")

def prueba_historial_con_tipo():
    """Prueba obtener historial filtrado por tipo"""
    print("\n" + "="*60)
    print("PRUEBA 4: Obtener historial con filtro por tipo (entrada)")
    print("="*60)
    
    hoy = datetime.now()
    inicio_mes = datetime(hoy.year, hoy.month, 1)
    
    params = {
        "fecha_inicio": inicio_mes.strftime("%Y-%m-%d"),
        "fecha_fin": hoy.strftime("%Y-%m-%d"),
        "tipo": "entrada",
        "limit": 100
    }
    
    url = f"{API_URL}/historial/{USUARIO_ID}"
    
    print(f"URL: {url}")
    print(f"Parámetros: {params}")
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Total de registros (entrada): {data.get('total', 0)}")
    except Exception as e:
        print(f"❌ Error: {e}")

def prueba_usuario_invalido():
    """Prueba con usuario inexistente"""
    print("\n" + "="*60)
    print("PRUEBA 5: Usuario inexistente (debería fallar)")
    print("="*60)
    
    usuario_id = 99999
    url = f"{API_URL}/historial/{usuario_id}"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("\n🧪 INICIANDO PRUEBAS DE ENDPOINT /historial/{usuario_id}")
    print(f"API URL: {API_URL}")
    print(f"Usuario ID para pruebas: {USUARIO_ID}")
    
    prueba_historial_sin_filtros()
    prueba_historial_mes_actual()
    prueba_historial_mes_especifico()
    prueba_historial_con_tipo()
    prueba_usuario_invalido()
    
    print("\n" + "="*60)
    print("✅ PRUEBAS COMPLETADAS")
    print("="*60 + "\n")
