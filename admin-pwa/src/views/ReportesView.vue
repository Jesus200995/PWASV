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
              <p class="header-subtitle">Firma y gestiona los reportes de los usuarios</p>
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
        <!-- Título del territorio (solo para admins territoriales) -->
        <div v-if="territorioUsuario" class="territorio-banner">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
            <circle cx="12" cy="10" r="3"/>
          </svg>
          <span>Reportes de {{ territorioUsuario }}</span>
        </div>

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
            
            <div class="stat-card firmados">
              <div class="stat-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 12l2 2 4-4"/>
                  <circle cx="12" cy="12" r="10"/>
                </svg>
              </div>
              <div class="stat-info">
                <span class="stat-value">{{ reportesFirmados.length }}</span>
                <span class="stat-label">Firmados</span>
              </div>
            </div>
            
            <div class="stat-card pendientes">
              <div class="stat-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12 6 12 12 16 14"/>
                </svg>
              </div>
              <div class="stat-info">
                <span class="stat-value">{{ reportesPendientes.length }}</span>
                <span class="stat-label">Pendientes</span>
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

        <!-- Barra de acciones para firma masiva -->
        <div v-if="reportesSeleccionados.length > 0" class="firma-actions-bar">
          <div class="firma-actions-info">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12l2 2 4-4"/>
              <rect x="3" y="3" width="18" height="18" rx="2"/>
            </svg>
            <span><strong>{{ reportesSeleccionados.length }}</strong> reportes seleccionados</span>
          </div>
          <div class="firma-actions-buttons">
            <button @click="deseleccionarTodos" class="btn-deselect">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
              Deseleccionar
            </button>
            <button @click="abrirModalFirma" class="btn-firmar-seleccionados">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 19l7-7 3 3-7 7-3-3z"/>
                <path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/>
                <path d="M2 2l7.586 7.586"/>
              </svg>
              Firmar Seleccionados ({{ reportesSeleccionados.length }})
            </button>
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
              <!-- Botón firmar todos los pendientes del período seleccionado -->
              <button 
                v-if="reportesPendientesFiltrados.length > 0" 
                @click="seleccionarTodosPendientes" 
                class="btn-firmar-todos"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 19l7-7 3 3-7 7-3-3z"/>
                  <path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/>
                </svg>
                Seleccionar Todos Pendientes ({{ reportesPendientesFiltrados.length }})
              </button>
            </div>
            
            <div class="filters-grid">
              <div class="filter-group search-group full-width">
                <label for="search-input" class="filter-label">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="m21 21-4.35-4.35"></path>
                  </svg>
                  Búsqueda General
                </label>
                <div class="search-input-wrapper">
                  <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="m21 21-4.35-4.35"></path>
                  </svg>
                  <input 
                    id="search-input"
                    v-model="filtros.busqueda" 
                    type="text" 
                    placeholder="Nombre de usuario, correo electrónico, CURP o territorio" 
                    class="search-input"
                  >
                  <transition name="fade-quick">
                    <button v-if="filtros.busqueda" @click="limpiarBusquedaReportes" class="clear-search-btn" title="Limpiar búsqueda">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                      </svg>
                    </button>
                  </transition>
                  <span v-if="filtros.busqueda && reportesFiltrados.length > 0" class="search-results-count">
                    {{ reportesFiltrados.length }} {{ reportesFiltrados.length === 1 ? 'resultado' : 'resultados' }}
                  </span>
                </div>
              </div>

              <div class="filter-group">
                <label for="filter-mes" class="filter-label">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                  </svg>
                  Mes
                </label>
                <select id="filter-mes" v-model="filtros.mes" @change="cargarReportes" class="filter-select">
                  <option value="">Todos los meses</option>
                  <option v-for="mes in meses" :key="mes.value" :value="mes.value">{{ mes.label }}</option>
                </select>
              </div>

              <div class="filter-group">
                <label for="filter-anio" class="filter-label">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                  </svg>
                  Año
                </label>
                <select id="filter-anio" v-model="filtros.anio" @change="cargarReportes" class="filter-select">
                  <option value="">Todos los años</option>
                  <option v-for="anio in anios" :key="anio" :value="anio">{{ anio }}</option>
                </select>
              </div>

              <div class="filter-group" v-if="!territorioUsuario">
                <label for="filter-territorio" class="filter-label">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                    <circle cx="12" cy="10" r="3"/>
                  </svg>
                  Territorio
                </label>
                <select id="filter-territorio" v-model="filtros.territorio" @change="cargarReportes" class="filter-select">
                  <option value="">Todos los territorios</option>
                  <option v-for="territorio in territorios" :key="territorio" :value="territorio">{{ territorio }}</option>
                </select>
              </div>

              <div class="filter-group">
                <label for="filter-estado" class="filter-label">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                  </svg>
                  Estado de Firma
                </label>
                <select id="filter-estado" v-model="filtros.estadoFirma" class="filter-select">
                  <option value="">Todos los estados</option>
                  <option value="pendiente">Pendientes de firma</option>
                  <option value="firmado">Firmados</option>
                </select>
              </div>

              <div class="filter-group filter-actions">
                <label class="filter-label-invisible">Acciones</label>
                <button @click="limpiarFiltros" class="clear-filters-btn" title="Limpiar todos los filtros">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 6h18"/>
                    <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
                    <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
                    <line x1="10" y1="11" x2="10" y2="17"/>
                    <line x1="14" y1="11" x2="14" y2="17"/>
                  </svg>
                  Limpiar Filtros
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
                    <th class="th-checkbox">
                      <input 
                        type="checkbox" 
                        :checked="todosSeleccionados && reportesPendientesFiltrados.length > 0"
                        :indeterminate="algunosSeleccionados"
                        @change="toggleSeleccionarTodos"
                        :disabled="reportesPendientesFiltrados.length === 0"
                        class="checkbox-header"
                        title="Seleccionar todos los pendientes"
                      >
                    </th>
                    <th class="th-estado">Estado</th>
                    <th class="th-usuario">Usuario</th>
                    <th class="th-territorio">Territorio</th>
                    <th class="th-reporte">Reporte</th>
                    <th class="th-periodo">Período</th>
                    <th class="th-fecha">Fecha</th>
                    <th class="th-acciones">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="reporte in reportesPaginados" :key="reporte.id" 
                      :class="{ 'row-firmado': reporte.firmado_supervisor, 'row-seleccionado': reportesSeleccionados.includes(reporte.id) }">
                    <td class="td-checkbox">
                      <input 
                        v-if="!reporte.firmado_supervisor"
                        type="checkbox"
                        :checked="reportesSeleccionados.includes(reporte.id)"
                        @change="toggleSeleccion(reporte)"
                        class="checkbox-row"
                        title="Seleccionar para firmar"
                      >
                    </td>
                    <td class="td-estado">
                      <div v-if="reporte.firmado_supervisor" class="estado-badge firmado" :title="'Firmado por ' + reporte.nombre_supervisor">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                          <path d="M9 12l2 2 4-4"/>
                          <circle cx="12" cy="12" r="10"/>
                        </svg>
                        <span>Firmado</span>
                      </div>
                      <div v-else class="estado-badge pendiente">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <circle cx="12" cy="12" r="10"/>
                          <polyline points="12 6 12 12 16 14"/>
                        </svg>
                        <span>Pendiente</span>
                      </div>
                    </td>
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
                      <span v-if="reporte.firmado_supervisor" class="firma-info">
                        Firmado por {{ reporte.nombre_supervisor }}
                      </span>
                    </td>
                    <td class="td-periodo">
                      <span class="periodo-badge">{{ reporte.mes }} {{ reporte.anio }}</span>
                    </td>
                    <td class="td-fecha">
                      <span class="fecha-text">{{ formatearFecha(reporte.fecha_generacion) }}</span>
                      <span v-if="reporte.firmado_supervisor && reporte.fecha_firma_supervisor" class="fecha-firma">
                        Firmado: {{ formatearFecha(reporte.fecha_firma_supervisor) }}
                      </span>
                    </td>
                    <td class="td-acciones">
                      <div class="acciones-buttons">
                        <!-- Botón firmar individual (solo si no está firmado) -->
                        <button 
                          v-if="!reporte.firmado_supervisor" 
                          @click="abrirModalFirmaIndividual(reporte)" 
                          class="btn-action btn-sign" 
                          title="Firmar reporte"
                        >
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 19l7-7 3 3-7 7-3-3z"/>
                            <path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/>
                          </svg>
                        </button>
                        <!-- Botón Ver (SIEMPRE VISIBLE) -->
                        <button @click="verReporte(reporte)" :disabled="viendoReporte === reporte.id" class="btn-action btn-view" title="Ver reporte">
                          <svg v-if="viendoReporte !== reporte.id" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
                          </svg>
                          <div v-else class="spinner-mini"></div>
                        </button>
                        <button v-if="reporte.tiene_pdf || reporte.datos_reporte" @click="descargarReporte(reporte)" :disabled="descargandoReporte === reporte.id" class="btn-action btn-download" title="Descargar">
                          <svg v-if="descargandoReporte !== reporte.id" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>
                          </svg>
                          <div v-else class="spinner-mini"></div>
                        </button>
                        <span v-if="!reporte.tiene_pdf && !reporte.datos_reporte && reporte.tipo === 'PDF'" class="no-pdf-badge" title="PDF no disponible">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
                          </svg>
                        </span>
                        <!-- Botón eliminar - SIEMPRE VISIBLE (se puede eliminar incluso si está firmado) -->
                        <button 
                          @click="confirmarEliminacion(reporte)" 
                          :disabled="eliminandoReporte === reporte.id" 
                          class="btn-action btn-delete" 
                          :title="reporte.firmado_supervisor ? 'Eliminar reporte firmado' : 'Eliminar reporte'"
                        >
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
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import FirmaDigitalAdmin from '../components/FirmaDigitalAdmin.vue'
import reportesService from '../services/reportesService'
import authService from '../services/authService'
import { generarPDFDesdesDatos } from '../utils/pdfGenerator'

