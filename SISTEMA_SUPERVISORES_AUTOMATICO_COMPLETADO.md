# 📋 SISTEMA DE ACTUALIZACIÓN AUTOMÁTICA DE SUPERVISORES PARA TÉCNICOS

## 🎯 Objetivo
Garantizar que todos los técnicos (TECNICO SOCIAL y TECNICO PRODUCTIVO) tengan automáticamente asignado el supervisor correcto según su territorio, tanto en nuevos registros como en usuarios existentes.

---

## ✅ Implementaciones Completadas

### 1️⃣ Backend - Endpoint de Actualización Masiva
📁 `backend/main.py` - Línea ~6790

**Nuevo Endpoint:**
```python
POST /actualizar-supervisores-tecnicos
```

**Funcionalidad:**
- Busca TODOS los técnicos en la base de datos
- Para cada técnico, encuentra su supervisor territorial según su territorio
- Actualiza el campo `supervisor` en la tabla `usuarios`
- Retorna estadísticas completas del proceso

**Respuesta:**
```json
{
  "success": true,
  "total_tecnicos": 150,
  "actualizados": 145,
  "sin_supervisor": 5,
  "errores": [...],
  "mensaje": "Se actualizaron 145 de 150 técnicos"
}
```

---

### 2️⃣ Script Python de Actualización
📁 `backend/actualizar_supervisores_tecnicos.py`

**Uso:**
```bash
python actualizar_supervisores_tecnicos.py
```

**Características:**
- Llama al endpoint `/actualizar-supervisores-tecnicos`
- Muestra estadísticas detalladas
- Lista errores si existen
- Timeout de 60 segundos

---

### 3️⃣ Script BAT para Windows
📁 `backend/ACTUALIZAR_SUPERVISORES.bat`

**Uso:**
```cmd
ACTUALIZAR_SUPERVISORES.bat
```

**Ventajas:**
- Doble clic para ejecutar
- Mensaje de confirmación
- Pausa al finalizar para ver resultados

---

### 4️⃣ Frontend PWA - Actualización Automática Continua
📁 `pwasuper/src/App.vue`

**Implementación:**

#### Al Iniciar Sesión (onMounted)
```javascript
// Línea ~257
if (tiene cargo y territorio) {
  actualizarSupervisorAutomatico(userData.value);
}
```

#### Al Cambiar Territorio
```javascript
// Línea ~198
if (territorio cambió && es técnico) {
  await actualizarSupervisorAutomatico(userData.value);
}
```

#### Verificación Periódica (cada 15 segundos)
```javascript
// Línea ~136 - checkUserDataFromServer()
// Compara supervisor local vs servidor
// Actualiza automáticamente si hay diferencia
```

---

### 5️⃣ Frontend PWA - Register.vue
📁 `pwasuper/src/views/Register.vue`

**Watchers Implementados:**
```javascript
// Al cambiar territorio → busca supervisor automático
watch(() => form.territorio, ...)

// Al cambiar cargo → busca supervisor si es técnico
watch(() => form.cargo, ...)
```

**Validación:**
- Supervisor obligatorio solo para NO técnicos
- Técnicos tienen supervisor readonly con fondo gris
- Texto informativo verde: "✅ Supervisor asignado automáticamente"

---

### 6️⃣ Frontend PWA - Profile.vue
📁 `pwasuper/src/views/Profile.vue`

**Después de guardar perfil:**
```javascript
if (es técnico) {
  obtenerSupervisorAutomatico();
  // Actualiza en BD y localStorage
}
```

---

## 🚀 Cómo Usar

### Para Actualizar TODOS los Técnicos Existentes (AHORA)

#### Opción 1: Script BAT (Windows - Recomendado)
```cmd
cd C:\Users\Admin_1\Pictures\PWA\PWASV\backend
ACTUALIZAR_SUPERVISORES.bat
```

#### Opción 2: Python Directo
```bash
cd backend
python actualizar_supervisores_tecnicos.py
```

#### Opción 3: Curl/Postman
```bash
curl -X POST http://31.97.8.51:8080/actualizar-supervisores-tecnicos
```

---

### Para Actualización Automática Continua

**Ya está funcionando automáticamente:**

1. ✅ Al registrar nuevo usuario técnico
2. ✅ Al cambiar territorio de un técnico
3. ✅ Al iniciar sesión (verifica y actualiza si cambió)
4. ✅ Cada 15 segundos (verificación en background)
5. ✅ Al guardar perfil

**No requiere acción manual.**

---

## 📊 Flujo de Actualización Automática

