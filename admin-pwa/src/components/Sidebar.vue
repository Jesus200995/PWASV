<template>
  <div class="sidebar">
    <!-- Efecto liquid glass background -->
    <div class="sidebar-header">
      <div class="header-content">
        <!-- Animación de flor elegante flotante -->
        <div class="flower-animation">
          <svg class="flower-icon" viewBox="0 0 120 120" fill="none">
            <!-- Pétalos principales mejorados con animación verde -->
            <g class="petals-main">
              <!-- Pétalos exteriores grandes -->
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-1)" opacity="0.9" transform="rotate(0 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="0 60 60;10 60 60;0 60 60" dur="4s" repeatCount="indefinite"/>
              </path>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-2)" opacity="0.85" transform="rotate(36 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="36 60 60;46 60 60;36 60 60" dur="4.2s" repeatCount="indefinite"/>
              </path>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-1)" opacity="0.9" transform="rotate(72 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="72 60 60;82 60 60;72 60 60" dur="3.8s" repeatCount="indefinite"/>
              </path>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-2)" opacity="0.85" transform="rotate(108 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="108 60 60;118 60 60;108 60 60" dur="4.1s" repeatCount="indefinite"/>
              </path>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-1)" opacity="0.9" transform="rotate(144 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="144 60 60;154 60 60;144 60 60" dur="3.9s" repeatCount="indefinite"/>
              </path>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-2)" opacity="0.85" transform="rotate(180 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="180 60 60;190 60 60;180 60 60" dur="4.3s" repeatCount="indefinite"/>
              </path>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-1)" opacity="0.9" transform="rotate(216 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="216 60 60;226 60 60;216 60 60" dur="3.7s" repeatCount="indefinite"/>
              </path>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-2)" opacity="0.85" transform="rotate(252 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="252 60 60;262 60 60;252 60 60" dur="4.4s" repeatCount="indefinite"/>
              </path>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-1)" opacity="0.9" transform="rotate(288 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="288 60 60;298 60 60;288 60 60" dur="3.6s" repeatCount="indefinite"/>
              </path>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-2)" opacity="0.85" transform="rotate(324 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="324 60 60;334 60 60;324 60 60" dur="4.5s" repeatCount="indefinite"/>
              </path>
            </g>
            
            <!-- Pétalos internos más pequeños con pulsación -->
            <g class="petals-inner">
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(18 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="2.5s" repeatCount="indefinite"/>
              </ellipse>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(54 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="2.8s" repeatCount="indefinite"/>
              </ellipse>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(90 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="2.3s" repeatCount="indefinite"/>
              </ellipse>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(126 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="2.7s" repeatCount="indefinite"/>
              </ellipse>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(162 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="2.4s" repeatCount="indefinite"/>
              </ellipse>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(198 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="2.9s" repeatCount="indefinite"/>
              </ellipse>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(234 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="2.2s" repeatCount="indefinite"/>
              </ellipse>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(270 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="2.6s" repeatCount="indefinite"/>
              </ellipse>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(306 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="2.1s" repeatCount="indefinite"/>
              </ellipse>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(342 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="3.0s" repeatCount="indefinite"/>
              </ellipse>
            </g>
            
            <!-- Centro con múltiples capas verdes -->
            <circle cx="60" cy="60" r="10" fill="url(#center-gradient)" opacity="0.95">
              <animate attributeName="r" values="10;12;10" dur="3s" repeatCount="indefinite"/>
            </circle>
            <circle cx="60" cy="60" r="7" fill="url(#center-gradient-2)" opacity="0.9">
              <animate attributeName="r" values="7;9;7" dur="2.8s" repeatCount="indefinite"/>
            </circle>
            <circle cx="60" cy="60" r="4" fill="#66BB6A" opacity="0.8">
              <animate attributeName="r" values="4;6;4" dur="2.5s" repeatCount="indefinite"/>
            </circle>
            <circle cx="60" cy="60" r="2" fill="#A5D6A7" opacity="0.9">
              <animate attributeName="r" values="2;3;2" dur="2.2s" repeatCount="indefinite"/>
            </circle>
            
            <!-- Brillos dinámicos en el centro con efecto verde -->
            <circle cx="57" cy="57" r="1.5" fill="#E8F5E8" opacity="0.9">
              <animate attributeName="opacity" values="0.9;0.3;0.9" dur="1.8s" repeatCount="indefinite"/>
              <animate attributeName="r" values="1.5;2.5;1.5" dur="1.8s" repeatCount="indefinite"/>
            </circle>
            <circle cx="63" cy="62" r="1" fill="#F1F8E9" opacity="0.7">
              <animate attributeName="opacity" values="0.7;0.2;0.7" dur="2.3s" repeatCount="indefinite"/>
              <animate attributeName="r" values="1;1.8;1" dur="2.3s" repeatCount="indefinite"/>
            </circle>
            
            <!-- Definiciones de degradados verdes mejorados -->
            <defs>
              <linearGradient id="petal-gradient-1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#C8E6C9;stop-opacity:0.95" />
                <stop offset="30%" style="stop-color:#A5D6A7;stop-opacity:0.9" />
                <stop offset="70%" style="stop-color:#81C784;stop-opacity:0.8" />
                <stop offset="100%" style="stop-color:#66BB6A;stop-opacity:0.7" />
              </linearGradient>
              <linearGradient id="petal-gradient-2" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#E8F5E8;stop-opacity:0.9" />
                <stop offset="30%" style="stop-color:#C8E6C9;stop-opacity:0.85" />
                <stop offset="70%" style="stop-color:#A5D6A7;stop-opacity:0.75" />
                <stop offset="100%" style="stop-color:#81C784;stop-opacity:0.65" />
              </linearGradient>
              <linearGradient id="inner-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#F1F8E9;stop-opacity:0.9" />
                <stop offset="50%" style="stop-color:#E8F5E8;stop-opacity:0.7" />
                <stop offset="100%" style="stop-color:#C8E6C9;stop-opacity:0.5" />
              </linearGradient>
              <radialGradient id="center-gradient" cx="50%" cy="50%" r="50%">
                <stop offset="0%" style="stop-color:#A5D6A7;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#81C784;stop-opacity:0.95" />
                <stop offset="100%" style="stop-color:#66BB6A;stop-opacity:0.8" />
              </radialGradient>
              <radialGradient id="center-gradient-2" cx="50%" cy="50%" r="50%">
                <stop offset="0%" style="stop-color:#C8E6C9;stop-opacity:0.9" />
                <stop offset="100%" style="stop-color:#81C784;stop-opacity:0.7" />
              </radialGradient>
            </defs>
          </svg>
        </div>
        <div class="logo-text">
          <h1 class="brand-title">SEMBRANDO VIDA</h1>
          <p class="brand-subtitle">Admin Panel</p>
        </div>
      </div>
    </div>
      <!-- Botón para ir al geoportal -->
    <div class="geoportal-section">
      <a href="https://geoportal.sembrandodatos.com/" target="_blank" class="geoportal-btn">
        <div class="geoportal-icon-wrapper">
          <svg class="geoportal-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <path d="M2 12h20"/>
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
            <path d="M8 12c0-2.5 1.8-4.5 4-4.5s4 2 4 4.5-1.8 4.5-4 4.5-4-2-4-4.5"/>
          </svg>
          <svg class="arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M7 17l10-10"/>
            <path d="M17 7v10"/>
            <path d="M17 7H7"/>
          </svg>
        </div>
        <span class="geoportal-text">Ir a Inicio Geoportal</span>
        <div class="geoportal-glow"></div>
      </a>
      
      <!-- Botón para ir a la App Móvil -->
      <a href="https://app.sembrandodatos.com/login" target="_blank" class="mobile-app-btn">
        <div class="mobile-app-icon-wrapper">
          <svg class="mobile-app-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="5" y="2" width="14" height="20" rx="2" ry="2"/>
            <line x1="12" y1="18" x2="12.01" y2="18"/>
          </svg>
          <svg class="mobile-arrow-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M7 17l10-10"/>
            <path d="M17 7v10"/>
            <path d="M17 7H7"/>
          </svg>
        </div>
        <span class="mobile-app-text">App Móvil</span>
        <div class="mobile-app-glow"></div>
      </a>
    </div>
      
      <nav class="sidebar-nav">
      <ul>
        <li class="nav-item" :class="{ active: $route.name === 'Dashboard' }">
          <router-link to="/dashboard" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="7" height="9"/>
                <rect x="14" y="3" width="7" height="5"/>
                <rect x="14" y="12" width="7" height="9"/>
                <rect x="3" y="16" width="7" height="5"/>
              </svg>
            </div>
            <span class="nav-text">Dashboard</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
        
        <li class="nav-item" :class="{ active: $route.name === 'Asistencia' }">
          <router-link to="/asistencia" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 6L9 17l-5-5"/>
                <path d="M3 12h6m6-6h6m-6 12h6"/>
                <rect x="7" y="3" width="3" height="18" rx="1"/>
                <rect x="14" y="3" width="3" height="18" rx="1"/>
              </svg>
            </div>
            <span class="nav-text">Asistencia</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
        
        <li class="nav-item" :class="{ active: $route.name === 'Registros' }">
          <router-link to="/registros" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <rect x="3" y="10" width="18" height="12"/>
                <line x1="8" y1="14" x2="16" y2="14"/>
                <line x1="8" y1="18" x2="12" y2="18"/>
              </svg>
            </div>
            <span class="nav-text">Registro de Actividades</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
        
        <li class="nav-item" :class="{ active: $route.name === 'Visor' }">
          <router-link to="/visor" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
            </div>
            <span class="nav-text">Visor de Mapa</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
        
        <li class="nav-item" :class="{ active: $route.name === 'Usuarios' }">
          <router-link to="/usuarios" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            </div>
            <span class="nav-text">Usuarios</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
        
        <li class="nav-item" :class="{ active: $route.name === 'Configuracion' }">
          <router-link to="/configuracion" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 1v6m0 6v6m11-7h-6m-6 0H1m21-7h-6M7 5h6"/>
                <path d="M19.42 15.58l-2.83-2.83m-3.18 0l-2.83 2.83M19.42 8.42l-2.83 2.83m-3.18 0L10.58 8.42"/>
              </svg>
            </div>
            <span class="nav-text">Configuración</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
      </ul>
    </nav>
      <div class="sidebar-footer">
      <button @click="showLogoutModal = true" class="logout-btn">
        <div class="btn-icon-wrapper">
          <svg class="logout-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16,17 21,12 16,7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
        </div>
        <span class="logout-text">Cerrar Sesión</span>
        <div class="logout-glow"></div>
      </button>
    </div>
    
    <!-- Modal de confirmación de logout -->
    <Teleport to="body">
      <div v-if="showLogoutModal" class="logout-modal-overlay" @click="closeModal">
        <div class="logout-modal" @click.stop>
          <div class="modal-header">          <div class="modal-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16,17 21,12 16,7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
          </div>
            <h3>Cerrar Sesión</h3>
          </div>
          
          <div class="modal-body">
            <p>¿Estás seguro de que quieres cerrar sesión?</p>
          </div>
          
          <div class="modal-actions">
            <button @click="closeModal" class="btn-cancel">
              Cancelar
            </button>
            <button @click="confirmLogout" class="btn-confirm">
              Aceptar
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['logout'])

// Estado del modal
const showLogoutModal = ref(false)

// Funciones del modal
const closeModal = () => {
  showLogoutModal.value = false
}

const confirmLogout = () => {
  showLogoutModal.value = false
  emit('logout')
}

// Cerrar modal con Escape
const handleKeydown = (event) => {
  if (event.key === 'Escape' && showLogoutModal.value) {
    closeModal()
  }
}

// Agregar listener para Escape
if (typeof window !== 'undefined') {
  window.addEventListener('keydown', handleKeydown)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800;900&family=Source+Sans+Pro:wght@300;400;600;700;900&display=swap');

.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: min(220px, 18vw);
  max-width: 240px;
  min-width: 180px;
  background: linear-gradient(180deg, 
    #1B5E20 0%, 
    #2E7D32 25%,
    #388E3C 50%,
    #2E7D32 75%,
    #1B5E20 100%);
  border-right: 3px solid #0D4E14;
  color: #FFFFFF;
  display: flex;
  flex-direction: column;
  z-index: 1000;
  overflow-y: auto;
  overflow-x: hidden;
  box-shadow: 
    0 8px 24px rgba(0, 0, 0, 0.25),
    0 4px 12px rgba(27, 94, 32, 0.4);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  
  /* Escalado dinámico basado en viewport */
  font-size: clamp(12px, 1.2vw, 16px);
}
.sidebar-header {
  padding: clamp(12px, 2.5vh, 28px) clamp(8px, 1.5vw, 20px) clamp(16px, 3vh, 32px);
  border-bottom: 2px solid rgba(255, 255, 255, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  background: linear-gradient(135deg, 
    rgba(13, 78, 20, 0.8) 0%, 
    rgba(27, 94, 32, 0.6) 100%);
  flex-shrink: 0;
  min-height: fit-content;
  max-height: 25vh;
}

.header-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: clamp(6px, 1.2vh, 12px);
  width: 100%;
  max-width: min(180px, 90%);
}

.sidebar-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 24px;
  right: 24px;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.6) 50%, 
    transparent 100%);
}

.logo {
  width: 56px;
  height: 56px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: transparent;
  border-radius: 18px;
  position: relative;
  overflow: visible;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  margin-bottom: 4px;
}

.logo:hover {
  transform: scale(1.1);
}

/* Estilos para la animación de flor girando */
.flower-animation {
  width: clamp(20px, 3.5vw, 40px);
  height: clamp(20px, 3.5vw, 40px);
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  filter: drop-shadow(0 4px 20px rgba(76, 175, 80, 0.4));
  animation: flowerRotate 8s linear infinite;
}

.flower-animation::before {
  content: '';
  position: absolute;
  width: 130%;
  height: 130%;
  background: radial-gradient(circle, rgba(76, 175, 80, 0.15) 0%, rgba(139, 195, 74, 0.08) 40%, transparent 70%);
  border-radius: 50%;
  animation: flowerAura 4s ease-in-out infinite;
  z-index: -1;
}

.flower-icon {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 3px 12px rgba(76, 175, 80, 0.5));
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  z-index: 1;
  position: relative;
}

.flower-icon:hover {
  transform: scale(1.15);
  filter: drop-shadow(0 6px 25px rgba(76, 175, 80, 0.7));
}

/* Animación de rotación continua para la flor */
@keyframes flowerRotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes flowerAura {
  0%, 100% {
    transform: scale(1);
    opacity: 0.4;
  }
  33% {
    transform: scale(1.1);
    opacity: 0.7;
  }
  66% {
    transform: scale(1.2);
    opacity: 0.5;
  }
}

/* Efectos adicionales para la nueva animación verde */
.flower-animation::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, transparent 60%, rgba(76, 175, 80, 0.1) 80%, transparent 100%);
  border-radius: 50%;
  animation: flowerPulse 3s ease-in-out infinite;
  z-index: -2;
}

@keyframes flowerPulse {
  0%, 100% {
    transform: scale(0.8);
    opacity: 0;
  }
  50% {
    transform: scale(1.4);
    opacity: 0.6;
  }
}

/* Tipografía profesional mejorada */
.logo-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 4px;
  width: 100%;
}

.brand-title {
  margin: 0;
  font-size: clamp(9px, 1.2vw, 14px);
  font-weight: 800;
  background: linear-gradient(135deg, 
    #E8F5E8 0%, 
    #A5D6A7 25%,
    #66BB6A 50%,
    #4CAF50 75%,
    #2E7D32 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: clamp(0.06em, 0.1vw, 0.12em);
  line-height: 1.2;
  font-family: 'Source Sans Pro', 'SF Pro Display', 'system-ui', '-apple-system', sans-serif;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-transform: uppercase;
  position: relative;
  white-space: nowrap;
  filter: drop-shadow(0 2px 4px rgba(76, 175, 80, 0.3));
  padding-bottom: clamp(3px, 0.6vh, 6px);
}

.brand-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    #E8F5E8 10%,
    #A5D6A7 25%,
    #66BB6A 50%,
    #4CAF50 75%,
    #2E7D32 90%,
    transparent 100%);
  border-radius: 2px;
  box-shadow: 
    0 0 8px rgba(76, 175, 80, 0.4),
    0 2px 4px rgba(0, 0, 0, 0.1);
  animation: underlineGlow 3s ease-in-out infinite;
}

@keyframes underlineGlow {
  0%, 100% {
    opacity: 0.8;
    transform: translateX(-50%) scaleX(1);
  }
  50% {
    opacity: 1;
    transform: translateX(-50%) scaleX(1.05);
  }
}

.brand-title:hover {
  transform: translateY(-1px);
}

.brand-subtitle {
  margin: 0;
  font-size: clamp(7px, 0.9vw, 10px);
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  letter-spacing: clamp(0.08em, 0.1vw, 0.12em);
  text-transform: uppercase;
  font-family: 'Montserrat', 'Inter', 'Source Sans Pro', sans-serif;
  opacity: 0.9;
  transition: all 0.3s ease;
  font-variant: small-caps;
}

.brand-subtitle:hover {
  opacity: 1;
  transform: translateY(-0.5px);
}

/* Estilos modernos para el botón del geoportal */
.geoportal-section {
  padding: clamp(8px, 1.5vh, 16px) clamp(8px, 1.5vw, 16px) clamp(12px, 2vh, 20px);
  margin-bottom: clamp(4px, 0.8vh, 8px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  background: linear-gradient(135deg, 
    rgba(13, 78, 20, 0.6) 0%, 
    rgba(27, 94, 32, 0.4) 100%);
  flex-shrink: 0;
  max-height: 20vh;
}

.geoportal-section::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 24px;
  right: 24px;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.4) 50%, 
    transparent 100%);
}

.geoportal-btn {
  width: 100%;
  background: linear-gradient(135deg, 
    #2E7D32 0%, 
    #4CAF50 30%,
    #388E3C 70%,
    #1B5E20 100%);
  backdrop-filter: blur(12px);
  border: 2px solid rgba(46, 125, 50, 0.4);
  color: white;
  padding: clamp(5px, 0.8vh, 8px) clamp(6px, 1vw, 10px);
  border-radius: clamp(10px, 1.8vw, 16px);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(3px, 0.6vw, 6px);
  font-size: clamp(9px, 1vw, 11px);
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  position: relative;
  overflow: hidden;
  min-height: clamp(28px, 3.5vh, 36px);
  box-shadow: 
    0 4px 15px rgba(46, 125, 50, 0.4),
    0 2px 8px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.geoportal-btn:hover {
  background: linear-gradient(135deg, 
    #1B5E20 0%, 
    #2E7D32 50%,
    #0D4E14 100%);
  transform: translateY(-3px) scale(1.05);
  box-shadow: 
    0 12px 30px rgba(46, 125, 50, 0.6),
    inset 0 1px 0 rgba(255, 255, 255, 0.3),
    0 0 0 3px rgba(46, 125, 50, 0.4);
}

.geoportal-btn:hover .geoportal-glow {
  opacity: 1;
  transform: scale(1);
}

.geoportal-btn:hover .arrow-icon {
  transform: translateX(6px) rotate(45deg);
}

.geoportal-btn:active {
  transform: translateY(-1px) scale(1.01);
}

.geoportal-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  gap: 6px;
}

.geoportal-icon {
  width: clamp(10px, 1.2vw, 14px);
  height: clamp(10px, 1.2vw, 14px);
  stroke-width: 2.2;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  transition: all 0.3s ease;
}

.arrow-icon {
  width: clamp(8px, 1vw, 10px);
  height: clamp(8px, 1vw, 10px);
  opacity: 0.8;
  stroke-width: 2.5;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.geoportal-text {
  font-size: clamp(9px, 1vw, 11px);
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.geoportal-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 70%);
  border-radius: 16px;
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  transition: all 0.4s ease;
  pointer-events: none;
}

/* Estilos modernos para el botón de la App Móvil */
.mobile-app-btn {
  width: 100%;
  background: linear-gradient(135deg, 
    #2196F3 0%, 
    #1976D2 100%);
  backdrop-filter: blur(12px);
  border: 2px solid rgba(33, 150, 243, 0.2);
  color: white;
  padding: clamp(5px, 0.8vh, 8px) clamp(6px, 1vw, 10px);
  border-radius: clamp(10px, 1.8vw, 16px);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(3px, 0.6vw, 6px);
  font-size: clamp(9px, 1vw, 11px);
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  position: relative;
  overflow: hidden;
  margin-top: clamp(4px, 1vh, 8px);
  min-height: clamp(28px, 3.5vh, 36px);
  box-shadow: 
    0 4px 15px rgba(33, 150, 243, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.mobile-app-btn:hover {
  background: linear-gradient(135deg, 
    #1976D2 0%, 
    #1565C0 100%);
  transform: translateY(-3px) scale(1.05);
  box-shadow: 
    0 12px 30px rgba(33, 150, 243, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.3),
    0 0 0 3px rgba(33, 150, 243, 0.3);
}

.mobile-app-btn:hover .mobile-app-glow {
  opacity: 1;
  transform: scale(1);
}

.mobile-app-btn:hover .mobile-arrow-icon {
  transform: translateX(6px) rotate(45deg);
}

.mobile-app-btn:active {
  transform: translateY(-1px) scale(1.01);
}

.mobile-app-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  gap: 6px;
}

.mobile-app-icon {
  width: clamp(10px, 1.2vw, 14px);
  height: clamp(10px, 1.2vw, 14px);
  stroke-width: 2.2;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  transition: all 0.3s ease;
}

.mobile-arrow-icon {
  width: clamp(8px, 1vw, 10px);
  height: clamp(8px, 1vw, 10px);
  opacity: 0.8;
  stroke-width: 2.5;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.mobile-app-text {
  font-size: clamp(9px, 1vw, 11px);
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.mobile-app-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 70%);
  border-radius: 16px;
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  transition: all 0.4s ease;
  pointer-events: none;
}

.sidebar-nav {
  flex: 1;
  padding: clamp(12px, 2vh, 24px) 0;
  overflow-y: auto;
  overflow-x: hidden;
  min-height: 0;
}

.sidebar-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin-bottom: clamp(3px, 0.6vh, 6px);
  padding: 0 clamp(6px, 1.2vw, 12px);
}

.nav-link {
  display: flex;
  align-items: center;
  gap: clamp(8px, 1.2vw, 12px);
  padding: clamp(8px, 1.6vh, 14px) clamp(8px, 1.5vw, 14px);
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  border-radius: clamp(6px, 1vw, 10px);
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
  margin-bottom: clamp(1px, 0.3vh, 3px);
  backdrop-filter: blur(10px);
  min-height: clamp(40px, 5vh, 52px);
}

.nav-link:hover {
  background: linear-gradient(135deg, 
    rgba(13, 78, 20, 0.3) 0%, 
    rgba(27, 94, 32, 0.2) 100%);
  color: #FFFFFF;
  transform: translateX(4px) scale(1.01);
  box-shadow: 
    0 4px 15px rgba(13, 78, 20, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
}

.nav-link:hover .nav-glow {
  opacity: 1;
  transform: scale(1);
}

.nav-item.active .nav-link,
.nav-link.router-link-active,
.nav-link.router-link-exact-active {
  background: linear-gradient(135deg, 
    #0D4E14 0%, 
    #1B5E20 100%);
  color: white;
  box-shadow: 
    0 6px 20px rgba(13, 78, 20, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.25);
  transform: translateX(3px);
}

.nav-item.active .nav-link .nav-icon,
.nav-link.router-link-active .nav-icon,
.nav-link.router-link-exact-active .nav-icon {
  filter: drop-shadow(0 2px 8px rgba(255, 255, 255, 0.3));
}

.nav-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: clamp(18px, 2.2vw, 20px);
  height: clamp(18px, 2.2vw, 20px);
  position: relative;
  flex-shrink: 0;
}

.nav-icon {
  width: clamp(14px, 1.8vw, 18px);
  height: clamp(14px, 1.8vw, 18px);
  stroke-width: 2.2;
  transition: all 0.3s ease;
  filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.2));
}

.nav-text {
  font-size: clamp(9px, 1.1vw, 12px);
  font-weight: 600;
  text-shadow: none;
  letter-spacing: -0.01em;
  white-space: normal;
  word-wrap: break-word;
  overflow-wrap: break-word;
  line-height: 1.2;
  flex: 1;
  min-width: 0;
  text-align: left;
}

.nav-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(27, 94, 32, 0.3) 0%, transparent 70%);
  border-radius: 16px;
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  transition: all 0.4s ease;
  pointer-events: none;
}

.sidebar-footer {
  padding: clamp(8px, 1.6vh, 16px) clamp(8px, 1.6vw, 16px) clamp(12px, 2vh, 20px);
  border-top: 2px solid rgba(255, 255, 255, 0.3);
  position: relative;
  display: flex;
  justify-content: center;
  background: linear-gradient(135deg, 
    rgba(13, 78, 20, 0.8) 0%, 
    rgba(27, 94, 32, 0.6) 100%);
  flex-shrink: 0;
  margin-top: auto;
  max-height: 15vh;
}

.sidebar-footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 24px;
  right: 24px;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.4) 50%, 
    transparent 100%);
}

