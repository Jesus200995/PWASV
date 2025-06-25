<template>
  <div class="registros-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div>
            <h1>Gestión de Registros</h1>
            <p>Administra todos los registros de usuarios en la aplicación</p>
          </div>          <div class="header-actions">
            <button @click="cargarRegistros" class="refresh-btn" :disabled="loading">
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

      <div class="page-content">        <!-- Filtros -->
        <div class="filters-section">
          <div class="filter-box">
            <div class="filter-group">
              <label for="usuario-filter">Filtrar por Usuario:</label>
              <select 
                id="usuario-filter"
                v-model="filtroUsuario" 
                @change="filtrarRegistros"
                class="filter-select"
              >
                <option value="">Todos los usuarios</option>
                <option v-for="usuario in usuariosDisponibles" :key="usuario.id" :value="usuario.id">
                  {{ usuario.nombre_completo || `Usuario ${usuario.id}` }}
                </option>
              </select>
            </div>
            
            <div class="filter-group">
              <label for="search-input">Buscar Usuario:</label>
              <div class="search-container">
                <input
                  id="search-input"
                  v-model="searchQuery"
                  type="text"
                  placeholder="Buscar por nombre o correo..."
                  class="search-input"
                  @input="buscarUsuarios"
                />
                <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="m21 21-4.35-4.35"></path>
                </svg>
                <button 
                  v-if="searchQuery" 
                  @click="limpiarBusqueda" 
                  class="clear-search"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>        <!-- Tabla de registros -->
        <div class="registros-section">
          <!-- Información de filtros activos -->
          <div v-if="(filtroUsuario || searchQuery) && registrosFiltrados.length > 0" class="filter-info">
            <span class="filter-badge">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
              </svg>
              Mostrando {{ registrosFiltrados.length }} de {{ registros.length }} registros
              <span v-if="filtroUsuario"> • Filtrado por usuario</span>
              <span v-if="searchQuery"> • Búsqueda: "{{ searchQuery }}"</span>
            </span>
          </div>
            <div v-if="loading && registros.length === 0" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando registros...</p>
          </div>
          
          <div v-else-if="error" class="error-container">
            <p>{{ error }}</p>
            <button @click="cargarRegistros" class="retry-btn">Reintentar</button>
          </div>
          
          <div v-else-if="registros.length === 0 && !loading" class="empty-state">
            <div class="empty-icon">📭</div>
            <h3>No hay registros</h3>
            <p>Aún no se han creado registros en la aplicación.</p>
          </div>
          
          <div v-else-if="registrosFiltrados.length === 0 && registros.length > 0" class="empty-state">
            <div class="empty-icon">�</div>
            <h3>Sin resultados</h3>
            <p v-if="filtroUsuario && searchQuery">
              No se encontraron registros para el usuario seleccionado que coincidan con "{{ searchQuery }}"
            </p>
            <p v-else-if="filtroUsuario">
              No se encontraron registros para {{ usuariosDisponibles.find(u => u.id.toString() === filtroUsuario.toString())?.nombre_completo || `Usuario ${filtroUsuario}` }}
            </p>
            <p v-else-if="searchQuery">
              No se encontraron registros que coincidan con "{{ searchQuery }}"
            </p>
            <button @click="limpiarFiltros" class="retry-btn" style="background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 6h18M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6m3 0V4c0-1 1-2 2-2h4c0 1 1 2 2 2v2"></path>
              </svg>
              Limpiar Filtros
            </button>
          </div>
          
          <div v-else class="table-container">
            <table class="registros-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Usuario</th>
                  <th>Foto</th>
                  <th>Ubicación</th>
                  <th>Descripción</th>
                  <th>Fecha</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>                <tr v-for="registro in registrosFiltrados" :key="registro.id">
                  <td>#{{ registro.id }}</td>
                  <td>
                    <div class="usuario-info">
                      <strong>{{ registro.usuario?.nombre_completo || `Usuario ${registro.usuario_id}` }}</strong>
                      <small>{{ registro.usuario?.correo || 'No disponible' }}</small>
                    </div>
                  </td>
                  <td>
                    <img 
                      v-if="registro.foto_url" 
                      :src="`${API_URL}/${registro.foto_url}`"
                      alt="Foto" 
                      class="foto-mini"
                      @click="verFoto(`${API_URL}/${registro.foto_url}`)"
                    >
                    <span v-else class="no-foto">Sin foto</span>
                  </td>
                  <td class="ubicacion">
                    {{ parseFloat(registro.latitud).toFixed(6) }},<br>
                    {{ parseFloat(registro.longitud).toFixed(6) }}
                  </td>
                  <td class="descripcion">
                    {{ registro.descripcion || 'Sin descripción' }}
                  </td>
                  <td class="fecha">
                    {{ formatFecha(registro.fecha_hora) }}
                  </td>
                  <td>
                    <button @click="verDetalles(registro)" class="btn-ver">
                      Ver Detalles
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal para detalles con mapa -->
    <div v-if="showModal" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content modal-large" @click.stop>
        <div class="modal-header">
          <h3>{{ modalTitle }}</h3>
          <button @click="cerrarModal" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <div v-if="modalType === 'details'" class="registro-detalles">            <div class="details-info">
              <div><strong>ID del Registro:</strong> #{{ selectedRegistro?.id }}</div>
              <div><strong>Usuario:</strong> {{ selectedRegistro?.usuario?.nombre_completo || `Usuario ${selectedRegistro?.usuario_id}` }}</div>
              <div><strong>Correo:</strong> {{ selectedRegistro?.usuario?.correo || 'No disponible' }}</div>
              <div><strong>Fecha y Hora:</strong> {{ formatFecha(selectedRegistro?.fecha_hora) }}</div>
              <div><strong>Descripción:</strong> {{ selectedRegistro?.descripcion || 'Sin descripción' }}</div>
              <div v-if="selectedRegistro?.foto_url">
                <strong>Fotografía:</strong><br>
                <img 
                  :src="`${API_URL}/${selectedRegistro.foto_url}`" 
                  alt="Foto del registro" 
                  class="detail-photo"
                >
              </div>
            </div>
            <div class="map-container">
              <div id="map" class="leaflet-map"></div>
            </div>
          </div>
          <div v-else-if="modalType === 'photo'" class="photo-modal">
            <img :src="selectedPhotoUrl" alt="Fotografía del registro" class="full-photo">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Sidebar from '../components/Sidebar.vue'
