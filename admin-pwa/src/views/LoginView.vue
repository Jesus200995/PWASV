<template>
  <div class="login-container">
    <!-- Liquid Glass Background con efectos mejorados -->
    <div class="liquid-background">
      <div class="gradient-overlay"></div>
      
      <!-- Elementos decorativos similares a Home.vue -->
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-green-300 rounded-full mix-blend-multiply filter blur-xl opacity-25 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-green-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse-slow" style="animation-delay: 4s;"></div>
      
      <div class="liquid-blob blob1"></div>
      <div class="liquid-blob blob2"></div>
      <div class="liquid-blob blob3"></div>
      <div class="liquid-blob blob4"></div>
      <div class="liquid-blob blob5"></div>
      <div class="liquid-blob blob6"></div>
      <div class="floating-particles">
        <div class="particle" v-for="n in 20" :key="n" :style="getParticleStyle(n)"></div>
      </div>
    </div>
    
    <!-- Contenedor principal con efecto glassmorphism -->
    <div class="login-card">
      <!-- Header con branding renovado -->
      <div class="login-header">
        <div class="logo-container">
          <!-- Nueva flor estática girando -->
          <div class="logo-bg">
            <svg class="logo-icon" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="petalGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#dcfce7;stop-opacity:1" />
                  <stop offset="30%" style="stop-color:#bbf7d0;stop-opacity:1" />
                  <stop offset="60%" style="stop-color:#86efac;stop-opacity:1" />
                  <stop offset="100%" style="stop-color:#4ade80;stop-opacity:1" />
                </linearGradient>
                <linearGradient id="centerGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#22c55e;stop-opacity:1" />
                  <stop offset="50%" style="stop-color:#16a34a;stop-opacity:1" />
                  <stop offset="100%" style="stop-color:#15803d;stop-opacity:1" />
                </linearGradient>
                <filter id="petalGlow" x="-50%" y="-50%" width="200%" height="200%">
                  <feGaussianBlur stdDeviation="1.5" result="coloredBlur"/>
                  <feMerge> 
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                  </feMerge>
                </filter>
                <filter id="centerShadow" x="-50%" y="-50%" width="200%" height="200%">
                  <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#15803d" flood-opacity="0.4"/>
                </filter>
              </defs>
              
              <!-- Grupo de la flor que girará como una unidad -->
              <g class="flower-rotating">
                <!-- Pétalos de la flor (8 pétalos) -->
                <!-- Pétalo superior -->
                <ellipse cx="50" cy="25" rx="8" ry="15" 
                         fill="url(#petalGradient)" filter="url(#petalGlow)"/>
                
                <!-- Pétalo superior derecho -->
                <ellipse cx="65" cy="35" rx="8" ry="15" 
                         fill="url(#petalGradient)" filter="url(#petalGlow)"
                         transform="rotate(45 65 35)"/>
                
                <!-- Pétalo derecho -->
                <ellipse cx="75" cy="50" rx="8" ry="15" 
                         fill="url(#petalGradient)" filter="url(#petalGlow)"
                         transform="rotate(90 75 50)"/>
                
                <!-- Pétalo inferior derecho -->
                <ellipse cx="65" cy="65" rx="8" ry="15" 
                         fill="url(#petalGradient)" filter="url(#petalGlow)"
                         transform="rotate(135 65 65)"/>
                
                <!-- Pétalo inferior -->
                <ellipse cx="50" cy="75" rx="8" ry="15" 
                         fill="url(#petalGradient)" filter="url(#petalGlow)"
                         transform="rotate(180 50 75)"/>
                
                <!-- Pétalo inferior izquierdo -->
                <ellipse cx="35" cy="65" rx="8" ry="15" 
                         fill="url(#petalGradient)" filter="url(#petalGlow)"
                         transform="rotate(225 35 65)"/>
                
                <!-- Pétalo izquierdo -->
                <ellipse cx="25" cy="50" rx="8" ry="15" 
                         fill="url(#petalGradient)" filter="url(#petalGlow)"
                         transform="rotate(270 25 50)"/>
                
                <!-- Pétalo superior izquierdo -->
                <ellipse cx="35" cy="35" rx="8" ry="15" 
                         fill="url(#petalGradient)" filter="url(#petalGlow)"
                         transform="rotate(315 35 35)"/>
                
                <!-- Centro de la flor -->
                <circle cx="50" cy="50" r="12" 
                        fill="url(#centerGradient)" filter="url(#centerShadow)"/>
                
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
        </div>
        
        <div class="brand-text">
          <h1 class="main-title">SEMBRANDO VIDA</h1>
          <p class="subtitle">Administración de app de seguimiento</p>
        </div>
      </div>
      
      <!-- Formulario con efectos glassmorphism -->
      <form @submit.prevent="login" class="login-form">
        <div class="input-group">
          <label for="username">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
            Usuario
          </label>
          <div class="input-container">
            <input 
              v-model="credentials.username"
              type="text" 
              id="username" 
              placeholder="Ingresa tu usuario" 
              required
              :disabled="loading"
            >
            <div class="input-glow"></div>
          </div>
        </div>
        
        <div class="input-group">
          <label for="password">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
              <circle cx="12" cy="16" r="1"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            Contraseña
          </label>
          <div class="input-container">
            <input 
              v-model="credentials.password"
              type="password" 
              id="password" 
              placeholder="Ingresa tu contraseña" 
              required
              :disabled="loading"
            >
            <div class="input-glow"></div>
          </div>
        </div>
        
        <button type="submit" class="login-btn" :disabled="loading">
          <div class="btn-content">
            <span v-if="!loading" class="btn-text">
              <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
                <polyline points="10,17 15,12 10,7"/>
                <line x1="15" y1="12" x2="3" y2="12"/>
              </svg>
              Iniciar Sesión
            </span>
            <span v-else class="loading-content">
              <div class="advanced-spinner">
                <div class="spinner-ring"></div>
                <div class="spinner-ring"></div>
                <div class="spinner-ring"></div>
              </div>
              Iniciando sesión...
            </span>
          </div>
          <div class="btn-liquid-effect"></div>
        </button>
        
        <div v-if="error" class="error-message">
          <svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10"/>
            <line x1="15" y1="9" x2="9" y2="15"/>
            <line x1="9" y1="9" x2="15" y2="15"/>
          </svg>
          {{ error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import authService from '../services/authService'

const router = useRouter()

const credentials = reactive({
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

// Función para generar estilos aleatorios de partículas
const getParticleStyle = (index) => {
  const size = Math.random() * 4 + 2
  const delay = Math.random() * 10
  const duration = Math.random() * 20 + 15
  const left = Math.random() * 100
  const top = Math.random() * 100
  
  return {
    '--size': `${size}px`,
    '--left': `${left}%`,
    '--top': `${top}%`,
    '--delay': `${delay}s`,
    '--duration': `${duration}s`,
  }
}

const login = async () => {
  if (!credentials.username || !credentials.password) {
    error.value = 'Por favor completa todos los campos'
    return
  }
  
  loading.value = true
  error.value = ''
  
  try {
    const result = await authService.login(credentials)
    
    if (result.success) {
      console.log('✅ Login exitoso:', result.user)
      // Redirigir al visor de mapa
      router.push('/visor-map')
    } else {
      error.value = 'Credenciales incorrectas'
    }
  } catch (err) {
    console.error('❌ Error de login:', err)
    if (err.response?.data?.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'No se pudo conectar con el servidor. Verifica tu conexión a internet.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* ===================================
   VARIABLES Y CONFIGURACIÓN BASE
   =================================== */
:root {
  --primary-green: #2e7d32;
  --secondary-green: #4caf50;
  --light-green: #66bb6a;
  --accent-green: #81c784;
  --white: #ffffff;
  --glass-white: rgba(255, 255, 255, 0.95);
  --glass-border: rgba(255, 255, 255, 0.2);
  --shadow-primary: rgba(46, 125, 50, 0.3);
  --shadow-dark: rgba(0, 0, 0, 0.1);
}

/* ===================================
   CONTENEDOR PRINCIPAL
   =================================== */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
  position: relative;
  overflow: hidden;
  font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* ===================================
   FONDO LÍQUIDO CON EFECTOS AVANZADOS
   =================================== */
.liquid-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, 
    #ffffff 0%, 
    #f8fffe 15%, 
    #f0fdf4 30%, 
    #ecfdf5 45%, 
    #d1fae5 60%, 
    #a7f3d0 75%, 
    #86efac 90%, 
    #6ee7b7 100%
  );
  z-index: 0;
}

@keyframes backgroundShift {
  0%, 100% { background-position: 0% 50%; }
  25% { background-position: 100% 50%; }
  50% { background-position: 100% 100%; }
  75% { background-position: 0% 100%; }
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 25% 25%, 
    rgba(167, 243, 208, 0.2) 0%, 
    transparent 70%
  ),
  radial-gradient(circle at 75% 25%, 
    rgba(134, 239, 172, 0.15) 0%, 
    transparent 65%
  ),
  radial-gradient(circle at 25% 75%, 
    rgba(110, 231, 183, 0.12) 0%, 
    transparent 60%
  ),
  radial-gradient(circle at 75% 75%, 
    rgba(74, 222, 128, 0.1) 0%, 
    transparent 55%
  );
}

/* Blobs líquidos mejorados */
.liquid-blob {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(45deg, 
    rgba(255, 255, 255, 0.6) 0%, 
    rgba(248, 255, 254, 0.5) 20%, 
    rgba(240, 253, 244, 0.4) 40%, 
    rgba(236, 253, 245, 0.35) 60%, 
    rgba(209, 250, 229, 0.3) 80%, 
    rgba(167, 243, 208, 0.25) 100%
  );
  backdrop-filter: blur(60px);
  filter: blur(2px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.blob1 {
  width: 350px;
  height: 350px;
  top: -175px;
  left: -175px;
}

.blob2 {
  width: 450px;
  height: 450px;
  top: 40%;
  right: -225px;
}

.blob3 {
  width: 300px;
  height: 300px;
  bottom: -150px;
  left: 30%;
}

.blob4 {
  width: 250px;
  height: 250px;
  top: 15%;
  left: 15%;
  animation-delay: -21s;
  animation-duration: 26s;
}

.blob5 {
  width: 200px;
  height: 200px;
  bottom: 25%;
  right: 25%;
  animation-delay: -28s;
  animation-duration: 24s;
}

.blob6 {
  width: 180px;
  height: 180px;
  top: 60%;
  left: 10%;
  animation-delay: -35s;
  animation-duration: 22s;
}

@keyframes liquidFloat {
  0% {
    transform: translate(0, 0) rotate(0deg) scale(1);
    border-radius: 50%;
  }
  20% {
    transform: translate(60px, -90px) rotate(72deg) scale(1.1);
    border-radius: 45% 55% 40% 60%;
  }
  40% {
    transform: translate(-40px, 80px) rotate(144deg) scale(0.9);
    border-radius: 35% 65% 55% 45%;
  }
  60% {
    transform: translate(-90px, -40px) rotate(216deg) scale(1.05);
    border-radius: 60% 40% 30% 70%;
  }
  80% {
    transform: translate(30px, 70px) rotate(288deg) scale(0.95);
    border-radius: 45% 55% 65% 35%;
  }
  100% {
    transform: translate(0, 0) rotate(360deg) scale(1);
    border-radius: 50%;
  }
}

/* Partículas flotantes */
.floating-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.particle {
  position: absolute;
  width: var(--size);
  height: var(--size);
  background: radial-gradient(circle, 
    rgba(255, 255, 255, 0.9) 0%, 
    rgba(248, 255, 254, 0.7) 25%, 
    rgba(240, 253, 244, 0.6) 50%, 
    rgba(236, 253, 245, 0.4) 75%, 
    rgba(209, 250, 229, 0.3) 90%, 
    transparent 100%
  );
  border-radius: 50%;
  left: var(--left);
  top: var(--top);
  animation: particleFloat var(--duration) ease-in-out infinite;
  animation-delay: var(--delay);
  opacity: 0.8;
  box-shadow: 0 0 8px rgba(167, 243, 208, 0.3);
}

@keyframes particleFloat {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
    opacity: 0.6;
  }
  25% {
    transform: translateY(-30px) rotate(90deg);
    opacity: 0.9;
  }
  50% {
    transform: translateY(-60px) rotate(180deg);
    opacity: 0.8;
  }
  75% {
    transform: translateY(-30px) rotate(270deg);
    opacity: 0.7;
  }
}

/* ===================================
   TARJETA DE LOGIN CON GLASSMORPHISM
   =================================== */
.login-card {
  background: var(--glass-white);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border: 2px solid var(--glass-border);
  border-radius: 20px;
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  padding: 32px;
  width: 100%;
  max-width: 380px;
  position: relative;
  z-index: 10;
  animation: cardFloat 8s ease-in-out infinite alternate;
  overflow: hidden;
}

.login-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    var(--secondary-green) 50%, 
    transparent 100%
  );
  animation: topGlow 3s ease-in-out infinite;
}

@keyframes cardFloat {
  0% {
    transform: translateY(0px) rotate(0deg);
  }
  100% {
    transform: translateY(-15px) rotate(0.5deg);
  }
}

@keyframes topGlow {
  0%, 100% {
    opacity: 0.3;
    transform: scaleX(0.5);
  }
  50% {
    opacity: 1;
    transform: scaleX(1);
  }
}

/* ===================================
   HEADER CON BRANDING
   =================================== */
.login-header {
  text-align: center;
  margin-bottom: 35px;
  position: relative;
}

.logo-container {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo-bg {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.3) 0%, 
    rgba(255, 255, 255, 0.1) 100%
  );
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 25px var(--shadow-primary),
    inset 0 1px 0 rgba(255, 255, 255, 0.4);
  position: relative;
  overflow: hidden;
}

.logo-bg::before {
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
  animation: logoRotate 8s linear infinite;
}

@keyframes logoRotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.logo-icon {
  width: 55px;
  height: 55px;
  position: relative;
  z-index: 1;
  filter: drop-shadow(0 3px 10px var(--shadow-primary));
}

/* Animaciones del logo de flor girando */
.flower-rotating {
  animation: smoothRotation 6s linear infinite;
  transform-origin: 50px 50px;
}

@keyframes smoothRotation {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Sin animaciones individuales de pétalos para evitar conflictos */
.petal {
  opacity: 0.95;
}

/* Animación sutil del centro de la flor */
.flower-center {
  animation: centerPulse 4s ease-in-out infinite;
}

@keyframes centerPulse {
  0%, 100% {
    r: 12;
    opacity: 1;
  }
  50% {
    r: 13;
    opacity: 0.9;
  }
}

/* Animación de los detalles del centro */
.center-detail {
  animation: detailRotate 4s ease-in-out infinite reverse;
}

@keyframes detailRotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Animación del highlight */
.center-highlight {
  animation: highlightShimmer 2.5s ease-in-out infinite;
}

@keyframes highlightShimmer {
  0%, 100% {
    opacity: 0.4;
    r: 3;
  }
  50% {
    opacity: 0.8;
    r: 4;
  }
}

/* Texto del branding */
.brand-text {
  position: relative;
}

.main-title {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 800;
  font-family: 'Poppins', 'Inter', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
  letter-spacing: 1.5px;
  position: relative;
  text-align: center;
  display: block;
  line-height: 1.2;
  white-space: nowrap;
  color: #4ade80;
  background: linear-gradient(
    90deg,
    #4ade80 0%,
    #22c55e 25%,
    #ffffff 50%,
    #22c55e 75%,
    #4ade80 100%
  );
  background-size: 200% 100%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: lightSweep 3s ease-in-out infinite;
  text-shadow: 0 2px 4px rgba(74, 222, 128, 0.3);
  -webkit-text-stroke: 0.5px #15803d;
  text-transform: uppercase;
}

@keyframes titleShine {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

/* Animación de luz que pasa de lado a lado */
@keyframes lightSweep {
  0% {
    background-position: -100% 0%;
  }
  50% {
    background-position: 100% 0%;
  }
  100% {
    background-position: -100% 0%;
  }
}

.subtitle {
  color: var(--secondary-green);
  font-size: 12px;
  font-weight: 500;
  margin: 0;
  opacity: 0.85;
  letter-spacing: 0.3px;
}

/* ===================================
   FORMULARIO CON EFECTOS GLASSMORPHISM
   =================================== */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group {
  position: relative;
}

.input-group label {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--primary-green);
  margin-bottom: 8px;
  font-weight: 600;
  font-size: 12px;
  letter-spacing: 0.3px;
}

.input-icon {
  width: 16px;
  height: 16px;
  stroke-width: 2;
}

.input-container {
  position: relative;
}

.input-container input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid rgba(76, 175, 80, 0.2);
  border-radius: 12px;
  font-size: 14px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  color: var(--primary-green);
  font-weight: 500;
  box-sizing: border-box;
}

.input-container input::placeholder {
  color: rgba(76, 175, 80, 0.5);
  font-weight: 400;
}

.input-container input:focus {
  outline: none;
  border-color: var(--secondary-green);
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 
    0 0 0 4px rgba(76, 175, 80, 0.1),
    0 8px 25px rgba(76, 175, 80, 0.15);
  transform: translateY(-2px);
}

.input-container input:disabled {
  background: rgba(245, 245, 245, 0.6);
  cursor: not-allowed;
  opacity: 0.7;
}

.input-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 14px;
  background: linear-gradient(45deg, 
    transparent 0%, 
    rgba(76, 175, 80, 0.1) 50%, 
    transparent 100%
  );
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.input-container input:focus + .input-glow {
  opacity: 1;
}

/* ===================================
   BOTÓN CON EFECTOS LÍQUIDOS
   =================================== */
.login-btn {
  width: 100%;
  background: linear-gradient(135deg, 
    var(--secondary-green) 0%, 
    var(--primary-green) 100%
  );
  color: var(--white);
  border: none;
  padding: 14px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 6px 20px var(--shadow-primary),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  letter-spacing: 0.4px;
}

.btn-content {
  position: relative;
  z-index: 2;
}

.btn-text, .loading-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.btn-icon {
  width: 20px;
  height: 20px;
  stroke-width: 2.5;
  transition: transform 0.3s ease;
}

.login-btn:hover:not(:disabled) .btn-icon {
  transform: translateX(3px);
}

.btn-liquid-effect {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.3) 50%, 
    transparent 100%
  );
  transition: left 0.6s ease;
  z-index: 1;
}

