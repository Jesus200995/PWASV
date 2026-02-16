# push_service.py
# Servicio de Web Push Notifications para PWASUPER
# Requiere: pip install pywebpush py-vapid

import json
import os
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

# Intentar importar pywebpush - si no está instalado, las funciones fallarán gracefully
try:
    from pywebpush import webpush, WebPushException
    WEBPUSH_AVAILABLE = True
except ImportError:
    WEBPUSH_AVAILABLE = False
    print("⚠️ pywebpush no está instalado. Ejecuta: pip install pywebpush py-vapid")

# Configuración VAPID - IMPORTANTE: Generar claves únicas para producción
# Puedes generar nuevas claves con: python -c "from py_vapid import Vapid; v = Vapid(); v.generate_keys(); print('PUBLIC:', v.public_key_urlsafe_base64); print('PRIVATE:', v.private_key_urlsafe_base64)"

# Claves VAPID por defecto (reemplazar con las generadas para producción)
VAPID_PUBLIC_KEY = os.environ.get('VAPID_PUBLIC_KEY', 'BHdnfVJMpZTJu4XxLSQKIKyLXGrQQFHYzYDwNmCBfQVAj9j7WRwKRKvjwN-7qM8_kHTp6F2NVpQWVZ1BcLfCZnc')
VAPID_PRIVATE_KEY = os.environ.get('VAPID_PRIVATE_KEY', 'dGVzdC1wcml2YXRlLWtleS1mb3ItZGV2ZWxvcG1lbnQtb25seQ')
VAPID_CLAIMS = {
    "sub": "mailto:admin@sembrandodatos.com"
}

@dataclass
class PushSubscription:
    """Modelo para una suscripción push"""
    endpoint: str
    p256dh: str
    auth: str
    usuario_id: int = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "endpoint": self.endpoint,
            "keys": {
                "p256dh": self.p256dh,
                "auth": self.auth
            }
        }

@dataclass
class PushNotification:
    """Modelo para una notificación push"""
    titulo: str
    mensaje: str
    icono: str = "/pwa-192x192.png"
    badge: str = "/pwa-192x192.png"
    url_destino: str = "/"
    tag: str = None
    notificacion_id: int = None
    tipo: str = "general"
    prioridad: str = "normal"
    color_acento: str = None
    imagen: str = None
    acciones: List[Dict] = None
    
    def to_payload(self) -> str:
        """Convertir a JSON payload para enviar"""
        payload = {
            "title": self.titulo,
            "body": self.mensaje,
            "icon": self.icono,
            "badge": self.badge,
            "data": {
                "url": self.url_destino,
                "notificacion_id": self.notificacion_id,
                "tipo": self.tipo,
                "prioridad": self.prioridad,
                "timestamp": None  # Se llenará en el SW
            },
            "tag": self.tag or f"notif-{self.notificacion_id or 'general'}",
            "renotify": True,
            "requireInteraction": self.prioridad in ["high", "urgent"],
            "vibrate": [100, 50, 100] if self.prioridad == "normal" else [200, 100, 200, 100, 200]
        }
        
        # Agregar imagen si existe
        if self.imagen:
            payload["image"] = self.imagen
            
        # Agregar color de acento si existe
        if self.color_acento:
            payload["data"]["colorAccent"] = self.color_acento
        
        # Agregar acciones por defecto
        if self.acciones:
            payload["actions"] = self.acciones
        else:
            payload["actions"] = [
                {"action": "open", "title": "Ver", "icon": "/icons/view.png"},
                {"action": "dismiss", "title": "Cerrar", "icon": "/icons/close.png"}
            ]
        
        return json.dumps(payload)


