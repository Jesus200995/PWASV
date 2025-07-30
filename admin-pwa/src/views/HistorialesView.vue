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
              <p class="header-subtitle">Consulta y gestiona el historial completo de actividades de los usuarios</p>
            </div>
          </div>
          <div class="header-actions">
            <div class="connection-status" :class="{ 'online': isOnline, 'offline': !isOnline }">
              <div class="status-indicator"></div>
              <span class="status-text">{{ isOnline ? 'En línea' : 'Sin conexión' }}</span>
            </div>
            <button @click="actualizarHistorial" class="refresh-btn" :disabled="loading">
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
        <!-- Selección de Usuario -->
        <div class="user-selection-section">
          <div class="selection-card">
            <div class="selection-header">
              <h3>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                Seleccionar Usuario
              </h3>
            </div>
            <div class="user-selector">
              <select v-model="usuarioSeleccionado" @change="onUsuarioChange" class="user-select">
                <option value="">Selecciona un usuario...</option>
                <option v-for="usuario in usuarios" :key="usuario.id" :value="usuario.id">
                  {{ usuario.nombre_completo }} - {{ usuario.correo }}
                </option>
              </select>
            </div>
          </div>
        </div>

        <!-- Filtros y Controles - Solo visible si hay usuario seleccionado -->
        <div v-if="usuarioSeleccionado" class="filters-section">
          <div class="filters-card">
            <div class="filters-header">
              <h3>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
                </svg>
                Filtros de Búsqueda
              </h3>
            </div>
            
            <div class="filters-grid">
              <!-- Filtros por fecha -->
              <div class="filter-group">
                <label>Tipo de período:</label>
                <div class="period-buttons">
                  <button 
                    @click="setPeriodo('dia')"
                    :class="['period-btn', { active: filtros.periodo === 'dia' }]"
                  >
                    Día
                  </button>
                  <button 
                    @click="setPeriodo('semana')"
                    :class="['period-btn', { active: filtros.periodo === 'semana' }]"
                  >
                    Semana
                  </button>
                  <button 
                    @click="setPeriodo('año')"
                    :class="['period-btn', { active: filtros.periodo === 'año' }]"
                  >
                    Año
                  </button>
                  <button 
                    @click="setPeriodo('todo')"
                    :class="['period-btn', { active: filtros.periodo === 'todo' }]"
                  >
                    Todo
                  </button>
                </div>
              </div>

              <!-- Selector de fecha específica (solo para día) -->
              <div v-if="filtros.periodo === 'dia'" class="filter-group">
                <label for="fecha-especifica">Fecha:</label>
                <input
                  id="fecha-especifica"
                  type="date"
                  v-model="filtros.fechaEspecifica"
                  @change="aplicarFiltros"
                  class="date-input"
                >
              </div>

              <!-- Selector de semana (solo para semana) -->
              <div v-if="filtros.periodo === 'semana'" class="filter-group">
                <label for="semana-especifica">Semana:</label>
                <input
                  id="semana-especifica"
                  type="week"
                  v-model="filtros.semanaEspecifica"
                  @change="aplicarFiltros"
                  class="date-input"
                >
              </div>

              <!-- Selector de año (solo para año) -->
              <div v-if="filtros.periodo === 'año'" class="filter-group">
                <label for="año-especifico">Año:</label>
                <select
                  id="año-especifico"
                  v-model="filtros.añoEspecifico"
                  @change="aplicarFiltros"
                  class="year-select"
                >
                  <option v-for="año in añosDisponibles" :key="año" :value="año">
                    {{ año }}
                  </option>
                </select>
              </div>

              <!-- Filtro por tipo -->
              <div class="filter-group">
                <label for="tipo-filtro">Tipo de actividad:</label>
                <select
                  id="tipo-filtro"
                  v-model="filtros.tipo"
                  @change="aplicarFiltros"
                  class="type-select"
                >
                  <option value="">Todos los tipos</option>
                  <option value="entrada">Entrada</option>
                  <option value="salida">Salida</option>
                  <option value="actividad">Actividad</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- Estadísticas Rápidas -->
        <div v-if="usuarioSeleccionado && resumen" class="stats-section">
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon total">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 12l2 2 4-4"></path>
                  <path d="M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9 9 4.03 9 9z"></path>
                </svg>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ resumen.estadisticas.total_registros }}</div>
                <div class="stat-label">Total Registros</div>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon entrada">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="12" y1="19" x2="12" y2="5"></line>
                  <polyline points="5,12 12,5 19,12"></polyline>
                </svg>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ resumen.estadisticas.entradas }}</div>
                <div class="stat-label">Entradas</div>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon salida">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <polyline points="19,12 12,19 5,12"></polyline>
                </svg>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ resumen.estadisticas.salidas }}</div>
                <div class="stat-label">Salidas</div>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon actividad">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="3"></circle>
                  <path d="M12 1v6m0 6v6m11-7h-6m-6 0H1"></path>
                </svg>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ resumen.estadisticas.actividades }}</div>
                <div class="stat-label">Actividades</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Historial -->
        <div v-if="usuarioSeleccionado" class="historial-section">
          <div class="historial-header">
            <h3>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              Historial de {{ usuarioActual?.nombre || 'Usuario' }}
            </h3>
            <div class="historial-actions">
              <span v-if="historial.length > 0" class="record-count">
                {{ historial.length }} registro(s) encontrado(s)
              </span>
              <button 
                v-if="historial.length > 0"
                @click="exportarExcel" 
                class="export-btn"
                :disabled="exportando"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14,2 14,8 20,8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="21"></line>
                  <line x1="8" y1="13" x2="16" y2="21"></line>
                </svg>
                {{ exportando ? 'Exportando...' : 'Exportar Excel' }}
              </button>
            </div>
          </div>

          <!-- Loading -->
          <div v-if="loading" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando historial...</p>
          </div>

          <!-- Error -->
          <div v-else-if="error" class="error-container">
            <div class="error-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="15" y1="9" x2="9" y2="15"></line>
                <line x1="9" y1="9" x2="15" y2="15"></line>
              </svg>
            </div>
            <h3>Error al cargar el historial</h3>
            <p>{{ error }}</p>
            <button @click="cargarHistorial" class="retry-btn">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
                <path d="M3 3v5h5"></path>
                <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"></path>
                <path d="M21 21v-5h-5"></path>
              </svg>
              Reintentar
            </button>
          </div>

          <!-- Sin registros -->
          <div v-else-if="historial.length === 0" class="empty-state">
            <div class="empty-icon">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <h3>No hay registros</h3>
            <p>No se encontraron registros para los filtros seleccionados.</p>
          </div>

          <!-- Tabla de historial -->
          <div v-else class="historial-table-container">
            <div class="table-wrapper">
              <table class="historial-table">
                <thead>
                  <tr>
                    <th>Origen</th>
                    <th>Tipo</th>
                    <th>Descripción</th>
                    <th>Fecha</th>
                    <th>Hora</th>
                    <th>Detalles</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="registro in historial" :key="registro.id" class="registro-row">
                    <td>
                      <span :class="['origen-badge', registro.origen]">
                        {{ formatearOrigen(registro.origen) }}
                      </span>
                    </td>
                    <td>
                      <span :class="['tipo-badge', registro.tipo]">
                        {{ formatearTipo(registro.tipo) }}
                      </span>
                    </td>
                    <td class="descripcion-cell">
                      {{ registro.descripcion || 'Sin descripción' }}
                    </td>
                    <td class="fecha-cell">
                      {{ formatearFecha(registro.fecha) }}
                    </td>
                    <td class="hora-cell">
                      {{ formatearHora(registro.hora) }}
                    </td>
                    <td class="detalles-cell">
                      <button 
                        v-if="registro.detalles"
                        @click="mostrarDetalles(registro)"
                        class="details-btn"
                      >
                        Ver detalles
                      </button>
                      <span v-else class="no-details">Sin detalles</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Estado inicial -->
        <div v-else class="welcome-section">
          <div class="welcome-card">
            <div class="welcome-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <h2>Historial de Usuarios</h2>
            <p>Selecciona un usuario de la lista superior para ver su historial completo de actividades.</p>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal de detalles -->
    <div v-if="modalDetalles.visible" class="modal-overlay" @click="cerrarModalDetalles">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Detalles del Registro</h3>
          <button @click="cerrarModalDetalles" class="close-btn">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="detail-grid">
            <div class="detail-item">
              <strong>Tipo:</strong>
              <span :class="['tipo-badge', modalDetalles.registro?.tipo]">
                {{ formatearTipo(modalDetalles.registro?.tipo) }}
              </span>
            </div>
            <div class="detail-item">
              <strong>Descripción:</strong>
              <span>{{ modalDetalles.registro?.descripcion || 'Sin descripción' }}</span>
            </div>
            <div class="detail-item">
              <strong>Fecha y Hora:</strong>
              <span>{{ formatearFechaHora(modalDetalles.registro?.fecha, modalDetalles.registro?.hora) }}</span>
            </div>
            <div v-if="modalDetalles.registro?.detalles" class="detail-item full-width">
              <strong>Información adicional:</strong>
              <pre class="json-display">{{ JSON.stringify(modalDetalles.registro.detalles, null, 2) }}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { useRouter } from 'vue-router'
