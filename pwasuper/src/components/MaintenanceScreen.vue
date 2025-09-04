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
        Sistema en Mantenimiento
      </h1>
      
      <!-- Mensaje personalizable -->
      <div class="maintenance-message">
        <p>{{ message || 'Estamos realizando algunas mejoras para ofrecerte un mejor servicio.' }}</p>
      </div>
      
      <!-- Información adicional en un solo recuadro -->
      <div class="maintenance-info-single">
        <div class="info-content">
          <div class="info-item">
            <div class="info-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12,6 12,12 16,14"/>
              </svg>
            </div>
            <p>Estimamos regresar pronto</p>
          </div>
          <div class="info-item">
            <div class="info-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="23 4 23 10 17 10"/>
                <polyline points="1 20 1 14 7 14"/>
                <path d="m3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
              </svg>
            </div>
            <p>Esta página se verifica automáticamente cada 30 segundos</p>
          </div>
          <div class="info-item">
            <div class="info-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
            </div>
            <p>Para urgencias, contáctanos directamente</p>
          </div>
        </div>
      </div>
      
      <!-- Botón de verificación manual centrado -->
      <div class="maintenance-actions">
        <button @click="reloadPage" class="reload-button" :disabled="isReloading">
          <svg v-if="!isReloading" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="23 4 23 10 17 10"/>
            <polyline points="1 20 1 14 7 14"/>
            <path d="m3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
          </svg>
          <div v-else class="loading-spinner"></div>
          {{ isReloading ? 'Verificando...' : 'Verificar disponibilidad' }}
        </button>
        
        <!-- Mensaje temporal después de verificar -->
        <transition name="fade">
          <div v-if="showVerificationMessage && !isReloading" class="verification-message">
            <div class="verification-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20,6 9,17 4,12"/>
              </svg>
            </div>
            <p>Verificación completada. Si el mantenimiento ha terminado, esta pantalla se ocultará automáticamente.</p>
          </div>
        </transition>
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
const showVerificationMessage = ref(false)

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

