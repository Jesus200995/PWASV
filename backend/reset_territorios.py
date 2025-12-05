#!/usr/bin/env python3
"""
Script para resetear todos los territorios de usuarios a NULL.
Esto obliga a todos los usuarios a seleccionar nuevamente su territorio
con la nueva lista de Territorios de Sembrando Vida.

Ejecutar en el servidor: python3 reset_territorios.py
"""

import psycopg2
import os
from datetime import datetime

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'pwa_database',
    'user': 'postgres',
    'password': 'postgres',
    'port': 5432
}

def reset_territorios():
    """Resetea el campo territorio de todos los usuarios a NULL"""
    try:
        print(f"\n{'='*60}")
        print("🔄 RESET DE TERRITORIOS DE USUARIOS")
        print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        # Conectar a la base de datos
        print("📡 Conectando a la base de datos...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("✅ Conexión exitosa\n")

        # Obtener estadísticas antes del reset
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE territorio IS NOT NULL")
        usuarios_con_territorio = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        
        print(f"📊 Estadísticas actuales:")
        print(f"   - Total de usuarios: {total_usuarios}")
        print(f"   - Usuarios con territorio asignado: {usuarios_con_territorio}")
        print(f"   - Usuarios sin territorio: {total_usuarios - usuarios_con_territorio}\n")

        if usuarios_con_territorio == 0:
            print("⚠️  No hay usuarios con territorio asignado. No se requiere reset.\n")
            return

        # Mostrar algunos ejemplos de territorios actuales
        print("📋 Territorios actuales (muestra):")
        cursor.execute("""
            SELECT territorio, COUNT(*) as cantidad 
            FROM usuarios 
            WHERE territorio IS NOT NULL 
            GROUP BY territorio 
            ORDER BY cantidad DESC 
            LIMIT 10
        """)
        for territorio, cantidad in cursor.fetchall():
            print(f"   - {territorio}: {cantidad} usuarios")
        print()

        # Confirmar antes de ejecutar
        confirmacion = input("⚠️  ¿Estás seguro de resetear TODOS los territorios? (escribir 'SI' para confirmar): ")
        
        if confirmacion.upper() != 'SI':
            print("\n❌ Operación cancelada por el usuario.\n")
            return

        # Ejecutar reset
        print("\n🔄 Ejecutando reset de territorios...")
        cursor.execute("UPDATE usuarios SET territorio = NULL WHERE territorio IS NOT NULL")
        filas_afectadas = cursor.rowcount
        conn.commit()

        print(f"\n✅ RESET COMPLETADO EXITOSAMENTE")
        print(f"   - Usuarios afectados: {filas_afectadas}")
        print(f"\n💡 Ahora todos los usuarios deberán seleccionar su territorio")
        print(f"   con la nueva lista de Territorios de Sembrando Vida.\n")

        # Cerrar conexión
        cursor.close()
        conn.close()
        print("🔌 Conexión cerrada.\n")

    except psycopg2.Error as e:
        print(f"\n❌ Error de PostgreSQL: {e}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    reset_territorios()
