<template>
  <div v-if="show" class="descarga-overlay">
    <div class="descarga-modal">
      <!-- Header -->
      <div class="descarga-header">
        <div class="descarga-title">
          <div class="descarga-icon">⚡</div>
          <h3>Descargando BD Completa</h3>
        </div>
      </div>

      <!-- Contenido -->
      <div class="descarga-content">
        <!-- Barra de progreso principal -->
        <div class="progress-section">
          <div class="progress-info">
            <span class="progress-label">Progreso de descarga</span>
            <span class="progress-percent">{{ progreso }}%</span>
          </div>
          <div class="progress-bar-container">
            <div class="progress-bar" :style="{ width: progreso + '%' }">
              <div class="progress-bar-shimmer"></div>
            </div>
          </div>
        </div>

        <!-- Estadísticas de descarga -->
        <div class="descarga-stats">
          <div class="stat-item">
            <div class="stat-icon">📊</div>
            <div class="stat-content">
              <div class="stat-label">Descargado</div>
              <div class="stat-value">{{ bytesDescargadosFormato }}</div>
            </div>
          </div>

          <div class="stat-item">
            <div class="stat-icon">📦</div>
            <div class="stat-content">
              <div class="stat-label">Tamaño Total</div>
              <div class="stat-value">{{ tamanoTotalFormato }}</div>
            </div>
          </div>

          <div class="stat-item">
            <div class="stat-icon">⚡</div>
            <div class="stat-content">
              <div class="stat-label">Velocidad</div>
              <div class="stat-value">{{ velocidadDescarga }}</div>
            </div>
          </div>

          <div class="stat-item">
            <div class="stat-icon">⏱️</div>
            <div class="stat-content">
              <div class="stat-label">Tiempo restante</div>
              <div class="stat-value">{{ tiempoRestante }}</div>
            </div>
          </div>
        </div>

        <!-- Mensaje de estado -->
        <div class="descarga-message">
          {{ mensaje }}
        </div>

        <!-- Animación de puntos -->
        <div class="descarga-loading">
          <div class="dot"></div>
          <div class="dot"></div>
          <div class="dot"></div>
        </div>
      </div>

      <!-- Footer -->
      <div class="descarga-footer">
        <p class="descarga-note">No cierre esta ventana durante la descarga</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['cancelar', 'completado'])

// Estado de descarga
const bytesDescargados = ref(0)
const tamanoTotal = ref(0)
const velocidadActual = ref(0)
const tiempoInicio = ref(null)
const mensaje = ref('Iniciando descarga...')

// Computadas
const progreso = computed(() => {
  if (tamanoTotal.value === 0) return 0
  return Math.round((bytesDescargados.value / tamanoTotal.value) * 100)
})

const bytesDescargadosFormato = computed(() => {
  return formatearBytes(bytesDescargados.value)
})

const tamanoTotalFormato = computed(() => {
  return formatearBytes(tamanoTotal.value)
})

const velocidadDescarga = computed(() => {
  if (velocidadActual.value === 0) return '0 KB/s'
  return formatearBytes(velocidadActual.value) + '/s'
})

const tiempoRestante = computed(() => {
  if (velocidadActual.value === 0 || tamanoTotal.value === 0) return '--:--'
  
  const bytesRestantes = tamanoTotal.value - bytesDescargados.value
  const segundosRestantes = Math.ceil(bytesRestantes / velocidadActual.value)
  
  if (segundosRestantes > 3600) {
    const horas = Math.floor(segundosRestantes / 3600)
    const minutos = Math.floor((segundosRestantes % 3600) / 60)
    return `${horas}h ${minutos}m`
  }
  
  if (segundosRestantes > 60) {
    const minutos = Math.floor(segundosRestantes / 60)
    const segundos = segundosRestantes % 60
    return `${minutos}m ${segundos}s`
  }
  
  return `${segundosRestantes}s`
})

// Funciones
function formatearBytes(bytes) {
  if (bytes === 0) return '0 B'
  
  const k = 1024
  const tamanios = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + tamanios[i]
}

