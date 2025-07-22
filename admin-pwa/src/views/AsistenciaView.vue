<template>
  <div class="asistencia-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 6L9 17l-5-5"/>
                <path d="M3 12h6m6-6h6m-6 12h6"/>
                <rect x="7" y="3" width="3" height="18" rx="1"/>
                <rect x="14" y="3" width="3" height="18" rx="1"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Control de Asistencia</h1>
              <p class="header-subtitle">Monitorea el registro de asistencias de todos los usuarios</p>
            </div>
          </div>
          <div class="header-actions">
            <div class="connection-status" :class="{ 'online': isOnline, 'offline': !isOnline }">
              <div class="status-indicator"></div>
              <span class="status-text">{{ isOnline ? 'En línea' : 'Sin conexión' }}</span>
            </div>
            <button @click="cargarAsistencias" class="refresh-btn" :disabled="loading">
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
            <!-- Barra de búsqueda -->
            <div class="search-box">
              <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <path d="m21 21-4.35-4.35"></path>
              </svg>
              <input 
                v-model="searchTerm" 
                type="text" 
                placeholder="Buscar por nombre, correo o ubicación..." 
                class="search-input"
                @input="filtrarAsistencias"
              >
              <button v-if="searchTerm" @click="limpiarBusqueda" class="clear-search-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
            
            <!-- Filtro de rango de fecha con datepickers -->
            <div class="date-range-filter">
              <div class="date-picker-container">
                <label class="date-label">Desde:</label>
                <input 
                  type="date" 
                  v-model="filtroFechaInicio" 
                  class="date-input" 
                  :max="filtroFechaFin || maxDate"
                  @change="filtrarAsistencias"
                >
              </div>
              <div class="date-picker-container">
                <label class="date-label">Hasta:</label>
                <input 
                  type="date" 
                  v-model="filtroFechaFin" 
                  class="date-input" 
                  :min="filtroFechaInicio"
                  :max="maxDate"
                  @change="filtrarAsistencias"
                >
              </div>
              
              <!-- Selectores rápidos de fecha -->
              <div class="quick-date-filters">
                <button 
                  @click="seleccionarFechaRapida('hoy')" 
                  :class="['quick-date-btn', filtroRapido === 'hoy' ? 'active' : '']"
                >
                  Hoy
                </button>
                <button 
                  @click="seleccionarFechaRapida('ayer')" 
                  :class="['quick-date-btn', filtroRapido === 'ayer' ? 'active' : '']"
                >
                  Ayer
                </button>
                <button 
                  @click="seleccionarFechaRapida('semana')" 
                  :class="['quick-date-btn', filtroRapido === 'semana' ? 'active' : '']"
                >
                  Esta semana
                </button>
                <button 
                  @click="seleccionarFechaRapida('mes')" 
                  :class="['quick-date-btn', filtroRapido === 'mes' ? 'active' : '']"
                >
                  Este mes
                </button>
                <button 
                  v-if="hayFiltrosFechas" 
                  @click="limpiarFiltrosFechas" 
                  class="clear-date-btn"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                  Limpiar
                </button>
              </div>
            </div>
          </div>
          
          <!-- Filtros adicionales y acciones (expandibles) -->
          <div class="filters-advanced" v-show="mostrarFiltrosAvanzados">
            <div class="advanced-filters-grid">
              <!-- Filtro por estado -->
              <div class="filter-group">
                <label class="filter-label">Estado</label>
                <div class="filter-options">
                  <label class="checkbox-option">
                    <input type="checkbox" v-model="filtroEntrada" @change="filtrarAsistencias">
                    <span>Con entrada</span>
                  </label>
                  <label class="checkbox-option">
                    <input type="checkbox" v-model="filtroSalida" @change="filtrarAsistencias">
                    <span>Con salida</span>
                  </label>
                  <label class="checkbox-option">
                    <input type="checkbox" v-model="filtroSinSalida" @change="filtrarAsistencias">
                    <span>Sin salida</span>
                  </label>
                </div>
              </div>
              
              <!-- Filtro por departamento -->
              <div class="filter-group" v-if="departamentos.length > 0">
                <label class="filter-label">Departamento</label>
                <select v-model="filtroDepartamento" @change="filtrarAsistencias" class="filter-select">
                  <option value="">Todos los departamentos</option>
                  <option v-for="depto in departamentos" :key="depto" :value="depto">{{ depto }}</option>
                </select>
              </div>
              
              <!-- Filtro por usuario -->
              <div class="filter-group">
                <label class="filter-label">Usuario</label>
                <select v-model="filtroUsuario" @change="filtrarAsistencias" class="filter-select">
                  <option value="">Todos los usuarios</option>
                  <option v-for="usuario in usuariosUnicos" :key="usuario.id" :value="usuario.id">
                    {{ usuario.nombre }}
                  </option>
                </select>
              </div>
            </div>
            
            <div class="advanced-actions">
              <button @click="exportarAsistencias('csv')" class="export-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="7 10 12 15 17 10"></polyline>
                  <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
                Exportar CSV
              </button>
              <button @click="exportarAsistencias('excel')" class="export-btn excel">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                  <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
                Exportar Excel
              </button>
              <button @click="imprimirAsistencias" class="export-btn print">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="6 9 6 2 18 2 18 9"></polyline>
                  <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                  <rect x="6" y="14" width="12" height="8"></rect>
                </svg>
                Imprimir
              </button>
            </div>
          </div>
          
          <!-- Botón para mostrar/ocultar filtros avanzados -->
          <button @click="mostrarFiltrosAvanzados = !mostrarFiltrosAvanzados" class="toggle-filters-btn">
            {{ mostrarFiltrosAvanzados ? 'Ocultar filtros avanzados' : 'Mostrar filtros avanzados' }}
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                 :style="{ transform: mostrarFiltrosAvanzados ? 'rotate(180deg)' : 'rotate(0deg)' }">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
          
          <!-- Resumen de filtros activos -->
          <div v-if="filtrosActivos.length > 0" class="active-filters">
            <span class="active-filters-label">Filtros activos:</span>
            <div class="active-filter-tags">
              <div v-for="(filtro, index) in filtrosActivos" :key="index" class="filter-tag">
                {{ filtro.label }}
                <button @click="quitarFiltro(filtro.tipo, filtro.valor)" class="remove-filter">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>
              <button @click="limpiarTodosFiltros" class="clear-all-filters">
                Limpiar todos
              </button>
            </div>
          </div>
        </div>

        <!-- Estadísticas rápidas -->
        <div class="stats-section">
          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
              </svg>
            </div>
            <div class="stat-info">
              <span class="stat-number">{{ totalAsistenciasHoy }}</span>
              <span class="stat-label">Asistencias Hoy</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </div>
            <div class="stat-info">
              <span class="stat-number">{{ usuariosPresentes }}</span>
              <span class="stat-label">Usuarios Presentes</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 6L9 17l-5-5"/>
              </svg>
            </div>
            <div class="stat-info">
              <span class="stat-number">{{ totalAsistencias }}</span>
              <span class="stat-label">Total Registros</span>
            </div>
          </div>
        </div>

        <!-- Tabla de asistencias -->
        <div class="asistencias-section">
          <div v-if="loading && asistencias.length === 0" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando asistencias...</p>
          </div>
          
          <div v-else-if="error" class="error-container">
            <p>{{ error }}</p>
            <button @click="cargarAsistencias" class="retry-btn">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
                <path d="M3 3v5h5"></path>
                <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"></path>
                <path d="M21 21v-5h-5"></path>
              </svg>
              Reintentar
            </button>
          </div>
          
          <div v-else-if="asistenciasFiltradas.length === 0" class="empty-state">
            <div class="empty-icon">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 6L9 17l-5-5"/>
                <path d="M3 12h6m6-6h6m-6 12h6"/>
                <rect x="7" y="3" width="3" height="18" rx="1"/>
                <rect x="14" y="3" width="3" height="18" rx="1"/>
              </svg>
            </div>
            <h3>No hay asistencias</h3>
            <p v-if="searchTerm">No se encontraron asistencias con el término "{{ searchTerm }}"</p>
            <p v-else>Aún no se han registrado asistencias en la aplicación.</p>
          </div>
          
          <div v-else class="table-container">
            <table class="asistencias-table">
              <thead>
                <tr>
                  <th>Usuario</th>
                  <th>Correo</th>
                  <th>Fecha</th>
                  <th>Entrada</th>
                  <th>Salida</th>
                  <th>Ubicación Entrada</th>
                  <th>Ubicación Salida</th>
                  <th>Fotos</th>
                  <th>Observaciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="asistencia in asistenciasFiltradas" :key="asistencia.id">
                  <td>
                    <div class="user-info">
                      <div class="user-avatar">
                        {{ obtenerIniciales(asistencia.nombre_usuario) }}
                      </div>
                      <div class="user-details">
                        <span class="user-name">{{ asistencia.nombre_usuario }}</span>
                        <span class="user-cargo">{{ asistencia.cargo_usuario }}</span>
                      </div>
                    </div>
                  </td>
                  <td>{{ asistencia.correo_usuario }}</td>
                  <td>
                    <span class="date-badge">
                      {{ formatearFecha(asistencia.fecha) }}
                    </span>
                  </td>
                  <td>
                    <span class="time-badge entrada" v-if="asistencia.hora_entrada">
                      {{ formatearHora(asistencia.hora_entrada) }}
                    </span>
                    <span v-else class="no-data">Sin registro</span>
                  </td>
                  <td>
                    <span class="time-badge salida" v-if="asistencia.hora_salida">
                      {{ formatearHora(asistencia.hora_salida) }}
                    </span>
                    <span v-else class="no-data">Pendiente</span>
                  </td>
                  <td>
                    <div v-if="asistencia.latitud_entrada && asistencia.longitud_entrada" class="location-cell">
                      <div class="location-info">
                        <span class="location-badge compact"
                              :title="`Lat: ${asistencia.latitud_entrada}, Lng: ${asistencia.longitud_entrada}`">
                          {{ formatearCoordenadas(asistencia.latitud_entrada, asistencia.longitud_entrada) }}
                        </span>
                      </div>
                      <div class="location-actions">
                        <button @click="abrirMapaModal(asistencia, 'entrada')" 
                                class="map-btn circular entrada-map"
                                title="Ver ubicación de entrada en el mapa">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                            <circle cx="12" cy="10" r="3"/>
                          </svg>
                        </button>
                      </div>
                    </div>
                    <span v-else class="no-data">N/A</span>
                  </td>
                  <td>
                    <div v-if="asistencia.latitud_salida && asistencia.longitud_salida" class="location-cell">
                      <div class="location-info">
                        <span class="location-badge compact"
                              :title="`Lat: ${asistencia.latitud_salida}, Lng: ${asistencia.longitud_salida}`">
                          {{ formatearCoordenadas(asistencia.latitud_salida, asistencia.longitud_salida) }}
                        </span>
                      </div>
                      <div class="location-actions">
                        <button @click="abrirMapaModal(asistencia, 'salida')" 
                                class="map-btn circular salida-map"
                                title="Ver ubicación de salida en el mapa">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                            <circle cx="12" cy="10" r="3"/>
                          </svg>
                        </button>
                      </div>
                    </div>
                    <span v-else class="no-data">N/A</span>
                  </td>
                  <td>
                    <div class="photos-cell">
                      <div class="photo-item" v-if="asistencia.foto_entrada_url">
                        <img 
                          :src="asistencia.foto_entrada_url" 
                          alt="Foto de entrada"
                          class="photo-thumbnail"
                          @click="abrirModal(asistencia.foto_entrada_url, 'Foto de entrada')"
                          @error="onImageError"
                          @load="onImageLoad"
                        >
                        <span class="photo-label">Entrada</span>
                      </div>
                      <div class="photo-item" v-if="asistencia.foto_salida_url">
                        <img 
                          :src="asistencia.foto_salida_url" 
                          alt="Foto de salida"
                          class="photo-thumbnail"
                          @click="abrirModal(asistencia.foto_salida_url, 'Foto de salida')"
                          @error="onImageError"
                          @load="onImageLoad"
                        >
                        <span class="photo-label">Salida</span>
                      </div>
                      <span v-if="!asistencia.foto_entrada_url && !asistencia.foto_salida_url" class="no-data">Sin fotos</span>
                    </div>
                  </td>
                  <td>
                    <div class="observations-cell">
                      <div v-if="asistencia.descripcion_entrada" class="observation-item">
                        <strong>Entrada:</strong> {{ asistencia.descripcion_entrada }}
                      </div>
                      <div v-if="asistencia.descripcion_salida" class="observation-item">
                        <strong>Salida:</strong> {{ asistencia.descripcion_salida }}
                      </div>
                      <span v-if="!asistencia.descripcion_entrada && !asistencia.descripcion_salida" class="no-data">Sin observaciones</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal para ver fotos en grande -->
    <div v-if="modalVisible" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ modalTitle }}</h3>
          <button @click="cerrarModal" class="modal-close">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <img :src="modalImage" :alt="modalTitle" class="modal-image">
        </div>
      </div>
    </div>

    <!-- Modal del mapa de asistencia -->
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
import AsistenciasService from '../services/asistenciasService.js'

