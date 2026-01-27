<script setup>
import { computed, ref, onMounted, onUnmounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import ConnectivityStatus from './components/ConnectivityStatus.vue';
import UpdateNotification from './components/UpdateNotification.vue';
import SupportBubble from './components/SupportBubble.vue';
import WelcomeModalNew from './components/WelcomeModalNew.vue';
import PoinsettiaFlower from './components/PoinsettiaFlower.vue';
import TerritorioModal from './components/TerritorioModal.vue';
import CargoModal from './components/CargoModal.vue';
import { useNotifications } from './composables/useNotifications.js';
import { API_URL } from './utils/network.js';
import { apiService } from './services/apiService.js';

const router = useRouter();
const route = useRoute();
const isLoggingOut = ref(false);
const showWelcome = ref(false);
const userData = ref(null);
const showMobileMenu = ref(false);
const showTerritorioModal = ref(false);
const showCargoModal = ref(false);
const activeIcon = ref(null);
let userCheckIntervalId = null;

const setActiveIcon = (icon) => {
  activeIcon.value = icon;
};

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value;
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
  
  // Verificar cargo en cada cambio de ruta (solo si está logueado) - PRIORIDAD SOBRE TERRITORIO
  if (userData.value && (!userData.value.cargo || userData.value.cargo.trim() === '') && route.name !== 'Login' && route.name !== 'Register') {
    console.log('⚠️ [Route Change] Usuario sin cargo, mostrando modal obligatorio');
    showCargoModal.value = true;
  }
  // Verificar territorio en cada cambio de ruta (solo si ya tiene cargo)
  else if (userData.value && !userData.value.territorio && route.name !== 'Login' && route.name !== 'Register') {
    console.log('⚠️ [Route Change] Usuario sin territorio, mostrando modal obligatorio');
    showTerritorioModal.value = true;
  }
});

// Watcher reactivo para userData - verifica cargo y territorio cuando cambian los datos del usuario
watch(userData, (newUserData) => {
  if (newUserData && (!newUserData.cargo || newUserData.cargo.trim() === '')) {
    console.log('⚠️ [Watch userData] Usuario sin cargo asignado, mostrando modal obligatorio');
    showCargoModal.value = true;
  } else if (newUserData && !newUserData.territorio) {
    console.log('⚠️ [Watch userData] Usuario sin territorio asignado, mostrando modal obligatorio');
    showTerritorioModal.value = true;
  }
}, { deep: true, immediate: true });

// Computed para verificar si el usuario necesita seleccionar cargo
const necesitaCargo = computed(() => {
  return userData.value && (!userData.value.cargo || userData.value.cargo.trim() === '');
});

