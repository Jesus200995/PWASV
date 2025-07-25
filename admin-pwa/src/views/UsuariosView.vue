<template>
  <div class="usuarios-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Gestión de Usuarios</h1>
              <p class="header-subtitle">Administra todos los usuarios registrados en la aplicación</p>
            </div>
          </div>
          <div class="header-actions">
            <div class="connection-status" :class="{ 'online': isOnline, 'offline': !isOnline }">
              <div class="status-indicator"></div>
              <span class="status-text">{{ isOnline ? 'En línea' : 'Sin conexión' }}</span>
            </div>
            <button @click="cargarUsuarios" class="refresh-btn" :disabled="loading">
              <svg class="refresh-icon" :class="{ spinning: loading }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="23 4 23 10 17 10"></polyline>
                <polyline points="1 20 1 14 7 14"></polyline>
                <path d="m3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
              </svg>
              {{ loading ? 'Cargando...' : 'Actualizar' }}
            </button>
          </div>
        </div>
      </header>

      <div class="page-content">
        <!-- Barra de búsqueda -->        <div class="search-section">
          <div class="search-box">
            <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="m21 21-4.35-4.35"></path>
            </svg>
            <input 
              v-model="searchTerm" 
              type="text" 
              placeholder="Buscar por nombre o correo..." 
              class="search-input"
              @input="filtrarUsuarios"
            >
          </div>
        </div>

        <!-- Tabla de usuarios -->
        <div class="usuarios-section">
          <div v-if="loading && usuarios.length === 0" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando usuarios...</p>
          </div>
          
          <div v-else-if="error" class="error-container">
            <p>{{ error }}</p>
            <button @click="cargarUsuarios" class="retry-btn">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
                <path d="M3 3v5h5"></path>
                <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"></path>
                <path d="M21 21v-5h-5"></path>
              </svg>
              Reintentar
            </button>
          </div>
            <div v-else-if="usuariosFiltrados.length === 0" class="empty-state">
            <div class="empty-icon">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
            </div>
            <h3>No hay usuarios</h3>
            <p v-if="searchTerm">No se encontraron usuarios con el término "{{ searchTerm }}"</p>
            <p v-else>Aún no se han registrado usuarios en la aplicación.</p>
          </div>
          
          <div v-else class="table-container">
            <table class="usuarios-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Correo</th>
                  <th>Nombre Completo</th>
                  <th>Cargo</th>
                  <th>Supervisor</th>
                  <th>Fecha de Registro</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>                <tr v-for="usuario in usuariosFiltrados" :key="usuario.id">
                  <td>#{{ usuario.id }}</td>
                  <td>{{ usuario.correo }}</td>
                  <td>{{ usuario.nombre_completo }}</td>
                  <td>{{ usuario.cargo }}</td>
                  <td>{{ usuario.supervisor }}</td>
                  <td>{{ formatFecha(usuario.created_at || new Date()) }}</td>
                  <td>
                    <span class="status-badge active">
                      Activo
                    </span>
                  </td>
                  <td>
                    <div class="actions-container">
                      <button @click="verDetalles(usuario)" class="btn-ver">
                        Ver Detalles
                      </button>
                      <button @click="confirmarEliminarUsuario(usuario)" class="btn-eliminar" title="Eliminar usuario">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <polyline points="3,6 5,6 21,6"></polyline>
                          <path d="m19,6v14a2,2 0 0,1 -2,2H7a2,2 0 0,1 -2,-2V6m3,0V4a2,2 0 0,1 2,-2h4a2,2 0 0,1 2,2v2"></path>
                          <line x1="10" y1="11" x2="10" y2="17"></line>
                          <line x1="14" y1="11" x2="14" y2="17"></line>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal para detalles - Diseño Moderno Responsivo -->
    <div v-if="showModal" class="modal-overlay-modern" @click="cerrarModal">
      <div class="modal-content-modern" @click.stop>
        <div class="modal-header-modern">
          <div class="modal-title-section">
            <div class="modal-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            </div>
            <h3 class="modal-title">{{ modalTitle }}</h3>
          </div>
          <button @click="cerrarModal" class="btn-close-modern">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        
        <div class="modal-body-modern">
          <div v-if="usuarioSeleccionado" class="user-details-grid">
            <!-- ID Usuario -->
            <div class="detail-card">
              <div class="detail-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                  <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
                </svg>
              </div>
              <div class="detail-content">
                <span class="detail-label">ID Usuario</span>
                <span class="detail-value">#{{ usuarioSeleccionado.id }}</span>
              </div>
            </div>

            <!-- Correo Electrónico -->
            <div class="detail-card">
              <div class="detail-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                  <polyline points="22,6 12,13 2,6"/>
                </svg>
              </div>
              <div class="detail-content">
                <span class="detail-label">Correo</span>
                <span class="detail-value">{{ usuarioSeleccionado.correo }}</span>
              </div>
            </div>

            <!-- Nombre Completo -->
            <div class="detail-card">
              <div class="detail-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </div>
              <div class="detail-content">
                <span class="detail-label">Nombre</span>
                <span class="detail-value">{{ usuarioSeleccionado.nombre_completo || 'No especificado' }}</span>
              </div>
            </div>

            <!-- Cargo -->
            <div class="detail-card">
              <div class="detail-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
                  <line x1="8" y1="21" x2="16" y2="21"/>
                  <line x1="12" y1="17" x2="12" y2="21"/>
                </svg>
              </div>
              <div class="detail-content">
                <span class="detail-label">Cargo</span>
                <span class="detail-value">{{ usuarioSeleccionado.cargo || 'No especificado' }}</span>
              </div>
            </div>

            <!-- Supervisor -->
            <div class="detail-card">
              <div class="detail-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                </svg>
              </div>
              <div class="detail-content">
                <span class="detail-label">Supervisor</span>
                <span class="detail-value">{{ usuarioSeleccionado.supervisor || 'No asignado' }}</span>
              </div>
            </div>

            <!-- CURP -->
            <div class="detail-card">
              <div class="detail-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14,2 14,8 20,8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                  <polyline points="10,9 9,9 8,9"/>
                </svg>
              </div>
              <div class="detail-content">
                <span class="detail-label">CURP</span>
                <span class="detail-value">{{ usuarioSeleccionado.curp || 'No especificada' }}</span>
              </div>
            </div>

            <!-- Estado -->
            <div class="detail-card">
              <div class="detail-icon status-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22,4 12,14.01 9,11.01"/>
                </svg>
              </div>
              <div class="detail-content">
                <span class="detail-label">Estado</span>
                <span class="detail-value status-active">● Activo</span>
              </div>
            </div>

            <!-- Contraseña -->
            <div class="detail-card password-card">
              <div class="detail-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                  <circle cx="12" cy="16" r="1"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
              </div>
              <div class="detail-content password-content">
                <span class="detail-label">Contraseña</span>
                <div class="password-display">
                  <span class="password-value">
                    {{ showPassword ? (usuarioSeleccionado.password || usuarioSeleccionado.contraseña || 'Sin contraseña') : '••••••••••••' }}
                  </span>
                  <button @click="togglePassword" class="password-toggle-btn" type="button">
                    <svg v-if="showPassword" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                      <line x1="1" y1="1" x2="23" y2="23"/>
                    </svg>
                    <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                      <circle cx="12" cy="12" r="3"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de confirmación para eliminar usuario -->
    <div v-if="showDeleteModal" class="modal-overlay-modern" @click="cancelarEliminar">
      <div class="modal-content-modern delete-modal" @click.stop>
        <div class="modal-header-modern delete-header">
          <div class="modal-title-section">
            <div class="modal-icon delete-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 6h18"></path>
                <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                <path d="M8 6V4c0-1 1-2 2-2h4c0-1 1-2 2-2v2"></path>
                <line x1="10" y1="11" x2="10" y2="17"></line>
                <line x1="14" y1="11" x2="14" y2="17"></line>
              </svg>
            </div>
            <h3 class="modal-title">Confirmar Eliminación</h3>
          </div>
          <button @click="cancelarEliminar" class="btn-close-modern">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        
        <div class="modal-body-modern">
          <div v-if="usuarioAEliminar" class="delete-confirmation">
            <div class="warning-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#f44336" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
              </svg>
            </div>
            <h4>¿Estás seguro de que deseas eliminar este usuario?</h4>
            <div class="user-info-delete">
              <p><strong>ID:</strong> #{{ usuarioAEliminar.id }}</p>
              <p><strong>Nombre:</strong> {{ usuarioAEliminar.nombre_completo }}</p>
              <p><strong>Correo:</strong> {{ usuarioAEliminar.correo }}</p>
            </div>
            <p class="warning-text">Esta acción eliminará permanentemente al usuario y todos sus datos asociados. <strong>Esta acción no se puede deshacer.</strong></p>
          </div>
        </div>
        
        <div class="modal-footer-delete">
          <button @click="cancelarEliminar" class="btn-cancel">
            Cancelar
          </button>
          <button @click="eliminarUsuario" class="btn-delete" :disabled="eliminandoUsuario">
            <svg v-if="eliminandoUsuario" class="spinner-small" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 12a9 9 0 11-6.219-8.56"/>
            </svg>
            {{ eliminandoUsuario ? 'Eliminando...' : 'Eliminar Usuario' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Sidebar from '../components/Sidebar.vue'
import { usuariosService } from '../services/usuariosService.js'

const router = useRouter()

// Estado de conexión
const isOnline = ref(navigator.onLine)

const API_URL = 'https://apipwa.sembrandodatos.com'
const usuarios = ref([])
const usuariosFiltrados = ref([])
const loading = ref(false)
const error = ref('')
const searchTerm = ref('')

const showModal = ref(false)
const modalTitle = ref('')
const modalContent = ref('')
const usuarioSeleccionado = ref(null)
const showPassword = ref(false)

// Variables para eliminación de usuarios
const showDeleteModal = ref(false)
const usuarioAEliminar = ref(null)
const eliminandoUsuario = ref(false)

onMounted(() => {
  cargarUsuarios()
  
  // Escuchar cambios de conexión
  window.addEventListener('online', () => {
    isOnline.value = true
  })
  
  window.addEventListener('offline', () => {
    isOnline.value = false
  })
})

const cargarUsuarios = async () => {
  loading.value = true
  error.value = ''
  
  try {
    // Usar el servicio de usuarios con datos reales de la base de datos
    usuarios.value = await usuariosService.obtenerUsuarios()
    usuariosFiltrados.value = usuarios.value
    
    console.log('✅ Usuarios reales cargados desde la base de datos:', usuarios.value)
  } catch (err) {
    console.error('❌ Error al cargar usuarios desde la base de datos:', err)
    error.value = 'Error al conectar con la base de datos. Verifica que el servidor esté funcionando.'
    usuarios.value = []
    usuariosFiltrados.value = []
  } finally {
    loading.value = false
  }
}

const filtrarUsuarios = () => {
  if (!searchTerm.value.trim()) {
    usuariosFiltrados.value = usuarios.value
    return
  }
  
  const termino = searchTerm.value.toLowerCase()
  usuariosFiltrados.value = usuarios.value.filter(usuario => 
    usuario.correo.toLowerCase().includes(termino) ||
    (usuario.nombre_completo && usuario.nombre_completo.toLowerCase().includes(termino)) ||
    (usuario.cargo && usuario.cargo.toLowerCase().includes(termino)) ||
    (usuario.supervisor && usuario.supervisor.toLowerCase().includes(termino))
  )
}

const formatFecha = (fechaStr) => {
  try {
    return new Date(fechaStr).toLocaleDateString('es-ES')
  } catch (e) {
    return fechaStr
  }
}

const verDetalles = (usuario) => {
  modalTitle.value = 'Detalles del Usuario'
  usuarioSeleccionado.value = usuario
  showPassword.value = false // Resetear al cerrar/abrir modal
  
  // Debug para ver qué datos tiene el usuario
  console.log('🔍 Usuario seleccionado para detalles:', usuario)
  console.log('🔑 Contraseña disponible:', usuario.password || usuario.contraseña || 'No encontrada')
  
  showModal.value = true
}

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const cerrarModal = () => {
  showModal.value = false
  usuarioSeleccionado.value = null
  showPassword.value = false
}

const confirmarEliminarUsuario = (usuario) => {
  usuarioAEliminar.value = usuario
  showDeleteModal.value = true
}

const cancelarEliminar = () => {
  showDeleteModal.value = false
  usuarioAEliminar.value = null
  eliminandoUsuario.value = false
}

const eliminarUsuario = async () => {
  if (!usuarioAEliminar.value) return
  
  eliminandoUsuario.value = true
  
  try {
    console.log('🗑️ Eliminando usuario:', usuarioAEliminar.value)
    
    // Llamar al servicio para eliminar el usuario
    await usuariosService.eliminarUsuario(usuarioAEliminar.value.id)
    
    // Eliminar del array local
    const index = usuarios.value.findIndex(u => u.id === usuarioAEliminar.value.id)
    if (index !== -1) {
      usuarios.value.splice(index, 1)
    }
    
    // Actualizar usuarios filtrados
    filtrarUsuarios()
    
    console.log('✅ Usuario eliminado exitosamente')
    
    // Cerrar modal
    cancelarEliminar()
    
  } catch (error) {
    console.error('❌ Error al eliminar usuario:', error)
    // Aquí podrías mostrar un mensaje de error al usuario
    alert('Error al eliminar el usuario. Por favor, inténtalo de nuevo.')
  } finally {
    eliminandoUsuario.value = false
  }
}

const logout = () => {
  // No usar confirm(), el modal se maneja en el Sidebar
  localStorage.removeItem('admin_token')
  localStorage.removeItem('admin_user')
  router.push('/login')
}
</script>

<style scoped>
.usuarios-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
  overflow: hidden;
}

.main-content {
  flex: 1;
  margin-left: clamp(180px, 18vw, 240px);
  width: calc(100vw - clamp(180px, 18vw, 240px));
  background: linear-gradient(135deg, #f8f9fa 0%, #f0fff0 100%);
  min-height: 100vh;
  position: relative;
  box-sizing: border-box;
  overflow-x: hidden;
}

.page-header {
  background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
  border-bottom: none;
  padding: clamp(16px, 4vh, 32px) clamp(16px, 4vw, 32px);
  color: white;
  box-shadow: 0 4px 20px rgba(46, 204, 113, 0.15);
  position: relative;
  overflow: hidden;
  width: 100%;
  box-sizing: border-box;
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
  position: relative;
  z-index: 2;
  flex-wrap: wrap;
  gap: clamp(12px, 3vw, 20px);
  max-width: 100%;
  margin: 0;
  width: 100%;
}

.header-main {
  display: flex;
  align-items: center;
  gap: clamp(12px, 3vw, 20px);
  flex: 1;
  min-width: 200px;
}

.header-icon {
  width: clamp(40px, 6vw, 48px);
  height: clamp(40px, 6vw, 48px);
  background: rgba(255, 255, 255, 0.15);
  border-radius: clamp(8px, 2vw, 12px);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: float 3s ease-in-out infinite;
}

.header-icon svg {
  width: clamp(20px, 3vw, 24px);
  height: clamp(20px, 3vw, 24px);
  color: white;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
}

.header-text {
  flex: 1;
  min-width: 200px;
}

.header-title {
  font-size: clamp(20px, 5vw, 32px);
  font-weight: 700;
  margin: 0 0 clamp(4px, 1vh, 8px) 0;
  background: linear-gradient(45deg, #ffffff 0%, #e8f5e8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  letter-spacing: -0.5px;
  line-height: 1.2;
}

.header-subtitle {
  font-size: clamp(12px, 2.5vw, 16px);
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  font-weight: 400;
  letter-spacing: 0.2px;
  line-height: 1.4;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: clamp(8px, 2vw, 16px);
  flex-wrap: wrap;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: clamp(6px, 1.5vw, 8px);
  padding: clamp(6px, 1.5vw, 8px) clamp(12px, 3vw, 16px);
  border-radius: clamp(16px, 4vw, 20px);
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  font-size: clamp(12px, 2.5vw, 14px);
  font-weight: 500;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.connection-status.online {
  background: rgba(39, 174, 96, 0.2);
  border-color: rgba(39, 174, 96, 0.3);
}

.connection-status.offline {
  background: rgba(231, 76, 60, 0.2);
  border-color: rgba(231, 76, 60, 0.3);
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.connection-status.online .status-indicator {
  background: #27ae60;
  box-shadow: 0 0 8px rgba(39, 174, 96, 0.6);
}

.connection-status.offline .status-indicator {
  background: #e74c3c;
  box-shadow: 0 0 8px rgba(231, 76, 60, 0.6);
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.7; }
  100% { transform: scale(1); opacity: 1; }
}

.status-text {
  color: white;
  font-weight: 500;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: clamp(6px, 1.5vw, 8px);
  padding: clamp(8px, 2vw, 10px) clamp(12px, 3vw, 16px);
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: clamp(8px, 2vw, 10px);
  color: white;
  font-size: clamp(12px, 2.5vw, 14px);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
  white-space: nowrap;
}

.refresh-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.refresh-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
  transition: left 0.6s ease;
}

.refresh-btn::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  transition: all 0.4s ease;
  transform: translate(-50%, -50%);
}

.refresh-btn:hover::before {
  left: 100%;
}

.refresh-btn:hover::after {
  width: 300px;
  height: 300px;
}

.refresh-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #45a049 0%, #5cb85c 50%, #45a049 100%);
  transform: translateY(-3px) scale(1.08);
  box-shadow: 
    0 12px 32px rgba(76, 175, 80, 0.5),
    0 4px 16px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.refresh-btn:active {
  transform: translateY(-1px) scale(1.02);
  transition: all 0.1s ease;
}

.refresh-btn:disabled {
  background: linear-gradient(135deg, #bbb 0%, #ddd 50%, #bbb 100%);
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  color: #888;
}

.refresh-icon {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  filter: drop-shadow(0 1px 2px rgba(0,0,0,0.2));
}

.refresh-icon.spinning {
  animation: spinGlow 1.8s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes spinGlow {
  0% { 
    transform: rotate(0deg) scale(1); 
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.2));
  }
  25% {
    transform: rotate(90deg) scale(1.1); 
    filter: drop-shadow(0 2px 6px rgba(76,175,80,0.4));
  }
  50% { 
    transform: rotate(180deg) scale(1); 
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.2));
  }
  75% {
    transform: rotate(270deg) scale(1.1); 
    filter: drop-shadow(0 2px 6px rgba(76,175,80,0.4));
  }
  100% { 
    transform: rotate(360deg) scale(1); 
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.2));
  }
}

