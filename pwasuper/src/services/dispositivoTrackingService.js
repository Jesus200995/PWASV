/**
 * 📱 Servicio de Tracking de Dispositivos
 * 
 * Este servicio detecta y registra el tipo de dispositivo del usuario
 * de forma reactiva y en tiempo real, cada vez que abre la app.
 * 
 * Funciona para:
 * - Usuarios haciendo login
 * - Usuarios ya logueados que abren la app
 * - Cualquier momento que se monta la aplicación
 */

import axios from 'axios';
import { API_URL, getBestApiUrl } from '../utils/network.js';

// Cache de la URL de API
let cachedApiUrl = null;

/**
 * Detecta el tipo de dispositivo del usuario
 * @returns {string} 'Android', 'iOS', 'Desktop', o 'Desconocido'
 */
export function detectarDispositivo() {
  const userAgent = navigator.userAgent || navigator.vendor || window.opera;
  
  // Detectar iOS (iPhone, iPad, iPod)
  if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {
    return 'iOS';
  }
  
  // Detectar Android
  if (/android/i.test(userAgent)) {
    return 'Android';
  }
  
  // Detectar Desktop (Windows, Mac, Linux)
  if (/Windows|Macintosh|Linux/.test(userAgent) && !/android/i.test(userAgent)) {
    return 'Desktop';
  }
  
  return 'Desconocido';
}

/**
 * Obtiene información detallada del dispositivo
 * @returns {Object} Información completa del dispositivo
 */
export function obtenerInfoDispositivo() {
  const userAgent = navigator.userAgent || '';
  const dispositivo = detectarDispositivo();
  
  // Detectar navegador
  let navegador = 'Desconocido';
  if (/chrome/i.test(userAgent) && !/edg/i.test(userAgent)) {
    navegador = 'Chrome';
  } else if (/safari/i.test(userAgent) && !/chrome/i.test(userAgent)) {
    navegador = 'Safari';
  } else if (/firefox/i.test(userAgent)) {
    navegador = 'Firefox';
  } else if (/edg/i.test(userAgent)) {
    navegador = 'Edge';
  } else if (/opera|opr/i.test(userAgent)) {
    navegador = 'Opera';
  }
  
  // Detectar si es PWA instalada
  const esPWA = window.matchMedia('(display-mode: standalone)').matches || 
                window.navigator.standalone === true;
  
  return {
    dispositivo,
    navegador,
    userAgent,
    esPWA,
    pantalla: {
      ancho: window.screen.width,
      alto: window.screen.height
    },
    timestamp: new Date().toISOString()
  };
}

/**
 * Obtén la mejor URL de API disponible
 */
async function getApiUrl() {
  if (cachedApiUrl) return cachedApiUrl;
  
  try {
    cachedApiUrl = await getBestApiUrl();
  } catch (error) {
    cachedApiUrl = API_URL;
  }
  
  return cachedApiUrl;
}

/**
 * Envía información del dispositivo al backend
 * @param {number} usuarioId - ID del usuario
 * @returns {Promise} Resultado de la operación
 */
export async function enviarInfoDispositivo(usuarioId) {
  if (!usuarioId) {
    console.log('📱 [Tracking] No hay usuario logueado, omitiendo tracking');
    return null;
  }
  
  try {
    const info = obtenerInfoDispositivo();
    const apiUrl = await getApiUrl();
    
    const response = await axios.post(`${apiUrl}/actualizar_dispositivo`, {
      usuario_id: usuarioId,
      dispositivo: info.dispositivo,
      user_agent: info.userAgent
    }, {
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    console.log(`📱 [Tracking] Dispositivo registrado: ${info.dispositivo} | PWA: ${info.esPWA ? 'Sí' : 'No'}`);
    return response.data;
  } catch (error) {
    // No mostrar error al usuario, es información estadística
    console.warn('📱 [Tracking] No se pudo actualizar dispositivo:', error.message);
    return null;
  }
}

/**
 * Registra el dispositivo del usuario actual
 * Busca el usuario en localStorage y envía la información
 * @returns {Promise} Resultado de la operación
 */
export async function registrarDispositivoActual() {
  try {
    const storedUser = localStorage.getItem('user');
    
    if (!storedUser) {
      console.log('📱 [Tracking] Sin usuario logueado, tracking pospuesto');
      return null;
    }
    
    const user = JSON.parse(storedUser);
    const usuarioId = user.id || user.usuario_id;
    
    if (!usuarioId) {
      console.log('📱 [Tracking] Usuario sin ID válido');
      return null;
    }
    
    return await enviarInfoDispositivo(usuarioId);
  } catch (error) {
    console.warn('📱 [Tracking] Error al registrar dispositivo:', error.message);
    return null;
  }
}

/**
 * Inicia tracking periódico del dispositivo
 * Útil para mantener actualizada la información
 * @param {number} intervaloMs - Intervalo en milisegundos (default: 5 minutos)
 * @returns {number} ID del intervalo para poder detenerlo
 */
export function iniciarTrackingPeriodico(intervaloMs = 300000) {
  // Registrar inmediatamente
  registrarDispositivoActual();
  
  // Luego periódicamente
  const intervalId = setInterval(registrarDispositivoActual, intervaloMs);
  
  console.log(`📱 [Tracking] Tracking periódico iniciado (cada ${intervaloMs / 1000}s)`);
  
  return intervalId;
}

/**
 * Detiene el tracking periódico
 * @param {number} intervalId - ID del intervalo a detener
 */
export function detenerTrackingPeriodico(intervalId) {
  if (intervalId) {
    clearInterval(intervalId);
    console.log('📱 [Tracking] Tracking periódico detenido');
  }
}

// Exportar servicio como objeto
export const dispositivoTrackingService = {
  detectarDispositivo,
  obtenerInfoDispositivo,
  enviarInfoDispositivo,
  registrarDispositivoActual,
  iniciarTrackingPeriodico,
  detenerTrackingPeriodico
};

export default dispositivoTrackingService;
