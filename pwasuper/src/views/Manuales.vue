<template>
  <div class="apple-manuales-page">
    <!-- Fondo dinámico Apple -->
    <div class="apple-dynamic-bg">
      <div class="apple-gradient-orb apple-orb-1"></div>
      <div class="apple-gradient-orb apple-orb-2"></div>
      <div class="apple-gradient-orb apple-orb-3"></div>
    </div>

    <div class="apple-manuales-container">
      <!-- Header fijo estilo Apple -->
      <div class="apple-header-fixed">
        <div class="apple-header-content">
          <div class="apple-header-card">
            <div class="apple-header-row">
              <div class="apple-header-title-group">
                <h1 class="apple-page-title">Manuales</h1>
                <p class="apple-page-subtitle">Documentos y guías</p>
              </div>
              <button 
                @click="refrescarManuales"
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
            <div v-if="manuales.length > 0" class="apple-counter-badge">
              <svg class="apple-badge-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25"/>
              </svg>
              <span class="apple-badge-count">{{ manuales.length }} documentos</span>
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
            <span class="apple-loading-text">Cargando manuales...</span>
          </div>
        </div>
        
        <!-- Error de conexión Apple -->
        <div v-else-if="error" class="apple-error-card">
          <div class="apple-error-content">
            <div class="apple-error-icon">⚠️</div>
            <h3 class="apple-error-title">Error de Conexión</h3>
            <p class="apple-error-message">{{ error }}</p>
            <button @click="cargarManuales" class="apple-retry-btn">
              Reintentar
            </button>
          </div>
        </div>
        
        <!-- Estado vacío Apple -->
        <div v-else-if="manuales.length === 0" class="apple-empty-card">
          <div class="apple-empty-content">
            <div class="apple-empty-icon">📚</div>
            <h3 class="apple-empty-title">Sin manuales</h3>
            <p class="apple-empty-message">No hay documentos disponibles</p>
          </div>
        </div>
        
        <!-- Lista de manuales -->
        <div v-else class="sf-manuales-list">
          <div class="sf-manuales-scroll">
            <div class="sf-manuales-grid">
          
          <article 
            v-for="(manual, index) in manuales" 
            :key="manual.id"
            class="sf-manual-card"
            :class="{ 'sf-manual-unread': !manual.leido }"
            :style="{ animationDelay: `${index * 0.05}s` }"
            @click="abrirManual(manual)"
          >
            
            <!-- Badge NUEVO -->
            <div v-if="!manual.leido" class="sf-new-badge">
              <span class="sf-new-dot"></span>
              Nuevo
            </div>
            
            <!-- Preview de imagen o placeholder -->
            <div class="sf-manual-preview">
              <img 
                v-if="manual.imagen_nombre"
                :src="getImagenUrl(manual.id)" 
                :alt="manual.titulo"
                class="sf-manual-image"
                @error="handleImageError($event)"
              />
              <div v-else class="sf-manual-placeholder">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path v-if="manual.archivo_nombre" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  <path v-else-if="manual.enlace_url" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/>
                  <path v-else d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
                </svg>
              </div>
            </div>
            
            <!-- Contenido -->
            <div class="sf-manual-content">
              
              <!-- Título -->
              <h3 class="sf-manual-title">{{ manual.titulo }}</h3>
              
              <!-- Subtítulo -->
              <p v-if="manual.subtitulo" class="sf-manual-subtitle">
                {{ manual.subtitulo }}
              </p>
              
              <!-- Descripción -->
              <p v-if="manual.descripcion" class="sf-manual-desc">
                {{ manual.descripcion }}
              </p>
              
              <!-- Meta info -->
              <div class="sf-manual-meta">
                <div class="sf-manual-badges">
                  <span v-if="manual.archivo_nombre" class="sf-badge sf-badge-pdf">
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                    PDF
                  </span>
                  <span v-if="manual.enlace_url" class="sf-badge sf-badge-link">
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <path d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                    </svg>
                    Link
                  </span>
                  <span v-if="manual.video_nombre" class="sf-badge sf-badge-video">
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <polygon points="23 7 16 12 23 17 23 7"/>
                      <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
                    </svg>
                    Video
                  </span>
                </div>
                <time class="sf-manual-date">{{ formatearFecha(manual.fecha_creacion) }}</time>
              </div>
              
            </div>
            
            <!-- Chevron -->
            <div class="sf-manual-chevron">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <polyline points="9,18 15,12 9,6"/>
              </svg>
            </div>
            
          </article>
          
            </div>
          </div>
        </div>
        
      </div>
      
    </div>
    
    <!-- Modal Apple Style -->
    <Teleport to="body">
      <Transition name="apple-modal">
        <div v-if="modalAbierto" class="apple-modal-overlay" @click="cerrarModal">
          
          <Transition name="apple-modal-content" appear>
            <article class="apple-modal" @click.stop>
              
              <!-- Handle bar (mobile) -->
              <div class="apple-modal-handle">
                <div class="apple-modal-bar"></div>
              </div>
              
              <!-- Close button -->
              <button class="apple-modal-close" @click="cerrarModal">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
              
              <!-- Scrollable content -->
              <div class="apple-modal-scroll">
                
                <!-- Hero image/gradient -->
                <div class="apple-modal-hero" @click="manualSeleccionado?.imagen_nombre && abrirImagenCompleta()">
                  <div v-if="manualSeleccionado?.imagen_nombre" class="apple-hero-image-wrap">
                    <img 
                      :src="getImagenUrl(manualSeleccionado.id)" 
                      :alt="manualSeleccionado.titulo"
                      class="apple-hero-image"
                    />
                    <div class="apple-hero-gradient"></div>
                    <!-- Expand hint -->
                    <div class="apple-expand-hint">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="15 3 21 3 21 9"/>
                        <polyline points="9 21 3 21 3 15"/>
                        <line x1="21" y1="3" x2="14" y2="10"/>
                        <line x1="3" y1="21" x2="10" y2="14"/>
                      </svg>
                      Ampliar
                    </div>
                  </div>
                  <div v-else class="apple-hero-gradient-only">
                    <div class="apple-hero-icon">
                      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <path d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25"/>
                      </svg>
                    </div>
                  </div>
                </div>
                
                <!-- Content container -->
                <div class="apple-modal-content">
                  
                  <!-- Title section -->
                  <header class="apple-content-header">
                    <h2 class="apple-modal-title">{{ manualSeleccionado?.titulo }}</h2>
                    <p v-if="manualSeleccionado?.subtitulo" class="apple-modal-subtitle">
                      {{ manualSeleccionado?.subtitulo }}
                    </p>
                  </header>
                  
                  <!-- Quick actions (tipo pill) -->
                  <div class="apple-quick-actions">
                    <a 
                      v-if="manualSeleccionado?.archivo_nombre"
                      :href="getArchivoUrl(manualSeleccionado.id)"
                      target="_blank"
                      class="apple-action-pill apple-pill-document"
                    >
                      <div class="apple-pill-icon">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                          <polyline points="14 2 14 8 20 8"/>
                          <line x1="12" y1="18" x2="12" y2="12"/>
                          <line x1="9" y1="15" x2="15" y2="15"/>
                        </svg>
                      </div>
                      <div class="apple-pill-text">
                        <span class="apple-pill-label">Documento</span>
                        <span class="apple-pill-action">Abrir PDF</span>
                      </div>
                    </a>
                    
                    <a 
                      v-if="manualSeleccionado?.enlace_url"
                      :href="manualSeleccionado.enlace_url"
                      target="_blank"
                      class="apple-action-pill apple-pill-link"
                    >
                      <div class="apple-pill-icon">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                          <polyline points="15 3 21 3 21 9"/>
                          <line x1="10" y1="14" x2="21" y2="3"/>
                        </svg>
                      </div>
                      <div class="apple-pill-text">
                        <span class="apple-pill-label">Enlace</span>
                        <span class="apple-pill-action">Abrir sitio</span>
                      </div>
                    </a>
                  </div>
                  
                  <!-- Description -->
                  <section v-if="manualSeleccionado?.descripcion" class="apple-section">
                    <h3 class="apple-section-title">Descripción</h3>
                    <p class="apple-description">{{ manualSeleccionado.descripcion }}</p>
                  </section>
                  
                  <!-- Video -->
                  <section v-if="manualSeleccionado?.video_nombre" class="apple-section">
                    <h3 class="apple-section-title">Video</h3>
                    <div class="apple-video-container">
                      <video 
                        :src="getVideoUrl(manualSeleccionado.id)" 
                        controls
                        controlsList="nodownload"
                        playsinline
                        preload="metadata"
                        class="apple-video"
                      ></video>
                    </div>
                  </section>
                  
                  <!-- Info list -->
                  <section class="apple-section">
                    <h3 class="apple-section-title">Información</h3>
                    <div class="apple-info-list">
                      <div class="apple-info-item">
                        <div class="apple-info-icon">
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                            <line x1="16" y1="2" x2="16" y2="6"/>
                            <line x1="8" y1="2" x2="8" y2="6"/>
                            <line x1="3" y1="10" x2="21" y2="10"/>
                          </svg>
                        </div>
                        <div class="apple-info-content">
                          <span class="apple-info-label">Publicación</span>
                          <span class="apple-info-value">{{ formatearFecha(manualSeleccionado?.fecha_creacion) }}</span>
                        </div>
                      </div>
                      
                      <div v-if="manualSeleccionado?.leido" class="apple-info-item apple-info-success">
                        <div class="apple-info-icon">
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                            <polyline points="22 4 12 14.01 9 11.01"/>
                          </svg>
                        </div>
                        <div class="apple-info-content">
                          <span class="apple-info-label">Lectura</span>
                          <span class="apple-info-value">{{ formatearFecha(manualSeleccionado?.fecha_lectura) }}</span>
                        </div>
                      </div>
                    </div>
                  </section>
                  
                </div>
                
              </div>
              
              <!-- Footer -->
              <footer class="apple-modal-footer">
                <button @click="cerrarModal" class="apple-btn-close">
                  Cerrar
                </button>
              </footer>
              
            </article>
          </Transition>
          
        </div>
      </Transition>
    </Teleport>
    
    <!-- Fullscreen Image Viewer -->
    <Teleport to="body">
      <Transition name="apple-fullscreen">
        <div v-if="imagenCompleta" class="apple-fullscreen-overlay" @click="cerrarImagenCompleta">
          <button class="apple-fullscreen-close" @click="cerrarImagenCompleta">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
          <img 
            :src="getImagenUrl(manualSeleccionado?.id)" 
            :alt="manualSeleccionado?.titulo"
            class="apple-fullscreen-image"
            @click.stop
          />
        </div>
      </Transition>
    </Teleport>
    
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { manualesService } from '../services/manualesService'