export default {
  name: 'AsistenciaView',
  components: {
    Sidebar,
    MapaAsistenciaModal
  },
  data() {
    return {
      asistencias: [],
      asistenciasFiltradas: [],
      searchTerm: '',
      // Filtros antiguos
      filtroFecha: '',
      // Nuevos filtros avanzados
      filtroFechaInicio: '',
      filtroFechaFin: '',
      filtroRapido: '',
      filtroUsuario: '',
      filtroDepartamento: '',
      filtroEntrada: false,
      filtroSalida: false,
      filtroSinSalida: false,
      mostrarFiltrosAvanzados: false,
      // Estado UI
      loading: false,
      error: null,
      isOnline: navigator.onLine,
      modalVisible: false,
      modalImage: '',
      modalTitle: '',
      // Propiedades para el modal del mapa
      mapaModalVisible: false,
      asistenciaSeleccionada: null,
      tipoMapa: 'entrada' // 'entrada', 'salida', 'asistencia'
    }
  },
  computed: {
    totalAsistencias() {
      return this.asistencias.length
    },
    totalAsistenciasHoy() {
      const hoy = new Date().toISOString().split('T')[0]
      return this.asistencias.filter(a => a.fecha === hoy).length
    },
    usuariosPresentes() {
      const hoy = new Date().toISOString().split('T')[0]
      const usuariosHoy = new Set()
      this.asistencias.forEach(a => {
        if (a.fecha === hoy && a.hora_entrada) {
          usuariosHoy.add(a.usuario_id)
        }
      })
      return usuariosHoy.size
    },
    departamentos() {
      // Obtiene lista única de departamentos
      const departamentosSet = new Set()
      this.asistencias.forEach(a => {
        if (a.departamento) {
          departamentosSet.add(a.departamento)
        }
      })
      return [...departamentosSet].sort()
    },
    usuariosUnicos() {
      // Obtiene lista única de usuarios
      const usuariosMap = new Map()
      this.asistencias.forEach(a => {
        if (a.usuario_id && a.nombre_usuario) {
          usuariosMap.set(a.usuario_id, {
            id: a.usuario_id,
            nombre: a.nombre_usuario
          })
        }
      })
      return [...usuariosMap.values()]
    },
    hayFiltrosFechas() {
      return this.filtroFechaInicio || this.filtroFechaFin || this.filtroRapido
    },
    maxDate() {
      return new Date().toISOString().split('T')[0]
    },
    filtrosActivos() {
      const filtros = []
      
      if (this.searchTerm) {
        filtros.push({
          tipo: 'busqueda',
          valor: this.searchTerm,
          label: `Búsqueda: ${this.searchTerm}`
        })
      }
      
      if (this.filtroFechaInicio && this.filtroFechaFin) {
        filtros.push({
          tipo: 'fechaRango',
          valor: [this.filtroFechaInicio, this.filtroFechaFin],
          label: `Periodo: ${this.formatearFechaCorta(this.filtroFechaInicio)} - ${this.formatearFechaCorta(this.filtroFechaFin)}`
        })
      } else if (this.filtroRapido) {
        const etiquetas = {
          'hoy': 'Hoy',
          'ayer': 'Ayer',
          'semana': 'Esta semana',
          'mes': 'Este mes'
        }
        filtros.push({
          tipo: 'fechaRapida',
          valor: this.filtroRapido,
          label: `Periodo: ${etiquetas[this.filtroRapido]}`
        })
      }
      
      if (this.filtroDepartamento) {
        filtros.push({
          tipo: 'departamento',
          valor: this.filtroDepartamento,
          label: `Departamento: ${this.filtroDepartamento}`
        })
      }
      
      if (this.filtroUsuario) {
        const usuario = this.usuariosUnicos.find(u => u.id === this.filtroUsuario)
        filtros.push({
          tipo: 'usuario',
          valor: this.filtroUsuario,
          label: `Usuario: ${usuario ? usuario.nombre : this.filtroUsuario}`
        })
      }
      
      if (this.filtroEntrada) {
        filtros.push({
          tipo: 'entrada',
          valor: true,
          label: 'Con entrada'
        })
      }
      
      if (this.filtroSalida) {
        filtros.push({
          tipo: 'salida',
          valor: true,
          label: 'Con salida'
        })
      }
      
      if (this.filtroSinSalida) {
        filtros.push({
          tipo: 'sinSalida',
          valor: true,
          label: 'Sin salida'
        })
      }
      
      return filtros
    }
  },
  mounted() {
    this.cargarAsistencias()
    this.configurarEventosConexion()
  },
  methods: {
    async cargarAsistencias() {
      this.loading = true
      this.error = null
      
      try {
        this.asistencias = await AsistenciasService.obtenerAsistenciasConUsuarios()
        this.filtrarAsistencias()
        console.log('✅ Asistencias cargadas:', this.asistencias.length)
      } catch (error) {
        console.error('❌ Error al cargar asistencias:', error)
        this.error = 'Error al cargar las asistencias. Por favor, intenta de nuevo.'
      } finally {
        this.loading = false
      }
    },

    filtrarAsistencias() {
      let filtradas = [...this.asistencias]

      // Filtro por texto
      if (this.searchTerm) {
        const termino = this.searchTerm.toLowerCase()
        filtradas = filtradas.filter(asistencia => 
          (asistencia.nombre_usuario && asistencia.nombre_usuario.toLowerCase().includes(termino)) ||
          (asistencia.correo_usuario && asistencia.correo_usuario.toLowerCase().includes(termino)) ||
          (asistencia.departamento && asistencia.departamento.toLowerCase().includes(termino)) ||
          (asistencia.fecha && asistencia.fecha.includes(termino))
        )
      }

      // Filtro por usuario específico
      if (this.filtroUsuario) {
        filtradas = filtradas.filter(asistencia => 
          asistencia.usuario_id === this.filtroUsuario
        )
      }
      
      // Filtro por departamento
      if (this.filtroDepartamento) {
        filtradas = filtradas.filter(asistencia => 
          asistencia.departamento === this.filtroDepartamento
        )
      }
      
      // Filtro por estado de entrada/salida
      if (this.filtroEntrada) {
        filtradas = filtradas.filter(asistencia => asistencia.hora_entrada)
      }
      
      if (this.filtroSalida) {
        filtradas = filtradas.filter(asistencia => asistencia.hora_salida)
      }
      
      if (this.filtroSinSalida) {
        filtradas = filtradas.filter(asistencia => 
          asistencia.hora_entrada && !asistencia.hora_salida
        )
      }

      // Filtros por fechas rápidas
      if (this.filtroRapido) {
        const hoy = new Date()
        hoy.setHours(0, 0, 0, 0)
        
        switch (this.filtroRapido) {
          case 'hoy':
            const fechaHoy = hoy.toISOString().split('T')[0]
            filtradas = filtradas.filter(asistencia => asistencia.fecha === fechaHoy)
            break
          case 'ayer':
            const ayer = new Date(hoy)
            ayer.setDate(ayer.getDate() - 1)
            const fechaAyer = ayer.toISOString().split('T')[0]
            filtradas = filtradas.filter(asistencia => asistencia.fecha === fechaAyer)
            break
          case 'semana':
            const inicioSemana = new Date(hoy)
            inicioSemana.setDate(hoy.getDate() - hoy.getDay())
            filtradas = filtradas.filter(asistencia => {
              const fechaAsistencia = new Date(asistencia.fecha)
              return fechaAsistencia >= inicioSemana && fechaAsistencia <= hoy
            })
            break
          case 'mes':
            const inicioMes = new Date(hoy.getFullYear(), hoy.getMonth(), 1)
            filtradas = filtradas.filter(asistencia => {
              const fechaAsistencia = new Date(asistencia.fecha)
              return fechaAsistencia >= inicioMes && fechaAsistencia <= hoy
            })
            break
        }
      } 
      // Filtro por rango de fechas personalizado
      else if (this.filtroFechaInicio && this.filtroFechaFin) {
        const fechaInicio = new Date(this.filtroFechaInicio)
        fechaInicio.setHours(0, 0, 0, 0)
        
        const fechaFin = new Date(this.filtroFechaFin)
        fechaFin.setHours(23, 59, 59, 999)
        
        filtradas = filtradas.filter(asistencia => {
          const fechaAsistencia = new Date(asistencia.fecha)
          return fechaAsistencia >= fechaInicio && fechaAsistencia <= fechaFin
        })
      }

      this.asistenciasFiltradas = filtradas
    },

    formatearFecha(fecha) {
      return AsistenciasService.formatearFecha(fecha)
    },

    formatearHora(hora) {
      return AsistenciasService.formatearHora(hora)
    },

    formatearCoordenadas(lat, lng) {
      return AsistenciasService.formatearCoordenadas(lat, lng)
    },

    obtenerIniciales(nombre) {
      if (!nombre) return '??'
      return nombre.split(' ')
        .map(n => n.charAt(0))
        .join('')
        .toUpperCase()
        .substring(0, 2)
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

    configurarEventosConexion() {
      window.addEventListener('online', () => {
        this.isOnline = true
        this.cargarAsistencias()
      })
      
      window.addEventListener('offline', () => {
        this.isOnline = false
      })
    },

    onImageLoad(event) {
      console.log('✅ Imagen cargada correctamente:', event.target.src)
    },

    limpiarBusqueda() {
      this.searchTerm = ''
      this.filtrarAsistencias()
    },

    seleccionarFechaRapida(tipo) {
      this.filtroRapido = this.filtroRapido === tipo ? '' : tipo
      this.filtroFechaInicio = ''
      this.filtroFechaFin = ''
      this.filtrarAsistencias()
    },

    limpiarFiltrosFechas() {
      this.filtroFechaInicio = ''
      this.filtroFechaFin = ''
      this.filtroRapido = ''
      this.filtrarAsistencias()
    },

    quitarFiltro(tipo, valor) {
      switch (tipo) {
        case 'busqueda':
          this.searchTerm = ''
          break
        case 'fechaRango':
          this.filtroFechaInicio = ''
          this.filtroFechaFin = ''
          break
        case 'fechaRapida':
          this.filtroRapido = ''
          break
        case 'departamento':
          this.filtroDepartamento = ''
          break
        case 'usuario':
          this.filtroUsuario = ''
          break
        case 'entrada':
          this.filtroEntrada = false
          break
        case 'salida':
          this.filtroSalida = false
          break
        case 'sinSalida':
          this.filtroSinSalida = false
          break
      }
      this.filtrarAsistencias()
    },

    limpiarTodosFiltros() {
      this.searchTerm = ''
      this.filtroFechaInicio = ''
      this.filtroFechaFin = ''
      this.filtroRapido = ''
      this.filtroUsuario = ''
      this.filtroDepartamento = ''
      this.filtroEntrada = false
      this.filtroSalida = false
      this.filtroSinSalida = false
      this.filtrarAsistencias()
    },

    exportarAsistencias(tipo) {
      if (tipo === 'csv') {
        this.exportarCSV()
      } else if (tipo === 'excel') {
        this.exportarExcel()
      }
    },

    exportarCSV() {
      // Crear encabezados
      const encabezados = [
        'Usuario',
        'Email',
        'Departamento',
        'Fecha',
        'Hora Entrada',
        'Hora Salida',
        'Coordenadas Entrada',
        'Coordenadas Salida',
        'Observaciones Entrada',
        'Observaciones Salida'
      ].join(',')

      // Crear filas de datos
      const filas = this.asistenciasFiltradas.map(a => {
        const coordenadasEntrada = a.latitud_entrada && a.longitud_entrada 
          ? `"${a.latitud_entrada},${a.longitud_entrada}"`
          : '""'
        
        const coordenadasSalida = a.latitud_salida && a.longitud_salida 
          ? `"${a.latitud_salida},${a.longitud_salida}"`
          : '""'
        
        return [
          `"${a.nombre_usuario || ''}"`,
          `"${a.correo_usuario || ''}"`,
          `"${a.departamento || ''}"`,
          `"${a.fecha || ''}"`,
          `"${a.hora_entrada || ''}"`,
          `"${a.hora_salida || ''}"`,
          coordenadasEntrada,
          coordenadasSalida,
          `"${a.descripcion_entrada || ''}"`,
          `"${a.descripcion_salida || ''}"`
        ].join(',')
      })

      // Combinar encabezados y filas
      const contenidoCSV = [encabezados, ...filas].join('\n')
      
      // Crear y descargar el archivo
      const blob = new Blob([contenidoCSV], { type: 'text/csv;charset=utf-8;' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.setAttribute('href', url)
      link.setAttribute('download', `asistencias_${new Date().toISOString().split('T')[0]}.csv`)
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },

    exportarExcel() {
      alert('La exportación a Excel se implementará próximamente')
      // En una implementación real, se usaría una librería como SheetJS
    },

    imprimirAsistencias() {
      window.print()
    },

    formatearFechaCorta(fechaStr) {
      if (!fechaStr) return ''
      const fecha = new Date(fechaStr)
      return fecha.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' })
    },
  }
}
</script>

<style scoped>
/* ULTRA RESPONSIVE ASISTENCIA VIEW - Patrón de éxito de UsuariosView */
.asistencia-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.main-content {
  flex: 1;
  margin-left: clamp(180px, 18vw, 240px);
  transition: all 0.3s ease;
  width: calc(100vw - clamp(180px, 18vw, 240px));
  overflow-x: hidden;
}

/* HEADER ULTRA RESPONSIVE */
.page-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  padding: clamp(0.75rem, 2vw, 1.25rem);
  position: sticky;
  top: 0;
  z-index: 100;
  width: 100%;
  box-sizing: border-box;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 100%;
  margin: 0;
  gap: clamp(0.5rem, 2vw, 1rem);
  flex-wrap: wrap;
  width: 100%;
}

.header-main {
  display: flex;
  align-items: center;
  gap: clamp(0.5rem, 2vw, 1rem);
  flex: 1;
  min-width: 200px;
}

.header-icon {
  width: clamp(36px, 5vw, 48px);
  height: clamp(36px, 5vw, 48px);
  background: linear-gradient(135deg, #4CAF50, #45a049);
  border-radius: clamp(8px, 1.5vw, 12px);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 24px rgba(76, 175, 80, 0.25);
  flex-shrink: 0;
}

.header-icon svg {
  width: clamp(16px, 3vw, 24px);
  height: clamp(16px, 3vw, 24px);
  color: white;
}

.header-text h1 {
  margin: 0;
  font-size: clamp(1.1rem, 3vw, 1.5rem);
  font-weight: 700;
  color: #2d3748;
  background: linear-gradient(135deg, #4CAF50, #2196F3);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1.2;
}

.header-text p {
  margin: clamp(0.15rem, 0.5vw, 0.25rem) 0 0 0;
  color: #718096;
  font-size: clamp(0.7rem, 1.5vw, 0.85rem);
  line-height: 1.3;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: clamp(0.5rem, 1.5vw, 1rem);
  flex-wrap: wrap;
  justify-content: flex-end;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: clamp(0.25rem, 0.8vw, 0.35rem);
  padding: clamp(0.25rem, 0.8vw, 0.35rem) clamp(0.5rem, 1.5vw, 0.75rem);
  border-radius: clamp(12px, 2vw, 16px);
  font-size: clamp(0.65rem, 1.5vw, 0.75rem);
  font-weight: 500;
  white-space: nowrap;
}

.connection-status.online {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.connection-status.offline {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

.status-indicator {
  width: clamp(4px, 1vw, 6px);
  height: clamp(4px, 1vw, 6px);
  border-radius: 50%;
  background: currentColor;
  flex-shrink: 0;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: clamp(0.25rem, 0.8vw, 0.35rem);
  padding: clamp(0.4rem, 1vw, 0.5rem) clamp(0.75rem, 2vw, 1rem);
  background: linear-gradient(135deg, #4CAF50, #45a049);
  color: white;
  border: none;
  border-radius: clamp(6px, 1.5vw, 8px);
  font-weight: 500;
  font-size: clamp(0.65rem, 1.5vw, 0.75rem);
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 3px 12px rgba(76, 175, 80, 0.25);
  white-space: nowrap;
}

.refresh-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(76, 175, 80, 0.4);
}

.refresh-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* CONTENIDO ULTRA RESPONSIVE - APROVECHA TODO EL ANCHO */
.page-content {
  padding: clamp(1rem, 2vw, 1.5rem);
  max-width: 100%;
  margin: 0;
  width: 100%;
  box-sizing: border-box;
}

/* FILTROS AVANZADOS ULTRA RESPONSIVE */
.advanced-filters {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: clamp(8px, 2vw, 12px);
  padding: clamp(0.75rem, 2vw, 1rem);
  margin-bottom: clamp(1rem, 2vw, 1.25rem);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.08);
  width: 100%;
  box-sizing: border-box;
}

.filters-main {
  display: flex;
  flex-wrap: wrap;
  gap: clamp(0.5rem, 1.5vw, 0.65rem);
  margin-bottom: clamp(0.5rem, 1.5vw, 0.75rem);
  width: 100%;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: clamp(200px, 40vw, 300px);
  max-width: 100%;
}

.search-icon {
  position: absolute;
  left: clamp(0.75rem, 2vw, 1rem);
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  width: clamp(14px, 2vw, 16px);
  height: clamp(14px, 2vw, 16px);
}

.search-input {
  width: 100%;
  padding: clamp(0.5rem, 1.5vw, 0.65rem) clamp(0.75rem, 2vw, 1rem) clamp(0.5rem, 1.5vw, 0.65rem) clamp(2.5rem, 6vw, 3rem);
  border: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: clamp(6px, 1.5vw, 8px);
  background: rgba(255, 255, 255, 0.9);
  font-size: clamp(0.75rem, 1.8vw, 0.85rem);
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.search-input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
}

.clear-search-btn {
  position: absolute;
  right: clamp(0.75rem, 2vw, 1rem);
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: clamp(0.2rem, 0.5vw, 0.25rem);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  width: clamp(20px, 3vw, 24px);
  height: clamp(20px, 3vw, 24px);
}

.clear-search-btn:hover {
  background: rgba(0, 0, 0, 0.05);
  color: #4b5563;
}

.date-range-filter {
  display: flex;
  flex-wrap: wrap;
  gap: clamp(0.75rem, 2vw, 1rem);
  align-items: center;
  width: 100%;
}

.date-picker-container {
  display: flex;
  align-items: center;
  gap: clamp(0.4rem, 1vw, 0.5rem);
  flex-wrap: wrap;
}

.date-label {
  font-weight: 500;
  color: #4b5563;
  white-space: nowrap;
  font-size: clamp(0.7rem, 1.5vw, 0.85rem);
}

.date-input {
  padding: clamp(0.4rem, 1vw, 0.5rem) clamp(0.6rem, 1.5vw, 0.75rem);
  border: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: clamp(6px, 1.5vw, 8px);
  background: rgba(255, 255, 255, 0.9);
  font-size: clamp(0.7rem, 1.5vw, 0.8rem);
  transition: all 0.3s ease;
  min-width: clamp(120px, 20vw, 140px);
}

.date-input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
}

.quick-date-filters {
  display: flex;
  flex-wrap: wrap;
  gap: clamp(0.4rem, 1vw, 0.5rem);
  margin-left: auto;
}

.quick-date-btn {
  padding: clamp(0.3rem, 0.8vw, 0.35rem) clamp(0.6rem, 1.5vw, 0.75rem);
  background: rgba(0, 0, 0, 0.05);
  border: none;
  border-radius: clamp(4px, 1vw, 6px);
  font-size: clamp(0.7rem, 1.5vw, 0.8rem);
  font-weight: 500;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.quick-date-btn:hover {
  background: rgba(0, 0, 0, 0.1);
}

.quick-date-btn.active {
  background: #4CAF50;
  color: white;
}

.clear-date-btn {
  display: flex;
  align-items: center;
  gap: clamp(0.25rem, 0.8vw, 0.35rem);
  padding: clamp(0.3rem, 0.8vw, 0.35rem) clamp(0.6rem, 1.5vw, 0.75rem);
  background: rgba(244, 67, 54, 0.1);
  border: none;
  border-radius: clamp(4px, 1vw, 6px);
  font-size: clamp(0.7rem, 1.5vw, 0.8rem);
  font-weight: 500;
  color: #f44336;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.clear-date-btn:hover {
  background: rgba(244, 67, 54, 0.2);
}

.filters-advanced {
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  padding-top: clamp(0.6rem, 1.5vw, 0.8rem);
  margin-top: clamp(0.3rem, 0.8vw, 0.4rem);
}

.advanced-filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(clamp(180px, 25vw, 220px), 1fr));
  gap: clamp(0.75rem, 2vw, 1rem);
  margin-bottom: clamp(0.6rem, 1.5vw, 0.8rem);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: clamp(0.25rem, 0.6vw, 0.3rem);
}

.filter-label {
  font-weight: 600;
  color: #4b5563;
  margin-bottom: clamp(0.1rem, 0.3vw, 0.15rem);
  font-size: clamp(0.7rem, 1.5vw, 0.8rem);
}

.filter-options {
  display: flex;
  flex-wrap: wrap;
  gap: clamp(0.5rem, 1.3vw, 0.65rem);
}

.checkbox-option {
  display: flex;
  align-items: center;
  gap: clamp(0.25rem, 0.8vw, 0.35rem);
  cursor: pointer;
  user-select: none;
  font-size: clamp(0.7rem, 1.5vw, 0.8rem);
}

.checkbox-option input[type="checkbox"] {
  width: clamp(12px, 2vw, 14px);
  height: clamp(12px, 2vw, 14px);
  accent-color: #4CAF50;
  cursor: pointer;
}

.filter-select {
  padding: clamp(0.35rem, 0.9vw, 0.45rem) clamp(0.6rem, 1.5vw, 0.75rem);
  border: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: clamp(6px, 1.5vw, 8px);
  background: rgba(255, 255, 255, 0.9);
  font-size: clamp(0.7rem, 1.5vw, 0.8rem);
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  box-sizing: border-box;
}

.filter-select:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
}

.advanced-actions {
  display: flex;
  flex-wrap: wrap;
  gap: clamp(0.75rem, 2vw, 1rem);
  justify-content: flex-end;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: clamp(0.25rem, 0.8vw, 0.35rem);
  padding: clamp(0.35rem, 0.9vw, 0.45rem) clamp(0.6rem, 1.5vw, 0.8rem);
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
  border: none;
  border-radius: clamp(4px, 1vw, 6px);
  font-weight: 500;
  font-size: clamp(0.65rem, 1.3vw, 0.75rem);
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.export-btn:hover {
  background: rgba(33, 150, 243, 0.2);
}

.export-btn.excel {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
}

.export-btn.excel:hover {
  background: rgba(76, 175, 80, 0.2);
}

.export-btn.print {
  background: rgba(156, 39, 176, 0.1);
  color: #9C27B0;
}

.export-btn.print:hover {
  background: rgba(156, 39, 176, 0.2);
}

.toggle-filters-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(0.25rem, 0.8vw, 0.35rem);
  width: 100%;
  padding: clamp(0.3rem, 0.8vw, 0.4rem);
  background: rgba(0, 0, 0, 0.02);
  border: none;
  border-radius: clamp(4px, 1vw, 6px);
  font-size: clamp(0.65rem, 1.3vw, 0.75rem);
  font-weight: 500;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: clamp(0.25rem, 0.8vw, 0.35rem);
}

.toggle-filters-btn:hover {
  background: rgba(0, 0, 0, 0.05);
}

.toggle-filters-btn svg {
  transition: transform 0.3s ease;
  width: clamp(12px, 2vw, 16px);
  height: clamp(12px, 2vw, 16px);
}

.active-filters {
  display: flex;
  flex-direction: column;
  gap: clamp(0.4rem, 1vw, 0.5rem);
  margin-top: clamp(0.6rem, 1.5vw, 0.8rem);
  padding-top: clamp(0.6rem, 1.5vw, 0.8rem);
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.active-filters-label {
  font-weight: 600;
  color: #4b5563;
  font-size: clamp(0.65rem, 1.3vw, 0.75rem);
}

.active-filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: clamp(0.25rem, 0.8vw, 0.35rem);
}

.filter-tag {
  display: flex;
  align-items: center;
  gap: clamp(0.25rem, 0.8vw, 0.35rem);
  padding: clamp(0.2rem, 0.5vw, 0.25rem) clamp(0.5rem, 1.2vw, 0.6rem);
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
  border-radius: clamp(8px, 1.5vw, 12px);
  font-size: clamp(0.65rem, 1.3vw, 0.75rem);
  font-weight: 500;
}

.remove-filter {
  background: none;
  border: none;
  cursor: pointer;
  padding: clamp(0.1rem, 0.3vw, 0.15rem);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4CAF50;
  transition: all 0.2s ease;
  width: clamp(16px, 2.5vw, 20px);
  height: clamp(16px, 2.5vw, 20px);
}

.remove-filter:hover {
  background: rgba(76, 175, 80, 0.2);
}

.remove-filter svg {
  width: clamp(8px, 1.5vw, 12px);
  height: clamp(8px, 1.5vw, 12px);
}

.clear-all-filters {
  padding: clamp(0.2rem, 0.5vw, 0.25rem) clamp(0.5rem, 1.2vw, 0.6rem);
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
  border: none;
  border-radius: clamp(8px, 1.5vw, 12px);
  font-size: clamp(0.65rem, 1.3vw, 0.75rem);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.clear-all-filters:hover {
  background: rgba(244, 67, 54, 0.2);
}

/* ESTADISTICAS ULTRA RESPONSIVE */
.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(clamp(180px, 25vw, 200px), 1fr));
  gap: clamp(0.75rem, 2vw, 1rem);
  margin-bottom: clamp(1rem, 2vw, 1.25rem);
  width: 100%;
}

.stat-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: clamp(8px, 2vw, 12px);
  padding: clamp(0.65rem, 1.5vw, 0.85rem);
  display: flex;
  align-items: center;
  gap: clamp(0.6rem, 1.5vw, 0.75rem);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  width: clamp(32px, 5vw, 38px);
  height: clamp(32px, 5vw, 38px);
  background: linear-gradient(135deg, #4CAF50, #45a049);
  border-radius: clamp(8px, 1.5vw, 10px);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg {
  width: clamp(14px, 2.5vw, 18px);
  height: clamp(14px, 2.5vw, 18px);
  color: white;
}

.stat-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
  flex: 1;
}

.stat-number {
  font-size: clamp(1.2rem, 3vw, 1.5rem);
  font-weight: 700;
  color: #2d3748;
  line-height: 1;
}

.stat-label {
  font-size: clamp(0.65rem, 1.5vw, 0.75rem);
  color: #718096;
  margin-top: clamp(0.1rem, 0.3vw, 0.15rem);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* TABLA ULTRA RESPONSIVE - APROVECHA TODO EL ANCHO DISPONIBLE */
.asistencias-section {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: clamp(12px, 2vw, 16px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  width: 100%;
  margin: 0;
}

.table-container {
  overflow-x: hidden !important; /* CRITICAL: Sin scroll horizontal */
  overflow-y: auto;
  width: 100%;
  margin: 0;
  padding: 0;
}

.asistencias-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed; /* CRITICAL: Layout fijo para control total */
  font-size: clamp(0.65rem, 1.3vw, 0.875rem);
  margin: 0;
}

/* DISTRIBUCIÓN DE COLUMNAS OPTIMIZADA PARA MÁXIMO ANCHO */
.asistencias-table th:nth-child(1), 
.asistencias-table td:nth-child(1) { width: 16%; } /* Usuario - más espacio */
.asistencias-table th:nth-child(2), 
.asistencias-table td:nth-child(2) { width: 14%; } /* Correo - más espacio */
.asistencias-table th:nth-child(3), 
.asistencias-table td:nth-child(3) { width: 10%; } /* Fecha */
.asistencias-table th:nth-child(4), 
.asistencias-table td:nth-child(4) { width: 8%; }  /* Entrada */
.asistencias-table th:nth-child(5), 
.asistencias-table td:nth-child(5) { width: 8%; }  /* Salida */
.asistencias-table th:nth-child(6), 
.asistencias-table td:nth-child(6) { width: 13%; } /* Ubicación Entrada - más espacio */
.asistencias-table th:nth-child(7), 
.asistencias-table td:nth-child(7) { width: 13%; } /* Ubicación Salida - más espacio */
.asistencias-table th:nth-child(8), 
.asistencias-table td:nth-child(8) { width: 9%; }  /* Fotos - más espacio */
.asistencias-table th:nth-child(9), 
.asistencias-table td:nth-child(9) { width: 9%; }  /* Observaciones - más espacio */

.asistencias-table th {
  background: linear-gradient(135deg, #f8fafc, #e2e8f0);
  padding: clamp(0.75rem, 1.5vw, 1rem);
  text-align: center;
  font-weight: 600;
  color: #4a5568;
  border-bottom: 2px solid #e2e8f0;
  font-size: clamp(0.6rem, 1.3vw, 0.8rem);
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.asistencias-table td {
  padding: clamp(0.5rem, 1vw, 0.75rem);
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
  text-align: center;
  overflow: hidden;
  word-wrap: break-word;
  hyphens: auto;
}

.asistencias-table tr:hover {
  background: rgba(76, 175, 80, 0.05);
}

/* ESTILOS ESPECÍFICOS DE CELDAS - ULTRA RESPONSIVE */
.user-info {
  display: flex;
  align-items: center;
  gap: clamp(0.4rem, 1vw, 0.6rem);
  justify-content: center;
  text-align: center;
}

.user-avatar {
  width: clamp(28px, 4vw, 36px);
  height: clamp(28px, 4vw, 36px);
  background: linear-gradient(135deg, #4CAF50, #45a049);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: clamp(0.6rem, 1.5vw, 0.75rem);
  flex-shrink: 0;
}

.user-details {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  min-width: 0;
  flex: 1;
}

.user-name {
  font-weight: 600;
  color: #2d3748;
  font-size: clamp(0.65rem, 1.3vw, 0.8rem);
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  width: 100%;
}

.user-cargo {
  font-size: clamp(0.55rem, 1.1vw, 0.65rem);
  color: #718096;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  width: 100%;
}

.date-badge {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
  padding: clamp(0.2rem, 0.5vw, 0.25rem) clamp(0.5rem, 1vw, 0.75rem);
  border-radius: clamp(12px, 2vw, 20px);
  font-weight: 500;
  font-size: clamp(0.6rem, 1.2vw, 0.75rem);
  white-space: nowrap;
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}

.time-badge {
  padding: clamp(0.2rem, 0.5vw, 0.25rem) clamp(0.5rem, 1vw, 0.75rem);
  border-radius: clamp(12px, 2vw, 20px);
  font-weight: 500;
  font-size: clamp(0.6rem, 1.2vw, 0.75rem);
  white-space: nowrap;
  display: inline-block;
  min-width: clamp(50px, 10vw, 60px);
  text-align: center;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}

.time-badge.entrada {
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
}

.time-badge.salida {
  background: rgba(255, 152, 0, 0.1);
  color: #FF9800;
}

/* Estilos específicos para columnas de hora */
.asistencias-table th:nth-child(4),
.asistencias-table th:nth-child(5),
.asistencias-table td:nth-child(4),
.asistencias-table td:nth-child(5) {
  min-width: 100px;
  white-space: nowrap;
  text-align: center;
}

/* Estilos específicos para columnas de ubicación */
.asistencias-table th:nth-child(6),
.asistencias-table th:nth-child(7),
.asistencias-table td:nth-child(6),
.asistencias-table td:nth-child(7) {
  min-width: 180px;
  max-width: 220px;
  padding: 0.75rem;
}

/* UBICACIONES ULTRA RESPONSIVE */
.location-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: clamp(0.4rem, 1vw, 0.5rem);
  text-align: center;
  min-height: clamp(40px, 6vw, 44px);
  padding: clamp(0.3rem, 0.8vw, 0.5rem);
}

.location-info {
  width: 100%;
  min-width: 0;
}

.location-actions {
  display: flex;
  justify-content: center;
  width: 100%;
}

.location-badge {
  background: rgba(156, 39, 176, 0.1);
  color: #9C27B0;
  padding: clamp(0.15rem, 0.4vw, 0.2rem) clamp(0.3rem, 0.8vw, 0.4rem);
  border-radius: clamp(8px, 1.5vw, 12px);
  font-size: clamp(0.55rem, 1.1vw, 0.65rem);
  font-family: monospace;
  cursor: help;
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  word-break: break-all;
  line-height: 1.2;
  text-align: center;
}

.location-badge.compact {
  font-size: clamp(0.5rem, 1vw, 0.6rem);
  padding: clamp(0.1rem, 0.3vw, 0.15rem) clamp(0.25rem, 0.6vw, 0.3rem);
}

/* BOTONES DE MAPA ULTRA RESPONSIVE */
.map-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
}

.map-btn.circular {
  width: clamp(28px, 4vw, 32px);
  height: clamp(28px, 4vw, 32px);
  border-radius: 50%;
  animation: subtlePulse 4s ease-in-out infinite;
}

@keyframes subtlePulse {
  0%, 100% {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }
  50% {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15), 0 0 0 3px rgba(76, 175, 80, 0.1);
  }
}

.map-btn.salida-map.circular {
  animation: subtlePulseSalida 4s ease-in-out infinite;
}

@keyframes subtlePulseSalida {
  0%, 100% {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }
  50% {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15), 0 0 0 3px rgba(244, 67, 54, 0.1);
  }
}

.map-btn svg {
  width: clamp(12px, 2.5vw, 16px);
  height: clamp(12px, 2.5vw, 16px);
  color: white;
  position: relative;
  z-index: 2;
}

.map-btn.entrada-map {
  background: linear-gradient(135deg, #4CAF50, #45a049);
}

.map-btn.entrada-map:hover {
  background: linear-gradient(135deg, #45a049, #388e3c);
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.map-btn.salida-map {
  background: linear-gradient(135deg, #f44336, #d32f2f);
}

.map-btn.salida-map:hover {
  background: linear-gradient(135deg, #d32f2f, #c62828);
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 6px 20px rgba(244, 67, 54, 0.4);
}

.map-btn:active {
  transform: translateY(0) scale(0.95);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* FOTOS Y OBSERVACIONES ULTRA RESPONSIVE */
.photos-cell {
  display: flex;
  flex-direction: column;
  gap: clamp(0.3rem, 0.8vw, 0.4rem);
  align-items: center;
  justify-content: center;
  text-align: center;
}

.photo-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(0.3rem, 0.8vw, 0.4rem);
  flex-direction: column;
}

.photo-thumbnail {
  width: clamp(28px, 4vw, 36px);
  height: clamp(28px, 4vw, 36px);
  object-fit: cover;
  border-radius: clamp(6px, 1.5vw, 8px);
  cursor: pointer;
  transition: transform 0.2s ease;
  border: 2px solid #e2e8f0;
  flex-shrink: 0;
}

.photo-thumbnail:hover {
  transform: scale(1.1);
  border-color: #4CAF50;
}

.photo-label {
  font-size: clamp(0.55rem, 1.1vw, 0.65rem);
  color: #718096;
  white-space: nowrap;
}

.observations-cell {
  text-align: center;
  max-width: 100%;
  word-wrap: break-word;
  hyphens: auto;
}

.observation-item {
  margin-bottom: clamp(0.3rem, 0.8vw, 0.4rem);
  font-size: clamp(0.6rem, 1.2vw, 0.7rem);
  line-height: 1.3;
  word-break: break-word;
}

.observation-item:last-child {
  margin-bottom: 0;
}

.observation-item strong {
  display: block;
  margin-bottom: clamp(0.1rem, 0.3vw, 0.15rem);
  font-size: clamp(0.55rem, 1.1vw, 0.65rem);
  color: #4CAF50;
}

.no-data {
  color: #a0aec0;
  font-style: italic;
  font-size: clamp(0.6rem, 1.2vw, 0.7rem);
  text-align: center;
}

/* ESTADOS Y MODAL ULTRA RESPONSIVE */
.loading-container, .error-container, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: clamp(3rem, 8vw, 4rem) clamp(1rem, 3vw, 2rem);
  text-align: center;
}

.spinner-large {
  width: clamp(36px, 6vw, 48px);
  height: clamp(36px, 6vw, 48px);
  border: 4px solid #e2e8f0;
  border-top: 4px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: clamp(0.75rem, 2vw, 1rem);
}

.empty-icon {
  margin-bottom: clamp(0.75rem, 2vw, 1rem);
  opacity: 0.6;
}

.empty-state h3 {
  font-size: clamp(1.1rem, 2.5vw, 1.3rem);
  color: #2d3748;
  margin-bottom: clamp(0.5rem, 1.5vw, 0.75rem);
}

.empty-state p {
  font-size: clamp(0.85rem, 1.8vw, 1rem);
  color: #718096;
  line-height: 1.5;
}

.retry-btn {
  display: flex;
  align-items: center;
  gap: clamp(0.4rem, 1vw, 0.5rem);
  padding: clamp(0.6rem, 1.5vw, 0.75rem) clamp(1.2rem, 3vw, 1.5rem);
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: clamp(6px, 1.5vw, 8px);
  cursor: pointer;
  margin-top: clamp(0.75rem, 2vw, 1rem);
  transition: background 0.3s ease;
  font-size: clamp(0.8rem, 1.8vw, 0.9rem);
}

.retry-btn:hover {
  background: #45a049;
}

/* MODAL ULTRA RESPONSIVE */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: clamp(1rem, 3vw, 2rem);
}

.modal-content {
  background: white;
  border-radius: clamp(12px, 2vw, 16px);
  max-width: 90vw;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: clamp(400px, 80vw, 600px);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: clamp(1rem, 3vw, 1.5rem);
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  margin: 0;
  color: #2d3748;
  font-size: clamp(1rem, 2.5vw, 1.2rem);
}

.modal-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: clamp(0.4rem, 1vw, 0.5rem);
  border-radius: clamp(6px, 1.5vw, 8px);
  transition: background 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close:hover {
  background: #f7fafc;
}

.modal-close svg {
  width: clamp(18px, 3vw, 24px);
  height: clamp(18px, 3vw, 24px);
}

.modal-body {
  padding: clamp(1rem, 3vw, 1.5rem);
  text-align: center;
}

.modal-image {
  max-width: 100%;
  max-height: clamp(300px, 60vh, 500px);
  object-fit: contain;
  border-radius: clamp(6px, 1.5vw, 8px);
}

/* ULTRA RESPONSIVE MÓVIL - ELIMINACIÓN TOTAL DE SCROLL HORIZONTAL */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    width: 100vw;
    overflow-x: hidden !important;
  }
  
  .header-content {
    flex-direction: column;
    gap: clamp(0.75rem, 2vw, 1rem);
    align-items: stretch;
    text-align: center;
  }
  
  .header-main {
    justify-content: center;
  }
  
  .header-actions {
    justify-content: center;
    gap: clamp(0.5rem, 2vw, 1rem);
  }
  
  .search-box {
    min-width: 100%;
  }
  
  .date-range-filter {
    flex-direction: column;
    align-items: stretch;
    gap: clamp(0.5rem, 1.5vw, 1rem);
  }
  
  .date-picker-container {
    justify-content: center;
  }
  
  .quick-date-filters {
    margin-left: 0;
    justify-content: center;
  }
  
  .stats-section {
    grid-template-columns: 1fr;
    gap: clamp(0.75rem, 2vw, 1rem);
  }
  
  .table-container {
    border-radius: 0;
    overflow-x: hidden !important;
  }
  
  .asistencias-table {
    font-size: clamp(0.6rem, 1.8vw, 0.75rem);
  }
  
  .asistencias-table th,
  .asistencias-table td {
    padding: clamp(0.4rem, 1.2vw, 0.6rem);
  }

  /* TABLA MÓVIL - DISTRIBUCIÓN OPTIMIZADA PARA TODO EL ANCHO */
  .asistencias-table th:nth-child(1), 
  .asistencias-table td:nth-child(1) { width: 20%; } /* Usuario - máximo espacio */
  .asistencias-table th:nth-child(2), 
  .asistencias-table td:nth-child(2) { width: 16%; } /* Correo - más espacio */
  .asistencias-table th:nth-child(3), 
  .asistencias-table td:nth-child(3) { width: 12%; } /* Fecha */
  .asistencias-table th:nth-child(4), 
  .asistencias-table td:nth-child(4) { width: 9%; }  /* Entrada */
  .asistencias-table th:nth-child(5), 
  .asistencias-table td:nth-child(5) { width: 9%; }  /* Salida */
  .asistencias-table th:nth-child(6), 
  .asistencias-table td:nth-child(6) { width: 11%; } /* Ubicación Entrada */
  .asistencias-table th:nth-child(7), 
  .asistencias-table td:nth-child(7) { width: 11%; } /* Ubicación Salida */
  .asistencias-table th:nth-child(8), 
  .asistencias-table td:nth-child(8) { width: 6%; }  /* Fotos - compacto */
  .asistencias-table th:nth-child(9), 
  .asistencias-table td:nth-child(9) { width: 6%; }  /* Observaciones - compacto */

  .user-info {
    flex-direction: column;
    gap: clamp(0.3rem, 1vw, 0.5rem);
  }

  .location-cell {
    gap: clamp(0.25rem, 0.8vw, 0.4rem);
  }

  .location-badge.compact {
    font-size: clamp(0.45rem, 1.2vw, 0.55rem);
    padding: clamp(0.1rem, 0.3vw, 0.15rem) clamp(0.2rem, 0.6vw, 0.25rem);
  }

  .map-btn.circular {
    width: clamp(24px, 6vw, 28px);
    height: clamp(24px, 6vw, 28px);
  }

  .map-btn svg {
    width: clamp(10px, 2.5vw, 12px);
    height: clamp(10px, 2.5vw, 12px);
  }

  .photo-thumbnail {
    width: clamp(24px, 6vw, 28px);
    height: clamp(24px, 6vw, 28px);
  }

  .time-badge {
    min-width: clamp(40px, 8vw, 50px);
    padding: clamp(0.15rem, 0.4vw, 0.2rem) clamp(0.4rem, 1vw, 0.5rem);
  }

  /* FILTROS MÓVIL */
  .advanced-filters-grid {
    grid-template-columns: 1fr;
    gap: clamp(0.75rem, 2vw, 1rem);
  }

  .filter-options {
    justify-content: center;
  }

  .advanced-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .export-btn {
    justify-content: center;
  }
}

/* EXTRA PEQUEÑO - ULTRA COMPACTO */
@media (max-width: 480px) {
  .asistencias-table {
    font-size: clamp(0.55rem, 2vw, 0.65rem);
  }
  
  .asistencias-table th,
  .asistencias-table td {
    padding: clamp(0.3rem, 1vw, 0.5rem);
  }

  .user-name {
    font-size: clamp(0.6rem, 1.8vw, 0.7rem);
  }

  .user-cargo {
    font-size: clamp(0.5rem, 1.5vw, 0.6rem);
  }
  
  /* TABLA EXTRA COMPACTA - USA TODO EL ANCHO DISPONIBLE */
  .asistencias-table th:nth-child(1), 
  .asistencias-table td:nth-child(1) { width: 22%; } /* Usuario - máximo espacio en pantalla pequeña */
  .asistencias-table th:nth-child(2), 
  .asistencias-table td:nth-child(2) { width: 18%; } /* Correo - más espacio */
  .asistencias-table th:nth-child(3), 
  .asistencias-table td:nth-child(3) { width: 12%; } /* Fecha */
  .asistencias-table th:nth-child(4), 
  .asistencias-table td:nth-child(4) { width: 9%; }  /* Entrada */
  .asistencias-table th:nth-child(5), 
  .asistencias-table td:nth-child(5) { width: 9%; }  /* Salida */
  .asistencias-table th:nth-child(6), 
  .asistencias-table td:nth-child(6) { width: 10%; } /* Ubicación Entrada */
  .asistencias-table th:nth-child(7), 
  .asistencias-table td:nth-child(7) { width: 10%; } /* Ubicación Salida */
  .asistencias-table th:nth-child(8), 
  .asistencias-table td:nth-child(8) { width: 5%; }  /* Fotos - muy compacto */
  .asistencias-table th:nth-child(9), 
  .asistencias-table td:nth-child(9) { width: 5%; }  /* Observaciones - muy compacto */
}
</style>
