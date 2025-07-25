/**
 * Composable para manejar funcionalidad offline
 * Proporciona un estado reactivo y funciones para trabajar con datos offline
 */

import { ref, reactive, computed, onMounted, onUnmounted, watch, readonly } from 'vue';
import offlineService from '../services/offlineService.js';
import { connectivityMonitor } from '../utils/network.js';
import { apiService } from '../services/apiService.js';

export function useOffline() {
  // Estado reactivo
  const connectionStatus = ref('checking');
  const isOnline = computed(() => connectionStatus.value === 'online');
  const isOffline = computed(() => connectionStatus.value === 'offline');
  const isChecking = computed(() => connectionStatus.value === 'checking');
  
  const pendingStats = reactive({
    pendingRecords: 0,
    pendingAttendances: 0,
    totalPending: 0,
    lastSync: null
  });

  const syncStatus = reactive({
    inProgress: false,
    lastAttempt: null,
    lastSuccess: null,
    lastError: null
  });

  // Referencias para cleanup
  let unsubscribeConnectivity = null;
  let unsubscribeOffline = null;
  let statsInterval = null;

  // Mensajes de notificación
  const notifications = ref([]);
  let notificationIdCounter = 0;

  // Configuración y funciones de inicialización
  const init = () => {
    // Configurar listener de conectividad
    unsubscribeConnectivity = connectivityMonitor.addListener((status) => {
      connectionStatus.value = status;
    });

    // Configurar listener de servicio offline
    unsubscribeOffline = offlineService.addListener((event) => {
      handleOfflineEvent(event);
    });

    // Cargar estadísticas iniciales
    updateStats();
    
    // Actualizar estadísticas periódicamente
    statsInterval = setInterval(updateStats, 15000);
  };

  // Manejo de eventos del servicio offline
  const handleOfflineEvent = ({ event, data }) => {
    switch (event) {
      case 'recordSaved':
        addNotification({
          type: 'offline',
          title: 'Registro guardado offline',
          message: data.message,
          icon: 'save'
        });
        updateStats();
        break;

      case 'attendanceSaved':
        addNotification({
          type: 'offline',
          title: 'Asistencia guardada offline', 
          message: data.message,
          icon: 'clock'
        });
        updateStats();
        break;

      case 'itemSynced':
        addNotification({
          type: 'success',
          title: 'Sincronizado',
          message: data.message,
          icon: 'check'
        });
        updateStats();
        break;

      case 'syncCompleted':
        addNotification({
          type: 'success',
          title: 'Sincronización completada',
          message: `${data.syncedCount} elemento${data.syncedCount > 1 ? 's' : ''} enviado${data.syncedCount > 1 ? 's' : ''}`,
          icon: 'sync'
        });
        syncStatus.lastSuccess = Date.now();
        updateStats();
        break;

      case 'syncError':
        addNotification({
          type: 'error',
          title: 'Error de sincronización',
          message: `Error al enviar ${data.type === 'record' ? 'registro' : 'asistencia'}`,
          icon: 'error',
          persistent: true
        });
        syncStatus.lastError = Date.now();
        break;

      case 'connection':
        if (data.online) {
          addNotification({
            type: 'success',
            title: 'Conexión restaurada',
            message: 'Iniciando sincronización automática...',
            icon: 'wifi'
          });
        }
        break;
    }
  };

  // Actualizar estadísticas
  const updateStats = async () => {
    try {
      const stats = await apiService.getOfflineStats();
      Object.assign(pendingStats, stats);
    } catch (error) {
      console.error('❌ Error actualizando estadísticas offline:', error);
    }
  };

  // Funciones de notificación
  const addNotification = (notificationData) => {
    const notification = {
      id: ++notificationIdCounter,
      timestamp: Date.now(),
      ...notificationData
    };

    notifications.value.push(notification);

    // Auto-remover notificaciones no persistentes después de 5 segundos
    if (!notification.persistent) {
      setTimeout(() => {
        removeNotification(notification.id);
      }, 5000);
    }

    // Limitar a 5 notificaciones máximo
    if (notifications.value.length > 5) {
      notifications.value.shift();
    }

    return notification.id;
  };

  const removeNotification = (id) => {
    const index = notifications.value.findIndex(n => n.id === id);
    if (index !== -1) {
      notifications.value.splice(index, 1);
    }
  };

  const clearAllNotifications = () => {
    notifications.value = [];
  };

  // Funciones de sincronización
  const forceSync = async () => {
    if (syncStatus.inProgress || !isOnline.value) {
      throw new Error('No se puede sincronizar en este momento');
    }

    syncStatus.inProgress = true;
    syncStatus.lastAttempt = Date.now();

    try {
      await apiService.forceSyncPending();
      syncStatus.lastSuccess = Date.now();
      addNotification({
        type: 'success',
        title: 'Sincronización manual exitosa',
        message: 'Todos los elementos han sido enviados',
        icon: 'sync'
      });
    } catch (error) {
      syncStatus.lastError = Date.now();
      addNotification({
        type: 'error',
        title: 'Error en sincronización',
        message: error.message || 'No se pudo completar la sincronización',
        icon: 'error',
        persistent: true
      });
      throw error;
    } finally {
      syncStatus.inProgress = false;
      await updateStats();
    }
  };

  // Funciones de almacenamiento offline
  const saveRecordOffline = async (recordData) => {
    try {
      const offlineId = await offlineService.saveRecordOffline(recordData);
      return { offlineId, success: true };
    } catch (error) {
      console.error('❌ Error guardando registro offline:', error);
      throw error;
    }
  };

  const saveAttendanceOffline = async (attendanceData) => {
    try {
      const offlineId = await offlineService.saveAttendanceOffline(attendanceData);
      return { offlineId, success: true };
    } catch (error) {
      console.error('❌ Error guardando asistencia offline:', error);
      throw error;
    }
  };

  // Obtener elementos pendientes
  const getPendingItems = async () => {
    try {
      return await apiService.getPendingOfflineItems();
    } catch (error) {
      console.error('❌ Error obteniendo elementos pendientes:', error);
      return { records: [], attendances: [], total: 0 };
    }
  };

  // Funciones utilitarias
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('es-ES', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const formatRelativeTime = (timestamp) => {
    const now = Date.now();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'Hace un momento';
    if (minutes < 60) return `Hace ${minutes} minuto${minutes > 1 ? 's' : ''}`;
    if (hours < 24) return `Hace ${hours} hora${hours > 1 ? 's' : ''}`;
    return `Hace ${days} día${days > 1 ? 's' : ''}`;
  };

  // Función de limpieza
  const cleanup = () => {
    if (unsubscribeConnectivity) unsubscribeConnectivity();
    if (unsubscribeOffline) unsubscribeOffline();
    if (statsInterval) clearInterval(statsInterval);
  };

  // Computeds adicionales
  const hasOfflineData = computed(() => pendingStats.totalPending > 0);
  const canSync = computed(() => isOnline.value && hasOfflineData.value && !syncStatus.inProgress);
  
  const connectionIcon = computed(() => {
    switch (connectionStatus.value) {
      case 'online': return 'wifi';
      case 'offline': return 'wifi-off';
      case 'checking': return 'refresh';
      default: return 'help';
    }
  });

  const connectionColor = computed(() => {
    switch (connectionStatus.value) {
      case 'online': return 'green';
      case 'offline': return 'red';
      case 'checking': return 'yellow';
      default: return 'gray';
    }
  });

  // Watch para auto-sincronización cuando se recupera la conexión
  watch(isOnline, (newValue, oldValue) => {
    if (newValue && !oldValue && hasOfflineData.value) {
      console.log('🔄 Conexión recuperada - iniciando auto-sincronización');
      setTimeout(() => {
        if (canSync.value) {
          forceSync().catch(error => {
            console.error('❌ Error en auto-sincronización:', error);
          });
        }
      }, 2000); // Esperar 2 segundos para que la conexión se estabilice
    }
  });

  return {
    // Estado
    connectionStatus: readonly(connectionStatus),
    isOnline,
    isOffline,
    isChecking,
    pendingStats: readonly(pendingStats),
    syncStatus: readonly(syncStatus),
    notifications: readonly(notifications),
    hasOfflineData,
    canSync,
    connectionIcon,
    connectionColor,

    // Funciones principales
    init,
    cleanup,
    forceSync,
    saveRecordOffline,
    saveAttendanceOffline,
    getPendingItems,
    updateStats,

    // Funciones de notificación
    addNotification,
    removeNotification,
    clearAllNotifications,

    // Utilidades
    formatTime,
    formatRelativeTime
  };
}

// Función helper para crear una instancia global si se necesita
let globalOfflineInstance = null;

export function useGlobalOffline() {
  if (!globalOfflineInstance) {
    globalOfflineInstance = useOffline();
    globalOfflineInstance.init();
  }
  return globalOfflineInstance;
}

export default useOffline;