.logout-btn {
  width: 100%;
  max-width: min(180px, 90%);
  background: linear-gradient(135deg, 
    #F44336 0%, 
    #E53935 100%);
  backdrop-filter: blur(12px);
  border: 2px solid rgba(244, 67, 54, 0.2);
  color: white;
  padding: clamp(6px, 1vh, 10px) clamp(8px, 1.4vw, 12px);
  border-radius: clamp(6px, 1vw, 10px);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(4px, 0.8vw, 8px);
  font-size: clamp(9px, 1vw, 11px);
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
  min-height: clamp(32px, 4vh, 40px);
  box-shadow: 
    0 4px 15px rgba(244, 67, 54, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.logout-btn:hover {
  background: linear-gradient(135deg, 
    #D32F2F 0%, 
    #C62828 100%);
  transform: translateY(-2px) scale(1.02);
  box-shadow: 
    0 8px 25px rgba(244, 67, 54, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.logout-btn:hover .logout-glow {
  opacity: 1;
  transform: scale(1);
}

.logout-btn:hover .logout-icon {
  animation: logoutShake 0.6s ease-in-out;
}

.logout-btn:active {
  transform: translateY(-1px) scale(1.02);
}

/* Animación sutil de pulsación para el botón */
@keyframes logoutPulse {
  0%, 100% {
    box-shadow: 
      0 6px 20px rgba(244, 67, 54, 0.2),
      0 0 0 1px rgba(255, 255, 255, 0.05),
      inset 0 1px 0 rgba(255, 255, 255, 0.08);
  }
  50% {
    box-shadow: 
      0 8px 25px rgba(244, 67, 54, 0.3),
      0 0 0 1px rgba(255, 255, 255, 0.08),
      inset 0 1px 0 rgba(255, 255, 255, 0.12);
  }
}

/* Animación de temblor para el icono en hover */
@keyframes logoutShake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-2px); }
  20%, 40%, 60%, 80% { transform: translateX(2px); }
}

.btn-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: clamp(14px, 1.6vw, 16px);
  height: clamp(14px, 1.6vw, 16px);
  flex-shrink: 0;
}

.logout-icon {
  width: clamp(10px, 1.2vw, 14px);
  height: clamp(10px, 1.2vw, 14px);
  stroke-width: 2.2;
  transition: all 0.3s ease;
  filter: drop-shadow(0 1px 3px rgba(0, 0, 0, 0.3));
}

.logout-text {
  font-size: clamp(9px, 1vw, 11px);
  font-weight: 600;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  letter-spacing: -0.01em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
  min-width: 0;
}

.logout-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.2) 0%, transparent 70%);
  border-radius: 12px;
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  transition: all 0.3s ease;
  pointer-events: none;
}

