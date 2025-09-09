<template>
  <div :class="['sidebar', { 'collapsed': isCollapsed }]">
    <!-- Botón de toggle para el sidebar en móviles -->
    <button class="sidebar-toggle" @click="toggleSidebar">
      <svg class="toggle-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
      </svg>
    </button>

    <!-- Cabecera del sidebar con logo animado -->
    <div class="sidebar-header">
      <div class="logo-container">
        <!-- Flor con pétalos largos y detallados -->
        <div class="logo-animation">
          <div class="detailed-flower">
            <div class="petal petal-1"></div>
            <div class="petal petal-2"></div>
            <div class="petal petal-3"></div>
            <div class="petal petal-4"></div>
            <div class="petal petal-5"></div>
            <div class="petal petal-6"></div>
            <div class="petal petal-7"></div>
            <div class="petal petal-8"></div>
            <div class="flower-center">
              <div class="center-core"></div>
              <div class="center-highlight"></div>
            </div>
          </div>
        </div>
        
        <!-- Texto del logo con efecto de brillo -->
        <div class="logo-text">
          <h1 class="brand-name">SEMBRANDO VIDA</h1>
          <p class="brand-tagline">App de Seguimiento</p>
          <div class="text-underline"></div>
        </div>
      </div>
    </div>

    <!-- Enlaces rápidos: Geoportal y App Móvil -->
    <div class="quick-links">
      <a href="https://geoportal.sembrandodatos.com/" target="_blank" class="quick-link geoportal">
        <div class="link-icon-container">
          <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <path d="M2 12h20"/>
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
          </svg>
        </div>
        <span>Geoportal</span>
      </a>
      <a href="https://app.sembrandodatos.com/login" target="_blank" class="quick-link app-movil">
        <div class="link-icon-container">
          <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="5" y="2" width="14" height="20" rx="2" ry="2"/>
            <line x1="12" y1="18" x2="12.01" y2="18"/>
          </svg>
        </div>
        <span>App Móvil</span>
      </a>
      
      <!-- Resumen Ejecutivo -->
      <a href="https://dashboard.sembrandodatos.com/public/dashboard/a3a689e6-e359-4a29-a87f-6b5afb589163?fecha=2025-09-05" target="_blank" class="quick-link resumen-ejecutivo">
        <div class="link-icon-container">
          <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
            <path d="M9 9h6v6H9z"/>
            <path d="M9 3v6"/>
            <path d="M21 9h-6"/>
            <path d="M9 15v6"/>
            <path d="M15 15h6"/>
          </svg>
        </div>
        <span>Resumen Ejecutivo</span>
      </a>
    </div>

    <!-- Navegación principal -->
    <nav class="sidebar-nav">
      <ul>
        <!-- Visor de seguimiento -->
        <li class="nav-item" :class="{ active: $route.name === 'VisorMap' }">
          <router-link to="/visor-map" class="nav-link">
            <div class="nav-icon-container">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <circle cx="12" cy="12" r="4"/>
                <line x1="21.17" y1="8" x2="12" y2="8"/>
                <line x1="3.95" y1="6.06" x2="8.54" y2="14"/>
                <line x1="10.88" y1="21.94" x2="15.46" y2="14"/>
              </svg>
            </div>
            <span class="nav-text">Visor de Seguimiento</span>
          </router-link>
          <div class="nav-indicator"></div>
        </li>

        <!-- Asistencia -->
        <li class="nav-item" :class="{ active: $route.name === 'Asistencia' }">
          <router-link to="/asistencia" class="nav-link">
            <div class="nav-icon-container">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22 4 12 14.01 9 11.01"/>
              </svg>
            </div>
            <span class="nav-text">Asistencia</span>
          </router-link>
          <div class="nav-indicator"></div>
        </li>

        <!-- Registro de Actividades -->
        <li class="nav-item" :class="{ active: $route.name === 'Registros' }">
          <router-link to="/registros" class="nav-link">
            <div class="nav-icon-container">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10 9 9 9 8 9"/>
              </svg>
            </div>
            <span class="nav-text">Registro de Actividades</span>
          </router-link>
          <div class="nav-indicator"></div>
        </li>

        <!-- Usuarios (solo para admin) -->
        <li class="nav-item" :class="{ active: $route.name === 'Usuarios' }" v-if="isAdmin">
          <router-link to="/usuarios" class="nav-link">
            <div class="nav-icon-container">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </div>
            <span class="nav-text">Usuarios</span>
          </router-link>
          <div class="nav-indicator"></div>
        </li>

        <!-- Historiales -->
        <li class="nav-item" :class="{ active: $route.name === 'Historiales' }">
          <router-link to="/historiales" class="nav-link">
            <div class="nav-icon-container">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
            </div>
            <span class="nav-text">Historiales</span>
          </router-link>
          <div class="nav-indicator"></div>
        </li>

        <!-- Notificaciones -->
        <li class="nav-item" :class="{ active: $route.name === 'Notificaciones' }">
          <router-link to="/notificaciones" class="nav-link">
            <div class="nav-icon-container">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
              </svg>
              <span class="notification-badge" v-if="unreadNotifications">{{ unreadNotifications }}</span>
            </div>
            <span class="nav-text">Notificaciones</span>
          </router-link>
          <div class="nav-indicator"></div>
        </li>

        <!-- Permisos de Usuarios (solo para admin) -->
        <li class="nav-item" :class="{ active: $route.name === 'Permisos' }" v-if="isAdmin">
          <router-link to="/permisos" class="nav-link">
            <div class="nav-icon-container">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
            </div>
            <span class="nav-text">Permisos de Usuarios</span>
          </router-link>
          <div class="nav-indicator"></div>
        </li>

        <!-- Configuración (solo para admin) -->
        <li class="nav-item" :class="{ active: $route.name === 'Configuracion' }" v-if="isAdmin">
          <router-link to="/configuracion" class="nav-link">
            <div class="nav-icon-container">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"/>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
              </svg>
            </div>
            <span class="nav-text">Configuración</span>
          </router-link>
          <div class="nav-indicator"></div>
        </li>
      </ul>
    </nav>

    <!-- Información del usuario y cerrar sesión -->
    <div class="sidebar-footer">
      <div class="user-info">
        <div class="user-avatar">
          <svg class="user-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
        </div>
        <div class="user-details">
          <p class="user-name">{{ userDisplayName }}</p>
          <p class="user-role">{{ roleDisplayName }}</p>
        </div>
      </div>
      <button @click="showLogoutModal = true" class="logout-button">
        <svg class="logout-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
          <polyline points="16 17 21 12 16 7"/>
          <line x1="21" y1="12" x2="9" y2="12"/>
        </svg>
        <span>Cerrar Sesión</span>
      </button>
    </div>
    
    <!-- Modal de confirmación de cierre de sesión -->
    <Teleport to="body">
      <transition name="fade">
        <div v-if="showLogoutModal" class="modal-overlay" @click="closeModal">
          <div class="modal-container" @click.stop>
            <div class="modal-header">
              <div class="modal-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                  <polyline points="16 17 21 12 16 7"/>
                  <line x1="21" y1="12" x2="9" y2="12"/>
                </svg>
              </div>
              <h3>Cerrar Sesión</h3>
              <button @click="closeModal" class="modal-close">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
            <div class="modal-body">
              <p>¿Estás seguro de que deseas cerrar sesión?</p>
            </div>
            <div class="modal-footer">
              <button @click="closeModal" class="btn-cancel">Cancelar</button>
              <button @click="confirmLogout" class="btn-confirm">Confirmar</button>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import authService from '../services/authService'

