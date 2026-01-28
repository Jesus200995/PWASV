"""
Script de diagnóstico para verificar el historial de reportes.
Ejecutar cuando el backend esté corriendo.
"""
import requests
import json

# Configuración
BASE_URL = "http://localhost:8000"

def test_historial():
    """Probar el endpoint del historial de reportes"""
    print("=" * 60)
    print("🔍 DIAGNÓSTICO DE HISTORIAL DE REPORTES")
    print("=" * 60)
    
    # Primero, obtener un usuario de prueba
    print("\n1. Obteniendo usuarios existentes...")
    try:
        response = requests.get(f"{BASE_URL}/usuarios", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('usuarios', data) if isinstance(data, dict) else data
            if usuarios and len(usuarios) > 0:
                usuario = usuarios[0]
                usuario_id = usuario.get('id')
                print(f"   ✅ Usuario de prueba: ID {usuario_id} - {usuario.get('nombre_completo', 'Sin nombre')}")
                
                # Probar historial para este usuario
                print(f"\n2. Obteniendo historial para usuario ID {usuario_id}...")
                response2 = requests.get(f"{BASE_URL}/reportes/historial/{usuario_id}", timeout=10)
                print(f"   Status: {response2.status_code}")
                print(f"   Response: {json.dumps(response2.json(), indent=2, ensure_ascii=False)}")
                
                return usuario_id
            else:
                print("   ⚠️ No hay usuarios en la base de datos")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
    
    return None

def test_verificar_reporte(usuario_id):
    """Probar el endpoint de verificación de reporte"""
    if not usuario_id:
        return
    
    print(f"\n3. Verificando si existe reporte para usuario {usuario_id} en Junio 2025...")
    try:
        response = requests.get(
            f"{BASE_URL}/reportes/verificar/{usuario_id}",
            params={"mes": "Junio", "anio": 2025},
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_tabla_reportes():
    """Verificar estructura de la tabla"""
    print("\n4. Verificando datos directamente en BD (a través de endpoint de prueba)...")
    print("   (Este test requiere acceso directo a la BD)")

def main():
    print("\n🚀 Iniciando diagnóstico...")
    print(f"   URL Base: {BASE_URL}")
    
    # Verificar que el servidor esté corriendo
    try:
        requests.get(f"{BASE_URL}/", timeout=5)
        print("   ✅ Servidor backend accesible")
    except:
        print("   ❌ ERROR: El servidor backend no está corriendo en localhost:8000")
        print("   Ejecuta primero: cd backend && uvicorn main:app --reload")
        return
    
    usuario_id = test_historial()
    test_verificar_reporte(usuario_id)
    
    print("\n" + "=" * 60)
    print("🏁 DIAGNÓSTICO COMPLETADO")
    print("=" * 60)

if __name__ == "__main__":
    main()
