#!/usr/bin/env python3
"""
Script para verificar supervisores territoriales directamente en la BD PostgreSQL del VPS
y actualizar todos los técnicos.
"""

import psycopg2
from psycopg2.extras import RealDictCursor

# Configuración de la base de datos PostgreSQL en el VPS
DB_CONFIG = {
    'host': '31.97.8.51',
    'port': 5432,
    'database': 'app_registros',
    'user': 'postgres',
    'password': 'tu_contraseña_aqui'  # CAMBIAR ESTO
}

def verificar_admins_territoriales():
    """Verifica qué territorios tienen administrador territorial"""
    
    print("=" * 80)
    print("🔍 VERIFICANDO ADMINISTRADORES TERRITORIALES EN LA BASE DE DATOS")
    print("=" * 80)
    print()
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Obtener todos los admins territoriales
        cursor.execute("""
            SELECT 
                id,
                nombre_completo,
                territorio,
                es_territorial,
                activo
            FROM admin_users
            WHERE es_territorial = TRUE
            ORDER BY territorio
        """)
        
        admins = cursor.fetchall()
        
        if admins:
            print(f"✅ Encontrados {len(admins)} administradores territoriales:")
            print("-" * 80)
            for admin in admins:
                estado = "✅ ACTIVO" if admin['activo'] else "❌ INACTIVO"
                print(f"   {admin['territorio']:45} → {admin['nombre_completo']} ({estado})")
            print()
        else:
            print("⚠️  NO HAY ADMINISTRADORES TERRITORIALES EN LA BASE DE DATOS")
            print()
            
        cursor.close()
        conn.close()
        
        return admins
        
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        print()
        print("💡 AYUDA:")
        print("   1. Verifica que PostgreSQL esté corriendo en el VPS")
        print("   2. Verifica las credenciales de conexión")
        print("   3. Verifica que el firewall permita conexiones al puerto 5432")
        return []

def verificar_tecnicos_sin_supervisor():
    """Verifica técnicos sin supervisor"""
    
    print("=" * 80)
    print("🔍 VERIFICANDO TÉCNICOS SIN SUPERVISOR")
    print("=" * 80)
    print()
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT 
                id,
                nombre_completo,
                cargo,
                territorio,
                supervisor
            FROM usuarios
            WHERE UPPER(cargo) IN ('TECNICO SOCIAL', 'TECNICO PRODUCTIVO')
            ORDER BY territorio, nombre_completo
        """)
        
        tecnicos = cursor.fetchall()
        
        sin_supervisor = [t for t in tecnicos if not t['supervisor'] or t['supervisor'].strip() == '']
        sin_territorio = [t for t in tecnicos if not t['territorio']]
        con_supervisor = [t for t in tecnicos if t['supervisor'] and t['supervisor'].strip() != '']
        
        print(f"📊 ESTADÍSTICAS:")
        print(f"   Total técnicos: {len(tecnicos)}")
        print(f"   ✅ Con supervisor: {len(con_supervisor)}")
        print(f"   ❌ Sin supervisor: {len(sin_supervisor)}")
        print(f"   ⚠️  Sin territorio: {len(sin_territorio)}")
        print()
        
        if sin_supervisor:
            print(f"⚠️  TÉCNICOS SIN SUPERVISOR ({len(sin_supervisor)}):")
            print("-" * 80)
            for tec in sin_supervisor[:20]:  # Mostrar máximo 20
                print(f"   ID: {tec['id']:4} | {tec['nombre_completo']:40} | {tec['territorio'] or 'SIN TERRITORIO'}")
            if len(sin_supervisor) > 20:
                print(f"   ... y {len(sin_supervisor) - 20} más")
            print()
        
        cursor.close()
        conn.close()
        
        return tecnicos, sin_supervisor
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return [], []

def actualizar_supervisores_masivo():
    """Actualiza supervisores de todos los técnicos"""
    
    print("=" * 80)
    print("🔄 ACTUALIZANDO SUPERVISORES DE TÉCNICOS")
    print("=" * 80)
    print()
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Obtener todos los técnicos con territorio
        cursor.execute("""
            SELECT id, nombre_completo, cargo, territorio
            FROM usuarios
            WHERE UPPER(cargo) IN ('TECNICO SOCIAL', 'TECNICO PRODUCTIVO')
            AND territorio IS NOT NULL
        """)
        
        tecnicos = cursor.fetchall()
        actualizados = 0
        sin_admin = 0
        
        for tec in tecnicos:
            # Buscar admin territorial para este territorio
            cursor.execute("""
                SELECT nombre_completo
                FROM admin_users
                WHERE es_territorial = TRUE
                AND territorio = %s
                AND activo = TRUE
                LIMIT 1
            """, (tec['territorio'],))
            
            admin = cursor.fetchone()
            
            if admin:
                # Actualizar supervisor
                cursor.execute("""
                    UPDATE usuarios
                    SET supervisor = %s
                    WHERE id = %s
                """, (admin['nombre_completo'], tec['id']))
                
                print(f"✅ {tec['nombre_completo']:40} → {admin['nombre_completo']}")
                actualizados += 1
            else:
                print(f"⚠️  {tec['nombre_completo']:40} → Sin admin territorial ({tec['territorio']})")
                sin_admin += 1
        
        conn.commit()
        
        print()
        print(f"✅ Actualizados: {actualizados}")
        print(f"⚠️  Sin admin territorial: {sin_admin}")
        print()
        
        cursor.close()
        conn.close()
        
        return actualizados, sin_admin
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 0, 0

if __name__ == "__main__":
    print()
    print("NOTA: Este script requiere conexión directa a PostgreSQL en el VPS")
    print("      Edita DB_CONFIG con la contraseña correcta antes de ejecutar")
    print()
    input("Presiona ENTER para continuar o Ctrl+C para cancelar...")
    print()
    
    # Verificar admins territoriales
    admins = verificar_admins_territoriales()
    
    # Verificar técnicos
    tecnicos, sin_sup = verificar_tecnicos_sin_supervisor()
    
    if sin_sup and admins:
        print("=" * 80)
        respuesta = input("¿Deseas actualizar los supervisores ahora? (s/n): ")
        if respuesta.lower() == 's':
            actualizar_supervisores_masivo()
    
    print("=" * 80)
    print("✅ PROCESO COMPLETADO")
    print("=" * 80)
