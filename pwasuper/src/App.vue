<script setup>
import { computed, ref, onMounted, onUnmounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import ConnectivityStatus from './components/ConnectivityStatus.vue';
import UpdateNotification from './components/UpdateNotification.vue';
import SupportBubble from './components/SupportBubble.vue';
import WelcomeModalNew from './components/WelcomeModalNew.vue';
import PoinsettiaFlower from './components/PoinsettiaFlower.vue';
import TerritorioModal from './components/TerritorioModal.vue';
import { useNotifications } from './composables/useNotifications.js';
import { API_URL } from './utils/network.js';

const router = useRouter();
const route = useRoute();
const isLoggingOut = ref(false);
const showWelcome = ref(false);
const userData = ref(null);
const showMobileMenu = ref(false);
const showTerritorioModal = ref(false);
const activeIcon = ref(null);
let userCheckIntervalId = null;

const setActiveIcon = (icon) => {
  activeIcon.value = icon;
};

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value;
  if (showMobileMenu.value) {
    setActiveIcon('menu');
  } else {
    setActiveIcon(null);
  }
};


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
  
  // Verificar territorio en cada cambio de ruta (solo si está logueado)
  if (userData.value && !userData.value.territorio && route.name !== 'Login' && route.name !== 'Register') {
    console.log('⚠️ [Route Change] Usuario sin territorio, mostrando modal obligatorio');
    showTerritorioModal.value = true;
  }
});

// Watcher reactivo para userData - verifica territorio cuando cambian los datos del usuario
watch(userData, (newUserData) => {
  if (newUserData && !newUserData.territorio) {
    console.log('⚠️ [Watch userData] Usuario sin territorio asignado, mostrando modal obligatorio');
    showTerritorioModal.value = true;
  }
}, { deep: true, immediate: false });

