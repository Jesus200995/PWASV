<template>
  <div class="notificaciones-container">
    <!-- Apple Dynamic Background -->
    <div class="apple-dynamic-bg">
      <div class="apple-orb apple-orb-1"></div>
      <div class="apple-orb apple-orb-2"></div>
      <div class="apple-orb apple-orb-3"></div>
    </div>
    
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <!-- ================== STICKY WRAPPER FOR HEADER + STATS + FILTERS ================== -->
      <div class="apple-sticky-wrapper">
        <!-- ================== HEADER APPLE STYLE ================== -->
        <header class="apple-page-header">
          <div class="apple-header-wrapper">
            <div class="apple-header-center">
              <div class="apple-title-group">
                <div class="apple-icon-mini">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M13.73 21a2 2 0 0 1-3.46 0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <span class="apple-title-divider">|</span>
                <h1 class="apple-page-title">NOTIFICACIONES</h1>
              </div>
              <p class="apple-page-subtitle">{{ tabActual === 'grupales' ? 'Notificaciones masivas a todos los usuarios' : 'Notificaciones personalizadas' }}</p>
            </div>
            
            <button @click="cargarNotificaciones" class="apple-refresh-button" :disabled="cargando">
              <svg :class="{ 'apple-spin': cargando }" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </header>

        <!-- ================== STATS CARDS APPLE STYLE ================== -->
        <div class="apple-stats-section">
          <div class="apple-stats-grid">
            <div class="apple-stat-card">
              <div class="apple-stat-icon blue">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                  <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                </svg>
              </div>
              <div class="apple-stat-content">
                <div class="apple-stat-value">{{ notificaciones.length }}</div>
                <div class="apple-stat-label">Total</div>
              </div>
            </div>

            <div class="apple-stat-card">
              <div class="apple-stat-icon green">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke-width="2"/>
                  <circle cx="9" cy="7" r="4" stroke-width="2"/>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87" stroke-width="2"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75" stroke-width="2"/>
                </svg>
              </div>
              <div class="apple-stat-content">
                <div class="apple-stat-value">{{ tabActual === 'grupales' ? 'Grupales' : 'Individuales' }}</div>
                <div class="apple-stat-label">Tipo Activo</div>
              </div>
            </div>

            <div class="apple-stat-card">
              <div class="apple-stat-icon purple">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <polyline points="20 6 9 17 4 12" stroke-width="2"/>
                </svg>
              </div>
              <div class="apple-stat-content">
                <div class="apple-stat-value">Enviadas</div>
                <div class="apple-stat-label">Estado</div>
              </div>
            </div>
          </div>

          <!-- ================== TABS + ACTIONS INSIDE STATS ================== -->
          <div class="apple-search-section">
            <div class="apple-tabs-row">
              <div class="apple-tabs-container">
                <button 
                  :class="['apple-tab-button', { 'active': tabActual === 'grupales' }]"
                  @click="cambiarTab('grupales')"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke-width="2"/>
                    <circle cx="9" cy="7" r="4" stroke-width="2"/>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87" stroke-width="2"/>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75" stroke-width="2"/>
                  </svg>
                  <span>Grupales</span>
                  <span class="apple-tab-badge">{{ tabActual === 'grupales' ? notificaciones.length : '' }}</span>
                </button>
                <button 
                  :class="['apple-tab-button', { 'active': tabActual === 'individuales' }]"
                  @click="cambiarTab('individuales')"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="8" r="4" stroke-width="2"/>
                    <path d="M12 14c-4.42 0-8 1.79-8 4v2h16v-2c0-2.21-3.58-4-8-4z" stroke-width="2"/>
                  </svg>
                  <span>Individuales</span>
                  <span class="apple-tab-badge">{{ tabActual === 'individuales' ? notificaciones.length : '' }}</span>
                </button>
              </div>

              <div class="apple-filter-controls" v-if="puedeCrearNotificaciones">
                <button 
                  @click="abrirModalCrear" 
                  class="apple-filter-btn create"
                  title="Nueva Notificación"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M12 5v14M5 12h14" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span>Nueva</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="apple-page-content">
        <!-- Mensaje de carga -->
        <div v-if="cargando" class="apple-loading-state">
          <div class="apple-loading-spinner"></div>
          <p>Cargando notificaciones...</p>
        </div>

        <!-- Mensaje de error -->
        <div v-if="error && !cargando" class="apple-error-state">
          <div class="apple-error-icon">⚠️</div>
          <h3>Error al cargar notificaciones</h3>
          <p>{{ error }}</p>
          <button class="apple-btn-secondary" @click="cargarNotificaciones">Reintentar</button>
        </div>

        <!-- Lista de notificaciones -->
        <div v-if="!cargando && !error" class="apple-notificaciones-list">
          <div class="apple-list-header">
            <h2>{{ tabActual === 'grupales' ? 'Notificaciones Grupales' : 'Notificaciones Individuales' }}</h2>
            <span class="apple-count-badge">{{ notificaciones.length }}</span>
          </div>

          <!-- Tabla de notificaciones estilo Apple -->
          <div class="apple-table-container">
            <table class="apple-table">
              <thead>
                <tr>
                  <th>Título</th>
                  <th>Subtítulo</th>
                  <th>Destinatarios</th>
                  <th>Fecha de Envío</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="notificacion in notificaciones" :key="notificacion.id" class="apple-table-row">
                  <td class="apple-title-cell">
                    <div class="apple-title-content">
                      <span class="apple-notification-title">{{ notificacion.titulo }}</span>
                      <span v-if="notificacion.archivo_nombre" class="apple-attachment-badge">
                        📎 {{ notificacion.archivo_nombre }}
                      </span>
                    </div>
                  </td>
                  <td class="apple-subtitle-cell">
                    <span v-if="notificacion.subtitulo" class="apple-notification-subtitle">
                      {{ notificacion.subtitulo }}
                    </span>
                    <span v-else class="apple-no-subtitle">Sin subtítulo</span>
                  </td>
                  <td>
                    <span :class="['apple-recipients-badge', { 'all-users': notificacion.enviada_a_todos }]">
                      {{ notificacion.destinatarios_texto }}
                    </span>
                  </td>
                  <td>
                    <span class="apple-date-badge">{{ formatearFecha(notificacion.fecha_envio) }}</span>
                  </td>
                  <td>
                    <span class="apple-status-badge enviada">Enviada</span>
                  </td>
                  <td>
                    <div class="apple-actions">
                      <button 
                        class="apple-action-btn view" 
                        @click="verDetalle(notificacion)"
                        title="Ver detalle"
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                          <circle cx="12" cy="12" r="3"/>
                        </svg>
                      </button>
                      <button 
                        v-if="puedeVerAcciones"
                        class="apple-action-btn edit" 
                        @click="editarNotificacion(notificacion)"
                        title="Editar notificación"
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                        </svg>
                      </button>
                      <button 
                        class="apple-action-btn stats" 
                        @click="verEstadisticas(notificacion)"
                        title="Ver estadísticas de lectura"
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M3 3v18h18"/>
                          <path d="M18 17V9"/>
                          <path d="M13 17V5"/>
                          <path d="M8 17v-3"/>
                        </svg>
                      </button>
                      <button 
                        v-if="puedeVerAcciones"
                        class="apple-action-btn delete" 
                        @click="confirmarEliminar(notificacion)"
                        title="Eliminar notificación"
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
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
            <div v-if="notificaciones.length === 0" class="apple-empty-state">
              <div class="apple-empty-icon">📢</div>
              <h3>No hay notificaciones grupales</h3>
              <p>Crea tu primera notificación grupal para comunicarte con todos los usuarios del sistema.</p>
              <button class="apple-btn-primary" @click="mostrarModalCrear = true">
                Crear Primera Notificación Grupal
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal Crear Notificación -->
    <div v-if="mostrarModalCrear" class="modal-overlay" @click="cerrarModalCrear">
      <div 
        class="modal-content" 
        :class="{ 'modal-compact': formNotificacion.enviada_a_todos, 'modal-expanded': !formNotificacion.enviada_a_todos }"
        @click.stop
      >
        <div class="modal-header">
          <h3>Nueva Notificación</h3>
          <button class="btn-close" @click="cerrarModalCrear">×</button>
        </div>
        
        <div class="modal-body" :class="{ 'modal-body-two-columns': !formNotificacion.enviada_a_todos }">
          <!-- Columna principal del formulario -->
          <div class="form-column">
            <form @submit.prevent="crearNotificacion">
              <!-- Título -->
              <div class="form-group-compact">
                <label for="titulo">Título *</label>
                <input
                  id="titulo"
                  v-model="formNotificacion.titulo"
                  type="text"
                  class="form-input-compact"
                  placeholder="Título de la notificación"
                  maxlength="150"
                  required
                />
                <small class="char-count">{{ formNotificacion.titulo.length }}/150</small>
              </div>

              <!-- Subtítulo -->
              <div class="form-group-compact">
                <label for="subtitulo">Subtítulo</label>
                <input
                  id="subtitulo"
                  v-model="formNotificacion.subtitulo"
                  type="text"
                  class="form-input-compact"
                  placeholder="Subtítulo opcional"
                  maxlength="200"
                />
                <small class="char-count">{{ formNotificacion.subtitulo.length }}/200</small>
              </div>

              <!-- Descripción -->
              <div class="form-group-compact">
                <label for="descripcion">Descripción</label>
                <textarea
                  id="descripcion"
                  v-model="formNotificacion.descripcion"
                  class="form-textarea-compact"
                  placeholder="Descripción detallada"
                  rows="3"
                ></textarea>
              </div>

              <!-- Enlace URL -->
              <div class="form-group-compact">
                <label for="enlace_url">Enlace URL (opcional)</label>
                <input
                  id="enlace_url"
                  v-model="formNotificacion.enlace_url"
                  type="url"
                  class="form-input-compact"
                  placeholder="https://ejemplo.com"
                />
              </div>

              <!-- Destinatarios -->
              <div class="form-group-compact">
                <label>Destinatarios</label>
                <div class="radio-group-compact">
                  <label class="radio-option-compact">
                    <input
                      v-model="formNotificacion.enviada_a_todos"
                      type="radio"
                      :value="true"
                      @change="limpiarUsuariosSeleccionados"
                    />
                    <span class="radio-text">Todos</span>
                  </label>
                  <label class="radio-option-compact">
                    <input
                      v-model="formNotificacion.enviada_a_todos"
                      type="radio"
                      :value="false"
                      @change="cargarUsuarios"
                    />
                    <span class="radio-text">Específicos</span>
                  </label>
                </div>
              </div>

              <!-- Archivo adjunto -->
              <div class="form-group-compact">
                <label for="archivo">Archivo adjunto</label>
                <div class="file-input-container-compact">
                  <input
                    id="archivo"
                    ref="archivoInput"
                    type="file"
                    class="file-input"
                    accept=".jpg,.jpeg,.png,.gif,.pdf,.mp4,.avi,.mov,.wmv"
                    @change="manejarArchivoSeleccionado"
                  />
                  <label for="archivo" class="file-input-label-compact">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14,2 14,8 20,8"/>
                    </svg>
                    <span class="file-text">{{ archivoSeleccionado ? archivoSeleccionado.name : 'Seleccionar archivo' }}</span>
                  </label>
                </div>
                <small class="file-help-compact">JPG, PNG, PDF, MP4 (máx. 50MB)</small>
              </div>

              <!-- Botones -->
              <div class="modal-actions-compact">
                <button type="button" class="btn-secondary-compact" @click="cerrarModalCrear">
                  Cancelar
                </button>
                <button type="submit" class="btn-primary-compact" :disabled="enviandoNotificacion">
                  <span v-if="enviandoNotificacion" class="loading-spinner-small"></span>
                  {{ enviandoNotificacion ? 'Enviando...' : 'Enviar' }}
                </button>
              </div>
            </form>
          </div>

          <!-- Columna del selector de usuarios (solo visible cuando "Específicos" está seleccionado) -->
          <div v-if="!formNotificacion.enviada_a_todos" class="users-column">
            <div class="users-column-header">
              <h4>Seleccionar Usuarios</h4>
              <div class="selected-count-badge">
                {{ formNotificacion.usuario_ids.length }} seleccionados
              </div>
            </div>
            
            <div v-if="cargandoUsuarios" class="loading-users-compact">
              <div class="loading-spinner-small"></div>
              <span>Cargando usuarios...</span>
            </div>
            
            <div v-else class="users-selector-column">
              <div class="search-input-wrapper">
                <input
                  v-model="busquedaUsuarios"
                  type="text"
                  class="form-input-compact search-users-column"
                  placeholder="🔍 Buscar por nombre, correo o CURP..."
                  autocomplete="off"
                />
              </div>
              
              <div class="users-list-column" v-show="usuariosFiltrados.length > 0">
                <div class="users-list-header" v-if="busquedaUsuarios">
                  {{ usuariosFiltrados.length }} resultado(s) encontrado(s)
                </div>
                <label
                  v-for="usuario in usuariosFiltrados"
                  :key="usuario.id"
                  class="user-option-column"
                  :class="{ 'selected': formNotificacion.usuario_ids.includes(usuario.id) }"
                >
                  <input
                    v-model="formNotificacion.usuario_ids"
                    :value="usuario.id"
                    type="checkbox"
                  />
                  <div class="user-info-column">
                    <span class="user-name-column">{{ usuario.nombre_completo || usuario.nombre || 'Sin nombre' }}</span>
                    <span class="user-email-column">{{ usuario.correo || usuario.email || 'Sin email' }}</span>
                    <span v-if="usuario.curp" class="user-curp-column">CURP: {{ usuario.curp }}</span>
                  </div>
                </label>
              </div>
              
              <div v-show="busquedaUsuarios && usuariosFiltrados.length === 0" class="no-users-found-column">
                ❌ No se encontraron usuarios que coincidan con "{{ busquedaUsuarios }}"
              </div>
              
              <div v-show="!busquedaUsuarios && usuarios.length === 0" class="no-users-loaded-column">
                📝 No hay usuarios disponibles
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Editar Notificación -->
    <div v-if="mostrarModalEditar" class="modal-overlay" @click="cerrarModalEditar">
      <div 
        class="modal-content" 
        :class="{ 'modal-compact': formEdicion.enviada_a_todos, 'modal-expanded': !formEdicion.enviada_a_todos }"
        @click.stop
      >
        <div class="modal-header">
          <h3>Editar Notificación</h3>
          <button class="btn-close" @click="cerrarModalEditar">×</button>
        </div>
        
        <div class="modal-body" :class="{ 'modal-body-two-columns': !formEdicion.enviada_a_todos }">
          <!-- Columna principal del formulario -->
          <div class="form-column">
            <form @submit.prevent="guardarEdicion">
              <!-- Título -->
              <div class="form-group-compact">
                <label for="titulo-edit">Título *</label>
                <input
                  id="titulo-edit"
                  v-model="formEdicion.titulo"
                  type="text"
                  class="form-input-compact"
                  placeholder="Título de la notificación"
                  maxlength="150"
                  required
                />
                <small class="char-count">{{ formEdicion.titulo.length }}/150</small>
              </div>

              <!-- Subtítulo -->
              <div class="form-group-compact">
                <label for="subtitulo-edit">Subtítulo</label>
                <input
                  id="subtitulo-edit"
                  v-model="formEdicion.subtitulo"
                  type="text"
                  class="form-input-compact"
                  placeholder="Subtítulo opcional"
                  maxlength="200"
                />
                <small class="char-count">{{ formEdicion.subtitulo.length }}/200</small>
              </div>

              <!-- Descripción -->
              <div class="form-group-compact">
                <label for="descripcion-edit">Descripción</label>
                <textarea
                  id="descripcion-edit"
                  v-model="formEdicion.descripcion"
                  class="form-textarea-compact"
                  placeholder="Descripción detallada"
                  rows="3"
                ></textarea>
              </div>

              <!-- Enlace URL -->
              <div class="form-group-compact">
                <label for="enlace_url-edit">Enlace URL (opcional)</label>
                <input
                  id="enlace_url-edit"
                  v-model="formEdicion.enlace_url"
                  type="url"
                  class="form-input-compact"
                  placeholder="https://ejemplo.com"
                />
              </div>

              <!-- Destinatarios -->
              <div class="form-group-compact">
                <label>Destinatarios</label>
                <div class="radio-group-compact">
                  <label class="radio-option-compact">
                    <input
                      v-model="formEdicion.enviada_a_todos"
                      type="radio"
                      :value="true"
                      @change="limpiarUsuariosSeleccionadosEdicion"
                    />
                    <span class="radio-text">Todos</span>
                  </label>
                  <label class="radio-option-compact">
                    <input
                      v-model="formEdicion.enviada_a_todos"
                      type="radio"
                      :value="false"
                      @change="cargarUsuarios"
                    />
                    <span class="radio-text">Específicos</span>
                  </label>
                </div>
              </div>

              <!-- Archivo adjunto actual -->
              <div v-if="archivoActual" class="form-group-compact">
                <label>Archivo actual</label>
                <div class="current-file-display">
                  <span class="file-name">📎 {{ archivoActual }}</span>
                  <span class="file-note">(Se mantendrá si no seleccionas uno nuevo)</span>
                </div>
              </div>

              <!-- Archivo adjunto nuevo -->
              <div class="form-group-compact">
                <label for="archivo-edit">{{ archivoActual ? 'Reemplazar archivo' : 'Archivo adjunto' }}</label>
                <div class="file-input-container-compact">
                  <input
                    id="archivo-edit"
                    ref="archivoInputEdit"
                    type="file"
                    class="file-input"
                    accept=".jpg,.jpeg,.png,.gif,.pdf,.mp4,.avi,.mov,.wmv"
                    @change="manejarArchivoSeleccionadoEdicion"
                  />
                  <label for="archivo-edit" class="file-input-label-compact">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14,2 14,8 20,8"/>
                    </svg>
                    <span class="file-text">{{ archivoSeleccionadoEdicion ? archivoSeleccionadoEdicion.name : 'Seleccionar nuevo archivo' }}</span>
                  </label>
                </div>
                <small class="file-help-compact">JPG, PNG, PDF, MP4 (máx. 50MB)</small>
              </div>

              <!-- Botones -->
              <div class="modal-actions-compact">
                <button type="button" class="btn-secondary-compact" @click="cerrarModalEditar">
                  Cancelar
                </button>
                <button type="submit" class="btn-primary-compact" :disabled="guardandoEdicion">
                  <span v-if="guardandoEdicion" class="loading-spinner-small"></span>
                  {{ guardandoEdicion ? 'Guardando...' : 'Guardar Cambios' }}
                </button>
              </div>
            </form>
          </div>

          <!-- Columna del selector de usuarios (solo visible cuando "Específicos" está seleccionado) -->
          <div v-if="!formEdicion.enviada_a_todos" class="users-column">
            <div class="users-column-header">
              <h4>Seleccionar Usuarios</h4>
              <div class="selected-count-badge">
                {{ formEdicion.usuario_ids.length }} seleccionados
              </div>
            </div>
            
            <div v-if="cargandoUsuarios" class="loading-users-compact">
              <div class="loading-spinner-small"></div>
              <span>Cargando usuarios...</span>
            </div>
            
            <div v-else class="users-selector-column">
              <div class="search-input-wrapper">
                <input
                  v-model="busquedaUsuariosEdicion"
                  type="text"
                  class="form-input-compact search-users-column"
                  placeholder="🔍 Buscar por nombre, correo o CURP..."
                  autocomplete="off"
                />
              </div>
              
              <div class="users-list-column" v-show="usuariosFiltradosEdicion.length > 0">
                <div class="users-list-header" v-if="busquedaUsuariosEdicion">
                  {{ usuariosFiltradosEdicion.length }} resultado(s) encontrado(s)
                </div>
                <label
                  v-for="usuario in usuariosFiltradosEdicion"
                  :key="usuario.id"
                  class="user-option-column"
                  :class="{ 'selected': formEdicion.usuario_ids.includes(usuario.id) }"
                >
                  <input
                    v-model="formEdicion.usuario_ids"
                    :value="usuario.id"
                    type="checkbox"
                  />
                  <div class="user-info-column">
                    <span class="user-name-column">{{ usuario.nombre_completo || usuario.nombre || 'Sin nombre' }}</span>
                    <span class="user-email-column">{{ usuario.correo || usuario.email || 'Sin email' }}</span>
                    <span v-if="usuario.curp" class="user-curp-column">CURP: {{ usuario.curp }}</span>
                  </div>
                </label>
              </div>
              
              <div v-show="busquedaUsuariosEdicion && usuariosFiltradosEdicion.length === 0" class="no-users-found-column">
                ❌ No se encontraron usuarios que coincidan con "{{ busquedaUsuariosEdicion }}"
              </div>
              
              <div v-show="!busquedaUsuariosEdicion && usuarios.length === 0" class="no-users-loaded-column">
                📝 No hay usuarios disponibles
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Ver Detalle -->
    <div v-if="mostrarModalDetalle && notificacionDetalle" class="modal-overlay" @click="cerrarModalDetalle">
      <div class="modal-content modal-detail" @click.stop>
        <div class="modal-header">
          <h3>{{ notificacionDetalle.titulo }}</h3>
          <button class="btn-close" @click="cerrarModalDetalle">×</button>
        </div>
        
        <div class="modal-body">
          <div class="detail-section">
            <h4>Información General</h4>
            <div class="detail-info">
              <div class="info-item">
                <strong>Título:</strong>
                <span>{{ notificacionDetalle.titulo }}</span>
              </div>
              <div v-if="notificacionDetalle.subtitulo" class="info-item">
                <strong>Subtítulo:</strong>
                <span>{{ notificacionDetalle.subtitulo }}</span>
              </div>
              <div v-if="notificacionDetalle.descripcion" class="info-item">
                <strong>Descripción:</strong>
                <p class="description-text">{{ notificacionDetalle.descripcion }}</p>
              </div>
              <div v-if="notificacionDetalle.enlace_url" class="info-item">
                <strong>Enlace:</strong>
                <a :href="notificacionDetalle.enlace_url" target="_blank" class="link-external">
                  {{ notificacionDetalle.enlace_url }}
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                    <polyline points="15,3 21,3 21,9"/>
                    <line x1="10" y1="14" x2="21" y2="3"/>
                  </svg>
                </a>
              </div>
              <div class="info-item">
                <strong>Fecha de Envío:</strong>
                <span>{{ formatearFecha(notificacionDetalle.fecha_envio) }}</span>
              </div>
            </div>
          </div>

          <!-- Archivo adjunto -->
          <div v-if="notificacionDetalle.archivo_nombre" class="detail-section">
            <h4>Archivo Adjunto</h4>
            <div class="attachment-preview">
              <div class="attachment-info">
                <span class="attachment-name">{{ notificacionDetalle.archivo_nombre }}</span>
                <span class="attachment-type">{{ notificacionDetalle.archivo_tipo }}</span>
              </div>
              <div class="attachment-actions">
                <button class="btn-secondary" @click="descargarArchivo(notificacionDetalle.id)">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7,10 12,15 17,10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                  </svg>
                  Descargar
                </button>
                <button class="btn-primary" @click="verArchivo(notificacionDetalle.id)">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                  </svg>
                  Ver
                </button>
              </div>
            </div>
          </div>

          <!-- Destinatarios -->
          <div class="detail-section">
            <h4>Destinatarios</h4>
            <div v-if="notificacionDetalle.enviada_a_todos" class="recipients-info">
              <div class="recipients-badge all-users">
                👥 Todos los usuarios del sistema
              </div>
            </div>
            <div v-else class="recipients-list">
              <div class="recipients-header">
                <span>{{ notificacionDetalle.destinatarios?.length || 0 }} usuarios seleccionados:</span>
              </div>
              <div class="specific-recipients">
                <div
                  v-for="usuario in notificacionDetalle.destinatarios"
                  :key="usuario.id"
                  class="recipient-item"
                >
                  <span class="recipient-name">{{ usuario.nombre_completo }}</span>
                  <span class="recipient-email">{{ usuario.correo }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Confirmar Eliminación -->
    <div v-if="mostrarModalEliminar" class="modal-overlay" @click="cancelarEliminar">
      <div class="modal-content modal-confirm" @click.stop>
        <div class="modal-header">
          <h3>Confirmar Eliminación</h3>
          <button class="btn-close" @click="cancelarEliminar">×</button>
        </div>
        
        <div class="modal-body">
          <div class="confirm-content">
            <div class="confirm-icon">⚠️</div>
            <h4>¿Estás seguro de que deseas eliminar esta notificación?</h4>
            <p><strong>{{ notificacionAEliminar?.titulo }}</strong></p>
            <p>Esta acción no se puede deshacer.</p>
          </div>

          <div class="modal-actions">
            <button class="btn-secondary" @click="cancelarEliminar">
              Cancelar
            </button>
            <button class="btn-danger" @click="eliminarNotificacion" :disabled="eliminandoNotificacion">
              <span v-if="eliminandoNotificacion" class="loading-spinner-small"></span>
              {{ eliminandoNotificacion ? 'Eliminando...' : 'Eliminar' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Estadísticas -->
    <div v-if="mostrarModalEstadisticas && estadisticasNotificacion" class="modal-overlay" @click="cerrarModalEstadisticas">
      <div class="modal-content modal-stats" @click.stop>
        <div class="modal-header">
          <h3>Estadísticas de Lectura</h3>
          <div class="header-actions">
            <button class="btn-reload" @click="recargarEstadisticas" :disabled="cargandoEstadisticas" title="Recargar estadísticas">
              <i class="fas fa-sync-alt" :class="{ 'spinning': cargandoEstadisticas }"></i>
            </button>
            <button class="btn-close" @click="cerrarModalEstadisticas">×</button>
          </div>
        </div>
        
        <div class="modal-body" v-if="!cargandoEstadisticas">
          <!-- Título de la notificación -->
          <div class="stats-notification-info">
            <h4>{{ estadisticasNotificacion.titulo }}</h4>
            <p v-if="estadisticasNotificacion.subtitulo" class="stats-subtitle">
              {{ estadisticasNotificacion.subtitulo }}
            </p>
            <div class="stats-meta">
              <span class="stats-audience">
                <svg v-if="estadisticasNotificacion.enviada_a_todos" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: inline-block; vertical-align: middle; margin-right: 4px;">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                </svg>
                <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: inline-block; vertical-align: middle; margin-right: 4px;">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
                {{ estadisticasNotificacion.enviada_a_todos ? 'Enviada a todos los usuarios' : 'Enviada a usuarios específicos' }}
              </span>
              <span class="stats-date">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: inline-block; vertical-align: middle; margin-right: 4px;">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
                {{ formatearFecha(estadisticasNotificacion.fecha_envio) }}
              </span>
            </div>
          </div>

          <!-- Resumen de estadísticas -->
          <div class="stats-summary">
            <div class="stats-grid">
              <div class="stat-card stat-total">
                <div class="stat-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                    <circle cx="9" cy="7" r="4"/>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                  </svg>
                </div>
                <div class="stat-value">{{ estadisticasNotificacion.resumen.total_usuarios_objetivo }}</div>
                <div class="stat-label">Total Destinatarios</div>
              </div>
              
              <div class="stat-card stat-read">
                <div class="stat-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <polyline points="20 6 9 17 4 12"/>
                  </svg>
                </div>
                <div class="stat-value">{{ estadisticasNotificacion.resumen.usuarios_leido }}</div>
                <div class="stat-label">Han Leído</div>
                <div class="stat-percentage">{{ estadisticasNotificacion.resumen.porcentaje_leido }}%</div>
              </div>
              
              <div class="stat-card stat-unread">
                <div class="stat-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <polyline points="12 6 12 12 16 14"/>
                  </svg>
                </div>
                <div class="stat-value">{{ estadisticasNotificacion.resumen.usuarios_no_leido }}</div>
                <div class="stat-label">No Han Leído</div>
                <div class="stat-percentage">{{ estadisticasNotificacion.resumen.porcentaje_no_leido }}%</div>
              </div>
            </div>

            <!-- Barra de progreso visual -->
            <div class="progress-bar-container">
              <div class="progress-bar">
                <div 
                  class="progress-fill" 
                  :style="{ width: estadisticasNotificacion.resumen.porcentaje_leido + '%' }"
                ></div>
              </div>
              <div class="progress-labels">
                <span class="progress-read">{{ estadisticasNotificacion.resumen.porcentaje_leido }}% leído</span>
                <span class="progress-unread">{{ estadisticasNotificacion.resumen.porcentaje_no_leido }}% sin leer</span>
              </div>
            </div>
          </div>

          <!-- Pestañas para usuarios -->
          <div class="stats-tabs">
            <div class="tabs-header">
              <button 
                class="tab-button" 
                :class="{ 'active': tabActiva === 'leidos' }"
                @click="tabActiva = 'leidos'"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="display: inline-block; vertical-align: middle; margin-right: 4px;">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
                Han Leído ({{ estadisticasNotificacion.resumen.usuarios_leido }})
              </button>
              <button 
                class="tab-button" 
                :class="{ 'active': tabActiva === 'no_leidos' }"
                @click="tabActiva = 'no_leidos'"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: inline-block; vertical-align: middle; margin-right: 4px;">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12 6 12 12 16 14"/>
                </svg>
                No Han Leído ({{ estadisticasNotificacion.resumen.usuarios_no_leido }})
              </button>
            </div>

            <div class="tab-content">
              <!-- Tab Usuarios que han leído -->
              <div v-if="tabActiva === 'leidos'" class="users-list-stats">
                <div v-if="estadisticasNotificacion.usuarios_que_leyeron.length === 0" class="empty-users">
                  <div class="empty-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <path d="M22 17H2a3 3 0 0 0 3-3V8a3 3 0 0 0-3-3h20a3 3 0 0 0-3 3v6a3 3 0 0 0 3 3zm0 0v2a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-2"/>
                    </svg>
                  </div>
                  <p>Ningún usuario ha leído esta notificación aún</p>
                </div>
                <div v-else>
                  <div class="users-grid">
                    <div 
                      v-for="usuario in estadisticasNotificacion.usuarios_que_leyeron" 
                      :key="'read-' + usuario.id"
                      class="user-card user-read"
                    >
                      <div class="user-info">
                        <div class="user-name">{{ usuario.nombre_completo }}</div>
                        <div class="user-email">{{ usuario.correo }}</div>
                        <div v-if="usuario.curp" class="user-curp">{{ usuario.curp }}</div>
                      </div>
                      <div class="user-read-date">
                        <span class="read-icon">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                            <polyline points="20 6 9 17 4 12"/>
                          </svg>
                        </span>
                        <span class="read-time">{{ formatearFecha(usuario.leida_en) }}</span>
                      </div>
                    </div>
                  </div>
                  <div v-if="estadisticasNotificacion.usuarios_que_leyeron.length >= 20" class="more-users-note">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: inline-block; vertical-align: middle; margin-right: 4px;">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14 2 14 8 20 8"/>
                      <line x1="16" y1="13" x2="8" y2="13"/>
                      <line x1="16" y1="17" x2="8" y2="17"/>
                      <polyline points="10 9 9 9 8 9"/>
                    </svg>
                    Mostrando los primeros 20 usuarios
                  </div>
                </div>
              </div>

              <!-- Tab Usuarios que no han leído -->
              <div v-if="tabActiva === 'no_leidos'" class="users-list-stats">
                <div v-if="estadisticasNotificacion.usuarios_que_no_leyeron.length === 0" class="empty-users">
                  <div class="empty-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <circle cx="12" cy="12" r="10"/>
                      <polyline points="8 12 12 16 16 12"/>
                      <line x1="12" y1="8" x2="12" y2="16"/>
                    </svg>
                  </div>
                  <p>¡Todos los usuarios han leído esta notificación!</p>
                </div>
                <div v-else>
                  <div class="users-grid">
                    <div 
                      v-for="usuario in estadisticasNotificacion.usuarios_que_no_leyeron" 
                      :key="'unread-' + usuario.id"
                      class="user-card user-unread"
                    >
                      <div class="user-info">
                        <div class="user-name">{{ usuario.nombre_completo }}</div>
                        <div class="user-email">{{ usuario.correo }}</div>
                        <div v-if="usuario.curp" class="user-curp">{{ usuario.curp }}</div>
                      </div>
                      <div class="user-unread-status">
                        <span class="unread-icon">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/>
                            <polyline points="12 6 12 12 16 14"/>
                          </svg>
                        </span>
                        <span class="unread-text">Sin leer</span>
                      </div>
                    </div>
                  </div>
                  <div v-if="estadisticasNotificacion.usuarios_que_no_leyeron.length >= 20" class="more-users-note">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: inline-block; vertical-align: middle; margin-right: 4px;">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14 2 14 8 20 8"/>
                      <line x1="16" y1="13" x2="8" y2="13"/>
                      <line x1="16" y1="17" x2="8" y2="17"/>
                      <polyline points="10 9 9 9 8 9"/>
                    </svg>
                    Mostrando los primeros 20 usuarios
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Estado de carga -->
        <div v-if="cargandoEstadisticas" class="modal-body">
          <div class="loading-stats">
            <div class="loading-spinner"></div>
            <p>Cargando estadísticas...</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast de notificaciones -->
    <div v-if="toast.show" class="toast" :class="toast.type">
      <div class="toast-content">
        <div class="toast-icon">
          {{ toast.type === 'success' ? '✅' : '❌' }}
        </div>
        <div class="toast-message">{{ toast.message }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '../components/Sidebar.vue'
import notificacionesService from '../services/notificacionesService.js'
import usuariosService from '../services/usuariosService.js'
import authService from '../services/authService.js'

export default {
  name: 'NotificacionesView',
  components: {
    Sidebar
  },
  data() {
    return {
      isOnline: navigator.onLine,
      cargando: false,
      error: null,
      
      // Pestaña activa ('grupales' o 'individuales')
      tabActual: 'grupales',
      
      // Lista de notificaciones
      notificaciones: [],
      
      // Modal crear notificación
      mostrarModalCrear: false,
      enviandoNotificacion: false,
      archivoSeleccionado: null,
      formNotificacion: {
        titulo: '',
        subtitulo: '',
        descripcion: '',
        enlace_url: '',
        enviada_a_todos: true,
        usuario_ids: []
      },
      
      // Modal editar notificación
      mostrarModalEditar: false,
      guardandoEdicion: false,
      archivoSeleccionadoEdicion: null,
      archivoActual: null,
      notificacionEditandoId: null,
      formEdicion: {
        titulo: '',
        subtitulo: '',
        descripcion: '',
        enlace_url: '',
        enviada_a_todos: true,
        usuario_ids: []
      },
      busquedaUsuariosEdicion: '',
      
      // Usuarios para selector
      usuarios: [],
      cargandoUsuarios: false,
      busquedaUsuarios: '',
      
      // Modal detalle
      mostrarModalDetalle: false,
      notificacionDetalle: null,
      
      // Modal eliminar
      mostrarModalEliminar: false,
      notificacionAEliminar: null,
      eliminandoNotificacion: false,
      
      // Modal estadísticas
      mostrarModalEstadisticas: false,
      estadisticasNotificacion: null,
      notificacionActualId: null,
      cargandoEstadisticas: false,
      tabActiva: 'leidos',
      
      // Toast
      toast: {
        show: false,
        type: 'success',
        message: ''
      },
      
      // Permisos del usuario actual (reactivo)
      userPermisos: authService.getCurrentUser()?.permisos || {},
      userRol: authService.getCurrentUser()?.rol || ''
    }
  },
  
  computed: {
    // Permiso para crear notificaciones - REACTIVO
    puedeCrearNotificaciones() {
      // Admin siempre puede crear
      if (this.userRol === 'admin' || authService.isAdmin()) {
        console.log('✅ NotificacionesView: Usuario es admin - puede crear notificaciones')
        return true
      }
      // Verificar permiso específico
      const tienePermiso = this.userPermisos?.notificaciones_crear === true
      console.log('🔍 NotificacionesView: Verificando permiso notificaciones_crear:', tienePermiso, this.userPermisos)
      return tienePermiso
    },
    
    // Permiso para ver acciones (editar/eliminar) - REACTIVO
    puedeVerAcciones() {
      // Admin siempre puede ver acciones
      if (this.userRol === 'admin' || authService.isAdmin()) {
        return true
      }
      // Verificar permiso específico
      return this.userPermisos?.notificaciones_acciones === true
    },
    
    usuariosFiltrados() {
      if (!this.busquedaUsuarios.trim()) return this.usuarios
      
      const busqueda = this.busquedaUsuarios.toLowerCase().trim()
      return this.usuarios.filter(usuario => {
        // Buscar en nombre completo, nombre, correo, email, CURP y cargo
        const nombre = (usuario.nombre_completo || usuario.nombre || '').toLowerCase()
        const email = (usuario.correo || usuario.email || '').toLowerCase()
        const curp = (usuario.curp || '').toLowerCase()
        const cargo = (usuario.cargo || '').toLowerCase()
        
        return nombre.includes(busqueda) || 
               email.includes(busqueda) || 
               curp.includes(busqueda) ||
               cargo.includes(busqueda)
      })
    },
    
    usuariosFiltradosEdicion() {
      if (!this.busquedaUsuariosEdicion.trim()) return this.usuarios
      
      const busqueda = this.busquedaUsuariosEdicion.toLowerCase().trim()
      return this.usuarios.filter(usuario => {
        const nombre = (usuario.nombre_completo || usuario.nombre || '').toLowerCase()
        const email = (usuario.correo || usuario.email || '').toLowerCase()
        const curp = (usuario.curp || '').toLowerCase()
        const cargo = (usuario.cargo || '').toLowerCase()
        
        return nombre.includes(busqueda) || 
               email.includes(busqueda) || 
               curp.includes(busqueda) ||
               cargo.includes(busqueda)
      })
    }
  },
  
  mounted() {
    this.configurarEventosConexion()
    this.configurarEventosPermisos()
    this.cargarNotificaciones()
  },
  
  beforeUnmount() {
    // Remover listener de permisos
    window.removeEventListener('user-session-updated', this.actualizarPermisosUsuario)
  },
  
  methods: {
    configurarEventosConexion() {
      window.addEventListener('online', () => {
        this.isOnline = true
      })
      
      window.addEventListener('offline', () => {
        this.isOnline = false
      })
    },
    
    // Configurar eventos para actualización reactiva de permisos
    configurarEventosPermisos() {
      window.addEventListener('user-session-updated', this.actualizarPermisosUsuario)
    },
    
    // Función para actualizar permisos cuando el evento es disparado
    actualizarPermisosUsuario(event) {
      const userData = event.detail
      console.log('🔄 NotificacionesView: Permisos actualizados en tiempo real', userData)
      console.log('📋 NotificacionesView: Nuevos permisos recibidos:', userData.permisos)
      this.userPermisos = userData.permisos || {}
      this.userRol = userData.rol || ''
      console.log('✅ NotificacionesView: Variables reactivas actualizadas')
      console.log('🔔 NotificacionesView: notificaciones_crear =', this.userPermisos?.notificaciones_crear)
      console.log('🔔 NotificacionesView: notificaciones_acciones =', this.userPermisos?.notificaciones_acciones)
    },

    // ==================== GESTIÓN DE NOTIFICACIONES ====================
    
    cambiarTab(tab) {
      if (this.tabActual === tab) return
      
      console.log(`🔄 Cambiando de pestaña: ${this.tabActual} → ${tab}`)
      this.tabActual = tab
      
      // Actualizar formNotificacion.enviada_a_todos según la pestaña
      this.formNotificacion.enviada_a_todos = (tab === 'grupales')
      
      // Recargar notificaciones
      this.cargarNotificaciones()
    },
    
    async cargarNotificaciones() {
      this.cargando = true
      this.error = null
      
      try {
        const tipo = this.tabActual // 'grupales' o 'individuales'
        console.log(`🔄 CARGANDO notificaciones ${tipo}...`)
        console.log(`📤 Parámetros: limit=50, offset=0, tipo="${tipo}"`)
        
        const respuesta = await notificacionesService.listarNotificaciones(50, 0, tipo)
        
        this.notificaciones = respuesta.notificaciones || []
        
        console.log(`✅ Notificaciones ${tipo} cargadas: ${this.notificaciones.length}`)
        console.log('📋 Detalle de notificaciones:')
        this.notificaciones.forEach((notif, index) => {
          console.log(`   ${index + 1}. ${notif.titulo} - enviada_a_todos: ${notif.enviada_a_todos}`)
        })
        
      } catch (error) {
        console.error('❌ Error cargando notificaciones:', error)
        this.error = error.message
      } finally {
        this.cargando = false
      }
    },

    // ==================== CREAR NOTIFICACIÓN ====================
    
    async cargarUsuarios() {
      if (this.usuarios.length > 0) {
        console.log('✅ Usuarios ya cargados:', this.usuarios.length)
        return
      }
      
      this.cargandoUsuarios = true
      try {
        console.log('🔄 Iniciando carga de usuarios...')
        const respuesta = await usuariosService.obtenerUsuarios()
        
        if (Array.isArray(respuesta)) {
          this.usuarios = respuesta
        } else if (respuesta && Array.isArray(respuesta.usuarios)) {
          this.usuarios = respuesta.usuarios
        } else {
          console.warn('⚠️ Respuesta inesperada del servicio:', respuesta)
          this.usuarios = []
        }
        
        console.log('✅ Usuarios cargados exitosamente:', this.usuarios.length)
        
        // Debug: mostrar estructura del primer usuario
        if (this.usuarios.length > 0) {
          console.log('🔍 Estructura del primer usuario:', {
            id: this.usuarios[0].id,
            nombre_completo: this.usuarios[0].nombre_completo,
            correo: this.usuarios[0].correo,
            curp: this.usuarios[0].curp,
            cargo: this.usuarios[0].cargo,
            propiedades: Object.keys(this.usuarios[0])
          })
        } else {
          console.warn('⚠️ No se encontraron usuarios en la respuesta')
        }
        
      } catch (error) {
        console.error('❌ Error cargando usuarios:', error)
        this.mostrarToast('Error al cargar usuarios: ' + error.message, 'error')
        this.usuarios = []
      } finally {
        this.cargandoUsuarios = false
      }
    },

    limpiarUsuariosSeleccionados() {
      this.formNotificacion.usuario_ids = []
      this.busquedaUsuarios = ''
    },

    manejarArchivoSeleccionado(evento) {
      const archivo = evento.target.files[0]
      if (archivo) {
        // Validar tamaño (50MB)
        if (archivo.size > 50 * 1024 * 1024) {
          this.mostrarToast('El archivo no debe exceder 50MB', 'error')
          this.$refs.archivoInput.value = ''
          return
        }
        
        this.archivoSeleccionado = archivo
        console.log('📎 Archivo seleccionado:', archivo.name, archivo.size, 'bytes')
      } else {
        this.archivoSeleccionado = null
      }
    },

    abrirModalCrear() {
      // Establecer enviada_a_todos según la pestaña activa
      this.formNotificacion.enviada_a_todos = (this.tabActual === 'grupales')
      console.log(`📝 Abriendo modal de crear - enviada_a_todos: ${this.formNotificacion.enviada_a_todos}`)
      this.mostrarModalCrear = true
      
      // Si es notificación individual, cargar usuarios
      if (this.tabActual === 'individuales') {
        this.cargarUsuarios()
      }
    },

    async crearNotificacion() {
      // Validaciones
      if (!this.formNotificacion.titulo.trim()) {
        this.mostrarToast('El título es obligatorio', 'error')
        return
      }
      
      if (!this.formNotificacion.enviada_a_todos && this.formNotificacion.usuario_ids.length === 0) {
        this.mostrarToast('Debe seleccionar al menos un usuario', 'error')
        return
      }
      
      this.enviandoNotificacion = true
      
      try {
        const respuesta = await notificacionesService.crearNotificacion(
          this.formNotificacion,
          this.archivoSeleccionado
        )
        
        console.log('✅ Notificación creada:', respuesta)
        this.mostrarToast('Notificación enviada exitosamente', 'success')
        
        // Recargar lista y cerrar modal
        this.cargarNotificaciones()
        this.cerrarModalCrear()
        
      } catch (error) {
        console.error('❌ Error creando notificación:', error)
        this.mostrarToast(error.message, 'error')
      } finally {
        this.enviandoNotificacion = false
      }
    },

    cerrarModalCrear() {
      this.mostrarModalCrear = false
      this.limpiarFormulario()
    },

    limpiarFormulario() {
      this.formNotificacion = {
        titulo: '',
        subtitulo: '',
        descripcion: '',
        enlace_url: '',
        enviada_a_todos: (this.tabActual === 'grupales'), // Usar el valor de la pestaña activa
        usuario_ids: []
      }
      this.archivoSeleccionado = null
      if (this.$refs.archivoInput) {
        this.$refs.archivoInput.value = ''
      }
      this.busquedaUsuarios = ''
    },

    // ==================== VER DETALLE ====================
    
    async verDetalle(notificacion) {
      try {
        this.notificacionDetalle = await notificacionesService.obtenerNotificacion(notificacion.id)
        this.mostrarModalDetalle = true
        console.log('✅ Detalle de notificación cargado:', this.notificacionDetalle)
      } catch (error) {
        console.error('❌ Error cargando detalle:', error)
        this.mostrarToast(error.message, 'error')
      }
    },

    cerrarModalDetalle() {
      this.mostrarModalDetalle = false
      this.notificacionDetalle = null
    },

    // ==================== EDITAR NOTIFICACIÓN ====================
    
    async editarNotificacion(notificacion) {
      try {
        // Cargar datos completos de la notificación
        const notificacionCompleta = await notificacionesService.obtenerNotificacion(notificacion.id)
        
        // Cargar usuarios si es necesario
        if (!notificacionCompleta.enviada_a_todos) {
          await this.cargarUsuarios()
        }
        
        // Llenar formulario de edición
        this.notificacionEditandoId = notificacionCompleta.id
        this.formEdicion = {
          titulo: notificacionCompleta.titulo || '',
          subtitulo: notificacionCompleta.subtitulo || '',
          descripcion: notificacionCompleta.descripcion || '',
          enlace_url: notificacionCompleta.enlace_url || '',
          enviada_a_todos: notificacionCompleta.enviada_a_todos,
          usuario_ids: notificacionCompleta.enviada_a_todos ? [] : 
            (notificacionCompleta.destinatarios || []).map(u => u.id)
        }
        
        // Guardar nombre del archivo actual
        this.archivoActual = notificacionCompleta.archivo_nombre || null
        this.archivoSeleccionadoEdicion = null
        this.busquedaUsuariosEdicion = ''
        
        // Mostrar modal
        this.mostrarModalEditar = true
        
        console.log('✏️ Editando notificación:', notificacionCompleta)
        
      } catch (error) {
        console.error('❌ Error cargando notificación para editar:', error)
        this.mostrarToast(error.message, 'error')
      }
    },

    limpiarUsuariosSeleccionadosEdicion() {
      this.formEdicion.usuario_ids = []
      this.busquedaUsuariosEdicion = ''
    },

    manejarArchivoSeleccionadoEdicion(evento) {
      const archivo = evento.target.files[0]
      if (archivo) {
        // Validar tamaño (50MB)
        if (archivo.size > 50 * 1024 * 1024) {
          this.mostrarToast('El archivo no debe exceder 50MB', 'error')
          this.$refs.archivoInputEdit.value = ''
          return
        }
        
        this.archivoSeleccionadoEdicion = archivo
        console.log('📎 Nuevo archivo seleccionado:', archivo.name, archivo.size, 'bytes')
      } else {
        this.archivoSeleccionadoEdicion = null
      }
    },

    async guardarEdicion() {
      // Validaciones
      if (!this.formEdicion.titulo.trim()) {
        this.mostrarToast('El título es obligatorio', 'error')
        return
      }
      
      if (!this.formEdicion.enviada_a_todos && this.formEdicion.usuario_ids.length === 0) {
        this.mostrarToast('Debe seleccionar al menos un usuario', 'error')
        return
      }
      
      this.guardandoEdicion = true
      
      try {
        const respuesta = await notificacionesService.actualizarNotificacion(
          this.notificacionEditandoId,
          this.formEdicion,
          this.archivoSeleccionadoEdicion
        )
        
        console.log('✅ Notificación actualizada:', respuesta)
        this.mostrarToast('Notificación actualizada exitosamente', 'success')
        
        // Recargar lista y cerrar modal
        this.cargarNotificaciones()
        this.cerrarModalEditar()
        
      } catch (error) {
        console.error('❌ Error actualizando notificación:', error)
        this.mostrarToast(error.message, 'error')
      } finally {
        this.guardandoEdicion = false
      }
    },

    cerrarModalEditar() {
      this.mostrarModalEditar = false
      this.limpiarFormularioEdicion()
    },

    limpiarFormularioEdicion() {
      this.formEdicion = {
        titulo: '',
        subtitulo: '',
        descripcion: '',
        enlace_url: '',
        enviada_a_todos: true,
        usuario_ids: []
      }
      this.archivoSeleccionadoEdicion = null
      this.archivoActual = null
      this.notificacionEditandoId = null
      if (this.$refs.archivoInputEdit) {
        this.$refs.archivoInputEdit.value = ''
      }
      this.busquedaUsuariosEdicion = ''
    },

    // ==================== ARCHIVOS ====================
    
    async descargarArchivo(notificacionId) {
      try {
        const respuesta = await notificacionesService.descargarArchivo(notificacionId)
        
        // Crear URL para descarga
        const url = window.URL.createObjectURL(new Blob([respuesta.data]))
        const link = document.createElement('a')
        link.href = url
        
        // Obtener nombre del archivo del header o usar uno por defecto
        const contentDisposition = respuesta.headers['content-disposition']
        let filename = `archivo_${notificacionId}`
        
        if (contentDisposition) {
          const filenameMatch = contentDisposition.match(/filename="(.+)"/)
          if (filenameMatch) {
            filename = filenameMatch[1]
          }
        }
        
        link.setAttribute('download', filename)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
        this.mostrarToast('Archivo descargado exitosamente', 'success')
        
      } catch (error) {
        console.error('❌ Error descargando archivo:', error)
        this.mostrarToast('Error al descargar el archivo', 'error')
      }
    },

    verArchivo(notificacionId) {
      const url = notificacionesService.obtenerUrlArchivo(notificacionId)
      window.open(url, '_blank')
    },

    // ==================== ELIMINAR ====================
    
    confirmarEliminar(notificacion) {
      this.notificacionAEliminar = notificacion
      this.mostrarModalEliminar = true
    },

    cancelarEliminar() {
      this.mostrarModalEliminar = false
      this.notificacionAEliminar = null
    },

    async eliminarNotificacion() {
      if (!this.notificacionAEliminar) return
      
      this.eliminandoNotificacion = true
      
      try {
        await notificacionesService.eliminarNotificacion(this.notificacionAEliminar.id)
        
        this.mostrarToast('Notificación eliminada exitosamente', 'success')
        this.cargarNotificaciones()
        this.cancelarEliminar()
        
      } catch (error) {
        console.error('❌ Error eliminando notificación:', error)
        this.mostrarToast(error.message, 'error')
      } finally {
        this.eliminandoNotificacion = false
      }
    },

    // ==================== UTILIDADES ====================
    
    formatearFecha(fecha) {
      if (!fecha) return 'Sin fecha'
      
      try {
        const date = new Date(fecha)
        return date.toLocaleDateString('es-MX', {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        })
      } catch (error) {
        return 'Fecha inválida'
      }
    },

    mostrarToast(message, type = 'success') {
      this.toast = {
        show: true,
        type,
        message
      }

      setTimeout(() => {
        this.toast.show = false
      }, 4000)
    },

    // ==================== ESTADÍSTICAS ====================
    
    async verEstadisticas(notificacion) {
      try {
        this.cargandoEstadisticas = true
        this.mostrarModalEstadisticas = true
        this.tabActiva = 'leidos'
        this.notificacionActualId = notificacion.id
        
        console.log('📊 Cargando estadísticas para notificación:', notificacion.id)
        
        const estadisticas = await notificacionesService.obtenerEstadisticasNotificacion(notificacion.id)
        this.estadisticasNotificacion = estadisticas
        
        console.log('✅ Estadísticas cargadas:', estadisticas)
        
      } catch (error) {
        console.error('❌ Error cargando estadísticas:', error)
        this.mostrarToast(error.message, 'error')
        this.cerrarModalEstadisticas()
      } finally {
        this.cargandoEstadisticas = false
      }
    },

    cerrarModalEstadisticas() {
      this.mostrarModalEstadisticas = false
      this.estadisticasNotificacion = null
      this.notificacionActualId = null
      this.cargandoEstadisticas = false
      this.tabActiva = 'leidos'
    },

    async recargarEstadisticas() {
      if (!this.notificacionActualId) return
      
      try {
        this.cargandoEstadisticas = true
        
        console.log('🔄 Recargando estadísticas para notificación:', this.notificacionActualId)
        
        const estadisticas = await notificacionesService.obtenerEstadisticasNotificacion(this.notificacionActualId)
        this.estadisticasNotificacion = estadisticas
        
        console.log('✅ Estadísticas recargadas:', estadisticas)
        this.mostrarToast('Estadísticas actualizadas correctamente', 'success')
        
      } catch (error) {
        console.error('❌ Error recargando estadísticas:', error)
        this.mostrarToast('Error al recargar las estadísticas: ' + error.message, 'error')
      } finally {
        this.cargandoEstadisticas = false
      }
    },
    
    logout() {
      localStorage.removeItem('admin_token')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ====================== BASE LAYOUT ====================== */
.notificaciones-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
  position: relative;
  overflow: hidden;
}

/* ====================== APPLE DYNAMIC BACKGROUND ====================== */
.apple-dynamic-bg {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.apple-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.4;
  animation: apple-float 20s ease-in-out infinite;
}

.apple-orb-1 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.3) 0%, rgba(139, 195, 74, 0.2) 100%);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.apple-orb-2 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, rgba(0, 122, 255, 0.15) 0%, rgba(90, 200, 250, 0.1) 100%);
  bottom: -50px;
  left: 10%;
  animation-delay: -7s;
}

.apple-orb-3 {
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, rgba(175, 82, 222, 0.15) 0%, rgba(191, 90, 242, 0.1) 100%);
  top: 40%;
  right: 20%;
  animation-delay: -14s;
}

@keyframes apple-float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -30px) scale(1.05); }
  50% { transform: translate(-20px, 20px) scale(0.95); }
  75% { transform: translate(-30px, -20px) scale(1.02); }
}

