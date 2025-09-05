#!/usr/bin/env python3
"""
Script para optimizar índices de la base de datos y mejorar el rendimiento de consultas.
Especialmente útil para solucionar problemas de timeout en registros.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import time

# Configuración de la base de datos
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"

def conectar_db():
    """Conectar a la base de datos"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST, 
            database=DB_NAME, 
            user=DB_USER, 
            password=DB_PASS,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"❌ Error conectando a la DB: {e}")
        return None

def verificar_indices_existentes(cursor):
    """Verificar qué índices ya existen"""
    print("🔍 Verificando índices existentes...")
    
    cursor.execute("""
        SELECT 
            schemaname,
            tablename,
            indexname,
            indexdef
        FROM pg_indexes 
        WHERE schemaname = 'public' 
        AND tablename IN ('registros', 'usuarios', 'asistencias')
        ORDER BY tablename, indexname;
    """)
    
    indices = cursor.fetchall()
    
    print(f"📊 Encontrados {len(indices)} índices:")
    for idx in indices:
        print(f"  • {idx['tablename']}.{idx['indexname']}")
    
    return indices

def crear_indices_optimizados(cursor):
    """Crear índices optimizados para mejorar el rendimiento"""
    print("\n🚀 Creando índices optimizados...")
    
    indices_a_crear = [
        # Índices para tabla registros
        {
            "nombre": "idx_registros_fecha_hora_desc",
            "sql": "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_registros_fecha_hora_desc ON registros (fecha_hora DESC);",
            "descripcion": "Optimiza ORDER BY fecha_hora DESC"
        },
        {
            "nombre": "idx_registros_usuario_id_fecha",
            "sql": "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_registros_usuario_id_fecha ON registros (usuario_id, fecha_hora DESC);",
            "descripcion": "Optimiza filtros por usuario + orden por fecha"
        },
        {
            "nombre": "idx_registros_id_desc",
            "sql": "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_registros_id_desc ON registros (id DESC);",
            "descripcion": "Optimiza ORDER BY id DESC para paginación"
        },
        {
            "nombre": "idx_registros_tipo_actividad",
            "sql": "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_registros_tipo_actividad ON registros (tipo_actividad);",
            "descripcion": "Optimiza filtros por tipo de actividad"
        },
        {
            "nombre": "idx_registros_fecha_dia",
            "sql": "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_registros_fecha_dia ON registros (DATE(fecha_hora));",
            "descripcion": "Optimiza consultas por día específico"
        },
        
        # Índices para tabla usuarios
        {
            "nombre": "idx_usuarios_correo",
            "sql": "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_usuarios_correo ON usuarios (correo);",
            "descripcion": "Optimiza búsquedas por correo"
        },
        {
            "nombre": "idx_usuarios_nombre_completo",
            "sql": "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_usuarios_nombre_completo ON usuarios (nombre_completo);",
            "descripcion": "Optimiza búsquedas por nombre"
        },
        {
            "nombre": "idx_usuarios_curp",
            "sql": "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_usuarios_curp ON usuarios (curp);",
            "descripcion": "Optimiza búsquedas por CURP"
        },
        
        # Índices para tabla asistencias
        {
            "nombre": "idx_asistencias_fecha",
            "sql": "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_asistencias_fecha ON asistencias (fecha);",
            "descripcion": "Optimiza consultas por fecha de asistencia"
        },
        {
            "nombre": "idx_asistencias_usuario_fecha",
            "sql": "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_asistencias_usuario_fecha ON asistencias (usuario_id, fecha);",
            "descripcion": "Optimiza consultas por usuario y fecha"
        }
    ]
    
    indices_creados = 0
    indices_existentes = 0
    errores = 0
    
    for idx in indices_a_crear:
        try:
            print(f"  📝 Creando {idx['nombre']}...")
            start_time = time.time()
            
            cursor.execute(idx['sql'])
            
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"    ✅ Creado en {duration:.2f}s - {idx['descripcion']}")
            indices_creados += 1
            
        except psycopg2.errors.DuplicateTable:
            print(f"    ℹ️  Ya existe - {idx['descripcion']}")
            indices_existentes += 1
        except Exception as e:
            print(f"    ❌ Error: {e}")
            errores += 1
    
    print(f"\n📊 Resumen de índices:")
    print(f"  • Creados: {indices_creados}")
    print(f"  • Ya existían: {indices_existentes}")
    print(f"  • Errores: {errores}")

