<template>
  <div class="visor-container">
    <!-- Importar fuentes modernas -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <Sidebar @logout="logout" />
    
    <main class="main-content">      <header class="page-header">
        <div class="header-content">
          <div class="title-section">
            <div class="title-glass-container">
              <svg class="title-icon" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
              </svg>
              <h1>Visor de Mapa</h1>
            </div>
            <p>Visualiza todas las ubicaciones en tiempo real</p>
          </div>
          <div class="header-actions">
            <button @click="recargarMapa" class="refresh-btn" :disabled="loading">
              <svg class="refresh-icon" :class="{ spinning: loading }" width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/>
              </svg>
              {{ loading ? 'Cargando...' : 'Actualizar' }}
            </button>
          </div>
        </div>
      </header>

      <div class="page-content">        <div class="modern-filter-bar">
          <div class="filter-group">
            <div class="filter-item">
              <svg class="filter-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M3 18h6v-2H3v2zM3 6v2h18V6H3zm0 7h12v-2H3v2z"/>
              </svg>
              <select v-model="filtroTipo" class="modern-select" @change="aplicarFiltros">
                <option value="">Todos los registros</option>
                <option value="critical">Puntos críticos</option>
                <option value="regular">Puntos regulares</option>
              </select>
            </div>
            
            <div class="filter-item">
              <svg class="filter-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M9 11H7v6h2v-6zm4 0h-2v6h2v-6zm4-4v11c0 1.1-.9 2-2 2H7c-1.1 0-2-.9-2-2V7c0-1.1.9-2 2-2h1V3c0-.55.45-1 1-1s1 .45 1 1v2h6V3c0-.55.45-1 1-1s1 .45 1 1v2h1c1.1 0 2 .9 2 2z"/>
              </svg>
              <select v-model="filtroPeriodo" class="modern-select" @change="aplicarFiltros">
                <option value="all">Todo el tiempo</option>
                <option value="today">Hoy</option>
                <option value="week">Esta semana</option>
                <option value="month">Este mes</option>
              </select>            </div>
            
            <div class="filter-item search-item">
              <div class="modern-search-wrapper">
                <svg class="search-input-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
                </svg>
                <input 
                  v-model="busquedaUbicacion" 
                  type="text" 
                  placeholder="Buscar ubicación..." 
                  class="modern-search-input"
                >                <button @click="buscarUbicacion" class="modern-search-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
                  </svg>
                </button>
              </div>
            </div>
            
            <!-- Leyenda de colores al lado del buscador -->
            <div class="filter-legend">
              <div class="legend-item-inline">
                <span class="legend-point-small reciente"></span>
                <span class="legend-text">Hoy</span>
              </div>
              <div class="legend-item-inline">
                <span class="legend-point-small antiguo"></span>
                <span class="legend-text">Anteriores</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Mapa principal -->
        <div class="visor-section">
          <div v-if="loading && !mapInitialized" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando mapa y ubicaciones...</p>
          </div>
          
          <div v-else-if="error" class="error-container">
            <p>{{ error }}</p>
            <button @click="inicializarMapa" class="retry-btn">Reintentar</button>
          </div>          
          <div id="mapa-principal" class="mapa-container"></div>
        </div>
          <!-- Panel lateral de detalles - separado del popup -->
        <div 
          v-if="mostrarPanelDetalles && registroSeleccionado" 
          class="registro-info-panel"
          :class="{ 
            'panel-visible': mostrarPanelDetalles,
            'panel-recent': esUbicacionReciente(registroSeleccionado.fecha_hora),
            'panel-old': !esUbicacionReciente(registroSeleccionado.fecha_hora)
          }"
        >
          <div class="panel-header">
            <div class="panel-title-section">
              <h3>Detalles del Registro</h3>
              <span class="panel-id">#{{ registroSeleccionado.id }}</span>
            </div>
            <button @click="cerrarPanelDetalles" class="close-panel-btn" title="Cerrar panel">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
              </svg>
            </button>
          </div>
          
          <div class="panel-content">
            <!-- Información del usuario -->
            <div class="user-section">
              <div class="user-avatar-large">
                <span class="avatar-text-large">{{ (registroSeleccionado.usuario?.nombre_completo || `Usuario ${registroSeleccionado.usuario_id}`).charAt(0).toUpperCase() }}</span>
              </div>
              <div class="user-info-detail">
                <h4 class="user-name-large">{{ registroSeleccionado.usuario?.nombre_completo || `Usuario ${registroSeleccionado.usuario_id}` }}</h4>
                <p class="user-email-large">{{ registroSeleccionado.usuario?.correo || registroSeleccionado.usuario?.email || 'correo@noregistrado.com' }}</p>
              </div>
            </div>

            <!-- Información del registro -->
            <div class="info-section">
              <h5 class="section-title">Información del Registro</h5>
              
              <div class="info-item-detail">
                <div class="info-icon-wrapper">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M9 11H7v6h2v-6zm4 0h-2v6h2v-6zm4-4v11c0 1.1-.9 2-2 2H7c-1.1 0-2-.9-2-2V7c0-1.1.9-2 2-2h1V3c0-.55.45-1 1-1s1 .45 1 1v2h6V3c0-.55.45-1 1-1s1 .45 1 1v2h1c1.1 0 2 .9 2 2z"/>
                  </svg>
                </div>
                <div class="info-text-wrapper">
                  <span class="info-label">Fecha y hora:</span>
                  <span class="info-value">{{ formatFecha(registroSeleccionado.fecha_hora) }}</span>
                </div>
              </div>

              <div class="info-item-detail">
                <div class="info-icon-wrapper">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                  </svg>
                </div>
                <div class="info-text-wrapper">
                  <span class="info-label">Coordenadas:</span>
                  <span class="info-value">{{ formatCoordenadas(registroSeleccionado.latitud, registroSeleccionado.longitud) }}</span>
                </div>
              </div>

              <div class="info-item-detail">
                <div class="info-icon-wrapper">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                  </svg>
                </div>
                <div class="info-text-wrapper">
                  <span class="info-label">Estado:</span>
                  <span :class="['status-badge-large', esUbicacionReciente(registroSeleccionado.fecha_hora) ? 'recent' : 'old']">
                    {{ esUbicacionReciente(registroSeleccionado.fecha_hora) ? 'Ubicación de hoy' : 'Ubicación anterior' }}
                  </span>
                </div>
              </div>

              <div v-if="registroSeleccionado.descripcion" class="info-item-detail">
                <div class="info-icon-wrapper">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                  </svg>
                </div>
                <div class="info-text-wrapper">
                  <span class="info-label">Descripción:</span>
                  <span class="info-value">{{ registroSeleccionado.descripcion }}</span>
                </div>
              </div>
            </div>

            <!-- Foto del registro -->
            <div v-if="registroSeleccionado.foto_url" class="photo-section">
              <h5 class="section-title">Fotografía del Registro</h5>
              <div class="photo-container">
                <img 
                  :src="`${API_URL}/${registroSeleccionado.foto_url}`" 
                  alt="Foto del registro"
                  @click="verFotoAmpliada(`${API_URL}/${registroSeleccionado.foto_url}`)"
                  class="registro-photo"
                >                <div class="photo-overlay" @click="verFotoAmpliada(`${API_URL}/${registroSeleccionado.foto_url}`)">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                    <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
                  </svg>                </div>                <!-- Mini botón de descarga animado -->
                <button @click.stop="descargarFoto(`${API_URL}/${registroSeleccionado.foto_url}`, `registro_${registroSeleccionado.id}_foto`, $event)" class="download-mini-btn" title="Descargar imagen">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" class="download-icon">
                    <path d="M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z"/>
                  </svg>
                  <div class="download-progress"></div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
      <!-- Modal para detalles completos y foto ampliada -->
    <div v-if="showModal" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop :class="modalType">
        <div class="modal-header">
          <h3>{{ modalTitle }}</h3>
          <button @click="cerrarModal" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <!-- Modal para foto ampliada -->
          <img v-if="modalType === 'photo'" :src="selectedPhotoUrl" alt="Fotografía ampliada" class="full-photo">
          
          <!-- Modal para detalles completos -->
          <div v-if="modalType === 'details'" class="details-modal-content">
            <!-- Información del usuario -->
            <div class="modal-user-section">
              <div class="modal-user-avatar">
                <span class="modal-avatar-text">{{ (registroSeleccionado?.usuario?.nombre_completo || `Usuario ${registroSeleccionado?.usuario_id}`).charAt(0).toUpperCase() }}</span>
              </div>
              <div class="modal-user-info">
                <h4 class="modal-user-name">{{ registroSeleccionado?.usuario?.nombre_completo || `Usuario ${registroSeleccionado?.usuario_id}` }}</h4>
                <p class="modal-user-email">{{ registroSeleccionado?.usuario?.correo || registroSeleccionado?.usuario?.email || 'correo@noregistrado.com' }}</p>
                <span :class="['modal-status-badge', esUbicacionReciente(registroSeleccionado?.fecha_hora) ? 'recent' : 'old']">
                  {{ esUbicacionReciente(registroSeleccionado?.fecha_hora) ? 'Ubicación de hoy' : 'Ubicación anterior' }}
                </span>
              </div>
            </div>

            <!-- Grid de información detallada -->
            <div class="modal-info-grid">
              <div class="modal-info-card">
                <div class="modal-info-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M9 11H7v6h2v-6zm4 0h-2v6h2v-6zm4-4v11c0 1.1-.9 2-2 2H7c-1.1 0-2-.9-2-2V7c0-1.1.9-2 2-2h1V3c0-.55.45-1 1-1s1 .45 1 1v2h6V3c0-.55.45-1 1-1s1 .45 1 1v2h1c1.1 0 2 .9 2 2z"/>
                  </svg>
                </div>
                <div class="modal-info-content">
                  <h5>Fecha y Hora</h5>
                  <p>{{ formatFecha(registroSeleccionado?.fecha_hora) }}</p>
                </div>
              </div>

              <div class="modal-info-card">
                <div class="modal-info-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                  </svg>
                </div>
                <div class="modal-info-content">
                  <h5>Ubicación</h5>
                  <p>{{ formatCoordenadas(registroSeleccionado?.latitud, registroSeleccionado?.longitud) }}</p>
                </div>
              </div>

              <div class="modal-info-card">
                <div class="modal-info-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                  </svg>
                </div>
                <div class="modal-info-content">
                  <h5>ID del Registro</h5>
                  <p>#{{ registroSeleccionado?.id }}</p>
                </div>
              </div>

              <div v-if="registroSeleccionado?.descripcion" class="modal-info-card full-width">
                <div class="modal-info-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                  </svg>
                </div>
                <div class="modal-info-content">
                  <h5>Descripción</h5>
                  <p>{{ registroSeleccionado?.descripcion }}</p>
                </div>
              </div>
            </div>

            <!-- Foto si existe -->
            <div v-if="registroSeleccionado?.foto_url" class="modal-photo-section">
              <h5>Fotografía del Registro</h5>
              <div class="modal-photo-container">
                <img 
                  :src="`${API_URL}/${registroSeleccionado.foto_url}`" 
                  alt="Foto del registro"
                  @click="verFotoAmpliada(`${API_URL}/${registroSeleccionado.foto_url}`)"
                  class="modal-photo"
                >
                <div class="modal-photo-overlay" @click="verFotoAmpliada(`${API_URL}/${registroSeleccionado.foto_url}`)">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="white">
                    <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
                  </svg>
                </div>
              </div>
            </div>

            <!-- Acciones del modal -->
            <div class="modal-actions">
              <button @click="centrarMapa(registroSeleccionado)" class="modal-action-btn primary">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8M3.05,13H1V11H3.05C3.5,6.83 6.83,3.5 11,3.05V1H13V3.05C17.17,3.5 20.5,6.83 20.95,11H23V13H20.95C20.5,17.17 17.17,20.5 13,20.95V23H11V20.95C6.83,20.5 3.5,17.17 3.05,13M12,5A7,7 0 0,0 5,12A7,7 0 0,0 12,19A7,7 0 0,0 19,12A7,7 0 0,0 12,5Z"/>
                </svg>
                Centrar en mapa
              </button>
              <button @click="cerrarModal" class="modal-action-btn secondary">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                </svg>
                Cerrar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Sidebar from '../components/Sidebar.vue'
