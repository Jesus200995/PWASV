<template>
  <div class="dashboard-container">
    <!-- Sidebar Component -->
    <Sidebar 
      :is-open="sidebarOpen" 
      :active-section="activeSection"
      @toggle="toggleSidebar"
      @close="closeSidebar"
      @navigate="navigateToSection"
      @logout="handleLogout"
    />

    <!-- Overlay para móvil -->
    <div 
      v-if="sidebarOpen" 
      class="sidebar-overlay" 
      @click="closeSidebar"
    ></div>

    <!-- Contenido principal -->
    <main class="main-content">
      <!-- Header -->
      <header class="main-header">
        <div class="header-left">
          <button class="menu-toggle" @click="toggleSidebar">
            <span class="hamburger-icon">☰</span>
          </button>
          <h1 class="page-title">Panel Administrativo Sembrando Vida</h1>
        </div>
        <div class="header-right">
          <div class="user-info">
            <span class="user-avatar">👤</span>
            <span class="user-name">{{ username }}</span>
          </div>
        </div>
      </header>

      <!-- Contenido dinámico -->
      <div class="content-wrapper">
        <!-- Sección Dashboard -->
        <section v-show="activeSection === 'dashboard'" class="content-section">
          <div class="welcome-card">
            <h2>¡Bienvenido/a, {{ username }}!</h2>
            <p>Gestiona los registros de la aplicación Sembrando Vida desde aquí.</p>
            <small>Último acceso: {{ lastLogin }}</small>
          </div>

          <!-- Estadísticas principales -->
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon">📊</div>
              <div class="stat-info">
                <h3>{{ stats.totalRegistros }}</h3>
                <p>Total Registros</p>
              </div>
              <div class="stat-trend positive">
                <span>+12%</span>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">👥</div>
              <div class="stat-info">
                <h3>{{ stats.totalUsuarios }}</h3>
                <p>Usuarios Activos</p>
              </div>
              <div class="stat-trend positive">
                <span>+5%</span>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">📱</div>
              <div class="stat-info">
                <h3>{{ stats.registrosHoy }}</h3>
                <p>Registros Hoy</p>
              </div>
              <div class="stat-trend neutral">
                <span>{{ stats.registrosHoy > 0 ? '+' : '' }}{{ stats.registrosHoy }}</span>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon">🌱</div>
              <div class="stat-info">
                <h3>100%</h3>
                <p>Sistema Activo</p>
              </div>
              <div class="stat-trend positive">
                <span>Online</span>
              </div>
            </div>
          </div>

          <!-- Gráficas y resúmenes -->
          <div class="dashboard-grid">
            <div class="dashboard-card">
              <div class="card-header">
                <h3>Registros por Día</h3>
                <button class="card-action">Ver más</button>
              </div>
              <div class="card-content">
                <div class="chart-placeholder">
                  <div class="chart-icon">📈</div>
                  <p>Gráfica de registros próximamente</p>
                </div>
              </div>
            </div>

            <div class="dashboard-card">
              <div class="card-header">
                <h3>Actividad Reciente</h3>
                <button class="card-action">Ver todo</button>
              </div>
              <div class="card-content">
                <div class="activity-list">
                  <div class="activity-item">
                    <div class="activity-icon">📱</div>
                    <div class="activity-text">
                      <p>Nuevo registro creado</p>
                      <small>Hace 2 horas</small>
                    </div>
                  </div>
                  <div class="activity-item">
                    <div class="activity-icon">👥</div>
                    <div class="activity-text">
                      <p>Usuario registrado</p>
                      <small>Hace 4 horas</small>
                    </div>
                  </div>
                  <div class="activity-item">
                    <div class="activity-icon">🔧</div>
                    <div class="activity-text">
                      <p>Sistema actualizado</p>
                      <small>Hace 1 día</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Sección Registros -->
        <section v-show="activeSection === 'registros'" class="content-section">
          <div class="section-header">
            <h2>Gestión de Registros</h2>
            <button @click="loadRegistros" class="btn-refresh" :disabled="loading">
              <span class="refresh-icon" :class="{ 'rotating': loading }">🔄</span>
              {{ loading ? 'Cargando...' : 'Actualizar' }}
            </button>
          </div>
          
          <div v-if="loading" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando registros...</p>
          </div>
          
          <div v-else-if="error" class="error-message">
            {{ error }}
          </div>
          
          <div v-else-if="registros.length === 0" class="empty-state">
            <div class="empty-icon">📭</div>
            <h3>No hay registros</h3>
            <p>Aún no se han creado registros en la aplicación.</p>
          </div>
          
          <div v-else class="table-container">
            <table class="registros-tabla">
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
                <tr v-for="registro in registros" :key="registro.id">
                  <td>#{{ registro.id }}</td>
                  <td>Usuario {{ registro.usuario_id }}</td>
                  <td>
                    <img 
                      v-if="registro.foto_url" 
                      :src="`${API_URL}/${registro.foto_url}`"
                      alt="Foto" 
                      class="foto-mini"
                      @click="showModal('foto', registro)"
                    />
                    <span v-else style="color: #999;">Sin foto</span>
                  </td>
                  <td>
                    <small>{{ Number(registro.latitud).toFixed(6) }}, {{ Number(registro.longitud).toFixed(6) }}</small>
                  </td>
                  <td>
                    <div class="descripcion-cell" :title="registro.descripcion || 'Sin descripción'">
                      {{ registro.descripcion || 'Sin descripción' }}
                    </div>
                  </td>
                  <td><small>{{ formatDate(registro.fecha_hora) }}</small></td>
                  <td>
                    <button class="btn-ver" @click="showModal('detalles', registro)">
                      Ver Detalles
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Sección Usuarios -->
        <section v-show="activeSection === 'usuarios'" class="content-section">
          <div class="section-header">
            <h2>Gestión de Usuarios</h2>
            <button class="btn-primary">Agregar Usuario</button>
          </div>
          
          <div class="coming-soon">
            <div class="coming-soon-icon">🚧</div>
            <h3>Próximamente</h3>
            <p>La gestión de usuarios estará disponible en una próxima actualización.</p>
          </div>
        </section>
      </div>
    </main>

    <!-- Modal -->
    <div v-if="modal.show" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ modal.title }}</h3>
          <button @click="closeModal" class="btn-close">×</button>
        </div>
        <div class="modal-body" v-html="modal.content"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Sidebar from '../components/Sidebar.vue'