// Watcher adicional para forzar el modal inmediatamente
watch(necesitaCargo, (necesita) => {
  if (necesita) {
    console.log('⚠️ [Computed necesitaCargo] Forzando modal de cargo');
    showCargoModal.value = true;
  }
}, { immediate: true });

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
// Esto detecta cambios realizados por el admin (ej: eliminar territorio o cargo)
const checkUserDataFromServer = async () => {
  if (!userData.value || !userData.value.id) return;
  
  try {
    const response = await fetch(`${API_URL}/usuarios/${userData.value.id}`);
    if (response.ok) {
      const serverUserData = await response.json();
      
      // Verificar si el cargo cambió (PRIORIDAD)
      const localCargo = userData.value.cargo;
      const serverCargo = serverUserData.cargo;
      
      // Si el servidor indica que ya no tiene cargo, actualizar local y mostrar modal
      if (localCargo && (!serverCargo || serverCargo.trim() === '')) {
        console.log('⚠️ [Server Check] Admin removió el cargo del usuario, actualizando...');
        userData.value = { ...userData.value, cargo: null };
        localStorage.setItem('user', JSON.stringify(userData.value));
        showCargoModal.value = true;
        return; // No continuar, prioridad en cargo
      }
      // Si el servidor tiene cargo pero local no, actualizar local
      else if ((!localCargo || localCargo.trim() === '') && serverCargo && serverCargo.trim() !== '') {
        console.log('✅ [Server Check] Admin asignó cargo al usuario:', serverCargo);
        userData.value = { ...userData.value, cargo: serverCargo };
        localStorage.setItem('user', JSON.stringify(userData.value));
        showCargoModal.value = false;
      }
      // Si el cargo cambió a uno diferente, actualizar
      else if (localCargo !== serverCargo && serverCargo) {
        console.log('🔄 [Server Check] Cargo actualizado por admin:', serverCargo);
        userData.value = { ...userData.value, cargo: serverCargo };
        localStorage.setItem('user', JSON.stringify(userData.value));
      }
      
      // Verificar si el territorio cambió (solo si ya tiene cargo)
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

// Iniciar verificación periódica cada 15 segundos (reactivo)
const startUserDataCheck = () => {
  // Verificar inmediatamente al iniciar
  checkUserDataFromServer();
  
  // Luego cada 15 segundos para ser más reactivo
  userCheckIntervalId = setInterval(checkUserDataFromServer, 15000);
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
      
      // Verificar si el usuario tiene cargo asignado (PRIORIDAD)
      if (!userData.value.cargo || userData.value.cargo.trim() === '') {
        console.log('⚠️ Usuario sin cargo asignado, mostrando modal obligatorio');
        showCargoModal.value = true;
      }
      // Verificar si el usuario tiene territorio asignado (solo si ya tiene cargo)
      else if (!userData.value.territorio) {
        console.log('⚠️ Usuario sin territorio asignado, mostrando modal obligatorio');
        showTerritorioModal.value = true;
      }
      // Si tiene cargo y territorio, verificar supervisor automático para técnicos
      else {
        actualizarSupervisorAutomatico(userData.value);
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
    localStorage.setItem('user', JSON.stringify(userData.value));
    
    // Ahora que tiene territorio, buscar supervisor automático si es técnico
    actualizarSupervisorAutomatico(userData.value);
  }
}

// Función para actualizar el supervisor automáticamente para técnicos
const actualizarSupervisorAutomatico = async (usuario) => {
  if (!usuario || !usuario.id) return;
  
  const cargoUpper = (usuario.cargo || '').toUpperCase();
  const cargosTecnicos = ['TECNICO SOCIAL', 'TECNICO PRODUCTIVO'];
  
  if (cargosTecnicos.includes(cargoUpper)) {
    try {
      console.log('🔍 Buscando supervisor automático para técnico...');
      const respuesta = await apiService.obtenerSupervisorAutomatico(usuario.id);
      
      if (respuesta.success && respuesta.supervisor) {
        // Actualizar en memoria y localStorage
        usuario.supervisor = respuesta.supervisor;
        userData.value.supervisor = respuesta.supervisor;
        localStorage.setItem('user', JSON.stringify(usuario));
        
        console.log(`✅ Supervisor automático actualizado: ${respuesta.supervisor}`);
      } else {
        console.log(`ℹ️ No se encontró supervisor automático: ${respuesta.mensaje}`);
      }
    } catch (error) {
      console.error('❌ Error obteniendo supervisor automático:', error);
    }
  }
}

// Función para manejar cuando se guarda el cargo
const handleCargoSaved = (cargo) => {
  console.log('✅ Cargo guardado:', cargo);
  showCargoModal.value = false;
  
  // Actualizar userData con el nuevo cargo
  if (userData.value) {
    userData.value.cargo = cargo;
    localStorage.setItem('user', JSON.stringify(userData.value));
    
    // Ahora verificar si tiene territorio
    if (!userData.value.territorio) {
      console.log('⚠️ Usuario ya tiene cargo, ahora verificar territorio');
      showTerritorioModal.value = true;
    }
  }
}

// Computed para obtener el ID del usuario actual
const currentUserId = computed(() => {
  return userData.value?.id || null;
});
</script>

<template>
  <div class="min-h-screen liquid-glass-bg relative fullscreen-bg">
    <!-- Fondo de vidrio líquido con burbujas verdes -->
    <div class="absolute inset-0 z-0 fullscreen-layer">
      <!-- Degradado base blanco-verde más intenso -->
      <div class="absolute inset-0 bg-gradient-to-br from-green-50 via-emerald-100 to-green-200"></div>
      
      <!-- Burbujas verdes grandes flotantes -->
      <div class="absolute top-10 left-10 w-64 h-64 bg-green-300/40 rounded-full filter blur-3xl animate-bubble-float-1"></div>
      <div class="absolute top-32 right-20 w-48 h-48 bg-emerald-300/35 rounded-full filter blur-3xl animate-bubble-float-2"></div>
      <div class="absolute bottom-20 left-32 w-56 h-56 bg-teal-300/40 rounded-full filter blur-3xl animate-bubble-float-3"></div>
      <div class="absolute bottom-40 right-16 w-40 h-40 bg-green-400/35 rounded-full filter blur-2xl animate-bubble-float-4"></div>
      <div class="absolute top-1/2 left-1/3 w-52 h-52 bg-emerald-400/30 rounded-full filter blur-3xl animate-bubble-float-5"></div>
      
      <!-- Burbujas pequeñas dispersas -->
      <div class="absolute top-1/4 right-1/4 w-24 h-24 bg-green-300/50 rounded-full filter blur-xl animate-bubble-rise-1"></div>
      <div class="absolute top-2/3 left-1/5 w-32 h-32 bg-emerald-300/45 rounded-full filter blur-xl animate-bubble-rise-2"></div>
      <div class="absolute bottom-1/3 right-1/3 w-28 h-28 bg-teal-300/50 rounded-full filter blur-xl animate-bubble-rise-3"></div>
      
      <!-- Capa de vidrio líquido con brillo -->
      <div class="absolute inset-0 bg-white/15 backdrop-blur-sm"></div>
      
      <!-- Reflejos de luz animados -->
      <div class="absolute top-0 left-0 right-0 h-64 bg-gradient-to-b from-white/40 to-transparent animate-shimmer-slow"></div>
      <div class="absolute bottom-0 left-0 right-0 h-64 bg-gradient-to-t from-green-200/40 to-transparent animate-pulse-gentle"></div>
    </div>

    <!-- Modal obligatorio de selección de cargo -->
    <CargoModal 
      :visible="showCargoModal && isLoggedIn"
      @cargo-guardado="handleCargoSaved"
    />

    <!-- Modal obligatorio de selección de territorio -->
    <TerritorioModal 
      :isVisible="showTerritorioModal && isLoggedIn && !showCargoModal"
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
    <header v-if="isLoggedIn" class="header-decorative bg-green-800 shadow-sm border-b border-gray-200 fixed top-0 left-0 right-0 z-40 mx-2 mt-2" :class="showMobileMenu ? 'rounded-t-3xl' : 'rounded-3xl'">
      <div class="max-w-sm mx-auto px-3 py-2">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <!-- Icono de plantita con contorno neón -->
            <PoinsettiaFlower />
            <div>
              <h1 class="header-title text-sm mb-0 font-semibold" style="color: #39ff14; letter-spacing: 0.02em;">
                Sembrando Vida
              </h1>
              <p class="text-xs text-gray-100 -mt-1">{{ userName }}</p>
            </div>
          </div>
          
          <div class="flex items-center space-x-2">
            <!-- Botón de notificaciones -->
            <router-link
              to="/notificaciones"
              class="relative p-1.5 rounded-full text-white hover:bg-green-700 focus:outline-none focus:ring-0 transition-colors"
              :class="route.name === 'Notificaciones' ? 'bg-green-700' : 'bg-transparent'"
              style="-webkit-tap-highlight-color: transparent;"
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
              class="p-1.5 rounded-full text-white hover:bg-green-700 focus:outline-none focus:ring-0 active:bg-green-900 transition-colors"
              :class="showMobileMenu ? 'bg-green-900' : 'bg-transparent'"
              style="-webkit-tap-highlight-color: transparent;"
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
        class="fixed top-[60px] inset-x-0 z-30 bg-green-800 shadow-lg rounded-b-3xl mx-2"
      >
        <div class="px-2 py-2">
          <nav class="space-y-1.5">
            <router-link
              to="/"
              @click="closeMobileMenu"
              class="flex items-center pl-2 pr-3 py-1.5 rounded-md text-sm font-medium text-white hover:bg-green-700 transition-colors"
              :class="{ 'bg-green-600': route.name === 'Home' }"
            >
              <svg class="h-4 w-4 mr-2.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
              </svg>
              <span>Inicio</span>
            </router-link>

            <router-link
              to="/historial"
              @click="closeMobileMenu"
              class="flex items-center pl-2 pr-3 py-1.5 rounded-md text-sm font-medium text-white hover:bg-green-700 transition-colors"
              :class="{ 'bg-green-600': route.name === 'Historial' }"
            >
              <svg class="h-4 w-4 mr-2.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
              </svg>
              <span>Historial</span>
            </router-link>

            <router-link
              to="/notificaciones"
              @click="closeMobileMenu"
              class="flex items-center pl-2 pr-3 py-1.5 rounded-md text-sm font-medium text-white hover:bg-green-700 transition-colors relative"
              :class="{ 'bg-green-600': route.name === 'Notificaciones' }"
            >
              <svg class="h-4 w-4 mr-2.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
              </svg>
              <span>Notificaciones</span>
              <span v-if="unreadCount > 0" class="ml-auto h-4 w-4 bg-red-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center flex-shrink-0">
                {{ unreadCount > 9 ? '9+' : unreadCount }}
              </span>
            </router-link>

            <router-link
              to="/profile"
              @click="closeMobileMenu"
              class="flex items-center pl-2 pr-3 py-1.5 rounded-md text-sm font-medium text-white hover:bg-green-700 transition-colors"
              :class="{ 'bg-green-600': route.name === 'Profile' }"
            >
              <svg class="h-4 w-4 mr-2.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
              </svg>
              <span>Mi Perfil</span>
            </router-link>

            <router-link
              to="/support"
              @click="closeMobileMenu"
              class="flex items-center pl-2 pr-3 py-1.5 rounded-md text-sm font-medium text-white hover:bg-green-700 transition-colors"
              :class="{ 'bg-green-600': route.name === 'Support' }"
            >
              <svg class="h-4 w-4 mr-2.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.829V11a1 1 0 11-2 0v-.171a3.001 3.001 0 01-1.402-5.618 1 1 0 111.73-1A1 1 0 0010 7a1 1 0 001 1h.01a1 1 0 100-2H11a1 1 0 00-1-1zm0 8a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
              </svg>
              <span>Soporte</span>
            </router-link>

            <router-link
              to="/reportes"
              @click="closeMobileMenu"
              class="flex items-center pl-2 pr-3 py-1.5 rounded-md text-sm font-medium text-white hover:bg-green-700 transition-colors"
              :class="{ 'bg-green-600': route.name === 'Reportes' }"
            >
              <svg class="h-4 w-4 mr-2.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
              </svg>
              <span>Reportes</span>
            </router-link>

            <router-link
              to="/settings"
              @click="closeMobileMenu"
              class="flex items-center pl-2 pr-3 py-1.5 rounded-md text-sm font-medium text-white hover:bg-green-700 transition-colors"
              :class="{ 'bg-green-600': route.name === 'Settings' }"
            >
              <svg class="h-4 w-4 mr-2.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd" />
              </svg>
              <span>Configuración</span>
            </router-link>

            <div class="border-t border-green-600 pt-2 mt-2">
              <button
                @click="logout"
                class="flex items-center w-full pl-2 pr-3 py-1.5 rounded-md text-sm font-medium text-red-300 hover:bg-red-900/30 hover:text-red-200 transition-colors focus:outline-none focus:ring-0 active:bg-red-900/30"
                style="-webkit-tap-highlight-color: transparent;"
              >
                <svg class="h-4 w-4 mr-2.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                  <path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd" />
                </svg>
                <span>Cerrar Sesión</span>
              </button>
            </div>
          </nav>
        </div>
      </div>
    </transition>

    <!-- Overlay para cerrar el menú con efecto de difuminado -->
    <div 
      v-if="isLoggedIn && showMobileMenu"
      @click="closeMobileMenu"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm z-20 transition-all duration-300"
    ></div>

    <!-- Contenido principal -->
    <main class="main-content relative z-10" :style="{ paddingTop: isLoggedIn ? '120px' : '0' }">
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

/* Optimización del scroll - solo cuando sea necesario */
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  width: 100%;
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
  background: linear-gradient(to bottom right, #d1fae5, #a7f3d0, #6ee7b7);
}

/* ====== FULLSCREEN Y SAFE AREAS ====== */

/* Fondo que abarca toda la pantalla incluyendo áreas del sistema */
.fullscreen-bg {
  min-height: 100vh;
  min-height: -webkit-fill-available;
  min-height: 100dvh; /* Dynamic viewport height */
  width: 100vw;
  width: 100dvw;
  position: relative;
}

.fullscreen-layer {
  top: calc(-1 * env(safe-area-inset-top));
  bottom: calc(-1 * env(safe-area-inset-bottom));
  left: calc(-1 * env(safe-area-inset-left));
  right: calc(-1 * env(safe-area-inset-right));
  position: fixed;
}

/* Asegurar que el fondo cubra toda la pantalla */
html {
  height: -webkit-fill-available;
}

body {
  min-height: 100vh;
  min-height: -webkit-fill-available;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  overflow-y: auto;
}

/* ====== LIQUID GLASS BACKGROUND ====== */

/* Fondo principal liquid glass */
.liquid-glass-bg {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 35%, #6ee7b7 70%, #34d399 100%);
  background-size: 400% 400%;
  animation: liquid-gradient 20s ease infinite;
}

@keyframes liquid-gradient {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

/* Animaciones de burbujas flotantes grandes */
@keyframes bubble-float-1 {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.3;
  }
  33% {
    transform: translate(40px, -60px) scale(1.15);
    opacity: 0.4;
  }
  66% {
    transform: translate(-30px, 40px) scale(0.95);
    opacity: 0.25;
  }
}

@keyframes bubble-float-2 {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.25;
  }
  33% {
    transform: translate(-50px, 50px) scale(1.1);
    opacity: 0.35;
  }
  66% {
    transform: translate(25px, -35px) scale(0.9);
    opacity: 0.2;
  }
}

@keyframes bubble-float-3 {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.3;
  }
  33% {
    transform: translate(60px, 30px) scale(1.2);
    opacity: 0.4;
  }
  66% {
    transform: translate(-40px, -50px) scale(0.85);
    opacity: 0.25;
  }
}

@keyframes bubble-float-4 {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.25;
  }
  33% {
    transform: translate(-35px, -45px) scale(1.1);
    opacity: 0.35;
  }
  66% {
    transform: translate(45px, 55px) scale(0.95);
    opacity: 0.2;
  }
}

