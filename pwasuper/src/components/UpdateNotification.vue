<template>
  <Teleport to="body">
    <!-- Toast de actualización automática -->
    <Transition name="slide-up">
      <div 
        v-if="showUpdateToast" 
        class="fixed bottom-4 left-4 right-4 z-50 flex justify-center"
      >
        <div class="bg-emerald-600 text-white px-4 py-3 rounded-xl shadow-2xl flex items-center gap-3 max-w-sm w-full" style="animation: pulse-glow 1.5s infinite;">
          <div class="flex-shrink-0">
            <svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
          <div class="flex-1">
            <p class="text-sm font-semibold">Actualizando...</p>
            <p class="text-xs text-emerald-100">Recargando en {{ countdown }}s</p>
          </div>
          <div class="flex-shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-emerald-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Modal obligatorio (solo si no es auto-update) -->
    <div 
      v-if="showUpdateModal && !autoUpdate" 
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/70"
    >
      <div class="w-11/12 max-w-md p-5 bg-white rounded-lg shadow-xl">
        <div class="text-center">
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

          <button
            @click="updateServiceWorker"
            class="w-full flex items-center justify-center px-5 py-3 font-medium text-white bg-primary rounded-lg shadow-md hover:bg-primary-dark transition-colors"
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
import { ref, onMounted, onUnmounted } from 'vue';
import { registerServiceWorker } from '../utils/serviceWorkerRegistration.js';

const showUpdateModal = ref(false);
const showUpdateToast = ref(false);
const autoUpdate = ref(true);
const registration = ref(null);
const updateAvailable = ref(false);
const countdown = ref(3);
let countdownInterval = null;

// Método para actualizar el service worker manualmente
function updateServiceWorker() {
  if (registration.value && registration.value.waiting) {
    registration.value.waiting.postMessage({ type: 'SKIP_WAITING' });
  }
  window.location.reload();
}

// Mostrar toast y cuenta regresiva (rápido - 2 segundos)
function showAutoUpdateToast() {
  showUpdateToast.value = true;
  countdown.value = 2;
  
  countdownInterval = setInterval(() => {
    countdown.value--;
    if (countdown.value <= 0) {
      clearInterval(countdownInterval);
      window.location.reload();
    }
  }, 1000);
}

// Callback cuando hay actualización
function handleUpdate(version) {
  console.log('🔔 Actualización detectada:', version);
  updateAvailable.value = true;
  
  if (version === 'auto-reload') {
    // Recarga automática desde el SW
    showAutoUpdateToast();
  } else {
    // Nueva versión disponible
    autoUpdate.value = true;
    showAutoUpdateToast();
  }
}

onMounted(() => {
  // Registrar SW con callback de actualización
  registerServiceWorker(handleUpdate).then((reg) => {
    registration.value = reg;
    
    // Verificar si hay una actualización esperando
    if (reg && reg.waiting) {
      handleUpdate('waiting');
    }
  });
});

onUnmounted(() => {
  if (countdownInterval) {
    clearInterval(countdownInterval);
  }
});

defineExpose({
  showUpdateModal,
  updateAvailable,
  showUpdateToast
});
</script>

<style scoped>
/* Animación de entrada desde abajo */
.slide-up-enter-active {
  animation: slideUp 0.3s ease-out;
}

.slide-up-leave-active {
  animation: slideUp 0.2s ease-in reverse;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Efecto de brillo pulsante */
@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4);
  }
  50% {
    box-shadow: 0 4px 30px rgba(16, 185, 129, 0.7);
  }
}
</style>
