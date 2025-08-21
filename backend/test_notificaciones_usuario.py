import requests
import json

# Configuración de la API
API_BASE_URL = "http://localhost:8000"

def test_notificaciones_usuario():
    """
    Probar el endpoint GET /notificaciones/usuario/{usuario_id}
    """
    try:
        # ID de usuario de prueba (usar un ID que exista en tu base de datos)
        usuario_id = 1  # Cambia este ID por uno que exista
        
        print(f"🧪 Probando GET /notificaciones/usuario/{usuario_id}")
        
        # Hacer petición al endpoint
        response = requests.get(f"{API_BASE_URL}/notificaciones/usuario/{usuario_id}")
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ Respuesta exitosa:")
            print(f"📊 Total de notificaciones: {data.get('total', 0)}")
            print(f"👤 Usuario: {data.get('usuario', {}).get('nombre_completo', 'No especificado')}")
            print(f"📋 Notificaciones obtenidas: {len(data.get('notificaciones', []))}")
            
            # Mostrar las primeras notificaciones
            notificaciones = data.get('notificaciones', [])
            if notificaciones:
                print("\n📝 Primeras notificaciones:")
                for i, notif in enumerate(notificaciones[:3], 1):
                    print(f"  {i}. {notif.get('titulo', 'Sin título')}")
                    print(f"     📅 Fecha: {notif.get('fecha_creacion', 'Sin fecha')}")
                    print(f"     📎 Archivo: {'Sí' if notif.get('archivo_nombre') else 'No'}")
                    print(f"     🎯 Enviado a todos: {'Sí' if notif.get('enviada_a_todos') else 'No'}")
                    print()
            else:
                print("📭 No se encontraron notificaciones para este usuario")
            
            return True
            
        elif response.status_code == 404:
            print("❌ Usuario no encontrado")
            return False
            
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se pudo conectar al servidor")
        print("💡 Asegúrate de que el backend esté ejecutándose en localhost:8000")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_notificaciones_usuario_con_paginacion():
    """
    Probar el endpoint con parámetros de paginación
    """
    try:
        usuario_id = 1
        
        print(f"🧪 Probando paginación para usuario {usuario_id}")
        
        # Probar con limit y offset
        response = requests.get(
            f"{API_BASE_URL}/notificaciones/usuario/{usuario_id}",
            params={"limit": 5, "offset": 0}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Paginación exitosa: {len(data.get('notificaciones', []))} notificaciones obtenidas")
            print(f"📊 Parámetros: limit={data.get('limit')}, offset={data.get('offset')}")
            return True
        else:
            print(f"❌ Error en paginación: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba de paginación: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del endpoint de notificaciones de usuario")
    print("=" * 60)
    
    # Test 1: Endpoint básico
    test_notificaciones_usuario()
    
    print("\n" + "=" * 60)
    
    # Test 2: Paginación
    test_notificaciones_usuario_con_paginacion()
    
    print("\n🏁 Pruebas completadas")
