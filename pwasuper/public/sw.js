/**
 * Service Worker para la PWA
 * Maneja cache, notificaciones push, actualizaciones obligatorias y sincronización en segundo plano
 * VERSIÓN MEJORADA PARA NOTIFICACIONES GARANTIZADAS
 */

// Incrementar la versión del cache cuando hay cambios importantes
const CACHE_NAME = 'pwa-super-v1.0.2';
const OFFLINE_URL = '/offline.html';

// Archivos a cachear para funcionamiento offline
const urlsToCache = [
  '/',
  '/src/main.js',
  '/src/style.css',
  '/src/assets/main.css',
  '/manifest.json',
  '/pwa-192x192.png',
  '/pwa-512x512.png'
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

// Variables para polling en segundo plano - VERSIÓN MEJORADA
let backgroundPollingUserId = null;
let backgroundPollingInterval = null;
let backgroundApiUrl = null;
let isPollingActive = false;
let pollingAttempts = 0;
let maxPollingAttempts = 5;

// NUEVO: Estado persistente para notificaciones con mejor tracking
let notificationState = {
  lastCheck: 0,
  lastCount: 0,
  isAppOpen: false,
  consecutiveErrors: 0,
  permissionGranted: false
};

// NUEVO: Cola de notificaciones pendientes
let pendingNotifications = [];

// MEJORADO: Función robusta para verificar notificaciones en segundo plano
async function checkForNewNotifications() {
  if (!backgroundPollingUserId || !backgroundApiUrl) {
    console.log('⚠️ No hay configuración de polling disponible');
    return;
  }

  // Si hay muchos errores consecutivos, reducir frecuencia
  if (notificationState.consecutiveErrors > 3) {
    console.log('⚠️ Demasiados errores, saltando esta verificación');
    return;
  }

  try {
    console.log(`🔄 [${new Date().toLocaleTimeString()}] Verificando notificaciones para usuario ${backgroundPollingUserId}...`);
    
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // Timeout de 10s
    
    const response = await fetch(`${backgroundApiUrl}/notificaciones/no-leidas?usuario_id=${backgroundPollingUserId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'PWA-ServiceWorker'
      },
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
    
    if (response.ok) {
      const data = await response.json();
      const unreadCount = data.total_no_leidas || 0;
      
      // Resetear contador de errores en caso de éxito
      notificationState.consecutiveErrors = 0;
      
      // Obtener el contador anterior del almacenamiento persistente
      const stored = await caches.open('notification-cache');
      const cachedResponse = await stored.match('last-notification-count');
      let previousCount = notificationState.lastCount || 0;
      
      if (cachedResponse) {
        try {
          const cachedData = await cachedResponse.json();
          previousCount = cachedData.count || 0;
        } catch (e) {
          console.warn('⚠️ Error leyendo cache, usando valor por defecto');
        }
      }
      
      console.log(`📊 Notificaciones: ${unreadCount} actual vs ${previousCount} anterior`);
      
      // MEJORADO: Solo mostrar notificación si hay incremento Y la app está cerrada
      if (unreadCount > previousCount && unreadCount > 0) {
        const newNotifications = unreadCount - previousCount;
        
        // Verificar estado de ventanas de forma más robusta
        const clients = await self.clients.matchAll({ 
          type: 'window', 
          includeUncontrolled: true 
        });
        
        let appIsOpen = false;
        for (const client of clients) {
          if (client.visibilityState === 'visible') {
            appIsOpen = true;
            break;
          }
        }
        
        console.log(`📱 Estado de app: ${appIsOpen ? 'Abierta' : 'Cerrada'} (${clients.length} cliente(s))`);
        
        if (!appIsOpen) {
          // MEJORADO: Verificar permisos antes de mostrar notificación
          if (notificationState.permissionGranted || Notification.permission === 'granted') {
            await showNotificationWithFallback(newNotifications, unreadCount);
          } else {
            console.log('🔔 Permisos no concedidos, almacenando notificación pendiente');
            pendingNotifications.push({ newCount: newNotifications, totalCount: unreadCount, timestamp: Date.now() });
          }
        } else {
          console.log(`📱 App visible, notificación manejada internamente (${newNotifications} nuevas)`);
        }
      }
      
      // Actualizar estado y cache
      notificationState.lastCount = unreadCount;
      notificationState.lastCheck = Date.now();
      
      await stored.put('last-notification-count', new Response(JSON.stringify({ 
        count: unreadCount, 
        timestamp: Date.now(),
        lastCheck: notificationState.lastCheck,
        userId: backgroundPollingUserId
      })));
      
      pollingAttempts = 0; // Resetear intentos fallidos
      
    } else {
      console.warn(`⚠️ Error HTTP obteniendo notificaciones: ${response.status} ${response.statusText}`);
      notificationState.consecutiveErrors++;
      
      if (response.status === 401 || response.status === 403) {
        console.error('❌ Error de autenticación, deteniendo polling');
        if (backgroundPollingInterval) {
          clearInterval(backgroundPollingInterval);
          isPollingActive = false;
        }
      }
    }
  } catch (error) {
    console.error(`❌ [${new Date().toLocaleTimeString()}] Error en verificación de notificaciones:`, error.message);
    notificationState.consecutiveErrors++;
    pollingAttempts++;
    
    // Si hay demasiados errores, reducir frecuencia
    if (pollingAttempts >= maxPollingAttempts) {
      console.warn('⚠️ Demasiados intentos fallidos, reiniciando polling con menos frecuencia');
      if (backgroundPollingInterval) {
        clearInterval(backgroundPollingInterval);
        // Reiniciar con menos frecuencia (30s en lugar de 15s)
        backgroundPollingInterval = setInterval(() => {
          if (isPollingActive) checkForNewNotifications();
        }, 30000);
      }
      pollingAttempts = 0;
    }
  }
}

// NUEVO: Función para mostrar notificaciones con fallbacks
async function showNotificationWithFallback(newNotifications, totalCount) {
  try {
    const notificationOptions = {
      body: `🔔 Tienes ${newNotifications} nueva(s) notificación(es)${totalCount > newNotifications ? ` (Total: ${totalCount})` : ''}`,
      icon: '/pwa-192x192.png',
      badge: '/pwa-192x192.png',
      vibrate: [200, 100, 200], // Vibración más simple y efectiva
      tag: `notification-${Date.now()}`, // Tag único para evitar reemplazos
      requireInteraction: true,
      silent: false,
      renotify: true,
      timestamp: Date.now(),
      image: '/pwa-512x512.png',
      data: {
        unreadCount: totalCount,
        newCount: newNotifications,
        timestamp: Date.now(),
        url: '/#/notificaciones',
        userId: backgroundPollingUserId
      },
      actions: [
        {
          action: 'view',
          title: '👀 Ver Notificaciones',
          icon: '/pwa-192x192.png'
        },
        {
          action: 'open',
          title: '🚀 Abrir App',
          icon: '/pwa-192x192.png'
        },
        {
          action: 'dismiss',
          title: '❌ Descartar',
          icon: '/pwa-192x192.png'
        }
      ]
    };
    
    await self.registration.showNotification('🔔 PWA Super - Nuevas Notificaciones', notificationOptions);
    
    console.log(`✅ [${new Date().toLocaleTimeString()}] Notificación push enviada: ${newNotifications} nueva(s) notificación(es)`);
    
    // Limpiar notificaciones pendientes exitosamente enviadas
    pendingNotifications = pendingNotifications.filter(n => n.timestamp < Date.now() - 60000);
    
  } catch (error) {
    console.error('❌ Error mostrando notificación push:', error);
    
    // Fallback: almacenar para reintento posterior
    pendingNotifications.push({
      newCount: newNotifications,
      totalCount: totalCount,
      timestamp: Date.now(),
      retryCount: 0
    });
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
self.addEventListener('message', async (event) => {
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
  
  // MEJORADO: Configurar polling de notificaciones en segundo plano
  if (event.data && event.data.type === 'START_BACKGROUND_NOTIFICATIONS_POLLING') {
    backgroundPollingUserId = event.data.userId;
    backgroundApiUrl = event.data.apiUrl;
    const interval = event.data.interval || 10000; // Más agresivo: cada 10 segundos
    
    console.log(`📡 [${new Date().toLocaleTimeString()}] Iniciando polling robusto para usuario ${backgroundPollingUserId} cada ${interval/1000}s`);
    
    // Limpiar intervalo anterior si existe
    if (backgroundPollingInterval) {
      clearInterval(backgroundPollingInterval);
    }
    
    // Resetear estado
    isPollingActive = true;
    pollingAttempts = 0;
    notificationState.consecutiveErrors = 0;
    
    // NUEVO: Verificar permisos inmediatamente
    notificationState.permissionGranted = Notification.permission === 'granted';
    
    if (!notificationState.permissionGranted) {
      console.warn('⚠️ Permisos de notificación no concedidos, solicitando...');
      // En un service worker no se puede solicitar permisos directamente
      // Se enviará mensaje a la app principal
      const clients = await self.clients.matchAll();
      clients.forEach(client => {
        client.postMessage({
          type: 'REQUEST_NOTIFICATION_PERMISSION',
          urgent: true
        });
      });
    }
    
    // Iniciar polling periódico robusto
    backgroundPollingInterval = setInterval(async () => {
      if (isPollingActive) {
        await checkForNewNotifications();
        
        // Procesar notificaciones pendientes si ahora tenemos permisos
        if (Notification.permission === 'granted' && pendingNotifications.length > 0) {
          notificationState.permissionGranted = true;
          const pending = pendingNotifications.splice(0, 3); // Procesar hasta 3 pendientes
          for (const notification of pending) {
            if (Date.now() - notification.timestamp < 300000) { // Solo si es menor a 5 minutos
              await showNotificationWithFallback(notification.newCount, notification.totalCount);
            }
          }
        }
      }
    }, interval);
    
    // Ejecutar verificación inmediata
    setTimeout(() => checkForNewNotifications(), 2000); // Esperar 2s para que la app se establezca
  }
  
  // MEJORADO: Detener polling de notificaciones
  if (event.data && event.data.type === 'STOP_BACKGROUND_NOTIFICATIONS_POLLING') {
    if (backgroundPollingInterval) {
      clearInterval(backgroundPollingInterval);
      backgroundPollingInterval = null;
      isPollingActive = false;
      console.log('🛑 Polling de notificaciones detenido');
    }
  }
  
  // MEJORADO: Marcar app como abierta/cerrada con más detalle
  if (event.data && event.data.type === 'APP_STATUS') {
    const wasOpen = notificationState.isAppOpen;
    notificationState.isAppOpen = event.data.isOpen;
    
    console.log(`📱 Estado de app: ${wasOpen ? 'Abierta' : 'Cerrada'} → ${event.data.isOpen ? 'Abierta' : 'Cerrada'}`);
    
    // Si la app se acaba de cerrar, aumentar frecuencia de polling temporalmente
    if (wasOpen && !event.data.isOpen && backgroundPollingInterval) {
      console.log('📱 App recién cerrada, aumentando frecuencia de polling temporalmente');
      clearInterval(backgroundPollingInterval);
      
      // Polling más frecuente cuando la app se acaba de cerrar (cada 5 segundos por 2 minutos)
      let tempPollingCount = 0;
      const tempInterval = setInterval(async () => {
        if (isPollingActive && tempPollingCount < 24) { // 24 * 5s = 2 minutos
          await checkForNewNotifications();
          tempPollingCount++;
        } else {
          clearInterval(tempInterval);
          // Volver al polling normal
          if (isPollingActive) {
            backgroundPollingInterval = setInterval(() => {
              if (isPollingActive) checkForNewNotifications();
            }, 10000);
          }
        }
      }, 5000);
    }
  }
  
  // NUEVO: Actualizar permisos de notificación
  if (event.data && event.data.type === 'NOTIFICATION_PERMISSION_UPDATED') {
    notificationState.permissionGranted = event.data.granted;
    console.log(`🔔 Permisos de notificación actualizados: ${event.data.granted ? 'Concedidos' : 'Denegados'}`);
    
    if (event.data.granted && pendingNotifications.length > 0) {
      console.log(`📤 Procesando ${pendingNotifications.length} notificaciones pendientes`);
      const pending = pendingNotifications.splice(0);
      for (const notification of pending) {
        if (Date.now() - notification.timestamp < 300000) { // Solo si es menor a 5 minutos
          await showNotificationWithFallback(notification.newCount, notification.totalCount);
          await new Promise(resolve => setTimeout(resolve, 1000)); // Esperar 1s entre notificaciones
        }
      }
    }
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