// Listener para cambios en localStorage (útil para logout desde otras pestañas)
const handleStorageChange = (e) => {
  if (e.key === 'user') {
    if (e.newValue === null) {
      // Si se eliminó el usuario del localStorage, limpiar estado y redirigir
      userData.value = null;
      showWelcome.value = false;
      showMobileMenu.value = false;
      showTerritorioModal.value = false;
      
      // Detener polling de notificaciones
      if (notificationPollingId) {
        stopPolling(notificationPollingId);
        notificationPollingId = null;
      }
      
      router.push('/login');
    } else if (e.newValue) {
      // Si se agregó o actualizó un usuario, cargar los datos
      try {
        const newUserData = JSON.parse(e.newValue);
        userData.value = newUserData;
        
        // Verificar si tiene territorio asignado
        if (!newUserData.territorio) {
          console.log('⚠️ [Storage Change] Usuario sin territorio, mostrando modal obligatorio');
          showTerritorioModal.value = true;
        }
        
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

// Función para verificar periódicamente los datos del usuario desde el servidor
// Esto detecta cambios realizados por el admin (ej: eliminar territorio)
const checkUserDataFromServer = async () => {
  if (!userData.value || !userData.value.id) return;
  
  try {
    const response = await fetch(`${API_URL}/usuarios/${userData.value.id}`);
    if (response.ok) {
      const serverUserData = await response.json();
      
      // Verificar si el territorio cambió
      const localTerritorio = userData.value.territorio;
      const serverTerritorio = serverUserData.territorio;
      
      // Si el servidor indica que ya no tiene territorio, actualizar local y mostrar modal
      if (localTerritorio && !serverTerritorio) {
        console.log('⚠️ [Server Check] Admin removió el territorio del usuario, actualizando...');
        userData.value = { ...userData.value, territorio: null };
        localStorage.setItem('user', JSON.stringify(userData.value));
        showTerritorioModal.value = true;
      } 
      // Si el servidor tiene territorio pero local no, actualizar local
      else if (!localTerritorio && serverTerritorio) {
        console.log('✅ [Server Check] Admin asignó territorio al usuario:', serverTerritorio);
        userData.value = { ...userData.value, territorio: serverTerritorio };
        localStorage.setItem('user', JSON.stringify(userData.value));
        showTerritorioModal.value = false;
      }
      // Si el territorio cambió a uno diferente, actualizar
      else if (localTerritorio !== serverTerritorio && serverTerritorio) {
        console.log('🔄 [Server Check] Territorio actualizado por admin:', serverTerritorio);
        userData.value = { ...userData.value, territorio: serverTerritorio };
        localStorage.setItem('user', JSON.stringify(userData.value));
      }
    }
  } catch (error) {
    console.warn('No se pudo verificar datos del usuario desde el servidor:', error.message);
  }
};

// Iniciar verificación periódica cada 30 segundos
const startUserDataCheck = () => {
  // Verificar inmediatamente al iniciar
  checkUserDataFromServer();
  
  // Luego cada 30 segundos
  userCheckIntervalId = setInterval(checkUserDataFromServer, 30000);
};

// Detener verificación periódica
const stopUserDataCheck = () => {
  if (userCheckIntervalId) {
    clearInterval(userCheckIntervalId);
    userCheckIntervalId = null;
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
      
      // Verificar si el usuario tiene territorio asignado
      if (!userData.value.territorio) {
        console.log('⚠️ Usuario sin territorio asignado, mostrando modal obligatorio');
        showTerritorioModal.value = true;
      }
      
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
  
  // Iniciar verificación periódica de datos del usuario (si está logueado)
  if (userData.value) {
    startUserDataCheck();
  }
});

onUnmounted(() => {
  // Limpiar listener
  window.removeEventListener('storage', handleStorageChange);
  // Detener el polling de notificaciones
  stopPolling(notificationPollingId);
  // Detener verificación de datos del usuario
  stopUserDataCheck();
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

// Función para manejar cuando se guarda el territorio
const handleTerritorioSaved = (territorio) => {
  console.log('✅ Territorio guardado:', territorio);
  showTerritorioModal.value = false;
  
  // Actualizar userData con el nuevo territorio
  if (userData.value) {
    userData.value.territorio = territorio;
  }
}

// Computed para obtener el ID del usuario actual
const currentUserId = computed(() => {
  return userData.value?.id || null;
});
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Modal obligatorio de selección de territorio -->
    <TerritorioModal 
      :isVisible="showTerritorioModal && isLoggedIn"
      :userId="currentUserId"
      @territorio-saved="handleTerritorioSaved"
    />
    <!-- Nuevo modal de bienvenida mejorado -->
    <WelcomeModalNew 
      :show="showWelcome"
      :userName="userName"
      @close="showWelcome = false"
    />

    <!-- Indicador de estado de conexión -->
    <ConnectivityStatus :show="route.name === 'Home' && !showMobileMenu" />

    <!-- Header móvil con menú hamburguesa -->
    <header v-if="isLoggedIn" class="header-decorative bg-green-800 shadow-sm border-b border-gray-200 fixed top-0 left-0 right-0 z-40 mx-2 mt-2 rounded-3xl">
      <div class="max-w-sm mx-auto px-3 py-2">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <!-- Icono de plantita con contorno neón -->
            <PoinsettiaFlower />
            <div>
              <h1 class="header-title text-sm mb-0 text-white">Sembrando Vida</h1>
              <p class="text-xs text-gray-100 -mt-1">{{ userName }}</p>
            </div>
          </div>
          
          <div class="flex items-center space-x-2">
            <!-- Botón de notificaciones -->
            <router-link
              to="/notificaciones"
              class="relative p-1.5 rounded-full text-white hover:bg-green-600 focus:outline-none transition-colors"
              :class="{ 'bg-green-600': activeIcon === 'notificaciones' }"
              @click="setActiveIcon('notificaciones')"
            >
              <!-- Icono de campanita moderno (Heroicons) -->
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-6 w-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
              </svg>
              <!-- Badge de notificaciones no leídas -->
              <span v-if="unreadCount > 0" class="absolute -top-1 -right-1 h-5 w-5 bg-red-500 text-white text-xs font-bold rounded-full flex items-center justify-center">
                {{ unreadCount > 9 ? '9+' : unreadCount }}
              </span>
            </router-link>
            
            <!-- Botón del menú hamburguesa -->
            <button
              @click="toggleMobileMenu"
              class="p-1.5 rounded-full text-white hover:bg-green-600 focus:outline-none transition-colors"
              :class="{ 'bg-green-600': activeIcon === 'menu' }"
            >
              <!-- Icono de menú moderno (Heroicons) -->
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-6 w-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Menú desplegable móvil -->
    <Transition name="menu-slide">
      <div 
        v-if="isLoggedIn && showMobileMenu" 
        class="fixed top-16 inset-x-0 z-30 bg-white border-b border-green-200 shadow-lg rounded-b-3xl mx-2"
      >
        <div class="px-4 py-2">
          <nav class="space-y-1">
            <router-link
              to="/"
              @click="closeMobileMenu"
              class="flex items-center px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900 transition-colors"
              :class="{ 'bg-green-50 text-green-700': route.name === 'Home' }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-3" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h7.5" />
              </svg>
              <span>Inicio</span>
            </router-link>

            <router-link
              to="/historial"
              @click="closeMobileMenu"
              class="flex items-center px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900 transition-colors"
              :class="{ 'bg-green-50 text-green-700': route.name === 'Historial' }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-3" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
              </svg>
              <span>Historial</span>
            </router-link>

            <router-link
              to="/notificaciones"
              @click="closeMobileMenu"
              class="flex items-center px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900 transition-colors relative"
              :class="{ 'bg-green-50 text-green-700': route.name === 'Notificaciones' }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-3" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
              </svg>
              <span>Notificaciones</span>
              <span v-if="unreadCount > 0" class="ml-auto h-5 w-5 bg-red-500 text-white text-xs font-bold rounded-full flex items-center justify-center">
                {{ unreadCount > 9 ? '9+' : unreadCount }}
              </span>
            </router-link>

            <router-link
              to="/profile"
              @click="closeMobileMenu"
              class="flex items-center px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900 transition-colors"
              :class="{ 'bg-green-50 text-green-700': route.name === 'Profile' }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-3" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span>Mi Perfil</span>
            </router-link>

            <router-link
              to="/support"
              @click="closeMobileMenu"
              class="flex items-center px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900 transition-colors"
              :class="{ 'bg-green-50 text-green-700': route.name === 'Support' }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-3" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9 5.25h.008v.008H12v-.008z" />
              </svg>
              <span>Soporte</span>
            </router-link>

            <router-link
              to="/settings"
              @click="closeMobileMenu"
              class="flex items-center px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900 transition-colors"
              :class="{ 'bg-green-50 text-green-700': route.name === 'Settings' }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-3" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10.343 3.94c.09-.542.56-1.003 1.11-1.227l.12-.06c.543-.248 1.15-.248 1.694 0l.12.06c.55.224 1.02.685 1.11 1.227l.028.168c.202.992 1.016 1.65 1.992 1.65h.21c.992 0 1.806.658 1.992 1.65l.028.168c.09.542.56 1.003 1.11 1.227l.12.06c.543-.248 1.15-.248 1.694 0l.12-.06c.55-.224 1.02-.685 1.11-1.227l.028-.168c.202-.992-1.016-1.65-1.992-1.65h-.21c-.992 0-1.806-.658-1.992-1.65l-.028-.168zM12 6.75a5.25 5.25 0 100 10.5 5.25 5.25 0 000-10.5zM12 15a3 3 0 100-6 3 3 0 000 6z" />
              </svg>
              <span>Configuración</span>
            </router-link>

            <div class="border-t border-gray-200 pt-2 mt-2">
              <button
                @click="logout"
                class="flex items-center w-full px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-100 hover:text-gray-900 transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-3" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
                </svg>
                <span>Cerrar Sesión</span>
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
    <main class="main-content" :style="{ paddingTop: isLoggedIn ? '120px' : '0' }">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Modal de actualización de la aplicación (obligatorio) -->
    <UpdateNotification />

    <!-- Burbuja de soporte (solo visible cuando el usuario está logueado y no está en la vista de soporte o notificaciones) -->
    <SupportBubble v-if="isLoggedIn" :hideOnSupportPage="route.name === 'Support' || route.name === 'Notificaciones'" />
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
  color: #ffffff;
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

/* Patrón decorativo para el header con hojas */
.header-decorative {
  position: relative;
  overflow: hidden;
  background-color: #006400; /* Verde fuerte actualizado */
}

.header-decorative::before {
  background-image: 
    /* Hojas grandes verdes suaves */
    radial-gradient(ellipse 60px 80px at 8% 20%, rgba(144, 238, 144, 0.7) 0%, rgba(144, 238, 144, 0.5) 30%, transparent 60%),
    radial-gradient(ellipse 55px 75px at 25% 15%, rgba(152, 251, 152, 0.65) 0%, rgba(152, 251, 152, 0.45) 30%, transparent 60%),
    radial-gradient(ellipse 65px 85px at 42% 18%, rgba(144, 238, 144, 0.7) 0%, rgba(144, 238, 144, 0.5) 30%, transparent 60%),
    radial-gradient(ellipse 58px 78px at 58% 22%, rgba(152, 251, 152, 0.65) 0%, rgba(152, 251, 152, 0.45) 30%, transparent 60%),
    radial-gradient(ellipse 62px 82px at 75% 16%, rgba(144, 238, 144, 0.7) 0%, rgba(144, 238, 144, 0.5) 30%, transparent 60%),
    radial-gradient(ellipse 56px 76px at 90% 21%, rgba(152, 251, 152, 0.65) 0%, rgba(152, 251, 152, 0.45) 30%, transparent 60%);
  /* Se eliminaron todos los gradientes de hojas blancas */
}

.header-decorative > * {
  position: relative;
  z-index: 1;
}

/* Animación del menú móvil */
.menu-slide-enter-active,
.menu-slide-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.menu-slide-enter-from,
.menu-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

body {
  background-color: #F9FAFB; /* bg-gray-50 */
}
</style>