"""
Script de prueba COMPLETO para el buscador - PRODUCCIÓN
Prueba contra: https://apipwa.sembrandodatos.com
CURP: ROCR820619MSLJSB05
"""
import requests
import json

API_URL = "https://apipwa.sembrandodatos.com"

def obtener_token_admin():
    """Obtener token de administrador"""
    
    print("🔐 Obteniendo token de administrador...")
    print("   (Necesitarás credenciales válidas)")
    
    # Solicitar credenciales
    username = input("   Usuario admin: ")
    password = input("   Contraseña: ")
    
    try:
        # OAuth2 usa form-data, no JSON
        response = requests.post(
            f"{API_URL}/admin/login",
            data={
                "username": username,
                "password": password
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print(f"   ✅ Token obtenido correctamente")
            return token
        else:
            print(f"   ❌ Error de autenticación: {response.status_code}")
            print(f"   {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None


def test_buscar_usuario_completo(curp_prueba="ROCR820619MSLJSB05"):
    """Prueba completa del flujo de búsqueda"""
    
    print("\n" + "=" * 80)
    print("🧪 PRUEBA COMPLETA DEL BUSCADOR DE REGISTROS")
    print("=" * 80)
    print(f"\n🌐 API: {API_URL}")
    print(f"📝 CURP a buscar: {curp_prueba}")
    
    # Obtener token
    token = obtener_token_admin()
    if not token:
        print("\n❌ No se pudo obtener el token. Abortando pruebas.")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # PASO 1: Buscar usuario
    print("\n" + "-" * 80)
    print("PASO 1: BUSCAR USUARIO")
    print("-" * 80)
    
    try:
        print(f"\n📡 GET {API_URL}/usuarios/buscar")
        print(f"   Params: nombre={curp_prueba}, correo={curp_prueba}, curp={curp_prueba}")
        
        response = requests.get(
            f"{API_URL}/usuarios/buscar",
            params={
                "nombre": curp_prueba,
                "correo": curp_prueba,
                "curp": curp_prueba
            },
            headers=headers,
            timeout=15
        )
        
        print(f"\n📊 Respuesta:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Headers: Content-Type: {response.headers.get('content-type')}")
        
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('usuarios', [])
            
            print(f"\n✅ Búsqueda exitosa")
            print(f"   👥 Usuarios encontrados: {len(usuarios)}")
            
            if len(usuarios) == 0:
                print("\n❌ NO SE ENCONTRARON USUARIOS")
                print("\n💡 Posibles causas:")
                print("   1. La CURP no existe en la base de datos")
                print("   2. El campo 'curp' está vacío para ese usuario")
                print("   3. La CURP está mal escrita")
                print("\n🔍 Intenta buscar por:")
                
                # Intentar buscar solo por parte de la CURP
                print("\n   Buscando CURPs que empiecen con 'ROCR82'...")
                response2 = requests.get(
                    f"{API_URL}/usuarios/buscar",
                    params={"curp": "ROCR82"},
                    headers=headers,
                    timeout=10
                )
                if response2.status_code == 200:
                    usuarios2 = response2.json().get('usuarios', [])
                    print(f"   Encontrados: {len(usuarios2)} usuarios")
                    for u in usuarios2[:5]:
                        print(f"      - {u.get('nombre_completo')} | CURP: {u.get('curp', 'N/A')}")
                
                return
            
            # Mostrar detalles del usuario encontrado
            for i, usuario in enumerate(usuarios, 1):
                print(f"\n   Usuario {i}:")
                print(f"      🆔 ID: {usuario.get('id')}")
                print(f"      👤 Nombre: {usuario.get('nombre_completo')}")
                print(f"      📋 CURP: {usuario.get('curp')}")
                print(f"      📧 Correo: {usuario.get('correo')}")
                print(f"      💼 Cargo: {usuario.get('cargo')}")
                print(f"      👨‍💼 Supervisor: {usuario.get('supervisor')}")
                print(f"      🎭 Rol: {usuario.get('rol')}")
            
            # PASO 2: Obtener info completa del usuario
            usuario_id = usuarios[0]['id']
            
            print("\n" + "-" * 80)
            print(f"PASO 2: OBTENER INFORMACIÓN COMPLETA DEL USUARIO {usuario_id}")
            print("-" * 80)
            
            print(f"\n📡 GET {API_URL}/usuarios/{usuario_id}")
            
            response3 = requests.get(
                f"{API_URL}/usuarios/{usuario_id}",
                headers=headers,
                timeout=10
            )
            
            print(f"\n📊 Respuesta:")
            print(f"   Status Code: {response3.status_code}")
            
            if response3.status_code == 200:
                usuario_completo = response3.json()
                print(f"\n✅ Usuario obtenido correctamente")
                print(f"   Tiene CURP: {'SÍ' if usuario_completo.get('curp') else 'NO'}")
                if usuario_completo.get('curp'):
                    print(f"   CURP: {usuario_completo.get('curp')}")
            
            # PASO 3: Buscar registros del usuario
            print("\n" + "-" * 80)
            print(f"PASO 3: BUSCAR REGISTROS DEL USUARIO {usuario_id}")
            print("-" * 80)
            
            print(f"\n📡 GET {API_URL}/admin/registros")
            print(f"   Params: usuario_id={usuario_id}, page=1, page_size=5000")
            
            response4 = requests.get(
                f"{API_URL}/admin/registros",
                params={
                    "usuario_id": usuario_id,
                    "page": 1,
                    "page_size": 5000
                },
                headers=headers,
                timeout=30
            )
            
            print(f"\n📊 Respuesta:")
            print(f"   Status Code: {response4.status_code}")
            
            if response4.status_code == 200:
                data_registros = response4.json()
                registros = data_registros.get('registros', [])
                total = data_registros.get('total', 0)
                
                print(f"\n✅ Registros obtenidos correctamente")
                print(f"   📊 Registros en respuesta: {len(registros)}")
                print(f"   📈 Total en BD: {total}")
                
                if len(registros) > 0:
                    print(f"\n   📋 Primeros 5 registros:")
                    for i, registro in enumerate(registros[:5], 1):
                        print(f"\n   Registro {i}:")
                        print(f"      🆔 ID: {registro.get('id')}")
                        print(f"      👤 Usuario ID: {registro.get('usuario_id')}")
                        print(f"      📝 Descripción: {registro.get('descripcion', 'N/A')[:80]}")
                        print(f"      📅 Fecha: {registro.get('fecha_hora')}")
                        print(f"      📍 Ubicación: {registro.get('latitud')}, {registro.get('longitud')}")
                        print(f"      🖼️ Tiene foto: {'SÍ' if registro.get('foto_url') else 'NO'}")
                    
                    # VERIFICACIÓN: ¿Los registros tienen info de usuario?
                    print(f"\n   🔍 Verificando estructura de registros...")
                    primer_registro = registros[0]
                    print(f"      Tiene campo 'usuario': {'SÍ' if 'usuario' in primer_registro else 'NO'}")
                    print(f"      Tiene campo 'usuario_id': {'SÍ' if 'usuario_id' in primer_registro else 'NO'}")
                    
                    # PASO 4: Simular enriquecimiento
                    print("\n" + "-" * 80)
                    print(f"PASO 4: SIMULACIÓN DE ENRIQUECIMIENTO DE REGISTROS")
                    print("-" * 80)
                    
                    print(f"\n   Este es el proceso que hace usuariosService.enriquecerRegistrosConUsuarios()")
                    print(f"   Toma los registros y les agrega la info completa del usuario")
                    
                    # Verificar si ya vienen enriquecidos
                    if 'usuario' in primer_registro and isinstance(primer_registro['usuario'], dict):
                        print(f"\n   ✅ Los registros YA vienen enriquecidos del backend")
                        print(f"      Usuario en registro: {primer_registro['usuario']}")
                    else:
                        print(f"\n   ⚠️ Los registros NO vienen enriquecidos")
                        print(f"      El frontend necesita obtener info del usuario por separado")
                        print(f"      Esto ya lo hace usuariosService automáticamente")
                    
                else:
                    print(f"\n   ⚠️ El usuario NO tiene registros de actividades")
                    print(f"\n   💡 Esto es normal si:")
                    print(f"      - El usuario es nuevo")
                    print(f"      - El usuario no ha registrado actividades aún")
                    print(f"      - Los registros están en otra tabla o filtro territorial")
            else:
                print(f"\n   ❌ Error al obtener registros: {response4.status_code}")
                print(f"   {response4.text[:500]}")
                
        else:
            print(f"\n❌ Error en búsqueda: {response.status_code}")
            print(f"   {response.text[:500]}")
            
    except requests.exceptions.Timeout:
        print(f"\n❌ Timeout: La consulta tardó demasiado")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 80)
    
    print("\n📝 RESUMEN:")
    print("   Si llegaste hasta aquí y viste registros, el backend funciona correctamente.")
    print("   Si no se muestran en el frontend, el problema está en:")
    print("      1. El filtrado local (filtrarRegistros)")
    print("      2. El enriquecimiento de datos (usuariosService)")
    print("      3. El render de la tabla en el componente")


if __name__ == "__main__":
    print("\n🚀 SCRIPT DE PRUEBA DEL BUSCADOR - PRODUCCIÓN\n")
    
    curp = input("📝 CURP a buscar (Enter para usar ROCR820619MSLJSB05): ").strip()
    if not curp:
        curp = "ROCR820619MSLJSB05"
    
    test_buscar_usuario_completo(curp)
    
    print("\n✅ FIN DE LAS PRUEBAS\n")
