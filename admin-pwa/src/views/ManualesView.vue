<template>
  <div class="manuales-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                <circle cx="12" cy="10" r="2"/>
                <path d="M12 14v3"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Centro de Manuales</h1>
              <p class="header-subtitle">Gestiona manuales, guías y documentos para los usuarios</p>
            </div>
          </div>
          <div v-if="puedeCrearManuales" class="header-actions">
            <button class="btn-primary" @click="mostrarModalCrear = true">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 5v14"/>
                <path d="M5 12h14"/>
              </svg>
              Nuevo Manual
            </button>
          </div>
        </div>
      </header>

      <div class="page-content">
        <!-- Mensaje de carga -->
        <div v-if="cargando" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Cargando manuales...</p>
        </div>

        <!-- Mensaje de error -->
        <div v-if="error && !cargando" class="error-state">
          <div class="error-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
          </div>
          <h3>Error al cargar manuales</h3>
          <p>{{ error }}</p>
          <button class="btn-secondary" @click="cargarManuales">Reintentar</button>
        </div>

        <!-- Lista de manuales -->
        <div v-if="!cargando && !error" class="manuales-list">
          <div class="list-header">
            <h2>Manuales Publicados ({{ manuales.length }})</h2>
            <button class="btn-refresh" @click="cargarManuales" :disabled="cargando">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M23 4v6h-6"/>
                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
              </svg>
              Actualizar
            </button>
          </div>

          <!-- Tabla de manuales -->
          <div class="table-container">
            <table class="manuales-table">
              <thead>
                <tr>
                  <th>Título</th>
                  <th>Subtítulo</th>
                  <th>Contenido</th>
                  <th>Destinatarios</th>
                  <th>Lecturas</th>
                  <th>Fecha</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="manual in manuales" :key="manual.id" class="manual-row">
                  <td class="title-cell">
                    <div class="title-content">
                      <span class="manual-title">{{ manual.titulo }}</span>
                    </div>
                  </td>
                  <td class="subtitle-cell">
                    <span v-if="manual.subtitulo" class="manual-subtitle">{{ manual.subtitulo }}</span>
                    <span v-else class="no-subtitle">—</span>
                  </td>
                  <td class="content-cell">
                    <div class="content-badges">
                      <span v-if="manual.archivo_nombre" class="badge badge-pdf" title="Documento adjunto">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                          <polyline points="14 2 14 8 20 8"/>
                        </svg>
                        PDF
                      </span>
                      <span v-if="manual.imagen_nombre" class="badge badge-img" title="Imagen adjunta">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                          <circle cx="8.5" cy="8.5" r="1.5"/>
                          <polyline points="21 15 16 10 5 21"/>
                        </svg>
                        IMG
                      </span>
                      <span v-if="manual.video_nombre" class="badge badge-video" title="Video adjunto">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <polygon points="23 7 16 12 23 17 23 7"/>
                          <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
                        </svg>
                        VIDEO
                      </span>
                      <span v-if="manual.enlace_url" class="badge badge-url" title="Enlace externo">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                          <polyline points="15 3 21 3 21 9"/>
                          <line x1="10" y1="14" x2="21" y2="3"/>
                        </svg>
                        URL
                      </span>
                      <span v-if="!manual.archivo_nombre && !manual.imagen_nombre && !manual.video_nombre && !manual.enlace_url" class="badge badge-text">
                        Solo texto
                      </span>
                    </div>
                  </td>
                  <td class="recipients-cell">
                    <span class="recipients-badge" :class="{ 'all-users': manual.enviado_a_todos }">
                      {{ manual.destinatarios_texto }}
                    </span>
                  </td>
                  <td class="reads-cell">
                    <span class="reads-badge">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                        <circle cx="12" cy="12" r="3"/>
                      </svg>
                      {{ manual.total_lecturas }}
                    </span>
                  </td>
                  <td class="date-cell">
                    <span class="manual-date">{{ formatearFecha(manual.fecha_creacion) }}</span>
                  </td>
                  <td class="actions-cell">
                    <div class="action-buttons">
                      <button class="btn-action btn-view" @click="verDetalle(manual)" title="Ver detalle">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                          <circle cx="12" cy="12" r="3"/>
                        </svg>
                      </button>
                      <button class="btn-action btn-stats" @click="verEstadisticas(manual)" title="Ver estadísticas">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M3 3v18h18"/>
                          <path d="M18 17V9"/>
                          <path d="M13 17V5"/>
                          <path d="M8 17v-3"/>
                        </svg>
                      </button>
                      <button v-if="puedeEliminar" class="btn-action btn-edit" @click="abrirModalEditar(manual)" title="Editar">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                        </svg>
                      </button>
                      <button v-if="puedeEliminar" class="btn-action btn-delete" @click="confirmarEliminar(manual)" title="Eliminar">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M3 6h18"/>
                          <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
                          <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- Estado vacío -->
            <div v-if="manuales.length === 0" class="empty-state">
              <div class="empty-icon">📚</div>
              <h3>No hay manuales</h3>
              <p>Crea tu primer manual para compartir información con los usuarios.</p>
              <button v-if="puedeCrearManuales" class="btn-primary" @click="mostrarModalCrear = true">
                Crear Primer Manual
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal Crear Manual -->
    <div v-if="mostrarModalCrear" class="modal-overlay" @click="cerrarModalCrear">
      <div class="modal-content modal-large" @click.stop>
        <div class="modal-header modal-header-crear">
          <div class="modal-header-content">
            <div class="modal-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                <path d="M12 7v6"/>
                <path d="M9 10h6"/>
              </svg>
            </div>
            <div class="modal-title-section">
              <h3>Crear Nuevo Manual</h3>
              <p class="modal-description">Comparte manuales, guías y documentos con tu equipo</p>
            </div>
          </div>
          <button class="btn-close" @click="cerrarModalCrear">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="crearManual">
            <div class="form-row">
              <!-- Título -->
              <div class="form-group">
                <label for="titulo">Título *</label>
                <input
                  id="titulo"
                  v-model="formManual.titulo"
                  type="text"
                  class="form-input"
                  placeholder="Título del manual"
                  maxlength="200"
                  required
                />
                <small class="char-count">{{ formManual.titulo.length }}/200</small>
              </div>

              <!-- Subtítulo -->
              <div class="form-group">
                <label for="subtitulo">Subtítulo</label>
                <input
                  id="subtitulo"
                  v-model="formManual.subtitulo"
                  type="text"
                  class="form-input"
                  placeholder="Subtítulo opcional"
                  maxlength="300"
                />
              </div>
            </div>

            <!-- Descripción -->
            <div class="form-group">
              <label for="descripcion">Descripción</label>
              <textarea
                id="descripcion"
                v-model="formManual.descripcion"
                class="form-textarea"
                placeholder="Descripción detallada del manual..."
                rows="4"
              ></textarea>
            </div>

            <!-- URL -->
            <div class="form-group">
              <label for="enlace_url">Enlace URL (opcional)</label>
              <input
                id="enlace_url"
                v-model="formManual.enlace_url"
                type="url"
                class="form-input"
                placeholder="https://ejemplo.com/recurso"
              />
            </div>

            <div class="form-row">
              <!-- Archivo PDF -->
              <div class="form-group">
                <label>Archivo PDF/Documento</label>
                <div class="file-upload-area" @click="$refs.archivoInput.click()">
                  <input
                    ref="archivoInput"
                    type="file"
                    accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx"
                    @change="handleArchivoChange"
                    hidden
                  />
                  <div v-if="!archivoSeleccionado" class="upload-placeholder">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14 2 14 8 20 8"/>
                      <line x1="12" y1="18" x2="12" y2="12"/>
                      <line x1="9" y1="15" x2="15" y2="15"/>
                    </svg>
                    <span>Clic para subir PDF</span>
                  </div>
                  <div v-else class="file-selected">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14 2 14 8 20 8"/>
                    </svg>
                    <span>{{ archivoSeleccionado.name }}</span>
                    <button type="button" class="btn-remove-file" @click.stop="removerArchivo">×</button>
                  </div>
                </div>
              </div>

              <!-- Selector de Media (Imagen o Video) -->
              <div class="form-group">
                <label>Multimedia de Portada</label>
                <div class="media-type-selector">
                  <label class="media-option" :class="{ active: tipoMedia === 'ninguno' }">
                    <input type="radio" v-model="tipoMedia" value="ninguno" hidden />
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"/>
                      <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
                    </svg>
                    <span>Ninguno</span>
                  </label>
                  <label class="media-option" :class="{ active: tipoMedia === 'imagen' }">
                    <input type="radio" v-model="tipoMedia" value="imagen" hidden />
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                      <circle cx="8.5" cy="8.5" r="1.5"/>
                      <polyline points="21 15 16 10 5 21"/>
                    </svg>
                    <span>Imagen</span>
                  </label>
                  <label class="media-option" :class="{ active: tipoMedia === 'video' }">
                    <input type="radio" v-model="tipoMedia" value="video" hidden />
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polygon points="23 7 16 12 23 17 23 7"/>
                      <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
                    </svg>
                    <span>Video</span>
                  </label>
                </div>
                
                <!-- Subir Imagen -->
                <div v-if="tipoMedia === 'imagen'" class="file-upload-area" @click="$refs.imagenInput.click()">
                  <input
                    ref="imagenInput"
                    type="file"
                    accept="image/*"
                    @change="handleImagenChange"
                    hidden
                  />
                  <div v-if="!imagenSeleccionada" class="upload-placeholder">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                      <circle cx="8.5" cy="8.5" r="1.5"/>
                      <polyline points="21 15 16 10 5 21"/>
                    </svg>
                    <span>Clic para subir imagen</span>
                  </div>
                  <div v-else class="file-selected">
                    <img :src="imagenPreview" alt="Preview" class="image-preview" />
                    <span>{{ imagenSeleccionada.name }}</span>
                    <button type="button" class="btn-remove-file" @click.stop="removerImagen">×</button>
                  </div>
                </div>
                
                <!-- Subir Video -->
                <div v-if="tipoMedia === 'video'" class="file-upload-area" @click="$refs.videoInput.click()">
                  <input
                    ref="videoInput"
                    type="file"
                    accept=".mp4,.webm,.mov,.avi,.mkv"
                    @change="handleVideoChange"
                    hidden
                  />
                  <div v-if="!videoSeleccionado" class="upload-placeholder">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polygon points="23 7 16 12 23 17 23 7"/>
                      <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
                    </svg>
                    <span>Clic para subir video (máx. 100MB)</span>
                    <small style="color: #888; margin-top: 4px; font-size: 11px;">Formatos: MP4, WebM, MOV, AVI, MKV</small>
                  </div>
                  <div v-else class="file-selected">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="2">
                      <polygon points="23 7 16 12 23 17 23 7"/>
                      <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
                    </svg>
                    <span>{{ videoSeleccionado.name }}</span>
                    <button type="button" class="btn-remove-file" @click.stop="removerVideo">×</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Destinatarios -->
            <div class="form-group">
              <label>Destinatarios</label>
              <div class="destinatarios-options">
                <label class="radio-option">
                  <input type="radio" v-model="formManual.enviado_a_todos" :value="true" />
                  <span class="radio-label">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                      <circle cx="9" cy="7" r="4"/>
                      <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                      <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                    </svg>
                    Todos los usuarios
                  </span>
                </label>
                <label class="radio-option">
                  <input type="radio" v-model="formManual.enviado_a_todos" :value="false" />
                  <span class="radio-label">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                      <circle cx="12" cy="7" r="4"/>
                    </svg>
                    Usuarios específicos
                  </span>
                </label>
              </div>
            </div>

            <!-- Selector de usuarios -->
            <div v-if="!formManual.enviado_a_todos" class="form-group usuarios-selector">
              <label>Seleccionar Usuarios</label>
              <div class="usuarios-search">
                <input
                  v-model="busquedaUsuario"
                  type="text"
                  class="form-input"
                  placeholder="Buscar usuario..."
                />
              </div>
              <div class="usuarios-list">
                <label 
                  v-for="usuario in usuariosFiltrados" 
                  :key="usuario.id" 
                  class="usuario-checkbox"
                >
                  <input 
                    type="checkbox" 
                    :value="usuario.id" 
                    v-model="formManual.usuario_ids"
                  />
                  <span class="usuario-info">
                    <span class="usuario-nombre">{{ usuario.nombre_completo || usuario.correo }}</span>
                    <span class="usuario-correo">{{ usuario.correo }}</span>
                  </span>
                </label>
              </div>
              <div class="usuarios-selected-count">
                {{ formManual.usuario_ids.length }} usuario(s) seleccionado(s)
              </div>
            </div>

            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModalCrear">Cancelar</button>
              <button type="submit" class="btn-primary" :disabled="enviando">
                <span v-if="enviando" class="spinner"></span>
                {{ enviando ? 'Creando...' : 'Crear Manual' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal Ver Detalle -->
    <div v-if="mostrarModalDetalle" class="modal-overlay" @click="cerrarModalDetalle">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <div class="modal-header-content">
            <div class="modal-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
              </svg>
            </div>
            <div class="modal-title-section">
              <h3>Detalle del Manual</h3>
            </div>
          </div>
          <button class="btn-close" @click="cerrarModalDetalle">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="modal-body" v-if="manualDetalle">
          <div class="detalle-header">
            <h2 class="detalle-title">{{ manualDetalle.titulo }}</h2>
            <p v-if="manualDetalle.subtitulo" class="detalle-subtitulo">{{ manualDetalle.subtitulo }}</p>
          </div>
          
          <div v-if="manualDetalle.imagen_nombre || manualDetalle.video_nombre" class="detalle-media">
            <img v-if="manualDetalle.imagen_nombre" :src="getImagenUrl(manualDetalle.id)" alt="Imagen del manual" class="detalle-imagen" />
            <video v-else-if="manualDetalle.video_nombre" :src="getVideoUrl(manualDetalle.id)" controls class="detalle-video"></video>
          </div>
          
          <div v-if="manualDetalle.descripcion" class="detalle-descripcion">
            <div class="section-header">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
              </svg>
              <h4>Descripción</h4>
            </div>
            <p>{{ manualDetalle.descripcion }}</p>
          </div>
          
          <div class="detalle-meta">
            <div class="section-header">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="16" x2="12" y2="12"/>
                <line x1="12" y1="8" x2="12.01" y2="8"/>
              </svg>
              <h4>Información</h4>
            </div>
            <div class="meta-grid">
              <div v-if="manualDetalle.archivo_nombre" class="meta-item">
                <div class="meta-icon meta-icon-file">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>
                    <polyline points="13 2 13 9 20 9"/>
                  </svg>
                </div>
                <div class="meta-content">
                  <span class="meta-label">Archivo</span>
                  <a :href="getArchivoUrl(manualDetalle.id)" target="_blank" class="link-archivo">
                    {{ manualDetalle.archivo_nombre }}
                  </a>
                </div>
              </div>
              <div v-if="manualDetalle.enlace_url" class="meta-item">
                <div class="meta-icon meta-icon-link">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                    <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
                  </svg>
                </div>
                <div class="meta-content">
                  <span class="meta-label">Enlace</span>
                  <a :href="manualDetalle.enlace_url" target="_blank" class="link-externo">
                    {{ manualDetalle.enlace_url }}
                  </a>
                </div>
              </div>
              <div class="meta-item">
                <div class="meta-icon meta-icon-users">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                    <circle cx="9" cy="7" r="4"/>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                  </svg>
                </div>
                <div class="meta-content">
                  <span class="meta-label">Destinatarios</span>
                  <span class="meta-value">{{ manualDetalle.enviado_a_todos ? 'Todos los usuarios' : `${manualDetalle.destinatarios?.length || 0} usuarios específicos` }}</span>
                </div>
              </div>
              <div class="meta-item">
                <div class="meta-icon meta-icon-read">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
                    <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
                  </svg>
                </div>
                <div class="meta-content">
                  <span class="meta-label">Lecturas</span>
                  <span class="meta-value">{{ manualDetalle.total_lecturas }} usuarios</span>
                </div>
              </div>
              <div class="meta-item">
                <div class="meta-icon meta-icon-date">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                    <line x1="16" y1="2" x2="16" y2="6"/>
                    <line x1="8" y1="2" x2="8" y2="6"/>
                    <line x1="3" y1="10" x2="21" y2="10"/>
                  </svg>
                </div>
                <div class="meta-content">
                  <span class="meta-label">Fecha de creación</span>
                  <span class="meta-value">{{ formatearFecha(manualDetalle.fecha_creacion) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Estadísticas -->
    <div v-if="mostrarModalEstadisticas" class="modal-overlay" @click="cerrarModalEstadisticas">
      <div class="modal-content modal-large" @click.stop>
        <div class="modal-header">
          <div class="modal-header-content">
            <div class="modal-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 20V10"/>
                <path d="M12 20V4"/>
                <path d="M6 20v-6"/>
              </svg>
            </div>
            <div class="modal-title-section">
              <h3>Estadísticas de Lectura</h3>
              <p class="modal-description">Análisis detallado de lecturas y compromisos</p>
            </div>
          </div>
          <button class="btn-close" @click="cerrarModalEstadisticas">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="modal-body" v-if="estadisticas">
          <div class="stats-header">
            <h2 class="stats-title">{{ estadisticas.titulo }}</h2>
            <div class="stats-summary">
              <div class="stat-card stat-card-primary">
                <div class="stat-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
                    <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
                  </svg>
                </div>
                <div class="stat-content">
                  <span class="stat-value">{{ estadisticas.total_lecturas }}</span>
                  <span class="stat-label">Lecturas</span>
                </div>
              </div>
              <div class="stat-card stat-card-success">
                <div class="stat-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                    <circle cx="9" cy="7" r="4"/>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                  </svg>
                </div>
                <div class="stat-content">
                  <span class="stat-value">{{ estadisticas.total_destinatarios }}</span>
                  <span class="stat-label">Destinatarios</span>
                </div>
              </div>
              <div class="stat-card stat-card-info">
                <div class="stat-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/>
                    <polyline points="12 6 12 12 16 14"/>
                  </svg>
                </div>
                <div class="stat-content">
                  <span class="stat-value">{{ estadisticas.porcentaje_lectura }}%</span>
                  <span class="stat-label">Completado</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="stats-lists">
            <div class="stats-column">
              <div class="stats-column-header">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
                <h4>Usuarios que leyeron</h4>
                <span class="stats-count">{{ estadisticas.lecturas.length }}</span>
              </div>
              <div class="users-list">
                <div v-for="lectura in estadisticas.lecturas" :key="lectura.usuario_id" class="user-item read">
                  <div class="user-avatar">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                      <circle cx="12" cy="7" r="4"/>
                    </svg>
                  </div>
                  <div class="user-details">
                    <span class="user-name">{{ lectura.nombre || lectura.correo }}</span>
                    <span class="read-date">{{ formatearFecha(lectura.fecha_lectura) }}</span>
                  </div>
                </div>
                <div v-if="estadisticas.lecturas.length === 0" class="no-users">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="8" x2="12" y2="12"/>
                    <line x1="12" y1="16" x2="12.01" y2="16"/>
                  </svg>
                  <p>Ningún usuario ha leído este manual aún</p>
                </div>
              </div>
            </div>
            
            <div v-if="!estadisticas.enviado_a_todos" class="stats-column">
              <div class="stats-column-header stats-column-header-warning">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12 6 12 12 16 14"/>
                </svg>
                <h4>Pendientes de leer</h4>
                <span class="stats-count">{{ estadisticas.no_leidos.length }}</span>
              </div>
              <div class="users-list">
                <div v-for="usuario in estadisticas.no_leidos" :key="usuario.usuario_id" class="user-item pending">
                  <div class="user-avatar">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                      <circle cx="12" cy="7" r="4"/>
                    </svg>
                  </div>
                  <div class="user-details">
                    <span class="user-name">{{ usuario.nombre || usuario.correo }}</span>
                  </div>
                </div>
                <div v-if="estadisticas.no_leidos.length === 0" class="no-users no-users-success">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                    <polyline points="22 4 12 14.01 9 11.01"/>
                  </svg>
                  <p>¡Todos los usuarios han leído el manual!</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Confirmar Eliminar -->
    <div v-if="mostrarModalEliminar" class="modal-overlay" @click="cerrarModalEliminar">
      <div class="modal-content modal-small" @click.stop>
        <div class="modal-header modal-header-danger">
          <div class="modal-header-content">
            <div class="modal-icon modal-icon-danger">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="3 6 5 6 21 6"/>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                <line x1="10" y1="11" x2="10" y2="17"/>
                <line x1="14" y1="11" x2="14" y2="17"/>
              </svg>
            </div>
            <div class="modal-title-section">
              <h3>Confirmar Eliminación</h3>
            </div>
          </div>
          <button class="btn-close" @click="cerrarModalEliminar">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <p class="confirm-text">
            ¿Estás seguro de eliminar el manual <strong>"{{ manualAEliminar?.titulo }}"</strong>?
          </p>
          <p class="confirm-warning">Esta acción no se puede deshacer.</p>
          <div class="form-actions">
            <button type="button" class="btn-secondary" @click="cerrarModalEliminar">Cancelar</button>
            <button type="button" class="btn-danger" @click="eliminarManual" :disabled="eliminando">
              {{ eliminando ? 'Eliminando...' : 'Eliminar' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Editar Manual -->
    <Transition name="modal-fade">
    <div v-if="mostrarModalEditar" class="modal-overlay" @click="cerrarModalEditar">
      <div class="modal-content modal-editar" @click.stop>
        <div class="modal-header modal-header-editar">
          <div class="modal-header-content">
            <div class="modal-icon modal-icon-editar">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
            </div>
            <div class="modal-title-section">
              <h3>Editar Manual</h3>
              <p class="modal-description">Modifica la información del manual</p>
            </div>
          </div>
          <button class="btn-close" @click="cerrarModalEditar" :disabled="cargandoEdicion">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <!-- Loading State -->
          <div v-if="cargandoEdicion" class="modal-loading">
            <div class="loading-spinner-modal"></div>
            <p>Cargando datos del manual...</p>
          </div>
          
          <!-- Formulario -->
          <form v-else @submit.prevent="confirmarActualizacion">
            <div class="form-row">
              <!-- Título -->
              <div class="form-group">
                <label for="titulo-edit">Título *</label>
                <input
                  id="titulo-edit"
                  v-model="formManual.titulo"
                  type="text"
                  class="form-input"
                  placeholder="Título del manual"
                  maxlength="200"
                  required
                />
                <small class="char-count">{{ formManual.titulo.length }}/200</small>
              </div>

              <!-- Subtítulo -->
              <div class="form-group">
                <label for="subtitulo-edit">Subtítulo</label>
                <input
                  id="subtitulo-edit"
                  v-model="formManual.subtitulo"
                  type="text"
                  class="form-input"
                  placeholder="Subtítulo opcional"
                  maxlength="300"
                />
              </div>
            </div>

            <!-- Descripción -->
            <div class="form-group">
              <label for="descripcion-edit">Descripción</label>
              <textarea
                id="descripcion-edit"
                v-model="formManual.descripcion"
                class="form-textarea"
                placeholder="Descripción detallada del manual..."
                rows="3"
              ></textarea>
            </div>

            <!-- URL -->
            <div class="form-group">
              <label for="enlace_url-edit">Enlace URL (opcional)</label>
              <input
                id="enlace_url-edit"
                v-model="formManual.enlace_url"
                type="url"
                class="form-input"
                placeholder="https://ejemplo.com/recurso"
              />
            </div>

            <!-- Archivo PDF -->
            <div class="form-group">
              <label>Archivo PDF/Documento</label>
              <div v-if="manualEditando && manualEditando.archivo_nombre && mantenerArchivoExistente" class="file-current">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                </svg>
                <span>{{ manualEditando.archivo_nombre }}</span>
                <button type="button" class="btn-remove-file" @click="removerArchivoExistente">×</button>
              </div>
              <div v-else class="file-upload-area file-upload-compact" @click="$refs.archivoInputEdit.click()">
                <input
                  ref="archivoInputEdit"
                  type="file"
                  accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx"
                  @change="handleArchivoChange"
                  hidden
                />
                <div v-if="!archivoSeleccionado" class="upload-placeholder">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                    <line x1="12" y1="18" x2="12" y2="12"/>
                    <line x1="9" y1="15" x2="15" y2="15"/>
                  </svg>
                  <span>Clic para {{ manualEditando && manualEditando.archivo_nombre ? 'cambiar' : 'subir' }} PDF</span>
                </div>
                <div v-else class="file-selected">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                  </svg>
                  <span>{{ archivoSeleccionado.name }}</span>
                  <button type="button" class="btn-remove-file" @click.stop="removerArchivo">×</button>
                </div>
              </div>
            </div>

            <!-- Selector de Media (Imagen o Video) -->
            <div class="form-group">
              <label>Multimedia de Portada</label>
              <div class="media-type-selector media-selector-compact">
                <label class="media-option" :class="{ active: tipoMedia === 'ninguno' }">
                  <input type="radio" v-model="tipoMedia" value="ninguno" @change="cambiarTipoMedia" hidden />
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
                  </svg>
                  <span>Ninguno</span>
                </label>
                <label class="media-option" :class="{ active: tipoMedia === 'imagen' }">
                  <input type="radio" v-model="tipoMedia" value="imagen" @change="cambiarTipoMedia" hidden />
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                    <circle cx="8.5" cy="8.5" r="1.5"/>
                    <polyline points="21 15 16 10 5 21"/>
                  </svg>
                  <span>Imagen</span>
                </label>
                <label class="media-option" :class="{ active: tipoMedia === 'video' }">
                  <input type="radio" v-model="tipoMedia" value="video" @change="cambiarTipoMedia" hidden />
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polygon points="23 7 16 12 23 17 23 7"/>
                    <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
                  </svg>
                  <span>Video</span>
                </label>
              </div>
              
              <!-- Subir Imagen -->
              <div v-if="tipoMedia === 'imagen'" class="media-upload-compact">
                <div v-if="manualEditando && manualEditando.imagen_nombre && mantenerImagenExistente" class="file-current">
                  <img v-if="manualEditando.imagen_nombre" :src="getImagenUrl(manualEditando.id)" alt="Preview" class="image-preview-small" />
                  <span>{{ manualEditando.imagen_nombre }}</span>
                  <button type="button" class="btn-remove-file" @click="removerImagenExistente">×</button>
                </div>
                <div v-else class="file-upload-area file-upload-compact" @click="$refs.imagenInputEdit.click()">
                  <input
                    ref="imagenInputEdit"
                    type="file"
                    accept="image/*"
                    @change="handleImagenChange"
                    hidden
                  />
                  <div v-if="!imagenSeleccionada" class="upload-placeholder">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                      <circle cx="8.5" cy="8.5" r="1.5"/>
                      <polyline points="21 15 16 10 5 21"/>
                    </svg>
                    <span>Subir imagen</span>
                  </div>
                  <div v-else class="file-selected">
                    <img :src="imagenPreview" alt="Preview" class="image-preview-small" />
                    <span>{{ imagenSeleccionada.name }}</span>
                    <button type="button" class="btn-remove-file" @click.stop="removerImagen">×</button>
                  </div>
                </div>
              </div>
              
              <!-- Subir Video -->
              <div v-if="tipoMedia === 'video'" class="media-upload-compact">
                <div v-if="manualEditando && manualEditando.video_nombre && mantenerVideoExistente" class="file-current">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="2">
                    <polygon points="23 7 16 12 23 17 23 7"/>
                    <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
                  </svg>
                  <span>{{ manualEditando.video_nombre }}</span>
                  <button type="button" class="btn-remove-file" @click="removerVideoExistente">×</button>
                </div>
                <div v-else class="file-upload-area file-upload-compact" @click="$refs.videoInputEdit.click()">
                  <input
                    ref="videoInputEdit"
                    type="file"
                    accept=".mp4,.webm,.mov,.avi,.mkv"
                    @change="handleVideoChange"
                    hidden
                  />
                  <div v-if="!videoSeleccionado" class="upload-placeholder">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polygon points="23 7 16 12 23 17 23 7"/>
                      <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
                    </svg>
                    <span>Subir video</span>
                  </div>
                  <div v-else class="file-selected">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="2">
                      <polygon points="23 7 16 12 23 17 23 7"/>
                      <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
                    </svg>
                    <span>{{ videoSeleccionado.name }}</span>
                    <button type="button" class="btn-remove-file" @click.stop="removerVideo">×</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Destinatarios -->
            <div class="form-group">
              <label>Destinatarios</label>
              <div class="destinatarios-options">
                <label class="radio-option">
                  <input type="radio" v-model="formManual.enviado_a_todos" :value="true" />
                  <span class="radio-label">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                      <circle cx="9" cy="7" r="4"/>
                      <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                      <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                    </svg>
                    Todos los usuarios
                  </span>
                </label>
                <label class="radio-option">
                  <input type="radio" v-model="formManual.enviado_a_todos" :value="false" />
                  <span class="radio-label">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                      <circle cx="12" cy="7" r="4"/>
                    </svg>
                    Usuarios específicos
                  </span>
                </label>
              </div>
            </div>

            <!-- Selector de usuarios -->
            <div v-if="!formManual.enviado_a_todos" class="form-group usuarios-selector">
              <label>Seleccionar Usuarios</label>
              <div class="usuarios-search">
                <input
                  v-model="busquedaUsuario"
                  type="text"
                  class="form-input"
                  placeholder="Buscar usuario..."
                />
              </div>
              <div class="usuarios-list">
                <label 
                  v-for="usuario in usuariosFiltrados" 
                  :key="usuario.id" 
                  class="usuario-checkbox"
                >
                  <input 
                    type="checkbox" 
                    :value="usuario.id" 
                    v-model="formManual.usuario_ids"
                  />
                  <span class="usuario-info">
                    <span class="usuario-nombre">{{ usuario.nombre_completo || usuario.correo }}</span>
                    <span class="usuario-correo">{{ usuario.correo }}</span>
                  </span>
                </label>
              </div>
              <div class="usuarios-selected-count">
                {{ formManual.usuario_ids.length }} usuario(s) seleccionado(s)
              </div>
            </div>

            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="cerrarModalEditar">Cancelar</button>
              <button type="submit" class="btn-primary btn-guardar">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
                  <polyline points="17 21 17 13 7 13 7 21"/>
                  <polyline points="7 3 7 8 15 8"/>
                </svg>
                Guardar Cambios
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    </Transition>

    <!-- Modal Confirmación de Edición -->
    <div v-if="mostrarModalConfirmarEdicion" class="modal-overlay mini-modal" @click="cerrarConfirmacionEdicion">
      <div class="modal-content modal-confirm" @click.stop>
        <div class="modal-header modal-confirm-header">
          <div class="modal-icon-confirm">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </div>
          <h3>¿Confirmar cambios?</h3>
        </div>
        <div class="modal-body-confirm">
          <p>¿Estás seguro de que deseas actualizar este manual?</p>
          <p class="confirm-detail">Los cambios se reflejarán inmediatamente para todos los usuarios.</p>
        </div>
        <div class="modal-actions-confirm">
          <button class="btn-cancel" @click="cerrarConfirmacionEdicion" :disabled="editando">
            Cancelar
          </button>
          <button class="btn-confirm-primary" @click="actualizarManual" :disabled="editando">
            <span v-if="editando" class="spinner"></span>
            {{ editando ? 'Guardando...' : 'Sí, Actualizar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de Feedback (Éxito/Error) -->
    <Transition name="fade">
      <div v-if="mostrarModalFeedback" class="feedback-overlay" @click="cerrarFeedback">
        <div class="feedback-modal" :class="feedbackTipo" @click.stop>
          <div class="feedback-icon">
            <svg v-if="feedbackTipo === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <circle cx="12" cy="12" r="10"/>
              <line x1="15" y1="9" x2="9" y2="15"/>
              <line x1="9" y1="9" x2="15" y2="15"/>
            </svg>
          </div>
          <h4 class="feedback-title">{{ feedbackTitulo }}</h4>
          <p class="feedback-message">{{ feedbackMensaje }}</p>
          <button class="feedback-btn" :class="feedbackTipo" @click="cerrarFeedback">
            Aceptar
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import authService from '../services/authService'
import manualesService from '../services/manualesService'
import usuariosService from '../services/usuariosService'
import { API_URL } from '../config/api.js'

export default {
  name: 'ManualesView',
  components: { Sidebar },
  
  setup() {
    const router = useRouter()
    
    // Estados
    const cargando = ref(false)
    const error = ref(null)
    const manuales = ref([])
    const usuarios = ref([])
    
    // Modales
    const mostrarModalCrear = ref(false)
    const mostrarModalEditar = ref(false)
    const mostrarModalConfirmarEdicion = ref(false)
    const mostrarModalDetalle = ref(false)
    const mostrarModalEstadisticas = ref(false)
    const mostrarModalEliminar = ref(false)
    const manualEditando = ref(null)
    
    // Modal de feedback
    const mostrarModalFeedback = ref(false)
    const feedbackTipo = ref('success') // 'success' o 'error'
    const feedbackTitulo = ref('')
    const feedbackMensaje = ref('')
    
    const mostrarFeedback = (tipo, titulo, mensaje) => {
      feedbackTipo.value = tipo
      feedbackTitulo.value = titulo
      feedbackMensaje.value = mensaje
      mostrarModalFeedback.value = true
    }
    
    const cerrarFeedback = () => {
      mostrarModalFeedback.value = false
    }
    
    // Datos de modales
    const manualDetalle = ref(null)
    const estadisticas = ref(null)
    const manualAEliminar = ref(null)
    
    // Formulario
    const formManual = ref({
      titulo: '',
      subtitulo: '',
      descripcion: '',
      enlace_url: '',
      enviado_a_todos: true,
      usuario_ids: []
    })
    
    const archivoSeleccionado = ref(null)
    const imagenSeleccionada = ref(null)
    const imagenPreview = ref(null)
    const videoSeleccionado = ref(null)
    const tipoMedia = ref('ninguno') // 'ninguno', 'imagen', 'video'
    const enviando = ref(false)
    const eliminando = ref(false)
    const busquedaUsuario = ref('')
    const editando = ref(false)
    const cargandoEdicion = ref(false)
    const mantenerArchivoExistente = ref(true)
    const mantenerImagenExistente = ref(true)
    const mantenerVideoExistente = ref(true)
    
    // Permisos
    const userPermisos = computed(() => authService.getCurrentUser()?.permisos || {})
    const userRol = computed(() => authService.getUserRole())
    
    const puedeCrearManuales = computed(() => {
      if (userRol.value === 'super_admin' || userRol.value === 'admin') return true
      return userPermisos.value?.manuales_crear === true
    })
    
    const puedeEliminar = computed(() => {
      if (userRol.value === 'super_admin' || userRol.value === 'admin') return true
      return userPermisos.value?.manuales_acciones === true
    })
    
    // Usuarios filtrados
    const usuariosFiltrados = computed(() => {
      if (!busquedaUsuario.value) return usuarios.value
      const busqueda = busquedaUsuario.value.toLowerCase()
      return usuarios.value.filter(u => 
        (u.nombre_completo && u.nombre_completo.toLowerCase().includes(busqueda)) ||
        (u.correo && u.correo.toLowerCase().includes(busqueda))
      )
    })
    
    // Cargar manuales
    const cargarManuales = async () => {
      cargando.value = true
      error.value = null
      try {
        const response = await manualesService.listarManuales()
        manuales.value = response.manuales || []
      } catch (err) {
        error.value = err.response?.data?.detail || 'Error al cargar manuales'
        console.error('Error:', err)
      } finally {
        cargando.value = false
      }
    }
    
    // Cargar usuarios
    const cargarUsuarios = async () => {
      try {
        const response = await usuariosService.obtenerUsuarios()
        usuarios.value = response.usuarios || response || []
      } catch (err) {
        console.error('Error cargando usuarios:', err)
      }
    }
    
    // Handlers de archivos
    const handleArchivoChange = (event) => {
      const file = event.target.files[0]
      if (file) {
        archivoSeleccionado.value = file
      }
    }
    
    const handleImagenChange = (event) => {
      const file = event.target.files[0]
      if (file) {
        imagenSeleccionada.value = file
        const reader = new FileReader()
        reader.onload = (e) => {
          imagenPreview.value = e.target.result
        }
        reader.readAsDataURL(file)
      }
    }
    
    const removerArchivo = () => {
      archivoSeleccionado.value = null
    }
    
    const removerImagen = () => {
      imagenSeleccionada.value = null
      imagenPreview.value = null
    }
    
    const handleVideoChange = (event) => {
      const file = event.target.files[0]
      if (file) {
        // Validar extensión
        const extensionesPermitidas = ['.mp4', '.webm', '.mov', '.avi', '.mkv']
        const extension = file.name.toLowerCase().slice(file.name.lastIndexOf('.'))
        if (!extensionesPermitidas.includes(extension)) {
          alert('Formato de video no permitido. Use: MP4, WEBM, MOV, AVI o MKV')
          return
        }
        // Validar tamaño (max 100MB)
        if (file.size > 100 * 1024 * 1024) {
          alert('El video no puede superar los 100MB')
          return
        }
        videoSeleccionado.value = file
      }
    }
    
    const removerVideo = () => {
      videoSeleccionado.value = null
    }
    
    // Crear manual
    const crearManual = async () => {
      if (!formManual.value.titulo.trim()) {
        alert('El título es obligatorio')
        return
      }
      
      if (!formManual.value.enviado_a_todos && formManual.value.usuario_ids.length === 0) {
        alert('Debe seleccionar al menos un usuario')
        return
      }
      
      enviando.value = true
      try {
        await manualesService.crearManual(
          formManual.value,
          archivoSeleccionado.value,
          tipoMedia.value === 'imagen' ? imagenSeleccionada.value : null,
          tipoMedia.value === 'video' ? videoSeleccionado.value : null
        )
        
        cerrarModalCrear()
        await cargarManuales()
        mostrarFeedback('success', '¡Manual Creado!', 'El manual se ha publicado correctamente y ya está disponible para los usuarios.')
      } catch (err) {
        console.error('Error:', err)
        
        // Determinar mensaje de error más descriptivo
        let mensajeError = 'Error desconocido al crear el manual'
        
        if (err.code === 'ERR_NETWORK') {
          if (err.message?.includes('413') || err.request?.status === 413) {
            mensajeError = 'El archivo es demasiado grande. El límite es de 50MB para documentos y 10MB para imágenes.'
          } else {
            mensajeError = 'Error de conexión. Verifica tu conexión a internet e intenta de nuevo.'
          }
        } else if (err.response?.status === 413) {
          mensajeError = 'El archivo es demasiado grande. El límite es de 50MB para documentos y 10MB para imágenes.'
        } else if (err.response?.data?.detail) {
          mensajeError = err.response.data.detail
        }
        
        mostrarFeedback('error', 'Error al Crear', mensajeError)
      } finally {
        enviando.value = false
      }
    }
    
    // Ver detalle
    const verDetalle = async (manual) => {
      try {
        manualDetalle.value = await manualesService.obtenerManual(manual.id)
        mostrarModalDetalle.value = true
      } catch (err) {
        alert('Error al cargar detalle')
      }
    }
    
    // Ver estadísticas
    const verEstadisticas = async (manual) => {
      try {
        estadisticas.value = await manualesService.obtenerEstadisticas(manual.id)
        mostrarModalEstadisticas.value = true
      } catch (err) {
        alert('Error al cargar estadísticas')
      }
    }
    
    // Eliminar
    const confirmarEliminar = (manual) => {
      manualAEliminar.value = manual
      mostrarModalEliminar.value = true
    }
    
    const eliminarManual = async () => {
      if (!manualAEliminar.value) return
      eliminando.value = true
      try {
        await manualesService.eliminarManual(manualAEliminar.value.id)
        cerrarModalEliminar()
        await cargarManuales()
      } catch (err) {
        alert('Error al eliminar manual')
      } finally {
        eliminando.value = false
      }
    }
    
    // Editar manual
    const abrirModalEditar = async (manual) => {
      // Abrir modal inmediatamente con loading
      mostrarModalEditar.value = true
      cargandoEdicion.value = true
      
      // Pre-llenar con datos básicos disponibles
      formManual.value = {
        titulo: manual.titulo || '',
        subtitulo: manual.subtitulo || '',
        descripcion: '',
        enlace_url: '',
        enviado_a_todos: true,
        usuario_ids: []
      }
      
      try {
        // Obtener detalle completo del manual
        manualEditando.value = await manualesService.obtenerManual(manual.id)
        
        // Pre-llenar formulario con datos completos
        formManual.value = {
          titulo: manualEditando.value.titulo || '',
          subtitulo: manualEditando.value.subtitulo || '',
          descripcion: manualEditando.value.descripcion || '',
          enlace_url: manualEditando.value.enlace_url || '',
          enviado_a_todos: manualEditando.value.enviado_a_todos,
          usuario_ids: manualEditando.value.usuario_ids || []
        }
        
        // Resetear archivos nuevos
        archivoSeleccionado.value = null
        imagenSeleccionada.value = null
        imagenPreview.value = null
        videoSeleccionado.value = null
        
        // Determinar tipo de media existente
        if (manualEditando.value.imagen_nombre) {
          tipoMedia.value = 'imagen'
          mantenerImagenExistente.value = true
        } else if (manualEditando.value.video_nombre) {
          tipoMedia.value = 'video'
          mantenerVideoExistente.value = true
        } else {
          tipoMedia.value = 'ninguno'
        }
        
        mantenerArchivoExistente.value = !!manualEditando.value.archivo_nombre
        
      } catch (err) {
        mostrarModalEditar.value = false
        mostrarFeedback('error', 'Error', 'No se pudo cargar el manual para editar')
        console.error(err)
      } finally {
        cargandoEdicion.value = false
      }
    }
    
    const confirmarActualizacion = () => {
      if (!formManual.value.titulo.trim()) {
        alert('El título es obligatorio')
        return
      }
      
      if (!formManual.value.enviado_a_todos && formManual.value.usuario_ids.length === 0) {
        alert('Debe seleccionar al menos un usuario')
        return
      }
      
      mostrarModalConfirmarEdicion.value = true
    }
    
    const actualizarManual = async () => {
      editando.value = true
      try {
        await manualesService.actualizarManual(
          manualEditando.value.id,
          formManual.value,
          archivoSeleccionado.value,
          tipoMedia.value === 'imagen' ? imagenSeleccionada.value : null,
          tipoMedia.value === 'video' ? videoSeleccionado.value : null,
          mantenerArchivoExistente.value,
          tipoMedia.value === 'imagen' ? mantenerImagenExistente.value : false,
          tipoMedia.value === 'video' ? mantenerVideoExistente.value : false
        )
        
        cerrarModalEditar()
        cerrarConfirmacionEdicion()
        await cargarManuales()
        mostrarFeedback('success', '¡Manual Actualizado!', 'El manual se ha actualizado correctamente.')
      } catch (err) {
        console.error('Error:', err)
        
        let mensajeError = 'Error desconocido al actualizar el manual'
        
        if (err.code === 'ERR_NETWORK') {
          if (err.message?.includes('413') || err.request?.status === 413) {
            mensajeError = 'El archivo es demasiado grande. El límite es de 50MB para documentos y 10MB para imágenes.'
          } else {
            mensajeError = 'Error de conexión. Verifica tu conexión a internet e intenta de nuevo.'
          }
        } else if (err.response?.status === 413) {
          mensajeError = 'El archivo es demasiado grande. El límite es de 50MB para documentos y 10MB para imágenes.'
        } else if (err.response?.data?.detail) {
          mensajeError = err.response.data.detail
        }
        
        mostrarFeedback('error', 'Error al Actualizar', mensajeError)
      } finally {
        editando.value = false
      }
    }
    
    const cerrarModalEditar = () => {
      mostrarModalEditar.value = false
      manualEditando.value = null
      formManual.value = {
        titulo: '',
        subtitulo: '',
        descripcion: '',
        enlace_url: '',
        enviado_a_todos: true,
        usuario_ids: []
      }
      archivoSeleccionado.value = null
      imagenSeleccionada.value = null
      imagenPreview.value = null
      videoSeleccionado.value = null
      tipoMedia.value = 'ninguno'
      mantenerArchivoExistente.value = true
      mantenerImagenExistente.value = true
      mantenerVideoExistente.value = true
    }
    
    const cerrarConfirmacionEdicion = () => {
      mostrarModalConfirmarEdicion.value = false
    }
    
    const removerArchivoExistente = () => {
      mantenerArchivoExistente.value = false
    }
    
    const removerImagenExistente = () => {
      mantenerImagenExistente.value = false
      tipoMedia.value = 'ninguno'
    }
    
    const removerVideoExistente = () => {
      mantenerVideoExistente.value = false
      tipoMedia.value = 'ninguno'
    }
    
    const cambiarTipoMedia = () => {
      if (tipoMedia.value === 'ninguno') {
        mantenerImagenExistente.value = false
        mantenerVideoExistente.value = false
      } else if (tipoMedia.value === 'imagen') {
        mantenerVideoExistente.value = false
      } else if (tipoMedia.value === 'video') {
        mantenerImagenExistente.value = false
      }
    }
    
    // URLs
    const getArchivoUrl = (id) => manualesService.getArchivoUrl(id)
    const getImagenUrl = (id) => manualesService.getImagenUrl(id)
    const getVideoUrl = (id) => manualesService.getVideoUrl(id)
    
    // Cerrar modales
    const cerrarModalCrear = () => {
      mostrarModalCrear.value = false
      formManual.value = {
        titulo: '',
        subtitulo: '',
        descripcion: '',
        enlace_url: '',
        enviado_a_todos: true,
        usuario_ids: []
      }
      archivoSeleccionado.value = null
      imagenSeleccionada.value = null
      imagenPreview.value = null
      videoSeleccionado.value = null
      tipoMedia.value = 'ninguno'
    }
    
    const cerrarModalDetalle = () => {
      mostrarModalDetalle.value = false
      manualDetalle.value = null
    }
    
    const cerrarModalEstadisticas = () => {
      mostrarModalEstadisticas.value = false
      estadisticas.value = null
    }
    
    const cerrarModalEliminar = () => {
      mostrarModalEliminar.value = false
      manualAEliminar.value = null
    }
    
    // Formato fecha
    const formatearFecha = (fecha) => {
      if (!fecha) return '—'
      const d = new Date(fecha)
      return d.toLocaleDateString('es-MX', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    // Logout
    const logout = () => {
      authService.logout()
      router.push('/login')
    }
    
    onMounted(() => {
      cargarManuales()
      cargarUsuarios()
    })
    
    return {
      cargando,
      error,
      manuales,
      usuarios,
      mostrarModalCrear,
      mostrarModalEditar,
      mostrarModalConfirmarEdicion,
      mostrarModalDetalle,
      mostrarModalEstadisticas,
      mostrarModalEliminar,
      manualDetalle,
      estadisticas,
      manualAEliminar,
      manualEditando,
      formManual,
      archivoSeleccionado,
      imagenSeleccionada,
      imagenPreview,
      videoSeleccionado,
      tipoMedia,
      enviando,
      editando,
      cargandoEdicion,
      eliminando,
      busquedaUsuario,
      mantenerArchivoExistente,
      mantenerImagenExistente,
      mantenerVideoExistente,
      puedeCrearManuales,
      puedeEliminar,
      usuariosFiltrados,
      cargarManuales,
      handleArchivoChange,
      handleImagenChange,
      handleVideoChange,
      removerArchivo,
      removerImagen,
      removerVideo,
      crearManual,
      verDetalle,
      verEstadisticas,
      confirmarEliminar,
      eliminarManual,
      abrirModalEditar,
      confirmarActualizacion,
      actualizarManual,
      cerrarModalEditar,
      cerrarConfirmacionEdicion,
      removerArchivoExistente,
      removerImagenExistente,
      removerVideoExistente,
      cambiarTipoMedia,
      getArchivoUrl,
      getImagenUrl,
      getVideoUrl,
      cerrarModalCrear,
      cerrarModalDetalle,
      cerrarModalEstadisticas,
      cerrarModalEliminar,
      formatearFecha,
      logout,
      mostrarModalFeedback,
      feedbackTipo,
      feedbackTitulo,
      feedbackMensaje,
      cerrarFeedback
    }
  }
}
</script>

<style scoped>
.manuales-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
}

.main-content {
  flex: 1;
  margin-left: min(220px, 18vw);
  width: calc(100vw - min(220px, 18vw));
  min-width: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: relative;
  box-sizing: border-box;
  overflow-x: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* === HEADER STYLES === */
.page-header {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 50%, #2E7D32 100%);
  color: white;
  padding: clamp(0.3rem, 0.8vw, 0.5rem);
  box-shadow: 
    0 2px 8px rgba(76, 175, 80, 0.3),
    0 4px 16px rgba(76, 175, 80, 0.15);
  position: sticky;
  top: 0;
  z-index: 100;
  width: 100%;
  box-sizing: border-box;
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
  z-index: 1;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 100%;
  margin: 0;
  gap: clamp(0.25rem, 0.8vw, 0.5rem);
  flex-wrap: wrap;
  width: 100%;
  position: relative;
  z-index: 2;
}

.header-main {
  display: flex;
  align-items: center;
  gap: clamp(0.5rem, 1.2vw, 0.8rem);
  flex: 1;
  min-width: 140px;
  margin-left: clamp(0.3rem, 1vw, 0.6rem);
}

.header-icon {
  width: clamp(28px, 3vw, 32px);
  height: clamp(28px, 3vw, 32px);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.1) 100%);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    inset 0 -1px 0 rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.header-icon svg {
  width: clamp(14px, 2.5vw, 16px);
  height: clamp(14px, 2.5vw, 16px);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  z-index: 1;
  position: relative;
}

.header-text {
  flex: 1;
}

.header-title {
  font-size: clamp(14px, 2.5vw, 16px);
  font-weight: 700;
  margin: 0 0 clamp(1px, 0.3vw, 2px) 0;
  background: linear-gradient(135deg, #ffffff 0%, #e8f5e8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-family: 'Inter', sans-serif;
  line-height: 1.2;
}

.header-subtitle {
  font-size: clamp(9px, 1.8vw, 11px);
  opacity: 0.9;
  margin: 0;
  font-weight: 400;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-family: 'Inter', sans-serif;
  line-height: 1.3;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: clamp(0.5rem, 1.2vw, 0.75rem);
  flex-shrink: 0;
}

.btn-primary {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.1) 100%);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: clamp(6px, 1vw, 8px) clamp(12px, 2vw, 14px);
  border-radius: clamp(12px, 2vw, 14px);
  font-weight: 600;
  font-size: clamp(10px, 1.8vw, 11px);
  display: flex;
  align-items: center;
  gap: clamp(4px, 0.8vw, 6px);
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.08),
    0 1px 4px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.4),
    inset 0 -1px 0 rgba(0, 0, 0, 0.1);
  font-family: 'Inter', sans-serif;
  white-space: nowrap;
  position: relative;
  overflow: hidden;
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.05) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: inherit;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.12),
    0 2px 8px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.5),
    inset 0 -1px 0 rgba(0, 0, 0, 0.15);
  border-color: rgba(255, 255, 255, 0.4);
}

.btn-primary:hover::before {
  opacity: 1;
}

.btn-primary svg {
  width: clamp(12px, 2vw, 14px);
  height: clamp(12px, 2vw, 14px);
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

/* Content */
.page-content {
  flex: 1;
  padding: 16px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.list-header h2 {
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.btn-refresh {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #f0f4f8;
  color: #64748b;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-refresh:hover {
  background: #e2e8f0;
  color: #475569;
}

/* Table */
.table-container {
  background: white;
  border-radius: 16px;
  overflow-x: auto;
  overflow-y: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  -webkit-overflow-scrolling: touch;
}

.manuales-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}

.manuales-table th {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  padding: 14px 16px;
  text-align: left;
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #e2e8f0;
}

.manuales-table td {
  padding: 16px;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}

.manual-row:hover {
  background: #f8fafc;
}

.manual-title {
  font-weight: 600;
  color: #1e293b;
}

.manual-subtitle, .no-subtitle {
  font-size: 13px;
  color: #64748b;
}

/* Badges */
.content-badges {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
}

.badge-pdf {
  background: #fef2f2;
  color: #dc2626;
}

.badge-img {
  background: #f0fdf4;
  color: #16a34a;
}

.badge-video {
  background: #fef3e2;
  color: #ea580c;
}

.badge-url {
  background: #eff6ff;
  color: #2563eb;
}

.badge-text {
  background: #f8fafc;
  color: #64748b;
}

.recipients-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  background: #f1f5f9;
  color: #475569;
}

.recipients-badge.all-users {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #1d4ed8;
}

.reads-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #64748b;
}

.manual-date {
  font-size: 13px;
  color: #64748b;
}

/* Actions */
.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-action {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.btn-view {
  background: #e0f2fe;
  color: #0284c7;
}

.btn-view:hover {
  background: #0284c7;
  color: white;
}

.btn-stats {
  background: #fef3c7;
  color: #d97706;
}

.btn-stats:hover {
  background: #d97706;
  color: white;
}

.btn-edit {
  background: #dbeafe;
  color: #2563eb;
}

.btn-edit:hover {
  background: #2563eb;
  color: white;
}

.btn-delete {
  background: #fee2e2;
  color: #dc2626;
}

.btn-delete:hover {
  background: #dc2626;
  color: white;
}

/* Loading & Empty States */
.loading-state, .empty-state, .error-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e2e8f0;
  border-top-color: #1a73e8;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon, .error-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border-radius: 50%;
  border: 3px solid #fca5a5;
}

.error-icon svg {
  width: 48px;
  height: 48px;
  stroke: #dc2626;
}

/* Modales */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: white;
  border-radius: 20px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-large {
  max-width: 800px;
}

/* Modal Editar */
.modal-editar {
  max-width: 720px;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  0% {
    opacity: 0;
    transform: translateY(30px) scale(0.98);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header-editar {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 50%, #1e40af 100%);
}

.modal-icon-editar {
  background: rgba(255, 255, 255, 0.2) !important;
}

.modal-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  gap: 16px;
}

.loading-spinner-modal {
  width: 44px;
  height: 44px;
  border: 4px solid #e5e7eb;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.modal-loading p {
  color: #6b7280;
  font-size: 14px;
  margin: 0;
}

/* Modal Fade Transition */
.modal-fade-enter-active {
  animation: modalFadeIn 0.25s ease-out;
}

.modal-fade-leave-active {
  animation: modalFadeOut 0.2s ease-in;
}

@keyframes modalFadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

@keyframes modalFadeOut {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

.btn-guardar {
  display: flex;
  align-items: center;
  gap: 6px;
}

/* Estilos compactos para modal editar */
.modal-editar .modal-body {
  overflow-x: hidden;
  max-height: 70vh;
  overflow-y: auto;
}

.file-upload-compact {
  padding: 12px 16px !important;
  min-height: auto !important;
}

.file-upload-compact .upload-placeholder {
  flex-direction: row !important;
  gap: 10px !important;
}

.file-upload-compact .upload-placeholder span {
  font-size: 13px !important;
}

.media-selector-compact {
  gap: 6px !important;
  flex-wrap: wrap;
}

.media-selector-compact .media-option {
  padding: 6px 10px !important;
  font-size: 12px !important;
  flex: 0 1 auto !important;
  min-width: 70px;
}

.media-selector-compact .media-option span {
  font-size: 12px !important;
}

.media-upload-compact {
  margin-top: 10px;
}

.modal-editar .file-current {
  max-width: 100%;
  overflow: hidden;
}

.modal-editar .file-current span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 200px;
}

.modal-editar .file-selected span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 180px;
}

.btn-guardar svg {
  flex-shrink: 0;
}

.modal-small {
  max-width: 450px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 50%, #2E7D32 100%);
  color: white;
  border-radius: 20px 20px 0 0;
  position: relative;
  overflow: hidden;
}

.modal-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
  z-index: 1;
}

.modal-header-content {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  position: relative;
  z-index: 2;
}

.modal-icon {
  width: 38px;
  height: 38px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.1) 100%);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    inset 0 -1px 0 rgba(0, 0, 0, 0.1),
    0 4px 12px rgba(0, 0, 0, 0.15);
  flex-shrink: 0;
}

