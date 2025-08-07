# 🚀 INSTRUCCIONES DE DESPLIEGUE - TÉRMINOS Y CONDICIONES EN PRODUCCIÓN

**Fecha:** 7 de agosto de 2025  
**Sistema:** PWASuper - Aviso de Privacidad y Términos  
**Servidor:** https://apipwa.sembrandodatos.com  

## ⚠️ IMPORTANTE - LEER ANTES DE PROCEDER

Este despliegue implementa la funcionalidad de **términos y condiciones obligatorios** en el registro de usuarios. **TODOS los nuevos usuarios** que se registren tendrán sus términos aceptados automáticamente.

---

## 📋 PASOS DE DESPLIEGUE

### PASO 1: Backup de Seguridad

```bash
# En el servidor de producción
cd /path/to/backend
cp main.py main_backup_$(date +%Y%m%d_%H%M%S).py
echo "✅ Backup creado"
```

### PASO 2: Subir Nuevo Código

**Archivo a subir:** `main_produccion_completo.py`  
**Destino:** Reemplazar el `main.py` actual en producción

```bash
# Copiar el contenido de main_produccion_completo.py al servidor
# y guardarlo como main.py
```

### PASO 3: Verificar Dependencias

Asegurarse que estas librerías estén instaladas en producción:

```bash
pip install fastapi uvicorn psycopg2-binary python-jose passlib bcrypt pytz
```

### PASO 4: Reiniciar el Servicio

```bash
# Método depende de cómo esté configurado el servidor
# Ejemplos comunes:

# Si usa systemd:
sudo systemctl restart fastapi-backend

# Si usa pm2:
pm2 restart backend

# Si es manual:
pkill -f "python.*main.py"
python main.py &
```

### PASO 5: Verificar Despliegue

Ejecutar el script de verificación:

```bash
python test_completo_terminos.py
```

**Resultados esperados:**
- ✅ Endpoint `/test/terminos` responde correctamente
- ✅ Creación de usuarios incluye términos automáticamente  
- ✅ Endpoints `/usuarios/{id}/terminos` y `/usuarios/aceptar_terminos` funcionan

---

## 🆕 NUEVOS ENDPOINTS AÑADIDOS

### 1. Verificar Términos de Usuario
```
GET /usuarios/{user_id}/terminos
```
**Respuesta:**
```json
{
  "usuario_id": 123,
  "ha_aceptado_terminos": true,
  "fecha_aceptacion": "2025-08-07T15:30:00"
}
```

### 2. Aceptar Términos Manualmente
```
POST /usuarios/aceptar_terminos
Content-Type: application/json

{
  "usuario_id": 123
}
```

### 3. Endpoint de Prueba
```
GET /test/terminos
```

---

## 🔧 MODIFICACIONES EN ENDPOINTS EXISTENTES

### Endpoint `/usuarios` (POST)

**ANTES:**
```json
{
  "id": 123,
  "mensaje": "Usuario creado exitosamente",
  "curp": "ABCD123456HDFABC01"
}
```

**DESPUÉS:**
```json
{
  "id": 123,
  "mensaje": "Usuario creado exitosamente con términos aceptados automáticamente",
  "curp": "ABCD123456HDFABC01",
  "terminos_registrados": true
}
```

---

## 🗄️ ESTRUCTURA DE BASE DE DATOS

La tabla `usuarios_terminos` ya existe en el VPS con esta estructura:

```sql
CREATE TABLE usuarios_terminos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    aceptado BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_aceptado TIMESTAMP NOT NULL DEFAULT NOW(),
    ip_aceptado VARCHAR(50)
);
```

**No se necesita modificar la base de datos.**

---

## 🔍 VERIFICACIONES POST-DESPLIEGUE

### 1. Test Manual de Funcionalidad

```bash
# Test 1: Endpoint de prueba
curl -X GET "https://apipwa.sembrandodatos.com/test/terminos"

# Test 2: Crear usuario nuevo
curl -X POST "https://apipwa.sembrandodatos.com/usuarios" \
  -H "Content-Type: application/json" \
  -d '{
    "correo": "test@example.com",
    "nombre_completo": "Test User",
    "cargo": "Tester",
    "contrasena": "123456",
    "curp": "ABCD123456HDFABC01"
  }'

# Test 3: Verificar términos del usuario creado
curl -X GET "https://apipwa.sembrandodatos.com/usuarios/{ID_USUARIO}/terminos"
```

### 2. Verificar Usuarios Existentes

Todos los usuarios existentes (9 usuarios) ya tienen términos aceptados desde pruebas anteriores.

### 3. Probar Registro Completo

Usar la aplicación PWASuper para registrar un usuario nuevo y verificar que:
- ✅ El aviso de privacidad se muestra correctamente
- ✅ El checkbox es obligatorio
- ✅ El usuario se crea exitosamente
- ✅ Los términos se registran automáticamente

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### Problema: Error 404 en endpoints de términos
**Solución:** El backend no se actualizó correctamente. Verificar que `main.py` contiene los nuevos endpoints.

### Problema: Error de conexión a base de datos
**Solución:** Verificar credenciales de PostgreSQL en el código.

### Problema: Usuarios sin términos
**Solución:** Ejecutar script de corrección (ya ejecutado previamente).

### Problema: Frontend no encuentra endpoints
**Solución:** Limpiar caché del navegador y verificar URL de API.

---

## ✅ CHECKLIST DE DESPLIEGUE

- [ ] Backup del código actual realizado
- [ ] Nuevo código subido al servidor
- [ ] Servicio backend reiniciado
- [ ] Endpoint `/test/terminos` responde correctamente
- [ ] Creación de usuarios funciona con términos automáticos
- [ ] Verificación de términos funciona
- [ ] Aceptación manual de términos funciona
- [ ] Frontend puede registrar usuarios nuevos
- [ ] No hay errores en logs del servidor

---

## 📞 CONTACTO TÉCNICO

Si surgen problemas durante el despliegue, revisar:

1. **Logs del servidor backend**
2. **Conexión a base de datos PostgreSQL**
3. **Permisos de archivos**
4. **Dependencias de Python instaladas**

---

**🎯 RESULTADO ESPERADO:** Después del despliegue, todos los usuarios nuevos que se registren en PWASuper tendrán automáticamente sus términos y condiciones aceptados, cumpliendo con los requisitos legales del aviso de privacidad.

---

*Creado por: Sistema de Implementación PWA*  
*Fecha: 7 de agosto de 2025*
