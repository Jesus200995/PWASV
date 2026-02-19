"""
Script para verificar usuarios y estadísticas de plataforma
"""
import psycopg2
from psycopg2.extras import RealDictCursor

# Configuración BD
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"

def conectar_bd():
    """Conectar a la base de datos"""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def obtener_estadisticas():
    """Obtener estadísticas de usuarios"""
    conn = conectar_bd()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # 1. Verificar estructura de la tabla usuarios
        print("=" * 60)
        print("📊 VERIFICANDO ESTRUCTURA DE TABLA USUARIOS")
        print("=" * 60)
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'usuarios'
            ORDER BY ordinal_position
        """)
        columnas = cursor.fetchall()
        print("\n📋 Columnas disponibles:")
        for col in columnas:
            print(f"   - {col['column_name']}: {col['data_type']}")
        
        # 2. Total de usuarios registrados
        print("\n" + "=" * 60)
        print("👥 ESTADÍSTICAS DE USUARIOS REGISTRADOS")
        print("=" * 60)
        
        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        total = cursor.fetchone()['total']
        print(f"\n✅ Total usuarios registrados: {total}")
        
        # 3. Usuarios por rol
        cursor.execute("""
            SELECT rol, COUNT(*) as cantidad
            FROM usuarios
            GROUP BY rol
            ORDER BY cantidad DESC
        """)
        roles = cursor.fetchall()
        print("\n📊 Distribución por rol:")
        for rol in roles:
            porcentaje = (rol['cantidad'] / total * 100) if total > 0 else 0
            print(f"   - {rol['rol']}: {rol['cantidad']} ({porcentaje:.1f}%)")
        
        # 4. Usuarios activos vs inactivos (si existe el campo)
        try:
            cursor.execute("""
                SELECT activo, COUNT(*) as cantidad
                FROM usuarios
                GROUP BY activo
            """)
            activos = cursor.fetchall()
            print("\n📊 Estado de usuarios:")
            for estado in activos:
                activo_texto = "Activos" if estado['activo'] else "Inactivos"
                porcentaje = (estado['cantidad'] / total * 100) if total > 0 else 0
                print(f"   - {activo_texto}: {estado['cantidad']} ({porcentaje:.1f}%)")
        except:
            print("\n⚠️  Campo 'activo' no disponible")
        
        # 5. Verificar si hay información de plataforma/dispositivo
        print("\n" + "=" * 60)
        print("📱 INFORMACIÓN DE DISPOSITIVOS/PLATAFORMA")
        print("=" * 60)
        
        # Buscar columnas relacionadas con dispositivos
        columnas_dispositivo = [col for col in columnas if any(
            keyword in col['column_name'].lower() 
            for keyword in ['device', 'platform', 'user_agent', 'mobile', 'os', 'browser']
        )]
        
        if columnas_dispositivo:
            print("\n✅ Se encontraron columnas relacionadas con dispositivos:")
            for col in columnas_dispositivo:
                print(f"   - {col['column_name']}")
                cursor.execute(f"SELECT {col['column_name']}, COUNT(*) as cantidad FROM usuarios GROUP BY {col['column_name']}")
                datos = cursor.fetchall()
                for dato in datos:
                    print(f"      • {dato[col['column_name']]}: {dato['cantidad']}")
        else:
            print("\n❌ NO se encontraron columnas con información de dispositivos")
            print("\n💡 La tabla usuarios NO está guardando información sobre:")
            print("   - Tipo de dispositivo (Android/iOS)")
            print("   - User Agent")
            print("   - Sistema operativo")
            print("   - Navegador")
        
        # 6. Verificar otras tablas que puedan tener info de dispositivos
        print("\n" + "=" * 60)
        print("🔍 BUSCANDO EN OTRAS TABLAS")
        print("=" * 60)
        
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        tablas = cursor.fetchall()
        
        tablas_relevantes = []
        for tabla in tablas:
            nombre = tabla['table_name']
            if any(keyword in nombre.lower() for keyword in ['session', 'device', 'login', 'access', 'log']):
                tablas_relevantes.append(nombre)
                cursor.execute(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = '{nombre}'
                    ORDER BY ordinal_position
                """)
                cols = cursor.fetchall()
                print(f"\n📋 Tabla '{nombre}':")
                print(f"   Columnas: {', '.join([c['column_name'] for c in cols])}")
        
        if not tablas_relevantes:
            print("\n❌ No se encontraron tablas con información de sesiones/dispositivos")
        
        # 7. Últimos registros para análisis
        print("\n" + "=" * 60)
        print("📅 ÚLTIMOS REGISTROS")
        print("=" * 60)
        
        cursor.execute("""
            SELECT id, correo, nombre_completo, rol, 
                   DATE(fecha_creacion) as fecha 
            FROM usuarios 
            ORDER BY fecha_creacion DESC 
            LIMIT 5
        """)
        ultimos = cursor.fetchall()
        print("\nÚltimos 5 usuarios registrados:")
        for u in ultimos:
            print(f"   - {u['nombre_completo']} ({u['rol']}) - {u['fecha']}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("\n🚀 INICIANDO ANÁLISIS DE USUARIOS Y PLATAFORMAS\n")
    obtener_estadisticas()
    print("\n" + "=" * 60)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 60)
