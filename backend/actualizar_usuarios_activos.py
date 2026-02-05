#!/usr/bin/env python3
"""
Script para actualizar todos los usuarios con activo = NULL a activo = TRUE
Ejecutar en el VPS: python3 actualizar_usuarios_activos.py
"""

import psycopg2

# Configuración de conexión a la base de datos
DB_CONFIG = {
    "host": "localhost",
    "database": "app_registros",
    "user": "jesus",
    "password": "jesus123"
}

def actualizar_usuarios_activos():
    try:
        print("🔌 Conectando a la base de datos...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Verificar cuántos usuarios tienen activo = NULL
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE activo IS NULL")
        count_null = cursor.fetchone()[0]
        print(f"📊 Usuarios con activo = NULL: {count_null}")
        
        # Verificar cuántos usuarios tienen activo = TRUE
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE activo = TRUE")
        count_true = cursor.fetchone()[0]
        print(f"📊 Usuarios con activo = TRUE: {count_true}")
        
        # Verificar cuántos usuarios tienen activo = FALSE
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE activo = FALSE")
        count_false = cursor.fetchone()[0]
        print(f"📊 Usuarios con activo = FALSE: {count_false}")
        
        if count_null > 0:
            print(f"\n🔄 Actualizando {count_null} usuarios a activo = TRUE...")
            cursor.execute("UPDATE usuarios SET activo = TRUE WHERE activo IS NULL")
            conn.commit()
            
            # Verificar el resultado
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE activo = TRUE")
            new_count_true = cursor.fetchone()[0]
            print(f"✅ Actualización completada!")
            print(f"📊 Usuarios activos ahora: {new_count_true}")
        else:
            print("\n✅ Todos los usuarios ya tienen un valor para 'activo'")
        
        cursor.close()
        conn.close()
        print("\n🎉 Script completado exitosamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    actualizar_usuarios_activos()
