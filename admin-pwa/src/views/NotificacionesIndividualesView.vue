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
            <button class="btn-primary" @click="mostrarModalEnviar = true">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 2L11 13"/>
                <path d="M22 2l-7 20-4-9-9-4 20-7z"/>
              </svg>
              Enviar Notificación
            </button>
          </div>
        </div>
      </header>

      <div class="page-content">
        <!-- Mensaje de carga -->
        <div v-if="cargando" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Cargando usuarios...</p>
        </div>

        <!-- Mensaje de error -->
        <div v-if="error && !cargando" class="error-state">
          <div class="error-icon">⚠️</div>
          <h3>Error al cargar datos</h3>
          <p>{{ error }}</p>
          <button class="btn-secondary" @click="cargarUsuarios">Reintentar</button>
        </div>

        <!-- Lista de usuarios -->
        <div v-if="!cargando && !error" class="usuarios-section">
          <div class="section-header">
            <h2>Seleccionar Usuario</h2>
            <div class="search-container">
              <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/>
                <path d="m21 21-4.35-4.35"/>
              </svg>
              <input 
                type="text" 
                v-model="busqueda" 
                placeholder="Buscar por nombre, correo o CURP..."
                class="search-input"
              >
            </div>
          </div>

          <!-- Tabla de usuarios -->
          <div class="usuarios-table-container">
            <table class="usuarios-table">
              <thead>
                <tr>
                  <th>Nombre</th>
                  <th>Correo</th>
                  <th>CURP</th>
                  <th>Cargo</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="usuario in usuariosFiltrados" :key="usuario.id" class="usuario-row">
                  <td class="name-cell">
                    <div class="user-avatar">
                      {{ obtenerIniciales(usuario.nombre_completo) }}
                    </div>
                    <span class="user-name">{{ usuario.nombre_completo }}</span>
                  </td>
                  <td>{{ usuario.correo }}</td>
                  <td>{{ usuario.curp || 'N/A' }}</td>
                  <td>
                    <span class="cargo-badge">{{ usuario.cargo || 'Sin cargo' }}</span>
                  </td>
                  <td>
                    <span :class="['status-badge', usuario.activo ? 'status-active' : 'status-inactive']">
                      {{ usuario.activo ? 'Activo' : 'Inactivo' }}
                    </span>
                  </td>
                  <td>
                    <button 
                      class="btn-enviar" 
                      @click="seleccionarUsuario(usuario)"
                      :disabled="!usuario.activo"
                    >
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M22 2L11 13"/>
                        <path d="M22 2l-7 20-4-9-9-4 20-7z"/>
                      </svg>
                      Enviar
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
            
            <div v-if="usuariosFiltrados.length === 0" class="empty-state">
              <p>No se encontraron usuarios con esos criterios de búsqueda</p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal para enviar notificación -->
    <Teleport to="body">
      <transition name="modal">
        <div v-if="mostrarModalEnviar" class="modal-overlay" @click="cerrarModal">
          <div class="modal-container" @click.stop>
            <div class="modal-header">
              <h3>{{ usuarioSeleccionado ? 'Enviar Notificación Individual' : 'Enviar Notificación' }}</h3>
              <button class="modal-close" @click="cerrarModal">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>

            <div class="modal-body">
              <div v-if="usuarioSeleccionado" class="user-selected">
                <p><strong>Destinatario:</strong> {{ usuarioSeleccionado.nombre_completo }}</p>
                <p><strong>Correo:</strong> {{ usuarioSeleccionado.correo }}</p>
              </div>

              <div class="form-group">
                <label for="titulo">Título de la notificación</label>
                <input 
                  type="text" 
                  id="titulo"
                  v-model="formulario.titulo" 
                  placeholder="Ej: Recuerda completar tu reporte"
                  class="form-input"
                  maxlength="100"
                >
              </div>

              <div class="form-group">
                <label for="mensaje">Mensaje</label>
                <textarea 
                  id="mensaje"
                  v-model="formulario.mensaje" 
                  placeholder="Escribe el mensaje de la notificación..."
                  class="form-textarea"
                  rows="4"
                  maxlength="500"
                ></textarea>
                <small class="char-count">{{ formulario.mensaje.length }}/500</small>
              </div>

              <div v-if="errorEnvio" class="error-message">
                {{ errorEnvio }}
              </div>
            </div>

            <div class="modal-footer">
              <button class="btn-cancel" @click="cerrarModal" :disabled="enviando">
                Cancelar
              </button>
              <button class="btn-send" @click="enviarNotificacion" :disabled="!formularioValido || enviando">
                <span v-if="!enviando">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 2L11 13"/>
                    <path d="M22 2l-7 20-4-9-9-4 20-7z"/>
                  </svg>
                  Enviar Notificación
                </span>
                <span v-else>
                  <div class="spinner-small"></div>
                  Enviando...
                </span>
              </button>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>

    <!-- Modal de éxito -->
    <Teleport to="body">
      <transition name="modal">
        <div v-if="mostrarExito" class="modal-overlay" @click="cerrarModalExito">
          <div class="modal-container success-modal" @click.stop>
            <div class="success-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
            </div>
            <h3>¡Notificación Enviada!</h3>
            <p>La notificación ha sido enviada exitosamente</p>
            <button class="btn-primary" @click="cerrarModalExito">Aceptar</button>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import authService from '../services/authService'
