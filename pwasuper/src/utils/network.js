// Utilidad para verificar conexión a internet
export function checkInternetConnection() {
  return new Promise((resolve) => {
    // Intentar hacer una petición a un servicio externo
    fetch('https://www.google.com', { 
      mode: 'no-cors',
      cache: 'no-store',
      method: 'HEAD',
      timeout: 5000 
    })
      .then(() => resolve(true))
      .catch(() => resolve(false));
  });
}

// Mensaje de error cuando no hay conexión
export function getOfflineMessage() {
  return "No hay conexión a internet. Esta función requiere conexión para funcionar correctamente.";
}

// URL de la API - CAMBIADA A PRODUCCIÓN
export const API_URL = "https://apipwa.sembrandodatos.com";
