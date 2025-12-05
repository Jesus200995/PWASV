<template>
  <div class="login-page">
    <!-- Fondo con patrón geométrico y gradiente -->
    <div class="background-layer">
      <div class="gradient-base"></div>
      <div class="geometric-pattern"></div>
      <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
        <div class="shape shape-4"></div>
        <div class="shape shape-5"></div>
      </div>
      <div class="glow-orbs">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
      </div>
    </div>

    <!-- Tarjeta de Login -->
    <div class="login-wrapper">
      <div class="login-card">
        <!-- Logo y Branding -->
        <div class="brand-section">
          <div class="logo-wrapper">
            <div class="logo-ring">
              <div class="ring-inner"></div>
            </div>
            <div class="logo-icon-container">
              <svg class="logo-svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <defs>
                  <filter id="neonGlow" x="-50%" y="-50%" width="200%" height="200%">
                    <feGaussianBlur stdDeviation="2" result="blur1"/>
                    <feGaussianBlur stdDeviation="4" result="blur2"/>
                    <feMerge>
                      <feMergeNode in="blur2"/>
                      <feMergeNode in="blur1"/>
                      <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                  </filter>
                </defs>
                <!-- Hoja con contorno neón -->
                <path 
                  d="M50 15 C30 25, 20 45, 25 65 C30 80, 45 85, 50 85 C55 85, 70 80, 75 65 C80 45, 70 25, 50 15" 
                  fill="none" 
                  stroke="#ffffff" 
                  stroke-width="2.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  filter="url(#neonGlow)"
                  class="leaf-outline"/>
                <!-- Nervadura central neón -->
                <path 
                  d="M50 22 L50 78" 
                  stroke="#ffffff" 
                  stroke-width="1.5" 
                  fill="none"
                  stroke-linecap="round"
                  filter="url(#neonGlow)"
                  class="leaf-vein"/>
                <!-- Nervaduras laterales neón -->
                <path 
                  d="M50 32 L38 42 M50 44 L34 56 M50 56 L36 66" 
                  stroke="#ffffff" 
                  stroke-width="1.2" 
                  fill="none"
                  stroke-linecap="round"
                  filter="url(#neonGlow)"
                  class="leaf-veins-left"/>
                <path 
                  d="M50 32 L62 42 M50 44 L66 56 M50 56 L64 66" 
                  stroke="#ffffff" 
                  stroke-width="1.2" 
                  fill="none"
                  stroke-linecap="round"
                  filter="url(#neonGlow)"
                  class="leaf-veins-right"/>
              </svg>
            </div>
          </div>
          
          <h1 class="brand-title">SEMBRANDO VIDA</h1>
          <p class="brand-subtitle">Administración de Seguimiento y Monitoreo</p>
        </div>

        <!-- Formulario -->
        <form @submit.prevent="login" class="login-form">
          <div class="form-group">
            <label for="username" class="form-label">
              <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
              Usuario
            </label>
            <div class="input-wrapper">
              <input 
                v-model="credentials.username"
                type="text" 
                id="username" 
                placeholder="Ingresa tu usuario"
                autocomplete="username"
                required
                :disabled="loading"
              >
              <div class="input-focus-ring"></div>
            </div>
          </div>

          <div class="form-group">
            <label for="password" class="form-label">
              <svg class="label-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <circle cx="12" cy="16" r="1"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
              Contraseña
            </label>
            <div class="input-wrapper">
              <input 
                v-model="credentials.password"
                :type="showPassword ? 'text' : 'password'" 
                id="password" 
                placeholder="Ingresa tu contraseña"
                autocomplete="current-password"
                required
                :disabled="loading"
              >
              <button 
                type="button" 
                class="toggle-password"
                @click="showPassword = !showPassword"
                :disabled="loading"
              >
                <svg v-if="!showPassword" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                  <line x1="1" y1="1" x2="23" y2="23"/>
                </svg>
              </button>
              <div class="input-focus-ring"></div>
            </div>
          </div>

          <button type="submit" class="submit-btn" :disabled="loading">
            <span v-if="!loading" class="btn-content">
              <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
                <polyline points="10 17 15 12 10 7"/>
                <line x1="15" y1="12" x2="3" y2="12"/>
              </svg>
              Iniciar Sesión
            </span>
            <span v-else class="btn-loading">
              <div class="spinner"></div>
              Verificando...
            </span>
          </button>

          <!-- Mensaje de error -->
          <transition name="error-fade">
            <div v-if="error" class="error-alert">
              <svg class="error-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              <span>{{ error }}</span>
            </div>
          </transition>
        </form>

        <!-- Footer -->
        <div class="card-footer">
          <p>© 2025 Sembrando Vida</p>
        </div>
      </div>
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
const showPassword = ref(false)

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
      router.push('/visor-map')
    } else {
      error.value = 'Credenciales incorrectas'
    }
  } catch (err) {
    console.error('❌ Error de login:', err)
    if (err.response?.data?.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'No se pudo conectar con el servidor'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* ========================================
   FORZAR MODO CLARO - NO DARK MODE
   ======================================== */
.login-page,
.login-page * {
  color-scheme: light only !important;
}

/* ========================================
   VARIABLES
   ======================================== */
.login-page {
  --green-50: #ecfdf5;
  --green-100: #d1fae5;
  --green-200: #a7f3d0;
  --green-300: #6ee7b7;
  --green-400: #34d399;
  --green-500: #10b981;
  --green-600: #059669;
  --green-700: #047857;
  --green-800: #065f46;
  --green-900: #064e3b;
  
  --white: #ffffff;
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
  
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-md: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 20px 25px -5px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);
}

/* ========================================
   CONTENEDOR PRINCIPAL
   ======================================== */
.login-page {
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
  font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
  background: url('https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=1920&q=80') center/cover no-repeat fixed;
}

/* ========================================
   FONDO ANIMADO
   ======================================== */
.background-layer {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.gradient-base {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, 
    rgba(6, 78, 59, 0.85) 0%,
    rgba(5, 150, 105, 0.7) 50%,
    rgba(6, 78, 59, 0.85) 100%
  );
}

@keyframes gradientMove {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.geometric-pattern {
  position: absolute;
  inset: 0;
  background-image: 
    radial-gradient(circle at 25% 25%, rgba(255,255,255,0.1) 2px, transparent 2px),
    radial-gradient(circle at 75% 75%, rgba(255,255,255,0.08) 2px, transparent 2px);
  background-size: 60px 60px;
  opacity: 0.6;
}

/* Formas flotantes */
.floating-shapes {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
  backdrop-filter: blur(2px);
}

.shape-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  left: -100px;
  animation: float1 20s ease-in-out infinite;
}

.shape-2 {
  width: 200px;
  height: 200px;
  top: 20%;
  right: -50px;
  animation: float2 18s ease-in-out infinite;
}

.shape-3 {
  width: 150px;
  height: 150px;
  bottom: 10%;
  left: 10%;
  animation: float3 22s ease-in-out infinite;
}

.shape-4 {
  width: 100px;
  height: 100px;
  top: 60%;
  right: 20%;
  animation: float1 16s ease-in-out infinite reverse;
}

.shape-5 {
  width: 180px;
  height: 180px;
  bottom: -50px;
  right: 30%;
  animation: float2 24s ease-in-out infinite;
}

@keyframes float1 {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  25% { transform: translate(30px, -30px) rotate(90deg); }
  50% { transform: translate(0, -50px) rotate(180deg); }
  75% { transform: translate(-30px, -20px) rotate(270deg); }
}

@keyframes float2 {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(-20px, 30px) scale(1.1); }
  66% { transform: translate(20px, -20px) scale(0.9); }
}

