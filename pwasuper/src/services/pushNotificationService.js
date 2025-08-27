/**
 * Servicio para manejar notificaciones push en la PWA
 */

class PushNotificationService {
  constructor() {
    this.registration = null;
    this.subscription = null;
    this.vapidPublicKey = null; // Se configurará desde el servidor
    this.isSupported = this.checkSupport();
  }

  /**
   * Verificar si las notificaciones push son soportadas
   */
  checkSupport() {
    return (
      'serviceWorker' in navigator &&
      'PushManager' in window &&
      'Notification' in window
    );
  }

  /**
   * Inicializar el servicio de push notifications
   */
  async init() {
    if (!this.isSupported) {
      console.warn('❌ Notificaciones push no soportadas en este navegador');
      return false;
    }

    try {
      // Registrar o obtener el service worker
      this.registration = await navigator.serviceWorker.ready;
      console.log('✅ Service Worker listo para notificaciones push');
      
      // Obtener configuración VAPID del servidor
      await this.loadVapidKey();
      
      return true;
    } catch (error) {
      console.error('❌ Error inicializando push notifications:', error);
      return false;
    }
  }

  /**
   * Cargar la clave pública VAPID desde el servidor
   */
  async loadVapidKey() {
    try {
      console.log('🔧 Cargando clave VAPID del servidor...');
      
      // Intentar obtener del servidor primero
      const apiBaseUrl = import.meta.env.PROD 
        ? 'https://apipwa.sembrandodatos.com' 
        : 'http://localhost:8000';
      
      try {
        const response = await fetch(`${apiBaseUrl}/api/vapid-public-key`);
        if (response.ok) {
          const data = await response.json();
          this.vapidPublicKey = data.publicKey;
          console.log('✅ Clave VAPID obtenida del servidor');
          return;
        }
      } catch (serverError) {
        console.warn('⚠️ No se pudo conectar al servidor para obtener clave VAPID');
      }

      // En desarrollo o si falla el servidor, usar clave local
      if (import.meta.env.DEV) {
        // Usar la misma clave que está en el servidor
        this.vapidPublicKey = 'BK2xdNLfyiFTLYObswC7XFi2ZFqU_VDqkteuiVxiPpJP6vzI6bvwL5xGB0ovqVpvngpQ8SdX1kF_eR3QsblHeN4';
        console.log('🔧 Usando clave VAPID de desarrollo');
        return;
      }

      throw new Error('No se pudo obtener la clave VAPID');
      
    } catch (error) {
      console.error('❌ Error cargando clave VAPID:', error);
      // Usar clave de respaldo
      this.vapidPublicKey = 'BK2xdNLfyiFTLYObswC7XFi2ZFqU_VDqkteuiVxiPpJP6vzI6bvwL5xGB0ovqVpvngpQ8SdX1kF_eR3QsblHeN4';
      console.log('🔧 Usando clave VAPID de respaldo');
    }
  }

  /**
   * Solicitar permisos para notificaciones
   */
  async requestPermission() {
    if (!this.isSupported) {
      throw new Error('Notificaciones no soportadas');
    }

    // Verificar estado actual del permiso
    let permission = Notification.permission;

    if (permission === 'default') {
      // Solicitar permiso
      permission = await Notification.requestPermission();
    }

    if (permission === 'granted') {
      console.log('✅ Permisos de notificación concedidos');
      return true;
    } else if (permission === 'denied') {
      console.warn('❌ Permisos de notificación denegados');
      throw new Error('Permisos de notificación denegados. Habilítalos en la configuración del navegador.');
    } else {
      console.warn('⚠️ Permisos de notificación no concedidos');
      return false;
    }
  }

