<template>
  <div v-if="visible" class="modal-overlay" @click="cerrarModal">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <div class="modal-title-section">
          <div class="modal-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
              <circle cx="12" cy="8" r="1" opacity="0.6"/>
            </svg>
          </div>
          <div class="modal-title-text">
            <h2>{{ esEdicion ? 'Editar Notificación' : 'Nueva Notificación' }}</h2>
            <p>{{ esEdicion ? 'Modifica los datos de la notificación' : 'Crea una nueva notificación para los usuarios' }}</p>
          </div>
        </div>
        <button @click="cerrarModal" class="close-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      
      <div class="modal-body">
        <form @submit.prevent="guardarNotificacion" class="notification-form">
          
          <!-- Título -->
          <div class="form-group">
            <label class="form-label" for="titulo">
              <span class="label-text">Título *</span>
              <span class="label-hint">Máximo 150 caracteres</span>
            </label>
            <input
              id="titulo"
              v-model="form.title"
              type="text"
              class="form-input"
              placeholder="Ej: Nueva actualización disponible"
              maxlength="150"
              required
            >
            <div class="char-counter">{{ form.title.length }}/150</div>
          </div>
          
          <!-- Mensaje -->
          <div class="form-group">
            <label class="form-label" for="mensaje">
              <span class="label-text">Mensaje *</span>
              <span class="label-hint">Contenido de la notificación</span>
            </label>
            <textarea
              id="mensaje"
              v-model="form.body"
              class="form-textarea"
              placeholder="Escribe el mensaje de la notificación..."
              rows="4"
              required
            ></textarea>
            <div class="char-counter">{{ form.body.length }} caracteres</div>
          </div>
          
          <div class="form-row">
            <!-- Tipo -->
            <div class="form-group">
              <label class="form-label" for="tipo">
                <span class="label-text">Tipo</span>
                <span class="label-hint">Categoría de la notificación</span>
              </label>
              <select
                id="tipo"
                v-model="form.type"
                class="form-select"
              >
                <option value="info">ℹ️ Informativa</option>
                <option value="success">✅ Éxito</option>
                <option value="warning">⚠️ Advertencia</option>
                <option value="urgent">🚨 Urgente</option>
              </select>
            </div>
            
            <!-- Audiencia -->
            <div class="form-group">
              <label class="form-label" for="audiencia">
                <span class="label-text">Destinatarios</span>
                <span class="label-hint">A quién enviar</span>
              </label>
              <select
                id="audiencia"
                v-model="form.audience"
                class="form-select"
                @change="onAudienceChange"
              >
                <option value="all">🌐 Todos los usuarios</option>
                <option value="users">👥 Usuarios específicos</option>
              </select>
            </div>
          </div>
          
          <!-- Selección de usuarios específicos -->
          <div v-if="form.audience === 'users'" class="form-group">
            <label class="form-label">
              <span class="label-text">Seleccionar Usuarios *</span>
              <span class="label-hint">Usuarios que recibirán la notificación</span>
            </label>
            <div v-if="cargandoUsuarios" class="loading-users">
              <div class="spinner"></div>
              <span>Cargando usuarios...</span>
            </div>
            <div v-else class="users-selection">
              <div class="users-search">
                <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="m21 21-4.35-4.35"></path>
                </svg>
                <input
                  v-model="busquedaUsuarios"
                  type="text"
                  placeholder="Buscar usuarios..."
                  class="users-search-input"
                >
              </div>
              <div class="users-list">
                <div
                  v-for="usuario in usuariosFiltrados"
                  :key="usuario.id"
                  class="user-item"
                  :class="{ selected: form.users.includes(usuario.id) }"
                  @click="toggleUsuario(usuario.id)"
                >
                  <div class="user-checkbox">
                    <svg v-if="form.users.includes(usuario.id)" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                  </div>
                  <div class="user-info">
                    <div class="user-name">{{ usuario.nombre_completo }}</div>
                    <div class="user-email">{{ usuario.correo }}</div>
                  </div>
                </div>
              </div>
              <div class="selected-count">
                {{ form.users.length }} usuario{{ form.users.length !== 1 ? 's' : '' }} seleccionado{{ form.users.length !== 1 ? 's' : '' }}
              </div>
            </div>
          </div>
          
          <!-- Programación de envío -->
          <div class="form-group">
            <label class="form-label">
              <span class="label-text">Programación</span>
              <span class="label-hint">¿Cuándo enviar la notificación?</span>
            </label>
            <div class="scheduling-options">
              <label class="radio-option">
                <input
                  type="radio"
                  name="scheduling"
                  value="now"
                  v-model="schedulingType"
                >
                <span class="radio-label">📤 Enviar ahora</span>
              </label>
              <label class="radio-option">
                <input
                  type="radio"
                  name="scheduling"
                  value="draft"
                  v-model="schedulingType"
                >
                <span class="radio-label">📝 Guardar como borrador</span>
              </label>
              <label class="radio-option">
                <input
                  type="radio"
                  name="scheduling"
                  value="scheduled"
                  v-model="schedulingType"
                >
                <span class="radio-label">⏰ Programar envío</span>
              </label>
            </div>
            
            <div v-if="schedulingType === 'scheduled'" class="scheduled-datetime">
              <input
                v-model="form.scheduled_at"
                type="datetime-local"
                class="form-input"
                :min="fechaMinima"
              >
            </div>
          </div>
          
          <!-- Metadata adicional -->
          <div class="form-group">
            <label class="form-label">
              <span class="label-text">Metadatos (Opcional)</span>
              <span class="label-hint">Información adicional en formato JSON</span>
            </label>
            <textarea
              v-model="metadataText"
              class="form-textarea metadata-input"
              placeholder='{"priority": "high", "category": "system"}'
              rows="3"
            ></textarea>
            <div v-if="metadataError" class="error-message">
              ❌ JSON inválido: {{ metadataError }}
            </div>
          </div>
          
        </form>
      </div>
      
      <div class="modal-footer">
        <button @click="cerrarModal" type="button" class="btn-secondary">
          Cancelar
        </button>
        <button @click="guardarNotificacion" type="submit" class="btn-primary" :disabled="enviando || !formularioValido">
          <span v-if="enviando" class="loading-spinner"></span>
          {{ enviando ? 'Guardando...' : (esEdicion ? 'Actualizar' : 'Crear Notificación') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import notificacionesService from '../services/notificacionesService.js'

export default {
  name: 'NotificacionModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    notificacion: {
      type: Object,
      default: null
    }
  },
  emits: ['close', 'saved'],
  data() {
    return {
      enviando: false,
      cargandoUsuarios: false,
      usuarios: [],
      busquedaUsuarios: '',
      schedulingType: 'now',
      metadataText: '',
      metadataError: null,
      form: {
        title: '',
        body: '',
        type: 'info',
        audience: 'all',
        users: [],
        scheduled_at: null,
        metadata: null
      }
    }
  },
  computed: {
    esEdicion() {
      return !!this.notificacion
    },
    usuariosFiltrados() {
      if (!this.busquedaUsuarios.trim()) {
        return this.usuarios
      }
      const termino = this.busquedaUsuarios.toLowerCase()
      return this.usuarios.filter(usuario => 
        usuario.nombre_completo.toLowerCase().includes(termino) ||
        usuario.correo.toLowerCase().includes(termino)
      )
    },
    formularioValido() {
      const tituloValido = this.form.title.trim().length > 0
      const mensajeValido = this.form.body.trim().length > 0
      const audienciaValida = this.form.audience === 'all' || 
        (this.form.audience === 'users' && this.form.users.length > 0)
      
      return tituloValido && mensajeValido && audienciaValida && !this.metadataError
    },
    fechaMinima() {
      const now = new Date()
      return now.toISOString().slice(0, 16)
    }
  },
  watch: {
    visible(newVal) {
      if (newVal) {
        this.cargarDatos()
      } else {
        this.resetearForm()
      }
    },
    'form.audience'() {
      if (this.form.audience === 'users' && this.usuarios.length === 0) {
        this.cargarUsuarios()
      }
    },
    metadataText(newVal) {
      this.validarMetadata(newVal)
    }
  },
  methods: {
    async cargarDatos() {
      if (this.esEdicion) {
        this.form = { ...this.notificacion }
        if (this.notificacion.metadata) {
          this.metadataText = JSON.stringify(this.notificacion.metadata, null, 2)
        }
      }
      
      if (this.form.audience === 'users') {
        await this.cargarUsuarios()
      }
    },
    
    async cargarUsuarios() {
      if (this.usuarios.length > 0) return
      
      try {
        this.cargandoUsuarios = true
        const response = await notificacionesService.obtenerUsuarios()
        this.usuarios = Array.isArray(response) ? response : (response.usuarios || [])
      } catch (error) {
        console.error('Error cargando usuarios:', error)
        this.$emit('error', 'Error al cargar la lista de usuarios')
      } finally {
        this.cargandoUsuarios = false
      }
    },
    
    onAudienceChange() {
      if (this.form.audience === 'all') {
        this.form.users = []
      }
    },
    
    toggleUsuario(userId) {
      const index = this.form.users.indexOf(userId)
      if (index > -1) {
        this.form.users.splice(index, 1)
      } else {
        this.form.users.push(userId)
      }
    },
    
    validarMetadata(texto) {
      this.metadataError = null
      
      if (!texto.trim()) {
        this.form.metadata = null
        return
      }
      
      try {
        this.form.metadata = JSON.parse(texto)
      } catch (error) {
        this.metadataError = error.message
      }
    },
    
    async guardarNotificacion() {
      if (!this.formularioValido) return
      
      try {
        this.enviando = true
        
        // Preparar datos para enviar
        const datosNotificacion = {
          title: this.form.title.trim(),
          body: this.form.body.trim(),
          type: this.form.type,
          audience: this.form.audience,
          metadata: this.form.metadata
        }
        
        // Añadir usuarios específicos si es necesario
        if (this.form.audience === 'users') {
          datosNotificacion.users = this.form.users
        }
        
        // Manejar programación
        if (this.schedulingType === 'scheduled' && this.form.scheduled_at) {
          datosNotificacion.scheduled_at = this.form.scheduled_at
        }
        
        let resultado
        if (this.esEdicion) {
          // TODO: Implementar endpoint de actualización
          throw new Error('Función de edición aún no implementada')
        } else {
          resultado = await notificacionesService.crearNotificacion(datosNotificacion)
        }
        
        // Si se debe enviar inmediatamente
        if (this.schedulingType === 'now') {
          await notificacionesService.enviarNotificacion(resultado.id)
        }
        
        this.$emit('saved', resultado)
        this.cerrarModal()
        
      } catch (error) {
        console.error('Error guardando notificación:', error)
        this.$emit('error', error.message || 'Error al guardar la notificación')
      } finally {
        this.enviando = false
      }
    },
    
    resetearForm() {
      this.form = {
        title: '',
        body: '',
        type: 'info',
        audience: 'all',
        users: [],
        scheduled_at: null,
        metadata: null
      }
      this.schedulingType = 'now'
      this.metadataText = ''
      this.metadataError = null
      this.busquedaUsuarios = ''
    },
    
    cerrarModal() {
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-container {
  background: #ffffff;
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #f8f9fa, #ffffff);
}

.modal-title-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.modal-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.modal-title-text h2 {
  margin: 0 0 0.25rem;
  font-size: 1.4rem;
  font-weight: 600;
  color: #2E7D32;
}

.modal-title-text p {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
}

.close-btn {
  background: transparent;
  border: none;
  padding: 8px;
  cursor: pointer;
  border-radius: 8px;
  color: #666;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background-color: #f5f5f5;
  color: #333;
}

.modal-body {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

.notification-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.label-text {
  font-weight: 500;
  color: #333;
  font-size: 0.9rem;
}

.label-hint {
  font-size: 0.8rem;
  color: #666;
}

.form-input,
.form-textarea,
.form-select {
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.9rem;
  transition: all 0.2s ease;
  font-family: inherit;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.char-counter {
  font-size: 0.75rem;
  color: #999;
  text-align: right;
  margin-top: 0.25rem;
}

.users-selection {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.users-search {
  position: relative;
  padding: 0.5rem;
  background-color: #f9f9f9;
  border-bottom: 1px solid #e0e0e0;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.users-search-input {
  width: 100%;
  padding: 0.5rem 0.5rem 0.5rem 2.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 0.85rem;
}

.users-list {
  max-height: 200px;
  overflow-y: auto;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
  border-bottom: 1px solid #f5f5f5;
}

.user-item:hover {
  background-color: #f9f9f9;
}

.user-item.selected {
  background-color: rgba(76, 175, 80, 0.1);
}

.user-checkbox {
  width: 20px;
  height: 20px;
  border: 2px solid #e0e0e0;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.user-item.selected .user-checkbox {
  background-color: #4CAF50;
  border-color: #4CAF50;
  color: white;
}

.user-info {
  flex: 1;
}

.user-name {
  font-weight: 500;
  color: #333;
  font-size: 0.9rem;
}

.user-email {
  font-size: 0.8rem;
  color: #666;
}

.selected-count {
  padding: 0.5rem 0.75rem;
  background-color: #f9f9f9;
  font-size: 0.8rem;
  color: #666;
  text-align: center;
}

.scheduling-options {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: background-color 0.2s ease;
}

.radio-option:hover {
  background-color: #f9f9f9;
}

.radio-label {
  font-size: 0.9rem;
  color: #333;
}

.scheduled-datetime {
  margin-top: 0.5rem;
}

.metadata-input {
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
  font-size: 0.8rem;
}

.error-message {
  color: #f44336;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.loading-users {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  justify-content: center;
  color: #666;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #e0e0e0;
  border-radius: 50%;
  border-top-color: #4CAF50;
  animation: spin 1s linear infinite;
}

.modal-footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  background-color: #f8f9fa;
}

.btn-secondary,
.btn-primary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-secondary {
  background: #f5f5f5;
  color: #666;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.btn-primary {
  background: linear-gradient(to bottom, #4CAF50, #43A047);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(to bottom, #43A047, #388E3C);
  transform: translateY(-1px);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (max-width: 640px) {
  .modal-container {
    max-width: 100%;
    max-height: 100%;
    border-radius: 0;
  }
  
  .modal-header,
  .modal-body,
  .modal-footer {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .modal-footer {
    flex-direction: column;
  }
  
  .btn-secondary,
  .btn-primary {
    width: 100%;
    justify-content: center;
  }
}
</style>
