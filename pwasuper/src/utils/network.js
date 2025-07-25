// Utilidad para verificar conexión a internet
export function checkInternetConnection() {
  return new Promise((resolve) => {
    // Verificar primero navigator.onLine
    if (!navigator.onLine) {
      resolve(false);
      return;
    }

    // Intentar hacer una petición a un servicio externo
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    fetch('https://www.google.com', { 
      mode: 'no-cors',
      cache: 'no-store',
      method: 'HEAD',
      signal: controller.signal
    })
      .then(() => {
        clearTimeout(timeoutId);
        resolve(true);
      })
      .catch(() => {
        clearTimeout(timeoutId);
        resolve(false);
      });
  });
}

// Verificación más robusta de conectividad
export async function checkApiConnectivity() {
  try {
    if (!navigator.onLine) return false;
    
    const apiUrl = await getBestApiUrl();
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 8000);

    const response = await fetch(`${apiUrl}/debug/usuarios-estructura`, {
      method: 'HEAD',
      signal: controller.signal,
      cache: 'no-store'
    });

    clearTimeout(timeoutId);
    return response.ok;
  } catch (error) {
    console.log('❌ Sin conectividad con API:', error.message);
    return false;
  }
}

// Mensaje de error cuando no hay conexión
export function getOfflineMessage() {
  return "No hay conexión a internet. Esta función requiere conexión para funcionar correctamente.";
}

// Estados de conectividad
export const ConnectionStatus = {
  ONLINE: 'online',
  OFFLINE: 'offline',
  CHECKING: 'checking',
  LIMITED: 'limited'
};

// Monitor de conectividad mejorado
class ConnectivityMonitor {
  constructor() {
    this.status = ConnectionStatus.CHECKING;
    this.listeners = new Set();
    this.checkInterval = null;
    this.lastCheck = null;
    this.consecutiveFailures = 0;
    
    this.init();
  }

  init() {
    // Verificar estado inicial
    this.checkConnectivity();
    
    // Escuchar eventos de conectividad del navegador
    window.addEventListener('online', () => {
      console.log('🌐 Evento: Conexión restaurada');
      this.handleOnlineEvent();
    });

    window.addEventListener('offline', () => {
      console.log('📴 Evento: Conexión perdida');
      this.handleOfflineEvent();
    });

    // Verificación periódica más inteligente
    this.startPeriodicCheck();
  }

  async checkConnectivity() {
    this.status = ConnectionStatus.CHECKING;
    this.notifyListeners();

    try {
      const isConnected = await checkApiConnectivity();
      const newStatus = isConnected ? ConnectionStatus.ONLINE : ConnectionStatus.OFFLINE;
      
      if (newStatus !== this.status) {
        console.log(`🔄 Cambio de conectividad: ${this.status} → ${newStatus}`);
        this.status = newStatus;
        this.lastCheck = Date.now();
        
        if (newStatus === ConnectionStatus.ONLINE) {
          this.consecutiveFailures = 0;
        } else {
          this.consecutiveFailures++;
        }
        
        this.notifyListeners();
      }
    } catch (error) {
      console.error('❌ Error verificando conectividad:', error);
      this.status = ConnectionStatus.OFFLINE;
      this.consecutiveFailures++;
      this.notifyListeners();
    }
  }

  handleOnlineEvent() {
    // Verificar conectividad real cuando el navegador dice que hay conexión
    setTimeout(() => this.checkConnectivity(), 1000);
  }

  handleOfflineEvent() {
    this.status = ConnectionStatus.OFFLINE;
    this.consecutiveFailures++;
    this.notifyListeners();
  }

  startPeriodicCheck() {
    // Intervalo adaptativo basado en el estado
    const getInterval = () => {
      if (this.status === ConnectionStatus.OFFLINE) {
        // Más frecuente cuando está offline para detectar reconexión rápidamente
        return Math.min(5000 + (this.consecutiveFailures * 2000), 30000);
      }
      // Menos frecuente cuando está online
      return 30000;
    };

    const scheduleNext = () => {
      this.checkInterval = setTimeout(() => {
        this.checkConnectivity().finally(() => scheduleNext());
      }, getInterval());
    };

    scheduleNext();
  }

