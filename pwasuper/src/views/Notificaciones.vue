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
              <h1 class="text-base font-medium tracking-wide text-emerald-700" style="font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif; letter-spacing: 0.025em;">
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
          
          <!-- Título de notificaciones fijo -->
          <div class="bg-transparent rounded-xl p-1">
            <h2 class="text-sm font-medium text-emerald-500/70 mb-1 flex items-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" />
              </svg>
              Total de Avisos
              <span v-if="notificacionesFiltradas.length > 0" class="ml-auto text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                {{ notificacionesFiltradas.length }}
              </span>
            </h2>
            <div class="green-line mb-0"></div>
          </div>
        </div>
      </div>

      <!-- Contenido con scroll -->
      <div class="absolute inset-0 overflow-hidden pt-40 sm:pt-44 pb-2">
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
            <div v-if="notificacionesFiltradas.length > 0" class="space-y-1">
            <!-- Contenedor relativo para cada notificación con campanita fuera -->
            <div v-for="(notificacion, index) in notificacionesFiltradas" 
                 :key="notificacion.id"
                 class="relative notification-container">
              
              <!-- Campanita vibrante FUERA de la notificación -->
              <div v-if="!notificacion.leida" class="absolute top-0 right-0 z-50">
                <div class="notification-bell bg-red-600 rounded-full w-6 h-6 flex items-center justify-center shadow-lg border-2 border-white">
                  <svg class="bell-icon w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z"/>
                  </svg>
                </div>
              </div>

              <!-- Card de notificación -->
              <div :class="[
                'enterprise-notification-card group cursor-pointer transition-all duration-300 ease-out rounded-2xl',
                notificacion.leida 
                  ? 'notification-read border-l-green-500' 
                  : 'notification-unread border-l-rose-700'
              ]"
              @click="abrirDetalleNotificacion(notificacion)"
              >
                <!-- Indicador lateral -->
                <div :class="[
                  'absolute left-0 top-0 h-full w-1 transition-all duration-300',
                  notificacion.leida ? 'bg-green-500' : 'bg-gradient-to-b from-white/70 via-rose-500 to-white/70'
                ]"></div>
                
                <div class="flex items-start gap-2.5 px-3 py-4">
                <!-- Avatar/Icono empresarial más pequeño -->
                <div class="flex-shrink-0 mt-2">
                  <div :class="[
                    'w-8 h-8 rounded-lg flex items-center justify-center shadow-sm border transition-all duration-300 group-hover:scale-105',
                    notificacion.leida 
                      ? 'bg-gradient-to-br from-green-50 to-green-100 border-green-200 text-green-600' 
                      : 'bg-gradient-to-br from-white/80 to-rose-400 border-white/40 text-rose-800 shadow-lg'
                  ]">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                    </svg>
                  </div>
                </div>
                
                <!-- Contenido principal -->
                <div class="flex-1 min-w-0">
                  <!-- Header con título y fecha -->
                  <div class="flex items-start justify-between mb-2">
                    <div class="flex-1 min-w-0 pr-3">
                      <h3 :class="[
                        'text-sm font-semibold leading-tight mb-1 transition-colors duration-200 line-clamp-1',
                        notificacion.leida ? 'text-gray-700 group-hover:text-gray-900' : 'text-white font-bold'
                      ]">
                        {{ notificacion.titulo }}
                      </h3>
                      <p v-if="notificacion.subtitulo" :class="[
                        'notification-subtitle text-xs font-medium transition-colors duration-200 line-clamp-1',
                        notificacion.leida ? 'text-gray-500' : 'text-white/90'
                      ]">
                        {{ notificacion.subtitulo }}
                      </p>
                    </div>
                    <div class="flex flex-col items-end flex-shrink-0">
                      <span :class="[
                        'notification-date text-xs font-medium transition-colors duration-200',
                        notificacion.leida ? 'text-gray-400' : 'text-white/85'
                      ]">
                        {{ formatearFecha(notificacion.fecha_creacion) }}
                      </span>
                      <div :class="[
                        'text-xs px-2 py-0.5 rounded-full mt-1 font-medium transition-all duration-200',
                        notificacion.leida 
                          ? 'bg-green-100 text-green-700 border border-green-200' 
                          : 'bg-gradient-to-r from-white/80 to-rose-400 text-rose-900 border border-white/50 shadow-md font-bold'
                      ]">
                        {{ notificacion.leida ? 'Leída' : 'Nueva' }}
                      </div>
                    </div>
                  </div>
                  
                  <!-- Descripción truncada - solo si hay descripción -->
                  <div v-if="notificacion.descripcion && notificacion.descripcion.trim()" class="mb-3">
                    <p :class="[
                      'text-xs leading-relaxed transition-colors duration-200 line-clamp-2',
                      notificacion.leida ? 'text-gray-600' : 'text-white/95'
                    ]">
                      {{ notificacion.descripcion }}
                    </p>
                  </div>

                  <!-- Vista previa de archivo compacta con efecto fade - SOLO para imágenes y videos -->
                  <div v-if="notificacion.tiene_archivo && (esImagen(notificacion.archivo_tipo) || esVideo(notificacion.archivo_tipo))" class="mb-3">
                    <div v-if="esImagen(notificacion.archivo_tipo)" class="notification-media-preview notification-has-media aspect-video max-w-xs bg-white overflow-hidden cursor-pointer" @click.stop="verNotificacionCompleta(notificacion)" style="box-shadow: none !important; border: none !important;">
                      <div class="absolute inset-0 flex items-center justify-center bg-gray-50 image-placeholder z-5">
                        <div class="text-gray-400 text-center">
                          <div class="text-lg mb-1">🖼️</div>
                          <div class="text-xs font-medium">Cargando...</div>
                        </div>
                      </div>
                      <img 
                        :src="obtenerUrlArchivo(notificacion.id)" 
                        :alt="notificacion.archivo_nombre"
                        class="hover:scale-105 transition-transform duration-300"
                        @error="onImageError"
                        @load="onImageLoad"
                        loading="lazy"
                        decoding="async"
                        style="filter: none !important; box-shadow: none !important;"
                      />
                    </div>
                    <div v-else-if="esVideo(notificacion.archivo_tipo)" class="notification-media-preview notification-has-media aspect-video max-w-xs bg-white overflow-hidden cursor-pointer relative" @click.stop="verNotificacionCompleta(notificacion)" style="box-shadow: none !important; border: none !important;">
                      <div class="absolute inset-0 flex items-center justify-center bg-gray-50 video-placeholder z-5">
                        <div class="text-gray-400 text-center">
                          <div class="text-xs font-medium">Cargando...</div>
                        </div>
                      </div>
                      <video 
                        :src="obtenerUrlArchivo(notificacion.id)"
                        muted
                        preload="metadata"
                        style="pointer-events: none; filter: none !important; box-shadow: none !important;"
                        @loadedmetadata="onVideoLoaded"
                        @canplay="onVideoLoaded"
                        @error="onVideoError"
                        @loadstart="(event) => setTimeout(() => onVideoFallback(event), 5000)"
                      >
                        Tu navegador no soporta video.
                      </video>
                      <!-- Icono de play suave desvanecido -->
                      <div class="absolute inset-0 flex items-center justify-center pointer-events-none video-play-overlay">
                        <div class="video-play-icon">
                          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <circle cx="12" cy="12" r="12" fill="rgba(0, 0, 0, 0.25)" stroke="rgba(255, 255, 255, 0.3)" stroke-width="1"/>
                            <polygon points="10,8 16,12 10,16" fill="white" opacity="0.9"/>
                          </svg>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Indicador sutil para archivos adjuntos (PDF, Word, etc.) - SOLO visible si hay archivo que no es imagen o video -->
                  <div v-if="notificacion.tiene_archivo && !esImagen(notificacion.archivo_tipo) && !esVideo(notificacion.archivo_tipo)" class="mb-3">
                    <div class="flex items-center gap-2 text-xs text-gray-500 bg-gray-50 rounded-md px-3 py-1.5 border border-gray-200">
                      <span class="text-sm">📎</span>
                      <span class="font-medium">Archivo adjunto</span>
                      <span class="text-gray-400">•</span>
                      <span class="capitalize truncate">{{ notificacion.archivo_tipo }}</span>
                    </div>
                  </div>
                  
                  <!-- Botón Ver completo con efecto vidrio líquido - alineado a la derecha -->
                  <div class="flex justify-end">
                    <button class="liquid-glass-button group inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-gray-700 rounded-md transition-all duration-300 relative overflow-hidden ml-auto">
                      <span class="relative z-10">Ver completo</span>
                      <svg class="w-3 h-3 transition-transform duration-200 group-hover:translate-x-0.5 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
              <!-- Fin del card de notificación -->
            </div>
            <!-- Fin del contenedor de notificación -->
            </div>
            <!-- Fin del div con v-if -->
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

    <!-- Modal de detalle de notificación - Teleportado al body para difuminación correcta -->
    <teleport to="body">
      <div v-if="notificacionSeleccionada" 
           class="fixed inset-0 bg-emerald-900/30 backdrop-blur-sm flex items-center justify-center p-2 sm:p-4 z-40 transition-all duration-500 animate-fade-in-blur"
           @click="cerrarDetalleNotificacion">
        
        <!-- Contenedor del modal con botón de cerrar -->
        <div class="relative" @click.stop>
          
          <!-- Botón de cerrar (-) flotante en esquina superior derecha -->
          <button 
            @click="cerrarDetalleNotificacion"
            class="absolute -top-1 right-1 sm:-top-2 sm:right-0 w-8 h-8 sm:w-9 sm:h-9 bg-emerald-600/90 hover:bg-emerald-700 backdrop-blur-sm text-white rounded-full flex items-center justify-center shadow-xl z-50 transition-all duration-200 transform hover:scale-110 active:scale-95 border border-white/20"
            style="box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);"
            title="Cerrar notificación"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-6 sm:w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M20 12H4" />
            </svg>
          </button>
          
          <!-- Modal principal -->
          <div class="news-modal bg-white rounded-2xl w-full max-w-md sm:max-w-2xl lg:max-w-4xl h-[99vh] sm:h-[88vh] max-h-[99vh] sm:max-h-[700px] overflow-hidden shadow-2xl transform transition-all duration-500 scale-100 flex flex-col animate-modal-open">
        
        <!-- Header Profesional tipo Notificación Moderna -->
        <div class="notification-modal-header relative overflow-hidden flex-shrink-0">
          <!-- Fondo degradado elegante guinda con verde -->
          <div class="absolute inset-0 bg-gradient-to-r from-rose-800 via-pink-900 to-emerald-700"></div>
          <!-- Patrón decorativo sutil (más pequeño) -->
          <div class="absolute inset-0 opacity-10">
            <div class="absolute top-0 right-0 w-10 h-10 sm:w-16 sm:h-16 bg-white rounded-full -translate-y-1/2 translate-x-1/2"></div>
            <div class="absolute bottom-0 left-0 w-8 h-8 sm:w-12 sm:h-12 bg-white rounded-full translate-y-1/2 -translate-x-1/2"></div>
          </div>
          
          <div class="relative z-10 px-3 py-2 sm:px-4 sm:py-3">
            <!-- Barra superior con etiqueta -->
            <div class="flex items-center justify-start mb-0.5">
              <div class="flex items-center gap-1">
                <!-- Icono de notificación -->
                <div class="w-4 h-4 sm:w-5 sm:h-5 bg-white/20 backdrop-blur-sm rounded-md flex items-center justify-center">
                  <svg class="w-2.5 h-2.5 sm:w-3 sm:h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
                  </svg>
                </div>
                <div class="flex items-center gap-1 sm:gap-1.5">
                  <span class="text-[7px] sm:text-[8px] font-bold text-white/85 uppercase tracking-wider">Aviso</span>
                  <span class="text-[7px] sm:text-[8px] text-white/50">•</span>
                  <span class="text-[7px] sm:text-[8px] text-white/50">{{ formatearFecha(notificacionSeleccionada.fecha_creacion) }}</span>
                </div>
              </div>
            </div>

            <!-- Título Principal y Badge en la misma línea -->
            <div class="flex items-start justify-between gap-1.5 sm:gap-2">
              <div class="flex-1 min-w-0">
                <h1 class="text-sm sm:text-base lg:text-lg font-bold text-white leading-snug whitespace-normal break-words">
                  {{ notificacionSeleccionada.titulo }}
                </h1>
                <p v-if="notificacionSeleccionada.subtitulo" class="text-[10px] sm:text-xs text-white/80 font-normal mt-0.5 italic whitespace-normal break-words line-clamp-2">
                  {{ notificacionSeleccionada.subtitulo }}
                </p>
              </div>
              
              <!-- Badge de estado -->
              <div :class="[
                'inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded-full text-[8px] font-semibold flex-shrink-0 whitespace-nowrap',
                notificacionSeleccionada.leida 
                  ? 'bg-green-400/25 text-green-50' 
                  : 'bg-amber-400/25 text-amber-50'
              ]">
                <span :class="[
                  'w-1 h-1 rounded-full',
                  notificacionSeleccionada.leida ? 'bg-green-300' : 'bg-amber-300 animate-pulse'
                ]"></span>
                <span>{{ notificacionSeleccionada.leida ? 'Leída' : 'Nueva' }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Contenido del Artículo -->
        <div class="notification-modal-content flex-1 p-4 sm:p-5 overflow-y-auto min-h-0">
          
          <!-- Sección de Vista Previa de Actividad (SI EXISTE) -->
          <div v-if="notificacionSeleccionada.actividad" class="mb-4">
            <!-- Etiqueta superior compacta -->
            <div class="flex items-center gap-1.5 mb-1.5">
              <div :class="[
                'w-5 h-5 rounded-md flex items-center justify-center shadow-sm',
                notificacionSeleccionada.actividad.tipo_actividad === 'campo'
                  ? 'bg-gradient-to-br from-green-500 to-emerald-600'
                  : notificacionSeleccionada.actividad.tipo_actividad === 'gabinete'
                  ? 'bg-gradient-to-br from-orange-500 to-amber-600'
                  : 'bg-gradient-to-br from-gray-500 to-gray-600'
              ]">
                <svg class="w-2.5 h-2.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" />
                </svg>
              </div>
              <h3 class="text-xs font-bold text-gray-700 uppercase tracking-wider">Datos de la actividad</h3>
            </div>
            
            <!-- Card de actividad compacta -->
            <div :class="[
              'relative overflow-hidden rounded-lg transition-all duration-300 border shadow-sm',
              'backdrop-filter backdrop-blur-xl',
              notificacionSeleccionada.actividad.tipo_actividad === 'campo' 
                ? 'bg-gradient-to-br from-green-50/80 via-emerald-25/40 to-green-100/60 border-green-200/60' 
                : notificacionSeleccionada.actividad.tipo_actividad === 'gabinete'
                ? 'bg-gradient-to-br from-orange-50/80 via-amber-25/40 to-orange-100/60 border-orange-200/60'
                : 'bg-gradient-to-br from-gray-50/80 via-white/60 to-gray-100/40 border-gray-200/60'
            ]"
            style="backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);">
              
              <!-- Efectos decorativos -->
              <div class="absolute inset-0 bg-gradient-to-br from-white/20 via-transparent to-transparent opacity-50 rounded-lg pointer-events-none"></div>
              <div v-if="notificacionSeleccionada.actividad.tipo_actividad === 'campo'" class="absolute top-0 right-0 w-10 h-10 bg-gradient-to-bl from-green-400/15 to-transparent rounded-full blur-lg"></div>
              <div v-else-if="notificacionSeleccionada.actividad.tipo_actividad === 'gabinete'" class="absolute top-0 right-0 w-10 h-10 bg-gradient-to-bl from-orange-400/15 to-transparent rounded-full blur-lg"></div>
              
              <!-- Borde superior -->
              <div :class="[
                'absolute top-0 left-0 right-0 h-0.5 rounded-t-lg',
                notificacionSeleccionada.actividad.tipo_actividad === 'campo' 
                  ? 'bg-gradient-to-r from-green-500 to-emerald-600' 
                  : notificacionSeleccionada.actividad.tipo_actividad === 'gabinete'
                  ? 'bg-gradient-to-r from-orange-500 to-amber-600'
                  : 'bg-gradient-to-r from-gray-400 to-gray-600'
              ]"></div>
              
              <div class="relative z-10 p-2">
                <div class="flex gap-2">
                  <!-- Foto compacta -->
                  <div class="w-11 h-11 flex-shrink-0 rounded-md overflow-hidden relative shadow-sm" 
                       :class="{'cursor-pointer': notificacionSeleccionada.actividad.foto_url}" 
                       @click="notificacionSeleccionada.actividad.foto_url && verImagen(notificacionSeleccionada.actividad.foto_url)">
                    <img v-if="notificacionSeleccionada.actividad.foto_url" 
                         :src="notificacionSeleccionada.actividad.foto_url" 
                         class="w-full h-full object-cover transition-transform duration-300 hover:scale-110" 
                         alt="Foto" />
                    <div v-else class="flex justify-center">
                      <div :class="[
                        'w-11 h-11 rounded flex items-center justify-center relative shadow-sm border',
                        notificacionSeleccionada.actividad.tipo_actividad === 'campo' 
                          ? 'bg-gradient-to-br from-green-100 to-green-50 border-green-200/50' 
                          : notificacionSeleccionada.actividad.tipo_actividad === 'gabinete'
                          ? 'bg-gradient-to-br from-orange-100 to-orange-50 border-orange-200/50'
                          : 'bg-gradient-to-br from-gray-100 to-gray-50 border-gray-200/50'
                      ]">
                        <svg xmlns="http://www.w3.org/2000/svg" :class="[
                          'h-5 w-5',
                          notificacionSeleccionada.actividad.tipo_actividad === 'campo' 
                            ? 'text-green-600' 
                            : notificacionSeleccionada.actividad.tipo_actividad === 'gabinete'
                            ? 'text-orange-600'
                            : 'text-gray-500'
                        ]" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"></path>
                        </svg>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Información compacta -->
                  <div class="flex-1 min-w-0 space-y-0.5">
                    <!-- Fecha y tipo -->
                    <div class="flex items-start justify-between gap-1">
                      <div class="flex flex-col">
                        <p v-if="notificacionSeleccionada.actividad.fecha" class="text-xs font-semibold text-gray-700 leading-tight">
                          {{ formatearFechaActividad(notificacionSeleccionada.actividad.fecha).split(' - ')[0] }}
                        </p>
                        <p v-if="notificacionSeleccionada.actividad.categoria_actividad" :class="[
                          'text-xs font-bold leading-tight',
                          notificacionSeleccionada.actividad.tipo_actividad === 'campo' 
                            ? 'text-green-700' 
                            : notificacionSeleccionada.actividad.tipo_actividad === 'gabinete'
                            ? 'text-orange-700'
                            : 'text-gray-700'
                        ]">
                          {{ notificacionSeleccionada.actividad.categoria_actividad }}
                        </p>
                      </div>
                      <!-- Coordenadas -->
                      <div v-if="notificacionSeleccionada.actividad.latitud && notificacionSeleccionada.actividad.longitud" :class="[
                        'text-center bg-white/60 backdrop-blur-sm rounded px-1 py-0.5 border text-[9px] flex-shrink-0',
                        notificacionSeleccionada.actividad.tipo_actividad === 'campo' 
                          ? 'border-green-200/60' 
                          : notificacionSeleccionada.actividad.tipo_actividad === 'gabinete'
                          ? 'border-orange-200/60'
                          : 'border-gray-200/60'
                      ]">
                        <div class="text-gray-600 font-mono leading-tight">{{ notificacionSeleccionada.actividad.latitud.toFixed(2) }}</div>
                        <div class="text-gray-600 font-mono leading-tight">{{ notificacionSeleccionada.actividad.longitud.toFixed(2) }}</div>
                      </div>
                    </div>
                    
                    <!-- Descripción en una línea -->
                    <p v-if="notificacionSeleccionada.actividad.descripcion" class="text-xs text-gray-700 leading-tight line-clamp-1">
                      {{ notificacionSeleccionada.actividad.descripcion }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Sección de Descripción/Mensaje -->
          <div class="notification-description-section mb-3">
            <div class="bg-gradient-to-br from-gray-50/80 to-white border border-gray-200/60 rounded-lg p-3 shadow-sm">
              <div class="notification-description-text text-xs text-gray-700 leading-relaxed" v-html="formatearDescripcion(notificacionSeleccionada.descripcion)"></div>
            </div>
          </div>

          <!-- Sección de Imagen -->
          <div v-if="notificacionSeleccionada.tiene_archivo && esImagen(notificacionSeleccionada.archivo_tipo)" class="notification-image-section mb-6">
            <div class="relative overflow-hidden bg-white rounded-xl border border-gray-200 shadow-md">
              <!-- Placeholder de carga -->
              <div class="flex items-center justify-center min-h-48 bg-gray-50 image-placeholder">
                <div class="text-gray-400 text-center">
                  <div class="w-12 h-12 mx-auto mb-2 bg-gray-200 rounded-full flex items-center justify-center">
                    <svg class="w-6 h-6 text-gray-400 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                    </svg>
                  </div>
                  <div class="text-sm font-medium">Cargando imagen...</div>
                </div>
              </div>
              <!-- Imagen real -->
              <img 
                :src="obtenerUrlArchivo(notificacionSeleccionada.id)" 
                :alt="notificacionSeleccionada.archivo_nombre"
                class="w-full h-auto object-contain cursor-pointer hover:scale-[1.02] transition-transform duration-300 relative z-10 bg-white"
                @click="abrirArchivo(notificacionSeleccionada.id)"
                @error="onImageError"
                @load="onImageLoad"
                loading="eager"
                decoding="async"
              />
              <!-- Overlay con información del archivo -->
              <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 via-black/40 to-transparent p-4">
                <div class="flex items-center justify-between">
                  <p class="text-white text-sm font-medium truncate max-w-[70%]">{{ notificacionSeleccionada.archivo_nombre }}</p>
                  <span class="text-white/70 text-xs bg-white/20 px-2 py-1 rounded-full backdrop-blur-sm">Toca para ampliar</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Sección de Video -->
          <div v-else-if="notificacionSeleccionada.tiene_archivo && esVideo(notificacionSeleccionada.archivo_tipo)" class="notification-video-section mb-6">
            <div class="relative overflow-hidden bg-gray-900 rounded-xl shadow-lg border border-gray-800">
              <video 
                :src="obtenerUrlArchivo(notificacionSeleccionada.id)"
                class="w-full h-auto object-cover"
                controls
                preload="metadata"
                poster=""
              >
                <div class="flex items-center justify-center min-h-48 bg-gray-800">
                  <div class="text-gray-400 text-center">
                    <div class="text-sm">Tu navegador no soporta video</div>
                  </div>
                </div>
              </video>
              <!-- Nombre del archivo -->
              <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-3 pointer-events-none">
                <p class="text-white/80 text-xs font-medium truncate">{{ notificacionSeleccionada.archivo_nombre }}</p>
              </div>
            </div>
          </div>

          <!-- Archivo adjunto -->
          <!-- Archivo adjunto con sistema de descarga y progreso -->
          <div v-else-if="notificacionSeleccionada.tiene_archivo" class="news-attachment mb-6">
            <div class="border border-gray-200 rounded-xl p-4 bg-gradient-to-r from-gray-50 to-white shadow-sm">
              
              <!-- Información del archivo -->
              <div class="flex items-center space-x-3 mb-3">
                <div class="w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 shadow-sm border-2 border-white"
                     :style="{ backgroundColor: obtenerColorTipoArchivo(notificacionSeleccionada.archivo_tipo) }">
                  <span class="text-xs font-bold text-white tracking-wider">{{ obtenerInicialesTipoArchivo(notificacionSeleccionada.archivo_tipo) }}</span>
                </div>
                <div class="flex-1 min-w-0">
                  <h4 class="text-sm font-semibold text-gray-800 truncate">{{ notificacionSeleccionada.archivo_nombre }}</h4>
                  <p class="text-xs text-gray-600 capitalize">{{ notificacionSeleccionada.archivo_tipo }}</p>
                  <p v-if="notificacionSeleccionada.archivoDescargado" class="text-xs text-green-600 font-medium">
                    ✅ Archivo listo para ver
                  </p>
                </div>
              </div>

              <!-- Estados del archivo -->
              <!-- Estado inicial: Sin descarga -->
              <div v-if="!notificacionSeleccionada.estadoDescarga" class="flex justify-end">
                <button 
                  @click="abrirArchivo(notificacionSeleccionada.id)"
                  class="glass-download-button group relative overflow-hidden px-3 py-1.5 rounded-full transition-all duration-300 transform hover:scale-105 active:scale-95"
                >
                  <!-- Fondo con efecto de vidrio líquido -->
                  <div class="absolute inset-0 bg-gradient-to-br from-blue-400/80 via-blue-500/70 to-blue-600/80 rounded-full backdrop-blur-sm"></div>
                  
                  <!-- Efecto de brillo líquido -->
                  <div class="absolute inset-0 rounded-full bg-gradient-to-r from-transparent via-white/20 to-transparent transform -skew-x-12 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
                  
                  <!-- Contenido del botón -->
                  <div class="relative flex items-center justify-center space-x-1.5 text-white">
                    <svg class="w-3.5 h-3.5 transform group-hover:animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                    <span class="font-medium text-2xs tracking-wide">Descargar</span>
                  </div>
                  
                  <!-- Sombra interna para efecto 3D -->
                  <div class="absolute inset-1 rounded-full shadow-inner opacity-30"></div>
                </button>
              </div>

              <!-- Estado: Preparando descarga -->
              <div v-else-if="notificacionSeleccionada.estadoDescarga === 'preparando'" class="space-y-3">
                <div class="flex items-center justify-center space-x-2 text-blue-600">
                  <svg class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                  </svg>
                  <span class="text-sm font-medium">Preparando descarga...</span>
                </div>
              </div>

              <!-- Estado: Descargando con barra de progreso -->
              <div v-else-if="notificacionSeleccionada.estadoDescarga === 'descargando'" class="space-y-3">
                <div class="flex items-center justify-between text-sm">
                  <span class="text-blue-600 font-medium">Descargando archivo...</span>
                  <span class="text-gray-600">{{ notificacionSeleccionada.progresoDescarga }}%</span>
                </div>
                
                <!-- Barra de progreso animada -->
                <div class="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                  <div 
                    class="bg-gradient-to-r from-blue-500 to-blue-600 h-2 rounded-full transition-all duration-500 ease-out relative overflow-hidden"
                    :style="{ width: `${notificacionSeleccionada.progresoDescarga}%` }"
                  >
                    <!-- Efecto de brillo en movimiento -->
                    <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-30 -skew-x-12 animate-pulse"></div>
                  </div>
                </div>
              </div>

              <!-- Estado: Descarga completada -->
              <div v-else-if="notificacionSeleccionada.estadoDescarga === 'completado'" class="space-y-3">
                <div class="flex items-center space-x-2 text-green-600 mb-3">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  <span class="text-sm font-medium">¡Descarga completada!</span>
                </div>
                
                <!-- Información del archivo descargado -->
                <div class="bg-green-50 border border-green-200 rounded-lg p-3 mb-3">
                  <p class="text-xs text-green-800 font-medium">
                    📁 {{ notificacionSeleccionada.archivoDescargado?.nombre }}
                  </p>
                  <p class="text-xs text-green-600 mt-1">
                    Tipo: {{ notificacionSeleccionada.archivoDescargado?.tipo }}
                  </p>
                </div>

                <!-- Botones de acción -->
                <div class="flex space-x-2 justify-end">
                  <!-- Botón para ver con app nativa -->
                  <button 
                    @click="verArchivoDescargado()"
                    class="px-4 py-2 bg-green-500 hover:bg-green-600 text-white text-sm font-medium rounded-lg transition-colors duration-200 flex items-center space-x-2"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                    </svg>
                    <span>Ver archivo</span>
                  </button>
                  
                  <!-- Botón para descargar de nuevo -->
                  <button 
                    @click="abrirArchivo(notificacionSeleccionada.id)"
                    class="px-3 py-2 bg-gray-500 hover:bg-gray-600 text-white text-sm font-medium rounded-lg transition-colors duration-200"
                  >
                    🔄
                  </button>
                </div>
              </div>

              <!-- Estado: Error en descarga -->
              <div v-else-if="notificacionSeleccionada.estadoDescarga === 'error'" class="space-y-3">
                <div class="flex items-center space-x-2 text-red-600 mb-3">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"/>
                  </svg>
                  <span class="text-sm font-medium">Error en la descarga</span>
                </div>
                
                <!-- Mensaje de error -->
                <div class="bg-red-50 border border-red-200 rounded-lg p-3 mb-3">
                  <p class="text-xs text-red-800">{{ notificacionSeleccionada.errorDescarga }}</p>
                </div>

                <!-- Botón para reintentar -->
                <div class="flex justify-end">
                  <button 
                    @click="abrirArchivo(notificacionSeleccionada.id)"
                    class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white text-sm font-medium rounded-lg transition-colors duration-200 flex items-center space-x-2"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                    </svg>
                    <span>Reintentar descarga</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Sección de Enlace -->
          <div v-if="notificacionSeleccionada.enlace_url" class="notification-link-section mb-6">
            <a 
              :href="notificacionSeleccionada.enlace_url" 
              target="_blank"
              rel="noopener noreferrer"
              class="notification-link-card group block"
            >
              <div class="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-4 hover:border-blue-400 hover:shadow-md transition-all duration-300">
                <div class="flex items-center gap-3">
                  <!-- Icono de enlace -->
                  <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center shadow-md group-hover:scale-105 transition-transform">
                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/>
                    </svg>
                  </div>
                  <!-- Contenido -->
                  <div class="flex-1 min-w-0">
                    <div class="text-sm font-semibold text-gray-800 group-hover:text-blue-600 transition-colors">Abrir enlace</div>
                    <div class="text-xs text-gray-500 truncate mt-0.5">{{ formatearEnlaceLegible(notificacionSeleccionada.enlace_url) }}</div>
                  </div>
                  <!-- Flecha -->
                  <div class="flex-shrink-0">
                    <svg class="w-5 h-5 text-gray-400 group-hover:text-blue-500 group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                    </svg>
                  </div>
                </div>
              </div>
            </a>
          </div>
        </div>
        
        <!-- Footer del modal mejorado -->
        <div class="notification-modal-footer flex-shrink-0 border-t border-gray-200 px-4 py-2 bg-gradient-to-r from-gray-50 to-gray-100">
          <div class="flex items-center justify-center gap-1.5 text-[10px] text-gray-400">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <span>Recibido: {{ formatearFecha(notificacionSeleccionada.fecha_creacion) }}</span>
          </div>
        </div>
        </div>
        </div>
      </div>
    </teleport>

    <!-- Modal para visualizar imagen de actividad -->
    <teleport to="body">
      <div v-if="imagenModalVisible" class="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50 p-2" @click="imagenModalVisible = false">
        <div class="relative max-w-full max-h-full">
          <button @click="imagenModalVisible = false" class="absolute right-1 top-1 bg-black bg-opacity-50 text-white rounded-full p-1 hover:bg-opacity-70 transition-opacity z-10">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <div class="overflow-auto max-h-[90vh]" @click.stop>
            <img :src="imagenSeleccionada" class="w-full h-auto object-contain max-h-[75vh]" alt="Imagen ampliada" />
          </div>
        </div>
      </div>
    </teleport>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import notificacionesService from '../services/notificacionesService.js'
import { useNotifications } from '../composables/useNotifications.js'

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
const conteoAnterior = ref(0) // NUEVO: Para detectar cambios en el contador

// Modal de imagen para actividades
const imagenModalVisible = ref(false)
const imagenSeleccionada = ref('')

// NUEVO: Audio para notificaciones
let audioNotificacion = null

// Inicializar audio en el navegador
const inicializarAudio = () => {
  try {
    // Crear un beep utilizando Web Audio API
    const audioContext = new (window.AudioContext || window.webkitAudioContext)()
    
    // Función para crear un sonido de notificación suave tipo "ding" moderno
    const crearSonidoNotificacion = () => {
      const oscillator1 = audioContext.createOscillator()
      const oscillator2 = audioContext.createOscillator()
      const gainNode = audioContext.createGain()
      
      // Conectar los nodos
      oscillator1.connect(gainNode)
      oscillator2.connect(gainNode)
      gainNode.connect(audioContext.destination)
      
      // Configurar el primer oscilador - tono principal
      oscillator1.type = 'sine' // Onda sinusoidal suave
      oscillator1.frequency.setValueAtTime(1000, audioContext.currentTime)
      oscillator1.frequency.exponentialRampToValueAtTime(800, audioContext.currentTime + 0.1)
      
      // Configurar el segundo oscilador - armonía sutil
      oscillator2.type = 'sine'
      oscillator2.frequency.setValueAtTime(1200, audioContext.currentTime)
      oscillator2.frequency.exponentialRampToValueAtTime(960, audioContext.currentTime + 0.1)
      
      // Configurar el volumen - envolvente muy suave tipo "ding"
      gainNode.gain.setValueAtTime(0, audioContext.currentTime)
      gainNode.gain.linearRampToValueAtTime(0.08, audioContext.currentTime + 0.02) // Ataque rápido
      gainNode.gain.exponentialRampToValueAtTime(0.05, audioContext.currentTime + 0.1) // Sustain suave
      gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.6) // Decay largo y suave
      
      // Reproducir ambos osciladores
      oscillator1.start(audioContext.currentTime)
      oscillator1.stop(audioContext.currentTime + 0.6)
      
      oscillator2.start(audioContext.currentTime)
      oscillator2.stop(audioContext.currentTime + 0.6)
    }
    
    audioNotificacion = crearSonidoNotificacion
    console.log('🔊 Audio de notificaciones inicializado correctamente')
    
  } catch (error) {
    console.warn('⚠️ No se pudo inicializar el audio de notificaciones:', error)
    
    // Fallback: usar un beep del sistema si está disponible
    audioNotificacion = () => {
      try {
        // Intentar usar el beep del sistema
        if (navigator.vibrate) {
          navigator.vibrate([100, 50, 100]) // Patrón de vibración suave
        }
        console.log('📳 Usando vibración como alternativa al sonido')
      } catch (e) {
        console.log('🔇 No hay alternativas de audio/vibración disponibles')
      }
    }
  }
}

