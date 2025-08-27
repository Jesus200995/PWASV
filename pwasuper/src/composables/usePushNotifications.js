/**
 * Composable para manejar notificaciones push
 * Proporciona funcionalidad reactiva para suscripciones push
 */

import { ref, computed, onMounted, readonly } from 'vue';
import pushNotificationService from '../services/pushNotificationService.js';

export function usePushNotifications() {
  // Estados reactivos
  const isSupported = ref(false);
  const permission = ref('default');
  const isSubscribed = ref(false);
  const isLoading = ref(false);
  const error = ref('');
  const subscription = ref(null);

  // Computed properties
  const canSubscribe = computed(() => {
    return isSupported.value && permission.value !== 'denied';
  });

  const needsPermission = computed(() => {
    return permission.value === 'default';
  });

  const isBlocked = computed(() => {
    return permission.value === 'denied';
  });

  const statusMessage = computed(() => {
    if (!isSupported.value) {
      return 'Tu navegador no soporta notificaciones push';
    }
    if (permission.value === 'denied') {
      return 'Notificaciones bloqueadas. Habilítalas en configuración del navegador';
    }
    if (permission.value === 'default') {
      return 'Permitir notificaciones para recibir alertas instantáneas';
    }
    if (isSubscribed.value) {
      return 'Notificaciones push activadas';
    }
    return 'Notificaciones disponibles - activar para recibir alertas';
  });

  const statusIcon = computed(() => {
    if (!isSupported.value) return '❌';
    if (permission.value === 'denied') return '🔕';
    if (permission.value === 'default') return '🔔';
    if (isSubscribed.value) return '✅';
    return '⚡';
  });

  /**
   * Inicializar el servicio de notificaciones push
   */
  const init = async () => {
    try {
      isLoading.value = true;
      error.value = '';

      // Inicializar el servicio
      const initialized = await pushNotificationService.init();
      if (!initialized) {
        throw new Error('No se pudo inicializar el servicio de notificaciones');
      }

      // Configurar listener para mensajes del SW
      pushNotificationService.setupMessageListener();

      // Obtener estado actual
      await updateStatus();

      console.log('✅ Push notifications initialized');
      
    } catch (err) {
      console.error('❌ Error inicializando push notifications:', err);
      error.value = err.message;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Actualizar estado de suscripción
   */
  const updateStatus = async () => {
    try {
      const status = await pushNotificationService.getSubscriptionStatus();
      
      isSupported.value = status.supported;
      permission.value = status.permission;
      isSubscribed.value = status.subscribed;
      subscription.value = status.subscription;

    } catch (err) {
      console.error('❌ Error obteniendo estado:', err);
      error.value = err.message;
    }
  };

  /**
   * Suscribirse a notificaciones push
   */
  const subscribe = async (usuarioId) => {
    if (!usuarioId) {
      throw new Error('ID de usuario requerido para suscribirse');
    }

    try {
      isLoading.value = true;
      error.value = '';

      console.log(`🔔 Suscribiendo usuario ${usuarioId} a push notifications`);
      
      const newSubscription = await pushNotificationService.subscribe(usuarioId);
      
      if (newSubscription) {
        await updateStatus();
        console.log('✅ Suscripción exitosa');
        return true;
      }
      
      return false;

    } catch (err) {
      console.error('❌ Error en suscripción:', err);
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Desuscribirse de notificaciones push
   */
  const unsubscribe = async (usuarioId) => {
    try {
      isLoading.value = true;
      error.value = '';

      console.log(`🔕 Desuscribiendo usuario ${usuarioId} de push notifications`);
      
      const success = await pushNotificationService.unsubscribe(usuarioId);
      
      if (success) {
        await updateStatus();
        console.log('✅ Desuscripción exitosa');
        return true;
      }
      
      return false;

    } catch (err) {
      console.error('❌ Error en desuscripción:', err);
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Toggle suscripción (suscribir/desuscribir)
   */
  const toggleSubscription = async (usuarioId) => {
    if (isSubscribed.value) {
      return await unsubscribe(usuarioId);
    } else {
      return await subscribe(usuarioId);
    }
  };

  /**
   * Solicitar permisos explícitamente
   */
  const requestPermission = async () => {
    try {
      isLoading.value = true;
      error.value = '';

      const granted = await pushNotificationService.requestPermission();
      await updateStatus();

      return granted;

    } catch (err) {
      console.error('❌ Error solicitando permisos:', err);
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Mostrar notificación de prueba
   */
  const showTestNotification = async () => {
    try {
      await pushNotificationService.showTestNotification();
    } catch (err) {
      console.error('❌ Error mostrando notificación de prueba:', err);
      error.value = err.message;
    }
  };

  /**
   * Obtener información de debugging
   */
  const getDebugInfo = () => {
    return {
      ...pushNotificationService.getDeviceInfo(),
      vueState: {
        isSupported: isSupported.value,
        permission: permission.value,
        isSubscribed: isSubscribed.value,
        error: error.value
      }
    };
  };

  /**
   * Limpiar error
   */
  const clearError = () => {
    error.value = '';
  };

  // Auto-inicializar cuando se monte
  onMounted(() => {
    init();
  });

  // Retornar API reactiva
  return {
    // Estados
    isSupported: readonly(isSupported),
    permission: readonly(permission),
    isSubscribed: readonly(isSubscribed),
    isLoading: readonly(isLoading),
    error: readonly(error),
    subscription: readonly(subscription),

    // Computed
    canSubscribe: readonly(canSubscribe),
    needsPermission: readonly(needsPermission),
    isBlocked: readonly(isBlocked),
    statusMessage: readonly(statusMessage),
    statusIcon: readonly(statusIcon),

    // Métodos
    init,
    subscribe,
    unsubscribe,
    toggleSubscription,
    requestPermission,
    updateStatus,
    showTestNotification,
    getDebugInfo,
    clearError
  };
}

export default usePushNotifications;