.login-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, 
    var(--primary-green) 0%, 
    #1b5e20 100%
  );
  transform: translateY(-3px);
  box-shadow: 
    0 12px 35px rgba(46, 125, 50, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.login-btn:hover:not(:disabled) .btn-liquid-effect {
  left: 100%;
}

.login-btn:active:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 
    0 6px 20px rgba(46, 125, 50, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.login-btn:disabled {
  background: linear-gradient(135deg, #cccccc 0%, #aaaaaa 100%);
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Spinner avanzado */
.advanced-spinner {
  position: relative;
  display: inline-block;
  width: 20px;
  height: 20px;
}

.spinner-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 2px solid transparent;
  border-top: 2px solid var(--white);
  border-radius: 50%;
  animation: spinRing 1.2s linear infinite;
}

.spinner-ring:nth-child(1) {
  animation-delay: 0s;
  border-top-color: rgba(255, 255, 255, 1);
}

.spinner-ring:nth-child(2) {
  animation-delay: 0.4s;
  border-top-color: rgba(255, 255, 255, 0.7);
  width: 80%;
  height: 80%;
  top: 10%;
  left: 10%;
}

.spinner-ring:nth-child(3) {
  animation-delay: 0.8s;
  border-top-color: rgba(255, 255, 255, 0.4);
  width: 60%;
  height: 60%;
  top: 20%;
  left: 20%;
}

@keyframes spinRing {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* ===================================
   MENSAJE DE ERROR
   =================================== */
.error-message {
  background: linear-gradient(135deg, 
    rgba(255, 245, 245, 0.95) 0%, 
    rgba(255, 235, 235, 0.9) 100%
  );
  color: #c62828;
  padding: 16px;
  border-radius: 12px;
  text-align: center;
  border: 2px solid rgba(255, 205, 205, 0.6);
  backdrop-filter: blur(20px);
  animation: errorSlideIn 0.5s ease-out;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-weight: 500;
  font-size: 14px;
  box-shadow: 0 4px 15px rgba(198, 40, 40, 0.2);
}

.error-icon {
  width: 20px;
  height: 20px;
  stroke-width: 2;
  flex-shrink: 0;
}

@keyframes errorSlideIn {
  0% {
    opacity: 0;
    transform: translateY(-10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ===================================
   RESPONSIVIDAD AVANZADA
   =================================== */

/* Móviles pequeños */
@media (max-width: 360px) {
  .login-container {
    padding: 10px;
  }
  
  .login-card {
    padding: 25px 20px;
    border-radius: 20px;
  }
  
  .logo-bg {
    width: 70px;
    height: 70px;
  }
  
  .logo-icon {
    width: 55px;
    height: 55px;
  }
  
  .main-title {
    font-size: 22px;
    letter-spacing: 1px;
  }
  
  .subtitle {
    font-size: 13px;
  }
  
  .input-container input {
    padding: 14px 16px;
    font-size: 16px;
  }
  
  .login-btn {
    padding: 16px;
    font-size: 15px;
  }
}

/* Móviles medianos */
@media (max-width: 480px) {
  .login-container {
    padding: 15px;
  }
  
  .login-card {
    padding: 30px 25px;
    max-width: 100%;
  }
  
  .liquid-blob {
    filter: blur(3px);
  }
  
  .blob1, .blob2, .blob3 {
    width: 280px;
    height: 280px;
  }
  
  .blob4, .blob5, .blob6 {
    width: 200px;
    height: 200px;
  }
  
  .main-title {
    font-size: 24px;
  }
  
  .subtitle {
    font-size: 14px;
  }
}

/* Tablets */
@media (min-width: 481px) and (max-width: 768px) {
  .login-card {
    max-width: 460px;
    padding: 45px 35px;
  }
  
  .logo-bg {
    width: 100px;
    height: 100px;
  }
  
  .logo-icon {
    width: 80px;
    height: 80px;
  }
  
  .main-title {
    font-size: 30px;
  }
}

/* Laptops y desktop */
@media (min-width: 769px) and (max-width: 1024px) {
  .login-card {
    max-width: 480px;
  }
}

/* Pantallas grandes y 2K */
@media (min-width: 1025px) {
  .login-card {
    max-width: 420px;
    padding: 38px 35px;
  }
  
  .logo-bg {
    width: 80px;
    height: 80px;
  }
  
  .logo-icon {
    width: 65px;
    height: 65px;
  }
  
  .main-title {
    font-size: 22px;
    letter-spacing: 1.6px;
    margin-bottom: 10px;
    font-weight: 800;
  }
  
  .subtitle {
    font-size: 14px;
  }
}

/* Para pantallas 2K y superiores */
@media (min-width: 1440px) {
  .main-title {
    font-size: 24px;
    letter-spacing: 1.8px;
    font-weight: 800;
    margin-bottom: 12px;
  }
  
  .subtitle {
    font-size: 15px;
    margin-top: 6px;
  }
}

/* Para pantallas 4K y ultra anchas */
@media (min-width: 2560px) {
  .main-title {
    font-size: 26px;
    letter-spacing: 2px;
    font-weight: 800;
    margin-bottom: 15px;
    line-height: 1.1;
    text-shadow: 0 2px 6px rgba(74, 222, 128, 0.4);
  }
  
  .subtitle {
    font-size: 16px;
    margin-top: 8px;
    font-weight: 500;
  }
  
  .login-card {
    max-width: 600px;
    padding: 60px 55px;
  }
}

/* Ajustes para altura de pantalla */
@media (max-height: 700px) {
  .login-container {
    align-items: flex-start;
    padding-top: 30px;
  }
  
  .login-card {
    padding: 30px;
  }
  
  .login-header {
    margin-bottom: 25px;
  }
  
  .logo-bg {
    width: 55px;
    height: 55px;
  }
  
  .logo-icon {
    width: 40px;
    height: 40px;
  }
  
  .main-title {
    font-size: 16px;
    letter-spacing: 0.8px;
    font-weight: 800;
  }
}

@media (max-height: 600px) {
  .login-container {
    padding: 15px;
    padding-top: 20px;
  }
  
  .login-card {
    padding: 25px 20px;
  }
  
  .login-header {
    margin-bottom: 20px;
  }
  
  .login-form {
    gap: 18px;
  }
  
  .input-container input {
    padding: 14px 18px;
  }
  
  .login-btn {
    padding: 16px;
  }
}

/* Modo landscape en móviles */
@media (max-height: 500px) and (orientation: landscape) {
  .login-container {
    padding: 10px;
    justify-content: flex-start;
    align-items: center;
  }
  
  .login-card {
    padding: 20px;
    max-width: 400px;
  }
  
  .logo-bg {
    width: 60px;
    height: 60px;
  }
  
  .logo-icon {
    width: 45px;
    height: 45px;
  }
  
  .main-title {
    font-size: 20px;
    margin-bottom: 5px;
  }
  
  .subtitle {
    font-size: 12px;
  }
  
  .login-header {
    margin-bottom: 15px;
  }
  
  .login-form {
    gap: 15px;
  }
}

/* Modo oscuro (opcional) */
@media (prefers-color-scheme: dark) {
  .login-card {
    background: rgba(30, 30, 30, 0.95);
    border-color: rgba(255, 255, 255, 0.1);
  }
  
  .input-container input {
    background: rgba(50, 50, 50, 0.8);
    color: #e0e0e0;
    border-color: rgba(76, 175, 80, 0.3);
  }
  
  .input-container input::placeholder {
    color: rgba(76, 175, 80, 0.6);
  }
  
  .error-message {
    background: rgba(50, 30, 30, 0.95);
    border-color: rgba(255, 100, 100, 0.3);
    color: #ff6b6b;
  }
}

/* Animaciones de entrada para el componente completo */
@keyframes componentFadeIn {
  0% {
    opacity: 0;
    transform: translateY(30px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Animación pulse lenta similar a Home.vue */
@keyframes animate-pulse-slow {
  0%, 100% {
    opacity: 0.15;
    transform: scale(1);
  }
  50% {
    opacity: 0.25;
    transform: scale(1.05);
  }
}

.animate-pulse-slow {
  animation: animate-pulse-slow 4s ease-in-out infinite;
}

.login-card {
  animation: componentFadeIn 0.8s ease-out;
}

/* Efectos de performance */
.liquid-blob,
.particle,
.logo-bg::before {
  will-change: transform;
}

.input-container input,
.login-btn {
  will-change: transform, box-shadow;
}
</style>
