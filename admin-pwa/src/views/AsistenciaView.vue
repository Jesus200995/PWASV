<template>
  <div class="apple-asistencia-container">
    <Sidebar @logout="logout" />
    
    <main class="apple-main-content">
      <!-- ================== STICKY WRAPPER FOR HEADER + STATS ================== -->
      <div class="apple-sticky-wrapper">
        <!-- ================== HEADER APPLE STYLE ================== -->
        <header class="apple-page-header">
          <div class="apple-header-wrapper">
            <div class="apple-header-left">
              <div class="apple-icon-circle">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="12" cy="12" r="10" stroke-width="2"/>
                  <path d="M9 12l2 2 4-4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div>
                <h1 class="apple-page-title">Asistencias</h1>
                <p class="apple-page-subtitle">{{ totalAsistencias.toLocaleString() }} registros</p>
              </div>
            </div>
            
            <button @click="cargarAsistencias" class="apple-refresh-button" :disabled="loading">
              <svg :class="{ 'apple-spin': loading }" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </header>

        <!-- ================== STATS CARDS APPLE STYLE ================== -->
        <div class="apple-stats-section">
          <div class="apple-stats-grid">
            <div class="apple-stat-card">
              <div class="apple-stat-icon blue">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
              </div>
              <div class="apple-stat-content">
                <div class="apple-stat-value">{{ formatNumber(totalAsistenciasHoy) }}</div>
                <div class="apple-stat-label">Hoy</div>
              </div>
            </div>

            <div class="apple-stat-card">
              <div class="apple-stat-icon green">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                </svg>
              </div>
              <div class="apple-stat-content">
                <div class="apple-stat-value">{{ formatNumber(usuariosPresentes) }}</div>
                <div class="apple-stat-label">Presentes</div>
              </div>
            </div>

            <div class="apple-stat-card">
              <div class="apple-stat-icon purple">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
              </div>
              <div class="apple-stat-content">
                <div class="apple-stat-value">{{ formatNumber(totalAsistencias) }}</div>
                <div class="apple-stat-label">Total</div>
              </div>
            </div>
          </div>

          <!-- ================== SEARCH & FILTERS INSIDE STATS ================== -->
          <div class="apple-search-section">
          <div class="apple-search-row">
            <div class="apple-search-container">
              <svg class="apple-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="11" cy="11" r="8" stroke-width="2.5"/>
                <path d="m21 21-4.35-4.35" stroke-width="2.5" stroke-linecap="round"/>
              </svg>
              <input 
                v-model="searchTerm" 
                @input="filtrarAsistencias"
                type="text" 
                placeholder="Buscar por nombre, correo, cargo..." 
                class="apple-search-input"
              >
              <button v-if="searchTerm" @click="limpiarBusqueda" class="apple-clear-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="12" cy="12" r="10" stroke-width="2"/>
                  <line x1="15" y1="9" x2="9" y2="15" stroke-width="2" stroke-linecap="round"/>
                  <line x1="9" y1="9" x2="15" y2="15" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </button>
            </div>

            <div class="apple-filter-controls">
              <button 
                @click="limpiarFiltros" 
                class="apple-filter-btn reset"
                title="Limpiar filtros"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M3 6h18M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Limpiar</span>
              </button>
              <button 
                @click="exportarCSV" 
                class="apple-filter-btn export"
                title="Exportar a CSV"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Exportar</span>
              </button>
            </div>
          </div>

          <div class="apple-quick-filters">
            <button 
              v-for="filter in quickFilters" 
              :key="filter.value"
              @click="seleccionarFechaRapida(filter.value)" 
              :class="['apple-filter-chip', { 'active': filtroRapido === filter.value }]"
            >
              <svg v-if="filter.value === 'hoy'" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="10" stroke-width="2"/>
                <path d="M12 6v6l4 2" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <svg v-else-if="filter.value === 'ayer'" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M3 3v5h5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <svg v-else-if="filter.value === 'semana'" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke-width="2"/>
                <line x1="16" y1="2" x2="16" y2="6" stroke-width="2" stroke-linecap="round"/>
                <line x1="8" y1="2" x2="8" y2="6" stroke-width="2" stroke-linecap="round"/>
                <line x1="3" y1="10" x2="21" y2="10" stroke-width="2"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke-width="2"/>
                <line x1="3" y1="10" x2="21" y2="10" stroke-width="2"/>
              </svg>
              <span>{{ filter.label }}</span>
            </button>
          </div>
        </div>
        </div>
      </div>  <!-- Close apple-sticky-wrapper -->

      <div class="apple-content-wrapper">
        <!-- ================== TABLE APPLE STYLE ================== -->
        <div class="apple-table-container">
          <div v-if="loading && asistencias.length === 0" class="apple-loading">
            <div class="apple-spinner"></div>
            <p>Cargando asistencias...</p>
          </div>

          <div v-else-if="error" class="apple-error">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="10" stroke-width="2"/>
              <line x1="12" y1="8" x2="12" y2="12" stroke-width="2" stroke-linecap="round"/>
              <line x1="12" y1="16" x2="12.01" y2="16" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <p>{{ error }}</p>
            <button @click="cargarAsistencias" class="apple-retry-btn">Reintentar</button>
          </div>

          <div v-else-if="asistenciasFiltradas.length === 0" class="apple-empty">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="10" stroke-width="2"/>
              <path d="M8 14s1.5 2 4 2 4-2 4-2" stroke-width="2" stroke-linecap="round"/>
              <line x1="9" y1="9" x2="9.01" y2="9" stroke-width="2" stroke-linecap="round"/>
              <line x1="15" y1="9" x2="15.01" y2="9" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <h3>No hay asistencias</h3>
            <p>No se encontraron registros con los filtros aplicados</p>
          </div>

          <div v-else class="apple-table-wrapper">
            <table class="apple-table">
              <thead>
                <tr>
                  <th>Usuario</th>
                  <th>Correo</th>
                  <th>Fecha</th>
                  <th>Entrada</th>
                  <th>Salida</th>
                  <th>Ubicación</th>
                  <th>Fotos</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="asistencia in asistenciasPaginadas" :key="asistencia.id" class="apple-table-row">
                  <td>
                    <div class="apple-user-cell">
                      <div class="apple-avatar">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                          <circle cx="12" cy="7" r="4" stroke-width="2.5"/>
                        </svg>
                      </div>
                      <div class="apple-user-info">
                        <div class="apple-user-name">{{ asistencia.nombre_usuario }}</div>
                        <div class="apple-user-role">{{ asistencia.cargo_usuario || 'Sin cargo' }}</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span class="apple-email">{{ asistencia.correo_usuario }}</span>
                  </td>
                  <td>
                    <span class="apple-date-badge">
                      {{ formatearFecha(asistencia.fecha) }}
                    </span>
                  </td>
                  <td>
                    <span v-if="asistencia.hora_entrada" class="apple-time-badge entrada">
                      {{ formatearHora(asistencia.hora_entrada) }}
                    </span>
                    <span v-else class="apple-no-data">—</span>
                  </td>
                  <td>
                    <span v-if="asistencia.hora_salida" class="apple-time-badge salida">
                      {{ formatearHora(asistencia.hora_salida) }}
                    </span>
                    <span v-else class="apple-no-data">—</span>
                  </td>
                  <td>
                    <button 
                      v-if="asistencia.latitud_entrada && asistencia.longitud_entrada"
                      @click="abrirMapaModal(asistencia, 'entrada')" 
                      class="apple-location-btn"
                      title="Ver mapa"
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" stroke-width="2"/>
                        <circle cx="12" cy="10" r="3" stroke-width="2"/>
                      </svg>
                    </button>
                    <span v-else class="apple-no-data">—</span>
                  </td>
                  <td>
                    <div class="apple-photos-cell">
                      <img 
                        v-if="asistencia.foto_entrada_url"
                        :src="asistencia.foto_entrada_url" 
                        @click="abrirModal(asistencia.foto_entrada_url, 'Foto de entrada')"
                        class="apple-photo-thumb"
                        alt="Entrada"
                      >
                      <img 
                        v-if="asistencia.foto_salida_url"
                        :src="asistencia.foto_salida_url" 
                        @click="abrirModal(asistencia.foto_salida_url, 'Foto de salida')"
                        class="apple-photo-thumb"
                        alt="Salida"
                      >
                    </div>
                  </td>
                  <td>
                    <span :class="['apple-status-badge', obtenerEstadoClase(asistencia)]">
                      {{ obtenerEstadoTexto(asistencia) }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- ================== PAGINATION APPLE STYLE ================== -->
          <div v-if="totalPaginas > 1" class="apple-pagination">
            <button 
              @click="irAPagina(paginaActual - 1)" 
              :disabled="paginaActual === 1"
              class="apple-pagination-btn"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <polyline points="15 18 9 12 15 6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>

            <div class="apple-pagination-numbers">
              <button 
                v-for="pagina in paginasVisibles" 
                :key="pagina"
                @click="irAPagina(pagina)"
                :class="['apple-pagination-number', { 'active': paginaActual === pagina }]"
              >
                {{ pagina }}
              </button>
            </div>

            <button 
              @click="irAPagina(paginaActual + 1)" 
              :disabled="paginaActual === totalPaginas"
              class="apple-pagination-btn"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <polyline points="9 18 15 12 9 6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- ================== MODALS ================== -->
    <transition name="apple-modal-fade">
      <div v-if="modalVisible" class="apple-modal-overlay" @click="cerrarModal">
        <div class="apple-modal-content" @click.stop>
          <button @click="cerrarModal" class="apple-modal-close">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <line x1="18" y1="6" x2="6" y2="18" stroke-width="2" stroke-linecap="round"/>
              <line x1="6" y1="6" x2="18" y2="18" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
          <img :src="modalImage" :alt="modalTitle" class="apple-modal-image">
        </div>
      </div>
    </transition>

    <MapaAsistenciaModal 
      :visible="mapaModalVisible"
      :asistencia="asistenciaSeleccionada"
      :tipo="tipoMapa"
      @cerrar="cerrarMapaModal"
    />
  </div>
</template>

<script>
import Sidebar from '../components/Sidebar.vue'
import MapaAsistenciaModal from '../components/MapaAsistenciaModal.vue'
import AsistenciasService from '../services/asistenciasServiceOptimized.js'
import authService from '../services/authService.js'
import { API_URL } from '../config/api.js'
import { useRealtimeStats } from '../composables/useRealtimeStats.js'
import { useAnimatedNumber } from '../composables/useAnimatedNumber.js'
import { computed } from 'vue'

export default {
  name: 'AsistenciaView',
  components: {
    Sidebar,
    MapaAsistenciaModal
  },
  setup() {
    // Estadísticas en tiempo real con polling inteligente (Apple-style)
    const {
      stats: realtimeStats,
      isLoading: statsLoading,
      refresh: refreshStats
    } = useRealtimeStats({
      pollingInterval: 5000, // Actualizar cada 5 segundos
      enableCache: true,
      cacheTTL: 5000,
      enablePolling: false // Deshabilitado por defecto - solo refresh manual
    })

    // Animaciones suaves para los contadores (Apple-style)
    const { displayValue: animatedHoy } = useAnimatedNumber(
      computed(() => realtimeStats.value?.asistencias_hoy || 0),
      { duration: 800 }
    )

    const { displayValue: animatedPresentes } = useAnimatedNumber(
      computed(() => realtimeStats.value?.usuarios_presentes || 0),
      { duration: 800 }
    )

    const { displayValue: animatedTotal } = useAnimatedNumber(
      computed(() => realtimeStats.value?.total_asistencias || 0),
      { duration: 800 }
    )

    return {
      realtimeStats,
      statsLoading,
      refreshStats,
      animatedHoy,
      animatedPresentes,
      animatedTotal
    }
  },
  data() {
    return {
      asistencias: [],
      asistenciasFiltradas: [],
      searchTerm: '',
      filtroRapido: '',
      paginaActual: 1,
      asistenciasPorPagina: 50,
      totalAsistenciasServidor: 0,
      loading: false,
      error: null,
      modalVisible: false,
      modalImage: '',
      modalTitle: '',
      mapaModalVisible: false,
      asistenciaSeleccionada: null,
      tipoMapa: 'entrada',
      estadisticasServidor: {
        totalAsistencias: 0,
        totalAsistenciasHoy: 0,
        usuariosPresentes: 0
      },
      quickFilters: [
        { label: 'Hoy', value: 'hoy' },
        { label: 'Ayer', value: 'ayer' },
        { label: 'Esta semana', value: 'semana' },
        { label: 'Este mes', value: 'mes' }
      ]
    }
  },
  computed: {
    totalAsistencias() {
      // Usar valor animado de tiempo real
      return this.animatedTotal || 0
    },
    totalAsistenciasHoy() {
      // Usar valor animado de tiempo real
      return this.animatedHoy || 0
    },
    usuariosPresentes() {
      // Usar valor animado de tiempo real
      return this.animatedPresentes || 0
    },
    totalPaginas() {
      return Math.ceil(this.asistenciasFiltradas.length / this.asistenciasPorPagina)
    },
    asistenciasPaginadas() {
      const inicio = (this.paginaActual - 1) * this.asistenciasPorPagina
      const fin = inicio + this.asistenciasPorPagina
      return this.asistenciasFiltradas.slice(inicio, fin)
    },
    paginasVisibles() {
      const paginas = []
      const inicio = Math.max(1, this.paginaActual - 2)
      const fin = Math.min(this.totalPaginas, this.paginaActual + 2)
      
      for (let i = inicio; i <= fin; i++) {
        paginas.push(i)
      }
      
      return paginas
    }
  },
  async mounted() {
    // Precargar datos en segundo plano para performance Apple-style
    AsistenciasService.precargarDatos()
    await this.cargarAsistencias()
  },
  methods: {
    async cargarAsistencias() {
      this.loading = true
      this.error = null
      
      try {
        console.time('⚡ Carga total de asistencias')
        
        // Refrescar estadísticas en tiempo real (Apple-style)
        await this.refreshStats()
        
        const asistencias = await AsistenciasService.obtenerAsistenciasConUsuarios(200)
        
        this.asistencias = asistencias
        this.filtrarAsistencias()
        
        console.timeEnd('⚡ Carga total de asistencias')
        console.log(`✅ ${asistencias.length} asistencias cargadas con éxito`)
      } catch (error) {
        console.error('Error al cargar asistencias:', error)
        this.error = 'Error al cargar las asistencias. Por favor, intenta de nuevo.'
      } finally {
        this.loading = false
      }
    },
    
    async cargarEstadisticas() {
      try {
        const territorioFilter = authService.getTerritorioFilter()
        let url = `${API_URL}/estadisticas`
        if (territorioFilter) {
          url += `?territorio=${encodeURIComponent(territorioFilter)}`
        }
        
        const response = await fetch(url, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
          priority: 'high'
        })
        
        if (!response.ok) throw new Error(`Error ${response.status}`)
        
        const data = await response.json()
        const stats = data.estadisticas
        
        if (stats) {
          this.estadisticasServidor = {
            totalAsistencias: stats.total_asistencias || 0,
            totalAsistenciasHoy: stats.asistencias_hoy || 0,
            usuariosPresentes: stats.usuarios_presentes || 0
          }
          
          this.totalAsistenciasServidor = stats.total_asistencias || 0
        }
      } catch (error) {
        console.warn('Error al cargar estadísticas:', error)
      }
    },
    
    filtrarAsistencias() {
      let filtradas = [...this.asistencias]

      if (this.searchTerm) {
        const termino = this.searchTerm.toLowerCase()
        filtradas = filtradas.filter(asistencia => 
          (asistencia.nombre_usuario && asistencia.nombre_usuario.toLowerCase().includes(termino)) ||
          (asistencia.correo_usuario && asistencia.correo_usuario.toLowerCase().includes(termino))
        )
      }

      if (this.filtroRapido) {
        const hoy = new Date()
        hoy.setHours(0, 0, 0, 0)
        
        switch (this.filtroRapido) {
          case 'hoy':
            const fechaHoy = hoy.toISOString().split('T')[0]
            filtradas = filtradas.filter(a => a.fecha === fechaHoy)
            break
          case 'ayer':
            const ayer = new Date(hoy)
            ayer.setDate(ayer.getDate() - 1)
            const fechaAyer = ayer.toISOString().split('T')[0]
            filtradas = filtradas.filter(a => a.fecha === fechaAyer)
            break
          case 'semana':
            const inicioSemana = new Date(hoy)
            inicioSemana.setDate(hoy.getDate() - hoy.getDay())
            filtradas = filtradas.filter(a => {
              const fecha = new Date(a.fecha)
              return fecha >= inicioSemana && fecha <= hoy
            })
            break
          case 'mes':
            const inicioMes = new Date(hoy.getFullYear(), hoy.getMonth(), 1)
            filtradas = filtradas.filter(a => {
              const fecha = new Date(a.fecha)
              return fecha >= inicioMes && fecha <= hoy
            })
            break
        }
      }

      this.asistenciasFiltradas = filtradas
      this.paginaActual = 1
    },
    
    seleccionarFechaRapida(tipo) {
      this.filtroRapido = this.filtroRapido === tipo ? '' : tipo
      this.filtrarAsistencias()
    },
    
    limpiarBusqueda() {
      this.searchTerm = ''
      this.filtrarAsistencias()
    },
    
    limpiarFiltros() {
      this.searchTerm = ''
      this.filtroRapido = ''
      this.filtrarAsistencias()
    },
    
    exportarCSV() {
      try {
        // Preparar datos para exportar (asistencias filtradas)
        const datos = this.asistenciasFiltradas.map(asistencia => ({
          'Fecha': this.formatearFecha(asistencia.fecha),
          'Usuario': asistencia.usuario?.nombre || 'N/A',
          'Email': asistencia.usuario?.email || 'N/A',
          'Cargo': asistencia.usuario?.cargo || 'N/A',
          'Presente': asistencia.presente ? 'Sí' : 'No',
          'Distancia': asistencia.distancia_metros ? `${asistencia.distancia_metros}m` : 'N/A',
          'Territorio': asistencia.usuario?.territorio || 'N/A'
        }))
        
        // Convertir a CSV
        const headers = Object.keys(datos[0]).join(',')
        const rows = datos.map(row => Object.values(row).join(','))
        const csv = [headers, ...rows].join('\\n')
        
        // Descargar archivo
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
        const link = document.createElement('a')
        const url = URL.createObjectURL(blob)
        link.setAttribute('href', url)
        link.setAttribute('download', `asistencias_${new Date().toISOString().split('T')[0]}.csv`)
        link.style.visibility = 'hidden'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      } catch (error) {
        console.error('Error al exportar CSV:', error)
        alert('Error al exportar el archivo CSV')
      }
    },
    
    irAPagina(numeroPagina) {
      if (numeroPagina >= 1 && numeroPagina <= this.totalPaginas) {
        this.paginaActual = numeroPagina
        
        // Scroll suave al inicio (Apple-style)
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        })
      }
    },
    
    formatearFecha(fecha) {
      return AsistenciasService.formatearFecha(fecha)
    },
    
    formatearHora(hora) {
      return AsistenciasService.formatearHora(hora)
    },
    
    formatNumber(num) {
      if (!num && num !== 0) return '0'
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    },
    
    obtenerIniciales(nombre) {
      if (!nombre) return '??'
      return nombre.split(' ')
        .map(n => n.charAt(0))
        .join('')
        .toUpperCase()
        .substring(0, 2)
    },
    
    obtenerEstadoClase(asistencia) {
      if (!asistencia.hora_entrada) return 'sin-entrada'
      if (!asistencia.hora_salida) return 'en-curso'
      return 'completa'
    },
    
    obtenerEstadoTexto(asistencia) {
      if (!asistencia.hora_entrada) return 'Sin entrada'
      if (!asistencia.hora_salida) return 'En curso'
      return 'Completa'
    },
    
    abrirModal(imageUrl, title) {
      this.modalImage = imageUrl
      this.modalTitle = title
      this.modalVisible = true
      document.body.style.overflow = 'hidden'
    },
    
    cerrarModal() {
      this.modalVisible = false
      this.modalImage = ''
      this.modalTitle = ''
      document.body.style.overflow = 'auto'
    },
    
    abrirMapaModal(asistencia, tipo) {
      this.asistenciaSeleccionada = asistencia
      this.tipoMapa = tipo
      this.mapaModalVisible = true
      document.body.style.overflow = 'hidden'
    },
    
    cerrarMapaModal() {
      this.mapaModalVisible = false
      this.asistenciaSeleccionada = null
      this.tipoMapa = 'entrada'
      document.body.style.overflow = 'auto'
    },
    
    logout() {
      // Limpiar caché al cerrar sesión
      AsistenciasService.limpiarCache()
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_user')
      this.$router.push('/login')
    }
  },
  beforeUnmount() {
    // Limpiar al desmontar el componente
    AsistenciasService.limpiarCache()
  }
}
</script>