.refresh-icon.spinning {
  animation: spinGlow 1.8s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes spinGlow {
  0% { 
    transform: rotate(0deg) scale(1); 
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.2));
  }
  25% {
    transform: rotate(90deg) scale(1.1);
    filter: drop-shadow(0 2px 4px rgba(255,255,255,0.5));
  }
  50% { 
    transform: rotate(180deg) scale(1.15);
    filter: drop-shadow(0 3px 6px rgba(255,255,255,0.7));
  }
  75% {
    transform: rotate(270deg) scale(1.1);
    filter: drop-shadow(0 2px 4px rgba(255,255,255,0.5));
  }
  100% { 
    transform: rotate(360deg) scale(1); 
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.2));
  }
}

.page-content {
  padding: clamp(16px, 2vw, 24px);
  box-sizing: border-box;
  width: 100%;
  max-width: 100%;
  margin: 0;
}

.search-section {
  margin-bottom: clamp(20px, 5vh, 32px);
  animation: slideInRight 0.6s ease-out;
}

@keyframes slideInRight {
  0% { transform: translateX(30px); opacity: 0; }
  100% { transform: translateX(0); opacity: 1; }
}

.search-box {
  position: relative;
  max-width: clamp(300px, 60vw, 500px);
  width: 100%;
}

