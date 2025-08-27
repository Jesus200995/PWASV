// Health check service para verificar disponibilidad de endpoints
import axios from 'axios'
import { API_URL } from '../config/api.js'

class HealthCheckService {
  constructor() {
    this.endpointStatus = {}
    this.lastCheck = null
    this.checkInterval = 5 * 60 * 1000 // 5 minutos
  }

  /**
   * Verificar si un endpoint específico está disponible
   */
  async checkEndpoint(endpoint, method = 'GET') {
    try {
      const url = `${API_URL}${endpoint}`
      const config = {
        timeout: 5000,
        validateStatus: (status) => {
          // Considerar exitosos códigos 200, 401 (no autorizado pero existe), 422 (validación)
          return status === 200 || status === 401 || status === 422
        }
      }

      let response
      if (method === 'POST') {
        // Para endpoints POST como /admin/login, hacer una petición de prueba
        response = await axios.post(url, {}, config)
      } else {
        response = await axios.get(url, config)
      }

      this.endpointStatus[endpoint] = {
        available: true,
        status: response.status,
        lastCheck: Date.now()
      }

      return true
    } catch (error) {
      const isNotFound = error.response?.status === 404
      const isMethodNotAllowed = error.response?.status === 405
      
      this.endpointStatus[endpoint] = {
        available: false,
        status: error.response?.status || 0,
        error: error.message,
        lastCheck: Date.now(),
        notFound: isNotFound,
        methodNotAllowed: isMethodNotAllowed
      }

      return false
    }
  }

  /**
   * Verificar todos los endpoints críticos
   */
  async checkAllEndpoints() {
    console.log('🏥 Verificando salud de endpoints API...')
    
    const criticalEndpoints = [
      { path: '/admin/login', method: 'POST' },
      { path: '/auth/me', method: 'GET' },
      { path: '/usuarios', method: 'GET' },
      { path: '/asistencias', method: 'GET' },
      { path: '/notificaciones', method: 'GET' }
    ]

    const results = await Promise.all(
      criticalEndpoints.map(({ path, method }) => 
        this.checkEndpoint(path, method).then(available => ({ path, method, available }))
      )
    )

    this.lastCheck = Date.now()
    
    const available = results.filter(r => r.available).length
    const total = results.length
    
    console.log(`🏥 Health Check: ${available}/${total} endpoints disponibles`)
    
    results.forEach(({ path, method, available }) => {
      const status = available ? '✅' : '❌'
      console.log(`${status} ${method} ${path}`)
    })

    return {
      healthy: available === total,
      available,
      total,
      results,
      timestamp: this.lastCheck
    }
  }

  /**
   * Verificar si es necesario hacer un health check
   */
  shouldCheckHealth() {
    if (!this.lastCheck) return true
    return (Date.now() - this.lastCheck) > this.checkInterval
  }

  /**
   * Obtener estado de un endpoint específico
   */
  getEndpointStatus(endpoint) {
    return this.endpointStatus[endpoint] || { available: null, lastCheck: null }
  }

  /**
   * Verificar si un endpoint está disponible (con cache)
   */
  async isEndpointAvailable(endpoint, method = 'GET') {
    const status = this.getEndpointStatus(endpoint)
    
    // Si no hemos verificado antes o hace mucho tiempo, verificar ahora
    if (!status.lastCheck || (Date.now() - status.lastCheck) > this.checkInterval) {
      await this.checkEndpoint(endpoint, method)
    }
    
    return this.getEndpointStatus(endpoint).available
  }
}

// Exportar instancia única
export default new HealthCheckService()
