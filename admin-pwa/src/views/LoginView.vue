<template>
  <div class="login-container">
    <!-- Liquid Glass Animation Background -->
    <div class="liquid-background">
      <div class="liquid-blob blob1"></div>
      <div class="liquid-blob blob2"></div>
      <div class="liquid-blob blob3"></div>
      <div class="liquid-blob blob4"></div>
      <div class="liquid-blob blob5"></div>
    </div>
    
    <div class="login-card">      <div class="login-header">
        <div class="logo">
          <!-- Icono de localización/ubicación profesional animado -->
          <svg class="professional-icon" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="locationGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#4CAF50;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#66BB6A;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#81C784;stop-opacity:1" />
              </linearGradient>
              <linearGradient id="pinGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#2E7D32;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#4CAF50;stop-opacity:1" />
              </linearGradient>
              <filter id="glow">
                <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                <feMerge> 
                  <feMergeNode in="coloredBlur"/>
                  <feMergeNode in="SourceGraphic"/>
                </feMerge>
              </filter>
              <filter id="shadow">
                <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#2E7D32" flood-opacity="0.3"/>
              </filter>
            </defs>
            
            <!-- Pin de ubicación principal -->
            <path class="location-pin" 
                  d="M50 15 C35 15 25 25 25 40 C25 55 50 80 50 80 C50 80 75 55 75 40 C75 25 65 15 50 15 Z" 
                  fill="url(#locationGradient)" 
                  filter="url(#shadow)"/>
            
            <!-- Círculo interior del pin -->
            <circle class="pin-center" cx="50" cy="40" r="12" fill="url(#pinGradient)"/>
            <circle class="pin-dot" cx="50" cy="40" r="6" fill="#FFFFFF"/>
            
            <!-- Ondas de señal -->
            <circle class="signal-wave wave1" cx="50" cy="40" r="20" fill="none" stroke="#4CAF50" stroke-width="2" opacity="0"/>
            <circle class="signal-wave wave2" cx="50" cy="40" r="25" fill="none" stroke="#66BB6A" stroke-width="1.5" opacity="0"/>
            <circle class="signal-wave wave3" cx="50" cy="40" r="30" fill="none" stroke="#81C784" stroke-width="1" opacity="0"/>
            
            <!-- Puntos de referencia alrededor -->
            <circle class="ref-point point1" cx="20" cy="25" r="2" fill="#4CAF50" opacity="0.6"/>
            <circle class="ref-point point2" cx="80" cy="30" r="1.5" fill="#66BB6A" opacity="0.7"/>
            <circle class="ref-point point3" cx="15" cy="60" r="1.8" fill="#81C784" opacity="0.5"/>
            <circle class="ref-point point4" cx="85" cy="65" r="2.2" fill="#4CAF50" opacity="0.6"/>
            
            <!-- Líneas de conexión sutiles -->
            <line class="connection-line conn1" x1="20" y1="25" x2="38" y2="35" stroke="#4CAF50" stroke-width="0.5" opacity="0.3"/>
            <line class="connection-line conn2" x1="80" y1="30" x2="62" y2="35" stroke="#66BB6A" stroke-width="0.5" opacity="0.3"/>
            <line class="connection-line conn3" x1="15" y1="60" x2="38" y2="45" stroke="#81C784" stroke-width="0.5" opacity="0.3"/>
            <line class="connection-line conn4" x1="85" y1="65" x2="62" y2="45" stroke="#4CAF50" stroke-width="0.5" opacity="0.3"/>
          </svg>
        </div>
        <h1>Panel Administrativo</h1>
        <p>Sembrando Vida - Administración</p>
      </div>
      
      <form @submit.prevent="login" class="login-form">
        <div class="input-group">
          <label for="username">Usuario</label>
          <input 
            v-model="credentials.username"
            type="text" 
            id="username" 
            placeholder="Ingresa tu usuario" 
            required
            :disabled="loading"
          >
        </div>
        
        <div class="input-group">
          <label for="password">Contraseña</label>
          <input 
            v-model="credentials.password"
            type="password" 
            id="password" 
            placeholder="Ingresa tu contraseña" 
            required
            :disabled="loading"
          >
        </div>
        
        <button type="submit" class="login-btn" :disabled="loading">
          <span v-if="!loading">Iniciar Sesión</span>
          <span v-else class="loading-text">
            <div class="spinner"></div>
            Iniciando sesión...
          </span>
        </button>
        
        <div v-if="error" class="error-message">
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
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

