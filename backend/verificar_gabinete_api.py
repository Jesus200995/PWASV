#!/usr/bin/env python3
"""
Script para verificar registros de gabinete usando la API
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
        
        if response.status_code == 200:
            registros = response.json()
            print(f"✅ Total registros obtenidos: {len(registros)}")
            
            # Filtrar por tipo de actividad
            tipos_actividad = {}
            registros_gabinete = []
            
            for registro in registros:
                tipo = registro.get('tipo_actividad', 'sin_tipo')
                tipos_actividad[tipo] = tipos_actividad.get(tipo, 0) + 1
                
                if tipo == 'gabinete':
                    registros_gabinete.append(registro)
            
            print(f"\n📊 DISTRIBUCIÓN POR TIPO DE ACTIVIDAD:")
            for tipo, cantidad in tipos_actividad.items():
                print(f"   - {tipo}: {cantidad} registros")
            
            print(f"\n🎯 REGISTROS DE GABINETE ENCONTRADOS: {len(registros_gabinete)}")
            
            if registros_gabinete:
                print("\n📋 DETALLES DE REGISTROS DE GABINETE:")
                for i, reg in enumerate(registros_gabinete[:10]):  # Mostrar solo los primeros 10
                    print(f"\n   Registro {i+1}:")
                    print(f"   - ID: {reg.get('id')}")
                    print(f"   - Usuario ID: {reg.get('usuario_id')}")
                    print(f"   - Fecha: {reg.get('fecha_hora')}")
                    print(f"   - Coordenadas: {reg.get('coordenadas')}")
                    print(f"   - Descripción: {reg.get('descripcion', 'N/A')}")
                    
                    # Verificar si tiene imagen
                    imagen_campos = ['imagen_url', 'foto_url', 'imagen', 'foto']
                    for campo in imagen_campos:
                        if reg.get(campo):
                            print(f"   - {campo}: {reg.get(campo)}")
            else:
                print("   ❌ No se encontraron registros de gabinete")
                
                # Mostrar algunos registros de muestra para verificar estructura
                print(f"\n🔍 MUESTRA DE REGISTROS (primeros 5):")
                for i, reg in enumerate(registros[:5]):
                    print(f"\n   Registro {i+1}:")
                    print(f"   - ID: {reg.get('id')}")
                    print(f"   - Usuario ID: {reg.get('usuario_id')}")
                    print(f"   - Tipo: {reg.get('tipo_actividad')}")
                    print(f"   - Fecha: {reg.get('fecha_hora')}")
                    print(f"   - Todas las claves: {list(reg.keys())}")
                    
        else:
            print(f"❌ Error al obtener registros: {response.status_code}")
            print(f"   Respuesta: {response.text}")
    
    except Exception as e:
        print(f"❌ Error al verificar registros: {e}")
    
    try:
        # 2. Verificar endpoint de asistencias también
        print(f"\n2️⃣ Verificando endpoint de asistencias...")
        response = requests.get(f"{API_URL}/asistencias", timeout=15)
        
        if response.status_code == 200:
            asistencias = response.json()
            print(f"✅ Total asistencias obtenidas: {len(asistencias)}")
            
            # Verificar tipos en asistencias
            tipos_asistencia = {}
            for asistencia in asistencias:
                tipo = asistencia.get('tipo_actividad', 'sin_tipo')
                tipos_asistencia[tipo] = tipos_asistencia.get(tipo, 0) + 1
            
            print(f"\n📊 TIPOS EN ASISTENCIAS:")
            for tipo, cantidad in tipos_asistencia.items():
                print(f"   - {tipo}: {cantidad}")
                
        else:
            print(f"❌ Error al obtener asistencias: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error al verificar asistencias: {e}")
    
    print("\n" + "=" * 60)
    print("✅ VERIFICACIÓN COMPLETADA")

def crear_registro_gabinete_prueba():
    """Crear un registro de gabinete de prueba"""
    
    print("\n🧪 CREANDO REGISTRO DE GABINETE DE PRUEBA...")
    
    # Datos de prueba para gabinete
    datos_gabinete = {
        "usuario_id": 1,  # Usar un usuario existente
        "tipo_actividad": "gabinete",
        "coordenadas": "19.432608,-99.133209",  # CDMX
        "descripcion": "Actividad de gabinete de prueba - análisis de datos",
        "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        response = requests.post(f"{API_URL}/registrar", json=datos_gabinete, timeout=10)
        
        if response.status_code in [200, 201]:
            print("✅ Registro de gabinete creado exitosamente!")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Error al crear registro: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error al crear registro de prueba: {e}")

if __name__ == "__main__":
    verificar_registros_gabinete()
    
    # Preguntar si quiere crear un registro de prueba
    respuesta = input("\n¿Quieres crear un registro de gabinete de prueba? (s/n): ")
    if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        crear_registro_gabinete_prueba()
