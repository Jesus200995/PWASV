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

      console.log(`📋 Estado de mantenimiento recibido: ${isMaintenanceEnabled}`)
      console.log(`📋 Estado local anterior: ${this.lastKnownState}`)
      
      // Actualizar el estado global siempre
      window.maintenanceMode = {
        enabled: isMaintenanceEnabled,
        message: message
      };
      
      // Almacenar en localStorage como respaldo
      if (isMaintenanceEnabled) {
        localStorage.setItem('maintenance_mode', JSON.stringify({
          enabled: true,
          message: message,
          timestamp: new Date().toISOString()
        }));
      } else {
        localStorage.removeItem('maintenance_mode');
      }
      
      // IMPORTANTE: Solo notificar si HAY un cambio real
      if (isMaintenanceEnabled !== this.lastKnownState) {
        console.log(`🔄 CAMBIO DETECTADO: ${this.lastKnownState} → ${isMaintenanceEnabled}`)
        this.lastKnownState = isMaintenanceEnabled
        this.notifyListeners(isMaintenanceEnabled, message)
      } else {
        console.log(`ℹ️ Sin cambios en el estado de mantenimiento: ${isMaintenanceEnabled}`)
      }

      return {
        enabled: isMaintenanceEnabled,
        message: message,
        timestamp: data.timestamp || new Date().toISOString()
      }
    } catch (error) {
      console.log('⚠️ Error verificando mantenimiento:', error.message)
      
      // En caso de error, verificar localStorage como respaldo
      try {
        const storedMaintenance = localStorage.getItem('maintenance_mode');
        if (storedMaintenance) {
          const parsed = JSON.parse(storedMaintenance);
          // Verificar que el estado no sea muy antiguo (máximo 5 minutos)
          const timestamp = new Date(parsed.timestamp);
          const now = new Date();
          const diffMinutes = (now - timestamp) / (1000 * 60);
          
          if (diffMinutes < 5 && parsed.enabled) {
            console.log('🔧 Usando estado de mantenimiento desde localStorage (reciente)');
            
            // Actualizar estado global
            window.maintenanceMode = {
              enabled: true,
              message: parsed.message
            };
            
            return {
              enabled: true,
              message: parsed.message,
              error: error.message,
              fromCache: true
            };
          }
        }
      } catch (parseError) {
        console.error('Error parsing maintenance from localStorage:', parseError);
      }
      
      // Si no hay cache válido, asumir que NO hay mantenimiento
      window.maintenanceMode = {
        enabled: false,
        message: ''
      };
      
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

  /**
   * Verificar estado inicial de mantenimiento de forma síncrona
   */
  getInitialMaintenanceState() {
    // Verificar estado global
    if (window.maintenanceMode && window.maintenanceMode.enabled) {
      console.log('🔧 Estado inicial de mantenimiento desde window.maintenanceMode: ACTIVO');
      return {
        enabled: true,
        message: window.maintenanceMode.message
      };
    }
    
    // Verificar localStorage
    try {
      const storedMaintenance = localStorage.getItem('maintenance_mode');
      if (storedMaintenance) {
        const parsed = JSON.parse(storedMaintenance);
        if (parsed.enabled) {
          console.log('🔧 Estado inicial de mantenimiento desde localStorage: ACTIVO');
          
          // Actualizar estado global
          window.maintenanceMode = {
            enabled: true,
            message: parsed.message
          };
          
          return {
            enabled: true,
            message: parsed.message
          };
        }
      }
    } catch (error) {
      console.error('Error verificando localStorage para estado inicial:', error);
    }
    
    console.log('🔧 Estado inicial de mantenimiento: INACTIVO');
    return {
      enabled: false,
      message: ''
    };
  }
}

// Exportar instancia única
export default new MaintenanceCheckService()
