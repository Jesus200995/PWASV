#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime
import pytz

def verificar_coherencia_estadisticas():
    print("🔍 VERIFICANDO COHERENCIA DE ESTADÍSTICAS...")
    
    # Obtener fecha CDMX
    cdmx_tz = pytz.timezone('America/Mexico_City')
    fecha_cdmx = datetime.now(cdmx_tz)
    fecha_hoy_cdmx = fecha_cdmx.strftime('%Y-%m-%d')
    print(f"📅 Fecha hoy CDMX: {fecha_hoy_cdmx}")
    
    try:
        # 1. Probar endpoint de estadísticas del servidor
        print("\n1️⃣ ESTADÍSTICAS DEL SERVIDOR:")
        response = requests.get('http://localhost:8000/estadisticas')
        if response.status_code == 200:
            data = response.json()
            stats = data.get('estadisticas', {})
            
            print(f"   📊 Total usuarios: {stats.get('total_usuarios', 0)}")
            print(f"   📊 Asistencias hoy: {stats.get('asistencias_hoy', 0)}")
            print(f"   📊 Usuarios presentes: {stats.get('usuarios_presentes', 0)}")
            print(f"   📊 Total asistencias: {stats.get('total_asistencias', 0)}")
        else:
            print(f"❌ Error en estadísticas del servidor: {response.status_code}")
            return
            
        # 2. Verificar asistencias reales
        print("\n2️⃣ ASISTENCIAS REALES DEL BACKEND:")
        response2 = requests.get('http://localhost:8000/asistencias')
        if response2.status_code == 200:
            data_asistencias = response2.json()
            asistencias = data_asistencias.get('asistencias', [])
            
            # Contar asistencias de hoy
            asistencias_hoy = [a for a in asistencias if a.get('fecha') == fecha_hoy_cdmx]
            usuarios_hoy = set(a.get('usuario_id') for a in asistencias_hoy if a.get('usuario_id'))
            
            print(f"   📊 Total asistencias en BD: {len(asistencias)}")
            print(f"   📅 Asistencias de hoy ({fecha_hoy_cdmx}): {len(asistencias_hoy)}")
            print(f"   👥 Usuarios únicos hoy: {len(usuarios_hoy)}")
            
            # Verificar coherencia
            server_asistencias_hoy = stats.get('asistencias_hoy', 0)
            server_usuarios_presentes = stats.get('usuarios_presentes', 0)
            
            print(f"\n3️⃣ VERIFICACIÓN DE COHERENCIA:")
            print(f"   Asistencias hoy - Servidor: {server_asistencias_hoy} vs Real: {len(asistencias_hoy)} {'✅' if server_asistencias_hoy == len(asistencias_hoy) else '❌'}")
            print(f"   Usuarios presentes - Servidor: {server_usuarios_presentes} vs Real: {len(usuarios_hoy)} {'✅' if server_usuarios_presentes == len(usuarios_hoy) else '❌'}")
            
            # Mostrar primeras asistencias de hoy para debug
            if asistencias_hoy:
                print(f"\n4️⃣ PRIMERAS 3 ASISTENCIAS DE HOY:")
                for i, a in enumerate(asistencias_hoy[:3]):
                    usuario_id = a.get('usuario_id', 'N/A')
                    hora_entrada = a.get('hora_entrada', 'N/A')
                    if hora_entrada != 'N/A':
                        try:
                            hora_entrada = datetime.fromisoformat(hora_entrada.replace('Z', '')).strftime('%H:%M:%S')
                        except:
                            pass
                    print(f"   {i+1}. Usuario {usuario_id} - Entrada: {hora_entrada}")
                    
        else:
            print(f"❌ Error en asistencias: {response2.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_coherencia_estadisticas()