// Router
const router = useRouter()

// Estados
const isCollapsed = ref(false)
const showLogoutModal = ref(false)
const currentUser = ref(null)
const unreadNotifications = ref(0)

// Computed properties
const isAdmin = computed(() => {
  return authService.isAdmin()
})

const userDisplayName = computed(() => {
  if (currentUser.value) {
    return currentUser.value.nombre || currentUser.value.username || 'Usuario'
  }
  return 'Usuario'
})

const roleDisplayName = computed(() => {
  const role = authService.getUserRole()
  return role === 'admin' ? 'Administrador' : 'Usuario'
})

// Métodos
const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}

const closeModal = () => {
  showLogoutModal.value = false
}

const confirmLogout = () => {
  showLogoutModal.value = false
  authService.logout()
  router.push('/login')
}

// Lifecycle hooks
onMounted(async () => {
  try {
    // Cargar información del usuario
    currentUser.value = authService.getCurrentUser()
    if (currentUser.value) {
      await authService.refreshUserInfo()
      currentUser.value = authService.getCurrentUser()
    }
    
    // Simular notificaciones no leídas (esto debería reemplazarse con datos reales)
    unreadNotifications.value = Math.floor(Math.random() * 10)
    
    // Agregar evento para tecla Escape para cerrar el modal
    window.addEventListener('keydown', handleKeydown)
  } catch (error) {
    console.error('Error cargando información del usuario:', error)
  }
})

