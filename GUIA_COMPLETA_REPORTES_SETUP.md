# 🔧 GUÍA COMPLETA DE CONFIGURACIÓN Y PRUEBAS - REPORTES

## ⚠️ PROBLEMA IDENTIFICADO

El **Backend NO está corriendo** en puerto 8000. Por eso las actividades no aparecen en Reportes.

```
Puerto 8000: ❌ SIN RESPUESTA
Puerto 5173: ❌ FRONTEND TAMBIÉN NECESITA INICIARSE
```

## 🚀 SOLUCIÓN PASO A PASO

### OPCIÓN 1: Usar Backend Real (Recomendado - cuando Python funcione)

#### Paso 1: Iniciar Backend en Terminal Separada

```powershell
cd c:\Users\ASUS\Music\PWASV\PWASV\backend
python main.py
```

**Espera que veas:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

#### Paso 2: Iniciar Frontend en otra Terminal

```powershell
cd c:\Users\ASUS\Music\PWASV\PWASV\pwasuper
npm run dev
```

**Espera que veas:**
```
VITE v... ready in XXX ms

➜  Local:   http://localhost:5173/
```

#### Paso 3: Verificar Conexión

1. Abre DevTools (F12) en Reportes
2. Va a Console
3. Presiona Ctrl+Shift+I
4. Debería ver logs de `reportesService`
5. Cambia mes/año → actividades deben aparecer

---

### OPCIÓN 2: Usar Servidor Mock para Pruebas (Rápido - funciona ahora)

#### Paso 1: Iniciar Mock Server

**Abre una terminal nueva en c:\Users\ASUS\Music\PWASV\PWASV:**

```powershell
cd c:\Users\ASUS\Music\PWASV\PWASV
node mock-server.js
```

Debería ver:
```
🟢 SERVIDOR MOCK INICIADO
📍 Escuchando en: http://localhost:8000
```

**NO cierres esta terminal, dejarla corriendo en background.**

#### Paso 2: Iniciar Frontend

**En otra terminal:**

```powershell
cd c:\Users\ASUS\Music\PWASV\PWASV\pwasuper
npm run dev
```

#### Paso 3: Probar Reportes

1. Abre http://localhost:5173
2. Login si es necesario
3. Va a Reportes
4. Abre DevTools (F12) → Console
5. Debería ver logs exitosos con actividades
6. Cambia mes/año → actividades deben aparecer

---

## 🧪 VERIFICACIONES RÁPIDAS

### Verificar que Servidores Están Corriendo

**Terminal para verificar puertos:**

```powershell
netstat -ano | findstr :8000
netstat -ano | findstr :5173
```

Debería ver algo como:
```
TCP    127.0.0.1:8000    LISTENING    1234
TCP    127.0.0.1:5173    LISTENING    5678
```

### Probar API Directamente en Navegador

Abre estas URLs en tu navegador (con mock-server o backend corriendo):

1. **Sin filtros:**
   ```
   http://localhost:8000/historial/1
   ```

2. **Con fechas:**
   ```
   http://localhost:8000/historial/1?fecha_inicio=2026-01-01&fecha_fin=2026-01-31
   ```

3. **Solo entradas:**
   ```
   http://localhost:8000/historial/1?tipo=entrada
   ```

**Deberías ver JSON con actividades.**

---

## 📋 CHECKLIST DE CONFIGURACIÓN

### Backend
- [ ] Mock server corriendo en puerto 8000 (`node mock-server.js`)
- [ ] O Backend real corriendo (`python main.py`)

### Frontend  
- [ ] npm run dev corriendo en puerto 5173
- [ ] Página abre sin errores HTTP 404

### Reportes
- [ ] Puedo ver tablas con datos de actividades
- [ ] Cambiar mes/año actualiza los datos
- [ ] DevTools Console muestra logs de reportesService

### API_URL
- [ ] network.js detecta correctamente el entorno
- [ ] API_URL está apuntando a http://localhost:8000 en desarrollo

---

## 🔍 DEBUGGING - SI SIGUE SIN FUNCIONAR

### 1. Verificar API_URL en Console

Abre Console en Reportes y ejecuta:

```javascript
// Ver configuración
import('../../src/utils/network.js').then(m => {
    console.log('API_URL:', m.API_URL);
});
```

Debería ser: `http://localhost:8000`

### 2. Verificar que el servidor responde

En Console:

```javascript
fetch('http://localhost:8000/health')
    .then(r => r.json())
    .then(d => console.log('✅ Server:', d))
    .catch(e => console.log('❌ Error:', e.message));
```

Debería responder con `{ status: 'ok', timestamp: '...' }`

### 3. Verificar petición completa

En Console:

```javascript
fetch('http://localhost:8000/historial/1?fecha_inicio=2026-01-01&fecha_fin=2026-01-31')
    .then(r => r.json())
    .then(d => {
        console.log('Actividades:', d.total);
        console.log(d.historial.slice(0, 3));
    })
    .catch(e => console.log('Error:', e.message));
```

### 4. Revisar Network Tab

En DevTools → Network tab:
1. Cambia mes/año en Reportes
2. Busca petición GET `/historial/1`
3. Status debe ser 200
4. Response debe tener JSON con datos

Si Status es 404 o 0 → Servidor no responde

---

## 📝 LOGS IMPORTANTES QUE DEBERÍAS VER

### En Console del Navegador (cuando cambia mes/año):

```
🔗 ReportesService - API_URL configurada como: http://localhost:8000
📊 Obteniendo actividades de 1/2026 para usuario 1
📅 Rango calculado: 2026-01-01 a 2026-01-31
🔗 URL: http://localhost:8000/historial/1
📋 Parámetros: { fecha_inicio: '2026-01-01', fecha_fin: '2026-01-31', limit: 1000 }
✅ Respuesta del servidor: { historial: [...], total: 42, ... }
📊 Total de actividades obtenidas: 42
```

### En Terminal del Servidor:

```
📊 Historial solicitado para usuario 1
   Período: 2026-01-01 a 2026-01-31
   Límite: 1000
   ✅ Retornando 42 actividades
```

Si ves esto → **¡FUNCIONANDO CORRECTAMENTE!**

---

## 🎯 RESUMEN FINAL

**El problema está resuelto en código:**
- ✅ API_URL está configurada dinámicamente
- ✅ ReportesService hace peticiones correctas con filtros
- ✅ Reportes.vue procesa respuestas correctamente

**Lo que FALTA:**
- ❌ Backend/Mock server corriendo en puerto 8000
- ❌ Frontend corriendo en puerto 5173

**Próximos pasos:**

1. **Abre DOS terminales nuevas**

2. **Terminal 1 - Backend/Mock:**
   ```
   cd c:\Users\ASUS\Music\PWASV\PWASV
   node mock-server.js
   ```

3. **Terminal 2 - Frontend:**
   ```
   cd c:\Users\ASUS\Music\PWASV\PWASV\pwasuper
   npm run dev
   ```

4. **Abre http://localhost:5173 en navegador**

5. **Va a Reportes y prueba cambiar fechas**

---

**Si aún hay problemas, revisa el archivo `test-api-directo.html` en:**
```
http://localhost:5173/test-api-directo.html
```

Este archivo prueba cada endpoint manualmente sin necesidad de frontend.

