<template>
  <div class="historiales-container">
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
                    <circle cx="12" cy="12" r="10" stroke-width="2"/>
                    <polyline points="12 6 12 12 16 14" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <span class="apple-title-divider">|</span>
                <h1 class="apple-page-title">HISTORIALES</h1>
              </div>
              <p class="apple-page-subtitle">Consulta de actividades por usuario</p>
            </div>
            
            <button @click="actualizarHistorial" class="apple-refresh-button" :disabled="loading">
              <svg :class="{ 'apple-spin': loading }" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </header>

        <!-- ================== STATS + SEARCH SECTION ================== -->
        <div class="apple-stats-section">
          <!-- Stats Cards cuando hay usuario seleccionado -->
          <div v-if="usuarioSeleccionado && resumen" class="apple-stats-grid">
            <div class="apple-stat-card">
              <div class="apple-stat-icon blue">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M9 12l2 2 4-4"/>
                  <path d="M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9 9 4.03 9 9z"/>
                </svg>
              </div>
              <div class="apple-stat-content">
                <div class="apple-stat-value">{{ resumen.estadisticas.total_registros }}</div>
                <div class="apple-stat-label">Total</div>
              </div>
            </div>

            <div class="apple-stat-card">
              <div class="apple-stat-icon green">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <line x1="12" y1="19" x2="12" y2="5" stroke-width="2"/>
                  <polyline points="5,12 12,5 19,12" stroke-width="2"/>
                </svg>
              </div>
              <div class="apple-stat-content">
                <div class="apple-stat-value">{{ resumen.estadisticas.entradas }}</div>
                <div class="apple-stat-label">Entradas</div>
              </div>
            </div>

            <div class="apple-stat-card">
              <div class="apple-stat-icon purple">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <line x1="12" y1="5" x2="12" y2="19" stroke-width="2"/>
                  <polyline points="19,12 12,19 5,12" stroke-width="2"/>
                </svg>
              </div>
              <div class="apple-stat-content">
                <div class="apple-stat-value">{{ resumen.estadisticas.salidas }}</div>
                <div class="apple-stat-label">Salidas</div>
              </div>
            </div>

            <div class="apple-stat-card">
              <div class="apple-stat-icon orange">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <circle cx="12" cy="12" r="3" stroke-width="2"/>
                  <path d="M12 1v6m0 6v6m11-7h-6m-6 0H1" stroke-width="2"/>
                </svg>
              </div>
              <div class="apple-stat-content">
                <div class="apple-stat-value">{{ resumen.estadisticas.actividades }}</div>
                <div class="apple-stat-label">Actividades</div>
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
                  v-model="terminoBusqueda" 
                  @input="onSearchInput"
                  @focus="abrirDropdown"
                  @blur="cerrarDropdownConDelay"
                  type="text" 
                  placeholder="Buscar usuario por nombre, correo o CURP..." 
                  class="apple-search-input"
                >
                <button v-if="terminoBusqueda" @click="limpiarBusqueda" class="apple-clear-btn">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10" stroke-width="2"/>
                    <line x1="15" y1="9" x2="9" y2="15" stroke-width="2" stroke-linecap="round"/>
                    <line x1="9" y1="9" x2="15" y2="15" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </button>
              </div>

              <!-- Usuario seleccionado badge -->
              <div v-if="usuarioActual" class="apple-selected-badge">
                <div class="apple-selected-avatar">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                </div>
                <span class="apple-selected-name">{{ usuarioActual.nombre_completo }}</span>
                <button @click="limpiarSeleccion" class="apple-remove-btn" title="Limpiar selección">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
              </div>

              <div class="apple-filter-controls">
                <button 
                  v-if="usuarioSeleccionado && historial.length > 0"
                  @click="exportarExcel" 
                  class="apple-filter-btn export"
                  :disabled="exportando"
                  title="Exportar a Excel"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span>{{ exportando ? 'Exportando...' : 'Excel' }}</span>
                </button>
              </div>
            </div>

            <!-- Unified Filter Row - Período + Fecha + Tipo -->
            <div v-if="usuarioSeleccionado" class="apple-unified-filters">
              <div class="apple-quick-filters">
                <button 
                  @click="setPeriodo('dia')"
                  :class="['apple-period-chip', { active: filtros.periodo === 'dia' }]"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke-width="2"/>
                    <line x1="16" y1="2" x2="16" y2="6" stroke-width="2"/>
                    <line x1="8" y1="2" x2="8" y2="6" stroke-width="2"/>
                    <line x1="3" y1="10" x2="21" y2="10" stroke-width="2"/>
                  </svg>
                  <span>Día</span>
                </button>
                <button 
                  @click="setPeriodo('semana')"
                  :class="['apple-period-chip', { active: filtros.periodo === 'semana' }]"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke-width="2"/>
                    <line x1="3" y1="10" x2="21" y2="10" stroke-width="2"/>
                  </svg>
                  <span>Semana</span>
                </button>
                <button 
                  @click="setPeriodo('mes')"
                  :class="['apple-period-chip', { active: filtros.periodo === 'mes' }]"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke-width="2"/>
                    <line x1="3" y1="10" x2="21" y2="10" stroke-width="2"/>
                    <line x1="9" y1="2" x2="9" y2="6" stroke-width="2"/>
                    <line x1="15" y1="2" x2="15" y2="6" stroke-width="2"/>
                  </svg>
                  <span>Mes</span>
                </button>
                <button 
                  @click="setPeriodo('año')"
                  :class="['apple-period-chip', { active: filtros.periodo === 'año' }]"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10" stroke-width="2"/>
                    <path d="M12 6v6l4 2" stroke-width="2"/>
                  </svg>
                  <span>Año</span>
                </button>
                <button 
                  @click="setPeriodo('todo')"
                  :class="['apple-period-chip', { active: filtros.periodo === 'todo' }]"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9 9 4.03 9 9z" stroke-width="2"/>
                    <path d="M9 12l2 2 4-4" stroke-width="2"/>
                  </svg>
                  <span>Todo</span>
                </button>
              </div>

              <!-- Selectores pill según período -->
              <div class="apple-filter-pill-row">
                <div v-if="filtros.periodo === 'dia'" :class="['apple-filter-pill', { active: filtros.fechaEspecifica }]">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <rect x="3" y="4" width="18" height="18" rx="2" stroke-width="2"/>
                    <line x1="16" y1="2" x2="16" y2="6" stroke-width="2"/>
                    <line x1="8" y1="2" x2="8" y2="6" stroke-width="2"/>
                    <line x1="3" y1="10" x2="21" y2="10" stroke-width="2"/>
                  </svg>
                  <input
                    type="date"
                    v-model="filtros.fechaEspecifica"
                    class="apple-pill-date"
                  >
                </div>

                <div v-if="filtros.periodo === 'semana'" :class="['apple-filter-pill', { active: filtros.semanaEspecifica }]">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <rect x="3" y="4" width="18" height="18" rx="2" stroke-width="2"/>
                    <line x1="3" y1="10" x2="21" y2="10" stroke-width="2"/>
                  </svg>
                  <input
                    type="week"
                    v-model="filtros.semanaEspecifica"
                    class="apple-pill-date"
                  >
                </div>

                <div v-if="filtros.periodo === 'mes'" :class="['apple-filter-pill', { active: filtros.mesEspecifico }]">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <rect x="3" y="4" width="18" height="18" rx="2" stroke-width="2"/>
                    <line x1="3" y1="10" x2="21" y2="10" stroke-width="2"/>
                  </svg>
                  <input
                    type="month"
                    v-model="filtros.mesEspecifico"
                    class="apple-pill-date"
                  >
                </div>

                <div v-if="filtros.periodo === 'año'" :class="['apple-filter-pill', { active: filtros.añoEspecifico }]">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10" stroke-width="2"/>
                    <path d="M12 6v6l4 2" stroke-width="2"/>
                  </svg>
                  <select v-model="filtros.añoEspecifico" class="apple-pill-select">
                    <option v-for="año in añosDisponibles" :key="año" :value="año">{{ año }}</option>
                  </select>
                </div>

                <div :class="['apple-filter-pill', { active: filtros.tipo }]">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" stroke-width="2"/>
                  </svg>
                  <select v-model="filtros.tipo" class="apple-pill-select">
                    <option value="">Tipo</option>
                    <option value="entrada">Entrada</option>
                    <option value="salida">Salida</option>
                    <option value="actividad">Actividad</option>
                  </select>
                </div>

                <div :class="['apple-filter-pill', { active: ordenAscendente }]" @click="toggleOrden">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M3 6h18M6 12h12M9 18h6" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                  <span class="apple-pill-label">{{ ordenAscendente ? 'Antiguo → Reciente' : 'Reciente → Antiguo' }}</span>
                </div>
              </div>

              <div v-if="historialOrdenado.length > 0" class="apple-count-badge">
                {{ historialOrdenado.length }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ================== CONTENT WRAPPER ================== -->
      <div class="apple-content-wrapper">
        <!-- Estado cuando no hay usuario seleccionado -->
        <div v-if="!usuarioSeleccionado" class="apple-welcome-section">
          <div class="apple-welcome-card">
            <div class="apple-welcome-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="11" cy="11" r="8"/>
                <path d="m21 21-4.35-4.35"/>
              </svg>
            </div>
            <h2>Buscar Historial de Usuario</h2>
            <p>Utiliza el buscador superior para encontrar y seleccionar un usuario.</p>
            <div class="apple-welcome-hint">
              <span class="apple-hint-icon">💡</span>
              <span>Puedes buscar por nombre, correo o CURP</span>
            </div>
          </div>
        </div>

        <!-- Tabla de historial -->
        <div v-else class="apple-table-container">
          <div v-if="loading && historial.length === 0" class="apple-loading">
            <div class="apple-spinner"></div>
            <p>Cargando historial...</p>
          </div>

          <div v-else-if="error" class="apple-error">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="10" stroke-width="2"/>
              <line x1="15" y1="9" x2="9" y2="15" stroke-width="2" stroke-linecap="round"/>
              <line x1="9" y1="9" x2="15" y2="15" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <h3>Error al cargar el historial</h3>
            <p>{{ error }}</p>
            <button @click="cargarHistorial" class="apple-retry-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"/>
              </svg>
              Reintentar
            </button>
          </div>

          <div v-else-if="historial.length === 0" class="apple-empty">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="10" stroke-width="1.5"/>
              <polyline points="12 6 12 12 16 14" stroke-width="2"/>
            </svg>
            <h3>No hay registros</h3>
            <p>No se encontraron registros para los filtros seleccionados.</p>
          </div>

          <div v-else class="apple-table-wrapper">
            <table class="apple-table">
              <thead>
                <tr>
                  <th>Origen</th>
                  <th>Tipo</th>
                  <th>Descripción</th>
                  <th>Fecha</th>
                  <th>Hora</th>
                  <th class="th-imagen">Imagen</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="registro in historialOrdenado" :key="registro.id" class="apple-table-row">
                  <td>
                    <span :class="['apple-origen-badge', registro.origen]">
                      {{ formatearOrigen(registro.origen) }}
                    </span>
                  </td>
                  <td>
                    <span :class="['apple-tipo-badge', registro.tipo]">
                      {{ formatearTipo(registro.tipo) }}
                    </span>
                  </td>
                  <td class="apple-descripcion-cell">
                    {{ registro.descripcion || 'Sin descripción' }}
                  </td>
                  <td class="apple-fecha-cell">
                    {{ formatearFecha(registro.fecha) }}
                  </td>
                  <td class="apple-hora-cell">
                    {{ formatearHora(registro.hora) }}
                  </td>
                  <td class="td-imagen-cell">
                    <img 
                      v-if="obtenerImagenUrl(registro)" 
                      :src="obtenerImagenUrl(registro)"
                      alt="Foto" 
                      class="apple-photo-thumb"
                      @click="abrirFotoCompleta(obtenerImagenUrl(registro))"
                    >
                    <span v-else class="apple-no-data">—</span>
                  </td>
                  <td>
                    <div class="apple-actions">
                      <button 
                        v-if="registro.detalles" 
                        @click="mostrarDetalles(registro)" 
                        class="apple-action-btn view" 
                        title="Ver detalles"
                      >
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke-width="2"/>
                          <circle cx="12" cy="12" r="3" stroke-width="2"/>
                        </svg>
                      </button>
                      <span v-else class="apple-no-details">-</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
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

    <!-- DROPDOWN DE BÚSQUEDA - TELEPORT AL BODY -->
    <Teleport to="body">
      <Transition name="apple-dropdown">
        <div 
          v-if="mostrarResultados && terminoBusqueda.length > 0" 
          class="apple-search-dropdown-portal"
          :style="dropdownStyle"
          @mousedown.prevent
        >
          <div v-if="buscandoUsuarios" class="apple-dropdown-loading">
            <div class="apple-spinner-mini"></div>
            <span>Buscando...</span>
          </div>
          <div v-else-if="terminoBusqueda.length < 2" class="apple-dropdown-hint">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 8v4m0 4h.01"/>
            </svg>
            <span>Escribe al menos 2 caracteres</span>
          </div>
          <div v-else-if="usuariosFiltrados.length === 0" class="apple-dropdown-empty">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
            <span>No se encontraron usuarios</span>
          </div>
          <div v-else class="apple-dropdown-results">
            <div 
              v-for="usuario in usuariosFiltrados" 
              :key="usuario.id" 
              :class="['apple-dropdown-item', { active: usuarioSeleccionado === usuario.id.toString() }]"
              @click="seleccionarUsuarioDesdeDropdown(usuario)"
            >
              <div class="apple-dropdown-avatar">
                {{ getInitials(usuario.nombre_completo) }}
              </div>
              <div class="apple-dropdown-info">
                <div class="apple-dropdown-name">{{ usuario.nombre_completo }}</div>
                <div class="apple-dropdown-email">{{ usuario.correo || 'Sin correo' }}</div>
                <div v-if="usuario.cargo" class="apple-dropdown-cargo">{{ usuario.cargo }}</div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

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
import Sidebar from '../components/Sidebar.vue'
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
    
    // Dropdown posición (para Teleport)
    const searchContainer = ref(null)
    const searchInput = ref(null)
    const dropdownPosition = ref({ top: 0, left: 0, width: 0 })
    
    // Estilo del dropdown calculado
    const dropdownStyle = computed(() => ({
      position: 'fixed',
      top: `${dropdownPosition.value.top}px`,
      left: `${dropdownPosition.value.left}px`,
      width: `${dropdownPosition.value.width}px`,
      zIndex: 99999
    }))
    
    // Filtros
    const filtros = ref({
      periodo: 'todo', // 'dia', 'semana', 'mes', 'año', 'todo'
      fechaEspecifica: new Date().toISOString().split('T')[0],
      semanaEspecifica: '',
      mesEspecifico: new Date().toISOString().slice(0, 7), // formato YYYY-MM
      añoEspecifico: new Date().getFullYear(),
      tipo: '' // '', 'entrada', 'salida', 'actividad'
    })
    
    // Orden de resultados
    const ordenAscendente = ref(true) // true = antiguo a reciente, false = reciente a antiguo

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

    // Historial ordenado y filtrado localmente
    const historialOrdenado = computed(() => {
      if (!historial.value || historial.value.length === 0) return []
      
      let resultado = [...historial.value]
      
      // ========== FILTRO POR TIPO ==========
      if (filtros.value.tipo) {
        resultado = resultado.filter(r => {
          const tipoRegistro = (r.tipo || r.tipo_actividad || '').toLowerCase()
          return tipoRegistro === filtros.value.tipo.toLowerCase()
        })
      }
      
      // ========== FILTRO POR PERÍODO Y FECHA ==========
      if (filtros.value.periodo !== 'todo') {
        resultado = resultado.filter(r => {
          const fechaRegistro = new Date(r.fecha_hora || r.fecha || r.timestamp)
          if (isNaN(fechaRegistro.getTime())) return true // Si no hay fecha válida, incluir
          
          const fechaRegistroStr = fechaRegistro.toISOString().split('T')[0]
          
          switch (filtros.value.periodo) {
            case 'dia':
              if (filtros.value.fechaEspecifica) {
                return fechaRegistroStr === filtros.value.fechaEspecifica
              }
              break
              
            case 'semana':
              if (filtros.value.semanaEspecifica) {
                const fechasSemana = calcularFechasSemanaLocal(filtros.value.semanaEspecifica)
                return fechaRegistroStr >= fechasSemana.inicio && fechaRegistroStr <= fechasSemana.fin
              }
              break
              
            case 'mes':
              if (filtros.value.mesEspecifico) {
                const [year, month] = filtros.value.mesEspecifico.split('-')
                const inicioMes = `${year}-${month}-01`
                const lastDay = new Date(parseInt(year), parseInt(month), 0).getDate()
                const finMes = `${year}-${month}-${lastDay.toString().padStart(2, '0')}`
                return fechaRegistroStr >= inicioMes && fechaRegistroStr <= finMes
              }
              break
              
            case 'año':
              if (filtros.value.añoEspecifico) {
                const inicioAño = `${filtros.value.añoEspecifico}-01-01`
                const finAño = `${filtros.value.añoEspecifico}-12-31`
                return fechaRegistroStr >= inicioAño && fechaRegistroStr <= finAño
              }
              break
          }
          return true
        })
      }
      
      // ========== ORDENAR POR FECHA ==========
      return resultado.sort((a, b) => {
        const fechaA = new Date(a.fecha_hora || a.fecha || a.timestamp || 0)
        const fechaB = new Date(b.fecha_hora || b.fecha || b.timestamp || 0)
        
        if (ordenAscendente.value) {
          return fechaA - fechaB // Antiguo a reciente
        } else {
          return fechaB - fechaA // Reciente a antiguo
        }
      })
    })
    
    // Función auxiliar para calcular fechas de semana (local)
    const calcularFechasSemanaLocal = (semanaString) => {
      if (!semanaString || !semanaString.includes('-W')) {
        return { inicio: '', fin: '' }
      }
      const [year, week] = semanaString.split('-W')
      const yearNum = parseInt(year)
      const weekNum = parseInt(week)
      
      // Calcular el primer día de la semana ISO (lunes)
      const simple = new Date(yearNum, 0, 1 + (weekNum - 1) * 7)
      const dow = simple.getDay()
      const ISOweekStart = simple
      if (dow <= 4) {
        ISOweekStart.setDate(simple.getDate() - simple.getDay() + 1)
      } else {
        ISOweekStart.setDate(simple.getDate() + 8 - simple.getDay())
      }
      
      const inicio = new Date(ISOweekStart)
      const fin = new Date(ISOweekStart)
      fin.setDate(inicio.getDate() + 6)
      
      return {
        inicio: inicio.toISOString().split('T')[0],
        fin: fin.toISOString().split('T')[0]
      }
    }

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
        console.log('🔍 Cargando historial COMPLETO para usuario ID:', userId)
        
        // Cargar TODO el historial sin filtros - el filtrado será local e instantáneo
        const data = await historialService.obtenerHistorialCompleto(userId, {})
        
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
          
        case 'mes':
          if (filtros.value.mesEspecifico) {
            const [year, month] = filtros.value.mesEspecifico.split('-')
            const lastDay = new Date(parseInt(year), parseInt(month), 0).getDate()
            filtrosAPI.fechaInicio = `${year}-${month}-01`
            filtrosAPI.fechaFin = `${year}-${month}-${lastDay.toString().padStart(2, '0')}`
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
          const fechaActual = new Date()
          const año = fechaActual.getFullYear()
          const semana = getWeekNumber(fechaActual)
          filtros.value.semanaEspecifica = `${año}-W${semana.toString().padStart(2, '0')}`
          break
        case 'mes':
          filtros.value.mesEspecifico = new Date().toISOString().slice(0, 7)
          break
        case 'año':
          filtros.value.añoEspecifico = new Date().getFullYear()
          break
      }
      // El filtrado es AUTOMÁTICO y LOCAL via computed (historialOrdenado)
      // No necesita recargar de la API - es instantáneo
    }
    
    const toggleOrden = () => {
      ordenAscendente.value = !ordenAscendente.value
    }

    const getWeekNumber = (date) => {
      const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()))
      const dayNum = d.getUTCDay() || 7
      d.setUTCDate(d.getUTCDate() + 4 - dayNum)
      const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1))
      return Math.ceil((((d - yearStart) / 86400000) + 1) / 7)
    }

    const aplicarFiltros = () => {
      // Los filtros ahora se aplican localmente en historialOrdenado (computed)
      // Solo recargamos si no hay historial cargado
      if (usuarioSeleccionado.value && historial.value.length === 0) {
        cargarHistorial()
      }
    }
    
    // Los filtros se aplican LOCAL e INSTANTÁNEAMENTE via computed (historialOrdenado)
    // NO necesitamos watcher que llame a la API - el filtrado es reactivo y local

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

    // Métodos de búsqueda de usuarios - OPTIMIZADO para velocidad
    const buscarUsuarios = async () => {
      // Limpiar timeout anterior
      if (timeoutBusqueda.value) {
        clearTimeout(timeoutBusqueda.value)
      }

      const termino = terminoBusqueda.value.trim().toLowerCase()
      
      if (termino.length === 0) {
        usuariosFiltrados.value = []
        mostrarResultados.value = false
        return
      }

      if (termino.length < 2) {
        usuariosFiltrados.value = []
        mostrarResultados.value = true
        return
      }

      // BÚSQUEDA LOCAL INMEDIATA (sin espera)
      if (usuarios.value && usuarios.value.length > 0) {
        const resultadosLocales = usuarios.value.filter(u => {
          const nombre = (u.nombre_completo || '').toLowerCase()
          const correo = (u.correo || '').toLowerCase()
          const curp = (u.curp || '').toLowerCase()
          return nombre.includes(termino) || 
                 correo.includes(termino) || 
                 curp.includes(termino)
        }).slice(0, 10)
        
        if (resultadosLocales.length > 0) {
          usuariosFiltrados.value = resultadosLocales
          mostrarResultados.value = true
          // Si encontramos suficientes locales, no buscar en servidor
          if (resultadosLocales.length >= 5) return
        }
      }

      // Búsqueda en servidor con debounce reducido (100ms)
      timeoutBusqueda.value = setTimeout(async () => {
        try {
          buscandoUsuarios.value = true
          
          const resultados = await usuariosService.buscarUsuarios(termino)
          
          // Combinar con resultados locales sin duplicados
          const idsLocales = new Set(usuariosFiltrados.value.map(u => u.id))
          const nuevos = resultados.filter(u => !idsLocales.has(u.id))
          usuariosFiltrados.value = [...usuariosFiltrados.value, ...nuevos].slice(0, 15)
          mostrarResultados.value = true
          
        } catch (err) {
          console.error('❌ Error al buscar usuarios:', err)
          // Mantener resultados locales si hay error
          if (usuariosFiltrados.value.length === 0) {
            error.value = 'Error al buscar usuarios'
          }
          mostrarResultados.value = true
        } finally {
          buscandoUsuarios.value = false
        }
      }, 100)
    }

    // Métodos para dropdown con Teleport
    const actualizarPosicionDropdown = () => {
      if (searchContainer.value) {
        const rect = searchContainer.value.getBoundingClientRect()
        dropdownPosition.value = {
          top: rect.bottom + 8,
          left: rect.left,
          width: rect.width
        }
      }
    }

    const abrirDropdown = () => {
      actualizarPosicionDropdown()
      mostrarResultados.value = true
    }

    const cerrarDropdownConDelay = () => {
      setTimeout(() => {
        mostrarResultados.value = false
      }, 180)
    }

    const onSearchInput = () => {
      actualizarPosicionDropdown()
      buscarUsuarios()
    }

    const getInitials = (name) => {
      if (!name) return '?'
      const words = name.trim().split(' ')
      if (words.length >= 2) {
        return (words[0][0] + words[1][0]).toUpperCase()
      }
      return name.substring(0, 2).toUpperCase()
    }

    const seleccionarUsuarioDesdeDropdown = (usuario) => {
      mostrarResultados.value = false
      seleccionarUsuario(usuario)
    }

    const limpiarBusqueda = () => {
      terminoBusqueda.value = ''
      usuariosFiltrados.value = []
      mostrarResultados.value = false
      if (timeoutBusqueda.value) {
        clearTimeout(timeoutBusqueda.value)
      }
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
      historialOrdenado,
      resumen,
      usuarioActual,
      filtros,
      modalDetalles,
      añosDisponibles,
      adminUser,
      ordenAscendente,
      
      // Lightbox
      showLightbox,
      lightboxImageUrl,
      
      // Estados de búsqueda
      terminoBusqueda,
      usuariosFiltrados,
      buscandoUsuarios,
      mostrarResultados,
      
      // Dropdown Teleport
      searchContainer,
      searchInput,
      dropdownStyle,
      dropdownPosition,
      abrirDropdown,
      cerrarDropdownConDelay,
      onSearchInput,
      getInitials,
      seleccionarUsuarioDesdeDropdown,
      
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
      toggleOrden,
      
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

/* ==================== APPLE DESIGN SYSTEM ==================== */

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

/* ====================== MAIN CONTENT ====================== */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
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
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 10px;
  margin-bottom: 12px;
}

