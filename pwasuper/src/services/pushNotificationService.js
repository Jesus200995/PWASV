/**
 * Servicio para manejar notificaciones push REALES en PWASUPER
 * Incluye VAPID keys, suscripciones del servidor y push notifications reales
 */

class PushNotificationService {
  constructor() {
    this.swRegistration = null
    this.isSupported = false
    this.subscription = null
    this.vapidPublicKey = null
    this.apiUrl = import.meta.env.PROD ? 'https://apipwa.sembrandodatos.com' : 'http://localhost:8000'
    
    this.checkSupport()
  }

  /**
   * Verificar soporte para notificaciones push
   */
  checkSupport() {
    if ('serviceWorker' in navigator && 'PushManager' in window && 'Notification' in window) {
      this.isSupported = true
      console.log('✅ Push notifications soportadas')
    } else {
      this.isSupported = false
      console.warn('❌ Push notifications no soportadas en este navegador')
    }
  }

  /**
   * Obtener la clave pública VAPID del servidor
   */
  async getVapidPublicKey() {
    try {
      const response = await fetch(`${this.apiUrl}/vapid/public-key`)
      if (!response.ok) {
        throw new Error(`Error obteniendo clave VAPID: ${response.status}`)
      }
      
      const data = await response.json()
      this.vapidPublicKey = data.public_key
      
      console.log('🔑 Clave VAPID obtenida exitosamente')
      return this.vapidPublicKey
    } catch (error) {
      console.error('❌ Error obteniendo clave VAPID:', error)
      throw error
    }
  }

