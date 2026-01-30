#!/usr/bin/env python3
"""
Script para probar la generación del reporte de la usuaria 463 (ELSI MAGANA TON GOMEZ)
Mes: Enero 2026
"""

import requests
import json
from datetime import datetime

# Configuración
API_URL = "https://apipwa.sembrandodatos.com"
USUARIO_ID = 463

def obtener_actividades():
    """Obtener actividades de enero 2026"""
    print(f"📥 Obteniendo actividades del usuario {USUARIO_ID} para enero 2026...")
    
    url = f"{API_URL}/registros"
    params = {
        "usuario_id": USUARIO_ID,
        "mes": 1,
        "anio": 2026
    }
    
    response = requests.get(url, params=params)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        # La API devuelve {'registros': [...]} directamente
        actividades = data.get('registros', [])
        print(f"   ✅ {len(actividades)} actividades encontradas")
        
        # Contar por tipo
        campo = sum(1 for a in actividades if (a.get('tipo_actividad') or '').lower() == 'campo')
        gabinete = sum(1 for a in actividades if (a.get('tipo_actividad') or '').lower() == 'gabinete')
        con_foto = sum(1 for a in actividades if a.get('foto_url'))
        
        print(f"   📊 Campo: {campo}, Gabinete: {gabinete}")
        print(f"   📸 Con foto: {con_foto}")
        
        return actividades
    else:
        print(f"   ❌ Error HTTP: {response.status_code}")
        print(f"   {response.text}")
        return []

def simular_guardado_reporte(actividades):
    """Simular el guardado del reporte"""
    print(f"\n💾 Simulando guardado de reporte...")
    
    # Preparar datos similares a como lo hace el frontend
    datos_reporte = {
        "usuario": {
            "id": USUARIO_ID,
            "nombre": "ELSI MAGANA TON GOMEZ",
            "cargo": "TECNICO SOCIAL",
            "curp": "TOGE890427MCSNML03",
            "territorio": "Pichucalco"
        },
        "periodo": {
            "mes": 0,  # 0 = Enero
            "mesNombre": "Enero",
            "anio": 2026,
            "fechaInicio": "2026-01-01T06:00:00.000Z",
            "fechaFin": "2026-01-31T05:59:59.999Z"
        },
        "actividades": [],
        "estadisticas": {
            "totalActividades": len(actividades),
            "actividadesCampo": sum(1 for a in actividades if (a.get('tipo_actividad') or '').lower() == 'campo'),
            "actividadesGabinete": sum(1 for a in actividades if (a.get('tipo_actividad') or '').lower() == 'gabinete'),
            "actividadesConFoto": sum(1 for a in actividades if a.get('foto_url'))
        },
        "fechaGeneracion": datetime.now().isoformat()
    }
    
    # Agregar actividades (sin foto_base64)
    for act in actividades:
        datos_reporte["actividades"].append({
            "id": act.get('id'),
            "fecha_hora": act.get('fecha_hora'),
            "tipo_actividad": act.get('tipo_actividad'),
            "descripcion": act.get('descripcion'),
            "foto_url": act.get('foto_url'),
            "latitud": act.get('latitud'),
            "longitud": act.get('longitud')
        })
    
    # Calcular tamaño del JSON
    json_str = json.dumps(datos_reporte)
    size_kb = len(json_str.encode('utf-8')) / 1024
    print(f"   📦 Tamaño del JSON: {size_kb:.2f} KB")
    
    # Preparar payload completo
    payload = {
        "usuario_id": USUARIO_ID,
        "nombre_reporte": "Reporte Enero 2026",
        "mes": "Enero",
        "anio": 2026,
        "tipo": "PDF",
        "datos_reporte": datos_reporte,
        "firma_usuario_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="  # Firma de prueba muy pequeña
    }
    
    payload_str = json.dumps(payload)
    payload_size_kb = len(payload_str.encode('utf-8')) / 1024
    print(f"   📦 Tamaño total del payload: {payload_size_kb:.2f} KB")
    
    # Intentar guardar
    print(f"\n🚀 Enviando a {API_URL}/reportes/guardar...")
    
    try:
        response = requests.post(
            f"{API_URL}/reportes/guardar",
            json=payload,
            timeout=30  # 30 segundos de timeout
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:500]}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   ✅ Reporte guardado exitosamente! ID: {data.get('reporte_id')}")
            else:
                print(f"   ❌ Error en respuesta: {data}")
        else:
            print(f"   ❌ Error HTTP: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print(f"   ❌ TIMEOUT: La petición tardó más de 30 segundos")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 70)
    print("TEST: Generación de reporte para usuario 463 (Enero 2026)")
    print("=" * 70)
    
    # Paso 1: Obtener actividades
    actividades = obtener_actividades()
    
    if not actividades:
        print("\n❌ No hay actividades, no se puede continuar")
        exit(1)
    
    # Paso 2: Simular guardado
    simular_guardado_reporte(actividades)
    
    print("\n" + "=" * 70)
    print("Test completado")
    print("=" * 70)
