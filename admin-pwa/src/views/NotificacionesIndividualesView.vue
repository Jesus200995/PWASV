<template>
  <div class="notificaciones-individuales-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
       <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                <circle cx="12" cy="12" r="2" fill="currentColor"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Notificaciones Individuales</h1>
              <p class="header-subtitle">Envía notificaciones personalizadas a usuarios específicos</p>
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
            <h2>Notificaciones Enviadas Individualmente ({{ notificaciones.length }})</h2>
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
                    <span class="recipients-badge">
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
                      <button class="btn-action btn-view" @click="verDetalle(notificacion)" title="Ver detalles">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                          <circle cx="12" cy="12" r="3"/>
                        </svg>
                      </button>
                      <button class="btn-action btn-stats" @click="verEstadisticas(notificacion)" title="Ver estadísticas">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M3 3v18h18"/>
                          <path d="M18 17V9"/>
                          <path d="M13 17V5"/>
                          <path d="M8 17v-3"/>
                        </svg>
                      </button>
                      <button class="btn-action btn-delete" @click="confirmarEliminar(notificacion)" title="Eliminar">
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
              <h3>No hay notificaciones individuales</h3>
              <p>Crea tu primera notificación individualizada para usuarios específicos.</p>
              <button class="btn-primary-large" @click="mostrarModalCrear = true">
                Crear Primera Notification
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal Crear Notificación -->
    <div v-if="mostrarModalCrear" class="modal-overlay" @click="cerrarModalCrear">
      <div class="modal-content modal-expanded" @click.stop>
        <div class="modal-header">
          <h3>Nueva Notificación Individual</h3>
          <button class="btn-close" @click="cerrarModalCrear">×</button>
        </div>
        
        <div class="modal-body modal-body-two-columns">
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
                <button type="submit" class="btn-primary-compact" :disabled="enviandoNotificacion || formNotificacion.usuario_ids.length === 0">
                  <span v-if="enviandoNotificacion" class="loading-spinner-small"></span>
                  {{ enviandoNotificacion ? 'Enviando...' : 'Enviar' }}
                </button>
              </div>
            </form>
          </div>

          <!-- Columna del selector de usuarios -->
          <div class="users-column">
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
  name: 'NotificacionesIndividualesView',
  components: {
    Sidebar
  },
  data() {
    return {
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
        enviada_a_todos: false,  // Siempre false para individuales
        usuario_ids: []
      },
      
      // Usuarios para selector
      usuarios: [],
      cargandoUsuarios: false,
      busquedaUsuarios: '',
      
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
    this.cargarNotificaciones()
    this.cargarUsuarios()
  },
  
  methods: {
    async cargarNotificaciones() {
      this.cargando = true
      this.error = null
      
      try {
        // Filtrar solo notificaciones individuales
        const respuesta = await notificacionesService.listarNotificaciones(50, 0, 'individuales')
        this.notificaciones = respuesta.notificaciones || []
        console.log('✅ Notificaciones individuales cargadas:', this.notificaciones.length)
      } catch (error) {
        console.error('❌ Error cargando notificaciones:', error)
        this.error = error.message
      } finally {
        this.cargando = false
      }
    },

    async cargarUsuarios() {
      if (this.usuarios.length > 0) {
        return
      }
      
      this.cargandoUsuarios = true
      try {
        const respuesta = await usuariosService.obtenerUsuarios()
        
        if (Array.isArray(respuesta)) {
          this.usuarios = respuesta
        } else if (respuesta && Array.isArray(respuesta.usuarios)) {
          this.usuarios = respuesta.usuarios
        } else {
          this.usuarios = []
        }
        
        console.log('✅ Usuarios cargados:', this.usuarios.length)
        
      } catch (error) {
        console.error('❌ Error cargando usuarios:', error)
        this.mostrarToast('Error al cargar usuarios: ' + error.message, 'error')
        this.usuarios = []
      } finally {
        this.cargandoUsuarios = false
      }
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
        console.log('📎 Archivo seleccionado:', archivo.name)
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
      
      if (this.formNotificacion.usuario_ids.length === 0) {
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
        enviada_a_todos: false,
        usuario_ids: []
      }
      this.archivoSeleccionado = null
      if (this.$refs.archivoInput) {
        this.$refs.archivoInput.value = ''
      }
      this.busquedaUsuarios = ''
    },

    verDetalle(notificacion) {
      console.log('Ver detalle:', notificacion)
      this.mostrarToast('Función en desarrollo', 'error')
    },

    verEstadisticas(notificacion) {
      console.log('Ver estadísticas:', notificacion)
      this.mostrarToast('Función en desarrollo', 'error')
    },

    confirmarEliminar(notificacion) {
      if (confirm(`¿Estás seguro de que deseas eliminar la notificación "${notificacion.titulo}"?`)) {
        this.eliminarNotificacion(notificacion.id)
      }
    },

    async eliminarNotificacion(id) {
      try {
        await notificacionesService.eliminarNotificacion(id)
        this.mostrarToast('Notificación eliminada exitosamente', 'success')
        this.cargarNotificaciones()
      } catch (error) {
        console.error('❌ Error eliminando notificación:', error)
        this.mostrarToast(error.message, 'error')
      }
    },

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
      authService.logout()
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* Copiar los estilos de NotificacionesView.vue */
.notificaciones-individuales-container {
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
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-sizing: border-box;
  overflow-x: hidden;
}

/* Header con barra verde */
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
  box-shadow: inset 0 -1px 0 rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.header-icon svg {
  width: clamp(14px, 2.5vw, 16px);
  height: clamp(14px, 2.5vw, 16px);
  color: white;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  z-index: 1;
  position: relative;
}

.header-text {
  flex: 1;
  color: white;
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
  color: rgba(255, 255, 255, 0.9);
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
  z-index: 1;
  position: relative;
  transition: all 0.3s ease;
}

.btn-primary:hover svg {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
  transform: scale(1.05);
}

/* Contenido de la página */
.page-content {
  padding: clamp(1rem, 2vw, 1.5rem);
  flex: 1;
}

/* Estados de carga y error */
.loading-state, .error-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f4f6;
  border-top-color: #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.btn-secondary {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: #45a049;
}