/* Responsive Design para tablets */
@media (max-width: 1024px) and (min-width: 769px) {
  .sidebar {
    width: 260px;
  }
  
  .sidebar-header {
    padding: 20px 16px 24px;
  }
  
  .flower-animation {
    width: 40px;
    height: 40px;
  }
  
  .brand-title {
    font-size: 14px;
    letter-spacing: 0.1em;
  }
  
  .brand-subtitle {
    font-size: 11px;
  }
  
  .geoportal-section {
    padding: 12px 12px 16px;
  }
  
  .geoportal-btn,
  .mobile-app-btn {
    padding: 8px 12px;
    font-size: 12px;
  }
  
  .nav-link {
    padding: 12px 14px;
    gap: 12px;
    min-height: 50px;
  }
  
  .nav-text {
    font-size: 13px;
    white-space: normal;
    word-wrap: break-word;
    line-height: 1.2;
  }
  
  .logout-btn {
    padding: 10px 14px;
    font-size: 12px;
  }
}

/* Responsive Design para móviles landscape */
@media (max-width: 768px) and (orientation: landscape) {
  .sidebar {
    width: 240px;
    height: 100vh;
    overflow-y: auto;
    overflow-x: hidden;
    position: fixed;
    z-index: 1001;
  }
  
  .sidebar-header {
    padding: 12px 12px 16px;
    min-height: auto;
  }
  
  .header-content {
    gap: 8px;
  }
  
  .flower-animation {
    width: 32px;
    height: 32px;
  }
  
  .brand-title {
    font-size: 12px;
    letter-spacing: 0.08em;
    line-height: 1.1;
  }
  
  .brand-subtitle {
    font-size: 9px;
  }
  
  .geoportal-section {
    padding: 8px 8px 12px;
  }
  
  .geoportal-btn,
  .mobile-app-btn {
    padding: 6px 10px;
    font-size: 11px;
    gap: 6px;
    margin-top: 8px;
  }
  
  .geoportal-icon,
  .mobile-app-icon {
    width: 14px;
    height: 14px;
  }
  
  .arrow-icon,
  .mobile-arrow-icon {
    width: 10px;
    height: 10px;
  }
  
  .sidebar-nav {
    padding: 12px 0;
  }
  
  .nav-item {
    margin-bottom: 4px;
    padding: 0 8px;
  }
  
  .nav-link {
    padding: 8px 12px;
    gap: 10px;
    min-height: 48px;
  }
  
  .nav-icon {
    width: 16px;
    height: 16px;
  }
  
  .nav-text {
    font-size: 11px;
    white-space: normal;
    word-wrap: break-word;
    line-height: 1.2;
  }
  
  .sidebar-footer {
    padding: 8px 8px 12px;
  }
  
  .logout-btn {
    padding: 8px 12px;
    font-size: 11px;
    gap: 8px;
  }
  
  .logout-icon {
    width: 14px;
    height: 14px;
  }
}