@keyframes bubble-float-5 {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.2;
  }
  33% {
    transform: translate(50px, -40px) scale(1.15);
    opacity: 0.3;
  }
  66% {
    transform: translate(-55px, 35px) scale(0.9);
    opacity: 0.15;
  }
}

/* Burbujas que suben */
@keyframes bubble-rise-1 {
  0% {
    transform: translateY(0) translateX(0) scale(1);
    opacity: 0.4;
  }
  50% {
    transform: translateY(-100px) translateX(20px) scale(1.1);
    opacity: 0.5;
  }
  100% {
    transform: translateY(-200px) translateX(-10px) scale(0.9);
    opacity: 0.3;
  }
}

@keyframes bubble-rise-2 {
  0% {
    transform: translateY(0) translateX(0) scale(1);
    opacity: 0.35;
  }
  50% {
    transform: translateY(-120px) translateX(-25px) scale(1.15);
    opacity: 0.45;
  }
  100% {
    transform: translateY(-240px) translateX(15px) scale(0.85);
    opacity: 0.25;
  }
}

@keyframes bubble-rise-3 {
  0% {
    transform: translateY(0) translateX(0) scale(1);
    opacity: 0.4;
  }
  50% {
    transform: translateY(-90px) translateX(30px) scale(1.2);
    opacity: 0.5;
  }
  100% {
    transform: translateY(-180px) translateX(-20px) scale(0.9);
    opacity: 0.3;
  }
}

