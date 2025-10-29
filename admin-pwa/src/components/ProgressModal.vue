<template>
  <Teleport to="body">
    <div v-if="show" class="progress-modal-overlay">
      <div class="progress-modal" @click.stop>
        <!-- Encabezado -->
        <div class="modal-header">
          <div class="modal-icon" :class="iconClass">
            <svg v-if="estado === 'procesando'" class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 2a10 10 0 0 1 0 20"></path>
            </svg>
            <svg v-else-if="estado === 'completado'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"></path>
            </svg>
          </div>
          <h3>{{ titulo }}</h3>
          <p v-if="estado === 'procesando'" class="subtitle">Eliminando imágenes...</p>
          <p v-else-if="estado === 'completado'" class="subtitle">¡Eliminación completada!</p>
        </div>

        <!-- Barra de progreso -->
        <div v-if="estado === 'procesando'" class="progress-section">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: progreso + '%' }"></div>
          </div>
          <div class="progress-text">
            <span class="percentage">{{ progreso }}%</span>
          </div>
        </div>

        <!-- Información detallada -->
        <div class="info-section">
          <div class="info-item" :class="{ completado: estadisticas.fotos_bd_limpiadas > 0 }">
            <div class="info-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 19V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2z"></path>
                <polyline points="17 6 17 16"></polyline>
                <line x1="13" y1="10" x2="7" y2="10"></line>
              </svg>
            </div>
            <div class="info-text">
              <span class="label">Fotos en BD limpiadas</span>
              <span class="value">{{ estadisticas.fotos_bd_limpiadas }}</span>
            </div>
            <div class="info-check" v-if="estadisticas.fotos_bd_limpiadas > 0">✓</div>
          </div>

          <div class="info-item" :class="{ completado: estadisticas.archivos_eliminados > 0 }">
            <div class="info-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                <polyline points="17 21 17 13 7 13 7 21"></polyline>
                <polyline points="7 5 7 13"></polyline>
              </svg>
            </div>
            <div class="info-text">
              <span class="label">Archivos eliminados</span>
              <span class="value">{{ estadisticas.archivos_eliminados }}</span>
            </div>
            <div class="info-check" v-if="estadisticas.archivos_eliminados > 0">✓</div>
          </div>

          <div v-if="estadisticas.archivos_no_encontrados > 0" class="info-item warning">
            <div class="info-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
            </div>
            <div class="info-text">
              <span class="label">Archivos no encontrados</span>
              <span class="value">{{ estadisticas.archivos_no_encontrados }}</span>
            </div>
          </div>

          <div v-if="estadisticas.errores_encontrados > 0" class="info-item error">
            <div class="info-icon">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"></path>
              </svg>
            </div>
            <div class="info-text">
              <span class="label">Errores encontrados</span>
              <span class="value">{{ estadisticas.errores_encontrados }}</span>
            </div>
          </div>
        </div>

        <!-- Resumen final -->
        <div v-if="estado === 'completado'" class="summary-section">
          <div class="summary-box">
            <div class="summary-stat">
              <span class="stat-value">{{ estadisticas.total_eliminado }}</span>
              <span class="stat-label">Total eliminado</span>
            </div>
          </div>
          <p v-if="mensajeResumen" class="summary-text">{{ mensajeResumen }}</p>
        </div>

        <!-- Acciones -->
        <div class="modal-actions">
          <button 
            @click="cerrar" 
            class="btn-aceptar"
            :disabled="estado === 'procesando'"
          >
            {{ estado === 'completado' ? 'Aceptar' : 'Cancelar' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  titulo: {
    type: String,
    default: 'Eliminar imágenes'
  }
})

const emit = defineEmits(['cerrar', 'completado'])

const estado = ref('procesando') // procesando, completado, error
const progreso = ref(0)
const estadisticas = ref({
  fotos_bd_limpiadas: 0,
  archivos_eliminados: 0,
  archivos_no_encontrados: 0,
  total_eliminado: 0,
  errores_encontrados: 0
})

const iconClass = computed(() => {
  const classes = {
    procesando: 'procesando-icon',
    completado: 'completado-icon',
    error: 'error-icon'
  }
  return classes[estado.value]
})

const mensajeResumen = computed(() => {
  const total = estadisticas.value.total_eliminado
  const archivos = estadisticas.value.archivos_eliminados
  const errores = estadisticas.value.errores_encontrados

  if (errores > 0) {
    return `Se eliminaron ${total} elementos, pero hubo ${errores} error(es) durante el proceso.`
  }
  return `Se han eliminado exitosamente ${total} archivos de imágenes del sistema.`
})

// Simular progreso
const iniciarProgreso = async () => {
  estado.value = 'procesando'
  progreso.value = 0

  const incremento = () => {
    progreso.value += Math.random() * 30
    if (progreso.value > 100) {
      progreso.value = 100
    }
  }

  const intervalo = setInterval(incremento, 500)

  return () => {
    clearInterval(intervalo)
    progreso.value = 100
  }
}