/* Responsive Design para móviles portrait */
@media (max-width: 768px) and (orientation: portrait) {
  .sidebar {
    width: 100%;
    height: 100vh;
    overflow-y: auto;
    overflow-x: hidden;
    position: fixed;
    z-index: 1001;
    display: flex;
    flex-direction: column;
  }
  
  .sidebar-header {
    padding: 16px 16px 20px;
    flex-shrink: 0;
  }
  
  .header-content {
    gap: 12px;
  }
  
  .flower-animation {
    width: 36px;
    height: 36px;
  }
  
  .brand-title {
    font-size: 13px;
    letter-spacing: 0.1em;
  }
  
  .brand-subtitle {
    font-size: 10px;
  }
  
  .geoportal-section {
    padding: 12px 16px 16px;
    flex-shrink: 0;
  }
  
  .geoportal-btn,
  .mobile-app-btn {
    padding: 10px 16px;
    font-size: 12px;
    gap: 10px;
  }
  
  .mobile-app-btn {
    margin-top: 10px;
  }
  
  .sidebar-nav {
    flex: 1;
    padding: 16px 0;
    overflow-y: auto;
  }
  
  .nav-item {
    margin-bottom: 6px;
    padding: 0 16px;
  }
  
  .nav-link {
    padding: 12px 16px;
    gap: 14px;
    min-height: 52px;
  }
  
  .nav-icon {
    width: 18px;
    height: 18px;
  }
  
  .nav-text {
    font-size: 12px;
    white-space: normal;
    word-wrap: break-word;
    line-height: 1.2;
  }
  
  .sidebar-footer {
    padding: 16px 16px 20px;
    flex-shrink: 0;
  }
  
  .logout-btn {
    padding: 12px 16px;
    font-size: 12px;
    gap: 10px;
  }
  
  .logout-icon {
    width: 16px;
    height: 16px;
  }
}

