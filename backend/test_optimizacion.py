#!/usr/bin/env python3
"""
Test rápido para verificar que el nuevo endpoint optimizado funciona correctamente.
"""

import requests
import time
import json

# Configuración
API_URL = "https://apipwa.sembrandodatos.com"

def test_endpoint_optimizado():
    """Probar el nuevo endpoint optimizado"""
    print("🧪 PROBANDO ENDPOINT OPTIMIZADO")
    print("="*50)
    
    # Test 1: Endpoint original (debería tener límite)
    print("\n1️⃣ Probando endpoint original con límite...")
    try:
        start_time = time.time()
        response = requests.get(f"{API_URL}/registros?limit=100", timeout=15)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Respuesta exitosa: {len(data.get('registros', []))} registros ({end_time - start_time:.2f}s)")
        else:
            print(f"   ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Nuevo endpoint admin
    print("\n2️⃣ Probando nuevo endpoint admin...")
    try:
        start_time = time.time()
        response = requests.get(f"{API_URL}/admin/registros?page=1&page_size=50", timeout=15)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            registros = data.get('registros', [])
            total = data.get('total', 0)
            page = data.get('page', 1)
            print(f"   ✅ Respuesta exitosa: {len(registros)} registros de {total} totales")
            print(f"   📄 Página {page}, Tiempo: {end_time - start_time:.2f}s")
            print(f"   📊 Estructura: {list(data.keys())}")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text[:100]}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Endpoint de estadísticas
    print("\n3️⃣ Probando endpoint de estadísticas...")
    try:
        start_time = time.time()
        response = requests.get(f"{API_URL}/estadisticas", timeout=10)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            stats = data.get('estadisticas', {})
            print(f"   ✅ Estadísticas obtenidas ({end_time - start_time:.2f}s):")
            print(f"       • Total registros: {stats.get('total_registros', 'N/A')}")
            print(f"       • Registros hoy: {stats.get('registros_hoy', 'N/A')}")
            print(f"       • Total usuarios: {stats.get('total_usuarios', 'N/A')}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Verificar API funciona
    print("\n4️⃣ Verificando estado general de la API...")
    try:
        response = requests.get(f"{API_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("   ✅ API respondiendo correctamente")
        else:
            print(f"   ⚠️ API responde con código {response.status_code}")
    except Exception as e:
        print(f"   ❌ API no responde: {e}")

def test_stress_ligero():
    """Prueba de estrés ligera para verificar estabilidad"""
    print("\n💪 PRUEBA DE ESTRÉS LIGERA")
    print("="*50)
    
    total_requests = 5
    success_count = 0
    total_time = 0
    
    for i in range(1, total_requests + 1):
        try:
            print(f"   📡 Petición {i}/{total_requests}...")
            start_time = time.time()
            
            response = requests.get(f"{API_URL}/admin/registros?page={i}&page_size=20", timeout=10)
            
            end_time = time.time()
            duration = end_time - start_time
            total_time += duration
            
            if response.status_code == 200:
                success_count += 1
                data = response.json()
                registros_count = len(data.get('registros', []))
                print(f"       ✅ Éxito: {registros_count} registros ({duration:.2f}s)")
            else:
                print(f"       ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"       ❌ Error: {e}")
        
        # Pequeña pausa entre peticiones
        time.sleep(0.5)
    
    avg_time = total_time / total_requests if total_requests > 0 else 0
    success_rate = (success_count / total_requests) * 100 if total_requests > 0 else 0
    
    print(f"\n📊 RESULTADOS:")
    print(f"   • Peticiones exitosas: {success_count}/{total_requests} ({success_rate:.1f}%)")
    print(f"   • Tiempo promedio: {avg_time:.2f}s")
    print(f"   • Tiempo total: {total_time:.2f}s")
    
    if success_rate >= 80 and avg_time < 5:
        print("   🎉 ¡PRUEBA EXITOSA! El servidor está estable")
    elif success_rate >= 60:
        print("   ⚠️ Estabilidad moderada. Revisar configuración")
    else:
        print("   ❌ Problemas detectados. Revisar servidor")

def main():
    """Función principal"""
    print("🔬 TEST DE FUNCIONALIDAD - API PWA OPTIMIZADA")
    print("=" * 60)
    print(f"🌐 Probando: {API_URL}")
    print(f"🕐 Hora: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ejecutar tests
    test_endpoint_optimizado()
    test_stress_ligero()
    
    print("\n" + "="*60)
    print("🎯 CONCLUSIÓN")
    print("="*60)
    print("Si todos los tests pasaron:")
    print("✅ La optimización fue exitosa")
    print("✅ El admin-pwa debería cargar sin problemas")
    print("✅ El servidor está estable")
    print("\nSi hay errores:")
    print("🔧 Ejecutar: python diagnostico_api.py")
    print("🔧 Revisar logs del servidor")
    print("🔧 Verificar optimizar_indices.py")

if __name__ == "__main__":
    main()
