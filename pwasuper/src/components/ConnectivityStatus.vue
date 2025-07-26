<template>
  <!-- Modal/Banner de estado de conectividad -->
  <teleport to="body">
    <!-- Overlay para modal cuando hay pendientes -->
    <div 
      v-if="showModal && pendientes.total > 0" 
      class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
      @click="closeModal"
    >
      <div 
        class="bg-white rounded-lg shadow-xl max-w-md w-full p-6"
        @click.stop
      >
        <div class="text-center">
          <!-- Icono según estado -->
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full mb-4"
               :class="getModalIconClasses()">
            <!-- Offline -->
            <svg v-if="!isOnline" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636a9 9 0 010 12.728m0 0l-2.829-2.829m2.829 2.829L21 21M15.536 8.464a5 5 0 010 7.072m0 0l-2.829-2.829m2.829 2.829L18 18M8.464 15.536a5 5 0 010-7.072m0 0l2.829 2.829m-2.829-2.829L6 6M5.636 18.364a9 9 0 010-12.728m0 0l2.829 2.829m-2.829-2.829L3 3" />
            </svg>
            <!-- Syncing -->
            <div v-else-if="isSyncing" class="animate-spin rounded-full h-6 w-6 border-b-2 border-current"></div>
            <!-- Online -->
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>

          <!-- Título -->
          <h3 class="text-lg font-medium text-gray-900 mb-2">
            {{ getModalTitle() }}
          </h3>

          <!-- Mensaje -->
          <p class="text-sm text-gray-500 mb-4">
            {{ getModalMessage() }}
          </p>

          <!-- Progreso de sincronización -->
          <div v-if="isSyncing && syncProgress" class="mb-4">
            <div class="bg-gray-200 rounded-full h-2">
              <div 
                class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                :style="{ width: `${(syncProgress.procesados / syncProgress.total) * 100}%` }"
              ></div>
            </div>
            <p class="text-xs text-gray-500 mt-1">
              {{ syncProgress.procesados }} / {{ syncProgress.total }} 
              ({{ syncProgress.exitosos }} exitosos, {{ syncProgress.fallidos }} fallidos)
            </p>
          </div>

          <!-- Botones -->
          <div class="flex gap-3 justify-center">
            <button
              @click="closeModal"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
            >
              Cerrar
            </button>
            
            <button
              v-if="isOnline && !isSyncing && pendientes.total > 0"
              @click="sincronizarManual"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors"
            >
              Sincronizar ahora
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Banner fijo debajo del header -->
    <div 
      v-if="showBanner" 
      class="fixed left-0 right-0 z-30 shadow-sm transition-all duration-300"
      :class="getBannerClasses()"
      :style="{ top: '64px' }"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between py-3">
          <div class="flex items-center">
            <!-- Icono de estado -->
            <div class="flex-shrink-0 mr-3">
              <!-- Offline -->
              <svg v-if="!isOnline" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636a9 9 0 010 12.728m0 0l-2.829-2.829m2.829 2.829L21 21M15.536 8.464a5 5 0 010 7.072m0 0l-2.829-2.829m2.829 2.829L18 18M8.464 15.536a5 5 0 010-7.072m0 0l2.829 2.829m-2.829-2.829L6 6M5.636 18.364a9 9 0 010-12.728m0 0l2.829 2.829m-2.829-2.829L3 3" />
              </svg>
              <!-- Syncing -->
              <div v-else-if="isSyncing" class="animate-spin rounded-full h-5 w-5 border-b-2 border-current"></div>
              <!-- Online -->
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0" />
              </svg>
            </div>

            <!-- Texto de estado -->
            <div>
              <p class="text-sm font-medium">
                {{ getBannerTitle() }}
              </p>
              <p v-if="getBannerSubtitle()" class="text-xs opacity-75">
                {{ getBannerSubtitle() }}
              </p>
            </div>
          </div>

          <!-- Botón de acción -->
          <div class="flex items-center">
            <button
              v-if="pendientes.total > 0"
              @click="openModal"
              class="text-xs px-3 py-1 rounded-full bg-white bg-opacity-20 hover:bg-opacity-30 transition-colors"
            >
              Ver detalles
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Notificación flotante simple para casos mínimos -->
    <div 
      v-if="!showBanner && !isOnline && !bannerDismissed" 
      class="fixed bottom-4 right-4 z-50 bg-red-500 text-white p-3 rounded-lg shadow-lg flex items-center max-w-sm"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <span class="text-sm">
        Sin conexión. 
        <span v-if="pendientes.total > 0">{{ pendientes.total }} registro{{ pendientes.total > 1 ? 's' : '' }} pendiente{{ pendientes.total > 1 ? 's' : '' }}.</span>
      </span>
    </div>
  </teleport>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import syncService from '../services/syncService.js';