.search-input {
  width: 100%;
  padding: clamp(12px, 3vw, 16px) clamp(16px, 4vw, 20px) clamp(12px, 3vw, 16px) clamp(44px, 10vw, 52px);
  border: 2px solid rgba(76, 175, 80, 0.2);
  border-radius: clamp(20px, 5vw, 25px);
  font-size: clamp(14px, 3vw, 16px);
  background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 
    0 4px 16px rgba(76, 175, 80, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  font-weight: 500;
  box-sizing: border-box;
}

.search-input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 
    0 0 0 4px rgba(76, 175, 80, 0.15),
    0 8px 24px rgba(76, 175, 80, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
  background: linear-gradient(135deg, #ffffff 0%, #f0fff0 100%);
  transform: translateY(-2px);
}

.search-input::placeholder {
  color: #999;
  font-weight: 400;
}

.search-icon {
  position: absolute;
  left: clamp(14px, 3vw, 18px);
  top: 50%;
  transform: translateY(-50%);
  color: #4CAF50;
  transition: all 0.3s ease;
}

.search-input:focus + .search-icon {
  color: #45a049;
  transform: translateY(-50%) scale(1.1);
}

.usuarios-section {
  background: linear-gradient(135deg, #ffffff 0%, #fafffe 100%);
  border-radius: clamp(12px, 3vw, 20px);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.08),
    0 2px 16px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255,255,255,0.8);
  overflow: hidden;
  border: 1px solid rgba(76, 175, 80, 0.1);
  transition: all 0.3s ease;
  animation: fadeInUp 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  padding: clamp(16px, 4vw, 24px);
  box-sizing: border-box;
}

@keyframes fadeInUp {
  0% { 
    opacity: 0; 
    transform: translateY(40px) scale(0.9); 
  }
  100% { 
    opacity: 1; 
    transform: translateY(0) scale(1); 
  }
}

.usuarios-section:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 12px 40px rgba(0, 0, 0, 0.12),
    0 4px 20px rgba(0, 0, 0, 0.06),
    inset 0 1px 0 rgba(255,255,255,0.9);
}

