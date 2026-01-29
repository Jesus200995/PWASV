import requests
import json

# Datos del usuario 463
url = "https://apipwa.sembrandodatos.com/reportes/guardar"

# Obtener actividades simuladas (simplificadas)
actividades = []
for i in range(51):
    actividades.append({
        'id': 600000 + i,
        'fecha_hora': f'2026-01-{(i % 28) + 1:02d}T{(i % 24):02d}:00:00',
        'fecha': f'2026-01-{(i % 28) + 1:02d}T{(i % 24):02d}:00:00',
        'tipo_actividad': 'campo' if i < 30 else 'gabinete',
        'tipo': 'campo' if i < 30 else 'gabinete',
        'descripcion': f'Actividad de prueba {i+1}',
        'foto_url': f'fotos/463_test_{i}.jpg',
        'foto_base64': None
    })

datos_reporte = {
    'usuario': {
        'id': 463,
        'nombre': 'ELSI MAGANA TON GOMEZ',
        'curp': 'TOGE890427MCSNML03',
        'territorio': 'Pichucalco',
        'cargo': 'TECNICO SOCIAL',
        'correo': 'elsi@test.com'
    },
    'periodo': {
        'mes': 0,
        'mesNombre': 'Enero',
        'anio': 2026
    },
    'actividades': actividades,
    'estadisticas': {
        'totalActividades': 51,
        'actividadesCampo': 30,
        'actividadesGabinete': 21,
        'actividadesConFoto': 51
    },
    'fechaGeneracion': '2026-01-29T20:00:00'
}

payload = {
    'usuario_id': 463,
    'nombre_reporte': 'Reporte Enero 2026 (TEST)',
    'mes': 'Enero',
    'anio': 2026,
    'tipo': 'PDF',
    'datos_reporte': datos_reporte,
    'firma_usuario_base64': 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
}

print(f"📦 Tamaño del payload: {len(json.dumps(payload)):,} bytes ({len(json.dumps(payload))/1024:.2f} KB)")
print(f"📊 Actividades: {len(actividades)}")

try:
    print(f"\n🚀 Enviando petición a {url}...")
    response = requests.post(url, json=payload, timeout=30)
    
    print(f"✅ Status Code: {response.status_code}")
    print(f"📄 Response: {response.json()}")
    
except requests.exceptions.Timeout:
    print(f"⏰ Timeout - La petición tardó más de 30 segundos")
except requests.exceptions.ConnectionError as e:
    print(f"🔌 Error de conexión: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    if hasattr(e, 'response'):
        print(f"   Status: {e.response.status_code}")
        print(f"   Body: {e.response.text}")
