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
    
    // Función para crear un sonido de campanita suave y delicada
    const createNotificationSound = () => {
      const oscillator1 = audioContext.createOscillator()
      const oscillator2 = audioContext.createOscillator()
      const gainNode = audioContext.createGain()
      const filterNode = audioContext.createBiquadFilter()
      
      // Conectar los nodos con filtro para sonido de campanita
      oscillator1.connect(filterNode)
      oscillator2.connect(filterNode)
      filterNode.connect(gainNode)
      gainNode.connect(audioContext.destination)
      
      // Configurar filtro para sonido de campanita cristalina
      filterNode.type = 'lowpass'
      filterNode.frequency.setValueAtTime(3000, audioContext.currentTime)
      filterNode.frequency.exponentialRampToValueAtTime(1500, audioContext.currentTime + 0.8)
      filterNode.Q.setValueAtTime(2, audioContext.currentTime)
      
      // Primer oscilador - campanita principal (Do mayor)
      oscillator1.type = 'sine'
      oscillator1.frequency.setValueAtTime(1046.5, audioContext.currentTime) // C6 (Do)
      oscillator1.frequency.exponentialRampToValueAtTime(523.25, audioContext.currentTime + 0.4) // C5 (Do octava baja)
      
      // Segundo oscilador - armonía de campanita (Mi mayor)
      oscillator2.type = 'triangle'
      oscillator2.frequency.setValueAtTime(1318.5, audioContext.currentTime) // E6 (Mi)
      oscillator2.frequency.exponentialRampToValueAtTime(659.25, audioContext.currentTime + 0.4) // E5 (Mi)
      
      // Configurar volumen - envolvente de campanita suave
      gainNode.gain.setValueAtTime(0, audioContext.currentTime)
      gainNode.gain.rapidRampToValueAtTime(0.8, audioContext.currentTime + 0.01) // Ataque instantáneo de campanita
      gainNode.gain.exponentialRampToValueAtTime(0.6, audioContext.currentTime + 0.1) // Sustain inicial
      gainNode.gain.exponentialRampToValueAtTime(0.2, audioContext.currentTime + 0.4) // Decaimiento suave
      gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 1.5) // Eco largo de campanita
      
      // Reproducir campanitas con timing delicado
      oscillator1.start(audioContext.currentTime)
      oscillator2.start(audioContext.currentTime + 0.03) // Ligeramente desfasado para realismo
      
      oscillator1.stop(audioContext.currentTime + 1.5)
      oscillator2.stop(audioContext.currentTime + 1.2) // Se desvanece antes para efecto natural
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

// MEJORADO: Solicitar permisos de notificación y configurar push notifications
const requestNotificationPermission = async () => {
  console.log('🔔 Iniciando proceso de permisos de notificación...');
  
  if (!('Notification' in window)) {
    console.warn('❌ Este navegador no soporta notificaciones');
    return false;
  }

  if (!('serviceWorker' in navigator)) {
    console.warn('❌ Service Worker no disponible');
    return false;
  }

  let permission = Notification.permission;
  console.log(`🔔 Permisos actuales: ${permission}`);

  // Si los permisos están por defecto, solicitarlos de manera insistente
  if (permission === 'default') {
    try {
      // Mostrar mensaje explicativo antes de solicitar
      const userWantsNotifications = confirm(
        '🔔 ¿Quieres recibir notificaciones de nuevas actividades incluso cuando la app esté cerrada?\n\n' +
        'Esto te permitirá estar siempre al día con las novedades.'
      );
      
      if (userWantsNotifications) {
        permission = await Notification.requestPermission();
        console.log(`🔔 Resultado de solicitud: ${permission}`);
        
        // Notificar al service worker sobre el cambio de permisos
        if (navigator.serviceWorker.controller) {
          navigator.serviceWorker.controller.postMessage({
            type: 'NOTIFICATION_PERMISSION_UPDATED',
            granted: permission === 'granted'
          });
        }
        
        if (permission === 'granted') {
          // Configurar push notifications inmediatamente
          await setupPushNotifications();
          
          // Mostrar notificación de bienvenida
          new Notification('✅ ¡Notificaciones activadas!', {
            body: 'Ahora recibirás notificaciones incluso con la app cerrada',
            icon: '/pwa-192x192.png',
            tag: 'welcome-notification'
          });
          
          return true;
        } else {
          // Si el usuario negó, intentar convencerlo una vez más
          setTimeout(() => {
            alert(
              '❌ Sin permisos de notificación no podrás recibir alertas cuando la app esté cerrada.\n\n' +
              '💡 Puedes activarlas después desde la configuración del navegador.'
            );
          }, 1000);
          return false;
        }
      } else {
        console.log('👤 Usuario decidió no recibir notificaciones');
        return false;
      }
    } catch (error) {
      console.error('❌ Error solicitando permisos de notificación:', error);
      return false;
    }
  }
  
  if (permission === 'granted') {
    await setupPushNotifications();
    
    // Notificar al service worker
    if (navigator.serviceWorker.controller) {
      navigator.serviceWorker.controller.postMessage({
        type: 'NOTIFICATION_PERMISSION_UPDATED',
        granted: true
      });
    }
    
    return true;
  }
  
  console.warn('❌ Permisos de notificación denegados');
  return false;
}

