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
          <p v-if="estado === 'procesando'" class="subtitle">
            <span class="periodo-text">{{ periodoTexto }}</span>
          </p>
          <p v-else-if="estado === 'completado'" class="subtitle">¡Eliminación completada!</p>
        </div>

        <!-- Barra de progreso -->
        <div v-if="estado === 'procesando'" class="progress-section">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: progreso + '%' }"></div>
          </div>
          <div class="progress-text">
            <span class="percentage">{{ progreso }}%</span>
            <span class="progress-message">{{ mensajeActual }}</span>
          </div>
        </div>

        <!-- Información detallada -->
        <div class="info-section">
          <div class="info-item" :class="{ completado: estadisticas.registros_limpiados > 0 }">
            <div class="info-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
              </svg>
            </div>
            <div class="info-text">
              <span class="label">Registros limpiados</span>
              <span class="value">{{ estadisticas.registros_limpiados }}</span>
            </div>
            <div class="info-check" v-if="estadisticas.registros_limpiados > 0">✓</div>
          </div>

          <div class="info-item" :class="{ completado: estadisticas.asistencias_limpiadas > 0 }">
            <div class="info-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <polyline points="16 11 18 13 22 9"></polyline>
              </svg>
            </div>
            <div class="info-text">
              <span class="label">Asistencias limpiadas</span>
              <span class="value">{{ estadisticas.asistencias_limpiadas }}</span>
            </div>
            <div class="info-check" v-if="estadisticas.asistencias_limpiadas > 0">✓</div>
          </div>

          <div class="info-item" :class="{ completado: estadisticas.archivos_eliminados > 0 }">
            <div class="info-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
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

          <div v-if="estadisticas.errores > 0" class="info-item error">
            <div class="info-icon">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"></path>
              </svg>
            </div>
            <div class="info-text">
              <span class="label">Errores encontrados</span>
              <span class="value">{{ estadisticas.errores }}</span>
            </div>
          </div>
        </div>

        <!-- Resumen final -->
        <div v-if="estado === 'completado'" class="summary-section">
          <div class="summary-box">
            <div class="summary-stat">
              <span class="stat-value">{{ estadisticas.total_procesado }}</span>
              <span class="stat-label">Total procesado</span>
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
    default: 'Eliminar imágenes por fecha'
  },
  periodo: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['cerrar', 'completado'])

const estado = ref('procesando') // procesando, completado, error
const progreso = ref(0)
const mensajeActual = ref('Conectando con el servidor...')
const estadisticas = ref({
  registros_limpiados: 0,
  asistencias_limpiadas: 0,
  archivos_eliminados: 0,
  archivos_no_encontrados: 0,
  total_procesado: 0,
  errores: 0
})

const periodoTexto = computed(() => {
  return props.periodo ? `Eliminando imágenes de: ${props.periodo}` : 'Procesando...'
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
  const total = estadisticas.value.total_procesado
  const errores = estadisticas.value.errores

  if (errores > 0) {
    return `Se procesaron ${total} elementos, pero hubo ${errores} error(es) durante el proceso.`
  }
  return `Se han eliminado exitosamente las imágenes del período seleccionado.`
})

// Simular progreso con mensajes
const mensajesProgreso = [
  'Conectando con el servidor...',
  'Buscando imágenes del período...',
  'Procesando registros de actividades...',
  'Procesando asistencias...',
  'Eliminando archivos...',
  'Limpiando referencias en BD...',
  'Finalizando...'
]

let intervaloProgreso = null

const iniciarProgreso = async () => {
  estado.value = 'procesando'
  progreso.value = 0
  let mensajeIndex = 0

  const incremento = () => {
    progreso.value += Math.random() * 15
    if (progreso.value > 95) {
      progreso.value = 95
    }
    
    // Cambiar mensaje cada cierto progreso
    const nuevoIndex = Math.min(Math.floor(progreso.value / 15), mensajesProgreso.length - 1)
    if (nuevoIndex !== mensajeIndex) {
      mensajeIndex = nuevoIndex
      mensajeActual.value = mensajesProgreso[mensajeIndex]
    }
  }

  intervaloProgreso = setInterval(incremento, 400)

  return () => {
    if (intervaloProgreso) {
      clearInterval(intervaloProgreso)
      intervaloProgreso = null
    }
    progreso.value = 100
    mensajeActual.value = '¡Completado!'
  }
}

const actualizar = (nuevasEstadisticas) => {
  estadisticas.value = {
    ...estadisticas.value,
    ...nuevasEstadisticas
  }
}

const completar = () => {
  if (intervaloProgreso) {
    clearInterval(intervaloProgreso)
    intervaloProgreso = null
  }
  estado.value = 'completado'
  progreso.value = 100
  mensajeActual.value = '¡Completado!'
  emit('completado')
}

const cerrar = () => {
  if (intervaloProgreso) {
    clearInterval(intervaloProgreso)
    intervaloProgreso = null
  }
  estado.value = 'procesando'
  progreso.value = 0
  mensajeActual.value = 'Conectando con el servidor...'
  estadisticas.value = {
    registros_limpiados: 0,
    asistencias_limpiadas: 0,
    archivos_eliminados: 0,
    archivos_no_encontrados: 0,
    total_procesado: 0,
    errores: 0
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
  max-height: 85vh;
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
  background: linear-gradient(135deg, rgba(249, 115, 22, 0.05) 0%, rgba(234, 88, 12, 0.05) 100%);
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
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
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
    box-shadow: 0 0 0 0 rgba(249, 115, 22, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 12px rgba(249, 115, 22, 0);
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
  font-size: 22px;
  font-weight: 700;
  color: #1f2937;
}

.subtitle {
  margin: 8px 0 0;
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.periodo-text {
  color: #ea580c;
  font-weight: 600;
}

.progress-section {
  padding: 24px 28px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.progress-bar {
  width: 100%;
  height: 10px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 12px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #f97316 0%, #ea580c 100%);
  border-radius: 10px;
  transition: width 0.3s ease;
  box-shadow: 0 0 20px rgba(249, 115, 22, 0.5);
  position: relative;
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.progress-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.percentage {
  font-size: 18px;
  font-weight: 700;
  color: #ea580c;
}

.progress-message {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
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
  background: rgba(249, 115, 22, 0.08);
  border-color: rgba(249, 115, 22, 0.2);
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
  color: #9ca3af;
}

.info-item.completado .info-icon {
  color: #ea580c;
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
}

.value {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
}

.info-item.completado .value {
  color: #c2410c;
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
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
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
  background: linear-gradient(135deg, rgba(249, 115, 22, 0.1) 0%, rgba(234, 88, 12, 0.05) 100%);
  border: 1px solid rgba(249, 115, 22, 0.2);
  border-radius: 12px;
}

.stat-value {
  font-size: 36px;
  font-weight: 800;
  color: #ea580c;
}

.stat-label {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
  margin-top: 4px;
}

.summary-text {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.6;
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
  cursor: pointer;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(249, 115, 22, 0.3);
}

.btn-aceptar:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(249, 115, 22, 0.4);
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
    font-size: 18px;
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
