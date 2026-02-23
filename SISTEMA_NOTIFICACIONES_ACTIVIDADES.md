# 🔔 SISTEMA DE NOTIFICACIONES SOBRE ACTIVIDADES

## Implementación completada el 23 de febrero de 2026

---

## 📋 RESUMEN

Se ha implementado un sistema completo para enviar notificaciones individuales a usuarios sobre actividades específicas desde la vista de Registros.

### Características principales:
✅ Botón "Notificar" en cada actividad de RegistrosView.vue
✅ Modal inteligente con pre-llenado automático de datos
✅ Selección múltiple de motivos de atención
✅ Vinculación de notificaciones con actividades específicas
✅ Soporte completo en backend y frontend

---

## 🚀 PASOS PARA APLICAR LOS CAMBIOS

### 1. Actualizar la Base de Datos

Ejecuta el script Python para agregar los nuevos campos:

```bash
cd backend
python agregar_actividad_notificaciones.py
```

Este script agregará:
- Campo `actividad_id` en la tabla `notificaciones` (vincula con `reportes_generados`)
- Campo `motivos_atencion` (array de strings)
- Índice para optimizar consultas por actividad

### 2. Reiniciar el Backend

El backend ya está actualizado con los cambios necesarios. Solo reinicia el servidor:

```bash
# Detener el servidor (Ctrl+C)
# Luego ejecutar:
python backend/main.py
```

### 3. Reiniciar el Frontend

El frontend también está actualizado. Reinicia el servidor de desarrollo:

```bash
cd admin-pwa
# Detener el servidor (Ctrl+C)
# Luego ejecutar:
npm run dev
```

---

## 📝 CÓMO USAR LA FUNCIONALIDAD

### Desde RegistrosView.vue:

1. **Ver la lista de registros de actividades**
   - Cada registro ahora tiene un botón naranja "Notificar" (🔔)

2. **Hacer clic en "Notificar"**
   - Se abre un modal con la información de la actividad
   - El título y subtítulo se pre-llenan automáticamente

3. **Completar el formulario:**
   - ✏️ **Título**: Pre-llenado (puedes editarlo)
   - 📝 **Subtítulo**: Pre-llenado con la categoría (opcional)
   - ⚠️ **Motivos de atención**: Selecciona uno o más (obligatorio)
     * Llamar atención
     * Corrección requerida
     * Información faltante
     * Revisión urgente
     * Documentación pendiente
     * Seguimiento necesario
     * Felicitación por buen trabajo
     * Otro motivo
   - 💬 **Mensaje detallado**: Escribe el mensaje para el usuario (obligatorio)
   - 🔗 **Enlace opcional**: URL con información adicional

4. **Enviar la notificación**
   - El usuario recibirá la notificación vinculada a esa actividad específica
   - Podrá ver sobre qué reporte/actividad se le está notificando

---

## 🎨 CAMBIOS VISUALES

