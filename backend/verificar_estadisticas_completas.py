#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def verificar_estadisticas_completas():
    print("🔍 VERIFICANDO ESTADÍSTICAS COMPLETAS CON SALIDAS...")
    
    try:
        # Probar endpoint de estadísticas
        response = requests.get('http://localhost:8000/estadisticas')
        
        if response.status_code == 200:
            data = response.json()
            stats = data.get('estadisticas', {})
            
            print("✅ ESTADÍSTICAS COMPLETAS DEL SERVIDOR:")
            for key, value in stats.items():
                emoji = {
                    'total_usuarios': '👥',
                    'asistencias_hoy': '⬅️',
                    'salidas_hoy': '➡️',
                    'usuarios_presentes': '👤',
                    'total_asistencias': '📊',
                    'total_registros': '📋',
                    'registros_hoy': '📝'
                }.get(key, '📊')
                
                print(f"   {emoji} {key}: {value}")
            
            # Verificar si salidas_hoy está incluido
            salidas_hoy = stats.get('salidas_hoy')
            if salidas_hoy is not None:
                print(f"\n✅ SALIDAS HOY INCLUIDAS: {salidas_hoy}")
                
                # Calcular total de actividades
                entradas = stats.get('asistencias_hoy', 0)
                total_actividades = entradas + salidas_hoy
                print(f"\n📊 CÁLCULO DE ACTIVIDADES:")
                print(f"   Entradas: {entradas}")
                print(f"   Salidas: {salidas_hoy}")
                print(f"   Total actividades: {total_actividades}")
            else:
                print(f"\n❌ SALIDAS HOY NO INCLUIDAS EN LA RESPUESTA")
                
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_estadisticas_completas()
