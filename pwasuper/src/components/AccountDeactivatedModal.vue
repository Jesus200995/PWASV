<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="show" class="deactivated-overlay" @click.prevent>
        <Transition name="pop">
          <div v-if="show" class="deactivated-modal">
            <!-- Icono animado -->
            <div class="deactivated-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
              </svg>
            </div>

            <!-- Título -->
            <h2 class="deactivated-title">Cuenta Desactivada</h2>

            <!-- Mensaje -->
            <div class="deactivated-content">
              <p class="deactivated-message">
                Tu cuenta ha sido desactivada por un administrador.
              </p>
              <p class="deactivated-submessage">
                Por favor, contacta al administrador del sistema para más información.
              </p>
            </div>

            <!-- Contador -->
            <div class="deactivated-countdown">
              <span>Cerrando sesión en </span>
              <span class="countdown-number">{{ countdown }}</span>
              <span> segundos...</span>
            </div>

            <!-- Botón -->
            <button @click="cerrarSesionAhora" class="deactivated-btn">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                <polyline points="16 17 21 12 16 7"/>
                <line x1="21" y1="12" x2="9" y2="12"/>
              </svg>
              Cerrar sesión ahora
            </button>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch, onUnmounted } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['logout'])

const countdown = ref(5)
let countdownInterval = null

const cerrarSesionAhora = () => {
  if (countdownInterval) {
    clearInterval(countdownInterval)
    countdownInterval = null
  }
  emit('logout')
}

const iniciarContador = () => {
  countdown.value = 5
  if (countdownInterval) {
    clearInterval(countdownInterval)
  }
  countdownInterval = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(countdownInterval)
      countdownInterval = null
      emit('logout')
    }
  }, 1000)
}

watch(() => props.show, (newVal) => {
  if (newVal) {
    iniciarContador()
  } else {
    if (countdownInterval) {
      clearInterval(countdownInterval)
      countdownInterval = null
    }
  }
})

onUnmounted(() => {
  if (countdownInterval) {
    clearInterval(countdownInterval)
  }
})
</script>

<style scoped>
.deactivated-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
  padding: 20px;
}

.deactivated-modal {
  background: linear-gradient(145deg, #ffffff, #f8f9fa);
  border-radius: 24px;
  padding: 40px 32px;
  max-width: 400px;
  width: 100%;
  text-align: center;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  animation: modalShake 0.5s ease-out;
}

@keyframes modalShake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
  20%, 40%, 60%, 80% { transform: translateX(5px); }
}

.deactivated-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  animation: pulseIcon 1.5s ease-in-out infinite;
}

@keyframes pulseIcon {
  0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
  50% { transform: scale(1.05); box-shadow: 0 0 20px 10px rgba(239, 68, 68, 0); }
}

.deactivated-title {
  font-size: 24px;
  font-weight: 700;
  color: #dc2626;
  margin: 0 0 16px 0;
}

.deactivated-content {
  margin-bottom: 24px;
}

.deactivated-message {
  font-size: 16px;
  color: #374151;
  margin: 0 0 8px 0;
  font-weight: 500;
}

.deactivated-submessage {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.deactivated-countdown {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  padding: 12px 20px;
  margin-bottom: 24px;
  font-size: 14px;
  color: #991b1b;
}

.countdown-number {
  font-weight: 700;
  font-size: 18px;
  color: #dc2626;
}

.deactivated-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 14px 28px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 14px rgba(220, 38, 38, 0.4);
}

.deactivated-btn:hover {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(220, 38, 38, 0.5);
}

.deactivated-btn:active {
  transform: translateY(0);
}

/* Transiciones */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.pop-enter-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.pop-leave-active {
  transition: all 0.25s ease-in;
}
.pop-enter-from {
  opacity: 0;
  transform: scale(0.8);
}
.pop-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

/* Responsive */
@media (max-width: 480px) {
  .deactivated-modal {
    padding: 32px 24px;
    margin: 16px;
  }
  
  .deactivated-icon {
    width: 64px;
    height: 64px;
  }
  
  .deactivated-icon svg {
    width: 36px;
    height: 36px;
  }
  
  .deactivated-title {
    font-size: 20px;
  }
  
  .deactivated-message {
    font-size: 14px;
  }
  
  .deactivated-btn {
    width: 100%;
    padding: 12px 24px;
  }
}
</style>
