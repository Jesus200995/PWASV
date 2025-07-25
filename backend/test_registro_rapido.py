import requests
import json
import time

# URL de la API
API_URL = "https://apipwa.sembrandodatos.com"

def test_registro_simple():
    """Probar registro sin CURP"""
    print("🧪 Probando registro SIN CURP...")
    
    usuario_test = {
        "correo": f"test_sin_curp_{int(time.time())}@ejemplo.com",
        "nombre_completo": "Usuario Test Sin CURP",
        "cargo": "Tester",
        "supervisor": "Supervisor Test",
        "contrasena": "123456"
    }
    
    try:
        response = requests.post(f"{API_URL}/usuarios", json=usuario_test)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registro SIN CURP exitoso!")
            return True
        else:
            print("❌ Error en registro SIN CURP")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_registro_con_curp():
    """Probar registro con CURP"""
    print("\n🧪 Probando registro CON CURP...")
    
    usuario_test = {
        "correo": f"test_con_curp_{int(time.time())}@ejemplo.com", 
        "nombre_completo": "Usuario Test Con CURP",
        "cargo": "Tester",
        "supervisor": "Supervisor Test",
        "contrasena": "123456",
        "curp": "ABCD123456HEFGHIJ01"
    }
    
    try:
        response = requests.post(f"{API_URL}/usuarios", json=usuario_test)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registro CON CURP exitoso!")
            return True
        else:
            print("❌ Error en registro CON CURP")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de registro")
    print("=" * 50)
    
    # Probar ambos casos
    sin_curp = test_registro_simple()
    con_curp = test_registro_con_curp()
    
    print("\n" + "=" * 50)
    print("📊 RESULTADOS:")
    print(f"  Sin CURP: {'✅ OK' if sin_curp else '❌ FALLO'}")
    print(f"  Con CURP: {'✅ OK' if con_curp else '❌ FALLO'}")
    
    if sin_curp or con_curp:
        print("\n🎉 Al menos un caso funciona! El sistema está operativo.")
    else:
        print("\n💥 Ambos casos fallaron. Revisar configuración del servidor.")
