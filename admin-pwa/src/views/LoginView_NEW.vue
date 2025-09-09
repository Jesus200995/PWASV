<template>
  <div class="login-container">
    <!-- Liquid Glass Background con efectos mejorados -->
    <div class="liquid-background">
      <div class="gradient-overlay"></div>
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
          <!-- Nuevo logo de Sembrando Vida -->
          <div class="logo-bg">
            <svg class="logo-icon" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="leafGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#2e7d32;stop-opacity:1" />
                  <stop offset="30%" style="stop-color:#4caf50;stop-opacity:1" />
                  <stop offset="70%" style="stop-color:#66bb6a;stop-opacity:1" />
                  <stop offset="100%" style="stop-color:#81c784;stop-opacity:1" />
                </linearGradient>
                <linearGradient id="stemGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style="stop-color:#388e3c;stop-opacity:1" />
                  <stop offset="100%" style="stop-color:#2e7d32;stop-opacity:1" />
                </linearGradient>
                <filter id="leafGlow" x="-50%" y="-50%" width="200%" height="200%">
                  <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                  <feMerge> 
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                  </feMerge>
                </filter>
                <filter id="dropShadow" x="-50%" y="-50%" width="200%" height="200%">
                  <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#1b5e20" flood-opacity="0.3"/>
                </filter>
              </defs>
              
              <!-- Tallo principal -->
              <rect class="main-stem" x="57" y="60" width="6" height="50" fill="url(#stemGradient)" rx="3" filter="url(#dropShadow)"/>
              
              <!-- Hojas principales (izquierda) -->
              <path class="leaf leaf-main-left" 
                    d="M60 45 Q30 35 25 55 Q30 75 55 65 Q58 55 60 45" 
                    fill="url(#leafGradient)" 
                    filter="url(#leafGlow)"/>
              
              <!-- Hojas principales (derecha) -->
              <path class="leaf leaf-main-right" 
                    d="M60 45 Q90 35 95 55 Q90 75 65 65 Q62 55 60 45" 
                    fill="url(#leafGradient)" 
                    filter="url(#leafGlow)"/>
              
              <!-- Hojas secundarias (izquierda superior) -->
              <path class="leaf leaf-secondary-left" 
                    d="M58 35 Q40 25 35 40 Q40 55 55 45 Q57 40 58 35" 
                    fill="url(#leafGradient)" 
                    filter="url(#leafGlow)"
                    opacity="0.8"/>
              
              <!-- Hojas secundarias (derecha superior) -->
              <path class="leaf leaf-secondary-right" 
                    d="M62 35 Q80 25 85 40 Q80 55 65 45 Q63 40 62 35" 
                    fill="url(#leafGradient)" 
                    filter="url(#leafGlow)"
                    opacity="0.8"/>
              
              <!-- Hojas pequeñas (izquierda inferior) -->
              <path class="leaf leaf-small-left" 
                    d="M57 55 Q45 50 42 60 Q45 70 55 65 Q56 60 57 55" 
                    fill="url(#leafGradient)" 
                    filter="url(#leafGlow)"
                    opacity="0.7"/>
              
              <!-- Hojas pequeñas (derecha inferior) -->
              <path class="leaf leaf-small-right" 
                    d="M63 55 Q75 50 78 60 Q75 70 65 65 Q64 60 63 55" 
                    fill="url(#leafGradient)" 
                    filter="url(#leafGlow)"
                    opacity="0.7"/>
              
              <!-- Brotes y detalles -->
              <circle class="growth-point point1" cx="60" cy="30" r="2" fill="#81c784" opacity="0.8"/>
              <circle class="growth-point point2" cx="60" cy="115" r="3" fill="#2e7d32"/>
              
              <!-- Nervaduras de las hojas -->
              <path class="vein vein1" d="M35 45 Q50 40 55 50" stroke="#2e7d32" stroke-width="0.5" fill="none" opacity="0.6"/>
              <path class="vein vein2" d="M85 45 Q70 40 65 50" stroke="#2e7d32" stroke-width="0.5" fill="none" opacity="0.6"/>
              <path class="vein vein3" d="M45 35 Q55 32 60 40" stroke="#2e7d32" stroke-width="0.4" fill="none" opacity="0.5"/>
              <path class="vein vein4" d="M75 35 Q65 32 60 40" stroke="#2e7d32" stroke-width="0.4" fill="none" opacity="0.5"/>
              
              <!-- Efectos de luz -->
              <ellipse class="light-effect effect1" cx="35" cy="45" rx="8" ry="4" fill="rgba(255,255,255,0.2)" opacity="0"/>
              <ellipse class="light-effect effect2" cx="85" cy="45" rx="8" ry="4" fill="rgba(255,255,255,0.2)" opacity="0"/>
              <ellipse class="light-effect effect3" cx="60" cy="35" rx="6" ry="3" fill="rgba(255,255,255,0.15)" opacity="0"/>
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
    var(--primary-green) 0%, 
    var(--secondary-green) 30%, 
    var(--light-green) 60%, 
    var(--accent-green) 100%
  );
  background-size: 400% 400%;
  animation: backgroundShift 20s ease infinite;
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
  background: radial-gradient(circle at 30% 20%, 
    rgba(255, 255, 255, 0.1) 0%, 
    transparent 50%
  ),
  radial-gradient(circle at 70% 80%, 
    rgba(255, 255, 255, 0.05) 0%, 
    transparent 50%
  );
}