/* ====================== MAIN CONTENT ====================== */
.main-content {
  flex: 1;
  margin-left: min(220px, 18vw);
  width: calc(100vw - min(220px, 18vw));
  min-height: 100vh;
  position: relative;
  box-sizing: border-box;
  overflow-x: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  padding: 8px 16px 0 16px;
  z-index: 1;
}

/* ====================== APPLE STICKY WRAPPER ====================== */
.apple-sticky-wrapper {
  position: sticky;
  top: 0;
  z-index: 100;
  background: transparent;
  margin-bottom: 20px;
}

/* ====================== APPLE PAGE HEADER ====================== */
.apple-page-header {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 50%, #2E7D32 100%);
  color: white;
  border-radius: 28px 28px 0 0;
  border: 2px solid #8BC34A;
  border-bottom: none;
  padding: 14px 20px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-header-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.apple-header-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.apple-title-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.apple-icon-mini {
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.apple-icon-mini svg {
  width: 18px;
  height: 18px;
  stroke: rgba(255, 255, 255, 0.9);
  stroke-width: 2;
}

.apple-title-divider {
  color: rgba(255, 255, 255, 0.4);
  font-size: 18px;
  font-weight: 300;
}

.apple-page-title {
  font-size: 18px;
  font-weight: 700;
  color: white;
  margin: 0;
  letter-spacing: 1.5px;
  text-transform: uppercase;
}

.apple-page-subtitle {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  font-weight: 500;
  letter-spacing: 0.3px;
}

.apple-refresh-button {
  position: absolute;
  right: 0;
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: white;
}

.apple-refresh-button svg {
  width: 14px;
  height: 14px;
  stroke-width: 2;
}

.apple-refresh-button:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.25);
  transform: scale(1.05);
}

