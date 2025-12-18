"""
Script para crear usuarios territoriales en la tabla admin_users
con permisos específicos para cada territorio de Sembrando Vida.

Ejecutar en el servidor: python3 crear_usuarios_territoriales.py
"""

import psycopg2
from passlib.context import CryptContext
import json

# Configuración de conexión a la base de datos
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"

# Configuración para hashear contraseñas (igual que en main.py)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Lista de usuarios territoriales a crear
USUARIOS_TERRITORIALES = [
    {"usuario": "acapulcocntc", "contrasena": "Acapulco24", "territorio": "Acapulco - Centro - Norte - Tierra Caliente"},
    {"usuario": "acayucan", "contrasena": "Acayucan24", "territorio": "Acayucan"},
    {"usuario": "balancan", "contrasena": "Balancan24", "territorio": "Balancán"},
    {"usuario": "chihuahuasonora", "contrasena": "Chihuahua24", "territorio": "Chihuahua / Sonora"},
    {"usuario": "colima", "contrasena": "Colima24", "territorio": "Colima"},
    {"usuario": "comalcalco", "contrasena": "Comalcalco24", "territorio": "Comalcalco"},
    {"usuario": "cordoba", "contrasena": "Cordoba24", "territorio": "Córdoba"},
    {"usuario": "costachica", "contrasena": "CostaChica24", "territorio": "Costa Chica - Montaña"},
    {"usuario": "costagrande", "contrasena": "CostaGrande24", "territorio": "Costa Grande - Sierra"},
    {"usuario": "durangozac", "contrasena": "Durango24", "territorio": "Durango / Zacatecas"},
    {"usuario": "hidalgo", "contrasena": "Hidalgo24", "territorio": "Hidalgo"},
    {"usuario": "istmo", "contrasena": "Istmo24", "territorio": "Istmo"},
    {"usuario": "michoacan", "contrasena": "Michoacan24", "territorio": "Michoacán"},
    {"usuario": "mixteca", "contrasena": "Mixteca24", "territorio": "Mixteca"},
    {"usuario": "morelos", "contrasena": "Morelos24", "territorio": "Morelos"},
    {"usuario": "nayaritjalisco", "contrasena": "Nayarit24", "territorio": "Nayarit / Jalisco"},
    {"usuario": "ocosingo", "contrasena": "Ocosingo24", "territorio": "Ocosingo"},
    {"usuario": "palenque", "contrasena": "Palenque24", "territorio": "Palenque"},
    {"usuario": "papantla", "contrasena": "Papantla24", "territorio": "Papantla"},
    {"usuario": "pichucalco", "contrasena": "Pichucalco24", "territorio": "Pichucalco"},
    {"usuario": "puebla", "contrasena": "Puebla24", "territorio": "Puebla"},
    {"usuario": "sanluispotosi", "contrasena": "SLPotosi24", "territorio": "San Luis Potosí"},
    {"usuario": "sinaloa", "contrasena": "Sinaloa24", "territorio": "Sinaloa"},
    {"usuario": "tamaulipas", "contrasena": "Tamaulipas24", "territorio": "Tamaulipas"},
    {"usuario": "tantoyuca", "contrasena": "Tantoyuca24", "territorio": "Tantoyuca"},
    {"usuario": "tapachula", "contrasena": "Tapachula24", "territorio": "Tapachula"},
    {"usuario": "teapa", "contrasena": "Teapa24", "territorio": "Teapa"},
    {"usuario": "tlaxcalaedomex", "contrasena": "Tlaxcala24", "territorio": "Tlaxcala / Estado de México"},
    {"usuario": "tzucacabopb", "contrasena": "Tzucacab24", "territorio": "Tzucacab / Opb"},
    {"usuario": "xpujil", "contrasena": "Xpujil24", "territorio": "Xpujil"},
]

# Permisos específicos para usuarios territoriales:
# - Visor de Seguimiento: TRUE
# - Asistencia: TRUE
# - Registros: TRUE
# - Usuarios: TRUE (solo ver, sin editar/eliminar)
# - usuarios_acciones: FALSE (no puede editar ni eliminar usuarios)
# - Historiales: TRUE
# - Notificaciones: FALSE
# - Permisos: FALSE
# - Configuración: FALSE
PERMISOS_TERRITORIALES = {
    "visor": True,
    "asistencia": True,
    "registros": True,
    "usuarios": True,
    "usuarios_acciones": False,  # Solo lectura de usuarios
    "historiales": True,
    "notificaciones": False,
    "permisos": False,
    "configuracion": False
}

