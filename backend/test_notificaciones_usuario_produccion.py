import requests
import json

# Configuración de la API
API_BASE_URL = "https://apipwa.sembrandodatos.com"

def test_notificaciones_usuario():
    """
    Probar el endpoint GET /notificaciones/usuario/{usuario_id}
    """
    try:
        # ID de usuario de prueba (usar un ID que exista en tu base de datos)
        usuario_id = 1  # Cambia este ID por uno que exista
        
        print(f"🧪 Probando GET /notificaciones/usuario/{usuario_id}")
        print(f"🌐 URL: {API_BASE_URL}")
        
        # Hacer petición al endpoint
        response = requests.get(f"{API_BASE_URL}/notificaciones/usuario/{usuario_id}", timeout=10)
        
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
            print(f"Response: {response.text}")
            return False
            
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se pudo conectar al servidor")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_varios_usuarios():
    """
    Probar con diferentes IDs de usuario
    """
    print("\n🧪 Probando con diferentes IDs de usuario:")
    
    for usuario_id in [1, 2, 3]:
        print(f"\n--- Usuario ID: {usuario_id} ---")
        try:
            response = requests.get(f"{API_BASE_URL}/notificaciones/usuario/{usuario_id}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                usuario_nombre = data.get('usuario', {}).get('nombre_completo', 'No especificado')
                total_notif = data.get('total', 0)
                print(f"✅ {usuario_nombre}: {total_notif} notificaciones")
            elif response.status_code == 404:
                print(f"❌ Usuario {usuario_id} no encontrado")
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del endpoint de notificaciones de usuario")
    print("🌐 Probando con API de producción: https://apipwa.sembrandodatos.com")
    print("=" * 60)
    
    # Test 1: Endpoint básico
    test_notificaciones_usuario()
    
    # Test 2: Probar varios usuarios
    test_varios_usuarios()
    
    print("\n🏁 Pruebas completadas")
