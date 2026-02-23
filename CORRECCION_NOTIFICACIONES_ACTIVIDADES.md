# ✅ CORRECCIÓN APLICADA: Sistema de Notificaciones sobre Actividades

## Fecha: 23 de febrero de 2026

---

## 🔧 PROBLEMA DETECTADO Y SOLUCIONADO

**Problema**: Al intentar enviar notificaciones desde el botón "Notificar" en RegistrosView.vue, se recibía el error:
```
❌ Error: Actividad con ID 770246 no encontrada
```

**Causa**: La foreign key del campo `actividad_id` en la tabla `notificaciones` estaba apuntando a la tabla incorrecta (`reportes_generados`) cuando debería apuntar a la tabla `registros` que es donde se almacenan las actividades reales.

---

## ✅ SOLUCIÓN APLICADA

### 1. Base de Datos (VPS)
Se ejecutó el siguiente script SQL:

```sql
-- Eliminar la foreign key incorrecta
ALTER TABLE notificaciones 
DROP CONSTRAINT IF EXISTS notificaciones_actividad_id_fkey;

-- Agregar la foreign key correcta apuntando a registros
ALTER TABLE notificaciones 
ADD CONSTRAINT notificaciones_actividad_id_fkey 
FOREIGN KEY (actividad_id) REFERENCES registros(id) ON DELETE SET NULL;
```

**Resultado**: ✅ Foreign key ahora apunta correctamente a `registros.id`

### 2. Backend (main.py)
Se actualizó la validación de `actividad_id` en el endpoint `POST /notificaciones`:

**Antes**:
```python
cursor.execute("SELECT id FROM reportes_generados WHERE id = %s", (actividad_id,))
```

**Después**:
```python
cursor.execute("SELECT id FROM registros WHERE id = %s", (actividad_id,))
```

**Resultado**: ✅ Backend actualizado en VPS (`/var/www/PWASV/backend/main.py`)

---

## 🚀 SIGUIENTE PASO: REINICIAR EL BACKEND

Para que los cambios surtan efecto, **debes reiniciar el backend en el VPS**:

### Opción 1: Si usas systemd
```bash
ssh root@31.97.8.51
systemctl restart pwasv-backend
systemctl status pwasv-backend
```

### Opción 2: Si usas supervisor
```bash
ssh root@31.97.8.51
supervisorctl restart pwasv-backend
supervisorctl status pwasv-backend
```

### Opción 3: Si ejecutas manualmente
```bash
ssh root@31.97.8.51
cd /var/www/PWASV/backend

# Detener proceso actual (buscar PID)
ps aux | grep "python.*main.py"
kill <PID>

# Reiniciar
source venv/bin/activate
nohup python main.py > backend.log 2>&1 &

# Verificar que esté corriendo
ps aux | grep "python.*main.py"
```

---

## 🧪 PRUEBA LA FUNCIONALIDAD

Una vez reiniciado el backend:

1. Ve a **Registros de Actividades** en el admin-pwa
2. Haz clic en el botón naranja **"Notificar"** (🔔) en cualquier registro
3. El modal debería abrirse con la información de la actividad pre-llenada
4. Completa el formulario:
   - Selecciona al menos un motivo de atención
   - Escribe un mensaje en la descripción
5. Haz clic en **"Enviar Notificación"**
6. Deberías ver un mensaje de éxito

### Logs esperados:

**Backend** (consola o archivo de log):
```
📊 Notificación vinculada a actividad (registro) ID: 770246
🔔 Creando notificación: Notificación sobre Campo - 23/02/2026
⚠️ Motivos de atención: ['correccion_requerida', 'informacion_faltante']
```

**Frontend** (consola del navegador):
```
🔔 Abriendo modal para notificar sobre actividad: {id: 770246, usuario_id: 1198, ...}
📤 Enviando notificación: {titulo: "...", actividad_id: 770246, ...}
✅ Notificación enviada: {id: 123, ...}
```

---

## 📊 VERIFICACIÓN EN BASE DE DATOS

Puedes verificar que la notificación se guardó correctamente:

```bash
ssh root@31.97.8.51
PGPASSWORD=2025 psql -h 31.97.8.51 -U jesus -d app_registros
```

```sql
-- Ver últimas notificaciones con actividad vinculada
SELECT 
    n.id,
    n.titulo,
    n.actividad_id,
    n.motivos_atencion,
    r.tipo_actividad,
    r.descripcion
FROM notificaciones n
LEFT JOIN registros r ON n.actividad_id = r.id
WHERE n.actividad_id IS NOT NULL
ORDER BY n.id DESC
LIMIT 5;
```

---

## 📝 ARCHIVOS MODIFICADOS

### En VPS:
- ✅ `/var/www/PWASV/backend/main.py` - Backend actualizado
- ✅ Base de datos `app_registros` - Foreign key corregida

### En Local:
- ✅ `backend/main.py` - Validación corregida
- ✅ `SISTEMA_NOTIFICACIONES_ACTIVIDADES.md` - Documentación actualizada
- ✅ `backend/agregar_actividad_notificaciones.sql` - Script original (aún referencia reportes_generados)

---

## ⚠️ NOTA IMPORTANTE

El script SQL original `agregar_actividad_notificaciones.sql` todavía hace referencia a `reportes_generados`. Este script inicial fue sobrescrito por la corrección aplicada. Si necesitas recrear la estructura desde cero en otro ambiente, usa directamente:

```sql
-- Crear campo con la foreign key correcta desde el principio
ALTER TABLE notificaciones 
ADD COLUMN IF NOT EXISTS actividad_id INTEGER REFERENCES registros(id) ON DELETE SET NULL;

ALTER TABLE notificaciones 
ADD COLUMN IF NOT EXISTS motivos_atencion TEXT[];

CREATE INDEX IF NOT EXISTS idx_notificaciones_actividad 
ON notificaciones(actividad_id) 
WHERE actividad_id IS NOT NULL;
```

---

## ✅ ESTADO ACTUAL

- ✅ Base de datos corregida (foreign key apunta a `registros`)
- ✅ Backend actualizado (valida contra tabla `registros`)
- ✅ Frontend sin cambios (ya estaba enviando el ID correcto)
- ⏳ **PENDIENTE**: Reiniciar backend en VPS para aplicar cambios

---

## 🎉 ¡LISTO PARA USAR!

Una vez reiniciado el backend, el sistema de notificaciones sobre actividades estará completamente funcional y podrás enviar notificaciones contextuales a los usuarios sobre sus registros/actividades específicas.
