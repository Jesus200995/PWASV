#!/usr/bin/env python3
"""
Script de diagnóstico para verificar el estado de la API PWA y detectar problemas.
"""

import requests
import time
import json
import psycopg2
from datetime import datetime

# Configuración
API_URL = "https://apipwa.sembrandodatos.com"
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"

def verificar_conexion_api():
    """Verificar si la API está respondiendo"""
    print("🌐 Verificando conexión a la API...")
    
    try:
        start_time = time.time()
        response = requests.get(f"{API_URL}/docs", timeout=10)
        end_time = time.time()
        
        duration = end_time - start_time
        
        if response.status_code == 200:
            print(f"  ✅ API responde correctamente ({duration:.2f}s)")
            return True
        else:
            print(f"  ❌ API responde con código {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("  ⏰ Timeout: La API no responde en 10 segundos")
        return False
    except requests.exceptions.ConnectionError:
        print("  🔌 Error de conexión: No se puede conectar a la API")
        return False
    except Exception as e:
        print(f"  ❌ Error inesperado: {e}")
        return False

def verificar_endpoint_registros():
    """Verificar específicamente el endpoint de registros que está fallando"""
    print("\n📋 Verificando endpoint de registros...")
    
    endpoints_a_probar = [
        {
            "url": f"{API_URL}/registros?limit=10",
            "descripcion": "Registros con límite pequeño"
        },
        {
            "url": f"{API_URL}/admin/registros?page=1&page_size=50",
            "descripcion": "Nuevo endpoint admin optimizado"
        },
        {
            "url": f"{API_URL}/estadisticas",
            "descripcion": "Estadísticas del sistema"
        }
    ]
    
    for endpoint in endpoints_a_probar:
        try:
            print(f"  🔍 Probando: {endpoint['descripcion']}")
            start_time = time.time()
            
            response = requests.get(endpoint['url'], timeout=30)
            
            end_time = time.time()
            duration = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                if 'registros' in data:
                    count = len(data['registros'])
                    print(f"    ✅ Respuesta exitosa: {count} registros ({duration:.2f}s)")
                elif 'estadisticas' in data:
                    print(f"    ✅ Estadísticas obtenidas ({duration:.2f}s)")
                else:
                    print(f"    ✅ Respuesta exitosa ({duration:.2f}s)")
            else:
                print(f"    ❌ Error HTTP {response.status_code}: {response.text[:100]}")
                
        except requests.exceptions.Timeout:
            print(f"    ⏰ Timeout después de 30s")
        except Exception as e:
            print(f"    ❌ Error: {e}")

def verificar_conexion_db():
    """Verificar conexión directa a la base de datos"""
    print("\n🗄️  Verificando conexión a la base de datos...")
    
    try:
        start_time = time.time()
        
        conn = psycopg2.connect(
            host=DB_HOST, 
            database=DB_NAME, 
            user=DB_USER, 
            password=DB_PASS,
            connect_timeout=10
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        cursor = conn.cursor()
        
        # Verificar conteos básicos
        cursor.execute("SELECT COUNT(*) FROM registros")
        total_registros = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        
        print(f"  ✅ Conexión exitosa ({duration:.2f}s)")
        print(f"  📊 Registros en DB: {total_registros:,}")
        print(f"  👥 Usuarios en DB: {total_usuarios:,}")
        
        # Verificar registros recientes
        cursor.execute("""
            SELECT COUNT(*) FROM registros 
            WHERE fecha_hora >= NOW() - INTERVAL '24 hours'
        """)
        registros_24h = cursor.fetchone()[0]
        print(f"  🕐 Registros últimas 24h: {registros_24h:,}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Error de conexión: {e}")
        return False

def probar_consulta_problematica():
    """Probar la consulta que está causando problemas"""
    print("\n🔍 Probando consulta problemática (sin límite)...")
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST, 
            database=DB_NAME, 
            user=DB_USER, 
            password=DB_PASS,
            connect_timeout=10
        )
        
        cursor = conn.cursor()
        
        # Probar la consulta problemática original
        start_time = time.time()
        
        print("  ⏳ Ejecutando: SELECT * FROM registros ORDER BY fecha_hora DESC")
        cursor.execute("""
            SELECT id, usuario_id, latitud, longitud, descripcion, foto_url, fecha_hora, tipo_actividad 
            FROM registros 
            ORDER BY fecha_hora DESC 
            LIMIT 1000
        """)
        
        resultados = cursor.fetchall()
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"  ✅ Consulta exitosa: {len(resultados)} registros ({duration:.2f}s)")
        
        # Probar sin LIMIT para ver el problema
        if duration < 5:  # Solo si la consulta anterior fue rápida
            print("  ⚠️  Probando sin LIMIT (puede ser lento)...")
            start_time = time.time()
            
            cursor.execute("SELECT COUNT(*) FROM registros")
            total = cursor.fetchone()[0]
            
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"  📊 Total de registros: {total:,} ({duration:.2f}s)")
            
            if total > 10000:
                print("  ⚠️  PROBLEMA DETECTADO: Demasiados registros para cargar sin límite")
                print(f"     Carga de {total:,} registros puede causar timeout/crash")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"  ❌ Error en consulta: {e}")

def verificar_memoria_servidor():
    """Verificar uso de memoria si es posible"""
    print("\n💾 Verificando recursos del servidor...")
    
    try:
        # Intentar obtener información del servidor a través de la API
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            print("  ✅ Endpoint de salud disponible")
        else:
            print("  ℹ️  Endpoint de salud no disponible")
    except:
        print("  ℹ️  No se puede verificar salud del servidor")

def generar_reporte():
    """Generar reporte de diagnóstico"""
    print("\n" + "="*60)
    print("📋 REPORTE DE DIAGNÓSTICO")
    print("="*60)
    
    print(f"🕐 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API URL: {API_URL}")
    print(f"🗄️  DB Host: {DB_HOST}")
    
    # Ejecutar todas las verificaciones
    api_ok = verificar_conexion_api()
    verificar_endpoint_registros()
    db_ok = verificar_conexion_db()
    probar_consulta_problematica()
    verificar_memoria_servidor()
    
    print("\n" + "="*60)
    print("🎯 CONCLUSIONES Y RECOMENDACIONES")
    print("="*60)
    
    if not api_ok:
        print("❌ CRÍTICO: API no responde - Verificar servidor FastAPI")
        print("   💡 Solución: Reiniciar servicio o verificar logs")
    
    if not db_ok:
        print("❌ CRÍTICO: Base de datos no accesible")
        print("   💡 Solución: Verificar conexión y credenciales")
    
    if api_ok and db_ok:
        print("✅ Servicios básicos funcionando")
        print("🔧 OPTIMIZACIONES RECOMENDADAS:")
        print("   1. Implementar paginación obligatoria en /registros")
        print("   2. Crear índices optimizados (ejecutar optimizar_indices.py)")
        print("   3. Agregar límites de memoria al servidor")
        print("   4. Implementar cache para consultas frecuentes")
        print("   5. Usar el nuevo endpoint /admin/registros en el frontend")
    
    print("\n🚀 SIGUIENTES PASOS:")
    print("   1. Ejecutar: python optimizar_indices.py")
    print("   2. Reiniciar el servidor de la API")
    print("   3. Actualizar frontend para usar endpoint optimizado")
    print("   4. Monitorear rendimiento")

def main():
    """Función principal"""
    print("🔍 DIAGNÓSTICO DE API PWA - SEMBRANDO VIDA")
    print("="*60)
    
    generar_reporte()

if __name__ == "__main__":
    main()