import { usuariosService } from '../services/usuariosService.js'

const router = useRouter()

const API_URL = 'https://apipwa.sembrandodatos.com'
const registros = ref([])
const registrosFiltrados = ref([])
const usuariosDisponibles = ref([])
const loading = ref(false)
const error = ref('')
const filtroUsuario = ref('')
const searchQuery = ref('')
const searchTimeout = ref(null)

const showModal = ref(false)
const modalTitle = ref('')
const modalType = ref('')
const selectedRegistro = ref(null)
const selectedPhotoUrl = ref('')

let map = null

onMounted(() => {
  cargarRegistros()
  // Cargar Leaflet desde CDN
  if (!window.L) {
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
    document.head.appendChild(link)
    
    const script = document.createElement('script')
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
    document.head.appendChild(script)
  }
})

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
    const registrosRaw = Array.isArray(response.data) ? response.data : (response.data.registros || [])    // Enriquecer registros con información de usuarios
    registros.value = await usuariosService.enriquecerRegistrosConUsuarios(registrosRaw)
    console.log('Registros cargados:', registros.value.length)
    aplicarFiltros() // Usar la nueva función de filtros
    
    // Extraer usuarios únicos para el filtro (con información completa)
    const usuariosUnicos = []
    const usuariosVistos = new Set()
    
    registros.value.forEach(registro => {
      if (!usuariosVistos.has(registro.usuario_id)) {
        usuariosVistos.add(registro.usuario_id)
        usuariosUnicos.push({
          id: registro.usuario_id,
          nombre_completo: registro.usuario?.nombre_completo || `Usuario ${registro.usuario_id}`
        })
      }
    })    
    usuariosDisponibles.value = usuariosUnicos.sort((a, b) => a.id - b.id)
    
    console.log('Registros enriquecidos cargados:', {
      total: registros.value.length,
      filtrados: registrosFiltrados.value.length,
      usuarios: usuariosDisponibles.value.length
    })
    
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