.apple-refresh-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.apple-spin {
  animation: apple-spin-animation 1s linear infinite;
}

@keyframes apple-spin-animation {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ====================== APPLE STATS SECTION ====================== */
.apple-stats-section {
  background: white;
  border-radius: 0 0 28px 28px;
  border: 2px solid #8BC34A;
  border-top: none;
  padding: 18px 16px 16px 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  margin-top: -1px;
}

.apple-stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 12px;
}

.apple-stat-card {
  background: linear-gradient(135deg, #FAFBFC 0%, #F8F9FA 100%);
  border-radius: 14px;
  padding: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.apple-stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.apple-stat-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.apple-stat-icon.blue {
  background: linear-gradient(135deg, #007AFF 0%, #5AC8FA 100%);
}

.apple-stat-icon.green {
  background: linear-gradient(135deg, #34C759 0%, #30D158 100%);
}

.apple-stat-icon.purple {
  background: linear-gradient(135deg, #AF52DE 0%, #BF5AF2 100%);
}

.apple-stat-icon svg {
  width: 16px;
  height: 16px;
  color: white;
  stroke: white;
  stroke-width: 2.5;
  fill: none;
}

.apple-stat-content {
  flex: 1;
}

.apple-stat-value {
  font-size: 16px;
  font-weight: 700;
  color: #1d1d1f;
  line-height: 1;
  margin-bottom: 4px;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
  letter-spacing: -0.3px;
}

.apple-stat-label {
  font-size: 10px;
  color: #86868b;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ====================== APPLE SEARCH SECTION (TABS) ====================== */
.apple-search-section {
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  padding-top: 12px;
  margin-top: 4px;
}

.apple-tabs-row {
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}

.apple-tabs-container {
  display: flex;
  gap: 8px;
  flex: 1;
}

.apple-tab-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 12px;
  border: 1.5px solid transparent;
  background: #f5f5f7;
  color: #86868b;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-tab-button svg {
  width: 16px;
  height: 16px;
  stroke-width: 2;
}

.apple-tab-button:hover {
  background: rgba(0, 122, 255, 0.08);
  color: #007AFF;
}

.apple-tab-button.active {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  border-color: #2E7D32;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.apple-tab-button.active svg {
  stroke: white;
}

.apple-tab-badge {
  background: rgba(255, 255, 255, 0.25);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 700;
  min-width: 20px;
  text-align: center;
}

.apple-tab-button.active .apple-tab-badge {
  background: rgba(255, 255, 255, 0.3);
}

/* ====================== APPLE FILTER CONTROLS ====================== */
.apple-filter-controls {
  display: flex;
  gap: 8px;
}

.apple-filter-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 10px;
  border: none;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-filter-btn svg {
  width: 14px;
  height: 14px;
  stroke-width: 2;
}

.apple-filter-btn.create {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.apple-filter-btn.create:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(76, 175, 80, 0.4);
}

/* ====================== APPLE PAGE CONTENT ====================== */
.apple-page-content {
  padding: 0;
}

/* ====================== APPLE LOADING & ERROR STATES ====================== */
.apple-loading-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

.apple-loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e8f5e8;
  border-top: 3px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.apple-error-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

.apple-error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.apple-btn-secondary {
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  color: #333;
  border: none;
  padding: 10px 20px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.apple-btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* ====================== APPLE NOTIFICATIONS LIST ====================== */
.apple-notificaciones-list {
  background: white;
  border-radius: 20px;
  padding: 0;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(76, 175, 80, 0.1);
  overflow: hidden;
}

.apple-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
  border-bottom: 1px solid rgba(76, 175, 80, 0.1);
}

.apple-list-header h2 {
  font-size: 16px;
  font-weight: 700;
  color: #2E7D32;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-count-badge {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 700;
}

/* ====================== APPLE TABLE ====================== */
.apple-table-container {
  overflow-x: auto;
}

.apple-table-container::-webkit-scrollbar {
  height: 6px;
}

.apple-table-container::-webkit-scrollbar-track {
  background: #f5f5f7;
  border-radius: 3px;
}

.apple-table-container::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
  border-radius: 3px;
}

.apple-table {
  width: 100%;
  border-collapse: collapse;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-table thead tr {
  background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
}

.apple-table th {
  color: #2E7D32;
  font-weight: 700;
  font-size: 11px;
  padding: 14px 16px;
  text-align: left;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid rgba(76, 175, 80, 0.2);
  border-right: 1px solid rgba(76, 175, 80, 0.1);
  position: sticky;
  top: 0;
  z-index: 10;
}

.apple-table th:last-child {
  border-right: none;
}

.apple-table td {
  padding: 14px 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
  vertical-align: middle;
  font-size: 13px;
  color: #1d1d1f;
}

.apple-table-row {
  transition: all 0.2s ease;
}

.apple-table-row:hover {
  background: linear-gradient(135deg, #f8fffe 0%, #f0fff4 100%);
  border-left: 3px solid #4CAF50;
}

/* ====================== APPLE TABLE CELLS ====================== */
.apple-title-cell {
  min-width: 180px;
}

.apple-title-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.apple-notification-title {
  font-weight: 600;
  color: #1d1d1f;
  font-size: 13px;
}

.apple-attachment-badge {
  font-size: 11px;
  color: #4CAF50;
  background: rgba(76, 175, 80, 0.1);
  padding: 2px 8px;
  border-radius: 6px;
  width: fit-content;
}

.apple-subtitle-cell {
  max-width: 200px;
}

.apple-notification-subtitle {
  color: #666;
  font-size: 12px;
}

.apple-no-subtitle {
  color: #999;
  font-style: italic;
  font-size: 11px;
}

.apple-recipients-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
  background: rgba(175, 82, 222, 0.1);
  color: #AF52DE;
  border: 1px solid rgba(175, 82, 222, 0.2);
}

.apple-recipients-badge.all-users {
  background: rgba(0, 122, 255, 0.1);
  color: #007AFF;
  border: 1px solid rgba(0, 122, 255, 0.2);
}

.apple-date-badge {
  display: inline-block;
  padding: 4px 10px;
  background: rgba(0, 122, 255, 0.08);
  color: #007AFF;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
}

.apple-status-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 10px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.apple-status-badge.enviada {
  background: rgba(52, 199, 89, 0.15);
  color: #34C759;
}

/* ====================== APPLE ACTIONS ====================== */
.apple-actions {
  display: flex;
  gap: 6px;
}

.apple-action-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.apple-action-btn svg {
  width: 14px;
  height: 14px;
  stroke-width: 2;
}

.apple-action-btn.view {
  background: linear-gradient(135deg, #34C759 0%, #30D158 100%);
  color: white;
}

.apple-action-btn.view svg {
  stroke: white;
}

.apple-action-btn.view:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(52, 199, 89, 0.4);
}

.apple-action-btn.edit {
  background: linear-gradient(135deg, #FF9500 0%, #FFCC00 100%);
  color: white;
}

.apple-action-btn.edit svg {
  stroke: white;
}

.apple-action-btn.edit:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(255, 149, 0, 0.4);
}

.apple-action-btn.stats {
  background: linear-gradient(135deg, #007AFF 0%, #5AC8FA 100%);
  color: white;
}

.apple-action-btn.stats svg {
  stroke: white;
}

.apple-action-btn.stats:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.4);
}

.apple-action-btn.delete {
  background: linear-gradient(135deg, #FF3B30 0%, #FF6961 100%);
  color: white;
}

.apple-action-btn.delete svg {
  stroke: white;
}

.apple-action-btn.delete:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(255, 59, 48, 0.4);
}

/* ====================== APPLE EMPTY STATE ====================== */
.apple-empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.apple-empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.apple-empty-state h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1d1d1f;
  margin-bottom: 8px;
}

.apple-empty-state p {
  font-size: 14px;
  color: #86868b;
  margin-bottom: 20px;
}

.apple-btn-primary {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.apple-btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(76, 175, 80, 0.4);
}

/* ====================== OLD HEADER STYLES (KEEP FOR COMPATIBILITY) ====================== */
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

/* === TABS STYLES === */
.tabs-container {
  display: flex;
  gap: 0.5rem;
  padding: 1rem 0 0 0;
  position: sticky;
  top: 0;
  z-index: 99;
  background: #fafafa;
  border-radius: 0;
  margin: 0;
  margin-bottom: 0;
  border-bottom: 1px solid #e0e0e0;
}

.tab-button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: #d0d0d0 !important;
  border: none !important;
  border-radius: 10px 10px 0 0;
  color: #666666 !important;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  box-shadow: none !important;
}

.tab-button::before {
  display: none;
}

.tab-button:hover:not(.active) {
  background: #c5c5c5 !important;
  color: #555555 !important;
  border: none !important;
  transform: translateY(-1px);
  box-shadow: none !important;
}

.tab-button.active {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
  color: #ffffff !important;
  border: none !important;
  box-shadow: 0 3px 8px rgba(76, 175, 80, 0.3) !important;
  font-weight: 700;
  transform: translateY(-1px);
  margin-bottom: 0;
}

.tab-button svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  transition: transform 0.2s ease;
  opacity: 0.7 !important;
  color: #666666 !important;
}

.tab-button.active svg {
  transform: scale(1.1);
  opacity: 1 !important;
  color: #ffffff !important;
}

.tab-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 22px;
  height: 22px;
  padding: 0 0.45rem;
  background: rgba(102, 102, 102, 0.3) !important;
  color: #666666 !important;
  border-radius: 11px;
  font-size: 0.7rem;
  font-weight: 700;
  margin-left: 0.4rem;
  transition: all 0.2s ease;
  border: none !important;
}

