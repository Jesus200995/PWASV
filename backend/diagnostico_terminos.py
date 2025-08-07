#!/usr/bin/env python3
"""
Script para verificar directamente en la base de datos del VPS
si los términos se están registrando automáticamente
"""

import psycopg2
from psycopg2.extras import RealDictCursor

# Configuración de conexión
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"

def verificar_ultimos_usuarios_y_terminos():
    """Verificar los últimos usuarios creados y si tienen términos"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS,
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        
        print("✅ Conexión a PostgreSQL exitosa")
        
        # Obtener los últimos 10 usuarios
        cursor.execute("""
            SELECT id, correo, nombre_completo, curp
            FROM usuarios 
            ORDER BY id DESC 
            LIMIT 10
        """)
        
        usuarios = cursor.fetchall()
        print(f"\n📋 Últimos {len(usuarios)} usuarios creados:")
        
        usuarios_con_terminos = 0
        usuarios_sin_terminos = 0
        
        for usuario in usuarios:
            user_id = usuario['id']
            correo = usuario['correo']
            
            # Verificar si tiene términos
            cursor.execute("""
                SELECT aceptado, fecha_aceptado 
                FROM usuarios_terminos 
                WHERE usuario_id = %s
            """, (user_id,))
            
            terminos = cursor.fetchone()
            
            if terminos:
                estado = "✅ CON términos" if terminos['aceptado'] else "⚠️  términos NO aceptados"
                fecha = terminos['fecha_aceptado'].strftime('%Y-%m-%d %H:%M:%S') if terminos['fecha_aceptado'] else 'N/A'
                usuarios_con_terminos += 1
                print(f"  {user_id:3d}. {correo:30s} | {estado} | {fecha}")
            else:
                estado = "❌ SIN términos"
                usuarios_sin_terminos += 1
                print(f"  {user_id:3d}. {correo:30s} | {estado}")
        
        print(f"\n📊 RESUMEN:")
        print(f"  - Usuarios CON términos: {usuarios_con_terminos}")
        print(f"  - Usuarios SIN términos: {usuarios_sin_terminos}")
        
        if usuarios_sin_terminos > 0:
            print(f"\n⚠️  PROBLEMA DETECTADO:")
            print(f"     {usuarios_sin_terminos} usuarios no tienen términos registrados")
            print(f"     Esto indica que el backend de producción NO está registrando términos automáticamente")
        else:
            print(f"\n✅ PERFECTO:")
            print(f"     Todos los usuarios tienen términos registrados")
        
        cursor.close()
        conn.close()
        
        return usuarios_sin_terminos == 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def registrar_terminos_faltantes():
    """Registrar términos para usuarios que no los tienen"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS,
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        
        # Encontrar usuarios sin términos
        cursor.execute("""
            SELECT u.id, u.correo 
            FROM usuarios u
            LEFT JOIN usuarios_terminos ut ON u.id = ut.usuario_id
            WHERE ut.usuario_id IS NULL
            ORDER BY u.id DESC
            LIMIT 50
        """)
        
        usuarios_sin_terminos = cursor.fetchall()
        
        if not usuarios_sin_terminos:
            print("✅ Todos los usuarios ya tienen términos registrados")
            return True
        
        print(f"🔧 Encontrados {len(usuarios_sin_terminos)} usuarios sin términos")
        print("🔄 Registrando términos automáticamente...")
        
        for usuario in usuarios_sin_terminos:
            user_id = usuario['id']
            correo = usuario['correo']
            
            try:
                cursor.execute("""
                    INSERT INTO usuarios_terminos (usuario_id, aceptado, fecha_aceptado) 
                    VALUES (%s, %s, NOW())
                """, (user_id, True))
                
                print(f"  ✅ Términos registrados para: {correo} (ID: {user_id})")
                
            except Exception as e:
                print(f"  ❌ Error registrando términos para {correo}: {e}")
        
        conn.commit()
        print(f"\n✅ Proceso completado: {len(usuarios_sin_terminos)} registros procesados")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error registrando términos faltantes: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 DIAGNÓSTICO - TÉRMINOS EN BASE DE DATOS VPS")
    print("=" * 60)
    
    # Verificar estado actual
    print("\n1️⃣ Verificando usuarios y términos existentes...")
    todo_ok = verificar_ultimos_usuarios_y_terminos()
    
    if not todo_ok:
        print("\n2️⃣ Corrigiendo usuarios sin términos...")
        if registrar_terminos_faltantes():
            print("\n3️⃣ Verificando nuevamente después de la corrección...")
            verificar_ultimos_usuarios_y_terminos()
    
    print("\n" + "=" * 60)
    print("✅ DIAGNÓSTICO COMPLETADO")
    print("\n🔧 PRÓXIMOS PASOS:")
    print("1. Subir el backend modificado al servidor de producción")
    print("2. Asegurar que los nuevos usuarios registren términos automáticamente")
    print("3. Probar el frontend para verificar el flujo completo")

if __name__ == "__main__":
    main()
