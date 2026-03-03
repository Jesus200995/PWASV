#!/usr/bin/env python3
import psycopg2

conn = psycopg2.connect(
    host='31.97.8.51',
    database='app_registros',
    user='jesus',
    password='2025'
)
cursor = conn.cursor()

print("=== Territorios disponibles ===")
cursor.execute("SELECT DISTINCT territorio FROM usuarios WHERE territorio IS NOT NULL AND territorio != '' LIMIT 20")
result = cursor.fetchall()
for r in result:
    print(f"  - {r[0]}")

print("\n=== Probando filtro por territorio 'Ocosingo' ===")
query = """
SELECT 
    u.territorio,
    COUNT(DISTINCT CASE WHEN UPPER(COALESCE(u.cargo, '')) LIKE '%%SOCIAL%%' THEN u.id END) as tecnicos_social,
    COUNT(DISTINCT CASE WHEN UPPER(COALESCE(u.cargo, '')) LIKE '%%PRODUCTIVO%%' THEN u.id END) as tecnicos_productivo,
    COUNT(DISTINCT u.id) as total_tecnicos
FROM usuarios u
WHERE u.territorio IS NOT NULL 
AND u.territorio != ''
AND COALESCE(u.activo, true) = TRUE
AND u.territorio = %s
GROUP BY u.territorio 
ORDER BY u.territorio
"""

try:
    cursor.execute(query, ('Ocosingo',))
    result = cursor.fetchall()
    print(f"Resultado: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

conn.close()