// Manejadores de eventos
const handleKeydown = (event) => {
  if (event.key === 'Escape' && showLogoutModal.value) {
    closeModal()
  }
}
</script>

<style scoped>
/* Importación de fuentes */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Montserrat:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

/* Variables de colores */
:root {
  --primary-dark: #1B5E20;
  --primary: #2E7D32;
  --primary-light: #4CAF50;
  --accent: #FFFFFF;
  --accent-light: #E8F5E9;
  --accent-very-light: #F1F8E9;
  --background: #FFFFFF;
  --surface: #F5F5F5;
  --surface-hover: #EEEEEE;
  --text-primary: #212121;
  --text-secondary: #757575;
  --text-light: #FFFFFF;
  --text-highlight: #FFFF8D;
  --border-light: rgba(255, 255, 255, 0.3);
  --border-dark: rgba(0, 0, 0, 0.1);
  --shadow-color: rgba(0, 0, 0, 0.2);
  --error: #FF5252;
  --warning: #FFD740;
  --info: #40C4FF;
  --success: #69F0AE;
}

/* Base */
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: min(220px, 18vw);
  max-width: 240px;
  min-width: 200px;
  background: linear-gradient(135deg, 
    #388E3C 0%, 
    #2E7D32 50%, 
    #1B5E20 100%);
  color: var(--text-light);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  box-shadow: 4px 0 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow-y: auto;
  overflow-x: hidden;
  border-radius: 0;
  font-family: 'Poppins', 'Segoe UI', sans-serif;
}

/* Modo colapsado (para responsive) */
.sidebar.collapsed {
  width: 70px;
}

.sidebar.collapsed .logo-text,
.sidebar.collapsed .brand-tagline,
.sidebar.collapsed .quick-links span,
.sidebar.collapsed .nav-text,
.sidebar.collapsed .user-details,
.sidebar.collapsed .logout-button span {
  display: none;
}

.sidebar.collapsed .nav-icon-container,
.sidebar.collapsed .link-icon-container {
  margin: 0 auto;
}

/* Toggle Button para móviles */
.sidebar-toggle {
  position: absolute;
  top: 16px;
  right: -44px;
  width: 40px;
  height: 40px;
  background: var(--primary);
  border: none;
  border-radius: 50%;
  color: white;
  display: none;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  z-index: 10;
  transition: all 0.3s ease;
}

.sidebar-toggle:hover {
  background: var(--primary-dark);
  transform: scale(1.05);
}

.toggle-icon {
  width: 22px;
  height: 22px;
}

/* Header */
.sidebar-header {
  padding: 12px 12px 8px;
  position: relative;
}

.logo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.logo-animation {
  width: 42px;
  height: 42px;
  position: relative;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Contenedor de la flor detallada */
.detailed-flower {
  position: relative;
  width: 100%;
  height: 100%;
  animation: flowerRotate 18s linear infinite;
  filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.15));
}

