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
        <!-- Logo animado con efecto de partículas -->
        <div class="logo-animation">
          <svg class="logo-svg" viewBox="0 0 120 120" fill="none">
            <!-- Círculo de fondo con brillo -->
            <circle cx="60" cy="60" r="50" fill="url(#circle-gradient)" opacity="0.8">
              <animate attributeName="opacity" values="0.8;0.6;0.8" dur="3s" repeatCount="indefinite" />
            </circle>
            
            <!-- Forma de hoja principal -->
            <path d="M60 20C40 20 25 40 25 60C25 80 40 100 60 100C80 100 95 80 95 60C95 40 80 20 60 20Z" fill="url(#leaf-gradient)" opacity="0.9">
              <animate attributeName="d" 
                values="
                  M60 20C40 20 25 40 25 60C25 80 40 100 60 100C80 100 95 80 95 60C95 40 80 20 60 20Z;
                  M60 20C42 23 27 42 27 62C27 82 42 97 62 97C82 97 93 82 93 62C93 42 78 17 60 20Z;
                  M60 20C40 20 25 40 25 60C25 80 40 100 60 100C80 100 95 80 95 60C95 40 80 20 60 20Z" 
                dur="8s" repeatCount="indefinite" />
            </path>
            
            <!-- Vena central de la hoja -->
            <path d="M60 20C60 20 60 60 60 100" stroke="url(#vein-gradient)" stroke-width="2" opacity="0.7">
              <animate attributeName="d" 
                values="
                  M60 20C60 20 60 60 60 100;
                  M60 20C62 40 58 80 60 100;
                  M60 20C60 20 60 60 60 100" 
                dur="5s" repeatCount="indefinite" />
            </path>
            
            <!-- Venas laterales -->
            <path d="M60 40C70 50 80 50 90 50" stroke="url(#vein-gradient)" stroke-width="1.5" opacity="0.6">
              <animate attributeName="d" 
                values="
                  M60 40C70 50 80 50 90 50;
                  M60 40C70 48 82 47 90 48;
                  M60 40C70 50 80 50 90 50" 
                dur="4.5s" repeatCount="indefinite" />
            </path>
            <path d="M60 40C50 50 40 50 30 50" stroke="url(#vein-gradient)" stroke-width="1.5" opacity="0.6">
              <animate attributeName="d" 
                values="
                  M60 40C50 50 40 50 30 50;
                  M60 40C50 48 38 47 30 48;
                  M60 40C50 50 40 50 30 50" 
                dur="4.8s" repeatCount="indefinite" />
            </path>
            <path d="M60 60C70 70 80 70 90 70" stroke="url(#vein-gradient)" stroke-width="1.5" opacity="0.6">
              <animate attributeName="d" 
                values="
                  M60 60C70 70 80 70 90 70;
                  M60 60C70 68 82 67 90 68;
                  M60 60C70 70 80 70 90 70" 
                dur="5.2s" repeatCount="indefinite" />
            </path>
            <path d="M60 60C50 70 40 70 30 70" stroke="url(#vein-gradient)" stroke-width="1.5" opacity="0.6">
              <animate attributeName="d" 
                values="
                  M60 60C50 70 40 70 30 70;
                  M60 60C50 68 38 67 30 68;
                  M60 60C50 70 40 70 30 70" 
                dur="4.9s" repeatCount="indefinite" />
            </path>
            <path d="M60 80C70 90 80 85 85 85" stroke="url(#vein-gradient)" stroke-width="1.5" opacity="0.6">
              <animate attributeName="d" 
                values="
                  M60 80C70 90 80 85 85 85;
                  M60 80C70 88 80 82 85 82;
                  M60 80C70 90 80 85 85 85" 
                dur="4.2s" repeatCount="indefinite" />
            </path>
            <path d="M60 80C50 90 40 85 35 85" stroke="url(#vein-gradient)" stroke-width="1.5" opacity="0.6">
              <animate attributeName="d" 
                values="
                  M60 80C50 90 40 85 35 85;
                  M60 80C50 88 40 82 35 82;
                  M60 80C50 90 40 85 35 85" 
                dur="4.4s" repeatCount="indefinite" />
            </path>

            <!-- Partículas flotantes animadas -->
            <circle cx="65" cy="45" r="1.5" fill="#E8F5E9" opacity="0.8">
              <animate attributeName="cy" values="45;40;45" dur="3s" repeatCount="indefinite" />
              <animate attributeName="opacity" values="0.8;0.4;0.8" dur="3s" repeatCount="indefinite" />
            </circle>
            <circle cx="55" cy="65" r="1.2" fill="#E8F5E9" opacity="0.7">
              <animate attributeName="cy" values="65;60;65" dur="2.5s" repeatCount="indefinite" />
              <animate attributeName="opacity" values="0.7;0.3;0.7" dur="2.5s" repeatCount="indefinite" />
            </circle>
            <circle cx="75" cy="55" r="1" fill="#E8F5E9" opacity="0.6">
              <animate attributeName="cy" values="55;52;55" dur="4s" repeatCount="indefinite" />
              <animate attributeName="opacity" values="0.6;0.2;0.6" dur="4s" repeatCount="indefinite" />
            </circle>
            
            <!-- Definición de gradientes -->
            <defs>
              <radialGradient id="circle-gradient" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#E8F5E9" stop-opacity="0.4" />
                <stop offset="100%" stop-color="#2E7D32" stop-opacity="0.05" />
              </radialGradient>
              
              <linearGradient id="leaf-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#43A047" stop-opacity="0.9" />
                <stop offset="50%" stop-color="#2E7D32" stop-opacity="0.85" />
                <stop offset="100%" stop-color="#1B5E20" stop-opacity="0.8" />
              </linearGradient>
              
              <linearGradient id="vein-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#81C784" stop-opacity="0.9" />
                <stop offset="100%" stop-color="#C8E6C9" stop-opacity="0.7" />
              </linearGradient>
            </defs>
          </svg>
          
          <!-- Efecto de destello -->
          <div class="logo-shine"></div>
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
  --accent: #81C784;
  --accent-light: #A5D6A7;
  --accent-very-light: #C8E6C9;
  --background: #FFFFFF;
  --surface: #F5F5F5;
  --surface-hover: #EEEEEE;
  --text-primary: #212121;
  --text-secondary: #757575;
  --text-light: #FFFFFF;
  --border-light: rgba(255, 255, 255, 0.2);
  --border-dark: rgba(0, 0, 0, 0.1);
  --shadow-color: rgba(0, 0, 0, 0.15);
  --error: #D32F2F;
  --warning: #FFA000;
  --info: #1976D2;
  --success: #388E3C;
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
    var(--primary-dark) 0%, 
    var(--primary) 100%);
  color: var(--text-light);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  box-shadow: 4px 0 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow-y: auto;
  overflow-x: hidden;
  border-radius: 0 12px 12px 0;
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
  padding: 16px 16px 12px;
  position: relative;
}

