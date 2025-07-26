<template>
  <div v-if="!isOnline" class="fixed bottom-4 right-4 z-50 bg-red-500 text-white p-3 rounded-lg shadow-lg flex items-center">
    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
    </svg>
    <span>Sin conexión a internet. Algunas funciones no estarán disponibles.</span>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { checkInternetConnection } from '../utils/network.js';

const isOnline = ref(true);
let intervalId = null;

// Verificar conexión inicialmente y cada 30 segundos
onMounted(async () => {
  isOnline.value = await checkInternetConnection();
  
  // Verificar periódicamente la conexión
  intervalId = setInterval(async () => {
    isOnline.value = await checkInternetConnection();
  }, 30000); // Cada 30 segundos
});

// Limpiar el intervalo cuando el componente se desmonta
onUnmounted(() => {
  if (intervalId) clearInterval(intervalId);
});
</script>
