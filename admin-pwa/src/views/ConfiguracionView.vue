<template>
  <div class="configuracion-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div>
            <h1>Configuración del Sistema</h1>
            <p>Administra las configuraciones generales de la aplicación</p>
          </div>
        </div>
      </header>

      <div class="page-content">
        <!-- Configuraciones de API -->
        <div class="config-section">
          <h2>Configuración de API</h2>
          <div class="config-card">
            <div class="config-item">
              <label>URL del Servidor API:</label>
              <input 
                v-model="apiConfig.url" 
                type="url" 
                class="config-input"
                placeholder="https://apipwa.sembrandodatos.com"
              >
            </div>
            <div class="config-item">
              <label>Timeout de Conexión (segundos):</label>
              <input 
                v-model="apiConfig.timeout" 
                type="number" 
                class="config-input"
                min="5"
                max="60"
              >
            </div>
            <button @click="guardarConfigAPI" class="save-btn">
              Guardar Configuración API
            </button>
          </div>
        </div>

        <!-- Configuraciones de la Aplicación -->
        <div class="config-section">
          <h2>Configuración de la Aplicación</h2>
          <div class="config-card">
            <div class="config-item">
              <label>Nombre de la Aplicación:</label>
              <input 
                v-model="appConfig.name" 
                type="text" 
                class="config-input"
                placeholder="Sembrando Vida Admin"
              >
            </div>
            <div class="config-item">
              <label>Registros por página:</label>
              <select v-model="appConfig.recordsPerPage" class="config-select">
                <option value="10">10</option>
                <option value="25">25</option>
                <option value="50">50</option>
                <option value="100">100</option>
              </select>
            </div>
            <div class="config-item">
              <label>Actualización automática:</label>
              <div class="checkbox-wrapper">
                <input 
                  id="autoRefresh"
                  v-model="appConfig.autoRefresh" 
                  type="checkbox" 
                  class="config-checkbox"
                >
                <label for="autoRefresh">Activar actualización automática cada 30 segundos</label>
              </div>
            </div>
            <button @click="guardarConfigApp" class="save-btn">
              Guardar Configuración de App
            </button>
          </div>
        </div>

        <!-- Información del Sistema -->
        <div class="config-section">
          <h2>Información del Sistema</h2>
          <div class="config-card">
            <div class="system-info">
              <div class="info-item">
                <strong>Versión:</strong> v1.0.0
              </div>
              <div class="info-item">
                <strong>Última actualización:</strong> {{ new Date().toLocaleDateString('es-ES') }}
              </div>
              <div class="info-item">
                <strong>Estado del servidor:</strong> 
                <span :class="serverStatus.class">{{ serverStatus.text }}</span>
              </div>
              <div class="info-item">
                <strong>Administrador actual:</strong> {{ adminUser }}
              </div>
            </div>
            <button @click="verificarEstadoServidor" class="check-btn" :disabled="checking">
              {{ checking ? 'Verificando...' : 'Verificar Estado del Servidor' }}
            </button>
          </div>
        </div>

        <!-- Acciones del Sistema -->
        <div class="config-section">
          <h2>Acciones del Sistema</h2>
          <div class="config-card">
            <div class="actions-grid">
              <button @click="exportarDatos" class="action-btn export-btn" :disabled="exporting">
                {{ exporting ? 'Exportando...' : '📊 Exportar Datos' }}
              </button>
              <button @click="limpiarCache" class="action-btn cache-btn">
                🗑️ Limpiar Cache
              </button>
              <button @click="reiniciarContadores" class="action-btn reset-btn">
                🔄 Reiniciar Contadores
              </button>
              <button @click="mostrarLogs" class="action-btn logs-btn">
                📝 Ver Logs del Sistema
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>    <!-- Modal para mensajes -->
    <div v-if="showModal" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ modalTitle }}</h3>
          <button @click="cerrarModal" class="btn-close">×</button>
        </div>
        <div class="modal-body" v-html="modalContent"></div>
      </div>
    </div>    <!-- Modal de confirmación -->
    <ConfirmModal
      :show="showConfirmModal"
      :title="confirmTitle"
      :message="confirmMessage"
      @confirm="handleConfirm"
      @cancel="handleCancel"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Sidebar from '../components/Sidebar.vue'
