# 📅 Sistema de Timestamps Precisos - Documentación

## 🎯 Objetivo
Asegurar que las asistencias (entrada/salida) mantengan la **hora exacta** en que se registraron, independientemente de si se guardaron offline o online, para un control preciso de horarios.

## 🔧 Implementación

### 1. **Registro Online** (`Home.vue`)
Cuando hay conexión a internet:
```javascript
// Se crea timestamp exacto al momento del registro
const timestampRegistro = new Date().toISOString();
formData.append("timestamp_registro", timestampRegistro);
```

### 2. **Registro Offline** (`offlineService.js`)
Cuando NO hay conexión:
```javascript
// Se guarda timestamp con máxima precisión (incluye milisegundos)
const timestamp = new Date().toISOString();
const asistencia = {
  timestamp: timestamp, // Hora EXACTA de creación offline
  fecha: fecha, // YYYY-MM-DD
  es_offline: true
};
```

### 3. **Sincronización** (`syncService.js`)
Al recuperar conexión, se envían múltiples campos:
```javascript
formData.append('timestamp_offline', asistencia.timestamp);     // Hora original offline
formData.append('timestamp_registro', asistencia.timestamp);    // Como timestamp_registro
formData.append('fecha_original', asistencia.fecha);           // Fecha original
```

## 📊 Campos Enviados al Backend

### Para registros Online:
- `timestamp_registro`: Hora exacta del registro online
- `usuario_id`, `latitud`, `longitud`, `descripcion`, `foto`

### Para registros Offline (sincronización):
- `timestamp_offline`: Hora exacta del registro offline
- `timestamp_registro`: Misma hora (para compatibilidad)
- `fecha_original`: Fecha del registro offline
- `usuario_id`, `latitud`, `longitud`, `descripcion`, `foto`

## ⚠️ Importante para el Backend

El backend debe:

1. **Detectar si viene `timestamp_offline`**:
   - Si existe → Usar esta fecha/hora en lugar de la actual
   - Si NO existe → Usar timestamp actual del servidor

2. **Usar el timestamp correcto**:
   ```python
   # Pseudocódigo Python
   if 'timestamp_offline' in request.form:
       # Registro viene de sincronización offline
       fecha_hora_registro = request.form['timestamp_offline']
   elif 'timestamp_registro' in request.form:
       # Registro online con timestamp específico
       fecha_hora_registro = request.form['timestamp_registro']
   else:
       # Fallback a hora actual del servidor
       fecha_hora_registro = datetime.now()
   ```

## 🕐 Formato de Timestamps

- **Formato**: ISO 8601 con milisegundos (`2025-01-26T18:30:45.123Z`)
- **Zona horaria**: UTC (se convierte al mostrar en interfaz)
- **Precisión**: Milisegundos para evitar conflictos

## 🔍 Debugging

### Para verificar timestamps en consola:
```javascript
// Offline - al guardar
console.log('💾 Timestamp guardado offline:', timestamp);

// Sync - al enviar
console.log('📤 Enviando timestamp_offline:', asistencia.timestamp);

// Online - al registrar
console.log('🕐 Timestamp de registro online:', timestampRegistro);
```

### Campos clave en IndexedDB:
- `timestamp`: Hora exacta de creación
- `sync_timestamp`: Hora de sincronización
- `es_offline`: Marcador de registro offline

## ✅ Resultado Esperado

- **Offline**: Registro guardado a las 14:30 → Se envía con timestamp 14:30 (no hora actual)
- **Online**: Registro enviado a las 14:30 → Se guarda con timestamp 14:30
- **Consistencia**: Ambos casos mantienen la hora real del registro

## 🚨 Validaciones

1. **Timestamp válido**: Se valida formato ISO antes de enviar
2. **Fallback seguro**: Si falla parsing, usa hora actual
3. **Logs detallados**: Para debugging de problemas de sincronización

---

**Nota**: Este sistema asegura transparencia total en los registros de horarios, manteniendo la hora exacta independientemente del estado de conectividad.
