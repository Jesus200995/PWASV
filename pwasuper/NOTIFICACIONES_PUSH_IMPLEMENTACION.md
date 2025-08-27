# Configuración de Notificaciones Push - Backend

## 📱 Implementación Completa de Push Notifications

Este documento describe cómo configurar el backend para soportar notificaciones push en tu PWA.

## 🚀 Frontend Ya Implementado

El frontend ya está completamente configurado con:

✅ **Service Worker actualizado** - Maneja notificaciones push
✅ **Servicio de Push Notifications** - Gestiona suscripciones
✅ **Composable reactivo** - Estado de notificaciones
✅ **Componente de configuración** - UI para activar/desactivar
✅ **Integración en vista** - Configuración en página de notificaciones

## 🔧 Backend Requerido

Para que las notificaciones push funcionen completamente, necesitas implementar estos endpoints en tu backend:

### 1. Endpoint para obtener clave VAPID pública

```python
# En tu main.py de FastAPI
from fastapi import FastAPI

app = FastAPI()

# Configurar tus claves VAPID (generar con py-vapid)
VAPID_PRIVATE_KEY = "tu_clave_privada_vapid"
VAPID_PUBLIC_KEY = "tu_clave_publica_vapid"

@app.get("/api/vapid-public-key")
async def get_vapid_public_key():
    return {"publicKey": VAPID_PUBLIC_KEY}
```

### 2. Endpoint para registrar suscripciones

```python
from pydantic import BaseModel

class PushSubscription(BaseModel):
    usuario_id: int
    endpoint: str
    keys: dict
    userAgent: str = None
    deviceInfo: dict = None

@app.post("/api/push/subscribe")
async def subscribe_to_push(subscription: PushSubscription):
    # Guardar en base de datos
    # Estructura sugerida:
    # - id (primary key)
    # - usuario_id (foreign key)
    # - endpoint (unique)
    # - p256dh_key 
    # - auth_key
    # - user_agent
    # - device_type
    # - created_at
    # - is_active
    
    return {"success": True, "message": "Suscripción registrada"}
```

### 3. Endpoint para desuscribirse

```python
class PushUnsubscribe(BaseModel):
    usuario_id: int

@app.post("/api/push/unsubscribe") 
async def unsubscribe_from_push(data: PushUnsubscribe):
    # Desactivar suscripción en BD
    return {"success": True}
```

### 4. Función para enviar notificaciones push

```python
import json
from pywebpush import webpush, WebPushException

def send_push_notification(subscription_info, title, body, data=None):
    """
    Enviar notificación push a un dispositivo específico
    """
    try:
        payload = {
            "title": title,
            "body": body,
            "icon": "/pwa-192x192.png",
            "badge": "/pwa-192x192.png",
            "data": data or {}
        }
        
        response = webpush(
            subscription_info={
                "endpoint": subscription_info["endpoint"],
                "keys": subscription_info["keys"]
            },
            data=json.dumps(payload),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={
                "sub": "mailto:admin@sembrandodatos.com"
            }
        )
        
        return True, response
        
    except WebPushException as ex:
        print(f"Error enviando push: {ex}")
        return False, str(ex)
```

### 5. Integración con sistema de notificaciones existente

```python
async def enviar_notificacion_con_push(usuario_id, titulo, descripcion, datos_extra=None):
    """
    Enviar notificación regular + push notification
    """
    
    # 1. Crear notificación en BD (tu código existente)
    notificacion = await crear_notificacion_bd(usuario_id, titulo, descripcion)
    
    # 2. Obtener suscripciones push activas del usuario
    suscripciones = await obtener_suscripciones_usuario(usuario_id)
    
    # 3. Enviar push a cada dispositivo suscrito
    for suscripcion in suscripciones:
        success, response = send_push_notification(
            subscription_info={
                "endpoint": suscripcion.endpoint,
                "keys": {
                    "p256dh": suscripcion.p256dh_key,
                    "auth": suscripcion.auth_key
                }
            },
            title=titulo,
            body=descripcion,
            data={
                "id": notificacion.id,
                "url": "/notificaciones"
            }
        )
        
        if not success:
            # Marcar suscripción como inactiva si falla
            await desactivar_suscripcion(suscripcion.id)
    
    return notificacion
```

## 📦 Dependencias Python Requeridas

Agregar a `requirements.txt`:

```
pywebpush==1.14.0
py-vapid==1.9.0
```

## 🛠️ Generar Claves VAPID

```bash
# Instalar vapid
pip install py-vapid

# Generar claves
vapid --gen

# Te dará algo como:
# Private Key: aBCdEf123456...
# Public Key: BCqXwzlcjKCh4YjQcOd5TnVw4PKZgKjOchWP...
```

## 🗄️ Tabla de Base de Datos Sugerida

```sql
CREATE TABLE push_subscriptions (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    endpoint VARCHAR(500) NOT NULL UNIQUE,
    p256dh_key VARCHAR(200) NOT NULL,
    auth_key VARCHAR(50) NOT NULL,
    user_agent TEXT,
    device_type VARCHAR(50),
    platform VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Índice para consultas rápidas
CREATE INDEX idx_push_subscriptions_usuario ON push_subscriptions(usuario_id);
CREATE INDEX idx_push_subscriptions_active ON push_subscriptions(is_active);
```

## 🧪 Prueba en Desarrollo

En modo desarrollo, el frontend funciona con datos simulados. Para probar push notifications reales:

1. Implementa los endpoints del backend
2. Configura las claves VAPID
3. Despliega en HTTPS (las push notifications requieren HTTPS)
4. Activa las notificaciones desde la PWA
5. Envía una notificación desde el panel admin

## 🔐 Consideraciones de Seguridad

- **VAPID keys**: Mantén la clave privada segura
- **HTTPS**: Las push notifications solo funcionan en HTTPS
- **Validación**: Valida que el usuario tenga permisos para la notificación
- **Rate limiting**: Limita el número de notificaciones por usuario
- **Cleanup**: Limpia suscripciones inactivas periódicamente

## 📱 Funcionamiento

Una vez implementado:

1. Usuario abre PWA → ve opción de activar push notifications
2. Usuario activa → se registra suscripción en backend
3. Admin envía notificación → llega como push + aparece en la app
4. Usuario hace clic en push → abre la app en /notificaciones

## ✨ Características Implementadas en Frontend

- 🔔 **Activación/Desactivación** - Toggle intuitivo
- 📱 **Detección automática** - Verifica compatibilidad del navegador
- 🔧 **Modo desarrollo** - Funciona con datos simulados
- 🎯 **Navegación inteligente** - Abre app en notificaciones al hacer clic
- ⚡ **Estados reactivos** - UI actualizada en tiempo real
- 🛠️ **Debug info** - Información técnica para desarrollo
- 📊 **Gestión de permisos** - Manejo de estados de autorización

¡Ya tienes todo el frontend listo! Solo necesitas implementar el backend. 🚀
