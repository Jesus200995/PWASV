<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="isVisible" class="territorio-modal-overlay" @click.stop>
        <Transition name="modal-scale">
          <div v-if="isVisible" class="territorio-modal">
            <!-- Icono decorativo -->
            <div class="modal-icon-container">
              <svg class="modal-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
              <div class="icon-pulse"></div>
            </div>

            <!-- Título -->
            <h2 class="modal-title">Selecciona tu Territorio</h2>

            <!-- Mensaje -->
            <p class="modal-message">
              Indica el territorio de Sembrando Vida donde te encuentras
            </p>

            <!-- Advertencia -->
            <p class="modal-advertencia">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                <line x1="12" y1="9" x2="12" y2="13"/>
                <line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
              Selecciona cuidadosamente tu territorio
            </p>

            <!-- Selector de estado -->
            <div class="select-container">
              <select 
                id="territorio-select" 
                v-model="selectedTerritorio" 
                class="territorio-select"
                :class="{ 'has-value': selectedTerritorio }"
              >
                <option value="" disabled>-- Selecciona un territorio --</option>
                <option v-for="territorio in territorios" :key="territorio" :value="territorio">
                  {{ territorio }}
                </option>
              </select>
            </div>

            <!-- Botón de confirmar -->
            <button 
              class="confirm-button" 
              :disabled="!selectedTerritorio || saving"
              @click="confirmarTerritorio"
            >
              <svg v-if="saving" class="animate-spin" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
              </svg>
              <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              <span>{{ saving ? 'Guardando...' : 'Continuar' }}</span>
            </button>

            <!-- Aviso obligatorio -->
            <p class="aviso-obligatorio">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              Es obligatorio seleccionar tu territorio para continuar con el acceso normal de la aplicación
            </p>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false
  },
  userId: {
    type: [Number, String],
    required: true
  }
})

const emit = defineEmits(['territorio-saved'])

const API_URL = 'https://apipwa.sembrandodatos.com'

const selectedTerritorio = ref('')
const saving = ref(false)

// Lista de territorios de Sembrando Vida
const territorios = ref([
  "Acapulco- Centro- Norte- Tierra Caliente",
  "Acayucan",
  "Balancán",
  "Chihuahua / Sonora",
  "Colima",
  "Comalcalco",
  "Córdoba",
  "Costa Chica - Montaña",
  "Costa Grande- Sierra",
  "Durango / Zacatecas",
  "Hidalgo",
  "Istmo",
  "Michoacán",
  "Mixteca",
  "Morelos",
  "Nayarit / Jalisco",
  "Ocosingo",
  "Palenque",
  "Papantla",
  "Pichucalco",
  "Puebla",
  "San Luis Potosí",
  "Sinaloa",
  "Tamaulipas",
  "Tantoyuca",
  "Tapachula",
  "Teapa",
  "Tlaxcala / Estado de México",
  "Tzucacab / Opb",
  "Xpujil"
])

const confirmarTerritorio = async () => {
  if (!selectedTerritorio.value || saving.value) return
  
  saving.value = true
  
  try {
    const response = await axios.patch(`${API_URL}/usuarios/${props.userId}/territorio`, {
      territorio: selectedTerritorio.value
    })
    
    if (response.data.success) {
      // Actualizar localStorage con el nuevo territorio
      const userData = JSON.parse(localStorage.getItem('user') || '{}')
      userData.territorio = selectedTerritorio.value
      localStorage.setItem('user', JSON.stringify(userData))
      
      console.log('✅ Territorio guardado:', selectedTerritorio.value)
      emit('territorio-saved', selectedTerritorio.value)
    }
  } catch (error) {
    console.error('❌ Error al guardar territorio:', error)
    alert('Error al guardar el territorio. Por favor intenta de nuevo.')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
/* Overlay - bloquea toda la pantalla */
.territorio-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999999;
  padding: 16px;
}

/* Modal container */
.territorio-modal {
  background: linear-gradient(145deg, #ffffff 0%, #f0fdf4 100%);
  border-radius: 24px;
  padding: 32px 24px;
  max-width: 400px;
  width: 100%;
  text-align: center;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.4),
    0 0 0 1px rgba(34, 197, 94, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  position: relative;
  overflow: hidden;
}

/* Decoración verde superior */
.territorio-modal::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #22c55e, #16a34a, #15803d);
}

/* Container del icono */
.modal-icon-container {
  position: relative;
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  box-shadow: 0 8px 24px rgba(34, 197, 94, 0.4);
}

.modal-icon {
  width: 40px;
  height: 40px;
  color: white;
  z-index: 2;
}

.icon-pulse {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: rgba(34, 197, 94, 0.3);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.15);
    opacity: 0.2;
  }
}