// NUEVO: Función para reproducir sonido de notificación
const reproducirSonidoNotificacion = () => {
  try {
    if (audioNotificacion && typeof audioNotificacion === 'function') {
      audioNotificacion()
      console.log('🔊 Sonido de notificación reproducido')
    } else {
      console.log('🔇 Audio de notificaciones no disponible')
    }
  } catch (error) {
    console.warn('⚠️ Error reproduciendo sonido de notificación:', error)
  }
}

// NUEVO: Detectar nuevas notificaciones y reproducir sonido (MEJORADO - menos frecuente)
const detectarNuevasNotificaciones = (nuevoConteo) => {
  // Solo reproducir sonido si:
  // 1. No estamos cargando por primera vez
  // 2. El nuevo conteo es mayor al anterior
  // 3. El conteo anterior no es 0 (evitar sonido al cargar inicial)
  // 4. Ha pasado al menos 10 segundos desde el último sonido
  const ahora = Date.now()
  const tiempoUltimoSonido = localStorage.getItem('ultimoSonidoNotificacion')
  const INTERVALO_MINIMO = 10000 // 10 segundos entre sonidos
  
  if (!cargando.value && 
      nuevoConteo > conteoAnterior.value && 
      conteoAnterior.value >= 0 &&
      (!tiempoUltimoSonido || (ahora - parseInt(tiempoUltimoSonido)) > INTERVALO_MINIMO)) {
    
    const nuevasNotificaciones = nuevoConteo - conteoAnterior.value
    console.log(`🔔 ${nuevasNotificaciones} nueva(s) notificación(es) detectada(s)`)
    
    // Reproducir sonido para nuevas notificaciones
    reproducirSonidoNotificacion()
    
    // Guardar timestamp del último sonido
    localStorage.setItem('ultimoSonidoNotificacion', ahora.toString())
    
    // Mostrar notificación del navegador si está permitido
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification('Nueva notificación', {
        body: `Tienes ${nuevasNotificaciones} nueva(s) notificación(es)`,
        icon: '/pwa-192x192.png',
        tag: 'new-notification',
        silent: false // Permitir que el navegador también haga sonido
      })
    }
  }
  
  // Actualizar contador anterior para la próxima comparación
  conteoAnterior.value = nuevoConteo
}

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

