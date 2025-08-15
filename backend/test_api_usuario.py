import requests
import json

try:
    # Probar el endpoint de usuarios
    response = requests.get("http://localhost:8000/usuarios/142", 
                          headers={"Content-Type": "application/json"},
                          timeout=5)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Datos del usuario:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"Error: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ No se pudo conectar al servidor. Asegúrate de que el backend esté ejecutándose en http://localhost:8000")
except Exception as e:
    print(f"❌ Error: {e}")
