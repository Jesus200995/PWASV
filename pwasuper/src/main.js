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

// Registrar el Service Worker para funcionalidad PWA offline
window.addEventListener('load', async () => {
  try {
    // Registrar el service worker
    const registration = await registerServiceWorker();
    
    // Esperar a que el service worker esté listo
    await waitForServiceWorkerReady();
    
    console.log('✅ Aplicación lista con soporte offline');
  } catch (error) {
    console.error('❌ Error al inicializar el Service Worker:', error);
  }
});

// Crear aplicación
const app = createApp(App)

// Usar router
app.use(router)

// Montar aplicación
app.mount('#app')
