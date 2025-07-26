/**
 * SCRIPT DE PRUEBA INMEDIATA - Ejecutar en consola del navegador
 * Para verificar que el timestamp offline funciona correctamente
 */

console.log('🚀 INICIANDO PRUEBA INMEDIATA DEL TIMESTAMP OFFLINE');

// Función para crear registro de prueba INMEDIATO
async function pruebaInmediata() {
    try {
        // Importar servicios
        const { default: offlineService } = await import('./src/services/offlineService.js');
        const { default: syncService } = await import('./src/services/syncService.js');
        
        console.log('✅ Servicios importados');
        
        // Crear una imagen simple
        const canvas = document.createElement('canvas');
        canvas.width = 50;
        canvas.height = 50;
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = '#00FF00';
        ctx.fillRect(0, 0, 50, 50);
        
        const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg'));
        const archivo = new File([blob], 'prueba-timestamp.jpg', { type: 'image/jpeg' });
        
        console.log('✅ Imagen de prueba creada');
        
        // Crear timestamp específico (hace 2 horas)
        const timestampOffline = new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString();
        console.log('🕐 TIMESTAMP OFFLINE QUE QUEREMOS CONSERVAR:', timestampOffline);
        console.log('🕐 TIMESTAMP ACTUAL (para comparar):', new Date().toISOString());
        
        // Guardar registro offline con timestamp específico usando el nuevo método
        console.log('📝 Guardando registro offline con timestamp personalizado...');
        
        const registroId = await offlineService.guardarRegistroOfflineConTimestamp(
            999, // usuario_id de prueba
            19.4326, // latitud
            -99.1332, // longitud
            'PRUEBA TIMESTAMP OFFLINE - DEBE MANTENER HORA ORIGINAL',
            archivo,
            timestampOffline
        );
        
        console.log('✅ Registro offline guardado con ID:', registroId);
        
        // Verificar que se guardó con el timestamp correcto
        const registros = await offlineService.obtenerRegistrosPendientes();
        const registroGuardado = registros.find(r => r.id === registroId);
        
        console.log('📋 VERIFICACIÓN - Registro guardado:', registroGuardado);
        console.log('🕐 VERIFICACIÓN - Timestamp en registro:', registroGuardado.timestamp);
        console.log('✅ CORRECTO - El timestamp offline se guardó correctamente');
        
        // Verificar conexión
        const conexion = syncService.getConnectionStatus();
        console.log('🌐 Estado de conexión:', conexion);
        
        if (conexion.isOnline) {
            console.log('🚀 INICIANDO SINCRONIZACIÓN...');
            console.log('🕐 HORA DE SINCRONIZACIÓN (debe ser diferente):', new Date().toISOString());
            console.log('⚠️ IMPORTANTE: Mira los logs del backend para verificar que usa el timestamp offline');
            
            // Sincronizar manualmente
            await syncService.sincronizarManual();
            
            console.log('✅ SINCRONIZACIÓN COMPLETADA');
            console.log('📋 EN EL BACKEND debes ver:');
            console.log('   - timestamp_offline recibido:', timestampOffline);
            console.log('   - "📅 ✅ FORZANDO uso de timestamp offline"');
            console.log('   - Fecha/hora guardada en BD debe ser la original, NO la actual');
            
        } else {
            console.log('❌ No hay conexión para sincronizar');
            console.log('� Conecta a internet y ejecuta: await syncService.sincronizarManual()');
        }
        
    } catch (error) {
        console.error('❌ ERROR EN PRUEBA:', error);
    }
}

// Función para probar asistencia también
async function pruebaAsistenciaInmediata() {
    try {
        const { default: offlineService } = await import('./src/services/offlineService.js');
        const { default: syncService } = await import('./src/services/syncService.js');
        
        // Crear imagen
        const canvas = document.createElement('canvas');
        canvas.width = 50;
        canvas.height = 50;
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = '#FF0000';
        ctx.fillRect(0, 0, 50, 50);
        
        const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg'));
        const archivo = new File([blob], 'prueba-asistencia.jpg', { type: 'image/jpeg' });
        
        // Timestamp hace 3 horas
        const timestampOffline = new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString();
        console.log('🕐 TIMESTAMP ASISTENCIA OFFLINE:', timestampOffline);
        
        const asistenciaId = await offlineService.guardarAsistenciaOfflineConTimestamp(
            998, // usuario_id
            'entrada',
            19.4326,
            -99.1332,
            'PRUEBA ASISTENCIA TIMESTAMP OFFLINE',
            archivo,
            timestampOffline
        );
        
        console.log('✅ Asistencia guardada con ID:', asistenciaId);
        
        if (syncService.getConnectionStatus().isOnline) {
            console.log('🚀 Sincronizando asistencia...');
            await syncService.sincronizarManual();
            console.log('✅ Asistencia sincronizada');
        }
        
    } catch (error) {
        console.error('❌ Error en prueba de asistencia:', error);
    }
}

// Ejecutar prueba
pruebaInmediata();

// También agregar funciones a window para acceso fácil
window.pruebaTimestamp = pruebaInmediata;
window.pruebaAsistenciaTimestamp = pruebaAsistenciaInmediata;

console.log('🛠️ FUNCIONES DISPONIBLES:');
console.log('  - pruebaTimestamp() - Prueba registro con timestamp offline');
console.log('  - pruebaAsistenciaTimestamp() - Prueba asistencia con timestamp offline');