.tab-button.active .tab-badge {
  background: rgba(255, 255, 255, 0.3) !important;
  color: #ffffff !important;
  border: none !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
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
  z-index: 1;
  position: relative;
  transition: all 0.3s ease;
}

.btn-primary:hover svg {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
  transform: scale(1.05);
}

.connection-status {
  display: flex;
  align-items: center;
  gap: clamp(4px, 1vw, 6px);
  padding: clamp(6px, 1.2vw, 8px) clamp(10px, 2vw, 14px);
  border-radius: clamp(14px, 2.5vw, 18px);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.08) 100%);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  transition: all 0.3s ease;
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.status-indicator {
  width: clamp(6px, 1.2vw, 8px);
  height: clamp(6px, 1.2vw, 8px);
  border-radius: 50%;
  transition: all 0.4s ease;
  position: relative;
}

.status-indicator::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border-radius: 50%;
  background: inherit;
  opacity: 0.3;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { 
    transform: scale(1); 
    opacity: 0.3; 
  }
  50% { 
    transform: scale(1.2); 
    opacity: 0.1; 
  }
}

.connection-status.online .status-indicator {
  background: #66BB6A;
  box-shadow: 
    0 0 12px rgba(102, 187, 106, 0.8),
    0 0 24px rgba(102, 187, 106, 0.4);
}

