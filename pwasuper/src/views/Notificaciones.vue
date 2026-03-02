<template>
  <div class="apple-notifications-page">
    <!-- Fondo dinámico Apple -->
    <div class="apple-dynamic-bg">
      <div class="apple-gradient-orb apple-orb-1"></div>
      <div class="apple-gradient-orb apple-orb-2"></div>
      <div class="apple-gradient-orb apple-orb-3"></div>
    </div>

    <div class="apple-notifications-container">
      <!-- Header fijo estilo Apple -->
      <div class="apple-header-fixed">
        <div class="apple-header-content">
          <div class="apple-header-card">
            <div class="apple-header-row">
              <div class="apple-header-title-group">
                <h1 class="apple-page-title">Notificaciones</h1>
                <p class="apple-page-subtitle">Mantente al día con tus avisos</p>
              </div>
              <button 
                @click="refrescarNotificaciones"
                :disabled="cargando"
                class="apple-refresh-btn"
                :class="{ 'apple-btn-disabled': cargando }"
              >
                <svg 
                  :class="['apple-refresh-icon', cargando ? 'apple-spinning' : '']"
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
            
            <!-- Badge contador -->
            <div v-if="notificacionesFiltradas.length > 0" class="apple-counter-badge">
              <svg class="apple-badge-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
              </svg>
              <span class="apple-badge-count">{{ notificacionesFiltradas.length }} avisos</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Contenido con scroll -->
      <div class="apple-scroll-container">

        <!-- Estado de carga Apple -->
        <div v-if="cargando" class="apple-loading-card">
          <div class="apple-loading-content">
            <div class="apple-spinner"></div>
            <span class="apple-loading-text">Cargando notificaciones...</span>
          </div>
        </div>

        <!-- Error de conexión Apple -->
        <div v-if="error && !cargando" class="apple-error-card">
          <div class="apple-error-content">
            <div class="apple-error-icon">⚠️</div>
            <h3 class="apple-error-title">Error de Conexión</h3>
            <p class="apple-error-message">{{ error }}</p>
            <button @click="cargarNotificaciones" class="apple-retry-btn">
              Reintentar
            </button>
          </div>
        </div>

        <!-- Contenedor de scroll para notificaciones -->
        <div v-if="!cargando && !error" class="sf-notifications-list">
          <!-- Lista de notificaciones -->
          <div class="sf-notifications-scroll">
            <div v-if="notificacionesFiltradas.length > 0" class="sf-notification-stack">
              
              <!-- NUEVA CARD APPLE STYLE -->
              <article 
                v-for="(notificacion, index) in notificacionesFiltradas" 
                :key="notificacion.id"
                :class="[
                  'sf-card',
                  notificacion.leida ? 'sf-card--read' : 'sf-card--unread'
                ]"
                :style="{ animationDelay: `${index * 0.06}s` }"
                @click="abrirDetalleNotificacion(notificacion)"
              >
                <!-- Punto de notificación no leída -->
                <span v-if="!notificacion.leida" class="sf-unread-dot"></span>
                
                <!-- Contenido de la card -->
                <div class="sf-card-inner">
                  
                  <!-- Icono circular -->
                  <div :class="['sf-icon-circle', notificacion.leida ? 'sf-icon--read' : 'sf-icon--unread']">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                      <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                      <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                    </svg>
                  </div>
                  
                  <!-- Bloque de texto -->
                  <div class="sf-text-block">
                    
                    <!-- Fila superior: título + tiempo/badge -->
                    <div class="sf-top-row">
                      <h3 :class="['sf-title', notificacion.leida ? 'sf-title--read' : 'sf-title--unread']">
                        {{ notificacion.titulo }}
                      </h3>
                      <div class="sf-meta-group">
                        <time :class="['sf-time', notificacion.leida ? 'sf-time--read' : 'sf-time--unread']">
                          {{ formatearFecha(notificacion.fecha_creacion) }}
                        </time>
                        <span :class="['sf-status-pill', notificacion.leida ? 'sf-pill--read' : 'sf-pill--unread']">
                          {{ notificacion.leida ? 'Leída' : 'Nueva' }}
                        </span>
                      </div>
                    </div>
                    
                    <!-- Subtítulo opcional -->
                    <p v-if="notificacion.subtitulo" :class="['sf-subtitle', notificacion.leida ? 'sf-subtitle--read' : 'sf-subtitle--unread']">
                      {{ notificacion.subtitulo }}
                    </p>
                    
                    <!-- Descripción -->
                    <p v-if="notificacion.descripcion && notificacion.descripcion.trim()" 
                       :class="['sf-description', notificacion.leida ? 'sf-desc--read' : 'sf-desc--unread']">
                      {{ notificacion.descripcion }}
                    </p>
                    
                    <!-- Vista previa de imagen -->
                    <div v-if="notificacion.tiene_archivo && esImagen(notificacion.archivo_tipo)" 
                         class="sf-media-preview" 
                         @click.stop="verNotificacionCompleta(notificacion)">
                      <img :src="obtenerUrlArchivo(notificacion.id)" 
                           :alt="notificacion.archivo_nombre"
                           @error="onImageError"
                           @load="onImageLoad"
                           loading="lazy"/>
                    </div>
                    
                    <!-- Vista previa de video -->
                    <div v-else-if="notificacion.tiene_archivo && esVideo(notificacion.archivo_tipo)" 
                         class="sf-media-preview sf-video-preview" 
                         @click.stop="verNotificacionCompleta(notificacion)">
                      <video :src="obtenerUrlArchivo(notificacion.id)"
                             muted
                             preload="metadata"
                             @loadedmetadata="onVideoLoaded"
                             @canplay="onVideoLoaded"
                             @error="onVideoError"/>
                      <div class="sf-play-btn">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="white">
                          <polygon points="9.5,7.5 16.5,12 9.5,16.5"/>
                        </svg>
                      </div>
                    </div>
                    
                    <!-- Archivo adjunto otro tipo -->
                    <div v-else-if="notificacion.tiene_archivo" class="sf-attachment">
                      <span class="sf-attachment-icon">📎</span>
                      <span class="sf-attachment-name">Archivo adjunto</span>
                      <span class="sf-attachment-type">{{ notificacion.archivo_tipo }}</span>
                    </div>

                  </div>
                  
                  <!-- Chevron derecho -->
                  <div class="sf-chevron">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="9 18 15 12 9 6"/>
                    </svg>
                  </div>
                  
                </div>
                
              </article>
              <!-- FIN CARD APPLE STYLE -->
              
            </div>
            <!-- Fin sf-notification-stack -->

            <!-- Estado vacío Apple -->
            <div v-else class="sf-empty-state">
              <div class="sf-empty-icon">📭</div>
              <h3 class="sf-empty-title">Sin notificaciones</h3>
              <p class="sf-empty-message">
                {{ soloRecientes ? 'No hay notificaciones recientes' : 'No tienes notificaciones por el momento' }}
              </p>
              <button 
                v-if="soloRecientes"
                @click="toggleSoloRecientes"
                class="sf-empty-btn"
              >
                Ver todas las notificaciones
              </button>
            </div>
          </div>
          <!-- Fin del sf-notifications-scroll -->

          <!-- Botón cargar más Apple -->
          <div v-if="puedeCargarMas" class="sf-load-more">
            <button 
              @click="cargarMasNotificaciones"
              :disabled="cargandoMas"
              class="sf-load-more-btn"
            >
              {{ cargandoMas ? 'Cargando...' : 'Cargar más' }}
            </button>
          </div>
        </div>
        <!-- Fin del sf-notifications-list -->
      </div>
      <!-- Fin del apple-scroll-container -->
    </div>
    <!-- Fin del apple-notifications-container -->

    <!-- Modal de detalle de notificación - Apple Design System -->
    <teleport to="body">
      <Transition name="sf-modal-backdrop">
        <div v-if="notificacionSeleccionada" 
             class="sf-modal-overlay"
             @click="cerrarDetalleNotificacion">
          
          <Transition name="sf-modal-content" appear>
            <article class="sf-modal" @click.stop>
              
              <!-- Botón cerrar estilo Apple -->
              <button 
                @click="cerrarDetalleNotificacion"
                class="sf-modal-close"
                aria-label="Cerrar"
              >
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
              
              <!-- Header del modal -->
              <header class="sf-modal-header">
                <div class="sf-modal-header-inner">
                  
                  <!-- Icono y meta -->
                  <div class="sf-modal-meta">
                    <div class="sf-modal-icon">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                        <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                      </svg>
                    </div>
                    <span class="sf-modal-label">Notificación</span>
                    <span class="sf-modal-separator">•</span>
                    <time class="sf-modal-time">{{ formatearFecha(notificacionSeleccionada.fecha_creacion) }}</time>
                  </div>
                  
                  <!-- Badge de estado -->
                  <span :class="['sf-modal-badge', notificacionSeleccionada.leida ? 'sf-modal-badge--read' : 'sf-modal-badge--unread']">
                    <span class="sf-modal-badge-dot"></span>
                    {{ notificacionSeleccionada.leida ? 'Leída' : 'Nueva' }}
                  </span>
                  
                </div>
                
                <!-- Título -->
                <h1 class="sf-modal-title">{{ notificacionSeleccionada.titulo }}</h1>
                
                <!-- Subtítulo -->
                <p v-if="notificacionSeleccionada.subtitulo" class="sf-modal-subtitle">
                  {{ notificacionSeleccionada.subtitulo }}
                </p>
                
              </header>
              
              <!-- Contenido scrolleable -->
              <div class="sf-modal-body">
                
                <!-- Vista previa de actividad (si existe) -->
                <section v-if="notificacionSeleccionada.actividad" class="sf-activity-card">
                  <div class="sf-activity-header">
                    <div :class="['sf-activity-icon', 
                      notificacionSeleccionada.actividad.tipo_actividad === 'campo' ? 'sf-activity-icon--campo' : 
                      notificacionSeleccionada.actividad.tipo_actividad === 'gabinete' ? 'sf-activity-icon--gabinete' : 'sf-activity-icon--default'
                    ]">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z"/>
                      </svg>
                    </div>
                    <span class="sf-activity-label">Actividad registrada</span>
                  </div>
                  
                  <div class="sf-activity-content">
                    <!-- Foto -->
                    <div class="sf-activity-photo"
                         :class="{ 'sf-activity-photo--clickable': notificacionSeleccionada.actividad.foto_url }"
                         @click="notificacionSeleccionada.actividad.foto_url && verImagen(getActividadFotoUrl(notificacionSeleccionada.actividad.foto_url))">
                      <img v-if="notificacionSeleccionada.actividad.foto_url"
                           :src="getActividadFotoUrl(notificacionSeleccionada.actividad.foto_url)"
                           alt="Foto actividad"/>
                      <div v-else class="sf-activity-photo-placeholder">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                          <rect x="3" y="3" width="18" height="18" rx="2"/>
                          <circle cx="8.5" cy="8.5" r="1.5"/>
                          <path d="M21 15l-5-5L5 21"/>
                        </svg>
                      </div>
                    </div>
                    
                    <!-- Info -->
                    <div class="sf-activity-info">
                      <div class="sf-activity-row">
                        <span v-if="notificacionSeleccionada.actividad.fecha" class="sf-activity-date">
                          {{ formatearFechaActividad(notificacionSeleccionada.actividad.fecha).split(' - ')[0] }}
                        </span>
                        <span v-if="notificacionSeleccionada.actividad.tipo_actividad" :class="['sf-activity-type', 
                          notificacionSeleccionada.actividad.tipo_actividad === 'campo' ? 'sf-activity-type--campo' : 
                          notificacionSeleccionada.actividad.tipo_actividad === 'gabinete' ? 'sf-activity-type--gabinete' : ''
                        ]">
                          {{ notificacionSeleccionada.actividad.tipo_actividad }}
                        </span>
                      </div>
                      <p v-if="notificacionSeleccionada.actividad.categoria_actividad" class="sf-activity-category">
                        {{ notificacionSeleccionada.actividad.categoria_actividad }}
                      </p>
                      <p v-if="notificacionSeleccionada.actividad.descripcion" class="sf-activity-desc">
                        {{ notificacionSeleccionada.actividad.descripcion }}
                      </p>
                    </div>
                  </div>
                </section>
                
                <!-- Descripción/Mensaje -->
                <section v-if="notificacionSeleccionada.descripcion" class="sf-message-section">
                  <div class="sf-message-content" v-html="formatearDescripcion(notificacionSeleccionada.descripcion)"></div>
                </section>
                
                <!-- Vista previa de imagen -->
                <section v-if="notificacionSeleccionada.tiene_archivo && esImagen(notificacionSeleccionada.archivo_tipo)" class="sf-image-section">
                  <div class="sf-image-container" @click="abrirArchivo(notificacionSeleccionada.id)">
                    <img 
                      :src="obtenerUrlArchivo(notificacionSeleccionada.id)"
                      :alt="notificacionSeleccionada.archivo_nombre"
                      class="sf-image-preview"
                      @error="onImageError"
                      @load="onImageLoad"
                      loading="eager"
                    />
                    <div class="sf-image-overlay">
                      <div class="sf-image-action">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M15 3h6v6M14 10l6.1-6.1M9 21H3v-6M10 14l-6.1 6.1"/>
                        </svg>
                        <span>Ampliar imagen</span>
                      </div>
                    </div>
                  </div>
                  <p class="sf-image-name">{{ notificacionSeleccionada.archivo_nombre }}</p>
                </section>
                
                <!-- Vista previa de video -->
                <section v-else-if="notificacionSeleccionada.tiene_archivo && esVideo(notificacionSeleccionada.archivo_tipo)" class="sf-video-section">
                  <div class="sf-video-container">
                    <video 
                      :src="obtenerUrlArchivo(notificacionSeleccionada.id)"
                      controls
                      preload="metadata"
                      class="sf-video-player"
                    ></video>
                  </div>
                  <p class="sf-video-name">{{ notificacionSeleccionada.archivo_nombre }}</p>
                </section>
                
                <!-- Archivo adjunto (otros tipos) -->
                <section v-else-if="notificacionSeleccionada.tiene_archivo" class="sf-file-section">
                  <div class="sf-file-card">
                    <div class="sf-file-icon" :style="{ backgroundColor: obtenerColorTipoArchivo(notificacionSeleccionada.archivo_tipo) }">
                      <span>{{ obtenerInicialesTipoArchivo(notificacionSeleccionada.archivo_tipo) }}</span>
                    </div>
                    <div class="sf-file-info">
                      <h4 class="sf-file-name">{{ notificacionSeleccionada.archivo_nombre }}</h4>
                      <p class="sf-file-type">{{ notificacionSeleccionada.archivo_tipo.toUpperCase() }}</p>
                    </div>
                    
                    <!-- Botón de descarga -->
                    <button 
                      v-if="!notificacionSeleccionada.estadoDescarga"
                      @click="abrirArchivo(notificacionSeleccionada.id)"
                      class="sf-download-btn"
                    >
                      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                        <polyline points="7,10 12,15 17,10"/>
                        <line x1="12" y1="15" x2="12" y2="3"/>
                      </svg>
                      <span>Descargar</span>
                    </button>
                    
                    <!-- Estado: Descargando -->
                    <div v-else-if="notificacionSeleccionada.estadoDescarga === 'descargando'" class="sf-download-progress">
                      <div class="sf-progress-ring">
                        <svg viewBox="0 0 36 36">
                          <circle cx="18" cy="18" r="16" fill="none" stroke="currentColor" stroke-width="2" opacity="0.2"/>
                          <circle cx="18" cy="18" r="16" fill="none" stroke="currentColor" stroke-width="2" 
                                  :stroke-dasharray="100" 
                                  :stroke-dashoffset="100 - (notificacionSeleccionada.progresoDescarga || 0)"
                                  transform="rotate(-90 18 18)"/>
                        </svg>
                        <span>{{ notificacionSeleccionada.progresoDescarga }}%</span>
                      </div>
                    </div>
                    
                    <!-- Estado: Completado -->
                    <div v-else-if="notificacionSeleccionada.estadoDescarga === 'completado'" class="sf-download-complete">
                      <button @click="verArchivoDescargado()" class="sf-open-btn">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                          <polyline points="15,3 21,3 21,9"/>
                          <line x1="10" y1="14" x2="21" y2="3"/>
                        </svg>
                        Abrir
                      </button>
                    </div>
                    
                    <!-- Estado: Error -->
                    <button 
                      v-else-if="notificacionSeleccionada.estadoDescarga === 'error'"
                      @click="abrirArchivo(notificacionSeleccionada.id)"
                      class="sf-retry-btn"
                    >
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M1 4v6h6M23 20v-6h-6"/>
                        <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"/>
                      </svg>
                      Reintentar
                    </button>
                  </div>
                </section>
                
                <!-- Enlace externo -->
                <section v-if="notificacionSeleccionada.enlace_url" class="sf-link-section">
                  <a :href="notificacionSeleccionada.enlace_url" 
                     target="_blank" 
                     rel="noopener noreferrer"
                     class="sf-link-card">
                    <div class="sf-link-icon">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                        <polyline points="15,3 21,3 21,9"/>
                        <line x1="10" y1="14" x2="21" y2="3"/>
                      </svg>
                    </div>
                    <div class="sf-link-info">
                      <span class="sf-link-label">Abrir enlace externo</span>
                      <span class="sf-link-url">{{ formatearEnlaceLegible(notificacionSeleccionada.enlace_url) }}</span>
                    </div>
                    <svg class="sf-link-chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="9,18 15,12 9,6"/>
                    </svg>
                  </a>
                </section>
                
              </div>
              
              <!-- Footer -->
              <footer class="sf-modal-footer">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12,6 12,12 16,14"/>
                </svg>
                <span>Recibido {{ formatearFecha(notificacionSeleccionada.fecha_creacion) }}</span>
              </footer>
              
            </article>
          </Transition>
          
        </div>
      </Transition>
    </teleport>

    <!-- Modal para visualizar imagen - Apple Photos Style -->
    <teleport to="body">
      <Transition name="sf-image-modal">
        <div v-if="imagenModalVisible" 
             class="sf-fullscreen-overlay"
             @click="imagenModalVisible = false">
          
          <!-- Close button - Apple style -->
          <button class="sf-fullscreen-close" @click.stop="imagenModalVisible = false">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
          
          <!-- Image container - no distortion -->
          <div class="sf-fullscreen-image-wrap" @click.stop>
            <img 
              :src="imagenSeleccionada" 
              class="sf-fullscreen-image" 
              alt="Imagen ampliada"
              @load="(e) => e.target.classList.add('loaded')"
            />
          </div>
          
        </div>
      </Transition>
    </teleport>
  </div>
  <!-- Fin del apple-notifications-page -->
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import notificacionesService from '../services/notificacionesService.js'
import { apiService } from '../services/apiService.js'
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

