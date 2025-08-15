<template>
  <div class="fixed inset-0 bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 overflow-hidden" style="z-index: 0;">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-emerald-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-teal-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>

    <div class="absolute inset-0 overflow-y-auto pt-16 sm:pt-20 pb-3" style="z-index: 1;">
      <div class="page-container w-full max-w-sm mx-auto relative z-10 p-3 sm:p-4 lg:p-5">
      <!-- Header del perfil -->
      <div class="glass-card mb-2">
        <div class="text-center mb-3">
          <div class="w-12 h-12 bg-primary rounded-full flex items-center justify-center mx-auto mb-2 glass-avatar">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
          <h1 class="text-base font-bold text-gray-800 modern-title">{{ user.nombre_completo }}</h1>
          <div class="green-line mx-auto mb-2"></div>
          <p class="text-xs text-gray-600">{{ user.cargo }}</p>
          <p class="text-xs text-gray-500 mt-1">{{ user.correo || user.email }}</p>
        </div>
      </div>

      <!-- Información del usuario -->
      <div class="glass-card mb-2">
        <div class="flex justify-between items-center mb-2">
          <h2 class="text-sm font-semibold text-gray-800 modern-title flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-2 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Información Personal
          </h2>
          <button @click="openEditModal" class="glass-edit-button">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
        </div>
        <div class="green-line mb-2"></div>
        
        <div class="space-y-2">
          <div class="glass-info-row flex justify-between items-center py-1">
            <span class="text-xs font-medium text-gray-600">Nombre completo:</span>
            <span class="text-xs text-gray-800 font-semibold">{{ user.nombre_completo || 'No disponible' }}</span>
          </div>
          
          <div class="glass-info-row flex justify-between items-center py-1">
            <span class="text-xs font-medium text-gray-600">Email:</span>
            <span class="text-xs text-gray-800 font-semibold">{{ user.correo || user.email || 'No disponible' }}</span>
          </div>
          
          <div class="glass-info-row flex justify-between items-center py-1">
            <span class="text-xs font-medium text-gray-600">Cargo:</span>
            <span class="text-xs text-gray-800 font-semibold">{{ user.cargo || 'No disponible' }}</span>
          </div>
          
          <div class="glass-info-row flex justify-between items-center py-1">
            <span class="text-xs font-medium text-gray-600">Supervisor:</span>
            <span class="text-xs text-gray-800 font-semibold">{{ (user.supervisor && user.supervisor.trim()) || 'No asignado' }}</span>
          </div>
          
          <div class="glass-info-row flex justify-between items-center py-1">
            <span class="text-xs font-medium text-gray-600">CURP:</span>
            <span class="text-xs text-gray-800 font-semibold">{{ (user.curp && user.curp.trim()) || 'No registrado' }}</span>
          </div>
          
          <div class="glass-info-row flex justify-between items-center py-1">
            <span class="text-xs font-medium text-gray-600">Teléfono:</span>
            <span class="text-xs text-gray-800 font-semibold">{{ (user.telefono && user.telefono.trim()) || 'No registrado' }}</span>
          </div>
          
          <div v-if="user.fecha_registro" class="glass-info-row flex justify-between items-center py-1">
            <span class="text-xs font-medium text-gray-600">Fecha de registro:</span>
            <span class="text-xs text-gray-800 font-semibold">{{ formatDate(user.fecha_registro) }}</span>
          </div>
        </div>
      </div>

      <!-- Cambio de contraseña -->
      <div class="glass-card">
        <h2 class="text-sm font-semibold text-gray-800 mb-2 modern-title flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-2 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          Cambiar Contraseña
        </h2>
        <div class="green-line mb-2"></div>
        <form @submit.prevent="changePassword" class="space-y-3">
        <!-- Mensaje de error general -->
        <div v-if="errors.general" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-2 rounded-lg" role="alert">
          <p class="text-xs">{{ errors.general }}</p>
        </div>
        
        <div>
          <label class="block text-xs font-medium text-gray-700 mb-1">Nueva contraseña</label>
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
          <label class="block text-xs font-medium text-gray-700 mb-1">Confirmar nueva contraseña</label>
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
          <svg v-if="isChangingPassword" class="animate-spin h-3 w-3 mr-2" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ isChangingPassword ? 'Cambiando...' : 'Cambiar Contraseña' }}
        </button>
      </form>
    </div>

    <!-- Modal de confirmación -->
    <transition name="fade">
      <div v-if="showSuccessModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-3" style="z-index: 60;">
        <div class="glass-card max-w-xs w-full mx-3">
          <div class="text-center">
            <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3 glass-success-icon">
              <svg class="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <h3 class="text-base font-semibold text-gray-900 mb-2 modern-title">¡Contraseña cambiada!</h3>
            <div class="green-line mx-auto mb-2"></div>
            <p class="text-xs text-gray-600 mb-3">Tu contraseña ha sido actualizada exitosamente.</p>
            <button @click="showSuccessModal = false" class="glass-button w-full">
              Entendido
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Modal de edición de información personal -->
    <transition name="fade">
      <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-3" style="z-index: 9999;">
        <div class="bg-white rounded-2xl max-w-xs w-full mx-3 max-h-[85vh] overflow-y-auto edit-modal">
          <div class="sticky top-0 bg-white rounded-t-2xl border-b border-green-100 p-3">
            <div class="flex justify-between items-center">
              <h3 class="text-sm font-bold text-gray-800 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Editar Información
              </h3>
              <button @click="closeEditModal" class="text-gray-400 hover:text-gray-600 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          
          <div class="p-3">
            <form @submit.prevent="updateUserInfo" class="space-y-3">
              <!-- Mensaje de error general -->
              <div v-if="editErrors.general" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-2 rounded-lg" role="alert">
                <p class="text-xs">{{ editErrors.general }}</p>
              </div>

              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">Nombre completo</label>
                <input
                  v-model="editForm.nombre_completo"
                  type="text"
                  class="edit-input-small w-full"
                  :class="{ 'border-red-500': editErrors.nombre_completo }"
                  placeholder="Ingresa tu nombre completo"
                  required
                />
                <p v-if="editErrors.nombre_completo" class="text-red-500 text-xs mt-1">{{ editErrors.nombre_completo }}</p>
              </div>

              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">Email</label>
                <input
                  v-model="editForm.correo"
                  type="email"
                  class="edit-input-small w-full"
                  :class="{ 'border-red-500': editErrors.correo }"
                  placeholder="Ingresa tu email"
                  required
                />
                <p v-if="editErrors.correo" class="text-red-500 text-xs mt-1">{{ editErrors.correo }}</p>
              </div>

              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">Cargo</label>
                <input
                  v-model="editForm.cargo"
                  type="text"
                  class="edit-input-small w-full"
                  :class="{ 'border-red-500': editErrors.cargo }"
                  placeholder="Ingresa tu cargo"
                  required
                />
                <p v-if="editErrors.cargo" class="text-red-500 text-xs mt-1">{{ editErrors.cargo }}</p>
              </div>

              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">Supervisor</label>
                <input
                  v-model="editForm.supervisor"
                  type="text"
                  class="edit-input-small w-full"
                  placeholder="Ingresa el nombre de tu supervisor"
                />
              </div>

              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">CURP</label>
                <input
                  v-model="editForm.curp"
                  type="text"
                  class="edit-input-small w-full"
                  :class="{ 'border-red-500': editErrors.curp }"
                  placeholder="Ingresa tu CURP"
                  maxlength="18"
                />
                <p v-if="editErrors.curp" class="text-red-500 text-xs mt-1">{{ editErrors.curp }}</p>
              </div>

              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">Teléfono</label>
                <div class="flex space-x-2">
                  <!-- Selector de código de país -->
                  <div class="relative">
                    <button 
                      type="button"
                      @click="showCountrySelector = !showCountrySelector"
                      class="edit-input-small flex items-center px-2 py-1 min-w-[70px] justify-between text-xs"
                    >
                      <div class="flex items-center">
                        <span class="text-xs mr-1">{{ paises.find(p => p.codigo === editForm.codigoPais)?.bandera || '🌎' }}</span>
                        <span class="text-xs font-medium">{{ editForm.codigoPais }}</span>
                      </div>
                      <svg class="w-2 h-2 ml-1 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                      </svg>
                    </button>
                    
                    <!-- Dropdown para selección de país -->
                    <div 
                      v-if="showCountrySelector" 
                      class="absolute z-50 w-56 top-full left-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-xl overflow-hidden"
                    >
                      <!-- Barra de búsqueda -->
                      <div class="sticky top-0 bg-white p-2 border-b border-gray-200">
                        <input 
                          type="text"
                          v-model="countrySearch"
                          placeholder="Buscar país..."
                          class="w-full px-2 py-1 border border-gray-300 rounded text-xs focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                          @click="$event.stopPropagation()"
                        />
                      </div>
                      
                      <ul class="py-1 max-h-40 overflow-y-auto">
                        <li 
                          v-for="pais in filteredCountries" 
                          :key="pais.codigo"
                          @click="selectCountry(pais)"
                          class="flex items-center px-2 py-1 hover:bg-gray-100 cursor-pointer transition-colors"
                        >
                          <span class="text-xs mr-2">{{ pais.bandera }}</span>
                          <span class="flex-1 text-xs">{{ pais.nombre }}</span>
                          <span class="text-gray-500 font-mono text-xs">{{ pais.codigo }}</span>
                        </li>
                        <li v-if="filteredCountries.length === 0" class="px-2 py-1 text-gray-500 text-center text-xs">
                          No se encontraron países
                        </li>
                      </ul>
                    </div>
                  </div>
                  
                  <!-- Campo de entrada del número -->
                  <div class="flex-1">
                    <input
                      v-model="editForm.telefonoDigitos"
                      type="tel"
                      class="edit-input-small w-full"
                      placeholder="10 dígitos"
                      maxlength="10"
                      @input="validatePhoneEdit"
                    />
                  </div>
                </div>
                <p class="mt-1 text-xs text-gray-500">Ingresa solo los 10 dígitos de tu número (sin lada)</p>
              </div>

              <div class="flex space-x-2 pt-3">
                <button
                  type="button"
                  @click="closeEditModal"
                  class="flex-1 px-3 py-1.5 border border-gray-300 rounded-lg text-gray-700 bg-white hover:bg-gray-50 text-xs font-medium transition-colors"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  :disabled="isUpdatingUser"
                  class="flex-1 px-3 py-1.5 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg text-xs font-medium hover:from-green-600 hover:to-green-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                >
                  <svg v-if="isUpdatingUser" class="animate-spin h-3 w-3 mr-2" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ isUpdatingUser ? 'Guardando...' : 'Guardar Cambios' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </transition>

    <!-- Modal de éxito para edición -->
    <transition name="fade">
      <div v-if="showEditSuccessModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-3" style="z-index: 70;">
        <div class="bg-white rounded-2xl max-w-xs w-full mx-3 p-6 text-center">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
          <h3 class="text-lg font-bold text-gray-900 mb-2">¡Información actualizada!</h3>
          <p class="text-sm text-gray-600 mb-4">Tus datos personales han sido actualizados correctamente.</p>
          <button @click="showEditSuccessModal = false" class="w-full px-4 py-2 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg font-medium hover:from-green-600 hover:to-green-700 transition-all">
            Entendido
          </button>
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

