<template>
  <div class="reportes-container">
    <!-- Apple Dynamic Background -->
    <div class="apple-dynamic-bg">
      <div class="apple-orb apple-orb-1"></div>
      <div class="apple-orb apple-orb-2"></div>
      <div class="apple-orb apple-orb-3"></div>
    </div>
    
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <!-- ================== STICKY WRAPPER FOR HEADER + STATS ================== -->
      <div class="apple-sticky-wrapper">
        <!-- ================== HEADER APPLE STYLE ================== -->
        <header class="apple-page-header">
          <div class="apple-header-wrapper">
            <div class="apple-header-center">
              <div class="apple-title-group">
                <div class="apple-icon-mini">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <line x1="18" y1="20" x2="18" y2="10" stroke-width="2" stroke-linecap="round"/>
                    <line x1="12" y1="20" x2="12" y2="4" stroke-width="2" stroke-linecap="round"/>
                    <line x1="6" y1="20" x2="6" y2="14" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </div>
                <span class="apple-title-divider">|</span>
                <h1 class="apple-page-title">REPORTES</h1>
              </div>
              <p class="apple-page-subtitle">Firma y gestiona los reportes de los usuarios</p>
            </div>
            
            <button @click="cargarReportes" class="apple-refresh-button" :disabled="loading">
              <svg :class="{ 'apple-spin': loading }" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </header>

        <!-- ================== STATS + FILTERS SECTION ================== -->
        <div class="apple-stats-section">
          <!-- Stats Cards Apple Style -->
          <div class="apple-stats-grid">
            <div class="apple-stat-card">
              <div class="apple-stat-icon blue">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                </svg>
              </div>
              <div class="apple-stat-content">
                <div class="apple-stat-value">{{ estadisticas.totalReportes }}</div>
                <div class="apple-stat-label">Total</div>
              </div>
            </div>

            <div class="apple-stat-card">
              <div class="apple-stat-icon green">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" stroke-width="2"/>
                  <polyline points="22 4 12 14.01 9 11.01" stroke-width="2"/>
                </svg>
              </div>
              <div class="apple-stat-content">
                <div class="apple-stat-value">{{ reportesFirmados.length }}</div>
                <div class="apple-stat-label">Firmados</div>
              </div>
            </div>

            <div class="apple-stat-card">
              <div class="apple-stat-icon orange">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="12" cy="12" r="10" stroke-width="2"/>
                  <polyline points="12 6 12 12 16 14" stroke-width="2"/>
                </svg>
              </div>
              <div class="apple-stat-content">
                <div class="apple-stat-value">{{ reportesPendientes.length }}</div>
                <div class="apple-stat-label">Pendientes</div>
              </div>
            </div>

            <div class="apple-stat-card">
              <div class="apple-stat-icon purple">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke-width="2"/>
                  <circle cx="9" cy="7" r="4" stroke-width="2"/>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87" stroke-width="2"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75" stroke-width="2"/>
                </svg>
              </div>
              <div class="apple-stat-content">
                <div class="apple-stat-value">{{ estadisticas.usuariosConReportes }}</div>
                <div class="apple-stat-label">Usuarios</div>
              </div>
            </div>
          </div>

          <!-- ================== SEARCH & FILTERS ================== -->
          <div class="apple-search-section">
            <div class="apple-search-row">
              <div class="apple-search-container">
                <svg class="apple-search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="11" cy="11" r="8" stroke-width="2.5"/>
                  <path d="m21 21-4.35-4.35" stroke-width="2.5" stroke-linecap="round"/>
                </svg>
                <input 
                  v-model="filtros.busqueda" 
                  type="text" 
                  placeholder="Buscar por nombre, correo, CURP o territorio..." 
                  class="apple-search-input"
                >
                <button v-if="filtros.busqueda" @click="limpiarBusquedaReportes" class="apple-clear-btn">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10" stroke-width="2"/>
                    <line x1="15" y1="9" x2="9" y2="15" stroke-width="2" stroke-linecap="round"/>
                    <line x1="9" y1="9" x2="15" y2="15" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </button>
              </div>

              <div class="apple-filter-controls">
                <button 
                  v-if="reportesPendientesFiltrados.length > 0" 
                  @click="seleccionarTodosPendientes" 
                  class="apple-filter-btn primary"
                  title="Seleccionar todos los pendientes"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M9 11l3 3L22 4" stroke-width="2" stroke-linecap="round"/>
                    <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" stroke-width="2"/>
                  </svg>
                  <span>Seleccionar Pendientes ({{ reportesPendientesFiltrados.length }})</span>
                </button>
                <button 
                  @click="abrirModalDescarga" 
                  class="apple-filter-btn export"
                  title="Descargar reportes en ZIP"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span>Descargar</span>
                </button>
              </div>
            </div>

            <!-- Unified Filter Row -->
            <div class="apple-unified-filters">
              <div class="apple-quick-filters">
                <button 
                  @click="filtros.estadoFirma = ''" 
                  :class="['apple-filter-chip', { 'active': filtros.estadoFirma === '' }]"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke-width="2"/>
                    <polyline points="14 2 14 8 20 8" stroke-width="2"/>
                  </svg>
                  <span>Todos</span>
                </button>
                <button 
                  @click="filtros.estadoFirma = 'firmado'" 
                  :class="['apple-filter-chip', { 'active': filtros.estadoFirma === 'firmado' }]"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" stroke-width="2"/>
                    <polyline points="22 4 12 14.01 9 11.01" stroke-width="2"/>
                  </svg>
                  <span>Firmados</span>
                </button>
                <button 
                  @click="filtros.estadoFirma = 'pendiente'" 
                  :class="['apple-filter-chip', { 'active': filtros.estadoFirma === 'pendiente' }]"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10" stroke-width="2"/>
                    <polyline points="12 6 12 12 16 14" stroke-width="2"/>
                  </svg>
                  <span>Pendientes</span>
                </button>
              </div>

              <div class="apple-filter-group">
                <label class="apple-filter-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <rect x="3" y="4" width="18" height="18" rx="2" stroke-width="2"/>
                    <line x1="16" y1="2" x2="16" y2="6" stroke-width="2"/>
                    <line x1="8" y1="2" x2="8" y2="6" stroke-width="2"/>
                    <line x1="3" y1="10" x2="21" y2="10" stroke-width="2"/>
                  </svg>
                  Mes:
                </label>
                <select v-model="filtros.mes" @change="cargarReportes" class="apple-select">
                  <option value="">Todos</option>
                  <option v-for="mes in meses" :key="mes.value" :value="mes.value">{{ mes.label }}</option>
                </select>
              </div>

              <div class="apple-filter-group">
                <label class="apple-filter-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <rect x="3" y="4" width="18" height="18" rx="2" stroke-width="2"/>
                    <line x1="16" y1="2" x2="16" y2="6" stroke-width="2"/>
                    <line x1="8" y1="2" x2="8" y2="6" stroke-width="2"/>
                  </svg>
                  Año:
                </label>
                <select v-model="filtros.anio" @change="cargarReportes" class="apple-select">
                  <option value="">Todos</option>
                  <option v-for="anio in anios" :key="anio" :value="anio">{{ anio }}</option>
                </select>
              </div>

              <div v-if="!territorioUsuario" class="apple-filter-group">
                <label class="apple-filter-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" stroke-width="2"/>
                    <circle cx="12" cy="10" r="3" stroke-width="2"/>
                  </svg>
                  Territorio:
                </label>
                <select v-model="filtros.territorio" @change="cargarReportes" class="apple-select">
                  <option value="">Todos</option>
                  <option v-for="territorio in territorios" :key="territorio" :value="territorio">{{ territorio }}</option>
                </select>
              </div>

              <button @click="limpiarFiltros" class="apple-clear-filters-btn" title="Limpiar filtros">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M3 6h18M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <span>Limpiar</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- ================== CONTENT WRAPPER ================== -->
      <div class="apple-content-wrapper">
        <!-- Título del territorio (solo para admins territoriales) -->
        <div v-if="territorioUsuario" class="apple-territorio-banner">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" stroke-width="2"/>
            <circle cx="12" cy="10" r="3" stroke-width="2"/>
          </svg>
          <span>Reportes de {{ territorioUsuario }}</span>
        </div>

        <!-- Barra de acciones para firma masiva Apple Style -->
        <transition name="apple-slide">
          <div v-if="reportesSeleccionados.length > 0" class="apple-firma-bar">
            <div class="apple-firma-info">
              <div class="apple-firma-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M9 12l2 2 4-4" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <rect x="3" y="3" width="18" height="18" rx="3" stroke-width="2"/>
                </svg>
              </div>
              <span><strong>{{ reportesSeleccionados.length }}</strong> reportes seleccionados</span>
            </div>
            <div class="apple-firma-actions">
              <button @click="deseleccionarTodos" class="apple-btn-deselect">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <line x1="18" y1="6" x2="6" y2="18" stroke-width="2" stroke-linecap="round"/>
                  <line x1="6" y1="6" x2="18" y2="18" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <span>Deseleccionar</span>
              </button>
              <button @click="abrirModalFirma" class="apple-btn-firmar">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M12 19l7-7 3 3-7 7-3-3z" stroke-width="2"/>
                  <path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z" stroke-width="2"/>
                </svg>
                <span>Firmar Seleccionados ({{ reportesSeleccionados.length }})</span>
              </button>
            </div>
          </div>
        </transition>

        <!-- ================== TABLE CONTAINER ================== -->
        <div class="apple-table-container">
          <div v-if="loading" class="apple-loading">
            <div class="apple-spinner"></div>
            <p>Cargando reportes...</p>
          </div>

          <div v-else-if="reportesFiltrados.length === 0" class="apple-empty">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke-width="1.5"/>
              <polyline points="14 2 14 8 20 8" stroke-width="1.5"/>
              <line x1="16" y1="13" x2="8" y2="13" stroke-width="1.5"/>
              <line x1="16" y1="17" x2="8" y2="17" stroke-width="1.5"/>
            </svg>
            <h3>No hay reportes</h3>
            <p>{{ filtrosActivos ? 'No se encontraron reportes con los filtros aplicados' : 'Aún no se han generado reportes' }}</p>
          </div>

          <div v-else class="apple-table-wrapper">
            <table class="apple-table">
              <thead>
                <tr>
                  <th class="th-checkbox">
                    <input 
                      type="checkbox" 
                      :checked="todosSeleccionados && reportesPendientesFiltrados.length > 0"
                      :indeterminate="algunosSeleccionados"
                      @change="toggleSeleccionarTodos"
                      :disabled="reportesPendientesFiltrados.length === 0"
                      class="apple-checkbox"
                      title="Seleccionar todos los pendientes"
                    >
                  </th>
                  <th>Estado</th>
                  <th>Usuario</th>
                  <th>Territorio</th>
                  <th>Reporte</th>
                  <th>Período</th>
                  <th>Fecha</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="reporte in reportesPaginados" :key="reporte.id" 
                    class="apple-table-row"
                    :class="{ 'apple-row-firmado': reporte.firmado_supervisor, 'apple-row-seleccionado': reportesSeleccionados.includes(reporte.id) }">
                  <td class="td-checkbox">
                    <input 
                      v-if="!reporte.firmado_supervisor"
                      type="checkbox"
                      :checked="reportesSeleccionados.includes(reporte.id)"
                      @change="toggleSeleccion(reporte)"
                      class="apple-checkbox"
                      title="Seleccionar para firmar"
                    >
                  </td>
                  <td>
                    <div v-if="reporte.firmado_supervisor" class="apple-status-badge firmado" :title="'Firmado por ' + reporte.nombre_supervisor">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M9 12l2 2 4-4" stroke-width="2.5"/>
                        <circle cx="12" cy="12" r="10" stroke-width="2"/>
                      </svg>
                      <span>Firmado</span>
                    </div>
                    <div v-else class="apple-status-badge pendiente">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <circle cx="12" cy="12" r="10" stroke-width="2"/>
                        <polyline points="12 6 12 12 16 14" stroke-width="2"/>
                      </svg>
                      <span>Pendiente</span>
                    </div>
                  </td>
                  <td>
                    <div class="apple-user-cell">
                      <div class="apple-avatar">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                          <circle cx="12" cy="7" r="4" stroke-width="2.5"/>
                        </svg>
                      </div>
                      <div class="apple-user-info">
                        <div class="apple-user-name">{{ reporte.usuario?.nombre_completo || 'Usuario desconocido' }}</div>
                        <div class="apple-user-role">{{ reporte.usuario?.correo || '-' }}</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span :class="['apple-territorio-badge', `territorio-${obtenerColorTerritorio(reporte.usuario?.territorio)}`]">{{ reporte.usuario?.territorio || 'Sin territorio' }}</span>
                  </td>
                  <td>
                    <div class="apple-reporte-info">
                      <span class="apple-reporte-nombre">{{ reporte.nombre_reporte }}</span>
                      <span v-if="reporte.firmado_supervisor" class="apple-firma-label">
                        Firmado por {{ reporte.nombre_supervisor }}
                      </span>
                    </div>
                  </td>
                  <td>
                    <span class="apple-periodo-badge">{{ reporte.mes }} {{ reporte.anio }}</span>
                  </td>
                  <td>
                    <div class="apple-fecha-info">
                      <span class="apple-fecha-text">{{ formatearFecha(reporte.fecha_generacion) }}</span>
                      <span v-if="reporte.firmado_supervisor && reporte.fecha_firma_supervisor" class="apple-fecha-firma">
                        Firmado: {{ formatearFecha(reporte.fecha_firma_supervisor) }}
                      </span>
                    </div>
                  </td>
                  <td>
                    <div class="apple-actions">
                      <!-- Botón firmar individual -->
                      <button 
                        v-if="!reporte.firmado_supervisor" 
                        @click="abrirModalFirmaIndividual(reporte)" 
                        class="apple-action-btn sign" 
                        title="Firmar reporte"
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <path d="M12 19l7-7 3 3-7 7-3-3z" stroke-width="2"/>
                          <path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z" stroke-width="2"/>
                        </svg>
                      </button>
                      <!-- Botón Ver -->
                      <button @click="verReporte(reporte)" :disabled="viendoReporte === reporte.id" class="apple-action-btn view" title="Ver reporte">
                        <svg v-if="viendoReporte !== reporte.id" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke-width="2"/><circle cx="12" cy="12" r="3" stroke-width="2"/>
                        </svg>
                        <div v-else class="apple-spinner-mini"></div>
                      </button>
                      <!-- Botón Descargar -->
                      <button v-if="reporte.tiene_pdf || reporte.datos_reporte" @click="descargarReporte(reporte)" :disabled="descargandoReporte === reporte.id" class="apple-action-btn download" title="Descargar">
                        <svg v-if="descargandoReporte !== reporte.id" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke-width="2"/>
                          <polyline points="7 10 12 15 17 10" stroke-width="2"/>
                          <line x1="12" y1="15" x2="12" y2="3" stroke-width="2"/>
                        </svg>
                        <div v-else class="apple-spinner-mini"></div>
                      </button>
                      <!-- Botón eliminar -->
                      <button 
                        @click="confirmarEliminacion(reporte)" 
                        :disabled="eliminandoReporte === reporte.id" 
                        class="apple-action-btn delete" 
                        :title="reporte.firmado_supervisor ? 'Eliminar reporte firmado' : 'Eliminar reporte'"
                      >
                        <svg v-if="eliminandoReporte !== reporte.id" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <polyline points="3 6 5 6 21 6" stroke-width="2"/>
                          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" stroke-width="2"/>
                        </svg>
                        <div v-else class="apple-spinner-mini"></div>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Paginación Apple Style -->
          <div v-if="totalPaginas > 1" class="apple-pagination">
            <div class="apple-pagination-controls">
              <button 
                @click="paginaActual = paginaActual - 1" 
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
                  @click="paginaActual = pagina"
                  :class="['apple-pagination-number', { 'active': paginaActual === pagina }]"
                >
                  {{ pagina }}
                </button>
              </div>

              <button 
                @click="paginaActual = paginaActual + 1" 
                :disabled="paginaActual === totalPaginas"
                class="apple-pagination-btn"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <polyline points="9 18 15 12 9 6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </div>
            
            <div class="apple-pagination-info">
              Mostrando {{ (paginaActual - 1) * porPagina + 1 }} - {{ Math.min(paginaActual * porPagina, reportesFiltrados.length) }} de {{ reportesFiltrados.length }}
            </div>
          </div>
        </div>
      </div>

      <!-- Modal de Firma de Supervisor -->
      <Teleport to="body">
        <Transition name="modal-fade">
          <div v-if="mostrarModalFirma" class="modal-overlay" @click.self="cancelarFirma">
            <div class="modal-container modal-firma">
              <div class="modal-header firma-header">
                <div class="modal-icon firma-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 19l7-7 3 3-7 7-3-3z"/>
                    <path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/>
                    <path d="M2 2l7.586 7.586"/>
                  </svg>
                </div>
                <div class="modal-title-container">
                  <h3>Firmar Reportes</h3>
                  <p>{{ reportesAFirmar.length }} reporte(s) seleccionado(s)</p>
                </div>
                <button @click="cancelarFirma" class="modal-close-btn">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
              </div>
              
              <div class="modal-body">
                <!-- Lista de reportes a firmar -->
                <div class="reportes-a-firmar">
                  <h4>Reportes a firmar:</h4>
                  <div class="reportes-list-scroll">
                    <div v-for="reporte in reportesAFirmar" :key="reporte.id" class="reporte-item">
                      <div class="reporte-item-icon">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                          <polyline points="14 2 14 8 20 8"/>
                        </svg>
                      </div>
                      <div class="reporte-item-info">
                        <span class="reporte-item-nombre">{{ reporte.nombre_reporte }}</span>
                        <span class="reporte-item-usuario">{{ reporte.usuario?.nombre_completo }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Componente de firma -->
                <div class="firma-container">
                  <FirmaDigitalAdmin 
                    ref="firmaComponentRef" 
                    label="Firma del Supervisor"
                    @firma-cambiada="onFirmaCambiada"
                  />
                </div>
              </div>
              
              <div class="modal-footer">
                <button @click="cancelarFirma" class="btn-cancel">
                  Cancelar
                </button>
                <button 
                  @click="confirmarFirma" 
                  class="btn-firmar-confirm"
                  :disabled="firmandoReportes || !firmaValida"
                >
                  <svg v-if="!firmandoReportes" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 19l7-7 3 3-7 7-3-3z"/>
                    <path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/>
                  </svg>
                  <div v-else class="spinner-mini white"></div>
                  {{ firmandoReportes ? 'Firmando...' : 'Firmar Reportes' }}
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </Teleport>

      <!-- Modal de Confirmación de Firma Exitosa -->
      <Teleport to="body">
        <Transition name="modal-fade">
          <div v-if="mostrarModalExito" class="modal-overlay" @click.self="cerrarModalExito">
            <div class="modal-container modal-exito">
              <div class="modal-header exito-header">
                <div class="modal-icon exito-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M9 12l2 2 4-4"/>
                    <circle cx="12" cy="12" r="10"/>
                  </svg>
                </div>
              </div>
              <div class="modal-body text-center">
                <h3 class="exito-title">¡Reportes Firmados!</h3>
                <p class="exito-message">Se firmaron {{ resultadoFirma.exitosos }} reporte(s) exitosamente.</p>
                <p v-if="resultadoFirma.fallidos > 0" class="exito-warning">
                  {{ resultadoFirma.fallidos }} reporte(s) no pudieron ser firmados.
                </p>
              </div>
              <div class="modal-footer centered">
                <button @click="cerrarModalExito" class="btn-exito-ok">
                  Aceptar
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </Teleport>

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

      <!-- Modal de Descarga de Reportes -->
      <Teleport to="body">
        <Transition name="modal-fade">
          <div v-if="mostrarModalDescarga" class="modal-overlay" @click.self="cerrarModalDescarga">
            <div class="modal-container modal-descarga">
              <!-- Botón cerrar circular en esquina superior derecha -->
              <button @click="cerrarModalDescarga" class="btn-close-corner">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
              
              <div class="modal-header descarga-header">
                <div class="modal-icon descarga-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                  </svg>
                </div>
                <div class="modal-title-container">
                  <h3>Descargar Reportes</h3>
                  <p>Selecciona el período y tipo de reportes</p>
                </div>
              </div>
              
              <div class="modal-body descarga-body">
                <!-- Selectores de Período -->
                <div class="periodo-selectors">
                  <div class="periodo-grupo">
                    <label class="periodo-label">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                        <line x1="16" y1="2" x2="16" y2="6"></line>
                        <line x1="8" y1="2" x2="8" y2="6"></line>
                        <line x1="3" y1="10" x2="21" y2="10"></line>
                      </svg>
                      Mes
                    </label>
                    <select v-model="descargaFiltros.mes" class="periodo-select" :class="{ 'select-required': !descargaFiltros.mes }">
                      <option value="" disabled>Selecciona mes</option>
                      <option v-for="mes in meses" :key="mes.value" :value="mes.value">{{ mes.label }}</option>
                    </select>
                  </div>
                  
                  <div class="periodo-grupo">
                    <label class="periodo-label">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                        <line x1="16" y1="2" x2="16" y2="6"></line>
                        <line x1="8" y1="2" x2="8" y2="6"></line>
                      </svg>
                      Año
                    </label>
                    <select v-model="descargaFiltros.anio" class="periodo-select" :class="{ 'select-required': !descargaFiltros.anio }">
                      <option value="" disabled>Selecciona año</option>
                      <option v-for="anio in anios" :key="anio" :value="anio">{{ anio }}</option>
                    </select>
                  </div>
                </div>

                <!-- Tipo de Reportes -->
                <div class="tipo-reportes-section">
                  <label class="section-label">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      <polyline points="14 2 14 8 20 8"/>
                      <line x1="16" y1="13" x2="8" y2="13"/>
                      <line x1="16" y1="17" x2="8" y2="17"/>
                    </svg>
                    Tipo de Reportes
                  </label>
                  <div class="tipo-reportes-grid">
                    <label class="tipo-card" :class="{ 'active': tipoDescarga === 'todos' }">
                      <input type="radio" v-model="tipoDescarga" value="todos" name="tipo-descarga">
                      <div class="tipo-card-content">
                        <div class="tipo-icon todos">
                          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                            <polyline points="14 2 14 8 20 8"/>
                          </svg>
                        </div>
                        <span class="tipo-name">Todos</span>
                        <span class="tipo-count">{{ conteoReportesDescarga.todos }}</span>
                      </div>
                    </label>
                    
                    <label class="tipo-card" :class="{ 'active': tipoDescarga === 'firmados' }">
                      <input type="radio" v-model="tipoDescarga" value="firmados" name="tipo-descarga">
                      <div class="tipo-card-content">
                        <div class="tipo-icon firmados">
                          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M9 12l2 2 4-4"/>
                            <circle cx="12" cy="12" r="10"/>
                          </svg>
                        </div>
                        <span class="tipo-name">Firmados</span>
                        <span class="tipo-count">{{ conteoReportesDescarga.firmados }}</span>
                      </div>
                    </label>
                    
                    <label class="tipo-card" :class="{ 'active': tipoDescarga === 'pendientes' }">
                      <input type="radio" v-model="tipoDescarga" value="pendientes" name="tipo-descarga">
                      <div class="tipo-card-content">
                        <div class="tipo-icon pendientes">
                          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/>
                            <polyline points="12 6 12 12 16 14"/>
                          </svg>
                        </div>
                        <span class="tipo-name">Pendientes</span>
                        <span class="tipo-count">{{ conteoReportesDescarga.pendientes }}</span>
                      </div>
                    </label>
                  </div>
                </div>

                <!-- Aviso de campos obligatorios -->
                <div class="campos-obligatorios" v-if="!descargaFiltros.mes || !descargaFiltros.anio">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="8" x2="12" y2="12"/>
                    <line x1="12" y1="16" x2="12.01" y2="16"/>
                  </svg>
                  <span>Selecciona mes y año para continuar</span>
                </div>

                <!-- Resumen de descarga -->
                <div class="descarga-resumen" v-else-if="conteoReportesDescarga[tipoDescarga] > 0">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                  </svg>
                  <div class="resumen-texto">
                    <span class="resumen-cantidad">{{ conteoReportesDescarga[tipoDescarga] }}</span>
                    <span class="resumen-descripcion">
                      {{ tipoDescarga === 'todos' ? 'reportes' : tipoDescarga === 'firmados' ? 'reportes firmados' : 'reportes pendientes' }}
                      {{ descargaFiltros.mes ? 'de ' + descargaFiltros.mes : '' }}
                      {{ descargaFiltros.anio ? descargaFiltros.anio : '' }}
                    </span>
                  </div>
                </div>

                <div class="descarga-vacio" v-else>
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="8" x2="12" y2="12"/>
                    <line x1="12" y1="16" x2="12.01" y2="16"/>
                  </svg>
                  <p>No hay reportes disponibles con los filtros seleccionados</p>
                </div>

                <!-- Barra de progreso -->
                <div class="descarga-progreso" v-if="descargandoZip && progresoDescarga.total > 0">
                  <div class="progreso-header">
                    <span class="progreso-texto">{{ progresoDescarga.mensaje }}</span>
                    <span class="progreso-contador">{{ progresoDescarga.actual }}/{{ progresoDescarga.total }}</span>
                  </div>
                  <div class="progreso-barra">
                    <div class="progreso-fill" :style="{ width: (progresoDescarga.actual / progresoDescarga.total * 100) + '%' }"></div>
                  </div>
                </div>
              </div>
              
              <div class="modal-footer descarga-footer">
                <button @click="cerrarModalDescarga" class="btn-cancel" :disabled="descargandoZip">
                  Cancelar
                </button>
                <button 
                  @click="descargarReportesZip" 
                  class="btn-descargar-confirm"
                  :disabled="descargandoZip || conteoReportesDescarga[tipoDescarga] === 0 || !descargaFiltros.mes || !descargaFiltros.anio"
                >
                  <svg v-if="!descargandoZip" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                  </svg>
                  <div v-else class="spinner-mini white"></div>
                  {{ descargandoZip ? (progresoDescarga.actual > 0 ? `${progresoDescarga.actual}/${progresoDescarga.total}` : 'Preparando...') : 'Descargar ZIP' }}
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </Teleport>

      <!-- Apple Mini Modal de Carga -->
      <Teleport to="body">
        <Transition name="apple-mini-modal">
          <div v-if="mostrarMiniModalCarga" class="apple-mini-modal-overlay">
            <div class="apple-mini-modal">
              <!-- Anillo de progreso con porcentaje real -->
              <div class="apple-mini-modal-spinner">
                <svg class="apple-progress-ring" viewBox="0 0 100 100">
                  <circle class="apple-ring-bg" cx="50" cy="50" r="42"/>
                  <circle 
                    class="apple-ring-progress-real" 
                    cx="50" cy="50" r="42"
                    :style="{ strokeDashoffset: 264 - (264 * Math.min(miniModalProgreso, 100) / 100) }"
                  />
                </svg>
                <div class="apple-mini-modal-percent">
                  {{ Math.round(Math.min(miniModalProgreso, 100)) }}<span>%</span>
                </div>
              </div>
              
              <!-- Info del reporte -->
              <div class="apple-mini-modal-content">
                <div class="apple-mini-modal-action">
                  <div class="apple-mini-modal-action-icon" :class="miniModalTipo">
                    <svg v-if="miniModalTipo === 'ver'" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke-width="2"/>
                      <circle cx="12" cy="12" r="3" stroke-width="2"/>
                    </svg>
                    <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke-width="2"/>
                      <polyline points="7 10 12 15 17 10" stroke-width="2"/>
                      <line x1="12" y1="15" x2="12" y2="3" stroke-width="2"/>
                    </svg>
                  </div>
                  <span>{{ miniModalTitulo }}</span>
                </div>
                
                <div class="apple-mini-modal-user">
                  <div class="apple-mini-modal-avatar">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke-width="2"/>
                      <circle cx="12" cy="7" r="4" stroke-width="2"/>
                    </svg>
                  </div>
                  <div class="apple-mini-modal-user-info">
                    <h4>{{ miniModalUsuario }}</h4>
                    <p>{{ miniModalPeriodo }}</p>
                  </div>
                </div>
              </div>
              
              <!-- Barra de progreso inferior -->
              <div class="apple-mini-modal-progress-bar">
                <div class="apple-mini-modal-progress-fill" :style="{ width: Math.min(miniModalProgreso, 100) + '%' }"></div>
              </div>
            </div>
          </div>
        </Transition>
      </Teleport>

      <!-- Modal de Confirmación de Descarga Exitosa (Apple Style) -->
      <Teleport to="body">
        <Transition name="apple-success-modal">
          <div v-if="mostrarModalDescargaExitosa" class="apple-success-overlay" @click.self="cerrarModalDescargaExitosa">
            <div class="apple-success-modal">
              <!-- Animación de check -->
              <div class="apple-success-check">
                <svg class="apple-check-circle" viewBox="0 0 100 100">
                  <circle class="apple-check-bg" cx="50" cy="50" r="45"/>
                  <circle class="apple-check-ring" cx="50" cy="50" r="45"/>
                  <path class="apple-check-mark" d="M30 50 L45 65 L70 35" />
                </svg>
              </div>
              
              <!-- Contenido -->
              <div class="apple-success-content">
                <h3>¡Descarga Completada!</h3>
                <p class="apple-success-filename">{{ descargaExitosaInfo.nombre }}</p>
              </div>
              
              <!-- Info del usuario -->
              <div class="apple-success-info">
                <div class="apple-success-user">
                  <div class="apple-success-avatar">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke-width="2"/>
                      <circle cx="12" cy="7" r="4" stroke-width="2"/>
                    </svg>
                  </div>
                  <div class="apple-success-user-details">
                    <span class="apple-success-user-name">{{ descargaExitosaInfo.usuario }}</span>
                    <span class="apple-success-user-period">{{ descargaExitosaInfo.periodo }}</span>
                  </div>
                </div>
                
                <div class="apple-success-status" :class="descargaExitosaInfo.firmado ? 'firmado' : 'pendiente'">
                  <svg v-if="descargaExitosaInfo.firmado" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M9 12l2 2 4-4" stroke-width="2.5"/>
                    <circle cx="12" cy="12" r="10" stroke-width="2"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10" stroke-width="2"/>
                    <polyline points="12 6 12 12 16 14" stroke-width="2"/>
                  </svg>
                  <span>{{ descargaExitosaInfo.firmado ? 'Firmado' : 'Pendiente' }}</span>
                </div>
              </div>
              
              <!-- Botón cerrar -->
              <button @click="cerrarModalDescargaExitosa" class="apple-success-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M5 12h14" stroke-width="2.5" stroke-linecap="round"/>
                  <path d="M12 5l7 7-7 7" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Continuar</span>
              </button>
            </div>
          </div>
        </Transition>
      </Teleport>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import FirmaDigitalAdmin from '../components/FirmaDigitalAdmin.vue'
import reportesService from '../services/reportesService'
import authService from '../services/authService'
import { generarPDFDesdesDatos } from '../utils/pdfGenerator'
import JSZip from 'jszip'
import { saveAs } from 'file-saver'

const router = useRouter()

// Obtener territorio del usuario admin actual (si es territorial)
const territorioUsuario = ref(authService.getTerritorioFilter())

// Función para obtener el color del territorio
const obtenerColorTerritorio = (territorio) => {
  if (!territorio) return 'gray'
  
  const coloresTerritorio = {
    "Acapulco - Centro - Norte - Tierra Caliente": "blue",
    "Acayucan": "emerald",
    "Balancán": "violet",
    "Chihuahua / Sonora": "orange",
    "Colima": "cyan",
    "Comalcalco": "rose",
    "Córdoba": "amber",
    "Costa Chica - Montaña": "teal",
    "Costa Grande - Sierra": "indigo",
    "Durango / Zacatecas": "lime",
    "Hidalgo": "pink",
    "Istmo": "sky",
    "Michoacán": "red",
    "Mixteca": "green",
    "Morelos": "purple",
    "Nayarit / Jalisco": "yellow",
    "Ocosingo": "fuchsia",
    "Palenque": "slate",
    "Papantla": "zinc",
    "Pichucalco": "stone",
    "Puebla": "coral",
    "San Luis Potosí": "mint",
    "Sinaloa": "navy",
    "Tamaulipas": "gold",
    "Tantoyuca": "crimson",
    "Tapachula": "forest",
    "Teapa": "plum",
    "Tlaxcala / Estado de México": "bronze",
    "Tzucacab / Opb": "ocean",
    "Xpujil": "wine",
    "Oficinas Centrales": "charcoal"
  }
  
  return coloresTerritorio[territorio] || 'gray'
}

const loading = ref(false)
const reportes = ref([])
const totalReportes = ref(0)
const territorios = ref([])

const viendoReporte = ref(null)
const descargandoReporte = ref(null)
const eliminandoReporte = ref(null)

// Mini modal de carga estilo Apple
const mostrarMiniModalCarga = ref(false)
const miniModalTipo = ref('ver') // 'ver' o 'descargar'
const miniModalTitulo = ref('')
const miniModalMensaje = ref('')
const miniModalNombreReporte = ref('')
const miniModalUsuario = ref('')
const miniModalPeriodo = ref('')
const miniModalProgreso = ref(0) // 0-100

// Modal de confirmación de descarga Apple
const mostrarModalDescargaExitosa = ref(false)
const descargaExitosaInfo = ref({
  nombre: '',
  usuario: '',
  periodo: '',
  firmado: false
})

const mostrarModalEliminar = ref(false)
const reporteAEliminar = ref(null)

// Estados para firma
const reportesSeleccionados = ref([])
const mostrarModalFirma = ref(false)
const reportesAFirmar = ref([])
const firmandoReportes = ref(false)
const firmaComponentRef = ref(null)
const firmaValida = ref(false)

// Modal de éxito
const mostrarModalExito = ref(false)
const resultadoFirma = ref({ exitosos: 0, fallidos: 0 })

// Modal de descarga
const mostrarModalDescarga = ref(false)
const tipoDescarga = ref('todos')
const descargandoZip = ref(false)
const descargaFiltros = ref({
  mes: '',
  anio: ''
})
const progresoDescarga = ref({ actual: 0, total: 0, mensaje: '' })

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
  tipo: '',
  estadoFirma: ''
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
  
  // Filtro de búsqueda en tiempo real (nombre, correo, CURP, territorio)
  if (filtros.value.busqueda) {
    const busqueda = filtros.value.busqueda.toLowerCase().trim()
    resultado = resultado.filter(r => {
      const nombreReporte = r.nombre_reporte?.toLowerCase() || ''
      const nombreCompleto = r.usuario?.nombre_completo?.toLowerCase() || ''
      const correo = r.usuario?.correo?.toLowerCase() || ''
      const curp = r.usuario?.curp?.toLowerCase() || ''
      const territorio = r.usuario?.territorio?.toLowerCase() || ''
      
      return nombreReporte.includes(busqueda) ||
             nombreCompleto.includes(busqueda) ||
             correo.includes(busqueda) ||
             curp.includes(busqueda) ||
             territorio.includes(busqueda)
    })
  }
  
  // Filtro por tipo de reporte
  if (filtros.value.tipo) {
    resultado = resultado.filter(r => r.tipo === filtros.value.tipo)
  }
  
  // Filtro por estado de firma
  if (filtros.value.estadoFirma === 'pendiente') {
    resultado = resultado.filter(r => !r.firmado_supervisor)
  } else if (filtros.value.estadoFirma === 'firmado') {
    resultado = resultado.filter(r => r.firmado_supervisor)
  }
  
  return resultado
})