  /**
   * Convertir clave VAPID base64 a Uint8Array
   */
  urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4)
    const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/')
    
    const rawData = window.atob(base64)
    const outputArray = new Uint8Array(rawData.length)
    
    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i)
    }
    return outputArray
  }

  /**
   * Registrar el Service Worker
   */
  async registerServiceWorker() {
    try {
      console.log('🔧 Registrando Service Worker...')
      
      const registration = await navigator.serviceWorker.register('/sw.js')
      this.swRegistration = registration
      
      console.log('✅ Service Worker registrado:', registration)
      return registration
    } catch (error) {
      console.error('❌ Error registrando Service Worker:', error)
      throw error
    }
  }

  /**
   * Solicitar permisos para notificaciones
   */
  async requestNotificationPermission() {
    try {
      console.log('🔔 Solicitando permisos de notificación...')
      
      // Verificar si ya tenemos permisos
      if (Notification.permission === 'granted') {
        console.log('✅ Permisos ya concedidos')
        return true
      }

      // Solicitar permisos
      const permission = await Notification.requestPermission()
      
      console.log('🔔 Resultado de permisos:', permission)
      
      if (permission === 'granted') {
        console.log('✅ Permisos concedidos')
        
        // Mostrar notificación de confirmación
        this.showLocalNotification(
          'Notificaciones activadas ✅',
          'Ahora recibirás notificaciones push automáticamente, incluso cuando la aplicación esté cerrada',
          { tag: 'permission-granted' }
        )
        
        return true
      } else if (permission === 'denied') {
        console.warn('❌ Permisos denegados por el usuario')
        throw new Error('Permisos de notificación denegados. Para activarlos, ve a la configuración del navegador.')
      } else {
        console.warn('⏸️ Permisos pendientes de decisión')
        throw new Error('Permisos de notificación pendientes')
      }
    } catch (error) {
      console.error('❌ Error solicitando permisos:', error)
      throw error
    }
  }

  /**
   * Suscribirse a notificaciones push REALES con VAPID
   */
  async subscribeToPush(usuarioId) {
    try {
      if (!this.swRegistration) {
        throw new Error('Service Worker no registrado')
      }

      console.log('📡 Suscribiéndose a push notifications REALES...')

      // Obtener clave VAPID si no la tenemos
      if (!this.vapidPublicKey) {
        await this.getVapidPublicKey()
      }

      // Convertir clave VAPID a Uint8Array
      const applicationServerKey = this.urlBase64ToUint8Array(this.vapidPublicKey)

      // Configuración de la suscripción
      const subscribeOptions = {
        userVisibleOnly: true,
        applicationServerKey: applicationServerKey
      }

      const subscription = await this.swRegistration.pushManager.subscribe(subscribeOptions)
      this.subscription = subscription

      console.log('✅ Suscripción push exitosa:', subscription)

      // Extraer claves de la suscripción
      const p256dh = btoa(String.fromCharCode(...new Uint8Array(subscription.getKey('p256dh'))))
      const auth = btoa(String.fromCharCode(...new Uint8Array(subscription.getKey('auth'))))

      // Detectar información del dispositivo
      const userAgent = navigator.userAgent
      const dispositivo = /Mobile|Android|iPhone|iPad/.test(userAgent) ? 'móvil' : 'escritorio'

      // Enviar suscripción al backend
      const subscriptionData = {
        usuario_id: usuarioId,
        endpoint: subscription.endpoint,
        p256dh: p256dh,
        auth: auth,
        user_agent: userAgent,
        dispositivo: dispositivo
      }

      const response = await fetch(`${this.apiUrl}/push/subscribe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(subscriptionData)
      })

      if (!response.ok) {
        throw new Error(`Error enviando suscripción al servidor: ${response.status}`)
      }

      const result = await response.json()
      console.log('✅ Suscripción registrada en el servidor:', result)

      return subscription
    } catch (error) {
      console.error('❌ Error en suscripción push:', error)
      throw error
    }
  }

  /**
   * Cancelar suscripción push
   */
  async unsubscribeFromPush(usuarioId) {
    try {
      if (this.subscription) {
        // Cancelar en el navegador
        await this.subscription.unsubscribe()
        
        // Cancelar en el servidor
        const response = await fetch(`${this.apiUrl}/push/unsubscribe/${usuarioId}?endpoint=${encodeURIComponent(this.subscription.endpoint)}`, {
          method: 'DELETE'
        })
        
        if (!response.ok) {
          console.warn('⚠️ Error cancelando en el servidor, pero suscripción local cancelada')
        }
        
        this.subscription = null
        console.log('✅ Suscripción push cancelada')
      }
    } catch (error) {
      console.error('❌ Error cancelando suscripción:', error)
      throw error
    }
  }

  /**
   * Mostrar notificación local (sin servidor push)
   */
  showLocalNotification(title, body, options = {}) {
    if (Notification.permission === 'granted') {
      const notification = new Notification(title, {
        body,
        icon: '/pwa-192x192.png',
        badge: '/pwa-192x192.png',
        ...options
      })

      // Auto cerrar después de 5 segundos
      setTimeout(() => {
        notification.close()
      }, 5000)

      return notification
    } else {
      console.warn('⚠️ No hay permisos para mostrar notificación')
      return null
    }
  }

  /**
   * Simular notificación push de nueva notificación (FALLBACK)
   */
  simulatePushNotification(notificacion) {
    if (Notification.permission === 'granted') {
      const options = {
        body: notificacion.subtitulo || notificacion.descripcion,
        icon: '/pwa-192x192.png',
        badge: '/pwa-192x192.png',
        tag: `notification-${notificacion.id}`,
        data: {
          notificacionId: notificacion.id,
          url: '/notificaciones',
          timestamp: Date.now()
        },
        vibrate: [200, 100, 200],
        requireInteraction: true // Mantener visible hasta que el usuario interactúe
      }

      const notification = new Notification(notificacion.titulo, options)

      // Manejar click en la notificación
      notification.onclick = () => {
        window.focus()
        // Navegar a notificaciones si es posible
        if (window.location.pathname !== '/notificaciones') {
          window.location.href = '/notificaciones'
        }
        notification.close()
      }

      return notification
    }
    return null
  }

  /**
   * Configurar polling para nuevas notificaciones (FALLBACK si push no funciona)
   */
  startNotificationPolling(usuarioId, interval = 5 * 60 * 1000) { // 5 minutos por defecto
    console.log(`🔄 Iniciando polling cada ${interval/1000}s para usuario ${usuarioId}`)
    
    // Guardar timestamp de la última verificación
    let lastCheck = Date.now()
    
    const checkForNewNotifications = async () => {
      try {
        console.log('🔍 Verificando nuevas notificaciones...')
        
        // Importar el servicio (asumiendo que está disponible globalmente)
        const notificacionesService = window.notificacionesService
        if (!notificacionesService) return

        // Obtener notificaciones recientes
        const response = await notificacionesService.obtenerNotificacionesUsuario(usuarioId, 5, 0)
        const notificaciones = response.notificaciones || []
        
        // Filtrar notificaciones nuevas desde la última verificación
        const nuevas = notificaciones.filter(notif => {
          const fechaNotif = new Date(notif.fecha_creacion).getTime()
          return fechaNotif > lastCheck
        })
        
        if (nuevas.length > 0) {
          console.log(`🆕 ${nuevas.length} notificaciones nuevas encontradas`)
          
          // Mostrar notificación push para cada nueva (FALLBACK)
          nuevas.forEach(notif => {
            setTimeout(() => {
              this.simulatePushNotification(notif)
            }, 1000) // Delay entre notificaciones
          })
        } else {
          console.log('📝 No hay notificaciones nuevas')
        }
        
        lastCheck = Date.now()
      } catch (error) {
        console.error('❌ Error verificando notificaciones:', error)
      }
    }
    
    // Verificación inicial
    checkForNewNotifications()
    
    // Configurar intervalo
    const intervalId = setInterval(checkForNewNotifications, interval)
    
    // Retornar función para cancelar
    return () => {
      clearInterval(intervalId)
      console.log('🛑 Polling de notificaciones detenido')
    }
  }

  /**
   * Configuración completa en un solo método
   */
  async setupPushNotifications(usuarioId) {
    try {
      console.log('🚀 Configurando push notifications REALES completas...')
      
      if (!this.isSupported) {
        throw new Error('Push notifications no soportadas')
      }
      
      // 1. Registrar Service Worker
      await this.registerServiceWorker()
      
      // 2. Solicitar permisos
      await this.requestNotificationPermission()
      
      // 3. Suscribirse a push REALES con VAPID
      let pushSubscriptionSuccess = false
      try {
        await this.subscribeToPush(usuarioId)
        pushSubscriptionSuccess = true
        console.log('✅ Push notifications REALES configuradas')
      } catch (error) {
        console.warn('⚠️ Suscripción push real falló, activando fallback:', error.message)
      }
      
      // 4. Iniciar polling como respaldo (opcional)
      let stopPolling = null
      if (!pushSubscriptionSuccess) {
        stopPolling = this.startNotificationPolling(usuarioId)
        console.log('📡 Modo fallback activado con polling')
      }
      
      console.log('✅ Push notifications configuradas completamente')
      
      return {
        success: true,
        hasPermissions: true,
        realPushEnabled: pushSubscriptionSuccess,
        fallbackEnabled: !pushSubscriptionSuccess,
        stopPolling
      }
    } catch (error) {
      console.error('❌ Error en configuración completa:', error)
      return {
        success: false,
        error: error.message,
        hasPermissions: false,
        realPushEnabled: false,
        fallbackEnabled: false
      }
    }
  }

  /**
   * Enviar notificación de prueba
   */
  async sendTestNotification(usuarioId) {
    try {
      const response = await fetch(`${this.apiUrl}/push/test/${usuarioId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: 'Prueba de Push Notification 🧪',
          body: 'Si ves esta notificación, ¡el sistema está funcionando correctamente!',
          icon: '/pwa-192x192.png',
          tag: 'test-notification'
        })
      })

      if (!response.ok) {
        throw new Error(`Error enviando prueba: ${response.status}`)
      }

      const result = await response.json()
      console.log('✅ Notificación de prueba enviada:', result)
      return result
    } catch (error) {
      console.error('❌ Error enviando notificación de prueba:', error)
      throw error
    }
  }

  /**
   * Verificar estado actual
   */
  getStatus() {
    return {
      supported: this.isSupported,
      permission: Notification.permission,
      serviceWorkerRegistered: !!this.swRegistration,
      subscribed: !!this.subscription,
      hasVapidKey: !!this.vapidPublicKey
    }
  }
}

// Crear instancia global
const pushNotificationService = new PushNotificationService()

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {
  module.exports = pushNotificationService
} else {
  // Hacer disponible globalmente
  window.pushNotificationService = pushNotificationService
}

export default pushNotificationService
