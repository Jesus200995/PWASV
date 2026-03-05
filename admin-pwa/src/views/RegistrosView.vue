<template>
  <div class="registros-container">
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
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <polyline points="14,2 14,8 20,8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <span class="apple-title-divider">|</span>
                <h1 class="apple-page-title">REGISTROS</h1>
              </div>
              <p class="apple-page-subtitle">Gestión de actividades y documentos</p>
            </div>
            
            <button @click="cargarRegistros" class="apple-refresh-button" :disabled="loading">
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
                <div class="apple-stat-value">{{ actividadesHoy }}</div>
                <div class="apple-stat-label">Hoy</div>
              </div>
            </div>

            <div class="apple-stat-card">
              <div class="apple-stat-icon green">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke-width="2"/>
                  <circle cx="9" cy="7" r="4" stroke-width="2"/>
                </svg>
              </div>
              <div class="apple-stat-content">
                <div class="apple-stat-value">{{ totalActividades }}</div>
                <div class="apple-stat-label">Total</div>
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
                <div class="apple-stat-value">{{ registrosFiltrados.length }}</div>
                <div class="apple-stat-label">Filtrados</div>
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
                  @input="buscarEnTiempoReal"
                  type="text" 
                  placeholder="Buscar por CURP, correo, nombre, descripción..." 
                  class="apple-search-input"
                >
                <button v-if="searchTerm && !buscandoUsuario" @click="limpiarBusqueda" class="apple-clear-btn">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10" stroke-width="2"/>
                    <line x1="15" y1="9" x2="9" y2="15" stroke-width="2" stroke-linecap="round"/>
                    <line x1="9" y1="9" x2="15" y2="15" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </button>
                <span v-if="buscandoUsuario" class="apple-search-loading">
                  <svg class="apple-spin" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
                  </svg>
                </span>
              </div>

              <div class="apple-filter-controls">
                <button 
                  @click="limpiarTodosFiltros" 
                  class="apple-filter-btn reset"
                  title="Limpiar filtros"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M3 6h18M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span>Limpiar</span>
                </button>
                <button 
                  @click="mostrarFiltrosAvanzados = !mostrarFiltrosAvanzados" 
                  class="apple-filter-btn"
                  :class="{ active: mostrarFiltrosAvanzados }"
                  title="Filtros avanzados"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span>Filtros</span>
                </button>
                <button 
                  @click="exportarRegistros('csv')" 
                  class="apple-filter-btn export"
                  title="Exportar a CSV"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span>CSV</span>
                </button>
              </div>
            </div>

            <!-- Quick Date Filters -->
            <div class="apple-quick-filters">
              <button 
                @click="seleccionarFechaRapida('hoy')" 
                :class="['apple-filter-chip', { 'active': filtroRapido === 'hoy' }]"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="12" cy="12" r="10" stroke-width="2"/>
                  <path d="M12 6v6l4 2" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <span>Hoy</span>
              </button>
              <button 
                @click="seleccionarFechaRapida('ayer')" 
                :class="['apple-filter-chip', { 'active': filtroRapido === 'ayer' }]"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M3 3v5h5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Ayer</span>
              </button>
              <button 
                @click="seleccionarFechaRapida('semana')" 
                :class="['apple-filter-chip', { 'active': filtroRapido === 'semana' }]"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke-width="2"/>
                  <line x1="16" y1="2" x2="16" y2="6" stroke-width="2" stroke-linecap="round"/>
                  <line x1="8" y1="2" x2="8" y2="6" stroke-width="2" stroke-linecap="round"/>
                  <line x1="3" y1="10" x2="21" y2="10" stroke-width="2"/>
                </svg>
                <span>Esta semana</span>
              </button>
              <button 
                @click="seleccionarFechaRapida('mes')" 
                :class="['apple-filter-chip', { 'active': filtroRapido === 'mes' }]"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke-width="2"/>
                  <line x1="3" y1="10" x2="21" y2="10" stroke-width="2"/>
                </svg>
                <span>Este mes</span>
              </button>
            </div>

            <!-- Filtros Avanzados Expandibles -->
            <div v-if="mostrarFiltrosAvanzados" class="apple-advanced-filters">
              <div class="advanced-grid">
                <div class="filter-item">
                  <label>Usuario</label>
                  <select v-model="filtroUsuario" @change="filtrarRegistros">
                    <option value="">Todos</option>
                    <option v-for="usuario in usuariosUnicos" :key="usuario.id" :value="usuario.id">
                      {{ usuario.nombre_completo }}
                    </option>
                  </select>
                </div>
                <div class="filter-item">
                  <label>Tipo</label>
                  <select v-model="filtroTipoActividad" @change="filtrarRegistros">
                    <option value="">Todos</option>
                    <option value="campo">Campo</option>
                    <option value="gabinete">Gabinete</option>
                  </select>
                </div>
                <div class="filter-item">
                  <label>Desde</label>
                  <input type="date" v-model="filtroFechaInicio" @change="filtrarRegistros" :max="filtroFechaFin || maxDate">
                </div>
                <div class="filter-item">
                  <label>Hasta</label>
                  <input type="date" v-model="filtroFechaFin" @change="filtrarRegistros" :min="filtroFechaInicio" :max="maxDate">
                </div>
              </div>
              <div class="filter-checkboxes">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="filtroConFoto" @change="filtrarRegistros">
                  <span>Con foto</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="filtroSinFoto" @change="filtrarRegistros">
                  <span>Sin foto</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="filtroConDescripcion" @change="filtrarRegistros">
                  <span>Con descripción</span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>  <!-- Close apple-sticky-wrapper -->

      <div class="apple-content-wrapper">
        <!-- ================== TABLE APPLE STYLE ================== -->
        <div class="apple-table-container">
          <div v-if="loading && registros.length === 0" class="apple-loading">
            <div class="apple-spinner"></div>
            <p>Cargando registros...</p>
          </div>

          <div v-else-if="error" class="apple-error">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="10" stroke-width="2"/>
              <line x1="12" y1="8" x2="12" y2="12" stroke-width="2" stroke-linecap="round"/>
              <line x1="12" y1="16" x2="12.01" y2="16" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <p>{{ error }}</p>
            <button @click="cargarRegistros" class="apple-retry-btn">Reintentar</button>
          </div>

          <div v-else-if="registrosFiltrados.length === 0" class="apple-empty">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="10" stroke-width="2"/>
              <path d="M8 14s1.5 2 4 2 4-2 4-2" stroke-width="2" stroke-linecap="round"/>
              <line x1="9" y1="9" x2="9.01" y2="9" stroke-width="2" stroke-linecap="round"/>
              <line x1="15" y1="9" x2="15.01" y2="9" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <h3>No hay registros</h3>
            <p v-if="filtroUsuario">No se encontraron registros para {{ usuariosDisponibles.find(u => u.id.toString() === filtroUsuario.toString())?.nombre_completo || `Usuario ${filtroUsuario}` }}</p>
            <p v-else>No se encontraron registros con los filtros aplicados</p>
          </div>
          
          <div v-else class="apple-table-wrapper">
            <table class="apple-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Usuario</th>
                  <th>Foto</th>
                  <th>Tipo</th>
                  <th>Ubicación</th>
                  <th>Descripción</th>
                  <th>Fecha</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="registro in registrosPaginados" :key="registro.id" class="apple-table-row">
                  <td>
                    <span class="apple-id-badge">#{{ registro.id }}</span>
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
                        <div class="apple-user-name">{{ registro.usuario?.nombre_completo || `Usuario ${registro.usuario_id}` }}</div>
                        <div class="apple-user-role">{{ registro.usuario?.correo || 'No disponible' }}</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <img 
                      v-if="registro.foto_url" 
                      :src="`${API_URL}/${registro.foto_url}`"
                      alt="Foto" 
                      class="apple-photo-thumb"
                      @click="abrirFotoCompleta(registro.foto_url)"
                    >
                    <span v-else class="apple-no-data">—</span>
                  </td>
                  <td>
                    <span :class="['apple-tipo-badge', getTipoClass(registro.tipo_actividad)]">
                      {{ getTipoLabel(registro.tipo_actividad) }}
                    </span>
                  </td>
                  <td>
                    <button 
                      v-if="registro.latitud && registro.longitud"
                      @click="abrirMapa(registro)" 
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
                    <span class="apple-descripcion">{{ truncateText(registro.descripcion || 'Sin descripción', 40) }}</span>
                  </td>
                  <td>
                    <div class="apple-fecha-cell">
                      <span class="apple-time-badge">{{ formatFechaCompacta(registro.fecha_hora).hora }}</span>
                      <span class="apple-date-badge">{{ formatFechaCompacta(registro.fecha_hora).fecha }}</span>
                    </div>
                  </td>
                  <td>
                    <div class="apple-actions">
                      <button @click="verDetalles(registro)" class="apple-action-btn view" title="Ver detalles">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke-width="2"/>
                          <circle cx="12" cy="12" r="3" stroke-width="2"/>
                        </svg>
                      </button>
                      <button v-if="puedeNotificarRegistros" @click="abrirModalNotificar(registro)" class="apple-action-btn notify" title="Notificar">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" stroke-width="2"/>
                          <path d="M13.73 21a2 2 0 0 1-3.46 0" stroke-width="2"/>
                        </svg>
                      </button>
                      <button v-if="puedeEliminarRegistros" @click="abrirModalEditar(registro)" class="apple-action-btn edit" title="Editar">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke-width="2"/>
                          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" stroke-width="2"/>
                        </svg>
                      </button>
                      <button v-if="puedeEliminarRegistros" @click="confirmarEliminarRegistro(registro)" class="apple-action-btn delete" title="Eliminar">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <polyline points="3 6 5 6 21 6" stroke-width="2"/>
                          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" stroke-width="2"/>
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
              v-if="totalRegistrosServidor > registros.length"
              @click="cargarMasRegistros" 
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

    <!-- Modal para detalles -->
    <Teleport to="body">
      <div v-if="showModal" class="modal-overlay" @click="cerrarModal">
        <div class="modal-content" @click.stop>
          <!-- Header del modal con degradado verde -->
          <div class="modal-header">
            <div class="modal-header-content">
              <div class="modal-icon">
                <svg width="18" height="18" fill="white" viewBox="0 0 24 24">
                  <path fill-rule="evenodd" d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0016.5 9h-1.875a1.875 1.875 0 01-1.875-1.875V5.25A3.75 3.75 0 009 1.5H5.625zM7.5 15a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5A.75.75 0 017.5 15zm.75 2.25a.75.75 0 000 1.5H12a.75.75 0 000-1.5H8.25z" clip-rule="evenodd"/>
                  <path d="M12.971 1.816A5.23 5.23 0 0114.25 5.25v1.875c0 .207.168.375.375.375H16.5a5.23 5.23 0 013.434 1.279 9.768 9.768 0 00-6.963-6.963z"/>
                </svg>
              </div>
              <h3 class="modal-title">
                Detalles del Registro
              </h3>
            </div>
            <button @click="cerrarModal" class="btn-close">
              <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>

          <!-- Contenido del modal -->
          <div class="modal-body">
            <!-- Vista de detalles del registro -->
            <div v-if="modalType === 'details' && selectedRegistro" class="registro-detalles">
              <div class="detail-grid">
                <div class="detail-item">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">ID del Registro</span>
                    <span class="detail-value highlight">#{{ selectedRegistro.id }}</span>
                  </div>
                </div>

                <div class="detail-item">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Usuario</span>
                    <span class="detail-value">{{ selectedRegistro.usuario?.nombre_completo || `Usuario ${selectedRegistro.usuario_id}` }}</span>
                  </div>
                </div>

                <div class="detail-item">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M1.5 8.67v8.58a3 3 0 003 3h15a3 3 0 003-3V8.67l-8.928 5.493a3 3 0 01-3.144 0L1.5 8.67z"/>
                      <path d="M22.5 6.908V6.75a3 3 0 00-3-3h-15a3 3 0 00-3 3v.158l9.714 5.978a1.5 1.5 0 001.572 0L22.5 6.908z"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Correo Electrónico</span>
                    <span class="detail-value">{{ selectedRegistro.usuario?.correo || 'No disponible' }}</span>
                  </div>
                </div>

                <div class="detail-item">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path fill-rule="evenodd" d="M6.75 2.25A.75.75 0 017.5 3v1.5h9V3A.75.75 0 0118 3v1.5h.75a3 3 0 013 3v11.25a3 3 0 01-3 3H5.25a3 3 0 01-3-3V7.5a3 3 0 013-3H6V3a.75.75 0 01.75-.75zm13.5 9a1.5 1.5 0 00-1.5-1.5H5.25a1.5 1.5 0 00-1.5 1.5v7.5a1.5 1.5 0 001.5 1.5h13.5a1.5 1.5 0 001.5-1.5v-7.5z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Fecha y Hora</span>
                    <span class="detail-value">{{ formatFecha(selectedRegistro.fecha_hora) }}</span>
                  </div>
                </div>

                <div class="detail-item">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Tipo de Actividad</span>
                    <span class="detail-value">
                      <span :class="['tipo-badge-modal', getTipoClass(selectedRegistro.tipo_actividad)]">
                        {{ getTipoLabel(selectedRegistro.tipo_actividad) }}
                      </span>
                    </span>
                  </div>
                </div>

                <div class="detail-item">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path fill-rule="evenodd" d="M11.54 22.351l.07.04.028.016a.76.76 0 00.723 0l.028-.015.071-.041a16.975 16.975 0 001.144-.742 19.58 19.58 0 002.683-2.282c1.944-1.99 3.963-4.98 3.963-8.827a8.25 8.25 0 00-16.5 0c0 3.846 2.02 6.837 3.963 8.827a19.58 19.58 0 002.682 2.282 16.975 16.975 0 001.145.742zM12 13.5a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Ubicación</span>
                    <span class="detail-value location">{{ parseFloat(selectedRegistro.latitud).toFixed(6) }}, {{ parseFloat(selectedRegistro.longitud).toFixed(6) }}</span>
                  </div>
                </div>

                <div class="detail-item full-width">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path fill-rule="evenodd" d="M4.125 3C3.089 3 2.25 3.84 2.25 4.875V18a3 3 0 003 3h15a3 3 0 01-3-3V4.875C17.25 3.839 16.41 3 15.375 3H4.125zM12 9.75a.75.75 0 000 1.5h1.5a.75.75 0 000-1.5H12zm-.75-2.25a.75.75 0 01.75-.75h1.5a.75.75 0 010 1.5H12a.75.75 0 01-.75-.75zM6 12.75a.75.75 0 000 1.5h7.5a.75.75 0 000-1.5H6zm-.75 3.75a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5H6a.75.75 0 01-.75-.75zM6 6.75a.75.75 0 00-.75.75v3c0 .414.336.75.75.75h3a.75.75 0 00.75-.75v-3A.75.75 0 009 6.75H6z" clip-rule="evenodd"/>
                      <path d="M18.75 6.75h1.875c.621 0 1.125.504 1.125 1.125V18a1.5 1.5 0 01-3 0V6.75z"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Descripción</span>
                    <span class="detail-value description">{{ selectedRegistro.descripcion || 'Sin descripción' }}</span>
                  </div>
                </div>

                <div v-if="selectedRegistro.foto_url" class="detail-item full-width">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path fill-rule="evenodd" d="M1.5 6a2.25 2.25 0 012.25-2.25h16.5A2.25 2.25 0 0122.5 6v12a2.25 2.25 0 01-2.25 2.25H3.75A2.25 2.25 0 011.5 18V6zM3 16.06V18c0 .414.336.75.75.75h16.5A.75.75 0 0021 18v-1.94l-2.69-2.689a1.5 1.5 0 00-2.12 0l-.88.879.97.97a.75.75 0 11-1.06 1.06l-5.16-5.159a1.5 1.5 0 00-2.12 0L3 16.061zm10.125-7.81a1.125 1.125 0 112.25 0 1.125 1.125 0 01-2.25 0z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Fotografía</span>
                    <div class="photo-container">
                      <img 
                        :src="`${API_URL}/${selectedRegistro.foto_url}`" 
                        alt="Foto del registro" 
                        class="detail-photo"
                        @click="abrirFotoCompleta(selectedRegistro.foto_url)"
                      >
                    </div>
                  </div>
                </div>

                <div class="detail-item full-width">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path fill-rule="evenodd" d="M8.25 6.75a3.75 3.75 0 117.5 0 3.75 3.75 0 01-7.5 0zM15.75 9.75a3 3 0 116 0 3 3 0 01-6 0zM2.25 9.75a3 3 0 116 0 3 3 0 01-6 0zM6.31 15.117A6.745 6.745 0 0112 12a6.745 6.745 0 016.709 7.498.75.75 0 01-.372.568A12.696 12.696 0 0112 21.75c-2.305 0-4.47-.612-6.337-1.684a.75.75 0 01-.372-.568 6.787 6.787 0 011.019-1.381z" clip-rule="evenodd"/>
                      <path d="M5.082 14.254a8.287 8.287 0 00-1.308 5.135 9.687 9.687 0 01-1.764-.44l-.115-.04a.563.563 0 01-.373-.487l-.01-.121a3.75 3.75 0 013.57-4.047z"/>
                      <path d="M20.226 19.389a8.287 8.287 0 00-1.308-5.135 3.75 3.75 0 013.57 4.047l-.01.121a.563.563 0 01-.373.486l-.115.041c-.07.027-.148.053-.3.102-.331.108-.763.21-1.464.338z"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Mapa de Ubicación</span>
                    <div class="map-container">
                      <div id="map" class="leaflet-map"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer del modal -->
          <div class="modal-footer">
            <!-- Footer simplificado sin botón de cerrar -->
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Lightbox para ver foto en pantalla completa -->
    <Teleport to="body" v-if="showLightbox">
      <div class="lightbox-overlay" @click="cerrarLightbox">
        <div class="lightbox-container">
          <button class="lightbox-close" @click="cerrarLightbox">
            <svg width="24" height="24" fill="white" viewBox="0 0 24 24">
              <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
            </svg>
          </button>
          <img 
            :src="lightboxImageUrl" 
            alt="Fotografía en pantalla completa"
            class="lightbox-image"
            @click.stop="requestFullscreen"
          >
          <p class="lightbox-hint">Haz clic en la imagen para pantalla completa • ESC o clic fuera para cerrar</p>
        </div>
      </div>
    </Teleport>

    <!-- Modal de confirmación para eliminar registro -->
    <Teleport to="body" v-if="showConfirmDelete">
      <div class="modal-overlay-delete" @click="cancelarEliminar">
        <div class="modal-delete-container" @click.stop>
          <!-- Header -->
          <div class="modal-delete-header">
            <svg class="warning-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M12 9v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <h3>Confirmar Eliminación</h3>
            <button @click="cancelarEliminar" class="btn-close-delete">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>

          <!-- Body -->
          <div class="modal-delete-body">
            <p class="delete-question">¿Estás seguro que deseas eliminar este registro?</p>
            
            <div class="registro-info-box" v-if="registroAEliminar">
              <div class="info-item">
                <span class="info-label-delete">ID:</span>
                <span class="info-value-delete">#{{ registroAEliminar.id }}</span>
              </div>
              <div class="info-item">
                <span class="info-label-delete">USUARIO:</span>
                <span class="info-value-delete">{{ registroAEliminar.usuario?.nombre_completo || `Usuario ${registroAEliminar.usuario_id}` }}</span>
              </div>
              <div class="info-item">
                <span class="info-label-delete">FECHA:</span>
                <span class="info-value-delete">{{ formatFecha(registroAEliminar.fecha_hora) }}</span>
              </div>
            </div>

            <div class="warning-box">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
              </svg>
              <span>Esta acción no se puede deshacer</span>
            </div>
          </div>

          <!-- Footer con botones -->
          <div class="modal-delete-footer">
            <button @click="cancelarEliminar" class="btn-cancel-delete">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
              Cancelar
            </button>
            <button @click="eliminarRegistro" class="btn-confirm-delete">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"/>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                <line x1="10" y1="11" x2="10" y2="17"/>
                <line x1="14" y1="11" x2="14" y2="17"/>
              </svg>
              Eliminar Registro
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Notificación Toast -->
    <Teleport to="body">
      <Transition name="toast">
        <div v-if="showToast" :class="['toast-notification', `toast-${toastType}`]">
          <svg v-if="toastType === 'success'" class="toast-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 6L9 17l-5-5"/>
          </svg>
          <svg v-else-if="toastType === 'error'" class="toast-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="15" y1="9" x2="9" y2="15"/>
            <line x1="9" y1="9" x2="15" y2="15"/>
          </svg>
          <svg v-else class="toast-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="16" x2="12" y2="12"/>
            <line x1="12" y1="8" x2="12.01" y2="8"/>
          </svg>
          <span class="toast-message">{{ toastMessage }}</span>
        </div>
      </Transition>
    </Teleport>

    <!-- Modal de Edición de Registro -->
    <Teleport to="body" v-if="showEditModal">
      <div class="modal-overlay-edit" @click="cerrarModalEditar">
        <div class="modal-edit-container" @click.stop>
          <!-- Header elegante -->
          <div class="modal-edit-header">
            <div class="header-icon-wrapper">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931z"/>
                <path d="M19.5 7.125L16.862 4.487"/>
              </svg>
            </div>
            <div class="header-text">
              <h3>Editar Registro de Actividad</h3>
              <span class="header-subtitle">ID #{{ registroEditando?.id }} - {{ registroEditando?.usuario?.nombre_completo || 'Usuario' }}</span>
            </div>
            <button @click="cerrarModalEditar" class="btn-close-edit" title="Cerrar">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>

          <!-- Contenido del modal con scroll -->
          <div class="modal-edit-scroll-area">
            <!-- Sección de datos NO editables -->
            <div class="modal-edit-readonly-section">
              <h4 class="section-title">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                  <path d="M7 11V7a5 5 0 0110 0v4"/>
                </svg>
                Información no editable
              </h4>
              
              <!-- Grid de 2 columnas para Ubicación y Fotografía -->
              <div class="readonly-grid-2col">
                <!-- Ubicación -->
                <div class="readonly-card">
                  <div class="readonly-card-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                    </svg>
                  </div>
                  <div class="readonly-card-content">
                    <span class="readonly-card-label">Ubicación GPS</span>
                    <span class="readonly-card-value">{{ parseFloat(registroEditando?.latitud || 0).toFixed(6) }}, {{ parseFloat(registroEditando?.longitud || 0).toFixed(6) }}</span>
                  </div>
                </div>

                <!-- Fotografía -->
                <div class="readonly-card readonly-card-photo">
                  <div class="readonly-card-icon" :class="{ 'readonly-card-icon-muted': !registroEditando?.foto_url }">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/>
                    </svg>
                  </div>
                  <div class="readonly-card-content">
                    <span class="readonly-card-label">Fotografía</span>
                    <div v-if="registroEditando?.foto_url" class="readonly-photo-preview-compact">
                      <img 
                        :src="`${API_URL}/${registroEditando.foto_url}`" 
                        alt="Foto del registro" 
                        class="edit-photo-thumb-compact"
                        @click="abrirFotoCompleta(registroEditando.foto_url)"
                      >
                    </div>
                    <span v-else class="readonly-card-value readonly-muted">Sin foto</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Formulario de edición -->
            <div class="modal-edit-body">
              <h4 class="section-title">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 20h9"/>
                  <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
                </svg>
                Campos editables
              </h4>
              
              <form @submit.prevent="guardarEdicion" class="edit-form">
                <!-- Fecha y Hora -->
                <div class="form-row-2col">
                  <div class="form-group">
                    <label for="edit-fecha" class="form-label">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M19 4h-1V2h-2v2H8V2H6v2H5c-1.11 0-1.99.9-1.99 2L3 20c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V9h14v11zM9 11H7v2h2v-2zm4 0h-2v2h2v-2zm4 0h-2v2h2v-2zm-8 4H7v2h2v-2zm4 0h-2v2h2v-2zm4 0h-2v2h2v-2z"/>
                      </svg>
                      Fecha
                    </label>
                    <input 
                      type="date"
                      id="edit-fecha"
                      v-model="editForm.fecha"
                      class="form-input"
                      required
                    />
                  </div>
                  <div class="form-group">
                    <label for="edit-hora" class="form-label">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/>
                      </svg>
                      Hora
                    </label>
                    <input 
                      type="time"
                      id="edit-hora"
                      v-model="editForm.hora"
                      class="form-input"
                      required
                    />
                  </div>
                </div>

                <!-- Tipo de Actividad (Modalidad) -->
                <div class="form-group">
                  <label for="edit-tipo" class="form-label">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                    Modalidad
                  </label>
                  <div class="tipo-selector">
                    <button 
                      type="button"
                      @click="editForm.tipo_actividad = 'campo'"
                      :class="['tipo-btn', 'tipo-campo', { active: editForm.tipo_actividad === 'campo' }]"
                    >
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 22c4.97 0 9-4.03 9-9-4.97 0-9 4.03-9 9zM5.6 10.25c0 1.38 1.12 2.5 2.5 2.5.53 0 1.01-.16 1.42-.44l-.02.19c0 1.38 1.12 2.5 2.5 2.5s2.5-1.12 2.5-2.5l-.02-.19c.4.28.89.44 1.42.44 1.38 0 2.5-1.12 2.5-2.5 0-1-.59-1.85-1.43-2.25.84-.4 1.43-1.25 1.43-2.25 0-1.38-1.12-2.5-2.5-2.5-.53 0-1.01.16-1.42.44l.02-.19C14.5 3.62 13.38 2.5 12 2.5S9.5 3.62 9.5 5l.02.19c-.4-.28-.89-.44-1.42-.44-1.38 0-2.5 1.12-2.5 2.5 0 1 .59 1.85 1.43 2.25-.84.4-1.43 1.25-1.43 2.25zM12 5.5c1.38 0 2.5 1.12 2.5 2.5s-1.12 2.5-2.5 2.5S9.5 9.38 9.5 8s1.12-2.5 2.5-2.5zM3 13c0 4.97 4.03 9 9 9 0-4.97-4.03-9-9-9z"/>
                      </svg>
                      <span>Campo</span>
                    </button>
                    <button 
                      type="button"
                      @click="editForm.tipo_actividad = 'gabinete'"
                      :class="['tipo-btn', 'tipo-gabinete', { active: editForm.tipo_actividad === 'gabinete' }]"
                    >
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
                      </svg>
                      <span>Gabinete</span>
                    </button>
                  </div>
                </div>

                <!-- Categoría de Actividad -->
                <div class="form-group">
                  <label for="edit-categoria" class="form-label">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/>
                    </svg>
                    Tipo de Actividad
                  </label>
                  <select 
                    id="edit-categoria"
                    v-model="editForm.categoria_actividad"
                    class="form-select"
                    :disabled="!editForm.tipo_actividad"
                    required
                  >
                    <option value="" disabled>{{ !editForm.tipo_actividad ? 'Primero selecciona la modalidad' : 'Selecciona el tipo de actividad' }}</option>
                    <option v-for="cat in categoriasActividad" :key="cat" :value="cat">{{ cat }}</option>
                  </select>
                </div>

                <!-- Campo Otro (condicional) -->
                <div v-if="editForm.categoria_actividad === 'Otro'" class="form-group">
                  <label for="edit-otro" class="form-label">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                    </svg>
                    Especifica la actividad
                  </label>
                  <input 
                    type="text"
                    id="edit-otro"
                    v-model="editForm.categoria_actividad_otro"
                    class="form-input"
                    placeholder="Describe el tipo de actividad..."
                    maxlength="100"
                    required
                  />
                </div>

                <!-- Descripción -->
                <div class="form-group">
                  <label for="edit-descripcion" class="form-label">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>
                    </svg>
                    Descripción
                    <span class="optional-label">(opcional)</span>
                  </label>
                  <textarea 
                    id="edit-descripcion"
                    v-model="editForm.descripcion"
                    class="form-textarea"
                    rows="3"
                    placeholder="Describe la actividad realizada..."
                    maxlength="1000"
                  ></textarea>
                  <span class="char-counter">{{ editForm.descripcion?.length || 0 }} / 1000</span>
                </div>
              </form>
            </div>
          </div>

          <!-- Footer con acciones -->
          <div class="modal-edit-footer">
            <button 
              type="button" 
              @click="cerrarModalEditar" 
              class="btn-cancel-edit"
              :disabled="isEditSaving"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
              Cancelar
            </button>
            <button 
              type="button"
              @click="guardarEdicion" 
              class="btn-save-edit"
              :disabled="isEditSaving || !editForm.tipo_actividad || !editForm.categoria_actividad || (editForm.categoria_actividad === 'Otro' && !editForm.categoria_actividad_otro?.trim())"
            >
              <svg v-if="!isEditSaving" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
                <polyline points="17 21 17 13 7 13 7 21"/>
                <polyline points="7 3 7 8 15 8"/>
              </svg>
              <svg v-else class="spinner-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
              </svg>
              {{ isEditSaving ? 'Guardando...' : 'Guardar Cambios' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Modal para notificar sobre actividad -->
    <Teleport to="body" v-if="showNotificarModal">
      <div class="modal-overlay-edit" @click="cerrarModalNotificar">
        <div class="modal-edit-container modal-notificar" @click.stop>
          <!-- Header -->
          <div class="modal-edit-header modal-notificar-header">
            <div class="header-icon-wrapper header-icon-notificar">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
              </svg>
            </div>
            <div class="header-text">
              <h3 class="header-title-notificar">Notificar sobre Actividad</h3>
              <span class="header-subtitle header-subtitle-notificar" v-if="actividadANotificar" style="display: flex; align-items: center; gap: 6px;">
                <span :class="['tipo-badge', getTipoClass(actividadANotificar.tipo_actividad)]" style="font-size: 9px; padding: 3px 7px;">
                  {{ actividadANotificar.tipo_actividad?.toUpperCase() }}
                </span>
                <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" style="flex-shrink: 0;">
                  <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                </svg>
                {{ actividadANotificar.usuario?.nombre_completo || 'Usuario' }}
              </span>
            </div>
            <button @click="cerrarModalNotificar" class="btn-close-edit btn-close-notificar" title="Cerrar">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>

          <!-- Contenido del modal con scroll -->
          <div class="modal-edit-scroll-area">
            <!-- Información de la actividad (readonly) -->
            <div class="modal-edit-readonly-section readonly-section-notificar">
              <h4 class="section-title section-title-notificar">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                  <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                Actividad seleccionada
              </h4>
              
              <div class="readonly-grid-3col" v-if="actividadANotificar">
                <div class="readonly-card">
                  <div class="readonly-card-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                  </div>
                  <div class="readonly-card-content">
                    <span class="readonly-card-label">Tipo</span>
                    <span class="readonly-card-value">
                      <span :class="['tipo-badge', getTipoClass(actividadANotificar.tipo_actividad)]" style="font-size: 11px; padding: 4px 10px;">
                        {{ actividadANotificar.tipo_actividad?.toUpperCase() }}
                      </span>
                    </span>
                  </div>
                </div>

                <div class="readonly-card">
                  <div class="readonly-card-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/>
                    </svg>
                  </div>
                  <div class="readonly-card-content">
                    <span class="readonly-card-label">Categoría</span>
                    <span class="readonly-card-value">{{ actividadANotificar.categoria_actividad || 'Sin categoría' }}</span>
                  </div>
                </div>

                <div class="readonly-card">
                  <div class="readonly-card-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M19 4h-1V2h-2v2H8V2H6v2H5c-1.11 0-1.99.9-1.99 2L3 20c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V9h14v11z"/>
                    </svg>
                  </div>
                  <div class="readonly-card-content">
                    <span class="readonly-card-label">Fecha</span>
                    <span class="readonly-card-value">{{ actividadANotificar.fecha_hora ? new Date(actividadANotificar.fecha_hora).toLocaleDateString('es-MX', { year: 'numeric', month: 'short', day: 'numeric' }) : 'Sin fecha' }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Formulario de notificación -->
            <div class="modal-edit-body">
              <h4 class="section-title section-title-notificar">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
                  <path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                </svg>
                Datos de la notificación
              </h4>
              
              <form @submit.prevent="enviarNotificacion" class="edit-form">
                <!-- Título (pre-llenado) -->
                <div class="form-group">
                  <label for="notif-titulo" class="form-label">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                    </svg>
                    Título *
                  </label>
                  <input 
                    type="text"
                    id="notif-titulo"
                    v-model="formNotificacion.titulo"
                    class="form-input"
                    maxlength="150"
                    placeholder="Ej: Reporte sobre tu actividad de campo"
                    required
                  />
                  <small class="char-count">{{ formNotificacion.titulo.length }}/150</small>
                </div>

                <!-- Subtítulo (generado automáticamente desde motivos) -->
                <div class="form-group" v-if="formNotificacion.motivos_atencion.length > 0">
                  <label class="form-label">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M19 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h4l3 3 3-3h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
                    </svg>
                    Motivos seleccionados (se enviarán en el subtítulo)
                  </label>
                  <div class="subtitulo-preview">
                    {{ motivosAtencionOpciones.filter(m => formNotificacion.motivos_atencion.includes(m.value)).map(m => m.label).join(', ') }}
                  </div>
                </div>

                <!-- Motivos de atención (checkboxes) -->
                <div class="form-group">
                  <label class="form-label">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
                    </svg>
                    Motivos de atención *
                  </label>
                  <div class="motivos-grid">
                    <label 
                      v-for="motivo in motivosAtencionOpciones"  
                      :key="motivo.value"
                      class="motivo-checkbox"
                      :class="{ selected: formNotificacion.motivos_atencion.includes(motivo.value) }"
                    >
                      <input 
                        type="checkbox"
                        :value="motivo.value"
                        v-model="formNotificacion.motivos_atencion"
                      />
                      <span>{{ motivo.label }}</span>
                    </label>
                  </div>
                  <small class="form-help">Selecciona al menos uno</small>
                </div>

                <!-- Descripción detallada -->
                <div class="form-group">
                  <label for="notif-descripcion" class="form-label">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>
                    </svg>
                    Mensaje detallado *
                  </label>
                  <textarea 
                    id="notif-descripcion"
                    v-model="formNotificacion.descripcion"
                    class="form-textarea form-textarea-notificacion"
                    rows="7"
                    placeholder="Escribe un mensaje detallado al usuario sobre por qué se le está notificando..."
                    required
                  ></textarea>
                  <div class="textarea-footer">
                    <small class="form-help">Explica claramente el motivo de la notificación</small>
                    <small class="char-count">{{ formNotificacion.descripcion.length }} caracteres</small>
                  </div>
                </div>

                <!-- Enlace URL (opcional) -->
                <div class="form-group">
                  <label for="notif-url" class="form-label">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"/>
                    </svg>
                    Enlace adicional (opcional)
                  </label>
                  <input 
                    type="url"
                    id="notif-url"
                    v-model="formNotificacion.enlace_url"
                    class="form-input"
                    placeholder="https://ejemplo.com"
                  />
                  <small class="form-help">URL con información adicional</small>
                </div>
              </form>
            </div>
          </div>

          <!-- Footer con acciones -->
          <div class="modal-edit-footer">
            <button 
              type="button" 
              @click="cerrarModalNotificar" 
              class="btn-cancel-edit"
              :disabled="enviandoNotificacion"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
              Cancelar
            </button>
            <button 
              type="button"
              @click="enviarNotificacion" 
              class="btn-save-edit btn-enviar-notificacion"
              :disabled="enviandoNotificacion || !formNotificacion.titulo.trim() || formNotificacion.motivos_atencion.length === 0 || !formNotificacion.descripcion.trim()"
            >
              <svg v-if="!enviandoNotificacion" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="m22 2-7 20-4-9-9-4Z"/>
                <path d="M22 2 11 13"/>
              </svg>
              <svg v-else class="spinner-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
              </svg>
              {{ enviandoNotificacion ? 'Enviando...' : 'Enviar Notificación' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import * as XLSX from 'xlsx'
import Sidebar from '../components/Sidebar.vue'
import { usuariosService } from '../services/usuariosService.js'
import authService from '../services/authService.js'
import notificacionesService from '../services/notificacionesService.js'

const router = useRouter()

// Estado de conexión
const isOnline = ref(navigator.onLine)

const API_URL = 'https://apipwa.sembrandodatos.com'
const registros = ref([])
const registrosFiltrados = ref([])
const usuariosDisponibles = ref([])
const usuariosFiltrados = ref([])
const loading = ref(false)
const error = ref('')
const filtroUsuario = ref('')
const filtroUsuarioTexto = ref('')
const mostrarSugerencias = ref(false)

// Variable reactiva para permisos del usuario actual (se actualiza en tiempo real)
const userPermisos = ref(authService.getCurrentUser()?.permisos || {})
const userRol = ref(authService.getCurrentUser()?.rol || '')

// Permiso para eliminar registros - REACTIVO
const puedeEliminarRegistros = computed(() => {
  // Admin siempre puede eliminar
  if (userRol.value === 'admin' || authService.isAdmin()) {
    console.log('✅ RegistrosView: Usuario es admin - puede eliminar')
    return true
  }
  // Verificar permiso específico usando la variable reactiva
  const tienePermiso = userPermisos.value?.registros_acciones === true
  console.log('🔍 RegistrosView: Verificando permiso registros_acciones:', tienePermiso, userPermisos.value)
  return tienePermiso
})

// Permiso para notificar sobre registros - REACTIVO
const puedeNotificarRegistros = computed(() => {
  // Admin siempre puede notificar
  if (userRol.value === 'admin' || authService.isAdmin()) {
    console.log('✅ RegistrosView: Usuario es admin - puede notificar')
    return true
  }
  // Verificar permiso específico usando la variable reactiva
  const tienePermiso = userPermisos.value?.registros_notificar === true
  console.log('🔍 RegistrosView: Verificando permiso registros_notificar:', tienePermiso, userPermisos.value)
  return tienePermiso
})

// Función para actualizar permisos cuando el evento es disparado
const actualizarPermisosUsuario = (event) => {
  const userData = event.detail
  console.log('🔄 RegistrosView: Permisos actualizados en tiempo real', userData)
  console.log('📋 RegistrosView: Nuevos permisos recibidos:', userData.permisos)
  userPermisos.value = userData.permisos || {}
  userRol.value = userData.rol || ''
  console.log('✅ RegistrosView: Variables reactivas actualizadas. registros_acciones =', userPermisos.value?.registros_acciones, ', registros_notificar =', userPermisos.value?.registros_notificar)
}

// Variables para ordenamiento
const campoOrdenamiento = ref('fecha') // Por defecto ordenar por fecha
const direccionOrdenamiento = ref('desc') // Por defecto más reciente primero

// Variables para filtros avanzados (nuevas)
const searchTerm = ref('')
const buscandoUsuario = ref(false)
const filtroFechaInicio = ref('')
const filtroFechaFin = ref('')
const filtroRapido = ref('')
const mostrarFiltrosAvanzados = ref(false)
const filtroTipoActividad = ref('')
const filtroConFoto = ref(false)
const filtroSinFoto = ref(false)
const filtroConDescripcion = ref(false)

// Variables para paginación y carga eficiente
const paginaActual = ref(1)
const registrosPorPagina = ref(50)
const paginaSalto = ref('')
const totalRegistrosServidor = ref(0)
const cargandoMas = ref(false)

// Función para cargar más registros cuando sea necesario
const cargarMasRegistros = async () => {
  if (cargandoMas.value) return
  
  try {
    cargandoMas.value = true
    const token = localStorage.getItem('admin_token')
    
    // Obtener filtro de territorio si el admin es territorial
    const territorioFilter = authService.getTerritorioFilter()
    
    console.log('📊 Cargando más registros...')
    
    // Construir parámetros con filtro territorial si aplica
    const params = {
      page: Math.ceil(registros.value.length / 1000) + 1,
      page_size: 1000,
      usuario_id: filtroUsuario.value || undefined
    }
    
    if (territorioFilter) {
      params.territorio = territorioFilter
    }
    
    const response = await axios.get(`${API_URL}/admin/registros`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      params,
      timeout: 30000
    })
    
    const { registros: registrosNuevos = [] } = response.data
    
    if (registrosNuevos.length > 0) {
      const registrosEnriquecidos = await usuariosService.enriquecerRegistrosConUsuarios(registrosNuevos)
      registros.value = [...registros.value, ...registrosEnriquecidos]
      console.log(`✅ Cargados ${registrosNuevos.length} registros adicionales`)
    }
    
  } catch (err) {
    console.error('Error cargando más registros:', err)
  } finally {
    cargandoMas.value = false
  }
}

// Variables para contadores de estadísticas
const actividadesHoy = ref('-')
const totalActividades = ref('-')

// Variables computadas para filtros
const maxDate = ref(new Date().toISOString().split('T')[0])
const hayFiltrosFechas = ref(false)
const usuariosUnicos = ref([])
const filtrosActivos = ref([])

const showModal = ref(false)
const modalTitle = ref('')
const modalType = ref('')
const selectedRegistro = ref(null)
const showLightbox = ref(false)
const lightboxImageUrl = ref('')
const showConfirmDelete = ref(false)
const registroAEliminar = ref(null)
const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref('success') // 'success' | 'error' | 'info'

// Variables para modal de edición
const showEditModal = ref(false)
const registroEditando = ref(null)
const editForm = ref({
  tipo_actividad: '',
  descripcion: '',
  categoria_actividad: '',
  categoria_actividad_otro: '',
  fecha: '',
  hora: ''
})
const isEditSaving = ref(false)

// Variables para modal de notificación sobre actividad
const showNotificarModal = ref(false)
const actividadANotificar = ref(null)
const formNotificacion = ref({
  titulo: '',
  subtitulo: '',
  descripcion: '',
  motivos_atencion: [],
  enlace_url: '',
  actividad_id: null,
  usuario_ids: []
})
const enviandoNotificacion = ref(false)

// Opciones de motivos de atención
const motivosAtencionOpciones = [
  { value: 'llamar_atencion', label: 'Llamar atención' },
  { value: 'correccion_requerida', label: 'Corrección requerida' },
  { value: 'informacion_faltante', label: 'Información faltante' },
  { value: 'revision_urgente', label: 'Revisión urgente' },
  { value: 'documentacion_pendiente', label: 'Documentación pendiente' },
  { value: 'seguimiento', label: 'Seguimiento necesario' },
  { value: 'felicitacion', label: 'Felicitación por buen trabajo' },
  { value: 'otro', label: 'Otro motivo' }
]

// Categorías de actividad (igual que en pwasuper)
const categoriasActividad = [
  "Acompañamiento técnico",
  "Productivas directas",
  "Ahorro y trámites financieros",
  "Capacitación / talleres / cursos",
  "Difusión y comunicación",
  "Eventos comunitarios / ferias / tianguis",
  "Reuniones y asambleas",
  "Trabajo administrativo y captura",
  "Viveros y biofábricas",
  "Otro"
]

let map = null

// Computed properties para paginación
const totalPaginas = computed(() => {
  return Math.ceil(registrosFiltrados.value.length / registrosPorPagina.value)
})

const indiceInicio = computed(() => {
  return (paginaActual.value - 1) * registrosPorPagina.value
})

const indiceFin = computed(() => {
  return indiceInicio.value + registrosPorPagina.value
})

const registrosPaginados = computed(() => {
  return registrosFiltrados.value.slice(indiceInicio.value, indiceFin.value)
})

const paginasVisibles = computed(() => {
  const paginas = []
  const inicio = Math.max(2, paginaActual.value - 2)
  const fin = Math.min(totalPaginas.value - 1, paginaActual.value + 2)
  
  for (let i = inicio; i <= fin; i++) {
    if (i !== 1 && i !== totalPaginas.value) {
      paginas.push(i)
    }
  }
  
  return paginas
})

const mostrarPagina = (numeroPagina) => {
  if (numeroPagina === 1) {
    return totalPaginas.value > 1 && (paginaActual.value <= 4 || numeroPagina === 1)
  }
  if (numeroPagina === totalPaginas.value) {
    return totalPaginas.value > 1 && (paginaActual.value >= totalPaginas.value - 3 || numeroPagina === totalPaginas.value)
  }
  return false
}

onMounted(() => {
  cargarRegistros()
  
  // Escuchar cambios de conexión
  window.addEventListener('online', () => {
    isOnline.value = true
  })
  
  window.addEventListener('offline', () => {
    isOnline.value = false
  })
  
  // Escuchar actualización de permisos en tiempo real
  window.addEventListener('user-session-updated', actualizarPermisosUsuario)
  
  // Cargar Leaflet desde CDN
  if (!window.L) {
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
    document.head.appendChild(link)
    
    const script = document.createElement('script')
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
    document.head.appendChild(script)
  }
})

// Event listener para cerrar lightbox con ESC
const handleKeyDown = (event) => {
  if (event.key === 'Escape' && showLightbox.value) {
    cerrarLightbox()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
  window.removeEventListener('user-session-updated', actualizarPermisosUsuario)
})

const cargarRegistros = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const token = localStorage.getItem('admin_token')
    
    // Obtener filtro de territorio si el admin es territorial
    const territorioFilter = authService.getTerritorioFilter()
    
    if (territorioFilter) {
      console.log(`📊 Solicitando registros del territorio: ${territorioFilter}...`)
    } else {
      console.log('📊 Solicitando todos los registros (admin global)...')
    }
    console.time('Carga de registros')
    
    // Construir parámetros con filtro territorial si aplica
    const params = {
      page: 1,
      page_size: 1000, // Paginación optimizada
      usuario_id: filtroUsuario.value || undefined
    }
    
    if (territorioFilter) {
      params.territorio = territorioFilter
    }
    
    // Usar el nuevo endpoint optimizado /admin/registros
    const response = await axios.get(`${API_URL}/admin/registros`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      params,
      timeout: 30000 // Timeout de 30 segundos
    })
    
    console.log('✅ Respuesta de la API obtenida exitosamente:', response.data)
    
    // El nuevo endpoint devuelve un objeto con paginación
    const { registros: registrosRaw = [], total = 0 } = response.data
    console.log(`🔢 Recibidos ${registrosRaw.length} registros de ${total} totales`)
    
    // Enriquecer registros con información de usuarios
    registros.value = await usuariosService.enriquecerRegistrosConUsuarios(registrosRaw)
    registrosFiltrados.value = registros.value
    
    // Aplicar ordenamiento inicial
    aplicarOrdenamiento()
    
    // Extraer usuarios únicos para el filtro (con información completa)
    const usuariosUnicosLista = []
    const usuariosVistos = new Set()
    
    registros.value.forEach(registro => {
      if (!usuariosVistos.has(registro.usuario_id)) {
        usuariosVistos.add(registro.usuario_id)
        usuariosUnicosLista.push({
          id: registro.usuario_id,
          nombre_completo: registro.usuario?.nombre_completo || `Usuario ${registro.usuario_id}`
        })
      }
    })
    
    usuariosDisponibles.value = usuariosUnicosLista.sort((a, b) => a.id - b.id)
    usuariosFiltrados.value = usuariosDisponibles.value
    
    console.log('Registros enriquecidos cargados:', registros.value)
    console.timeEnd('Carga de registros')
    
    // Estadísticas rápidas
    const conFotos = registros.value.filter(r => r.foto_url).length;
    const conDescripcion = registros.value.filter(r => r.descripcion && r.descripcion.trim() !== '').length;
    const totalUsuariosUnicos = new Set(registros.value.map(r => r.usuario_id)).size;
    
    console.log(`📈 Estadísticas: ${registros.value.length.toLocaleString('es')} registros cargados | ${totalUsuariosUnicos} usuarios | ${conFotos} con foto (${(conFotos/registros.value.length*100).toFixed(1)}%) | ${conDescripcion} con descripción (${(conDescripcion/registros.value.length*100).toFixed(1)}%)`);
    
    // Aplicar filtros iniciales
    filtrarRegistros()
    
    // Calcular estadísticas
    calcularEstadisticas()
    
  } catch (err) {
    console.error('Error al cargar registros:', err)
    if (err.code === 'ECONNABORTED') {
      error.value = 'Timeout: La consulta está tardando demasiado. Intenta filtrar por usuario específico.'
    } else if (err.response?.status === 401) {
      logout()
    } else if (err.response?.status === 503) {
      error.value = 'Servicio temporalmente no disponible. Inténtalo de nuevo en unos momentos.'
    } else {
      error.value = 'Error al cargar los registros: ' + (err.response?.data?.detail || err.message)
    }
  } finally {
    loading.value = false
  }
}

// Función para calcular estadísticas
const calcularEstadisticas = async () => {
  try {
    // Obtener estadísticas del servidor para datos precisos
    const token = localStorage.getItem('admin_token')
    
    // Obtener filtro de territorio si el admin es territorial
    const territorioFilter = authService.getTerritorioFilter()
    
    try {
      // Construir URL con parámetro de territorio si aplica
      let url = `${API_URL}/estadisticas`
      if (territorioFilter) {
        url += `?territorio=${encodeURIComponent(territorioFilter)}`
        console.log(`📊 Obteniendo estadísticas del territorio: ${territorioFilter}`)
      } else {
        console.log('📊 Obteniendo estadísticas globales')
      }
      
      const response = await axios.get(url, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000 // Timeout corto para estadísticas
      })
      
      const stats = response.data.estadisticas
      
      if (stats) {
        totalActividades.value = stats.total_registros?.toLocaleString('es') || '0'
        actividadesHoy.value = stats.registros_hoy?.toLocaleString('es') || '0'
        totalRegistrosServidor.value = stats.total_registros || 0
        
        const territorioInfo = stats.territorio ? ` (territorio: ${stats.territorio})` : ' (global)'
        console.log(`✅ Estadísticas cargadas${territorioInfo}: ${totalActividades.value} total, ${actividadesHoy.value} hoy`)
      }
    } catch (statsError) {
      console.warn('⚠️ No se pudieron obtener estadísticas del servidor, usando datos locales...')
      // Fallback a cálculo local
      calcularEstadisticasLocales()
    }
    
  } catch (error) {
    console.error('Error al calcular estadísticas:', error)
    calcularEstadisticasLocales()
  }
}

