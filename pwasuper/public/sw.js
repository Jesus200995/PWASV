/**
 * Service Worker para la PWA
 * Maneja cache, notificaciones, actualizaciones obligatorias y sincronización en segundo plano
 */

// Incrementar la versión del cache cuando hay cambios importantes
// Esto forzará a que se muestre la notificación de actualización
const CACHE_NAME = 'pwa-super-v1.0.1';
const OFFLINE_URL = '/offline.html';

// Archivos a cachear para funcionamiento offline
const urlsToCache = [
  '/',
  '/src/main.js',
  '/src/style.css',
  '/src/assets/main.css',
  // Agregar más archivos críticos según sea necesario
];

// Evento de instalación
self.addEventListener('install', (event) => {
  console.log('🔧 Service Worker instalándose...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('📦 Cache abierto');
        return cache.addAll(urlsToCache);
      })
      .then(() => {
        console.log('✅ Service Worker instalado correctamente');
        // Forzar activación inmediata
        return self.skipWaiting();
      })
  );
});

// Evento de activación
self.addEventListener('activate', (event) => {
  console.log('🚀 Service Worker activándose...');
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('🗑️ Eliminando cache obsoleto:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('✅ Service Worker activado');
      // Tomar control de todas las ventanas inmediatamente
      return self.clients.claim();
    })
  );
});

// Evento de fetch (intercepta todas las solicitudes de red)
self.addEventListener('fetch', (event) => {
  // Solo manejar solicitudes GET
  if (event.request.method !== 'GET') return;
  
  // Ignorar solicitudes del chrome-extension
  if (event.request.url.startsWith('chrome-extension://')) return;
  
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Si está en cache, devolverlo
        if (response) {
          return response;
        }
        
        // Si no está en cache, intentar descargarlo
        return fetch(event.request).then((response) => {
          // Verificar que la respuesta sea válida
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }
          
          // Clonar la respuesta (solo se puede usar una vez)
          const responseToCache = response.clone();
          
          // Agregar al cache
          caches.open(CACHE_NAME)
            .then((cache) => {
              cache.put(event.request, responseToCache);
            });
          
          return response;
        }).catch(() => {
          // Si falla la descarga, mostrar página offline para navegación
          if (event.request.mode === 'navigate') {
            return caches.match(OFFLINE_URL);
          }
        });
      })
  );
});

// Evento de sincronización en segundo plano
self.addEventListener('sync', (event) => {
  console.log('🔄 Evento de sincronización:', event.tag);
  
  if (event.tag === 'background-sync') {
    event.waitUntil(
      // Aquí se podría implementar lógica adicional de sincronización
      // Por ahora, el syncService.js se encarga de la sincronización
      console.log('📡 Sincronización en segundo plano ejecutada')
    );
  }
});

// Evento de notificación push
self.addEventListener('push', (event) => {
  console.log('🔔 Notificación push recibida:', event);
  
  let notificationData = {
    title: 'Sembrando Vida',
    body: 'Tienes nuevas notificaciones',
    icon: '/pwa-192x192.png',
    badge: '/pwa-192x192.png',
    tag: 'notification',
    requireInteraction: true,
    vibrate: [200, 100, 200],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: '1',
      url: '/notificaciones'
    }
  };

  // Si el push tiene datos, parsearlos
  if (event.data) {
    try {
      const pushData = event.data.json();
      notificationData = {
        ...notificationData,
        title: pushData.title || notificationData.title,
        body: pushData.body || pushData.descripcion || notificationData.body,
        icon: pushData.icon || notificationData.icon,
        data: {
          ...notificationData.data,
          id: pushData.id,
          url: pushData.url || '/notificaciones',
          ...pushData
        }
      };
    } catch (e) {
      // Si no es JSON, usar como texto simple
      notificationData.body = event.data.text();
    }
  }

  const options = {
    ...notificationData,
    actions: [
      {
        action: 'open',
        title: 'Ver notificación',
        icon: '/pwa-192x192.png'
      },
      {
        action: 'close',
        title: 'Cerrar',
        icon: '/pwa-192x192.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification(notificationData.title, options)
  );
});

// Evento de click en notificación
self.addEventListener('notificationclick', (event) => {
  console.log('🔔 Click en notificación:', event);
  
  event.notification.close();
  
  // Obtener la URL de la notificación
  const notificationUrl = event.notification.data?.url || '/notificaciones';
  
  if (event.action === 'open' || !event.action) {
    // Abrir o enfocar la aplicación en la página de notificaciones
    event.waitUntil(
      clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
        // Buscar si ya hay una ventana abierta
        for (let client of clientList) {
          if (client.url.includes(self.location.origin)) {
            // Si hay una ventana abierta, enfocarla y navegar a notificaciones
            return client.focus().then(() => {
              return client.postMessage({
                type: 'NAVIGATE_TO_NOTIFICATIONS',
                data: event.notification.data
              });
            });
          }
        }
        // Si no hay ventanas abiertas, abrir una nueva
        return clients.openWindow(notificationUrl);
      })
    );
  } else if (event.action === 'close') {
    // Solo cerrar la notificación
    console.log('Notificación cerrada por el usuario');
  }
});

// Evento de mensaje (comunicación con la aplicación principal)
self.addEventListener('message', (event) => {
  console.log('💬 Mensaje recibido en Service Worker:', event.data);
  
  // Al recibir mensaje para actualizar, saltar el waiting y activar el nuevo SW
  if (event.data && event.data.type === 'SKIP_WAITING') {
    console.log('⚡ Aplicando actualización solicitada por usuario...');
    self.skipWaiting();
  }
  
  // Proporcionar la versión actual cuando se solicite
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({
      type: 'VERSION',
      version: CACHE_NAME
    });
  }
});

// Función para limpiar caches antiguos
async function cleanupCaches() {
  const cacheNames = await caches.keys();
  await Promise.all(
    cacheNames
      .filter(cacheName => cacheName !== CACHE_NAME)
      .map(cacheName => caches.delete(cacheName))
  );
}

// Ejecutar limpieza de caches al activarse
self.addEventListener('activate', (event) => {
  event.waitUntil(cleanupCaches());
});

console.log('📱 Service Worker de PWA Super cargado correctamente');
