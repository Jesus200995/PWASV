# 🚨 INSTRUCCIONES URGENTES PARA ACTUALIZAR SERVIDOR DE PRODUCCIÓN

## PROBLEMA IDENTIFICADO:
El servidor en producción (`https://apipwa.sembrandodatos.com`) NO tiene el código actualizado que requiere CURP.

## ✅ LO QUE YA ESTÁ HECHO:
1. ✅ Columna CURP existe en la base de datos
2. ✅ Código backend actualizado (local)
3. ✅ Código frontend actualizado y compilado

## 🚨 LO QUE FALTA:
**SUBIR EL CÓDIGO ACTUALIZADO AL SERVIDOR DE PRODUCCIÓN**

---

## 📋 PASOS PARA ACTUALIZAR EL SERVIDOR:

### 1. **BACKEND** - Subir main.py actualizado

**Archivo a subir:** `c:\Users\Admin_1\Pictures\PWA\PWASV\backend\main.py`

**Ubicación en servidor:** donde esté el archivo `main.py` del servidor de producción

**Cambios clave en el código:**
- CURP es obligatoria en el modelo `UserCreate`
- Validación de CURP de 18 caracteres
- Validación de formato (solo letras mayúsculas y números)
- Verificación de CURP duplicada

### 2. **FRONTEND** - Subir archivos compilados

**Archivos a subir:** todo el contenido de `c:\Users\Admin_1\Pictures\PWA\PWASV\pwasuper\dist\`

**Ubicación en servidor:** directorio web público del servidor

### 3. **REINICIAR SERVICIOS**

Después de subir los archivos:
```bash
# Reiniciar el servidor backend (FastAPI/Python)
# El comando exacto depende de cómo esté configurado el servidor
```

---

## 🧪 VERIFICACIÓN POST-DESPLIEGUE:

Una vez actualizado el servidor, ejecutar estas pruebas:

### Prueba 1: Registro CON CURP (debe funcionar)
```bash
curl -X POST "https://apipwa.sembrandodatos.com/usuarios" \
  -H "Content-Type: application/json" \
  -d '{
    "correo": "test@ejemplo.com",
    "nombre_completo": "Test User", 
    "cargo": "Tester",
    "contrasena": "123456",
    "curp": "ABCD123456HEFGHIJ01"
  }'
```
**Resultado esperado:** Status 200, usuario creado

### Prueba 2: Registro SIN CURP (debe fallar)
```bash
curl -X POST "https://apipwa.sembrandodatos.com/usuarios" \
  -H "Content-Type: application/json" \
  -d '{
    "correo": "test2@ejemplo.com",
    "nombre_completo": "Test User 2",
    "cargo": "Tester", 
    "contrasena": "123456"
  }'
```
**Resultado esperado:** Status 400, error "La CURP es obligatoria"

### Prueba 3: CURP inválida (debe fallar)
```bash
curl -X POST "https://apipwa.sembrandodatos.com/usuarios" \
  -H "Content-Type: application/json" \
  -d '{
    "correo": "test3@ejemplo.com",
    "nombre_completo": "Test User 3",
    "cargo": "Tester",
    "contrasena": "123456", 
    "curp": "ABC123"
  }'
```
**Resultado esperado:** Status 400, error "La CURP debe tener exactamente 18 caracteres"

---

## 📁 ARCHIVOS CLAVE A SUBIR:

### Backend:
- `backend/main.py` (PRINCIPAL - contiene todas las validaciones)

### Frontend:
- `pwasuper/dist/index.html`
- `pwasuper/dist/assets/` (toda la carpeta)
- `pwasuper/dist/manifest.webmanifest`
- `pwasuper/dist/registerSW.js`
- `pwasuper/dist/sw.js`
- `pwasuper/dist/workbox-*.js`

---

## ⚡ ACCIÓN INMEDIATA REQUERIDA:

1. **Subir `main.py` al servidor de producción**
2. **Reiniciar el servicio backend**
3. **Subir archivos del `dist/` al directorio web**
4. **Probar con las URLs de verificación**

Una vez hecho esto, el sistema funcionará con CURP obligatoria como se requiere.

---

## 📞 SI HAY PROBLEMAS:

- Verificar logs del servidor para errores
- Asegurar que el servidor use Python con las librerías necesarias
- Verificar que la base de datos tenga la columna CURP (ya confirmado ✅)

**URGENTE: Sin este despliegue, el sistema seguirá sin requerir CURP.**
