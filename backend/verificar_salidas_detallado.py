#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime
import pytz

def verificar_salidas_detallado():
    print("🔍 VERIFICANDO SALIDAS EN TIEMPO REAL CDMX...")
    
    # Obtener fecha CDMX
    cdmx_tz = pytz.timezone('America/Mexico_City')
    fecha_cdmx = datetime.now(cdmx_tz)
    fecha_hoy_cdmx = fecha_cdmx.strftime('%Y-%m-%d')
    print(f"📅 Fecha hoy CDMX: {fecha_hoy_cdmx}")
    print(f"🕐 Hora actual CDMX: {fecha_cdmx.strftime('%H:%M:%S')}")
    
    try:
        # Obtener todas las asistencias
        response = requests.get('http://localhost:8000/asistencias')
        if response.status_code == 200:
            data_asistencias = response.json()
            asistencias = data_asistencias.get('asistencias', [])
            
            print(f"\n📊 Total asistencias en sistema: {len(asistencias)}")
            
            # Filtrar asistencias de hoy
            asistencias_hoy = [a for a in asistencias if a.get('fecha') == fecha_hoy_cdmx]
            print(f"📅 Asistencias de hoy: {len(asistencias_hoy)}")
            
            # Contar entradas y salidas
            con_entrada = [a for a in asistencias_hoy if a.get('hora_entrada')]
            con_salida = [a for a in asistencias_hoy if a.get('hora_salida')]
            solo_entrada = [a for a in asistencias_hoy if a.get('hora_entrada') and not a.get('hora_salida')]
            entrada_y_salida = [a for a in asistencias_hoy if a.get('hora_entrada') and a.get('hora_salida')]
            
            print(f"\n📊 ANÁLISIS DETALLADO DE HOY ({fecha_hoy_cdmx}):")
            print(f"   ⬅️  Con entrada registrada: {len(con_entrada)}")
            print(f"   ➡️  Con salida registrada: {len(con_salida)}")
            print(f"   🔄 Solo entrada (sin salida): {len(solo_entrada)}")
            print(f"   ✅ Entrada y salida completas: {len(entrada_y_salida)}")
            
            if con_salida:
                print(f"\n➡️  PRIMERAS 10 SALIDAS DE HOY:")
                for i, a in enumerate(con_salida[:10]):
                    usuario_id = a.get('usuario_id', 'N/A')
                    hora_entrada = a.get('hora_entrada', 'N/A')
                    hora_salida = a.get('hora_salida', 'N/A')
                    
                    # Formatear horas
                    try:
                        if hora_entrada != 'N/A':
                            hora_entrada = datetime.fromisoformat(hora_entrada.replace('Z', '')).strftime('%H:%M:%S')
                    except:
                        pass
                    
                    try:
                        if hora_salida != 'N/A':
                            hora_salida = datetime.fromisoformat(hora_salida.replace('Z', '')).strftime('%H:%M:%S')
                    except:
                        pass
                    
                    print(f"   {i+1}. Usuario {usuario_id} - Entrada: {hora_entrada}, Salida: {hora_salida}")
            else:
                print(f"\n➡️  NO HAY SALIDAS REGISTRADAS HOY")
                
            # Mostrar últimas 5 asistencias para ver el patrón
            print(f"\n🔍 ÚLTIMAS 5 ASISTENCIAS DE HOY (para ver patrón):")
            for i, a in enumerate(asistencias_hoy[-5:]):
                usuario_id = a.get('usuario_id', 'N/A')
                hora_entrada = a.get('hora_entrada', 'N/A')
                hora_salida = a.get('hora_salida', 'N/A')
                
                # Formatear horas
                try:
                    if hora_entrada != 'N/A':
                        hora_entrada = datetime.fromisoformat(hora_entrada.replace('Z', '')).strftime('%H:%M:%S')
                except:
                    pass
                
                try:
                    if hora_salida != 'N/A':
                        hora_salida = datetime.fromisoformat(hora_salida.replace('Z', '')).strftime('%H:%M:%S')
                except:
                    pass
                
                estado_salida = "SIN SALIDA" if hora_salida == 'N/A' else f"SALIDA: {hora_salida}"
                print(f"   {len(asistencias_hoy)-4+i}. Usuario {usuario_id} - Entrada: {hora_entrada} - {estado_salida}")
                
        else:
            print(f"❌ Error al obtener asistencias: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_salidas_detallado()
