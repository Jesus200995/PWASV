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
        <!-- Icono de localización/ubicación profesional animado -->
        <svg class="location-icon" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="sidebarLocationGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:#4CAF50;stop-opacity:1" />
              <stop offset="50%" style="stop-color:#66BB6A;stop-opacity:1" />
              <stop offset="100%" style="stop-color:#81C784;stop-opacity:1" />
            </linearGradient>
            <linearGradient id="sidebarPinGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:#2E7D32;stop-opacity:1" />
              <stop offset="100%" style="stop-color:#4CAF50;stop-opacity:1" />
            </linearGradient>
            <filter id="sidebarGlow">
              <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
              <feMerge> 
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
            <filter id="sidebarShadow">
              <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#2E7D32" flood-opacity="0.3"/>
            </filter>
          </defs>
          
          <!-- Pin de ubicación principal -->
          <path class="sidebar-location-pin" 
                d="M50 15 C35 15 25 25 25 40 C25 55 50 80 50 80 C50 80 75 55 75 40 C75 25 65 15 50 15 Z" 
                fill="url(#sidebarLocationGradient)" 
                filter="url(#sidebarShadow)"/>
          
          <!-- Círculo interior del pin -->
          <circle class="sidebar-pin-center" cx="50" cy="40" r="12" fill="url(#sidebarPinGradient)"/>
          <circle class="sidebar-pin-dot" cx="50" cy="40" r="6" fill="#FFFFFF"/>
          
          <!-- Ondas de señal -->
          <circle class="sidebar-signal-wave sidebar-wave1" cx="50" cy="40" r="20" fill="none" stroke="#4CAF50" stroke-width="2" opacity="0"/>
          <circle class="sidebar-signal-wave sidebar-wave2" cx="50" cy="40" r="25" fill="none" stroke="#66BB6A" stroke-width="1.5" opacity="0"/>
          <circle class="sidebar-signal-wave sidebar-wave3" cx="50" cy="40" r="30" fill="none" stroke="#81C784" stroke-width="1" opacity="0"/>
          
          <!-- Puntos de referencia alrededor -->
          <circle class="sidebar-ref-point sidebar-point1" cx="20" cy="25" r="2" fill="#4CAF50" opacity="0.6"/>
          <circle class="sidebar-ref-point sidebar-point2" cx="80" cy="30" r="1.5" fill="#66BB6A" opacity="0.7"/>
          <circle class="sidebar-ref-point sidebar-point3" cx="15" cy="60" r="1.8" fill="#81C784" opacity="0.5"/>
          <circle class="sidebar-ref-point sidebar-point4" cx="85" cy="65" r="2.2" fill="#4CAF50" opacity="0.6"/>
        </svg>
      </div>
      <div class="logo-text">
        <h2>Sembrando Vida</h2>
        <p>Admin Panel</p>
      </div>    </div>
    
    <!-- Botón para ir al geoportal -->
    <div class="geoportal-section">
      <a href="https://geoportal.sembrandodatos.com/" target="_blank" class="geoportal-btn">
        <div class="geoportal-icon-wrapper">
          <svg class="geoportal-icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z"/>
          </svg>
          <svg class="arrow-icon" viewBox="0 0 16 16" fill="currentColor">
            <path d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>
          </svg>
        </div>
        <span class="geoportal-text">Ir a Inicio Geoportal</span>
        <div class="geoportal-glow"></div>
      </a>
    </div>
      
      <nav class="sidebar-nav">
      <ul>
        <li class="nav-item" :class="{ active: $route.name === 'Dashboard' }">
          <router-link to="/dashboard" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
              </svg>
            </div>
            <span class="nav-text">Dashboard</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
        
        <li class="nav-item" :class="{ active: $route.name === 'Registros' }">
          <router-link to="/registros" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
              </svg>
            </div>
            <span class="nav-text">Registros</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
        
        <li class="nav-item" :class="{ active: $route.name === 'Usuarios' }">
          <router-link to="/usuarios" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M16 17V19H2V17S2 13 9 13 16 17 16 17M12.5 7.5A3.5 3.5 0 1 0 9 11A3.5 3.5 0 0 0 12.5 7.5M15.94 13A5.32 5.32 0 0 1 18 17V19H22V17S22 13.37 15.94 13M15 4A3.39 3.39 0 0 0 13.07 4.59A5 5 0 0 1 13.07 10.41A3.39 3.39 0 0 0 15 11A3.5 3.5 0 0 0 15 4Z"/>
              </svg>
            </div>
            <span class="nav-text">Usuarios</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
        
        <li class="nav-item" :class="{ active: $route.name === 'Configuracion' }">
          <router-link to="/configuracion" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.22,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.22,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.68 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"/>
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
          <svg class="nav-icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M16,17V14H9V10H16V7L21,12L16,17M14,2A2,2 0 0,1 16,4V6H14V4H5V20H14V18H16V20A2,2 0 0,1 14,22H5A2,2 0 0,1 3,20V4A2,2 0 0,1 5,2H14Z"/>
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
          <div class="modal-header">
            <div class="modal-icon">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M16,17V14H9V10H16V7L21,12L16,17M14,2A2,2 0 0,1 16,4V6H14V4H5V20H14V18H16V20A2,2 0 0,1 14,22H5A2,2 0 0,1 3,20V4A2,2 0 0,1 5,2H14Z"/>
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
  background: linear-gradient(135deg, 
    rgba(76, 175, 80, 0.95) 0%, 
    rgba(56, 142, 60, 0.95) 50%, 
    rgba(46, 125, 50, 0.95) 100%);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  display: flex;
  flex-direction: column;
  z-index: 1000;
  overflow: hidden;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