/* Pétalos curvados y naturales - técnica basada en estudios botánicos */
.petal {
  position: absolute;
  width: 10px;
  height: 20px;
  top: 50%;
  left: 50%;
  transform-origin: center bottom;
  background: linear-gradient(
    to top,
    #1B5E20 0%,
    #2E7D32 25%,
    #4CAF50 45%,
    #66BB6A 65%,
    #A5D6A7 82%,
    rgba(255, 255, 255, 0.9) 95%,
    rgba(255, 255, 255, 0.95) 100%
  );
  /* Forma curvada natural que termina en punta */
  border-radius: 45% 55% 45% 55% / 85% 85% 15% 15%;
  /* Curvatura adicional usando clip-path sutil */
  clip-path: ellipse(50% 100% at 50% 100%);
  /* Sombras para curvatura natural */
  box-shadow: 
    inset 0.8px 0 2px rgba(255, 255, 255, 0.35),
    inset -0.3px 0 1.5px rgba(27, 94, 32, 0.2),
    0 0.5px 1.5px rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  /* Curvatura lateral sutil */
  transform-style: preserve-3d;
}

/* Efecto de curvatura lateral para naturalidad */
.petal::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    45deg,
    transparent 0%,
    rgba(255, 255, 255, 0.08) 30%,
    transparent 70%
  );
  border-radius: inherit;
  transform: skewX(-2deg);
}

/* Vena central muy sutil */
.petal::after {
  content: '';
  position: absolute;
  top: 20%;
  left: 50%;
  width: 0.3px;
  height: 60%;
  background: linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0.4) 0%,
    rgba(129, 199, 132, 0.25) 50%,
    transparent 100%
  );
  transform: translateX(-50%);
  border-radius: 0.3px;
  opacity: 0.6;
}

/* Posicionamiento preciso de cada pétalo */
.petal-1 {
  transform: translate(-50%, -100%) rotate(0deg);
}

.petal-2 {
  transform: translate(-50%, -100%) rotate(45deg);
}

.petal-3 {
  transform: translate(-50%, -100%) rotate(90deg);
}

.petal-4 {
  transform: translate(-50%, -100%) rotate(135deg);
}

.petal-5 {
  transform: translate(-50%, -100%) rotate(180deg);
}

.petal-6 {
  transform: translate(-50%, -100%) rotate(225deg);
}

.petal-7 {
  transform: translate(-50%, -100%) rotate(270deg);
}

.petal-8 {
  transform: translate(-50%, -100%) rotate(315deg);
}

/* Centro de la flor con múltiples capas - tamaño ajustado */
.flower-center {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 12px;
  height: 12px;
  transform: translate(-50%, -50%);
  z-index: 10;
}

/* Núcleo principal del centro */
.center-core {
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(
    circle at 30% 30%,
    #FFEB3B 0%,
    #FFC107 40%,
    #FF9800 70%,
    #1B5E20 100%
  );
  border-radius: 50%;
  box-shadow: 
    0 0 6px rgba(255, 235, 59, 0.4),
    inset 0 1px 3px rgba(255, 255, 255, 0.6),
    inset 0 -0.5px 1px rgba(27, 94, 32, 0.3);
  animation: centerPulse 4s ease-in-out infinite;
}

/* Punto de luz central */
.center-highlight {
  position: absolute;
  top: 25%;
  left: 25%;
  width: 50%;
  height: 50%;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.85) 0%,
    rgba(255, 235, 59, 0.6) 60%,
    transparent 100%
  );
  border-radius: 50%;
  animation: highlight 3s ease-in-out infinite alternate;
}

/* Animaciones */
@keyframes flowerRotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes centerPulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 
      0 0 8px rgba(255, 235, 59, 0.5),
      inset 0 2px 4px rgba(255, 255, 255, 0.6),
      inset 0 -1px 2px rgba(27, 94, 32, 0.3);
  }
  50% {
    transform: scale(1.1);
    box-shadow: 
      0 0 12px rgba(255, 235, 59, 0.7),
      inset 0 2px 4px rgba(255, 255, 255, 0.8),
      inset 0 -1px 2px rgba(27, 94, 32, 0.4);
  }
}