.apple-stat-card {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.apple-stat-card:hover {
  background: #f0f1f3;
}

.apple-stat-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.apple-stat-icon.blue {
  background: #007AFF;
}

.apple-stat-icon.green {
  background: #34C759;
}

.apple-stat-icon.purple {
  background: #AF52DE;
}

.apple-stat-icon.orange {
  background: linear-gradient(135deg, #FF9500 0%, #FFCC00 100%);
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
  border-color: #007AFF;
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

/* ====================== APPLE SEARCH DROPDOWN ====================== */
.apple-search-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  right: 0;
  background: white;
  border-radius: 16px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(0, 0, 0, 0.08);
  max-height: 320px;
  overflow-y: auto;
  z-index: 1000;
  animation: dropdownSlide 0.2s ease;
}

@keyframes dropdownSlide {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.apple-dropdown-loading,
.apple-dropdown-hint,
.apple-dropdown-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 24px;
  color: #86868b;
  font-size: 12px;
  font-weight: 500;
}

.apple-dropdown-loading svg,
.apple-dropdown-hint svg,
.apple-dropdown-empty svg {
  width: 18px;
  height: 18px;
  stroke: #86868b;
}

.apple-spinner-mini {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(0, 122, 255, 0.2);
  border-top-color: #007AFF;
  border-radius: 50%;
  animation: apple-spin-animation 0.8s linear infinite;
}

.apple-dropdown-results {
  padding: 8px 0;
}

.apple-dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.apple-dropdown-item:last-child {
  border-bottom: none;
}

.apple-dropdown-item:hover {
  background: rgba(0, 122, 255, 0.06);
}

.apple-dropdown-item.active {
  background: linear-gradient(135deg, rgba(139, 195, 74, 0.1) 0%, rgba(102, 187, 106, 0.05) 100%);
}

.apple-dropdown-avatar {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #8BC34A 0%, #66BB6A 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.apple-dropdown-avatar svg {
  width: 18px;
  height: 18px;
  color: white;
  stroke: white;
}

.apple-dropdown-info {
  flex: 1;
  min-width: 0;
}

.apple-dropdown-name {
  font-size: 13px;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 2px;
}

.apple-dropdown-email {
  font-size: 11px;
  color: #86868b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.apple-dropdown-cargo {
  display: inline-block;
  margin-top: 4px;
  padding: 2px 8px;
  background: rgba(139, 195, 74, 0.15);
  color: #558B2F;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 600;
}

/* ====================== APPLE SELECTED BADGE ====================== */
.apple-selected-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: linear-gradient(135deg, rgba(139, 195, 74, 0.15) 0%, rgba(102, 187, 106, 0.1) 100%);
  border: 1.5px solid rgba(139, 195, 74, 0.3);
  border-radius: 20px;
  flex-shrink: 0;
}

.apple-selected-avatar {
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, #8BC34A 0%, #66BB6A 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.apple-selected-avatar svg {
  width: 12px;
  height: 12px;
  color: white;
  stroke: white;
}

.apple-selected-name {
  font-size: 12px;
  font-weight: 600;
  color: #558B2F;
  max-width: 150px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.apple-remove-btn {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.1);
  border: none;
  color: #ef4444;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  padding: 0;
}

.apple-remove-btn svg {
  width: 12px;
  height: 12px;
  stroke: #ef4444;
}

.apple-remove-btn:hover {
  background: #ef4444;
}

.apple-remove-btn:hover svg {
  stroke: white;
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

.apple-filter-btn.export:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ====================== APPLE UNIFIED FILTERS ====================== */
.apple-unified-filters {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

/* ====================== APPLE QUICK FILTERS ====================== */
.apple-quick-filters {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

/* ====================== APPLE PERIOD CHIPS ====================== */
.apple-period-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 8px 14px;
  border-radius: 50px;
  border: 1.5px solid #e5e5e5;
  background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
  color: #374151;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.apple-period-chip svg {
  width: 14px;
  height: 14px;
  stroke-width: 2;
  transition: stroke 0.2s ease;
}

.apple-period-chip:hover {
  border-color: #007AFF;
  background: linear-gradient(145deg, #ffffff 0%, #f0f7ff 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.12);
}

.apple-period-chip:hover svg {
  stroke: #007AFF;
}

.apple-period-chip.active {
  background: linear-gradient(145deg, #007AFF 0%, #0056CC 100%);
  color: white;
  border-color: #007AFF;
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
}

.apple-period-chip.active span {
  color: white !important;
}

.apple-period-chip.active svg {
  stroke: white !important;
}

/* ====================== APPLE FILTER PILL ROW ====================== */
.apple-filter-pill-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

/* ====================== APPLE FILTER PILLS ====================== */
.apple-filter-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 0 4px 0 12px;
  height: 36px;
  border-radius: 50px;
  background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
  border: 1.5px solid #e5e5e5;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.apple-filter-pill:hover {
  border-color: #007AFF;
  background: linear-gradient(145deg, #ffffff 0%, #f0f7ff 100%);
  box-shadow: 0 4px 12px rgba(0, 122, 255, 0.12);
  transform: translateY(-1px);
}

.apple-filter-pill:focus-within {
  border-color: #007AFF;
  box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1);
}

.apple-filter-pill svg {
  width: 15px;
  height: 15px;
  stroke: #86868b;
  stroke-width: 2;
  flex-shrink: 0;
  transition: stroke 0.2s ease;
}

.apple-filter-pill:hover svg {
  stroke: #007AFF;
}

.apple-filter-pill.active {
  background: linear-gradient(145deg, #e8f4ff 0%, #d6eaff 100%);
  border-color: #007AFF;
}

.apple-filter-pill.active svg {
  stroke: #007AFF;
}

.apple-pill-date {
  appearance: none;
  border: none;
  background: transparent;
  padding: 0 12px 0 4px;
  font-size: 13px;
  font-weight: 500;
  color: #1d1d1f;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
  cursor: pointer;
  outline: none;
  min-width: 100px;
}

.apple-pill-date::-webkit-calendar-picker-indicator {
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.apple-pill-date::-webkit-calendar-picker-indicator:hover {
  opacity: 1;
}

.apple-pill-select {
  appearance: none;
  border: none;
  background: transparent;
  padding: 0 28px 0 4px;
  font-size: 13px;
  font-weight: 500;
  color: #1d1d1f;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
  cursor: pointer;
  outline: none;
  min-width: 60px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 24 24' fill='none' stroke='%2386868b' stroke-width='2.5'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 8px center;
}

.apple-pill-select option {
  padding: 12px;
  font-size: 14px;
  background: white;
  color: #1d1d1f;
}

.apple-pill-label {
  font-size: 12px;
  font-weight: 500;
  color: #1d1d1f;
  padding-right: 12px;
  white-space: nowrap;
}

.apple-filter-pill.active .apple-pill-select,
.apple-filter-pill.active .apple-pill-date,
.apple-filter-pill.active .apple-pill-label {
  color: #0056CC;
  font-weight: 600;
}

/* ====================== LEGACY APPLE FILTER CHIP (para compatibilidad) ====================== */
.apple-filter-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 7px 12px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  background: white;
  color: #374151;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-filter-chip svg {
  width: 13px;
  height: 13px;
  stroke-width: 2;
}

.apple-filter-chip:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.apple-filter-chip.active {
  background: #007AFF;
  color: white;
  border-color: #007AFF;
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

.apple-date-input,
.apple-select {
  height: 34px;
  border-radius: 10px;
  border: 1.5px solid #e5e5e5;
  background: #f5f5f7;
  padding: 0 12px;
  font-size: 12px;
  color: #1d1d1f;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s ease;
}

.apple-select {
  padding: 0 28px 0 12px;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2386868b' stroke-width='2'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
}

.apple-date-input:hover,
.apple-select:hover {
  border-color: #d1d1d6;
  background-color: white;
}

.apple-date-input:focus,
.apple-select:focus {
  outline: none;
  border-color: #8BC34A;
}

.apple-count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 8px;
  border-radius: 12px;
  background: #8BC34A;
  color: white;
  font-size: 11px;
  font-weight: 700;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

/* ====================== APPLE CONTENT WRAPPER ====================== */
.apple-content-wrapper {
  padding: 0;
  overflow-x: hidden;
}

/* ====================== APPLE TABLE CONTAINER ====================== */
.apple-table-container {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
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
  border-bottom: 1px solid #e5e7eb;
  transition: all 0.15s ease;
  background: white;
}

.apple-table-row:nth-child(even) {
  background: #f9fafb;
}

.apple-table-row:hover {
  background: #f3f4f6;
}

.apple-table-row:hover td:first-child {
  border-left-color: #8BC34A;
}

.apple-table td {
  padding: 14px 16px;
  font-size: 13px;
  color: #1D1D1F;
  border-left: 2px solid transparent;
  transition: all 0.15s ease;
  vertical-align: middle;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

/* ====================== APPLE BADGES ====================== */
.apple-origen-badge,
.apple-tipo-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}

.apple-origen-badge {
  background: rgba(139, 195, 74, 0.15);
  color: #558B2F;
}

.apple-origen-badge.web {
  background: rgba(59, 130, 246, 0.15);
  color: #2563eb;
}

.apple-origen-badge.app {
  background: rgba(139, 195, 74, 0.15);
  color: #558B2F;
}

.apple-origen-badge.sistema {
  background: rgba(107, 114, 128, 0.15);
  color: #4b5563;
}

.apple-tipo-badge.entrada {
  background: rgba(34, 197, 94, 0.15);
  color: #16a34a;
}

.apple-tipo-badge.salida {
  background: rgba(239, 68, 68, 0.15);
  color: #dc2626;
}

.apple-tipo-badge.actividad {
  background: rgba(59, 130, 246, 0.15);
  color: #2563eb;
}

/* ====================== APPLE PHOTO THUMBNAIL ====================== */
.th-imagen {
  text-align: center;
  width: 60px;
}

.td-imagen-cell {
  text-align: center;
  vertical-align: middle;
}

.apple-photo-thumb {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  object-fit: cover;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  border: 2px solid rgba(139, 195, 74, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.apple-photo-thumb:hover {
  transform: scale(1.15);
  border-color: #8BC34A;
  box-shadow: 0 6px 16px rgba(139, 195, 74, 0.4);
}

.apple-no-data {
  color: #d1d1d6;
  font-size: 13px;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Responsivo para columna de imagen */
@media (max-width: 1024px) {
  .apple-photo-thumb {
    width: 34px;
    height: 34px;
  }
  
  .th-imagen {
    width: 50px;
  }
}

@media (max-width: 768px) {
  .apple-photo-thumb {
    width: 32px;
    height: 32px;
  }
  
  .th-imagen {
    width: 45px;
  }
}

@media (max-width: 640px) {
  .th-imagen {
    display: none;
  }
  
  .td-imagen-cell {
    display: none;
  }
}

.apple-descripcion-cell {
  max-width: 250px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.apple-fecha-cell,
.apple-hora-cell {
  white-space: nowrap;
  color: #86868b;
  font-size: 12px;
}

/* ====================== APPLE ACTIONS ====================== */
.apple-actions {
  display: flex;
  gap: 6px;
}

.apple-action-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.apple-action-btn svg {
  width: 14px;
  height: 14px;
  stroke-width: 2;
}

.apple-action-btn.view {
  background: #007AFF;
  color: white;
}

.apple-action-btn.view svg {
  stroke: white;
}

.apple-action-btn.view:hover {
  background: #0056b3;
  transform: scale(1.05);
}

.apple-no-details {
  color: #d1d1d6;
  font-size: 12px;
}

/* ====================== APPLE LOADING/ERROR/EMPTY ====================== */
.apple-loading,
.apple-error,
.apple-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 24px;
  text-align: center;
}

.apple-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(139, 195, 74, 0.2);
  border-top-color: #8BC34A;
  border-radius: 50%;
  animation: apple-spin-animation 0.8s linear infinite;
  margin-bottom: 16px;
}

.apple-loading p,
.apple-error p,
.apple-empty p {
  color: #86868b;
  font-size: 14px;
  margin: 8px 0 0 0;
}

.apple-error svg,
.apple-empty svg {
  width: 56px;
  height: 56px;
  margin-bottom: 16px;
}

.apple-error svg {
  color: #ef4444;
  stroke: #ef4444;
}

.apple-empty svg {
  color: #8BC34A;
  stroke: #8BC34A;
}

.apple-error h3,
.apple-empty h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0;
}

.apple-retry-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 16px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #8BC34A 0%, #7CB342 100%);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.apple-retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 195, 74, 0.4);
}

.apple-retry-btn svg {
  width: 16px;
  height: 16px;
}

/* ====================== APPLE WELCOME SECTION ====================== */
.apple-welcome-section {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 40px;
}

.apple-welcome-card {
  background: white;
  border-radius: 28px;
  padding: 48px;
  text-align: center;
  max-width: 450px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.04);
}

.apple-welcome-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, rgba(139, 195, 74, 0.15) 0%, rgba(102, 187, 106, 0.1) 100%);
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
}

.apple-welcome-icon svg {
  width: 40px;
  height: 40px;
  color: #8BC34A;
  stroke: #8BC34A;
}

.apple-welcome-card h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1d1d1f;
  margin: 0 0 12px 0;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
}

.apple-welcome-card p {
  color: #86868b;
  font-size: 15px;
  line-height: 1.6;
  margin: 0 0 24px 0;
}

.apple-welcome-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: rgba(139, 195, 74, 0.1);
  padding: 12px 20px;
  border-radius: 12px;
  color: #558B2F;
  font-size: 13px;
  font-weight: 500;
}

.apple-hint-icon {
  font-size: 16px;
}

/* ====================== RESPONSIVE STYLES ====================== */
@media (max-width: 1024px) {
  .apple-stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .apple-search-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .apple-search-container {
    min-width: 100%;
  }
  
  .apple-filter-controls {
    justify-content: flex-start;
    width: 100%;
  }
  
  .apple-unified-filters {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    width: 100%;
    padding: 8px;
  }
  
  .apple-page-header {
    border-radius: 20px 20px 0 0;
    padding: 8px 12px;
  }
  
  .apple-stats-section {
    border-radius: 0 0 20px 20px;
    padding: 14px 12px 12px 12px;
  }
  
  .apple-stats-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
  }
  
  .apple-stat-card {
    padding: 10px 8px;
    flex-direction: column;
    text-align: center;
    gap: 6px;
  }
  
  .apple-stat-icon {
    width: 28px;
    height: 28px;
  }
  
  .apple-stat-icon svg {
    width: 12px;
    height: 12px;
  }
  
  .apple-stat-value {
    font-size: 14px;
  }
  
  .apple-stat-label {
    font-size: 8px;
  }
  
  .apple-search-input {
    height: 36px;
    font-size: 11px;
  }
  
  .apple-filter-chip {
    padding: 5px 10px;
    font-size: 10px;
  }
  
  .apple-filter-chip svg {
    width: 11px;
    height: 11px;
  }
  
  .apple-table-container {
    max-height: calc(100vh - 380px);
    border-radius: 16px;
  }
  
  .apple-table th,
  .apple-table td {
    padding: 10px 12px;
    font-size: 11px;
  }
  
  .apple-descripcion-cell {
    max-width: 120px;
  }
  
  .apple-welcome-card {
    padding: 32px 24px;
  }
  
  .apple-welcome-icon {
    width: 60px;
    height: 60px;
  }
  
  .apple-welcome-icon svg {
    width: 30px;
    height: 30px;
  }
  
  .apple-welcome-card h2 {
    font-size: 20px;
  }
}

