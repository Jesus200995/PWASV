<template>
  <div class="reportes-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="20" x2="18" y2="10"/>
                <line x1="12" y1="20" x2="12" y2="4"/>
                <line x1="6" y1="20" x2="6" y2="14"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Gestión de Reportes</h1>
              <p class="header-subtitle">Consulta los reportes firmados por los usuarios</p>
            </div>
          </div>
          <div class="header-actions">
            <button @click="cargarReportes" class="refresh-btn" :disabled="loading">
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
        <!-- Estadísticas Rápidas -->
        <div class="stats-section">
          <div class="stats-grid">
            <div class="stat-card total">
              <div class="stat-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                </svg>
              </div>
              <div class="stat-info">
                <span class="stat-value">{{ estadisticas.totalReportes }}</span>
                <span class="stat-label">Total Reportes</span>
              </div>
            </div>
            
            <div class="stat-card mes">
              <div class="stat-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
              </div>
              <div class="stat-info">
                <span class="stat-value">{{ estadisticas.reportesMes }}</span>
                <span class="stat-label">Este Mes</span>
              </div>
            </div>
            
            <div class="stat-card pdf">
              <div class="stat-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                </svg>
              </div>
              <div class="stat-info">
                <span class="stat-value">{{ estadisticas.porTipo?.PDF || 0 }}</span>
                <span class="stat-label">Reportes PDF</span>
              </div>
            </div>
            
            <div class="stat-card usuarios">
              <div class="stat-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                </svg>
              </div>
              <div class="stat-info">
                <span class="stat-value">{{ estadisticas.usuariosConReportes }}</span>
                <span class="stat-label">Usuarios Activos</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Filtros -->
        <div class="filters-section">
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
              <div class="filter-group search-group">
                <label>Buscar:</label>
                <div class="search-input-wrapper">
                  <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="m21 21-4.35-4.35"></path>
                  </svg>
                  <input 
                    v-model="filtros.busqueda" 
                    type="text" 
                    placeholder="Buscar por nombre, correo, territorio..." 
                    class="search-input"
                    @input="filtrarReportes"
                  >
                </div>
              </div>

              <div class="filter-group">
                <label>Mes:</label>
                <select v-model="filtros.mes" @change="cargarReportes" class="filter-select">
                  <option value="">Todos los meses</option>
                  <option v-for="mes in meses" :key="mes.value" :value="mes.value">{{ mes.label }}</option>
                </select>
              </div>

              <div class="filter-group">
                <label>Año:</label>
                <select v-model="filtros.anio" @change="cargarReportes" class="filter-select">
                  <option value="">Todos los años</option>
                  <option v-for="anio in anios" :key="anio" :value="anio">{{ anio }}</option>
                </select>
              </div>

              <div class="filter-group">
                <label>Territorio:</label>
                <select v-model="filtros.territorio" @change="cargarReportes" class="filter-select">
                  <option value="">Todos los territorios</option>
                  <option v-for="territorio in territorios" :key="territorio" :value="territorio">{{ territorio }}</option>
                </select>
              </div>

              <div class="filter-group">
                <label>Tipo:</label>
                <select v-model="filtros.tipo" @change="filtrarReportes" class="filter-select">
                  <option value="">Todos</option>
                  <option value="PDF">PDF</option>
                  <option value="CSV">CSV</option>
                </select>
              </div>

              <div class="filter-group filter-actions">
                <button @click="limpiarFiltros" class="clear-filters-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
                  </svg>
                  Limpiar
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Lista de Reportes -->
        <div class="reportes-section">
          <div class="reportes-card">
            <div class="reportes-header">
              <h3>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>
                </svg>
                Reportes Generados
              </h3>
              <div class="reportes-count">
                <span class="count-badge">{{ reportesFiltrados.length }}</span>
                <span class="count-text">de {{ totalReportes }}</span>
              </div>
            </div>

            <div v-if="loading" class="loading-state">
              <div class="spinner"></div>
              <p>Cargando reportes...</p>
            </div>

            <div v-else-if="reportesFiltrados.length === 0" class="empty-state">
              <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
              </svg>
              <h4 class="empty-title">No hay reportes</h4>
              <p class="empty-subtitle">{{ filtrosActivos ? 'No se encontraron reportes con los filtros aplicados' : 'Aún no se han generado reportes' }}</p>
            </div>

            <div v-else class="reportes-table-container">
              <table class="reportes-table">
                <thead>
                  <tr>
                    <th class="th-usuario">Usuario</th>
                    <th class="th-territorio">Territorio</th>
                    <th class="th-reporte">Reporte</th>
                    <th class="th-periodo">Período</th>
                    <th class="th-tipo">Tipo</th>
                    <th class="th-fecha">Fecha</th>
                    <th class="th-acciones">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="reporte in reportesPaginados" :key="reporte.id">
                    <td class="td-usuario">
                      <div class="usuario-cell">
                        <div class="usuario-avatar">{{ obtenerIniciales(reporte.usuario?.nombre_completo) }}</div>
                        <div class="usuario-info">
                          <span class="usuario-nombre">{{ reporte.usuario?.nombre_completo || 'Usuario desconocido' }}</span>
                          <span class="usuario-correo">{{ reporte.usuario?.correo || '-' }}</span>
                        </div>
                      </div>
                    </td>
                    <td class="td-territorio">
                      <span class="territorio-badge">{{ reporte.usuario?.territorio || 'Sin territorio' }}</span>
                    </td>
                    <td class="td-reporte">
                      <span class="reporte-nombre">{{ reporte.nombre_reporte }}</span>
                    </td>
                    <td class="td-periodo">
                      <span class="periodo-badge">{{ reporte.mes }} {{ reporte.anio }}</span>
                    </td>
                    <td class="td-tipo">
                      <span :class="['tipo-badge', reporte.tipo?.toLowerCase()]">
                        <svg v-if="reporte.tipo === 'PDF'" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>
                        </svg>
                        <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>
                        </svg>
                        {{ reporte.tipo }}
                      </span>
                    </td>
                    <td class="td-fecha">
                      <span class="fecha-text">{{ formatearFecha(reporte.fecha_generacion) }}</span>
                    </td>
                    <td class="td-acciones">
                      <div class="acciones-buttons">
                        <button v-if="reporte.tiene_pdf" @click="verReporte(reporte)" :disabled="viendoReporte === reporte.id" class="btn-action btn-view" title="Ver reporte">
                          <svg v-if="viendoReporte !== reporte.id" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
                          </svg>
                          <div v-else class="spinner-mini"></div>
                        </button>
                        <button v-if="reporte.tiene_pdf" @click="descargarReporte(reporte)" :disabled="descargandoReporte === reporte.id" class="btn-action btn-download" title="Descargar">
                          <svg v-if="descargandoReporte !== reporte.id" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>
                          </svg>
                          <div v-else class="spinner-mini"></div>
                        </button>
                        <span v-if="!reporte.tiene_pdf && reporte.tipo === 'PDF'" class="no-pdf-badge" title="PDF no disponible">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
                          </svg>
                        </span>
                        <button @click="confirmarEliminacion(reporte)" :disabled="eliminandoReporte === reporte.id" class="btn-action btn-delete" title="Eliminar">
                          <svg v-if="eliminandoReporte !== reporte.id" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                          </svg>
                          <div v-else class="spinner-mini"></div>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-if="reportesFiltrados.length > 0" class="pagination-container">
              <div class="pagination-info">
                Mostrando {{ (paginaActual - 1) * porPagina + 1 }} - {{ Math.min(paginaActual * porPagina, reportesFiltrados.length) }} de {{ reportesFiltrados.length }}
              </div>
              <div class="pagination-controls">
                <button @click="paginaActual = 1" :disabled="paginaActual === 1" class="pagination-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="11 17 6 12 11 7"/><polyline points="18 17 13 12 18 7"/></svg>
                </button>
                <button @click="paginaActual--" :disabled="paginaActual === 1" class="pagination-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
                </button>
                <span class="pagination-pages">Página {{ paginaActual }} de {{ totalPaginas }}</span>
                <button @click="paginaActual++" :disabled="paginaActual === totalPaginas" class="pagination-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
                </button>
                <button @click="paginaActual = totalPaginas" :disabled="paginaActual === totalPaginas" class="pagination-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="13 17 18 12 13 7"/><polyline points="6 17 11 12 6 7"/></svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal de Confirmación de Eliminación -->
      <Teleport to="body">
        <Transition name="modal-fade">
          <div v-if="mostrarModalEliminar" class="modal-overlay" @click.self="cancelarEliminacion">
            <div class="modal-container modal-delete">
              <div class="modal-header delete-header">
                <div class="modal-icon delete-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                    <line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/>
                  </svg>
                </div>
                <div class="modal-title-container">
                  <h3>Eliminar Reporte</h3>
                  <p>Esta acción no se puede deshacer</p>
                </div>
              </div>
              <div class="modal-body">
                <p>¿Estás seguro de que deseas eliminar el reporte:</p>
                <div class="reporte-eliminar-info">
                  <strong>{{ reporteAEliminar?.nombre_reporte }}</strong>
                  <span>de {{ reporteAEliminar?.usuario?.nombre_completo }}</span>
                </div>
              </div>
              <div class="modal-footer">
                <button @click="cancelarEliminacion" class="btn-cancel">Cancelar</button>
                <button @click="ejecutarEliminacion" class="btn-delete-confirm" :disabled="eliminandoReporte">
                  <svg v-if="!eliminandoReporte" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                  </svg>
                  <div v-else class="spinner-mini white"></div>
                  {{ eliminandoReporte ? 'Eliminando...' : 'Eliminar' }}
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </Teleport>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import reportesService from '../services/reportesService'

