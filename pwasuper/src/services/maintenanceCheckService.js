// Servicio para verificar el estado de mantenimiento en la PWA Super
import { API_URL } from '../utils/network.js'

class MaintenanceCheckService {
  constructor() {
    this.isChecking = false
    this.checkInterval = null
    this.lastKnownState = false
    this.listeners = []
  }

  /**
   * Verificar estado de mantenimiento una sola vez
   */
  async checkMaintenanceStatus() {
    try {
      console.log('🔍 Verificando estado de mantenimiento...')
      
      const response = await fetch(`${API_URL}/maintenance/status`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        // No timeout muy largo para que no bloquee la app
        signal: AbortSignal.timeout(5000)
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }

      const data = await response.json()
      const isMaintenanceEnabled = data.maintenance || false
      const message = data.message || 'Sistema en mantenimiento'

      console.log(`📋 Estado de mantenimiento: ${isMaintenanceEnabled}`)
      
      // Si el estado cambió, notificar a los listeners
      if (isMaintenanceEnabled !== this.lastKnownState) {
        console.log(`🔄 Estado cambió de ${this.lastKnownState} a ${isMaintenanceEnabled}`)
        this.lastKnownState = isMaintenanceEnabled
        this.notifyListeners(isMaintenanceEnabled, message)
      }

      return {
        enabled: isMaintenanceEnabled,
        message: message,
        timestamp: data.timestamp || new Date().toISOString()
      }
    } catch (error) {
      console.log('⚠️ Error verificando mantenimiento (continuando normalmente):', error.message)
      // En caso de error, asumir que no hay mantenimiento para no bloquear la app
      return {
        enabled: false,
        message: '',
        error: error.message
      }
    }
  }

  /**
   * Iniciar verificación periódica
   */
  startPeriodicCheck(intervalMs = 30000) { // 30 segundos por defecto
    console.log(`🔄 Iniciando verificación periódica de mantenimiento cada ${intervalMs/1000}s`)
    
    // Hacer una verificación inicial
    this.checkMaintenanceStatus()
    
    // Configurar verificaciones periódicas
    if (this.checkInterval) {
      clearInterval(this.checkInterval)
    }
    
    this.checkInterval = setInterval(() => {
      this.checkMaintenanceStatus()
    }, intervalMs)
  }

  /**
   * Detener verificación periódica
   */
  stopPeriodicCheck() {
    if (this.checkInterval) {
      console.log('⏹️ Deteniendo verificación periódica de mantenimiento')
      clearInterval(this.checkInterval)
      this.checkInterval = null
    }
  }

  /**
   * Suscribirse a cambios de estado
   */
  onStateChange(callback) {
    if (typeof callback === 'function') {
      this.listeners.push(callback)
      console.log(`📡 Listener agregado. Total: ${this.listeners.length}`)
    }
  }

  /**
   * Desuscribirse de cambios de estado
   */
  removeStateChangeListener(callback) {
    const index = this.listeners.indexOf(callback)
    if (index > -1) {
      this.listeners.splice(index, 1)
      console.log(`📡 Listener removido. Total: ${this.listeners.length}`)
    }
  }

  /**
   * Notificar a todos los listeners sobre cambios
   */
  notifyListeners(enabled, message) {
    console.log(`📡 Notificando ${this.listeners.length} listeners sobre cambio de estado`)
    this.listeners.forEach(callback => {
      try {
        callback(enabled, message)
      } catch (error) {
        console.error('Error en listener de mantenimiento:', error)
      }
    })
  }

  /**
   * Obtener el último estado conocido
   */
  getLastKnownState() {
    return this.lastKnownState
  }

  /**
   * Forzar verificación inmediata
   */
  async forceCheck() {
    console.log('🔄 Forzando verificación inmediata de mantenimiento')
    return await this.checkMaintenanceStatus()
  }
}

// Exportar instancia única
export default new MaintenanceCheckService()