// Variable para la URL de la API (para construir URLs de fotos)
const currentApiUrl = ref('')

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

// Función para construir URL completa de foto de actividad
const getActividadFotoUrl = (fotoUrl) => {
  if (!fotoUrl) return null
  
  // Si ya es una URL completa (http:// o https://), devolverla directamente
  if (fotoUrl.startsWith('http://') || fotoUrl.startsWith('https://')) {
    return fotoUrl
  }
  
  // Si es una ruta relativa, agregar el prefijo de la API
  const baseUrl = currentApiUrl.value || ''
  if (baseUrl) {
    // Asegurar que no haya doble barra
    const cleanBase = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl
    const cleanPath = fotoUrl.startsWith('/') ? fotoUrl : `/${fotoUrl}`
    return `${cleanBase}${cleanPath}`
  }
  
  return fotoUrl
}

// Función para formatear la descripción respetando TODOS los saltos de línea
const formatearDescripcion = (texto) => {
  if (!texto) return ''
  
  // Escapar HTML para seguridad
  const escaparHtml = (str) => {
    const div = document.createElement('div')
    div.textContent = str
    return div.innerHTML
  }
  
  let textoFormateado = escaparHtml(texto)
  
  // PASO 1: Normalizar todos los tipos de saltos de línea
  textoFormateado = textoFormateado.replace(/\r\n/g, '\n')
  textoFormateado = textoFormateado.replace(/\r/g, '\n')
  
  // PASO 2: Convertir múltiples saltos (2+) en separador de párrafo doble
  textoFormateado = textoFormateado.replace(/\n{2,}/g, '{{PARRAFO}}')
  
  // PASO 3: Convertir saltos simples en <br> para respetar el formato original
  textoFormateado = textoFormateado.replace(/\n/g, '<br>')
  
  // PASO 4: Limpiar espacios múltiples (pero NO los <br>)
  textoFormateado = textoFormateado.replace(/  +/g, ' ')
  
  // PASO 5: Convertir marcadores de párrafo a HTML con espaciado CSS controlado
  textoFormateado = textoFormateado.replace(/\{\{PARRAFO\}\}/g, '</p><p class="mt-3">')
  
  // PASO 6: Detectar URLs y convertirlas en enlaces
  const urlRegex = /(https?:\/\/[^\s<]+)/g
  textoFormateado = textoFormateado.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer" class="text-orange-600 hover:text-orange-800 underline break-all">$1</a>')
  
  // PASO 7: Detectar texto entre asteriscos como negrita/itálica
  textoFormateado = textoFormateado.replace(/\*\*(.+?)\*\*/g, '<strong class="font-semibold text-gray-900">$1</strong>')
  textoFormateado = textoFormateado.replace(/\*(.+?)\*/g, '<em class="italic">$1</em>')
  
  // PASO 8: Envolver en contenedor de párrafos
  textoFormateado = `<p class="mt-0">${textoFormateado}</p>`
  
  // Limpiar párrafos vacíos
  textoFormateado = textoFormateado.replace(/<p class="mt-\d+">\s*<\/p>/g, '')
  
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
  
  // Inicializar URL de la API para las fotos
  currentApiUrl.value = apiService.getCurrentApiUrl() || ''
  console.log(`🌐 API URL inicializada: ${currentApiUrl.value}`)
  
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
/* ================================================
   ESTILOS APPLE - NOTIFICACIONES
   Sistema de Diseño Liquid Glass
   ================================================ */

/* Página principal */
.apple-notifications-page {
  position: fixed;
  inset: 0;
  background: linear-gradient(145deg, #f5f7fa 0%, #e8ecf3 50%, #f0f4f8 100%);
  overflow: hidden;
  z-index: 0;
}

/* Fondo dinámico con orbes */
.apple-dynamic-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.apple-gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: appleOrbFloat 20s ease-in-out infinite;
}

.apple-orb-1 {
  top: 10%;
  left: 15%;
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.4), rgba(52, 211, 153, 0.3));
  animation-delay: 0s;
}