.modal-icon svg {
  width: 20px;
  height: 20px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.modal-title-section {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.modal-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  background: linear-gradient(135deg, #ffffff 0%, #e8f5e8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-family: 'Inter', sans-serif;
  line-height: 1.3;
}

.modal-description {
  margin: 0;
  font-size: 11px;
  opacity: 0.9;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.95);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  line-height: 1.3;
}

.modal-header-danger {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 50%, #991b1b 100%);
}

.modal-icon-danger {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.1) 100%);
  border-color: rgba(255, 255, 255, 0.3);
}

.btn-close {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  position: relative;
  z-index: 2;
  flex-shrink: 0;
}

.btn-close:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.3);
  transform: rotate(90deg);
}

.btn-close svg {
  width: 16px;
  height: 16px;
}

.modal-body {
  padding: 20px 24px;
  background: linear-gradient(135deg, #fafafa 0%, #ffffff 100%);
}

/* Form */
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  margin-bottom: 18px;
}

.form-group label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 7px;
  display: flex;
  align-items: center;
  gap: 6px;
  line-height: 1.3;
}

.form-input, .form-textarea {
  width: 100%;
  padding: 10px 14px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 13px;
  transition: all 0.2s ease;
  box-sizing: border-box;
  background: white;
  font-family: 'Inter', sans-serif;
  line-height: 1.4;
}

