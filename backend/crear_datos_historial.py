import psycopg2
from datetime import datetime, timedelta
import json
import random

# Configuración de la base de datos
DB_HOST = "31.97.8.51"
DB_NAME = "app_registros"
DB_USER = "jesus"
DB_PASS = "2025"

def crear_datos_prueba():
    """Crear datos de prueba para la tabla historial"""
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
        )
        cursor = conn.cursor()
        
        print("✅ Conexión a la base de datos exitosa")
        
        # Verificar que existe la tabla historial
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'historial'
            );
        """)
        tabla_existe = cursor.fetchone()[0]
        
        if not tabla_existe:
            print("❌ La tabla 'historial' no existe. Creándola...")
            cursor.execute("""
                CREATE TABLE historial (
                    id SERIAL PRIMARY KEY,
                    usuario_id INTEGER REFERENCES usuarios(id),
                    tipo VARCHAR(30), -- 'entrada', 'salida', 'actividad'
                    descripcion TEXT,
                    fecha DATE NOT NULL,
                    hora TIME NOT NULL,
                    detalles JSONB, -- para guardar ubicación, foto_url, etc.
                    creado_en TIMESTAMP DEFAULT NOW()
                );
            """)
            print("✅ Tabla 'historial' creada")
        
        # Obtener algunos usuarios existentes
        cursor.execute("SELECT id, nombre_completo FROM usuarios LIMIT 5")
        usuarios = cursor.fetchall()
        
        if not usuarios:
            print("❌ No hay usuarios en la base de datos")
            return
        
        print(f"📊 Usuarios encontrados: {len(usuarios)}")
        
        # Crear datos de prueba para los últimos 30 días
        tipos_actividad = ['entrada', 'salida', 'actividad']
        descripciones = {
            'entrada': [
                'Llegada a la oficina',
                'Inicio de jornada laboral',
                'Entrada después del almuerzo',
                'Regreso de reunión externa'
            ],
            'salida': [
                'Fin de jornada laboral',
                'Salida para almuerzo',
                'Salida por cita médica',
                'Fin de turno'
            ],
            'actividad': [
                'Reunión de equipo',
                'Capacitación técnica',
                'Revisión de proyectos',
                'Llamada con cliente',
                'Trabajo en campo',
                'Mantenimiento de equipo'
            ]
        }
        
        # Generar datos para los últimos 30 días
        fecha_base = datetime.now().date()
        registros_creados = 0
        
        for i in range(30):  # Últimos 30 días
            fecha_actual = fecha_base - timedelta(days=i)
            
            # Saltar fines de semana para algunos tipos de actividad
            es_fin_semana = fecha_actual.weekday() >= 5
            
            for usuario_id, nombre_usuario in usuarios:
                # Generar entre 1 y 4 actividades por día (menos en fines de semana)
                num_actividades = random.randint(1, 2 if es_fin_semana else 4)
                
                for _ in range(num_actividades):
                    tipo = random.choice(tipos_actividad)
                    descripcion = random.choice(descripciones[tipo])
                    
                    # Generar hora aleatoria durante el día laboral
                    if tipo == 'entrada':
                        hora = datetime.strptime(f"{random.randint(7, 9)}:{random.randint(0, 59):02d}", "%H:%M").time()
                    elif tipo == 'salida':
                        hora = datetime.strptime(f"{random.randint(16, 18)}:{random.randint(0, 59):02d}", "%H:%M").time()
                    else:  # actividad
                        hora = datetime.strptime(f"{random.randint(9, 17)}:{random.randint(0, 59):02d}", "%H:%M").time()
                    
                    # Generar detalles aleatorios
                    detalles = {
                        "ubicacion": {
                            "lat": round(19.4326 + random.uniform(-0.01, 0.01), 6),
                            "lng": round(-99.1332 + random.uniform(-0.01, 0.01), 6)
                        },
                        "dispositivo": random.choice(["Móvil Android", "Móvil iOS", "Navegador Web"]),
                        "ip": f"192.168.1.{random.randint(100, 200)}"
                    }
                    
                    if tipo == 'actividad':
                        detalles["duracion_estimada"] = f"{random.randint(30, 240)} minutos"
                        detalles["departamento"] = random.choice(["IT", "RRHH", "Ventas", "Operaciones"])
                    
                    # Insertar registro
                    cursor.execute("""
                        INSERT INTO historial (usuario_id, tipo, descripcion, fecha, hora, detalles)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        usuario_id,
                        tipo,
                        descripcion,
                        fecha_actual,
                        hora,
                        json.dumps(detalles)
                    ))
                    
                    registros_creados += 1
        
        # Confirmar transacción
        conn.commit()
        print(f"✅ Se crearon {registros_creados} registros de historial")
        
        # Mostrar estadísticas
        cursor.execute("""
            SELECT 
                tipo,
                COUNT(*) as cantidad
            FROM historial 
            GROUP BY tipo 
            ORDER BY cantidad DESC
        """)
        stats = cursor.fetchall()
        
        print("\n📊 Estadísticas de registros creados:")
        for tipo, cantidad in stats:
            print(f"  {tipo.capitalize()}: {cantidad}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    crear_datos_prueba()