import usuariosService from '../services/usuariosService.js'
import historialService from '../services/historialService.js'
import * as XLSX from 'xlsx'

export default {
  name: 'HistorialesView',
  components: {
    Sidebar
  },
  setup() {
    const router = useRouter()
    
    // Estados reactivos
    const isOnline = ref(navigator.onLine)
    const loading = ref(false)
    const exportando = ref(false)
    const error = ref('')
    const usuarios = ref([])
    const usuarioSeleccionado = ref('')
    const historial = ref([])
    const resumen = ref(null)
    const usuarioActual = ref(null)
    
    // Filtros
    const filtros = ref({
      periodo: 'todo', // 'dia', 'semana', 'año', 'todo'
      fechaEspecifica: new Date().toISOString().split('T')[0],
      semanaEspecifica: '',
      añoEspecifico: new Date().getFullYear(),
      tipo: '' // '', 'entrada', 'salida', 'actividad'
    })

    // Modal de detalles
    const modalDetalles = ref({
      visible: false,
      registro: null
    })

    // Años disponibles
    const añosDisponibles = computed(() => {
      const currentYear = new Date().getFullYear()
      const years = []
      for (let i = currentYear; i >= currentYear - 10; i--) {
        years.push(i)
      }
      return years
    })

    // Admin user
    const adminUser = computed(() => {
      const userData = localStorage.getItem('userData')
      if (userData) {
        const user = JSON.parse(userData)
        return user.nombre || 'Administrador'
      }
      return 'Administrador'
    })

    // Watchers
    watch(usuarioSeleccionado, (newUserId) => {
      if (newUserId) {
        // Convertir a número para asegurar compatibilidad
        const userId = parseInt(newUserId)
        usuarioActual.value = usuarios.value.find(u => u.id === userId)
        cargarResumen()
        cargarHistorial()
      } else {
        usuarioActual.value = null
        historial.value = []
        resumen.value = null
      }
    })

    // Métodos principales
    const cargarUsuarios = async () => {
      try {
        console.log('🔍 Cargando usuarios...')
        const usuariosData = await historialService.obtenerUsuarios()
        usuarios.value = usuariosData.usuarios || usuariosData || []
        console.log(`✅ ${usuarios.value.length} usuarios cargados`)
      } catch (err) {
        console.error('❌ Error al cargar usuarios:', err)
        error.value = 'Error al cargar la lista de usuarios'
      }
    }

    const cargarHistorial = async () => {
      if (!usuarioSeleccionado.value) {
        console.log('⚠️ No hay usuario seleccionado')
        return
      }

      loading.value = true
      error.value = ''
      
      try {
        const userId = parseInt(usuarioSeleccionado.value)
        console.log('🔍 Cargando historial completo para usuario ID:', userId)
        console.log('🔍 Filtros aplicados:', filtros.value)
        
        const filtrosAPI = construirFiltrosAPI()
        console.log('🔍 Filtros API:', filtrosAPI)
        
        // Usar el nuevo método de historial completo
        const data = await historialService.obtenerHistorialCompleto(userId, filtrosAPI)
        
        historial.value = data.historial || []
        resumen.value = {
          estadisticas: data.estadisticas || {
            total_registros: 0,
            entradas: 0,
            salidas: 0,
            actividades: 0
          }
        }
        
        console.log(`✅ ${historial.value.length} registros de historial completo cargados`)
        console.log('📊 Estadísticas:', resumen.value.estadisticas)
        
        if (historial.value.length === 0) {
          console.log('⚠️ No se encontraron registros para este usuario con los filtros aplicados')
        }
        
      } catch (err) {
        console.error('❌ Error al cargar historial:', err)
        error.value = err.message || 'Error al cargar el historial'
        historial.value = []
        resumen.value = null
        
        // Si es error 404, mostrar mensaje más amigable
        if (err.message.includes('404') || err.message.includes('no encontrado')) {
          error.value = 'Usuario no encontrado o sin historial disponible'
        }
      } finally {
        loading.value = false
      }
    }

    const cargarResumen = async () => {
      // Ya no necesitamos cargar resumen por separado
      // El historial completo ya incluye las estadísticas
      console.log('📊 Resumen incluido en historial completo')
    }

    const construirFiltrosAPI = () => {
      const filtrosAPI = {}

      switch (filtros.value.periodo) {
        case 'dia':
          if (filtros.value.fechaEspecifica) {
            filtrosAPI.fechaInicio = filtros.value.fechaEspecifica
            filtrosAPI.fechaFin = filtros.value.fechaEspecifica
          }
          break
          
        case 'semana':
          if (filtros.value.semanaEspecifica) {
            const fechasSemana = calcularFechasSemana(filtros.value.semanaEspecifica)
            filtrosAPI.fechaInicio = fechasSemana.inicio
            filtrosAPI.fechaFin = fechasSemana.fin
          }
          break
          
        case 'año':
          filtrosAPI.fechaInicio = `${filtros.value.añoEspecifico}-01-01`
          filtrosAPI.fechaFin = `${filtros.value.añoEspecifico}-12-31`
          break
          
        // Para 'todo' no agregamos filtros de fecha
      }

      if (filtros.value.tipo) {
        filtrosAPI.tipo = filtros.value.tipo
      }

      return filtrosAPI
    }

    const calcularFechasSemana = (semanaString) => {
      // semanaString viene en formato "2024-W30"
      const [year, week] = semanaString.split('-W')
      const yearNum = parseInt(year)
      const weekNum = parseInt(week)
      
      // Calcular el primer día de la semana
      const firstDayOfYear = new Date(yearNum, 0, 1)
      const daysToFirstMonday = (8 - firstDayOfYear.getDay()) % 7
      const firstMonday = new Date(yearNum, 0, 1 + daysToFirstMonday)
      
      const targetDate = new Date(firstMonday)
      targetDate.setDate(firstMonday.getDate() + (weekNum - 1) * 7)
      
      const inicio = new Date(targetDate)
      const fin = new Date(targetDate)
      fin.setDate(inicio.getDate() + 6)
      
      return {
        inicio: inicio.toISOString().split('T')[0],
        fin: fin.toISOString().split('T')[0]
      }
    }

    // Métodos de UI
    const setPeriodo = (periodo) => {
      filtros.value.periodo = periodo
      
      // Configurar valores por defecto según el período
      switch (periodo) {
        case 'dia':
          filtros.value.fechaEspecifica = new Date().toISOString().split('T')[0]
          break
        case 'semana':
          const semanaActual = historialService.obtenerSemanaActual()
          const fechaActual = new Date()
          const año = fechaActual.getFullYear()
          const semana = getWeekNumber(fechaActual)
          filtros.value.semanaEspecifica = `${año}-W${semana.toString().padStart(2, '0')}`
          break
        case 'año':
          filtros.value.añoEspecifico = new Date().getFullYear()
          break
      }
      
      aplicarFiltros()
    }

    const getWeekNumber = (date) => {
      const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()))
      const dayNum = d.getUTCDay() || 7
      d.setUTCDate(d.getUTCDate() + 4 - dayNum)
      const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1))
      return Math.ceil((((d - yearStart) / 86400000) + 1) / 7)
    }

    const aplicarFiltros = () => {
      if (usuarioSeleccionado.value) {
        cargarHistorial()
      }
    }

    const actualizarHistorial = () => {
      if (usuarioSeleccionado.value) {
        cargarHistorial()
        cargarResumen()
      } else {
        cargarUsuarios()
      }
    }

    const onUsuarioChange = () => {
      error.value = ''
    }

    // Métodos de formato
    const formatearOrigen = (origen) => {
      const origenes = {
        historial: 'Historial',
        registros: 'Actividades',
        asistencias: 'Asistencia'
      }
      return origenes[origen] || origen
    }

    const formatearTipo = (tipo) => {
      return historialService.formatearTipo(tipo)
    }

    const formatearFecha = (fecha) => {
      return historialService.formatearFecha(fecha)
    }

    const formatearHora = (hora) => {
      return historialService.formatearHora(hora)
    }

    const formatearFechaHora = (fecha, hora) => {
      if (!fecha || !hora) return 'N/A'
      
      try {
        const fechaObj = new Date(fecha + 'T' + hora)
        return fechaObj.toLocaleString('es-ES', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        })
      } catch (error) {
        return `${formatearFecha(fecha)} ${formatearHora(hora)}`
      }
    }

    // Métodos de modal
    const mostrarDetalles = (registro) => {
      modalDetalles.value = {
        visible: true,
        registro: registro
      }
    }

    const cerrarModalDetalles = () => {
      modalDetalles.value = {
        visible: false,
        registro: null
      }
    }

    // Exportar a Excel
    const exportarExcel = async () => {
      if (historial.value.length === 0) return

      exportando.value = true
      
      try {
        console.log('📊 Generando archivo Excel...')
        
        const datosExcel = historialService.generarDatosExcel(
          historial.value, 
          usuarioActual.value?.nombre_completo || 'Usuario'
        )

        // Crear libro de trabajo
        const workbook = XLSX.utils.book_new()
        const worksheet = XLSX.utils.json_to_sheet(datosExcel.datos)

        // Ajustar anchos de columnas
        const columnWidths = [
          { wch: 8 },   // ID
          { wch: 25 },  // Usuario
          { wch: 30 },  // Correo
          { wch: 12 },  // Tipo
          { wch: 40 },  // Descripción
          { wch: 12 },  // Fecha
          { wch: 10 },  // Hora
          { wch: 18 }   // Creado en
        ]
        worksheet['!cols'] = columnWidths

        // Agregar hoja al libro
        XLSX.utils.book_append_sheet(workbook, worksheet, datosExcel.nombreHoja)

        // Descargar archivo
        XLSX.writeFile(workbook, datosExcel.nombreArchivo)
        
        console.log('✅ Archivo Excel generado:', datosExcel.nombreArchivo)
        
      } catch (err) {
        console.error('❌ Error al exportar Excel:', err)
        error.value = 'Error al generar el archivo Excel'
      } finally {
        exportando.value = false
      }
    }

    // Métodos de sistema
    const logout = () => {
      localStorage.removeItem('userData')
      localStorage.removeItem('token')
      router.push('/login')
    }

    const updateOnlineStatus = () => {
      isOnline.value = navigator.onLine
    }

    // Lifecycle
    onMounted(async () => {
      window.addEventListener('online', updateOnlineStatus)
      window.addEventListener('offline', updateOnlineStatus)
      
      // Probar conectividad primero
      try {
        await historialService.probarConectividad()
        console.log('✅ Conectividad con backend confirmada')
      } catch (err) {
        console.error('❌ Error de conectividad:', err)
        error.value = 'No se puede conectar con el servidor. Verifica que esté funcionando.'
      }
      
      await cargarUsuarios()
      
      // Configurar semana inicial
      const fechaActual = new Date()
      const año = fechaActual.getFullYear()
      const semana = getWeekNumber(fechaActual)
      filtros.value.semanaEspecifica = `${año}-W${semana.toString().padStart(2, '0')}`
    })

    return {
      // Estados
      isOnline,
      loading,
      exportando,
      error,
      usuarios,
      usuarioSeleccionado,
      historial,
      resumen,
      usuarioActual,
      filtros,
      modalDetalles,
      añosDisponibles,
      adminUser,
      
      // Métodos principales
      cargarHistorial,
      actualizarHistorial,
      onUsuarioChange,
      
      // Métodos de filtros
      setPeriodo,
      aplicarFiltros,
      
      // Métodos de formato
      formatearOrigen,
      formatearTipo,
      formatearFecha,
      formatearHora,
      formatearFechaHora,
      
      // Métodos de modal
      mostrarDetalles,
      cerrarModalDetalles,
      
      // Exportar
      exportarExcel,
      
      // Sistema
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
  display: flex;
  flex-direction: column;
  gap: clamp(12px, 2.5vw, 20px);
}

