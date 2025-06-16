<template>
  <div class="registros-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div>
            <h1>Gestión de Registros</h1>
            <p>Administra todos los registros de usuarios en la aplicación</p>
          </div>
          <div class="header-actions">
            <button @click="cargarRegistros" class="refresh-btn" :disabled="loading">
              <span class="refresh-icon" :class="{ spinning: loading }">🔄</span>
              {{ loading ? 'Cargando...' : 'Actualizar' }}
            </button>
          </div>
        </div>
      </header>

      <div class="page-content">
        <!-- Filtros -->
        <div class="filters-section">
          <div class="filter-box">
            <label for="usuario-filter">Filtrar por Usuario:</label>
            <select 
              id="usuario-filter"
              v-model="filtroUsuario" 
              @change="filtrarRegistros"
              class="filter-select"
            >
              <option value="">Todos los usuarios</option>
              <option v-for="usuario in usuariosDisponibles" :key="usuario" :value="usuario">
                Usuario {{ usuario }}
              </option>
            </select>
          </div>
        </div>

        <!-- Tabla de registros -->
        <div class="registros-section">
          <div v-if="loading && registros.length === 0" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando registros...</p>
          </div>
          
          <div v-else-if="error" class="error-container">
            <p>{{ error }}</p>
            <button @click="cargarRegistros" class="retry-btn">Reintentar</button>
          </div>
          
          <div v-else-if="registrosFiltrados.length === 0" class="empty-state">
            <div class="empty-icon">📭</div>
            <h3>No hay registros</h3>
            <p v-if="filtroUsuario">No se encontraron registros para Usuario {{ filtroUsuario }}</p>
            <p v-else>Aún no se han creado registros en la aplicación.</p>
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
              <tbody>
                <tr v-for="registro in registrosFiltrados" :key="registro.id">
                  <td>#{{ registro.id }}</td>
                  <td>Usuario {{ registro.usuario_id }}</td>
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
          <div v-if="modalType === 'details'" class="registro-detalles">
            <div class="details-info">
              <div><strong>ID del Registro:</strong> #{{ selectedRegistro?.id }}</div>
              <div><strong>Usuario:</strong> Usuario {{ selectedRegistro?.usuario_id }}</div>
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

const router = useRouter()

const API_URL = 'https://apipwa.sembrandodatos.com'
const registros = ref([])
const registrosFiltrados = ref([])
const usuariosDisponibles = ref([])
const loading = ref(false)
const error = ref('')
const filtroUsuario = ref('')

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
    
    registros.value = response.data.registros || []
    registrosFiltrados.value = registros.value
    
    // Extraer usuarios únicos para el filtro
    const usuarios = [...new Set(registros.value.map(r => r.usuario_id))].sort((a, b) => a - b)
    usuariosDisponibles.value = usuarios
    
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
  if (!filtroUsuario.value) {
    registrosFiltrados.value = registros.value
    return
  }
  
  registrosFiltrados.value = registros.value.filter(registro => 
    registro.usuario_id.toString() === filtroUsuario.value
  )
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
  if (confirm('¿Estás seguro de que quieres cerrar sesión?')) {
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_user')
    router.push('/login')
  }
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
}

.filters-section {
  margin-bottom: 24px;
}

.filter-box {
  display: flex;
  align-items: center;
  gap: 12px;
  background: white;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.filter-box label {
  font-weight: 500;
  color: #2c3e50;
  white-space: nowrap;
}

.filter-select {
  padding: 8px 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  min-width: 200px;
  transition: all 0.2s;
}

.filter-select:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.registros-section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.loading-container, .error-container, .empty-state {
  padding: 60px 20px;
  text-align: center;
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

.error-container {
  color: #e74c3c;
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

.empty-state {
  color: #666;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.table-container {
  overflow-x: auto;
}

.registros-table {
  width: 100%;
  border-collapse: collapse;
}

.registros-table th {
  background: #f8f9fa;
  padding: 16px 12px;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e0e0e0;
  font-size: 14px;
}

.registros-table td {
  padding: 12px;
  border-bottom: 1px solid #e0e0e0;
  font-size: 14px;
}

.registros-table tr:hover {
  background: #f8f9fa;
}

.foto-mini {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 6px;
  cursor: pointer;
  transition: transform 0.2s;
}

.foto-mini:hover {
  transform: scale(1.1);
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

.btn-ver {
  padding: 6px 12px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}

.btn-ver:hover {
  background: #45a049;
  transform: translateY(-1px);
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
  }
  
  .filter-select {
    width: 100%;
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
