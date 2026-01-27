#!/usr/bin/env python3
"""
Script para crear administradores territoriales faltantes vía API
"""

import requests
import json

API_URL = "https://apipwa.sembrandodatos.com"

# Territorios que necesitan administrador territorial
TERRITORIOS_FALTANTES = [
    {
        "correo": "admin.acayucan@sembrandovida.gob.mx",
        "nombre_completo": "ADMINISTRADOR TERRITORIAL ACAYUCAN",
        "territorio": "Acayucan",
        "password": "Admin2026!Acayucan"
    },
    {
        "correo": "admin.chihuahuasonora@sembrandovida.gob.mx",
        "nombre_completo": "ADMINISTRADOR TERRITORIAL CHIHUAHUA SONORA",
        "territorio": "Chihuahua / Sonora",
        "password": "Admin2026!Chihuahua"
    },
    {
        "correo": "admin.durangozacatecas@sembrandovida.gob.mx",
        "nombre_completo": "ADMINISTRADOR TERRITORIAL DURANGO ZACATECAS",
        "territorio": "Durango / Zacatecas",
        "password": "Admin2026!Durango"
    },
    {
        "correo": "admin.nayaritjalisco@sembrandovida.gob.mx",
        "nombre_completo": "ADMINISTRADOR TERRITORIAL NAYARIT JALISCO",
        "territorio": "Nayarit / Jalisco",
        "password": "Admin2026!Nayarit"
    },
    {
        "correo": "admin.tlaxcalaedomex@sembrandovida.gob.mx",
        "nombre_completo": "ADMINISTRADOR TERRITORIAL TLAXCALA ESTADO DE MEXICO",
        "territorio": "Tlaxcala / Estado de México",
        "password": "Admin2026!Tlaxcala"
    },
    {
        "correo": "admin.tzucacab@sembrandovida.gob.mx",
        "nombre_completo": "ADMINISTRADOR TERRITORIAL TZUCACAB OPB",
        "territorio": "Tzucacab / Opb",
        "password": "Admin2026!Tzucacab"
    },
    {
        "correo": "admin.centrales@sembrandovida.gob.mx",
        "nombre_completo": "ADMINISTRADOR TERRITORIAL OFICINAS CENTRALES",
        "territorio": "Oficinas Centrales",
        "password": "Admin2026!Centrales"
    }
]

def crear_admin_territorial(admin_data):
    """Crea un administrador territorial usando la API"""
    
    try:
        # Endpoint correcto según el backend
        url = f"{API_URL}/admin/usuarios"
        
        payload = {
            "username": admin_data["correo"],
            "password": admin_data["password"],
            "rol": "user",  # Los territoriales son tipo 'user'
            "nombre_completo": admin_data["nombre_completo"],
            "territorio": admin_data["territorio"],
            "es_territorial": True,
            "cargo": "ADMINISTRADOR TERRITORIAL"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code in [200, 201]:
            print(f"✅ Creado: {admin_data['nombre_completo']}")
            return True
        elif response.status_code == 409:
            print(f"ℹ️  Ya existe: {admin_data['nombre_completo']}")
            return True
        else:
            print(f"❌ Error {response.status_code}: {admin_data['nombre_completo']}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error creando {admin_data['nombre_completo']}: {e}")
        return False

def main():
    print("=" * 80)
    print("🔧 CREANDO ADMINISTRADORES TERRITORIALES FALTANTES")
    print("=" * 80)
    print()
    
    print("⚠️  NOTA: Este script intenta crear admins vía API.")
    print("   Si el endpoint no existe, usa el archivo SQL o crea desde admin-pwa")
    print()
    
    creados = 0
    errores = 0
    
    for admin in TERRITORIOS_FALTANTES:
        if crear_admin_territorial(admin):
            creados += 1
        else:
            errores += 1
    
    print()
    print("=" * 80)
    print(f"✅ Creados/Existentes: {creados}")
    print(f"❌ Errores: {errores}")
    print("=" * 80)
    print()
    
    if creados > 0:
        print("🔄 Ahora ejecuta: python actualizar_supervisores_tecnicos.py")
        print("   Para asignar supervisores a todos los técnicos")
    
    print()
    print("📋 CREDENCIALES GENERADAS:")
    print("-" * 80)
    for admin in TERRITORIOS_FALTANTES:
        print(f"   Usuario: {admin['correo']}")
        print(f"   Password: {admin['password']}")
        print()

if __name__ == "__main__":
    main()
