<template>
  <div class="historiales-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Gestión de Historiales</h1>
              <p class="header-subtitle">Consulta y gestiona el historial completo de actividades de los usuarios</p>
            </div>
          </div>
          <div class="header-actions">
            <button @click="actualizarHistorial" class="refresh-btn" :disabled="loading">
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
        <!-- Buscador de Usuario -->
        <div class="user-selection-section">
          <div class="selection-card">
            <div class="selection-header">
              <h3>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="m21 21-4.35-4.35"></path>
                </svg>
                Buscar Usuario
              </h3>
            </div>
            <div class="user-search-container">
              <div class="search-input-wrapper">
                <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="m21 21-4.35-4.35"></path>
                </svg>
                <input 
                  v-model="terminoBusqueda" 
                  type="text" 
                  placeholder="Buscar por nombre, correo o CURP..." 
                  class="search-input"
                  @input="buscarUsuarios"
                  @focus="mostrarResultados = true"
                  @blur="setTimeout(() => mostrarResultados = false, 150)"
                >
              </div>
            </div>
            
            <!-- Resultados de búsqueda - Dropdown flotante independiente -->
            <div v-if="mostrarResultados && terminoBusqueda.length > 0" class="search-results-dropdown">
              <div v-if="buscandoUsuarios" class="loading-search">
                <div class="spinner-small"></div>
                <span>Buscando...</span>
              </div>
              <div v-else-if="terminoBusqueda.length < 2" class="need-more-chars">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"></circle>
                  <path d="M12 8v4m0 4h.01"></path>
                </svg>
                <p>Escribe al menos 2 caracteres para buscar</p>
              </div>
              <div v-else-if="usuariosFiltrados.length === 0" class="no-results">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="m21 21-4.35-4.35"></path>
                </svg>
                <p>No se encontraron usuarios</p>
              </div>
              <div v-else class="results-list">
                <div 
                  v-for="usuario in usuariosFiltrados" 
                  :key="usuario.id" 
                  :class="['result-item', { active: usuarioSeleccionado === usuario.id.toString() }]"
                  @click="seleccionarUsuario(usuario)"
                >
                  <div class="user-avatar">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                      <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                  </div>
                  <div class="user-info">
                    <div class="user-name">{{ usuario.nombre_completo }}</div>
                    <div class="user-details">
                      <span class="user-email">{{ usuario.correo }}</span>
                      <span v-if="usuario.curp" class="user-curp">• {{ usuario.curp }}</span>
                    </div>
                    <div v-if="usuario.cargo" class="user-cargo">{{ usuario.cargo }}</div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Usuario seleccionado -->
            <div v-if="usuarioActual" class="selected-user">
              <div class="selected-user-header">
                <h4>Usuario Seleccionado:</h4>
                <button @click="limpiarSeleccion" class="clear-selection-btn">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                  Limpiar selección
                </button>
              </div>
              <div class="selected-user-card">
                <div class="selected-user-avatar">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                </div>
                <div class="selected-user-info">
                  <div class="selected-user-name">{{ usuarioActual.nombre_completo }}</div>
                  <div class="selected-user-email">{{ usuarioActual.correo }}</div>
                  <div v-if="usuarioActual.curp" class="selected-user-curp">CURP: {{ usuarioActual.curp }}</div>
                  <div v-if="usuarioActual.cargo" class="selected-user-cargo">{{ usuarioActual.cargo }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Filtros y Controles - Solo visible si hay usuario seleccionado -->
        <div v-if="usuarioSeleccionado" class="filters-section">
          <div class="filters-card">
            <div class="filters-header">
              <h3>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
                </svg>
                Filtros de Búsqueda
              </h3>
            </div>
            
            <div class="filters-grid">
              <!-- Filtros por fecha -->
              <div class="filter-group">
                <label>Tipo de período:</label>
                <div class="period-buttons">
                  <button 
                    @click="setPeriodo('dia')"
                    :class="['period-btn', { active: filtros.periodo === 'dia' }]"
                  >
                    Día
                  </button>
                  <button 
                    @click="setPeriodo('semana')"
                    :class="['period-btn', { active: filtros.periodo === 'semana' }]"
                  >
                    Semana
                  </button>
                  <button 
                    @click="setPeriodo('año')"
                    :class="['period-btn', { active: filtros.periodo === 'año' }]"
                  >
                    Año
                  </button>
                  <button 
                    @click="setPeriodo('todo')"
                    :class="['period-btn', { active: filtros.periodo === 'todo' }]"
                  >
                    Todo
                  </button>
                </div>
              </div>

              <!-- Selector de fecha específica (solo para día) -->
              <div v-if="filtros.periodo === 'dia'" class="filter-group">
                <label for="fecha-especifica">Fecha:</label>
                <input
                  id="fecha-especifica"
                  type="date"
                  v-model="filtros.fechaEspecifica"
                  @change="aplicarFiltros"
                  class="date-input"
                >
              </div>

              <!-- Selector de semana (solo para semana) -->
              <div v-if="filtros.periodo === 'semana'" class="filter-group">
                <label for="semana-especifica">Semana:</label>
                <input
                  id="semana-especifica"
                  type="week"
                  v-model="filtros.semanaEspecifica"
                  @change="aplicarFiltros"
                  class="date-input"
                >
              </div>

              <!-- Selector de año (solo para año) -->
              <div v-if="filtros.periodo === 'año'" class="filter-group">
                <label for="año-especifico">Año:</label>
                <select
                  id="año-especifico"
                  v-model="filtros.añoEspecifico"
                  @change="aplicarFiltros"
                  class="year-select"
                >
                  <option v-for="año in añosDisponibles" :key="año" :value="año">
                    {{ año }}
                  </option>
                </select>
              </div>

              <!-- Filtro por tipo -->
              <div class="filter-group">
                <label for="tipo-filtro">Tipo de actividad:</label>
                <select
                  id="tipo-filtro"
                  v-model="filtros.tipo"
                  @change="aplicarFiltros"
                  class="type-select"
                >
                  <option value="">Todos los tipos</option>
                  <option value="entrada">Entrada</option>
                  <option value="salida">Salida</option>
                  <option value="actividad">Actividad</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- Estadísticas Rápidas -->
        <div v-if="usuarioSeleccionado && resumen" class="stats-section">
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon total">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 12l2 2 4-4"></path>
                  <path d="M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9 9 4.03 9 9z"></path>
                </svg>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ resumen.estadisticas.total_registros }}</div>
                <div class="stat-label">Total Registros</div>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon entrada">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="12" y1="19" x2="12" y2="5"></line>
                  <polyline points="5,12 12,5 19,12"></polyline>
                </svg>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ resumen.estadisticas.entradas }}</div>
                <div class="stat-label">Entradas</div>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon salida">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <polyline points="19,12 12,19 5,12"></polyline>
                </svg>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ resumen.estadisticas.salidas }}</div>
                <div class="stat-label">Salidas</div>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon actividad">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="3"></circle>
                  <path d="M12 1v6m0 6v6m11-7h-6m-6 0H1"></path>
                </svg>
              </div>
              <div class="stat-content">
                <div class="stat-number">{{ resumen.estadisticas.actividades }}</div>
                <div class="stat-label">Actividades</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Historial -->
        <div v-if="usuarioSeleccionado" class="historial-section">
          <div class="historial-header">
            <h3>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              Historial de {{ usuarioActual?.nombre || 'Usuario' }}
            </h3>
            <div class="historial-actions">
              <span v-if="historial.length > 0" class="record-count">
                {{ historial.length }} registro(s) encontrado(s)
              </span>
              <button 
                v-if="historial.length > 0"
                @click="exportarExcel" 
                class="export-btn"
                :disabled="exportando"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14,2 14,8 20,8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="21"></line>
                  <line x1="8" y1="13" x2="16" y2="21"></line>
                </svg>
                {{ exportando ? 'Exportando...' : 'Exportar Excel' }}
              </button>
            </div>
          </div>

          <!-- Loading -->
          <div v-if="loading" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando historial...</p>
          </div>

          <!-- Error -->
          <div v-else-if="error" class="error-container">
            <div class="error-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="15" y1="9" x2="9" y2="15"></line>
                <line x1="9" y1="9" x2="15" y2="15"></line>
              </svg>
            </div>
            <h3>Error al cargar el historial</h3>
            <p>{{ error }}</p>
            <button @click="cargarHistorial" class="retry-btn">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
                <path d="M3 3v5h5"></path>
                <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"></path>
                <path d="M21 21v-5h-5"></path>
              </svg>
              Reintentar
            </button>
          </div>

          <!-- Sin registros -->
          <div v-else-if="historial.length === 0" class="empty-state">
            <div class="empty-icon">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <h3>No hay registros</h3>
            <p>No se encontraron registros para los filtros seleccionados.</p>
          </div>

          <!-- Tabla de historial -->
          <div v-else class="historial-table-container">
            <div class="table-wrapper">
              <table class="historial-table">
                <thead>
                  <tr>
                    <th>Origen</th>
                    <th>Tipo</th>
                    <th>Descripción</th>
                    <th>Fecha</th>
                    <th>Hora</th>
                    <th>Detalles</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="registro in historial" :key="registro.id" class="registro-row">
                    <td class="origen-cell">
                      <span :class="['origen-badge', registro.origen]">
                        {{ formatearOrigen(registro.origen) }}
                      </span>
                    </td>
                    <td class="tipo-cell">
                      <span :class="['tipo-badge', registro.tipo]">
                        {{ formatearTipo(registro.tipo) }}
                      </span>
                    </td>
                    <td class="descripcion-cell">
                      {{ registro.descripcion || 'Sin descripción' }}
                    </td>
                    <td class="fecha-cell">
                      {{ formatearFecha(registro.fecha) }}
                    </td>
                    <td class="hora-cell">
                      {{ formatearHora(registro.hora) }}
                    </td>
                    <td class="detalles-cell">
                      <div v-if="registro.detalles" class="action-container">
                        <button @click="mostrarDetalles(registro)" class="btn-ver" title="Ver detalles del registro">
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                            <circle cx="12" cy="12" r="3"/>
                          </svg>
                        </button>
                        <span class="btn-label">Detalles</span>
                      </div>
                      <span v-else class="no-details">Sin detalles</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Estado inicial -->
        <div v-else-if="!mostrarResultados || usuariosFiltrados.length === 0" class="welcome-section">
          <div class="modern-welcome-card">
            <div class="glass-background"></div>
            <div class="welcome-content">
              <div class="welcome-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <path d="m21 21-4.35-4.35"></path>
                </svg>
              </div>
              <h2>Buscar Historial de Usuario</h2>
              <p>Utiliza el buscador superior para encontrar y seleccionar un usuario.</p>
              <div class="modern-divider"></div>
              <div class="search-hint">
                <span class="hint-icon">💡</span>
                <span>Puedes buscar por nombre, correo o CURP</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal de detalles moderno y compacto -->
    <div v-if="modalDetalles.visible" class="modal-overlay-modern" @click="cerrarModalDetalles">
      <div class="modal-content-modern-horizontal" @click.stop>
        <!-- Header del modal -->
        <div class="modal-header-modern">
          <div class="modal-title-section">
            <div class="modal-icon-header">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 1v6m0 6v6m11-7h-6m-6 0H1"/>
              </svg>
            </div>
            <h3 class="modal-title-text">Detalles del Registro</h3>
          </div>
          <button @click="cerrarModalDetalles" class="btn-close-modern">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        
        <!-- Body del modal con dos columnas -->
        <div class="modal-body-modern-horizontal">
          <div v-if="modalDetalles.registro" class="modal-columns-container">
            
            <!-- Columna izquierda: Información del registro -->
            <div class="modal-column-left">
            
            <!-- Información del Usuario -->
            <div class="detail-main-info">
              <div class="detail-card-compact">
                <div class="detail-header-compact">
                  <div class="detail-icon-small">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                      <circle cx="12" cy="7" r="4"/>
                    </svg>
                  </div>
                  <span class="detail-label-compact">Información del Usuario</span>
                </div>
                <div class="detail-content-compact">
                  <div class="info-row">
                    <span class="info-label">Nombre:</span>
                    <span class="info-value">{{ modalDetalles.registro?.usuario_nombre || 'Sin nombre' }}</span>
                  </div>
                  <div class="info-row">
                    <span class="info-label">Correo:</span>
                    <span class="info-value">{{ modalDetalles.registro?.usuario_correo || 'Sin correo' }}</span>
                  </div>
                  <div class="info-row">
                    <span class="info-label">CURP:</span>
                    <span class="info-value">{{ modalDetalles.registro?.usuario_curp || 'Sin CURP' }}</span>
                  </div>
                  <div class="info-row" v-if="modalDetalles.registro?.usuario_cargo">
                    <span class="info-label">Cargo:</span>
                    <span class="info-value">{{ modalDetalles.registro?.usuario_cargo }}</span>
                  </div>
                </div>
              </div>

              <!-- Fecha y hora -->
              <div class="detail-card-compact">
                <div class="detail-header-compact">
                  <div class="detail-icon-small">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"/>
                      <polyline points="12 6 12 12 16 14"/>
                    </svg>
                  </div>
                  <span class="detail-label-compact">Fecha y Hora</span>
                </div>
                <div class="detail-content-compact">
                  <div class="info-row">
                    <span class="info-label">Fecha:</span>
                    <span class="info-value">{{ formatearFecha(modalDetalles.registro?.fecha) }}</span>
                  </div>
                  <div class="info-row">
                    <span class="info-label">Hora:</span>
                    <span class="info-value">{{ formatearHora(modalDetalles.registro?.hora) }}</span>
                  </div>
                </div>
              </div>

              <!-- Tipo y descripción -->
              <div class="detail-card-compact">
                <div class="detail-header-compact">
                  <div class="detail-icon-small">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M9 12l2 2 4-4"/>
                      <path d="M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9 9 4.03 9 9z"/>
                    </svg>
                  </div>
                  <span class="detail-label-compact">Información General</span>
                </div>
                <div class="detail-content-compact">
                  <div class="info-row">
                    <span class="info-label">Tipo:</span>
                    <span :class="['tipo-badge-modal', modalDetalles.registro?.tipo]">
                      {{ formatearTipo(modalDetalles.registro?.tipo) }}
                    </span>
                  </div>
                  <div class="info-row">
                    <span class="info-label">Descripción:</span>
                    <span class="info-value">{{ modalDetalles.registro?.descripcion || 'Sin descripción' }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Imagen si existe -->
            <div v-if="obtenerImagenUrl(modalDetalles.registro)" class="detail-image-section">
              <div class="detail-image-container">
                <img 
                  :src="obtenerImagenUrl(modalDetalles.registro)" 
                  :alt="'Imagen del registro'"
                  class="detail-image"
                  @error="onImageError"
                  @load="onImageLoad"
                  @click="abrirFotoCompleta(obtenerImagenUrl(modalDetalles.registro))"
                  style="cursor: pointer;"
                />
                <div class="image-overlay">
                  <div class="image-info">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                      <circle cx="9" cy="9" r="2"/>
                      <path d="M21 15l-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
                    </svg>
                    <span>Fotografía</span>
                  </div>
                </div>
              </div>
            </div>

            </div>

            <!-- Columna derecha: Origen, Ubicación y Mapa -->
            <div class="modal-column-right">
              <!-- Origen de Datos -->
              <div class="detail-card-compact origen-card">
                <div class="detail-header-compact">
                  <div class="detail-icon-small">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                      <path d="M6.5 2H20v20l-5.5-6-5.5 6V2"/>
                    </svg>
                  </div>
                  <span class="detail-label-compact">Origen de Datos</span>
                </div>
                <div class="detail-content-compact">
                  <span :class="['origen-badge-modal', modalDetalles.registro?.origen]">
                    {{ formatearOrigen(modalDetalles.registro?.origen) }}
                  </span>
                </div>
              </div>

              <!-- Información de ubicación -->
              <div class="detail-card-compact location-card">
                <div class="detail-header-compact">
                  <div class="detail-icon-small">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                      <circle cx="12" cy="10" r="3"/>
                    </svg>
                  </div>
                  <span class="detail-label-compact">Ubicación</span>
                </div>
                <div class="detail-content-compact">
                  <div class="location-info">
                    <div class="coordinate-row">
                      <span class="coordinate-label">Latitud</span>
                      <span class="coordinate-value">{{ obtenerUbicacion(modalDetalles.registro).latitud || 'N/A' }}</span>
                    </div>
                    <div class="coordinate-row">
                      <span class="coordinate-label">Longitud</span>
                      <span class="coordinate-value">{{ obtenerUbicacion(modalDetalles.registro).longitud || 'N/A' }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Mapa de Mapbox -->
              <div class="detail-card-compact map-card">
                <div class="detail-header-compact">
                  <div class="detail-icon-small">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polygon points="3 6 9 1 15 6 21 1 21 18 15 23 9 18 3 23"/>
                      <line x1="9" y1="1" x2="9" y2="18"/>
                      <line x1="15" y1="6" x2="15" y2="23"/>
                    </svg>
                  </div>
                  <span class="detail-label-compact">Mapa Interactivo</span>
                </div>
                <div class="detail-content-compact map-content">
                  <div id="mapbox-container" class="mapbox-container"></div>
                  <div v-if="!obtenerUbicacion(modalDetalles.registro).latitud" class="no-location-message">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                      <circle cx="12" cy="10" r="3"/>
                      <line x1="12" y1="7" x2="12" y2="13"/>
                      <line x1="12" y1="17" x2="12.01" y2="17"/>
                    </svg>
                    <p>No hay coordenadas disponibles para este registro</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Lightbox para ver foto en pantalla completa -->
    <Teleport to="body" v-if="showLightbox">
      <div class="lightbox-overlay" @click="cerrarLightbox">
        <!-- Contenedor centrado de la imagen -->
        <div class="lightbox-container" @click.stop>
          <div class="lightbox-image-wrapper">
            <img 
              :src="lightboxImageUrl" 
              alt="Fotografía en pantalla completa"
              class="lightbox-image"
              @click.stop="requestFullscreen"
            >
            <!-- Botón de cerrar dentro de la imagen -->
            <button class="lightbox-close-btn" @click.stop="cerrarLightbox">
              ×
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'
import Sidebar from '../components/Sidebar_NEW.vue'
import { useRouter } from 'vue-router'
import usuariosService from '../services/usuariosService.js'
import historialService from '../services/historialService.js'
import * as XLSX from 'xlsx'

export default {
  name: 'HistorialesView',
  components: {
    Sidebar
  },
  setup() {
    const router = useRouter()
    
    // Estados reactivos
    const isOnline = ref(navigator.onLine)
    const loading = ref(false)
    const exportando = ref(false)
    const error = ref('')
    const usuarios = ref([])
    const usuarioSeleccionado = ref('')
    const historial = ref([])
    const resumen = ref(null)
    const usuarioActual = ref(null)
    
    // Estados para búsqueda de usuarios
    const terminoBusqueda = ref('')
    const usuariosFiltrados = ref([])
    const buscandoUsuarios = ref(false)
    const mostrarResultados = ref(false)
    const timeoutBusqueda = ref(null)
    
    // Filtros
    const filtros = ref({
      periodo: 'todo', // 'dia', 'semana', 'año', 'todo'
      fechaEspecifica: new Date().toISOString().split('T')[0],
      semanaEspecifica: '',
      añoEspecifico: new Date().getFullYear(),
      tipo: '' // '', 'entrada', 'salida', 'actividad'
    })

    // Modal de detalles
    const modalDetalles = ref({
      visible: false,
      registro: null
    })

    // Lightbox para imágenes
    const showLightbox = ref(false)
    const lightboxImageUrl = ref('')

    // Años disponibles
    const añosDisponibles = computed(() => {
      const currentYear = new Date().getFullYear()
      const years = []
      for (let i = currentYear; i >= currentYear - 10; i--) {
        years.push(i)
      }
      return years
    })

    // Admin user
    const adminUser = computed(() => {
      const userData = localStorage.getItem('userData')
      if (userData) {
        const user = JSON.parse(userData)
        return user.nombre || 'Administrador'
      }
      return 'Administrador'
    })

    // Watchers
    watch(usuarioSeleccionado, (newUserId) => {
      if (newUserId && !usuarioActual.value) {
        // Solo buscar usuario si no está ya cargado (para compatibilidad con selección directa)
        const userId = parseInt(newUserId)
        usuarioActual.value = usuarios.value.find(u => u.id === userId)
        if (usuarioActual.value) {
          cargarResumen()
          cargarHistorial()
        }
      } else if (!newUserId) {
        usuarioActual.value = null
        historial.value = []
        resumen.value = null
      }
    })

    // Métodos principales
    const cargarUsuarios = async () => {
      try {
        console.log('🔍 Cargando usuarios...')
        const usuariosData = await historialService.obtenerUsuarios()
        usuarios.value = usuariosData.usuarios || usuariosData || []
        console.log(`✅ ${usuarios.value.length} usuarios cargados`)
      } catch (err) {
        console.error('❌ Error al cargar usuarios:', err)
        error.value = 'Error al cargar la lista de usuarios'
      }
    }

    const cargarHistorial = async () => {
      if (!usuarioSeleccionado.value) {
        console.log('⚠️ No hay usuario seleccionado')
        return
      }

      loading.value = true
      error.value = ''
      
      try {
        const userId = parseInt(usuarioSeleccionado.value)
        console.log('🔍 Cargando historial completo para usuario ID:', userId)
        console.log('🔍 Filtros aplicados:', filtros.value)
        
        const filtrosAPI = construirFiltrosAPI()
        console.log('🔍 Filtros API:', filtrosAPI)
        
        // Usar el nuevo método de historial completo
        const data = await historialService.obtenerHistorialCompleto(userId, filtrosAPI)
        
        historial.value = data.historial || []
        resumen.value = {
          estadisticas: data.estadisticas || {
            total_registros: 0,
            entradas: 0,
            salidas: 0,
            actividades: 0
          }
        }
        
        console.log(`✅ ${historial.value.length} registros de historial completo cargados`)
        console.log('📊 Estadísticas:', resumen.value.estadisticas)
        
        if (historial.value.length === 0) {
          console.log('⚠️ No se encontraron registros para este usuario con los filtros aplicados')
        }
        
      } catch (err) {
        console.error('❌ Error al cargar historial:', err)
        error.value = err.message || 'Error al cargar el historial'
        historial.value = []
        resumen.value = null
        
        // Si es error 404, mostrar mensaje más amigable
        if (err.message.includes('404') || err.message.includes('no encontrado')) {
          error.value = 'Usuario no encontrado o sin historial disponible'
        }
      } finally {
        loading.value = false
      }
    }

    const cargarResumen = async () => {
      // Ya no necesitamos cargar resumen por separado
      // El historial completo ya incluye las estadísticas
      console.log('📊 Resumen incluido en historial completo')
    }

    const construirFiltrosAPI = () => {
      const filtrosAPI = {}

      switch (filtros.value.periodo) {
        case 'dia':
          if (filtros.value.fechaEspecifica) {
            filtrosAPI.fechaInicio = filtros.value.fechaEspecifica
            filtrosAPI.fechaFin = filtros.value.fechaEspecifica
          }
          break
          
        case 'semana':
          if (filtros.value.semanaEspecifica) {
            const fechasSemana = calcularFechasSemana(filtros.value.semanaEspecifica)
            filtrosAPI.fechaInicio = fechasSemana.inicio
            filtrosAPI.fechaFin = fechasSemana.fin
          }
          break
          
        case 'año':
          filtrosAPI.fechaInicio = `${filtros.value.añoEspecifico}-01-01`
          filtrosAPI.fechaFin = `${filtros.value.añoEspecifico}-12-31`
          break
          
        // Para 'todo' no agregamos filtros de fecha
      }

      if (filtros.value.tipo) {
        filtrosAPI.tipo = filtros.value.tipo
      }

      return filtrosAPI
    }

    const calcularFechasSemana = (semanaString) => {
      // semanaString viene en formato "2024-W30"
      const [year, week] = semanaString.split('-W')
      const yearNum = parseInt(year)
      const weekNum = parseInt(week)
      
      // Calcular el primer día de la semana
      const firstDayOfYear = new Date(yearNum, 0, 1)
      const daysToFirstMonday = (8 - firstDayOfYear.getDay()) % 7
      const firstMonday = new Date(yearNum, 0, 1 + daysToFirstMonday)
      
      const targetDate = new Date(firstMonday)
      targetDate.setDate(firstMonday.getDate() + (weekNum - 1) * 7)
      
      const inicio = new Date(targetDate)
      const fin = new Date(targetDate)
      fin.setDate(inicio.getDate() + 6)
      
      return {
        inicio: inicio.toISOString().split('T')[0],
        fin: fin.toISOString().split('T')[0]
      }
    }

    // Métodos de UI
    const setPeriodo = (periodo) => {
      filtros.value.periodo = periodo
      
      // Configurar valores por defecto según el período
      switch (periodo) {
        case 'dia':
          filtros.value.fechaEspecifica = new Date().toISOString().split('T')[0]
          break
        case 'semana':
          const semanaActual = historialService.obtenerSemanaActual()
          const fechaActual = new Date()
          const año = fechaActual.getFullYear()
          const semana = getWeekNumber(fechaActual)
          filtros.value.semanaEspecifica = `${año}-W${semana.toString().padStart(2, '0')}`
          break
        case 'año':
          filtros.value.añoEspecifico = new Date().getFullYear()
          break
      }
      
      aplicarFiltros()
    }

    const getWeekNumber = (date) => {
      const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()))
      const dayNum = d.getUTCDay() || 7
      d.setUTCDate(d.getUTCDate() + 4 - dayNum)
      const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1))
      return Math.ceil((((d - yearStart) / 86400000) + 1) / 7)
    }

    const aplicarFiltros = () => {
      if (usuarioSeleccionado.value) {
        cargarHistorial()
      }
    }

    const actualizarHistorial = () => {
      if (usuarioSeleccionado.value) {
        cargarHistorial()
        cargarResumen()
      } else {
        cargarUsuarios()
      }
    }

    const onUsuarioChange = () => {
      error.value = ''
    }

    // Métodos de búsqueda de usuarios
    const buscarUsuarios = async () => {
      // Limpiar timeout anterior
      if (timeoutBusqueda.value) {
        clearTimeout(timeoutBusqueda.value)
      }

      const termino = terminoBusqueda.value.trim()
      console.log('🔍 Término de búsqueda:', termino, 'Longitud:', termino.length)
      
      if (termino.length === 0) {
        usuariosFiltrados.value = []
        mostrarResultados.value = false
        return
      }

      if (termino.length < 2) {
        // Mostrar mensaje de que necesita más caracteres
        usuariosFiltrados.value = []
        mostrarResultados.value = true
        return
      }

      // Debounce de 300ms
      timeoutBusqueda.value = setTimeout(async () => {
        try {
          buscandoUsuarios.value = true
          console.log(`🔍 Iniciando búsqueda con término: "${termino}"`)
          
          const resultados = await usuariosService.buscarUsuarios(termino)
          console.log('📋 Resultados obtenidos:', resultados)
          
          usuariosFiltrados.value = resultados
          mostrarResultados.value = true
          
          console.log(`✅ Mostrando ${resultados.length} usuarios filtrados`)
        } catch (err) {
          console.error('❌ Error al buscar usuarios:', err)
          error.value = 'Error al buscar usuarios'
          usuariosFiltrados.value = []
          mostrarResultados.value = true
        } finally {
          buscandoUsuarios.value = false
        }
      }, 300)
    }

    const seleccionarUsuario = (usuario) => {
      console.log('👤 Usuario seleccionado:', usuario)
      usuarioSeleccionado.value = usuario.id.toString()
      usuarioActual.value = usuario
      terminoBusqueda.value = usuario.nombre_completo
      mostrarResultados.value = false
      usuariosFiltrados.value = []
      error.value = ''
      
      // Cargar historial del usuario seleccionado
      cargarResumen()
      cargarHistorial()
    }

    const limpiarBusqueda = () => {
      terminoBusqueda.value = ''
      usuariosFiltrados.value = []
      mostrarResultados.value = false
      if (timeoutBusqueda.value) {
        clearTimeout(timeoutBusqueda.value)
      }
    }

    const limpiarSeleccion = () => {
      usuarioSeleccionado.value = ''
      usuarioActual.value = null
      historial.value = []
      resumen.value = null
      terminoBusqueda.value = ''
      usuariosFiltrados.value = []
      mostrarResultados.value = false
      error.value = ''
    }

    // Cerrar resultados al hacer clic fuera
    const cerrarResultados = (event) => {
      const searchContainer = event.target.closest('.user-search-container')
      const dropdown = event.target.closest('.search-results-dropdown')
      if (!searchContainer && !dropdown) {
        mostrarResultados.value = false
      }
    }

    // Métodos de formato
    const formatearOrigen = (origen) => {
      const origenes = {
        historial: 'Historial',
        registros: 'Actividades',
        asistencias: 'Asistencia'
      }
      return origenes[origen] || origen
    }

    const formatearTipo = (tipo) => {
      return historialService.formatearTipo(tipo)
    }

    const formatearFecha = (fecha) => {
      return historialService.formatearFecha(fecha)
    }

    const formatearHora = (hora) => {
      return historialService.formatearHora(hora)
    }

    const formatearFechaHora = (fecha, hora) => {
      if (!fecha || !hora) return 'N/A'
      
      try {
        const fechaObj = new Date(fecha + 'T' + hora)
        return fechaObj.toLocaleString('es-ES', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        })
      } catch (error) {
        return `${formatearFecha(fecha)} ${formatearHora(hora)}`
      }
    }

    // Métodos de modal
    const mostrarDetalles = (registro) => {
      console.log('🔍 DEBUG - Mostrando detalles del registro:', registro);
      console.log('🔍 DEBUG - Datos de usuario en el registro:', {
        usuario_nombre: registro?.usuario_nombre,
        usuario_correo: registro?.usuario_correo,
        usuario_curp: registro?.usuario_curp,
        usuario_cargo: registro?.usuario_cargo,
        origen: registro?.origen,
        id: registro?.id
      });
      
      modalDetalles.value = {
        visible: true,
        registro: registro
      }
    }

    const cerrarModalDetalles = () => {
      modalDetalles.value = {
        visible: false,
        registro: null
      }
    }

    // Métodos del lightbox
    const abrirFotoCompleta = (fotoUrl) => {
      lightboxImageUrl.value = fotoUrl
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

    // Obtener URL de imagen desde los detalles
    const obtenerImagenUrl = (registro) => {
      if (!registro || !registro.detalles) return null
      
      try {
        let detalles
        if (typeof registro.detalles === 'string') {
          detalles = JSON.parse(registro.detalles)
        } else {
          detalles = registro.detalles
        }
        
        const baseUrl = 'https://apipwa.sembrandodatos.com'
        
        if (detalles.foto_url) {
          // Si ya tiene el protocolo, usarla directamente
          if (detalles.foto_url.startsWith('http')) {
            return detalles.foto_url
          }
          // Si no, agregar la base URL
          return `${baseUrl}${detalles.foto_url.startsWith('/') ? '' : '/'}${detalles.foto_url}`
        }
        
        return null
      } catch (error) {
        console.error('Error al obtener URL de imagen:', error)
        return null
      }
    }

    // Obtener información de ubicación desde los detalles
    const obtenerUbicacion = (registro) => {
      if (!registro || !registro.detalles) return null
      
      try {
        let detalles
        if (typeof registro.detalles === 'string') {
          detalles = JSON.parse(registro.detalles)
        } else {
          detalles = registro.detalles
        }
        
        if (detalles.latitud && detalles.longitud) {
          return {
            latitud: detalles.latitud,
            longitud: detalles.longitud
          }
        }
        
        return null
      } catch (error) {
        console.error('Error al obtener ubicación:', error)
        return null
      }
    }

    // Manejar error de carga de imagen
    const onImageError = (event) => {
      console.error('Error al cargar imagen:', event.target.src)
      event.target.style.display = 'none'
    }

    // Manejar carga exitosa de imagen
    const onImageLoad = (event) => {
      console.log('Imagen cargada exitosamente:', event.target.src)
    }

    // Variables para el mapa
    let mapboxInstance = null
    let leafletInstance = null
    const mapboxAccessToken = 'pk.eyJ1IjoidGVzdHVzZXIiLCJhIjoiY2xhYmNkZWZnMGFiYzNxbnV4eXpuaWRleiJ9.invalid'

    // Inicializar mapa de Mapbox o Leaflet como fallback
    const inicializarMapa = (latitud, longitud) => {
      console.log('🗺️ Iniciando inicialización del mapa:', { latitud, longitud })
      
      // Destruir mapas existentes
      if (mapboxInstance) {
        mapboxInstance.remove()
        mapboxInstance = null
      }
      if (leafletInstance) {
        leafletInstance.remove()
        leafletInstance = null
      }

      // Verificar que el contenedor existe
      const container = document.getElementById('mapbox-container')
      if (!container) {
        console.error('❌ Contenedor del mapa no encontrado')
        return
      }

      console.log('✅ Contenedor del mapa encontrado:', container)

      // Limpiar contenedor
      container.innerHTML = ''

      // Usar Leaflet directamente (más confiable)
      if (window.L) {
        try {
          console.log('🍃 Inicializando con Leaflet...')
          
          leafletInstance = window.L.map('mapbox-container', {
            center: [latitud, longitud],
            zoom: 16,
            zoomControl: false,
            attributionControl: false
          })

          // Añadir capa de OpenStreetMap
          window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: ''
          }).addTo(leafletInstance)

          // Crear icono personalizado verde
          const greenIcon = window.L.divIcon({
            html: `<div style="
              background-color: #4CAF50;
              width: 20px;
              height: 20px;
              border-radius: 50% 50% 50% 0;
              transform: rotate(-45deg);
              border: 2px solid white;
              box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            "></div>`,
            className: 'custom-div-icon',
            iconSize: [20, 20],
            iconAnchor: [10, 20]
          })

          // Añadir marcador
          window.L.marker([latitud, longitud], { icon: greenIcon })
            .addTo(leafletInstance)
            .bindPopup(`
              <div style="text-align: center; padding: 4px; font-family: 'Inter', sans-serif;">
                <strong style="color: #4CAF50; font-size: 12px;">📍 Ubicación</strong><br>
                <small style="color: #666; font-size: 10px;">
                  ${latitud.toFixed(6)}, ${longitud.toFixed(6)}
                </small>
              </div>
            `)

          console.log('✅ Mapa Leaflet inicializado correctamente')
          
          // Forzar redimensionamiento del mapa
          setTimeout(() => {
            leafletInstance.invalidateSize()
          }, 100)
          
        } catch (error) {
          console.error('❌ Error al inicializar Leaflet:', error)
          mostrarErrorMapa(container)
        }
      } else {
        console.error('❌ Leaflet no está disponible')
        mostrarErrorMapa(container)
      }
    }

    // Mostrar mensaje de error
    const mostrarErrorMapa = (container) => {
      container.innerHTML = `
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: #e74c3c; text-align: center; padding: 20px;">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
            <circle cx="12" cy="10" r="3"/>
          </svg>
          <p style="margin: 8px 0 0 0; font-size: 10px;">No se puede cargar el mapa</p>
        </div>
      `
    }

    // Destruir mapa
    const destruirMapa = () => {
      if (mapboxInstance) {
        mapboxInstance.remove()
        mapboxInstance = null
      }
      if (leafletInstance) {
        leafletInstance.remove()
        leafletInstance = null
      }
    }

    // Watch para el modal de detalles
    watch(() => modalDetalles.value.visible, (visible) => {
      if (visible && modalDetalles.value.registro) {
        // Usar nextTick para asegurar que el DOM está listo
        nextTick(() => {
          const ubicacion = obtenerUbicacion(modalDetalles.value.registro)
          if (ubicacion && ubicacion.latitud && ubicacion.longitud) {
            // Delay mayor para asegurar que el contenedor está completamente en el DOM
            setTimeout(() => {
              console.log('🗺️ Inicializando mapa con coordenadas:', ubicacion.latitud, ubicacion.longitud)
              inicializarMapa(ubicacion.latitud, ubicacion.longitud)
            }, 300)
          } else {
            console.log('⚠️ No hay coordenadas válidas para el mapa')
          }
        })
      } else {
        destruirMapa()
      }
    })

    // Limpiar mapa al desmontar el componente
    onUnmounted(() => {
      destruirMapa()
    })

    // Exportar a Excel
    const exportarExcel = async () => {
      if (historial.value.length === 0) return

      exportando.value = true
      
      try {
        console.log('📊 Generando archivo Excel...')
        
        const datosExcel = historialService.generarDatosExcel(
          historial.value, 
          usuarioActual.value?.nombre_completo || 'Usuario'
        )

        // Crear libro de trabajo
        const workbook = XLSX.utils.book_new()
        const worksheet = XLSX.utils.json_to_sheet(datosExcel.datos)

        // Ajustar anchos de columnas
        const columnWidths = [
          { wch: 8 },   // ID
          { wch: 25 },  // Usuario
          { wch: 30 },  // Correo
          { wch: 12 },  // Tipo
          { wch: 40 },  // Descripción
          { wch: 12 },  // Fecha
          { wch: 10 },  // Hora
          { wch: 18 }   // Creado en
        ]
        worksheet['!cols'] = columnWidths

        // Agregar hoja al libro
        XLSX.utils.book_append_sheet(workbook, worksheet, datosExcel.nombreHoja)

        // Descargar archivo
        XLSX.writeFile(workbook, datosExcel.nombreArchivo)
        
        console.log('✅ Archivo Excel generado:', datosExcel.nombreArchivo)
        
      } catch (err) {
        console.error('❌ Error al exportar Excel:', err)
        error.value = 'Error al generar el archivo Excel'
      } finally {
        exportando.value = false
      }
    }

    // Métodos de sistema
    const logout = () => {
      localStorage.removeItem('userData')
      localStorage.removeItem('token')
      router.push('/login')
    }

    const updateOnlineStatus = () => {
      isOnline.value = navigator.onLine
    }

    // Lifecycle
    onMounted(async () => {
      window.addEventListener('online', updateOnlineStatus)
      window.addEventListener('offline', updateOnlineStatus)
      document.addEventListener('click', cerrarResultados)
      
      // Event listener para cerrar lightbox con ESC
      document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && showLightbox.value) {
          cerrarLightbox()
        }
      })
      
      // Probar conectividad primero
      try {
        await historialService.probarConectividad()
        console.log('✅ Conectividad con backend confirmada')
      } catch (err) {
        console.error('❌ Error de conectividad:', err)
        error.value = 'No se puede conectar con el servidor. Verifica que esté funcionando.'
      }
      
      await cargarUsuarios()
      
      // Configurar semana inicial
      const fechaActual = new Date()
      const año = fechaActual.getFullYear()
      const semana = getWeekNumber(fechaActual)
      filtros.value.semanaEspecifica = `${año}-W${semana.toString().padStart(2, '0')}`
    })

    onUnmounted(() => {
      window.removeEventListener('online', updateOnlineStatus)
      window.removeEventListener('offline', updateOnlineStatus)
      document.removeEventListener('click', cerrarResultados)
      if (timeoutBusqueda.value) {
        clearTimeout(timeoutBusqueda.value)
      }
    })

    return {
      // Estados
      isOnline,
      loading,
      exportando,
      error,
      usuarios,
      usuarioSeleccionado,
      historial,
      resumen,
      usuarioActual,
      filtros,
      modalDetalles,
      añosDisponibles,
      adminUser,
      
      // Lightbox
      showLightbox,
      lightboxImageUrl,
      
      // Estados de búsqueda
      terminoBusqueda,
      usuariosFiltrados,
      buscandoUsuarios,
      mostrarResultados,
      
      // Métodos principales
      cargarHistorial,
      actualizarHistorial,
      onUsuarioChange,
      
      // Métodos de búsqueda
      buscarUsuarios,
      seleccionarUsuario,
      limpiarBusqueda,
      limpiarSeleccion,
      
      // Métodos de filtros
      setPeriodo,
      aplicarFiltros,
      
      // Métodos de formato
      formatearOrigen,
      formatearTipo,
      formatearFecha,
      formatearHora,
      formatearFechaHora,
      
      // Métodos de modal
      mostrarDetalles,
      cerrarModalDetalles,
      obtenerImagenUrl,
      obtenerUbicacion,
      onImageError,
      onImageLoad,
      
      // Métodos de lightbox
      abrirFotoCompleta,
      cerrarLightbox,
      requestFullscreen,
      
      // Exportar
      exportarExcel,
      
      // Sistema
      logout
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  overflow-x: hidden;
}