/* Liquid Glass Background Animation */
.liquid-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 50%, #66BB6A 100%);
  z-index: 0;
}

.liquid-blob {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(45deg, 
    rgba(76, 175, 80, 0.8) 0%, 
    rgba(102, 187, 106, 0.6) 50%, 
    rgba(129, 199, 132, 0.4) 100%);
  backdrop-filter: blur(40px);
  filter: blur(1px);
  animation: liquidFloat 20s ease-in-out infinite;
}

.blob1 {
  width: 300px;
  height: 300px;
  top: -150px;
  left: -150px;
  animation-delay: 0s;
  animation-duration: 25s;
}

.blob2 {
  width: 400px;
  height: 400px;
  top: 50%;
  right: -200px;
  animation-delay: -5s;
  animation-duration: 30s;
}

.blob3 {
  width: 350px;
  height: 350px;
  bottom: -175px;
  left: 50%;
  transform: translateX(-50%);
  animation-delay: -10s;
  animation-duration: 35s;
}

.blob4 {
  width: 250px;
  height: 250px;
  top: 20%;
  left: 20%;
  animation-delay: -15s;
  animation-duration: 28s;
}

.blob5 {
  width: 200px;
  height: 200px;
  bottom: 20%;
  right: 30%;
  animation-delay: -20s;
  animation-duration: 22s;
}

@keyframes liquidFloat {
  0% {
    transform: translate(0, 0) rotate(0deg) scale(1);
  }
  25% {
    transform: translate(50px, -80px) rotate(90deg) scale(1.1);
  }
  50% {
    transform: translate(-30px, 70px) rotate(180deg) scale(0.9);
  }
  75% {
    transform: translate(-80px, -30px) rotate(270deg) scale(1.05);
  }
  100% {
    transform: translate(0, 0) rotate(360deg) scale(1);
  }
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.1),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  padding: 40px;
  width: 100%;
  max-width: 400px;
  position: relative;
  z-index: 10;
  animation: cardFloat 6s ease-in-out infinite alternate;
}

@keyframes cardFloat {
  0% {
    transform: translateY(0px);
  }
  100% {
    transform: translateY(-10px);
  }
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  margin-bottom: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.professional-icon {
  width: 80px;
  height: 80px;
  animation: iconBounce 3s ease-in-out infinite;
  filter: drop-shadow(0 4px 12px rgba(76, 175, 80, 0.3));
  transition: all 0.3s ease;
}

.professional-icon:hover {
  transform: scale(1.05);
  filter: drop-shadow(0 6px 16px rgba(76, 175, 80, 0.4));
}

/* Animación principal del icono */
@keyframes iconBounce {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-8px);
  }
}

/* Animación del pin de ubicación */
.location-pin {
  animation: pinPulse 2.5s ease-in-out infinite;
  transform-origin: 50px 40px;
}

