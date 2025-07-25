<template>
  <!-- Indicador de estado de conectividad -->
  <div class="fixed bottom-4 right-4 z-50 max-w-sm">
    <!-- Estado offline -->
    <transition name="slide-up">
      <div v-if="connectionStatus === 'offline'" 
           class="bg-red-500 text-white p-3 rounded-lg shadow-lg flex items-center mb-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-12.728 12.728m0-12.728l12.728 12.728" />
        </svg>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium">Sin conexión</p>
          <p class="text-xs opacity-90">Los datos se guardarán localmente</p>
        </div>
      </div>
    </transition>

    <!-- Estado verificando -->
    <transition name="slide-up">
      <div v-if="connectionStatus === 'checking'" 
           class="bg-yellow-500 text-white p-3 rounded-lg shadow-lg flex items-center mb-2">
        <div class="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white mr-2"></div>
        <span class="text-sm">Verificando conexión...</span>
      </div>
    </transition>

    <!-- Mensajes de sincronización -->
    <transition-group name="slide-up" tag="div" class="space-y-2">
      <div v-for="message in messages" 
           :key="message.id"
           class="p-3 rounded-lg shadow-lg flex items-start"
           :class="getMessageClass(message.type)">
        
        <!-- Ícono según el tipo de mensaje -->
        <div class="flex-shrink-0 mr-2 mt-0.5">
          <!-- Guardado offline -->
          <svg v-if="message.type === 'offline'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          
          <!-- Sincronizando -->
          <div v-else-if="message.type === 'syncing'" class="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-current"></div>
          
          <!-- Éxito -->
          <svg v-else-if="message.type === 'success'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          
          <!-- Error -->
          <svg v-else-if="message.type === 'error'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          
          <!-- Info -->
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>

        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium">{{ message.title }}</p>
          <p class="text-xs opacity-90">{{ message.text }}</p>
          
          <!-- Detalles adicionales para elementos pendientes -->
          <div v-if="message.pendingCount" class="mt-1">
            <span class="text-xs bg-white bg-opacity-20 px-2 py-1 rounded">
              {{ message.pendingCount }} pendiente{{ message.pendingCount > 1 ? 's' : '' }}
            </span>
          </div>
        </div>

        <!-- Botón de cerrar para ciertos mensajes -->
        <button v-if="message.closable" 
                @click="dismissMessage(message.id)"
                class="flex-shrink-0 ml-2 text-white hover:text-gray-200">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </transition-group>

    <!-- Panel de estadísticas offline (expandible) -->
    <transition name="slide-up">
      <div v-if="showStats && (pendingStats.totalPending > 0 || connectionStatus === 'offline')" 
           class="bg-gray-800 text-white p-3 rounded-lg shadow-lg mt-2">
        <div class="flex items-center justify-between mb-2">
          <h3 class="text-sm font-medium">Estado Offline</h3>
          <button @click="showStats = false" class="text-gray-400 hover:text-white">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="space-y-1 text-xs">
          <div class="flex justify-between">
            <span>Registros pendientes:</span>
            <span class="font-mono">{{ pendingStats.pendingRecords }}</span>
          </div>
          <div class="flex justify-between">
            <span>Asistencias pendientes:</span>
            <span class="font-mono">{{ pendingStats.pendingAttendances }}</span>
          </div>
          <div v-if="pendingStats.lastSync" class="flex justify-between">
            <span>Última sincronización:</span>
            <span class="font-mono">{{ formatTime(pendingStats.lastSync) }}</span>
          </div>
        </div>

        <!-- Botón de sincronización manual -->
        <button v-if="connectionStatus === 'online' && pendingStats.totalPending > 0"
                @click="forceSyncNow"
                :disabled="syncInProgress"
                class="w-full mt-2 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-500 px-3 py-1 rounded text-sm font-medium">
          <span v-if="syncInProgress">Sincronizando...</span>
          <span v-else>Sincronizar Ahora</span>
        </button>
      </div>
    </transition>

    <!-- Botón flotante para mostrar estadísticas -->
    <button v-if="!showStats && (pendingStats.totalPending > 0 || connectionStatus === 'offline')"
            @click="showStats = true"
            class="fixed bottom-20 right-4 bg-gray-800 text-white p-2 rounded-full shadow-lg hover:bg-gray-700 transition-colors">
      <span class="text-xs font-bold">{{ pendingStats.totalPending }}</span>
    </button>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue';
import { connectivityMonitor } from '../utils/network.js';
import { apiService } from '../services/apiService.js';
import offlineService from '../services/offlineService.js';

// Estado reactivo
const connectionStatus = ref('checking');
const messages = ref([]);
const showStats = ref(false);
const syncInProgress = ref(false);
const pendingStats = reactive({
  pendingRecords: 0,
  pendingAttendances: 0,
  totalPending: 0,
  lastSync: null
});

