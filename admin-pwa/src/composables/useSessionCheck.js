// useSessionCheck.js
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import sessionCheckService from '../services/sessionCheckService'

export function useSessionCheck() {
  const router = useRouter()
  const showSessionExpiredModal = ref(false)
  const sessionExpiredReason = ref('password_changed')
  const sessionExpiredTitle = ref('Contraseña Actualizada')
  const sessionExpiredMessage = ref('Tu contraseña ha sido actualizada desde otro dispositivo.')
  
  let removeListener = null

  const handleSessionInvalid = (reason, newVersion) => {
    console.log('🔒 Sesión invalidada detectada:', reason)
    
    // Configurar mensajes según la razón
    switch (reason) {
      case 'password_changed':
        sessionExpiredTitle.value = 'Contraseña Actualizada'
        sessionExpiredMessage.value = 'Tu contraseña ha sido actualizada desde otro dispositivo. Por seguridad, debes iniciar sesión nuevamente.'
        sessionExpiredReason.value = 'refresh'
        break
      case 'user_not_found':
        sessionExpiredTitle.value = 'Usuario No Encontrado'
        sessionExpiredMessage.value = 'Tu cuenta de usuario ya no existe en el sistema.'
        sessionExpiredReason.value = 'deleted'
        break
      default:
        sessionExpiredTitle.value = 'Sesión Finalizada'
        sessionExpiredMessage.value = 'Tu sesión ha sido cerrada por motivos de seguridad.'
        sessionExpiredReason.value = 'deactivated'
    }
    
    // Mostrar modal
    showSessionExpiredModal.value = true
    
    // Detener verificación
    sessionCheckService.stopSessionCheck()
  }

  const handleModalClose = () => {
    showSessionExpiredModal.value = false
    // Limpiar datos de sesión
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_user')
    // Redirigir al login
    router.push('/login')
  }

  const startSessionChecking = () => {
    // Registrar listener para eventos de sesión invalidada
    removeListener = sessionCheckService.onSessionInvalid(handleSessionInvalid)
    
    // Iniciar verificación periódica
    sessionCheckService.startSessionCheck()
  }

  const stopSessionChecking = () => {
    // Remover listener
    if (removeListener) {
      removeListener()
      removeListener = null
    }
    
    // Detener verificación
    sessionCheckService.stopSessionCheck()
  }

  // Iniciar cuando se monta el componente
  onMounted(() => {
    startSessionChecking()
  })

  // Limpiar cuando se desmonta
  onUnmounted(() => {
    stopSessionChecking()
  })

  return {
    showSessionExpiredModal,
    sessionExpiredReason,
    sessionExpiredTitle,
    sessionExpiredMessage,
    handleModalClose,
    startSessionChecking,
    stopSessionChecking
  }
}
