#!/usr/bin/env python3
"""
Script de prueba para crear una notificación de ejemplo
"""

import requests

API_BASE_URL = "http://localhost:8000"

def crear_notificacion_prueba():
    try:
        print("🔔 Creando notificación de prueba...")
        
        # Datos de la notificación
        data = {
            'titulo': 'Notificación de Prueba del Sistema',
            'subtitulo': 'Sistema completamente funcional',
            'descripcion': 'Esta es una notificación de prueba para verificar que todo funciona correctamente. El sistema de notificaciones está operativo.',
            'enlace_url': 'https://sembrandodatos.com',
            'enviada_a_todos': True
        }
        
        response = requests.post(f"{API_BASE_URL}/notificaciones", data=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Notificación creada exitosamente!")
            print(f"   ID: {result.get('id')}")
            print(f"   Título: {result.get('titulo')}")
            print(f"   Enviada a: {result.get('usuarios_destinatarios')}")
            print(f"   Fecha: {result.get('fecha_envio')}")
            
            # Probar obtener la notificación
            print("\n🔍 Obteniendo la notificación creada...")
            get_response = requests.get(f"{API_BASE_URL}/notificaciones/{result.get('id')}")
            
            if get_response.status_code == 200:
                notificacion = get_response.json()
                print("✅ Notificación obtenida correctamente!")
                print(f"   Descripción: {notificacion.get('descripcion')[:50]}...")
                print(f"   Enlace: {notificacion.get('enlace_url')}")
            
        else:
            print(f"❌ Error creando notificación: {response.status_code}")
            print(f"   Mensaje: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def listar_notificaciones():
    try:
        print("\n📋 Listando todas las notificaciones...")
        
        response = requests.get(f"{API_BASE_URL}/notificaciones")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Se encontraron {result.get('total', 0)} notificaciones")
            
            for notif in result.get('notificaciones', []):
                print(f"   - ID {notif['id']}: {notif['titulo']}")
                print(f"     Destinatarios: {notif['destinatarios_texto']}")
                print(f"     Fecha: {notif['fecha_creacion']}")
        else:
            print(f"❌ Error listando notificaciones: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    crear_notificacion_prueba()
    listar_notificaciones()
