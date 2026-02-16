/**
 * pushNotificationsService.js
 * Servicio para manejar Web Push Notifications en PWASUPER
 * Versión: 1.0.0
 */

// Configuración de la API
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://apipwa.sembrandodatos.com' 
  : 'http://localhost:8000'

/**
 * Convierte una clave VAPID base64 a Uint8Array
 * Necesario para la API de Push del navegador
 */
function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4)
  const base64 = (base64String + padding)
    .replace(/-/g, '+')
    .replace(/_/g, '/')
  
  const rawData = window.atob(base64)
  const outputArray = new Uint8Array(rawData.length)
  
  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i)
  }
  
  return outputArray
}

/**
 * Obtiene información del dispositivo/navegador
 */
function getDeviceInfo() {
  const ua = navigator.userAgent
  let browser = 'unknown'
  let os = 'unknown'
  
  // Detectar navegador
  if (ua.includes('Chrome')) browser = 'Chrome'
  else if (ua.includes('Firefox')) browser = 'Firefox'
  else if (ua.includes('Safari')) browser = 'Safari'
  else if (ua.includes('Edge')) browser = 'Edge'
  
  // Detectar OS
  if (ua.includes('Android')) os = 'Android'
  else if (ua.includes('iPhone') || ua.includes('iPad')) os = 'iOS'
  else if (ua.includes('Windows')) os = 'Windows'
  else if (ua.includes('Mac')) os = 'macOS'
  else if (ua.includes('Linux')) os = 'Linux'
  
  return {
    browser,
    os,
    userAgent: ua.substring(0, 150),
    language: navigator.language,
    platform: navigator.platform,
    timestamp: new Date().toISOString()
  }
}

