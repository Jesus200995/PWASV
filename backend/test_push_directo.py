#!/usr/bin/env python3
"""Test Push Notifications directo"""
import requests

print("=" * 50)
print("🧪 TEST PUSH NOTIFICATIONS DIRECTO")
print("=" * 50)

# Crear notificación con push
resp = requests.post(
    "http://localhost:8000/notificaciones",
    data={
        "titulo": "Test Push Directo",
        "subtitulo": "Prueba desde script de test",
        "enviada_a_todos": "true",
        "tipo": "general",
        "prioridad": "normal",
        "enviar_push": "true"
    }
)

print(f"\n📤 Respuesta: {resp.status_code}")
print(f"📦 Contenido: {resp.json()}")

result = resp.json()
print(f"\n✅ Notificación ID: {result.get('id')}")
print(f"📲 Push enviadas: {result.get('push_enviadas')}")

if result.get('push_enviadas', 0) == 0:
    print("\n⚠️ No se enviaron push notifications!")
    print("   Posibles causas:")
    print("   1. No hay suscripciones activas")
    print("   2. Error en el servicio de push")
    print("   3. El parámetro enviar_push no está funcionando")
else:
    print(f"\n🎉 ¡{result.get('push_enviadas')} push enviadas exitosamente!")
