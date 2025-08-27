<template>
  <div class="fixed inset-0 bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 overflow-hidden" style="z-index: 0;">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-emerald-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-teal-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>

    <div class="absolute inset-0 overflow-hidden" style="z-index: 1;">
      <!-- Header fijo de notificaciones -->
      <div class="fixed top-16 sm:top-20 left-0 right-0 z-20 px-2 sm:px-3 lg:px-4 pt-2 sm:pt-3">
        <div class="w-full max-w-md mx-auto">
          <div class="glass-card mb-0 relative">
            <div class="text-center mb-1 relative py-0.5">
              <h1 class="text-sm font-medium text-gray-800 modern-title">
                Mis Notificaciones
              </h1>
              <!-- Botón de refresh movido al lado derecho -->
              <button 
                @click="refrescarNotificaciones"
                :disabled="cargando"
                class="absolute top-1/2 right-3 transform -translate-y-1/2 p-2 rounded-full hover:bg-white hover:bg-opacity-20 transition-colors duration-200 group"
                :class="{ 'cursor-not-allowed opacity-50': cargando }"
                title="Actualizar notificaciones"
              >
                <svg 
                  class="w-5 h-5 text-gray-600 group-hover:text-gray-800 transition-colors duration-200"
                  :class="{ 'animate-spin': cargando }"
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path 
                    stroke-linecap="round" 
                    stroke-linejoin="round" 
                    stroke-width="2" 
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
              </button>
            </div>
          </div>
          
          <!-- Componente de configuración de notificaciones push -->
          <div class="mb-2">
            <PushNotificationSetup 
              :usuario-id="usuario?.id || obtenerUsuarioId()"
              @subscribed="onPushSubscribed"
              @unsubscribed="onPushUnsubscribed"
              @error="onPushError"
            />
          </div>
          
          <!-- Título de notificaciones fijo -->
          <div class="bg-transparent rounded-xl p-1">
            <h2 class="text-sm font-semibold text-gray-800 mb-1 modern-title flex items-center">
              <span class="mr-2">📋</span>
              Notificaciones
              <span v-if="notificacionesFiltradas.length > 0" class="ml-auto text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                {{ notificacionesFiltradas.length }}
              </span>
            </h2>
            <div class="green-line mb-0"></div>
          </div>
        </div>
      </div>

      <!-- Contenido con scroll -->
      <div class="absolute inset-0 overflow-hidden pt-56 sm:pt-60 pb-2">
        <div class="page-container w-full max-w-md mx-auto relative z-10 px-2 sm:px-3 lg:px-4 py-1 h-full">

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

        <!-- Contenedor de scroll para notificaciones -->
        <div v-if="!cargando && !error" class="h-full flex flex-col">
          <!-- Lista de notificaciones con scroll propio -->
          <div class="flex-1 overflow-y-auto bg-transparent rounded-xl px-2 py-4 notifications-scroll-container">
            <div v-if="notificacionesFiltradas.length > 0" class="space-y-2">
            <div 
              v-for="(notificacion, index) in notificacionesFiltradas" 
              :key="notificacion.id"
              :class="[
                'notification-item rounded-xl p-3 transition-all duration-300 cursor-pointer shadow-lg border-2 hover:shadow-xl relative',
                notificacion.leida 
                  ? 'bg-white border-gray-300 hover:border-gray-400 hover:bg-gray-50' 
                  : 'bg-red-50 border-red-400 hover:border-red-500 hover:bg-red-100'
              ]"
              @click="abrirDetalleNotificacion(notificacion)"
            >
              <!-- Campanita animada para notificaciones no leídas -->
              <div v-if="!notificacion.leida" class="absolute -top-1 -right-1 z-20">
                <div class="bg-red-600 rounded-full w-6 h-6 flex items-center justify-center shadow-sm bell-container">
                  <svg class="bell-icon w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/>
                  </svg>
                </div>
              </div>
              
              <div class="flex items-start space-x-3">
                <!-- Icono de tipo -->
                <div class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center"
                     :class="notificacion.leida 
                       ? 'bg-green-600 shadow-lg shadow-gray-200' 
                       : 'bg-red-600 shadow-lg shadow-gray-200'">
                  <!-- Ícono de correo blanco -->
                  <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                    <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                  </svg>
                </div>
                
                <!-- Contenido -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between mb-1">
                    <div class="flex items-center space-x-2 flex-1 min-w-0">
                      <h3 class="text-sm font-medium text-gray-900 truncate">
                        {{ notificacion.titulo }}
                      </h3>
                    </div>
                  </div>
                  
                  <p v-if="notificacion.subtitulo" class="text-xs text-gray-700 mb-1">
                    {{ notificacion.subtitulo }}
                  </p>
                  
                  <p class="text-xs text-gray-600 line-clamp-2 mb-2">
                    {{ notificacion.descripcion }}
                  </p>

                  <!-- Vista previa de archivo -->
                  <div v-if="notificacion.tiene_archivo" class="mb-3 w-full flex justify-center items-center">
                    <div v-if="esImagen(notificacion.archivo_tipo)" class="aspect-square w-full max-w-[180px] bg-gray-100 rounded-lg overflow-hidden relative">
                      <!-- Placeholder de carga -->
                      <div class="absolute inset-0 flex items-center justify-center bg-gray-100 image-placeholder">
                        <div class="text-gray-400 text-center">
                          <div class="text-lg mb-1">🖼️</div>
                          <div class="text-xs">Cargando...</div>
                        </div>
                      </div>
                      <!-- Imagen real -->
                      <img 
                        :src="obtenerUrlArchivo(notificacion.id)" 
                        :alt="notificacion.archivo_nombre"
                        class="w-full h-full object-cover cursor-pointer hover:opacity-90 transition-opacity relative z-10"
                        @click.stop="abrirArchivo(notificacion.id)"
                        @error="onImageError"
                        @load="onImageLoad"
                        loading="lazy"
                      />
                    </div>
                    <div v-else-if="esVideo(notificacion.archivo_tipo)" class="aspect-video w-full max-w-[180px] bg-gray-100 rounded-lg overflow-hidden">
                      <video 
                        :src="obtenerUrlArchivo(notificacion.id)"
                        class="w-full h-full object-cover cursor-pointer"
                        controls
                        preload="metadata"
                        @click.stop
                      >
                        Tu navegador no soporta video.
                      </video>
                    </div>
                    <div v-else class="bg-gray-50 rounded-lg p-2 max-w-[180px]">
                      <div class="flex items-center space-x-2">
                        <span class="text-lg">{{ obtenerIconoArchivo(notificacion.archivo_tipo) }}</span>
                        <div class="flex-1 min-w-0">
                          <div class="text-xs font-medium text-gray-800 truncate">
                            {{ notificacion.archivo_nombre }}
                          </div>
                          <div class="text-xs text-gray-600 capitalize">
                            {{ notificacion.archivo_tipo }}
                          </div>
                        </div>
                        <button 
                          @click.stop="abrirArchivo(notificacion.id)"
                          class="px-2 py-1 bg-green-500 text-white text-xs rounded hover:bg-green-600 transition-colors"
                        >
                          Ver
                        </button>
                      </div>
                    </div>
                  </div>
                  
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-gray-500">
                      {{ formatearFecha(notificacion.fecha_creacion) }}
                    </span>
                  </div>
                  
                  <!-- Botón Ver completo más pequeño -->
                  <div class="flex justify-center items-center w-full mt-3 px-2">
                    <button class="group professional-button px-3 py-1.5 text-gray-700 text-2xs font-medium border border-gray-300 rounded-md transition-all duration-300 hover:border-green-500 hover:text-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50 mx-auto">
                      <span class="flex items-center justify-center space-x-1">
                        <span class="whitespace-nowrap">Ver completo</span>
                        <svg class="w-2.5 h-2.5 transition-transform duration-300 group-hover:translate-x-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                        </svg>
                      </span>
                    </button>
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
          <div v-if="puedeCargarMas" class="text-center mt-3 flex-shrink-0">
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
    </div>

    <!-- Modal de detalle de notificación -->
    <div v-if="notificacionSeleccionada" 
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-2 sm:p-4 z-50"
         @click="cerrarDetalleNotificacion">
      <div class="bg-white rounded-xl max-w-xs sm:max-w-sm w-full max-h-[85vh] sm:max-h-[90vh] overflow-hidden" @click.stop>
        <!-- Header del modal -->
        <div class="bg-gradient-to-r from-green-500 to-emerald-500 text-white p-3">
          <div class="flex items-start justify-between">
            <div class="flex-1 min-w-0 mr-3">
              <h2 class="text-sm sm:text-base font-medium truncate">
                {{ notificacionSeleccionada.titulo }}
              </h2>
              <p v-if="notificacionSeleccionada.subtitulo" class="text-xs sm:text-sm text-green-100 mt-1">
                {{ notificacionSeleccionada.subtitulo }}
              </p>
            </div>
            <button 
              @click="cerrarDetalleNotificacion"
              class="bg-white bg-opacity-20 hover:bg-opacity-30 rounded-full p-2 transition-all duration-200 flex-shrink-0"
            >
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
        </div>

        <!-- Contenido del modal -->
        <div class="p-3 overflow-y-auto" style="max-height: calc(85vh - 120px);">
          <!-- Descripción -->
          <div class="mb-3">
            <h3 class="text-xs font-medium text-gray-800 mb-2">Descripción</h3>
            <p class="text-xs text-gray-700 whitespace-pre-wrap">
              {{ notificacionSeleccionada.descripcion }}
            </p>
          </div>

          <!-- Enlace URL -->
          <div v-if="notificacionSeleccionada.enlace_url" class="mb-3">
            <h3 class="text-xs font-medium text-gray-800 mb-2">Enlace</h3>
            <a 
              :href="notificacionSeleccionada.enlace_url" 
              target="_blank"
              class="text-xs text-blue-600 hover:text-blue-800 underline break-all"
            >
              {{ notificacionSeleccionada.enlace_url }}
            </a>
          </div>

          <!-- Archivo adjunto -->
          <div v-if="notificacionSeleccionada.tiene_archivo" class="mb-3">
            
            <!-- Vista previa de imagen -->
            <div v-if="esImagen(notificacionSeleccionada.archivo_tipo)">
              <div class="bg-gray-50 rounded-lg p-2 relative">
                <!-- Placeholder de carga -->
                <div class="flex items-center justify-center min-h-24 bg-gray-100 image-placeholder rounded">
                  <div class="text-gray-400 text-center">
                    <div class="text-lg mb-1">🖼️</div>
                    <div class="text-xs">Cargando...</div>
                  </div>
                </div>
                <!-- Imagen real -->
                <div class="flex justify-center">
                  <img 
                    :src="obtenerUrlArchivo(notificacionSeleccionada.id)" 
                    :alt="notificacionSeleccionada.archivo_nombre"
                    class="max-w-full max-h-48 object-contain rounded cursor-pointer hover:opacity-90 transition-opacity relative z-10 mx-auto"
                    @click="abrirArchivo(notificacionSeleccionada.id)"
                    @error="onImageError"
                    @load="onImageLoad"
                    loading="lazy"
                  />
                </div>
              </div>
            </div>
            
            <!-- Vista previa de video -->
            <div v-else-if="esVideo(notificacionSeleccionada.archivo_tipo)">
              <div class="bg-gray-50 rounded-lg p-2">
                <div class="flex justify-center">
                  <video 
                    :src="obtenerUrlArchivo(notificacionSeleccionada.id)"
                    class="max-w-full max-h-48 object-contain rounded mx-auto"
                    controls
                    preload="metadata"
                  >
                    Tu navegador no soporta video.
                  </video>
                </div>
              </div>
            </div>
            
            <!-- Otros archivos -->
            <div v-else class="bg-gray-50 rounded-lg p-2">
              <div class="flex items-center justify-center">
                <div class="flex items-center space-x-2">
                  <span class="text-2xl">{{ obtenerIconoArchivo(notificacionSeleccionada.archivo_tipo) }}</span>
                  <button 
                    @click="abrirArchivo(notificacionSeleccionada.id)"
                    class="px-3 py-1 bg-green-500 text-white text-xs rounded hover:bg-green-600 transition-colors"
                  >
                    Ver archivo
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Fecha de recibido -->
          <div class="px-3 pb-3 pt-2 border-t border-gray-100 mt-3">
            <div class="text-xs text-gray-500 text-center">
              Recibido: {{ formatearFechaCompleta(notificacionSeleccionada.fecha_creacion) }}
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import notificacionesService from '../services/notificacionesService.js'
import { useNotifications } from '../composables/useNotifications.js'
import PushNotificationSetup from '../components/PushNotificationSetup.vue'

