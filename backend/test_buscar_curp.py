"""
Script de prueba para el buscador de usuarios por CURP
Prueba con: ROCR820619MSLJSB05
"""
import requests
import json

# Configuración
API_URL = "http://localhost:8000"  # Cambiar si es necesario
# API_URL = "https://apipwa.sembrandodatos.com"  # Para producción

def test_buscar_por_curp():
    """Prueba la búsqueda por CURP"""
    
    curp_prueba = "ROCR820619MSLJSB05"
    
    print("=" * 70)
    print("🧪 PRUEBA DE BÚSQUEDA POR CURP")
    print("=" * 70)
    print(f"\n📝 CURP a buscar: {curp_prueba}")
    
    # 1. Buscar usuario por CURP
    print(f"\n1️⃣ Buscando usuario en /usuarios/buscar...")
    
    try:
        response = requests.get(
            f"{API_URL}/usuarios/buscar",
            params={
                "nombre": curp_prueba,
                "correo": curp_prueba,
                "curp": curp_prueba
            },
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('usuarios', [])
            
            print(f"   ✅ Respuesta exitosa")
            print(f"   👥 Usuarios encontrados: {len(usuarios)}")
            
            if len(usuarios) > 0:
                print("\n   📋 Detalles de usuarios encontrados:")
                for i, usuario in enumerate(usuarios, 1):
                    print(f"\n   Usuario {i}:")
                    print(f"      ID: {usuario.get('id')}")
                    print(f"      Nombre: {usuario.get('nombre_completo')}")
                    print(f"      CURP: {usuario.get('curp')}")
                    print(f"      Correo: {usuario.get('correo')}")
                    print(f"      Cargo: {usuario.get('cargo')}")
                    print(f"      Rol: {usuario.get('rol')}")
                    
                # 2. Buscar registros del usuario encontrado
                usuario_id = usuarios[0]['id']
                print(f"\n2️⃣ Buscando registros del usuario {usuario_id}...")
                
                response2 = requests.get(
                    f"{API_URL}/admin/registros",
                    params={
                        "usuario_id": usuario_id,
                        "page": 1,
                        "page_size": 5000
                    },
                    timeout=20
                )
                
                print(f"   Status: {response2.status_code}")
                
                if response2.status_code == 200:
                    data2 = response2.json()
                    registros = data2.get('registros', [])
                    total = data2.get('total', 0)
                    
                    print(f"   ✅ Respuesta exitosa")
                    print(f"   📊 Registros encontrados: {len(registros)} de {total} totales")
                    
                    if len(registros) > 0:
                        print("\n   📋 Primeros 3 registros:")
                        for i, registro in enumerate(registros[:3], 1):
                            print(f"\n   Registro {i}:")
                            print(f"      ID: {registro.get('id')}")
                            print(f"      Descripción: {registro.get('descripcion', 'N/A')[:50]}")
                            print(f"      Fecha: {registro.get('fecha_hora')}")
                            print(f"      Ubicación: {registro.get('latitud')}, {registro.get('longitud')}")
                    else:
                        print("\n   ⚠️ El usuario no tiene registros de actividades")
                else:
                    print(f"   ❌ Error al buscar registros: {response2.status_code}")
                    print(f"   {response2.text}")
                    
            else:
                print(f"\n   ❌ No se encontró ningún usuario con CURP: {curp_prueba}")
                print("\n   💡 Verifica que:")
                print("      - La CURP exista en la base de datos")
                print("      - La CURP esté escrita correctamente")
                print("      - El campo 'curp' tenga datos en la tabla usuarios")
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"   {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"\n   ❌ Error de conexión")
        print(f"   💡 Verifica que:")
        print(f"      - El backend esté corriendo en {API_URL}")
        print(f"      - El puerto sea el correcto")
        
    except requests.exceptions.Timeout:
        print(f"\n   ❌ Timeout: La consulta tardó más de 10 segundos")
        
    except Exception as e:
        print(f"\n   ❌ Error inesperado: {e}")
    
    print("\n" + "=" * 70)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 70)


def test_verificar_usuario_existe():
    """Verifica si el usuario con esa CURP existe directamente"""
    
    print("\n" + "=" * 70)
    print("🔍 VERIFICACIÓN DIRECTA EN BASE DE DATOS")
    print("=" * 70)
    
    curp_prueba = "ROCR820619MSLJSB05"
    
    import psycopg2
    
    try:
        conn = psycopg2.connect(
            host="31.97.8.51",
            database="app_registros",
            user="jesus",
            password="2025"
        )
        cursor = conn.cursor()
        
        # Buscar usuario por CURP
        print(f"\n📝 Buscando CURP: {curp_prueba}")
        
        cursor.execute("""
            SELECT id, correo, nombre_completo, cargo, curp, territorio
            FROM usuarios
            WHERE curp ILIKE %s
        """, (f"%{curp_prueba}%",))
        
        usuarios = cursor.fetchall()
        
        print(f"✅ Usuarios encontrados: {len(usuarios)}")
        
        if len(usuarios) > 0:
            for i, usuario in enumerate(usuarios, 1):
                print(f"\nUsuario {i}:")
                print(f"  ID: {usuario[0]}")
                print(f"  Correo: {usuario[1]}")
                print(f"  Nombre: {usuario[2]}")
                print(f"  Cargo: {usuario[3]}")
                print(f"  CURP: {usuario[4]}")
                print(f"  Territorio: {usuario[5]}")
                
                # Contar registros
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM datos_historial
                    WHERE usuario_id = %s
                """, (usuario[0],))
                
                total_registros = cursor.fetchone()[0]
                print(f"  📊 Total de registros: {total_registros}")
        else:
            print(f"\n❌ No se encontró ningún usuario con CURP: {curp_prueba}")
            
            # Buscar CURPs similares
            print(f"\n🔍 Buscando CURPs similares...")
            cursor.execute("""
                SELECT id, nombre_completo, curp
                FROM usuarios
                WHERE curp ILIKE %s
                LIMIT 5
            """, (f"%ROCR82%",))
            
            similares = cursor.fetchall()
            if similares:
                print(f"   CURPs similares encontradas:")
                for similar in similares:
                    print(f"      - {similar[2]} ({similar[1]})")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    print("\n🚀 INICIANDO PRUEBAS DEL BUSCADOR\n")
    
    # Primero verificar en la BD
    test_verificar_usuario_existe()
    
    # Luego probar el endpoint
    test_buscar_por_curp()
    
    print("\n✅ TODAS LAS PRUEBAS COMPLETADAS\n")
