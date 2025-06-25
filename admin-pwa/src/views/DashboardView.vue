<template>
  <div class="dashboard-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">      <header class="dashboard-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="7" height="7"/>
                <rect x="14" y="3" width="7" height="7"/>
                <rect x="14" y="14" width="7" height="7"/>
                <rect x="3" y="14" width="7" height="7"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Panel Administrativo</h1>
              <p class="header-subtitle">Bienvenido, {{ adminUser }}</p>
            </div>
          </div>
          <div class="connection-status" :class="{ 'online': isOnline, 'offline': !isOnline }">
            <div class="status-indicator"></div>
            <span class="status-text">{{ isOnline ? 'En línea' : 'Sin conexión' }}</span>
          </div>
        </div>
      </header>

      <div class="dashboard-content">
        <!-- Estadísticas -->
        <div class="stats-grid">
          <div class="stat-card animated-card" v-for="stat in statCards" :key="stat.label">
            <div class="stat-icon svg-icon" v-html="stat.icon"></div>
            <div class="stat-info">
              <h3>{{ stat.value }}</h3>
              <p>{{ stat.label }}</p>
            </div>
          </div>
        </div>

        <!-- Registros recientes -->
        <div class="section">
          <div class="section-header">
            <h2>Registros Recientes</h2>            <button @click="cargarRegistros" class="refresh-btn" :disabled="loading">
              <svg class="refresh-icon" :class="{ spinning: loading }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="23 4 23 10 17 10"></polyline>
                <polyline points="1 20 1 14 7 14"></polyline>
                <path d="m3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
              </svg>
              {{ loading ? 'Cargando...' : 'Actualizar' }}
            </button>
          </div>
          
          <div v-if="loading && registros.length === 0" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando registros...</p>
          </div>
          
          <div v-else-if="error" class="error-container">
            <p>{{ error }}</p>
            <button @click="cargarRegistros" class="retry-btn">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
                <path d="M3 3v5h5"></path>
                <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"></path>
                <path d="M21 21v-5h-5"></path>
              </svg>
              Reintentar
            </button>
          </div>
            <div v-else-if="registros.length === 0" class="empty-state">
            <div class="empty-icon">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
              </svg>
            </div>
            <h3>No hay registros</h3>
            <p>Aún no se han creado registros en la aplicación.</p>
          </div>
          
          <div v-else class="registros-table-container">
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
              <tbody>                <tr v-for="registro in registros.slice(0, 10)" :key="registro.id">
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
                      @click="abrirFotoCompleta(registro.foto_url)"
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
                  </td>                  <td>
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

    <!-- Modal para detalles -->
    <Teleport to="body">
      <div v-if="showModal" class="modal-overlay" @click="cerrarModal">
        <div class="modal-content" @click.stop>
          <!-- Header del modal con degradado verde -->
          <div class="modal-header">
            <div class="modal-header-content">
              <div class="modal-icon">
                <svg width="18" height="18" fill="white" viewBox="0 0 24 24">
                  <path fill-rule="evenodd" d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0016.5 9h-1.875a1.875 1.875 0 01-1.875-1.875V5.25A3.75 3.75 0 009 1.5H5.625zM7.5 15a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5A.75.75 0 017.5 15zm.75 2.25a.75.75 0 000 1.5H12a.75.75 0 000-1.5H8.25z" clip-rule="evenodd"/>
                  <path d="M12.971 1.816A5.23 5.23 0 0114.25 5.25v1.875c0 .207.168.375.375.375H16.5a5.23 5.23 0 013.434 1.279 9.768 9.768 0 00-6.963-6.963z"/>
                </svg>
              </div>
              <h3 class="modal-title">
                Detalles del Registro
              </h3>
            </div>
            <button @click="cerrarModal" class="btn-close">
              <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>

          <!-- Contenido del modal -->
          <div class="modal-body">
            <!-- Vista de detalles del registro -->
            <div v-if="modalType === 'details' && selectedRecord" class="registro-detalles">
              <div class="detail-grid">
                <div class="detail-item">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">ID del Registro</span>
                    <span class="detail-value highlight">#{{ selectedRecord.id }}</span>
                  </div>
                </div>

                <div class="detail-item">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Usuario</span>
                    <span class="detail-value">{{ selectedRecord.usuario?.nombre_completo || `Usuario ${selectedRecord.usuario_id}` }}</span>
                  </div>
                </div>

                <div class="detail-item">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M1.5 8.67v8.58a3 3 0 003 3h15a3 3 0 003-3V8.67l-8.928 5.493a3 3 0 01-3.144 0L1.5 8.67z"/>
                      <path d="M22.5 6.908V6.75a3 3 0 00-3-3h-15a3 3 0 00-3 3v.158l9.714 5.978a1.5 1.5 0 001.572 0L22.5 6.908z"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Correo Electrónico</span>
                    <span class="detail-value">{{ selectedRecord.usuario?.correo || 'No disponible' }}</span>
                  </div>
                </div>

                <div class="detail-item">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path fill-rule="evenodd" d="M6.75 2.25A.75.75 0 017.5 3v1.5h9V3A.75.75 0 0118 3v1.5h.75a3 3 0 013 3v11.25a3 3 0 01-3 3H5.25a3 3 0 01-3-3V7.5a3 3 0 013-3H6V3a.75.75 0 01.75-.75zm13.5 9a1.5 1.5 0 00-1.5-1.5H5.25a1.5 1.5 0 00-1.5 1.5v7.5a1.5 1.5 0 001.5 1.5h13.5a1.5 1.5 0 001.5-1.5v-7.5z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Fecha y Hora</span>
                    <span class="detail-value">{{ formatFecha(selectedRecord.fecha_hora) }}</span>
                  </div>
                </div>

                <div class="detail-item">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path fill-rule="evenodd" d="M11.54 22.351l.07.04.028.016a.76.76 0 00.723 0l.028-.015.071-.041a16.975 16.975 0 001.144-.742 19.58 19.58 0 002.683-2.282c1.944-1.99 3.963-4.98 3.963-8.827a8.25 8.25 0 00-16.5 0c0 3.846 2.02 6.837 3.963 8.827a19.58 19.58 0 002.682 2.282 16.975 16.975 0 001.145.742zM12 13.5a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Ubicación</span>
                    <span class="detail-value location">{{ parseFloat(selectedRecord.latitud).toFixed(6) }}, {{ parseFloat(selectedRecord.longitud).toFixed(6) }}</span>
                  </div>
                </div>

                <div class="detail-item full-width">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path fill-rule="evenodd" d="M4.125 3C3.089 3 2.25 3.84 2.25 4.875V18a3 3 0 003 3h15a3 3 0 01-3-3V4.875C17.25 3.839 16.41 3 15.375 3H4.125zM12 9.75a.75.75 0 000 1.5h1.5a.75.75 0 000-1.5H12zm-.75-2.25a.75.75 0 01.75-.75h1.5a.75.75 0 010 1.5H12a.75.75 0 01-.75-.75zM6 12.75a.75.75 0 000 1.5h7.5a.75.75 0 000-1.5H6zm-.75 3.75a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5H6a.75.75 0 01-.75-.75zM6 6.75a.75.75 0 00-.75.75v3c0 .414.336.75.75.75h3a.75.75 0 00.75-.75v-3A.75.75 0 009 6.75H6z" clip-rule="evenodd"/>
                      <path d="M18.75 6.75h1.875c.621 0 1.125.504 1.125 1.125V18a1.5 1.5 0 01-3 0V6.75z"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Descripción</span>
                    <span class="detail-value description">{{ selectedRecord.descripcion || 'Sin descripción' }}</span>
                  </div>
                </div>

                <div v-if="selectedRecord.foto_url" class="detail-item full-width">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path fill-rule="evenodd" d="M1.5 6a2.25 2.25 0 012.25-2.25h16.5A2.25 2.25 0 0122.5 6v12a2.25 2.25 0 01-2.25 2.25H3.75A2.25 2.25 0 011.5 18V6zM3 16.06V18c0 .414.336.75.75.75h16.5A.75.75 0 0021 18v-1.94l-2.69-2.689a1.5 1.5 0 00-2.12 0l-.88.879.97.97a.75.75 0 11-1.06 1.06l-5.16-5.159a1.5 1.5 0 00-2.12 0L3 16.061zm10.125-7.81a1.125 1.125 0 112.25 0 1.125 1.125 0 01-2.25 0z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Fotografía</span>
                    <div class="photo-container">
                      <img 
                        :src="`${API_URL}/${selectedRecord.foto_url}`" 
                        alt="Foto del registro" 
                        class="detail-photo"
                        @click="abrirFotoCompleta(selectedRecord.foto_url)"
                      >
                    </div>
                  </div>
                </div>

                <div class="detail-item full-width">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path fill-rule="evenodd" d="M11.54 22.351l.07.04.028.016a.76.76 0 00.723 0l.028-.015.071-.041a16.975 16.975 0 001.144-.742 19.58 19.58 0 002.683-2.282c1.944-1.99 3.963-4.98 3.963-8.827a8.25 8.25 0 00-16.5 0c0 3.846 2.02 6.837 3.963 8.827a19.58 19.58 0 002.682 2.282 16.975 16.975 0 001.145.742zM12 13.5a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Mapa de Ubicación</span>
                    <div class="map-container">
                      <div id="map" class="leaflet-map"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer del modal -->
          <div class="modal-footer">
            <!-- Footer simplificado sin botón de cerrar -->
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Lightbox para ver foto en pantalla completa -->
    <Teleport to="body" v-if="showLightbox">
      <div class="lightbox-overlay" @click="cerrarLightbox">
        <div class="lightbox-container">
          <button class="lightbox-close" @click="cerrarLightbox">
            <svg width="24" height="24" fill="white" viewBox="0 0 24 24">
              <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
            </svg>
          </button>
          <img 
            :src="lightboxImageUrl" 
            alt="Fotografía en pantalla completa"
            class="lightbox-image"
            @click.stop="requestFullscreen"
          >
          <p class="lightbox-hint">Haz clic en la imagen para pantalla completa • ESC o clic fuera para cerrar</p>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Sidebar from '../components/Sidebar.vue'
