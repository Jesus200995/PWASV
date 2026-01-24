// Utilidad para verificar conexión a internet
export async function checkInternetConnection() {
  // Si estamos en localhost, primero verificar si el servidor local está disponible
  const environment = detectEnvironment();
  
  if (environment === 'development') {
    // En desarrollo, verificar primero si el servidor local responde
    try {
      const localUrl = getApiUrl();
      const response = await fetch(`${localUrl}/health`, {
        method: 'HEAD',
        cache: 'no-store',
        signal: AbortSignal.timeout(2000) // 2 segundos timeout
      });
      
      if (response.ok || response.status === 404) {
        // Si el servidor local responde (aunque sea 404), consideramos que hay "conexión"
        console.log('✅ Servidor local disponible en:', localUrl);
        return true;
      }
    } catch (error) {
      console.warn('⚠️ Servidor local no responde, verificando internet externa...');
    }
  }
  
  // Si no es desarrollo o el servidor local no responde, verificar conexión externa
  return new Promise((resolve) => {
    fetch('https://www.google.com', { 
      mode: 'no-cors',
      cache: 'no-store',
      method: 'HEAD'
    })
      .then(() => resolve(true))
      .catch(() => resolve(false));
  });
}

// Mensaje de información cuando no hay conexión
export function getOfflineMessage() {
  return "Sin conexión. Los registros de actividades, entrada y salida se guardarán automáticamente y serán enviados cuando se restablezca la conexión.";
}

// Configuración de URLs de API
const API_URLS = {
  development: ["http://localhost:8000", "http://localhost:8001"],
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

// Exportar API_URL dinámica basada en el entorno actual
export const API_URL = getApiUrl();

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

// URL dinámica para casos donde se necesite la mejor conexión disponible (uso interno)
const INTERNAL_API_URL = getApiUrl();

// URL dinámica para casos donde se necesita la mejor conexión disponible
export let DYNAMIC_API_URL = INTERNAL_API_URL;