// Computed para reportes firmados y pendientes
const reportesFirmados = computed(() => reportes.value.filter(r => r.firmado_supervisor))
const reportesPendientes = computed(() => reportes.value.filter(r => !r.firmado_supervisor))
const reportesPendientesFiltrados = computed(() => reportesFiltrados.value.filter(r => !r.firmado_supervisor))

// Computed para conteo de reportes según filtros de descarga
const conteoReportesDescarga = computed(() => {
  let reportesFiltradosDescarga = [...reportes.value]
  
  // Filtrar por mes seleccionado en el modal
  if (descargaFiltros.value.mes) {
    reportesFiltradosDescarga = reportesFiltradosDescarga.filter(r => {
      const mesReporte = r.mes || r.nombre_reporte?.match(/Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre/)?.[0]
      return mesReporte === descargaFiltros.value.mes
    })
  }
  
  // Filtrar por año seleccionado en el modal
  if (descargaFiltros.value.anio) {
    reportesFiltradosDescarga = reportesFiltradosDescarga.filter(r => {
      const anioReporte = r.anio || r.nombre_reporte?.match(/\d{4}/)?.[0]
      return anioReporte == descargaFiltros.value.anio
    })
  }
  
  return {
    todos: reportesFiltradosDescarga.length,
    firmados: reportesFiltradosDescarga.filter(r => r.firmado_supervisor).length,
    pendientes: reportesFiltradosDescarga.filter(r => !r.firmado_supervisor).length
  }
})

