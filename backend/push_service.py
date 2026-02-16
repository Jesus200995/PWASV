# push_service.py
# Servicio de Web Push Notifications para PWASUPER
# Sistema Empresarial - Estilo Mercado Libre
# Requiere: pip install pywebpush py-vapid

import json
import os
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

# Intentar importar pywebpush - si no está instalado, las funciones fallarán gracefully
try:
    from pywebpush import webpush, WebPushException
    WEBPUSH_AVAILABLE = True
except ImportError:
    WEBPUSH_AVAILABLE = False
    print("⚠️ pywebpush no está instalado. Ejecuta: pip install pywebpush py-vapid")

# Configuración VAPID - IMPORTANTE: Estas son las claves de producción
# Generadas con: python generate_vapid_keys.py

# Claves VAPID para Web Push Notifications
VAPID_PUBLIC_KEY = os.environ.get('VAPID_PUBLIC_KEY', 'BD-0z4EAUumFxy-j6VQZS5udEjQEyYveFrxr_vwSctewA4Ktayin9zOWNy-GWEBon40sM4D2IEHC4sO8EbChBzI')
VAPID_PRIVATE_KEY = os.environ.get('VAPID_PRIVATE_KEY', 'OzDa4UD4CaY87eXfEnC4m2jv2Dtgd0pOav6sG9HrjPs')
VAPID_CLAIMS = {
    "sub": "mailto:admin@sembrandodatos.com"
}

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE TIPOS DE NOTIFICACIÓN - ESTILO EMPRESARIAL
# ═══════════════════════════════════════════════════════════════════════════════

NOTIFICATION_TYPES = {
    "info": {
        "icon": "/icons/info-notification.png",
        "badge": "/badge-72x72.png",
        "color": "#3B82F6",
        "emoji": "ℹ️"
    },
    "success": {
        "icon": "/icons/success-notification.png", 
        "badge": "/badge-72x72.png",
        "color": "#10B981",
        "emoji": "✅"
    },
    "warning": {
        "icon": "/icons/warning-notification.png",
        "badge": "/badge-72x72.png", 
        "color": "#F59E0B",
        "emoji": "⚠️"
    },
    "urgent": {
        "icon": "/icons/urgent-notification.png",
        "badge": "/badge-72x72.png",
        "color": "#EF4444",
        "emoji": "🚨"
    },
    "message": {
        "icon": "/icons/message-notification.png",
        "badge": "/badge-72x72.png",
        "color": "#8B5CF6",
        "emoji": "💬"
    },
    "reminder": {
        "icon": "/icons/reminder-notification.png",
        "badge": "/badge-72x72.png",
        "color": "#EC4899",
        "emoji": "🔔"
    },
    "general": {
        "icon": "/pwa-192x192.png",
        "badge": "/badge-72x72.png",
        "color": "#10B981",
        "emoji": "📢"
    }
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
    """
    Modelo para una notificación push empresarial
    Similar a las notificaciones de Mercado Libre, Amazon, etc.
    """
    titulo: str
    mensaje: str
    # Tipo determina el estilo visual
    tipo: str = "general"  # info, success, warning, urgent, message, reminder, general
    # Prioridad determina comportamiento
    prioridad: str = "normal"  # baja, normal, alta, urgent
    # Personalización visual
    icono: str = None  # Si es None, se usa el del tipo
    badge: str = None
    imagen: str = None  # Imagen grande (Big Picture style)
    color_acento: str = None  # Si es None, se usa el del tipo
    # Navegación
    url_destino: str = "/notificaciones"
    # Identificación
    notificacion_id: int = None
    tag: str = None
    # Contenido adicional
    subtitulo: str = None  # Línea secundaria
    # Acciones personalizadas
    acciones: List[Dict] = None
    # Comportamiento
    silenciosa: bool = False
    requiere_interaccion: bool = None  # Si es None, depende de prioridad
    # Datos extra para la app
    extra: Dict = None
    
    def to_payload(self) -> str:
        """
        Convertir a JSON payload empresarial para enviar
        Formato compatible con el Service Worker v3.0.0
        """
        # Obtener configuración del tipo
        type_config = NOTIFICATION_TYPES.get(self.tipo, NOTIFICATION_TYPES["general"])
        
        # Determinar icono (personalizado > tipo > default)
        icono = self.icono or type_config["icon"]
        
        # Determinar badge
        badge = self.badge or type_config["badge"]
        
        # Determinar color de acento
        color = self.color_acento or type_config["color"]
        
        # Determinar comportamiento según prioridad
        prioridad_map = {
            "baja": "low",
            "normal": "normal", 
            "alta": "high",
            "urgent": "urgent",
            "media": "high"
        }
        prioridad_normalizada = prioridad_map.get(self.prioridad, self.prioridad)
        
        # Vibración según prioridad
        vibration_patterns = {
            "low": [50, 25, 50],
            "normal": [100, 50, 100],
            "high": [150, 75, 150],
            "urgent": [200, 100, 200, 100, 200]
        }
        vibrate = vibration_patterns.get(prioridad_normalizada, [100, 50, 100])
        
        # Requerir interacción para prioridades altas
        require_interaction = self.requiere_interaccion
        if require_interaction is None:
            require_interaction = prioridad_normalizada in ["high", "urgent"]
        
        # Construir payload rico
        payload = {
            # Contenido principal
            "title": self.titulo,
            "body": self.mensaje,
            "subtitle": self.subtitulo,
            
            # Visual
            "icon": icono,
            "badge": badge,
            "image": self.imagen,
            "color_acento": color,
            
            # Tipo y prioridad
            "tipo": self.tipo,
            "prioridad": prioridad_normalizada,
            
            # Identificación
            "notificacion_id": self.notificacion_id,
            "tag": self.tag or f"sv-{self.tipo}-{self.notificacion_id or 'general'}-{int(datetime.now().timestamp())}",
            
            # Navegación
            "url": self.url_destino,
            
            # Comportamiento
            "silent": self.silenciosa,
            "requireInteraction": require_interaction,
            "vibrate": vibrate,
            "renotify": True,
            
            # Acciones
            "actions": self._build_actions(),
            
            # Datos adicionales
            "extra": self.extra or {},
            
            # Timestamp
            "timestamp": int(datetime.now().timestamp() * 1000)
        }
        
        return json.dumps(payload, ensure_ascii=False)
    
    def _build_actions(self) -> List[Dict]:
        """Construir acciones según tipo de notificación"""
        if self.acciones:
            return self.acciones
        
        # Acciones predeterminadas según tipo
        actions_by_type = {
            "message": [
                {"action": "reply", "title": "💬 Responder"},
                {"action": "open", "title": "📖 Ver"}
            ],
            "urgent": [
                {"action": "open", "title": "🚨 Ver ahora"},
                {"action": "remind", "title": "⏰ Recordar"}
            ],
            "reminder": [
                {"action": "complete", "title": "✓ Completado"},
                {"action": "snooze", "title": "⏰ Posponer"}
            ],
            "warning": [
                {"action": "open", "title": "⚠️ Ver detalle"},
                {"action": "dismiss", "title": "✕ Ignorar"}
            ],
            "success": [
                {"action": "open", "title": "✅ Ver"},
                {"action": "dismiss", "title": "✕ Cerrar"}
            ]
        }
        
        return actions_by_type.get(self.tipo, [
            {"action": "open", "title": "📖 Ver detalle"},
            {"action": "dismiss", "title": "✕ Descartar"}
        ])


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
