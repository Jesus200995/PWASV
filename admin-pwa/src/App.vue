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
import sessionCheckService from './services/sessionCheckService.js'
import SessionExpiredModal from './components/SessionExpiredModal.vue'

const router = useRouter()

// Estado del modal de sesión
const showSessionModal = ref(false)
const sessionModalConfig = ref({
  title: 'Cuenta Desactivada',
  message: 'Tu cuenta ha sido desactivada. Contacta al administrador.',
  iconType: 'deactivated'
})

let removeSessionListener = null

// Handler para sesión invalidada (nuevo sistema reactivo)
const handleSessionInvalid = (reason, newVersion) => {
  console.log('🔒 Sesión invalidada detectada:', reason)
  
  // Configurar mensajes según la razón
  if (reason === 'password_changed') {
    sessionModalConfig.value = {
      title: 'Contraseña Actualizada',
      message: 'Tu contraseña ha sido actualizada desde otro dispositivo. Por seguridad, debes iniciar sesión nuevamente.',
      iconType: 'refresh'
    }
  } else if (reason === 'user_not_found') {
    sessionModalConfig.value = {
      title: 'Usuario No Encontrado',
      message: 'Tu cuenta de usuario ya no existe en el sistema.',
      iconType: 'deleted'
    }
  } else {
    sessionModalConfig.value = {
      title: 'Sesión Finalizada',
      message: 'Tu sesión ha sido cerrada por motivos de seguridad.',
      iconType: 'deactivated'
    }
  }
  
  showSessionModal.value = true
  sessionCheckService.stopSessionCheck()
}

// Handler para mostrar el modal de sesión expirada (sistema anterior)
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
  // Limpiar sesión
  localStorage.removeItem('admin_token')
  localStorage.removeItem('admin_user')
}

const handleRedirectToLogin = () => {
  showSessionModal.value = false
  // Limpiar sesión
  localStorage.removeItem('admin_token')
  localStorage.removeItem('admin_user')
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
    
    // Sistema antiguo de verificación
    authService.startSessionCheck()
    
    // Nuevo sistema reactivo de verificación de contraseña
    removeSessionListener = sessionCheckService.onSessionInvalid(handleSessionInvalid)
    sessionCheckService.startSessionCheck()
  }
  
  // Escuchar evento de forzar logout
  window.addEventListener('force-logout', handleForceLogout)
  
  // Escuchar evento de forzar refresh (cambio de rol)
  window.addEventListener('force-refresh', handleForceRefresh)
})

onUnmounted(() => {
  // Limpiar listeners
  window.removeEventListener('force-logout', handleForceLogout)
  window.removeEventListener('force-refresh', handleForceRefresh)
  
  // Remover listener de sesión
  if (removeSessionListener) {
    removeSessionListener()
  }
  
  // Detener verificación de sesión
  sessionCheckService.stopSessionCheck()
})
</script>
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

html, body {
  min-height: 100vh;
  background-color: #f5f5f5 !important;
  color: #333 !important;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

#app {
  min-height: 100vh;
  background-color: #f5f5f5 !important;
}

/* Evitar pantalla negra durante carga */
#app:empty::before {
  content: 'Cargando...';
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 18px;
  color: #666;
  background-color: #f5f5f5;
}
</style>