.apple-orb-2 {
  top: 60%;
  right: 10%;
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.35), rgba(14, 165, 233, 0.25));
  animation-delay: -7s;
}

.apple-orb-3 {
  bottom: 15%;
  left: 25%;
  width: 280px;
  height: 280px;
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.35), rgba(16, 185, 129, 0.25));
  animation-delay: -14s;
}

@keyframes appleOrbFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -20px) scale(1.05); }
  50% { transform: translate(-20px, 30px) scale(0.95); }
  75% { transform: translate(20px, 20px) scale(1.02); }
}

/* Contenedor principal */
.apple-notifications-container {
  position: absolute;
  inset: 0;
  overflow: hidden;
  z-index: 1;
}

/* Header fijo */
.apple-header-fixed {
  position: fixed;
  top: 3.75rem;
  left: 0;
  right: 0;
  z-index: 20;
  padding: 0.625rem 0.75rem;
}

@media (min-width: 640px) {
  .apple-header-fixed {
    top: 4.75rem;
    padding: 0.75rem 1rem;
  }
}

.apple-header-content {
  max-width: 28rem;
  margin: 0 auto;
}

/* Card del header */
.apple-header-card {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.95) 0%, 
    rgba(255, 255, 255, 0.85) 100%);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-radius: 20px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  padding: 0.875rem;
  box-shadow: 
    0 4px 24px rgba(0, 0, 0, 0.06),
    0 1px 4px rgba(0, 0, 0, 0.04);
  animation: appleFadeInScale 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes appleFadeInScale {
  from {
    opacity: 0;
    transform: scale(0.96) translateY(-8px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.apple-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.apple-header-title-group {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.apple-page-title {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
}

.apple-page-subtitle {
  font-size: 0.75rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.45);
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', sans-serif;
}

/* Botón refresh */
.apple-refresh-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.25rem;
  height: 2.25rem;
  background: rgba(16, 185, 129, 0.1);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-refresh-btn:hover {
  background: rgba(16, 185, 129, 0.2);
  transform: scale(1.05);
}

.apple-refresh-btn:active {
  transform: scale(0.95);
}

.apple-btn-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.apple-refresh-icon {
  width: 1.125rem;
  height: 1.125rem;
  color: #059669;
  transition: transform 0.3s ease;
}

.apple-spinning {
  animation: appleSpin 1s linear infinite;
}

@keyframes appleSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Badge contador */
.apple-counter-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.625rem;
  padding-top: 0.625rem;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.apple-badge-icon {
  width: 0.875rem;
  height: 0.875rem;
  color: rgba(0, 0, 0, 0.4);
}

.apple-badge-count {
  font-size: 0.6875rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.6);
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', sans-serif;
}

/* Contenedor de scroll */
.apple-scroll-container {
  position: absolute;
  inset: 0;
  overflow: hidden;
  padding-top: 12rem;
  padding-bottom: 1rem;
}

@media (min-width: 640px) {
  .apple-scroll-container {
    padding-top: 13rem;
  }
}

/* Loading state */
.apple-loading-card {
  max-width: 28rem;
  margin: 0 auto;
  padding: 0 0.75rem;
}

.apple-loading-content {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.apple-spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid rgba(16, 185, 129, 0.2);
  border-top-color: #10b981;
  border-radius: 50%;
  animation: appleSpin 1s linear infinite;
}

.apple-loading-text {
  margin-left: 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.6);
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', sans-serif;
}

/* Error state */
.apple-error-card {
  max-width: 28rem;
  margin: 0 auto;
  padding: 0 0.75rem;
}

.apple-error-content {
  text-align: center;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.apple-error-icon {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
}

.apple-error-title {
  font-size: 1rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
  margin-bottom: 0.5rem;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
}

.apple-error-message {
  font-size: 0.8125rem;
  color: rgba(0, 0, 0, 0.5);
  margin-bottom: 1rem;
}

.apple-retry-btn {
  padding: 0.625rem 1.25rem;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  font-size: 0.8125rem;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.apple-retry-btn:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
}

/* ================================================
   SF NOTIFICATIONS - APPLE DESIGN SYSTEM
   ================================================ */

/* Lista principal */
.sf-notifications-list {
  height: 100%;
  display: flex;
  flex-direction: column;
  max-width: 26rem;
  margin: 0 auto;
  padding: 0 1rem;
}

.sf-notifications-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem 0 1.5rem 0;
  -webkit-overflow-scrolling: touch;
}

.sf-notification-stack {
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
}

/* Animación de entrada */
@keyframes sfSlideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ================================================
   CARD PRINCIPAL - SF STYLE
   ================================================ */

.sf-card {
  position: relative;
  background: #ffffff;
  border-radius: 14px;
  cursor: pointer;
  animation: sfSlideUp 0.45s cubic-bezier(0.25, 0.46, 0.45, 0.94) backwards;
  transition: transform 0.28s cubic-bezier(0.25, 0.46, 0.45, 0.94),
              box-shadow 0.28s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.sf-card:hover {
  transform: translateY(-3px) scale(1.008);
}

.sf-card:active {
  transform: scale(0.985);
}

/* CARD NO LEÍDA - Fondo rojo suave */
.sf-card--unread {
  background: linear-gradient(145deg, #fff5f5 0%, #fef2f2 100%);
  border: 1.5px solid rgba(239, 68, 68, 0.2);
  box-shadow: 
    0 4px 18px rgba(239, 68, 68, 0.1),
    0 1px 3px rgba(239, 68, 68, 0.06);
}

.sf-card--unread:hover {
  border-color: rgba(239, 68, 68, 0.35);
  box-shadow: 
    0 10px 35px rgba(239, 68, 68, 0.15),
    0 4px 12px rgba(239, 68, 68, 0.08);
}

/* CARD LEÍDA - Fondo verde suave */
.sf-card--read {
  background: linear-gradient(145deg, #f0fdf4 0%, #ecfdf5 100%);
  border: 1.5px solid rgba(34, 197, 94, 0.18);
  box-shadow: 
    0 3px 12px rgba(34, 197, 94, 0.06),
    0 1px 3px rgba(0, 0, 0, 0.03);
}

.sf-card--read:hover {
  border-color: rgba(34, 197, 94, 0.32);
  box-shadow: 
    0 8px 28px rgba(34, 197, 94, 0.12),
    0 3px 10px rgba(34, 197, 94, 0.06);
}

/* ================================================
   PUNTO DE NO LEÍDA
   ================================================ */

.sf-unread-dot {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 10px;
  height: 10px;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.45);
  z-index: 5;
  animation: sfPulse 2s ease-in-out infinite;
}

@keyframes sfPulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.15); opacity: 0.85; }
}