const router = useRouter()

// Obtener territorio del usuario admin actual (si es territorial)
const territorioUsuario = ref(authService.getTerritorioFilter())

const loading = ref(false)
const reportes = ref([])
const totalReportes = ref(0)
const territorios = ref([])

const viendoReporte = ref(null)
const descargandoReporte = ref(null)
const eliminandoReporte = ref(null)

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
  if (descargandoReporte.value) {
    console.log('⚠️ Ya se está descargando un reporte')
    return
  }

  console.log(`📥 Descargando reporte: ${reporte.nombre_reporte}`)
  descargandoReporte.value = reporte.id

  try {
    // Obtener datos del reporte desde el servidor
    const response = await reportesService.obtenerReporte(reporte.id)
    
    if (!response.success) {
      throw new Error('No se pudo obtener el reporte')
    }
    
    const reporteData = response.reporte
    
    // Generar PDF desde datos estructurados
    if (reporteData.datos_reporte) {
      console.log('📄 Generando PDF desde datos estructurados...')
      
      // Generar PDF con las firmas disponibles
      const pdfBase64 = await generarPDFDesdesDatos(
        reporteData.datos_reporte,
        reporteData.firma_usuario_base64,
        reporteData.firmado_supervisor ? reporteData.firma_supervisor_base64 : null,
        reporteData.nombre_supervisor
      )
      
      // Descargar el PDF
      descargarPDFBase64(pdfBase64, reporte.nombre_reporte)
      
      console.log('✅ Reporte generado y descargado exitosamente')
      
      alert(reporteData.firmado_supervisor 
        ? `${reporte.nombre_reporte} descargado (firmado por supervisor)` 
        : `${reporte.nombre_reporte} descargado (pendiente de autorización)`)
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
    descargandoReporte.value = null
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

.reportes-container { display: flex; min-height: 100vh; background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%); }

.main-content { flex: 1; margin-left: min(220px, 18vw); width: calc(100vw - min(220px, 18vw)); background: linear-gradient(135deg, #f8f9fa 0%, #f0fff0 100%); min-height: 100vh; position: relative; box-sizing: border-box; overflow-x: hidden; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }

.page-header { background: linear-gradient(135deg, #4CAF50 0%, #45a049 50%, #2E7D32 100%); color: white; padding: clamp(0.3rem, 0.8vw, 0.5rem); box-shadow: 0 4px 16px rgba(76, 175, 80, 0.15); position: sticky; top: 0; z-index: 100; width: 100%; box-sizing: border-box; backdrop-filter: blur(8px); border-bottom: 1px solid rgba(255, 255, 255, 0.1); overflow: hidden; }

.page-header::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat; z-index: 1; }

.header-content { display: flex; justify-content: space-between; align-items: center; max-width: 100%; margin: 0; gap: clamp(0.25rem, 0.8vw, 0.5rem); flex-wrap: wrap; width: 100%; position: relative; z-index: 2; }

.header-main { display: flex; align-items: center; gap: clamp(0.5rem, 1.2vw, 0.8rem); flex: 1; min-width: 140px; margin-left: clamp(0.3rem, 1vw, 0.6rem); }

.header-icon { width: clamp(28px, 3vw, 32px); height: clamp(28px, 3vw, 32px); background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.1) 100%); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: inset 0 -1px 0 rgba(0, 0, 0, 0.1); position: relative; overflow: hidden; }

.header-icon svg { width: clamp(14px, 2.5vw, 16px); height: clamp(14px, 2.5vw, 16px); filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2)); z-index: 1; position: relative; flex-shrink: 0; }