<style scoped>
/* ==================== APPLE DESIGN SYSTEM ==================== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --apple-blue: #007AFF;
  --apple-green: #34C759;
  --apple-purple: #AF52DE;
  --apple-gray-1: #F5F5F7;
  --apple-gray-2: #E5E5EA;
  --apple-gray-3: #D1D1D6;
  --apple-gray-4: #8E8E93;
  --apple-gray-5: #636366;
  --apple-gray-6: #48484A;
  --apple-text: #1D1D1F;
  --apple-radius: 16px;
  --apple-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  --apple-shadow-lg: 0 12px 40px rgba(0, 0, 0, 0.12);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.apple-asistencia-container {
  display: flex;
  min-height: 100vh;
  background: var(--apple-gray-1);
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.apple-main-content {
  flex: 1;
  margin-left: 220px;
  width: calc(100vw - 220px);
  overflow-x: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  padding: 8px 16px 0 16px;
}

/* ==================== STICKY WRAPPER ==================== */
.apple-sticky-wrapper {
  position: sticky;
  top: 0;
  z-index: 100;
  margin-bottom: 20px;
}

/* ==================== HEADER ==================== */
.apple-page-header {
  background: linear-gradient(135deg, 
    #388E3C 0%, 
    #2E7D32 50%, 
    #1B5E20 100%);
  border-bottom: none;
  padding: 12px 20px;
  box-shadow: none;
  border-radius: 28px 28px 0 0;
  border: 2px solid #8BC34A;
  border-bottom: none;
}

.apple-header-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.apple-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.apple-icon-circle {
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  flex-shrink: 0;
}

.apple-icon-circle svg {
  width: 16px;
  height: 16px;
  stroke: white;
  stroke-width: 2.5;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.apple-page-title {
  font-size: 19px;
  font-weight: 700;
  color: white;
  margin: 0;
  letter-spacing: -0.3px;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
}

.apple-page-subtitle {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.85);
  margin: 2px 0 0 0;
  font-weight: 500;
}

.apple-refresh-button {
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-refresh-button:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.25);
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.apple-refresh-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.apple-refresh-button svg {
  width: 16px;
  height: 16px;
  stroke: white;
  stroke-width: 2;
  fill: none;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.apple-spin {
  animation: apple-spin 0.8s linear infinite;
}

@keyframes apple-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ==================== CONTENT ==================== */
.apple-content-wrapper {
  padding: 0;
  overflow-x: hidden;
}

/* ==================== STATS SECTION WITH SEARCH ==================== */
.apple-stats-section {
  background: white;
  border-radius: 0 0 28px 28px;
  padding: 24px 20px 20px 20px;
  margin-bottom: 0;
  box-shadow: none;
  border: 2px solid #8BC34A;
  border-top: none;
  margin-top: -1px;
}

.apple-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

.apple-stat-card {
  background: linear-gradient(135deg, #FAFBFC 0%, #F8F9FA 100%);
  border-radius: 16px;
  padding: 18px;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.apple-stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.apple-stat-icon {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}

.apple-stat-icon.blue {
  background: linear-gradient(135deg, #007AFF 0%, #5AC8FA 100%);
}

.apple-stat-icon.green {
  background: linear-gradient(135deg, #34C759 0%, #30D158 100%);
}

.apple-stat-icon.purple {
  background: linear-gradient(135deg, #AF52DE 0%, #BF5AF2 100%);
}

.apple-stat-icon svg {
  width: 19px;
  height: 19px;
  stroke: white;
  stroke-width: 2.5;
  fill: none;
}

.apple-stat-value {
  font-size: 22px;
  font-weight: 700;
  color: var(--apple-text);
  line-height: 1;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: transform;
  letter-spacing: -0.3px;
}

/* Animación sutil cuando el contador se actualiza (Apple-style) */
.apple-stat-value.updating {
  animation: counter-pulse 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes counter-pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.apple-stat-label {
  font-size: 11px;
  color: var(--apple-gray-4);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ==================== SEARCH & FILTERS INSIDE STATS ==================== */
.apple-search-section {
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  padding-top: 16px;
  margin-top: 4px;
}

.apple-search-row {
  display: flex;
  gap: 12px;
  margin-bottom: 12px;
  align-items: center;
}

.apple-search-container {
  position: relative;
  flex: 1;
}

.apple-search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  stroke: #007AFF;
  stroke-width: 2.5;
  pointer-events: none;
  z-index: 1;
}

.apple-search-input {
  width: 100%;
  height: 44px;
  padding: 0 44px 0 44px;
  border: 1.5px solid transparent;
  border-radius: 22px;
  background: var(--apple-gray-1);
  font-size: 13px;
  font-weight: 500;
  color: var(--apple-text);
  transition: all 0.25s ease;
}

.apple-search-input::placeholder {
  color: var(--apple-gray-4);
  font-size: 13px;
}

.apple-search-input:hover {
  background: rgba(0, 122, 255, 0.04);
  border-color: rgba(0, 122, 255, 0.08);
}

.apple-search-input:focus {
  outline: none;
  border-color: rgba(0, 122, 255, 0.2);
  background: white;
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.05);
}

.apple-filter-controls {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.apple-filter-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 18px;
  background: white;
  border: 1.5px solid var(--apple-gray-3);
  border-radius: 18px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.apple-filter-btn svg {
  width: 16px;
  height: 16px;
  stroke-width: 2;
}

.apple-filter-btn.reset {
  color: #FF3B30;
  border-color: rgba(255, 59, 48, 0.2);
}

.apple-filter-btn.reset:hover {
  background: rgba(255, 59, 48, 0.08);
  border-color: #FF3B30;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(255, 59, 48, 0.2);
}

.apple-filter-btn.reset svg {
  stroke: #FF3B30;
}

.apple-filter-btn.export {
  color: #34C759;
  border-color: rgba(52, 199, 89, 0.2);
}

.apple-filter-btn.export:hover {
  background: rgba(52, 199, 89, 0.08);
  border-color: #34C759;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(52, 199, 89, 0.2);
}

.apple-filter-btn.export svg {
  stroke: #34C759;
}

.apple-clear-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  width: 32px;
  height: 32px;
  background: var(--apple-gray-3);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.apple-clear-btn:hover {
  background: var(--apple-gray-4);
  transform: translateY(-50%) scale(1.1);
}

.apple-clear-btn svg {
  width: 18px;
  height: 18px;
  stroke: white;
  stroke-width: 2.5;
}

.apple-quick-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.apple-filter-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 9px 16px;
  background: var(--apple-gray-1);
  border: 2px solid transparent;
  border-radius: 24px;
  font-size: 12px;
  font-weight: 600;
  color: var(--apple-text);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.apple-filter-chip svg {
  width: 14px;
  height: 14px;
  stroke-width: 2;
}

.apple-filter-chip:hover {
  background: rgba(0, 122, 255, 0.1);
  border-color: rgba(0, 122, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 122, 255, 0.15);
}

.apple-filter-chip.active {
  background: linear-gradient(135deg, #007AFF 0%, #0051D5 100%);
  border-color: #007AFF;
  color: white !important;
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.4);
  transform: translateY(-2px);
}

.apple-filter-chip.active span {
  color: white !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.apple-filter-chip.active svg {
  stroke: white !important;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

/* ==================== TABLE ==================== */
.apple-table-container {
  background: white;
  border-radius: 20px;
  box-shadow: var(--apple-shadow);
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.04);
  max-height: calc(100vh - 340px);
  display: flex;
  flex-direction: column;
}

.apple-table-wrapper {
  overflow-y: auto;
  overflow-x: hidden;
  flex: 1;
  max-height: 100%;
}

/* Scrollbar estilo Apple */
.apple-table-wrapper::-webkit-scrollbar {
  width: 8px;
}

.apple-table-wrapper::-webkit-scrollbar-track {
  background: transparent;
}

.apple-table-wrapper::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.15);
  border-radius: 10px;
  border: 2px solid transparent;
  background-clip: content-box;
}

.apple-table-wrapper::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.25);
  background-clip: content-box;
}

.apple-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: auto;
}

.apple-table thead {
  position: sticky;
  top: 0;
  z-index: 10;
  background: var(--apple-gray-1);
  border-bottom: 1px solid var(--apple-gray-2);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.apple-table th {
  padding: 12px 16px;
  text-align: left;
  font-size: 11px;
  font-weight: 700;
  color: var(--apple-gray-5);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: linear-gradient(to bottom, #F8F9FA 0%, #F1F3F5 100%);
  white-space: nowrap;
  position: sticky;
  top: 0;
}

.apple-table th:first-child {
  border-top-left-radius: 20px;
}

.apple-table th:last-child {
  border-top-right-radius: 20px;
}

.apple-table-row {
  border-bottom: 1px solid #E5E7EB;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  background: white;
}

.apple-table-row:nth-child(even) {
  background: linear-gradient(to right, #FAFBFC 0%, #F8F9FA 100%);
}

.apple-table-row:hover {
  background: rgba(0, 122, 255, 0.04);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transform: scale(1.001);
}

.apple-table td {
  padding: 14px 16px;
  font-size: 13px;
  color: var(--apple-text);
  border-left: 3px solid transparent;
  transition: border-color 0.2s;
}

.apple-table-row:hover td:first-child {
  border-left-color: #007AFF;
}

/* ==================== TABLE CELLS ==================== */
.apple-user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.apple-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #007AFF 0%, #5AC8FA 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  font-weight: 700;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 122, 255, 0.25);
}

.apple-avatar svg {
  width: 22px;
  height: 22px;
  stroke: white;
  stroke-width: 2.5;
  fill: none;
}

.apple-user-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--apple-text);
}

.apple-user-role {
  font-size: 12px;
  color: var(--apple-gray-4);
}

.apple-email {
  font-size: 13px;
  color: var(--apple-gray-4);
  font-style: italic;
}

.apple-date-badge,
.apple-time-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
}

.apple-date-badge {
  background: rgba(0, 122, 255, 0.1);
  color: var(--apple-blue);
}

.apple-time-badge.entrada {
  background: rgba(52, 199, 89, 0.1);
  color: var(--apple-green);
}

.apple-time-badge.salida {
  background: rgba(255, 59, 48, 0.1);
  color: #FF3B30;
}

.apple-location-btn {
  min-width: 36px;
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #007AFF 0%, #5AC8FA 100%);
  border: none;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 122, 255, 0.25);
}

.apple-location-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 14px rgba(0, 122, 255, 0.4);
  background: linear-gradient(135deg, #0051D5 0%, #4AB8F1 100%);
}

.apple-location-btn svg {
  width: 18px;
  height: 18px;
  stroke: white;
  stroke-width: 2.5;
  fill: none;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.apple-photos-cell {
  display: flex;
  gap: 8px;
}

.apple-photo-thumb {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  object-fit: cover;
  cursor: pointer;
  transition: all 0.2s;
}

.apple-photo-thumb:hover {
  transform: scale(1.1);
}

.apple-status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.apple-status-badge.completa {
  background: rgba(52, 199, 89, 0.1);
  color: var(--apple-green);
}

.apple-status-badge.en-curso {
  background: rgba(255, 149, 0, 0.1);
  color: #FF9500;
}

.apple-status-badge.sin-entrada {
  background: rgba(255, 59, 48, 0.1);
  color: #FF3B30;
}

.apple-no-data {
  color: var(--apple-gray-4);
  font-size: 14px;
}

/* ==================== PAGINATION ==================== */
.apple-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px 20px;
  border-top: 1px solid var(--apple-gray-2);
  background: white;
  position: sticky;
  bottom: 0;
  z-index: 5;
}

.apple-pagination-btn {
  width: 40px;
  height: 40px;
  background: var(--apple-gray-1);
  border: none;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.apple-pagination-btn:hover:not(:disabled) {
  background: var(--apple-gray-2);
}

.apple-pagination-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.apple-pagination-btn svg {
  width: 20px;
  height: 20px;
  stroke: var(--apple-text);
  stroke-width: 2;
}

.apple-pagination-numbers {
  display: flex;
  gap: 4px;
}

.apple-pagination-number {
  width: 40px;
  height: 40px;
  background: transparent;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: var(--apple-text);
  cursor: pointer;
  transition: all 0.2s;
}

.apple-pagination-number:hover {
  background: var(--apple-gray-1);
}

.apple-pagination-number.active {
  background: var(--apple-blue);
  color: white;
}

/* ==================== STATES ==================== */
.apple-loading,
.apple-error,
.apple-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 40px;
  text-align: center;
}

.apple-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--apple-gray-2);
  border-top-color: var(--apple-blue);
  border-radius: 50%;
  animation: apple-spin 0.8s linear infinite;
  margin-bottom: 24px;
}

