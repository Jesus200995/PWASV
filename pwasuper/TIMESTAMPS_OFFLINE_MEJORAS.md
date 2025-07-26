# Mejoras en el Sistema Offline - Gestión de Timestamps

## Problema Identificado

El sistema offline estaba guardando la hora actual (`timestamp`) cuando se creaba el registro offline, pero al sincronizar con el servidor, esta hora se trataba como la hora de creación del registro, no la hora de sincronización. Esto causaba que los registros aparecieran con la hora en que se sincronizaron en lugar de la hora en que realmente ocurrieron las actividades.

## Solución Implementada

### 1. Modificaciones en `offlineService.js`

- **Nuevo campo `sync_timestamp`**: Se agregó un campo adicional para distinguir entre:
  - `timestamp`: Hora de creación del registro offline (hora real de la actividad)
  - `sync_timestamp`: Hora en que se sincronizó con el servidor

- **Nuevo método `actualizarTimestampSincronizacion()`**: Actualiza el registro con la hora de sincronización antes de enviarlo al servidor.

- **Nuevo método `obtenerResumenPendientes()`**: Proporciona información detallada de los registros pendientes para debugging.

### 2. Modificaciones en `syncService.js`

- **Envío del timestamp original**: Al sincronizar, se envía el campo `timestamp_offline` con la hora original de creación del registro offline.
- **Actualización previa del sync_timestamp**: Antes de enviar cada registro, se actualiza con la hora de sincronización.

### 3. Modificaciones en `main.py` (Backend)

Se modificaron los endpoints para aceptar el campo opcional `timestamp_offline`:

- **`/registro`**: Acepta `timestamp_offline` para registros generales
- **`/asistencia/entrada`**: Acepta `timestamp_offline` para entradas
- **`/asistencia/salida`**: Acepta `timestamp_offline` para salidas

Cuando se recibe `timestamp_offline`, se usa esa fecha/hora para el registro en la base de datos. Si no se proporciona, se usa la hora actual del servidor.

## Estructura de Datos

### Registro Offline (IndexedDB)
```javascript
{
  id: 1,
  usuario_id: 123,
  latitud: 19.4326,
  longitud: -99.1332,
  descripcion: "Registro de actividad",
  foto_base64: "data:image/jpeg;base64,...",
  foto_filename: "foto.jpg",
  foto_type: "image/jpeg",
  timestamp: "2025-07-26T15:30:00.000Z",      // Hora de creación offline
  sync_timestamp: "2025-07-26T16:45:00.000Z", // Hora de sincronización
  tipo: "registro_general"
}
```

### Asistencia Offline (IndexedDB)
```javascript
{
  id: 1,
  usuario_id: 123,
  tipo: "entrada", // o "salida"
  latitud: 19.4326,
  longitud: -99.1332,
  descripcion: "Entrada al trabajo",
  foto_base64: "data:image/jpeg;base64,...",
  foto_filename: "entrada.jpg",
  foto_type: "image/jpeg",
  timestamp: "2025-07-26T08:00:00.000Z",      // Hora de creación offline
  sync_timestamp: "2025-07-26T16:45:00.000Z", // Hora de sincronización
  fecha: "2025-07-26"
}
```

## Flujo de Sincronización

1. **Creación Offline**: Se guarda el registro con `timestamp` (hora real) y `sync_timestamp: null`
2. **Sincronización**: 
   - Se actualiza `sync_timestamp` con la hora actual
   - Se envía `timestamp_offline` con la hora original al servidor
   - El servidor usa `timestamp_offline` para la fecha/hora del registro en la base de datos
3. **Eliminación**: Se elimina el registro offline después del envío exitoso

## Beneficios

- ✅ Los registros mantienen la hora real en que ocurrieron las actividades
- ✅ Se puede distinguir entre hora de actividad y hora de sincronización
- ✅ Mejor trazabilidad para debugging
- ✅ Compatibilidad con registros existentes (campo opcional)
- ✅ No afecta el funcionamiento online normal

## Debugging

Para verificar el estado de los registros offline:

```javascript
import offlineService from './services/offlineService.js';

// Obtener resumen detallado
const resumen = await offlineService.obtenerResumenPendientes();
console.log(resumen);
```

Esto mostrará todos los registros pendientes con sus timestamps para facilitar el debugging.