def analizar_rendimiento_consultas(cursor):
    """Analizar el rendimiento de consultas comunes"""
    print("\n📊 Analizando rendimiento de consultas...")
    
    consultas_test = [
        {
            "nombre": "Últimos 1000 registros",
            "sql": "SELECT COUNT(*) FROM registros ORDER BY fecha_hora DESC LIMIT 1000;",
        },
        {
            "nombre": "Registros por usuario",
            "sql": "SELECT COUNT(*) FROM registros WHERE usuario_id = 1 ORDER BY fecha_hora DESC LIMIT 100;",
        },
        {
            "nombre": "Registros de hoy",
            "sql": "SELECT COUNT(*) FROM registros WHERE DATE(fecha_hora) = CURRENT_DATE;",
        },
        {
            "nombre": "Total de registros",
            "sql": "SELECT COUNT(*) FROM registros;",
        }
    ]
    
    for consulta in consultas_test:
        try:
            start_time = time.time()
            cursor.execute(consulta['sql'])
            result = cursor.fetchone()
            end_time = time.time()
            
            duration = end_time - start_time
            print(f"  • {consulta['nombre']}: {duration:.3f}s")
            
        except Exception as e:
            print(f"  • {consulta['nombre']}: ❌ Error - {e}")

def optimizar_configuracion_db(cursor):
    """Verificar y sugerir optimizaciones de configuración"""
    print("\n⚙️  Verificando configuración de la base de datos...")
    
    # Verificar configuraciones importantes
    configuraciones = [
        "shared_buffers",
        "work_mem",
        "maintenance_work_mem",
        "effective_cache_size",
        "random_page_cost",
        "checkpoint_segments"
    ]
    
    for config in configuraciones:
        try:
            cursor.execute(f"SHOW {config};")
            valor = cursor.fetchone()
            if valor:
                print(f"  • {config}: {valor[0]}")
        except:
            print(f"  • {config}: No disponible")

def limpiar_estadisticas_db(cursor):
    """Actualizar estadísticas de la base de datos"""
    print("\n🧹 Actualizando estadísticas de la base de datos...")
    
    try:
        print("  📊 Ejecutando ANALYZE en tablas principales...")
        cursor.execute("ANALYZE registros;")
        cursor.execute("ANALYZE usuarios;")
        cursor.execute("ANALYZE asistencias;")
        print("  ✅ Estadísticas actualizadas")
    except Exception as e:
        print(f"  ❌ Error actualizando estadísticas: {e}")

def main():
    """Función principal"""
    print("🚀 OPTIMIZADOR DE BASE DE DATOS - PWA SEMBRANDO VIDA")
    print("=" * 60)
    
    # Conectar a la base de datos
    conn = conectar_db()
    if not conn:
        print("❌ No se pudo conectar a la base de datos")
        return
    
    try:
        cursor = conn.cursor()
        
        # Verificar índices existentes
        verificar_indices_existentes(cursor)
        
        # Crear índices optimizados
        crear_indices_optimizados(cursor)
        
        # Confirmar cambios
        conn.commit()
        print("\n✅ Índices creados/verificados exitosamente")
        
        # Limpiar estadísticas
        limpiar_estadisticas_db(cursor)
        conn.commit()
        
        # Analizar rendimiento
        analizar_rendimiento_consultas(cursor)
        
        # Verificar configuración
        optimizar_configuracion_db(cursor)
        
        print("\n🎉 Optimización completada!")
        print("\n💡 Recomendaciones:")
        print("  • Reinicia el servidor de la API para que tome los nuevos índices")
        print("  • Monitorea el rendimiento en las próximas horas")
        print("  • Ejecuta este script semanalmente para mantener optimizado")
        
    except Exception as e:
        print(f"❌ Error durante la optimización: {e}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