// Estado
const cargando = ref(false)
const error = ref(null)
const manuales = ref([])
const modalAbierto = ref(false)
const manualSeleccionado = ref(null)
const imagenCompleta = ref(false)

// Usuario actual
const usuarioId = computed(() => {
  const userData = localStorage.getItem('user')
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
    manual.leido = true
    manual.fecha_lectura = new Date().toISOString()
    window.dispatchEvent(new CustomEvent('manual-leido'))
  }
}

// Cerrar modal
const cerrarModal = () => {
  modalAbierto.value = false
  manualSeleccionado.value = null
  imagenCompleta.value = false
}

// Abrir imagen completa
const abrirImagenCompleta = () => {
  imagenCompleta.value = true
}

// Cerrar imagen completa
const cerrarImagenCompleta = () => {
  imagenCompleta.value = false
}

// Obtener URL de imagen
const getImagenUrl = (manualId) => {
  return manualesService.getImagenUrl(manualId)
}

// Obtener URL de video
const getVideoUrl = (manualId) => {
  return manualesService.getVideoUrl(manualId)
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
/* ================================================
   APPLE MANUALES - DESIGN SYSTEM (iOS 17)
   ================================================ */

/* Page container */
.apple-manuales-page {
  position: fixed;
  inset: 0;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  background: linear-gradient(180deg, #f0fdf4 0%, #ecfdf5 50%, #f0fdf4 100%);
}

/* Fondo dinámico Apple */
.apple-dynamic-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
  z-index: 0;
}

.apple-gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(70px);
  opacity: 0.6;
  animation: appleOrbFloat 20s ease-in-out infinite;
}

