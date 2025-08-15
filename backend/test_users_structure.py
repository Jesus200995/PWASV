import psycopg2
from psycopg2.extras import RealDictCursor

try:
    conn = psycopg2.connect(
        host='31.97.8.51',
        database='app_registros', 
        user='jesus',
        password='2025',
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    
    # Obtener estructura de la tabla usuarios
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_schema = 'public' AND table_name = 'usuarios'
        ORDER BY ordinal_position;
    """)
    
    columns = cursor.fetchall()
    print('📊 Estructura de la tabla usuarios:')
    print('=' * 50)
    for col in columns:
        print(f'• {col["column_name"]} ({col["data_type"]}) - Nullable: {col["is_nullable"]} - Default: {col["column_default"]}')
    
    # También obtener un usuario de ejemplo para ver qué campos tienen datos
    cursor.execute("SELECT * FROM usuarios LIMIT 1")
    user_sample = cursor.fetchone()
    
    if user_sample:
        print('\n📋 Campos disponibles en un usuario ejemplo:')
        print('=' * 50)
        for key, value in user_sample.items():
            print(f'• {key}: {value}')
    else:
        print('\n⚠️ No hay usuarios en la tabla')
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f'❌ Error: {e}')
