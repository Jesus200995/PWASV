<template>
  <div class="fixed inset-0 bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 overflow-hidden" style="z-index: 0;">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-indigo-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>

    <div class="absolute inset-0 overflow-hidden" style="z-index: 1;">
      <!-- Header fijo de manuales -->
      <div class="fixed top-16 sm:top-20 left-0 right-0 z-20 px-2 sm:px-3 lg:px-4 pt-2 sm:pt-3">
        <div class="w-full max-w-md mx-auto">
          <div class="glass-card mb-0 relative">
            <div class="text-center mb-1 relative py-0.5">
              <h1 class="text-base font-medium tracking-wide text-indigo-700" style="font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif; letter-spacing: 0.025em;">
                Mis Manuales
              </h1>
              <!-- Botón de refresh -->
              <button 
                @click="refrescarManuales"
                :disabled="cargando"
                class="absolute top-1/2 right-3 transform -translate-y-1/2 p-2 rounded-full hover:bg-white hover:bg-opacity-20 transition-colors duration-200 group"
                :class="{ 'cursor-not-allowed opacity-50': cargando }"
                title="Actualizar manuales"
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
          
          <!-- Título de manuales fijo -->
          <div class="bg-transparent rounded-xl p-1">
            <h2 class="text-sm font-medium text-indigo-500/70 mb-1 flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
              </svg>
              Documentos y Guías
              <span v-if="manuales.length > 0" class="ml-auto text-xs bg-indigo-100 text-indigo-800 px-2 py-1 rounded-full">
                {{ manuales.length }}
              </span>
            </h2>
            <div class="indigo-line mb-0"></div>
          </div>
        </div>
      </div>

      <!-- Contenido con scroll -->
      <div class="absolute inset-0 overflow-hidden pt-40 sm:pt-44 pb-2">
        <div class="page-container w-full max-w-md mx-auto relative z-10 px-2 sm:px-3 lg:px-4 py-1 h-full">

        <!-- Estado de carga -->
        <div v-if="cargando" class="glass-card mb-2">
          <div class="flex items-center justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500"></div>
            <span class="ml-3 text-gray-600 text-sm">Cargando manuales...</span>
          </div>
        </div>

        <!-- Error de conexión -->
        <div v-if="error && !cargando" class="glass-card mb-2">
          <div class="text-center py-6">
            <div class="text-4xl mb-3">⚠️</div>
            <h3 class="text-sm font-medium text-gray-800 mb-2">Error de Conexión</h3>
            <p class="text-xs text-gray-600 mb-4">{{ error }}</p>
            <button 
              @click="cargarManuales"
              class="px-4 py-2 bg-indigo-500 text-white text-xs rounded-lg hover:bg-indigo-600 transition-colors"
            >
              Reintentar
            </button>
          </div>
        </div>

        <!-- Contenedor de scroll para manuales -->
        <div v-if="!cargando && !error" class="h-full flex flex-col">
          <!-- Lista de manuales con scroll propio -->
          <div class="flex-1 overflow-y-auto bg-transparent rounded-xl px-2 py-4 manuales-scroll-container">
            <div v-if="manuales.length > 0" class="space-y-3">
              
            <!-- Card de cada manual -->
            <div v-for="(manual, index) in manuales" 
                 :key="manual.id"
                 class="relative manual-container">
              
              <!-- Badge de no leído -->
              <div v-if="!manual.leido" class="absolute -top-1 -right-1 z-50">
                <div class="manual-badge bg-rose-500 rounded-full w-6 h-6 flex items-center justify-center shadow-lg border-2 border-white animate-pulse">
                  <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z"/>
                  </svg>
                </div>
              </div>

              <!-- Card del manual -->
              <div :class="[
                'manual-card group cursor-pointer transition-all duration-300 ease-out rounded-2xl overflow-hidden',
                manual.leido 
                  ? 'manual-read' 
                  : 'manual-unread'
              ]"
              @click="abrirManual(manual)"
              >
                <!-- Imagen de portada si existe -->
                <div v-if="manual.imagen_nombre" class="manual-image-container">
                  <img 
                    :src="getImagenUrl(manual.id)" 
                    :alt="manual.titulo"
                    class="manual-image"
                    @error="handleImageError($event)"
                  />
                  <div class="manual-image-overlay"></div>
                </div>
                
                <!-- Contenido del manual -->
                <div class="manual-content p-4">
                  <!-- Header -->
                  <div class="flex items-start gap-3">
                    <!-- Icono del tipo -->
                    <div :class="[
                      'flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center transition-all duration-300 group-hover:scale-110',
                      manual.leido 
                        ? 'bg-gradient-to-br from-indigo-50 to-indigo-100 text-indigo-600' 
                        : 'bg-gradient-to-br from-indigo-400 to-purple-500 text-white shadow-lg'
                    ]">
                      <svg v-if="manual.archivo_nombre" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                      </svg>
                      <svg v-else-if="manual.enlace_url" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/>
                      </svg>
                      <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                      </svg>
                    </div>
                    
                    <!-- Título y subtítulo -->
                    <div class="flex-1 min-w-0">
                      <h3 :class="[
                        'text-base font-semibold leading-tight mb-1 transition-colors duration-200',
                        manual.leido ? 'text-gray-700' : 'text-indigo-800'
                      ]">
                        {{ manual.titulo }}
                      </h3>
                      <p v-if="manual.subtitulo" :class="[
                        'text-xs font-medium mb-2 line-clamp-1',
                        manual.leido ? 'text-gray-500' : 'text-indigo-600'
                      ]">
                        {{ manual.subtitulo }}
                      </p>
                    </div>
                  </div>
                  
                  <!-- Descripción -->
                  <p v-if="manual.descripcion" :class="[
                    'text-xs mt-2 line-clamp-2',
                    manual.leido ? 'text-gray-500' : 'text-gray-600'
                  ]">
                    {{ manual.descripcion }}
                  </p>
                  
                  <!-- Badges y fecha -->
                  <div class="flex items-center justify-between mt-3 pt-2 border-t border-gray-100">
                    <div class="flex gap-1.5">
                      <span v-if="manual.archivo_nombre" class="manual-badge-small badge-pdf">
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                        </svg>
                        PDF
                      </span>
                      <span v-if="manual.enlace_url" class="manual-badge-small badge-url">
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                        </svg>
                        URL
                      </span>
                    </div>
                    <span class="text-xs text-gray-400">
                      {{ formatearFecha(manual.fecha_creacion) }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            </div>

            <!-- Estado vacío -->
            <div v-else class="glass-card mb-2">
              <div class="text-center py-8">
                <div class="text-5xl mb-4">📚</div>
                <h3 class="text-sm font-medium text-gray-800 mb-2">Sin Manuales</h3>
                <p class="text-xs text-gray-600">No hay manuales disponibles para ti en este momento.</p>
              </div>
            </div>
          </div>
        </div>
        </div>
      </div>
    </div>

    <!-- Modal de Detalle del Manual -->
    <Teleport to="body">
      <transition name="modal-fade">
        <div v-if="modalAbierto" class="fixed inset-0 z-50 flex items-center justify-center p-4">
          <!-- Overlay -->
          <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="cerrarModal"></div>
          
          <!-- Modal Content -->
          <div class="relative w-full max-w-lg bg-white rounded-3xl shadow-2xl overflow-hidden transform transition-all max-h-[90vh] flex flex-col">
            <!-- Header con imagen -->
            <div class="relative">
              <div v-if="manualSeleccionado?.imagen_nombre" class="modal-header-image">
                <img 
                  :src="getImagenUrl(manualSeleccionado.id)" 
                  :alt="manualSeleccionado.titulo"
                  class="w-full h-40 object-cover"
                />
                <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
              </div>
              <div :class="[
                'modal-header-content',
                manualSeleccionado?.imagen_nombre ? 'absolute bottom-0 left-0 right-0 p-4 text-white' : 'bg-gradient-to-r from-indigo-500 to-purple-600 p-4 text-white'
              ]">
                <h2 class="text-xl font-bold">{{ manualSeleccionado?.titulo }}</h2>
                <p v-if="manualSeleccionado?.subtitulo" class="text-sm opacity-90">{{ manualSeleccionado?.subtitulo }}</p>
              </div>
              
              <!-- Botón cerrar -->
              <button 
                @click="cerrarModal" 
                class="absolute top-3 right-3 w-8 h-8 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center text-white hover:bg-white/30 transition-colors"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>
            
            <!-- Body -->
            <div class="flex-1 overflow-y-auto p-4">
              <!-- Descripción -->
              <div v-if="manualSeleccionado?.descripcion" class="mb-4">
                <h3 class="text-sm font-semibold text-gray-700 mb-2">Descripción</h3>
                <p class="text-sm text-gray-600 leading-relaxed">{{ manualSeleccionado.descripcion }}</p>
              </div>
              
              <!-- Información -->
              <div class="bg-gray-50 rounded-xl p-3 space-y-2">
                <div class="flex items-center justify-between text-sm">
                  <span class="text-gray-500">Fecha de publicación</span>
                  <span class="text-gray-700 font-medium">{{ formatearFecha(manualSeleccionado?.fecha_creacion) }}</span>
                </div>
                <div v-if="manualSeleccionado?.leido" class="flex items-center justify-between text-sm">
                  <span class="text-gray-500">Leído el</span>
                  <span class="text-green-600 font-medium">{{ formatearFecha(manualSeleccionado?.fecha_lectura) }}</span>
                </div>
              </div>
            </div>
            
            <!-- Footer con acciones -->
            <div class="p-4 border-t border-gray-100 bg-gray-50 space-y-2">
              <!-- Abrir archivo -->
              <a 
                v-if="manualSeleccionado?.archivo_nombre"
                :href="getArchivoUrl(manualSeleccionado.id)"
                target="_blank"
                class="w-full flex items-center justify-center gap-2 py-3 px-4 bg-gradient-to-r from-rose-500 to-pink-500 text-white rounded-xl font-medium hover:from-rose-600 hover:to-pink-600 transition-all shadow-lg"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                Abrir Documento
              </a>
              
              <!-- Abrir enlace -->
              <a 
                v-if="manualSeleccionado?.enlace_url"
                :href="manualSeleccionado.enlace_url"
                target="_blank"
                class="w-full flex items-center justify-center gap-2 py-3 px-4 bg-gradient-to-r from-indigo-500 to-blue-500 text-white rounded-xl font-medium hover:from-indigo-600 hover:to-blue-600 transition-all shadow-lg"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                </svg>
                Abrir Enlace
              </a>
              
              <!-- Botón cerrar -->
              <button 
                @click="cerrarModal"
                class="w-full py-2.5 px-4 text-gray-600 font-medium rounded-xl hover:bg-gray-100 transition-colors"
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { manualesService } from '@/services/manualesService'

