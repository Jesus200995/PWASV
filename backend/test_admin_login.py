#!/usr/bin/env python3
"""
Script para probar el endpoint de login de administrador
"""
import requests
import json

def test_admin_login():
    """Probar el endpoint de login administrativo"""
    
    # URLs para probar
    urls = [
        'http://localhost:8000/admin/login',
        'https://apipwa.sembrandodatos.com/admin/login'
    ]
    
    # Datos de login para probar
    test_credentials = [
        {'username': 'admin', 'password': 'admin123'},
        {'username': 'admin', 'password': 'admin'},
    ]
    
    for url in urls:
        print(f"\n🔍 Probando URL: {url}")
        
        # Verificar primero si el endpoint existe
        try:
            response = requests.options(url, timeout=5)
            print(f"   OPTIONS status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ No se puede conectar a {url}: {e}")
            continue
        
        # Probar con diferentes credenciales
        for creds in test_credentials:
            try:
                print(f"   🔐 Probando credenciales: {creds['username']}/{'*' * len(creds['password'])}")
                
                # Preparar datos en formato form-urlencoded
                form_data = {
                    'grant_type': '',
                    'username': creds['username'],
                    'password': creds['password'],
                    'scope': '',
                    'client_id': '',
                    'client_secret': ''
                }
                
                response = requests.post(
                    url, 
                    data=form_data,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'},
                    timeout=10
                )
                
                print(f"   Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Login exitoso!")
                    print(f"   Token recibido: {data.get('access_token', 'No token')[:50]}...")
                    print(f"   User info: {data.get('user_info', 'No user info')}")
                    return True
                    
                elif response.status_code == 422:
                    print(f"   ❌ Error 422 (Validation Error)")
                    try:
                        error_detail = response.json()
                        print(f"   Detalles: {json.dumps(error_detail, indent=2)}")
                    except:
                        print(f"   Response text: {response.text}")
                        
                elif response.status_code == 400:
                    print(f"   ❌ Error 400 (Bad Request)")
                    try:
                        error_detail = response.json()
                        print(f"   Detalles: {error_detail}")
                    except:
                        print(f"   Response text: {response.text}")
                        
                else:
                    print(f"   ❌ Error {response.status_code}")
                    print(f"   Response: {response.text[:200]}")
                    
            except Exception as e:
                print(f"   ❌ Error en request: {e}")
    
    return False

def check_admin_users_table():
    """Verificar la tabla admin_users en local"""
    print("\n📋 Verificando tabla admin_users local...")
    try:
        import psycopg2
        
        conn = psycopg2.connect(
            host="localhost",
            database="asistencias_db",
            user="asistencias_user",
            password="123456"
        )
        cursor = conn.cursor()
        
        # Verificar si la tabla existe
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'admin_users'
            )
        """)
        
        table_exists = cursor.fetchone()[0]
        print(f"   Tabla admin_users existe: {table_exists}")
        
        if table_exists:
            # Obtener usuarios admin
            cursor.execute("SELECT id, username, rol FROM admin_users")
            admin_users = cursor.fetchall()
            print(f"   Usuarios admin encontrados: {len(admin_users)}")
            
            for user in admin_users:
                print(f"   - ID: {user[0]}, Username: {user[1]}, Rol: {user[2]}")
        
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Error verificando tabla: {e}")

if __name__ == "__main__":
    print("🔍 Iniciando pruebas de autenticación...")
    
    # Verificar tabla local primero
    check_admin_users_table()
    
    # Probar login
    success = test_admin_login()
    
    if success:
        print("\n✅ Prueba de login exitosa!")
    else:
        print("\n❌ Todas las pruebas de login fallaron")
        print("\nPosibles soluciones:")
        print("1. Verificar que el backend esté corriendo")
        print("2. Verificar que la tabla admin_users exista y tenga usuarios")
        print("3. Verificar que las credenciales sean correctas")
        print("4. Verificar la conectividad de red hacia la API de producción")
