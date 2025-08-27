<template>
  <div class="push-notifications-setup">
    <!-- Card principal -->
    <div class="glass-card p-4 mb-4">
      <!-- Header -->
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center space-x-3">
          <div class="text-2xl">{{ statusIcon }}</div>
          <div>
            <h3 class="text-lg font-semibold text-gray-800">
              Notificaciones Push
            </h3>
            <p class="text-sm text-gray-600">
              Recibe alertas instantáneas
            </p>
          </div>
        </div>
        
        <!-- Toggle switch -->
        <div class="flex items-center space-x-2">
          <button
            v-if="canSubscribe && !needsPermission"
            @click="handleToggle"
            :disabled="isLoading"
            :class="[
              'relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200',
              isSubscribed 
                ? 'bg-green-600 hover:bg-green-700' 
                : 'bg-gray-200 hover:bg-gray-300',
              isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
            ]"
          >
            <span class="sr-only">{{ isSubscribed ? 'Desactivar' : 'Activar' }} notificaciones</span>
            <span
              :class="[
                'inline-block h-4 w-4 transform rounded-full bg-white transition-transform duration-200',
                isSubscribed ? 'translate-x-6' : 'translate-x-1'
              ]"
            />
          </button>
          
          <!-- Indicador de carga -->
          <div v-if="isLoading" class="animate-spin rounded-full h-5 w-5 border-2 border-green-500 border-t-transparent"></div>
        </div>
      </div>

      <!-- Mensaje de estado -->
      <div class="mb-4">
        <p class="text-sm text-gray-700 leading-relaxed">
          {{ statusMessage }}
        </p>
      </div>

      <!-- Acciones según el estado -->
      <div class="space-y-3">
        
        <!-- Botón para solicitar permisos -->
        <button
          v-if="needsPermission"
          @click="handleRequestPermission"
          :disabled="isLoading"
          class="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-medium rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5-5-5h5v-12z" />
          </svg>
          <span>Permitir Notificaciones</span>
        </button>

        <!-- Botón para activar notificaciones -->
        <button
          v-else-if="canSubscribe && !isSubscribed"
          @click="handleSubscribe"
          :disabled="isLoading"
          class="w-full py-3 px-4 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white font-medium rounded-lg transition-colors duration-200 flex items-center justify-center space-x-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5-5-5h5v-12z" />
          </svg>
          <span>Activar Notificaciones Push</span>
        </button>

        <!-- Información cuando está bloqueado -->
        <div v-else-if="isBlocked" class="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-r-lg">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <div class="ml-3">
              <h4 class="text-sm font-medium text-yellow-800">
                Notificaciones bloqueadas
              </h4>
              <p class="text-sm text-yellow-700 mt-1">
                Para habilitar: ve a la configuración del navegador → Notificaciones → permite este sitio.
              </p>
            </div>
          </div>
        </div>

        <!-- Información cuando no es soportado -->
        <div v-else-if="!isSupported" class="bg-red-50 border-l-4 border-red-400 p-4 rounded-r-lg">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <div class="ml-3">
              <h4 class="text-sm font-medium text-red-800">
                No soportado
              </h4>
              <p class="text-sm text-red-700 mt-1">
                Tu navegador no soporta notificaciones push. Actualiza tu navegador o usa uno compatible.
              </p>
            </div>
          </div>
        </div>

      </div>

      <!-- Botones de prueba (solo en desarrollo) -->
      <div v-if="isDev && isSubscribed" class="mt-4 pt-4 border-t border-gray-200">
        <div class="flex space-x-2">
          <button
            @click="handleTestNotification"
            class="flex-1 py-2 px-3 bg-purple-100 hover:bg-purple-200 text-purple-800 text-sm rounded-lg transition-colors duration-200"
          >
            🧪 Probar
          </button>
          <button
            @click="showDebugInfo"
            class="flex-1 py-2 px-3 bg-gray-100 hover:bg-gray-200 text-gray-800 text-sm rounded-lg transition-colors duration-200"
          >
            🔍 Debug
          </button>
        </div>
      </div>
      
      <!-- Error message -->
      <div v-if="error" class="mt-4 p-3 bg-red-100 border border-red-400 rounded-lg">
        <div class="flex justify-between items-start">
          <p class="text-red-700 text-sm">
            {{ error }}
          </p>
          <button
            @click="clearError"
            class="text-red-400 hover:text-red-600 ml-2"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Información adicional -->
    <div class="bg-blue-50 border-l-4 border-blue-400 p-4 rounded-r-lg">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div class="ml-3">
          <h4 class="text-sm font-medium text-blue-800">
            ¿Cómo funcionan las notificaciones push?
          </h4>
          <p class="text-sm text-blue-700 mt-1">
            Las notificaciones push aparecerán en tu dispositivo incluso cuando la aplicación esté cerrada.
            Recibirás alertas instantáneas sobre nuevas notificaciones importantes.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineEmits } from 'vue'
import { usePushNotifications } from '../composables/usePushNotifications.js'

// Props
const props = defineProps({
  usuarioId: {
    type: [Number, String],
    required: true
  }
})

// Emits
const emit = defineEmits(['subscribed', 'unsubscribed', 'error'])

// Usar composable de push notifications
const {
  isSupported,
  permission,
  isSubscribed,
  isLoading,
  error,
  canSubscribe,
  needsPermission,
  isBlocked,
  statusMessage,
  statusIcon,
  subscribe,
  unsubscribe,
  requestPermission,
  showTestNotification,
  getDebugInfo,
  clearError
} = usePushNotifications()

// Computed
const isDev = computed(() => import.meta.env.DEV)

// Métodos
const handleRequestPermission = async () => {
  try {
    const granted = await requestPermission()
    if (granted) {
      console.log('✅ Permisos concedidos')
    }
  } catch (err) {
    console.error('❌ Error solicitando permisos:', err)
    emit('error', err.message)
  }
}

const handleSubscribe = async () => {
  try {
    const success = await subscribe(props.usuarioId)
    if (success) {
      console.log('✅ Suscripción exitosa')
      emit('subscribed')
    }
  } catch (err) {
    console.error('❌ Error en suscripción:', err)
    emit('error', err.message)
  }
}

const handleUnsubscribe = async () => {
  try {
    const success = await unsubscribe(props.usuarioId)
    if (success) {
      console.log('✅ Desuscripción exitosa')
      emit('unsubscribed')
    }
  } catch (err) {
    console.error('❌ Error en desuscripción:', err)
    emit('error', err.message)
  }
}

const handleToggle = async () => {
  if (isSubscribed.value) {
    await handleUnsubscribe()
  } else {
    await handleSubscribe()
  }
}

const handleTestNotification = async () => {
  try {
    await showTestNotification()
  } catch (err) {
    console.error('❌ Error mostrando notificación de prueba:', err)
  }
}

const showDebugInfo = () => {
  const info = getDebugInfo()
  console.log('🔍 Push Notifications Debug Info:', info)
  alert(JSON.stringify(info, null, 2))
}
</script>

<style scoped>
.glass-card {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 6px 25px 0 rgba(31, 38, 135, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.05);
}

/* Animación para el toggle switch */
.push-notifications-setup button[role="switch"] {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Hover effects */
.push-notifications-setup button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.push-notifications-setup button:active:not(:disabled) {
  transform: translateY(0);
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .glass-card {
    padding: 1rem;
    margin-bottom: 1rem;
  }
  
  .push-notifications-setup h3 {
    font-size: 1rem;
  }
  
  .push-notifications-setup p {
    font-size: 0.875rem;
  }
}
</style>