const router = useRouter()
const API_URL = 'https://apipwa.sembrandodatos.com'

// Estado reactivo
const sidebarOpen = ref(false)
const activeSection = ref('dashboard')
const loading = ref(false)
const error = ref('')
const registros = ref([])

const modal = reactive({
  show: false,
  title: '',
  content: ''
})

const stats = reactive({
  totalRegistros: 0,
  totalUsuarios: 0,
  registrosHoy: 0
})

// Computed properties
const username = computed(() => localStorage.getItem('admin_user') || 'Admin')
const lastLogin = computed(() => {
  const loginTime = localStorage.getItem('login_time')
  return loginTime ? new Date(loginTime).toLocaleDateString('es-ES') : 'hoy'
})

// Métodos
const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const closeSidebar = () => {
  sidebarOpen.value = false
}

const navigateToSection = (section) => {
  activeSection.value = section
  closeSidebar()
  
  if (section === 'registros') {
    loadRegistros()
  }
}

const handleLogout = () => {
  if (confirm('¿Estás seguro de que quieres cerrar sesión?')) {
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_user')
    localStorage.removeItem('login_time')
    router.push('/login')
  }
}

const loadRegistros = async () => {
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
    calculateStats()
  } catch (err) {
    console.error('Error al cargar registros:', err)
    
    if (err.response?.status === 401) {
      alert('Tu sesión ha expirado. Redirigiendo al login...')
      handleLogout()
      return
    }
    
    error.value = 'Error al cargar los registros: ' + (err.response?.data?.detail || err.message)
  } finally {
    loading.value = false
  }
}

