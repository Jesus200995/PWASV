<template>
  <!-- Indicador de estado offline/sync en la parte superior -->
  <div v-if="shouldShow" class="fixed top-0 left-0 right-0 z-50 transition-all duration-300">
    <!-- Barra de estado offline -->
    <div 
      v-if="!isOnline" 
      class="bg-red-500 text-white px-4 py-2 text-center text-sm font-medium"
    >
      <div class="flex items-center justify-center space-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-12.728 12.728m0-12.728l12.728 12.728" />
        </svg>
        <span>Sin conexión a internet</span>
        <span v-if="hasPendingRecords" class="bg-red-600 px-2 py-1 rounded-full text-xs">
          {{ pendingRecords.total }} pendientes
        </span>
      </div>
    </div>

    <!-- Barra de progreso de sincronización -->
    <div 
      v-else-if="isSyncing" 
      class="bg-blue-500 text-white"
    >
      <div class="px-4 py-2 text-center text-sm font-medium">
        <div class="flex items-center justify-center space-x-2 mb-1">
          <div class="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white"></div>
          <span>{{ syncMessage || 'Sincronizando...' }}</span>
        </div>
      </div>
      
      <!-- Barra de progreso -->
      <div v-if="syncProgress.total > 0" class="w-full bg-blue-600 h-1">
        <div 
          class="bg-white h-1 transition-all duration-300"
          :style="{ width: `${(syncProgress.procesados / syncProgress.total) * 100}%` }"
        ></div>
      </div>
    </div>

    <!-- Mensaje de estado general -->
    <div 
      v-else-if="syncMessage && isOnline" 
      class="px-4 py-2 text-center text-sm font-medium transition-all duration-300"
      :class="{
        'bg-green-500 text-white': syncMessage.includes('correctamente') || syncMessage.includes('sincronizado'),
        'bg-yellow-500 text-white': syncMessage.includes('Error') || syncMessage.includes('error'),
        'bg-blue-500 text-white': !syncMessage.includes('correctamente') && !syncMessage.includes('Error')
      }"
    >
      <div class="flex items-center justify-center space-x-2">
        <!-- Icono de éxito -->
        <svg 
          v-if="syncMessage.includes('correctamente') || syncMessage.includes('sincronizado')" 
          xmlns="http://www.w3.org/2000/svg" 
          class="h-4 w-4" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        
        <!-- Icono de error -->
        <svg 
          v-else-if="syncMessage.includes('Error') || syncMessage.includes('error')" 
          xmlns="http://www.w3.org/2000/svg" 
          class="h-4 w-4" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        
        <!-- Icono de información -->
        <svg 
          v-else
          xmlns="http://www.w3.org/2000/svg" 
          class="h-4 w-4" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        
        <span>{{ syncMessage }}</span>
      </div>
    </div>

    <!-- Indicador de registros pendientes cuando está online pero hay pendientes -->
    <div 
      v-else-if="hasPendingRecords && isOnline && !isSyncing" 
      class="bg-yellow-500 text-white px-4 py-2 text-center text-sm font-medium cursor-pointer hover:bg-yellow-600 transition-colors"
      @click="$emit('force-sync')"
    >
      <div class="flex items-center justify-center space-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <span>{{ pendingRecords.total }} registro(s) pendientes</span>
        <span class="text-xs opacity-75">- Toca para sincronizar</span>
      </div>
    </div>
  </div>

  <!-- Modal de detalles de sincronización (opcional) -->
  <div 
    v-if="showDetails && hasPendingRecords" 
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
    @click="showDetails = false"
  >
    <div 
      class="bg-white rounded-lg max-w-md w-full p-6"
      @click.stop
    >
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold text-gray-800">Registros Pendientes</h3>
        <button 
          @click="showDetails = false"
          class="text-gray-400 hover:text-gray-600"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="space-y-3">
        <div v-if="pendingRecords.entradas > 0" class="flex justify-between items-center">
          <span class="text-gray-600">Entradas pendientes:</span>
          <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-sm font-medium">
            {{ pendingRecords.entradas }}
          </span>
        </div>

        <div v-if="pendingRecords.salidas > 0" class="flex justify-between items-center">
          <span class="text-gray-600">Salidas pendientes:</span>
          <span class="bg-red-100 text-red-800 px-2 py-1 rounded-full text-sm font-medium">
            {{ pendingRecords.salidas }}
          </span>
        </div>

        <hr class="my-4">

        <div class="grid grid-cols-2 gap-3">
          <button 
            @click="handleForceSync"
            :disabled="!isOnline || isSyncing"
            class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors text-sm"
          >
            {{ isSyncing ? 'Sincronizando...' : 'Sincronizar Ahora' }}
          </button>

          <button 
            @click="handleClearRecords"
            :disabled="isSyncing"
            class="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors text-sm"
          >
            Eliminar Todo
          </button>
        </div>

        <p class="text-xs text-gray-500 text-center mt-4">
          Los registros se sincronizarán automáticamente cuando tengas conexión a internet.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

// Props
const props = defineProps({
  isOnline: {
    type: Boolean,
    default: true
  },
  isSyncing: {
    type: Boolean,
    default: false
  },
  syncProgress: {
    type: Object,
    default: () => ({ total: 0, procesados: 0, errores: 0 })
  },
  pendingRecords: {
    type: Object,
    default: () => ({ entradas: 0, salidas: 0, total: 0 })
  },
  syncMessage: {
    type: String,
    default: ''
  }
});

// Emits
const emit = defineEmits(['force-sync', 'clear-records']);

// Estado local
const showDetails = ref(false);

// Computed
const shouldShow = computed(() => {
  return !props.isOnline || 
         props.isSyncing || 
         props.syncMessage || 
         props.pendingRecords.total > 0;
});

const hasPendingRecords = computed(() => props.pendingRecords.total > 0);

// Métodos
function handleForceSync() {
  emit('force-sync');
  showDetails.value = false;
}

function handleClearRecords() {
  if (confirm('¿Estás seguro de que quieres eliminar todos los registros pendientes? Esta acción no se puede deshacer.')) {
    emit('clear-records');
    showDetails.value = false;
  }
}

// Mostrar detalles al hacer doble clic en el indicador de pendientes
function toggleDetails() {
  if (hasPendingRecords.value) {
    showDetails.value = !showDetails.value;
  }
}
</script>

<style scoped>
/* Animaciones adicionales si se necesitan */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: transform 0.3s ease;
}

.slide-down-enter-from {
  transform: translateY(-100%);
}

.slide-down-leave-to {
  transform: translateY(-100%);
}
</style>