.logo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.logo-animation {
  width: 45px;
  height: 45px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.2));
  transition: transform 0.3s ease;
}

.logo-svg:hover {
  transform: scale(1.05);
}

.logo-shine {
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(
    circle at 30% 30%,
    rgba(255, 255, 255, 0.3) 0%,
    transparent 70%
  );
  border-radius: 50%;
  animation: shineEffect 8s infinite linear;
}

@keyframes shineEffect {
  0%, 100% {
    opacity: 0.6;
    transform: scale(0.8) rotate(0deg);
  }
  25% {
    opacity: 0.8;
    transform: scale(0.9) rotate(90deg);
  }
  50% {
    opacity: 0.6;
    transform: scale(0.8) rotate(180deg);
  }
  75% {
    opacity: 0.8;
    transform: scale(0.9) rotate(270deg);
  }
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
  font-size: 14px;
  font-weight: 700;
  color: var(--text-light);
  letter-spacing: 0.4px;
  margin: 0;
  text-transform: uppercase;
  background: linear-gradient(45deg, #FFFFFF 30%, #C8E6C9 70%);
  -webkit-background-clip: text;
  color: transparent;
  background-clip: text;
  animation: gradientText 3s ease infinite;
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
  font-size: 10px;
  font-weight: 300;
  color: var(--accent-very-light);
  opacity: 0.8;
  margin: 2px 0 0;
}

.text-underline {
  width: 70%;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent, 
    var(--accent-light),
    transparent);
  margin-top: 8px;
  border-radius: 2px;
  position: relative;
  overflow: hidden;
}

