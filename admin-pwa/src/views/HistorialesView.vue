<template>
  <div class="historiales-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Gestión de Historiales</h1>
              <p class="header-subtitle">Administra todos los historiales registrados en la aplicación</p>
            </div>
          </div>
          <div class="header-actions">
            <div class="connection-status" :class="{ 'online': isOnline, 'offline': !isOnline }">
              <div class="status-indicator"></div>
              <span class="status-text">{{ isOnline ? 'En línea' : 'Sin conexión' }}</span>
            </div>
            <button @click="cargarHistoriales" class="refresh-btn" :disabled="loading">
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
        <!-- Búsqueda y Filtros -->
        <div class="search-section">
          <div class="controls-row">
            <!-- Barra de búsqueda -->
            <div class="search-group">
              <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.35-4.35"></path>
              </svg>
              <input 
                v-model="searchTerm" 
                type="text" 
                placeholder="Buscar historiales..." 
                class="search-input"
                @input="filtrarHistoriales"
              >
            </div>

            <!-- Ordenamiento -->
            <div class="sort-group">
              <label>Ordenar:</label>
              <div class="sort-buttons">
                <button 
                  @click="ordenarPor('id')"
                  :class="['sort-btn', { active: campoOrdenamiento === 'id' }]"
                  title="Ordenar por ID"
                >
                  ID
                  <svg v-if="campoOrdenamiento === 'id'" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path v-if="direccionOrdenamiento === 'asc'" d="m7 15 5 5 5-5"/>
                    <path v-else d="m7 9 5-5 5 5"/>
                  </svg>
                </button>
                <button 
                  @click="ordenarPor('fecha')"
                  :class="['sort-btn', { active: campoOrdenamiento === 'fecha' }]"
                  title="Ordenar por Fecha"
                >
                  Fecha
                  <svg v-if="campoOrdenamiento === 'fecha'" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path v-if="direccionOrdenamiento === 'asc'" d="m7 15 5 5 5-5"/>
                    <path v-else d="m7 9 5-5 5 5"/>
                  </svg>
                </button>
                <button 
                  @click="ordenarPor('tipo')"
                  :class="['sort-btn', { active: campoOrdenamiento === 'tipo' }]"
                  title="Ordenar por Tipo"
                >
                  Tipo
                  <svg v-if="campoOrdenamiento === 'tipo'" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path v-if="direccionOrdenamiento === 'asc'" d="m7 15 5 5 5-5"/>
                    <path v-else d="m7 9 5-5 5 5"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Tabla de historiales -->
        <div class="historiales-section">
          <div v-if="loading && historiales.length === 0" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando historiales...</p>
          </div>
          
          <div v-else-if="error" class="error-container">
            <p>{{ error }}</p>
            <button @click="cargarHistoriales" class="retry-btn">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
                <path d="M3 3v5h5"></path>
                <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"></path>
                <path d="M21 21v-5h-5"></path>
              </svg>
              Reintentar
            </button>
          </div>

          <div v-else-if="historialesFiltrados.length === 0" class="empty-state">
            <div class="empty-icon">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <h3>No hay historiales disponibles</h3>
            <p>Aún no se han registrado historiales en el sistema o no coinciden con la búsqueda.</p>
          </div>

          <div v-else class="welcome-section">
            <div class="welcome-card">
              <div class="welcome-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <h2>Sección de Historiales</h2>
              <p>Esta sección está disponible para la gestión de historiales del sistema. Próximamente se agregarán más funcionalidades.</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { useRouter } from 'vue-router'