const calcularEstadisticasLocales = () => {
  try {
    // Total de actividades (registros locales)
    totalActividades.value = registros.value.length.toLocaleString('es')
    
    // Actividades de hoy
    const hoy = new Date()
    hoy.setHours(0, 0, 0, 0)
    const mañana = new Date(hoy)
    mañana.setDate(mañana.getDate() + 1)
    
    const registrosHoy = registros.value.filter(registro => {
      const fechaRegistro = new Date(registro.fecha_hora)
      return fechaRegistro >= hoy && fechaRegistro < mañana
    })
    
    actividadesHoy.value = registrosHoy.length.toLocaleString('es')
    
    console.log(`📊 Estadísticas locales: ${totalActividades.value} total, ${actividadesHoy.value} hoy`)
  } catch (error) {
    console.error('Error al calcular estadísticas locales:', error)
    actividadesHoy.value = '0'
    totalActividades.value = '0'
  }
}

// Variable para debounce de búsqueda
let busquedaTimeout = null

// Función para buscar usuarios en el backend y cargar sus registros
const buscarUsuarioEnBackend = async (termino) => {
  if (!termino || termino.length < 3) return []
  
  buscandoUsuario.value = true
  
  try {
    const token = localStorage.getItem('admin_token')
    const terminoLimpio = termino.trim()
    
    console.log(`\n🔍 ===== INICIANDO BÚSQUEDA =====`)
    console.log(`📝 Término de búsqueda: "${terminoLimpio}"`)
    console.log(`📊 Registros actuales en memoria: ${registros.value.length}`)
    
    // Hacer UNA SOLA búsqueda pasando el término en todos los campos (backend usa OR)
    console.log(`📡 Llamando al backend con búsqueda unificada (OR)...`)
    
    const response = await axios.get(`${API_URL}/api/buscar-usuarios`, {
      headers: { 'Authorization': `Bearer ${token}` },
      params: { 
        nombre: terminoLimpio,
        correo: terminoLimpio,
        curp: terminoLimpio
      },
      timeout: 15000
    })
    
    const usuariosEncontrados = response.data?.usuarios || []
    
    console.log(`\n✅ Total usuarios únicos encontrados: ${usuariosEncontrados.length}`)
    
    if (usuariosEncontrados.length === 0) {
      console.log('❌ No se encontraron usuarios con ese criterio')
      console.log('💡 Verifica que:')
      console.log('   - La CURP, nombre o correo existan en la BD')
      console.log('   - El backend esté respondiendo correctamente')
      return []
    }
    
    // Mostrar info de usuarios encontrados
    usuariosEncontrados.forEach((u, index) => {
      console.log(`   👤 ${index + 1}. ID: ${u.id} | Nombre: ${u.nombre_completo} | CURP: ${u.curp || 'N/A'} | Correo: ${u.correo}`)
    })
    
    // CAMBIO: Limpiar registros previos para mostrar SOLO los del usuario buscado
    console.log(`\n🗑️ Limpiando registros previos para mostrar solo los del usuario buscado...`)
    registros.value = []
    
    // Cargar registros de cada usuario encontrado
    console.log(`\n📥 Cargando registros de ${usuariosEncontrados.length} usuario(s)...`)
    
    let totalRegistrosNuevos = 0
    
    for (const usuario of usuariosEncontrados) {
      if (usuario.id) {
        console.log(`   ⬇️ Cargando registros del usuario ${usuario.id} (${usuario.nombre_completo})...`)
        const antes = registros.value.length
        await cargarRegistrosParaUsuario(usuario.id)
        const despues = registros.value.length
        totalRegistrosNuevos += (despues - antes)
      }
    }
    
    console.log(`\n📊 Total de registros cargados: ${registros.value.length}`)
    if (totalRegistrosNuevos > 0) {
      console.log(`   ✅ ${totalRegistrosNuevos} registros del usuario buscado`)
    } else {
      console.log(`   ⚠️ El usuario no tiene registros de actividades`)
    }
    console.log(`===== FIN DE BÚSQUEDA =====\n`)
    
    return usuariosEncontrados
    
  } catch (error) {
    console.error('❌ Error buscando usuario en backend:', error)
    if (error.response) {
      console.error(`   📛 Status: ${error.response.status}`)
      console.error(`   📛 Detail: ${error.response.data?.detail || error.message}`)
    }
    return []
  } finally {
    buscandoUsuario.value = false
  }
}

