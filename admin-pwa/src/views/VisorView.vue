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
    
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
    document.head.appendChild(link)
    
    const script = document.createElement('script')
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
    script.onload = () => {
      console.log('Leaflet cargado exitosamente')
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
        popupAnchor: [0, -iconSize[0] / 2]
      })
        // Crear marcador y popup
      const marker = window.L.marker([lat, lng], { icon: customIcon })
        .bindPopup(`
          <div class="marker-popup">
            <h3>Registro #${registro.id}</h3>
            <p><strong>Usuario:</strong> ${registro.usuario?.nombre_completo || `Usuario ${registro.usuario_id}`}</p>
            <p><strong>Fecha:</strong> ${formatFecha(registro.fecha_hora)}</p>
            <p><strong>Estado:</strong> <span class="estado-badge ${esReciente ? 'reciente' : 'antiguo'}">${esReciente ? 'Hoy' : 'Días anteriores'}</span></p>
            <p><strong>Última ubicación:</strong> Sí</p>
            <button class="popup-btn">Ver detalles</button>
          </div>
        `)
      
      // Añadir evento de click para mostrar más detalles
      marker.on('click', () => {
        mostrarDetallesRegistro(registro)
      })
      
      // Añadir evento al botón dentro del popup
      marker.on('popupopen', () => {
        setTimeout(() => {
          const btn = document.querySelector('.popup-btn')
          if (btn) {
            btn.addEventListener('click', () => {
              mostrarDetallesRegistro(registro)
            })
          }
        }, 0)
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

// Mostrar detalles de un registro
const mostrarDetallesRegistro = (registro) => {
  registroSeleccionado.value = registro
  
  // Resaltar el marcador seleccionado
  if (map && markers.length > 0) {
    markers.forEach(m => {
      const markerElement = m.getElement()
      if (markerElement) {
        const marker = markerElement.querySelector('.location-marker')
        if (marker) {
          marker.classList.remove('selected')
        }
      }
    })
    
    if (registro.marker) {
      const markerElement = registro.marker.getElement()
      if (markerElement) {
        const marker = markerElement.querySelector('.location-marker')
        if (marker) {
          marker.classList.add('selected')
        }
      }
    }
  }
}

// Cerrar panel de detalles
const cerrarDetalles = () => {
  registroSeleccionado.value = null
  
  // Quitar resaltado de todos los marcadores
  if (map && markers.length > 0) {
    markers.forEach(m => {
      const markerElement = m.getElement()
      if (markerElement) {
        const marker = markerElement.querySelector('.location-marker')
        if (marker) {
          marker.classList.remove('selected')
        }
      }
    })
  }
}

// Centrar mapa en un registro específico
const centrarMapa = (registro) => {
  if (!map) return
  
  const lat = parseFloat(registro.latitud)
  const lng = parseFloat(registro.longitud)
  
  if (!isNaN(lat) && !isNaN(lng)) {
    map.setView([lat, lng], 16)
    
    // Si hay un marcador asociado, abrir su popup
    if (registro.marker) {
      registro.marker.openPopup()
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
  background: white;
  border-bottom: 1px solid #e0e0e0;
  padding: 14px 32px; /* Reducido de 24px a 14px */
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h1 {
  font-size: 24px; /* Reducido de 28px a 24px */
  color: #2c3e50;
  margin-bottom: 2px; /* Reducido de 4px a 2px */
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
  background: white;
  padding: 8px 12px; /* Reducido padding vertical */
  border-radius: 8px; /* Reducido el border-radius */
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1); /* Sombra más sutil */
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
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

.retry-btn {
  padding: 10px 16px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 16px;
}

.mapa-container {
  flex: 1;
  width: 100%;
  min-height: 400px;
  z-index: 10;
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

/* Panel de información del registro seleccionado */
.registro-info-panel {
  position: absolute;
  top: 78px; /* Posicionado después de los controles más compactos */
  right: 16px; /* Reducido de 20px a 16px */
  width: 300px; /* Reducido de 320px a 300px */
  max-width: calc(100% - 32px); /* Espacio en ambos lados */
  max-height: calc(100% - 95px); /* Ajustado para no superponer */
  background: white;
  border-radius: 10px; /* Reducido de 12px a 10px */
  box-shadow: 0 3px 15px rgba(0, 0, 0, 0.12); /* Sombra más sutil */
  overflow: auto;
  z-index: 900;
  animation: slideinPanel 0.3s ease-out;
}

@keyframes slideinPanel {
  from {
    transform: translateX(320px); /* Ajustado al nuevo ancho */
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
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
  transform: scale(1.1);
  z-index: 100;
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

:global(.marker-popup) {
  text-align: center;
  min-width: 200px;
}

:global(.marker-popup h3) {
  margin-top: 0;
  margin-bottom: 10px;
  color: #2c3e50;
  font-size: 16px;
}

:global(.marker-popup p) {
  margin: 5px 0;
  font-size: 14px;
}

:global(.popup-btn) {
  margin-top: 10px;
  padding: 6px 12px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

:global(.popup-btn:hover) {
  background: #45a049;
}

:global(.leaflet-popup-content-wrapper) {
  border-radius: 8px;
  box-shadow: 0 3px 14px rgba(0, 0, 0, 0.2);
}

:global(.leaflet-popup-content) {
  margin: 12px 16px;
}

:global(.leaflet-container a.leaflet-popup-close-button) {
  top: 10px;
  right: 10px;
  color: #333;
}

/* Responsive */
@media (max-width: 1200px) {
  .registro-info-panel {
    width: 280px; /* Reducido de 300px a 280px */
    top: 75px; /* Ajustado para los controles más pequeños */
  }
}

@media (max-width: 992px) {
  .control-group {
    min-width: 140px; /* Reducido de 150px a 140px */
  }
  
  .search-group {
    min-width: 180px; /* Reducido de 200px a 180px */
  }
  
  .registro-info-panel {
    width: 260px; /* Reducido para pantallas medianas */
    top: 72px;
  }
  
  .map-controls {
    padding: 6px 10px; /* Aún más compacto en pantallas medianas */
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }
  
  .page-header {
    padding: 12px 16px; /* Reducido de 14px 20px */
  }
  
  .header-content {
    flex-direction: column;
    gap: 10px; /* Reducido de 12px a 10px */
    align-items: flex-start;
  }
  
  .page-content {
    padding: 10px 16px; /* Reducido de 12px 20px */
    height: auto;
  }
  
  .map-controls {
    flex-direction: column;
    gap: 8px; /* Reducido de 12px a 8px */
    padding: 8px; /* Reducido de 10px a 8px */
  }
  
  .control-group {
    width: 100%;
    min-width: auto;
  }
  
  .visor-section {
    height: 60vh;
  }
  
  .registro-info-panel {
    position: fixed;
    top: auto;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100%;
    border-radius: 10px 10px 0 0; /* Ajustado al nuevo border-radius */
    max-height: 45vh; /* Reducido de 50vh a 45vh */
  }
  
  .panel-content {
    max-height: 30vh; /* Reducido de 35vh a 30vh */
  }
  
  .map-legend {
    bottom: 8px; /* Reducido de 10px a 8px */
    left: 8px; /* Reducido de 10px a 8px */
    right: auto;
    padding: 8px; /* Reducido de 12px a 8px */
  }
}

/* Estilos para badge de última ubicación */
.ubicacion-badge {
  display: inline-block;
  font-size: 0.75rem;
  background-color: #4CAF50;
  color: white;
  padding: 2px 6px;
  border-radius: 10px;
  margin-left: 8px;
  font-weight: 500;
}

/* Estilos para las etiquetas de estado en los popups */
:global(.estado-badge) {
  display: inline-block;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 0.75rem;
  color: white;
  font-weight: 500;
}

:global(.estado-badge.reciente) {
  background-color: #4CAF50;
}

:global(.estado-badge.antiguo) {
  background-color: #FF9800;
}

/* Mejoras para badges en el panel de detalles */
.ubicacion-badge, .estado-badge {
  display: inline-block;
  font-size: 0.65rem; /* Reducido de 0.7rem a 0.65rem */
  padding: 1px 4px; /* Reducido padding horizontal */
  border-radius: 8px; /* Reducido de 10px a 8px */
  margin: 1px; /* Reducido de 2px a 1px */
  font-weight: 500;
  white-space: nowrap;
}

/* Mejoras adicionales para la compactación */
.control-input {
  padding-right: 32px; /* Ajustado para el botón más pequeño */
}

.search-wrapper .control-input {
  height: 32px; /* Asegurar altura consistente */
}
</style>