def crear_usuarios_territoriales():
    """Crea los usuarios territoriales en la base de datos"""
    
    conn = None
    cursor = None
    
    try:
        print("=" * 60)
        print("🚀 CREACIÓN DE USUARIOS TERRITORIALES")
        print("=" * 60)
        
        # Conectar a la base de datos
        print("\n📡 Conectando a la base de datos...")
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            connect_timeout=10
        )
        cursor = conn.cursor()
        print("✅ Conexión exitosa")
        
        # Verificar estructura de la tabla admin_users
        print("\n📋 Verificando estructura de tabla admin_users...")
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'admin_users'
        """)
        columnas = [row[0] for row in cursor.fetchall()]
        print(f"   Columnas existentes: {columnas}")
        
        # Convertir permisos a JSON
        permisos_json = json.dumps(PERMISOS_TERRITORIALES)
        
        # Contadores
        creados = 0
        existentes = 0
        errores = 0
        
        print("\n" + "=" * 60)
        print("👥 CREANDO USUARIOS...")
        print("=" * 60)
        
        for usuario_data in USUARIOS_TERRITORIALES:
            username = usuario_data["usuario"]
            password = usuario_data["contrasena"]
            territorio = usuario_data["territorio"]
            
            try:
                # Verificar si el usuario ya existe
                cursor.execute("SELECT id FROM admin_users WHERE username = %s", (username,))
                if cursor.fetchone():
                    print(f"⚠️  Usuario '{username}' ya existe - omitido")
                    existentes += 1
                    continue
                
                # Hashear la contraseña
                hashed_password = pwd_context.hash(password)
                
                # Insertar el usuario
                cursor.execute("""
                    INSERT INTO admin_users (username, password, rol, permisos, activo, es_territorial, territorio) 
                    VALUES (%s, %s, %s, %s, TRUE, TRUE, %s) 
                    RETURNING id
                """, (username, hashed_password, 'user', permisos_json, territorio))
                
                nuevo_id = cursor.fetchone()[0]
                print(f"✅ Usuario '{username}' creado (ID: {nuevo_id}) - Territorio: {territorio}")
                creados += 1
                
            except Exception as e:
                print(f"❌ Error creando usuario '{username}': {e}")
                errores += 1
                conn.rollback()
                continue
        
        # Confirmar cambios
        conn.commit()
        
        # Resumen final
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE CREACIÓN")
        print("=" * 60)
        print(f"   ✅ Usuarios creados: {creados}")
        print(f"   ⚠️  Usuarios existentes (omitidos): {existentes}")
        print(f"   ❌ Errores: {errores}")
        print(f"   📋 Total procesados: {len(USUARIOS_TERRITORIALES)}")
        
        # Mostrar permisos asignados
        print("\n📋 PERMISOS ASIGNADOS A USUARIOS TERRITORIALES:")
        for permiso, valor in PERMISOS_TERRITORIALES.items():
            estado = "✅ Activado" if valor else "❌ Desactivado"
            print(f"   - {permiso}: {estado}")
        
        print("\n" + "=" * 60)
        print("✅ PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        
        # Listar usuarios creados
        print("\n📋 USUARIOS TERRITORIALES EN EL SISTEMA:")
        cursor.execute("""
            SELECT id, username, rol, territorio, activo 
            FROM admin_users 
            WHERE es_territorial = TRUE 
            ORDER BY territorio
        """)
        usuarios = cursor.fetchall()
        print(f"\n   Total de usuarios territoriales: {len(usuarios)}\n")
        for u in usuarios:
            estado = "🟢 Activo" if u[4] else "🔴 Inactivo"
            print(f"   ID: {u[0]:3} | Usuario: {u[1]:20} | Rol: {u[2]:5} | Territorio: {u[3]} | {estado}")
        
    except Exception as e:
        print(f"\n❌ ERROR GENERAL: {e}")
        if conn:
            conn.rollback()
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("\n🔌 Conexión a la base de datos cerrada")

if __name__ == "__main__":
    crear_usuarios_territoriales()