/* ================================================
   CONTENIDO INTERNO
   ================================================ */

.sf-card-inner {
  display: flex;
  align-items: flex-start;
  gap: 0.875rem;
  padding: 1rem 1rem 1rem 1.125rem;
}

/* ================================================
   ICONO CIRCULAR
   ================================================ */

.sf-icon-circle {
  flex-shrink: 0;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.25s ease;
}

.sf-card:hover .sf-icon-circle {
  transform: scale(1.06);
}

.sf-icon--unread {
  background: linear-gradient(145deg, rgba(239, 68, 68, 0.15), rgba(220, 38, 38, 0.1));
  color: #dc2626;
}

.sf-icon--read {
  background: linear-gradient(145deg, rgba(34, 197, 94, 0.15), rgba(22, 163, 74, 0.1));
  color: #16a34a;
}

/* ================================================
   BLOQUE DE TEXTO
   ================================================ */

.sf-text-block {
  flex: 1;
  min-width: 0;
}

/* Fila superior */
.sf-top-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 0.25rem;
}

/* Título */
.sf-title {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
  font-size: 0.9375rem;
  font-weight: 600;
  letter-spacing: -0.015em;
  line-height: 1.35;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.sf-title--unread {
  color: rgba(0, 0, 0, 0.92);
}

.sf-title--read {
  color: rgba(0, 0, 0, 0.8);
}

/* Tiempo */
.sf-time {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.6875rem;
  font-weight: 500;
  flex-shrink: 0;
  white-space: nowrap;
  padding-top: 0.125rem;
}

.sf-time--unread {
  color: rgba(0, 0, 0, 0.55);
}

.sf-time--read {
  color: rgba(0, 0, 0, 0.4);
}

/* Grupo de metadata (fecha + badge) */
.sf-meta-group {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.375rem;
  flex-shrink: 0;
}

/* Status Pill - Estilo Apple */
.sf-status-pill {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.5625rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 0.1875rem 0.4375rem;
  border-radius: 4px;
  line-height: 1;
}

.sf-pill--unread {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  box-shadow: 0 1px 4px rgba(239, 68, 68, 0.3);
}

.sf-pill--read {
  background: rgba(34, 197, 94, 0.12);
  color: #15803d;
  border: 1px solid rgba(34, 197, 94, 0.18);
}

/* Subtítulo */
.sf-subtitle {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.75rem;
  font-weight: 500;
  margin: 0.125rem 0 0 0;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.sf-subtitle--unread {
  color: rgba(0, 0, 0, 0.55);
}

.sf-subtitle--read {
  color: rgba(0, 0, 0, 0.42);
}

/* Descripción */
.sf-description {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.8125rem;
  line-height: 1.5;
  margin: 0.5rem 0 0 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.sf-desc--unread {
  color: rgba(0, 0, 0, 0.68);
}

.sf-desc--read {
  color: rgba(0, 0, 0, 0.52);
}

/* ================================================
   VISTA PREVIA MEDIA
   ================================================ */

.sf-media-preview {
  margin-top: 0.75rem;
  border-radius: 10px;
  overflow: hidden;
  position: relative;
  max-width: 100%;
}

.sf-media-preview img,
.sf-media-preview video {
  width: 100%;
  max-height: 180px;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;
}

.sf-media-preview:hover img,
.sf-media-preview:hover video {
  transform: scale(1.02);
}

.sf-video-preview {
  background: #000;
}

.sf-play-btn {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 48px;
  height: 48px;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(10px);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  transition: transform 0.25s ease, background 0.25s ease;
}

.sf-media-preview:hover .sf-play-btn {
  transform: translate(-50%, -50%) scale(1.08);
  background: rgba(0, 0, 0, 0.55);
}

/* Archivo adjunto */
.sf-attachment {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.75rem;
  padding: 0.5rem 0.75rem;
  background: rgba(0, 0, 0, 0.035);
  border-radius: 8px;
}

.sf-attachment-icon {
  font-size: 0.875rem;
}

.sf-attachment-name {
  font-size: 0.75rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.6);
}

.sf-attachment-type {
  font-size: 0.6875rem;
  color: rgba(0, 0, 0, 0.38);
  margin-left: auto;
  text-transform: uppercase;
}

/* ================================================
   CHEVRON DERECHO
   ================================================ */

.sf-chevron {
  flex-shrink: 0;
  color: rgba(0, 0, 0, 0.25);
  align-self: center;
  transition: transform 0.2s ease, color 0.2s ease;
}

.sf-card:hover .sf-chevron {
  transform: translateX(3px);
  color: rgba(0, 0, 0, 0.4);
}

/* ================================================
   BADGE DE ESTADO
   ================================================ */

.sf-badge {
  position: absolute;
  bottom: 0.75rem;
  right: 0.75rem;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.625rem;
  font-weight: 600;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
}

.sf-badge--unread {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.35);
}

.sf-badge--read {
  background: rgba(34, 197, 94, 0.12);
  color: #16a34a;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

/* ================================================
   ESTADO VACÍO
   ================================================ */

.sf-empty-state {
  text-align: center;
  padding: 4rem 1.5rem;
}

.sf-empty-icon {
  font-size: 3.5rem;
  margin-bottom: 1.25rem;
  filter: grayscale(10%);
}

.sf-empty-title {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
  font-size: 1.125rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.78);
  margin: 0 0 0.5rem 0;
}

.sf-empty-message {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.48);
  margin: 0 0 1.5rem 0;
}