// Función para verificar estado (NO recargar la página)
const reloadPage = async () => {
  isReloading.value = true
  lastCheck.value = new Date().toLocaleTimeString('es-ES')
  showVerificationMessage.value = true
  
  // Emitir evento para que el componente padre maneje la verificación
  // IMPORTANTE: Solo verificar, NO cerrar la pantalla automáticamente
  emit('reload')
  
  // Tiempo de verificación más realista
  setTimeout(() => {
    isReloading.value = false
    // Ocultar el mensaje después de unos segundos
    setTimeout(() => {
      showVerificationMessage.value = false
    }, 3000)
  }, 1500)
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
  background: linear-gradient(135deg, #ffffff 0%, #f8fffe 30%, #f0fdf4 70%, #ffffff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Inter', sans-serif;
  z-index: 10000;
  overflow: hidden;
  color: #374151;
}

.maintenance-container {
  text-align: center;
  max-width: 450px;
  padding: 30px 20px;
  background: rgba(240, 253, 244, 0.7);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(34, 197, 94, 0.2);
  box-shadow: 
    0 20px 40px rgba(34, 197, 94, 0.1),
    0 8px 32px rgba(0, 0, 0, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  position: relative;
  z-index: 2;
}

/* Icono de mantenimiento animado */
.maintenance-icon {
  position: relative;
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
}

.gear {
  position: absolute;
  color: rgba(34, 197, 94, 0.8);
}

.gear-1 {
  width: 56px;
  height: 56px;
  top: 0;
  left: 12px;
  animation: rotate-clockwise 8s linear infinite;
}

.gear-2 {
  width: 42px;
  height: 42px;
  top: 20px;
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
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 16px 0;
  color: #27ae60;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  letter-spacing: -0.3px;
}

/* Mensaje */
.maintenance-message {
  margin-bottom: 28px;
}

.maintenance-message p {
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
  opacity: 0.95;
  font-weight: 400;
}

/* Información adicional en un solo recuadro */
.maintenance-info-single {
  margin-bottom: 28px;
}

.info-content {
  background: rgba(240, 253, 244, 0.8);
  backdrop-filter: blur(15px);
  border-radius: 12px;
  border: 1px solid rgba(34, 197, 94, 0.25);
  padding: 16px;
  box-shadow: 
    0 4px 15px rgba(34, 197, 94, 0.08),
    0 2px 8px rgba(0, 0, 0, 0.03),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
}

.info-item:not(:last-child) {
  border-bottom: 1px solid rgba(34, 197, 94, 0.15);
  margin-bottom: 8px;
  padding-bottom: 12px;
}

.info-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  color: rgba(34, 197, 94, 0.8);
  flex-shrink: 0;
}

.info-icon svg {
  width: 18px;
  height: 18px;
}

.info-item p {
  margin: 0;
  font-size: 12px;
  font-weight: 500;
  color: rgba(55, 65, 81, 0.9);
  text-align: left;
  line-height: 1.4;
}

/* Botón de recarga centrado */
.maintenance-actions {
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.reload-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 28px;
  background: rgba(34, 197, 94, 0.9);
  border: 2px solid rgba(34, 197, 94, 1);
  border-radius: 50px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  box-shadow: 
    0 4px 15px rgba(34, 197, 94, 0.3),
    0 2px 8px rgba(0, 0, 0, 0.1);
  min-width: 200px;
}

.reload-button:hover:not(:disabled) {
  background: rgba(34, 197, 94, 1);
  border-color: rgba(34, 197, 94, 1);
  transform: translateY(-2px);
  box-shadow: 
    0 6px 20px rgba(34, 197, 94, 0.4),
    0 4px 12px rgba(0, 0, 0, 0.15);
}

.reload-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.reload-button svg {
  width: 16px;
  height: 16px;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Mensaje de verificación */
.verification-message {
  display: flex;
  align-items: center;
  gap: 8px;
  max-width: 380px;
  padding: 10px 14px;
  background: rgba(220, 252, 231, 0.8);
  border: 1px solid rgba(34, 197, 94, 0.3);
  border-radius: 10px;
  backdrop-filter: blur(10px);
  margin-top: 8px;
  box-shadow: 
    0 2px 8px rgba(34, 197, 94, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.verification-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  color: #22c55e;
}

.verification-icon svg {
  width: 16px;
  height: 16px;
}

.verification-message p {
  margin: 0;
  font-size: 12px;
  color: rgba(55, 65, 81, 0.9);
  text-align: left;
  line-height: 1.4;
}

/* Transición para el mensaje */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Footer */
.maintenance-footer {
  opacity: 0.7;
  font-size: 11px;
  color: rgba(55, 65, 81, 0.8);
}

.maintenance-footer p {
  margin: 3px 0;
}

.app-name {
  font-weight: 700;
  color: rgba(34, 197, 94, 0.9);
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
  background: rgba(34, 197, 94, 0.08);
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

/* Responsive - Móviles */
@media (max-width: 768px) {
  .maintenance-container {
    max-width: 95%;
    padding: 18px 14px;
    margin: 10px;
    border-radius: 14px;
  }
  
  .maintenance-title {
    font-size: 18px;
    line-height: 1.3;
    margin-bottom: 14px;
  }
  
  .maintenance-message p {
    font-size: 13px;
    line-height: 1.4;
    padding: 0 6px;
  }
  
  .maintenance-icon {
    width: 64px;
    height: 64px;
    margin-bottom: 16px;
  }
  
  .gear-1 {
    width: 44px;
    height: 44px;
    left: 10px;
  }
  
  .gear-2 {
    width: 32px;
    height: 32px;
    top: 16px;
    left: 0;
  }
  
  .maintenance-info-single {
    margin-bottom: 20px;
  }
  
  .info-content {
    padding: 12px;
  }
  
  .info-item {
    gap: 10px;
    padding: 6px 0;
  }
  
  .info-item:not(:last-child) {
    margin-bottom: 6px;
    padding-bottom: 10px;
  }
  
  .info-item p {
    font-size: 11px;
  }
  
  .info-icon {
    width: 16px;
    height: 16px;
  }
  
  .info-icon svg {
    width: 16px;
    height: 16px;
  }
  
  .reload-button {
    padding: 12px 24px;
    font-size: 13px;
    min-width: 180px;
  }
  
  .reload-button svg,
  .loading-spinner {
    width: 16px;
    height: 16px;
  }
  
  .verification-message {
    max-width: 90%;
    padding: 8px 10px;
    margin-top: 10px;
  }
  
  .verification-icon {
    width: 14px;
    height: 14px;
  }
  
  .verification-icon svg {
    width: 14px;
    height: 14px;
  }
  
  .verification-message p {
    font-size: 11px;
  }
  
  .maintenance-footer {
    font-size: 10px;
    margin-top: 14px;
  }
}

/* Responsive - Móviles pequeños */
@media (max-width: 480px) {
  .maintenance-container {
    max-width: 98%;
    padding: 14px 10px;
    margin: 5px;
  }
  
  .maintenance-title {
    font-size: 16px;
    margin-bottom: 12px;
  }
  
  .maintenance-message p {
    font-size: 12px;
    padding: 0 4px;
  }
  
  .maintenance-icon {
    width: 56px;
    height: 56px;
    margin-bottom: 14px;
  }
  
  .gear-1 {
    width: 38px;
    height: 38px;
    left: 9px;
  }
  
  .gear-2 {
    width: 28px;
    height: 28px;
    top: 14px;
  }
  
  .info-content {
    padding: 10px;
  }
  
  .info-item {
    gap: 8px;
    padding: 5px 0;
  }
  
  .info-item:not(:last-child) {
    margin-bottom: 5px;
    padding-bottom: 8px;
  }
  
  .info-item p {
    font-size: 10px;
  }
  
  .info-icon {
    width: 14px;
    height: 14px;
  }
  
  .info-icon svg {
    width: 14px;
    height: 14px;
  }
  
  .reload-button {
    padding: 10px 20px;
    font-size: 12px;
    min-width: 160px;
  }
  
  .reload-button svg,
  .loading-spinner {
    width: 14px;
    height: 14px;
  }
  
  .verification-message {
    max-width: 95%;
    padding: 6px 8px;
  }
  
  .verification-icon {
    width: 12px;
    height: 12px;
  }
  
  .verification-icon svg {
    width: 12px;
    height: 12px;
  }
  
  .verification-message p {
    font-size: 10px;
  }
}

/* Responsive - Pantallas muy pequeñas */
@media (max-width: 360px) {
  .maintenance-container {
    padding: 12px 8px;
  }
  
  .maintenance-title {
    font-size: 14px;
    margin-bottom: 10px;
  }
  
  .maintenance-message p {
    font-size: 11px;
  }
  
  .maintenance-icon {
    width: 48px;
    height: 48px;
    margin-bottom: 12px;
  }
  
  .gear-1 {
    width: 32px;
    height: 32px;
    left: 8px;
  }
  
  .gear-2 {
    width: 24px;
    height: 24px;
    top: 12px;
  }
  
  .info-content {
    padding: 8px;
  }
  
  .info-item {
    gap: 6px;
    padding: 4px 0;
  }
  
  .info-item:not(:last-child) {
    margin-bottom: 4px;
    padding-bottom: 6px;
  }
  
  .info-item p {
    font-size: 9px;
  }
  
  .reload-button {
    padding: 8px 16px;
    font-size: 11px;
    min-width: 140px;
  }
  
  .verification-message {
    max-width: 98%;
    padding: 5px 6px;
  }
  
  .verification-message p {
    font-size: 9px;
  }
  
  .maintenance-footer {
    font-size: 9px;
  }
}
</style>