function actualizar(datos) {
  if (datos.bytesDescargados !== undefined) {
    bytesDescargados.value = datos.bytesDescargados
  }
  if (datos.tamanoTotal !== undefined) {
    tamanoTotal.value = datos.tamanoTotal
  }
  if (datos.velocidad !== undefined) {
    velocidadActual.value = datos.velocidad
  }
  if (datos.mensaje !== undefined) {
    mensaje.value = datos.mensaje
  }
}

function iniciar() {
  bytesDescargados.value = 0
  tamanoTotal.value = 0
  velocidadActual.value = 0
  tiempoInicio.value = Date.now()
  mensaje.value = 'Iniciando descarga...'
}

function completar() {
  mensaje.value = '✅ Descarga completada exitosamente'
}

function cancelar() {
  emit('cancelar')
}

// Exponer métodos
defineExpose({
  actualizar,
  iniciar,
  completar,
  cancelar
})

// Watch para cambios en el show
watch(() => props.show, (newVal) => {
  if (newVal) {
    iniciar()
  }
})
</script>

<style scoped>
.descarga-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.descarga-modal {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 420px;
  overflow: hidden;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Header */
.descarga-header {
  background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%);
  padding: 20px;
  color: white;
}

.descarga-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.descarga-icon {
  font-size: 28px;
  animation: bounce 0.6s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-6px);
  }
}

.descarga-title h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
}

/* Contenido */
.descarga-content {
  padding: 24px;
}

/* Progress Section */
.progress-section {
  margin-bottom: 24px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.progress-label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  font-family: 'Inter', sans-serif;
}

.progress-percent {
  font-size: 16px;
  font-weight: 700;
  color: #ec4899;
  font-family: 'Inter', sans-serif;
}

.progress-bar-container {
  width: 100%;
  height: 8px;
  background: #e5e7eb;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06);
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #ec4899 0%, #f472b6 100%);
  border-radius: 10px;
  transition: width 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(236, 72, 153, 0.5);
}

.progress-bar-shimmer {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
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
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

/* Estadísticas */
.descarga-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 20px;
}

@media (max-width: 480px) {
  .descarga-stats {
    grid-template-columns: 1fr;
  }
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.05) 0%, rgba(244, 114, 182, 0.05) 100%);
  border: 1px solid rgba(236, 72, 153, 0.1);
  border-radius: 10px;
  transition: all 0.2s ease;
}

.stat-item:hover {
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.1) 0%, rgba(244, 114, 182, 0.1) 100%);
  border-color: rgba(236, 72, 153, 0.2);
}

.stat-icon {
  font-size: 20px;
  min-width: 20px;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
}

.stat-value {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  font-family: 'Inter', monospace;
}

/* Mensaje */
.descarga-message {
  text-align: center;
  font-size: 13px;
  color: #6b7280;
  margin-bottom: 16px;
  font-family: 'Inter', sans-serif;
  min-height: 18px;
}

/* Loading Animation */
.descarga-loading {
  display: flex;
  justify-content: center;
  gap: 6px;
  margin-top: 16px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ec4899;
  animation: dot-bounce 1.4s infinite;
}

.dot:nth-child(1) {
  animation-delay: -0.32s;
}

.dot:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes dot-bounce {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Footer */
.descarga-footer {
  padding: 12px 24px;
  background: rgba(249, 250, 251, 0.8);
  border-top: 1px solid #e5e7eb;
  text-align: center;
}

.descarga-note {
  margin: 0;
  font-size: 12px;
  color: #9ca3af;
  font-family: 'Inter', sans-serif;
}

/* Responsive Design */
@media (max-width: 600px) {
  .descarga-modal {
    max-width: calc(100% - 32px);
    margin: 16px;
  }

  .descarga-content {
    padding: 16px;
  }

  .descarga-header {
    padding: 16px;
  }

  .descarga-title h3 {
    font-size: 16px;
  }

  .progress-label {
    font-size: 12px;
  }

  .progress-percent {
    font-size: 14px;
  }

  .stat-label {
    font-size: 11px;
  }

  .stat-value {
    font-size: 13px;
  }

  .descarga-message {
    font-size: 12px;
  }
}
</style>
