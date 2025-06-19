<template>
  <div class="visor-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div>
            <h1>Visor de Mapa</h1>
            <p>Visualiza todas las ubicaciones en tiempo real</p>
          </div>
          <div class="header-actions">
            <button @click="recargarMapa" class="refresh-btn" :disabled="loading">
              <span class="refresh-icon" :class="{ spinning: loading }">🔄</span>
              {{ loading ? 'Cargando...' : 'Actualizar' }}
            </button>
          </div>
        </div>
      </header>

      <div class="page-content">
        <div class="map-controls">
          <div class="control-group">
            <label for="filter-type">Filtrar por tipo:</label>
            <select id="filter-type" v-model="filtroTipo" class="control-select" @change="aplicarFiltros">
              <option value="">Todos los registros</option>
              <option value="critical">Puntos críticos</option>
              <option value="regular">Puntos regulares</option>
            </select>
          </div>
          
          <div class="control-group">
            <label for="filter-date">Periodo de tiempo:</label>
            <select id="filter-date" v-model="filtroPeriodo" class="control-select" @change="aplicarFiltros">
              <option value="all">Todo el tiempo</option>
              <option value="today">Hoy</option>
              <option value="week">Esta semana</option>
              <option value="month">Este mes</option>
            </select>
          </div>
          
          <div class="control-group search-group">
            <label for="search-location">Buscar ubicación:</label>
            <div class="search-wrapper">
              <input 
                id="search-location" 
                v-model="busquedaUbicacion" 
                type="text" 
                placeholder="Dirección o coordenadas..." 
                class="control-input"
              >
              <button @click="buscarUbicacion" class="search-btn">
                <span class="search-icon">🔍</span>
              </button>
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
          
          <div id="mapa-principal" class="mapa-container"></div>          <div class="map-legend">
            <h3>Leyenda</h3>
            <div class="legend-item">
              <span class="legend-point reciente"></span>
              <span>Ubicación del día de hoy</span>
            </div>
            <div class="legend-item">
              <span class="legend-point antiguo"></span>
              <span>Ubicación de días anteriores</span>
            </div>
          </div>
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
                >
                <div class="photo-overlay" @click="verFotoAmpliada(`${API_URL}/${registroSeleccionado.foto_url}`)">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                    <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
                  </svg>
                </div>
              </div>
            </div>

            <!-- Acciones del panel -->
            <div class="panel-actions-section">
              <button @click="centrarMapa(registroSeleccionado)" class="action-btn-large primary-btn">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8M3.05,13H1V11H3.05C3.5,6.83 6.83,3.5 11,3.05V1H13V3.05C17.17,3.5 20.5,6.83 20.95,11H23V13H20.95C20.5,17.17 17.17,20.5 13,20.95V23H11V20.95C6.83,20.5 3.5,17.17 3.05,13M12,5A7,7 0 0,0 5,12A7,7 0 0,0 12,19A7,7 0 0,0 19,12A7,7 0 0,0 12,5Z"/>
                </svg>
                Centrar en mapa
              </button>
              <button @click="verRegistroCompleto(registroSeleccionado)" class="action-btn-large secondary-btn">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z"/>
                </svg>
                Ver registro completo
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
    
    <!-- Modal para foto ampliada -->
    <div v-if="showModal" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ modalTitle }}</h3>
          <button @click="cerrarModal" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <img v-if="modalType === 'photo'" :src="selectedPhotoUrl" alt="Fotografía ampliada" class="full-photo">
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
    return new Date(fechaStr).toLocaleString('es-ES')
  } catch (e) {
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

// Ver foto ampliada en modal
const verFotoAmpliada = (fotoUrl) => {
  selectedPhotoUrl.value = fotoUrl
  modalTitle.value = 'Fotografía del Registro'
  modalType.value = 'photo'
  showModal.value = true
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
.visor-container {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  margin-left: 280px;
  background: #f8f9fa;
}

.page-header {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-bottom: 1px solid #e0e0e0;
  padding: 14px 32px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h1 {
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 24px;
  margin-bottom: 2px;
  font-weight: 700;
}

.header-content p {
  color: #7f8c8d;
  font-size: 13px; /* Reducido de 14px a 13px */
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background: #45a049;
  transform: translateY(-1px);
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.page-content {
  padding: 12px 24px; /* Reducido aún más el padding */
  display: flex;
  flex-direction: column;
  gap: 10px; /* Reducido de 16px a 10px */
  height: calc(100vh - 85px); /* Ajustado para optimizar el espacio */
  position: relative;
}

/* Controles del mapa */
.map-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 8px; /* Reducido de 12px a 8px */
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 8px 12px; /* Reducido padding vertical */
  border-radius: 8px; /* Reducido el border-radius */
  margin-bottom: 8px; /* Reducido el margen inferior */
  min-height: 60px; /* Altura mínima controlada */
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 2px; /* Reducido de 4px a 2px */
  min-width: 160px; /* Reducido de 180px a 160px */
  flex: 1;
}

.search-group {
  min-width: 250px; /* Reducido de 300px a 250px */
  flex: 2;
}

.control-group label {
  font-weight: 500;
  color: #2c3e50;
  font-size: 12px; /* Reducido de 14px a 12px */
}

.control-select, .control-input {
  padding: 6px 8px; /* Reducido de 8px 10px */
  border: 1px solid #e0e0e0;
  border-radius: 4px; /* Reducido de 6px a 4px */
  font-size: 12px; /* Reducido de 13px a 12px */
  transition: all 0.2s;
  height: 32px; /* Altura fija para mejor control */
}

.control-select:focus, .control-input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.search-wrapper {
  position: relative;
  display: flex;
}

.control-input {
  flex: 1;
  padding-right: 44px;
}

.search-btn {
  position: absolute;
  right: 2px;
  top: 50%;
  transform: translateY(-50%);
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  width: 28px; /* Reducido de 36px a 28px */
  height: 28px; /* Reducido de 36px a 28px */
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 12px; /* Añadido para mejor proporción */
}

.search-btn:hover {
  background: #45a049;
}

/* Mapa principal */
.visor-section {
  position: relative;
  flex: 1;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
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

/* Leyenda del mapa */
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
  background: #4CAF50; /* Verde para ubicaciones del día de hoy */
}

.legend-point.antiguo {
  background: #FF9800; /* Naranja para ubicaciones de días anteriores */
}

/* Panel de información del registro seleccionado - Versión mejorada */
.registro-info-panel {
  position: fixed;
  top: 90px;
  right: -400px;
  width: 380px;
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
  padding: 16px 20px;
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
  margin: 0 0 4px 0;
  font-size: 18px;
  font-weight: 700;
}

.panel-id {
  font-size: 12px;
  opacity: 0.9;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.close-panel-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 32px;
  height: 32px;
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
  max-height: calc(100vh - 180px);
  overflow-y: auto;
}

/* Sección de usuario */
.user-section {
  padding: 20px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-avatar-large {
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

.panel-old .user-avatar-large {
  background: linear-gradient(135deg, #FF9800 0%, #f57c00 100%);
}

.avatar-text-large {
  font-size: 24px;
  font-weight: 800;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.user-info-detail {
  flex: 1;
  min-width: 0;
}

.user-name-large {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 700;
  color: #2c3e50;
}

.user-email-large {
  margin: 0;
  font-size: 14px;
  color: #6c757d;
  word-break: break-word;
}

/* Sección de información */
.info-section {
  padding: 20px;
}

.section-title {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 8px;
}

.info-item-detail {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 16px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 3px solid #4CAF50;
}

.panel-old .info-item-detail {
  border-left-color: #FF9800;
}

.info-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
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
  font-size: 12px;
  font-weight: 600;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.info-value {
  display: block;
  font-size: 14px;
  color: #2c3e50;
  font-weight: 500;
}

.status-badge-large {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
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
  padding: 20px;
  border-top: 1px solid #dee2e6;
}

.photo-container {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s;
}

.photo-container:hover {
  transform: scale(1.02);
}

.registro-photo {
  width: 100%;
  height: auto;
  max-height: 200px;
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

/* Sección de acciones */
.panel-actions-section {
  padding: 20px;
  border-top: 1px solid #dee2e6;
  background: #f8f9fa;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.action-btn-large {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
  text-decoration: none;
}

.primary-btn {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(76, 175, 80, 0.4);
}

.secondary-btn {
  background: white;
  color: #4CAF50;
  border: 2px solid #4CAF50;
}

.secondary-btn:hover {
  background: #4CAF50;
  color: white;
  transform: translateY(-2px);
}

.panel-old .primary-btn {
  background: linear-gradient(135deg, #FF9800 0%, #f57c00 100%);
  box-shadow: 0 4px 12px rgba(255, 152, 0, 0.3);
}

.panel-old .primary-btn:hover {
  box-shadow: 0 6px 16px rgba(255, 152, 0, 0.4);
}

.panel-old .secondary-btn {
  color: #FF9800;
  border-color: #FF9800;
}

.panel-old .secondary-btn:hover {
  background: #FF9800;
}

/* Modal para foto ampliada */
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
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 90%;
  width: auto;
  max-height: 90vh;
  overflow-y: auto;
  margin: 20px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-body {
  padding: 20px;
}

.full-photo {
  max-width: 100%;
  max-height: 70vh;
  display: block;
  margin: 0 auto;
  border-radius: 8px;
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

/* Responsive mejorado para popup moderno y panel de detalles */
@media (max-width: 1200px) {
  .registro-info-panel {
    width: 350px;
    right: -370px;
  }
  
  .registro-info-panel.panel-visible {
    right: 15px;
  }
}

@media (max-width: 1024px) {
  .registro-info-panel {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    right: auto;
    width: 90%;
    max-width: 400px;
    max-height: 85vh;
    z-index: 2000;
    border-radius: 16px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  }
  
  .registro-info-panel.panel-visible {
    right: auto;
    animation: scaleInCenter 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  }
    /* Overlay para móvil que no bloquee el mapa */
  .registro-info-panel::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    z-index: -1;
    animation: fadeInOverlay 0.3s ease-out;
    pointer-events: none; /* No bloquear eventos del mapa */
  }
  
  :global(.modern-popup-container .leaflet-popup-content) {
    width: 280px !important;
  }
  
  :global(.modern-marker-popup) {
    min-width: 260px;
  }
}

@keyframes scaleInCenter {
  0% {
    transform: translate(-50%, -50%) scale(0.8);
    opacity: 0;
  }
  100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }
  
  .registro-info-panel {
    width: 95%;
    max-width: none;
    border-radius: 12px;
  }
  
  .user-section {
    padding: 16px;
    gap: 12px;
  }
  
  .user-avatar-large {
    width: 50px;
    height: 50px;
  }
  
  .avatar-text-large {
    font-size: 20px;
  }
  
  .user-name-large {
    font-size: 16px;
  }
  
  .user-email-large {
    font-size: 13px;
  }
  
  .info-section,
  .photo-section,
  .panel-actions-section {
    padding: 16px;
  }
  
  .section-title {
    font-size: 15px;
  }
  
  .info-item-detail {
    padding: 10px;
  }
  
  .info-icon-wrapper {
    width: 20px;
    height: 20px;
  }
  
  .info-label {
    font-size: 11px;
  }
  
  .info-value {
    font-size: 13px;
  }
  
  .action-btn-large {
    padding: 10px 14px;
    font-size: 13px;
  }
  
  :global(.modern-popup-container .leaflet-popup-content) {
    width: 250px !important;
  }
  
  :global(.modern-marker-popup) {
    min-width: 240px;
  }
  
  :global(.popup-header) {
    padding: 12px 16px 8px;
  }
  
  :global(.popup-title h3) {
    font-size: 16px;
  }
  
  :global(.popup-content) {
    padding: 16px;
  }
  
  :global(.user-avatar) {
    width: 40px;
    height: 40px;
  }
  
  :global(.avatar-text) {
    font-size: 18px;
  }
    :global(.user-name) {
    font-size: 14px;
  }
    /* Responsive para botón glass en móviles - estilo iPhone optimizado */
  :global(.enhanced-detail-btn) {
    padding: 10px 20px !important;
    font-size: 0.9rem !important;
    width: auto !important;
    margin: 8px auto !important;
    border-radius: 18px !important;
  }
  
  :global(.enhanced-detail-btn .btn-icon) {
    font-size: 12px !important;
  }
  
  :global(.enhanced-detail-btn .btn-text) {
    font-size: 0.85rem !important;
  }
  
  :global(.user-email) {
    font-size: 12px;
    gap: 4px;
  }
  
  :global(.email-icon svg) {
    width: 10px;
    height: 10px;
  }
    :global(.modern-popup-btn) {
    padding: 8px 14px;
    font-size: 12px;
    min-width: 160px;
  }
    :global(.enhanced-detail-btn) {
    padding: 8px 12px;
    font-size: 11px;
    min-width: 120px;
    letter-spacing: 0.3px;
  }
  
  :global(.enhanced-detail-btn .btn-text) {
    font-size: 11px;
  }
    :global(.popup-close-btn) {
    width: 20px;
    height: 20px;
    top: 6px;
    right: 6px;
  }
  
  :global(.popup-close-btn svg) {
    width: 10px;
    height: 10px;
  }
  
  :global(.popup-header) {
    padding: 12px 32px 8px 16px !important; /* Más padding derecho para el botón */
  }
  
  .map-controls {
    flex-direction: column;
    gap: 8px;
    padding: 12px;
  }
  
  .control-group {
    min-width: auto;
  }
  
  .search-group {
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .registro-info-panel {
    width: 98%;
    max-height: 90vh;
  }
  
  .panel-header {
    padding: 12px 16px;
  }
  
  .panel-title-section h3 {
    font-size: 16px;
  }
  
  .user-section {
    padding: 12px;
    gap: 10px;
  }
  
  .user-avatar-large {
    width: 45px;
    height: 45px;
  }
  
  .avatar-text-large {
    font-size: 18px;
  }
  
  .user-name-large {
    font-size: 15px;
  }
  
  .user-email-large {
    font-size: 12px;
  }
  
  .info-section,
  .photo-section,
  .panel-actions-section {
    padding: 12px;
  }
  
  .section-title {
    font-size: 14px;
    margin-bottom: 12px;
  }
  
  .info-item-detail {
    padding: 8px;
    margin-bottom: 12px;
  }
  
  .action-btn-large {
    padding: 8px 12px;
    font-size: 12px;
    gap: 6px;
  }
  
  :global(.modern-popup-container .leaflet-popup-content) {
    width: 220px !important;
  }
  
  :global(.modern-marker-popup) {
    min-width: 200px;
  }
  
  :global(.popup-content) {
    padding: 12px;
  }
  
  :global(.user-info) {
    gap: 10px;
  }
  
  :global(.user-avatar) {
    width: 35px;
    height: 35px;
  }
  
  :global(.avatar-text) {
    font-size: 16px;
  }
  
  .page-content {
    padding: 8px 12px;
  }
  
  .map-controls {
    padding: 8px;
  }
}

/* Animaciones y efectos adicionales */

/* Efecto de brillo en el panel header */
.panel-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  animation: headerShinePanel 4s ease-in-out infinite;
}

@keyframes headerShinePanel {
  0% { left: -100%; }
  50% { left: 100%; }
  100% { left: 100%; }
}

/* Animaciones mejoradas para el popup */
:global(.popup-header) {
  animation: headerSlideDown 0.6s ease-out 0.4s both;
}

/* Efectos para la navegación del mapa siempre habilitada */
:global(.leaflet-clickable) {
  cursor: pointer !important;
}

:global(.leaflet-container) {
  cursor: grab !important;
}

:global(.leaflet-container:active) {
  cursor: grabbing !important;
}

/* Mejorar visibilidad de controles del mapa */
:global(.leaflet-control-zoom a) {
  background-color: rgba(255, 255, 255, 0.95) !important;
  color: #333 !important;
  border: 1px solid rgba(0, 0, 0, 0.1) !important;
  transition: all 0.2s ease !important;
}

:global(.leaflet-control-zoom a:hover) {
  background-color: #4CAF50 !important;
  color: white !important;
  transform: scale(1.05) !important;
}

/* Animación de entrada para elementos del panel */
.info-item-detail {
  opacity: 0;
  animation: fadeInUp 0.5s ease-out forwards;
}

.info-item-detail:nth-child(1) { animation-delay: 0.1s; }
.info-item-detail:nth-child(2) { animation-delay: 0.2s; }
.info-item-detail:nth-child(3) { animation-delay: 0.3s; }
.info-item-detail:nth-child(4) { animation-delay: 0.4s; }
.info-item-detail:nth-child(5) { animation-delay: 0.5s; }

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

/* Efecto de pulso para el avatar */
.user-avatar-large {
  animation: avatarPulse 3s ease-in-out infinite;
}

@keyframes avatarPulse {
  0%, 100% {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  50% {
    box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
  }
}

.panel-old .user-avatar-large {
  animation: avatarPulseOrange 3s ease-in-out infinite;
}

@keyframes avatarPulseOrange {
  0%, 100% {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  50% {
    box-shadow: 0 6px 20px rgba(255, 152, 0, 0.3);
  }
}

/* Animación para la foto */
.photo-container {
  opacity: 0;
  animation: fadeInScale 0.6s ease-out 0.8s forwards;
}

@keyframes fadeInScale {
  0% {
    opacity: 0;
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

/* Animación para los botones de acción */
.action-btn-large {
  opacity: 0;
  animation: slideInBottom 0.5s ease-out forwards;
}

.action-btn-large:nth-child(1) { animation-delay: 0.9s; }
.action-btn-large:nth-child(2) { animation-delay: 1s; }

@keyframes slideInBottom {
  0% {
    opacity: 0;
    transform: translateY(30px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Efectos de hover mejorados */
.info-item-detail:hover {
  transform: translateX(4px);
  background: #f1f3f4;
  border-left-width: 4px;
}

.info-icon-wrapper:hover {
  transform: scale(1.1);
}

/* Scroll personalizado para el panel */
.panel-content::-webkit-scrollbar {
  width: 6px;
}

.panel-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.panel-content::-webkit-scrollbar-thumb {
  background: #4CAF50;
  border-radius: 3px;
}

.panel-old .panel-content::-webkit-scrollbar-thumb {
  background: #FF9800;
}

.panel-content::-webkit-scrollbar-thumb:hover {
  background: #45a049;
}

.panel-old .panel-content::-webkit-scrollbar-thumb:hover {
  background: #f57c00;
}

/* Efectos adicionales para marcadores */
:global(.location-marker:hover) {
  transform: scale(1.1);
  box-shadow: 0 0 8px rgba(76, 175, 80, 0.6);
}

:global(.location-marker.antiguo:hover) {
  box-shadow: 0 0 8px rgba(255, 152, 0, 0.6);
}

/* Mejoras en la accesibilidad - focus visible */
.modern-popup-btn:focus-visible,
.action-btn-large:focus-visible,
.close-panel-btn:focus-visible,
.control-select:focus-visible,
.control-input:focus-visible,
.search-btn:focus-visible,
.refresh-btn:focus-visible {
  outline: 2px solid #4CAF50;
  outline-offset: 2px;
}

/* Transiciones suaves para todos los elementos interactivos */
* {
  transition: all 0.2s ease-out;
}

/* Estados de carga mejorados */
.loading-container {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  padding: 60px 20px;
  text-align: center;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mejoras en el contenedor del mapa para evitar problemas de z-index */
.mapa-container {
  flex: 1;
  width: 100%;
  min-height: 400px;
  z-index: 10;
  position: relative;
}

/* Asegurar que Leaflet no interfiera con nuestros z-index */
:global(.leaflet-map-pane) {
  z-index: 1 !important;
}

:global(.leaflet-popup-pane) {
  z-index: 1000 !important;
}

:global(.leaflet-tooltip-pane) {
  z-index: 1050 !important;
}

/* Prevenir scroll del body cuando el panel móvil está abierto */
@media (max-width: 1024px) {
  body.panel-open {
    overflow: hidden;
  }
}

/* Transiciones suaves para todos los elementos interactivos */
* {
  transition: all 0.2s ease-out;
}

/* Mejora en la accesibilidad - focus visible */
.modern-popup-btn:focus-visible,
.action-btn:focus-visible,
.control-select:focus-visible,
.control-input:focus-visible,
.search-btn:focus-visible,
.refresh-btn:focus-visible {
  outline: 2px solid #4CAF50;
  outline-offset: 2px;
}

/* Estados de carga mejorados */
.loading-container {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  padding: 60px 20px;
  text-align: center;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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

/* Mejoras en el estado de error */
.error-container {
  background: linear-gradient(135deg, #fee 0%, #fcc 100%);
  border: 1px solid #f5c6cb;
  color: #721c24;
  padding: 60px 20px;
  text-align: center;
  border-radius: 12px;
  animation: shakeError 0.6s ease-out;
}

@keyframes shakeError {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px);
  }
  75% {
    transform: translateX(5px);
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

/* Mejoras en el header */
.page-header {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-bottom: 1px solid #e0e0e0;
  padding: 14px 32px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.header-content h1 {
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 24px;
  margin-bottom: 2px;
  font-weight: 700;
}

/* Mejoras finales en controles */
.map-controls {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}
</style>
