import requests
import json

# URL base de la API
BASE_URL = "http://localhost:8000"

def test_actualizar_notificacion():
    """Probar la actualización de una notificación"""
    
    print("=" * 60)
    print("TEST: Actualizar Notificación")
    print("=" * 60)
    
    # Primero, obtener la lista de notificaciones para tener un ID válido
    print("\n1. Obteniendo lista de notificaciones...")
    response = requests.get(f"{BASE_URL}/notificaciones")
    
    if response.status_code != 200:
        print(f"❌ Error al obtener notificaciones: {response.status_code}")
        print(f"Respuesta: {response.text}")
        return
    
    data = response.json()
    notificaciones = data.get('notificaciones', [])
    
    if not notificaciones:
        print("❌ No hay notificaciones para actualizar")
        print("💡 Crea una notificación primero desde la interfaz web")
        return
    
    # Tomar la primera notificación
    notificacion_id = notificaciones[0]['id']
    print(f"✅ Notificación seleccionada: ID {notificacion_id}")
    print(f"   Título actual: {notificaciones[0]['titulo']}")
    print(f"   Enviada a todos: {notificaciones[0]['enviada_a_todos']}")
    
    # Preparar datos de actualización
    print(f"\n2. Actualizando notificación {notificacion_id}...")
    
    datos_actualizacion = {
        'titulo': f"[ACTUALIZADA] {notificaciones[0]['titulo']}",
        'subtitulo': 'Subtítulo actualizado desde el test',
        'descripcion': 'Esta notificación fue actualizada mediante el script de prueba',
        'enlace_url': 'https://ejemplo.com/actualizado',
        'enviada_a_todos': True  # Cambiar a todos
    }
    
    # Enviar petición de actualización
    response = requests.put(
        f"{BASE_URL}/notificaciones/{notificacion_id}",
        data=datos_actualizacion
    )
    
    print(f"\n3. Resultado de la actualización:")
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        resultado = response.json()
        print(f"   ✅ {resultado.get('message', 'Actualización exitosa')}")
        print(f"   Título actualizado: {resultado.get('titulo', 'N/A')}")
        
        # Verificar la actualización
        print(f"\n4. Verificando cambios...")
        verify_response = requests.get(f"{BASE_URL}/notificaciones/{notificacion_id}")
        
        if verify_response.status_code == 200:
            notificacion_actualizada = verify_response.json()
            print(f"   ✅ Notificación verificada:")
            print(f"      Título: {notificacion_actualizada.get('titulo')}")
            print(f"      Subtítulo: {notificacion_actualizada.get('subtitulo')}")
            print(f"      Descripción: {notificacion_actualizada.get('descripcion')}")
            print(f"      Enlace: {notificacion_actualizada.get('enlace_url')}")
            print(f"      Enviada a todos: {notificacion_actualizada.get('enviada_a_todos')}")
        else:
            print(f"   ⚠️ No se pudo verificar: {verify_response.status_code}")
    else:
        print(f"   ❌ Error en la actualización")
        print(f"   Respuesta: {response.text}")
        
        # Intentar parsear el error
        try:
            error_data = response.json()
            print(f"   Detalle del error: {error_data.get('detail', 'Sin detalles')}")
        except:
            pass
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        test_actualizar_notificacion()
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("💡 Asegúrate de que el backend esté ejecutándose en http://localhost:8000")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
