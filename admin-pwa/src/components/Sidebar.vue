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
        <!-- Flor SVG girando como en LoginView -->
        <div class="logo-animation">
          <svg class="logo-flower-svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="petalGradientSidebar" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#dcfce7;stop-opacity:1" />
                <stop offset="30%" style="stop-color:#bbf7d0;stop-opacity:1" />
                <stop offset="60%" style="stop-color:#86efac;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#4ade80;stop-opacity:1" />
              </linearGradient>
              <linearGradient id="centerGradientSidebar" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#22c55e;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#16a34a;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#15803d;stop-opacity:1" />
              </linearGradient>
              <filter id="petalGlowSidebar" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="1.5" result="coloredBlur"/>
                <feMerge> 
                  <feMergeNode in="coloredBlur"/>
                  <feMergeNode in="SourceGraphic"/>
                </feMerge>
              </filter>
              <filter id="centerShadowSidebar" x="-50%" y="-50%" width="200%" height="200%">
                <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#15803d" flood-opacity="0.4"/>
              </filter>
            </defs>
            
            <!-- Grupo de la flor que girará como una unidad -->
            <g class="flower-rotating-sidebar">
              <!-- Pétalos de la flor (8 pétalos) -->
              <!-- Pétalo superior -->
              <ellipse cx="50" cy="25" rx="8" ry="15" 
                       fill="url(#petalGradientSidebar)" filter="url(#petalGlowSidebar)"/>
              
              <!-- Pétalo superior derecho -->
              <ellipse cx="65" cy="35" rx="8" ry="15" 
                       fill="url(#petalGradientSidebar)" filter="url(#petalGlowSidebar)"
                       transform="rotate(45 65 35)"/>
              
              <!-- Pétalo derecho -->
              <ellipse cx="75" cy="50" rx="8" ry="15" 
                       fill="url(#petalGradientSidebar)" filter="url(#petalGlowSidebar)"
                       transform="rotate(90 75 50)"/>
              
              <!-- Pétalo inferior derecho -->
              <ellipse cx="65" cy="65" rx="8" ry="15" 
                       fill="url(#petalGradientSidebar)" filter="url(#petalGlowSidebar)"
                       transform="rotate(135 65 65)"/>
              
              <!-- Pétalo inferior -->
              <ellipse cx="50" cy="75" rx="8" ry="15" 
                       fill="url(#petalGradientSidebar)" filter="url(#petalGlowSidebar)"
                       transform="rotate(180 50 75)"/>
              
              <!-- Pétalo inferior izquierdo -->
              <ellipse cx="35" cy="65" rx="8" ry="15" 
                       fill="url(#petalGradientSidebar)" filter="url(#petalGlowSidebar)"
                       transform="rotate(225 35 65)"/>
              
              <!-- Pétalo izquierdo -->
              <ellipse cx="25" cy="50" rx="8" ry="15" 
                       fill="url(#petalGradientSidebar)" filter="url(#petalGlowSidebar)"
                       transform="rotate(270 25 50)"/>
              
              <!-- Pétalo superior izquierdo -->
              <ellipse cx="35" cy="35" rx="8" ry="15" 
                       fill="url(#petalGradientSidebar)" filter="url(#petalGlowSidebar)"
                       transform="rotate(315 35 35)"/>
              
              <!-- Centro de la flor -->
              <circle cx="50" cy="50" r="12" 
                      fill="url(#centerGradientSidebar)" filter="url(#centerShadowSidebar)"/>
              
              <!-- Detalles del centro -->
              <circle cx="50" cy="50" r="8" 
                      fill="#22c55e" opacity="0.8"/>
              <circle cx="47" cy="47" r="3" 
                      fill="#86efac" opacity="0.6"/>
              
              <!-- Pequeños detalles en los pétalos -->
              <circle cx="50" cy="30" r="1.5" fill="#22c55e" opacity="0.7"/>
              <circle cx="62" cy="38" r="1.5" fill="#22c55e" opacity="0.7"/>
              <circle cx="70" cy="50" r="1.5" fill="#22c55e" opacity="0.7"/>
              <circle cx="62" cy="62" r="1.5" fill="#22c55e" opacity="0.7"/>
              <circle cx="50" cy="70" r="1.5" fill="#22c55e" opacity="0.7"/>
              <circle cx="38" cy="62" r="1.5" fill="#22c55e" opacity="0.7"/>
              <circle cx="30" cy="50" r="1.5" fill="#22c55e" opacity="0.7"/>
              <circle cx="38" cy="38" r="1.5" fill="#22c55e" opacity="0.7"/>
            </g>
          </svg>
        </div>
        
        <!-- Texto del logo con efecto de brillo -->
        <div class="logo-text">
          <h1 class="brand-name">SEMBRANDO VIDA</h1>
          <p class="brand-tagline">App de Seguimiento</p>
          
          <!-- Información del usuario -->
          <div class="user-info" style="margin-top: 12px;">
            <div class="user-avatar">
              <span class="user-initials">{{ userInitials }}</span>
            </div>
            <div class="user-details">
              <p class="user-name">{{ userDisplayName }}</p>
              <!-- Solo mostrar rol si NO es 'user' (usuario normal) -->
              <p v-if="userRole !== 'user'" class="user-role">{{ roleDisplayName }}</p>
              <!-- Línea separadora verde antes del territorio -->
              <div v-if="isTerritorial && territorioAsignado" class="territorio-separator"></div>
              <!-- Territorio integrado debajo -->
              <div v-if="isTerritorial && territorioAsignado" class="user-territorio">
                <span class="user-territorio-text">{{ territorioAsignado }}</span>
              </div>
              <p v-if="isTerritorial && estadosDelTerritorio" class="user-estados">{{ estadosDelTerritorio }}</p>
            </div>
          </div>
          
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
      <a href="https://dashboard.sembrandodatos.com/public/dashboard/7b96d8b2-a786-4593-9765-3585c9212949" target="_blank" class="quick-link resumen-ejecutivo">
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
        <li class="nav-item" :class="{ active: $route.name === 'VisorMap' }" v-if="tienePermiso('visor')">
          <router-link to="/visor-map" class="nav-link">
            <div class="nav-icon-container">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <path d="M8 3h3a7 7 0 0 0 3 18h-3A17 17 0 0 1 8 3z"/>
                <path d="M16 12h3"/>
                <path d="M16 18h2"/>
                <path d="M16 6h2"/>
                <path d="M3 12h3"/>
                <path d="M6 6h2"/>
                <path d="M6 18h2"/>
              </svg>
            </div>
            <span class="nav-text">Visor de Seguimiento</span>
          </router-link>
          <div class="nav-indicator"></div>
        </li>

        <!-- Asistencia -->
        <li class="nav-item" :class="{ active: $route.name === 'Asistencia' }" v-if="tienePermiso('asistencia')">
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
        <li class="nav-item" :class="{ active: $route.name === 'Registros' }" v-if="tienePermiso('registros')">
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

        <!-- Usuarios -->
        <li class="nav-item" :class="{ active: $route.name === 'Usuarios' }" v-if="tienePermiso('usuarios')">
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
        <li class="nav-item" :class="{ active: $route.name === 'Historiales' }" v-if="tienePermiso('historiales')">
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
        <li class="nav-item" :class="{ active: $route.name === 'Notificaciones' }" v-if="tienePermiso('notificaciones')">
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

        <!-- Permisos Administrativos -->
        <li class="nav-item" :class="{ active: $route.name === 'Permisos' }" v-if="tienePermiso('permisos')">
          <router-link to="/permisos" class="nav-link">
            <div class="nav-icon-container">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
            </div>
            <span class="nav-text">Permisos Administrativos</span>
          </router-link>
          <div class="nav-indicator"></div>
        </li>

        <!-- Configuración -->
        <li class="nav-item" :class="{ active: $route.name === 'Configuracion' }" v-if="tienePermiso('configuracion')">
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

    <!-- Cerrar sesión -->
    <div class="sidebar-footer">
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
      <transition name="modal">
        <div v-if="showLogoutModal" class="logout-modal-overlay" @click="closeModal">
          <div class="logout-modal-container" @click.stop>
            
            <!-- Header con gradiente rojo -->
            <div class="logout-modal-header">
              <div class="logout-header-content">
                <div class="logout-icon-container">
                  <div class="logout-icon-bg">
                    <svg class="logout-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                      <polyline points="16 17 21 12 16 7"/>
                      <line x1="21" y1="12" x2="9" y2="12"/>
                    </svg>
                  </div>
                </div>
                <div class="logout-header-text">
                  <h3 class="logout-title">Cerrar Sesión</h3>
                  <p class="logout-subtitle">Finalizar tu sesión actual</p>
                </div>
              </div>
              
              <!-- Botón cerrar elegante -->
              <button @click="closeModal" class="logout-close-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>

            <!-- Cuerpo del modal con iconografía -->
            <div class="logout-modal-body">
              <div class="logout-warning-section">
                <div class="logout-warning-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                    <line x1="12" y1="9" x2="12" y2="13"/>
                    <line x1="12" y1="17" x2="12.01" y2="17"/>
                  </svg>
                </div>
                <div class="logout-warning-content">
                  <h4 class="logout-warning-title">¿Confirmar cierre de sesión?</h4>
                  <p class="logout-warning-text">
                    Se cerrará tu sesión actual y tendrás que iniciar sesión nuevamente para acceder al sistema.
                  </p>
                </div>
              </div>
              
              <!-- Información adicional -->
              <div class="logout-info-section">
                <div class="logout-info-item">
                  <svg class="logout-info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <polyline points="12 6 12 12 16 14"/>
                  </svg>
                  <span>Tu trabajo se ha guardado automáticamente</span>
                </div>
                <div class="logout-info-item">
                  <svg class="logout-info-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                  <span>La sesión se cerrará de forma segura</span>
                </div>
              </div>
            </div>

            <!-- Footer con botones mejorados -->
            <div class="logout-modal-footer">
              <button @click="closeModal" class="logout-btn logout-btn-cancel">
                <svg class="logout-btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M18 6L6 18M6 6l12 12"/>
                </svg>
                <span>Cancelar</span>
              </button>
              <button @click="confirmLogout" class="logout-btn logout-btn-confirm">
                <svg class="logout-btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                  <polyline points="16 17 21 12 16 7"/>
                  <line x1="21" y1="12" x2="9" y2="12"/>
                </svg>
                <span>Cerrar Sesión</span>
              </button>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import authService from '../services/authService'