/* Blobs líquidos mejorados */
.liquid-blob {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(45deg, 
    rgba(255, 255, 255, 0.15) 0%, 
    rgba(255, 255, 255, 0.08) 50%, 
    rgba(255, 255, 255, 0.03) 100%
  );
  backdrop-filter: blur(60px);
  filter: blur(2px);
  animation: liquidFloat 25s ease-in-out infinite;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.blob1 {
  width: 350px;
  height: 350px;
  top: -175px;
  left: -175px;
  animation-delay: 0s;
  animation-duration: 28s;
}

.blob2 {
  width: 450px;
  height: 450px;
  top: 40%;
  right: -225px;
  animation-delay: -7s;
  animation-duration: 32s;
}

.blob3 {
  width: 300px;
  height: 300px;
  bottom: -150px;
  left: 30%;
  animation-delay: -14s;
  animation-duration: 30s;
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
    rgba(255, 255, 255, 0.8) 0%, 
    rgba(255, 255, 255, 0.2) 100%
  );
  border-radius: 50%;
  left: var(--left);
  top: var(--top);
  animation: particleFloat var(--duration) ease-in-out infinite;
  animation-delay: var(--delay);
  opacity: 0.6;
}

@keyframes particleFloat {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
    opacity: 0.3;
  }
  25% {
    transform: translateY(-20px) rotate(90deg);
    opacity: 0.8;
  }
  50% {
    transform: translateY(-40px) rotate(180deg);
    opacity: 0.6;
  }
  75% {
    transform: translateY(-20px) rotate(270deg);
    opacity: 0.4;
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
  border-radius: 24px;
  box-shadow: 
    0 30px 60px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  padding: 40px;
  width: 100%;
  max-width: 440px;
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
  width: 90px;
  height: 90px;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.3) 0%, 
    rgba(255, 255, 255, 0.1) 100%
  );
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 10px 30px var(--shadow-primary),
    inset 0 1px 0 rgba(255, 255, 255, 0.4);
  position: relative;
  overflow: hidden;
  animation: logoFloat 6s ease-in-out infinite;
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

@keyframes logoFloat {
  0%, 100% {
    transform: translateY(0px) scale(1);
  }
  50% {
    transform: translateY(-8px) scale(1.05);
  }
}

@keyframes logoRotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.logo-icon {
  width: 70px;
  height: 70px;
  position: relative;
  z-index: 1;
  filter: drop-shadow(0 4px 12px var(--shadow-primary));
  transition: all 0.3s ease;
}

.logo-icon:hover {
  transform: scale(1.1);
  filter: drop-shadow(0 6px 20px var(--shadow-primary));
}

