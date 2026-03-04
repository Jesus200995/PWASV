// ========================================
// COMPOSABLE PARA ESTADÍSTICAS EN TIEMPO REAL
// Técnicas Apple: Polling inteligente, caché optimizado, transiciones suaves
// ========================================

import { ref, onMounted, onUnmounted, computed } from 'vue';
import { API_URL } from '../config/api.js';
import authService from '../services/authService.js';

/**
 * Composable para obtener estadísticas en tiempo real con polling inteligente
 * Inspirado en las técnicas de optimización de Apple:
 * - Polling solo cuando la pestaña está visible
 * - Caché con TTL de 5 segundos
 * - Exponential backoff en errores
 * - Cancelación automática
 * - Animaciones suaves de transición
 */
export function useRealtimeStats(options = {}) {
  const {
    pollingInterval = 5000, // 5 segundos (Apple-style refresh rate)
    enableCache = true,
    cacheTTL = 5000,
    enablePolling = true,
    onError = null
  } = options;

  // Estado reactivo
  const stats = ref({
    asistencias_hoy: 0,
    usuarios_presentes: 0,
    total_asistencias: 0
  });
  
  const isLoading = ref(false);
  const error = ref(null);
  const lastUpdate = ref(null);

  // Caché en memoria
  let cache = null;
  let cacheTimestamp = 0;

  // Control de polling
  let pollingTimer = null;
  let abortController = null;
  let retryCount = 0;
  const maxRetries = 3;

  /**
   * Obtiene estadísticas del endpoint optimizado
   */
  const fetchStats = async (force = false) => {
    // Verificar caché si está habilitado
    if (enableCache && !force && cache && Date.now() - cacheTimestamp < cacheTTL) {
      console.log('📦 Stats desde caché (ultra-rápido)');
      return cache;
    }

    // Cancelar request anterior si existe
    if (abortController) {
      abortController.abort();
    }

    abortController = new AbortController();

    try {
      const territorioFilter = authService.getTerritorioFilter();
      let url = `${API_URL}/estadisticas/rapidas`;
      
      if (territorioFilter) {
        url += `?territorio=${encodeURIComponent(territorioFilter)}`;
      }

      console.time('⚡ Fetch stats rápidas');
      
      const response = await fetch(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        signal: abortController.signal,
        priority: 'high' // Prioridad alta para responsividad
      });

      console.timeEnd('⚡ Fetch stats rápidas');

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      const newStats = data.estadisticas;

      // Actualizar caché
      if (enableCache) {
        cache = newStats;
        cacheTimestamp = Date.now();
      }

      // Resetear contador de reintentos en éxito
      retryCount = 0;
      error.value = null;

      return newStats;

    } catch (err) {
      if (err.name === 'AbortError') {
        console.log('⚠️ Request de stats cancelado');
        return null;
      }

      console.error('❌ Error al obtener stats rápidas:', err);
      error.value = err.message;
      
      if (onError) {
        onError(err);
      }

      // Exponential backoff
      retryCount++;
      if (retryCount < maxRetries) {
        const backoffDelay = Math.min(1000 * Math.pow(2, retryCount), 10000);
        console.log(`🔄 Reintentando en ${backoffDelay}ms (intento ${retryCount}/${maxRetries})`);
        await new Promise(resolve => setTimeout(resolve, backoffDelay));
        return fetchStats(force);
      }

      throw err;
    }
  };

  /**
   * Actualiza las estadísticas y aplica transición suave
   */
  const updateStats = async (force = false) => {
    if (isLoading.value && !force) return;

    isLoading.value = true;

    try {
      const newStats = await fetchStats(force);
      
      if (newStats) {
        // Actualizar con los nuevos valores
        stats.value = {
          asistencias_hoy: newStats.asistencias_hoy || 0,
          usuarios_presentes: newStats.usuarios_presentes || 0,
          total_asistencias: newStats.total_asistencias || 0
        };
        
        lastUpdate.value = new Date();
        console.log('✅ Stats actualizadas:', stats.value);
      }
    } catch (err) {
      console.error('❌ Error al actualizar stats:', err);
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Inicia el polling inteligente
   */
  const startPolling = () => {
    if (!enablePolling) return;

    // Limpiar timer anterior
    stopPolling();

    // Primera carga inmediata
    updateStats();

    // Configurar polling con visibilitychange API (Apple-style)
    const poll = () => {
      // Solo hacer polling si la pestaña está visible
      if (document.hidden) {
        console.log('⏸️ Polling pausado (pestaña oculta)');
        return;
      }

      updateStats();
    };

    // Timer principal
    pollingTimer = setInterval(poll, pollingInterval);

    // Listener para pausar/reanudar cuando cambia visibilidad
    const handleVisibilityChange = () => {
      if (!document.hidden) {
        console.log('▶️ Polling reanudado (pestaña visible)');
        updateStats(true); // Force refresh al volver
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);

    // Guardar referencia para cleanup
    pollingTimer._visibilityHandler = handleVisibilityChange;
  };

  /**
   * Detiene el polling
   */
  const stopPolling = () => {
    if (pollingTimer) {
      clearInterval(pollingTimer);
      
      if (pollingTimer._visibilityHandler) {
        document.removeEventListener('visibilitychange', pollingTimer._visibilityHandler);
      }
      
      pollingTimer = null;
    }

    if (abortController) {
      abortController.abort();
      abortController = null;
    }
  };

  /**
   * Refresca manualmente las estadísticas
   */
  const refresh = () => {
    return updateStats(true);
  };

  /**
   * Limpia el caché
   */
  const clearCache = () => {
    cache = null;
    cacheTimestamp = 0;
  };

  // Computed para tiempo desde última actualización
  const timeSinceUpdate = computed(() => {
    if (!lastUpdate.value) return null;
    const seconds = Math.floor((Date.now() - lastUpdate.value) / 1000);
    if (seconds < 60) return `${seconds}s`;
    const minutes = Math.floor(seconds / 60);
    return `${minutes}m`;
  });

  // Lifecycle hooks
  onMounted(() => {
    if (enablePolling) {
      startPolling();
    }
  });

  onUnmounted(() => {
    stopPolling();
  });

  return {
    stats,
    isLoading,
    error,
    lastUpdate,
    timeSinceUpdate,
    refresh,
    clearCache,
    startPolling,
    stopPolling
  };
}