import { usuariosService } from '../services/usuariosService.js'
import { formatearFechaCDMX } from '../utils/dateUtils.js'

const router = useRouter()

const API_URL = 'https://apipwa.sembrandodatos.com'
const registros = ref([])
const loading = ref(false)
const error = ref('')

// Estado del mapa
const mapInitialized = ref(false)
let map = null
let markers = []
let markersLayer = null

// Filtros y búsqueda
const filtroTipo = ref('')
const filtroPeriodo = ref('all')
const busquedaUbicacion = ref('')

// Registro seleccionado y estado del panel de detalles
const registroSeleccionado = ref(null)
const mostrarPanelDetalles = ref(false)
const popupActivo = ref(null)

// Modal para foto ampliada
const showModal = ref(false)
const modalTitle = ref('')
const modalType = ref('')
const selectedPhotoUrl = ref('')

// Función para formatear fechas
const formatFecha = (fechaStr) => {
  try {
    return formatearFechaCDMX(fechaStr, 'DD/MM/YYYY HH:mm:ss')
  } catch (e) {
    console.error('Error formateando fecha:', e)
    return fechaStr
  }
}

// Formatear coordenadas para mejor visualización
const formatCoordenadas = (lat, lng) => {
  return `${parseFloat(lat).toFixed(6)}, ${parseFloat(lng).toFixed(6)}`
}

// Cargar registros desde la API
const cargarRegistros = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const token = localStorage.getItem('admin_token')
    const response = await axios.get(`${API_URL}/registros`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    // La respuesta puede ser directamente un array o tener una propiedad específica
    const registrosRaw = Array.isArray(response.data) ? response.data : (response.data.registros || [])
    
    // Enriquecer registros con información de usuarios
    const registrosEnriquecidos = await usuariosService.enriquecerRegistrosConUsuarios(registrosRaw)
    
    // Filtrar para mostrar solo la última ubicación de cada usuario
    const ultimasUbicacionesPorUsuario = obtenerUltimasUbicacionesPorUsuario(registrosEnriquecidos)
    
    // Guardar todos los registros para referencia (por si se quiere cambiar el filtro)
    registros.value = registrosEnriquecidos
    
    if (mapInitialized.value) {
      actualizarMarcadores(ultimasUbicacionesPorUsuario)
    } else {
      inicializarMapa(ultimasUbicacionesPorUsuario)
    }
    
  } catch (err) {
    console.error('Error al cargar registros:', err)
    if (err.response?.status === 401) {
      logout()
    } else {
      error.value = 'Error al cargar los registros: ' + (err.response?.data?.detail || err.message)
    }
  } finally {
    loading.value = false
  }
}

// Función para obtener las últimas ubicaciones por usuario
const obtenerUltimasUbicacionesPorUsuario = (registros) => {
  // Agrupar por usuario_id y obtener el más reciente según fecha_hora
  const mapaUsuarios = new Map()
  
  registros.forEach(registro => {
    const usuarioId = registro.usuario_id
    const fechaHora = new Date(registro.fecha_hora)
    
    if (!mapaUsuarios.has(usuarioId) || 
        fechaHora > new Date(mapaUsuarios.get(usuarioId).fecha_hora)) {
      mapaUsuarios.set(usuarioId, registro)
    }
  })
  
  // Convertir el mapa de vuelta a un array
  return Array.from(mapaUsuarios.values())
}

// Inicializar el mapa
const inicializarMapa = (ultimasUbicaciones = null) => {
  if (mapInitialized.value) return
  
  // Asegurarse de que Leaflet está disponible
  if (!window.L) {
    return cargarLeaflet()
  }
  
  const mapContainer = document.getElementById('mapa-principal')
  if (!mapContainer) return
  
  try {
    // Inicializar mapa
    map = window.L.map('mapa-principal').setView([0, 0], 2)
    
    // Agregar capa de mapa base
    window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(map)
    
    // Crear capa para los marcadores
    markersLayer = window.L.layerGroup().addTo(map)
    
    // Agregar controles adicionales
    window.L.control.scale({
      imperial: false,
      position: 'bottomleft'
    }).addTo(map)
    
    // Personalizar íconos de marcadores
    if (ultimasUbicaciones) {
      actualizarMarcadores(ultimasUbicaciones)
    } else {
      // Si no hay ubicaciones pasadas, obtener las últimas
      const ultimasUbicacionesPorUsuario = obtenerUltimasUbicacionesPorUsuario(registros.value)
      actualizarMarcadores(ultimasUbicacionesPorUsuario)
    }
    
    mapInitialized.value = true
    
    // Ajustar vista para mostrar todos los marcadores
    if (markers.length > 0) {
      const group = new window.L.featureGroup(markers)
      map.fitBounds(group.getBounds().pad(0.1))
    } else {
      // Coordenadas por defecto (centrado en algún lugar de interés)
      map.setView([19.4326, -99.1332], 5) // Centrado en México como ejemplo
    }
    
  } catch (error) {
    console.error('Error al inicializar el mapa:', error)
    error.value = 'No se pudo cargar el mapa. Por favor, actualice la página.'
  }
}

// Cargar la biblioteca Leaflet si no está disponible
const cargarLeaflet = () => {
  return new Promise((resolve) => {
    if (window.L) return resolve()
    
    // Cargar Animate.css para mejores animaciones
    const animateLink = document.createElement('link')
    animateLink.rel = 'stylesheet'
    animateLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css'
    document.head.appendChild(animateLink)
    
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
    document.head.appendChild(link)
    
    const script = document.createElement('script')
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
    script.onload = () => {
      console.log('Leaflet y Animate.css cargados exitosamente')
      inicializarMapa()
      resolve()
    }
    document.head.appendChild(script)
  })
}