// Variables reactivas para edición de información personal
const showEditModal = ref(false)
const showEditSuccessModal = ref(false)
const isUpdatingUser = ref(false)
const editErrors = ref({})
const editForm = ref({
  nombre_completo: '',
  correo: '',
  cargo: '',
  supervisor: '',
  curp: '',
  telefono: '',
  codigoPais: '+52',
  telefonoDigitos: ''
})

// Variables para selector de país
const showCountrySelector = ref(false)
const countrySearch = ref('')

// Lista de países más comunes con sus códigos y banderas
const paises = [
  { codigo: '+52', nombre: 'México', bandera: '🇲🇽' },
  { codigo: '+1', nombre: 'Estados Unidos', bandera: '🇺🇸' },
  { codigo: '+34', nombre: 'España', bandera: '🇪🇸' },
  { codigo: '+57', nombre: 'Colombia', bandera: '🇨🇴' },
  { codigo: '+56', nombre: 'Chile', bandera: '🇨🇱' },
  { codigo: '+54', nombre: 'Argentina', bandera: '🇦🇷' },
  { codigo: '+51', nombre: 'Perú', bandera: '🇵🇪' },
  { codigo: '+591', nombre: 'Bolivia', bandera: '🇧🇴' },
  { codigo: '+502', nombre: 'Guatemala', bandera: '🇬🇹' },
  { codigo: '+503', nombre: 'El Salvador', bandera: '🇸🇻' }
]

