# INSTRUCCIONES PARA PROBAR TIMESTAMPS OFFLINE - EJECUTAR AHORA

## 🚀 PASO A PASO PARA VERIFICAR LA SOLUCIÓN

### 1. Abrir la Aplicación
- La aplicación ya está abierta en: http://localhost:5177/
- El backend está ejecutándose en puerto 8000

### 2. Abrir la Consola del Navegador
- Presiona F12 o clic derecho > Inspeccionar
- Ve a la pestaña "Console"

### 3. Ejecutar el Script de Prueba
Copia y pega este código en la consola:

```javascript
// SCRIPT DE PRUEBA INMEDIATA
console.log('🚀 INICIANDO PRUEBA DE TIMESTAMP OFFLINE');

async function pruebaInmediata() {
    try {
        // Importar servicios
        const { default: offlineService } = await import('./src/services/offlineService.js');
        const { default: syncService } = await import('./src/services/syncService.js');
        
        console.log('✅ Servicios importados');
        
        // Crear imagen de prueba
        const canvas = document.createElement('canvas');
        canvas.width = 50;
        canvas.height = 50;
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = '#00FF00';
        ctx.fillRect(0, 0, 50, 50);
        
        const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg'));
        const archivo = new File([blob], 'prueba-timestamp.jpg', { type: 'image/jpeg' });
        
        // TIMESTAMP DE HACE 2 HORAS (esto es lo que queremos conservar)
        const timestampOffline = new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString();
        console.log('🕐 TIMESTAMP OFFLINE (hace 2 horas):', timestampOffline);
        console.log('🕐 TIMESTAMP ACTUAL (para comparar):', new Date().toISOString());
        
        // Guardar registro offline
        const registroId = await offlineService.guardarRegistroOfflineConTimestamp(
            999, // usuario_id
            19.4326, // latitud
            -99.1332, // longitud
            'PRUEBA TIMESTAMP - DEBE MANTENER HORA ORIGINAL',
            archivo,
            timestampOffline
        );
        
        console.log('✅ Registro offline guardado con ID:', registroId);
        
        // Verificar datos guardados
        const registros = await offlineService.obtenerRegistrosPendientes();
        const registro = registros.find(r => r.id === registroId);
        console.log('📋 Registro guardado:', registro);
        console.log('🕐 Timestamp en registro:', registro.timestamp);
        
        // SINCRONIZAR
        console.log('🚀 SINCRONIZANDO...');
        console.log('🕐 Hora de sincronización:', new Date().toISOString());
        console.log('⚠️ MIRA LOS LOGS - Debe usar el timestamp offline, NO el actual');
        
        await syncService.sincronizarManual();
        
        console.log('✅ PRUEBA COMPLETADA');
        console.log('🔍 RESULTADOS ESPERADOS:');
        console.log('  ✓ En consola: "📤 ✅ ENVIANDO timestamp_offline"');
        console.log('  ✓ En backend: "📅 ✅ FORZANDO uso de timestamp offline"');
        console.log('  ✓ En BD: fecha/hora debe ser la original (hace 2 horas)');
        
    } catch (error) {
        console.error('❌ ERROR:', error);
    }
}

// EJECUTAR PRUEBA
pruebaInmediata();
```

### 4. Verificar los Resultados

**En la Consola del Navegador debes ver:**
- `📤 ✅ ENVIANDO timestamp_offline: [timestamp de hace 2 horas]`
- `📋 Campos del FormData:` mostrando `timestamp_offline`

**En la Consola del Backend debes ver:**
- `🔍 REGISTRO - Datos recibidos:`
- `timestamp_offline: '[timestamp]' (tipo: <class 'str'>)`
- `📅 ✅ FORZANDO uso de timestamp offline: [fecha convertida]`
- `✅ Registro guardado en BD con fecha_hora: [fecha original]`

### 5. Prueba Adicional de Asistencia

Si quieres probar también las asistencias, ejecuta:

```javascript
async function pruebaAsistencia() {
    const { default: offlineService } = await import('./src/services/offlineService.js');
    const { default: syncService } = await import('./src/services/syncService.js');
    
    const canvas = document.createElement('canvas');
    canvas.width = 50;
    canvas.height = 50;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#FF0000';
    ctx.fillRect(0, 0, 50, 50);
    
    const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg'));
    const archivo = new File([blob], 'asistencia-prueba.jpg', { type: 'image/jpeg' });
    
    const timestampOffline = new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString();
    console.log('🕐 TIMESTAMP ASISTENCIA (hace 3 horas):', timestampOffline);
    
    const asistenciaId = await offlineService.guardarAsistenciaOfflineConTimestamp(
        998, 'entrada', 19.4326, -99.1332, 'PRUEBA ASISTENCIA TIMESTAMP', archivo, timestampOffline
    );
    
    console.log('✅ Asistencia guardada con ID:', asistenciaId);
    await syncService.sincronizarManual();
    console.log('✅ Asistencia sincronizada');
}

pruebaAsistencia();
```

## ✅ CONFIRMACIÓN DE QUE FUNCIONA

Si ves estos mensajes, la solución está funcionando correctamente:
- Frontend envía `timestamp_offline` correctamente
- Backend recibe y usa el timestamp offline
- Los registros se guardan con la hora original, no la de sincronización

## 🧹 LIMPIAR DESPUÉS DE LA PRUEBA

```javascript
const { default: offlineService } = await import('./src/services/offlineService.js');
await offlineService.limpiarTodo();
console.log('🧹 Datos de prueba limpiados');
```