// Actualizar marcadores en el mapa
const actualizarMarcadores = (ubicacionesAMostrar = null) => {
  if (!map || !markersLayer) return
  
  // Limpiar marcadores existentes
  markersLayer.clearLayers()
  markers = []
  
  // Determinar qué registros mostrar
  let registrosFiltrados
  
  if (ubicacionesAMostrar) {
    // Si se pasan específicamente las ubicaciones a mostrar, usar esas
    registrosFiltrados = ubicacionesAMostrar
  } else {
    // En caso contrario, filtrar los registros según criterios
    // y luego obtener las últimas ubicaciones por usuario
    registrosFiltrados = filtrarRegistros()
    registrosFiltrados = obtenerUltimasUbicacionesPorUsuario(registrosFiltrados)
  }
  
  // Crear nuevos marcadores
  registrosFiltrados.forEach(registro => {
    try {
      const lat = parseFloat(registro.latitud)
      const lng = parseFloat(registro.longitud)
      
      if (isNaN(lat) || isNaN(lng)) return      // Determinar la antigüedad del registro para asignar color
      const fechaRegistro = new Date(registro.fecha_hora)
      const ahora = new Date()
      const diferenciaMilisegundos = ahora - fechaRegistro
      const diferenciaHoras = diferenciaMilisegundos / (1000 * 60 * 60)
      
      // Si es de hoy (menos de 24 horas), verde; si es más antiguo, azul
      const esReciente = diferenciaHoras <= 24
      const iconSize = [32, 32]
        // Crear un HTML simple y moderno para el marcador
      const markerHtml = `
        <div class="location-marker ${esReciente ? 'reciente' : 'antiguo'}">
          <div class="pulse-ring"></div>
        </div>
      `
      
      const customIcon = window.L.divIcon({
        className: 'custom-location-marker',
        html: markerHtml,
        iconSize: iconSize,
        iconAnchor: [iconSize[0] / 2, iconSize[0] / 2],
        popupAnchor: [0, -iconSize[0] / 2 - 5] // Posicionamiento preciso para alineación con marcador
      })

      // Crear marcador y popup con posicionamiento mejorado
      const marker = window.L.marker([lat, lng], { icon: customIcon })        .bindPopup(`
          <div class="modern-marker-popup ${esReciente ? 'recent-popup' : 'old-popup'}">
            <!-- Botón de cerrar personalizado con mejor posicionamiento -->
            <button class="popup-close-btn" data-popup-close="true" title="Cerrar">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z"/>
              </svg>
            </button>
            
            <div class="popup-header">
              <div class="popup-title">
                <span class="popup-id">#${registro.id}</span>
                <h3>Registro de Usuario</h3>
              </div>
              <div class="popup-status">
                <span class="status-badge ${esReciente ? 'recent' : 'old'}">${esReciente ? 'Hoy' : 'Anterior'}</span>
              </div>
            </div>
            
            <div class="popup-content">
              <div class="user-info">
                <div class="user-avatar">
                  <span class="avatar-text">${(registro.usuario?.nombre_completo || `Usuario ${registro.usuario_id}`).charAt(0).toUpperCase()}</span>
                </div>
                <div class="user-details">
                  <div class="user-name">${registro.usuario?.nombre_completo || `Usuario ${registro.usuario_id}`}</div>
                  <div class="user-email">
                    <span class="email-icon">
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.89 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                      </svg>
                    </span>
                    <span class="email-text">${registro.usuario?.correo || registro.usuario?.email || 'correo@noregistrado.com'}</span>
                  </div>
                </div>
              </div>
              
              <div class="popup-info">
                <div class="info-item">
                  <span class="info-icon">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M9 11H7v6h2v-6zm4 0h-2v6h2v-6zm4-4v11c0 1.1-.9 2-2 2H7c-1.1 0-2-.9-2-2V7c0-1.1.9-2 2-2h1V3c0-.55.45-1 1-1s1 .45 1 1v2h6V3c0-.55.45-1 1-1s1 .45 1 1v2h1c1.1 0 2 .9 2 2z"/>
                    </svg>
                  </span>
                  <span class="info-text">${formatFecha(registro.fecha_hora)}</span>
                </div>
                <div class="info-item">
                  <span class="info-icon">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                    </svg>
                  </span>
                  <span class="info-text">Última ubicación conocida</span>
                </div>
              </div>
                <div class="popup-actions">
                <button class="modern-popup-btn popup-detail-btn enhanced-detail-btn" data-registro-id="${registro.id}">
                  <span class="btn-icon">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z"/>
                    </svg>
                  </span>
                  <span class="btn-text">Ver detalles completos</span>
                </button>
              </div>
            </div>
          </div>`, {
          maxWidth: 320,
          minWidth: 300,
          className: `modern-popup-container centered-popup ${esReciente ? 'recent-tip' : 'old-tip'}`,
          offset: [0, -16], // Ajustado para alinear perfectamente con el marcador
          autoPan: true,
          autoPanPadding: [50, 50],
          keepInView: true,
          closeButton: false // Desactivar botón de cerrar por defecto para usar el personalizado
        })
        // Solo guardar referencia del marcador al hacer click (no mostrar panel aún)
      marker.on('click', () => {
        // Centrar el mapa en la ubicación seleccionada
        centrarMapaEnUbicacion(registro)
        
        // Actualizar registro seleccionado pero no mostrar panel aún
        registroSeleccionado.value = registro
        
        // Guardar referencia del popup activo
        popupActivo.value = marker
        
        // Resaltar marcador
        resaltarMarcador(registro)
      })
      
      // Añadir evento al botón "Ver detalles" dentro del popup
      marker.on('popupopen', (e) => {
        setTimeout(() => {
          // Botón "Ver detalles"
          const detailBtn = document.querySelector('.popup-detail-btn')
          if (detailBtn) {
            detailBtn.addEventListener('click', (e) => {
              e.preventDefault()
              e.stopPropagation()
              
              // Mostrar panel de detalles sin cerrar el popup
              mostrarPanelDetalles.value = true
              
              // Añadir clase al body en móvil para prevenir scroll
              if (window.innerWidth <= 1024) {
                document.body.classList.add('panel-open')
              }
              
              // Verificar que el registro seleccionado sea el correcto
              const registroId = detailBtn.getAttribute('data-registro-id')
              if (registroId && registroId !== registro.id.toString()) {
                // Si hay un registro diferente, actualizar
                registroSeleccionado.value = registro
              }
            })
          }
          
          // Botón de cerrar personalizado
          const closeBtn = document.querySelector('.popup-close-btn')
          if (closeBtn) {
            closeBtn.addEventListener('click', (e) => {
              e.preventDefault()
              e.stopPropagation()
              
              // Cerrar el popup
              marker.closePopup()
            })
          }
          
          // Añadir efecto de animación líquida al popup
          const popupWrapper = document.querySelector('.leaflet-popup-content-wrapper')
          if (popupWrapper) {
            popupWrapper.classList.add('liquid-entrance')
          }
        }, 100)
      })
      
      // Manejar el cierre del popup
      marker.on('popupclose', (e) => {
        // Si el popup se cierra, también cerrar el panel de detalles
        if (mostrarPanelDetalles.value) {
          cerrarPanelDetalles()
        }
        // Limpiar resaltado del marcador
        limpiarResaltadoMarcadores()
      })
      
      marker.addTo(markersLayer)
      markers.push(marker)
      
      // Guardar referencia al marcador en el registro para facilidad de uso
      registro.marker = marker
      
    } catch (err) {
      console.error('Error al crear marcador:', err)
    }
  })
  
  // Actualizar vista del mapa si hay marcadores
  if (markers.length > 0) {
    const group = new window.L.featureGroup(markers)
    map.fitBounds(group.getBounds().pad(0.1))
  }
}

// Filtrar registros según los criterios seleccionados
const filtrarRegistros = () => {
  let resultado = [...registros.value]
  
  // Filtrar por tipo
  if (filtroTipo.value === 'critical') {
    // Ejemplo: supongamos que los "críticos" tienen descripción que incluye "crítico" o "urgente"
    resultado = resultado.filter(r => {
      const desc = r.descripcion?.toLowerCase() || ''
      return desc.includes('crítico') || desc.includes('urgente') || Math.random() < 0.3 // Random para demo
    })
  } else if (filtroTipo.value === 'regular') {
    resultado = resultado.filter(r => {
      const desc = r.descripcion?.toLowerCase() || ''
      return !desc.includes('crítico') && !desc.includes('urgente') && Math.random() >= 0.3 // Random para demo
    })
  }
  
  // Filtrar por periodo
  if (filtroPeriodo.value !== 'all') {
    const now = new Date()
    
    if (filtroPeriodo.value === 'today') {
      // Hoy
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
      resultado = resultado.filter(r => new Date(r.fecha_hora) >= today)
    } else if (filtroPeriodo.value === 'week') {
      // Esta semana
      const weekStart = new Date(now)
      weekStart.setDate(now.getDate() - now.getDay())
      weekStart.setHours(0, 0, 0, 0)
      resultado = resultado.filter(r => new Date(r.fecha_hora) >= weekStart)
    } else if (filtroPeriodo.value === 'month') {
      // Este mes
      const monthStart = new Date(now.getFullYear(), now.getMonth(), 1)
      resultado = resultado.filter(r => new Date(r.fecha_hora) >= monthStart)
    }
  }
  
  return resultado
}

// Aplicar filtros y actualizar mapa
const aplicarFiltros = () => {
  // Primero aplicamos los filtros normales
  const registrosFiltrados = filtrarRegistros()
  
  // Luego obtenemos solo la última ubicación de cada usuario
  const ultimasUbicaciones = obtenerUltimasUbicacionesPorUsuario(registrosFiltrados)
  
  // Actualizamos los marcadores con estas ubicaciones filtradas
  actualizarMarcadores(ultimasUbicaciones)
}

