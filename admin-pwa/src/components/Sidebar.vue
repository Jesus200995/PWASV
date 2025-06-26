<template>
  <div class="sidebar">
    <!-- Efecto liquid glass background -->
    <div class="sidebar-header">
      <div class="header-content">
        <!-- Animación de flor elegante flotante -->
        <div class="flower-animation">
          <svg class="flower-icon" viewBox="0 0 120 120" fill="none">
            <!-- Pétalos principales mejorados -->
            <g class="petals-main">
              <!-- Pétalos exteriores grandes -->
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-1)" opacity="0.9" transform="rotate(0 60 60)"/>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-2)" opacity="0.85" transform="rotate(36 60 60)"/>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-1)" opacity="0.9" transform="rotate(72 60 60)"/>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-2)" opacity="0.85" transform="rotate(108 60 60)"/>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-1)" opacity="0.9" transform="rotate(144 60 60)"/>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-2)" opacity="0.85" transform="rotate(180 60 60)"/>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-1)" opacity="0.9" transform="rotate(216 60 60)"/>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-2)" opacity="0.85" transform="rotate(252 60 60)"/>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-1)" opacity="0.9" transform="rotate(288 60 60)"/>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-2)" opacity="0.85" transform="rotate(324 60 60)"/>
            </g>
            
            <!-- Pétalos internos más pequeños -->
            <g class="petals-inner">
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(18 60 60)"/>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(54 60 60)"/>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(90 60 60)"/>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(126 60 60)"/>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(162 60 60)"/>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(198 60 60)"/>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(234 60 60)"/>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(270 60 60)"/>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(306 60 60)"/>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(342 60 60)"/>
            </g>
            
            <!-- Centro con múltiples capas -->
            <circle cx="60" cy="60" r="10" fill="url(#center-gradient)" opacity="0.95"/>
            <circle cx="60" cy="60" r="7" fill="url(#center-gradient-2)" opacity="0.9"/>
            <circle cx="60" cy="60" r="4" fill="#FFD700" opacity="0.8"/>
            <circle cx="60" cy="60" r="2" fill="#FFF8DC" opacity="0.9"/>
            
            <!-- Brillos dinámicos en el centro -->
            <circle cx="57" cy="57" r="1.5" fill="#FFFFFF" opacity="0.9">
              <animate attributeName="opacity" values="0.9;0.4;0.9" dur="2s" repeatCount="indefinite"/>
            </circle>
            <circle cx="63" cy="62" r="1" fill="#FFFFFF" opacity="0.7">
              <animate attributeName="opacity" values="0.7;0.3;0.7" dur="3s" repeatCount="indefinite"/>
            </circle>
            
            <!-- Definiciones de degradados mejorados -->
            <defs>
              <linearGradient id="petal-gradient-1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#FFFFFF;stop-opacity:0.95" />
                <stop offset="30%" style="stop-color:#F1F8E9;stop-opacity:0.9" />
                <stop offset="70%" style="stop-color:#E8F5E8;stop-opacity:0.8" />
                <stop offset="100%" style="stop-color:#C8E6C9;stop-opacity:0.7" />
              </linearGradient>
              <linearGradient id="petal-gradient-2" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#FFFFFF;stop-opacity:0.9" />
                <stop offset="30%" style="stop-color:#F8FFF8;stop-opacity:0.85" />
                <stop offset="70%" style="stop-color:#F1F8E9;stop-opacity:0.75" />
                <stop offset="100%" style="stop-color:#E8F5E8;stop-opacity:0.65" />
              </linearGradient>
              <linearGradient id="inner-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#FFFFFF;stop-opacity:0.9" />
                <stop offset="50%" style="stop-color:#F8FFF8;stop-opacity:0.7" />
                <stop offset="100%" style="stop-color:#F1F8E9;stop-opacity:0.5" />
              </linearGradient>
              <radialGradient id="center-gradient" cx="50%" cy="50%" r="50%">
                <stop offset="0%" style="stop-color:#FFE082;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#FFB300;stop-opacity:0.95" />
                <stop offset="100%" style="stop-color:#FF8F00;stop-opacity:0.8" />
              </radialGradient>
              <radialGradient id="center-gradient-2" cx="50%" cy="50%" r="50%">
                <stop offset="0%" style="stop-color:#FFF176;stop-opacity:0.9" />
                <stop offset="100%" style="stop-color:#FFB300;stop-opacity:0.7" />
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
        
        <li class="nav-item" :class="{ active: $route.name === 'Registros' }">
          <router-link to="/registros" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10,9 9,9 8,9"/>
              </svg>
            </div>
            <span class="nav-text">Registros</span>
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
  width: 280px;
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
  overflow: hidden;
  box-shadow: 
    0 8px 24px rgba(0, 0, 0, 0.25),
    0 4px 12px rgba(27, 94, 32, 0.4);
}
.sidebar-header {
  padding: 28px 20px 32px;
  border-bottom: 2px solid rgba(255, 255, 255, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  background: linear-gradient(135deg, 
    rgba(13, 78, 20, 0.8) 0%, 
    rgba(27, 94, 32, 0.6) 100%);
}

.header-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  width: 100%;
  max-width: 220px;
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

/* Estilos para la animación de flor flotante mejorada */
.flower-animation {
  width: 48px;
  height: 48px;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: flowerFloat 8s ease-in-out infinite;
  position: relative;
  filter: drop-shadow(0 4px 15px rgba(139, 195, 74, 0.3));
}

.flower-animation::before {
  content: '';
  position: absolute;
  width: 120%;
  height: 120%;
  background: radial-gradient(circle, rgba(139, 195, 74, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  animation: flowerAura 6s ease-in-out infinite;
  z-index: -1;
}

.flower-icon {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 2px 8px rgba(139, 195, 74, 0.4));
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  z-index: 1;
  position: relative;
}

.flower-icon:hover {
  transform: scale(1.2);
  filter: drop-shadow(0 6px 20px rgba(139, 195, 74, 0.6));
}

/* Animaciones mejoradas para la flor flotante */
@keyframes flowerFloat {
  0%, 100% {
    transform: translateY(0px) rotate(0deg) scale(1);
  }
  25% {
    transform: translateY(-8px) rotate(90deg) scale(1.05);
  }
  50% {
    transform: translateY(-4px) rotate(180deg) scale(1.1);
  }
  75% {
    transform: translateY(-10px) rotate(270deg) scale(1.05);
  }
}

@keyframes flowerAura {
  0%, 100% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.3);
    opacity: 0.6;
  }
}

