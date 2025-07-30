// Test específico para usuarios e historial después de la migración a API de producción
console.log('🧪 Testing servicios de Usuarios e Historial...');

// Simulamos la importación de los servicios (en el navegador esto estaría disponible)
const API_BASE = 'https://apipwa.sembrandodatos.com';

async function testUsuariosService() {
  console.log('\n📊 Testing UsuariosService...');
  
  try {
    // Test 1: Obtener usuarios regulares
    console.log('🔍 Test 1: Obteniendo usuarios...');
    const responseUsuarios = await fetch(`${API_BASE}/usuarios`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    if (responseUsuarios.ok) {
      const dataUsuarios = await responseUsuarios.json();
      console.log('✅ Usuarios obtenidos:', dataUsuarios.usuarios?.length || 0, 'usuarios');
    } else {
      console.log('❌ Error obteniendo usuarios:', responseUsuarios.status);
    }

    // Test 2: Obtener usuarios con contraseñas (exportación completa)
    console.log('🔍 Test 2: Obteniendo usuarios con contraseñas...');
    const responseExportacion = await fetch(`${API_BASE}/usuarios/exportacion-completa`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    if (responseExportacion.ok) {
      const dataExportacion = await responseExportacion.json();
      console.log('✅ Usuarios con contraseñas obtenidos:', dataExportacion.usuarios?.length || 0, 'usuarios');
      
      // Probar historial si hay usuarios
      if (dataExportacion.usuarios && dataExportacion.usuarios.length > 0) {
        await testHistorialService(dataExportacion.usuarios[0].id);
      }
    } else {
      const errorText = await responseExportacion.text();
      console.log('❌ Error obteniendo usuarios con contraseñas:', responseExportacion.status, errorText);
    }

  } catch (error) {
    console.error('❌ Error en testUsuariosService:', error);
  }
}

async function testHistorialService(usuarioId) {
  console.log('\n📈 Testing HistorialService...');
  
  try {
    // Test 1: Obtener historial de usuario específico
    console.log(`🔍 Test 1: Obteniendo historial del usuario ${usuarioId}...`);
    const responseHistorial = await fetch(`${API_BASE}/historial/${usuarioId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    if (responseHistorial.ok) {
      const dataHistorial = await responseHistorial.json();
      console.log('✅ Historial de usuario obtenido:', dataHistorial.total || 0, 'registros');
    } else {
      const errorText = await responseHistorial.text();
      console.log('❌ Error obteniendo historial de usuario:', responseHistorial.status, errorText);
    }

    // Test 2: Obtener resumen de historial
    console.log(`🔍 Test 2: Obteniendo resumen del usuario ${usuarioId}...`);
    const responseResumen = await fetch(`${API_BASE}/historial/resumen/${usuarioId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    if (responseResumen.ok) {
      const dataResumen = await responseResumen.json();
      console.log('✅ Resumen obtenido:', dataResumen);
    } else {
      const errorText = await responseResumen.text();
      console.log('❌ Error obteniendo resumen:', responseResumen.status, errorText);
    }

    // Test 3: Obtener historial general (si está disponible)
    console.log('🔍 Test 3: Obteniendo historial general...');
    const responseGeneral = await fetch(`${API_BASE}/historial`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    if (responseGeneral.ok) {
      const dataGeneral = await responseGeneral.json();
      console.log('✅ Historial general obtenido:', dataGeneral.total || 0, 'registros');
    } else {
      const errorText = await responseGeneral.text();
      console.log('❌ Error obteniendo historial general:', responseGeneral.status, errorText);
    }

  } catch (error) {
    console.error('❌ Error en testHistorialService:', error);
  }
}

// Ejecutar tests
async function runTests() {
  console.log('🚀 Iniciando tests de servicios...');
  await testUsuariosService();
  console.log('\n✅ Tests completados!');
}

runTests().catch(error => {
  console.error('❌ Error general en los tests:', error);
});