/* Animaciones del logo de Sembrando Vida */
.main-stem {
  animation: stemGrow 3s ease-in-out infinite alternate;
  transform-origin: center bottom;
}

@keyframes stemGrow {
  0% { transform: scaleY(1); }
  100% { transform: scaleY(1.05); }
}

.leaf {
  animation: leafSway 4s ease-in-out infinite;
  transform-origin: center;
}

.leaf-main-left {
  animation-delay: 0s;
}

.leaf-main-right {
  animation-delay: 0.5s;
}

.leaf-secondary-left {
  animation-delay: 1s;
}

.leaf-secondary-right {
  animation-delay: 1.5s;
}

.leaf-small-left {
  animation-delay: 2s;
}

.leaf-small-right {
  animation-delay: 2.5s;
}

@keyframes leafSway {
  0%, 100% {
    transform: rotate(0deg) scale(1);
  }
  25% {
    transform: rotate(2deg) scale(1.02);
  }
  75% {
    transform: rotate(-2deg) scale(0.98);
  }
}

.growth-point {
  animation: pointPulse 2s ease-in-out infinite;
}

.point1 {
  animation-delay: 0s;
}

.point2 {
  animation-delay: 1s;
}

@keyframes pointPulse {
  0%, 100% {
    r: 2;
    opacity: 0.8;
  }
  50% {
    r: 3;
    opacity: 1;
  }
}

.vein {
  animation: veinFlow 3s ease-in-out infinite;
}

.vein1 { animation-delay: 0s; }
.vein2 { animation-delay: 0.5s; }
.vein3 { animation-delay: 1s; }
.vein4 { animation-delay: 1.5s; }

@keyframes veinFlow {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

.light-effect {
  animation: lightShimmer 4s ease-in-out infinite;
}

.effect1 { animation-delay: 0s; }
.effect2 { animation-delay: 1s; }
.effect3 { animation-delay: 2s; }

@keyframes lightShimmer {
  0%, 80%, 100% { opacity: 0; }
  10%, 70% { opacity: 0.3; }
}

/* Efectos hover para el logo */
.logo-bg:hover .leaf {
  animation-duration: 2s;
}

.logo-bg:hover .light-effect {
  opacity: 0.4 !important;
}

/* Texto del branding */
.brand-text {
  position: relative;
}

.main-title {
  color: var(--primary-green);
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 800;
  letter-spacing: 2px;
  text-shadow: 0 3px 6px rgba(46, 125, 50, 0.2);
  position: relative;
  background: linear-gradient(135deg, 
    var(--primary-green) 0%, 
    var(--secondary-green) 50%, 
    var(--light-green) 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: titleShine 3s ease-in-out infinite;
}

@keyframes titleShine {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.subtitle {
  color: var(--secondary-green);
  font-size: 15px;
  font-weight: 500;
  margin: 0;
  opacity: 0.9;
  letter-spacing: 0.5px;
}

/* ===================================
   FORMULARIO CON EFECTOS GLASSMORPHISM
   =================================== */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.input-group {
  position: relative;
}

.input-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--primary-green);
  margin-bottom: 10px;
  font-weight: 600;
  font-size: 14px;
  letter-spacing: 0.5px;
}

.input-icon {
  width: 18px;
  height: 18px;
  stroke-width: 2;
}

.input-container {
  position: relative;
}

.input-container input {
  width: 100%;
  padding: 16px 20px;
  border: 2px solid rgba(76, 175, 80, 0.2);
  border-radius: 14px;
  font-size: 16px;
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
  padding: 18px;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 8px 25px var(--shadow-primary),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  letter-spacing: 0.5px;
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

/* Pantallas grandes */
@media (min-width: 1025px) {
  .login-card {
    max-width: 500px;
    padding: 50px 45px;
  }
  
  .logo-bg {
    width: 110px;
    height: 110px;
  }
  
  .logo-icon {
    width: 90px;
    height: 90px;
  }
  
  .main-title {
    font-size: 32px;
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
    width: 70px;
    height: 70px;
  }
  
  .logo-icon {
    width: 55px;
    height: 55px;
  }
  
  .main-title {
    font-size: 24px;
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
