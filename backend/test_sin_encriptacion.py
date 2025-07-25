import requests
import json

# URL de la API
BASE_URL = "https://apipwa.sembrandodatos.com"

def test_registro_sin_encriptacion():
    """Prueba el registro de usuario sin encriptación de contraseña"""
    print("🔐 Probando registro sin encriptación de contraseña...")
    
    # Datos de prueba
    usuario_datos = {
        "correo": f"test_sin_encriptacion@example.com",
        "nombre_completo": "Usuario Test Sin Encriptación",
        "cargo": "Empleado",
        "supervisor": "Supervisor Test",
        "contrasena": "password123",  # Contraseña en texto plano
        "curp": "ABCD123456HDFGTR90"
    }
    
    try:
        # Registro
        response = requests.post(f"{BASE_URL}/usuarios", json=usuario_datos)
        print(f"📝 Status registro: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Usuario registrado exitosamente: {result}")
            
            # Probar login inmediatamente
            print("\n🔓 Probando login con contraseña sin encriptar...")
            login_datos = {
                "correo": usuario_datos["correo"],
                "contrasena": usuario_datos["contrasena"]
            }
            
            login_response = requests.post(f"{BASE_URL}/login", json=login_datos)
            print(f"🔑 Status login: {login_response.status_code}")
            
            if login_response.status_code == 200:
                login_result = login_response.json()
                print(f"✅ Login exitoso: {login_result}")
                print("🎉 ¡PERFECTO! El sistema funciona sin encriptación")
            else:
                print(f"❌ Error en login: {login_response.text}")
                
        else:
            print(f"❌ Error en registro: {response.text}")
            
    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    test_registro_sin_encriptacion()