const filtrarRegistros = () => {
  aplicarFiltros()
}

const buscarUsuarios = () => {
  // Limpiar timeout anterior
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }
  
  // Aplicar búsqueda con debounce de 300ms
  searchTimeout.value = setTimeout(() => {
    aplicarFiltros()
  }, 300)
}

const limpiarBusqueda = () => {
  searchQuery.value = ''
  aplicarFiltros()
}

const limpiarFiltros = () => {
  filtroUsuario.value = ''
  searchQuery.value = ''
  aplicarFiltros()
}

const aplicarFiltros = () => {
  let registrosFiltradosTemp = [...registros.value] // Crear copia para evitar mutaciones
  
  // Filtrar por usuario seleccionado
  if (filtroUsuario.value) {
    registrosFiltradosTemp = registrosFiltradosTemp.filter(registro => 
      registro.usuario_id.toString() === filtroUsuario.value.toString()
    )
  }
  
  // Filtrar por búsqueda de texto
  if (searchQuery.value && searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    registrosFiltradosTemp = registrosFiltradosTemp.filter(registro => {
      const nombreCompleto = (registro.usuario?.nombre_completo || '').toLowerCase()
      const correo = (registro.usuario?.correo || '').toLowerCase()
      const descripcion = (registro.descripcion || '').toLowerCase()
      
      return nombreCompleto.includes(query) || 
             correo.includes(query) || 
             descripcion.includes(query)
    })
  }
  
  registrosFiltrados.value = registrosFiltradosTemp
  console.log('Filtros aplicados:', {
    total: registros.value.length,
    filtrados: registrosFiltradosTemp.length,
    filtroUsuario: filtroUsuario.value,
    searchQuery: searchQuery.value
  })
}

const formatFecha = (fechaStr) => {
  try {
    return new Date(fechaStr).toLocaleString('es-ES')
  } catch (e) {
    return fechaStr
  }
}

const verDetalles = async (registro) => {
  selectedRegistro.value = registro
  modalTitle.value = 'Detalles del Registro'
  modalType.value = 'details'
  showModal.value = true
  
  // Esperar a que el modal se renderice
  await nextTick()
  
  // Inicializar el mapa
  setTimeout(() => {
    initMap(registro.latitud, registro.longitud)
  }, 100)
}

const initMap = (lat, lng) => {
  if (map) {
    map.remove()
  }
  
  const mapElement = document.getElementById('map')
  if (!mapElement) return
  
  // Verificar que Leaflet esté cargado
  if (!window.L) {
    console.error('Leaflet no está cargado')
    return
  }
  
  try {
    map = window.L.map('map').setView([parseFloat(lat), parseFloat(lng)], 15)
    
    window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map)
    
    window.L.marker([parseFloat(lat), parseFloat(lng)])
      .addTo(map)
      .bindPopup(`Registro #${selectedRegistro.value?.id}<br>Lat: ${lat}<br>Lng: ${lng}`)
      .openPopup()
  } catch (error) {
    console.error('Error al inicializar el mapa:', error)
  }
}

const verFoto = (fotoUrl) => {
  selectedPhotoUrl.value = fotoUrl
  modalTitle.value = 'Fotografía del Registro'
  modalType.value = 'photo'
  showModal.value = true
}

