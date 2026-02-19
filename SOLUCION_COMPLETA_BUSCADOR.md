# 🎯 SOLUCIÓN COMPLETA AL PROBLEMA DEL BUSCADOR

## 📋 RESUMEN DEL PROBLEMA
El buscador en `/registros` no encuentra usuarios al buscar por CURP (ej: ROCR820619MSLJSB05).

## ✅ CAUSA IDENTIFICADA
El endpoint `/usuarios/buscar` en el backend de producción probablemente usa AND en vez de OR, lo que requiere que TODOS los campos coincidan en vez de CUALQUIERA.

## 🛠️ SOLUCIÓN IMPLEMENTADA

### 1. ✅ Backend Local ARREGLADO
Ya está solucionado en tu copia local:
- **Archivo**: `backend/main.py` línea 6436
- **Cambio**: `WHERE {' OR '.join(condiciones)}` (antes era AND)

### 2. ✅ Frontend con Logging Detallado
El frontend ya tiene logging extenso que muestra cada paso.

### 3. ✅ Página de Debug Creada
Nueva página para diagnosticar problemas: `/debug-buscador`

### 4. ✅ Script de Despliegue Automático
Script para subir los cambios al servidor: `backend/desplegar_backend_auto.py`

---

## 🚀 PASOS PARA SOLUCIONAR

### PASO 1: Probar Localmente (Opcional)

Si quieres verificar primero localmente:

```bash
# Terminal 1: Iniciar backend local
cd backend
python main.py

# Terminal 2: Iniciar frontend
cd admin-pwa
npm run dev
```

Luego ve a: `http://localhost:5173/#/debug-buscador`

### PASO 2: Desplegar al Servidor

```bash
cd backend

# Opción A: Script automático (RECOMENDADO)
pip install paramiko
python desplegar_backend_auto.py

# Opción B: Manual (si el script falla)
# Ver instrucciones en GUIA_DEBUG_BUSCADOR_COMPLETO.md
```

El script automático:
1. ✅ Se conecta al servidor
2. ✅ Encuentra el archivo main.py
3. ✅ Crea un backup automático
4. ✅ Sube el archivo arreglado
5. ✅ Reinicia el servicio
6. ✅ Verifica que esté corriendo

### PASO 3: Probar en Producción

1. Ve a tu admin-pwa desplegado (o local apuntando a producción)
2. Navega a: `#/debug-buscador`
3. Ingresa la CURP: `ROCR820619MSLJSB05`
4. Click en "🔍 Buscar"
5. Observa el log en la parte inferior

#### ✅ Si funciona correctamente:
```
✅ Total usuarios únicos encontrados: 1
👤 Usuario: [Nombre] | CURP: ROCR820619MSLJSB05
✅ Registros recibidos: [N] de [N]
```

#### ❌ Si NO encuentra usuarios:
- Verifica que esa CURP exista en la BD
- Usa la opción "🔍 Verificar Endpoint OR"
- Si dice que usa AND, el despliegue no funcionó

### PASO 4: Verificar en la Vista Normal

Una vez que funcione en `/debug-buscador`, prueba en `/registros`:

1. Ve a Registros
2. En el buscador escribe: `ROCR820619MSLJSB05`
3. Espera 500ms (debounce)
4. Deberías ver los registros del usuario

---

## 🔍 DIAGNÓSTICO RÁPIDO

### Si NO aparece ningún usuario:

```bash
# Conectarse al servidor
ssh root@31.97.8.51

# Verificar que el archivo tenga el cambio
grep -n "OR.*join.*condiciones" /ruta/al/backend/main.py

# Debería mostrar algo como:
# 6436:    WHERE {' OR '.join(condiciones)}
```

### Si encuentra el usuario pero NO tiene registros:

Es normal. Ese usuario no ha registrado actividades. Prueba con otro usuario.

### Si da error de token:

Refresca la página para renovar el token de sesión.

---

## 📁 ARCHIVOS CREADOS

1. **`admin-pwa/src/views/DebugBuscadorView.vue`**
   - Página de debugging completa
   - Ruta: `/#/debug-buscador`

2. **`backend/desplegar_backend_auto.py`**
   - Script de despliegue automático
   - Uso: `python desplegar_backend_auto.py`

