#!/usr/bin/env python3
"""
Script de prueba para verificar el registro de usuarios con CURP
Ejecutar desde la carpeta backend: python test_registro_curp.py
"""

import requests
import json

# URL de la API (cambiar si es necesario)
API_URL = "https://apipwa.sembrandodatos.com"  # Producción
# API_URL = "http://localhost:8000"  # Local para pruebas

def probar_estructura_tabla():
    """Verificar que la tabla usuarios tenga la columna CURP"""
    print("🔍 Verificando estructura de la tabla usuarios...")
    
    try:
        response = requests.get(f"{API_URL}/debug/usuarios-estructura")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Estructura de tabla verificada:")
            print(f"   - Tabla existe: {data['tabla_existe']}")
            print(f"   - Columna CURP existe: {data['curp_columna_existe']}")
            print(f"   - Total registros: {data['total_registros']}")
            
            print("\n📋 Columnas de la tabla:")
            for col in data['columnas']:
                print(f"   - {col['nombre']}: {col['tipo']} ({'NULL' if col['nullable'] == 'YES' else 'NOT NULL'})")
            
            return data['curp_columna_existe']
        else:
            print(f"❌ Error verificando estructura: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error conectando con la API: {e}")
        return False

def probar_registro_usuario():
    """Probar el registro de un usuario con CURP"""
    print("\n🧪 Probando registro de usuario con CURP...")
    
    # Datos de prueba
    usuario_prueba = {
        "correo": f"prueba_curp_{import_time()}@test.com",
        "nombre_completo": "Usuario Prueba CURP",
        "cargo": "Desarrollador",
        "supervisor": "Supervisor Test",
        "contrasena": "123456",
        "curp": "ABCD123456HEFGHIJ01"  # CURP de prueba válida (18 caracteres)
    }
    
    try:
        response = requests.post(
            f"{API_URL}/usuarios",
            json=usuario_prueba,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Usuario registrado exitosamente:")
            print(f"   - ID: {data['id']}")
            print(f"   - Mensaje: {data['mensaje']}")
            return data['id']
        else:
            print(f"❌ Error en registro: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error registrando usuario: {e}")
        return None

def probar_validaciones_curp():
    """Probar las validaciones de CURP"""
    print("\n🔍 Probando validaciones de CURP...")
    
    casos_prueba = [
        {
            "descripcion": "CURP muy corta (17 caracteres)",
            "curp": "ABCD123456HEFGHIJ0",
            "debe_fallar": True
        },
        {
            "descripcion": "CURP muy larga (19 caracteres)",
            "curp": "ABCD123456HEFGHIJ012",
            "debe_fallar": True
        },
        {
            "descripcion": "CURP vacía",
            "curp": "",
            "debe_fallar": True
        },
        {
            "descripcion": "CURP con caracteres especiales",
            "curp": "ABCD123456HEFGHI@0",
            "debe_fallar": True
        },
        {
            "descripcion": "CURP válida (18 caracteres)",
            "curp": "WXYZ987654ABCDEFGH23",
            "debe_fallar": False
        }
    ]
    
    for i, caso in enumerate(casos_prueba, 1):
        print(f"\n📝 Caso {i}: {caso['descripcion']}")
        
        usuario_prueba = {
            "correo": f"test_val_{i}_{import_time()}@test.com",
            "nombre_completo": f"Usuario Validación {i}",
            "cargo": "Tester",
            "supervisor": None,
            "contrasena": "123456",
            "curp": caso['curp']
        }
        
        try:
            response = requests.post(
                f"{API_URL}/usuarios",
                json=usuario_prueba,
                headers={"Content-Type": "application/json"}
            )
            
            if caso['debe_fallar']:
                if response.status_code != 200:
                    print(f"   ✅ Validación correcta - Error esperado: {response.status_code}")
                else:
                    print(f"   ❌ Validación falló - Se esperaba error pero se registró")
            else:
                if response.status_code == 200:
                    print(f"   ✅ Registro exitoso como se esperaba")
                else:
                    print(f"   ❌ Error inesperado: {response.status_code}")
                    print(f"   Respuesta: {response.text}")
                    
        except Exception as e:
            print(f"   ❌ Error en la prueba: {e}")

def import_time():
    """Importar time y devolver timestamp para IDs únicos"""
    import time
    return int(time.time())

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas del sistema de registro con CURP")
    print("=" * 60)
    
    # 1. Verificar estructura de la tabla
    curp_existe = probar_estructura_tabla()
    
    if not curp_existe:
        print("\n❌ La columna CURP no existe en la tabla usuarios.")
        print("Por favor ejecuta el script SQL 'add_curp_column.sql' primero.")
        return
    
    # 2. Probar registro normal
    user_id = probar_registro_usuario()
    
    # 3. Probar validaciones
    probar_validaciones_curp()
    
    print("\n" + "=" * 60)
    print("🏁 Pruebas completadas")
    
    if user_id:
        print(f"✅ Se registró exitosamente un usuario con ID: {user_id}")
    
    print("\n💡 Próximos pasos:")
    print("1. Verificar en la base de datos que los registros tengan CURP")
    print("2. Probar el formulario web de registro")
    print("3. Verificar que las validaciones funcionen en el frontend")

if __name__ == "__main__":
    main()
