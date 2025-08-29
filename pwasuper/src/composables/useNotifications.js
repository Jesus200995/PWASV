import { ref, reactive } from 'vue'
import notificacionesService from '../services/notificacionesService.js'

// Estado global de notificaciones
const globalNotificationState = reactive({
  unreadCount: 0,
  isLoading: false,
  lastUpdate: null,
  userId: null,
  soundEnabled: true, // NUEVO: Control del sonido
  previousCount: 0,   // NUEVO: Para detectar cambios
  isInitialized: false // NUEVO: Para evitar sonido en carga inicial
})

// Referencia reactiva al conteo no leídas
const unreadCount = ref(0)
const isUpdating = ref(false)

// NUEVO: Audio global para notificaciones
let globalAudioNotification = null

// NUEVO: Inicializar audio global
const initializeGlobalAudio = () => {
  try {
    // Crear un beep utilizando Web Audio API
    const audioContext = new (window.AudioContext || window.webkitAudioContext)()
    
    // Función para crear un sonido de notificación suave tipo "ding" moderno
    const createNotificationSound = () => {
      const oscillator1 = audioContext.createOscillator()
      const oscillator2 = audioContext.createOscillator()
      const gainNode = audioContext.createGain()
      
      // Conectar los nodos
      oscillator1.connect(gainNode)
      oscillator2.connect(gainNode)
      gainNode.connect(audioContext.destination)
      
      // Configurar el primer oscilador - tono principal
      oscillator1.type = 'sine' // Onda sinusoidal suave
      oscillator1.frequency.setValueAtTime(1000, audioContext.currentTime)
      oscillator1.frequency.exponentialRampToValueAtTime(800, audioContext.currentTime + 0.1)
      
      // Configurar el segundo oscilador - armonía sutil
      oscillator2.type = 'sine'
      oscillator2.frequency.setValueAtTime(1200, audioContext.currentTime)
      oscillator2.frequency.exponentialRampToValueAtTime(960, audioContext.currentTime + 0.1)
      
      // Configurar el volumen - envolvente muy suave tipo "ding"
      gainNode.gain.setValueAtTime(0, audioContext.currentTime)
      gainNode.gain.linearRampToValueAtTime(1.0, audioContext.currentTime + 0.02) // Ataque rápido al 100%
      gainNode.gain.exponentialRampToValueAtTime(0.8, audioContext.currentTime + 0.1) // Sustain fuerte
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.6) // Decay largo y suave
      
      // Reproducir ambos osciladores
      oscillator1.start(audioContext.currentTime)
      oscillator1.stop(audioContext.currentTime + 0.6)
      
      oscillator2.start(audioContext.currentTime)
      oscillator2.stop(audioContext.currentTime + 0.6)
    }
    
    globalAudioNotification = createNotificationSound
    console.log('🔊 Audio global de notificaciones inicializado correctamente')
    
  } catch (error) {
    console.warn('⚠️ No se pudo inicializar el audio global de notificaciones:', error)
    
    // Fallback: usar vibración si está disponible
    globalAudioNotification = () => {
      try {
        if (navigator.vibrate) {
          navigator.vibrate([100, 50, 100]) // Patrón de vibración suave
        }
        console.log('📳 Usando vibración como alternativa al sonido')
      } catch (e) {
        console.log('🔇 No hay alternativas de audio/vibración disponibles')
      }
    }
  }
}

// NUEVO: Reproducir sonido de notificación global
const playGlobalNotificationSound = () => {
  try {
    if (globalNotificationState.soundEnabled && globalAudioNotification && typeof globalAudioNotification === 'function') {
      globalAudioNotification()
      console.log('🔊 Sonido global de notificación reproducido')
      
      // Mostrar notificación del navegador si está permitido
      if ('Notification' in window && Notification.permission === 'granted') {
        new Notification('Nueva notificación', {
          body: `Tienes ${globalNotificationState.unreadCount} notificación(es) no leída(s)`,
          icon: '/pwa-192x192.png',
          tag: 'new-notification',
          silent: false,
          requireInteraction: false,
          timestamp: Date.now()
        })
      }
    } else {
      console.log('🔇 Sonido deshabilitado o no disponible')
    }
  } catch (error) {
    console.warn('⚠️ Error reproduciendo sonido global de notificación:', error)
  }
}

// NUEVO: Detectar nuevas notificaciones y reproducir sonido globalmente
const detectNewNotifications = (newCount) => {
  // Solo reproducir sonido si:
  // 1. La aplicación ya está inicializada
  // 2. El nuevo conteo es mayor al anterior
  // 3. El sonido está habilitado
  if (globalNotificationState.isInitialized && 
      newCount > globalNotificationState.previousCount && 
      globalNotificationState.soundEnabled) {
    
    const newNotifications = newCount - globalNotificationState.previousCount
    console.log(`🔔 ${newNotifications} nueva(s) notificación(es) detectada(s) globalmente`)
    
    // Reproducir sonido
    playGlobalNotificationSound()
  }
  
  // Actualizar contador anterior para la próxima comparación
  globalNotificationState.previousCount = newCount
}

