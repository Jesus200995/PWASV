#!/usr/bin/env python3
"""
Script para verificar qué territorios tienen administrador territorial asignado
y mostrar usuarios técnicos sin supervisor.
"""

import requests
import json

# URL del backend en producción VPS
API_URL = "https://apipwa.sembrandodatos.com"

def verificar_supervisores_territoriales():
    """Verifica supervisores territoriales para cada territorio"""
    
    print("=" * 80)
    print("🔍 VERIFICACIÓN DE SUPERVISORES TERRITORIALES")
    print("=" * 80)
    print()
    
    territorios = [
        "Acapulco - Centro - Norte - Tierra Caliente",
        "Acayucan",
        "Balancán",
        "Chihuahua / Sonora",
        "Colima",
        "Comalcalco",
        "Córdoba",
        "Costa Chica - Montaña",
        "Costa Grande - Sierra",
        "Durango / Zacatecas",
        "Hidalgo",
        "Istmo",
        "Michoacán",
        "Mixteca",
        "Morelos",
        "Nayarit / Jalisco",
        "Ocosingo",
        "Palenque",
        "Papantla",
        "Pichucalco",
        "Puebla",
        "San Luis Potosí",
        "Sinaloa",
        "Tamaulipas",
        "Tantoyuca",
        "Tapachula",
        "Teapa",
        "Tlaxcala / Estado de México",
        "Tzucacab / Opb",
        "Xpujil",
        "Oficinas Centrales"
    ]
    
    con_supervisor = []
    sin_supervisor = []
    
    print("📊 Verificando cada territorio...")
    print("-" * 80)
    
    for territorio in territorios:
        try:
            url = f"{API_URL}/supervisor-territorio/{requests.utils.quote(territorio)}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('supervisor'):
                    con_supervisor.append({
                        'territorio': territorio,
                        'supervisor': data['supervisor']
                    })
                    print(f"✅ {territorio:45} → {data['supervisor']}")
                else:
                    sin_supervisor.append(territorio)
                    print(f"❌ {territorio:45} → SIN SUPERVISOR")
            else:
                sin_supervisor.append(territorio)
                print(f"⚠️  {territorio:45} → ERROR HTTP {response.status_code}")
                
        except Exception as e:
            sin_supervisor.append(territorio)
            print(f"❌ {territorio:45} → ERROR: {str(e)[:30]}")
    
    print()
    print("=" * 80)
    print("📈 RESUMEN")
    print("=" * 80)
    print(f"✅ Territorios CON supervisor: {len(con_supervisor)}/{len(territorios)}")
    print(f"❌ Territorios SIN supervisor: {len(sin_supervisor)}/{len(territorios)}")
    print()
    
    if sin_supervisor:
        print("⚠️  TERRITORIOS SIN ADMINISTRADOR TERRITORIAL:")
        print("-" * 80)
        for territorio in sin_supervisor:
            print(f"   • {territorio}")
        print()
        print("💡 SOLUCIÓN: Asignar un administrador territorial a estos territorios")
        print("   desde el admin-pwa en la gestión de usuarios administrativos.")
    
    return con_supervisor, sin_supervisor

def verificar_tecnicos_sin_supervisor():
    """Muestra técnicos que no tienen supervisor asignado"""
    
    print()
    print("=" * 80)
    print("🔍 VERIFICANDO TÉCNICOS SIN SUPERVISOR")
    print("=" * 80)
    print()
    
    try:
        # Este endpoint debería existir o crear uno nuevo
        url = f"{API_URL}/usuarios"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            usuarios = response.json()
            
            tecnicos_sin_supervisor = []
            
            for usuario in usuarios:
                cargo = (usuario.get('cargo') or '').upper()
                if cargo in ['TECNICO SOCIAL', 'TECNICO PRODUCTIVO']:
                    supervisor = usuario.get('supervisor')
                    territorio = usuario.get('territorio')
                    
                    if not supervisor or supervisor.strip() == '':
                        tecnicos_sin_supervisor.append({
                            'id': usuario.get('id'),
                            'nombre': usuario.get('nombre_completo'),
                            'cargo': cargo,
                            'territorio': territorio or 'SIN TERRITORIO'
                        })
            
            if tecnicos_sin_supervisor:
                print(f"⚠️  Encontrados {len(tecnicos_sin_supervisor)} técnicos SIN supervisor:")
                print("-" * 80)
                for tec in tecnicos_sin_supervisor:
                    print(f"   ID: {tec['id']:4} | {tec['nombre']:40} | {tec['territorio']}")
                print()
            else:
                print("✅ Todos los técnicos tienen supervisor asignado")
                print()
                
            return tecnicos_sin_supervisor
        else:
            print(f"❌ Error obteniendo usuarios: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

if __name__ == "__main__":
    # Verificar supervisores territoriales
    con_sup, sin_sup = verificar_supervisores_territoriales()
    
    # Verificar técnicos sin supervisor
    tecnicos_sin_sup = verificar_tecnicos_sin_supervisor()
    
    print("=" * 80)
    print("🔧 ACCIONES RECOMENDADAS:")
    print("=" * 80)
    
    if sin_sup:
        print("1. Asignar administradores territoriales a los territorios sin supervisor")
    
    if tecnicos_sin_sup:
        print("2. Ejecutar actualización masiva de supervisores:")
        print("   python actualizar_supervisores_tecnicos.py")
    
    if not sin_sup and not tecnicos_sin_sup:
        print("✅ TODO ESTÁ CORRECTO - No se requieren acciones")
    
    print("=" * 80)