/* Animación de los pétalos con movimiento independiente */
.petals-main {
  animation: petalsRotate 12s linear infinite;
  transform-origin: 60px 60px;
}

.petals-inner {
  animation: petalsRotate 18s linear infinite reverse;
  transform-origin: 60px 60px;
}

@keyframes petalsRotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
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
  font-size: 20px;
  font-weight: 800;
  color: #FFFFFF;
  letter-spacing: 0.08em;
  line-height: 1.1;
  font-family: 'Playfair Display', 'Georgia', 'Times New Roman', serif;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-transform: uppercase;
  font-variant: small-caps;
  position: relative;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5), 0 0 15px rgba(255, 255, 255, 0.2);
  white-space: nowrap;
}

.brand-title:hover {
  transform: translateY(-1px);
}

.brand-subtitle {
  margin: 0;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  letter-spacing: 0.15em;
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
  padding: 16px 16px 20px;
  margin-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  background: linear-gradient(135deg, 
    rgba(13, 78, 20, 0.6) 0%, 
    rgba(27, 94, 32, 0.4) 100%);
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
  padding: 10px 14px;
  border-radius: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  position: relative;
  overflow: hidden;
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
  width: 16px;
  height: 16px;
  stroke-width: 2.2;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  transition: all 0.3s ease;
}

.arrow-icon {
  width: 12px;
  height: 12px;
  opacity: 0.8;
  stroke-width: 2.5;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.geoportal-text {
  font-size: 13px;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  flex: 1;
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
  padding: 10px 14px;
  border-radius: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  position: relative;
  overflow: hidden;
  margin-top: 12px;
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
  width: 16px;
  height: 16px;
  stroke-width: 2.2;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  transition: all 0.3s ease;
}

.mobile-arrow-icon {
  width: 12px;
  height: 12px;
  opacity: 0.8;
  stroke-width: 2.5;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.mobile-app-text {
  font-size: 13px;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  flex: 1;
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
  padding: 24px 0;
}

.sidebar-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin-bottom: 8px;
  padding: 0 16px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 18px;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
  margin-bottom: 4px;
  backdrop-filter: blur(10px);
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
  width: 24px;
  height: 24px;
  position: relative;
}

.nav-icon {
  width: 20px;
  height: 20px;
  stroke-width: 2.2;
  transition: all 0.3s ease;
  filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.2));
}

.nav-text {
  font-size: 15px;
  font-weight: 600;
  text-shadow: none;
  letter-spacing: -0.01em;
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
  padding: 16px 16px 20px;
  border-top: 2px solid rgba(255, 255, 255, 0.3);
  position: relative;
  display: flex;
  justify-content: center;
  background: linear-gradient(135deg, 
    rgba(13, 78, 20, 0.8) 0%, 
    rgba(27, 94, 32, 0.6) 100%);
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
  max-width: 200px;
  background: linear-gradient(135deg, 
    #F44336 0%, 
    #E53935 100%);
  backdrop-filter: blur(12px);
  border: 2px solid rgba(244, 67, 54, 0.2);
  color: white;
  padding: 12px 16px;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: 13px;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
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
  width: 18px;
  height: 18px;
}

.logout-icon {
  width: 16px;
  height: 16px;
  stroke-width: 2.2;
  transition: all 0.3s ease;
  filter: drop-shadow(0 1px 3px rgba(0, 0, 0, 0.3));
}

.logout-text {
  font-size: 13px;
  font-weight: 600;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  letter-spacing: -0.01em;
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

/* Responsive para pantallas muy pequeñas */
@media (max-width: 480px) {
  .sidebar {
    width: 100%;
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    width: 280px;
  }
  
  .sidebar.collapsed {
    transform: translateX(-100%);
  }
  
  .sidebar:not(.collapsed) {
    transform: translateX(0);
  }
  
  .mobile-overlay {
    display: block;
  }
  
  .sidebar-toggle {
    display: block;
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 1002;
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

/* Responsive Design */
@media (max-width: 480px) {
  .logout-modal {
    margin: 10px;
    border-radius: 16px;
  }
  
  .modal-header {
    padding: 24px 20px 16px;
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
    font-size: 20px;
  }
  
  .modal-body {
    padding: 16px 20px;
  }
  
  .modal-body p {
    font-size: 15px;
  }
  
  .modal-actions {
    padding: 16px 20px 24px;
    flex-direction: column;
  }
  
  .btn-cancel,
  .btn-confirm {
    min-width: auto;
    padding: 14px 20px;
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
</style>
