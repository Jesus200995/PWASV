<template>
  <div class="sidebar">
    <!-- Efecto liquid glass background -->
    <div class="liquid-bg">
      <div class="liquid-shape shape-1"></div>
      <div class="liquid-shape shape-2"></div>
      <div class="liquid-shape shape-3"></div>
    </div>
      <div class="sidebar-header">
      <div class="logo">
        <!-- Animación de flor elegante -->
        <div class="flower-animation">
          <svg class="flower-icon" viewBox="0 0 100 100" fill="none">
            <!-- Fondo circular sutil -->
            <circle cx="50" cy="50" r="35" fill="rgba(76, 175, 80, 0.05)" opacity="0.6"/>
            <circle cx="50" cy="50" r="30" fill="rgba(255, 255, 255, 0.03)" opacity="0.8"/>
            
            <!-- Pétalos principales con degradados -->
            <g class="petals-main">
              <path d="M50 20 C45 25, 45 35, 50 40 C55 35, 55 25, 50 20 Z" fill="url(#petal-gradient-1)" opacity="0.95" transform="rotate(0 50 50)"/>
              <path d="M50 20 C45 25, 45 35, 50 40 C55 35, 55 25, 50 20 Z" fill="url(#petal-gradient-2)" opacity="0.9" transform="rotate(45 50 50)"/>
              <path d="M50 20 C45 25, 45 35, 50 40 C55 35, 55 25, 50 20 Z" fill="url(#petal-gradient-1)" opacity="0.95" transform="rotate(90 50 50)"/>
              <path d="M50 20 C45 25, 45 35, 50 40 C55 35, 55 25, 50 20 Z" fill="url(#petal-gradient-2)" opacity="0.9" transform="rotate(135 50 50)"/>
              <path d="M50 20 C45 25, 45 35, 50 40 C55 35, 55 25, 50 20 Z" fill="url(#petal-gradient-1)" opacity="0.95" transform="rotate(180 50 50)"/>
              <path d="M50 20 C45 25, 45 35, 50 40 C55 35, 55 25, 50 20 Z" fill="url(#petal-gradient-2)" opacity="0.9" transform="rotate(225 50 50)"/>
              <path d="M50 20 C45 25, 45 35, 50 40 C55 35, 55 25, 50 20 Z" fill="url(#petal-gradient-1)" opacity="0.95" transform="rotate(270 50 50)"/>
              <path d="M50 20 C45 25, 45 35, 50 40 C55 35, 55 25, 50 20 Z" fill="url(#petal-gradient-2)" opacity="0.9" transform="rotate(315 50 50)"/>
            </g>
            
            <!-- Pétalos secundarios más refinados -->
            <g class="petals-secondary">
              <ellipse cx="50" cy="32" rx="3" ry="8" fill="rgba(200, 230, 201, 0.7)" opacity="0.8" transform="rotate(22.5 50 50)"/>
              <ellipse cx="50" cy="32" rx="3" ry="8" fill="rgba(200, 230, 201, 0.7)" opacity="0.8" transform="rotate(67.5 50 50)"/>
              <ellipse cx="50" cy="32" rx="3" ry="8" fill="rgba(200, 230, 201, 0.7)" opacity="0.8" transform="rotate(112.5 50 50)"/>
              <ellipse cx="50" cy="32" rx="3" ry="8" fill="rgba(200, 230, 201, 0.7)" opacity="0.8" transform="rotate(157.5 50 50)"/>
              <ellipse cx="50" cy="32" rx="3" ry="8" fill="rgba(200, 230, 201, 0.7)" opacity="0.8" transform="rotate(202.5 50 50)"/>
              <ellipse cx="50" cy="32" rx="3" ry="8" fill="rgba(200, 230, 201, 0.7)" opacity="0.8" transform="rotate(247.5 50 50)"/>
              <ellipse cx="50" cy="32" rx="3" ry="8" fill="rgba(200, 230, 201, 0.7)" opacity="0.8" transform="rotate(292.5 50 50)"/>
              <ellipse cx="50" cy="32" rx="3" ry="8" fill="rgba(200, 230, 201, 0.7)" opacity="0.8" transform="rotate(337.5 50 50)"/>
            </g>
            
            <!-- Centro mejorado con brillos -->
            <circle cx="50" cy="50" r="7" fill="url(#center-gradient)" opacity="0.95"/>
            <circle cx="50" cy="50" r="4" fill="#FFB300" opacity="0.9"/>
            <circle cx="50" cy="50" r="2" fill="#FFF9C4" opacity="0.8"/>
            
            <!-- Brillos en el centro -->
            <circle cx="48" cy="48" r="1" fill="#FFFFFF" opacity="0.9"/>
            <circle cx="52" cy="51" r="0.5" fill="#FFFFFF" opacity="0.7"/>
            
            <!-- Definiciones de degradados -->
            <defs>
              <linearGradient id="petal-gradient-1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#FFFFFF;stop-opacity:0.9" />
                <stop offset="50%" style="stop-color:#E8F5E8;stop-opacity:0.8" />
                <stop offset="100%" style="stop-color:#C8E6C9;stop-opacity:0.7" />
              </linearGradient>
              <linearGradient id="petal-gradient-2" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#F1F8E9;stop-opacity:0.85" />
                <stop offset="50%" style="stop-color:#DCEDC8;stop-opacity:0.75" />
                <stop offset="100%" style="stop-color:#AED581;stop-opacity:0.65" />
              </linearGradient>
              <radialGradient id="center-gradient" cx="50%" cy="50%" r="50%">
                <stop offset="0%" style="stop-color:#FFD54F;stop-opacity:1" />
                <stop offset="70%" style="stop-color:#FF8F00;stop-opacity:0.9" />
                <stop offset="100%" style="stop-color:#E65100;stop-opacity:0.8" />
              </radialGradient>
            </defs>
          </svg>
        </div>
      </div>
      <div class="logo-text">
        <h2>Sembrando Vida</h2>
        <p>Admin Panel</p>
      </div>    </div>
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
                <rect x="3" y="3" width="7" height="7"/>
                <rect x="14" y="3" width="7" height="7"/>
                <rect x="14" y="14" width="7" height="7"/>
                <rect x="3" y="14" width="7" height="7"/>
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
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16,17 21,12 16,7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
        </div>
        <span class="nav-text">Cerrar Sesión</span>
        <div class="btn-glow"></div>
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
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 280px;
  background: linear-gradient(180deg, 
    rgba(34, 139, 34, 0.98) 0%, 
    rgba(46, 125, 50, 0.98) 35%, 
    rgba(56, 142, 60, 0.98) 65%, 
    rgba(27, 94, 32, 0.98) 100%);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border-right: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
  display: flex;
  flex-direction: column;
  z-index: 1000;
  overflow: hidden;
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