/* Shimmer suave */
@keyframes shimmer-slow {
  0%, 100% {
    opacity: 0.5;
  }
  50% {
    opacity: 0.7;
  }
}

/* Pulso gentil */
@keyframes pulse-gentle {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.5;
  }
}

/* Aplicar animaciones */
.animate-bubble-float-1 {
  animation: bubble-float-1 12s ease-in-out infinite;
}

.animate-bubble-float-2 {
  animation: bubble-float-2 15s ease-in-out infinite;
}

.animate-bubble-float-3 {
  animation: bubble-float-3 13s ease-in-out infinite;
}

.animate-bubble-float-4 {
  animation: bubble-float-4 11s ease-in-out infinite;
}

.animate-bubble-float-5 {
  animation: bubble-float-5 14s ease-in-out infinite;
}

.animate-bubble-rise-1 {
  animation: bubble-rise-1 20s ease-in-out infinite;
}

.animate-bubble-rise-2 {
  animation: bubble-rise-2 18s ease-in-out infinite;
}

.animate-bubble-rise-3 {
  animation: bubble-rise-3 22s ease-in-out infinite;
}

.animate-shimmer-slow {
  animation: shimmer-slow 8s ease-in-out infinite;
}

.animate-pulse-gentle {
  animation: pulse-gentle 6s ease-in-out infinite;
}

