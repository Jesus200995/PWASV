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
          
          <div id="mapa-principal" class="mapa-container"></div>
          
          <div class="map-legend">
            <h3>Leyenda</h3>
            <div class="legend-item">
              <span class="legend-marker regular"></span>
              <span>Registro regular</span>
            </div>
            <div class="legend-item">
              <span class="legend-marker critical"></span>
              <span>Punto crítico</span>
            </div>
            <div class="legend-item">
              <span class="legend-marker selected"></span>
              <span>Seleccionado</span>
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
            </div>
            <div class="info-row">
              <strong>Ubicación:</strong> {{ formatCoordenadas(registroSeleccionado.latitud, registroSeleccionado.longitud) }}
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
    registros.value = await usuariosService.enriquecerRegistrosConUsuarios(registrosRaw)
    
    if (mapInitialized.value) {
      actualizarMarcadores()
    } else {
      inicializarMapa()
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

// Inicializar el mapa
const inicializarMapa = () => {
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
    actualizarMarcadores()
    
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
const actualizarMarcadores = () => {
  if (!map || !markersLayer) return
  
  // Limpiar marcadores existentes
  markersLayer.clearLayers()
  markers = []
  
  // Filtrar registros según criterios
  const registrosFiltrados = filtrarRegistros()
  
  // Crear nuevos marcadores
  registrosFiltrados.forEach(registro => {
    try {
      const lat = parseFloat(registro.latitud)
      const lng = parseFloat(registro.longitud)
      
      if (isNaN(lat) || isNaN(lng)) return
      
      // Determinar el tipo de marcador (normal o crítico)
      const esCritico = Math.random() < 0.3 // Solo para demo, deberías tener un criterio real
      const iconColor = esCritico ? '#e74c3c' : '#4CAF50'
      const iconSize = esCritico ? [32, 32] : [25, 25]
      
      const customIcon = window.L.divIcon({
        className: 'custom-map-marker',
        html: `<div class="marker-pin" style="background-color: ${iconColor}; width: ${iconSize[0]}px; height: ${iconSize[1]}px;"></div>`,
        iconSize: iconSize,
        iconAnchor: [iconSize[0] / 2, iconSize[1]],
        popupAnchor: [0, -iconSize[1] / 2]
      })
      
      // Crear marcador y popup
      const marker = window.L.marker([lat, lng], { icon: customIcon })
        .bindPopup(`
          <div class="marker-popup">
            <h3>Registro #${registro.id}</h3>
            <p><strong>Usuario:</strong> ${registro.usuario?.nombre_completo || `Usuario ${registro.usuario_id}`}</p>
            <p><strong>Fecha:</strong> ${formatFecha(registro.fecha_hora)}</p>
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
  actualizarMarcadores()
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
        markerElement.querySelector('.marker-pin')?.classList.remove('selected')
      }
    })
    
    if (registro.marker) {
      const markerElement = registro.marker.getElement()
      if (markerElement) {
        markerElement.querySelector('.marker-pin')?.classList.add('selected')
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
        markerElement.querySelector('.marker-pin')?.classList.remove('selected')
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
  padding: 24px 32px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h1 {
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 4px;
}

.header-content p {
  color: #7f8c8d;
  font-size: 14px;
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
  padding: 24px 32px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  height: calc(100vh - 120px);
}

/* Controles del mapa */
.map-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  background: white;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 200px;
  flex: 1;
}

.search-group {
  min-width: 300px;
  flex: 2;
}

.control-group label {
  font-weight: 500;
  color: #2c3e50;
  font-size: 14px;
}

.control-select, .control-input {
  padding: 10px 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.2s;
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
  right: 4px;
  top: 50%;
  transform: translateY(-50%);
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
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
  margin-bottom: 6px;
  font-size: 12px;
}

.legend-marker {
  display: inline-block;
  width: 16px;
  height: 16px;
  border-radius: 50%;
}

.legend-marker.regular {
  background: #4CAF50;
}

.legend-marker.critical {
  background: #e74c3c;
}

.legend-marker.selected {
  background: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.3);
}

/* Panel de información del registro seleccionado */
.registro-info-panel {
  position: fixed;
  top: 100px;
  right: 20px;
  width: 360px;
  max-width: 100%;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  z-index: 900;
  animation: slideinPanel 0.3s ease-out;
}

@keyframes slideinPanel {
  from {
    transform: translateX(420px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.panel-header {
  padding: 16px 20px;
  background: #4CAF50;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h3 {
  margin: 0;
  font-size: 18px;
}

.close-panel-btn {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  width: 30px;
  height: 30px;
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
  padding: 16px 20px;
  max-height: 60vh;
  overflow-y: auto;
}

.info-row {
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 14px;
}

.info-row:last-child {
  border-bottom: none;
}

.info-row strong {
  color: #2c3e50;
  margin-right: 6px;
}

.info-photo {
  margin-top: 16px;
  margin-bottom: 16px;
}

.info-photo img {
  width: 100%;
  height: auto;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
}

.info-photo img:hover {
  transform: scale(1.02);
}

.panel-actions {
  display: flex;
  gap: 10px;
  margin-top: 16px;
}

.action-btn {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
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
:global(.custom-map-marker) {
  background: transparent;
  border: none;
}

:global(.marker-pin) {
  width: 30px;
  height: 30px;
  border-radius: 50% 50% 50% 0;
  background: #4CAF50;
  transform: rotate(-45deg);
  animation: pulseMarker 2s infinite;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

:global(.marker-pin)::after {
  content: '';
  width: 60%;
  height: 60%;
  margin: auto;
  background: white;
  border-radius: 50%;
}

:global(.marker-pin.selected) {
  background: #3498db;
  transform: rotate(-45deg) scale(1.2);
  box-shadow: 0 0 0 4px rgba(52, 152, 219, 0.4), 0 0 15px rgba(0, 0, 0, 0.4);
  z-index: 1000;
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
    width: 320px;
  }
}

@media (max-width: 992px) {
  .control-group {
    min-width: 150px;
  }
  
  .search-group {
    min-width: 200px;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }
  
  .page-header {
    padding: 16px 20px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .page-content {
    padding: 16px 20px;
    height: auto;
  }
  
  .map-controls {
    flex-direction: column;
    gap: 12px;
  }
  
  .control-group {
    width: 100%;
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
    border-radius: 12px 12px 0 0;
    max-height: 50vh;
  }
  
  .panel-content {
    max-height: 30vh;
  }
  
  .map-legend {
    bottom: 10px;
    left: 10px;
    right: auto;
  }
}
</style>