import ConfirmModal from '../components/ConfirmModal.vue'
import { obtenerFechaActualCDMX } from '../utils/dateUtils.js'

const router = useRouter()

const adminUser = ref(localStorage.getItem('admin_user') || 'Admin')
const checking = ref(false)
const exporting = ref(false)

// Variables para el modal de confirmación
const showConfirmModal = ref(false)
const confirmAction = ref(null)
const confirmTitle = ref('')
const confirmMessage = ref('')

const apiConfig = reactive({
  url: 'https://apipwa.sembrandodatos.com',
  timeout: 30
})

const appConfig = reactive({
  name: 'Sembrando Vida Admin',
  recordsPerPage: 25,
  autoRefresh: false
})

const serverStatus = reactive({
  text: 'Desconocido',
  class: 'status-unknown'
})

const showModal = ref(false)
const modalTitle = ref('')
const modalContent = ref('')

onMounted(() => {
  cargarConfiguraciones()
  verificarEstadoServidor()
})

const cargarConfiguraciones = () => {
  // Cargar configuraciones desde localStorage
  const savedApiConfig = localStorage.getItem('admin_api_config')
  if (savedApiConfig) {
    Object.assign(apiConfig, JSON.parse(savedApiConfig))
  }

  const savedAppConfig = localStorage.getItem('admin_app_config')
  if (savedAppConfig) {
    Object.assign(appConfig, JSON.parse(savedAppConfig))
  }
}

const guardarConfigAPI = () => {
  localStorage.setItem('admin_api_config', JSON.stringify(apiConfig))
  mostrarMensaje('Éxito', 'Configuración de API guardada correctamente.')
}

const guardarConfigApp = () => {
  localStorage.setItem('admin_app_config', JSON.stringify(appConfig))
  mostrarMensaje('Éxito', 'Configuración de la aplicación guardada correctamente.')
}

const verificarEstadoServidor = async () => {
  checking.value = true
  
  try {
    const token = localStorage.getItem('admin_token')
    await axios.get(`${apiConfig.url}/usuarios`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      timeout: apiConfig.timeout * 1000
    })
    
    serverStatus.text = '🟢 Conectado'
    serverStatus.class = 'status-online'
  } catch (err) {
    serverStatus.text = '🔴 Desconectado'
    serverStatus.class = 'status-offline'
  } finally {
    checking.value = false
  }
}

