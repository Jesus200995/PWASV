<template>
  <div class="notificaciones-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                <circle cx="12" cy="8" r="1" opacity="0.6"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Centro de Notificaciones</h1>
              <p class="header-subtitle">Administra y envía notificaciones a los usuarios</p>
            </div>
          </div>
          <div class="header-actions">
            <div class="connection-status" :class="{ 'online': isOnline, 'offline': !isOnline }">
              <div class="status-indicator"></div>
              <span class="status-text">{{ isOnline ? 'En línea' : 'Sin conexión' }}</span>
            </div>
            <button @click="cargarNotificaciones" class="refresh-btn" :disabled="loading">
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

      <div class="page-content">
        <!-- Panel de filtros avanzados -->
        <div class="advanced-filters">
          <!-- Filtros principales -->
          <div class="filters-main">
            <!-- Contenedor izquierdo con filtros -->
            <div class="filters-left">
              <!-- Barra de búsqueda -->
              <div class="search-box">
                <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="m21 21-4.35-4.35"></path>
                </svg>
                <input 
                  v-model="searchTerm" 
                  type="text" 
                  placeholder="Buscar notificaciones..." 
                  class="search-input"
                >
                <button v-if="searchTerm" @click="limpiarBusqueda" class="clear-search-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>
            </div>
            
            <!-- Contadores de estadísticas en el lado derecho -->
            <div class="filters-right">
              <div class="visor-stats-compact">
                <div class="compact-stat-card">
                  <div class="compact-stat-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" fill="#4CAF50" opacity="0.8"/>
                      <circle cx="12" cy="8" r="4" fill="#66BB6A" opacity="0.5"/>
                    </svg>
                  </div>
                  <div class="compact-stat-info">
                    <div class="compact-stat-value">0</div>
                    <div class="compact-stat-label">Total Notificaciones</div>
                  </div>
                </div>
                
                <div class="compact-stat-card">
                  <div class="compact-stat-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M22 17H2a3 3 0 0 0 3-3V9a7 7 0 0 1 14 0v5a3 3 0 0 0 3 3z" fill="#4CAF50" opacity="0.7"/>
                      <path d="M19 17v2a3 3 0 0 1-3 3h-8a3 3 0 0 1-3-3v-2" stroke="#4CAF50" stroke-width="2"/>
                      <circle cx="12" cy="10" r="3" fill="#66BB6A" opacity="0.7"/>
                    </svg>
                  </div>
                  <div class="compact-stat-info">
                    <div class="compact-stat-value">0</div>
                    <div class="compact-stat-label">Enviadas Hoy</div>
                  </div>
                </div>

                <div class="compact-stat-card">
                  <div class="compact-stat-icon">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke="#4CAF50" stroke-width="2" fill="none"/>
                      <circle cx="8.5" cy="7" r="4" fill="#66BB6A"/>
                      <circle cx="17" cy="11" r="6" fill="#4CAF50" opacity="0.5"/>
                      <path d="M18 8l-2 6" stroke="white" stroke-width="1.5"/>
                    </svg>
                  </div>
                  <div class="compact-stat-info">
                    <div class="compact-stat-value">0</div>
                    <div class="compact-stat-label">Usuarios Alcanzados</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Contenido principal de notificaciones -->
        <div class="notificaciones-section">
          <div v-if="loading" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando notificaciones...</p>
          </div>
          
          <div v-else class="empty-state">
            <div class="empty-icon">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                <circle cx="12" cy="8" r="1" opacity="0.6"/>
              </svg>
            </div>
            <h3>No hay notificaciones</h3>
            <p>Aún no se han configurado notificaciones en el sistema.</p>
            <button class="create-btn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="16"/>
                <line x1="8" y1="12" x2="16" y2="12"/>
              </svg>
              Crear Nueva Notificación
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import Sidebar from '../components/Sidebar.vue'

