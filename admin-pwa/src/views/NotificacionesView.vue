<template>
  <div class="notificaciones-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                <circle cx="18" cy="6" r="3" fill="#ff4757" opacity="0.9"/>
                <circle cx="18" cy="6" r="1.5" fill="#ffffff" opacity="0.8"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Centro de Notificaciones</h1>
              <p class="header-subtitle">Gestiona todas las notificaciones y alertas del sistema</p>
            </div>
          </div>
          <div class="header-actions">
            <button class="btn-primary" @click="mostrarModalCrear = true">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 5v14"/>
                <path d="M5 12h14"/>
              </svg>
              Nueva Notificación
            </button>
            <div class="connection-status" :class="{ 'online': isOnline, 'offline': !isOnline }">
              <div class="status-indicator"></div>
              <span class="status-text">{{ isOnline ? 'En línea' : 'Sin conexión' }}</span>
            </div>
          </div>
        </div>
      </header>

      <div class="page-content">
        <!-- Mensaje de carga -->
        <div v-if="cargando" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Cargando notificaciones...</p>
        </div>

        <!-- Mensaje de error -->
        <div v-if="error && !cargando" class="error-state">
          <div class="error-icon">⚠️</div>
          <h3>Error al cargar notificaciones</h3>
          <p>{{ error }}</p>
          <button class="btn-secondary" @click="cargarNotificaciones">Reintentar</button>
        </div>

        <!-- Lista de notificaciones -->
        <div v-if="!cargando && !error" class="notificaciones-list">
          <div class="list-header">
            <h2>Notificaciones Enviadas ({{ notificaciones.length }})</h2>
            <button class="btn-refresh" @click="cargarNotificaciones" :disabled="cargando">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M23 4v6h-6"/>
                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
              </svg>
              Actualizar
            </button>
          </div>

          <!-- Tabla de notificaciones -->
          <div class="notifications-table-container">
            <table class="notifications-table">
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
                <tr v-for="notificacion in notificaciones" :key="notificacion.id" class="notification-row">
                  <td class="title-cell">
                    <div class="title-content">
                      <span class="notification-title">{{ notificacion.titulo }}</span>
                      <span v-if="notificacion.archivo_nombre" class="attachment-badge">
                        📎 {{ notificacion.archivo_nombre }}
                      </span>
                    </div>
                  </td>
                  <td class="subtitle-cell">
                    <span v-if="notificacion.subtitulo" class="notification-subtitle">
                      {{ notificacion.subtitulo }}
                    </span>
                    <span v-else class="no-subtitle">Sin subtítulo</span>
                  </td>
                  <td class="recipients-cell">
                    <span class="recipients-badge" :class="{ 'all-users': notificacion.enviada_a_todos }">
                      {{ notificacion.destinatarios_texto }}
                    </span>
                  </td>
                  <td class="date-cell">
                    <span class="notification-date">{{ formatearFecha(notificacion.fecha_envio) }}</span>
                  </td>
                  <td class="status-cell">
                    <span class="status-badge status-sent">Enviada</span>
                  </td>
                  <td class="actions-cell">
                    <div class="action-buttons">
                      <button 
                        class="btn-action btn-view" 
                        @click="verDetalle(notificacion)"
                        title="Ver detalle"
                      >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                          <circle cx="12" cy="12" r="3"/>
                        </svg>
                      </button>
                      <button 
                        class="btn-action btn-delete" 
                        @click="confirmarEliminar(notificacion)"
                        title="Eliminar notificación"
                      >
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
            <div v-if="notificaciones.length === 0" class="empty-state">
              <div class="empty-icon">📢</div>
              <h3>No hay notificaciones</h3>
              <p>Crea tu primera notificación para comunicarte con los usuarios del sistema.</p>
              <button class="btn-primary" @click="mostrarModalCrear = true">
                Crear Primera Notificación
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal Crear Notificación -->
    <div v-if="mostrarModalCrear" class="modal-overlay" @click="cerrarModalCrear">
      <div class="modal-content modal-compact" @click.stop>
        <div class="modal-header">
          <h3>Nueva Notificación</h3>
          <button class="btn-close" @click="cerrarModalCrear">×</button>
        </div>
        
        <div class="modal-body">
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

            <!-- Selector de usuarios específicos -->
            <div v-if="!formNotificacion.enviada_a_todos" class="form-group-compact">
              <label class="selector-label">Seleccionar usuarios</label>
              <div v-if="cargandoUsuarios" class="loading-users-compact">
                <div class="loading-spinner-small"></div>
                <span>Cargando...</span>
              </div>
              <div v-else class="users-selector-compact">
                <div class="search-input-wrapper">
                  <input
                    v-model="busquedaUsuarios"
                    type="text"
                    class="form-input-compact search-users"
                    placeholder="🔍 Buscar por nombre, correo o CURP..."
                    autocomplete="off"
                  />
                </div>
                <div class="users-list-compact" v-show="usuariosFiltrados.length > 0">
                  <div class="users-list-header" v-if="busquedaUsuarios">
                    {{ usuariosFiltrados.length }} resultado(s) encontrado(s)
                  </div>
                  <label
                    v-for="usuario in usuariosFiltrados"
                    :key="usuario.id"
                    class="user-option-compact"
                    :class="{ 'selected': formNotificacion.usuario_ids.includes(usuario.id) }"
                  >
                    <input
                      v-model="formNotificacion.usuario_ids"
                      :value="usuario.id"
                      type="checkbox"
                    />
                    <div class="user-info-compact">
                      <span class="user-name-compact">{{ usuario.nombre_completo || usuario.nombre || 'Sin nombre' }}</span>
                      <span class="user-email-compact">{{ usuario.correo || usuario.email || 'Sin email' }}</span>
                      <span v-if="usuario.curp" class="user-curp-compact">CURP: {{ usuario.curp }}</span>
                    </div>
                  </label>
                </div>
                <div v-show="busquedaUsuarios && usuariosFiltrados.length === 0" class="no-users-found">
                  ❌ No se encontraron usuarios que coincidan con "{{ busquedaUsuarios }}"
                </div>
                <div v-show="!busquedaUsuarios && usuarios.length === 0" class="no-users-loaded">
                  📝 No hay usuarios disponibles
                </div>
                <div class="selected-count-wrapper">
                  <small class="selected-count">
                    ✅ {{ formNotificacion.usuario_ids.length }} usuario(s) seleccionado(s)
                  </small>
                </div>
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
      
      // Toast
      toast: {
        show: false,
        type: 'success',
        message: ''
      }
    }
  },
  
  computed: {
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
    }
  },
  
  mounted() {
    this.configurarEventosConexion()
    this.cargarNotificaciones()
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

    // ==================== GESTIÓN DE NOTIFICACIONES ====================
    
    async cargarNotificaciones() {
      this.cargando = true
      this.error = null
      
      try {
        const respuesta = await notificacionesService.listarNotificaciones()
        this.notificaciones = respuesta.notificaciones || []
        console.log('✅ Notificaciones cargadas:', this.notificaciones.length)
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
        enviada_a_todos: true,
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
    
    logout() {
      localStorage.removeItem('admin_token')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

.notificaciones-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
}

.main-content {
  flex: 1;
  margin-left: min(220px, 18vw);
  max-width: calc(100vw - min(220px, 18vw));
  min-width: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* === HEADER STYLES === */
.page-header {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 50%, #2E7D32 100%);
  color: white;
  padding: 16px 24px;
  box-shadow: 
    0 2px 8px rgba(76, 175, 80, 0.3),
    0 4px 16px rgba(76, 175, 80, 0.15);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
}

.header-main {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.header-icon svg {
  width: 20px;
  height: 20px;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

.header-text {
  flex: 1;
}

.header-title {
  font-size: 20px;
  font-weight: 700;
  margin: 0 0 4px 0;
  background: linear-gradient(135deg, #ffffff 0%, #e8f5e8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-family: 'Inter', sans-serif;
}

.header-subtitle {
  font-size: 13px;
  opacity: 0.9;
  margin: 0;
  font-weight: 400;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-family: 'Inter', sans-serif;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.btn-primary {
  background: linear-gradient(135deg, #ffffff 0%, #f0fff4 100%);
  color: #2E7D32;
  border: none;
  padding: 10px 16px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  font-family: 'Inter', sans-serif;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.status-indicator {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.connection-status.online .status-indicator {
  background: #66BB6A;
  box-shadow: 0 0 8px rgba(102, 187, 106, 0.6);
}

.connection-status.offline .status-indicator {
  background: #FF7043;
  box-shadow: 0 0 8px rgba(255, 112, 67, 0.6);
}

.status-text {
  font-size: 12px;
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* === CONTENT STYLES === */
.page-content {
  flex: 1;
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

/* === LOADING & ERROR STATES === */
.loading-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
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
  border-radius: 16px;
  padding: 0;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.08),
    0 4px 16px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(76, 175, 80, 0.1);
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

.btn-delete {
  background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
  color: #d32f2f;
}

.btn-delete:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(211, 47, 47, 0.3);
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
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 
    0 24px 48px rgba(0, 0, 0, 0.2),
    0 12px 24px rgba(0, 0, 0, 0.1);
}

.modal-compact {
  max-width: 480px;
  width: 95%;
}

.modal-detail {
  max-width: 700px;
}

.modal-confirm {
  max-width: 400px;
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
  z-index: 2000;
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
@media (max-width: 1200px) {
  .main-content {
    margin-left: 260px;
    max-width: calc(100vw - 260px);
  }
}

@media (max-width: 1024px) {
  .main-content {
    margin-left: 240px;
    max-width: calc(100vw - 240px);
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    max-width: 100vw;
  }
  
  .page-header {
    padding: 12px 16px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
  
  .header-main {
    flex-direction: column;
    gap: 8px;
  }
  
  .header-actions {
    width: 100%;
    justify-content: center;
  }
  
  .page-content {
    padding: 16px;
  }
  
  .modal-content {
    width: 95%;
    max-height: 85vh;
  }
  
  .modal-compact {
    width: 98%;
    max-width: none;
    max-height: 90vh;
  }
  
  .modal-body {
    padding: 20px 16px;
  }
  
  .modal-compact .modal-body {
    padding: 16px 12px;
  }
  
  .notifications-table {
    font-size: 12px;
  }
  
  .notifications-table th,
  .notifications-table td {
    padding: 8px;
  }
  
  .title-cell {
    min-width: 150px;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 4px;
  }
  
  .btn-action {
    width: 28px;
    height: 28px;
  }
  
  .toast {
    bottom: 16px;
    right: 16px;
    left: 16px;
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .page-header {
    padding: 12px;
  }
  
  .notifications-table-container {
    overflow-x: scroll;
  }
  
  .notifications-table {
    min-width: 600px;
  }
  
  .modal-content {
    width: 98%;
    margin: 1%;
  }
  
  .modal-compact {
    width: 96%;
    margin: 2%;
    max-height: 95vh;
  }
  
  .modal-compact .modal-body {
    padding: 12px 8px;
  }
  
  .form-group-compact {
    margin-bottom: 12px;
  }
  
  .radio-group-compact {
    flex-direction: column;
    gap: 8px;
  }
  
  .users-list-compact {
    max-height: 120px;
  }
  
  .user-name-compact {
    font-size: 10px;
  }
  
  .user-email-compact {
    font-size: 9px;
  }
  
  .users-list-header {
    font-size: 10px;
  }
  
  .attachment-preview {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .attachment-actions {
    justify-content: center;
  }
  
  .modal-actions-compact {
    flex-direction: column-reverse;
    gap: 8px;
  }
  
  .btn-secondary-compact,
  .btn-primary-compact {
    width: 100%;
    justify-content: center;
  }
  
  .file-text {
    max-width: 150px;
  }
}
</style>