// Router
const router = useRouter()

// Estados
const isCollapsed = ref(false)
const showLogoutModal = ref(false)
const currentUser = ref(null)
const unreadNotifications = ref(0)

// Permisos por defecto (todos en false, el usuario solo ve lo que se le asignó)
const permisosDefault = {
  visor: false,
  asistencia: false,
  registros: false,
  usuarios: false,
  historiales: false,
  notificaciones: false,
  permisos: false,
  configuracion: false
}

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

const userInitials = computed(() => {
  const name = userDisplayName.value
  return name ? name.charAt(0).toUpperCase() : 'U'
})

const roleDisplayName = computed(() => {
  const role = authService.getUserRole()
  return role === 'admin' ? 'Administrador' : 'Usuario'
})

// Computed para obtener el rol del usuario (para condicionales)
const userRole = computed(() => {
  return authService.getUserRole()
})

// Computed para verificar si es admin territorial
const isTerritorial = computed(() => {
  return authService.isTerritorial()
})

// Computed para obtener el nombre del territorio
const territorioAsignado = computed(() => {
  return authService.getTerritorio()
})

// Mapeo de territorios a estados de la república
const TERRITORIOS_ESTADOS = {
  'Acapulco - Centro - Norte - Tierra Caliente': ['Guerrero'],
  'Acayucan': ['Veracruz'],
  'Balancán': ['Tabasco'],
  'Chihuahua / Sonora': ['Chihuahua', 'Sonora'],
  'Colima': ['Colima'],
  'Comalcalco': ['Tabasco'],
  'Córdoba': ['Veracruz'],
  'Costa Chica - Montaña': ['Guerrero'],
  'Costa Grande - Sierra': ['Guerrero'],
  'Durango / Zacatecas': ['Durango', 'Zacatecas'],
  'Hidalgo': ['Hidalgo'],
  'Istmo': ['Oaxaca'],
  'Michoacán': ['Michoacán'],
  'Mixteca': ['Oaxaca'],
  'Morelos': ['Morelos'],
  'Nayarit / Jalisco': ['Nayarit', 'Jalisco'],
  'Ocosingo': ['Chiapas'],
  'Palenque': ['Chiapas'],
  'Papantla': ['Veracruz'],
  'Pichucalco': ['Chiapas'],
  'Puebla': ['Puebla'],
  'San Luis Potosí': ['San Luis Potosí'],
  'Sinaloa': ['Sinaloa'],
  'Tamaulipas': ['Tamaulipas'],
  'Tantoyuca': ['Veracruz'],
  'Tapachula': ['Chiapas'],
  'Teapa': ['Tabasco'],
  'Tlaxcala / Estado de México': ['Tlaxcala', 'Estado de México'],
  'Tzucacab / Opb': ['Quintana Roo'],
  'Xpujil': ['Campeche'],
  'Oficinas Centrales': ['Ciudad de México']
}

