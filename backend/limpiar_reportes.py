import psycopg2

# Conectar a la base de datos
conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='app_registros',
    user='jesus',
    password='Jdls2004.'
)

cur = conn.cursor()

# Contar reportes antes
cur.execute('SELECT COUNT(*) FROM reportes')
antes = cur.fetchone()[0]
print(f'📊 Reportes antes de limpiar: {antes}')

# Eliminar todos los reportes
cur.execute('DELETE FROM reportes')
conn.commit()

# Contar reportes después
cur.execute('SELECT COUNT(*) FROM reportes')
despues = cur.fetchone()[0]
print(f'✅ Reportes después de limpiar: {despues}')
print(f'🗑️  Se eliminaron {antes - despues} reportes')

cur.close()
conn.close()
