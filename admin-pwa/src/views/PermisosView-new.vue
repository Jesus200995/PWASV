<template>
  <div class="permisos-container">
    <Sidebar_NEW @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2a10 10 0 1 0 10 10 4 4 0 0 0-4-4H8a4 4 0 0 0-4 4 6 6 0 0 0 6 6z"/>
                <path d="M8.21 13.89 7 23l5-3 5 3-1.21-9.12"/>
                <path d="M16 12a4 4 0 0 0-8 0"/>
                <circle cx="12" cy="8" r="2"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Gestión de Permisos</h1>
              <p class="header-subtitle">Administra usuarios administrativos y sus permisos de acceso</p>
            </div>
          </div>
          <div class="header-actions">
            <button class="btn-primary" @click="mostrarModalCrear = true">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 5v14"/>
                <path d="M5 12h14"/>
              </svg>
              Nuevo Usuario Admin
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
          <p>Cargando usuarios administrativos...</p>
        </div>

        <!-- Mensaje de error -->
        <div v-if="error && !cargando" class="error-state">
          <div class="error-icon">⚠️</div>
          <h3>Error al cargar usuarios administrativos</h3>
          <p>{{ error }}</p>
          <button class="btn-secondary" @click="cargarUsuariosAdmin">Reintentar</button>
        </div>

        <!-- Lista de usuarios administrativos -->
        <div v-if="!cargando && !error" class="usuarios-list">
          <div class="list-header">
            <h2>Usuarios Administrativos ({{ usuariosAdmin.length }})</h2>
            <div class="header-filters">
              <select v-model="filtroRol" class="filter-select" @change="aplicarFiltros">
                <option value="">Todos los roles</option>
                <option value="admin">Admin</option>
                <option value="user">Usuario</option>
              </select>
              <button class="btn-refresh" @click="cargarUsuariosAdmin" :disabled="cargando">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M23 4v6h-6"/>
                  <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
                </svg>
                Actualizar
              </button>
            </div>
          </div>

          <!-- Tabla de usuarios administrativos -->
          <div class="usuarios-table-container">
            <table class="usuarios-table">
              <thead>
                <tr>
                  <th>Usuario</th>
                  <th>Rol</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="usuario in usuariosFiltrados" :key="usuario.id" class="usuario-row">
                  <td class="name-cell">
                    <div class="user-info">
                      <div class="user-avatar">
                        {{ usuario.username.charAt(0).toUpperCase() }}
                      </div>
                      <div class="user-details">
                        <div class="user-name">{{ usuario.username }}</div>
                        <div class="user-supervisor">ID: {{ usuario.id }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="rol-cell">
                    <span class="rol-badge" :class="usuario.rol">
                      {{ usuario.rol === 'admin' ? '👑 Administrador' : '👤 Usuario' }}
                    </span>
                  </td>
                  <td class="status-cell">
                    <span class="status-badge status-active">Activo</span>
                  </td>
                  <td class="actions-cell">
                    <div class="action-buttons">
                      <button 
                        class="btn-action btn-edit" 
                        @click="editarUsuario(usuario)"
                        title="Editar usuario"
                      >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                          <path d="M18.5 2.5a2.12 2.12 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                        </svg>
                      </button>
                      <button 
                        v-if="usuario.username !== 'admin'"
                        class="btn-action btn-delete" 
                        @click="confirmarEliminar(usuario)"
                        title="Eliminar usuario"
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
            <div v-if="usuariosFiltrados.length === 0" class="empty-state">
              <div class="empty-icon">👥</div>
              <h3>No hay usuarios administrativos</h3>
              <p>Crea el primer usuario administrativo para gestionar el sistema.</p>
              <button class="btn-primary" @click="mostrarModalCrear = true">
                Crear Primer Usuario Admin
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal Crear/Editar Usuario -->
    <div v-if="mostrarModalCrear || mostrarModalEditar" class="modal-overlay" @click="cerrarModales">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ modoEdicion ? 'Editar Usuario Admin' : 'Nuevo Usuario Admin' }}</h3>
          <button class="btn-close" @click="cerrarModales">×</button>
        </div>
        
        <div class="modal-body">
          <!-- Sección de Información básica -->
          <div class="form-section">
            <h4>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
              Información Básica
            </h4>
            
            <form @submit.prevent="guardarUsuario">
              <!-- Username -->
              <div class="form-group">
                <label for="username">Nombre de Usuario *</label>
                <input
                  id="username"
                  v-model="formularioUsuario.username"
                  type="text"
                  class="form-input"
                  placeholder="Ingrese el nombre de usuario"
                  :disabled="modoEdicion && formularioUsuario.username === 'admin'"
                  required
                />
                <small class="form-help">Debe ser único y no puede contener espacios</small>
              </div>

              <!-- Password -->
              <div class="form-group">
                <label for="password">{{ modoEdicion ? 'Nueva Contraseña (opcional)' : 'Contraseña *' }}</label>
                <input
                  id="password"
                  v-model="formularioUsuario.password"
                  type="password"
                  class="form-input"
                  placeholder="Ingrese la contraseña"
                  :required="!modoEdicion"
                />
                <small class="form-help">
                  {{ modoEdicion ? 'Deje vacío para mantener la contraseña actual' : 'Mínimo 6 caracteres' }}
                </small>
              </div>

              <!-- Rol -->
              <div class="form-group">
                <label>Rol del Usuario *</label>
                <div class="radio-group">
                  <div 
                    class="radio-option" 
                    :class="{ 'selected': formularioUsuario.rol === 'admin' }"
                    @click="formularioUsuario.rol = 'admin'"
                  >
                    <input
                      v-model="formularioUsuario.rol"
                      type="radio"
                      value="admin"
                      :disabled="modoEdicion && formularioUsuario.username === 'admin'"
                    />
                    <div class="radio-content">
                      <div class="radio-title">👑 Administrador</div>
                      <div class="radio-description">
                        Acceso completo al sistema, puede gestionar usuarios, configuraciones y todos los módulos
                      </div>
                    </div>
                  </div>
                  
                  <div 
                    class="radio-option"
                    :class="{ 'selected': formularioUsuario.rol === 'user' }"
                    @click="formularioUsuario.rol = 'user'"
                  >
                    <input
                      v-model="formularioUsuario.rol"
                      type="radio"
                      value="user"
                      :disabled="modoEdicion && formularioUsuario.username === 'admin'"
                    />
                    <div class="radio-content">
                      <div class="radio-title">👤 Usuario</div>
                      <div class="radio-description">
                        Acceso limitado, puede ver reportes y consultar información básica del sistema
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Botones -->
              <div class="modal-actions">
                <button type="button" class="btn-secondary" @click="cerrarModales">
                  Cancelar
                </button>
                <button type="submit" class="btn-primary" :disabled="guardando">
                  <span v-if="guardando" class="loading-spinner-small"></span>
                  {{ guardando ? 'Guardando...' : (modoEdicion ? 'Actualizar' : 'Crear Usuario') }}
                </button>
              </div>
            </form>
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
            <h4>¿Estás seguro de que deseas eliminar este usuario administrativo?</h4>
            <p><strong>Usuario:</strong> {{ usuarioAEliminar?.username }}</p>
            <p><strong>Rol:</strong> {{ usuarioAEliminar?.rol }}</p>
            
            <div class="warning-text">
              Esta acción no se puede deshacer. El usuario perderá acceso inmediatamente al sistema administrativo.
            </div>
          </div>

          <div class="modal-actions">
            <button class="btn-secondary" @click="cancelarEliminar">
              Cancelar
            </button>
            <button class="btn-danger" @click="eliminarUsuario" :disabled="eliminando">
              <span v-if="eliminando" class="loading-spinner-small"></span>
              {{ eliminando ? 'Eliminando...' : 'Eliminar Usuario' }}
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
import permisosService from '../services/permisosService.js'