@keyframes float3 {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-40px); }
}

/* Orbes de brillo */
.glow-orbs {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: var(--green-400);
  opacity: 0.3;
  top: -100px;
  left: -100px;
  animation: orbPulse 8s ease-in-out infinite;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: var(--green-300);
  opacity: 0.25;
  bottom: -50px;
  right: -50px;
  animation: orbPulse 10s ease-in-out infinite 2s;
}

.orb-3 {
  width: 250px;
  height: 250px;
  background: var(--green-200);
  opacity: 0.2;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: orbPulse 12s ease-in-out infinite 4s;
}

@keyframes orbPulse {
  0%, 100% { opacity: 0.2; transform: scale(1); }
  50% { opacity: 0.35; transform: scale(1.1); }
}

/* ========================================
   WRAPPER Y TARJETA
   ======================================== */
.login-wrapper {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 420px;
  animation: cardEntry 0.6s ease-out;
}

@keyframes cardEntry {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.login-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 32px;
  padding: 40px 36px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.3),
    inset 0 1px 1px rgba(255, 255, 255, 0.4),
    inset 0 -1px 1px rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.25);
  position: relative;
  overflow: hidden;
}

/* Efecto de brillo líquido */
.login-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -50%;
  width: 200%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  transform: skewX(-20deg);
  animation: liquidShine 4s ease-in-out infinite;
  pointer-events: none;
}

@keyframes liquidShine {
  0%, 100% { left: -50%; opacity: 0; }
  50% { left: 50%; opacity: 1; }
}

/* Decoración superior - OCULTA */
.card-decoration {
  display: none;
}

.decoration-line {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent);
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  to { left: 100%; }
}

/* ========================================
   BRANDING / LOGO
   ======================================== */
.brand-section {
  text-align: center;
  margin-bottom: 32px;
}