/* Sección de selección de usuario */
.user-selection-section {
  width: 100%;
}

.selection-card {
  background: white;
  border-radius: clamp(10px, 2vw, 16px);
  padding: clamp(16px, 3vw, 24px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
}

.selection-header {
  margin-bottom: clamp(12px, 2.5vw, 16px);
}

.selection-header h3 {
  display: flex;
  align-items: center;
  gap: clamp(8px, 1.5vw, 10px);
  font-size: clamp(16px, 3vw, 20px);
  font-weight: 600;
  color: #2c5530;
  margin: 0;
}

.selection-header svg {
  color: #27ae60;
}

.user-selector {
  width: 100%;
}

.user-select {
  width: 100%;
  padding: clamp(10px, 2vw, 14px);
  border: 2px solid #e9ecef;
  border-radius: clamp(8px, 1.5vw, 10px);
  font-size: clamp(14px, 2.5vw, 16px);
  background: white;
  color: #495057;
  transition: all 0.3s ease;
}

.user-select:focus {
  outline: none;
  border-color: #2ecc71;
  box-shadow: 0 0 0 3px rgba(46, 204, 113, 0.1);
}

/* Sección de filtros */
.filters-section {
  width: 100%;
}

.filters-card {
  background: white;
  border-radius: clamp(10px, 2vw, 16px);
  padding: clamp(16px, 3vw, 24px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
}

.filters-header {
  margin-bottom: clamp(16px, 3vw, 20px);
}

.filters-header h3 {
  display: flex;
  align-items: center;
  gap: clamp(8px, 1.5vw, 10px);
  font-size: clamp(16px, 3vw, 20px);
  font-weight: 600;
  color: #2c5530;
  margin: 0;
}

.filters-header svg {
  color: #27ae60;
}

.filters-grid {
  display: grid;
  gap: clamp(16px, 3vw, 20px);
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: clamp(6px, 1.2vw, 8px);
}

.filter-group label {
  font-size: clamp(14px, 2.5vw, 16px);
  font-weight: 500;
  color: #495057;
}

.period-buttons {
  display: flex;
  gap: clamp(6px, 1.2vw, 8px);
  flex-wrap: wrap;
}

.period-btn {
  padding: clamp(8px, 1.5vw, 10px) clamp(12px, 2.5vw, 16px);
  border: 2px solid #e9ecef;
  background: white;
  border-radius: clamp(6px, 1.2vw, 8px);
  font-size: clamp(12px, 2.2vw, 14px);
  font-weight: 500;
  color: #6c757d;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.period-btn:hover {
  border-color: #2ecc71;
  color: #2ecc71;
}

.period-btn.active {
  background: #2ecc71;
  border-color: #2ecc71;
  color: white;
}

.date-input, .year-select, .type-select {
  padding: clamp(8px, 1.5vw, 10px);
  border: 2px solid #e9ecef;
  border-radius: clamp(6px, 1.2vw, 8px);
  font-size: clamp(14px, 2.5vw, 16px);
  background: white;
  color: #495057;
  transition: all 0.3s ease;
}

.date-input:focus, .year-select:focus, .type-select:focus {
  outline: none;
  border-color: #2ecc71;
  box-shadow: 0 0 0 3px rgba(46, 204, 113, 0.1);
}

/* Sección de estadísticas */
.stats-section {
  width: 100%;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: clamp(12px, 2.5vw, 16px);
}

.stat-card {
  background: white;
  border-radius: clamp(10px, 2vw, 14px);
  padding: clamp(16px, 3vw, 20px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
  display: flex;
  align-items: center;
  gap: clamp(12px, 2.5vw, 16px);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  width: clamp(40px, 8vw, 48px);
  height: clamp(40px, 8vw, 48px);
  border-radius: clamp(8px, 1.5vw, 10px);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon.total {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
}

.stat-icon.entrada {
  background: linear-gradient(135deg, #27ae60, #229954);
  color: white;
}

.stat-icon.salida {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
}

.stat-icon.actividad {
  background: linear-gradient(135deg, #f39c12, #d68910);
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: clamp(20px, 4vw, 28px);
  font-weight: 700;
  color: #2c5530;
  margin: 0;
  line-height: 1;
}

.stat-label {
  font-size: clamp(12px, 2.2vw, 14px);
  color: #6c757d;
  margin: clamp(4px, 0.8vw, 6px) 0 0 0;
  font-weight: 500;
}

/* Sección de historial */
.historial-section {
  background: white;
  border-radius: clamp(10px, 2vw, 16px);
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
  min-height: 400px;
  display: flex;
  flex-direction: column;
}

.historial-header {
  padding: clamp(16px, 3vw, 20px);
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: clamp(12px, 2.5vw, 16px);
}

.historial-header h3 {
  display: flex;
  align-items: center;
  gap: clamp(8px, 1.5vw, 10px);
  font-size: clamp(16px, 3vw, 20px);
  font-weight: 600;
  color: #2c5530;
  margin: 0;
}

.historial-header svg {
  color: #27ae60;
}

.historial-actions {
  display: flex;
  align-items: center;
  gap: clamp(12px, 2.5vw, 16px);
  flex-wrap: wrap;
}

.record-count {
  font-size: clamp(12px, 2.2vw, 14px);
  color: #6c757d;
  white-space: nowrap;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: clamp(6px, 1.2vw, 8px);
  padding: clamp(8px, 1.5vw, 10px) clamp(12px, 2.5vw, 16px);
  background: #27ae60;
  border: none;
  border-radius: clamp(6px, 1.2vw, 8px);
  color: white;
  font-size: clamp(12px, 2.2vw, 14px);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.export-btn:hover:not(:disabled) {
  background: #229954;
  transform: translateY(-1px);
}

.export-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Estados de carga y error */
.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: clamp(40px, 8vw, 60px);
  text-align: center;
  flex: 1;
}

.spinner-large {
  width: clamp(32px, 6vw, 48px);
  height: clamp(32px, 6vw, 48px);
  border: 3px solid #f3f3f3;
  border-top: 3px solid #2ecc71;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: clamp(16px, 3vw, 20px);
}

.loading-container p, .error-container p {
  color: #6c757d;
  font-size: clamp(14px, 2.5vw, 16px);
  margin: 0;
}

.error-icon {
  margin-bottom: clamp(16px, 3vw, 20px);
  color: #e74c3c;
}

.error-container h3 {
  color: #495057;
  font-size: clamp(16px, 3vw, 20px);
  font-weight: 600;
  margin: 0 0 clamp(8px, 1.5vw, 12px) 0;
}

.retry-btn {
  display: flex;
  align-items: center;
  gap: clamp(6px, 1.2vw, 8px);
  padding: clamp(8px, 1.5vw, 10px) clamp(16px, 3vw, 20px);
  background: #2ecc71;
  border: none;
  border-radius: clamp(6px, 1.2vw, 8px);
  color: white;
  font-size: clamp(14px, 2.5vw, 16px);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: clamp(16px, 3vw, 20px);
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
  padding: clamp(40px, 8vw, 60px);
  text-align: center;
  flex: 1;
}

.empty-icon {
  margin-bottom: clamp(16px, 3vw, 20px);
  opacity: 0.6;
}

.empty-state h3 {
  color: #495057;
  font-size: clamp(16px, 3vw, 20px);
  font-weight: 600;
  margin: 0 0 clamp(8px, 1.5vw, 12px) 0;
}

.empty-state p {
  color: #6c757d;
  font-size: clamp(14px, 2.5vw, 16px);
  margin: 0;
  line-height: 1.5;
}

/* Tabla de historial */
.historial-table-container {
  flex: 1;
  overflow: auto;
}

.table-wrapper {
  min-width: 100%;
  overflow-x: auto;
}

.historial-table {
  width: 100%;
  border-collapse: collapse;
  font-size: clamp(12px, 2.2vw, 14px);
}

.historial-table th {
  background: #f8f9fa;
  padding: clamp(12px, 2.5vw, 16px);
  text-align: left;
  font-weight: 600;
  color: #495057;
  border-bottom: 2px solid #e9ecef;
  white-space: nowrap;
}

.historial-table td {
  padding: clamp(12px, 2.5vw, 16px);
  border-bottom: 1px solid #e9ecef;
  vertical-align: middle;
}

.registro-row:hover {
  background: #f8f9fa;
}

.tipo-badge {
  display: inline-flex;
  align-items: center;
  padding: clamp(4px, 0.8vw, 6px) clamp(8px, 1.5vw, 10px);
  border-radius: clamp(12px, 2.5vw, 16px);
  font-size: clamp(11px, 2vw, 12px);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.tipo-badge.entrada {
  background: rgba(39, 174, 96, 0.1);
  color: #27ae60;
  border: 1px solid rgba(39, 174, 96, 0.2);
}

.tipo-badge.salida {
  background: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
  border: 1px solid rgba(231, 76, 60, 0.2);
}

.tipo-badge.actividad {
  background: rgba(52, 152, 219, 0.1);
  color: #3498db;
  border: 1px solid rgba(52, 152, 219, 0.2);
}

.origen-badge {
  display: inline-flex;
  align-items: center;
  padding: clamp(3px, 0.6vw, 5px) clamp(6px, 1.2vw, 8px);
  border-radius: clamp(10px, 2vw, 12px);
  font-size: clamp(10px, 1.8vw, 11px);
  font-weight: 500;
  text-transform: capitalize;
  letter-spacing: 0.3px;
  white-space: nowrap;
}

.origen-badge.historial {
  background: rgba(156, 39, 176, 0.1);
  color: #9c27b0;
  border: 1px solid rgba(156, 39, 176, 0.2);
}

.origen-badge.registros {
  background: rgba(255, 193, 7, 0.1);
  color: #ff9800;
  border: 1px solid rgba(255, 193, 7, 0.2);
}

.origen-badge.asistencias {
  background: rgba(103, 58, 183, 0.1);
  color: #673ab7;
  border: 1px solid rgba(103, 58, 183, 0.2);
}

.descripcion-cell {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.fecha-cell, .hora-cell {
  white-space: nowrap;
  color: #6c757d;
}

.details-btn {
  padding: clamp(4px, 0.8vw, 6px) clamp(8px, 1.5vw, 10px);
  background: #3498db;
  border: none;
  border-radius: clamp(4px, 0.8vw, 6px);
  color: white;
  font-size: clamp(11px, 2vw, 12px);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.details-btn:hover {
  background: #2980b9;
}

.no-details {
  color: #adb5bd;
  font-style: italic;
  font-size: clamp(11px, 2vw, 12px);
}

/* Welcome section */
.welcome-section {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: clamp(40px, 8vw, 60px);
  min-height: 400px;
}

.welcome-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(46, 204, 113, 0.2);
  border-radius: clamp(16px, 3vw, 24px);
  padding: clamp(24px, 5vw, 40px);
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
  width: clamp(48px, 10vw, 64px);
  height: clamp(48px, 10vw, 64px);
  background: linear-gradient(135deg, #2ecc71, #27ae60);
  border-radius: clamp(10px, 2vw, 14px);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto clamp(16px, 3vw, 20px) auto;
  box-shadow: 0 10px 25px rgba(46, 204, 113, 0.3);
  transition: transform 0.3s ease;
}

.welcome-card:hover .welcome-icon {
  transform: scale(1.05) rotate(5deg);
}

.welcome-icon svg {
  width: clamp(24px, 5vw, 32px);
  height: clamp(24px, 5vw, 32px);
  color: white;
}

.welcome-card h2 {
  color: #2c5530;
  font-size: clamp(18px, 4vw, 24px);
  font-weight: 800;
  margin: 0 0 clamp(12px, 2.5vw, 16px) 0;
  text-shadow: 0 2px 10px rgba(46, 204, 113, 0.2);
  letter-spacing: -0.5px;
}

.welcome-card p {
  color: #27ae60;
  font-size: clamp(14px, 2.8vw, 16px);
  line-height: 1.6;
  margin: 0;
  font-weight: 500;
}

/* Modal de detalles */
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
  padding: clamp(16px, 3vw, 20px);
}

.modal-content {
  background: white;
  border-radius: clamp(12px, 2.5vw, 16px);
  max-width: 600px;
  width: 100%;
  max-height: 80vh;
  overflow: auto;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: clamp(16px, 3vw, 20px);
  border-bottom: 1px solid #e9ecef;
}

.modal-header h3 {
  margin: 0;
  font-size: clamp(16px, 3vw, 18px);
  font-weight: 600;
  color: #2c5530;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: clamp(4px, 0.8vw, 6px);
  border-radius: clamp(4px, 0.8vw, 6px);
  color: #6c757d;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: #f8f9fa;
  color: #495057;
}

.modal-body {
  padding: clamp(16px, 3vw, 20px);
}

.detail-grid {
  display: grid;
  gap: clamp(12px, 2.5vw, 16px);
}

.detail-item {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: clamp(8px, 1.5vw, 12px);
  align-items: start;
}

.detail-item.full-width {
  grid-column: 1 / -1;
  grid-template-columns: 1fr;
}

.detail-item strong {
  color: #495057;
  font-weight: 600;
  font-size: clamp(13px, 2.3vw, 14px);
}

.json-display {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: clamp(6px, 1.2vw, 8px);
  padding: clamp(12px, 2.5vw, 16px);
  font-family: 'Courier New', monospace;
  font-size: clamp(11px, 2vw, 12px);
  color: #495057;
  overflow-x: auto;
  white-space: pre-wrap;
  margin-top: clamp(8px, 1.5vw, 10px);
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
    gap: clamp(12px, 2.5vw, 16px);
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .filters-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .historial-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .historial-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .detail-item {
    grid-template-columns: 1fr;
    gap: clamp(4px, 0.8vw, 6px);
  }
}

@media (max-width: 480px) {
  .page-content {
    padding: clamp(8px, 1.5vw, 12px);
    gap: clamp(8px, 1.5vw, 12px);
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .period-buttons {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .historial-table {
    font-size: clamp(10px, 2vw, 12px);
  }
  
  .historial-table th,
  .historial-table td {
    padding: clamp(8px, 1.5vw, 10px);
  }
  
  .modal-content {
    margin: clamp(8px, 1.5vw, 12px);
    max-height: 90vh;
  }
}

@media (max-width: 360px) {
  .header-main {
    flex-direction: column;
    align-items: flex-start;
    gap: clamp(8px, 1.5vw, 10px);
  }
  
  .header-actions {
    flex-direction: column;
    width: 100%;
    gap: clamp(8px, 1.5vw, 10px);
  }
  
  .connection-status {
    width: 100%;
    justify-content: center;
  }
  
  .refresh-btn {
    width: 100%;
    justify-content: center;
  }
  
  .period-buttons {
    flex-direction: column;
  }
  
  .period-btn {
    text-align: center;
  }
}
</style>
