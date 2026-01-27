/**
 * Utilidad para registrar el service worker y manejar actualizaciones
 * Sistema de actualización reactiva e inmediata
 */

// Callback para notificar actualizaciones
let onUpdateCallback = null;

// Registrar el service worker
export async function registerServiceWorker(onUpdate) {
  // Guardar callback para notificar actualizaciones
  if (onUpdate) {
    onUpdateCallback = onUpdate;
  }

  if ('serviceWorker' in navigator) {
    try {
      const registration = await navigator.serviceWorker.register('/sw.js');
      console.log('📦 Service Worker registrado con éxito:', registration.scope);
      
      // Verificar actualizaciones inmediatamente
      checkForUpdates(registration);
      
      // Verificar actualizaciones cada 15 segundos (para actualización inmediata)
      setInterval(() => {
        checkForUpdates(registration);
      }, 15 * 1000); // Cada 15 segundos
      
      // Escuchar mensajes del Service Worker
      navigator.serviceWorker.addEventListener('message', (event) => {
        console.log('📩 Mensaje del SW:', event.data);
        
        if (event.data && event.data.type === 'SW_UPDATED') {
          console.log('🚀 SW actualizado a versión:', event.data.version);
          if (onUpdateCallback) {
            onUpdateCallback(event.data.version);
          }
        }
      });

      // Detectar cuando hay un nuevo SW instalado y esperando
      registration.addEventListener('updatefound', () => {
        const newWorker = registration.installing;
        console.log('🔄 Nuevo Service Worker encontrado...');
        
        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'installed') {
            if (navigator.serviceWorker.controller) {
              // Hay una actualización disponible
              console.log('⬆️ Actualización del SW lista para aplicar');
              // Activar el nuevo SW inmediatamente
              newWorker.postMessage({ type: 'SKIP_WAITING' });
            }
          }
        });
      });

      // Recargar automáticamente cuando el SW toma el control
      let refreshing = false;
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        if (!refreshing) {
          refreshing = true;
          console.log('⚡ Nuevo SW tomando control, recargando...');
          // Notificar antes de recargar
          if (onUpdateCallback) {
            onUpdateCallback('auto-reload');
          }
          // Recargar después de mostrar notificación
          setTimeout(() => {
            window.location.reload();
          }, 1500);
        }
      });
      
      return registration;
    } catch (error) {
      console.error('❌ Error al registrar el Service Worker:', error);
      return null;
    }
  } else {
    console.warn('⚠️ El navegador no soporta Service Workers');
    return null;
  }
}

// Verificar si hay actualizaciones disponibles
function checkForUpdates(registration) {
  if (!registration) return;
  
  registration.update().then(() => {
    console.log('🔍 Verificando actualizaciones del SW...');
  }).catch(err => {
    console.error('Error al buscar actualizaciones del SW:', err);
  });
}

// Esperar a que el service worker esté listo
export function waitForServiceWorkerReady() {
  return new Promise((resolve) => {
    if (!('serviceWorker' in navigator)) {
      return resolve(false);
    }
    
    if (navigator.serviceWorker.controller) {
      // Ya hay un service worker controlando la página
      return resolve(true);
    } else {
      // Esperar a que el service worker tome control
      const listener = () => {
        resolve(true);
        navigator.serviceWorker.removeEventListener('controllerchange', listener);
      };
      
      navigator.serviceWorker.addEventListener('controllerchange', listener);
      
      // Timeout para evitar esperar indefinidamente
      setTimeout(() => {
        navigator.serviceWorker.removeEventListener('controllerchange', listener);
        resolve(false);
      }, 10000);
    }
  });
}
