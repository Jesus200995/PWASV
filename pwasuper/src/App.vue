<script setup>
import { computed, ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import ConnectivityStatus from './components/ConnectivityStatus.vue';

const router = useRouter();
const route = useRoute();
const isLoggingOut = ref(false);
const showWelcome = ref(false);
const userData = ref(null);
const showMobileMenu = ref(false);

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

// Función para obtener las primeras dos letras del nombre
const getUserInitials = computed(() => {
  if (userData.value && userData.value.nombre_completo) {
    const names = userData.value.nombre_completo.split(' ');
    return names.length >= 2 ? 
      (names[0][0] + names[1][0]).toUpperCase() : 
      names[0].substring(0, 2).toUpperCase();
  }
  return 'US';
});

// Función para cerrar el menú móvil cuando se navega
const closeMobileMenu = () => {
  showMobileMenu.value = false;
};

function logout() {
  isLoggingOut.value = true;
  showMobileMenu.value = false;
  
  // Simulamos un pequeño retraso para mostrar la animación
  setTimeout(() => {
    localStorage.removeItem('user');
    router.push('/login');
    isLoggingOut.value = false;
  }, 600);
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Mensaje de bienvenida -->
    <transition name="slide-down">
      <div v-if="showWelcome" class="fixed top-0 inset-x-0 z-50 bg-primary-dark text-white p-3 shadow-lg">
        <div class="max-w-sm mx-auto flex items-center justify-between">
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <span class="font-medium text-sm">¡Bienvenido, {{ userName }}!</span>
          </div>
          <button @click="showWelcome = false" class="text-white hover:text-gray-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </transition>

    <!-- Indicador de estado de conexión -->
    <ConnectivityStatus />

    <!-- Header móvil con menú hamburguesa -->
    <header v-if="isLoggedIn" class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-40">
      <div class="max-w-sm mx-auto px-4 py-3">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <div class="w-8 h-8 bg-primary rounded-full flex items-center justify-center mr-3">
              <span class="text-white text-xs font-bold">{{ getUserInitials }}</span>
            </div>
            <div>
              <h1 class="text-lg font-semibold text-gray-900">Sembrando Vida</h1>
              <p class="text-xs text-gray-500">{{ userName }}</p>
            </div>
          </div>
          
          <!-- Botón del menú hamburguesa -->
          <button 
            @click="showMobileMenu = !showMobileMenu"
            class="p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- Menú desplegable móvil -->
    <transition name="slide-down">
      <div 
        v-if="isLoggedIn && showMobileMenu" 
        class="fixed top-16 inset-x-0 z-30 bg-white border-b border-gray-200 shadow-lg"
      >
        <div class="max-w-sm mx-auto px-4 py-2">
          <nav class="space-y-1">
            <router-link 
              to="/" 
              @click="closeMobileMenu"
              class="flex items-center px-3 py-3 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors"
              :class="{ 'bg-primary/10 text-primary': route.name === 'Home' }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              <span class="font-medium">Inicio</span>
            </router-link>
            
            <router-link 
              to="/historial" 
              @click="closeMobileMenu"
              class="flex items-center px-3 py-3 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors"
              :class="{ 'bg-primary/10 text-primary': route.name === 'Historial' }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
              <span class="font-medium">Historial</span>
            </router-link>
            
            <router-link 
              to="/profile" 
              @click="closeMobileMenu"
              class="flex items-center px-3 py-3 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors"
              :class="{ 'bg-primary/10 text-primary': route.name === 'Profile' }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <span class="font-medium">Mi Perfil</span>
            </router-link>
            
            <div class="border-t border-gray-200 pt-2 mt-2">
              <button 
                @click="logout" 
                class="flex items-center w-full px-3 py-3 rounded-lg text-red-600 hover:bg-red-50 transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                <span class="font-medium">Cerrar Sesión</span>
              </button>
            </div>
          </nav>
        </div>
      </div>
    </transition>

    <!-- Overlay para cerrar el menú -->
    <div 
      v-if="isLoggedIn && showMobileMenu"
      @click="closeMobileMenu"
      class="fixed inset-0 bg-black bg-opacity-25 z-20"
    ></div>

    <!-- Contenido principal -->
    <main class="main-content">
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
