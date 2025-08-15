<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-emerald-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-teal-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>
    
    <div class="page-container w-full max-w-md relative z-10 px-2">
      <!-- Back to Login Link - Top Left -->
      <div class="flex justify-start mb-3">
        <router-link to="/login" class="text-sm font-medium text-primary hover:text-primary-dark transition-colors duration-200 glass-link">
          ← Volver al inicio de sesión
        </router-link>
      </div>

      <!-- Header Section -->
      <div class="text-center mb-4">
        <h1 class="text-lg font-bold text-primary mb-1 text-center glass-title">Recuperar Contraseña</h1>
        <h2 class="text-base font-semibold text-gray-700">Cambiar contraseña</h2>
        <p class="mt-1 text-gray-500 text-xs">Ingresa tu correo y nueva contraseña</p>
      </div>

      <!-- Success Message -->
      <transition name="bounce">
        <div v-if="successMessage" class="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 rounded-lg shadow-sm mb-4" role="alert">
          <p class="flex items-center text-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            {{ successMessage }}
          </p>
        </div>
      </transition>

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

      <!-- Reset Password Form -->
      <div class="glass-card">
        <form @submit.prevent="resetPassword">
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
                  class="glass-input w-full pl-9 pr-3 py-2 text-sm" 
                  placeholder="nombre@ejemplo.com" 
                  :class="{ 'animate-shake': formError }" 
                />
              </div>
            </div>
            
            <div>
              <label for="newPassword" class="block text-xs font-medium text-gray-800 mb-1">Nueva contraseña</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <input 
                  v-model="newPassword" 
                  id="newPassword" 
                  name="newPassword" 
                  :type="showPassword ? 'text' : 'password'" 
                  autocomplete="new-password" 
                  required 
                  class="glass-input w-full pl-9 pr-9 py-2 text-sm" 
                  placeholder="Nueva contraseña" 
                  :class="{ 'animate-shake': formError }" 
                  minlength="6"
                />
                <button
                  type="button"
                  @click="togglePasswordVisibility"
                  class="absolute inset-y-0 right-0 flex items-center pr-2 text-primary hover:text-primary-dark focus:outline-none transition-colors duration-200"
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
              <p class="mt-1 text-xs text-gray-500">Mínimo 6 caracteres</p>
            </div>

            <div>
              <label for="confirmPassword" class="block text-xs font-medium text-gray-800 mb-1">Confirmar nueva contraseña</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <input 
                  v-model="confirmPassword" 
                  id="confirmPassword" 
                  name="confirmPassword" 
                  :type="showConfirmPassword ? 'text' : 'password'" 
                  autocomplete="new-password" 
                  required 
                  class="glass-input w-full pl-9 pr-9 py-2 text-sm" 
                  placeholder="Confirmar contraseña" 
                  :class="{ 'animate-shake': formError }" 
                  minlength="6"
                />
                <button
                  type="button"
                  @click="toggleConfirmPasswordVisibility"
                  class="absolute inset-y-0 right-0 flex items-center pr-2 text-primary hover:text-primary-dark focus:outline-none transition-colors duration-200"
                >
                  <svg v-if="showConfirmPassword" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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
            class="glass-button w-full mt-4 flex items-center justify-center py-2 text-sm"
            :class="{ 'opacity-50 cursor-not-allowed': loading }"
          >
            <svg v-if="loading" class="animate-spin h-3 w-3 mr-2" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ loading ? 'Cambiando contraseña...' : 'Cambiar contraseña' }}</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { API_URL, getBestApiUrl, checkInternetConnection, getOfflineMessage } from '../utils/network.js';

const router = useRouter();
const email = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const formError = ref(false);

function togglePasswordVisibility() {
  showPassword.value = !showPassword.value;
}

function toggleConfirmPasswordVisibility() {
  showConfirmPassword.value = !showConfirmPassword.value;
}

async function resetPassword() {
  loading.value = true;
  errorMessage.value = '';
  successMessage.value = '';
  formError.value = false;
  
  // Validaciones
  if (!email.value || !newPassword.value || !confirmPassword.value) {
    errorMessage.value = 'Por favor, completa todos los campos';
    formError.value = true;
    loading.value = false;
    return;
  }
  
  if (newPassword.value.length < 6) {
    errorMessage.value = 'La nueva contraseña debe tener al menos 6 caracteres';
    formError.value = true;
    loading.value = false;
    return;
  }
  
  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value = 'Las contraseñas no coinciden';
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
  
  try {
    // Obtener la mejor URL del servidor
    const currentApiUrl = await getBestApiUrl();
    
    // Primero verificar que el usuario existe
    const usuariosResponse = await axios.get(`${currentApiUrl}/usuarios`, {
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    const usuarios = usuariosResponse.data.usuarios;
    const usuario = usuarios.find(u => u.correo.toLowerCase() === email.value.toLowerCase());
    
    if (!usuario) {
      errorMessage.value = 'No se encontró una cuenta con ese correo electrónico';
      formError.value = true;
      loading.value = false;
      return;
    }
    
    // Actualizar la contraseña directamente en la base de datos
    // Como el backend usa contraseñas sin encriptar, podemos usar el endpoint de actualización
    const updateData = {
      correo: usuario.correo,
      nombre_completo: usuario.nombre_completo,
      cargo: usuario.cargo,
      supervisor: usuario.supervisor,
      contrasena: newPassword.value, // Nueva contraseña
      curp: usuario.curp,
      telefono: usuario.telefono
    };
    
    await axios.put(`${currentApiUrl}/usuarios/${usuario.id}`, updateData, {
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    successMessage.value = 'Contraseña actualizada exitosamente. Ahora puedes iniciar sesión con tu nueva contraseña.';
    
    // Limpiar formulario
    email.value = '';
    newPassword.value = '';
    confirmPassword.value = '';
    
    // Redirigir al login después de 3 segundos
    setTimeout(() => {
      router.push('/login');
    }, 3000);
    
  } catch (error) {
    console.error('Error al cambiar contraseña:', error);
    
    if (error.response) {
      const status = error.response.status;
      if (status === 404) {
        errorMessage.value = 'No se encontró una cuenta con ese correo electrónico';
      } else if (status === 500) {
        errorMessage.value = 'Error del servidor. Inténtalo de nuevo en unos minutos.';
      } else {
        errorMessage.value = error.response.data.detail || 'Error al cambiar la contraseña';
      }
    } else if (error.request) {
      errorMessage.value = 'No se pudo conectar con el servidor. Verifica tu conexión a internet.';
    } else if (error.code === 'ECONNABORTED') {
      errorMessage.value = 'La conexión tardó demasiado. Verifica tu conexión a internet.';
    } else {
      errorMessage.value = 'Error al cambiar contraseña: ' + error.message;
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

.glass-title {
  color: #2e7d32;
  text-shadow: 
    0 1px 2px rgba(46, 125, 50, 0.3),
    0 0 8px rgba(46, 125, 50, 0.2);
  filter: drop-shadow(0 1px 1px rgba(255, 255, 255, 0.3));
  position: relative;
}

.glass-title::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.2) 0%, 
    rgba(255, 255, 255, 0.05) 50%,
    rgba(255, 255, 255, 0.2) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  z-index: 1;
  pointer-events: none;
}

/* Estilos específicos para los botones del ojo */
button[type="button"] {
  background: transparent !important;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  min-height: 32px;
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
  
  .glass-card {
    padding: 1rem;
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
    max-width: 420px;
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