// Estado
const cargando = ref(false)
const error = ref(null)
const manuales = ref([])
const modalAbierto = ref(false)
const manualSeleccionado = ref(null)

// Usuario actual
const usuarioId = computed(() => {
  const userData = localStorage.getItem('user_data')
  if (userData) {
    const user = JSON.parse(userData)
    return user.id || user.usuario_id
  }
  return null
})

// Cargar manuales
const cargarManuales = async () => {
  if (!usuarioId.value) {
    error.value = 'No se encontró información del usuario'
    return
  }
  
  cargando.value = true
  error.value = null
  
  try {
    const response = await manualesService.obtenerManualesUsuario(usuarioId.value)
    manuales.value = response.manuales || []
  } catch (err) {
    console.error('Error cargando manuales:', err)
    error.value = err.message || 'Error al cargar manuales'
  } finally {
    cargando.value = false
  }
}

// Refrescar manuales
const refrescarManuales = () => {
  cargarManuales()
}

// Abrir manual y marcarlo como leído
const abrirManual = async (manual) => {
  manualSeleccionado.value = manual
  modalAbierto.value = true
  
  // Marcar como leído si no lo está
  if (!manual.leido && usuarioId.value) {
    await manualesService.marcarComoLeido(manual.id, usuarioId.value)
    // Actualizar el estado local
    manual.leido = true
    manual.fecha_lectura = new Date().toISOString()
  }
}