// Computed para obtener los estados del territorio
const estadosDelTerritorio = computed(() => {
  const territorio = territorioAsignado.value
  if (territorio && TERRITORIOS_ESTADOS[territorio]) {
    return TERRITORIOS_ESTADOS[territorio].join(', ')
  }
  return ''
})

// Función para verificar permisos
const tienePermiso = (permiso) => {
  // Si es admin, tiene todos los permisos por defecto
  if (isAdmin.value) {
    return true
  }
  
  // Verificar permisos del usuario
  const user = currentUser.value
  if (user && user.permisos) {
    return user.permisos[permiso] === true
  }
  
  // Si no hay permisos definidos, usar defaults
  return permisosDefault[permiso] || false
}

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

// Handler para actualización de usuario en tiempo real
const handleUserSessionUpdated = (event) => {
  console.log('🔄 Sidebar: Usuario actualizado en tiempo real', event.detail)
  currentUser.value = event.detail
  
  // Forzar re-render del sidebar
  const newUser = authService.getCurrentUser()
  if (newUser) {
    currentUser.value = { ...newUser }
  }
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
    
    // Escuchar actualizaciones de sesión en tiempo real
    window.addEventListener('user-session-updated', handleUserSessionUpdated)
  } catch (error) {
    console.error('Error cargando información del usuario:', error)
  }
})

