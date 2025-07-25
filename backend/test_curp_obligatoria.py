import requests
import json
import time

# URL de la API
API_URL = "https://apipwa.sembrandodatos.com"

def test_registro_obligatorio_curp():
    """Probar registro CON CURP obligatoria"""
    print("🧪 Probando registro CON CURP obligatoria...")
    
    usuario_test = {
        "correo": f"test_curp_obligatoria_{int(time.time())}@ejemplo.com",
        "nombre_completo": "Usuario Test CURP Obligatoria",
        "cargo": "Tester",
        "supervisor": "Supervisor Test",
        "contrasena": "123456",
        "curp": "WXYZ987654ABCDEFGH23"
    }
    
    try:
        response = requests.post(f"{API_URL}/usuarios", json=usuario_test)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Registro con CURP obligatoria exitoso!")
            return True
        else:
            print("❌ Error en registro con CURP obligatoria")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_registro_sin_curp_debe_fallar():
    """Probar que registro SIN CURP debe fallar"""
    print("\n🧪 Probando registro SIN CURP (debe fallar)...")
    
    usuario_test = {
        "correo": f"test_sin_curp_{int(time.time())}@ejemplo.com",
        "nombre_completo": "Usuario Test Sin CURP",
        "cargo": "Tester",
        "supervisor": "Supervisor Test",
        "contrasena": "123456"
        # NO incluir CURP - debe fallar
    }
    
    try:
        response = requests.post(f"{API_URL}/usuarios", json=usuario_test)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 400:
            print("✅ Correcto! El registro sin CURP falló como se esperaba")
            return True
        elif response.status_code == 200:
            print("❌ Error! El registro sin CURP no debería funcionar")
            return False
        else:
            print(f"❌ Error inesperado: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_curp_invalida():
    """Probar CURP inválida"""
    print("\n🧪 Probando CURP inválida (debe fallar)...")
    
    usuario_test = {
        "correo": f"test_curp_invalida_{int(time.time())}@ejemplo.com",
        "nombre_completo": "Usuario Test CURP Inválida",
        "cargo": "Tester",
        "supervisor": "Supervisor Test",
        "contrasena": "123456",
        "curp": "ABCD123"  # Solo 7 caracteres - debe fallar
    }
    
    try:
        response = requests.post(f"{API_URL}/usuarios", json=usuario_test)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 400:
            print("✅ Correcto! CURP inválida rechazada como se esperaba")
            return True
        elif response.status_code == 200:
            print("❌ Error! CURP inválida no debería funcionar")
            return False
        else:
            print(f"❌ Error inesperado: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de CURP obligatoria")
    print("=" * 60)
    
    # Probar casos
    curp_ok = test_registro_obligatorio_curp()
    sin_curp_falla = test_registro_sin_curp_debe_fallar()
    curp_invalida_falla = test_curp_invalida()
    
    print("\n" + "=" * 60)
    print("📊 RESULTADOS:")
    print(f"  Con CURP válida: {'✅ OK' if curp_ok else '❌ FALLO'}")
    print(f"  Sin CURP (debe fallar): {'✅ OK' if sin_curp_falla else '❌ FALLO'}")
    print(f"  CURP inválida (debe fallar): {'✅ OK' if curp_invalida_falla else '❌ FALLO'}")
    
    if curp_ok and sin_curp_falla and curp_invalida_falla:
        print("\n🎉 ¡PERFECTO! Todas las validaciones funcionan correctamente.")
        print("✅ CURP es obligatoria y se valida correctamente")
    else:
        print("\n⚠️ Algunas validaciones no funcionan como se esperaba")