// Estados reactivos
const notificaciones = ref([])
const notificacionSeleccionada = ref(null)
const usuario = ref(null)
const cargando = ref(false)
const cargandoMas = ref(false)
const error = ref('')
const soloNoLeidas = ref(false) // CAMBIO: Cambiar a no leídas por defecto
const notificacionesLeidas = ref(new Set()) // IDs de notificaciones leídas
const conteoNoLeidas = ref(0) // NUEVO: Contador de no leídas

// Sistema global de notificaciones para actualización inmediata del badge
const { fetchUnreadCount, markAsRead } = useNotifications()

// Paginación
const limit = ref(10)
const offset = ref(0)
const totalNotificaciones = ref(0)

// Computed properties ACTUALIZADOS
const notificacionesFiltradas = computed(() => {
  return notificaciones.value
})

const puedeCargarMas = computed(() => {
  return notificaciones.value.length < totalNotificaciones.value
})

// NUEVO: Computed para estadísticas
const notificacionesNoLeidasLocales = computed(() => {
  return notificacionesFiltradas.value.filter(n => !n.leida).length
})

const notificacionesTotales = computed(() => {
  return notificacionesFiltradas.value.length
})

// Variables para interval
let autoUpdateInterval = null

// Funciones MEJORADAS con nuevos endpoints
const obtenerUsuarioId = () => {
  console.log('🔍 Buscando ID de usuario en localStorage...')
  
  // 1. Buscar en 'user' (formato principal de PWASUPER)
  const userData = localStorage.getItem('user')
  if (userData) {
    try {
      const user = JSON.parse(userData)
      console.log('👤 Datos de usuario encontrados:', user)
      const id = user.id || user.usuario_id || user.user_id
      if (id) {
        console.log(`✅ ID de usuario encontrado: ${id}`)
        return parseInt(id)
      }
    } catch (e) {
      console.error('Error parseando datos de usuario:', e)
    }
  }
  
  // 2. Buscar en 'userData' (formato alternativo)
  const alternativeUserData = localStorage.getItem('userData')
  if (alternativeUserData) {
    try {
      const user = JSON.parse(alternativeUserData)
      console.log('👤 Datos alternativos encontrados:', user)
      const id = user.id || user.usuario_id || user.user_id
      if (id) {
        console.log(`✅ ID de usuario encontrado (alternativo): ${id}`)
        return parseInt(id)
      }
    } catch (e) {
      console.error('Error parseando datos alternativos:', e)
    }
  }
  
  // 3. Fallback: buscar IDs directos
  const directIds = ['userId', 'user_id', 'id']
  for (const key of directIds) {
    const id = localStorage.getItem(key)
    if (id) {
      console.log(`✅ ID directo encontrado (${key}): ${id}`)
      return parseInt(id)
    }
  }
  
  console.error('❌ No se encontró ID de usuario en localStorage')
  return null
}