// Computed para selección
const todosSeleccionados = computed(() => {
  const pendientes = reportesPendientesFiltrados.value
  return pendientes.length > 0 && pendientes.every(r => reportesSeleccionados.value.includes(r.id))
})

const algunosSeleccionados = computed(() => {
  const pendientes = reportesPendientesFiltrados.value
  const seleccionados = pendientes.filter(r => reportesSeleccionados.value.includes(r.id))
  return seleccionados.length > 0 && seleccionados.length < pendientes.length
})

const limpiarBusquedaReportes = () => {
  filtros.value.busqueda = ''
}

const reportesPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * porPagina.value
  return reportesFiltrados.value.slice(inicio, inicio + porPagina.value)
})

const totalPaginas = computed(() => Math.ceil(reportesFiltrados.value.length / porPagina.value) || 1)

// Computed para páginas visibles en paginación
const paginasVisibles = computed(() => {
  const total = totalPaginas.value
  const actual = paginaActual.value
  const visibles = []
  
  if (total <= 5) {
    for (let i = 1; i <= total; i++) visibles.push(i)
  } else {
    if (actual <= 3) {
      visibles.push(1, 2, 3, 4, 5)
    } else if (actual >= total - 2) {
      visibles.push(total - 4, total - 3, total - 2, total - 1, total)
    } else {
      visibles.push(actual - 2, actual - 1, actual, actual + 1, actual + 2)
    }
  }
  
  return visibles
})

const filtrosActivos = computed(() => 
  filtros.value.busqueda || filtros.value.mes || filtros.value.anio || filtros.value.territorio || filtros.value.tipo
)

