<template>
  <div class="usuarios-container">
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
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="9" cy="7" r="4" stroke-width="2"/>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <span class="apple-title-divider">|</span>
                <h1 class="apple-page-title">USUARIOS</h1>
              </div>
              <p class="apple-page-subtitle">Administración de usuarios del sistema</p>
            </div>
            
            <button @click="cargarUsuarios" class="apple-refresh-button" :disabled="loading">
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
                <div class="apple-stat-value">{{ totalUsuarios }}</div>
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
                <div class="apple-stat-value">{{ contadorEstados.activos || 0 }}</div>
                <div class="apple-stat-label">Activos</div>
              </div>
            </div>

            <div class="apple-stat-card">
              <div class="apple-stat-icon purple">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="12" cy="12" r="10" stroke-width="2"/>
                  <line x1="4.93" y1="4.93" x2="19.07" y2="19.07" stroke-width="2"/>
                </svg>
              </div>
              <div class="apple-stat-content">
                <div class="apple-stat-value">{{ contadorEstados.inactivos || 0 }}</div>
                <div class="apple-stat-label">Inactivos</div>
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
                  @input="filtrarUsuarios"
                  type="text" 
                  placeholder="Buscar por nombre, correo, CURP..." 
                  class="apple-search-input"
                >
                <button v-if="searchTerm" @click="limpiarBusquedaUsuarios" class="apple-clear-btn">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10" stroke-width="2"/>
                    <line x1="15" y1="9" x2="9" y2="15" stroke-width="2" stroke-linecap="round"/>
                    <line x1="9" y1="9" x2="15" y2="15" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </button>
              </div>

              <div class="apple-filter-controls">
                <button 
                  @click="sincronizarSupervisores" 
                  class="apple-filter-btn sync"
                  :disabled="sincronizando"
                  title="Sincronizar supervisores"
                >
                  <svg :class="{ 'apple-spin': sincronizando }" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span>{{ sincronizando ? 'Sincronizando...' : 'Sincronizar' }}</span>
                </button>
                <button 
                  @click="exportarExcel" 
                  class="apple-filter-btn export"
                  title="Exportar a Excel"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span>Excel</span>
                </button>
                <button 
                  @click="imprimirUsuarios" 
                  class="apple-filter-btn print"
                  title="Imprimir"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <polyline points="6 9 6 2 18 2 18 9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <rect x="6" y="14" width="12" height="8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span>Imprimir</span>
                </button>
              </div>
            </div>

            <!-- Unified Filter Row - Estado + Cargo + Ordenamiento -->
            <div class="apple-unified-filters">
              <div class="apple-quick-filters">
                <button 
                  @click="filtroEstado = 'todos'; filtrarUsuarios()" 
                  :class="['apple-filter-chip', { 'active': filtroEstado === 'todos' }]"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke-width="2"/>
                    <circle cx="9" cy="7" r="4" stroke-width="2"/>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87" stroke-width="2"/>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75" stroke-width="2"/>
                  </svg>
                  <span>Todos</span>
                </button>
                <button 
                  @click="filtroEstado = 'activos'; filtrarUsuarios()" 
                  :class="['apple-filter-chip', { 'active': filtroEstado === 'activos' }]"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" stroke-width="2"/>
                    <polyline points="22 4 12 14.01 9 11.01" stroke-width="2"/>
                  </svg>
                  <span>Activos</span>
                </button>
                <button 
                  @click="filtroEstado = 'inactivos'; filtrarUsuarios()" 
                  :class="['apple-filter-chip', { 'active': filtroEstado === 'inactivos' }]"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10" stroke-width="2"/>
                    <line x1="4.93" y1="4.93" x2="19.07" y2="19.07" stroke-width="2"/>
                  </svg>
                  <span>Inactivos</span>
                </button>
              </div>

              <div class="apple-filter-group">
                <label class="apple-filter-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <rect x="2" y="3" width="20" height="14" rx="2" ry="2" stroke-width="2"/>
                    <line x1="8" y1="21" x2="16" y2="21" stroke-width="2"/>
                    <line x1="12" y1="17" x2="12" y2="21" stroke-width="2"/>
                  </svg>
                  Cargo:
                </label>
                <select v-model="filtroCargo" @change="filtrarUsuarios" class="apple-select">
                  <option value="todos">Todos los cargos</option>
                  <option v-for="cargo in cargosDisponibles.filter(c => c !== 'OTRO')" :key="cargo" :value="cargo">
                    {{ cargo }}
                  </option>
                  <option value="OTRO">OTRO</option>
                  <option value="sin-cargo">Sin cargo</option>
                </select>
                <div :class="['apple-count-badge', `cargo-${obtenerColorCargo(filtroCargo === 'todos' ? '' : filtroCargo)}`]">
                  {{ contadorPorCargo[filtroCargo] || 0 }}
                </div>
              </div>

              <div class="apple-sort-group">
                <span class="apple-sort-label">Ordenar:</span>
                <div class="apple-sort-buttons">
                  <button 
                    @click="ordenarPor('id')"
                    :class="['apple-sort-btn', { active: campoOrdenamiento === 'id' }]"
                    title="Ordenar por ID"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M4 9h16M4 15h16M10 3L8 21M16 3l-2 18" stroke-width="2"/>
                    </svg>
                    ID
                    <svg v-if="campoOrdenamiento === 'id'" class="sort-direction" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path v-if="direccionOrdenamiento === 'asc'" d="m7 15 5 5 5-5" stroke-width="2"/>
                      <path v-else d="m7 9 5-5 5 5" stroke-width="2"/>
                    </svg>
                  </button>
                  <button 
                    @click="ordenarPor('nombre')"
                    :class="['apple-sort-btn', { active: campoOrdenamiento === 'nombre' }]"
                    title="Ordenar por Nombre"
                  >
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke-width="2"/>
                      <circle cx="12" cy="7" r="4" stroke-width="2"/>
                    </svg>
                    Nombre
                    <svg v-if="campoOrdenamiento === 'nombre'" class="sort-direction" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path v-if="direccionOrdenamiento === 'asc'" d="m7 15 5 5 5-5" stroke-width="2"/>
                      <path v-else d="m7 9 5-5 5 5" stroke-width="2"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ================== CONTENT WRAPPER ================== -->
      <div class="apple-content-wrapper">
        <!-- ================== TABLE APPLE STYLE ================== -->
        <div class="apple-table-container">
          <div v-if="loading && usuarios.length === 0" class="apple-loading">
            <div class="apple-spinner"></div>
            <p>Cargando usuarios...</p>
          </div>

          <div v-else-if="error" class="apple-error">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="10" stroke-width="2"/>
              <line x1="12" y1="8" x2="12" y2="12" stroke-width="2" stroke-linecap="round"/>
              <line x1="12" y1="16" x2="12.01" y2="16" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <p>{{ error }}</p>
            <button @click="cargarUsuarios" class="apple-retry-btn">Reintentar</button>
          </div>

          <div v-else-if="usuariosFiltrados.length === 0" class="apple-empty">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke-width="2"/>
              <circle cx="12" cy="7" r="4" stroke-width="2"/>
            </svg>
            <h3>No hay usuarios</h3>
            <p v-if="searchTerm">No se encontraron usuarios con el término "{{ searchTerm }}"</p>
            <p v-else>Aún no se han registrado usuarios en la aplicación.</p>
          </div>

          <div v-else class="apple-table-wrapper">
            <table class="apple-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Usuario</th>
                  <th>Correo</th>
                  <th>Cargo</th>
                  <th>Supervisor</th>
                  <th>CURP</th>
                  <th>Territorio</th>
                  <th>Estado</th>
                  <th v-if="puedeVerAcciones">Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="usuario in usuariosPaginados" :key="usuario.id" class="apple-table-row" :class="{ 'apple-row-inactive': usuario.activo === false }">
                  <td>
                    <span class="apple-id-badge">#{{ usuario.id }}</span>
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
                        <div class="apple-user-name">{{ usuario.nombre_completo || 'Sin nombre' }}</div>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span class="apple-email">{{ usuario.correo }}</span>
                  </td>
                  <td>
                    <span v-if="usuario.cargo" :class="['apple-cargo-badge', `cargo-${obtenerColorCargo(usuario.cargo)}`]">
                      {{ usuario.cargo }}
                    </span>
                    <span v-else class="apple-cargo-badge cargo-empty">Sin cargo</span>
                  </td>
                  <td>
                    <span class="apple-supervisor">{{ usuario.supervisor || '—' }}</span>
                  </td>
                  <td>
                    <span class="apple-curp">{{ (usuario.curp || 'N/A').toUpperCase() }}</span>
                  </td>
                  <td>
                    <span v-if="usuario.territorio" :class="['apple-territorio-badge', `territorio-${obtenerColorTerritorio(usuario.territorio)}`]">
                      {{ usuario.territorio }}
                    </span>
                    <span v-else class="apple-no-data">Sin asignar</span>
                  </td>
                  <td>
                    <span :class="['apple-status-badge', usuario.activo === false ? 'inactivo' : 'activo']">
                      {{ usuario.activo === false ? 'Inactivo' : 'Activo' }}
                    </span>
                  </td>
                  <td v-if="puedeVerAcciones">
                    <div class="apple-actions">
                      <button @click="verDetalles(usuario)" class="apple-action-btn view" title="Ver detalles">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke-width="2"/>
                          <circle cx="12" cy="12" r="3" stroke-width="2"/>
                        </svg>
                      </button>
                      <button 
                        @click="usuario.activo !== false && editarUsuario(usuario)" 
                        :class="['apple-action-btn edit', { disabled: usuario.activo === false }]"
                        :title="usuario.activo === false ? 'Usuario inactivo' : 'Editar'"
                        :disabled="usuario.activo === false"
                      >
                        <svg v-if="usuario.activo === false" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke-width="2"/>
                          <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke-width="2"/>
                        </svg>
                        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke-width="2"/>
                          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" stroke-width="2"/>
                        </svg>
                      </button>
                      <button 
                        v-if="puedeActivarDesactivar"
                        @click="toggleEstadoUsuario(usuario)" 
                        :class="['apple-action-btn', usuario.activo === false ? 'activate' : 'deactivate']"
                        :title="usuario.activo === false ? 'Activar' : 'Desactivar'"
                      >
                        <svg v-if="usuario.activo === false" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" stroke-width="2"/>
                          <polyline points="22 4 12 14.01 9 11.01" stroke-width="2"/>
                        </svg>
                        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <circle cx="12" cy="12" r="10" stroke-width="2"/>
                          <line x1="4.93" y1="4.93" x2="19.07" y2="19.07" stroke-width="2"/>
                        </svg>
                      </button>
                      <button 
                        @click="usuario.activo !== false && confirmarEliminarUsuario(usuario)" 
                        :class="['apple-action-btn delete', { disabled: usuario.activo === false }]"
                        :title="usuario.activo === false ? 'Usuario inactivo' : 'Eliminar'"
                        :disabled="usuario.activo === false"
                      >
                        <svg v-if="usuario.activo === false" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke-width="2"/>
                          <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke-width="2"/>
                        </svg>
                        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <polyline points="3,6 5,6 21,6" stroke-width="2"/>
                          <path d="m19,6v14a2,2 0 0,1 -2,2H7a2,2 0 0,1 -2,-2V6m3,0V4a2,2 0 0,1 2,-2h4a2,2 0 0,1 2,2v2" stroke-width="2"/>
                          <line x1="10" y1="11" x2="10" y2="17" stroke-width="2"/>
                          <line x1="14" y1="11" x2="14" y2="17" stroke-width="2"/>
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
          </div>
        </div>
      </div>
    </main>

    <!-- Modal para detalles - Diseño Moderno Responsivo -->
    <div v-if="showModal" class="modal-overlay-modern" @click="cerrarModal">
      <div class="modal-content-modern" @click.stop>
        <div class="modal-header-modern">
          <div class="modal-title-section">
            <div class="modal-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            </div>
            <h3 class="modal-title">{{ modalTitle }}</h3>
          </div>
          <button @click="cerrarModal" class="btn-close-modern">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        
        <div class="modal-body-modern">
          <div v-if="usuarioSeleccionado" class="user-details-grid">
            <!-- ID Usuario -->
            <div class="detail-card">
              <div class="detail-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                  <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
                </svg>
              </div>
              <div class="detail-content">
                <span class="detail-label">ID Usuario</span>
                <span class="detail-value">#{{ usuarioSeleccionado.id }}</span>
              </div>
            </div>

            <!-- Correo Electrónico -->
            <div class="detail-card">
              <div class="detail-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                  <polyline points="22,6 12,13 2,6"/>
                </svg>
              </div>
              <div class="detail-content">
                <span class="detail-label">Correo</span>
                <span class="detail-value">{{ usuarioSeleccionado.correo }}</span>
              </div>
            </div>

            <!-- Nombre Completo -->
            <div class="detail-card">
              <div class="detail-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </div>
              <div class="detail-content">
                <span class="detail-label">Nombre</span>
                <span class="detail-value">{{ usuarioSeleccionado.nombre_completo || 'No especificado' }}</span>
              </div>
            </div>

            <!-- Cargo -->
            <div class="detail-card">
              <div class="detail-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
                  <line x1="8" y1="21" x2="16" y2="21"/>
                  <line x1="12" y1="17" x2="12" y2="21"/>
                </svg>
              </div>
              <div class="detail-content">
                <span class="detail-label">Cargo</span>
                <span v-if="usuarioSeleccionado.cargo" :class="['cargo-badge', 'cargo-badge-detail', `cargo-${obtenerColorCargo(usuarioSeleccionado.cargo)}`]">
                  {{ usuarioSeleccionado.cargo }}
                </span>
                <span v-else class="detail-value">No especificado</span>
              </div>
            </div>

            <!-- Supervisor -->
            <div class="detail-card">
              <div class="detail-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                </svg>
              </div>
              <div class="detail-content">
                <span class="detail-label">Supervisor</span>
                <span class="detail-value">{{ usuarioSeleccionado.supervisor || 'No asignado' }}</span>
              </div>
            </div>

            <!-- CURP -->
            <div class="detail-card">
              <div class="detail-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14,2 14,8 20,8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                  <polyline points="10,9 9,9 8,9"/>
                </svg>
              </div>
              <div class="detail-content">
                <span class="detail-label">CURP</span>
                <span class="detail-value">{{ usuarioSeleccionado.curp || 'No especificada' }}</span>
              </div>
            </div>

            <!-- Teléfono -->
            <div class="detail-card">
              <div class="detail-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
                </svg>
              </div>
              <div class="detail-content">
                <span class="detail-label">Teléfono</span>
                <span class="detail-value phone-value">{{ usuarioSeleccionado.telefono || 'No especificado' }}</span>
              </div>
            </div>

            <!-- Territorio -->
            <div class="detail-card">
              <div class="detail-icon territorio-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
              </div>
              <div class="detail-content">
                <span class="detail-label">Territorio</span>
                <span :class="usuarioSeleccionado.territorio ? 'detail-value territorio-value' : 'detail-value territorio-empty-detail'">{{ usuarioSeleccionado.territorio || 'Sin asignar' }}</span>
              </div>
            </div>

            <!-- Estado -->
            <div class="detail-card">
              <div class="detail-icon status-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22,4 12,14.01 9,11.01"/>
                </svg>
              </div>
              <div class="detail-content">
                <span class="detail-label">Estado</span>
                <span class="detail-value status-active">● Activo</span>
              </div>
            </div>

            <!-- Contraseña -->
            <div class="detail-card password-card">
              <div class="detail-icon">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                  <circle cx="12" cy="16" r="1"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
              </div>
              <div class="detail-content password-content">
                <span class="detail-label">Contraseña</span>
                <div class="password-display">
                  <span class="password-value">
                    {{ showPassword ? obtenerContrasenaUsuario(usuarioSeleccionado) : '••••••••••••' }}
                  </span>
                  <button @click="togglePassword" class="password-toggle-btn" type="button">
                    <svg v-if="showPassword" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                      <line x1="1" y1="1" x2="23" y2="23"/>
                    </svg>
                    <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                      <circle cx="12" cy="12" r="3"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de confirmación para eliminar usuario -->
    <div v-if="showDeleteModal" class="modal-overlay-modern" @click="cancelarEliminar">
      <div class="modal-content-modern delete-modal" @click.stop>
        <div class="modal-header-modern delete-header">
          <div class="modal-title-section">
            <div class="modal-icon delete-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 6h18"></path>
                <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                <path d="M8 6V4c0-1 1-2 2-2h4c0-1 1-2 2-2v2"></path>
                <line x1="10" y1="11" x2="10" y2="17"></line>
                <line x1="14" y1="11" x2="14" y2="17"></line>
              </svg>
            </div>
            <h3 class="modal-title">Confirmar Eliminación</h3>
          </div>
          <button @click="cancelarEliminar" class="btn-close-modern">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        
        <div class="modal-body-modern">
          <div v-if="usuarioAEliminar" class="delete-confirmation">
            <div class="warning-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#f44336" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
              </svg>
            </div>
            <h4>¿Estás seguro de que deseas eliminar este usuario?</h4>
            <div class="user-info-delete">
              <p><strong>ID:</strong> #{{ usuarioAEliminar.id }}</p>
              <p><strong>Nombre:</strong> {{ usuarioAEliminar.nombre_completo }}</p>
              <p><strong>Correo:</strong> {{ usuarioAEliminar.correo }}</p>
              <p><strong>Teléfono:</strong> {{ usuarioAEliminar.telefono || 'No especificado' }}</p>
            </div>
            <p class="warning-text">Esta acción eliminará permanentemente al usuario y todos sus datos asociados. <strong>Esta acción no se puede deshacer.</strong></p>
          </div>
        </div>
        
        <div class="modal-footer-delete">
          <button @click="cancelarEliminar" class="btn-cancel">
            Cancelar
          </button>
          <button @click="eliminarUsuario" class="btn-delete" :disabled="eliminandoUsuario">
            <svg v-if="eliminandoUsuario" class="spinner-small" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 12a9 9 0 11-6.219-8.56"/>
            </svg>
            {{ eliminandoUsuario ? 'Eliminando...' : 'Eliminar Usuario' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de Cambio de Estado (Activar/Desactivar) -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showEstadoModal" class="estado-overlay" @click="cancelarCambioEstado">
          <Transition name="pop">
            <div v-if="showEstadoModal" class="estado-box" @click.stop>
              <!-- Icono superior -->
              <div class="estado-icon-circle" :class="usuarioACambiarEstado?.activo === false ? 'icon-green' : 'icon-orange'">
                <svg v-if="usuarioACambiarEstado?.activo === false" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
                <svg v-else width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
                </svg>
              </div>

              <!-- Título -->
              <h3 class="estado-titulo">
                {{ usuarioACambiarEstado?.activo === false ? 'Activar Cuenta' : 'Desactivar Cuenta' }}
              </h3>

              <!-- Info usuario -->
              <div class="estado-user-card" v-if="usuarioACambiarEstado">
                <p class="estado-user-name">{{ usuarioACambiarEstado.nombre_completo || 'Sin nombre' }}</p>
                <p class="estado-user-email">{{ usuarioACambiarEstado.correo }}</p>
                <span :class="['estado-badge', usuarioACambiarEstado.activo === false ? 'badge-inactive' : 'badge-active']">
                  {{ usuarioACambiarEstado.activo === false ? 'Inactivo' : 'Activo' }}
                </span>
              </div>

              <!-- Mensaje -->
              <p class="estado-msg" :class="usuarioACambiarEstado?.activo === false ? 'msg-green' : 'msg-orange'">
                {{ usuarioACambiarEstado?.activo === false 
                  ? 'El usuario podrá iniciar sesión nuevamente.' 
                  : 'El usuario no podrá iniciar sesión.' 
                }}
              </p>

              <!-- Botones -->
              <div class="estado-actions">
                <button @click="cancelarCambioEstado" class="estado-btn-cancel">Cancelar</button>
                <button 
                  @click="confirmarCambioEstado" 
                  :class="['estado-btn-confirm', usuarioACambiarEstado?.activo === false ? 'btn-green' : 'btn-orange']"
                  :disabled="cambiandoEstado"
                >
                  <svg v-if="cambiandoEstado" class="spinner-small" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 12a9 9 0 11-6.219-8.56"/></svg>
                  {{ cambiandoEstado 
                    ? (usuarioACambiarEstado?.activo === false ? 'Activando...' : 'Desactivando...') 
                    : (usuarioACambiarEstado?.activo === false ? 'Sí, activar' : 'Sí, desactivar') 
                  }}
                </button>
              </div>
            </div>
          </Transition>
        </div>
      </Transition>
    </Teleport>

    <!-- Modal de edición de usuario - REDISEÑO COMPLETO -->
    <Teleport to="body">
      <div v-if="showEditModal" class="edit-modal-overlay" @click.self="cancelarEdicion">
        <div class="edit-modal-container">
          <!-- Header del modal -->
          <div class="edit-modal-header">
            <div class="edit-modal-title-wrapper">
              <div class="edit-modal-icon">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
            </div>
            <div class="edit-modal-title-text">
              <h3>Editar Usuario</h3>
              <span class="edit-modal-subtitle">ID: #{{ usuarioAEditar?.id }}</span>
            </div>
          </div>
          <button @click="cancelarEdicion" class="edit-modal-close">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        
        <!-- Body del modal -->
        <div class="edit-modal-body">
          <div v-if="usuarioAEditar" class="edit-form-container">
            <!-- Fila 1: Correo y Nombre -->
            <div class="edit-form-row">
              <div class="edit-form-field">
                <label for="edit-correo">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                  Correo Electrónico
                </label>
                <input 
                  id="edit-correo"
                  v-model="datosEdicion.correo" 
                  type="email" 
                  placeholder="correo@ejemplo.com"
                />
              </div>
              <div class="edit-form-field">
                <label for="edit-nombre">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                  Nombre Completo
                </label>
                <input 
                  id="edit-nombre"
                  v-model="datosEdicion.nombre_completo" 
                  type="text" 
                  placeholder="Nombre completo"
                  style="text-transform: uppercase;"
                  @input="datosEdicion.nombre_completo = normalizarTexto($event.target.value)"
                />
              </div>
            </div>

            <!-- Fila 2: Cargo y Supervisor -->
            <div class="edit-form-row">
              <div class="edit-form-field">
                <label for="edit-cargo">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
                  Cargo
                </label>
                <select 
                  id="edit-cargo"
                  v-model="datosEdicion.cargo"
                  style="cursor: pointer;"
                >
                  <option value="">-- Selecciona un cargo --</option>
                  <option v-for="cargo in cargosDisponibles" :key="cargo" :value="cargo">{{ cargo }}</option>
                </select>
              </div>
              <div class="edit-form-field">
                <label for="edit-supervisor">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                  Supervisor
                </label>
                <input 
                  id="edit-supervisor"
                  v-model="datosEdicion.supervisor" 
                  type="text" 
                  :placeholder="esTecnicoEdicion && buscandoSupervisor ? 'Buscando supervisor...' : 'Nombre del supervisor'"
                  :readonly="esTecnicoEdicion"
                  :style="esTecnicoEdicion ? 'background-color: #e5e7eb; cursor: not-allowed; color: #1f2937;' : 'text-transform: uppercase;'"
                  @input="!esTecnicoEdicion && (datosEdicion.supervisor = normalizarTexto($event.target.value))"
                />
                <p v-if="esTecnicoEdicion" style="margin-top: 0.25rem; font-size: 0.75rem; color: #10b981;">
                  ✅ Supervisor asignado automáticamente según territorio
                </p>
              </div>
            </div>

            <!-- Campo para especificar cargo OTRO -->
            <div v-if="datosEdicion.cargo === 'OTRO'" class="edit-form-row">
              <div class="edit-form-field" style="grid-column: 1 / -1;">
                <label for="edit-cargo-otro">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                  </svg>
                  Especifica el cargo
                </label>
                <input 
                  id="edit-cargo-otro"
                  v-model="datosEdicion.cargoOtro" 
                  type="text" 
                  placeholder="Escribe el cargo personalizado"
                  style="text-transform: uppercase;"
                />
                <p style="margin-top: 0.25rem; font-size: 0.75rem; color: #6b7280;">
                  Escribe el nombre del cargo sin tildes
                </p>
              </div>
            </div>

            <!-- Fila 3: Contraseña y CURP -->
            <div class="edit-form-row">
              <div class="edit-form-field">
                <label for="edit-contrasena">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                  Contraseña
                </label>
                <div class="edit-password-wrapper">
                  <input 
                    id="edit-contrasena"
                    v-model="datosEdicion.contrasena" 
                    :type="showEditPassword ? 'text' : 'password'"
                    placeholder="Nueva contraseña (opcional)"
                  />
                  <button @click="showEditPassword = !showEditPassword" type="button" class="edit-password-toggle">
                    <svg v-if="showEditPassword" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                      <line x1="1" y1="1" x2="23" y2="23"/>
                    </svg>
                    <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                      <circle cx="12" cy="12" r="3"/>
                    </svg>
                  </button>
                </div>
              </div>
              <div class="edit-form-field">
                <label for="edit-curp">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                  CURP
                </label>
                <input 
                  id="edit-curp"
                  v-model="datosEdicion.curp" 
                  type="text" 
                  placeholder="CURP de 18 caracteres"
                  maxlength="18"
                  style="text-transform: uppercase;"
                  @input="datosEdicion.curp = normalizarTexto($event.target.value)"
                />
              </div>
            </div>

            <!-- Fila 4: Teléfono y Territorio -->
            <div class="edit-form-row">
              <div class="edit-form-field">
                <label for="edit-telefono">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                  Teléfono
                </label>
                <input 
                  id="edit-telefono"
                  v-model="datosEdicion.telefono" 
                  type="tel" 
                  placeholder="+52 000 000 0000"
                />
              </div>
              <div class="edit-form-field">
                <label for="edit-territorio">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                  Territorio
                </label>
                <select id="edit-territorio" v-model="datosEdicion.territorio">
                  <option value="">-- Sin asignar --</option>
                  <option v-for="territorio in territoriosSembrandoVida" :key="territorio" :value="territorio">{{ territorio }}</option>
                </select>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Footer del modal -->
        <div class="edit-modal-footer">
          <button @click="cancelarEdicion" class="edit-btn-cancel">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            Cancelar
          </button>
          <button @click="guardarEdicion" class="edit-btn-save" :disabled="editandoUsuario">
            <svg v-if="editandoUsuario" class="spinner-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12a9 9 0 11-6.219-8.56"/>
            </svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
            {{ editandoUsuario ? 'Guardando...' : 'Guardar Cambios' }}
          </button>
        </div>
      </div>
    </div>
    </Teleport>
    
    <!-- Modal de Éxito (movido dentro del contenedor principal) -->
    <Teleport to="body">
      <div v-if="showSuccessModal" class="modal-overlay-success" @click.self="cerrarSuccessModal">
        <div class="modal-content-success">
          <div class="success-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20,6 9,17 4,12"></polyline>
            </svg>
          </div>
          
          <h3>¡Usuario actualizado!</h3>
          <p>Los cambios se guardaron exitosamente en la base de datos.</p>
          
          <button @click="cerrarSuccessModal" class="btn-success-ok">
            Aceptar
          </button>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Sidebar from '../components/Sidebar.vue'
import { usuariosService } from '../services/usuariosService.js'
import authService from '../services/authService.js'

const router = useRouter()

// Variable reactiva para permisos del usuario actual (se actualiza en tiempo real)
const userPermisos = ref(authService.getCurrentUser()?.permisos || {})
const userRol = ref(authService.getCurrentUser()?.rol || '')

// Permiso para ver acciones (editar/eliminar) - REACTIVO
const puedeVerAcciones = computed(() => {
  // Admin siempre puede ver acciones
  if (userRol.value === 'admin' || authService.isAdmin()) {
    return true
  }
  // Verificar permiso específico usando la variable reactiva
  return userPermisos.value?.usuarios_acciones === true
})

// Permiso para activar/desactivar usuarios - REACTIVO
const puedeActivarDesactivar = computed(() => {
  // Admin siempre puede activar/desactivar
  if (userRol.value === 'admin' || authService.isAdmin()) {
    return true
  }
  // Verificar permiso específico usando la variable reactiva
  return userPermisos.value?.usuarios_estado === true
})

// Función para actualizar permisos cuando el evento es disparado
const actualizarPermisosUsuario = (event) => {
  const userData = event.detail
  console.log('🔄 UsuariosView: Permisos actualizados en tiempo real', userData.permisos)
  userPermisos.value = userData.permisos || {}
  userRol.value = userData.rol || ''
}

// Estado de conexión
const isOnline = ref(navigator.onLine)

// Lista de territorios de Sembrando Vida para el selector de territorio
const territoriosSembrandoVida = [
  "Acapulco - Centro - Norte - Tierra Caliente",
  "Acayucan",
  "Balancán",
  "Chihuahua / Sonora",
  "Colima",
  "Comalcalco",
  "Córdoba",
  "Costa Chica - Montaña",
  "Costa Grande - Sierra",
  "Durango / Zacatecas",
  "Hidalgo",
  "Istmo",
  "Michoacán",
  "Mixteca",
  "Morelos",
  "Nayarit / Jalisco",
  "Ocosingo",
  "Palenque",
  "Papantla",
  "Pichucalco",
  "Puebla",
  "San Luis Potosí",
  "Sinaloa",
  "Tamaulipas",
  "Tantoyuca",
  "Tapachula",
  "Teapa",
  "Tlaxcala / Estado de México",
  "Tzucacab / Opb",
  "Xpujil",
  "Oficinas Centrales"
]

// Lista de cargos disponibles (sin tildes)
const cargosDisponibles = [
  'TECNICO PRODUCTIVO',
  'TECNICO SOCIAL',
  'FACILITADOR COMUNITARIO',
  'COORDINACION TERRITORIAL C',
  'COORDINACION TERRITORIAL B',
  'COORDINACION TERRITORIAL A',
  'ESPECIALISTAS PRODUCTIVOS Y SOCIALES',
  'SEMBRADOR',
  'OTRO'
]

const API_URL = 'https://apipwa.sembrandodatos.com'
const usuarios = ref([])
const usuariosFiltrados = ref([])
const loading = ref(false)
const error = ref('')
const searchTerm = ref('')
const filtroEstado = ref('todos') // 'todos', 'activos', 'inactivos'
const filtroCargo = ref('todos') // 'todos' o nombre del cargo
const supervisoresPorTerritorio = ref({}) // Mapa de territorio -> supervisor

// Variable para contador de usuarios
const totalUsuarios = ref('-')

// Variables para paginación
const paginaActual = ref(1)
const usuariosPorPagina = ref(50)
const paginaSalto = ref('')
const recargaCompleta = ref(false) // Control para saber si es recarga completa

// Variables para ordenamiento
const campoOrdenamiento = ref('fecha') // Por defecto ordenar por fecha
const direccionOrdenamiento = ref('desc') // Por defecto más reciente primero

const showModal = ref(false)
const modalTitle = ref('')
const modalContent = ref('')
const usuarioSeleccionado = ref(null)
const showPassword = ref(false)
const showEditPassword = ref(false) // Nueva variable para el modal de edición

// Variables para eliminación de usuarios
const showDeleteModal = ref(false)
const usuarioAEliminar = ref(null)
const eliminandoUsuario = ref(false)

// Variables para cambio de estado (activar/desactivar)
const showEstadoModal = ref(false)
const usuarioACambiarEstado = ref(null)
const cambiandoEstado = ref(false)

// Variables para edición de usuarios
const showEditModal = ref(false)
const usuarioAEditar = ref(null)
const editandoUsuario = ref(false)
const inicializandoModalEdicion = ref(false) // Para evitar que watchers limpien campos al abrir modal
const datosEdicion = ref({
  correo: '',
  nombre_completo: '',
  cargo: '',
  cargoOtro: '', // Campo para cargo personalizado cuando se selecciona OTRO
  supervisor: '',
  contrasena: '',
  curp: '',
  telefono: '',
  territorio: ''
})

// Variables para modal de éxito
const showSuccessModal = ref(false)

// Variable para sincronización de supervisores
const sincronizando = ref(false)

// Función para normalizar texto: mayúsculas sin tildes
const normalizarTexto = (texto) => {
  if (!texto) return ''
  return texto
    .toUpperCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // Eliminar tildes
}

// Variables para supervisor automático de técnicos
const buscandoSupervisor = ref(false)

// Función para obtener color del cargo
const obtenerColorCargo = (cargo) => {
  if (!cargo) return 'gray'
  
  const cargoUpper = cargo.toUpperCase()
  
  const coloresCargo = {
    'TECNICO PRODUCTIVO': 'emerald',
    'TECNICO SOCIAL': 'blue',
    'FACILITADOR COMUNITARIO': 'violet',
    'COORDINACION TERRITORIAL C': 'orange-light',
    'COORDINACION TERRITORIAL B': 'orange',
    'COORDINACION TERRITORIAL A': 'red',
    'ESPECIALISTAS PRODUCTIVOS Y SOCIALES': 'cyan',
    'SEMBRADOR': 'yellow',
    'OTRO': 'gray'
  }
  
  return coloresCargo[cargoUpper] || 'gray'
}

// Función para obtener color del territorio - mapeo fijo único para cada territorio
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

// Computed: Contar usuarios por cargo (considerando filtros de estado y búsqueda)
const contadorPorCargo = computed(() => {
  let usuariosFiltradosBase = [...usuarios.value]
  
  // Aplicar filtro de estado
  if (filtroEstado.value === 'activos') {
    usuariosFiltradosBase = usuariosFiltradosBase.filter(usuario => 
      usuario.activo === true || usuario.activo === undefined || usuario.activo === null
    )
  } else if (filtroEstado.value === 'inactivos') {
    usuariosFiltradosBase = usuariosFiltradosBase.filter(usuario => usuario.activo === false)
  }
  
  // Aplicar filtro de búsqueda
  if (searchTerm.value.trim()) {
    const termino = searchTerm.value.toLowerCase()
    usuariosFiltradosBase = usuariosFiltradosBase.filter(usuario => 
      usuario.correo.toLowerCase().includes(termino) ||
      (usuario.nombre_completo && usuario.nombre_completo.toLowerCase().includes(termino)) ||
      (usuario.cargo && usuario.cargo.toLowerCase().includes(termino)) ||
      (usuario.supervisor && usuario.supervisor.toLowerCase().includes(termino)) ||
      (usuario.curp && usuario.curp.toLowerCase().includes(termino)) ||
      (usuario.territorio && usuario.territorio.toLowerCase().includes(termino))
    )
  }
  
  // Contar por cargo
  const contador = {}
  
  cargosDisponibles.forEach(cargo => {
    if (cargo === 'OTRO') {
      contador[cargo] = usuariosFiltradosBase.filter(u => 
        u.cargo && u.cargo.toUpperCase() === 'OTRO'
      ).length
    } else {
      contador[cargo] = usuariosFiltradosBase.filter(u => 
        u.cargo && u.cargo.toUpperCase() === cargo.toUpperCase()
      ).length
    }
  })
  
  // Contar sin cargo
  contador['sin-cargo'] = usuariosFiltradosBase.filter(u => 
    !u.cargo || u.cargo.trim() === ''
  ).length
  
  // Total
  contador['todos'] = usuariosFiltradosBase.length
  
  return contador
})

// Computed: Contar usuarios por estado (activos/inactivos)
const contadorEstados = computed(() => {
  const activos = usuarios.value.filter(u => 
    u.activo === true || u.activo === undefined || u.activo === null
  ).length
  const inactivos = usuarios.value.filter(u => u.activo === false).length
  return { activos, inactivos }
})

// Computed: detectar si el usuario editado es técnico
const esTecnicoEdicion = computed(() => {
  const cargo = (datosEdicion.value.cargo || '').toUpperCase()
  return cargo === 'TECNICO SOCIAL' || cargo === 'TECNICO PRODUCTIVO'
})

// Función para buscar supervisor automático por territorio
const buscarSupervisorAutomatico = async (territorio) => {
  if (!territorio) {
    datosEdicion.value.supervisor = ''
    return
  }
  
  try {
    buscandoSupervisor.value = true
    console.log('🔍 Buscando supervisor para territorio:', territorio)
    
    const response = await fetch(`${API_URL}/supervisor-territorio/${encodeURIComponent(territorio)}`)
    const data = await response.json()
    
    if (data.success && data.supervisor) {
      datosEdicion.value.supervisor = data.supervisor
      console.log('✅ Supervisor encontrado:', data.supervisor)
    } else {
      datosEdicion.value.supervisor = ''
      console.log('⚠️ No hay supervisor territorial para:', territorio)
    }
  } catch (error) {
    console.error('❌ Error buscando supervisor:', error)
    datosEdicion.value.supervisor = ''
  } finally {
    buscandoSupervisor.value = false
  }
}

// Watcher: cuando cambie el territorio en el modal de edición
watch(() => datosEdicion.value.territorio, async (nuevoTerritorio, viejoTerritorio) => {
  // No hacer nada si estamos inicializando el modal
  if (inicializandoModalEdicion.value) return
  
  if (nuevoTerritorio !== viejoTerritorio && esTecnicoEdicion.value) {
    await buscarSupervisorAutomatico(nuevoTerritorio)
  }
})

// Watcher: cuando cambie el cargo en el modal de edición
watch(() => datosEdicion.value.cargo, async (nuevoCargo, viejoCargo) => {
  // No hacer nada si estamos inicializando el modal
  if (inicializandoModalEdicion.value) return
  
  if (nuevoCargo !== viejoCargo) {
    const cargoUpper = (nuevoCargo || '').toUpperCase()
    const esNuevoTecnico = cargoUpper === 'TECNICO SOCIAL' || cargoUpper === 'TECNICO PRODUCTIVO'
    const viejoCargoUpper = (viejoCargo || '').toUpperCase()
    const eraViejoTecnico = viejoCargoUpper === 'TECNICO SOCIAL' || viejoCargoUpper === 'TECNICO PRODUCTIVO'
    
    // Limpiar cargoOtro si el usuario cambia de OTRO a otro cargo
    if (viejoCargo === 'OTRO' && nuevoCargo !== 'OTRO') {
      datosEdicion.value.cargoOtro = ''
    }
    
    if (esNuevoTecnico && datosEdicion.value.territorio) {
      // Si ahora es técnico y tiene territorio, buscar supervisor automático
      await buscarSupervisorAutomatico(datosEdicion.value.territorio)
    } else if (eraViejoTecnico && !esNuevoTecnico) {
      // Solo limpiar supervisor si está CAMBIANDO de técnico a no-técnico
      datosEdicion.value.supervisor = ''
    }
  }
})

onMounted(() => {
  cargarUsuarios()
  
  // Escuchar cambios de conexión
  window.addEventListener('online', () => {
    isOnline.value = true
  })
  
  window.addEventListener('offline', () => {
    isOnline.value = false
  })
  
  // Escuchar actualizaciones de permisos en tiempo real
  window.addEventListener('user-session-updated', actualizarPermisosUsuario)
})

// Limpiar listeners al desmontar
onUnmounted(() => {
  window.removeEventListener('user-session-updated', actualizarPermisosUsuario)
})

// Función para cargar supervisores territoriales actuales
const cargarSupervisoresTerritoriales = async () => {
  try {
    console.log('🔄 Cargando supervisores territoriales...')
    const response = await fetch(`${API_URL}/admin/usuarios`)
    if (!response.ok) throw new Error('Error al cargar admins')
    
    const data = await response.json()
    const admins = data.usuarios || data
    
    // Crear mapa de territorio -> supervisor
    const mapa = {}
    admins.forEach(admin => {
      if (admin.es_territorial && admin.territorio && admin.nombre_completo) {
        mapa[admin.territorio] = admin.nombre_completo
      }
    })
    
    supervisoresPorTerritorio.value = mapa
    console.log('✅ Supervisores territoriales cargados:', Object.keys(mapa).length)
    
    return mapa
  } catch (error) {
    console.error('❌ Error al cargar supervisores territoriales:', error)
    return {}
  }
}

// Función para actualizar supervisor de un técnico según su territorio
const actualizarSupervisorTecnico = (usuario) => {
  const esTecnico = usuario.cargo && (
    usuario.cargo.toUpperCase().includes('TECNICO SOCIAL') ||
    usuario.cargo.toUpperCase().includes('TECNICO PRODUCTIVO')
  )
  
  if (esTecnico && usuario.territorio) {
    const supervisorActual = supervisoresPorTerritorio.value[usuario.territorio]
    if (supervisorActual) {
      usuario.supervisor = supervisorActual
    }
  }
  
  return usuario
}

const cargarUsuarios = async () => {
  loading.value = true
  error.value = ''
  recargaCompleta.value = true // Marcar que es recarga completa
  
  try {
    // Primero cargar los supervisores territoriales
    await cargarSupervisoresTerritoriales()
    
    // Usar el servicio de usuarios con datos reales de la base de datos
    let usuariosDB = await usuariosService.obtenerUsuarios()
    
    // Actualizar supervisores de técnicos con los datos actuales de territoriales
    usuarios.value = usuariosDB.map(usuario => actualizarSupervisorTecnico({...usuario}))
    usuariosFiltrados.value = usuarios.value
    
    // Actualizar contador de usuarios
    totalUsuarios.value = usuarios.value.length.toLocaleString('es')
    
    // Aplicar ordenamiento inicial
    aplicarOrdenamiento()
    
    console.log('✅ Usuarios reales cargados desde la base de datos:', usuarios.value)
  } catch (err) {
    console.error('❌ Error al cargar usuarios desde la base de datos:', err)
    error.value = 'Error al conectar con la base de datos. Verifica que el servidor esté funcionando.'
    usuarios.value = []
    usuariosFiltrados.value = []
    totalUsuarios.value = '0'
  } finally {
    loading.value = false
  }
}

// Función para sincronizar supervisores de todos los técnicos
const sincronizarSupervisores = async () => {
  if (sincronizando.value) return
  
  sincronizando.value = true
  
  try {
    console.log('🔄 Sincronizando supervisores de técnicos...')
    
    // Recargar supervisores territoriales
    await cargarSupervisoresTerritoriales()
    
    // Actualizar supervisores de todos los técnicos en el array local
    let actualizados = 0
    usuarios.value = usuarios.value.map(usuario => {
      const usuarioOriginal = {...usuario}
      const usuarioActualizado = actualizarSupervisorTecnico({...usuario})
      
      if (usuarioOriginal.supervisor !== usuarioActualizado.supervisor) {
        actualizados++
      }
      
      return usuarioActualizado
    })
    
    // Actualizar filtrados
    filtrarUsuarios(false)
    
    console.log(`✅ Sincronización completada: ${actualizados} técnicos actualizados`)
    
    alert(`Supervisores sincronizados correctamente.\n${actualizados} técnicos actualizados.`)
    
  } catch (error) {
    console.error('❌ Error al sincronizar supervisores:', error)
    alert('Error al sincronizar supervisores. Por favor, intenta de nuevo.')
  } finally {
    sincronizando.value = false
  }
}

// Funciones de exportación
const imprimirUsuarios = () => {
  const ventanaImpresion = window.open('', '_blank')
  
  const estilosImpresion = `
    <style>
      * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
      }
      
      body { 
        font-family: Arial, sans-serif; 
        font-size: 10px; 
        margin: 0; 
        padding: 15px;
        background: white;
        color: #333;
      }
      
      .header { 
        text-align: center; 
        margin-bottom: 25px; 
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 12px;
      }
      
      .header h1 { 
        color: #4CAF50; 
        margin: 0; 
        font-size: 22px;
        font-weight: bold;
      }
      
      .header p { 
        margin: 4px 0; 
        color: #666;
        font-size: 11px;
      }
      
      table { 
        width: 100%; 
        border-collapse: collapse; 
        margin-top: 15px;
        font-size: 9px;
        border: 2px solid #4CAF50;
      }
      
      th, td { 
        border: 1px solid #ddd; 
        padding: 6px 4px; 
        text-align: left;
        word-wrap: break-word;
        vertical-align: top;
      }
      
      th { 
        background-color: #4CAF50 !important; 
        color: white !important; 
        font-weight: bold;
        font-size: 8px;
        text-align: center;
      }
      
      tr:nth-child(even) { 
        background-color: #f8f9fa !important; 
      }
      
      tr:nth-child(odd) { 
        background-color: white !important; 
      }
      
      .col-id { width: 60px; text-align: center; }
      .col-correo { width: 180px; }
      .col-nombre { width: 140px; }
      .col-cargo { width: 120px; }
      .col-supervisor { width: 140px; }
      .col-curp { width: 120px; text-align: center; }
      .col-territorio { width: 100px; text-align: center; }
      .col-estado { width: 70px; text-align: center; font-size: 8px; }
      .col-telefono { width: 120px; font-family: monospace; font-size: 8px; }
      
      .estado-activo { 
        color: #28a745 !important; 
        font-weight: bold; 
      }
      
      .estado-inactivo { 
        color: #dc3545 !important; 
        font-weight: bold; 
      }
      
      .footer {
        margin-top: 25px;
        text-align: center;
        font-size: 9px;
        color: #666;
        border-top: 1px solid #ddd;
        padding-top: 12px;
      }
      
      @media print {
        body { 
          font-family: Arial, sans-serif; 
          font-size: 10px; 
          margin: 0; 
          padding: 15px;
          -webkit-print-color-adjust: exact;
          print-color-adjust: exact;
        }
        
        table {
          page-break-inside: auto;
        }
        
        tr {
          page-break-inside: avoid;
          page-break-after: auto;
        }
        
        @page {
          margin: 0.5in;
          size: A4 landscape;
        }
      }
      
      @media screen {
        body {
          max-width: 1200px;
          margin: 0 auto;
        }
      }
    </style>
  `
  
  const fecha = new Date().toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
  
  const obtenerEstadoUsuario = (usuario) => {
    // Determinar estado basado en si tiene datos completos (sin contar contraseña)
    const tieneCorreo = usuario.correo && usuario.correo.trim() !== ''
    const tieneNombre = usuario.nombre_completo && usuario.nombre_completo.trim() !== ''
    const tieneCargo = usuario.cargo && usuario.cargo.trim() !== ''
    const tieneCurp = usuario.curp && usuario.curp.trim() !== ''
    
    return (tieneCorreo && tieneNombre && tieneCargo && tieneCurp) ? 'Activo' : 'Incompleto'
  }
  
  const obtenerFechaRegistro = (usuario) => {
    // Usar fecha real si está disponible, sino simular basada en ID
    if (usuario.fecha_registro) {
      return formatFecha(usuario.fecha_registro)
    } else if (usuario.created_at) {
      return formatFecha(usuario.created_at)
    } else {
      // Simular fecha basada en ID (usuarios más recientes tienen ID mayor)
      const baseDate = new Date('2024-01-01')
      const daysToAdd = (usuario.id || 1) * 2 // 2 días por ID para espaciar
      const fechaSimulada = new Date(baseDate.getTime() + (daysToAdd * 24 * 60 * 60 * 1000))
      return fechaSimulada.toLocaleDateString('es-ES')
    }
  }
  
  const contenidoHTML = `
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Lista Completa de Usuarios - ${fecha}</title>
      ${estilosImpresion}
    </head>
    <body>
      <div class="header">
        <h1>📋 Lista de Usuarios del Sistema</h1>
        <p>Generado el: ${fecha}</p>
        <p>Total de usuarios: ${usuariosFiltrados.value.length}</p>
        <p><strong>Información administrativa del sistema</strong></p>
      </div>
      
      <table>
        <thead>
          <tr>
            <th class="col-id">ID</th>
            <th class="col-correo">Correo</th>
            <th class="col-nombre">Nombre</th>
            <th class="col-cargo">Cargo</th>
            <th class="col-supervisor">Supervisor</th>
            <th class="col-curp">CURP</th>
            <th class="col-territorio">Territorio</th>
            <th class="col-estado">Estado</th>
          </tr>
        </thead>
        <tbody>
          ${usuariosFiltrados.value.map(usuario => {
            return `
            <tr style="${usuario.activo === false ? 'opacity:0.45;background:#f0f0f0;color:#999;' : ''}">
              <td class="col-id">${usuario.id}</td>
              <td class="col-correo">${usuario.correo || 'No especificado'}</td>
              <td class="col-nombre">${usuario.nombre_completo || 'Sin nombre'}</td>
              <td class="col-cargo">${usuario.cargo || 'Sin cargo'}</td>
              <td class="col-supervisor">${usuario.supervisor || 'Sin supervisor'}</td>
              <td class="col-curp">${(usuario.curp || 'Sin CURP').toUpperCase()}</td>
              <td class="col-territorio">${usuario.territorio || ''}</td>
              <td class="col-estado" style="color:${usuario.activo === false ? '#999' : '#2e7d32'};font-weight:700;">${usuario.activo === false ? 'Inactivo' : 'Activo'}</td>
            </tr>
            `
          }).join('')}
        </tbody>
      </table>
      
      <div class="footer">
        <p><strong>Sistema de Gestión de Usuarios PWA</strong></p>
        <p>Documento generado automáticamente</p>
        <p>Total de registros: ${usuariosFiltrados.value.length} usuarios</p>
      </div>
    </body>
    </html>
  `
  
  // Escribir el contenido y asegurar carga completa
  ventanaImpresion.document.open()
  ventanaImpresion.document.write(contenidoHTML)
  ventanaImpresion.document.close()
  
  // Esperar a que se carguen completamente los estilos antes de imprimir
  ventanaImpresion.onload = function() {
    setTimeout(() => {
      ventanaImpresion.print()
    }, 500)
  }
  
  // Fallback por si onload no se dispara
  setTimeout(() => {
    if (ventanaImpresion.document.readyState === 'complete') {
      ventanaImpresion.print()
    }
  }, 750)
}

const exportarExcel = () => {
  // Headers completos con todos los campos incluyendo Estado
  const headers = [
    'ID Usuario',
    'Correo Electrónico', 
    'Nombre Completo', 
    'Cargo', 
    'Supervisor', 
    'CURP',
    'Territorio',
    'Teléfono',
    'Estado'
  ]
  
  const obtenerEstadoUsuario = (usuario) => {
    return usuario.activo === false ? 'Inactivo' : 'Activo'
  }
  
  const obtenerFechaRegistro = (usuario) => {
    if (usuario.fecha_registro) {
      return formatFecha(usuario.fecha_registro)
    } else if (usuario.created_at) {
      return formatFecha(usuario.created_at)
    } else {
      // Simular fecha basada en ID
      const baseDate = new Date('2024-01-01')
      const daysToAdd = (usuario.id || 1) * 2
      const fechaSimulada = new Date(baseDate.getTime() + (daysToAdd * 24 * 60 * 60 * 1000))
      return fechaSimulada.toLocaleDateString('es-ES')
    }
  }
  
  const csvData = usuariosFiltrados.value.map(usuario => [
    usuario.id || '',
    usuario.correo || 'No especificado',
    usuario.nombre_completo || 'Sin nombre',
    usuario.cargo || 'Sin cargo',
    usuario.supervisor || 'Sin supervisor',
    (usuario.curp || 'Sin CURP').toUpperCase(),
    usuario.territorio || '',
    usuario.telefono || 'Sin teléfono',
    obtenerEstadoUsuario(usuario)
  ])
  
  // Crear contenido CSV con información adicional
  let csvContent = `"SISTEMA DE GESTIÓN DE USUARIOS PWA"\n`
  csvContent += `"Exportación generada el: ${new Date().toLocaleDateString('es-ES', { 
    year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' 
  })}"\n`
  csvContent += `"Total de usuarios: ${usuariosFiltrados.value.length}"\n`
  csvContent += `"Información administrativa del sistema"\n\n`
  
  // Agregar headers
  csvContent += headers.join(',') + '\n'
  
  // Agregar datos
  csvData.forEach(row => {
    csvContent += row.map(field => `"${field}"`).join(',') + '\n'
  })
  
  // Agregar información adicional al final
  csvContent += `\n"Notas:"\n`
  csvContent += `"- CURP mostrada en mayúsculas para mejor legibilidad"\n`
  csvContent += `"- Información de contraseñas y fechas excluida por seguridad"\n`
  
  // Agregar BOM para caracteres especiales en Excel
  const BOM = '\uFEFF'
  const csvWithBOM = BOM + csvContent
  
  // Crear y descargar el archivo
  const blob = new Blob([csvWithBOM], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  
  if (link.download !== undefined) {
    const fecha = new Date().toISOString().split('T')[0]
    const url = URL.createObjectURL(blob)
    link.setAttribute('href', url)
    link.setAttribute('download', `usuarios_${fecha}.csv`)
    link.style.visibility = 'hidden'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
}

const filtrarUsuarios = (resetPaginacion = true) => {
  let resultado = usuarios.value
  
  // Filtrar por estado (activo/inactivo)
  if (filtroEstado.value === 'activos') {
    resultado = resultado.filter(usuario => usuario.activo === true || usuario.activo === undefined || usuario.activo === null)
  } else if (filtroEstado.value === 'inactivos') {
    resultado = resultado.filter(usuario => usuario.activo === false)
  }
  
  // Filtrar por cargo
  if (filtroCargo.value !== 'todos') {
    if (filtroCargo.value === 'sin-cargo') {
      resultado = resultado.filter(usuario => !usuario.cargo || usuario.cargo.trim() === '')
    } else {
      resultado = resultado.filter(usuario => 
        usuario.cargo && usuario.cargo.toUpperCase() === filtroCargo.value.toUpperCase()
      )
    }
  }
  
  // Filtrar por término de búsqueda
  if (searchTerm.value.trim()) {
    const termino = searchTerm.value.toLowerCase()
    resultado = resultado.filter(usuario => 
      usuario.correo.toLowerCase().includes(termino) ||
      (usuario.nombre_completo && usuario.nombre_completo.toLowerCase().includes(termino)) ||
      (usuario.cargo && usuario.cargo.toLowerCase().includes(termino)) ||
      (usuario.supervisor && usuario.supervisor.toLowerCase().includes(termino)) ||
      (usuario.curp && usuario.curp.toLowerCase().includes(termino)) ||
      (usuario.territorio && usuario.territorio.toLowerCase().includes(termino))
    )
  }
  
  usuariosFiltrados.value = resultado
  
  if (resetPaginacion) {
    resetearPaginacion()
  }
  aplicarOrdenamiento()
}

const limpiarBusquedaUsuarios = () => {
  searchTerm.value = ''
  filtrarUsuarios()
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
  if (!usuariosFiltrados.value.length) return

  usuariosFiltrados.value.sort((a, b) => {
    let valorA, valorB

    switch (campoOrdenamiento.value) {
      case 'id':
        valorA = parseInt(a.id)
        valorB = parseInt(b.id)
        break
      case 'nombre':
        valorA = (a.nombre_completo || '').toLowerCase()
        valorB = (b.nombre_completo || '').toLowerCase()
        break
      case 'fecha':
        valorA = new Date(a.fecha_registro)
        valorB = new Date(b.fecha_registro)
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
    // Si viene una fecha ISO completa (con T), la procesamos con zona horaria
    if (typeof fechaStr === 'string' && fechaStr.includes('T')) {
      return new Date(fechaStr).toLocaleDateString('es-ES', {
        timeZone: 'America/Mexico_City' // Forzar zona horaria de México
      })
    }
    
    // Si viene solo una fecha (YYYY-MM-DD), crear la fecha sin zona horaria
    if (typeof fechaStr === 'string' && fechaStr.match(/^\d{4}-\d{2}-\d{2}$/)) {
      const [year, month, day] = fechaStr.split('-').map(num => parseInt(num, 10))
      const fecha = new Date(year, month - 1, day) // month - 1 porque los meses en JS van de 0-11
      
      return fecha.toLocaleDateString('es-ES')
    }
    
    // Para otros casos, usar el método estándar
    return new Date(fechaStr).toLocaleDateString('es-ES')
  } catch (e) {
    console.error('Error al formatear fecha:', e, 'Fecha original:', fechaStr)
    return fechaStr
  }
}

const verDetalles = (usuario) => {
  modalTitle.value = 'Detalles del Usuario'
  usuarioSeleccionado.value = usuario
  showPassword.value = false // Resetear al cerrar/abrir modal
  
  // Debug para ver qué datos tiene el usuario
  console.log('🔍 Usuario seleccionado para detalles:', usuario)
  console.log('🔑 Contraseña disponible:', usuario.contrasena || usuario.password || usuario.contraseña || 'No encontrada')
  
  showModal.value = true
}

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

// Función helper para obtener la contraseña del usuario
const obtenerContrasenaUsuario = (usuario) => {
  if (!usuario) return 'Sin contraseña'
  
  // Verificar diferentes posibles nombres del campo contraseña
  const contraseña = usuario.contrasena || usuario.password || usuario.contraseña || usuario.pwd
  
  console.log('🔍 Buscando contraseña en usuario:', usuario)
  console.log('🔑 Contraseña encontrada:', contraseña)
  console.log('📋 Propiedades del usuario:', Object.keys(usuario))
  
  return contraseña || 'Sin contraseña'
}

const cerrarModal = () => {
  showModal.value = false
  usuarioSeleccionado.value = null
  showPassword.value = false
}

const confirmarEliminarUsuario = (usuario) => {
  usuarioAEliminar.value = usuario
  showDeleteModal.value = true
}

const toggleEstadoUsuario = async (usuario) => {
  usuarioACambiarEstado.value = usuario
  showEstadoModal.value = true
}

const cancelarCambioEstado = () => {
  showEstadoModal.value = false
  usuarioACambiarEstado.value = null
  cambiandoEstado.value = false
}

const confirmarCambioEstado = async () => {
  if (!usuarioACambiarEstado.value) return
  
  cambiandoEstado.value = true
  const nuevoEstado = !usuarioACambiarEstado.value.activo
  const accion = nuevoEstado ? 'activar' : 'desactivar'
  
  try {
    console.log(`🔄 ${accion === 'activar' ? 'Activando' : 'Desactivando'} usuario:`, usuarioACambiarEstado.value.username)
    
    // Llamar al servicio para cambiar el estado
    await usuariosService.cambiarEstadoUsuario(usuarioACambiarEstado.value.id, nuevoEstado)
    
    // Actualizar el estado local
    usuarioACambiarEstado.value.activo = nuevoEstado
    
    console.log(`✅ Usuario ${accion === 'activar' ? 'activado' : 'desactivado'} exitosamente`)
    
    // Actualizar la lista filtrada en tiempo real
    filtrarUsuarios(false)
    
    // Cerrar modal
    cancelarCambioEstado()
    
  } catch (error) {
    console.error(`❌ Error al ${accion} usuario:`, error)
    alert(`Error al ${accion} la cuenta. Por favor, inténtalo de nuevo.`)
  } finally {
    cambiandoEstado.value = false
  }
}


const cancelarEliminar = () => {
  showDeleteModal.value = false
  usuarioAEliminar.value = null
  eliminandoUsuario.value = false
}

const eliminarUsuario = async () => {
  if (!usuarioAEliminar.value) return
  
  eliminandoUsuario.value = true
  
  try {
    console.log('🗑️ Eliminando usuario:', usuarioAEliminar.value)
    
    // Llamar al servicio para eliminar el usuario
    await usuariosService.eliminarUsuario(usuarioAEliminar.value.id)
    
    // Eliminar del array local
    const index = usuarios.value.findIndex(u => u.id === usuarioAEliminar.value.id)
    if (index !== -1) {
      usuarios.value.splice(index, 1)
    }
    
    // Actualizar usuarios filtrados sin resetear paginación
    filtrarUsuarios(false)
    
    // Ajustar página actual si la página quedó vacía
    if (usuariosPaginados.value.length === 0 && paginaActual.value > 1) {
      paginaActual.value = Math.min(paginaActual.value - 1, totalPaginas.value)
    }
    
    console.log('✅ Usuario eliminado exitosamente')
    
    // Cerrar modal
    cancelarEliminar()
    
  } catch (error) {
    console.error('❌ Error al eliminar usuario:', error)
    // Aquí podrías mostrar un mensaje de error al usuario
    alert('Error al eliminar el usuario. Por favor, inténtalo de nuevo.')
  } finally {
    eliminandoUsuario.value = false
  }
}

// Funciones para edición de usuarios
const editarUsuario = async (usuario) => {
  usuarioAEditar.value = usuario
  showEditPassword.value = false // Resetear visibilidad de contraseña
  inicializandoModalEdicion.value = true // Activar bandera de inicialización
  
  // Detectar si el cargo está en la lista de cargos predefinidos
  const cargoUsuario = usuario.cargo || ''
  const cargoEstaEnLista = cargosDisponibles.includes(cargoUsuario.toUpperCase())
  
  // Llenar el formulario con los datos del usuario
  datosEdicion.value = {
    correo: usuario.correo || '',
    nombre_completo: usuario.nombre_completo || '',
    cargo: cargoEstaEnLista ? cargoUsuario.toUpperCase() : 'OTRO',
    cargoOtro: cargoEstaEnLista ? '' : cargoUsuario.toUpperCase(),
    supervisor: usuario.supervisor || '',
    contrasena: usuario.contrasena || '',
    curp: usuario.curp || '',
    telefono: usuario.telefono || '',
    territorio: usuario.territorio || ''
  }
  
  // Esperar un tick para que los watchers no interfieran
  await new Promise(resolve => setTimeout(resolve, 50))
  inicializandoModalEdicion.value = false // Desactivar bandera
  
  showEditModal.value = true
  
  // Si es técnico y tiene territorio, buscar supervisor automático
  const cargoUpper = (usuario.cargo || '').toUpperCase()
  const esTecnico = cargoUpper === 'TECNICO SOCIAL' || cargoUpper === 'TECNICO PRODUCTIVO'
  if (esTecnico && usuario.territorio) {
    await buscarSupervisorAutomatico(usuario.territorio)
  }
}

const cancelarEdicion = () => {
  showEditModal.value = false
  usuarioAEditar.value = null
  editandoUsuario.value = false
  inicializandoModalEdicion.value = false // Resetear bandera
  showEditPassword.value = false // Resetear visibilidad de contraseña
  // Limpiar formulario
  datosEdicion.value = {
    correo: '',
    nombre_completo: '',
    cargo: '',
    cargoOtro: '',
    supervisor: '',
    contrasena: '',
    curp: '',
    telefono: '',
    territorio: ''
  }
}

const guardarEdicion = async () => {
  if (!usuarioAEditar.value) return
  
  editandoUsuario.value = true
  
  try {
    console.log('✏️ Editando usuario:', usuarioAEditar.value.id, datosEdicion.value)
    
    // Determinar el cargo final: si es OTRO, usar cargoOtro; si no, usar cargo
    const cargoFinal = datosEdicion.value.cargo === 'OTRO' 
      ? datosEdicion.value.cargoOtro.trim().toUpperCase() 
      : datosEdicion.value.cargo.toUpperCase()
    
    // Normalizar nombre_completo, curp y supervisor (mayúsculas sin tildes)
    const nombreNormalizado = normalizarTexto(datosEdicion.value.nombre_completo)
    const curpNormalizado = normalizarTexto(datosEdicion.value.curp)
    const supervisorNormalizado = normalizarTexto(datosEdicion.value.supervisor)
    
    // Preparar datos para el backend con el formato correcto
    const datosParaEnviar = {
      correo: datosEdicion.value.correo,
      nombre_completo: nombreNormalizado,
      cargo: cargoFinal,
      supervisor: supervisorNormalizado,
      curp: curpNormalizado,
      telefono: datosEdicion.value.telefono,
      territorio: datosEdicion.value.territorio || null,
      rol: 'user' // Por defecto, los usuarios editados desde admin son 'user'
    }
    
    // Solo incluir nueva_contrasena si se proporcionó una nueva contraseña
    if (datosEdicion.value.contrasena && datosEdicion.value.contrasena.trim() !== '') {
      datosParaEnviar.nueva_contrasena = datosEdicion.value.contrasena.trim()
      console.log('🔑 Incluyendo nueva contraseña en la actualización')
    } else {
      console.log('⚪ No se proporcionó nueva contraseña, se mantendrá la actual')
    }
    
    console.log('📤 Enviando datos al backend:', datosParaEnviar)
    
    // Llamar al servicio para actualizar el usuario en la base de datos
    const resultado = await usuariosService.actualizarUsuario(usuarioAEditar.value.id, datosParaEnviar)
    
    // Actualizar el usuario en el array local con los datos devueltos por el servidor
    const index = usuarios.value.findIndex(u => u.id === usuarioAEditar.value.id)
    if (index !== -1) {
      // Actualizar supervisor si es técnico (reactivo)
      const usuarioActualizado = actualizarSupervisorTecnico({...resultado.usuario})
      usuarios.value[index] = usuarioActualizado
    }
    
    // Actualizar usuarios filtrados SIN resetear la paginación
    filtrarUsuarios(false)
    
    console.log('✅ Usuario editado exitosamente en la base de datos')
    
    // Cerrar modal de edición
    cancelarEdicion()
    
    // Mostrar modal de éxito
    showSuccessModal.value = true
    
  } catch (error) {
    console.error('❌ Error al editar usuario:', error)
    alert(`Error al editar el usuario: ${error.message}`)
  } finally {
    editandoUsuario.value = false
  }
}

// Función para cerrar modal de éxito
const cerrarSuccessModal = () => {
  showSuccessModal.value = false
}

// Funciones de paginación
const usuariosPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * usuariosPorPagina.value
  const fin = inicio + usuariosPorPagina.value
  return usuariosFiltrados.value.slice(inicio, fin)
})

const totalPaginas = computed(() => {
  return Math.ceil(usuariosFiltrados.value.length / usuariosPorPagina.value)
})

const indiceInicio = computed(() => {
  return (paginaActual.value - 1) * usuariosPorPagina.value
})

const indiceFin = computed(() => {
  return indiceInicio.value + usuariosPorPagina.value
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

const irAPagina = (numeroPagina) => {
  if (numeroPagina >= 1 && numeroPagina <= totalPaginas.value) {
    paginaActual.value = numeroPagina
  }
}

const saltarAPagina = () => {
  if (paginaSalto.value && paginaSalto.value >= 1 && paginaSalto.value <= totalPaginas.value) {
    irAPagina(paginaSalto.value)
    paginaSalto.value = ''
  }
}

const cambiarUsuariosPorPagina = () => {
  paginaActual.value = 1 // Reset a la primera página
}

const cambiarPagina = (nuevaPagina) => {
  if (nuevaPagina >= 1 && nuevaPagina <= totalPaginas.value) {
    paginaActual.value = nuevaPagina
  }
}

const paginaAnterior = () => {
  if (paginaActual.value > 1) {
    paginaActual.value--
  }
}

const paginaSiguiente = () => {
  if (paginaActual.value < totalPaginas.value) {
    paginaActual.value++
  }
}

// Resetear página al filtrar
const resetearPaginacion = () => {
  paginaActual.value = 1
}

// Watchers para mejor funcionalidad
watch(searchTerm, () => {
  filtrarUsuarios() // Sí resetear paginación al buscar
})

watch(filtroEstado, () => {
  filtrarUsuarios() // Filtrar en tiempo real cuando cambia el estado
})

watch(filtroCargo, () => {
  filtrarUsuarios() // Filtrar en tiempo real cuando cambia el cargo
})

watch(usuarios, () => {
  // Solo resetear paginación si es recarga completa
  const debeResetear = recargaCompleta.value
  filtrarUsuarios(debeResetear)
  recargaCompleta.value = false // Resetear el flag
})

// Validar que la página actual no exceda el total de páginas
watch(totalPaginas, (newTotal) => {
  if (paginaActual.value > newTotal && newTotal > 0) {
    paginaActual.value = newTotal
  }
})

// Obtener páginas visibles alrededor de la actual
const obtenerPaginasVisibles = () => {
  const paginas = []
  const total = totalPaginas.value
  const actual = paginaActual.value
  
  if (total <= 6) {
    // Si hay 6 páginas o menos, mostrar todas
    for (let i = 2; i < total; i++) {
      paginas.push(i)
    }
  } else {
    // Lógica para más de 6 páginas
    if (actual <= 4) {
      // Páginas al inicio
      for (let i = 2; i <= 4; i++) {
        paginas.push(i)
      }
    } else if (actual >= total - 3) {
      // Páginas al final
      for (let i = total - 3; i < total; i++) {
        paginas.push(i)
      }
    } else {
      // Páginas en el medio
      for (let i = actual - 1; i <= actual + 1; i++) {
        paginas.push(i)
      }
    }
  }
  
  return paginas
}

const logout = () => {
  // No usar confirm(), el modal se maneja en el Sidebar
  localStorage.removeItem('admin_token')
  localStorage.removeItem('admin_user')
  router.push('/login')
}
</script>

<style scoped>
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

.usuarios-container {
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
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
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

.apple-filter-btn.sync {
  color: #007AFF;
  border-color: rgba(0, 122, 255, 0.2);
}

.apple-filter-btn.sync svg {
  stroke: #007AFF;
}

.apple-filter-btn.sync:hover {
  background: rgba(0, 122, 255, 0.08);
  border-color: #007AFF;
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

.apple-filter-btn.print {
  color: #8E8E93;
  border-color: rgba(142, 142, 147, 0.2);
}

.apple-filter-btn.print svg {
  stroke: #8E8E93;
}

.apple-filter-btn.print:hover {
  background: rgba(142, 142, 147, 0.08);
  border-color: #8E8E93;
}

/* ====================== APPLE UNIFIED FILTERS ====================== */
.apple-unified-filters {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
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

.apple-count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 8px;
  border-radius: 12px;
  background: linear-gradient(135deg, #8BC34A 0%, #7CB342 100%);
  color: white;
  font-size: 11px;
  font-weight: 700;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
  box-shadow: 0 2px 6px rgba(139, 195, 74, 0.3);
}

/* ====================== APPLE SORT GROUP ====================== */
.apple-sort-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.apple-sort-label {
  font-size: 11px;
  font-weight: 600;
  color: #86868b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-sort-buttons {
  display: flex;
  gap: 4px;
}

.apple-sort-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 10px;
  border-radius: 10px;
  border: 1.5px solid #e5e5e5;
  background: white;
  color: #1d1d1f;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-sort-btn svg {
  width: 12px;
  height: 12px;
  stroke-width: 2;
}

.apple-sort-btn .sort-direction {
  width: 10px;
  height: 10px;
}

.apple-sort-btn:hover {
  background: #f5f5f7;
  border-color: #d1d1d6;
}

.apple-sort-btn.active {
  background: linear-gradient(135deg, #8BC34A 0%, #7CB342 100%);
  color: white;
  border-color: #8BC34A;
}

.apple-sort-btn.active svg {
  stroke: white;
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

.apple-table-row.apple-row-inactive {
  opacity: 0.6;
  background: #f5f5f7;
}

.apple-table td {
  padding: 14px 16px;
  font-size: 13px;
  color: #1D1D1F;
  border-left: 2px solid transparent;
  transition: all 0.15s ease;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-table-row:hover td:first-child {
  border-left-color: #8BC34A;
}

/* ====================== APPLE TABLE CELLS ====================== */
.apple-id-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 6px;
  background: rgba(0, 122, 255, 0.1);
  color: #007AFF;
  font-size: 12px;
  font-weight: 600;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
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
  flex: 1;
}

.apple-user-name {
  font-size: 13px;
  font-weight: 600;
  color: #1d1d1f;
}

.apple-email {
  font-size: 12px;
  color: #86868b;
  font-style: italic;
}

.apple-cargo-badge {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.apple-cargo-badge.cargo-blue {
  background: rgba(0, 122, 255, 0.1);
  color: #007AFF;
}

.apple-cargo-badge.cargo-green {
  background: rgba(52, 199, 89, 0.1);
  color: #34C759;
}

.apple-cargo-badge.cargo-purple {
  background: rgba(175, 82, 222, 0.1);
  color: #AF52DE;
}

.apple-cargo-badge.cargo-orange {
  background: rgba(255, 149, 0, 0.1);
  color: #FF9500;
}

.apple-cargo-badge.cargo-red {
  background: rgba(255, 59, 48, 0.1);
  color: #FF3B30;
}

.apple-cargo-badge.cargo-gray,
.apple-cargo-badge.cargo-empty {
  background: rgba(142, 142, 147, 0.1);
  color: #8E8E93;
}

.apple-supervisor {
  font-size: 12px;
  color: #1d1d1f;
}

.apple-curp {
  font-size: 11px;
  font-weight: 500;
  color: #86868b;
  font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
  letter-spacing: 0.5px;
}

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

.apple-territorio {
  font-size: 12px;
  color: #1d1d1f;
}

.apple-no-data {
  font-size: 12px;
  color: #d1d1d6;
}

.apple-status-badge {
  display: inline-flex;
  align-items: center;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.apple-status-badge.activo {
  background: rgba(52, 199, 89, 0.15);
  color: #34C759;
}

.apple-status-badge.inactivo {
  background: rgba(255, 59, 48, 0.1);
  color: #FF3B30;
}

/* ====================== APPLE ACTIONS ====================== */
.apple-actions {
  display: flex;
  gap: 6px;
}

.apple-action-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.apple-action-btn svg {
  width: 14px;
  height: 14px;
  stroke-width: 2;
}

.apple-action-btn.view {
  background: linear-gradient(135deg, #007AFF 0%, #5AC8FA 100%);
  color: white;
}

.apple-action-btn.view svg {
  stroke: white;
}

.apple-action-btn.view:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.4);
}

.apple-action-btn.edit {
  background: linear-gradient(135deg, #FF9500 0%, #FFCC00 100%);
  color: white;
}

.apple-action-btn.edit svg {
  stroke: white;
}

.apple-action-btn.edit:hover:not(.disabled) {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(255, 149, 0, 0.4);
}

.apple-action-btn.activate {
  background: linear-gradient(135deg, #34C759 0%, #30D158 100%);
  color: white;
}

.apple-action-btn.activate svg {
  stroke: white;
}

.apple-action-btn.activate:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(52, 199, 89, 0.4);
}

.apple-action-btn.deactivate {
  background: linear-gradient(135deg, #8E8E93 0%, #AEAEB2 100%);
  color: white;
}

.apple-action-btn.deactivate svg {
  stroke: white;
}

.apple-action-btn.deactivate:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(142, 142, 147, 0.4);
}

.apple-action-btn.delete {
  background: linear-gradient(135deg, #FF3B30 0%, #FF6961 100%);
  color: white;
}

.apple-action-btn.delete svg {
  stroke: white;
}

.apple-action-btn.delete:hover:not(.disabled) {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(255, 59, 48, 0.4);
}

.apple-action-btn.disabled {
  background: #d1d1d6;
  cursor: not-allowed;
  opacity: 0.6;
}

.apple-action-btn.disabled:hover {
  transform: none;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

/* ====================== APPLE LOADING/ERROR/EMPTY STATES ====================== */
.apple-loading,
.apple-error,
.apple-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.apple-loading p,
.apple-error p,
.apple-empty p {
  color: #86868b;
  font-size: 14px;
  margin: 12px 0 0 0;
}

.apple-empty h3 {
  color: #1d1d1f;
  font-size: 18px;
  font-weight: 600;
  margin: 12px 0 4px 0;
}

.apple-loading svg,
.apple-error svg,
.apple-empty svg {
  width: 64px;
  height: 64px;
  stroke: #8BC34A;
  stroke-width: 1.5;
}

.apple-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #E8F5E9;
  border-top-color: #8BC34A;
  border-radius: 50%;
  animation: apple-spin-animation 1s linear infinite;
}

.apple-retry-btn {
  margin-top: 16px;
  padding: 10px 20px;
  border-radius: 12px;
  border: none;
  background: linear-gradient(135deg, #8BC34A 0%, #7CB342 100%);
  color: white;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
}

.apple-retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 195, 74, 0.4);
}

/* ====================== APPLE PAGINATION ====================== */
.apple-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
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

/* ====================== OLD STYLES FOR COMPATIBILITY ====================== */
.page-header {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 50%, #2E7D32 100%);
  color: white;
  padding: clamp(0.3rem, 0.8vw, 0.5rem);
  box-shadow: 
    0 4px 16px rgba(76, 175, 80, 0.15);
  position: sticky;
  top: 0;
  z-index: 100;
  width: 100%;
  box-sizing: border-box;
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
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
  min-width: 120px;
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

.page-content {
  padding: clamp(16px, 2vw, 24px);
  box-sizing: border-box;
  width: 100%;
  max-width: 100%;
  margin: 0;
}

.search-section {
  margin-bottom: clamp(8px, 1.5vw, 12px);
  animation: slideInRight 0.6s ease-out;
  background: linear-gradient(135deg, #f0fff4 0%, #e8f5e8 100%);
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-radius: clamp(6px, 1.2vw, 9px);
  padding: clamp(6px, 1.5vw, 10px) clamp(8px, 2vw, 12px);
  box-shadow: 
    0 6px 24px rgba(76, 175, 80, 0.12),
    0 3px 12px rgba(76, 175, 80, 0.08);
  transition: all 0.3s ease;
}

.search-section:hover {
  border-color: rgba(76, 175, 80, 0.5);
  box-shadow: 
    0 8px 32px rgba(76, 175, 80, 0.15),
    0 4px 16px rgba(76, 175, 80, 0.1);
  transform: translateY(-1px);
}

.controls-row {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
  justify-content: space-between;
}

.controls-left {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
  flex: 1;
  min-width: 0;
}

.controls-right {
  display: flex;
  align-items: center;
  margin-left: clamp(0.5rem, 1.5vw, 1rem);
  flex-shrink: 0;
}

.controls-right .users-stats-compact {
  margin: 0;
  padding: 0;
  display: flex;
  gap: clamp(0.3rem, 0.8vw, 0.4rem);
}

.search-group, .sort-group, .export-actions, .filter-estado-group {
  display: flex;
  align-items: center;
  gap: clamp(4px, 1vw, 6px);
}

.search-group {
  position: relative;
  flex: 1;
  min-width: clamp(150px, 20vw, 180px);
}

/* ========== FILTRO DE ESTADO MEJORADO ========== */
.filter-estado-group {
  display: flex;
  align-items: center;
  gap: 6px;
}

.filter-estado-buttons {
  display: flex;
  gap: 4px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(240, 255, 244, 0.95) 100%);
  padding: 4px;
  border-radius: 16px;
  border: 1.5px solid rgba(76, 175, 80, 0.2);
  box-shadow: 
    0 2px 8px rgba(76, 175, 80, 0.08),
    inset 0 1px 2px rgba(255, 255, 255, 0.9);
}

.filter-estado-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  border: none;
  border-radius: 12px;
  background: transparent;
  color: #6b7280;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  text-transform: capitalize;
  letter-spacing: 0.2px;
}

.filter-estado-btn:hover {
  background: rgba(156, 163, 175, 0.15);
  color: #4b5563;
  transform: translateY(-1px);
}

.filter-estado-btn.active {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(107, 114, 128, 0.35);
  transform: translateY(-1px);
}

.filter-estado-btn.activo {
  color: #22c55e;
}

.filter-estado-btn.activo:hover {
  background: rgba(34, 197, 94, 0.12);
  color: #16a34a;
}

.filter-estado-btn.activo.active {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(34, 197, 94, 0.4);
}

.filter-estado-btn.inactivo {
  color: #ef4444;
}

.filter-estado-btn.inactivo:hover {
  background: rgba(239, 68, 68, 0.12);
  color: #dc2626;
}

.filter-estado-btn.inactivo.active {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
}

.filter-estado-btn svg {
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

/* ========== FILTRO DE CARGO ========== */
.filter-cargo-group {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(240, 255, 244, 0.9) 100%);
  padding: 6px 12px;
  border-radius: 16px;
  border: 1.5px solid rgba(76, 175, 80, 0.2);
  box-shadow: 
    0 2px 8px rgba(76, 175, 80, 0.08),
    inset 0 1px 2px rgba(255, 255, 255, 0.9);
}

.filter-cargo-label {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #4b5563;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
  letter-spacing: 0.2px;
}

.filter-cargo-label svg {
  flex-shrink: 0;
  stroke: #4CAF50;
}

.filter-cargo-label span {
  color: #374151;
}

.filter-cargo-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-cargo-select {
  appearance: none;
  background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
  border: 1.5px solid rgba(76, 175, 80, 0.25);
  border-radius: 10px;
  padding: 6px 32px 6px 12px;
  font-size: 11px;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  min-width: 180px;
  background-image: url("data:image/svg+xml,%3Csvg width='12' height='12' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M6 9l6 6 6-6' stroke='%234CAF50' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.filter-cargo-select:hover {
  border-color: rgba(76, 175, 80, 0.4);
  background: linear-gradient(135deg, #ffffff 0%, #f0fff4 100%);
  box-shadow: 0 2px 6px rgba(76, 175, 80, 0.12);
  transform: translateY(-1px);
}

.filter-cargo-select:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 
    0 0 0 3px rgba(76, 175, 80, 0.15),
    0 2px 6px rgba(76, 175, 80, 0.2);
  transform: translateY(-1px);
}

.filter-cargo-select option {
  padding: 8px;
  font-weight: 500;
  color: #374151;
}

.filter-cargo-select option::after {
  font-weight: 600;
  color: #4CAF50;
}

/* Contador de cargo con colores */
.cargo-count-badge {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 700;
  color: white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  min-width: 50px;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.cargo-count-badge svg {
  flex-shrink: 0;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.cargo-count-number {
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  position: relative;
  z-index: 1;
}

/* Colores para el contador según el cargo */
.cargo-count-emerald {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.4);
}

.cargo-count-blue {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
}

.cargo-count-violet {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  box-shadow: 0 2px 8px rgba(139, 92, 246, 0.4);
}

.cargo-count-orange-light {
  background: linear-gradient(135deg, #fb923c 0%, #f97316 100%);
  box-shadow: 0 2px 8px rgba(251, 146, 60, 0.4);
}

.cargo-count-orange {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  box-shadow: 0 2px 8px rgba(249, 115, 22, 0.4);
}

.cargo-count-red {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
}

.cargo-count-cyan {
  background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
  box-shadow: 0 2px 8px rgba(6, 182, 212, 0.4);
}

.cargo-count-yellow {
  background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%);
  color: #422006;
  box-shadow: 0 2px 8px rgba(234, 179, 8, 0.4);
}

.cargo-count-gray {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  box-shadow: 0 2px 8px rgba(107, 114, 128, 0.4);
}

.filter-estado-btn:hover svg {
  transform: scale(1.1);
}

.filter-estado-btn.active svg {
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.sort-buttons {
  display: flex;
  gap: 4px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(240, 255, 244, 0.95) 100%);
  padding: 4px;
  border-radius: 16px;
  border: 1.5px solid rgba(76, 175, 80, 0.2);
  box-shadow: 
    0 2px 8px rgba(76, 175, 80, 0.08),
    inset 0 1px 2px rgba(255, 255, 255, 0.9);
}

.sort-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  border: none;
  border-radius: 12px;
  background: transparent;
  color: #4CAF50;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-transform: uppercase;
  letter-spacing: 0.2px;
  white-space: nowrap;
}

.sort-btn:hover {
  background: rgba(76, 175, 80, 0.12);
  color: #388E3C;
  transform: translateY(-1px);
}

.sort-btn.active {
  background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.4);
  transform: translateY(-1px);
}

.sort-btn.active:hover {
  background: linear-gradient(135deg, #388E3C 0%, #2E7D32 100%);
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(76, 175, 80, 0.5);
}

.sort-btn svg {
  flex-shrink: 0;
  transition: transform 0.2s ease;
  filter: drop-shadow(0 1px 1px rgba(0,0,0,0.1));
}

.sort-btn.active svg {
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

/* Estilos para botones de exportación */
.export-actions {
  display: flex;
  flex-wrap: wrap;
  gap: clamp(0.5rem, 1.5vw, 0.75rem);
  justify-content: flex-end;
  margin-left: auto;
  flex-shrink: 0;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: clamp(0.2rem, 0.6vw, 0.3rem);
  padding: clamp(0.25rem, 0.7vw, 0.35rem) clamp(0.45rem, 1.2vw, 0.6rem);
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
  border: none;
  border-radius: clamp(3px, 0.8vw, 5px);
  font-weight: 500;
  font-size: clamp(0.55rem, 1.1vw, 0.65rem);
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

.export-btn.sync {
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
}

.export-btn.sync:hover:not(:disabled) {
  background: rgba(33, 150, 243, 0.2);
}

.export-btn.sync:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.sort-btn svg {
  transition: transform 0.2s ease;
  flex-shrink: 0;
}

@keyframes slideInRight {
  0% { transform: translateX(30px); opacity: 0; }
  100% { transform: translateX(0); opacity: 1; }
}

.search-group {
  position: relative;
}

.search-input {
  width: 100%;
  padding: clamp(10px, 1.2vw, 12px) clamp(44px, 5vw, 48px) clamp(10px, 1.2vw, 12px) clamp(44px, 5vw, 48px);
  border: 1.5px solid rgba(76, 175, 80, 0.2);
  border-radius: 50px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  font-size: clamp(11px, 1.3vw, 12px);
  color: #2d3748;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-sizing: border-box;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.08), inset 0 1px 2px rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.search-input::placeholder {
  color: rgba(107, 114, 128, 0.6);
  font-weight: 400;
  font-size: clamp(10px, 1.2vw, 11px);
}

.search-input:focus {
  outline: none;
  border-color: #4CAF50;
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.18), 0 0 0 3px rgba(76, 175, 80, 0.1), inset 0 1px 2px rgba(255, 255, 255, 0.9);
  transform: translateY(-1px);
}

.search-input:hover {
  border-color: rgba(76, 175, 80, 0.4);
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.12), inset 0 1px 2px rgba(255, 255, 255, 0.9);
}

.search-icon {
  position: absolute;
  left: clamp(14px, 1.8vw, 16px);
  top: 50%;
  transform: translateY(-50%);
  color: rgba(76, 175, 80, 0.6);
  z-index: 1;
  width: clamp(14px, 2.2vw, 16px);
  height: clamp(14px, 2.2vw, 16px);
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

.usuarios-section {
  background: linear-gradient(135deg, #ffffff 0%, #fafffe 100%);
  border-radius: clamp(12px, 3vw, 20px);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.08),
    0 2px 16px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255,255,255,0.8);
  overflow: hidden;
  border: 1px solid rgba(76, 175, 80, 0.1);
  /* Eliminar transición para mejor rendimiento */
  padding: clamp(16px, 4vw, 24px);
  box-sizing: border-box;
  overflow-x: auto !important;
  width: 100% !important;
}

.usuarios-section:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 12px 40px rgba(0, 0, 0, 0.12),
    0 4px 20px rgba(0, 0, 0, 0.06),
    inset 0 1px 0 rgba(255,255,255,0.9);
}

.loading-container, .error-container, .empty-state {
  text-align: center;
  padding: clamp(40px, 10vh, 80px) clamp(16px, 4vw, 32px);
  color: #666;
  /* Eliminar animación fadeIn para mejor rendimiento */
}

.spinner-large {
  width: clamp(40px, 8vw, 48px);
  height: clamp(40px, 8vw, 48px);
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
  margin: 16px auto 0;
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
    0 8px 24px rgba(214, 51, 132, 0.5),
    0 4px 12px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
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
  overflow-x: auto !important;
  overflow-y: visible !important;
  border-radius: clamp(12px, 3vw, 16px);
  background: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
  width: 100% !important;
  max-width: none !important;
  box-sizing: border-box;
  display: block !important;
}

/* Estilos de scrollbar */
.table-container::-webkit-scrollbar {
  height: 8px;
}

.table-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.table-container::-webkit-scrollbar-thumb {
  background: #4CAF50;
  border-radius: 4px;
}

.table-container::-webkit-scrollbar-thumb:hover {
  background: #45a049;
}

.usuarios-table {
  width: 100%;
  min-width: 1200px !important;
  table-layout: fixed !important;
  border-collapse: collapse;
  position: relative;
  background: transparent;
  display: table !important;
  white-space: nowrap !important;
}

.usuarios-table th {
  background: linear-gradient(135deg, #f8f9fa 0%, #f0f8f0 100%);
  padding: clamp(6px, 1.2vw, 8px) clamp(3px, 0.8vw, 5px);
  text-align: center;
  font-weight: 700;
  color: #4CAF50;
  text-transform: uppercase;
  font-size: clamp(7px, 1.2vw, 8px);
  letter-spacing: 0.5px;
  border-bottom: 2px solid rgba(76, 175, 80, 0.2);
  position: sticky;
  top: 0;
  z-index: 10;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Headers específicos */
.usuarios-table th.col-id {
  min-width: 80px;
  font-size: clamp(7px, 1.2vw, 9px);
  padding: clamp(8px, 1.5vw, 12px) clamp(2px, 0.5vw, 4px);
}

.usuarios-table th.col-nombre {
  min-width: 140px;
  text-align: center;
  color: #4CAF50;
  font-weight: 700;
}

/* Anchos FIJOS específicos para cada columna */
.usuarios-table th.col-id { width: 55px; min-width: 55px; }
.usuarios-table th.col-nombre { width: 160px; min-width: 160px; }
.usuarios-table th.col-correo { width: 200px; min-width: 200px; }
.usuarios-table th.col-cargo { width: 180px; min-width: 180px; }
.usuarios-table th.col-supervisor { width: 150px; min-width: 150px; }
.usuarios-table th.col-curp { width: 145px; min-width: 145px; }
.usuarios-table th.col-territorio { width: 150px; min-width: 150px; }
.usuarios-table th.col-estado { width: 90px; min-width: 90px; }
.usuarios-table th.col-acciones { 
  width: 200px !important; 
  min-width: 200px !important;
  white-space: normal !important;
}
.usuarios-table td.col-acciones { 
  width: 200px !important; 
  min-width: 200px !important;
  white-space: normal !important;
}

.usuarios-table td {
  padding: clamp(6px, 1.2vw, 8px) clamp(4px, 0.8vw, 6px);
  border-bottom: 1px solid rgba(224, 224, 224, 0.6);
  font-size: clamp(9px, 1.5vw, 11px);
  color: #444;
  font-weight: 500;
  white-space: nowrap;
  vertical-align: middle;
  text-align: center;
}

/* Anchos mínimos simplificados para celdas */
.usuarios-table td.col-id { min-width: 55px; max-width: 55px; overflow: hidden; }  /* ID */
.usuarios-table td.col-nombre { 
  min-width: 160px; 
  max-width: 160px;
  text-align: left; 
  padding-left: clamp(8px, 2vw, 12px); 
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
} /* Nombre */
.usuarios-table td.col-correo { 
  min-width: 200px; 
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
} /* Correo */
.usuarios-table td.col-cargo { 
  min-width: 180px; 
  max-width: 180px;
  white-space: nowrap;
  overflow: visible;
  text-overflow: clip;
} /* Cargo */

/* Badges de cargo */
.cargo-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 9px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.cargo-emerald {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
}

.cargo-blue {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
}

.cargo-violet {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(139, 92, 246, 0.3);
}

.cargo-orange-light {
  background: linear-gradient(135deg, #fb923c 0%, #f97316 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(251, 146, 60, 0.3);
}

.cargo-orange {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(249, 115, 22, 0.3);
}

.cargo-red {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(239, 68, 68, 0.3);
}

.cargo-cyan {
  background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(6, 182, 212, 0.3);
}

.cargo-yellow {
  background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%);
  color: #422006;
  box-shadow: 0 2px 4px rgba(234, 179, 8, 0.3);
}

.cargo-gray {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(107, 114, 128, 0.3);
}

.cargo-empty {
  background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%);
  color: #6b7280;
  box-shadow: 0 2px 4px rgba(107, 114, 128, 0.15);
}

.cargo-badge:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.cargo-badge-detail {
  font-size: 10px;
  padding: 5px 12px;
}

.usuarios-table td.col-supervisor { 
  min-width: 150px; 
  max-width: 150px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
} /* Supervisor */
.usuarios-table td.col-curp { min-width: 145px; max-width: 145px; } /* CURP */
.usuarios-table td.col-territorio { 
  min-width: 150px; 
  max-width: 180px;
  white-space: normal !important;
  word-wrap: break-word;
  word-break: break-word;
  line-height: 1.3;
  vertical-align: middle;
} /* Territorio */
.usuarios-table td.col-estado { min-width: 90px; max-width: 90px; white-space: nowrap !important; } /* Estado */
.usuarios-table td.col-acciones { min-width: 200px; } /* Acciones */

/* Estilos para columna CURP */
.col-curp {
  width: 140px;
  text-align: center;
}

.curp-text {
  display: inline-block;
  font-family: 'Courier New', monospace;
  font-size: clamp(8px, 1.3vw, 10px);
  font-weight: 600;
  color: #555;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  background: rgba(100, 100, 100, 0.08);
  padding: 2px 6px;
  border-radius: 4px;
}

/* Estilos para columna Territorio */
.col-territorio {
  width: 150px;
  min-width: 150px;
  max-width: 180px;
  text-align: center;
  white-space: normal !important;
  word-wrap: break-word;
  word-break: break-word;
  line-height: 1.4;
}

.territorio-text {
  display: inline-block;
  font-size: clamp(8px, 1.3vw, 10px);
  font-weight: 600;
  color: #1565C0;
  background: rgba(21, 101, 192, 0.1);
  padding: 4px 8px;
  border-radius: 4px;
  white-space: normal !important;
  word-wrap: break-word;
  word-break: break-word;
  line-height: 1.3;
  max-width: 100%;
}

/* ===== Columna Estado ===== */
.col-estado {
  width: 90px;
  min-width: 90px;
  max-width: 90px;
  text-align: center;
  white-space: nowrap !important;
  overflow: visible;
}

.estado-badge-cell {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 50px;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.4px;
  text-transform: capitalize;
  white-space: nowrap;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  transition: all 0.2s ease;
}

.estado-badge-cell .estado-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
  animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.15); opacity: 0.85; }
}

.estado-activo {
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  color: #2e7d32;
  border: 1px solid rgba(76, 175, 80, 0.3);
}
.estado-activo .estado-dot {
  background: linear-gradient(135deg, #66bb6a, #43a047);
  box-shadow: 0 0 8px rgba(76, 175, 80, 0.7), inset 0 1px 2px rgba(255,255,255,0.4);
}
.estado-activo:hover {
  background: linear-gradient(135deg, #c8e6c9 0%, #a5d6a7 100%);
  box-shadow: 0 3px 10px rgba(76, 175, 80, 0.25);
}

.estado-inactivo {
  background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
  color: #c62828;
  border: 1px solid rgba(244, 67, 54, 0.25);
}
.estado-inactivo .estado-dot {
  background: linear-gradient(135deg, #ef5350, #d32f2f);
  box-shadow: 0 0 8px rgba(244, 67, 54, 0.5), inset 0 1px 2px rgba(255,255,255,0.3);
  animation: none;
}
.estado-inactivo:hover {
  background: linear-gradient(135deg, #ffcdd2 0%, #ef9a9a 100%);
  box-shadow: 0 3px 10px rgba(244, 67, 54, 0.2);
}

/* ===== Fila de usuario inactivo (apagado) ===== */
.fila-inactiva {
  background: linear-gradient(90deg, #e8e8e8 0%, #f0f0f0 50%, #e8e8e8 100%) !important;
  transition: all 0.3s ease;
}
.fila-inactiva:hover {
  background: linear-gradient(90deg, #ddd 0%, #e5e5e5 50%, #ddd 100%) !important;
}
.fila-inactiva td {
  color: #888 !important;
  border-bottom-color: #ccc !important;
  opacity: 0.7;
}
.fila-inactiva .nombre-normal,
.fila-inactiva .curp-text,
.fila-inactiva .territorio-text,
.fila-inactiva .territorio-empty {
  color: #888 !important;
  background: rgba(150, 150, 150, 0.15) !important;
}
.fila-inactiva .estado-badge-cell {
  background: rgba(120, 120, 120, 0.2) !important;
  color: #777 !important;
}
.fila-inactiva .estado-dot {
  background: #999 !important;
  box-shadow: none !important;
}
.fila-inactiva .btn-ver,
.fila-inactiva .btn-editar,
.fila-inactiva .btn-eliminar {
  opacity: 0.5;
}
.fila-inactiva .btn-activar {
  opacity: 1 !important;
}

/* Estilo para territorio vacío */
.territorio-empty {
  display: inline-block;
  font-size: clamp(8px, 1.3vw, 10px);
  font-weight: 400;
  font-style: italic;
  color: #9e9e9e;
  padding: 2px 8px;
}

/* Estilos específicos para columnas */
.col-id {
  width: 80px;
  font-family: 'Courier New', monospace;
  font-weight: 700;
  color: #666;
  font-size: clamp(9px, 1.5vw, 11px) !important;
}

.col-nombre {
  width: 160px;
  min-width: 160px;
  text-align: left !important;
  padding-left: clamp(8px, 2vw, 12px) !important;
}

/* Estilo simple para el nombre (sin animaciones) */
.nombre-normal {
  display: block;
  color: #2E7D32;
  font-weight: 600;
  font-size: clamp(9px, 1.6vw, 11px);
  white-space: normal;
  word-wrap: break-word;
  line-height: 1.3;
}

.usuarios-table tbody tr {
  position: relative;
}

.usuarios-table tbody tr:hover {
  background-color: rgba(76, 175, 80, 0.05);
}

.usuarios-table tbody tr:hover td {
  border-bottom-color: rgba(76, 175, 80, 0.2);
}

.status-badge {
  padding: clamp(2px, 0.4vw, 3px) clamp(4px, 1vw, 6px);
  border-radius: clamp(6px, 1.5vw, 9px);
  font-size: clamp(6px, 1.2vw, 7px);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  transition: all 0.3s ease;
  display: inline-block;
  position: relative;
  overflow: hidden;
  white-space: nowrap;
  min-width: clamp(28px, 5.5vw, 40px);
  text-align: center;
  max-width: 100%;
}

.status-badge::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  transition: left 0.5s ease;
}

.status-badge:hover::before {
  left: 100%;
}

.status-badge.active {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  color: #155724;
  border: 1px solid rgba(21, 87, 36, 0.2);
  box-shadow: 0 2px 6px rgba(21, 87, 36, 0.2);
}

.status-badge.active:hover {
  background: linear-gradient(135deg, #c3e6cb 0%, #b1dfbb 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(21, 87, 36, 0.3);
}

.status-badge.inactive {
  background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
  color: #721c24;
  border: 1px solid rgba(114, 28, 36, 0.2);
  box-shadow: 0 2px 6px rgba(114, 28, 36, 0.2);
}

.btn-ver {
  width: clamp(24px, 4.5vw, 28px) !important;
  height: clamp(24px, 4.5vw, 28px) !important;
  min-width: clamp(24px, 4.5vw, 28px) !important;
  min-height: clamp(24px, 4.5vw, 28px) !important;
  padding: 0;
  background: linear-gradient(135deg, #4CAF50, #43A047);
  color: white;
  border: none;
  border-radius: 50% !important;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.25);
  position: relative;
  overflow: hidden;
  display: flex !important;
  align-items: center;
  justify-content: center;
  flex-shrink: 0 !important;
  white-space: normal !important;
}

.btn-ver::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
  transition: left 0.5s ease;
}

.btn-ver:hover::before {
  left: 100%;
}

.btn-ver:hover {
  background: linear-gradient(135deg, #43A047, #388E3C);
  transform: translateY(-2px) scale(1.1);
  box-shadow: 
    0 6px 16px rgba(76, 175, 80, 0.4),
    0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-ver:active {
  transform: translateY(-1px) scale(1.05);
  box-shadow: 0 3px 10px rgba(76, 175, 80, 0.3);
}

.btn-ver svg {
  width: clamp(12px, 2.5vw, 14px);
  height: clamp(12px, 2.5vw, 14px);
  transition: all 0.3s ease;
}

.btn-ver:hover svg {
  transform: scale(1.1);
}

/* Estilos para contenedores de acciones */
.actions-container {
  display: flex !important;
  gap: 12px;
  align-items: center;
  justify-content: center;
  white-space: normal !important;
  flex-shrink: 0 !important;
}

/* Contenedor de acción individual */
.action-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 8px 0;
}

/* Estilos para el botón de eliminar */
.btn-eliminar {
  width: clamp(24px, 4.5vw, 28px) !important;
  height: clamp(24px, 4.5vw, 28px) !important;
  min-width: clamp(24px, 4.5vw, 28px) !important;
  min-height: clamp(24px, 4.5vw, 28px) !important;
  padding: 0;
  background: linear-gradient(135deg, #f44336, #d32f2f);
  color: white;
  border: none;
  border-radius: 50% !important;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 2px 8px rgba(244, 67, 54, 0.25);
  position: relative;
  overflow: hidden;
  display: flex !important;
  align-items: center;
  justify-content: center;
  flex-shrink: 0 !important;
  white-space: normal !important;
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
  background: linear-gradient(135deg, #d32f2f, #b71c1c);
  transform: translateY(-2px) scale(1.1);
  box-shadow: 
    0 6px 16px rgba(244, 67, 54, 0.4),
    0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-eliminar:active {
  transform: translateY(-1px) scale(1.05);
  box-shadow: 0 3px 10px rgba(244, 67, 54, 0.3);
}

.btn-eliminar svg {
  width: clamp(12px, 2.5vw, 14px);
  height: clamp(12px, 2.5vw, 14px);
  transition: all 0.3s ease;
}

.btn-eliminar:hover svg {
  transform: scale(1.1);
}

/* Estilos para el botón de toggle (activar/desactivar) */
.btn-toggle {
  width: clamp(24px, 4.5vw, 28px) !important;
  height: clamp(24px, 4.5vw, 28px) !important;
  min-width: clamp(24px, 4.5vw, 28px) !important;
  min-height: clamp(24px, 4.5vw, 28px) !important;
  padding: 0;
  color: white;
  border: none;
  border-radius: 50% !important;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
  display: flex !important;
  align-items: center;
  justify-content: center;
  flex-shrink: 0 !important;
  white-space: normal !important;
}

.btn-desactivar {
  background: linear-gradient(135deg, #9e9e9e, #757575);
  box-shadow: 0 2px 8px rgba(158, 158, 158, 0.25);
}

.btn-desactivar:hover {
  background: linear-gradient(135deg, #757575, #616161);
  transform: translateY(-2px) scale(1.1);
  box-shadow: 
    0 6px 16px rgba(158, 158, 158, 0.4),
    0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-activar {
  background: linear-gradient(135deg, #4CAF50, #388E3C);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.25);
}

.btn-activar:hover {
  background: linear-gradient(135deg, #388E3C, #2E7D32);
  transform: translateY(-2px) scale(1.1);
  box-shadow: 
    0 6px 16px rgba(76, 175, 80, 0.4),
    0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-toggle::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
  transition: left 0.5s ease;
}

.btn-toggle:hover::before {
  left: 100%;
}

.btn-toggle:active {
  transform: translateY(-1px) scale(1.05);
}

.btn-toggle svg {
  width: clamp(12px, 2.5vw, 14px);
  height: clamp(12px, 2.5vw, 14px);
  transition: all 0.3s ease;
}

.btn-toggle:hover svg {
  transform: scale(1.1);
}


/* Estilos para el botón de editar */
.btn-editar {
  width: clamp(24px, 4.5vw, 28px) !important;
  height: clamp(24px, 4.5vw, 28px) !important;
  min-width: clamp(24px, 4.5vw, 28px) !important;
  min-height: clamp(24px, 4.5vw, 28px) !important;
  padding: 0;
  background: linear-gradient(135deg, #ff9800, #f57c00);
  color: white;
  border: none;
  border-radius: 50% !important;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 2px 8px rgba(255, 152, 0, 0.25);
  position: relative;
  overflow: hidden;
  display: flex !important;
  align-items: center;
  justify-content: center;
  flex-shrink: 0 !important;
  white-space: normal !important;
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

.btn-editar:hover {
  background: linear-gradient(135deg, #f57c00, #e65100);
  transform: translateY(-2px) scale(1.1);
  box-shadow: 
    0 6px 16px rgba(255, 152, 0, 0.4),
    0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-editar:active {
  transform: translateY(-1px) scale(1.05);
  box-shadow: 0 3px 10px rgba(255, 152, 0, 0.3);
}

.btn-editar svg {
  width: clamp(12px, 2.5vw, 14px);
  height: clamp(12px, 2.5vw, 14px);
  transition: all 0.3s ease;
}

.btn-editar:hover svg {
  transform: scale(1.1);
}

/* Label para botón ver/detalles (verde) */
.btn-label {
  font-size: 10px;
  color: #4CAF50;
  font-weight: 600;
  letter-spacing: 0.5px;
  margin-top: 2px;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.action-container:hover .btn-label {
  opacity: 1;
  color: #43A047;
}

/* Label para botón eliminar (rojo) */
.btn-label-eliminar {
  font-size: 10px;
  color: #f44336;
  font-weight: 600;
  letter-spacing: 0.5px;
  margin-top: 2px;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.action-container:hover .btn-label-eliminar {
  opacity: 1;
  color: #d32f2f;
}

/* Label para botón editar (naranja) */
.btn-label-editar {
  font-size: 10px;
  color: #ff9800;
  font-weight: 600;
  letter-spacing: 0.5px;
  margin-top: 2px;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.action-container:hover .btn-label-editar {
  opacity: 1;
  color: #f57c00;
}

/* Label para botón desactivar (gris) */
.btn-label-desactivar {
  font-size: 10px;
  color: #9e9e9e;
  font-weight: 600;
  letter-spacing: 0.5px;
  margin-top: 2px;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.action-container:hover .btn-label-desactivar {
  opacity: 1;
  color: #757575;
}

/* Label para botón activar (verde) */
.btn-label-activar {
  font-size: 10px;
  color: #4CAF50;
  font-weight: 600;
  letter-spacing: 0.5px;
  margin-top: 2px;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.action-container:hover .btn-label-activar {
  opacity: 1;
  color: #388E3C;
}

/* ========== ESTILOS PARA BOTONES BLOQUEADOS ========== */
.btn-bloqueado {
  background: linear-gradient(135deg, #e0e0e0 0%, #bdbdbd 100%) !important;
  border: 2px solid #9e9e9e !important;
  color: #757575 !important;
  cursor: not-allowed !important;
  opacity: 0.7;
  box-shadow: none !important;
  transform: none !important;
  position: relative;
}

.btn-bloqueado::before {
  display: none !important;
}

.btn-bloqueado:hover {
  transform: none !important;
  box-shadow: none !important;
  background: linear-gradient(135deg, #e0e0e0 0%, #bdbdbd 100%) !important;
}

.btn-bloqueado:active {
  transform: none !important;
}

.btn-bloqueado svg {
  color: #757575 !important;
  stroke: #757575 !important;
  filter: none !important;
}

.btn-bloqueado:hover svg {
  transform: none !important;
}

/* Label bloqueado */
.label-bloqueado {
  color: #9e9e9e !important;
  font-style: italic;
}

.action-container:hover .label-bloqueado {
  color: #757575 !important;
}

/* Estilos para el modal de eliminación */
.delete-modal {
  max-width: 500px !important;
}

.delete-header {
  background: linear-gradient(135deg, #ffebee, #fce4ec);
  border-bottom: 2px solid #f44336;
}

.delete-icon {
  background: linear-gradient(135deg, #f44336, #d32f2f);
  color: white;
}

.delete-confirmation {
  text-align: center;
  padding: 20px 0;
}

.warning-icon {
  margin: 0 auto 20px;
  display: flex;
  justify-content: center;
}

.delete-confirmation h4 {
  color: #333;
  margin-bottom: 20px;
  font-size: 18px;
  font-weight: 600;
}

.user-info-delete {
  background: #f9f9f9;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 15px;
  margin: 20px 0;
  text-align: left;
}

.user-info-delete p {
  margin: 5px 0;
  font-size: 14px;
  color: #555;
}

.warning-text {
  color: #f44336;
  font-size: 14px;
  line-height: 1.5;
  margin-top: 15px;
  padding: 10px;
  background: #ffebee;
  border-radius: 6px;
  border-left: 4px solid #f44336;
}

.modal-footer-delete {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding: 20px;
  border-top: 1px solid #e0e0e0;
  background: #f8f9fa;
}

.btn-cancel {
  background: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-cancel:hover {
  background: #5a6268;
  transform: translateY(-1px);
}

.btn-delete {
  background: linear-gradient(135deg, #f44336, #d32f2f);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-delete:hover:not(:disabled) {
  background: linear-gradient(135deg, #d32f2f, #b71c1c);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.3);
}

.btn-delete:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.spinner-small {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Estilos para el modal compacto de cambio de estado */
.estado-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 16px;
}

.estado-box {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 380px;
  padding: 32px 28px 24px;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  position: relative;
}

.estado-icon-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.icon-green {
  background: linear-gradient(135deg, #4CAF50, #2e7d32);
  box-shadow: 0 4px 14px rgba(76, 175, 80, 0.35);
}

.icon-orange {
  background: linear-gradient(135deg, #ff9800, #e65100);
  box-shadow: 0 4px 14px rgba(255, 152, 0, 0.35);
}

.estado-titulo {
  font-size: 1.15rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 16px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.estado-user-card {
  background: #f8f9fb;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 14px;
  margin-bottom: 14px;
}

.estado-user-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 4px;
}

.estado-user-email {
  font-size: 0.8rem;
  color: #6b7280;
  margin: 0 0 10px;
}

.estado-badge {
  display: inline-block;
  padding: 3px 12px;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-active {
  background: #dcfce7;
  color: #16a34a;
}

.badge-inactive {
  background: #f3f4f6;
  color: #6b7280;
}

.estado-msg {
  font-size: 0.82rem;
  line-height: 1.5;
  margin: 0 0 20px;
  padding: 10px 14px;
  border-radius: 8px;
}

.msg-green {
  background: #f0fdf4;
  color: #15803d;
  border-left: 3px solid #4CAF50;
}

.msg-orange {
  background: #fff7ed;
  color: #c2410c;
  border-left: 3px solid #ff9800;
}

.estado-actions {
  display: flex;
  gap: 10px;
}

.estado-btn-cancel {
  flex: 1;
  padding: 10px;
  border: 1.5px solid #d1d5db;
  background: white;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s;
}

.estado-btn-cancel:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.estado-btn-confirm {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.btn-green {
  background: linear-gradient(135deg, #4CAF50, #2e7d32);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
}

.btn-green:hover:not(:disabled) {
  box-shadow: 0 4px 14px rgba(76, 175, 80, 0.45);
  transform: translateY(-1px);
}

.btn-orange {
  background: linear-gradient(135deg, #ff9800, #e65100);
  box-shadow: 0 2px 8px rgba(255, 152, 0, 0.3);
}

.btn-orange:hover:not(:disabled) {
  box-shadow: 0 4px 14px rgba(255, 152, 0, 0.45);
  transform: translateY(-1px);
}

.estado-btn-confirm:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Transiciones del modal estado */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.pop-enter-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.pop-leave-active {
  transition: all 0.2s ease-in;
}
.pop-enter-from {
  opacity: 0;
  transform: scale(0.9);
}
.pop-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

@media (max-width: 480px) {
  .estado-box {
    max-width: 95vw;
    padding: 24px 20px 20px;
  }
  
  .estado-actions {
    flex-direction: column-reverse;
  }
}

/* Estilos para el modal de edición */
.edit-modal {
  max-width: 600px !important;
}

.edit-header {
  background: linear-gradient(135deg, #fff8e1, #ffecb3);
  border-bottom: 2px solid #ff9800;
}

.edit-icon {
  background: linear-gradient(135deg, #ff9800, #f57c00);
  color: white;
}

/* Modal de edición - Estilo completamente rediseñado */
.edit-modal {
  max-width: 680px !important;
  max-height: 92vh !important;
  width: 92vw !important;
}

.edit-modal .modal-header-modern {
  padding: 18px 24px;
}

.edit-modal .modal-body-modern {
  padding: 24px;
  overflow-y: auto;
  max-height: calc(92vh - 150px);
}

.edit-form {
  width: 100%;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px 24px;
  width: 100%;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  color: #374151;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-group label::before {
  content: '';
  width: 3px;
  height: 16px;
  background: linear-gradient(135deg, #ff9800, #f57c00);
  border-radius: 2px;
  flex-shrink: 0;
}

.form-input {
  width: 100% !important;
  padding: 14px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 15px;
  transition: all 0.2s ease;
  background: #f9fafb;
  color: #1f2937;
  box-sizing: border-box;
}

.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  background-size: 18px;
  padding-right: 48px !important;
  cursor: pointer;
  background-color: #f9fafb;
  width: 100% !important;
}

.form-select:focus {
  background-color: white;
}

.form-input:focus {
  outline: none;
  border-color: #ff9800;
  box-shadow: 0 0 0 4px rgba(255, 152, 0, 0.12);
  background: white;
}

.form-input:hover:not(:focus) {
  border-color: #d1d5db;
  background: white;
}

.form-input::placeholder {
  color: #9ca3af;
  font-style: normal;
  font-weight: 400;
}

/* Estilos para el campo de contraseña en el modal de edición */
.password-field-container {
  position: relative;
  width: 100% !important;
}

.password-field-container .form-input {
  width: 100% !important;
  padding-right: 52px !important;
}

.password-toggle-btn-edit {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, #4CAF50, #45a049);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 2px 6px rgba(76, 175, 80, 0.3);
  z-index: 2;
}

.password-toggle-btn-edit:hover {
  background: linear-gradient(135deg, #45a049, #3d8b40);
  transform: translateY(-50%) scale(1.05);
  box-shadow: 0 3px 9px rgba(76, 175, 80, 0.4);
}

.password-toggle-btn-edit:active {
  transform: translateY(-50%) scale(1.02);
}

.password-toggle-btn-edit svg {
  width: 14px;
  height: 14px;
}

.modal-footer-edit {
  display: flex;
  justify-content: flex-end;
  gap: clamp(10px, 2vw, 14px);
  padding: clamp(14px, 3vw, 20px) clamp(16px, 3vw, 24px);
  background: linear-gradient(135deg, #f8f9fa 0%, #f1f3f4 100%);
  border-top: 2px solid #e9ecef;
  flex-shrink: 0;
}

.btn-cancel {
  background: white;
  color: #6b7280;
  border: 2px solid #e5e7eb;
  padding: clamp(10px, 2vw, 12px) clamp(18px, 3vw, 24px);
  border-radius: 10px;
  cursor: pointer;
  font-size: clamp(13px, 2.5vw, 15px);
  font-weight: 600;
  transition: all 0.25s ease;
}

.btn-cancel:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
  color: #374151;
}

.btn-save {
  background: linear-gradient(135deg, #ff9800, #f57c00);
  color: white;
  border: none;
  padding: clamp(10px, 2vw, 12px) clamp(18px, 3vw, 24px);
  border-radius: 10px;
  cursor: pointer;
  font-size: clamp(13px, 2.5vw, 15px);
  font-weight: 600;
  transition: all 0.25s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(255, 152, 0, 0.25);
}

.btn-save:hover:not(:disabled) {
  background: linear-gradient(135deg, #f57c00, #e65100);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(255, 152, 0, 0.35);
}

.btn-save:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Modal Moderno - Diseño Responsivo */
.modal-overlay-modern {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: clamp(12px, 3vw, 20px);
  backdrop-filter: blur(4px); /* Reducir la intensidad del filtro blur */
  /* Eliminar animación */
}

.modal-content-modern {
  background: linear-gradient(135deg, #ffffff 0%, #fdfdfd 100%);
  border-radius: clamp(16px, 2.5vw, 24px);
  max-width: clamp(320px, 90vw, 480px);
  max-height: 90vh; /* Aumentar altura máxima para aprovechar más espacio en pantalla */
  width: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column; /* Organizar contenido en columna para permitir scroll correcto */
  box-shadow: 
    0 25px 80px rgba(0, 0, 0, 0.15),
    0 10px 40px rgba(0, 0, 0, 0.08);
  border: 2px solid rgba(76, 175, 80, 0.08);
  /* Eliminar animación costosa */
}

.modal-header-modern {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: clamp(12px, 3vw, 18px) clamp(16px, 4vw, 24px);
  border-bottom: 2px solid rgba(76, 175, 80, 0.1);
  background: linear-gradient(135deg, 
    rgba(76, 175, 80, 0.05) 0%, 
    rgba(76, 175, 80, 0.02) 100%);
  flex-shrink: 0; /* Evita que el encabezado se encoja cuando hay scroll */
}

.modal-title-section {
  display: flex;
  align-items: center;
  gap: clamp(8px, 2vw, 12px);
}

.modal-icon {
  width: clamp(28px, 6vw, 36px);
  height: clamp(28px, 6vw, 36px);
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.modal-title {
  font-size: clamp(14px, 3.5vw, 18px);
  font-weight: 700;
  color: #2E7D32;
  margin: 0;
  letter-spacing: 0.3px;
}

.btn-close-modern {
  width: clamp(28px, 6vw, 32px);
  height: clamp(28px, 6vw, 32px);
  background: rgba(244, 67, 54, 0.1);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #F44336;
}

.btn-close-modern:hover {
  background: rgba(244, 67, 54, 0.2);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.3);
}

.modal-body-modern {
  padding: clamp(8px, 2vw, 12px) clamp(16px, 4vw, 24px) clamp(16px, 4vw, 24px);
  flex: 1; /* Toma el espacio restante en el contenedor flex */
  overflow-y: auto; /* Scroll vertical automático */
  overscroll-behavior: contain; /* Mejora el comportamiento del scroll */
  font-size: 14px; /* Reducir tamaño de fuente para mejor visualización */
  min-height: 0; /* Fuerza el scroll en contenedor flex */
}

.modal-body-modern::-webkit-scrollbar {
  width: 8px; /* Ancho más grande para mejor visibilidad y usabilidad */
  height: 8px;
}

.modal-body-modern::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
  margin: 2px 0;
}

.modal-body-modern::-webkit-scrollbar-thumb {
  background: #4CAF50;
  border-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.user-details-grid {
  display: grid;
  gap: clamp(6px, 1.5vw, 10px);
  padding-right: 4px; /* Espacio para el scrollbar */
  overflow-anchor: none; /* Mejora el comportamiento del scroll */
}

.detail-card {
  background: linear-gradient(135deg, 
    rgba(248, 255, 254, 0.6) 0%, 
    rgba(240, 255, 240, 0.4) 100%);
  border: 1px solid rgba(76, 175, 80, 0.15);
  border-radius: clamp(6px, 1.5vw, 10px);
  padding: clamp(6px, 1.5vw, 10px) clamp(8px, 2vw, 12px);
  display: flex;
  align-items: flex-start;
  gap: clamp(4px, 1vw, 8px);
  transition: all 0.3s ease;
  margin-bottom: 6px; /* Espacio reducido entre tarjetas */
}

.detail-card:hover {
  background: linear-gradient(135deg, 
    rgba(240, 255, 240, 0.8) 0%, 
    rgba(232, 245, 232, 0.6) 100%);
  border-color: rgba(76, 175, 80, 0.25);
  transform: translateX(2px);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.1);
}

.detail-icon {
  width: clamp(24px, 5vw, 28px);
  height: clamp(24px, 5vw, 28px);
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.15), rgba(76, 175, 80, 0.1));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4CAF50;
  flex-shrink: 0;
  margin-top: 2px;
}

.status-icon {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.2), rgba(76, 175, 80, 0.15));
}

.detail-content {
  flex: 1;
  min-width: 0;
}

.detail-label {
  display: block;
  font-size: clamp(8px, 1.8vw, 10px);
  font-weight: 600;
  color: #4CAF50;
  text-transform: uppercase;
  letter-spacing: 0.2px;
  margin-bottom: 2px;
}

.detail-value {
  display: block;
  font-size: clamp(10px, 2vw, 12px);
  font-weight: 500;
  color: #2E7D32;
  line-height: 1.2;
  word-break: break-word;
}

.status-active {
  color: #4CAF50 !important;
  font-weight: 600;
}

/* Estilo especial para el campo de teléfono */
.phone-value {
  font-family: 'Courier New', monospace;
  letter-spacing: 0.5px;
  color: #0277BD;
  font-weight: 600; /* Más legible */
  white-space: nowrap; /* Evitar saltos de línea en el número */
  font-size: clamp(10px, 2vw, 12px); /* Tamaño consistente */
}

/* Estilo especial para el campo de territorio */
.territorio-icon {
  background: linear-gradient(135deg, rgba(21, 101, 192, 0.15), rgba(21, 101, 192, 0.1)) !important;
  color: #1565C0 !important;
}

.territorio-value {
  color: #1565C0 !important;
  font-weight: 600;
}

.territorio-empty-detail {
  color: #9e9e9e !important;
  font-style: italic;
  font-weight: 400;
}

/* Estilos especiales para el campo de contraseña */
.password-card {
  border-color: rgba(255, 87, 34, 0.2);
  background: linear-gradient(135deg, 
    rgba(255, 243, 224, 0.4) 0%, 
    rgba(255, 248, 225, 0.3) 100%);
}

.password-card:hover {
  border-color: rgba(255, 87, 34, 0.3);
  background: linear-gradient(135deg, 
    rgba(255, 243, 224, 0.6) 0%, 
    rgba(255, 248, 225, 0.5) 100%);
}

.password-card .detail-icon {
  background: linear-gradient(135deg, rgba(255, 87, 34, 0.15), rgba(255, 87, 34, 0.1));
  color: #FF5722;
}

.password-content {
  width: 100%;
}

.password-display {
  display: flex;
  align-items: center;
  gap: clamp(6px, 1.5vw, 8px);
  margin-top: clamp(4px, 1vw, 6px);
}

.password-value {
  font-family: 'Courier New', 'Monaco', monospace;
  font-size: clamp(10px, 2.2vw, 12px);
  font-weight: 600;
  color: #FF5722;
  background: rgba(255, 255, 255, 0.8);
  padding: clamp(4px, 1vw, 6px) clamp(6px, 1.5vw, 8px);
  border-radius: clamp(4px, 1vw, 6px);
  border: 1px solid rgba(255, 87, 34, 0.2);
  flex: 1;
  min-width: 0;
  word-break: break-all;
}

.password-toggle-btn {
  width: clamp(22px, 4.5vw, 26px);
  height: clamp(22px, 4.5vw, 26px);
  background: linear-gradient(135deg, #FF5722, #FF7043);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 2px 6px rgba(255, 87, 34, 0.3);
}

.password-toggle-btn:hover {
  background: linear-gradient(135deg, #E64A19, #FF5722);
  transform: scale(1.1);
  box-shadow: 0 3px 9px rgba(255, 87, 34, 0.4);
}

.password-toggle-btn:active {
  transform: scale(1.05);
}

.modal-header h3 {
  margin: 0;
  color: #333;
  font-size: clamp(16px, 4vw, 20px);
  font-weight: 700;
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.btn-close {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 2px solid rgba(76, 175, 80, 0.2);
  font-size: clamp(16px, 4vw, 20px);
  cursor: pointer;
  color: #666;
  padding: clamp(6px, 1.5vw, 8px);
  width: clamp(30px, 8vw, 36px);
  height: clamp(30px, 8vw, 36px);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  font-weight: 700;
}

.btn-close:hover {
  background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
  border-color: #4CAF50;
  color: #4CAF50;
  transform: scale(1.1) rotate(90deg);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2);
}

.modal-body {
  padding: clamp(16px, 4vw, 24px) clamp(20px, 5vw, 28px);
  overflow: auto;
  max-height: calc(80vh - clamp(80px, 20vw, 120px));
}

.usuario-detalles div {
  margin-bottom: 16px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #f8fffe 0%, #f0fff0 100%);
  border-radius: 12px;
  border-left: 4px solid #4CAF50;
  transition: all 0.3s ease;
}

.usuario-detalles div:hover {
  background: linear-gradient(135deg, #f0fff0 0%, #e8f5e8 100%);
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.1);
}

.usuario-detalles div:last-child {
  margin-bottom: 0;
}

.usuario-detalles strong {
  color: #4CAF50;
  font-weight: 700;
  display: block;
  margin-bottom: 4px;
  text-transform: uppercase;
  font-size: 11px;
  letter-spacing: 0.5px;
}

/* Estilos para el campo de contraseña */
.detalle-item {
  margin-bottom: 16px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #f8fffe 0%, #f0fff0 100%);
  border-radius: 12px;
  border-left: 4px solid #4CAF50;
  transition: all 0.3s ease;
}

.detalle-item:hover {
  background: linear-gradient(135deg, #f0fff0 0%, #e8f5e8 100%);
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.1);
}

.detalle-item:last-child {
  margin-bottom: 0;
}

.password-field {
  border-left-color: #FF5722;
}

.password-container {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
}

.password-text {
  font-family: 'Courier New', monospace;
  background: rgba(255, 255, 255, 0.7);
  padding: 8px 12px;
  border-radius: 8px;
  border: 2px solid rgba(76, 175, 80, 0.2);
  font-size: 14px;
  font-weight: 600;
  color: #2E7D32;
  letter-spacing: 1px;
  flex: 1;
  transition: all 0.3s ease;
}

.toggle-password-btn {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  border: none;
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
}

.toggle-password-btn:hover {
  background: linear-gradient(135deg, #43A047, #4CAF50);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
}

.toggle-password-btn:active {
  transform: translateY(0);
  box-shadow: 0 1px 4px rgba(76, 175, 80, 0.3);
}

.estado-activo {
  color: #4CAF50;
  font-weight: 600;
  background: rgba(76, 175, 80, 0.1);
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
}

/* Estilos de Paginación */
.pagination-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 16px;
  border: 1px solid rgba(76, 175, 80, 0.1);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.08);
  animation: fadeInUp 0.4s ease-out;
}

.pagination-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.pagination-text {
  color: #4b5563;
  font-size: 0.9rem;
  font-weight: 500;
}

.pagination-text strong {
  color: #4CAF50;
  font-weight: 700;
}

.pagination-selector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.pagination-label {
  color: #6b7280;
  font-size: 0.85rem;
  font-weight: 500;
  white-space: nowrap;
}

.pagination-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid rgba(209, 213, 219, 0.6);
  border-radius: 8px;
  background: white;
  color: #374151;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 70px;
}

.pagination-select:hover {
  border-color: rgba(76, 175, 80, 0.4);
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
}

.pagination-select:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.15);
}

.pagination-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  flex-wrap: wrap;
}

.pagination-btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.625rem 1rem;
  background: white;
  border: 1px solid rgba(209, 213, 219, 0.6);
  border-radius: 10px;
  color: #6b7280;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  user-select: none;
  min-height: 44px;
}

.pagination-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(76, 175, 80, 0.1), transparent);
  transition: left 0.5s ease;
}

.pagination-btn:hover:not(:disabled)::before {
  left: 100%;
}

.pagination-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
  border-color: #4CAF50;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.3);
}

.pagination-btn:active:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(76, 175, 80, 0.3);
}

.pagination-btn:disabled {
  background: #f9fafb;
  color: #d1d5db;
  cursor: not-allowed;
  border-color: #e5e7eb;
}

.pagination-btn-text {
  font-weight: 600;
  letter-spacing: 0.025em;
}

.pagination-first,
.pagination-last {
  padding: 0.625rem 0.75rem;
}

.pagination-numbers {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  margin: 0 0.5rem;
  flex-wrap: wrap;
  justify-content: center;
}

.pagination-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  padding: 0;
  background: white;
  border: 1px solid rgba(209, 213, 219, 0.6);
  border-radius: 12px;
  color: #6b7280;
  font-size: 0.875rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  user-select: none;
}

.pagination-number::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(76, 175, 80, 0.15), transparent);
  transition: left 0.4s ease;
}

.pagination-number:hover:not(.active)::before {
  left: 100%;
}

.pagination-number:hover:not(.active) {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(76, 175, 80, 0.05) 100%);
  border-color: rgba(76, 175, 80, 0.4);
  color: #4CAF50;
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.2);
}

.pagination-number.active {
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
  border-color: #4CAF50;
  color: white;
  transform: translateY(-2px);
  box-shadow: 
    0 8px 25px rgba(76, 175, 80, 0.4),
    0 3px 10px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  cursor: default;
}

.pagination-ellipsis {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  color: #9ca3af;
  font-size: 1.25rem;
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

/* ====================== APPLE RESPONSIVE 1024px ====================== */
@media (max-width: 1024px) {
  .apple-sticky-wrapper {
    margin-bottom: 16px;
  }
  
  .apple-content-wrapper {
    padding: 24px 24px;
  }
  
  .apple-stats-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
  }
  
  .apple-stat-card {
    padding: 12px;
  }
  
  .apple-stat-icon {
    width: 32px;
    height: 32px;
  }
  
  .apple-stat-value {
    font-size: 16px;
  }
  
  .apple-unified-filters {
    gap: 12px;
  }
  
  /* Apple Table Responsive 1024px */
  .apple-table-container {
    max-height: calc(100vh - 380px);
    border-radius: 16px;
  }
  
  .apple-table th,
  .apple-table td {
    padding: 12px 14px;
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
  
  .apple-action-btn {
    width: 30px;
    height: 30px;
  }
  
  .apple-action-btn svg {
    width: 13px;
    height: 13px;
  }
}

/* ====================== APPLE RESPONSIVE 768px ====================== */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    width: 100%;
    padding: 8px;
  }
  
  .apple-sticky-wrapper {
    margin-bottom: 12px;
  }
  
  .apple-page-header {
    border-radius: 20px 20px 0 0;
    padding: 8px 12px;
  }
  
  .apple-header-wrapper {
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
    border-radius: 0 0 20px 20px;
    padding: 14px 12px 12px 12px;
  }
  
  .apple-stats-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
  }
  
  .apple-stat-card {
    padding: 10px;
    border-radius: 12px;
    flex-direction: column;
    text-align: center;
    gap: 6px;
  }
  
  .apple-stat-icon {
    width: 28px;
    height: 28px;
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
    gap: 8px;
  }
  
  .apple-search-container {
    min-width: 100%;
  }
  
  .apple-search-input {
    height: 36px;
    font-size: 11px;
  }
  
  .apple-filter-controls {
    width: 100%;
    justify-content: center;
  }
  
  .apple-filter-btn {
    padding: 6px 10px;
    font-size: 11px;
  }
  
  .apple-filter-btn span {
    display: none;
  }
  
  .apple-quick-filters {
    justify-content: center;
    gap: 6px;
  }
  
  .apple-filter-chip {
    padding: 5px 10px;
    font-size: 10px;
  }
  
  .apple-unified-filters {
    gap: 10px;
  }
  
  .apple-filter-group {
    flex-shrink: 0;
  }
  
  .apple-select {
    flex: 1;
    height: 32px;
    font-size: 11px;
  }
  
  .apple-sort-group {
    width: 100%;
    flex-wrap: wrap;
  }
  
  .apple-sort-buttons {
    flex-wrap: wrap;
    gap: 4px;
  }
  
  .apple-sort-btn {
    padding: 5px 8px;
    font-size: 10px;
  }
  
  .apple-content-wrapper {
    padding: 16px;
  }
  
  /* Apple Table Responsive 768px */
  .apple-table-container {
    max-height: calc(100vh - 420px);
    border-radius: 14px;
  }
  
  .apple-table th,
  .apple-table td {
    padding: 10px 12px;
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
  
  .apple-user-name {
    font-size: 11px;
  }
  
  .apple-id-badge {
    padding: 3px 6px;
    font-size: 10px;
  }
  
  .apple-cargo-badge {
    padding: 3px 8px;
    font-size: 9px;
  }
  
  .apple-status-badge {
    padding: 3px 8px;
    font-size: 9px;
  }
  
  .apple-actions {
    gap: 4px;
  }
  
  .apple-action-btn {
    width: 28px;
    height: 28px;
  }
  
  .apple-action-btn svg {
    width: 12px;
    height: 12px;
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
}

/* ====================== APPLE RESPONSIVE 480px ====================== */
@media (max-width: 480px) {
  .main-content {
    padding: 6px;
  }
  
  .apple-page-header {
    border-radius: 16px 16px 0 0;
    padding: 6px 10px;
  }
  
  .apple-stats-section {
    border-radius: 0 0 16px 16px;
    padding: 12px 10px 10px 10px;
  }
  
  .apple-stats-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 4px;
  }
  
  .apple-stat-card {
    padding: 8px;
    border-radius: 10px;
  }
  
  .apple-stat-icon {
    width: 24px;
    height: 24px;
  }
  
  .apple-stat-icon svg {
    width: 12px;
    height: 12px;
  }
  
  .apple-stat-value {
    font-size: 12px;
  }
  
  .apple-stat-label {
    font-size: 8px;
  }
  
  .apple-search-input {
    height: 34px;
    padding: 0 36px;
    font-size: 11px;
  }
  
  .apple-search-icon {
    width: 16px;
    height: 16px;
  }
  
  .apple-clear-btn {
    width: 24px;
    height: 24px;
  }
  
  .apple-filter-btn {
    padding: 5px 8px;
    font-size: 10px;
    border-radius: 12px;
  }
  
  .apple-filter-btn svg {
    width: 12px;
    height: 12px;
  }
  
  .apple-filter-chip {
    padding: 4px 8px;
    font-size: 9px;
    border-radius: 14px;
  }
  
  .apple-filter-chip svg {
    width: 10px;
    height: 10px;
  }
  
  .apple-select {
    height: 30px;
    font-size: 10px;
    padding: 0 24px 0 10px;
  }
  
  .apple-count-badge {
    min-width: 20px;
    height: 20px;
    font-size: 9px;
  }
  
  .apple-sort-btn {
    padding: 4px 6px;
    font-size: 9px;
    border-radius: 8px;
  }
  
  .apple-sort-btn svg {
    width: 10px;
    height: 10px;
  }
  
  .apple-content-wrapper {
    padding: 12px;
  }
  
  /* Apple Table Responsive 480px */
  .apple-table-container {
    max-height: calc(100vh - 450px);
    border-radius: 12px;
  }
  
  .apple-table th,
  .apple-table td {
    padding: 8px 10px;
    font-size: 10px;
  }
  
  .apple-table th {
    font-size: 8px;
    letter-spacing: 0.3px;
  }
  
  .apple-avatar {
    width: 28px;
    height: 28px;
  }
  
  .apple-avatar svg {
    width: 14px;
    height: 14px;
  }
  
  .apple-user-name {
    font-size: 10px;
  }
  
  .apple-id-badge {
    padding: 2px 5px;
    font-size: 9px;
  }
  
  .apple-email {
    font-size: 9px;
  }
  
  .apple-cargo-badge {
    padding: 2px 6px;
    font-size: 8px;
  }
  
  .apple-curp {
    font-size: 9px;
  }
  
  .apple-status-badge {
    padding: 2px 6px;
    font-size: 8px;
    border-radius: 12px;
  }
  
  .apple-actions {
    gap: 3px;
  }
  
  .apple-action-btn {
    width: 24px;
    height: 24px;
  }
  
  .apple-action-btn svg {
    width: 10px;
    height: 10px;
  }
  
  .apple-pagination {
    padding: 10px 12px;
    gap: 8px;
  }
  
  .apple-pagination-btn,
  .apple-pagination-number {
    width: 30px;
    height: 30px;
  }
  
  .apple-pagination-btn svg {
    width: 14px;
    height: 14px;
  }
  
  .apple-pagination-number {
    font-size: 11px;
  }
}

/* === RESPONSIVIDAD ADICIONAL PARA TABLA === */
/* En dispositivos más pequeños, asegurar que el scroll funcione */
@media (max-width: 1024px) {
  .usuarios-table {
    min-width: 1000px; /* Forzar scroll horizontal en tablets */
  }
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
    align-items: center;
    text-align: center;
    gap: 0.75rem;
  }
  
  .pagination-nav {
    gap: 0.125rem;
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
    padding: 0.5rem 0.625rem;
  }
  
  .pagination-number {
    width: 40px;
    height: 40px;
    font-size: 0.8rem;
  }
  
  .pagination-jump {
    margin-top: 0.5rem;
  }
  
  .pagination-input {
    width: 70px;
  }
}

.pagination-btn.active {
  background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%);
  color: white;
  box-shadow: 
    0 2px 6px rgba(76, 175, 80, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  border-color: #388E3C;
  transform: scale(1.1);
}

.pagination-numbers {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(3px, 0.5vw, 4px);
}

.pagination-dots {
  padding: 0 clamp(4px, 0.6vw, 6px);
  color: #4CAF50;
  font-weight: bold;
  font-size: clamp(9px, 1.1vw, 11px);
}

/* Responsive */
@media (max-width: 1024px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
  
  .table-container {
    overflow: hidden;
    width: 100%;
  }
  
  .usuarios-table {
    width: 100%;
    max-width: 100%;
    font-size: clamp(7px, 1.3vw, 9px);
  }
  
  .usuarios-table th,
  .usuarios-table td {
    padding: clamp(3px, 0.8vw, 5px) clamp(1px, 0.5vw, 3px);
    font-size: clamp(7px, 1.3vw, 9px);
    text-align: center;
  }
  
  .btn-ver {
    padding: clamp(2px, 0.4vw, 3px) clamp(3px, 0.6vw, 4px);
    font-size: clamp(6px, 1vw, 7px);
    min-width: clamp(30px, 6vw, 45px);
    width: 100%;
    max-width: 100%;
  }
  
  .status-badge {
    padding: clamp(1px, 0.3vw, 2px) clamp(3px, 0.6vw, 4px);
    font-size: clamp(5px, 1vw, 6px);
    min-width: clamp(24px, 4.5vw, 35px);
    width: 100%;
    max-width: 100%;
  }
}

@media (max-width: 768px) and (orientation: landscape) {
  .main-content {
    margin-left: 160px;
    width: calc(100vw - 160px);
  }
  
  /* Modal de edición en landscape */
  .edit-modal {
    max-width: 85vw !important;
    max-height: 94vh !important;
  }
  
  .edit-modal .modal-body-modern {
    padding: clamp(8px, 1.5vw, 12px) clamp(12px, 2vw, 16px);
    max-height: calc(94vh - 100px);
  }
  
  .form-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: clamp(8px, 1.5vw, 12px);
  }
  
  .form-group {
    gap: 3px;
  }
  
  .form-group label {
    font-size: clamp(10px, 1.8vw, 12px);
  }
  
  .form-input {
    padding: clamp(6px, 1.2vw, 10px) clamp(8px, 1.5vw, 12px);
    font-size: clamp(11px, 2vw, 13px);
  }
  
  .modal-footer-edit {
    padding: clamp(8px, 1.5vw, 12px) clamp(12px, 2vw, 16px);
    gap: 8px;
  }
  
  .btn-save, .btn-cancel {
    padding: clamp(8px, 1.5vw, 10px) clamp(14px, 2.5vw, 18px);
    font-size: clamp(11px, 2vw, 13px);
  }
}

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
  
  .usuarios-table {
    min-width: 900px; /* Forzar scroll en tablets */
  }
  
  /* Responsive filtro estado */
  .filter-estado-buttons {
    padding: 3px;
    border-radius: 14px;
  }
  
  .filter-estado-btn {
    padding: 5px 10px;
    font-size: 10px;
    gap: 4px;
  }
  
  .filter-estado-btn svg {
    width: 10px;
    height: 10px;
  }
  
  /* Responsive ordenar */
  .sort-buttons {
    padding: 3px;
    border-radius: 14px;
  }
  
  .sort-btn {
    padding: 5px 10px;
    font-size: 10px;
    gap: 4px;
  }
  
  .sort-btn svg {
    width: 10px;
    height: 10px;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 240px;
    width: calc(100vw - 240px);
  }
  
  .page-header {
    padding: clamp(12px, 3vw, 20px);
  }
  
  .header-content {
    flex-direction: column;
    gap: clamp(8px, 2vw, 12px);
    align-items: flex-start;
  }
  
  .header-main {
    width: 100%;
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .page-content {
    padding: clamp(12px, 3vw, 20px);
  }
  
  .search-box {
    max-width: 100%;
  }
  
  .table-container {
    border-radius: clamp(6px, 1.5vw, 10px);
    overflow: hidden;
    width: 100%;
    max-width: 100%;
  }
  
  .usuarios-table {
    width: 100%;
    max-width: 100%;
    font-size: clamp(7px, 1.4vw, 10px);
    table-layout: fixed;
  }
  
  .usuarios-table th,
  .usuarios-table td {
    padding: clamp(4px, 0.8vw, 6px) clamp(2px, 0.5vw, 4px);
    font-size: clamp(7px, 1.4vw, 10px);
    text-align: center;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .usuarios-table td:nth-child(1) { /* ID */
    width: 6%;
  }
  
  .usuarios-table td:nth-child(2) { /* Correo */
    width: 25%;
  }
  
  .usuarios-table td:nth-child(3) { /* Nombre */
    width: 20%;
  }
  
  .usuarios-table td:nth-child(4) { /* Cargo */
    width: 15%;
  }
  
  .usuarios-table td:nth-child(5) { /* Supervisor */
    width: 12%;
  }
  
  .usuarios-table td:nth-child(6) { /* Fecha */
    width: 10%;
  }
  
  .usuarios-table td:nth-child(7) { /* Estado */
    width: 8%;
  }
  
  .usuarios-table td:nth-child(8) { /* Acciones */
    width: 12%;
  }
  
  .btn-ver {
    padding: clamp(2px, 0.5vw, 4px) clamp(3px, 0.8vw, 5px);
    font-size: clamp(6px, 1.2vw, 8px);
    min-width: auto;
    width: 100%;
    max-width: 100%;
    border-radius: clamp(6px, 1.5vw, 10px);
  }
  
  .status-badge {
    padding: clamp(2px, 0.4vw, 3px) clamp(3px, 0.8vw, 5px);
    font-size: clamp(6px, 1.2vw, 8px);
    min-width: auto;
    width: 100%;
    max-width: 100%;
    border-radius: clamp(6px, 1.5vw, 10px);
  }
  
  .modal-content {
    margin: clamp(5px, 2vw, 10px);
    max-width: calc(100vw - clamp(10px, 4vw, 20px));
  }
  
  /* Estilos responsivos para modal de edición */
  .edit-modal {
    max-width: 94vw !important;
    max-height: 94vh !important;
    margin: 3vh auto;
  }
  
  .edit-modal .modal-body-modern {
    padding: clamp(12px, 2.5vw, 18px);
    max-height: calc(94vh - 130px);
  }
  
  .form-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: clamp(10px, 2vw, 14px);
  }
  
  .form-group {
    gap: 4px;
  }
  
  .form-group label {
    font-size: clamp(11px, 2.2vw, 13px);
  }
  
  .form-group label::before {
    width: 2px;
    height: 12px;
  }
  
  .form-input {
    padding: clamp(8px, 1.8vw, 12px) clamp(10px, 2vw, 14px);
    font-size: clamp(12px, 2.2vw, 14px);
    border-radius: 8px;
  }
  
  .password-toggle-btn-edit {
    width: 28px;
    height: 28px;
    right: 10px;
  }
  
  .password-toggle-btn-edit svg {
    width: 14px;
    height: 14px;
  }
  
  .password-input {
    padding-right: 46px !important;
  }
  
  .modal-footer-edit {
    padding: clamp(12px, 2.5vw, 16px);
    gap: 10px;
  }
  
  .btn-save, .btn-cancel {
    padding: clamp(10px, 2vw, 12px) clamp(16px, 3vw, 20px);
    font-size: clamp(12px, 2.2vw, 14px);
  }
  
  .pagination-container {
    padding: clamp(8px, 1.2vw, 12px);
    gap: clamp(6px, 1.5vw, 8px);
  }
  
  .pagination-info {
    order: 2;
    margin-bottom: 0;
    font-size: clamp(8px, 1vw, 10px);
  }
  
  .pagination-controls {
    order: 1;
    gap: clamp(3px, 0.5vw, 4px);
  }
}

@media (max-width: 480px) {
  .header-content {
    align-items: center;
    text-align: center;
  }
  
  .header-main {
    flex-direction: column;
    gap: clamp(6px, 1.5vw, 10px);
  }
  
  .table-container {
    border-radius: clamp(4px, 1vw, 8px);
    overflow-x: auto; /* Asegurar scroll horizontal */
  }
  
  .usuarios-table {
    min-width: 800px; /* Forzar scroll horizontal en móviles */
    font-size: clamp(8px, 1.2vw, 10px);
  }
  
  .usuarios-table th,
  .usuarios-table td {
    padding: clamp(4px, 0.8vw, 6px) clamp(2px, 0.4vw, 4px);
    font-size: clamp(8px, 1.2vw, 10px);
  }
  
  .btn-ver {
    padding: clamp(1px, 0.3vw, 3px) clamp(2px, 0.5vw, 4px);
    font-size: clamp(5px, 1vw, 7px);
    min-width: auto;
    width: 100%;
    max-width: 100%;
    border-radius: clamp(4px, 1vw, 8px);
  }
  
  .status-badge {
    padding: clamp(1px, 0.3vw, 2px) clamp(2px, 0.5vw, 4px);
    font-size: clamp(5px, 1vw, 7px);
    min-width: auto;
    width: 100%;
    max-width: 100%;
    border-radius: clamp(4px, 1vw, 8px);
  }
  
  /* Responsive filtro estado móvil */
  .filter-estado-group {
    order: -1;
    width: 100%;
    justify-content: center;
  }
  
  .filter-estado-buttons {
    width: 100%;
    justify-content: center;
    padding: 3px;
    gap: 3px;
  }
  
  .filter-estado-btn {
    padding: 5px 8px;
    font-size: 9px;
    gap: 3px;
    flex: 1;
    justify-content: center;
  }
  
  .filter-estado-btn svg {
    width: 10px;
    height: 10px;
  }
  
  /* Responsive ordenar móvil */
  .sort-group {
    order: -1;
    width: 100%;
    justify-content: center;
  }
  
  .sort-buttons {
    width: 100%;
    justify-content: center;
    padding: 3px;
    gap: 3px;
  }
  
  .sort-btn {
    padding: 5px 8px;
    font-size: 9px;
    gap: 3px;
    flex: 1;
    justify-content: center;
  }
  
  .sort-btn svg {
    width: 9px;
    height: 9px;
  }
  
  .modal-content {
    max-width: calc(100vw - 10px);
    margin: 5px;
  }
  
  .pagination-numbers {
    gap: clamp(1px, 0.3vw, 2px);
  }
  
  .pagination-btn {
    width: clamp(20px, 2.8vw, 24px);
    height: clamp(20px, 2.8vw, 24px);
    font-size: clamp(8px, 0.9vw, 10px);
    border-width: 1px;
  }
  
  .pagination-numbers {
    gap: clamp(2px, 0.4vw, 3px);
  }
  
  /* Modal de edición en pantallas pequeñas */
  .edit-modal {
    max-width: 96vw !important;
    max-height: 96vh !important;
  }
  
  .edit-modal .modal-body-modern {
    padding: clamp(10px, 2vw, 14px);
    max-height: calc(96vh - 120px);
  }
  
  .form-grid {
    grid-template-columns: 1fr;
    gap: clamp(10px, 2vw, 14px);
  }
  
  .form-group:last-child {
    grid-column: 1;
  }
  
  .form-group label {
    font-size: clamp(11px, 2.5vw, 13px);
  }
  
  .form-input {
    padding: clamp(10px, 2vw, 12px);
    font-size: clamp(13px, 2.8vw, 15px);
  }
  
  .modal-footer-edit {
    padding: clamp(12px, 2.5vw, 16px);
    flex-direction: column;
    gap: 10px;
  }
  
  .btn-save, .btn-cancel {
    width: 100%;
    justify-content: center;
    padding: clamp(12px, 2.5vw, 14px);
  }
}

/* Media query específico para dispositivos ultra pequeños */
@media (max-width: 360px) {
  .table-container {
    overflow: hidden;
    width: 100%;
  }
  
  .usuarios-table {
    width: 100%;
    max-width: 100%;
    font-size: clamp(5px, 1vw, 7px);
    table-layout: fixed;
  }
  
  .usuarios-table th,
  .usuarios-table td {
    padding: clamp(2px, 0.4vw, 3px) clamp(1px, 0.2vw, 2px);
    font-size: clamp(5px, 1vw, 7px);
    text-align: center;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .usuarios-table td:nth-child(1) { /* ID */
    width: 4%;
  }
  
  .usuarios-table td:nth-child(2) { /* Correo */
    width: 30%;
  }
  
  .usuarios-table td:nth-child(3) { /* Nombre */
    width: 25%;
  }
  
  .usuarios-table td:nth-child(4) { /* Cargo */
    width: 12%;
  }
  
  .usuarios-table td:nth-child(5) { /* Supervisor */
    width: 9%;
  }
  
  .usuarios-table td:nth-child(6) { /* Fecha */
    width: 7%;
  }
  
  .usuarios-table td:nth-child(7) { /* Estado */
    width: 5%;
  }
  
  .usuarios-table td:nth-child(8) { /* Acciones */
    width: 8%;
  }
  
  .btn-ver {
    padding: 1px 2px;
    font-size: clamp(4px, 0.8vw, 6px);
    min-width: auto;
    width: 100%;
    max-width: 100%;
    border-radius: 3px;
  }
  
  .status-badge {
    padding: 1px;
    font-size: clamp(4px, 0.8vw, 6px);
    min-width: auto;
    width: 100%;
    max-width: 100%;
    border-radius: 3px;
  }
}

/* Responsive para Modal Moderno */
@media (max-width: 768px) {
  .modal-content-modern {
    max-width: 95vw;
    max-height: 90vh;
    margin: clamp(5px, 2vw, 10px);
  }
  
  .modal-header-modern {
    padding: clamp(10px, 2.5vw, 14px) clamp(14px, 3.5vw, 18px);
  }
  
  .modal-title {
    font-size: clamp(12px, 3vw, 16px);
  }
  
  .modal-icon {
    width: clamp(24px, 5vw, 30px);
    height: clamp(24px, 5vw, 30px);
  }
  
  .btn-close-modern {
    width: clamp(24px, 5vw, 28px);
    height: clamp(24px, 5vw, 28px);
  }
  
  .modal-body-modern {
    padding: clamp(6px, 1.5vw, 8px) clamp(14px, 3.5vw, 18px) clamp(14px, 3.5vw, 18px);
  }
  
  .detail-card {
    padding: clamp(6px, 1.5vw, 8px) clamp(8px, 2vw, 10px);
    gap: clamp(4px, 1vw, 6px);
  }
  
  .detail-icon {
    width: clamp(20px, 4vw, 24px);
    height: clamp(20px, 4vw, 24px);
  }
  
  .detail-label {
    font-size: clamp(8px, 1.8vw, 10px);
  }
  
  .detail-value {
    font-size: clamp(10px, 2.2vw, 12px);
  }
  
  .password-value {
    font-size: clamp(9px, 2vw, 11px);
    padding: clamp(3px, 0.8vw, 4px) clamp(4px, 1vw, 6px);
  }
  
  .password-toggle-btn {
    width: clamp(18px, 3.5vw, 22px);
    height: clamp(18px, 3.5vw, 22px);
  }
}

@media (max-width: 480px) {
  .modal-content-modern {
    max-width: 98vw;
    max-height: 95vh;
    border-radius: clamp(12px, 2vw, 16px);
  }
  
  .modal-header-modern {
    padding: clamp(8px, 2vw, 12px) clamp(12px, 3vw, 16px);
  }
  
  .modal-title-section {
    gap: clamp(6px, 1.5vw, 8px);
  }
  
  .modal-title {
    font-size: clamp(11px, 2.8vw, 14px);
  }
  
  .modal-icon {
    width: clamp(20px, 4.5vw, 26px);
    height: clamp(20px, 4.5vw, 26px);
  }
  
  .btn-close-modern {
    width: clamp(20px, 4.5vw, 24px);
    height: clamp(20px, 4.5vw, 24px);
  }
  
  .detail-card {
    padding: clamp(5px, 1.2vw, 7px) clamp(7px, 1.8vw, 9px);
    gap: clamp(3px, 0.8vw, 5px);
    border-radius: clamp(6px, 1.5vw, 8px);
  }
  
  .detail-icon {
    width: clamp(16px, 3.5vw, 20px);
    height: clamp(16px, 3.5vw, 20px);
  }
  
  .detail-label {
    font-size: clamp(7px, 1.6vw, 9px);
    margin-bottom: clamp(1px, 0.3vw, 2px);
  }
  
  .detail-value {
    font-size: clamp(9px, 2vw, 11px);
  }
  
  .password-display {
    gap: clamp(4px, 1vw, 6px);
    margin-top: clamp(2px, 0.5vw, 4px);
  }
  
  .password-value {
    font-size: clamp(8px, 1.8vw, 10px);
    padding: clamp(2px, 0.6vw, 3px) clamp(3px, 0.8vw, 4px);
  }
  
  .password-toggle-btn {
    width: clamp(16px, 3vw, 18px);
    height: clamp(16px, 3vw, 18px);
  }
  
  .password-toggle-btn svg {
    width: clamp(10px, 2.2vw, 12px);
    height: clamp(10px, 2.2vw, 12px);
  }
}

/* Estilos para Modal de Éxito */
.modal-overlay-success {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content-success {
  background: white;
  border-radius: 12px;
  padding: 24px;
  width: 90%;
  max-width: 320px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  border: 1px solid #e5e7eb;
  animation: slideUp 0.3s ease-out;
  text-align: center;
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

.success-icon {
  width: 48px;
  height: 48px;
  background: #22c55e;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  color: white;
}

.modal-content-success h3 {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

.modal-content-success p {
  margin: 0 0 20px 0;
  font-size: 14px;
  color: #6b7280;
  line-height: 1.4;
}

.btn-success-ok {
  background: #22c55e;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 24px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 100px;
}

.btn-success-ok:hover {
  background: #16a34a;
  transform: translateY(-1px);
}

.btn-success-ok:active {
  transform: translateY(0);
}

/* Responsive para Modal de Éxito */
@media (max-width: 768px) {
  .modal-content-success {
    width: 95%;
    padding: 20px;
    max-width: 280px;
  }
  
  .success-icon {
    width: 40px;
    height: 40px;
    margin-bottom: 12px;
  }
  
  .success-icon svg {
    width: 20px;
    height: 20px;
  }
  
  .modal-content-success h3 {
    font-size: 16px;
  }
  
  .modal-content-success p {
    font-size: 13px;
  }
  
  .btn-success-ok {
    padding: 8px 20px;
    font-size: 13px;
  }
}

/* === ESTILOS PARA CONTADOR DE USUARIOS === */
.users-stats-compact {
  display: flex;
  gap: clamp(0.5rem, 1.5vw, 1rem);
  padding: 0;
  background: transparent;
  justify-content: center;
  flex-wrap: wrap;
  margin: 0;
  animation: fadeInUp 0.6s ease-out 0.2s both;
}

.users-stats-compact .compact-stat-card {
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

.users-stats-compact .compact-stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(76, 175, 80, 0.08), transparent);
  transition: left 0.8s ease;
}

.users-stats-compact .compact-stat-card:hover::before {
  left: 100%;
}

.users-stats-compact .compact-stat-card:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 
    0 4px 20px rgba(76, 175, 80, 0.15),
    0 2px 8px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
  border-color: rgba(76, 175, 80, 0.25);
  background: linear-gradient(135deg, rgba(255, 255, 255, 1) 0%, rgba(240, 255, 240, 0.95) 100%);
}

.users-stats-compact .compact-stat-icon {
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

.users-stats-compact .compact-stat-icon::before {
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

.users-stats-compact .compact-stat-card:hover .compact-stat-icon {
  transform: rotate(-3deg) scale(1.08);
  box-shadow: 0 3px 12px rgba(76, 175, 80, 0.2);
  background: linear-gradient(135deg, rgba(255, 255, 255, 1) 0%, rgba(240, 255, 240, 0.9) 100%);
  border-color: rgba(76, 175, 80, 0.4);
}

.users-stats-compact .compact-stat-card:hover .compact-stat-icon::before {
  opacity: 1;
}

.users-stats-compact .compact-stat-icon svg {
  width: clamp(14px, 2.2vw, 16px);
  height: clamp(14px, 2.2vw, 16px);
  transition: all 0.3s ease;
  filter: drop-shadow(0 1px 2px rgba(76, 175, 80, 0.3));
}

.users-stats-compact .compact-stat-card:hover .compact-stat-icon svg {
  transform: scale(1.1);
  filter: drop-shadow(0 2px 4px rgba(76, 175, 80, 0.4));
}

.users-stats-compact .compact-stat-info {
  display: flex;
  flex-direction: column;
  gap: clamp(0.1rem, 0.3vw, 0.15rem);
  flex: 1;
  min-width: 0;
}

.users-stats-compact .compact-stat-value {
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

.users-stats-compact .compact-stat-card:hover .compact-stat-value {
  transform: scale(1.03);
  background: linear-gradient(135deg, #4CAF50 0%, #43A047 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.users-stats-compact .compact-stat-label {
  font-size: clamp(0.55rem, 1.1vw, 0.65rem);
  font-weight: 500;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  line-height: 1.1;
  transition: all 0.3s ease;
}

.users-stats-compact .compact-stat-card:hover .compact-stat-label {
  color: #4CAF50;
  transform: translateX(1px);
}

/* Responsive para contador de usuarios */
@media (max-width: 768px) {
  .controls-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .controls-left {
    width: 100%;
  }
  
  .filter-cargo-group {
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
  }
  
  .filter-cargo-wrapper {
    width: 100%;
    flex-direction: column;
    gap: 6px;
  }
  
  .filter-cargo-select {
    width: 100%;
    min-width: auto;
  }
  
  .cargo-count-badge {
    align-self: flex-start;
  }
  
  .controls-right {
    margin-left: 0;
    margin-top: clamp(0.5rem, 1vw, 0.75rem);
    justify-content: center;
  }
  
  .users-stats-compact {
    gap: 0.75rem;
    padding: 0;
    margin: 0;
    justify-content: center;
  }
  
  .users-stats-compact .compact-stat-card {
    min-width: 110px;
    padding: 0.6rem 0.8rem;
    gap: 0.5rem;
  }
  
  .users-stats-compact .compact-stat-icon {
    width: 28px;
    height: 28px;
  }
  
  .users-stats-compact .compact-stat-icon svg {
    width: 14px;
    height: 14px;
  }
  
  .users-stats-compact .compact-stat-value {
    font-size: 1rem;
  }
  
  .users-stats-compact .compact-stat-label {
    font-size: 0.58rem;
  }
  
  .cargo-count-badge {
    font-size: 10px;
    padding: 4px 8px;
    min-width: 45px;
  }
  
  .cargo-count-number {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .controls-right .users-stats-compact {
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
  }
  
  .users-stats-compact .compact-stat-card {
    min-width: 100%;
    max-width: 220px;
    margin: 0 auto;
    padding: 0.6rem 0.8rem;
  }
  
  .users-stats-compact .compact-stat-icon {
    width: 26px;
    height: 26px;
  }
  
  .users-stats-compact .compact-stat-icon svg {
    width: 13px;
    height: 13px;
  }
  
  .cargo-count-badge {
    font-size: 9px;
    padding: 4px 7px;
    min-width: 40px;
    gap: 4px;
  }
  
  .cargo-count-badge svg {
    width: 10px;
    height: 10px;
  }
  
  .cargo-count-number {
    font-size: 11px;
  }
  
  .users-stats-compact .compact-stat-value {
    font-size: 0.95rem;
  }
  
  .users-stats-compact .compact-stat-label {
    font-size: 0.55rem;
  }
}

/* Indicador visual para scroll horizontal en dispositivos muy pequeños */
@media (max-width: 480px) {
  .table-container::after {
    content: "← Desliza para ver más →";
    position: absolute;
    bottom: -25px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 10px;
    color: #666;
    background: rgba(255, 255, 255, 0.9);
    padding: 2px 8px;
    border-radius: 10px;
    border: 1px solid #ddd;
    white-space: nowrap;
    z-index: 1;
  }
  
  .page-content {
    padding-bottom: 40px; /* Espacio extra para el indicador */
  }
}

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

/* CSS específico para forzar scroll horizontal en tablets y móviles */
@media (max-width: 1024px) {
  .table-container {
    overflow-x: scroll !important;
    -webkit-overflow-scrolling: touch !important;
    display: block !important;
    white-space: nowrap !important;
  }
  
  .usuarios-table {
    min-width: 1290px !important;
    width: 1290px !important;
    display: table !important;
    table-layout: fixed !important;
  }
  
  .usuarios-table td,
  .usuarios-table th {
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
  }
}

/* ============================================
   MODALES TOTALMENTE RESPONSIVOS
   Para cualquier tamaño y orientación de pantalla
   ============================================ */

/* Modal en orientación horizontal (landscape) */
@media (orientation: landscape) and (max-height: 600px) {
  .modal-overlay-modern {
    padding: 8px;
  }
  
  .modal-content-modern {
    max-height: 95vh;
    max-width: 90vw;
  }
  
  .modal-body-modern {
    max-height: calc(95vh - 60px);
    overflow-y: auto;
    padding: 10px 15px;
  }
  
  .user-details-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 8px;
  }
  
  .detail-card {
    padding: 6px 10px;
  }
  
  .detail-label {
    font-size: 9px;
  }
  
  .detail-value {
    font-size: 11px;
  }
  
  .modal-header-modern {
    padding: 10px 15px;
  }
  
  .modal-title {
    font-size: 14px;
  }
}

/* Modal muy pequeño en landscape */
@media (orientation: landscape) and (max-height: 450px) {
  .modal-content-modern {
    max-height: 98vh;
    border-radius: 10px;
  }
  
  .modal-body-modern {
    max-height: calc(98vh - 50px);
    padding: 8px 12px;
  }
  
  .user-details-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
  }
  
  .detail-card {
    padding: 5px 8px;
  }
  
  .detail-icon {
    width: 18px;
    height: 18px;
  }
  
  .detail-label {
    font-size: 8px;
  }
  
  .detail-value {
    font-size: 10px;
  }
  
  .modal-header-modern {
    padding: 8px 12px;
  }
  
  .modal-title {
    font-size: 12px;
  }
  
  .modal-icon, .btn-close-modern {
    width: 22px;
    height: 22px;
  }
}

/* Modal en pantallas muy pequeñas (portrait) */
@media (orientation: portrait) and (max-width: 400px) {
  .modal-content-modern {
    max-width: 98vw;
    max-height: 90vh;
    margin: 5px;
    border-radius: 12px;
  }
  
  .modal-body-modern {
    max-height: calc(90vh - 70px);
    overflow-y: auto;
    padding: 10px;
  }
  
  .user-details-grid {
    grid-template-columns: 1fr;
    gap: 6px;
  }
  
  .detail-card {
    padding: 8px 10px;
    flex-direction: row;
    align-items: center;
    gap: 10px;
  }
  
  .detail-card .detail-info {
    flex: 1;
  }
  
  .form-group {
    margin-bottom: 10px;
  }
  
  .form-group label {
    font-size: 11px;
    margin-bottom: 4px;
  }
  
  .form-group input,
  .form-group select,
  .form-select {
    padding: 8px 10px;
    font-size: 13px;
  }
}

/* Asegurar scroll en el body del modal */
.modal-body-modern {
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(37, 99, 235, 0.3) transparent;
}

.modal-body-modern::-webkit-scrollbar {
  width: 6px;
}

.modal-body-modern::-webkit-scrollbar-track {
  background: transparent;
}

.modal-body-modern::-webkit-scrollbar-thumb {
  background: rgba(37, 99, 235, 0.3);
  border-radius: 3px;
}

.modal-body-modern::-webkit-scrollbar-thumb:hover {
  background: rgba(37, 99, 235, 0.5);
}

/* Grid responsive para formularios de edición */
.edit-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

@media (min-width: 600px) and (orientation: landscape) {
  .edit-form {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .edit-form .form-group:last-child {
    grid-column: span 2;
  }
}

/* Fix para inputs en modal de edición */
.form-group input,
.form-group select,
.form-select {
  width: 100%;
  box-sizing: border-box;
}

/* Botones de acción del modal responsivos */
.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  flex-wrap: wrap;
  padding-top: 15px;
  border-top: 1px solid #e5e7eb;
  margin-top: 10px;
}

@media (max-width: 400px) {
  .modal-actions {
    flex-direction: column;
  }
  
  .modal-actions button {
    width: 100%;
  }
}

@media (orientation: landscape) and (max-height: 500px) {
  .modal-actions {
    padding-top: 10px;
    margin-top: 8px;
  }
  
  .modal-actions button {
    padding: 8px 16px;
    font-size: 12px;
  }
  
  /* Footer de modal de edición en landscape */
  .modal-footer-edit {
    padding: 10px 15px;
  }
  
  .modal-footer-edit .btn-save,
  .modal-footer-edit .btn-cancel {
    padding: 8px 14px;
    font-size: 12px;
  }
  
  /* Footer de modal de eliminar en landscape */
  .modal-footer-delete {
    padding: 10px 15px;
  }
  
  .modal-footer-delete .btn-delete,
  .modal-footer-delete .btn-cancel {
    padding: 8px 14px;
    font-size: 12px;
  }
  
  /* Form grid en landscape muy pequeño */
  .form-grid {
    gap: 10px;
  }
  
  .form-group {
    gap: 4px;
  }
  
  .form-group label {
    font-size: 11px;
  }
  
  .form-input {
    padding: 8px 10px;
    font-size: 12px;
  }
}

/* Estilos adicionales para pantallas muy pequeñas en portrait */
@media (orientation: portrait) and (max-width: 360px) {
  .modal-content-modern {
    max-width: 100vw;
    max-height: 95vh;
    margin: 0;
    border-radius: 0;
  }
  
  .modal-footer-edit,
  .modal-footer-delete {
    flex-direction: column;
    padding: 12px;
    gap: 8px;
  }
  
  .modal-footer-edit button,
  .modal-footer-delete button {
    width: 100%;
  }
  
  .form-group label {
    font-size: 11px;
  }
  
  .form-input {
    padding: 10px;
    font-size: 14px;
  }
}

/* =====================================================
   MODAL DE EDICIÓN - REDISEÑO COMPLETO Y RESPONSIVO
   ===================================================== */

/* Overlay del modal */
.edit-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 16px;
}

/* Contenedor principal del modal */
.edit-modal-container {
  background: #ffffff;
  border-radius: 16px;
  width: 100%;
  max-width: 700px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  overflow: hidden;
  animation: modalSlideIn 0.25s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Header del modal - Estilo vidrio líquido naranja */
.edit-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  background: linear-gradient(135deg, 
    rgba(255, 152, 0, 0.85) 0%, 
    rgba(245, 124, 0, 0.9) 50%,
    rgba(255, 167, 38, 0.85) 100%);
  backdrop-filter: blur(10px);
  color: white;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 4px 15px rgba(255, 152, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.3),
    inset 0 -1px 0 rgba(0, 0, 0, 0.1);
}

.edit-modal-title-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.edit-modal-icon {
  width: 38px;
  height: 38px;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(4px);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.edit-modal-icon svg {
  stroke: white;
  width: 20px;
  height: 20px;
}

.edit-modal-title-text h3 {
  margin: 0;
  font-size: 17px;
  font-weight: 700;
  letter-spacing: -0.2px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);
}

.edit-modal-subtitle {
  font-size: 12px;
  opacity: 0.9;
  font-weight: 500;
}

.edit-modal-close {
  width: 32px;
  height: 32px;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(4px);
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.edit-modal-close:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: scale(1.05);
}

.edit-modal-close svg {
  stroke: white;
}

/* Body del modal */
.edit-modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background: #f8fafc;
}

.edit-form-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Fila del formulario - 2 columnas */
.edit-form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

/* Campo individual */
.edit-form-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.edit-form-field label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
}

.edit-form-field label svg {
  stroke: #ff9800;
  flex-shrink: 0;
}

.edit-form-field input,
.edit-form-field select {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 15px;
  color: #1e293b;
  background: #ffffff;
  transition: all 0.2s;
  box-sizing: border-box;
}

.edit-form-field input:focus,
.edit-form-field select:focus {
  outline: none;
  border-color: #ff9800;
  box-shadow: 0 0 0 4px rgba(255, 152, 0, 0.1);
}

.edit-form-field input:hover:not(:focus),
.edit-form-field select:hover:not(:focus) {
  border-color: #cbd5e1;
}

.edit-form-field input::placeholder {
  color: #94a3b8;
}

.edit-form-field select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 20px;
  padding-right: 44px;
  cursor: pointer;
}

/* Campo de contraseña */
.edit-password-wrapper {
  position: relative;
  width: 100%;
}

.edit-password-wrapper input {
  width: 100%;
  padding-right: 52px;
}

.edit-password-toggle {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  width: 36px;
  height: 36px;
  border: none;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  color: white;
}

.edit-password-toggle:hover {
  transform: translateY(-50%) scale(1.05);
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
}

.edit-password-toggle svg {
  stroke: white;
}

/* Footer del modal */
.edit-modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  background: #ffffff;
  border-top: 1px solid #e2e8f0;
}

.edit-btn-cancel,
.edit-btn-save {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.edit-btn-cancel {
  background: #f1f5f9;
  border: 2px solid #e2e8f0;
  color: #64748b;
}

.edit-btn-cancel:hover {
  background: #e2e8f0;
  border-color: #cbd5e1;
  color: #475569;
}

.edit-btn-save {
  background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
  border: none;
  color: white;
  box-shadow: 0 4px 14px rgba(255, 152, 0, 0.3);
}

.edit-btn-save:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 152, 0, 0.4);
}

.edit-btn-save:disabled {
  opacity: 0.7;
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

/* =====================================================
   RESPONSIVE - TABLETS (768px)
   ===================================================== */
@media (max-width: 768px) {
  .edit-modal-overlay {
    padding: 12px;
  }
  
  .edit-modal-container {
    max-width: 100%;
    max-height: 94vh;
    border-radius: 14px;
  }
  
  .edit-modal-header {
    padding: 16px 20px;
  }
  
  .edit-modal-icon {
    width: 40px;
    height: 40px;
  }
  
  .edit-modal-title-text h3 {
    font-size: 18px;
  }
  
  .edit-modal-body {
    padding: 20px;
  }
  
  .edit-form-row {
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }
  
  .edit-form-field input,
  .edit-form-field select {
    padding: 12px 14px;
    font-size: 14px;
  }
  
  .edit-modal-footer {
    padding: 16px 20px;
  }
  
  .edit-btn-cancel,
  .edit-btn-save {
    padding: 11px 20px;
    font-size: 14px;
  }
}

/* =====================================================
   RESPONSIVE - MÓVILES (480px)
   ===================================================== */
@media (max-width: 480px) {
  .edit-modal-overlay {
    padding: 8px;
    align-items: flex-end;
  }
  
  .edit-modal-container {
    max-height: 92vh;
    border-radius: 16px 16px 0 0;
  }
  
  .edit-modal-header {
    padding: 14px 16px;
  }
  
  .edit-modal-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
  }
  
  .edit-modal-icon svg {
    width: 18px;
    height: 18px;
  }
  
  .edit-modal-title-text h3 {
    font-size: 16px;
  }
  
  .edit-modal-subtitle {
    font-size: 12px;
  }
  
  .edit-modal-close {
    width: 32px;
    height: 32px;
  }
  
  .edit-modal-body {
    padding: 16px;
  }
  
  .edit-form-container {
    gap: 16px;
  }
  
  .edit-form-row {
    grid-template-columns: 1fr;
    gap: 14px;
  }
  
  .edit-form-field label {
    font-size: 12px;
  }
  
  .edit-form-field input,
  .edit-form-field select {
    padding: 12px 14px;
    font-size: 15px;
    border-radius: 8px;
  }
  
  .edit-password-toggle {
    width: 34px;
    height: 34px;
  }
  
  .edit-modal-footer {
    padding: 14px 16px;
    flex-direction: column;
    gap: 10px;
  }
  
  .edit-btn-cancel,
  .edit-btn-save {
    width: 100%;
    padding: 14px;
    justify-content: center;
  }
  
  .edit-btn-save {
    order: -1;
  }
}

/* =====================================================
   RESPONSIVE - LANDSCAPE EN MÓVILES
   ===================================================== */
@media (max-height: 500px) and (orientation: landscape) {
  .edit-modal-overlay {
    padding: 8px;
    align-items: center;
  }
  
  .edit-modal-container {
    max-height: 96vh;
    max-width: 90vw;
    border-radius: 12px;
  }
  
  .edit-modal-header {
    padding: 12px 16px;
  }
  
  .edit-modal-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
  }
  
  .edit-modal-icon svg {
    width: 16px;
    height: 16px;
  }
  
  .edit-modal-title-text h3 {
    font-size: 15px;
  }
  
  .edit-modal-subtitle {
    font-size: 11px;
  }
  
  .edit-modal-body {
    padding: 12px 16px;
  }
  
  .edit-form-container {
    gap: 10px;
  }
  
  .edit-form-row {
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }
  
  .edit-form-field {
    gap: 4px;
  }
  
  .edit-form-field label {
    font-size: 11px;
  }
  
  .edit-form-field label svg {
    width: 14px;
    height: 14px;
  }
  
  .edit-form-field input,
  .edit-form-field select {
    padding: 10px 12px;
    font-size: 13px;
    border-radius: 8px;
  }
  
  .edit-password-toggle {
    width: 30px;
    height: 30px;
    border-radius: 6px;
  }
  
  .edit-password-toggle svg {
    width: 14px;
    height: 14px;
  }
  
  .edit-modal-footer {
    padding: 10px 16px;
    gap: 10px;
  }
  
  .edit-btn-cancel,
  .edit-btn-save {
    padding: 10px 18px;
    font-size: 13px;
    border-radius: 8px;
  }
}

/* =====================================================
   RESPONSIVE - TABLETS LANDSCAPE
   ===================================================== */
@media (min-width: 768px) and (max-height: 600px) and (orientation: landscape) {
  .edit-modal-container {
    max-width: 85vw;
    max-height: 94vh;
  }
  
  .edit-modal-body {
    padding: 16px 20px;
  }
  
  .edit-form-row {
    gap: 16px;
  }
  
  .edit-form-field input,
  .edit-form-field select {
    padding: 11px 14px;
    font-size: 14px;
  }
}
</style>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
</style>