export default {
  name: 'HistorialesView',
  components: {
    Sidebar
  },
  setup() {
    const router = useRouter()
    const isOnline = ref(navigator.onLine)
    const loading = ref(false)
    const error = ref('')
    const historiales = ref([])
    const searchTerm = ref('')
    const campoOrdenamiento = ref('id')
    const direccionOrdenamiento = ref('desc')

    const adminUser = computed(() => {
      const userData = localStorage.getItem('userData')
      if (userData) {
        const user = JSON.parse(userData)
        return user.nombre || 'Administrador'
      }
      return 'Administrador'
    })

    const historialesFiltrados = computed(() => {
      let resultado = [...historiales.value]
      
      // Aplicar búsqueda
      if (searchTerm.value.trim()) {
        const termino = searchTerm.value.toLowerCase().trim()
        resultado = resultado.filter(historial => 
          historial.id.toString().includes(termino) ||
          historial.tipo?.toLowerCase().includes(termino) ||
          historial.descripcion?.toLowerCase().includes(termino)
        )
      }
      
      // Aplicar ordenamiento
      resultado.sort((a, b) => {
        let valorA = a[campoOrdenamiento.value]
        let valorB = b[campoOrdenamiento.value]
        
        if (campoOrdenamiento.value === 'fecha') {
          valorA = new Date(valorA)
          valorB = new Date(valorB)
        }
        
        if (direccionOrdenamiento.value === 'asc') {
          return valorA > valorB ? 1 : -1
        } else {
          return valorA < valorB ? 1 : -1
        }
      })
      
      return resultado
    })

    const cargarHistoriales = async () => {
      loading.value = true
      error.value = ''
      try {
        // Aquí se implementará la lógica para cargar historiales
        await new Promise(resolve => setTimeout(resolve, 1000)) // Simulación
        // historiales.value = await api.getHistoriales()
        console.log('Historiales cargados')
      } catch (err) {
        console.error('Error al cargar historiales:', err)
        error.value = 'Error al cargar los historiales. Por favor, inténtalo de nuevo.'
      } finally {
        loading.value = false
      }
    }

    const filtrarHistoriales = () => {
      // La lógica de filtrado está en el computed historialesFiltrados
    }

    const ordenarPor = (campo) => {
      if (campoOrdenamiento.value === campo) {
        direccionOrdenamiento.value = direccionOrdenamiento.value === 'asc' ? 'desc' : 'asc'
      } else {
        campoOrdenamiento.value = campo
        direccionOrdenamiento.value = 'asc'
      }
    }

    const logout = () => {
      localStorage.removeItem('userData')
      localStorage.removeItem('token')
      router.push('/login')
    }

    const updateOnlineStatus = () => {
      isOnline.value = navigator.onLine
    }

    onMounted(() => {
      window.addEventListener('online', updateOnlineStatus)
      window.addEventListener('offline', updateOnlineStatus)
      cargarHistoriales()
    })

    return {
      isOnline,
      loading,
      error,
      historiales,
      historialesFiltrados,
      searchTerm,
      campoOrdenamiento,
      direccionOrdenamiento,
      adminUser,
      cargarHistoriales,
      filtrarHistoriales,
      ordenarPor,
      logout
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  overflow-x: hidden;
}

.historiales-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  width: 100%;
  overflow-x: hidden;
  position: relative;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: clamp(180px, 18vw, 240px);
  width: calc(100vw - clamp(180px, 18vw, 240px));
  background: linear-gradient(135deg, #f8f9fa 0%, #f0fff0 100%);
  min-height: 100vh;
  position: relative;
  box-sizing: border-box;
  overflow-x: hidden;
}

.page-header {
  background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
  border-bottom: none;
  padding: clamp(16px, 4vh, 32px) clamp(16px, 4vw, 32px);
  color: white;
  box-shadow: 0 4px 20px rgba(46, 204, 113, 0.15);
  position: relative;
  overflow: hidden;
  width: 100%;
  box-sizing: border-box;
}

.page-header::before {
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
  flex-wrap: wrap;
  gap: clamp(12px, 3vw, 20px);
  max-width: 100%;
  margin: 0;
  width: 100%;
}

.header-main {
  display: flex;
  align-items: center;
  gap: clamp(12px, 3vw, 20px);
  flex: 1;
  min-width: 200px;
}

.header-icon {
  width: clamp(40px, 6vw, 48px);
  height: clamp(40px, 6vw, 48px);
  background: rgba(255, 255, 255, 0.15);
  border-radius: clamp(8px, 2vw, 12px);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: float 3s ease-in-out infinite;
}

.header-icon svg {
  width: clamp(20px, 3vw, 24px);
  height: clamp(20px, 3vw, 24px);
  color: white;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
}

.header-text {
  flex: 1;
  min-width: 200px;
}

.header-title {
  font-size: clamp(20px, 5vw, 32px);
  font-weight: 700;
  margin: 0 0 clamp(4px, 1vh, 8px) 0;
  background: linear-gradient(45deg, #ffffff 0%, #e8f5e8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  letter-spacing: -0.5px;
  line-height: 1.2;
}

.header-subtitle {
  font-size: clamp(12px, 2.5vw, 16px);
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  font-weight: 400;
  letter-spacing: 0.2px;
  line-height: 1.4;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: clamp(8px, 2vw, 16px);
  flex-wrap: wrap;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: clamp(6px, 1.5vw, 8px);
  padding: clamp(6px, 1.5vw, 8px) clamp(12px, 3vw, 16px);
  border-radius: clamp(16px, 4vw, 20px);
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  font-size: clamp(12px, 2.5vw, 14px);
  font-weight: 500;
  transition: all 0.3s ease;
  white-space: nowrap;
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

.refresh-btn {
  display: flex;
  align-items: center;
  gap: clamp(4px, 1vw, 8px);
  padding: clamp(6px, 1.5vw, 8px) clamp(12px, 3vw, 16px);
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: clamp(16px, 4vw, 20px);
  color: white;
  font-size: clamp(12px, 2.5vw, 14px);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  white-space: nowrap;
}

.refresh-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-icon {
  transition: transform 0.3s ease;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.page-content {
  flex: 1;
  padding: clamp(16px, 2vw, 24px);
  box-sizing: border-box;
  width: 100%;
  max-width: 100%;
  margin: 0;
}

.search-section {
  background: white;
  border-radius: clamp(10px, 2vw, 14px);
  padding: clamp(12px, 2.5vw, 18px);
  margin-bottom: clamp(12px, 2.5vw, 18px);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  border: 1px solid #e9ecef;
  width: 100%;
  box-sizing: border-box;
}

.controls-row {
  display: flex;
  gap: clamp(10px, 2vw, 16px);
  align-items: center;
  flex-wrap: wrap;
  width: 100%;
}

.search-group {
  position: relative;
  flex: 1 1 250px;
  min-width: 200px;
  max-width: 400px;
}

.search-icon {
  position: absolute;
  left: clamp(8px, 1.5vw, 10px);
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
  z-index: 2;
}

.search-input {
  width: 100%;
  padding: clamp(8px, 1.5vw, 10px) clamp(8px, 1.5vw, 10px) clamp(8px, 1.5vw, 10px) clamp(28px, 5vw, 35px);
  border: 2px solid #e9ecef;
  border-radius: clamp(6px, 1.5vw, 8px);
  font-size: clamp(12px, 2vw, 14px);
  transition: all 0.3s ease;
  background: #f8f9fa;
  box-sizing: border-box;
}

.search-input:focus {
  outline: none;
  border-color: #2ecc71;
  background: white;
  box-shadow: 0 0 0 3px rgba(46, 204, 113, 0.1);
}

.sort-group {
  display: flex;
  align-items: center;
  gap: clamp(6px, 1.5vw, 10px);
  flex-shrink: 0;
  flex-wrap: wrap;
}

.sort-group label {
  font-size: clamp(12px, 2vw, 13px);
  font-weight: 500;
  color: #495057;
  white-space: nowrap;
}

.sort-buttons {
  display: flex;
  gap: clamp(3px, 0.8vw, 6px);
  flex-wrap: wrap;
}

.sort-btn {
  display: flex;
  align-items: center;
  gap: clamp(2px, 0.4vw, 3px);
  padding: clamp(3px, 0.8vw, 5px) clamp(6px, 1.5vw, 10px);
  border: 1px solid #dee2e6;
  background: white;
  border-radius: clamp(3px, 0.8vw, 5px);
  font-size: clamp(10px, 1.8vw, 11px);
  font-weight: 500;
  color: #6c757d;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.sort-btn:hover {
  border-color: #2ecc71;
  color: #2ecc71;
}

.sort-btn.active {
  background: #2ecc71;
  border-color: #2ecc71;
  color: white;
}

.historiales-section {
  background: white;
  border-radius: clamp(10px, 2vw, 14px);
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  border: 1px solid #e9ecef;
  width: 100%;
  box-sizing: border-box;
  min-height: 350px;
}

.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: clamp(24px, 5vw, 40px);
  text-align: center;
}

.spinner-large {
  width: clamp(32px, 8vw, 48px);
  height: clamp(32px, 8vw, 48px);
  border: 3px solid #f3f3f3;
  border-top: 3px solid #2ecc71;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: clamp(12px, 3vw, 16px);
}

.loading-container p, .error-container p {
  color: #6c757d;
  font-size: clamp(12px, 2.5vw, 14px);
  margin: 0;
}

.retry-btn {
  display: flex;
  align-items: center;
  gap: clamp(4px, 1vw, 8px);
  padding: clamp(6px, 1.5vw, 8px) clamp(12px, 3vw, 16px);
  background: #2ecc71;
  border: none;
  border-radius: clamp(4px, 1vw, 6px);
  color: white;
  font-size: clamp(12px, 2.5vw, 14px);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: clamp(8px, 2vw, 12px);
}

.retry-btn:hover {
  background: #27ae60;
  transform: translateY(-1px);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: clamp(24px, 5vw, 40px);
  text-align: center;
}

.empty-icon {
  margin-bottom: clamp(12px, 3vw, 18px);
  opacity: 0.6;
}

.empty-state h3 {
  color: #495057;
  font-size: clamp(14px, 3vw, 18px);
  font-weight: 600;
  margin: 0 0 clamp(8px, 2vw, 12px) 0;
}

.empty-state p {
  color: #6c757d;
  font-size: clamp(11px, 2vw, 13px);
  margin: 0;
  line-height: 1.5;
}

.welcome-section {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: clamp(20px, 4vw, 32px);
}

.welcome-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(46, 204, 113, 0.2);
  border-radius: clamp(16px, 3vw, 20px);
  padding: clamp(16px, 3vw, 28px);
  text-align: center;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 15px 40px rgba(46, 204, 113, 0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
  overflow: hidden;
  box-sizing: border-box;
}

.welcome-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #2ecc71, #27ae60, #16a085);
  border-radius: 24px 24px 0 0;
}

.welcome-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 30px 80px rgba(46, 204, 113, 0.25);
}

.welcome-icon {
  width: clamp(40px, 8vw, 60px);
  height: clamp(40px, 8vw, 60px);
  background: linear-gradient(135deg, #2ecc71, #27ae60);
  border-radius: clamp(8px, 2vw, 12px);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto clamp(12px, 2.5vw, 18px) auto;
  box-shadow: 0 10px 25px rgba(46, 204, 113, 0.3);
  transition: transform 0.3s ease;
}

.welcome-card:hover .welcome-icon {
  transform: scale(1.05) rotate(5deg);
}

.welcome-icon svg {
  width: clamp(20px, 4vw, 28px);
  height: clamp(20px, 4vw, 28px);
  color: white;
}

.welcome-card h2 {
  color: #2c5530;
  font-size: clamp(16px, 3.5vw, 22px);
  font-weight: 800;
  margin: 0 0 clamp(8px, 2vw, 14px) 0;
  text-shadow: 0 2px 10px rgba(46, 204, 113, 0.2);
  letter-spacing: -0.5px;
}

.welcome-card p {
  color: #27ae60;
  font-size: clamp(11px, 2.5vw, 14px);
  line-height: 1.6;
  margin: 0;
  font-weight: 500;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .main-content {
    margin-left: clamp(120px, 12vw, 180px);
    width: calc(100vw - clamp(120px, 12vw, 180px));
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    width: 100%;
  }
  
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: clamp(8px, 2vw, 12px);
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .controls-row {
    flex-direction: column;
    align-items: stretch;
    gap: clamp(8px, 2vw, 12px);
  }
  
  .search-group {
    min-width: unset;
    max-width: none;
    flex: 1 1 auto;
  }
  
  .sort-group {
    justify-content: center;
    width: 100%;
  }
  
  .sort-buttons {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .page-content {
    padding: clamp(6px, 1.5vw, 10px);
  }
  
  .search-section {
    padding: clamp(8px, 2vw, 12px);
    margin-bottom: clamp(8px, 2vw, 12px);
  }
  
  .welcome-card {
    padding: clamp(12px, 2.5vw, 16px);
    border-radius: clamp(12px, 2.5vw, 14px);
  }
  
  .welcome-section {
    padding: clamp(12px, 2.5vw, 16px);
  }
}

@media (max-width: 360px) {
  .header-main {
    flex-direction: column;
    align-items: flex-start;
    gap: clamp(6px, 1.5vw, 8px);
  }
  
  .header-actions {
    flex-direction: column;
    width: 100%;
    gap: clamp(6px, 1.5vw, 8px);
  }
  
  .connection-status {
    width: 100%;
    justify-content: center;
  }
  
  .refresh-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
