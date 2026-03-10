<template>
  <div class="apple-asistencia-container">
    <!-- Apple Dynamic Background -->
    <div class="apple-dynamic-bg">
      <div class="apple-orb apple-orb-1"></div>
      <div class="apple-orb apple-orb-2"></div>
      <div class="apple-orb apple-orb-3"></div>
    </div>
    
    <Sidebar @logout="logout" />
    
    <main class="apple-main-content">
      <!-- ================== STICKY WRAPPER FOR HEADER + STATS ================== -->
      <div class="apple-sticky-wrapper">
        <!-- ================== HEADER APPLE STYLE ================== -->
        <header class="apple-page-header">
          <div class="apple-header-wrapper">
            <div class="apple-header-center">
              <div class="apple-title-group">
                <div class="apple-icon-mini">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10" stroke-width="2"/>
                    <path d="M9 12l2 2 4-4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <span class="apple-title-divider">|</span>
                <h1 class="apple-page-title">ASISTENCIAS</h1>
              </div>
              <p class="apple-page-subtitle">Control de registros de entrada y salida</p>
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
            <div class="apple-search-container" ref="searchContainer">
              <svg class="apple-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="11" cy="11" r="8" stroke-width="2.5"/>
                <path d="m21 21-4.35-4.35" stroke-width="2.5" stroke-linecap="round"/>
              </svg>
              <input 
                ref="searchInput"
                v-model="searchTerm" 
                @input="onSearchInput"
                @focus="abrirDropdown"
                @blur="cerrarDropdownConDelay"
                type="text" 
                placeholder="Buscar por nombre, correo o CURP..." 
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

          <!-- ================== FILTROS DE TIPO ASISTENCIA ================== -->
          <div class="apple-type-filters">
            <span class="apple-type-label">Mostrar:</span>
            <div class="apple-type-buttons">
              <button 
                v-for="tipo in tiposFiltro" 
                :key="tipo.value"
                @click="seleccionarTipo(tipo.value)" 
                :class="['apple-type-chip', { 'active': filtroTipo === tipo.value }]"
              >
                <svg v-if="tipo.value === 'todas'" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M4 6h16M4 12h16M4 18h16" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <svg v-else-if="tipo.value === 'entradas'" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <polyline points="10 17 15 12 10 7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <line x1="15" y1="12" x2="3" y2="12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg v-else-if="tipo.value === 'salidas'" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <polyline points="16 17 21 12 16 7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <line x1="21" y1="12" x2="9" y2="12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <polyline points="22 4 12 14.01 9 11.01" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>{{ tipo.label }}</span>
              </button>
            </div>
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
            <div class="apple-pagination-controls">
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
            
            <!-- ================== LOAD MORE BUTTON ================== -->
            <button 
              v-if="hayMasRegistros && asistencias.length > 0"
              @click="cargarMasAsistencias" 
              :disabled="cargandoMas"
              class="apple-load-more-btn"
            >
              <svg v-if="!cargandoMas" viewBox="0 0 24 24" fill="none" stroke="currentColor" class="apple-load-more-icon">
                <path d="M12 5v14M5 12h14" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <div v-else class="apple-load-more-spinner"></div>
              <span>{{ cargandoMas ? 'Cargando...' : 'Cargar más' }}</span>
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- ================== MODALS ================== -->
    <transition name="apple-modal-fade">
      <div v-if="modalVisible" class="apple-modal-overlay" @click="cerrarModal">
        <div class="apple-modal-content" @click.stop>
          <div class="lightbox-image-wrapper">
            <img :src="modalImage" :alt="modalTitle" class="apple-modal-image">
            <!-- Botón de cerrar estilo liquid glass -->
            <button @click="cerrarModal" class="lightbox-close-btn">
              ×
            </button>
          </div>
        </div>
      </div>
    </transition>

    <MapaAsistenciaModal 
      :visible="mapaModalVisible"
      :asistencia="asistenciaSeleccionada"
      :tipo="tipoMapa"
      @cerrar="cerrarMapaModal"
    />

    <!-- DROPDOWN DE BÚSQUEDA - TELEPORT AL BODY -->
    <Teleport to="body">
      <Transition name="apple-dropdown">
        <div 
          v-if="mostrarDropdown && searchTerm.length > 0" 
          class="apple-search-dropdown-portal"
          :style="dropdownStyle"
          @mousedown.prevent
        >
          <div v-if="searchTerm.length < 2" class="apple-dropdown-hint">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 8v4m0 4h.01"/>
            </svg>
            <span>Escribe al menos 2 caracteres</span>
          </div>
          <div v-else-if="resultadosBusqueda.length === 0" class="apple-dropdown-empty">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
            <span>No se encontraron resultados</span>
          </div>
          <div v-else class="apple-dropdown-results">
            <div 
              v-for="resultado in resultadosBusqueda" 
              :key="resultado.id" 
              class="apple-dropdown-item"
              @click="seleccionarResultado(resultado)"
            >
              <div class="apple-dropdown-avatar">
                {{ getInitials(resultado.nombre_usuario) }}
              </div>
              <div class="apple-dropdown-info">
                <div class="apple-dropdown-name">{{ resultado.nombre_usuario }}</div>
                <div class="apple-dropdown-email">{{ resultado.correo_usuario || 'Sin correo' }}</div>
                <div v-if="resultado.curp_usuario" class="apple-dropdown-curp">CURP: {{ resultado.curp_usuario }}</div>
              </div>
              <div class="apple-dropdown-badge" :class="resultado.presente ? 'presente' : 'ausente'">
                {{ resultado.presente ? 'Presente' : 'Ausente' }}
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
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
      ],
      // Filtros de tipo de asistencia
      tiposFiltro: [
        { label: 'Todas', value: 'todas' },
        { label: 'Solo entradas', value: 'entradas' },
        { label: 'Solo salidas', value: 'salidas' },
        { label: 'Completas', value: 'completas' }
      ],
      filtroTipo: 'todas',
      // Carga incremental
      registrosCargados: 200,
      registrosPorCarga: 200,
      cargandoMas: false,
      hayMasRegistros: true,
      // Dropdown de búsqueda Apple
      mostrarDropdown: false,
      dropdownPosition: { top: 0, left: 0, width: 0 }
    }
  },
  computed: {
    // Estilo del dropdown posicionado
    dropdownStyle() {
      return {
        position: 'fixed',
        top: `${this.dropdownPosition.top}px`,
        left: `${this.dropdownPosition.left}px`,
        width: `${this.dropdownPosition.width}px`,
        zIndex: 99999
      }
    },
    // Resultados de búsqueda para dropdown Apple
    resultadosBusqueda() {
      if (!this.searchTerm || this.searchTerm.length < 2) return []
      const termino = this.searchTerm.toLowerCase()
      const resultados = this.asistencias.filter(asistencia => 
        (asistencia.nombre_usuario && asistencia.nombre_usuario.toLowerCase().includes(termino)) ||
        (asistencia.correo_usuario && asistencia.correo_usuario.toLowerCase().includes(termino)) ||
        (asistencia.curp_usuario && asistencia.curp_usuario.toLowerCase().includes(termino))
      )
      // Agrupar por usuario único y mostrar máximo 8
      const usuariosUnicos = new Map()
      resultados.forEach(a => {
        if (!usuariosUnicos.has(a.nombre_usuario)) {
          usuariosUnicos.set(a.nombre_usuario, a)
        }
      })
      return Array.from(usuariosUnicos.values()).slice(0, 8)
    },
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
      this.registrosCargados = 200
      
      try {
        console.time('⚡ Carga total de asistencias')
        
        // Refrescar estadísticas en tiempo real (Apple-style)
        await this.refreshStats()
        
        const asistencias = await AsistenciasService.obtenerAsistenciasConUsuarios(this.registrosCargados)
        
        this.asistencias = asistencias
        this.hayMasRegistros = asistencias.length === this.registrosCargados
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
    
    async cargarMasAsistencias() {
      if (this.cargandoMas || !this.hayMasRegistros) return
      
      this.cargandoMas = true
      
      try {
        this.registrosCargados += this.registrosPorCarga
        console.log(`📥 Cargando más asistencias... Total: ${this.registrosCargados}`)
        
        const asistencias = await AsistenciasService.obtenerAsistenciasConUsuarios(this.registrosCargados)
        
        this.asistencias = asistencias
        this.hayMasRegistros = asistencias.length === this.registrosCargados
        this.filtrarAsistencias()
        
        console.log(`✅ ${asistencias.length} asistencias totales cargadas`)
      } catch (error) {
        console.error('Error al cargar más asistencias:', error)
        this.error = 'Error al cargar más registros. Por favor, intenta de nuevo.'
      } finally {
        this.cargandoMas = false
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

      // ========== FILTRO POR BÚSQUEDA (nombre, correo, CURP) ==========
      if (this.searchTerm) {
        const termino = this.searchTerm.toLowerCase()
        filtradas = filtradas.filter(asistencia => 
          (asistencia.nombre_usuario && asistencia.nombre_usuario.toLowerCase().includes(termino)) ||
          (asistencia.correo_usuario && asistencia.correo_usuario.toLowerCase().includes(termino)) ||
          (asistencia.curp_usuario && asistencia.curp_usuario.toLowerCase().includes(termino))
        )
      }

      // ========== FILTRO POR TIPO DE ASISTENCIA ==========
      if (this.filtroTipo && this.filtroTipo !== 'todas') {
        switch (this.filtroTipo) {
          case 'entradas':
            // Solo registros que tienen entrada pero NO salida
            filtradas = filtradas.filter(a => a.hora_entrada && !a.hora_salida)
            break
          case 'salidas':
            // Solo registros que tienen salida (con o sin entrada)
            filtradas = filtradas.filter(a => a.hora_salida)
            break
          case 'completas':
            // Solo registros que tienen AMBOS: entrada Y salida
            filtradas = filtradas.filter(a => a.hora_entrada && a.hora_salida)
            break
        }
      }

      // ========== FILTRO POR FECHA ==========
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
      this.filtroTipo = 'todas'
      this.mostrarDropdown = false
      this.filtrarAsistencias()
    },
    
    seleccionarTipo(tipo) {
      this.filtroTipo = tipo
      this.filtrarAsistencias()
    },
    
    seleccionarResultado(resultado) {
      this.searchTerm = resultado.nombre_usuario
      this.mostrarDropdown = false
      this.filtrarAsistencias()
    },
    
    cerrarDropdownConDelay() {
      setTimeout(() => {
        this.mostrarDropdown = false
      }, 180)
    },
    
    abrirDropdown() {
      this.actualizarPosicionDropdown()
      this.mostrarDropdown = true
    },
    
    onSearchInput() {
      this.actualizarPosicionDropdown()
      this.filtrarAsistencias()
    },
    
    actualizarPosicionDropdown() {
      if (this.$refs.searchContainer) {
        const rect = this.$refs.searchContainer.getBoundingClientRect()
        this.dropdownPosition = {
          top: rect.bottom + 8,
          left: rect.left,
          width: rect.width
        }
      }
    },
    
    getInitials(name) {
      if (!name) return '?'
      const words = name.trim().split(' ')
      if (words.length >= 2) {
        return (words[0][0] + words[1][0]).toUpperCase()
      }
      return name.substring(0, 2).toUpperCase()
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
  background: linear-gradient(180deg, #f0fdf4 0%, #ecfdf5 50%, #f0fdf4 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  position: relative;
  overflow-x: hidden;
  overflow-y: visible;
}

/* Dynamic Background */
.apple-dynamic-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.apple-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(70px);
  opacity: 0.6;
  animation: appleOrbFloat 20s ease-in-out infinite;
}

.apple-orb-1 {
  width: 300px;
  height: 300px;
  top: 10%;
  right: 15%;
  background: linear-gradient(135deg, rgba(139, 195, 74, 0.4), rgba(102, 187, 106, 0.3));
}

.apple-orb-2 {
  width: 250px;
  height: 250px;
  top: 50%;
  left: 10%;
  background: linear-gradient(135deg, rgba(165, 214, 167, 0.35), rgba(129, 199, 132, 0.2));
  animation-delay: -7s;
}

.apple-orb-3 {
  width: 280px;
  height: 280px;
  bottom: 15%;
  left: 25%;
  background: linear-gradient(135deg, rgba(102, 187, 106, 0.35), rgba(76, 175, 80, 0.25));
  animation-delay: -14s;
}

@keyframes appleOrbFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(20px, -30px) scale(1.05); }
  50% { transform: translate(-10px, 20px) scale(0.95); }
  75% { transform: translate(30px, 10px) scale(1.02); }
}

.apple-main-content {
  flex: 1;
  margin-left: 220px;
  width: calc(100vw - 220px);
  overflow-x: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  padding: 8px 16px 0 16px;
  position: relative;
  z-index: 1;
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
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 50%, #2E7D32 100%);
  border-bottom: none;
  padding: 14px 20px;
  border-radius: 28px 28px 0 0;
  border: 2px solid #8BC34A;
  border-bottom: none;
}

.apple-header-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.apple-header-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.apple-title-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.apple-icon-mini {
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.apple-icon-mini svg {
  width: 18px;
  height: 18px;
  stroke: rgba(255, 255, 255, 0.9);
  stroke-width: 2;
}

.apple-title-divider {
  color: rgba(255, 255, 255, 0.4);
  font-size: 18px;
  font-weight: 300;
}

.apple-page-title {
  font-size: 18px;
  font-weight: 700;
  color: white;
  margin: 0;
  letter-spacing: 1.5px;
  text-transform: uppercase;
}

.apple-page-subtitle {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  font-weight: 500;
  letter-spacing: 0.3px;
}

.apple-refresh-button {
  position: absolute;
  right: 0;
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.apple-refresh-button:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.25);
}

.apple-refresh-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.apple-refresh-button svg {
  width: 14px;
  height: 14px;
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
  padding: 18px 16px 16px 16px;
  margin-bottom: 0;
  box-shadow: none;
  border: 2px solid #8BC34A;
  border-top: none;
  margin-top: -1px;
  overflow: visible;
  position: relative;
  z-index: 100;
}

.apple-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 10px;
  margin-bottom: 12px;
}