// Cleanup al desmontar
onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  window.removeEventListener('user-session-updated', handleUserSessionUpdated)
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
  /* Asegurar que siempre esté visible */
  transform: translateX(0);
}

/* Modo colapsado (solo en desktop) */
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

/* Toggle Button para móviles - Oculto porque el sidebar siempre está visible */
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
  display: none; /* Siempre oculto */
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

/* SVG de la flor girando como en LoginView */
.logo-flower-svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.15));
}

/* Animaciones del logo de flor girando igual que en LoginView */
.flower-rotating-sidebar {
  animation: smoothRotationSidebar 6s linear infinite;
  transform-origin: 50px 50px;
}

@keyframes smoothRotationSidebar {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Efectos hover para la nueva animación SVG */
.logo-animation:hover .logo-flower-svg {
  filter: drop-shadow(0 3px 8px rgba(0, 0, 0, 0.2));
}

.logo-animation:hover .flower-rotating-sidebar {
  animation-duration: 4s;
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
  background: linear-gradient(135deg, #e8ffd4 0%, #d4ff9a 15%, #c6f76c 30%, #fff8b8 50%, #ffe566 70%, #ffdd44 85%, #ffd700 100%);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  color: transparent;
  background-clip: text;
  animation: gradientTextBright 4s ease infinite;
}

@keyframes gradientTextBright {
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
  width: 85%;
  height: 3px;
  background: linear-gradient(90deg, 
    transparent 0%,
    #10b981 15%,
    #22c55e 35%,
    #4ade80 50%,
    #22c55e 65%,
    #10b981 85%,
    transparent 100%);
  margin: 8px auto 0 auto;
  border-radius: 2px;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 0 8px rgba(16, 185, 129, 0.6),
    0 0 15px rgba(34, 197, 94, 0.4),
    0 0 25px rgba(74, 222, 128, 0.2);
}

/* Luz que recorre de lado a lado */
.text-underline::before {
  content: "";
  position: absolute;
  width: 35%;
  height: 150%;
  top: -25%;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(134, 239, 172, 0.3) 10%,
    rgba(187, 247, 208, 0.6) 30%,
    rgba(255, 255, 255, 1) 50%,
    rgba(187, 247, 208, 0.6) 70%,
    rgba(134, 239, 172, 0.3) 90%,
    transparent 100%);
  left: -35%;
  animation: shineSideToSide 3s infinite ease-in-out;
  border-radius: 2px;
  filter: blur(0.5px);
  box-shadow: 0 0 10px rgba(134, 239, 172, 0.9);
}

.text-underline::after {
  display: none;
}

@keyframes shineSideToSide {
  0% {
    left: -35%;
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    left: 100%;
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
  padding: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: transparent;
}

.user-info {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 20px;
  border: 1.5px solid #39FF14;
  box-shadow: 
    0 0 6px rgba(57, 255, 20, 0.4),
    0 0 12px rgba(57, 255, 20, 0.2),
    inset 0 0 8px rgba(57, 255, 20, 0.1);
  transition: all 0.3s ease;
  width: auto;
  max-width: 100%;
}

.user-info:hover {
  border-color: #7FFF00;
  box-shadow: 
    0 0 10px rgba(57, 255, 20, 0.6),
    0 0 18px rgba(57, 255, 20, 0.3),
    inset 0 0 12px rgba(57, 255, 20, 0.15);
}

.user-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 1.5px solid rgba(57, 255, 20, 0.6);
}

.user-initials {
  font-size: 11px;
  font-weight: 600;
  color: #39FF14;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  line-height: 1;
}

.user-details {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
}

.user-name {
  margin: 0;
  font-size: 11px;
  font-weight: 700;
  color: #39FF14;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-shadow: 
    0 0 4px rgba(57, 255, 20, 0.5),
    0 0 8px rgba(57, 255, 20, 0.3),
    0 1px 2px rgba(0, 0, 0, 0.5);
  letter-spacing: 0.3px;
  line-height: 1.2;
}

.user-role {
  margin: 2px 0 0 0;
  font-size: 9px;
  color: rgba(255, 255, 255, 0.85);
  opacity: 1;
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  line-height: 1.2;
}

/* Territorio integrado en user-details */
.territorio-separator {
  width: 100%;
  height: 1px;
  background: #4ade80;
  margin: 6px 0 4px 0;
}

.user-territorio {
  display: flex;
  align-items: center;
  gap: 3px;
  margin-top: 3px;
}

.user-territorio-icon {
  width: 10px;
  height: 10px;
  color: #f97316;
  flex-shrink: 0;
}

.user-territorio-text {
  font-size: 8px;
  font-weight: 500;
  color: #fed7aa;
  line-height: 1.2;
}

.user-estados {
  margin: 2px 0 0 0;
  font-size: 7px;
  color: rgba(187, 247, 208, 0.9);
  font-weight: 400;
  font-style: italic;
  line-height: 1.2;
}

.logout-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 6px 8px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  background: linear-gradient(135deg, 
    rgba(255, 87, 34, 0.9) 0%,
    rgba(244, 67, 54, 0.9) 100%);
  color: white;
  font-family: 'Poppins', sans-serif;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
  letter-spacing: 0.3px;
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
  width: 15px;
  height: 15px;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

/* ===================================
   MODAL DE LOGOUT MODERNO Y ELEGANTE
   =================================== */

/* Overlay con blur y animación */
.logout-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, 
    rgba(0, 0, 0, 0.4) 0%, 
    rgba(20, 20, 20, 0.6) 50%, 
    rgba(0, 0, 0, 0.8) 100%
  );
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 20px;
}

