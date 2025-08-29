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
  
  if (event.tag === 'background-sync' || event.tag === 'background-sync-notifications') {
    event.waitUntil(
      checkForNewNotifications()
    );
  }
});

// Variables para polling en segundo plano
let backgroundPollingUserId = null;
let backgroundPollingInterval = null;
let backgroundApiUrl = null;
let isPollingActive = false;

// NUEVO: Estado persistente para notificaciones
let notificationState = {
  lastCheck: 0,
  lastCount: 0,
  isAppOpen: false
};

// NUEVO: Función para verificar notificaciones en segundo plano
async function checkForNewNotifications() {
  if (!backgroundPollingUserId || !backgroundApiUrl) {
    console.log('⚠️ No hay configuración de polling disponible');
    return;
  }

  try {
    console.log(`🔄 Verificando notificaciones para usuario ${backgroundPollingUserId}...`);
    
    const response = await fetch(`${backgroundApiUrl}/notificaciones/no-leidas?usuario_id=${backgroundPollingUserId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      const unreadCount = data.total_no_leidas || 0;
      
      // Obtener el contador anterior del almacenamiento
      const stored = await caches.open('notification-cache');
      const cachedResponse = await stored.match('last-notification-count');
      let previousCount = notificationState.lastCount || 0;
      
      if (cachedResponse) {
        const cachedData = await cachedResponse.json();
        previousCount = cachedData.count || 0;
      }
      
      console.log(`📊 Notificaciones: ${unreadCount} (anterior: ${previousCount})`);
      
      // Si hay nuevas notificaciones, mostrar notificación push
      if (unreadCount > previousCount && unreadCount > 0) {
        const newNotifications = unreadCount - previousCount;
        
        // Verificar si alguna ventana de la app está abierta
        const clients = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
        const appIsOpen = clients.length > 0;
        
        if (!appIsOpen) {
          // Solo mostrar notificación push si la app NO está abierta
          await self.registration.showNotification('🌿 PWA Super - Nueva Notificación', {
            body: `Tienes ${newNotifications} nueva(s) notificación(es) por revisar`,
            icon: '/pwa-192x192.png',
            badge: '/pwa-192x192.png',
            vibrate: [150, 50, 150, 50, 150, 50, 200], // Patrón de vibración natural
            tag: 'new-notifications-' + Date.now(), // Tag único para evitar reemplazar
            requireInteraction: true, // Mantiene la notificación hasta que el usuario interactúe
            silent: false, // Permite sonido del sistema
            renotify: true, // Permite mostrar nuevamente la notificación
            timestamp: Date.now(),
            image: '/pwa-512x512.png', // Imagen grande en la notificación
            data: {
              unreadCount: unreadCount,
              newCount: newNotifications,
              timestamp: Date.now(),
              url: '/#/notificaciones'
            },
            actions: [
              {
                action: 'view',
                title: '👀 Ver Notificaciones',
                icon: '/pwa-192x192.png'
              },
              {
                action: 'dismiss',
                title: '✖️ Descartar',
                icon: '/pwa-192x192.png'
              },
              {
                action: 'open',
                title: '🚀 Abrir App',
                icon: '/pwa-192x192.png'
              }
            ]
          });
          
          console.log(`🔔 Notificación push enviada: ${newNotifications} nueva(s) notificación(es) (App cerrada)`);
        } else {
          console.log(`📱 App abierta, no se envía notificación push (${newNotifications} nuevas)`);
        }
      }
      
      // Actualizar contador y estado en cache
      notificationState.lastCount = unreadCount;
      notificationState.lastCheck = Date.now();
      
      await stored.put('last-notification-count', new Response(JSON.stringify({ 
        count: unreadCount, 
        timestamp: Date.now(),
        lastCheck: notificationState.lastCheck
      })));
      
    } else {
      console.warn('⚠️ Error obteniendo notificaciones:', response.status, response.statusText);
    }
  } catch (error) {
    console.error('❌ Error en verificación de notificaciones en segundo plano:', error);
  }
}

// Evento de notificación push
self.addEventListener('push', (event) => {
  console.log('🔔 Notificación push recibida:', event);
  
  const options = {
    body: event.data ? event.data.text() : 'Tienes nuevas actualizaciones disponibles',
    icon: '/pwa-192x192.png',
    badge: '/pwa-192x192.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: '1'
    },
    actions: [
      {
        action: 'explore',
        title: 'Ver',
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
    self.registration.showNotification('PWA Super', options)
  );
});

// Evento de click en notificación
self.addEventListener('notificationclick', (event) => {
  console.log('🔔 Click en notificación:', event.action, event.notification.data);
  
  event.notification.close();
  
  const handleNotificationClick = async () => {
    const clients = await self.clients.matchAll({ 
      type: 'window',
      includeUncontrolled: true 
    });
    
    if (event.action === 'view') {
      // Abrir la aplicación en la sección de notificaciones
      if (clients.length > 0) {
        const client = clients[0];
        await client.focus();
        client.postMessage({
          type: 'NAVIGATE_TO_NOTIFICATIONS',
          data: event.notification.data
        });
      } else {
        await self.clients.openWindow('/#/notificaciones');
      }
    } else if (event.action === 'open') {
      // Abrir la aplicación en la página principal
      if (clients.length > 0) {
        await clients[0].focus();
      } else {
        await self.clients.openWindow('/');
      }
    } else if (event.action === 'dismiss') {
      // Solo cerrar la notificación (ya se cerró arriba)
      console.log('🔕 Notificación descartada por el usuario');
    } else {
      // Click general en la notificación - abrir aplicación
      if (clients.length > 0) {
        const client = clients[0];
        await client.focus();
        client.postMessage({
          type: 'NAVIGATE_TO_NOTIFICATIONS',
          data: event.notification.data
        });
      } else {
        await self.clients.openWindow('/#/notificaciones');
      }
    }
  };
  
  event.waitUntil(handleNotificationClick());
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
  
  // NUEVO: Configurar polling de notificaciones en segundo plano
  if (event.data && event.data.type === 'START_BACKGROUND_NOTIFICATIONS_POLLING') {
    backgroundPollingUserId = event.data.userId;
    backgroundApiUrl = event.data.apiUrl;
    const interval = event.data.interval || 15000;
    
    console.log(`📡 Iniciando polling de notificaciones en segundo plano para usuario ${backgroundPollingUserId} cada ${interval/1000}s`);
    
    // Limpiar intervalo anterior si existe
    if (backgroundPollingInterval) {
      clearInterval(backgroundPollingInterval);
    }
    
    // Marcar como activo
    isPollingActive = true;
    
    // Iniciar polling periódico
    backgroundPollingInterval = setInterval(() => {
      if (isPollingActive) {
        checkForNewNotifications();
      }
    }, interval);
    
    // Ejecutar verificación inmediata
    checkForNewNotifications();
  }
  
  // NUEVO: Detener polling de notificaciones
  if (event.data && event.data.type === 'STOP_BACKGROUND_NOTIFICATIONS_POLLING') {
    if (backgroundPollingInterval) {
      clearInterval(backgroundPollingInterval);
      backgroundPollingInterval = null;
      isPollingActive = false;
      console.log('🛑 Polling de notificaciones en segundo plano detenido');
    }
  }
  
  // NUEVO: Marcar app como abierta/cerrada
  if (event.data && event.data.type === 'APP_STATUS') {
    notificationState.isAppOpen = event.data.isOpen;
    console.log(`📱 Estado de app actualizado: ${event.data.isOpen ? 'Abierta' : 'Cerrada'}`);
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
