// Script para verificar que la configuración de la API está funcionando correctamente
console.log('🔍 Verificando conexión con la API de producción...');

const API_URL = 'https://apipwa.sembrandodatos.com';

async function verificarEndpoints() {
  const endpoints = [
    { url: `${API_URL}/usuarios`, nombre: 'Usuarios' },
    { url: `${API_URL}/usuarios/exportacion-completa`, nombre: 'Usuarios con contraseñas' },
    { url: `${API_URL}/historial`, nombre: 'Historial general' },
    { url: `${API_URL}/asistencias`, nombre: 'Asistencias' }
  ];

  console.log(`\n📡 Probando ${endpoints.length} endpoints principales...\n`);

  for (const endpoint of endpoints) {
    try {
      console.log(`🧪 Probando ${endpoint.nombre}...`);
      
      const response = await fetch(endpoint.url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log(`✅ ${endpoint.nombre}: OK (${response.status})`);
        
        // Mostrar información básica del response
        if (data.usuarios) {
          console.log(`   📊 ${data.usuarios.length} usuarios encontrados`);
        } else if (data.asistencias) {
          console.log(`   📊 ${data.asistencias.length} asistencias encontradas`);
        } else if (data.registros) {
          console.log(`   📊 ${data.registros.length} registros encontrados`);
        } else if (Array.isArray(data)) {
          console.log(`   📊 ${data.length} elementos encontrados`);
        }
      } else {
        console.log(`❌ ${endpoint.nombre}: Error ${response.status} - ${response.statusText}`);
      }
    } catch (error) {
      console.log(`❌ ${endpoint.nombre}: Error de conexión - ${error.message}`);
    }
    
    console.log(''); // Línea en blanco para separar
  }

  console.log('🔚 Verificación completada');
}

// Ejecutar verificación
verificarEndpoints().catch(error => {
  console.error('❌ Error general en la verificación:', error);
});