@keyframes pinPulse {
  0%, 100% {
    transform: scale(1);
    filter: url(#shadow) brightness(1);
  }
  50% {
    transform: scale(1.05);
    filter: url(#shadow) brightness(1.1);
  }
}

/* Animación del centro del pin */
.pin-center {
  animation: centerGlow 2s ease-in-out infinite alternate;
}

@keyframes centerGlow {
  0% {
    r: 12;
    opacity: 1;
  }
  100% {
    r: 14;
    opacity: 0.8;
  }
}

/* Animación del punto central */
.pin-dot {
  animation: dotPulse 1.5s ease-in-out infinite;
}

@keyframes dotPulse {
  0%, 100% {
    r: 6;
    opacity: 1;
  }
  50% {
    r: 4;
    opacity: 0.7;
  }
}

/* Animaciones de las ondas de señal */
.signal-wave {
  animation: signalRipple 3s ease-out infinite;
}

.wave1 {
  animation-delay: 0s;
}

.wave2 {
  animation-delay: 1s;
}

.wave3 {
  animation-delay: 2s;
}

@keyframes signalRipple {
  0% {
    r: 15;
    opacity: 0.8;
    stroke-width: 3;
  }
  50% {
    opacity: 0.4;
    stroke-width: 2;
  }
  100% {
    r: 35;
    opacity: 0;
    stroke-width: 0.5;
  }
}

/* Animación de los puntos de referencia */
.ref-point {
  animation: pointTwinkle 4s ease-in-out infinite;
}

.point1 {
  animation-delay: 0s;
}

.point2 {
  animation-delay: 1s;
}

.point3 {
  animation-delay: 2s;
}

.point4 {
  animation-delay: 3s;
}

@keyframes pointTwinkle {
  0%, 80%, 100% {
    opacity: 0.3;
    r: 1.5;
  }
  20% {
    opacity: 1;
    r: 3;
  }
}

/* Animación de las líneas de conexión */
.connection-line {
  animation: connectionFade 5s ease-in-out infinite;
  stroke-dasharray: 5, 3;
}

.conn1 {
  animation-delay: 0s;
}

.conn2 {
  animation-delay: 1.25s;
}

.conn3 {
  animation-delay: 2.5s;
}

.conn4 {
  animation-delay: 3.75s;
}

@keyframes connectionFade {
  0%, 90% {
    opacity: 0.1;
    stroke-dashoffset: 0;
  }
  10%, 80% {
    opacity: 0.6;
    stroke-dashoffset: 8;
  }
}

/* Efecto hover especial para el pin */
.professional-icon:hover .location-pin {
  animation: pinHover 0.6s ease-in-out;
}

@keyframes pinHover {
  0%, 100% {
    transform: scale(1) rotate(0deg);
  }
  25% {
    transform: scale(1.1) rotate(-2deg);
  }
  75% {
    transform: scale(1.1) rotate(2deg);
  }
}

/* Efecto hover para las ondas */
.professional-icon:hover .signal-wave {
  animation: signalBoost 1s ease-out;
}

@keyframes signalBoost {
  0% {
    opacity: 0;
    r: 15;
  }
  50% {
    opacity: 1;
    r: 25;
  }
  100% {
    opacity: 0;
    r: 40;
  }
}

.login-header h1 {
  color: #2E7D32;
  margin-bottom: 8px;
  font-size: 24px;
  font-weight: 700;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.login-header p {
  color: #4CAF50;
  font-size: 14px;
  font-weight: 500;
}

.input-group {
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  color: #2E7D32;
  margin-bottom: 8px;
  font-weight: 600;
}

.input-group input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid rgba(76, 175, 80, 0.3);
  border-radius: 12px;
  font-size: 16px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.input-group input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
  background: rgba(255, 255, 255, 1);
}

.input-group input:disabled {
  background-color: rgba(245, 245, 245, 0.8);
  cursor: not-allowed;
}

.login-btn {
  width: 100%;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  border: none;
  padding: 14px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
  position: relative;
  overflow: hidden;
}

.login-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.login-btn:hover:not(:disabled)::before {
  left: 100%;
}

.login-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #45a049 0%, #388e3c 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.login-btn:disabled {
  background: linear-gradient(135deg, #cccccc 0%, #aaaaaa 100%);
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.loading-text {
  display: flex;
  align-items: center;
  gap: 8px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  background: rgba(255, 238, 238, 0.9);
  color: #c33;
  padding: 12px;
  border-radius: 12px;
  margin-top: 16px;
  text-align: center;
  border: 1px solid rgba(255, 204, 204, 0.5);
  backdrop-filter: blur(10px);
  animation: errorShake 0.5s ease-in-out;
}

@keyframes errorShake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .login-container {
    padding: 10px;
  }
  
  .login-card {
    padding: 30px 20px;
  }
  
  .liquid-blob {
    filter: blur(2px);
  }
  
  .blob1, .blob2, .blob3 {
    width: 250px;
    height: 250px;
  }
  
  .blob4, .blob5 {
    width: 180px;
    height: 180px;
  }
}
</style>