// Variables para cleanup
let messageIdCounter = 0;
let unsubscribeConnectivity = null;
let unsubscribeOffline = null;
let statsInterval = null;

// Montaje del componente
onMounted(async () => {
  // Configurar listener de conectividad
  unsubscribeConnectivity = connectivityMonitor.addListener((status) => {
    const oldStatus = connectionStatus.value;
    connectionStatus.value = status;
    
    // Mostrar mensaje cuando se restaura la conexión
    if (oldStatus === 'offline' && status === 'online') {
      addMessage({
        type: 'success',
        title: 'Conexión restaurada',
        text: 'Iniciando sincronización automática...',
        duration: 3000
      });
    }
  });

  // Configurar listener de servicio offline
  unsubscribeOffline = offlineService.addListener((event) => {
    handleOfflineEvent(event);
  });

  // Cargar estadísticas iniciales
  await updateStats();
  
  // Actualizar estadísticas periódicamente
  statsInterval = setInterval(updateStats, 10000);
});

// Desmontaje del componente
onUnmounted(() => {
  if (unsubscribeConnectivity) unsubscribeConnectivity();
  if (unsubscribeOffline) unsubscribeOffline();
  if (statsInterval) clearInterval(statsInterval);
});

// Manejo de eventos del servicio offline
function handleOfflineEvent({ event, data }) {
  switch (event) {
    case 'recordSaved':
    case 'attendanceSaved':
      addMessage({
        type: 'offline',
        title: 'Guardado localmente',
        text: data.message,
        duration: 5000,
        pendingCount: null
      });
      updateStats();
      break;

    case 'itemSynced':
      addMessage({
        type: 'success',
        title: 'Enviado con éxito',
        text: data.message,
        duration: 3000
      });
      updateStats();
      break;

    case 'syncCompleted':
      addMessage({
        type: 'success',
        title: 'Sincronización completada',
        text: `${data.syncedCount} elemento${data.syncedCount > 1 ? 's' : ''} sincronizado${data.syncedCount > 1 ? 's' : ''}`,
        duration: 4000
      });
      updateStats();
      break;

    case 'syncError':
      addMessage({
        type: 'error',
        title: 'Error de sincronización',
        text: `No se pudo enviar un ${data.type === 'record' ? 'registro' : 'asistencia'}`,
        duration: 5000,
        closable: true
      });
      break;

    case 'connection':
      // Ya manejado por el listener de conectividad
      break;
  }
}

// Actualizar estadísticas
async function updateStats() {
  try {
    const stats = await apiService.getOfflineStats();
    Object.assign(pendingStats, stats);
  } catch (error) {
    console.error('❌ Error actualizando estadísticas offline:', error);
  }
}

// Agregar mensaje
function addMessage(messageData) {
  const message = {
    id: ++messageIdCounter,
    ...messageData,
    timestamp: Date.now()
  };

  messages.value.push(message);

  // Auto-remover mensaje después de la duración especificada
  if (message.duration) {
    setTimeout(() => {
      dismissMessage(message.id);
    }, message.duration);
  }

  // Limitar a 5 mensajes máximo
  if (messages.value.length > 5) {
    messages.value.shift();
  }
}

// Descartar mensaje
function dismissMessage(messageId) {
  const index = messages.value.findIndex(m => m.id === messageId);
  if (index !== -1) {
    messages.value.splice(index, 1);
  }
}

// Obtener clase CSS para el tipo de mensaje
function getMessageClass(type) {
  const classes = {
    offline: 'bg-blue-500 text-white',
    syncing: 'bg-yellow-500 text-white',
    success: 'bg-green-500 text-white',
    error: 'bg-red-500 text-white',
    info: 'bg-gray-500 text-white'
  };
  return classes[type] || classes.info;
}

// Formatear tiempo
function formatTime(timestamp) {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('es-ES', { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
}

// Forzar sincronización manual
async function forceSyncNow() {
  if (syncInProgress.value || connectionStatus.value !== 'online') {
    return;
  }

  syncInProgress.value = true;
  
  addMessage({
    type: 'syncing',
    title: 'Sincronizando',
    text: 'Enviando elementos pendientes...',
    duration: null
  });

  try {
    await apiService.forceSyncPending();
    addMessage({
      type: 'success',
      title: 'Sincronización manual exitosa',
      text: 'Todos los elementos han sido enviados',
      duration: 4000
    });
  } catch (error) {
    addMessage({
      type: 'error',
      title: 'Error en sincronización',
      text: error.message || 'No se pudo completar la sincronización',
      duration: 5000,
      closable: true
    });
  } finally {
    syncInProgress.value = false;
    await updateStats();
  }
}
</script>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-up-move {
  transition: transform 0.3s ease;
}
</style>
