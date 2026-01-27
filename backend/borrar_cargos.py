#!/usr/bin/env python3
"""
Script para borrar los cargos de todos los usuarios
"""
import psycopg2

# Conexión a la base de datos
conn = psycopg2.connect(
    host="localhost",
    database="app_registros",
    user="jesus",
    password="2025"
)

cursor = conn.cursor()

# Actualizar cargo a string vacío
cursor.execute("UPDATE usuarios SET cargo = ''")
rows_affected = cursor.rowcount

conn.commit()
cursor.close()
conn.close()

print(f"Cargos borrados de {rows_affected} usuarios")
