// Configuración de API para diferentes entornos
const API_CONFIGS = {
  production: {
    baseURL: 'https://apipwa.sembrandodatos.com',
    endpoints: {
      adminLogin: '/admin/login',
      authMe: '/auth/me',
      usuarios: '/usuarios',
      // Otros endpoints según la API de producción
    }
  },
  local: {
    baseURL: 'http://localhost:8000',
    endpoints: {
      adminLogin: '/admin/login',
      authMe: '/auth/me',
      usuarios: '/admin/usuarios',
      // Endpoints locales con rutas completas
    }
  }
}

// Detectar automáticamente el entorno
const getEnvironment = () => {
  const hostname = window.location.hostname
  
  // FORZAR PRODUCCION - Siempre usar API de producción
  return 'production'
  
  // Código original comentado (para desarrollo local):
  // if (hostname === 'localhost' || hostname === '127.0.0.1') {
  //   return 'local'
  // }
  // return 'production'
}

// Exportar configuración del entorno actual
const currentEnv = getEnvironment()
export const API_CONFIG = API_CONFIGS[currentEnv]
export const API_URL = API_CONFIG.baseURL

console.log(`🌍 Entorno API: ${currentEnv}`)
console.log(`🔗 API URL: ${API_URL}`)

export default API_CONFIG