.logo-wrapper {
  position: relative;
  width: 90px;
  height: 90px;
  margin: 0 auto 20px;
}

.logo-ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 3px solid rgba(134, 239, 172, 0.5);
  animation: ringRotate 10s linear infinite;
}

.logo-ring::before {
  content: '';
  position: absolute;
  top: -6px;
  left: 50%;
  transform: translateX(-50%);
  width: 12px;
  height: 12px;
  background: #86efac;
  border-radius: 50%;
  box-shadow: 
    0 0 6px var(--green-400),
    0 0 12px var(--green-400),
    0 0 20px var(--green-300);
  animation: locationPulse 2s ease-in-out infinite;
}

.logo-ring::after {
  content: '';
  position: absolute;
  top: -16px;
  left: 50%;
  transform: translateX(-50%);
  width: 32px;
  height: 32px;
  background: radial-gradient(circle, var(--green-400) 0%, var(--green-300) 30%, transparent 70%);
  border-radius: 50%;
  opacity: 0;
  animation: locationGlow 2s ease-out infinite;
}

@keyframes locationPulse {
  0%, 100% {
    transform: translateX(-50%) scale(1);
    box-shadow: 
      0 0 6px var(--green-400),
      0 0 12px var(--green-400),
      0 0 20px var(--green-300);
    opacity: 1;
  }
  50% {
    transform: translateX(-50%) scale(1.2);
    box-shadow: 
      0 0 10px var(--green-300),
      0 0 20px var(--green-300),
      0 0 30px var(--green-200);
    opacity: 0.8;
  }
}

@keyframes locationGlow {
  0% {
    transform: translateX(-50%) scale(0.3);
    opacity: 0.6;
  }
  100% {
    transform: translateX(-50%) scale(2);
    opacity: 0;
  }
}

.ring-inner {
  position: absolute;
  inset: 8px;
  border-radius: 50%;
  border: 2px dashed rgba(134, 239, 172, 0.5);
  opacity: 0.7;
  animation: ringRotate 15s linear infinite reverse;
}

@keyframes ringRotate {
  to { transform: rotate(360deg); }
}

.logo-icon-container {
  position: absolute;
  inset: 15px;
  background: transparent;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-svg {
  width: 45px;
  height: 45px;
}

/* Animaciones de la hoja neón */
.leaf-outline {
  animation: leafPulse 3s ease-in-out infinite, leafSway 4s ease-in-out infinite;
  transform-origin: 50px 85px;
}

.leaf-vein {
  animation: veinPulse 3s ease-in-out infinite 0.2s;
}

.leaf-veins-left,
.leaf-veins-right {
  animation: veinPulse 3s ease-in-out infinite 0.4s;
}

@keyframes leafPulse {
  0%, 100% { 
    stroke: #10b981;
    filter: url(#neonGlow) drop-shadow(0 0 4px #10b981);
  }
  50% { 
    stroke: #34d399;
    filter: url(#neonGlow) drop-shadow(0 0 8px #34d399);
  }
}

@keyframes veinPulse {
  0%, 100% { 
    opacity: 0.7;
    stroke: #10b981;
  }
  50% { 
    opacity: 1;
    stroke: #6ee7b7;
  }
}

@keyframes leafSway {
  0%, 100% { transform: rotate(-2deg); }
  50% { transform: rotate(2deg); }
}

.brand-title {
  font-size: 18px;
  font-weight: 600;
  background: linear-gradient(90deg, 
    #86efac 0%,
    #86efac 35%,
    #ffffff 50%,
    #86efac 65%,
    #86efac 100%
  );
  background-size: 200% 100%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 1px;
  margin: 0 0 8px 0;
  text-transform: uppercase;
  font-family: 'Poppins', 'Segoe UI', sans-serif;
  animation: shimmerText 1.5s ease-in-out infinite;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

@keyframes shimmerText {
  0% { background-position: 100% 50%; }
  100% { background-position: -100% 50%; }
}

.brand-subtitle {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
  font-weight: 500;
  letter-spacing: 0.5px;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

/* ========================================
   FORMULARIO
   ======================================== */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.95);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.label-icon {
  width: 16px;
  height: 16px;
  color: #86efac;
}

.input-wrapper {
  position: relative;
}

.input-wrapper input {
  width: 100%;
  padding: 14px 16px;
  padding-right: 48px;
  font-size: 15px;
  font-weight: 500;
  color: #ffffff;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  outline: none;
  transition: all 0.3s ease;
  box-sizing: border-box;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.input-wrapper input::placeholder {
  color: rgba(255, 255, 255, 0.5);
  font-weight: 400;
}

.input-wrapper input:focus {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(134, 239, 172, 0.6);
  box-shadow: 0 0 20px rgba(134, 239, 172, 0.3);
}

.input-wrapper input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.input-focus-ring {
  position: absolute;
  inset: -2px;
  border-radius: 14px;
  background: linear-gradient(135deg, var(--green-400), var(--green-600));
  opacity: 0;
  z-index: -1;
  transition: opacity 0.3s ease;
}

.input-wrapper input:focus ~ .input-focus-ring {
  opacity: 0.1;
}

/* Toggle password */
.toggle-password {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.6);
  transition: color 0.2s ease;
  padding: 0;
}

.toggle-password:hover:not(:disabled) {
  color: #86efac;
}

.toggle-password:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.toggle-password svg {
  width: 20px;
  height: 20px;
}

/* ========================================
   BOTÓN SUBMIT
   ======================================== */
.submit-btn {
  width: 100%;
  padding: 16px 24px;
  margin-top: 8px;
  font-size: 15px;
  font-weight: 700;
  color: var(--white);
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.8) 0%, rgba(5, 150, 105, 0.9) 100%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.submit-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s ease;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(16, 185, 129, 0.4);
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.9) 0%, rgba(5, 150, 105, 1) 100%);
}

.submit-btn:hover:not(:disabled)::before {
  left: 100%;
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  background: var(--gray-400);
  cursor: not-allowed;
  box-shadow: none;
}

.btn-content,
.btn-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.btn-icon {
  width: 20px;
  height: 20px;
  transition: transform 0.3s ease;
}

.submit-btn:hover:not(:disabled) .btn-icon {
  transform: translateX(4px);
}

/* Spinner */
.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255,255,255,0.3);
  border-top-color: var(--white);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ========================================
   MENSAJE DE ERROR
   ======================================== */