// NUEVO: Configurar push notifications para funcionamiento en segundo plano
const setupPushNotifications = async () => {
  try {
    const registration = await navigator.serviceWorker.ready
    
    // Verificar si ya hay una suscripción push activa
    let subscription = await registration.pushManager.getSubscription()
    
    if (!subscription) {
      // Crear nueva suscripción push
      subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: generateVAPIDKey()
      })
      
      console.log('📡 Suscripción push creada para notificaciones en segundo plano')
      
      // Enviar suscripción al servidor (opcional, para push notifications desde servidor)
      await sendSubscriptionToServer(subscription)
    }
    
    // Configurar sincronización en segundo plano para polling
    if ('serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype) {
      await registration.sync.register('background-sync-notifications')
    }
    
    // Configurar polling personalizado en el service worker
    await setupServiceWorkerPolling(registration)
    
    console.log('✅ Push notifications configuradas para funcionamiento en segundo plano')
    return true
  } catch (error) {
    console.error('❌ Error configurando push notifications:', error)
    return false
  }
}

// NUEVO: Generar clave VAPID básica (para demo, en producción usar clave del servidor)
const generateVAPIDKey = () => {
  // Clave VAPID de ejemplo (en producción debe venir del servidor)
  const publicVapidKey = 'BCOlp6JlNfVlK1PTDX8Tth7hCNz_W5OWpRBb0F7N1E_rKxDfYLpHPF9KGQcA8KhJQ9yL3Tpb7XGbDXZ5FcD2kJw'
  
  function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4)
    const base64 = (base64String + padding)
      .replace(/\-/g, '+')
      .replace(/_/g, '/')
    
    const rawData = window.atob(base64)
    const outputArray = new Uint8Array(rawData.length)
    
    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i)
    }
    return outputArray
  }
  
  return urlBase64ToUint8Array(publicVapidKey)
}

// NUEVO: Enviar suscripción al servidor (opcional)
const sendSubscriptionToServer = async (subscription) => {
  try {
    const userId = getUserId()
    if (!userId) return
    
    // Aquí se enviaría la suscripción al backend para enviar push notifications
    console.log('📤 Enviando suscripción push al servidor:', {
      userId,
      endpoint: subscription.endpoint,
      keys: subscription.keys
    })
    
    // En el futuro, enviar al endpoint del backend:
    // await fetch('/api/push-subscription', {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ userId, subscription })
    // })
    
  } catch (error) {
    console.warn('⚠️ Error enviando suscripción al servidor:', error)
  }
}

// NUEVO: Configurar polling en Service Worker
const setupServiceWorkerPolling = async (registration) => {
  try {
    // Enviar mensaje al Service Worker para iniciar polling en segundo plano
    if (registration.active) {
      const userId = getUserId()
      const apiUrl = import.meta.env.PROD 
        ? 'https://apipwa.sembrandodatos.com' 
        : 'http://localhost:8000'
      
      registration.active.postMessage({
        type: 'START_BACKGROUND_NOTIFICATIONS_POLLING',
        userId: userId,
        apiUrl: apiUrl,
        interval: 8000 // Muy agresivo: cada 8 segundos para garantizar recepción
      })
      
      console.log('📡 Polling de notificaciones configurado en Service Worker')
    }
  } catch (error) {
    console.warn('⚠️ Error configurando polling en Service Worker:', error)
  }
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
    
    // NUEVOS: Métodos de sonido y push notifications
    enableSound,
    disableSound,
    playTestSound,
    requestNotificationPermission,
    initializeGlobalAudio,
    setupPushNotifications,
    
    // Estado global (solo lectura)
    state: globalNotificationState
  }
}

export default useNotifications