/* Efecto liquid glass background */
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
  background: linear-gradient(45deg, 
    rgba(255, 255, 255, 0.1) 0%, 
    rgba(255, 255, 255, 0.05) 100%);
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 200px;
  height: 200px;
  top: -50px;
  right: -50px;
  animation-delay: 0s;
}

.shape-2 {
  width: 150px;
  height: 150px;
  bottom: 100px;
  left: -30px;
  animation-delay: 2s;
}

.shape-3 {
  width: 100px;
  height: 100px;
  top: 50%;
  right: -20px;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% { 
    transform: translateY(0px) scale(1);
    opacity: 0.7;
  }
  50% { 
    transform: translateY(-20px) scale(1.1);
    opacity: 1;
  }
}

.sidebar-header {
  padding: 32px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
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
    rgba(255, 255, 255, 0.3) 50%, 
    transparent 100%);
}

.logo {
  min-width: 36px;
  display: flex;
  justify-content: center;
  align-items: center;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.location-icon {
  width: 40px;
  height: 40px;
  animation: sidebarIconFloat 3s ease-in-out infinite;
  filter: drop-shadow(0 2px 8px rgba(76, 175, 80, 0.3));
  transition: all 0.3s ease;
}

.location-icon:hover {
  transform: scale(1.05);
  filter: drop-shadow(0 4px 12px rgba(76, 175, 80, 0.4));
}

/* Animaciones del icono en sidebar */
@keyframes sidebarIconFloat {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-4px);
  }
}

/* Animación del pin de ubicación en sidebar */
.sidebar-location-pin {
  animation: sidebarPinPulse 2.5s ease-in-out infinite;
  transform-origin: 50px 40px;
}