.apple-stat-card {
  background: linear-gradient(135deg, #FAFBFC 0%, #F8F9FA 100%);
  border-radius: 14px;
  padding: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.apple-stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.apple-stat-icon {
  width: 36px;
  height: 36px;
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
  width: 16px;
  height: 16px;
  stroke: white;
  stroke-width: 2.5;
  fill: none;
}

.apple-stat-value {
  font-size: 18px;
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
  font-size: 10px;
  color: var(--apple-gray-4);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ==================== SEARCH & FILTERS INSIDE STATS ==================== */
.apple-search-section {
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  padding-top: 12px;
  margin-top: 4px;
  overflow: visible;
  position: relative;
  z-index: 200;
}

.apple-search-row {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  align-items: center;
  overflow: visible;
}

.apple-search-container {
  position: relative;
  flex: 1;
  z-index: 300;
}

.apple-search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  stroke: #007AFF;
  stroke-width: 2.5;
  pointer-events: none;
  z-index: 1;
}

.apple-search-input {
  width: 100%;
  height: 38px;
  padding: 0 40px 0 40px;
  border: 1.5px solid transparent;
  border-radius: 19px;
  background: #f5f5f7;
  font-size: 12px;
  font-weight: 500;
  color: #1d1d1f;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
  transition: all 0.25s ease;
}

.apple-search-input::placeholder {
  color: #86868b;
  font-size: 12px;
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
  padding: 8px 14px;
  background: white;
  border: 1.5px solid var(--apple-gray-3);
  border-radius: 16px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.apple-filter-btn svg {
  width: 15px;
  height: 15px;
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
  width: 28px;
  height: 28px;
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
  width: 16px;
  height: 16px;
  stroke: white;
  stroke-width: 2.5;
}

/* ==================== APPLE SEARCH DROPDOWN PORTAL ==================== */
/* Must be global styles since dropdown is teleported to body */
</style>

<style>
/* DROPDOWN PORTAL - ESTILOS GLOBALES */
.apple-search-dropdown-portal {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 18px;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 12px 24px -8px rgba(0, 0, 0, 0.12),
    0 0 0 1px rgba(0, 0, 0, 0.05);
  max-height: 400px;
  overflow-y: auto;
  overflow-x: hidden;
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

/* Transition animation */
.apple-dropdown-enter-active {
  animation: appleDropdownEnter 0.28s cubic-bezier(0.32, 0.72, 0, 1);
}

.apple-dropdown-leave-active {
  animation: appleDropdownLeave 0.2s cubic-bezier(0.32, 0.72, 0, 1);
}

@keyframes appleDropdownEnter {
  0% { 
    opacity: 0; 
    transform: translateY(-12px) scale(0.94);
  }
  100% { 
    opacity: 1; 
    transform: translateY(0) scale(1);
  }
}

@keyframes appleDropdownLeave {
  0% { 
    opacity: 1; 
    transform: translateY(0) scale(1);
  }
  100% { 
    opacity: 0; 
    transform: translateY(-8px) scale(0.96);
  }
}

.apple-search-dropdown-portal .apple-dropdown-hint,
.apple-search-dropdown-portal .apple-dropdown-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  padding: 40px 28px;
  color: #8e8e93;
  font-size: 15px;
  font-weight: 500;
  text-align: center;
}

.apple-search-dropdown-portal .apple-dropdown-hint svg,
.apple-search-dropdown-portal .apple-dropdown-empty svg {
  width: 36px;
  height: 36px;
  stroke: #c7c7cc;
  flex-shrink: 0;
}

.apple-search-dropdown-portal .apple-dropdown-results {
  padding: 8px;
}

.apple-search-dropdown-portal .apple-dropdown-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  margin-bottom: 2px;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-search-dropdown-portal .apple-dropdown-item:last-child {
  margin-bottom: 0;
}

.apple-search-dropdown-portal .apple-dropdown-item:hover {
  background: rgba(0, 122, 255, 0.08);
}

.apple-search-dropdown-portal .apple-dropdown-item:active {
  background: rgba(0, 122, 255, 0.15);
  transform: scale(0.98);
}

.apple-search-dropdown-portal .apple-dropdown-avatar {
  width: 46px;
  height: 46px;
  background: linear-gradient(145deg, #34C759 0%, #30D158 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: white;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.02em;
  box-shadow: 0 4px 14px rgba(52, 199, 89, 0.35);
}

.apple-search-dropdown-portal .apple-dropdown-info {
  flex: 1;
  min-width: 0;
}

.apple-search-dropdown-portal .apple-dropdown-name {
  font-size: 16px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  letter-spacing: -0.01em;
}

.apple-search-dropdown-portal .apple-dropdown-email {
  font-size: 13px;
  color: #8e8e93;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.apple-search-dropdown-portal .apple-dropdown-curp {
  font-size: 11px;
  color: #007AFF;
  font-weight: 500;
  letter-spacing: 0.02em;
  margin-top: 2px;
}

.apple-search-dropdown-portal .apple-dropdown-badge {
  padding: 6px 14px;
  border-radius: 100px;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
  letter-spacing: -0.01em;
}

.apple-search-dropdown-portal .apple-dropdown-badge.presente {
  background: linear-gradient(135deg, rgba(52, 199, 89, 0.18) 0%, rgba(48, 209, 88, 0.12) 100%);
  color: #248A3D;
}

.apple-search-dropdown-portal .apple-dropdown-badge.ausente {
  background: linear-gradient(135deg, rgba(255, 59, 48, 0.18) 0%, rgba(255, 69, 58, 0.12) 100%);
  color: #D70015;
}
</style>

<style scoped>
.apple-quick-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.apple-filter-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 7px 12px;
  background: var(--apple-gray-1);
  border: 2px solid transparent;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  color: var(--apple-text);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.apple-filter-chip svg {
  width: 13px;
  height: 13px;
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

/* ==================== FILTROS DE TIPO ==================== */
.apple-type-filters {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.apple-type-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--apple-text-secondary);
  white-space: nowrap;
}

.apple-type-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.apple-type-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: var(--apple-gray-1);
  border: 2px solid transparent;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  color: var(--apple-text);
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.apple-type-chip svg {
  width: 14px;
  height: 14px;
  stroke-width: 2;
}

.apple-type-chip:hover {
  background: rgba(52, 199, 89, 0.1);
  border-color: rgba(52, 199, 89, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(52, 199, 89, 0.15);
}

.apple-type-chip.active {
  background: linear-gradient(135deg, #34C759 0%, #248A3D 100%);
  border-color: #34C759;
  color: white !important;
  box-shadow: 0 4px 14px rgba(52, 199, 89, 0.4);
  transform: translateY(-2px);
}

.apple-type-chip.active span {
  color: white !important;
}

.apple-type-chip.active svg {
  stroke: white !important;
}

/* Colores específicos para cada tipo */
.apple-type-chip[data-tipo="entradas"]:hover {
  background: rgba(0, 122, 255, 0.1);
  border-color: rgba(0, 122, 255, 0.2);
}

.apple-type-chip[data-tipo="salidas"]:hover {
  background: rgba(255, 149, 0, 0.1);
  border-color: rgba(255, 149, 0, 0.2);
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
  overflow-x: auto;
  flex: 1;
  max-height: 100%;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior-x: contain;
  overscroll-behavior-y: auto;
  scroll-behavior: smooth;
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
  background: #E8F5E9;
  border-bottom: 1px solid #C8E6C9;
}

.apple-table th {
  padding: 16px 20px;
  text-align: left;
  font-size: 12px;
  font-weight: 600;
  color: #2E7D32;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  background: #E8F5E9;
  white-space: nowrap;
  position: sticky;
  top: 0;
  border-bottom: 1px solid #C8E6C9;
  border-right: 1px solid #C8E6C9;
}

.apple-table th:last-child {
  border-right: none;
}

.apple-table-row {
  border-bottom: 1px solid #F0F0F0;
  transition: all 0.15s ease;
  background: white;
}

.apple-table-row:nth-child(even) {
  background: #FAFAFA;
}

.apple-table-row:hover {
  background: #F5F5F7;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.apple-table td {
  padding: 16px 20px;
  font-size: 13px;
  color: #1D1D1F;
  border-left: 2px solid transparent;
  transition: all 0.15s ease;
}

.apple-table-row:hover td:first-child {
  border-left-color: #0071E3;
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
  background: linear-gradient(135deg, #66BB6A 0%, #81C784 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  font-weight: 700;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(102, 187, 106, 0.25);
}

.apple-avatar svg {
  width: 22px;
  height: 22px;
  stroke: white;
  stroke-width: 2.5;
  fill: none;
}

.apple-user-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--apple-text);
}

.apple-user-role {
  font-size: 11px;
  color: var(--apple-gray-4);
}

.apple-email {
  font-size: 12px;
  color: var(--apple-gray-4);
  font-style: italic;
}

.apple-date-badge,
.apple-time-badge {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 8px;
  font-size: 12px;
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
  gap: 10px;
  justify-content: center;
  align-items: center;
}

.apple-photo-thumb {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  object-fit: cover;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid rgba(139, 195, 74, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.apple-photo-thumb:hover {
  transform: scale(1.15);
  border-color: #8BC34A;
  box-shadow: 0 4px 16px rgba(139, 195, 74, 0.35);
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
  justify-content: space-between;
  gap: 16px;
  padding: 10px 16px;
  border-top: 1px solid #C8E6C9;
  background: #E8F5E9;
  position: sticky;
  bottom: 0;
  z-index: 5;
}

.apple-pagination-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.apple-pagination-btn {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #8BC34A 0%, #7CB342 100%);
  border: none;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(139, 195, 74, 0.3);
}

.apple-pagination-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #7CB342 0%, #689F38 100%);
  box-shadow: 0 4px 12px rgba(139, 195, 74, 0.4);
  transform: translateY(-1px);
}

.apple-pagination-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
  box-shadow: none;
}

.apple-pagination-btn svg {
  width: 18px;
  height: 18px;
  stroke: white;
  stroke-width: 2.5;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.apple-pagination-numbers {
  display: flex;
  gap: 4px;
}

.apple-pagination-number {
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--apple-text);
  cursor: pointer;
  transition: all 0.2s;
}

.apple-pagination-number:hover {
  background: #E8F5E9;
}

.apple-pagination-number.active {
  background: linear-gradient(135deg, #8BC34A 0%, #66BB6A 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(139, 195, 74, 0.4);
}

/* ==================== LOAD MORE BUTTON ==================== */
.apple-load-more-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: linear-gradient(135deg, #8BC34A 0%, #7CB342 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(139, 195, 74, 0.3);
  white-space: nowrap;
}

.apple-load-more-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #7CB342 0%, #689F38 100%);
  box-shadow: 0 4px 12px rgba(139, 195, 74, 0.4);
  transform: translateY(-1px);
}

.apple-load-more-btn:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(139, 195, 74, 0.3);
}

.apple-load-more-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.apple-load-more-icon {
  width: 16px;
  height: 16px;
  stroke-width: 2.5;
}

.apple-load-more-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: apple-spin 0.8s linear infinite;
}

@keyframes apple-spin {
  to { transform: rotate(360deg); }
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
  font-size: 16px;
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

.lightbox-image-wrapper {
  position: relative;
  display: inline-block;
}

.lightbox-close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.4) 0%,
    rgba(255, 255, 255, 0.15) 50%,
    rgba(255, 255, 255, 0.25) 100%
  );
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1.5px solid rgba(255, 255, 255, 0.5);
  border-radius: 50%;
  width: 46px;
  height: 46px;
  font-size: 26px;
  font-weight: 300;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.2),
    inset 0 1px 1px rgba(255, 255, 255, 0.6),
    inset 0 -1px 1px rgba(255, 255, 255, 0.1);
  z-index: 10002;
  line-height: 1;
  text-align: center;
  padding: 0;
  margin: 0;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.lightbox-close-btn:hover {
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.55) 0%,
    rgba(255, 255, 255, 0.25) 50%,
    rgba(255, 255, 255, 0.35) 100%
  );
  border-color: rgba(255, 255, 255, 0.7);
  transform: scale(1.1) rotate(90deg);
  box-shadow: 
    0 12px 40px rgba(0, 0, 0, 0.25),
    inset 0 1px 2px rgba(255, 255, 255, 0.8),
    inset 0 -1px 1px rgba(255, 255, 255, 0.2),
    0 0 20px rgba(255, 255, 255, 0.15);
}