/* Efecto liquid glass background mejorado */
.liquid-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: -1;
}

.liquid-shape {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.08) 0%, 
    rgba(255, 255, 255, 0.03) 50%,
    rgba(76, 175, 80, 0.06) 100%);
  animation: float 8s ease-in-out infinite;
  filter: blur(1px);
}

.shape-1 {
  width: 240px;
  height: 240px;
  top: -60px;
  right: -60px;
  animation-delay: 0s;
}

.shape-2 {
  width: 180px;
  height: 180px;
  bottom: 120px;
  left: -40px;
  animation-delay: 2.7s;
}

.shape-3 {
  width: 120px;
  height: 120px;
  top: 45%;
  right: -30px;
  animation-delay: 5.4s;
}

@keyframes float {
  0%, 100% { 
    transform: translateY(0px) rotate(0deg) scale(1);
    opacity: 0.4;
  }
  33% {
    transform: translateY(-15px) rotate(120deg) scale(1.05);
    opacity: 0.7;
  }
  66% {
    transform: translateY(-25px) rotate(240deg) scale(0.95);
    opacity: 0.5;
  }
}

.sidebar-header {
  padding: 32px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
  background: rgba(255, 255, 255, 0.02);
}

.sidebar-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 24px;
  right: 24px;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.2) 50%, 
    transparent 100%);
}

.logo {
  min-width: 48px;
  height: 48px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.12) 0%, 
    rgba(255, 255, 255, 0.06) 50%,
    rgba(76, 175, 80, 0.08) 100%);
  border-radius: 14px;
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  filter: drop-shadow(0 6px 16px rgba(0, 0, 0, 0.2));
  position: relative;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.logo::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.1) 0%, 
    transparent 50%);
  border-radius: 14px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
  filter: drop-shadow(0 8px 24px rgba(0, 0, 0, 0.25));
  border-color: rgba(255, 255, 255, 0.25);
}

.logo:hover::before {
  opacity: 1;
}

/* Estilos para la animación de la flor mejorada */
.flower-animation {
  width: 28px;
  height: 28px;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: flowerRotate 15s linear infinite;
  position: relative;
}

.flower-animation::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(76, 175, 80, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  animation: flowerPulse 4s ease-in-out infinite;
}

.flower-icon {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 3px 12px rgba(76, 175, 80, 0.4));
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  z-index: 1;
  position: relative;
}

.flower-icon:hover {
  transform: scale(1.15);
  filter: drop-shadow(0 6px 20px rgba(76, 175, 80, 0.6));
}

/* Animaciones mejoradas para la flor */
@keyframes flowerRotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes flowerPulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.6;
  }
}

/* Animación de los pétalos con movimiento más suave */
.petals-main {
  animation: petalsRotate 20s linear infinite;
  transform-origin: 50px 50px;
}

.petals-secondary {
  animation: petalsRotate 25s linear infinite reverse;
  transform-origin: 50px 50px;
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
  gap: 2px;
}

