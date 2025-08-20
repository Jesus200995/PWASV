import requests
import json

print('🚀 Probando sistema de notificaciones...')

# 1. Probar estadísticas
try:
    response = requests.get('http://localhost:8000/notifications/stats')
    print(f'📊 Estadísticas - Status: {response.status_code}')
    if response.status_code == 200:
        print('✅ Estadísticas funcionando')
        stats = response.json()
        print(f'   Total notificaciones: {stats["general"]["total_notifications"]}')
        print(f'   Dispositivos registrados: {stats["general"]["total_devices"]}')
except Exception as e:
    print(f'❌ Error en estadísticas: {e}')

# 2. Crear notificación de prueba
try:
    notif_data = {
        'title': 'Prueba Sistema',
        'body': 'Probando el sistema de notificaciones',
        'type': 'info',
        'audience': 'all',
        'status': 'draft'
    }

    response = requests.post('http://localhost:8000/notifications', json=notif_data)
    print(f'📝 Crear notificación - Status: {response.status_code}')
    if response.status_code == 200:
        print('✅ Notificación creada exitosamente')
        notif_result = response.json()
        notif_id = notif_result['id']
        print(f'   ID: {notif_id}')
        
        # 3. Obtener detalles de la notificación
        response = requests.get(f'http://localhost:8000/notifications/{notif_id}')
        print(f'🔍 Obtener notificación - Status: {response.status_code}')
        if response.status_code == 200:
            print('✅ Detalles obtenidos correctamente')
    else:
        print(f'❌ Error creando: {response.text}')
except Exception as e:
    print(f'❌ Error en notificación: {e}')

# 4. Listar notificaciones
try:
    response = requests.get('http://localhost:8000/notifications')
    print(f'📋 Listar notificaciones - Status: {response.status_code}')
    if response.status_code == 200:
        print('✅ Lista obtenida correctamente')
        result = response.json()
        print(f'   Total encontradas: {result["total"]}')
except Exception as e:
    print(f'❌ Error en lista: {e}')

print('✅ Pruebas completadas!')
