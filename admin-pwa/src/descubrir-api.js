// Script para descubrir qué endpoints están disponibles en la API
import axios from 'axios'

const API_URL = 'https://apipwa.sembrandodatos.com'

async function descubrirEndpoints() {
  console.log('🔍 Descubriendo endpoints disponibles...')
  
  const endpointsComunes = [
    '/',
    '/docs',
    '/openapi.json',
    '/health',
    '/status',
    '/registros',
    '/api',
    '/api/docs',
    '/admin',
    '/login',
    '/auth'
  ]
  
  for (const endpoint of endpointsComunes) {
    try {
      console.log(`📡 Probando: ${API_URL}${endpoint}`)
      
      const response = await axios.get(`${API_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json'
        },
        timeout: 5000
      })
      
      console.log(`✅ DISPONIBLE - ${endpoint}:`, {
        status: response.status,
        contentType: response.headers['content-type'],
        hasData: !!response.data
      })
      
    } catch (error) {
      if (error.response?.status === 405) {
        console.log(`⚠️  MÉTODO NO PERMITIDO - ${endpoint}: (endpoint existe pero GET no permitido)`)
      } else if (error.response?.status === 401) {
        console.log(`🔐 REQUIERE AUTH - ${endpoint}: (endpoint existe pero requiere autenticación)`)
      } else {
        console.log(`❌ NO DISPONIBLE - ${endpoint}: ${error.response?.status || 'Sin respuesta'}`)
      }
    }
  }
}

// Ejecutar el descubrimiento
descubrirEndpoints().then(() => {
  console.log('\n🏁 Descubrimiento completado')
}).catch(err => {
  console.error('💥 Error en el descubrimiento:', err)
})