import usuariosService from '../services/usuariosService'
import notificacionesService from '../services/notificacionesService'

export default {
  name: 'NotificacionesIndividualesView',
  components: {
    Sidebar
  },
  setup() {
    const router = useRouter()
    const usuarios = ref([])
    const cargando = ref(false)
    const error = ref(null)
    const busqueda = ref('')
    const mostrarModalEnviar = ref(false)
    const usuarioSeleccionado = ref(null)
    const enviando = ref(false)
    const errorEnvio = ref(null)
    const mostrarExito = ref(false)

    const formulario = ref({
      titulo: '',
      mensaje: ''
    })

    const usuariosFiltrados = computed(() => {
      if (!busqueda.value) return usuarios.value

      const termino = busqueda.value.toLowerCase()
      return usuarios.value.filter(usuario => 
        usuario.nombre_completo?.toLowerCase().includes(termino) ||
        usuario.correo?.toLowerCase().includes(termino) ||
        usuario.curp?.toLowerCase().includes(termino)
      )
    })

    const formularioValido = computed(() => {
      return formulario.value.titulo.trim().length > 0 && 
             formulario.value.mensaje.trim().length > 0
    })

    const cargarUsuarios = async () => {
      cargando.value = true
      error.value = null
      
      try {
        const respuesta = await usuariosService.getUsuarios()
        usuarios.value = respuesta.data || respuesta
      } catch (err) {
        console.error('Error al cargar usuarios:', err)
        error.value = 'No se pudieron cargar los usuarios. Por favor, intenta de nuevo.'
      } finally {
        cargando.value = false
      }
    }

    const seleccionarUsuario = (usuario) => {
      usuarioSeleccionado.value = usuario
      mostrarModalEnviar.value = true
    }

    const cerrarModal = () => {
      mostrarModalEnviar.value = false
      usuarioSeleccionado.value = null
      formulario.value = {
        titulo: '',
        mensaje: ''
      }
      errorEnvio.value = null
    }

    const cerrarModalExito = () => {
      mostrarExito.value = false
      cerrarModal()
    }

    const enviarNotificacion = async () => {
      if (!formularioValido.value) return

      enviando.value = true
      errorEnvio.value = null

      try {
        const datos = {
          titulo: formulario.value.titulo.trim(),
          subtitulo: formulario.value.mensaje.trim(),
          usuario_id: usuarioSeleccionado.value?.id
        }

        await notificacionesService.enviarNotificacion(datos)
        
        mostrarExito.value = true
        enviando.value = false
      } catch (err) {
        console.error('Error al enviar notificación:', err)
        errorEnvio.value = 'No se pudo enviar la notificación. Por favor, intenta de nuevo.'
        enviando.value = false
      }
    }

    const obtenerIniciales = (nombre) => {
      if (!nombre) return '?'
      const palabras = nombre.split(' ')
      if (palabras.length >= 2) {
        return (palabras[0][0] + palabras[1][0]).toUpperCase()
      }
      return nombre.substring(0, 2).toUpperCase()
    }

    const logout = () => {
      authService.logout()
      router.push('/login')
    }

    onMounted(() => {
      cargarUsuarios()
    })

    return {
      usuarios,
      cargando,
      error,
      busqueda,
      usuariosFiltrados,
      mostrarModalEnviar,
      usuarioSeleccionado,
      formulario,
      formularioValido,
      enviando,
      errorEnvio,
      mostrarExito,
      cargarUsuarios,
      seleccionarUsuario,
      cerrarModal,
      cerrarModalExito,
      enviarNotificacion,
      obtenerIniciales,
      logout
    }
  }
}
</script>