/* Título */
.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #166534;
  margin-bottom: 12px;
  line-height: 1.2;
}

/* Mensaje */
.modal-message {
  font-size: 0.95rem;
  color: #4b5563;
  line-height: 1.5;
  margin-bottom: 10px;
}

/* Advertencia amarilla */
.modal-advertencia {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 0.8rem;
  color: #b45309;
  background-color: #fef3c7;
  border: 1px solid #fcd34d;
  border-radius: 6px;
  padding: 8px 12px;
  margin-bottom: 16px;
  text-align: center;
  line-height: 1.3;
}

.modal-advertencia svg {
  flex-shrink: 0;
  color: #d97706;
}

/* Container del select */
.select-container {
  margin-bottom: 20px;
  text-align: left;
}

/* Label removido para simplificar */
.select-label {
  display: none;
}

/* Select estilizado */
.territorio-select {
  width: 100%;
  padding: 14px 16px;
  font-size: 1rem;
  border: 2px solid #d1d5db;
  border-radius: 12px;
  background-color: white;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.3s ease;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%236b7280' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 20px;
}

.territorio-select:focus {
  outline: none;
  border-color: #22c55e;
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.2);
}

.territorio-select.has-value {
  color: #111827;
  border-color: #22c55e;
}

.territorio-select option {
  padding: 12px;
}

/* Botón de confirmar */
.confirm-button {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 24px;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 14px rgba(34, 197, 94, 0.4);
}

.confirm-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(34, 197, 94, 0.5);
}

.confirm-button:active:not(:disabled) {
  transform: translateY(0);
}

.confirm-button:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  box-shadow: none;
}

/* Aviso obligatorio en rojo */
.aviso-obligatorio {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 16px;
  padding: 10px 14px;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 500;
  color: #dc2626;
  text-align: center;
  line-height: 1.4;
}

.aviso-obligatorio svg {
  flex-shrink: 0;
  color: #dc2626;
}

/* Animación de giro para el loading */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Transiciones del modal */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-scale-enter-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-scale-leave-active {
  transition: all 0.2s ease-in;
}

.modal-scale-enter-from {
  opacity: 0;
  transform: scale(0.8) translateY(20px);
}

.modal-scale-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

/* Responsive - optimizado para que siempre se vea todo */
@media (max-width: 480px) {
  .territorio-modal-overlay {
    padding: 16px;
    align-items: center;
  }
  
  .territorio-modal {
    padding: 24px 20px;
    border-radius: 20px;
    max-width: 100%;
    max-height: 90vh;
    overflow-y: auto;
  }
  
  .modal-icon-container {
    width: 60px;
    height: 60px;
    margin-bottom: 12px;
  }
  
  .modal-icon {
    width: 30px;
    height: 30px;
  }
  
  .modal-title {
    font-size: 1.3rem;
    margin-bottom: 8px;
  }
  
  .modal-message {
    font-size: 0.9rem;
    margin-bottom: 8px;
  }
  
  .modal-advertencia {
    font-size: 0.75rem;
    padding: 6px 10px;
    margin-bottom: 12px;
  }
  
  .territorio-select {
    padding: 14px 16px;
    font-size: 1rem;
    border-radius: 12px;
  }
  
  .confirm-button {
    padding: 14px 20px;
    font-size: 1rem;
    border-radius: 12px;
  }
  
  .aviso-obligatorio {
    font-size: 0.8rem;
    padding: 8px 12px;
    margin-top: 12px;
  }
}

