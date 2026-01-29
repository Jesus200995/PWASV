#!/usr/bin/env python3
"""
Script para probar la generación de reporte de la usuaria #463
"""
import psycopg2
import json
import sys

# Conectar a la base de datos
try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='app_registros',
        user='jesus',
        password='Jdls2004.'
    )
    cur = conn.cursor()
    print("✅ Conectado a la base de datos")
except Exception as e:
    print(f"❌ Error conectando a BD: {e}")
    sys.exit(1)

# Obtener datos del usuario
usuario_id = 463
print(f"\n📋 Obteniendo datos de usuario {usuario_id}...")

cur.execute("""
    SELECT id, nombre_completo, curp, territorio, cargo, correo
    FROM usuarios WHERE id = %s
""", (usuario_id,))

usuario = cur.fetchone()
if not usuario:
    print(f"❌ Usuario {usuario_id} no encontrado")
    sys.exit(1)

print(f"👤 Usuario: {usuario[1]}")
print(f"   CURP: {usuario[2]}")
print(f"   Territorio: {usuario[3]}")
print(f"   Cargo: {usuario[4]}")

# Obtener actividades de enero 2026
print(f"\n📊 Obteniendo actividades de enero 2026...")

cur.execute("""
    SELECT 
        id, fecha_hora, tipo_actividad, descripcion, 
        foto_url, latitud, longitud
    FROM registros 
    WHERE usuario_id = %s 
    AND EXTRACT(MONTH FROM fecha_hora) = 1 
    AND EXTRACT(YEAR FROM fecha_hora) = 2026
    ORDER BY fecha_hora DESC
""", (usuario_id,))

actividades = cur.fetchall()
print(f"✅ {len(actividades)} actividades encontradas")

# Construir datos_reporte (SIN fotos en base64)
actividades_data = []
for act in actividades:
    actividades_data.append({
        'id': act[0],
        'fecha_hora': act[1].isoformat() if act[1] else None,
        'fecha': act[1].isoformat() if act[1] else None,
        'tipo_actividad': act[2],
        'tipo': act[2],
        'descripcion': act[3],
        'foto_url': act[4],
        'latitud': float(act[5]) if act[5] else None,
        'longitud': float(act[6]) if act[6] else None,
        'foto_base64': None  # NO incluir base64
    })

datos_reporte = {
    'usuario': {
        'id': usuario[0],
        'nombre': usuario[1],
        'curp': usuario[2],
        'territorio': usuario[3],
        'cargo': usuario[4],
        'correo': usuario[5]
    },
    'periodo': {
        'mes': 0,  # Enero
        'mesNombre': 'Enero',
        'anio': 2026
    },
    'actividades': actividades_data,
    'estadisticas': {
        'totalActividades': len(actividades),
        'actividadesCampo': len([a for a in actividades if a[2] and a[2].lower() == 'campo']),
        'actividadesGabinete': len([a for a in actividades if a[2] and a[2].lower() == 'gabinete']),
        'actividadesConFoto': len([a for a in actividades if a[4]])
    }
}

# Convertir a JSON
datos_json = json.dumps(datos_reporte)
print(f"\n📏 Tamaño de datos_reporte:")
print(f"   - JSON string: {len(datos_json):,} bytes ({len(datos_json)/1024:.2f} KB)")
print(f"   - Actividades: {len(actividades)}")
print(f"   - Con foto: {datos_reporte['estadisticas']['actividadesConFoto']}")

# Simular firma (pequeña)
firma_usuario_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

# Intentar guardar
print(f"\n💾 Intentando guardar reporte...")
try:
    cur.execute("""
        INSERT INTO reportes_generados 
        (usuario_id, nombre_reporte, mes, anio, tipo, fecha_generacion, datos_reporte, firma_usuario_base64)
        VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s)
        RETURNING id
    """, (
        usuario_id,
        'Reporte Enero 2026 (TEST)',
        'Enero',
        2026,
        'PDF',
        datos_json,
        firma_usuario_base64
    ))
    
    reporte_id = cur.fetchone()[0]
    conn.commit()
    
    print(f"✅ Reporte guardado exitosamente!")
    print(f"   ID: {reporte_id}")
    
    # Eliminar el reporte de prueba
    print(f"\n🗑️  Eliminando reporte de prueba...")
    cur.execute("DELETE FROM reportes_generados WHERE id = %s", (reporte_id,))
    conn.commit()
    print(f"✅ Reporte de prueba eliminado")
    
except Exception as e:
    conn.rollback()
    print(f"❌ Error guardando reporte: {e}")
    import traceback
    traceback.print_exc()

cur.close()
conn.close()
print(f"\n✅ Prueba completada")
