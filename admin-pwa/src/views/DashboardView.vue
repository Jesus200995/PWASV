<template>
  <div class="dashboard-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="dashboard-header">
        <div class="header-content">
          <div>
            <h1>Panel Administrativo</h1>
            <p>Bienvenido, {{ adminUser }}</p>
          </div>
          <div class="header-actions">
            <span class="connection-status" :class="{ online: isOnline, offline: !isOnline }">
              {{ isOnline ? '🟢 Conectado' : '🔴 Sin conexión' }}
            </span>
          </div>
        </div>
      </header>

      <div class="dashboard-content">
        <!-- Estadísticas -->
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-info">
              <h3>{{ stats.totalRegistros }}</h3>
              <p>Total Registros</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">👥</div>
            <div class="stat-info">
              <h3>{{ stats.totalUsuarios }}</h3>
              <p>Usuarios Activos</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">📱</div>
            <div class="stat-info">
              <h3>{{ stats.registrosHoy }}</h3>
              <p>Registros Hoy</p>
            </div>
          </div>
        </div>

        <!-- Registros recientes -->
        <div class="section">
          <div class="section-header">
            <h2>Registros Recientes</h2>
            <button @click="cargarRegistros" class="refresh-btn" :disabled="loading">
              <span class="refresh-icon" :class="{ spinning: loading }">🔄</span>
              {{ loading ? 'Cargando...' : 'Actualizar' }}
            </button>
          </div>
          
          <div v-if="loading && registros.length === 0" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando registros...</p>
          </div>
          
          <div v-else-if="error" class="error-container">
            <p>{{ error }}</p>
            <button @click="cargarRegistros" class="retry-btn">Reintentar</button>
          </div>
          
          <div v-else-if="registros.length === 0" class="empty-state">
            <div class="empty-icon">📭</div>
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
    <div v-if="showModal" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ modalTitle }}</h3>
          <button @click="cerrarModal" class="btn-close">×</button>
        </div>
        <div class="modal-body" v-html="modalContent"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
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
const modalTitle = ref('')
const modalContent = ref('')

// Detectar cambios de conexión
window.addEventListener('online', () => { isOnline.value = true })
window.addEventListener('offline', () => { isOnline.value = false })

onMounted(() => {
  cargarRegistros()
  cargarUsuarios() // También cargar usuarios para estadísticas más precisas
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

const verDetalles = (registro) => {
  // Redirigir a la vista de registros para ver el detalle completo con mapa
  router.push('/registros')
}

const verFoto = (fotoUrl) => {
  modalTitle.value = 'Fotografía del Registro'
  modalContent.value = `
    <div style="text-align: center;">
      <img src="${fotoUrl}" alt="Fotografía del registro" style="max-width: 100%; height: auto; border-radius: 8px;">
    </div>
  `
  showModal.value = true
}

const cerrarModal = () => {
  showModal.value = false
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
  margin-left: 280px; /* Actualizado para el nuevo ancho */
  background: #f8f9fa;
}

.dashboard-header {
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
  color: #333;
  margin-bottom: 4px;
}

.header-content p {
  color: #666;
  font-size: 14px;
}

.connection-status {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.connection-status.online {
  background: #e8f5e8;
  color: #2e7d2e;
}

.connection-status.offline {
  background: #fdeaea;
  color: #d63384;
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
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  font-size: 32px;
  background: #f0f8f0;
  padding: 12px;
  border-radius: 8px;
}

.stat-info h3 {
  font-size: 28px;
  color: #4CAF50;
  margin-bottom: 4px;
}

.stat-info p {
  color: #666;
  font-size: 14px;
}

.section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
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
  gap: 8px;
  background: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.refresh-btn:hover:not(:disabled) {
  background: #45a049;
}

.refresh-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-container, .empty-state {
  text-align: center;
  padding: 64px 32px;
  color: #666;
}

.spinner-large {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.error-container {
  text-align: center;
  padding: 32px;
  color: #d63384;
}

.retry-btn {
  background: #d63384;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 16px;
}

.registros-table-container {
  overflow-x: auto;
}

.registros-table {
  width: 100%;
  border-collapse: collapse;
}

.registros-table th,
.registros-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

.registros-table th {
  background: #f8f9fa;
  font-weight: 600;
  color: #333;
}

.foto-mini {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 4px;
  cursor: pointer;
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
  background: #007bff;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.btn-ver:hover {
  background: #0056b3;
}

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
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 600px;
  max-height: 80vh;
  width: 100%;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 24px;
  overflow: auto;
  max-height: calc(80vh - 120px);
}

/* Responsive */
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
}
</style>

<style>
.registro-detalles > div {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.registro-detalles > div:last-child {
  border-bottom: none;
}
</style>