// Filtro de países basado en la búsqueda
const filteredCountries = computed(() => {
  if (!countrySearch.value) return paises
  
  const searchTerm = countrySearch.value.toLowerCase()
  return paises.filter(pais => 
    pais.nombre.toLowerCase().includes(searchTerm) || 
    pais.codigo.includes(searchTerm)
  )
})

onMounted(() => {
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    user.value = JSON.parse(storedUser)
    
    // Cargar los datos completos del usuario desde el backend
    loadUserData()
  }

  // Event listeners para cerrar el selector de país
  document.addEventListener('click', closeCountrySelector)
  document.addEventListener('keydown', handleEscKey)
})

// Función para cerrar el selector de país al hacer clic fuera
const closeCountrySelector = (e) => {
  if (e.target.closest('button') && e.target.closest('button').contains(document.querySelector('svg')) || 
      e.target.closest('div') && e.target.closest('div').querySelector && e.target.closest('div').querySelector('input[placeholder="Buscar país..."]')) {
    return
  }
  showCountrySelector.value = false
}

// Función para cerrar con tecla Escape
const handleEscKey = (event) => {
  if (event.key === 'Escape' && showCountrySelector.value) {
    showCountrySelector.value = false
  }
}

const loadUserData = async () => {
  try {
    console.log('🔍 Cargando datos del usuario ID:', user.value.id)
    console.log('📋 Datos iniciales del user:', user.value)
    
    const online = await checkInternetConnection()
    if (!online) {
      console.log('❌ Sin conexión, usando datos del localStorage')
      return
    }
    
    console.log('🌐 Haciendo petición a:', `${API_URL}/usuarios/${user.value.id}`)
    
    const response = await axios.get(`${API_URL}/usuarios/${user.value.id}`, {
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    console.log('📡 Respuesta status:', response.status)
    
    if (response.status === 200) {
      const userData = response.data
      console.log('📊 Datos RAW del backend:', userData)
      console.log('👀 Supervisor:', userData.supervisor)
      console.log('� CURP:', userData.curp)
      console.log('👀 Teléfono:', userData.telefono)
      
      // No incluir la contraseña para seguridad
      delete userData.contrasena
      
      // Actualizar los datos del usuario
      user.value = {
        ...user.value,
        ...userData
      }
      
      console.log('✅ Datos del usuario FINALES:', user.value)
      console.log('🔎 user.supervisor final:', user.value.supervisor)
      console.log('🔎 user.curp final:', user.value.curp)
      console.log('🔎 user.telefono final:', user.value.telefono)
      
      // Actualizar también el localStorage con los datos completos
      localStorage.setItem('user', JSON.stringify(user.value))
      
      console.log('✅ Datos del usuario actualizados desde el backend')
    }
  } catch (error) {
    console.error('❌ Error al cargar datos completos del usuario:', error)
    if (error.response) {
      console.error('📡 Error response:', error.response.status, error.response.data)
    } else if (error.request) {
      console.error('📡 Error request:', error.request)
    } else {
      console.error('📡 Error message:', error.message)
    }
  }
}

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

// Función para abrir el modal de edición
const openEditModal = () => {
  // Extraer código de país y dígitos del teléfono actual
  let codigoPais = '+52'
  let telefonoDigitos = ''
  
  if (user.value.telefono) {
    const telefonoCompleto = user.value.telefono.toString()
    // Buscar coincidencia con códigos de país conocidos
    const paisEncontrado = paises.find(pais => telefonoCompleto.startsWith(pais.codigo))
    if (paisEncontrado) {
      codigoPais = paisEncontrado.codigo
      telefonoDigitos = telefonoCompleto.slice(paisEncontrado.codigo.length)
    } else {
      // Si no encuentra coincidencia, asumir que es completo sin código
      telefonoDigitos = telefonoCompleto
    }
  }
  
  // Cargar los datos actuales en el formulario
  editForm.value = {
    nombre_completo: user.value.nombre_completo || '',
    correo: user.value.correo || '',
    cargo: user.value.cargo || '',
    supervisor: user.value.supervisor || '',
    curp: user.value.curp || '',
    telefono: user.value.telefono || '',
    codigoPais: codigoPais,
    telefonoDigitos: telefonoDigitos
  }
  
  // Resetear errores
  editErrors.value = {}
  
  showEditModal.value = true
}

// Función para cerrar el modal de edición
const closeEditModal = () => {
  showEditModal.value = false
  showCountrySelector.value = false
  countrySearch.value = ''
  editForm.value = {
    nombre_completo: '',
    correo: '',
    cargo: '',
    supervisor: '',
    curp: '',
    telefono: '',
    codigoPais: '+52',
    telefonoDigitos: ''
  }
  editErrors.value = {}
}

// Función para actualizar la información del usuario
const updateUserInfo = async () => {
  try {
    console.log('Iniciando actualización de información personal...')
    
    // Resetear errores
    editErrors.value = {}
    
    // Validaciones
    if (!editForm.value.nombre_completo?.trim()) {
      editErrors.value.nombre_completo = 'El nombre completo es obligatorio'
      return
    }
    
    if (!editForm.value.correo?.trim()) {
      editErrors.value.correo = 'El email es obligatorio'
      return
    }
    
    // Validar formato de email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(editForm.value.correo)) {
      editErrors.value.correo = 'El formato del email no es válido'
      return
    }
    
    if (!editForm.value.cargo?.trim()) {
      editErrors.value.cargo = 'El cargo es obligatorio'
      return
    }
    
    // Validar CURP si se proporciona
    if (editForm.value.curp && editForm.value.curp.length > 0) {
      if (editForm.value.curp.length !== 18) {
        editErrors.value.curp = 'El CURP debe tener exactamente 18 caracteres'
        return
      }
    }
    
    isUpdatingUser.value = true
    
    // Verificar conexión a internet
    const online = await checkInternetConnection()
    if (!online) {
      editErrors.value.general = getOfflineMessage()
      return
    }
    
    const storedUser = JSON.parse(localStorage.getItem('user'))
    
    // Construir teléfono completo
    const telefonoCompleto = editForm.value.telefonoDigitos ? 
      `${editForm.value.codigoPais}${editForm.value.telefonoDigitos.trim()}` : null
    
    const response = await axios.patch(`${API_URL}/usuarios/${storedUser.id}/info`, {
      nombre_completo: editForm.value.nombre_completo.trim(),
      correo: editForm.value.correo.trim(),
      cargo: editForm.value.cargo.trim(),
      supervisor: editForm.value.supervisor?.trim() || null,
      curp: editForm.value.curp?.trim() || null,
      telefono: telefonoCompleto
    }, {
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    console.log('Respuesta del servidor:', response.data)
    
    if (response.status === 200 && response.data.success) {
      // Construir teléfono completo para guardar
      const telefonoCompleto = editForm.value.telefonoDigitos ? 
        `${editForm.value.codigoPais}${editForm.value.telefonoDigitos.trim()}` : null
      
      // Actualizar los datos del usuario en el estado local
      user.value = {
        ...user.value,
        nombre_completo: editForm.value.nombre_completo,
        correo: editForm.value.correo,
        cargo: editForm.value.cargo,
        supervisor: editForm.value.supervisor,
        curp: editForm.value.curp,
        telefono: telefonoCompleto
      }
      
      // Actualizar localStorage
      const updatedUser = { 
        ...storedUser, 
        nombre_completo: editForm.value.nombre_completo,
        correo: editForm.value.correo,
        cargo: editForm.value.cargo,
        supervisor: editForm.value.supervisor,
        curp: editForm.value.curp,
        telefono: telefonoCompleto
      }
      localStorage.setItem('user', JSON.stringify(updatedUser))
      
      // Cerrar modal de edición
      closeEditModal()
      
      // Mostrar modal de éxito
      showEditSuccessModal.value = true
      
      // Recargar datos del usuario para asegurar sincronización
      setTimeout(() => {
        loadUserData()
      }, 1000)
    }
    
  } catch (error) {
    console.error('Error al actualizar información:', error)
    
    if (error.response) {
      const errorMsg = error.response.data?.detail || 
                      error.response.data?.message || 
                      'Error al actualizar la información'
      editErrors.value.general = errorMsg
    } else if (error.request) {
      editErrors.value.general = 'No se pudo conectar con el servidor. Verifica tu conexión.'
    } else {
      editErrors.value.general = 'Error al actualizar la información: ' + error.message
    }
  } finally {
    isUpdatingUser.value = false
  }
}

// Función para seleccionar país
const selectCountry = (pais) => {
  editForm.value.codigoPais = pais.codigo
  showCountrySelector.value = false
}

// Función para validar teléfono
const validatePhoneEdit = () => {
  editForm.value.telefonoDigitos = editForm.value.telefonoDigitos.replace(/\D/g, '')
  
  if (editForm.value.telefonoDigitos.length > 10) {
    editForm.value.telefonoDigitos = editForm.value.telefonoDigitos.slice(0, 10)
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
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 6px 25px 0 rgba(31, 38, 135, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  padding: 0.875rem;
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
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  font-size: 0.8rem;
  color: #1f2937;
  transition: all 0.3s ease;
  box-shadow: 
    0 3px 12px 0 rgba(31, 38, 135, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  min-height: 30px;
  padding: 0.5rem;
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
  padding: 0.625rem 1rem;
  border-radius: 10px;
  border: 1px solid rgba(76, 175, 80, 0.3);
  background: linear-gradient(135deg, 
    rgba(76, 175, 80, 0.8) 0%, 
    rgba(56, 142, 60, 0.8) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  color: white;
  font-weight: 600;
  font-size: 0.8rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 3px 15px 0 rgba(76, 175, 80, 0.3),
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
  padding: 0.5rem 0;
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
  width: 40px;
  height: 1.5px;
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
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
  }
  
  .glass-card {
    padding: 0.625rem;
    margin-bottom: 0.375rem;
    border-radius: 12px;
  }
  
  .glass-input {
    font-size: 14px; /* Evita zoom en iOS */
    min-height: 28px;
    padding: 0.375rem;
  }
  
  .text-base {
    font-size: 0.8rem;
  }
  
  .text-sm {
    font-size: 0.75rem;
  }
  
  .w-12, .h-12 {
    width: 2.75rem;
    height: 2.75rem;
  }
  
  .h-6, .w-6 {
    height: 1.25rem;
    width: 1.25rem;
  }
  
  .mb-2 {
    margin-bottom: 0.375rem;
  }
  
  .mb-3 {
    margin-bottom: 0.5rem;
  }
  
  .space-y-3 > * + * {
    margin-top: 0.5rem;
  }
  
  .space-y-2 > * + * {
    margin-top: 0.375rem;
  }
}

@media (max-width: 375px) {
  .page-container {
    padding-left: 0.375rem;
    padding-right: 0.375rem;
    max-width: calc(100vw - 0.75rem);
  }
  
  .glass-card {
    padding: 0.5rem;
    margin-bottom: 0.25rem;
    border-radius: 10px;
  }
  
  .glass-input {
    font-size: 14px;
    min-height: 26px;
    padding: 0.25rem 0.375rem;
  }
  
  .glass-button {
    padding: 0.375rem 0.75rem;
    font-size: 0.75rem;
  }
  
  .text-base {
    font-size: 0.75rem;
  }
  
  .text-sm {
    font-size: 0.7rem;
  }
  
  .text-xs {
    font-size: 0.65rem;
  }
}

@media (max-height: 700px) {
  .page-container {
    padding-top: 0.375rem;
    padding-bottom: 0.375rem;
  }
  
  .glass-card {
    margin-bottom: 0.25rem;
    padding: 0.5rem;
  }
  
  .mb-2 {
    margin-bottom: 0.25rem;
  }
  
  .mb-3 {
    margin-bottom: 0.375rem;
  }
  
  .space-y-3 > * + * {
    margin-top: 0.375rem;
  }
  
  .space-y-2 > * + * {
    margin-top: 0.25rem;
  }
}

@media (max-height: 600px) {
  .page-container {
    max-width: 280px;
    padding: 0.25rem 0.375rem;
  }
  
  .glass-card {
    padding: 0.5rem;
    margin-bottom: 0.125rem;
  }
  
  .w-12, .h-12 {
    width: 2.5rem;
    height: 2.5rem;
  }
  
  .text-base {
    font-size: 0.75rem;
  }
  
  .text-sm {
    font-size: 0.7rem;
  }
}

@media (max-height: 500px) {
  .glass-card {
    padding: 0.375rem;
  }
  
  .mb-1, .mb-2, .mb-3 {
    margin-bottom: 0.125rem;
  }
  
  .space-y-3 > * + * {
    margin-top: 0.25rem;
  }
  
  .space-y-2 > * + * {
    margin-top: 0.125rem;
  }
}

/* Para pantallas grandes */
@media (min-width: 768px) {
  .page-container {
    max-width: 350px;
    padding: 0.75rem;
  }
  
  .glass-card {
    padding: 1rem;
    margin-bottom: 0.75rem;
  }
}

@media (min-width: 1024px) {
  .page-container {
    max-width: 380px;
    padding: 1rem 0.75rem;
  }
  
  .glass-card {
    padding: 1.125rem;
    margin-bottom: 1rem;
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

/* Estilos para modales de edición */
.edit-modal {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Inputs del modal de edición */
.edit-input {
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  background-color: #f9fafb;
}

.edit-input:focus {
  outline: none;
  border-color: #10b981;
  background-color: white;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.edit-input.border-red-500 {
  border-color: #ef4444;
}

.edit-input.border-red-500:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

/* Versión pequeña de inputs para móviles */
.edit-input-small {
  padding: 0.5rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.75rem;
  transition: all 0.2s ease;
  background-color: #f9fafb;
}

.edit-input-small:focus {
  outline: none;
  border-color: #10b981;
  background-color: white;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1);
}

.edit-input-small.border-red-500 {
  border-color: #ef4444;
}

.edit-input-small.border-red-500:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.1);
}

/* Botón de edición circular mejorado */
.glass-edit-button {
  width: 2rem;
  height: 2rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #374151;
  transition: all 0.2s ease;
  cursor: pointer;
}

.glass-edit-button:hover {
  background: rgba(16, 185, 129, 0.1);
  border-color: rgba(16, 185, 129, 0.3);
  color: #10b981;
  transform: scale(1.05);
}

.glass-edit-button:active {
  transform: scale(0.95);
}
</style>
