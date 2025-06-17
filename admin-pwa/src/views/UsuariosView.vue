<template>
  <div class="usuarios-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div>
            <h1>Gestión de Usuarios</h1>
            <p>Administra todos los usuarios registrados en la aplicación</p>
          </div>
          <div class="header-actions">
            <button @click="cargarUsuarios" class="refresh-btn" :disabled="loading">
              <span class="refresh-icon" :class="{ spinning: loading }">🔄</span>
              {{ loading ? 'Cargando...' : 'Actualizar' }}
            </button>
          </div>
        </div>
      </header>

      <div class="page-content">
        <!-- Barra de búsqueda -->
        <div class="search-section">
          <div class="search-box">
            <input 
              v-model="searchTerm" 
              type="text" 
              placeholder="Buscar por nombre o correo..." 
              class="search-input"
              @input="filtrarUsuarios"
            >
            <span class="search-icon">🔍</span>
          </div>
        </div>

        <!-- Tabla de usuarios -->
        <div class="usuarios-section">
          <div v-if="loading && usuarios.length === 0" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando usuarios...</p>
          </div>
          
          <div v-else-if="error" class="error-container">
            <p>{{ error }}</p>
            <button @click="cargarUsuarios" class="retry-btn">Reintentar</button>
          </div>
          
          <div v-else-if="usuariosFiltrados.length === 0" class="empty-state">
            <div class="empty-icon">👥</div>
            <h3>No hay usuarios</h3>
            <p v-if="searchTerm">No se encontraron usuarios con el término "{{ searchTerm }}"</p>
            <p v-else>Aún no se han registrado usuarios en la aplicación.</p>
          </div>
          
          <div v-else class="table-container">
            <table class="usuarios-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Correo</th>
                  <th>Nombre Completo</th>
                  <th>Cargo</th>
                  <th>Supervisor</th>
                  <th>Fecha de Registro</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>                <tr v-for="usuario in usuariosFiltrados" :key="usuario.id">
                  <td>#{{ usuario.id }}</td>
                  <td>{{ usuario.correo }}</td>
                  <td>{{ usuario.nombre_completo }}</td>
                  <td>{{ usuario.cargo }}</td>
                  <td>{{ usuario.supervisor }}</td>
                  <td>{{ formatFecha(usuario.created_at || new Date()) }}</td>
                  <td>
                    <span class="status-badge active">
                      Activo
                    </span>
                  </td>
                  <td>
                    <button @click="verDetalles(usuario)" class="btn-ver">
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Sidebar from '../components/Sidebar.vue'
import { usuariosService } from '../services/usuariosService.js'

const router = useRouter()

const API_URL = 'https://apipwa.sembrandodatos.com'
const usuarios = ref([])
const usuariosFiltrados = ref([])
const loading = ref(false)
const error = ref('')
const searchTerm = ref('')

const showModal = ref(false)
const modalTitle = ref('')
const modalContent = ref('')

onMounted(() => {
  cargarUsuarios()
})

const cargarUsuarios = async () => {
  loading.value = true
  error.value = ''
  
  try {
    // Usar el servicio de usuarios con datos reales de la base de datos
    usuarios.value = await usuariosService.obtenerUsuarios()
    usuariosFiltrados.value = usuarios.value
    
    console.log('✅ Usuarios reales cargados desde la base de datos:', usuarios.value)
  } catch (err) {
    console.error('❌ Error al cargar usuarios desde la base de datos:', err)
    error.value = 'Error al conectar con la base de datos. Verifica que el servidor esté funcionando.'
    usuarios.value = []
    usuariosFiltrados.value = []
  } finally {
    loading.value = false
  }
}

const filtrarUsuarios = () => {
  if (!searchTerm.value.trim()) {
    usuariosFiltrados.value = usuarios.value
    return
  }
  
  const termino = searchTerm.value.toLowerCase()
  usuariosFiltrados.value = usuarios.value.filter(usuario => 
    usuario.correo.toLowerCase().includes(termino) ||
    (usuario.nombre_completo && usuario.nombre_completo.toLowerCase().includes(termino)) ||
    (usuario.cargo && usuario.cargo.toLowerCase().includes(termino)) ||
    (usuario.supervisor && usuario.supervisor.toLowerCase().includes(termino))
  )
}

const formatFecha = (fechaStr) => {
  try {
    return new Date(fechaStr).toLocaleDateString('es-ES')
  } catch (e) {
    return fechaStr
  }
}

const verDetalles = (usuario) => {
  modalTitle.value = 'Detalles del Usuario'
  modalContent.value = `
    <div class="usuario-detalles">
      <div><strong>ID:</strong> #${usuario.id}</div>
      <div><strong>Correo:</strong> ${usuario.correo}</div>
      <div><strong>Nombre Completo:</strong> ${usuario.nombre_completo}</div>
      <div><strong>Cargo:</strong> ${usuario.cargo}</div>
      <div><strong>Supervisor:</strong> ${usuario.supervisor}</div>
      <div><strong>Estado:</strong> Activo</div>
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
.usuarios-container {
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

.search-section {
  margin-bottom: 24px;
}

.search-box {
  position: relative;
  max-width: 400px;
}

.search-input {
  width: 100%;
  padding: 12px 16px 12px 44px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 14px;
  transition: all 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.search-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.usuarios-section {
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

.usuarios-table {
  width: 100%;
  border-collapse: collapse;
}

.usuarios-table th {
  background: #f8f9fa;
  padding: 16px 12px;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e0e0e0;
  font-size: 14px;
}

.usuarios-table td {
  padding: 12px;
  border-bottom: 1px solid #e0e0e0;
  font-size: 14px;
}

.usuarios-table tr:hover {
  background: #f8f9fa;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.active {
  background: #d4edda;
  color: #155724;
}

.status-badge.inactive {
  background: #f8d7da;
  color: #721c24;
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

.usuario-detalles div {
  margin-bottom: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.usuario-detalles div:last-child {
  border-bottom: none;
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
  
  .table-container {
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .usuarios-table {
    font-size: 12px;
  }
  
  .usuarios-table th,
  .usuarios-table td {
    padding: 8px 4px;
  }
}
</style>
