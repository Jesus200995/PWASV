<template>
  <div class="apple-forgot bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 relative">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-emerald-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-teal-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>

    <!-- Success Modal -->
    <Teleport to="body">
      <Transition name="modal-scale">
        <div v-if="showSuccessModal" class="modal-backdrop" @click.self="goToLogin">
          <div class="modal-container">
            <div class="modal-success-icon">
              <svg viewBox="0 0 56 56" fill="none">
                <circle cx="28" cy="28" r="26" stroke="#34C759" stroke-width="3"/>
                <path d="M17 28l7 7 15-15" stroke="#34C759" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h2 class="modal-heading">Contraseña Actualizada</h2>
            <p class="modal-description">Tu contraseña ha sido cambiada exitosamente</p>
            <div class="modal-progress-track">
              <div class="modal-progress-fill"></div>
            </div>
            <p class="modal-redirect-text">Redirigiendo al inicio de sesión...</p>
            <button @click="goToLogin" class="modal-action-btn">Continuar</button>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Main Content -->
    <div class="forgot-content relative z-10">
      <!-- Fixed Navigation Header -->
      <nav class="forgot-nav">
        <div class="nav-container">
          <router-link to="/login" class="nav-back-btn">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M15 19l-7-7 7-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>Volver</span>
          </router-link>
          <h1 class="nav-title">Recuperar Contraseña</h1>
          <div class="nav-spacer"></div>
        </div>
      </nav>

      <!-- Header Section -->
      <header class="forgot-hero">
        <p class="hero-instruction">Ingresa tu correo electrónico y tu nueva contraseña para recuperar el acceso a tu cuenta.</p>
      </header>

      <!-- Error Alert -->
      <Transition name="alert-slide">
        <div v-if="errorMessage" class="error-alert">
          <div class="alert-icon">
            <svg viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              <path d="M12 8v4m0 4h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <p class="alert-text">{{ errorMessage }}</p>
        </div>
      </Transition>

      <!-- Reset Password Form -->
      <form @submit.prevent="resetPassword" class="forgot-form">
        <!-- Email Section -->
        <div class="form-group">
          <div class="group-header">
            <div class="group-icon">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <polyline points="22,6 12,13 2,6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <span class="group-title">Correo Electrónico</span>
          </div>

          <div class="form-field">
            <label class="field-label">Tu correo registrado</label>
            <div class="input-wrapper" :class="{ 'has-error': formError && !email }">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="2"/>
                <path d="M16 8v5a3 3 0 006 0v-1a10 10 0 10-3.92 7.94" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <input 
                v-model="email" 
                type="email" 
                required 
                placeholder="nombre@ejemplo.com"
                autocomplete="email"
              />
            </div>
          </div>
        </div>

        <!-- New Password Section -->
        <div class="form-group">
          <div class="group-header">
            <div class="group-icon">
              <svg viewBox="0 0 24 24" fill="none">
                <rect x="3" y="11" width="18" height="11" rx="2" stroke="currentColor" stroke-width="2"/>
                <path d="M7 11V7a5 5 0 0110 0v4" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <span class="group-title">Nueva Contraseña</span>
          </div>

          <div class="form-field">
            <label class="field-label">Nueva contraseña</label>
            <div class="input-wrapper password-wrapper" :class="{ 'has-error': formError && newPassword.length < 6 }">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                <rect x="3" y="11" width="18" height="11" rx="2" stroke="currentColor" stroke-width="2"/>
                <path d="M7 11V7a5 5 0 0110 0v4" stroke="currentColor" stroke-width="2"/>
              </svg>
              <input 
                v-model="newPassword" 
                :type="showPassword ? 'text' : 'password'" 
                required 
                placeholder="Mínimo 6 caracteres"
                minlength="6"
                @input="checkPasswordsMatch"
              />
              <button type="button" class="visibility-toggle" @click="togglePasswordVisibility">
                <svg v-if="showPassword" viewBox="0 0 24 24" fill="none">
                  <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <line x1="1" y1="1" x2="23" y2="23" stroke="currentColor" stroke-width="2"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" stroke-width="2"/>
                  <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
                </svg>
              </button>
            </div>
            <span class="field-hint">Mínimo 6 caracteres</span>
          </div>

          <div class="form-field">
            <label class="field-label">Confirmar nueva contraseña</label>
            <div class="input-wrapper password-wrapper" :class="{ 'has-error': !passwordsMatch, 'has-success': passwordsMatch && confirmPassword.length > 0 }">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <input 
                v-model="confirmPassword" 
                :type="showConfirmPassword ? 'text' : 'password'" 
                required 
                placeholder="Confirmar contraseña"
                minlength="6"
                @input="checkPasswordsMatch"
              />
              <button type="button" class="visibility-toggle" @click="toggleConfirmPasswordVisibility">
                <svg v-if="showConfirmPassword" viewBox="0 0 24 24" fill="none">
                  <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <line x1="1" y1="1" x2="23" y2="23" stroke="currentColor" stroke-width="2"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" stroke-width="2"/>
                  <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
                </svg>
              </button>
            </div>
            <span v-if="confirmPassword && !passwordsMatch" class="field-hint error-hint">
              <svg viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <path d="M15 9l-6 6m0-6l6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              Las contraseñas no coinciden
            </span>
            <span v-else-if="confirmPassword && passwordsMatch" class="field-hint success-hint">
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              Las contraseñas coinciden
            </span>
          </div>
        </div>

        <!-- Submit Button -->
        <button type="submit" :disabled="loading || !isFormComplete || !passwordsMatch" class="submit-btn" :class="{ 'is-loading': loading, 'is-disabled': !isFormComplete || !passwordsMatch }">
          <Transition name="btn-fade" mode="out-in">
            <span v-if="loading" key="loading" class="btn-inner">
              <div class="btn-loader"></div>
              <span>Cambiando contraseña...</span>
            </span>
            <span v-else-if="!email" key="email" class="btn-inner">
              <svg viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <path d="M12 8v4m0 4h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <span>Ingresa tu correo</span>
            </span>
            <span v-else-if="newPassword.length < 6" key="password" class="btn-inner">
              <svg viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <path d="M12 8v4m0 4h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <span>Mínimo 6 caracteres</span>
            </span>
            <span v-else-if="!passwordsMatch" key="mismatch" class="btn-inner">
              <svg viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <path d="M15 9l-6 6m0-6l6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <span>Las contraseñas deben coincidir</span>
            </span>
            <span v-else key="ready" class="btn-inner">
              <span>Cambiar contraseña</span>
              <svg viewBox="0 0 24 24" fill="none">
                <path d="M5 12h14m-6-6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </span>
          </Transition>
        </button>
      </form>

      <!-- Footer -->
      <footer class="forgot-footer">
        <p>¿Recordaste tu contraseña? <router-link to="/login">Iniciar sesión</router-link></p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, Teleport, Transition } from 'vue';
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
const formError = ref(false);
const showSuccessModal = ref(false);
const passwordsMatch = ref(true);

