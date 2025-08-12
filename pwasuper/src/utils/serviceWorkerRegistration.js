/**
 * Utilidad para registrar el service worker y manejar actualizaciones
 */

// Registrar el service worker
export async function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    try {
      const registration = await navigator.serviceWorker.register('/sw.js');
      console.log('Service Worker registrado con éxito:', registration.scope);
      
      // Verificar actualizaciones inmediatamente
      checkForUpdates(registration);
      
      // Verificar actualizaciones periódicamente
      setInterval(() => {
        checkForUpdates(registration);
      }, 60 * 60 * 1000); // Verificar cada hora
      
      return registration;
    } catch (error) {
      console.error('Error al registrar el Service Worker:', error);
      return null;
    }
  } else {
    console.warn('El navegador no soporta Service Workers');
    return null;
  }
}

// Verificar si hay actualizaciones disponibles
function checkForUpdates(registration) {
  if (!registration) return;
  
  registration.update().catch(err => {
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
