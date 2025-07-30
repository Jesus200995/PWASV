# Instrucciones para Desplegar los Cambios de Contraseñas

## Resumen de Cambios Realizados

### 1. Backend - Endpoints Agregados/Modificados:

1. **`GET /usuarios`** - Ahora incluye contraseñas
2. **`GET /usuarios/exportacion-completa`** - Nuevo endpoint para exportación completa con contraseñas
3. **`GET /usuarios/{user_id}`** - Ahora incluye contraseñas

### 2. Frontend - Cambios Realizados:

1. **`usuariosService.js`** - Configuración flexible para cambiar entre APIs
2. **`UsuariosView.vue`** - Función `obtenerContrasenaUsuario` para mostrar contraseñas
3. **Modal de detalles** - Ahora muestra contraseñas con botón de mostrar/ocultar

## Pasos para Desplegar en Producción

### Paso 1: Subir el Backend Actualizado

El archivo `main_para_servidor.py` debe subirse al servidor de producción `https://apipwa.sembrandodatos.com`.

#### Cambios específicos en main_para_servidor.py:

**Endpoint GET /usuarios (líneas 268-305):**
```python
@app.get("/usuarios")
async def obtener_usuarios():
    # ... incluye "contrasena" en el SELECT y en el diccionario de respuesta
```

**Endpoint GET /usuarios/exportacion-completa (líneas 307-349):**
```python
@app.get("/usuarios/exportacion-completa")
async def obtener_usuarios_exportacion_completa():
    # ... nuevo endpoint para exportación completa con contraseñas
```

**Endpoint GET /usuarios/{user_id} (líneas 350-392):**
```python
@app.get("/usuarios/{user_id}")
async def obtener_usuario(user_id: int):
    # ... incluye "contrasena" en el SELECT y en el diccionario de respuesta
```

### Paso 2: Reiniciar el Servidor de Producción

Después de subir el archivo, reiniciar el servicio FastAPI en el servidor de producción.

### Paso 3: Verificar que Funciona

1. Probar el endpoint: `GET https://apipwa.sembrandodatos.com/usuarios`
2. Verificar que la respuesta incluya el campo `contrasena` para cada usuario
3. Probar el frontend en la aplicación web

## Comandos de Verificación

```bash
# Probar endpoint de usuarios
curl https://apipwa.sembrandodatos.com/usuarios

# Probar endpoint individual
curl https://apipwa.sembrandodatos.com/usuarios/1

# Probar endpoint de exportación
curl https://apipwa.sembrandodatos.com/usuarios/exportacion-completa
```

## Estado Actual

✅ Backend local (localhost:8000) - FUNCIONANDO
✅ Frontend configurado para producción - LISTO
⏳ Backend producción - PENDIENTE DESPLIEGUE

Una vez desplegado el backend de producción, la funcionalidad de mostrar contraseñas funcionará completamente.