.header-text { flex: 1; min-width: 120px; }

.header-title { font-size: clamp(14px, 2.5vw, 16px); font-weight: 700; margin: 0 0 clamp(1px, 0.3vw, 2px) 0; background: linear-gradient(135deg, #ffffff 0%, #e8f5e8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1); font-family: 'Inter', sans-serif; line-height: 1.2; }

.header-subtitle { font-size: clamp(9px, 1.8vw, 11px); opacity: 0.9; margin: 0; font-weight: 400; text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1); font-family: 'Inter', sans-serif; line-height: 1.3; }

.header-actions { display: flex; gap: clamp(0.2rem, 0.5vw, 0.4rem); align-items: center; margin-right: clamp(0.3rem, 1vw, 0.6rem); }

.refresh-btn { display: flex; align-items: center; gap: clamp(3px, 0.5vw, 5px); padding: clamp(4px, 0.8vw, 6px) clamp(8px, 1.2vw, 10px); background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.1) 100%); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); color: white; border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 6px; font-size: clamp(10px, 1.8vw, 12px); font-weight: 600; cursor: pointer; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); font-family: 'Inter', sans-serif; box-shadow: inset 0 -1px 0 rgba(0, 0, 0, 0.1); }

.refresh-btn:hover:not(:disabled) { background: rgba(255, 255, 255, 0.3); transform: translateY(-1px); }

