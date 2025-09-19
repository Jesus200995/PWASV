<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-emerald-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-teal-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>
    
    <div class="page-container w-full max-w-md relative z-10 px-2">
      <!-- Header Section Compacto -->
      <div class="text-center mb-4">
        <div class="w-32 h-32 sm:w-36 sm:h-36 md:w-40 md:h-40 mx-auto -mb-6">
          <img 
            src="/src/images/icono.png" 
            alt="Sembrando Vida Logo" 
            class="w-full h-full object-contain rounded-full"
          />
        </div>
        <h1 class="text-lg font-semibold mb-1 text-center modern-title">Aplicación de Seguimiento</h1>
        <div class="green-line mx-auto mb-2"></div>
        <h2 class="text-base font-semibold text-gray-700">Iniciar sesión</h2>
        <p class="mt-1 text-gray-500 text-xs">Ingresa tus credenciales para acceder</p>
      </div>

      <!-- Error Message -->
      <transition name="bounce">
        <div v-if="errorMessage" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg shadow-sm mb-4" role="alert">
          <p class="flex items-center text-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            {{ errorMessage }}
          </p>
        </div>
      </transition>

      <!-- Login Form -->
      <div class="glass-card">
        <form @submit.prevent="login">
          <div class="space-y-3">
            <div>
              <label for="email" class="block text-xs font-medium text-gray-800 mb-1">Correo electrónico</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                </div>
                <input 
                  v-model="email" 
                  id="email" 
                  name="email" 
                  type="email" 
                  autocomplete="email" 
                  required 
                  class="glass-input w-full pl-9 pr-4 py-2" 
                  placeholder="nombre@ejemplo.com" 
                  :class="{ 'animate-shake': formError }" 
                />
              </div>
            </div>
            
            <div>
              <label for="password" class="block text-xs font-medium text-gray-800 mb-1">Contraseña</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <input 
                  v-model="password" 
                  id="password" 
                  name="password" 
                  :type="showPassword ? 'text' : 'password'" 
                  autocomplete="current-password" 
                  required 
                  class="glass-input w-full pl-9 pr-9 py-2" 
                  placeholder="••••••••" 
                  :class="{ 'animate-shake': formError }" 
                />
                <button
                  type="button"
                  @click="togglePasswordVisibility"
                  class="absolute inset-y-0 right-0 flex items-center pr-3 text-primary hover:text-primary-dark focus:outline-none transition-colors duration-200"
                >
                  <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <button 
            type="submit" 
            :disabled="loading" 
            class="glass-button w-full mt-4 flex items-center justify-center"
            :class="{ 'opacity-50 cursor-not-allowed': loading }"
          >
            <svg v-if="loading" class="animate-spin h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ loading ? 'Iniciando sesión...' : 'Iniciar sesión' }}</span>
          </button>
        </form>

        <!-- Register Link -->
        <div class="text-center mt-4">
          <p class="text-xs text-gray-700">
            ¿No tienes cuenta?
            <router-link to="/register" class="font-medium text-primary hover:text-primary-dark transition-colors duration-200 glass-link">
              Crear cuenta
            </router-link>
          </p>
          <p class="text-xs text-gray-700 mt-1">
            <router-link to="/forgot-password" class="font-medium text-primary hover:text-primary-dark transition-colors duration-200 glass-link">
              ¿Olvidaste tu contraseña?
            </router-link>
          </p>
        </div>
      </div>
    </div>
    
    <!-- Componente de soporte específico para login -->
    <SupportBubbleLogin />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { API_URL, getBestApiUrl, checkInternetConnection, getOfflineMessage } from '../utils/network.js';
import SupportBubbleLogin from '../components/SupportBubbleLogin.vue';

const router = useRouter();
const email = ref('');
const password = ref('');
const showPassword = ref(false);
const loading = ref(false);
const errorMessage = ref('');
const formError = ref(false);
const isOnline = ref(true);
const currentApiUrl = ref(API_URL);

// Verificar conexión a internet cuando carga el componente
onMounted(async () => {
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    errorMessage.value = getOfflineMessage();
  } else {
    try {
      currentApiUrl.value = await getBestApiUrl();
      console.log(`🌐 Login usando servidor: ${currentApiUrl.value}`);
    } catch (error) {
      console.warn('Error detectando servidor, usando URL por defecto:', error);
      currentApiUrl.value = API_URL;
    }
  }
});