class PushService:
    """Servicio principal para enviar Push Notifications"""
    
    def __init__(self, public_key: str = None, private_key: str = None, claims: dict = None):
        self.public_key = public_key or VAPID_PUBLIC_KEY
        self.private_key = private_key or VAPID_PRIVATE_KEY
        self.claims = claims or VAPID_CLAIMS
        
        if not WEBPUSH_AVAILABLE:
            print("⚠️ PushService: pywebpush no disponible, las notificaciones push no funcionarán")
    
    def get_vapid_public_key(self) -> str:
        """Obtener la clave pública VAPID para el cliente"""
        return self.public_key
    
    def send_notification(self, subscription: PushSubscription, notification: PushNotification) -> Dict[str, Any]:
        """
        Enviar una notificación push a una suscripción específica
        
        Returns:
            Dict con 'success' bool y 'error' si falló
        """
        if not WEBPUSH_AVAILABLE:
            return {"success": False, "error": "pywebpush no está instalado"}
        
        try:
            response = webpush(
                subscription_info=subscription.to_dict(),
                data=notification.to_payload(),
                vapid_private_key=self.private_key,
                vapid_claims=self.claims.copy()
            )
            
            print(f"✅ Push enviado exitosamente a {subscription.endpoint[:50]}...")
            return {"success": True, "status_code": response.status_code}
            
        except WebPushException as e:
            error_msg = str(e)
            print(f"❌ Error enviando push: {error_msg}")
            
            # Detectar si la suscripción expiró o es inválida
            if e.response and e.response.status_code in [404, 410]:
                return {
                    "success": False, 
                    "error": "subscription_expired",
                    "should_remove": True,
                    "status_code": e.response.status_code
                }
            
            return {"success": False, "error": error_msg}
            
        except Exception as e:
            print(f"❌ Error inesperado enviando push: {e}")
            return {"success": False, "error": str(e)}
    
    def send_to_multiple(self, subscriptions: List[PushSubscription], notification: PushNotification) -> Dict[str, Any]:
        """
        Enviar notificación a múltiples suscripciones
        
        Returns:
            Dict con estadísticas de envío
        """
        results = {
            "total": len(subscriptions),
            "sent": 0,
            "failed": 0,
            "expired": [],  # Lista de endpoints expirados para eliminar
            "errors": []
        }
        
        for sub in subscriptions:
            result = self.send_notification(sub, notification)
            
            if result.get("success"):
                results["sent"] += 1
            else:
                results["failed"] += 1
                if result.get("should_remove"):
                    results["expired"].append(sub.endpoint)
                else:
                    results["errors"].append({
                        "endpoint": sub.endpoint[:50],
                        "error": result.get("error", "Unknown error")
                    })
        
        print(f"📊 Push batch: {results['sent']}/{results['total']} enviados, {results['failed']} fallidos")
        return results


# Instancia global del servicio
push_service = PushService()


def generate_vapid_keys():
    """
    Utilidad para generar nuevas claves VAPID
    Ejecutar una vez para producción y guardar las claves de forma segura
    """
    try:
        from py_vapid import Vapid
        
        vapid = Vapid()
        vapid.generate_keys()
        
        return {
            "public_key": vapid.public_key_urlsafe_base64,
            "private_key": vapid.private_key_urlsafe_base64,
            "instructions": "Guarda estas claves de forma segura. La pública va en el frontend, la privada solo en el backend."
        }
    except ImportError:
        return {
            "error": "py-vapid no está instalado. Ejecuta: pip install py-vapid"
        }


# Función helper para testing
def test_push_notification():
    """Test básico del sistema de push"""
    print("=" * 50)
    print("🧪 Test de Push Notifications")
    print("=" * 50)
    print(f"pywebpush disponible: {WEBPUSH_AVAILABLE}")
    print(f"VAPID Public Key: {VAPID_PUBLIC_KEY[:30]}...")
    print("=" * 50)
    
    if not WEBPUSH_AVAILABLE:
        print("❌ Instala pywebpush para completar el test")
        return False
    
    print("✅ Sistema de push listo")
    return True


if __name__ == "__main__":
    test_push_notification()
    
    # Generar nuevas claves si es necesario
    print("\n🔑 Generando nuevas claves VAPID...")
    keys = generate_vapid_keys()
    print(json.dumps(keys, indent=2))
