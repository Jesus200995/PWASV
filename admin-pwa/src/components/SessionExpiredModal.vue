<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="isVisible" class="session-modal-overlay" @click.self="handleClose">
        <Transition name="modal-scale">
          <div v-if="isVisible" class="session-modal">
            <!-- Icono animado -->
            <div class="modal-icon-container" :class="iconType">
              <!-- Icono de cuenta desactivada -->
              <svg v-if="iconType === 'deactivated'" class="modal-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <path d="M4.93 4.93l14.14 14.14"/>
                <path d="M12 8v4"/>
                <path d="M12 16h.01"/>
              </svg>
              
              <!-- Icono de cuenta eliminada -->
              <svg v-else-if="iconType === 'deleted'" class="modal-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 6h18"/>
                <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
                <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
                <line x1="10" y1="11" x2="10" y2="17"/>
                <line x1="14" y1="11" x2="14" y2="17"/>
              </svg>
              
              <!-- Icono de refresh (cambio de rol) -->
              <svg v-else-if="iconType === 'refresh'" class="modal-icon spin-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
                <path d="M3 3v5h5"/>
                <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/>
                <path d="M21 21v-5h-5"/>
              </svg>
              
              <!-- Icono de sesión expirada (default) -->
              <svg v-else class="modal-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
              
              <!-- Círculo animado de fondo -->
              <div class="icon-pulse"></div>
            </div>
            
            <!-- Título -->
            <h2 class="modal-title">{{ title }}</h2>
            
            <!-- Mensaje -->
            <p class="modal-message">{{ message }}</p>
            
            <!-- Info adicional -->
            <div class="modal-info">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="16" x2="12" y2="12"/>
                <line x1="12" y1="8" x2="12.01" y2="8"/>
              </svg>
              <span>Serás redirigido a la página de inicio de sesión</span>
            </div>
            
            <!-- Botón -->
            <button class="modal-button" @click="handleClose">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                <polyline points="16 17 21 12 16 7"/>
                <line x1="21" y1="12" x2="9" y2="12"/>
              </svg>
              <span>Ir al inicio de sesión</span>
            </button>
            
            <!-- Contador de redirección automática -->
            <p class="auto-redirect">
              Redirección automática en <span class="countdown">{{ countdown }}</span> segundos
            </p>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Sesión Finalizada'
  },
  message: {
    type: String,
    default: 'Tu sesión ha sido cerrada.'
  },
  iconType: {
    type: String,
    default: 'deactivated' // 'deactivated', 'deleted', 'expired'
  },
  autoRedirect: {
    type: Boolean,
    default: true
  },
  redirectDelay: {
    type: Number,
    default: 5
  }
})

const emit = defineEmits(['close', 'redirect'])

const countdown = ref(props.redirectDelay)
let countdownInterval = null

const handleClose = () => {
  clearInterval(countdownInterval)
  emit('close')
  emit('redirect')
}

watch(() => props.isVisible, (newVal) => {
  if (newVal && props.autoRedirect) {
    countdown.value = props.redirectDelay
    countdownInterval = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        handleClose()
      }
    }, 1000)
  } else {
    clearInterval(countdownInterval)
  }
})

onUnmounted(() => {
  clearInterval(countdownInterval)
})
</script>

<style scoped>
/* Overlay con fondo difuminado oscuro */
.session-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
  padding: 20px;
}

/* Modal container */
.session-modal {
  background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
  border-radius: 24px;
  padding: 40px 32px;
  max-width: 420px;
  width: 100%;
  text-align: center;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}

/* Decoración de fondo del modal */
.session-modal::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #f44336, #ff5722, #ff9800);
}

/* Contenedor del icono */
.modal-icon-container {
  width: 100px;
  height: 100px;
  margin: 0 auto 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.modal-icon-container.deactivated {
  background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
}

.modal-icon-container.deleted {
  background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
}

.modal-icon-container.expired {
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
}

/* Icono SVG */
.modal-icon {
  width: 48px;
  height: 48px;
  z-index: 1;
  animation: iconBounce 0.6s ease-out;
}

.modal-icon-container.deactivated .modal-icon {
  color: #d32f2f;
}

.modal-icon-container.deleted .modal-icon {
  color: #c2185b;
}

.modal-icon-container.expired .modal-icon {
  color: #f57c00;
}

/* Pulso animado detrás del icono */
.icon-pulse {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

.modal-icon-container.deactivated .icon-pulse {
  background: rgba(244, 67, 54, 0.2);
}

.modal-icon-container.deleted .icon-pulse {
  background: rgba(194, 24, 91, 0.2);
}

.modal-icon-container.expired .icon-pulse {
  background: rgba(245, 124, 0, 0.2);
}

.modal-icon-container.refresh {
  background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
  box-shadow: 0 4px 20px rgba(33, 150, 243, 0.4);
}

.modal-icon-container.refresh .modal-icon {
  color: white;
}

.modal-icon-container.refresh .icon-pulse {
  background: rgba(33, 150, 243, 0.2);
}

/* Animación de giro para el icono de refresh */
.spin-icon {
  animation: spin 1.5s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.3;
  }
}

@keyframes iconBounce {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Título */
.modal-title {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 12px;
  letter-spacing: -0.5px;
}

/* Mensaje */
.modal-message {
  font-size: 15px;
  color: #5a5a6e;
  line-height: 1.6;
  margin-bottom: 20px;
  padding: 0 10px;
}

/* Info adicional */
.modal-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  border-radius: 12px;
  margin-bottom: 24px;
  font-size: 13px;
  color: #1565c0;
}

.modal-info svg {
  flex-shrink: 0;
}

/* Botón principal */
.modal-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
  padding: 16px 24px;
  font-size: 15px;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #4CAF50 0%, #2e7d32 100%);
  border: none;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}

.modal-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4);
}

.modal-button:active {
  transform: translateY(0);
}

/* Contador de redirección */
.auto-redirect {
  margin-top: 16px;
  font-size: 13px;
  color: #9e9e9e;
}

.countdown {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
  color: white;
  border-radius: 50%;
  font-weight: 700;
  font-size: 12px;
  margin: 0 4px;
  animation: countdownPulse 1s ease-in-out infinite;
}

@keyframes countdownPulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

/* Transiciones */
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

/* Responsivo */
@media (max-width: 480px) {
  .session-modal {
    padding: 32px 24px;
    border-radius: 20px;
    margin: 16px;
  }
  
  .modal-icon-container {
    width: 80px;
    height: 80px;
  }
  
  .modal-icon {
    width: 40px;
    height: 40px;
  }
  
  .modal-title {
    font-size: 20px;
  }
  
  .modal-message {
    font-size: 14px;
  }
  
  .modal-button {
    padding: 14px 20px;
    font-size: 14px;
  }
}

@media (max-width: 360px) {
  .session-modal {
    padding: 24px 16px;
  }
  
  .modal-icon-container {
    width: 70px;
    height: 70px;
    margin-bottom: 16px;
  }
  
  .modal-icon {
    width: 36px;
    height: 36px;
  }
  
  .modal-title {
    font-size: 18px;
  }
}
</style>