// NUEVO: Obtener conteo de no leídas
const obtenerConteoNoLeidas = async (usuarioId) => {
  try {
    if (!usuarioId) return 0
    
    console.log(`📊 Obteniendo conteo de no leídas para usuario ${usuarioId}`)
    
    const conteo = await notificacionesService.obtenerConteoNoLeidas(usuarioId)
    conteoNoLeidas.value = conteo
    
    console.log(`📊 ${conteo} notificaciones no leídas`)
    return conteo
    
  } catch (err) {
    console.error('Error obteniendo conteo no leídas:', err)
    return 0
  }
}

const cargarNotificaciones = async (resetear = true) => {
  try {
    let usuarioId = obtenerUsuarioId()
    
    // Si no se encuentra un usuario, crear uno de prueba para development
    if (!usuarioId) {
      if (import.meta.env.DEV) {
        console.log('🧪 Modo desarrollo: creando datos de prueba')
        usuarioId = 1 // ID de prueba
        // Crear datos de usuario de prueba
        const testUser = {
          id: 1,
          nombre_completo: 'Usuario de Prueba',
          correo: 'test@example.com'
        }
        localStorage.setItem('user', JSON.stringify(testUser))
        usuario.value = testUser
      } else {
        error.value = 'No se pudo identificar al usuario. Inicia sesión nuevamente.'
        return
      }
    }

    if (resetear) {
      cargando.value = true
      offset.value = 0
      notificaciones.value = []
      error.value = ''
    } else {
      cargandoMas.value = true
    }

    console.log(`📱 Cargando notificaciones para usuario ${usuarioId} (filtro: ${soloNoLeidas.value ? 'no leídas' : 'todas'})`)
    
    // USAR NUEVO ENDPOINT CON FILTROS
    let response
    if (soloNoLeidas.value) {
      // Usar endpoint de lista filtrada para no leídas
      response = await notificacionesService.obtenerListaNotificaciones(
        usuarioId, 
        'unread', 
        limit.value, 
        offset.value
      )
    } else {
      // Usar endpoint de lista filtrada para todas
      response = await notificacionesService.obtenerListaNotificaciones(
        usuarioId, 
        'all', 
        limit.value, 
        offset.value
      )
    }

    if (resetear) {
      notificaciones.value = response.notificaciones || []
      if (response.usuario) {
        usuario.value = response.usuario
      }
    } else {
      notificaciones.value.push(...(response.notificaciones || []))
    }
    
    totalNotificaciones.value = response.total || 0
    offset.value += limit.value

    console.log(`✅ ${response.notificaciones?.length || 0} notificaciones cargadas`)
    
    // Obtener conteo de no leídas
    await obtenerConteoNoLeidas(usuarioId)
    
  } catch (err) {
    console.error('Error cargando notificaciones:', err)
    
    // Manejo de errores específicos
    if (err.message === 'No se puede establecer una conexión') {
      error.value = 'Sin conexión a internet. Verifica tu conexión e inténtalo de nuevo.'
    } else if (err.message.includes('404')) {
      error.value = 'Usuario no encontrado. Contacta al administrador.'
    } else if (err.message.includes('500')) {
      error.value = 'Error del servidor. Inténtalo más tarde.'
    } else {
      error.value = err.message || 'Error al cargar las notificaciones'
    }
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

// NUEVA FUNCIÓN: Refrescar notificaciones manualmente
const refrescarNotificaciones = async () => {
  if (cargando.value) return // Evitar múltiples llamadas simultáneas
  
  console.log('🔄 Refrescando notificaciones manualmente...')
  
  try {
    // Recargar notificaciones desde el inicio
    await cargarNotificaciones(true)
    
    // También actualizar el badge global
    const usuarioId = obtenerUsuarioId()
    if (usuarioId) {
      await fetchUnreadCount(usuarioId)
    }
    
    console.log('✅ Notificaciones refrescadas exitosamente')
    
  } catch (error) {
    console.error('❌ Error al refrescar notificaciones:', error)
  }
}

// NUEVO: Toggle para filtro de no leídas
const toggleFiltroNoLeidas = async () => {
  soloNoLeidas.value = !soloNoLeidas.value
  localStorage.setItem('soloNoLeidas', soloNoLeidas.value.toString())
  
  // Recargar notificaciones con nuevo filtro
  await cargarNotificaciones(true)
}

const abrirDetalleNotificacion = (notificacion) => {
  notificacionSeleccionada.value = {
    ...notificacion,
    tiene_archivo: notificacionesService.tieneArchivo(notificacion)
  }
  
  // MEJORADO: Marcar como leída inmediatamente al abrir el modal
  if (!notificacion.leida) {
    console.log(`📖 Abriendo notificación ${notificacion.id} - marcando como leída inmediatamente`)
    marcarComoLeidaRemoto(notificacion.id)
  }
}

const cerrarDetalleNotificacion = () => {
  notificacionSeleccionada.value = null
}

// NUEVA FUNCIÓN: Marcar como leída en el servidor con actualización inmediata del badge
const marcarComoLeidaRemoto = async (notificacionId) => {
  const usuarioId = obtenerUsuarioId()
  if (!usuarioId) return
  
  try {
    console.log(`📖 Marcando notificación ${notificacionId} como leída...`)
    
    // Actualizar estado local inmediatamente (UI optimista)
    const notificacion = notificaciones.value.find(n => n.id === notificacionId)
    if (notificacion && !notificacion.leida) {
      notificacion.leida = true
      
      // Decrementar conteo local inmediatamente
      if (conteoNoLeidas.value > 0) {
        conteoNoLeidas.value--
      }
      
      console.log(`🔄 Estado local actualizado: ${conteoNoLeidas.value} no leídas`)
    }
    
    // Usar el composable para marcar como leída y actualizar badge global inmediatamente
    const success = await markAsRead(notificacionId)
    
    if (success) {
      console.log(`✅ Notificación ${notificacionId} marcada como leída y badge actualizado`)
      
      // Si estamos en filtro de solo no leídas, remover la notificación de la vista
      if (soloNoLeidas.value && notificacion) {
        const index = notificaciones.value.findIndex(n => n.id === notificacionId)
        if (index !== -1) {
          notificaciones.value.splice(index, 1)
          totalNotificaciones.value = Math.max(0, totalNotificaciones.value - 1)
        }
      }
      
      // Forzar actualización del conteo local
      await obtenerConteoNoLeidas(usuarioId)
      
    } else {
      // Revertir estado local si falló
      if (notificacion) {
        notificacion.leida = false
        conteoNoLeidas.value++
      }
      console.error('❌ Error marcando como leída - revirtiendo estado local')
    }
    
  } catch (error) {
    console.error('Error marcando como leída:', error)
    
    // Revertir estado local en caso de error
    const notificacion = notificaciones.value.find(n => n.id === notificacionId)
    if (notificacion) {
      notificacion.leida = false
      conteoNoLeidas.value++
    }
  }
}

// MANTENER COMPATIBILIDAD: Función legacy para el sistema local
const marcarComoLeida = (notificacionId) => {
  if (!notificacionesLeidas.value.has(notificacionId)) {
    notificacionesLeidas.value.add(notificacionId)
    guardarNotificacionesLeidas()
  }
}

const esNotificacionLeida = (notificacionId) => {
  // Primero verificar en el estado de la notificación (desde servidor)
  const notificacion = notificaciones.value.find(n => n.id === notificacionId)
  if (notificacion && notificacion.hasOwnProperty('leida')) {
    return notificacion.leida
  }
  
  // Fallback al sistema local
  return notificacionesLeidas.value.has(notificacionId)
}

const guardarNotificacionesLeidas = () => {
  const usuarioId = obtenerUsuarioId()
  if (usuarioId) {
    const key = `notificacionesLeidas_${usuarioId}`
    const leidasArray = Array.from(notificacionesLeidas.value)
    localStorage.setItem(key, JSON.stringify(leidasArray))
  }
}

const cargarNotificacionesLeidas = () => {
  const usuarioId = obtenerUsuarioId()
  if (usuarioId) {
    const key = `notificacionesLeidas_${usuarioId}`
    const leidasGuardadas = localStorage.getItem(key)
    if (leidasGuardadas) {
      try {
        const leidasArray = JSON.parse(leidasGuardadas)
        notificacionesLeidas.value = new Set(leidasArray)
      } catch (e) {
        console.error('Error cargando notificaciones leídas:', e)
        notificacionesLeidas.value = new Set()
      }
    }
  }
}

const abrirArchivo = (notificacionId) => {
  const url = notificacionesService.obtenerUrlArchivo(notificacionId)
  window.open(url, '_blank')
}

const obtenerUrlArchivo = (notificacionId) => {
  return notificacionesService.obtenerUrlArchivo(notificacionId)
}

const obtenerIconoArchivo = (tipoArchivo) => {
  return notificacionesService.obtenerIconoArchivo(tipoArchivo)
}

const esImagen = (tipoArchivo) => {
  if (!tipoArchivo) return false
  const tiposImagen = ['imagen', 'image', 'jpg', 'jpeg', 'png', 'gif', 'webp', 'svg']
  return tiposImagen.some(tipo => tipoArchivo.toLowerCase().includes(tipo))
}

const esVideo = (tipoArchivo) => {
  if (!tipoArchivo) return false
  const tiposVideo = ['video', 'mp4', 'webm', 'ogg', 'avi', 'mov']
  return tiposVideo.some(tipo => tipoArchivo.toLowerCase().includes(tipo))
}

const onImageLoad = (event) => {
  // Ocultar el placeholder de carga cuando la imagen se haya cargado
  const placeholder = event.target.parentNode.querySelector('.image-placeholder')
  if (placeholder) {
    placeholder.style.display = 'none'
  }
}

const onImageError = (event) => {
  console.warn('Error cargando imagen:', event.target.src)
  
  // Ocultar el placeholder de carga
  const placeholder = event.target.parentNode.querySelector('.image-placeholder')
  if (placeholder) {
    placeholder.style.display = 'none'
  }
  
  // Crear elemento de reemplazo con mejor diseño
  const parent = event.target.parentNode
  const errorDiv = document.createElement('div')
  errorDiv.className = 'flex flex-col items-center justify-center w-full h-full bg-gray-100 rounded text-xs text-gray-500 p-4 absolute inset-0 z-20'
  
  errorDiv.innerHTML = `
    <div class="text-2xl mb-2">🖼️</div>
    <div class="text-center">
      <div class="font-medium">Error cargando imagen</div>
      <div class="text-xs text-gray-400 mt-1">Archivo no disponible</div>
    </div>
  `
  
  // Ocultar imagen original y mostrar error
  event.target.style.display = 'none'
  parent.appendChild(errorDiv)
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
  // Cargar configuración de filtro no leídas
  const savedSoloNoLeidas = localStorage.getItem('soloNoLeidas')
  if (savedSoloNoLeidas !== null) {
    soloNoLeidas.value = savedSoloNoLeidas === 'true'
  }
  
  // Cargar notificaciones leídas (sistema legacy - mantener compatibilidad)
  cargarNotificacionesLeidas()
}

// Ciclo de vida ACTUALIZADO
onMounted(async () => {
  console.log('📱 Componente Notificaciones montado')
  
  cargarConfiguracion()
  
  // Cargar notificaciones inicial
  await cargarNotificaciones()
  
  // Auto-actualizar cada segundo para respuesta inmediata y silenciosa
  autoUpdateInterval = setInterval(async () => {
    if (!cargando.value && !cargandoMas.value) {
      // Actualización silenciosa - sin log constante
      const usuarioId = obtenerUsuarioId()
      if (usuarioId) {
        await fetchUnreadCount(usuarioId)
        await obtenerConteoNoLeidas(usuarioId)
      }
      
      // Solo recargar lista si está en vista de no leídas y hay cambios
      if (soloNoLeidas.value && conteoNoLeidas.value > 0) {
        await cargarNotificaciones()
      }
    }
  }, 1000) // 1 segundo para actualización inmediata
})

onBeforeUnmount(() => {
  if (autoUpdateInterval) {
    clearInterval(autoUpdateInterval)
  }
})

// Manejadores para eventos de push notifications
const onPushSubscribed = () => {
  console.log('✅ Usuario suscrito a notificaciones push')
  // Aquí podrías mostrar un toast de confirmación
}

const onPushUnsubscribed = () => {
  console.log('🔕 Usuario desuscrito de notificaciones push')
  // Aquí podrías mostrar un toast de confirmación
}

const onPushError = (error) => {
  console.error('❌ Error en notificaciones push:', error)
  // Aquí podrías mostrar un toast de error
}
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

/* Clase de texto extra pequeño para mejor responsividad */
.text-2xs {
  font-size: 0.65rem;
  line-height: 0.9rem;
}

/* Asegurar que no interfiera con el título */
.glass-card {
  position: relative;
  min-height: 45px;
}

/* Botón de refresh con efecto glassmorphism */
.glass-card button {
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  transition: background-color 0.2s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.2s ease;
}

.glass-card button:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.2) !important;
}

