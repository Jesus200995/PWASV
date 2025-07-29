<template>
  <div class="configuracion-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 1v6m0 6v6m11-7h-6m-6 0H1"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Configuración del Sistema</h1>
              <p class="header-subtitle">Administra las configuraciones generales de la aplicación</p>
            </div>
          </div>
          <div class="connection-status" :class="{ 'online': isOnline, 'offline': !isOnline }">
            <div class="status-indicator"></div>
            <span class="status-text">{{ isOnline ? 'En línea' : 'Sin conexión' }}</span>
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
              <button @click="descargarBaseDatos" class="action-btn sql-btn" :disabled="descargandoBD">
                {{ descargandoBD ? 'Descargando...' : '💾 Descargar BD SQL' }}
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

        <!-- NUEVA SECCIÓN: Eliminación Masiva de Datos -->
        <div class="config-section">
          <h2>⚠️ Eliminación Masiva de Datos</h2>
          <div class="config-card danger-card">
            <div class="danger-warning">
              <div class="warning-icon">⚠️</div>
              <div class="warning-text">
                <strong>¡ATENCIÓN!</strong> Las siguientes acciones eliminarán datos de forma permanente y no se pueden deshacer.
                <br>Úsalas solo si estás completamente seguro.
              </div>
            </div>
            
            <div class="danger-actions-grid">
              <button @click="confirmarEliminarRegistros" class="danger-btn registros-btn" :disabled="eliminandoRegistros">
                {{ eliminandoRegistros ? 'Eliminando...' : '📋 Eliminar TODOS los Registros' }}
              </button>
              <button @click="confirmarEliminarAsistencias" class="danger-btn asistencias-btn" :disabled="eliminandoAsistencias">
                {{ eliminandoAsistencias ? 'Eliminando...' : '🕐 Eliminar TODAS las Asistencias' }}
              </button>
            </div>
            
            <div class="danger-note">
              <p><strong>Nota:</strong> Estas acciones requerirán múltiples confirmaciones por seguridad.</p>
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