const isFormComplete = computed(() => {
  return email.value.trim() !== '' && 
         newPassword.value.length >= 6 && 
         confirmPassword.value.trim() !== '';
});

function togglePasswordVisibility() {
  showPassword.value = !showPassword.value;
}

function toggleConfirmPasswordVisibility() {
  showConfirmPassword.value = !showConfirmPassword.value;
}

function checkPasswordsMatch() {
  if (confirmPassword.value === '') {
    passwordsMatch.value = true;
    return;
  }
  passwordsMatch.value = newPassword.value === confirmPassword.value;
}

function goToLogin() {
  router.push('/login');
}

async function resetPassword() {
  loading.value = true;
  errorMessage.value = '';
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
    
    // Actualizar la contraseña
    const updateData = {
      correo: usuario.correo,
      nombre_completo: usuario.nombre_completo,
      cargo: usuario.cargo,
      supervisor: usuario.supervisor,
      contrasena: newPassword.value,
      curp: usuario.curp,
      telefono: usuario.telefono
    };
    
    await axios.put(`${currentApiUrl}/usuarios/${usuario.id}`, updateData, {
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    // Mostrar modal de éxito
    showSuccessModal.value = true;
    
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
/* ==========================================================================
   APPLE DESIGN SYSTEM - FORGOT PASSWORD
   ========================================================================== */

/* Main Container */
.apple-forgot {
  position: fixed;
  inset: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Scrollable Content */
.forgot-content {
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
  padding: 0 20px env(safe-area-inset-bottom, 20px);
  padding-top: 0;
}

/* Fixed Navigation */
.forgot-nav {
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(245, 245, 247, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  padding: 0 20px;
  margin: 0 -20px;
}

.nav-container {
  max-width: 500px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  gap: 16px;
}

.nav-back-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 980px;
  color: #06c;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
  flex-shrink: 0;
}

.nav-back-btn:hover {
  background: rgba(255, 255, 255, 1);
  transform: translateX(-2px);
}

.nav-back-btn svg {
  width: 16px;
  height: 16px;
}

.nav-title {
  font-size: 17px;
  font-weight: 600;
  color: #1d1d1f;
  letter-spacing: -0.3px;
  margin: 0;
  text-align: center;
  flex: 1;
}

.nav-spacer {
  width: 90px;
  flex-shrink: 0;
}

/* Hero Section */
.forgot-hero {
  text-align: center;
  padding: 20px 0 16px;
  max-width: 500px;
  margin: 0 auto;
}

.hero-instruction {
  font-size: 13px;
  line-height: 1.5;
  color: #86868b;
  font-weight: 400;
  margin: 0;
  text-align: center;
}

/* Error Alert */
.error-alert {
  max-width: 500px;
  margin: 0 auto 16px;
  padding: 14px;
  background: #fff2f2;
  border-radius: 12px;
  border: 1px solid rgba(255, 59, 48, 0.2);
  display: flex;
  align-items: center;
  gap: 10px;
}

.alert-icon svg {
  width: 20px;
  height: 20px;
  color: #ff3b30;
}

.alert-text {
  font-size: 13px;
  color: #ff3b30;
  font-weight: 500;
  line-height: 1.4;
}

/* Form Container */
.forgot-form {
  max-width: 500px;
  margin: 0 auto;
}

/* Form Groups */
.form-group {
  background: white;
  border-radius: 14px;
  padding: 15px;
  margin-bottom: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.group-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f5f5f7;
}

.group-icon {
  width: 28px;
  height: 28px;
  background: linear-gradient(180deg, #34c759 0%, #30b350 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.group-icon svg {
  width: 14px;
  height: 14px;
  color: white;
}

.group-title {
  font-size: 13px;
  font-weight: 600;
  color: #1d1d1f;
  letter-spacing: -0.2px;
}

/* Form Fields */
.form-field {
  margin-bottom: 16px;
}

.form-field:last-child {
  margin-bottom: 0;
}

.field-label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 7px;
  letter-spacing: -0.1px;
}

/* Input Wrapper */
.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background: #f5f5f7;
  border: 2px solid transparent;
  border-radius: 12px;
  transition: all 0.2s cubic-bezier(0.25, 0.1, 0.25, 1);
}

.input-wrapper:focus-within {
  background: white;
  border-color: #34c759;
  box-shadow: 0 0 0 4px rgba(52, 199, 89, 0.1);
}

.input-wrapper.has-error {
  border-color: #ff3b30;
}

.input-wrapper.has-success {
  border-color: #34c759;
}

.input-icon {
  position: absolute;
  left: 12px;
  width: 18px;
  height: 18px;
  color: #86868b;
  pointer-events: none;
  transition: color 0.2s ease;
}

.input-wrapper:focus-within .input-icon {
  color: #34c759;
}

.input-wrapper.has-error .input-icon {
  color: #ff3b30;
}

.input-wrapper input {
  flex: 1;
  width: 100%;
  padding: 12px 12px 12px 42px;
  border: none;
  background: transparent;
  font-size: 15px;
  color: #1d1d1f;
  outline: none;
  font-family: inherit;
}

.input-wrapper input::placeholder {
  color: #86868b;
}

.password-wrapper input {
  padding-right: 44px;
}

/* Field Hints */
.field-hint {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  color: #86868b;
  margin-top: 5px;
}

.field-hint svg {
  width: 14px;
  height: 14px;
}

.field-hint.error-hint {
  color: #ff3b30;
}

.field-hint.success-hint {
  color: #34c759;
}

/* Visibility Toggle */
.visibility-toggle {
  position: absolute;
  right: 6px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  cursor: pointer;
  border-radius: 10px;
  transition: background 0.15s ease;
}

.visibility-toggle:hover {
  background: rgba(0, 0, 0, 0.04);
}

.visibility-toggle svg {
  width: 20px;
  height: 20px;
  color: #86868b;
}

/* Submit Button */
.submit-btn {
  width: 100%;
  padding: 15px 20px;
  background: linear-gradient(180deg, #34c759 0%, #30b350 100%);
  border: none;
  border-radius: 14px;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.25, 0.1, 0.25, 1);
  box-shadow: 0 4px 14px rgba(52, 199, 89, 0.35);
  font-family: inherit;
  margin-top: 8px;
}

.submit-btn:hover:not(.is-loading):not(.is-disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(52, 199, 89, 0.4);
}

.submit-btn:active:not(.is-loading):not(.is-disabled) {
  transform: translateY(0);
}

.submit-btn.is-disabled {
  background: linear-gradient(180deg, #8e8e93 0%, #7c7c80 100%);
  cursor: not-allowed;
  box-shadow: none;
}

.submit-btn.is-loading {
  cursor: wait;
}

.btn-inner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-inner svg {
  width: 18px;
  height: 18px;
}

.btn-loader {
  width: 18px;
  height: 18px;
  border: 2.5px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spinner-rotate 0.8s linear infinite;
}

@keyframes spinner-rotate {
  to { transform: rotate(360deg); }
}

/* Footer */
.forgot-footer {
  max-width: 500px;
  margin: 24px auto;
  text-align: center;
  padding-bottom: 24px;
}

.forgot-footer p {
  font-size: 13px;
  color: #86868b;
}

.forgot-footer a {
  color: #06c;
  font-weight: 600;
  text-decoration: none;
}

.forgot-footer a:hover {
  text-decoration: underline;
}

/* ==========================================================================
   MODAL
   ========================================================================== */

.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 1000;
}

.modal-container {
  background: white;
  border-radius: 24px;
  padding: 32px 28px;
  max-width: 360px;
  width: 100%;
  text-align: center;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.25);
}

.modal-success-icon {
  width: 70px;
  height: 70px;
  margin: 0 auto 20px;
}

.modal-success-icon svg {
  width: 100%;
  height: 100%;
}

.modal-heading {
  font-size: 21px;
  font-weight: 700;
  color: #1d1d1f;
  margin-bottom: 8px;
  letter-spacing: -0.3px;
}

.modal-description {
  font-size: 14px;
  color: #86868b;
  margin-bottom: 20px;
}

.modal-progress-track {
  height: 4px;
  background: #f5f5f7;
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 8px;
}

.modal-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #34c759, #30d158);
  border-radius: 2px;
  animation: progress-fill 3s linear forwards;
}

@keyframes progress-fill {
  from { width: 0%; }
  to { width: 100%; }
}

.modal-redirect-text {
  font-size: 12px;
  color: #34c759;
  font-weight: 500;
  margin-bottom: 20px;
}

.modal-action-btn {
  padding: 13px 28px;
  background: linear-gradient(180deg, #34c759 0%, #30b350 100%);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.modal-action-btn:hover {
  transform: scale(1.03);
}

/* ==========================================================================
   ANIMATIONS
   ========================================================================== */

/* Modal Scale */
.modal-scale-enter-active {
  animation: modal-in 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-scale-leave-active {
  animation: modal-in 0.2s ease reverse;
}

@keyframes modal-in {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Alert Slide */
.alert-slide-enter-active,
.alert-slide-leave-active {
  transition: all 0.3s ease;
}

.alert-slide-enter-from,
.alert-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Button Fade */
.btn-fade-enter-active,
.btn-fade-leave-active {
  transition: all 0.2s ease;
}

.btn-fade-enter-from,
.btn-fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* ==========================================================================
   RESPONSIVE
   ========================================================================== */

@media (max-width: 480px) {
  .forgot-content {
    padding: 0 16px env(safe-area-inset-bottom, 16px);
    padding-top: 0;
  }
  
  .forgot-nav {
    padding: 0 16px;
    margin: 0 -16px;
  }
  
  .nav-container {
    height: 52px;
  }
  
  .nav-title {
    font-size: 16px;
  }
  
  .nav-back-btn {
    padding: 7px 12px;
    font-size: 13px;
  }
  
  .nav-spacer {
    width: 80px;
  }
  
  .hero-instruction {
    font-size: 12px;
  }
  
  .form-group {
    padding: 14px;
    border-radius: 14px;
  }
  
  .input-wrapper input {
    font-size: 16px; /* Prevents iOS zoom */
    padding: 12px 12px 12px 40px;
  }
}

@media (min-width: 768px) {
  .forgot-content {
    padding: 0 24px 40px;
    padding-top: 0;
  }
  
  .forgot-nav {
    padding: 0 24px;
    margin: 0 -24px;
  }
  
  .nav-container {
    height: 60px;
  }
  
  .nav-title {
    font-size: 19px;
  }
  
  .form-group {
    padding: 18px;
  }
}

/* ==========================================================================
   BACKDROP FILTER FALLBACK
   ========================================================================== */

@supports not (backdrop-filter: blur(20px)) {
  .forgot-nav {
    background: rgba(245, 245, 247, 0.98);
  }
  
  .modal-backdrop {
    background: rgba(0, 0, 0, 0.7);
  }
}
</style>
