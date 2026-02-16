import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Importar estilos (Tailwind CSS y personalizados)
import './style.css'

// Importar Font Awesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faHeadset, faUserGear, faCommentDots, faHeadphones } from '@fortawesome/free-solid-svg-icons'

// Agregar iconos a la librería
library.add(faHeadset, faUserGear, faCommentDots, faHeadphones)

// Importar Leaflet CSS globalmente
import 'leaflet/dist/leaflet.css'

// Corregir el problema del ícono de Leaflet
import { Icon } from 'leaflet'
delete Icon.Default.prototype._getIconUrl
Icon.Default.mergeOptions({
  iconRetinaUrl: '/leaflet/marker-icon-2x.png',
  iconUrl: '/leaflet/marker-icon.png',
  shadowUrl: '/leaflet/marker-shadow.png',
})

// Importar utilidad de registro del Service Worker
import { registerServiceWorker, waitForServiceWorkerReady } from './utils/serviceWorkerRegistration.js'

// Importar composable de notificaciones para inicialización global
import { useNotifications } from './composables/useNotifications.js'

// Importar servicio de Push Notifications
import { pushNotificationsService } from './services/pushNotificationsService.js'

// Registrar el Service Worker para funcionalidad PWA offline
window.addEventListener('load', async () => {
  try {
    // Registrar el service worker
    const registration = await registerServiceWorker();
    
    // Esperar a que el service worker esté listo
    await waitForServiceWorkerReady();
    
    console.log('✅ Aplicación lista con soporte offline');
    
    // ═══════════════════════════════════════════════════════════════════
    // INICIALIZACIÓN DE PUSH NOTIFICATIONS
    // ═══════════════════════════════════════════════════════════════════
    
    // Inicializar el servicio de push notifications
    const pushResult = await pushNotificationsService.initialize()
    console.log('🔔 Push Notifications:', pushResult.success ? 'Inicializado' : 'No disponible')
    
    // Si el usuario ya tiene sesión, intentar suscribirse automáticamente
    const userData = localStorage.getItem('user')
    if (userData && pushResult.success) {
      try {
        const user = JSON.parse(userData)
        const userId = user.id || user.usuario_id
        
        if (userId) {
          // Verificar si ya está suscrito
          const subCheck = await pushNotificationsService.checkSubscription()
          
          if (!subCheck.subscribed) {
            // Intentar suscribir automáticamente
            console.log('🔔 Intentando suscripción automática para usuario:', userId)
            const subResult = await pushNotificationsService.subscribe(userId)
            
            if (subResult.success) {
              console.log('✅ Usuario suscrito a push notifications automáticamente')
            } else {
              console.log('⚠️ No se pudo suscribir automáticamente:', subResult.reason || subResult.error)
            }
          } else {
            console.log('✅ Usuario ya está suscrito a push notifications')
          }
        }
      } catch (e) {
        console.warn('⚠️ Error verificando suscripción push:', e)
      }
    }
    
    // Configurar listener para mensajes del SW (push recibido, etc.)
    pushNotificationsService.setupMessageListener((data) => {
      if (data.type === 'PUSH_RECEIVED') {
        console.log('🔔 Push notification recibida en primer plano:', data.notification)
        // Aquí se podría mostrar un toast o actualizar la UI
      }
    })
    
    // ═══════════════════════════════════════════════════════════════════
    
    // Inicializar sistema de notificaciones global con sonido
    const { initializeGlobalAudio, requestNotificationPermission } = useNotifications();
    
    // Solicitar permisos de notificación al usuario
    await requestNotificationPermission();
    
    // Inicializar audio global (después de interacción del usuario)
    document.addEventListener('click', () => {
      initializeGlobalAudio();
    }, { once: true });
    
    console.log('🔔 Sistema de notificaciones con sonido inicializado');
    
  } catch (error) {
    console.error('❌ Error al inicializar la aplicación:', error);
  }
});

// Crear aplicación
const app = createApp(App)

// Registrar componente Font Awesome globalmente
app.component('font-awesome-icon', FontAwesomeIcon)

// Usar router
app.use(router)

// Montar aplicación
app.mount('#app')