/* Responsive para pantallas muy pequeñas (móviles pequeños) */
@media (max-width: 480px) {
  .sidebar {
    width: 100%;
  }
  
  .sidebar-header {
    padding: 12px 12px 16px;
  }
  
  .flower-animation {
    width: 30px;
    height: 30px;
  }
  
  .brand-title {
    font-size: 11px;
    letter-spacing: 0.08em;
  }
  
  .brand-subtitle {
    font-size: 9px;
  }
  
  .geoportal-section {
    padding: 10px 12px 14px;
  }
  
  .geoportal-btn,
  .mobile-app-btn {
    padding: 8px 12px;
    font-size: 11px;
    gap: 8px;
    border-radius: 16px;
  }
  
  .geoportal-icon,
  .mobile-app-icon {
    width: 14px;
    height: 14px;
  }
  
  .arrow-icon,
  .mobile-arrow-icon {
    width: 10px;
    height: 10px;
  }
  
  .sidebar-nav {
    padding: 14px 0;
  }
  
  .nav-item {
    margin-bottom: 4px;
    padding: 0 12px;
  }
  
  .nav-link {
    padding: 10px 14px;
    gap: 12px;
    border-radius: 10px;
    min-height: 46px;
  }
  
  .nav-icon {
    width: 16px;
    height: 16px;
  }
  
  .nav-text {
    font-size: 11px;
    white-space: normal;
    word-wrap: break-word;
    line-height: 1.2;
  }
  
  .sidebar-footer {
    padding: 12px 12px 16px;
  }
  
  .logout-btn {
    padding: 10px 14px;
    font-size: 11px;
    gap: 8px;
    border-radius: 10px;
  }
  
  .logout-icon {
    width: 14px;
    height: 14px;
  }
}