// NUEVO: Obtener conteo de no leídas con detección de cambios
const obtenerConteoNoLeidas = async (usuarioId, detectarCambios = true) => {
  try {
    if (!usuarioId) return 0
    
    console.log(`📊 Obteniendo conteo de no leídas para usuario ${usuarioId}`)
    
    const conteo = await notificacionesService.obtenerConteoNoLeidas(usuarioId)
    
    // Detectar cambios y reproducir sonido si corresponde
    if (detectarCambios) {
      detectarNuevasNotificaciones(conteo)
    }
    
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
    
    // Obtener conteo de no leídas (sin detectar cambios en la carga inicial)
    await obtenerConteoNoLeidas(usuarioId, !resetear)
    
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

// Función para abrir directamente el modal completo (usado en los clicks de imágenes/videos)
const verNotificacionCompleta = (notificacion) => {
  abrirDetalleNotificacion(notificacion)
}

const cerrarDetalleNotificacion = () => {
  notificacionSeleccionada.value = null
}

// Función para formatear enlace de manera más legible
const formatearEnlace = (url) => {
  if (!url) return ''
  
  try {
    const urlObj = new URL(url)
    const domain = urlObj.hostname.replace('www.', '')
    const path = urlObj.pathname
    
    // Si el path es muy largo, truncarlo
    if (path.length > 30) {
      return `${domain}${path.substring(0, 25)}...`
    }
    
    return `${domain}${path}`
  } catch (e) {
    // Si no es una URL válida, truncar el texto
    return url.length > 40 ? `${url.substring(0, 37)}...` : url
  }
}

// Función para formatear enlace de manera muy corta
const formatearEnlaceCorto = (url) => {
  if (!url) return ''
  
  try {
    const urlObj = new URL(url)
    const domain = urlObj.hostname.replace('www.', '')
    
    // Solo mostrar el dominio, máximo 25 caracteres
    return domain.length > 25 ? `${domain.substring(0, 22)}...` : domain
  } catch (e) {
    // Si no es una URL válida, mostrar solo los primeros caracteres
    return url.length > 25 ? `${url.substring(0, 22)}...` : url
  }
}

// Función para formatear enlace de manera más legible y atractiva
const formatearEnlaceLegible = (url) => {
  if (!url) return ''
  
  try {
    const urlObj = new URL(url)
    let domain = urlObj.hostname.replace('www.', '')
    const path = urlObj.pathname
    
    // Hacer el dominio más legible
    if (domain.includes('.')) {
      const parts = domain.split('.')
      if (parts.length >= 2) {
        // Capitalizar el nombre principal del sitio
        const mainName = parts[parts.length - 2]
        const extension = parts[parts.length - 1]
        const capitalizedName = mainName.charAt(0).toUpperCase() + mainName.slice(1)
        
        if (parts.length > 2) {
          // Para subdominios
          domain = `${parts.slice(0, -2).join('.')}.${capitalizedName}.${extension}`
        } else {
          domain = `${capitalizedName}.${extension}`
        }
      }
    }
    
    // Agregar path si es corto y relevante
    if (path && path !== '/' && path.length <= 20) {
      return `${domain}${path}`
    }
    
    // Si el dominio es muy largo, truncarlo elegantemente
    if (domain.length > 30) {
      return `${domain.substring(0, 27)}...`
    }
    
    return domain
  } catch (e) {
    // Si no es una URL válida, intentar hacerla más legible
    const cleaned = url.replace(/^https?:\/\//, '').replace(/^www\./, '')
    return cleaned.length > 30 ? `${cleaned.substring(0, 27)}...` : cleaned
  }
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
      await obtenerConteoNoLeidas(usuarioId, false) // No detectar cambios en operaciones manuales
      
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

const abrirArchivo = async (notificacionId) => {
  try {
    console.log(`📂 Preparando descarga de archivo de notificación ${notificacionId}`)
    
    // Buscar la notificación para obtener información del archivo
    const notificacion = notificaciones.value.find(n => n.id === notificacionId) || 
                         (notificacionSeleccionada.value?.id === notificacionId ? notificacionSeleccionada.value : null)
    
    if (!notificacion) {
      console.error('❌ Notificación no encontrada')
      mostrarNotificacionError('No se encontró la notificación')
      return
    }

    // Abrir el modal de la notificación si no está abierto
    if (!notificacionSeleccionada.value || notificacionSeleccionada.value.id !== notificacionId) {
      abrirDetalleNotificacion(notificacion)
    }

    // Crear estado de descarga en la notificación seleccionada
    if (notificacionSeleccionada.value) {
      notificacionSeleccionada.value.estadoDescarga = 'preparando'
      notificacionSeleccionada.value.progresoDescarga = 0
      notificacionSeleccionada.value.archivoDescargado = null
      notificacionSeleccionada.value.errorDescarga = null
    }

    // Simular inicio de descarga
    setTimeout(async () => {
      try {
        console.log(`🔄 Iniciando descarga: ${notificacion.archivo_nombre || `Archivo ${notificacionId}`}`)
        
        if (notificacionSeleccionada.value) {
          notificacionSeleccionada.value.estadoDescarga = 'descargando'
          notificacionSeleccionada.value.progresoDescarga = 10
        }

        // Obtener el archivo del servidor usando base64 para evitar problemas de encoding
        const archivoData = await notificacionesService.obtenerArchivoBase64(notificacionId)
        
        if (notificacionSeleccionada.value) {
          notificacionSeleccionada.value.progresoDescarga = 60
        }

        // El servicio ya convierte base64 a blob y devuelve la URL lista
        if (notificacionSeleccionada.value) {
          notificacionSeleccionada.value.progresoDescarga = 90
        }
        
        if (notificacionSeleccionada.value) {
          notificacionSeleccionada.value.progresoDescarga = 100
          notificacionSeleccionada.value.estadoDescarga = 'completado'
          notificacionSeleccionada.value.archivoDescargado = {
            url: archivoData.url,
            nombre: archivoData.nombre,
            tipo: archivoData.mimeType,
            tamano: archivoData.size
          }
        }

        console.log('✅ Archivo preparado para visualización')
        mostrarNotificacionExito('Archivo listo para ver')
        
      } catch (error) {
        console.error('❌ Error descargando archivo:', error)
        
        if (notificacionSeleccionada.value) {
          notificacionSeleccionada.value.estadoDescarga = 'error'
          notificacionSeleccionada.value.errorDescarga = error.message || 'Error al descargar el archivo'
        }
        
        mostrarNotificacionError(`Error: ${error.message || 'No se pudo descargar el archivo'}`)
      }
    }, 500) // Pequeño delay para mostrar el estado inicial

  } catch (error) {
    console.error('❌ Error general preparando archivo:', error)
    
    if (notificacionSeleccionada.value) {
      notificacionSeleccionada.value.estadoDescarga = 'error'
      notificacionSeleccionada.value.errorDescarga = error.message || 'Error preparando descarga'
    }
    
    mostrarNotificacionError(`Error: ${error.message || 'No se pudo preparar el archivo'}`)
  }
}

// Función original comentada como backup
/*
const abrirArchivoBackup = async (notificacionId) => {
  try {
    console.log(`� Descargando archivo de notificación ${notificacionId} para abrir con app externa`)
    
    // Buscar la notificación para obtener información del archivo
    const notificacion = notificaciones.value.find(n => n.id === notificacionId) || 
                         (notificacionSeleccionada.value?.id === notificacionId ? notificacionSeleccionada.value : null)
    
    if (!notificacion) {
      console.error('❌ Notificación no encontrada')
      mostrarNotificacionError('No se encontró la notificación')
      return
    }

    console.log(`📂 Iniciando descarga de: ${notificacion.archivo_nombre || `Archivo ${notificacionId}`}`)

    // Crear enlace temporal para descarga automática
    const link = document.createElement('a')
    let descargaExitosa = false

    // ESTRATEGIA 1: Intentar descargar con URL segura (mejor para archivos con caracteres especiales)
    try {
      console.log('🔄 Intento 1: Descarga con URL segura...')
      const urlSegura = notificacionesService.obtenerUrlArchivo(notificacionId, true)
      
      link.href = urlSegura
      link.download = notificacion.archivo_nombre || `archivo_${notificacionId}`
      link.target = '_blank'
      link.rel = 'noopener noreferrer'
      
      // Agregar al DOM temporalmente y hacer click
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      descargaExitosa = true
      console.log('✅ Descarga iniciada con URL segura')
      
    } catch (error) {
      console.log('❌ Error con URL segura:', error.message)
      
      // ESTRATEGIA 2: URL normal como fallback
      try {
        console.log('🔄 Intento 2: Descarga con URL normal...')
        const urlNormal = notificacionesService.obtenerUrlArchivo(notificacionId, false)
        
        link.href = urlNormal
        link.download = notificacion.archivo_nombre || `archivo_${notificacionId}`
        link.target = '_blank'
        link.rel = 'noopener noreferrer'
        
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        
        descargaExitosa = true
        console.log('✅ Descarga iniciada con URL normal')
        
      } catch (error2) {
        console.log('❌ Error con URL normal:', error2.message)
        
        // ESTRATEGIA 3: Página de carga móvil elegante como último recurso
        try {
          console.log('🔄 Intento 3: Abriendo con página de carga móvil...')
          const urlMobile = `${import.meta.env.PROD ? 'https://apipwa.sembrandodatos.com' : 'http://localhost:8000'}/notificaciones/${notificacionId}/archivo/mobile`
          
          const nuevaVentana = window.open(urlMobile, '_blank', 'noopener,noreferrer')
          
          if (nuevaVentana) {
            descargaExitosa = true
            console.log('✅ Página de carga móvil abierta')
            mostrarNotificacionExito('Se abrió una página de carga. El archivo se descargará automáticamente.')
          } else {
            throw new Error('El navegador bloqueó la ventana emergente')
          }
          
        } catch (error3) {
          console.log('❌ Error abriendo página de carga móvil:', error3.message)
          throw new Error('No se pudo abrir el archivo con ningún método disponible')
        }
      }
    }
    
    // Mostrar confirmación si la descarga fue exitosa
    if (descargaExitosa) {
      // Feedback visual y háptico
      if (window.navigator && window.navigator.vibrate) {
        window.navigator.vibrate(100) // Vibración suave de confirmación
      }
      
      mostrarNotificacionExito('Archivo enviado para descarga. Se abrirá con la aplicación predeterminada de tu dispositivo.')
    }
    
  } catch (error) {
    console.error('❌ Error general abriendo archivo:', error)
    
    const mensaje = error.message || 'No se pudo abrir el archivo. Verifica tu conexión.'
    mostrarNotificacionError(`Error: ${mensaje}`)
    
    // Vibración de error
    if (window.navigator && window.navigator.vibrate) {
      window.navigator.vibrate([200, 100, 200])
    }
  }
}

}
*/

// Nueva función para abrir el archivo descargado con aplicación nativa
const verArchivoDescargado = () => {
  if (!notificacionSeleccionada.value?.archivoDescargado) {
    mostrarNotificacionError('No hay archivo descargado para ver')
    return
  }

  try {
    console.log('🔄 Abriendo archivo con aplicación nativa...')
    
    // Crear enlace temporal para descargar/abrir
    const link = document.createElement('a')
    link.href = notificacionSeleccionada.value.archivoDescargado.url
    link.download = notificacionSeleccionada.value.archivoDescargado.nombre
    link.target = '_blank'
    link.rel = 'noopener noreferrer'
    
    // Agregar al DOM, hacer click y remover
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    console.log('✅ Archivo enviado para abrir con aplicación nativa')
    mostrarNotificacionExito('Archivo abierto con aplicación del dispositivo')
    
    // Vibración de confirmación
    if (window.navigator && window.navigator.vibrate) {
      window.navigator.vibrate(100)
    }
    
  } catch (error) {
    console.error('❌ Error abriendo archivo:', error)
    mostrarNotificacionError('No se pudo abrir el archivo')
  }
}

// Funciones auxiliares para notificaciones de estado
const mostrarNotificacionExito = (mensaje) => {
  const notificacion = crearNotificacionTemporal(mensaje, 'success')
  document.body.appendChild(notificacion)
  
  setTimeout(() => {
    if (document.body.contains(notificacion)) {
      document.body.removeChild(notificacion)
    }
  }, 4000)
}

const mostrarNotificacionError = (mensaje) => {
  const notificacion = crearNotificacionTemporal(mensaje, 'error')
  document.body.appendChild(notificacion)
  
  setTimeout(() => {
    if (document.body.contains(notificacion)) {
      document.body.removeChild(notificacion)
    }
  }, 6000)
}

const crearNotificacionTemporal = (mensaje, tipo = 'success') => {
  const notificacion = document.createElement('div')
  
  const estilos = tipo === 'success' 
    ? 'bg-green-500 text-white' 
    : 'bg-red-500 text-white'
    
  const icono = tipo === 'success' 
    ? `<svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
         <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
       </svg>`
    : `<svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
         <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
       </svg>`
  
  notificacion.className = `fixed top-4 right-4 ${estilos} px-4 py-3 rounded-lg shadow-lg z-50 max-w-sm animate-fade-in`
  notificacion.innerHTML = `
    <div class="flex items-start gap-3">
      ${icono}
      <div>
        <div class="font-medium">${tipo === 'success' ? '¡Éxito!' : 'Error'}</div>
        <div class="text-sm opacity-90 mt-1">${mensaje}</div>
      </div>
    </div>
  `
  
  return notificacion
}

// Función para determinar si el archivo se puede mostrar inline
const puedeVerseInline = (tipo) => {
  if (!tipo) return false
  const tipoLower = tipo.toLowerCase()
  
  // Tipos que se pueden mostrar directamente en el navegador
  return tipoLower.includes('pdf') || 
         tipoLower.includes('image') || 
         tipoLower.includes('imagen') ||
         ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'pdf'].includes(tipoLower)
}

const obtenerUrlArchivo = (notificacionId) => {
  return notificacionesService.obtenerUrlArchivo(notificacionId)
}

const obtenerIconoArchivo = (tipoArchivo) => {
  return notificacionesService.obtenerIconoArchivo(tipoArchivo)
}

// Función para obtener las iniciales del tipo de archivo
const obtenerInicialesTipoArchivo = (tipoArchivo) => {
  if (!tipoArchivo) return 'AR'
  
  const tipo = tipoArchivo.toLowerCase()
  
  // Tipos específicos con iniciales personalizadas
  if (tipo.includes('pdf')) return 'PDF'
  if (tipo.includes('doc') || tipo.includes('word')) return 'DOC'
  if (tipo.includes('xls') || tipo.includes('excel')) return 'XLS'
  if (tipo.includes('ppt') || tipo.includes('powerpoint')) return 'PPT'
  if (tipo.includes('txt')) return 'TXT'
  if (tipo.includes('zip') || tipo.includes('rar')) return 'ZIP'
  if (tipo.includes('imagen') || tipo.includes('image')) return 'IMG'
  if (tipo.includes('video')) return 'VID'
  if (tipo.includes('audio')) return 'AUD'
  if (tipo.includes('csv')) return 'CSV'
  if (tipo.includes('json')) return 'JSON'
  if (tipo.includes('xml')) return 'XML'
  
  // Para tipos genéricos, tomar las primeras 3 letras y convertir a mayúsculas
  return tipo.substring(0, 3).toUpperCase() || 'AR'
}

// Función para obtener el color de fondo según el tipo de archivo
const obtenerColorTipoArchivo = (tipoArchivo) => {
  if (!tipoArchivo) return '#6B7280' // Gris por defecto
  
  const tipo = tipoArchivo.toLowerCase()
  
  // Colores específicos por tipo de archivo
  if (tipo.includes('pdf')) return '#EF4444' // Rojo para PDF
  if (tipo.includes('doc') || tipo.includes('word')) return '#2563EB' // Azul para Word
  if (tipo.includes('xls') || tipo.includes('excel')) return '#059669' // Verde para Excel
  if (tipo.includes('ppt') || tipo.includes('powerpoint')) return '#DC2626' // Rojo oscuro para PowerPoint
  if (tipo.includes('txt')) return '#6B7280' // Gris para TXT
  if (tipo.includes('zip') || tipo.includes('rar')) return '#7C3AED' // Púrpura para archivos comprimidos
  if (tipo.includes('imagen') || tipo.includes('image')) return '#EC4899' // Rosa para imágenes
  if (tipo.includes('video')) return '#F59E0B' // Ámbar para videos
  if (tipo.includes('audio')) return '#10B981' // Esmeralda para audio
  if (tipo.includes('csv')) return '#059669' // Verde para CSV
  if (tipo.includes('json')) return '#8B5CF6' // Violeta para JSON
  if (tipo.includes('xml')) return '#F97316' // Naranja para XML
  
  // Color por defecto
  return '#6366F1' // Índigo por defecto
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

const onVideoLoaded = (event) => {
  // Ocultar el placeholder de carga cuando el video se haya cargado
  const video = event.target
  const placeholder = video.parentNode.querySelector('.video-placeholder')
  
  if (placeholder && video.readyState >= 1) {
    // readyState >= 1 significa que los metadatos han sido cargados
    video.setAttribute('data-loaded', 'true')
    placeholder.style.opacity = '0'
    setTimeout(() => {
      if (placeholder.style.opacity === '0') {
        placeholder.style.display = 'none'
      }
    }, 300) // Transición suave
  }
}

const onVideoError = (event) => {
  console.warn('Error cargando video:', event.target.src)
  
  // Ocultar el placeholder de carga
  const placeholder = event.target.parentNode.querySelector('.video-placeholder')
  if (placeholder) {
    placeholder.style.display = 'none'
  }
  
  // Crear elemento de reemplazo con mejor diseño
  const parent = event.target.parentNode
  const errorDiv = document.createElement('div')
  errorDiv.className = 'flex flex-col items-center justify-center w-full h-full bg-gray-100 rounded text-xs text-gray-500 p-4 absolute inset-0 z-20'
  
  errorDiv.innerHTML = `
    <div class="text-center">
      <div class="font-medium">Error cargando video</div>
      <div class="text-xs text-gray-400 mt-1">Archivo no disponible</div>
    </div>
  `
  
  // Ocultar video original y mostrar error
  event.target.style.display = 'none'
  parent.appendChild(errorDiv)
}

const onVideoFallback = (event) => {
  // Fallback para ocultar placeholder después de 5 segundos si no se ha cargado
  const video = event.target
  const placeholder = video.parentNode.querySelector('.video-placeholder')
  
  if (placeholder && !video.hasAttribute('data-loaded')) {
    console.log('Video tardando en cargar, ocultando placeholder por fallback')
    placeholder.style.opacity = '0'
    setTimeout(() => {
      if (placeholder && placeholder.style.opacity === '0') {
        placeholder.style.display = 'none'
      }
    }, 300)
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

// Función para formatear fecha de actividad
const formatearFechaActividad = (fechaISO) => {
  if (!fechaISO) return ''
  
  try {
    const fecha = new Date(fechaISO)
    const opciones = { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }
    return fecha.toLocaleDateString('es-MX', opciones)
  } catch (error) {
    return fechaISO
  }
}

// Función para abrir modal de imagen
const verImagen = (url) => {
  if (!url) return
  imagenSeleccionada.value = url
  imagenModalVisible.value = true
  
  // Cerrar con tecla ESC
  nextTick(() => {
    const handleKeyPress = (event) => {
      if (event.key === 'Escape') {
        imagenModalVisible.value = false
        document.removeEventListener('keydown', handleKeyPress)
      }
    }
    document.addEventListener('keydown', handleKeyPress)
  })
}

// Función para formatear la descripción respetando saltos de línea y formato
const formatearDescripcion = (texto) => {
  if (!texto) return ''
  
  // Escapar HTML para seguridad
  const escaparHtml = (str) => {
    const div = document.createElement('div')
    div.textContent = str
    return div.innerHTML
  }
  
  let textoFormateado = escaparHtml(texto)
  
  // Convertir saltos de línea a <br>
  textoFormateado = textoFormateado.replace(/\n\n/g, '</p><p class="mt-3">')
  textoFormateado = textoFormateado.replace(/\n/g, '<br>')
  
  // Detectar URLs y convertirlas en enlaces
  const urlRegex = /(https?:\/\/[^\s<]+)/g
  textoFormateado = textoFormateado.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline break-all">$1</a>')
  
  // Detectar texto entre asteriscos como negrita
  textoFormateado = textoFormateado.replace(/\*\*(.+?)\*\*/g, '<strong class="font-semibold text-gray-900">$1</strong>')
  textoFormateado = textoFormateado.replace(/\*(.+?)\*/g, '<em class="italic">$1</em>')
  
  // Envolver en párrafo si no está ya
  if (!textoFormateado.startsWith('<p')) {
    textoFormateado = `<p class="mb-0">${textoFormateado}</p>`
  }
  
  return textoFormateado
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
  
  // Inicializar audio de notificaciones
  inicializarAudio()
  
  // Solicitar permisos de notificación si no están otorgados
  if ('Notification' in window && Notification.permission === 'default') {
    try {
      const permission = await Notification.requestPermission()
      console.log(`🔔 Permisos de notificación: ${permission}`)
    } catch (error) {
      console.warn('⚠️ Error solicitando permisos de notificación:', error)
    }
  }
  
  cargarConfiguracion()
  
  // Cargar notificaciones inicial (sin detección de cambios)
  await cargarNotificaciones()
  
  // Establecer el contador inicial después de la primera carga
  const usuarioId = obtenerUsuarioId()
  if (usuarioId) {
    conteoAnterior.value = conteoNoLeidas.value // Establecer el valor base
  }
  
  // Auto-actualizar cada 30 segundos para detección de nuevas notificaciones (reducido de 2 segundos)
  autoUpdateInterval = setInterval(async () => {
    if (!cargando.value && !cargandoMas.value) {
      const usuarioId = obtenerUsuarioId()
      if (usuarioId) {
        // Actualizar badge global y detectar nuevas notificaciones con sonido
        await fetchUnreadCount(usuarioId)
        await obtenerConteoNoLeidas(usuarioId, true) // Habilitar detección de cambios
        
        // Solo recargar lista si está en vista de no leídas y hay cambios
        if (soloNoLeidas.value && conteoNoLeidas.value > 0) {
          await cargarNotificaciones()
        }
      }
    }
  }, 30000) // 30 segundos para reducir el spam de sonidos
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

/* Contenedor para notificaciones con campanita externa */
.notification-container {
  margin-bottom: 0.25rem; /* Reducido de 0.5rem a 0.25rem */
  padding-top: 0.25rem; /* Espacio reducido para la campanita */
}

/* Estilos empresariales para notificaciones - Optimizado */
.enterprise-notification-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 1rem !important;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Inter', 'Helvetica Neue', sans-serif;
}

.enterprise-notification-card.notification-read,
.enterprise-notification-card.notification-unread {
  border-radius: 1rem !important;
}

/* Tipografía profesional para elementos de notificaciones */
.enterprise-notification-card h3 {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Inter', 'Helvetica Neue', sans-serif;
  font-weight: 600;
  letter-spacing: -0.025em;
}

.enterprise-notification-card p {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Inter', 'Helvetica Neue', sans-serif;
  font-weight: 400;
  line-height: 1.5;
}

.enterprise-notification-card .notification-subtitle {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Inter', 'Helvetica Neue', sans-serif;
  font-weight: 500;
  font-style: italic;
  opacity: 0.9;
  line-height: 1.4;
}

.enterprise-notification-card .notification-date {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Inter', 'Helvetica Neue', sans-serif;
  font-weight: 500;
  letter-spacing: 0.025em;
}

.enterprise-notification-card:hover {
  border-color: #d1d5db;
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1), 
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transform: translateY(-1px);
}

.enterprise-notification-card.notification-unread {
  background: linear-gradient(-45deg, #9f1239, #be123c, #881337, #a21547, #9f1239);
  background-size: 400% 400%;
  animation: gradient-flow 4s ease infinite;
  border-left-width: 4px;
  border-left-color: rgba(255, 255, 255, 0.7);
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 15px 0 rgba(159, 18, 57, 0.4),
    0 2px 6px 0 rgba(159, 18, 57, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
  will-change: background-position;
}

/* Animación de flujo del gradiente */
@keyframes gradient-flow {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

/* Efecto de brillo sutil moviéndose */
.enterprise-notification-card.notification-unread::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    rgba(255, 255, 255, 0.2),
    rgba(255, 255, 255, 0.1),
    transparent
  );
  animation: shimmer-sweep 3s ease-in-out infinite;
  z-index: 1;
  pointer-events: none;
}

@keyframes shimmer-sweep {
  0% {
    left: -100%;
  }
  50%, 100% {
    left: 100%;
  }
}

/* Overlay de brillo suave */
.enterprise-notification-card.notification-unread::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(
    ellipse at 30% 20%,
    rgba(255, 255, 255, 0.15) 0%,
    transparent 50%
  );
  z-index: 1;
  pointer-events: none;
}

/* Asegurar que el contenido esté por encima de todo */
.enterprise-notification-card.notification-unread > * {
  position: relative;
  z-index: 2;
}

/* Textos blancos para notificaciones no leídas */
.enterprise-notification-card.notification-unread h3,
.enterprise-notification-card.notification-unread .notification-subtitle,
.enterprise-notification-card.notification-unread .notification-date,
.enterprise-notification-card.notification-unread p {
  color: #ffffff !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.enterprise-notification-card.notification-unread h3 {
  color: #ffffff !important;
  font-weight: 700;
}

.enterprise-notification-card.notification-unread .notification-subtitle {
  color: rgba(255, 255, 255, 0.9) !important;
}

.enterprise-notification-card.notification-unread .notification-date {
  color: rgba(255, 255, 255, 0.85) !important;
}

/* Icono con fondo blanco/rojo para contraste */
.enterprise-notification-card.notification-unread .flex-shrink-0 > div {
  background: linear-gradient(135deg, rgba(255,255,255,0.85) 0%, #fb7185 100%) !important;
  border-color: rgba(255, 255, 255, 0.5) !important;
  color: #881337 !important;
  box-shadow: 0 2px 8px rgba(255, 255, 255, 0.3);
}

.enterprise-notification-card.notification-read {
  background: #ffffff;
  border-left-width: 3px;
  border-left-color: #22c55e;
}

.enterprise-notification-card.notification-unread:hover {
  background: linear-gradient(-45deg, #881337, #9f1239, #7f1d1d, #9f1239, #881337);
  background-size: 400% 400%;
  animation: gradient-flow 2s ease infinite;
  border-left-color: rgba(255, 255, 255, 0.9);
  box-shadow: 
    0 8px 25px 0 rgba(159, 18, 57, 0.5),
    0 4px 10px 0 rgba(159, 18, 57, 0.3),
    0 0 0 2px rgba(255, 255, 255, 0.2);
  transform: translateY(-3px) scale(1.01);
}

/* Acelerar animación de brillo en hover */
.enterprise-notification-card.notification-unread:hover::before {
  animation: shimmer-sweep 1.5s ease-in-out infinite;
}

.enterprise-notification-card.notification-read:hover {
  background: #f9fafb;
}

/* Botón Ver completo compacto - LEGACY */
.enterprise-view-button-compact {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Inter', 'Helvetica Neue', sans-serif;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.enterprise-view-button-compact:hover {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

/* Nuevo botón con efecto vidrio líquido */
.liquid-glass-button {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.1),
    0 2px 4px rgba(0, 0, 0, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
  position: relative;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Inter', 'Helvetica Neue', sans-serif;
}

/* Efecto de onda líquida */
.liquid-glass-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(34, 197, 94, 0.15),
    rgba(16, 185, 129, 0.2),
    rgba(34, 197, 94, 0.15),
    transparent
  );
  transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  z-index: 1;
}

/* Efecto de burbuja líquida */
.liquid-glass-button::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: radial-gradient(
    circle,
    rgba(34, 197, 94, 0.2) 0%,
    rgba(16, 185, 129, 0.15) 50%,
    transparent 70%
  );
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1;
  opacity: 0;
}

.liquid-glass-button:hover {
  background: rgba(255, 255, 255, 0.85);
  border-color: rgba(34, 197, 94, 0.3);
  box-shadow: 
    0 8px 32px rgba(34, 197, 94, 0.15),
    0 4px 16px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.8),
    inset 0 -1px 0 rgba(34, 197, 94, 0.1);
  transform: translateY(-1px);
  color: #065f46;
}

/* Activar efectos en hover */
.liquid-glass-button:hover::before {
  left: 100%;
}

.liquid-glass-button:hover::after {
  width: 150px;
  height: 150px;
  opacity: 1;
}

.liquid-glass-button:active {
  transform: translateY(0) scale(0.98);
  box-shadow: 
    0 4px 16px rgba(34, 197, 94, 0.2),
    0 2px 8px rgba(0, 0, 0, 0.1),
    inset 0 2px 4px rgba(34, 197, 94, 0.1);
}

.liquid-glass-button:focus {
  outline: none;
  box-shadow: 
    0 8px 32px rgba(34, 197, 94, 0.15),
    0 4px 16px rgba(0, 0, 0, 0.08),
    0 0 0 3px rgba(34, 197, 94, 0.2);
}

/* Botón de descarga con efecto de vidrio líquido mejorado */
.glass-download-button {
  position: relative;
  background: transparent;
  border: none;
  cursor: pointer;
  box-shadow: 
    0 8px 32px rgba(59, 130, 246, 0.25),
    0 4px 16px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    inset 0 -1px 0 rgba(0, 0, 0, 0.1);
}

.glass-download-button:hover {
  box-shadow: 
    0 12px 40px rgba(59, 130, 246, 0.35),
    0 6px 20px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3),
    inset 0 -1px 0 rgba(0, 0, 0, 0.15);
}

.glass-download-button:active {
  transform: scale(0.95) !important;
  box-shadow: 
    0 4px 16px rgba(59, 130, 246, 0.2),
    0 2px 8px rgba(0, 0, 0, 0.08),
    inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.glass-download-button:focus {
  outline: none;
  box-shadow: 
    0 8px 32px rgba(59, 130, 246, 0.3),
    0 4px 16px rgba(0, 0, 0, 0.1),
    0 0 0 3px rgba(59, 130, 246, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

/* Utilidades para truncar texto */
.line-clamp-1 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 1;
  line-clamp: 1;
}

.line-clamp-2 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  line-clamp: 2;
}

/* Animaciones suaves para elementos interactivos */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.enterprise-notification-card {
  animation: fadeInUp 0.3s ease-out;
}

/* Estilos responsivos para notificaciones empresariales - Compacto */
@media (max-width: 640px) {
  .notification-container {
    margin-bottom: 0.2rem; /* Aún más compacto en móviles */
  }
  
  .enterprise-notification-card {
    border-radius: 0.375rem;
  }
  
  .enterprise-notification-card .flex.items-start {
    padding: 0.5rem 0.75rem;
    gap: 0.5rem;
  }
  
  .enterprise-notification-card h3 {
    font-size: 0.8125rem;
  }
  
  .enterprise-notification-card p {
    font-size: 0.75rem;
  }
  
  .enterprise-view-button-compact {
    padding: 0.375rem 0.5rem;
    font-size: 0.75rem;
  }
  
  .enterprise-view-button-compact svg {
    width: 0.75rem;
    height: 0.75rem;
  }
}

/* Campanita vibrante para notificaciones no leídas - Nueva animación suave */
.notification-bell {
  box-shadow: 
    0 2px 6px rgba(220, 38, 38, 0.4),
    0 1px 3px rgba(220, 38, 38, 0.3);
  position: relative;
  z-index: 50;
  border: 2px solid rgba(255, 255, 255, 0.9);
  /* El círculo NO se mueve */
}

.notification-bell:hover .bell-icon {
  animation-play-state: paused;
}

.bell-icon {
  animation: bell-swing 0.5s ease-in-out infinite;
  transform-origin: center 20%;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
  /* Solo el ícono se anima con movimiento pendular más rápido */
}

/* Nueva animación pendular suave - como una campanita real colgando */
@keyframes bell-swing {
  0% {
    transform: rotate(0deg);
  }
  15% {
    transform: rotate(-12deg);
  }
  30% {
    transform: rotate(8deg);
  }
  45% {
    transform: rotate(-5deg);
  }
  60% {
    transform: rotate(3deg);
  }
  75% {
    transform: rotate(-1deg);
  }
  90% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(0deg);
  }
}

/* Efecto de fade para vista previa de medios en notificaciones */
.notification-media-preview {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  height: 50% !important; /* Forzar altura a solo 50% */
}

/* Ajustar aspect ratio para que solo muestre la mitad */
.notification-media-preview.aspect-video {
  aspect-ratio: 16 / 4.5 !important; /* Cambiar aspect ratio para mostrar solo mitad */
}

/* Posicionar imagen/video para mostrar la parte superior */
.notification-media-preview img,
.notification-media-preview video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 200% !important; /* Hacer el contenido el doble de alto */
  object-fit: cover;
  object-position: top; /* Alinear al top */
}

/* Overlay sólido para garantizar que no se vea nada debajo */
.notification-media-preview::after {
  content: '';
  position: absolute;
  bottom: -1px; /* Ligeramente debajo para cubrir cualquier pixel residual */
  left: -1px;
  right: -1px;
  height: 10px;
  background: #ffffff;
  z-index: 30;
  pointer-events: none;
}

/* Efecto de desvanecido desde la parte inferior - SOLO para contenido multimedia */
.notification-media-preview.notification-has-media::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 40%;
  background: linear-gradient(to top, 
    rgba(255,255,255,1) 0%,
    rgba(255,255,255,0.95) 15%,
    rgba(255,255,255,0.85) 25%,
    rgba(255,255,255,0.7) 35%,
    rgba(255,255,255,0.5) 45%,
    rgba(255,255,255,0.3) 55%,
    rgba(255,255,255,0.15) 70%,
    rgba(255,255,255,0.05) 85%,
    transparent 100%
  );
  z-index: 25;
  pointer-events: none;
  /* Agregar un blur sutil para hacer el efecto más suave */
  filter: blur(0.5px);
}

/* Variante adicional con radial gradient - SOLO para contenido multimedia */
.notification-media-preview.notification-has-media::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: -2px;
  right: -2px;
  height: 25%;
  background: radial-gradient(ellipse at center bottom, 
    rgba(255,255,255,0.9) 0%,
    rgba(255,255,255,0.6) 40%,
    rgba(255,255,255,0.3) 70%,
    transparent 100%
  );
  z-index: 26;
  pointer-events: none;
}

