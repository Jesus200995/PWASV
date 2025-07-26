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

// Registrar Service Worker para funcionalidad PWA offline
if ('serviceWorker' in navigator) {
  window.addEventListener('load', async () => {
    try {
      const registration = await navigator.serviceWorker.register('/sw.js', {
        scope: '/'
      });
      
      console.log('✅ Service Worker registrado correctamente:', registration.scope);
      
      // Escuchar actualizaciones del service worker
      registration.addEventListener('updatefound', () => {
        const newWorker = registration.installing;
        console.log('🔄 Nueva versión del Service Worker encontrada');
        
        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
            console.log('🆕 Nueva versión disponible, considera recargar la página');
            
            // Opcional: mostrar notificación al usuario sobre la actualización
            if (window.confirm('Hay una nueva versión disponible. ¿Deseas actualizar?')) {
              newWorker.postMessage({ type: 'SKIP_WAITING' });
              window.location.reload();
            }
          }
        });
      });
      
      // Listener para cuando un service worker toma control
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        console.log('🔄 Service Worker actualizado, recargando página...');
        window.location.reload();
      });
      
    } catch (error) {
      console.error('❌ Error al registrar Service Worker:', error);
    }
  });
} else {
  console.warn('⚠️ Service Worker no soportado en este navegador');
}

// Importar y verificar servicios offline
import offlineService from './services/offlineService.js'

// Verificar estado de la base de datos offline
setTimeout(async () => {
  try {
    console.log('🔍 Verificando estado de la base de datos offline...');
    const estado = await offlineService.verificarEstadoDB();
    if (!estado) {
      console.warn('⚠️ Base de datos offline tiene problemas, reiniciando...');
      await offlineService.resetDatabase();
    }
  } catch (error) {
    console.error('❌ Error verificando base de datos offline:', error);
  }
}, 2000);

// Crear aplicación
const app = createApp(App)

// Usar router
app.use(router)

// Montar aplicación
app.mount('#app')
