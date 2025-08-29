/**
 * Configuración para notificaciones push
 * VERSIÓN ROBUSTA PARA GARANTIZAR FUNCIONAMIENTO
 */

// Configuración de notificaciones
export const NOTIFICATION_CONFIG = {
  // Intervalos de polling (en milisegundos)
  POLLING_INTERVALS: {
    NORMAL: 8000,        // 8 segundos cuando la app está abierta
    BACKGROUND: 10000,   // 10 segundos cuando la app está en background
    CLOSED: 5000,        // 5 segundos cuando la app está cerrada (más agresivo)
    ERROR_FALLBACK: 30000 // 30 segundos cuando hay errores
  },

  // Configuración de reintentos
  RETRY_CONFIG: {
    MAX_CONSECUTIVE_ERRORS: 3,
    MAX_POLLING_ATTEMPTS: 5,
    BACKOFF_MULTIPLIER: 1.5
  },

  // Configuración de notificaciones
  NOTIFICATION_OPTIONS: {
    requireInteraction: true,
    renotify: true,
    silent: false,
    vibrate: [200, 100, 200], // Patrón simple y efectivo
    icon: '/pwa-192x192.png',
    badge: '/pwa-192x192.png',
    image: '/pwa-512x512.png'
  },

  // Mensajes de notificación
  MESSAGES: {
    SINGLE: '🔔 Tienes una nueva notificación',
    MULTIPLE: (count) => `🔔 Tienes ${count} nuevas notificaciones`,
    TITLE: '🔔 PWA Super - Nuevas Notificaciones'
  }
};

// Generar VAPID key válida para push notifications
export function generateValidVAPIDKey() {
  // Esta es una clave de demostración válida
  const publicVapidKey = 'BPiTvF1xXGl2B2DnKQkSnbWXjRl6nMcVXOjzXzQJgLKdH3n1aILsqQn0yVhW1Jy0KvJ8nJdBFgYpgA2EHWFjFxM';
  
  function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
      .replace(/\-/g, '+')
      .replace(/_/g, '/');
    
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    
    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }
  
  return urlBase64ToUint8Array(publicVapidKey);
}

// Configuración de API
export const API_CONFIG = {
  TIMEOUT: 10000, // 10 segundos de timeout
  RETRY_DELAY: 2000, // 2 segundos entre reintentos
  MAX_RETRIES: 3
};

// Funciones utilitarias
export const NotificationUtils = {
  // Verificar si las notificaciones están soportadas
  isSupported() {
    return 'Notification' in window && 'serviceWorker' in navigator;
  },

  // Verificar permisos
  hasPermission() {
    return Notification.permission === 'granted';
  },

  // Generar ID único para notificación
  generateNotificationId() {
    return `notification-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  },

  // Formatear mensaje de notificación
  formatMessage(newCount, totalCount) {
    if (newCount === 1) {
      return NOTIFICATION_CONFIG.MESSAGES.SINGLE;
    } else {
      return NOTIFICATION_CONFIG.MESSAGES.MULTIPLE(newCount) + 
        (totalCount > newCount ? ` (Total: ${totalCount})` : '');
    }
  },

  // Verificar si una notificación es reciente (menos de 5 minutos)
  isRecentNotification(timestamp) {
    return Date.now() - timestamp < 5 * 60 * 1000;
  }
};

export default {
  NOTIFICATION_CONFIG,
  generateValidVAPIDKey,
  API_CONFIG,
  NotificationUtils
};