// Función de búsqueda en tiempo real con debounce
const buscarEnTiempoReal = async () => {
  // Limpiar timeout anterior
  if (busquedaTimeout) {
    clearTimeout(busquedaTimeout)
  }
  
  const termino = searchTerm.value?.trim() || ''
  
  // Si el término de búsqueda tiene 3 o más caracteres, buscar en el backend
  if (termino.length >= 3) {
    console.log(`⏳ Iniciando búsqueda en 500ms para: "${termino}"`)
    busquedaTimeout = setTimeout(async () => {
      console.log(`🚀 Ejecutando búsqueda para: "${termino}"`)
      const usuariosEncontrados = await buscarUsuarioEnBackend(termino)
      
      // CAMBIO: Después de cargar los registros del usuario, mostrarlos directamente
      // NO aplicar filtro local porque ya tenemos exactamente los registros que queremos
      if (usuariosEncontrados.length > 0) {
        console.log(`✅ Mostrando todos los registros del usuario encontrado`)
        registrosFiltrados.value = [...registros.value]
        aplicarOrdenamiento()
        actualizarUsuariosUnicos()
        actualizarFiltrosActivos()
      } else {
        console.log(`⚠️ No se encontraron usuarios, mostrando registros vacíos`)
        registrosFiltrados.value = []
      }
      
      console.log(`✅ Búsqueda completada. Registros mostrados: ${registrosFiltrados.value.length}`)
    }, 500) // Esperar 500ms después de que el usuario deje de escribir
  } else if (termino.length === 0) {
    // Si se borra la búsqueda, recargar todos los registros
    console.log('🔄 Búsqueda vacía, recargando registros...')
    await cargarRegistros()
  } else {
    // Si es menos de 3 caracteres, solo filtrar localmente
    console.log(`📝 Búsqueda corta (${termino.length} caracteres), solo filtro local`)
    filtrarRegistros()
  }
}

const filtrarRegistros = async () => {
  console.log(`\n🔍 ===== INICIANDO FILTRADO =====`)
  console.log(`📊 Total de registros en memoria: ${registros.value.length}`)
  
  let filtrados = [...registros.value]
  
  // Actualizar usuariosUnicos basado en los registros actuales
  actualizarUsuariosUnicos()

  // Si cambió el filtro de usuario, recargar del servidor
  if (filtroUsuario.value && !registros.value.some(r => r.usuario_id === parseInt(filtroUsuario.value))) {
    await cargarRegistrosParaUsuario(parseInt(filtroUsuario.value))
    filtrados = [...registros.value]
  }

  // Filtro por texto de búsqueda (ahora incluye CURP)
  // NOTA: Este filtro solo se aplica cuando NO se ha hecho una búsqueda de usuario
  // Si se buscó un usuario, los registros ya están filtrados por usuario
  const terminoBusqueda = searchTerm.value?.trim() || ''
  if (terminoBusqueda && terminoBusqueda.length < 3) {
    // Solo filtrar localmente si es una búsqueda corta (no se fue al backend)
    const termino = terminoBusqueda.toLowerCase()
    console.log(`🔎 Aplicando filtro local corto: "${termino}"`)
    
    const antesDeFiltrar = filtrados.length
    
    filtrados = filtrados.filter(registro => {
      // Asegurarse de que el registro tenga información de usuario
      if (!registro.usuario) {
        return false
      }
      
      const nombre = (registro.usuario.nombre_completo || '').toLowerCase()
      const correo = (registro.usuario.correo || '').toLowerCase()
      const curp = (registro.usuario.curp || '').toLowerCase()
      const descripcion = (registro.descripcion || '').toLowerCase()
      const latitud = registro.latitud ? registro.latitud.toString() : ''
      const longitud = registro.longitud ? registro.longitud.toString() : ''
      
      const coincide = 
        nombre.includes(termino) ||
        correo.includes(termino) ||
        curp.includes(termino) ||
        descripcion.includes(termino) ||
        latitud.includes(termino) ||
        longitud.includes(termino)
      
      return coincide
    })
    
    console.log(`   ✅ Registros después de búsqueda: ${filtrados.length} (filtrados: ${antesDeFiltrar - filtrados.length})`)
    
    // Mostrar algunos ejemplos de registros que coinciden
    if (filtrados.length > 0 && filtrados.length <= 5) {
      console.log(`   📋 Registros encontrados:`)
      filtrados.forEach((r, i) => {
        console.log(`      ${i+1}. ${r.usuario?.nombre_completo} (${r.usuario?.curp || 'Sin CURP'}) - ${r.descripcion?.substring(0, 30) || 'Sin descripción'}`)
      })
    }
  }

  // Filtro por usuario específico
  if (filtroUsuario.value) {
    filtrados = filtrados.filter(registro => 
      registro.usuario_id === parseInt(filtroUsuario.value)
    )
  }
  
  // Filtro por tipo de actividad
  if (filtroTipoActividad.value) {
    filtrados = filtrados.filter(registro => {
      const tipo = registro.tipo_actividad || 'campo' // Default para registros antiguos
      return tipo.toLowerCase() === filtroTipoActividad.value.toLowerCase()
    })
  }
  
  // Filtros por estado de foto y descripción
  if (filtroConFoto.value) {
    filtrados = filtrados.filter(registro => registro.foto_url)
  }
  
  if (filtroSinFoto.value) {
    filtrados = filtrados.filter(registro => !registro.foto_url)
  }
  
  if (filtroConDescripcion.value) {
    filtrados = filtrados.filter(registro => 
      registro.descripcion && registro.descripcion.trim() !== ''
    )
  }

  // Filtros por fechas rápidas
  if (filtroRapido.value) {
    const hoy = new Date()
    hoy.setHours(0, 0, 0, 0)
    
    switch (filtroRapido.value) {
      case 'hoy':
        const fechaHoy = hoy.toISOString().split('T')[0]
        filtrados = filtrados.filter(registro => {
          const fechaRegistro = new Date(registro.fecha_hora).toISOString().split('T')[0]
          return fechaRegistro === fechaHoy
        })
        break
      case 'ayer':
        const ayer = new Date(hoy)
        ayer.setDate(ayer.getDate() - 1)
        const fechaAyer = ayer.toISOString().split('T')[0]
        filtrados = filtrados.filter(registro => {
          const fechaRegistro = new Date(registro.fecha_hora).toISOString().split('T')[0]
          return fechaRegistro === fechaAyer
        })
        break
      case 'semana':
        const inicioSemana = new Date(hoy)
        inicioSemana.setDate(hoy.getDate() - hoy.getDay())
        filtrados = filtrados.filter(registro => {
          const fechaRegistro = new Date(registro.fecha_hora)
          return fechaRegistro >= inicioSemana && fechaRegistro <= hoy
        })
        break
      case 'mes':
        const inicioMes = new Date(hoy.getFullYear(), hoy.getMonth(), 1)
        filtrados = filtrados.filter(registro => {
          const fechaRegistro = new Date(registro.fecha_hora)
          return fechaRegistro >= inicioMes && fechaRegistro <= hoy
        })
        break
    }
  } 
  // Filtro por rango de fechas personalizado
  else if (filtroFechaInicio.value && filtroFechaFin.value) {
    const fechaInicio = new Date(filtroFechaInicio.value)
    fechaInicio.setHours(0, 0, 0, 0)
    
    const fechaFin = new Date(filtroFechaFin.value)
    fechaFin.setHours(23, 59, 59, 999)
    
    filtrados = filtrados.filter(registro => {
      const fechaRegistro = new Date(registro.fecha_hora)
      return fechaRegistro >= fechaInicio && fechaRegistro <= fechaFin
    })
  }

  registrosFiltrados.value = filtrados
  
  console.log(`\n📊 RESULTADO FINAL DEL FILTRADO:`)
  console.log(`   🗂️ Registros mostrados: ${filtrados.length}`)
  console.log(`   🔢 Usuarios únicos: ${new Set(filtrados.map(r => r.usuario_id)).size}`)
  
  if (searchTerm.value && filtrados.length === 0) {
    console.warn(`   ⚠️ No se encontraron registros para "${searchTerm.value}"`)
    console.log(`   💡 Sugerencia: Verifica que el usuario tenga registros en la base de datos`)
  }
  
  console.log(`===== FIN DE FILTRADO =====\n`)
  
  // Resetear a la primera página cuando se aplican filtros
  paginaActual.value = 1
  
  actualizarFiltrosActivos()
  aplicarOrdenamiento()
}

// Nueva función para cargar registros de un usuario específico
const cargarRegistrosParaUsuario = async (usuarioId) => {
  if (!usuarioId) return
  
  try {
    const token = localStorage.getItem('admin_token')
    
    // Obtener filtro de territorio si el admin es territorial
    const territorioFilter = authService.getTerritorioFilter()
    
    console.log(`      🔍 Solicitando registros del usuario ${usuarioId} al backend...`)
    
    // Construir parámetros con filtro territorial si aplica
    const params = {
      page: 1,
      page_size: 5000, // Aumentar para obtener más registros
      usuario_id: usuarioId
    }
    
    if (territorioFilter) {
      params.territorio = territorioFilter
    }
    
    const response = await axios.get(`${API_URL}/admin/registros`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      params,
      timeout: 20000 // Aumentar timeout
    })
    
    const { registros: registrosUsuario = [], total = 0 } = response.data
    
    console.log(`      📦 Backend respondió: ${registrosUsuario.length} registros de ${total} totales`)
    
    if (registrosUsuario.length > 0) {
      console.log(`      🔄 Enriqueciendo registros con información de usuarios...`)
      const registrosEnriquecidos = await usuariosService.enriquecerRegistrosConUsuarios(registrosUsuario)
      
      // Combinar con registros existentes (evitar duplicados)
      const idsExistentes = new Set(registros.value.map(r => r.id))
      const registrosNuevos = registrosEnriquecidos.filter(r => !idsExistentes.has(r.id))
      
      console.log(`      📊 Registros nuevos: ${registrosNuevos.length} | Ya existentes: ${registrosEnriquecidos.length - registrosNuevos.length}`)
      
      if (registrosNuevos.length > 0) {
        registros.value = [...registros.value, ...registrosNuevos]
        console.log(`      ✅ Total registros en memoria ahora: ${registros.value.length}`)
        
        // Verificar que los registros tengan información del usuario con CURP
        const registroConCurp = registrosNuevos.find(r => r.usuario?.curp)
        if (registroConCurp) {
          console.log(`      📋 Ejemplo de registro con CURP: ${registroConCurp.usuario.nombre_completo} - ${registroConCurp.usuario.curp}`)
        }
      } else {
        console.log(`      ℹ️ No hay registros nuevos para agregar (todos ya existían)`)
      }
    } else {
      console.log(`      ⚠️ No se encontraron registros para el usuario ${usuarioId}`)
    }
    
  } catch (error) {
    console.error(`      ❌ Error cargando registros del usuario ${usuarioId}:`, error)
    if (error.response) {
      console.error(`      📛 Status: ${error.response.status} | Message: ${error.response.data?.detail || error.message}`)
    }
  }
}

const actualizarUsuariosUnicos = () => {
  const usuariosMap = new Map()
  registros.value.forEach(registro => {
    if (registro.usuario && !usuariosMap.has(registro.usuario_id)) {
      usuariosMap.set(registro.usuario_id, {
        id: registro.usuario_id,
        nombre_completo: registro.usuario.nombre_completo || `Usuario ${registro.usuario_id}`
      })
    }
  })
  usuariosUnicos.value = Array.from(usuariosMap.values()).sort((a, b) => a.id - b.id)
}

const actualizarFiltrosActivos = () => {
  const activos = []
  
  if (searchTerm.value) {
    activos.push({ tipo: 'busqueda', valor: searchTerm.value, label: `Búsqueda: "${searchTerm.value}"` })
  }
  
  if (filtroFechaInicio.value && filtroFechaFin.value) {
    activos.push({ 
      tipo: 'fechaRango', 
      valor: `${filtroFechaInicio.value}|${filtroFechaFin.value}`, 
      label: `Fecha: ${filtroFechaInicio.value} - ${filtroFechaFin.value}` 
    })
  }
  
  if (filtroRapido.value) {
    const labels = { hoy: 'Hoy', ayer: 'Ayer', semana: 'Esta semana', mes: 'Este mes' }
    activos.push({ tipo: 'fechaRapida', valor: filtroRapido.value, label: labels[filtroRapido.value] })
  }
  
  if (filtroUsuario.value) {
    const usuario = usuariosUnicos.value.find(u => u.id === parseInt(filtroUsuario.value))
    activos.push({ 
      tipo: 'usuario', 
      valor: filtroUsuario.value, 
      label: `Usuario: ${usuario?.nombre_completo || 'Usuario ' + filtroUsuario.value}` 
    })
  }
  
  if (filtroTipoActividad.value) {
    const tipoLabel = filtroTipoActividad.value === 'campo' ? 'Campo' : 'Gabinete'
    activos.push({ 
      tipo: 'tipoActividad', 
      valor: filtroTipoActividad.value, 
      label: `Tipo: ${tipoLabel}` 
    })
  }
  
  if (filtroConFoto.value) {
    activos.push({ tipo: 'conFoto', valor: true, label: 'Con foto' })
  }
  
  if (filtroSinFoto.value) {
    activos.push({ tipo: 'sinFoto', valor: true, label: 'Sin foto' })
  }
  
  if (filtroConDescripcion.value) {
    activos.push({ tipo: 'conDescripcion', valor: true, label: 'Con descripción' })
  }
  
  filtrosActivos.value = activos
  
  // Actualizar hayFiltrosFechas
  hayFiltrosFechas.value = !!(filtroFechaInicio.value || filtroFechaFin.value || filtroRapido.value)
}

// Nuevas funciones para filtros avanzados
const limpiarBusqueda = async () => {
  searchTerm.value = ''
  console.log('🔄 Limpiando búsqueda, recargando registros iniciales...')
  await cargarRegistros()
}

const seleccionarFechaRapida = (tipo) => {
  filtroRapido.value = filtroRapido.value === tipo ? '' : tipo
  filtroFechaInicio.value = ''
  filtroFechaFin.value = ''
  filtrarRegistros()
}

const limpiarFiltrosFechas = () => {
  filtroFechaInicio.value = ''
  filtroFechaFin.value = ''
  filtroRapido.value = ''
  filtrarRegistros()
}

const quitarFiltro = (tipo, valor) => {
  switch (tipo) {
    case 'busqueda':
      searchTerm.value = ''
      break
    case 'fechaRango':
      filtroFechaInicio.value = ''
      filtroFechaFin.value = ''
      break
    case 'fechaRapida':
      filtroRapido.value = ''
      break
    case 'usuario':
      filtroUsuario.value = ''
      break
    case 'tipoActividad':
      filtroTipoActividad.value = ''
      break
    case 'conFoto':
      filtroConFoto.value = false
      break
    case 'sinFoto':
      filtroSinFoto.value = false
      break
    case 'conDescripcion':
      filtroConDescripcion.value = false
      break
  }
  filtrarRegistros()
}

const limpiarTodosFiltros = () => {
  searchTerm.value = ''
  filtroFechaInicio.value = ''
  filtroFechaFin.value = ''
  filtroRapido.value = ''
  filtroUsuario.value = ''
  filtroTipoActividad.value = ''
  filtroConFoto.value = false
  filtroSinFoto.value = false
  filtroConDescripcion.value = false
  filtroUsuarioTexto.value = ''
  mostrarSugerencias.value = false
  paginaActual.value = 1 // Resetear paginación
  filtrarRegistros()
}

// Funciones de paginación
const irAPagina = (numeroPagina) => {
  if (numeroPagina >= 1 && numeroPagina <= totalPaginas.value) {
    paginaActual.value = numeroPagina
    
    // Scroll suave al inicio de la tabla
    const tableContainer = document.querySelector('.table-container')
    if (tableContainer) {
      tableContainer.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
      })
    }
  }
}

const cambiarRegistrosPorPagina = () => {
  // Recalcular qué página mostrar para mantener aproximadamente el mismo registro visible
  const registroActual = indiceInicio.value + 1
  const nuevaPagina = Math.ceil(registroActual / registrosPorPagina.value)
  paginaActual.value = Math.max(1, Math.min(nuevaPagina, totalPaginas.value))
}

const saltarAPagina = () => {
  if (paginaSalto.value && paginaSalto.value >= 1 && paginaSalto.value <= totalPaginas.value) {
    irAPagina(paginaSalto.value)
    paginaSalto.value = ''
  }
}

const exportarRegistros = (tipo) => {
  if (tipo === 'csv') {
    exportarCSV()
  } else if (tipo === 'excel') {
    exportarExcel()
  }
}

const exportarCSV = () => {
  // Crear encabezados
  const encabezados = [
    'ID',
    'Usuario',
    'Email',
    'Tipo Actividad',
    'Fecha y Hora',
    'Latitud',
    'Longitud',
    'Descripción',
    'Foto URL'
  ].join(',')

  // Crear filas de datos
  const filas = registrosFiltrados.value.map(r => {
    return [
      `"${r.id}"`,
      `"${r.usuario?.nombre_completo || 'Usuario ' + r.usuario_id}"`,
      `"${r.usuario?.correo || 'No disponible'}"`,
      `"${getTipoLabel(r.tipo_actividad)}"`,
      `"${formatFecha(r.fecha_hora)}"`,
      `"${r.latitud || ''}"`,
      `"${r.longitud || ''}"`,
      `"${r.descripcion || ''}"`,
      `"${r.foto_url || ''}"`
    ].join(',')
  })

  // Combinar encabezados y filas
  const contenidoCSV = [encabezados, ...filas].join('\n')
  
  // Crear y descargar el archivo
  const blob = new Blob([contenidoCSV], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.setAttribute('download', `registros_${new Date().toISOString().split('T')[0]}.csv`)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

const exportarExcel = () => {
  try {
    // Crear un nuevo libro de trabajo
    const workbook = XLSX.utils.book_new()
    
    // Obtener datos filtrados
    const registrosParaExportar = registrosFiltrados.value
    
    // Estadísticas generales
    const estadisticas = {
      totalRegistros: registrosParaExportar.length,
      usuariosUnicos: [...new Set(registrosParaExportar.map(r => r.usuario_id))].length,
      conFotografia: registrosParaExportar.filter(r => r.foto_url).length,
      conDescripcion: registrosParaExportar.filter(r => r.descripcion && r.descripcion.trim()).length
    }
    
    // === HOJA 1: RESUMEN EJECUTIVO ===
    const resumenData = [
      ['REPORTE DE REGISTROS - SISTEMA PWA SEMBRANDO VIDA'],
      [''],
      ['📊 RESUMEN EJECUTIVO'],
      [''],
      ['Fecha de Generación:', new Date().toLocaleDateString('es-ES', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })],
      ['Hora de Generación:', new Date().toLocaleTimeString('es-ES')],
      [''],
      ['📈 ESTADÍSTICAS GENERALES'],
      [''],
      ['Métrica', 'Valor', 'Descripción'],
      ['Total de Registros', estadisticas.totalRegistros, 'Cantidad total de registros en el reporte'],
      ['Usuarios Únicos', estadisticas.usuariosUnicos, 'Número de usuarios diferentes que han creado registros'],
      ['Registros con Fotografía', estadisticas.conFotografia, 'Registros que incluyen archivo de imagen'],
      ['Registros con Descripción', estadisticas.conDescripcion, 'Registros que incluyen texto descriptivo'],
      ['Porcentaje con Foto', `${((estadisticas.conFotografia / estadisticas.totalRegistros) * 100).toFixed(1)}%`, 'Porcentaje de registros que incluyen fotografía'],
      ['Porcentaje con Descripción', `${((estadisticas.conDescripcion / estadisticas.totalRegistros) * 100).toFixed(1)}%`, 'Porcentaje de registros con información descriptiva'],
      [''],
      ['🔍 FILTROS APLICADOS'],
      [''],
      ['Filtro', 'Estado'],
      ['Búsqueda por texto', searchTerm.value || 'Sin filtro'],
      ['Filtro de fecha', (filtroFechaInicio.value && filtroFechaFin.value) ? `${filtroFechaInicio.value} - ${filtroFechaFin.value}` : filtroRapido.value || 'Sin filtro'],
      ['Usuario específico', filtroUsuario.value ? usuariosUnicos.value.find(u => u.id === parseInt(filtroUsuario.value))?.nombre_completo || 'Usuario no encontrado' : 'Todos los usuarios'],
      ['Con fotografía', filtroConFoto.value ? 'Sí' : 'Sin filtro'],
      ['Sin fotografía', filtroSinFoto.value ? 'Sí' : 'Sin filtro'],
      ['Con descripción', filtroConDescripcion.value ? 'Sí' : 'Sin filtro'],
    ]
    
    // === HOJA 2: DATOS DETALLADOS ===
    const datosDetallados = [
      ['ID', 'Usuario', 'Email', 'Tipo Actividad', 'Fecha y Hora', 'Latitud', 'Longitud', 'Descripción', 'Estado Foto', 'URL Foto']
    ]
    
    registrosParaExportar.forEach(registro => {
      datosDetallados.push([
        `REG-${registro.id.toString().padStart(5, '0')}`,
        registro.usuario?.nombre_completo || `Usuario ${registro.usuario_id}`,
        registro.usuario?.correo || 'No disponible',
        getTipoLabel(registro.tipo_actividad),
        formatFecha(registro.fecha_hora),
        parseFloat(registro.latitud).toFixed(6),
        parseFloat(registro.longitud).toFixed(6),
        registro.descripcion || 'Sin descripción',
        registro.foto_url ? 'Con Fotografía' : 'Sin Fotografía',
        registro.foto_url ? `${API_URL}/${registro.foto_url}` : 'No disponible'
      ])
    })
    
    // === HOJA 3: ANÁLISIS POR USUARIO ===
    const usuariosAnalisis = [
      ['👤 ANÁLISIS POR USUARIO'],
      [''],
      ['Usuario', 'ID Usuario', 'Total Registros', 'Con Foto', 'Con Descripción', 'Último Registro']
    ]
    
    const analisisPorUsuario = new Map()
    
    registrosParaExportar.forEach(registro => {
      const usuarioId = registro.usuario_id
      if (!analisisPorUsuario.has(usuarioId)) {
        analisisPorUsuario.set(usuarioId, {
          nombre: registro.usuario?.nombre_completo || `Usuario ${usuarioId}`,
          id: usuarioId,
          total: 0,
          conFoto: 0,
          conDescripcion: 0,
          ultimoRegistro: null
        })
      }
      
      const usuario = analisisPorUsuario.get(usuarioId)
      usuario.total++
      if (registro.foto_url) usuario.conFoto++
      if (registro.descripcion && registro.descripcion.trim()) usuario.conDescripcion++
      
      const fechaRegistro = new Date(registro.fecha_hora)
      if (!usuario.ultimoRegistro || fechaRegistro > new Date(usuario.ultimoRegistro)) {
        usuario.ultimoRegistro = registro.fecha_hora
      }
    })
    
    Array.from(analisisPorUsuario.values())
      .sort((a, b) => b.total - a.total)
      .forEach(usuario => {
        usuariosAnalisis.push([
          usuario.nombre,
          usuario.id,
          usuario.total,
          usuario.conFoto,
          usuario.conDescripcion,
          formatFecha(usuario.ultimoRegistro)
        ])
      })
    
    // === HOJA 4: ANÁLISIS TEMPORAL ===
    const analisisTemporal = [
      ['📅 ANÁLISIS TEMPORAL'],
      [''],
      ['Fecha', 'Registros del Día', 'Usuarios Activos', 'Con Foto', 'Con Descripción']
    ]
    
    const registrosPorFecha = new Map()
    
    registrosParaExportar.forEach(registro => {
      const fecha = new Date(registro.fecha_hora).toISOString().split('T')[0]
      if (!registrosPorFecha.has(fecha)) {
        registrosPorFecha.set(fecha, {
          total: 0,
          usuarios: new Set(),
          conFoto: 0,
          conDescripcion: 0
        })
      }
      
      const dia = registrosPorFecha.get(fecha)
      dia.total++
      dia.usuarios.add(registro.usuario_id)
      if (registro.foto_url) dia.conFoto++
      if (registro.descripcion && registro.descripcion.trim()) dia.conDescripcion++
    })
    
    Array.from(registrosPorFecha.entries())
      .sort(([a], [b]) => b.localeCompare(a))
      .forEach(([fecha, datos]) => {
        analisisTemporal.push([
          new Date(fecha).toLocaleDateString('es-ES'),
          datos.total,
          datos.usuarios.size,
          datos.conFoto,
          datos.conDescripcion
        ])
      })
    
    // Crear las hojas de trabajo
    const hojaResumen = XLSX.utils.aoa_to_sheet(resumenData)
    const hojaDatos = XLSX.utils.aoa_to_sheet(datosDetallados)
    const hojaUsuarios = XLSX.utils.aoa_to_sheet(usuariosAnalisis)
    const hojaTemporal = XLSX.utils.aoa_to_sheet(analisisTemporal)
    
    // === APLICAR ESTILOS Y FORMATO ===
    
    // Configurar anchos de columna para la hoja de resumen
    hojaResumen['!cols'] = [
      { width: 25 }, // Columna A
      { width: 20 }, // Columna B
      { width: 40 }  // Columna C
    ]
    
    // Configurar anchos de columna para la hoja de datos
    hojaDatos['!cols'] = [
      { width: 12 }, // ID
      { width: 25 }, // Usuario
      { width: 30 }, // Email
      { width: 15 }, // Tipo Actividad
      { width: 20 }, // Fecha
      { width: 12 }, // Latitud
      { width: 12 }, // Longitud
      { width: 35 }, // Descripción (reducido para dar espacio)
      { width: 15 }, // Estado Foto
      { width: 45 }  // URL Foto (reducido para dar espacio)
    ]
    
    // Configurar anchos de columna para la hoja de usuarios
    hojaUsuarios['!cols'] = [
      { width: 25 }, // Usuario
      { width: 12 }, // ID Usuario
      { width: 15 }, // Total
      { width: 12 }, // Con Foto
      { width: 18 }, // Con Descripción
      { width: 20 }  // Último Registro
    ]
    
    // Configurar anchos de columna para la hoja temporal
    hojaTemporal['!cols'] = [
      { width: 15 }, // Fecha
      { width: 18 }, // Registros
      { width: 18 }, // Usuarios Activos
      { width: 12 }, // Con Foto
      { width: 18 }  // Con Descripción
    ]
    
    // Agregar las hojas al libro
    XLSX.utils.book_append_sheet(workbook, hojaResumen, '📊 Resumen Ejecutivo')
    XLSX.utils.book_append_sheet(workbook, hojaDatos, '📋 Datos Detallados')
    XLSX.utils.book_append_sheet(workbook, hojaUsuarios, '👤 Análisis Usuarios')
    XLSX.utils.book_append_sheet(workbook, hojaTemporal, '📅 Análisis Temporal')
    
    // Generar nombre de archivo con timestamp
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19)
    const nombreArchivo = `Registros_PWA_SembrandoVida_${timestamp}.xlsx`
    
    // Descargar el archivo
    XLSX.writeFile(workbook, nombreArchivo)
    
    // Mostrar mensaje de éxito
    alert(`✅ Excel generado exitosamente!\n\n📊 ${estadisticas.totalRegistros} registros exportados\n👥 ${estadisticas.usuariosUnicos} usuarios únicos\n📷 ${estadisticas.conFotografia} con fotografía\n📝 ${estadisticas.conDescripcion} con descripción\n\n📁 Archivo: ${nombreArchivo}`)
    
  } catch (error) {
    console.error('Error al exportar a Excel:', error)
    alert('❌ Error al generar el archivo Excel. Por favor, inténtalo de nuevo.')
  }
}

