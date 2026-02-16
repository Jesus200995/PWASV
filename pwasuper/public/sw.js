/**
 * Service Worker para la PWA
 * Maneja cache, notificaciones push, actualizaciones obligatorias y sincronización en segundo plano
 * Versión: 3.0.0 - Sistema de Push Notifications Empresarial (Estilo Mercado Libre)
 */

// Incrementar la versión del cache cuando hay cambios importantes
const CACHE_NAME = 'pwa-super-v3.0.0';
const OFFLINE_URL = '/offline.html';

// Configuración de la app para notificaciones
const APP_CONFIG = {
  name: 'Sembrando Vida',
  shortName: 'SV',
  defaultIcon: '/pwa-192x192.png',
  badge: '/badge-72x72.png', // Badge monocromático para Android
  accentColor: '#10B981' // Verde esmeralda - Color de marca
};

// Archivos a cachear para funcionamiento offline
const urlsToCache = [
  '/',
  '/src/main.js',
  '/src/style.css',
  '/src/assets/main.css',
  '/pwa-192x192.png',
  '/pwa-512x512.png',
  '/badge-72x72.png',
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

// ═══════════════════════════════════════════════════════════════════════════════════
// SISTEMA DE NOTIFICACIONES PUSH EMPRESARIAL - ESTILO MERCADO LIBRE
// ═══════════════════════════════════════════════════════════════════════════════════

/**
 * Mapeo de tipos de notificación a configuraciones visuales
 * Similar a cómo Mercado Libre diferencia entre tipos de notificación
 * Nota: Todos los iconos apuntan al icono principal ya que los personalizados no están creados
 */
const NOTIFICATION_TYPES = {
  info: {
    icon: '/pwa-192x192.png',  // Usar icono principal
    color: '#3B82F6', // Azul
    vibrate: [100, 50, 100],
    sound: 'default'
  },
  success: {
    icon: '/pwa-192x192.png',  // Usar icono principal
    color: '#10B981', // Verde
    vibrate: [100, 50, 100],
    sound: 'default'
  },
  warning: {
    icon: '/pwa-192x192.png',  // Usar icono principal
    color: '#F59E0B', // Amarillo
    vibrate: [150, 75, 150],
    sound: 'default'
  },
  urgent: {
    icon: '/pwa-192x192.png',  // Usar icono principal
    color: '#EF4444', // Rojo
    vibrate: [200, 100, 200, 100, 200],
    sound: 'urgent',
    requireInteraction: true
  },
  message: {
    icon: '/pwa-192x192.png',  // Usar icono principal
    color: '#8B5CF6', // Púrpura
    vibrate: [100, 50, 100],
    sound: 'default'
  },
  reminder: {
    icon: '/pwa-192x192.png',  // Usar icono principal
    color: '#EC4899', // Rosa
    vibrate: [150, 75, 150, 75, 150],
    sound: 'default'
  }
};

/**
 * Construye una notificación rica estilo empresarial
 * @param {Object} pushData - Datos recibidos del servidor
 * @returns {Object} Configuración completa de la notificación
 */
function buildRichNotification(pushData) {
  // Obtener configuración por tipo
  const typeConfig = NOTIFICATION_TYPES[pushData.tipo] || NOTIFICATION_TYPES.info;
  
  // Timestamp formateado
  const timestamp = Date.now();
  
  // Construir título profesional
  let title = pushData.title || 'Sembrando Vida';
  
  // Construir cuerpo con formato empresarial
  let body = pushData.body || pushData.message || '';
  
  // Si hay información adicional, añadirla de forma elegante
  if (pushData.subtitle) {
    body = `${pushData.subtitle}\n${body}`;
  }
  
  // Determinar el icono a usar - SIEMPRE usar icono principal como fallback
  let icon = APP_CONFIG.defaultIcon; // Empezar con el default seguro
  
  // Solo usar icono personalizado si es una URL válida
  if (pushData.icon && (pushData.icon.startsWith('/pwa') || pushData.icon.startsWith('http'))) {
    icon = pushData.icon;
  }
  
  // Badge (icono pequeño en la barra de estado - Android)
  const badge = APP_CONFIG.badge || APP_CONFIG.defaultIcon;
  
  // Imagen grande (Big Picture style - como Mercado Libre)
  const image = pushData.image || null;
  
  // Acciones dinámicas según tipo de notificación
  let actions = [];
  
  // Acciones personalizadas del servidor
  if (pushData.actions && Array.isArray(pushData.actions)) {
    actions = pushData.actions;
  } else {
    // Acciones predeterminadas según tipo
    switch (pushData.tipo) {
      case 'message':
        actions = [
          { action: 'reply', title: '💬 Responder' },
          { action: 'open', title: '📖 Ver' }
        ];
        break;
      case 'urgent':
        actions = [
          { action: 'open', title: '🚨 Ver ahora' },
          { action: 'remind', title: '⏰ Recordar' }
        ];
        break;
      case 'reminder':
        actions = [
          { action: 'complete', title: '✓ Completado' },
          { action: 'snooze', title: '⏰ Posponer' }
        ];
        break;
      default:
        actions = [
          { action: 'open', title: '📖 Ver detalle' },
          { action: 'dismiss', title: '✕ Descartar' }
        ];
    }
  }
  
  // Configuración de vibración
  let vibrate = typeConfig.vibrate;
  if (pushData.prioridad === 'urgent' || pushData.prioridad === 'alta') {
    vibrate = [200, 100, 200, 100, 200]; // Vibración más intensa
  } else if (pushData.prioridad === 'high' || pushData.prioridad === 'media') {
    vibrate = [150, 75, 150];
  } else if (pushData.silent) {
    vibrate = []; // Sin vibración
  }
  
  // Tag único para agrupar/reemplazar notificaciones
  const tag = pushData.tag || `sv-${pushData.tipo || 'notif'}-${pushData.notificacion_id || timestamp}`;
  
  return {
    title: title,
    options: {
      body: body,
      icon: icon,
      badge: badge,
      image: image,
      tag: tag,
      // Datos para manejar el click
      data: {
        url: pushData.url || pushData.data?.url || '/notificaciones',
        notificacion_id: pushData.notificacion_id || pushData.data?.notificacion_id,
        tipo: pushData.tipo || 'general',
        prioridad: pushData.prioridad || 'normal',
        colorAccent: pushData.color_acento || typeConfig.color,
        timestamp: timestamp,
        // Datos adicionales para la app
        extra: pushData.extra || {}
      },
      // Comportamiento
      requireInteraction: pushData.requireInteraction || typeConfig.requireInteraction || false,
      renotify: true, // Siempre notificar aunque sea el mismo tag
      silent: pushData.silent || false,
      vibrate: vibrate,
      // Acciones (botones)
      actions: actions,
      // Timestamp para ordenar en el panel de notificaciones
      timestamp: timestamp,
      // Dirección del texto
      dir: 'ltr',
      // Idioma
      lang: 'es-MX'
    }
  };
}

// Evento de notificación push - Sistema Empresarial
self.addEventListener('push', (event) => {
  console.log('🔔 [PUSH] Notificación recibida');
  
  let notificationConfig;
  
  try {
    // Intentar parsear los datos del push
    if (event.data) {
      const pushData = event.data.json();
      console.log('📦 [PUSH] Datos recibidos:', JSON.stringify(pushData, null, 2));
      
      // Construir notificación rica
      notificationConfig = buildRichNotification(pushData);
    } else {
      // Notificación sin datos - usar valores por defecto
      notificationConfig = {
        title: APP_CONFIG.name,
        options: {
          body: 'Tienes una nueva notificación',
          icon: APP_CONFIG.defaultIcon,
          badge: APP_CONFIG.badge,
          tag: `sv-default-${Date.now()}`,
          data: { url: '/notificaciones' },
          vibrate: [100, 50, 100],
          actions: [
            { action: 'open', title: '📖 Ver' }
          ]
        }
      };
    }
  } catch (e) {
    console.error('❌ [PUSH] Error parseando datos:', e);
    // Fallback con texto plano
    notificationConfig = {
      title: APP_CONFIG.name,
      options: {
        body: event.data ? event.data.text() : 'Nueva notificación',
        icon: APP_CONFIG.defaultIcon,
        badge: APP_CONFIG.badge,
        tag: `sv-error-${Date.now()}`,
        data: { url: '/notificaciones' },
        vibrate: [100, 50, 100]
      }
    };
  }
  
  console.log('🎨 [PUSH] Mostrando notificación:', notificationConfig.title);
  
  // Mostrar la notificación
  const showNotificationPromise = self.registration.showNotification(
    notificationConfig.title,
    notificationConfig.options
  );
  
  // Notificar a los clientes abiertos
  const notifyClientsPromise = self.clients.matchAll({ 
    type: 'window', 
    includeUncontrolled: true 
  }).then(clients => {
    console.log(`📢 [PUSH] Notificando a ${clients.length} cliente(s)`);
    clients.forEach(client => {
      client.postMessage({
        type: 'PUSH_RECEIVED',
        notification: {
          title: notificationConfig.title,
          ...notificationConfig.options.data
        }
      });
    });
  });
  
  event.waitUntil(
    Promise.all([showNotificationPromise, notifyClientsPromise])
  );
});

// Evento de click en notificación - Manejo Empresarial
self.addEventListener('notificationclick', (event) => {
  console.log('🖱️ [CLICK] Notificación clickeada');
  console.log('   Tag:', event.notification.tag);
  console.log('   Action:', event.action || 'click general');
  
  const notification = event.notification;
  const action = event.action;
  const notificationData = notification.data || {};
  
  // Cerrar la notificación
  notification.close();
  
  // Manejar acciones específicas
  switch (action) {
    case 'dismiss':
      console.log('👋 [CLICK] Notificación descartada');
      // Solo cerrar, registrar como descartada
      trackNotificationAction(notificationData.notificacion_id, 'dismissed');
      return;
      
    case 'snooze':
    case 'remind':
      console.log('⏰ [CLICK] Posponiendo notificación');
      // Programar recordatorio (si se implementa)
      trackNotificationAction(notificationData.notificacion_id, 'snoozed');
      // Por ahora, solo cerrar
      return;
      
    case 'complete':
      console.log('✓ [CLICK] Marcando como completado');
      trackNotificationAction(notificationData.notificacion_id, 'completed');
      // Podría enviar al servidor que se completó
      return;
      
    case 'reply':
      console.log('💬 [CLICK] Abriendo para responder');
      // Caer a través para abrir la app
      break;
      
    case 'open':
    default:
      console.log('📖 [CLICK] Abriendo notificación');
      trackNotificationAction(notificationData.notificacion_id, 'opened');
      break;
  }
  
  // Determinar la URL a abrir
  let urlToOpen = notificationData.url || '/notificaciones';
  
  // Si hay notificacion_id, añadirlo como parámetro
  if (notificationData.notificacion_id) {
    const separator = urlToOpen.includes('?') ? '&' : '?';
    urlToOpen = `${urlToOpen}${separator}id=${notificationData.notificacion_id}`;
  }
  
  console.log('🔗 [CLICK] URL a abrir:', urlToOpen);
  
  // Abrir/enfocar la app
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then(clientList => {
        // Buscar si ya hay una ventana de la app abierta
        for (const client of clientList) {
          if (client.url.includes(self.location.origin) && 'focus' in client) {
            console.log('📱 [CLICK] Enfocando ventana existente');
            // Navegar a la URL de la notificación
            client.postMessage({
              type: 'NAVIGATE_TO',
              url: urlToOpen,
              notificacion_id: notificationData.notificacion_id,
              action: action || 'open'
            });
            return client.focus();
          }
        }
        
        // Si no hay ventana abierta, abrir una nueva
        console.log('🆕 [CLICK] Abriendo nueva ventana');
        if (self.clients.openWindow) {
          return self.clients.openWindow(urlToOpen);
        }
      })
  );
});

/**
 * Registra una acción de notificación (para analytics)
 */
function trackNotificationAction(notificacionId, action) {
  // Enviar a todos los clientes para que registren la acción
  self.clients.matchAll({ type: 'window' }).then(clients => {
    clients.forEach(client => {
      client.postMessage({
        type: 'NOTIFICATION_ACTION',
        notificacion_id: notificacionId,
        action: action,
        timestamp: Date.now()
      });
    });
  });
}

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