@keyframes highlight {
  0% {
    opacity: 0.6;
    transform: scale(0.8);
  }
  100% {
    opacity: 0.9;
    transform: scale(1.2);
  }
}

/* Efectos hover naturales */
.logo-animation:hover .detailed-flower {
  animation-duration: 12s;
  filter: drop-shadow(0 3px 8px rgba(0, 0, 0, 0.2));
}

.logo-animation:hover .petal {
  box-shadow: 
    inset 1.5px 0 4px rgba(255, 255, 255, 0.5),
    inset -0.5px 0 3px rgba(27, 94, 32, 0.25),
    0 2px 4px rgba(0, 0, 0, 0.12);
  background: linear-gradient(
    to top,
    #1B5E20 0%,
    #2E7D32 18%,
    #4CAF50 38%,
    #66BB6A 58%,
    #A5D6A7 78%,
    rgba(255, 255, 255, 0.97) 94%,
    rgba(255, 255, 255, 1) 100%
  );
  transform: scale(1.02);
}

.logo-animation:hover .center-core {
  animation-duration: 2.5s;
}

.logo-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  width: 100%;
}

.brand-name {
  font-family: 'Montserrat', sans-serif;
  font-size: 15px;
  font-weight: 800;
  color: var(--text-light);
  letter-spacing: 0.5px;
  margin: 0;
  text-transform: uppercase;
  background: linear-gradient(45deg, #F1F8E9 10%, #E8F5E8 30%, #DCEDC8 50%, #FFF9C4 70%, #FFEB3B 90%);
  -webkit-background-clip: text;
  color: transparent;
  background-clip: text;
  animation: gradientText 3s ease infinite;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  filter: drop-shadow(0 1px 3px rgba(0, 0, 0, 0.3));
}

@keyframes gradientText {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.brand-tagline {
  font-size: 11px;
  font-weight: 500;
  color: #FFFFFF;
  opacity: 0.95;
  margin: 4px 0 0;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.text-underline {
  width: 80%;
  height: 3px;
  background: linear-gradient(90deg, 
    transparent 0%,
    #1B5E20 25%,
    #2E7D32 50%,
    #1B5E20 75%,
    transparent 100%);
  margin: 8px auto 0 auto;
  border-radius: 2px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(27, 94, 32, 0.3);
}

.text-underline::after {
  content: "";
  position: absolute;
  width: 40%;
  height: 100%;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.3) 20%,
    rgba(255, 255, 255, 0.8) 50%,
    rgba(255, 255, 255, 0.3) 80%,
    transparent 100%);
  left: -50%;
  top: 0;
  animation: underlineShine 2.5s infinite ease-in-out;
  border-radius: 2px;
}

@keyframes underlineShine {
  0% {
    left: -50%;
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    left: 110%;
    opacity: 0;
  }
}

/* Links rápidos */
.quick-links {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
  padding: 8px 12px;
  margin: 0 10px 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  position: relative;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.quick-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: white;
  gap: 3px;
  padding: 4px;
  border-radius: 6px;
  transition: all 0.3s ease;
  width: 45%;
  max-width: 70px;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

/* Tercer botón ocupa toda la fila inferior */
.quick-link.resumen-ejecutivo {
  width: 100%;
  max-width: none;
  margin-top: 4px;
}

.quick-link:hover {
  transform: translateY(-2px);
}

.quick-link.geoportal {
  color: white;
  background: rgba(46, 125, 50, 0.8);
}

.quick-link.geoportal:hover {
  background: rgba(46, 125, 50, 0.9);
}

.quick-link.app-movil {
  color: white;
  background: linear-gradient(135deg, rgba(38, 166, 154, 0.7) 0%, rgba(33, 150, 243, 0.7) 100%);
}

.quick-link.app-movil:hover {
  background: linear-gradient(135deg, rgba(38, 166, 154, 0.8) 0%, rgba(33, 150, 243, 0.8) 100%);
}

.quick-link.resumen-ejecutivo {
  background: linear-gradient(135deg, rgba(156, 39, 176, 0.7) 0%, rgba(103, 58, 183, 0.7) 100%);
}

.quick-link.resumen-ejecutivo:hover {
  background: linear-gradient(135deg, rgba(156, 39, 176, 0.8) 0%, rgba(103, 58, 183, 0.8) 100%);
}

.link-icon-container {
  width: 22px;
  height: 22px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
  border: none;
}

.quick-link:hover .link-icon-container {
  transform: scale(1.1);
  background: rgba(255, 255, 255, 0.25);
}

.quick-link.geoportal .link-icon-container {
  background: rgba(255, 255, 255, 0.2);
}

.quick-link.app-movil .link-icon-container {
  background: rgba(255, 255, 255, 0.2);
}

.link-icon {
  width: 12px;
  height: 12px;
  stroke-width: 2;
  color: white;
  filter: drop-shadow(0 1px 1px rgba(0, 0, 0, 0.2));
}

.quick-link span {
  font-size: 8px;
  font-weight: 400;
  position: relative;
  z-index: 1;
  color: white;
  letter-spacing: 0.1px;
  white-space: nowrap;
}

.quick-link:active .link-icon-container {
  transform: scale(0.95);
}

/* Navegación */
.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 6px 10px 12px;
}

.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
}

