import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Importar estilos (Tailwind CSS y personalizados)
import './style.css'

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

// Registrar el Service Worker para funcionalidad PWA offline
window.addEventListener('load', async () => {
  try {
    // Registrar el service worker
    const registration = await registerServiceWorker();
    
    // Esperar a que el service worker esté listo
    await waitForServiceWorkerReady();
    
    console.log('✅ Aplicación lista con soporte offline');
    
    // Inicializar sistema de notificaciones global con sonido
    const { initializeGlobalAudio, requestNotificationPermission } = useNotifications();
    
    // Solicitar permisos de notificación al usuario
    await requestNotificationPermission();
    
    // Inicializar audio global (después de interacción del usuario)
    document.addEventListener('click', () => {
      initializeGlobalAudio();
    }, { once: true });
    
    console.log('🔔 Sistema de notificaciones con sonido inicializado');
    
    // Configurar listener para mensajes del Service Worker
    navigator.serviceWorker.addEventListener('message', (event) => {
      if (event.data && event.data.type === 'NAVIGATE_TO_NOTIFICATIONS') {
        // Navegar a notificaciones cuando se hace click en notificación push
        router.push('/notificaciones');
        console.log('📱 Navegando a notificaciones desde push notification');
      }
    });
    
  } catch (error) {
    console.error('❌ Error al inicializar la aplicación:', error);
  }
});

// Crear aplicación
const app = createApp(App)

// Usar router
app.use(router)

// Montar aplicación
app.mount('#app')
