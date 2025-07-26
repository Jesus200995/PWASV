/**
 * Script de prueba para verificar el servicio de geolocalización
 * Ejecutar en la consola del navegador para debuggear
 */

// Función para probar el servicio de geolocalización
async function probarGeolocalizacion() {
  console.log('🧪 Iniciando pruebas de geolocalización...');
  
  try {
    // Importar el servicio (si está disponible globalmente)
    if (window.geoLocationService) {
      const service = window.geoLocationService;
      
      console.log('📊 Estado inicial del servicio:', service.getStatus());
      
      // Probar obtener ubicación
      console.log('🔍 Probando getLocationSmart...');
      const location = await service.getLocationSmart();
      
      console.log('✅ Ubicación obtenida:', location);
      console.log('📊 Estado después de obtener ubicación:', service.getStatus());
      
      return location;
    } else {
      console.error('❌ Servicio de geolocalización no encontrado en window');
    }
  } catch (error) {
    console.error('❌ Error en prueba:', error);
  }
}

// Función para probar navigator.geolocation directamente
function probarGeolocationNativo() {
  console.log('🧪 Probando navigator.geolocation directamente...');
  
  if (!navigator.geolocation) {
    console.error('❌ navigator.geolocation no está disponible');
    return;
  }
  
  navigator.geolocation.getCurrentPosition(
    (position) => {
      console.log('✅ Ubicación nativa obtenida:', {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        accuracy: position.coords.accuracy
      });
    },
    (error) => {
      console.error('❌ Error geolocalización nativa:', error);
    },
    {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 60000
    }
  );
}

// Función para verificar permisos
async function verificarPermisos() {
  console.log('🔐 Verificando permisos de geolocalización...');
  
  try {
    if ('permissions' in navigator) {
      const permission = await navigator.permissions.query({name: 'geolocation'});
      console.log('📋 Estado del permiso:', permission.state);
      
      permission.addEventListener('change', () => {
        console.log('🔄 Cambio en permisos:', permission.state);
      });
    } else {
      console.log('⚠️ API de permisos no disponible');
    }
  } catch (error) {
    console.error('❌ Error verificando permisos:', error);
  }
}

// Ejecutar pruebas automáticamente
console.log('🚀 Herramientas de debugging de geolocalización cargadas');
console.log('💡 Ejecuta las siguientes funciones en la consola:');
console.log('  - probarGeolocalizacion()');
console.log('  - probarGeolocationNativo()');
console.log('  - verificarPermisos()');

// Verificar permisos automáticamente
verificarPermisos();
