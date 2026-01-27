<template>
  <teleport to="body">
    <!-- Fondo difuminado -->
    <transition name="blur-fade">
      <div 
        v-if="show" 
        class="fixed inset-0 bg-black/40 backdrop-blur-md z-[1000]"
        @click="closeModal"
      ></div>
    </transition>

    <!-- Modal centrado -->
    <transition name="welcome-modal">
      <div 
        v-if="show"
        class="fixed inset-0 flex items-center justify-center z-[1001] pointer-events-none p-4"
      >
        <div 
          class="relative bg-white rounded-2xl shadow-2xl w-full max-w-xs p-5 pointer-events-auto transform transition-all"
          @click.stop
        >
          <!-- Contenedor principal con gradiente verde manzana -->
          <div class="relative">
            <!-- Gradiente de fondo decorativo (más sutil) -->
            <div class="absolute -top-8 -right-8 w-28 h-28 bg-gradient-to-br from-apple-green/15 to-transparent rounded-full blur-2xl"></div>
            <div class="absolute -bottom-8 -left-8 w-28 h-28 bg-gradient-to-tr from-apple-green/10 to-transparent rounded-full blur-2xl"></div>

            <!-- Contenido -->
            <div class="relative z-10 text-center">
              <!-- Icono decorativo de bienvenida - estático y elegante -->
              <div class="mx-auto mb-4 w-14 h-14 bg-gradient-to-br from-apple-green to-apple-green-dark rounded-full flex items-center justify-center shadow-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>

              <!-- Texto de bienvenida -->
              <h1 class="text-xl font-bold bg-gradient-to-r from-apple-green to-apple-green-dark bg-clip-text text-transparent mb-1">
                ¡Bienvenido!
              </h1>
              
              <p class="text-gray-700 font-medium mb-0.5 text-sm">
                {{ userName }}
              </p>
              
              <p class="text-gray-500 text-xs mb-4">
                Sesión iniciada correctamente
              </p>

              <!-- Barra de progreso con tiempo -->
              <div class="mb-3">
                <div class="relative h-1 bg-gray-200 rounded-full overflow-hidden">
                  <!-- Barra de progreso animada -->
                  <div 
                    class="h-full bg-gradient-to-r from-apple-green to-apple-green-dark rounded-full transition-all"
                    :style="{ width: progressPercentage + '%' }"
                  ></div>
                </div>
              </div>

              <!-- Botón para cerrar manualmente -->
              <button
                @click="closeModal"
                class="w-full bg-gradient-to-r from-apple-green to-apple-green-dark text-white font-semibold py-2.5 rounded-xl hover:shadow-lg transition-all duration-300 transform hover:scale-105 active:scale-95 flex items-center justify-center gap-2 text-sm"
              >
                Continuar
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  userName: {
    type: String,
    default: 'Usuario'
  }
});

const emit = defineEmits(['close']);

const duration = 3000; // 3 segundos
const remainingTime = ref(duration);
const progressPercentage = ref(100);
let animationInterval = null;
let timeoutId = null;

const updateProgress = () => {
  const elapsed = duration - remainingTime.value;
  progressPercentage.value = ((elapsed) / duration) * 100;
};

watch(() => props.show, (newVal) => {
  if (newVal) {
    remainingTime.value = duration;
    progressPercentage.value = 100;
    
    // Actualizar barra cada 50ms
    animationInterval = setInterval(() => {
      remainingTime.value = Math.max(0, remainingTime.value - 50);
      updateProgress();
      
      if (remainingTime.value <= 0) {
        clearInterval(animationInterval);
        closeModal();
      }
    }, 50);
  } else {
    if (animationInterval) {
      clearInterval(animationInterval);
    }
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
  }
});

const closeModal = () => {
  if (animationInterval) {
    clearInterval(animationInterval);
  }
  if (timeoutId) {
    clearTimeout(timeoutId);
  }
  emit('close');
};

onUnmounted(() => {
  if (animationInterval) {
    clearInterval(animationInterval);
  }
  if (timeoutId) {
    clearTimeout(timeoutId);
  }
});
</script>

<style scoped>
/* Animaciones */
.blur-fade-enter-active,
.blur-fade-leave-active {
  transition: backdrop-filter 0.4s ease, opacity 0.4s ease;
}

.blur-fade-enter-from,
.blur-fade-leave-to {
  backdrop-filter: blur(0px);
  opacity: 0;
}

.welcome-modal-enter-active {
  animation: welcomeIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.welcome-modal-leave-active {
  animation: welcomeOut 0.3s ease-in;
}

@keyframes welcomeIn {
  from {
    opacity: 0;
    transform: scale(0.5) translateY(-50px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes welcomeOut {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(0.95);
  }
}

/* Animación de bounce sutil */
@keyframes bounceSubtle {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

.animate-bounce-subtle {
  animation: bounceSubtle 2s ease-in-out infinite;
}

/* Colores personalizados para verde manzana (fallback si Tailwind no los carga) */
:root {
  --apple-green: #6CC651;
  --apple-green-dark: #5DB33C;
  --apple-green-light: #8FD968;
}

.from-apple-green {
  --tw-gradient-from: #6CC651 var(--tw-gradient-from-position);
  --tw-gradient-to: rgb(108 198 81 / 0) var(--tw-gradient-to-position);
  --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to);
}

.to-apple-green-dark {
  --tw-gradient-to: #5DB33C var(--tw-gradient-to-position);
}

.bg-gradient-to-r.from-apple-green {
  background-image: linear-gradient(to right, #6CC651, #5DB33C);
}

.bg-clip-text {
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.bg-gradient-to-r {
  background-image: linear-gradient(to right, var(--tw-gradient-stops));
}

.from-apple-green\/20 {
  --tw-gradient-from: rgb(108 198 81 / 0.2) var(--tw-gradient-from-position);
  --tw-gradient-to: rgb(108 198 81 / 0) var(--tw-gradient-to-position);
  --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to);
}

.to-transparent {
  --tw-gradient-to: transparent var(--tw-gradient-to-position);
}

.from-apple-green\/15 {
  --tw-gradient-from: rgb(108 198 81 / 0.15) var(--tw-gradient-from-position);
  --tw-gradient-to: rgb(108 198 81 / 0) var(--tw-gradient-to-position);
  --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to);
}

.bg-apple-green {
  background-color: #6CC651;
}

.bg-apple-green-dark {
  background-color: #5DB33C;
}

.text-apple-green-dark {
  color: #5DB33C;
}

.border-apple-green\/20 {
  border-color: rgb(108 198 81 / 0.2);
}

.bg-gradient-to-r.from-apple-green\/10.to-apple-green-dark\/10 {
  background-image: linear-gradient(to right, rgb(108 198 81 / 0.1), rgb(93 179 60 / 0.1));
}

.text-white {
  color: white;
}
</style>