.loading-container, .error-container, .empty-state {
  text-align: center;
  padding: clamp(40px, 10vh, 80px) clamp(16px, 4vw, 32px);
  color: #666;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

.spinner-large {
  width: clamp(40px, 8vw, 48px);
  height: clamp(40px, 8vw, 48px);
  border: 4px solid rgba(76, 175, 80, 0.1);
  border-top: 4px solid #4CAF50;
  border-radius: 50%;
  animation: spinLarge 1.2s cubic-bezier(0.55, 0.06, 0.68, 0.19) infinite;
  margin: 0 auto 20px;
  position: relative;
}

.spinner-large::after {
  content: '';
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  border: 4px solid transparent;
  border-top: 4px solid rgba(76, 175, 80, 0.3);
  border-radius: 50%;
  animation: spinLarge 2s linear infinite reverse;
}

@keyframes spinLarge {
  0% { transform: rotate(0deg) scale(1); }
  50% { transform: rotate(180deg) scale(1.1); }
  100% { transform: rotate(360deg) scale(1); }
}

.error-container {
  color: #d63384;
}

.retry-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #d63384 0%, #c2185b 50%, #d63384 100%);
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 50px;
  cursor: pointer;
  margin: 16px auto 0;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 
    0 4px 16px rgba(214, 51, 132, 0.35),
    0 2px 6px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.retry-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
  transition: left 0.5s ease;
}

.retry-btn:hover::before {
  left: 100%;
}

