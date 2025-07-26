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

// Crear aplicación
const app = createApp(App)

// Usar router
app.use(router)

// Montar aplicación
app.mount('#app')

// Registrar Service Worker para soporte offline
if ('serviceWorker' in navigator) {
  window.addEventListener('load', async () => {
    try {
      const registration = await navigator.serviceWorker.register('/sw.js', {
        scope: '/'
      });
      
      console.log('✅ Service Worker registrado correctamente:', registration.scope);
      
      // Escuchar actualizaciones del Service Worker
      registration.addEventListener('updatefound', () => {
        const newWorker = registration.installing;
        console.log('🔄 Nuevo Service Worker encontrado, instalando...');
        
        newWorker?.addEventListener('statechange', () => {
          if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
            console.log('🆕 Nueva versión del Service Worker disponible');
            // Aquí se podría mostrar un mensaje al usuario para recargar
          }
        });
      });
      
      // Escuchar mensajes del Service Worker
      navigator.serviceWorker.addEventListener('message', (event) => {
        console.log('💬 Mensaje del Service Worker:', event.data);
        
        if (event.data && event.data.type === 'TRIGGER_SYNC') {
          // Disparar evento personalizado para que los componentes sincronicen
          window.dispatchEvent(new CustomEvent('sw-sync-trigger', {
            detail: event.data
          }));
        }
      });
      
    } catch (error) {
      console.error('❌ Error registrando Service Worker:', error);
    }
  });
} else {
  console.warn('⚠️ Service Workers no soportados en este navegador');
}
