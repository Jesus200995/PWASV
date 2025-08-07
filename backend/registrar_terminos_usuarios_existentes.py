#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para registrar términos automáticamente a usuarios existentes
que no los tengan, desde el backend actualizado.

EJECUTAR SOLO DESPUÉS DEL DESPLIEGUE EN PRODUCCIÓN
"""

import psycopg2
from datetime import datetime

# Configuración de base de datos
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"

def registrar_terminos_usuarios_existentes():
    """Registra términos para usuarios que no los tengan"""
    print("🔍 REGISTRO AUTOMÁTICO DE TÉRMINOS PARA USUARIOS EXISTENTES")
    print("="*60)
    
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cursor = conn.cursor()
        print("✅ Conexión a la base de datos exitosa")
        
        # Obtener usuarios sin términos
        cursor.execute("""
            SELECT u.id, u.correo, u.nombre_completo
            FROM usuarios u
            LEFT JOIN usuarios_terminos ut ON u.id = ut.usuario_id
            WHERE ut.usuario_id IS NULL
        """)
        
        usuarios_sin_terminos = cursor.fetchall()
        print(f"📊 Usuarios sin términos encontrados: {len(usuarios_sin_terminos)}")
        
        if not usuarios_sin_terminos:
            print("✅ Todos los usuarios ya tienen términos aceptados")
            return
        
        # Registrar términos para cada usuario
        usuarios_procesados = 0
        for usuario in usuarios_sin_terminos:
            user_id, correo, nombre = usuario
            try:
                cursor.execute("""
                    INSERT INTO usuarios_terminos (usuario_id, aceptado, fecha_aceptado) 
                    VALUES (%s, %s, NOW())
                """, (user_id, True))
                
                usuarios_procesados += 1
                print(f"✅ Términos registrados para usuario {user_id}: {correo}")
                
            except Exception as e:
                print(f"❌ Error registrando términos para usuario {user_id}: {e}")
        
        # Confirmar cambios
        conn.commit()
        print(f"\n🎉 PROCESO COMPLETADO")
        print(f"   📊 Usuarios procesados: {usuarios_procesados}")
        print(f"   ✅ Términos registrados exitosamente")
        
        # Verificar resultado final
        cursor.execute("SELECT COUNT(*) FROM usuarios_terminos WHERE aceptado = true")
        total_con_terminos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        
        print(f"\n📈 ESTADÍSTICAS FINALES:")
        print(f"   👥 Total usuarios: {total_usuarios}")
        print(f"   ✅ Con términos aceptados: {total_con_terminos}")
        print(f"   📊 Cobertura: {(total_con_terminos/total_usuarios*100):.1f}%")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    print(f"🕐 Iniciado: {datetime.now()}")
    registrar_terminos_usuarios_existentes()
    print(f"🕐 Finalizado: {datetime.now()}")