/* Contenedor principal del modal */
.logout-modal-container {
  width: 100%;
  max-width: 340px;
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 
    0 20px 40px -12px rgba(0, 0, 0, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  position: relative;
  transform-origin: center;
}

/* Header con gradiente rojo elegante */
.logout-modal-header {
  background: linear-gradient(135deg, 
    #dc2626 0%, 
    #ef4444 25%, 
    #f87171 50%, 
    #ef4444 75%, 
    #dc2626 100%
  );
  background-size: 300% 300%;
  animation: gradientShift 6s ease infinite;
  padding: 18px;
  position: relative;
  overflow: hidden;
}

/* Patrón de fondo sutil */
.logout-modal-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 25% 25%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 75% 75%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
  z-index: 1;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

/* Contenido del header */
.logout-header-content {
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
  z-index: 2;
}

/* Contenedor del icono principal */
.logout-icon-container {
  position: relative;
}

.logout-icon-bg {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.25) 0%, 
    rgba(255, 255, 255, 0.1) 100%
  );
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 6px 24px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.logout-icon-bg::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: conic-gradient(
    from 0deg,
    transparent 0deg,
    rgba(255, 255, 255, 0.1) 90deg,
    transparent 180deg,
    rgba(255, 255, 255, 0.1) 270deg,
    transparent 360deg
  );
  animation: iconRotate 4s linear infinite;
}

@keyframes iconRotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.logout-icon {
  width: 24px;
  height: 24px;
  color: #ffffff;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  z-index: 1;
  position: relative;
}

/* Texto del header */
.logout-header-text {
  flex: 1;
}

.logout-title {
  margin: 0 0 3px 0;
  font-size: 18px;
  font-weight: 700;
  color: #ffffff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  font-family: 'Inter', sans-serif;
}

.logout-subtitle {
  margin: 0;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 400;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* Botón cerrar elegante */
.logout-close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
  z-index: 3;
}

.logout-close-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.3);
  transform: rotate(90deg) scale(1.1);
}

.logout-close-btn svg {
  width: 16px;
  height: 16px;
  color: #ffffff;
}

/* Cuerpo del modal */
.logout-modal-body {
  padding: 24px 18px;
  background: #ffffff;
}

/* Sección de advertencia */
.logout-warning-section {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  padding: 16px;
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  border-radius: 10px;
  border: 1px solid #fecaca;
  position: relative;
  overflow: hidden;
}

.logout-warning-section::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(to bottom, #dc2626, #ef4444);
}

.logout-warning-icon {
  flex-shrink: 0;
  width: 42px;
  height: 42px;
  background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 3px 10px rgba(220, 38, 38, 0.3);
}

.logout-warning-icon svg {
  width: 20px;
  height: 20px;
  color: #ffffff;
}

.logout-warning-content {
  flex: 1;
}

.logout-warning-title {
  margin: 0 0 6px 0;
  font-size: 15px;
  font-weight: 600;
  color: #7f1d1d;
  font-family: 'Inter', sans-serif;
}

.logout-warning-text {
  margin: 0;
  font-size: 13px;
  color: #991b1b;
  line-height: 1.4;
}

/* Sección de información */
.logout-info-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.logout-info-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  background: #f8fafc;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.logout-info-item:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.logout-info-icon {
  width: 20px;
  height: 20px;
  color: #64748b;
  flex-shrink: 0;
}

.logout-info-item span {
  font-size: 13px;
  color: #475569;
  font-weight: 500;
}

/* Footer con botones */
.logout-modal-footer {
  padding: 16px 18px;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

/* Botones del modal */
.logout-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  border-radius: 8px;
  border: none;
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.logout-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.6s ease;
}

.logout-btn:hover::before {
  left: 100%;
}

.logout-btn-icon {
  width: 14px;
  height: 14px;
  transition: transform 0.2s ease;
}

