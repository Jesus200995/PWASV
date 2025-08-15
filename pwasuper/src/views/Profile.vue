<template>
  <div class="fixed inset-0 bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 overflow-hidden" style="z-index: 0;">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-emerald-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-teal-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>

    <div class="absolute inset-0 overflow-y-auto pt-16 sm:pt-20 pb-4" style="z-index: 1;">
      <div class="page-container w-full max-w-md mx-auto relative z-10 p-4 sm:p-6 lg:p-8">
      <!-- Header del perfil -->
      <div class="glass-card mb-3">
        <div class="text-center mb-4">
          <div class="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-2 glass-avatar">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
          <h1 class="text-lg font-bold text-gray-800 modern-title">{{ user.nombre_completo }}</h1>
          <div class="green-line mx-auto mb-2"></div>
          <p class="text-sm text-gray-600">{{ user.cargo }}</p>
          <p class="text-xs text-gray-500 mt-1">{{ user.email }}</p>
        </div>
      </div>

      <!-- Información del usuario -->
      <div class="glass-card mb-3">
        <h2 class="text-base font-semibold text-gray-800 mb-3 modern-title flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Información Personal
        </h2>
        <div class="green-line mb-3"></div>
        
        <div class="space-y-3">
          <div class="glass-info-row flex justify-between items-center py-2">
            <span class="text-sm font-medium text-gray-600">Nombre completo:</span>
            <span class="text-sm text-gray-800 font-semibold">{{ user.nombre_completo }}</span>
          </div>
          
          <div class="glass-info-row flex justify-between items-center py-2">
            <span class="text-sm font-medium text-gray-600">Email:</span>
            <span class="text-sm text-gray-800 font-semibold">{{ user.email }}</span>
          </div>
          
          <div class="glass-info-row flex justify-between items-center py-2">
            <span class="text-sm font-medium text-gray-600">Cargo:</span>
            <span class="text-sm text-gray-800 font-semibold">{{ user.cargo }}</span>
          </div>
          
          <div class="glass-info-row flex justify-between items-center py-2">
            <span class="text-sm font-medium text-gray-600">Fecha de registro:</span>
            <span class="text-sm text-gray-800 font-semibold">{{ formatDate(user.fecha_registro) }}</span>
          </div>
        </div>
      </div>

      <!-- Cambio de contraseña -->
      <div class="glass-card">
        <h2 class="text-base font-semibold text-gray-800 mb-3 modern-title flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          Cambiar Contraseña
        </h2>
        <div class="green-line mb-3"></div>
        <form @submit.prevent="changePassword" class="space-y-4">
        <!-- Mensaje de error general -->
        <div v-if="errors.general" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-3 rounded-lg" role="alert">
          <p class="text-sm">{{ errors.general }}</p>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Nueva contraseña</label>
          <input
            v-model="passwordForm.newPassword"
            type="password"
            class="glass-input w-full"
            :class="{ 'border-red-500': errors.newPassword }"
            placeholder="Ingresa tu nueva contraseña"
            required
          />
          <p v-if="errors.newPassword" class="text-red-500 text-xs mt-1">{{ errors.newPassword }}</p>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Confirmar nueva contraseña</label>
          <input
            v-model="passwordForm.confirmPassword"
            type="password"
            class="glass-input w-full"
            :class="{ 'border-red-500': errors.confirmPassword }"
            placeholder="Confirma tu nueva contraseña"
            required
          />
          <p v-if="errors.confirmPassword" class="text-red-500 text-xs mt-1">{{ errors.confirmPassword }}</p>
        </div>
        
        <button
          type="submit"
          :disabled="isChangingPassword"
          class="glass-button w-full"
          :class="{ 'opacity-50 cursor-not-allowed': isChangingPassword }"
        >
          <svg v-if="isChangingPassword" class="animate-spin h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ isChangingPassword ? 'Cambiando...' : 'Cambiar Contraseña' }}
        </button>
      </form>
    </div>

    <!-- Modal de confirmación -->
    <transition name="fade">
      <div v-if="showSuccessModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4" style="z-index: 60;">
        <div class="glass-card max-w-sm w-full mx-4">
          <div class="text-center">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4 glass-success-icon">
              <svg class="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2 modern-title">¡Contraseña cambiada!</h3>
            <div class="green-line mx-auto mb-3"></div>
            <p class="text-sm text-gray-600 mb-4">Tu contraseña ha sido actualizada exitosamente.</p>
            <button @click="showSuccessModal = false" class="glass-button w-full">
              Entendido
            </button>
          </div>
        </div>
      </div>
    </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { API_URL, checkInternetConnection, getOfflineMessage } from '../utils/network.js'