/* Animación para elementos decorativos */
@keyframes pulse-slow {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.05);
  }
}

.animate-pulse-slow {
  animation: pulse-slow 4s ease-in-out infinite;
}

/* Animación de brillo para el título Sembrando Vida con efecto rayado verde-blanco */
.sembrando-vida-shine {
  font-weight: 600;
  letter-spacing: 0.02em;
}

.sembrando-vida-shine span {
  display: inline-block;
  background: repeating-linear-gradient(
    45deg,
    #ffffff,
    #ffffff 2px,
    #a7f3d0 2px,
    #a7f3d0 4px
  );
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: letter-shine-header 3s ease-in-out infinite;
  animation-delay: calc(var(--char-index) * 0.15s);
}

.sembrando-vida-shine .space-char {
  min-width: 0.3em;
  background: none;
  -webkit-text-fill-color: transparent;
}

@keyframes letter-shine-header {
  0%, 100% {
    filter: brightness(1) drop-shadow(0 0 1px rgba(255, 255, 255, 0.3));
    transform: scale(1);
  }
  15% {
    filter: brightness(1.8) drop-shadow(0 0 4px rgba(255, 255, 255, 0.9)) drop-shadow(0 0 8px rgba(16, 185, 129, 0.6));
    transform: scale(1.05);
  }
  30% {
    filter: brightness(1) drop-shadow(0 0 1px rgba(255, 255, 255, 0.3));
    transform: scale(1);
  }
}
</style>