.connection-status.offline .status-indicator {
  background: #FF7043;
  box-shadow: 
    0 0 12px rgba(255, 112, 67, 0.8),
    0 0 24px rgba(255, 112, 67, 0.4);
}

.status-text {
  font-size: clamp(10px, 1.8vw, 12px);
  font-weight: 500;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
  white-space: nowrap;
  font-family: 'Inter', sans-serif;
}

/* === CONTENT STYLES === */
.page-content {
  flex: 1;
  padding: 0 24px 24px 24px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

/* === LOADING & ERROR STATES === */
.loading-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
  margin-top: 0;
  background: white;
  border-radius: 0 0 16px 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e8f5e8;
  border-top: 3px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
  margin-top: 0;
  background: white;
  border-radius: 0 0 16px 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

.error-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.btn-secondary {
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  color: #333;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}

.btn-secondary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* === NOTIFICATIONS LIST === */
.notificaciones-list {
  background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
  border-radius: 0 0 16px 16px;
  padding: 0;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.08),
    0 4px 16px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(76, 175, 80, 0.1);
  border-top: none;
  margin-top: 0;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(76, 175, 80, 0.1);
}

.list-header h2 {
  font-size: 18px;
  font-weight: 600;
  color: #2E7D32;
  margin: 0;
  font-family: 'Inter', sans-serif;
}

.btn-refresh {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}

.btn-refresh:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.btn-refresh:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* === NOTIFICATIONS TABLE === */
.notifications-table-container {
  overflow-x: auto;
}

.notifications-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Inter', sans-serif;
}