const cerrarModal = () => {
  showModal.value = false
  if (map) {
    map.remove()
    map = null
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
.registros-container {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  margin-left: 280px;
  background: linear-gradient(135deg, #f8f9fa 0%, #f0fff0 100%);
  min-height: 100vh;
  position: relative;
}

.page-header {
  background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
  border-bottom: 1px solid rgba(76, 175, 80, 0.1);
  padding: 32px 40px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.05);
  position: relative;
  overflow: hidden;
}

.page-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #4CAF50, #66BB6A, #4CAF50);
  animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
  0%, 100% { opacity: 0.7; }
  50% { opacity: 1; }
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h1 {
  font-size: 28px;
  color: #333;
  margin-bottom: 4px;
}

.header-content p {
  color: #666;
  font-size: 14px;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 50%, #4CAF50 100%);
  color: white;
  border: none;
  padding: 14px 24px;
  border-radius: 50px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 700;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 
    0 6px 20px rgba(76, 175, 80, 0.35),
    0 2px 8px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  min-width: 140px;
  justify-content: center;
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
  padding: 32px;
}

.filters-section {
  background: linear-gradient(135deg, #ffffff 0%, #fafffe 100%);
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.08),
    0 2px 16px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255,255,255,0.8);
  border: 1px solid rgba(76, 175, 80, 0.1);
  margin-bottom: 24px;
  padding: 24px;
  transition: all 0.3s ease;
}

.filters-section:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 12px 40px rgba(0, 0, 0, 0.12),
    0 4px 20px rgba(0, 0, 0, 0.06),
    inset 0 1px 0 rgba(255,255,255,0.9);
}

.filter-box {
  display: flex;
  align-items: flex-start;
  gap: 32px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 250px;
}

.filter-box label {
  font-weight: 600;
  color: #4CAF50;
  white-space: nowrap;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-size: 13px;
  min-width: fit-content;
}

.search-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  padding: 12px 48px 12px 20px;
  border: 2px solid rgba(76, 175, 80, 0.2);
  border-radius: 50px;
  font-size: 14px;
  width: 100%;
  min-width: 250px;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.1);
  font-weight: 500;
  color: #333;
}

.search-input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.25);
  transform: translateY(-1px);
}

.search-input:hover {
  border-color: rgba(76, 175, 80, 0.4);
  box-shadow: 0 3px 12px rgba(76, 175, 80, 0.15);
}

.search-input::placeholder {
  color: #999;
  font-style: italic;
}

.search-icon {
  position: absolute;
  right: 16px;
  color: #4CAF50;
  pointer-events: none;
  transition: all 0.3s ease;
}

.search-input:focus + .search-icon {
  color: #388E3C;
  transform: scale(1.1);
}

.clear-search {
  position: absolute;
  right: 44px;
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
  padding: 4px;
  border-radius: 50%;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
}

.clear-search:hover {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
  transform: scale(1.1);
}

.filter-select {
  padding: 12px 48px 12px 20px;
  border: 2px solid rgba(76, 175, 80, 0.2);
  border-radius: 50px;
  font-size: 14px;
  min-width: 250px;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.1);
  cursor: pointer;
  font-weight: 500;
  color: #333;
  
  /* Ocultar flecha nativa del select */
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  
  /* Agregar flecha personalizada */
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%234CAF50' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 16px center;
  background-repeat: no-repeat;
  background-size: 16px;
}

.filter-select:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.25);
  transform: translateY(-1px);
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23388E3C' stroke-linecap='round' stroke-linejoin='round' stroke-width='2.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
}

.filter-select:hover {
  border-color: rgba(76, 175, 80, 0.4);
  box-shadow: 0 3px 12px rgba(76, 175, 80, 0.15);
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23388E3C' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
}

.registros-section {
  background: linear-gradient(135deg, #ffffff 0%, #fafffe 100%);
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.08),
    0 2px 16px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255,255,255,0.8);
  border: 1px solid rgba(76, 175, 80, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
}

.registros-section:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 12px 40px rgba(0, 0, 0, 0.12),
    0 4px 20px rgba(0, 0, 0, 0.06),
    inset 0 1px 0 rgba(255,255,255,0.9);
}

.filter-info {
  padding: 16px 24px;
  border-bottom: 1px solid rgba(224, 224, 224, 0.3);
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.03) 0%, rgba(76, 175, 80, 0.01) 100%);
}

.filter-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(76, 175, 80, 0.05) 100%);
  color: #4CAF50;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  border: 1px solid rgba(76, 175, 80, 0.2);
}