.lightbox-close-btn:active {
  transform: scale(0.95);
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.6) 0%,
    rgba(255, 255, 255, 0.3) 100%
  );
}

/* Responsive para botón lightbox */
@media (max-width: 768px) {
  .lightbox-close-btn {
    top: 10px;
    right: 10px;
    width: 40px;
    height: 40px;
    font-size: 22px;
  }
}

@media (max-width: 480px) {
  .lightbox-close-btn {
    top: 8px;
    right: 8px;
    width: 36px;
    height: 36px;
    font-size: 20px;
  }
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
  
  .apple-table-container {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  .apple-table {
    min-width: 900px;
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
    padding: 12px 20px;
  }
  
  .apple-header-wrapper {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .apple-page-title {
    font-size: 18px;
  }
  
  .apple-stats-grid {
    grid-template-columns: 1fr;
  }
  
  .apple-table-container {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    overscroll-behavior-x: contain;
    overscroll-behavior-y: auto;
    border-radius: 16px;
  }
  
  .apple-table-wrapper {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    overscroll-behavior-x: contain;
    overscroll-behavior-y: auto;
  }
  
  .apple-table {
    min-width: 1000px;
    font-size: 11px;
  }
  
  .apple-table th,
  .apple-table td {
    padding: 10px 12px;
  }
  
  .apple-pagination {
    padding: 12px 16px;
    flex-wrap: wrap;
  }
  
  .apple-pagination-btn,
  .apple-pagination-number {
    width: 36px;
    height: 36px;
  }
  
  .apple-search-row {
    flex-direction: column;
    gap: 12px;
  }
  
  .apple-filter-controls {
    width: 100%;
    justify-content: space-between;
  }
  
  .apple-type-filters {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .apple-type-buttons {
    width: 100%;
  }
  
  .apple-type-chip {
    padding: 6px 10px;
    font-size: 11px;
    flex: 1;
    justify-content: center;
  }
  
  .apple-type-chip svg {
    width: 12px;
    height: 12px;
  }
}
</style>