export default {
  name: 'PermisosView',
  components: {
    Sidebar
  },
  data() {
    return {
      isOnline: navigator.onLine,
      cargando: false,
      error: null,
      
      // Lista de usuarios admin
      usuariosAdmin: [],
      filtroRol: '',
      
      // Modal crear/editar usuario
      mostrarModalCrear: false,
      mostrarModalEditar: false,
      modoEdicion: false,
      usuarioEditando: null,
      guardando: false,
      formularioUsuario: {
        username: '',
        password: '',
        rol: 'user'
      },
      
      // Modal eliminar
      mostrarModalEliminar: false,
      usuarioAEliminar: null,
      eliminando: false,
      
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
      if (!this.filtroRol) return this.usuariosAdmin
      return this.usuariosAdmin.filter(usuario => usuario.rol === this.filtroRol)
    }
  },
  
  mounted() {
    this.configurarEventosConexion()
    this.cargarUsuariosAdmin()
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

    // ==================== GESTIÓN DE USUARIOS ADMIN ====================
    
    async cargarUsuariosAdmin() {
      this.cargando = true
      this.error = null
      
      try {
        const respuesta = await permisosService.obtenerUsuariosAdmin()
        this.usuariosAdmin = respuesta.usuarios || []
        console.log('✅ Usuarios admin cargados:', this.usuariosAdmin.length)
      } catch (error) {
        console.error('❌ Error cargando usuarios admin:', error)
        this.error = error.message
      } finally {
        this.cargando = false
      }
    },

    aplicarFiltros() {
      // Los filtros se aplican automáticamente a través del computed usuariosFiltrados
      console.log('🔍 Filtro aplicado:', this.filtroRol)
    },

    // ==================== CREAR/EDITAR USUARIO ADMIN ====================
    
    editarUsuario(usuario) {
      this.modoEdicion = true
      this.usuarioEditando = usuario
      this.formularioUsuario = {
        username: usuario.username,
        password: '', // No mostramos la contraseña actual
        rol: usuario.rol
      }
      this.mostrarModalEditar = true
    },

    async guardarUsuario() {
      // Validaciones básicas
      if (!this.formularioUsuario.username.trim()) {
        this.mostrarToast('El nombre de usuario es obligatorio', 'error')
        return
      }
      
      // Validar que no tenga espacios
      if (this.formularioUsuario.username.includes(' ')) {
        this.mostrarToast('El nombre de usuario no puede contener espacios', 'error')
        return
      }
      
      if (!this.modoEdicion && !this.formularioUsuario.password.trim()) {
        this.mostrarToast('La contraseña es obligatoria para nuevos usuarios', 'error')
        return
      }

      if (this.formularioUsuario.password && this.formularioUsuario.password.length < 6) {
        this.mostrarToast('La contraseña debe tener al menos 6 caracteres', 'error')
        return
      }
      
      this.guardando = true
      
      try {
        if (this.modoEdicion) {
          // Actualizar usuario existente
          const datosActualizacion = {
            username: this.formularioUsuario.username,
            rol: this.formularioUsuario.rol
          }
          
          // Solo incluir password si se proporcionó
          if (this.formularioUsuario.password.trim()) {
            datosActualizacion.password = this.formularioUsuario.password
          }
          
          await permisosService.actualizarUsuarioAdmin(this.usuarioEditando.id, datosActualizacion)
          this.mostrarToast('Usuario administrativo actualizado exitosamente', 'success')
        } else {
          // Crear nuevo usuario
          await permisosService.crearUsuarioAdmin(this.formularioUsuario)
          this.mostrarToast('Usuario administrativo creado exitosamente', 'success')
        }
        
        // Recargar lista y cerrar modal
        this.cargarUsuariosAdmin()
        this.cerrarModales()
        
      } catch (error) {
        console.error('❌ Error guardando usuario admin:', error)
        this.mostrarToast(error.message, 'error')
      } finally {
        this.guardando = false
      }
    },

    cerrarModales() {
      this.mostrarModalCrear = false
      this.mostrarModalEditar = false
      this.modoEdicion = false
      this.usuarioEditando = null
      this.limpiarFormulario()
    },

    limpiarFormulario() {
      this.formularioUsuario = {
        username: '',
        password: '',
        rol: 'user'
      }
    },

    // ==================== ELIMINAR USUARIO ADMIN ====================
    
    confirmarEliminar(usuario) {
      this.usuarioAEliminar = usuario
      this.mostrarModalEliminar = true
    },

    cancelarEliminar() {
      this.mostrarModalEliminar = false
      this.usuarioAEliminar = null
    },

    async eliminarUsuario() {
      if (!this.usuarioAEliminar) return
      
      this.eliminando = true
      
      try {
        await permisosService.eliminarUsuarioAdmin(this.usuarioAEliminar.id)
        
        this.mostrarToast('Usuario administrativo eliminado exitosamente', 'success')
        this.cargarUsuariosAdmin()
        this.cancelarEliminar()
        
      } catch (error) {
        console.error('❌ Error eliminando usuario admin:', error)
        this.mostrarToast(error.message, 'error')
      } finally {
        this.eliminando = false
      }
    },

    // ==================== UTILIDADES ====================
    
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

.permisos-container {
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

/* === USUARIOS LIST === */
.usuarios-list {
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

.header-filters {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-radius: 8px;
  font-size: 14px;
  background: white;
  color: #333;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}

.filter-select:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
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

/* === USUARIOS TABLE === */
.usuarios-table-container {
  overflow-x: auto;
}

.usuarios-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Inter', sans-serif;
}

.usuarios-table th {
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
  color: #2E7D32;
  font-weight: 600;
  font-size: 13px;
  padding: 14px 16px;
  text-align: left;
  border-bottom: 2px solid rgba(76, 175, 80, 0.2);
  white-space: nowrap;
}

.usuarios-table td {
  padding: 16px;
  border-bottom: 1px solid rgba(76, 175, 80, 0.1);
  vertical-align: middle;
}

.usuario-row:hover {
  background: linear-gradient(135deg, #f8fffe 0%, #f0fff4 100%);
}

.name-cell {
  min-width: 250px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 16px;
  flex-shrink: 0;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.user-supervisor {
  font-size: 12px;
  color: #666;
}

.rol-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
}

.rol-badge.admin {
  background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
  color: white;
}

.rol-badge.user {
  background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
  color: white;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-active {
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

.btn-edit {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  color: #1976d2;
}

.btn-edit:hover {
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
  transition: all 0.3s ease;
}

.modal-confirm {
  max-width: 500px;
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
.form-section {
  margin-bottom: 24px;
  padding: 20px;
  background: linear-gradient(135deg, #f8fffe 0%, #f0fff4 100%);
  border-radius: 12px;
  border: 1px solid rgba(76, 175, 80, 0.1);
}

.form-section h4 {
  font-size: 16px;
  font-weight: 600;
  color: #2E7D32;
  margin: 0 0 16px 0;
  font-family: 'Inter', sans-serif;
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid rgba(76, 175, 80, 0.2);
  border-radius: 10px;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.form-help {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
  display: block;
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.radio-option {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  border: 2px solid rgba(76, 175, 80, 0.2);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.radio-option:hover {
  border-color: #4CAF50;
  background: rgba(76, 175, 80, 0.05);
}

.radio-option.selected {
  border-color: #4CAF50;
  background: rgba(76, 175, 80, 0.1);
}

.radio-option input[type="radio"] {
  width: 18px;
  height: 18px;
  accent-color: #4CAF50;
  margin: 0;
  flex-shrink: 0;
}

.radio-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.radio-title {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.radio-description {
  font-size: 12px;
  color: #666;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid rgba(76, 175, 80, 0.1);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid #e8f5e8;
  border-top: 2px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* === CONFIRM MODAL === */
.confirm-content {
  text-align: center;
}

.confirm-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.confirm-content h4 {
  color: #2E7D32;
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 12px 0;
  font-family: 'Inter', sans-serif;
}

.warning-text {
  color: #d32f2f;
  font-weight: 500;
  margin: 16px 0 0 0;
  font-size: 14px;
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

/* === TOAST === */
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  background: white;
  border-radius: 12px;
  padding: 16px 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  z-index: 9999;
  animation: toastSlideIn 0.3s ease-out;
  min-width: 300px;
  max-width: 500px;
}

.toast.success {
  border-left: 4px solid #4CAF50;
}

.toast.error {
  border-left: 4px solid #f44336;
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.toast-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.toast-message {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

@keyframes toastSlideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* === RESPONSIVE DESIGN === */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    max-width: 100vw;
  }
  
  .page-content {
    padding: 16px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: space-between;
  }
  
  .usuarios-table-container {
    overflow-x: scroll;
  }
  
  .modal-content {
    width: 95%;
    max-width: none;
    margin: 0 10px;
  }
}

@media (max-width: 480px) {
  .page-content {
    padding: 12px;
  }
  
  .form-section {
    padding: 16px;
  }
  
  .modal-actions {
    flex-direction: column;
  }
  
  .modal-actions button {
    width: 100%;
  }
}
</style>
