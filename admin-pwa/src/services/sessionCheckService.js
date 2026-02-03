// sessionCheckService.js
import axios from 'axios'
import { API_URL } from '../config/api.js'

class SessionCheckService {
  constructor() {
    this.checkInterval = null
    this.checkIntervalTime = 30000 // Verificar cada 30 segundos
    this.listeners = []
  }

  /**
   * Iniciar verificación periódica de la sesión
   */
  startSessionCheck() {
    // Limpiar intervalo anterior si existe
    if (this.checkInterval) {
      clearInterval(this.checkInterval)
    }

    // Verificar inmediatamente
    this.checkSession()

    // Configurar verificación periódica
    this.checkInterval = setInterval(() => {
      this.checkSession()
    }, this.checkIntervalTime)

    console.log('🔒 Verificación de sesión iniciada (cada 30s)')
  }

  /**
   * Detener verificación periódica
   */
  stopSessionCheck() {
    if (this.checkInterval) {
      clearInterval(this.checkInterval)
      this.checkInterval = null
      console.log('🔓 Verificación de sesión detenida')
    }
  }

  /**
   * Verificar si la sesión sigue siendo válida
   */
  async checkSession() {
    try {
      // Obtener datos del usuario del localStorage
      const userDataStr = localStorage.getItem('admin_user')
      if (!userDataStr) {
        return // No hay sesión activa
      }

      const userData = JSON.parse(userDataStr)
      const userId = userData.id
      const sessionVersion = userData.session_version || 1

      // Verificar con el backend
      const response = await axios.get(
        `${API_URL}/usuarios/${userId}/session-check`,
        {
          params: { session_version: sessionVersion }
        }
      )

      const { valid, reason, current_version } = response.data

      if (!valid) {
        console.log('❌ Sesión invalidada:', reason)
        this.notifySessionInvalid(reason, current_version)
      }

    } catch (error) {
      console.error('Error verificando sesión:', error)
      // No hacer nada en caso de error de red, solo en caso de sesión inválida
    }
  }

  /**
   * Notificar a los listeners que la sesión fue invalidada
   */
  notifySessionInvalid(reason, newVersion) {
    this.listeners.forEach(listener => {
      if (typeof listener === 'function') {
        listener(reason, newVersion)
      }
    })
  }

  /**
   * Agregar un listener para eventos de sesión invalidada
   * @param {Function} callback - Función a ejecutar cuando la sesión sea invalidada
   * @returns {Function} Función para remover el listener
   */
  onSessionInvalid(callback) {
    this.listeners.push(callback)

    // Retornar función para remover el listener
    return () => {
      const index = this.listeners.indexOf(callback)
      if (index > -1) {
        this.listeners.splice(index, 1)
      }
    }
  }

  /**
   * Actualizar la versión de sesión en localStorage
   */
  updateSessionVersion(newVersion) {
    try {
      const userDataStr = localStorage.getItem('admin_user')
      if (userDataStr) {
        const userData = JSON.parse(userDataStr)
        userData.session_version = newVersion
        localStorage.setItem('admin_user', JSON.stringify(userData))
        console.log('✅ Versión de sesión actualizada:', newVersion)
      }
    } catch (error) {
      console.error('Error actualizando versión de sesión:', error)
    }
  }

  /**
   * Obtener la versión de sesión actual
   */
  getCurrentSessionVersion() {
    try {
      const userDataStr = localStorage.getItem('admin_user')
      if (userDataStr) {
        const userData = JSON.parse(userDataStr)
        return userData.session_version || 1
      }
    } catch (error) {
      console.error('Error obteniendo versión de sesión:', error)
    }
    return 1
  }
}

// Crear instancia única (singleton)
const sessionCheckService = new SessionCheckService()

export default sessionCheckService