const calculateStats = () => {
  stats.totalRegistros = registros.value.length
  stats.totalUsuarios = [...new Set(registros.value.map(r => r.usuario_id))].length
  
  const hoy = new Date().toDateString()
  stats.registrosHoy = registros.value.filter(r => {
    const fechaRegistro = new Date(r.fecha_hora).toDateString()
    return fechaRegistro === hoy
  }).length
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('es-ES')
}

const showModal = (type, registro) => {
  if (type === 'foto') {
    modal.title = 'Fotografía del Registro'
    modal.content = `
      <div style="text-align: center;">
        <img src="${API_URL}/${registro.foto_url}" alt="Fotografía del registro" style="max-width: 100%; height: auto; border-radius: 8px;">
      </div>
    `
  } else if (type === 'detalles') {
    const fecha = formatDate(registro.fecha_hora)
    const fotoHtml = registro.foto_url ? 
      `<img src="${API_URL}/${registro.foto_url}" alt="Foto del registro" style="max-width: 100%; height: auto; border-radius: 8px; margin-top: 10px;">` : 
      'No disponible'
    
    modal.title = 'Detalles del Registro'
    modal.content = `
      <div style="display: grid; gap: 20px;">
        <div><strong>ID del Registro:</strong> #${registro.id}</div>
        <div><strong>Usuario:</strong> Usuario ${registro.usuario_id}</div>
        <div><strong>Fecha y Hora:</strong> ${fecha}</div>
        <div>
          <strong>Ubicación:</strong><br>
          Latitud: ${Number(registro.latitud).toFixed(6)}<br>
          Longitud: ${Number(registro.longitud).toFixed(6)}
        </div>
        <div><strong>Descripción:</strong><br>${registro.descripcion || 'Sin descripción'}</div>
        <div><strong>Fotografía:</strong><br>${fotoHtml}</div>
        <div>
          <strong>Ver en Google Maps:</strong><br>
          <a href="https://www.google.com/maps?q=${registro.latitud},${registro.longitud}" target="_blank" style="color: #4CAF50; text-decoration: none;">
            📍 Abrir ubicación en Google Maps
          </a>
        </div>
      </div>
    `
  }
  modal.show = true
}

const closeModal = () => {
  modal.show = false
}

// Lifecycle
onMounted(() => {
  loadRegistros()
})
</script>

<style scoped>
.dashboard-container {
  display: flex;
  min-height: 100vh;
  background: #f8fafc;
}

.sidebar-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  z-index: 999;
}

.main-content {
  flex: 1;
  margin-left: 280px;
  transition: margin-left 0.3s ease;
}

