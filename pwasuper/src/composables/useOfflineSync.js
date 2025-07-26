// Composable para manejar conectividad y sincronización offline
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { checkInternetConnection } from '../utils/network.js';
import offlineService from '../services/offlineService.js';
import asistenciasService from '../services/asistenciasService.js';

/**
 * Composable para manejar el estado offline y sincronización automática
 */
export function useOfflineSync() {
  // Estado reactivo
  const isOnline = ref(navigator.onLine);
  const isCheckingConnection = ref(false);
  const isSyncing = ref(false);
  const syncProgress = ref({ total: 0, procesados: 0, errores: 0 });
  const pendingRecords = ref({ entradas: 0, salidas: 0, total: 0 });
  const lastSyncAttempt = ref(null);
  const syncMessage = ref('');

  // Intervalos y timeouts
  let connectionCheckInterval = null;
  let syncTimeout = null;
  let syncRetryTimeout = null;

  // Estado computado
  const hasPendingRecords = computed(() => pendingRecords.value.total > 0);
  const shouldShowSyncStatus = computed(() => hasPendingRecords.value || isSyncing.value);

  /**
   * Verifica la conectividad a internet
   */
  async function checkConnection() {
    if (isCheckingConnection.value) return isOnline.value;
    
    isCheckingConnection.value = true;
    try {
      const connected = await checkInternetConnection();
      const wasOffline = !isOnline.value;
      
      isOnline.value = connected;
      
      // Si acabamos de conectarnos, intentar sincronizar
      if (connected && wasOffline) {
        console.log('🌐 Conexión recuperada, intentando sincronizar...');
        await attemptSync();
      }
      
      return connected;
    } catch (error) {
      console.error('❌ Error verificando conexión:', error);
      isOnline.value = false;
      return false;
    } finally {
      isCheckingConnection.value = false;
    }
  }

  /**
   * Actualiza el contador de registros pendientes
   */
  async function updatePendingCount() {
    try {
      const stats = await offlineService.obtenerEstadisticas();
      if (stats) {
        pendingRecords.value = {
          entradas: stats.entradas_pendientes,
          salidas: stats.salidas_pendientes,
          total: stats.total_pendientes
        };
      }
    } catch (error) {
      console.error('❌ Error actualizando contador pendientes:', error);
    }
  }

  /**
   * Intenta sincronizar registros pendientes
   */
  async function attemptSync() {
    if (isSyncing.value || !isOnline.value) {
      return;
    }

    // Verificar si hay registros pendientes
    await updatePendingCount();
    if (!hasPendingRecords.value) {
      return;
    }

    isSyncing.value = true;
    lastSyncAttempt.value = new Date();
    syncMessage.value = 'Sincronizando registros...';
    
    try {
      await offlineService.sincronizarRegistros(
        asistenciasService,
        // onProgress
        (progress) => {
          syncProgress.value = progress;
          syncMessage.value = `Sincronizando ${progress.procesados}/${progress.total} registros...`;
        },
        // onSuccess
        (count) => {
          syncMessage.value = count > 0 ? `${count} registro(s) sincronizado(s) correctamente` : 'No hay registros por sincronizar';
          setTimeout(() => {
            syncMessage.value = '';
          }, 3000);
          updatePendingCount();
        },
        // onError
        (errors, successful) => {
          console.error('❌ Errores en sincronización:', errors);
          syncMessage.value = successful > 0 ? 
            `${successful} sincronizados, ${errors.length} con errores` : 
            'Error al sincronizar registros';
          
          // Programar reintento en 30 segundos
          scheduleSyncRetry();
          updatePendingCount();
        }
      );
    } catch (error) {
      console.error('❌ Error durante sincronización:', error);
      syncMessage.value = 'Error al sincronizar registros';
      scheduleSyncRetry();
    } finally {
      isSyncing.value = false;
    }
  }

  /**
   * Programa un reintento de sincronización
   */
  function scheduleSyncRetry() {
    if (syncRetryTimeout) {
      clearTimeout(syncRetryTimeout);
    }
    
    syncRetryTimeout = setTimeout(async () => {
      if (isOnline.value) {
        console.log('🔄 Reintentando sincronización...');
        await attemptSync();
      }
    }, 30000); // Reintentar en 30 segundos
  }

  /**
   * Guarda un registro de entrada offline
   */
  async function saveEntradaOffline(datos, usuarioId) {
    try {
      await offlineService.guardarEntradaOffline(datos, usuarioId);
      await updatePendingCount();
      return {
        success: true,
        message: 'Sin conexión. El registro se enviará automáticamente cuando recuperes internet.'
      };
    } catch (error) {
      console.error('❌ Error guardando entrada offline:', error);
      return {
        success: false,
        message: 'Error al guardar el registro offline.'
      };
    }
  }

  /**
   * Guarda un registro de salida offline
   */
  async function saveSalidaOffline(datos, usuarioId) {
    try {
      await offlineService.guardarSalidaOffline(datos, usuarioId);
      await updatePendingCount();
      return {
        success: true,
        message: 'Sin conexión. El registro se enviará automáticamente cuando recuperes internet.'
      };
    } catch (error) {
      console.error('❌ Error guardando salida offline:', error);
      return {
        success: false,
        message: 'Error al guardar el registro offline.'
      };
    }
  }

  /**
   * Fuerza una sincronización manual
   */
  async function forceSyncronization() {
    if (isSyncing.value) return;
    
    console.log('🔄 Forzando sincronización manual...');
    await checkConnection();
    if (isOnline.value) {
      await attemptSync();
    } else {
      syncMessage.value = 'Sin conexión a internet';
      setTimeout(() => {
        syncMessage.value = '';
      }, 3000);
    }
  }

  /**
   * Limpia todos los registros offline
   */
  async function clearOfflineRecords() {
    try {
      await offlineService.limpiarRegistrosOffline();
      await updatePendingCount();
      syncMessage.value = 'Registros offline eliminados';
      setTimeout(() => {
        syncMessage.value = '';
      }, 2000);
    } catch (error) {
      console.error('❌ Error limpiando registros:', error);
    }
  }

  // Lifecycle hooks
  onMounted(async () => {
    console.log('🔧 Inicializando sistema offline...');
    
    // Inicializar base de datos offline
    try {
      await offlineService.initDB();
    } catch (error) {
      console.error('❌ Error inicializando BD offline:', error);
    }

    // Verificar conexión inicial
    await checkConnection();
    await updatePendingCount();

    // Configurar listeners de eventos de conectividad
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Listener para eventos del Service Worker
    window.addEventListener('sw-sync-trigger', handleServiceWorkerSync);

    // Verificar conexión periódicamente (cada 30 segundos)
    connectionCheckInterval = setInterval(checkConnection, 30000);

    // Si ya hay registros pendientes y hay conexión, intentar sincronizar
    if (isOnline.value && hasPendingRecords.value) {
      // Esperar un poco antes de sincronizar para que la app se cargue
      syncTimeout = setTimeout(attemptSync, 2000);
    }
  });

  onUnmounted(() => {
    // Limpiar listeners y timeouts
    window.removeEventListener('online', handleOnline);
    window.removeEventListener('offline', handleOffline);
    window.removeEventListener('sw-sync-trigger', handleServiceWorkerSync);
    
    if (connectionCheckInterval) {
      clearInterval(connectionCheckInterval);
    }
    
    if (syncTimeout) {
      clearTimeout(syncTimeout);
    }
    
    if (syncRetryTimeout) {
      clearTimeout(syncRetryTimeout);
    }
  });

  // Event handlers
  async function handleOnline() {
    console.log('🌐 Evento: Conexión establecida');
    isOnline.value = true;
    await attemptSync();
  }

  function handleOffline() {
    console.log('📵 Evento: Conexión perdida');
    isOnline.value = false;
    if (isSyncing.value) {
      syncMessage.value = 'Sincronización interrumpida - sin conexión';
    }
  }

  // Handler para eventos del Service Worker
  async function handleServiceWorkerSync(event) {
    console.log('🔄 Service Worker solicitó sincronización:', event.detail);
    await checkConnection();
    if (isOnline.value) {
      await attemptSync();
    }
  }

  // API pública del composable
  return {
    // Estado reactivo
    isOnline,
    isCheckingConnection,
    isSyncing,
    syncProgress,
    pendingRecords,
    syncMessage,
    
    // Estado computado
    hasPendingRecords,
    shouldShowSyncStatus,
    
    // Métodos
    checkConnection,
    updatePendingCount,
    attemptSync,
    saveEntradaOffline,
    saveSalidaOffline,
    forceSyncronization,
    clearOfflineRecords,
    
    // Información adicional
    lastSyncAttempt
  };
}