@media (max-width: 480px) {
  .apple-page-header {
    padding: 6px 10px;
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
  
  .apple-stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .apple-quick-filters {
    width: 100%;
    justify-content: center;
  }
  
  .apple-filter-group {
    width: 100%;
  }
  
  .apple-date-input,
  .apple-select {
    flex: 1;
    min-width: 0;
  }
  
  .apple-selected-badge {
    width: 100%;
    justify-content: center;
  }
  
  .apple-selected-name {
    max-width: none;
    flex: 1;
  }
}

/* ==================== END APPLE DESIGN SYSTEM ==================== */

/* ====================== OLD STYLES (KEPT FOR COMPATIBILITY) ====================== */

.page-header {
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
  z-index: 1;
}

.search-input-wrapper {
  position: relative;
  width: 100%;
  z-index: 2;
}

.search-icon {
  position: absolute;
  left: clamp(14px, 1.8vw, 16px);
  top: 50%;
  transform: translateY(-50%);
  color: rgba(76, 175, 80, 0.6);
  width: clamp(14px, 2.2vw, 16px);
  height: clamp(14px, 2.2vw, 16px);
  pointer-events: none;
  z-index: 3;
}

.search-input {
  width: 100%;
  padding: clamp(10px, 1.2vw, 12px) clamp(44px, 5vw, 48px) clamp(10px, 1.2vw, 12px) clamp(44px, 5vw, 48px);
  border: 1.5px solid rgba(76, 175, 80, 0.2);
  border-radius: 50px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  font-size: clamp(12px, 2vw, 13px);
  color: #2d3748;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-sizing: border-box;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.08), inset 0 1px 2px rgba(255, 255, 255, 0.9);
  position: relative;
  z-index: 1;
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
}

.search-input::placeholder {
  color: rgba(107, 114, 128, 0.6);
  font-size: clamp(11px, 1.9vw, 12px);
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
  z-index: 3;
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

/* Resultados de búsqueda - Dropdown flotante independiente */
.search-results-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  right: 0;
  background: white;
  border: 2px solid rgba(76, 175, 80, 0.4);
  border-radius: clamp(8px, 1.5vw, 12px);
  box-shadow: 0 8px 24px rgba(76, 175, 80, 0.3);
  max-height: min(calc(100vh - 280px), 600px);
  overflow-y: auto;
  z-index: 1000;
  animation: slideDown 0.2s ease-out;
  backdrop-filter: blur(8px);
}

@media (max-width: 768px) {
  .search-results-dropdown {
    max-height: calc(100vh - 320px);
  }
}

@media (min-width: 769px) and (max-width: 1366px) {
  .search-results-dropdown {
    max-height: calc(100vh - 300px);
  }
}

@media (min-width: 1367px) {
  .search-results-dropdown {
    max-height: 600px;
  }
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
  gap: clamp(8px, 1.4vw, 10px);
  padding: clamp(8px, 1.4vw, 10px);
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
  width: clamp(28px, 4.5vw, 32px);
  height: clamp(28px, 4.5vw, 32px);
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
  font-size: clamp(11px, 1.8vw, 13px);
  color: #2c5530;
  margin-bottom: clamp(2px, 0.4vw, 3px);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-details {
  display: flex;
  align-items: center;
  gap: clamp(4px, 0.8vw, 6px);
  margin-bottom: clamp(2px, 0.4vw, 3px);
}

.user-email {
  font-size: clamp(10px, 1.6vw, 11px);
  color: #6c757d;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 150px;
}

.user-curp {
  font-size: clamp(10px, 1.6vw, 11px);
  color: #6c757d;
  white-space: nowrap;
}

.user-cargo {
  font-size: clamp(10px, 1.6vw, 11px);
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
  padding: 20px;
  box-sizing: border-box;
  overflow: hidden;
}

.lightbox-container {
  position: relative;
  max-width: calc(100vw - 40px);
  max-height: calc(100vh - 40px);
  display: flex;
  justify-content: center;
  align-items: center;
}

.lightbox-image-wrapper {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 100%;
  max-height: calc(100vh - 60px);
}

.lightbox-image {
  max-width: calc(100vw - 60px);
  max-height: calc(100vh - 80px);
  width: auto;
  height: auto;
  object-fit: contain;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
  animation: scaleIn 0.3s ease-in-out;
  cursor: pointer;
  display: block;
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

/* Responsivo para lightbox */
@media (max-width: 768px) {
  .lightbox-overlay {
    padding: 15px;
  }
  
  .lightbox-image {
    max-width: calc(100vw - 40px);
    max-height: calc(100vh - 60px);
    border-radius: 8px;
  }
  
  .lightbox-close-btn {
    top: 10px;
    right: 10px;
    width: 40px;
    height: 40px;
    font-size: 22px;
  }
}

@media (max-width: 480px) {
  .lightbox-overlay {
    padding: 10px;
  }
  
  .lightbox-image {
    max-width: calc(100vw - 24px);
    max-height: calc(100vh - 50px);
    border-radius: 6px;
  }
  
  .lightbox-close-btn {
    top: 8px;
    right: 8px;
    width: 36px;
    height: 36px;
    font-size: 20px;
  }
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

<!-- Estilos GLOBALES para el dropdown portal (Teleport al body) -->
<style>
.apple-search-dropdown-portal {
  position: fixed;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  max-height: 340px;
  overflow-y: auto;
  z-index: 999999;
  transform-origin: top center;
}

.apple-search-dropdown-portal::-webkit-scrollbar {
  width: 6px;
}

.apple-search-dropdown-portal::-webkit-scrollbar-track {
  background: transparent;
}

.apple-search-dropdown-portal::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.15);
  border-radius: 3px;
}

/* Loading state */
.apple-search-dropdown-portal .apple-dropdown-loading {
  padding: 20px 16px;
  text-align: center;
  color: #007AFF;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.apple-search-dropdown-portal .apple-spinner-mini {
  width: 18px;
  height: 18px;
  border: 2px solid #007AFF;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin-dropdown 0.8s linear infinite;
}

/* Hint state */
.apple-search-dropdown-portal .apple-dropdown-hint,
.apple-search-dropdown-portal .apple-dropdown-empty {
  padding: 24px 16px;
  text-align: center;
  color: #8e8e93;
  font-size: 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.apple-search-dropdown-portal .apple-dropdown-hint svg,
.apple-search-dropdown-portal .apple-dropdown-empty svg {
  width: 28px;
  height: 28px;
  opacity: 0.5;
}

/* Results container */
.apple-search-dropdown-portal .apple-dropdown-results {
  padding: 6px 0;
}

/* Individual item */
.apple-search-dropdown-portal .apple-dropdown-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.apple-search-dropdown-portal .apple-dropdown-item:last-child {
  border-bottom: none;
}

.apple-search-dropdown-portal .apple-dropdown-item:hover {
  background: rgba(0, 122, 255, 0.08);
}

.apple-search-dropdown-portal .apple-dropdown-item:active {
  background: rgba(0, 122, 255, 0.15);
  transform: scale(0.99);
}

.apple-search-dropdown-portal .apple-dropdown-item.active {
  background: rgba(0, 122, 255, 0.12);
}

/* Avatar */
.apple-search-dropdown-portal .apple-dropdown-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #007AFF;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 13px;
  flex-shrink: 0;
}

/* Info container */
.apple-search-dropdown-portal .apple-dropdown-info {
  flex: 1;
  min-width: 0;
}

.apple-search-dropdown-portal .apple-dropdown-name {
  font-weight: 600;
  color: #1d1d1f;
  font-size: 14px;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.apple-search-dropdown-portal .apple-dropdown-email {
  font-size: 12px;
  color: #8e8e93;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.apple-search-dropdown-portal .apple-dropdown-cargo {
  font-size: 11px;
  color: #007AFF;
  font-weight: 500;
  margin-top: 2px;
}

@keyframes spin-dropdown {
  to { transform: rotate(360deg); }
}

/* Animaciones de entrada/salida */
.apple-dropdown-enter-active {
  animation: dropdownEnter 0.25s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

.apple-dropdown-leave-active {
  animation: dropdownLeave 0.2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

@keyframes dropdownEnter {
  from {
    opacity: 0;
    transform: translateY(-8px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes dropdownLeave {
  from {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  to {
    opacity: 0;
    transform: translateY(-6px) scale(0.97);
  }
}
</style>
