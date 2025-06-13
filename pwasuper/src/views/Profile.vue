<template>
  <div class="page-container py-4">
    <!-- Header del perfil -->
    <div class="card mb-4">
      <div class="text-center mb-6">
        <div class="w-20 h-20 bg-primary rounded-full flex items-center justify-center mx-auto mb-3">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <h1 class="text-xl font-bold text-gray-800">{{ user.nombre_completo }}</h1>
        <p class="text-sm text-gray-600">{{ user.cargo }}</p>
        <p class="text-xs text-gray-500 mt-1">{{ user.email }}</p>
      </div>
    </div>

    <!-- Información del usuario -->
    <div class="card mb-4">
      <h2 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        Información Personal
      </h2>
      
      <div class="space-y-3">
        <div class="flex justify-between items-center py-2 border-b border-gray-100">
          <span class="text-sm font-medium text-gray-600">Nombre completo:</span>
          <span class="text-sm text-gray-800">{{ user.nombre_completo }}</span>
        </div>
        
        <div class="flex justify-between items-center py-2 border-b border-gray-100">
          <span class="text-sm font-medium text-gray-600">Email:</span>
          <span class="text-sm text-gray-800">{{ user.email }}</span>
        </div>
        
        <div class="flex justify-between items-center py-2 border-b border-gray-100">
          <span class="text-sm font-medium text-gray-600">Cargo:</span>
          <span class="text-sm text-gray-800">{{ user.cargo }}</span>
        </div>
        
        <div class="flex justify-between items-center py-2">
          <span class="text-sm font-medium text-gray-600">Fecha de registro:</span>
          <span class="text-sm text-gray-800">{{ formatDate(user.fecha_registro) }}</span>
        </div>
      </div>
    </div>    <!-- Cambio de contraseña -->
    <div class="card">
      <h2 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
        Cambiar Contraseña
      </h2>
      
      <form @submit.prevent="changePassword" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Nueva contraseña</label>
          <input
            v-model="passwordForm.newPassword"
            type="password"
            class="form-input"
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
            class="form-input"
            :class="{ 'border-red-500': errors.confirmPassword }"
            placeholder="Confirma tu nueva contraseña"
            required
          />
          <p v-if="errors.confirmPassword" class="text-red-500 text-xs mt-1">{{ errors.confirmPassword }}</p>
        </div>
        
        <button
          type="submit"
          :disabled="isChangingPassword"
          class="btn btn-primary w-full"
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
      <div v-if="showSuccessModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-lg p-6 max-w-sm w-full mx-4">
          <div class="text-center">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">¡Contraseña cambiada!</h3>
            <p class="text-sm text-gray-600 mb-4">Tu contraseña ha sido actualizada exitosamente.</p>
            <button @click="showSuccessModal = false" class="btn btn-primary w-full">
              Entendido
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

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
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch (e) {
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
  
  try {
    // Simular llamada a la API
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Aquí iría la lógica real para cambiar la contraseña
    // Por ahora solo simulamos éxito
      // Limpiar el formulario
    passwordForm.value = {
      newPassword: '',
      confirmPassword: ''
    }
    
    // Mostrar modal de éxito
    showSuccessModal.value = true
    
  } catch (error) {
    console.error('Error al cambiar contraseña:', error)
    errors.value.general = 'Error al cambiar la contraseña. Por favor, intenta de nuevo.'
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
</style>
