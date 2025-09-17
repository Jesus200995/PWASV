<template>
  <div class="asistencia-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                <polyline points="22 4 12 14.01 9 11.01"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Control de Asistencia</h1>
              <p class="header-subtitle">Monitorea el registro de asistencias de todos los usuarios</p>
            </div>
          </div>
          <div class="header-actions">
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
            
            <!-- Contadores de estadísticas en el lado derecho -->
            <div class="filters-right">
              <div class="visor-stats-compact">
                <div class="compact-stat-card">
                  <div class="compact-stat-icon">
                    <!-- Icono de asistencias hoy -->
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" 
                            fill="#4CAF50"/>
                      <circle cx="12" cy="12" r="3" fill="#66BB6A" opacity="0.8"/>
                    </svg>
                  </div>
                  <div class="compact-stat-info">
                    <div class="compact-stat-value">{{ totalAsistenciasHoy }}</div>
                    <div class="compact-stat-label">Asistencias hoy</div>
                  </div>
                </div>
                
                <div class="compact-stat-card">
                  <div class="compact-stat-icon">
                    <!-- Icono de usuarios presentes -->
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" 
                            fill="#4CAF50"/>
                      <circle cx="9" cy="7" r="4" fill="#66BB6A"/>
                      <path d="M22 21v-2a4 4 0 0 0-3-3.87" stroke="#4CAF50" stroke-width="2"/>
                      <path d="M16 3.13a4 4 0 0 1 0 7.75" stroke="#43A047" stroke-width="2"/>
                    </svg>
                  </div>
                  <div class="compact-stat-info">
                    <div class="compact-stat-value">{{ usuariosPresentes }}</div>
                    <div class="compact-stat-label">Usuarios presentes</div>
                  </div>
                </div>

                <div class="compact-stat-card">
                  <div class="compact-stat-icon">
                    <!-- Icono de total registros -->
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M20 6L9 17l-5-5" stroke="#4CAF50" stroke-width="3" fill="none"/>
                      <circle cx="18" cy="8" r="2" fill="#66BB6A"/>
                      <circle cx="6" cy="16" r="2" fill="#43A047"/>
                      <circle cx="12" cy="12" r="1.5" fill="#4CAF50"/>
                    </svg>
                  </div>
                  <div class="compact-stat-info">
                    <div class="compact-stat-value">{{ totalAsistencias }}</div>
                    <div class="compact-stat-label">Total registros</div>
                  </div>
                </div>
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
                <tr v-for="asistencia in asistenciasPaginadas" :key="asistencia.id">
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
            
            <!-- Componente de Paginación -->
            <div v-if="totalPaginas > 1" class="pagination-container">
              <div class="pagination-info">
                <span class="pagination-text">
                  Mostrando <strong>{{ indiceInicio + 1 }}</strong> a <strong>{{ Math.min(indiceFin, asistenciasFiltradas.length) }}</strong> 
                  de <strong>{{ asistenciasFiltradas.length }}</strong> asistencias
                </span>
                <div class="pagination-selector">
                  <label for="itemsPorPagina" class="pagination-label">Asistencias por página:</label>
                  <select 
                    id="itemsPorPagina" 
                    v-model="asistenciasPorPagina" 
                    @change="cambiarAsistenciasPorPagina"
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
import Sidebar from '../components/Sidebar_NEW.vue'
import MapaAsistenciaModal from '../components/MapaAsistenciaModal.vue'
import AsistenciasService from '../services/asistenciasService.js'
import EstadisticasService from '../services/estadisticasService.js'
import * as XLSX from 'xlsx'

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
      // Variables para paginación
      paginaActual: 1,
      asistenciasPorPagina: 50,
      paginaSalto: '',
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
      tipoMapa: 'entrada', // 'entrada', 'salida', 'asistencia'
      // Estadísticas del servidor
      estadisticasServidor: {
        totalAsistencias: 0,
        totalAsistenciasHoy: 0,
        usuariosPresentes: 0,
        totalRegistros: 0,
        totalUsuarios: 0,
        registrosHoy: 0
      }
    }
  },
  computed: {
    totalAsistencias() {
      // Usar estadísticas del servidor si están disponibles, sino calcular localmente
      return this.estadisticasServidor.totalAsistencias > 0 
        ? this.estadisticasServidor.totalAsistencias 
        : this.asistencias.length
    },
    totalAsistenciasHoy() {
      // Usar estadísticas del servidor si están disponibles, sino calcular localmente
      if (this.estadisticasServidor.totalAsistenciasHoy > 0) {
        return this.estadisticasServidor.totalAsistenciasHoy
      }
      
      const hoy = new Date().toISOString().split('T')[0]
      return this.asistencias.filter(a => a.fecha === hoy).length
    },
    usuariosPresentes() {
      // Usar estadísticas del servidor si están disponibles, sino calcular localmente
      if (this.estadisticasServidor.usuariosPresentes > 0) {
        return this.estadisticasServidor.usuariosPresentes
      }
      
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
    },
    // Computed properties para paginación
    totalPaginas() {
      return Math.ceil(this.asistenciasFiltradas.length / this.asistenciasPorPagina)
    },
    indiceInicio() {
      return (this.paginaActual - 1) * this.asistenciasPorPagina
    },
    indiceFin() {
      return this.indiceInicio + this.asistenciasPorPagina
    },
    asistenciasPaginadas() {
      return this.asistenciasFiltradas.slice(this.indiceInicio, this.indiceFin)
    },
    paginasVisibles() {
      const paginas = []
      const inicio = Math.max(2, this.paginaActual - 2)
      const fin = Math.min(this.totalPaginas - 1, this.paginaActual + 2)
      
      for (let i = inicio; i <= fin; i++) {
        if (i !== 1 && i !== this.totalPaginas) {
          paginas.push(i)
        }
      }
      
      return paginas
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
        console.log('📊 Solicitando TODAS las asistencias sin límite...')
        console.time('Carga de asistencias')
        
        // Cargar asistencias y estadísticas en paralelo
        const [asistencias] = await Promise.all([
          AsistenciasService.obtenerAsistenciasConUsuarios(),
          this.cargarEstadisticas()
        ])
        
        console.log(`🔢 Recibidas ${asistencias.length} asistencias totales del servidor`)
        
        this.asistencias = asistencias
        this.filtrarAsistencias()
        
        console.timeEnd('Carga de asistencias')
        
        // Estadísticas rápidas
        const conEntrada = this.asistencias.filter(a => a.hora_entrada).length
        const conSalida = this.asistencias.filter(a => a.hora_salida).length
        const completas = this.asistencias.filter(a => a.hora_entrada && a.hora_salida).length
        const totalUsuariosUnicos = new Set(this.asistencias.map(a => a.usuario_id)).size
        
        console.log(`📈 Estadísticas de asistencias: ${this.asistencias.length.toLocaleString('es')} registros | ${totalUsuariosUnicos} usuarios únicos | ${conEntrada} con entrada (${(conEntrada/this.asistencias.length*100).toFixed(1)}%) | ${conSalida} con salida (${(conSalida/this.asistencias.length*100).toFixed(1)}%) | ${completas} completas (${(completas/this.asistencias.length*100).toFixed(1)}%)`)
        
        console.log('✅ Asistencias cargadas exitosamente:', this.asistencias.length)
      } catch (error) {
        console.error('❌ Error al cargar asistencias:', error)
        this.error = 'Error al cargar las asistencias. Por favor, intenta de nuevo.'
      } finally {
        this.loading = false
      }
    },

    async cargarEstadisticas() {
      try {
        console.log('🔍 Cargando estadísticas desde el servidor...')
        
        // Usar el servicio de estadísticas con fallback
        const estadisticas = await EstadisticasService.obtenerEstadisticasConFallback(
          [], // registros (no los usamos aquí)
          [], // usuarios (no los usamos aquí) 
          this.asistencias // asistencias para fallback
        )
        
        // Actualizar estadísticas del servidor
        this.estadisticasServidor = {
          totalAsistencias: estadisticas.totalAsistencias || 0,
          totalAsistenciasHoy: estadisticas.asistenciasHoy || 0,
          usuariosPresentes: estadisticas.usuariosPresentes || 0,
          totalRegistros: estadisticas.totalRegistros || 0,
          totalUsuarios: estadisticas.totalUsuarios || 0,
          registrosHoy: estadisticas.registrosHoy || 0
        }
        
        console.log('✅ Estadísticas cargadas:', this.estadisticasServidor)
        
      } catch (error) {
        console.warn('⚠️ Error al cargar estadísticas, usando cálculo local:', error)
        // En caso de error, resetear estadísticas para que use cálculo local
        this.estadisticasServidor = {
          totalAsistencias: 0,
          totalAsistenciasHoy: 0,
          usuariosPresentes: 0,
          totalRegistros: 0,
          totalUsuarios: 0,
          registrosHoy: 0
        }
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

    formatearFechaCorta(fecha) {
      if (!fecha) return ''
      try {
        const fechaObj = new Date(fecha)
        return fechaObj.toLocaleDateString('es-ES', {
          day: '2-digit',
          month: '2-digit'
        })
      } catch (error) {
        return fecha
      }
    },

    formatearFechaSimple(fecha) {
      if (!fecha) return ''
      try {
        const fechaObj = new Date(fecha)
        return fechaObj.toLocaleDateString('es-ES', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric'
        })
      } catch (error) {
        return fecha
      }
    },

    formatearFechaConDia(fecha) {
      if (!fecha) return ''
      try {
        const fechaObj = new Date(fecha)
        return fechaObj.toLocaleDateString('es-ES', {
          weekday: 'long'
        })
      } catch (error) {
        return ''
      }
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

    // === MÉTODOS DE PAGINACIÓN ===
    mostrarPagina(numeroPagina) {
      if (numeroPagina === 1) {
        return this.totalPaginas > 1 && (this.paginaActual <= 4 || numeroPagina === 1)
      }
      if (numeroPagina === this.totalPaginas) {
        return this.totalPaginas > 1 && (this.paginaActual >= this.totalPaginas - 3 || numeroPagina === this.totalPaginas)
      }
      return false
    },

    irAPagina(numeroPagina) {
      if (numeroPagina >= 1 && numeroPagina <= this.totalPaginas) {
        this.paginaActual = numeroPagina
        
        // Scroll suave al inicio de la tabla
        const tableContainer = document.querySelector('.table-container')
        if (tableContainer) {
          tableContainer.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
          })
        }
      }
    },

    cambiarAsistenciasPorPagina() {
      // Recalcular qué página mostrar para mantener aproximadamente la misma asistencia visible
      const asistenciaActual = this.indiceInicio + 1
      const nuevaPagina = Math.ceil(asistenciaActual / this.asistenciasPorPagina)
      this.paginaActual = Math.max(1, Math.min(nuevaPagina, this.totalPaginas))
    },

    saltarAPagina() {
      if (this.paginaSalto && this.paginaSalto >= 1 && this.paginaSalto <= this.totalPaginas) {
        this.irAPagina(this.paginaSalto)
        this.paginaSalto = ''
      }
    },

    // === FIN MÉTODOS DE PAGINACIÓN ===

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
      try {
        // Crear libro de trabajo
        const workbook = XLSX.utils.book_new()
        
        // Datos filtrados para exportación
        const asistenciasParaExportar = this.asistenciasFiltradas
        
        // Calcular estadísticas avanzadas
        const estadisticas = this.calcularEstadisticasCompletas(asistenciasParaExportar)
        
        // ================================
        // HOJA 1: RESUMEN EJECUTIVO
        // ================================
        const resumenData = [
          ['📊 REPORTE DE ASISTENCIAS - RESUMEN EJECUTIVO'],
          [''],
          ['📅 Información del Reporte'],
          ['Fecha de Generación:', new Date().toLocaleDateString('es-ES', { 
            weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' 
          })],
          ['Total de Registros:', estadisticas.totalAsistencias],
          ['Período Analizado:', this.obtenerPeriodoAnalizado()],
          ['Estado del Sistema:', 'Operativo ✅'],
          [''],
          ['👥 Estadísticas de Usuarios'],
          ['Usuarios Únicos:', estadisticas.usuariosUnicos],
          ['Usuarios Activos Hoy:', estadisticas.usuariosActivosHoy],
          ['Promedio Asistencias/Usuario:', estadisticas.promedioAsistenciasPorUsuario],
          [''],
          ['⏰ Estadísticas de Tiempo'],
          ['Asistencias Completas:', `${estadisticas.asistenciasCompletas} (${estadisticas.porcentajeCompletas}%)`],
          ['Asistencias en Curso:', `${estadisticas.asistenciasEnCurso} (${estadisticas.porcentajeEnCurso}%)`],
          ['Sin Entrada Registrada:', `${estadisticas.sinEntrada} (${estadisticas.porcentajeSinEntrada}%)`],
          ['Tiempo Promedio Trabajado:', estadisticas.tiempoPromedioTrabajado],
          ['Total Horas Trabajadas:', estadisticas.totalHorasTrabajadas],
          [''],
          ['📍 Estadísticas de Ubicación'],
          ['Registros con Geolocalización:', `${estadisticas.conGeolocalizacion} (${estadisticas.porcentajeGeolocalizacion}%)`],
          ['Entradas sin Ubicación:', estadisticas.sinUbicacionEntrada],
          ['Salidas sin Ubicación:', estadisticas.sinUbicacionSalida],
          [''],
          ['🎯 Indicadores de Rendimiento'],
          ['Tasa de Finalización:', `${estadisticas.tasaFinalizacion}%`],
          ['Puntualidad Promedio:', estadisticas.puntualidadPromedio],
          ['Eficiencia del Sistema:', `${estadisticas.eficienciaSistema}%`],
          [''],
          ['⚠️ Alertas y Observaciones'],
          ...estadisticas.alertas.map(alerta => ['', alerta])
        ]
        
        const wsResumen = XLSX.utils.aoa_to_sheet(resumenData)
        
        // Aplicar estilos al resumen
        this.aplicarEstilosResumen(wsResumen)
        
        XLSX.utils.book_append_sheet(workbook, wsResumen, '📊 Resumen Ejecutivo')
        
        // ================================
        // HOJA 2: DATOS DETALLADOS
        // ================================
        const datosDetallados = [
          [
            'ID Usuario', 'Nombre Usuario', 'Email', 'Fecha', 'Día Semana',
            'Hora Entrada', 'Hora Salida', 'Tiempo Trabajado', 'Estado Asistencia',
            'Lat. Entrada', 'Lng. Entrada', 'Lat. Salida', 'Lng. Salida',
            'Descripción Entrada', 'Descripción Salida', 'Departamento', 'Observaciones'
          ]
        ]
        
        asistenciasParaExportar.forEach(asistencia => {
          const tiempoTrabajado = this.calcularTiempoTrabajadoDetallado(asistencia)
          const estadoAsistencia = this.obtenerEstadoAsistenciaTexto(asistencia)
          const diaSemana = asistencia.fecha ? 
            this.formatearFechaConDia(asistencia.fecha) : ''
          
          datosDetallados.push([
            asistencia.usuario_id || '',
            asistencia.nombre_usuario || `Usuario ${asistencia.usuario_id}`,
            asistencia.correo_usuario || 'No disponible',
            asistencia.fecha ? this.formatearFechaSimple(asistencia.fecha) : '',
            diaSemana,
            asistencia.hora_entrada || '',
            asistencia.hora_salida || '',
            tiempoTrabajado.texto,
            estadoAsistencia,
            asistencia.latitud_entrada || '',
            asistencia.longitud_entrada || '',
            asistencia.latitud_salida || '',
            asistencia.longitud_salida || '',
            asistencia.descripcion_entrada || '',
            asistencia.descripcion_salida || '',
            asistencia.departamento || 'No asignado',
            asistencia.observaciones || ''
          ])
        })
        
        const wsDetallados = XLSX.utils.aoa_to_sheet(datosDetallados)
        
        // Aplicar estilos a datos detallados
        this.aplicarEstilosDetallados(wsDetallados, datosDetallados.length)
        
        XLSX.utils.book_append_sheet(workbook, wsDetallados, '📋 Datos Detallados')
        
        // ================================
        // HOJA 3: ANÁLISIS POR USUARIO
        // ================================
        const analisisUsuarios = this.generarAnalisisPorUsuario(asistenciasParaExportar)
        const wsUsuarios = XLSX.utils.aoa_to_sheet(analisisUsuarios)
        
        this.aplicarEstilosAnalisisUsuarios(wsUsuarios)
        
        XLSX.utils.book_append_sheet(workbook, wsUsuarios, '👥 Análisis Usuarios')
        
        // ================================
        // HOJA 4: ANÁLISIS TEMPORAL
        // ================================
        const analisisTemporal = this.generarAnalisisTemporal(asistenciasParaExportar)
        const wsTemporal = XLSX.utils.aoa_to_sheet(analisisTemporal)
        
        this.aplicarEstilosAnalisisTemporal(wsTemporal)
        
        XLSX.utils.book_append_sheet(workbook, wsTemporal, '📅 Análisis Temporal')
        
        // ================================
        // HOJA 5: MAPA DE UBICACIONES
        // ================================
        const mapaUbicaciones = this.generarMapaUbicaciones(asistenciasParaExportar)
        const wsUbicaciones = XLSX.utils.aoa_to_sheet(mapaUbicaciones)
        
        this.aplicarEstilosUbicaciones(wsUbicaciones)
        
        XLSX.utils.book_append_sheet(workbook, wsUbicaciones, '📍 Ubicaciones')
        
        // Generar y descargar archivo
        const nombreArchivo = `Asistencias_Detallado_${new Date().toISOString().split('T')[0]}_${Date.now()}.xlsx`
        XLSX.writeFile(workbook, nombreArchivo)
        
        // Mostrar mensaje de éxito
        this.mostrarNotificacionExito('Excel generado exitosamente', `Se ha exportado el archivo: ${nombreArchivo}`)
        
      } catch (error) {
        console.error('Error al exportar Excel:', error)
        this.mostrarNotificacionError('Error al exportar', 'No se pudo generar el archivo Excel. Inténtalo nuevamente.')
      }
    },

    calcularEstadisticasCompletas(asistencias) {
      const totalAsistencias = asistencias.length
      const usuariosUnicos = [...new Set(asistencias.map(a => a.usuario_id))].length
      const hoy = new Date().toISOString().split('T')[0]
      const usuariosActivosHoy = [...new Set(asistencias.filter(a => a.fecha === hoy).map(a => a.usuario_id))].length
      
      const asistenciasCompletas = asistencias.filter(a => a.hora_entrada && a.hora_salida).length
      const asistenciasEnCurso = asistencias.filter(a => a.hora_entrada && !a.hora_salida).length
      const sinEntrada = asistencias.filter(a => !a.hora_entrada).length
      
      const conGeolocalizacion = asistencias.filter(a => 
        (a.latitud_entrada && a.longitud_entrada) || (a.latitud_salida && a.longitud_salida)
      ).length
      
      const sinUbicacionEntrada = asistencias.filter(a => a.hora_entrada && (!a.latitud_entrada || !a.longitud_entrada)).length
      const sinUbicacionSalida = asistencias.filter(a => a.hora_salida && (!a.latitud_salida || !a.longitud_salida)).length
      
      // Cálculos de porcentajes
      const porcentajeCompletas = totalAsistencias > 0 ? ((asistenciasCompletas / totalAsistencias) * 100).toFixed(1) : 0
      const porcentajeEnCurso = totalAsistencias > 0 ? ((asistenciasEnCurso / totalAsistencias) * 100).toFixed(1) : 0
      const porcentajeSinEntrada = totalAsistencias > 0 ? ((sinEntrada / totalAsistencias) * 100).toFixed(1) : 0
      const porcentajeGeolocalizacion = totalAsistencias > 0 ? ((conGeolocalizacion / totalAsistencias) * 100).toFixed(1) : 0
      
      // Cálculos de tiempo
      let totalMinutos = 0
      let totalHoras = 0
      const asistenciasConTiempo = asistencias.filter(a => a.hora_entrada && a.hora_salida)
      
      asistenciasConTiempo.forEach(asistencia => {
        try {
          const entrada = new Date(`${asistencia.fecha} ${asistencia.hora_entrada}`)
          const salida = new Date(`${asistencia.fecha} ${asistencia.hora_salida}`)
          const diferencia = salida - entrada
          if (diferencia > 0) {
            totalMinutos += diferencia / (1000 * 60)
            totalHoras += diferencia / (1000 * 60 * 60)
          }
        } catch (error) {
          console.warn('Error calculando tiempo para asistencia:', asistencia)
        }
      })
      
      const tiempoPromedioMinutos = asistenciasConTiempo.length > 0 ? totalMinutos / asistenciasConTiempo.length : 0
      const horasPromedio = Math.floor(tiempoPromedioMinutos / 60)
      const minutosPromedio = Math.floor(tiempoPromedioMinutos % 60)
      
      // Generar alertas
      const alertas = []
      if (porcentajeSinEntrada > 10) alertas.push(`⚠️ Alto porcentaje sin entrada registrada: ${porcentajeSinEntrada}%`)
      if (porcentajeGeolocalizacion < 80) alertas.push(`📍 Baja cobertura de geolocalización: ${porcentajeGeolocalizacion}%`)
      if (asistenciasEnCurso > totalAsistencias * 0.2) alertas.push(`⏰ Muchas asistencias sin finalizar: ${asistenciasEnCurso}`)
      if (alertas.length === 0) alertas.push('✅ Todos los indicadores dentro de parámetros normales')
      
      return {
        totalAsistencias,
        usuariosUnicos,
        usuariosActivosHoy,
        promedioAsistenciasPorUsuario: usuariosUnicos > 0 ? (totalAsistencias / usuariosUnicos).toFixed(1) : 0,
        asistenciasCompletas,
        asistenciasEnCurso,
        sinEntrada,
        porcentajeCompletas,
        porcentajeEnCurso,
        porcentajeSinEntrada,
        tiempoPromedioTrabajado: `${horasPromedio}h ${minutosPromedio}m`,
        totalHorasTrabajadas: `${Math.floor(totalHoras)}h ${Math.floor((totalHoras % 1) * 60)}m`,
        conGeolocalizacion,
        porcentajeGeolocalizacion,
        sinUbicacionEntrada,
        sinUbicacionSalida,
        tasaFinalizacion: porcentajeCompletas,
        puntualidadPromedio: 'En desarrollo',
        eficienciaSistema: Math.min(100, parseFloat(porcentajeGeolocalizacion) + parseFloat(porcentajeCompletas)) / 2,
        alertas
      }
    },

    obtenerPeriodoAnalizado() {
      const asistencias = this.asistenciasFiltradas
      if (asistencias.length === 0) return 'Sin datos'
      
      const fechas = asistencias.map(a => a.fecha).filter(f => f).sort()
      if (fechas.length === 0) return 'Sin fechas válidas'
      
      const fechaInicio = this.formatearFechaSimple(fechas[0])
      const fechaFin = this.formatearFechaSimple(fechas[fechas.length - 1])
      
      return fechaInicio === fechaFin ? fechaInicio : `${fechaInicio} - ${fechaFin}`
    },

    calcularTiempoTrabajadoDetallado(asistencia) {
      if (!asistencia.hora_entrada || !asistencia.hora_salida) {
        return { 
          texto: asistencia.hora_entrada ? 'En curso' : 'Sin entrada',
          minutos: 0,
          estado: asistencia.hora_entrada ? 'en_curso' : 'sin_entrada'
        }
      }
      
      try {
        const entrada = new Date(`${asistencia.fecha} ${asistencia.hora_entrada}`)
        const salida = new Date(`${asistencia.fecha} ${asistencia.hora_salida}`)
        const diferencia = salida - entrada
        
        if (diferencia < 0) return { texto: 'Error en horarios', minutos: 0, estado: 'error' }
        
        const minutosTotales = Math.floor(diferencia / (1000 * 60))
        const horas = Math.floor(minutosTotales / 60)
        const minutos = minutosTotales % 60
        
        return {
          texto: `${horas}h ${minutos}m`,
          minutos: minutosTotales,
          estado: 'completo'
        }
      } catch (error) {
        return { texto: 'Error', minutos: 0, estado: 'error' }
      }
    },

    obtenerEstadoAsistenciaTexto(asistencia) {
      if (!asistencia.hora_entrada) return '❌ Sin Entrada'
      if (!asistencia.hora_salida) return '⏳ En Curso'
      return '✅ Completa'
    },

    generarAnalisisPorUsuario(asistencias) {
      const analisisPorUsuario = new Map()
      
      asistencias.forEach(asistencia => {
        const userId = asistencia.usuario_id
        if (!analisisPorUsuario.has(userId)) {
          analisisPorUsuario.set(userId, {
            nombre: asistencia.nombre_usuario || `Usuario ${userId}`,
            email: asistencia.correo_usuario || 'No disponible',
            totalAsistencias: 0,
            asistenciasCompletas: 0,
            asistenciasEnCurso: 0,
            sinEntrada: 0,
            totalMinutosTrabajados: 0,
            diasUnicos: new Set(),
            primeraAsistencia: asistencia.fecha,
            ultimaAsistencia: asistencia.fecha
          })
        }
        
        const user = analisisPorUsuario.get(userId)
        user.totalAsistencias++
        
        if (asistencia.fecha) {
          user.diasUnicos.add(asistencia.fecha)
          if (asistencia.fecha < user.primeraAsistencia) user.primeraAsistencia = asistencia.fecha
          if (asistencia.fecha > user.ultimaAsistencia) user.ultimaAsistencia = asistencia.fecha
        }
        
        if (!asistencia.hora_entrada) {
          user.sinEntrada++
        } else if (!asistencia.hora_salida) {
          user.asistenciasEnCurso++
        } else {
          user.asistenciasCompletas++
          const tiempo = this.calcularTiempoTrabajadoDetallado(asistencia)
          user.totalMinutosTrabajados += tiempo.minutos
        }
      })
      
      const analisisData = [
        ['👥 ANÁLISIS DETALLADO POR USUARIO'],
        [''],
        ['Usuario', 'Email', 'Total Asistencias', 'Completas', 'En Curso', 'Sin Entrada', 
         'Días Trabajados', 'Tiempo Total', 'Promedio/Día', 'Primera Asistencia', 'Última Asistencia', 'Estado']
      ]
      
      Array.from(analisisPorUsuario.values())
        .sort((a, b) => b.totalAsistencias - a.totalAsistencias)
        .forEach(user => {
          const diasTrabajados = user.diasUnicos.size
          const horasTotales = Math.floor(user.totalMinutosTrabajados / 60)
          const minutosTotales = user.totalMinutosTrabajados % 60
          const promedioMinutosPorDia = diasTrabajados > 0 ? user.totalMinutosTrabajados / diasTrabajados : 0
          const promedioHoras = Math.floor(promedioMinutosPorDia / 60)
          const promedioMinutos = Math.floor(promedioMinutosPorDia % 60)
          
          const estado = user.sinEntrada > user.totalAsistencias * 0.3 ? '⚠️ Irregular' :
                        user.asistenciasCompletas > user.totalAsistencias * 0.8 ? '✅ Excelente' :
                        '⏳ Regular'
          
          analisisData.push([
            user.nombre,
            user.email,
            user.totalAsistencias,
            user.asistenciasCompletas,
            user.asistenciasEnCurso,
            user.sinEntrada,
            diasTrabajados,
            `${horasTotales}h ${minutosTotales}m`,
            `${promedioHoras}h ${promedioMinutos}m`,
            user.primeraAsistencia || 'N/A',
            user.ultimaAsistencia || 'N/A',
            estado
          ])
        })
      
      return analisisData
    },

    generarAnalisisTemporal(asistencias) {
      const analisisPorFecha = new Map()
      const analisisPorDia = new Map()
      const analisisPorHora = new Map()
      
      asistencias.forEach(asistencia => {
        // Análisis por fecha
        if (asistencia.fecha) {
          if (!analisisPorFecha.has(asistencia.fecha)) {
            analisisPorFecha.set(asistencia.fecha, {
              entradas: 0,
              salidas: 0,
              completas: 0,
              usuarios: new Set()
            })
          }
          const fechaData = analisisPorFecha.get(asistencia.fecha)
          fechaData.usuarios.add(asistencia.usuario_id)
          if (asistencia.hora_entrada) fechaData.entradas++
          if (asistencia.hora_salida) fechaData.salidas++
          if (asistencia.hora_entrada && asistencia.hora_salida) fechaData.completas++
        }
        
        // Análisis por día de la semana
        if (asistencia.fecha) {
          const diaSemana = this.formatearFechaConDia(asistencia.fecha)
          if (!analisisPorDia.has(diaSemana)) {
            analisisPorDia.set(diaSemana, { count: 0, completas: 0 })
          }
          analisisPorDia.get(diaSemana).count++
          if (asistencia.hora_entrada && asistencia.hora_salida) {
            analisisPorDia.get(diaSemana).completas++
          }
        }
        
        // Análisis por hora de entrada
        if (asistencia.hora_entrada) {
          const hora = asistencia.hora_entrada.split(':')[0]
          if (!analisisPorHora.has(hora)) {
            analisisPorHora.set(hora, 0)
          }
          analisisPorHora.set(hora, analisisPorHora.get(hora) + 1)
        }
      })
      
      const analisisData = [
        ['📅 ANÁLISIS TEMPORAL DE ASISTENCIAS'],
        [''],
        ['=== ANÁLISIS POR FECHA ==='],
        ['Fecha', 'Usuarios Únicos', 'Entradas', 'Salidas', 'Completas', 'Eficiencia %']
      ]
      
      // Agregar datos por fecha
      Array.from(analisisPorFecha.entries())
        .sort(([a], [b]) => new Date(b) - new Date(a))
        .slice(0, 30) // Últimas 30 fechas
        .forEach(([fecha, data]) => {
          const eficiencia = data.entradas > 0 ? ((data.completas / data.entradas) * 100).toFixed(1) : 0
          analisisData.push([
            this.formatearFechaSimple(fecha),
            data.usuarios.size,
            data.entradas,
            data.salidas,
            data.completas,
            `${eficiencia}%`
          ])
        })
      
      analisisData.push([''], ['=== ANÁLISIS POR DÍA DE LA SEMANA ==='])
      analisisData.push(['Día', 'Total Asistencias', 'Completas', 'Porcentaje Finalización'])
      
      Array.from(analisisPorDia.entries())
        .forEach(([dia, data]) => {
          const porcentaje = data.count > 0 ? ((data.completas / data.count) * 100).toFixed(1) : 0
          analisisData.push([dia, data.count, data.completas, `${porcentaje}%`])
        })
      
      analisisData.push([''], ['=== ANÁLISIS POR HORA DE ENTRADA ==='])
      analisisData.push(['Hora', 'Cantidad de Entradas', 'Porcentaje del Total'])
      
      const totalEntradas = Array.from(analisisPorHora.values()).reduce((a, b) => a + b, 0)
      Array.from(analisisPorHora.entries())
        .sort(([a], [b]) => parseInt(a) - parseInt(b))
        .forEach(([hora, count]) => {
          const porcentaje = totalEntradas > 0 ? ((count / totalEntradas) * 100).toFixed(1) : 0
          analisisData.push([`${hora}:00`, count, `${porcentaje}%`])
        })
      
      return analisisData
    },

    generarMapaUbicaciones(asistencias) {
      const ubicacionesData = [
        ['📍 MAPA DE UBICACIONES DE ASISTENCIAS'],
        [''],
        ['Tipo', 'Usuario', 'Fecha', 'Hora', 'Latitud', 'Longitud', 'Descripción', 'Precisión GPS']
      ]
      
      asistencias.forEach(asistencia => {
        // Ubicación de entrada
        if (asistencia.latitud_entrada && asistencia.longitud_entrada) {
          ubicacionesData.push([
            '🏁 Entrada',
            asistencia.nombre_usuario || `Usuario ${asistencia.usuario_id}`,
            asistencia.fecha ? this.formatearFechaSimple(asistencia.fecha) : '',
            asistencia.hora_entrada || '',
            parseFloat(asistencia.latitud_entrada).toFixed(6),
            parseFloat(asistencia.longitud_entrada).toFixed(6),
            asistencia.descripcion_entrada || 'Sin descripción',
            'Alta'
          ])
        }
        
        // Ubicación de salida
        if (asistencia.latitud_salida && asistencia.longitud_salida) {
          ubicacionesData.push([
            '🏁 Salida',
            asistencia.nombre_usuario || `Usuario ${asistencia.usuario_id}`,
            asistencia.fecha ? this.formatearFechaSimple(asistencia.fecha) : '',
            asistencia.hora_salida || '',
            parseFloat(asistencia.latitud_salida).toFixed(6),
            parseFloat(asistencia.longitud_salida).toFixed(6),
            asistencia.descripcion_salida || 'Sin descripción',
            'Alta'
          ])
        }
      })
      
      return ubicacionesData
    },

    aplicarEstilosResumen(worksheet) {
      // Configurar ancho de columnas
      const cols = [
        { wch: 30 }, // Columna A - Etiquetas
        { wch: 40 }  // Columna B - Valores
      ]
      worksheet['!cols'] = cols
      
      // Aplicar formato a celdas específicas
      if (worksheet['A1']) {
        worksheet['A1'].s = {
          font: { bold: true, sz: 16, color: { rgb: "FFFFFF" } },
          fill: { patternType: "solid", fgColor: { rgb: "4CAF50" } },
          alignment: { horizontal: "center" }
        }
      }
    },

    aplicarEstilosDetallados(worksheet, totalRows) {
      // Configurar ancho de columnas
      const cols = [
        { wch: 12 }, // ID Usuario
        { wch: 20 }, // Nombre
        { wch: 25 }, // Email
        { wch: 12 }, // Fecha
        { wch: 12 }, // Día
        { wch: 12 }, // Entrada
        { wch: 12 }, // Salida
        { wch: 15 }, // Tiempo
        { wch: 15 }, // Estado
        { wch: 12 }, // Lat Entrada
        { wch: 12 }, // Lng Entrada
        { wch: 12 }, // Lat Salida
        { wch: 12 }, // Lng Salida
        { wch: 20 }, // Desc Entrada
        { wch: 20 }, // Desc Salida
        { wch: 15 }, // Departamento
        { wch: 20 }  // Observaciones
      ]
      worksheet['!cols'] = cols
      
      // Aplicar filtros automáticos
      if (totalRows > 1) {
        worksheet['!autofilter'] = { ref: `A1:Q${totalRows}` }
      }
    },

    aplicarEstilosAnalisisUsuarios(worksheet) {
      const cols = [
        { wch: 25 }, // Usuario
        { wch: 30 }, // Email
        { wch: 15 }, // Total
        { wch: 12 }, // Completas
        { wch: 12 }, // En Curso
        { wch: 12 }, // Sin Entrada
        { wch: 15 }, // Días
        { wch: 15 }, // Tiempo Total
        { wch: 15 }, // Promedio
        { wch: 15 }, // Primera
        { wch: 15 }, // Última
        { wch: 15 }  // Estado
      ]
      worksheet['!cols'] = cols
    },

    aplicarEstilosAnalisisTemporal(worksheet) {
      const cols = [
        { wch: 15 }, // Fecha/Día/Hora
        { wch: 15 }, // Usuarios/Total
        { wch: 12 }, // Entradas
        { wch: 12 }, // Salidas
        { wch: 12 }, // Completas
        { wch: 15 }  // Eficiencia/Porcentaje
      ]
      worksheet['!cols'] = cols
    },

    aplicarEstilosUbicaciones(worksheet) {
      const cols = [
        { wch: 12 }, // Tipo
        { wch: 20 }, // Usuario
        { wch: 12 }, // Fecha
        { wch: 10 }, // Hora
        { wch: 15 }, // Latitud
        { wch: 15 }, // Longitud
        { wch: 25 }, // Descripción
        { wch: 12 }  // Precisión
      ]
      worksheet['!cols'] = cols
    },

    mostrarNotificacionExito(titulo, mensaje) {
      // Implementar notificación de éxito (puede usar toast, alert, etc.)
      console.log(`✅ ${titulo}: ${mensaje}`)
      alert(`${titulo}\n${mensaje}`)
    },

    mostrarNotificacionError(titulo, mensaje) {
      // Implementar notificación de error
      console.error(`❌ ${titulo}: ${mensaje}`)
      alert(`Error: ${titulo}\n${mensaje}`)
    },

    imprimirAsistencias() {
      // Crear ventana de impresión
      const printWindow = window.open('', '_blank', 'width=800,height=600')
      
      // Obtener datos filtrados
      const asistenciasParaImprimir = this.asistenciasFiltradas
      
      // Calcular estadísticas
      const estadisticas = {
        totalAsistencias: asistenciasParaImprimir.length,
        usuariosUnicos: [...new Set(asistenciasParaImprimir.map(a => a.usuario_id))].length,
        conEntrada: asistenciasParaImprimir.filter(a => a.hora_entrada).length,
        conSalida: asistenciasParaImprimir.filter(a => a.hora_salida).length,
        sinSalida: asistenciasParaImprimir.filter(a => a.hora_entrada && !a.hora_salida).length,
        horasPromedio: this.calcularHorasPromedio(asistenciasParaImprimir)
      }
      
      // Generar HTML para impresión
      const htmlContent = `
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reporte de Asistencias - ${this.formatearFechaSimple(new Date().toISOString())}</title>
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
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                    gap: 15px;
                    margin: 20px 0;
                    padding: 15px;
                    background: linear-gradient(135deg, #e8f5e8 0%, #f0fff4 100%);
                    border-radius: 10px;
                    border: 1px solid #4CAF50;
                    page-break-inside: avoid;
                }
                
                .stat-item {
                    text-align: center;
                    padding: 10px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                
                .stat-number {
                    font-size: 20px;
                    font-weight: bold;
                    color: #4CAF50;
                    display: block;
                }
                
                .stat-label {
                    font-size: 10px;
                    color: #666;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    margin-top: 5px;
                }
                
                .asistencias-table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    background: white;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    border-radius: 8px;
                    overflow: hidden;
                    font-size: 10px;
                }
                
                .asistencias-table th {
                    background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                    color: white;
                    padding: 10px 6px;
                    text-align: left;
                    font-weight: 600;
                    font-size: 9px;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    border-bottom: 2px solid #388e3c;
                }
                
                .asistencias-table td {
                    padding: 8px 6px;
                    border-bottom: 1px solid #eee;
                    font-size: 9px;
                    vertical-align: top;
                }
                
                .asistencias-table tbody tr:nth-child(even) {
                    background-color: #f8f9fa;
                }
                
                .asistencias-table tbody tr:hover {
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
                    font-size: 9px;
                }
                
                .usuario-email {
                    color: #666;
                    font-size: 8px;
                    font-style: italic;
                }
                
                .fecha-cell {
                    white-space: nowrap;
                    font-size: 9px;
                    line-height: 1.3;
                    text-align: center;
                }
                
                .hora-cell {
                    font-family: 'Courier New', monospace;
                    font-size: 8px;
                    font-weight: bold;
                    text-align: center;
                    line-height: 1.4;
                }
                
                .hora-entrada {
                    color: #28a745;
                }
                
                .hora-salida {
                    color: #dc3545;
                }
                
                .sin-hora {
                    color: #6c757d;
                    font-style: italic;
                }
                
                .ubicacion-cell {
                    font-family: 'Courier New', monospace;
                    font-size: 7px;
                    color: #555;
                    line-height: 1.2;
                }
                
                .descripcion-cell {
                    max-width: 150px;
                    word-wrap: break-word;
                    font-size: 8px;
                    line-height: 1.3;
                }
                
                .estado-asistencia {
                    display: inline-block;
                    padding: 2px 6px;
                    border-radius: 8px;
                    font-size: 7px;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.3px;
                    text-align: center;
                }
                
                .completa {
                    background: #d4edda;
                    color: #155724;
                    border: 1px solid #c3e6cb;
                }
                
                .incompleta {
                    background: #fff3cd;
                    color: #856404;
                    border: 1px solid #ffeaa7;
                }
                
                .sin-entrada {
                    background: #f8d7da;
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                }
                
                .tiempo-trabajado {
                    font-family: 'Courier New', monospace;
                    font-weight: bold;
                    font-size: 8px;
                    color: #495057;
                    text-align: center;
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
                        font-size: 9px;
                    }
                    
                    .print-header h1 {
                        font-size: 22px;
                    }
                    
                    .asistencias-table {
                        box-shadow: none;
                        font-size: 8px;
                    }
                    
                    .asistencias-table th {
                        background: #4CAF50 !important;
                        -webkit-print-color-adjust: exact;
                        color-adjust: exact;
                    }
                    
                    .summary-stats {
                        background: #e8f5e8 !important;
                        -webkit-print-color-adjust: exact;
                        color-adjust: exact;
                    }
                    
                    .asistencias-table tbody tr:nth-child(even) {
                        background-color: #f8f9fa !important;
                        -webkit-print-color-adjust: exact;
                        color-adjust: exact;
                    }
                    
                    .stat-item {
                        background: white !important;
                        -webkit-print-color-adjust: exact;
                        color-adjust: exact;
                    }
                    
                    .completa {
                        background: #d4edda !important;
                        -webkit-print-color-adjust: exact;
                        color-adjust: exact;
                    }
                    
                    .incompleta {
                        background: #fff3cd !important;
                        -webkit-print-color-adjust: exact;
                        color-adjust: exact;
                    }
                    
                    .sin-entrada {
                        background: #f8d7da !important;
                        -webkit-print-color-adjust: exact;
                        color-adjust: exact;
                    }
                    
                    /* Evitar quiebres de página en elementos importantes */
                    .print-header,
                    .summary-stats,
                    .asistencias-table thead {
                        page-break-inside: avoid;
                    }
                    
                    .asistencias-table tbody tr {
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
                <h1>⏰ Reporte de Asistencias</h1>
                <div class="subtitle">Sistema de Control de Asistencia - PWA Sembrando Vida</div>
                <div class="date-range">
                    📅 Generado el ${new Date().toLocaleDateString('es-ES', { 
                        timeZone: 'America/Mexico_City',
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
                    <span class="stat-number">${estadisticas.totalAsistencias}</span>
                    <span class="stat-label">Total Asistencias</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">${estadisticas.usuariosUnicos}</span>
                    <span class="stat-label">Usuarios Únicos</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">${estadisticas.conEntrada}</span>
                    <span class="stat-label">Con Entrada</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">${estadisticas.conSalida}</span>
                    <span class="stat-label">Con Salida</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">${estadisticas.sinSalida}</span>
                    <span class="stat-label">Sin Salida</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">${estadisticas.horasPromedio}</span>
                    <span class="stat-label">Hrs Promedio</span>
                </div>
            </div>
            
            <table class="asistencias-table">
                <thead>
                    <tr>
                        <th style="width: 18%;">Usuario</th>
                        <th style="width: 10%;">Fecha</th>
                        <th style="width: 10%;">Entrada</th>
                        <th style="width: 10%;">Salida</th>
                        <th style="width: 10%;">Tiempo</th>
                        <th style="width: 15%;">Ubicación Entrada</th>
                        <th style="width: 15%;">Ubicación Salida</th>
                        <th style="width: 12%;">Estado</th>
                    </tr>
                </thead>
                <tbody>
                    ${asistenciasParaImprimir.map(asistencia => {
                        const tiempoTrabajado = this.calcularTiempoTrabajado(asistencia)
                        const estadoAsistencia = this.obtenerEstadoAsistencia(asistencia)
                        
                        return `
                            <tr>
                                <td>
                                    <div class="usuario-info">
                                        <span class="usuario-nombre">${asistencia.nombre_usuario || `Usuario ${asistencia.usuario_id}`}</span>
                                        <span class="usuario-email">${asistencia.correo_usuario || 'No disponible'}</span>
                                    </div>
                                </td>
                                <td class="fecha-cell">
                                    ${asistencia.fecha ? this.formatearFechaSimple(asistencia.fecha) : 'No disponible'}
                                </td>
                                <td class="hora-cell">
                                    <span class="${asistencia.hora_entrada ? 'hora-entrada' : 'sin-hora'}">
                                        ${asistencia.hora_entrada || 'Sin entrada'}
                                    </span>
                                </td>
                                <td class="hora-cell">
                                    <span class="${asistencia.hora_salida ? 'hora-salida' : 'sin-hora'}">
                                        ${asistencia.hora_salida || 'Sin salida'}
                                    </span>
                                </td>
                                <td class="tiempo-trabajado">
                                    ${tiempoTrabajado}
                                </td>
                                <td class="ubicacion-cell">
                                    ${asistencia.latitud_entrada && asistencia.longitud_entrada ? 
                                        `${parseFloat(asistencia.latitud_entrada).toFixed(4)}, ${parseFloat(asistencia.longitud_entrada).toFixed(4)}` : 
                                        'No disponible'}
                                </td>
                                <td class="ubicacion-cell">
                                    ${asistencia.latitud_salida && asistencia.longitud_salida ? 
                                        `${parseFloat(asistencia.latitud_salida).toFixed(4)}, ${parseFloat(asistencia.longitud_salida).toFixed(4)}` : 
                                        'No disponible'}
                                </td>
                                <td>
                                    <span class="estado-asistencia ${estadoAsistencia.clase}">
                                        ${estadoAsistencia.texto}
                                    </span>
                                </td>
                            </tr>
                        `
                    }).join('')}
                </tbody>
            </table>
            
            <div class="print-footer">
                <div class="generated-info">
                    🖨️ Documento generado automáticamente por el Sistema de Control de Asistencia PWA
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
    },

    calcularHorasPromedio(asistencias) {
      const asistenciasCompletas = asistencias.filter(a => a.hora_entrada && a.hora_salida)
      if (asistenciasCompletas.length === 0) return '0.0'
      
      let totalMinutos = 0
      asistenciasCompletas.forEach(asistencia => {
        const entrada = new Date(`${asistencia.fecha} ${asistencia.hora_entrada}`)
        const salida = new Date(`${asistencia.fecha} ${asistencia.hora_salida}`)
        const diferencia = salida - entrada
        totalMinutos += diferencia / (1000 * 60)
      })
      
      const promedioHoras = totalMinutos / asistenciasCompletas.length / 60
      return promedioHoras.toFixed(1)
    },

    calcularTiempoTrabajado(asistencia) {
      if (!asistencia.hora_entrada || !asistencia.hora_salida) {
        return asistencia.hora_entrada ? 'En curso' : '--'
      }
      
      try {
        const entrada = new Date(`${asistencia.fecha} ${asistencia.hora_entrada}`)
        const salida = new Date(`${asistencia.fecha} ${asistencia.hora_salida}`)
        const diferencia = salida - entrada
        
        if (diferencia < 0) return 'Error'
        
        const horas = Math.floor(diferencia / (1000 * 60 * 60))
        const minutos = Math.floor((diferencia % (1000 * 60 * 60)) / (1000 * 60))
        
        return `${horas}h ${minutos}m`
      } catch (error) {
        return 'Error'
      }
    },

    obtenerEstadoAsistencia(asistencia) {
      if (!asistencia.hora_entrada) {
        return { clase: 'sin-entrada', texto: '❌ Sin Entrada' }
      } else if (!asistencia.hora_salida) {
        return { clase: 'incompleta', texto: '⏳ En Curso' }
      } else {
        return { clase: 'completa', texto: '✅ Completa' }
      }
    },

    formatearFechaCorta(fechaStr) {
      if (!fechaStr) return ''
      
      try {
        // Si viene una fecha ISO completa (con T), la procesamos con zona horaria
        if (typeof fechaStr === 'string' && fechaStr.includes('T')) {
          return new Date(fechaStr).toLocaleDateString('es-ES', {
            timeZone: 'America/Mexico_City', // Forzar zona horaria de México
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
          })
        }
        
        // Si viene solo una fecha (YYYY-MM-DD), crear la fecha sin zona horaria
        if (typeof fechaStr === 'string' && fechaStr.match(/^\d{4}-\d{2}-\d{2}$/)) {
          const [year, month, day] = fechaStr.split('-').map(num => parseInt(num, 10))
          const fecha = new Date(year, month - 1, day) // month - 1 porque los meses en JS van de 0-11
          
          return fecha.toLocaleDateString('es-ES', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
          })
        }
        
        // Para otros casos, usar el método estándar
        const fecha = new Date(fechaStr)
        return fecha.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' })
      } catch (e) {
        console.error('Error al formatear fecha corta:', e, 'Fecha original:', fechaStr)
        return fechaStr
      }
    },

    // Nueva función utilitaria para formatear fechas con día de la semana
    formatearFechaConDia(fechaStr) {
      if (!fechaStr) return ''
      
      try {
        // Si viene una fecha ISO completa (con T), la procesamos con zona horaria
        if (typeof fechaStr === 'string' && fechaStr.includes('T')) {
          return new Date(fechaStr).toLocaleDateString('es-ES', {
            timeZone: 'America/Mexico_City', // Forzar zona horaria de México
            weekday: 'long'
          })
        }
        
        // Si viene solo una fecha (YYYY-MM-DD), crear la fecha sin zona horaria
        if (typeof fechaStr === 'string' && fechaStr.match(/^\d{4}-\d{2}-\d{2}$/)) {
          const [year, month, day] = fechaStr.split('-').map(num => parseInt(num, 10))
          const fecha = new Date(year, month - 1, day) // month - 1 porque los meses en JS van de 0-11
          
          return fecha.toLocaleDateString('es-ES', { weekday: 'long' })
        }
        
        // Para otros casos, usar el método estándar
        return new Date(fechaStr).toLocaleDateString('es-ES', { weekday: 'long' })
      } catch (e) {
        console.error('Error al formatear fecha con día:', e, 'Fecha original:', fechaStr)
        return fechaStr
      }
    },

    // Nueva función utilitaria para formatear fechas simples (DD/MM/YYYY)
    formatearFechaSimple(fechaStr) {
      if (!fechaStr) return ''
      
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
        console.error('Error al formatear fecha simple:', e, 'Fecha original:', fechaStr)
        return fechaStr
      }
    },

    logout() {
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_user')
      this.$router.push('/login')
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
  margin-left: min(220px, 18vw);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  width: calc(100vw - min(220px, 18vw));
  overflow-x: hidden;
}

/* HEADER ULTRA RESPONSIVE */
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

/* Responsive improvements for smaller screens */
@media (max-width: 768px) {
  .page-header {
    padding: clamp(0.3rem, 1vw, 0.5rem);
  }
  
  .header-content {
    flex-direction: column;
    gap: clamp(0.75rem, 2vw, 1rem);
    align-items: stretch;
    text-align: center;
  }
}

/* CONTENIDO ULTRA RESPONSIVE - APROVECHA TODO EL ANCHO */
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
  min-width: clamp(110px, 18vw, 130px);
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

/* ESTILOS PARA CONTADORES COMPACTOS EN FILTROS - EXACTO COMO REGISTROSVIEW */
.filters-left {
  display: flex;
  flex-direction: column;
  gap: clamp(0.4rem, 1vw, 0.6rem);
  flex: 1;
  min-width: 0;
}

.filters-right {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-left: auto;
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
  font-size: clamp(8px, 1.5vw, 10px); /* Tamaño igual a usuarios-table */
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
  background: linear-gradient(135deg, #f8f9fa 0%, #f0f8f0 100%);
  padding: clamp(6px, 1.2vw, 8px) clamp(3px, 0.8vw, 5px); /* Padding igual a usuarios-table */
  text-align: center;
  font-weight: 700; /* Peso igual a usuarios-table */
  color: #4CAF50; /* Color igual a usuarios-table */
  text-transform: uppercase; /* Igual a usuarios-table */
  font-size: clamp(7px, 1.2vw, 8px); /* Tamaño igual a usuarios-table */
  letter-spacing: 0.5px; /* Igual a usuarios-table */
  border-bottom: 2px solid rgba(76, 175, 80, 0.2); /* Igual a usuarios-table */
  position: sticky;
  top: 0;
  z-index: 10;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.asistencias-table td {
  padding: clamp(4px, 1vw, 6px) clamp(2px, 0.6vw, 4px); /* Padding igual a usuarios-table */
  border-bottom: 1px solid rgba(224, 224, 224, 0.6); /* Igual a usuarios-table */
  vertical-align: middle;
  text-align: center;
  font-size: clamp(8px, 1.5vw, 10px); /* Tamaño igual a usuarios-table */
  transition: all 0.3s ease; /* Igual a usuarios-table */
  color: #444; /* Igual a usuarios-table */
  font-weight: 500; /* Igual a usuarios-table */
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Estilos específicos por columna para mejor responsividad */
.asistencias-table td:nth-child(1) { /* Usuario */
  white-space: nowrap;
}

.asistencias-table td:nth-child(2) { /* Correo - permitir wrap */
  white-space: normal;
  word-break: break-word;
  hyphens: auto;
  line-height: 1.2;
  max-width: 0; /* Forzar que respete el width */
  font-family: Arial, sans-serif; /* Fuente Arial */
  font-size: clamp(8px, 1.4vw, 9px); /* Mismo tamaño que user-name */
  color: #5d4037; /* Color café oscuro */
  font-weight: 700; /* Negritas (bold) */
  font-style: italic; /* Cursiva/de lado */
}

.asistencias-table td:nth-child(3) { /* Fecha */
  white-space: nowrap;
}

.asistencias-table td:nth-child(4), /* Entrada */
.asistencias-table td:nth-child(5) { /* Salida */
  white-space: nowrap;
}

.asistencias-table td:nth-child(6), /* Ubicación Entrada */
.asistencias-table td:nth-child(7) { /* Ubicación Salida */
  white-space: normal;
  word-break: break-word;
}

.asistencias-table td:nth-child(8) { /* Fotos */
  white-space: nowrap;
}

.asistencias-table td:nth-child(9) { /* Observaciones - permitir wrap */
  white-space: normal;
  word-break: break-word;
  hyphens: auto;
  line-height: 1.3;
  max-width: 0; /* Forzar que respete el width */
  text-align: left; /* Mejor lectura para texto largo */
  padding-left: clamp(4px, 1vw, 6px);
}

.asistencias-table tr:hover {
  background: rgba(76, 175, 80, 0.05);
}

/* ESTILOS ESPECÍFICOS DE CELDAS - COMPACTO COMO USUARIOS */
.user-info {
  display: flex;
  align-items: center;
  gap: clamp(0.25rem, 0.8vw, 0.35rem); /* Gap más pequeño */
  justify-content: center;
  text-align: center;
}

.user-avatar {
  width: clamp(20px, 3vw, 24px); /* Avatar más pequeño */
  height: clamp(20px, 3vw, 24px);
  background: linear-gradient(135deg, #4CAF50, #45a049);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: clamp(7px, 1.2vw, 8px); /* Texto más pequeño */
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
  font-size: clamp(8px, 1.4vw, 9px); /* Nombre más pequeño */
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  width: 100%;
}

.user-cargo {
  font-size: clamp(7px, 1.1vw, 8px); /* Cargo más pequeño */
  color: #718096;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  width: 100%;
}

.date-badge {
  background: rgba(96, 96, 96, 0.1);
  color: #424242;
  padding: clamp(2px, 0.4vw, 3px) clamp(4px, 0.8vw, 6px); /* Padding más pequeño */
  border-radius: clamp(6px, 1.2vw, 8px); /* Border radius más pequeño */
  font-weight: 500;
  font-size: clamp(7px, 1.2vw, 8px); /* Tamaño más pequeño */
  font-style: italic;
  white-space: nowrap;
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}

.time-badge {
  padding: clamp(2px, 0.4vw, 3px) clamp(4px, 0.8vw, 6px); /* Padding más pequeño */
  border-radius: clamp(6px, 1.2vw, 8px); /* Border radius más pequeño */
  font-weight: 500;
  font-size: clamp(7px, 1.2vw, 8px); /* Tamaño más pequeño */
  white-space: nowrap;
  display: inline-block;
  min-width: clamp(35px, 8vw, 45px); /* Ancho mínimo más pequeño */
  text-align: center;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}

.time-badge.entrada {
  background: rgba(30, 144, 255, 0.1);
  color: #1e90ff;
}

.time-badge.salida {
  background: rgba(220, 20, 60, 0.1);
  color: #dc143c;
}

/* Estilos específicos para columnas de hora */
.asistencias-table th:nth-child(4),
.asistencias-table th:nth-child(5),
.asistencias-table td:nth-child(4),
.asistencias-table td:nth-child(5) {
  min-width: 70px; /* Ancho mínimo más pequeño */
  white-space: nowrap;
  text-align: center;
}

/* Estilos específicos para columnas de ubicación */
.asistencias-table th:nth-child(6),
.asistencias-table th:nth-child(7),
.asistencias-table td:nth-child(6),
.asistencias-table td:nth-child(7) {
  min-width: 120px; /* Ancho mínimo más pequeño */
  max-width: 150px; /* Ancho máximo más pequeño */
  padding: clamp(4px, 1vw, 6px) clamp(2px, 0.6vw, 4px); /* Padding igual a usuarios-table */
}

/* UBICACIONES ULTRA RESPONSIVE */
.location-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: clamp(2px, 0.8vw, 4px); /* Gap más pequeño */
  text-align: center;
  min-height: clamp(28px, 4vw, 32px); /* Altura mínima más pequeña */
  padding: clamp(2px, 0.6vw, 4px); /* Padding más pequeño */
  word-break: break-word; /* Permitir división de palabras largas */
}

.location-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: clamp(2px, 0.4vw, 3px);
  width: 100%;
  min-width: 0; /* Permitir contracción */
}

.location-actions {
  display: flex;
  justify-content: center;
  width: 100%;
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
  padding: clamp(2px, 0.3vw, 3px) clamp(4px, 0.6vw, 6px); /* Padding más pequeño */
  border-radius: clamp(4px, 1vw, 6px); /* Border radius más pequeño */
  font-size: clamp(7px, 1.1vw, 8px); /* Tamaño más pequeño */
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
  font-size: clamp(7px, 1vw, 8px); /* Tamaño más pequeño */
  padding: clamp(2px, 0.2vw, 3px) clamp(4px, 0.4vw, 5px); /* Padding más pequeño */
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
  width: clamp(20px, 3vw, 24px); /* Botón más pequeño */
  height: clamp(20px, 3vw, 24px);
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
  background: linear-gradient(135deg, #1e90ff, #1976d2);
}

.map-btn.entrada-map:hover {
  background: linear-gradient(135deg, #1976d2, #1565c0);
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 6px 20px rgba(30, 144, 255, 0.4);
}

.map-btn.salida-map {
  background: linear-gradient(135deg, #dc143c, #b71c1c);
}

.map-btn.salida-map:hover {
  background: linear-gradient(135deg, #b71c1c, #c62828);
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 6px 20px rgba(220, 20, 60, 0.4);
}

.map-btn:active {
  transform: translateY(0) scale(0.95);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* FOTOS Y OBSERVACIONES ULTRA RESPONSIVE */
.photos-cell {
  display: flex;
  flex-direction: column;
  gap: clamp(2px, 0.6vw, 4px); /* Gap más pequeño */
  align-items: center;
  justify-content: center;
  text-align: center;
}

.photo-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(2px, 0.6vw, 4px); /* Gap más pequeño */
  flex-direction: column;
}

.photo-thumbnail {
  width: clamp(20px, 3vw, 24px); /* Thumbnail más pequeño */
  height: clamp(20px, 3vw, 24px);
  object-fit: cover;
  border-radius: clamp(4px, 1vw, 6px); /* Border radius más pequeño */
  cursor: pointer;
  transition: transform 0.2s ease;
  border: 1px solid #e2e8f0; /* Border más delgado */
  flex-shrink: 0;
}

.photo-thumbnail:hover {
  transform: scale(1.1);
  border-color: #4CAF50;
}

.photo-label {
  font-size: clamp(7px, 1vw, 8px); /* Tamaño más pequeño */
  color: #718096;
  white-space: nowrap;
}

.observations-cell {
  text-align: left; /* Cambiado a izquierda para mejor lectura */
  max-width: 100%;
  word-wrap: break-word;
  hyphens: auto;
  line-height: 1.3;
  padding: clamp(4px, 1vw, 6px); /* Padding consistente */
}

.observation-item {
  margin-bottom: clamp(2px, 0.6vw, 3px); /* Margen más pequeño */
  font-size: clamp(7px, 1.2vw, 8px); /* Tamaño más pequeño */
  line-height: 1.3;
  word-break: break-word;
  text-align: left; /* Alineación izquierda */
}

.observation-item:last-child {
  margin-bottom: 0;
}

.observation-item strong {
  color: #4CAF50; /* Color destacado para las etiquetas */
  font-weight: 600;
  display: inline-block;
  margin-right: 4px;
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
  font-size: clamp(7px, 1.1vw, 8px); /* Tamaño más pequeño */
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
@media (max-width: 992px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
    overflow-x: hidden !important;
  }
}

@media (min-width: 481px) and (max-width: 768px) {
  .main-content {
    margin-left: 250px;
    width: calc(100vw - 250px);
    overflow-x: hidden !important;
  }
}

@media (max-width: 768px) and (orientation: landscape) {
  .main-content {
    margin-left: 160px;
    width: calc(100vw - 160px);
    overflow-x: hidden !important;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 240px;
    width: calc(100vw - 240px);
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
    font-size: clamp(7px, 1.4vw, 9px); /* Tamaño más pequeño para móvil */
  }
  
  .asistencias-table th,
  .asistencias-table td {
    padding: clamp(3px, 0.8vw, 5px); /* Padding más pequeño para móvil */
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
    gap: clamp(2px, 0.8vw, 4px); /* Gap más pequeño */
  }

  /* Estilos específicos para correo en tablet */
  .asistencias-table td:nth-child(2) { /* Correo */
    font-family: Arial, sans-serif; /* Fuente Arial */
    font-size: clamp(7px, 1.3vw, 8px); /* Tamaño consistente */
    color: #5d4037; /* Color café oscuro */
    font-weight: 700; /* Negritas (bold) */
    font-style: italic; /* Cursiva/de lado */
  }

  .location-cell {
    gap: clamp(2px, 0.6vw, 3px); /* Gap más pequeño */
  }

  .location-badge.compact {
    font-size: clamp(6px, 1vw, 7px); /* Tamaño más pequeño */
    padding: clamp(1px, 0.2vw, 2px) clamp(3px, 0.4vw, 4px); /* Padding más pequeño */
  }

  .map-btn.circular {
    width: clamp(18px, 4vw, 20px); /* Botón más pequeño */
    height: clamp(18px, 4vw, 20px);
  }

  .map-btn svg {
    width: clamp(8px, 2vw, 10px); /* Icono más pequeño */
    height: clamp(8px, 2vw, 10px);
  }

  .photo-thumbnail {
    width: clamp(18px, 4vw, 20px); /* Thumbnail más pequeño */
    height: clamp(18px, 4vw, 20px);
  }

  .time-badge {
    min-width: clamp(30px, 6vw, 35px); /* Ancho mínimo más pequeño */
    padding: clamp(2px, 0.3vw, 3px) clamp(4px, 0.8vw, 6px); /* Padding más pequeño */
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
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
    overflow-x: hidden !important;
  }
  
  .asistencias-table {
    font-size: clamp(7px, 1.8vw, 8px); /* Tamaño más pequeño y consistente */
  }
  
  .asistencias-table th,
  .asistencias-table td {
    padding: clamp(3px, 0.8vw, 4px) clamp(1px, 0.4vw, 2px); /* Padding extra compacto */
  }

  .user-name {
    font-size: clamp(7px, 1.6vw, 8px); /* Tamaño más pequeño */
  }

  .user-cargo {
    font-size: clamp(6px, 1.3vw, 7px); /* Tamaño más pequeño */
  }

  .user-avatar {
    width: clamp(16px, 3vw, 18px); /* Avatar extra pequeño */
    height: clamp(16px, 3vw, 18px);
    font-size: clamp(6px, 1.2vw, 7px);
  }

  .time-badge,
  .date-badge {
    font-size: clamp(6px, 1.2vw, 7px); /* Badges más pequeños */
    padding: clamp(1px, 0.2vw, 2px) clamp(3px, 0.6vw, 4px);
  }

  .location-badge.compact {
    font-size: clamp(5px, 1vw, 6px); /* Location badge extra pequeño */
    padding: clamp(1px, 0.1vw, 2px) clamp(2px, 0.3vw, 3px);
  }

  .photo-thumbnail {
    width: clamp(14px, 3vw, 16px); /* Thumbnails extra pequeños */
    height: clamp(14px, 3vw, 16px);
  }

  .map-btn.circular {
    width: clamp(14px, 3vw, 16px); /* Botones extra pequeños */
    height: clamp(14px, 3vw, 16px);
  }

  .observation-item {
    font-size: clamp(6px, 1.2vw, 7px); /* Observaciones más pequeñas */
    line-height: 1.2;
  }

  .no-data {
    font-size: clamp(6px, 1.1vw, 7px); /* No-data más pequeño */
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

  /* Ajustes específicos para mejorar la lectura en móvil */
  .asistencias-table td:nth-child(2) { /* Correo */
    font-size: clamp(7px, 1.2vw, 8px); /* Mismo tamaño que user-name en móvil */
    line-height: 1.1;
    font-family: Arial, sans-serif; /* Fuente Arial */
    color: #5d4037; /* Color café oscuro */
    font-weight: 700; /* Negritas (bold) */
    font-style: italic; /* Cursiva/de lado */
  }

  .asistencias-table td:nth-child(9) { /* Observaciones */
    text-align: left;
    padding-left: clamp(2px, 0.5vw, 3px);
  }
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
}

@media (max-width: 375px) {
  .main-content {
    margin-left: 180px;
    width: calc(100vw - 180px);
    overflow-x: hidden !important;
  }
}
</style>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
</style>