.notifications-table th {
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
  color: #2E7D32;
  font-weight: 600;
  font-size: 13px;
  padding: 14px 16px;
  text-align: left;
  border-bottom: 2px solid rgba(76, 175, 80, 0.2);
  white-space: nowrap;
}

.notifications-table td {
  padding: 16px;
  border-bottom: 1px solid rgba(76, 175, 80, 0.1);
  vertical-align: middle;
}

.notification-row:hover {
  background: linear-gradient(135deg, #f8fffe 0%, #f0fff4 100%);
}

.title-cell {
  min-width: 200px;
}

.title-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.notification-title {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.attachment-badge {
  font-size: 12px;
  color: #4CAF50;
  background: rgba(76, 175, 80, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  width: fit-content;
}

.subtitle-cell {
  max-width: 250px;
}

.notification-subtitle {
  color: #666;
  font-size: 13px;
}

.no-subtitle {
  color: #999;
  font-style: italic;
  font-size: 12px;
}

.recipients-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
}

.recipients-badge.all-users {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
}

.recipients-badge:not(.all-users) {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  color: #1976d2;
}

.notification-date {
  color: #666;
  font-size: 13px;
  white-space: nowrap;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-sent {
  background: linear-gradient(135deg, #c8e6c9 0%, #a5d6a7 100%);
  color: #2e7d32;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-action {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.btn-view {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  color: #1976d2;
}

.btn-view:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3);
}

.btn-edit {
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  color: #f57c00;
}

.btn-edit:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(245, 124, 0, 0.3);
}

.btn-delete {
  background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
  color: #d32f2f;
}

.btn-delete:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(211, 47, 47, 0.3);
}

.btn-stats {
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  color: #2e7d32;
}

.btn-stats:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
}

/* === ARCHIVO ACTUAL === */
.current-file-display {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px;
  background: rgba(76, 175, 80, 0.05);
  border: 1px solid rgba(76, 175, 80, 0.2);
  border-radius: 8px;
}

.current-file-display .file-name {
  font-size: 13px;
  font-weight: 500;
  color: #2E7D32;
}

.current-file-display .file-note {
  font-size: 11px;
  color: #666;
  font-style: italic;
}

/* === EMPTY STATE === */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-state h3 {
  color: #2E7D32;
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 8px 0;
  font-family: 'Inter', sans-serif;
}

.empty-state p {
  color: #666;
  margin: 0 0 24px 0;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
}

/* === MODALS === */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  backdrop-filter: blur(4px);
  padding: 16px;
  box-sizing: border-box;
  overflow-y: auto;
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 600px;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 
    0 24px 48px rgba(0, 0, 0, 0.3),
    0 12px 24px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  margin: auto;
  position: relative;
}

/* Modal expandido para dos columnas */
.modal-expanded {
  max-width: 1000px;
  width: 95%;
}

.modal-compact {
  max-width: 480px;
  width: 90%;
}

.modal-detail {
  max-width: 700px;
  width: 90%;
}

.modal-confirm {
  max-width: 400px;
  width: 90%;
}

/* Layout de dos columnas para el modal */
.modal-body-two-columns {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 24px;
  padding: 24px;
}

.form-column {
  min-width: 0;
}

.users-column {
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid rgba(76, 175, 80, 0.2);
  display: flex;
  flex-direction: column;
  height: fit-content;
  max-height: 60vh;
}

.users-column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(76, 175, 80, 0.2);
}

.users-column-header h4 {
  font-size: 16px;
  font-weight: 600;
  color: #2E7D32;
  margin: 0;
  font-family: 'Inter', sans-serif;
}

.selected-count-badge {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  min-width: fit-content;
  white-space: nowrap;
}

.users-selector-column {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}

.search-users-column {
  margin-bottom: 12px;
  padding: 10px 12px;
  font-size: 13px;
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-radius: 8px;
  background: white;
  transition: all 0.3s ease;
}

.search-users-column:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.users-list-column {
  flex: 1;
  overflow-y: auto;
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-radius: 8px;
  background: white;
  max-height: 400px;
}

.user-option-column {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  border-bottom: 1px solid rgba(76, 175, 80, 0.1);
  cursor: pointer;
  transition: all 0.2s ease;
}

.user-option-column:hover {
  background: rgba(76, 175, 80, 0.05);
}

.user-option-column.selected {
  background: rgba(76, 175, 80, 0.1);
  border-left: 3px solid #4CAF50;
}

.user-option-column:last-child {
  border-bottom: none;
}

.user-option-column input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: #4CAF50;
  margin: 0;
  flex-shrink: 0;
}

.user-info-column {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
  min-width: 0;
}

