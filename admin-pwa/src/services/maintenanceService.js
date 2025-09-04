// Servicio de mantenimiento para controlar el estado de la PWA Super
import axios from 'axios'
import { API_URL } from '../config/api.js'

class MaintenanceService {
  constructor() {
    this.maintenanceEndpoint = `${API_URL}/maintenance`
  }

  /**
   * Obtener el token de autorización
   */
  getAuthHeaders() {
    const token = localStorage.getItem('admin_token')
    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  }

  /**
   * Activar modo mantenimiento
   */
  async activarMantenimiento(message = 'Sistema en mantenimiento. Volveremos pronto.') {
    try {
      console.log('🔧 Activando modo mantenimiento...')
      
      const response = await axios.post(`${this.maintenanceEndpoint}/enable`, {
        maintenance: true,
        message: message,
        enabled_at: new Date().toISOString(),
        enabled_by: localStorage.getItem('admin_user') || 'admin'
      }, {
        headers: this.getAuthHeaders()
      })

      console.log('✅ Modo mantenimiento activado:', response.data)
      return {
        success: true,
        data: response.data,
        message: 'Modo mantenimiento activado correctamente'
      }
    } catch (error) {
      console.error('❌ Error activando mantenimiento:', error)
      
      // Si no existe el endpoint, simular activación
      if (error.response?.status === 404) {
        console.log('⚠️ Endpoint de mantenimiento no encontrado, simulando activación...')
        
        // Guardar estado local como fallback
        localStorage.setItem('maintenance_mode', JSON.stringify({
          enabled: true,
          message: message,
          enabled_at: new Date().toISOString(),
          enabled_by: localStorage.getItem('admin_user') || 'admin'
        }))
        
        return {
          success: true,
          simulated: true,
          message: 'Modo mantenimiento activado (simulado)'
        }
      }

      throw {
        success: false,
        error: error.response?.data?.detail || error.message || 'Error activando mantenimiento'
      }
    }
  }

  /**
   * Desactivar modo mantenimiento
   */
  async desactivarMantenimiento() {
    try {
      console.log('🔧 Desactivando modo mantenimiento...')
      
      const response = await axios.post(`${this.maintenanceEndpoint}/disable`, {
        maintenance: false,
        disabled_at: new Date().toISOString(),
        disabled_by: localStorage.getItem('admin_user') || 'admin'
      }, {
        headers: this.getAuthHeaders()
      })

      console.log('✅ Modo mantenimiento desactivado:', response.data)
      return {
        success: true,
        data: response.data,
        message: 'Modo mantenimiento desactivado correctamente'
      }
    } catch (error) {
      console.error('❌ Error desactivando mantenimiento:', error)
      
      // Si no existe el endpoint, simular desactivación
      if (error.response?.status === 404) {
        console.log('⚠️ Endpoint de mantenimiento no encontrado, simulando desactivación...')
        
        // Remover estado local
        localStorage.removeItem('maintenance_mode')
        
        return {
          success: true,
          simulated: true,
          message: 'Modo mantenimiento desactivado (simulado)'
        }
      }

      throw {
        success: false,
        error: error.response?.data?.detail || error.message || 'Error desactivando mantenimiento'
      }
    }
  }

  /**
   * Verificar estado del modo mantenimiento
   */
  async verificarEstadoMantenimiento() {
    try {
      console.log('🔍 Verificando estado de mantenimiento...')
      
      const response = await axios.get(`${this.maintenanceEndpoint}/status`, {
        headers: this.getAuthHeaders()
      })

      console.log('📋 Estado de mantenimiento:', response.data)
      return {
        success: true,
        data: response.data,
        enabled: response.data.maintenance || false,
        message: response.data.message || ''
      }
    } catch (error) {
      console.error('❌ Error verificando estado:', error)
      
      // Si no existe el endpoint, verificar estado local
      if (error.response?.status === 404) {
        console.log('⚠️ Endpoint de mantenimiento no encontrado, verificando estado local...')
        
        const localState = localStorage.getItem('maintenance_mode')
        if (localState) {
          const state = JSON.parse(localState)
          return {
            success: true,
            simulated: true,
            data: state,
            enabled: state.enabled || false,
            message: state.message || ''
          }
        }
        
        return {
          success: true,
          simulated: true,
          enabled: false,
          message: ''
        }
      }

      throw {
        success: false,
        error: error.response?.data?.detail || error.message || 'Error verificando estado'
      }
    }
  }

  /**
   * Notificar a la PWA Super sobre el cambio de estado
   */
  async notificarCambioEstado(enabled) {
    try {
      console.log(`📡 Notificando cambio de estado de mantenimiento: ${enabled}`)
      
      // Intentar notificar a través de WebSocket o Server-Sent Events si están disponibles
      // Por ahora, usar una llamada HTTP simple
      const response = await axios.post(`${API_URL}/maintenance/notify`, {
        maintenance: enabled,
        timestamp: new Date().toISOString(),
        source: 'admin-panel'
      }, {
        headers: this.getAuthHeaders()
      })

      console.log('✅ Notificación enviada:', response.data)
      return { success: true, data: response.data }
    } catch (error) {
      console.log('⚠️ Error enviando notificación (continuando):', error.message)
      // No fallar si no se puede notificar, es opcional
      return { success: false, error: error.message }
    }
  }

  /**
   * Activar mantenimiento y notificar
   */
  async activarMantenimientoCompleto(message) {
    const resultado = await this.activarMantenimiento(message)
    if (resultado.success) {
      await this.notificarCambioEstado(true)
    }
    return resultado
  }

  /**
   * Desactivar mantenimiento y notificar
   */
  async desactivarMantenimientoCompleto() {
    const resultado = await this.desactivarMantenimiento()
    if (resultado.success) {
      await this.notificarCambioEstado(false)
    }
    return resultado
  }
}

// Exportar instancia única
export default new MaintenanceService()
