/**
 * Servicio de Geolocalización Offline
 * Maneja la obtención de ubicación incluso sin conexión a internet
 * Cachea ubicaciones y las sincroniza cuando hay conexión
 */

class GeoLocationService {
  constructor() {
    this.lastKnownLocation = null;
    this.locationCache = [];
    this.maxCacheSize = 50; // Máximo de ubicaciones en caché
    this.loadFromStorage();
    
    // Intentar obtener ubicación inicial de forma silenciosa
    this.initializeLocation();
  }

  /**
   * Cargar datos del localStorage
   */
  loadFromStorage() {
    try {
      const stored = localStorage.getItem('geoLocationCache');
      if (stored) {
        const data = JSON.parse(stored);
        this.lastKnownLocation = data.lastKnownLocation;
        this.locationCache = data.locationCache || [];
      }
    } catch (error) {
      console.warn('Error cargando caché de ubicaciones:', error);
    }
  }

  /**
   * Guardar datos al localStorage
   */
  saveToStorage() {
    try {
      const data = {
        lastKnownLocation: this.lastKnownLocation,
        locationCache: this.locationCache.slice(-this.maxCacheSize) // Solo guardar las últimas N ubicaciones
      };
      localStorage.setItem('geoLocationCache', JSON.stringify(data));
    } catch (error) {
      console.warn('Error guardando caché de ubicaciones:', error);
    }
  }

  /**
   * Inicializar ubicación de forma silenciosa al cargar el servicio
   */
  initializeLocation() {
    // Solo intentar si el navegador soporta geolocalización
    if (!navigator.geolocation) {
      console.log('📍 Navegador no soporta geolocalización, usando ubicación por defecto');
      // Agregar ubicación por defecto para México
      this.setDefaultLocation();
      return;
    }

    // Intentar obtener ubicación de forma silenciosa (no mostrar errores)
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const locationData = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          accuracy: position.coords.accuracy,
          timestamp: position.timestamp
        };
        