const router = useRouter()

const loading = ref(false)
const reportes = ref([])
const totalReportes = ref(0)
const territorios = ref([])

const viendoReporte = ref(null)
const descargandoReporte = ref(null)
const eliminandoReporte = ref(null)

const mostrarModalEliminar = ref(false)
const reporteAEliminar = ref(null)

const estadisticas = ref({
  totalReportes: 0,
  reportesMes: 0,
  porTipo: {},
  usuariosConReportes: 0,
  porTerritorio: {}
})

const filtros = ref({
  busqueda: '',
  mes: '',
  anio: '',
  territorio: '',
  tipo: ''
})

const paginaActual = ref(1)
const porPagina = ref(15)

const meses = [
  { value: 'Enero', label: 'Enero' },
  { value: 'Febrero', label: 'Febrero' },
  { value: 'Marzo', label: 'Marzo' },
  { value: 'Abril', label: 'Abril' },
  { value: 'Mayo', label: 'Mayo' },
  { value: 'Junio', label: 'Junio' },
  { value: 'Julio', label: 'Julio' },
  { value: 'Agosto', label: 'Agosto' },
  { value: 'Septiembre', label: 'Septiembre' },
  { value: 'Octubre', label: 'Octubre' },
  { value: 'Noviembre', label: 'Noviembre' },
  { value: 'Diciembre', label: 'Diciembre' }
]