// Cerrar modal
const cerrarModal = () => {
  modalAbierto.value = false
  manualSeleccionado.value = null
}

// Obtener URL de imagen
const getImagenUrl = (manualId) => {
  return manualesService.getImagenUrl(manualId)
}

// Obtener URL de archivo
const getArchivoUrl = (manualId) => {
  return manualesService.getArchivoUrl(manualId)
}

// Manejar error de imagen
const handleImageError = (event) => {
  event.target.style.display = 'none'
}

// Formatear fecha
const formatearFecha = (fecha) => {
  if (!fecha) return '—'
  const d = new Date(fecha)
  return d.toLocaleDateString('es-MX', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

// Cargar al montar
onMounted(() => {
  cargarManuales()
})
</script>

<style scoped>
/* Animación pulse slow */
@keyframes pulse-slow {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.05); }
}

.animate-pulse-slow {
  animation: pulse-slow 6s ease-in-out infinite;
}

/* Glass card */
.glass-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  padding: 12px 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Línea decorativa indigo */
.indigo-line {
  height: 2px;
  background: linear-gradient(to right, #6366f1, #8b5cf6, transparent);
  border-radius: 9999px;
}

/* Contenedor de scroll */
.manuales-scroll-container {
  scrollbar-width: thin;
  scrollbar-color: rgba(99, 102, 241, 0.3) transparent;
}

.manuales-scroll-container::-webkit-scrollbar {
  width: 4px;
}

.manuales-scroll-container::-webkit-scrollbar-track {
  background: transparent;
}

.manuales-scroll-container::-webkit-scrollbar-thumb {
  background: rgba(99, 102, 241, 0.3);
  border-radius: 9999px;
}

/* Cards de manuales */
.manual-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.manual-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

.manual-unread {
  border-left: 4px solid #6366f1;
  background: linear-gradient(135deg, rgba(238, 242, 255, 0.9), rgba(255, 255, 255, 0.9));
}

.manual-read {
  border-left: 4px solid #10b981;
  opacity: 0.85;
}

/* Imagen del manual */
.manual-image-container {
  position: relative;
  height: 120px;
  overflow: hidden;
}

.manual-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.manual-card:hover .manual-image {
  transform: scale(1.05);
}

.manual-image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.3), transparent);
}

/* Badges pequeños */
.manual-badge-small {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  border-radius: 9999px;
  font-size: 10px;
  font-weight: 600;
}

.badge-pdf {
  background: #fef2f2;
  color: #dc2626;
}

.badge-url {
  background: #eff6ff;
  color: #2563eb;
}

/* Modal transitions */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-active .relative,
.modal-fade-leave-active .relative {
  transition: transform 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-from .relative {
  transform: scale(0.95) translateY(20px);
}

.modal-fade-leave-to .relative {
  transform: scale(0.95) translateY(20px);
}

/* Responsive */
@media (max-width: 640px) {
  .manual-image-container {
    height: 100px;
  }
}
</style>