.error-alert {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: linear-gradient(135deg, #fef2f2, #fee2e2);
  border: 1px solid #fecaca;
  border-radius: 12px;
  color: #dc2626;
  font-size: 14px;
  font-weight: 500;
}

.error-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.error-fade-enter-active,
.error-fade-leave-active {
  transition: all 0.3s ease;
}

.error-fade-enter-from,
.error-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* ========================================
   FOOTER
   ======================================== */
.card-footer {
  text-align: center;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.card-footer p {
  margin: 0;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.7);
}

/* ========================================
   RESPONSIVO
   ======================================== */

/* Móviles pequeños */
@media (max-width: 380px) {
  .login-page {
    padding: 16px;
  }
  
  .login-card {
    padding: 32px 24px;
    border-radius: 20px;
  }
  
  .logo-wrapper {
    width: 75px;
    height: 75px;
  }
  
  .logo-svg {
    width: 38px;
    height: 38px;
  }
  
  .brand-title {
    font-size: 18px;
    letter-spacing: 1.5px;
  }
  
  .brand-subtitle {
    font-size: 12px;
  }
  
  .input-wrapper input {
    padding: 12px 14px;
    padding-right: 44px;
    font-size: 14px;
  }
  
  .submit-btn {
    padding: 14px 20px;
    font-size: 14px;
  }
}

/* Tablets */
@media (min-width: 481px) and (max-width: 768px) {
  .login-card {
    padding: 48px 44px;
  }
  
  .logo-wrapper {
    width: 100px;
    height: 100px;
  }
  
  .logo-svg {
    width: 50px;
    height: 50px;
  }
  
  .brand-title {
    font-size: 26px;
  }
}

/* Desktop */
@media (min-width: 769px) {
  .login-card {
    padding: 48px 44px;
  }
}

/* Altura pequeña */
@media (max-height: 700px) {
  .login-page {
    padding: 16px;
    align-items: flex-start;
    padding-top: 5vh;
  }
  
  .login-card {
    padding: 28px 32px;
  }
  
  .brand-section {
    margin-bottom: 24px;
  }
  
  .logo-wrapper {
    width: 70px;
    height: 70px;
    margin-bottom: 16px;
  }
  
  .login-form {
    gap: 16px;
  }
}

/* Landscape en móviles */
@media (max-height: 500px) and (orientation: landscape) {
  .login-page {
    padding: 12px;
  }
  
  .login-card {
    padding: 20px 28px;
    max-width: 380px;
  }
  
  .logo-wrapper {
    width: 55px;
    height: 55px;
    margin-bottom: 12px;
  }
  
  .logo-svg {
    width: 30px;
    height: 30px;
  }
  
  .brand-title {
    font-size: 16px;
    margin-bottom: 4px;
  }
  
  .brand-subtitle {
    font-size: 11px;
  }
  
  .brand-section {
    margin-bottom: 16px;
  }
  
  .login-form {
    gap: 12px;
  }
  
  .form-group {
    gap: 4px;
  }
  
  .input-wrapper input {
    padding: 10px 14px;
  }
  
  .submit-btn {
    padding: 12px 20px;
  }
  
  .card-footer {
    margin-top: 12px;
    padding-top: 12px;
  }
}
</style>