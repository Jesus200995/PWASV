<script setup>
import { computed, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ConnectivityStatus from './components/ConnectivityStatus.vue';

const router = useRouter();
const isLoggingOut = ref(false);
const showWelcome = ref(false);
const userData = ref(null);

onMounted(() => {
  // Obtener los datos del usuario del localStorage
  const storedUser = localStorage.getItem('user');
  if (storedUser) {
    userData.value = JSON.parse(storedUser);
    
    // Mostrar mensaje de bienvenida solo si recién inició sesión
    const justLoggedIn = sessionStorage.getItem('justLoggedIn');
    if (justLoggedIn) {
      showWelcome.value = true;
      sessionStorage.removeItem('justLoggedIn');
      
      // Ocultar el mensaje después de 3 segundos
      setTimeout(() => {
        showWelcome.value = false;
      }, 3000);
    }
  }
});

const isLoggedIn = computed(() => {
  return localStorage.getItem('user') !== null;
});

const userName = computed(() => {
  if (userData.value) {
    return userData.value.nombre_completo;
  }
  return '';
});

function logout() {
  isLoggingOut.value = true;
  
  // Simulamos un pequeño retraso para mostrar la animación
  setTimeout(() => {
    localStorage.removeItem('user');
    router.push('/login');
    isLoggingOut.value = false;
  }, 600);
}
</script>

<template>
  <div class="min-h-screen">
    <!-- Mensaje de bienvenida -->
    <transition name="slide-down">
      <div v-if="showWelcome" class="fixed top-0 inset-x-0 z-50 bg-primary-dark text-white p-3 shadow-lg">
        <div class="max-w-6xl mx-auto flex items-center justify-between">
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <span class="font-medium">¡Bienvenido, {{ userName }}!</span>
          </div>
          <button @click="showWelcome = false" class="text-white hover:text-gray-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </transition>

    <!-- Indicador de estado de conexión -->
    <ConnectivityStatus />

    <nav v-if="isLoggedIn" class="bg-primary text-white shadow-lg sticky top-0 z-40">
      <div class="max-w-6xl mx-auto px-4">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <span class="font-bold text-xl tracking-wide">Sembrando Vida</span>
          </div>
          <div class="flex items-center space-x-3">
            <div class="hidden md:block text-right mr-3">
              <p class="text-sm text-white/80">Sesión iniciada como:</p>
              <p class="font-medium">{{ userName }}</p>
            </div>
            <router-link to="/" class="px-4 py-2 rounded-lg hover:bg-primary-dark transition-all duration-200 transform hover:scale-105 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7m-7-7v14" />
              </svg>
              Inicio
            </router-link>
            <router-link to="/historial" class="px-4 py-2 rounded-lg hover:bg-primary-dark transition-all duration-200 transform hover:scale-105 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              Historial
            </router-link>
            <button @click="logout" class="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/20 hover:bg-white/30 transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-white/50">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main>
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Animación para el mensaje de bienvenida */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  transform: translateY(-100%);
  opacity: 0;
}
</style>
