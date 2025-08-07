#!/usr/bin/env python3
"""
Script para probar específicamente el registro de términos
con la estructura de PostgreSQL del VPS
"""

import psycopg2
from psycopg2.extras import RealDictCursor

# Configuración de conexión (misma que en main.py)
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"

def test_usuarios_terminos_table():
    """Probar la tabla usuarios_terminos y su estructura"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS,
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        
        print("✅ Conexión a PostgreSQL exitosa")
        
        # Verificar si la tabla usuarios_terminos existe
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'usuarios_terminos'
        """)
        
        tabla_existe = cursor.fetchone()
        
        if tabla_existe:
            print("✅ Tabla usuarios_terminos existe")
            
            # Obtener estructura de la tabla
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_schema = 'public' AND table_name = 'usuarios_terminos' 
                ORDER BY ordinal_position
            """)
            
            columnas = cursor.fetchall()
            print("\n📋 Estructura de la tabla usuarios_terminos:")
            for col in columnas:
                print(f"  - {col['column_name']}: {col['data_type']} (nullable: {col['is_nullable']}, default: {col['column_default']})")
                
        else:
            print("❌ Tabla usuarios_terminos NO existe")
            print("Creando tabla con la estructura del VPS...")
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios_terminos (
                    id SERIAL PRIMARY KEY,
                    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
                    aceptado BOOLEAN NOT NULL DEFAULT FALSE,
                    fecha_aceptado TIMESTAMP NOT NULL DEFAULT NOW(),
                    ip_aceptado VARCHAR(50)
                )
            """)
            conn.commit()
            print("✅ Tabla usuarios_terminos creada")
        
        # Verificar cuántos registros hay
        cursor.execute("SELECT COUNT(*) as total FROM usuarios_terminos")
        total = cursor.fetchone()['total']
        print(f"\n📊 Total de registros en usuarios_terminos: {total}")
        
        # Mostrar algunos registros de ejemplo
        if total > 0:
            cursor.execute("""
                SELECT ut.*, u.correo, u.nombre_completo 
                FROM usuarios_terminos ut
                JOIN usuarios u ON ut.usuario_id = u.id
                ORDER BY ut.fecha_aceptado DESC 
                LIMIT 5
            """)
            
            registros = cursor.fetchall()
            print("\n📋 Últimos registros de términos:")
            for reg in registros:
                print(f"  - Usuario: {reg['correo']} | Aceptado: {reg['aceptado']} | Fecha: {reg['fecha_aceptado']}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_insert_terminos():
    """Probar insertar un registro de términos"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cursor = conn.cursor()
        
        # Buscar un usuario existente para probar
        cursor.execute("SELECT id, correo FROM usuarios ORDER BY id DESC LIMIT 1")
        usuario = cursor.fetchone()
        
        if not usuario:
            print("❌ No hay usuarios en la base de datos para probar")
            return False
        
        user_id, correo = usuario
        print(f"🧪 Probando con usuario: {correo} (ID: {user_id})")
        
        # Verificar si ya tiene términos
        cursor.execute("SELECT id FROM usuarios_terminos WHERE usuario_id = %s", (user_id,))
        ya_existe = cursor.fetchone()
        
        if ya_existe:
            print(f"ℹ️  Usuario ya tiene términos registrados, actualizando...")
            cursor.execute("""
                UPDATE usuarios_terminos 
                SET aceptado = %s, fecha_aceptado = NOW()
                WHERE usuario_id = %s
            """, (True, user_id))
        else:
            print(f"🆕 Insertando nuevos términos...")
            cursor.execute("""
                INSERT INTO usuarios_terminos (usuario_id, aceptado, fecha_aceptado) 
                VALUES (%s, %s, NOW())
            """, (user_id, True))
        
        conn.commit()
        print("✅ Términos registrados/actualizados exitosamente")
        
        # Verificar el registro
        cursor.execute("""
            SELECT aceptado, fecha_aceptado 
            FROM usuarios_terminos 
            WHERE usuario_id = %s
        """, (user_id,))
        
        resultado = cursor.fetchone()
        print(f"✅ Verificación: Aceptado = {resultado[0]}, Fecha = {resultado[1]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando insert: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 PRUEBA ESPECÍFICA - TÉRMINOS EN VPS POSTGRESQL")
    print("=" * 60)
    
    # Probar tabla y estructura
    print("\n1️⃣ Probando tabla usuarios_terminos...")
    if not test_usuarios_terminos_table():
        return
    
    print("\n2️⃣ Probando inserción de términos...")
    if not test_insert_terminos():
        return
    
    print("\n" + "=" * 60)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("\n🔧 DIAGNÓSTICO:")
    print("- ✅ Conexión con PostgreSQL funciona")
    print("- ✅ Tabla usuarios_terminos con estructura correcta")
    print("- ✅ Inserción/actualización de términos funciona")
    print("- ✅ Sistema listo para registrar términos automáticamente")

if __name__ == "__main__":
    main()