import { usuariosService } from '../services/usuariosService.js'

const router = useRouter()

const API_URL = 'https://apipwa.sembrandodatos.com'
const adminUser = ref(localStorage.getItem('admin_user') || 'Admin')
const isOnline = ref(navigator.onLine)

const registros = ref([])
const usuarios = ref([])
const loading = ref(false)
const error = ref('')

const stats = reactive({
  totalRegistros: '-',
  totalUsuarios: '-',
  registrosHoy: '-'
})

const showModal = ref(false)
const modalType = ref('details')
const selectedRecord = ref(null)
const showLightbox = ref(false)
const lightboxImageUrl = ref('')

// Variable para el mapa
let map = null

const statCards = computed(() => [
  {
    label: 'Total Registros',
    value: stats.totalRegistros,
    icon: `<svg width="36" height="36" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="4" fill="#e8f5e8"/><path d="M7 17v-6m5 6V7m5 10v-3" stroke="#4CAF50" stroke-width="2" stroke-linecap="round"/></svg>`
  },
  {
    label: 'Usuarios Activos',
    value: stats.totalUsuarios,
    icon: `<svg width="36" height="36" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="4" fill="#e8f5e8"/><circle cx="12" cy="10" r="3" stroke="#4CAF50" stroke-width="2"/><path d="M6 18c0-2.21 3.58-3.5 6-3.5s6 1.29 6 3.5" stroke="#4CAF50" stroke-width="2"/></svg>`
  },
  {
    label: 'Registros Hoy',
    value: stats.registrosHoy,
    icon: `<svg width="36" height="36" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="4" fill="#e8f5e8"/><path d="M8 7h8M8 11h8m-8 4h5" stroke="#4CAF50" stroke-width="2" stroke-linecap="round"/></svg>`
  }
])