/* Ajustes para pantallas extra pequeñas */
@media (max-width: 320px) {
  .sidebar-header {
    padding: 10px 8px 12px;
  }
  
  .flower-animation {
    width: 28px;
    height: 28px;
  }
  
  .brand-title {
    font-size: 10px;
    letter-spacing: 0.06em;
  }
  
  .brand-subtitle {
    font-size: 8px;
  }
  
  .geoportal-section {
    padding: 8px 8px 12px;
  }
  
  .geoportal-btn,
  .mobile-app-btn {
    padding: 6px 10px;
    font-size: 10px;
    gap: 6px;
  }
  
  .nav-item {
    padding: 0 8px;
  }
  
  .nav-link {
    padding: 8px 10px;
    gap: 10px;
    min-height: 44px;
  }
  
  .nav-icon {
    width: 14px;
    height: 14px;
  }
  
  .nav-text {
    font-size: 10px;
    white-space: normal;
    word-wrap: break-word;
    line-height: 1.2;
  }
  
  .sidebar-footer {
    padding: 8px 8px 12px;
  }
  
  .logout-btn {
    padding: 8px 10px;
    font-size: 10px;
    gap: 6px;
  }
  
  .logout-icon {
    width: 12px;
    height: 12px;
  }
}

/* Mejoras para scrolling en móviles */
@media (max-width: 768px) {
  .sidebar {
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    -ms-overflow-style: none;
  }
  
  .sidebar::-webkit-scrollbar {
    display: none;
  }
  
  .sidebar-nav {
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    -ms-overflow-style: none;
  }
  
  .sidebar-nav::-webkit-scrollbar {
    display: none;
  }
}

/* Estilos del Modal de Logout */
.logout-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  padding: 20px;
  animation: overlayFadeIn 0.3s ease-out;
}

@keyframes overlayFadeIn {
  from {
    opacity: 0;
    backdrop-filter: blur(0px);
  }
  to {
    opacity: 1;
    backdrop-filter: blur(8px);
  }
}

.logout-modal {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  max-width: 400px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  animation: modalSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.8) translateY(30px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  padding: 30px 30px 20px;
  text-align: center;
  border-bottom: 1px solid rgba(76, 175, 80, 0.1);
}

.modal-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto 16px;
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: iconPulse 2s ease-in-out infinite;
}

@keyframes iconPulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 10px rgba(76, 175, 80, 0);
  }
}

.modal-icon svg {
  width: 28px;
  height: 28px;
  color: white;
}

.modal-header h3 {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #2E7D32;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.modal-body {
  padding: 20px 30px;
  text-align: center;
}