// Buscar ubicación por dirección o coordenadas
const buscarUbicacion = async () => {
  if (!busquedaUbicacion.value || !map) return
  
  const searchTerm = busquedaUbicacion.value.trim()
  
  // Verificar si son coordenadas
  const coordsRegex = /^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$/
  
  if (coordsRegex.test(searchTerm)) {
    // Es coordenadas directamente
    const [lat, lng] = searchTerm.split(',').map(coord => parseFloat(coord.trim()))
    map.setView([lat, lng], 15)
    window.L.marker([lat, lng])
      .addTo(map)
      .bindPopup(`<b>Ubicación buscada</b><br>Lat: ${lat}, Lng: ${lng}`)
      .openPopup()
  } else {
    // Usar servicio de geocodificación (Nominatim)
    try {
      const response = await axios.get(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchTerm)}`)
      
      if (response.data && response.data.length > 0) {
        const result = response.data[0]
        const lat = parseFloat(result.lat)
        const lng = parseFloat(result.lon)
        
        map.setView([lat, lng], 15)
        window.L.marker([lat, lng])
          .addTo(map)
          .bindPopup(`<b>${result.display_name}</b>`)
          .openPopup()
      } else {
        alert('No se encontraron resultados para esa ubicación')
      }
    } catch (err) {
      console.error('Error al buscar ubicación:', err)
      alert('Error al buscar la ubicación')
    }
  }
}

// Centrar mapa en una ubicación específica (función separada)
const centrarMapaEnUbicacion = (registro) => {
  if (!map) return
  
  const lat = parseFloat(registro.latitud)
  const lng = parseFloat(registro.longitud)
  
  if (!isNaN(lat) && !isNaN(lng)) {
    // Centrar el mapa en la ubicación con animación suave
    map.flyTo([lat, lng], Math.max(map.getZoom(), 15), {
      animate: true,
      duration: 1.2,
      easeLinearity: 0.15
    })
  }
}

// Resaltar marcador seleccionado
const resaltarMarcador = (registro) => {
  if (!map || !markers.length) return
  
  // Limpiar resaltados previos
  limpiarResaltadoMarcadores()
  
  // Encontrar y resaltar el marcador correspondiente
  markers.forEach(m => {
    const markerElement = m.getElement()
    if (markerElement && m === registro.marker) {
      const marker = markerElement.querySelector('.location-marker')
      if (marker) {
        marker.classList.add('selected', 'pulse-selected')
        
        // Quitar animación temporal después de 2 segundos
        setTimeout(() => {
          marker.classList.remove('pulse-selected')
        }, 2000)
      }
    }
  })
}

// Limpiar resaltado de todos los marcadores
const limpiarResaltadoMarcadores = () => {
  if (!map || !markers.length) return
  
  markers.forEach(m => {
    const markerElement = m.getElement()
    if (markerElement) {
      const marker = markerElement.querySelector('.location-marker')
      if (marker) {
        marker.classList.remove('selected', 'pulse-selected')
        marker.classList.add('marker-unselected')
        setTimeout(() => {
          marker.classList.remove('marker-unselected')
        }, 500)
      }
    }
  })
}

// Cerrar panel de detalles (función separada)
const cerrarPanelDetalles = () => {
  mostrarPanelDetalles.value = false
  
  // Remover clase del body en móvil
  if (window.innerWidth <= 1024) {
    document.body.classList.remove('panel-open')
  }
  
  // Limpiar resaltado de marcadores
  limpiarResaltadoMarcadores()
  
  // Opcional: recentrar el mapa para mostrar todos los marcadores
  if (map && markers.length > 0) {
    const group = new window.L.featureGroup(markers)
    map.fitBounds(group.getBounds().pad(0.1), {
      animate: true,
      duration: 1,
      easeLinearity: 0.2
    })
  }
}

// Mostrar detalles de un registro - función simplificada
const mostrarDetallesRegistro = (registro) => {
  registroSeleccionado.value = registro
  centrarMapaEnUbicacion(registro)
  resaltarMarcador(registro)
}

// Cerrar panel de detalles con animaciones mejoradas - función legacy para compatibilidad
const cerrarDetalles = () => {
  cerrarPanelDetalles()
}

// Centrar mapa en un registro específico con mejor posicionamiento
const centrarMapa = (registro) => {
  if (!map) return
  
  const lat = parseFloat(registro.latitud)
  const lng = parseFloat(registro.longitud)
  
  if (!isNaN(lat) && !isNaN(lng)) {
    let targetLat = lat
    let targetLng = lng
    
    // Si el panel de detalles está abierto en desktop, ajustar el centrado
    if (mostrarPanelDetalles.value && window.innerWidth > 1024) {
      const mapContainer = map.getContainer()
      const mapBounds = mapContainer.getBoundingClientRect()
      const panelWidth = 380 // Ancho del panel de detalles
      
      // Centrar en el área visible disponible (descontando el panel)
      const availableWidth = mapBounds.width - panelWidth - 40 // 40px de margen
      const centerOffset = (availableWidth / 2) - (mapBounds.width / 2)
      
      // Convertir offset a coordenadas geográficas
      const targetPoint = map.latLngToContainerPoint([lat, lng])
      const offsetPoint = window.L.point(targetPoint.x + centerOffset, targetPoint.y)
      const newCenter = map.containerPointToLatLng(offsetPoint)
      
      targetLat = newCenter.lat
      targetLng = newCenter.lng
    }
    
    map.flyTo([targetLat, targetLng], Math.max(map.getZoom(), 16), {
      animate: true,
      duration: 1.5,
      easeLinearity: 0.1
    })
    
    // Si hay un marcador asociado, abrir su popup después de la animación
    if (registro.marker) {
      setTimeout(() => {
        // Añadir animación especial al marcador
        const markerElement = registro.marker.getElement()
        if (markerElement) {
          const marker = markerElement.querySelector('.location-marker')
          if (marker) {
            marker.classList.add('marker-focus-bounce')
            setTimeout(() => {
              marker.classList.remove('marker-focus-bounce')
            }, 1000)
          }
        }
        registro.marker.openPopup()
      }, 800)
    }
  }
}

// Ver registro completo en la página de registros
const verRegistroCompleto = (registro) => {
  // Guardar ID del registro en localStorage para recuperarlo en la página de registros
  localStorage.setItem('selected_registro_id', registro.id)
  router.push('/registros')
}

// Ver detalles completos en modal
const verDetallesCompletos = (registro) => {
  registroSeleccionado.value = registro
  modalTitle.value = `Detalles del Registro #${registro.id}`
  modalType.value = 'details'
  showModal.value = true
}

// Ver foto ampliada en modal
const verFotoAmpliada = (fotoUrl) => {
  selectedPhotoUrl.value = fotoUrl
  modalTitle.value = 'Fotografía del Registro'
  modalType.value = 'photo'
  showModal.value = true
}

// Descargar foto
const descargarFoto = async (fotoUrl, nombreArchivo, evento = null) => {
  try {
    console.log('Iniciando descarga de:', fotoUrl)
    
    // Mostrar animación de carga en el botón
    const button = evento?.target?.closest('.download-mini-btn')
    if (button) {
      button.style.pointerEvents = 'none'
      button.querySelector('.download-progress')?.classList.add('downloading')
    }

    // Obtener el token de autenticación
    const token = localStorage.getItem('admin_token')
    
    // Configurar headers para la petición
    const headers = {
      'Accept': 'image/*'
    }
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    
    const response = await fetch(fotoUrl, {
      method: 'GET',
      headers: headers
    })
    
    if (!response.ok) {
      throw new Error(`Error HTTP: ${response.status}`)
    }
    
    const blob = await response.blob()
    
    // Detectar el tipo de imagen
    const contentType = blob.type || 'image/jpeg'
    let extension = 'jpg'
    
    if (contentType.includes('png')) extension = 'png'
    else if (contentType.includes('gif')) extension = 'gif'
    else if (contentType.includes('webp')) extension = 'webp'
    else if (contentType.includes('jpeg') || contentType.includes('jpg')) extension = 'jpg'
    
    // Crear un enlace temporal para forzar la descarga
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.style.display = 'none'
    link.href = url
    link.download = `${nombreArchivo}.${extension}`
    
    // Forzar el atributo download para asegurar la descarga
    link.setAttribute('download', `${nombreArchivo}.${extension}`)
    
    // Agregar al DOM, hacer clic para descargar y remover
    document.body.appendChild(link)
    link.click()
    
    // Limpiar recursos después de un breve delay
    setTimeout(() => {
      if (document.body.contains(link)) {
        document.body.removeChild(link)
      }
      window.URL.revokeObjectURL(url)
      
      // Restaurar el botón
      if (button) {
        button.style.pointerEvents = 'auto'
        button.querySelector('.download-progress')?.classList.remove('downloading')
      }
    }, 100)
    
    console.log(`Imagen descargada exitosamente: ${nombreArchivo}.${extension}`)
    
  } catch (error) {
    console.error('Error al descargar la foto:', error)
    
    // Restaurar el botón en caso de error
    const button = evento?.target?.closest('.download-mini-btn')
    if (button) {
      button.style.pointerEvents = 'auto'
      button.querySelector('.download-progress')?.classList.remove('downloading')
    }
    
    // Método alternativo: abrir en nueva pestaña
    try {
      const link = document.createElement('a')
      link.href = fotoUrl
      link.target = '_blank'
      link.download = `${nombreArchivo}.jpg`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      console.log('Descarga iniciada usando método alternativo')
    } catch (fallbackError) {
      console.error('Error en método alternativo:', fallbackError)
      alert('No se pudo descargar la imagen. Haz clic derecho en la imagen y selecciona "Guardar imagen como..."')
    }
  }
}

// Cerrar modal
const cerrarModal = () => {
  showModal.value = false
}

// Recargar mapa y datos
const recargarMapa = () => {
  cargarRegistros()
}

// Logout
const logout = () => {
  localStorage.removeItem('admin_token')
  localStorage.removeItem('admin_user')
  router.push('/login')
}

// Función para determinar si una ubicación es reciente (dentro de las últimas 24 horas)
const esUbicacionReciente = (fechaStr) => {
  try {
    const fechaRegistro = new Date(fechaStr)
    const ahora = new Date()
    const diferenciaMilisegundos = ahora - fechaRegistro
    const diferenciaHoras = diferenciaMilisegundos / (1000 * 60 * 60)
    return diferenciaHoras <= 24
  } catch (e) {
    return false
  }
}

// Manejar tecla Escape para cerrar panel
const manejarTeclaEscape = (event) => {
  if (event.key === 'Escape') {
    if (mostrarPanelDetalles.value) {
      cerrarPanelDetalles()
    }
    if (popupActivo.value) {
      popupActivo.value.closePopup()
    }
  }
}

// Ciclo de vida
onMounted(() => {
  // Cargar registros y después inicializar el mapa
  cargarRegistros()
  
  // Agregar listener para tecla Escape
  document.addEventListener('keydown', manejarTeclaEscape)
})

onUnmounted(() => {
  // Limpiar mapa al salir
  if (map) {
    map.remove()
    map = null
  }
  
  // Remover listener de tecla Escape
  document.removeEventListener('keydown', manejarTeclaEscape)
  
  // Limpiar clase del body
  document.body.classList.remove('panel-open')
})

// Vigilar cambios en los filtros
watch([filtroTipo, filtroPeriodo], () => {
  if (mapInitialized.value) {
    aplicarFiltros()
  }
})
</script>

<style scoped>
/* Importación de fuentes */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');

/* Estilos principales */
.visor-container {
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, #f0f2f5 0%, #e8f5e8 100%);
  font-family: 'Inter', 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  overflow: hidden;
}

.main-content {
  flex: 1;
  margin-left: 280px;
  background: transparent;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Header con efecto liquid glass */
.page-header {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 16px 32px;
  box-shadow: 0 4px 32px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(76, 175, 80, 0.1), 
    transparent
  );
  animation: headerGlassShine 6s ease-in-out infinite;
}

@keyframes headerGlassShine {
  0% { left: -100%; }
  50% { left: 100%; }
  100% { left: 100%; }
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 2;
}

.title-section {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.title-glass-container {
  display: flex;
  align-items: center;
  gap: 12px;
  animation: titleFadeIn 1s ease-out;
}

@keyframes titleFadeIn {
  0% {
    opacity: 0;
    transform: translateY(-20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.title-icon {
  color: #4CAF50;
  filter: drop-shadow(0 2px 4px rgba(76, 175, 80, 0.3));
  animation: iconFloat 3s ease-in-out infinite;
}

@keyframes iconFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

.title-glass-container h1 {
  font-family: 'Poppins', sans-serif;
  font-size: 28px;
  font-weight: 600;
  background: linear-gradient(135deg, #2c3e50 0%, #4CAF50 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.title-section p {
  color: #666;
  font-size: 14px;
  margin: 0;
  font-weight: 400;
  opacity: 0.8;
}

.header-actions {
  display: flex;
  align-items: center;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 500;
  font-size: 14px;
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.3);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.refresh-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.6s;
}

.refresh-btn:hover::before {
  left: 100%;
}

.refresh-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(76, 175, 80, 0.4);
}

.refresh-btn:active {
  transform: translateY(0);
}

.refresh-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.refresh-icon {
  transition: transform 0.3s ease;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Contenido principal */
.page-content {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow: hidden;
}

/* Barra de filtros moderna */
.modern-filter-bar {
  animation: filterBarSlideIn 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes filterBarSlideIn {
  0% {
    opacity: 0;
    transform: translateX(-30px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 16px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 12px 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
  width: fit-content;
}

.filter-group::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(76, 175, 80, 0.3), transparent);
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
}

.filter-icon {
  color: #4CAF50;
  opacity: 0.8;
  transition: all 0.3s ease;
}

.filter-item:hover .filter-icon {
  opacity: 1;
  transform: scale(1.1);
}

.modern-select {
  background: transparent;
  border: none;
  color: #2c3e50;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
  outline: none;
  min-width: 140px;
}

.modern-select:hover {
  background: rgba(76, 175, 80, 0.05);
}

.modern-select:focus {
  background: rgba(76, 175, 80, 0.08);
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

/* Leyenda integrada en los filtros - ubicada al lado del buscador */
.filter-legend {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 12px;
  background: rgba(76, 175, 80, 0.05);
  border-radius: 10px;
  border: 1px solid rgba(76, 175, 80, 0.15);
  margin-left: 12px; /* Espacio entre el buscador y la leyenda */
}

.legend-item-inline {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
  color: #2c3e50;
}

.legend-point-small {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.2);
  flex-shrink: 0;
}

.legend-point-small.reciente {
  background: #4CAF50; /* Verde para ubicaciones del día de hoy */
}

.legend-point-small.antiguo {
  background: #FF9800; /* Naranja para ubicaciones de días anteriores */
}

.legend-text {
  font-size: 12px;
  font-weight: 500;
  color: #555;
  white-space: nowrap;
}

.modern-search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(76, 175, 80, 0.2);
  border-radius: 12px;
  padding: 4px;
  transition: all 0.3s ease;
  min-width: 280px;
}

.modern-search-wrapper:focus-within {
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
  background: rgba(255, 255, 255, 0.95);
}

.search-input-icon {
  color: #4CAF50;
  margin-left: 12px;
  opacity: 0.7;
}

.modern-search-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 10px 12px;
  font-size: 14px;
  color: #2c3e50;
  outline: none;
  font-weight: 400;
}

.modern-search-input::placeholder {
  color: #999;
  font-weight: 400;
}

.modern-search-btn {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  border: none;
  border-radius: 8px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
}

.modern-search-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.4);
}

.modern-search-btn:active {
  transform: scale(0.95);
}

/* Mapa principal */
.visor-section {
  position: relative;
  flex: 1;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.loading-container, .error-container {
  padding: 60px 20px;
  text-align: center;
  background: white;
  border-radius: 12px;
}

.spinner-large {
  width: 40px;
  height: 40px;
  border: 4px solid #e0e0e0;
  border-top: 4px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite, pulse 2s ease-in-out infinite;
  margin: 0 auto 20px;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.retry-btn {
  padding: 12px 20px;
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
}

.retry-btn:active {
  transform: translateY(0);
}

.mapa-container {
  flex: 1;
  width: 100%;
  min-height: 400px;
  z-index: 10;
  position: relative;
  pointer-events: auto; /* Asegurar que el mapa siempre sea navegable */
}

/* Asegurar navegabilidad del mapa en todas las condiciones */
:global(.leaflet-container) {
  pointer-events: auto !important;
}

:global(.leaflet-control-zoom) {
  pointer-events: auto !important;
  z-index: 1000 !important;
}

:global(.leaflet-control-attribution) {
  pointer-events: auto !important;
  z-index: 1000 !important;
}

/* Leyenda del mapa - REMOVIDA: Ahora está integrada en los filtros */
/* 
.map-legend {
  position: absolute;
  bottom: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.9);
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  z-index: 500;
  max-width: 200px;
}

.map-legend h3 {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #2c3e50;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 12px;
}

.legend-point {
  display: inline-block;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.2);
}

.legend-point.reciente {
  background: #4CAF50;
}

.legend-point.antiguo {
  background: #FF9800;
}
*/

/* Panel de información del registro seleccionado - Versión mejorada */
.registro-info-panel {
  position: fixed;
  top: 90px;
  right: -320px; /* Reducido de -400px */
  width: 300px; /* Reducido de 380px */
  max-width: calc(100% - 40px);
  max-height: calc(100vh - 110px);
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  z-index: 1100; /* Reducido para no interferir con el mapa */
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  border: 1px solid rgba(0, 0, 0, 0.1);
  pointer-events: auto; /* Asegurar que solo el panel capture eventos */
}

.registro-info-panel.panel-visible {
  right: 20px;
  animation: slideInFromRight 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* Bordes superiores con colores según la leyenda */
.registro-info-panel.panel-recent {
  border-top: 4px solid #4CAF50;
}

.registro-info-panel.panel-old {
  border-top: 4px solid #FF9800;
}

@keyframes slideInFromRight {
  0% {
    transform: translateX(100%) scale(0.95);
    opacity: 0;
    filter: blur(5px);
  }
  40% {
    transform: translateX(-10px) scale(1.02);
    opacity: 0.8;
    filter: blur(2px);
  }
  100% {
    transform: translateX(0) scale(1);
    opacity: 1;
    filter: blur(0);
  }
}

.panel-header {
  padding: 10px 14px; /* Reducido de 16px 20px */
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 5;
}

.panel-old .panel-header {
  background: linear-gradient(135deg, #FF9800 0%, #f57c00 100%);
}

.panel-title-section {
  flex: 1;
}

.panel-title-section h3 {
  margin: 0 0 2px 0; /* Reducido de 4px */
  font-size: 14px; /* Reducido de 18px */
  font-weight: 700;
}

.panel-id {
  font-size: 10px; /* Reducido de 12px */
  opacity: 0.9;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.close-panel-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 26px; /* Reducido de 32px */
  height: 26px; /* Reducido de 32px */
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  backdrop-filter: blur(10px);
}

.close-panel-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.panel-content {
  padding: 0;
  max-height: calc(100vh - 160px); /* Ajustado para el header más pequeño */
  overflow-y: auto;
  padding-bottom: 20px; /* Más espacio en la parte inferior */
}

/* Sección de usuario */
.user-section {
  padding: 12px; /* Reducido de 20px */
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
  display: flex;
  align-items: center;
  gap: 10px; /* Reducido de 16px */
}

.user-avatar-large {
  width: 40px; /* Reducido de 60px */
  height: 40px; /* Reducido de 60px */
  border-radius: 50%;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid white; /* Reducido de 3px */
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); /* Reducido */
}

.panel-old .user-avatar-large {
  background: linear-gradient(135deg, #FF9800 0%, #f57c00 100%);
}

.avatar-text-large {
  font-size: 16px; /* Reducido de 24px */
  font-weight: 800;
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.user-info-detail {
  flex: 1;
  min-width: 0;
}

.user-name-large {
  margin: 0 0 4px 0; /* Reducido de 8px */
  font-size: 14px; /* Reducido de 18px */
  font-weight: 700;
  color: #2c3e50;
}

.user-email-large {
  margin: 0;
  font-size: 11px; /* Reducido de 14px */
  color: #6c757d;
  word-break: break-word;
}

/* Sección de información */
.info-section {
  padding: 16px; /* Mejor padding uniforme */
  margin-top: 4px; /* Pequeño espacio superior */
  margin-bottom: 12px; /* Más espacio entre secciones */
}

.section-title {
  margin: 0 0 10px 0; /* Reducido de 16px */
  font-size: 13px; /* Reducido de 16px */
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 1px solid #e9ecef; /* Reducido de 2px */
  padding-bottom: 4px; /* Reducido de 8px */
}

.info-item-detail {
  display: flex;
  align-items: flex-start;
  gap: 8px; /* Reducido de 12px */
  margin-bottom: 10px; /* Reducido de 16px */
  padding: 8px; /* Reducido de 12px */
  background: #f8f9fa;
  border-radius: 6px; /* Reducido de 8px */
  border-left: 2px solid #4CAF50; /* Reducido de 3px */
}

.panel-old .info-item-detail {
  border-left-color: #FF9800;
}

.info-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 18px; /* Reducido de 24px */
  height: 18px; /* Reducido de 24px */
  background: #4CAF50;
  border-radius: 50%;
  color: white;
  flex-shrink: 0;
}

.panel-old .info-icon-wrapper {
  background: #FF9800;
}

.info-text-wrapper {
  flex: 1;
  min-width: 0;
}

.info-label {
  display: block;
  font-size: 10px; /* Reducido de 12px */
  font-weight: 600;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.3px; /* Reducido de 0.5px */
  margin-bottom: 2px; /* Reducido de 4px */
}

.info-value {
  display: block;
  font-size: 12px; /* Reducido de 14px */
  color: #2c3e50;
  font-weight: 500;
}

.status-badge-large {
  display: inline-block;
  padding: 2px 8px; /* Reducido de 4px 12px */
  border-radius: 12px; /* Reducido de 20px */
  font-size: 10px; /* Reducido de 12px */
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px; /* Reducido de 0.5px */
}

.status-badge-large.recent {
  background: #4CAF50;
  color: white;
}

.status-badge-large.old {
  background: #FF9800;
  color: white;
}
/* Sección de foto */
.photo-section {
  padding: 16px; /* Padding uniforme */
  border-top: 1px solid #dee2e6;
  margin-bottom: 16px; /* Más espacio inferior para la parte final del panel */
}

.photo-container {
  position: relative;
  border-radius: 8px; /* Reducido de 12px */
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* Reducido */
  cursor: pointer;
  transition: transform 0.2s;
}

.photo-container:hover {
  transform: scale(1.02);
}

.registro-photo {
  width: 100%;
  height: auto;
  max-height: 120px; /* Reducido de 200px */
  object-fit: cover;
  display: block;
}

.photo-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.photo-container:hover .photo-overlay {
  opacity: 1;
}

/* Mini botón de descarga animado */
.download-mini-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 32px;
  height: 32px;
  background: rgba(76, 175, 80, 0.9);
  border: none;
  border-radius: 50%;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
  z-index: 10;
  opacity: 0;
  transform: scale(0.8);
}

.photo-container:hover .download-mini-btn {
  opacity: 1;
  transform: scale(1);
  animation: downloadAppear 0.3s ease-out;
}

@keyframes downloadAppear {
  0% {
    opacity: 0;
    transform: scale(0.5) rotate(-180deg);
  }
  60% {
    transform: scale(1.2) rotate(-10deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

.download-mini-btn:hover {
  background: rgba(76, 175, 80, 1);
  transform: scale(1.1);
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.4);
}

.download-mini-btn:active {
  transform: scale(0.95);
}

.download-icon {
  transition: transform 0.2s ease;
}

.download-mini-btn:hover .download-icon {
  transform: translateY(-1px);
  animation: downloadBounce 0.6s ease-in-out;
}

@keyframes downloadBounce {
  0%, 100% { transform: translateY(0); }
  25% { transform: translateY(-2px); }
  50% { transform: translateY(1px); }
  75% { transform: translateY(-1px); }
}

.download-progress {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid transparent;
  opacity: 0;
  transition: opacity 0.2s;
}

.download-progress.downloading {
  opacity: 1;
  border-color: rgba(255, 255, 255, 0.6);
  animation: downloadSpin 1s linear infinite;
}

.download-mini-btn:active .download-progress {
  opacity: 1;
  border-color: rgba(255, 255, 255, 0.6);
  animation: downloadSpin 0.8s linear;
}

@keyframes downloadSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Modal para foto ampliada y detalles completos */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 90%;
  width: auto;
  max-height: 90vh;
  overflow-y: auto;
  margin: 20px;
  animation: slideInUp 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

/* Modal para detalles completos - más ancho */
.modal-content.details {
  width: 800px;
  max-width: 95%;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e0e0e0;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 16px 16px 0 0;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 20px;
  font-weight: 700;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.btn-close:hover {
  background: rgba(0, 0, 0, 0.1);
  color: #333;
}

.modal-body {
  padding: 24px;
}

.full-photo {
  max-width: 100%;
  max-height: 70vh;
  display: block;
  margin: 0 auto;
  border-radius: 8px;
}

/* Estilos para el modal de detalles completos */
.details-modal-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.modal-user-section {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  border-left: 4px solid #4CAF50;
}

.modal-user-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.modal-avatar-text {
  font-size: 24px;
  font-weight: 800;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.modal-user-info {
  flex: 1;
}

.modal-user-name {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 700;
  color: #2c3e50;
}

.modal-user-email {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #6c757d;
}

.modal-status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modal-status-badge.recent {
  background: #4CAF50;
  color: white;
}

.modal-status-badge.old {
  background: #FF9800;
  color: white;
}

.modal-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.modal-info-card {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.modal-info-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.modal-info-card.full-width {
  grid-column: 1 / -1;
}

.modal-info-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  border-radius: 10px;
  color: white;
  flex-shrink: 0;
}

.modal-info-content h5 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modal-info-content p {
  margin: 0;
  font-size: 16px;
  color: #2c3e50;
  font-weight: 500;
}

.modal-photo-section {
  margin-top: 8px;
}

.modal-photo-section h5 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

.modal-photo-container {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s ease;
}

.modal-photo-container:hover {
  transform: scale(1.02);
}

.modal-photo {
  width: 100%;
  height: auto;
  max-height: 300px;
  object-fit: cover;
  display: block;
}

.modal-photo-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.modal-photo-container:hover .modal-photo-overlay {
  opacity: 1;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 16px;
  border-top: 1px solid #e9ecef;
}

.modal-action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s ease;
  text-decoration: none;
}

.modal-action-btn.primary {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.modal-action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(76, 175, 80, 0.4);
}

.modal-action-btn.secondary {
  background: white;
  color: #6c757d;
  border: 1px solid #dee2e6;
}

.modal-action-btn.secondary:hover {
  background: #f8f9fa;
  color: #495057;
  transform: translateY(-1px);
}

/* Responsivo para el modal */
@media (max-width: 768px) {
  .modal-content.details {
    width: 100%;
    margin: 10px;
    max-height: 95vh;
  }
  
  .modal-body {
    padding: 16px;
  }
  
  .modal-info-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .modal-user-section {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
  
  .modal-actions {
    flex-direction: column;
    gap: 8px;
  }
  
  .modal-action-btn {
    width: 100%;
    justify-content: center;
  }
}

/* Estilos para marcadores personalizados */
:global(.custom-location-marker) {
  background: transparent;
  border: none;
}

:global(.location-marker) {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 3px solid white;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
  animation: appearScale 0.4s ease-out;
}

:global(.location-marker.reciente) {
  background: #4CAF50; /* Verde para ubicaciones del día de hoy (últimas 24 horas) */
}

:global(.location-marker.antiguo) {
  background: #FF9800; /* Naranja para ubicaciones de días anteriores (más de 24 horas) */
}

:global(.location-marker.selected) {
  border: 3px solid white;
  box-shadow: 0 0 0 4px rgba(52, 152, 219, 0.7), 0 0 10px rgba(0, 0, 0, 0.4);
  transform: scale(1.15);
  z-index: 100;
  animation: selectedPulse 1.5s ease-in-out infinite;
}

/* Animación de pulso para marcador seleccionado */
:global(.location-marker.pulse-selected) {
  animation: selectedPulse 1.5s ease-in-out infinite, markerGlow 2s ease-in-out;
}

@keyframes selectedPulse {
  0%, 100% {
    box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
  }
  50% {
    box-shadow: 0 2px 15px rgba(76, 175, 80, 0.6);
    transform: scale(1.05);
  }
}

@keyframes markerGlow {
  0% {
    filter: brightness(1);
  }
  50% {
    filter: brightness(1.3) saturate(1.2);
  }
  100% {
    filter: brightness(1);
  }
}

/* Animación para marcador deseleccionado */
:global(.location-marker.marker-unselected) {
  animation: unselectMarker 0.5s ease-out;
}

@keyframes unselectMarker {
  0% {
    transform: scale(1.15);
    filter: brightness(1.2);
  }
  100% {
    transform: scale(1);
    filter: brightness(1);
  }
}

/* Animación de enfoque para marcador */
:global(.location-marker.marker-focus-bounce) {
  animation: focusBounce 1s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes focusBounce {
  0% {
    transform: scale(1);
  }
  30% {
    transform: scale(1.3) rotate(5deg);
  }
  60% {
    transform: scale(1.1) rotate(-2deg);
  }
  100% {
    transform: scale(1.15) rotate(0deg);
  }
}

:global(.pulse-ring) {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  animation: pulsate 2s ease-out infinite;
  background: inherit;
  opacity: 0;
  z-index: -1;
}

@keyframes pulsate {
  0% {
    transform: scale(0.95);
    opacity: 0.8;
  }
  
  70% {
    transform: scale(1.6);
    opacity: 0;
  }
  
  100% {
    transform: scale(1.6);
    opacity: 0;
  }
}

@keyframes appearScale {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  
  60% {
    transform: scale(1.1);
    opacity: 1;
  }
  
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes pulseMarker {
  0% {
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(76, 175, 80, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0);
  }
}

/* Estilos mejorados para el popup moderno del marcador */
:global(.modern-popup-container .leaflet-popup-content-wrapper) {
  border-radius: 20px;
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
  border: none;
  padding: 0;
  overflow: hidden;
  backdrop-filter: blur(15px);
  transform-origin: bottom center;
  z-index: 1050; /* Z-index ajustado para no interferir con la navegación del mapa */
  pointer-events: auto; /* Solo el popup captura eventos */
}

/* Popup centrado - mejora del posicionamiento */
:global(.modern-popup-container.centered-popup .leaflet-popup-content-wrapper) {
  animation: liquidSplashUp 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

/* Animación líquida principal - efecto splash */
@keyframes liquidSplashUp {
  0% {
    opacity: 0;
    transform: translateY(30px) scale(0.3) rotateX(-15deg);
    filter: blur(10px);
    box-shadow: 0 0 0 rgba(0, 0, 0, 0);
  }
  20% {
    opacity: 0.7;
    transform: translateY(15px) scale(0.7) rotateX(-5deg);
    filter: blur(5px);
  }
  40% {
    opacity: 0.9;
    transform: translateY(-5px) scale(1.1) rotateX(2deg);
    filter: blur(2px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  }
  60% {
    opacity: 1;
    transform: translateY(-8px) scale(1.05) rotateX(0deg);
    filter: blur(0px);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
  }
  80% {
    transform: translateY(2px) scale(0.98) rotateX(0deg);
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.18);
  }
  100% {
    opacity: 1;
    transform: translateY(0px) scale(1) rotateX(0deg);
    filter: blur(0px);
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
  }
}

/* Animación de entrada líquida adicional */
:global(.modern-popup-container .leaflet-popup-content-wrapper.liquid-entrance) {
  animation: liquidSplashUp 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275), liquidRipple 1.2s ease-out 0.3s;
}

/* Efecto de ondas líquidas */
@keyframes liquidRipple {
  0% {
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
  }
  25% {
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2), 0 0 0 10px rgba(255, 255, 255, 0.1);
  }
  50% {
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2), 0 0 0 20px rgba(255, 255, 255, 0.05);
  }
  75% {
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2), 0 0 0 30px rgba(255, 255, 255, 0.02);
  }
  100% {
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
  }
}

/* Animación de cierre del popup */
:global(.modern-marker-popup.popup-closing) {
  animation: liquidSplashDown 0.3s cubic-bezier(0.55, 0.085, 0.68, 0.53) forwards;
}

@keyframes liquidSplashDown {
  0% {
    opacity: 1;
    transform: translateY(0px) scale(1);
    filter: blur(0px);
  }
  50% {
    opacity: 0.7;
    transform: translateY(10px) scale(0.9);
    filter: blur(2px);
  }
  100% {
    opacity: 0;
    transform: translateY(30px) scale(0.3);
    filter: blur(10px);
  }
}

:global(.modern-popup-container .leaflet-popup-content) {
  margin: 0;
  padding: 0;
  width: 320px !important;
  max-width: calc(100vw - 40px) !important;
}

:global(.modern-popup-container .leaflet-popup-tip) {
  background: white !important;
  border: none !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  width: 14px !important;
  height: 14px !important;
  margin: 0 !important;
}

/* Posicionamiento mejorado del tip (punta del popup) */
:global(.modern-popup-container.centered-popup .leaflet-popup-tip) {
  left: 50% !important;
  margin-left: -7px !important;
}

/* Asegurar que la punta del popup sea visible y tenga el color correcto */
:global(.modern-popup-container .leaflet-popup-tip-container) {
  width: 40px !important;
  height: 20px !important;
  pointer-events: none !important;
  margin: 0 auto !important;
}

/* Color de la flecha para popup reciente (verde) */
:global(.modern-popup-container .leaflet-popup-tip) {
  background: white !important;
  border: none !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  width: 14px !important;
  height: 14px !important;
  margin: 0 !important;
  z-index: 1051 !important;
}

/* Hacer que la flecha herede el color del popup */
:global(.modern-popup-container:has(.recent-popup) .leaflet-popup-tip) {
  background: #4CAF50 !important;
}

:global(.modern-popup-container:has(.old-popup) .leaflet-popup-tip) {
  background: #FF9800 !important;
}

/* Fallback para navegadores que no soportan :has() */
:global(.modern-popup-container.recent-tip .leaflet-popup-tip) {
  background: #4CAF50 !important;
}

:global(.modern-popup-container.old-tip .leaflet-popup-tip) {
  background: #FF9800 !important;
}

/* Ocultar el botón de cerrar por defecto de Leaflet ya que usamos uno personalizado */
:global(.modern-popup-container .leaflet-container a.leaflet-popup-close-button) {
  display: none !important;
}

/* Asegurar que Leaflet sea navegable con z-index apropiados */
:global(.leaflet-map-pane) {
  z-index: 1 !important;
}

:global(.leaflet-popup-pane) {
  z-index: 1050 !important; /* Reducido para permitir navegación */
}

:global(.leaflet-tooltip-pane) {
  z-index: 1055 !important;
}

:global(.leaflet-control-container) {
  z-index: 1000 !important; /* Controles del mapa siempre accesibles */
}

@keyframes popupSlideFromRight {
  0% {
    opacity: 0;
    transform: translateX(50px) rotateY(-15deg) scale(0.9);
  }
  60% {
    opacity: 0.9;
    transform: translateX(-5px) rotateY(2deg) scale(1.02);
  }
  100% {
    opacity: 1;
    transform: translateX(0) rotateY(0deg) scale(1);
  }
}

:global(.modern-marker-popup) {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: white;
  border-radius: 20px;
  overflow: hidden;
  min-width: 280px;
  animation: contentFlipIn 0.9s cubic-bezier(0.175, 0.885, 0.32, 1.275) 0.2s both;
  position: relative;
}

/* Flecha personalizada para el popup - Perfectamente alineada con el marcador */
:global(.modern-marker-popup::after) {
  content: "";
  position: absolute;
  left: 50%;
  bottom: -16px; /* Pegada al borde inferior */
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-width: 16px 16px 0 16px; /* Triángulo hacia abajo */
  border-style: solid;
  border-color: transparent transparent transparent transparent;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  z-index: 5; /* Para no tapar el marcador */
  pointer-events: none;
}

/* Versión alternativa con rotate para mayor compatibilidad */
:global(.modern-marker-popup::before) {
  content: "";
  position: absolute;
  left: 50%;
  bottom: -8px;
  transform: translateX(-50%) rotate(180deg);
  width: 16px;
  height: 8px;
  background: transparent;
  z-index: 4;
  pointer-events: none;
}

/* Responsive: Flecha ajustada en dispositivos táctiles */
@media (max-width: 768px) {
  :global(.modern-marker-popup::after) {
    border-width: 14px 14px 0 14px;
    bottom: -14px;
  }
}

/* Flecha verde para registros recientes */
:global(.modern-marker-popup.recent-popup::after) {
  border-color: #4CAF50 transparent transparent transparent;
}

/* Flecha naranja para registros antiguos */
:global(.modern-marker-popup.old-popup::after) {
  border-color: #FF9800 transparent transparent transparent;
}

/* Botón de cerrar personalizado del popup - Posicionamiento mejorado */
:global(.popup-close-btn) {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 24px;
  height: 24px;
  background: rgba(255, 255, 255, 0.95);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 15; /* Z-index alto para estar por encima del contenido */
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  color: #666;
  backdrop-filter: blur(10px);
  animation: fadeInRotate 0.6s ease-out 0.4s both;
}

:global(.popup-close-btn:hover) {
  background: rgba(244, 67, 54, 0.95);
  color: white;
  transform: scale(1.1) rotate(90deg);
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.3);
}

:global(.popup-close-btn:active) {
  transform: scale(0.95) rotate(90deg);
}

:global(.popup-close-btn svg) {
  width: 12px;
  height: 12px;
}

@keyframes fadeInRotate {
  0% {
    opacity: 0;
    transform: scale(0.5) rotate(-180deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

/* Popup para ubicaciones recientes (verde) */
:global(.modern-marker-popup.recent-popup) {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 50%, #388e3c 100%);
  box-shadow: 0 8px 32px rgba(76, 175, 80, 0.3);
}

/* Popup para ubicaciones antiguas (naranja) */
:global(.modern-marker-popup.old-popup) {
  background: linear-gradient(135deg, #FF9800 0%, #f57c00 50%, #ef6c00 100%);
  box-shadow: 0 8px 32px rgba(255, 152, 0, 0.3);
}

@keyframes contentFlipIn {
  0% {
    opacity: 0;
    transform: rotateX(-90deg) scale(0.8);
    transform-origin: center bottom;
  }
  50% {
    opacity: 0.7;
    transform: rotateX(10deg) scale(1.05);
  }
  100% {
    opacity: 1;
    transform: rotateX(0deg) scale(1);
  }
}

:global(.popup-header) {
  padding: 18px 40px 14px 22px; /* Padding derecho aumentado para el botón de cerrar */
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(15px);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid rgba(255, 255, 255, 0.25);
  position: relative;
  animation: headerSlideDown 0.6s ease-out 0.4s both;
}

@keyframes headerSlideDown {
  0% {
    opacity: 0;
    transform: translateY(-30px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Efecto brillante en el header */
:global(.popup-header::before) {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  animation: headerShine 3s ease-in-out infinite;
}

@keyframes headerShine {
  0% { left: -100%; }
  50% { left: 100%; }
  100% { left: 100%; }
}

:global(.popup-title) {
  flex: 1;
}

:global(.popup-id) {
  font-size: 12px;
  opacity: 0.9;
  font-weight: 600;
  display: block;
  margin-bottom: 4px;
  animation: fadeInUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.3s both;
  letter-spacing: 0.5px;
}

:global(.popup-title h3) {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  animation: fadeInUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.4s both;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

:global(.popup-status) {
  animation: bounceIn 1s cubic-bezier(0.68, -0.55, 0.265, 1.55) 0.5s both;
}

:global(.status-badge) {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

:global(.status-badge.recent) {
  background: rgba(76, 175, 80, 0.9);
  color: white;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
  animation: pulseGreen 2s ease-in-out infinite 2s;
}

:global(.status-badge.old) {
  background: rgba(255, 152, 0, 0.9);
  color: white;
  box-shadow: 0 2px 8px rgba(255, 152, 0, 0.3);
  animation: pulseOrange 2s ease-in-out infinite 2s;
}

@keyframes pulseGreen {
  0%, 100% {
    box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
  }
  50% {
    box-shadow: 0 2px 15px rgba(76, 175, 80, 0.6);
    transform: scale(1.05);
  }
}

@keyframes pulseOrange {
  0%, 100% {
    box-shadow: 0 2px 8px rgba(255, 152, 0, 0.3);
  }
  50% {
    box-shadow: 0 2px 15px rgba(255, 152, 0, 0.6);
    transform: scale(1.05);
  }
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3) rotate(-45deg);
  }
  50% {
    opacity: 1;
    transform: scale(1.15) rotate(5deg);
  }
  70% {
    transform: scale(0.95) rotate(-2deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

:global(.popup-content) {
  padding: 22px;
}

:global(.user-info) {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 18px;
  animation: slideInLeft 0.9s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.6s both;
}

@keyframes slideInLeft {
  0% {
    opacity: 0;
    transform: translateX(-20px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

:global(.user-avatar) {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid rgba(255, 255, 255, 0.4);
  animation: rotateIn 1s cubic-bezier(0.68, -0.55, 0.265, 1.55) 0.7s both;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

@keyframes rotateIn {
  0% {
    opacity: 0;
    transform: rotate(-180deg) scale(0.8);
  }
  100% {
    opacity: 1;
    transform: rotate(0deg) scale(1);
  }
}

:global(.avatar-text) {
  font-size: 22px;
  font-weight: 800;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

:global(.user-details) {
  flex: 1;
  min-width: 0;
}

:global(.user-name) {
  font-size: 17px;
  font-weight: 700;
  margin-bottom: 5px;
  color: white;
  animation: fadeInRight 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.8s both;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

@keyframes fadeInRight {
  0% {
    opacity: 0;
    transform: translateX(30px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

:global(.user-email) {
  font-size: 13px;
  opacity: 0.95;
  color: rgba(255, 255, 255, 0.9);
  word-break: break-word;
  animation: typewriterEmail 1.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.9s both;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  gap: 6px;
}

:global(.email-icon) {
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  animation: bounceInIcon 0.6s ease-out 1.2s both;
}

:global(.email-icon svg) {
  width: 12px;
  height: 12px;
}

@keyframes bounceInIcon {
  0% {
    opacity: 0;
    transform: scale(0) rotate(180deg);
  }
  60% {
    opacity: 1;
    transform: scale(1.2) rotate(0deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

:global(.email-text) {
  flex: 1;
  min-width: 0;
}

@keyframes typewriterEmail {
  0% {
    opacity: 0;
    width: 0;
    transform: translateX(-10px);
  }
  30% {
    opacity: 1;
    transform: translateX(0);
  }
  100% {
    opacity: 0.9;
    width: 100%;
  }
}

/* Efecto adicional de destello para el email */
:global(.user-email::after) {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: emailShine 2s ease-out 1.5s;
}

@keyframes emailShine {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

:global(.popup-info) {
  margin-bottom: 20px;
}

:global(.info-item) {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  opacity: 0;
  animation: fadeInUp 0.5s ease-out forwards;
}

:global(.info-item:nth-child(1)) {
  animation-delay: 0.9s;
}

:global(.info-item:nth-child(2)) {
  animation-delay: 1s;
}

:global(.info-icon) {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  color: rgba(255, 255, 255, 0.9);
}

:global(.info-icon svg) {
  width: 14px;
  height: 14px;
}

:global(.info-text) {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
}

:global(.popup-actions) {
  text-align: center;
  animation: fadeInUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) 1.2s both;
}

:global(.modern-popup-btn) {
  background: rgba(255, 255, 255, 0.95);
  color: #333;
  border: none;
  padding: 12px 20px;
  border-radius: 25px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
  min-width: 180px;
  justify-content: center;
}

/* Botón "Ver detalles" con estilo Glassmorphism moderno (iPhone style) */
:global(.enhanced-detail-btn) {
  background: rgba(255, 255, 255, 0.2) !important;
  border-radius: 20px !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  color: #fff !important;
  padding: 12px 28px !important;
  font-size: 0.95rem !important;
  width: auto !important;
  margin: 10px auto !important;
  box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.1) !important;
  backdrop-filter: blur(8px) !important;
  -webkit-backdrop-filter: blur(8px) !important;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
  cursor: pointer !important;
  font-weight: 700 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 6px !important;
  text-decoration: none !important;
  position: relative !important;
  overflow: hidden !important;
  text-transform: none !important;
  letter-spacing: 0.3px !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
}

:global(.enhanced-detail-btn::before) {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.4s ease;
  z-index: 1;
}

:global(.enhanced-detail-btn:hover::before) {
  left: 100%;
}

:global(.enhanced-detail-btn:hover) {
  background: rgba(255, 255, 255, 0.35) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  transform: translateY(-2px) !important;
  border-color: rgba(255, 255, 255, 0.4) !important;
}

:global(.enhanced-detail-btn:active) {
  transform: scale(0.95) !important;
  background: rgba(255, 255, 255, 0.15) !important;
  transition: all 0.1s ease-out !important;
}

/* Efecto de líquido para el botón glass */
@keyframes liquidGlassEffect {
  0% {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  }
  50% {
    box-shadow: 0 4px 25px rgba(255, 255, 255, 0.15);
  }
  100% {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  }
}

:global(.enhanced-detail-btn .btn-icon) {
  color: rgba(255, 255, 255, 0.9) !important;
  font-size: 14px !important;
  transition: all 0.3s ease;
  z-index: 2;
}

:global(.enhanced-detail-btn:hover .btn-icon) {
  color: #ffffff !important;
  transform: scale(1.15);
}

:global(.enhanced-detail-btn .btn-text) {
  color: rgba(255, 255, 255, 0.95) !important;
  font-weight: 700 !important;
  font-size: 0.92rem !important;
  position: relative;
  z-index: 2;
  transition: color 0.3s ease;
}

:global(.enhanced-detail-btn:hover .btn-text) {
  color: #ffffff !important;
}

:global(.modern-popup-btn:hover) {
   background: white;
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.18);
}

:global(.modern-popup-btn:hover .btn-icon) {
  transform: scale(1.1);
}

:global(.modern-popup-btn:active) {
  transform: translateY(0) scale(1);
}

:global(.btn-icon) {
  font-size: 16px;
  transition: all 0.3s ease;
}

/* Estilos responsivos para la barra de filtros moderna */
@media (max-width: 1024px) {
  .main-content {
    margin-left: 0;
  }
  
  .filter-group {
    flex-wrap: wrap;
    gap: 12px;
    width: 100%;
  }
    .filter-legend {
    order: 2; /* Colocar después del buscador en pantallas medianas */
    width: auto;
    justify-content: center;
    margin: 8px 0 0 0;
  }
  
  .search-item {
    margin-left: 0;
    width: 100%;
    order: 1; /* Buscador antes que la leyenda */
  }
  
  .modern-search-wrapper {
    min-width: 100%;
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 12px 16px;
  }
  
  .title-glass-container h1 {
    font-size: 24px;
  }
  
  .title-icon {
    width: 20px;
    height: 20px;
  }
  
  .refresh-btn {
    padding: 10px 16px;
    font-size: 13px;
  }
  
  .page-content {
    padding: 16px 12px;
  }
    .filter-group {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
    padding: 16px;
  }
    .filter-legend {
    order: 2; /* Mantener la leyenda después del buscador */
    width: 100%;
    justify-content: center;
    gap: 20px;
    margin: 8px 0 0 0;
    padding: 12px;
  }
  
  .legend-item-inline {
    gap: 8px;
  }
  
  .legend-point-small {
    width: 14px;
    height: 14px;
  }
  
  .legend-text {
    font-size: 13px;
  }
  
  .filter-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .modern-select {
    width: 100%;
    min-width: auto;
    padding: 12px;
    font-size: 16px;
  }
  
  .modern-search-wrapper {
    min-width: 100%;
    padding: 6px;
  }
  
  .modern-search-input {
    padding: 12px;
    font-size: 16px;
  }
  
  .modern-search-btn {
    width: 40px;
    height: 40px;
  }
}

@media (max-width: 480px) {
  .title-glass-container {
    gap: 8px;
  }
  
  .title-glass-container h1 {
    font-size: 20px;
  }
  
  .title-section p {
    font-size: 12px;
  }
  
  .refresh-btn {
    padding: 8px 12px;
    font-size: 12px;
    gap: 6px;
  }
    .filter-group {
    border-radius: 12px;
    padding: 12px;
  }
  
  .filter-legend {
    padding: 10px;
    gap: 16px;
    border-radius: 8px;
  }
  
  .legend-item-inline {
    gap: 6px;
  }
  
  .legend-point-small {
    width: 12px;
    height: 12px;
  }
  
  .legend-text {
    font-size: 11px;
  }
  
  .modern-search-wrapper {
    border-radius: 10px;
  }
  
  .modern-search-btn {
    border-radius: 6px;
  }
}
</style>