const anioActual = new Date().getFullYear()
const anios = computed(() => {
  const lista = []
  for (let i = anioActual; i >= anioActual - 5; i--) lista.push(i)
  return lista
})

const reportesFiltrados = computed(() => {
  let resultado = [...reportes.value]
  if (filtros.value.busqueda) {
    const busqueda = filtros.value.busqueda.toLowerCase()
    resultado = resultado.filter(r => 
      r.nombre_reporte?.toLowerCase().includes(busqueda) ||
      r.usuario?.nombre_completo?.toLowerCase().includes(busqueda) ||
      r.usuario?.correo?.toLowerCase().includes(busqueda) ||
      r.usuario?.territorio?.toLowerCase().includes(busqueda)
    )
  }
  if (filtros.value.tipo) {
    resultado = resultado.filter(r => r.tipo === filtros.value.tipo)
  }
  return resultado
})

const reportesPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * porPagina.value
  return reportesFiltrados.value.slice(inicio, inicio + porPagina.value)
})

const totalPaginas = computed(() => Math.ceil(reportesFiltrados.value.length / porPagina.value) || 1)

const filtrosActivos = computed(() => 
  filtros.value.busqueda || filtros.value.mes || filtros.value.anio || filtros.value.territorio || filtros.value.tipo
)