.retry-btn:hover {
  background: linear-gradient(135deg, #c2185b 0%, #ad1457 50%, #c2185b 100%);
  transform: translateY(-2px) scale(1.05);
  box-shadow: 
    0 8px 24px rgba(214, 51, 132, 0.5),
    0 4px 12px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.empty-icon {
  margin-bottom: 24px;
  animation: bounce 2s ease-in-out infinite;
  display: flex;
  justify-content: center;
  align-items: center;
}

.empty-icon svg {
  filter: drop-shadow(0 4px 8px rgba(76, 175, 80, 0.3));
  transition: all 0.3s ease;
}

.empty-state:hover .empty-icon svg {
  transform: scale(1.1) rotate(5deg);
  filter: drop-shadow(0 6px 12px rgba(76, 175, 80, 0.4));
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

.empty-state h3 {
  color: #4CAF50;
  font-size: 24px;
  margin-bottom: 12px;
  font-weight: 600;
}

.empty-state p {
  font-size: 16px;
  color: #888;
}

.table-container {
  overflow: hidden;
  animation: fadeInUp 0.6s ease-out 0.2s both;
  border-radius: clamp(12px, 3vw, 16px);
  background: linear-gradient(135deg, #ffffff 0%, #fafffe 100%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  width: 100%;
  max-width: 100%;
}

.usuarios-table {
  width: 100%;
  max-width: 100%;
  border-collapse: collapse;
  position: relative;
  background: transparent;
  table-layout: fixed;
  overflow: hidden;
}

.usuarios-table th {
  background: linear-gradient(135deg, #f8f9fa 0%, #f0f8f0 100%);
  padding: clamp(8px, 1.5vw, 12px) clamp(4px, 1vw, 8px);
  text-align: center;
  font-weight: 700;
  color: #4CAF50;
  text-transform: uppercase;
  font-size: clamp(8px, 1.5vw, 10px);
  letter-spacing: 0.5px;
  border-bottom: 2px solid rgba(76, 175, 80, 0.2);
  position: sticky;
  top: 0;
  z-index: 10;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.usuarios-table td {
  padding: clamp(6px, 1.2vw, 10px) clamp(3px, 0.8vw, 6px);
  border-bottom: 1px solid rgba(224, 224, 224, 0.6);
  font-size: clamp(9px, 1.8vw, 12px);
  transition: all 0.3s ease;
  color: #444;
  font-weight: 500;
  white-space: nowrap;
  vertical-align: middle;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: center;
}

.usuarios-table td:nth-child(1) { /* ID */
  width: 8%;
  text-align: center;
}

.usuarios-table td:nth-child(2) { /* Correo */
  width: 22%;
  text-align: center;
}

.usuarios-table td:nth-child(3) { /* Nombre */
  width: 18%;
  text-align: center;
}

.usuarios-table td:nth-child(4) { /* Cargo */
  width: 15%;
  text-align: center;
}

.usuarios-table td:nth-child(5) { /* Supervisor */
  width: 15%;
  text-align: center;
}

.usuarios-table td:nth-child(6) { /* Fecha */
  width: 12%;
  text-align: center;
}

.usuarios-table td:nth-child(7) { /* Estado */
  width: 10%;
  text-align: center;
}

.usuarios-table td:nth-child(8) { /* Acciones */
  width: 15%;
  text-align: center;
}

.usuarios-table tbody tr {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
}

.usuarios-table tbody tr:hover {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.05) 0%, rgba(76, 175, 80, 0.02) 100%);
  transform: translateX(4px);
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.1);
}

.usuarios-table tbody tr:hover td {
  border-bottom-color: rgba(76, 175, 80, 0.2);
}

.status-badge {
  padding: clamp(3px, 0.6vw, 5px) clamp(6px, 1.2vw, 8px);
  border-radius: clamp(8px, 2vw, 12px);
  font-size: clamp(7px, 1.4vw, 9px);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  transition: all 0.3s ease;
  display: inline-block;
  position: relative;
  overflow: hidden;
  white-space: nowrap;
  min-width: clamp(35px, 7vw, 50px);
  text-align: center;
  max-width: 100%;
}

.status-badge::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  transition: left 0.5s ease;
}

.status-badge:hover::before {
  left: 100%;
}

.status-badge.active {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  color: #155724;
  border: 1px solid rgba(21, 87, 36, 0.2);
  box-shadow: 0 2px 6px rgba(21, 87, 36, 0.2);
}

.status-badge.active:hover {
  background: linear-gradient(135deg, #c3e6cb 0%, #b1dfbb 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(21, 87, 36, 0.3);
}

.status-badge.inactive {
  background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
  color: #721c24;
  border: 1px solid rgba(114, 28, 36, 0.2);
  box-shadow: 0 2px 6px rgba(114, 28, 36, 0.2);
}

.btn-ver {
  padding: clamp(4px, 0.8vw, 6px) clamp(6px, 1.2vw, 8px);
  background: linear-gradient(135deg, #4CAF50, #43A047);
  color: white;
  border: none;
  border-radius: clamp(8px, 2vw, 12px);
  cursor: pointer;
  font-size: clamp(8px, 1.5vw, 10px);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 2px 6px rgba(76, 175, 80, 0.3);
  position: relative;
  overflow: hidden;
  white-space: nowrap;
  min-width: clamp(50px, 10vw, 70px);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  max-width: 100%;
}

.btn-ver::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
  transition: left 0.5s ease;
}

.btn-ver:hover::before {
  left: 100%;
}

.btn-ver:hover {
  background: linear-gradient(135deg, #43A047, #388E3C);
  transform: translateY(-2px) scale(1.05);
  box-shadow: 
    0 8px 20px rgba(76, 175, 80, 0.5),
    0 4px 12px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.btn-ver:active {
  transform: translateY(-1px) scale(1.02);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
}

/* Estilos para el contenedor de acciones */
.actions-container {
  display: flex;
  gap: 8px;
  align-items: center;
  justify-content: flex-start;
}

/* Estilos para el botón de eliminar */
.btn-eliminar {
  background: linear-gradient(135deg, #f44336, #d32f2f);
  color: white;
  border: none;
  padding: 8px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: 0 2px 6px rgba(244, 67, 54, 0.3);
}

.btn-eliminar:hover {
  background: linear-gradient(135deg, #d32f2f, #b71c1c);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.4);
}

.btn-eliminar:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(244, 67, 54, 0.3);
}

.btn-eliminar svg {
  width: 16px;
  height: 16px;
  stroke-width: 2.5;
}

/* Estilos para el modal de eliminación */
.delete-modal {
  max-width: 500px !important;
}

.delete-header {
  background: linear-gradient(135deg, #ffebee, #fce4ec);
  border-bottom: 2px solid #f44336;
}

.delete-icon {
  background: linear-gradient(135deg, #f44336, #d32f2f);
  color: white;
}

.delete-confirmation {
  text-align: center;
  padding: 20px 0;
}

.warning-icon {
  margin: 0 auto 20px;
  display: flex;
  justify-content: center;
}

.delete-confirmation h4 {
  color: #333;
  margin-bottom: 20px;
  font-size: 18px;
  font-weight: 600;
}

.user-info-delete {
  background: #f9f9f9;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 15px;
  margin: 20px 0;
  text-align: left;
}

.user-info-delete p {
  margin: 5px 0;
  font-size: 14px;
  color: #555;
}

.warning-text {
  color: #f44336;
  font-size: 14px;
  line-height: 1.5;
  margin-top: 15px;
  padding: 10px;
  background: #ffebee;
  border-radius: 6px;
  border-left: 4px solid #f44336;
}

.modal-footer-delete {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding: 20px;
  border-top: 1px solid #e0e0e0;
  background: #f8f9fa;
}

.btn-cancel {
  background: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-cancel:hover {
  background: #5a6268;
  transform: translateY(-1px);
}

.btn-delete {
  background: linear-gradient(135deg, #f44336, #d32f2f);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-delete:hover:not(:disabled) {
  background: linear-gradient(135deg, #d32f2f, #b71c1c);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.3);
}

.btn-delete:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.spinner-small {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Modal Moderno - Diseño Responsivo */
.modal-overlay-modern {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: clamp(12px, 3vw, 20px);
  backdrop-filter: blur(8px);
  animation: fadeIn 0.3s ease-out;
}

.modal-content-modern {
  background: linear-gradient(135deg, #ffffff 0%, #fdfdfd 100%);
  border-radius: clamp(16px, 2.5vw, 24px);
  max-width: clamp(320px, 90vw, 480px);
  max-height: clamp(500px, 85vh, 700px);
  width: 100%;
  overflow: hidden;
  box-shadow: 
    0 25px 80px rgba(0, 0, 0, 0.15),
    0 10px 40px rgba(0, 0, 0, 0.08);
  border: 2px solid rgba(76, 175, 80, 0.08);
  animation: modalSlideUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes modalSlideUp {
  0% { 
    opacity: 0; 
    transform: scale(0.85) translateY(30px); 
  }
  100% { 
    opacity: 1; 
    transform: scale(1) translateY(0); 
  }
}

.modal-header-modern {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: clamp(12px, 3vw, 18px) clamp(16px, 4vw, 24px);
  border-bottom: 2px solid rgba(76, 175, 80, 0.1);
  background: linear-gradient(135deg, 
    rgba(76, 175, 80, 0.05) 0%, 
    rgba(76, 175, 80, 0.02) 100%);
}

.modal-title-section {
  display: flex;
  align-items: center;
  gap: clamp(8px, 2vw, 12px);
}

.modal-icon {
  width: clamp(28px, 6vw, 36px);
  height: clamp(28px, 6vw, 36px);
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.modal-title {
  font-size: clamp(14px, 3.5vw, 18px);
  font-weight: 700;
  color: #2E7D32;
  margin: 0;
  letter-spacing: 0.3px;
}

.btn-close-modern {
  width: clamp(28px, 6vw, 32px);
  height: clamp(28px, 6vw, 32px);
  background: rgba(244, 67, 54, 0.1);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #F44336;
}

.btn-close-modern:hover {
  background: rgba(244, 67, 54, 0.2);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.3);
}

.modal-body-modern {
  padding: clamp(8px, 2vw, 12px) clamp(16px, 4vw, 24px) clamp(16px, 4vw, 24px);
  max-height: calc(85vh - clamp(60px, 12vw, 80px));
  overflow-y: auto;
}

.modal-body-modern::-webkit-scrollbar {
  width: 4px;
}

.modal-body-modern::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 2px;
}

.modal-body-modern::-webkit-scrollbar-thumb {
  background: #4CAF50;
  border-radius: 2px;
}

.user-details-grid {
  display: grid;
  gap: clamp(6px, 1.5vw, 10px);
}

.detail-card {
  background: linear-gradient(135deg, 
    rgba(248, 255, 254, 0.6) 0%, 
    rgba(240, 255, 240, 0.4) 100%);
  border: 1px solid rgba(76, 175, 80, 0.15);
  border-radius: clamp(8px, 2vw, 12px);
  padding: clamp(8px, 2vw, 12px) clamp(10px, 2.5vw, 14px);
  display: flex;
  align-items: flex-start;
  gap: clamp(6px, 1.5vw, 10px);
  transition: all 0.3s ease;
}

.detail-card:hover {
  background: linear-gradient(135deg, 
    rgba(240, 255, 240, 0.8) 0%, 
    rgba(232, 245, 232, 0.6) 100%);
  border-color: rgba(76, 175, 80, 0.25);
  transform: translateX(2px);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.1);
}

.detail-icon {
  width: clamp(24px, 5vw, 28px);
  height: clamp(24px, 5vw, 28px);
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.15), rgba(76, 175, 80, 0.1));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4CAF50;
  flex-shrink: 0;
  margin-top: 2px;
}

.status-icon {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.2), rgba(76, 175, 80, 0.15));
}

.detail-content {
  flex: 1;
  min-width: 0;
}

.detail-label {
  display: block;
  font-size: clamp(9px, 2vw, 11px);
  font-weight: 600;
  color: #4CAF50;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: clamp(2px, 0.5vw, 4px);
}

.detail-value {
  display: block;
  font-size: clamp(11px, 2.5vw, 14px);
  font-weight: 500;
  color: #2E7D32;
  line-height: 1.3;
  word-break: break-word;
}

.status-active {
  color: #4CAF50 !important;
  font-weight: 600;
}

/* Estilos especiales para el campo de contraseña */
.password-card {
  border-color: rgba(255, 87, 34, 0.2);
  background: linear-gradient(135deg, 
    rgba(255, 243, 224, 0.4) 0%, 
    rgba(255, 248, 225, 0.3) 100%);
}

.password-card:hover {
  border-color: rgba(255, 87, 34, 0.3);
  background: linear-gradient(135deg, 
    rgba(255, 243, 224, 0.6) 0%, 
    rgba(255, 248, 225, 0.5) 100%);
}

.password-card .detail-icon {
  background: linear-gradient(135deg, rgba(255, 87, 34, 0.15), rgba(255, 87, 34, 0.1));
  color: #FF5722;
}

.password-content {
  width: 100%;
}

.password-display {
  display: flex;
  align-items: center;
  gap: clamp(6px, 1.5vw, 8px);
  margin-top: clamp(4px, 1vw, 6px);
}

.password-value {
  font-family: 'Courier New', 'Monaco', monospace;
  font-size: clamp(10px, 2.2vw, 12px);
  font-weight: 600;
  color: #FF5722;
  background: rgba(255, 255, 255, 0.8);
  padding: clamp(4px, 1vw, 6px) clamp(6px, 1.5vw, 8px);
  border-radius: clamp(4px, 1vw, 6px);
  border: 1px solid rgba(255, 87, 34, 0.2);
  flex: 1;
  min-width: 0;
  word-break: break-all;
}

.password-toggle-btn {
  width: clamp(22px, 4.5vw, 26px);
  height: clamp(22px, 4.5vw, 26px);
  background: linear-gradient(135deg, #FF5722, #FF7043);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 2px 6px rgba(255, 87, 34, 0.3);
}

.password-toggle-btn:hover {
  background: linear-gradient(135deg, #E64A19, #FF5722);
  transform: scale(1.1);
  box-shadow: 0 3px 9px rgba(255, 87, 34, 0.4);
}

.password-toggle-btn:active {
  transform: scale(1.05);
}

.modal-header h3 {
  margin: 0;
  color: #333;
  font-size: clamp(16px, 4vw, 20px);
  font-weight: 700;
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.btn-close {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 2px solid rgba(76, 175, 80, 0.2);
  font-size: clamp(16px, 4vw, 20px);
  cursor: pointer;
  color: #666;
  padding: clamp(6px, 1.5vw, 8px);
  width: clamp(30px, 8vw, 36px);
  height: clamp(30px, 8vw, 36px);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  font-weight: 700;
}

.btn-close:hover {
  background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
  border-color: #4CAF50;
  color: #4CAF50;
  transform: scale(1.1) rotate(90deg);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2);
}

.modal-body {
  padding: clamp(16px, 4vw, 24px) clamp(20px, 5vw, 28px);
  overflow: auto;
  max-height: calc(80vh - clamp(80px, 20vw, 120px));
}

.usuario-detalles div {
  margin-bottom: 16px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #f8fffe 0%, #f0fff0 100%);
  border-radius: 12px;
  border-left: 4px solid #4CAF50;
  transition: all 0.3s ease;
}

.usuario-detalles div:hover {
  background: linear-gradient(135deg, #f0fff0 0%, #e8f5e8 100%);
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.1);
}

.usuario-detalles div:last-child {
  margin-bottom: 0;
}

.usuario-detalles strong {
  color: #4CAF50;
  font-weight: 700;
  display: block;
  margin-bottom: 4px;
  text-transform: uppercase;
  font-size: 11px;
  letter-spacing: 0.5px;
}

/* Estilos para el campo de contraseña */
.detalle-item {
  margin-bottom: 16px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #f8fffe 0%, #f0fff0 100%);
  border-radius: 12px;
  border-left: 4px solid #4CAF50;
  transition: all 0.3s ease;
}

.detalle-item:hover {
  background: linear-gradient(135deg, #f0fff0 0%, #e8f5e8 100%);
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.1);
}

.detalle-item:last-child {
  margin-bottom: 0;
}

.password-field {
  border-left-color: #FF5722;
}

.password-container {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
}

.password-text {
  font-family: 'Courier New', monospace;
  background: rgba(255, 255, 255, 0.7);
  padding: 8px 12px;
  border-radius: 8px;
  border: 2px solid rgba(76, 175, 80, 0.2);
  font-size: 14px;
  font-weight: 600;
  color: #2E7D32;
  letter-spacing: 1px;
  flex: 1;
  transition: all 0.3s ease;
}

.toggle-password-btn {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  border: none;
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
}

.toggle-password-btn:hover {
  background: linear-gradient(135deg, #43A047, #4CAF50);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
}

.toggle-password-btn:active {
  transform: translateY(0);
  box-shadow: 0 1px 4px rgba(76, 175, 80, 0.3);
}

.estado-activo {
  color: #4CAF50;
  font-weight: 600;
  background: rgba(76, 175, 80, 0.1);
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
}

/* Responsive */
@media (max-width: 1024px) {
  .main-content {
    margin-left: clamp(120px, 12vw, 180px);
    width: calc(100vw - clamp(120px, 12vw, 180px));
  }
  
  .table-container {
    overflow: hidden;
    width: 100%;
  }
  
  .usuarios-table {
    width: 100%;
    max-width: 100%;
    font-size: clamp(8px, 1.6vw, 11px);
  }
  
  .usuarios-table th,
  .usuarios-table td {
    padding: clamp(5px, 1vw, 8px) clamp(2px, 0.6vw, 5px);
    font-size: clamp(8px, 1.6vw, 11px);
    text-align: center;
  }
  
  .btn-ver {
    padding: clamp(3px, 0.6vw, 5px) clamp(4px, 0.8vw, 6px);
    font-size: clamp(7px, 1.2vw, 9px);
    min-width: clamp(40px, 8vw, 60px);
    width: 100%;
    max-width: 100%;
  }
  
  .status-badge {
    padding: clamp(2px, 0.4vw, 4px) clamp(4px, 0.8vw, 6px);
    font-size: clamp(6px, 1.2vw, 8px);
    min-width: clamp(30px, 6vw, 45px);
    width: 100%;
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    width: 100%;
  }
  
  .page-header {
    padding: clamp(12px, 3vw, 20px);
  }
  
  .header-content {
    flex-direction: column;
    gap: clamp(8px, 2vw, 12px);
    align-items: flex-start;
  }
  
  .header-main {
    width: 100%;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .page-content {
    padding: clamp(12px, 3vw, 20px);
  }
  
  .search-box {
    max-width: 100%;
  }
  
  .table-container {
    border-radius: clamp(6px, 1.5vw, 10px);
    overflow: hidden;
    width: 100%;
    max-width: 100%;
  }
  
  .usuarios-table {
    width: 100%;
    max-width: 100%;
    font-size: clamp(7px, 1.4vw, 10px);
    table-layout: fixed;
  }
  
  .usuarios-table th,
  .usuarios-table td {
    padding: clamp(4px, 0.8vw, 6px) clamp(2px, 0.5vw, 4px);
    font-size: clamp(7px, 1.4vw, 10px);
    text-align: center;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .usuarios-table td:nth-child(1) { /* ID */
    width: 6%;
  }
  
  .usuarios-table td:nth-child(2) { /* Correo */
    width: 25%;
  }
  
  .usuarios-table td:nth-child(3) { /* Nombre */
    width: 20%;
  }
  
  .usuarios-table td:nth-child(4) { /* Cargo */
    width: 15%;
  }
  
  .usuarios-table td:nth-child(5) { /* Supervisor */
    width: 12%;
  }
  
  .usuarios-table td:nth-child(6) { /* Fecha */
    width: 10%;
  }
  
  .usuarios-table td:nth-child(7) { /* Estado */
    width: 8%;
  }
  
  .usuarios-table td:nth-child(8) { /* Acciones */
    width: 12%;
  }
  
  .btn-ver {
    padding: clamp(2px, 0.5vw, 4px) clamp(3px, 0.8vw, 5px);
    font-size: clamp(6px, 1.2vw, 8px);
    min-width: auto;
    width: 100%;
    max-width: 100%;
    border-radius: clamp(6px, 1.5vw, 10px);
  }
  
  .status-badge {
    padding: clamp(2px, 0.4vw, 3px) clamp(3px, 0.8vw, 5px);
    font-size: clamp(6px, 1.2vw, 8px);
    min-width: auto;
    width: 100%;
    max-width: 100%;
    border-radius: clamp(6px, 1.5vw, 10px);
  }
  
  .modal-content {
    margin: clamp(5px, 2vw, 10px);
    max-width: calc(100vw - clamp(10px, 4vw, 20px));
  }
}

@media (max-width: 480px) {
  .header-content {
    align-items: center;
    text-align: center;
  }
  
  .header-main {
    flex-direction: column;
    gap: clamp(6px, 1.5vw, 10px);
  }
  
  .table-container {
    border-radius: clamp(4px, 1vw, 8px);
    overflow: hidden;
    width: 100%;
  }
  
  .usuarios-table {
    width: 100%;
    max-width: 100%;
    font-size: clamp(6px, 1.2vw, 9px);
    table-layout: fixed;
  }
  
  .usuarios-table th,
  .usuarios-table td {
    padding: clamp(3px, 0.6vw, 5px) clamp(1px, 0.3vw, 3px);
    font-size: clamp(6px, 1.2vw, 9px);
    text-align: center;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .usuarios-table td:nth-child(1) { /* ID */
    width: 5%;
  }
  
  .usuarios-table td:nth-child(2) { /* Correo */
    width: 28%;
  }
  
  .usuarios-table td:nth-child(3) { /* Nombre */
    width: 22%;
  }
  
  .usuarios-table td:nth-child(4) { /* Cargo */
    width: 13%;
  }
  
  .usuarios-table td:nth-child(5) { /* Supervisor */
    width: 10%;
  }
  
  .usuarios-table td:nth-child(6) { /* Fecha */
    width: 8%;
  }
  
  .usuarios-table td:nth-child(7) { /* Estado */
    width: 6%;
  }
  
  .usuarios-table td:nth-child(8) { /* Acciones */
    width: 8%;
  }
  
  .btn-ver {
    padding: clamp(1px, 0.3vw, 3px) clamp(2px, 0.5vw, 4px);
    font-size: clamp(5px, 1vw, 7px);
    min-width: auto;
    width: 100%;
    max-width: 100%;
    border-radius: clamp(4px, 1vw, 8px);
  }
  
  .status-badge {
    padding: clamp(1px, 0.3vw, 2px) clamp(2px, 0.5vw, 4px);
    font-size: clamp(5px, 1vw, 7px);
    min-width: auto;
    width: 100%;
    max-width: 100%;
    border-radius: clamp(4px, 1vw, 8px);
  }
  
  .modal-content {
    max-width: calc(100vw - 10px);
    margin: 5px;
  }
}

/* Media query específico para dispositivos ultra pequeños */
@media (max-width: 360px) {
  .table-container {
    overflow: hidden;
    width: 100%;
  }
  
  .usuarios-table {
    width: 100%;
    max-width: 100%;
    font-size: clamp(5px, 1vw, 7px);
    table-layout: fixed;
  }
  
  .usuarios-table th,
  .usuarios-table td {
    padding: clamp(2px, 0.4vw, 3px) clamp(1px, 0.2vw, 2px);
    font-size: clamp(5px, 1vw, 7px);
    text-align: center;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .usuarios-table td:nth-child(1) { /* ID */
    width: 4%;
  }
  
  .usuarios-table td:nth-child(2) { /* Correo */
    width: 30%;
  }
  
  .usuarios-table td:nth-child(3) { /* Nombre */
    width: 25%;
  }
  
  .usuarios-table td:nth-child(4) { /* Cargo */
    width: 12%;
  }
  
  .usuarios-table td:nth-child(5) { /* Supervisor */
    width: 9%;
  }
  
  .usuarios-table td:nth-child(6) { /* Fecha */
    width: 7%;
  }
  
  .usuarios-table td:nth-child(7) { /* Estado */
    width: 5%;
  }
  
  .usuarios-table td:nth-child(8) { /* Acciones */
    width: 8%;
  }
  
  .btn-ver {
    padding: 1px 2px;
    font-size: clamp(4px, 0.8vw, 6px);
    min-width: auto;
    width: 100%;
    max-width: 100%;
    border-radius: 3px;
  }
  
  .status-badge {
    padding: 1px;
    font-size: clamp(4px, 0.8vw, 6px);
    min-width: auto;
    width: 100%;
    max-width: 100%;
    border-radius: 3px;
  }
}

/* Responsive para Modal Moderno */
@media (max-width: 768px) {
  .modal-content-modern {
    max-width: 95vw;
    max-height: 90vh;
    margin: clamp(5px, 2vw, 10px);
  }
  
  .modal-header-modern {
    padding: clamp(10px, 2.5vw, 14px) clamp(14px, 3.5vw, 18px);
  }
  
  .modal-title {
    font-size: clamp(12px, 3vw, 16px);
  }
  
  .modal-icon {
    width: clamp(24px, 5vw, 30px);
    height: clamp(24px, 5vw, 30px);
  }
  
  .btn-close-modern {
    width: clamp(24px, 5vw, 28px);
    height: clamp(24px, 5vw, 28px);
  }
  
  .modal-body-modern {
    padding: clamp(6px, 1.5vw, 8px) clamp(14px, 3.5vw, 18px) clamp(14px, 3.5vw, 18px);
  }
  
  .detail-card {
    padding: clamp(6px, 1.5vw, 8px) clamp(8px, 2vw, 10px);
    gap: clamp(4px, 1vw, 6px);
  }
  
  .detail-icon {
    width: clamp(20px, 4vw, 24px);
    height: clamp(20px, 4vw, 24px);
  }
  
  .detail-label {
    font-size: clamp(8px, 1.8vw, 10px);
  }
  
  .detail-value {
    font-size: clamp(10px, 2.2vw, 12px);
  }
  
  .password-value {
    font-size: clamp(9px, 2vw, 11px);
    padding: clamp(3px, 0.8vw, 4px) clamp(4px, 1vw, 6px);
  }
  
  .password-toggle-btn {
    width: clamp(18px, 3.5vw, 22px);
    height: clamp(18px, 3.5vw, 22px);
  }
}

@media (max-width: 480px) {
  .modal-content-modern {
    max-width: 98vw;
    max-height: 95vh;
    border-radius: clamp(12px, 2vw, 16px);
  }
  
  .modal-header-modern {
    padding: clamp(8px, 2vw, 12px) clamp(12px, 3vw, 16px);
  }
  
  .modal-title-section {
    gap: clamp(6px, 1.5vw, 8px);
  }
  
  .modal-title {
    font-size: clamp(11px, 2.8vw, 14px);
  }
  
  .modal-icon {
    width: clamp(20px, 4.5vw, 26px);
    height: clamp(20px, 4.5vw, 26px);
  }
  
  .btn-close-modern {
    width: clamp(20px, 4.5vw, 24px);
    height: clamp(20px, 4.5vw, 24px);
  }
  
  .detail-card {
    padding: clamp(5px, 1.2vw, 7px) clamp(7px, 1.8vw, 9px);
    gap: clamp(3px, 0.8vw, 5px);
    border-radius: clamp(6px, 1.5vw, 8px);
  }
  
  .detail-icon {
    width: clamp(16px, 3.5vw, 20px);
    height: clamp(16px, 3.5vw, 20px);
  }
  
  .detail-label {
    font-size: clamp(7px, 1.6vw, 9px);
    margin-bottom: clamp(1px, 0.3vw, 2px);
  }
  
  .detail-value {
    font-size: clamp(9px, 2vw, 11px);
  }
  
  .password-display {
    gap: clamp(4px, 1vw, 6px);
    margin-top: clamp(2px, 0.5vw, 4px);
  }
  
  .password-value {
    font-size: clamp(8px, 1.8vw, 10px);
    padding: clamp(2px, 0.6vw, 3px) clamp(3px, 0.8vw, 4px);
  }
  
  .password-toggle-btn {
    width: clamp(16px, 3vw, 18px);
    height: clamp(16px, 3vw, 18px);
  }
  
  .password-toggle-btn svg {
    width: clamp(10px, 2.2vw, 12px);
    height: clamp(10px, 2.2vw, 12px);
  }
}
</style>
