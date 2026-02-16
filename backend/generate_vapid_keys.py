#!/usr/bin/env python
"""
Generador de claves VAPID para Web Push Notifications
Ejecutar: python generate_vapid_keys.py
"""

import base64
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

def generate_vapid_keys():
    """Genera un par de claves VAPID válidas para Web Push"""
    
    # Generar clave privada EC
    private_key = ec.generate_private_key(
        ec.SECP256R1(),
        default_backend()
    )
    
    # Obtener clave pública
    public_key = private_key.public_key()
    
    # Serializar clave privada (formato raw de 32 bytes)
    private_numbers = private_key.private_numbers()
    private_bytes = private_numbers.private_value.to_bytes(32, byteorder='big')
    
    # Serializar clave pública (formato uncompressed point de 65 bytes)
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    
    # Codificar a base64url sin padding
    private_b64 = base64.urlsafe_b64encode(private_bytes).decode('utf-8').rstrip('=')
    public_b64 = base64.urlsafe_b64encode(public_bytes).decode('utf-8').rstrip('=')
    
    return {
        'public_key': public_b64,
        'private_key': private_b64
    }

if __name__ == '__main__':
    keys = generate_vapid_keys()
    
    print("\n" + "="*70)
    print("🔑 CLAVES VAPID GENERADAS PARA WEB PUSH NOTIFICATIONS")
    print("="*70)
    print("\nCopia estas claves a tu archivo push_service.py o variables de entorno:\n")
    print(f"VAPID_PUBLIC_KEY = '{keys['public_key']}'")
    print(f"VAPID_PRIVATE_KEY = '{keys['private_key']}'")
    print("\n" + "="*70)
    print("⚠️  IMPORTANTE: Guarda estas claves de forma segura.")
    print("    La clave privada NO debe compartirse ni exponerse públicamente.")
    print("="*70 + "\n")