function togglePasswordVisibility() {
  showPassword.value = !showPassword.value;
}

async function login() {
  loading.value = true;
  errorMessage.value = '';
  formError.value = false;
  
  // Verificar si hay campos vacíos
  if (!email.value || !password.value) {
    errorMessage.value = 'Por favor, completa todos los campos';
    formError.value = true;
    loading.value = false;
    return;
  }
  
  // Verificar conexión a internet
  const online = await checkInternetConnection();
  if (!online) {
    errorMessage.value = getOfflineMessage();
    formError.value = true;
    loading.value = false;
    return;
  }
  
  // Actualizar URL si es necesario
  if (!currentApiUrl.value || currentApiUrl.value === API_URL) {
    currentApiUrl.value = await getBestApiUrl();
  }
  
  try {
    // Conectar con la API real
    const response = await axios.post(`${currentApiUrl.value}/login`, {
      correo: email.value,
      contrasena: password.value
    }, {
      timeout: 10000, // 10 segundos de timeout
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    // Obtener datos del usuario desde la respuesta
    const userData = response.data;
    
    // Guardar datos del usuario en localStorage
    localStorage.setItem('user', JSON.stringify(userData));
    
    // Establecer bandera para mostrar mensaje de bienvenida
    sessionStorage.setItem('justLoggedIn', 'true');
    
    // Forzar recarga de la página para asegurar que el estado se actualice correctamente
    window.location.href = '/';
  } catch (error) {
    console.error('Error de inicio de sesión:', error);
    
    if (error.response) {
      // El servidor respondió con un estado de error
      const status = error.response.status;
      if (status === 401) {
        errorMessage.value = 'Credenciales incorrectas. Verifica tu email y contraseña.';
      } else if (status === 500) {
        errorMessage.value = 'Error del servidor. Inténtalo de nuevo en unos minutos.';
      } else {
        errorMessage.value = error.response.data.detail || 'Error al iniciar sesión. Verifica tus credenciales.';
      }
    } else if (error.request) {
      // La solicitud fue hecha pero no se recibió respuesta
      errorMessage.value = 'No se pudo conectar con el servidor. Verifica tu conexión a internet.';
    } else if (error.code === 'ECONNABORTED') {
      // Timeout
      errorMessage.value = 'La conexión tardó demasiado. Verifica tu conexión a internet.';
    } else {
      // Algo ocurrió al configurar la solicitud
      errorMessage.value = 'Error al iniciar sesión: ' + error.message;
    }
    
    formError.value = true;
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.bounce-enter-active {
  animation: bounce-in 0.5s;
}
.bounce-leave-active {
  animation: bounce-in 0.5s reverse;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.5;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
  20%, 40%, 60%, 80% { transform: translateX(5px); }
}

.animate-shake {
  animation: shake 0.6s cubic-bezier(.36,.07,.19,.97) both;
}

/* Efecto de vidrio realista - Glassmorphism */
.glass-card {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 8px 32px 0 rgba(31, 38, 135, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  padding: 1.25rem;
  position: relative;
  overflow: hidden;
}

.glass-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -50%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  transform: skewX(-25deg);
  transition: all 0.6s;
}

.glass-card:hover::before {
  left: 150%;
}

.glass-input {
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  font-size: 0.875rem;
  color: #1f2937;
  transition: all 0.3s ease;
  box-shadow: 
    0 4px 16px 0 rgba(31, 38, 135, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  min-height: 36px;
}

.glass-input:focus {
  outline: none;
  border: 1px solid rgba(76, 175, 80, 0.4);
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 0 0 3px rgba(76, 175, 80, 0.1),
    0 8px 25px 0 rgba(31, 38, 135, 0.15),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

.glass-input::placeholder {
  color: rgba(75, 85, 99, 0.6);
}

/* Estilos para los iconos y botones dentro de los inputs */
.relative .absolute {
  z-index: 10;
}

.relative .absolute svg {
  width: 1rem;
  height: 1rem;
}

/* Estilos específicos para el botón del ojo */
button[type="button"] {
  background: transparent !important;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
  min-height: 36px;
  transition: all 0.2s ease;
  box-shadow: none !important;
}

button[type="button"]:focus {
  outline: none;
  background: transparent !important;
  box-shadow: none !important;
}

button[type="button"]:hover {
  background: transparent !important;
  box-shadow: none !important;
}

button[type="button"] svg {
  transition: all 0.2s ease;
}

button[type="button"]:hover svg {
  transform: scale(1.1);
}

.glass-button {
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(76, 175, 80, 0.3);
  background: linear-gradient(135deg, 
    rgba(76, 175, 80, 0.8) 0%, 
    rgba(56, 142, 60, 0.8) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 20px 0 rgba(76, 175, 80, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.glass-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 30px 0 rgba(76, 175, 80, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
  background: linear-gradient(135deg, 
    rgba(76, 175, 80, 0.9) 0%, 
    rgba(56, 142, 60, 0.9) 100%);
}

.glass-button:active:not(:disabled) {
  transform: translateY(0px);
  box-shadow: 
    0 4px 15px 0 rgba(76, 175, 80, 0.3),
    inset 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}

.glass-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: left 0.5s;
}

.glass-button:hover::before {
  left: 100%;
}

.glass-link {
  position: relative;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.glass-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #4CAF50, #81C784);
  transition: width 0.3s ease;
  border-radius: 1px;
}

.glass-link:hover::after {
  width: 100%;
}

.modern-title {
  background: linear-gradient(
    90deg, 
    #166534 0%, 
    #15803d 25%, 
    #86efac 50%, 
    #15803d 75%, 
    #166534 100%
  );
  background-size: 300% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: gradient-wave 3s ease-in-out infinite;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  letter-spacing: -0.015em;
  font-weight: 500;
  position: relative;
}

.green-line {
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, #16a34a, #22c55e, #16a34a);
  border-radius: 1px;
  animation: line-glow 2s ease-in-out infinite alternate;
}

@keyframes gradient-wave {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

@keyframes line-glow {
  0% {
    box-shadow: 0 0 5px rgba(34, 197, 94, 0.3);
    opacity: 0.8;
  }
  100% {
    box-shadow: 0 0 15px rgba(34, 197, 94, 0.6);
    opacity: 1;
  }
}

/* Respaldo para navegadores que no soportan background-clip: text */
@supports not (-webkit-background-clip: text) {
  .modern-title {
    color: #166534;
    animation: none;
  }
}

/* Mejoras de responsividad para pantallas móviles */
@media (max-width: 480px) {
  .page-container {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }
  
  .glass-card {
    padding: 1rem;
    margin: 0 0.25rem;
  }
  
  .glass-input {
    font-size: 14px; /* Evita zoom en iOS */
    min-height: 36px;
  }
  
  .relative .absolute svg {
    width: 0.875rem;
    height: 0.875rem;
  }
  
  .text-lg {
    font-size: 1rem;
  }
  
  .text-base {
    font-size: 0.875rem;
  }
}

@media (max-height: 600px) {
  .page-container {
    max-width: 320px;
  }
  
  .text-center.mb-4 {
    margin-bottom: 0.75rem;
  }
  
  .w-32.h-32 {
    width: 2.5rem;
    height: 2.5rem;
  }
  
  .text-lg {
    font-size: 1rem;
  }
  
  .text-base {
    font-size: 0.875rem;
  }
  
  .glass-card {
    padding: 1rem;
  }
}

@media (max-height: 500px) {
  .text-center.mb-4 {
    margin-bottom: 0.5rem;
  }
  
  .mb-3 {
    margin-bottom: 0.25rem;
  }
  
  .mt-4 {
    margin-top: 0.75rem;
  }
  
  .glass-card {
    padding: 0.875rem;
  }
}

/* Para pantallas muy pequeñas como iPhone SE */
@media (max-width: 375px) and (max-height: 667px) {
  .page-container {
    max-width: 300px;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }
  
  .glass-card {
    padding: 0.875rem;
  }
  
  .glass-input {
    font-size: 14px;
    min-height: 34px;
  }
}

/* Para pantallas grandes */
@media (min-width: 768px) {
  .page-container {
    max-width: 380px;
  }
  
  .glass-card {
    padding: 1.5rem;
  }
}

/* Soporte adicional para navegadores que no soportan backdrop-filter */
@supports not (backdrop-filter: blur(20px)) {
  .glass-card {
    background: rgba(255, 255, 255, 0.85);
  }
  
  .glass-input {
    background: rgba(255, 255, 255, 0.7);
  }
}
</style>