const imprimirRegistros = () => {
  // Crear ventana de impresión
  const printWindow = window.open('', '_blank', 'width=800,height=600')
  
  // Obtener datos filtrados
  const registrosParaImprimir = registrosFiltrados.value
  
  // Generar HTML para impresión
  const htmlContent = `
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reporte de Registros - ${new Date().toLocaleDateString('es-ES')}</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background: white;
                font-size: 12px;
            }
            
            .print-header {
                text-align: center;
                margin-bottom: 30px;
                padding: 20px 0;
                border-bottom: 3px solid #4CAF50;
                page-break-inside: avoid;
            }
            
            .print-header h1 {
                color: #4CAF50;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .print-header .subtitle {
                color: #666;
                font-size: 14px;
                margin-bottom: 15px;
            }
            
            .print-header .date-range {
                color: #333;
                font-weight: 600;
                font-size: 13px;
                background: #f8f9fa;
                padding: 8px 16px;
                border-radius: 20px;
                display: inline-block;
                border: 1px solid #e9ecef;
            }
            
            .summary-stats {
                display: flex;
                justify-content: space-around;
                margin: 20px 0;
                padding: 15px;
                background: linear-gradient(135deg, #e8f5e8 0%, #f0fff4 100%);
                border-radius: 10px;
                border: 1px solid #4CAF50;
                page-break-inside: avoid;
            }
            
            .stat-item {
                text-align: center;
                flex: 1;
            }
            
            .stat-number {
                font-size: 24px;
                font-weight: bold;
                color: #4CAF50;
                display: block;
            }
            
            .stat-label {
                font-size: 11px;
                color: #666;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-top: 5px;
            }
            
            .registros-table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background: white;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                border-radius: 8px;
                overflow: hidden;
            }
            
            .registros-table th {
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                color: white;
                padding: 12px 8px;
                text-align: left;
                font-weight: 600;
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                border-bottom: 2px solid #388e3c;
            }
            
            .registros-table td {
                padding: 10px 8px;
                border-bottom: 1px solid #eee;
                font-size: 11px;
                vertical-align: top;
            }
            
            .registros-table tbody tr:nth-child(even) {
                background-color: #f8f9fa;
            }
            
            .registros-table tbody tr:hover {
                background-color: #e8f5e8;
            }
            
            .usuario-info {
                display: flex;
                flex-direction: column;
                gap: 2px;
            }
            
            .usuario-nombre {
                font-weight: 600;
                color: #333;
                font-size: 11px;
            }
            
            .usuario-email {
                color: #666;
                font-size: 10px;
                font-style: italic;
            }
            
            .registro-id {
                font-weight: bold;
                color: #4CAF50;
                background: #e8f5e8;
                padding: 2px 6px;
                border-radius: 4px;
                font-size: 10px;
            }
            
            .fecha-cell {
                white-space: nowrap;
                font-size: 10px;
                line-height: 1.3;
            }
            
            .ubicacion-cell {
                font-family: 'Courier New', monospace;
                font-size: 9px;
                color: #555;
                line-height: 1.2;
            }
            
            .descripcion-cell {
                max-width: 200px;
                word-wrap: break-word;
                font-size: 10px;
                line-height: 1.3;
            }
            
            .estado-foto {
                display: inline-block;
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 9px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.3px;
            }
            
            .con-foto {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            
            .sin-foto {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            
            .tipo-print {
                display: inline-block;
                padding: 2px 6px;
                border-radius: 8px;
                font-size: 9px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.3px;
            }
            
            .tipo-print.tipo-campo {
                background: #e8f5e8;
                color: #2e7d32;
                border: 1px solid #a5d6a7;
            }
            
            .tipo-print.tipo-gabinete {
                background: #fff3e0;
                color: #ef6c00;
                border: 1px solid #ff9800;
            }
            
            .print-footer {
                margin-top: 30px;
                padding: 20px 0;
                border-top: 2px solid #4CAF50;
                text-align: center;
                color: #666;
                font-size: 10px;
                page-break-inside: avoid;
            }
            
            .print-footer .generated-info {
                margin-bottom: 10px;
                font-weight: 600;
            }
            
            .print-footer .company-info {
                color: #999;
                font-style: italic;
            }
            
            /* Estilos específicos para impresión */
            @media print {
                body {
                    font-size: 10px;
                }
                
                .print-header h1 {
                    font-size: 24px;
                }
                
                .registros-table {
                    box-shadow: none;
                }
                
                .registros-table th {
                    background: #4CAF50 !important;
                    -webkit-print-color-adjust: exact;
                    color-adjust: exact;
                }
                
                .summary-stats {
                    background: #e8f5e8 !important;
                    -webkit-print-color-adjust: exact;
                    color-adjust: exact;
                }
                
                .registros-table tbody tr:nth-child(even) {
                    background-color: #f8f9fa !important;
                    -webkit-print-color-adjust: exact;
                    color-adjust: exact;
                }
                
                .con-foto {
                    background: #d4edda !important;
                    -webkit-print-color-adjust: exact;
                    color-adjust: exact;
                }
                
                .sin-foto {
                    background: #f8d7da !important;
                    -webkit-print-color-adjust: exact;
                    color-adjust: exact;
                }
                
                .tipo-print.tipo-campo {
                    background: #e8f5e8 !important;
                    -webkit-print-color-adjust: exact;
                    color-adjust: exact;
                }
                
                .tipo-print.tipo-gabinete {
                    background: #fff3e0 !important;
                    -webkit-print-color-adjust: exact;
                    color-adjust: exact;
                }
                
                .registro-id {
                    background: #e8f5e8 !important;
                    -webkit-print-color-adjust: exact;
                    color-adjust: exact;
                }
                
                /* Evitar quiebres de página en elementos importantes */
                .print-header,
                .summary-stats,
                .registros-table thead {
                    page-break-inside: avoid;
                }
                
                .registros-table tbody tr {
                    page-break-inside: avoid;
                }
            }
            
            @page {
                margin: 1.5cm;
                size: A4;
            }
        </style>
    </head>
    <body>
        <div class="print-header">
            <h1>📋 Reporte de Registros</h1>
            <div class="subtitle">Sistema de Gestión PWA - Sembrando Vida</div>
            <div class="date-range">
                📅 Generado el ${new Date().toLocaleDateString('es-ES', { 
                    weekday: 'long', 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                })}
            </div>
        </div>
        
        <div class="summary-stats">
            <div class="stat-item">
                <span class="stat-number">${registrosParaImprimir.length}</span>
                <span class="stat-label">Total Registros</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">${[...new Set(registrosParaImprimir.map(r => r.usuario_id))].length}</span>
                <span class="stat-label">Usuarios Únicos</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">${registrosParaImprimir.filter(r => r.foto_url).length}</span>
                <span class="stat-label">Con Fotografía</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">${registrosParaImprimir.filter(r => r.descripcion && r.descripcion.trim()).length}</span>
                <span class="stat-label">Con Descripción</span>
            </div>
        </div>
        
        <table class="registros-table">
            <thead>
                <tr>
                    <th style="width: 8%;">ID</th>
                    <th style="width: 18%;">Usuario</th>
                    <th style="width: 10%;">Tipo</th>
                    <th style="width: 13%;">Fecha y Hora</th>
                    <th style="width: 16%;">Ubicación</th>
                    <th style="width: 22%;">Descripción</th>
                    <th style="width: 13%;">Estado Foto</th>
                </tr>
            </thead>
            <tbody>
                ${registrosParaImprimir.map(registro => `
                    <tr>
                        <td>
                            <span class="registro-id">#${registro.id}</span>
                        </td>
                        <td>
                            <div class="usuario-info">
                                <span class="usuario-nombre">${registro.usuario?.nombre_completo || `Usuario ${registro.usuario_id}`}</span>
                                <span class="usuario-email">${registro.usuario?.correo || 'No disponible'}</span>
                            </div>
                        </td>
                        <td>
                            <span class="tipo-print ${getTipoClass(registro.tipo_actividad)}">
                                ${getTipoLabel(registro.tipo_actividad)}
                            </span>
                        </td>
                        <td class="fecha-cell">
                            ${formatFecha(registro.fecha_hora)}
                        </td>
                        <td class="ubicacion-cell">
                            Lat: ${parseFloat(registro.latitud).toFixed(6)}<br>
                            Lng: ${parseFloat(registro.longitud).toFixed(6)}
                        </td>
                        <td class="descripcion-cell">
                            ${registro.descripcion || '<em>Sin descripción</em>'}
                        </td>
                        <td>
                            <span class="estado-foto ${registro.foto_url ? 'con-foto' : 'sin-foto'}">
                                ${registro.foto_url ? '📷 Con Foto' : '❌ Sin Foto'}
                            </span>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
        
        <div class="print-footer">
            <div class="generated-info">
                🖨️ Documento generado automáticamente por el Sistema PWA Sembrando Vida
            </div>
            <div class="company-info">
                Este reporte contiene información confidencial - Página 1 de 1
            </div>
        </div>
    </body>
    </html>
  `
  
  // Escribir contenido en la ventana de impresión
  printWindow.document.write(htmlContent)
  printWindow.document.close()
  
  // Esperar a que se cargue el contenido y abrir diálogo de impresión
  printWindow.onload = () => {
    setTimeout(() => {
      printWindow.focus()
      printWindow.print()
      
      // Cerrar ventana después de imprimir (opcional)
      printWindow.onafterprint = () => {
        printWindow.close()
      }
    }, 500)
  }
}

const buscarUsuarios = () => {
  const texto = filtroUsuarioTexto.value.toLowerCase().trim()
  
  if (!texto) {
    usuariosFiltrados.value = usuariosDisponibles.value
    filtroUsuario.value = ''
    mostrarSugerencias.value = false
    filtrarRegistros()
    return
  }
  
  usuariosFiltrados.value = usuariosDisponibles.value.filter(usuario => {
    const nombre = (usuario.nombre_completo || '').toLowerCase()
    const usuarioId = `usuario ${usuario.id}`.toLowerCase()
    return nombre.includes(texto) || usuarioId.includes(texto)
  })
  
  mostrarSugerencias.value = true
  
  // Buscar coincidencia exacta para filtrar automáticamente
  const coincidenciaExacta = usuariosFiltrados.value.find(usuario => 
    (usuario.nombre_completo || '').toLowerCase() === texto
  )
  
  if (coincidenciaExacta) {
    filtroUsuario.value = coincidenciaExacta.id.toString()
    filtrarRegistros()
  } else {
    filtroUsuario.value = ''
    filtrarRegistros()
  }
}

const seleccionarUsuario = (usuario) => {
  filtroUsuarioTexto.value = usuario.nombre_completo || `Usuario ${usuario.id}`
  filtroUsuario.value = usuario.id.toString()
  mostrarSugerencias.value = false
  filtrarRegistros()
}

const ocultarSugerencias = () => {
  setTimeout(() => {
    mostrarSugerencias.value = false
  }, 200) // Delay para permitir clic en sugerencias
}

const limpiarFiltroUsuario = () => {
  filtroUsuarioTexto.value = ''
  filtroUsuario.value = ''
  usuariosFiltrados.value = usuariosDisponibles.value
  mostrarSugerencias.value = false
  filtrarRegistros()
}

const limpiarFiltros = () => {
  limpiarTodosFiltros()
}

// Funciones de ordenamiento
const ordenarPor = (campo) => {
  if (campoOrdenamiento.value === campo) {
    // Si es el mismo campo, cambiar dirección
    direccionOrdenamiento.value = direccionOrdenamiento.value === 'asc' ? 'desc' : 'asc'
  } else {
    // Si es un campo diferente, establecer nuevo campo y dirección por defecto
    campoOrdenamiento.value = campo
    direccionOrdenamiento.value = campo === 'fecha' ? 'desc' : 'asc' // Fecha descendente por defecto, otros ascendente
  }
  aplicarOrdenamiento()
}

const aplicarOrdenamiento = () => {
  if (!registrosFiltrados.value.length) return

  registrosFiltrados.value.sort((a, b) => {
    let valorA, valorB

    switch (campoOrdenamiento.value) {
      case 'id':
        valorA = parseInt(a.id)
        valorB = parseInt(b.id)
        break
      case 'usuario':
        valorA = (a.usuario?.nombre_completo || `Usuario ${a.usuario_id}`).toLowerCase()
        valorB = (b.usuario?.nombre_completo || `Usuario ${b.usuario_id}`).toLowerCase()
        break
      case 'tipo':
        valorA = getTipoLabel(a.tipo_actividad).toLowerCase()
        valorB = getTipoLabel(b.tipo_actividad).toLowerCase()
        break
      case 'fecha':
        valorA = new Date(a.fecha_hora)
        valorB = new Date(b.fecha_hora)
        break
      default:
        return 0
    }

    if (direccionOrdenamiento.value === 'asc') {
      if (valorA < valorB) return -1
      if (valorA > valorB) return 1
      return 0
    } else {
      if (valorA > valorB) return -1
      if (valorA < valorB) return 1
      return 0
    }
  })
}

const formatFecha = (fechaStr) => {
  try {
    return new Date(fechaStr).toLocaleString('es-ES')
  } catch (e) {
    return fechaStr
  }
}

const formatFechaCompacta = (fechaStr) => {
  try {
    const fecha = new Date(fechaStr)
    const hora = fecha.toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    })
    const fechaCorta = fecha.toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: '2-digit'
    })
    return { hora, fecha: fechaCorta }
  } catch (e) {
    return { hora: '--:--', fecha: '--/--/--' }
  }
}

const getTipoLabel = (tipo) => {
  if (!tipo) return 'Campo' // Valor por defecto para registros antiguos
  
  switch (tipo.toLowerCase()) {
    case 'campo':
      return 'Campo'
    case 'gabinete':
      return 'Gabinete'
    default:
      return 'Campo'
  }
}

const getTipoClass = (tipo) => {
  if (!tipo) return 'tipo-campo' // Valor por defecto para registros antiguos
  
  switch (tipo.toLowerCase()) {
    case 'campo':
      return 'tipo-campo'
    case 'gabinete':
      return 'tipo-gabinete'
    default:
      return 'tipo-campo'
  }
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

const verDetalles = async (registro) => {
  selectedRegistro.value = registro
  modalTitle.value = 'Detalles del Registro'
  modalType.value = 'details'
  showModal.value = true
  
  // Esperar a que el modal se renderice
  await nextTick()
  
  // Inicializar el mapa
  setTimeout(() => {
    initMap(registro.latitud, registro.longitud)
  }, 100)
}

const initMap = (lat, lng) => {
  if (map) {
    map.remove()
  }
  
  const mapElement = document.getElementById('map')
  if (!mapElement) return
  
  // Verificar que Leaflet esté cargado
  if (!window.L) {
    console.error('Leaflet no está cargado')
    return
  }
  
  try {
    map = window.L.map('map').setView([parseFloat(lat), parseFloat(lng)], 15)
    
    window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map)
    
    window.L.marker([parseFloat(lat), parseFloat(lng)])
      .addTo(map)
      .bindPopup(`Registro #${selectedRegistro.value?.id}<br>Lat: ${lat}<br>Lng: ${lng}`)
      .openPopup()
  } catch (error) {
    console.error('Error al inicializar el mapa:', error)
  }
}

const abrirFotoCompleta = (fotoUrl) => {
  lightboxImageUrl.value = `${API_URL}/${fotoUrl}`
  showLightbox.value = true
}

const cerrarLightbox = () => {
  showLightbox.value = false
  lightboxImageUrl.value = ''
}

// ==================== MÉTODOS DE NOTIFICACIÓN ====================

const abrirModalNotificar = (registro) => {
  console.log('🔔 Abriendo modal para notificar sobre actividad:', registro)
  
  actividadANotificar.value = registro
  
  // Pre-llenar el formulario
  const tipoActividad = registro.tipo_actividad || 'Actividad'
  const categoriaActividad = registro.categoria_actividad || ''
  const fecha = registro.fecha_hora ? new Date(registro.fecha_hora).toLocaleDateString('es-MX') : ''
  const nombreUsuario = registro.usuario?.nombre_completo || 'Usuario'
  
  formNotificacion.value = {
    titulo: '', // Vacío - obligatorio que el admin escriba el título
    subtitulo: '', // Se actualizará automáticamente cuando se seleccionen motivos
    descripcion: '', // Vacío - obligatorio que el admin escriba el mensaje
    motivos_atencion: [],
    enlace_url: '',
    actividad_id: registro.id,
    usuario_ids: [registro.usuario_id] // El usuario de la actividad
  }
  
  showNotificarModal.value = true
}

const cerrarModalNotificar = () => {
  showNotificarModal.value = false
  actividadANotificar.value = null
  formNotificacion.value = {
    titulo: '',
    subtitulo: '',
    descripcion: '',
    motivos_atencion: [],
    enlace_url: '',
    actividad_id: null,
    usuario_ids: []
  }
}

const enviarNotificacion = async () => {
  // Actualizar subtítulo con los motivos seleccionados
  const motivosSeleccionados = motivosAtencionOpciones
    .filter(m => formNotificacion.value.motivos_atencion.includes(m.value))
    .map(m => m.label)
    .join(', ')
  
  formNotificacion.value.subtitulo = motivosSeleccionados
  
  if (!formNotificacion.value.titulo.trim()) {
    mostrarToast('El título es obligatorio', 'error')
    return
  }
  
  if (formNotificacion.value.motivos_atencion.length === 0) {
    mostrarToast('Selecciona al menos un motivo de atención', 'error')
    return
  }
  
  if (!formNotificacion.value.descripcion.trim()) {
    mostrarToast('La descripción es obligatoria', 'error')
    return
  }
  
  enviandoNotificacion.value = true
  
  try {
    const notificacion = {
      ...formNotificacion.value,
      enviada_a_todos: false // Siempre individual
    }
    
    const respuesta = await notificacionesService.crearNotificacion(notificacion, null)
    
    console.log('✅ Notificación enviada:', respuesta)
    mostrarToast('Notificación enviada exitosamente', 'success')
    
    cerrarModalNotificar()
    
  } catch (error) {
    console.error('❌ Error enviando notificación:', error)
    mostrarToast(error.message || 'Error al enviar la notificación', 'error')
  } finally {
    enviandoNotificacion.value = false
  }
}

// ==================== FIN MÉTODOS DE NOTIFICACIÓN ====================

const requestFullscreen = (event) => {
  if (event.target.requestFullscreen) {
    event.target.requestFullscreen()
  }
}

// Funciones para edición de registros
const abrirModalEditar = (registro) => {
  registroEditando.value = registro
  
  // Parsear fecha y hora del registro
  let fecha = ''
  let hora = ''
  if (registro.fecha_hora) {
    try {
      const fechaObj = new Date(registro.fecha_hora)
      fecha = fechaObj.toISOString().split('T')[0]
      hora = fechaObj.toTimeString().slice(0, 5)
    } catch (e) {
      console.error('Error parseando fecha:', e)
    }
  }
  
  editForm.value = {
    tipo_actividad: registro.tipo_actividad || '',
    descripcion: registro.descripcion || '',
    categoria_actividad: registro.categoria_actividad || '',
    categoria_actividad_otro: registro.categoria_actividad_otro || '',
    fecha: fecha,
    hora: hora
  }
  showEditModal.value = true
}

const cerrarModalEditar = () => {
  showEditModal.value = false
  registroEditando.value = null
  editForm.value = {
    tipo_actividad: '',
    descripcion: '',
    categoria_actividad: '',
    categoria_actividad_otro: '',
    fecha: '',
    hora: ''
  }
  isEditSaving.value = false
}