  /**
   * Suscribirse a notificaciones push
   */
  async subscribe(usuarioId) {
    if (!this.isSupported || !this.registration) {
      throw new Error('Push notifications no disponibles');
    }

    if (!this.vapidPublicKey) {
      await this.loadVapidKey();
    }

    try {
      // Verificar permisos
      const hasPermission = await this.requestPermission();
      if (!hasPermission) {
        throw new Error('Sin permisos para notificaciones');
      }

      // Verificar si ya hay una suscripción
      this.subscription = await this.registration.pushManager.getSubscription();
      
      if (this.subscription) {
        console.log('✅ Ya hay una suscripción activa');
        // Enviar al servidor para actualizar
        await this.sendSubscriptionToServer(usuarioId, this.subscription);
        return this.subscription;
      }

      // Validar que tenemos la clave VAPID
      if (!this.vapidPublicKey) {
        console.log('🔄 Cargando clave VAPID...');
        await this.loadVapidKey();
      }

      if (!this.vapidPublicKey) {
        throw new Error('No se pudo obtener la clave VAPID del servidor');
      }

      console.log('🔐 Usando clave VAPID:', this.vapidPublicKey);

      // Convertir la clave VAPID
      let applicationServerKey;
      try {
        applicationServerKey = this.urlBase64ToUint8Array(this.vapidPublicKey);
        console.log('✅ Clave VAPID convertida correctamente');
      } catch (keyError) {
        console.error('❌ Error convirtiendo clave VAPID:', keyError);
        throw new Error('Clave VAPID inválida: ' + keyError.message);
      }

      // Crear nueva suscripción
      console.log('📝 Creando nueva suscripción push...');
      this.subscription = await this.registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: applicationServerKey
      });

      console.log('✅ Nueva suscripción push creada exitosamente');

      // Enviar al servidor
      await this.sendSubscriptionToServer(usuarioId, this.subscription);
      
