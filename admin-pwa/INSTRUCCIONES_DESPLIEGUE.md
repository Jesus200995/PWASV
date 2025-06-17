# Script de Despliegue - Backend con Endpoints de Usuarios
# INSTRUCCIONES PARA DESPLEGAR EN EL SERVIDOR REMOTO

## 🎯 Lo que necesitas hacer:

### 1. Subir el archivo main.py actualizado
Copia el archivo `backend/main.py` (que tiene los nuevos endpoints GET) a tu servidor donde está corriendo `apipwa.sembrandodatos.com`

### 2. Instalar dependencias en el servidor remoto
```bash
pip install passlib python-jose
```

### 3. Reiniciar el servidor
```bash
# Detener el proceso actual (si está corriendo)
pkill -f "python.*main.py"

# Iniciar el servidor actualizado
cd /ruta/al/backend
python main.py
```

## 🔍 Para verificar que funciona:

### Probar los nuevos endpoints:
```bash
# Probar GET usuarios
curl https://apipwa.sembrandodatos.com/usuarios

# Probar GET usuario específico
curl https://apipwa.sembrandodatos.com/usuarios/1
```

## 📋 Endpoints que se agregan:

- **GET /usuarios** → Obtiene todos los usuarios de la base de datos
- **GET /usuarios/{id}** → Obtiene un usuario específico por ID

## ⚠️ IMPORTANTE:
Una vez que subas y reinicies el servidor remoto:
1. El frontend ya está configurado para usar `https://apipwa.sembrandodatos.com`
2. Los datos aparecerán automáticamente en `adminpwa.sembrandodatos.com`
3. Ya no necesitarás correr Python localmente

## 🎉 Resultado Final:
- Panel admin funcionará 100% en línea
- Datos reales de la base de datos PostgreSQL
- Sin dependencia de servidor local