const user = ref({})
const passwordForm = ref({
  newPassword: '',
  confirmPassword: ''
})
const errors = ref({})
const isChangingPassword = ref(false)
const showSuccessModal = ref(false)

onMounted(() => {
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    user.value = JSON.parse(storedUser)
  }
})

const formatDate = (dateString) => {
  if (!dateString) return 'No disponible'
  try {
    // Si viene una fecha ISO completa (con T), la procesamos
    if (typeof dateString === 'string' && dateString.includes('T')) {
      return new Date(dateString).toLocaleDateString('es-ES', {
        timeZone: 'America/Mexico_City', // Forzar zona horaria de México
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    // Si viene solo una fecha (YYYY-MM-DD), crear la fecha sin zona horaria
    if (typeof dateString === 'string' && dateString.match(/^\d{4}-\d{2}-\d{2}$/)) {
      const [year, month, day] = dateString.split('-').map(num => parseInt(num, 10))
      const fecha = new Date(year, month - 1, day) // month - 1 porque los meses en JS van de 0-11
      
      return fecha.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    // Para otros casos, usar el método estándar
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch (e) {
    console.error('Error al formatear fecha:', e, 'Fecha original:', dateString)
    return 'No disponible'
  }
}

const validateForm = () => {
  errors.value = {}
  
  if (passwordForm.value.newPassword.length < 6) {
    errors.value.newPassword = 'La nueva contraseña debe tener al menos 6 caracteres'
  }
  
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    errors.value.confirmPassword = 'Las contraseñas no coinciden'
  }
  
  return Object.keys(errors.value).length === 0
}

const changePassword = async () => {
  if (!validateForm()) return
  
  isChangingPassword.value = true
  errors.value = {}
  
  try {
    // Verificar conexión a internet
    const online = await checkInternetConnection()
    if (!online) {
      errors.value.general = getOfflineMessage()
      return
    }
    
    // Llamada a la API para cambiar contraseña
    const response = await axios.post(`${API_URL}/cambiar_contrasena`, {
      usuario_id: user.value.id,
      nueva_contrasena: passwordForm.value.newPassword
    }, {
      timeout: 10000, // 10 segundos de timeout
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    // Verificar respuesta exitosa
    if (response.status === 200) {
      // Limpiar el formulario
      passwordForm.value = {
        newPassword: '',
        confirmPassword: ''
      }
      
      // Mostrar modal de éxito
      showSuccessModal.value = true
    }
    
  } catch (error) {
    console.error('Error al cambiar contraseña:', error)
    
    if (error.response) {
      // El servidor respondió con un estado de error
      const errorMsg = error.response.data?.detail || 
                      error.response.data?.message || 
                      'Error al cambiar la contraseña'
      errors.value.general = errorMsg
    } else if (error.request) {
      // La solicitud fue hecha pero no se recibió respuesta
      errors.value.general = 'No se pudo conectar con el servidor. Verifica tu conexión.'
    } else {
      // Algo ocurrió al configurar la solicitud
      errors.value.general = 'Error al cambiar la contraseña: ' + error.message
    }
  } finally {
    isChangingPassword.value = false
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
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
  padding: 0.75rem;
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

.glass-avatar {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px 0 rgba(76, 175, 80, 0.3),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
}

.glass-success-icon {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 2px solid rgba(34, 197, 94, 0.2);
  box-shadow: 
    0 8px 32px 0 rgba(34, 197, 94, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
}

.glass-info-row {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  padding: 0.75rem 0;
  transition: all 0.3s ease;
}

.glass-info-row:hover {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding-left: 0.5rem;
  padding-right: 0.5rem;
}

.glass-info-row:last-child {
  border-bottom: none;
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

/* Animación para elementos decorativos */
@keyframes pulse-slow {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.05);
  }
}

.animate-pulse-slow {
  animation: pulse-slow 4s ease-in-out infinite;
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
    padding-left: 0.75rem;
    padding-right: 0.75rem;
    padding-top: 0.75rem;
    padding-bottom: 0.75rem;
  }
  
  .glass-card {
    padding: 0.875rem;
    margin-bottom: 0.5rem;
    border-radius: 16px;
  }
  
  .glass-input {
    font-size: 14px; /* Evita zoom en iOS */
    min-height: 32px;
    padding: 0.5rem;
  }
  
  .text-lg {
    font-size: 1rem;
  }
  
  .text-base {
    font-size: 0.875rem;
  }
  
  .w-16, .h-16 {
    width: 3.5rem;
    height: 3.5rem;
  }
  
  .h-8, .w-8 {
    height: 1.75rem;
    width: 1.75rem;
  }
  
  .mb-3 {
    margin-bottom: 0.5rem;
  }
  
  .mb-4 {
    margin-bottom: 0.75rem;
  }
  
  .space-y-4 > * + * {
    margin-top: 0.75rem;
  }
  
  .space-y-3 > * + * {
    margin-top: 0.5rem;
  }
}

@media (max-width: 375px) {
  .page-container {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    max-width: calc(100vw - 1rem);
  }
  
  .glass-card {
    padding: 0.75rem;
    margin-bottom: 0.375rem;
    border-radius: 12px;
  }
  
  .glass-input {
    font-size: 14px;
    min-height: 30px;
    padding: 0.375rem 0.5rem;
  }
  
  .glass-button {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
  }
  
  .text-lg {
    font-size: 0.95rem;
  }
  
  .text-base {
    font-size: 0.8rem;
  }
  
  .text-sm {
    font-size: 0.75rem;
  }
  
  .text-xs {
    font-size: 0.65rem;
  }
}

@media (max-height: 700px) {
  .page-container {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
  }
  
  .glass-card {
    margin-bottom: 0.375rem;
    padding: 0.75rem;
  }
  
  .mb-3 {
    margin-bottom: 0.375rem;
  }
  
  .mb-4 {
    margin-bottom: 0.5rem;
  }
  
  .space-y-4 > * + * {
    margin-top: 0.5rem;
  }
  
  .space-y-3 > * + * {
    margin-top: 0.375rem;
  }
}

@media (max-height: 600px) {
  .page-container {
    max-width: 300px;
    padding: 0.375rem 0.5rem;
  }
  
  .glass-card {
    padding: 0.625rem;
    margin-bottom: 0.25rem;
  }
  
  .w-16, .h-16 {
    width: 3rem;
    height: 3rem;
  }
  
  .text-lg {
    font-size: 0.9rem;
  }
  
  .text-base {
    font-size: 0.775rem;
  }
}

@media (max-height: 500px) {
  .glass-card {
    padding: 0.5rem;
  }
  
  .mb-2, .mb-3, .mb-4 {
    margin-bottom: 0.25rem;
  }
  
  .space-y-4 > * + * {
    margin-top: 0.375rem;
  }
  
  .space-y-3 > * + * {
    margin-top: 0.25rem;
  }
}

/* Para pantallas grandes */
@media (min-width: 768px) {
  .page-container {
    max-width: 400px;
    padding: 1rem;
  }
  
  .glass-card {
    padding: 1.25rem;
    margin-bottom: 1rem;
  }
}

@media (min-width: 1024px) {
  .page-container {
    max-width: 450px;
    padding: 1.5rem 1rem;
  }
  
  .glass-card {
    padding: 1.5rem;
    margin-bottom: 1.25rem;
  }
}

/* Prevenir superposición de elementos */
.glass-card {
  position: relative;
  z-index: 2;
  clear: both;
}

/* Asegurar que los modales estén por encima de todo */
.fixed[style*="z-index: 60"] {
  z-index: 60 !important;
}

/* Z-index hierarchy para elementos principales */
.page-container {
  position: relative;
  z-index: 2;
}

/* Contenedor de fondo con z-index bajo */
.fixed.inset-0[style*="z-index: 0"] {
  z-index: 0 !important;
}

/* Contenedor scrollable */
.absolute.inset-0[style*="z-index: 1"] {
  z-index: 1 !important;
}

/* Mejoras para el contenedor scrollable */
.absolute.inset-0.overflow-y-auto {
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}

/* Espaciado optimizado para evitar superposición */
.space-y-3 > * + * {
  margin-top: 0.75rem;
}

.space-y-4 > * + * {
  margin-top: 1rem;
}

/* Soporte adicional para navegadores que no soportan backdrop-filter */
@supports not (backdrop-filter: blur(20px)) {
  .glass-card {
    background: rgba(255, 255, 255, 0.85);
  }
  
  .glass-input {
    background: rgba(255, 255, 255, 0.7);
  }
  
  .glass-button {
    background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%);
  }
}
</style>