.sf-empty-btn {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #059669;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.sf-empty-btn:hover {
  background: rgba(5, 150, 105, 0.08);
  color: #047857;
}

/* ================================================
   CARGAR MÁS
   ================================================ */

.sf-load-more {
  text-align: center;
  padding: 1.25rem 0;
  flex-shrink: 0;
}

.sf-load-more-btn {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  padding: 0.75rem 2rem;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.28s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.25);
}

.sf-load-more-btn:hover:not(:disabled) {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.35);
}

.sf-load-more-btn:active:not(:disabled) {
  transform: scale(0.98);
}

.sf-load-more-btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

/* ================================================
   RESPONSIVIDAD APPLE
   ================================================ */

@media (max-width: 374px) {
  .apple-header-card {
    padding: 0.75rem;
    border-radius: 16px;
  }
  
  .apple-page-title {
    font-size: 1.125rem;
  }
  
  .apple-refresh-btn {
    width: 2rem;
    height: 2rem;
  }
  
  .apple-refresh-icon {
    width: 1rem;
    height: 1rem;
  }
  
  .apple-notification-card {
    border-radius: 14px;
  }
  
  .apple-card-content {
    padding: 0.75rem;
    padding-left: 1rem;
    gap: 0.5rem;
  }
  
  .apple-notification-icon {
    width: 2rem;
    height: 2rem;
    border-radius: 8px;
  }
  
  .apple-notification-icon svg {
    width: 1rem;
    height: 1rem;
  }
  
  .apple-notification-title {
    font-size: 0.875rem;
  }
  
  .apple-notification-date {
    font-size: 0.625rem;
  }
  
  .apple-description-text {
    font-size: 0.75rem;
  }
  
  /* SF Cards responsivo - móvil pequeño */
  .sf-notifications-list {
    padding: 0 0.75rem;
  }
  
  .sf-card-inner {
    padding: 0.875rem;
    gap: 0.625rem;
  }
  
  .sf-icon-circle {
    width: 2.125rem;
    height: 2.125rem;
  }
  
  .sf-icon-circle svg {
    width: 16px;
    height: 16px;
  }
  
  .sf-title {
    font-size: 0.875rem;
  }
  
  .sf-description {
    font-size: 0.75rem;
    -webkit-line-clamp: 2;
  }
  
  .sf-status-pill {
    font-size: 0.5rem;
    padding: 0.125rem 0.3125rem;
  }
  
  .sf-meta-group {
    gap: 0.25rem;
  }
}

