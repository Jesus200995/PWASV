"""
Script para crear usuarios territoriales usando la API REST
en producción: https://apipwa.sembrandodatos.com

Ejecutar: python crear_usuarios_via_api.py
"""

import requests
import json
import time

# URL de la API de producción
API_URL = "https://apipwa.sembrandodatos.com"

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

def verificar_api():
    """Verifica que la API esté disponible"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API disponible: {data.get('message', 'OK')}")
            return True
        else:
            print(f"❌ API respondió con status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando a la API: {e}")
        return False

def crear_usuario(usuario_data):
    """Crea un usuario territorial usando la API"""
    try:
        payload = {
            "username": usuario_data["usuario"],
            "password": usuario_data["contrasena"],
            "rol": "user",
            "permisos": PERMISOS_TERRITORIALES,
            "es_territorial": True,
            "territorio": usuario_data["territorio"]
        }
        
        response = requests.post(
            f"{API_URL}/admin/usuarios",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return {"success": True, "data": data}
        elif response.status_code == 409:
            return {"success": False, "error": "Usuario ya existe"}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}: {response.text}"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    print("=" * 70)
    print("🚀 CREACIÓN DE USUARIOS TERRITORIALES VÍA API")
    print("=" * 70)
    print(f"\n📡 API: {API_URL}")
    print(f"👥 Usuarios a crear: {len(USUARIOS_TERRITORIALES)}")
    
    # Verificar API
    print("\n🔍 Verificando conexión a la API...")
    if not verificar_api():
        print("\n❌ No se puede continuar sin conexión a la API")
        return
    
    # Contadores
    creados = 0
    existentes = 0
    errores = 0
    
    print("\n" + "=" * 70)
    print("👥 CREANDO USUARIOS...")
    print("=" * 70 + "\n")
    
    for i, usuario_data in enumerate(USUARIOS_TERRITORIALES, 1):
        username = usuario_data["usuario"]
        territorio = usuario_data["territorio"]
        
        print(f"[{i:02d}/{len(USUARIOS_TERRITORIALES)}] Creando '{username}'...", end=" ")
        
        resultado = crear_usuario(usuario_data)
        
        if resultado["success"]:
            print(f"✅ Creado (ID: {resultado['data'].get('id', '?')})")
            creados += 1
        elif "ya existe" in resultado["error"].lower():
            print(f"⚠️  Ya existe")
            existentes += 1
        else:
            print(f"❌ Error: {resultado['error']}")
            errores += 1
        
        # Pequeña pausa para no saturar la API
        time.sleep(0.3)
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE CREACIÓN")
    print("=" * 70)
    print(f"   ✅ Usuarios creados: {creados}")
    print(f"   ⚠️  Usuarios existentes (omitidos): {existentes}")
    print(f"   ❌ Errores: {errores}")
    print(f"   📋 Total procesados: {len(USUARIOS_TERRITORIALES)}")
    
    # Mostrar permisos asignados
    print("\n📋 PERMISOS ASIGNADOS A USUARIOS TERRITORIALES:")
    for permiso, valor in PERMISOS_TERRITORIALES.items():
        estado = "✅ Activado" if valor else "❌ Desactivado"
        print(f"   - {permiso}: {estado}")
    
    print("\n" + "=" * 70)
    print("✅ PROCESO COMPLETADO")
    print("=" * 70)
    
    # Mostrar tabla de credenciales
    print("\n📋 CREDENCIALES DE USUARIOS CREADOS:")
    print("-" * 70)
    print(f"{'Usuario':<20} {'Contraseña':<15} {'Territorio':<35}")
    print("-" * 70)
    for u in USUARIOS_TERRITORIALES:
        print(f"{u['usuario']:<20} {u['contrasena']:<15} {u['territorio']:<35}")
    print("-" * 70)

if __name__ == "__main__":
    main()