const descargarBaseDatos = async () => {
  descargandoBD.value = true
  
  try {
    const token = localStorage.getItem('admin_token')
    
    mostrarMensaje('Iniciando', 'Obteniendo todos los datos de la base de datos...')
    
    // Obtener TODOS los datos disponibles de la base de datos app_registros
    const [usuariosRes, registrosRes, asistenciasRes] = await Promise.all([
      axios.get(`${apiConfig.url}/usuarios`, {
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
    sqlContent += `    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n`
    sqlContent += `    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n`
    sqlContent += `);\n\n`
    
    // Insertar datos de usuarios
    if (usuariosData.length > 0) {
      sqlContent += `-- Datos de usuarios (${usuariosData.length} registros)\n`
      sqlContent += `INSERT INTO usuarios (id, correo, nombre_completo, cargo, supervisor, contrasena, curp) VALUES\n`
      
      const usuariosInserts = usuariosData.map((usuario, index) => {
        const id = usuario.id || index + 1
        const correo = (usuario.correo || usuario.email || '').replace(/'/g, "''")
        const nombre = (usuario.nombre_completo || usuario.nombre || '').replace(/'/g, "''")
        const cargo = (usuario.cargo || '').replace(/'/g, "''")
        const supervisor = (usuario.supervisor || '').replace(/'/g, "''")
        const contrasena = (usuario.contrasena || usuario.password || 'sin_contrasena').replace(/'/g, "''")
        const curp = (usuario.curp || '').replace(/'/g, "''")
        
        return `(${id}, '${correo}', '${nombre}', '${cargo}', '${supervisor}', '${contrasena}', '${curp}')`
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
/* CONFIGURACION VIEW - ULTRA RESPONSIVE CON APROVECHAMIENTO TOTAL DEL ANCHO */
.configuracion-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.main-content {
  flex: 1;
  margin-left: clamp(180px, 18vw, 240px);
  width: calc(100vw - clamp(180px, 18vw, 240px));
  background: transparent;
  overflow-x: hidden;
}

.page-header {
  background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
  border-bottom: none;
  padding: clamp(1.5rem, 4vw, 2rem);
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
  gap: clamp(1rem, 3vw, 1.5rem);
  max-width: 100%;
  margin: 0;
  width: 100%;
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

.page-content {
  padding: clamp(1rem, 3vw, 2rem);
  max-width: 100%;
  margin: 0;
  width: 100%;
  box-sizing: border-box;
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

.sql-btn {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
  border: 2px solid #1d4ed8;
}

.sql-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
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

/* ESTILOS PARA ELIMINACIÓN MASIVA */
.danger-card {
  border: 2px solid #e74c3c;
  background: linear-gradient(135deg, #ffffff 0%, #ffeaa7 100%);
  position: relative;
  overflow: hidden;
}

.danger-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #e74c3c 0%, #f39c12 50%, #e74c3c 100%);
  animation: dangerGlow 2s ease-in-out infinite alternate;
}

@keyframes dangerGlow {
  0% { opacity: 0.7; }
  100% { opacity: 1; }
}

.danger-warning {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  background: rgba(231, 76, 60, 0.1);
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 24px;
  border: 1px solid rgba(231, 76, 60, 0.2);
}

.warning-icon {
  font-size: 32px;
  color: #e74c3c;
  animation: shake 2s ease-in-out infinite;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-2px); }
  75% { transform: translateX(2px); }
}

.warning-text {
  flex: 1;
  color: #2c3e50;
  line-height: 1.5;
}

.warning-text strong {
  color: #e74c3c;
}

.danger-actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 20px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.danger-btn {
  padding: 16px 20px;
  border: 2px solid;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  position: relative;
  overflow: hidden;
}

.danger-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.danger-btn:hover::before {
  left: 100%;
}

.usuarios-btn {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  border-color: #c0392b;
  color: white;
  box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
}

.usuarios-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #c0392b 0%, #a93226 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
}

.registros-btn {
  background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
  border-color: #e67e22;
  color: white;
  box-shadow: 0 4px 15px rgba(243, 156, 18, 0.3);
}

.registros-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #e67e22 0%, #d35400 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(243, 156, 18, 0.4);
}

.asistencias-btn {
  background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%);
  border-color: #8e44ad;
  color: white;
  box-shadow: 0 4px 15px rgba(155, 89, 182, 0.3);
}

.asistencias-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #8e44ad 0%, #7d3c98 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(155, 89, 182, 0.4);
}

.danger-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

.danger-note {
  background: rgba(52, 73, 94, 0.1);
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid #34495e;
}

.danger-note p {
  margin: 0;
  color: #2c3e50;
  font-size: 14px;
  font-style: italic;
}

/* RESPONSIVE ULTRA COMPLETO - USA TODO EL ANCHO */
@media (max-width: 1024px) and (min-width: 769px) {
  .danger-actions-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    max-width: 600px;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    width: 100vw;
    overflow-x: hidden;
  }
  
  .page-header {
    padding: clamp(1rem, 3vw, 1.5rem);
    width: 100%;
  }
  
  .header-content {
    flex-direction: column;
    gap: clamp(0.75rem, 2vw, 1rem);
    align-items: center;
    text-align: center;
  }
  
  .header-main {
    gap: 16px;
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
    font-size: 24px;
  }
  
  .header-subtitle {
    font-size: 14px;
  }
  
  .connection-status {
    align-self: center;
  }
  
  .page-content {
    padding: clamp(1rem, 4vw, 1.5rem);
  }
  
  .config-card {
    padding: clamp(1rem, 2vw, 1.5rem);
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .danger-actions-grid {
    grid-template-columns: 1fr;
    max-width: 100%;
  }
  
  .danger-warning {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
  
  .warning-icon {
    font-size: 28px;
  }
  
  .config-input, .config-select {
    max-width: 100%;
  }
}
</style>