### Botón "Notificar"
- Color: Naranja (#FF9800) 
- Ubicación: Entre el botón "Detalles" (verde) y "Editar" (amarillo)
- Icono: Campana de notificación
- Animaciones: Hover con efecto de brillo y escala

### Modal de Notificación
- Diseño consistente con el modal de edición
- Header naranja distintivo
- Sección de información readonly mostrando: Tipo, Categoría, Fecha
- Grid de checkboxes para motivos de atención
- Validaciones en tiempo real

---

## 🔧 CAMBIOS TÉCNICOS

### Base de Datos (PostgreSQL)
```sql
-- Nuevos campos en tabla notificaciones
actividad_id INTEGER REFERENCES reportes_generados(id) ON DELETE SET NULL
motivos_atencion TEXT[]
```

### Backend (main.py)
- Endpoint `POST /notificaciones` actualizado con:
  - Parámetro `actividad_id` (opcional)
  - Parámetro `motivos_atencion` (opcional, JSON array)
  - Validación de existencia de actividad
  - Logging detallado

### Frontend (admin-pwa)

#### RegistrosView.vue
- Nuevo botón "Notificar" en acciones
- Modal completo con formulario
- Variables reactivas:
  * `showNotificarModal`
  * `actividadANotificar`
  * `formNotificacion`
  * `motivosAtencionOpciones`
- Métodos:
  * `abrirModalNotificar(registro)`
  * `cerrarModalNotificar()`
  * `enviarNotificacion()`

#### notificacionesService.js
- Método `crearNotificacion()` actualizado
- Soporte para `actividad_id` y `motivos_atencion`

---

## 📊 FLUJO DE DATOS

```
┌─────────────────────┐
│  RegistrosView.vue  │
│                     │
│ [Botón Notificar] ──┼──> Abre Modal
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│  Modal Notificar    │
│                     │
│ • Pre-llena datos   │
│ • Muestra actividad │
│ • Select motivos    │
│ • Descripción       │
└─────────────────────┘
           │
           ▼ [Enviar]
┌─────────────────────┐
│ notificaciones      │
│ Service.js          │
│                     │
│ FormData con:       │
│ - titulo            │
│ - subtitulo         │
│ - descripcion       │
│ - actividad_id ✨   │
│ - motivos[] ✨      │
│ - usuario_ids[]     │
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│  Backend API        │
│  POST /notificaciones
│                     │
│ • Valida actividad  │
│ • Valida motivos    │
│ • Crea notificación │
│ • Vincula con user  │
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│  Base de Datos      │
│                     │
│ notificaciones:     │
│ - id: 123           │
│ - titulo: "..."     │
│ - actividad_id: 456 ✨
│ - motivos: [...]    ✨
│                     │
│ notificacion_usuarios:
│ - notificacion_id   │
│ - usuario_id        │
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│  Usuario Final      │
│  (en PWA Supervisor)│
│                     │
│ Ve notificación:    │
│ "Sobre actividad    │
│  del 23/02/2026"    │
└─────────────────────┘
```

---

## ✅ VALIDACIONES IMPLEMENTADAS

### Frontend
- ✅ Título obligatorio (máx. 150 caracteres)
- ✅ Subtítulo opcional (máx. 200 caracteres)
- ✅ Al menos un motivo seleccionado
- ✅ Descripción obligatoria
- ✅ Formato URL válido (si se proporciona)

### Backend
- ✅ Título obligatorio y longitud validada
- ✅ Subtítulo longitud validada (si existe)
- ✅ Actividad debe existir en reportes_generados
- ✅ Usuario debe existir
- ✅ Motivos deben ser un array válido
- ✅ Archivo máximo 50MB

---

## 🔍 EJEMPLOS DE USO

### Caso 1: Corrección requerida
```
Usuario reporta actividad de campo pero falta información GPS

Admin hace clic en "Notificar":
- Título: "Notificación sobre Actividad Campo - 23/02/2026"
- Motivos: ["correccion_requerida", "informacion_faltante"]
- Descripción: "Hola Juan, tu reporte del 23/02 no tiene coordenadas GPS válidas. Por favor verifica que tu GPS esté habilitado y vuelve a registrar la actividad."
```

### Caso 2: Felicitación
```
Usuario tiene excelente registro con fotos de calidad

Admin hace clic en "Notificar":
- Título: "¡Excelente trabajo! - Actividad 23/02/2026"
- Motivos: ["felicitacion"]
- Descripción: "María, tu reporte de hoy es ejemplar. Las fotos son muy claras y la descripción detallada. ¡Sigue así!"
```

### Caso 3: Revisión urgente
```
Actividad requiere atención inmediata

Admin hace clic en "Notificar":
- Título: "URGENTE: Revisar actividad del 23/02/2026"
- Motivos: ["revision_urgente", "documentacion_pendiente"]
- Descripción: "Pedro, tu actividad reporta un problema crítico. Necesitamos que envíes la documentación faltante hoy mismo."
```

---

## 🐛 DEBUGGING Y LOGS

El sistema incluye logging extenso:

### Backend
```python
print(f"🔔 Creando notificación: {titulo}")
print(f"📊 Notificación vinculada a actividad ID: {actividad_id}")
print(f"⚠️ Motivos de atención: {motivos_array}")
```

### Frontend
```javascript
console.log('🔔 Abriendo modal para notificar sobre actividad:', registro)
console.log('✅ Notificación enviada:', respuesta)
```

Revisa las consolas del navegador y del backend para seguir el flujo completo.

---

## 📱 RESPONSIVE

El modal es completamente responsive:
- Desktop: Grid de 3 columnas para info de actividad
- Tablet: Grid de 2 columnas
- Móvil: Columna única con scroll vertical

---

## 🎯 PRÓXIMAS MEJORAS (OPCIONAL)

- [ ] Ver historial de notificaciones por actividad
- [ ] Plantillas pre-configuradas de notificaciones
- [ ] Notificaciones masivas a múltiples actividades
- [ ] Estadísticas de respuesta a notificaciones
- [ ] Recordatorios automáticos

---

## ⚠️ NOTAS IMPORTANTES

1. **No olvides aplicar los cambios de BD** antes de usar la funcionalidad
2. Los **motivos de atención** se almacenan como array PostgreSQL
3. La **actividad_id** tiene `ON DELETE SET NULL` para preservar notificaciones históricas
4. Los **usuarios deben existir** antes de enviar notificación
5. La notificación se envía **inmediatamente** al usuario de la actividad

---

## 📞 SOPORTE

Si encuentras algún problema:
1. Revisa los logs del backend
2. Revisa la consola del navegador
3. Verifica que la BD tenga los campos nuevos
4. Confirma que el usuario de la actividad existe

---

## ✨ ¡LISTO!

El sistema está completamente implementado y listo para usar. Solo falta aplicar los cambios de base de datos y reiniciar los servidores.

**¡Disfruta notificando a tus usuarios sobre sus actividades! 🎉**
