<template>
  <Teleport to="body">
    <div 
      v-if="showUpdateModal" 
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/70"
    >
      <div class="w-11/12 max-w-md p-5 bg-white rounded-lg shadow-xl">
        <div class="text-center">
          <!-- Icono de actualización -->
          <div class="flex justify-center mb-4">
            <div class="p-3 bg-blue-100 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </div>
          </div>
          
          <h2 class="text-xl font-bold text-gray-800 mb-2">¡Nueva versión disponible!</h2>
          <p class="text-sm text-gray-600 mb-6">
            Una actualización importante está disponible. Es necesario actualizar la aplicación para continuar.
          </p>

          <!-- Botón de actualizar -->
          <button
            @click="updateServiceWorker"
            class="w-full flex items-center justify-center px-5 py-3 font-medium text-white bg-primary rounded-lg shadow-md hover:bg-primary-dark transition-colors animate-pulse"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Actualizar Ahora
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const showUpdateModal = ref(false);
const registration = ref(null);
const updateAvailable = ref(false);

// Método para actualizar el service worker
function updateServiceWorker() {
  if (registration.value && registration.value.waiting) {
    // Enviar mensaje al SW para que se actualice
    registration.value.waiting.postMessage({ type: 'SKIP_WAITING' });
  }
  
  // Recargar la página para aplicar la nueva versión
  window.location.reload();
}

// Verificar actualizaciones del service worker al montar el componente
onMounted(() => {
  // Solo si el navegador soporta service workers
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.ready
      .then((reg) => {
        registration.value = reg;
        
        // Verificar si hay una actualización ya esperando
        if (reg.waiting) {
          updateAvailable.value = true;
          showUpdateModal.value = true;
          return;
        }
        
        // Escuchar por nuevas actualizaciones
        reg.addEventListener('updatefound', () => {
          const newWorker = reg.installing;
          
          newWorker.addEventListener('statechange', () => {
            // Cuando el nuevo SW está instalado y esperando
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              updateAvailable.value = true;
              showUpdateModal.value = true;
            }
          });
        });
      });
    
    // Escuchar eventos de controllerchange (cuando el SW se actualiza)
    let refreshing = false;
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      if (!refreshing) {
        refreshing = true;
        window.location.reload();
      }
    });
  }
});

// Exportar propiedades para uso externo
defineExpose({
  showUpdateModal,
  updateAvailable
});
</script>

<style scoped>
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
}
</style>