@media (min-width: 640px) {
  .apple-header-card {
    padding: 1.25rem;
  }
  
  .apple-page-title {
    font-size: 1.375rem;
  }
  
  .apple-page-subtitle {
    font-size: 0.8125rem;
  }
  
  .apple-notification-stack {
    gap: 1rem;
  }
  
  .apple-card-content {
    padding: 1.25rem;
    padding-left: 1.5rem;
  }
  
  .apple-notification-icon {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 12px;
  }
  
  .apple-notification-icon svg {
    width: 1.25rem;
    height: 1.25rem;
  }
  
  .apple-notification-title {
    font-size: 1rem;
  }
  
  /* SF Cards responsivo - tablet/desktop */
  .sf-notifications-list {
    max-width: 30rem;
    padding: 0 1.25rem;
  }
  
  .sf-notification-stack {
    gap: 1rem;
  }
  
  .sf-card-inner {
    padding: 1.25rem;
    gap: 1rem;
  }
  
  .sf-icon-circle {
    width: 2.75rem;
    height: 2.75rem;
  }
  
  .sf-icon-circle svg {
    width: 22px;
    height: 22px;
  }
  
  .sf-title {
    font-size: 1rem;
  }
  
  .sf-description {
    font-size: 0.875rem;
  }
  
  .sf-media-preview img,
  .sf-media-preview video {
    max-height: 220px;
  }
}

/* ================================================
   ESTILOS LEGACY (mantener compatibilidad)
   ================================================ */

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

/* ================================================
   SF MODAL - APPLE DESIGN SYSTEM (iOS 17 Style)
   ================================================ */

/* Apple Spring Animation Keyframes */
@keyframes sfModalSpring {
  0% { 
    opacity: 0;
    transform: scale(0.85) translateY(30px);
  }
  50% { 
    transform: scale(1.02) translateY(-2px);
  }
  75% {
    transform: scale(0.99) translateY(1px);
  }
  100% { 
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes sfModalOut {
  0% { 
    opacity: 1;
    transform: scale(1) translateY(0);
  }
  100% { 
    opacity: 0;
    transform: scale(0.9) translateY(15px);
  }
}

@keyframes sfIconPulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 8px rgba(16, 185, 129, 0);
  }
}

@keyframes sfShimmer {
  0% { background-position: -200% center; }
  100% { background-position: 200% center; }
}

/* Backdrop overlay - intenso blur tipo Apple */
.sf-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem;
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
}

/* Modal container - iOS 17 card style */
.sf-modal {
  position: relative;
  width: 100%;
  max-width: 28rem;
  max-height: 88vh;
  background: rgba(255, 255, 255, 0.98);
  border-radius: 22px;
  box-shadow: 
    0 30px 70px -10px rgba(0, 0, 0, 0.35),
    0 15px 35px -5px rgba(0, 0, 0, 0.15),
    0 0 0 0.5px rgba(255, 255, 255, 0.6) inset,
    0 0 0 1px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: sfModalSpring 0.32s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  will-change: transform, opacity;
}

@media (min-width: 640px) {
  .sf-modal {
    max-width: 34rem;
    border-radius: 26px;
  }
}

@media (min-width: 768px) {
  .sf-modal {
    max-width: 38rem;
    max-height: 82vh;
  }
}

/* Close button - iOS style - positioned outside header-inner */
.sf-modal-close {
  position: absolute;
  top: 0.625rem;
  right: 0.625rem;
  z-index: 60;
  width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(120, 120, 128, 0.12);
  border: none;
  border-radius: 50%;
  color: rgba(60, 60, 67, 0.6);
  cursor: pointer;
  transition: all 0.12s cubic-bezier(0.4, 0, 0.2, 1);
}

.sf-modal-close:hover {
  background: rgba(120, 120, 128, 0.2);
  color: rgba(60, 60, 67, 0.85);
  transform: scale(1.08);
}

.sf-modal-close:active {
  transform: scale(0.92);
  background: rgba(120, 120, 128, 0.25);
}

/* Modal header - clean Apple style */
.sf-modal-header {
  flex-shrink: 0;
  padding: 1rem 1rem 0.875rem;
  padding-right: 2.5rem; /* Space for close button */
  background: rgba(255, 255, 255, 0.95);
  border-bottom: 0.5px solid rgba(0, 0, 0, 0.08);
}

@media (min-width: 640px) {
  .sf-modal-header {
    padding: 1.25rem 1.25rem 1rem;
    padding-right: 2.75rem;
  }
}

.sf-modal-header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

/* Meta info */
.sf-modal-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Animated notification icon */
.sf-modal-icon {
  width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, #34d399, #10b981);
  border-radius: 7px;
  color: white;
  animation: sfIconPulse 2.5s ease-in-out infinite;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.35);
}