@keyframes sidebarPinPulse {
  0%, 100% {
    transform: scale(1);
    filter: url(#sidebarShadow) brightness(1);
  }
  50% {
    transform: scale(1.03);
    filter: url(#sidebarShadow) brightness(1.1);
  }
}

/* Animación del centro del pin en sidebar */
.sidebar-pin-center {
  animation: sidebarCenterGlow 2s ease-in-out infinite alternate;
}

@keyframes sidebarCenterGlow {
  0% {
    r: 12;
    opacity: 1;
  }
  100% {
    r: 13;
    opacity: 0.8;
  }
}

/* Animación del punto central en sidebar */
.sidebar-pin-dot {
  animation: sidebarDotPulse 1.5s ease-in-out infinite;
}

@keyframes sidebarDotPulse {
  0%, 100% {
    r: 6;
    opacity: 1;
  }
  50% {
    r: 5;
    opacity: 0.8;
  }
}

/* Animaciones de las ondas de señal en sidebar */
.sidebar-signal-wave {
  animation: sidebarSignalRipple 4s ease-out infinite;
}

.sidebar-wave1 {
  animation-delay: 0s;
}

.sidebar-wave2 {
  animation-delay: 1.3s;
}

.sidebar-wave3 {
  animation-delay: 2.6s;
}

@keyframes sidebarSignalRipple {
  0% {
    r: 15;
    opacity: 0.6;
    stroke-width: 2;
  }
  50% {
    opacity: 0.3;
    stroke-width: 1.5;
  }
  100% {
    r: 32;
    opacity: 0;
    stroke-width: 0.5;
  }
}

/* Animación de los puntos de referencia en sidebar */
.sidebar-ref-point {
  animation: sidebarPointTwinkle 5s ease-in-out infinite;
}

.sidebar-point1 {
  animation-delay: 0s;
}

.sidebar-point2 {
  animation-delay: 1.25s;
}

.sidebar-point3 {
  animation-delay: 2.5s;
}

.sidebar-point4 {
  animation-delay: 3.75s;
}

@keyframes sidebarPointTwinkle {
  0%, 85%, 100% {
    opacity: 0.4;
    r: 1.5;
  }
  15% {
    opacity: 1;
    r: 2.5;
  }
}

.logo-text h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.logo-text p {
  margin: 0;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

/* Estilos para el botón del geoportal */
.geoportal-section {
  padding: 16px 16px 20px;
  margin-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
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
    rgba(255, 255, 255, 0.3) 50%, 
    transparent 100%);
}

.geoportal-btn {
  width: 100%;
  background: linear-gradient(135deg, 
    rgba(33, 150, 243, 0.9) 0%, 
    rgba(25, 118, 210, 0.9) 100%);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 12px 16px;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 15px rgba(33, 150, 243, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.geoportal-btn:hover {
  background: linear-gradient(135deg, 
    rgba(33, 150, 243, 1) 0%, 
    rgba(25, 118, 210, 1) 100%);
  transform: translateY(-2px);
  box-shadow: 
    0 8px 25px rgba(33, 150, 243, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.geoportal-btn:hover .geoportal-glow {
  opacity: 1;
  transform: scale(1);
}

.geoportal-btn:hover .arrow-icon {
  transform: translateX(4px);
}

.geoportal-btn:active {
  transform: translateY(0px);
}

.geoportal-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  gap: 4px;
}

.geoportal-icon {
  width: 18px;
  height: 18px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  animation: geoportalPulse 2s ease-in-out infinite;
}

.arrow-icon {
  width: 14px;
  height: 14px;
  opacity: 0.8;
  transition: all 0.3s ease;
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
  border-radius: 12px;
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  transition: all 0.3s ease;
  pointer-events: none;
}

@keyframes geoportalPulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
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
  padding: 14px 16px;
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  border-radius: 12px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  transform: translateX(4px);
}

.nav-link:hover .nav-glow {
  opacity: 1;
  transform: scale(1);
}

.nav-item.active .nav-link {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  color: white;
  box-shadow: 
    0 4px 15px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

/* Estilos específicos para router-link */
.nav-link.router-link-active,
.nav-link.router-link-exact-active {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  color: white;
  box-shadow: 
    0 4px 15px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
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
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.nav-text {
  font-size: 15px;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.nav-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  border-radius: 12px;
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  transition: all 0.3s ease;
  pointer-events: none;
}

.sidebar-footer {
  padding: 20px 16px 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  display: flex;
  justify-content: center;
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
    rgba(255, 255, 255, 0.3) 50%, 
    transparent 100%);
}

.logout-btn {
  width: 100%;
  background: linear-gradient(135deg, 
    rgba(244, 67, 54, 0.9) 0%, 
    rgba(211, 47, 47, 0.9) 100%);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 14px 16px;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 15px rgba(244, 67, 54, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.logout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 6px 20px rgba(244, 67, 54, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.logout-btn:hover .btn-glow {
  opacity: 1;
  transform: scale(1);
}

.logout-btn:active {
  transform: translateY(0);
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
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* Responsive para pantallas muy pequeñas */
@media (max-width: 480px) {
  .sidebar {
    width: 100%;
  }
}

.logout-btn {
  color: white;
  padding: 14px 16px;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 15px rgba(244, 67, 54, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.logout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 6px 20px rgba(244, 67, 54, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.logout-btn:hover .btn-glow {
  opacity: 1;
  transform: scale(1);
}

.logout-btn:active {
  transform: translateY(0);
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

.mobile-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 999;
}

/* Responsive */
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

/* Scrollbar personalizado para la navegación */
.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
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