/* Lista de notificaciones */
.notificaciones-list {
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.list-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.list-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

.btn-refresh {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.875rem;
}

.btn-refresh:hover:not(:disabled) {
  background: #45a049;
  transform: translateY(-2px);
}

.btn-refresh:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Tabla de notificaciones */
.notifications-table-container {
  overflow-x: auto;
}

.notifications-table {
  width: 100%;
  border-collapse: collapse;
}

.notifications-table thead {
  background: #f9fafb;
}

.notifications-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-family: 'Inter', sans-serif;
}

.notifications-table tbody tr {
  border-bottom: 1px solid #f3f4f6;
  transition: background-color 0.2s ease;
}

.notifications-table tbody tr:hover {
  background: #f9fafb;
}

.notifications-table td {
  padding: 1rem;
  color: #4b5563;
  font-family: 'Inter', sans-serif;
}

.title-cell {
  min-width: 200px;
}

.title-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.notification-title {
  font-weight: 600;
  color: #1f2937;
}

.attachment-badge {
  font-size: 0.75rem;
  color: #6b7280;
}

.subtitle-cell {
  min-width: 150px;
}

.notification-subtitle {
  color: #6b7280;
}

.no-subtitle {
  color: #9ca3af;
  font-style: italic;
  font-size: 0.875rem;
}

.recipients-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #dbeafe;
  color: #1e40af;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
}

.date-cell {
  white-space: nowrap;
}

.notification-date {
  color: #6b7280;
  font-size: 0.875rem;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
}

.status-sent {
  background: #d1fae5;
  color: #065f46;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.btn-action {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-view {
  background: #dbe afe;
  color: #1e40af;
}

.btn-view:hover {
  background: #bfdbfe;
}

.btn-stats {
  background: #fef3c7;
  color: #92400e;
}

.btn-stats:hover {
  background: #fde68a;
}

.btn-delete {
  background: #fee2e2;
  color: #991b1b;
}

.btn-delete:hover {
  background: #fecaca;
}

/* Estado vacío */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  margin: 0 0 0.5rem 0;
  color: #1f2937;
  font-size: 1.5rem;
  font-family: 'Inter', sans-serif;
}

.empty-state p {
  margin: 0 0 1.5rem 0;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
}

.btn-primary-large {
  padding: 0.75rem 2rem;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
  font-family: 'Inter', sans-serif;
}

.btn-primary-large:hover {
  background: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 100%;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  max-height: 90vh;
  overflow-y: auto;
  font-family: 'Inter', sans-serif;
}