.sf-modal-icon svg {
  filter: drop-shadow(0 1px 1px rgba(0,0,0,0.15));
}

.sf-modal-label {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: rgba(0, 0, 0, 0.45);
}

.sf-modal-separator {
  font-size: 0.5rem;
  color: rgba(0, 0, 0, 0.2);
}

.sf-modal-time {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.6875rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.38);
}

/* Badge - iOS pill style */
.sf-modal-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.2rem 0.5rem;
  border-radius: 100px;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.5625rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  transition: all 0.2s ease;
  flex-shrink: 0;
  white-space: nowrap;
}

.sf-modal-badge-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  flex-shrink: 0;
}

.sf-modal-badge--unread {
  background: linear-gradient(145deg, #fef2f2, #fecaca);
  color: #dc2626;
  box-shadow: 0 1px 3px rgba(220, 38, 38, 0.15);
}

.sf-modal-badge--unread .sf-modal-badge-dot {
  background: #ef4444;
  animation: sfPulse 1.5s ease-in-out infinite;
}

.sf-modal-badge--read {
  background: linear-gradient(145deg, #ecfdf5, #d1fae5);
  color: #059669;
  box-shadow: 0 1px 3px rgba(5, 150, 105, 0.15);
}

.sf-modal-badge--read .sf-modal-badge-dot {
  background: #10b981;
}

/* Title - Apple typography */
.sf-modal-title {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
  font-size: 1.1875rem;
  font-weight: 650;
  letter-spacing: -0.018em;
  line-height: 1.22;
  color: rgba(0, 0, 0, 0.9);
  margin: 0;
}

@media (min-width: 640px) {
  .sf-modal-title {
    font-size: 1.3125rem;
  }
}

/* Subtitle */
.sf-modal-subtitle {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.8125rem;
  font-weight: 400;
  color: rgba(0, 0, 0, 0.48);
  margin: 0.375rem 0 0;
  line-height: 1.45;
}

/* Modal body - smooth scroll */
.sf-modal-body {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 1.125rem;
  -webkit-overflow-scrolling: touch;
  scroll-behavior: smooth;
}

.sf-modal-body::-webkit-scrollbar {
  width: 5px;
}

.sf-modal-body::-webkit-scrollbar-track {
  background: transparent;
}

.sf-modal-body::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.12);
  border-radius: 10px;
}

@media (min-width: 640px) {
  .sf-modal-body {
    padding: 1.375rem;
  }
}

/* Activity card - iOS card style */
.sf-activity-card {
  background: linear-gradient(155deg, #f8fafc, #f1f5f9);
  border: 0.5px solid rgba(0, 0, 0, 0.06);
  border-radius: 16px;
  padding: 1rem;
  margin-bottom: 1rem;
  transition: all 0.2s ease;
}

.sf-activity-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
}

.sf-activity-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.625rem;
}

