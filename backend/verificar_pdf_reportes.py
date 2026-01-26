#!/usr/bin/env python3
import psycopg2

conn = psycopg2.connect(host='localhost', database='app_registros', user='jesus', password='2025')
cursor = conn.cursor()

# Verificar columnas de la tabla
cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'reportes_generados'")
cols = cursor.fetchall()
print('Columnas en reportes_generados:')
for c in cols:
    print(f'  - {c[0]}')

# Ver últimos reportes
cursor.execute('SELECT id, nombre_reporte, tipo, CASE WHEN pdf_base64 IS NOT NULL THEN LENGTH(pdf_base64) ELSE 0 END as pdf_len FROM reportes_generados ORDER BY id DESC LIMIT 5')
reportes = cursor.fetchall()
print()
print('Ultimos 5 reportes:')
for r in reportes:
    print(f'  ID: {r[0]}, Nombre: {r[1]}, Tipo: {r[2]}, PDF Length: {r[3]}')

cursor.close()
conn.close()