.sidebar-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  position: relative;
  margin-bottom: 5px;
  overflow: hidden;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 8px 10px;
  text-decoration: none;
  color: var(--text-light);
  border-radius: 15px;
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  font-weight: 400;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.nav-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0);
  transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  z-index: 0;
  border-radius: 15px;
  backdrop-filter: blur(0px);
  transform: scale(0.95);
  opacity: 0;
}

.nav-link:hover::before {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  transform: scale(1);
  opacity: 1;
}

.nav-icon-container {
  width: 26px;
  height: 26px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
  position: relative;
  z-index: 1;
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-icon {
  width: 14px;
  height: 14px;
  stroke-width: 2;
  transition: all 0.3s ease;
  filter: drop-shadow(0 1px 1px rgba(0, 0, 0, 0.2));
  color: #FFFFFF;
}

.nav-text {
  font-size: 12px;
  font-weight: 400;
  position: relative;
  z-index: 1;
  flex: 1;
  letter-spacing: 0.3px;
  color: #FFFFFF;
}

.nav-indicator {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) scaleY(0);
  width: 4px;
  height: 70%;
  background: var(--text-highlight);
  border-radius: 0 4px 4px 0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0;
  box-shadow: 0 0 10px rgba(255, 255, 141, 0.6);
}

/* Estado activo para items de navegación - Liquid Glass Effect */
.nav-item.active .nav-link::before {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.4) 0%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0.3) 100%);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 15px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.4),
    inset 0 -1px 0 rgba(255, 255, 255, 0.1);
  transform: scale(1);
  opacity: 1;
}

.nav-item.active .nav-icon-container {
  background: linear-gradient(135deg,
    rgba(255, 255, 255, 0.5) 0%,
    rgba(255, 255, 255, 0.2) 50%,
    rgba(255, 255, 255, 0.4) 100%);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 
    0 8px 25px rgba(0, 0, 0, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.6),
    inset 0 -1px 0 rgba(255, 255, 255, 0.2);
  transform: translateY(-1px) scale(1.05);
  border-radius: 12px;
}

.nav-item.active .nav-text {
  font-weight: 400;
  color: #FFFFFF;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.nav-item.active .nav-icon {
  color: #FFFFFF;
  filter: drop-shadow(0 1px 3px rgba(0, 0, 0, 0.3));
}

.nav-item.active .nav-indicator {
  opacity: 1;
  transform: translateY(-50%) scaleY(1);
}

/* Liquid Glass Transition Effect */
.nav-item::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.2) 25%,
    rgba(255, 255, 255, 0.4) 50%,
    rgba(255, 255, 255, 0.2) 75%,
    transparent 100%);
  backdrop-filter: blur(10px);
  transition: left 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  border-radius: 15px;
  z-index: 2;
  pointer-events: none;
}

.nav-item.active::after {
  left: 100%;
}

