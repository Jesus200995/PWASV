// Composable para manejar el modal de logout de forma global
import { ref } from 'vue'

// Estado global del modal de logout
const showLogoutModal = ref(false)
let logoutCallback = null

export function useLogoutModal() {
  const openLogoutModal = (callback = null) => {
    logoutCallback = callback
    showLogoutModal.value = true
  }

  const closeLogoutModal = () => {
    showLogoutModal.value = false
    logoutCallback = null
  }

  const confirmLogout = () => {
    showLogoutModal.value = false
    if (logoutCallback) {
      logoutCallback()
    }
    logoutCallback = null
  }

  return {
    showLogoutModal,
    openLogoutModal,
    closeLogoutModal,
    confirmLogout
  }
}
