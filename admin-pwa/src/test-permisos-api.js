import axios from 'axios'

// Configurar axios con la URL de producción
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
console.log('🌐 Probando API:', API_BASE_URL)

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Función de prueba
async function probarEndpointPermisos() {
  console.log('🔄 Iniciando prueba de endpoints de permisos...')
  
  try {
    // Probar endpoint de health
    console.log('📡 Probando /health...')
    const healthResponse = await api.get('/health')
    console.log('✅ Health OK:', healthResponse.data)
    
    // Probar endpoint de usuarios admin
    console.log('📡 Probando /admin/usuarios...')
    const usuariosResponse = await api.get('/admin/usuarios')
    console.log('✅ Usuarios admin obtenidos:', usuariosResponse.data)
    
    return true
    
  } catch (error) {
    console.error('❌ Error en la prueba:', error)
    console.error('❌ Response status:', error.response?.status)
    console.error('❌ Response data:', error.response?.data)
    console.error('❌ Request URL:', error.config?.url)
    return false
  }
}

// Ejecutar la prueba cuando se carga el script
if (typeof window !== 'undefined') {
  window.probarEndpointPermisos = probarEndpointPermisos
  console.log('💡 Ejecuta probarEndpointPermisos() en la consola para probar')
}

export default probarEndpointPermisos
