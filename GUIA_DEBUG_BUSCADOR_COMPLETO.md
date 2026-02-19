# 🔍 GUÍA RÁPIDA: DEBUG DEL BUSCADOR

## ✅ SOLUCIÓN IMPLEMENTADA

Se ha creado una página de debugging completa que te permitirá ver exactamente qué está fallando en el buscador.

## 🚀 CÓMO USAR

### 1. Iniciar el admin-pwa

```bash
cd admin-pwa
npm run dev
```

### 2. Acceder a la página de debug

Una vez que el admin-pwa esté corriendo, accede a:

```
http://localhost:5173/#/debug-buscador
```

(O la URL que te muestre vite al iniciar)

### 3. Seguir los pasos en la interfaz

La página de debug te guiará a través de 4 pasos:

1. **Autenticación**: Verifica que tengas una sesión activa
2. **Buscar Usuario**: Ingresa una CURP, nombre o correo para buscar
3. **Cargar Registros**: Carga los registros del usuario encontrado
4. **Verificar Backend**: Verifica que el backend use OR correctamente

### 4. Revisar el log

En la parte inferior verás un registro detallado de:
- Todas las peticiones HTTP que se hacen
- Los parámetros enviados
- Las respuestas recibidas
- Cualquier error que ocurra

## 🔎 QUÉ BUSCAR

### Si NO encuentra usuarios:

1. ✅ Verifica que la CURP exista en la base de datos
2. ✅ Verifica que el campo `curp` no esté NULL en la BD
3. ✅ Verifica que el backend esté usando OR y no AND

### Si encuentra usuarios pero NO tiene registros:

1. ✅ Es normal - ese usuario simplemente no ha registrado actividades
2. ✅ Prueba con otro usuario que sepas que tiene actividades

### Si hay errores de red:

1. ✅ Verifica que el backend esté corriendo
2. ✅ Verifica que la URL del API sea correcta
3. ✅ Verifica que tu token no haya expirado (refresca la página)

## 🛠️ SIGUIENTE PASO: DESPLEGAR AL SERVIDOR

Si el debug muestra que el problema es que el backend usa AND en vez de OR, necesitas:

### 1. Conectarte al servidor

```bash
ssh root@31.97.8.51
```

### 2. Ubicar el archivo main.py

```bash
find /root -name "main.py" -type f | grep -v node_modules
```

Probablemente esté en algo como `/root/backend/main.py` o `/root/app/main.py`

### 3. Editar el endpoint de búsqueda

Busca la línea que tiene `@app.get("/usuarios/buscar")` y asegúrate de que use OR:

```python
# ❌ MAL (con AND)
if condiciones:
    where_clause = f"WHERE {' AND '.join(condiciones)}"

# ✅ BIEN (con OR)
if condiciones:
    where_clause = f"WHERE {' OR '.join(condiciones)}"
```

### 4. Reiniciar el servicio

```bash
# Depende de cómo esté configurado tu servidor
# Puede ser uno de estos:

# Si usa systemd:
systemctl restart pwa-backend

# Si usa pm2:
pm2 restart pwa-backend

# Si usa supervisord:
supervisorctl restart pwa-backend

# Si corre con uvicorn directamente, kill y reiniciar:
pkill -f "uvicorn main:app"
cd /ruta/al/backend
nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
```

## 📝 ARCHIVO DE REFERENCIA

El cambio que necesitas en el backend está en el archivo:
- `backend/main.py` líneas 6395-6470

Ya está modificado en tu copia local, solo falta desplegarlo al servidor.

## 🆘 SI NECESITAS AYUDA

1. Abre el admin-pwa con F12 (DevTools)
2. Ve a la pestaña "Console"
3. Busca por "ROCR820619MSLJSB05"
4. Copia todos los logs y mensajes que veas

El sistema ya tiene logging muy detallado que te dirá exactamente:
- Cuántos registros hay en memoria
- Qué buscan
- Qué encuentran
- Por qué no se muestran

## ✅ VERIFICACIÓN FINAL

Una vez que despliegues el backend, vuelve a la página de debug y:

1. Click en "🔍 Verificar Endpoint OR"
2. Si dice "✅ El backend parece usar OR correctamente", ¡está arreglado!
3. Vuelve a probar en la página de Registros normal

---

**Nota**: La página de debug es solo para diagnosticar. Una vez que todo funcione, seguirás usando la página de Registros normal (`/registros`).