const actualizar = (nuevasEstadisticas) => {
  estadisticas.value = {
    ...estadisticas.value,
    ...nuevasEstadisticas
  }
}

const completar = () => {
  estado.value = 'completado'
  progreso.value = 100
  emit('completado')
}

const cerrar = () => {
  estado.value = 'procesando'
  progreso.value = 0
  estadisticas.value = {
    fotos_bd_limpiadas: 0,
    archivos_eliminados: 0,
    archivos_no_encontrados: 0,
    total_eliminado: 0,
    errores_encontrados: 0
  }
  emit('cerrar')
}

// Exponer métodos
defineExpose({
  iniciarProgreso,
  actualizar,
  completar,
  cerrar
})
</script>

<style scoped>
.progress-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10000;
  padding: 20px;
  animation: overlayFadeIn 0.3s ease-out;
}

@keyframes overlayFadeIn {
  from {
    opacity: 0;
    backdrop-filter: blur(0px);
  }
  to {
    opacity: 1;
    backdrop-filter: blur(8px);
  }
}

.progress-modal {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 24px;
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  max-width: 500px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  animation: modalSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.8) translateY(30px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  padding: 32px 28px 24px;
  text-align: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.5) 0%, rgba(248, 249, 250, 0.5) 100%);
}

.modal-icon {
  width: 72px;
  height: 72px;
  margin: 0 auto 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-icon svg {
  width: 40px;
  height: 40px;
  color: white;
}

.procesando-icon {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  animation: iconPulse 2s ease-in-out infinite;
}

.completado-icon {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  animation: iconCheck 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.error-icon {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  animation: iconShake 0.5s ease-in-out;
}

@keyframes iconPulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 12px rgba(59, 130, 246, 0);
  }
}

@keyframes iconCheck {
  0% {
    transform: scale(0.5) rotate(-30deg);
  }
  100% {
    transform: scale(1) rotate(0);
  }
}

@keyframes iconShake {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-4px);
  }
  75% {
    transform: translateX(4px);
  }
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.modal-header h3 {
  margin: 0 0 4px;
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

.subtitle {
  margin: 8px 0 0;
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.progress-section {
  padding: 24px 28px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6 0%, #1d4ed8 100%);
  border-radius: 10px;
  transition: width 0.3s ease;
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
}

.progress-text {
  display: flex;
  justify-content: center;
  align-items: center;
}

.percentage {
  font-size: 14px;
  font-weight: 600;
  color: #3b82f6;
  font-family: 'Inter', sans-serif;
}

.info-section {
  padding: 20px 28px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  margin-bottom: 8px;
  background: rgba(248, 249, 250, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-item.completado {
  background: rgba(16, 185, 129, 0.08);
  border-color: rgba(16, 185, 129, 0.2);
}

.info-item.warning {
  background: rgba(245, 158, 11, 0.08);
  border-color: rgba(245, 158, 11, 0.2);
}

.info-item.error {
  background: rgba(239, 68, 68, 0.08);
  border-color: rgba(239, 68, 68, 0.2);
}

.info-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #3b82f6;
}

.info-item.completado .info-icon {
  color: #10b981;
}

.info-item.warning .info-icon {
  color: #f59e0b;
}

.info-item.error .info-icon {
  color: #ef4444;
}

.info-icon svg {
  width: 20px;
  height: 20px;
  stroke-width: 2;
}

.info-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.label {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
}

.value {
  font-size: 16px;
  font-weight: 700;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

.info-item.completado .value {
  color: #059669;
}

.info-item.warning .value {
  color: #d97706;
}

.info-item.error .value {
  color: #dc2626;
}

.info-check {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border-radius: 50%;
  font-weight: 700;
  font-size: 16px;
  flex-shrink: 0;
  animation: checkPop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes checkPop {
  0% {
    transform: scale(0);
  }
  100% {
    transform: scale(1);
  }
}

.summary-section {
  padding: 24px 28px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  text-align: center;
}

.summary-box {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.summary-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 12px;
}

.stat-value {
  font-size: 32px;
  font-weight: 800;
  color: #059669;
  font-family: 'Inter', sans-serif;
}

.stat-label {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
  margin-top: 4px;
  font-family: 'Inter', sans-serif;
}

.summary-text {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
  font-family: 'Inter', sans-serif;
}

.modal-actions {
  padding: 20px 28px 28px;
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-aceptar {
  flex: 1;
  max-width: 300px;
  padding: 12px 24px;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

.btn-aceptar:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
}

.btn-aceptar:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 480px) {
  .progress-modal {
    border-radius: 20px;
    max-height: 90vh;
  }

  .modal-header {
    padding: 24px 20px 20px;
  }

  .modal-icon {
    width: 60px;
    height: 60px;
  }

  .modal-icon svg {
    width: 32px;
    height: 32px;
  }

  .modal-header h3 {
    font-size: 20px;
  }

  .progress-section,
  .info-section,
  .summary-section,
  .modal-actions {
    padding-left: 20px;
    padding-right: 20px;
  }
}
</style>