async function cargarReportes() {
  loading.value = true
  try {
    const params = { limite: 500 }
    if (filtros.value.mes) params.mes = filtros.value.mes
    if (filtros.value.anio) params.anio = filtros.value.anio
    
    // Si el usuario es territorial, filtrar automáticamente por su territorio
    if (territorioUsuario.value) {
      params.territorio = territorioUsuario.value
      console.log(`🌎 Filtrando reportes por territorio: ${territorioUsuario.value}`)
    } else if (filtros.value.territorio) {
      // Si es admin global, permitir filtro manual
      params.territorio = filtros.value.territorio
    }
    
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
  
  // Mostrar mini modal Apple con info completa
  miniModalTipo.value = 'ver'
  miniModalTitulo.value = 'Abriendo Reporte'
  miniModalNombreReporte.value = reporte.nombre_reporte
  miniModalUsuario.value = reporte.usuario?.nombre_completo || 'Usuario'
  miniModalPeriodo.value = `${reporte.mes} ${reporte.anio}`
  miniModalProgreso.value = 0
  mostrarMiniModalCarga.value = true
  
  // Simular progreso de apertura
  const intervalo = setInterval(() => {
    if (miniModalProgreso.value < 90) {
      miniModalProgreso.value += Math.random() * 15 + 5
    }
  }, 150)
  
  try {
    await reportesService.verReporte(reporte.id)
    miniModalProgreso.value = 100
  } catch (error) {
    console.error('Error al ver reporte:', error)
    alert('No se pudo abrir el reporte: ' + error.message)
  } finally {
    clearInterval(intervalo)
    // Pequeño delay para animación fluida
    setTimeout(() => {
      mostrarMiniModalCarga.value = false
      viendoReporte.value = null
      miniModalProgreso.value = 0
    }, 400)
  }
}

async function descargarReporte(reporte) {
  if (descargandoReporte.value) {
    console.log('⚠️ Ya se está descargando un reporte')
    return
  }

  console.log(`📥 Descargando reporte: ${reporte.nombre_reporte}`)
  descargandoReporte.value = reporte.id
  
  // Mostrar mini modal Apple con info completa
  miniModalTipo.value = 'descargar'
  miniModalTitulo.value = 'Descargando'
  miniModalNombreReporte.value = reporte.nombre_reporte
  miniModalUsuario.value = reporte.usuario?.nombre_completo || 'Usuario'
  miniModalPeriodo.value = `${reporte.mes} ${reporte.anio}`
  miniModalProgreso.value = 0
  mostrarMiniModalCarga.value = true
  
  // Progreso: 0-30% obtener datos
  const intervaloInicial = setInterval(() => {
    if (miniModalProgreso.value < 30) {
      miniModalProgreso.value += Math.random() * 8 + 2
    }
  }, 100)

  try {
    // Obtener datos del reporte desde el servidor
    const response = await reportesService.obtenerReporte(reporte.id)
    clearInterval(intervaloInicial)
    miniModalProgreso.value = 35
    
    if (!response.success) {
      throw new Error('No se pudo obtener el reporte')
    }
    
    const reporteData = response.reporte
    
    // Generar PDF desde datos estructurados
    if (reporteData.datos_reporte) {
      console.log('📄 Generando PDF desde datos estructurados...')
      miniModalProgreso.value = 50
      
      // Progreso: 50-90% generar PDF
      const intervaloPDF = setInterval(() => {
        if (miniModalProgreso.value < 85) {
          miniModalProgreso.value += Math.random() * 10 + 3
        }
      }, 120)
      
      // Generar PDF con las firmas disponibles
      const pdfBase64 = await generarPDFDesdesDatos(
        reporteData.datos_reporte,
        reporteData.firma_usuario_base64,
        reporteData.firmado_supervisor ? reporteData.firma_supervisor_base64 : null,
        reporteData.nombre_supervisor
      )
      
      clearInterval(intervaloPDF)
      miniModalProgreso.value = 95
      
      // Descargar el PDF
      descargarPDFBase64(pdfBase64, reporte.nombre_reporte)
      miniModalProgreso.value = 100
      
      console.log('✅ Reporte generado y descargado exitosamente')
      
      // Guardar info para modal de confirmación
      descargaExitosaInfo.value = {
        nombre: reporte.nombre_reporte,
        usuario: reporte.usuario?.nombre_completo || 'Usuario',
        periodo: `${reporte.mes} ${reporte.anio}`,
        firmado: reporteData.firmado_supervisor
      }
    } else {
      throw new Error('El reporte no tiene datos disponibles para generar el PDF')
    }
    
  } catch (error) {
    console.error('❌ Error descargando reporte:', error)
    
    let mensaje = 'Error al descargar el reporte'
    if (error.response?.status === 404) {
      mensaje = 'El reporte no está disponible'
    }
    
    alert(mensaje)
  } finally {
    // Pequeño delay para animación fluida, luego mostrar modal de confirmación
    setTimeout(() => {
      mostrarMiniModalCarga.value = false
      descargandoReporte.value = null
      miniModalProgreso.value = 0
      
      // Si fue exitoso, mostrar modal de confirmación
      if (descargaExitosaInfo.value.nombre) {
        setTimeout(() => {
          mostrarModalDescargaExitosa.value = true
        }, 200)
      }
    }, 400)
  }
}

function descargarPDFBase64(base64Data, nombreReporte) {
  const byteCharacters = atob(base64Data)
  const byteNumbers = new Array(byteCharacters.length)
  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i)
  }
  const byteArray = new Uint8Array(byteNumbers)
  const blob = new Blob([byteArray], { type: 'application/pdf' })
  
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${nombreReporte.replace(/\s+/g, '_')}.pdf`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.URL.revokeObjectURL(url)
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
  filtros.value = { busqueda: '', mes: '', anio: '', territorio: '', tipo: '', estadoFirma: '' }
  reportesSeleccionados.value = []
  cargarReportes()
}

// ========== FUNCIONES DE SELECCIÓN ==========

function toggleSeleccion(reporte) {
  if (reporte.firmado_supervisor) return
  
  const index = reportesSeleccionados.value.indexOf(reporte.id)
  if (index > -1) {
    reportesSeleccionados.value.splice(index, 1)
  } else {
    reportesSeleccionados.value.push(reporte.id)
  }
}

function toggleSeleccionarTodos() {
  const pendientes = reportesPendientesFiltrados.value
  if (todosSeleccionados.value) {
    // Deseleccionar todos
    reportesSeleccionados.value = reportesSeleccionados.value.filter(
      id => !pendientes.some(r => r.id === id)
    )
  } else {
    // Seleccionar todos los pendientes
    const nuevoSet = new Set(reportesSeleccionados.value)
    pendientes.forEach(r => nuevoSet.add(r.id))
    reportesSeleccionados.value = Array.from(nuevoSet)
  }
}

function seleccionarTodosPendientes() {
  const pendientes = reportesPendientesFiltrados.value
  reportesSeleccionados.value = pendientes.map(r => r.id)
}

function deseleccionarTodos() {
  reportesSeleccionados.value = []
}

// ========== FUNCIONES DE FIRMA ==========

function abrirModalFirma() {
  if (reportesSeleccionados.value.length === 0) return
  
  // Obtener los objetos de reportes seleccionados
  reportesAFirmar.value = reportes.value.filter(r => 
    reportesSeleccionados.value.includes(r.id) && !r.firmado_supervisor
  )
  
  if (reportesAFirmar.value.length === 0) {
    alert('No hay reportes pendientes seleccionados para firmar.')
    return
  }
  
  mostrarModalFirma.value = true
  firmaValida.value = false
  
  // Reinicializar el componente de firma
  nextTick(() => {
    if (firmaComponentRef.value) {
      firmaComponentRef.value.reinicializar()
    }
  })
}

function abrirModalFirmaIndividual(reporte) {
  reportesSeleccionados.value = [reporte.id]
  reportesAFirmar.value = [reporte]
  mostrarModalFirma.value = true
  firmaValida.value = false
  
  nextTick(() => {
    if (firmaComponentRef.value) {
      firmaComponentRef.value.reinicializar()
    }
  })
}

function cancelarFirma() {
  mostrarModalFirma.value = false
  reportesAFirmar.value = []
  firmaValida.value = false
}

async function confirmarFirma() {
  // Verificar firma
  if (!firmaComponentRef.value || !firmaComponentRef.value.tieneFirma()) {
    alert('Por favor, dibuje su firma antes de continuar.')
    return
  }
  
  firmandoReportes.value = true
  
  try {
    // Obtener datos del supervisor actual
    const adminData = authService.getCurrentUser()
    const firmaBase64 = firmaComponentRef.value.obtenerFirmaBase64()
    
    const firmaData = {
      supervisor_id: adminData?.id || 1,
      nombre_supervisor: adminData?.nombre_completo || adminData?.username || 'Supervisor',
      firma_base64: firmaBase64
    }
    
    console.log('✍️ Firmando reportes:', reportesAFirmar.value.map(r => r.id))
    
    // Firmar cada reporte
    const resultados = await reportesService.firmarMultiplesReportes(
      reportesAFirmar.value.map(r => r.id),
      firmaData
    )
    
    resultadoFirma.value = {
      exitosos: resultados.exitosos.length,
      fallidos: resultados.fallidos.length
    }
    
    // Actualizar estado local de los reportes firmados
    resultados.exitosos.forEach(id => {
      const reporte = reportes.value.find(r => r.id === id)
      if (reporte) {
        reporte.firmado_supervisor = true
        reporte.nombre_supervisor = firmaData.nombre_supervisor
        reporte.fecha_firma_supervisor = new Date().toISOString()
      }
    })
    
    // Limpiar selección
    reportesSeleccionados.value = reportesSeleccionados.value.filter(
      id => !resultados.exitosos.includes(id)
    )
    
    // Cerrar modal de firma y mostrar modal de éxito
    mostrarModalFirma.value = false
    mostrarModalExito.value = true
    
    // Recargar reportes desde el backend para actualizar la vista
    await cargarReportes()
    
    // Recargar estadísticas
    await cargarEstadisticas()
    
  } catch (error) {
    console.error('Error firmando reportes:', error)
    alert('Error al firmar los reportes: ' + error.message)
  } finally {
    firmandoReportes.value = false
  }
}

function cerrarModalExito() {
  mostrarModalExito.value = false
  resultadoFirma.value = { exitosos: 0, fallidos: 0 }
}

function cerrarModalDescargaExitosa() {
  mostrarModalDescargaExitosa.value = false
  descargaExitosaInfo.value = { nombre: '', usuario: '', periodo: '', firmado: false }
}

// Funciones para descarga de reportes
function abrirModalDescarga() {
  // Reiniciar filtros del modal de descarga
  descargaFiltros.value = { mes: '', anio: '' }
  tipoDescarga.value = 'todos'
  mostrarModalDescarga.value = true
}

function cerrarModalDescarga() {
  mostrarModalDescarga.value = false
  descargandoZip.value = false
}

async function descargarReportesZip() {
  try {
    descargandoZip.value = true
    progresoDescarga.value = { actual: 0, total: 0, mensaje: 'Obteniendo reportes...' }
    
    console.log('📦 Iniciando descarga ZIP:', { 
      mes: descargaFiltros.value.mes, 
      anio: descargaFiltros.value.anio, 
      tipo: tipoDescarga.value 
    })
    
    // Filtrar reportes según los criterios del modal
    let reportesADescargar = [...reportes.value]
    
    // Filtrar por mes
    if (descargaFiltros.value.mes) {
      reportesADescargar = reportesADescargar.filter(r => {
        const mesReporte = r.mes || r.nombre_reporte?.match(/Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Octubre|Noviembre|Diciembre/)?.[0]
        return mesReporte === descargaFiltros.value.mes
      })
    }
    
    // Filtrar por año
    if (descargaFiltros.value.anio) {
      reportesADescargar = reportesADescargar.filter(r => {
        const anioReporte = r.anio || r.nombre_reporte?.match(/\d{4}/)?.[0]
        return anioReporte == descargaFiltros.value.anio
      })
    }
    
    // Filtrar por tipo de descarga
    if (tipoDescarga.value === 'firmados') {
      reportesADescargar = reportesADescargar.filter(r => r.firmado_supervisor)
    } else if (tipoDescarga.value === 'pendientes') {
      reportesADescargar = reportesADescargar.filter(r => !r.firmado_supervisor)
    }
    
    if (reportesADescargar.length === 0) {
      throw new Error('No hay reportes para descargar con los filtros seleccionados')
    }
    
    progresoDescarga.value.total = reportesADescargar.length
    console.log(`📄 Procesando ${reportesADescargar.length} reportes...`)
    
    // Crear ZIP
    const zip = new JSZip()
    let pdfsGenerados = 0
    let errores = 0
    
    // Procesar cada reporte
    for (let i = 0; i < reportesADescargar.length; i++) {
      const reporte = reportesADescargar[i]
      progresoDescarga.value.actual = i + 1
      progresoDescarga.value.mensaje = `Generando PDF ${i + 1} de ${reportesADescargar.length}...`
      
      try {
        // Obtener datos completos del reporte
        const datosCompletos = await reportesService.obtenerReporte(reporte.id)
        
        if (!datosCompletos.success || !datosCompletos.reporte) {
          console.warn(`⚠️ No se pudieron obtener datos del reporte ${reporte.id}`)
          errores++
          continue
        }
        
        const reporteData = datosCompletos.reporte
        let pdfBase64 = null
        
        // Generar PDF desde datos_reporte (igual que la visualización)
        if (reporteData.datos_reporte) {
          console.log(`📄 Generando PDF para reporte ${reporte.id}...`)
          pdfBase64 = await generarPDFDesdesDatos(
            reporteData.datos_reporte,
            reporteData.firma_usuario_base64,
            reporteData.firma_supervisor_base64,
            reporteData.nombre_supervisor
          )
        } else if (reporteData.pdf_base64) {
          // Si hay PDF guardado, usar ese
          pdfBase64 = reporteData.pdf_base64
          // Limpiar prefijo si existe
          if (pdfBase64.includes('base64,')) {
            pdfBase64 = pdfBase64.split('base64,')[1]
          }
        }
        
        if (!pdfBase64) {
          console.warn(`⚠️ No se pudo generar PDF para reporte ${reporte.id}`)
          errores++
          continue
        }
        
        // Convertir base64 a bytes
        const pdfBytes = Uint8Array.from(atob(pdfBase64), c => c.charCodeAt(0))
        
        // Sanitizar nombres para el archivo
        const territorio = (reporte.usuario?.territorio || 'Sin_Territorio').replace(/[<>:"/\\|?*]/g, '_')
        const nombreUsuario = (reporte.usuario?.nombre_completo || 'Usuario').replace(/[<>:"/\\|?*]/g, '_')
        const mesReporte = reporte.mes || descargaFiltros.value.mes
        const anioReporte = reporte.anio || descargaFiltros.value.anio
        
        // Nombre del archivo: Territorio/Mes_Año/NombreUsuario_Reporte.pdf
        const fileName = `${territorio}/${mesReporte}_${anioReporte}/${nombreUsuario}_Reporte_${mesReporte}_${anioReporte}.pdf`
        
        // Agregar al ZIP
        zip.file(fileName, pdfBytes, { binary: true })
        pdfsGenerados++
        console.log(`✅ Agregado: ${fileName}`)
        
      } catch (error) {
        console.error(`❌ Error procesando reporte ${reporte.id}:`, error)
        errores++
      }
    }
    
    if (pdfsGenerados === 0) {
      throw new Error('No se pudo generar ningún PDF. Verifica que los reportes tengan datos.')
    }
    
    progresoDescarga.value.mensaje = 'Comprimiendo archivos...'
    
    // Generar el ZIP
    const zipBlob = await zip.generateAsync({ 
      type: 'blob',
      compression: 'DEFLATE',
      compressionOptions: { level: 6 }
    })
    
    // Nombre del archivo ZIP
    const tipoLabel = tipoDescarga.value === 'todos' ? 'Todos' : tipoDescarga.value === 'firmados' ? 'Firmados' : 'Pendientes'
    const nombreZip = `Reportes_${tipoLabel}_${descargaFiltros.value.mes}_${descargaFiltros.value.anio}.zip`
    
    // Descargar
    saveAs(zipBlob, nombreZip)
    
    console.log(`✅ ZIP generado: ${nombreZip} (${pdfsGenerados} PDFs, ${errores} errores)`)
    
    if (errores > 0) {
      alert(`ZIP descargado con ${pdfsGenerados} reportes. ${errores} reportes no pudieron procesarse.`)
    }
    
    cerrarModalDescarga()
    
  } catch (error) {
    console.error('❌ Error descargando ZIP:', error)
    alert(error.message || 'Error al descargar los reportes. Por favor intenta de nuevo.')
  } finally {
    descargandoZip.value = false
    progresoDescarga.value = { actual: 0, total: 0, mensaje: '' }
  }
}

// Callback cuando cambia el estado de la firma
function onFirmaCambiada(tieneFirma) {
  console.log('📝 Firma cambiada:', tieneFirma)
  firmaValida.value = tieneFirma
}

// Watcher para verificar si la firma es válida
function verificarFirma() {
  if (firmaComponentRef.value) {
    firmaValida.value = firmaComponentRef.value.tieneFirma()
  }
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
/* ====================== APPLE DESIGN SYSTEM ====================== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ====================== APPLE DYNAMIC BACKGROUND ====================== */
.apple-dynamic-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;
  pointer-events: none;
  background: linear-gradient(135deg, #f8f9fa 0%, #f0fff0 100%);
}

.apple-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.6;
  animation: apple-float 20s ease-in-out infinite;
}

.apple-orb-1 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(139, 195, 74, 0.4) 0%, transparent 70%);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.apple-orb-2 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(102, 187, 106, 0.35) 0%, transparent 70%);
  bottom: 20%;
  left: -50px;
  animation-delay: -7s;
}

.apple-orb-3 {
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, rgba(129, 199, 132, 0.3) 0%, transparent 70%);
  top: 40%;
  right: 20%;
  animation-delay: -14s;
}

@keyframes apple-float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(20px, -30px) scale(1.05); }
  50% { transform: translate(-10px, 20px) scale(0.95); }
  75% { transform: translate(30px, 10px) scale(1.02); }
}

/* ====================== CONTAINER ====================== */
.reportes-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
  overflow: hidden;
}

.main-content {
  flex: 1;
  margin-left: min(220px, 18vw);
  width: calc(100vw - min(220px, 18vw));
  min-height: 100vh;
  position: relative;
  box-sizing: border-box;
  overflow-x: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  padding: 8px 16px 0 16px;
  z-index: 1;
}

/* ====================== APPLE STICKY WRAPPER ====================== */
.apple-sticky-wrapper {
  position: sticky;
  top: 0;
  z-index: 100;
  background: transparent;
  margin-bottom: 20px;
}

/* ====================== APPLE PAGE HEADER ====================== */
.apple-page-header {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 50%, #2E7D32 100%);
  color: white;
  border-radius: 28px 28px 0 0;
  border: 2px solid #8BC34A;
  border-bottom: none;
  padding: 14px 20px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
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
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-page-subtitle {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  font-weight: 500;
  letter-spacing: 0.3px;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
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
  color: white;
}

.apple-refresh-button svg {
  width: 14px;
  height: 14px;
  stroke: white;
  stroke-width: 2;
}

.apple-refresh-button:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.25);
  transform: scale(1.05);
}

.apple-refresh-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.apple-spin {
  animation: apple-spin-animation 1s linear infinite;
}

@keyframes apple-spin-animation {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ====================== APPLE STATS SECTION ====================== */
.apple-stats-section {
  background: white;
  border-radius: 0 0 28px 28px;
  border: 2px solid #8BC34A;
  border-top: none;
  padding: 18px 16px 16px 16px;
  box-shadow: none;
  margin-top: -1px;
}

.apple-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
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
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
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
  flex-shrink: 0;
}

.apple-stat-icon.blue {
  background: linear-gradient(135deg, #007AFF 0%, #5AC8FA 100%);
}

.apple-stat-icon.green {
  background: linear-gradient(135deg, #34C759 0%, #30D158 100%);
}

.apple-stat-icon.orange {
  background: linear-gradient(135deg, #FF9500 0%, #FFCC00 100%);
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

.apple-stat-content {
  flex: 1;
}

.apple-stat-value {
  font-size: 18px;
  font-weight: 700;
  color: #1d1d1f;
  line-height: 1;
  margin-bottom: 4px;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-stat-label {
  font-size: 10px;
  color: #86868b;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

/* ====================== APPLE SEARCH SECTION ====================== */
.apple-search-section {
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  padding-top: 12px;
  margin-top: 4px;
}

.apple-search-row {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 10px;
}

.apple-search-container {
  flex: 1;
  min-width: 250px;
  position: relative;
  display: flex;
  align-items: center;
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
  border-radius: 19px;
  border: 1.5px solid transparent;
  background: #f5f5f7;
  padding: 0 40px 0 40px;
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
  background: white;
  border-color: rgba(0, 122, 255, 0.2);
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.05);
}

.apple-clear-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #d1d1d6;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  padding: 0;
}

.apple-clear-btn svg {
  width: 16px;
  height: 16px;
  stroke: white;
  stroke-width: 2.5;
}

.apple-clear-btn:hover {
  background: #86868b;
  transform: translateY(-50%) scale(1.1);
}

/* ====================== APPLE FILTER CONTROLS ====================== */
.apple-filter-controls {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  flex-shrink: 0;
}

.apple-filter-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 16px;
  border: 1.5px solid #d1d1d6;
  background: white;
  color: #1d1d1f;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-filter-btn svg {
  width: 15px;
  height: 15px;
  stroke-width: 2;
}

.apple-filter-btn:hover {
  background: #f5f5f7;
  border-color: #d1d1d6;
  transform: translateY(-2px);
}

.apple-filter-btn.primary {
  background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
  color: white;
  border-color: #007AFF;
}

.apple-filter-btn.primary svg {
  stroke: white;
}

.apple-filter-btn.primary:hover {
  background: linear-gradient(135deg, #0056B3 0%, #4030A0 100%);
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
}

.apple-filter-btn.export {
  color: #34C759;
  border-color: rgba(52, 199, 89, 0.2);
}

.apple-filter-btn.export svg {
  stroke: #34C759;
}

.apple-filter-btn.export:hover {
  background: rgba(52, 199, 89, 0.08);
  border-color: #34C759;
}

/* ====================== APPLE UNIFIED FILTERS ====================== */
.apple-unified-filters {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.apple-quick-filters {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.apple-filter-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 7px 12px;
  border-radius: 20px;
  border: 2px solid transparent;
  background: #f5f5f7;
  color: #1d1d1f;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
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
}

.apple-filter-chip.active {
  background: linear-gradient(135deg, #007AFF 0%, #0051D5 100%);
  color: white;
  border-color: #007AFF;
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.4);
  transform: translateY(-2px);
}

.apple-filter-chip.active svg {
  stroke: white !important;
}

.apple-filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.apple-filter-label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 600;
  color: #86868b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-filter-label svg {
  width: 14px;
  height: 14px;
  stroke: #86868b;
  stroke-width: 2;
}

.apple-select {
  height: 34px;
  border-radius: 10px;
  border: 1.5px solid #e5e5e5;
  background: #f5f5f7;
  padding: 0 28px 0 12px;
  font-size: 12px;
  color: #1d1d1f;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s ease;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2386868b' stroke-width='2'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
}

.apple-select:hover {
  border-color: #d1d1d6;
  background-color: white;
}

.apple-select:focus {
  outline: none;
  border-color: #8BC34A;
  box-shadow: 0 0 0 3px rgba(139, 195, 74, 0.1);
}

.apple-clear-filters-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 12px;
  border-radius: 12px;
  border: 1.5px solid rgba(255, 59, 48, 0.3);
  background: rgba(255, 59, 48, 0.08);
  color: #FF3B30;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-clear-filters-btn svg {
  width: 14px;
  height: 14px;
  stroke: #FF3B30;
  stroke-width: 2;
}

.apple-clear-filters-btn:hover {
  background: rgba(255, 59, 48, 0.15);
  border-color: #FF3B30;
  transform: translateY(-2px);
}

/* ====================== APPLE CONTENT WRAPPER ====================== */
.apple-content-wrapper {
  padding: 0;
  overflow-x: hidden;
}

/* ====================== APPLE TERRITORIO BANNER ====================== */
.apple-territorio-banner {
  background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%);
  color: white;
  padding: 12px 20px;
  border-radius: 16px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 600;
}

.apple-territorio-banner svg {
  width: 18px;
  height: 18px;
  stroke: white;
}

/* ====================== APPLE FIRMA BAR ====================== */
.apple-firma-bar {
  background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
  border-radius: 16px;
  padding: 14px 20px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  box-shadow: 0 4px 20px rgba(0, 122, 255, 0.25);
}

.apple-firma-info {
  display: flex;
  align-items: center;
  gap: 12px;
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 500;
}

.apple-firma-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.apple-firma-icon svg {
  width: 18px;
  height: 18px;
  stroke: white;
}

.apple-firma-actions {
  display: flex;
  gap: 8px;
}

.apple-btn-deselect {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 12px;
  border: 1.5px solid rgba(255, 255, 255, 0.4);
  background: rgba(255, 255, 255, 0.15);
  color: white;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-btn-deselect svg {
  width: 14px;
  height: 14px;
  stroke: white;
}

.apple-btn-deselect:hover {
  background: rgba(255, 255, 255, 0.25);
}

.apple-btn-firmar {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 12px;
  border: none;
  background: white;
  color: #007AFF;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.25s ease;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.apple-btn-firmar svg {
  width: 14px;
  height: 14px;
  stroke: #007AFF;
}

.apple-btn-firmar:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Transition */
.apple-slide-enter-active,
.apple-slide-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-slide-enter-from,
.apple-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* ====================== APPLE TABLE ====================== */
.apple-table-container {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.04);
  max-height: calc(100vh - 380px);
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
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
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

.apple-table-row.apple-row-firmado {
  background: rgba(52, 199, 89, 0.05);
}

.apple-table-row.apple-row-seleccionado {
  background: rgba(0, 122, 255, 0.08);
  border-left: 3px solid #007AFF;
}

.apple-table td {
  padding: 16px 20px;
  font-size: 13px;
  color: #1D1D1F;
  border-left: 2px solid transparent;
  transition: all 0.15s ease;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-table-row:hover td:first-child {
  border-left-color: #8BC34A;
}

.th-checkbox,
.td-checkbox {
  width: 40px;
  text-align: center;
}

.apple-checkbox {
  width: 18px;
  height: 18px;
  accent-color: #8BC34A;
  cursor: pointer;
}

/* ====================== APPLE STATUS BADGE ====================== */
.apple-status-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.apple-status-badge svg {
  width: 14px;
  height: 14px;
}

.apple-status-badge.firmado {
  background: rgba(52, 199, 89, 0.1);
  color: #34C759;
}

.apple-status-badge.firmado svg {
  stroke: #34C759;
}

.apple-status-badge.pendiente {
  background: rgba(255, 149, 0, 0.1);
  color: #FF9500;
}

.apple-status-badge.pendiente svg {
  stroke: #FF9500;
}

/* ====================== APPLE USER CELL ====================== */
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

.apple-user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.apple-user-name {
  font-size: 13px;
  font-weight: 600;
  color: #1d1d1f;
}

.apple-user-role {
  font-size: 11px;
  color: #86868b;
  font-style: italic;
}

/* ====================== APPLE BADGES ====================== */
/* ====================== APPLE TERRITORIO BADGE ====================== */
.apple-territorio-badge {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 8px;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.3px;
  white-space: normal;
  word-wrap: break-word;
  line-height: 1.4;
  text-align: center;
}

.apple-territorio-badge.territorio-blue {
  background: linear-gradient(135deg, rgba(0, 122, 255, 0.15) 0%, rgba(0, 102, 204, 0.12) 100%);
  color: #007AFF;
  border: 1px solid rgba(0, 122, 255, 0.2);
}

.apple-territorio-badge.territorio-emerald {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.12) 100%);
  color: #059669;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.apple-territorio-badge.territorio-violet {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(124, 58, 237, 0.12) 100%);
  color: #7C3AED;
  border: 1px solid rgba(139, 92, 246, 0.2);
}

.apple-territorio-badge.territorio-orange {
  background: linear-gradient(135deg, rgba(249, 115, 22, 0.15) 0%, rgba(234, 88, 12, 0.12) 100%);
  color: #EA580C;
  border: 1px solid rgba(249, 115, 22, 0.2);
}

.apple-territorio-badge.territorio-cyan {
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(8, 145, 178, 0.12) 100%);
  color: #0891B2;
  border: 1px solid rgba(6, 182, 212, 0.2);
}

.apple-territorio-badge.territorio-rose {
  background: linear-gradient(135deg, rgba(244, 63, 94, 0.15) 0%, rgba(225, 29, 72, 0.12) 100%);
  color: #E11D48;
  border: 1px solid rgba(244, 63, 94, 0.2);
}

.apple-territorio-badge.territorio-amber {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.12) 100%);
  color: #D97706;
  border: 1px solid rgba(245, 158, 11, 0.2);
}

.apple-territorio-badge.territorio-teal {
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.15) 0%, rgba(13, 148, 136, 0.12) 100%);
  color: #0D9488;
  border: 1px solid rgba(20, 184, 166, 0.2);
}

.apple-territorio-badge.territorio-indigo {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(79, 70, 229, 0.12) 100%);
  color: #4F46E5;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.apple-territorio-badge.territorio-lime {
  background: linear-gradient(135deg, rgba(132, 204, 22, 0.15) 0%, rgba(101, 163, 13, 0.12) 100%);
  color: #65A30D;
  border: 1px solid rgba(132, 204, 22, 0.2);
}

.apple-territorio-badge.territorio-pink {
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.15) 0%, rgba(219, 39, 119, 0.12) 100%);
  color: #DB2777;
  border: 1px solid rgba(236, 72, 153, 0.2);
}

.apple-territorio-badge.territorio-sky {
  background: linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(2, 132, 199, 0.12) 100%);
  color: #0284C7;
  border: 1px solid rgba(14, 165, 233, 0.2);
}

.apple-territorio-badge.territorio-gray {
  background: linear-gradient(135deg, rgba(107, 114, 128, 0.15) 0%, rgba(75, 85, 99, 0.12) 100%);
  color: #4B5563;
  border: 1px solid rgba(107, 114, 128, 0.2);
}

.apple-territorio-badge.territorio-red {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(220, 38, 38, 0.12) 100%);
  color: #DC2626;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.apple-territorio-badge.territorio-green {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(22, 163, 74, 0.12) 100%);
  color: #16A34A;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.apple-territorio-badge.territorio-purple {
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(147, 51, 234, 0.12) 100%);
  color: #9333EA;
  border: 1px solid rgba(168, 85, 247, 0.2);
}

.apple-territorio-badge.territorio-yellow {
  background: linear-gradient(135deg, rgba(234, 179, 8, 0.18) 0%, rgba(202, 138, 4, 0.15) 100%);
  color: #B45309;
  border: 1px solid rgba(234, 179, 8, 0.25);
}

.apple-territorio-badge.territorio-fuchsia {
  background: linear-gradient(135deg, rgba(217, 70, 239, 0.15) 0%, rgba(192, 38, 211, 0.12) 100%);
  color: #C026D3;
  border: 1px solid rgba(217, 70, 239, 0.2);
}

.apple-territorio-badge.territorio-slate {
  background: linear-gradient(135deg, rgba(100, 116, 139, 0.15) 0%, rgba(71, 85, 105, 0.12) 100%);
  color: #475569;
  border: 1px solid rgba(100, 116, 139, 0.2);
}

.apple-territorio-badge.territorio-zinc {
  background: linear-gradient(135deg, rgba(113, 113, 122, 0.15) 0%, rgba(82, 82, 91, 0.12) 100%);
  color: #52525B;
  border: 1px solid rgba(113, 113, 122, 0.2);
}

.apple-territorio-badge.territorio-stone {
  background: linear-gradient(135deg, rgba(120, 113, 108, 0.15) 0%, rgba(87, 83, 78, 0.12) 100%);
  color: #57534E;
  border: 1px solid rgba(120, 113, 108, 0.2);
}

.apple-territorio-badge.territorio-coral {
  background: linear-gradient(135deg, rgba(251, 113, 133, 0.15) 0%, rgba(244, 63, 94, 0.12) 100%);
  color: #E11D48;
  border: 1px solid rgba(251, 113, 133, 0.2);
}

.apple-territorio-badge.territorio-mint {
  background: linear-gradient(135deg, rgba(52, 211, 153, 0.15) 0%, rgba(16, 185, 129, 0.12) 100%);
  color: #059669;
  border: 1px solid rgba(52, 211, 153, 0.2);
}

.apple-territorio-badge.territorio-navy {
  background: linear-gradient(135deg, rgba(30, 58, 138, 0.18) 0%, rgba(30, 64, 175, 0.15) 100%);
  color: #1E3A8A;
  border: 1px solid rgba(30, 58, 138, 0.25);
}

.apple-territorio-badge.territorio-gold {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.18) 0%, rgba(245, 158, 11, 0.15) 100%);
  color: #B45309;
  border: 1px solid rgba(251, 191, 36, 0.25);
}

.apple-territorio-badge.territorio-crimson {
  background: linear-gradient(135deg, rgba(190, 18, 60, 0.15) 0%, rgba(159, 18, 57, 0.12) 100%);
  color: #9F1239;
  border: 1px solid rgba(190, 18, 60, 0.2);
}

.apple-territorio-badge.territorio-forest {
  background: linear-gradient(135deg, rgba(21, 128, 61, 0.15) 0%, rgba(22, 101, 52, 0.12) 100%);
  color: #166534;
  border: 1px solid rgba(21, 128, 61, 0.2);
}

.apple-territorio-badge.territorio-plum {
  background: linear-gradient(135deg, rgba(126, 34, 206, 0.15) 0%, rgba(107, 33, 168, 0.12) 100%);
  color: #7E22CE;
  border: 1px solid rgba(126, 34, 206, 0.2);
}

.apple-territorio-badge.territorio-bronze {
  background: linear-gradient(135deg, rgba(180, 83, 9, 0.18) 0%, rgba(146, 64, 14, 0.15) 100%);
  color: #92400E;
  border: 1px solid rgba(180, 83, 9, 0.25);
}

.apple-territorio-badge.territorio-ocean {
  background: linear-gradient(135deg, rgba(3, 105, 161, 0.15) 0%, rgba(7, 89, 133, 0.12) 100%);
  color: #0369A1;
  border: 1px solid rgba(3, 105, 161, 0.2);
}

.apple-territorio-badge.territorio-wine {
  background: linear-gradient(135deg, rgba(136, 19, 55, 0.15) 0%, rgba(157, 23, 77, 0.12) 100%);
  color: #881337;
  border: 1px solid rgba(136, 19, 55, 0.2);
}

.apple-territorio-badge.territorio-charcoal {
  background: linear-gradient(135deg, rgba(38, 38, 38, 0.15) 0%, rgba(23, 23, 23, 0.12) 100%);
  color: #262626;
  border: 1px solid rgba(38, 38, 38, 0.2);
}

.apple-periodo-badge {
  display: inline-block;
  padding: 5px 10px;
  background: rgba(175, 82, 222, 0.1);
  color: #AF52DE;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.apple-reporte-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.apple-reporte-nombre {
  font-weight: 600;
  color: #1d1d1f;
  font-size: 13px;
}

.apple-firma-label {
  font-size: 11px;
  color: #34C759;
  font-weight: 500;
}

.apple-fecha-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.apple-fecha-text {
  display: inline-block;
  padding: 5px 10px;
  background: rgba(0, 122, 255, 0.1);
  color: #007AFF;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.apple-fecha-firma {
  font-size: 11px;
  color: #86868b;
}

/* ====================== APPLE ACTIONS ====================== */
.apple-actions {
  display: flex;
  gap: 8px;
}

.apple-action-btn {
  min-width: 36px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-action-btn svg {
  width: 18px;
  height: 18px;
  stroke-width: 2.5;
  fill: none;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.apple-action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.apple-action-btn.sign {
  background: linear-gradient(135deg, #007AFF 0%, #5AC8FA 100%);
  box-shadow: 0 2px 8px rgba(0, 122, 255, 0.25);
}

.apple-action-btn.sign svg {
  stroke: white;
}

.apple-action-btn.sign:hover:not(:disabled) {
  transform: scale(1.1);
  box-shadow: 0 4px 14px rgba(0, 122, 255, 0.4);
  background: linear-gradient(135deg, #0051D5 0%, #4AB8F1 100%);
}

.apple-action-btn.view {
  background: linear-gradient(135deg, #34C759 0%, #30D158 100%);
  box-shadow: 0 2px 8px rgba(52, 199, 89, 0.25);
}

.apple-action-btn.view svg {
  stroke: white;
}

.apple-action-btn.view:hover:not(:disabled) {
  transform: scale(1.1);
  box-shadow: 0 4px 14px rgba(52, 199, 89, 0.4);
  background: linear-gradient(135deg, #28A745 0%, #2ECC40 100%);
}

.apple-action-btn.download {
  background: linear-gradient(135deg, #5856D6 0%, #AF52DE 100%);
  box-shadow: 0 2px 8px rgba(88, 86, 214, 0.25);
}

.apple-action-btn.download svg {
  stroke: white;
}

.apple-action-btn.download:hover:not(:disabled) {
  transform: scale(1.1);
  box-shadow: 0 4px 14px rgba(88, 86, 214, 0.4);
  background: linear-gradient(135deg, #4030A0 0%, #9030C0 100%);
}

.apple-action-btn.delete {
  background: linear-gradient(135deg, #FF3B30 0%, #FF453A 100%);
  box-shadow: 0 2px 8px rgba(255, 59, 48, 0.25);
}

.apple-action-btn.delete svg {
  stroke: white;
}

.apple-action-btn.delete:hover:not(:disabled) {
  transform: scale(1.1);
  box-shadow: 0 4px 14px rgba(255, 59, 48, 0.4);
  background: linear-gradient(135deg, #D93025 0%, #EA4335 100%);
}

.apple-spinner-mini {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: apple-spin-animation 0.8s linear infinite;
}

/* ====================== APPLE LOADING & EMPTY ====================== */
.apple-loading,
.apple-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #86868b;
  text-align: center;
}

.apple-loading svg,
.apple-empty svg {
  width: 60px;
  height: 60px;
  stroke: #d1d1d6;
  margin-bottom: 16px;
}

.apple-loading h3,
.apple-empty h3 {
  font-size: 16px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0 0 8px;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-loading p,
.apple-empty p {
  font-size: 13px;
  color: #86868b;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(139, 195, 74, 0.2);
  border-top-color: #8BC34A;
  border-radius: 50%;
  animation: apple-spin-animation 1s linear infinite;
  margin-bottom: 16px;
}

/* ====================== APPLE PAGINATION ====================== */
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

.apple-pagination-info {
  font-size: 12px;
  color: #2E7D32;
  font-weight: 500;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
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
  color: #1d1d1f;
  cursor: pointer;
  transition: all 0.2s;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-pagination-number:hover {
  background: rgba(139, 195, 74, 0.15);
}

.apple-pagination-number.active {
  background: linear-gradient(135deg, #8BC34A 0%, #66BB6A 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(139, 195, 74, 0.4);
}

/* ====================== RESPONSIVE DESIGN ====================== */
@media (max-width: 1024px) {
  .apple-stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .apple-unified-filters {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  
  .apple-filter-group {
    flex-wrap: wrap;
  }
}

@media (max-width: 768px) {
  .apple-container {
    padding: 12px;
  }
  
  .apple-page-header {
    padding: clamp(14px, 2.5vw, 18px);
    border-radius: 24px 24px 0 0;
  }
  
  .apple-stats-section {
    padding: 14px 12px 12px 12px;
    border-radius: 0 0 24px 24px;
  }
  
  .apple-stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }
  
  .apple-stat-card {
    padding: 10px;
    gap: 8px;
  }
  
  .apple-stat-icon {
    width: 30px;
    height: 30px;
  }
  
  .apple-stat-icon svg {
    width: 14px;
    height: 14px;
  }
  
  .apple-stat-value {
    font-size: 14px;
  }
  
  .apple-stat-label {
    font-size: 9px;
  }
  
  .apple-search-row {
    flex-direction: column;
  }
  
  .apple-search-container {
    min-width: 100%;
  }
  
  .apple-filter-controls {
    width: 100%;
    justify-content: space-between;
  }
  
  .apple-quick-filters {
    flex-wrap: wrap;
  }
  
  .apple-filter-chip {
    flex: 1;
    justify-content: center;
    min-width: 80px;
  }
  
  .apple-table-container {
    max-height: calc(100vh - 450px);
  }
  
  .apple-table th,
  .apple-table td {
    padding: 10px 8px;
    font-size: 11px;
  }
  
  .th-territorio,
  .td-territorio,
  .th-periodo,
  .td-periodo {
    display: none;
  }
  
  .apple-user-cell {
    flex-direction: row;
    align-items: center;
    gap: 8px;
  }
  
  .apple-avatar {
    width: 32px;
    height: 32px;
  }
  
  .apple-avatar svg {
    width: 18px;
    height: 18px;
  }
  
  .apple-action-btn {
    min-width: 32px;
    width: 32px;
    height: 32px;
  }
  
  .apple-action-btn svg {
    width: 16px;
    height: 16px;
  }
  
  .apple-pagination {
    flex-direction: column;
    gap: 10px;
    text-align: center;
  }
  
  .apple-pagination-numbers {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .apple-orb-1, .apple-orb-2, .apple-orb-3 {
    opacity: 0.4;
  }
  
  .apple-firma-bar {
    flex-direction: column;
    text-align: center;
  }
  
  .apple-firma-actions {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .apple-stats-grid {
    grid-template-columns: 1fr 1fr;
    gap: 6px;
  }
  
  .apple-stat-card {
    padding: 10px;
    flex-direction: column;
    text-align: center;
    gap: 6px;
    border-radius: 16px;
  }
  
  .apple-stat-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
  }
  
  .apple-stat-value {
    font-size: 18px;
    font-weight: 700;
  }
  
  .apple-stat-label {
    font-size: 10px;
    letter-spacing: 0.02em;
  }
  
  .apple-header-title {
    font-size: clamp(1rem, 4vw, 1.2rem);
  }
  
  .apple-refresh-btn {
    width: 34px;
    height: 34px;
  }
  
  /* Tabla responsiva estilo Apple - Cards en móvil */
  .apple-table-wrapper {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  .apple-table th,
  .apple-table td {
    padding: 10px 8px;
    font-size: 11px;
  }
  
  .th-checkbox,
  .td-checkbox {
    width: 32px;
    padding: 8px 4px !important;
  }
  
  .apple-checkbox {
    width: 18px;
    height: 18px;
    border-radius: 5px;
  }
  
  /* Botones de acción mejorados para móvil */
  .apple-actions {
    gap: 6px;
    flex-wrap: nowrap;
  }
  
  .apple-action-btn {
    width: 32px;
    height: 32px;
    min-width: 32px;
    border-radius: 10px;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  .apple-action-btn:active {
    transform: scale(0.92);
  }
  
  .apple-action-btn svg {
    width: 15px;
    height: 15px;
  }
  
  .apple-filter-btn {
    padding: 8px 12px;
    font-size: 12px;
    border-radius: 10px;
  }
  
  .apple-filter-controls {
    gap: 8px;
  }
  
  .apple-filter-btn span {
    display: none;
  }
  
  .apple-filter-btn svg {
    margin: 0;
  }
  
  /* User cell compacto */
  .apple-user-cell {
    min-width: 120px;
  }
  
  .apple-user-name {
    font-size: 12px;
    max-width: 100px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .apple-user-role {
    display: none;
  }
  
  /* Status badge compacto */
  .apple-status-badge span {
    display: none;
  }
  
  .apple-status-badge {
    padding: 6px;
    min-width: auto;
  }
  
  .apple-status-badge svg {
    width: 16px;
    height: 16px;
  }
  
  /* Territorio badge compacto */
  .apple-territorio-badge {
    font-size: 9px;
    padding: 4px 8px;
    max-width: 80px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  /* Periodo badge compact */
  .apple-periodo-badge {
    font-size: 10px;
    padding: 4px 8px;
  }
}

/* ====================== MODALS ====================== */
.modal-overlay { position: fixed; inset: 0; background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; padding: 16px; z-index: 1000; }

.modal-container { background: white; border-radius: 16px; max-width: 420px; width: 100%; box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2); overflow: hidden; animation: modalSlideIn 0.3s ease-out; }

@keyframes modalSlideIn { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

.modal-header { display: flex; align-items: center; gap: 14px; padding: 18px; }

.modal-header.delete-header { background: linear-gradient(135deg, #fef2f2, #fee2e2); border-bottom: 1px solid #fecaca; }

.modal-icon { width: 44px; height: 44px; min-width: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }

.modal-icon.delete-icon { background: #fee2e2; color: #dc2626; }

.modal-icon svg { width: 22px; height: 22px; max-width: 22px; max-height: 22px; flex-shrink: 0; }

.modal-title-container h3 { font-size: 1.1rem; font-weight: 600; color: #1a1a1a; margin: 0; font-family: 'Inter', sans-serif; }

.modal-title-container p { font-size: 0.8rem; color: #6b7280; margin: 4px 0 0; font-family: 'Inter', sans-serif; }

.modal-body { padding: 18px; font-family: 'Inter', sans-serif; }

.modal-body p { margin: 0 0 12px; color: #374151; font-size: 0.875rem; line-height: 1.5; }

.reporte-eliminar-info { background: #f9fafb; padding: 12px; border-radius: 8px; border: 1px solid #e5e7eb; }

.reporte-eliminar-info strong { display: block; color: #1a1a1a; font-size: 0.9rem; }

.reporte-eliminar-info span { font-size: 0.8rem; color: #6b7280; }

.modal-footer { display: flex; gap: 10px; padding: 14px 18px; background: #f9fafb; border-top: 1px solid #e5e7eb; }

.btn-cancel { flex: 1; padding: 10px 16px; background: white; border: 1.5px solid #d1d5db; border-radius: 8px; font-size: 0.875rem; font-weight: 500; color: #374151; cursor: pointer; transition: all 0.2s; font-family: 'Inter', sans-serif; }

.btn-cancel:hover { background: #f3f4f6; border-color: #9ca3af; }

.btn-delete-confirm { flex: 1; display: flex; align-items: center; justify-content: center; gap: 8px; padding: 10px 16px; background: linear-gradient(135deg, #dc2626, #b91c1c); border: none; border-radius: 8px; font-size: 0.875rem; font-weight: 600; color: white; cursor: pointer; transition: all 0.2s; font-family: 'Inter', sans-serif; }

.btn-delete-confirm:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(220, 38, 38, 0.4); background: linear-gradient(135deg, #b91c1c, #991b1b); }

.btn-delete-confirm:disabled { opacity: 0.7; cursor: not-allowed; }

.btn-delete-confirm svg { width: 16px; height: 16px; max-width: 16px; max-height: 16px; }

.modal-fade-enter-active, .modal-fade-leave-active { transition: all 0.3s ease; }

.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

.modal-fade-enter-from .modal-container, .modal-fade-leave-to .modal-container { transform: scale(0.95) translateY(10px); }

/* ==========================================
   ESTILOS PARA SISTEMA DE FIRMAS
   ========================================== */

/* Checkbox column styles */
.th-checkbox, .td-checkbox {
  width: 40px;
  text-align: center;
  padding: 8px !important;
}

.th-checkbox input[type="checkbox"],
.td-checkbox input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #4CAF50;
  border-radius: 4px;
}

.th-checkbox input[type="checkbox"]:disabled,
.td-checkbox input[type="checkbox"]:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

/* Estado column styles */
.th-estado, .td-estado {
  width: 100px;
  text-align: center;
}

.estado-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 600;
  white-space: nowrap;
}

.estado-badge.firmado {
  background: linear-gradient(135deg, #dcfce7, #bbf7d0);
  color: #15803d;
}

.estado-badge.pendiente {
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  color: #b45309;
}

.estado-badge svg {
  width: 12px;
  height: 12px;
}

/* Row states */
.row-firmado {
  background: rgba(220, 252, 231, 0.3) !important;
}

.row-seleccionado {
  background: rgba(59, 130, 246, 0.1) !important;
}

.reportes-table tbody tr.row-firmado:hover {
  background: rgba(220, 252, 231, 0.5) !important;
}

.reportes-table tbody tr.row-seleccionado:hover {
  background: rgba(59, 130, 246, 0.15) !important;
}

/* Action buttons for firma */
.btn-sign {
  background: #f0fdf4;
  border-color: #86efac;
  color: #16a34a;
}

.btn-sign:hover:not(:disabled) {
  background: #dcfce7;
  transform: translateY(-1px);
}

.btn-protected {
  background: #f3f4f6;
  border-color: #d1d5db;
  color: #9ca3af;
  cursor: not-allowed !important;
}

/* Firma info tooltip */
.firma-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.firma-info .nombre-supervisor {
  font-weight: 600;
  color: #15803d;
  font-size: 0.75rem;
}

.fecha-firma {
  font-size: 0.65rem;
  color: #6b7280;
}

/* ==========================================
   BARRA DE ACCIONES DE FIRMA FLOTANTE
   ========================================== */

.firma-actions-bar {
  position: sticky;
  top: 0;
  background: linear-gradient(135deg, #15803d 0%, #22c55e 50%, #16a34a 100%);
  padding: clamp(10px, 1.2vw, 14px) clamp(16px, 2vw, 20px);
  border-radius: 12px;
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 14px;
  box-shadow: 0 4px 16px rgba(34, 197, 94, 0.3), 0 2px 6px rgba(0, 0, 0, 0.08);
  z-index: 10;
  animation: slideDown 0.3s ease-out;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

@keyframes slideDown {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.firma-actions-bar .firma-actions-info {
  display: flex;
  align-items: center;
  gap: 10px;
  color: white;
  font-size: clamp(0.75rem, 1vw, 0.85rem);
  font-weight: 500;
}

.firma-actions-bar .firma-actions-info svg {
  width: clamp(18px, 2vw, 20px);
  height: clamp(18px, 2vw, 20px);
  flex-shrink: 0;
}

.firma-actions-bar .firma-actions-info span {
  font-weight: 400;
  letter-spacing: 0.2px;
}

.firma-actions-bar .firma-actions-info strong {
  font-weight: 700;
  font-size: clamp(0.85rem, 1.1vw, 0.95rem);
  margin-right: 2px;
}

.firma-actions-bar .firma-actions-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
}

.btn-firmar-seleccionados {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: clamp(8px, 1vw, 10px) clamp(14px, 1.8vw, 18px);
  background: white;
  border: none;
  border-radius: 8px;
  color: #15803d;
  font-size: clamp(0.72rem, 1vw, 0.8rem);
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'Inter', sans-serif;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.12);
}

.btn-firmar-seleccionados:hover {
  background: #f0fdf4;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.18);
}

.btn-firmar-seleccionados svg {
  width: clamp(15px, 1.8vw, 17px);
  height: clamp(15px, 1.8vw, 17px);
  color: #16a34a;
}

.btn-deselect {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: clamp(8px, 1vw, 10px) clamp(12px, 1.6vw, 16px);
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 8px;
  color: white;
  font-size: clamp(0.72rem, 1vw, 0.8rem);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'Inter', sans-serif;
}

.btn-deselect:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: white;
  transform: translateY(-1px);
}

.btn-deselect svg {
  width: clamp(14px, 1.6vw, 15px);
  height: clamp(14px, 1.6vw, 15px);
}

/* ==========================================
   BOTONES SELECCIONAR TODOS EN HEADER
   ========================================== */

.header-actions-buttons {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.btn-firmar-todos {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 11px 20px;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  border: none;
  color: white;
  box-shadow: 0 3px 10px rgba(34, 197, 94, 0.25);
  white-space: nowrap;
  letter-spacing: 0.01em;
}

.btn-firmar-todos:hover:not(:disabled) {
  background: linear-gradient(135deg, #16a34a, #15803d);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(34, 197, 94, 0.4);
}

.btn-firmar-todos:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(34, 197, 94, 0.3);
}

.btn-firmar-todos:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-firmar-todos svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  stroke-width: 2.5;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.15));
  stroke: rgba(230, 240, 255, 0.95);
  color: rgba(230, 240, 255, 0.95);
}

.btn-descargar-reportes {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 11px 20px;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border: none;
  color: white;
  box-shadow: 0 3px 10px rgba(59, 130, 246, 0.25);
  white-space: nowrap;
  letter-spacing: 0.01em;
}

.btn-descargar-reportes:hover {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
}

.btn-descargar-reportes:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.btn-descargar-reportes svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  stroke-width: 2.5;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.15));
  stroke: rgba(219, 234, 254, 0.95);
  color: rgba(219, 234, 254, 0.95);
}

/* ==========================================
   MODAL DE FIRMA
   ========================================== */

.modal-firma {
  max-width: 520px;
  width: 95%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.firma-header {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-bottom: 1px solid rgba(22, 163, 74, 0.2);
}

.firma-icon {
  background: #dcfce7;
  color: #16a34a;
}

.modal-firma .modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.reportes-a-firmar {
  margin-bottom: 16px;
}

.reportes-a-firmar h4 {
  font-size: 0.85rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.reportes-list-scroll {
  max-height: 150px;
  overflow-y: auto;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  padding: 8px;
}

.reporte-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  background: white;
  border-radius: 6px;
  margin-bottom: 6px;
  border: 1px solid #e5e7eb;
  font-size: 0.8rem;
}

.reporte-item:last-child {
  margin-bottom: 0;
}

.reporte-item svg {
  width: 16px;
  height: 16px;
  color: #16a34a;
  flex-shrink: 0;
}

.reporte-item .reporte-info {
  flex: 1;
  min-width: 0;
}

.reporte-item .reporte-nombre {
  font-weight: 600;
  color: #374151;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.reporte-item .reporte-usuario {
  font-size: 0.7rem;
  color: #6b7280;
}

/* Firma container */
.firma-container {
  margin-top: 12px;
}

.firma-container h4 {
  font-size: 0.85rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}

/* Botón cerrar modal */
.modal-close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 32px;
  height: 32px;
  border: none;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  color: #6b7280;
}

.modal-close-btn:hover {
  background: rgba(0, 0, 0, 0.1);
  color: #374151;
}

/* Items de reporte en el modal */
.reporte-item-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #dcfce7, #bbf7d0);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.reporte-item-icon svg {
  color: #16a34a;
}

.reporte-item-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.reporte-item-nombre {
  font-weight: 600;
  color: #374151;
  font-size: 0.8rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.reporte-item-usuario {
  font-size: 0.7rem;
  color: #6b7280;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Header del modal firma con posición relativa para el botón de cerrar */
.modal-firma .firma-header {
  position: relative;
  padding-right: 50px;
}

/* Modal footer para firma */
.modal-firma .modal-footer {
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  padding: 14px 16px;
}

.btn-firmar-confirm {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'Inter', sans-serif;
}

.btn-firmar-confirm:hover:not(:disabled) {
  background: linear-gradient(135deg, #16a34a, #15803d);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(34, 197, 94, 0.4);
}

.btn-firmar-confirm:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-firmar-confirm svg {
  width: 16px;
  height: 16px;
}

/* ==========================================
   MODAL DE ÉXITO
   ========================================== */

.modal-exito {
  max-width: 400px;
  text-align: center;
}

.exito-header {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-bottom: 1px solid rgba(22, 163, 74, 0.2);
  flex-direction: column;
  padding: 24px 18px 16px;
}

.exito-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
  animation: successPop 0.4s ease-out;
}

.exito-icon svg {
  width: 32px;
  height: 32px;
  color: white;
}

@keyframes successPop {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.modal-exito .modal-title-container {
  text-align: center;
}

.modal-exito .modal-title-container h3 {
  color: #15803d;
  font-size: 1.2rem;
}

.modal-exito .modal-body {
  padding: 20px;
}

.resultado-firma {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.resultado-stat {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 12px 16px;
  background: #f0fdf4;
  border-radius: 10px;
  border: 1px solid #dcfce7;
}

.resultado-stat svg {
  width: 24px;
  height: 24px;
  color: #16a34a;
}

.resultado-stat span {
  font-size: 1rem;
  font-weight: 600;
  color: #15803d;
}

.modal-exito .modal-footer {
  justify-content: center;
  padding: 16px 20px 20px;
  background: white;
  border-top: none;
}

.modal-exito .modal-footer.centered {
  justify-content: center;
}

.modal-exito .modal-body.text-center {
  text-align: center;
}

.exito-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #15803d;
  margin: 0 0 12px;
  font-family: 'Inter', sans-serif;
}

.exito-message {
  font-size: 0.95rem;
  color: #374151;
  margin: 0 0 8px;
  font-family: 'Inter', sans-serif;
}

.exito-warning {
  font-size: 0.85rem;
  color: #b45309;
  background: #fef3c7;
  padding: 8px 12px;
  border-radius: 8px;
  margin: 12px 0 0;
  font-family: 'Inter', sans-serif;
}

.btn-exito-ok {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 40px;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  border: none;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'Inter', sans-serif;
}

.btn-exito-ok:hover {
  background: linear-gradient(135deg, #16a34a, #15803d);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(34, 197, 94, 0.4);
}

.btn-cerrar-exito {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 32px;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  border: none;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'Inter', sans-serif;
}

.btn-cerrar-exito:hover {
  background: linear-gradient(135deg, #16a34a, #15803d);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(34, 197, 94, 0.4);
}

.btn-cerrar-exito svg {
  width: 16px;
  height: 16px;
}

/* ==========================================
   MODAL DE DESCARGA - NUEVO DISEÑO
   ========================================== */

.modal-descarga {
  max-width: 480px;
  width: 95%;
  border-radius: 20px;
  overflow: visible;
  position: relative;
}

/* Botón cerrar circular en esquina superior derecha */
.btn-close-corner {
  position: absolute;
  top: -10px;
  right: -10px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  z-index: 10;
  transition: all 0.2s;
}

.btn-close-corner:hover {
  background: #f3f4f6;
  transform: scale(1.1);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2);
}

.btn-close-corner svg {
  color: #6b7280;
}

.btn-close-corner:hover svg {
  color: #ef4444;
}

.descarga-header {
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
  border-bottom: none;
  padding: 20px 24px;
  border-radius: 20px 20px 0 0;
}

.descarga-header .modal-title-container h3 {
  color: white;
  font-size: 1.1rem;
  text-shadow: none;
}

.descarga-header .modal-title-container p {
  color: rgba(255,255,255,0.8);
}

.descarga-icon {
  background: rgba(255,255,255,0.2);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.descarga-icon svg {
  color: white;
}

.descarga-header .btn-close-modal {
  color: white;
  background: rgba(255,255,255,0.15);
}

.descarga-header .btn-close-modal:hover {
  background: rgba(255,255,255,0.25);
}

.descarga-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Selectores de Período */
.periodo-selectors {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.periodo-grupo {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.periodo-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  color: #374151;
  font-family: 'Inter', sans-serif;
}

.periodo-label svg {
  color: #3b82f6;
}

.periodo-select {
  padding: 11px 14px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 0.875rem;
  font-family: 'Inter', sans-serif;
  color: #374151;
  background: #f9fafb;
  cursor: pointer;
  transition: all 0.2s;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 10px center;
  background-repeat: no-repeat;
  background-size: 16px;
}

.periodo-select:focus {
  outline: none;
  border-color: #3b82f6;
  background-color: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.periodo-select:hover {
  border-color: #3b82f6;
}

.periodo-select.select-required {
  border-color: #fca5a5;
  background-color: #fef2f2;
}

.periodo-select.select-required:hover {
  border-color: #f87171;
}

/* Aviso campos obligatorios */
.campos-obligatorios {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 1px solid #fcd34d;
  border-radius: 10px;
  padding: 12px 16px;
}

.campos-obligatorios svg {
  flex-shrink: 0;
  color: #d97706;
}

.campos-obligatorios span {
  font-size: 0.82rem;
  font-weight: 500;
  color: #92400e;
  font-family: 'Inter', sans-serif;
}

/* Tipo de Reportes Section */
.tipo-reportes-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  color: #374151;
  font-family: 'Inter', sans-serif;
}

.section-label svg {
  color: #3b82f6;
}

.tipo-reportes-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.tipo-card {
  position: relative;
  cursor: pointer;
}

.tipo-card input[type="radio"] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.tipo-card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 14px 10px;
  background: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  transition: all 0.2s;
}

.tipo-card:hover .tipo-card-content {
  border-color: #3b82f6;
  background: #f0f9ff;
}

.tipo-card.active .tipo-card-content {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

.tipo-icon {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.tipo-icon.todos {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #2563eb;
}

.tipo-icon.firmados {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  color: #16a34a;
}

.tipo-icon.pendientes {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #ca8a04;
}

.tipo-card.active .tipo-icon.todos {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.tipo-card.active .tipo-icon.firmados {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
}

.tipo-card.active .tipo-icon.pendientes {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.tipo-name {
  font-size: 0.75rem;
  font-weight: 600;
  color: #374151;
  font-family: 'Inter', sans-serif;
}

.tipo-card.active .tipo-name {
  color: #1f2937;
}

.tipo-count {
  font-size: 0.85rem;
  font-weight: 700;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
}

.tipo-card.active .tipo-count {
  color: #1e40af;
}

/* Resumen de descarga */
.descarga-resumen {
  display: flex;
  align-items: center;
  gap: 12px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border: 1px solid #bfdbfe;
  border-radius: 12px;
  padding: 14px 16px;
}

.descarga-resumen svg {
  flex-shrink: 0;
  color: #2563eb;
}

.resumen-texto {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 4px;
}

.resumen-cantidad {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e40af;
  font-family: 'Inter', sans-serif;
}

.resumen-descripcion {
  font-size: 0.85rem;
  color: #374151;
  font-family: 'Inter', sans-serif;
}

.descarga-vacio {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 24px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  text-align: center;
}

.descarga-vacio svg {
  color: #dc2626;
  opacity: 0.6;
}

.descarga-vacio p {
  margin: 0;
  font-size: 0.85rem;
  color: #991b1b;
  font-family: 'Inter', sans-serif;
}

/* Barra de progreso de descarga */
.descarga-progreso {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border: 1px solid #bfdbfe;
  border-radius: 12px;
  padding: 14px 16px;
  margin-top: 4px;
}

.progreso-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.progreso-texto {
  font-size: 0.8rem;
  color: #1e40af;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
}

.progreso-contador {
  font-size: 0.75rem;
  font-weight: 700;
  color: #3b82f6;
  background: white;
  padding: 2px 10px;
  border-radius: 10px;
  font-family: 'Inter', sans-serif;
}

.progreso-barra {
  width: 100%;
  height: 8px;
  background: #e0e7ff;
  border-radius: 4px;
  overflow: hidden;
}

.progreso-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #2563eb);
  border-radius: 4px;
  transition: width 0.3s ease;
}

/* Footer del modal de descarga */
.descarga-footer {
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
  padding: 16px 20px;
  gap: 12px;
}

.btn-descargar-confirm {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border: none;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'Inter', sans-serif;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.25);
  flex: 1;
}

.btn-descargar-confirm:hover:not(:disabled) {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
}

.btn-descargar-confirm:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.btn-descargar-confirm svg {
  width: 16px;
  height: 16px;
}

/* ==========================================
   RESPONSIVE PARA FIRMA
   ========================================== */

@media (max-width: 768px) {
  .firma-actions-bar {
    flex-direction: column;
    text-align: center;
    padding: clamp(10px, 2vw, 12px) clamp(12px, 2.5vw, 14px);
    gap: 10px;
  }
  
  .firma-actions-bar .firma-actions-info {
    font-size: clamp(0.72rem, 1.5vw, 0.8rem);
    justify-content: center;
  }

  .firma-actions-bar .firma-actions-info svg {
    width: 16px;
    height: 16px;
  }

  .firma-actions-bar .firma-actions-info strong {
    font-size: clamp(0.8rem, 1.7vw, 0.88rem);
  }
  
  .firma-actions-bar .firma-actions-buttons {
    width: 100%;
    justify-content: center;
  }

  .btn-firmar-seleccionados,
  .btn-deselect {
    font-size: 0.75rem;
    padding: 8px 14px;
  }
  
  .modal-firma {
    max-width: 95%;
  }
  
  .reportes-list-scroll {
    max-height: 120px;
  }
  
  .th-estado, .td-estado {
    display: none;
  }
  
  .btn-firmar-todos {
    padding: 8px 14px;
    font-size: 0.75rem;
  }
  
  .filters-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .filters-header .btn-firmar-todos {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .th-checkbox, .td-checkbox {
    width: 32px;
    padding: 6px !important;
  }
  
  .th-checkbox input[type="checkbox"],
  .td-checkbox input[type="checkbox"] {
    width: 16px;
    height: 16px;
  }
  
  .firma-actions-bar {
    position: fixed;
    bottom: 0;
    left: 60px;
    right: 0;
    top: auto;
    border-radius: 16px 16px 0 0;
    margin-bottom: 0;
    z-index: 100;
    padding: 16px;
  }
  
  .btn-firmar-seleccionados {
    padding: 10px 16px;
    font-size: 0.8rem;
  }
  
  .btn-deselect {
    padding: 10px 14px;
    font-size: 0.8rem;
  }
  
  .exito-icon {
    width: 50px;
    height: 50px;
  }
  
  .exito-icon svg {
    width: 26px;
    height: 26px;
  }

  .header-actions-buttons {
    width: 100%;
    justify-content: center;
  }

  .btn-firmar-todos,
  .btn-descargar-reportes {
    flex: 1;
    min-width: 0;
    font-size: 0.75rem;
    padding: 9px 14px;
  }

  .modal-descarga {
    max-width: 95%;
    margin: 10px;
  }

  .descarga-body {
    padding: 16px;
    gap: 16px;
  }

  .periodo-selectors {
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }

  .periodo-select {
    padding: 10px 12px;
    font-size: 0.82rem;
  }

  .tipo-reportes-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
  }

  .tipo-card-content {
    padding: 12px 8px;
    gap: 6px;
  }

  .tipo-icon {
    width: 36px;
    height: 36px;
  }

  .tipo-icon svg {
    width: 18px;
    height: 18px;
  }

  .tipo-name {
    font-size: 0.7rem;
  }

  .tipo-count {
    font-size: 0.8rem;
  }

  .descarga-resumen {
    padding: 12px;
  }

  .resumen-cantidad {
    font-size: 1rem;
  }

  .resumen-descripcion {
    font-size: 0.8rem;
  }

  .descarga-footer {
    padding: 14px 16px;
  }

  .btn-descargar-confirm {
    padding: 11px 20px;
    font-size: 0.82rem;
  }
}

@media (max-width: 480px) {
  .header-actions-buttons {
    flex-direction: column;
    width: 100%;
    gap: 8px;
  }

  .btn-firmar-todos,
  .btn-descargar-reportes {
    width: 100%;
    justify-content: center;
    font-size: 0.72rem;
    padding: 10px;
  }

  .modal-descarga {
    max-width: 98%;
    margin: 6px;
  }

  .descarga-header {
    padding: 16px;
  }

  .descarga-header .modal-title-container h3 {
    font-size: 1rem;
  }

  .descarga-body {
    padding: 14px;
    gap: 14px;
  }

  .periodo-selectors {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .periodo-label {
    font-size: 0.75rem;
  }

  .periodo-select {
    padding: 10px;
    font-size: 0.8rem;
  }

  .tipo-reportes-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
  }

  .tipo-card-content {
    padding: 10px 6px;
    gap: 4px;
    border-radius: 10px;
  }

  .tipo-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
  }

  .tipo-icon svg {
    width: 16px;
    height: 16px;
  }

  .tipo-name {
    font-size: 0.65rem;
  }

  .tipo-count {
    font-size: 0.72rem;
  }

  .descarga-resumen {
    padding: 10px 12px;
    flex-direction: column;
    text-align: center;
    gap: 8px;
  }

  .resumen-cantidad {
    font-size: 1.1rem;
  }

  .resumen-descripcion {
    font-size: 0.78rem;
  }

  .descarga-vacio {
    padding: 18px;
  }

  .descarga-vacio svg {
    width: 32px;
    height: 32px;
  }

  .descarga-vacio p {
    font-size: 0.8rem;
  }

  .descarga-footer {
    padding: 12px 14px;
    flex-direction: column;
  }

  .btn-cancel {
    order: 2;
  }

  .btn-descargar-confirm {
    order: 1;
    width: 100%;
    padding: 12px;
    font-size: 0.85rem;
  }
}

/* ====================== APPLE MINI MODAL DE CARGA ====================== */
.apple-mini-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 20px;
}

.apple-mini-modal {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border-radius: 28px;
  padding: 28px 32px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  box-shadow: 
    0 30px 60px -15px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 1);
  min-width: 280px;
  max-width: 340px;
  animation: apple-modal-bounce 0.45s cubic-bezier(0.34, 1.56, 0.64, 1);
  overflow: hidden;
  position: relative;
}

@keyframes apple-modal-bounce {
  0% {
    opacity: 0;
    transform: scale(0.85) translateY(25px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.apple-mini-modal-spinner {
  position: relative;
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.apple-progress-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.apple-ring-bg {
  fill: none;
  stroke: #f0f0f5;
  stroke-width: 6;
}

.apple-ring-progress-real {
  fill: none;
  stroke: url(#green-gradient);
  stroke: #34C759;
  stroke-width: 6;
  stroke-linecap: round;
  stroke-dasharray: 264;
  stroke-dashoffset: 264;
  transition: stroke-dashoffset 0.3s ease-out;
}

.apple-mini-modal-percent {
  position: absolute;
  display: flex;
  align-items: baseline;
  justify-content: center;
  font-size: 28px;
  font-weight: 700;
  color: #1d1d1f;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
  letter-spacing: -0.03em;
}

.apple-mini-modal-percent span {
  font-size: 14px;
  font-weight: 600;
  color: #86868b;
  margin-left: 1px;
}

.apple-mini-modal-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  width: 100%;
}

.apple-mini-modal-action {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px;
  background: linear-gradient(135deg, #f8f9fa 0%, #f0f1f3 100%);
  border-radius: 20px;
}

.apple-mini-modal-action-icon {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.apple-mini-modal-action-icon.ver {
  background: linear-gradient(135deg, #34C759 0%, #30D158 100%);
}

.apple-mini-modal-action-icon.descargar {
  background: linear-gradient(135deg, #5856D6 0%, #AF52DE 100%);
}

.apple-mini-modal-action-icon svg {
  width: 16px;
  height: 16px;
  stroke: white;
  stroke-width: 2.5;
}

.apple-mini-modal-action span {
  font-size: 13px;
  font-weight: 600;
  color: #1d1d1f;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Inter', sans-serif;
  letter-spacing: -0.01em;
}

.apple-mini-modal-user {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border-radius: 16px;
  width: 100%;
  border: 1px solid rgba(59, 130, 246, 0.15);
}

.apple-mini-modal-avatar {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #007AFF 0%, #5AC8FA 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.apple-mini-modal-avatar svg {
  width: 24px;
  height: 24px;
  stroke: white;
  stroke-width: 2;
}

.apple-mini-modal-user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
  flex: 1;
}

.apple-mini-modal-user-info h4 {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: #1d1d1f;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
  letter-spacing: -0.02em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.apple-mini-modal-user-info p {
  margin: 0;
  font-size: 13px;
  font-weight: 500;
  color: #007AFF;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Inter', sans-serif;
}

.apple-mini-modal-progress-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: #e5e7eb;
}

.apple-mini-modal-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #34C759 0%, #30D158 50%, #32D74B 100%);
  transition: width 0.25s ease-out;
  border-radius: 0 2px 2px 0;
}

/* Transición del mini modal Apple */
.apple-mini-modal-enter-active {
  transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.apple-mini-modal-leave-active {
  transition: all 0.25s ease-out;
}

.apple-mini-modal-enter-from {
  opacity: 0;
}

.apple-mini-modal-enter-from .apple-mini-modal {
  transform: scale(0.85) translateY(25px);
}

.apple-mini-modal-leave-to {
  opacity: 0;
}

.apple-mini-modal-leave-to .apple-mini-modal {
  transform: scale(0.95) translateY(-15px);
}

/* Responsive del mini modal */
@media (max-width: 480px) {
  .apple-mini-modal {
    padding: 24px 20px 16px;
    min-width: 260px;
    max-width: 300px;
    border-radius: 24px;
  }
  
  .apple-mini-modal-spinner {
    width: 80px;
    height: 80px;
  }
  
  .apple-mini-modal-percent {
    font-size: 24px;
  }
  
  .apple-mini-modal-percent span {
    font-size: 12px;
  }
  
  .apple-mini-modal-action {
    padding: 6px 12px;
  }
  
  .apple-mini-modal-action-icon {
    width: 24px;
    height: 24px;
  }
  
  .apple-mini-modal-action-icon svg {
    width: 14px;
    height: 14px;
  }
  
  .apple-mini-modal-action span {
    font-size: 12px;
  }
  
  .apple-mini-modal-user {
    padding: 10px 12px;
  }
  
  .apple-mini-modal-avatar {
    width: 38px;
    height: 38px;
  }
  
  .apple-mini-modal-avatar svg {
    width: 20px;
    height: 20px;
  }
  
  .apple-mini-modal-user-info h4 {
    font-size: 14px;
  }
  
  .apple-mini-modal-user-info p {
    font-size: 12px;
  }
}

/* ====================== APPLE SUCCESS MODAL (Descarga Exitosa) ====================== */
.apple-success-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10001;
  padding: 20px;
}

.apple-success-modal {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border-radius: 28px;
  padding: 32px 28px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  box-shadow: 
    0 30px 60px -15px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 1);
  min-width: 300px;
  max-width: 360px;
  animation: apple-success-bounce 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes apple-success-bounce {
  0% {
    opacity: 0;
    transform: scale(0.8) translateY(30px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.apple-success-check {
  width: 90px;
  height: 90px;
  position: relative;
}

.apple-check-circle {
  width: 100%;
  height: 100%;
}

.apple-check-bg {
  fill: none;
  stroke: #e8f5e9;
  stroke-width: 4;
}

.apple-check-ring {
  fill: none;
  stroke: #34C759;
  stroke-width: 4;
  stroke-linecap: round;
  stroke-dasharray: 283;
  stroke-dashoffset: 283;
  animation: apple-ring-draw 0.6s ease-out 0.1s forwards;
  transform-origin: center;
  transform: rotate(-90deg);
}

@keyframes apple-ring-draw {
  to {
    stroke-dashoffset: 0;
  }
}

.apple-check-mark {
  fill: none;
  stroke: #34C759;
  stroke-width: 5;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-dasharray: 60;
  stroke-dashoffset: 60;
  animation: apple-check-draw 0.4s ease-out 0.5s forwards;
}

@keyframes apple-check-draw {
  to {
    stroke-dashoffset: 0;
  }
}

.apple-success-content {
  text-align: center;
}

.apple-success-content h3 {
  margin: 0 0 8px;
  font-size: 22px;
  font-weight: 700;
  color: #1d1d1f;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
  letter-spacing: -0.03em;
}

.apple-success-filename {
  margin: 0;
  font-size: 14px;
  color: #34C759;
  font-weight: 600;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Inter', sans-serif;
  padding: 6px 14px;
  background: rgba(52, 199, 89, 0.1);
  border-radius: 20px;
  display: inline-block;
}

.apple-success-info {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px;
  background: linear-gradient(135deg, #f8f9fa 0%, #f0f1f3 100%);
  border-radius: 16px;
}

.apple-success-user {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  min-width: 0;
}

.apple-success-avatar {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #007AFF 0%, #5AC8FA 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.apple-success-avatar svg {
  width: 22px;
  height: 22px;
  stroke: white;
  stroke-width: 2;
}

.apple-success-user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.apple-success-user-name {
  font-size: 14px;
  font-weight: 600;
  color: #1d1d1f;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Inter', sans-serif;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.apple-success-user-period {
  font-size: 12px;
  font-weight: 500;
  color: #007AFF;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Inter', sans-serif;
}

.apple-success-status {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.apple-success-status.firmado {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  color: #155724;
}

.apple-success-status.pendiente {
  background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%);
  color: #856404;
}

.apple-success-status svg {
  width: 16px;
  height: 16px;
}

.apple-success-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 24px;
  background: linear-gradient(135deg, #34C759 0%, #30D158 100%);
  border: none;
  border-radius: 14px;
  color: white;
  font-size: 16px;
  font-weight: 600;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Inter', sans-serif;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 14px rgba(52, 199, 89, 0.35);
}

.apple-success-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(52, 199, 89, 0.45);
  background: linear-gradient(135deg, #28A745 0%, #2ECC40 100%);
}

.apple-success-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(52, 199, 89, 0.3);
}

.apple-success-btn svg {
  width: 20px;
  height: 20px;
  stroke-width: 2.5;
}

/* Transición del modal de éxito */
.apple-success-modal-enter-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.apple-success-modal-leave-active {
  transition: all 0.25s ease-out;
}

.apple-success-modal-enter-from {
  opacity: 0;
}

.apple-success-modal-enter-from .apple-success-modal {
  transform: scale(0.8) translateY(30px);
}

.apple-success-modal-leave-to {
  opacity: 0;
}

.apple-success-modal-leave-to .apple-success-modal {
  transform: scale(0.95) translateY(-15px);
}

/* Responsive del modal de éxito */
@media (max-width: 480px) {
  .apple-success-modal {
    padding: 24px 20px 20px;
    min-width: 280px;
    max-width: 320px;
    border-radius: 24px;
  }
  
  .apple-success-check {
    width: 70px;
    height: 70px;
  }
  
  .apple-success-content h3 {
    font-size: 18px;
  }
  
  .apple-success-filename {
    font-size: 12px;
    padding: 5px 12px;
  }
  
  .apple-success-info {
    padding: 12px;
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }
  
  .apple-success-user {
    justify-content: center;
  }
  
  .apple-success-status {
    justify-content: center;
  }
  
  .apple-success-avatar {
    width: 36px;
    height: 36px;
  }
  
  .apple-success-avatar svg {
    width: 18px;
    height: 18px;
  }
  
  .apple-success-user-name {
    font-size: 13px;
  }
  
  .apple-success-user-period {
    font-size: 11px;
  }
  
  .apple-success-btn {
    padding: 12px 20px;
    font-size: 15px;
  }
}

</style>