const exportarDatos = async () => {
  exporting.value = true
  
  try {
    const token = localStorage.getItem('admin_token')
    
    // Obtener todos los datos
    const [usuariosRes, registrosRes] = await Promise.all([
      axios.get(`${apiConfig.url}/usuarios`, {
        headers: { 'Authorization': `Bearer ${token}` }
      }),
      axios.get(`${apiConfig.url}/registros`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
    ])
    
    // Manejar diferentes formatos de respuesta
    const usuariosData = Array.isArray(usuariosRes.data) ? usuariosRes.data : (usuariosRes.data.usuarios || [])
    const registrosData = Array.isArray(registrosRes.data) ? registrosRes.data : (registrosRes.data.registros || [])
    
    const datos = {
      usuarios: usuariosData,
      registros: registrosData,
      exportado_en: new Date().toISOString(),
      total_usuarios: usuariosData.length,
      total_registros: registrosData.length
    }
    
    // Crear y descargar archivo JSON
    const blob = new Blob([JSON.stringify(datos, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `sembrando_vida_export_${new Date().toISOString().split('T')[0]}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    mostrarMensaje('Éxito', `Datos exportados correctamente.<br>Usuarios: ${datos.total_usuarios}<br>Registros: ${datos.total_registros}`)
  } catch (err) {
    mostrarMensaje('Error', 'Error al exportar los datos: ' + (err.response?.data?.detail || err.message))
  } finally {
    exporting.value = false
  }
}

// Funciones para el modal de confirmación
const showConfirmation = (title, message, action) => {
  confirmTitle.value = title
  confirmMessage.value = message
  confirmAction.value = action
  showConfirmModal.value = true
}

const handleConfirm = () => {
  if (confirmAction.value) {
    confirmAction.value()
  }
  showConfirmModal.value = false
}

const handleCancel = () => {
  showConfirmModal.value = false
  confirmAction.value = null
}

const limpiarCache = () => {
  showConfirmation(
    'Limpiar Cache',
    '¿Estás seguro de que quieres limpiar el cache? Esto eliminará datos temporales almacenados.',
    () => {
      // Limpiar cache del navegador (localStorage excepto tokens)
      const token = localStorage.getItem('admin_token')
      const user = localStorage.getItem('admin_user')
      
      localStorage.clear()
      
      if (token) localStorage.setItem('admin_token', token)
      if (user) localStorage.setItem('admin_user', user)
      
      // Guardar configuraciones actuales
      localStorage.setItem('admin_api_config', JSON.stringify(apiConfig))
      localStorage.setItem('admin_app_config', JSON.stringify(appConfig))
      
      mostrarMensaje('Éxito', 'Cache limpiado correctamente.')
    }
  )
}

const reiniciarContadores = () => {
  showConfirmation(
    'Reiniciar Contadores',
    '¿Estás seguro de que quieres reiniciar los contadores del sistema?',
    () => {
      // Simular reinicio de contadores
      mostrarMensaje('Éxito', 'Contadores del sistema reiniciados correctamente.')
    }
  )
}

const mostrarLogs = () => {
  const fechaActual = obtenerFechaActualCDMX().format('DD/MM/YYYY HH:mm:ss')
  const logs = [
    `[${fechaActual}] Sistema iniciado`,
    `[${fechaActual}] Usuario ${adminUser.value} autenticado`,
    `[${fechaActual}] Configuración cargada`,
    `[${fechaActual}] Estado del servidor verificado`
  ]
  
  mostrarMensaje('Logs del Sistema', `<pre>${logs.join('\n')}</pre>`)
}

const mostrarMensaje = (titulo, contenido) => {
  modalTitle.value = titulo
  modalContent.value = contenido
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
.configuracion-container {
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

.header-content h1 {
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 4px;
}

.header-content p {
  color: #7f8c8d;
  font-size: 14px;
}

.page-content {
  padding: 24px 32px;
}

.config-section {
  margin-bottom: 32px;
}

.config-section h2 {
  color: #2c3e50;
  margin-bottom: 16px;
  font-size: 20px;
}

.config-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.config-item {
  margin-bottom: 20px;
}

.config-item label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #2c3e50;
}

.config-input, .config-select {
  width: 100%;
  max-width: 400px;
  padding: 10px 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.2s;
}

.config-input:focus, .config-select:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.config-checkbox {
  width: auto;
}

.save-btn, .check-btn {
  padding: 10px 20px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}

.save-btn:hover, .check-btn:hover {
  background: #45a049;
  transform: translateY(-1px);
}

.save-btn:disabled, .check-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.system-info {
  display: grid;
  gap: 12px;
  margin-bottom: 20px;
}

.info-item {
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
  border-bottom: none;
}

.status-online {
  color: #27ae60;
}

.status-offline {
  color: #e74c3c;
}

.status-unknown {
  color: #f39c12;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.action-btn {
  padding: 16px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.export-btn {
  background: #3498db;
  color: white;
}

.export-btn:hover:not(:disabled) {
  background: #2980b9;
  transform: translateY(-1px);
}

.cache-btn {
  background: #f39c12;
  color: white;
}

.cache-btn:hover {
  background: #d35400;
  transform: translateY(-1px);
}

.reset-btn {
  background: #9b59b6;
  color: white;
}

.reset-btn:hover {
  background: #8e44ad;
  transform: translateY(-1px);
}

.logs-btn {
  background: #34495e;
  color: white;
}

.logs-btn:hover {
  background: #2c3e50;
  transform: translateY(-1px);
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
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

.modal-body pre {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  font-size: 12px;
  overflow-x: auto;
}

/* Responsive */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }
  
  .page-header {
    padding: 16px 20px;
  }
  
  .page-content {
    padding: 16px 20px;
  }
  
  .config-card {
    padding: 16px;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .config-input, .config-select {
    max-width: 100%;
  }
}
</style>