.modal-expanded {
  max-width: 1000px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

.btn-close {
  background: none;
  border: none;
  font-size: 2rem;
  color: #6b7280;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.btn-close:hover {
  background: #f3f4f6;
}

.modal-body {
  padding: 0;
}

.modal-body-two-columns {
  display: grid;
  grid-template-columns:  1fr 350px;
  gap: 0;
  height: calc(90vh - 140px);
}

.form-column {
  padding: 2rem;
  overflow-y: auto;
  border-right: 1px solid #e5e7eb;
}

.form-group-compact {
  margin-bottom: 1.5rem;
}

.form-group-compact label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
  font-family: 'Inter', sans-serif;
}

.form-input-compact, .form-textarea-compact {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.95rem;
  font-family: 'Inter', sans-serif;
  transition: all 0.3s ease;
}

.form-input-compact:focus, .form-textarea-compact:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.form-textarea-compact {
  resize: vertical;
}

.char-count {
  display: block;
  text-align: right;
  margin-top: 0.25rem;
  font-size: 0.75rem;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
}

.file-input {
  display: none;
}

.file-input-container-compact {
  position: relative;
}

.file-input-label-compact {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border: 2px dashed #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}

.file-input-label-compact:hover {
  border-color: #4CAF50;
  background: rgba(76, 175, 80, 0.05);
}

.file-text {
  flex: 1;
  font-size: 0.875rem;
  color: #6b7280;
}

.file-help-compact {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.75rem;
  color: #9ca3af;
  font-family: 'Inter', sans-serif;
}

.modal-actions-compact {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.btn-secondary-compact {
  padding: 0.75rem 1.5rem;
  background: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}

.btn-secondary-compact:hover {
  background: #e5e7eb;
}

.btn-primary-compact {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}

.btn-primary-compact:hover:not(:disabled) {
  background: #45a049;
  transform: translateY(-2px);
}

.btn-primary-compact:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Selector de usuarios */
.users-column {
  padding: 1.5rem;
  background: #f9fafb;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.users-column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.users-column-header h4 {
  margin: 0;
  font-size: 1rem;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

.selected-count-badge {
  padding: 0.25rem 0.75rem;
  background: #4CAF50;
  color: white;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
}

.loading-users-compact {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  gap: 1rem;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
}

.users-selector-column {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.search-input-wrapper {
  margin-bottom: 1rem;
}

.search-users-column {
  width: 100%;
}

.users-list-column {
  flex: 1;
  overflow-y: auto;
  max-height: calc(90vh - 300px);
}

.users-list-header {
  padding: 0.5rem;
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
}

.user-option-column {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.user-option-column:hover {
  border-color: #4CAF50;
  background: rgba(76, 175, 80, 0.05);
}

.user-option-column.selected {
  border-color: #4CAF50;
  background: rgba(76, 175, 80, 0.1);
}

.user-option-column input[type="checkbox"] {
  margin-top: 2px;
  cursor: pointer;
}

.user-info-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.user-name-column {
  font-weight: 600;
  color: #1f2937;
  font-size: 0.875rem;
  font-family: 'Inter', sans-serif;
}

.user-email-column {
  color: #6b7280;
  font-size: 0.75rem;
  font-family: 'Inter', sans-serif;
}

.user-curp-column {
  color: #9ca3af;
  font-size: 0.75rem;
  font-family: 'Inter', sans-serif;
}

.no-users-found-column, .no-users-loaded-column {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
}

/* Toast */
.toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  min-width: 300px;
  z-index: 2000;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.toast.success {
  border-left: 4px solid #4CAF50;
}

.toast.error {
  border-left: 4px solid #ef4444;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.toast-icon {
  font-size: 1.5rem;
}

.toast-message {
  color: #1f2937;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
}

/* Responsive */
@media (max-width: 992px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
}

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

  .modal-body-two-columns {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr;
    height: auto;
  }
  
  .form-column {
    border-right: none;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .users-column {
    max-height: 50vh;
  }

  .notifications-table {
    font-size: 11px;
  }

  .notifications-table th,
  .notifications-table td {
    padding: 6px;
  }
}

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
  
  .modal-content {
    width: 100%;
    max-width: 100%;
    height: 100vh;
    max-height: 100vh;
    border-radius: 0;
  }
  
  .modal-body-two-columns {
    height: calc(100vh - 140px);
  }
}
</style>