.sf-activity-icon {
  width: 26px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 7px;
  color: white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

.sf-activity-icon--campo {
  background: linear-gradient(145deg, #34d399, #10b981);
}

.sf-activity-icon--gabinete {
  background: linear-gradient(145deg, #fb923c, #f97316);
}

.sf-activity-icon--default {
  background: linear-gradient(145deg, #9ca3af, #6b7280);
}

.sf-activity-label {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: rgba(0, 0, 0, 0.5);
}

.sf-activity-content {
  display: flex;
  gap: 0.75rem;
}

/* Activity photo - no distortion */
.sf-activity-photo {
  width: 60px;
  height: 60px;
  flex-shrink: 0;
  border-radius: 12px;
  overflow: hidden;
  background: linear-gradient(145deg, #f1f5f9, #e2e8f0);
  position: relative;
}

.sf-activity-photo--clickable {
  cursor: pointer;
  transition: all 0.2s ease;
}

.sf-activity-photo--clickable:hover {
  transform: scale(1.03);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.sf-activity-photo--clickable:hover img {
  transform: scale(1);
}

.sf-activity-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.sf-activity-photo-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(0, 0, 0, 0.2);
  background: linear-gradient(145deg, #f8fafc, #f1f5f9);
}

.sf-activity-info {
  flex: 1;
  min-width: 0;
}

.sf-activity-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.sf-activity-date {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.72);
}

.sf-activity-type {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.5625rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  padding: 0.2rem 0.5rem;
  border-radius: 5px;
}

.sf-activity-type--campo {
  background: linear-gradient(145deg, #d1fae5, #a7f3d0);
  color: #047857;
}

.sf-activity-type--gabinete {
  background: linear-gradient(145deg, #fed7aa, #fdba74);
  color: #c2410c;
}

.sf-activity-category {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.8125rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.82);
  margin: 0.125rem 0 0.25rem;
  line-height: 1.3;
}

.sf-activity-desc {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.75rem;
  color: rgba(0, 0, 0, 0.5);
  margin: 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Message section - Apple quote style */
.sf-message-section {
  margin-bottom: 1rem;
}

.sf-message-content {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.9375rem;
  line-height: 1.7;
  color: rgba(0, 0, 0, 0.75);
  padding: 1rem 1.125rem;
  background: linear-gradient(155deg, rgba(245, 247, 250, 0.9), rgba(255, 255, 255, 0.95));
  border-radius: 14px;
  border-left: 3px solid transparent;
  border-image: linear-gradient(180deg, #10b981, #059669) 1;
  position: relative;
}

.sf-message-content::before {
  content: '"';
  position: absolute;
  top: 0.5rem;
  left: 0.75rem;
  font-family: Georgia, serif;
  font-size: 2.5rem;
  color: rgba(16, 185, 129, 0.15);
  line-height: 1;
}

.sf-message-content p {
  margin: 0;
  text-indent: 1rem;
}

.sf-message-content p:first-child {
  text-indent: 1.5rem;
}

.sf-message-content p + p {
  margin-top: 0.625rem;
}

/* Image section - NO distortion, Apple Photos style */
.sf-image-section {
  margin-bottom: 1rem;
}

.sf-image-container {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  background: linear-gradient(145deg, #f8fafc, #f1f5f9);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 120px;
  max-height: 320px;
  transition: all 0.2s ease;
}

.sf-image-container:hover {
  transform: scale(1.01);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

.sf-image-container:active {
  transform: scale(0.99);
}

/* Image WITHOUT distortion - maintain aspect ratio */
.sf-image-preview {
  width: 100%;
  height: auto;
  max-height: 320px;
  display: block;
  object-fit: contain;
  object-position: center;
  transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.sf-image-container:hover .sf-image-preview {
  transform: scale(1.03);
}

.sf-image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, transparent 40%, rgba(0, 0, 0, 0.6) 100%);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: 1rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.sf-image-container:hover .sf-image-overlay {
  opacity: 1;
}

.sf-image-action {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border-radius: 100px;
  color: rgba(0, 0, 0, 0.85);
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  transition: transform 0.15s ease;
}

.sf-image-action:hover {
  transform: scale(1.03);
}

.sf-image-name {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.6875rem;
  color: rgba(0, 0, 0, 0.4);
  margin: 0.5rem 0 0;
  text-align: center;
}

/* Video section - Apple TV+ style */
.sf-video-section {
  margin-bottom: 1rem;
}

.sf-video-container {
  border-radius: 16px;
  overflow: hidden;
  background: #000;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.sf-video-player {
  width: 100%;
  height: auto;
  display: block;
  aspect-ratio: 16/9;
  object-fit: contain;
  background: #000;
}

.sf-video-name {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.6875rem;
  color: rgba(0, 0, 0, 0.4);
  margin: 0.5rem 0 0;
  text-align: center;
}

/* File section - iOS Files app style */
.sf-file-section {
  margin-bottom: 1rem;
}

.sf-file-card {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 0.875rem 1rem;
  background: linear-gradient(155deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.95));
  border: 0.5px solid rgba(0, 0, 0, 0.08);
  border-radius: 14px;
  transition: all 0.2s ease;
}

.sf-file-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.sf-file-icon {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
  font-size: 0.625rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.sf-file-info {
  flex: 1;
  min-width: 0;
}

.sf-file-name {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.875rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.88);
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sf-file-type {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.6875rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.4);
  margin: 0.125rem 0 0;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

/* Download button - Apple button style */
.sf-download-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 0.875rem;
  background: linear-gradient(145deg, #3b82f6, #2563eb);
  border: none;
  border-radius: 10px;
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.35);
}

.sf-download-btn:hover {
  transform: translateY(-1px) scale(1.02);
  box-shadow: 0 4px 14px rgba(59, 130, 246, 0.45);
}

.sf-download-btn:active {
  transform: scale(0.97);
  box-shadow: 0 1px 4px rgba(59, 130, 246, 0.3);
}

/* Progress indicator - Apple spinner style */
.sf-download-progress {
  display: flex;
  align-items: center;
  justify-content: center;
}

.sf-progress-ring {
  position: relative;
  width: 38px;
  height: 38px;
}

.sf-progress-ring svg {
  transform: rotate(-90deg);
  filter: drop-shadow(0 1px 2px rgba(59, 130, 246, 0.3));
}

.sf-progress-ring circle {
  stroke: #3b82f6;
  stroke-linecap: round;
  transition: stroke-dashoffset 0.2s ease;
}

.sf-progress-ring span {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.5625rem;
  font-weight: 700;
  color: rgba(0, 0, 0, 0.6);
}

/* Open button - success state */
.sf-open-btn {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.45rem 0.75rem;
  background: linear-gradient(145deg, #22c55e, #16a34a);
  border: none;
  border-radius: 8px;
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.7rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
  box-shadow: 0 2px 6px rgba(34, 197, 94, 0.3);
}

.sf-open-btn:hover {
  transform: scale(1.04);
}

.sf-open-btn:active {
  transform: scale(0.97);
}

/* Retry button - error state */
.sf-retry-btn {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.45rem 0.75rem;
  background: linear-gradient(145deg, #ef4444, #dc2626);
  border: none;
  border-radius: 8px;
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.7rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
  box-shadow: 0 2px 6px rgba(239, 68, 68, 0.3);
}

.sf-retry-btn:hover {
  transform: scale(1.04);
}

.sf-retry-btn:active {
  transform: scale(0.97);
}

/* Link section - Safari style */
.sf-link-section {
  margin-bottom: 1rem;
}

.sf-link-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  background: linear-gradient(155deg, #eff6ff, #f0f9ff);
  border: 0.5px solid rgba(59, 130, 246, 0.18);
  border-radius: 14px;
  text-decoration: none;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.sf-link-card:hover {
  border-color: rgba(59, 130, 246, 0.4);
  box-shadow: 0 4px 18px rgba(59, 130, 246, 0.12);
  transform: translateY(-2px);
}

.sf-link-card:active {
  transform: translateY(0) scale(0.99);
}

.sf-link-icon {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, #3b82f6, #2563eb);
  border-radius: 10px;
  color: white;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.35);
}

.sf-link-info {
  flex: 1;
  min-width: 0;
}

.sf-link-label {
  display: block;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.8125rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.88);
}

.sf-link-url {
  display: block;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.65rem;
  color: rgba(0, 0, 0, 0.4);
  margin-top: 0.125rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sf-link-chevron {
  flex-shrink: 0;
  color: rgba(0, 0, 0, 0.25);
  transition: all 0.15s ease;
}

.sf-link-card:hover .sf-link-chevron {
  transform: translateX(4px);
  color: #3b82f6;
}

/* Modal footer - subtle Apple style */
.sf-modal-footer {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.75rem 1rem;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.95) 0%, rgba(249, 250, 251, 0.98) 100%);
  border-top: 0.5px solid rgba(0, 0, 0, 0.06);
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.65rem;
  color: rgba(0, 0, 0, 0.35);
  letter-spacing: 0.01em;
}

.sf-modal-footer svg {
  opacity: 0.6;
}

/* ================================================
   SF MODAL TRANSITIONS - Apple iOS Speed
   ================================================ */

/* Backdrop transition - fast */
.sf-modal-backdrop-enter-active {
  transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
}

.sf-modal-backdrop-leave-active {
  transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
}

.sf-modal-backdrop-enter-from,
.sf-modal-backdrop-leave-to {
  opacity: 0;
}

/* Content transition - spring bounce */
.sf-modal-content-enter-active {
  transition: none;
  animation: sfModalSpring 0.32s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}

.sf-modal-content-leave-active {
  animation: sfModalOut 0.18s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

.sf-modal-content-enter-from,
.sf-modal-content-leave-to {
  opacity: 0;
}

/* ================================================
   SF FULLSCREEN IMAGE MODAL - Apple Photos Style
   ================================================ */

.sf-fullscreen-overlay {
  position: fixed;
  inset: 0;
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.92);
  backdrop-filter: blur(30px) saturate(150%);
  -webkit-backdrop-filter: blur(30px) saturate(150%);
  padding: 1rem;
}

.sf-fullscreen-close {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 10001;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  color: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  transition: all 0.15s ease;
}

.sf-fullscreen-close:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: scale(1.08);
}

.sf-fullscreen-close:active {
  transform: scale(0.95);
}

.sf-fullscreen-image-wrap {
  max-width: 95vw;
  max-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sf-fullscreen-image {
  max-width: 100%;
  max-height: 88vh;
  width: auto;
  height: auto;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  opacity: 0;
  transform: scale(0.95);
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.sf-fullscreen-image.loaded {
  opacity: 1;
  transform: scale(1);
}

/* Fullscreen image modal transitions */
.sf-image-modal-enter-active {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.sf-image-modal-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.sf-image-modal-enter-from {
  opacity: 0;
}

.sf-image-modal-enter-from .sf-fullscreen-image {
  transform: scale(0.85);
}

.sf-image-modal-leave-to {
  opacity: 0;
}

.sf-image-modal-leave-to .sf-fullscreen-image {
  transform: scale(0.9);
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
