# 🚀 INSTRUCCIONES PARA EL ADMINISTRADOR DEL SERVIDOR

## 📋 Problema identificado:
El servidor `https://apipwa.sembrandodatos.com` tiene un error en el endpoint `/registros` que impide cargar el historial de registros.

**Error actual:**
```
"Error al obtener registros: 'cursor_factory' is an invalid keyword argument for this function"
```

## ✅ Solución:
Reemplazar el archivo `main.py` del servidor con el archivo `main_para_servidor.py` que se incluye en esta carpeta.

## 🔧 Cambios principales realizados:

### 1. **Endpoint `/registros` corregido:**
- ❌ **Antes:** Uso incorrecto de `cursor_factory` en `cursor.execute()`
- ✅ **Después:** Uso correcto del cursor sin `cursor_factory` en execute
- ✅ **Mejora:** Conversión manual de tuplas a diccionarios
- ✅ **Mejora:** Mejor manejo de errores y logging

### 2. **Mejor conexión a la base de datos:**
- ✅ Manejo de errores en la conexión inicial
- ✅ Verificación de conexión antes de ejecutar consultas
- ✅ Logging mejorado para debug

### 3. **Datos optimizados:**
- ✅ Conversión correcta de tipos de datos (float, datetime)
- ✅ Manejo de valores nulos
- ✅ Formato JSON serializable

## 📁 Archivos a actualizar en el servidor:

1. **Reemplazar:** `main.py` con el contenido de `main_para_servidor.py`
2. **Mantener:** Todos los demás archivos y configuraciones

## 🧪 Prueba después de la actualización:

Hacer una petición GET a: `https://apipwa.sembrandodatos.com/registros`

**Respuesta esperada:**
```json
{
  "registros": [
    {
      "id": 1,
      "usuario_id": 3,
      "latitud": 19.4318454,
      "longitud": -99.1563216,
      "descripcion": "Ejemplo",
      "foto_url": "fotos/3_20250613220710.png",
      "fecha_hora": "2025-06-13T22:07:10.996226"
    }
  ]
}
```

## ⚠️ Importante:
- **NO cambiar** las credenciales de la base de datos
- **NO modificar** la estructura de las tablas
- **SÍ reiniciar** el servidor después de actualizar el código

## 📞 Verificación:
Una vez actualizado, el historial de registros en la aplicación PWA debería cargar correctamente sin errores 500.

---
*Actualización realizada el 13 de junio de 2025*