```
┌─────────────────────────────────────────────────────┐
│  TÉCNICO CAMBIA TERRITORIO                          │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  Watcher detecta cambio en form.territorio          │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  Llama a buscarSupervisorPorTerritorio()            │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  Backend busca admin territorial en admin_users     │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  Actualiza supervisor en usuarios (BD)             │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  Actualiza localStorage del usuario                 │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  Campo supervisor se actualiza en UI (readonly)     │
└─────────────────────────────────────────────────────┘
```

---

## 🔍 Verificación

### Verificar en Base de Datos
```sql
-- Ver técnicos y sus supervisores
SELECT 
  id,
  nombre_completo,
  cargo,
  territorio,
  supervisor
FROM usuarios
WHERE cargo IN ('TECNICO SOCIAL', 'TECNICO PRODUCTIVO')
ORDER BY territorio;

-- Contar técnicos actualizados
SELECT 
  territorio,
  COUNT(*) as total_tecnicos,
  COUNT(supervisor) as con_supervisor
FROM usuarios
WHERE cargo IN ('TECNICO SOCIAL', 'TECNICO PRODUCTIVO')
GROUP BY territorio;
```

### Verificar en Admin Panel
1. Ir a admin-pwa
2. Vista Usuarios
3. Filtrar por cargo "TECNICO SOCIAL" o "TECNICO PRODUCTIVO"
4. Verificar columna "Supervisor"

---

## ⚙️ Configuración Backend

### Endpoint Individual (ya existía)
```python
GET /usuarios/{user_id}/supervisor-automatico
```
- Actualiza supervisor de UN usuario específico
- Usado por Profile.vue y App.vue

### Endpoint Masivo (NUEVO)
```python
POST /actualizar-supervisores-tecnicos
```
- Actualiza supervisores de TODOS los técnicos
- Usado para migración o corrección masiva

---

## 📝 Logs y Depuración

### Backend
```python
# Ver logs en consola del backend
🔍 Buscando supervisor automático para usuario ID: 123
✅ Supervisor actualizado en BD: MARÍA GARCÍA LÓPEZ
⚠️ No hay administrador territorial para: Territorio X
```

### Frontend
```javascript
// Ver en consola del navegador (F12)
🔄 Territorio cambió, actualizando supervisor automático...
✅ Supervisor automático actualizado: MARÍA GARCÍA LÓPEZ
ℹ️ No se encontró supervisor automático: Sin territorio
```

---

## 🛠️ Mantenimiento

### Agregar Nuevo Administrador Territorial
1. Ir a admin-pwa
2. Crear/editar usuario en admin_users
3. Marcar `es_territorial = TRUE`
4. Asignar territorio
5. Los técnicos se actualizarán automáticamente en su próxima sesión

### Cambiar Territorio de Admin Territorial
1. Actualizar territorio en admin_users
2. Ejecutar script de actualización masiva:
   ```bash
   ACTUALIZAR_SUPERVISORES.bat
   ```

---

## 📌 Notas Importantes

1. **Solo afecta a técnicos:** TECNICO SOCIAL y TECNICO PRODUCTIVO
2. **Otros cargos:** Escriben supervisor manualmente
3. **Sin territorio:** Supervisor permanece vacío hasta asignar territorio
4. **Sin admin territorial:** Se registra en logs, supervisor queda vacío
5. **Actualización en BD:** Se guarda en PostgreSQL, no solo en memoria
6. **Admin-pwa:** Verá los supervisores actualizados inmediatamente

---

## ✅ Checklist de Verificación

- [x] Endpoint `/actualizar-supervisores-tecnicos` creado
- [x] Script Python funcional
- [x] Script BAT para Windows
- [x] App.vue actualiza supervisor al login
- [x] App.vue verifica supervisor cada 15 segundos
- [x] Register.vue asigna supervisor automático
- [x] Profile.vue actualiza supervisor al guardar
- [x] Watchers en territorio y cargo funcionando
- [x] Validación de supervisor omitida para técnicos
- [x] Campo supervisor readonly para técnicos
- [x] Fondo gris en campo supervisor técnicos
- [x] Texto informativo verde mostrándose

---

## 🎉 Resultado Final

**Antes:**
- Técnicos escribían supervisor manualmente
- Supervisores desactualizados
- Inconsistencia entre PWA y Admin

**Ahora:**
- ✅ Supervisores asignados automáticamente
- ✅ Actualización en tiempo real
- ✅ Sincronización PWA ↔ Admin ↔ BD
- ✅ Sin intervención manual necesaria
- ✅ Campo readonly para evitar errores

---

**Fecha:** 27 de enero de 2026  
**Versión:** 1.0  
**Estado:** ✅ Implementación Completa
