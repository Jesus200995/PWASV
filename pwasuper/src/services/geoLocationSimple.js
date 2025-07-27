/**
 * Servicio de geolocalización simple y robusto
 * Fallback para cuando el servicio principal falla
 */

/**
 * Obtener ubicación de forma simple y garantizada
 * @returns {Promise<{latitude: number, longitude: number, source: string}>}
 */
export async function obtenerUbicacionSimple() {
  console.log('🔍 Usando servicio de geolocalización simple...');

  // 1. Intentar geolocalización nativa primero
  try {
    if (navigator.geolocation) {
      console.log('📡 Intentando geolocalización nativa...');
      
      const position = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
          resolve,
          reject,
          {
            enableHighAccuracy: true,
            timeout: 20000, // 20 segundos para mayor precisión
            maximumAge: 60000 // 1 minuto para ubicación más fresca
          }
        );
      });

      const result = {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        accuracy: position.coords.accuracy,
        source: 'gps'
      };

      console.log('✅ Ubicación GPS obtenida:', result);
      
      // Guardar en caché simple para uso futuro
      guardarUbicacionSimple(result.latitude, result.longitude);
      
      return result;
    }
  } catch (error) {
    console.warn('⚠️ Geolocalización nativa falló:', error.message);
  }

  // 2. Intentar ubicación del localStorage (caché manual)
  try {
    const cached = localStorage.getItem('ubicacion_cache_simple');
    if (cached) {
      const parsedCache = JSON.parse(cached);
      const age = Date.now() - parsedCache.timestamp;
      
      // Si es menor a 1 hora, usarla (reducido de 24 horas para mayor precisión)
      if (age < 1 * 60 * 60 * 1000) {
        console.log('✅ Usando ubicación del caché simple (menos de 1 hora):', parsedCache);
        return {
          latitude: parsedCache.latitude,
          longitude: parsedCache.longitude,
          accuracy: parsedCache.accuracy || 100,
          source: 'cache'
        };
      } else {
        console.log('⏰ Caché simple expirado (más de 1 hora), obteniendo nueva ubicación');
      }
    }
  } catch (error) {
    console.warn('⚠️ Error leyendo caché simple:', error.message);
  }

  // 3. Ubicación por defecto (Ciudad de México)
  console.log('🏙️ Usando ubicación por defecto...');
  const defaultLocation = {
    latitude: 19.4326,
    longitude: -99.1332,
    source: 'default'
  };

  // Guardar en caché simple
  try {
    localStorage.setItem('ubicacion_cache_simple', JSON.stringify({
      ...defaultLocation,
      timestamp: Date.now()
    }));
  } catch (error) {
    console.warn('⚠️ No se pudo guardar en caché simple:', error.message);
  }

  return defaultLocation;
}

/**
 * Guardar ubicación en caché simple
 * @param {number} latitude 
 * @param {number} longitude 
 * @param {number} accuracy - Precisión opcional
 */
export function guardarUbicacionSimple(latitude, longitude, accuracy = null) {
  try {
    const data = {
      latitude,
      longitude,
      accuracy,
      timestamp: Date.now()
    };
    localStorage.setItem('ubicacion_cache_simple', JSON.stringify(data));
    console.log('💾 Ubicación guardada en caché simple:', data);
  } catch (error) {
    console.warn('⚠️ No se pudo guardar ubicación simple:', error.message);
  }
}

/**
 * Limpiar caché simple
 */
export function limpiarCacheSimple() {
  try {
    localStorage.removeItem('ubicacion_cache_simple');
    console.log('🧹 Caché simple limpiado');
  } catch (error) {
    console.warn('⚠️ Error limpiando caché simple:', error.message);
  }
}