3. **`GUIA_DEBUG_BUSCADOR_COMPLETO.md`**  
   - Guía detallada de uso

4. **`backend/test_buscar_produccion.py`**
   - Script de prueba contra producción
   - Requiere credenciales admin

---

## 🎓 CÓMO USAR LA PÁGINA DE DEBUG

### Interfaz de Usuario:

```
┌─────────────────────────────────────────┐
│ 🔍 Debug del Buscador de Registros      │
├─────────────────────────────────────────┤
│ 1️⃣ Autenticación                        │
│    ✅ Token encontrado: eyJ...          │
├─────────────────────────────────────────┤
│ 2️⃣ Buscar Usuario                       │
│    [ROCR820619MSLJSB05] [🔍 Buscar]    │
│                                         │
│    📊 Resultado:                         │
│    👥 Usuarios encontrados: 1           │
│    ┌─────────────────────────────────┐ │
│    │ ID: 123                         │ │
│    │ Nombre: Juan Pérez              │ │
│    │ CURP: ROCR820619MSLJSB05        │ │
│    │ [📥 Cargar registros]           │ │
│    └─────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ 3️⃣ Cargar Registros                     │
│    Total: 45 registros                  │
│    Primeros 5 registros...              │
├─────────────────────────────────────────┤
│ 4️⃣ Verificar Backend                    │
│    [🔍 Verificar Endpoint OR]           │
│    ✅ El backend usa OR correctamente   │
├─────────────────────────────────────────┤
│ 📝 Registro de Actividad                │
│ ┌───────────────────────────────────┐  │
│ │ 14:35:22 🔍 Buscando: "ROCR82..."  │  │
│ │ 14:35:22 📡 GET /usuarios/buscar   │  │
│ │ 14:35:23 ✅ Respuesta: 1 usuarios  │  │
│ │ 14:35:23 📥 Cargando registros...  │  │
│ │ 14:35:24 ✅ 45 registros recibidos │  │
│ └───────────────────────────────────┘  │
│ [🗑️ Limpiar Log]                        │
└─────────────────────────────────────────┘
```

---

## ⚡ COMANDO RÁPIDO TODO EN UNO

```bash
# Desde la raíz del proyecto:
cd backend && pip install paramiko && python desplegar_backend_auto.py
```

Luego abre: `tu-admin-url/#/debug-buscador`

---

## 🆘 TROUBLESHOOTING

### Error: "paramiko not found"
```bash
pip install paramiko
```

### Error: "no se encuentra main.py"
```bash
# Asegúrate de estar en la carpeta backend
cd backend
pwd  # Debe mostrar: .../PWA/PWASV/backend
```

### Error: "Connection refused"
Verifica que puedes conectarte por SSH:
```bash
ssh root@31.97.8.51
```

### El backend no reinicia automáticamente
Conéctate manualmente y reinicia:
```bash
ssh root@31.97.8.51
# Luego uno de estos:
systemctl restart pwa-backend
# o
pm2 restart all
# o
supervisorctl restart pwa-backend
```

---

## ✅ VERIFICACIÓN FINAL

Después de desplegar, verifica estos 3 puntos:

### 1. Backend actualizado
```bash
ssh root@31.97.8.51 'grep "OR.*join" /ruta/al/main.py'
# Debe mostrar: WHERE {' OR '.join(condiciones)}
```

### 2. Backend corriendo
```bash
ssh root@31.97.8.51 'ps aux | grep uvicorn'
# Debe mostrar el proceso activo
```

### 3. API responde correctamente
En `/debug-buscador`:
- Click en "🔍 Verificar Endpoint OR"
- Debe decir: ✅ El backend parece usar OR correctamente

---

## 📞 APOYO

Si después de seguir estos pasos sigue sin funcionar:

1. Abre la consola del navegador (F12)
2. Ve a la pestaña "Network"
3. Busca por "ROCR820619MSLJSB05" en `/registros`
4. Click en la petición a `/usuarios/buscar`
5. Revisa la respuesta

O usa la página de debug que muestra todo visualmente.

---

**Última actualización**: 19 de febrero de 2026
**Versión**: 2.0 (con debug integrado)