export default {
  name: 'NotificacionesView',
  components: {
    Sidebar
  },
  data() {
    return {
      loading: false,
      isOnline: navigator.onLine,
      searchTerm: ''
    }
  },
  mounted() {
    this.configurarEventosConexion()
  },
  methods: {
    cargarNotificaciones() {
      this.loading = true
      
      // Simulación de carga
      setTimeout(() => {
        this.loading = false
      }, 1000)
    },
    
    limpiarBusqueda() {
      this.searchTerm = ''
    },
    
    configurarEventosConexion() {
      window.addEventListener('online', () => {
        this.isOnline = true
      })
      
      window.addEventListener('offline', () => {
        this.isOnline = false
      })
    },
    
    logout() {
      localStorage.removeItem('admin_token')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.notificaciones-container {
  display: flex;
  min-height: 100vh;
  background-color: #f9f9f9;
}

.main-content {
  flex: 1;
  margin-left: min(220px, 18vw); /* Ajusta según el ancho del sidebar */
  padding: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow-x: hidden;
}

.page-header {
  padding: 1.5rem 2rem;
  background: linear-gradient(to right, #ffffff, #f5f5f5);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-main {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}

.header-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

.header-text {
  display: flex;
  flex-direction: column;
}

.header-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
  color: #2E7D32;
}

.header-subtitle {
  font-size: 0.95rem;
  color: #666;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.connection-status {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.connection-status.online {
  background-color: rgba(76, 175, 80, 0.1);
  color: #2E7D32;
}

.connection-status.offline {
  background-color: rgba(244, 67, 54, 0.1);
  color: #C62828;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 8px;
}

.online .status-indicator {
  background-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.3);
  animation: pulse 1.5s infinite;
}

.offline .status-indicator {
  background-color: #F44336;
  box-shadow: 0 0 0 2px rgba(244, 67, 54, 0.3);
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0.5rem 1rem;
  background: linear-gradient(to bottom, #ffffff, #f9f9f9);
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  color: #333;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-btn:hover {
  background: linear-gradient(to bottom, #f9f9f9, #f0f0f0);
  border-color: #d0d0d0;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.refresh-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.refresh-icon {
  transition: transform 0.5s ease;
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.4); }
  70% { box-shadow: 0 0 0 5px rgba(76, 175, 80, 0); }
  100% { box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
}

.page-content {
  flex: 1;
  padding: 1.5rem 2rem;
  display: flex;
  flex-direction: column;
}

.advanced-filters {
  background: #ffffff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 1.5rem;
}

.filters-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.filters-left {
  flex: 1;
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 280px;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #f9f9f9;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #4CAF50;
  background-color: #ffffff;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.clear-search-btn {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  cursor: pointer;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  width: 20px;
  height: 20px;
}

.clear-search-btn:hover {
  color: #666;
}

.filters-right {
  display: flex;
  gap: 1rem;
}

.visor-stats-compact {
  display: flex;
  gap: 1rem;
}

.compact-stat-card {
  background: linear-gradient(to bottom, #ffffff, #f9f9f9);
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 0.75rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 160px;
}

.compact-stat-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #f5f5f5, #ffffff);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.compact-stat-info {
  display: flex;
  flex-direction: column;
}

.compact-stat-value {
  font-weight: 700;
  font-size: 1.2rem;
  color: #2E7D32;
}

.compact-stat-label {
  font-size: 0.75rem;
  color: #666;
}

.notificaciones-section {
  flex: 1;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.loading-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
}

.spinner-large {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(76, 175, 80, 0.2);
  border-radius: 50%;
  border-top-color: #4CAF50;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
}

.empty-icon {
  margin-bottom: 1.5rem;
  opacity: 0.8;
}

.empty-state h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 0.5rem;
}

.empty-state p {
  color: #666;
  margin: 0 0 2rem;
  max-width: 400px;
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(to bottom, #4CAF50, #43A047);
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
  transition: all 0.2s ease;
}

.create-btn:hover {
  background: linear-gradient(to bottom, #43A047, #388E3C);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.create-btn:active {
  transform: translateY(-1px);
}

/* Responsive styles */
@media (max-width: 1200px) {
  .filters-main {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filters-right {
    width: 100%;
    margin-top: 1rem;
  }
  
  .visor-stats-compact {
    width: 100%;
    justify-content: space-between;
  }
  
  .compact-stat-card {
    min-width: 0;
    flex: 1;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 60px; /* Ajustar para sidebar colapsado */
  }
  
  .page-header {
    padding: 1rem;
  }
  
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .header-icon {
    width: 40px;
    height: 40px;
  }
  
  .header-icon svg {
    width: 20px;
    height: 20px;
  }
  
  .header-title {
    font-size: 1.5rem;
  }
  
  .page-content {
    padding: 1rem;
  }
  
  .advanced-filters {
    padding: 1rem;
  }
  
  .filters-left {
    width: 100%;
  }
  
  .search-box {
    width: 100%;
  }
  
  .visor-stats-compact {
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .compact-stat-card {
    padding: 0.5rem;
    min-width: calc(50% - 0.5rem);
  }
  
  .notificaciones-section {
    padding: 1rem;
  }
  
  .empty-state {
    padding: 2rem 1rem;
  }
}

@media (max-width: 480px) {
  .compact-stat-card {
    min-width: 100%;
    margin-bottom: 0.5rem;
  }
  
  .header-main {
    width: 100%;
  }
  
  .header-title {
    font-size: 1.3rem;
  }
  
  .header-subtitle {
    font-size: 0.8rem;
  }
  
  .create-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