async function cargarReportes() {
  loading.value = true
  try {
    const params = { limite: 500 }
    if (filtros.value.mes) params.mes = filtros.value.mes
    if (filtros.value.anio) params.anio = filtros.value.anio
    if (filtros.value.territorio) params.territorio = filtros.value.territorio
    
    const response = await reportesService.obtenerTodosReportes(params)
    if (response.success) {
      reportes.value = response.reportes || []
      totalReportes.value = response.total || 0
      const territoriosUnicos = new Set()
      reportes.value.forEach(r => { if (r.usuario?.territorio) territoriosUnicos.add(r.usuario.territorio) })
      territorios.value = Array.from(territoriosUnicos).sort()
    }
    paginaActual.value = 1
  } catch (error) {
    console.error('Error cargando reportes:', error)
  } finally {
    loading.value = false
  }
}

async function cargarEstadisticas() {
  try {
    const response = await reportesService.obtenerEstadisticas()
    if (response.success) {
      estadisticas.value = {
        totalReportes: response.estadisticas.total_reportes || 0,
        reportesMes: response.estadisticas.reportes_mes_actual || 0,
        porTipo: response.estadisticas.por_tipo || {},
        usuariosConReportes: response.estadisticas.usuarios_con_reportes || 0,
        porTerritorio: response.estadisticas.por_territorio || {}
      }
    }
  } catch (error) {
    console.error('Error cargando estadísticas:', error)
  }
}

async function verReporte(reporte) {
  viendoReporte.value = reporte.id
  try {
    await reportesService.verReporte(reporte.id)
  } catch (error) {
    console.error('Error al ver reporte:', error)
    alert('No se pudo abrir el reporte: ' + error.message)
  } finally {
    viendoReporte.value = null
  }
}

async function descargarReporte(reporte) {
  descargandoReporte.value = reporte.id
  try {
    await reportesService.descargarReporte(reporte.id)
  } catch (error) {
    console.error('Error al descargar reporte:', error)
    alert('No se pudo descargar el reporte: ' + error.message)
  } finally {
    descargandoReporte.value = null
  }
}

function confirmarEliminacion(reporte) {
  reporteAEliminar.value = reporte
  mostrarModalEliminar.value = true
}

function cancelarEliminacion() {
  mostrarModalEliminar.value = false
  reporteAEliminar.value = null
}

async function ejecutarEliminacion() {
  if (!reporteAEliminar.value) return
  eliminandoReporte.value = reporteAEliminar.value.id
  try {
    await reportesService.eliminarReporte(reporteAEliminar.value.id)
    reportes.value = reportes.value.filter(r => r.id !== reporteAEliminar.value.id)
    totalReportes.value--
    cancelarEliminacion()
    await cargarEstadisticas()
  } catch (error) {
    console.error('Error al eliminar reporte:', error)
    alert('No se pudo eliminar el reporte: ' + error.message)
  } finally {
    eliminandoReporte.value = null
  }
}

function filtrarReportes() { paginaActual.value = 1 }

function limpiarFiltros() {
  filtros.value = { busqueda: '', mes: '', anio: '', territorio: '', tipo: '' }
  cargarReportes()
}

