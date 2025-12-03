<template>
  <div id="app">
    <router-view />
    
    <!-- Modal de sesión expirada/desactivada -->
    <SessionExpiredModal
      :isVisible="showSessionModal"
      :title="sessionModalConfig.title"
      :message="sessionModalConfig.message"
      :iconType="sessionModalConfig.iconType"
      @close="handleSessionModalClose"
      @redirect="handleRedirectToLogin"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import authService from './services/authService.js'
import SessionExpiredModal from './components/SessionExpiredModal.vue'

const router = useRouter()

// Estado del modal de sesión
const showSessionModal = ref(false)
const sessionModalConfig = ref({
  title: 'Cuenta Desactivada',
  message: 'Tu cuenta ha sido desactivada. Contacta al administrador.',
  iconType: 'deactivated'
})

// Handler para mostrar el modal de sesión expirada
const handleForceLogout = (event) => {
  const { reason, message } = event.detail || {}
  
  // Configurar el modal según el motivo
  if (reason === 'deleted') {
    sessionModalConfig.value = {
      title: 'Cuenta Eliminada',
      message: message || 'Tu cuenta ha sido eliminada del sistema.',
      iconType: 'deleted'
    }
  } else if (reason === 'expired') {
    sessionModalConfig.value = {
      title: 'Sesión Expirada',
      message: message || 'Tu sesión ha expirado. Por favor, inicia sesión nuevamente.',
      iconType: 'expired'
    }
  } else {
    // Default: desactivada
    sessionModalConfig.value = {
      title: 'Cuenta Desactivada',
      message: message || 'Tu cuenta ha sido desactivada. Contacta al administrador.',
      iconType: 'deactivated'
    }
  }
  
  showSessionModal.value = true
}

const handleSessionModalClose = () => {
  showSessionModal.value = false
}

const handleRedirectToLogin = () => {
  showSessionModal.value = false
  router.push('/login')
}

// Handler para forzar refresh cuando cambia el rol
const handleForceRefresh = (event) => {
  const { reason, message } = event.detail || {}
  
  if (reason === 'role-changed') {
    sessionModalConfig.value = {
      title: 'Actualizando Permisos',
      message: message || 'Se están aplicando los cambios de configuración...',
      iconType: 'refresh'
    }
    showSessionModal.value = true
    
    // El refresh se hace automáticamente desde authService después de 500ms
  }
}

// Iniciar verificación de sesión en tiempo real si el usuario ya está logueado
onMounted(() => {
  if (authService.isAuthenticated()) {
    console.log('🔄 Usuario ya logueado, iniciando verificación de sesión en tiempo real')
    authService.startSessionCheck()
  }
  
  // Escuchar evento de forzar logout
  window.addEventListener('force-logout', handleForceLogout)
  
  // Escuchar evento de forzar refresh (cambio de rol)
  window.addEventListener('force-refresh', handleForceRefresh)
})

// Detener verificación al desmontar
onUnmounted(() => {
  authService.stopSessionCheck()
  window.removeEventListener('force-logout', handleForceLogout)
  window.removeEventListener('force-refresh', handleForceRefresh)
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: #f5f5f5;
}

#app {
  min-height: 100vh;
}
</style>
