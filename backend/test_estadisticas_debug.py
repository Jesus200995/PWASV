#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime
import pytz

def probar_estadisticas():
    print("🔍 PROBANDO ESTADÍSTICAS DEL BACKEND...")
    
    # Obtener fecha CDMX
    cdmx_tz = pytz.timezone('America/Mexico_City')
    fecha_cdmx = datetime.now(cdmx_tz)
    fecha_hoy_cdmx = fecha_cdmx.strftime('%Y-%m-%d')
    print(f"📅 Fecha hoy CDMX: {fecha_hoy_cdmx}")
    
    try:
        # Probar endpoint de estadísticas
        response = requests.get('http://localhost:8000/estadisticas')
        if response.status_code == 200:
            estadisticas = response.json()
            print('\n✅ ESTADÍSTICAS DEL BACKEND:')
            for key, value in estadisticas.items():
                print(f"   {key}: {value}")
        else:
            print(f"❌ Error en estadísticas: {response.status_code}")
            
        # Probar endpoint de asistencias
        response2 = requests.get('http://localhost:8000/asistencias')
        if response2.status_code == 200:
            data_asistencias = response2.json()
            asistencias = data_asistencias.get('asistencias', [])
            print(f'\n� ASISTENCIAS TOTALES: {len(asistencias)}')
            
            if len(asistencias) > 0:
                print(f'📋 PRIMERA ASISTENCIA: {asistencias[0]}')
            
            # Contar asistencias de hoy
            asistencias_hoy = [a for a in asistencias if a.get('fecha') == fecha_hoy_cdmx]
            print(f'📅 ASISTENCIAS DE HOY ({fecha_hoy_cdmx}): {len(asistencias_hoy)}')
            
            if asistencias_hoy:
                print("\n📋 PRIMERAS 3 ASISTENCIAS DE HOY:")
                for i, a in enumerate(asistencias_hoy[:3]):
                    print(f"   {i+1}. Usuario: {a.get('usuario_id', 'N/A')}, Fecha: {a.get('fecha')}, Entrada: {a.get('hora_entrada', 'N/A')}, Salida: {a.get('hora_salida', 'N/A')}")
        else:
            print(f"❌ Error en asistencias: {response2.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    probar_estadisticas()