  addListener(callback) {
    this.listeners.add(callback);
    // Notificar estado actual inmediatamente
    callback(this.status);
    
    return () => this.listeners.delete(callback);
  }

  notifyListeners() {
    this.listeners.forEach(callback => {
      try {
        callback(this.status);
      } catch (error) {
        console.error('❌ Error en listener de conectividad:', error);
      }
    });
  }

  isOnline() {
    return this.status === ConnectionStatus.ONLINE;
  }

  getStatus() {
    return this.status;
  }

  forceCheck() {
    return this.checkConnectivity();
  }

  destroy() {
    if (this.checkInterval) {
      clearTimeout(this.checkInterval);
    }
    this.listeners.clear();
  }
}

// Instancia singleton del monitor
const connectivityMonitor = new ConnectivityMonitor();

export { connectivityMonitor };
export { ConnectivityMonitor };

// Configuración de URLs de API
const API_URLS = {
  development: ["http://localhost:8001", "http://localhost:8000"],
  production: "https://apipwa.sembrandodatos.com"
};

// Función para detectar automáticamente el entorno
function detectEnvironment() {
  // Si estamos en localhost, usar desarrollo
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'development';
  }
  // Si no, usar producción
  return 'production';
}

// Función para obtener la URL de la API según el entorno
function getApiUrl() {
  const environment = detectEnvironment();
  const urls = API_URLS[environment];
  // Si hay múltiples URLs, devolver la primera
  return Array.isArray(urls) ? urls[0] : urls;
}

// Función para obtener todas las URLs de desarrollo
function getAllDevelopmentUrls() {
  return Array.isArray(API_URLS.development) ? API_URLS.development : [API_URLS.development];
}

// Función para probar conectividad con un servidor específico
async function testServerConnection(url) {
  try {
    const response = await fetch(`${url}/debug/usuarios-estructura`, {
      method: 'GET',
      timeout: 5000,
      headers: {
        'Content-Type': 'application/json'
      }
    });
    return response.ok;
  } catch (error) {
    console.log(`❌ Error conectando a ${url}:`, error);
    return false;
  }
}

// Función para obtener la mejor URL disponible
export async function getBestApiUrl() {
  const environment = detectEnvironment();
  
  if (environment === 'development') {
    // Probar todas las URLs de desarrollo
    const devUrls = getAllDevelopmentUrls();
    for (const url of devUrls) {
      const works = await testServerConnection(url);
      if (works) {
        console.log(`✅ Conectado a servidor de desarrollo: ${url}`);
        return url;
      }
    }
    
    // Si ninguna URL de desarrollo funciona, probar producción
    const productionWorks = await testServerConnection(API_URLS.production);
    if (productionWorks) {
      console.log(`✅ Conectado a servidor de producción: ${API_URLS.production}`);
      return API_URLS.production;
    }
  } else {
    // Probar producción primero
    const productionWorks = await testServerConnection(API_URLS.production);
    if (productionWorks) {
      console.log(`✅ Conectado a servidor de producción: ${API_URLS.production}`);
      return API_URLS.production;
    }
    
    // Si producción falla, probar desarrollo
    const devUrls = getAllDevelopmentUrls();
    for (const url of devUrls) {
      const works = await testServerConnection(url);
      if (works) {
        console.log(`✅ Conectado a servidor de desarrollo alternativo: ${url}`);
        return url;
      }
    }
  }
  
  // Si todo falla, devolver la URL primaria
  const primaryUrl = getApiUrl();
  console.log(`❌ Ningún servidor disponible, usando ${primaryUrl} por defecto`);
  return primaryUrl;
}

// URL de la API - Se determina automáticamente
export const API_URL = getApiUrl();

// URL dinámica para casos donde se necesita la mejor conexión disponible
export let DYNAMIC_API_URL = API_URL;