/* Primera capa de humo - Movimiento fluido y continuo */
@keyframes smoke-drift-1 {
  0% {
    transform: translate3d(-20%, -3%, 0) rotate(0deg) scale(0.9);
    opacity: 0.9;
    filter: blur(0.6px);
  }
  25% {
    transform: translate3d(10%, 2%, 0) rotate(90deg) scale(1.1);
    opacity: 1;
    filter: blur(0.8px);
  }
  50% {
    transform: translate3d(40%, -2%, 0) rotate(180deg) scale(0.95);
    opacity: 0.95;
    filter: blur(1px);
  }
  75% {
    transform: translate3d(70%, 3%, 0) rotate(270deg) scale(1.05);
    opacity: 0.8;
    filter: blur(1.2px);
  }
  100% {
    transform: translate3d(100%, -1%, 0) rotate(360deg) scale(0.8);
    opacity: 0.6;
    filter: blur(1.5px);
  }
}

/* Segunda capa de humo - Movimiento en contrafase */
@keyframes smoke-drift-2 {
  0% {
    transform: translate3d(30%, 4%, 0) rotate(0deg) scale(0.8);
    opacity: 0.7;
    filter: blur(1px);
  }
  25% {
    transform: translate3d(5%, -1%, 0) rotate(-90deg) scale(1.2);
    opacity: 0.9;
    filter: blur(1.2px);
  }
  50% {
    transform: translate3d(-20%, 3%, 0) rotate(-180deg) scale(0.9);
    opacity: 1;
    filter: blur(1.4px);
  }
  75% {
    transform: translate3d(-45%, -2%, 0) rotate(-270deg) scale(1.1);
    opacity: 0.7;
    filter: blur(1.6px);
  }
  100% {
    transform: translate3d(-70%, 2%, 0) rotate(-360deg) scale(0.7);
    opacity: 0.5;
    filter: blur(1.8px);
  }
}