.apple-orb-1 {
  top: 10%;
  right: 15%;
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, rgba(52, 211, 153, 0.4), rgba(16, 185, 129, 0.3));
}

.apple-orb-2 {
  top: 50%;
  left: 10%;
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, rgba(110, 231, 183, 0.35), rgba(52, 211, 153, 0.2));
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
.apple-manuales-container {
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
.apple-error-card,
.apple-empty-card {
  max-width: 28rem;
  margin: 0 auto;
  padding: 0 0.75rem;
}

.apple-error-content,
.apple-empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2.5rem 1.5rem;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  text-align: center;
}

.apple-error-icon,
.apple-empty-icon {
  font-size: 2.5rem;
  margin-bottom: 0.75rem;
}

.apple-error-title,
.apple-empty-title {
  font-size: 1rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
  margin: 0 0 0.375rem;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
}

.apple-error-message,
.apple-empty-message {
  font-size: 0.8125rem;
  color: rgba(0, 0, 0, 0.5);
  margin: 0;
}

.apple-retry-btn {
  margin-top: 1rem;
  padding: 0.625rem 1.5rem;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  border-radius: 100px;
  color: white;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.apple-retry-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4);
}

.apple-retry-btn:active {
  transform: scale(0.98);
}

/* ================================================
   MANUALES LIST
   ================================================ */

