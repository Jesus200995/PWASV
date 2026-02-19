"""
📊 ESTADÍSTICAS EN TIEMPO REAL - USUARIOS POR PLATAFORMA
Ejecutar: python estadisticas_tiempo_real.py
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import time

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

def obtener_estadisticas_completas():
    """Obtiene estadísticas completas de dispositivos"""
    conn = conectar_bd()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        print("\n" + "="*70)
        print(f"📊 ESTADÍSTICAS DE USUARIOS POR PLATAFORMA")
        print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("="*70)
        
        # 1. Total de usuarios
        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        total = cursor.fetchone()['total']
        
        # 2. Por dispositivo
        cursor.execute("""
            SELECT 
                COALESCE(dispositivo, 'Desconocido') as dispositivo,
                COUNT(*) as cantidad,
                ROUND(COUNT(*) * 100.0 / NULLIF((SELECT COUNT(*) FROM usuarios), 0), 2) as porcentaje
            FROM usuarios
            GROUP BY dispositivo
            ORDER BY cantidad DESC
        """)
        dispositivos = cursor.fetchall()
        
        print(f"\n📱 TOTAL DE USUARIOS REGISTRADOS: {total}")
        print("\n" + "-"*70)
        print("DISTRIBUCIÓN POR DISPOSITIVO:")
        print("-"*70)
        
        for disp in dispositivos:
            cantidad = disp['cantidad']
            porcentaje = float(disp['porcentaje'])
            barra = "█" * int(porcentaje / 2)
            
            icono = {
                'Android': '🤖',
                'iOS': '🍎',
                'Desktop': '💻',
                'Desconocido': '❓'
            }.get(disp['dispositivo'], '📱')
            
            print(f"{icono} {disp['dispositivo']:12} {cantidad:6} usuarios ({porcentaje:6.2f}%) {barra}")
        
        # 3. Por rol y dispositivo
        print("\n" + "-"*70)
        print("DISTRIBUCIÓN POR ROL Y DISPOSITIVO:")
        print("-"*70)
        
        cursor.execute("""
            SELECT 
                rol,
                COALESCE(dispositivo, 'Desconocido') as dispositivo,
                COUNT(*) as cantidad
            FROM usuarios
            GROUP BY rol, dispositivo
            ORDER BY rol, cantidad DESC
        """)
        por_rol = cursor.fetchall()
        
        rol_actual = None
        for item in por_rol:
            if item['rol'] != rol_actual:
                rol_actual = item['rol']
                print(f"\n📋 {rol_actual.upper()}:")
            
            icono = {
                'Android': '  🤖',
                'iOS': '  🍎',
                'Desktop': '  💻',
                'Desconocido': '  ❓'
            }.get(item['dispositivo'], '  📱')
            
            print(f"{icono} {item['dispositivo']:12} {item['cantidad']} usuarios")
        
        # 4. Usuarios activos recientes
        print("\n" + "-"*70)
        print("USUARIOS ACTIVOS (ÚLTIMOS 30 DÍAS):")
        print("-"*70)
        
        cursor.execute("""
            SELECT 
                COALESCE(dispositivo, 'Desconocido') as dispositivo,
                COUNT(*) as cantidad,
                ROUND(COUNT(*) * 100.0 / NULLIF((SELECT COUNT(*) FROM usuarios WHERE ultimo_acceso >= NOW() - INTERVAL '30 days'), 0), 2) as porcentaje
            FROM usuarios
            WHERE ultimo_acceso >= NOW() - INTERVAL '30 days'
            GROUP BY dispositivo
            ORDER BY cantidad DESC
        """)
        activos = cursor.fetchall()
        
        if activos:
            total_activos = sum(a['cantidad'] for a in activos)
            print(f"\nTotal activos: {total_activos} usuarios")
            for act in activos:
                icono = {
                    'Android': '🤖',
                    'iOS': '🍎',
                    'Desktop': '💻',
                    'Desconocido': '❓'
                }.get(act['dispositivo'], '📱')
                print(f"{icono} {act['dispositivo']:12} {act['cantidad']:6} usuarios ({float(act['porcentaje']):6.2f}%)")
        else:
            print("⚠️  No hay datos de usuarios activos recientes")
        
        # 5. Últimos 10 accesos
        print("\n" + "-"*70)
        print("ÚLTIMOS 10 ACCESOS:")
        print("-"*70)
        
        cursor.execute("""
            SELECT 
                nombre_completo,
                COALESCE(dispositivo, 'Desconocido') as dispositivo,
                rol,
                ultimo_acceso
            FROM usuarios
            WHERE ultimo_acceso IS NOT NULL
            ORDER BY ultimo_acceso DESC
            LIMIT 10
        """)
        ultimos = cursor.fetchall()
        
        for u in ultimos:
            icono = {
                'Android': '🤖',
                'iOS': '🍎',
                'Desktop': '💻',
                'Desconocido': '❓'
            }.get(u['dispositivo'], '📱')
            
            fecha = u['ultimo_acceso'].strftime('%d/%m/%Y %H:%M') if u['ultimo_acceso'] else 'N/A'
            print(f"{icono} {u['nombre_completo'][:25]:25} {u['dispositivo']:10} {fecha}")
        
        print("\n" + "="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

def modo_monitor(intervalo=30):
    """Modo monitor que actualiza cada X segundos"""
    print("\n🔄 MODO MONITOR ACTIVADO")
    print(f"   Actualizaciones cada {intervalo} segundos")
    print("   Presiona Ctrl+C para detener\n")
    
    try:
        while True:
            obtener_estadisticas_completas()
            print(f"\n⏳ Próxima actualización en {intervalo} segundos...")
            time.sleep(intervalo)
    except KeyboardInterrupt:
        print("\n\n✅ Monitor detenido por el usuario")

if __name__ == "__main__":
    import sys
    
    print("\n" + "="*70)
    print("📱 SISTEMA DE ESTADÍSTICAS DE DISPOSITIVOS")
    print("="*70)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        intervalo = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        modo_monitor(intervalo)
    else:
        obtener_estadisticas_completas()
        print("\n💡 Tip: Usa 'python estadisticas_tiempo_real.py --monitor' para actualizaciones continuas")
        print("    Usa 'python estadisticas_tiempo_real.py --monitor 10' para actualizar cada 10 segundos\n")