.form-input:focus, .form-textarea:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
  background: #fafffe;
}

.form-textarea {
  resize: vertical;
  min-height: 85px;
}

.char-count {
  font-size: 10px;
  color: #9ca3af;
  text-align: right;
  display: block;
  margin-top: 3px;
}

/* Media Type Selector */
.media-type-selector {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.media-option {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 10px 8px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
  line-height: 1.2;
}

.media-option:hover {
  border-color: #4CAF50;
  background: #f8fffe;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.1);
}

.media-option.active {
  border-color: #4CAF50;
  background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
  color: #2E7D32;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.15);
}

.media-option.active svg {
  stroke: #2E7D32;
}

.media-option svg {
  stroke: #9ca3af;
  transition: stroke 0.2s ease;
}

/* File Upload */
.file-upload-area {
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  background: linear-gradient(135deg, #fafafa 0%, #ffffff 100%);
}

.file-upload-area:hover {
  border-color: #4CAF50;
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(76, 175, 80, 0.1);
}

.upload-placeholder {
  color: #6b7280;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.upload-placeholder svg {
  stroke: #9ca3af;
}

.upload-placeholder span {
  font-weight: 500;
  font-size: 12px;
  line-height: 1.3;
}

.file-selected {
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: center;
  font-size: 13px;
}

.file-selected span {
  line-height: 1.3;
}

.image-preview {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 6px;
}

.btn-remove-file {
  background: #fee2e2;
  color: #dc2626;
  border: none;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.btn-remove-file:hover {
  background: #fecaca;
}

/* Destinatarios */
.destinatarios-options {
  display: flex;
  gap: 12px;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 13px;
  color: #374151;
  line-height: 1.3;
}

/* Usuarios selector */
.usuarios-selector {
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  padding: 12px;
  background: #fafafa;
}

.usuarios-search {
  margin-bottom: 10px;
}

.usuarios-list {
  max-height: 180px;
  overflow-y: auto;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
}

.usuario-checkbox {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.usuario-checkbox:hover {
  background: #f3f4f6;
}

.usuario-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.usuario-nombre {
  font-weight: 500;
  color: #1f2937;
  font-size: 13px;
  line-height: 1.3;
}

.usuario-correo {
  font-size: 11px;
  color: #6b7280;
  line-height: 1.3;
}

.usuarios-selected-count {
  margin-top: 10px;
  font-size: 12px;
  color: #4CAF50;
  font-weight: 500;
}

/* Form actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
  padding-top: 18px;
  border-top: 2px solid #f0f0f0;
}

.btn-secondary {
  padding: 10px 22px;
  background: white;
  color: #374151;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 13px;
  font-family: 'Inter', sans-serif;
}

.btn-secondary:hover {
  background: #f9fafb;
  border-color: #d1d5db;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.form-actions .btn-primary {
  padding: 10px 22px;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: 'Inter', sans-serif;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2);
}

.form-actions .btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #45a049 0%, #388e3c 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(76, 175, 80, 0.3);
}

.form-actions .btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-danger {
  padding: 10px 22px;
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 13px;
  font-family: 'Inter', sans-serif;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.25);
}

.btn-danger:hover:not(:disabled) {
  background: linear-gradient(135deg, #b91c1c 0%, #991b1b 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(220, 38, 38, 0.35);
}

.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: inline-block;
  margin-right: 8px;
}

/* Detalle */
.detalle-header {
  margin-bottom: 18px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f0f0f0;
}

.detalle-title {
  color: #1e293b;
  margin: 0 0 6px;
  font-size: 20px;
  font-weight: 700;
  line-height: 1.2;
}

.detalle-subtitulo {
  color: #64748b;
  font-size: 13px;
  margin: 0;
  line-height: 1.3;
}

.detalle-media {
  margin: 16px auto;
  max-width: 480px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.detalle-imagen,
.detalle-video {
  width: 100%;
  height: auto;
  display: block;
}

.detalle-descripcion {
  margin: 18px 0;
  padding: 14px;
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
  border-radius: 10px;
  border-left: 3px solid #4CAF50;
}

.detalle-descripcion p {
  margin: 6px 0 0;
  color: #374151;
  font-size: 13px;
  line-height: 1.5;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.section-header svg {
  width: 18px;
  height: 18px;
  stroke: #4CAF50;
  flex-shrink: 0;
}

.section-header h4 {
  margin: 0;
  color: #1f2937;
  font-size: 14px;
  font-weight: 600;
  line-height: 1.2;
}

.detalle-meta {
  margin-top: 18px;
}

.meta-grid {
  display: grid;
  gap: 10px;
  margin-top: 10px;
}

.meta-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.meta-item:hover {
  border-color: #4CAF50;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.1);
  transform: translateY(-2px);
}

.meta-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.meta-icon svg {
  width: 18px;
  height: 18px;
}

.meta-icon-file {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
}

.meta-icon-file svg {
  stroke: #3b82f6;
}

.meta-icon-link {
  background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
}

.meta-icon-link svg {
  stroke: #6366f1;
}

.meta-icon-users {
  background: linear-gradient(135deg, #ddd6fe 0%, #c4b5fd 100%);
}

.meta-icon-users svg {
  stroke: #8b5cf6;
}

.meta-icon-read {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
}

.meta-icon-read svg {
  stroke: #10b981;
}

.meta-icon-date {
  background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
}

.meta-icon-date svg {
  stroke: #f59e0b;
}

.meta-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}

.meta-label {
  font-size: 11px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  line-height: 1.2;
}

.meta-value {
  color: #1f2937;
  font-size: 13px;
  font-weight: 500;
  word-break: break-word;
  line-height: 1.3;
}

.link-archivo,
.link-externo {
  color: #4CAF50;
  text-decoration: none;
  font-weight: 500;
  font-size: 13px;
  word-break: break-all;
  transition: all 0.2s ease;
  line-height: 1.3;
}

.link-archivo:hover,
.link-externo:hover {
  color: #45a049;
  text-decoration: underline;
}

/* Estadísticas */
.stats-header {
  margin-bottom: 28px;
}

.stats-title {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 16px;
  line-height: 1.3;
}

.stats-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 14px;
}

.stat-card {
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 14px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 14px;
  transition: all 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.stat-card-primary {
  border-color: #3b82f6;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
}

.stat-card-primary:hover {
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.2);
}

.stat-card-success {
  border-color: #4CAF50;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
}

.stat-card-success:hover {
  box-shadow: 0 8px 20px rgba(76, 175, 80, 0.2);
}

.stat-card-info {
  border-color: #8b5cf6;
  background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
}

.stat-card-info:hover {
  box-shadow: 0 8px 20px rgba(139, 92, 246, 0.2);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-card-primary .stat-icon {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.stat-card-success .stat-icon {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
}

.stat-card-info .stat-icon {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.stat-icon svg {
  width: 24px;
  height: 24px;
  stroke: white;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat-value {
  font-size: 28px;
  font-weight: 800;
  line-height: 1;
}

.stat-card-primary .stat-value {
  color: #1e40af;
}

.stat-card-success .stat-value {
  color: #2E7D32;
}

.stat-card-info .stat-value {
  color: #6b21a8;
}

.stat-label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #64748b;
}

.stats-lists {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.stats-column {
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 14px;
  overflow: hidden;
}

.stats-column-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-bottom: 2px solid #4CAF50;
}

.stats-column-header svg {
  width: 20px;
  height: 20px;
  stroke: #2E7D32;
  flex-shrink: 0;
}

.stats-column-header h4 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  flex: 1;
}

.stats-column-header-warning {
  background: linear-gradient(135deg, #fefce8 0%, #fef9c3 100%);
  border-bottom-color: #eab308;
}

.stats-column-header-warning svg {
  stroke: #a16207;
}

.stats-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 28px;
  height: 28px;
  padding: 0 10px;
  background: white;
  border-radius: 14px;
  font-size: 13px;
  font-weight: 700;
  color: #2E7D32;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.stats-column-header-warning .stats-count {
  color: #a16207;
}

.users-list {
  max-height: 320px;
  overflow-y: auto;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-bottom: 1px solid #f1f5f9;
  transition: background 0.2s ease;
}

.user-item:last-child {
  border-bottom: none;
}

.user-item:hover {
  background: #f8fafc;
}

.user-item.read {
  background: linear-gradient(135deg, #f0fdf4 0%, rgba(240, 253, 244, 0.3) 100%);
}

.user-item.read:hover {
  background: #f0fdf4;
}

.user-item.pending {
  background: linear-gradient(135deg, #fefce8 0%, rgba(254, 252, 232, 0.3) 100%);
}

.user-item.pending:hover {
  background: #fefce8;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border: 2px solid #e5e7eb;
}

.user-item.read .user-avatar {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  border-color: #2E7D32;
}

.user-item.pending .user-avatar {
  background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%);
  border-color: #a16207;
}

.user-avatar svg {
  width: 18px;
  height: 18px;
  stroke: white;
}

.user-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.user-name {
  font-weight: 600;
  font-size: 13px;
  color: #1f2937;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.read-date {
  font-size: 11px;
  color: #6b7280;
}

.no-users {
  padding: 32px 20px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.no-users svg {
  width: 48px;
  height: 48px;
  stroke: #cbd5e1;
}

.no-users p {
  margin: 0;
  color: #9ca3af;
  font-size: 13px;
  font-weight: 500;
}

.no-users-success svg {
  stroke: #4CAF50;
}

.no-users-success p {
  color: #2E7D32;
}

/* Confirmación */
.confirm-text {
  font-size: 16px;
  color: #374151;
  margin-bottom: 8px;
}

.confirm-warning {
  color: #dc2626;
  font-size: 14px;
}

/* Responsive */
@media (max-width: 992px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
}

@media (min-width: 481px) and (max-width: 768px) {
  .main-content {
    margin-left: 250px;
    width: calc(100vw - 250px);
  }
}

@media (max-width: 768px) and (orientation: landscape) {
  .main-content {
    margin-left: 160px;
    width: calc(100vw - 160px);
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 240px;
    width: calc(100vw - 240px);
  }
  
  .page-content {
    padding: 12px;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .stats-lists {
    grid-template-columns: 1fr;
  }
  
  .stats-summary {
    grid-template-columns: 1fr;
  }
  
  .stat-card {
    padding: 14px;
  }
  
  .stat-value {
    font-size: 24px;
  }
  
  .meta-grid {
    grid-template-columns: 1fr;
  }
  
  .meta-item {
    padding: 12px;
  }
  
  .meta-icon {
    width: 36px;
    height: 36px;
  }
  
  .meta-icon svg {
    width: 18px;
    height: 18px;
  }
  
  .page-header {
    padding: 12px 16px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .header-main {
    flex-direction: row;
    gap: 12px;
    align-items: center;
    width: 100%;
  }
  
  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .manuales-table {
    font-size: 11px;
  }
  
  .manuales-table th,
  .manuales-table td {
    padding: 6px;
  }
  
  .modal-content {
    width: 95%;
    margin: 16px;
  }
  
  .modal-large,
  .modal-editar {
    max-width: 95%;
  }
  
  .modal-editar .modal-body {
    padding: 16px;
  }
  
  .modal-editar .form-row {
    grid-template-columns: 1fr;
  }
  
  .modal-editar .media-type-selector {
    flex-wrap: wrap;
  }
  
  .modal-editar .file-current span,
  .modal-editar .file-selected span {
    max-width: 160px;
  }
  
  .detalle-title {
    font-size: 20px;
  }
}

@media (max-width: 480px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
  
  .page-header {
    padding: 10px 12px;
  }
  
  .header-icon {
    width: 28px;
    height: 28px;
  }
  
  .header-icon svg {
    width: 14px;
    height: 14px;
  }
  
  .header-title {
    font-size: 14px;
  }
  
  .header-subtitle {
    font-size: 10px;
  }
  
  .btn-primary {
    padding: 8px 12px;
    font-size: 11px;
  }
  
  .table-container {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  .manuales-table {
    min-width: 650px;
    font-size: 10px;
  }
  
  .stat-card {
    flex-direction: column;
    text-align: center;
  }
  
  .stat-icon {
    width: 40px;
    height: 40px;
  }
  
  .stat-value {
    font-size: 22px;
  }
  
  .stat-label {
    font-size: 11px;
  }
  
  .stats-title {
    font-size: 18px;
  }
  
  .user-item {
    padding: 10px 12px;
  }
  
  .user-avatar {
    width: 32px;
    height: 32px;
  }
  
  .user-avatar svg {
    width: 16px;
    height: 16px;
  }
  
  .user-name {
    font-size: 12px;
  }
  
  .detalle-title {
    font-size: 18px;
  }
  
  .detalle-subtitulo {
    font-size: 13px;
  }
  
  .meta-label {
    font-size: 11px;
  }
  
  .meta-value {
    font-size: 13px;
  }
  
  .modal-editar {
    max-width: 98%;
    margin: 8px;
    max-height: 95vh;
  }
  
  .modal-editar .modal-header {
    padding: 12px 16px;
  }
  
  .modal-editar .modal-body {
    padding: 12px;
  }
  
  .modal-editar .form-input,
  .modal-editar .form-textarea {
    font-size: 14px;
    padding: 10px 12px;
  }
  
  .modal-editar .form-actions {
    flex-direction: column;
    gap: 8px;
  }
  
  .modal-editar .form-actions button {
    width: 100%;
    justify-content: center;
  }
  
  .modal-editar .media-type-selector {
    flex-direction: column;
    align-items: stretch;
  }
  
  .modal-editar .media-option {
    justify-content: center;
  }
  
  .modal-editar .file-current span,
  .modal-editar .file-selected span {
    max-width: 120px;
  }
  
  .modal-loading {
    padding: 40px 16px;
  }
  
  .loading-spinner-modal {
    width: 36px;
    height: 36px;
  }
}

@media (max-width: 375px) {
  .main-content {
    margin-left: 180px;
    width: calc(100vw - 180px);
  }
}

/* ===== MODAL DE CONFIRMACIÓN ===== */
.mini-modal {
  z-index: 10100;
}

.modal-confirm {
  max-width: 420px;
  animation: slideDown 0.25s ease-out;
}

@keyframes slideDown {
  0% {
    opacity: 0;
    transform: translateY(-20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-confirm-header {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 12px;
  padding: 20px 24px 16px;
  border-bottom: none;
}

.modal-icon-confirm {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-icon-confirm svg {
  width: 24px;
  height: 24px;
  stroke: white;
}

.modal-confirm-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  text-align: center;
}

.modal-body-confirm {
  padding: 0 24px 20px;
  text-align: center;
}

.modal-body-confirm p {
  margin: 0 0 8px;
  color: #4b5563;
  font-size: 14px;
  line-height: 1.5;
}

.confirm-detail {
  font-size: 13px;
  color: #6b7280;
}

.modal-actions-confirm {
  display: flex;
  gap: 10px;
  padding: 0 24px 20px;
}

.btn-cancel {
  flex: 1;
  padding: 10px 18px;
  background: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover:not(:disabled) {
  background: #e5e7eb;
}

.btn-cancel:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-confirm-primary {
  flex: 1;
  padding: 10px 18px;
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-confirm-primary:hover:not(:disabled) {
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
  transform: translateY(-1px);
}

.btn-confirm-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* ===== ARCHIVOS EXISTENTES EN EDICIÓN ===== */
.file-current {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  background: #f0fdf4;
  border: 1.5px solid #86efac;
  border-radius: 10px;
  margin-top: 8px;
}

.file-current svg {
  flex-shrink: 0;
}

.file-current span {
  flex: 1;
  color: #166534;
  font-size: 13px;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-current .btn-remove-file {
  background: #dcfce7;
  color: #166534;
}

.file-current .btn-remove-file:hover {
  background: #bbf7d0;
}

.image-preview-small {
  width: 48px;
  height: 48px;
  object-fit: cover;
  border-radius: 6px;
  flex-shrink: 0;
}

/* ===== MODAL DE FEEDBACK ===== */
.feedback-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 16px;
  backdrop-filter: blur(4px);
}

.feedback-modal {
  background: white;
  border-radius: 20px;
  padding: 32px 24px;
  max-width: 340px;
  width: 100%;
  text-align: center;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: feedbackPop 0.3s ease-out;
}

@keyframes feedbackPop {
  0% {
    transform: scale(0.8);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.feedback-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.feedback-modal.success .feedback-icon {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.feedback-modal.error .feedback-icon {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.feedback-icon svg {
  width: 32px;
  height: 32px;
  color: white;
}

.feedback-title {
  font-size: 20px;
  font-weight: 700;
  margin: 0 0 8px;
  color: #1f2937;
}

.feedback-message {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 24px;
  line-height: 1.5;
}

.feedback-btn {
  width: 100%;
  padding: 12px 24px;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.feedback-btn.success {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.feedback-btn.success:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.feedback-btn.error {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.feedback-btn.error:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

/* Transiciones */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive feedback */
@media (max-width: 480px) {
  .feedback-modal {
    padding: 24px 20px;
    max-width: 300px;
  }
  
  .feedback-icon {
    width: 56px;
    height: 56px;
  }
  
  .feedback-icon svg {
    width: 28px;
    height: 28px;
  }
  
  .feedback-title {
    font-size: 18px;
  }
  
  .feedback-message {
    font-size: 13px;
  }
}
</style>