.sf-manuales-list {
  height: 100%;
  overflow: hidden;
  max-width: 28rem;
  margin: 0 auto;
  padding: 0 0.75rem;
}

.sf-manuales-scroll {
  height: 100%;
  overflow-y: auto;
  padding: 0.25rem;
  -webkit-overflow-scrolling: touch;
}

.sf-manuales-scroll::-webkit-scrollbar {
  width: 4px;
}

.sf-manuales-scroll::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

/* ================================================
   MANUALES GRID
   ================================================ */

.sf-manuales-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding-bottom: 1rem;
}

/* ================================================
   MANUAL CARD
   ================================================ */

.sf-manual-card {
  position: relative;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.95);
  border: 0.5px solid rgba(0, 0, 0, 0.06);
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  animation: sfCardIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) backwards;
}

@keyframes sfCardIn {
  from {
    opacity: 0;
    transform: translateY(15px) scale(0.97);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.sf-manual-card:hover {
  transform: translateY(-3px) scale(1.01);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
  border-color: rgba(0, 0, 0, 0.1);
}

.sf-manual-card:active {
  transform: scale(0.98);
}

.sf-manual-unread {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(236, 253, 245, 0.95));
  border-color: rgba(16, 185, 129, 0.15);
}

/* NEW badge */
.sf-new-badge {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  z-index: 10;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.3rem 0.75rem;
  background: linear-gradient(145deg, #ef4444, #dc2626);
  border-radius: 100px;
  font-size: 0.625rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: white;
  box-shadow: 0 3px 10px rgba(220, 38, 38, 0.4);
  animation: sfBadgePulse 2s ease-in-out infinite;
}

.sf-new-dot {
  width: 6px;
  height: 6px;
  background: white;
  border-radius: 50%;
  animation: sfDotPulse 1.5s ease-in-out infinite;
}

@keyframes sfBadgePulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.03); }
}

@keyframes sfDotPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Preview - imagen arriba */
.sf-manual-preview {
  width: 100%;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
}

@media (min-width: 640px) {
  .sf-manual-preview {
    height: 140px;
  }
}

.sf-manual-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.35s ease;
}

.sf-manual-card:hover .sf-manual-image {
  transform: scale(1.08);
}

.sf-manual-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, #e0f2fe, #dbeafe, #e0e7ff);
  color: rgba(59, 130, 246, 0.4);
}

.sf-manual-placeholder svg {
  width: 40px;
  height: 40px;
}

/* Content */
.sf-manual-content {
  flex: 1;
  min-width: 0;
  padding: 1rem;
  display: flex;
  flex-direction: column;
}

.sf-manual-title {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: -0.01em;
  color: rgba(0, 0, 0, 0.9);
  margin: 0;
  line-height: 1.3;
}

.sf-manual-subtitle {
  font-size: 0.8125rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.5);
  margin: 0.25rem 0 0;
  line-height: 1.35;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.sf-manual-desc {
  font-size: 0.75rem;
  color: rgba(0, 0, 0, 0.45);
  margin: 0.375rem 0 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Meta */
.sf-manual-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  margin-top: auto;
  padding-top: 0.5rem;
}

.sf-manual-badges {
  display: flex;
  gap: 0.375rem;
}