.logo-text h2 {
  margin: 0;
  font-size: 21px;
  font-weight: 800;
  background: linear-gradient(135deg, #FFFFFF 0%, #E8F5E8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 3px 12px rgba(0, 0, 0, 0.4);
  letter-spacing: -0.02em;
  line-height: 1.2;
  font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
  filter: drop-shadow(0 2px 8px rgba(76, 175, 80, 0.3));
  transition: all 0.3s ease;
}

.logo-text h2:hover {
  filter: drop-shadow(0 4px 16px rgba(76, 175, 80, 0.5));
  transform: translateY(-1px);
}

.logo-text p {
  margin: 0;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.75);
  font-weight: 600;
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
  letter-spacing: 0.02em;
  text-transform: uppercase;
  font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
  opacity: 0.9;
  transition: all 0.3s ease;
}

.logo-text p:hover {
  color: rgba(255, 255, 255, 0.9);
  opacity: 1;
}

/* Estilos modernos para el botón del geoportal */
.geoportal-section {
  padding: 16px 16px 20px;
  margin-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  position: relative;
  background: rgba(255, 255, 255, 0.02);
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
    rgba(255, 255, 255, 0.2) 50%, 
    transparent 100%);
}

.geoportal-btn {
  width: 100%;
  background: linear-gradient(135deg, 
    rgba(76, 175, 80, 0.9) 0%, 
    rgba(102, 187, 106, 0.9) 100%);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
  padding: 14px 18px;
  border-radius: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 8px 25px rgba(76, 175, 80, 0.25),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.geoportal-btn:hover {
  background: linear-gradient(135deg, 
    rgba(76, 175, 80, 1) 0%, 
    rgba(102, 187, 106, 1) 100%);
  transform: translateY(-3px) scale(1.02);
  box-shadow: 
    0 15px 35px rgba(76, 175, 80, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
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
  width: 18px;
  height: 18px;
  stroke-width: 2.2;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  transition: all 0.3s ease;
}

.arrow-icon {
  width: 14px;
  height: 14px;
  opacity: 0.8;
  stroke-width: 2.5;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.geoportal-text {
  font-size: 14px;
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
    rgba(33, 150, 243, 0.8) 0%, 
    rgba(25, 118, 210, 0.8) 100%);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
  padding: 14px 18px;
  border-radius: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
  margin-top: 12px;
  box-shadow: 
    0 8px 25px rgba(33, 150, 243, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.mobile-app-btn:hover {
  background: linear-gradient(135deg, 
    rgba(33, 150, 243, 0.95) 0%, 
    rgba(25, 118, 210, 0.95) 100%);
  transform: translateY(-3px) scale(1.02);
  box-shadow: 
    0 15px 35px rgba(33, 150, 243, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
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
  width: 18px;
  height: 18px;
  stroke-width: 2.2;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  transition: all 0.3s ease;
}

.mobile-arrow-icon {
  width: 14px;
  height: 14px;
  opacity: 0.8;
  stroke-width: 2.5;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.mobile-app-text {
  font-size: 14px;
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
  color: rgba(255, 255, 255, 0.85);
  text-decoration: none;
  border-radius: 16px;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
  margin-bottom: 4px;
  backdrop-filter: blur(10px);
}

.nav-link:hover {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.12) 0%, 
    rgba(255, 255, 255, 0.08) 100%);
  color: white;
  transform: translateX(6px) scale(1.02);
  box-shadow: 
    0 8px 25px rgba(76, 175, 80, 0.15),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.nav-link:hover .nav-glow {
  opacity: 1;
  transform: scale(1);
}

.nav-item.active .nav-link,
.nav-link.router-link-active,
.nav-link.router-link-exact-active {
  background: linear-gradient(135deg, 
    rgba(76, 175, 80, 0.9) 0%, 
    rgba(56, 142, 60, 0.9) 100%);
  color: white;
  box-shadow: 
    0 12px 30px rgba(76, 175, 80, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
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
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  letter-spacing: -0.01em;
}

.nav-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(76, 175, 80, 0.15) 0%, transparent 70%);
  border-radius: 16px;
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  transition: all 0.4s ease;
  pointer-events: none;
}

.sidebar-footer {
  padding: 20px 16px 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  position: relative;
  display: flex;
  justify-content: center;
  background: rgba(255, 255, 255, 0.02);
}

.sidebar-footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 24px;
  right: 24px;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.2) 50%, 
    transparent 100%);
}

.logout-btn {
  width: 100%;
  background: linear-gradient(135deg, 
    rgba(244, 67, 54, 0.9) 0%, 
    rgba(211, 47, 47, 0.9) 100%);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
  padding: 16px 18px;
  border-radius: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 8px 25px rgba(244, 67, 54, 0.25),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.logout-btn:hover {
  background: linear-gradient(135deg, 
    rgba(244, 67, 54, 1) 0%, 
    rgba(211, 47, 47, 1) 100%);
  transform: translateY(-3px) scale(1.02);
  box-shadow: 
    0 15px 35px rgba(244, 67, 54, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.logout-btn:hover .btn-glow {
  opacity: 1;
  transform: scale(1);
}

.logout-btn:active {
  transform: translateY(-1px) scale(1.01);
}

.btn-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
}

.btn-glow {
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

/* Scrollbar personalizado */
.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 2px;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
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