<style scoped>
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
  box-shadow: 
    inset 0 -1px 0 rgba(0, 0, 0, 0.1);
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

.btn-primary:active {
  transform: translateY(0);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* Contenido de la página */
.page-content {
  max-width: 1400px;
  margin: 2rem auto;
  padding: 0 2rem;
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
  border-top-color: #22c55e;
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
  background: #22c55e;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: #16a34a;
}

/* Sección de usuarios */
.usuarios-section {
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.section-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #1f2937;
}

.search-container {
  position: relative;
  flex: 1;
  max-width: 400px;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #9ca3af;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #22c55e;
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
}

/* Tabla de usuarios */
.usuarios-table-container {
  overflow-x: auto;
}

.usuarios-table {
  width: 100%;
  border-collapse: collapse;
}

.usuarios-table thead {
  background: #f9fafb;
}

.usuarios-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.usuarios-table tbody tr {
  border-bottom: 1px solid #f3f4f6;
  transition: background-color 0.2s ease;
}

.usuarios-table tbody tr:hover {
  background: #f9fafb;
}

.usuarios-table td {
  padding: 1rem;
  color: #4b5563;
}

.name-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
}

.user-name {
  font-weight: 600;
  color: #1f2937;
}

.cargo-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #e0f2fe;
  color: #0369a1;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
}

.status-active {
  background: #d1fae5;
  color: #065f46;
}

.status-inactive {
  background: #fee2e2;
  color: #991b1b;
}

.btn-enviar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #22c55e;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.875rem;
}

.btn-enviar:hover:not(:disabled) {
  background: #16a34a;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
}

.btn-enviar:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
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

.modal-container {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 600px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  max-height: 90vh;
  overflow-y: auto;
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
}

.modal-close {
  background: none;
  border: none;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.modal-close:hover {
  background: #f3f4f6;
}

.modal-close svg {
  width: 20px;
  height: 20px;
  color: #6b7280;
}

.modal-body {
  padding: 2rem;
}

.user-selected {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.user-selected p {
  margin: 0.5rem 0;
  color: #166534;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #374151;
}

.form-input, .form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.3s ease;
}

.form-input:focus, .form-textarea:focus {
  outline: none;
  border-color: #22c55e;
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
}

.form-textarea {
  resize: vertical;
}

.char-count {
  display: block;
  text-align: right;
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.error-message {
  background: #fee2e2;
  border: 1px solid #fecaca;
  color: #991b1b;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem 2rem;
  border-top: 1px solid #e5e7eb;
}

.btn-cancel {
  padding: 0.75rem 1.5rem;
  background: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-cancel:hover {
  background: #e5e7eb;
}

.btn-send {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #22c55e;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-send:hover:not(:disabled) {
  background: #16a34a;
  transform: translateY(-2px);
}

.btn-send:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Modal de éxito */
.success-modal {
  text-align: center;
  padding: 3rem 2rem;
}

.success-icon {
  width: 80px;
  height: 80px;
  background: #d1fae5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}

.success-icon svg {
  width: 40px;
  height: 40px;
  color: #22c55e;
}

.success-modal h3 {
  margin: 0 0 0.5rem 0;
  color: #1f2937;
  font-size: 1.5rem;
}

.success-modal p {
  margin: 0 0 1.5rem 0;
  color: #6b7280;
}

/* Transiciones del modal */
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container, 
.modal-leave-active .modal-container {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-container, 
.modal-leave-to .modal-container {
  transform: scale(0.95);
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
    margin-left: 0;
    width: 100vw;
  }
  
  .modal-overlay {
    padding: 16px;
    align-items: flex-start;
    padding-top: 40px;
  }
  
  .modal-container {
    width: 100%;
    max-width: 680px;
    max-height: calc(100vh - 80px);
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

  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-container {
    max-width: 100%;
  }

  .modal-overlay {
    padding: 0;
    align-items: stretch;
  }
  
  .modal-container {
    width: 100%;
    max-width: 100%;
    max-height: 100vh;
    border-radius: 0;
    margin: 0;
  }
  
  .modal-body {
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

  .usuarios-table {
    font-size: 11px;
  }

  .usuarios-table th,
  .usuarios-table td {
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

  .usuarios-table-container {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  .usuarios-table {
    min-width: 650px;
    font-size: 10px;
  }
  
  .modal-container {
    width: 100%;
    max-width: 100%;
    height: 100vh;
    max-height: 100vh;
    border-radius: 0;
  }
}
</style>