/* Hover effects */
.nav-link:hover .nav-icon-container {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.25);
}

/* Notification badge */
.notification-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  min-width: 18px;
  height: 18px;
  background-color: var(--error);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: bold;
  z-index: 2;
  padding: 0 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

/* Footer */
.sidebar-footer {
  padding: 14px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: transparent;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  background: transparent;
  border-radius: 8px;
  border: none;
  box-shadow: none;
}

.user-avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: none;
  box-shadow: none;
}

.user-icon {
  width: 18px;
  height: 18px;
  color: rgba(255, 255, 255, 0.8);
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.user-details {
  flex: 1;
  overflow: hidden;
}

.user-name {
  margin: 0;
  font-size: 13px;
  font-weight: 400;
  color: #FFFFFF;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.user-role {
  margin: 0;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.7);
  opacity: 0.9;
  font-weight: 400;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
}

.logout-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 14px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  background: linear-gradient(135deg, 
    rgba(255, 87, 34, 0.9) 0%,
    rgba(244, 67, 54, 0.9) 100%);
  color: white;
  font-family: 'Poppins', sans-serif;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
  letter-spacing: 0.5px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  width: 100%;
}

.logout-button:hover {
  background: linear-gradient(135deg,
    rgba(255, 87, 34, 1) 0%,
    rgba(244, 67, 54, 1) 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
  border-color: rgba(255, 255, 255, 0.5);
}

.logout-button:active {
  transform: translateY(0);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
}

.logout-icon {
  width: 18px;
  height: 18px;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  backdrop-filter: blur(4px);
}

.modal-container {
  width: 100%;
  max-width: 340px;
  background-color: white;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  animation: modalAppear 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes modalAppear {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.modal-header {
  background-color: var(--primary);
  color: white;
  padding: 14px 16px;
  display: flex;
  align-items: center;
  position: relative;
}

.modal-icon {
  width: 30px;
  height: 30px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
}

.modal-icon svg {
  width: 16px;
  height: 16px;
}

.modal-header h3 {
  margin: 0;
  font-weight: 600;
  font-size: 16px;
}

.modal-close {
  position: absolute;
  right: 16px;
  top: 16px;
  background: transparent;
  border: none;
  color: white;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close svg {
  width: 20px;
  height: 20px;
}

.modal-body {
  padding: 18px 16px;
  color: var(--text-primary);
  font-size: 14px;
}

.modal-footer {
  padding: 12px 16px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  border-top: 1px solid var(--border-dark);
}

.btn-cancel,
.btn-confirm {
  padding: 8px 14px;
  border-radius: 6px;
  border: none;
  font-family: 'Poppins', sans-serif;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-cancel {
  background-color: var(--surface);
  color: var(--text-primary);
}

.btn-confirm {
  background-color: var(--error);
  color: white;
  box-shadow: 0 2px 8px rgba(244, 67, 54, 0.2);
}

.btn-cancel:hover {
  background-color: var(--surface-hover);
}

.btn-confirm:hover {
  background-color: #C62828;
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.3);
}

/* Transiciones */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive Design */
@media (max-width: 992px) {
  .sidebar {
    width: 230px;
    min-width: 220px;
  }
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    width: 230px;
    min-width: 220px;
  }
  
  .sidebar.collapsed {
    transform: translateX(0);
    width: 230px;
    min-width: 220px;
  }
  
  .sidebar-toggle {
    display: flex;
  }
  
  /* Mostrar textos aún colapsado en móvil */
  .sidebar.collapsed .logo-text,
  .sidebar.collapsed .brand-tagline,
  .sidebar.collapsed .quick-links span,
  .sidebar.collapsed .nav-text,
  .sidebar.collapsed .user-details,
  .sidebar.collapsed .logout-button span {
    display: block;
  }
  
  .sidebar.collapsed .nav-icon-container,
  .sidebar.collapsed .link-icon-container {
    margin: 0;
    margin-right: 12px;
  }
}

@media (max-width: 480px) {
  .sidebar,
  .sidebar.collapsed {
    width: 100%;
  }
}
</style>