function formatearFecha(fechaISO) {
  if (!fechaISO) return '-'
  return new Date(fechaISO).toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

function obtenerIniciales(nombre) {
  if (!nombre) return '??'
  const partes = nombre.split(' ')
  return partes.length >= 2 ? (partes[0][0] + partes[1][0]).toUpperCase() : nombre.substring(0, 2).toUpperCase()
}

function logout() {
  localStorage.removeItem('adminToken')
  router.push('/login')
}

onMounted(() => {
  cargarReportes()
  cargarEstadisticas()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

.reportes-container { display: flex; min-height: 100vh; background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%); }

.main-content { flex: 1; margin-left: min(220px, 18vw); width: calc(100vw - min(220px, 18vw)); background: linear-gradient(135deg, #f8f9fa 0%, #f0fff0 100%); min-height: 100vh; position: relative; box-sizing: border-box; overflow-x: hidden; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }

.page-header { background: linear-gradient(135deg, #4CAF50 0%, #45a049 50%, #2E7D32 100%); color: white; padding: clamp(0.5rem, 1.2vw, 0.8rem) clamp(1rem, 2vw, 1.5rem); box-shadow: 0 4px 16px rgba(76, 175, 80, 0.15); position: sticky; top: 0; z-index: 100; width: 100%; box-sizing: border-box; backdrop-filter: blur(8px); border-bottom: 1px solid rgba(255, 255, 255, 0.1); overflow: hidden; }

.page-header::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat; z-index: 1; }

.header-content { display: flex; justify-content: space-between; align-items: center; max-width: 100%; gap: clamp(0.5rem, 1vw, 1rem); flex-wrap: wrap; position: relative; z-index: 2; }

.header-main { display: flex; align-items: center; gap: clamp(0.5rem, 1.5vw, 1rem); }

.header-icon { width: 38px; height: 38px; min-width: 38px; background: rgba(255, 255, 255, 0.2); border-radius: 10px; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.3); flex-shrink: 0; }

.header-icon svg { width: 18px; height: 18px; max-width: 18px; max-height: 18px; color: white; flex-shrink: 0; }

.header-text { display: flex; flex-direction: column; gap: 2px; }

.header-title { font-size: clamp(1rem, 2vw, 1.5rem); font-weight: 700; margin: 0; font-family: 'Inter', sans-serif; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }

.header-subtitle { font-size: clamp(0.65rem, 1.2vw, 0.85rem); opacity: 0.9; margin: 0; font-family: 'Inter', sans-serif; }

.header-actions { display: flex; gap: 0.5rem; }

.refresh-btn { display: flex; align-items: center; gap: 6px; padding: clamp(6px, 1vw, 10px) clamp(12px, 1.5vw, 16px); background: rgba(255, 255, 255, 0.2); color: white; border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 8px; font-size: clamp(0.7rem, 1.2vw, 0.85rem); font-weight: 600; cursor: pointer; transition: all 0.2s; font-family: 'Inter', sans-serif; backdrop-filter: blur(10px); }

.refresh-btn:hover:not(:disabled) { background: rgba(255, 255, 255, 0.3); transform: translateY(-1px); }

.refresh-btn:disabled { opacity: 0.7; cursor: not-allowed; }

.refresh-icon { width: 16px; height: 16px; }

.refresh-icon.spinning { animation: spin 1s linear infinite; }

@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

.page-content { padding: clamp(12px, 2vw, 24px); max-width: 1600px; margin: 0 auto; }

.stats-section { margin-bottom: clamp(16px, 2vw, 24px); }

.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: clamp(12px, 1.5vw, 16px); }

.stat-card { background: white; border-radius: 10px; padding: 12px 14px; display: flex; align-items: center; gap: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06); border: 1px solid rgba(0, 0, 0, 0.05); transition: all 0.2s; }

.stat-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12); }

.stat-icon { width: 40px; height: 40px; min-width: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }

.stat-icon svg { width: 20px; height: 20px; max-width: 20px; max-height: 20px; color: white; flex-shrink: 0; }

