<template>
  <div class="maintenance-screen">
    <div class="maintenance-container">
      <!-- Icono animado de mantenimiento -->
      <div class="maintenance-icon">
        <div class="gear gear-1">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3"/>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
          </svg>
        </div>
        <div class="gear gear-2">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3"/>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
          </svg>
        </div>
      </div>
      
      <!-- Título principal -->
      <h1 class="maintenance-title">
        🔧 Sistema en Mantenimiento
      </h1>
      
      <!-- Mensaje personalizable -->
      <div class="maintenance-message">
        <p>{{ message || 'Estamos realizando algunas mejoras para ofrecerte un mejor servicio.' }}</p>
      </div>
      
      <!-- Información adicional -->
      <div class="maintenance-info">
        <div class="info-item">
          <div class="info-icon">🕐</div>
          <p>Estimamos regresar pronto</p>
        </div>
        <div class="info-item">
          <div class="info-icon">🔄</div>
          <p>Esta página se actualizará automáticamente</p>
        </div>
        <div class="info-item">
          <div class="info-icon">📧</div>
          <p>Para urgencias, contáctanos directamente</p>
        </div>
      </div>
      
      <!-- Botón de recarga manual -->
      <div class="maintenance-actions">
        <button @click="reloadPage" class="reload-button" :disabled="isReloading">
          <svg v-if="!isReloading" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="23 4 23 10 17 10"/>
            <polyline points="1 20 1 14 7 14"/>
            <path d="m3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
          </svg>
          <div v-else class="loading-spinner"></div>
          {{ isReloading ? 'Verificando...' : 'Verificar Estado' }}
        </button>
      </div>
      
      <!-- Footer con timestamp -->
      <div class="maintenance-footer">
        <p>Última verificación: {{ lastCheck }}</p>
        <p class="app-name">{{ appName || 'Sembrando Vida' }}</p>
      </div>
    </div>
    
    <!-- Partículas decorativas de fondo -->
    <div class="background-particles">
      <div class="particle" v-for="n in 20" :key="n" :style="getParticleStyle(n)"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// Props
const props = defineProps({
  message: {
    type: String,
    default: 'Sistema en mantenimiento programado. Volveremos pronto.'
  },
  appName: {
    type: String,
    default: 'Sembrando Vida'
  }
})

// Emits
const emit = defineEmits(['reload'])

// Estado reactivo
const isReloading = ref(false)
const lastCheck = ref(new Date().toLocaleTimeString('es-ES'))

// Actualizar timestamp cada minuto
let timestampInterval = null

onMounted(() => {
  // Actualizar timestamp cada minuto
  timestampInterval = setInterval(() => {
    lastCheck.value = new Date().toLocaleTimeString('es-ES')
  }, 60000)
})

onUnmounted(() => {
  if (timestampInterval) {
    clearInterval(timestampInterval)
  }
})

// Función para recargar la página
const reloadPage = async () => {
  isReloading.value = true
  lastCheck.value = new Date().toLocaleTimeString('es-ES')
  
  // Emitir evento para que el componente padre maneje la verificación
  emit('reload')
  
  // Simular verificación
  setTimeout(() => {
    isReloading.value = false
  }, 2000)
}

// Generar estilos aleatorios para las partículas
const getParticleStyle = (index) => {
  const size = Math.random() * 10 + 5
  const left = Math.random() * 100
  const duration = Math.random() * 20 + 10
  const delay = Math.random() * 5
  
  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${left}%`,
    animationDuration: `${duration}s`,
    animationDelay: `${delay}s`
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

.maintenance-screen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #27ae60 0%, #2ecc71 50%, #27ae60 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Inter', sans-serif;
  z-index: 10000;
  overflow: hidden;
  color: white;
}

.maintenance-container {
  text-align: center;
  max-width: 500px;
  padding: 40px 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  position: relative;
  z-index: 2;
}

/* Icono de mantenimiento animado */
.maintenance-icon {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 30px;
}

.gear {
  position: absolute;
  color: rgba(255, 255, 255, 0.9);
}

.gear-1 {
  width: 80px;
  height: 80px;
  top: 0;
  left: 20px;
  animation: rotate-clockwise 8s linear infinite;
}

.gear-2 {
  width: 60px;
  height: 60px;
  top: 30px;
  left: 0;
  animation: rotate-counter-clockwise 6s linear infinite;
}

@keyframes rotate-clockwise {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes rotate-counter-clockwise {
  from { transform: rotate(0deg); }
  to { transform: rotate(-360deg); }
}

/* Título */
.maintenance-title {
  font-size: 32px;
  font-weight: 800;
  margin: 0 0 20px 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  letter-spacing: -0.5px;
}

/* Mensaje */
.maintenance-message {
  margin-bottom: 40px;
}

.maintenance-message p {
  font-size: 18px;
  line-height: 1.6;
  margin: 0;
  opacity: 0.95;
  font-weight: 400;
}

/* Información adicional */
.maintenance-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 40px;
}

.info-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.info-icon {
  font-size: 20px;
}

.info-item p {
  margin: 0;
  font-size: 14px;
  font-weight: 500;
}

/* Botón de recarga */
.maintenance-actions {
  margin-bottom: 30px;
}

.reload-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50px;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.reload-button:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.reload-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.reload-button svg {
  width: 18px;
  height: 18px;
}

.loading-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Footer */
.maintenance-footer {
  opacity: 0.8;
  font-size: 12px;
}

.maintenance-footer p {
  margin: 4px 0;
}

.app-name {
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
}

/* Partículas de fondo */
.background-particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: 1;
}

.particle {
  position: absolute;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  animation: float-up linear infinite;
}

@keyframes float-up {
  from {
    transform: translateY(100vh) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  to {
    transform: translateY(-100px) rotate(360deg);
    opacity: 0;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .maintenance-container {
    max-width: 90%;
    padding: 30px 20px;
  }
  
  .maintenance-title {
    font-size: 24px;
  }
  
  .maintenance-message p {
    font-size: 16px;
  }
  
  .maintenance-icon {
    width: 100px;
    height: 100px;
  }
  
  .gear-1 {
    width: 70px;
    height: 70px;
    left: 15px;
  }
  
  .gear-2 {
    width: 50px;
    height: 50px;
    top: 25px;
  }
  
  .info-item {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }
  
  .reload-button {
    padding: 12px 24px;
    font-size: 14px;
  }
}
</style>
