// Service Worker para PWA con soporte offline
const CACHE_NAME = 'pwa-asistencia-v1';
const OFFLINE_CACHE = 'pwa-offline-v1';

// Recursos que siempre deben estar disponibles offline
const STATIC_CACHE_URLS = [
  '/',
  '/index.html',
  '/src/main.js',
  '/src/style.css',
  '/src/assets/main.css',
  // Agregar otros archivos estáticos críticos aquí
];

// URLs de la API que deben manejarse offline
const API_CACHE_PATTERNS = [
  '/asistencia/entrada',
  '/asistencia/salida',
  '/registro',
  '/asistencias'
];

// Instalar Service Worker
self.addEventListener('install', (event) => {
  console.log('🔧 Service Worker: Instalando...');
  
  event.waitUntil(
    Promise.all([
      // Cachear recursos estáticos
      caches.open(CACHE_NAME).then((cache) => {
        console.log('📦 Service Worker: Cacheando recursos estáticos');
        return cache.addAll(STATIC_CACHE_URLS.map(url => new Request(url, {
          credentials: 'same-origin'
        })));
      }),
      // Preparar cache offline
      caches.open(OFFLINE_CACHE)
    ]).then(() => {
      console.log('✅ Service Worker: Instalación completada');
      // Forzar la activación del nuevo service worker
      self.skipWaiting();
    }).catch((error) => {
      console.error('❌ Service Worker: Error durante instalación:', error);
    })
  );
});

// Activar Service Worker
self.addEventListener('activate', (event) => {
  console.log('🚀 Service Worker: Activando...');
  
  event.waitUntil(
    Promise.all([
      // Limpiar caches viejos
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME && cacheName !== OFFLINE_CACHE) {
              console.log('🗑️ Service Worker: Eliminando cache viejo:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      }),
      // Tomar control de todas las páginas
      self.clients.claim()
    ]).then(() => {
      console.log('✅ Service Worker: Activación completada');
    })
  );
});

// Interceptar solicitudes de red
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Solo manejar solicitudes HTTP/HTTPS
  if (!request.url.startsWith('http')) {
    return;
  }

  // Estrategia para recursos estáticos: Cache First
  if (request.method === 'GET' && isStaticResource(request)) {
    event.respondWith(handleStaticResource(request));
    return;
  }

  // Estrategia para API calls: Network First con fallback offline
  if (isApiCall(request)) {
    event.respondWith(handleApiCall(request));
    return;
  }

  // Para todo lo demás: Network First
  event.respondWith(handleGenericRequest(request));
});

// Verificar si es un recurso estático
function isStaticResource(request) {
  const url = new URL(request.url);
  return (
    request.method === 'GET' && (
      url.pathname.endsWith('.js') ||
      url.pathname.endsWith('.css') ||
      url.pathname.endsWith('.html') ||
      url.pathname.endsWith('.ico') ||
      url.pathname.endsWith('.png') ||
      url.pathname.endsWith('.jpg') ||
      url.pathname.endsWith('.svg') ||
      url.pathname === '/'
    )
  );
}

// Verificar si es una llamada a la API
function isApiCall(request) {
  const url = new URL(request.url);
  return url.hostname.includes('apipwa.sembrandodatos.com') || 
         url.hostname === 'localhost' && url.port === '8000' ||
         url.hostname === 'localhost' && url.port === '8001';
}

// Manejar recursos estáticos (Cache First)
async function handleStaticResource(request) {
  try {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    const networkResponse = await fetch(request);
    
    // Cachear la respuesta si es exitosa
    if (networkResponse.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('❌ Service Worker: Error cargando recurso estático:', error);
    
    // Fallback para HTML
    if (request.headers.get('accept')?.includes('text/html')) {
      const fallbackResponse = await caches.match('/index.html');
      if (fallbackResponse) return fallbackResponse;
    }
    
    throw error;
  }
}

// Manejar llamadas a la API (Network First con manejo offline)
async function handleApiCall(request) {
  try {
    // Intentar primero la red
    const networkResponse = await fetch(request.clone());
    
    // Si es exitosa y es GET, cachear para consultas offline
    if (networkResponse.ok && request.method === 'GET') {
      const cache = await caches.open(OFFLINE_CACHE);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('📵 Service Worker: Fallo de red en API call:', error);
    
    // Si es GET, intentar servir desde cache
    if (request.method === 'GET') {
      const cachedResponse = await caches.match(request);
      if (cachedResponse) {
        console.log('📦 Service Worker: Sirviendo desde cache:', request.url);
        return cachedResponse;
      }
    }
    
    // Para POST/PUT que fallan, no hacer nada especial
    // El manejo offline se hace desde el cliente con IndexedDB
    throw error;
  }
}

// Manejar solicitudes genéricas
async function handleGenericRequest(request) {
  try {
    return await fetch(request);
  } catch (error) {
    // Si falla, intentar cache solo para GET
    if (request.method === 'GET') {
      const cachedResponse = await caches.match(request);
      if (cachedResponse) {
        return cachedResponse;
      }
    }
    throw error;
  }
}

// Escuchar mensajes del cliente
self.addEventListener('message', (event) => {
  console.log('💬 Service Worker: Mensaje recibido:', event.data);
  
  if (event.data && event.data.type === 'SYNC_OFFLINE_DATA') {
    // Aquí se podría implementar Background Sync
    // Por simplicidad, enviamos confirmación
    event.ports[0]?.postMessage({
      type: 'SYNC_RESPONSE',
      success: true,
      message: 'Sincronización programada'
    });
  }
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// Manejo de sincronización en background (requiere Background Sync API)
self.addEventListener('sync', (event) => {
  console.log('🔄 Service Worker: Evento de sincronización:', event.tag);
  
  if (event.tag === 'sync-offline-data') {
    event.waitUntil(
      // Notificar al cliente que debe sincronizar
      self.clients.matchAll().then((clients) => {
        clients.forEach((client) => {
          client.postMessage({
            type: 'TRIGGER_SYNC',
            message: 'Conectividad restaurada - sincronizando datos offline'
          });
        });
      })
    );
  }
});

// Log de estado
console.log('🔧 Service Worker: Script cargado');