import { checkInternetConnection } from '../utils/network.js';

// Estado reactivo
const isOnline = ref(true);
const isSyncing = ref(false);
const pendientes = ref({ registros: 0, asistencias: 0, total: 0 });
const syncProgress = ref(null);
const showModal = ref(false);
const bannerDismissed = ref(false);
const lastSyncResult = ref(null);
const lastConnectionCheck = ref(new Date());

// Computed para mostrar el tiempo transcurrido desde la última verificación
const timeAgoText = computed(() => {
  const timeAgo = Math.floor((new Date() - lastConnectionCheck.value) / 1000);
  if (timeAgo < 2) return 'ahora';
  if (timeAgo < 60) return `${timeAgo}s`;
  if (timeAgo < 3600) return `${Math.floor(timeAgo / 60)}m`;
  return `${Math.floor(timeAgo / 3600)}h`;
});

// Control de visualización - Siempre mostrar banner con estado de red
const showBanner = computed(() => {
  // Siempre mostrar el banner para ver el estado de conectividad en tiempo real
  return true;
});

// Métodos para obtener clases CSS
const getBannerClasses = () => {
  if (!isOnline.value) {
    return 'bg-red-500 text-white';
  } else if (isSyncing.value) {
    return 'bg-blue-500 text-white';
  } else if (pendientes.value.total > 0) {
    return 'bg-yellow-500 text-white';
  } else {
    return 'bg-green-500 text-white';
  }
};

const getModalIconClasses = () => {
  if (!isOnline.value) {
    return 'bg-red-100 text-red-600';
  } else if (isSyncing.value) {
    return 'bg-blue-100 text-blue-600';
  } else {
    return 'bg-green-100 text-green-600';
  }
};

// Métodos para obtener textos
const getBannerTitle = () => {
  if (!isOnline.value) {
    return 'Sin conexión';
  } else if (isSyncing.value) {
    return 'Sincronizando...';
  } else if (pendientes.value.total > 0) {
    return `${pendientes.value.total} registro${pendientes.value.total > 1 ? 's' : ''} pendiente${pendientes.value.total > 1 ? 's' : ''}`;
  } else {
    return 'Conectado';
  }
};

const getBannerSubtitle = () => {
  const checkStatus = `Verificado ${timeAgoText.value}`;
  
  if (!isOnline.value && pendientes.value.total > 0) {
    return `${pendientes.value.total} registro${pendientes.value.total > 1 ? 's' : ''} se enviarán al recuperar conexión • ${checkStatus}`;
  } else if (isSyncing.value && syncProgress.value) {
    return `${syncProgress.value.procesados}/${syncProgress.value.total} procesados`;
  } else if (pendientes.value.total > 0) {
    return `Toca para sincronizar ahora • ${checkStatus}`;
  } else if (isOnline.value) {
    return `Estado: Conectado • ${checkStatus}`;
  }
  return checkStatus;
};

const getModalTitle = () => {
  if (!isOnline.value) {
    return 'Sin conexión a internet';
  } else if (isSyncing.value) {
    return 'Sincronizando registros';
  } else if (lastSyncResult.value) {
    return 'Sincronización completada';
  } else {
    return 'Registros pendientes';
  }
};

const getModalMessage = () => {
  if (!isOnline.value) {
    return `Tienes ${pendientes.value.total} registro${pendientes.value.total > 1 ? 's' : ''} guardado${pendientes.value.total > 1 ? 's' : ''} que se enviarán automáticamente cuando recuperes la conexión.`;
  } else if (isSyncing.value) {
    return 'Enviando tus registros guardados al servidor...';
  } else if (lastSyncResult.value) {
    const { exitosos, fallidos } = lastSyncResult.value;
    return `Se enviaron ${exitosos} registro${exitosos > 1 ? 's' : ''} correctamente${fallidos > 0 ? ` y ${fallidos} fallaron` : ''}.`;
  } else {
    return `Tienes ${pendientes.value.total} registro${pendientes.value.total > 1 ? 's' : ''} pendiente${pendientes.value.total > 1 ? 's' : ''} de envío.`;
  }
};