        // Actualizar sin hacer ruido
        this.updateLastKnownLocation(locationData);
        console.log('📍 Ubicación inicial obtenida silenciosamente');
      },
      (error) => {
        // Fallar silenciosamente y usar ubicación por defecto
        console.log('📍 No se pudo obtener ubicación inicial, usando por defecto:', error.message);
        this.setDefaultLocation();
      },
      {
        enableHighAccuracy: true, // Usar alta precisión desde el inicio
        timeout: 10000, // Timeout más generoso para inicialización
        maximumAge: 300000 // Permitir ubicaciones de hasta 5 minutos
      }
    );
  }

  /**
   * Establecer ubicación por defecto (Ciudad de México como ejemplo)
   */
  setDefaultLocation() {
    const defaultLocation = {
      latitude: 19.4326, // Ciudad de México
      longitude: -99.1332,
      accuracy: 10000, // 10km de precisión estimada
      timestamp: Date.now(),
      isDefault: true
    };
    
    this.updateLastKnownLocation(defaultLocation);
    console.log('📍 Ubicación por defecto establecida (Ciudad de México)');
  }

  /**
   * Obtener ubicación actual con fallback a caché
   * @param {Object} options - Opciones de geolocalización
   * @returns {Promise} Promise con la ubicación
   */
  async getCurrentLocation(options = {}) {
    const defaultOptions = {
      enableHighAccuracy: true,
      timeout: 25000, // 25 segundos para mayor precisión
      maximumAge: 60000, // 1 minuto para obtener ubicación más fresca
      useCache: true, // Permitir usar caché como fallback
      ...options
    };

    return new Promise((resolve, reject) => {
      // Verificar si el navegador soporta geolocalización
      if (!navigator.geolocation) {
        // Si no hay soporte y tenemos ubicación en caché, usarla
        if (defaultOptions.useCache && this.lastKnownLocation) {
          console.warn('Navegador no soporta geolocalización, usando ubicación en caché');
          resolve({
            ...this.lastKnownLocation,
            fromCache: true,
            timestamp: Date.now()
          });
          return;
        }
        reject(new Error('Tu navegador no soporta geolocalización'));
        return;
      }

      // Variables para manejar timeouts y fallbacks
      let resolved = false;
      let fallbackTimer = null;

      // Función para resolver con caché si está disponible
      const resolveWithCache = () => {
        if (!resolved && defaultOptions.useCache && this.lastKnownLocation) {
          resolved = true;
          console.warn('Usando ubicación en caché como fallback');
          resolve({
            ...this.lastKnownLocation,
            fromCache: true,
            timestamp: Date.now()
          });
          return true;
        }
        return false;
      };

      // Configurar fallback a caché después de un tiempo
      if (defaultOptions.useCache && this.lastKnownLocation) {
        fallbackTimer = setTimeout(() => {
          if (!resolved) {
            console.warn('Geolocalización tardando mucho, usando caché');
            resolveWithCache();
          }
        }, Math.min(defaultOptions.timeout, 15000)); // Usar caché después de 15 segundos máximo
      }

      // Intentar obtener ubicación actual
      navigator.geolocation.getCurrentPosition(
        (position) => {
          if (resolved) return;
          resolved = true;
          
          if (fallbackTimer) {
            clearTimeout(fallbackTimer);
          }

          const locationData = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            accuracy: position.coords.accuracy,
            timestamp: position.timestamp,
            fromCache: false
          };

          // Guardar como última ubicación conocida
          this.updateLastKnownLocation(locationData);

          resolve(locationData);
        },
        (error) => {
          if (resolved) return;
          
          if (fallbackTimer) {
            clearTimeout(fallbackTimer);
          }

          console.error('Error de geolocalización:', error);

          // Intentar usar caché como fallback
          if (resolveWithCache()) {
            return;
          }

          // Si no hay caché disponible, rechazar con error mejorado
          let errorMessage = 'Error obteniendo ubicación';
          switch (error.code) {
            case error.PERMISSION_DENIED:
              errorMessage = 'Permisos de ubicación denegados. Por favor, habilita el acceso a la ubicación en tu navegador.';
              break;
            case error.POSITION_UNAVAILABLE:
              errorMessage = 'Ubicación no disponible. Verifica que tengas GPS activado.';
              break;
            case error.TIMEOUT:
              errorMessage = 'Tiempo de espera agotado obteniendo ubicación.';
              break;
            default:
              errorMessage = `Error de ubicación: ${error.message}`;
          }

          resolved = true;
          reject(new Error(errorMessage));
        },
        {
          enableHighAccuracy: defaultOptions.enableHighAccuracy,
          timeout: defaultOptions.timeout,
          maximumAge: defaultOptions.maximumAge
        }
      );
    });
  }

  /**
   * Actualizar la última ubicación conocida
   * @param {Object} locationData - Datos de ubicación
   */
  updateLastKnownLocation(locationData) {
    this.lastKnownLocation = {
      latitude: locationData.latitude,
      longitude: locationData.longitude,
      accuracy: locationData.accuracy,
      timestamp: locationData.timestamp || Date.now()
    };

    // Agregar al caché
    this.addToCache(this.lastKnownLocation);
    this.saveToStorage();
  }

  /**
   * Agregar ubicación al caché
   * @param {Object} locationData - Datos de ubicación
   */
  addToCache(locationData) {
    const cacheEntry = {
      ...locationData,
      id: Date.now() + Math.random()
    };

    this.locationCache.push(cacheEntry);

    // Mantener solo las últimas ubicaciones
    if (this.locationCache.length > this.maxCacheSize) {
      this.locationCache = this.locationCache.slice(-this.maxCacheSize);
    }
  }

  /**
   * Obtener la última ubicación conocida
   * @returns {Object|null} Última ubicación o null
   */
  getLastKnownLocation() {
    return this.lastKnownLocation;
  }

  /**
   * Obtener el historial de ubicaciones
   * @returns {Array} Array de ubicaciones
   */
  getLocationHistory() {
    return [...this.locationCache];
  }

  /**
   * Verificar si hay una ubicación válida en caché
   * @param {number} maxAge - Edad máxima en millisegundos (default: 1 hora)
   * @returns {boolean} True si hay ubicación válida
   */
  hasValidCachedLocation(maxAge = 3600000) { // 1 hora por defecto
    if (!this.lastKnownLocation) return false;
    
    const age = Date.now() - this.lastKnownLocation.timestamp;
    return age <= maxAge;
  }

  /**
   * Limpiar caché de ubicaciones
   */
  clearCache() {
    this.lastKnownLocation = null;
    this.locationCache = [];
    localStorage.removeItem('geoLocationCache');
  }

  /**
   * Obtener ubicación con estrategia inteligente
   * Garantiza siempre devolver una ubicación válida (funciona offline)
   * @param {Object} options - Opciones
   * @returns {Promise} Promise con ubicación
   */
  async getLocationSmart(options = {}) {
    try {
      // Intentar obtener ubicación actual primero con configuración optimizada
      const location = await this.getCurrentLocation({
        timeout: 20000, // 20 segundos para mayor precisión
        enableHighAccuracy: true,
        useCache: true,
        ...options
      });
      
      return location;
    } catch (error) {
      console.warn('Error en getCurrentLocation:', error.message);
      
      // Si hay ubicación en caché, usarla (funciona offline)
      if (this.lastKnownLocation) {
        console.log('🔄 Usando ubicación en caché como fallback (modo offline)');
        return {
          ...this.lastKnownLocation,
          fromCache: true,
          timestamp: Date.now()
        };
      }
      
      // Si no hay caché, establecer ubicación por defecto y usarla (siempre funciona)
      console.log('🆘 Sin caché disponible, estableciendo ubicación por defecto (modo offline)');
      this.setDefaultLocation();
      
      return {
        ...this.lastKnownLocation,
        fromCache: true,
        isDefault: true,
        timestamp: Date.now()
      };
    }
  }

  /**
   * Obtener información del estado del servicio
   * @returns {Object} Estado del servicio
   */
  getStatus() {
    return {
      hasGeolocationSupport: 'geolocation' in navigator,
      hasLastKnownLocation: !!this.lastKnownLocation,
      lastLocationAge: this.lastKnownLocation ? 
        Date.now() - this.lastKnownLocation.timestamp : null,
      cacheSize: this.locationCache.length,
      isOnline: navigator.onLine
    };
  }
}

// Crear instancia singleton
const geoLocationService = new GeoLocationService();

// Hacer disponible globalmente para debugging
if (typeof window !== 'undefined') {
  window.geoLocationService = geoLocationService;
}

export default geoLocationService;
