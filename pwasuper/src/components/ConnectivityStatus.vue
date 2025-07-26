<template>
  <div v-if="shouldShow" class="fixed bottom-4 right-4 z-40 max-w-sm">
    <!-- Indicador de estado offline -->
    <div 
      v-if="!isOnline" 
      class="bg-red-500 text-white p-3 rounded-lg shadow-lg flex items-center mb-2 transition-all duration-300"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-12.728 12.728m0-12.728l12.728 12.728" />
      </svg>
      <div class="flex-1">
        <span class="text-sm font-medium">Sin conexión a internet</span>
        <div v-if="hasPendingRecords" class="text-xs mt-1 opacity-90">
          {{ pendingRecords.total }} registro(s) pendientes
        </div>
      </div>
    </div>

    <!-- Indicador de sincronización en progreso -->
    <div 
      v-else-if="isSyncing" 
      class="bg-blue-500 text-white p-3 rounded-lg shadow-lg transition-all duration-300"
    >
      <div class="flex items-center mb-2">
        <div class="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white mr-2"></div>
        <span class="text-sm font-medium">Sincronizando...</span>
      </div>
      
      <div v-if="syncProgress.total > 0" class="text-xs mb-2">
        {{ syncProgress.procesados }}/{{ syncProgress.total }} registros
      </div>
      
      <!-- Barra de progreso -->
      <div v-if="syncProgress.total > 0" class="w-full bg-blue-600 rounded-full h-2">
        <div 
          class="bg-white rounded-full h-2 transition-all duration-300"
          :style="{ width: `${(syncProgress.procesados / syncProgress.total) * 100}%` }"
        ></div>
      </div>
    </div>

    <!-- Indicador de registros pendientes (cuando hay conexión pero hay pendientes) -->
    <div 
      v-else-if="hasPendingRecords && isOnline" 
      class="bg-yellow-500 text-white p-3 rounded-lg shadow-lg cursor-pointer hover:bg-yellow-600 transition-all duration-300"
      @click="$emit('force-sync')"
    >
      <div class="flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <div class="flex-1">
          <span class="text-sm font-medium">{{ pendingRecords.total }} pendiente(s)</span>
          <div class="text-xs mt-1 opacity-90">Toca para sincronizar ahora</div>
        </div>
      </div>
    </div>

    <!-- Mensaje de estado exitoso -->
    <div 
      v-else-if="syncMessage && (syncMessage.includes('correctamente') || syncMessage.includes('sincronizado'))" 
      class="bg-green-500 text-white p-3 rounded-lg shadow-lg transition-all duration-300"
    >
      <div class="flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        <span class="text-sm font-medium">{{ syncMessage }}</span>
      </div>
    </div>

    <!-- Mensaje de error -->
    <div 
      v-else-if="syncMessage && (syncMessage.includes('Error') || syncMessage.includes('error'))" 
      class="bg-red-500 text-white p-3 rounded-lg shadow-lg transition-all duration-300"
    >
      <div class="flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <span class="text-sm font-medium">{{ syncMessage }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

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
const emit = defineEmits(['force-sync']);

// Estado computado
const hasPendingRecords = computed(() => props.pendingRecords.total > 0);

const shouldShow = computed(() => {
  return !props.isOnline || 
         props.isSyncing || 
         props.syncMessage || 
         hasPendingRecords.value;
});
</script>

<style scoped>
/* Animaciones suaves para las transiciones */
.transition-all {
  transition: all 0.3s ease-in-out;
}

/* Efecto hover suave */
.hover\:bg-yellow-600:hover {
  background-color: rgb(217, 119, 6);
}
</style>