.sf-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
  font-size: 0.5625rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.sf-badge-pdf {
  background: linear-gradient(145deg, #fef2f2, #fee2e2);
  color: #dc2626;
}

.sf-badge-link {
  background: linear-gradient(145deg, #eff6ff, #dbeafe);
  color: #2563eb;
}

.sf-badge-video {
  background: linear-gradient(145deg, #fff7ed, #ffedd5);
  color: #ea580c;
}

.sf-manual-date {
  font-size: 0.6875rem;
  color: rgba(0, 0, 0, 0.4);
  font-weight: 500;
}

/* Chevron - oculto en layout vertical */
.sf-manual-chevron {
  display: none;
}

/* ================================================
   APPLE MODAL (iOS 17 Style)
   ================================================ */

.apple-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding-top: env(safe-area-inset-top, 20px);
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);
}

@media (min-width: 640px) {
  .apple-modal-overlay {
    align-items: center;
    padding: 1.5rem;
  }
}

.apple-modal {
  position: relative;
  width: 100%;
  max-width: 100%;
  max-height: calc(100vh - env(safe-area-inset-top, 20px) - 44px);
  margin-top: auto;
  background: #ffffff;
  border-radius: 14px 14px 0 0;
  box-shadow: 0 -20px 60px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

@media (min-width: 640px) {
  .apple-modal {
    max-width: 26rem;
    max-height: 88vh;
    margin-top: 0;
    border-radius: 28px;
    box-shadow: 0 30px 80px rgba(0, 0, 0, 0.3);
  }
}

/* Handle bar */
.apple-modal-handle {
  flex-shrink: 0;
  display: flex;
  justify-content: center;
  padding: 0.5rem 0 0.25rem;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 30;
}

@media (min-width: 640px) {
  .apple-modal-handle {
    display: none;
  }
}

.apple-modal-bar {
  width: 36px;
  height: 5px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 100px;
}

/* Close button */
.apple-modal-close {
  position: absolute;
  top: 0.875rem;
  right: 0.875rem;
  z-index: 30;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: none;
  border-radius: 50%;
  color: white;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-modal-close:hover {
  background: rgba(0, 0, 0, 0.5);
  transform: scale(1.1);
}

.apple-modal-close:active {
  transform: scale(0.95);
}

/* Scrollable content */
.apple-modal-scroll {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
}

.apple-modal-scroll::-webkit-scrollbar {
  width: 4px;
}

.apple-modal-scroll::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

/* Hero section */
.apple-modal-hero {
  position: relative;
  cursor: pointer;
}

.apple-hero-image-wrap {
  position: relative;
  height: 180px;
  overflow: hidden;
}

@media (min-width: 640px) {
  .apple-hero-image-wrap {
    height: 200px;
  }
}

.apple-hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.apple-modal-hero:hover .apple-hero-image {
  transform: scale(1.03);
}

.apple-hero-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, 
    transparent 0%, 
    transparent 40%, 
    rgba(0, 0, 0, 0.4) 100%
  );
}

.apple-expand-hint {
  position: absolute;
  bottom: 0.75rem;
  right: 0.75rem;
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 100px;
  font-size: 0.6875rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.75);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  transition: all 0.2s ease;
}

.apple-expand-hint svg {
  width: 12px;
  height: 12px;
}

.apple-modal-hero:hover .apple-expand-hint {
  background: white;
  transform: scale(1.05);
}