.refresh-btn:disabled { opacity: 0.7; cursor: not-allowed; }

.refresh-icon { width: 16px; height: 16px; }

.refresh-icon.spinning { animation: spin 1s linear infinite; }

@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

.page-content { padding: clamp(12px, 2vw, 24px); max-width: 1600px; margin: 0 auto; }

/* Banner de territorio (solo para admins territoriales) */
.territorio-banner {
  background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%);
  color: white;
  padding: 14px 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  box-shadow: 0 4px 12px rgba(139, 69, 19, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-family: 'Inter', sans-serif;
  font-size: clamp(14px, 2vw, 16px);
  font-weight: 600;
  text-align: center;
}

.territorio-banner svg {
  width: 18px;
  height: 18px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

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
.stat-card.firmados .stat-icon { background: linear-gradient(135deg, #22c55e, #16a34a); }
.stat-card.pendientes .stat-icon { background: linear-gradient(135deg, #f59e0b, #d97706); }

.stat-info { display: flex; flex-direction: column; }

.stat-value { font-size: 1.25rem; font-weight: 700; color: #1a1a1a; font-family: 'Inter', sans-serif; line-height: 1; }

.stat-label { font-size: 0.7rem; color: #666; font-family: 'Inter', sans-serif; margin-top: 2px; }

.filters-section { margin-bottom: clamp(16px, 2vw, 24px); }

.filters-card { background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); border: 1px solid rgba(0, 0, 0, 0.05); overflow: hidden; }

.filters-header { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  gap: 16px; 
  flex-wrap: wrap;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); 
  padding: 16px 20px; 
  border-bottom: 1px solid rgba(34, 197, 94, 0.15); 
}

.filters-header h3 { display: flex; align-items: center; gap: 10px; margin: 0; font-size: clamp(0.9rem, 1.3vw, 1rem); font-weight: 600; color: #15803d; font-family: 'Inter', sans-serif; }

.filters-header svg { color: #16a34a; }

.filters-grid { 
  display: grid; 
  grid-template-columns: 1fr 1fr 1fr 1fr auto; 
  gap: clamp(10px, 1.3vw, 14px); 
  padding: clamp(12px, 1.5vw, 16px);
  align-items: end;
}

.filter-group { 
  display: flex; 
  flex-direction: column; 
  gap: 6px; 
}

.filter-group.full-width {
  grid-column: 1 / -1;
  margin-bottom: 6px;
}

.filter-group.filter-actions {
  display: flex;
  align-items: flex-end;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: clamp(0.68rem, 0.95vw, 0.75rem); 
  font-weight: 600; 
  color: #374151; 
  font-family: 'Inter', sans-serif;
  letter-spacing: -0.01em;
}

.filter-label-invisible {
  display: flex;
  opacity: 0;
  pointer-events: none;
  font-size: clamp(0.68rem, 0.95vw, 0.75rem);
  margin-bottom: 6px;
}

.filter-label svg {
  color: #16a34a;
  opacity: 0.85;
  flex-shrink: 0;
}

.filter-select { 
  padding: clamp(7px, 0.9vw, 9px) clamp(10px, 1.2vw, 12px); 
  border: 1.5px solid #e5e7eb; 
  border-radius: 8px; 
  font-size: clamp(0.7rem, 1vw, 0.78rem); 
  font-family: 'Inter', sans-serif; 
  background: white; 
  cursor: pointer; 
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  color: #374151;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}

.filter-select:hover {
  border-color: #4CAF50;
  box-shadow: 0 2px 6px rgba(76, 175, 80, 0.12);
}

.filter-select:focus { 
  outline: none; 
  border-color: #4CAF50; 
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
}

.search-group { grid-column: span 2; }

.search-input-wrapper { position: relative; }

.search-icon { 
  position: absolute; 
  left: 16px; 
  top: 50%; 
  transform: translateY(-50%); 
  color: #16a34a;
  width: 18px;
  height: 18px;
  z-index: 1;
  pointer-events: none;
}

.search-input { 
  width: 100%; 
  padding: clamp(10px, 1.2vw, 12px) clamp(44px, 5vw, 48px) clamp(10px, 1.2vw, 12px) clamp(48px, 5.5vw, 52px);
  border: 1.5px solid rgba(76, 175, 80, 0.2);
  border-radius: 50px; 
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  font-size: clamp(0.75rem, 1.1vw, 0.85rem); 
  font-family: 'Inter', sans-serif; 
  color: #2d3748;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-sizing: border-box;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.08), inset 0 1px 2px rgba(255, 255, 255, 0.9);
}

.search-input:hover {
  border-color: rgba(76, 175, 80, 0.4);
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.12), inset 0 1px 2px rgba(255, 255, 255, 0.9);
}

.search-input:focus { 
  outline: none; 
  border-color: #4CAF50; 
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.18), 0 0 0 3px rgba(76, 175, 80, 0.1), inset 0 1px 2px rgba(255, 255, 255, 0.9);
  transform: translateY(-1px);
}

.search-input::placeholder {
  color: rgba(107, 114, 128, 0.6);
}

.clear-search-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(239, 68, 68, 0.1);
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  padding: 0;
  z-index: 2;
}

.clear-search-btn:hover {
  background: rgba(239, 68, 68, 0.2);
  transform: translateY(-50%) scale(1.1);
}

.clear-search-btn:active {
  transform: translateY(-50%) scale(0.95);
}

.clear-search-btn svg {
  width: 11px;
  height: 11px;
  color: #ef4444;
}

.search-results-count {
  position: absolute;
  right: 50px;
  top: 50%;
  transform: translateY(-50%);
  font-size: clamp(0.7rem, 1vw, 0.78rem);
  color: #16a34a;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  background: rgba(220, 252, 231, 0.8);
  padding: 4px 10px;
  border-radius: 12px;
  white-space: nowrap;
  z-index: 1;
}

.fade-quick-enter-active, .fade-quick-leave-active {
  transition: opacity 0.15s ease;
}

.fade-quick-enter-from, .fade-quick-leave-to {
  opacity: 0;
}

.filter-actions { display: flex; align-items: flex-end; }

.clear-filters-btn { 
  display: flex; 
  align-items: center; 
  justify-content: center;
  gap: 7px; 
  padding: clamp(7px, 0.9vw, 9px) clamp(16px, 1.8vw, 20px); 
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  color: #dc2626; 
  border: 1.5px solid #fecaca; 
  border-radius: 8px; 
  font-size: clamp(0.7rem, 1vw, 0.78rem); 
  font-weight: 600; 
  cursor: pointer; 
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); 
  font-family: 'Inter', sans-serif;
  box-shadow: 0 1px 3px rgba(220, 38, 38, 0.08);
  white-space: nowrap;
  min-width: 150px;
}

.clear-filters-btn:hover { 
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border-color: #dc2626; 
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(220, 38, 38, 0.18);
}

.clear-filters-btn:active {
  transform: translateY(0);
  box-shadow: 0 1px 3px rgba(220, 38, 38, 0.12);
}

.clear-filters-btn svg {
  flex-shrink: 0;
  transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.clear-filters-btn:hover svg {
  transform: scale(1.1) rotate(-5deg);
}

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

@media (max-width: 1200px) { .main-content { margin-left: min(200px, 16vw); width: calc(100vw - min(200px, 16vw)); } }

@media (max-width: 1024px) { .main-content { margin-left: 200px; width: calc(100vw - 200px); } .stats-grid { grid-template-columns: repeat(2, 1fr); } .filters-grid { grid-template-columns: 1fr 1fr 1fr; } .search-group { grid-column: span 3; } .full-width { grid-column: span 3; } .filter-actions { grid-column: span 3; } .clear-filters-btn { width: 100%; } }

@media (max-width: 768px) and (orientation: landscape) { .main-content { margin-left: 160px; width: calc(100vw - 160px); } }

@media (max-width: 992px) { .main-content { margin-left: 200px; width: calc(100vw - 200px); } }

@media (min-width: 481px) and (max-width: 768px) { .main-content { margin-left: 250px; width: calc(100vw - 250px); } }

@media (max-width: 768px) { .main-content { margin-left: 240px; width: calc(100vw - 240px); } .header-content { flex-direction: column; align-items: flex-start; gap: 12px; } .header-main { width: 100%; } .header-actions { width: 100%; justify-content: flex-end; } .stats-grid { grid-template-columns: repeat(2, 1fr); } .filters-grid { grid-template-columns: 1fr 1fr; } .search-group { grid-column: span 2; } .full-width { grid-column: 1 / -1; } .filter-actions { grid-column: span 2; } .clear-filters-btn { width: 100%; } .reportes-table th, .reportes-table td { padding: 8px 6px; font-size: 0.7rem; } .usuario-avatar { width: 28px; height: 28px; font-size: 0.6rem; } .modal-container { max-width: 90%; } .modal-header { padding: 14px; gap: 12px; } .modal-icon { width: 38px; height: 38px; min-width: 38px; } .modal-icon svg { width: 18px; height: 18px; max-width: 18px; max-height: 18px; } .modal-body { padding: 14px; } .modal-footer { padding: 12px 14px; } .modal-title-container h3 { font-size: 1rem; } .modal-title-container p { font-size: 0.75rem; } .search-results-count { font-size: 0.68rem; right: 44px; padding: 3px 8px; } }

@media (max-width: 480px) { .main-content { margin-left: 60px; width: calc(100vw - 60px); } .page-content { padding: 8px; } .stats-grid { grid-template-columns: 1fr 1fr; gap: 8px; } .stat-card { padding: 8px 10px; } .stat-icon { width: 32px; height: 32px; min-width: 32px; } .stat-icon svg { width: 16px; height: 16px; max-width: 16px; max-height: 16px; } .stat-value { font-size: 1rem; } .stat-label { font-size: 0.65rem; } .pagination-container { flex-direction: column; text-align: center; } .filters-grid { grid-template-columns: 1fr; gap: 10px; } .filter-actions { grid-column: span 1; } .clear-filters-btn { width: 100%; min-width: unset; } .th-territorio, .td-territorio { display: none; } .btn-action { width: 28px; height: 28px; } .modal-overlay { padding: 12px; } .modal-container { max-width: 95%; } .modal-header { padding: 12px; gap: 10px; flex-wrap: wrap; } .modal-icon { width: 36px; height: 36px; min-width: 36px; } .modal-icon svg { width: 16px; height: 16px; } .modal-body { padding: 12px; } .modal-body p { font-size: 0.8rem; } .modal-footer { padding: 12px; flex-direction: column; gap: 8px; } .btn-cancel, .btn-delete-confirm { width: 100%; padding: 11px 16px; font-size: 0.85rem; } .modal-title-container h3 { font-size: 0.95rem; } .modal-title-container p { font-size: 0.7rem; } .reporte-eliminar-info { padding: 10px; } .reporte-eliminar-info strong { font-size: 0.85rem; } }

@media (max-width: 360px) { .main-content { margin-left: 60px; width: calc(100vw - 60px); } .header-title { font-size: 1rem !important; } .stats-grid { grid-template-columns: 1fr; } }

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

.btn-firmar-todos {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  font-family: 'Inter', sans-serif;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  border: none;
  color: white;
  box-shadow: 0 3px 10px rgba(34, 197, 94, 0.25);
  white-space: nowrap;
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
  width: 16px;
  height: 16px;
  flex-shrink: 0;
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
}
</style>