const guardarEdicion = async () => {
  if (!registroEditando.value || !editForm.value.tipo_actividad) {
    mostrarToast('Por favor selecciona un tipo de actividad', 'error')
    return
  }

  if (!editForm.value.categoria_actividad) {
    mostrarToast('Por favor selecciona una categoría de actividad', 'error')
    return
  }

  if (editForm.value.categoria_actividad === 'Otro' && !editForm.value.categoria_actividad_otro?.trim()) {
    mostrarToast('Por favor especifica la categoría', 'error')
    return
  }

  isEditSaving.value = true
  
  try {
    const token = localStorage.getItem('admin_token')
    
    // Construir fecha_hora combinando fecha y hora
    let fechaHoraStr = null
    if (editForm.value.fecha && editForm.value.hora) {
      fechaHoraStr = `${editForm.value.fecha}T${editForm.value.hora}:00`
    }
    
    const response = await axios.put(
      `${API_URL}/api/registros/${registroEditando.value.id}`,
      {
        tipo_actividad: editForm.value.tipo_actividad,
        descripcion: editForm.value.descripcion?.trim() || '',
        categoria_actividad: editForm.value.categoria_actividad,
        categoria_actividad_otro: editForm.value.categoria_actividad === 'Otro' ? editForm.value.categoria_actividad_otro?.trim() : '',
        fecha_hora: fechaHoraStr
      },
      {
        headers: { 'Authorization': `Bearer ${token}` },
        timeout: 15000
      }
    )

    if (response.data) {
      // Actualizar el registro en la lista local
      const indexRegistros = registros.value.findIndex(r => r.id === registroEditando.value.id)
      const indexFiltrados = registrosFiltrados.value.findIndex(r => r.id === registroEditando.value.id)
      
      const registroActualizado = {
        ...registroEditando.value,
        tipo_actividad: editForm.value.tipo_actividad,
        descripcion: editForm.value.descripcion?.trim() || '',
        categoria_actividad: editForm.value.categoria_actividad,
        categoria_actividad_otro: editForm.value.categoria_actividad === 'Otro' ? editForm.value.categoria_actividad_otro?.trim() : '',
        fecha_hora: fechaHoraStr || registroEditando.value.fecha_hora
      }
      
      if (indexRegistros !== -1) {
        registros.value[indexRegistros] = registroActualizado
      }
      if (indexFiltrados !== -1) {
        registrosFiltrados.value[indexFiltrados] = registroActualizado
      }
      
      mostrarToast('Registro actualizado correctamente', 'success')
      cerrarModalEditar()
    }
  } catch (error) {
    console.error('Error al actualizar registro:', error)
    const mensaje = error.response?.data?.detail || 'Error al actualizar el registro'
    mostrarToast(mensaje, 'error')
  } finally {
    isEditSaving.value = false
  }
}

const cerrarModal = () => {
  showModal.value = false
  if (map) {
    map.remove()
    map = null
  }
}

const confirmarEliminarRegistro = (registro) => {
  registroAEliminar.value = registro
  showConfirmDelete.value = true
}

const cancelarEliminar = () => {
  showConfirmDelete.value = false
  registroAEliminar.value = null
}

const mostrarToast = (mensaje, tipo = 'success') => {
  toastMessage.value = mensaje
  toastType.value = tipo
  showToast.value = true
  
  setTimeout(() => {
    showToast.value = false
  }, 3500)
}

