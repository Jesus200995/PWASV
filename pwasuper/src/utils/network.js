// Utilidad para verificar conexión a internet
export async function checkInternetConnection() {
  // Si el OS/navegador dice que no hay red, no hay nada que verificar
  if (!navigator.onLine) {
    return false;
  }

  const environment = detectEnvironment();
  const apiUrl = getApiUrl();

  // Intentar verificar el endpoint /health de la API.
  // Si falla pero navigator.onLine es true, asumir online y dejar que
  // el API call real maneje el error (guarda offline si realmente falla).
  // Esto evita falsos "Sin conexión" en WiFi donde /health puede fallar
  // por timeout, SSL inspection, o bloqueo de ruta específica.
  try {
    const response = await fetch(`${apiUrl}/health`, {
      method: 'GET',
      cache: 'no-store',
      signal: AbortSignal.timeout(environment === 'development' ? 3000 : 10000)
    });
    // Cualquier respuesta HTTP (incluso 4xx/5xx) significa que llegamos al servidor
    return true;
  } catch (error) {
    // Fetch falló: timeout, SSL inválido, red bloqueada, etc.
    console.warn('⚠️ API health check falló:', error?.message || error);
    // Si el navegador confirma que hay internet, confiar en ello.
    // Los uploads intentarán enviarse; si fallan, se guardan offline.
    return navigator.onLine;
  }
}

// Mensaje de información cuando no hay conexión
export function getOfflineMessage() {
  return "Sin conexión. Los registros de actividades, entrada y salida se guardarán automáticamente y serán enviados cuando se restablezca la conexión.";
}

// Configuración de URLs de API
// En producción usamos URL relativa (/api) para que las peticiones vayan por el mismo dominio
// (app.sembrandodatos.com) y usen el certificado ZeroSSL (compatible Android 4.x+).
// Esto elimina ERR_CERT_AUTHORITY_INVALID en redes privadas y dispositivos Android antiguos.
const API_URLS = {
  development: ["http://localhost:8000", "http://localhost:8001"],
  production: "/api"
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
    const devUrls = getAllDevelopmentUrls();
    for (const url of devUrls) {
      const works = await testServerConnection(url);
      if (works) {
        console.log(`✅ Conectado a servidor de desarrollo: ${url}`);
        return url;
      }
    }
  }

  // En producción siempre usar la URL relativa /api (mismo dominio, cert ZeroSSL)
  return getApiUrl();
}

// URL dinámica para casos donde se necesite la mejor conexión disponible (uso interno)
const INTERNAL_API_URL = getApiUrl();

// URL dinámica para casos donde se necesita la mejor conexión disponible
export let DYNAMIC_API_URL = INTERNAL_API_URL;
