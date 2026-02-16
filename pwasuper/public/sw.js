/**
 * Service Worker para la PWA
 * Maneja cache, notificaciones push, actualizaciones obligatorias y sincronización en segundo plano
 * Versión: 2.0.0 - Sistema de Push Notifications Profesional
 */

// Incrementar la versión del cache cuando hay cambios importantes
const CACHE_NAME = 'pwa-super-v2.0.0';
const OFFLINE_URL = '/offline.html';

// Archivos a cachear para funcionamiento offline
const urlsToCache = [
  '/',
  '/src/main.js',
  '/src/style.css',
  '/src/assets/main.css',
  '/pwa-192x192.png',
  '/pwa-512x512.png',
  // Agregar más archivos críticos según sea necesario
];

// Sonidos para notificaciones (si están disponibles)
const NOTIFICATION_SOUNDS = {
  default: '/sounds/notification.mp3',
  urgent: '/sounds/urgent.mp3',
  silent: null
};

// Evento de instalación
self.addEventListener('install', (event) => {
  console.log('🔧 Service Worker instalándose... v2.0.0');
  
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
    }).then(() => {
      // Notificar a todos los clientes que hay una actualización
      return self.clients.matchAll().then(clients => {
        clients.forEach(client => {
          client.postMessage({
            type: 'SW_UPDATED',
            version: CACHE_NAME
          });
        });
      });
    })
  );
});

// Evento de fetch (intercepta todas las solicitudes de red)
self.addEventListener('fetch', (event) => {
  // Ignorar solicitudes del chrome-extension y data:
  if (event.request.url.startsWith('chrome-extension://') || 
      event.request.url.startsWith('data:')) {
    return;
  }
  
  // Para peticiones GET, usar estrategia de cache-first
  if (event.request.method === 'GET') {
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
  } else {
    // Para otras peticiones (POST, PATCH, DELETE, PUT, etc.), permitir que pasen directamente
    // sin intervención del SW. Esto permite que los endpoints de API funcionen correctamente
    event.respondWith(
      fetch(event.request).catch(() => {
        // Si falla la conexión, mostrar página offline para navegación
        if (event.request.mode === 'navigate') {
          return caches.match(OFFLINE_URL);
        }
        // Para otros tipos de petición, rechazar
        return Promise.reject(new Error('No hay conexión de red'));
      })
    );
  }
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

// Evento de notificación push - Sistema Profesional
self.addEventListener('push', (event) => {
  console.log('🔔 Push Notification recibida');
  
  let notificationData = {
    title: 'Nueva Notificación',
    body: 'Tienes una nueva actualización',
    icon: '/pwa-192x192.png',
    badge: '/pwa-192x192.png',
    tag: 'general',
    data: { url: '/notificaciones' }
  };
  
  // Intentar parsear los datos del push
  if (event.data) {
    try {
      const pushData = event.data.json();
      console.log('📦 Datos del push:', pushData);
      
      notificationData = {
        title: pushData.title || notificationData.title,
        body: pushData.body || pushData.message || notificationData.body,
        icon: pushData.icon || notificationData.icon,
        badge: pushData.badge || notificationData.badge,
        image: pushData.image || null,
        tag: pushData.tag || `notif-${Date.now()}`,
        data: {
          url: pushData.data?.url || '/notificaciones',
          notificacion_id: pushData.data?.notificacion_id,
          tipo: pushData.data?.tipo || 'general',
          prioridad: pushData.data?.prioridad || 'normal',
          colorAccent: pushData.data?.colorAccent,
          timestamp: Date.now()
        },
        requireInteraction: pushData.requireInteraction || false,
        renotify: pushData.renotify !== false,
        silent: pushData.silent || false,
        vibrate: pushData.vibrate || [100, 50, 100],
        actions: pushData.actions || [
          { action: 'open', title: '📖 Ver', icon: '/icons/view.png' },
          { action: 'dismiss', title: '✕ Cerrar', icon: '/icons/close.png' }
        ]
      };
      
      // Configurar vibración según prioridad
      if (notificationData.data.prioridad === 'urgent') {
        notificationData.vibrate = [200, 100, 200, 100, 200];
        notificationData.requireInteraction = true;
      } else if (notificationData.data.prioridad === 'high') {
        notificationData.vibrate = [150, 75, 150];
      }
      
    } catch (e) {
      console.warn('⚠️ Error parseando datos del push:', e);
      notificationData.body = event.data.text();
    }
  }
  
  // Mostrar la notificación
  const showNotificationPromise = self.registration.showNotification(
    notificationData.title,
    {
      body: notificationData.body,
      icon: notificationData.icon,
      badge: notificationData.badge,
      image: notificationData.image,
      tag: notificationData.tag,
      data: notificationData.data,
      requireInteraction: notificationData.requireInteraction,
      renotify: notificationData.renotify,
      silent: notificationData.silent,
      vibrate: notificationData.vibrate,
      actions: notificationData.actions,
      // Timestamp para ordenar
      timestamp: Date.now()
    }
  );
  
  // Notificar a los clientes abiertos sobre la nueva notificación
  const notifyClientsPromise = self.clients.matchAll({ 
    type: 'window', 
    includeUncontrolled: true 
  }).then(clients => {
    clients.forEach(client => {
      client.postMessage({
        type: 'PUSH_RECEIVED',
        notification: notificationData
      });
    });
  });
  
  event.waitUntil(
    Promise.all([showNotificationPromise, notifyClientsPromise])
  );
});

// Evento de click en notificación - Manejo mejorado
self.addEventListener('notificationclick', (event) => {
  console.log('🖱️ Click en notificación:', event.notification.tag);
  
  const notification = event.notification;
  const action = event.action;
  const notificationData = notification.data || {};
  
  // Cerrar la notificación
  notification.close();
  
  // Determinar la URL a abrir
  let urlToOpen = notificationData.url || '/notificaciones';
  
  // Si hay notificacion_id, añadirlo como parámetro
  if (notificationData.notificacion_id) {
    urlToOpen = `/notificaciones?id=${notificationData.notificacion_id}`;
  }
  
  // Manejar acción específica
  if (action === 'dismiss') {
    console.log('👋 Notificación descartada por el usuario');
    // Solo cerrar, no abrir nada
    return;
  }
  
  // Para acción 'open' o click general - Abrir/enfocar la app
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then(clientList => {
        // Buscar si ya hay una ventana abierta
        for (const client of clientList) {
          if (client.url.includes(self.location.origin) && 'focus' in client) {
            // Navegar a la URL de la notificación
            client.postMessage({
              type: 'NAVIGATE_TO',
              url: urlToOpen,
              notificacion_id: notificationData.notificacion_id
            });
            return client.focus();
          }
        }
        
        // Si no hay ventana abierta, abrir una nueva
        if (self.clients.openWindow) {
          return self.clients.openWindow(urlToOpen);
        }
      })
  );
});

// Evento de cierre de notificación (sin acción específica)
self.addEventListener('notificationclose', (event) => {
  console.log('🔕 Notificación cerrada:', event.notification.tag);
  
  // Opcional: Registrar que la notificación fue cerrada sin acción
  const notificationData = event.notification.data || {};
  
  self.clients.matchAll({ type: 'window' }).then(clients => {
    clients.forEach(client => {
      client.postMessage({
        type: 'NOTIFICATION_CLOSED',
        notificacion_id: notificationData.notificacion_id,
        dismissed: true
      });
    });
  });
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
