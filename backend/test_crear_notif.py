import requests
import json

print('🔧 Probando creación de notificación...')

# Crear notificación de prueba
notif_data = {
    'title': 'Bienvenido al Sistema de Notificaciones',
    'body': 'Esta es la primera notificación del sistema PWA. Todo está funcionando correctamente.',
    'type': 'success',
    'audience': 'all'
}

try:
    response = requests.post('http://localhost:8000/notifications', json=notif_data)
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        result = response.json()
        print(f'✅ Notificación creada con ID: {result["id"]}')
        
        # Listar notificaciones
        list_response = requests.get('http://localhost:8000/notifications')
        if list_response.status_code == 200:
            notifications = list_response.json()
            print(f'📋 Total encontradas: {notifications["total"]}')
        
        # Obtener estadísticas
        stats_response = requests.get('http://localhost:8000/notifications/stats')
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f'📊 Total notificaciones: {stats["general"]["total_notifications"]}')
        
        print('✅ Todo funciona correctamente!')
    else:
        print(f'❌ Error: {response.text}')
except Exception as e:
    print(f'❌ Error: {e}')