.historiales-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  width: 100%;
  overflow-x: hidden;
  position: relative;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: min(220px, 18vw);
  width: calc(100vw - min(220px, 18vw));
  background: linear-gradient(135deg, #f8f9fa 0%, #f0fff0 100%);
  min-height: 100vh;
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-sizing: border-box;
  overflow-x: hidden;
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
  flex: 1;
  padding: clamp(8px, 1.5vw, 16px) clamp(16px, 4vw, 32px);
  box-sizing: border-box;
  width: 100%;
  max-width: 100%;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: clamp(8px, 1.5vw, 12px);
  overflow: visible;
}

/* Sección de selección de usuario */
.user-selection-section {
  width: 100%;
  overflow: visible;
  position: relative;
}

.selection-card {
  background: linear-gradient(135deg, #f0fff4 0%, #e8f5e8 100%);
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-radius: clamp(6px, 1.5vw, 8px);
  padding: clamp(0.4rem, 1vw, 0.6rem);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.08);
  overflow: visible;
  position: relative;
}

.selection-header {
  margin-bottom: clamp(8px, 1.5vw, 10px);
}

.selection-header h3 {
  display: flex;
  align-items: center;
  gap: clamp(4px, 1vw, 6px);
  font-size: clamp(12px, 2.5vw, 14px);
  font-weight: 600;
  color: #2c5530;
  margin: 0;
}

