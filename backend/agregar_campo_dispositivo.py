"""
Script para agregar campo de dispositivo/plataforma a la tabla usuarios
"""
import psycopg2

# Configuración BD
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"

def agregar_campo_dispositivo():
    """Agregar columna de dispositivo a la tabla usuarios"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()
        
        print("🔧 Agregando campo 'dispositivo' a la tabla usuarios...")
        
        # 1. Verificar si la columna ya existe
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='usuarios' AND column_name='dispositivo'
        """)
        
        if cursor.fetchone():
            print("✅ La columna 'dispositivo' ya existe")
        else:
            # Agregar la columna
            cursor.execute("""
                ALTER TABLE usuarios 
                ADD COLUMN dispositivo VARCHAR(50) DEFAULT 'desconocido'
            """)
            conn.commit()
            print("✅ Columna 'dispositivo' agregada exitosamente")
        
        # 2. Agregar columna para user_agent completo (útil para análisis)
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='usuarios' AND column_name='user_agent'
        """)
        
        if cursor.fetchone():
            print("✅ La columna 'user_agent' ya existe")
        else:
            cursor.execute("""
                ALTER TABLE usuarios 
                ADD COLUMN user_agent TEXT DEFAULT NULL
            """)
            conn.commit()
            print("✅ Columna 'user_agent' agregada exitosamente")
        
        # 3. Agregar columna para última actualización de dispositivo
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='usuarios' AND column_name='ultimo_acceso'
        """)
        
        if cursor.fetchone():
            print("✅ La columna 'ultimo_acceso' ya existe")
        else:
            cursor.execute("""
                ALTER TABLE usuarios 
                ADD COLUMN ultimo_acceso TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            """)
            conn.commit()
            print("✅ Columna 'ultimo_acceso' agregada exitosamente")
        
        # 4. Crear índice para búsquedas rápidas por dispositivo
        cursor.execute("""
            SELECT indexname 
            FROM pg_indexes 
            WHERE tablename='usuarios' AND indexname='idx_usuarios_dispositivo'
        """)
        
        if cursor.fetchone():
            print("✅ Índice sobre 'dispositivo' ya existe")
        else:
            cursor.execute("""
                CREATE INDEX idx_usuarios_dispositivo ON usuarios(dispositivo)
            """)
            conn.commit()
            print("✅ Índice creado exitosamente")
        
        print("\n✅ Tabla usuarios actualizada correctamente")
        print("\n📊 Estadísticas actuales:")
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total = cursor.fetchone()[0]
        print(f"   Total de usuarios: {total}")
        
        cursor.execute("""
            SELECT dispositivo, COUNT(*) as cantidad
            FROM usuarios
            GROUP BY dispositivo
            ORDER BY cantidad DESC
        """)
        dispositivos = cursor.fetchall()
        print("\n   Distribución por dispositivo:")
        for disp, cant in dispositivos:
            porcentaje = (cant / total * 100) if total > 0 else 0
            print(f"   - {disp}: {cant} ({porcentaje:.1f}%)")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando actualización de tabla usuarios...\n")
    agregar_campo_dispositivo()