.main-header {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.menu-toggle {
  display: none;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #4a5568;
  padding: 8px;
  border-radius: 8px;
  transition: background 0.2s ease;
}

.menu-toggle:hover {
  background: #f7fafc;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f7fafc;
  padding: 8px 16px;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
}

.user-avatar {
  font-size: 16px;
}

.user-name {
  font-weight: 500;
  color: #2d3748;
  font-size: 14px;
}

.content-wrapper {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.content-section {
  width: 100%;
}

.welcome-card {
  background: linear-gradient(135deg, #4CAF50, #45a049);
  color: white;
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 32px;
  box-shadow: 0 8px 32px rgba(76, 175, 80, 0.3);
}

.welcome-card h2 {
  font-size: 28px;
  margin: 0 0 8px 0;
  font-weight: 700;
}

.welcome-card p {
  font-size: 16px;
  opacity: 0.9;
  margin: 0 0 8px 0;
}

.welcome-card small {
  font-size: 14px;
  opacity: 0.8;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  border: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(to bottom, #4CAF50, #45a049);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}

.stat-icon {
  font-size: 40px;
  background: linear-gradient(135deg, #f0fff4, #dcfce7);
  padding: 12px;
  border-radius: 12px;
  border: 1px solid #bbf7d0;
}

.stat-info {
  flex: 1;
}

.stat-info h3 {
  font-size: 36px;
  font-weight: 800;
  color: #1a202c;
  margin: 0 0 4px 0;
  line-height: 1;
}

.stat-info p {
  color: #718096;
  font-size: 14px;
  font-weight: 600;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-trend {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 12px;
  text-align: center;
}

.stat-trend.positive {
  background: #dcfce7;
  color: #166534;
}

.stat-trend.neutral {
  background: #f1f5f9;
  color: #475569;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
}

.dashboard-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  overflow: hidden;
}

.card-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
}

.card-action {
  background: none;
  border: none;
  color: #4CAF50;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: background 0.2s ease;
}

.card-action:hover {
  background: #f0fff4;
}

.card-content {
  padding: 24px;
}

.chart-placeholder {
  text-align: center;
  padding: 60px 20px;
  color: #718096;
}

.chart-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
  border-left: 3px solid #4CAF50;
}

.activity-icon {
  font-size: 20px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 6px;
}

.activity-text p {
  margin: 0 0 4px 0;
  font-weight: 500;
  color: #2d3748;
  font-size: 14px;
}

.activity-text small {
  color: #718096;
  font-size: 12px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
}

.btn-refresh {
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 15px;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
}

.btn-refresh:hover:not(:disabled) {
  background: #45a049;
}

.btn-refresh:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-icon.rotating {
  animation: spin 1s linear infinite;
}

.btn-primary {
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease;
}

.btn-primary:hover {
  background: #45a049;
}

.loading-container {
  text-align: center;
  padding: 40px;
  color: #718096;
}

.spinner-large {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  color: #e74c3c;
  background: #ffebee;
  border: 1px solid #ffcdd2;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: #718096;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.table-container {
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  overflow: hidden;
}

.registros-tabla {
  width: 100%;
  border-collapse: collapse;
}

.registros-tabla th,
.registros-tabla td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.registros-tabla th {
  background: #f7fafc;
  font-weight: 600;
  color: #4a5568;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.registros-tabla td {
  color: #2d3748;
}

.registros-tabla tbody tr:hover {
  background: #f7fafc;
}

.foto-mini {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  object-fit: cover;
  cursor: pointer;
}

.descripcion-cell {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.btn-ver {
  background: #3182ce;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 12px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.btn-ver:hover {
  background: #2c5aa0;
}

.coming-soon {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.coming-soon-icon {
  font-size: 64px;
  margin-bottom: 24px;
}

.coming-soon h3 {
  font-size: 24px;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 12px 0;
}

.coming-soon p {
  color: #718096;
  font-size: 16px;
  margin: 0;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  color: #1a202c;
  font-size: 18px;
  font-weight: 600;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #718096;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close:hover {
  color: #2d3748;
}

.modal-body {
  padding: 20px;
}

/* Responsive */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }
  
  .menu-toggle {
    display: block;
  }
  
  .sidebar-overlay {
    display: block;
  }
  
  .page-title {
    font-size: 18px;
  }
  
  .content-wrapper {
    padding: 16px;
  }
  
  .welcome-card {
    padding: 24px;
    margin-bottom: 24px;
  }
  
  .welcome-card h2 {
    font-size: 24px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .dashboard-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .section-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .main-header {
    padding: 12px 16px;
  }
  
  .header-left {
    gap: 12px;
  }
  
  .user-info {
    padding: 6px 12px;
  }
  
  .registros-tabla {
    font-size: 14px;
  }
  
  .registros-tabla th,
  .registros-tabla td {
    padding: 10px 8px;
  }
  
  .modal-content {
    margin: 20px;
    max-width: calc(100% - 40px);
  }
}
</style>