// NUEVO: Solicitar permisos de notificación
const requestNotificationPermission = async () => {
  if ('Notification' in window && Notification.permission === 'default') {
    try {
      const permission = await Notification.requestPermission()
      console.log(`🔔 Permisos de notificación: ${permission}`)
      return permission === 'granted'
    } catch (error) {
      console.warn('⚠️ Error solicitando permisos de notificación:', error)
      return false
    }
  }
  return Notification.permission === 'granted'
}

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
      
      // Solo hacer log detallado si es la primera vez o si hay cambios
      const isFirstLoad = globalNotificationState.lastUpdate === null
      if (isFirstLoad) {
        console.log(`🔔 Cargando conteo inicial de notificaciones para usuario ${currentUserId}`)
      }
      
      const count = await notificacionesService.obtenerConteoNoLeidas(currentUserId)
      
      // NUEVO: Detectar cambios y reproducir sonido si corresponde
      if (globalNotificationState.isInitialized) {
        detectNewNotifications(count)
      } else {
        // Primera carga - establecer contador base sin sonido
        globalNotificationState.previousCount = count
        globalNotificationState.isInitialized = true
        console.log(`🔔 Estado inicial establecido: ${count} notificaciones no leídas`)
      }
      
      // Actualizar estado global
      const prevCount = globalNotificationState.unreadCount
      globalNotificationState.unreadCount = count
      globalNotificationState.lastUpdate = new Date()
      unreadCount.value = count
      
      // Solo hacer log si cambió o es la primera carga
      if (isFirstLoad || prevCount !== count) {
        console.log(`🔔 Badge actualizado: ${prevCount || 0} → ${count} notificaciones no leídas`)
      }
      
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
   * Marcar una notificación como leída y actualizar conteo inmediatamente
   */
  const markAsRead = async (notificationId) => {
    try {
      const userId = getUserId()
      if (!userId) return false

      console.log(`🔔 Marcando notificación ${notificationId} como leída...`)
      
      // Actualización optimista del badge (decrementar inmediatamente)
      if (globalNotificationState.unreadCount > 0) {
        globalNotificationState.unreadCount--
        unreadCount.value = globalNotificationState.unreadCount
        console.log(`🔔 Badge actualizado optimísticamente: ${unreadCount.value}`)
      }

      const deviceId = `browser_${navigator.userAgent.split(' ').pop()}_${Date.now()}`
      
      await notificacionesService.marcarComoLeida(notificationId, userId, deviceId)
      
      // Verificar el conteo real del servidor para confirmar
      await fetchUnreadCount(userId)
      
      console.log(`✅ Notificación ${notificationId} marcada como leída correctamente`)
      return true
      
    } catch (error) {
      console.error('Error marcando como leída:', error)
      
      // Revertir actualización optimista en caso de error
      if (globalNotificationState.unreadCount >= 0) {
        globalNotificationState.unreadCount++
        unreadCount.value = globalNotificationState.unreadCount
        console.log(`🔄 Revirtiendo badge por error: ${unreadCount.value}`)
      }
      
      return false
    }
  }

  /**
   * Inicializar polling automático del conteo - cada segundo para respuesta inmediata
   */
  const startPolling = (intervalMs = 2000) => { // 2 segundos para balance entre respuesta y rendimiento
    const userId = getUserId()
    if (!userId) return null

    console.log(`🔄 Iniciando polling global cada ${intervalMs / 1000}s para notificaciones`)
    
    // NUEVO: Inicializar audio global y solicitar permisos
    initializeGlobalAudio()
    requestNotificationPermission()
    
    // Obtener conteo inicial
    fetchUnreadCount(userId)
    
    // Configurar interval - actualización constante para detectar nuevas notificaciones
    const intervalId = setInterval(async () => {
      if (!isUpdating.value) {
        // Actualización con detección de cambios y sonido
        const prevCount = globalNotificationState.unreadCount
        await fetchUnreadCount(userId)
        
        // Solo hacer log si cambió el conteo
        if (prevCount !== globalNotificationState.unreadCount) {
          console.log(`🔔 Badge actualizado globalmente: ${prevCount} → ${globalNotificationState.unreadCount}`)
        }
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
    globalNotificationState.previousCount = 0 // NUEVO: Reiniciar contador anterior
    globalNotificationState.isInitialized = false // NUEVO: Reiniciar inicialización
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
      isUpdating: isUpdating.value,
      soundEnabled: globalNotificationState.soundEnabled, // NUEVO
      previousCount: globalNotificationState.previousCount, // NUEVO
      isInitialized: globalNotificationState.isInitialized // NUEVO
    }
  }

  // NUEVO: Controlar sonido
  const enableSound = () => {
    globalNotificationState.soundEnabled = true
    console.log('🔊 Sonido de notificaciones habilitado')
  }

  const disableSound = () => {
    globalNotificationState.soundEnabled = false
    console.log('🔇 Sonido de notificaciones deshabilitado')
  }

  // NUEVO: Reproducir sonido manualmente (para pruebas)
  const playTestSound = () => {
    playGlobalNotificationSound()
  }

  return {
    // Estado reactivo
    unreadCount,
    isUpdating,
    
    // Métodos existentes
    fetchUnreadCount,
    markAsRead,
    startPolling,
    stopPolling,
    resetState,
    getState,
    getUserId,
    
    // NUEVOS: Métodos de sonido
    enableSound,
    disableSound,
    playTestSound,
    requestNotificationPermission,
    initializeGlobalAudio,
    
    // Estado global (solo lectura)
    state: globalNotificationState
  }
}

export default useNotifications