// Detectar cambios de conexión
window.addEventListener('online', () => { isOnline.value = true })
window.addEventListener('offline', () => { isOnline.value = false })

onMounted(() => {
  cargarRegistros()
  cargarUsuarios() // También cargar usuarios para estadísticas más precisas
  
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

// Event listener para cerrar lightbox con ESC
const handleKeyDown = (event) => {
  if (event.key === 'Escape' && showLightbox.value) {
    cerrarLightbox()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
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
    const registrosRaw = Array.isArray(response.data) ? response.data : (response.data.registros || [])
      // Enriquecer registros con información de usuarios reales
    registros.value = await usuariosService.enriquecerRegistrosConUsuarios(registrosRaw)
    calcularEstadisticas()
    
    console.log('Registros cargados en Dashboard:', registros.value)
  } catch (err) {
    console.error('Error al cargar registros:', err)
    if (err.response?.status === 401) {
      // Token expirado
      logout()
    } else {
      error.value = 'Error al cargar los registros: ' + (err.response?.data?.detail || err.message)
    }
  } finally {
    loading.value = false
  }
}

const cargarUsuarios = async () => {
  try {
    usuarios.value = await usuariosService.obtenerUsuarios()
    calcularEstadisticas() // Recalcular con usuarios reales
    console.log('✅ Usuarios reales cargados en Dashboard:', usuarios.value)
  } catch (err) {
    console.error('❌ Error al cargar usuarios desde la base de datos:', err)
    // Si no se pueden cargar usuarios, usar los únicos de registros
    if (registros.value.length > 0) {
      const usuariosUnicos = [...new Set(registros.value.map(r => r.usuario_id))]
      stats.totalUsuarios = usuariosUnicos.length
    }
  }
}

const calcularEstadisticas = () => {
  const totalRegistros = registros.value.length
  const totalUsuarios = usuarios.value.length // Usar usuarios reales en lugar de únicos de registros
  
  const hoy = new Date().toDateString()
  const registrosHoy = registros.value.filter(r => {
    const fechaRegistro = new Date(r.fecha_hora).toDateString()
    return fechaRegistro === hoy
  }).length
  
  stats.totalRegistros = totalRegistros
  stats.totalUsuarios = totalUsuarios
  stats.registrosHoy = registrosHoy
}

const formatFecha = (fechaStr) => {
  try {
    return new Date(fechaStr).toLocaleString('es-ES')
  } catch (e) {
    return fechaStr
  }
}

const verDetalles = async (registro) => {
  selectedRecord.value = registro
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
      .bindPopup(`Registro #${selectedRecord.value?.id}<br>Lat: ${lat}<br>Lng: ${lng}`)
      .openPopup()
  } catch (error) {
    console.error('Error al inicializar el mapa:', error)
  }
}

const abrirFotoCompleta = (fotoUrl) => {
  lightboxImageUrl.value = `${API_URL}/${fotoUrl}`
  showLightbox.value = true
}

const cerrarLightbox = () => {
  showLightbox.value = false
  lightboxImageUrl.value = ''
}

const requestFullscreen = (event) => {
  if (event.target.requestFullscreen) {
    event.target.requestFullscreen()
  }
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
.dashboard-container {
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

.dashboard-header {
  background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
  border-bottom: none;
  padding: 32px;
  color: white;
  box-shadow: 0 4px 20px rgba(46, 204, 113, 0.15);
  position: relative;
  overflow: hidden;
}

.dashboard-header::before {
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
}

.header-main {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-icon {
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: float 3s ease-in-out infinite;
}

.header-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
}

.header-text {
  flex: 1;
}

.header-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px 0;
  background: linear-gradient(45deg, #ffffff 0%, #e8f5e8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  letter-spacing: -0.5px;
}

.header-subtitle {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  font-weight: 400;
  letter-spacing: 0.2px;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
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

/* Contenido del dashboard */
.dashboard-content {
  padding: 32px 40px;
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

.refresh-btn:hover::before {
  left: 100%;
}

.refresh-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #45a049 0%, #5cb85c 50%, #45a049 100%);
  transform: translateY(-3px) scale(1.08);
  box-shadow: 
    0 12px 32px rgba(76, 175, 80, 0.5),
    0 4px 16px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
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

.dashboard-content {
  padding: 32px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
  padding: 28px;
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(76, 175, 80, 0.1), 
    0 2px 16px rgba(0,0,0,0.05),
    inset 0 1px 0 rgba(255,255,255,0.8);
  display: flex;
  align-items: center;
  gap: 24px;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  cursor: pointer;
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
  animation: fadeInUp 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  backdrop-filter: blur(10px);
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(76, 175, 80, 0.1), transparent);
  transition: left 0.6s ease;
}

.stat-card:hover::before {
  left: 100%;
}

.stat-card:hover {
  transform: translateY(-12px) scale(1.05);
  box-shadow: 
    0 20px 48px rgba(76, 175, 80, 0.2), 
    0 8px 24px rgba(0,0,0,0.12),
    inset 0 1px 0 rgba(255,255,255,0.9);
  border-color: rgba(76, 175, 80, 0.3);
  background: linear-gradient(135deg, #ffffff 0%, #f0fff0 100%);
}

.animated-card {
  opacity: 0;
  animation: fadeInUp 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}

.animated-card:nth-child(1) { animation-delay: 0.1s; }
.animated-card:nth-child(2) { animation-delay: 0.2s; }
.animated-card:nth-child(3) { animation-delay: 0.3s; }

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

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes slideInRight {
  0% { transform: translateX(30px); opacity: 0; }
  100% { transform: translateX(0); opacity: 1; }
}

.svg-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(76, 175, 80, 0.05) 100%);
  position: relative;
}

.svg-icon::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: radial-gradient(circle, rgba(76, 175, 80, 0.2) 0%, transparent 70%);
  border-radius: 50%;
  transition: all 0.4s ease;
  transform: translate(-50%, -50%);
}

.stat-card:hover .svg-icon {
  transform: scale(1.2) rotate(-8deg);
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(76, 175, 80, 0.08) 100%);
}

.stat-card:hover .svg-icon::before {
  width: 80px;
  height: 80px;
}

.stat-info h3 {
  font-size: 36px;
  color: #4CAF50;
  margin-bottom: 6px;
  font-weight: 800;
  letter-spacing: 1.5px;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
}

.stat-card:hover .stat-info h3 {
  transform: scale(1.1);
  background: linear-gradient(135deg, #388e3c 0%, #4CAF50 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: pulse 2s ease-in-out infinite;
}

.stat-info p {
  color: #666;
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-card:hover .stat-info p {
  color: #4CAF50;
  transform: translateX(4px);
}

.section {
  background: linear-gradient(135deg, #ffffff 0%, #fafffe 100%);
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.08),
    0 2px 16px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255,255,255,0.8);
  overflow: hidden;
  border: 1px solid rgba(76, 175, 80, 0.1);
  transition: all 0.3s ease;
  animation: slideInRight 0.6s ease-out;
}

.section:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 12px 40px rgba(0, 0, 0, 0.12),
    0 4px 20px rgba(0, 0, 0, 0.06),
    inset 0 1px 0 rgba(255,255,255,0.9);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px;
  border-bottom: 1px solid #e0e0e0;
}

.section-header h2 {
  color: #333;
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

.loading-container, .empty-state {
  text-align: center;
  padding: 80px 32px;
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

.error-container {
  text-align: center;
  padding: 32px;
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

.registros-table-container {
  overflow-x: auto;
  animation: fadeInUp 0.6s ease-out 0.2s both;
}

.registros-table {
  width: 100%;
  border-collapse: collapse;
  position: relative;
}

.registros-table th,
.registros-table td {
  padding: 16px 12px;
  text-align: left;
  border-bottom: 1px solid rgba(224, 224, 224, 0.6);
  transition: all 0.3s ease;
}

.registros-table th {
  background: linear-gradient(135deg, #f8f9fa 0%, #f0f8f0 100%);
  font-weight: 700;
  color: #4CAF50;
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.5px;
  position: sticky;
  top: 0;
  z-index: 10;
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
  font-size: 12px;
}

.ubicacion, .fecha {
  font-size: 12px;
  color: #666;
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

.descripcion {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
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

.btn-ver:active {
  transform: translateY(0);
  box-shadow: 0 1px 3px rgba(76, 175, 80, 0.3);
}

/* Estilos del modal mejorados */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  animation: modalFadeIn 0.3s ease-out;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    backdrop-filter: blur(0px);
  }
  to {
    opacity: 1;
    backdrop-filter: blur(4px);
  }
}

.modal-content {
  background: white;
  border-radius: 16px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
  max-width: 600px;
  width: 100%;
  max-height: 85vh;
  overflow: hidden;
  position: relative;
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    transform: translateY(30px) scale(0.95);
    opacity: 0;
  }
  to {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}

.modal-header {
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
  color: white;
  padding: 20px 24px;
  border-radius: 16px 16px 0 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

.modal-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='20' cy='20' r='1.5'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
  z-index: 1;
}

.modal-header-content {
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
  z-index: 2;
}

.modal-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.modal-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: white;
}

.btn-close {
  background: rgba(255, 255, 255, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 10px;
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 2;
}

.btn-close:hover {
  background: rgba(255, 255, 255, 0.35);
  transform: scale(1.1);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.modal-body {
  padding: 24px;
  max-height: 55vh;
  overflow-y: auto;
}

.modal-body::-webkit-scrollbar {
  width: 6px;
}

.modal-body::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.modal-body::-webkit-scrollbar-thumb {
  background: #4CAF50;
  border-radius: 3px;
}

.modal-body::-webkit-scrollbar-thumb:hover {
  background: #45a049;
}

/* Estilos para detalles del registro */
.registro-detalles {
  animation: contentFadeIn 0.4s ease-out 0.1s both;
}

@keyframes contentFadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #f8fffe 0%, #f0fff4 100%);
  border: 1px solid rgba(76, 175, 80, 0.1);
  border-radius: 10px;
  transition: all 0.2s ease;
}

.detail-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.08);
  border-color: rgba(76, 175, 80, 0.2);
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.detail-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  font-size: 12px;
  font-weight: 600;
  color: #4CAF50;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.detail-value {
  font-size: 14px;
  color: #2c3e50;
  line-height: 1.3;
  font-weight: 500;
}

.detail-value.highlight {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
  font-size: 16px;
}

.detail-value.location {
  font-family: 'Courier New', monospace;
  background: #f0f0f0;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
}

.detail-value.description {
  background: #f8f9fa;
  padding: 8px;
  border-radius: 6px;
  border-left: 3px solid #4CAF50;
  font-style: italic;
  font-size: 13px;
}

/* Estilos para fotografías */
.photo-container {
  position: relative;
  display: inline-block;
  border-radius: 12px;
  overflow: hidden;
  margin-top: 8px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.photo-container:hover {
  transform: scale(1.02);
}

.detail-photo {
  width: 100%;
  max-width: 250px;
  height: auto;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.detail-photo:hover {
  box-shadow: 0 8px 25px rgba(76, 175, 80, 0.2);
}

/* Estilos para el mapa */
.map-container {
  margin-top: 8px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.leaflet-map {
  height: 200px;
  width: 100%;
}

/* Footer del modal */
.modal-footer {
  padding: 0;
  background: transparent;
  border: none;
  height: 0;
}

/* Responsividad */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }
  
  .dashboard-content {
    padding: 16px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .modal-overlay {
    padding: 10px;
  }
  
  .modal-content {
    max-height: 95vh;
    border-radius: 12px;
  }
  
  .modal-header {
    padding: 20px;
    border-radius: 12px 12px 0 0;
  }
  
  .modal-title {
    font-size: 18px;
  }
  
  .modal-body {
    padding: 16px;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .detail-item {
    padding: 12px;
    flex-direction: row;
    align-items: flex-start;
    text-align: left;
  }
  
  .detail-icon {
    width: 28px;
    height: 28px;
  }
  
  .modal-footer {
    display: none;
  }
}

/* Estilos del Lightbox */
.lightbox-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.95);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: lightboxFadeIn 0.3s ease-out;
}

.lightbox-container {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.lightbox-close {
  position: absolute;
  top: -50px;
  right: 0;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.lightbox-close:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.lightbox-image {
  max-width: 100%;
  max-height: 80vh;
  object-fit: contain;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
  cursor: pointer;
  transition: transform 0.3s ease;
  animation: lightboxImageIn 0.4s ease-out;
}

.lightbox-image:hover {
  transform: scale(1.02);
}

.lightbox-hint {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  text-align: center;
  margin: 0;
  padding: 10px 20px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

@keyframes lightboxFadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes lightboxImageIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Responsive para lightbox */
@media (max-width: 768px) {
  .lightbox-container {
    max-width: 95vw;
    max-height: 95vh;
    gap: 15px;
  }
  
  .lightbox-close {
    top: -40px;
    width: 35px;
    height: 35px;
  }
  
  .lightbox-image {
    max-height: 75vh;
    border-radius: 8px;
  }
  
  .lightbox-hint {
    font-size: 12px;
    padding: 8px 16px;
  }
}
</style>
