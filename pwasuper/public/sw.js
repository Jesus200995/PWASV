// Service Worker para PWA Offline
// Este archivo puede ser usado para habilitar cache de recursos estáticos

const CACHE_NAME = 'pwa-super-v1';
const urlsToCache = [
  '/',
  '/offline.html',
  // Se pueden agregar recursos críticos aquí
];

// Instalación del Service Worker
self.addEventListener('install', (event) => {
  console.log('🔧 Service Worker: Instalando...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('📦 Service Worker: Cache abierto');
        return cache.addAll(urlsToCache);
      })
  );
});

// Activación del Service Worker
self.addEventListener('activate', (event) => {
  console.log('✅ Service Worker: Activado');
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('🗑️ Service Worker: Eliminando cache antigua', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Intercepción de requests
self.addEventListener('fetch', (event) => {
  // Solo manejar requests GET
  if (event.request.method !== 'GET') {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Devolver desde cache si existe
        if (response) {
          return response;
        }

        // Intentar fetch de la red
        return fetch(event.request).then((response) => {
          // Verificar si es una respuesta válida
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }

          // Clonar la respuesta
          const responseToCache = response.clone();

          caches.open(CACHE_NAME)
            .then((cache) => {
              cache.put(event.request, responseToCache);
            });

          return response;
        });
      }
    )
  );
});

// Manejo de sincronización en background (futuro)
self.addEventListener('sync', (event) => {
  console.log('🔄 Service Worker: Evento de sincronización', event.tag);
  
  if (event.tag === 'background-sync') {
    event.waitUntil(
      // Aquí se puede implementar sincronización en background
      console.log('📤 Service Worker: Sincronización en background')
    );
  }
});

// Manejo de notificaciones push (futuro)
self.addEventListener('push', (event) => {
  console.log('📬 Service Worker: Notificación push recibida');
  
  const options = {
    body: 'Datos sincronizados exitosamente',
    icon: '/icon-192x192.png',
    badge: '/icon-96x96.png'
  };

  event.waitUntil(
    self.registration.showNotification('PWA Super', options)
  );
});
