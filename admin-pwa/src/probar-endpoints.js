// Script para probar endpoints de la API
// Ejecutar en la consola del navegador

async function probarEndpoints() {
  const API_URL = 'https://apipwa.sembrandodatos.com';
  const token = localStorage.getItem('admin_token');
  
  if (!token) {
    console.log('❌ No hay token de admin. Haz login primero.');
    return;
  }
  
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  };
  
  // Lista de endpoints posibles para usuarios
  const endpointsUsuarios = [
    '/usuarios',
    '/usuario', 
    '/users',
    '/user',
    '/admin/usuarios',
    '/admin/users',
    '/api/usuarios',
    '/api/users'
  ];
  
  // Lista de endpoints posibles para registros
  const endpointsRegistros = [
    '/registros',
    '/registro',
    '/records',
    '/record',
    '/admin/registros',
    '/admin/records',
    '/api/registros',
    '/api/records'
  ];
  
  console.log('🔍 Probando endpoints de usuarios...');
  
  for (const endpoint of endpointsUsuarios) {
    try {
      const response = await fetch(`${API_URL}${endpoint}`, { 
        method: 'GET',
        headers 
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log(`✅ ${endpoint} - Status: ${response.status}`, data);
      } else {
        console.log(`❌ ${endpoint} - Status: ${response.status} (${response.statusText})`);
      }
    } catch (error) {
      console.log(`❌ ${endpoint} - Error:`, error.message);
    }
    
    // Pequeña pausa entre requests
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  console.log('🔍 Probando endpoints de registros...');
  
  for (const endpoint of endpointsRegistros) {
    try {
      const response = await fetch(`${API_URL}${endpoint}`, { 
        method: 'GET',
        headers 
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log(`✅ ${endpoint} - Status: ${response.status}`, data);
      } else {
        console.log(`❌ ${endpoint} - Status: ${response.status} (${response.statusText})`);
      }
    } catch (error) {
      console.log(`❌ ${endpoint} - Error:`, error.message);
    }
    
    // Pequeña pausa entre requests
    await new Promise(resolve => setTimeout(resolve, 100));
  }
}

// Ejecutar automáticamente
probarEndpoints();
