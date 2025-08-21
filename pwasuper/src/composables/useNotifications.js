import { ref, reactive } from 'vue'
import notificacionesService from '../services/notificacionesService.js'

// Estado global de notificaciones
const globalNotificationState = reactive({
  unreadCount: 0,
  isLoading: false,
  lastUpdate: null,
  userId: null
})

// Referencia reactiva al conteo no leídas
const unreadCount = ref(0)
const isUpdating = ref(false)

/**
 * Composable para manejar el estado global de notificaciones
 * Útil para mostrar badges en iconos de campana, etc.
 */
export const useNotifications = () => {
  
  /**
   * Obtener ID de usuario desde localStorage
   */
  const getUserId = () => {
    try {
      // 1. Buscar en 'user' (formato principal de PWASUPER)
      const userData = localStorage.getItem('user')
      if (userData) {
        const user = JSON.parse(userData)
        const id = user.id || user.usuario_id || user.user_id
        if (id) return parseInt(id)
      }
      
      // 2. Buscar en 'userData' (formato alternativo)
      const alternativeUserData = localStorage.getItem('userData')
      if (alternativeUserData) {
        const user = JSON.parse(alternativeUserData)
        const id = user.id || user.usuario_id || user.user_id
        if (id) return parseInt(id)
      }
      
      // 3. Fallback: buscar IDs directos
      const directIds = ['userId', 'user_id', 'id']
      for (const key of directIds) {
        const id = localStorage.getItem(key)
        if (id) return parseInt(id)
      }
      
      return null
    } catch (error) {
      console.error('Error obteniendo user ID:', error)
      return null
    }
  }

  /**
   * Actualizar conteo de notificaciones no leídas
   */
  const fetchUnreadCount = async (userId = null) => {
    try {
      const currentUserId = userId || getUserId()
      if (!currentUserId) {
        console.warn('No hay usuario identificado para obtener notificaciones')
        return 0
      }

      if (isUpdating.value) {
        console.log('Ya hay una actualización en curso...')
        return globalNotificationState.unreadCount
      }

      isUpdating.value = true
      globalNotificationState.isLoading = true
      globalNotificationState.userId = currentUserId
      
      console.log(`🔔 Actualizando conteo de no leídas para usuario ${currentUserId}`)
      
      const count = await notificacionesService.obtenerConteoNoLeidas(currentUserId)
      
      // Actualizar estado global
      globalNotificationState.unreadCount = count
      globalNotificationState.lastUpdate = new Date()
      unreadCount.value = count
      
      console.log(`🔔 Badge actualizado: ${count} notificaciones no leídas`)
      
      return count
      
    } catch (error) {
      console.error('Error obteniendo conteo no leídas:', error)
      
      // En desarrollo, simular datos
      if (import.meta.env.DEV) {
        const simulatedCount = Math.floor(Math.random() * 5)
        globalNotificationState.unreadCount = simulatedCount
        unreadCount.value = simulatedCount
        console.log(`🧪 Modo desarrollo: simulando ${simulatedCount} no leídas`)
        return simulatedCount
      }
      
      return 0
    } finally {
      isUpdating.value = false
      globalNotificationState.isLoading = false
    }
  }

  /**
   * Marcar una notificación como leída y actualizar conteo
   */
  const markAsRead = async (notificationId) => {
    try {
      const userId = getUserId()
      if (!userId) return false

      const deviceId = `browser_${navigator.userAgent.split(' ').pop()}_${Date.now()}`
      
      await notificacionesService.marcarComoLeida(notificationId, userId, deviceId)
      
      // Actualizar conteo después de marcar como leída
      await fetchUnreadCount(userId)
      
      return true
      
    } catch (error) {
      console.error('Error marcando como leída:', error)
      return false
    }
  }

  /**
   * Inicializar polling automático del conteo
   */
  const startPolling = (intervalMs = 2 * 60 * 1000) => { // 2 minutos por defecto
    const userId = getUserId()
    if (!userId) return null

    console.log(`🔄 Iniciando polling cada ${intervalMs / 1000}s para notificaciones`)
    
    // Obtener conteo inicial
    fetchUnreadCount(userId)
    
    // Configurar interval
    const intervalId = setInterval(() => {
      if (!isUpdating.value) {
        fetchUnreadCount(userId)
      }
    }, intervalMs)

    return intervalId
  }

  /**
   * Detener polling
   */
  const stopPolling = (intervalId) => {
    if (intervalId) {
      clearInterval(intervalId)
      console.log('🔄 Polling de notificaciones detenido')
    }
  }

  /**
   * Reiniciar estado (útil al cambiar de usuario)
   */
  const resetState = () => {
    globalNotificationState.unreadCount = 0
    globalNotificationState.isLoading = false
    globalNotificationState.lastUpdate = null
    globalNotificationState.userId = null
    unreadCount.value = 0
    isUpdating.value = false
    
    console.log('🔄 Estado de notificaciones reiniciado')
  }

  /**
   * Obtener información de estado completa
   */
  const getState = () => {
    return {
      unreadCount: globalNotificationState.unreadCount,
      isLoading: globalNotificationState.isLoading,
      lastUpdate: globalNotificationState.lastUpdate,
      userId: globalNotificationState.userId,
      isUpdating: isUpdating.value
    }
  }

  return {
    // Estado reactivo
    unreadCount,
    isUpdating,
    
    // Métodos
    fetchUnreadCount,
    markAsRead,
    startPolling,
    stopPolling,
    resetState,
    getState,
    getUserId,
    
    // Estado global (solo lectura)
    state: globalNotificationState
  }
}

export default useNotifications
