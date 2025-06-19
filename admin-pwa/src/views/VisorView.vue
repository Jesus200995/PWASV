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
        
        <!-- Información del registro seleccionado -->
        <div v-if="registroSeleccionado" class="registro-info-panel">
          <div class="panel-header">
            <h3>Detalles del Registro</h3>
            <button @click="cerrarDetalles" class="close-panel-btn">×</button>
          </div>
          <div class="panel-content">
            <div class="info-row">
              <strong>ID:</strong> #{{ registroSeleccionado.id }}
            </div>
            <div class="info-row">
              <strong>Usuario:</strong> {{ registroSeleccionado.usuario?.nombre_completo || `Usuario ${registroSeleccionado.usuario_id}` }}
            </div>
            <div class="info-row">
              <strong>Fecha:</strong> {{ formatFecha(registroSeleccionado.fecha_hora) }}
            </div>            <div class="info-row">
              <strong>Ubicación:</strong> {{ formatCoordenadas(registroSeleccionado.latitud, registroSeleccionado.longitud) }}
              <span class="ubicacion-badge">Última conocida</span>
              <span :class="['estado-badge', esUbicacionReciente(registroSeleccionado.fecha_hora) ? 'reciente' : 'antiguo']">
                {{ esUbicacionReciente(registroSeleccionado.fecha_hora) ? 'Hoy' : 'Días anteriores' }}
              </span>
            </div>
            <div class="info-row">
              <strong>Descripción:</strong> {{ registroSeleccionado.descripcion || 'Sin descripción' }}
            </div>
            <div v-if="registroSeleccionado.foto_url" class="info-photo">
              <img 
                :src="`${API_URL}/${registroSeleccionado.foto_url}`" 
                alt="Foto del registro"
                @click="verFotoAmpliada(`${API_URL}/${registroSeleccionado.foto_url}`)"
              >
            </div>
            <div class="panel-actions">
              <button @click="centrarMapa(registroSeleccionado)" class="action-btn center-btn">
                Centrar en mapa
              </button>
              <button @click="verRegistroCompleto(registroSeleccionado)" class="action-btn view-btn">
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