.loading-container, .error-container, .empty-state {
  padding: 80px 32px;
  text-align: center;
  color: #666;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

.spinner-large {
  width: 48px;
  height: 48px;
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
  margin-top: 16px;
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
  margin-left: auto;
  margin-right: auto;
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
    0 8px 24px rgba(214, 51, 132, 0.5),    0 4px 12px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

/* Estilo específico para el botón verde de limpiar filtros */
.retry-btn[style*="background: linear-gradient(135deg, #4CAF50"]:hover {
  background: linear-gradient(135deg, #45a049 0%, #5cb85c 100%) !important;
  box-shadow: 
    0 8px 24px rgba(76, 175, 80, 0.5),
    0 4px 12px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.empty-state {
  color: #666;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.table-container {
  overflow-x: auto;
  animation: fadeInUp 0.6s ease-out 0.2s both;
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

.registros-table {
  width: 100%;
  border-collapse: collapse;
  position: relative;
}

.registros-table th {
  background: linear-gradient(135deg, #f8f9fa 0%, #f0f8f0 100%);
  padding: 16px 12px;
  text-align: left;
  font-weight: 700;
  color: #4CAF50;
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.5px;
  position: sticky;
  top: 0;
  z-index: 10;
  border-bottom: 1px solid rgba(224, 224, 224, 0.6);
}

.registros-table td {
  padding: 16px 12px;
  border-bottom: 1px solid rgba(224, 224, 224, 0.6);
  font-size: 14px;
  transition: all 0.3s ease;
}

.registros-table tbody tr {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
}

.registros-table tbody tr:hover {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.05) 0%, rgba(76, 175, 80, 0.02) 100%);
  transform: translateX(4px);
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.1);
}

.registros-table tbody tr:hover td {
  border-bottom-color: rgba(76, 175, 80, 0.2);
}

.foto-mini {
  width: 48px;
  height: 48px;
  object-fit: cover;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 2px solid rgba(76, 175, 80, 0.2);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.foto-mini:hover {
  transform: scale(1.1) rotate(2deg);
  border-color: #4CAF50;
  box-shadow: 0 8px 24px rgba(76, 175, 80, 0.3);
}

.no-foto {
  color: #999;
  font-style: italic;
  font-size: 12px;
}

.ubicacion {
  font-family: monospace;
  font-size: 12px;
}

.descripcion {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.fecha {
  white-space: nowrap;
  font-size: 12px;
}

.usuario-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.usuario-info strong {
  font-size: 14px;
  color: #2c3e50;
}

.usuario-info small {
  font-size: 12px;
  color: #666;
  font-style: italic;
}

.btn-ver {
  padding: 8px 16px;
  background: linear-gradient(135deg, #4CAF50, #43A047);
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
  white-space: nowrap;
}

.btn-ver:hover {
  background: linear-gradient(135deg, #43A047, #388E3C);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-content.modal-large {
  max-width: 900px;
  max-height: 90vh;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
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

.btn-close:hover {
  background: #f0f0f0;
  border-radius: 4px;
}

.modal-body {
  padding: 20px;
}

.registro-detalles {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.details-info div {
  margin-bottom: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.details-info div:last-child {
  border-bottom: none;
}

.detail-photo {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin-top: 10px;
}

.map-container {
  min-height: 300px;
}

.leaflet-map {
  height: 300px;
  border-radius: 8px;
}

.photo-modal {
  text-align: center;
}

.full-photo {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}

/* Responsive */
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
  }
  .filter-box {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }
  
  .filter-group {
    width: 100%;
    min-width: unset;
  }
  
  .filter-select,
  .search-input {
    width: 100%;
    min-width: unset;
    padding: 14px 48px 14px 20px;
    font-size: 16px; /* Evita el zoom en iOS */
  }
  
  .search-input {
    padding-right: 70px; /* Más espacio para iconos en móvil */
  }
  
  .table-container {
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .registros-table {
    font-size: 12px;
  }
  
  .registros-table th,
  .registros-table td {
    padding: 8px 4px;
  }
  
  .modal-content.modal-large {
    max-width: 95%;
  }
  
  .registro-detalles {
    grid-template-columns: 1fr;
  }
}
</style>