      return this.subscription;

    } catch (error) {
      console.error('❌ Error detallado en suscripción push:', error);
      console.error('Stack:', error.stack);
      throw error;
    }
  }

  /**
   * Desuscribirse de notificaciones push
   */
  async unsubscribe(usuarioId) {
    try {
      if (this.subscription) {
        await this.subscription.unsubscribe();
        console.log('✅ Desuscripción exitosa');
        
        // Notificar al servidor
        await this.removeSubscriptionFromServer(usuarioId);
        
        this.subscription = null;
        return true;
      }
      return false;
    } catch (error) {
      console.error('❌ Error desuscribiendo:', error);
      throw error;
    }
  }

  /**
   * Enviar suscripción al servidor
   */
  async sendSubscriptionToServer(usuarioId, subscription) {
    try {
      const subscriptionData = {
        usuario_id: usuarioId,
        endpoint: subscription.endpoint,
        keys: {
          p256dh: btoa(String.fromCharCode.apply(null, new Uint8Array(subscription.getKey('p256dh')))),
          auth: btoa(String.fromCharCode.apply(null, new Uint8Array(subscription.getKey('auth'))))
        },
        userAgent: navigator.userAgent,
        deviceInfo: {
          type: 'mobile', // Detectar tipo de dispositivo
          platform: navigator.platform
        }
      };

      console.log('📤 Enviando suscripción al servidor:', subscriptionData);

      // En desarrollo, usar servidor local
      const apiBaseUrl = import.meta.env.PROD 
        ? 'https://apipwa.sembrandodatos.com' 
        : 'http://localhost:8000';

      const response = await fetch(`${apiBaseUrl}/api/push/subscribe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(subscriptionData)
      });

      if (!response.ok) {
        const errorData = await response.text();
        throw new Error(`Error del servidor (${response.status}): ${errorData}`);
      }

      const result = await response.json();
      console.log('✅ Suscripción enviada al servidor exitosamente:', result);

    } catch (error) {
      console.error('❌ Error enviando suscripción al servidor:', error);
      
      // En desarrollo, guardar localmente como fallback
      if (import.meta.env.DEV && error.message.includes('Failed to fetch')) {
        console.log('🔧 Modo desarrollo - guardando suscripción localmente como fallback');
        localStorage.setItem('pushSubscription', JSON.stringify(subscriptionData));
        return;
      }
      
      throw error;
    }
  }

  /**
   * Remover suscripción del servidor
   */
  async removeSubscriptionFromServer(usuarioId) {
    try {
      // En desarrollo, remover del localStorage
      if (import.meta.env.DEV) {
        console.log('🔧 Modo desarrollo - removiendo suscripción localmente');
        localStorage.removeItem('pushSubscription');
      }

      // Intentar remover del servidor siempre
      const apiBaseUrl = import.meta.env.PROD 
        ? 'https://apipwa.sembrandodatos.com' 
        : 'http://localhost:8000';

      const response = await fetch(`${apiBaseUrl}/api/push/unsubscribe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ usuario_id: usuarioId })
      });

      if (response.ok) {
        console.log('✅ Suscripción removida del servidor');
      } else {
        console.warn('⚠️ No se pudo remover del servidor, pero se removió localmente');
      }

    } catch (error) {
      console.error('❌ Error removiendo suscripción del servidor:', error);
      // No lanzar error, ya que se removió localmente
    }
  }

  /**
   * Verificar estado de suscripción
   */
  async getSubscriptionStatus() {
    if (!this.isSupported || !this.registration) {
      return {
        supported: false,
        permission: 'default',
        subscribed: false
      };
    }

    const subscription = await this.registration.pushManager.getSubscription();
    
    return {
      supported: this.isSupported,
      permission: Notification.permission,
      subscribed: !!subscription,
      subscription: subscription
    };
  }

  /**
   * Mostrar notificación de prueba
   */
  async showTestNotification() {
    if (Notification.permission === 'granted') {
      new Notification('Notificación de prueba', {
        body: 'Las notificaciones push están funcionando correctamente',
        icon: '/pwa-192x192.png',
        badge: '/pwa-192x192.png',
        vibrate: [200, 100, 200]
      });
    }
  }

  /**
   * Convertir clave VAPID a formato Uint8Array
   */
  urlBase64ToUint8Array(base64String) {
    // Limpiar la cadena y agregar padding si es necesario
    const cleanBase64 = base64String.replace(/[^A-Za-z0-9+/]/g, '');
    const padding = '='.repeat((4 - cleanBase64.length % 4) % 4);
    const base64 = (cleanBase64 + padding)
      .replace(/\-/g, '+')
      .replace(/_/g, '/');

    try {
      const rawData = window.atob(base64);
      const outputArray = new Uint8Array(rawData.length);

      for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
      }
      return outputArray;
    } catch (error) {
      console.error('❌ Error decodificando clave VAPID:', error);
      console.error('Clave problemática:', base64String);
      
      // Intentar decodificación alternativa para claves URL-safe
      try {
        const urlSafeBase64 = base64String
          .replace(/\-/g, '+')
          .replace(/_/g, '/');
        const padding = '='.repeat((4 - urlSafeBase64.length % 4) % 4);
        const finalBase64 = urlSafeBase64 + padding;
        
        const rawData = window.atob(finalBase64);
        const outputArray = new Uint8Array(rawData.length);
        
        for (let i = 0; i < rawData.length; ++i) {
          outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
      } catch (secondError) {
        console.error('❌ Error en decodificación alternativa:', secondError);
        throw new Error('No se pudo decodificar la clave VAPID');
      }
    }
  }

  /**
   * Configurar listener para mensajes del service worker
   */
  setupMessageListener() {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.addEventListener('message', (event) => {
        if (event.data.type === 'NAVIGATE_TO_NOTIFICATIONS') {
          console.log('📱 Navegando a notificaciones desde push notification');
          // Aquí se puede implementar navegación programática
          // Por ejemplo, usando el router de Vue
          window.location.href = '/notificaciones';
        }
      });
    }
  }

  /**
   * Obtener información del dispositivo para debugging
   */
  getDeviceInfo() {
    return {
      userAgent: navigator.userAgent,
      platform: navigator.platform,
      language: navigator.language,
      onLine: navigator.onLine,
      serviceWorkerSupported: 'serviceWorker' in navigator,
      pushManagerSupported: 'PushManager' in window,
      notificationSupported: 'Notification' in window,
      permission: Notification.permission
    };
  }
}

// Crear instancia singleton
export const pushNotificationService = new PushNotificationService();

export default pushNotificationService;