.selection-header svg {
  color: #27ae60;
}

.user-selector {
  width: 100%;
}

/* Estilos para el buscador de usuarios */
.user-search-container {
  position: relative;
  width: 100%;
  overflow: visible;
}

.search-input-wrapper {
  position: relative;
  width: 100%;
}

.search-icon {
  position: absolute;
  left: clamp(8px, 1.5vw, 10px);
  top: 50%;
  transform: translateY(-50%);
  color: #9ca3af;
  width: clamp(12px, 2vw, 14px);
  height: clamp(12px, 2vw, 14px);
  pointer-events: none;
  z-index: 2;
}

.search-input {
  width: 100%;
  padding: clamp(0.25rem, 0.6vw, 0.35rem) clamp(0.4rem, 1vw, 0.5rem) clamp(0.25rem, 0.6vw, 0.35rem) clamp(2rem, 4vw, 2.5rem);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: clamp(4px, 1vw, 6px);
  background: rgba(255, 255, 255, 0.9);
  font-size: clamp(11px, 2vw, 12px);
  color: #495057;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.search-input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
}

/* Resultados de búsqueda - Dropdown flotante independiente */
.search-results-dropdown {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: white;
  border: 2px solid rgba(76, 175, 80, 0.4);
  border-radius: clamp(6px, 1.2vw, 8px);
  box-shadow: 0 8px 24px rgba(76, 175, 80, 0.3);
  max-height: 220px;
  overflow-y: auto;
  z-index: 10000;
  animation: slideDown 0.2s ease-out;
  backdrop-filter: blur(8px);
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.loading-search {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(4px, 0.8vw, 6px);
  padding: clamp(8px, 1.5vw, 10px);
  color: #6c757d;
  font-size: clamp(9px, 1.6vw, 10px);
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.need-more-chars {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: clamp(10px, 2vw, 14px);
  color: #6c757d;
  text-align: center;
}

.need-more-chars svg {
  margin-bottom: clamp(4px, 0.8vw, 6px);
  opacity: 0.6;
}

.need-more-chars p {
  margin: 0;
  font-size: clamp(8px, 1.5vw, 9px);
  font-style: italic;
}

.no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: clamp(14px, 2.8vw, 18px);
  color: #6c757d;
  text-align: center;
}

.no-results svg {
  margin-bottom: clamp(6px, 1.2vw, 8px);
  opacity: 0.5;
}

.no-results p {
  margin: 0;
  font-size: clamp(9px, 1.6vw, 10px);
}

.results-list {
  padding: 0;
}

.result-item {
  display: flex;
  align-items: center;
  gap: clamp(6px, 1.2vw, 8px);
  padding: clamp(6px, 1.2vw, 8px);
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.result-item:last-child {
  border-bottom: none;
}

.result-item:hover {
  background: rgba(76, 175, 80, 0.08);
}

.result-item.active {
  background: rgba(76, 175, 80, 0.12);
  border-left: 4px solid #4CAF50;
}

.user-avatar {
  width: clamp(22px, 4vw, 26px);
  height: clamp(22px, 4vw, 26px);
  background: linear-gradient(135deg, #4CAF50, #45a049);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: white;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-weight: 600;
  font-size: clamp(9px, 1.6vw, 10px);
  color: #2c5530;
  margin-bottom: clamp(1px, 0.3vw, 2px);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-details {
  display: flex;
  align-items: center;
  gap: clamp(3px, 0.6vw, 4px);
  margin-bottom: clamp(1px, 0.3vw, 2px);
}

.user-email {
  font-size: clamp(8px, 1.4vw, 9px);
  color: #6c757d;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 150px;
}

.user-curp {
  font-size: clamp(8px, 1.4vw, 9px);
  color: #6c757d;
  white-space: nowrap;
}

.user-cargo {
  font-size: clamp(8px, 1.4vw, 9px);
  color: #4CAF50;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Usuario seleccionado */
.selected-user {
  margin-top: clamp(8px, 1.5vw, 10px);
  padding-top: clamp(8px, 1.5vw, 10px);
  border-top: 1px solid rgba(76, 175, 80, 0.2);
}

.selected-user-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: clamp(6px, 1.2vw, 8px);
}

.selected-user-header h4 {
  margin: 0;
  font-size: clamp(9px, 1.6vw, 10px);
  font-weight: 600;
  color: #2c5530;
}

.clear-selection-btn {
  display: flex;
  align-items: center;
  gap: clamp(3px, 0.6vw, 4px);
  padding: clamp(3px, 0.6vw, 4px) clamp(6px, 1.2vw, 8px);
  background: transparent;
  border: 1px solid rgba(231, 76, 60, 0.3);
  border-radius: clamp(2px, 0.4vw, 3px);
  color: #e74c3c;
  font-size: clamp(8px, 1.4vw, 9px);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.clear-selection-btn:hover {
  background: rgba(231, 76, 60, 0.05);
  border-color: rgba(231, 76, 60, 0.5);
}

.selected-user-card {
  display: flex;
  align-items: center;
  gap: clamp(6px, 1.2vw, 8px);
  padding: clamp(6px, 1.2vw, 8px);
  background: rgba(76, 175, 80, 0.05);
  border: 1px solid rgba(76, 175, 80, 0.2);
  border-radius: clamp(3px, 0.8vw, 4px);
}

.selected-user-avatar {
  width: clamp(24px, 4.5vw, 28px);
  height: clamp(24px, 4.5vw, 28px);
  background: linear-gradient(135deg, #4CAF50, #45a049);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: white;
}

.selected-user-info {
  flex: 1;
  min-width: 0;
}

.selected-user-name {
  font-weight: 700;
  font-size: clamp(10px, 1.8vw, 11px);
  color: #2c5530;
  margin-bottom: clamp(2px, 0.4vw, 3px);
}

.selected-user-email {
  font-size: clamp(8px, 1.4vw, 9px);
  color: #6c757d;
  margin-bottom: clamp(1px, 0.3vw, 2px);
}

.selected-user-curp {
  font-size: clamp(8px, 1.4vw, 9px);
  color: #6c757d;
  margin-bottom: clamp(1px, 0.3vw, 2px);
}

.selected-user-cargo {
  font-size: clamp(8px, 1.4vw, 9px);
  color: #4CAF50;
  font-weight: 600;
}

/* Sección de filtros */
.filters-section {
  width: 100%;
}

.filters-card {
  background: linear-gradient(135deg, #f0fff4 0%, #e8f5e8 100%);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-radius: clamp(4px, 1vw, 6px);
  padding: clamp(0.3rem, 0.8vw, 0.4rem);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.08);
  transition: all 0.3s ease;
}

.filters-card:hover {
  border-color: rgba(76, 175, 80, 0.5);
  box-shadow: 0 3px 12px rgba(76, 175, 80, 0.12);
  transform: translateY(-1px);
}

.filters-header {
  margin-bottom: clamp(0.2rem, 0.5vw, 0.25rem);
}

.filters-header h3 {
  display: flex;
  align-items: center;
  gap: clamp(3px, 0.8vw, 4px);
  font-size: clamp(10px, 2vw, 11px);
  font-weight: 600;
  color: #2c5530;
  margin: 0;
}

.filters-header svg {
  color: #27ae60;
}

.filters-grid {
  display: grid;
  gap: clamp(0.2rem, 0.5vw, 0.25rem);
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: clamp(2px, 0.4vw, 3px);
}

.filter-group label {
  font-size: clamp(9px, 1.6vw, 10px);
  font-weight: 500;
  color: #495057;
}

.period-buttons {
  display: flex;
  gap: clamp(2px, 0.4vw, 3px);
  flex-wrap: wrap;
}

.period-btn {
  padding: clamp(0.15rem, 0.4vw, 0.2rem) clamp(0.3rem, 0.8vw, 0.4rem);
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.9);
  border-radius: clamp(2px, 0.6vw, 3px);
  font-size: clamp(8px, 1.4vw, 9px);
  font-weight: 500;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.period-btn:hover {
  border-color: #4CAF50;
  color: #4CAF50;
  background: rgba(76, 175, 80, 0.05);
}

.period-btn.active {
  background: #4CAF50;
  border-color: #4CAF50;
  color: white;
}

.date-input, .year-select, .type-select {
  padding: clamp(0.2rem, 0.4vw, 0.25rem) clamp(0.3rem, 0.8vw, 0.4rem);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: clamp(3px, 0.8vw, 4px);
  background: rgba(255, 255, 255, 0.9);
  font-size: clamp(8px, 1.4vw, 9px);
  color: #495057;
  transition: all 0.3s ease;
}

.date-input:focus, .year-select:focus, .type-select:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
}

/* Sección de estadísticas */
.stats-section {
  width: 100%;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: clamp(8px, 1.5vw, 10px);
}

.stat-card {
  background: white;
  border-radius: clamp(8px, 1.5vw, 10px);
  padding: clamp(10px, 2vw, 12px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
  display: flex;
  align-items: center;
  gap: clamp(8px, 1.5vw, 10px);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  width: clamp(28px, 5vw, 32px);
  height: clamp(28px, 5vw, 32px);
  border-radius: clamp(6px, 1.2vw, 8px);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon.total {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
}

.stat-icon.entrada {
  background: linear-gradient(135deg, #27ae60, #229954);
  color: white;
}

.stat-icon.salida {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
}

.stat-icon.actividad {
  background: linear-gradient(135deg, #f39c12, #d68910);
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: clamp(14px, 3vw, 18px);
  font-weight: 700;
  color: #2c5530;
  margin: 0;
  line-height: 1;
}

.stat-label {
  font-size: clamp(10px, 1.8vw, 11px);
  color: #6c757d;
  margin: clamp(3px, 0.6vw, 4px) 0 0 0;
  font-weight: 500;
}

/* Sección de historial */
.historial-section {
  background: white;
  border-radius: clamp(8px, 1.5vw, 12px);
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e9ecef;
  min-height: 300px;
  display: flex;
  flex-direction: column;
}

.historial-header {
  padding: clamp(10px, 2vw, 14px);
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: clamp(8px, 1.5vw, 10px);
}

.historial-header h3 {
  display: flex;
  align-items: center;
  gap: clamp(6px, 1.2vw, 8px);
  font-size: clamp(12px, 2.5vw, 14px);
  font-weight: 600;
  color: #2c5530;
  margin: 0;
}

.historial-header svg {
  color: #27ae60;
}

.historial-actions {
  display: flex;
  align-items: center;
  gap: clamp(8px, 1.5vw, 10px);
  flex-wrap: wrap;
}

.record-count {
  font-size: clamp(10px, 1.8vw, 11px);
  color: #6c757d;
  white-space: nowrap;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: clamp(4px, 0.8vw, 6px);
  padding: clamp(6px, 1.2vw, 8px) clamp(10px, 2vw, 12px);
  background: #27ae60;
  border: none;
  border-radius: clamp(4px, 0.8vw, 6px);
  color: white;
  font-size: clamp(10px, 1.8vw, 11px);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.export-btn:hover:not(:disabled) {
  background: #229954;
  transform: translateY(-1px);
}

.export-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Estados de carga y error */
.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: clamp(40px, 8vw, 60px);
  text-align: center;
  flex: 1;
}

.spinner-large {
  width: clamp(32px, 6vw, 48px);
  height: clamp(32px, 6vw, 48px);
  border: 3px solid #f3f3f3;
  border-top: 3px solid #2ecc71;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: clamp(16px, 3vw, 20px);
}

.loading-container p, .error-container p {
  color: #6c757d;
  font-size: clamp(14px, 2.5vw, 16px);
  margin: 0;
}

.error-icon {
  margin-bottom: clamp(16px, 3vw, 20px);
  color: #e74c3c;
}

.error-container h3 {
  color: #495057;
  font-size: clamp(16px, 3vw, 20px);
  font-weight: 600;
  margin: 0 0 clamp(8px, 1.5vw, 12px) 0;
}

.retry-btn {
  display: flex;
  align-items: center;
  gap: clamp(6px, 1.2vw, 8px);
  padding: clamp(8px, 1.5vw, 10px) clamp(16px, 3vw, 20px);
  background: #2ecc71;
  border: none;
  border-radius: clamp(6px, 1.2vw, 8px);
  color: white;
  font-size: clamp(14px, 2.5vw, 16px);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: clamp(16px, 3vw, 20px);
}

.retry-btn:hover {
  background: #27ae60;
  transform: translateY(-1px);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: clamp(40px, 8vw, 60px);
  text-align: center;
  flex: 1;
}

.empty-icon {
  margin-bottom: clamp(16px, 3vw, 20px);
  opacity: 0.6;
}

.empty-state h3 {
  color: #495057;
  font-size: clamp(16px, 3vw, 20px);
  font-weight: 600;
  margin: 0 0 clamp(8px, 1.5vw, 12px) 0;
}

.empty-state p {
  color: #6c757d;
  font-size: clamp(14px, 2.5vw, 16px);
  margin: 0;
  line-height: 1.5;
}

/* Tabla de historial */
.historial-table-container {
  flex: 1;
  overflow: auto;
}

.table-wrapper {
  min-width: 100%;
  overflow-x: auto;
}

.historial-table {
  width: 100%;
  border-collapse: collapse;
  font-size: clamp(10px, 1.8vw, 11px);
}

.historial-table th {
  background: #f8f9fa;
  padding: clamp(8px, 1.5vw, 10px);
  text-align: center;
  font-weight: 600;
  color: #495057;
  border-bottom: 2px solid #e9ecef;
  white-space: nowrap;
}

.historial-table td {
  padding: clamp(8px, 1.5vw, 10px);
  border-bottom: 1px solid #e9ecef;
  vertical-align: middle;
  text-align: center;
}

.registro-row:hover {
  background: #f8f9fa;
}

.tipo-badge {
  display: inline-flex;
  align-items: center;
  padding: clamp(3px, 0.6vw, 4px) clamp(6px, 1.2vw, 8px);
  border-radius: clamp(10px, 2vw, 12px);
  font-size: clamp(9px, 1.6vw, 10px);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.tipo-badge.entrada {
  background: rgba(39, 174, 96, 0.1);
  color: #27ae60;
  border: 1px solid rgba(39, 174, 96, 0.2);
}

.tipo-badge.salida {
  background: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
  border: 1px solid rgba(231, 76, 60, 0.2);
}

.tipo-badge.actividad {
  background: rgba(52, 152, 219, 0.1);
  color: #3498db;
  border: 1px solid rgba(52, 152, 219, 0.2);
}

.origen-badge {
  display: inline-flex;
  align-items: center;
  padding: clamp(2px, 0.4vw, 3px) clamp(5px, 1vw, 6px);
  border-radius: clamp(8px, 1.5vw, 10px);
  font-size: clamp(8px, 1.4vw, 9px);
  font-weight: 500;
  text-transform: capitalize;
  letter-spacing: 0.3px;
  white-space: nowrap;
}

.origen-badge.historial {
  background: rgba(156, 39, 176, 0.1);
  color: #9c27b0;
  border: 1px solid rgba(156, 39, 176, 0.2);
}

.origen-badge.registros {
  background: rgba(255, 193, 7, 0.1);
  color: #ff9800;
  border: 1px solid rgba(255, 193, 7, 0.2);
}

.origen-badge.asistencias {
  background: rgba(103, 58, 183, 0.1);
  color: #673ab7;
  border: 1px solid rgba(103, 58, 183, 0.2);
}

.origen-cell, .tipo-cell {
  text-align: center;
  white-space: nowrap;
}

.descripcion-cell {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: center;
}

.fecha-cell, .hora-cell {
  white-space: nowrap;
  color: #6c757d;
  text-align: center;
}

.detalles-cell {
  text-align: center;
}

.action-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 8px 0;
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

.no-details {
  color: #adb5bd;
  font-style: italic;
  font-size: clamp(9px, 1.6vw, 10px);
  text-align: center;
}

/* Welcome section moderna */
.welcome-section {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: clamp(60px, 8vw, 100px) clamp(20px, 4vw, 30px) clamp(40px, 6vw, 60px);
  min-height: calc(100vh - 200px);
  padding-top: clamp(80px, 12vw, 120px);
}

.modern-welcome-card {
  position: relative;
  max-width: min(420px, 90vw);
  width: 100%;
  border-radius: clamp(12px, 2.5vw, 20px);
  overflow: hidden;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
}

.glass-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.15) 0%,
    rgba(255, 255, 255, 0.05) 100%);
  backdrop-filter: blur(20px);
}

.welcome-content {
  position: relative;
  z-index: 2;
  padding: clamp(20px, 4vw, 32px);
  text-align: center;
}

.welcome-icon {
  width: clamp(28px, 5vw, 40px);
  height: clamp(28px, 5vw, 40px);
  margin: 0 auto clamp(12px, 2.5vw, 20px) auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.welcome-icon svg {
  width: 100%;
  height: 100%;
  color: #6b7280;
  stroke-width: 1.5;
}

.welcome-content h2 {
  color: #374151;
  font-size: clamp(14px, 3vw, 20px);
  font-weight: 500;
  margin: 0 0 clamp(6px, 1.2vw, 12px) 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  letter-spacing: -0.025em;
  line-height: 1.3;
}

.welcome-content p {
  color: #6b7280;
  font-size: clamp(12px, 2.5vw, 15px);
  line-height: 1.5;
  margin: 0 0 clamp(12px, 2.5vw, 20px) 0;
  font-weight: 400;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  max-width: 300px;
  margin-left: auto;
  margin-right: auto;
}

.modern-divider {
  width: clamp(30px, 8vw, 60px);
  height: 1px;
  background: rgba(156, 163, 175, 0.3);
  margin: 0 auto clamp(12px, 2.5vw, 20px) auto;
}

.search-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(4px, 1vw, 8px);
  padding: clamp(6px, 1.5vw, 12px) clamp(8px, 2vw, 16px);
  background: rgba(243, 244, 246, 0.6);
  border: 1px solid rgba(229, 231, 235, 0.8);
  border-radius: clamp(6px, 1.5vw, 12px);
  color: #6b7280;
  font-size: clamp(10px, 2vw, 13px);
  font-weight: 400;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.hint-icon {
  font-size: clamp(11px, 2.2vw, 14px);
  opacity: 0.8;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .welcome-section {
    padding-top: clamp(60px, 10vw, 80px);
    padding-bottom: clamp(30px, 5vw, 40px);
  }
  
  .modern-welcome-card {
    max-width: 95vw;
  }
  
  .welcome-content {
    padding: clamp(16px, 3vw, 24px);
  }
  
  .welcome-content p {
    max-width: 280px;
  }
}

@media (max-width: 480px) {
  .welcome-section {
    padding-top: clamp(50px, 8vw, 70px);
  }
  
  .welcome-content p {
    max-width: 240px;
  }
  
  .search-hint {
    flex-direction: column;
    gap: clamp(3px, 0.8vw, 5px);
    text-align: center;
  }
}

@media (max-width: 360px) {
  .welcome-section {
    padding: clamp(40px, 6vw, 50px) clamp(12px, 3vw, 16px) clamp(20px, 4vw, 30px);
  }
  
  .welcome-content {
    padding: clamp(12px, 2.5vw, 18px);
  }
}

/* Modal de detalles moderno */
.modal-overlay-modern {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: clamp(12px, 2vw, 16px);
  animation: fadeInOverlay 0.3s ease-out;
}

@keyframes fadeInOverlay {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content-modern {
  background: linear-gradient(135deg, #f8fff9 0%, #f0fff4 100%);
  border: 1px solid rgba(76, 175, 80, 0.2);
  border-radius: clamp(8px, 1.5vw, 12px);
  max-width: clamp(320px, 85vw, 480px);
  width: 100%;
  max-height: 85vh;
  overflow: hidden;
  box-shadow: 
    0 10px 40px rgba(76, 175, 80, 0.15),
    0 4px 20px rgba(0, 0, 0, 0.1);
  animation: slideInModal 0.3s ease-out;
  position: relative;
}

/* Modal horizontal para dos columnas */
.modal-content-modern-horizontal {
  background: linear-gradient(135deg, #f8fff9 0%, #f0fff4 100%);
  border: 1px solid rgba(76, 175, 80, 0.2);
  border-radius: clamp(8px, 1.5vw, 12px);
  max-width: clamp(420px, 90vw, 800px);
  width: 100%;
  max-height: 85vh;
  overflow: hidden;
  box-shadow: 
    0 10px 40px rgba(76, 175, 80, 0.15),
    0 4px 20px rgba(0, 0, 0, 0.1);
  animation: slideInModal 0.3s ease-out;
  position: relative;
}

@keyframes slideInModal {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header-modern {
  background: linear-gradient(135deg, #4CAF50 0%, #43A047 100%);
  color: white;
  padding: clamp(8px, 1.5vw, 12px) clamp(12px, 2vw, 16px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

.modal-header-modern * {
  user-select: none !important;
}

.modal-header-modern .modal-title-section * {
  pointer-events: none !important;
}

.modal-header-modern::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='20' cy='20' r='1.5'/%3E%3C/g%3E%3C/svg%3E") repeat;
  z-index: 1;
}

.modal-title-section {
  display: flex;
  align-items: center;
  gap: clamp(6px, 1.2vw, 8px);
  position: relative;
  z-index: 2;
}

.modal-icon-header {
  width: clamp(20px, 3.5vw, 24px);
  height: clamp(20px, 3.5vw, 24px);
  background: rgba(255, 255, 255, 0.15);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.modal-title-text {
  font-size: clamp(12px, 2.2vw, 14px);
  font-weight: 600;
  margin: 0;
  line-height: 1;
  user-select: none;
  pointer-events: none;
  cursor: default;
}

.modal-title-text::before,
.modal-title-text::after {
  display: none !important;
  content: none !important;
}

.modal-title-section {
  display: flex;
  align-items: center;
  gap: clamp(6px, 1.2vw, 8px);
  position: relative;
  z-index: 2;
  user-select: none;
  pointer-events: none;
}

.btn-close-modern {
  background: rgba(255, 255, 255, 0.15);
  border: none;
  border-radius: 50%;
  width: clamp(24px, 4vw, 28px);
  height: clamp(24px, 4vw, 28px);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  flex-shrink: 0;
  position: relative;
  z-index: 2;
}

.btn-close-modern:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: scale(1.05);
}

.modal-body-modern {
  padding: clamp(12px, 2vw, 16px);
  max-height: calc(85vh - 60px);
  overflow-y: auto;
}

/* Body del modal horizontal */
.modal-body-modern-horizontal {
  padding: clamp(12px, 2vw, 16px);
  max-height: calc(85vh - 60px);
  overflow-y: auto;
}

/* Contenedor de columnas */
.modal-columns-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: clamp(16px, 3vw, 24px);
  height: 100%;
}

/* Columna izquierda */
.modal-column-left {
  display: flex;
  flex-direction: column;
  gap: clamp(10px, 1.8vw, 12px);
}

/* Columna derecha */
.modal-column-right {
  display: flex;
  flex-direction: column;
  gap: clamp(10px, 1.8vw, 12px);
}

.details-grid-modern {
  display: flex;
  flex-direction: column;
  gap: clamp(10px, 1.8vw, 12px);
}

/* Sección de imagen */
.detail-image-section {
  width: 100%;
  margin-bottom: clamp(4px, 0.8vw, 6px);
}

.detail-image-container {
  position: relative;
  width: 100%;
  height: clamp(120px, 25vw, 160px);
  border-radius: clamp(6px, 1.2vw, 8px);
  overflow: hidden;
  background: linear-gradient(135deg, #e8f5e8 0%, #f0fff4 100%);
  border: 1px solid rgba(76, 175, 80, 0.2);
}

.detail-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.detail-image:hover {
  transform: scale(1.02);
}

.image-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.6));
  padding: clamp(6px, 1.2vw, 8px) clamp(8px, 1.5vw, 10px);
}

.image-info {
  display: flex;
  align-items: center;
  gap: clamp(4px, 0.8vw, 6px);
  color: white;
  font-size: clamp(10px, 1.8vw, 11px);
  font-weight: 500;
}

/* Información principal */
.detail-main-info {
  display: flex;
  flex-direction: column;
  gap: clamp(8px, 1.5vw, 10px);
}

.detail-card-compact {
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(76, 175, 80, 0.15);
  border-radius: clamp(4px, 0.8vw, 6px);
  overflow: hidden;
  transition: all 0.3s ease;
}

.detail-card-compact:hover {
  border-color: rgba(76, 175, 80, 0.25);
  background: rgba(255, 255, 255, 0.8);
  transform: translateY(-1px);
}

/* Tarjetas más compactas para ubicación y origen */
.location-card,
.origen-card {
  min-height: auto;
}

.location-card .detail-header-compact,
.origen-card .detail-header-compact {
  padding: clamp(4px, 0.8vw, 6px) clamp(6px, 1.2vw, 8px);
}

.location-card .detail-content-compact,
.origen-card .detail-content-compact {
  padding: clamp(6px, 1.2vw, 8px);
}

.detail-header-compact {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.08) 0%, rgba(76, 175, 80, 0.05) 100%);
  padding: clamp(6px, 1.2vw, 8px) clamp(8px, 1.5vw, 10px);
  display: flex;
  align-items: center;
  gap: clamp(4px, 0.8vw, 6px);
  border-bottom: 1px solid rgba(76, 175, 80, 0.1);
}

.detail-icon-small {
  width: clamp(16px, 3vw, 18px);
  height: clamp(16px, 3vw, 18px);
  background: linear-gradient(135deg, #4CAF50, #43A047);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.detail-label-compact {
  font-size: clamp(9px, 1.6vw, 10px);
  font-weight: 600;
  color: #2c5530;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-content-compact {
  padding: clamp(8px, 1.5vw, 10px);
}

.info-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: clamp(3px, 0.6vw, 4px) 0;
  border-bottom: 1px solid rgba(76, 175, 80, 0.08);
}

.info-row:last-child {
  border-bottom: none;
}

.info-label {
  font-size: clamp(9px, 1.6vw, 10px);
  font-weight: 500;
  color: #6b7280;
  min-width: clamp(40px, 15vw, 60px);
}

.info-value {
  font-size: clamp(9px, 1.6vw, 10px);
  color: #374151;
  text-align: right;
  flex: 1;
}

/* Badges del modal */
.tipo-badge-modal {
  display: inline-flex;
  align-items: center;
  padding: clamp(2px, 0.4vw, 3px) clamp(6px, 1.2vw, 8px);
  border-radius: clamp(8px, 1.5vw, 10px);
  font-size: clamp(8px, 1.4vw, 9px);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  white-space: nowrap;
}

.tipo-badge-modal.entrada {
  background: rgba(39, 174, 96, 0.15);
  color: #27ae60;
  border: 1px solid rgba(39, 174, 96, 0.3);
}

.tipo-badge-modal.salida {
  background: rgba(231, 76, 60, 0.15);
  color: #e74c3c;
  border: 1px solid rgba(231, 76, 60, 0.3);
}

.tipo-badge-modal.actividad {
  background: rgba(52, 152, 219, 0.15);
  color: #3498db;
  border: 1px solid rgba(52, 152, 219, 0.3);
}

.origen-badge-modal {
  display: inline-flex;
  align-items: center;
  padding: clamp(2px, 0.4vw, 3px) clamp(6px, 1.2vw, 8px);
  border-radius: clamp(6px, 1.2vw, 8px);
  font-size: clamp(8px, 1.4vw, 9px);
  font-weight: 500;
  text-transform: capitalize;
  letter-spacing: 0.3px;
  white-space: nowrap;
}

.origen-badge-modal.historial {
  background: rgba(156, 39, 176, 0.15);
  color: #9c27b0;
  border: 1px solid rgba(156, 39, 176, 0.3);
}

.origen-badge-modal.registros {
  background: rgba(255, 193, 7, 0.15);
  color: #ff9800;
  border: 1px solid rgba(255, 193, 7, 0.3);
}

.origen-badge-modal.asistencias {
  background: rgba(103, 58, 183, 0.15);
  color: #673ab7;
  border: 1px solid rgba(103, 58, 183, 0.3);
}

/* Información de ubicación */
.location-info {
  display: flex;
  gap: clamp(8px, 1.5vw, 12px);
}

.coordinate-row {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  padding: clamp(4px, 0.8vw, 6px);
  background: rgba(76, 175, 80, 0.05);
  border-radius: clamp(3px, 0.6vw, 4px);
  border: 1px solid rgba(76, 175, 80, 0.1);
}

.coordinate-label {
  font-size: clamp(8px, 1.4vw, 9px);
  font-weight: 600;
  color: #4CAF50;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  margin-bottom: clamp(1px, 0.2vw, 2px);
}

.coordinate-value {
  font-size: clamp(8px, 1.4vw, 9px);
  color: #374151;
  font-family: 'Courier New', monospace;
}

/* Estilos para el mapa */
.map-card {
  flex: 1;
  min-height: clamp(320px, 35vh, 380px);
}

.map-content {
  padding: 16px !important;
  border-radius: clamp(4px, 0.8vw, 6px);
  overflow: visible;
  background: #f8f9fa;
  min-height: clamp(320px, 35vh, 380px);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mapbox-container {
  width: 280px;
  height: 280px;
  border-radius: 50% !important;
  overflow: hidden;
  background: linear-gradient(135deg, #e8f5e8 0%, #f0fff4 100%);
  border: 4px solid rgba(76, 175, 80, 0.4);
  box-shadow: 
    0 8px 24px rgba(76, 175, 80, 0.25),
    inset 0 2px 8px rgba(76, 175, 80, 0.1);
  position: relative;
  margin: 16px auto;
  flex-shrink: 0;
}

.mapbox-container canvas,
.mapbox-container .mapboxgl-canvas,
.mapbox-container .leaflet-container {
  border-radius: 50% !important;
}

.mapbox-container .mapboxgl-control-container,
.mapbox-container .leaflet-control-container {
  display: none !important;
}

/* Estilos para Leaflet */
.mapbox-container .leaflet-container {
  background: transparent !important;
}

.mapbox-container .leaflet-tile-pane {
  border-radius: 50% !important;
}

.mapbox-container .leaflet-map-pane {
  border-radius: 50% !important;
  overflow: hidden !important;
}

.no-location-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #6b7280;
  text-align: center;
  padding: clamp(20px, 4vw, 30px);
}

.no-location-message svg {
  margin-bottom: clamp(8px, 1.5vw, 12px);
  opacity: 0.6;
}

.no-location-message p {
  margin: 0;
  font-size: clamp(10px, 1.8vw, 12px);
  font-style: italic;
  line-height: 1.4;
}

/* Responsive design para el modal horizontal */
@media (max-width: 768px) {
  .modal-content-modern-horizontal {
    max-width: 95vw;
    max-height: 90vh;
  }
  
  .modal-columns-container {
    grid-template-columns: 1fr;
    gap: clamp(12px, 2.5vw, 16px);
  }
  
  .mapbox-container {
    width: 220px;
    height: 220px;
    border-radius: 50% !important;
    margin: 12px auto;
  }
}

@media (max-width: 480px) {
  .modal-content-modern-horizontal {
    max-width: 98vw;
  }
  
  .modal-body-modern-horizontal {
    padding: clamp(8px, 1.5vw, 12px);
  }
  
  .modal-columns-container {
    gap: clamp(8px, 1.5vw, 12px);
  }
  
  .mapbox-container {
    width: 200px;
    height: 200px;
    border-radius: 50% !important;
    margin: 10px auto;
  }
  
  .map-card {
    min-height: clamp(180px, 25vh, 220px);
  }
}

/* Responsive design para el modal */
@media (max-width: 480px) {
  .modal-content-modern {
    max-width: 95vw;
    max-height: 90vh;
  }
  
  .detail-image-container {
    height: clamp(100px, 20vw, 120px);
  }
  
  .details-grid-modern {
    gap: clamp(8px, 1.5vw, 10px);
  }
  
  .location-info {
    flex-direction: column;
    gap: clamp(6px, 1.2vw, 8px);
  }
  
  .info-row {
    flex-direction: column;
    align-items: flex-start;
    gap: clamp(2px, 0.4vw, 3px);
  }
  
  .info-value {
    text-align: left;
  }
}

@media (max-width: 360px) {
  .modal-overlay-modern {
    padding: clamp(8px, 1.5vw, 12px);
  }
  
  .modal-content-modern {
    max-width: 98vw;
  }
}

/* Responsive Design */
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
  
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: clamp(12px, 2.5vw, 16px);
  }
  
  .header-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .filters-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .historial-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .historial-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .detail-item {
    grid-template-columns: 1fr;
    gap: clamp(4px, 0.8vw, 6px);
  }
}

@media (max-width: 480px) {
  .page-content {
    padding: clamp(8px, 1.5vw, 12px);
    gap: clamp(8px, 1.5vw, 12px);
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .period-buttons {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .historial-table {
    font-size: clamp(10px, 2vw, 12px);
  }
  
  .historial-table th,
  .historial-table td {
    padding: clamp(8px, 1.5vw, 10px);
  }
  
  .modal-content {
    margin: clamp(8px, 1.5vw, 12px);
    max-height: 90vh;
  }
}

@media (max-width: 360px) {
  .header-main {
    flex-direction: column;
    align-items: flex-start;
    gap: clamp(8px, 1.5vw, 10px);
  }
  
  .header-actions {
    flex-direction: column;
    width: 100%;
    gap: clamp(8px, 1.5vw, 10px);
  }
  
  .connection-status {
    width: 100%;
    justify-content: center;
  }
  
  .refresh-btn {
    width: 100%;
    justify-content: center;
  }
  
  .period-buttons {
    flex-direction: column;
  }
  
  .period-btn {
    text-align: center;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 240px;
    width: calc(100vw - 240px);
  }
  
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: clamp(12px, 2.5vw, 16px);
  }
  
  .header-actions {
    flex-direction: column;
    align-items: stretch;
    gap: clamp(8px, 1.5vw, 12px);
    width: 100%;
  }
  
  .period-buttons {
    flex-wrap: wrap;
  }
  
  .period-btn {
    min-width: auto;
    flex: 1;
    white-space: nowrap;
  }
  
  .search-bar input {
    min-width: auto;
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
  
  .period-btn {
    text-align: center;
  }
}

/* Lightbox Styles */
.lightbox-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.95);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10000;
  animation: fadeIn 0.3s ease-in-out;
}

.lightbox-container {
  position: relative;
  width: 90vw;
  height: 90vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.lightbox-image-wrapper {
  position: relative;
  display: inline-block;
}

.lightbox-image {
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
  animation: scaleIn 0.3s ease-in-out;
  cursor: pointer;
  display: block;
}

.lightbox-close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  width: 45px;
  height: 45px;
  font-size: 28px;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2), 
              inset 0 1px 0 rgba(255, 255, 255, 0.3);
  z-index: 10002;
  line-height: 1;
  text-align: center;
  padding: 0;
  margin: 0;
}

.lightbox-close-btn:hover {
  background: rgba(255, 255, 255, 0.35);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3), 
              inset 0 1px 0 rgba(255, 255, 255, 0.4);
  font-size: 30px;
}

.lightbox-fullscreen-btn {
  position: absolute;
  bottom: -40px;
  right: -10px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  font-size: 20px;
  font-weight: bold;
  color: #333;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  z-index: 10001;
}

.lightbox-fullscreen-btn:hover {
  background: white;
  transform: scale(1.1);
}

.clickable-image {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.clickable-image:hover {
  transform: scale(1.05);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes scaleIn {
  from {
    transform: scale(0.8);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

@media (max-width: 768px) {
  .lightbox-container {
    max-width: 98vw;
    max-height: 98vh;
    padding: 10px;
  }
  
  .lightbox-close-btn {
    top: 10px;
    right: 10px;
    width: 40px;
    height: 40px;
    font-size: 20px;
  }
}

@media (max-width: 375px) {
  .main-content {
    margin-left: 180px;
    width: calc(100vw - 180px);
  }
}
</style>
