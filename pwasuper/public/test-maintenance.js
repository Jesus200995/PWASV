// Script de prueba para simular modo mantenimiento
// Ejecutar en la consola del navegador de la PWA Super

console.log('🧪 SIMULADOR DE MODO MANTENIMIENTO');
console.log('================================');

// Función para activar mantenimiento manualmente
window.activarMantenimientoPrueba = function(mensaje = 'Prueba de mantenimiento desde consola') {
  console.log('🔧 Activando modo mantenimiento de prueba...');
  
  // Simular el cambio en el servicio
  if (window.vue && window.vue.$data) {
    // Si tenemos acceso a la instancia de Vue
    const app = window.vue;
    if (app.isMaintenanceMode !== undefined) {
      app.isMaintenanceMode = true;
      app.maintenanceMessage = mensaje;
      console.log('✅ Modo mantenimiento activado via Vue');
      return;
    }
  }
  
  // Método alternativo: disparar evento personalizado
  const event = new CustomEvent('maintenance-mode-change', {
    detail: { enabled: true, message: mensaje }
  });
  window.dispatchEvent(event);
  console.log('✅ Evento de mantenimiento disparado');
};

// Función para desactivar mantenimiento manualmente
window.desactivarMantenimientoPrueba = function() {
  console.log('🔧 Desactivando modo mantenimiento de prueba...');
  
  // Simular el cambio en el servicio
  if (window.vue && window.vue.$data) {
    // Si tenemos acceso a la instancia de Vue
    const app = window.vue;
    if (app.isMaintenanceMode !== undefined) {
      app.isMaintenanceMode = false;
      app.maintenanceMessage = '';
      console.log('✅ Modo mantenimiento desactivado via Vue');
      return;
    }
  }
  
  // Método alternativo: disparar evento personalizado
  const event = new CustomEvent('maintenance-mode-change', {
    detail: { enabled: false, message: '' }
  });
  window.dispatchEvent(event);
  console.log('✅ Evento de desactivación disparado');
};

// Función para obtener el estado actual
window.estadoMantenimiento = function() {
  if (window.vue && window.vue.$data) {
    const app = window.vue;
    if (app.isMaintenanceMode !== undefined) {
      console.log(`📋 Estado actual: ${app.isMaintenanceMode ? 'MANTENIMIENTO' : 'NORMAL'}`);
      if (app.isMaintenanceMode) {
        console.log(`📝 Mensaje: "${app.maintenanceMessage}"`);
      }
      return app.isMaintenanceMode;
    }
  }
  console.log('⚠️ No se pudo obtener el estado');
  return null;
};

console.log('');
console.log('📋 COMANDOS DISPONIBLES:');
console.log('');
console.log('✅ activarMantenimientoPrueba("Tu mensaje aquí")');
console.log('❌ desactivarMantenimientoPrueba()');
console.log('📊 estadoMantenimiento()');
console.log('');
console.log('Ejemplo:');
console.log('activarMantenimientoPrueba("Mantenimiento de prueba por 2 minutos")');
console.log('');

// Auto-detectar si ya hay mantenimiento activo
setTimeout(() => {
  const estado = window.estadoMantenimiento();
  if (estado === null) {
    console.log('💡 TIP: Si no funcionan los comandos directos, puedes usar:');
    console.log('');
    console.log('// Activar mantenimiento');
    console.log('localStorage.setItem("maintenance_mode", JSON.stringify({enabled: true, message: "Prueba"}));');
    console.log('location.reload();');
    console.log('');
    console.log('// Desactivar mantenimiento'); 
    console.log('localStorage.removeItem("maintenance_mode");');
    console.log('location.reload();');
  }
}, 1000);
