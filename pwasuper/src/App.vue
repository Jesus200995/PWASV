<script setup>
import { computed, ref, onMounted, onUnmounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import ConnectivityStatus from './components/ConnectivityStatus.vue';
import UpdateNotification from './components/UpdateNotification.vue';
import SupportBubble from './components/SupportBubble.vue';
import WelcomeModalNew from './components/WelcomeModalNew.vue';
import PoinsettiaFlower from './components/PoinsettiaFlower.vue';
import { useNotifications } from './composables/useNotifications.js';

const router = useRouter();
const route = useRoute();
const isLoggingOut = ref(false);
const showWelcome = ref(false);
const userData = ref(null);
const showMobileMenu = ref(false);

// Sistema de notificaciones en tiempo real
const { unreadCount, startPolling, stopPolling } = useNotifications();
let notificationPollingId = null;

// Watcher para detectar cambios de ruta y actualizar el estado
watch(() => route.path, () => {
  // Verificar estado de autenticación en cada cambio de ruta
  const storedUser = localStorage.getItem('user');
  if (storedUser && !userData.value) {
    try {
      userData.value = JSON.parse(storedUser);
    } catch (error) {
      console.error('Error parsing user data:', error);
      localStorage.clear();
      sessionStorage.clear();
    }
  } else if (!storedUser && userData.value) {
    userData.value = null;
  }
});

// Listener para cambios en localStorage (útil para logout desde otras pestañas)
const handleStorageChange = (e) => {
  if (e.key === 'user') {
    if (e.newValue === null) {
      // Si se eliminó el usuario del localStorage, limpiar estado y redirigir
      userData.value = null;
      showWelcome.value = false;
      showMobileMenu.value = false;
      
      // Detener polling de notificaciones
      if (notificationPollingId) {
        stopPolling(notificationPollingId);
        notificationPollingId = null;
      }
      
      router.push('/login');
    } else if (e.newValue && !userData.value) {
      // Si se agregó un usuario y no tenemos datos, cargarlos
      try {
        userData.value = JSON.parse(e.newValue);
        
        // Reiniciar polling de notificaciones para el nuevo usuario
        if (notificationPollingId) {
          stopPolling(notificationPollingId);
        }
        notificationPollingId = startPolling();
        
      } catch (error) {
        console.error('Error parsing user data:', error);
        localStorage.removeItem('user');
      }
    }
  }
};

onMounted(() => {
  // Verificar el estado de autenticación al cargar la app
  const storedUser = localStorage.getItem('user');
  
  if (storedUser) {
    try {
      userData.value = JSON.parse(storedUser);
      
      // Inicializar sistema de notificaciones una vez que el usuario está identificado
      notificationPollingId = startPolling();
      
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
    } catch (error) {
      console.error('Error parsing user data:', error);
      // Si hay error al parsear, limpiar y redirigir
      localStorage.clear();
      sessionStorage.clear();
      router.push('/login');
    }
  } else {
    // Si no hay usuario logueado, asegurar que esté en login
    if (route.name !== 'Login' && route.name !== 'Register') {
      router.push('/login');
    }
  }
  
  // Escuchar cambios en localStorage
  window.addEventListener('storage', handleStorageChange);
});

onUnmounted(() => {
  // Limpiar listener
  window.removeEventListener('storage', handleStorageChange);
  // Detener el polling de notificaciones
  stopPolling(notificationPollingId);
});

const isLoggedIn = computed(() => {
  // Verificar tanto el ref como el localStorage para mayor seguridad
  return userData.value !== null && localStorage.getItem('user') !== null;
});

const userName = computed(() => {
  if (userData.value && userData.value.nombre_completo) {
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
  
  // Detener el polling de notificaciones
  stopPolling(notificationPollingId);
  notificationPollingId = null;
  
  // Limpiar el estado reactivo primero
  userData.value = null;
  showWelcome.value = false;
  
  // Guardar el estado de asistencia del localStorage antes de limpiarlo
  const today = new Date().toISOString().split('T')[0];
  const storedUser = localStorage.getItem('user');
  let userId = null;
  
  if (storedUser) {
    try {
      const user = JSON.parse(storedUser);
      userId = user.id;
    } catch (error) {
      console.error('Error parsing user data:', error);
    }
  }
  
  // Si tenemos el ID del usuario, guardar su estado de asistencia y la última fecha
  let asistenciaHoy = null;
  let ultimaFecha = null;
  
  if (userId) {
    asistenciaHoy = localStorage.getItem(`asistencia_${userId}_${today}`);
    ultimaFecha = localStorage.getItem(`asistencia_ultima_fecha_${userId}`);
  }
  
  // Limpiar localStorage y sessionStorage (excepto datos de asistencia)
  localStorage.clear();
  sessionStorage.clear();
  
  // Restaurar el estado de asistencia del día en localStorage si existe
  if (userId && asistenciaHoy) {
    localStorage.setItem(`asistencia_${userId}_${today}`, asistenciaHoy);
  }
  
  // Restaurar la última fecha consultada
  if (userId && ultimaFecha) {
    localStorage.setItem(`asistencia_ultima_fecha_${userId}`, ultimaFecha);
  }
  
  // Pequeño delay para que se vea la limpieza del estado
  setTimeout(() => {
    // Recargar la página completamente para limpiar todo el estado
    window.location.href = '/login';
  }, 100);
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Nuevo modal de bienvenida mejorado -->
    <WelcomeModalNew 
      :show="showWelcome"
      :userName="userName"
      @close="showWelcome = false"
    />

    <!-- Indicador de estado de conexión -->
    <ConnectivityStatus :show="route.name === 'Home' && !showMobileMenu" />

    <!-- Header móvil con menú hamburguesa -->
    <header v-if="isLoggedIn" class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-40">
      <div class="max-w-sm mx-auto px-4 py-3">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <!-- Icono de plantita con contorno neón -->
            <PoinsettiaFlower />
            <div>
              <h1 class="header-title text-base mb-0">Sembrando Vida</h1>
              <p class="text-xs text-gray-500 -mt-0.5">{{ userName }}</p>
            </div>
          </div>
          
          <div class="flex items-center space-x-2">
            <!-- Botón de notificaciones -->
            <router-link 
              to="/notificaciones"
              class="relative p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition-colors"
              :class="{ 'bg-blue-50 text-blue-600': route.name === 'Notificaciones' }"
            >
              <!-- Icono de campanita -->
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
              </svg>
              <!-- Badge de notificaciones no leídas -->
              <span v-if="unreadCount > 0" class="absolute -top-1 -right-1 h-5 w-5 bg-red-500 text-white text-xs font-bold rounded-full flex items-center justify-center">
                {{ unreadCount > 9 ? '9+' : unreadCount }}
              </span>
            </router-link>
            
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
              to="/notificaciones" 
              @click="closeMobileMenu"
              class="flex items-center px-3 py-3 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors relative"
              :class="{ 'bg-primary/10 text-primary': route.name === 'Notificaciones' }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
              </svg>
              <span class="font-medium">Notificaciones</span>
              <!-- Badge de notificaciones no leídas en el menú -->
              <span v-if="unreadCount > 0" class="ml-auto h-5 w-5 bg-red-500 text-white text-xs font-bold rounded-full flex items-center justify-center">
                {{ unreadCount > 9 ? '9+' : unreadCount }}
              </span>
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
            
            <router-link 
              to="/support" 
              @click="closeMobileMenu"
              class="flex items-center px-3 py-3 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors"
              :class="{ 'bg-primary/10 text-primary': route.name === 'Support' }"
            >
              <font-awesome-icon 
                icon="headset"
                class="h-5 w-5 mr-3"
              />
              <span class="font-medium">Soporte</span>
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
    <main class="main-content" :style="{ paddingTop: isLoggedIn ? '48px' : '0' }">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Modal de actualización de la aplicación (obligatorio) -->
    <UpdateNotification />

    <!-- Burbuja de soporte (solo visible cuando el usuario está logueado y no está en la vista de soporte) -->
    <SupportBubble v-if="isLoggedIn" :hideOnSupportPage="route.name === 'Support'" />
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

/* Título del header con tipografía elegante y animación de brillo */
.header-title {
  font-family: 'Segoe UI', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
  font-weight: 500;
  letter-spacing: 0.5px;
  color: #16a34a;
  background: linear-gradient(
    90deg,
    #16a34a 0%,
    #16a34a 40%,
    #4ade80 50%,
    #16a34a 60%,
    #16a34a 100%
  );
  background-size: 200% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: textShine 2.5s ease-in-out infinite;
}

@keyframes textShine {
  0% {
    background-position: 100% 50%;
  }
  100% {
    background-position: -100% 50%;
  }
}

/* Colores personalizados para verde manzana */
:root {
  --apple-green: #6CC651;
  --apple-green-dark: #5DB33C;
  --apple-green-light: #8FD968;
}

.bg-apple-green {
  background-color: #6CC651;
}

.bg-apple-green-dark {
  background-color: #5DB33C;
}

.text-apple-green {
  color: #6CC651;
}

.text-apple-green-dark {
  color: #5DB33C;
}
</style>
