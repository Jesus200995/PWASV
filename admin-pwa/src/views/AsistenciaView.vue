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
              <svg v-if="!buscandoUsuario" class="apple-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="11" cy="11" r="8" stroke-width="2.5"/>
                <path d="m21 21-4.35-4.35" stroke-width="2.5" stroke-linecap="round"/>
              </svg>
              <div v-else class="apple-search-loading">
                <div class="apple-search-spinner"></div>
              </div>
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

          <!-- ================== FILTROS COMBINADOS: FECHA + TIPO ================== -->
          <div class="apple-filters-row">
            <!-- Filtros de fecha -->
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

            <!-- Separador visual -->
            <div class="apple-filters-divider"></div>

            <!-- Filtros de tipo con contadores -->
            <div class="apple-type-filters-inline">
              <button 
                @click="seleccionarTipo('todas')" 
                :class="['apple-type-chip', { 'active': filtroTipo === 'todas' }]"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M4 6h16M4 12h16M4 18h16" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <span>Todas ({{ conteoTipos.todas }})</span>
              </button>
              
              <button 
                @click="seleccionarTipo('entradas')" 
                :class="['apple-type-chip', { 'active': filtroTipo === 'entradas' }]"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <polyline points="10 17 15 12 10 7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <line x1="15" y1="12" x2="3" y2="12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Pendientes ({{ conteoTipos.soloEntradas }})</span>
              </button>
              
              <button 
                @click="seleccionarTipo('salidas')" 
                :class="['apple-type-chip', { 'active': filtroTipo === 'salidas' }]"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <polyline points="16 17 21 12 16 7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <line x1="21" y1="12" x2="9" y2="12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Con Salida ({{ conteoTipos.conSalidas }})</span>
              </button>
              
              <button 
                @click="seleccionarTipo('completas')" 
                :class="['apple-type-chip', { 'active': filtroTipo === 'completas' }]"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <polyline points="22 4 12 14.01 9 11.01" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Completas ({{ conteoTipos.completas }})</span>
              </button>
            </div>
          </div>
        </div>
        </div>
      </div>  <!-- Close apple-sticky-wrapper -->

      <div class="apple-content-wrapper">
        <!-- ================== TABLE APPLE STYLE ================== -->
        <div class="apple-table-container">
          <!-- Indicador de búsqueda en backend -->
          <div v-if="buscandoUsuario" class="apple-searching">
            <div class="apple-spinner"></div>
            <p>Buscando en base de datos...</p>
          </div>

          <div v-else-if="loading && asistencias.length === 0" class="apple-loading">
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
            <!-- Indicador de resultados -->
            <div v-if="searchTerm && searchTerm.length >= 3" class="apple-results-indicator">
              <span class="apple-results-badge">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" width="14" height="14">
                  <circle cx="11" cy="11" r="8" stroke-width="2"/>
                  <path d="m21 21-4.35-4.35" stroke-width="2" stroke-linecap="round"/>
                </svg>
                {{ asistenciasFiltradas.length }} resultado{{ asistenciasFiltradas.length !== 1 ? 's' : '' }} encontrado{{ asistenciasFiltradas.length !== 1 ? 's' : '' }}
                <button @click="limpiarBusqueda" class="apple-clear-search-btn">Ver todos</button>
              </span>
            </div>
            
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
                  <th class="col-acciones">Acciones</th>
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
                  <!-- COLUMNA ACCIONES -->
                  <td class="col-acciones">
                    <div class="apple-actions-cell">
                      <button
                        @click="abrirModalEditar(asistencia)"
                        class="apple-action-btn edit"
                        title="Editar asistencia"
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                        </svg>
                      </button>
                      <button
                        @click="abrirModalEliminar(asistencia)"
                        class="apple-action-btn delete"
                        title="Eliminar asistencia"
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <polyline points="3 6 5 6 21 6"/>
                          <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
                          <path d="M10 11v6M14 11v6"/>
                          <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
                        </svg>
                      </button>
                    </div>
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

    <!-- ================== MODAL EDITAR ASISTENCIA ================== -->
    <Teleport to="body">
      <Transition name="apple-modal-fade">
        <div v-if="modalEditarVisible" class="apple-modal-overlay" @click.self="cerrarModalEditar">
          <div class="apple-edit-modal" @click.stop>
            <!-- Header del modal -->
            <div class="apple-edit-modal-header">
              <div class="apple-edit-modal-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
              </div>
              <div class="apple-edit-modal-title-group">
                <h2 class="apple-edit-modal-title">Editar Asistencia</h2>
                <p class="apple-edit-modal-subtitle">{{ editandoAsistencia?.nombre_usuario }}</p>
              </div>
              <button @click="cerrarModalEditar" class="apple-edit-modal-close">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>

            <!-- Body del modal -->
            <div class="apple-edit-modal-body">
              <!-- Fecha -->
              <div class="apple-edit-field">
                <label class="apple-edit-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                    <line x1="16" y1="2" x2="16" y2="6"/>
                    <line x1="8" y1="2" x2="8" y2="6"/>
                    <line x1="3" y1="10" x2="21" y2="10"/>
                  </svg>
                  Fecha
                </label>
                <input
                  type="date"
                  v-model="editForm.fecha"
                  class="apple-edit-input"
                >
              </div>

              <!-- Hora Entrada -->
              <div class="apple-edit-field">
                <label class="apple-edit-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 6v6l4 2" stroke-linecap="round"/>
                  </svg>
                  Hora de Entrada
                </label>
                <input
                  type="time"
                  v-model="editForm.hora_entrada"
                  class="apple-edit-input"
                >
              </div>

              <!-- Hora Salida -->
              <div class="apple-edit-field">
                <label class="apple-edit-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 6v6l4 2" stroke-linecap="round"/>
                  </svg>
                  Hora de Salida
                </label>
                <input
                  type="time"
                  v-model="editForm.hora_salida"
                  class="apple-edit-input"
                  :disabled="!editandoAsistencia || !editandoAsistencia.hora_salida"
                  :class="{ 'apple-edit-input--disabled': !editandoAsistencia || !editandoAsistencia.hora_salida }"
                >
                <p v-if="!editandoAsistencia || !editandoAsistencia.hora_salida" class="apple-edit-field-note">
                  El usuario aún no ha registrado su salida
                </p>
              </div>

              <!-- Descripción Entrada -->
              <div class="apple-edit-field">
                <label class="apple-edit-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  Descripción de Entrada
                </label>
                <textarea
                  v-model="editForm.descripcion_entrada"
                  class="apple-edit-textarea"
                  rows="2"
                  placeholder="Sin descripción..."
                ></textarea>
              </div>

              <!-- Descripción Salida -->
              <div class="apple-edit-field">
                <label class="apple-edit-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  Descripción de Salida
                </label>
                <textarea
                  v-model="editForm.descripcion_salida"
                  class="apple-edit-textarea"
                  rows="2"
                  placeholder="Sin descripción..."
                  :disabled="!editandoAsistencia || !editandoAsistencia.hora_salida"
                  :class="{ 'apple-edit-input--disabled': !editandoAsistencia || !editandoAsistencia.hora_salida }"
                ></textarea>
                <p v-if="!editandoAsistencia || !editandoAsistencia.hora_salida" class="apple-edit-field-note">
                  El usuario aún no ha registrado su salida
                </p>
              </div>

              <!-- Error -->
              <div v-if="editError" class="apple-edit-error">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="8" x2="12" y2="12" stroke-linecap="round"/>
                  <line x1="12" y1="16" x2="12.01" y2="16" stroke-linecap="round"/>
                </svg>
                {{ editError }}
              </div>
            </div>

            <!-- Footer del modal -->
            <div class="apple-edit-modal-footer">
              <button @click="cerrarModalEditar" class="apple-edit-btn cancel">
                Cancelar
              </button>
              <button @click="guardarEdicion" class="apple-edit-btn save" :disabled="guardandoEdicion">
                <svg v-if="guardandoEdicion" class="apple-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="16" height="16">
                  <path d="M21 12a9 9 0 1 1-6.219-8.56" stroke-linecap="round"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="16" height="16">
                  <polyline points="20 6 9 17 4 12" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                {{ guardandoEdicion ? 'Guardando...' : 'Guardar cambios' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ================== MODAL CONFIRMAR ELIMINAR ================== -->
    <Teleport to="body">
      <Transition name="apple-modal-fade">
        <div v-if="modalEliminarVisible" class="apple-modal-overlay" @click.self="cerrarModalEliminar">
          <div class="apple-delete-modal" @click.stop>
            <!-- Icono de advertencia -->
            <div class="apple-delete-modal-icon-wrap">
              <div class="apple-delete-modal-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="3 6 5 6 21 6"/>
                  <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
                  <path d="M10 11v6M14 11v6"/>
                  <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
                </svg>
              </div>
            </div>

            <h2 class="apple-delete-modal-title">Eliminar Asistencia</h2>
            <p class="apple-delete-modal-desc">
              ¿Estás seguro de que deseas eliminar la asistencia de
              <strong>{{ eliminandoAsistencia?.nombre_usuario }}</strong>
              del <strong>{{ eliminandoAsistencia ? formatearFecha(eliminandoAsistencia.fecha) : '' }}</strong>?
            </p>
            <p class="apple-delete-modal-warning">Esta acción no se puede deshacer.</p>

            <div v-if="deleteError" class="apple-edit-error" style="margin-bottom:16px">
              {{ deleteError }}
            </div>

            <div class="apple-delete-modal-footer">
              <button @click="cerrarModalEliminar" class="apple-edit-btn cancel">
                Cancelar
              </button>
              <button @click="confirmarEliminar" class="apple-edit-btn danger" :disabled="eliminando">
                <svg v-if="eliminando" class="apple-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="16" height="16">
                  <path d="M21 12a9 9 0 1 1-6.219-8.56" stroke-linecap="round"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="16" height="16">
                  <polyline points="3 6 5 6 21 6" stroke-linecap="round"/>
                  <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                {{ eliminando ? 'Eliminando...' : 'Sí, eliminar' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

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
      asistenciasOriginales: [], // Respaldo para restaurar al limpiar búsqueda
      searchTerm: '',
      filtroRapido: '',
      paginaActual: 1,
      asistenciasPorPagina: 50,
      totalAsistenciasServidor: 0,
      buscandoUsuario: false,
      busquedaTimeout: null,
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
      dropdownPosition: { top: 0, left: 0, width: 0 },
      // Modal Editar Asistencia
      modalEditarVisible: false,
      editandoAsistencia: null,
      editForm: {
        fecha: '',
        hora_entrada: '',
        hora_salida: '',
        descripcion_entrada: '',
        descripcion_salida: ''
      },
      guardandoEdicion: false,
      editError: null,
      // Modal Eliminar Asistencia
      modalEliminarVisible: false,
      eliminandoAsistencia: null,
      eliminando: false,
      deleteError: null
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
    // Contadores de tipos de asistencia
    conteoTipos() {
      const todas = this.asistencias.length
      const soloEntradas = this.asistencias.filter(a => a.hora_entrada && !a.hora_salida).length
      const conSalidas = this.asistencias.filter(a => a.hora_salida).length
      const completas = this.asistencias.filter(a => a.hora_entrada && a.hora_salida).length
      return { todas, soloEntradas, conSalidas, completas }
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
        this.asistenciasOriginales = [...asistencias] // Guardar copia original
        this.hayMasRegistros = asistencias.length === this.registrosCargados
        this.filtrarAsistencias()
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
        const asistencias = await AsistenciasService.obtenerAsistenciasConUsuarios(this.registrosCargados)
        
        this.asistencias = asistencias
        this.hayMasRegistros = asistencias.length === this.registrosCargados
        this.filtrarAsistencias()
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
            filtradas = filtradas.filter(a => a.hora_entrada && !a.hora_salida)
            break
          case 'salidas':
            filtradas = filtradas.filter(a => a.hora_salida)
            break
          case 'completas':
            filtradas = filtradas.filter(a => a.hora_entrada && a.hora_salida)
            break
        }
      }

      // ========== FILTRO POR FECHA (solo aplica si no se cargó desde backend) ==========
      // Los filtros de fecha ahora cargan directamente del backend via seleccionarFechaRapida()
      // Este filtro local es solo backup/fallback

      this.asistenciasFiltradas = filtradas
      this.paginaActual = 1
    },
    
    async seleccionarFechaRapida(tipo) {
      // Toggle del filtro
      if (this.filtroRapido === tipo) {
        this.filtroRapido = ''
        // Restaurar datos originales
        if (this.asistenciasOriginales.length > 0) {
          this.asistencias = [...this.asistenciasOriginales]
        }
        this.filtrarAsistencias()
        return
      }
      
      this.filtroRapido = tipo
      this.buscandoUsuario = true
      
      try {
        const hoy = new Date()
        hoy.setHours(0, 0, 0, 0)
        
        let fechaParam = ''
        let fechaInicioParam = ''
        let fechaFinParam = ''
        
        switch (tipo) {
          case 'hoy':
            fechaParam = hoy.toISOString().split('T')[0]
            break
          case 'ayer':
            const ayer = new Date(hoy)
            ayer.setDate(ayer.getDate() - 1)
            fechaParam = ayer.toISOString().split('T')[0]
            break
          case 'semana':
            const inicioSemana = new Date(hoy)
            inicioSemana.setDate(hoy.getDate() - hoy.getDay())
            fechaInicioParam = inicioSemana.toISOString().split('T')[0]
            fechaFinParam = hoy.toISOString().split('T')[0]
            break
          case 'mes':
            const inicioMes = new Date(hoy.getFullYear(), hoy.getMonth(), 1)
            fechaInicioParam = inicioMes.toISOString().split('T')[0]
            fechaFinParam = hoy.toISOString().split('T')[0]
            break
        }
        
        // Construir URL con parámetros de fecha
        let url = `${API_URL}/asistencias?`
        if (fechaParam) {
          url += `fecha=${fechaParam}`
        } else if (fechaInicioParam && fechaFinParam) {
          url += `fecha_inicio=${fechaInicioParam}&fecha_fin=${fechaFinParam}`
        }
        
        const response = await fetch(url, {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('admin_token')}` }
        })
        
        if (response.ok) {
          const data = await response.json()
          const asistenciasRaw = data.asistencias || []
          
          // Cargar usuarios para enriquecer datos
          const usuarios = await this.obtenerUsuariosCache()
          const usuariosMap = new Map(usuarios.map(u => [u.id, u]))
          
          // Función helper para construir URL de foto
          const construirUrlFoto = (rutaFoto) => {
            if (!rutaFoto) return null
            if (rutaFoto.startsWith('http://') || rutaFoto.startsWith('https://')) {
              return rutaFoto
            }
            let rutaLimpia = rutaFoto
            if (!rutaLimpia.startsWith('fotos/')) {
              if (!rutaLimpia.includes('/')) {
                rutaLimpia = `fotos/${rutaLimpia}`
              }
            }
            return `${API_URL}/${rutaLimpia}`
          }
          
          // Enriquecer asistencias
          const asistenciasEnriquecidas = asistenciasRaw.map(a => {
            const usuario = usuariosMap.get(a.usuario_id)
            return {
              ...a,
              nombre_usuario: usuario?.nombre_completo || 'Usuario no encontrado',
              correo_usuario: usuario?.correo || 'N/A',
              cargo_usuario: usuario?.cargo || 'N/A',
              curp_usuario: usuario?.curp || null,
              foto_entrada_url: construirUrlFoto(a.foto_entrada_url),
              foto_salida_url: construirUrlFoto(a.foto_salida_url)
            }
          })
          
          this.asistencias = asistenciasEnriquecidas
          this.filtrarAsistencias()
        }
      } catch (error) {
        console.error('Error cargando por fecha:', error)
        // Fallback a filtro local
        this.filtrarAsistencias()
      } finally {
        this.buscandoUsuario = false
      }
    },
    
    async obtenerUsuariosCache() {
      // Intentar del caché del servicio o cargar
      try {
        const response = await fetch(`${API_URL}/usuarios`, {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('admin_token')}` }
        })
        if (response.ok) {
          const data = await response.json()
          return data.usuarios || []
        }
      } catch (e) {
        console.warn('Error cargando usuarios:', e)
      }
      return []
    },
    
    limpiarBusqueda() {
      this.searchTerm = ''
      this.filtroRapido = ''
      // Restaurar asistencias originales si hay respaldo
      if (this.asistenciasOriginales.length > 0) {
        this.asistencias = [...this.asistenciasOriginales]
      }
      this.filtrarAsistencias()
    },
    
    limpiarFiltros() {
      this.searchTerm = ''
      this.filtroRapido = ''
      this.filtroTipo = 'todas'
      this.mostrarDropdown = false
      // Restaurar asistencias originales si hay respaldo
      if (this.asistenciasOriginales.length > 0) {
        this.asistencias = [...this.asistenciasOriginales]
      }
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
      
      // Limpiar timeout anterior
      if (this.busquedaTimeout) {
        clearTimeout(this.busquedaTimeout)
      }
      
      const termino = this.searchTerm?.trim() || ''
      
      // SIEMPRE hacer filtro local INMEDIATO para respuesta instantánea
      this.filtrarAsistencias()
      
      // Si el término tiene 3+ caracteres, buscar en backend con debounce RÁPIDO
      if (termino.length >= 3) {
        this.busquedaTimeout = setTimeout(async () => {
          await this.buscarUsuarioEnBackend(termino)
        }, 300) // Solo 300ms de espera
      } else if (termino.length === 0) {
        // Si se borra la búsqueda, restaurar asistencias originales
        if (this.asistenciasOriginales.length > 0) {
          this.asistencias = [...this.asistenciasOriginales]
          this.filtroRapido = '' // Limpiar filtro de fecha también
          this.filtrarAsistencias()
        }
      }
    },
    
    async buscarUsuarioEnBackend(termino) {
      if (!termino || termino.length < 3) return
      
      this.buscandoUsuario = true
      
      try {
        const token = localStorage.getItem('admin_token')
        const terminoLimpio = termino.trim()
        
        // Buscar usuarios que coincidan con el término
        const response = await fetch(`${API_URL}/api/buscar-usuarios?nombre=${encodeURIComponent(terminoLimpio)}&correo=${encodeURIComponent(terminoLimpio)}&curp=${encodeURIComponent(terminoLimpio)}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        
        if (!response.ok) {
          throw new Error(`Error ${response.status}`)
        }
        
        const data = await response.json()
        const usuariosEncontrados = data.usuarios || []
        
        if (usuariosEncontrados.length === 0) {
          this.asistencias = []
          this.filtrarAsistencias()
          return
        }
        
        // Función helper para construir URL de foto
        const construirUrlFoto = (rutaFoto) => {
          if (!rutaFoto) return null
          if (rutaFoto.startsWith('http://') || rutaFoto.startsWith('https://')) {
            return rutaFoto
          }
          let rutaLimpia = rutaFoto
          if (!rutaLimpia.startsWith('fotos/')) {
            if (!rutaLimpia.includes('/')) {
              rutaLimpia = `fotos/${rutaLimpia}`
            }
          }
          return `${API_URL}/${rutaLimpia}`
        }
        
        // Cargar asistencias en PARALELO para mayor velocidad
        const promesas = usuariosEncontrados.map(async (usuario) => {
          if (usuario.id) {
            const asistResponse = await fetch(`${API_URL}/asistencias?usuario_id=${usuario.id}`, {
              headers: { 'Authorization': `Bearer ${token}` }
            })
            
            if (asistResponse.ok) {
              const asistData = await asistResponse.json()
              return (asistData.asistencias || []).map(a => ({
                ...a,
                nombre_usuario: usuario.nombre_completo || 'N/A',
                correo_usuario: usuario.correo || 'N/A',
                cargo_usuario: usuario.cargo || 'N/A',
                curp_usuario: usuario.curp || null,
                foto_entrada_url: construirUrlFoto(a.foto_entrada_url),
                foto_salida_url: construirUrlFoto(a.foto_salida_url)
              }))
            }
          }
          return []
        })
        
        // Esperar todas las promesas en paralelo
        const resultados = await Promise.all(promesas)
        const todasAsistencias = resultados.flat()
        
        // Ordenar por fecha descendente
        todasAsistencias.sort((a, b) => new Date(b.fecha) - new Date(a.fecha))
        
        this.asistencias = todasAsistencias
        this.filtrarAsistencias()
        
      } catch (error) {
        console.error('Error en búsqueda:', error)
        this.filtrarAsistencias()
      } finally {
        this.buscandoUsuario = false
      }
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

    // ============ EDITAR ASISTENCIA ============
    abrirModalEditar(asistencia) {
      this.editandoAsistencia = asistencia
      this.editError = null

      // Extraer solo la parte de tiempo HH:MM:SS de las horas
      const extraerHora = (horaStr) => {
        if (!horaStr) return ''
        // Si viene como timestamp completo, extraer la parte de tiempo
        if (horaStr.includes('T')) {
          return horaStr.split('T')[1].substring(0, 5)
        }
        // Si viene como HH:MM:SS, tomar solo HH:MM
        return horaStr.substring(0, 5)
      }

      this.editForm = {
        fecha: asistencia.fecha || '',
        hora_entrada: extraerHora(asistencia.hora_entrada),
        hora_salida: extraerHora(asistencia.hora_salida),
        descripcion_entrada: asistencia.descripcion_entrada || '',
        descripcion_salida: asistencia.descripcion_salida || ''
      }
      this.modalEditarVisible = true
      document.body.style.overflow = 'hidden'
    },

    cerrarModalEditar() {
      this.modalEditarVisible = false
      this.editandoAsistencia = null
      this.editError = null
      document.body.style.overflow = 'auto'
    },

    async guardarEdicion() {
      if (!this.editandoAsistencia) return
      this.guardandoEdicion = true
      this.editError = null

      try {
        const token = localStorage.getItem('admin_token')

        // Construir el cuerpo con solo los campos con valor
        const body = {}
        if (this.editForm.fecha) body.fecha = this.editForm.fecha
        // Normalizar hora a HH:MM para evitar formato inválido HH:MM:SS:00
        const normHora = (h) => h ? h.substring(0, 5) : null
        const fecha = this.editForm.fecha || this.editandoAsistencia.fecha
        if (this.editForm.hora_entrada) {
          body.hora_entrada = `${fecha}T${normHora(this.editForm.hora_entrada)}:00`
        } else {
          body.hora_entrada = null
        }
        if (this.editForm.hora_salida && this.editandoAsistencia.hora_salida) {
          body.hora_salida = `${fecha}T${normHora(this.editForm.hora_salida)}:00`
        } else {
          body.hora_salida = null
        }
        body.descripcion_entrada = this.editForm.descripcion_entrada || null
        body.descripcion_salida = this.editForm.descripcion_salida || null

        const response = await fetch(`${API_URL}/admin/asistencias/${this.editandoAsistencia.id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(body)
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.detail || 'Error al guardar')
        }

        // Actualizar la asistencia localmente
        const idx = this.asistencias.findIndex(a => a.id === this.editandoAsistencia.id)
        if (idx !== -1) {
          this.asistencias[idx] = {
            ...this.asistencias[idx],
            fecha: this.editForm.fecha || this.asistencias[idx].fecha,
            hora_entrada: this.editForm.hora_entrada
              ? `${this.editForm.fecha}T${this.editForm.hora_entrada.substring(0,5)}:00`
              : null,
            hora_salida: (this.editForm.hora_salida && this.editandoAsistencia.hora_salida)
              ? `${this.editForm.fecha}T${this.editForm.hora_salida.substring(0,5)}:00`
              : null,
            descripcion_entrada: this.editForm.descripcion_entrada || null,
            descripcion_salida: this.editForm.descripcion_salida || null
          }
          // Actualizar también en filtradas
          const idxF = this.asistenciasFiltradas.findIndex(a => a.id === this.editandoAsistencia.id)
          if (idxF !== -1) {
            this.asistenciasFiltradas[idxF] = { ...this.asistencias[idx] }
          }
        }

        this.cerrarModalEditar()
      } catch (err) {
        this.editError = err.message || 'Error al guardar los cambios'
      } finally {
        this.guardandoEdicion = false
      }
    },

    // ============ ELIMINAR ASISTENCIA ============
    abrirModalEliminar(asistencia) {
      this.eliminandoAsistencia = asistencia
      this.deleteError = null
      this.modalEliminarVisible = true
      document.body.style.overflow = 'hidden'
    },

    cerrarModalEliminar() {
      this.modalEliminarVisible = false
      this.eliminandoAsistencia = null
      this.deleteError = null
      document.body.style.overflow = 'auto'
    },

    async confirmarEliminar() {
      if (!this.eliminandoAsistencia) return
      this.eliminando = true
      this.deleteError = null

      try {
        const token = localStorage.getItem('admin_token')

        const response = await fetch(`${API_URL}/admin/asistencias/${this.eliminandoAsistencia.id}`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${token}` }
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.detail || 'Error al eliminar')
        }

        // Eliminar localmente de ambos arrays
        const id = this.eliminandoAsistencia.id
        this.asistencias = this.asistencias.filter(a => a.id !== id)
        this.asistenciasFiltradas = this.asistenciasFiltradas.filter(a => a.id !== id)
        this.asistenciasOriginales = this.asistenciasOriginales.filter(a => a.id !== id)

        // Ajustar página si queda vacía
        if (this.asistenciasPaginadas.length === 0 && this.paginaActual > 1) {
          this.paginaActual--
        }

        this.cerrarModalEliminar()
      } catch (err) {
        this.deleteError = err.message || 'Error al eliminar la asistencia'
      } finally {
        this.eliminando = false
      }
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

/* Loading spinner para búsqueda */
.apple-search-loading {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  z-index: 1;
}

.apple-search-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(0, 122, 255, 0.2);
  border-top-color: #007AFF;
  border-radius: 50%;
  animation: search-spin 0.8s linear infinite;
}

@keyframes search-spin {
  to { transform: rotate(360deg); }
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

/* ==================== FILA COMBINADA DE FILTROS ==================== */
.apple-filters-row {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.apple-filters-divider {
  width: 1px;
  height: 24px;
  background: rgba(0, 0, 0, 0.12);
  flex-shrink: 0;
}

.apple-type-filters-inline {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* Para mantener compatibilidad con estilos existentes */
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

/* Indicador de resultados de búsqueda */
.apple-results-indicator {
  padding: 12px 20px;
  background: linear-gradient(135deg, rgba(0, 122, 255, 0.04) 0%, rgba(52, 199, 89, 0.04) 100%);
  border-bottom: 1px solid rgba(0, 122, 255, 0.08);
}

.apple-results-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: white;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  color: #007AFF;
  box-shadow: 0 2px 8px rgba(0, 122, 255, 0.12);
}

.apple-results-badge svg {
  stroke: #007AFF;
}

.apple-clear-search-btn {
  margin-left: 8px;
  padding: 4px 10px;
  background: #007AFF;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.apple-clear-search-btn:hover {
  background: #0051D5;
  transform: scale(1.05);
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
.apple-empty,
.apple-searching {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 40px;
  text-align: center;
}

.apple-searching {
  background: linear-gradient(135deg, rgba(0, 122, 255, 0.03) 0%, rgba(52, 199, 89, 0.03) 100%);
}

.apple-searching p {
  color: #007AFF;
  font-weight: 600;
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
  
  /* Filtros combinados responsivos */
  .apple-filters-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    padding-top: 8px;
  }
  
  .apple-filters-divider {
    display: none;
  }
  
  .apple-quick-filters,
  .apple-type-filters-inline {
    width: 100%;
  }
  
  .apple-type-filters {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .apple-type-buttons {
    width: 100%;
  }
  
  .apple-filter-chip,
  .apple-type-chip {
    padding: 6px 10px;
    font-size: 11px;
    flex: 1;
    justify-content: center;
  }
  
  .apple-filter-chip svg,
  .apple-type-chip svg {
    width: 12px;
    height: 12px;
  }
}

/* ==================== ACTIONS COLUMN ==================== */
.col-acciones {
  width: 90px;
  text-align: center;
}

.apple-actions-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

/* Botón base de acción */
.apple-action-btn {
  width: 34px;
  height: 34px;
  border: none;
  border-radius: 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.18s cubic-bezier(0.34, 1.56, 0.64, 1),
              box-shadow 0.18s ease,
              background 0.18s ease;
  position: relative;
  overflow: hidden;
}

.apple-action-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(255,255,255,0.15);
  opacity: 0;
  transition: opacity 0.15s;
  border-radius: inherit;
}
.apple-action-btn:hover::before { opacity: 1; }

.apple-action-btn svg {
  width: 15px;
  height: 15px;
  flex-shrink: 0;
}

/* Editar — azul */
.apple-action-btn.edit {
  background: linear-gradient(145deg, #3b82f6, #2563eb);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.35);
  color: #fff;
}
.apple-action-btn.edit svg { stroke: #fff; }
.apple-action-btn.edit:hover {
  transform: translateY(-2px) scale(1.08);
  box-shadow: 0 6px 18px rgba(59, 130, 246, 0.5);
  background: linear-gradient(145deg, #60a5fa, #3b82f6);
}
.apple-action-btn.edit:active { transform: scale(0.95); }

/* Eliminar — rojo */
.apple-action-btn.delete {
  background: linear-gradient(145deg, #f87171, #dc2626);
  box-shadow: 0 2px 8px rgba(220, 38, 38, 0.3);
  color: #fff;
}
.apple-action-btn.delete svg { stroke: #fff; }
.apple-action-btn.delete:hover {
  transform: translateY(-2px) scale(1.08);
  box-shadow: 0 6px 18px rgba(220, 38, 38, 0.5);
  background: linear-gradient(145deg, #fca5a5, #ef4444);
}
.apple-action-btn.delete:active { transform: scale(0.95); }

/* ==================== MODAL BASE COMPARTIDO ==================== */
.apple-edit-modal,
.apple-delete-modal {
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(40px) saturate(180%);
  -webkit-backdrop-filter: blur(40px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.7);
  border-radius: 28px;
  box-shadow:
    0 32px 80px rgba(0, 0, 0, 0.18),
    0 8px 24px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
  width: 100%;
  max-width: 480px;
  margin: 16px;
  overflow: hidden;
  animation: apple-modal-pop 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes apple-modal-pop {
  from { opacity: 0; transform: scale(0.88) translateY(20px); }
  to   { opacity: 1; transform: scale(1) translateY(0); }
}

/* Header del modal editar */
.apple-edit-modal-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 22px 24px 18px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.apple-edit-modal-icon {
  width: 44px;
  height: 44px;
  background: linear-gradient(145deg, #3b82f6, #2563eb);
  border-radius: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4);
}
.apple-edit-modal-icon svg {
  width: 22px; height: 22px; stroke: #fff;
}

.apple-edit-modal-title-group { flex: 1; }
.apple-edit-modal-title {
  font-size: 17px;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0 0 2px;
  letter-spacing: -0.3px;
}
.apple-edit-modal-subtitle {
  font-size: 12px;
  color: #6b7280;
  margin: 0;
  font-weight: 500;
}

.apple-edit-modal-close {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 50%;
  background: rgba(0,0,0,0.06);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s, transform 0.15s;
  flex-shrink: 0;
}
.apple-edit-modal-close:hover {
  background: rgba(0,0,0,0.12);
  transform: scale(1.08);
}
.apple-edit-modal-close svg {
  width: 14px; height: 14px; stroke: #374151;
}

/* Body formulario */
.apple-edit-modal-body {
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  max-height: 60vh;
  overflow-y: auto;
}

.apple-edit-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.apple-edit-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}
.apple-edit-label svg {
  width: 13px; height: 13px; stroke: #6b7280; flex-shrink: 0;
}

.apple-edit-input,
.apple-edit-textarea {
  width: 100%;
  padding: 10px 14px;
  border: 1.5px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  font-size: 14px;
  font-family: inherit;
  color: #1a1a2e;
  background: rgba(255,255,255,0.8);
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
  box-sizing: border-box;
}
.apple-edit-input:focus,
.apple-edit-textarea:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
  background: #fff;
}
.apple-edit-textarea { resize: vertical; min-height: 56px; }

.apple-edit-input--disabled,
.apple-edit-input:disabled {
  background: rgba(0,0,0,0.05);
  color: #9ca3af;
  cursor: not-allowed;
  border-color: rgba(0,0,0,0.06);
}
.apple-edit-field-note {
  margin: 4px 0 0;
  font-size: 12px;
  color: #9ca3af;
  font-style: italic;
}

.apple-edit-error {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(220, 38, 38, 0.08);
  border: 1px solid rgba(220, 38, 38, 0.2);
  border-radius: 10px;
  padding: 10px 14px;
  font-size: 13px;
  color: #dc2626;
  font-weight: 500;
}
.apple-edit-error svg { width: 15px; height: 15px; stroke: #dc2626; flex-shrink: 0; }

/* Footer del modal */
.apple-edit-modal-footer,
.apple-delete-modal-footer {
  display: flex;
  gap: 10px;
  padding: 16px 24px 22px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  justify-content: flex-end;
}

.apple-edit-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 10px 20px;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: transform 0.18s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.18s, background 0.15s, opacity 0.15s;
}
.apple-edit-btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
  transform: none !important;
}

.apple-edit-btn.cancel {
  background: rgba(0, 0, 0, 0.06);
  color: #374151;
}
.apple-edit-btn.cancel:hover:not(:disabled) {
  background: rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.apple-edit-btn.save {
  background: linear-gradient(145deg, #3b82f6, #2563eb);
  color: #fff;
  box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4);
}
.apple-edit-btn.save:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.5);
}

.apple-edit-btn.danger {
  background: linear-gradient(145deg, #f87171, #dc2626);
  color: #fff;
  box-shadow: 0 4px 14px rgba(220, 38, 38, 0.35);
}
.apple-edit-btn.danger:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(220, 38, 38, 0.5);
}

/* ==================== MODAL ELIMINAR ==================== */
.apple-delete-modal {
  max-width: 400px;
  text-align: center;
  padding: 32px 28px 24px;
}

.apple-delete-modal-icon-wrap {
  display: flex;
  justify-content: center;
  margin-bottom: 18px;
}

.apple-delete-modal-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(145deg, #fecaca, #fee2e2);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 20px rgba(220, 38, 38, 0.2);
}
.apple-delete-modal-icon svg {
  width: 28px; height: 28px; stroke: #dc2626;
}

.apple-delete-modal-title {
  font-size: 20px;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0 0 10px;
  letter-spacing: -0.4px;
}
.apple-delete-modal-desc {
  font-size: 14px;
  color: #4b5563;
  margin: 0 0 6px;
  line-height: 1.6;
}
.apple-delete-modal-warning {
  font-size: 12px;
  color: #dc2626;
  font-weight: 600;
  margin: 0 0 20px;
}
.apple-delete-modal-footer {
  border: none;
  padding: 0;
  justify-content: center;
}

@media (max-width: 540px) {
  .apple-edit-modal,
  .apple-delete-modal {
    border-radius: 20px;
    margin: 12px;
  }
  .apple-edit-modal-header { padding: 18px 18px 14px; }
  .apple-edit-modal-body { padding: 16px 18px; }
  .apple-edit-modal-footer { padding: 14px 18px 18px; }
  .apple-delete-modal { padding: 24px 20px 20px; }
  .col-acciones { width: 76px; }
  .apple-action-btn { width: 30px; height: 30px; border-radius: 8px; }
  .apple-action-btn svg { width: 13px; height: 13px; }
  .apple-actions-cell { gap: 4px; }
}
</style>
