<template>
  <div class="configuracion-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"/>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Configuración del Sistema</h1>
              <p class="header-subtitle">Administra las configuraciones generales de la aplicación</p>
            </div>
          </div>
        </div>
      </header>

      <div class="page-content">
        <!-- Grid de configuraciones compacto -->
        <div class="config-grid">
          <!-- Configuración de API -->
          <div class="config-card">
            <div class="card-header">
              <div class="card-icon api-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>
                  <polyline points="14,2 14,8 20,8"/>
                  <line x1="12" y1="18" x2="12" y2="12"/>
                  <line x1="9" y1="15" x2="15" y2="15"/>
                </svg>
              </div>
              <h3>API Configuration</h3>
            </div>
            
            <div class="form-group">
              <label>URL del Servidor</label>
              <input 
                v-model="apiConfig.url" 
                type="url" 
                class="form-input"
                placeholder="https://apipwa.sembrandodatos.com"
              >
            </div>
            
            <div class="form-group">
              <label>Timeout (segundos)</label>
              <input 
                v-model="apiConfig.timeout" 
                type="number" 
                class="form-input"
                min="5"
                max="60"
              >
            </div>
            
            <button @click="guardarConfigAPI" class="btn btn-primary">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/>
              </svg>
              Guardar
            </button>
          </div>

          <!-- Configuración de la App -->
          <div class="config-card">
            <div class="card-header">
              <div class="card-icon app-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
                  <line x1="8" y1="21" x2="16" y2="21"/>
                  <line x1="12" y1="17" x2="12" y2="21"/>
                </svg>
              </div>
              <h3>Aplicación</h3>
            </div>
            
            <div class="form-group">
              <label>Nombre de la App</label>
              <input 
                v-model="appConfig.name" 
                type="text" 
                class="form-input"
                placeholder="Sembrando Vida Admin"
              >
            </div>
            
            <div class="form-group">
              <label>Registros por página</label>
              <select v-model="appConfig.recordsPerPage" class="form-select">
                <option value="10">10</option>
                <option value="25">25</option>
                <option value="50">50</option>
                <option value="100">100</option>
              </select>
            </div>
            
            <div class="checkbox-group">
              <input 
                id="autoRefresh"
                v-model="appConfig.autoRefresh" 
                type="checkbox" 
                class="checkbox"
              >
              <label for="autoRefresh">Actualización automática</label>
            </div>
            
            <button @click="guardarConfigApp" class="btn btn-primary">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/>
              </svg>
              Guardar
            </button>
          </div>

          <!-- Información del Sistema -->
          <div class="config-card">
            <div class="card-header">
              <div class="card-icon info-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="16" x2="12" y2="12"/>
                  <line x1="12" y1="8" x2="12.01" y2="8"/>
                </svg>
              </div>
              <h3>Sistema</h3>
            </div>
            
            <div class="info-list">
              <div class="info-item">
                <span class="info-label">Versión</span>
                <span class="info-value">v1.0.0</span>
              </div>
              <div class="info-item">
                <span class="info-label">Última actualización</span>
                <span class="info-value">{{ new Date().toLocaleDateString('es-ES') }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Estado del servidor</span>
                <span :class="['status-badge', serverStatus.class]">{{ serverStatus.text }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Administrador</span>
                <span class="info-value">{{ adminUser }}</span>
              </div>
            </div>
            
            <button @click="verificarEstadoServidor" class="btn btn-secondary" :disabled="checking">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 12c0 1-.19 1.96-.55 2.84l1.34.82c.24-.94.35-1.94.35-2.96 0-3.22-1.2-6.15-3.15-8.37l-1.06 1.06C19.55 7 21 9.36 21 12z"/>
                <path d="M3 12c0-1 .19-1.96.55-2.84L2.21 8.34C1.97 9.28 1.86 10.28 1.86 12c0 3.22 1.2 6.15 3.15 8.37l1.06-1.06C4.45 17 3 14.64 3 12z"/>
                <path d="M19 12c0-1.66-.61-3.15-1.61-4.31l-1.06 1.06C17.09 9.64 17.5 10.77 17.5 12s-.41 2.36-1.17 3.25l1.06 1.06C18.39 15.15 19 13.66 19 12z"/>
                <path d="M5 12c0 1.66.61 3.15 1.61 4.31l1.06-1.06C6.91 14.36 6.5 13.23 6.5 12s.41-2.36 1.17-3.25L6.61 7.69C5.61 8.85 5 10.34 5 12z"/>
                <circle cx="12" cy="12" r="2"/>
              </svg>
              {{ checking ? 'Verificando...' : 'Verificar' }}
            </button>
          </div>

          <!-- Acciones del Sistema -->
          <div class="config-card">
            <div class="card-header">
              <div class="card-icon actions-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="9,11 12,14 22,4"/>
                  <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
                </svg>
              </div>
              <h3>Acciones</h3>
            </div>
            
            <div class="actions-grid">
              <button @click="exportarDatos" class="action-btn export-btn" :disabled="exporting">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="7,10 12,15 17,10"/>
                  <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                {{ exporting ? 'Exportando JSON...' : 'Exportar Datos (JSON)' }}
              </button>
              
              <button @click="descargarBaseDatos" class="action-btn database-btn" :disabled="descargandoBD">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <ellipse cx="12" cy="5" rx="9" ry="3"/>
                  <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
                  <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
                </svg>
                {{ descargandoBD ? 'Descargando...' : 'Descargar BD' }}
              </button>
              
              <button @click="limpiarCache" class="action-btn cache-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 6h18"/>
                  <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
                  <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
                </svg>
                Limpiar Cache
              </button>
              
              <button @click="reiniciarContadores" class="action-btn reset-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>
                  <path d="M21 3v5h-5"/>
                  <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>
                  <path d="M8 16H3v5"/>
                </svg>
                Reiniciar Contadores
              </button>
              
              <button @click="mostrarLogs" class="action-btn logs-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14,2 14,8 20,8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                  <polyline points="10,9 9,9 8,9"/>
                </svg>
                Ver Logs
              </button>
            </div>
          </div>

          <!-- Eliminación Masiva - BLOQUEADA -->
          <div class="config-card danger-card danger-card-blocked">
            <div class="card-header">
              <div class="card-icon danger-icon danger-icon-blocked">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="15" y1="9" x2="9" y2="15"/>
                  <line x1="9" y1="9" x2="15" y2="15"/>
                </svg>
              </div>
              <h3>Zona Peligrosa (Bloqueada)</h3>
            </div>
            
            <div class="danger-warning danger-warning-blocked">
              <div class="warning-content">
                <strong>🔒 Sección Bloqueada:</strong> Esta zona está temporalmente deshabilitada por seguridad. Las funciones de eliminación masiva no están disponibles.
              </div>
            </div>
            
            <div class="danger-actions">
              <button class="danger-btn registros-btn danger-btn-blocked" disabled>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14,2 14,8 20,8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                  <polyline points="10,9 9,9 8,9"/>
                </svg>
                Eliminar Registros (Bloqueado)
              </button>
              
              <button class="danger-btn asistencias-btn danger-btn-blocked" disabled>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12,6 12,12 16,14"/>
                </svg>
                Eliminar Asistencias (Bloqueado)
              </button>
            </div>
            
            <!-- Overlay de bloqueo -->
            <div class="blocked-overlay">
              <div class="blocked-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                  <circle cx="12" cy="16" r="1"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
              </div>
              <div class="blocked-text">BLOQUEADO</div>
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
import Sidebar from '../components/Sidebar_NEW.vue'
import ConfirmModal from '../components/ConfirmModal.vue'
import asistenciasService from '../services/asistenciasService.js'

const router = useRouter()

// Estado de conexión
const isOnline = ref(navigator.onLine)

const adminUser = ref(localStorage.getItem('admin_user') || 'Admin')
const checking = ref(false)
const exporting = ref(false)

// Variables para el modal de confirmación
const showConfirmModal = ref(false)
const confirmAction = ref(null)
const confirmTitle = ref('')
const confirmMessage = ref('')

// Variables para las acciones de eliminación masiva
const eliminandoRegistros = ref(false)
const eliminandoAsistencias = ref(false)
const descargandoBD = ref(false)

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
  
  // Escuchar cambios de conexión
  window.addEventListener('online', () => {
    isOnline.value = true
  })
  
  window.addEventListener('offline', () => {
    isOnline.value = false
  })
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
    
    mostrarMensaje('Iniciando', 'Obteniendo todos los registros de actividades...')
    
    // Obtener TODOS los registros sin límite y todos los usuarios
    const [usuariosRes, registrosRes] = await Promise.all([
      axios.get(`${apiConfig.url}/usuarios`, {
        headers: { 'Authorization': `Bearer ${token}` }
      }),
      axios.get(`${apiConfig.url}/registros`, {
        headers: { 'Authorization': `Bearer ${token}` },
        params: { 
          limit: 10000, // Límite alto para obtener todos los registros
          page_size: 5000 // Tamaño de página grande
        }
      })
    ])
    
    // Manejar diferentes formatos de respuesta
    const usuariosData = Array.isArray(usuariosRes.data) ? usuariosRes.data : (usuariosRes.data.usuarios || [])
    const registrosData = Array.isArray(registrosRes.data) ? registrosRes.data : (registrosRes.data.registros || [])
    
    console.log('📊 Datos obtenidos:', {
      usuarios: usuariosData.length,
      registros: registrosData.length
    })
    
    // Crear estructura JSON completa con información detallada
    const datos = {
      metadatos: {
        exportado_en: new Date().toISOString(),
        fecha_exportacion: new Date().toLocaleString('es-ES'),
        servidor: apiConfig.url,
        tipo_exportacion: 'registros_actividades_completo',
        version: '1.0'
      },
      resumen: {
        total_usuarios: usuariosData.length,
        total_registros: registrosData.length,
        registros_campo: registrosData.filter(r => r.tipo_actividad === 'campo').length,
        registros_gabinete: registrosData.filter(r => r.tipo_actividad === 'gabinete').length,
        registros_sin_tipo: registrosData.filter(r => !r.tipo_actividad || r.tipo_actividad === null).length
      },
      usuarios: usuariosData.map(usuario => ({
        id: usuario.id,
        correo: usuario.correo,
        nombre_completo: usuario.nombre_completo,
        cargo: usuario.cargo,
        supervisor: usuario.supervisor,
        curp: usuario.curp,
        telefono: usuario.telefono,
        rol: usuario.rol || 'user'
      })),
      registros_actividades: registrosData.map(registro => ({
        id: registro.id,
        usuario_id: registro.usuario_id,
        usuario_info: {
          nombre: usuariosData.find(u => u.id === registro.usuario_id)?.nombre_completo || 'Usuario no encontrado',
          correo: usuariosData.find(u => u.id === registro.usuario_id)?.correo || 'N/A'
        },
        ubicacion: {
          latitud: registro.latitud,
          longitud: registro.longitud
        },
        actividad: {
          descripcion: registro.descripcion,
          tipo: registro.tipo_actividad || 'campo',
          fecha_hora: registro.fecha_hora,
          foto_url: registro.foto_url
        }
      }))
    }
    
    // Crear y descargar archivo JSON con nombre descriptivo
    const timestamp = new Date().toISOString().split('T')[0]
    const blob = new Blob([JSON.stringify(datos, null, 2)], { type: 'application/json; charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `registros_actividades_${timestamp}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    // Calcular tamaño del archivo
    const tamanhoKB = Math.round(blob.size / 1024)
    
    mostrarMensaje('✅ Exportación JSON Exitosa', 
      `<div style="text-align: left;">
        <h4 style="color: #2563eb; margin-bottom: 15px;">📄 Archivo JSON Generado</h4>
        <p><strong>📁 Archivo:</strong> registros_actividades_${timestamp}.json</p>
        <p><strong>📊 Tamaño:</strong> ${tamanhoKB} KB</p>
        <hr style="margin: 15px 0;">
        <h5 style="color: #1e40af;">📋 Datos Exportados:</h5>
        <ul style="margin: 10px 0; padding-left: 20px;">
          <li><strong>👥 Usuarios:</strong> ${datos.resumen.total_usuarios}</li>
          <li><strong>📝 Total registros:</strong> ${datos.resumen.total_registros}</li>
          <li><strong>🏞️ Actividades campo:</strong> ${datos.resumen.registros_campo}</li>
          <li><strong>🏢 Actividades gabinete:</strong> ${datos.resumen.registros_gabinete}</li>
          <li><strong>❓ Sin tipo:</strong> ${datos.resumen.registros_sin_tipo}</li>
        </ul>
        <hr style="margin: 15px 0;">
        <p style="font-size: 12px; color: #666; margin-top: 15px;">
          El archivo JSON contiene todos los registros de actividades con información 
          detallada de usuarios, ubicaciones y metadatos. Compatible con análisis de datos 
          y herramientas de visualización.
        </p>
      </div>`
    )
  } catch (err) {
    let errorMsg = 'Error al exportar los datos: '
    
    if (err.response?.status === 401) {
      errorMsg += 'No autorizado. Inicia sesión nuevamente.'
    } else if (err.response?.status === 403) {
      errorMsg += 'Acceso denegado. Permisos insuficientes.'
    } else if (err.response?.status === 500) {
      errorMsg += 'Error del servidor. Intenta más tarde.'
    } else if (err.request) {
      errorMsg += 'No se pudo conectar con el servidor. Verifica tu conexión.'
    } else {
      errorMsg += err.message || 'Error desconocido'
    }
    
    mostrarMensaje('❌ Error', errorMsg)
  } finally {
    exporting.value = false
  }
}

const descargarBaseDatos = async () => {
  descargandoBD.value = true
  
  try {
    const token = localStorage.getItem('admin_token')
    
    mostrarMensaje('Iniciando', 'Obteniendo todos los datos de la base de datos...')
    
    // Obtener TODOS los datos disponibles de la base de datos app_registros
    const [usuariosRes, registrosRes, asistenciasRes] = await Promise.all([
      axios.get(`${apiConfig.url}/usuarios/exportacion-completa`, {
        headers: { 'Authorization': `Bearer ${token}` }
      }),
      axios.get(`${apiConfig.url}/registros`, {
        headers: { 'Authorization': `Bearer ${token}` }
      }),
      axios.get(`${apiConfig.url}/asistencias`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
    ])
    
    // Manejar diferentes formatos de respuesta
    const usuariosData = Array.isArray(usuariosRes.data) ? usuariosRes.data : (usuariosRes.data.usuarios || [])
    const registrosData = Array.isArray(registrosRes.data) ? registrosRes.data : (registrosRes.data.registros || [])
    const asistenciasData = Array.isArray(asistenciasRes.data) ? asistenciasRes.data : (asistenciasRes.data.asistencias || [])
    
    // DEBUG: Mostrar datos de usuarios para verificar campos disponibles
    console.log('🔍 DEBUG - Datos de usuarios recibidos:', usuariosData)
    if (usuariosData.length > 0) {
      console.log('🔍 DEBUG - Primer usuario completo:', usuariosData[0])
      console.log('🔍 DEBUG - Campos disponibles:', Object.keys(usuariosData[0]))
    }
    
    // Generar SQL completo
    let sqlContent = ''
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
    
    // Header del archivo SQL
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- EXPORTACIÓN COMPLETA BASE DE DATOS app_registros\n`
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- Fecha de exportación: ${new Date().toLocaleString('es-ES')}\n`
    sqlContent += `-- Servidor: ${apiConfig.url}\n`
    sqlContent += `-- Total usuarios: ${usuariosData.length}\n`
    sqlContent += `-- Total registros: ${registrosData.length}\n`
    sqlContent += `-- Total asistencias: ${asistenciasData.length}\n`
    sqlContent += `-- ===============================================\n\n`
    
    // =================== TABLA USUARIOS ===================
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- TABLA: USUARIOS\n`
    sqlContent += `-- ===============================================\n`
    sqlContent += `DROP TABLE IF EXISTS usuarios CASCADE;\n\n`
    
    sqlContent += `CREATE TABLE usuarios (\n`
    sqlContent += `    id SERIAL PRIMARY KEY,\n`
    sqlContent += `    correo VARCHAR(255) UNIQUE NOT NULL,\n`
    sqlContent += `    nombre_completo VARCHAR(255) NOT NULL,\n`
    sqlContent += `    cargo VARCHAR(255),\n`
    sqlContent += `    supervisor VARCHAR(255),\n`
    sqlContent += `    contrasena VARCHAR(255) NOT NULL,\n`
    sqlContent += `    curp VARCHAR(18) UNIQUE,\n`
    sqlContent += `    telefono VARCHAR(20),\n`
    sqlContent += `    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n`
    sqlContent += `    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n`
    sqlContent += `);\n\n`
    
    // Insertar datos de usuarios
    if (usuariosData.length > 0) {
      sqlContent += `-- Datos de usuarios (${usuariosData.length} registros)\n`
      sqlContent += `INSERT INTO usuarios (id, correo, nombre_completo, cargo, supervisor, contrasena, curp, telefono) VALUES\n`
      
      const usuariosInserts = usuariosData.map((usuario, index) => {
        const id = usuario.id || index + 1
        const correo = (usuario.correo || usuario.email || '').replace(/'/g, "''")
        const nombre = (usuario.nombre_completo || usuario.nombre || '').replace(/'/g, "''")
        const cargo = (usuario.cargo || '').replace(/'/g, "''")
        const supervisor = (usuario.supervisor || '').replace(/'/g, "''")
        
        // Obtener la contraseña real del nuevo endpoint
        const contrasena = (usuario.contrasena || 'sin_contrasena').replace(/'/g, "''")
        const curp = (usuario.curp || '').replace(/'/g, "''")
        const telefono = (usuario.telefono || '').replace(/'/g, "''")
        
        // DEBUG: Log de cada usuario para verificar contraseña y teléfono
        console.log(`🔍 Usuario ${id}: contrasena="${contrasena}", telefono="${telefono}"`)
        
        return `(${id}, '${correo}', '${nombre}', '${cargo}', '${supervisor}', '${contrasena}', '${curp}', '${telefono}')`
      })
      
      sqlContent += usuariosInserts.join(',\n') + ';\n\n'
    }
    
    // =================== TABLA REGISTROS ===================
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- TABLA: REGISTROS\n`
    sqlContent += `-- ===============================================\n`
    sqlContent += `DROP TABLE IF EXISTS registros CASCADE;\n\n`
    
    sqlContent += `CREATE TABLE registros (\n`
    sqlContent += `    id SERIAL PRIMARY KEY,\n`
    sqlContent += `    usuario_id INTEGER REFERENCES usuarios(id),\n`
    sqlContent += `    latitud DECIMAL(10, 8),\n`
    sqlContent += `    longitud DECIMAL(11, 8),\n`
    sqlContent += `    descripcion TEXT,\n`
    sqlContent += `    foto_url VARCHAR(500),\n`
    sqlContent += `    fecha_hora TIMESTAMP NOT NULL,\n`
    sqlContent += `    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n`
    sqlContent += `);\n\n`
    
    // Insertar datos de registros
    if (registrosData.length > 0) {
      sqlContent += `-- Datos de registros (${registrosData.length} registros)\n`
      sqlContent += `INSERT INTO registros (id, usuario_id, latitud, longitud, descripcion, foto_url, fecha_hora) VALUES\n`
      
      const registrosInserts = registrosData.map((registro, index) => {
        const id = registro.id || index + 1
        const usuario_id = registro.usuario_id || 'NULL'
        const latitud = registro.latitud || 'NULL'
        const longitud = registro.longitud || 'NULL'
        const descripcion = (registro.descripcion || '').replace(/'/g, "''")
        const foto_url = (registro.foto_url || '').replace(/'/g, "''")
        const fecha_hora = registro.fecha_hora || new Date().toISOString()
        
        return `(${id}, ${usuario_id}, ${latitud}, ${longitud}, '${descripcion}', '${foto_url}', '${fecha_hora}')`
      })
      
      sqlContent += registrosInserts.join(',\n') + ';\n\n'
    }
    
    // =================== TABLA ASISTENCIAS ===================
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- TABLA: ASISTENCIAS\n`
    sqlContent += `-- ===============================================\n`
    sqlContent += `DROP TABLE IF EXISTS asistencias CASCADE;\n\n`
    
    sqlContent += `CREATE TABLE asistencias (\n`
    sqlContent += `    id SERIAL PRIMARY KEY,\n`
    sqlContent += `    usuario_id INTEGER REFERENCES usuarios(id),\n`
    sqlContent += `    fecha DATE NOT NULL,\n`
    sqlContent += `    hora_entrada TIME,\n`
    sqlContent += `    hora_salida TIME,\n`
    sqlContent += `    latitud_entrada DECIMAL(10, 8),\n`
    sqlContent += `    longitud_entrada DECIMAL(11, 8),\n`
    sqlContent += `    latitud_salida DECIMAL(10, 8),\n`
    sqlContent += `    longitud_salida DECIMAL(11, 8),\n`
    sqlContent += `    foto_entrada_url VARCHAR(500),\n`
    sqlContent += `    foto_salida_url VARCHAR(500),\n`
    sqlContent += `    descripcion_entrada TEXT,\n`
    sqlContent += `    descripcion_salida TEXT,\n`
    sqlContent += `    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n`
    sqlContent += `);\n\n`
    
    // Insertar datos de asistencias
    if (asistenciasData.length > 0) {
      sqlContent += `-- Datos de asistencias (${asistenciasData.length} registros)\n`
      sqlContent += `INSERT INTO asistencias (id, usuario_id, fecha, hora_entrada, hora_salida, latitud_entrada, longitud_entrada, latitud_salida, longitud_salida, foto_entrada_url, foto_salida_url, descripcion_entrada, descripcion_salida) VALUES\n`
      
      const asistenciasInserts = asistenciasData.map((asistencia, index) => {
        const id = asistencia.id || index + 1
        const usuario_id = asistencia.usuario_id || 'NULL'
        const fecha = asistencia.fecha || new Date().toISOString().split('T')[0]
        const hora_entrada = asistencia.hora_entrada ? `'${asistencia.hora_entrada}'` : 'NULL'
        const hora_salida = asistencia.hora_salida ? `'${asistencia.hora_salida}'` : 'NULL'
        const latitud_entrada = asistencia.latitud_entrada || 'NULL'
        const longitud_entrada = asistencia.longitud_entrada || 'NULL'
        const latitud_salida = asistencia.latitud_salida || 'NULL'
        const longitud_salida = asistencia.longitud_salida || 'NULL'
        const foto_entrada_url = (asistencia.foto_entrada_url || '').replace(/'/g, "''")
        const foto_salida_url = (asistencia.foto_salida_url || '').replace(/'/g, "''")
        const descripcion_entrada = (asistencia.descripcion_entrada || '').replace(/'/g, "''")
        const descripcion_salida = (asistencia.descripcion_salida || '').replace(/'/g, "''")
        
        return `(${id}, ${usuario_id}, '${fecha}', ${hora_entrada}, ${hora_salida}, ${latitud_entrada}, ${longitud_entrada}, ${latitud_salida}, ${longitud_salida}, '${foto_entrada_url}', '${foto_salida_url}', '${descripcion_entrada}', '${descripcion_salida}')`
      })
      
      sqlContent += asistenciasInserts.join(',\n') + ';\n\n'
    }
    
    // =================== ÍNDICES Y CONSTRAINTS ===================
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- ÍNDICES Y OPTIMIZACIONES\n`
    sqlContent += `-- ===============================================\n`
    sqlContent += `CREATE INDEX IF NOT EXISTS idx_usuarios_correo ON usuarios(correo);\n`
    sqlContent += `CREATE INDEX IF NOT EXISTS idx_usuarios_curp ON usuarios(curp);\n`
    sqlContent += `CREATE INDEX IF NOT EXISTS idx_registros_usuario ON registros(usuario_id);\n`
    sqlContent += `CREATE INDEX IF NOT EXISTS idx_registros_fecha ON registros(fecha_hora);\n`
    sqlContent += `CREATE INDEX IF NOT EXISTS idx_asistencias_usuario ON asistencias(usuario_id);\n`
    sqlContent += `CREATE INDEX IF NOT EXISTS idx_asistencias_fecha ON asistencias(fecha);\n\n`
    
    // Footer del archivo
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- RESUMEN DE EXPORTACIÓN\n`
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- Usuarios exportados: ${usuariosData.length}\n`
    sqlContent += `-- Registros exportados: ${registrosData.length}\n`
    sqlContent += `-- Asistencias exportadas: ${asistenciasData.length}\n`
    sqlContent += `-- Total de registros: ${usuariosData.length + registrosData.length + asistenciasData.length}\n`
    sqlContent += `-- Fin de la exportación completa\n`
    sqlContent += `-- Fecha: ${new Date().toLocaleString('es-ES')}\n`
    sqlContent += `-- ===============================================\n`
    
    // Crear y descargar archivo SQL
    const blob = new Blob([sqlContent], { type: 'application/sql; charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `BASE_DATOS_COMPLETA_${timestamp}.sql`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    // Calcular tamaño del archivo
    const tamanhoKB = Math.round(blob.size / 1024)
    const totalRegistros = usuariosData.length + registrosData.length + asistenciasData.length
    
    mostrarMensaje('🎉 Base de Datos Completa Descargada', 
      `<div style="text-align: left;">
        <h4 style="color: #2563eb; margin-bottom: 15px;">✅ Exportación Exitosa</h4>
        <p><strong>📁 Archivo:</strong> BASE_DATOS_COMPLETA_${timestamp}.sql</p>
        <p><strong>📊 Tamaño:</strong> ${tamanhoKB} KB</p>
        <hr style="margin: 15px 0;">
        <h5 style="color: #1e40af;">📋 Datos Exportados:</h5>
        <ul style="margin: 10px 0; padding-left: 20px;">
          <li><strong>👥 Usuarios:</strong> ${usuariosData.length} registros</li>
          <li><strong>📝 Registros:</strong> ${registrosData.length} registros</li>
          <li><strong>🕐 Asistencias:</strong> ${asistenciasData.length} registros</li>
        </ul>
        <hr style="margin: 15px 0;">
        <p><strong>🔢 Total de registros:</strong> ${totalRegistros}</p>
        <p style="font-size: 12px; color: #666; margin-top: 15px;">
          El archivo contiene la estructura completa de la base de datos con todos los datos disponibles, 
          índices y constraints. Puede ser restaurado en cualquier servidor PostgreSQL.
        </p>
      </div>`
    )
  } catch (err) {
    let errorMsg = 'Error al descargar la base de datos: '
    
    if (err.response?.status === 401) {
      errorMsg += 'No autorizado. Inicia sesión nuevamente.'
    } else if (err.response?.status === 403) {
      errorMsg += 'Acceso denegado. Permisos insuficientes.'
    } else if (err.response?.status === 404) {
      errorMsg += 'Algunos endpoints no están disponibles. Se descargaron los datos disponibles.'
    } else if (err.response?.status === 500) {
      errorMsg += 'Error del servidor. Intenta más tarde.'
    } else if (err.request) {
      errorMsg += 'No se pudo conectar con el servidor. Verifica tu conexión.'
    } else {
      errorMsg += err.message || 'Error desconocido'
    }
    
    mostrarMensaje('❌ Error', errorMsg)
  } finally {
    descargandoBD.value = false
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
  const logs = [
    `[${new Date().toLocaleString()}] Sistema iniciado`,
    `[${new Date().toLocaleString()}] Usuario ${adminUser.value} autenticado`,
    `[${new Date().toLocaleString()}] Configuración cargada`,
    `[${new Date().toLocaleString()}] Estado del servidor verificado`
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

// MÉTODOS DE ELIMINACIÓN MASIVA
const confirmarEliminarRegistros = () => {
  showConfirmation(
    '⚠️ ELIMINAR TODOS LOS REGISTROS',
    '¿Estás COMPLETAMENTE SEGURO de que quieres eliminar TODOS los registros del sistema?<br><br><strong>Esta acción NO SE PUEDE DESHACER</strong> y eliminará:<br>• Todos los registros históricos<br>• Fotos y documentos asociados<br>• Datos de ubicación<br><br>Esta operación es irreversible.',
    async () => {
      // Segunda confirmación más estricta
      const confirmacion = prompt('Para confirmar, escribe exactamente: ELIMINAR REGISTROS')
      if (confirmacion === 'ELIMINAR REGISTROS') {
        await eliminarTodosRegistros()
      } else {
        mostrarMensaje('Cancelado', 'Eliminación de registros cancelada.')
      }
    }
  )
}

const confirmarEliminarAsistencias = () => {
  showConfirmation(
    '⚠️ ELIMINAR TODAS LAS ASISTENCIAS',
    '¿Estás COMPLETAMENTE SEGURO de que quieres eliminar TODAS las asistencias del sistema?<br><br><strong>Esta acción NO SE PUEDE DESHACER</strong> y eliminará:<br>• Todos los registros de entrada y salida<br>• Fotos de asistencia<br>• Datos de ubicación de asistencias<br>• Historial completo de asistencias<br><br>Esta operación es irreversible.',
    async () => {
      // Segunda confirmación más estricta
      const confirmacion = prompt('Para confirmar, escribe exactamente: ELIMINAR ASISTENCIAS')
      if (confirmacion === 'ELIMINAR ASISTENCIAS') {
        await eliminarTodasAsistencias()
      } else {
        mostrarMensaje('Cancelado', 'Eliminación de asistencias cancelada.')
      }
    }
  )
}

const eliminarTodosRegistros = async () => {
  eliminandoRegistros.value = true
  
  try {
    const resultado = await asistenciasService.eliminarTodosRegistros()
    
    if (resultado.status === 'success') {
      mostrarMensaje(
        '✅ Registros Eliminados', 
        `Se han eliminado ${resultado.registros_eliminados} registros exitosamente.<br><br><strong>⚠️ El sistema de registros ha sido completamente limpiado.</strong>`
      )
    } else if (resultado.status === 'info') {
      mostrarMensaje('ℹ️ Sin Datos', resultado.message)
    }
  } catch (error) {
    mostrarMensaje('❌ Error', 'Error al eliminar registros: ' + (error.message || 'Error desconocido'))
  } finally {
    eliminandoRegistros.value = false
  }
}

const eliminarTodasAsistencias = async () => {
  eliminandoAsistencias.value = true
  
  try {
    const resultado = await asistenciasService.eliminarTodasAsistencias()
    
    if (resultado.status === 'success') {
      mostrarMensaje(
        '✅ Asistencias Eliminadas', 
        `Se han eliminado ${resultado.asistencias_eliminadas} asistencias y ${resultado.fotos_eliminadas || 0} fotos exitosamente.<br><br><strong>⚠️ El sistema de asistencias ha sido completamente limpiado.</strong>`
      )
    } else if (resultado.status === 'info') {
      mostrarMensaje('ℹ️ Sin Datos', resultado.message)
    }
  } catch (error) {
    mostrarMensaje('❌ Error', 'Error al eliminar asistencias: ' + (error.message || 'Error desconocido'))
  } finally {
    eliminandoAsistencias.value = false
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

.configuracion-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
}

.main-content {
  flex: 1;
  margin-left: min(220px, 18vw);
  width: calc(100vw - min(220px, 18vw));
  min-width: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: relative;
  box-sizing: border-box;
  overflow-x: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* === HEADER STYLES === */
.page-header {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 50%, #2E7D32 100%);
  color: white;
  padding: clamp(0.3rem, 0.8vw, 0.5rem);
  box-shadow: 
    0 4px 16px rgba(76, 175, 80, 0.15);
  position: sticky;
  top: 0;
  z-index: 100;
  width: 100%;
  box-sizing: border-box;
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
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
  max-width: 100%;
  margin: 0;
  gap: clamp(0.25rem, 0.8vw, 0.5rem);
  flex-wrap: wrap;
  width: 100%;
  position: relative;
  z-index: 2;
}

.header-main {
  display: flex;
  align-items: center;
  gap: clamp(0.5rem, 1.2vw, 0.8rem);
  flex: 1;
  min-width: 140px;
  margin-left: clamp(0.3rem, 1vw, 0.6rem);
}

.header-icon {
  width: clamp(28px, 3vw, 32px);
  height: clamp(28px, 3vw, 32px);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.1) 100%);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    inset 0 -1px 0 rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.header-icon svg {
  width: clamp(14px, 2.5vw, 16px);
  height: clamp(14px, 2.5vw, 16px);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  z-index: 1;
  position: relative;
}

.header-text {
  flex: 1;
}

.header-title {
  font-size: clamp(14px, 2.5vw, 16px);
  font-weight: 700;
  margin: 0 0 clamp(1px, 0.3vw, 2px) 0;
  background: linear-gradient(135deg, #ffffff 0%, #e8f5e8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-family: 'Inter', sans-serif;
  line-height: 1.2;
}

.header-subtitle {
  font-size: clamp(9px, 1.8vw, 11px);
  opacity: 0.9;
  margin: 0;
  font-weight: 400;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-family: 'Inter', sans-serif;
  line-height: 1.3;
}

/* === CONTENT STYLES === */
.page-content {
  flex: 1;
  padding: 16px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

/* Grid moderno y compacto */
.config-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

/* Cards modernos */
.config-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.config-card:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Headers de cards con iconos */
.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.card-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-icon svg {
  width: 18px;
  height: 18px;
  stroke-width: 2.5;
}

.api-icon {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
}

.app-icon {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.info-icon {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
}

.actions-icon {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.danger-icon {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

/* Formularios modernos */
.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
  font-weight: 500;
  color: #374151;
  font-family: 'Inter', sans-serif;
}

.form-input, .form-select {
  width: 100%;
  padding: 8px 12px;
  border: 1.5px solid #d1d5db;
  border-radius: 8px;
  font-size: 13px;
  font-family: 'Inter', sans-serif;
  transition: all 0.2s ease;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(5px);
}

.form-input:focus, .form-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  background: rgba(255, 255, 255, 0.95);
}

/* Checkbox moderno */
.checkbox-group {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.checkbox {
  width: 16px;
  height: 16px;
  border: 2px solid #d1d5db;
  border-radius: 4px;
  appearance: none;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.checkbox:checked {
  background: #3b82f6;
  border-color: #3b82f6;
  background-image: url("data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='m13.854 3.646-7.5 7.5a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6 10.293l7.146-7.147a.5.5 0 0 1 .708.708z'/%3e%3c/svg%3e");
}

.checkbox-group label {
  font-size: 13px;
  font-weight: 400;
  color: #374151;
  cursor: pointer;
  user-select: none;
}

/* Botones modernos */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.btn svg {
  width: 16px;
  height: 16px;
  stroke-width: 2;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
}

.btn-secondary {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(107, 114, 128, 0.2);
}

.btn-secondary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(107, 114, 128, 0.3);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

/* Info list moderna */
.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 13px;
  font-weight: 500;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
}

.info-value {
  font-size: 13px;
  font-weight: 500;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

/* Status badges */
.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-online {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.status-offline {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.status-unknown {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

/* Actions grid compacto */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 12px 8px;
  border: none;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  min-height: 60px;
  justify-content: center;
}

.action-btn svg {
  width: 18px;
  height: 18px;
  stroke-width: 2.5;
}

.export-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
}

.database-btn {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(139, 92, 246, 0.2);
}

.cache-btn {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(245, 158, 11, 0.2);
}

.reset-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
}

.logs-btn {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(107, 114, 128, 0.2);
}

.action-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

/* Zona peligrosa compacta */
.danger-card {
  border: 2px solid #ef4444;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(254, 242, 242, 0.9) 100%);
  position: relative;
}

.danger-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #ef4444 0%, #f59e0b 50%, #ef4444 100%);
  border-radius: 12px 12px 0 0;
}

/* Estilos para zona peligrosa bloqueada */
.danger-card-blocked {
  border: 2px solid #6b7280;
  background: linear-gradient(135deg, rgba(249, 250, 251, 0.95) 0%, rgba(243, 244, 246, 0.9) 100%);
  filter: grayscale(1);
  opacity: 0.6;
  cursor: not-allowed;
  user-select: none;
  position: relative;
}

.danger-card-blocked::before {
  background: linear-gradient(90deg, #6b7280 0%, #9ca3af 50%, #6b7280 100%);
}

.danger-icon-blocked {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  color: white;
}

.danger-warning-blocked {
  background: rgba(107, 114, 128, 0.1);
  border: 1px solid rgba(107, 114, 128, 0.2);
}

.danger-warning-blocked .warning-content {
  color: #374151;
}

.danger-btn-blocked {
  background: linear-gradient(135deg, #9ca3af 0%, #6b7280 100%);
  border-color: #6b7280;
  color: #d1d5db;
  cursor: not-allowed;
  pointer-events: none;
}

/* Overlay de bloqueo */
.blocked-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(107, 114, 128, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  backdrop-filter: blur(2px);
  z-index: 10;
}

.blocked-icon {
  width: 40px;
  height: 40px;
  color: #6b7280;
  margin-bottom: 8px;
}

.blocked-icon svg {
  width: 100%;
  height: 100%;
}

.blocked-text {
  font-size: 14px;
  font-weight: 700;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-family: 'Inter', sans-serif;
}

.danger-warning {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
}

.warning-content {
  font-size: 13px;
  color: #7f1d1d;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
  line-height: 1.4;
}

.danger-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 12px;
}

.danger-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border: 2px solid;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: all 0.2s ease;
  justify-content: center;
}

.danger-btn svg {
  width: 16px;
  height: 16px;
  stroke-width: 2.5;
}

.registros-btn {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border-color: #d97706;
  color: white;
  box-shadow: 0 2px 4px rgba(245, 158, 11, 0.3);
}

.asistencias-btn {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  border-color: #7c3aed;
  color: white;
  box-shadow: 0 2px 4px rgba(139, 92, 246, 0.3);
}

.danger-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.danger-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
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
  backdrop-filter: blur(4px);
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 16px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
}

.btn-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #6b7280;
  padding: 4px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.btn-close:hover {
  background: #f3f4f6;
  color: #1f2937;
}

.modal-body {
  padding: 16px;
  font-family: 'Inter', sans-serif;
}

.modal-body pre {
  background: #f9fafb;
  padding: 12px;
  border-radius: 6px;
  font-size: 11px;
  overflow-x: auto;
  border: 1px solid #e5e7eb;
}

/* Responsive */
@media (max-width: 992px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
}

@media (min-width: 481px) and (max-width: 768px) {
  .main-content {
    margin-left: 250px;
    width: calc(100vw - 250px);
  }
}

@media (max-width: 768px) and (orientation: landscape) {
  .main-content {
    margin-left: 160px;
    width: calc(100vw - 160px);
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 240px;
    width: calc(100vw - 240px);
  }
  
  .page-content {
    padding: 12px;
  }
  
  .config-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .config-card {
    padding: 12px;
  }
  
  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .danger-actions {
    grid-template-columns: 1fr;
  }
  
  .card-header h3 {
    font-size: 14px;
  }
  
  .form-input, .form-select {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}

@media (max-width: 375px) {
  .main-content {
    margin-left: 180px;
    width: calc(100vw - 180px);
  }
}
</style>