.stat-card.total .stat-icon { background: linear-gradient(135deg, #4CAF50, #2E7D32); }
.stat-card.mes .stat-icon { background: linear-gradient(135deg, #2196F3, #1565C0); }
.stat-card.pdf .stat-icon { background: linear-gradient(135deg, #F44336, #C62828); }
.stat-card.usuarios .stat-icon { background: linear-gradient(135deg, #9C27B0, #6A1B9A); }

.stat-info { display: flex; flex-direction: column; }

.stat-value { font-size: 1.25rem; font-weight: 700; color: #1a1a1a; font-family: 'Inter', sans-serif; line-height: 1; }

.stat-label { font-size: 0.7rem; color: #666; font-family: 'Inter', sans-serif; margin-top: 2px; }

.filters-section { margin-bottom: clamp(16px, 2vw, 24px); }

.filters-card { background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); border: 1px solid rgba(0, 0, 0, 0.05); overflow: hidden; }

.filters-header { background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); padding: clamp(12px, 1.5vw, 16px); border-bottom: 1px solid rgba(0, 0, 0, 0.05); }

.filters-header h3 { display: flex; align-items: center; gap: 10px; margin: 0; font-size: clamp(0.9rem, 1.3vw, 1rem); font-weight: 600; color: #15803d; font-family: 'Inter', sans-serif; }

.filters-header svg { color: #16a34a; }

.filters-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: clamp(12px, 1.5vw, 16px); padding: clamp(12px, 1.5vw, 16px); }

.filter-group { display: flex; flex-direction: column; gap: 6px; }

.filter-group label { font-size: clamp(0.7rem, 1.1vw, 0.8rem); font-weight: 600; color: #374151; font-family: 'Inter', sans-serif; }

.filter-select { padding: clamp(8px, 1vw, 10px) clamp(10px, 1.2vw, 12px); border: 1.5px solid #d1d5db; border-radius: 8px; font-size: clamp(0.75rem, 1.1vw, 0.85rem); font-family: 'Inter', sans-serif; background: white; cursor: pointer; transition: all 0.2s; }

.filter-select:focus { outline: none; border-color: #4CAF50; box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1); }

.search-group { grid-column: span 2; }

.search-input-wrapper { position: relative; }

.search-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #9ca3af; }

.search-input { width: 100%; padding: clamp(8px, 1vw, 10px) clamp(10px, 1.2vw, 12px) clamp(8px, 1vw, 10px) 40px; border: 1.5px solid #d1d5db; border-radius: 8px; font-size: clamp(0.75rem, 1.1vw, 0.85rem); font-family: 'Inter', sans-serif; transition: all 0.2s; box-sizing: border-box; }

.search-input:focus { outline: none; border-color: #4CAF50; box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1); }

.filter-actions { display: flex; align-items: flex-end; }

.clear-filters-btn { display: flex; align-items: center; gap: 6px; padding: clamp(8px, 1vw, 10px) clamp(12px, 1.5vw, 16px); background: #f3f4f6; color: #374151; border: 1.5px solid #d1d5db; border-radius: 8px; font-size: clamp(0.7rem, 1.1vw, 0.8rem); font-weight: 500; cursor: pointer; transition: all 0.2s; font-family: 'Inter', sans-serif; }

.clear-filters-btn:hover { background: #e5e7eb; border-color: #9ca3af; }

.reportes-section { margin-bottom: 24px; }

.reportes-card { background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); border: 1px solid rgba(0, 0, 0, 0.05); overflow: hidden; }

.reportes-header { display: flex; justify-content: space-between; align-items: center; background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); padding: clamp(12px, 1.5vw, 16px); border-bottom: 1px solid rgba(0, 0, 0, 0.05); }

.reportes-header h3 { display: flex; align-items: center; gap: 10px; margin: 0; font-size: clamp(0.9rem, 1.3vw, 1rem); font-weight: 600; color: #15803d; font-family: 'Inter', sans-serif; }

.reportes-header svg { color: #16a34a; }

.reportes-count { display: flex; align-items: center; gap: 6px; }

.count-badge { background: linear-gradient(135deg, #4CAF50, #2E7D32); color: white; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; font-family: 'Inter', sans-serif; }

.count-text { font-size: 0.75rem; color: #666; font-family: 'Inter', sans-serif; }

.loading-state, .empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 60px 20px; color: #666; }

.spinner { width: 40px; height: 40px; border: 3px solid rgba(76, 175, 80, 0.2); border-top-color: #4CAF50; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 16px; }

.empty-state svg { color: #d1d5db; margin-bottom: 16px; }

.empty-title { font-size: 1.1rem; font-weight: 600; color: #374151; margin: 0 0 8px; font-family: 'Inter', sans-serif; }

.empty-subtitle { font-size: 0.85rem; color: #6b7280; margin: 0; text-align: center; font-family: 'Inter', sans-serif; }

.reportes-table-container { overflow-x: auto; }

.reportes-table { width: 100%; border-collapse: collapse; font-family: 'Inter', sans-serif; }

.reportes-table thead { background: #f9fafb; position: sticky; top: 0; }

.reportes-table th { padding: clamp(10px, 1.2vw, 14px) clamp(8px, 1vw, 12px); text-align: left; font-size: clamp(0.65rem, 1vw, 0.75rem); font-weight: 600; color: #374151; border-bottom: 2px solid #e5e7eb; white-space: nowrap; text-transform: uppercase; letter-spacing: 0.5px; }

.reportes-table td { padding: clamp(10px, 1.2vw, 14px) clamp(8px, 1vw, 12px); font-size: clamp(0.7rem, 1.1vw, 0.85rem); color: #374151; border-bottom: 1px solid #f3f4f6; vertical-align: middle; }

.reportes-table tbody tr { transition: background 0.15s; }

.reportes-table tbody tr:hover { background: #f9fafb; }

.usuario-cell { display: flex; align-items: center; gap: 10px; }

.usuario-avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #4CAF50, #2E7D32); color: white; display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: 600; flex-shrink: 0; }

.usuario-info { display: flex; flex-direction: column; min-width: 0; }

.usuario-nombre { font-weight: 600; color: #1a1a1a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.usuario-correo { font-size: 0.7rem; color: #6b7280; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.territorio-badge { display: inline-block; padding: 4px 10px; background: linear-gradient(135deg, #e0f2fe, #bae6fd); color: #0369a1; border-radius: 6px; font-size: 0.7rem; font-weight: 500; white-space: nowrap; }

.reporte-nombre { font-weight: 500; color: #374151; }

.periodo-badge { display: inline-block; padding: 4px 10px; background: linear-gradient(135deg, #f3e8ff, #e9d5ff); color: #7c3aed; border-radius: 6px; font-size: 0.7rem; font-weight: 500; white-space: nowrap; }

.tipo-badge { display: inline-flex; align-items: center; gap: 4px; padding: 4px 10px; border-radius: 6px; font-size: 0.7rem; font-weight: 600; }

.tipo-badge.pdf { background: linear-gradient(135deg, #fee2e2, #fecaca); color: #dc2626; }

.tipo-badge.csv { background: linear-gradient(135deg, #dcfce7, #bbf7d0); color: #16a34a; }

.fecha-text { color: #6b7280; font-size: 0.75rem; white-space: nowrap; }

.acciones-buttons { display: flex; gap: 6px; }

.btn-action { width: 32px; height: 32px; border-radius: 8px; border: 1.5px solid; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; }

.btn-action:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-view { background: #f0fdf4; border-color: #86efac; color: #16a34a; }

.btn-view:hover:not(:disabled) { background: #dcfce7; transform: translateY(-1px); }

.btn-download { background: #eff6ff; border-color: #93c5fd; color: #2563eb; }

.btn-download:hover:not(:disabled) { background: #dbeafe; transform: translateY(-1px); }

.btn-delete { background: #fef2f2; border-color: #fca5a5; color: #dc2626; }

.btn-delete:hover:not(:disabled) { background: #fee2e2; transform: translateY(-1px); }

.no-pdf-badge { color: #9ca3af; }

.spinner-mini { width: 14px; height: 14px; border: 2px solid rgba(0, 0, 0, 0.1); border-top-color: currentColor; border-radius: 50%; animation: spin 0.8s linear infinite; }

.spinner-mini.white { border-color: rgba(255, 255, 255, 0.3); border-top-color: white; }

.pagination-container { display: flex; justify-content: space-between; align-items: center; padding: clamp(12px, 1.5vw, 16px); border-top: 1px solid #f3f4f6; flex-wrap: wrap; gap: 12px; }

.pagination-info { font-size: clamp(0.7rem, 1.1vw, 0.8rem); color: #6b7280; font-family: 'Inter', sans-serif; }

.pagination-controls { display: flex; align-items: center; gap: 8px; }

.pagination-btn { width: 32px; height: 32px; border-radius: 8px; border: 1.5px solid #d1d5db; background: white; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; color: #374151; }

.pagination-btn:hover:not(:disabled) { background: #f3f4f6; border-color: #4CAF50; color: #4CAF50; }

.pagination-btn:disabled { opacity: 0.4; cursor: not-allowed; }

.pagination-pages { font-size: 0.8rem; color: #374151; font-weight: 500; padding: 0 12px; font-family: 'Inter', sans-serif; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; padding: 20px; z-index: 1000; }

.modal-container { background: white; border-radius: 16px; max-width: 400px; width: 100%; box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2); overflow: hidden; }

.modal-header { display: flex; align-items: center; gap: 16px; padding: 20px; }

.modal-header.delete-header { background: linear-gradient(135deg, #fef2f2, #fee2e2); border-bottom: 1px solid #fecaca; }

.modal-icon { width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; }

.modal-icon.delete-icon { background: #fee2e2; color: #dc2626; }

.modal-title-container h3 { font-size: 1.1rem; font-weight: 600; color: #1a1a1a; margin: 0; font-family: 'Inter', sans-serif; }

.modal-title-container p { font-size: 0.8rem; color: #6b7280; margin: 4px 0 0; font-family: 'Inter', sans-serif; }

.modal-body { padding: 20px; font-family: 'Inter', sans-serif; }

.modal-body p { margin: 0 0 12px; color: #374151; font-size: 0.9rem; }

.reporte-eliminar-info { background: #f9fafb; padding: 12px; border-radius: 8px; border: 1px solid #e5e7eb; }

.reporte-eliminar-info strong { display: block; color: #1a1a1a; font-size: 0.9rem; }

.reporte-eliminar-info span { font-size: 0.8rem; color: #6b7280; }

.modal-footer { display: flex; gap: 12px; padding: 16px 20px; background: #f9fafb; border-top: 1px solid #e5e7eb; }

.btn-cancel { flex: 1; padding: 10px 16px; background: white; border: 1.5px solid #d1d5db; border-radius: 8px; font-size: 0.9rem; font-weight: 500; color: #374151; cursor: pointer; transition: all 0.2s; font-family: 'Inter', sans-serif; }

.btn-cancel:hover { background: #f3f4f6; }

.btn-delete-confirm { flex: 1; display: flex; align-items: center; justify-content: center; gap: 8px; padding: 10px 16px; background: linear-gradient(135deg, #dc2626, #b91c1c); border: none; border-radius: 8px; font-size: 0.9rem; font-weight: 600; color: white; cursor: pointer; transition: all 0.2s; font-family: 'Inter', sans-serif; }

.btn-delete-confirm:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3); }

.btn-delete-confirm:disabled { opacity: 0.7; cursor: not-allowed; }

.modal-fade-enter-active, .modal-fade-leave-active { transition: all 0.3s ease; }

.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

.modal-fade-enter-from .modal-container, .modal-fade-leave-to .modal-container { transform: scale(0.95) translateY(10px); }

@media (max-width: 1200px) { .main-content { margin-left: min(200px, 16vw); width: calc(100vw - min(200px, 16vw)); } }

@media (max-width: 1024px) { .main-content { margin-left: 200px; width: calc(100vw - 200px); } .stats-grid { grid-template-columns: repeat(2, 1fr); } .filters-grid { grid-template-columns: repeat(2, 1fr); } .search-group { grid-column: span 2; } }

@media (max-width: 768px) and (orientation: landscape) { .main-content { margin-left: 160px; width: calc(100vw - 160px); } }

@media (max-width: 992px) { .main-content { margin-left: 200px; width: calc(100vw - 200px); } }

@media (min-width: 481px) and (max-width: 768px) { .main-content { margin-left: 250px; width: calc(100vw - 250px); } }

@media (max-width: 768px) { .main-content { margin-left: 240px; width: calc(100vw - 240px); } .header-content { flex-direction: column; align-items: flex-start; gap: 12px; } .header-main { width: 100%; } .header-actions { width: 100%; justify-content: flex-end; } .stats-grid { grid-template-columns: repeat(2, 1fr); } .filters-grid { grid-template-columns: 1fr; } .search-group { grid-column: span 1; } .reportes-table th, .reportes-table td { padding: 8px 6px; font-size: 0.7rem; } .usuario-avatar { width: 28px; height: 28px; font-size: 0.6rem; } }

@media (max-width: 480px) { .main-content { margin-left: 60px; width: calc(100vw - 60px); } .page-content { padding: 8px; } .stats-grid { grid-template-columns: 1fr 1fr; gap: 8px; } .stat-card { padding: 8px 10px; } .stat-icon { width: 32px; height: 32px; min-width: 32px; } .stat-icon svg { width: 16px; height: 16px; max-width: 16px; max-height: 16px; } .stat-value { font-size: 1rem; } .stat-label { font-size: 0.65rem; } .pagination-container { flex-direction: column; text-align: center; } .th-territorio, .td-territorio { display: none; } .btn-action { width: 28px; height: 28px; } }

@media (max-width: 360px) { .main-content { margin-left: 60px; width: calc(100vw - 60px); } .header-title { font-size: 1rem !important; } .stats-grid { grid-template-columns: 1fr; } }
</style>
