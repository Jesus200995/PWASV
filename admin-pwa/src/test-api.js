// Script de prueba para verificar la API
// Ejecutar desde la consola del navegador

const API_URL = 'https://apipwa.sembrandodatos.com';

// Función para probar endpoints
async function probarAPI() {
  const token = localStorage.getItem('admin_token');
  
  if (!token) {
    console.log('❌ No hay token de admin. Primero haz login.');
    return;
  }
  
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  };
  
  try {
    console.log('🔍 Probando endpoint /usuarios...');
    const usuariosResponse = await fetch(`${API_URL}/usuarios`, { headers });
    const usuariosData = await usuariosResponse.json();
    console.log('✅ Usuarios:', usuariosData);
    console.log('📊 Estructura usuarios:', Array.isArray(usuariosData) ? 'Array directo' : 'Objeto con propiedades');
    
    console.log('🔍 Probando endpoint /registros...');
    const registrosResponse = await fetch(`${API_URL}/registros`, { headers });
    const registrosData = await registrosResponse.json();
    console.log('✅ Registros:', registrosData);
    console.log('📊 Estructura registros:', Array.isArray(registrosData) ? 'Array directo' : 'Objeto con propiedades');
    
  } catch (error) {
    console.error('❌ Error al probar API:', error);
  }
}

// Ejecutar la prueba
probarAPI();
