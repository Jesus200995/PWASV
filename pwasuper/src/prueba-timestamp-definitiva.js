/**
 * SCRIPT DE PRUEBA DEFINITIVO - EJECUTAR EN CONSOLA
 * Este script GARANTIZA que el timestamp offline se conserve
 */

console.log('🚀 ============ PRUEBA DEFINITIVA TIMESTAMP OFFLINE ============');

async function pruebaDefinitiva() {
    try {
        // Importar servicios
        const { default: offlineService } = await import('./src/services/offlineService.js');
        const { default: syncService } = await import('./src/services/syncService.js');
        
        console.log('✅ Servicios importados correctamente');
        
        // Crear imagen de prueba
        const canvas = document.createElement('canvas');
        canvas.width = 100;
        canvas.height = 100;
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = '#FF5722';
        ctx.fillRect(0, 0, 100, 100);
        ctx.fillStyle = '#FFFFFF';
        ctx.font = '14px Arial';
        ctx.fillText('OFFLINE', 20, 50);
        ctx.fillText('TEST', 30, 70);
        
        const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg', 0.8));
        const archivo = new File([blob], 'prueba-definitiva.jpg', { type: 'image/jpeg' });
        
        // TIMESTAMP ESPECÍFICO (hace 2 horas y 30 minutos)
        const horaOffline = new Date(Date.now() - (2.5 * 60 * 60 * 1000)).toISOString();
        const horaActual = new Date().toISOString();
        
        console.log('🕐 ============ COMPARACIÓN DE HORAS ============');
        console.log('🕐 Hora OFFLINE (lo que queremos conservar):', horaOffline);
        console.log('🕐 Hora ACTUAL (NO debe usarse):', horaActual);
        console.log('🕐 Diferencia en minutos:', Math.round((new Date() - new Date(horaOffline)) / 60000));
        console.log('🕐 ==========================================');
        
        // GUARDAR REGISTRO OFFLINE con timestamp específico
        console.log('💾 Guardando registro offline...');
        const registroId = await offlineService.guardarRegistroOfflineConHoraEspecifica(
            777, // usuario_id único para identificar
            19.4326, // latitud CDMX
            -99.1332, // longitud CDMX
            'PRUEBA DEFINITIVA - CONSERVAR HORA OFFLINE',
            archivo,
            horaOffline // HORA ESPECÍFICA QUE DEBE CONSERVARSE
        );
        
        console.log('✅ Registro offline creado con ID:', registroId);
        
        // VERIFICAR que se guardó correctamente
        const registros = await offlineService.obtenerRegistrosPendientes();
        const registroGuardado = registros.find(r => r.id === registroId);
        
        console.log('🔍 ============ VERIFICACIÓN REGISTRO GUARDADO ============');
        console.log('🔍 Registro completo:', registroGuardado);
        console.log('🔍 Timestamp guardado:', registroGuardado.timestamp);
        console.log('🔍 ¿Es el timestamp correcto?', registroGuardado.timestamp === horaOffline ? '✅ SÍ' : '❌ NO');
        console.log('🔍 ================================================');
        
        // VERIFICAR CONEXIÓN
        const estadoConexion = syncService.getConnectionStatus();
        console.log('🌐 Estado de conexión:', estadoConexion);
        
        if (!estadoConexion.isOnline) {
            console.log('❌ No hay conexión a internet. Conecta y ejecuta manualmente:');
            console.log('   await syncService.sincronizarManual()');
            return;
        }
        
        // SINCRONIZAR
        console.log('🚀 ============ INICIANDO SINCRONIZACIÓN ============');
        console.log('🚀 Hora de sincronización (DIFERENTE a la offline):', new Date().toISOString());
        console.log('🚀 ATENCIÓN: Mira los logs del backend para verificar que usa el timestamp offline');
        console.log('🚀 =============================================');
        
        // Limpiar consola del navegador para ver mejor los logs
        console.clear();
        console.log('📊 ============ LOGS DE SINCRONIZACIÓN ============');
        
        await syncService.sincronizarManual();
        
        console.log('✅ ============ SINCRONIZACIÓN COMPLETADA ============');
        console.log('✅ VERIFICA EN LOS LOGS DEL BACKEND:');
        console.log('✅   1. "timestamp_offline: \'[horaOffline]\'"');
        console.log('✅   2. "📅 ✅ ✅ ✅ USANDO TIMESTAMP OFFLINE EXITOSAMENTE"');
        console.log('✅   3. "timestamp_usado: offline" en la respuesta');
        console.log('✅ ============================================');
        
        // VERIFICAR que no queden registros pendientes
        const pendientesPostSync = await offlineService.contarPendientes();
        console.log('📊 Registros pendientes después de sync:', pendientesPostSync);
        
        console.log('🎉 ============ PRUEBA COMPLETADA ============');
        console.log('🎉 Si viste "USANDO TIMESTAMP OFFLINE EXITOSAMENTE" en backend,');
        console.log('🎉 entonces el timestamp offline se conservó correctamente.');
        console.log('🎉 =======================================');
        
    } catch (error) {
        console.error('❌ ============ ERROR EN PRUEBA ============');
        console.error('❌ Error:', error);
        console.error('❌ Stack:', error.stack);
        console.error('❌ ================================');
    }
}

// FUNCIÓN PARA PROBAR ASISTENCIA TAMBIÉN
async function pruebaAsistenciaDefinitiva() {
    try {
        const { default: offlineService } = await import('./src/services/offlineService.js');
        const { default: syncService } = await import('./src/services/syncService.js');
        
        // Imagen para asistencia
        const canvas = document.createElement('canvas');
        canvas.width = 100;
        canvas.height = 100;
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = '#4CAF50';
        ctx.fillRect(0, 0, 100, 100);
        ctx.fillStyle = '#FFFFFF';
        ctx.font = '12px Arial';
        ctx.fillText('ENTRADA', 15, 45);
        ctx.fillText('OFFLINE', 20, 65);
        
        const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg', 0.8));
        const archivo = new File([blob], 'entrada-offline.jpg', { type: 'image/jpeg' });
        
        // Timestamp para entrada (hace 4 horas)
        const horaEntrada = new Date(Date.now() - (4 * 60 * 60 * 1000)).toISOString();
        
        console.log('🕐 ASISTENCIA - Hora offline de entrada:', horaEntrada);
        console.log('🕐 ASISTENCIA - Hora actual:', new Date().toISOString());
        
        const asistenciaId = await offlineService.guardarAsistenciaOfflineConHoraEspecifica(
            888, // usuario_id único
            'entrada',
            19.4326,
            -99.1332,
            'ENTRADA OFFLINE - CONSERVAR HORA',
            archivo,
            horaEntrada
        );
        
        console.log('✅ Asistencia offline guardada con ID:', asistenciaId);
        
        if (syncService.getConnectionStatus().isOnline) {
            console.log('🚀 Sincronizando asistencia...');
            await syncService.sincronizarManual();
            console.log('✅ Asistencia sincronizada');
        }
        
    } catch (error) {
        console.error('❌ Error en prueba de asistencia:', error);
    }
}

// EJECUTAR PRUEBA PRINCIPAL
pruebaDefinitiva();

// Agregar funciones a window para fácil acceso
window.pruebaTimestampDefinitiva = pruebaDefinitiva;
window.pruebaAsistenciaDefinitiva = pruebaAsistenciaDefinitiva;

console.log('🛠️ FUNCIONES DISPONIBLES:');
console.log('  - pruebaTimestampDefinitiva() - Prueba completa de registro');
console.log('  - pruebaAsistenciaDefinitiva() - Prueba completa de asistencia');
