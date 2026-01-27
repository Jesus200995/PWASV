<template>
  <div v-if="visible" class="cargo-modal-overlay">
    <div class="cargo-modal">
      <div class="cargo-modal-header">
        <div class="cargo-icon">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
          </svg>
        </div>
        <h2>Selecciona tu Cargo</h2>
      </div>
      
      <div class="cargo-modal-warning">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
        </svg>
        <p><strong>¡Importante!</strong> Selecciona correctamente tu cargo. De lo contrario, podrías perder el acceso a tu información.</p>
      </div>

      <!-- Select de cargo -->
      <div class="cargo-select-container">
        <label class="cargo-select-label">Tu cargo:</label>
        <select v-model="cargoSeleccionado" class="cargo-select">
          <option value="" disabled>-- Selecciona tu cargo --</option>
          <option v-for="cargo in cargosDisponibles" :key="cargo" :value="cargo">
            {{ cargo }}
          </option>
        </select>
      </div>

      <!-- Campo para OTRO -->
      <div v-if="cargoSeleccionado === 'OTRO'" class="cargo-otro-container">
        <label class="cargo-otro-label">Escribe tu cargo:</label>
        <input 
          type="text" 
          v-model="cargoOtroTexto"
          @input="convertirMayusculas"
          placeholder="ESCRIBE TU CARGO AQUI"
          class="cargo-otro-input"
          maxlength="100"
        />
      </div>

      <button 
        class="cargo-submit-btn"
        :disabled="!puedeGuardar || guardando"
        @click="guardarCargo"
      >
        <span v-if="guardando" class="loading-spinner"></span>
        <span v-else>Confirmar Cargo</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { apiService } from '../services/apiService'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['cargo-guardado'])

const cargosDisponibles = [
  'TECNICO PRODUCTIVO',
  'TECNICO SOCIAL',
  'FACILITADOR COMUNITARIO',
  'COORDINACION TERRITORIAL C',
  'COORDINACION TERRITORIAL B',
  'COORDINACION TERRITORIAL A',
  'ESPECIALISTAS PRODUCTIVOS Y SOCIALES',
  'SEMBRADOR',
  'OTRO'
]

const cargoSeleccionado = ref('')
const cargoOtroTexto = ref('')
const guardando = ref(false)

const puedeGuardar = computed(() => {
  if (!cargoSeleccionado.value) return false
  if (cargoSeleccionado.value === 'OTRO') {
    return cargoOtroTexto.value.trim().length >= 3
  }
  return true
})

const convertirMayusculas = () => {
  // Convertir a mayúsculas y quitar tildes
  cargoOtroTexto.value = cargoOtroTexto.value
    .toUpperCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
}

const guardarCargo = async () => {
  if (!puedeGuardar.value || guardando.value) return
  
  guardando.value = true
  
  try {
    const cargoFinal = cargoSeleccionado.value === 'OTRO' 
      ? cargoOtroTexto.value.trim() 
      : cargoSeleccionado.value
    
    // Obtener usuario del localStorage
    const userStr = localStorage.getItem('user')
    if (!userStr) {
      alert('Error: No se encontró información del usuario')
      guardando.value = false
      return
    }
    
    const user = JSON.parse(userStr)
    
    // Llamar al API para actualizar cargo
    const response = await apiService.actualizarCargo(user.id, cargoFinal)
    
    if (response.success) {
      // Actualizar localStorage
      user.cargo = cargoFinal
      localStorage.setItem('user', JSON.stringify(user))
      
      emit('cargo-guardado', cargoFinal)
    } else {
      alert('Error al guardar el cargo: ' + (response.message || 'Intenta de nuevo'))
    }
  } catch (error) {
    console.error('Error guardando cargo:', error)
    alert('Error de conexión. Verifica tu internet e intenta de nuevo.')
  } finally {
    guardando.value = false
  }
}
</script>

<style scoped>
.cargo-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
  padding: 16px;
  backdrop-filter: blur(4px);
}

.cargo-modal {
  background: linear-gradient(145deg, #064e3b 0%, #065f46 50%, #047857 100%);
  border-radius: 20px;
  padding: 24px;
  width: 100%;
  max-width: 400px;
  max-height: 90vh;
  overflow-y: auto;
  border: 2px solid #10b981;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 40px rgba(16, 185, 129, 0.2);
}

.cargo-modal-header {
  text-align: center;
  margin-bottom: 20px;
}

.cargo-icon {
  width: 70px;
  height: 70px;
  margin: 0 auto 14px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.cargo-icon svg {
  width: 36px;
  height: 36px;
  color: white;
}

.cargo-modal-header h2 {
  color: #fff;
  font-size: 22px;
  font-weight: 700;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.cargo-modal-warning {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  background: rgba(251, 191, 36, 0.2);
  border: 1px solid rgba(251, 191, 36, 0.5);
  border-radius: 12px;
  padding: 14px;
  margin-bottom: 24px;
}

.cargo-modal-warning svg {
  width: 26px;
  height: 26px;
  color: #fbbf24;
  flex-shrink: 0;
}

.cargo-modal-warning p {
  color: #fef3c7;
  font-size: 13px;
  margin: 0;
  line-height: 1.5;
}

.cargo-select-container {
  margin-bottom: 20px;
}

.cargo-select-label {
  display: block;
  color: #d1fae5;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 10px;
}

.cargo-select {
  width: 100%;
  padding: 14px 16px;
  background: rgba(0, 0, 0, 0.3);
  border: 2px solid #10b981;
  border-radius: 12px;
  color: #fff;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2310b981' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 20px;
}

.cargo-select:focus {
  outline: none;
  border-color: #34d399;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.3);
}

.cargo-select option {
  background: #064e3b;
  color: #fff;
  padding: 12px;
}

.cargo-otro-container {
  margin-bottom: 20px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.cargo-otro-label {
  display: block;
  color: #d1fae5;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 10px;
}

.cargo-otro-input {
  width: 100%;
  padding: 14px 16px;
  background: rgba(0, 0, 0, 0.3);
  border: 2px solid #10b981;
  border-radius: 12px;
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  text-transform: uppercase;
  box-sizing: border-box;
}

.cargo-otro-input:focus {
  outline: none;
  border-color: #34d399;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.3);
}

.cargo-otro-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.cargo-submit-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.cargo-submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4);
}

.cargo-submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  width: 22px;
  height: 22px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 480px) {
  .cargo-modal {
    padding: 20px 16px;
    max-height: 85vh;
    margin: 0 8px;
  }
  
  .cargo-icon {
    width: 60px;
    height: 60px;
  }
  
  .cargo-icon svg {
    width: 30px;
    height: 30px;
  }
  
  .cargo-modal-header h2 {
    font-size: 20px;
  }
  
  .cargo-select {
    font-size: 14px;
    padding: 12px 14px;
  }
}
</style>