.apple-loading p,
.apple-error p,
.apple-empty p {
  fontSize: 16px;
  color: var(--apple-gray-4);
  margin-top: 12px;
}

.apple-error svg,
.apple-empty svg {
  width: 64px;
  height: 64px;
  stroke: var(--apple-gray-3);
  stroke-width: 2;
  margin-bottom: 20px;
}

.apple-empty h3 {
  font-size: 24px;
  font-weight: 700;
  color: var(--apple-text);
  margin-bottom: 8px;
}

.apple-retry-btn {
  margin-top: 20px;
  padding: 12px 24px;
  background: var(--apple-blue);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.apple-retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 122, 255, 0.3);
}

/* ==================== MODALS ==================== */
.apple-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 40px;
}

.apple-modal-content {
  position: relative;
  background: white;
  border-radius: 20px;
  max-width: 90vw;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.apple-modal-close {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 36px;
  height: 36px;
  background: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  z-index: 10;
}

.apple-modal-close:hover {
  background: rgba(0, 0, 0, 0.2);
}

.apple-modal-close svg {
  width: 20px;
  height: 20px;
  stroke: white;
  stroke-width: 2;
}

.apple-modal-image {
  max-width: 100%;
  max-height: 90vh;
  display: block;
}

.apple-modal-fade-enter-active,
.apple-modal-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-modal-fade-enter-from,
.apple-modal-fade-leave-to {
  opacity: 0;
}

.apple-modal-fade-enter-from .apple-modal-content,
.apple-modal-fade-leave-to .apple-modal-content {
  transform: scale(0.9);
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 1024px) {
  .apple-main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
  
  .apple-content-wrapper {
    padding: 24px 24px;
  }
  
  .apple-page-header {
    padding: 16px 24px;
  }
}

@media (max-width: 768px) {
  .apple-main-content {
    margin-left: 0;
    width: 100vw;
  }
  
  .apple-content-wrapper {
    padding: 16px;
  }
  
  .apple-page-header {
    padding: 12px 24px;
  }
  
  .apple-header-wrapper {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .apple-page-title {
    font-size: 24px;
  }
  
  .apple-stats-grid {
    grid-template-columns: 1fr;
  }
  
  .apple-table {
    font-size: 12px;
  }
  
  .apple-table th,
  .apple-table td {
    padding: 12px;
  }
}
</style>
