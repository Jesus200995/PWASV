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
          <div class="error-icon">⚠️</div>
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
                      <span v-if="manual.enlace_url" class="badge badge-url" title="Enlace externo">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                          <polyline points="15 3 21 3 21 9"/>
                          <line x1="10" y1="14" x2="21" y2="3"/>
                        </svg>
                        URL
                      </span>
                      <span v-if="!manual.archivo_nombre && !manual.imagen_nombre && !manual.enlace_url" class="badge badge-text">
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
        <div class="modal-header">
          <h3>📚 Nuevo Manual</h3>
          <button class="btn-close" @click="cerrarModalCrear">×</button>
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
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14 2 14 8 20 8"/>
                      <line x1="12" y1="18" x2="12" y2="12"/>
                      <line x1="9" y1="15" x2="15" y2="15"/>
                    </svg>
                    <span>Clic para subir PDF</span>
                  </div>
                  <div v-else class="file-selected">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14 2 14 8 20 8"/>
                    </svg>
                    <span>{{ archivoSeleccionado.name }}</span>
                    <button type="button" class="btn-remove-file" @click.stop="removerArchivo">×</button>
                  </div>
                </div>
              </div>

              <!-- Imagen -->
              <div class="form-group">
                <label>Imagen de Portada</label>
                <div class="file-upload-area" @click="$refs.imagenInput.click()">
                  <input
                    ref="imagenInput"
                    type="file"
                    accept="image/*"
                    @change="handleImagenChange"
                    hidden
                  />
                  <div v-if="!imagenSeleccionada" class="upload-placeholder">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
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
          <h3>📖 Detalle del Manual</h3>
          <button class="btn-close" @click="cerrarModalDetalle">×</button>
        </div>
        <div class="modal-body" v-if="manualDetalle">
          <div class="detalle-header">
            <h2>{{ manualDetalle.titulo }}</h2>
            <p v-if="manualDetalle.subtitulo" class="detalle-subtitulo">{{ manualDetalle.subtitulo }}</p>
          </div>
          
          <div v-if="manualDetalle.imagen_nombre" class="detalle-imagen">
            <img :src="getImagenUrl(manualDetalle.id)" alt="Imagen del manual" />
          </div>
          
          <div v-if="manualDetalle.descripcion" class="detalle-descripcion">
            <h4>Descripción</h4>
            <p>{{ manualDetalle.descripcion }}</p>
          </div>
          
          <div class="detalle-meta">
            <div v-if="manualDetalle.archivo_nombre" class="meta-item">
              <strong>Archivo:</strong>
              <a :href="getArchivoUrl(manualDetalle.id)" target="_blank" class="link-archivo">
                📎 {{ manualDetalle.archivo_nombre }}
              </a>
            </div>
            <div v-if="manualDetalle.enlace_url" class="meta-item">
              <strong>Enlace:</strong>
              <a :href="manualDetalle.enlace_url" target="_blank" class="link-externo">
                🔗 {{ manualDetalle.enlace_url }}
              </a>
            </div>
            <div class="meta-item">
              <strong>Destinatarios:</strong>
              <span>{{ manualDetalle.enviado_a_todos ? 'Todos los usuarios' : `${manualDetalle.destinatarios?.length || 0} usuarios específicos` }}</span>
            </div>
            <div class="meta-item">
              <strong>Lecturas:</strong>
              <span>{{ manualDetalle.total_lecturas }} usuarios</span>
            </div>
            <div class="meta-item">
              <strong>Fecha:</strong>
              <span>{{ formatearFecha(manualDetalle.fecha_creacion) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Estadísticas -->
    <div v-if="mostrarModalEstadisticas" class="modal-overlay" @click="cerrarModalEstadisticas">
      <div class="modal-content modal-large" @click.stop>
        <div class="modal-header">
          <h3>📊 Estadísticas de Lectura</h3>
          <button class="btn-close" @click="cerrarModalEstadisticas">×</button>
        </div>
        <div class="modal-body" v-if="estadisticas">
          <div class="stats-header">
            <h2>{{ estadisticas.titulo }}</h2>
            <div class="stats-summary">
              <div class="stat-card">
                <span class="stat-value">{{ estadisticas.total_lecturas }}</span>
                <span class="stat-label">Lecturas</span>
              </div>
              <div class="stat-card">
                <span class="stat-value">{{ estadisticas.total_destinatarios }}</span>
                <span class="stat-label">Destinatarios</span>
              </div>
              <div class="stat-card">
                <span class="stat-value">{{ estadisticas.porcentaje_lectura }}%</span>
                <span class="stat-label">Completado</span>
              </div>
            </div>
          </div>
          
          <div class="stats-lists">
            <div class="stats-column">
              <h4>✅ Usuarios que leyeron ({{ estadisticas.lecturas.length }})</h4>
              <div class="users-list">
                <div v-for="lectura in estadisticas.lecturas" :key="lectura.usuario_id" class="user-item read">
                  <span class="user-name">{{ lectura.nombre || lectura.correo }}</span>
                  <span class="read-date">{{ formatearFecha(lectura.fecha_lectura) }}</span>
                </div>
                <div v-if="estadisticas.lecturas.length === 0" class="no-users">
                  Ningún usuario ha leído este manual aún
                </div>
              </div>
            </div>
            
            <div v-if="!estadisticas.enviado_a_todos" class="stats-column">
              <h4>⏳ Pendientes de leer ({{ estadisticas.no_leidos.length }})</h4>
              <div class="users-list">
                <div v-for="usuario in estadisticas.no_leidos" :key="usuario.usuario_id" class="user-item pending">
                  <span class="user-name">{{ usuario.nombre || usuario.correo }}</span>
                </div>
                <div v-if="estadisticas.no_leidos.length === 0" class="no-users">
                  ¡Todos los usuarios han leído el manual!
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
          <h3>🗑️ Confirmar Eliminación</h3>
          <button class="btn-close" @click="cerrarModalEliminar">×</button>
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
    const mostrarModalDetalle = ref(false)
    const mostrarModalEstadisticas = ref(false)
    const mostrarModalEliminar = ref(false)
    
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
    const enviando = ref(false)
    const eliminando = ref(false)
    const busquedaUsuario = ref('')
    
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
          imagenSeleccionada.value
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
    
    // URLs
    const getArchivoUrl = (id) => manualesService.getArchivoUrl(id)
    const getImagenUrl = (id) => manualesService.getImagenUrl(id)
    
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
      mostrarModalDetalle,
      mostrarModalEstadisticas,
      mostrarModalEliminar,
      manualDetalle,
      estadisticas,
      manualAEliminar,
      formManual,
      archivoSeleccionado,
      imagenSeleccionada,
      imagenPreview,
      enviando,
      eliminando,
      busquedaUsuario,
      puedeCrearManuales,
      puedeEliminar,
      usuariosFiltrados,
      cargarManuales,
      handleArchivoChange,
      handleImagenChange,
      removerArchivo,
      removerImagen,
      crearManual,
      verDetalle,
      verEstadisticas,
      confirmarEliminar,
      eliminarManual,
      getArchivoUrl,
      getImagenUrl,
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
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
}

.main-content {
  flex: 1;
  margin-left: 280px;
  padding: 0;
  min-height: 100vh;
}

/* Header */
.page-header {
  background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
  padding: 24px 32px;
  color: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
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
  gap: 16px;
}

.header-icon {
  width: 56px;
  height: 56px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
}

.header-icon svg {
  width: 32px;
  height: 32px;
  stroke: white;
}

.header-title {
  font-size: 28px;
  font-weight: 700;
  margin: 0;
}

.header-subtitle {
  font-size: 14px;
  opacity: 0.85;
  margin: 4px 0 0;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: white;
  color: #1a73e8;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

/* Content */
.page-content {
  padding: 24px 32px;
  max-width: 1400px;
  margin: 0 auto;
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
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.manuales-table {
  width: 100%;
  border-collapse: collapse;
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
  font-size: 64px;
  margin-bottom: 16px;
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

.modal-small {
  max-width: 450px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
  background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
  color: white;
  border-radius: 20px 20px 0 0;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
}

.modal-header-danger {
  background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
}

.btn-close {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-body {
  padding: 24px;
}

/* Form */
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.form-input, .form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus, .form-textarea:focus {
  outline: none;
  border-color: #1a73e8;
  box-shadow: 0 0 0 3px rgba(26, 115, 232, 0.1);
}

.char-count {
  font-size: 11px;
  color: #9ca3af;
  text-align: right;
  display: block;
  margin-top: 4px;
}

/* File Upload */
.file-upload-area {
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #fafafa;
}

.file-upload-area:hover {
  border-color: #1a73e8;
  background: #f0f7ff;
}

.upload-placeholder {
  color: #6b7280;
}

.upload-placeholder svg {
  margin-bottom: 8px;
  stroke: #9ca3af;
}

.file-selected {
  display: flex;
  align-items: center;
  gap: 12px;
  justify-content: center;
}

.image-preview {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
}

.btn-remove-file {
  background: #fee2e2;
  color: #dc2626;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
}

/* Destinatarios */
.destinatarios-options {
  display: flex;
  gap: 16px;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #374151;
}

/* Usuarios selector */
.usuarios-selector {
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px;
  background: #fafafa;
}

.usuarios-search {
  margin-bottom: 12px;
}

.usuarios-list {
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
}

.usuario-checkbox {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.usuario-checkbox:hover {
  background: #f3f4f6;
}

.usuario-info {
  display: flex;
  flex-direction: column;
}

.usuario-nombre {
  font-weight: 500;
  color: #1f2937;
}

.usuario-correo {
  font-size: 12px;
  color: #6b7280;
}

.usuarios-selected-count {
  margin-top: 12px;
  font-size: 13px;
  color: #1a73e8;
  font-weight: 500;
}

/* Form actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
}

.btn-secondary {
  padding: 12px 24px;
  background: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

.btn-danger {
  padding: 12px 24px;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-danger:hover {
  background: #b91c1c;
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
.detalle-header h2 {
  color: #1e293b;
  margin: 0 0 8px;
}

.detalle-subtitulo {
  color: #64748b;
  font-size: 16px;
}

.detalle-imagen {
  margin: 20px 0;
}

.detalle-imagen img {
  max-width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.detalle-descripcion {
  margin: 20px 0;
  padding: 16px;
  background: #f8fafc;
  border-radius: 12px;
}

.detalle-descripcion h4 {
  margin: 0 0 8px;
  color: #475569;
}

.detalle-meta {
  display: grid;
  gap: 12px;
}

.meta-item {
  display: flex;
  gap: 8px;
}

.meta-item strong {
  color: #64748b;
  min-width: 120px;
}

.link-archivo, .link-externo {
  color: #1a73e8;
  text-decoration: none;
}

.link-archivo:hover, .link-externo:hover {
  text-decoration: underline;
}

/* Estadísticas */
.stats-header {
  margin-bottom: 24px;
}

.stats-summary {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-top: 16px;
}

.stat-card {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  padding: 20px;
  border-radius: 12px;
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 32px;
  font-weight: 700;
  color: #1a73e8;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
}

.stats-lists {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.stats-column h4 {
  margin: 0 0 12px;
  font-size: 14px;
  color: #374151;
}

.users-list {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
}

.user-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #f1f5f9;
}

.user-item.read {
  background: #f0fdf4;
}

.user-item.pending {
  background: #fefce8;
}

.user-name {
  font-weight: 500;
  color: #1f2937;
}

.read-date {
  font-size: 12px;
  color: #6b7280;
}

.no-users {
  padding: 20px;
  text-align: center;
  color: #9ca3af;
  font-style: italic;
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
@media (max-width: 1024px) {
  .main-content {
    margin-left: 0;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .stats-lists {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 16px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .page-content {
    padding: 16px;
  }
  
  .manuales-table {
    font-size: 12px;
  }
  
  .modal-content {
    width: 95%;
    margin: 16px;
  }
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