.modal-body p {
  margin: 0;
  font-size: 16px;
  color: #555;
  line-height: 1.5;
}

.modal-actions {
  padding: 20px 30px 30px;
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-cancel,
.btn-confirm {
  flex: 1;
  padding: 12px 20px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  min-width: 120px;
}

.btn-cancel {
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  color: #666;
  border: 2px solid rgba(0, 0, 0, 0.1);
}

.btn-cancel:hover {
  background: linear-gradient(135deg, #eeeeee 0%, #d5d5d5 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-confirm {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}

.btn-confirm:hover {
  background: linear-gradient(135deg, #45a049 0%, #388e3c 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.btn-confirm::before,
.btn-cancel::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn-confirm:hover::before,
.btn-cancel:hover::before {
  left: 100%;
}

.btn-confirm:active,
.btn-cancel:active {
  transform: translateY(0);
}

/* Responsive Design para modal de logout */
@media (max-width: 480px) {
  .logout-modal {
    margin: 10px;
    border-radius: 16px;
    max-width: calc(100vw - 20px);
  }
  
  .modal-header {
    padding: 20px 16px 12px;
  }
  
  .modal-icon {
    width: 50px;
    height: 50px;
    margin-bottom: 12px;
  }
  
  .modal-icon svg {
    width: 24px;
    height: 24px;
  }
  
  .modal-header h3 {
    font-size: 18px;
  }
  
  .modal-body {
    padding: 12px 16px;
  }
  
  .modal-body p {
    font-size: 14px;
  }
  
  .modal-actions {
    padding: 12px 16px 20px;
    flex-direction: column;
    gap: 8px;
  }
  
  .btn-cancel,
  .btn-confirm {
    min-width: auto;
    padding: 12px 16px;
    font-size: 14px;
  }
}

@media (max-width: 360px) {
  .logout-modal {
    margin: 8px;
  }
  
  .modal-header {
    padding: 16px 12px 10px;
  }
  
  .modal-icon {
    width: 45px;
    height: 45px;
    margin-bottom: 10px;
  }
  
  .modal-icon svg {
    width: 22px;
    height: 22px;
  }
  
  .modal-header h3 {
    font-size: 16px;
  }
  
  .modal-body {
    padding: 10px 12px;
  }
  
  .modal-body p {
    font-size: 13px;
  }
  
  .modal-actions {
    padding: 10px 12px 16px;
  }
  
  .btn-cancel,
  .btn-confirm {
    padding: 10px 14px;
    font-size: 13px;
  }
}

/* Mejoras para accesibilidad táctil */
@media (max-width: 768px) {
  .nav-link,
  .geoportal-btn,
  .mobile-app-btn,
  .logout-btn {
    min-height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .btn-cancel,
  .btn-confirm {
    min-height: 44px;
    touch-action: manipulation;
  }
}

/* Reglas para zoom extremo y alta densidad de píxeles */
@media (max-width: 100vw) and (max-height: 100vh) {
  .sidebar {
    font-size: clamp(8px, 1vw, 16px);
    width: clamp(160px, 20vw, 240px);
  }
  
  .sidebar-header {
    padding: clamp(6px, 1.5vh, 28px) clamp(4px, 1vw, 20px) clamp(8px, 2vh, 32px);
    max-height: clamp(80px, 20vh, 160px);
  }
  
  .flower-animation {
    width: clamp(20px, 3vw, 48px);
    height: clamp(20px, 3vw, 48px);
  }
  
  .brand-title {
    font-size: clamp(8px, 1.2vw, 16px);
    letter-spacing: clamp(0.05em, 0.1vw, 0.15em);
  }
  
  .brand-subtitle {
    font-size: clamp(6px, 0.8vw, 12px);
  }
  
  .geoportal-section {
    padding: clamp(4px, 1vh, 16px) clamp(4px, 1vw, 16px) clamp(6px, 1.5vh, 20px);
    max-height: clamp(60px, 15vh, 120px);
  }
  
  .geoportal-btn,
  .mobile-app-btn {
    padding: clamp(4px, 0.8vh, 10px) clamp(6px, 1vw, 14px);
    font-size: clamp(8px, 0.9vw, 13px);
    min-height: clamp(28px, 3.5vh, 44px);
    border-radius: clamp(8px, 1.5vw, 20px);
  }
  
  .geoportal-icon,
  .mobile-app-icon {
    width: clamp(10px, 1.2vw, 16px);
    height: clamp(10px, 1.2vw, 16px);
  }
  
  .arrow-icon,
  .mobile-arrow-icon {
    width: clamp(8px, 1vw, 12px);
    height: clamp(8px, 1vw, 12px);
  }
  
  .sidebar-nav {
    padding: clamp(8px, 1.5vh, 24px) 0;
    min-height: clamp(200px, 40vh, 400px);
  }
  
  .nav-item {
    margin-bottom: clamp(2px, 0.5vh, 8px);
    padding: 0 clamp(4px, 1vw, 16px);
  }
  
  .nav-link {
    padding: clamp(6px, 1vh, 16px) clamp(8px, 1.5vw, 18px);
    gap: clamp(8px, 1.2vw, 16px);
    min-height: clamp(32px, 4vh, 52px);
    border-radius: clamp(6px, 1vw, 12px);
  }
  
  .nav-icon {
    width: clamp(14px, 1.8vw, 20px);
    height: clamp(14px, 1.8vw, 20px);
  }
  
  .nav-text {
    font-size: clamp(9px, 1.1vw, 15px);
  }
  
  .sidebar-footer {
    padding: clamp(6px, 1.2vh, 16px) clamp(6px, 1.2vw, 16px) clamp(8px, 1.6vh, 20px);
    max-height: clamp(60px, 12vh, 100px);
  }
  
  .logout-btn {
    padding: clamp(6px, 1vh, 12px) clamp(8px, 1.4vw, 16px);
    font-size: clamp(8px, 0.9vw, 13px);
    min-height: clamp(32px, 4vh, 48px);
    border-radius: clamp(6px, 1vw, 12px);
    gap: clamp(4px, 0.8vw, 10px);
  }
  
  .logout-icon {
    width: clamp(10px, 1.2vw, 16px);
    height: clamp(10px, 1.2vw, 16px);
  }
}

/* Ajustes para zoom de navegador */
@media screen and (-webkit-min-device-pixel-ratio: 1.25), 
       screen and (min-resolution: 120dpi) {
  .sidebar {
    font-size: clamp(10px, 1.1vw, 15px);
  }
  
  .brand-title {
    font-size: clamp(9px, 1.3vw, 15px);
  }
  
  .nav-text,
  .geoportal-text,
  .mobile-app-text,
  .logout-text {
    font-size: clamp(9px, 1vw, 12px);
  }
}

/* Ajustes para zoom muy alto */
@media screen and (-webkit-min-device-pixel-ratio: 2), 
       screen and (min-resolution: 192dpi) {
  .sidebar {
    font-size: clamp(8px, 1vw, 14px);
    width: clamp(140px, 18vw, 220px);
  }
  
  .flower-animation {
    width: clamp(18px, 2.5vw, 40px);
    height: clamp(18px, 2.5vw, 40px);
  }
  
  .brand-title {
    font-size: clamp(7px, 1.1vw, 14px);
  }
  
  .brand-subtitle {
    font-size: clamp(5px, 0.7vw, 10px);
  }
  
  .nav-text,
  .geoportal-text,
  .mobile-app-text,
  .logout-text {
    font-size: clamp(7px, 0.9vw, 11px);
  }
}

/* Manejo de contenido que se desborda */
@media (max-height: 500px) {
  .sidebar {
    font-size: clamp(8px, 1vw, 12px);
  }
  
  .sidebar-header {
    padding: clamp(4px, 1vh, 16px) clamp(6px, 1vw, 16px);
    max-height: 15vh;
  }
  
  .flower-animation {
    width: clamp(16px, 2.5vw, 32px);
    height: clamp(16px, 2.5vw, 32px);
  }
  
  .brand-title {
    font-size: clamp(7px, 1vw, 12px);
    padding-bottom: clamp(2px, 0.5vh, 6px);
  }
  
  .brand-subtitle {
    font-size: clamp(5px, 0.7vw, 9px);
  }
  
  .geoportal-section {
    padding: clamp(3px, 0.8vh, 12px) clamp(6px, 1vw, 12px);
    max-height: 12vh;
  }
  
  .geoportal-btn,
  .mobile-app-btn {
    padding: clamp(3px, 0.6vh, 8px) clamp(6px, 1vw, 12px);
    font-size: clamp(6px, 0.8vw, 10px);
    min-height: clamp(24px, 3vh, 36px);
    margin-top: clamp(3px, 0.8vh, 8px);
  }
  
  .nav-link {
    padding: clamp(4px, 0.8vh, 12px) clamp(8px, 1.2vw, 14px);
    min-height: clamp(28px, 3.5vh, 44px);
  }
  
  .nav-text {
    font-size: clamp(6px, 0.9vw, 12px);
  }
  
  .nav-icon {
    width: clamp(12px, 1.5vw, 18px);
    height: clamp(12px, 1.5vw, 18px);
  }
  
  .sidebar-footer {
    padding: clamp(4px, 1vh, 12px) clamp(6px, 1vw, 12px);
    max-height: 10vh;
  }
  
  .logout-btn {
    padding: clamp(4px, 0.8vh, 10px) clamp(6px, 1.2vw, 14px);
    font-size: clamp(6px, 0.8vw, 11px);
    min-height: clamp(28px, 3.5vh, 40px);
  }
}

/* Prevención de contenido oculto */
@media (max-height: 400px) {
  .sidebar {
    overflow-y: auto !important;
    height: 100vh;
  }
  
  .sidebar-header,
  .geoportal-section,
  .sidebar-footer {
    flex-shrink: 0;
  }
  
  .sidebar-nav {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
  }
  
  .brand-title {
    font-size: clamp(6px, 0.9vw, 10px);
    line-height: 1.1;
  }
  
  .brand-subtitle {
    font-size: clamp(4px, 0.6vw, 8px);
  }
  
  .nav-text,
  .geoportal-text,
  .mobile-app-text,
  .logout-text {
    font-size: clamp(5px, 0.7vw, 9px);
  }
}

/* Animación de cierre */
.logout-modal-overlay.fade-out {
  animation: overlayFadeOut 0.3s ease-in;
}

.logout-modal-overlay.fade-out .logout-modal {
  animation: modalSlideOut 0.3s ease-in;
}

@keyframes overlayFadeOut {
  from {
    opacity: 1;
    backdrop-filter: blur(8px);
  }
  to {
    opacity: 0;
    backdrop-filter: blur(0px);
  }
}

@keyframes modalSlideOut {
  from {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
  to {
    opacity: 0;
    transform: scale(0.8) translateY(30px);
  }
}

/* Optimizaciones finales para escalado dinámico */
.sidebar * {
  box-sizing: border-box;
}

/* Asegurar que el texto nunca se corte */
.nav-text,
.geoportal-text,
.mobile-app-text,
.logout-text,
.brand-title,
.brand-subtitle {
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
}

/* Scroll suave en toda la aplicación */
.sidebar,
.sidebar-nav {
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.sidebar::-webkit-scrollbar,
.sidebar-nav::-webkit-scrollbar {
  display: none;
}

/* Mejora de rendimiento para animaciones */
.flower-animation,
.flower-icon,
.nav-glow,
.geoportal-glow,
.mobile-app-glow,
.logout-glow {
  transform: translateZ(0);
  backface-visibility: hidden;
  perspective: 1000px;
}

.sidebar {
  will-change: transform;
  contain: layout style paint;
}

/* Estados hover optimizados para zoom */
@media (hover: hover) and (pointer: fine) {
  .nav-link:hover,
  .geoportal-btn:hover,
  .mobile-app-btn:hover,
  .logout-btn:hover {
    transform: translateX(2px) scale(1.01);
  }
}

/* Estados activos para touch */
@media (hover: none) and (pointer: coarse) {
  .nav-link:active,
  .geoportal-btn:active,
  .mobile-app-btn:active,
  .logout-btn:active {
    transform: scale(0.98);
  }
}

/* Prevención de zoom accidental en iOS */
@media screen and (-webkit-min-device-pixel-ratio: 0) {
  .sidebar input,
  .sidebar button,
  .sidebar select,
  .sidebar textarea {
    font-size: clamp(16px, 1.2vw, 16px);
  }
}
</style>