.logout-btn:hover .logout-btn-icon {
  transform: scale(1.1);
}

/* Botón cancelar */
.logout-btn-cancel {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  color: #475569;
  border: 2px solid #cbd5e1;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.logout-btn-cancel:hover {
  background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
  border-color: #94a3b8;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Botón confirmar */
.logout-btn-confirm {
  background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
  color: #ffffff;
  border: 2px solid #dc2626;
  box-shadow: 
    0 4px 12px rgba(220, 38, 38, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.logout-btn-confirm:hover {
  background: linear-gradient(135deg, #b91c1c 0%, #dc2626 100%);
  border-color: #b91c1c;
  transform: translateY(-2px);
  box-shadow: 
    0 8px 20px rgba(220, 38, 38, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.logout-btn-confirm:active {
  transform: translateY(0);
  box-shadow: 
    0 2px 8px rgba(220, 38, 38, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

/* Animaciones de transición del modal */
.modal-enter-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-enter-from {
  opacity: 0;
  transform: scale(0.8) translateY(20px);
}

.modal-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-10px);
}

.modal-enter-to,
.modal-leave-from {
  opacity: 1;
  transform: scale(1) translateY(0);
}

/* Responsividad */
@media (max-width: 480px) {
  .logout-modal-overlay {
    padding: 12px;
  }
  
  .logout-modal-container {
    max-width: 100%;
    border-radius: 14px;
    margin: 0 auto;
  }
  
  .logout-modal-header {
    padding: 16px;
  }
  
  .logout-header-content {
    gap: 10px;
  }
  
  .logout-icon-bg {
    width: 40px;
    height: 40px;
  }
  
  .logout-icon {
    width: 20px;
    height: 20px;
  }
  
  .logout-title {
    font-size: 16px;
  }
  
  .logout-subtitle {
    font-size: 12px;
  }
  
  .logout-close-btn {
    top: 10px;
    right: 10px;
    width: 28px;
    height: 28px;
  }
  
  .logout-close-btn svg {
    width: 14px;
    height: 14px;
  }
  
  .logout-modal-body {
    padding: 18px 16px;
  }
  
  .logout-warning-section {
    padding: 14px;
    gap: 10px;
    margin-bottom: 16px;
  }
  
  .logout-warning-icon {
    width: 36px;
    height: 36px;
  }
  
  .logout-warning-icon svg {
    width: 18px;
    height: 18px;
  }
  
  .logout-warning-title {
    font-size: 14px;
  }
  
  .logout-warning-text {
    font-size: 12px;
  }
  
  .logout-info-section {
    gap: 8px;
  }
  
  .logout-info-item {
    padding: 8px 12px;
    gap: 8px;
  }
  
  .logout-info-icon {
    width: 16px;
    height: 16px;
  }
  
  .logout-info-item span {
    font-size: 12px;
  }
  
  .logout-modal-footer {
    padding: 14px 16px;
    flex-direction: column;
    gap: 8px;
  }
  
  .logout-btn {
    justify-content: center;
    padding: 10px 14px;
    font-size: 12px;
  }
  
  .logout-btn-icon {
    width: 12px;
    height: 12px;
  }
}

/* Para pantallas extra pequeñas */
@media (max-width: 320px) {
  .logout-modal-overlay {
    padding: 8px;
  }
  
  .logout-modal-container {
    border-radius: 12px;
  }
  
  .logout-modal-header {
    padding: 14px;
  }
  
  .logout-title {
    font-size: 15px;
  }
  
  .logout-subtitle {
    font-size: 11px;
  }
  
  .logout-modal-body {
    padding: 16px 14px;
  }
  
  .logout-warning-section {
    padding: 12px;
  }
  
  .logout-modal-footer {
    padding: 12px 14px;
  }
}

/* Para tablets en orientación portrait */
@media (min-width: 481px) and (max-width: 768px) {
  .logout-modal-container {
    max-width: 380px;
  }
  
  .logout-modal-header {
    padding: 20px;
  }
  
  .logout-modal-body {
    padding: 26px 20px;
  }
  
  .logout-modal-footer {
    padding: 18px 20px;
  }
}

/* Para tablets en orientación landscape y pantallas medianas */
@media (min-width: 769px) and (max-width: 1024px) {
  .logout-modal-container {
    max-width: 340px;
  }
}

/* Para pantallas grandes */
@media (min-width: 1025px) {
  .logout-modal-container {
    max-width: 340px;
  }
}

/* Ajustes para altura de pantalla */
@media (max-height: 600px) {
  .logout-modal-overlay {
    align-items: flex-start;
    padding-top: 20px;
  }
  
  .logout-modal-body {
    padding: 18px 16px;
  }
  
  .logout-warning-section {
    margin-bottom: 16px;
  }
  
  .logout-info-section {
    gap: 8px;
  }
}

@media (max-height: 500px) {
  .logout-modal-overlay {
    padding: 10px;
    padding-top: 15px;
  }
  
  .logout-modal-header {
    padding: 14px;
  }
  
  .logout-modal-body {
    padding: 16px 14px;
  }
  
  .logout-warning-section {
    padding: 12px;
    margin-bottom: 12px;
  }
  
  .logout-info-section {
    gap: 6px;
  }
  
  .logout-info-item {
    padding: 6px 10px;
  }
  
  .logout-modal-footer {
    padding: 12px 14px;
  }
}

/* Modo oscuro (opcional) */
@media (prefers-color-scheme: dark) {
  .logout-modal-container {
    background: #1f2937;
  }
  
  .logout-modal-body {
    background: #1f2937;
  }
  
  .logout-warning-section {
    background: linear-gradient(135deg, #374151 0%, #4b5563 100%);
    border-color: #6b7280;
  }
  
  .logout-warning-title {
    color: #fca5a5;
  }
  
  .logout-warning-text {
    color: #f87171;
  }
  
  .logout-info-item {
    background: #374151;
    border-color: #4b5563;
  }
  
  .logout-info-item:hover {
    background: #4b5563;
    border-color: #6b7280;
  }
  
  .logout-info-icon {
    color: #9ca3af;
  }
  
  .logout-info-item span {
    color: #d1d5db;
  }
  
  .logout-modal-footer {
    background: #374151;
    border-color: #4b5563;
  }
}

/* Responsive Design - Sidebar siempre visible */
@media (max-width: 992px) {
  .sidebar {
    width: 200px;
    min-width: 180px;
    max-width: 220px;
  }
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    width: 240px;
    min-width: 220px;
    max-width: 260px;
    z-index: 9999;
    transform: translateX(0);
    transition: transform 0.3s ease;
  }
  
  .sidebar-toggle {
    display: none; /* Ocultar botón toggle ya que siempre está visible */
  }
  
  /* Asegurar que el contenido principal tenga margen para el sidebar */
  .main-content {
    margin-left: 240px;
    width: calc(100% - 240px);
  }
  
  /* Mostrar todos los textos en móvil */
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
  .sidebar {
    width: 200px;
    min-width: 180px;
    max-width: 220px;
  }
  
  .main-content {
    margin-left: 200px;
    width: calc(100% - 200px);
  }
  
  /* Reducir tamaños para aprovechar mejor el espacio en móviles */
  .sidebar-header {
    padding: 8px 10px 6px;
  }
  
  .logo-animation {
    width: 32px;
    height: 32px;
    margin-bottom: 6px;
  }
  
  .brand-name {
    font-size: 12px;
    letter-spacing: 0.3px;
  }
  
  .brand-tagline {
    font-size: 9px;
    margin: 2px 0 0;
  }
  
  .text-underline {
    margin: 6px auto 0 auto;
    height: 2px;
  }
  
  .quick-links {
    padding: 6px 10px;
    margin: 0 8px 6px;
    gap: 6px;
  }
  
  .quick-link {
    padding: 6px 4px;
    gap: 2px;
  }
  
  .link-icon-container {
    width: 18px;
    height: 18px;
  }
  
  .link-icon {
    width: 10px;
    height: 10px;
  }
  
  .quick-link span {
    font-size: 7px;
  }
  
  .sidebar-nav {
    padding: 4px 8px 10px;
  }
  
  .nav-item {
    margin-bottom: 3px;
  }
  
  .nav-link {
    padding: 8px 10px;
  }
  
  .nav-icon-container {
    width: 22px;
    height: 22px;
    margin-right: 6px;
  }
  
  .nav-icon {
    width: 12px;
    height: 12px;
  }
  
  .nav-text {
    font-size: 11px;
  }
  
  .sidebar-footer {
    padding: 8px;
    gap: 6px;
  }
  
  .user-info {
    padding: 4px;
    gap: 6px;
  }
  
  .user-avatar {
    width: 24px;
    height: 24px;
  }
  
  .user-initials {
    font-size: 9px;
  }
  
  .user-name {
    font-size: 10px;
  }
  
  .user-role {
    font-size: 8px;
  }
  
  .logout-button {
    padding: 8px 10px;
    font-size: 10px;
    min-height: auto;
  }
  
  .logout-icon {
    width: 12px;
    height: 12px;
  }
}

/* Estilos específicos para orientación landscape en móviles */
@media (max-width: 768px) and (orientation: landscape) {
  .sidebar {
    width: 160px;
    min-width: 140px;
  }
  
  .main-content {
    margin-left: 160px;
    width: calc(100% - 160px);
  }
  
  .sidebar-header {
    padding: 6px 8px 4px;
  }
  
  .logo-animation {
    width: 24px;
    height: 24px;
    margin-bottom: 3px;
  }
  
  .brand-name {
    font-size: 10px;
    letter-spacing: 0.2px;
  }
  
  .brand-tagline {
    font-size: 7px;
    margin: 1px 0 0;
  }
  
  .text-underline {
    margin: 3px auto 0 auto;
    height: 1px;
  }
  
  .quick-links {
    padding: 3px 6px;
    margin: 0 4px 3px;
    gap: 3px;
  }
  
  .quick-link {
    padding: 3px 2px;
    gap: 1px;
  }
  
  .link-icon-container {
    width: 14px;
    height: 14px;
  }
  
  .link-icon {
    width: 7px;
    height: 7px;
  }
  
  .quick-link span {
    font-size: 5px;
  }
  
  .sidebar-nav {
    padding: 2px 4px 6px;
  }
  
  .nav-item {
    margin-bottom: 1px;
  }
  
  .nav-link {
    padding: 5px 6px;
  }
  
  .nav-icon-container {
    width: 18px;
    height: 18px;
    margin-right: 4px;
  }
  
  .nav-icon {
    width: 10px;
    height: 10px;
  }
  
  .nav-text {
    font-size: 9px;
  }
  
  .sidebar-footer {
    padding: 4px;
    gap: 3px;
  }
  
  .user-info {
    padding: 2px;
    gap: 3px;
  }
  
  .user-avatar {
    width: 20px;
    height: 20px;
  }
  
  .user-initials {
    font-size: 7px;
  }
  
  .user-name {
    font-size: 8px;
  }
  
  .user-role {
    font-size: 6px;
  }
  
  .logout-button {
    padding: 4px 6px;
    font-size: 8px;
  }
  
  .logout-icon {
    width: 8px;
    height: 8px;
  }
}

/* Estilos para tablets */
@media (min-width: 481px) and (max-width: 768px) {
  .sidebar {
    width: 250px;
    min-width: 230px;
  }
  
  .main-content {
    margin-left: 250px;
    width: calc(100% - 250px);
  }
}

/* Estilos para pantallas muy pequeñas (iPhone SE, etc.) */
@media (max-width: 375px) {
  .sidebar {
    width: 180px;
    min-width: 160px;
  }
  
  .main-content {
    margin-left: 180px;
    width: calc(100% - 180px);
  }
  
  .sidebar-header {
    padding: 6px 8px 4px;
  }
  
  .logo-animation {
    width: 28px;
    height: 28px;
    margin-bottom: 4px;
  }
  
  .brand-name {
    font-size: 11px;
    letter-spacing: 0.2px;
  }
  
  .brand-tagline {
    font-size: 8px;
    margin: 1px 0 0;
  }
  
  .text-underline {
    margin: 4px auto 0 auto;
    height: 2px;
  }
  
  .quick-links {
    padding: 4px 8px;
    margin: 0 6px 4px;
    gap: 4px;
  }
  
  .quick-link {
    padding: 4px 2px;
    gap: 1px;
  }
  
  .link-icon-container {
    width: 16px;
    height: 16px;
  }
  
  .link-icon {
    width: 8px;
    height: 8px;
  }
  
  .quick-link span {
    font-size: 6px;
  }
  
  .sidebar-nav {
    padding: 3px 6px 8px;
  }
  
  .nav-item {
    margin-bottom: 2px;
  }
  
  .nav-link {
    padding: 6px 8px;
  }
  
  .nav-icon-container {
    width: 20px;
    height: 20px;
    margin-right: 5px;
  }
  
  .nav-icon {
    width: 11px;
    height: 11px;
  }
  
  .nav-text {
    font-size: 10px;
  }
  
  .sidebar-footer {
    padding: 6px;
    gap: 4px;
  }
  
  .user-info {
    padding: 3px;
    gap: 4px;
  }
  
  .user-avatar {
    width: 22px;
    height: 22px;
  }
  
  .user-initials {
    font-size: 8px;
  }
  
  .user-name {
    font-size: 9px;
  }
  
  .user-role {
    font-size: 7px;
  }
  
  .logout-button {
    padding: 6px 8px;
    font-size: 9px;
  }
  
  .logout-icon {
    width: 10px;
    height: 10px;
  }
}

/* Estilos para dispositivos con notch (iPhone X+, etc.) */
@supports (padding: max(0px)) {
  .sidebar {
    padding-top: max(12px, env(safe-area-inset-top));
    padding-left: max(0px, env(safe-area-inset-left));
  }
}

/* Estilos para modo oscuro del sistema */
@media (prefers-color-scheme: dark) {
  .sidebar {
    box-shadow: 4px 0 15px rgba(0, 0, 0, 0.3);
  }
}

/* Mejoras de accesibilidad táctil - Manteniendo compacto */
@media (pointer: coarse) {
  .nav-link {
    min-height: 36px;
    display: flex;
    align-items: center;
  }
  
  .quick-link {
    min-height: 32px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  
  .logout-button {
    min-height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>
