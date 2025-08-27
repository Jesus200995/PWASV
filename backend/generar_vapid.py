#!/usr/bin/env python3
"""
Generador de claves VAPID para push notifications
"""

import os
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

def generate_vapid_keys():
    """Generar claves VAPID para push notifications"""
    try:
        # Generar clave privada EC P-256
        private_key = ec.generate_private_key(ec.SECP256R1())
        
        # Obtener clave pública
        public_key = private_key.public_key()
        
        # Serializar clave privada en formato PEM
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Serializar clave pública en formato PEM
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        # Convertir a string
        private_key_str = private_pem.decode('utf-8')
        public_key_str = public_pem.decode('utf-8')
        
        print("=" * 60)
        print("🔐 CLAVES VAPID GENERADAS EXITOSAMENTE")
        print("=" * 60)
        print()
        print("CLAVE PRIVADA (Private Key):")
        print(repr(private_key_str))
        print()
        print("CLAVE PÚBLICA (Public Key):")
        print(repr(public_key_str))
        print()
        
        # También generar claves en formato base64 comprimido (para URL)
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
        
        # Base64 URL-safe para la clave pública (formato que espera el frontend)
        public_key_b64 = base64.urlsafe_b64encode(public_bytes).decode('utf-8').rstrip('=')
        
        print("CLAVE PÚBLICA BASE64 (para frontend):")
        print(f"'{public_key_b64}'")
        print()
        print("=" * 60)
        print("IMPORTANTE:")
        print("- Guarda estas claves en un lugar seguro")
        print("- Actualiza las claves en main.py (VAPID_PRIVATE_KEY y VAPID_PUBLIC_KEY)")
        print("- La clave privada NUNCA debe ser compartida")
        print("- Usa la clave pública BASE64 para el frontend")
        print("=" * 60)
        
        return private_key_str, public_key_b64
        
    except Exception as e:
        print(f"❌ Error generando claves VAPID: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    generate_vapid_keys()