const eliminarRegistro = async () => {
  if (!registroAEliminar.value) return
  
  try {
    const token = localStorage.getItem('admin_token')
    if (!token) {
      mostrarToast('No hay sesión activa', 'error')
      router.push('/login')
      return
    }
    
    const response = await fetch(`${API_URL}/admin/registros/${registroAEliminar.value.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (!response.ok) {
      throw new Error('Error al eliminar el registro')
    }
    
    const data = await response.json()
    console.log('Registro eliminado:', data)
    
    // Cerrar modal de confirmación
    showConfirmDelete.value = false
    
    // Mostrar mensaje de éxito
    mostrarToast(`Registro #${registroAEliminar.value.id} eliminado exitosamente`, 'success')
    
    registroAEliminar.value = null
    
    // Recargar registros
    await cargarRegistros()
    
  } catch (error) {
    console.error('Error al eliminar registro:', error)
    mostrarToast('Error al eliminar el registro. Por favor, intenta de nuevo.', 'error')
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
.registros-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
  overflow: hidden;
  background: linear-gradient(180deg, #f0fdf4 0%, #ecfdf5 50%, #f0fdf4 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  position: relative;
}

/* Apple Dynamic Background */
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
  background: linear-gradient(135deg, #388E3C 0%, #2E7D32 50%, #1B5E20 100%);
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
  color: white;
}

.apple-refresh-button svg {
  width: 14px;
  height: 14px;
  stroke-width: 2;
}

.apple-refresh-button:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.25);
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
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
  color: white;
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
  letter-spacing: -0.3px;
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
  min-width: 280px;
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
  color: #007AFF;
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
  color: white;
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

.apple-search-loading {
  position: absolute;
  right: 14px;
}

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
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
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
}

.apple-filter-btn.active {
  background: linear-gradient(135deg, #8BC34A, #7CB342);
  color: white;
  border-color: #8BC34A;
}

.apple-filter-btn.reset {
  color: #FF3B30;
  border-color: rgba(255, 59, 48, 0.2);
}

.apple-filter-btn.reset svg {
  stroke: #FF3B30;
}

.apple-filter-btn.reset:hover {
  background: rgba(255, 59, 48, 0.08);
  border-color: #FF3B30;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(255, 59, 48, 0.2);
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
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(52, 199, 89, 0.2);
}

/* ====================== APPLE QUICK FILTERS ====================== */
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
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
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
  box-shadow: 0 4px 10px rgba(0, 122, 255, 0.15);
}

.apple-filter-chip.active {
  background: linear-gradient(135deg, #007AFF 0%, #0051D5 100%);
  color: white;
  border-color: #007AFF;
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

/* ====================== APPLE ADVANCED FILTERS ====================== */
.apple-advanced-filters {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.advanced-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
  margin-bottom: 10px;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-item label {
  font-size: 11px;
  font-weight: 600;
  color: #86868b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.filter-item select,
.filter-item input[type="date"] {
  height: 42px;
  border-radius: 12px;
  border: 1.5px solid #e5e5e5;
  background: #f5f5f7;
  padding: 0 14px;
  font-size: 13px;
  color: #1d1d1f;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.filter-item select:focus,
.filter-item input[type="date"]:focus {
  outline: none;
  background: white;
  border-color: #8BC34A;
  box-shadow: 0 0 0 4px rgba(139, 195, 74, 0.1);
}

.filter-checkboxes {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 13px;
  color: #1d1d1f;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
  transition: color 0.2s ease;
}

.checkbox-label:hover {
  color: #8BC34A;
}

.checkbox-label input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: #8BC34A;
}

/* ====================== APPLE CONTENT WRAPPER ====================== */
.apple-content-wrapper {
  padding: 0;
  overflow-x: hidden;
}

/* ====================== APPLE TABLE CONTAINER ====================== */
.apple-table-container {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
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
  height: 8px;
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

/* ====================== APPLE TABLE ====================== */
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
  padding: 14px 16px;
  text-align: left;
  font-size: 11px;
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
  padding: 14px 16px;
  font-size: 13px;
  color: #1D1D1F;
  border-left: 2px solid transparent;
  transition: all 0.15s ease;
  vertical-align: middle;
}

.apple-table-row:hover td:first-child {
  border-left-color: #8BC34A;
}

/* ====================== APPLE TABLE CELLS ====================== */
.apple-id-badge {
  display: inline-block;
  padding: 4px 10px;
  background: rgba(0, 122, 255, 0.1);
  color: #007AFF;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  font-family: monospace;
}

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
  min-width: 0;
}

.apple-user-name {
  font-size: 13px;
  font-weight: 600;
  color: #1D1D1F;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.apple-user-role {
  font-size: 11px;
  color: #86868b;
  font-style: italic;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.apple-photo-thumb {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  object-fit: cover;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid rgba(139, 195, 74, 0.2);
}

.apple-photo-thumb:hover {
  transform: scale(1.1);
  border-color: #8BC34A;
  box-shadow: 0 4px 12px rgba(139, 195, 74, 0.3);
}

.apple-tipo-badge {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
}

.apple-tipo-badge.siembra {
  background: rgba(52, 199, 89, 0.1);
  color: #34C759;
}

.apple-tipo-badge.riego {
  background: rgba(0, 122, 255, 0.1);
  color: #007AFF;
}

.apple-tipo-badge.cosecha {
  background: rgba(255, 149, 0, 0.1);
  color: #FF9500;
}

.apple-tipo-badge.otro {
  background: rgba(175, 82, 222, 0.1);
  color: #AF52DE;
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
}

.apple-descripcion {
  font-size: 12px;
  color: #86868b;
  max-width: 150px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.apple-fecha-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.apple-time-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  background: rgba(52, 199, 89, 0.1);
  color: #34C759;
}

.apple-date-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 500;
  background: rgba(0, 122, 255, 0.1);
  color: #007AFF;
}

.apple-no-data {
  color: #86868b;
  font-size: 14px;
}

/* ====================== APPLE ACTIONS ====================== */
.apple-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.apple-action-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.apple-action-btn svg {
  width: 16px;
  height: 16px;
  stroke: white;
  stroke-width: 2;
  fill: none;
}

.apple-action-btn.view {
  background: linear-gradient(135deg, #8BC34A 0%, #7CB342 100%);
}

.apple-action-btn.view:hover {
  background: linear-gradient(135deg, #7CB342 0%, #689F38 100%);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(139, 195, 74, 0.4);
}

.apple-action-btn.notify {
  background: linear-gradient(135deg, #E65100 0%, #D84315 100%);
}

.apple-action-btn.notify:hover {
  background: linear-gradient(135deg, #D84315 0%, #BF360C 100%);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(230, 81, 0, 0.4);
}

.apple-action-btn.edit {
  background: linear-gradient(135deg, #6366f1 0%, #5558e3 100%);
}

.apple-action-btn.edit:hover {
  background: linear-gradient(135deg, #5558e3 0%, #4f46e5 100%);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

.apple-action-btn.delete {
  background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
}

.apple-action-btn.delete:hover {
  background: linear-gradient(135deg, #d32f2f 0%, #c62828 100%);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.4);
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
  color: #1D1D1F;
  cursor: pointer;
  transition: all 0.2s;
}

.apple-pagination-number:hover {
  background: rgba(139, 195, 74, 0.15);
}

.apple-pagination-number.active {
  background: linear-gradient(135deg, #8BC34A 0%, #66BB6A 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(139, 195, 74, 0.4);
}

/* ====================== APPLE LOAD MORE BUTTON ====================== */
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

/* ====================== APPLE STATES ====================== */
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
  border: 4px solid #E8F5E9;
  border-top-color: #8BC34A;
  border-radius: 50%;
  animation: apple-spin 0.8s linear infinite;
  margin-bottom: 24px;
}

.apple-loading p,
.apple-error p,
.apple-empty p {
  font-size: 14px;
  color: #86868b;
  margin-top: 12px;
}

.apple-error svg,
.apple-empty svg {
  width: 64px;
  height: 64px;
  stroke: #8BC34A;
  stroke-width: 1.5;
  margin-bottom: 16px;
}

.apple-empty h3,
.apple-error h3 {
  font-size: 20px;
  font-weight: 600;
  color: #1D1D1F;
  margin: 0 0 8px 0;
}

.apple-retry-btn {
  margin-top: 16px;
  padding: 10px 24px;
  background: linear-gradient(135deg, #8BC34A 0%, #7CB342 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(139, 195, 74, 0.3);
}

.apple-retry-btn:hover {
  background: linear-gradient(135deg, #7CB342 0%, #689F38 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(139, 195, 74, 0.4);
}

.page-header {
  display: none; /* Ocultar header antiguo */
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

.header-actions {
  display: flex;
  align-items: center;
  gap: clamp(0.5rem, 1.2vw, 0.75rem);
  flex-shrink: 0;
}

.refresh-btn {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.1) 100%);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: clamp(6px, 1vw, 8px) clamp(12px, 2vw, 14px);
  border-radius: clamp(12px, 2vw, 14px);
  font-weight: 600;
  font-size: clamp(10px, 1.8vw, 11px);
  display: flex;
  align-items: center;
  gap: clamp(4px, 0.8vw, 6px);
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 
    inset 0 -1px 0 rgba(0, 0, 0, 0.1);
  font-family: 'Inter', sans-serif;
  white-space: nowrap;
  position: relative;
  overflow: hidden;
}

.refresh-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.05) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: inherit;
}

.refresh-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    inset 0 -1px 0 rgba(0, 0, 0, 0.15);
  border-color: rgba(255, 255, 255, 0.4);
}

.refresh-btn:hover:not(:disabled)::before {
  opacity: 1;
}

.refresh-btn svg {
  width: clamp(12px, 2vw, 14px);
  height: clamp(12px, 2vw, 14px);
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
  z-index: 1;
  position: relative;
  transition: all 0.3s ease;
}

.refresh-btn:hover:not(:disabled) svg {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
  transform: scale(1.05);
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Responsive 1024px - Tablets */
@media (max-width: 1024px) {
  .apple-content-wrapper {
    padding: 24px 24px;
  }
}

/* Responsive improvements for smaller screens */
@media (max-width: 768px) {
  .page-header {
    padding: clamp(0.3rem, 1vw, 0.5rem);
  }
  
  .header-content {
    gap: 0.5rem;
  }
  
  .header-main {
    gap: 0.5rem;
    min-width: 150px;
  }
  
  .header-icon {
    width: 26px;
    height: 26px;
  }
  
  .header-icon svg {
    width: 14px;
    height: 14px;
  }
  
  .header-title {
    font-size: 0.95rem;
    line-height: 1.05;
  }
  
  .header-subtitle {
    font-size: 0.62rem;
    margin-top: 0.05rem;
  }
  
  .header-actions {
    gap: 0.4rem;
  }
  
  .connection-status {
    padding: 0.15rem 0.4rem;
    font-size: 0.58rem;
    gap: 0.15rem;
  }
  
  .status-indicator {
    width: 3px;
    height: 3px;
  }
  
  .refresh-btn {
    padding: 0.25rem 0.5rem;
    font-size: 0.58rem;
    gap: 0.15rem;
  }
  
  /* Espaciado mínimo en tablets */
  .page-content {
    padding: 6px 16px;
  }
  
  /* Filtros más compactos en tablets - DEPRECATED (usando Apple design) */
  .advanced-filters {
    display: none; /* Ocultar diseño antiguo */
  }
  
  /* Apple Design Responsive */
  .apple-sticky-wrapper {
    margin-bottom: 16px;
  }
  
  .apple-page-header {
    padding: 10px 16px;
    border-radius: 24px 24px 0 0;
  }
  
  .apple-header-left {
    gap: 10px;
  }
  
  .apple-icon-circle {
    width: 28px;
    height: 28px;
  }
  
  .apple-icon-circle svg {
    width: 14px;
    height: 14px;
  }
  
  .apple-page-title {
    font-size: 16px;
  }
  
  .apple-page-subtitle {
    font-size: 10px;
  }
  
  .apple-refresh-button {
    width: 28px;
    height: 28px;
  }
  
  .apple-refresh-button svg {
    width: 14px;
    height: 14px;
  }
  
  .apple-stats-section {
    padding: 20px 16px 16px 16px;
    border-radius: 0 0 24px 24px;
  }
  
  .apple-stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 10px;
    margin-bottom: 14px;
  }
  
  .apple-stat-card {
    padding: 14px;
    gap: 10px;
    border-radius: 14px;
  }
  
  .apple-stat-icon {
    width: 38px;
    height: 38px;
  }
  
  .apple-stat-icon svg {
    width: 17px;
    height: 17px;
  }
  
  .apple-stat-value {
    font-size: 20px;
  }
  
  .apple-stat-label {
    font-size: 10px;
  }
  
  .apple-search-row {
    gap: 10px;
    margin-bottom: 10px;
  }
  
  .apple-search-input {
    height: 40px;
    font-size: 12px;
  }
  
  .apple-filter-btn {
    padding: 8px 14px;
    font-size: 12px;
  }
  
  .apple-filter-chip {
    padding: 7px 12px;
    font-size: 11px;
  }
  
  .advanced-grid {
    gap: 10px;
  }
  
  /* Apple Table Responsive */
  .apple-content-wrapper {
    padding: 16px;
  }
  
  .apple-table-container {
    max-height: calc(100vh - 380px);
    border-radius: 16px;
  }
  
  .apple-table th,
  .apple-table td {
    padding: 12px 10px;
    font-size: 12px;
  }
  
  .apple-avatar {
    width: 36px;
    height: 36px;
  }
  
  .apple-avatar svg {
    width: 18px;
    height: 18px;
  }
  
  .apple-user-name {
    font-size: 12px;
  }
  
  .apple-user-role {
    font-size: 10px;
  }
  
  .apple-action-btn {
    width: 28px;
    height: 28px;
  }
  
  .apple-action-btn svg {
    width: 14px;
    height: 14px;
  }
  
  .apple-pagination {
    padding: 8px 12px;
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .apple-pagination-btn,
  .apple-pagination-number {
    width: 28px;
    height: 28px;
    font-size: 12px;
  }
  
  .apple-load-more-btn {
    padding: 6px 12px;
    font-size: 11px;
  }

  .main-content {
    padding: 6px 12px 0 12px;
  }
  
  .filters-main {
    gap: 0.25rem;
    margin-bottom: 0.25rem;
  }
  
  .search-input {
    padding: 0.25rem 0.4rem 0.25rem 1.8rem;
    font-size: 0.6rem;
  }
  
  .date-input {
    padding: 0.2rem 0.35rem;
    font-size: 0.58rem;
    min-width: 90px;
  }
  
  .quick-date-btn {
    padding: 0.15rem 0.3rem;
    font-size: 0.58rem;
  }
  
  .toggle-filters-btn {
    padding: 0.25rem 0.4rem;
    font-size: 0.6rem;
    margin-top: 0.25rem;
  }
  
  /* Estilos responsive para fecha-hora */
  .fecha-hora-container {
    gap: 1px;
  }
  
  .hora-display {
    font-size: 10px;
    padding: 1px 4px;
  }
  
  .fecha-display {
    font-size: 8px;
  }
}

@media (max-width: 480px) {
  .page-header {
    display: none;
  }
  
  .advanced-filters {
    display: none;
  }
  
  /* Apple Design Mobile */
  .apple-sticky-wrapper {
    margin-bottom: 12px;
  }
  
  .apple-page-header {
    padding: 8px 12px;
    border-radius: 20px 20px 0 0;
  }
  
  .apple-header-left {
    gap: 8px;
  }
  
  .apple-icon-circle {
    width: 24px;
    height: 24px;
  }
  
  .apple-icon-circle svg {
    width: 12px;
    height: 12px;
  }
  
  .apple-page-title {
    font-size: 14px;
  }
  
  .apple-page-subtitle {
    font-size: 9px;
  }
  
  .apple-refresh-button {
    width: 24px;
    height: 24px;
  }
  
  .apple-refresh-button svg {
    width: 12px;
    height: 12px;
  }
  
  .apple-stats-section {
    padding: 16px 12px 12px 12px;
    border-radius: 0 0 20px 20px;
  }
  
  .apple-stats-grid {
    grid-template-columns: 1fr;
    gap: 8px;
    margin-bottom: 12px;
  }
  
  .apple-stat-card {
    padding: 12px;
    gap: 10px;
    border-radius: 12px;
  }
  
  .apple-stat-icon {
    width: 32px;
    height: 32px;
  }
  
  .apple-stat-icon svg {
    width: 15px;
    height: 15px;
  }
  
  .apple-stat-value {
    font-size: 18px;
  }
  
  .apple-stat-label {
    font-size: 9px;
  }
  
  .apple-search-section {
    padding-top: 12px;
  }
  
  .apple-search-row {
    flex-direction: column;
    gap: 8px;
    margin-bottom: 8px;
  }
  
  .apple-search-container {
    min-width: 100%;
  }
  
  .apple-search-input {
    height: 38px;
    font-size: 12px;
    padding: 0 38px 0 38px;
  }
  
  .apple-search-icon {
    width: 16px;
    height: 16px;
    left: 12px;
  }
  
  .apple-clear-btn {
    width: 28px;
    height: 28px;
  }
  
  .apple-clear-btn svg {
    width: 14px;
    height: 14px;
  }
  
  .apple-filter-controls {
    width: 100%;
    justify-content: space-between;
  }
  
  .apple-filter-btn {
    flex: 1;
    justify-content: center;
    padding: 8px;
    font-size: 0;
  }
  
  .apple-filter-btn svg {
    width: 18px;
    height: 18px;
  }
  
  .apple-filter-btn span {
    display: none;
  }
  
  .apple-quick-filters {
    gap: 6px;
  }
  
  .apple-filter-chip {
    padding: 6px 10px;
    font-size: 10px;
    gap: 4px;
  }
  
  .apple-filter-chip svg {
    width: 12px;
    height: 12px;
  }
  
  .advanced-grid {
    grid-template-columns: 1fr;
    gap: 8px;
  }
  
  .filter-item select,
  .filter-item input[type="date"] {
    height: 38px;
    font-size: 12px;
  }
  
  /* Apple Table Mobile */
  .apple-content-wrapper {
    padding: 12px;
  }
  
  .apple-table-container {
    max-height: calc(100vh - 420px);
    border-radius: 12px;
  }
  
  .apple-table th,
  .apple-table td {
    padding: 10px 8px;
    font-size: 11px;
  }
  
  .apple-table th {
    font-size: 9px;
    letter-spacing: 0.5px;
  }
  
  .apple-avatar {
    width: 32px;
    height: 32px;
  }
  
  .apple-avatar svg {
    width: 16px;
    height: 16px;
  }
  
  .apple-user-cell {
    gap: 8px;
  }
  
  .apple-user-name {
    font-size: 11px;
  }
  
  .apple-user-role {
    font-size: 9px;
  }
  
  .apple-id-badge {
    padding: 3px 6px;
    font-size: 10px;
  }
  
  .apple-photo-thumb {
    width: 28px;
    height: 28px;
    border-radius: 6px;
  }
  
  .apple-tipo-badge {
    padding: 3px 6px;
    font-size: 9px;
  }
  
  .apple-location-btn {
    width: 28px;
    height: 28px;
    min-width: 28px;
  }
  
  .apple-location-btn svg {
    width: 14px;
    height: 14px;
  }
  
  .apple-descripcion {
    font-size: 10px;
    max-width: 100px;
  }
  
  .apple-fecha-cell {
    gap: 2px;
  }
  
  .apple-time-badge,
  .apple-date-badge {
    padding: 2px 6px;
    font-size: 9px;
  }
  
  .apple-actions {
    gap: 4px;
  }
  
  .apple-action-btn {
    width: 26px;
    height: 26px;
  }
  
  .apple-action-btn svg {
    width: 12px;
    height: 12px;
  }
  
  .apple-pagination {
    padding: 8px;
    flex-direction: column;
    gap: 8px;
  }
  
  .apple-pagination-controls {
    gap: 4px;
  }
  
  .apple-pagination-btn,
  .apple-pagination-number {
    width: 26px;
    height: 26px;
    font-size: 11px;
  }
  
  .apple-pagination-btn svg {
    width: 14px;
    height: 14px;
  }
  
  .apple-load-more-btn {
    width: 100%;
    justify-content: center;
    padding: 8px 12px;
    font-size: 11px;
  }
  
  .apple-loading,
  .apple-error,
  .apple-empty {
    padding: 40px 20px;
  }
  
  .apple-spinner {
    width: 36px;
    height: 36px;
  }
  
  .apple-error svg,
  .apple-empty svg {
    width: 48px;
    height: 48px;
  }
  
  .apple-empty h3,
  .apple-error h3 {
    font-size: 16px;
  }
  
  .apple-loading p,
  .apple-error p,
  .apple-empty p {
    font-size: 12px;
  }

  .main-content {
    padding: 4px 8px 0 8px;
  }
  
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.4rem;
  }
  
  .header-main {
    width: 100%;
    justify-content: flex-start;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .header-title {
    font-size: 0.85rem;
  }
  
  .header-subtitle {
    font-size: 0.6rem;
  }
  
  /* Espaciado ultra mínimo en móviles */
  .page-content {
    padding: 4px 12px;
  }
  
  /* Filtros ultra compactos en móviles */
  .advanced-filters {
    padding: 0.25rem 0.3rem;
    margin-bottom: 0.25rem;
    border-radius: 4px;
  }
  
  .filters-main {
    gap: 0.2rem;
    margin-bottom: 0.2rem;
  }
  
  .search-box {
    min-width: 150px;
  }
  
  .search-input {
    padding: 0.2rem 0.3rem 0.2rem 1.6rem;
    font-size: 0.58rem;
    border-radius: 3px;
  }
  
  .search-icon {
    width: 10px;
    height: 10px;
    left: 0.4rem;
  }
  
  .date-range-filter {
    gap: 0.3rem;
  }
  
  .date-picker-container {
    gap: 0.2rem;
  }
  
  .date-label {
    font-size: 0.55rem;
  }
  
  .date-input {
    padding: 0.15rem 0.25rem;
    font-size: 0.55rem;
    min-width: 80px;
    border-radius: 3px;
  }
  
  .quick-date-filters {
    gap: 0.15rem;
  }
  
  .quick-date-btn {
    padding: 0.12rem 0.25rem;
    font-size: 0.55rem;
    border-radius: 2px;
  }
  
  .toggle-filters-btn {
    padding: 0.2rem 0.3rem;
    font-size: 0.58rem;
    margin-top: 0.15rem;
    border-radius: 3px;
  }
  
  .advanced-filters-grid {
    grid-template-columns: 1fr;
    gap: 0.3rem;
  }
  
  .filter-label {
    font-size: 0.55rem;
  }
  
  .filter-select {
    padding: 0.2rem 0.3rem;
    font-size: 0.55rem;
    border-radius: 3px;
  }
  
  .checkbox-option {
    font-size: 0.55rem;
    gap: 0.1rem;
  }
  
  .checkbox-option input[type="checkbox"] {
    width: 8px;
    height: 8px;
  }
  
  .sort-btn {
    padding: 0.15rem 0.3rem;
    font-size: 0.55rem;
    border-radius: 2px;
  }
  
  .export-btn {
    padding: 0.2rem 0.3rem;
    font-size: 0.55rem;
    border-radius: 2px;
  }
  
  .advanced-actions {
    gap: 0.25rem;
  }
  
  /* Tabla ultra compacta para tablets */
  .registros-table {
    min-width: 450px;
  }
  
  .registros-table th {
    padding: 4px 6px;
    font-size: 7px;
    letter-spacing: 0.2px;
  }
  
  .registros-table td {
    padding: 4px 6px;
    font-size: 9px;
  }
  
  .foto-mini {
    width: 20px;
    height: 20px;
    border-radius: 3px;
    border-width: 1px;
  }
  
  .btn-ver {
    width: 20px;
    height: 20px;
  }
  
  .usuario-info strong {
    font-size: 9px;
  }
  
  .usuario-info small {
    font-size: 7px;
  }
  
  .ubicacion,
  .fecha,
  .no-foto {
    font-size: 7px;
  }
  
  .descripcion {
    max-width: 100px;
  }
  
  /* Estilos para fecha-hora en móvil */
  .fecha-hora-container {
    gap: 0px;
  }
  
  .hora-display {
    font-size: 9px;
    padding: 1px 3px;
  }
  
  .fecha-display {
    font-size: 7px;
  }
}

/* Estilos para información de carga optimizada */
.load-info {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.08) 0%, rgba(76, 175, 80, 0.04) 100%);
  border: 1px solid rgba(76, 175, 80, 0.2);
  border-radius: 12px;
  padding: 1rem 1.5rem;
  margin-bottom: 1rem;
  animation: fadeInDown 0.4s ease-out;
}

.load-status {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  justify-content: space-between;
}

.load-icon {
  font-size: 1.2rem;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.load-text {
  color: #4b5563;
  font-weight: 500;
  font-size: 0.9rem;
  flex: 1;
}

.load-more-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
}

.load-more-btn:hover {
  background: linear-gradient(135deg, #43A047 0%, #5CB85C 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
}

.loading-more {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #4CAF50;
  font-weight: 500;
  font-size: 0.85rem;
}

.loading-more .spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive para información de carga */
@media (max-width: 768px) {
  .load-info {
    padding: 0.75rem 1rem;
    margin-bottom: 0.75rem;
  }
  
  .load-status {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }
  
  .load-text {
    text-align: center;
    font-size: 0.8rem;
  }
  
  .load-more-btn {
    justify-content: center;
    padding: 0.6rem 1rem;
    font-size: 0.8rem;
  }
}

.refresh-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
  transition: left 0.6s ease;
}

.refresh-btn::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  transition: all 0.4s ease;
  transform: translate(-50%, -50%);
}

.refresh-btn:hover::before {
  left: 100%;
}

.refresh-btn:hover::after {
  width: 300px;
  height: 300px;
}

.refresh-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #45a049 0%, #5cb85c 50%, #45a049 100%);
  transform: translateY(-3px) scale(1.08);
  box-shadow: 
    0 12px 32px rgba(76, 175, 80, 0.5),
    0 4px 16px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.refresh-btn:active {
  transform: translateY(-1px) scale(1.02);
  transition: all 0.1s ease;
}

.refresh-btn:disabled {
  background: linear-gradient(135deg, #bbb 0%, #ddd 50%, #bbb 100%);
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  color: #888;
}

.refresh-icon {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  filter: drop-shadow(0 1px 2px rgba(0,0,0,0.2));
}

.refresh-icon.spinning {
  animation: spinGlow 1.8s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes spinGlow {
  0% { 
    transform: rotate(0deg) scale(1); 
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.2));
  }
  25% {
    transform: rotate(90deg) scale(1.1);
    filter: drop-shadow(0 2px 4px rgba(255,255,255,0.5));
  }
  50% { 
    transform: rotate(180deg) scale(1.15);
    filter: drop-shadow(0 3px 6px rgba(255,255,255,0.7));
  }
  75% {
    transform: rotate(270deg) scale(1.1);
    filter: drop-shadow(0 2px 4px rgba(255,255,255,0.5));
  }
  100% { 
    transform: rotate(360deg) scale(1); 
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.2));
  }
}

.page-content {
  padding: clamp(8px, 1.5vw, 16px) clamp(12px, 2vw, 20px);
  box-sizing: border-box;
  width: 100%;
}

/* FILTROS AVANZADOS ULTRA COMPACTOS */
.advanced-filters {
  background: linear-gradient(135deg, #f0fff4 0%, #e8f5e8 100%);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-radius: clamp(6px, 1.5vw, 8px);
  padding: clamp(0.4rem, 1vw, 0.6rem);
  margin-bottom: clamp(0.4rem, 1vw, 0.6rem);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.08);
  width: 100%;
  box-sizing: border-box;
  transition: all 0.3s ease;
}

.advanced-filters:hover {
  border-color: rgba(76, 175, 80, 0.5);
  box-shadow: 0 3px 12px rgba(76, 175, 80, 0.12);
  transform: translateY(-1px);
}

.filters-main {
  display: flex;
  flex-wrap: wrap;
  gap: clamp(0.3rem, 0.8vw, 0.4rem);
  margin-bottom: clamp(0.3rem, 0.8vw, 0.4rem);
  width: 100%;
  align-items: stretch;
  justify-content: space-between;
}

.filters-left {
  display: flex;
  flex-wrap: wrap;
  gap: clamp(0.3rem, 0.8vw, 0.4rem);
  flex: 1;
  min-width: 0;
}

.filters-right {
  display: flex;
  align-items: center;
  margin-left: clamp(0.5rem, 1.5vw, 1rem);
  flex-shrink: 0;
}

.filters-right .visor-stats-compact {
  margin: 0;
  padding: 0;
  display: flex;
  gap: clamp(0.3rem, 0.8vw, 0.4rem);
}

.search-box {
  position: relative;
  flex: 1;
  min-width: clamp(180px, 35vw, 250px);
  max-width: 100%;
}

.search-icon {
  position: absolute;
  left: clamp(0.5rem, 1.2vw, 0.7rem);
  top: 50%;
  transform: translateY(-50%);
  color: rgba(76, 175, 80, 0.6);
  width: clamp(14px, 2.2vw, 16px);
  height: clamp(14px, 2.2vw, 16px);
  pointer-events: none;
  z-index: 2;
}

.search-input {
  width: 100%;
  padding: clamp(10px, 1.2vw, 12px) clamp(44px, 5vw, 48px) clamp(10px, 1.2vw, 12px) clamp(44px, 5vw, 48px);
  border: 1.5px solid rgba(76, 175, 80, 0.2);
  border-radius: 50px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  font-size: clamp(12px, 1.3vw, 13px);
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
  font-size: clamp(11px, 1.2vw, 12px);
}

.clear-search-btn {
  position: absolute;
  right: clamp(12px, 1.5vw, 14px);
  top: 50%;
  transform: translateY(-50%);
  background: rgba(239, 68, 68, 0.1);
  border: none;
  border-radius: 50%;
  width: clamp(20px, 2.5vw, 24px);
  height: clamp(20px, 2.5vw, 24px);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 0;
  z-index: 2;
}

.clear-search-btn:hover {
  background: rgba(239, 68, 68, 0.2);
  transform: translateY(-50%) scale(1.1);
}

.clear-search-btn svg {
  width: clamp(10px, 1.5vw, 12px);
  height: clamp(10px, 1.5vw, 12px);
  color: #ef4444;
}

.search-loading {
  position: absolute;
  right: clamp(12px, 1.5vw, 14px);
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}

.search-loading svg {
  width: clamp(14px, 2vw, 16px);
  height: clamp(14px, 2vw, 16px);
  color: #3b82f6;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.date-range-filter {
  display: flex;
  flex-wrap: wrap;
  gap: clamp(0.4rem, 1vw, 0.6rem);
  align-items: center;
  width: 100%;
}

.date-picker-container {
  display: flex;
  align-items: center;
  gap: clamp(0.25rem, 0.6vw, 0.35rem);
  flex-wrap: wrap;
}

.date-label {
  font-weight: 500;
  color: #4b5563;
  white-space: nowrap;
  font-size: clamp(0.6rem, 1.2vw, 0.7rem);
}

.date-input {
  padding: clamp(0.25rem, 0.6vw, 0.35rem) clamp(0.4rem, 1vw, 0.5rem);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: clamp(4px, 1vw, 6px);
  background: rgba(255, 255, 255, 0.9);
  font-size: clamp(0.6rem, 1.2vw, 0.7rem);
  transition: all 0.3s ease;
  min-width: clamp(100px, 16vw, 120px);
}

.date-input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
}

.quick-date-filters {
  display: flex;
  flex-wrap: wrap;
  gap: clamp(0.25rem, 0.6vw, 0.35rem);
  margin-left: auto;
}

.quick-date-btn {
  padding: clamp(0.2rem, 0.5vw, 0.25rem) clamp(0.4rem, 1vw, 0.5rem);
  background: rgba(0, 0, 0, 0.05);
  border: none;
  border-radius: clamp(3px, 0.8vw, 4px);
  font-size: clamp(0.6rem, 1.2vw, 0.7rem);
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
  gap: clamp(0.15rem, 0.5vw, 0.25rem);
  padding: clamp(0.2rem, 0.5vw, 0.25rem) clamp(0.4rem, 1vw, 0.5rem);
  background: rgba(244, 67, 54, 0.1);
  border: none;
  border-radius: clamp(3px, 0.8vw, 4px);
  font-size: clamp(0.6rem, 1.2vw, 0.7rem);
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
  padding-top: clamp(0.3rem, 0.8vw, 0.4rem);
  margin-top: clamp(0.2rem, 0.5vw, 0.25rem);
}

.advanced-filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(clamp(150px, 20vw, 180px), 1fr));
  gap: clamp(0.4rem, 1vw, 0.6rem);
  margin-bottom: clamp(0.3rem, 0.8vw, 0.4rem);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: clamp(0.15rem, 0.4vw, 0.2rem);
}

.filter-label {
  font-weight: 600;
  color: #4b5563;
  margin-bottom: clamp(0.05rem, 0.2vw, 0.1rem);
  font-size: clamp(0.6rem, 1.2vw, 0.7rem);
}

.filter-options {
  display: flex;
  flex-wrap: wrap;
  gap: clamp(0.3rem, 0.8vw, 0.4rem);
}

.checkbox-option {
  display: flex;
  align-items: center;
  gap: clamp(0.15rem, 0.5vw, 0.25rem);
  cursor: pointer;
  user-select: none;
  font-size: clamp(0.6rem, 1.2vw, 0.7rem);
}

.checkbox-option input[type="checkbox"] {
  width: clamp(10px, 1.5vw, 12px);
  height: clamp(10px, 1.5vw, 12px);
  accent-color: #4CAF50;
  cursor: pointer;
}

.filter-select {
  padding: clamp(0.25rem, 0.6vw, 0.3rem) clamp(0.4rem, 1vw, 0.5rem);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: clamp(4px, 1vw, 6px);
  background: rgba(255, 255, 255, 0.9);
  font-size: clamp(0.6rem, 1.2vw, 0.7rem);
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

.sort-options {
  display: flex;
  flex-wrap: wrap;
  gap: clamp(0.25rem, 0.6vw, 0.35rem);
}

.sort-btn {
  display: flex;
  align-items: center;
  gap: clamp(0.15rem, 0.5vw, 0.25rem);
  padding: clamp(0.2rem, 0.5vw, 0.25rem) clamp(0.4rem, 1vw, 0.5rem);
  background: rgba(0, 0, 0, 0.05);
  border: none;
  border-radius: clamp(3px, 0.8vw, 4px);
  font-size: clamp(0.6rem, 1.2vw, 0.7rem);
  font-weight: 500;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.sort-btn:hover {
  background: rgba(0, 0, 0, 0.1);
}

.sort-btn.active {
  background: #4CAF50;
  color: white;
}

.advanced-actions {
  display: flex;
  flex-wrap: wrap;
  gap: clamp(0.4rem, 1vw, 0.6rem);
  justify-content: flex-end;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: clamp(0.15rem, 0.5vw, 0.25rem);
  padding: clamp(0.25rem, 0.6vw, 0.3rem) clamp(0.4rem, 1vw, 0.5rem);
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
  border: none;
  border-radius: clamp(3px, 0.8vw, 4px);
  font-weight: 500;
  font-size: clamp(0.6rem, 1.2vw, 0.7rem);
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
  gap: clamp(0.25rem, 0.6vw, 0.35rem);
  padding: clamp(0.3rem, 0.8vw, 0.4rem) clamp(0.5rem, 1.2vw, 0.7rem);
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.2);
  border-radius: clamp(4px, 1vw, 6px);
  color: #4CAF50;
  font-size: clamp(0.65rem, 1.3vw, 0.75rem);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: clamp(0.3rem, 0.8vw, 0.4rem);
  width: 100%;
  justify-content: center;
}

.toggle-filters-btn:hover {
  background: rgba(76, 175, 80, 0.15);
  border-color: rgba(76, 175, 80, 0.3);
}

.toggle-filters-btn svg {
  transition: transform 0.3s ease;
}

.active-filters {
  margin-top: clamp(0.6rem, 1.5vw, 0.8rem);
  padding-top: clamp(0.6rem, 1.5vw, 0.8rem);
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.active-filters-label {
  font-size: clamp(0.7rem, 1.5vw, 0.8rem);
  font-weight: 600;
  color: #4b5563;
  margin-bottom: clamp(0.3rem, 0.8vw, 0.4rem);
  display: block;
}

.active-filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: clamp(0.35rem, 1vw, 0.5rem);
  align-items: center;
}

.filter-tag {
  display: flex;
  align-items: center;
  gap: clamp(0.25rem, 0.8vw, 0.35rem);
  padding: clamp(0.25rem, 0.8vw, 0.35rem) clamp(0.5rem, 1.2vw, 0.65rem);
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  border-radius: clamp(12px, 3vw, 16px);
  font-size: clamp(0.6rem, 1.4vw, 0.75rem);
  font-weight: 500;
  white-space: nowrap;
}

.remove-filter {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: clamp(14px, 2.5vw, 16px);
  height: clamp(14px, 2.5vw, 16px);
  border-radius: 50%;
  transition: all 0.2s ease;
}

.remove-filter:hover {
  background: rgba(255, 255, 255, 0.2);
}

.clear-all-filters {
  padding: clamp(0.25rem, 0.8vw, 0.35rem) clamp(0.5rem, 1.2vw, 0.65rem);
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid rgba(244, 67, 54, 0.2);
  border-radius: clamp(12px, 3vw, 16px);
  color: #f44336;
  font-size: clamp(0.6rem, 1.4vw, 0.75rem);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.clear-all-filters:hover {
  background: rgba(244, 67, 54, 0.15);
  border-color: rgba(244, 67, 54, 0.3);
}

/* Filtros legacy (mantener para compatibilidad) */
.filters-section {
  display: none; /* Ocultar filtros antiguos */
}

.sort-btn.active {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  border-color: #4CAF50;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
  transform: translateY(-1px);
}

.sort-btn.active:hover {
  background: linear-gradient(135deg, #45a049 0%, #3d8b40 100%);
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(76, 175, 80, 0.4);
}

.sort-btn svg {
  transition: transform 0.2s ease;
  flex-shrink: 0;
}

.clear-filters-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 10px;
  border: 1px solid rgba(220, 53, 69, 0.3);
  border-radius: 12px;
  background: linear-gradient(135deg, #ffffff 0%, #fef8f8 100%);
  color: #dc3545;
  font-size: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px rgba(220, 53, 69, 0.1);
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin-left: auto;
}

.clear-filters-btn:hover {
  border-color: rgba(220, 53, 69, 0.5);
  background: linear-gradient(135deg, rgba(220, 53, 69, 0.05) 0%, rgba(220, 53, 69, 0.02) 100%);
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(220, 53, 69, 0.2);
}

.suggestions-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-top: none;
  border-radius: 0 0 8px 8px;
  box-shadow: 
    0 6px 20px rgba(0, 0, 0, 0.12),
    0 2px 8px rgba(76, 175, 80, 0.15),
    0 1px 4px rgba(0, 0, 0, 0.08);
  max-height: 150px;
  overflow-y: auto;
  z-index: 9999;
  animation: fadeInDown 0.2s ease-out;
}

@keyframes fadeInDown {
  0% {
    opacity: 0;
    transform: translateY(-5px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.suggestion-item {
  padding: 8px 12px;
  cursor: pointer;
  font-size: 12px;
  color: #333;
  transition: all 0.2s ease;
  border-bottom: 1px solid rgba(224, 224, 224, 0.3);
}

.suggestion-item:hover {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(76, 175, 80, 0.05) 100%);
  color: #4CAF50;
  font-weight: 500;
}

.suggestion-item:last-child {
  border-bottom: none;
}

.suggestion-more {
  padding: 6px 12px;
  font-size: 10px;
  color: #666;
  font-style: italic;
  text-align: center;
  background: rgba(246, 246, 246, 0.8);
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
}

.clear-user-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(108, 117, 125, 0.1);
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #6c757d;
  transition: all 0.2s ease;
}

.clear-user-btn:hover {
  background: rgba(220, 53, 69, 0.1);
  color: #dc3545;
  transform: translateY(-50%) scale(1.1);
}

.clear-user-btn svg {
  transition: transform 0.2s ease;
}

.clear-user-btn:hover svg {
  transform: rotate(90deg);
}

.registros-section {
  background: linear-gradient(135deg, #ffffff 0%, #fafffe 100%);
  border-radius: clamp(12px, 3vw, 20px);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.08),
    0 2px 16px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255,255,255,0.8);
  border: 1px solid rgba(76, 175, 80, 0.1);
  padding: clamp(12px, 2.5vw, 18px);
  transition: all 0.3s ease;
  position: relative;
  z-index: 5;
  box-sizing: border-box;
  overflow: hidden;
}

.registros-section:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 12px 40px rgba(0, 0, 0, 0.12),
    0 4px 20px rgba(0, 0, 0, 0.06),
    inset 0 1px 0 rgba(255,255,255,0.9);
}

.loading-container, .error-container, .empty-state {
  padding: 80px 32px;
  text-align: center;
  color: #666;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

.spinner-large {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(76, 175, 80, 0.1);
  border-top: 4px solid #4CAF50;
  border-radius: 50%;
  animation: spinLarge 1.2s cubic-bezier(0.55, 0.06, 0.68, 0.19) infinite;
  margin: 0 auto 20px;
  position: relative;
}

.spinner-large::after {
  content: '';
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  border: 4px solid transparent;
  border-top: 4px solid rgba(76, 175, 80, 0.3);
  border-radius: 50%;
  animation: spinLarge 2s linear infinite reverse;
}

@keyframes spinLarge {
  0% { transform: rotate(0deg) scale(1); }
  50% { transform: rotate(180deg) scale(1.1); }
  100% { transform: rotate(360deg) scale(1); }
}

.error-container {
  color: #d63384;
}

.retry-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #d63384 0%, #c2185b 50%, #d63384 100%);
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 50px;
  cursor: pointer;
  margin-top: 16px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 
    0 4px 16px rgba(214, 51, 132, 0.35),
    0 2px 6px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
  margin-left: auto;
  margin-right: auto;
}

.retry-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
  transition: left 0.5s ease;
}

.retry-btn:hover::before {
  left: 100%;
}

.retry-btn:hover {
  background: linear-gradient(135deg, #c2185b 0%, #ad1457 50%, #c2185b 100%);
  transform: translateY(-2px) scale(1.05);
  box-shadow: 
    0 8px 24px rgba(214, 51, 132, 0.5),    0 4px 12px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.empty-state {
  color: #666;
}

.empty-icon {
  margin-bottom: 24px;
  animation: bounce 2s ease-in-out infinite;
  display: flex;
  justify-content: center;
  align-items: center;
}

.empty-icon svg {
  filter: drop-shadow(0 4px 8px rgba(76, 175, 80, 0.3));
  transition: all 0.3s ease;
}

.empty-state:hover .empty-icon svg {
  transform: scale(1.1) rotate(5deg);
  filter: drop-shadow(0 6px 12px rgba(76, 175, 80, 0.4));
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

.empty-state h3 {
  color: #4CAF50;
  font-size: 24px;
  margin-bottom: 12px;
  font-weight: 600;
}

.empty-state p {
  font-size: 16px;
  color: #888;
}

.table-container {
  overflow-x: auto;
  animation: fadeInUp 0.6s ease-out 0.2s both;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  background: white;
  box-sizing: border-box;
  -webkit-overflow-scrolling: touch;
  overscroll-behavior-x: contain;
  overscroll-behavior-y: auto;
  scroll-behavior: smooth;
}

@keyframes fadeInUp {
  0% { 
    opacity: 0; 
    transform: translateY(40px) scale(0.9); 
  }
  100% { 
    opacity: 1; 
    transform: translateY(0) scale(1); 
  }
}

.registros-table {
  width: 100%;
  min-width: clamp(500px, 85vw, 900px);
  border-collapse: collapse;
  position: relative;
}

.registros-table th {
  background: #E8F5E9;
  padding: 16px 20px;
  text-align: left;
  font-weight: 600;
  color: #2E7D32;
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.8px;
  position: sticky;
  top: 0;
  z-index: 10;
  border-bottom: 1px solid #C8E6C9;
  white-space: nowrap;
  border-right: none;
}

.registros-table td {
  padding: 16px 20px;
  border-bottom: 1px solid #F0F0F0;
  font-size: 13px;
  transition: all 0.3s ease;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 0;
  text-align: left;
  vertical-align: middle;
  background: white;
  border-right: none;
}

.registros-table tbody tr {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
}

.registros-table tbody tr:nth-child(even) td {
  background: #FAFAFA;
}

.registros-table tbody tr:hover td {
  background: #F5F5F7 !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.foto-mini {
  width: clamp(24px, 4vw, 32px);
  height: clamp(24px, 4vw, 32px);
  object-fit: cover;
  border-radius: clamp(4px, 1vw, 6px);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 1px solid rgba(76, 175, 80, 0.2);
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}

.foto-mini:hover {
  transform: scale(1.05);
  border-color: #4CAF50;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.25);
}

.no-foto {
  color: #999;
  font-style: italic;
  font-size: clamp(8px, 1.8vw, 10px);
}

.ubicacion {
  font-family: monospace;
  font-size: clamp(7px, 1.6vw, 9px);
  line-height: 1.3;
}

.descripcion {
  max-width: clamp(110px, 14vw, 140px);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.fecha {
  white-space: nowrap;
  font-size: clamp(8px, 1.8vw, 10px);
}

.usuario-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.usuario-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #66BB6A 0%, #81C784 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(102, 187, 106, 0.25);
  transition: all 0.3s ease;
}

.usuario-avatar:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(102, 187, 106, 0.35);
}

.usuario-avatar svg {
  width: 20px;
  height: 20px;
  stroke: white;
  stroke-width: 2;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

.usuario-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.usuario-info strong {
  font-size: 13px;
  color: #1D1D1F;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.usuario-info small {
  font-size: 11px;
  color: #8E8E93;
  font-weight: 400;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.btn-ver {
  width: 32px;
  height: 32px;
  padding: 0;
  background: linear-gradient(135deg, #8BC34A, #7CB342);
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(139, 195, 74, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.btn-ver::before {
  display: none;
}

.btn-ver:hover {
  background: linear-gradient(135deg, #7CB342, #689F38);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(139, 195, 74, 0.4);
}

.btn-ver:active {
  transform: scale(1.05);
  box-shadow: 0 3px 10px rgba(139, 195, 74, 0.3);
}

.btn-ver svg {
  width: 16px;
  height: 16px;
  transition: all 0.3s ease;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.btn-ver:hover svg {
  transform: scale(1.1);
}

.btn-eliminar {
  width: 32px;
  height: 32px;
  padding: 0;
  background: linear-gradient(135deg, #f44336, #d32f2f);
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 2px 8px rgba(244, 67, 54, 0.3);
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.btn-eliminar::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
  transition: left 0.5s ease;
}

.btn-eliminar:hover::before {
  left: 100%;
}

.btn-eliminar:hover {
  background: linear-gradient(135deg, #d32f2f, #c62828);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.4);
}

.btn-eliminar:active {
  transform: scale(1.05);
  box-shadow: 0 3px 10px rgba(244, 67, 54, 0.3);
}

.btn-eliminar svg {
  width: 16px;
  height: 16px;
  transition: all 0.3s ease;
}

.btn-eliminar:hover svg {
  transform: scale(1.1);
}

/* Botón de notificar - Naranja oscuro */
.btn-notificar {
  width: 32px;
  height: 32px;
  padding: 0;
  background: linear-gradient(135deg, #E65100, #D84315);
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 2px 8px rgba(230, 81, 0, 0.35);
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.btn-notificar::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
  transition: left 0.5s ease;
}

.btn-notificar:hover::before {
  left: 100%;
}

.btn-notificar:hover {
  background: linear-gradient(135deg, #D84315, #BF360C);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(230, 81, 0, 0.45);
}

.btn-notificar:active {
  transform: scale(1.05);
  box-shadow: 0 3px 10px rgba(230, 81, 0, 0.35);
}

.btn-notificar svg {
  width: 16px;
  height: 16px;
  transition: all 0.3s ease;
}

.btn-notificar:hover svg {
  transform: scale(1.1);
}

/* Label para botón notificar (naranja oscuro) */
.btn-label-notificar {
  font-size: 10px;
  color: #E65100;
  font-weight: 600;
  text-transform: none;
  letter-spacing: 0.3px;
  margin-top: 3px;
  opacity: 0.85;
  transition: all 0.3s ease;
  text-align: center;
}

.action-container:hover .btn-label-notificar {
  opacity: 1;
  color: #D84315;
}

/* Modal de notificación - Naranja Oscuro Profesional - CON ESPECIFICIDAD ALTA */
.modal-notificar.modal-edit-container {
  max-width: 720px !important;
  animation: modalSlideIn 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border-radius: 14px !important;
  overflow: hidden;
  box-shadow: 0 16px 48px rgba(230, 81, 0, 0.35) !important;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Header con naranja oscuro - MAYOR ESPECIFICIDAD */
.modal-notificar.modal-edit-container .modal-edit-header {
  background: linear-gradient(135deg, #E65100 0%, #D84315 50%, #BF360C 100%) !important;
  padding: 16px 22px !important;
  border-bottom: 3px solid #BF360C !important;
  box-shadow: 0 4px 16px rgba(230, 81, 0, 0.4) !important;
  position: relative;
}

.modal-notificar.modal-edit-container .modal-edit-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 15% 40%, rgba(255, 255, 255, 0.12) 0%, transparent 60%);
  pointer-events: none;
}

.modal-notificar.modal-edit-container .modal-edit-header h3 {
  color: #ffffff !important;
  font-size: 15px !important;
  font-weight: 700 !important;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.25) !important;
  letter-spacing: 0.3px !important;
  margin: 0 !important;
}

.modal-notificar.modal-edit-container .header-subtitle {
  color: rgba(255, 255, 255, 0.93) !important;
  font-size: 11px !important;
  font-weight: 500 !important;
  display: flex !important;
  align-items: center;
  margin-top: 4px !important;
  background: rgba(0, 0, 0, 0.18) !important;
  padding: 3px 9px !important;
  border-radius: 10px !important;
  backdrop-filter: blur(8px);
}

.modal-notificar.modal-edit-container .btn-close-edit {
  background: rgba(255, 255, 255, 0.16) !important;
  backdrop-filter: blur(8px);
  border: 1.5px solid rgba(255, 255, 255, 0.28) !important;
  transition: all 0.3s ease !important;
  width: 30px !important;
  height: 30px !important;
  padding: 0 !important;
}

.modal-notificar.modal-edit-container .btn-close-edit:hover {
  background: rgba(255, 255, 255, 0.28) !important;
  transform: rotate(90deg) scale(1.05) !important;
  border-color: rgba(255, 255, 255, 0.45) !important;
}

.modal-notificar.modal-edit-container .header-icon-wrapper {
  background: rgba(255, 255, 255, 0.2) !important;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.35) !important;
  border: 1.5px solid rgba(255, 255, 255, 0.3) !important;
  width: 38px !important;
  height: 38px !important;
}

/* Section titles con especificidad alta */
.modal-notificar .section-title {
  color: #D84315 !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
  margin-bottom: 12px !important;
  padding-bottom: 8px !important;
  border-bottom: 2px solid rgba(230, 81, 0, 0.18) !important;
  position: relative;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modal-notificar .section-title::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 50px;
  height: 2px;
  background: #D84315;
  border-radius: 2px;
}

.modal-notificar .modal-edit-readonly-section {
  background: linear-gradient(135deg, rgba(230, 81, 0, 0.04), transparent) !important;
  border: 1.5px solid rgba(230, 81, 0, 0.18) !important;
  border-radius: 11px !important;
  padding: 14px !important;
}

.modal-notificar .readonly-grid-3col {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-top: 10px;
}

.modal-notificar .readonly-card {
  background: white !important;
  border: 1.5px solid rgba(230, 81, 0, 0.22) !important;
  border-radius: 9px !important;
  padding: 10px !important;
  transition: all 0.25s ease;
  position: relative;
}

.modal-notificar .readonly-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 3px;
  height: 100%;
  background: #D84315;
  transform: scaleY(0);
  transform-origin: top;
  transition: transform 0.25s ease;
  border-radius: 9px 0 0 9px;
}

.modal-notificar .readonly-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(230, 81, 0, 0.2) !important;
  border-color: #D84315 !important;
}

.modal-notificar .readonly-card:hover::before {
  transform: scaleY(1);
}

.modal-notificar .readonly-card-icon {
  color: #E65100 !important;
  margin-bottom: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px !important;
  height: 32px !important;
  background: linear-gradient(135deg, rgba(230, 81, 0, 0.13), rgba(230, 81, 0, 0.07)) !important;
  border-radius: 8px !important;
  transition: all 0.25s ease;
}

.modal-notificar .readonly-card:hover .readonly-card-icon {
  background: linear-gradient(135deg, rgba(230, 81, 0, 0.22), rgba(230, 81, 0, 0.13)) !important;
  transform: scale(1.08);
}

.modal-notificar .readonly-card-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.modal-notificar .readonly-card-label {
  font-size: 9px !important;
  color: #777 !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.4px !important;
}

.modal-notificar .readonly-card-value {
  font-size: 12px !important;
  color: #1a1a1a !important;
  font-weight: 600 !important;
  line-height: 1.3 !important;
}

/* Preview de subtítulo */
.modal-notificar .subtitulo-preview {
  background: linear-gradient(135deg, rgba(230, 81, 0, 0.09), rgba(230, 81, 0, 0.05)) !important;
  border: 1.5px solid rgba(230, 81, 0, 0.25) !important;
  border-radius: 9px !important;
  padding: 8px 11px !important;
  font-size: 11px !important;
  color: #D84315 !important;
  font-weight: 600 !important;
  line-height: 1.4 !important;
  margin-top: 5px !important;
}

.modal-notificar .motivos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 9px;
  margin-top: 9px;
}

.modal-notificar .motivo-checkbox {
  display: flex;
  align-items: center;
  gap: 7px !important;
  padding: 8px 10px !important;
  border: 1.5px solid #ddd !important;
  border-radius: 8px !important;
  cursor: pointer;
  transition: all 0.25s ease;
  background: white !important;
  position: relative;
}

.modal-notificar .motivo-checkbox:hover {
  border-color: #E65100 !important;
  background: linear-gradient(135deg, rgba(230, 81, 0, 0.07), rgba(230, 81, 0, 0.03)) !important;
  transform: translateX(2px);
  box-shadow: 0 2px 7px rgba(230, 81, 0, 0.14) !important;
}

.modal-notificar .motivo-checkbox.selected {
  border-color: #D84315 !important;
  background: linear-gradient(135deg, rgba(230, 81, 0, 0.13), rgba(230, 81, 0, 0.07)) !important;
  box-shadow: 0 2px 7px rgba(230, 81, 0, 0.17) !important;
}

.modal-notificar .motivo-checkbox.selected:hover {
  background: linear-gradient(135deg, rgba(230, 81, 0, 0.17), rgba(230, 81, 0, 0.09)) !important;
}

.modal-notificar .motivo-checkbox input[type="checkbox"] {
  width: 16px !important;
  height: 16px !important;
  cursor: pointer;
  accent-color: #D84315 !important;
  flex-shrink: 0;
}

.modal-notificar .motivo-checkbox span {
  font-size: 11px !important;
  color: #333 !important;
  font-weight: 500 !important;
  transition: color 0.2s ease;
  line-height: 1.3 !important;
}

.modal-notificar .motivo-checkbox.selected span {
  color: #D84315 !important;
  font-weight: 600 !important;
}

.modal-notificar .form-textarea {
  width: 100% !important;
  padding: 10px !important;
  border: 1.5px solid #ddd !important;
  border-radius: 9px !important;
  font-size: 12px !important;
  line-height: 1.5 !important;
  font-family: 'Inter', sans-serif !important;
  transition: all 0.25s ease !important;
  resize: vertical !important;
  background: white !important;
}

.modal-notificar .form-textarea-notificacion {
  min-height: 130px !important;
}

.modal-notificar .form-textarea:focus {
  outline: none !important;
  border-color: #D84315 !important;
  box-shadow: 0 0 0 3px rgba(230, 81, 0, 0.13), 0 3px 9px rgba(230, 81, 0, 0.13) !important;
  background: white !important;
}

.modal-notificar .form-label {
  font-size: 11px !important;
  font-weight: 600 !important;
  color: #555 !important;
  display: flex !important;
  align-items: center !important;
  gap: 5px !important;
  margin-bottom: 5px !important;
}

.modal-notificar .form-label svg {
  color: #D84315 !important;
}

.modal-notificar .form-help {
  display: block;
  margin-top: 4px !important;
  font-size: 10px !important;
  color: #666 !important;
  font-style: italic;
}

.modal-notificar .textarea-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 4px !important;
  gap: 8px;
}

.modal-notificar .char-count {
  font-size: 9px !important;
  color: #999 !important;
  font-weight: 500 !important;
  white-space: nowrap;
}

.modal-notificar .btn-enviar-notificacion,
.modal-notificar .modal-edit-actions button:last-child {
  background: linear-gradient(135deg, #E65100, #D84315, #BF360C) !important;
  box-shadow: 0 3px 11px rgba(230, 81, 0, 0.38) !important;
  font-size: 12px !important;
  padding: 9px 18px !important;
  font-weight: 600 !important;
  border: none !important;
  color: white !important;
}

.modal-notificar .btn-enviar-notificacion:hover:not(:disabled),
.modal-notificar .modal-edit-actions button:last-child:hover:not(:disabled) {
  background: linear-gradient(135deg, #D84315, #BF360C, #A51C00) !important;
  box-shadow: 0 5px 16px rgba(230, 81, 0, 0.48) !important;
  transform: translateY(-1px) !important;
}

.modal-notificar .btn-enviar-notificacion:active:not(:disabled),
.modal-notificar .modal-edit-actions button:last-child:active:not(:disabled) {
  transform: translateY(0) !important;
  box-shadow: 0 2px 9px rgba(230, 81, 0, 0.38) !important;
}

/* Responsividad con especificidad */
@media (max-width: 768px) {
  .modal-notificar.modal-edit-container {
    max-width: 95vw !important;
    margin: 10px !important;
  }
  
  .modal-notificar .readonly-grid-3col {
    grid-template-columns: 1fr !important;
    gap: 9px !important;
  }
  
  .modal-notificar .motivos-grid {
    grid-template-columns: 1fr !important;
  }
  
  .modal-notificar .textarea-footer {
    flex-direction: column;
    align-items: flex-start !important;
  }
  
  .modal-notificar .char-count {
    align-self: flex-end !important;
  }
  
  .modal-notificar.modal-edit-container .modal-edit-header h3 {
    font-size: 14px !important;
  }
  
  .modal-notificar .section-title {
    font-size: 12px !important;
  }
}

@media (max-width: 480px) {
  .modal-notificar.modal-edit-container {
    max-width: 100vw !important;
    margin: 0 !important;
    border-radius: 14px 14px 0 0 !important;
  }
  
  .modal-notificar .form-textarea-notificacion {
    min-height: 110px !important;
    font-size: 11px !important;
  }
  
  .modal-notificar.modal-edit-container .modal-edit-header {
    padding: 13px 16px !important;
  }
  
  .modal-notificar .readonly-card {
    padding: 9px !important;
  }
  
  .modal-notificar .readonly-card-icon {
    width: 28px !important;
    height: 28px !important;
  }
}

.confirm-delete-modal {
  max-width: 500px;
}

.delete-header {
  background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
}

.delete-icon {
  background: rgba(255, 255, 255, 0.2);
}

.confirm-delete-content {
  padding: 20px;
  text-align: center;
}

.confirm-message {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
}

.registro-info {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 15px;
  margin: 20px 0;
  text-align: left;
}

.info-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #e0e0e0;
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  font-weight: 600;
  color: #666;
}

.info-value {
  color: #333;
  font-weight: 500;
}

.warning-text {
  color: #ff9800;
  font-size: 14px;
  font-weight: 500;
  margin-top: 15px;
}

.btn-cancel {
  padding: 10px 24px;
  background: #e0e0e0;
  color: #333;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-cancel:hover {
  background: #d5d5d5;
  transform: translateY(-2px);
}

.btn-delete-confirm {
  padding: 10px 24px;
  background: linear-gradient(135deg, #f44336, #d32f2f);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(244, 67, 54, 0.3);
}

.btn-delete-confirm:hover {
  background: linear-gradient(135deg, #d32f2f, #c62828);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.4);
}

/* Contenedor principal de acciones (horizontal) */
.actions-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 8px 0;
}

/* Contenedor de acción individual (vertical con botón y label) */
.action-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  min-width: 50px;
}

/* Label para botón ver/detalles (verde) */
.btn-label {
  font-size: 10px;
  color: #4CAF50;
  font-weight: 600;
  text-transform: none;
  letter-spacing: 0.3px;
  margin-top: 3px;
  opacity: 0.85;
  transition: all 0.3s ease;
  text-align: center;
}

.action-container:hover .btn-label {
  opacity: 1;
  color: #43A047;
}

/* Label para botón editar (morado) */
.btn-label-editar {
  font-size: 10px;
  color: #6366f1;
  font-weight: 600;
  text-transform: none;
  letter-spacing: 0.3px;
  margin-top: 3px;
  opacity: 0.85;
  transition: all 0.3s ease;
  text-align: center;
}

.action-container:hover .btn-label-editar {
  opacity: 1;
  color: #5558e3;
}

/* Label para botón eliminar (rojo) */
.btn-label-eliminar {
  font-size: 10px;
  color: #f44336;
  font-weight: 600;
  text-transform: none;
  letter-spacing: 0.3px;
  margin-top: 3px;
  opacity: 0.85;
  transition: all 0.3s ease;
  text-align: center;
}

.action-container:hover .btn-label-eliminar {
  opacity: 1;
  color: #d32f2f;
}

/* Estilos para columnas específicas de la tabla */
.col-id {
  width: 55px !important;
  max-width: 55px !important;
  min-width: 55px !important;
}

.col-usuario {
  width: 170px !important;
  max-width: 170px !important;
  min-width: 170px !important;
  text-align: left !important;
}

.col-foto {
  width: 55px !important;
  max-width: 55px !important;
  min-width: 55px !important;
}

.col-tipo {
  width: 75px !important;
  max-width: 75px !important;
  min-width: 75px !important;
}

.col-ubicacion {
  width: 110px !important;
  max-width: 110px !important;
  min-width: 110px !important;
}

.col-descripcion {
  width: 140px !important;
  max-width: 140px !important;
  min-width: 140px !important;
  text-align: left !important;
}

.col-fecha {
  width: 90px !important;
  max-width: 90px !important;
  min-width: 90px !important;
}

.col-acciones {
  width: 160px !important;
  max-width: 160px !important;
  min-width: 160px !important;
}

/* Estilos para contenedor de fecha y hora */
.fecha-hora-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  line-height: 1.1;
}

.hora-display {
  font-size: 11px;
  font-weight: 700;
  color: #7b1fa2;
  text-shadow: 0 1px 2px rgba(123, 31, 162, 0.2);
  background: linear-gradient(135deg, rgba(123, 31, 162, 0.1) 0%, rgba(142, 36, 170, 0.05) 100%);
  padding: 2px 6px;
  border-radius: 8px;
  border: 1px solid rgba(123, 31, 162, 0.2);
  white-space: nowrap;
  letter-spacing: 0.3px;
}

.fecha-display {
  font-size: 9px;
  font-weight: 500;
  color: #666;
  white-space: nowrap;
  opacity: 0.8;
  letter-spacing: 0.2px;
}

/* Estilos para badges de tipo de actividad */
.tipo-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  line-height: 1;
  white-space: nowrap;
  transition: all 0.3s ease;
}

.tipo-campo {
  background: linear-gradient(135deg, #e8f5e8 0%, #f0fff4 100%);
  color: #2e7d32;
  border: 1px solid #4CAF50;
}

.tipo-gabinete {
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  color: #ef6c00;
  border: 1px solid #ff9800;
}

.tipo-badge:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Modal styles empresariales compactos */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(3px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 15px;
  animation: modalBackdropIn 0.25s ease-out;
}

@keyframes modalBackdropIn {
  from {
    opacity: 0;
    backdrop-filter: blur(0px);
  }
  to {
    opacity: 1;
    backdrop-filter: blur(3px);
  }
}

.modal-content {
  background: #ffffff;
  border-radius: 6px;
  box-shadow: 
    0 16px 48px rgba(76, 175, 80, 0.15),
    0 4px 16px rgba(76, 175, 80, 0.08),
    0 0 0 1px rgba(76, 175, 80, 0.1);
  max-width: 520px;
  width: 100%;
  max-height: 85vh;
  overflow: hidden;
  animation: modalContentIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
}

@keyframes modalContentIn {
  from {
    opacity: 0;
    transform: translateY(-30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  padding: 14px 18px;
  color: white;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 2px solid #388e3c;
}

.modal-header-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.modal-icon {
  width: 24px;
  height: 24px;
  background: rgba(255, 255, 255, 0.25);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.modal-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: white;
  letter-spacing: 0.2px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.btn-close {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 4px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: white;
}

.btn-close:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.4);
  transform: scale(1.05);
}

.modal-body {
  padding: 0;
  overflow-y: auto;
  max-height: calc(85vh - 80px);
}

.registro-detalles {
  padding: 20px;
  animation: contentFadeIn 0.3s ease-out 0.1s both;
}

@keyframes contentFadeIn {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  max-width: none;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px;
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.05) 0%, rgba(76, 175, 80, 0.02) 100%);
  border: 1px solid rgba(76, 175, 80, 0.15);
  border-radius: 4px;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.detail-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 3px;
  height: 100%;
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
}

.detail-item:hover {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.08) 0%, rgba(76, 175, 80, 0.04) 100%);
  border-color: rgba(76, 175, 80, 0.3);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.12);
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-icon {
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.25);
}

.detail-content {
  flex: 1;
  min-width: 0;
}

.detail-label {
  display: block;
  font-size: 10px;
  font-weight: 600;
  color: #4CAF50;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
  line-height: 1.2;
}

.detail-value {
  display: block;
  font-size: 13px;
  color: #2c3e50;
  font-weight: 500;
  line-height: 1.3;
  word-break: break-word;
}

.detail-value.highlight {
  color: #4CAF50;
  font-weight: 700;
  font-size: 14px;
}

.detail-value.location {
  font-family: 'Segoe UI Mono', 'Courier New', monospace;
  font-size: 11px;
  background: rgba(76, 175, 80, 0.1);
  padding: 3px 6px;
  border-radius: 4px;
  display: inline-block;
  margin-top: 2px;
  border: 1px solid rgba(76, 175, 80, 0.2);
}

.detail-value.description {
  max-height: 50px;
  overflow-y: auto;
  padding-right: 6px;
}

/* Estilos para badges de tipo en el modal */
.tipo-badge-modal {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  line-height: 1;
  white-space: nowrap;
  transition: all 0.2s ease;
  margin-top: 3px;
}

.tipo-badge-modal.tipo-campo {
  background: linear-gradient(135deg, #e8f5e8 0%, #f0fff4 100%);
  color: #2e7d32;
  border: 1px solid #4CAF50;
}

.tipo-badge-modal.tipo-gabinete {
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  color: #ef6c00;
  border: 1px solid #ff9800;
}

.photo-container {
  margin-top: 6px;
}

.detail-photo {
  width: 100%;
  max-width: 150px;
  height: auto;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.15);
  border: 2px solid rgba(76, 175, 80, 0.2);
}

.detail-photo:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2);
  border-color: rgba(76, 175, 80, 0.4);
}

.map-container {
  margin-top: 6px;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.12);
  border: 2px solid rgba(76, 175, 80, 0.2);
}

.leaflet-map {
  height: 140px;
  width: 100%;
}

.modal-footer {
  padding: 0;
  background: transparent;
  border: none;
  height: 0;
}

/* Estilos del Lightbox */
.lightbox-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.95);
  z-index: 11000;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: lightboxFadeIn 0.3s ease-out;
}

.lightbox-container {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.lightbox-close {
  position: absolute;
  top: -50px;
  right: 0;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.lightbox-close:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.lightbox-image {
  max-width: 100%;
  max-height: 80vh;
  object-fit: contain;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
  cursor: pointer;
  transition: transform 0.3s ease;
  animation: lightboxImageIn 0.4s ease-out;
}

.lightbox-image:hover {
  transform: scale(1.02);
}

.lightbox-hint {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  text-align: center;
  margin: 0;
  padding: 10px 20px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

/* ========== MODAL DE CONFIRMACIÓN DE ELIMINACIÓN - REDISEÑADO ========== */
.modal-overlay-delete {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.2s ease;
}

.modal-delete-container {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 480px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  overflow: hidden;
}

.modal-delete-header {
  background: linear-gradient(135deg, #f44336 0%, #e53935 100%);
  padding: 20px 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
}

.warning-icon {
  color: white;
  flex-shrink: 0;
  animation: pulse 2s infinite;
}

.modal-delete-header h3 {
  color: white;
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  flex: 1;
}

.btn-close-delete {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.btn-close-delete:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.modal-delete-body {
  padding: 24px;
}

.delete-question {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin: 0 0 20px 0;
  text-align: center;
  line-height: 1.5;
}

.registro-info-box {
  background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
  border: 2px solid #ffc107;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 193, 7, 0.2);
}

.info-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.info-label-delete {
  font-size: 11px;
  font-weight: 700;
  color: #f57c00;
  letter-spacing: 0.5px;
}

.info-value-delete {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  text-align: right;
  max-width: 65%;
  word-break: break-word;
}

.warning-box {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #ffebee;
  border-left: 4px solid #f44336;
  border-radius: 8px;
}

.warning-box svg {
  color: #f44336;
  flex-shrink: 0;
}

.warning-box span {
  font-size: 13px;
  font-weight: 600;
  color: #c62828;
}

.modal-delete-footer {
  padding: 16px 24px;
  background: #f5f5f5;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  border-top: 1px solid #e0e0e0;
}

.btn-cancel-delete {
  padding: 10px 20px;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #666;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-cancel-delete:hover {
  background: #f5f5f5;
  border-color: #bdbdbd;
  transform: translateY(-1px);
}

.btn-confirm-delete {
  padding: 10px 20px;
  background: linear-gradient(135deg, #f44336 0%, #e53935 100%);
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 2px 8px rgba(244, 67, 54, 0.3);
}

.btn-confirm-delete:hover {
  background: linear-gradient(135deg, #e53935 0%, #d32f2f 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.4);
}

.btn-confirm-delete:active {
  transform: translateY(0);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
}

/* Responsive para móviles */
@media (max-width: 768px) {
  .modal-delete-container {
    width: 95%;
    max-width: 420px;
  }

  .modal-delete-header {
    padding: 16px 20px;
  }

  .modal-delete-header h3 {
    font-size: 16px;
  }

  .modal-delete-body {
    padding: 20px;
  }

  .delete-question {
    font-size: 15px;
  }

  .info-label-delete {
    font-size: 10px;
  }

  .info-value-delete {
    font-size: 13px;
  }

  .modal-delete-footer {
    padding: 12px 16px;
    flex-direction: column-reverse;
  }

  .btn-cancel-delete,
  .btn-confirm-delete {
    width: 100%;
    justify-content: center;
  }
}

@keyframes lightboxFadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes lightboxImageIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* ========== MODAL DE EDICIÓN DE REGISTRO ========== */
.modal-overlay-edit {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(6px);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.2s ease;
}

.modal-edit-container {
  background: #ffffff;
  border-radius: 24px;
  width: 95%;
  max-width: 580px;
  max-height: 92vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 30px 90px rgba(0, 0, 0, 0.4);
  animation: slideUp 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
  overflow: hidden;
}

.modal-edit-header {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
  padding: 14px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
  flex-shrink: 0;
}

.header-icon-wrapper {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.header-text {
  flex: 1;
  min-width: 0;
}

.modal-edit-header h3 {
  color: white;
  font-size: 16px;
  font-weight: 700;
  margin: 0;
  line-height: 1.3;
}

.header-subtitle {
  color: rgba(255, 255, 255, 0.85);
  font-size: 11px;
  font-weight: 500;
  display: block;
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.btn-close-edit {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.btn-close-edit:hover {
  background: rgba(255, 255, 255, 0.35);
  transform: scale(1.1) rotate(90deg);
}

/* Área de scroll */
.modal-edit-scroll-area {
  flex: 1;
  overflow-y: auto;
  overscroll-behavior: contain;
}

/* Sección de solo lectura */
.modal-edit-readonly-section {
  padding: 20px 24px;
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 1px solid #e2e8f0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 16px 0;
}

.section-title svg {
  color: #94a3b8;
}

/* Grid de 2 columnas para ubicación y foto */
.readonly-grid-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.readonly-card {
  background: white;
  border-radius: 16px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.readonly-card-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.readonly-card-icon-muted {
  background: linear-gradient(135deg, #94a3b8 0%, #cbd5e1 100%);
  box-shadow: 0 4px 12px rgba(148, 163, 184, 0.3);
}

.readonly-card-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.readonly-card-label {
  font-size: 11px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.readonly-card-value {
  font-size: 12px;
  font-weight: 600;
  color: #1e293b;
  word-break: break-word;
}

.readonly-photo-preview-compact {
  margin-top: 4px;
}

.edit-photo-thumb-compact {
  width: 80px;
  height: 60px;
  object-fit: cover;
  border-radius: 10px;
  cursor: pointer;
  border: 2px solid #e2e8f0;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.edit-photo-thumb-compact:hover {
  transform: scale(1.08);
  border-color: #8b5cf6;
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
}

.readonly-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px dashed #e2e8f0;
}

.readonly-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.readonly-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.readonly-icon-muted {
  background: #cbd5e1;
}

.readonly-content {
  flex: 1;
  min-width: 0;
}

.readonly-label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin-bottom: 4px;
}

.readonly-value {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  word-break: break-word;
}

.readonly-muted {
  color: #94a3b8;
  font-style: italic;
  font-weight: 500;
}

.readonly-photo-item {
  align-items: flex-start;
}

.readonly-photo-preview {
  margin-top: 8px;
}

.edit-photo-thumb {
  width: 120px;
  height: 90px;
  object-fit: cover;
  border-radius: 10px;
  cursor: pointer;
  border: 2px solid #e2e8f0;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.edit-photo-thumb:hover {
  transform: scale(1.05);
  border-color: #8b5cf6;
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
}

.photo-hint {
  display: block;
  font-size: 11px;
  color: #94a3b8;
  margin-top: 6px;
}

/* Body del formulario */
.modal-edit-body {
  padding: 20px 24px 24px 24px;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-row-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #334155;
}

.form-label svg {
  color: #8b5cf6;
  flex-shrink: 0;
}

.optional-label {
  font-size: 11px;
  font-weight: 400;
  color: #94a3b8;
  margin-left: auto;
}

/* Selector de tipo (Campo/Gabinete) */
.tipo-selector {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.tipo-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px 12px;
  border: 2px solid #e2e8f0;
  border-radius: 14px;
  background: #fff;
  cursor: pointer;
  transition: all 0.25s ease;
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
}

.tipo-btn svg {
  transition: all 0.25s ease;
}

.tipo-btn:hover {
  border-color: #cbd5e1;
  transform: translateY(-2px);
}

.tipo-btn.tipo-campo.active {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  border-color: #22c55e;
  color: #166534;
  box-shadow: 0 4px 15px rgba(34, 197, 94, 0.25);
}

.tipo-btn.tipo-campo.active svg {
  color: #22c55e;
}

.tipo-btn.tipo-gabinete.active {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-color: #f59e0b;
  color: #92400e;
  box-shadow: 0 4px 15px rgba(245, 158, 11, 0.25);
}

.tipo-btn.tipo-gabinete.active svg {
  color: #f59e0b;
}

/* Select de categoría */
.form-select {
  padding: 14px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px;
  color: #334155;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  padding-right: 44px;
}

.form-select:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.15);
}

.form-select:hover:not(:disabled) {
  border-color: #cbd5e1;
}

.form-select:disabled {
  background-color: #f8fafc;
  color: #94a3b8;
  cursor: not-allowed;
}

/* Input de texto */
.form-input {
  padding: 14px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px;
  color: #334155;
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.15);
}

.form-input:hover:not(:disabled) {
  border-color: #cbd5e1;
}

.form-input::placeholder {
  color: #94a3b8;
}

/* Textarea */
.form-textarea {
  padding: 14px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px;
  color: #334155;
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
  transition: all 0.2s ease;
}

.form-textarea:focus {
  outline: none;
  border-color: #8b5cf6;
  box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.15);
}

.form-textarea:hover {
  border-color: #cbd5e1;
}

.form-textarea::placeholder {
  color: #94a3b8;
}

.char-counter {
  font-size: 11px;
  color: #94a3b8;
  text-align: right;
  margin-top: -4px;
}

/* Footer */
.modal-edit-footer {
  padding: 18px 24px;
  background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  border-top: 1px solid #e2e8f0;
  flex-shrink: 0;
}

.btn-cancel-edit {
  padding: 12px 24px;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-cancel-edit:hover:not(:disabled) {
  background: #f1f5f9;
  border-color: #cbd5e1;
  transform: translateY(-1px);
}

.btn-cancel-edit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-save-edit {
  padding: 12px 28px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35);
}

.btn-save-edit:hover:not(:disabled) {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.45);
}

.btn-save-edit:active:not(:disabled) {
  transform: translateY(0);
}

.btn-save-edit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.spinner-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Responsive modal de edición */
@media (max-width: 768px) {
  .modal-edit-container {
    width: 100%;
    max-width: 100%;
    max-height: 100vh;
    margin: 0;
    border-radius: 0;
  }

  .modal-edit-header {
    padding: 12px 16px;
  }

  .header-icon-wrapper {
    width: 40px;
    height: 40px;
  }

  .modal-edit-header h3 {
    font-size: 16px;
  }

  .modal-edit-readonly-section,
  .modal-edit-body {
    padding: 16px 20px;
  }

  .readonly-grid-2col {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .readonly-card {
    padding: 14px;
  }

  .readonly-card-icon {
    width: 42px;
    height: 42px;
  }

  .form-row-2col {
    grid-template-columns: 1fr;
    gap: 14px;
  }

  .tipo-selector {
    gap: 10px;
  }

  .tipo-btn {
    padding: 14px 10px;
    font-size: 13px;
  }

  .modal-edit-footer {
    padding: 14px 20px;
    flex-direction: column-reverse;
    gap: 10px;
  }

  .btn-cancel-edit,
  .btn-save-edit {
    width: 100%;
    justify-content: center;
    padding: 14px 24px;
  }

  .edit-photo-thumb {
    width: 100px;
    height: 75px;
  }
}

/* Botón de editar en acciones */
.btn-editar {
  width: 32px;
  height: 32px;
  padding: 0;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
}

.btn-editar::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
  transition: left 0.5s ease;
}

.btn-editar:hover::before {
  left: 100%;
}

.btn-editar svg {
  width: 16px;
  height: 16px;
  transition: all 0.3s ease;
}

.btn-editar:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

.btn-editar:active {
  transform: scale(1.05);
  box-shadow: 0 3px 10px rgba(99, 102, 241, 0.3);
}

.btn-editar:hover svg {
  transform: scale(1.1);
}

.btn-label-editar {
  font-size: 10px;
  color: #6366f1;
  font-weight: 600;
  text-transform: none;
  letter-spacing: 0.3px;
  margin-top: 3px;
}

/* Responsive */
@media (max-width: 992px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
}

/* Tablet portrait - 481px a 768px */
@media (min-width: 481px) and (max-width: 768px) {
  .main-content {
    margin-left: 250px;
    width: calc(100vw - 250px);
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 240px;
    width: calc(100vw - 240px);
  }
  
  .page-header {
    padding: 16px 20px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .page-content {
    padding: 16px 20px;
  }
  
  /* Filtros avanzados responsive */
  .search-box {
    min-width: 100%;
  }
  
  .date-range-filter {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
  }
  
  .quick-date-filters {
    margin-left: 0;
    justify-content: flex-start;
  }
  
  .advanced-filters-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .advanced-actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .export-btn {
    justify-content: center;
  }
  
  .toggle-filters-btn {
    font-size: 0.9rem;
  }
  
  .active-filter-tags {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-tag {
    justify-content: space-between;
  }
    .filter-box {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .filter-select {
    width: 100%;
    min-width: unset;
    padding: 14px 48px 14px 20px;
    font-size: 16px; /* Evita el zoom en iOS */
  }

  .filter-input {
    width: 100%;
    min-width: unset;
    padding: 14px 20px;
    font-size: 16px; /* Evita el zoom en iOS */
  }

  .clear-filters-btn {
    width: 100%;
    justify-content: center;
    margin-top: 8px;
  }
  
  .table-container {
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .registros-table {
    min-width: 380px;
    font-size: 8px;
  }
  
  .registros-table th {
    padding: 3px 4px;
    font-size: 6px;
    letter-spacing: 0.1px;
  }
  
  .registros-table td {
    padding: 3px 4px;
    font-size: 8px;
  }
  
  /* Elementos de la tabla ultra compactos para móviles */
  .foto-mini {
    width: 16px;
    height: 16px;
    border-radius: 2px;
    border-width: 0.5px;
  }
  
  .btn-ver {
    width: 16px;
    height: 16px;
  }
  
  .btn-ver svg {
    width: 8px;
    height: 8px;
  }
  
  .usuario-info {
    gap: 0;
  }
  
  .usuario-info strong {
    font-size: 7px;
    line-height: 1.1;
  }
  
  .usuario-info small {
    font-size: 6px;
    line-height: 1;
  }
  
  .ubicacion,
  .fecha,
  .no-foto {
    font-size: 6px;
    line-height: 1;
  }
  
  .descripcion {
    max-width: 80px;
    font-size: 6px;
  }
  
  .modal-content {
    margin: 8px;
    max-width: calc(100vw - 16px);
    max-height: calc(100vh - 16px);
    border-radius: 4px;
  }
  
  .modal-header {
    padding: 12px 16px;
  }
  
  .modal-title {
    font-size: 14px;
  }
  
  .modal-icon {
    width: 20px;
    height: 20px;
    border-radius: 3px;
  }
  
  .btn-close {
    width: 24px;
    height: 24px;
  }
  
  .registro-detalles {
    padding: 16px;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .detail-item {
    padding: 10px;
  }
  
  .detail-icon {
    width: 20px;
    height: 20px;
    border-radius: 3px;
  }
  
  .detail-label {
    font-size: 9px;
  }
  
  .detail-value {
    font-size: 12px;
  }
  
  .detail-value.highlight {
    font-size: 13px;
  }
  
  .modal-footer {
    display: none;
  }
  
  .lightbox-container {
    max-width: 95vw;
    max-height: 95vh;
    gap: 15px;
  }
  
  .lightbox-close {
    top: -40px;
    width: 35px;
    height: 35px;
  }
  
  .lightbox-image {
    max-height: 75vh;
    border-radius: 8px;
  }
  
  .lightbox-hint {
    font-size: 12px;
    padding: 8px 16px;
  }
}

/* Ultra compacto para pantallas muy pequeñas */
@media (max-width: 400px) {
  .page-content {
    padding: 2px 8px;
  }
  
  .registros-table {
    min-width: 320px;
  }
  
  .registros-table th {
    padding: 2px 3px;
    font-size: 5px;
    letter-spacing: 0;
  }
  
  .registros-table td {
    padding: 2px 3px;
    font-size: 7px;
  }
  
  .foto-mini {
    width: 14px;
    height: 14px;
    border-radius: 1px;
  }
  
  .btn-ver {
    width: 14px;
    height: 14px;
  }
  
  .btn-ver svg {
    width: 7px;
    height: 7px;
  }
  
  .usuario-info strong {
    font-size: 6px;
  }
  
  .usuario-info small {
    font-size: 5px;
  }
  
  .ubicacion,
  .fecha,
  .no-foto {
    font-size: 5px;
  }
  
  .descripcion {
    max-width: 60px;
    font-size: 5px;
  }
  
  .advanced-filters {
    padding: 0.2rem 0.25rem;
    margin-bottom: 0.2rem;
  }
  
  .registros-info {
    padding: 0.2rem 0.25rem;
  }
  
  /* Modal más compacto para pantallas ultra pequeñas */
  .modal-content {
    margin: 4px;
    max-width: calc(100vw - 8px);
    max-height: calc(100vh - 8px);
    border-radius: 3px;
  }
  
  .modal-header {
    padding: 10px 12px;
  }
  
  .modal-title {
    font-size: 13px;
  }
  
  .modal-icon {
    width: 18px;
    height: 18px;
    border-radius: 2px;
  }
  
  .btn-close {
    width: 22px;
    height: 22px;
    border-radius: 3px;
  }
  
  .registro-detalles {
    padding: 12px;
  }
  
  .detail-grid {
    gap: 10px;
  }
  
  .detail-item {
    padding: 8px;
  }
  
  .detail-icon {
    width: 18px;
    height: 18px;
    border-radius: 2px;
  }
  
  .detail-label {
    font-size: 8px;
  }
  
  .detail-value {
    font-size: 11px;
  }
  
  .detail-value.highlight {
    font-size: 12px;
  }
  
  .detail-photo {
    max-width: 120px;
  }
  
  .leaflet-map {
    height: 120px;
  }
}

/* Estilos para el contador de registros */
.registros-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  padding: 0.5rem 1rem;
  background: rgba(76, 175, 80, 0.08);
  border-radius: 8px;
  border: 1px solid rgba(76, 175, 80, 0.2);
  font-size: 0.9rem;
}

.registros-total {
  color: #4a4a4a;
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.05) 0%, rgba(76, 175, 80, 0.15) 100%);
  box-shadow: 0 2px 6px rgba(76, 175, 80, 0.1);
  padding: 10px 16px;
  border-radius: 8px;
  position: relative;
  overflow: hidden;
  animation: fadeIn 0.5s ease-out;
  border: 1px solid rgba(76, 175, 80, 0.2);
}

.registros-total::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  animation: shimmer 2s infinite;
}

.registros-total .highlight {
  font-weight: 700;
  color: #4CAF50;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 4px;
  padding: 0.2rem 0.5rem;
  display: inline-block;
  font-size: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.registros-total {
  display: flex;
  align-items: center;
}

.registros-icon {
  font-size: 20px;
  margin-right: 8px;
}

.registros-text {
  flex: 1;
}

.registros-summary {
  display: flex;
  gap: 8px;
}

.registros-badge {
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
  border-radius: 12px;
  padding: 3px 8px;
  font-size: 11px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
  border: 1px solid rgba(33, 150, 243, 0.2);
}

.registros-badge i {
  font-size: 10px;
}

.pagination-badge {
  background: rgba(156, 39, 176, 0.1);
  color: #9C27B0;
  border-color: rgba(156, 39, 176, 0.2);
}

/* === ESTILOS DE PAGINACIÓN === */
.pagination-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 0;
  padding: 0;
  background: transparent;
  border-radius: 0;
  border: none;
  box-shadow: none;
  animation: fadeInUp 0.4s ease-out;
}

.pagination-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 12px 16px;
  background: #E8F5E9;
  border-top: 1px solid #C8E6C9;
}

.pagination-text {
  color: #2E7D32;
  font-size: 13px;
  font-weight: 600;
}

.pagination-text strong {
  color: #1B5E20;
  font-weight: 700;
}

.pagination-selector {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pagination-label {
  color: #2E7D32;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.pagination-select {
  padding: 6px 12px;
  border: 1px solid #C8E6C9;
  border-radius: 8px;
  background: white;
  color: #2E7D32;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 70px;
}

.pagination-select:hover {
  border-color: #8BC34A;
  box-shadow: 0 2px 8px rgba(139, 195, 74, 0.2);
}

.pagination-select:focus {
  outline: none;
  border-color: #8BC34A;
  box-shadow: 0 0 0 3px rgba(139, 195, 74, 0.15);
}

.pagination-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 16px;
  background: #E8F5E9;
  border-top: 1px solid #C8E6C9;
  flex-wrap: wrap;
}

.pagination-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: linear-gradient(135deg, #8BC34A 0%, #7CB342 100%);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(139, 195, 74, 0.3);
  user-select: none;
  min-height: 32px;
}

.pagination-btn::before {
  display: none;
}

.pagination-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #7CB342 0%, #689F38 100%);
  box-shadow: 0 4px 12px rgba(139, 195, 74, 0.4);
  transform: translateY(-1px);
}

.pagination-btn:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(139, 195, 74, 0.3);
}

.pagination-btn:disabled {
  background: #C8E6C9;
  color: #81C784;
  cursor: not-allowed;
  box-shadow: none;
  opacity: 0.5;
}

.pagination-btn svg {
  width: 16px;
  height: 16px;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.pagination-btn-text {
  font-weight: 600;
  letter-spacing: 0.025em;
}

.pagination-first,
.pagination-last {
  padding: 8px;
}

.pagination-numbers {
  display: flex;
  align-items: center;
  gap: 4px;
  margin: 0;
  flex-wrap: wrap;
  justify-content: center;
}

.pagination-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  padding: 0;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: #2E7D32;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
}

.pagination-number::before {
  display: none;
}

.pagination-number:hover:not(.active) {
  background: rgba(139, 195, 74, 0.15);
  color: #1B5E20;
  transform: scale(1.05);
}

.pagination-number.active {
  background: linear-gradient(135deg, #8BC34A 0%, #7CB342 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(139, 195, 74, 0.4);
  cursor: default;
}

.pagination-ellipsis {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  color: #81C784;
  font-size: 16px;
  font-weight: 700;
  user-select: none;
  letter-spacing: 0.1em;
}

.pagination-jump {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  justify-content: center;
  flex-wrap: wrap;
}

.pagination-input {
  width: 80px;
  padding: 0.5rem 0.75rem;
  border: 1px solid rgba(209, 213, 219, 0.6);
  border-radius: 8px;
  background: white;
  color: #374151;
  font-size: 0.875rem;
  font-weight: 500;
  text-align: center;
  transition: all 0.2s ease;
}

.pagination-input:hover {
  border-color: rgba(76, 175, 80, 0.4);
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
}

.pagination-input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.15);
}

.pagination-jump-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  padding: 0;
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
  border: none;
  border-radius: 10px;
  color: white;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.pagination-jump-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.25), transparent);
  transition: left 0.4s ease;
}

.pagination-jump-btn:hover::before {
  left: 100%;
}

.pagination-jump-btn:hover {
  background: linear-gradient(135deg, #43A047 0%, #5CB85C 100%);
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.pagination-jump-btn:active {
  transform: translateY(-1px) scale(1.02);
  box-shadow: 0 3px 10px rgba(76, 175, 80, 0.3);
}

/* Responsive para paginación */
@media (max-width: 768px) {
  .pagination-container {
    gap: 1rem;
    margin-top: 1.5rem;
    padding: 1rem;
  }
  
  .pagination-info {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
    gap: 0.75rem;
  }
  
  .pagination-selector {
    justify-content: center;
  }
  
  .pagination-nav {
    gap: 0.15rem;
  }
  
  .pagination-btn {
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
    min-height: 40px;
  }
  
  .pagination-btn-text {
    display: none;
  }
  
  .pagination-first,
  .pagination-last {
    padding: 0.5rem;
  }
  
  .pagination-number {
    width: 40px;
    height: 40px;
    font-size: 0.8rem;
  }
  
  .pagination-ellipsis {
    width: 30px;
    height: 40px;
    font-size: 1rem;
  }
  
  .pagination-jump {
    margin-top: 0.5rem;
  }
  
  .pagination-input {
    width: 70px;
    padding: 0.4rem 0.6rem;
    font-size: 0.8rem;
  }
  
  .pagination-jump-btn {
    width: 36px;
    height: 36px;
  }
}

@media (max-width: 480px) {
  .pagination-container {
    padding: 0.75rem;
    gap: 0.75rem;
  }
  
  .pagination-nav {
    gap: 0.1rem;
  }
  
  .pagination-btn {
    padding: 0.4rem 0.6rem;
    font-size: 0.75rem;
    min-height: 36px;
  }
  
  .pagination-first,
  .pagination-last {
    padding: 0.4rem;
  }
  
  .pagination-number {
    width: 36px;
    height: 36px;
    font-size: 0.75rem;
    border-radius: 8px;
  }
  
  .pagination-ellipsis {
    width: 24px;
    height: 36px;
    font-size: 0.9rem;
  }
  
  .pagination-numbers {
    margin: 0 0.25rem;
  }
  
  .pagination-text {
    font-size: 0.8rem;
  }
  
  .pagination-label {
    font-size: 0.8rem;
  }
  
  .pagination-select {
    padding: 0.4rem 0.6rem;
    font-size: 0.8rem;
    min-width: 60px;
  }
}

/* === ESTILOS PARA CONTADORES COMPACTOS === */
/* Estilos para contadores compactos del visor - MÁS PEQUEÑOS */
.visor-stats-compact {
  display: flex;
  gap: clamp(0.5rem, 1.5vw, 1rem);
  padding: 0;
  background: transparent;
  justify-content: center;
  flex-wrap: wrap;
  margin: 0;
  animation: fadeInUp 0.6s ease-out 0.2s both;
}

.compact-stat-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: clamp(0.4rem, 1vw, 0.6rem);
  padding: clamp(0.5rem, 1.2vw, 0.8rem) clamp(0.8rem, 2vw, 1.2rem);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.9) 100%);
  border: 1px solid rgba(76, 175, 80, 0.15);
  border-radius: clamp(8px, 2vw, 12px);
  box-shadow: 
    0 2px 12px rgba(76, 175, 80, 0.08),
    0 1px 4px rgba(0, 0, 0, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  overflow: hidden;
  backdrop-filter: blur(8px);
  cursor: default;
  min-width: clamp(120px, 15vw, 150px);
  font-size: clamp(0.75rem, 1.4vw, 0.85rem);
}

.compact-stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(76, 175, 80, 0.08), transparent);
  transition: left 0.8s ease;
}

