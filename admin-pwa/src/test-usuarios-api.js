// Script para probar endpoints de usuarios en la API
import axios from 'axios'

const API_URL = 'https://apipwa.sembrandodatos.com'

async function probarEndpointsUsuarios() {
  console.log('🔍 Probando endpoints de usuarios...')
  
  const endpointsAPrueba = [
    '/usuarios',
    '/usuarios/',
    '/usuario',
    '/usuario/',
    '/users',
    '/user',
    '/api/usuarios',
    '/api/usuario'
  ]
  
  for (const endpoint of endpointsAPrueba) {
    try {
      console.log(`📡 Probando: ${API_URL}${endpoint}`)
      
      const response = await axios.get(`${API_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: 5000
      })
      
      console.log(`✅ ÉXITO - ${endpoint}:`, {
        status: response.status,
        dataType: Array.isArray(response.data) ? 'Array' : typeof response.data,
        dataLength: Array.isArray(response.data) ? response.data.length : 'N/A',
        firstItem: Array.isArray(response.data) && response.data.length > 0 ? response.data[0] : response.data
      })
      
    } catch (error) {
      console.log(`❌ FALLO - ${endpoint}:`, {
        status: error.response?.status || 'No response',
        message: error.message
      })
    }
  }
  
  // Probar endpoints específicos de usuario por ID
  console.log('\n🔍 Probando endpoints de usuario por ID...')
  
  const endpointsUsuarioId = [
    '/usuarios/1',
    '/usuarios/2',
    '/usuarios/3',
    '/usuario/1',
    '/usuario/2',
    '/usuario/3'
  ]
  
  for (const endpoint of endpointsUsuarioId) {
    try {
      console.log(`📡 Probando: ${API_URL}${endpoint}`)
      
      const response = await axios.get(`${API_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: 5000
      })
      
      console.log(`✅ ÉXITO - ${endpoint}:`, {
        status: response.status,
        usuario: response.data
      })
      
    } catch (error) {
      console.log(`❌ FALLO - ${endpoint}:`, {
        status: error.response?.status || 'No response',
        message: error.message
      })
    }
  }
}

// Ejecutar las pruebas
probarEndpointsUsuarios().then(() => {
  console.log('\n🏁 Pruebas completadas')
}).catch(err => {
  console.error('💥 Error en las pruebas:', err)
})