.user-name-column {
  font-weight: 600;
  color: #333;
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email-column {
  font-size: 11px;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-curp-column {
  font-size: 10px;
  color: #4CAF50;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.no-users-found-column,
.no-users-loaded-column {
  padding: 20px;
  text-align: center;
  color: #666;
  font-size: 12px;
  font-style: italic;
}

.no-users-found-column {
  color: #d32f2f;
}

.no-users-loaded-column {
  color: #ff9800;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(76, 175, 80, 0.1);
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
  border-radius: 16px 16px 0 0;
}

.modal-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #2E7D32;
  margin: 0;
  font-family: 'Inter', sans-serif;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-reload {
  background: none;
  border: none;
  font-size: 16px;
  color: #4CAF50;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.2s ease;
  padding: 0;
}

.btn-reload:hover {
  background-color: rgba(76, 175, 80, 0.1);
  color: #2E7D32;
}

.btn-reload:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-reload .spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  color: #666;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-close:hover {
  background: rgba(211, 47, 47, 0.1);
  color: #d32f2f;
}

.modal-body {
  padding: 24px;
}

/* === FORM STYLES === */
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
}

.form-input, .form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid rgba(76, 175, 80, 0.2);
  border-radius: 10px;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-input:focus, .form-textarea:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.char-count {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
  display: block;
}

.radio-group {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #333;
}

.radio-option input[type="radio"] {
  width: 16px;
  height: 16px;
  accent-color: #4CAF50;
}

.radio-text {
  font-weight: 500;
}

/* === COMPACT FORM STYLES === */
.form-group-compact {
  margin-bottom: 14px;
}

.form-group-compact label {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
  font-size: 13px;
  font-family: 'Inter', sans-serif;
}

.form-input-compact, .form-textarea-compact {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-radius: 8px;
  font-size: 13px;
  font-family: 'Inter', sans-serif;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-input-compact:focus, .form-textarea-compact:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
}

.form-textarea-compact {
  resize: vertical;
  min-height: 70px;
}

.radio-group-compact {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.radio-option-compact {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 13px;
  color: #333;
}

.radio-option-compact input[type="radio"] {
  width: 14px;
  height: 14px;
  accent-color: #4CAF50;
}

.radio-option-compact .radio-text {
  font-weight: 500;
}

.loading-users-compact {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #666;
  font-size: 12px;
  padding: 8px;
}

.selector-label {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
  font-size: 13px;
  font-family: 'Inter', sans-serif;
}

.users-selector-compact {
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-radius: 8px;
  padding: 10px;
  background: #f9f9f9;
}

.search-input-wrapper {
  position: relative;
  margin-bottom: 8px;
}

.search-users {
  width: 100%;
  padding: 6px 10px;
  font-size: 12px;
  border: 1px solid rgba(76, 175, 80, 0.4);
  border-radius: 6px;
  background: white;
  transition: all 0.3s ease;
}

.search-users:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.users-list-compact {
  max-height: 140px;
  overflow-y: auto;
  border: 1px solid rgba(76, 175, 80, 0.2);
  border-radius: 6px;
  background: white;
  margin-bottom: 8px;
}

.users-list-header {
  padding: 6px 8px;
  background: rgba(76, 175, 80, 0.1);
  color: #2E7D32;
  font-size: 11px;
  font-weight: 500;
  border-bottom: 1px solid rgba(76, 175, 80, 0.2);
}

.user-option-compact {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  border-bottom: 1px solid rgba(76, 175, 80, 0.1);
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.user-option-compact:hover {
  background: rgba(76, 175, 80, 0.05);
}

.user-option-compact.selected {
  background: rgba(76, 175, 80, 0.1);
  border-left: 3px solid #4CAF50;
}

.user-option-compact:last-child {
  border-bottom: none;
}

.user-option-compact input[type="checkbox"] {
  width: 14px;
  height: 14px;
  accent-color: #4CAF50;
  margin: 0;
  flex-shrink: 0;
}

.user-info-compact {
  display: flex;
  flex-direction: column;
  gap: 1px;
  flex: 1;
  min-width: 0;
}

.user-name-compact {
  font-weight: 500;
  color: #333;
  font-size: 11px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email-compact {
  font-size: 10px;
  color: #666;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-curp-compact {
  font-size: 9px;
  color: #4CAF50;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.no-users-found, .no-users-loaded {
  padding: 12px 8px;
  text-align: center;
  color: #666;
  font-size: 11px;
  font-style: italic;
}

.no-users-found {
  color: #d32f2f;
}

.no-users-loaded {
  color: #ff9800;
}

.selected-count-wrapper {
  padding-top: 4px;
  border-top: 1px solid rgba(76, 175, 80, 0.2);
}

.selected-count {
  font-size: 11px;
  color: #4CAF50;
  font-weight: 500;
  display: block;
}

.file-input-container-compact {
  position: relative;
}

.file-input-label-compact {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border: 1px dashed rgba(76, 175, 80, 0.4);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #666;
  font-weight: 500;
  background: rgba(76, 175, 80, 0.05);
  font-size: 12px;
}

.file-input-label-compact:hover {
  border-color: #4CAF50;
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.file-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
}

.file-help-compact {
  font-size: 11px;
  color: #666;
  margin-top: 2px;
  display: block;
}

.modal-actions-compact {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid rgba(76, 175, 80, 0.1);
}

.btn-secondary-compact {
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  color: #333;
  border: none;
  padding: 8px 14px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}

.btn-secondary-compact:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
}

.btn-primary-compact {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-primary-compact:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.btn-primary-compact:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* === USER SELECTOR === */
.loading-users {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  font-size: 14px;
  padding: 12px;
}

.loading-spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid #e8f5e8;
  border-top: 2px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.users-selector {
  border: 2px solid rgba(76, 175, 80, 0.2);
  border-radius: 10px;
  padding: 16px;
  background: #f9f9f9;
}

.users-search {
  margin-bottom: 12px;
}

.users-list {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid rgba(76, 175, 80, 0.1);
  border-radius: 8px;
  background: white;
}

.user-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-bottom: 1px solid rgba(76, 175, 80, 0.1);
  cursor: pointer;
  transition: background 0.2s ease;
}

.user-option:hover {
  background: rgba(76, 175, 80, 0.05);
}

.user-option:last-child {
  border-bottom: none;
}

.user-option input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: #4CAF50;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.user-email {
  font-size: 12px;
  color: #666;
}

.selected-count {
  margin-top: 8px;
  font-size: 12px;
  color: #4CAF50;
  font-weight: 500;
}

/* === FILE INPUT === */
.file-input-container {
  position: relative;
}

.file-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.file-input-label {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border: 2px dashed rgba(76, 175, 80, 0.3);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #666;
  font-weight: 500;
  background: rgba(76, 175, 80, 0.05);
}

.file-input-label:hover {
  border-color: #4CAF50;
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.file-help {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
  display: block;
}

/* === MODAL ACTIONS === */
.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid rgba(76, 175, 80, 0.1);
}

.btn-danger {
  background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-danger:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.3);
}

.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* === DETAIL MODAL === */
.detail-section {
  margin-bottom: 24px;
}

.detail-section:last-child {
  margin-bottom: 0;
}

.detail-section h4 {
  font-size: 16px;
  font-weight: 600;
  color: #2E7D32;
  margin: 0 0 12px 0;
  font-family: 'Inter', sans-serif;
}

.detail-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item strong {
  font-weight: 600;
  color: #333;
  font-size: 13px;
}

.info-item span {
  color: #666;
  font-size: 14px;
}

.description-text {
  color: #666;
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
  white-space: pre-wrap;
}

.link-external {
  color: #4CAF50;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 4px;
  font-weight: 500;
  transition: color 0.3s ease;
}

.link-external:hover {
  color: #2E7D32;
}

/* === ATTACHMENT PREVIEW === */
.attachment-preview {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: rgba(76, 175, 80, 0.05);
  border: 1px solid rgba(76, 175, 80, 0.2);
  border-radius: 10px;
}

.attachment-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.attachment-name {
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.attachment-type {
  font-size: 12px;
  color: #4CAF50;
  text-transform: capitalize;
}

.attachment-actions {
  display: flex;
  gap: 8px;
}

/* === RECIPIENTS === */
.recipients-info {
  padding: 16px;
  background: rgba(76, 175, 80, 0.05);
  border-radius: 10px;
}

.recipients-list {
  background: rgba(76, 175, 80, 0.05);
  border-radius: 10px;
  padding: 16px;
}

.recipients-header {
  font-weight: 500;
  color: #2E7D32;
  margin-bottom: 12px;
  font-size: 14px;
}

.specific-recipients {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 200px;
  overflow-y: auto;
}

.recipient-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: white;
  border-radius: 8px;
  border: 1px solid rgba(76, 175, 80, 0.1);
}

.recipient-name {
  font-weight: 500;
  color: #333;
  font-size: 13px;
}

.recipient-email {
  font-size: 12px;
  color: #666;
}

/* === CONFIRM MODAL === */
.confirm-content {
  text-align: center;
  padding: 20px 0;
}

.confirm-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.confirm-content h4 {
  color: #d32f2f;
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 12px 0;
  font-family: 'Inter', sans-serif;
}

.confirm-content p {
  color: #666;
  margin: 8px 0;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
}

/* === TOAST === */
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 16px 20px;
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  z-index: 20000;
  min-width: 300px;
  max-width: 500px;
}

.toast.success {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
}

.toast.error {
  background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
  color: white;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.toast-icon {
  font-size: 20px;
}

.toast-message {
  font-weight: 500;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
}

/* === RESPONSIVE DESIGN === */

/* Desktop grande */
@media (min-width: 1200px) {
  .modal-content {
    max-height: 80vh;
  }
  
  .modal-expanded {
    max-width: 1100px;
  }
}

/* Tablets y Laptops pequeñas */
@media (max-width: 992px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
  
  .modal-overlay {
    padding: 12px;
  }
  
  .modal-expanded {
    max-width: 900px;
  }
  
  .modal-body-two-columns {
    gap: 20px;
  }
}

/* Tablet portrait - 481px a 768px */
@media (min-width: 481px) and (max-width: 768px) {
  .main-content {
    margin-left: 0;
    width: 100vw;
  }
  
  .modal-overlay {
    padding: 16px;
    align-items: flex-start;
    padding-top: 40px;
  }
  
  .modal-content {
    width: 100%;
    max-width: 680px;
    max-height: calc(100vh - 80px);
  }
  
  .modal-expanded {
    width: 100%;
    max-width: none;
  }
  
  .modal-compact {
    width: 100%;
    max-width: 500px;
  }
  
  /* Cambiar a layout vertical */
  .modal-body-two-columns {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto;
    gap: 16px;
    padding: 16px;
  }
  
  .users-column {
    order: 2;
    max-height: 350px;
  }
  
  .form-column {
    order: 1;
  }
}

/* Móviles y tablets pequeñas */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    width: 100vw;
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
  
  .page-content {
    padding: 12px 16px;
  }
  
  /* Modales en móviles */
  .modal-overlay {
    padding: 0;
    align-items: stretch;
  }
  
  .modal-content {
    width: 100%;
    max-width: 100%;
    max-height: 100vh;
    border-radius: 0;
    margin: 0;
  }
  
  .modal-compact {
    width: 100%;
    max-width: 100%;
    border-radius: 0;
  }
  
  .modal-expanded {
    width: 100%;
    max-width: 100%;
    border-radius: 0;
  }
  
  .modal-detail {
    width: 100%;
    max-width: 100%;
    border-radius: 0;
  }
  
  .modal-confirm {
    width: 100%;
    max-width: 100%;
    max-height: 100vh;
    border-radius: 0;
    display: flex;
    flex-direction: column;
  }
  
  /* Cambiar a layout vertical en móviles */
  .modal-body-two-columns {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr;
    gap: 16px;
    padding: 16px;
    height: 100%;
  }
  
  .users-column {
    order: 2;
    max-height: 50vh;
    padding: 16px;
  }
  
  .form-column {
    order: 1;
  }
  
  .modal-body {
    padding: 16px;
    flex: 1;
  }
  
  .modal-compact .modal-body {
    padding: 16px;
  }
  
  .modal-header {
    position: sticky;
    top: 0;
    background: white;
    z-index: 10;
    padding: 16px;
    border-bottom: 1px solid #e0e0e0;
  }
  
  .notifications-table {
    font-size: 11px;
  }
  
  .notifications-table th,
  .notifications-table td {
    padding: 6px;
  }
  
  .title-cell {
    min-width: 120px;
  }
  
  .action-buttons {
    flex-wrap: wrap;
    gap: 6px;
  }
  
  .btn-action {
    width: 32px;
    height: 32px;
  }
  
  .toast {
    bottom: 16px;
    right: 16px;
    left: 16px;
    min-width: auto;
    max-width: calc(100vw - 32px);
  }
}