.compact-stat-card:hover::before {
  left: 100%;
}

.compact-stat-card:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 
    0 4px 20px rgba(76, 175, 80, 0.15),
    0 2px 8px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
  border-color: rgba(76, 175, 80, 0.25);
  background: linear-gradient(135deg, rgba(255, 255, 255, 1) 0%, rgba(240, 255, 240, 0.95) 100%);
}

.compact-stat-icon {
  position: relative;
  width: clamp(28px, 3.5vw, 32px);
  height: clamp(28px, 3.5vw, 32px);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.8) 100%);
  border: 2px solid rgba(76, 175, 80, 0.2);
  border-radius: clamp(6px, 1.5vw, 8px);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.1);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  overflow: hidden;
}

.compact-stat-icon::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, rgba(255, 255, 255, 0.3) 0%, transparent 50%, rgba(255, 255, 255, 0.1) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.compact-stat-card:hover .compact-stat-icon {
  transform: rotate(-3deg) scale(1.08);
  box-shadow: 0 3px 12px rgba(76, 175, 80, 0.2);
  background: linear-gradient(135deg, rgba(255, 255, 255, 1) 0%, rgba(240, 255, 240, 0.9) 100%);
  border-color: rgba(76, 175, 80, 0.4);
}

.compact-stat-card:hover .compact-stat-icon::before {
  opacity: 1;
}