/* Pantallas muy pequeñas */
@media (max-width: 360px) {
  .territorio-modal {
    padding: 20px 16px;
  }
  
  .modal-icon-container {
    width: 50px;
    height: 50px;
    margin-bottom: 10px;
  }
  
  .modal-icon {
    width: 26px;
    height: 26px;
  }
  
  .modal-title {
    font-size: 1.2rem;
  }
  
  .modal-message {
    font-size: 0.85rem;
    margin-bottom: 6px;
  }
  
  .modal-advertencia {
    font-size: 0.7rem;
    padding: 5px 8px;
    margin-bottom: 10px;
  }
  
  .territorio-select {
    padding: 12px 14px;
    font-size: 1rem;
  }
  
  .confirm-button {
    padding: 12px 18px;
    font-size: 0.95rem;
  }
  
  .aviso-obligatorio {
    font-size: 0.75rem;
    padding: 6px 10px;
    margin-top: 10px;
  }
}

/* Landscape móvil - altura limitada */
@media (max-height: 500px) and (orientation: landscape) {
  .territorio-modal-overlay {
    padding: 10px;
    align-items: center;
  }
  
  .territorio-modal {
    padding: 16px 24px;
    max-width: 450px;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 12px;
  }
  
  .modal-icon-container {
    width: 50px;
    height: 50px;
    margin-bottom: 0;
  }
  
  .modal-icon {
    width: 26px;
    height: 26px;
  }
  
  .icon-pulse {
    display: none;
  }
  
  .modal-title {
    flex: 1;
    font-size: 1.1rem;
    margin-bottom: 0;
    text-align: left;
  }
  
  .modal-message {
    width: 100%;
    font-size: 0.85rem;
    margin-bottom: 4px;
    text-align: center;
  }
  
  .modal-advertencia {
    width: 100%;
    font-size: 0.7rem;
    padding: 4px 8px;
    margin-bottom: 8px;
  }
  
  .select-container {
    flex: 1;
    margin-bottom: 0;
    min-width: 200px;
  }
  
  .territorio-select {
    padding: 10px 12px;
    font-size: 0.95rem;
    border-radius: 10px;
  }
  
  .confirm-button {
    padding: 10px 20px;
    font-size: 0.9rem;
    border-radius: 10px;
    white-space: nowrap;
  }
  
  .aviso-obligatorio {
    width: 100%;
    font-size: 0.75rem;
    padding: 6px 10px;
    margin-top: 8px;
  }
}

/* Landscape muy pequeño (altura < 400px) */
@media (max-height: 400px) and (orientation: landscape) {
  .territorio-modal {
    padding: 12px 20px;
    gap: 8px;
    max-width: 480px;
  }
  
  .modal-icon-container {
    width: 40px;
    height: 40px;
  }
  
  .modal-icon {
    width: 22px;
    height: 22px;
  }
  
  .modal-title {
    font-size: 1rem;
  }
  
  .modal-message {
    font-size: 0.8rem;
    margin-bottom: 4px;
  }
  
  .modal-advertencia {
    width: 100%;
    font-size: 0.65rem;
    padding: 4px 6px;
    margin-bottom: 6px;
  }
  
  .select-container {
    min-width: 180px;
  }
  
  .territorio-select {
    padding: 8px 10px;
    font-size: 0.9rem;
  }
  
  .confirm-button {
    padding: 8px 16px;
    font-size: 0.85rem;
  }
  
  .aviso-obligatorio {
    width: 100%;
    font-size: 0.7rem;
    padding: 5px 8px;
    margin-top: 6px;
  }
}

/* Tablets en portrait */
@media (min-width: 481px) and (max-width: 768px) {
  .territorio-modal {
    max-width: 380px;
    padding: 28px 24px;
  }
}

/* Tablets en landscape */
@media (min-width: 769px) and (orientation: landscape) {
  .territorio-modal {
    max-width: 420px;
    padding: 36px 32px;
  }
}
</style>