.glass-card button:active:not(:disabled) {
  background: rgba(255, 255, 255, 0.15) !important;
}

/* Responsividad para el botón de refresh */
@media (max-width: 480px) {
  .glass-card button {
    padding: 0.375rem;
    right: 0.5rem !important;
  }
  
  .glass-card button svg {
    width: 1rem;
    height: 1rem;
  }
}

@media (max-width: 375px) {
  .glass-card button {
    padding: 0.3rem;
    right: 0.375rem !important;
  }
  
  .glass-card button svg {
    width: 0.9rem;
    height: 0.9rem;
  }
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
  padding: 0.6rem;
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
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  /* Eliminado backdrop-filter para hacer las notificaciones sólidas */
}

.notification-item:hover {
  transform: translateY(-2px) scale(1.02);
}

/* Círculos de notificación con efecto mejorado */
.notification-item .bg-red-600 {
  background: linear-gradient(135deg, #dc2626, #ef4444, #dc2626) !important;
  box-shadow: 
    0 4px 12px rgba(220, 38, 38, 0.4),
    0 2px 6px rgba(220, 38, 38, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: pulse-red-circle 2s ease-in-out infinite;
}

.notification-item .bg-green-600 {
  background: linear-gradient(135deg, #16a34a, #22c55e, #16a34a) !important;
  box-shadow: 
    0 4px 12px rgba(34, 197, 94, 0.4),
    0 2px 6px rgba(34, 197, 94, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Animación sutil para círculo rojo (no leído) */
@keyframes pulse-red-circle {
  0%, 100% {
    transform: scale(1);
    box-shadow: 
      0 4px 12px rgba(220, 38, 38, 0.4),
      0 2px 6px rgba(220, 38, 38, 0.3),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 
      0 6px 16px rgba(220, 38, 38, 0.5),
      0 3px 8px rgba(220, 38, 38, 0.4),
      inset 0 1px 0 rgba(255, 255, 255, 0.25);
  }
}

/* Efecto hover para los círculos */
.notification-item:hover .bg-red-600 {
  transform: scale(1.1);
  box-shadow: 
    0 6px 16px rgba(220, 38, 38, 0.6),
    0 3px 8px rgba(220, 38, 38, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
}

.notification-item:hover .bg-green-600 {
  transform: scale(1.1);
  box-shadow: 
    0 6px 16px rgba(34, 197, 94, 0.6),
    0 3px 8px rgba(34, 197, 94, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
}

/* Notificaciones no leídas - Fondo rojo sólido */
.notification-item.bg-red-50 {
  background-color: #fef2f2 !important;
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.1),
    0 1px 2px rgba(0, 0, 0, 0.05);
  border-color: #f87171;
}

.notification-item.bg-red-50:hover {
  background-color: #fee2e2 !important;
  border-color: #ef4444 !important;
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.15),
    0 2px 4px rgba(0, 0, 0, 0.08);
}

/* Notificaciones leídas - Fondo blanco sólido */
.notification-item.bg-white {
  background-color: #ffffff !important;
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.1),
    0 1px 2px rgba(0, 0, 0, 0.05);
  border-color: #d1d5db;
}

.notification-item.bg-white:hover {
  background-color: #f9fafb !important;
  border-color: #9ca3af !important;
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.15),
    0 2px 4px rgba(0, 0, 0, 0.08);
}

/* Campanita animada */
.bell-container {
  animation: bell-shake 0.8s ease-in-out infinite;
  box-shadow: 
    0 2px 6px rgba(0, 0, 0, 0.15),
    0 1px 3px rgba(0, 0, 0, 0.08);
  border: 2px solid rgba(255, 255, 255, 0.9);
}

.bell-icon {
  animation: bell-ring 1.2s ease-in-out infinite;
  transform-origin: top center;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

@keyframes bell-shake {
  0%, 100% {
    transform: translateX(0) rotate(0deg);
  }
  25% {
    transform: translateX(-1px) rotate(-2deg);
  }
  50% {
    transform: translateX(1px) rotate(2deg);
  }
  75% {
    transform: translateX(-0.5px) rotate(-1deg);
  }
}

@keyframes bell-ring {
  0%, 100% {
    transform: rotate(0deg);
  }
  10%, 30%, 50%, 70%, 90% {
    transform: rotate(-8deg);
  }
  20%, 40%, 60%, 80% {
    transform: rotate(8deg);
  }
}

/* Badge de nueva notificación - Ahora sin uso pero mantengo por compatibilidad */
.notification-badge {
  animation: pulse-green 2s ease-in-out infinite;
  box-shadow: 0 0 8px rgba(34, 197, 94, 0.5);
}

@keyframes pulse-green {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
    box-shadow: 0 0 8px rgba(34, 197, 94, 0.5);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
    box-shadow: 0 0 12px rgba(34, 197, 94, 0.8);
  }
}

/* Limitador de líneas */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Mejoras de responsividad para pantallas móviles */
@media (max-width: 480px) {
  .page-container {
    padding-left: 0.25rem;
    padding-right: 0.25rem;
    padding-top: 0.25rem;
    padding-bottom: 0.25rem;
    max-width: calc(100vw - 0.5rem);
  }
  
  .glass-card {
    padding: 0.5rem;
    margin-bottom: 0.25rem;
    border-radius: 12px;
  }
  
  .notifications-scroll-container {
    padding-left: 0.25rem !important;
    padding-right: 0.25rem !important;
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
  
  .space-y-2 > * + * {
    margin-top: 0.375rem;
  }
}

@media (max-width: 375px) {
  .page-container {
    padding-left: 0.125rem;
    padding-right: 0.125rem;
    max-width: calc(100vw - 0.25rem);
  }
  
  .glass-card {
    padding: 0.375rem;
    margin-bottom: 0.125rem;
    border-radius: 10px;
  }
  
  .notifications-scroll-container {
    padding-left: 0.125rem !important;
    padding-right: 0.125rem !important;
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
  
  .space-y-2 > * + * {
    margin-top: 0.25rem;
  }
}

/* Para pantallas grandes */
@media (min-width: 768px) {
  .page-container {
    max-width: 450px;
    padding: 0.75rem;
  }
  
  .glass-card {
    padding: 1rem;
    margin-bottom: 0.75rem;
  }
}

@media (min-width: 1024px) {
  .page-container {
    max-width: 500px;
    padding: 1rem;
  }
}

/* Soporte adicional para navegadores que no soportan backdrop-filter */
@supports not (backdrop-filter: blur(20px)) {
  .glass-card {
    background: rgba(255, 255, 255, 0.85);
  }
}

/* Contenedor de scroll de notificaciones */
.notifications-scroll-container {
  scrollbar-width: thin;
  scrollbar-color: rgba(34, 197, 94, 0.3) transparent;
}

.notifications-scroll-container::-webkit-scrollbar {
  width: 4px;
}

.notifications-scroll-container::-webkit-scrollbar-track {
  background: transparent;
}

.notifications-scroll-container::-webkit-scrollbar-thumb {
  background-color: rgba(34, 197, 94, 0.3);
  border-radius: 2px;
}

.notifications-scroll-container::-webkit-scrollbar-thumb:hover {
  background-color: rgba(34, 197, 94, 0.5);
}

/* Estilos para vista previa de archivos */
.aspect-square {
  aspect-ratio: 1 / 1;
}

.aspect-video {
  aspect-ratio: 16 / 9;
}

/* Centrado perfecto para contenido multimedia */
.media-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.media-content {
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 100%;
}

/* Efectos hover para imágenes */
.notification-item img {
  transition: all 0.3s ease;
}

.notification-item:hover img {
  transform: scale(1.02);
}

/* Estilos para videos */
video {
  outline: none;
}

video::-webkit-media-controls {
  outline: none;
}

/* Loading placeholder para imágenes */
.image-placeholder {
  background: linear-gradient(-90deg, #f0f0f0 0%, #e0e0e0 50%, #f0f0f0 100%);
  background-size: 400% 400%;
  animation: loading-shimmer 1.5s ease-in-out infinite;
}

@keyframes loading-shimmer {
  0% { background-position: 0% 0%; }
  100% { background-position: -200% 0%; }
}

/* Mejoras para archivos de error */
.file-error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px dashed rgba(239, 68, 68, 0.3);
  color: rgb(127, 29, 29);
}

/* Estilos responsivos para archivos multimedia */
@media (max-width: 480px) {
  .aspect-square,
  .aspect-video {
    max-width: 160px;
    margin: 0 auto;
  }
  
  video,
  img {
    max-height: 160px;
  }
  
  .media-container {
    justify-content: center;
  }
}

@media (max-width: 375px) {
  .aspect-square,
  .aspect-video {
    max-width: 140px;
    margin: 0 auto;
  }
  
  video,
  img {
    max-height: 140px;
  }
  
  .media-container {
    justify-content: center;
  }
}

/* Centrado perfecto para contenido multimedia */
.notification-item .aspect-square,
.notification-item .aspect-video {
  margin: 0 auto;
}

/* Centrado para elementos de notificación */
.notification-media-center {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  margin: 0.5rem 0;
}

/* Asegurar que las imágenes y videos estén siempre centrados */
.center-content {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.center-content > * {
  margin: 0 auto;
}

/* Botón profesional empresarial */
.professional-button {
  background: transparent;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 1px 3px rgba(0, 0, 0, 0.1),
    0 1px 2px rgba(0, 0, 0, 0.06);
}

.professional-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(34, 197, 94, 0.08),
    transparent
  );
  transition: all 0.6s ease;
}

.professional-button:hover::before {
  left: 100%;
}

.professional-button:hover {
  background: rgba(34, 197, 94, 0.02);
  box-shadow: 
    0 4px 12px rgba(34, 197, 94, 0.15),
    0 2px 4px rgba(34, 197, 94, 0.1);
  transform: translateY(-1px);
}

.professional-button:active {
  transform: translateY(0);
  box-shadow: 
    0 2px 6px rgba(34, 197, 94, 0.2),
    0 1px 2px rgba(34, 197, 94, 0.1);
}

.professional-button:focus {
  border-color: #22c55e;
  box-shadow: 
    0 0 0 2px rgba(34, 197, 94, 0.2),
    0 2px 4px rgba(0, 0, 0, 0.05);
}

/* Responsividad para el botón profesional */
@media (max-width: 480px) {
  .professional-button {
    padding: 0.375rem 0.75rem !important;
    font-size: 0.625rem !important;
    margin: 0 auto !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    max-width: fit-content !important;
    border-radius: 0.375rem !important;
  }
  
  .professional-button svg {
    width: 0.625rem !important;
    height: 0.625rem !important;
  }
  
  .professional-button span {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 0.25rem !important;
  }
}

@media (max-width: 375px) {
  .professional-button {
    padding: 0.3rem 0.6rem !important;
    font-size: 0.55rem !important;
    margin: 0 auto !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    max-width: fit-content !important;
    border-radius: 0.3rem !important;
  }
  
  .professional-button svg {
    width: 0.55rem !important;
    height: 0.55rem !important;
  }
  
  .professional-button span {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 0.2rem !important;
  }
}

.ver-mas-btn {
  background: linear-gradient(45deg, #16a34a, #22c55e);
  box-shadow: 0 2px 4px rgba(34, 197, 94, 0.3);
  transition: all 0.2s ease;
}

.ver-mas-btn:hover {
  background: linear-gradient(45deg, #15803d, #16a34a);
  box-shadow: 0 4px 8px rgba(34, 197, 94, 0.4);
  transform: translateY(-1px);
}
</style>
