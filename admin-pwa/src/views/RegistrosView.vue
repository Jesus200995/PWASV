<template>
  <div class="registros-container">
    <Sidebar_NEW @logout="logout" />
    
    <main class="main-content">      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10,9 9,9 8,9"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Gestión de Registros</h1>
              <p class="header-subtitle">Administra todos los registros de usuarios en la aplicación</p>
            </div>
          </div>
          <div class="header-actions">
            <button @click="cargarRegistros" class="refresh-btn" :disabled="loading">
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
            <!-- Contenedor izquierdo con filtros -->
            <div class="filters-left">
              <!-- Barra de búsqueda -->
              <div class="search-box">
                <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="m21 21-4.35-4.35"></path>
                </svg>
                <input 
                  v-model="searchTerm" 
                  type="text" 
                  placeholder="Buscar por usuario, descripción o ubicación..." 
                  class="search-input"
                  @input="filtrarRegistros"
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
                    @change="filtrarRegistros"
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
                    @change="filtrarRegistros"
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
            
            <!-- Contadores de estadísticas en el lado derecho -->
            <div class="filters-right">
              <div class="visor-stats-compact">
                <div class="compact-stat-card">
                  <div class="compact-stat-icon">
                    <!-- Icono de calendario/actividades hoy -->
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z" 
                            fill="#4CAF50"/>
                      <circle cx="12" cy="6" r="2" fill="#66BB6A" opacity="0.8"/>
                      <path d="M16 11h2v2h-2zm0 3h2v2h-2z" fill="#4CAF50" opacity="0.6"/>
                    </svg>
                  </div>
                  <div class="compact-stat-info">
                    <div class="compact-stat-value">{{ actividadesHoy }}</div>
                    <div class="compact-stat-label">Actividades hoy</div>
                  </div>
                </div>
                
                <div class="compact-stat-card">
                  <div class="compact-stat-icon">
                    <!-- Icono de estadísticas/total actividades -->
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z" 
                            fill="#4CAF50"/>
                      <circle cx="5" cy="19" r="2" fill="#66BB6A" opacity="0.7"/>
                      <circle cx="12" cy="12" r="1.5" fill="#4CAF50" opacity="0.8"/>
                      <circle cx="19" cy="5" r="1.5" fill="#43A047"/>
                    </svg>
                  </div>
                  <div class="compact-stat-info">
                    <div class="compact-stat-value">{{ totalActividades }}</div>
                    <div class="compact-stat-label">Total actividades</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Filtros adicionales y acciones (expandibles) -->
          <div class="filters-advanced" v-show="mostrarFiltrosAvanzados">
            <div class="advanced-filters-grid">
              <!-- Filtro por ordenamiento -->
              <div class="filter-group">
                <label class="filter-label">Ordenar por</label>
                <div class="sort-options">
                  <button 
                    @click="ordenarPor('id')"
                    :class="['sort-btn', { active: campoOrdenamiento === 'id' }]"
                    title="Ordenar por ID"
                  >
                    ID
                    <svg v-if="campoOrdenamiento === 'id'" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path v-if="direccionOrdenamiento === 'asc'" d="m7 15 5 5 5-5"/>
                      <path v-else d="m7 9 5-5 5 5"/>
                    </svg>
                  </button>
                  <button 
                    @click="ordenarPor('usuario')"
                    :class="['sort-btn', { active: campoOrdenamiento === 'usuario' }]"
                    title="Ordenar por Usuario"
                  >
                    Usuario
                    <svg v-if="campoOrdenamiento === 'usuario'" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path v-if="direccionOrdenamiento === 'asc'" d="m7 15 5 5 5-5"/>
                      <path v-else d="m7 9 5-5 5 5"/>
                    </svg>
                  </button>
                  <button 
                    @click="ordenarPor('tipo')"
                    :class="['sort-btn', { active: campoOrdenamiento === 'tipo' }]"
                    title="Ordenar por Tipo"
                  >
                    Tipo
                    <svg v-if="campoOrdenamiento === 'tipo'" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path v-if="direccionOrdenamiento === 'asc'" d="m7 15 5 5 5-5"/>
                      <path v-else d="m7 9 5-5 5 5"/>
                    </svg>
                  </button>
                  <button 
                    @click="ordenarPor('fecha')"
                    :class="['sort-btn', { active: campoOrdenamiento === 'fecha' }]"
                    title="Ordenar por Fecha"
                  >
                    Fecha
                    <svg v-if="campoOrdenamiento === 'fecha'" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path v-if="direccionOrdenamiento === 'asc'" d="m7 15 5 5 5-5"/>
                      <path v-else d="m7 9 5-5 5 5"/>
                    </svg>
                  </button>
                </div>
              </div>
              
              <!-- Filtro por usuario -->
              <div class="filter-group">
                <label class="filter-label">Usuario</label>
                <select v-model="filtroUsuario" @change="filtrarRegistros" class="filter-select">
                  <option value="">Todos los usuarios</option>
                  <option v-for="usuario in usuariosUnicos" :key="usuario.id" :value="usuario.id">
                    {{ usuario.nombre_completo }}
                  </option>
                </select>
              </div>

              <!-- Filtro por tipo de actividad -->
              <div class="filter-group">
                <label class="filter-label">Tipo de Actividad</label>
                <select v-model="filtroTipoActividad" @change="filtrarRegistros" class="filter-select">
                  <option value="">Todos los tipos</option>
                  <option value="campo">Campo</option>
                  <option value="gabinete">Gabinete</option>
                </select>
              </div>

              <!-- Filtro por estado de foto -->
              <div class="filter-group">
                <label class="filter-label">Estado de Foto</label>
                <div class="filter-options">
                  <label class="checkbox-option">
                    <input type="checkbox" v-model="filtroConFoto" @change="filtrarRegistros">
                    <span>Con foto</span>
                  </label>
                  <label class="checkbox-option">
                    <input type="checkbox" v-model="filtroSinFoto" @change="filtrarRegistros">
                    <span>Sin foto</span>
                  </label>
                  <label class="checkbox-option">
                    <input type="checkbox" v-model="filtroConDescripcion" @change="filtrarRegistros">
                    <span>Con descripción</span>
                  </label>
                </div>
              </div>
            </div>
            
            <div class="advanced-actions">
              <button @click="exportarRegistros('csv')" class="export-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="7 10 12 15 17 10"></polyline>
                  <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
                Exportar CSV
              </button>
              <button @click="exportarRegistros('excel')" class="export-btn excel">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                  <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
                Exportar Excel
              </button>
              <button @click="imprimirRegistros" class="export-btn print">
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

        <!-- Tabla de registros -->
        <div class="registros-section">
          <div v-if="loading && registros.length === 0" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando registros...</p>
          </div>
          
          <div v-else-if="error" class="error-container">
            <p>{{ error }}</p>
            <button @click="cargarRegistros" class="retry-btn">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
                <path d="M3 3v5h5"></path>
                <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"></path>
                <path d="M21 21v-5h-5"></path>
              </svg>
              Reintentar
            </button>
          </div>
            <div v-else-if="registrosFiltrados.length === 0" class="empty-state">
            <div class="empty-icon">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="4"/>
                <path d="M7 17v-6m5 6V7m5 10v-3"/>
              </svg>
            </div>
            <h3>No hay registros</h3>
            <p v-if="filtroUsuario">No se encontraron registros para {{ usuariosDisponibles.find(u => u.id.toString() === filtroUsuario.toString())?.nombre_completo || `Usuario ${filtroUsuario}` }}</p>
            <p v-else>Aún no se han creado registros en la aplicación.</p>
          </div>
          
          <div v-else class="table-container">
            <!-- Información de carga optimizada -->
            <div class="load-info">
              <div class="load-status">
                <span class="load-icon">⚡</span>
                <span class="load-text">
                  Mostrando {{ registros.length.toLocaleString('es') }} registros cargados
                  <template v-if="totalRegistrosServidor > registros.length">
                    de {{ totalRegistrosServidor.toLocaleString('es') }} totales
                  </template>
                </span>
                <button 
                  v-if="totalRegistrosServidor > registros.length && !cargandoMas" 
                  @click="cargarMasRegistros"
                  class="load-more-btn"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 5v14m-7-7l7 7 7-7"/>
                  </svg>
                  Cargar más
                </button>
                <span v-if="cargandoMas" class="loading-more">
                  <svg class="spinner" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    <path d="M9 12l2 2 4-4"/>
                  </svg>
                  Cargando...
                </span>
              </div>
            </div>
            <!-- 
            <div class="registros-info">
              <div class="registros-total">
                <div class="registros-icon">📊</div>
                <div class="registros-text">
                  Página <span class="highlight">{{ paginaActual }}</span> de <span class="highlight">{{ totalPaginas }}</span>
                  • {{ registrosFiltrados.length.toLocaleString('es') }} {{ registrosFiltrados.length === 1 ? 'registro' : 'registros' }} 
                  <template v-if="registrosFiltrados.length !== registros.length">
                    de <span class="highlight">{{ registros.length.toLocaleString('es') }}</span> totales
                  </template>
                </div>
                <div class="registros-summary" v-if="registros.length > 0">
                  <span class="registros-badge" title="Registros con fotografía">
                    <i class="fas fa-camera"></i> {{ (registros.filter(r => r.foto_url).length / registros.length * 100).toFixed(0) }}%
                  </span>
                  <span class="registros-badge" title="Usuarios únicos">
                    <i class="fas fa-users"></i> {{ [...new Set(registros.map(r => r.usuario_id))].length }}
                  </span>
                  <span class="registros-badge pagination-badge" title="Registros por página">
                    <i class="fas fa-list"></i> {{ registrosPorPagina }}/pág
                  </span>
                </div>
              </div>
            </div>
            -->
            <table class="registros-table">
              <thead>
                <tr>
                  <th class="col-id">ID</th>
                  <th class="col-usuario">Usuario</th>
                  <th class="col-foto">Foto</th>
                  <th class="col-tipo">Tipo</th>
                  <th class="col-ubicacion">Ubicación</th>
                  <th class="col-descripcion">Descripción</th>
                  <th class="col-fecha">Fecha</th>
                  <th class="col-acciones">Acciones</th>
                </tr>
              </thead>
              <tbody>                <tr v-for="registro in registrosPaginados" :key="registro.id">
                  <td class="col-id">#{{ registro.id }}</td>
                  <td class="col-usuario">
                    <div class="usuario-info">
                      <strong>{{ registro.usuario?.nombre_completo || `Usuario ${registro.usuario_id}` }}</strong>
                      <small>{{ registro.usuario?.correo || 'No disponible' }}</small>
                    </div>
                  </td>
                  <td class="col-foto">
                    <img 
                      v-if="registro.foto_url" 
                      :src="`${API_URL}/${registro.foto_url}`"
                      alt="Foto" 
                      class="foto-mini"
                      @click="abrirFotoCompleta(registro.foto_url)"
                    >
                    <span v-else class="no-foto">Sin foto</span>
                  </td>
                  <td class="col-tipo">
                    <span :class="['tipo-badge', getTipoClass(registro.tipo_actividad)]">
                      {{ getTipoLabel(registro.tipo_actividad) }}
                    </span>
                  </td>
                  <td class="col-ubicacion ubicacion">
                    {{ parseFloat(registro.latitud).toFixed(4) }},<br>
                    {{ parseFloat(registro.longitud).toFixed(4) }}
                  </td>
                  <td class="col-descripcion descripcion">
                    {{ truncateText(registro.descripcion || 'Sin descripción', 40) }}
                  </td>
                  <td class="col-fecha fecha">
                    <div class="fecha-hora-container">
                      <div class="hora-display">{{ formatFechaCompacta(registro.fecha_hora).hora }}</div>
                      <div class="fecha-display">{{ formatFechaCompacta(registro.fecha_hora).fecha }}</div>
                    </div>
                  </td>
                  <td class="col-acciones">
                    <div class="action-container">
                      <button @click="verDetalles(registro)" class="btn-ver" title="Ver detalles del registro">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                      </button>
                      <span class="btn-label">Detalles</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            
            <!-- Componente de Paginación -->
            <div v-if="totalPaginas > 1" class="pagination-container">
              <div class="pagination-info">
                <span class="pagination-text">
                  Mostrando <strong>{{ indiceInicio + 1 }}</strong> a <strong>{{ Math.min(indiceFin, registrosFiltrados.length) }}</strong> 
                  de <strong>{{ registrosFiltrados.length }}</strong> registros
                </span>
                <div class="pagination-selector">
                  <label for="itemsPorPagina" class="pagination-label">Registros por página:</label>
                  <select 
                    id="itemsPorPagina" 
                    v-model="registrosPorPagina" 
                    @change="cambiarRegistrosPorPagina"
                    class="pagination-select"
                  >
                    <option value="25">25</option>
                    <option value="50">50</option>
                    <option value="100">100</option>
                    <option value="200">200</option>
                  </select>
                </div>
              </div>
              
              <nav class="pagination-nav" aria-label="Navegación de páginas">
                <!-- Botón Primera Página -->
                <button 
                  @click="irAPagina(1)" 
                  :disabled="paginaActual === 1"
                  class="pagination-btn pagination-first"
                  title="Primera página"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="11 17 6 12 11 7"></polyline>
                    <polyline points="18 17 13 12 18 7"></polyline>
                  </svg>
                </button>
                
                <!-- Botón Página Anterior -->
                <button 
                  @click="irAPagina(paginaActual - 1)" 
                  :disabled="paginaActual === 1"
                  class="pagination-btn pagination-prev"
                  title="Página anterior"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="15 18 9 12 15 6"></polyline>
                  </svg>
                  <span class="pagination-btn-text">Anterior</span>
                </button>
                
                <!-- Números de Página -->
                <div class="pagination-numbers">
                  <!-- Página 1 siempre visible si hay más de 1 página -->
                  <button 
                    v-if="mostrarPagina(1)"
                    @click="irAPagina(1)"
                    :class="['pagination-number', { active: paginaActual === 1 }]"
                  >
                    1
                  </button>
                  
                  <!-- Puntos suspensivos iniciales -->
                  <span v-if="paginaActual > 4" class="pagination-ellipsis">...</span>
                  
                  <!-- Páginas del rango visible -->
                  <button 
                    v-for="pagina in paginasVisibles" 
                    :key="pagina"
                    @click="irAPagina(pagina)"
                    :class="['pagination-number', { active: paginaActual === pagina }]"
                  >
                    {{ pagina }}
                  </button>
                  
                  <!-- Puntos suspensivos finales -->
                  <span v-if="paginaActual < totalPaginas - 3" class="pagination-ellipsis">...</span>
                  
                  <!-- Última página siempre visible si hay más de 1 página -->
                  <button 
                    v-if="mostrarPagina(totalPaginas) && totalPaginas > 1"
                    @click="irAPagina(totalPaginas)"
                    :class="['pagination-number', { active: paginaActual === totalPaginas }]"
                  >
                    {{ totalPaginas }}
                  </button>
                </div>
                
                <!-- Botón Página Siguiente -->
                <button 
                  @click="irAPagina(paginaActual + 1)" 
                  :disabled="paginaActual === totalPaginas"
                  class="pagination-btn pagination-next"
                  title="Página siguiente"
                >
                  <span class="pagination-btn-text">Siguiente</span>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="9 18 15 12 9 6"></polyline>
                  </svg>
                </button>
                
                <!-- Botón Última Página -->
                <button 
                  @click="irAPagina(totalPaginas)" 
                  :disabled="paginaActual === totalPaginas"
                  class="pagination-btn pagination-last"
                  title="Última página"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="13 17 18 12 13 7"></polyline>
                    <polyline points="6 17 11 12 6 7"></polyline>
                  </svg>
                </button>
              </nav>
              
              <!-- Navegación rápida -->
              <div class="pagination-jump">
                <label for="jumpToPage" class="pagination-label">Ir a página:</label>
                <input 
                  id="jumpToPage"
                  type="number" 
                  v-model.number="paginaSalto"
                  @keyup.enter="saltarAPagina"
                  :min="1" 
                  :max="totalPaginas"
                  class="pagination-input"
                  placeholder="Nº"
                >
                <button @click="saltarAPagina" class="pagination-jump-btn" title="Ir a página">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M5 12h14m-7-7 7 7-7 7"/>
                  </svg>
                </button>
              </div>
            </div>
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
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import * as XLSX from 'xlsx'
import Sidebar from '../components/Sidebar.vue'
import { usuariosService } from '../services/usuariosService.js'

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