// Registro seleccionado
const registroSeleccionado = ref(null)

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
        popupAnchor: [0, -iconSize[0] / 2] // Centrado horizontalmente sobre el marcador
      })

      // Crear marcador y popup con posicionamiento mejorado
      const marker = window.L.marker([lat, lng], { icon: customIcon })
        .bindPopup(`
          <div class="modern-marker-popup ${esReciente ? 'recent-popup' : 'old-popup'}">
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
                <button class="modern-popup-btn popup-detail-btn">
                  <span class="btn-icon">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
                    </svg>
                  </span>
                  Ver detalles
                </button>
              </div>
            </div>
          </div>
        `, {
          maxWidth: 320,
          minWidth: 300,
          className: 'modern-popup-container centered-popup',
          offset: [0, 0], // Centrado sobre el marcador
          autoPan: true, // Permitir autopan inteligente
          autoPanPadding: [50, 50], // Padding para evitar bordes
          keepInView: true // Mantener popup visible
        })
      
      // Añadir evento de click para mostrar más detalles
      marker.on('click', () => {
        mostrarDetallesRegistro(registro)
      })      // Añadir evento al botón dentro del popup con animación mejorada
      marker.on('popupopen', (e) => {
        setTimeout(() => {
          const btn = document.querySelector('.popup-detail-btn')
          if (btn) {
            btn.addEventListener('click', (e) => {
              e.preventDefault()
              e.stopPropagation()
              
              // Añadir clase de animación al popup antes de cerrar
              const popupElement = btn.closest('.modern-marker-popup')
              if (popupElement) {
                popupElement.classList.add('popup-closing')
              }
              
              // Cerrar popup y mostrar detalles con delay para animación
              setTimeout(() => {
                marker.closePopup()
                mostrarDetallesRegistro(registro)
              }, 300)
            })
            
            // Añadir efecto de animación líquida al popup
            const popupWrapper = btn.closest('.leaflet-popup-content-wrapper')
            if (popupWrapper) {
              popupWrapper.classList.add('liquid-entrance')
            }
          }
        }, 100)
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

// Mostrar detalles de un registro con posicionamiento mejorado
const mostrarDetallesRegistro = (registro) => {
  registroSeleccionado.value = registro
  
  // Centrar el mapa en la ubicación seleccionada con animación suave
  if (map && registro.latitud && registro.longitud) {
    const lat = parseFloat(registro.latitud)
    const lng = parseFloat(registro.longitud)
    
    // Calcular el mejor centrado considerando el tamaño del popup y el panel de detalles
    const mapContainer = map.getContainer()
    const mapBounds = mapContainer.getBoundingClientRect()
    const panelWidth = 300 // Ancho del panel de detalles
    
    // Centrar el marcador en el área visible disponible (descontando el panel)
    const availableWidth = mapBounds.width - panelWidth - 50 // 50px de margen
    const centerOffset = (availableWidth / 2) - (mapBounds.width / 2)
    
    // Convertir offset a coordenadas geográficas
    const targetPoint = map.latLngToContainerPoint([lat, lng])
    const offsetPoint = window.L.point(targetPoint.x + centerOffset, targetPoint.y)
    const newCenter = map.containerPointToLatLng(offsetPoint)
    
    // Animación suave hacia la nueva posición
    map.flyTo(newCenter, Math.max(map.getZoom(), 15), {
      animate: true,
      duration: 1.2,
      easeLinearity: 0.15
    })
  }
  
  // Resaltar el marcador seleccionado con animación
  if (map && markers.length > 0) {
    markers.forEach(m => {
      const markerElement = m.getElement()
      if (markerElement) {
        const marker = markerElement.querySelector('.location-marker')
        if (marker) {
          marker.classList.remove('selected', 'pulse-selected')
        }
      }
    })
    
    if (registro.marker) {
      const markerElement = registro.marker.getElement()
      if (markerElement) {
        const marker = markerElement.querySelector('.location-marker')
        if (marker) {
          marker.classList.add('selected', 'pulse-selected')
          
          // Añadir animación temporal de destaque
          setTimeout(() => {
            marker.classList.remove('pulse-selected')
          }, 2000)
        }
      }
    }
  }
}

// Cerrar panel de detalles con animaciones mejoradas
const cerrarDetalles = () => {
  registroSeleccionado.value = null
  
  // Quitar resaltado de todos los marcadores con animación
  if (map && markers.length > 0) {
    markers.forEach(m => {
      const markerElement = m.getElement()
      if (markerElement) {
        const marker = markerElement.querySelector('.location-marker')
        if (marker) {
          marker.classList.remove('selected', 'pulse-selected')
          // Añadir animación de salida temporal
          marker.classList.add('marker-unselected')
          setTimeout(() => {
            marker.classList.remove('marker-unselected')
          }, 500)
        }
      }
    })
  }
  
  // Recentrar el mapa para mostrar todos los marcadores
  if (map && markers.length > 0) {
    const group = new window.L.featureGroup(markers)
    map.fitBounds(group.getBounds().pad(0.1), {
      animate: true,
      duration: 1,
      easeLinearity: 0.2
    })
  }
}

// Centrar mapa en un registro específico con mejor posicionamiento
const centrarMapa = (registro) => {
  if (!map) return
  
  const lat = parseFloat(registro.latitud)
  const lng = parseFloat(registro.longitud)
  
  if (!isNaN(lat) && !isNaN(lng)) {
    // Calcular el mejor centrado considerando el panel de detalles abierto
    const mapContainer = map.getContainer()
    const mapBounds = mapContainer.getBoundingClientRect()
    const panelWidth = 300
    
    // Centrar en el área visible disponible
    const availableWidth = mapBounds.width - panelWidth - 50
    const centerOffset = (availableWidth / 2) - (mapBounds.width / 2)
    
    const targetPoint = map.latLngToContainerPoint([lat, lng])
    const offsetPoint = window.L.point(targetPoint.x + centerOffset, targetPoint.y)
    const newCenter = map.containerPointToLatLng(offsetPoint)
    
    map.flyTo(newCenter, Math.max(map.getZoom(), 16), {
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

// Ciclo de vida
onMounted(() => {
  // Cargar registros y después inicializar el mapa
  cargarRegistros()
})

onUnmounted(() => {
  // Limpiar mapa al salir
  if (map) {
    map.remove()
    map = null
  }
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

/* Panel de información del registro seleccionado - z-index mejorado */
.registro-info-panel {
  position: absolute;
  top: 78px;
  right: 16px;
  width: 300px;
  max-width: calc(100% - 32px);
  max-height: calc(100% - 95px);
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  overflow: auto;
  z-index: 1200; /* Mayor que el popup para que aparezca encima */
  animation: slideinPanel 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

@keyframes slideinPanel {
  from {
    transform: translateX(320px) scale(0.95);
    opacity: 0;
    filter: blur(5px);
  }
  to {
    transform: translateX(0) scale(1);
    opacity: 1;
    filter: blur(0px);
  }
}

.panel-header {
  padding: 10px 14px; /* Reducido aún más */
  background: #4CAF50;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 5;
}

.panel-header h3 {
  margin: 0;
  font-size: 15px; /* Reducido de 16px a 15px */
}

.close-panel-btn {
  background: none;
  border: none;
  color: white;
  font-size: 20px; /* Reducido de 22px a 20px */
  cursor: pointer;
  width: 26px; /* Reducido de 28px a 26px */
  height: 26px; /* Reducido de 28px a 26px */
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s;
}

.close-panel-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.panel-content {
  padding: 12px 14px; /* Reducido de 14px 16px */
  max-height: calc(100% - 46px); /* Ajustado para el nuevo header más pequeño */
  overflow-y: auto;
}

.info-row {
  margin-bottom: 8px; /* Reducido de 10px a 8px */
  padding-bottom: 8px; /* Reducido de 10px a 8px */
  border-bottom: 1px solid #f0f0f0;
  font-size: 12px; /* Reducido de 13px a 12px */
  line-height: 1.4; /* Mejorar legibilidad */
}

.info-row:last-child {
  border-bottom: none;
}

.info-row strong {
  color: #2c3e50;
  margin-right: 6px;
  display: inline-block;
  min-width: 65px; /* Alinear mejor las etiquetas */
}

.info-photo {
  margin-top: 10px; /* Reducido de 12px a 10px */
  margin-bottom: 10px; /* Reducido de 12px a 10px */
  text-align: center;
}

.info-photo img {
  width: 100%;
  max-height: 150px; /* Reducido de 180px a 150px */
  object-fit: cover;
  border-radius: 6px; /* Reducido de 8px a 6px */
  cursor: pointer;
  transition: transform 0.2s;
}

.info-photo img:hover {
  transform: scale(1.02);
}

.panel-actions {
  display: flex;
  gap: 6px; /* Reducido de 8px a 6px */
  margin-top: 10px; /* Reducido de 12px a 10px */
  flex-wrap: wrap;
}

.action-btn {
  flex: 1;
  padding: 6px 8px; /* Reducido de 8px 10px */
  border: none;
  border-radius: 4px; /* Reducido de 6px a 4px */
  cursor: pointer;
  font-size: 11px; /* Reducido de 13px a 11px */
  font-weight: 500;
  transition: all 0.2s;
  min-width: 80px; /* Reducido de 100px a 80px */
}

.center-btn {
  background: #3498db;
  color: white;
}

.center-btn:hover {
  background: #2980b9;
}

.view-btn {
  background: #4CAF50;
  color: white;
}

.view-btn:hover {
  background: #45a049;
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
  z-index: 1000;
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
  background: white;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  width: 12px;
  height: 12px;
}

/* Posicionamiento mejorado del tip (punta del popup) */
:global(.modern-popup-container.centered-popup .leaflet-popup-tip) {
  left: 50% !important;
  margin-left: -6px !important;
}

:global(.modern-popup-container .leaflet-container a.leaflet-popup-close-button) {
  top: 12px;
  right: 12px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 22px;
  width: 28px;
  height: 28px;
  line-height: 28px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 50%;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  z-index: 1001;
}

:global(.modern-popup-container .leaflet-container a.leaflet-popup-close-button:hover) {
  background: rgba(255, 255, 255, 0.9);
  color: #333;
  transform: scale(1.1) rotate(90deg);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
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
  padding: 18px 22px 14px;
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
  padding: 10px 18px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);
  backdrop-filter: blur(10px);
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

/* Responsive mejorado para popup moderno */
@media (max-width: 1024px) {
  .registro-info-panel {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    right: auto;
    width: 90%;
    max-width: 400px;
    max-height: 80vh;
    z-index: 2000;
    border-radius: 16px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  }
  
  :global(.modern-popup-container .leaflet-popup-content) {
    width: 280px !important;
  }
  
  :global(.modern-marker-popup) {
    min-width: 260px;
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
    max-height: 85vh;
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

/* Estilos adicionales para mejorar la experiencia */

/* Overlay para dispositivos móviles cuando el panel está abierto */
@media (max-width: 1024px) {
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
  }
}

@keyframes fadeInOverlay {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
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