.compact-stat-icon svg {
  width: clamp(14px, 2.2vw, 16px);
  height: clamp(14px, 2.2vw, 16px);
  transition: all 0.3s ease;
  filter: drop-shadow(0 1px 2px rgba(76, 175, 80, 0.3));
}

.compact-stat-card:hover .compact-stat-icon svg {
  transform: scale(1.1);
  filter: drop-shadow(0 2px 4px rgba(76, 175, 80, 0.4));
}

.compact-stat-info {
  display: flex;
  flex-direction: column;
  gap: clamp(0.1rem, 0.3vw, 0.15rem);
  flex: 1;
  min-width: 0;
}

.compact-stat-value {
  font-size: clamp(0.95rem, 2.2vw, 1.15rem);
  font-weight: 700;
  color: #2c3e50;
  line-height: 1;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: linear-gradient(135deg, #2c3e50 0%, #4CAF50 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  transition: all 0.3s ease;
}

.compact-stat-card:hover .compact-stat-value {
  transform: scale(1.03);
  background: linear-gradient(135deg, #4CAF50 0%, #43A047 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.compact-stat-label {
  font-size: clamp(0.55rem, 1.1vw, 0.65rem);
  font-weight: 500;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  line-height: 1.1;
  transition: all 0.3s ease;
}

.compact-stat-card:hover .compact-stat-label {
  color: #4CAF50;
  transform: translateX(1px);
}

/* Responsive para contadores compactos - NUEVA ESTRUCTURA */
@media (max-width: 768px) {
  .filters-main {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filters-left {
    width: 100%;
  }
  
  .filters-right {
    margin-left: 0;
    margin-top: clamp(0.5rem, 1vw, 0.75rem);
    justify-content: center;
  }
  
  .visor-stats-compact {
    gap: 0.75rem;
    padding: 0;
    margin: 0;
    justify-content: center;
  }
  
  .compact-stat-card {
    min-width: 110px;
    padding: 0.6rem 0.8rem;
    gap: 0.5rem;
  }
  
  .compact-stat-icon {
    width: 28px;
    height: 28px;
  }
  
  .compact-stat-icon svg {
    width: 14px;
    height: 14px;
  }
  
  .compact-stat-value {
    font-size: 1rem;
  }
  
  .compact-stat-label {
    font-size: 0.58rem;
  }
}

@media (max-width: 480px) {
  .filters-right .visor-stats-compact {
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
  }
  
  .compact-stat-card {
    min-width: 100%;
    max-width: 220px;
    margin: 0 auto;
    padding: 0.6rem 0.8rem;
  }
  
  .visor-stats-compact {
    gap: 0.75rem;
    padding: 0.5rem 0.75rem;
    margin: 0;
  }
  
  .compact-stat-card {
    min-width: 110px;
    padding: 0.6rem 0.8rem;
    gap: 0.5rem;
    border-radius: 10px;
  }
  
  .compact-stat-icon {
    width: 26px;
    height: 26px;
    border-radius: 8px;
  }
  
  .compact-stat-icon svg {
    width: 13px;
    height: 13px;
  }
  
  .compact-stat-value {
    font-size: 0.95rem;
  }
  
  .compact-stat-label {
    font-size: 0.55rem;
    letter-spacing: 0.02em;
  }
}

/* Tablet landscape */
@media (max-width: 768px) and (orientation: landscape) {
  .main-content {
    margin-left: 160px;
    width: calc(100vw - 160px);
  }
}

@media (max-width: 480px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
}

@media (max-width: 375px) {
  .main-content {
    margin-left: 180px;
    width: calc(100vw - 180px);
  }
}

/* Animaciones adicionales */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========================================
   NOTIFICACIONES TOAST
   ======================================== */

.toast-notification {
  position: fixed;
  top: 80px;
  right: 24px;
  z-index: 10000;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 24px;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12), 0 2px 8px rgba(0, 0, 0, 0.08);
  font-size: 14px;
  font-weight: 500;
  color: white;
  min-width: 300px;
  max-width: 420px;
  backdrop-filter: blur(10px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-notification.toast-success {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.toast-notification.toast-error {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.toast-notification.toast-info {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.toast-icon {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.toast-message {
  flex: 1;
  line-height: 1.5;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* Animación de entrada/salida del toast */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%) scale(0.8);
}

.toast-enter-to {
  opacity: 1;
  transform: translateX(0) scale(1);
}

.toast-leave-from {
  opacity: 1;
  transform: translateX(0) scale(1);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.8);
}

/* Responsive para toast en móviles */
@media (max-width: 768px) {
  .toast-notification {
    top: 70px;
    right: 12px;
    left: 12px;
    min-width: auto;
    max-width: none;
    padding: 14px 18px;
    font-size: 13px;
  }
  
  .toast-icon {
    width: 18px;
    height: 18px;
  }
}

@media (max-width: 480px) {
  .toast-notification {
    top: 60px;
    right: 8px;
    left: 8px;
    padding: 12px 16px;
    font-size: 12.5px;
    gap: 10px;
  }
}
</style>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
</style>