/* Eliminamos la animación del contenedor - solo se queda fijo */

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
  
  .space-y-1 > * + * {
    margin-top: 0.2rem;
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
  
  .space-y-1 > * + * {
    margin-top: 0.15rem;
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

/* Responsividad para el botón profesional - mantener alineación derecha */
@media (max-width: 480px) {
  .professional-button,
  .liquid-glass-button {
    padding: 0.375rem 0.75rem !important;
    font-size: 0.625rem !important;
    border-radius: 0.375rem !important;
    /* Remover margin auto para mantener alineación derecha */
    margin-left: auto !important;
  }
  
  .professional-button svg,
  .liquid-glass-button svg {
    width: 0.625rem !important;
    height: 0.625rem !important;
  }
  
  .professional-button span,
  .liquid-glass-button span {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 0.25rem !important;
  }
}

@media (max-width: 375px) {
  .professional-button,
  .liquid-glass-button {
    padding: 0.3rem 0.6rem !important;
    font-size: 0.55rem !important;
    border-radius: 0.3rem !important;
    /* Remover margin auto para mantener alineación derecha */
    margin-left: auto !important;
  }
  
  .professional-button svg,
  .liquid-glass-button svg {
    width: 0.55rem !important;
    height: 0.55rem !important;
  }
  
  .professional-button span,
  .liquid-glass-button span {
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

/* =================================
   ESTILOS PARA MODAL PROFESIONAL TIPO NOTICIA
   ================================= */

/* Modal principal con animaciones suaves y tamaño fijo - más ancho, altura moderada */
.news-modal {
  animation: modalSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(0, 0, 0, 0.05);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  /* Tamaño más ancho, altura reducida */
  height: 85vh;
  max-height: 720px;
  min-height: 520px;
  width: 95vw;
  max-width: 900px;
  min-width: 320px;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Header estilo periódico profesional */
.news-header {
  background: linear-gradient(135deg, 
    #1e293b 0%, 
    #334155 25%, 
    #475569 50%, 
    #334155 75%, 
    #1e293b 100%);
  background-size: 300% 300%;
  animation: headerGradient 8s ease infinite;
  position: relative;
}

@keyframes headerGradient {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

/* Patrón de periódico sutil */
.bg-newspaper-pattern {
  background-image: 
    linear-gradient(45deg, transparent 35%, rgba(255,255,255,.1) 35%, rgba(255,255,255,.1) 65%, transparent 65%),
    linear-gradient(-45deg, transparent 35%, rgba(255,255,255,.05) 35%, rgba(255,255,255,.05) 65%, transparent 65%);
  background-size: 20px 20px;
}

/* Título estilo periódico */
.news-title {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Inter', 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.2;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  letter-spacing: -0.025em;
  font-weight: 600;
}

.news-subtitle {
  font-family: 'Inter', sans-serif;
  font-style: italic;
  opacity: 0.9;
  line-height: 1.4;
}

/* Botón cerrar mejorado */
.close-button {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  margin-top: -4px; /* Subir el botón un poquito más arriba */
}

.close-button:hover {
  transform: rotate(90deg) scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Contenido del artículo con scroll interno */
.news-content {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  line-height: 1.7;
  color: #374151;
  /* Scroll interno sin altura máxima específica - se ajusta al contenedor flex */
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(34, 197, 94, 0.3) transparent;
}

.news-content::-webkit-scrollbar {
  width: 6px;
}

.news-content::-webkit-scrollbar-track {
  background: transparent;
}

.news-content::-webkit-scrollbar-thumb {
  background-color: rgba(34, 197, 94, 0.3);
  border-radius: 3px;
}

.news-content::-webkit-scrollbar-thumb:hover {
  background-color: rgba(34, 197, 94, 0.5);
}

/* Entradilla/Lead del artículo - optimizado */
.news-lead {
  position: relative;
  margin: 0 -4px; /* Aprovecha más el ancho disponible */
}

.news-lead p {
  font-size: 1em;
  line-height: 1.5;
  position: relative;
  margin: 0; /* Elimina márgenes extra */
}

.news-lead::before {
  content: '"';
  position: absolute;
  left: -8px;
  top: -8px;
  font-size: 3rem;
  color: #10b981;
  opacity: 0.3;
  font-family: serif;
  z-index: -1;
}

/* Imagen destacada estilo revista - tamaño reducido */
.news-featured-image {
  position: relative;
  max-width: 100%; /* Permitir ancho completo para imágenes grandes */
  margin: 0 auto; /* Centra la imagen */
}

.news-featured-image img {
  max-height: 70vh; /* Máximo 70% de la altura de la ventana */
  filter: contrast(1.02) saturate(1.05);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  background-color: #ffffff !important; /* Forzar fondo blanco */
}

.news-featured-image:hover img {
  filter: contrast(1.05) saturate(1.1);
}

/* Video embebido profesional - tamaño reducido */
.news-video {
  max-width: 85%;
  margin: 0 auto;
}

.news-video video {
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.news-video:hover video {
  transform: translateY(-2px);
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.2);
}

/* Archivo adjunto estilo profesional */
.news-attachment {
  position: relative;
}

.news-attachment::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(to bottom, #10b981, #059669);
  border-radius: 2px;
}

/* Enlaces relacionados - Diseño compacto */
.news-related-link {
  position: relative;
}

/* === DISEÑO EMPRESARIAL MODERNO PARA ENLACES === */
/* Inspirado en Slack, GitHub, Notion y Microsoft Teams */

.enterprise-link-section {
  margin: 8px 0;
}

.link-section-title {
  font-size: 11px;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
  padding-left: 2px;
}

.enterprise-link-card {
  background: linear-gradient(135deg, #0f766e 0%, #1e40af 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 8px 12px;
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 3px 10px rgba(15, 118, 110, 0.2);
  overflow: hidden;
  max-width: 280px;
  margin: 0 auto;
}

.enterprise-link-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.1) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.enterprise-link-card:hover::before {
  opacity: 1;
}

.enterprise-link-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(15, 118, 110, 0.3);
  border-color: rgba(255, 255, 255, 0.2);
}

.link-header {
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
  z-index: 2;
}

.link-icon-container {
  background: rgba(255, 255, 255, 0.15);
  border-radius: 6px;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.link-icon {
  width: 12px;
  height: 12px;
  color: #ffffff;
  stroke-width: 2.5;
}

.link-content {
  flex: 1;
  min-width: 0;
}

.link-url-display {
  font-size: 10px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.85);
  line-height: 1.3;
  word-break: break-all;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.enterprise-action-btn {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  padding: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  transition: all 0.2s ease;
  flex-shrink: 0;
  backdrop-filter: blur(10px);
}

.enterprise-action-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.4);
  transform: translateX(1px);
}

.enterprise-action-btn:active {
  transform: translateX(0) scale(0.95);
}

.action-icon {
  width: 12px;
  height: 12px;
  color: #ffffff;
  stroke-width: 2.5;
}

/* === ESTILOS ANTIGUOS DE ENLACES ELIMINADOS === */
/* Reemplazados por el nuevo diseño empresarial arriba */

.link-url-preview {
  font-size: 0.6875rem;
  color: #64748b;
  margin-top: 0.25rem;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  background: rgba(100, 116, 139, 0.1);
  padding: 0.125rem 0.25rem;
  border-radius: 3px;
  display: inline-block;
  max-width: fit-content;
}

/* Responsividad para el enlace compacto */
@media (max-width: 480px) {
  .link-compact-content {
    padding: 0.5rem;
  }
  
  .link-icon-mini {
    width: 1rem;
    height: 1rem;
  }
  
  .link-icon-mini svg {
    width: 0.75rem;
    height: 0.75rem;
  }
  
  .link-mini-label {
    font-size: 0.6875rem;
  }
  
  .link-mini-btn {
    padding: 0.1875rem 0.375rem;
    font-size: 0.625rem;
  }
  
  .link-mini-btn svg {
    width: 0.625rem;
    height: 0.625rem;
  }
  
  .link-url-preview {
    font-size: 0.625rem;
    margin-top: 0.1875rem;
  }
}

/* Footer del artículo */
.news-footer {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-top: 2px solid #e2e8f0;
  position: relative;
}

.news-footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, #10b981, transparent);
}

/* Animaciones para elementos interactivos */
.news-modal button {
  position: relative;
  overflow: hidden;
}

.news-modal button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: all 0.6s;
}

.news-modal button:hover::before {
  left: 100%;
}

/* Efectos de carga mejorados */
.news-content .image-placeholder {
  background: linear-gradient(-90deg, #f7fafc 0%, #edf2f7 50%, #f7fafc 100%);
  background-size: 400% 400%;
  animation: shimmerNews 2s ease-in-out infinite;
}

@keyframes shimmerNews {
  0% { background-position: 0% 0%; }
  100% { background-position: -200% 0%; }
}

/* Responsividad para el modal profesional - Tamaños balanceados */
@media (max-width: 640px) {
  .news-modal {
    margin: 0.75rem;
    height: 80vh;
    max-height: 620px;
    min-height: 450px;
    border-radius: 1rem;
    width: calc(100vw - 1.5rem);
    max-width: calc(100vw - 1.5rem);
  }
  
  .news-header {
    padding: 0.5rem;
  }
  
  .news-title {
    font-size: 0.875rem;
    line-height: 1.3;
  }
  
  .news-subtitle {
    font-size: 0.75rem;
  }
  
  .news-content {
    padding: 0.75rem;
  }
  
  .news-footer {
    padding: 0.5rem;
  }
  
  .news-lead p {
    font-size: 0.75rem;
    padding: 0.5rem;
  }
  
  .news-featured-image img {
    max-height: 50vh; /* 50% de altura en pantallas medianas */
  }
}

@media (max-width: 480px) {
  .news-modal {
    margin: 0.5rem;
    height: 78vh;
    max-height: 580px;
    min-height: 400px;
    border-radius: 0.75rem;
    width: calc(100vw - 1rem);
    max-width: calc(100vw - 1rem);
  }
  
  .news-header {
    padding: 0.5rem;
  }
  
  .news-title {
    font-size: 0.8125rem;
    line-height: 1.25;
  }
  
  .news-subtitle {
    font-size: 0.6875rem;
  }
  
  .news-content {
    padding: 0.5rem;
  }
  
  .news-footer {
    padding: 0.5rem;
  }
  
  .news-lead p {
    font-size: 0.6875rem;
    padding: 0.5rem;
  }
  
  .news-featured-image img {
    max-height: 40vh; /* 40% de altura en pantallas pequeñas */
  }
}

/* Dispositivos extra pequeños - altura moderada */
@media (max-width: 360px) {
  .news-modal {
    margin: 0.25rem;
    height: 76vh;
    max-height: 520px;
    min-height: 360px;
    width: calc(100vw - 0.5rem);
    max-width: calc(100vw - 0.5rem);
  }
  
  .news-header {
    padding: 0.375rem;
  }
  
  .news-content {
    padding: 0.5rem;
  }
  
  .news-footer {
    padding: 0.375rem;
  }
  
  .news-title {
    font-size: 0.75rem;
    line-height: 1.2;
  }
  
  .news-subtitle {
    font-size: 0.625rem;
  }
  
  .news-lead p {
    font-size: 0.625rem;
    padding: 0.5rem;
  }
  
  .news-featured-image img {
    max-height: 30vh; /* 30% de altura en pantallas muy pequeñas */
  }
}

/* Tablets - más ancho */
@media (min-width: 641px) and (max-width: 1024px) {
  .news-modal {
    width: 90vw;
    max-width: 800px;
  }
}

/* Desktop - más ancho */
@media (min-width: 1025px) {
  .news-modal {
    width: 85vw;
    max-width: 900px;
  }
}

@media (max-height: 700px) {
  .news-modal {
    height: 78vh;
    max-height: 540px;
    min-height: 420px;
  }
}

@media (max-height: 600px) {
  .news-modal {
    height: 72vh;
    max-height: 480px;
    min-height: 380px;
    margin: 0.5rem;
  }
  
  .news-header {
    padding: 0.375rem;
  }
  
  .news-content {
    padding: 0.5rem;
  }
  
  .news-footer {
    padding: 0.375rem;
  }
}

@media (max-height: 500px) {
  .news-modal {
    height: 68vh;
    max-height: 420px;
    min-height: 340px;
    margin: 0.25rem;
  }
  
  .news-header {
    padding: 0.25rem;
  }
  
  .news-content {
    padding: 0.375rem;
  }
  
  .news-footer {
    padding: 0.25rem;
  }
  
  .news-title {
    font-size: 0.75rem !important;
  }
  
  .news-subtitle {
    font-size: 0.625rem !important;
  }
  
  .news-lead p {
    font-size: 0.625rem !important;
    padding: 0.375rem !important;
  }
}

/* Mejoras para accesibilidad y contraste */
@media (prefers-reduced-motion: reduce) {
  .news-modal,
  .news-header,
  .news-modal button,
  .news-featured-image img,
  .news-video video,
  .close-button {
    animation: none;
    transition: none;
  }
}

/* Modo oscuro (opcional para futuras implementaciones) */
@media (prefers-color-scheme: dark) {
  .news-modal {
    background: #1f2937;
    color: #f9fafb;
  }
  
  .news-content {
    color: #e5e7eb;
  }
  
  .news-lead p {
    background: rgba(31, 41, 55, 0.8);
    border-color: #10b981;
  }
  
  .news-footer {
    background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
    border-color: #374151;
  }
}

/* Efectos adicionales para elementos interactivos */
.news-modal a {
  transition: all 0.2s ease;
  position: relative;
}

.news-modal a::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: currentColor;
  transition: width 0.3s ease;
}

.news-modal a:hover::after {
  width: 100%;
}

/* Sombras y profundidad mejoradas */
.news-attachment,
.news-related-link {
  box-shadow: 
    0 4px 6px rgba(0, 0, 0, 0.05),
    0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.news-attachment:hover,
.news-related-link:hover {
  box-shadow: 
    0 8px 25px rgba(0, 0, 0, 0.1),
    0 4px 10px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

/* Estado de carga y error para imágenes en el modal */
.news-featured-image .image-placeholder {
  min-height: 200px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

/* Placeholders para vista previa con animación de carga */
.notification-media-preview .image-placeholder,
.notification-media-preview .video-placeholder {
  background: linear-gradient(90deg, #f9f9f9 25%, #f0f0f0 50%, #f9f9f9 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  transition: opacity 0.3s ease;
  opacity: 1;
}

/* Ocultamiento suave del placeholder */
.notification-media-preview .image-placeholder[style*="opacity: 0"],
.notification-media-preview .video-placeholder[style*="opacity: 0"] {
  opacity: 0 !important;
}

/* Estado de carga para videos */
.notification-media-preview video[preload="metadata"] + .video-placeholder {
  opacity: 1;
  pointer-events: none;
}

/* Video cargado exitosamente - ocultar placeholder */
.notification-media-preview video[data-loaded="true"] + .video-placeholder {
  opacity: 0;
  transition: opacity 0.3s ease;
}

/* Animación de carga suave */
@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* Optimización de carga de imágenes y videos */
.notification-media-preview img,
.notification-media-preview video {
  opacity: 0;
  transition: opacity 0.3s ease;
}

.notification-media-preview img[loading="lazy"],
.notification-media-preview video[preload="metadata"] {
  opacity: 1;
}

/* Videos que han cargado metadatos exitosamente */
.notification-media-preview video:not([error]) {
  opacity: 1;
}

/* Icono de play para videos */
.video-play-overlay {
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 10;
}

.notification-media-preview:hover .video-play-overlay {
  opacity: 1;
}

.video-play-icon {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  transition: all 0.3s ease;
}

.notification-media-preview:hover .video-play-icon {
  transform: scale(1.1);
}

.video-play-icon svg {
  transition: all 0.3s ease;
}

/* Icono de play siempre visible pero muy sutil */
.notification-media-preview .video-play-overlay {
  opacity: 0.6;
}

.notification-media-preview:hover .video-play-overlay {
  opacity: 1;
}

/* Print styles para cuando el usuario quiera imprimir */
@media print {
  .news-modal {
    position: static !important;
    box-shadow: none !important;
    background: white !important;
    border-radius: 0 !important;
    max-height: none !important;
    width: 100% !important;
    max-width: none !important;
  }
  
  .close-button,
  .news-footer button {
    display: none !important;
  }
  
  .news-header {
    background: #1e293b !important;
    print-color-adjust: exact;
  }
}

/* =================================
   ESTILOS PARA MODAL DE ARCHIVOS
   ================================= */

/* Modal principal para archivos */
.file-viewer-modal {
  animation: modalSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(0, 0, 0, 0.05);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

/* Header del modal de archivos */
.file-header {
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

/* Contenido del archivo */
.file-content {
  background: #f8fafc;
}

/* Estilos para iframe de PDF */
.file-content iframe {
  background: white;
  box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.1);
}

/* Footer del modal */
.file-footer {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-top: 1px solid #e2e8f0;
}

/* Botones del modal de archivos */
.file-footer button,
.file-footer a {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.file-footer button:hover,
.file-footer a:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* Responsividad para modal de archivos */
@media (max-width: 640px) {
  .file-viewer-modal {
    margin: 0.5rem;
    height: 85vh;
    border-radius: 1rem;
    width: calc(100vw - 1rem);
    max-width: calc(100vw - 1rem);
  }
  
  .file-header {
    padding: 0.75rem;
  }
  
  .file-header h3 {
    font-size: 1rem;
    max-width: 200px;
  }
  
  .file-footer {
    padding: 0.75rem;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .file-footer > div:last-child {
    justify-content: center;
    width: 100%;
  }
}

@media (max-width: 480px) {
  .file-viewer-modal {
    margin: 0.25rem;
    height: 80vh;
    width: calc(100vw - 0.5rem);
    max-width: calc(100vw - 0.5rem);
  }
  
  .file-header {
    padding: 0.5rem;
  }
  
  .file-header h3 {
    font-size: 0.9rem;
    max-width: 150px;
  }
  
  .file-footer {
    padding: 0.5rem;
  }
  
  .file-footer button,
  .file-footer a {
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
  }
}

/* Estados de carga para archivos */
.file-content iframe {
  opacity: 0;
  transition: opacity 0.3s ease;
}

.file-content iframe[src] {
  opacity: 1;
}

/* Placeholder para archivos que fallan al cargar */
.file-error-placeholder {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  border: 2px dashed #fca5a5;
  color: #dc2626;
}

/* Animaciones para el modal de archivos */
@keyframes fileModalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.file-viewer-modal {
  animation: fileModalSlideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Mejoras de accesibilidad */
.file-header button:focus,
.file-footer button:focus,
.file-footer a:focus {
  outline: none;
  box-shadow: 
    0 0 0 3px rgba(59, 130, 246, 0.3),
    0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Estilos para diferentes tipos de archivos */
.file-content .pdf-viewer {
  background: #ffffff;
  border: 1px solid #e5e7eb;
}

.file-content .image-viewer {
  background: #f9fafb;
  padding: 1rem;
}

.file-content .video-viewer {
  background: #111827;
  padding: 1rem;
}

.file-content .document-viewer {
  background: #ffffff;
  padding: 2rem;
  text-align: center;
}

/* Indicador de tipo de archivo */
.file-type-indicator {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  z-index: 10;
}

/* =================================
   ESTILOS PARA MODAL PROFESIONAL DE NOTIFICACIONES
   ================================= */

/* Header del modal de notificación */
.notification-modal-header {
  position: relative;
  overflow: hidden;
}

/* Contenido del modal */
.notification-modal-content {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  background: #ffffff;
  scrollbar-width: thin;
  scrollbar-color: rgba(16, 185, 129, 0.3) transparent;
}

.notification-modal-content::-webkit-scrollbar {
  width: 6px;
}

.notification-modal-content::-webkit-scrollbar-track {
  background: transparent;
}

.notification-modal-content::-webkit-scrollbar-thumb {
  background-color: rgba(16, 185, 129, 0.3);
  border-radius: 3px;
}

.notification-modal-content::-webkit-scrollbar-thumb:hover {
  background-color: rgba(16, 185, 129, 0.5);
}

/* Sección de descripción */
.notification-description-section {
  position: relative;
}

.notification-description-text {
  font-size: 0.9375rem;
  line-height: 1.75;
  color: #374151;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.notification-description-text p {
  margin-bottom: 0;
}

.notification-description-text p + p {
  margin-top: 0.75rem;
}

.notification-description-text a {
  color: #2563eb;
  text-decoration: underline;
  transition: color 0.2s ease;
}

.notification-description-text a:hover {
  color: #1d4ed8;
}

/* Sección de imagen */
.notification-image-section {
  position: relative;
}

.notification-image-section img {
  max-height: 60vh;
  width: 100%;
  object-fit: contain;
  background: #f9fafb;
}

/* Sección de video */
.notification-video-section video {
  max-height: 60vh;
  width: 100%;
  object-fit: contain;
}

/* Sección de enlace */
.notification-link-card {
  text-decoration: none;
  display: block;
  transition: all 0.3s ease;
}

.notification-link-card:hover {
  transform: translateY(-2px);
}

/* Footer del modal */
.notification-modal-footer {
  position: relative;
}

.notification-modal-footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, #10b981, transparent);
}

/* Responsividad para el modal de notificaciones */
@media (max-width: 640px) {
  .notification-modal-header {
    padding: 1rem !important;
  }
  
  .notification-modal-header h1 {
    font-size: 1.125rem !important;
  }
  
  .notification-modal-content {
    padding: 1rem !important;
  }
  
  .notification-description-text {
    font-size: 0.875rem;
    line-height: 1.625;
  }
  
  .notification-image-section img {
    max-height: 50vh;
  }
  
  .notification-video-section video {
    max-height: 50vh;
  }
  
  .notification-modal-footer {
    padding: 0.75rem 1rem !important;
  }
}

@media (max-width: 480px) {
  .notification-modal-header {
    padding: 0.875rem !important;
  }
  
  .notification-modal-header h1 {
    font-size: 1rem !important;
  }
  
  .notification-modal-header .text-xs {
    font-size: 0.65rem !important;
  }
  
  .notification-modal-content {
    padding: 0.875rem !important;
  }
  
  .notification-description-text {
    font-size: 0.8125rem;
    line-height: 1.5;
  }
  
  .notification-image-section img {
    max-height: 40vh;
  }
  
  .notification-video-section video {
    max-height: 40vh;
  }
  
  .notification-link-section .rounded-xl {
    padding: 0.75rem !important;
  }
  
  .notification-modal-footer {
    padding: 0.625rem 0.875rem !important;
  }
  
  .notification-modal-footer button {
    padding: 0.5rem 0.75rem !important;
    font-size: 0.75rem !important;
  }
}

@media (max-width: 360px) {
  .notification-modal-header {
    padding: 0.75rem !important;
  }
  
  .notification-modal-header h1 {
    font-size: 0.9375rem !important;
  }
  
  .notification-modal-content {
    padding: 0.75rem !important;
  }
  
  .notification-description-text {
    font-size: 0.75rem;
  }
  
  .notification-image-section img,
  .notification-video-section video {
    max-height: 35vh;
  }
}

/* Animaciones para elementos del modal */
.notification-description-section,
.notification-image-section,
.notification-video-section,
.notification-link-section {
  animation: fadeInUp 0.4s ease-out;
  animation-fill-mode: backwards;
}

.notification-image-section {
  animation-delay: 0.1s;
}

.notification-video-section {
  animation-delay: 0.1s;
}

.notification-link-section {
  animation-delay: 0.2s;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mejoras de accesibilidad */
@media (prefers-reduced-motion: reduce) {
  .notification-description-section,
  .notification-image-section,
  .notification-video-section,
  .notification-link-section {
    animation: none;
  }
}

/* Animaciones de apertura del modal con desenfoque */
@keyframes fadeInBlur {
  from {
    opacity: 0;
    backdrop-filter: blur(0px);
  }
  to {
    opacity: 1;
    backdrop-filter: blur(10px);
  }
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.animate-fade-in-blur {
  animation: fadeInBlur 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

.animate-modal-open {
  animation: modalSlideIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}
</style>