export const pushNotificationsService = {
  /**
   * Estado actual del servicio
   */
  _state: {
    supported: false,
    permission: 'default',
    subscribed: false,
    subscription: null,
    vapidPublicKey: null,
    initialized: false
  },

  /**
   * Verificar si el navegador soporta Push Notifications
   */
  isSupported() {
    return 'serviceWorker' in navigator && 
           'PushManager' in window && 
           'Notification' in window
  },

  /**
   * Obtener el estado actual del permiso de notificaciones
   */
  getPermissionStatus() {
    if (!('Notification' in window)) {
      return 'unsupported'
    }
    return Notification.permission
  },

  /**
   * Inicializar el servicio de push notifications
   */
  async initialize() {
    console.log('🔔 Inicializando servicio de Push Notifications...')
    
    if (!this.isSupported()) {
      console.warn('⚠️ Push Notifications no soportadas en este navegador')
      this._state.supported = false
      return { success: false, reason: 'not_supported' }
    }
    
    this._state.supported = true
    this._state.permission = this.getPermissionStatus()
    
    try {
      // Obtener la clave pública VAPID del servidor
      const response = await fetch(`${API_BASE_URL}/push/vapid-public-key`)
      
      if (!response.ok) {
        throw new Error('No se pudo obtener la clave VAPID')
      }
      
      const data = await response.json()
      this._state.vapidPublicKey = data.publicKey
      this._state.initialized = true
      
      console.log('✅ Servicio de Push Notifications inicializado')
      console.log('📋 Estado de permisos:', this._state.permission)
      
      return { 
        success: true, 
        permission: this._state.permission,
        canSubscribe: this._state.permission !== 'denied'
      }
      
    } catch (error) {
      console.error('❌ Error inicializando push notifications:', error)
      return { success: false, error: error.message }
    }
  },

  /**
   * Solicitar permiso para notificaciones
   */
  async requestPermission() {
    console.log('🔔 Solicitando permiso de notificaciones...')
    
    if (!this._state.supported) {
      return { success: false, reason: 'not_supported' }
    }
    
    try {
      const permission = await Notification.requestPermission()
      this._state.permission = permission
      
      console.log('📋 Resultado del permiso:', permission)
      
      return {
        success: permission === 'granted',
        permission: permission,
        message: permission === 'granted' 
          ? 'Permisos concedidos' 
          : permission === 'denied' 
            ? 'Permisos denegados por el usuario'
            : 'El usuario no respondió'
      }
      
    } catch (error) {
      console.error('❌ Error solicitando permiso:', error)
      return { success: false, error: error.message }
    }
  },

  /**
   * Suscribirse a Push Notifications
   * @param {number} usuarioId - ID del usuario a suscribir
   */
  async subscribe(usuarioId) {
    console.log('🔔 Suscribiendo a Push Notifications para usuario:', usuarioId)
    
    if (!this._state.supported) {
      return { success: false, reason: 'not_supported' }
    }
    
    if (!this._state.initialized) {
      await this.initialize()
    }
    
    if (this._state.permission !== 'granted') {
      const permResult = await this.requestPermission()
      if (!permResult.success) {
        return permResult
      }
    }
    
    try {
      // Obtener el Service Worker registration
      const registration = await navigator.serviceWorker.ready
      
      // Verificar si ya hay una suscripción
      let subscription = await registration.pushManager.getSubscription()
      
      if (!subscription) {
        // Crear nueva suscripción
        console.log('📝 Creando nueva suscripción push...')
        
        subscription = await registration.pushManager.subscribe({
          userVisibleOnly: true,
          applicationServerKey: urlBase64ToUint8Array(this._state.vapidPublicKey)
        })
      }
      
      // Extraer datos de la suscripción
      const subscriptionJson = subscription.toJSON()
      const p256dh = subscriptionJson.keys.p256dh
      const auth = subscriptionJson.keys.auth
      
      console.log('📤 Registrando suscripción en el servidor...')
      
      // Enviar al servidor
      const response = await fetch(`${API_BASE_URL}/push/subscribe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          usuario_id: usuarioId,
          endpoint: subscription.endpoint,
          p256dh: p256dh,
          auth: auth,
          device_info: getDeviceInfo()
        })
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Error registrando suscripción')
      }
      
      const data = await response.json()
      
      this._state.subscribed = true
      this._state.subscription = subscription
      
      console.log('✅ Suscripción registrada exitosamente:', data.subscription_id)
      
      // Guardar estado en localStorage
      localStorage.setItem('push_subscribed', 'true')
      localStorage.setItem('push_subscription_id', data.subscription_id)
      
      return {
        success: true,
        subscription_id: data.subscription_id,
        message: '¡Notificaciones push activadas!'
      }
      
    } catch (error) {
      console.error('❌ Error en suscripción push:', error)
      return { success: false, error: error.message }
    }
  },

  /**
   * Cancelar suscripción de Push Notifications
   */
  async unsubscribe() {
    console.log('🔕 Cancelando suscripción push...')
    
    try {
      const registration = await navigator.serviceWorker.ready
      const subscription = await registration.pushManager.getSubscription()
      
      if (!subscription) {
        console.log('⚠️ No hay suscripción activa')
        return { success: true, message: 'No había suscripción activa' }
      }
      
      // Cancelar en el servidor
      const response = await fetch(`${API_BASE_URL}/push/unsubscribe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          endpoint: subscription.endpoint
        })
      })
      
      // Cancelar localmente
      await subscription.unsubscribe()
      
      this._state.subscribed = false
      this._state.subscription = null
      
      // Limpiar localStorage
      localStorage.removeItem('push_subscribed')
      localStorage.removeItem('push_subscription_id')
      
      console.log('✅ Suscripción cancelada')
      
      return { success: true, message: 'Suscripción cancelada' }
      
    } catch (error) {
      console.error('❌ Error cancelando suscripción:', error)
      return { success: false, error: error.message }
    }
  },

  /**
   * Verificar si el usuario está suscrito
   */
  async checkSubscription() {
    if (!this._state.supported) {
      return { subscribed: false, reason: 'not_supported' }
    }
    
    try {
      const registration = await navigator.serviceWorker.ready
      const subscription = await registration.pushManager.getSubscription()
      
      this._state.subscribed = !!subscription
      this._state.subscription = subscription
      
      return {
        subscribed: !!subscription,
        endpoint: subscription?.endpoint?.substring(0, 50) + '...'
      }
      
    } catch (error) {
      console.error('❌ Error verificando suscripción:', error)
      return { subscribed: false, error: error.message }
    }
  },

  /**
   * Enviar notificación de prueba
   * @param {number} usuarioId - ID del usuario
   */
  async sendTestNotification(usuarioId) {
    console.log('🧪 Enviando notificación de prueba...')
    
    try {
      const response = await fetch(`${API_BASE_URL}/push/send-test/${usuarioId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      
      const data = await response.json()
      
      if (data.success) {
        console.log('✅ Notificación de prueba enviada')
        return { success: true, message: 'Notificación enviada' }
      } else {
        console.warn('⚠️ No se pudo enviar:', data.message)
        return { success: false, message: data.message }
      }
      
    } catch (error) {
      console.error('❌ Error enviando prueba:', error)
      return { success: false, error: error.message }
    }
  },

  /**
   * Mostrar notificación local (sin push)
   */
  async showLocalNotification(title, options = {}) {
    if (this._state.permission !== 'granted') {
      await this.requestPermission()
    }
    
    if (this._state.permission !== 'granted') {
      console.warn('⚠️ Sin permiso para notificaciones')
      return { success: false, reason: 'permission_denied' }
    }
    
    try {
      const registration = await navigator.serviceWorker.ready
      
      await registration.showNotification(title, {
        body: options.body || '',
        icon: options.icon || '/pwa-192x192.png',
        badge: '/pwa-192x192.png',
        tag: options.tag || `local-${Date.now()}`,
        data: options.data || {},
        vibrate: options.vibrate || [100, 50, 100],
        requireInteraction: options.requireInteraction || false,
        ...options
      })
      
      return { success: true }
      
    } catch (error) {
      console.error('❌ Error mostrando notificación local:', error)
      return { success: false, error: error.message }
    }
  },

  /**
   * Obtener el estado completo del servicio
   */
  getState() {
    return { ...this._state }
  },

  /**
   * Escuchar mensajes del Service Worker
   */
  setupMessageListener(callback) {
    if (!('serviceWorker' in navigator)) {
      return
    }
    
    navigator.serviceWorker.addEventListener('message', (event) => {
      console.log('📨 Mensaje del SW:', event.data)
      
      if (callback && typeof callback === 'function') {
        callback(event.data)
      }
    })
  }
}

export default pushNotificationsService
