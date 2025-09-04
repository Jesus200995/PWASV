import { ref } from 'vue'

// Estado global del modo mantenimiento
export const isMaintenanceMode = ref(false)
export const maintenanceMessage = ref('')

// Función para actualizar el estado
export const setMaintenanceState = (enabled, message = '') => {
  isMaintenanceMode.value = enabled
  maintenanceMessage.value = message
}

// Función para verificar si está en modo mantenimiento
export const getMaintenanceState = () => ({
  enabled: isMaintenanceMode.value,
  message: maintenanceMessage.value
})
