// Script de prueba para verificar la funcionalidad del historial
console.log('🧪 Iniciando pruebas del sistema de historial...');

// Probar conectividad con usuarios
fetch('http://localhost:8000/usuarios')
  .then(response => response.json())
  .then(data => {
    console.log('✅ Usuarios obtenidos:', data);
    
    if (data.usuarios && data.usuarios.length > 0) {
      const primerUsuario = data.usuarios[0];
      console.log('🧪 Probando historial para usuario:', primerUsuario.id);
      
      // Probar historial del primer usuario
      return fetch(`http://localhost:8000/historial/${primerUsuario.id}`);
    } else {
      throw new Error('No hay usuarios disponibles');
    }
  })
  .then(response => response.json())
  .then(historialData => {
    console.log('✅ Historial obtenido:', historialData);
    console.log(`📊 Total de registros: ${historialData.total}`);
  })
  .catch(error => {
    console.error('❌ Error en las pruebas:', error);
  });

// Probar endpoint de historial general
fetch('http://localhost:8000/historial')
  .then(response => response.json())
  .then(data => {
    console.log('✅ Historial general obtenido:', data);
    console.log(`📊 Total de registros generales: ${data.total}`);
  })
  .catch(error => {
    console.error('❌ Error obteniendo historial general:', error);
  });
