/**
 * Script de prueba para verificar el correcto funcionamiento del sistema offline
 * Ejecutar en la consola del navegador después de cargar la aplicación
 */

console.log('🧪 Iniciando prueba del sistema offline...');

// Función auxiliar para crear un blob de imagen de prueba
function crearImagenPrueba() {
  const canvas = document.createElement('canvas');
  canvas.width = 100;
  canvas.height = 100;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#FF0000';
  ctx.fillRect(0, 0, 100, 100);
  ctx.fillStyle = '#FFFFFF';
  ctx.font = '12px Arial';
  ctx.fillText('Test', 35, 50);
  
  return new Promise(resolve => {
    canvas.toBlob(blob => {
      const file = new File([blob], 'test-offline.jpg', { type: 'image/jpeg' });
      resolve(file);
    }, 'image/jpeg');
  });
}

// Función principal de prueba
async function probarSistemaOffline() {
  try {
    console.log('📋 Paso 1: Importando servicios...');
    
    // Importar servicios (esto depende de tu configuración de módulos)
    const { default: offlineService } = await import('./src/services/offlineService.js');
    const { default: syncService } = await import('./src/services/syncService.js');
    
    console.log('📋 Paso 2: Crear imagen de prueba...');
    const imagenPrueba = await crearImagenPrueba();
    
    console.log('📋 Paso 3: Crear registro offline...');
    const timestampOffline = new Date().toISOString();
    console.log('🕐 Timestamp de creación offline:', timestampOffline);
    
    // Simular un registro offline
    const registroId = await offlineService.guardarRegistroOffline(
      123, // usuario_id
      19.4326, // latitud CDMX
      -99.1332, // longitud CDMX
      'Prueba de registro offline',
      imagenPrueba
    );
    
    console.log('✅ Registro offline creado con ID:', registroId);
    
    console.log('📋 Paso 4: Verificar datos guardados...');
    const resumen = await offlineService.obtenerResumenPendientes();
    console.log('📊 Resumen de datos offline:', resumen);
    
    console.log('📋 Paso 5: Esperar 3 segundos para simular diferencia de tiempo...');
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    console.log('📋 Paso 6: Sincronizar datos...');
    console.log('🕐 Hora de sincronización:', new Date().toISOString());
    
    // Verificar que hay conexión
    const status = syncService.getConnectionStatus();
    console.log('🌐 Estado de conexión:', status);
    
    if (status.isOnline) {
      await syncService.sincronizarManual();
      console.log('✅ Sincronización completada');
      
      console.log('📋 Paso 7: Verificar que se eliminó de offline...');
      const resumenFinal = await offlineService.obtenerResumenPendientes();
      console.log('📊 Resumen final:', resumenFinal);
    } else {
      console.log('❌ No hay conexión, no se puede probar la sincronización');
    }
    
    console.log('🎉 Prueba completada exitosamente');
    
  } catch (error) {
    console.error('❌ Error durante la prueba:', error);
  }
}

// Función para prueba de asistencia
async function probarAsistenciaOffline() {
  try {
    console.log('📋 Iniciando prueba de asistencia offline...');
    
    const { default: offlineService } = await import('./src/services/offlineService.js');
    const { default: syncService } = await import('./src/services/syncService.js');
    
    const imagenPrueba = await crearImagenPrueba();
    const timestampOffline = new Date().toISOString();
    console.log('🕐 Timestamp de asistencia offline:', timestampOffline);
    
    // Crear asistencia de entrada offline
    const asistenciaId = await offlineService.guardarAsistenciaOffline(
      123, // usuario_id
      'entrada', // tipo
      19.4326, // latitud
      -99.1332, // longitud
      'Entrada offline de prueba',
      imagenPrueba
    );
    
    console.log('✅ Asistencia offline creada con ID:', asistenciaId);
    
    console.log('📋 Esperando 3 segundos...');
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    console.log('📋 Sincronizando asistencia...');
    const status = syncService.getConnectionStatus();
    
    if (status.isOnline) {
      await syncService.sincronizarManual();
      console.log('✅ Asistencia sincronizada');
    } else {
      console.log('❌ No hay conexión para sincronizar');
    }
    
  } catch (error) {
    console.error('❌ Error en prueba de asistencia:', error);
  }
}

// Funciones de utilidad para debugging
window.debugOffline = {
  probarRegistro: probarSistemaOffline,
  probarAsistencia: probarAsistenciaOffline,
  
  async verPendientes() {
    const { default: offlineService } = await import('./src/services/offlineService.js');
    const resumen = await offlineService.obtenerResumenPendientes();
    console.table(resumen.registros.items);
    console.table(resumen.asistencias.items);
    return resumen;
  },
  
  async limpiarTodo() {
    const { default: offlineService } = await import('./src/services/offlineService.js');
    await offlineService.limpiarTodo();
    console.log('🧹 Datos offline limpiados');
  },
  
  async sincronizar() {
    const { default: syncService } = await import('./src/services/syncService.js');
    await syncService.sincronizarManual();
    console.log('🔄 Sincronización manual completada');
  }
};

console.log('🛠️ Herramientas de debugging disponibles en window.debugOffline:');
console.log('  - debugOffline.probarRegistro() - Prueba completa de registro offline');
console.log('  - debugOffline.probarAsistencia() - Prueba completa de asistencia offline');
console.log('  - debugOffline.verPendientes() - Ver datos pendientes');
console.log('  - debugOffline.limpiarTodo() - Limpiar todos los datos offline');
console.log('  - debugOffline.sincronizar() - Forzar sincronización manual');
