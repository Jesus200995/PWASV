<template>
  <div class="fixed inset-0 bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 overflow-hidden" style="z-index: 0;">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-emerald-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-teal-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>

    <div class="absolute inset-0 overflow-y-auto pt-16 sm:pt-20 pb-3" style="z-index: 1;">
      <div class="page-container w-full max-w-sm mx-auto relative z-10 p-3 sm:p-4 lg:p-5">
        
        <!-- Header de notificaciones -->
        <div class="glass-card mb-2">
          <div class="text-center mb-3">
            <div class="inline-flex items-center justify-center w-12 h-12 bg-gradient-to-br from-green-400 to-emerald-500 rounded-full glass-avatar mb-2">
              <span class="text-white text-xl font-bold">📨</span>
            </div>
            <h1 class="text-base font-semibold text-gray-800 modern-title">
              Mis Notificaciones
            </h1>
            <p class="text-xs text-gray-600 mt-1">
              {{ usuario?.nombre_completo || 'Usuario' }}
            </p>
          </div>
        </div>

        <!-- Estado de carga -->
        <div v-if="cargando" class="glass-card mb-2">
          <div class="flex items-center justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-green-500"></div>
            <span class="ml-3 text-gray-600 text-sm">Cargando notificaciones...</span>
          </div>
        </div>

        <!-- Error de conexión -->
        <div v-if="error && !cargando" class="glass-card mb-2">
          <div class="text-center py-6">
            <div class="text-4xl mb-3">⚠️</div>
            <h3 class="text-sm font-medium text-gray-800 mb-2">Error de Conexión</h3>
            <p class="text-xs text-gray-600 mb-4">{{ error }}</p>
            <button 
              @click="cargarNotificaciones"
              class="px-4 py-2 bg-green-500 text-white text-xs rounded-lg hover:bg-green-600 transition-colors"
            >
              Reintentar
            </button>
          </div>
        </div>

        <!-- Filtros y estadísticas -->
        <div v-if="!cargando && !error" class="glass-card mb-2">
          <div class="flex justify-between items-center mb-2">
            <h2 class="text-sm font-semibold text-gray-800 modern-title">Filtros</h2>
            <button 
              @click="cargarNotificaciones"
              class="text-green-600 hover:text-green-700 transition-colors"
              title="Actualizar notificaciones"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
            </button>
          </div>
          <div class="green-line mb-2"></div>
          
          <!-- Toggle para mostrar solo no leídas -->
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs text-gray-700">Solo recientes</span>
            <button 
              @click="toggleSoloRecientes"
              :class="[
                'relative inline-flex h-5 w-9 items-center rounded-full transition-colors',
                soloRecientes ? 'bg-green-500' : 'bg-gray-300'
              ]"
            >
              <span 
                :class="[
                  'inline-block h-3 w-3 transform rounded-full bg-white transition-transform',
                  soloRecientes ? 'translate-x-5' : 'translate-x-1'
                ]"
              ></span>
            </button>
          </div>
          
          <!-- Estadísticas -->
          <div class="grid grid-cols-2 gap-2 text-center">
            <div class="bg-white bg-opacity-30 rounded-lg p-2">
              <div class="text-lg font-bold text-green-600">{{ totalNotificaciones }}</div>
              <div class="text-xs text-gray-600">Total</div>
            </div>
            <div class="bg-white bg-opacity-30 rounded-lg p-2">
              <div class="text-lg font-bold text-blue-600">{{ notificacionesRecientes }}</div>
              <div class="text-xs text-gray-600">Recientes</div>
            </div>
          </div>
        </div>

        <!-- Lista de notificaciones -->
        <div v-if="!cargando && !error" class="glass-card">
          <h2 class="text-sm font-semibold text-gray-800 mb-2 modern-title flex items-center">
            <span class="mr-2">📋</span>
            Notificaciones
            <span v-if="notificacionesFiltradas.length > 0" class="ml-auto text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
              {{ notificacionesFiltradas.length }}
            </span>
          </h2>
          <div class="green-line mb-3"></div>
          
          <!-- Lista de notificaciones -->
          <div v-if="notificacionesFiltradas.length > 0" class="space-y-2">
            <div 
              v-for="notificacion in notificacionesFiltradas" 
              :key="notificacion.id"
              class="notification-item bg-white bg-opacity-40 rounded-lg p-3 cursor-pointer hover:bg-opacity-60 transition-all"
              @click="abrirDetalleNotificacion(notificacion)"
            >
              <div class="flex items-start space-x-3">
                <!-- Icono de tipo -->
                <div class="flex-shrink-0 w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                  <span class="text-sm">
                    {{ notificacion.tiene_archivo ? obtenerIconoArchivo(notificacion.archivo_tipo) : '📢' }}
                  </span>
                </div>
                
                <!-- Contenido -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between mb-1">
                    <h3 class="text-sm font-medium text-gray-900 truncate">
                      {{ notificacion.titulo }}
                    </h3>
                    <div class="flex items-center space-x-1">
                      <span v-if="notificacion.tiene_archivo" class="text-xs text-green-600" title="Tiene archivo adjunto">
                        📎
                      </span>
                      <span v-if="esReciente(notificacion.fecha_creacion)" class="w-2 h-2 bg-blue-500 rounded-full" title="Reciente"></span>
                    </div>
                  </div>
                  
                  <p v-if="notificacion.subtitulo" class="text-xs text-gray-700 mb-1">
                    {{ notificacion.subtitulo }}
                  </p>
                  
                  <p class="text-xs text-gray-600 line-clamp-2 mb-2">
                    {{ notificacion.descripcion }}
                  </p>
                  
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-gray-500">
                      {{ formatearFecha(notificacion.fecha_creacion) }}
                    </span>
                    <div class="flex items-center space-x-2">
                      <span v-if="notificacion.enviada_a_todos" class="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full">
                        Todos
                      </span>
                      <span v-else class="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
                        Personal
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Estado vacío -->
          <div v-else class="text-center py-8">
            <div class="text-4xl mb-3">📭</div>
            <h3 class="text-sm font-medium text-gray-800 mb-2">Sin notificaciones</h3>
            <p class="text-xs text-gray-600 mb-4">
              {{ soloRecientes ? 'No hay notificaciones recientes' : 'No tienes notificaciones por el momento' }}
            </p>
            <button 
              v-if="soloRecientes"
              @click="toggleSoloRecientes"
              class="text-xs text-green-600 hover:text-green-700"
            >
              Ver todas las notificaciones
            </button>
          </div>
        </div>

        <!-- Botón cargar más -->
        <div v-if="!cargando && !error && puedeCargarMas" class="text-center mt-3">
          <button 
            @click="cargarMasNotificaciones"
            :disabled="cargandoMas"
            class="px-4 py-2 bg-green-500 text-white text-xs rounded-lg hover:bg-green-600 transition-colors disabled:opacity-50"
          >
            {{ cargandoMas ? 'Cargando...' : 'Cargar más' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de detalle de notificación -->
    <div v-if="notificacionSeleccionada" 
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
         @click="cerrarDetalleNotificacion">
      <div class="bg-white rounded-2xl max-w-sm w-full max-h-[90vh] overflow-hidden" @click.stop>
        <!-- Header del modal -->
        <div class="bg-gradient-to-r from-green-500 to-emerald-500 text-white p-4">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-semibold truncate flex-1 mr-4">
              {{ notificacionSeleccionada.titulo }}
            </h2>
            <button 
              @click="cerrarDetalleNotificacion"
              class="text-white hover:text-gray-200 transition-colors"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          <p v-if="notificacionSeleccionada.subtitulo" class="text-sm text-green-100 mt-1">
            {{ notificacionSeleccionada.subtitulo }}
          </p>
        </div>

        <!-- Contenido del modal -->
        <div class="p-4 overflow-y-auto" style="max-height: calc(90vh - 200px);">
          <!-- Información de fecha -->
          <div class="mb-4 p-3 bg-gray-50 rounded-lg">
            <div class="text-xs text-gray-600 mb-1">Fecha de envío</div>
            <div class="text-sm font-medium">
              {{ formatearFechaCompleta(notificacionSeleccionada.fecha_creacion) }}
            </div>
          </div>

          <!-- Descripción -->
          <div class="mb-4">
            <h3 class="text-sm font-medium text-gray-800 mb-2">Descripción</h3>
            <p class="text-sm text-gray-700 whitespace-pre-wrap">
              {{ notificacionSeleccionada.descripcion }}
            </p>
          </div>

          <!-- Enlace URL -->
          <div v-if="notificacionSeleccionada.enlace_url" class="mb-4">
            <h3 class="text-sm font-medium text-gray-800 mb-2">Enlace</h3>
            <a 
              :href="notificacionSeleccionada.enlace_url" 
              target="_blank"
              class="text-sm text-blue-600 hover:text-blue-800 underline break-all"
            >
              {{ notificacionSeleccionada.enlace_url }}
            </a>
          </div>

          <!-- Archivo adjunto -->
          <div v-if="notificacionSeleccionada.tiene_archivo" class="mb-4">
            <h3 class="text-sm font-medium text-gray-800 mb-2">Archivo adjunto</h3>
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <span class="text-lg">{{ obtenerIconoArchivo(notificacionSeleccionada.archivo_tipo) }}</span>
                  <div>
                    <div class="text-sm font-medium text-gray-800">
                      {{ notificacionSeleccionada.archivo_nombre }}
                    </div>
                    <div class="text-xs text-gray-600 capitalize">
                      {{ notificacionSeleccionada.archivo_tipo }}
                    </div>
                  </div>
                </div>
                <button 
                  @click="abrirArchivo(notificacionSeleccionada.id)"
                  class="px-3 py-1 bg-green-500 text-white text-xs rounded hover:bg-green-600 transition-colors"
                >
                  Ver
                </button>
              </div>
            </div>
          </div>

          <!-- Tipo de notificación -->
          <div class="flex items-center justify-between text-xs text-gray-500">
            <span>
              {{ notificacionSeleccionada.enviada_a_todos ? 'Enviado a todos los usuarios' : 'Notificación personal' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import notificacionesService from '../services/notificacionesService.js'

// Estados reactivos
const notificaciones = ref([])
const notificacionSeleccionada = ref(null)
const usuario = ref(null)
const cargando = ref(false)
const cargandoMas = ref(false)
const error = ref('')
const soloRecientes = ref(true)

// Paginación
const limit = ref(10)
const offset = ref(0)
const totalNotificaciones = ref(0)

// Computed properties
const notificacionesFiltradas = computed(() => {
  if (!soloRecientes.value) {
    return notificaciones.value
  }
  
  // Mostrar notificaciones de los últimos 7 días
  const hace7Dias = new Date()
  hace7Dias.setDate(hace7Dias.getDate() - 7)
  
  return notificaciones.value.filter(notificacion => {
    const fechaNotificacion = new Date(notificacion.fecha_creacion)
    return fechaNotificacion >= hace7Dias
  })
})

const notificacionesRecientes = computed(() => {
  const hace7Dias = new Date()
  hace7Dias.setDate(hace7Dias.getDate() - 7)
  
  return notificaciones.value.filter(notificacion => {
    const fechaNotificacion = new Date(notificacion.fecha_creacion)
    return fechaNotificacion >= hace7Dias
  }).length
})

const puedeCargarMas = computed(() => {
  return notificaciones.value.length < totalNotificaciones.value
})

// Variables para interval
let autoUpdateInterval = null

// Funciones
const obtenerUsuarioId = () => {
  // Obtener ID del usuario del localStorage
  const userData = localStorage.getItem('userData')
  if (userData) {
    try {
      const user = JSON.parse(userData)
      return user.id || user.usuario_id
    } catch (e) {
      console.error('Error parseando userData:', e)
    }
  }
  
  // Fallback: obtener de otras fuentes
  const userId = localStorage.getItem('userId') || localStorage.getItem('user_id')
  return userId ? parseInt(userId) : null
}

const cargarNotificaciones = async (resetear = true) => {
  try {
    const usuarioId = obtenerUsuarioId()
    
    if (!usuarioId) {
      error.value = 'No se pudo identificar al usuario. Inicia sesión nuevamente.'
      return
    }

    if (resetear) {
      cargando.value = true
      offset.value = 0
      notificaciones.value = []
      error.value = ''
    } else {
      cargandoMas.value = true
    }

    console.log(`📱 Cargando notificaciones para usuario ${usuarioId}`)
    
    const response = await notificacionesService.obtenerNotificacionesUsuario(
      usuarioId, 
      limit.value, 
      offset.value
    )

    if (resetear) {
      notificaciones.value = response.notificaciones || []
      usuario.value = response.usuario
    } else {
      notificaciones.value.push(...(response.notificaciones || []))
    }
    
    totalNotificaciones.value = response.total || 0
    offset.value += limit.value

    console.log(`✅ ${response.notificaciones?.length || 0} notificaciones cargadas`)
    
  } catch (err) {
    console.error('Error cargando notificaciones:', err)
    error.value = err.message || 'Error al cargar las notificaciones'
  } finally {
    cargando.value = false
    cargandoMas.value = false
  }
}

const cargarMasNotificaciones = () => {
  if (!cargandoMas.value && puedeCargarMas.value) {
    cargarNotificaciones(false)
  }
}

const toggleSoloRecientes = () => {
  soloRecientes.value = !soloRecientes.value
  localStorage.setItem('soloRecientes', soloRecientes.value.toString())
}

const abrirDetalleNotificacion = (notificacion) => {
  notificacionSeleccionada.value = {
    ...notificacion,
    tiene_archivo: notificacionesService.tieneArchivo(notificacion)
  }
}

const cerrarDetalleNotificacion = () => {
  notificacionSeleccionada.value = null
}

const abrirArchivo = (notificacionId) => {
  const url = notificacionesService.obtenerUrlArchivo(notificacionId)
  window.open(url, '_blank')
}

const obtenerIconoArchivo = (tipoArchivo) => {
  return notificacionesService.obtenerIconoArchivo(tipoArchivo)
}

const formatearFecha = (fechaISO) => {
  return notificacionesService.formatearFecha(fechaISO)
}

const formatearFechaCompleta = (fechaISO) => {
  return notificacionesService.formatearFechaCompleta(fechaISO)
}

const esReciente = (fechaISO) => {
  if (!fechaISO) return false
  
  const fecha = new Date(fechaISO)
  const ahora = new Date()
  const diferencia = ahora - fecha
  
  // Menos de 24 horas
  return diferencia < 86400000
}

const cargarConfiguracion = () => {
  // Cargar configuración de solo recientes
  const savedSoloRecientes = localStorage.getItem('soloRecientes')
  if (savedSoloRecientes !== null) {
    soloRecientes.value = savedSoloRecientes === 'true'
  }
}

// Ciclo de vida
onMounted(async () => {
  console.log('📱 Componente Notificaciones montado')
  
  cargarConfiguracion()
  
  // Cargar notificaciones inicial
  await cargarNotificaciones()
  
  // Auto-actualizar cada 5 minutos
  autoUpdateInterval = setInterval(() => {
    if (!cargando.value && !cargandoMas.value) {
      console.log('🔄 Auto-actualizando notificaciones...')
      cargarNotificaciones()
    }
  }, 5 * 60 * 1000) // 5 minutos
})

onBeforeUnmount(() => {
  if (autoUpdateInterval) {
    clearInterval(autoUpdateInterval)
  }
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Efecto de vidrio realista - Glassmorphism */
.glass-card {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 6px 25px 0 rgba(31, 38, 135, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  padding: 0.875rem;
  position: relative;
  overflow: hidden;
}

.glass-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -50%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  transform: skewX(-25deg);
  transition: all 0.6s;
}

.glass-card:hover::before {
  left: 150%;
}

.glass-avatar {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px 0 rgba(59, 130, 246, 0.3),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
}

.modern-title {
  background: linear-gradient(
    90deg, 
    #166534 0%, 
    #15803d 25%, 
    #86efac 50%, 
    #15803d 75%, 
    #166534 100%
  );
  background-size: 300% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: gradient-wave 3s ease-in-out infinite;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  letter-spacing: -0.015em;
  font-weight: 500;
  position: relative;
}

.green-line {
  width: 40px;
  height: 1.5px;
  background: linear-gradient(90deg, #16a34a, #22c55e, #16a34a);
  border-radius: 1px;
  animation: line-glow 2s ease-in-out infinite alternate;
}

@keyframes gradient-wave {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

@keyframes line-glow {
  0% {
    box-shadow: 0 0 5px rgba(34, 197, 94, 0.3);
    opacity: 0.8;
  }
  100% {
    box-shadow: 0 0 15px rgba(34, 197, 94, 0.6);
    opacity: 1;
  }
}

/* Animación para elementos decorativos */
@keyframes pulse-slow {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.05);
  }
}

.animate-pulse-slow {
  animation: pulse-slow 4s ease-in-out infinite;
}

/* Respaldo para navegadores que no soportan background-clip: text */
@supports not (-webkit-background-clip: text) {
  .modern-title {
    color: #166534;
    animation: none;
  }
}

/* Estilos para notificaciones */
.notification-item {
  transition: all 0.2s ease;
}

.notification-item:hover {
  transform: translateX(2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Limitador de líneas */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Mejoras de responsividad para pantallas móviles */
@media (max-width: 480px) {
  .page-container {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
  }
  
  .glass-card {
    padding: 0.625rem;
    margin-bottom: 0.375rem;
    border-radius: 12px;
  }
  
  .text-base {
    font-size: 0.8rem;
  }
  
  .text-sm {
    font-size: 0.75rem;
  }
  
  .w-12, .h-12 {
    width: 2.75rem;
    height: 2.75rem;
  }
  
  .h-6, .w-6 {
    height: 1.25rem;
    width: 1.25rem;
  }
  
  .mb-2 {
    margin-bottom: 0.375rem;
  }
  
  .mb-3 {
    margin-bottom: 0.5rem;
  }
  
  .space-y-3 > * + * {
    margin-top: 0.5rem;
  }
}

@media (max-width: 375px) {
  .page-container {
    padding-left: 0.375rem;
    padding-right: 0.375rem;
    max-width: calc(100vw - 0.75rem);
  }
  
  .glass-card {
    padding: 0.5rem;
    margin-bottom: 0.25rem;
    border-radius: 10px;
  }
  
  .text-base {
    font-size: 0.75rem;
  }
  
  .text-sm {
    font-size: 0.7rem;
  }
  
  .text-xs {
    font-size: 0.65rem;
  }
}

@media (max-height: 700px) {
  .page-container {
    padding-top: 0.375rem;
    padding-bottom: 0.375rem;
  }
  
  .glass-card {
    margin-bottom: 0.25rem;
    padding: 0.5rem;
  }
  
  .mb-2 {
    margin-bottom: 0.25rem;
  }
  
  .mb-3 {
    margin-bottom: 0.375rem;
  }
  
  .space-y-3 > * + * {
    margin-top: 0.375rem;
  }
}

/* Para pantallas grandes */
@media (min-width: 768px) {
  .page-container {
    max-width: 350px;
    padding: 0.75rem;
  }
  
  .glass-card {
    padding: 1rem;
    margin-bottom: 0.75rem;
  }
}

/* Soporte adicional para navegadores que no soportan backdrop-filter */
@supports not (backdrop-filter: blur(20px)) {
  .glass-card {
    background: rgba(255, 255, 255, 0.85);
  }
}
</style>