/* Gradient only (no image) */
.apple-hero-gradient-only {
  height: 120px;
  background: linear-gradient(145deg, #10b981, #059669, #047857);
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (min-width: 640px) {
  .apple-hero-gradient-only {
    height: 140px;
  }
}

.apple-hero-icon {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  color: white;
}

/* Content container */
.apple-modal-content {
  padding: 1.25rem;
}

@media (min-width: 640px) {
  .apple-modal-content {
    padding: 1.5rem;
  }
}

/* Header */
.apple-content-header {
  margin-bottom: 1rem;
}

.apple-modal-title {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
  font-size: 1.375rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: rgba(0, 0, 0, 0.9);
  margin: 0;
  line-height: 1.2;
}

@media (min-width: 640px) {
  .apple-modal-title {
    font-size: 1.5rem;
  }
}

.apple-modal-subtitle {
  font-size: 0.875rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.5);
  margin: 0.375rem 0 0;
  line-height: 1.4;
}

/* Quick actions (pills) */
.apple-quick-actions {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  margin-bottom: 1.25rem;
}

.apple-action-pill {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 0.875rem 1rem;
  background: rgba(0, 0, 0, 0.03);
  border-radius: 14px;
  text-decoration: none;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-action-pill:hover {
  background: rgba(0, 0, 0, 0.06);
  transform: translateX(4px);
}

.apple-action-pill:active {
  transform: scale(0.98);
}

.apple-pill-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  flex-shrink: 0;
}

.apple-pill-document .apple-pill-icon {
  background: linear-gradient(145deg, #ef4444, #dc2626);
  color: white;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

.apple-pill-link .apple-pill-icon {
  background: linear-gradient(145deg, #3b82f6, #2563eb);
  color: white;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.apple-pill-text {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.apple-pill-label {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: rgba(0, 0, 0, 0.4);
}

.apple-pill-action {
  font-size: 0.9375rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
}

/* Sections */
.apple-section {
  margin-bottom: 1.25rem;
}

.apple-section-title {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: rgba(0, 0, 0, 0.4);
  margin: 0 0 0.625rem;
}

.apple-description {
  font-size: 0.9375rem;
  line-height: 1.65;
  color: rgba(0, 0, 0, 0.7);
  margin: 0;
  white-space: pre-wrap;
}

/* Video */
.apple-video-container {
  border-radius: 16px;
  overflow: hidden;
  background: #000;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.apple-video {
  width: 100%;
  height: auto;
  display: block;
}

/* Info list */
.apple-info-list {
  background: linear-gradient(145deg, #f8fafc, #f1f5f9);
  border-radius: 14px;
  overflow: hidden;
}

.apple-info-item {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 0.875rem 1rem;
}

.apple-info-item + .apple-info-item {
  border-top: 0.5px solid rgba(0, 0, 0, 0.06);
}

.apple-info-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  color: rgba(0, 0, 0, 0.5);
  flex-shrink: 0;
}

.apple-info-success .apple-info-icon {
  background: rgba(16, 185, 129, 0.12);
  color: #059669;
}

.apple-info-content {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.apple-info-label {
  font-size: 0.6875rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.45);
}

.apple-info-value {
  font-size: 0.8125rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.8);
}

.apple-info-success .apple-info-value {
  color: #059669;
}

/* Footer */
.apple-modal-footer {
  flex-shrink: 0;
  padding: 1rem 1.25rem 1.25rem;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0) 0%, #ffffff 100%);
}

@media (min-width: 640px) {
  .apple-modal-footer {
    padding: 1rem 1.5rem 1.5rem;
  }
}

.apple-btn-close {
  width: 100%;
  padding: 0.875rem 1.5rem;
  background: rgba(0, 0, 0, 0.06);
  border: none;
  border-radius: 14px;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 1rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.65);
  cursor: pointer;
  transition: all 0.2s ease;
}

.apple-btn-close:hover {
  background: rgba(0, 0, 0, 0.1);
}

.apple-btn-close:active {
  transform: scale(0.98);
}

/* ================================================
   FULLSCREEN IMAGE VIEWER
   ================================================ */

.apple-fullscreen-overlay {
  position: fixed;
  inset: 0;
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

.apple-fullscreen-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 10;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: none;
  border-radius: 50%;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.apple-fullscreen-close:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: scale(1.1);
}

.apple-fullscreen-image {
  max-width: 95%;
  max-height: 90vh;
  object-fit: contain;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

/* ================================================
   MODAL TRANSITIONS (Apple iOS 17 Style)
   ================================================ */

/* Overlay backdrop fade */
.apple-modal-enter-active {
  animation: appleOverlayIn 0.4s cubic-bezier(0.32, 0.72, 0, 1) forwards;
}

.apple-modal-leave-active {
  animation: appleOverlayOut 0.3s cubic-bezier(0.32, 0.72, 0, 1) forwards;
}

@keyframes appleOverlayIn {
  0% {
    opacity: 0;
    backdrop-filter: blur(0px);
    -webkit-backdrop-filter: blur(0px);
  }
  100% {
    opacity: 1;
    backdrop-filter: blur(12px) saturate(180%);
    -webkit-backdrop-filter: blur(12px) saturate(180%);
  }
}

@keyframes appleOverlayOut {
  0% {
    opacity: 1;
    backdrop-filter: blur(12px) saturate(180%);
    -webkit-backdrop-filter: blur(12px) saturate(180%);
  }
  100% {
    opacity: 0;
    backdrop-filter: blur(0px);
    -webkit-backdrop-filter: blur(0px);
  }
}

/* Modal sheet animation - Mobile (slides up like iOS) */
.apple-modal-content-enter-active {
  animation: appleSheetIn 0.5s cubic-bezier(0.32, 0.72, 0, 1) forwards;
}

.apple-modal-content-leave-active {
  animation: appleSheetOut 0.35s cubic-bezier(0.32, 0.72, 0, 1) forwards;
}

@keyframes appleSheetIn {
  0% {
    opacity: 0;
    transform: translateY(100%) scale(0.96);
  }
  40% {
    opacity: 1;
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes appleSheetOut {
  0% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  100% {
    opacity: 0;
    transform: translateY(40%) scale(0.98);
  }
}

/* Modal animation - Desktop (scales in like macOS) */
@media (min-width: 640px) {
  .apple-modal-content-enter-active {
    animation: appleModalDesktopIn 0.45s cubic-bezier(0.32, 0.72, 0, 1) forwards;
  }
  
  .apple-modal-content-leave-active {
    animation: appleModalDesktopOut 0.3s cubic-bezier(0.32, 0.72, 0, 1) forwards;
  }
  
  @keyframes appleModalDesktopIn {
    0% {
      opacity: 0;
      transform: scale(0.88) translateY(30px);
    }
    50% {
      opacity: 1;
    }
    100% {
      opacity: 1;
      transform: scale(1) translateY(0);
    }
  }
  
  @keyframes appleModalDesktopOut {
    0% {
      opacity: 1;
      transform: scale(1) translateY(0);
    }
    100% {
      opacity: 0;
      transform: scale(0.92) translateY(20px);
    }
  }
}

/* Content stagger animation inside modal */
.apple-modal-scroll {
  animation: appleContentFadeIn 0.6s cubic-bezier(0.32, 0.72, 0, 1) 0.15s both;
}

@keyframes appleContentFadeIn {
  0% {
    opacity: 0;
    transform: translateY(15px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Hero section special animation */
.apple-modal-hero {
  animation: appleHeroIn 0.55s cubic-bezier(0.32, 0.72, 0, 1) 0.1s both;
}

@keyframes appleHeroIn {
  0% {
    opacity: 0;
    transform: scale(1.05);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

/* Action pills stagger */
.apple-action-pill:nth-child(1) {
  animation: applePillIn 0.4s cubic-bezier(0.32, 0.72, 0, 1) 0.2s both;
}

.apple-action-pill:nth-child(2) {
  animation: applePillIn 0.4s cubic-bezier(0.32, 0.72, 0, 1) 0.28s both;
}

@keyframes applePillIn {
  0% {
    opacity: 0;
    transform: translateX(-12px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Fullscreen image viewer transitions */
.apple-fullscreen-enter-active {
  animation: appleFullscreenIn 0.4s cubic-bezier(0.32, 0.72, 0, 1) forwards;
}

.apple-fullscreen-leave-active {
  animation: appleFullscreenOut 0.3s cubic-bezier(0.32, 0.72, 0, 1) forwards;
}

@keyframes appleFullscreenIn {
  0% {
    opacity: 0;
    backdrop-filter: blur(0px);
  }
  100% {
    opacity: 1;
    backdrop-filter: blur(20px);
  }
}

@keyframes appleFullscreenOut {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

.apple-fullscreen-enter-active .apple-fullscreen-image {
  animation: appleImageZoomIn 0.5s cubic-bezier(0.32, 0.72, 0, 1) forwards;
}

.apple-fullscreen-leave-active .apple-fullscreen-image {
  animation: appleImageZoomOut 0.3s cubic-bezier(0.32, 0.72, 0, 1) forwards;
}

@keyframes appleImageZoomIn {
  0% {
    opacity: 0;
    transform: scale(0.75);
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes appleImageZoomOut {
  0% {
    opacity: 1;
    transform: scale(1);
  }
  100% {
    opacity: 0;
    transform: scale(0.85);
  }
}
</style>