.text-underline::after {
  content: "";
  position: absolute;
  width: 50%;
  height: 100%;
  background: rgba(255, 255, 255, 0.4);
  left: -100%;
  top: 0;
  animation: underlineShine 3s infinite ease-in-out;
}

@keyframes underlineShine {
  0% {
    left: -100%;
  }
  50%, 100% {
    left: 100%;
  }
}

/* Links rápidos */
.quick-links {
  display: flex;
  justify-content: space-around;
  padding: 12px 8px;
  margin: 0 10px 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  position: relative;
}

.quick-links::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 10px;
  z-index: -1;
}

.quick-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: var(--text-light);
  gap: 6px;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
  flex: 1;
  position: relative;
  overflow: hidden;
}

.quick-link::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0);
  transition: all 0.3s ease;
  top: 0;
  left: 0;
  border-radius: 10px;
  z-index: 0;
}

.quick-link:hover::before {
  background: rgba(255, 255, 255, 0.1);
}

.quick-link.geoportal {
  color: #81D4FA;
}

.quick-link.app-movil {
  color: #FFD54F;
}

.link-icon-container {
  width: 28px;
  height: 28px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
}

.quick-link:hover .link-icon-container {
  transform: translateY(-3px);
}

.quick-link.geoportal .link-icon-container {
  box-shadow: 0 0 12px rgba(129, 212, 250, 0.3);
}

.quick-link.app-movil .link-icon-container {
  box-shadow: 0 0 12px rgba(255, 213, 79, 0.3);
}

.link-icon {
  width: 14px;
  height: 14px;
  stroke-width: 2;
}

.quick-link span {
  font-size: 10px;
  font-weight: 500;
  position: relative;
  z-index: 1;
}

.quick-link:active .link-icon-container {
  transform: scale(0.95);
}

/* Navegación */
.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 8px 10px 16px;
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
  margin-bottom: 6px;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  text-decoration: none;
  color: var(--text-light);
  border-radius: 10px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.nav-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0);
  transition: all 0.3s ease;
  z-index: 0;
}

.nav-link:hover::before {
  background: rgba(255, 255, 255, 0.08);
}

.nav-icon-container {
  width: 30px;
  height: 30px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
}

.nav-icon {
  width: 16px;
  height: 16px;
  stroke-width: 2;
  transition: all 0.3s ease;
}

.nav-text {
  font-size: 12px;
  font-weight: 500;
  position: relative;
  z-index: 1;
  flex: 1;
}

.nav-indicator {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%) scaleY(0);
  width: 4px;
  height: 60%;
  background: var(--accent-light);
  border-radius: 0 4px 4px 0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0;
}

/* Estado activo para items de navegación */
.nav-item.active .nav-link::before {
  background: rgba(255, 255, 255, 0.12);
}

.nav-item.active .nav-icon-container {
  background: var(--accent);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
  transform: translateY(-2px);
}

.nav-item.active .nav-icon {
  color: #FFF;
}

.nav-item.active .nav-indicator {
  opacity: 1;
  transform: translateY(-50%) scaleY(1);
}

/* Hover effects */
.nav-link:hover .nav-icon-container {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.15);
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
  padding: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px;
  background: rgba(255, 255, 255, 0.07);
  border-radius: 8px;
}

.user-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--primary-light);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-icon {
  width: 16px;
  height: 16px;
  color: var(--text-light);
}

.user-details {
  flex: 1;
  overflow: hidden;
}

.user-name {
  margin: 0;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-light);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  margin: 0;
  font-size: 10px;
  color: var(--accent-very-light);
  opacity: 0.8;
}

.logout-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, 
    rgba(255, 87, 34, 0.8) 0%,
    rgba(244, 67, 54, 0.8) 100%);
  color: white;
  font-family: 'Poppins', sans-serif;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 3px 10px rgba(244, 67, 54, 0.3);
}

.logout-button:hover {
  background: linear-gradient(135deg,
    rgba(255, 87, 34, 0.9) 0%,
    rgba(244, 67, 54, 0.9) 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(244, 67, 54, 0.4);
}

.logout-button:active {
  transform: translateY(0);
  box-shadow: 0 3px 8px rgba(244, 67, 54, 0.3);
}

.logout-icon {
  width: 18px;
  height: 18px;
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
    border-radius: 0;
  }
}
</style>