// Variables para ordenamiento
const campoOrdenamiento = ref('fecha') // Por defecto ordenar por fecha
const direccionOrdenamiento = ref('desc') // Por defecto más reciente primero

// Variables para filtros avanzados (nuevas)
const searchTerm = ref('')
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
    
    console.log('📊 Cargando más registros...')
    
    const response = await axios.get(`${API_URL}/admin/registros`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      params: {
        page: Math.ceil(registros.value.length / 1000) + 1,
        page_size: 1000,
        usuario_id: filtroUsuario.value || undefined
      },
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
})

const cargarRegistros = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const token = localStorage.getItem('admin_token')
    console.log('📊 Solicitando registros con límite seguro...')
    console.time('Carga de registros')
    
    // Usar el nuevo endpoint optimizado /admin/registros
    const response = await axios.get(`${API_URL}/admin/registros`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      params: {
        page: 1,
        page_size: 1000, // Paginación optimizada
        usuario_id: filtroUsuario.value || undefined
      },
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
    
    try {
      const response = await axios.get(`${API_URL}/estadisticas`, {
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

const filtrarRegistros = async () => {
  let filtrados = [...registros.value]
  
  // Actualizar usuariosUnicos basado en los registros actuales
  actualizarUsuariosUnicos()

  // Si cambió el filtro de usuario, recargar del servidor
  if (filtroUsuario.value && !registros.value.some(r => r.usuario_id === parseInt(filtroUsuario.value))) {
    await cargarRegistrosParaUsuario(parseInt(filtroUsuario.value))
    filtrados = [...registros.value]
  }

  // Filtro por texto de búsqueda
  if (searchTerm.value) {
    const termino = searchTerm.value.toLowerCase()
    filtrados = filtrados.filter(registro => 
      (registro.usuario?.nombre_completo && registro.usuario.nombre_completo.toLowerCase().includes(termino)) ||
      (registro.usuario?.correo && registro.usuario.correo.toLowerCase().includes(termino)) ||
      (registro.descripcion && registro.descripcion.toLowerCase().includes(termino)) ||
      (registro.latitud && registro.latitud.toString().includes(termino)) ||
      (registro.longitud && registro.longitud.toString().includes(termino))
    )
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
    console.log(`🔍 Cargando registros para usuario ${usuarioId}...`)
    
    const response = await axios.get(`${API_URL}/admin/registros`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      params: {
        page: 1,
        page_size: 1000,
        usuario_id: usuarioId
      },
      timeout: 15000
    })
    
    const { registros: registrosUsuario = [] } = response.data
    
    if (registrosUsuario.length > 0) {
      const registrosEnriquecidos = await usuariosService.enriquecerRegistrosConUsuarios(registrosUsuario)
      
      // Combinar con registros existentes (evitar duplicados)
      const idsExistentes = new Set(registros.value.map(r => r.id))
      const registrosNuevos = registrosEnriquecidos.filter(r => !idsExistentes.has(r.id))
      
      if (registrosNuevos.length > 0) {
        registros.value = [...registros.value, ...registrosNuevos]
        console.log(`✅ Agregados ${registrosNuevos.length} registros del usuario ${usuarioId}`)
      }
    }
    
  } catch (error) {
    console.error(`Error cargando registros del usuario ${usuarioId}:`, error)
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
const limpiarBusqueda = () => {
  searchTerm.value = ''
  filtrarRegistros()
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

const requestFullscreen = (event) => {
  if (event.target.requestFullscreen) {
    event.target.requestFullscreen()
  }
}

const cerrarModal = () => {
  showModal.value = false
  if (map) {
    map.remove()
    map = null
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
}

.main-content {
  flex: 1;
  margin-left: min(220px, 18vw);
  width: calc(100vw - min(220px, 18vw));
  background: linear-gradient(135deg, #f8f9fa 0%, #f0fff0 100%);
  min-height: 100vh;
  position: relative;
  box-sizing: border-box;
  overflow-x: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

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
  
  /* Filtros más compactos en tablets */
  .advanced-filters {
    padding: 0.3rem 0.4rem;
    margin-bottom: 0.3rem;
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
    padding: 0.25rem 0.4rem;
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
  padding: clamp(8px, 1.5vw, 16px) clamp(16px, 4vw, 32px);
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
  color: #9ca3af;
  width: clamp(12px, 1.5vw, 14px);
  height: clamp(12px, 1.5vw, 14px);
}

.search-input {
  width: 100%;
  padding: clamp(0.3rem, 0.8vw, 0.4rem) clamp(0.5rem, 1.2vw, 0.7rem) clamp(0.3rem, 0.8vw, 0.4rem) clamp(2rem, 4vw, 2.4rem);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: clamp(4px, 1vw, 6px);
  background: rgba(255, 255, 255, 0.9);
  font-size: clamp(0.65rem, 1.3vw, 0.75rem);
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
  right: clamp(0.5rem, 1.2vw, 0.7rem);
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: clamp(0.15rem, 0.3vw, 0.2rem);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  width: clamp(16px, 2.5vw, 20px);
  height: clamp(16px, 2.5vw, 20px);
}

.clear-search-btn:hover {
  background: rgba(0, 0, 0, 0.05);
  color: #4b5563;
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
  padding: clamp(16px, 4vw, 24px);
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
  border-radius: clamp(8px, 2vw, 12px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background: white;
  box-sizing: border-box;
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
  min-width: clamp(500px, 70vw, 700px);
  border-collapse: collapse;
  position: relative;
}

.registros-table th {
  background: linear-gradient(135deg, #f8f9fa 0%, #f0f8f0 100%);
  padding: clamp(6px, 1.5vw, 10px) clamp(4px, 1vw, 8px);
  text-align: center;
  font-weight: 700;
  color: #4CAF50;
  text-transform: uppercase;
  font-size: clamp(8px, 1.8vw, 10px);
  letter-spacing: 0.3px;
  position: sticky;
  top: 0;
  z-index: 10;
  border-bottom: 1px solid rgba(224, 224, 224, 0.6);
  white-space: nowrap;
}

.registros-table td {
  padding: clamp(6px, 1.5vw, 10px) clamp(4px, 1vw, 8px);
  border-bottom: 1px solid rgba(224, 224, 224, 0.6);
  font-size: clamp(10px, 1.8vw, 12px);
  transition: all 0.3s ease;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 0;
  text-align: center;
  vertical-align: middle;
}

.registros-table tbody tr {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
}

.registros-table tbody tr:hover {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.05) 0%, rgba(76, 175, 80, 0.02) 100%);
  transform: translateX(4px);
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.1);
}

.registros-table tbody tr:hover td {
  border-bottom-color: rgba(76, 175, 80, 0.2);
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
  font-size: clamp(8px, 1.8vw, 10px);
}

.descripcion {
  max-width: clamp(120px, 16vw, 160px);
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
  flex-direction: column;
  gap: clamp(0.5px, 0.3vh, 1px);
}

.usuario-info strong {
  font-size: clamp(10px, 2.2vw, 12px);
  color: #2c3e50;
}

.usuario-info small {
  font-size: clamp(8px, 1.8vw, 10px);
  color: #666;
  font-style: italic;
}

.btn-ver {
  width: clamp(24px, 4vw, 28px);
  height: clamp(24px, 4vw, 28px);
  padding: 0;
  background: linear-gradient(135deg, #4CAF50, #43A047);
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.25);
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
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
  width: clamp(14px, 3vw, 16px);
  height: clamp(14px, 3vw, 16px);
  transition: all 0.3s ease;
}

.btn-ver:hover svg {
  transform: scale(1.1);
}

/* Contenedor de acción centrado */
.action-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 8px 0;
}

/* Label pequeño debajo del botón */
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

/* Estilos para columnas específicas de la tabla */
.col-id {
  width: 60px !important;
  max-width: 60px !important;
  min-width: 60px !important;
}

.col-usuario {
  width: 180px !important;
  max-width: 180px !important;
  min-width: 180px !important;
  text-align: left !important;
}

.col-foto {
  width: 60px !important;
  max-width: 60px !important;
  min-width: 60px !important;
}

.col-tipo {
  width: 80px !important;
  max-width: 80px !important;
  min-width: 80px !important;
}

.col-ubicacion {
  width: 120px !important;
  max-width: 120px !important;
  min-width: 120px !important;
}

.col-descripcion {
  width: 150px !important;
  max-width: 150px !important;
  min-width: 150px !important;
  text-align: left !important;
}

.col-fecha {
  width: 100px !important;
  max-width: 100px !important;
  min-width: 100px !important;
}

.col-acciones {
  width: 80px !important;
  max-width: 80px !important;
  min-width: 80px !important;
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
  z-index: 2000;
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
</style>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
</style>