// Métodos de control
const openModal = () => {
  showModal.value = true;
  bannerDismissed.value = true;
};

const closeModal = () => {
  showModal.value = false;
  lastSyncResult.value = null;
  syncProgress.value = null;
};

const dismissBanner = () => {
  bannerDismissed.value = true;
  
  // Reaparecer el banner más rápido si todo está OK (10s) o más lento si hay problemas (30s)
  const timeout = (isOnline.value && pendientes.value.total === 0 && !isSyncing.value) ? 10000 : 30000;
  
  setTimeout(() => {
    bannerDismissed.value = false;
  }, timeout);
};

const sincronizarManual = async () => {
  try {
    await syncService.sincronizarManual();
  } catch (error) {
    console.error('Error en sincronización manual:', error);
  }
};

// Listener para eventos de sincronización
const handleSyncEvent = (event, online, data) => {
  isOnline.value = online;
  
  switch (event) {
    case 'online':
      console.log('🌐 Conectado');
      bannerDismissed.value = false; // Mostrar banner al conectarse
      break;
      
    case 'offline':
      console.log('📴 Desconectado');
      bannerDismissed.value = false; // Mostrar banner al desconectarse
      break;
      
    case 'syncing':
      console.log('🔄 Iniciando sincronización');
      isSyncing.value = true;
      syncProgress.value = null;
      bannerDismissed.value = false;
      break;
      
    case 'sync_progress':
      console.log('📊 Progreso de sincronización:', data);
      syncProgress.value = data;
      break;
      
    case 'sync_complete':
      console.log('✅ Sincronización completada:', data);
      isSyncing.value = false;
      lastSyncResult.value = data;
      syncProgress.value = null;
      
      // Si todos los registros se enviaron exitosamente, ocultar banner después de 3 segundos
      if (data.exitosos > 0 && data.fallidos === 0) {
        setTimeout(() => {
          bannerDismissed.value = true;
          showModal.value = false;
        }, 3000);
      }
      break;
      
    case 'sync_error':
      console.log('❌ Error en sincronización:', data);
      isSyncing.value = false;
      syncProgress.value = null;
      break;
  }
};

// Actualizar contador de pendientes
const actualizarPendientes = async () => {
  try {
    pendientes.value = await syncService.obtenerPendientes();
  } catch (error) {
    console.error('Error obteniendo pendientes:', error);
  }
};

// Variables para intervalos
let pendientesInterval = null;
let conectividadInterval = null;
let uiUpdateInterval = null;

// Función para verificar conectividad más frecuentemente
const verificarConectividad = async () => {
  try {
    const estadoActual = await syncService.getConnectionStatus();
    const nuevaConexion = await checkInternetConnection();
    
    // Actualizar timestamp de última verificación
    lastConnectionCheck.value = new Date();
    
    // Solo actualizar si hay cambio para evitar renders innecesarios
    if (isOnline.value !== nuevaConexion) {
      isOnline.value = nuevaConexion;
      console.log(`🔄 Estado de conectividad actualizado: ${nuevaConexion ? 'Online' : 'Offline'}`);
    }
  } catch (error) {
    console.error('Error verificando conectividad:', error);
  }
};

// Lifecycle hooks
onMounted(async () => {
  // Configurar listener de sincronización
  syncService.addListener(handleSyncEvent);
  
  // Obtener estado inicial
  const status = syncService.getConnectionStatus();
  isOnline.value = status.isOnline;
  isSyncing.value = status.isSyncing;
  
  // Actualizar pendientes inicialmente y cada 5 segundos
  await actualizarPendientes();
  pendientesInterval = setInterval(actualizarPendientes, 5000);
  
  // Verificar conectividad cada segundo
  conectividadInterval = setInterval(verificarConectividad, 1000);
  
  // Actualizar UI cada segundo para mostrar tiempo transcurrido
  uiUpdateInterval = setInterval(() => {
    // Forzar reactividad del computed timeAgoText
    lastConnectionCheck.value = lastConnectionCheck.value;
  }, 1000);
  
  // Limpiar intervalos al desmontar
  onUnmounted(() => {
    if (pendientesInterval) clearInterval(pendientesInterval);
    if (conectividadInterval) clearInterval(conectividadInterval);
    if (uiUpdateInterval) clearInterval(uiUpdateInterval);
    syncService.removeListener(handleSyncEvent);
  });
});
</script>