/* Móviles pequeños - Menos de 480px */
@media (max-width: 480px) {
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
  
  .notifications-table-container {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  .notifications-table {
    min-width: 650px;
    font-size: 10px;
  }
  
  /* Modales pantalla completa en móviles pequeños */
  .modal-overlay {
    padding: 0;
  }
  
  .modal-content,
  .modal-compact,
  .modal-expanded,
  .modal-detail,
  .modal-confirm {
    width: 100%;
    max-width: 100%;
    height: 100vh;
    max-height: 100vh;
    border-radius: 0;
    margin: 0;
  }
  
  .modal-header {
    padding: 14px 16px;
    border-bottom: 2px solid #e0e0e0;
  }
  
  .modal-header h3 {
    font-size: 16px;
  }
  
  .btn-close {
    width: 32px;
    height: 32px;
    font-size: 24px;
  }
  
  .modal-body {
    padding: 16px 12px;
  }
  
  .modal-body-two-columns {
    padding: 12px;
    gap: 12px;
    min-height: calc(100vh - 100px);
  }
  
  .users-column {
    padding: 12px;
    max-height: 40vh;
  }
  
  .users-column-header h4 {
    font-size: 13px;
  }
  
  .selected-count-badge {
    font-size: 10px;
    padding: 3px 8px;
  }
  
  .user-option-column {
    padding: 10px;
  }
  
  .user-name-column {
    font-size: 11px;
  }
  
  .user-email-column {
    font-size: 9px;
  }
  
  .user-curp-column {
    font-size: 8px;
  }
  
  .form-group-compact {
    margin-bottom: 14px;
  }
  
  .form-group-compact label {
    font-size: 12px;
  }
  
  .form-input-compact,
  .form-textarea-compact {
    font-size: 13px;
    padding: 10px;
  }
  
  .radio-group-compact {
    flex-direction: column;
    gap: 10px;
  }
  
  .file-input-label-compact {
    padding: 10px 12px;
  }
  
  .file-text {
    font-size: 11px;
    max-width: 180px;
  }
  
  .modal-actions-compact {
    flex-direction: column-reverse;
    gap: 10px;
  }
  
  .btn-secondary-compact,
  .btn-primary-compact {
    width: 100%;
    padding: 12px;
    font-size: 13px;
  }
  
  .attachment-preview {
    flex-direction: column;
    gap: 12px;
  }
  
  .attachment-actions {
    width: 100%;
    flex-direction: column;
  }
  
  .attachment-actions button {
    width: 100%;
  }
  
  .confirm-content {
    padding: 16px;
  }
  
  .confirm-icon {
    font-size: 40px;
  }
  
  .confirm-content h4 {
    font-size: 16px;
  }
  
  .confirm-content p {
    font-size: 13px;
  }
  
  .modal-actions {
    flex-direction: column-reverse;
    gap: 10px;
    padding: 16px;
  }
  
  .modal-actions button {
    width: 100%;
    padding: 12px;
  }
}

/* Orientación horizontal en móviles */
@media (max-width: 768px) and (orientation: landscape) {
  .modal-overlay {
    align-items: flex-start;
    overflow-y: auto;
  }
  
  .modal-content {
    max-height: 95vh;
    margin: 2.5vh auto;
  }
  
  .modal-body-two-columns {
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto;
    gap: 16px;
    max-height: calc(95vh - 80px);
  }
  
  .users-column {
    order: 2;
    max-height: calc(95vh - 120px);
  }
  
  .form-column {
    order: 1;
    max-height: calc(95vh - 120px);
    overflow-y: auto;
  }
}

/* iPhone SE y dispositivos muy pequeños */
@media (max-width: 375px) {
  .header-title {
    font-size: 13px;
  }
  
  .header-subtitle {
    font-size: 9px;
  }
  
  .btn-primary {
    padding: 6px 10px;
    font-size: 10px;
  }
  
  .btn-primary svg {
    width: 12px;
    height: 12px;
  }
  
  .modal-header h3 {
    font-size: 15px;
  }
  
  .form-input-compact,
  .form-textarea-compact {
    font-size: 12px;
  }
  
  .user-name-column {
    font-size: 10px;
  }
  
  .user-email-column {
    font-size: 8px;
  }
}

/* Estadísticas modal responsivo */
@media (max-width: 768px) {
  .modal-stats {
    width: 100%;
    max-width: 100%;
    height: 100vh;
    max-height: 100vh;
    border-radius: 0;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .stat-card {
    max-width: 100%;
  }
  
  .stats-meta {
    flex-direction: column;
    gap: 8px;
  }
  
  .tabs-header {
    flex-direction: row;
  }
  
  .tab-button {
    padding: 12px 16px;
    font-size: 12px;
  }
  
  .user-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .user-read-date,
  .user-unread-status {
    align-self: flex-end;
  }
}

/* Prevenir zoom en inputs en iOS */
@media (max-width: 768px) {
  input[type="text"],
  input[type="url"],
  input[type="email"],
  textarea,
  select {
    font-size: 16px !important;
  }
}

/* === MODAL ESTADÍSTICAS === */
.modal-stats {
  max-width: 750px;
  width: 90%;
}

.stats-notification-info {
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
  border: 1px solid rgba(76, 175, 80, 0.2);
}

.stats-notification-info h4 {
  font-size: 18px;
  font-weight: 600;
  color: #2E7D32;
  margin: 0 0 8px 0;
  font-family: 'Inter', sans-serif;
}

.stats-subtitle {
  font-size: 14px;
  color: #666;
  margin: 0 0 12px 0;
  font-style: italic;
}

.stats-meta {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.stats-audience,
.stats-date {
  font-size: 13px;
  color: #4CAF50;
  font-weight: 500;
}

.stats-summary {
  margin-bottom: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
  margin-bottom: 20px;
  justify-items: center;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 2px solid transparent;
  transition: all 0.3s ease;
  width: 100%;
  max-width: 140px;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.stat-total {
  border-color: rgba(33, 150, 243, 0.3);
}

.stat-read {
  border-color: rgba(76, 175, 80, 0.3);
}

.stat-unread {
  border-color: rgba(255, 152, 0, 0.3);
}

.stat-icon {
  font-size: 20px;
  margin-bottom: 6px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #2E7D32;
  margin-bottom: 3px;
  font-family: 'Inter', sans-serif;
}

.stat-label {
  font-size: 11px;
  color: #666;
  font-weight: 500;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  line-height: 1.2;
}

.stat-percentage {
  font-size: 12px;
  font-weight: 600;
  color: #4CAF50;
  background: rgba(76, 175, 80, 0.1);
  padding: 3px 8px;
  border-radius: 12px;
  display: inline-block;
}

.progress-bar-container {
  margin-top: 20px;
}

.progress-bar {
  width: 100%;
  height: 12px;
  background: #f0f0f0;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  border-radius: 6px;
  transition: width 0.8s ease;
}

.progress-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
}

.progress-read {
  color: #4CAF50;
  font-size: 12px;
  font-weight: 600;
}

.progress-unread {
  color: #ff9800;
  font-size: 12px;
  font-weight: 600;
}

.stats-tabs {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.tabs-header {
  display: flex;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

/* Estilos de tab-button movidos arriba - no duplicar aquí */

.tab-content {
  padding: 20px;
}

.users-list-stats {
  min-height: 200px;
}

.empty-users {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.users-grid {
  display: grid;
  gap: 12px;
}

.user-card {
  background: #f8f9fa;
  border-radius: 6px;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
}

.user-card:hover {
  background: #e9ecef;
  transform: translateX(4px);
}

.user-read {
  border-left-color: #4CAF50;
}

.user-unread {
  border-left-color: #ff9800;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 12px;
  font-weight: 600;
  color: #333;
  margin-bottom: 1px;
}

.user-email {
  font-size: 10px;
  color: #666;
  margin-bottom: 1px;
}

.user-curp {
  font-size: 9px;
  color: #4CAF50;
  font-weight: 500;
}

.user-read-date {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  text-align: center;
}

.read-icon {
  font-size: 14px;
}

.read-time {
  font-size: 10px;
  color: #4CAF50;
  font-weight: 500;
}

.user-unread-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.unread-icon {
  font-size: 16px;
}

.unread-text {
  font-size: 11px;
  color: #ff9800;
  font-weight: 500;
}

.more-users-note {
  margin-top: 16px;
  padding: 12px;
  background: rgba(76, 175, 80, 0.1);
  border-radius: 8px;
  text-align: center;
  font-size: 13px;
  color: #4CAF50;
  font-weight: 500;
}

.loading-stats {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.loading-stats .loading-spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 16px;
}

/* ====================== APPLE RESPONSIVE STYLES ====================== */
@media (max-width: 1200px) {
  .apple-stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1024px) {
  .main-content {
    margin-left: 0;
    width: 100%;
    padding: 8px 12px 0 12px;
  }
  
  .apple-sticky-wrapper {
    margin-bottom: 16px;
  }

  .apple-page-header {
    border-radius: 20px 20px 0 0;
    padding: 12px 16px;
  }

  .apple-stats-section {
    border-radius: 0 0 20px 20px;
    padding: 14px 12px 12px 12px;
  }
  
  .apple-stats-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
  }
  
  .apple-stat-card {
    padding: 10px;
    border-radius: 12px;
  }

  .apple-stat-icon {
    width: 32px;
    height: 32px;
  }

  .apple-stat-value {
    font-size: 14px;
  }

  .apple-tabs-row {
    flex-direction: column;
    gap: 10px;
  }

  .apple-tabs-container {
    width: 100%;
    justify-content: center;
  }

  .apple-filter-controls {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 6px 10px 0 10px;
  }
  
  .apple-page-header {
    border-radius: 16px 16px 0 0;
    padding: 10px 14px;
  }

  .apple-page-title {
    font-size: 14px;
    letter-spacing: 1px;
  }

  .apple-page-subtitle {
    font-size: 10px;
  }

  .apple-stats-section {
    border-radius: 0 0 16px 16px;
    padding: 12px 10px 10px 10px;
  }
  
  .apple-stats-grid {
    grid-template-columns: 1fr 1fr 1fr;
    gap: 6px;
  }
  
  .apple-stat-card {
    flex-direction: column;
    text-align: center;
    padding: 10px 6px;
    gap: 6px;
  }

  .apple-stat-icon {
    width: 28px;
    height: 28px;
  }

  .apple-stat-icon svg {
    width: 14px;
    height: 14px;
  }

  .apple-stat-value {
    font-size: 13px;
  }

  .apple-stat-label {
    font-size: 9px;
  }

  .apple-tabs-container {
    flex-direction: column;
    gap: 6px;
  }

  .apple-tab-button {
    width: 100%;
    justify-content: center;
    padding: 10px 12px;
  }

  .apple-notificaciones-list {
    border-radius: 16px;
  }

  .apple-list-header {
    padding: 12px 14px;
  }

  .apple-list-header h2 {
    font-size: 14px;
  }

  .apple-table th,
  .apple-table td {
    padding: 10px 12px;
    font-size: 11px;
  }

  .apple-action-btn {
    width: 28px;
    height: 28px;
  }

  .apple-action-btn svg {
    width: 12px;
    height: 12px;
  }
}

@media (max-width: 480px) {
  .main-content {
    padding: 4px 6px 0 6px;
  }

  .apple-page-header {
    border-radius: 12px 12px 0 0;
    padding: 8px 10px;
  }

  .apple-title-group {
    gap: 6px;
  }

  .apple-icon-mini {
    width: 18px;
    height: 18px;
  }

  .apple-icon-mini svg {
    width: 14px;
    height: 14px;
  }

  .apple-page-title {
    font-size: 12px;
  }

  .apple-stats-section {
    border-radius: 0 0 12px 12px;
    padding: 10px 8px 8px 8px;
  }

  .apple-stats-grid {
    gap: 4px;
  }

  .apple-stat-card {
    padding: 8px 4px;
    border-radius: 10px;
  }

  .apple-stat-icon {
    width: 24px;
    height: 24px;
  }

  .apple-stat-icon svg {
    width: 12px;
    height: 12px;
  }

  .apple-stat-value {
    font-size: 12px;
  }

  .apple-stat-label {
    font-size: 8px;
  }

  .apple-refresh-button {
    width: 28px;
    height: 28px;
  }

  .apple-refresh-button svg {
    width: 12px;
    height: 12px;
  }

  .apple-notificaciones-list {
    border-radius: 12px;
  }

  .apple-list-header {
    padding: 10px 12px;
  }

  .apple-list-header h2 {
    font-size: 12px;
  }

  .apple-table th,
  .apple-table td {
    padding: 8px 10px;
    font-size: 10px;
  }

  .apple-actions {
    gap: 4px;
  }

  .apple-action-btn {
    width: 24px;
    height: 24px;
  }

  .apple-action-btn svg {
    width: 10px;
    height: 10px;
  }
}
</style>
