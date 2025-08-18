<template>
  <div class="visor-container">
    <!-- Importar fuentes modernas -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <Sidebar @logout="logout" />
    
    <main class="main-content">      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Visor de Seguimiento</h1>
              <p class="header-subtitle">Visualiza todas las ubicaciones en tiempo real</p>
            </div>
          </div>
          <div class="header-actions">
            <div class="connection-status" :class="{ 'online': isOnline, 'offline': !isOnline }">
              <div class="status-indicator"></div>
              <span class="status-text">{{ isOnline ? 'En línea' : 'Sin conexión' }}</span>
            </div>
            
            <!-- Contador de puntos en el mapa con efecto de cristal líquido -->
            <div class="lcd-counter">
              <div class="lcd-display">
                <div class="lcd-label">PUNTOS EN MAPA</div>
                <div class="lcd-number">{{ totalPuntosEnMapa.toLocaleString() }}</div>
              </div>
            </div>
            
            <button @click="recargarMapa" class="refresh-btn-icon" :disabled="loading" title="Actualizar manualmente">
              <svg class="refresh-icon" :class="{ spinning: loading }" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="23 4 23 10 17 10"></polyline>
                <polyline points="1 20 1 14 7 14"></polyline>
                <path d="m3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
              </svg>
            </button>
          </div>
        </div>
      </header>

      <!-- Contadores pequeños desde Dashboard -->
      <div class="visor-stats-compact">
        <div class="compact-stat-card" v-for="stat in statCards" :key="stat.label">
          <div class="compact-stat-icon" v-html="stat.icon"></div>
          <div class="compact-stat-info">
            <span class="compact-stat-value">{{ stat.value }}</span>
            <span class="compact-stat-label">{{ stat.label }}</span>
          </div>
        </div>
      </div>

      <div class="page-content">        <div class="modern-filter-bar">
          <div class="filter-group">
            <div class="filter-item">
              <svg class="filter-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M3 18h6v-2H3v2zM3 6v2h18V6H3zm0 7h12v-2H3v2z"/>
              </svg>
              <select v-model="filtroTipo" class="modern-select" @change="aplicarFiltros">
                <option value="">Todas las actividades</option>
                <option value="entrada">Solo Entradas</option>
                <option value="salida">Solo Salidas</option>
                <option value="registro-hoy">Solo Registros de Hoy</option>
                <option value="registro-antiguo">Solo Registros Antiguos</option>
              </select>
            </div>
            
            <div class="filter-item">
              <svg class="filter-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M9 11H7v6h2v-6zm4 0h-2v6h2v-6zm4-4v11c0 1.1-.9 2-2 2H7c-1.1 0-2-.9-2-2V7c0-1.1.9-2 2-2h1V3c0-.55.45-1 1-1s1 .45 1 1v2h6V3c0-.55.45-1 1-1s1 .45 1 1v2h1c1.1 0 2 .9 2 2z"/>
              </svg>
              <select v-model="filtroPeriodo" class="modern-select" @change="aplicarFiltros">
                <option value="all">Todo el tiempo</option>
                <option value="today">Hoy</option>
                <option value="week">Esta semana</option>
                <option value="month">Este mes</option>
              </select>            </div>
            
            <div class="filter-item search-item">
              <div class="modern-search-wrapper">
                <svg class="search-input-icon" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
                </svg>
                <input 
                  v-model="busquedaUsuario" 
                  type="text" 
                  placeholder="Buscar usuario por nombre..." 
                  class="modern-search-input"
                  @input="buscarUsuarioEnTiempoReal"
                  @focus="mostrarSugerencias = true"
                  @blur="ocultarSugerenciasConDelay"
                  @keydown="manejarTeclasNavegacion"
                  autocomplete="off"
                >
                <!-- Dropdown de sugerencias -->
                <div 
                  v-if="mostrarSugerencias && sugerenciasUsuarios.length > 0" 
                  class="suggestions-dropdown"
                >
                  <div class="suggestions-header">
                    <span class="suggestions-count">{{ sugerenciasUsuarios.length }} usuario{{ sugerenciasUsuarios.length !== 1 ? 's' : '' }} encontrado{{ sugerenciasUsuarios.length !== 1 ? 's' : '' }}</span>
                  </div>
                  <div class="suggestions-list">
                    <div 
                      v-for="(usuario, index) in sugerenciasUsuarios" 
                      :key="`${usuario.usuario_id}-${usuario.tipo_actividad}`"
                      :class="['suggestion-item', { 'suggestion-selected': index === sugerenciaSeleccionada }]"
                      @mousedown="seleccionarUsuario(usuario, index)"
                      @mouseenter="sugerenciaSeleccionada = index"
                    >
                      <div class="suggestion-avatar">
                        <span :class="['avatar-letter', determinarTipoActividad(usuario).clase]">
                          {{ (usuario.usuario?.nombre_completo || `Usuario ${usuario.usuario_id}`).charAt(0).toUpperCase() }}
                        </span>
                      </div>
                      <div class="suggestion-info">
                        <div class="suggestion-name">
                          {{ usuario.usuario?.nombre_completo || `Usuario ${usuario.usuario_id}` }}
                        </div>
                        <div class="suggestion-details">
                          <span class="suggestion-email">{{ usuario.usuario?.correo || usuario.usuario?.email || 'Sin correo' }}</span>
                          <span :class="['suggestion-status', determinarTipoActividad(usuario).clase]">
                            {{ determinarTipoActividad(usuario).descripcion }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <!-- Indicador de usuario encontrado -->
                <div v-if="usuarioEncontrado && !mostrarSugerencias" class="user-found-indicator">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                  </svg>
                  <span>{{ usuarioEncontrado.usuario?.nombre_completo || `Usuario ${usuarioEncontrado.usuario_id}` }}</span>
                </div>                <button @click="enfocarUsuarioSeleccionado" class="modern-search-btn" :disabled="!usuarioEncontrado">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8M3.05,13H1V11H3.05C3.5,6.83 6.83,3.5 11,3.05V1H13V3.05C17.17,3.5 20.5,6.83 20.95,11H23V13H20.95C20.5,17.17 17.17,20.5 13,20.95V23H11V20.95C6.83,20.5 3.5,17.17 3.05,13M12,5A7,7 0 0,0 5,12A7,7 0 0,0 12,19A7,7 0 0,0 19,12A7,7 0 0,0 12,5Z"/>
                  </svg>
                </button>
              </div>
            </div>
            
            <!-- Leyenda de colores al lado del buscador -->
            <div class="filter-legend">
              <div class="legend-item-inline">
                <span class="legend-point-small entrada"></span>
                <span class="legend-text">Entrada</span>
              </div>
              <div class="legend-item-inline">
                <span class="legend-point-small salida"></span>
                <span class="legend-text">Salida</span>
              </div>
              <div class="legend-item-inline">
                <span class="legend-point-small registro-hoy"></span>
                <span class="legend-text">Registro Hoy</span>
              </div>
              <div class="legend-item-inline">
                <span class="legend-point-small antiguo"></span>
                <span class="legend-text">Anteriores</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Mapa principal -->
        <div class="visor-section">
          <div v-if="loading && !mapInitialized" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando mapa y ubicaciones...</p>
          </div>
          
          <div v-else-if="error" class="error-container">
            <p>{{ error }}</p>
            <button @click="inicializarMapa" class="retry-btn">Reintentar</button>
          </div>          
          <div id="mapa-principal" class="mapa-container">
            <!-- Panel lateral de detalles - dentro del mapa -->
            <div 
              v-if="mostrarPanelDetalles && registroSeleccionado" 
              class="registro-info-panel"
              :class="{ 
                'panel-visible': mostrarPanelDetalles,
                'panel-entrada': registroSeleccionado.tipo_actividad === 'entrada',
                'panel-salida': registroSeleccionado.tipo_actividad === 'salida',
                'panel-registro-hoy': registroSeleccionado.tipo_actividad === 'registro' && esUbicacionReciente(registroSeleccionado.fecha_hora),
                'panel-old': registroSeleccionado.tipo_actividad === 'registro' && !esUbicacionReciente(registroSeleccionado.fecha_hora)
              }"
            >
              <div class="panel-header">
                <div class="panel-title-section">
                  <h3>Detalles del Registro</h3>
                  <span class="panel-id">#{{ registroSeleccionado.tipo_actividad }}_{{ registroSeleccionado.usuario_id }}</span>
                </div>
                <button @click="cerrarPanelDetalles" class="close-panel-btn" title="Cerrar panel">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                  </svg>
                </button>
              </div>
              <div class="panel-content">

                <!-- Información del usuario -->
                <div class="user-section">
                  <div class="user-avatar-large">
                    <span class="avatar-text-large">{{ (registroSeleccionado.usuario?.nombre_completo || `Usuario ${registroSeleccionado.usuario_id}`).charAt(0).toUpperCase() }}</span>
                  </div>
                  <div class="user-info-detail">
                    <h4 class="user-name-large">{{ registroSeleccionado.usuario?.nombre_completo || `Usuario ${registroSeleccionado.usuario_id}` }}</h4>
                    <p class="user-email-large">{{ registroSeleccionado.usuario?.correo || registroSeleccionado.usuario?.email || 'Sin correo disponible' }}</p>
                  </div>
                </div>

                <!-- Información del registro -->
                <div class="info-section">
                  <h5 class="section-title">Información del Registro</h5>

                  <div class="info-item-detail">
                    <div class="info-icon-wrapper">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M9 11H7v6h2v-6zm4 0h-2v6h2v-6zm4-4v11c0 1.1-.9 2-2 2H7c-1.1 0-2-.9-2-2V7c0-1.1.9-2 2-2h1V3c0-.55.45-1 1-1s1 .45 1 1v2h6V3c0-.55.45-1 1-1s1 .45 1 1v2h1c1.1 0 2 .9 2 2z"/>
                      </svg>
                    </div>
                    <div class="info-text-wrapper">
                      <span class="info-label">Fecha y hora:</span>
                      <span class="info-value">{{ new Date(registroSeleccionado.fecha_hora).toLocaleString('es-ES') }}</span>
                    </div>
                  </div>

                  <div class="info-item-detail">
                    <div class="info-icon-wrapper">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                      </svg>
                    </div>
                    <div class="info-text-wrapper">
                      <span class="info-label">Coordenadas:</span>
                      <span class="info-value">{{ registroSeleccionado.latitud }}, {{ registroSeleccionado.longitud }}</span>
                    </div>
                  </div>

                  <div class="info-item-detail">
                    <div class="info-icon-wrapper">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                      </svg>
                    </div>
                    <div class="info-text-wrapper">
                      <span class="info-label">Estado:</span>
                      <span :class="['status-badge-large', determinarTipoActividad(registroSeleccionado).clase]">
                        {{ determinarTipoActividad(registroSeleccionado).descripcion }}
                      </span>
                    </div>
                  </div>

                  <div v-if="registroSeleccionado.descripcion" class="info-item-detail">
                    <div class="info-icon-wrapper">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                      </svg>
                    </div>
                    <div class="info-text-wrapper">
                      <span class="info-label">Descripción:</span>
                      <span class="info-value">{{ registroSeleccionado.descripcion }}</span>
                    </div>
                  </div>
                </div>

                <!-- Foto del registro -->
                <div v-if="registroSeleccionado.foto_url" class="photo-section">
                  <h5 class="section-title">Fotografía del Registro</h5>
                  <div class="photo-container" @click="verFotoAmpliada(registroSeleccionado.foto_url.startsWith('http') ? registroSeleccionado.foto_url : `${API_URL}/${registroSeleccionado.foto_url}`)">
                    <img 
                      :src="registroSeleccionado.foto_url.startsWith('http') ? registroSeleccionado.foto_url : `${API_URL}/${registroSeleccionado.foto_url}`" 
                      alt="Foto del registro" 
                      class="registro-photo"
                      @error="onImageError"
                      @load="onImageLoad">
                    <div class="photo-overlay">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                        <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
                      </svg>
                    </div>
                    <!-- Mini botón de descarga animado -->
                    <button @click.stop="descargarFoto(registroSeleccionado.foto_url.startsWith('http') ? registroSeleccionado.foto_url : `${API_URL}/${registroSeleccionado.foto_url}`, `registro_${registroSeleccionado.usuario_id}_${new Date(registroSeleccionado.fecha_hora).toISOString().slice(0,10)}.jpg`, $event)" class="download-mini-btn" title="Descargar imagen">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" class="download-icon">
                        <path d="M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z"/>
                      </svg>
                      <div class="download-progress"></div>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
      <!-- Modal para detalles completos y foto ampliada -->
    <div v-if="showModal" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop :class="modalType">
        <div class="modal-header">
          <h3>{{ modalTitle }}</h3>
          <button @click="cerrarModal" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <!-- Modal para foto ampliada -->
          <img v-if="modalType === 'photo'" :src="selectedPhotoUrl" alt="Fotografía ampliada" class="full-photo">
          
          <!-- Modal para detalles completos -->
          <div v-if="modalType === 'details'" class="details-modal-content">
            <!-- Información del usuario -->
            <div class="modal-user-section">
              <div class="modal-user-avatar">
                <span class="modal-avatar-text">{{ (registroSeleccionado?.usuario?.nombre_completo || `Usuario ${registroSeleccionado?.usuario_id}`).charAt(0).toUpperCase() }}</span>
              </div>
              <div class="modal-user-info">
                <h4 class="modal-user-name">{{ registroSeleccionado?.usuario?.nombre_completo || `Usuario ${registroSeleccionado?.usuario_id}` }}</h4>
                <p class="modal-user-email">{{ registroSeleccionado?.usuario?.correo || registroSeleccionado?.usuario?.email || 'correo@noregistrado.com' }}</p>
                <span :class="['modal-status-badge', determinarTipoActividad(registroSeleccionado).clase]">
                  {{ determinarTipoActividad(registroSeleccionado).descripcion }}
                </span>
              </div>
            </div>

            <!-- Grid de información detallada -->
            <div class="modal-info-grid">
              <div class="modal-info-card">
                <div class="modal-info-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M9 11H7v6h2v-6zm4 0h-2v6h2v-6zm4-4v11c0 1.1-.9 2-2 2H7c-1.1 0-2-.9-2-2V7c0-1.1.9-2 2-2h1V3c0-.55.45-1 1-1s1 .45 1 1v2h6V3c0-.55.45-1 1-1s1 .45 1 1v2h1c1.1 0 2 .9 2 2z"/>
                  </svg>
                </div>
                <div class="modal-info-content">
                  <h5>Fecha y Hora</h5>
                  <p>{{ formatFecha(registroSeleccionado?.fecha_hora) }}</p>
                </div>
              </div>

              <div class="modal-info-card">
                <div class="modal-info-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                  </svg>
                </div>
                <div class="modal-info-content">
                  <h5>Ubicación</h5>
                  <p>{{ formatCoordenadas(registroSeleccionado?.latitud, registroSeleccionado?.longitud) }}</p>
                </div>
              </div>

              <div class="modal-info-card">
                <div class="modal-info-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                  </svg>
                </div>
                <div class="modal-info-content">
                  <h5>ID del Registro</h5>
                  <p>#{{ registroSeleccionado?.id }}</p>
                </div>
              </div>

              <div v-if="registroSeleccionado?.descripcion" class="modal-info-card full-width">
                <div class="modal-info-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                  </svg>
                </div>
                <div class="modal-info-content">
                  <h5>Descripción</h5>
                  <p>{{ registroSeleccionado?.descripcion }}</p>
                </div>
              </div>
            </div>

            <!-- Foto si existe -->
            <div v-if="registroSeleccionado?.foto_url" class="modal-photo-section">
              <h5>Fotografía del Registro</h5>
              <div class="modal-photo-container">
                <img 
                  :src="`${API_URL}/${registroSeleccionado.foto_url}`" 
                  alt="Foto del registro"
                  @click="verFotoAmpliada(`${API_URL}/${registroSeleccionado.foto_url}`)"
                  class="modal-photo"
                >
                <div class="modal-photo-overlay" @click="verFotoAmpliada(`${API_URL}/${registroSeleccionado.foto_url}`)">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="white">
                    <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
                  </svg>
                </div>
              </div>
            </div>

            <!-- Acciones del modal -->
            <div class="modal-actions">
              <button @click="centrarMapa(registroSeleccionado)" class="modal-action-btn primary">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8M3.05,13H1V11H3.05C3.5,6.83 6.83,3.5 11,3.05V1H13V3.05C17.17,3.5 20.5,6.83 20.95,11H23V13H20.95C20.5,17.17 17.17,20.5 13,20.95V23H11V20.95C6.83,20.5 3.5,17.17 3.05,13M12,5A7,7 0 0,0 5,12A7,7 0 0,0 12,19A7,7 0 0,0 19,12A7,7 0 0,0 12,5Z"/>
                </svg>
                Centrar en mapa
              </button>
              <button @click="cerrarModal" class="modal-action-btn secondary">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                </svg>
                Cerrar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Sidebar from '../components/Sidebar.vue'
import { usuariosService } from '../services/usuariosService.js'
import asistenciasService from '../services/asistenciasService.js'
import { estadisticasService } from '../services/estadisticasService.js'

const router = useRouter()

// Estado de conexión
const isOnline = ref(navigator.onLine)

const API_URL = 'https://apipwa.sembrandodatos.com'
const registros = ref([])
const asistencias = ref([])
const usuarios = ref([])
const loading = ref(false)
const error = ref('')

// Variables para estadísticas
const stats = reactive({
  totalUsuarios: '-',
  registrosHoy: '-',
  asistenciasHoy: '-',
  usuariosPresentes: '-'
})

// Estado del mapa
const mapInitialized = ref(false)
let map = null
let markers = []
let markersLayer = null

// Filtros y búsqueda
const filtroTipo = ref('')
const filtroPeriodo = ref('all')
const busquedaUsuario = ref('')
const usuarioEncontrado = ref(null)
const ultimasActividades = ref([])
const mostrarSugerencias = ref(false)
const sugerenciasUsuarios = ref([])
const sugerenciaSeleccionada = ref(-1)

// Variables de tiempo para sugerencias solamente
const timeoutSugerencias = ref(null)

// Registro seleccionado y estado del panel de detalles
const registroSeleccionado = ref(null)
const mostrarPanelDetalles = ref(false)
const popupActivo = ref(null)

// Modal para foto ampliada
const showModal = ref(false)
const modalTitle = ref('')
const modalType = ref('')
const selectedPhotoUrl = ref('')

// Contador de puntos en el mapa
const totalPuntosEnMapa = ref(0)

// Computed property para las tarjetas de estadísticas compactas
const statCards = computed(() => [
  {
    label: 'Usuarios Activos',
    value: stats.totalUsuarios,
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><defs><linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#66BB6A;stop-opacity:1" /><stop offset="100%" style="stop-color:#4CAF50;stop-opacity:0.8" /></linearGradient></defs><path d="M16 7a4 4 0 1 1-8 0 4 4 0 0 1 8 0ZM12 14a7 7 0 0 0-7 7h14a7 7 0 0 0-7-7Z" fill="url(#grad2)"/></svg>`
  },
  {
    label: 'Actividades de Hoy',
    value: stats.registrosHoy,
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><defs><linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#66BB6A;stop-opacity:1" /><stop offset="100%" style="stop-color:#4CAF50;stop-opacity:0.8" /></linearGradient></defs><path d="M8 6h8v2H8zM6 10h12v8a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2z" fill="url(#grad3)"/><circle cx="9" cy="13" r="0.5" fill="#66BB6A"/><circle cx="12" cy="13" r="0.5" fill="#66BB6A"/><circle cx="15" cy="13" r="0.5" fill="#66BB6A"/></svg>`
  },
  {
    label: 'Asistencias Hoy',
    value: stats.asistenciasHoy,
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><defs><linearGradient id="grad5" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#66BB6A;stop-opacity:1" /><stop offset="100%" style="stop-color:#4CAF50;stop-opacity:0.8" /></linearGradient></defs><circle cx="12" cy="12" r="8" stroke="#4CAF50" stroke-width="2" fill="none"/><path d="m12 6 v6 l4 2" stroke="#4CAF50" stroke-width="2.5" stroke-linecap="round"/></svg>`
  },
  {
    label: 'Usuarios Presentes',
    value: stats.usuariosPresentes,
    icon: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><defs><linearGradient id="grad6" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#66BB6A;stop-opacity:1" /><stop offset="100%" style="stop-color:#4CAF50;stop-opacity:0.8" /></linearGradient></defs><circle cx="8" cy="8" r="2" fill="url(#grad6)"/><circle cx="16" cy="8" r="2" fill="url(#grad6)"/><path d="M4 18v-1a4 4 0 0 1 4-4h0a4 4 0 0 1 4 4v1M16 13a4 4 0 0 1 4 4v1" stroke="#4CAF50" stroke-width="2" stroke-linecap="round"/></svg>`
  }
])

// Función para formatear fechas
const formatFecha = (fechaStr) => {
  try {
    // Si viene una fecha ISO completa (con T), la procesamos con zona horaria
    if (typeof fechaStr === 'string' && fechaStr.includes('T')) {
      return new Date(fechaStr).toLocaleString('es-ES', {
        timeZone: 'America/Mexico_City' // Forzar zona horaria de México
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
      }) + ' 12:00:00'
    }
    
    // Para otros casos, usar el método estándar
    return new Date(fechaStr).toLocaleString('es-ES')
  } catch (e) {
    console.error('Error al formatear fecha:', e, 'Fecha original:', fechaStr)
    return fechaStr
  }
}

// Formatear coordenadas para mejor visualización
const formatCoordenadas = (lat, lng) => {
  return `${parseFloat(lat).toFixed(6)}, ${parseFloat(lng).toFixed(6)}`
}

// Función para recalcular la posición del palito cuando sea necesario
const recalcularPalitos = () => {
  // Encontrar todos los popups abiertos y recalcular sus palitos
  setTimeout(() => {
    const popupsAbiertos = document.querySelectorAll('.leaflet-popup-content .modern-marker-popup')
    if (popupsAbiertos.length > 0) {
      // Encontrar el marcador asociado a este popup
      markers.forEach(marker => {
        if (marker.isPopupOpen && marker.isPopupOpen()) {
          conectarPalitoConCirculo(marker, marker.getPopup())
        }
      })
    }
  }, 100) // Pequeño delay para asegurar que las posiciones se hayan actualizado
}

// Función para calcular y conectar el palito dinámicamente con el centro del círculo
const conectarPalitoConCirculo = (marker, popup) => {
  // Esperar a que el popup esté completamente renderizado
  setTimeout(() => {
    const popupElement = popup.getElement()
    const markerElement = marker.getElement()
    
    if (!popupElement || !markerElement) return
    
    const popupContent = popupElement.querySelector('.modern-marker-popup')
    const circleElement = markerElement.querySelector('.location-marker')
    
    if (!popupContent || !circleElement) return
    
    try {
      // Obtener las posiciones exactas relativas al viewport
      const popupRect = popupContent.getBoundingClientRect()
      const circleRect = circleElement.getBoundingClientRect()
      
      // Calcular el centro exacto del círculo
      const circleCenterX = circleRect.left + (circleRect.width / 2)
      const circleCenterY = circleRect.top + (circleRect.height / 2)
      
      // Calcular el centro del popup
      const popupCenterX = popupRect.left + (popupRect.width / 2)
      const popupBottomY = popupRect.bottom
      
      // Calcular desplazamiento horizontal para centrar el palito con el círculo
      const offsetX = circleCenterX - popupCenterX
      
      // Calcular la distancia exacta vertical
      const distanciaVertical = Math.abs(circleCenterY - popupBottomY)
      
      // Asegurar una altura mínima visible
      const palitoHeight = Math.max(distanciaVertical - 2, 15) // Mínimo 15px, menos 2px de ajuste
      
      // Obtener el tipo de popup para el color correcto
      const popupClasses = popupContent.className
      let colorPalito = '#FF9800' // Naranja por defecto
      let shadowColor = 'rgba(255, 152, 0, 0.5)'
      
      if (popupClasses.includes('entrada-popup')) {
        colorPalito = '#32CD32'
        shadowColor = 'rgba(50, 205, 50, 0.5)'
      } else if (popupClasses.includes('salida-popup')) {
        colorPalito = '#DC2626'
        shadowColor = 'rgba(220, 38, 38, 0.5)'
      } else if (popupClasses.includes('registro-hoy-popup')) {
        colorPalito = '#1E3A8A'
        shadowColor = 'rgba(30, 58, 138, 0.5)'
      }
      
      // Crear o actualizar el estilo dinámico del palito
      let styleElement = document.getElementById('dynamic-palito-style')
      if (!styleElement) {
        styleElement = document.createElement('style')
        styleElement.id = 'dynamic-palito-style'
        document.head.appendChild(styleElement)
      }
      
      // CSS dinámico para este popup específico - centrado exactamente con el círculo
      styleElement.textContent = `
        .modern-marker-popup::after {
          content: "" !important;
          display: block !important;
          position: absolute !important;
          left: calc(50% + ${offsetX}px) !important;
          bottom: -${palitoHeight}px !important;
          transform: translateX(-50%) !important;
          width: 3px !important;
          height: ${palitoHeight}px !important;
          background: ${colorPalito} !important;
          border-radius: 1.5px !important;
          box-shadow: 0 0 10px ${shadowColor}, 0 0 0 1px rgba(255, 255, 255, 0.4) !important;
          z-index: 10000 !important;
          pointer-events: none !important;
          opacity: 1 !important;
        }
        
        /* Círculo pequeño al final del palito - en el centro exacto del marcador */
        .modern-marker-popup::before {
          content: "" !important;
          display: block !important;
          position: absolute !important;
          left: calc(50% + ${offsetX}px) !important;
          bottom: -${palitoHeight + 8}px !important;
          transform: translateX(-50%) !important;
          width: 8px !important;
          height: 8px !important;
          background: ${colorPalito} !important;
          border-radius: 50% !important;
          border: 2px solid rgba(255, 255, 255, 0.8) !important;
          box-shadow: 0 0 15px ${shadowColor}, 0 0 0 1px rgba(255, 255, 255, 0.3) !important;
          z-index: 10001 !important;
          pointer-events: none !important;
          opacity: 1 !important;
        }
        
        /* Asegurar que el palito y círculo sean visibles en responsive */
        @media (max-width: 768px) {
          .modern-marker-popup::after {
            width: 2.5px !important;
            height: ${Math.max(palitoHeight * 0.85, 12)}px !important;
            bottom: -${Math.max(palitoHeight * 0.85, 12)}px !important;
            left: calc(50% + ${offsetX * 0.9}px) !important;
          }
          
          .modern-marker-popup::before {
            width: 6px !important;
            height: 6px !important;
            bottom: -${Math.max(palitoHeight * 0.85, 12) + 7}px !important;
            left: calc(50% + ${offsetX * 0.9}px) !important;
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
          }
        }
        
        @media (max-width: 480px) {
          .modern-marker-popup::after {
            width: 2px !important;
            height: ${Math.max(palitoHeight * 0.7, 10)}px !important;
            bottom: -${Math.max(palitoHeight * 0.7, 10)}px !important;
            left: calc(50% + ${offsetX * 0.8}px) !important;
          }
          
          .modern-marker-popup::before {
            width: 5px !important;
            height: 5px !important;
            bottom: -${Math.max(palitoHeight * 0.7, 10) + 6}px !important;
            left: calc(50% + ${offsetX * 0.8}px) !important;
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
          }
        }
      `
      
      console.log(`Palito + círculo conectados - Altura: ${palitoHeight}px, OffsetX: ${offsetX}px, Color: ${colorPalito}`)
      
    } catch (error) {
      console.error('Error al calcular posición del palito:', error)
    }
  }, 200) // Aumentado el delay para mejor precisión
}

// Cargar registros y asistencias desde la API
const cargarRegistros = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const token = localStorage.getItem('admin_token')
    
    // Cargar registros, asistencias y usuarios en paralelo
    const [responseRegistros, asistenciasData, usuariosData] = await Promise.all([
      axios.get(`${API_URL}/registros`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }),
      asistenciasService.obtenerAsistenciasConUsuarios(),
      usuariosService.obtenerUsuarios()
    ])
    
    // La respuesta puede ser directamente un array o tener una propiedad específica
    const registrosRaw = Array.isArray(responseRegistros.data) ? responseRegistros.data : (responseRegistros.data.registros || [])
    
    // Enriquecer registros con información de usuarios
    const registrosEnriquecidos = await usuariosService.enriquecerRegistrosConUsuarios(registrosRaw)
    
    // Guardar datos
    registros.value = registrosEnriquecidos
    asistencias.value = asistenciasData
    usuarios.value = usuariosData
    
    // Calcular estadísticas
    await calcularEstadisticas()
    
    // Obtener las últimas actividades por usuario (combinando registros y asistencias)
    const ultimasActividadesData = obtenerUltimasActividadesPorUsuario(registrosEnriquecidos, asistenciasData)
    
    // Guardar las últimas actividades para búsqueda
    ultimasActividades.value = ultimasActividadesData
    
    if (mapInitialized.value) {
      actualizarMarcadores(ultimasActividadesData)
    } else {
      inicializarMapa(ultimasActividadesData)
    }
    
  } catch (err) {
    console.error('Error al cargar registros:', err)
    if (err.response?.status === 401) {
      logout()
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
    // Usar el servicio de estadísticas con fallback automático
    const estadisticasReales = await estadisticasService.obtenerEstadisticasConFallback(
      registros.value,
      usuarios.value,
      asistencias.value
    )
    
    // Aplicar las estadísticas obtenidas (solo las 4 que queremos mostrar)
    stats.totalUsuarios = estadisticasReales.totalUsuarios
    stats.registrosHoy = estadisticasReales.registrosHoy
    stats.asistenciasHoy = estadisticasReales.asistenciasHoy
    stats.usuariosPresentes = estadisticasReales.usuariosPresentes
    
    console.log('✅ Estadísticas aplicadas en Visor:', {
      totalUsuarios: stats.totalUsuarios,
      registrosHoy: stats.registrosHoy,
      asistenciasHoy: stats.asistenciasHoy,
      usuariosPresentes: stats.usuariosPresentes
    })
    
  } catch (error) {
    console.error('❌ Error obteniendo estadísticas en Visor:', error)
    
    // Si hay error del token, hacer logout
    if (error.message === 'TOKEN_EXPIRED') {
      logout()
      return
    }
    
    // Como último recurso, usar valores por defecto
    stats.totalUsuarios = '-'
    stats.registrosHoy = '-'
    stats.asistenciasHoy = '-'
    stats.usuariosPresentes = '-'
  }
}

// Función para obtener las últimas actividades por usuario (combinando registros y asistencias)
const obtenerUltimasActividadesPorUsuario = (registros, asistencias) => {
  const mapaUsuarios = new Map()
  
  // Procesar registros normales
  registros.forEach(registro => {
    const usuarioId = registro.usuario_id
    const fechaHora = new Date(registro.fecha_hora)
    
    const actividad = {
      ...registro,
      tipo_actividad: 'registro',
      fecha_actividad: fechaHora,
      latitud: registro.latitud,
      longitud: registro.longitud
    }
    
    if (!mapaUsuarios.has(usuarioId) || 
        fechaHora > mapaUsuarios.get(usuarioId).fecha_actividad) {
      mapaUsuarios.set(usuarioId, actividad)
    }
  })
  
  // Procesar asistencias (entrada y salida)
  asistencias.forEach(asistencia => {
    const usuarioId = asistencia.usuario_id
    
    // Procesar entrada si existe
    if (asistencia.hora_entrada && asistencia.latitud_entrada && asistencia.longitud_entrada) {
      const fechaEntrada = new Date(asistencia.hora_entrada)
      
      const actividadEntrada = {
        id: `entrada_${asistencia.id}`,
        usuario_id: usuarioId,
        usuario: {
          nombre_completo: asistencia.nombre_usuario,
          correo: asistencia.correo_usuario,
          cargo: asistencia.cargo_usuario
        },
        tipo_actividad: 'entrada',
        fecha_actividad: fechaEntrada,
        fecha_hora: asistencia.hora_entrada,
        latitud: asistencia.latitud_entrada,
        longitud: asistencia.longitud_entrada,
        foto_url: asistencia.foto_entrada_url,
        descripcion: asistencia.descripcion_entrada || 'Entrada registrada'
      }
      
      if (!mapaUsuarios.has(usuarioId) || 
          fechaEntrada > mapaUsuarios.get(usuarioId).fecha_actividad) {
        mapaUsuarios.set(usuarioId, actividadEntrada)
      }
    }
    
    // Procesar salida si existe
    if (asistencia.hora_salida && asistencia.latitud_salida && asistencia.longitud_salida) {
      const fechaSalida = new Date(asistencia.hora_salida)
      
      const actividadSalida = {
        id: `salida_${asistencia.id}`,
        usuario_id: usuarioId,
        usuario: {
          nombre_completo: asistencia.nombre_usuario,
          correo: asistencia.correo_usuario,
          cargo: asistencia.cargo_usuario
        },
        tipo_actividad: 'salida',
        fecha_actividad: fechaSalida,
        fecha_hora: asistencia.hora_salida,
        latitud: asistencia.latitud_salida,
        longitud: asistencia.longitud_salida,
        foto_url: asistencia.foto_salida_url,
        descripcion: asistencia.descripcion_salida || 'Salida registrada'
      }
      
      if (!mapaUsuarios.has(usuarioId) || 
          fechaSalida > mapaUsuarios.get(usuarioId).fecha_actividad) {
        mapaUsuarios.set(usuarioId, actividadSalida)
      }
    }
  })
  
  // Convertir el mapa de vuelta a un array
  return Array.from(mapaUsuarios.values())
}

// Función para obtener las últimas ubicaciones por usuario (método anterior para compatibilidad)
const obtenerUltimasUbicacionesPorUsuario = (registros) => {
  // Agrupar por usuario_id y obtener el más reciente según fecha_hora
  const mapaUsuarios = new Map()
  
  registros.forEach(registro => {
    const usuarioId = registro.usuario_id
    const fechaHora = new Date(registro.fecha_hora)
    
    if (!mapaUsuarios.has(usuarioId) || 
        fechaHora > new Date(mapaUsuarios.get(usuarioId).fecha_hora)) {
      mapaUsuarios.set(usuarioId, registro)
    }
  })
  
  // Convertir el mapa de vuelta a un array
  return Array.from(mapaUsuarios.values())
}

// Inicializar el mapa
const inicializarMapa = (ultimasUbicaciones = null) => {
  if (mapInitialized.value) return
  
  // Asegurarse de que Leaflet está disponible
  if (!window.L) {
    return cargarLeaflet()
  }
  
  const mapContainer = document.getElementById('mapa-principal')
  if (!mapContainer) return
  
  try {
    // Inicializar mapa
    map = window.L.map('mapa-principal').setView([0, 0], 2)
    
    // Agregar capa de mapa base
    window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(map)
    
    // Crear capa para los marcadores
    markersLayer = window.L.layerGroup().addTo(map)
    
    // Agregar listeners para recalcular palitos cuando sea necesario
    map.on('moveend', recalcularPalitos)
    map.on('zoomend', recalcularPalitos)
    window.addEventListener('resize', recalcularPalitos)
    
    // Agregar controles adicionales
    window.L.control.scale({
      imperial: false,
      position: 'bottomleft'
    }).addTo(map)
    
    // Personalizar íconos de marcadores
    if (ultimasUbicaciones) {
      actualizarMarcadores(ultimasUbicaciones)
    } else {
      // Si no hay ubicaciones pasadas, obtener las últimas
      const ultimasUbicacionesPorUsuario = obtenerUltimasUbicacionesPorUsuario(registros.value)
      actualizarMarcadores(ultimasUbicacionesPorUsuario)
    }
    
    mapInitialized.value = true
    
    // Ajustar vista para mostrar todos los marcadores
    if (markers.length > 0) {
      const group = new window.L.featureGroup(markers)
      map.fitBounds(group.getBounds().pad(0.1))
    } else {
      // Coordenadas por defecto (centrado en algún lugar de interés)
      map.setView([19.4326, -99.1332], 5) // Centrado en México como ejemplo
    }
    
  } catch (error) {
    console.error('Error al inicializar el mapa:', error)
    error.value = 'No se pudo cargar el mapa. Por favor, actualice la página.'
  }
}

// Cargar la biblioteca Leaflet si no está disponible
const cargarLeaflet = () => {
  return new Promise((resolve) => {
    if (window.L) return resolve()
    
    // Cargar Animate.css para mejores animaciones
    const animateLink = document.createElement('link')
    animateLink.rel = 'stylesheet'
    animateLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css'
    document.head.appendChild(animateLink)
    
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
    document.head.appendChild(link)
    
    const script = document.createElement('script')
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
    script.onload = () => {
      console.log('Leaflet y Animate.css cargados exitosamente')
      inicializarMapa()
      resolve()
    }
    document.head.appendChild(script)
  })
}

// Actualizar marcadores en el mapa - SUPER OPTIMIZADO PARA RENDIMIENTO
// - Tamaño de marcadores muy pequeño: 12x12 px (desde 32x32 original)
// - Eliminadas animaciones costosas (pulse-ring, pulsate, etc.)
// - Animaciones de selección/enfoque más rápidas y eficientes
// - Mantiene toda la funcionalidad y diseño visual
// - Marcadores discretos pero completamente funcionales
const actualizarMarcadores = (ubicacionesAMostrar = null) => {
  if (!map || !markersLayer) return
  
  // Limpiar marcadores existentes
  markersLayer.clearLayers()
  markers = []
  
  // Determinar qué registros mostrar
  let registrosFiltrados
  
  if (ubicacionesAMostrar) {
    // Si se pasan específicamente las ubicaciones a mostrar, usar esas
    registrosFiltrados = ubicacionesAMostrar
  } else {
    // En caso contrario, filtrar los registros según criterios
    // y luego obtener las últimas actividades por usuario
    const registrosFiltradosBase = filtrarRegistros()
    registrosFiltrados = obtenerUltimasActividadesPorUsuario(registrosFiltradosBase, asistencias.value)
  }
  
  // Crear nuevos marcadores
  registrosFiltrados.forEach(registro => {
    try {
      const lat = parseFloat(registro.latitud)
      const lng = parseFloat(registro.longitud)
      
      if (isNaN(lat) || isNaN(lng)) return
      
      // Determinar el tipo de actividad y color
      const tipoActividad = determinarTipoActividad(registro)
      // Tamaño de icono reducido para mejor rendimiento con muchos puntos
      
      // Crear un HTML simple y moderno para el marcador (sin animaciones para mejor rendimiento)
      const markerHtml = `
        <div class="location-marker ${tipoActividad.clase}">
        </div>
      `
      
      // Iconos muy pequeños para mejor rendimiento y menos saturación visual
      const verySmallIconSize = [12, 12] // Reducido de [20, 20] a [12, 12]
      
      const customIcon = window.L.divIcon({
        className: 'custom-location-marker',
        html: markerHtml,
        iconSize: verySmallIconSize,
        iconAnchor: [verySmallIconSize[0] / 2, verySmallIconSize[0] / 2],
        popupAnchor: [5, -verySmallIconSize[0] / 2 - 35] // Desplazado 5px a la derecha para mejor centrado
      })

      // Crear marcador y popup con posicionamiento mejorado
      const marker = window.L.marker([lat, lng], { icon: customIcon })        .bindPopup(`
          <div class="modern-marker-popup ${tipoActividad.clase}-popup">
            <!-- Botón de cerrar personalizado con mejor posicionamiento -->
            <button class="popup-close-btn" data-popup-close="true" title="Cerrar">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z"/>
              </svg>
            </button>
            
            <div class="popup-header">
              <div class="popup-title">
                <span class="popup-id">#${registro.id}</span>
                <h3>${tipoActividad.descripcion}</h3>
              </div>
              <div class="popup-status">
                <span class="status-badge ${tipoActividad.clase}">${tipoActividad.descripcion}</span>
              </div>
            </div>
            
            <div class="popup-content">
              <div class="user-info">
                <div class="user-avatar">
                  <span class="avatar-text">${(registro.usuario?.nombre_completo || `Usuario ${registro.usuario_id}`).charAt(0).toUpperCase()}</span>
                </div>
                <div class="user-details">
                  <div class="user-name">${registro.usuario?.nombre_completo || `Usuario ${registro.usuario_id}`}</div>
                  <div class="user-email">
                    <span class="email-icon">
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.89 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                      </svg>
                    </span>
                    <span class="email-text">${registro.usuario?.correo || registro.usuario?.email || 'correo@noregistrado.com'}</span>
                  </div>
                </div>
              </div>
              
              <div class="popup-info">
                <div class="info-item">
                  <span class="info-icon">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M9 11H7v6h2v-6zm4 0h-2v6h2v-6zm4-4v11c0 1.1-.9 2-2 2H7c-1.1 0-2-.9-2-2V7c0-1.1.9-2 2-2h1V3c0-.55.45-1 1-1s1 .45 1 1v2h6V3c0-.55.45-1 1-1s1 .45 1 1v2h1c1.1 0 2 .9 2 2z"/>
                    </svg>
                  </span>
                  <span class="info-text">${formatFecha(registro.fecha_hora)}</span>
                </div>
                <div class="info-item">
                  <span class="info-icon">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                    </svg>
                  </span>
                  <span class="info-text">${tipoActividad.descripcion} más reciente</span>
                </div>
              </div>
                <div class="popup-actions">
                <button class="modern-popup-btn popup-detail-btn enhanced-detail-btn" data-registro-id="${registro.id}">
                  <span class="btn-icon">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z"/>
                    </svg>
                  </span>
                  <span class="btn-text">Ver detalles completos</span>
                </button>
              </div>
            </div>
          </div>`, {
          maxWidth: 320,
          minWidth: 300,
          className: `modern-popup-container centered-popup ${tipoActividad.clase}-tip`,
          offset: [3, -2], // Desplazado 3px a la derecha para mejor centrado
          autoPan: true,
          autoPanPadding: [50, 50],
          keepInView: true,
          closeButton: false // Desactivar botón de cerrar por defecto para usar el personalizado
        })
        // Solo guardar referencia del marcador al hacer click (no mostrar panel aún)
      marker.on('click', () => {
        // Centrar el mapa en la ubicación seleccionada
        centrarMapaEnUbicacion(registro)
        
        // Actualizar registro seleccionado pero no mostrar panel aún
        registroSeleccionado.value = registro
        
        // Guardar referencia del popup activo
        popupActivo.value = marker
        
        // Resaltar marcador
        resaltarMarcador(registro)
      })
      
      // Añadir evento al botón "Ver detalles" dentro del popup
      marker.on('popupopen', (e) => {
        // Conectar dinámicamente el palito con el círculo - primera vez
        conectarPalitoConCirculo(marker, marker.getPopup())
        
        // Recalcular después de un tiempo para asegurar renderizado completo
        setTimeout(() => {
          conectarPalitoConCirculo(marker, marker.getPopup())
        }, 300)
        
        setTimeout(() => {
          // Botón "Ver detalles"
          const detailBtn = document.querySelector('.popup-detail-btn')
          if (detailBtn) {
            detailBtn.addEventListener('click', (e) => {
              e.preventDefault()
              e.stopPropagation()
              
              // Mostrar panel de detalles sin cerrar el popup
              mostrarPanelDetalles.value = true
              
              // Añadir clase al body en móvil para prevenir scroll
              if (window.innerWidth <= 1024) {
                document.body.classList.add('panel-open')
              }
              
              // Verificar que el registro seleccionado sea el correcto
              const registroId = detailBtn.getAttribute('data-registro-id')
              if (registroId && registroId !== registro.id.toString()) {
                // Si hay un registro diferente, actualizar
                registroSeleccionado.value = registro
              }
            })
          }
          
          // Botón de cerrar personalizado
          const closeBtn = document.querySelector('.popup-close-btn')
          if (closeBtn) {
            closeBtn.addEventListener('click', (e) => {
              e.preventDefault()
              e.stopPropagation()
              
              // Cerrar el popup
              marker.closePopup()
            })
          }
          
          // Añadir efecto de animación líquida al popup
          const popupWrapper = document.querySelector('.leaflet-popup-content-wrapper')
          if (popupWrapper) {
            popupWrapper.classList.add('liquid-entrance')
          }
        }, 100)
      })
      
      // Manejar el cierre del popup
      marker.on('popupclose', (e) => {
        // Limpiar el estilo dinámico del palito
        const styleElement = document.getElementById('dynamic-palito-style')
        if (styleElement) {
          styleElement.remove()
        }
        
        // Si el popup se cierra, también cerrar el panel de detalles
        if (mostrarPanelDetalles.value) {
          cerrarPanelDetalles()
        }
        // Limpiar resaltado del marcador
        limpiarResaltadoMarcadores()
      })
      
      marker.addTo(markersLayer)
      markers.push(marker)
      
      // Guardar referencia al marcador en el registro para facilidad de uso
      registro.marker = marker
      
    } catch (err) {
      console.error('Error al crear marcador:', err)
    }
  })
  
  // Actualizar vista del mapa si hay marcadores
  if (markers.length > 0) {
    const group = new window.L.featureGroup(markers)
    map.fitBounds(group.getBounds().pad(0.1))
  }
  
  // Actualizar contador de puntos en el mapa
  totalPuntosEnMapa.value = markers.length
  console.log(`📍 Puntos actualizados en el mapa: ${totalPuntosEnMapa.value}`)
}

// Filtrar registros según los criterios seleccionados
const filtrarRegistros = () => {
  let resultado = [...registros.value]
  
  // Filtrar por periodo primero (afecta solo a registros normales)
  if (filtroPeriodo.value !== 'all') {
    const now = new Date()
    
    if (filtroPeriodo.value === 'today') {
      // Hoy
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
      resultado = resultado.filter(r => new Date(r.fecha_hora) >= today)
    } else if (filtroPeriodo.value === 'week') {
      // Esta semana
      const weekStart = new Date(now)
      weekStart.setDate(now.getDate() - now.getDay())
      weekStart.setHours(0, 0, 0, 0)
      resultado = resultado.filter(r => new Date(r.fecha_hora) >= weekStart)
    } else if (filtroPeriodo.value === 'month') {
      // Este mes
      const monthStart = new Date(now.getFullYear(), now.getMonth(), 1)
      resultado = resultado.filter(r => new Date(r.fecha_hora) >= monthStart)
    }
  }
  
  return resultado
}

// Aplicar filtros y actualizar mapa
const aplicarFiltros = () => {
  // Si hay una búsqueda de usuario activa, mantenerla
  if (busquedaUsuario.value.trim()) {
    buscarUsuarioEnTiempoReal()
    return
  }
  
  // Si no hay búsqueda de usuario, aplicar filtros normales
  actualizarMarcadoresConFiltros()
}

// Buscar usuario en tiempo real
const buscarUsuarioEnTiempoReal = () => {
  sugerenciaSeleccionada.value = -1
  
  if (!busquedaUsuario.value.trim()) {
    usuarioEncontrado.value = null
    sugerenciasUsuarios.value = []
    mostrarSugerencias.value = false
    // Mostrar todas las actividades si no hay búsqueda
    limpiarBusquedaUsuario()
    return
  }
  
  const terminoBusqueda = busquedaUsuario.value.toLowerCase().trim()
  
  // Buscar en las últimas actividades
  const usuariosEncontrados = ultimasActividades.value.filter(actividad => {
    const nombreCompleto = actividad.usuario?.nombre_completo?.toLowerCase() || ''
    const correo = actividad.usuario?.correo?.toLowerCase() || actividad.usuario?.email?.toLowerCase() || ''
    const usuarioId = actividad.usuario_id.toString()
    
    return nombreCompleto.includes(terminoBusqueda) ||
           correo.includes(terminoBusqueda) ||
           usuarioId.includes(terminoBusqueda)
  })
  
  // Actualizar sugerencias
  sugerenciasUsuarios.value = usuariosEncontrados.slice(0, 8) // Máximo 8 sugerencias
  mostrarSugerencias.value = usuariosEncontrados.length > 0
  
  if (usuariosEncontrados.length > 0) {
    // Mostrar solo los usuarios encontrados en el mapa
    actualizarMarcadores(usuariosEncontrados)
  } else {
    usuarioEncontrado.value = null
    // Si no se encuentra nada, mostrar mapa vacío
    actualizarMarcadores([])
  }
}

// Limpiar búsqueda de usuario
const limpiarBusquedaUsuario = () => {
  usuarioEncontrado.value = null
  mostrarSugerencias.value = false
  sugerenciasUsuarios.value = []
  sugerenciaSeleccionada.value = -1
  if (timeoutSugerencias.value) {
    clearTimeout(timeoutSugerencias.value)
    timeoutSugerencias.value = null
  }
  actualizarMarcadoresConFiltros()
}

// Enfocar en el usuario seleccionado
const enfocarUsuarioSeleccionado = () => {
  if (!usuarioEncontrado.value || !map) return
  
  const lat = parseFloat(usuarioEncontrado.value.latitud)
  const lng = parseFloat(usuarioEncontrado.value.longitud)
  
  if (!isNaN(lat) && !isNaN(lng)) {
    // Centrar el mapa en la ubicación del usuario con animación suave
    map.flyTo([lat, lng], Math.max(map.getZoom(), 16), {
      animate: true,
      duration: 1.5,
      easeLinearity: 0.1
    })
    
    // Encontrar el marcador del usuario y abrirle el popup
    const usuario = usuarioEncontrado.value
    if (usuario.marker) {
      setTimeout(() => {
        usuario.marker.openPopup()
        
        // Mostrar también el panel de detalles
        registroSeleccionado.value = usuario
        mostrarPanelDetalles.value = true
        
        // Añadir animación especial al marcador - optimizada
        const markerElement = usuario.marker.getElement()
        if (markerElement) {
          const marker = markerElement.querySelector('.location-marker')
          if (marker) {
            marker.classList.add('marker-focus-bounce')
            setTimeout(() => {
              marker.classList.remove('marker-focus-bounce')
            }, 400) // Reducido de 1000ms a 400ms para mejor rendimiento
          }
        }
      }, 800)
    }
  }
}

// Funciones para manejar las sugerencias
const seleccionarUsuario = (usuario, index) => {
  if (timeoutSugerencias.value) {
    clearTimeout(timeoutSugerencias.value)
    timeoutSugerencias.value = null
  }
  
  usuarioEncontrado.value = usuario
  busquedaUsuario.value = usuario.usuario?.nombre_completo || `Usuario ${usuario.usuario_id}`
  mostrarSugerencias.value = false
  sugerenciaSeleccionada.value = -1
  
  // Enfocar en el usuario seleccionado
  setTimeout(() => {
    enfocarUsuarioSeleccionado()
  }, 100)
}

const ocultarSugerenciasConDelay = () => {
  // Delay para permitir el clic en las sugerencias
  timeoutSugerencias.value = setTimeout(() => {
    mostrarSugerencias.value = false
    sugerenciaSeleccionada.value = -1
  }, 150) // Reducido el delay para mejor UX
}

const manejarTeclasNavegacion = (event) => {
  if (!mostrarSugerencias.value || sugerenciasUsuarios.value.length === 0) return
  
  switch (event.key) {
    case 'ArrowDown':
      event.preventDefault()
      sugerenciaSeleccionada.value = Math.min(
        sugerenciaSeleccionada.value + 1,
        sugerenciasUsuarios.value.length - 1
      )
      break
    case 'ArrowUp':
      event.preventDefault()
      sugerenciaSeleccionada.value = Math.max(sugerenciaSeleccionada.value - 1, -1)
      break
    case 'Enter':
      event.preventDefault()
      if (sugerenciaSeleccionada.value >= 0) {
        seleccionarUsuario(
          sugerenciasUsuarios.value[sugerenciaSeleccionada.value],
          sugerenciaSeleccionada.value
        )
      }
      break
    case 'Escape':
      mostrarSugerencias.value = false
      sugerenciaSeleccionada.value = -1
      break
  }
}

// Función auxiliar para actualizar marcadores con filtros aplicados
const actualizarMarcadoresConFiltros = () => {
  // Aplicar filtros normales si no hay búsqueda de usuario
  const registrosFiltrados = filtrarRegistros()
  let actividadesFiltradas = obtenerUltimasActividadesPorUsuario(registrosFiltrados, asistencias.value)
  
  // Aplicar filtro por tipo de actividad
  if (filtroTipo.value) {
    actividadesFiltradas = actividadesFiltradas.filter(actividad => {
      const tipoActividad = determinarTipoActividad(actividad)
      
      switch (filtroTipo.value) {
        case 'entrada':
          return tipoActividad.tipo === 'entrada'
        case 'salida':
          return tipoActividad.tipo === 'salida'
        case 'registro-hoy':
          return tipoActividad.tipo === 'registro-hoy'
        case 'registro-antiguo':
          return tipoActividad.tipo === 'registro-antiguo'
        default:
          return true
      }
    })
  }
  
  actualizarMarcadores(actividadesFiltradas)
}

// Centrar mapa en una ubicación específica (función separada)
const centrarMapaEnUbicacion = (registro) => {
  if (!map) return
  
  const lat = parseFloat(registro.latitud)
  const lng = parseFloat(registro.longitud)
  
  if (!isNaN(lat) && !isNaN(lng)) {
    // Centrar el mapa en la ubicación con animación suave
    map.flyTo([lat, lng], Math.max(map.getZoom(), 15), {
      animate: true,
      duration: 1.2,
      easeLinearity: 0.15
    })
  }
}

// Resaltar marcador seleccionado - optimizado
const resaltarMarcador = (registro) => {
  if (!map || !markers.length) return
  
  // Limpiar resaltados previos
  limpiarResaltadoMarcadores()
  
  // Encontrar y resaltar el marcador correspondiente
  markers.forEach(m => {
    const markerElement = m.getElement()
    if (markerElement && m === registro.marker) {
      const marker = markerElement.querySelector('.location-marker')
      if (marker) {
        marker.classList.add('selected', 'pulse-selected')
        
        // Quitar animación temporal después de tiempo optimizado
        setTimeout(() => {
          marker.classList.remove('pulse-selected')
        }, 600) // Reducido de 2000ms a 600ms
      }
    }
  })
}

// Limpiar resaltado de todos los marcadores - optimizado
const limpiarResaltadoMarcadores = () => {
  if (!map || !markers.length) return
  
  markers.forEach(m => {
    const markerElement = m.getElement()
    if (markerElement) {
      const marker = markerElement.querySelector('.location-marker')
      if (marker) {
        marker.classList.remove('selected', 'pulse-selected')
        marker.classList.add('marker-unselected')
        // Limpiar la clase después de la animación más rápida
        setTimeout(() => {
          marker.classList.remove('marker-unselected')
        }, 300) // Reducido de 500ms a 300ms
      }
    }
  })
}

// Cerrar panel de detalles (función separada)
const cerrarPanelDetalles = () => {
  mostrarPanelDetalles.value = false
  
  // Remover clase del body en móvil
  if (window.innerWidth <= 1024) {
    document.body.classList.remove('panel-open')
  }
  
  // Limpiar resaltado de marcadores
  limpiarResaltadoMarcadores()
  
  // Opcional: recentrar el mapa para mostrar todos los marcadores
  if (map && markers.length > 0) {
    const group = new window.L.featureGroup(markers)
    map.fitBounds(group.getBounds().pad(0.1), {
      animate: true,
      duration: 1,
      easeLinearity: 0.2
    })
  }
}

// Mostrar detalles de un registro - función simplificada
const mostrarDetallesRegistro = (registro) => {
  registroSeleccionado.value = registro
  centrarMapaEnUbicacion(registro)
  resaltarMarcador(registro)
}

// Cerrar panel de detalles con animaciones mejoradas - función legacy para compatibilidad
const cerrarDetalles = () => {
  cerrarPanelDetalles()
}

// Centrar mapa en un registro específico con mejor posicionamiento
const centrarMapa = (registro) => {
  if (!map) return
  
  const lat = parseFloat(registro.latitud)
  const lng = parseFloat(registro.longitud)
  
  if (!isNaN(lat) && !isNaN(lng)) {
    let targetLat = lat
    let targetLng = lng
    
    // Si el panel de detalles está abierto en desktop, ajustar el centrado
    if (mostrarPanelDetalles.value && window.innerWidth > 1024) {
      const mapContainer = map.getContainer()
      const mapBounds = mapContainer.getBoundingClientRect()
      const panelWidth = 380 // Ancho del panel de detalles
      
      // Centrar en el área visible disponible (descontando el panel)
      const availableWidth = mapBounds.width - panelWidth - 40 // 40px de margen
      const centerOffset = (availableWidth / 2) - (mapBounds.width / 2)
      
      // Convertir offset a coordenadas geográficas
      const targetPoint = map.latLngToContainerPoint([lat, lng])
      const offsetPoint = window.L.point(targetPoint.x + centerOffset, targetPoint.y)
      const newCenter = map.containerPointToLatLng(offsetPoint)
      
      targetLat = newCenter.lat
      targetLng = newCenter.lng
    }
    
    map.flyTo([targetLat, targetLng], Math.max(map.getZoom(), 16), {
      animate: true,
      duration: 1.5,
      easeLinearity: 0.1
    })
    
    // Si hay un marcador asociado, abrir su popup después de la animación
    if (registro.marker) {
      setTimeout(() => {
        // Añadir animación especial al marcador - optimizada
        const markerElement = registro.marker.getElement()
        if (markerElement) {
          const marker = markerElement.querySelector('.location-marker')
          if (marker) {
            marker.classList.add('marker-focus-bounce')
            setTimeout(() => {
              marker.classList.remove('marker-focus-bounce')
            }, 400) // Reducido de 1000ms a 400ms para mejor rendimiento
          }
        }
        registro.marker.openPopup()
      }, 800)
    }
  }
}

// Ver registro completo en la página de registros
const verRegistroCompleto = (registro) => {
  // Guardar ID del registro en localStorage para recuperarlo en la página de registros
  localStorage.setItem('selected_registro_id', registro.id)
  router.push('/registros')
}

// Ver detalles completos en modal
const verDetallesCompletos = (registro) => {
  registroSeleccionado.value = registro
  modalTitle.value = `Detalles del Registro #${registro.id}`
  modalType.value = 'details'
  showModal.value = true
}

// Ver foto ampliada en modal
const verFotoAmpliada = (fotoUrl) => {
  selectedPhotoUrl.value = fotoUrl
  modalTitle.value = 'Fotografía del Registro'
  modalType.value = 'photo'
  showModal.value = true
}

// Descargar foto
const descargarFoto = async (fotoUrl, nombreArchivo, evento = null) => {
  try {
    console.log('Iniciando descarga de:', fotoUrl)
    
    // Mostrar animación de carga en el botón
    const button = evento?.target?.closest('.download-mini-btn')
    if (button) {
      button.style.pointerEvents = 'none'
      button.querySelector('.download-progress')?.classList.add('downloading')
    }

    // Obtener el token de autenticación
    const token = localStorage.getItem('admin_token')
    
    // Configurar headers para la petición
    const headers = {
      'Accept': 'image/*'
    }
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    
    const response = await fetch(fotoUrl, {
      method: 'GET',
      headers: headers
    })
    
    if (!response.ok) {
      throw new Error(`Error HTTP: ${response.status}`)
    }
    
    const blob = await response.blob()
    
    // Detectar el tipo de imagen
    const contentType = blob.type || 'image/jpeg'
    let extension = 'jpg'
    
    if (contentType.includes('png')) extension = 'png'
    else if (contentType.includes('gif')) extension = 'gif'
    else if (contentType.includes('webp')) extension = 'webp'
    else if (contentType.includes('jpeg') || contentType.includes('jpg')) extension = 'jpg'
    
    // Crear un enlace temporal para forzar la descarga
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.style.display = 'none'
    link.href = url
    link.download = `${nombreArchivo}.${extension}`
    
    // Forzar el atributo download para asegurar la descarga
    link.setAttribute('download', `${nombreArchivo}.${extension}`)
    
    // Agregar al DOM, hacer clic para descargar y remover
    document.body.appendChild(link)
    link.click()
    
    // Limpiar recursos después de un breve delay
    setTimeout(() => {
      if (document.body.contains(link)) {
        document.body.removeChild(link)
      }
      window.URL.revokeObjectURL(url)
      
      // Restaurar el botón
      if (button) {
        button.style.pointerEvents = 'auto'
        button.querySelector('.download-progress')?.classList.remove('downloading')
      }
    }, 100)
    
    console.log(`Imagen descargada exitosamente: ${nombreArchivo}.${extension}`)
    
  } catch (error) {
    console.error('Error al descargar la foto:', error)
    
    // Restaurar el botón en caso de error
    const button = evento?.target?.closest('.download-mini-btn')
    if (button) {
      button.style.pointerEvents = 'auto'
      button.querySelector('.download-progress')?.classList.remove('downloading')
    }
    
    // Método alternativo: abrir en nueva pestaña
    try {
      const link = document.createElement('a')
      link.href = fotoUrl
      link.target = '_blank'
      link.download = `${nombreArchivo}.jpg`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      console.log('Descarga iniciada usando método alternativo')
    } catch (fallbackError) {
      console.error('Error en método alternativo:', fallbackError)
      alert('No se pudo descargar la imagen. Haz clic derecho en la imagen y selecciona "Guardar imagen como..."')
    }
  }
}

// Manejar errores de carga de imagen
const onImageError = (event) => {
  console.error('Error al cargar la imagen:', event.target.src)
  event.target.style.display = 'none'
  
  // Crear un placeholder para imagen no encontrada
  const placeholder = document.createElement('div')
  placeholder.className = 'image-placeholder'
  placeholder.innerHTML = `
    <svg width="48" height="48" viewBox="0 0 24 24" fill="#ccc">
      <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H20A2,2 0 0,0 22,20V8L14,2M18,20H6V4H13V9H20V20Z"/>
    </svg>
    <p style="color: #999; font-size: 10px; margin: 4px 0 0 0;">Imagen no disponible</p>
  `
  placeholder.style.cssText = `
    display: flex; 
    flex-direction: column; 
    align-items: center; 
    justify-content: center; 
    width: 100%; 
    height: 80px; 
    background: #f5f5f5; 
    border-radius: 6px;
  `
  
  // Reemplazar la imagen con el placeholder
  event.target.parentNode.insertBefore(placeholder, event.target)
  event.target.remove()
}

// Manejar carga exitosa de imagen
const onImageLoad = (event) => {
  console.log('Imagen cargada exitosamente:', event.target.src)
  event.target.style.opacity = '1'
}

// Cerrar modal
const cerrarModal = () => {
  showModal.value = false
}

// Recargar mapa y datos
const recargarMapa = async () => {
  await cargarRegistros()
  await calcularEstadisticas()
}

// Logout
const logout = () => {
  localStorage.removeItem('admin_token')
  localStorage.removeItem('admin_user')
  router.push('/login')
}

// Función para determinar el tipo de actividad y color
const determinarTipoActividad = (actividad) => {
  if (actividad.tipo_actividad === 'entrada') {
    return {
      tipo: 'entrada',
      clase: 'entrada',
      descripcion: 'Entrada',
      color: '#32CD32' // Verde lima
    }
  } else if (actividad.tipo_actividad === 'salida') {
    return {
      tipo: 'salida',
      clase: 'salida',
      descripcion: 'Salida',
      color: '#DC2626' // Rojo
    }
  } else {
    // Es un registro normal
    const fechaRegistro = new Date(actividad.fecha_hora)
    const ahora = new Date()
    const diferenciaMilisegundos = ahora - fechaRegistro
    const diferenciaHoras = diferenciaMilisegundos / (1000 * 60 * 60)
    
    if (diferenciaHoras <= 24) {
      return {
        tipo: 'registro-hoy',
        clase: 'registro-hoy',
        descripcion: 'Registro de Hoy',
        color: '#1E3A8A' // Azul marino
      }
    } else {
      return {
        tipo: 'registro-antiguo',
        clase: 'antiguo',
        descripcion: 'Registro Anterior',
        color: '#FF9800' // Naranja
      }
    }
  }
}

// Función para determinar si una ubicación es reciente (dentro de las últimas 24 horas)
const esUbicacionReciente = (fechaStr) => {
  try {
    const fechaRegistro = new Date(fechaStr)
    const ahora = new Date()
    const diferenciaMilisegundos = ahora - fechaRegistro
    const diferenciaHoras = diferenciaMilisegundos / (1000 * 60 * 60)
    return diferenciaHoras <= 24
  } catch (e) {
    return false
  }
}

// Manejar tecla Escape para cerrar panel y limpiar búsqueda
const manejarTeclaEscape = (event) => {
  if (event.key === 'Escape') {
    if (mostrarPanelDetalles.value) {
      cerrarPanelDetalles()
    }
    if (popupActivo.value) {
      popupActivo.value.closePopup()
    }
    if (busquedaUsuario.value.trim()) {
      busquedaUsuario.value = ''
      limpiarBusquedaUsuario()
    }
  }
}

// Ciclo de vida
onMounted(() => {
  // Cargar registros y después inicializar el mapa
  cargarRegistros()
  
  // Agregar listener para tecla Escape
  document.addEventListener('keydown', manejarTeclaEscape)
  
  // Escuchar cambios de conexión
  window.addEventListener('online', () => {
    isOnline.value = true
  })
  
  window.addEventListener('offline', () => {
    isOnline.value = false
  })
})

onUnmounted(() => {
  // Limpiar listeners de redimensionamiento
  window.removeEventListener('resize', recalcularPalitos)
  
  // Limpiar estilo dinámico del palito
  const styleElement = document.getElementById('dynamic-palito-style')
  if (styleElement) {
    styleElement.remove()
  }
  
  // Limpiar mapa al salir
  if (map) {
    map.remove()
    map = null
  }
  
  // Remover listener de tecla Escape
  document.removeEventListener('keydown', manejarTeclaEscape)
  
  // Limpiar clase del body
  document.body.classList.remove('panel-open')
})

// Vigilar cambios en los filtros
watch([filtroTipo, filtroPeriodo], () => {
  if (mapInitialized.value) {
    aplicarFiltros()
  }
})
</script>

<style scoped>
/* Importación de fuentes */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');

/* Estilos principales */
.visor-container {
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, #f0f2f5 0%, #e8f5e8 100%);
  font-family: 'Inter', 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  overflow: hidden;
}

.main-content {
  flex: 1;
  margin-left: clamp(180px, 18vw, 240px);
  width: calc(100vw - clamp(180px, 18vw, 240px));
  background: transparent;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 100vh;
  padding: 0;
  box-sizing: border-box;
  position: relative;
  z-index: 1;
}

/* Header con diseño moderno y verde - MÁS DELGADO */
.page-header {
  background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
  border-bottom: none;
  padding: clamp(0.4rem, 1.2vw, 0.7rem);
  position: sticky;
  top: 0;
  z-index: 100;
  width: 100%;
  box-sizing: border-box;
  color: white;
  box-shadow: 0 4px 20px rgba(46, 204, 113, 0.15);
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
  gap: clamp(0.3rem, 1.2vw, 0.6rem);
  flex-wrap: wrap;
  width: 100%;
  position: relative;
  z-index: 2;
}

.header-main {
  display: flex;
  align-items: center;
  gap: clamp(0.3rem, 1.2vw, 0.6rem);
  flex: 1;
  min-width: 150px;
}

.header-icon {
  width: clamp(28px, 4vw, 36px);
  height: clamp(28px, 4vw, 36px);
  background: rgba(255, 255, 255, 0.15);
  border-radius: clamp(6px, 1vw, 8px);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  flex-shrink: 0;
  animation: float 3s ease-in-out infinite;
}

.header-icon svg {
  width: clamp(14px, 2.5vw, 18px);
  height: clamp(14px, 2.5vw, 18px);
  color: white;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
}

.header-text {
  flex: 1;
  min-width: 150px;
}

.header-title {
  font-size: clamp(0.9rem, 2.2vw, 1.2rem);
  font-weight: 700;
  margin: 0;
  background: linear-gradient(45deg, #ffffff 0%, #e8f5e8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  letter-spacing: -0.5px;
  line-height: 1.1;
}

.header-subtitle {
  margin: clamp(0.1rem, 0.3vw, 0.15rem) 0 0 0;
  color: rgba(255, 255, 255, 0.9);
  font-size: clamp(0.6rem, 1.2vw, 0.7rem);
  line-height: 1.2;
  font-weight: 400;
  letter-spacing: 0.1px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: clamp(0.3rem, 1vw, 0.6rem);
  flex-wrap: wrap;
  justify-content: flex-end;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: clamp(0.2rem, 0.6vw, 0.25rem);
  padding: clamp(0.2rem, 0.6vw, 0.25rem) clamp(0.4rem, 1.2vw, 0.6rem);
  border-radius: clamp(10px, 1.5vw, 12px);
  font-size: clamp(0.6rem, 1.2vw, 0.7rem);
  font-weight: 500;
  white-space: nowrap;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.connection-status.online {
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.connection-status.offline {
  background: rgba(244, 67, 54, 0.2);
  color: #fff2f0;
  box-shadow: 0 2px 8px rgba(244, 67, 54, 0.2);
}

.status-indicator {
  width: clamp(4px, 1vw, 6px);
  height: clamp(4px, 1vw, 6px);
  border-radius: 50%;
  background: currentColor;
  flex-shrink: 0;
}

.status-text {
  color: white;
  font-weight: 500;
}

/* Contador LCD estilo vidrio/cristal elegante - MÁS COMPACTO */
.lcd-counter {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.25) 0%,
    rgba(255, 255, 255, 0.10) 100%);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  padding: 6px 10px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.4),
    inset 0 -1px 0 rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.lcd-counter:hover {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.35) 0%,
    rgba(255, 255, 255, 0.15) 100%);
  box-shadow: 
    0 12px 40px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.5),
    inset 0 -1px 0 rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

.lcd-counter::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, 
    rgba(0, 255, 0, 0.05) 0%,
    transparent 30%,
    transparent 70%,
    rgba(0, 255, 0, 0.03) 100%);
  pointer-events: none;
  border-radius: 12px;
}

.lcd-counter::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, 
    transparent 40%,
    rgba(255, 255, 255, 0.1) 50%,
    transparent 60%);
  animation: glass-shimmer 4s ease-in-out infinite;
  pointer-events: none;
  border-radius: 12px;
}

@keyframes glass-shimmer {
  0%, 100% {
    opacity: 0;
    transform: translateX(-100%);
  }
  50% {
    opacity: 1;
    transform: translateX(100%);
  }
}

.lcd-display {
  position: relative;
  z-index: 2;
  text-align: center;
}

.lcd-label {
  font-family: 'Inter', 'Poppins', sans-serif;
  font-size: 6px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.85);
  text-transform: uppercase;
  letter-spacing: 0.8px;
  margin-bottom: 2px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  opacity: 0.9;
}

.lcd-number {
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 900;
  color: #ffffff;
  text-shadow: 
    0 0 8px rgba(255, 255, 255, 0.8),
    0 0 16px rgba(255, 255, 255, 0.4),
    0 1px 3px rgba(0, 0, 0, 0.3),
    0 0 4px rgba(0, 255, 65, 0.3);
  line-height: 1;
  animation: lcd-pulse 3s ease-in-out infinite alternate;
  background: linear-gradient(135deg, 
    #ffffff 0%,
    #f0f0f0 50%,
    #ffffff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: brightness(1.1);
}

@keyframes lcd-pulse {
  0% {
    text-shadow: 
      0 0 8px rgba(255, 255, 255, 0.8),
      0 0 16px rgba(255, 255, 255, 0.4),
      0 1px 3px rgba(0, 0, 0, 0.3),
      0 0 4px rgba(0, 255, 65, 0.3);
    transform: scale(1);
    filter: brightness(1.1);
  }
  100% {
    text-shadow: 
      0 0 12px rgba(255, 255, 255, 1),
      0 0 20px rgba(255, 255, 255, 0.6),
      0 1px 3px rgba(0, 0, 0, 0.4),
      0 0 8px rgba(0, 255, 65, 0.4);
    transform: scale(1.02);
    filter: brightness(1.2);
  }
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: clamp(0.25rem, 0.8vw, 0.35rem);
  padding: clamp(0.4rem, 1vw, 0.5rem) clamp(0.75rem, 2vw, 1rem);
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: clamp(6px, 1.5vw, 8px);
  font-weight: 500;
  font-size: clamp(0.65rem, 1.5vw, 0.75rem);
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  white-space: nowrap;
  backdrop-filter: blur(10px);
}

.refresh-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
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

/* Nuevo botón solo con icono - MÁS COMPACTO */
.refresh-btn-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: clamp(6px, 1.5vw, 8px);
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: clamp(6px, 1.5vw, 8px);
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
  width: clamp(32px, 6vw, 36px);
  height: clamp(32px, 6vw, 36px);
}

.refresh-btn-icon:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px) scale(1.1);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.2);
}

.refresh-btn-icon:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.refresh-btn-icon:active {
  transform: translateY(-1px) scale(1.05);
  transition: all 0.1s ease;
}

/* Animación del botón de recarga */
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
    filter: drop-shadow(0 2px 6px rgba(76,175,80,0.4));
  }
  50% { 
    transform: rotate(180deg) scale(1); 
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.2));
  }
  75% {
    transform: rotate(270deg) scale(1.1); 
    filter: drop-shadow(0 2px 6px rgba(76,175,80,0.4));
  }
  100% { 
    transform: rotate(360deg) scale(1); 
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.2));
  }
}

.title-section p {
  color: #666;
  font-size: 14px;
  margin: 0;
  font-weight: 400;
  opacity: 0.8;
}

/* Header actions */

/* Contenido principal */
.page-content {
  flex: 1;
  padding: clamp(6px, 1.5vw, 8px);
  display: flex;
  flex-direction: column;
  gap: clamp(4px, 1vw, 6px);
  overflow: visible;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  position: relative;
}

/* Barra de filtros moderna - Completamente responsiva */
.modern-filter-bar {
  position: relative;
  z-index: 500;
  animation: filterBarSlideIn 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  width: 100%;
  max-width: 100%;
  overflow: visible;
  box-sizing: border-box;
  margin-top: clamp(-2px, -0.5vw, 0px);
}

@keyframes filterBarSlideIn {
  0% {
    opacity: 0;
    transform: translateX(-30px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

.filter-group {
  display: grid;
  grid-template-columns: 1fr 1fr minmax(280px, 1fr) minmax(200px, 300px);
  grid-template-areas: "filter1 filter2 search legend";
  gap: clamp(6px, 1vw, 8px);
  background: linear-gradient(135deg, #f0fff4 0%, #e8f5e8 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border: 1px solid #4CAF50;
  border-radius: clamp(8px, 1.5vw, 10px);
  padding: clamp(6px, 1.2vw, 10px);
  box-shadow: 
    0 6px 24px rgba(76, 175, 80, 0.12),
    0 2px 8px rgba(76, 175, 80, 0.08);
  position: relative;
  overflow: visible;
  width: 100%;
  box-sizing: border-box;
  align-items: center;
  transition: all 0.3s ease;
}

.filter-group:hover {
  border-color: #45a049;
  box-shadow: 
    0 8px 28px rgba(76, 175, 80, 0.15),
    0 3px 12px rgba(76, 175, 80, 0.1);
  transform: translateY(-0.5px);
}

/* Layout responsivo con breakpoints específicos */
@media (max-width: 1400px) {
  .filter-group {
    grid-template-columns: 1fr 1fr minmax(250px, 1fr) minmax(180px, 280px);
    gap: clamp(5px, 1vw, 8px);
  }
}

@media (max-width: 1200px) {
  .filter-group {
    grid-template-columns: 1fr 1fr;
    grid-template-areas: 
      "filter1 filter2"
      "search search"
      "legend legend";
    gap: clamp(6px, 1.2vw, 8px);
    padding: clamp(8px, 1.8vw, 12px);
  }
}

@media (max-width: 900px) {
  .filter-group {
    grid-template-columns: 1fr;
    grid-template-areas: 
      "search"
      "filter1"
      "filter2"  
      "legend";
    gap: clamp(6px, 1.5vw, 10px);
  }
}

@media (max-width: 480px) {
  .filter-group {
    padding: clamp(6px, 1.5vw, 8px);
    gap: clamp(6px, 1.5vw, 8px);
  }
}

.filter-group::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(76, 175, 80, 0.3), transparent);
}

.filter-item {
  display: flex;
  align-items: center;
  gap: clamp(4px, 0.8vw, 6px);
  position: relative;
  min-width: 0;
  box-sizing: border-box;
}

.filter-item:nth-child(1) {
  grid-area: filter1;
}

.filter-item:nth-child(2) {
  grid-area: filter2;
}

.filter-icon {
  color: #4CAF50;
  opacity: 0.8;
  transition: all 0.3s ease;
  flex-shrink: 0;
  width: clamp(12px, 1.5vw, 14px);
  height: clamp(12px, 1.5vw, 14px);
}

.filter-item:hover .filter-icon {
  opacity: 1;
  transform: scale(1.1);
}

.modern-select {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(76, 175, 80, 0.2);
  color: #2c3e50;
  font-size: clamp(11px, 1.5vw, 12px);
  font-weight: 500;
  cursor: pointer;
  padding: clamp(4px, 0.8vw, 6px) clamp(6px, 1.2vw, 8px);
  border-radius: clamp(5px, 0.8vw, 6px);
  transition: all 0.3s ease;
  outline: none;
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
}

.modern-select:hover {
  background: rgba(76, 175, 80, 0.05);
  border-color: rgba(76, 175, 80, 0.3);
}

.modern-select:focus {
  background: rgba(76, 175, 80, 0.08);
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.modern-select:hover {
  background: rgba(76, 175, 80, 0.05);
}

.modern-select:focus {
  background: rgba(76, 175, 80, 0.08);
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

/* Leyenda integrada en los filtros - Completamente responsiva y MÁS COMPACTA */
.filter-legend {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(6px, 1.2vw, 8px);
  padding: clamp(6px, 1.2vw, 8px);
  background: rgba(76, 175, 80, 0.08);
  border-radius: clamp(6px, 1.2vw, 8px);
  border: 1px solid rgba(76, 175, 80, 0.2);
  grid-area: legend;
  flex-wrap: wrap;
  box-sizing: border-box;
  width: 100%;
}

.legend-item-inline {
  display: flex;
  align-items: center;
  gap: clamp(3px, 0.8vw, 4px);
  font-size: clamp(9px, 1.2vw, 10px);
  font-weight: 500;
  color: #2c3e50;
  flex-shrink: 0;
  white-space: nowrap;
}

.legend-point-small {
  display: inline-block;
  width: clamp(8px, 1.2vw, 10px);
  height: clamp(8px, 1.2vw, 10px);
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.2);
  flex-shrink: 0;
}

.legend-text {
  font-size: clamp(10px, 1.5vw, 12px);
  font-weight: 500;
  color: #555;
  white-space: nowrap;
}

/* Ajustes específicos para diferentes tamaños de pantalla */
@media (max-width: 1200px) {
  .filter-legend {
    justify-content: space-around;
    margin-top: 0;
    gap: clamp(8px, 2vw, 12px);
  }
}

@media (max-width: 900px) {
  .filter-legend {
    gap: clamp(8px, 2vw, 12px);
  }
  
  .legend-item-inline {
    gap: clamp(4px, 1.2vw, 6px);
  }
}

@media (max-width: 600px) {
  .filter-legend {
    flex-wrap: wrap;
    gap: clamp(6px, 1.5vw, 8px);
  }
  
  .legend-item-inline {
    flex: 1 1 45%;
    justify-content: center;
    min-width: 0;
  }
}

@media (max-width: 400px) {
  .legend-text {
    font-size: clamp(8px, 1.8vw, 9px);
  }
  
  .legend-point-small {
    width: clamp(6px, 1.5vw, 8px);
    height: clamp(6px, 1.5vw, 8px);
  }
}

/* Actualización de leyenda con nuevos colores */
.legend-point-small.entrada {
  background: #32CD32; /* Verde lima para entrada */
}

.legend-point-small.salida {
  background: #DC2626; /* Rojo para salida */
}

.legend-point-small.registro-hoy {
  background: #1E3A8A; /* Azul marino para registros de hoy */
}

.legend-point-small.antiguo {
  background: #FF9800; /* Naranja para ubicaciones de días anteriores */
}

.legend-text {
  font-size: clamp(9px, 1.2vw, 10px);
  font-weight: 500;
  color: #555;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Estilos específicos para el elemento de búsqueda */
.search-item {
  position: relative !important;
  z-index: 2500 !important;
  overflow: visible !important;
  grid-area: search;
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
}

.modern-search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-radius: clamp(8px, 1.2vw, 10px);
  padding: clamp(3px, 0.6vw, 4px);
  transition: all 0.3s ease;
  width: 100%;
  overflow: visible;
  z-index: inherit;
  box-sizing: border-box;
}

.modern-search-wrapper:focus-within {
  border-color: #4CAF50;
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
  background: rgba(255, 255, 255, 0.98);
}

.search-input-icon {
  color: #4CAF50;
  margin-left: clamp(6px, 1.2vw, 8px);
  opacity: 0.7;
  flex-shrink: 0;
  width: clamp(12px, 1.5vw, 14px);
  height: clamp(12px, 1.5vw, 14px);
}

.modern-search-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: clamp(6px, 1.2vw, 8px);
  font-size: clamp(11px, 1.5vw, 12px);
  color: #2c3e50;
  outline: none;
  font-weight: 400;
  min-width: 0;
  width: 100%;
  box-sizing: border-box;
}

.modern-search-input::placeholder {
  color: #999;
  font-weight: 400;
}

.modern-search-btn {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  border: none;
  border-radius: clamp(5px, 0.8vw, 6px);
  width: clamp(28px, 4vw, 32px);
  height: clamp(28px, 4vw, 32px);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
  flex-shrink: 0;
  margin-right: clamp(2px, 0.4vw, 3px);
}

.modern-search-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.4);
}

.modern-search-btn:active {
  transform: scale(0.95);
}

.modern-search-btn:disabled {
  background: linear-gradient(135deg, #bdc3c7 0%, #95a5a6 100%);
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 2px 8px rgba(149, 165, 166, 0.3);
  opacity: 0.6;
}

.modern-search-btn:disabled:hover {
  transform: none;
  box-shadow: 0 2px 8px rgba(149, 165, 166, 0.3);
}

/* Indicador de usuario encontrado */
.user-found-indicator {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 4px;
  box-shadow: 0 2px 8px rgba(39, 174, 96, 0.3);
  animation: slideDownFade 0.3s ease-out;
  z-index: 10;
}

@keyframes slideDownFade {
  0% {
    opacity: 0;
    transform: translateY(-10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.user-found-indicator svg {
  flex-shrink: 0;
}

/* Dropdown de sugerencias */
.suggestions-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e1e8ed;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  margin-top: 8px;
  z-index: 9999 !important;
  max-height: 320px;
  overflow: hidden;
  animation: dropdownSlide 0.2s ease-out;
}

@keyframes dropdownSlide {
  0% {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.suggestions-header {
  padding: 8px 12px;
  background: #f7f9fa;
  border-bottom: 1px solid #e1e8ed;
  font-size: 11px;
  color: #657786;
  font-weight: 500;
}

.suggestions-count {
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.suggestions-list {
  max-height: 280px;
  overflow-y: auto;
}

.suggestion-item {
  display: flex;
  align-items: center;
  padding: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom: 1px solid #f7f9fa;
  gap: 12px;
}

.suggestion-item:hover,
.suggestion-selected {
  background: #f0f8ff;
  border-color: #e3f2fd;
}

.suggestion-item:last-child {
  border-bottom: none;
}

.suggestion-avatar {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.avatar-letter {
  font-size: 14px;
  font-weight: 600;
  color: white;
  text-transform: uppercase;
}

.avatar-letter.entrada {
  background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
}

.avatar-letter.salida {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
}

.avatar-letter.registro-hoy {
  background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
}

.avatar-letter.registro-anterior {
  background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
}

.suggestion-info {
  flex: 1;
  min-width: 0;
}

.suggestion-name {
  font-size: 13px;
  font-weight: 600;
  color: #14171a;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.suggestion-details {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.suggestion-email {
  font-size: 11px;
  color: #657786;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 150px;
}

.suggestion-status {
  font-size: 10px;
  font-weight: 500;
  padding: 2px 6px;
  border-radius: 10px;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.suggestion-status.entrada {
  background: rgba(39, 174, 96, 0.1);
  color: #27ae60;
}

.suggestion-status.salida {
  background: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
}

.suggestion-status.registro-hoy {
  background: rgba(30, 58, 138, 0.1);
  color: #1e3a8a;
}

.suggestion-status.registro-anterior {
  background: rgba(243, 156, 18, 0.1);
  color: #f39c12;
}

/* Mapa principal - Completamente responsivo */
.visor-section {
  position: relative;
  flex: 1;
  background: white;
  border-radius: clamp(12px, 2vw, 16px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  width: 100%;
  min-height: 0;
  box-sizing: border-box;
}

.loading-container, .error-container {
  padding: clamp(40px, 8vw, 60px) clamp(20px, 4vw, 40px);
  text-align: center;
  background: white;
  border-radius: clamp(8px, 1.5vw, 12px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: clamp(200px, 30vh, 300px);
}

.spinner-large {
  width: clamp(32px, 6vw, 40px);
  height: clamp(32px, 6vw, 40px);
  border: 4px solid #e0e0e0;
  border-top: 4px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite, pulse 2s ease-in-out infinite;
  margin: 0 auto clamp(16px, 3vw, 20px);
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.retry-btn {
  padding: clamp(10px, 2vw, 12px) clamp(16px, 3vw, 20px);
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  color: white;
  border: none;
  border-radius: clamp(6px, 1vw, 8px);
  cursor: pointer;
  margin-top: clamp(12px, 2.5vw, 16px);
  font-weight: 500;
  font-size: clamp(12px, 2vw, 14px);
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
}

.retry-btn:active {
  transform: translateY(0);
}

.mapa-container {
  flex: 1;
  width: 100%;
  height: 100%;
  min-height: clamp(250px, 45vh, 400px);
  max-height: none;
  z-index: 10;
  position: relative;
  pointer-events: auto;
  border-radius: 0;
  overflow: hidden;
  box-sizing: border-box;
}

/* Responsividad específica para diferentes dispositivos */
@media (max-width: 1024px) and (orientation: landscape) {
  .mapa-container {
    min-height: clamp(200px, 50vh, 350px);
  }
}

@media (max-width: 768px) {
  .visor-section {
    border-radius: clamp(8px, 2vw, 12px);
  }
  
  .mapa-container {
    min-height: clamp(250px, 40vh, 350px);
  }
}

@media (max-width: 480px) {
  .mapa-container {
    min-height: clamp(200px, 35vh, 300px);
  }
}

/* Para tablets en modo portrait */
@media (max-width: 1024px) and (orientation: portrait) {
  .mapa-container {
    min-height: clamp(300px, 50vh, 500px);
  }
}

/* Asegurar navegabilidad del mapa en todas las condiciones */
:global(.leaflet-container) {
  pointer-events: auto !important;
}

:global(.leaflet-control-zoom) {
  pointer-events: auto !important;
  z-index: 1000 !important;
}

:global(.leaflet-control-attribution) {
  pointer-events: auto !important;
  z-index: 1000 !important;
}

/* Leyenda del mapa - REMOVIDA: Ahora está integrada en los filtros */
/* 
.map-legend {
  position: absolute;
  bottom: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.9);
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  z-index: 500;
  max-width: 200px;
}

.map-legend h3 {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #2c3e50;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 12px;
}

.legend-point {
  display: inline-block;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.2);
}

.legend-point.reciente {
  background: #4CAF50;
}

.legend-point.antiguo {
  background: #FF9800;
}
*/

/* Panel de información del registro seleccionado - Versión compacta dentro del mapa */
.registro-info-panel {
  position: absolute;
  top: 10px;
  right: -280px;
  width: clamp(240px, 28vw, 280px);
  max-width: calc(100vw - 40px);
  max-height: calc(100vh - 140px);
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  z-index: 1100;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  border: 1px solid rgba(255, 255, 255, 0.2);
  pointer-events: auto;
}

.registro-info-panel.panel-visible {
  right: 10px;
  animation: slideInFromRight 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* Bordes superiores con colores según el tipo de actividad */
.registro-info-panel.panel-entrada {
  border-top: 4px solid #32CD32; /* Verde lima para entrada */
}

.registro-info-panel.panel-salida {
  border-top: 4px solid #DC2626; /* Rojo para salida */
}

.registro-info-panel.panel-registro-hoy {
  border-top: 4px solid #1E3A8A; /* Azul marino para registros de hoy */
}

.registro-info-panel.panel-old {
  border-top: 4px solid #FF9800; /* Naranja para registros antiguos */
}

@keyframes slideInFromRight {
  0% {
    transform: translateX(100%) scale(0.95);
    opacity: 0;
    filter: blur(5px);
  }
  40% {
    transform: translateX(-10px) scale(1.02);
    opacity: 0.8;
    filter: blur(2px);
  }
  100% {
    transform: translateX(0) scale(1);
    opacity: 1;
    filter: blur(0);
  }
}

.panel-header {
  padding: 8px 12px;
  background: linear-gradient(135deg, #1E3A8A 0%, #1e40af 100%); /* Azul marino por defecto */
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 5;
  gap: 8px;
}

.panel-entrada .panel-header {
  background: linear-gradient(135deg, #32CD32 0%, #28a745 100%); /* Verde lima para entrada */
}

.panel-salida .panel-header {
  background: linear-gradient(135deg, #DC2626 0%, #b91c1c 100%); /* Rojo para salida */
}

.panel-registro-hoy .panel-header {
  background: linear-gradient(135deg, #1E3A8A 0%, #1e40af 100%); /* Azul marino para registros de hoy */
}

.panel-old .panel-header {
  background: linear-gradient(135deg, #FF9800 0%, #f57c00 100%); /* Naranja para registros antiguos */
}

.panel-title-section {
  flex: 1;
  min-width: 0;
}

.panel-title-section h3 {
  margin: 0 0 2px 0;
  font-size: 13px;
  font-weight: 600;
  line-height: 1.2;
}

.panel-id {
  font-size: 9px;
  opacity: 0.85;
  font-weight: 500;
  letter-spacing: 0.3px;
}

.close-panel-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  backdrop-filter: blur(10px);
}

.close-panel-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.panel-content {
  padding: 0;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
  padding-bottom: 12px;
}

/* Sección de usuario */
.user-section {
  padding: 8px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-avatar-large {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.panel-old .user-avatar-large {
  background: linear-gradient(135deg, #FF9800 0%, #f57c00 100%);
}

.avatar-text-large {
  font-size: 11px;
  font-weight: 700;
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.user-info-detail {
  flex: 1;
  min-width: 0;
}

.user-name-large {
  margin: 0 0 2px 0;
  font-size: 11px;
  font-weight: 600;
  color: #2c3e50;
  line-height: 1.2;
}

.user-email-large {
  margin: 0;
  font-size: 9px;
  color: #6c757d;
  word-break: break-word;
  line-height: 1.2;
}

/* Sección de información */
.info-section {
  padding: 10px;
  margin-top: 2px;
  margin-bottom: 8px;
}

.section-title {
  margin: 0 0 6px 0;
  font-size: 10px;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 2px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-item-detail {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  margin-bottom: 6px;
  padding: 4px;
  background: #f8f9fa;
  border-radius: 4px;
  border-left: 2px solid #4CAF50;
}

.panel-old .info-item-detail {
  border-left-color: #FF9800;
}

.info-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
  background: #4CAF50;
  border-radius: 50%;
  color: white;
  flex-shrink: 0;
}

.panel-old .info-icon-wrapper {
  background: #FF9800;
}

.info-text-wrapper {
  flex: 1;
  min-width: 0;
}

.info-label {
  display: block;
  font-size: 8px;
  font-weight: 600;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.2px;
  margin-bottom: 1px;
}

.info-value {
  display: block;
  font-size: 9px;
  color: #2c3e50;
  font-weight: 500;
  line-height: 1.2;
}

.status-badge-large {
  display: inline-block;
  padding: 1px 4px;
  border-radius: 8px;
  font-size: 7px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.2px;
}

.status-badge-large.entrada {
  background: #32CD32;
  color: white;
}

.status-badge-large.salida {
  background: #DC2626;
  color: white;
}

.status-badge-large.registro-hoy {
  background: #1E3A8A;
  color: white;
}

.status-badge-large.antiguo {
  background: #FF9800;
  color: white;
}
/* Sección de foto */
.photo-section {
  padding: 8px;
  border-top: 1px solid #dee2e6;
  margin-bottom: 8px;
}

.photo-container {
  position: relative;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s;
}

.photo-container:hover {
  transform: scale(1.02);
}

.registro-photo {
  width: 100%;
  height: auto;
  max-height: 80px;
  object-fit: cover;
  display: block;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.registro-photo[src] {
  opacity: 1;
}

/* Placeholder para imágenes no disponibles */
.image-placeholder {
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  width: 100% !important;
  height: 80px !important;
  background: #f5f5f5 !important;
  border-radius: 6px !important;
  border: 1px dashed #ddd !important;
}

.photo-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.photo-container:hover .photo-overlay {
  opacity: 1;
}

/* Mini botón de descarga animado */
.download-mini-btn {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 20px;
  height: 20px;
  background: rgba(76, 175, 80, 0.9);
  border: none;
  border-radius: 50%;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
  z-index: 10;
  opacity: 0;
  transform: scale(0.8);
}

.photo-container:hover .download-mini-btn {
  opacity: 1;
  transform: scale(1);
  animation: downloadAppear 0.3s ease-out;
}

@keyframes downloadAppear {
  0% {
    opacity: 0;
    transform: scale(0.5) rotate(-180deg);
  }
  60% {
    transform: scale(1.2) rotate(-10deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

.download-mini-btn:hover {
  background: rgba(76, 175, 80, 1);
  transform: scale(1.1);
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.4);
}

.download-mini-btn:active {
  transform: scale(0.95);
}

.download-icon {
  transition: transform 0.2s ease;
}

.download-mini-btn:hover .download-icon {
  transform: translateY(-1px);
  animation: downloadBounce 0.6s ease-in-out;
}

@keyframes downloadBounce {
  0%, 100% { transform: translateY(0); }
  25% { transform: translateY(-2px); }
  50% { transform: translateY(1px); }
  75% { transform: translateY(-1px); }
}

.download-progress {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid transparent;
  opacity: 0;
  transition: opacity 0.2s;
}

.download-progress.downloading {
  opacity: 1;
  border-color: rgba(255, 255, 255, 0.6);
  animation: downloadSpin 1s linear infinite;
}

.download-mini-btn:active .download-progress {
  opacity: 1;
  border-color: rgba(255, 255, 255, 0.6);
  animation: downloadSpin 0.8s linear;
}

@keyframes downloadSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Modal para foto ampliada y detalles completos */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2100; /* Z-index más alto que el popup */
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 90%;
  width: auto;
  max-height: 90vh;
  overflow-y: auto;
  margin: 20px;
  animation: slideInUp 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

/* Modal para detalles completos - más ancho */
.modal-content.details {
  width: 800px;
  max-width: 95%;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e0e0e0;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 16px 16px 0 0;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 20px;
  font-weight: 700;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.btn-close:hover {
  background: rgba(0, 0, 0, 0.1);
  color: #333;
}

.modal-body {
  padding: 24px;
}

.full-photo {
  max-width: 100%;
  max-height: 70vh;
  display: block;
  margin: 0 auto;
  border-radius: 8px;
}

/* Estilos para el modal de detalles completos */
.details-modal-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.modal-user-section {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  border-left: 4px solid #4CAF50;
}

.modal-user-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.modal-avatar-text {
  font-size: 24px;
  font-weight: 800;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.modal-user-info {
  flex: 1;
}

.modal-user-name {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 700;
  color: #2c3e50;
}

.modal-user-email {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #6c757d;
}

.modal-status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modal-status-badge.entrada {
  background: #32CD32;
  color: white;
}

.modal-status-badge.salida {
  background: #DC2626;
  color: white;
}

.modal-status-badge.registro-hoy {
  background: #1E3A8A;
  color: white;
}

.modal-status-badge.antiguo {
  background: #FF9800;
  color: white;
}

.modal-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.modal-info-card {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.modal-info-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.modal-info-card.full-width {
  grid-column: 1 / -1;
}

.modal-info-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  border-radius: 10px;
  color: white;
  flex-shrink: 0;
}

.modal-info-content h5 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
  color: #6c757d;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modal-info-content p {
  margin: 0;
  font-size: 16px;
  color: #2c3e50;
  font-weight: 500;
}

.modal-photo-section {
  margin-top: 8px;
}

.modal-photo-section h5 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

.modal-photo-container {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s ease;
}

.modal-photo-container:hover {
  transform: scale(1.02);
}

.modal-photo {
  width: 100%;
  height: auto;
  max-height: 300px;
  object-fit: cover;
  display: block;
}

.modal-photo-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.modal-photo-container:hover .modal-photo-overlay {
  opacity: 1;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 16px;
  border-top: 1px solid #e9ecef;
}

.modal-action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s ease;
  text-decoration: none;
}

.modal-action-btn.primary {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.modal-action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(76, 175, 80, 0.4);
}

.modal-action-btn.secondary {
  background: white;
  color: #6c757d;
  border: 1px solid #dee2e6;
}

.modal-action-btn.secondary:hover {
  background: #f8f9fa;
  color: #495057;
  transform: translateY(-1px);
}

/* Responsivo para el modal */
@media (max-width: 768px) {
  .modal-content.details {
    width: 95%;
    max-width: 95%;
    margin: 10px;
    max-height: 95vh;
  }
  
  .modal-body {
    padding: 16px;
  }
  
  .modal-info-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .modal-user-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    padding: 16px;
  }
  
  .modal-user-avatar {
    width: 50px;
    height: 50px;
    align-self: center;
  }
  
  .modal-avatar-text {
    font-size: 20px;
  }
  
  .modal-user-name {
    font-size: 18px;
    text-align: center;
    width: 100%;
  }
  
  .modal-user-email {
    text-align: center;
    width: 100%;
  }
  
  .modal-actions {
    flex-direction: column;
    gap: 8px;
  }
  
  .modal-action-btn {
    width: 100%;
    justify-content: center;
    padding: 14px 20px;
  }
  
  .modal-header {
    padding: 16px 20px;
  }
  
  .modal-header h3 {
    font-size: 18px;
  }
  
  .modal-info-card {
    padding: 12px;
  }
  
  .modal-info-icon {
    width: 36px;
    height: 36px;
  }
  
  .modal-info-content h5 {
    font-size: 12px;
  }
  
  .modal-info-content p {
    font-size: 14px;
  }
  
  .modal-photo {
    max-height: 250px;
  }
}

@media (max-width: 480px) {
  .modal-content {
    margin: 5px;
    border-radius: 12px;
  }
  
  .modal-content.details {
    width: calc(100% - 10px);
    max-width: calc(100% - 10px);
    max-height: 98vh;
  }
  
  .modal-body {
    padding: 12px;
  }
  
  .modal-header {
    padding: 12px 16px;
  }
  
  .modal-header h3 {
    font-size: 16px;
  }
  
  .btn-close {
    width: 32px;
    height: 32px;
    font-size: 20px;
  }
  
  .modal-user-section {
    padding: 12px;
    gap: 10px;
  }
  
  .modal-user-avatar {
    width: 45px;
    height: 45px;
  }
  
  .modal-avatar-text {
    font-size: 18px;
  }
  
  .modal-user-name {
    font-size: 16px;
  }
  
  .modal-user-email {
    font-size: 12px;
  }
  
  .modal-status-badge {
    padding: 4px 8px;
    font-size: 10px;
  }
  
  .modal-info-grid {
    gap: 8px;
  }
  
  .modal-info-card {
    padding: 10px;
    gap: 8px;
  }
  
  .modal-info-icon {
    width: 32px;
    height: 32px;
  }
  
  .modal-info-content h5 {
    font-size: 11px;
  }
  
  .modal-info-content p {
    font-size: 13px;
  }
  
  .modal-photo {
    max-height: 200px;
  }
  
  .modal-actions {
    padding-top: 12px;
  }
  
  .modal-action-btn {
    padding: 12px 16px;
    font-size: 12px;
  }
}

@media (max-width: 360px) {
  .modal-content.details {
    width: calc(100% - 6px);
    max-width: calc(100% - 6px);
    margin: 3px;
    max-height: 99vh;
  }
  
  .modal-body {
    padding: 10px;
  }
  
  .modal-header {
    padding: 10px 12px;
  }
  
  .modal-header h3 {
    font-size: 14px;
  }
  
  .btn-close {
    width: 28px;
    height: 28px;
    font-size: 18px;
  }
  
  .modal-user-name {
    font-size: 14px;
  }
  
  .modal-user-email {
    font-size: 11px;
  }
  
  .modal-info-content h5 {
    font-size: 10px;
  }
  
  .modal-info-content p {
    font-size: 12px;
  }
}
  
  /* Estilos responsive para sugerencias */
  .suggestions-dropdown {
    left: -10px;
    right: -10px;
    max-height: 280px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  }
  
  .suggestion-item {
    padding: 10px;
    gap: 10px;
  }
  
  .suggestion-avatar {
    width: 32px;
    height: 32px;
  }
  
  .avatar-letter {
    font-size: 12px;
  }
  
  .suggestion-name {
    font-size: 12px;
  }
  
  .suggestion-email {
    font-size: 10px;
    max-width: 120px;
  }
  
  .suggestion-status {
    font-size: 9px;
    padding: 1px 4px;
  }
  
  /* Estilos responsive para el panel compacto */
  .registro-info-panel {
    width: clamp(200px, 45vw, 240px);
    top: 5px;
    right: -240px;
    max-height: calc(100vh - 100px);
  }
  
  .registro-info-panel.panel-visible {
    right: 5px;
  }
  
  .panel-header {
    padding: 6px 8px;
  }
  
  .panel-title-section h3 {
    font-size: 11px;
  }
  
  .panel-id {
    font-size: 8px;
  }
  
  .close-panel-btn {
    width: 18px;
    height: 18px;
  }
  
  .user-section {
    padding: 6px;
    gap: 6px;
  }
  
  .user-avatar-large {
    width: 24px;
    height: 24px;
  }
  
  .avatar-text-large {
    font-size: 9px;
  }
  
  .user-name-large {
    font-size: 10px;
  }
  
  .user-email-large {
    font-size: 8px;
  }
  
  .info-section {
    padding: 6px;
  }
  
  .section-title {
    font-size: 9px;
    margin-bottom: 4px;
  }
  
  .info-item-detail {
    padding: 3px;
    gap: 4px;
    margin-bottom: 4px;
  }
  
  .info-icon-wrapper {
    width: 12px;
    height: 12px;
  }
  
  .info-label {
    font-size: 7px;
  }
  
  .info-value {
    font-size: 8px;
  }
  
  .status-badge-large {
    padding: 1px 3px;
    font-size: 6px;
  }
  
  .photo-section {
    padding: 6px;
  }
  
  .registro-photo {
    max-height: 60px;
  }
  
  .download-mini-btn {
    width: 16px;
    height: 16px;
    top: 3px;
    right: 3px;
  }

/* Estilos para marcadores personalizados - Optimizados para rendimiento */
:global(.custom-location-marker) {
  background: transparent;
  border: none;
}

/* Marcadores muy pequeños pero visibles - Optimizados para rendimiento */
:global(.location-marker) {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 1px solid white; /* Borde muy delgado para marcadores pequeños */
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.4); /* Sombra más pronunciada para mejor visibilidad */
  /* Eliminadas las animaciones para mejor rendimiento con muchos puntos */
  transition: transform 0.2s ease; /* Solo transición básica para hover/selección */
  cursor: pointer; /* Asegurar que sea clickeable */
}

:global(.location-marker.entrada) {
  background: #32CD32; /* Verde lima para entrada de asistencia */
}

:global(.location-marker.salida) {
  background: #DC2626; /* Rojo para salida de asistencia */
}

:global(.location-marker.registro-hoy) {
  background: #1E3A8A; /* Azul marino para registros del día de hoy */
}

:global(.location-marker.antiguo) {
  background: #FF9800; /* Naranja para ubicaciones de días anteriores (más de 24 horas) */
}

/* Marcador seleccionado - optimizado para tamaño muy pequeño */
:global(.location-marker.selected) {
  border: 1px solid white; /* Borde consistente pero delgado */
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.8), 0 0 6px rgba(0, 0, 0, 0.5); /* Halo más pequeño pero visible */
  transform: scale(1.5); /* Escala mayor para compensar el tamaño pequeño */
  z-index: 100;
  /* Eliminada animación infinita para mejor rendimiento */
}

/* Animación de pulso solo cuando se selecciona (no infinita) */
:global(.location-marker.pulse-selected) {
  animation: selectedPulse 0.6s ease-out; /* Solo una vez, no infinita */
}

/* Animación de pulso más corta y eficiente para marcadores pequeños */
@keyframes selectedPulse {
  0% {
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.8), 0 0 6px rgba(0, 0, 0, 0.5);
    transform: scale(1.5);
  }
  50% {
    box-shadow: 0 0 0 4px rgba(52, 152, 219, 0.6), 0 0 10px rgba(0, 0, 0, 0.6);
    transform: scale(1.7);
  }
  100% {
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.8), 0 0 6px rgba(0, 0, 0, 0.5);
    transform: scale(1.5);
  }
}

/* Animación optimizada para marcador enfocado */
@keyframes markerGlow {
  0% {
    filter: brightness(1);
  }
  100% {
    filter: brightness(1.2);
  }
}

/* Animación de deselección optimizada */
:global(.location-marker.marker-unselected) {
  animation: unselectMarker 0.3s ease-out; /* Más rápida */
}

@keyframes unselectMarker {
  0% {
    transform: scale(1.5); /* Desde escala seleccionada */
    filter: brightness(1.1);
  }
  100% {
    transform: scale(1); /* Volver a tamaño normal */
    filter: brightness(1);
  }
}

/* Animación de enfoque más rápida y eficiente para marcadores pequeños */
:global(.location-marker.marker-focus-bounce) {
  animation: focusBounce 0.4s ease-out; /* Más rápida */
}

@keyframes focusBounce {
  0% {
    transform: scale(1.5); /* Comenzar desde escala seleccionada */
  }
  60% {
    transform: scale(2.0); /* Escala mayor para compensar tamaño pequeño */
  }
  100% {
    transform: scale(1.5); /* Volver a escala seleccionada */
  }
}

/* Animaciones de pulso eliminadas para mejor rendimiento */
:global(.pulse-ring) {
  /* Eliminada la animación pulse-ring para optimización de rendimiento */
  display: none;
}

/* Animación de aparición simple y rápida */
@keyframes appearScale {
  0% {
    transform: scale(0.8);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Eliminadas animaciones costosas: pulsate, pulseMarker para mejor rendimiento */

/* Estilos mejorados para el popup moderno del marcador */
:global(.modern-popup-container .leaflet-popup-content-wrapper) {
  border-radius: 20px;
  box-shadow: none !important;
  border: none;
  padding: 0;
  overflow: visible;
  backdrop-filter: none !important;
  transform-origin: bottom center;
  z-index: 1050; /* Z-index ajustado para no interferir con la navegación del mapa */
  pointer-events: auto; /* Solo el popup captura eventos */
  background: transparent !important; /* Quitar el fondo blanco */
  -webkit-backdrop-filter: none !important;
}

/* Popup centrado - mejora del posicionamiento */
:global(.modern-popup-container.centered-popup .leaflet-popup-content-wrapper) {
  animation: liquidSplashUp 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  margin-left: auto !important;
  margin-right: auto !important;
  position: relative;
  left: 50% !important;
  transform: translateX(-50%) !important;
}

/* Animación líquida principal - efecto splash */
@keyframes liquidSplashUp {
  0% {
    opacity: 0;
    transform: translateY(30px) scale(0.3) rotateX(-15deg);
    filter: blur(10px);
    box-shadow: 0 0 0 rgba(0, 0, 0, 0);
  }
  20% {
    opacity: 0.7;
    transform: translateY(15px) scale(0.7) rotateX(-5deg);
    filter: blur(5px);
  }
  40% {
    opacity: 0.9;
    transform: translateY(-5px) scale(1.1) rotateX(2deg);
    filter: blur(2px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  }
  60% {
    opacity: 1;
    transform: translateY(-8px) scale(1.05) rotateX(0deg);
    filter: blur(0px);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
  }
  80% {
    transform: translateY(2px) scale(0.98) rotateX(0deg);
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.18);
  }
  100% {
    opacity: 1;
    transform: translateY(0px) scale(1) rotateX(0deg);
    filter: blur(0px);
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
  }
}

/* Animación de entrada líquida adicional */
:global(.modern-popup-container .leaflet-popup-content-wrapper.liquid-entrance) {
  animation: liquidSplashUp 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275), liquidRipple 1.2s ease-out 0.3s;
}

/* Efecto de ondas líquidas */
@keyframes liquidRipple {
  0% {
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
  }
  25% {
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2), 0 0 0 10px rgba(255, 255, 255, 0.1);
  }
  50% {
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2), 0 0 0 20px rgba(255, 255, 255, 0.05);
  }
  75% {
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2), 0 0 0 30px rgba(255, 255, 255, 0.02);
  }
  100% {
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
  }
}

/* Animación de cierre del popup */
:global(.modern-marker-popup.popup-closing) {
  animation: liquidSplashDown 0.3s cubic-bezier(0.55, 0.085, 0.68, 0.53) forwards;
}

@keyframes liquidSplashDown {
  0% {
    opacity: 1;
    transform: translateY(0px) scale(1);
    filter: blur(0px);
  }
  50% {
    opacity: 0.7;
    transform: translateY(10px) scale(0.9);
    filter: blur(2px);
  }
  100% {
    opacity: 0;
    transform: translateY(30px) scale(0.3);
    filter: blur(10px);
  }
}

:global(.modern-popup-container .leaflet-popup-content) {
  margin: 0;
  padding: 0;
  width: 280px !important;
  max-width: calc(100vw - 40px) !important;
  background: transparent !important; /* Quitar el fondo blanco */
  box-shadow: none !important; /* Quitar sombra por defecto */
  overflow: visible !important; /* Permitir que el palito sea visible */
}

:global(.modern-popup-container .leaflet-popup-tip) {
  display: none !important; /* Ocultar completamente el tip original de Leaflet */
  visibility: hidden !important;
  opacity: 0 !important;
  width: 0 !important;
  height: 0 !important;
}

/* Tip oculto para popup centrado */
:global(.modern-popup-container.centered-popup .leaflet-popup-tip) {
  display: none !important; /* Ocultar el tip de Leaflet */
  visibility: hidden !important;
  opacity: 0 !important;
}

/* Ocultar el contenedor del tip de Leaflet */
:global(.modern-popup-container .leaflet-popup-tip-container) {
  display: none !important; /* Ocultar completamente el contenedor del tip */
}





/* Ocultar el botón de cerrar por defecto de Leaflet ya que usamos uno personalizado */
:global(.modern-popup-container .leaflet-container a.leaflet-popup-close-button) {
  display: none !important;
}

/* Ocultar cualquier fondo blanco adicional de Leaflet */
:global(.modern-popup-container .leaflet-popup-content-wrapper::before) {
  display: none !important;
}

:global(.modern-popup-container .leaflet-popup-content-wrapper::after) {
  display: none !important;
}

/* Eliminar cualquier pseudo-elemento que pueda crear fondos */
:global(.modern-popup-container::before) {
  display: none !important;
}

:global(.modern-popup-container::after) {
  display: none !important;
}

/* Eliminar efectos de desenfoque y fondos en todos los elementos del popup */
:global(.modern-popup-container .leaflet-popup) {
  background: transparent !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  box-shadow: none !important;
}

:global(.modern-popup-container .leaflet-popup-content-wrapper) {
  background: transparent !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  box-shadow: none !important;
  border-radius: 0 !important;
  overflow: visible !important;
}

/* Asegurar que no haya bordes o fondos blancos en ningún elemento del popup */
:global(.modern-popup-container *) {
  border: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

:global(.modern-popup-container .leaflet-popup-content-wrapper) {
  background: transparent !important;
  border: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  box-shadow: none !important;
}

:global(.modern-popup-container .leaflet-popup-content) {
  background: transparent !important;
  border: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  box-shadow: none !important;
}

/* Asegurar que todos los contenedores de Leaflet permitan el overflow visible */
:global(.leaflet-popup-pane) {
  overflow: visible !important;
}

:global(.leaflet-popup) {
  overflow: visible !important;
}

:global(.modern-popup-container) {
  overflow: visible !important;
}
:global(.leaflet-map-pane) {
  z-index: 1 !important;
}

:global(.leaflet-popup-pane) {
  z-index: 1050 !important; /* Reducido para permitir navegación */
}

:global(.leaflet-tooltip-pane) {
  z-index: 1055 !important;
}

:global(.leaflet-control-container) {
  z-index: 1000 !important; /* Controles del mapa siempre accesibles */
}

/* Responsividad completa para el popup */
@media (max-width: 480px) {
  :global(.modern-popup-container .leaflet-popup-content) {
    width: 240px !important;
    max-width: calc(100vw - 20px) !important;
  }
  
  :global(.modern-popup-container.centered-popup .leaflet-popup-content-wrapper) {
    left: 50% !important;
    transform: translateX(-50%) !important;
    margin: 0 auto !important;
  }
  
  :global(.modern-marker-popup) {
    min-width: 200px;
    border-radius: 12px;
  }
  
  :global(.popup-header) {
    padding: 10px 28px 8px 12px;
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
  }
  
  :global(.popup-title) {
    width: 100%;
  }
  
  :global(.popup-title h3) {
    font-size: 13px;
  }
  
  :global(.popup-id) {
    font-size: 9px;
  }
  
  :global(.popup-status) {
    align-self: flex-end;
    margin-top: -24px;
  }
  
  :global(.status-badge) {
    padding: 2px 6px;
    font-size: 8px;
  }
  
  :global(.popup-content) {
    padding: 12px;
  }
  
  :global(.user-info) {
    gap: 8px;
    margin-bottom: 10px;
  }
  
  :global(.user-avatar) {
    width: 36px;
    height: 36px;
    border: 2px solid rgba(255, 255, 255, 0.4);
  }
  
  :global(.avatar-text) {
    font-size: 14px;
  }
  
  :global(.user-name) {
    font-size: 12px;
    line-height: 1.2;
  }
  
  :global(.user-email) {
    font-size: 9px;
    gap: 3px;
  }
  
  :global(.email-icon svg) {
    width: 8px;
    height: 8px;
  }
  
  :global(.popup-info) {
    gap: 8px;
  }
  
  :global(.info-item) {
    gap: 6px;
  }
  
  :global(.info-icon) {
    width: 24px;
    height: 24px;
  }
  
  :global(.info-icon svg) {
    width: 10px;
    height: 10px;
  }
  
  :global(.info-text) {
    font-size: 10px;
  }
  
  :global(.popup-actions) {
    margin-top: 10px;
  }
  
  :global(.enhanced-detail-btn) {
    padding: 8px 12px;
    font-size: 10px;
    gap: 4px;
  }
  
  :global(.enhanced-detail-btn svg) {
    width: 10px;
    height: 10px;
  }
  
  :global(.popup-close-btn) {
    top: 4px;
    right: 4px;
    width: 18px;
    height: 18px;
  }
  
  :global(.popup-close-btn svg) {
    width: 8px;
    height: 8px;
  }
}

@media (max-width: 360px) {
  :global(.modern-popup-container .leaflet-popup-content) {
    width: 200px !important;
    max-width: calc(100vw - 16px) !important;
  }
  
  :global(.modern-popup-container.centered-popup .leaflet-popup-content-wrapper) {
    left: 50% !important;
    transform: translateX(-50%) !important;
    margin: 0 auto !important;
  }
  
  :global(.modern-marker-popup) {
    min-width: 180px;
  }
  
  :global(.popup-header) {
    padding: 8px 24px 6px 10px;
  }
  
  :global(.popup-title h3) {
    font-size: 12px;
  }
  
  :global(.popup-content) {
    padding: 10px;
  }
  
  :global(.user-avatar) {
    width: 32px;
    height: 32px;
  }
  
  :global(.avatar-text) {
    font-size: 12px;
  }
  
  :global(.user-name) {
    font-size: 11px;
  }
  
  :global(.user-email) {
    font-size: 8px;
  }
}

/* Tablet responsividad */
@media (min-width: 481px) and (max-width: 768px) {
  :global(.modern-popup-container .leaflet-popup-content) {
    width: 260px !important;
  }
  
  :global(.modern-popup-container.centered-popup .leaflet-popup-content-wrapper) {
    left: 50% !important;
    transform: translateX(-50%) !important;
    margin: 0 auto !important;
  }
  
  :global(.popup-header) {
    padding: 12px 30px 9px 14px;
  }
  
  :global(.popup-content) {
    padding: 14px;
  }
}

@keyframes popupSlideFromRight {
  0% {
    opacity: 0;
    transform: translateX(50px) rotateY(-15deg) scale(0.9);
  }
  60% {
    opacity: 0.9;
    transform: translateX(-5px) rotateY(2deg) scale(1.02);
  }
  100% {
    opacity: 1;
    transform: translateX(0) rotateY(0deg) scale(1);
  }
}

:global(.modern-marker-popup) {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: white;
  border-radius: 16px;
  overflow: visible !important; /* Permitir que el palito sea visible fuera del popup */
  min-width: 240px;
  animation: contentFlipIn 0.9s cubic-bezier(0.175, 0.885, 0.32, 1.275) 0.2s both;
  position: relative;
  /* El palito vertical se crea usando ::after - ver estilos más abajo */
}

/* Palito vertical tipo paleta - Conecta el modal con el centro exacto del círculo */
:global(.modern-marker-popup::after) {
  content: "" !important;
  display: block !important;
  position: absolute !important;
  left: 50% !important;
  bottom: -35px !important; /* Longitud para llegar al centro del círculo */
  transform: translateX(-50%) !important;
  width: 4px !important; /* Ancho del palito */
  height: 35px !important; /* Altura que llega exactamente al centro del círculo */
  background: #FF9800 !important; /* Color por defecto naranja */
  border-radius: 2px !important; /* Bordes redondeados */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
  z-index: 1000 !important; /* Z-index alto para estar visible */
  pointer-events: none !important;
}



/* Responsive: Palito ajustado en dispositivos táctiles */
@media (max-width: 768px) {
  :global(.modern-marker-popup::after) {
    width: 3px !important;
    height: 30px !important;
    bottom: -30px !important;
  }
}

@media (max-width: 480px) {
  :global(.modern-marker-popup::after) {
    width: 2px !important;
    height: 25px !important;
    bottom: -25px !important;
  }
}

/* Palito con los colores según tipo de actividad - Más visible y conectado */
:global(.modern-marker-popup.entrada-popup::after) {
  background: #32CD32 !important; /* Verde lima para entrada */
  box-shadow: 0 0 8px rgba(50, 205, 50, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.2) !important; /* Brillo verde + borde */
}

:global(.modern-marker-popup.salida-popup::after) {
  background: #DC2626 !important; /* Rojo para salida */
  box-shadow: 0 0 8px rgba(220, 38, 38, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.2) !important; /* Brillo rojo + borde */
}

:global(.modern-marker-popup.registro-hoy-popup::after) {
  background: #1E3A8A !important; /* Azul marino para registros de hoy */
  box-shadow: 0 0 8px rgba(30, 58, 138, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.2) !important; /* Brillo azul + borde */
}

:global(.modern-marker-popup.antiguo-popup::after) {
  background: #FF9800 !important; /* Naranja para registros antiguos */
  box-shadow: 0 0 8px rgba(255, 152, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.2) !important; /* Brillo naranja + borde */
}



/* Botón de cerrar personalizado del popup - Posicionamiento mejorado */
:global(.popup-close-btn) {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 20px;
  height: 20px;
  background: rgba(255, 255, 255, 0.95);
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 15; /* Z-index alto para estar por encima del contenido */
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  color: #666;
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
  animation: fadeInRotate 0.6s ease-out 0.4s both;
}

:global(.popup-close-btn:hover) {
  background: rgba(244, 67, 54, 0.95);
  color: white;
  transform: scale(1.1) rotate(90deg);
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.3);
}

:global(.popup-close-btn:active) {
  transform: scale(0.95) rotate(90deg);
}

:global(.popup-close-btn svg) {
  width: 10px;
  height: 10px;
}

@keyframes fadeInRotate {
  0% {
    opacity: 0;
    transform: scale(0.5) rotate(-180deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

/* Popup para entrada (verde lima) */
:global(.modern-marker-popup.entrada-popup) {
  background: linear-gradient(135deg, #32CD32 0%, #28a745 50%, #20c997 100%);
  box-shadow: 0 8px 32px rgba(50, 205, 50, 0.3);
}

/* Popup para salida (rojo) */
:global(.modern-marker-popup.salida-popup) {
  background: linear-gradient(135deg, #DC2626 0%, #b91c1c 50%, #991b1b 100%);
  box-shadow: 0 8px 32px rgba(220, 38, 38, 0.3);
}

/* Popup para registros de hoy (azul marino) */
:global(.modern-marker-popup.registro-hoy-popup) {
  background: linear-gradient(135deg, #1E3A8A 0%, #1e40af 50%, #1d4ed8 100%);
  box-shadow: 0 8px 32px rgba(30, 58, 138, 0.3);
}

/* Popup para ubicaciones antiguas (naranja) */
:global(.modern-marker-popup.antiguo-popup) {
  background: linear-gradient(135deg, #FF9800 0%, #f57c00 50%, #ef6c00 100%);
  box-shadow: 0 8px 32px rgba(255, 152, 0, 0.3);
}

@keyframes contentFlipIn {
  0% {
    opacity: 0;
    transform: rotateX(-90deg) scale(0.8);
    transform-origin: center bottom;
  }
  50% {
    opacity: 0.7;
    transform: rotateX(10deg) scale(1.05);
  }
  100% {
    opacity: 1;
    transform: rotateX(0deg) scale(1);
  }
}

:global(.popup-header) {
  padding: 14px 32px 10px 16px; /* Padding derecho aumentado para el botón de cerrar */
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid rgba(255, 255, 255, 0.25);
  position: relative;
  animation: headerSlideDown 0.6s ease-out 0.4s both;
}

@keyframes headerSlideDown {
  0% {
    opacity: 0;
    transform: translateY(-30px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Efecto brillante en el header */
:global(.popup-header::before) {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  animation: headerShine 3s ease-in-out infinite;
}

@keyframes headerShine {
  0% { left: -100%; }
  50% { left: 100%; }
  100% { left: 100%; }
}

:global(.popup-title) {
  flex: 1;
}

:global(.popup-id) {
  font-size: 10px;
  opacity: 0.9;
  font-weight: 600;
  display: block;
  margin-bottom: 3px;
  animation: fadeInUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.3s both;
  letter-spacing: 0.5px;
}

:global(.popup-title h3) {
  margin: 0;
  font-size: 15px;
  font-weight: 700;
  animation: fadeInUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.4s both;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

:global(.popup-status) {
  animation: bounceIn 1s cubic-bezier(0.68, -0.55, 0.265, 1.55) 0.5s both;
}

:global(.status-badge) {
  padding: 3px 8px;
  border-radius: 16px;
  font-size: 9px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

:global(.status-badge.entrada) {
  background: rgba(50, 205, 50, 0.9); /* Verde lima */
  color: white;
  box-shadow: 0 2px 8px rgba(50, 205, 50, 0.3);
  animation: pulseEntrada 2s ease-in-out infinite 2s;
}

:global(.status-badge.salida) {
  background: rgba(220, 38, 38, 0.9); /* Rojo */
  color: white;
  box-shadow: 0 2px 8px rgba(220, 38, 38, 0.3);
  animation: pulseSalida 2s ease-in-out infinite 2s;
}

:global(.status-badge.registro-hoy) {
  background: rgba(30, 58, 138, 0.9); /* Azul marino */
  color: white;
  box-shadow: 0 2px 8px rgba(30, 58, 138, 0.3);
  animation: pulseRegistroHoy 2s ease-in-out infinite 2s;
}

:global(.status-badge.antiguo) {
  background: rgba(255, 152, 0, 0.9); /* Naranja */
  color: white;
  box-shadow: 0 2px 8px rgba(255, 152, 0, 0.3);
  animation: pulseOrange 2s ease-in-out infinite 2s;
}

@keyframes pulseGreen {
  0%, 100% {
    box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
  }
  50% {
    box-shadow: 0 2px 15px rgba(76, 175, 80, 0.6);
    transform: scale(1.05);
  }
}

@keyframes pulseOrange {
  0%, 100% {
    box-shadow: 0 2px 8px rgba(255, 152, 0, 0.3);
  }
  50% {
    box-shadow: 0 2px 15px rgba(255, 152, 0, 0.6);
    transform: scale(1.05);
  }
}

@keyframes pulseEntrada {
  0%, 100% {
    box-shadow: 0 2px 8px rgba(50, 205, 50, 0.3);
  }
  50% {
    box-shadow: 0 2px 15px rgba(50, 205, 50, 0.6);
    transform: scale(1.05);
  }
}

@keyframes pulseSalida {
  0%, 100% {
    box-shadow: 0 2px 8px rgba(220, 38, 38, 0.3);
  }
  50% {
    box-shadow: 0 2px 15px rgba(220, 38, 38, 0.6);
    transform: scale(1.05);
  }
}

@keyframes pulseRegistroHoy {
  0%, 100% {
    box-shadow: 0 2px 8px rgba(30, 58, 138, 0.3);
  }
  50% {
    box-shadow: 0 2px 15px rgba(30, 58, 138, 0.6);
    transform: scale(1.05);
  }
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3) rotate(-45deg);
  }
  50% {
    opacity: 1;
    transform: scale(1.15) rotate(5deg);
  }
  70% {
    transform: scale(0.95) rotate(-2deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

:global(.popup-content) {
  padding: 16px;
}

:global(.user-info) {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
  animation: slideInLeft 0.9s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.6s both;
}

@keyframes slideInLeft {
  0% {
    opacity: 0;
    transform: translateX(-20px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

:global(.user-avatar) {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(255, 255, 255, 0.4);
  animation: rotateIn 1s cubic-bezier(0.68, -0.55, 0.265, 1.55) 0.7s both;
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

@keyframes rotateIn {
  0% {
    opacity: 0;
    transform: rotate(-180deg) scale(0.8);
  }
  100% {
    opacity: 1;
    transform: rotate(0deg) scale(1);
  }
}

:global(.avatar-text) {
  font-size: 18px;
  font-weight: 800;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

:global(.user-details) {
  flex: 1;
  min-width: 0;
}

:global(.user-name) {
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 3px;
  color: white;
  animation: fadeInRight 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.8s both;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

@keyframes fadeInRight {
  0% {
    opacity: 0;
    transform: translateX(30px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

:global(.user-email) {
  font-size: 11px;
  opacity: 0.95;
  color: rgba(255, 255, 255, 0.9);
  word-break: break-word;
  animation: typewriterEmail 1.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.9s both;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  gap: 4px;
}

:global(.email-icon) {
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  animation: bounceInIcon 0.6s ease-out 1.2s both;
}

:global(.email-icon svg) {
  width: 12px;
  height: 12px;
}

@keyframes bounceInIcon {
  0% {
    opacity: 0;
    transform: scale(0) rotate(180deg);
  }
  60% {
    opacity: 1;
    transform: scale(1.2) rotate(0deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

:global(.email-text) {
  flex: 1;
  min-width: 0;
}

@keyframes typewriterEmail {
  0% {
    opacity: 0;
    width: 0;
    transform: translateX(-10px);
  }
  30% {
    opacity: 1;
    transform: translateX(0);
  }
  100% {
    opacity: 0.9;
    width: 100%;
  }
}

/* Efecto adicional de destello para el email */
:global(.user-email::after) {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: emailShine 2s ease-out 1.5s;
}

@keyframes emailShine {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

:global(.popup-info) {
  margin-bottom: 20px;
}

:global(.info-item) {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  opacity: 0;
  animation: fadeInUp 0.5s ease-out forwards;
}

:global(.info-item:nth-child(1)) {
  animation-delay: 0.9s;
}

:global(.info-item:nth-child(2)) {
  animation-delay: 1s;
}

:global(.info-icon) {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  color: rgba(255, 255, 255, 0.9);
}

:global(.info-icon svg) {
  width: 14px;
  height: 14px;
}

:global(.info-text) {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
}

:global(.popup-actions) {
  text-align: center;
  animation: fadeInUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) 1.2s both;
}

:global(.modern-popup-btn) {
  background: rgba(255, 255, 255, 0.95);
  color: #333;
  border: none;
  padding: 12px 20px;
  border-radius: 25px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
  position: relative;
  overflow: hidden;
  min-width: 180px;
  justify-content: center;
}

/* Botón "Ver detalles" con estilo Glassmorphism moderno (iPhone style) */
:global(.enhanced-detail-btn) {
  background: rgba(255, 255, 255, 0.2) !important;
  border-radius: 20px !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  color: #fff !important;
  padding: 12px 28px !important;
  font-size: 0.95rem !important;
  width: auto !important;
  margin: 10px auto !important;
  box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.1) !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
  cursor: pointer !important;
  font-weight: 700 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 6px !important;
  text-decoration: none !important;
  position: relative !important;
  overflow: hidden !important;
  text-transform: none !important;
  letter-spacing: 0.3px !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
}

:global(.enhanced-detail-btn::before) {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.4s ease;
  z-index: 1;
}

:global(.enhanced-detail-btn:hover::before) {
  left: 100%;
}

:global(.enhanced-detail-btn:hover) {
  background: rgba(255, 255, 255, 0.35) !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  transform: translateY(-2px) !important;
  border-color: rgba(255, 255, 255, 0.4) !important;
}

:global(.enhanced-detail-btn:active) {
  transform: scale(0.95) !important;
  background: rgba(255, 255, 255, 0.15) !important;
  transition: all 0.1s ease-out !important;
}

/* Efecto de líquido para el botón glass */
@keyframes liquidGlassEffect {
  0% {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  }
  50% {
    box-shadow: 0 4px 25px rgba(255, 255, 255, 0.15);
  }
  100% {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  }
}

:global(.enhanced-detail-btn .btn-icon) {
  color: rgba(255, 255, 255, 0.9) !important;
  font-size: 14px !important;
  transition: all 0.3s ease;
  z-index: 2;
}

:global(.enhanced-detail-btn:hover .btn-icon) {
  color: #ffffff !important;
  transform: scale(1.15);
}

:global(.enhanced-detail-btn .btn-text) {
  color: rgba(255, 255, 255, 0.95) !important;
  font-weight: 700 !important;
  font-size: 0.92rem !important;
  position: relative;
  z-index: 2;
  transition: color 0.3s ease;
}

:global(.enhanced-detail-btn:hover .btn-text) {
  color: #ffffff !important;
}

:global(.modern-popup-btn:hover) {
   background: white;
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.18);
}

:global(.modern-popup-btn:hover .btn-icon) {
  transform: scale(1.1);
}

:global(.modern-popup-btn:active) {
  transform: translateY(0) scale(1);
}

:global(.btn-icon) {
  font-size: 16px;
  transition: all 0.3s ease;
}

/* Estilos responsivos - IGUAL QUE REGISTROSVIEW */

/* Responsive */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }
  
  .page-header {
    padding: 8px 20px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .page-content {
    padding: 16px 20px;
  }
  
  .filter-group {
    grid-template-columns: 1fr;
    grid-template-areas: 
      "search"
      "filter1"
      "filter2"
      "legend";
    gap: 12px;
    padding: 16px;
  }
  
  .filter-item {
    width: 100%;
  }
  
  .modern-select {
    width: 100%;
    padding: 10px 12px;
    font-size: 14px;
  }
  
  .modern-search-input {
    padding: 10px;
    font-size: 14px;
  }
  
  .modern-search-btn {
    width: 36px;
    height: 36px;
  }
  
  .mapa-container {
    min-height: 300px;
  }
}

/* Ajustes específicos para el panel de detalles responsivo */
.registro-info-panel {
  position: fixed;
  top: clamp(80px, 15vh, 120px);
  right: -100vw;
  width: clamp(280px, 35vw, 400px);
  max-width: calc(100vw - 40px);
  height: calc(100vh - clamp(100px, 20vh, 160px));
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: clamp(12px, 2vw, 16px) 0 0 clamp(12px, 2vw, 16px);
  box-shadow: -8px 0 32px rgba(0, 0, 0, 0.15);
  z-index: 3000;
  transition: right 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow-y: auto;
  box-sizing: border-box;
}

.registro-info-panel.panel-visible {
  right: clamp(10px, 2vw, 20px);
}

/* Responsive para panel de detalles */
@media (max-width: 1024px) {
  .registro-info-panel {
    width: clamp(300px, 50vw, 450px);
    top: clamp(70px, 12vh, 100px);
  }
}

@media (max-width: 768px) {
  .registro-info-panel {
    width: calc(100vw - 20px);
    right: -100vw;
    top: clamp(60px, 10vh, 80px);
    height: calc(100vh - clamp(80px, 15vh, 120px));
    border-radius: clamp(8px, 2vw, 12px) clamp(8px, 2vw, 12px) 0 0;
  }
  
  .registro-info-panel.panel-visible {
    right: 10px;
  }
}

@media (max-width: 480px) {
  .registro-info-panel {
    width: calc(100vw - 10px);
    right: -100vw;
    top: clamp(50px, 8vh, 70px);
    height: calc(100vh - clamp(60px, 12vh, 100px));
  }
  
  .registro-info-panel.panel-visible {
    right: 5px;
  }
}

/* Asegurar que los controles de Leaflet sean accesibles */
:global(.leaflet-control-zoom) {
  margin-right: clamp(10px, 2vw, 20px) !important;
  margin-top: clamp(10px, 2vw, 20px) !important;
}

:global(.leaflet-control-attribution) {
  font-size: clamp(9px, 1.5vw, 11px) !important;
}

/* Popup responsivo del mapa */
:global(.leaflet-popup-content-wrapper) {
  max-width: clamp(280px, 50vw, 400px) !important;
  min-width: clamp(250px, 45vw, 320px) !important;
}

:global(.leaflet-popup-content) {
  margin: clamp(8px, 1.5vw, 12px) clamp(10px, 2vw, 16px) !important;
  font-size: clamp(11px, 1.8vw, 13px) !important;
}

@media (max-width: 768px) {
  :global(.leaflet-popup-content-wrapper) {
    max-width: calc(100vw - 40px) !important;
    min-width: clamp(200px, 80vw, 300px) !important;
  }
}

@media (max-width: 480px) {
  :global(.leaflet-popup-content-wrapper) {
    max-width: calc(100vw - 20px) !important;
    min-width: calc(100vw - 60px) !important;
  }
  
  :global(.leaflet-popup-content) {
    margin: clamp(6px, 1.5vw, 10px) clamp(8px, 2vw, 12px) !important;
    font-size: clamp(10px, 2.5vw, 12px) !important;
  }
}

/* Estilos para contadores compactos del visor */
.visor-stats-compact {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(clamp(120px, 18vw, 160px), 1fr));
  gap: clamp(8px, 1.5vw, 12px);
  padding: clamp(8px, 2vw, 12px) clamp(12px, 3vw, 20px);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 255, 248, 0.95) 100%);
  border-bottom: 1px solid rgba(76, 175, 80, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  width: 100%;
  box-sizing: border-box;
  margin: 0;
  border-radius: 0;
}

.compact-stat-card {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.08) 0%, rgba(102, 187, 106, 0.05) 100%);
  padding: clamp(6px, 1.5vw, 10px) clamp(8px, 2vw, 12px);
  border-radius: clamp(8px, 1.5vw, 12px);
  box-shadow: 
    0 2px 8px rgba(76, 175, 80, 0.1), 
    0 1px 4px rgba(0,0,0,0.05),
    inset 0 1px 0 rgba(255,255,255,0.3);
  display: flex;
  align-items: center;
  gap: clamp(6px, 1.5vw, 8px);
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(76, 175, 80, 0.15);
  min-height: clamp(40px, 6vh, 50px);
}

.compact-stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(76, 175, 80, 0.1), transparent);
  border-radius: clamp(8px, 1.5vw, 12px);
  transition: left 0.5s ease;
  z-index: 0;
}

.compact-stat-card:hover::before {
  left: 100%;
}

.compact-stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 4px 16px rgba(76, 175, 80, 0.2), 
    0 2px 8px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255,255,255,0.4);
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.12) 0%, rgba(102, 187, 106, 0.08) 100%);
  border-color: rgba(76, 175, 80, 0.25);
}

.compact-stat-icon {
  width: clamp(24px, 4vw, 28px);
  height: clamp(24px, 4vw, 28px);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border-radius: clamp(4px, 1vw, 6px);
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(102, 187, 106, 0.05) 100%);
  position: relative;
  flex-shrink: 0;
  z-index: 1;
}

.compact-stat-icon::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: radial-gradient(circle, rgba(76, 175, 80, 0.15) 0%, transparent 70%);
  border-radius: 50%;
  transition: all 0.3s ease;
  transform: translate(-50%, -50%);
}

.compact-stat-card:hover .compact-stat-icon {
  transform: scale(1.1);
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(102, 187, 106, 0.08) 100%);
}

.compact-stat-card:hover .compact-stat-icon::before {
  width: clamp(35px, 6vw, 40px);
  height: clamp(35px, 6vw, 40px);
}

.compact-stat-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  z-index: 1;
}

.compact-stat-value {
  font-size: clamp(14px, 2.8vw, 18px);
  color: #4CAF50;
  margin-bottom: clamp(1px, 0.5vw, 2px);
  font-weight: 700;
  letter-spacing: clamp(0.3px, 0.08vw, 0.5px);
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.1;
}

.compact-stat-card:hover .compact-stat-value {
  transform: scale(1.05);
  background: linear-gradient(135deg, #388e3c 0%, #4CAF50 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.compact-stat-label {
  color: #666;
  font-size: clamp(8px, 1.4vw, 10px);
  font-weight: 600;
  margin: 0;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: clamp(0.1px, 0.05vw, 0.2px);
  line-height: 1.2;
}

.compact-stat-card:hover .compact-stat-label {
  color: #4CAF50;
}

/* Responsive para contadores compactos */
@media (max-width: 768px) {
  .visor-stats-compact {
    grid-template-columns: repeat(2, 1fr);
    gap: clamp(6px, 1.5vw, 8px);
    padding: clamp(6px, 1.5vw, 8px) clamp(10px, 2.5vw, 16px);
  }
  
  .compact-stat-card {
    padding: clamp(5px, 1.2vw, 8px) clamp(6px, 1.5vw, 10px);
    min-height: clamp(35px, 5vh, 45px);
    gap: clamp(4px, 1vw, 6px);
  }
  
  .compact-stat-icon {
    width: clamp(20px, 3.5vw, 24px);
    height: clamp(20px, 3.5vw, 24px);
  }
  
  .compact-stat-value {
    font-size: clamp(12px, 2.5vw, 16px);
  }
  
  .compact-stat-label {
    font-size: clamp(7px, 1.2vw, 9px);
  }
}

@media (max-width: 480px) {
  .visor-stats-compact {
    grid-template-columns: repeat(2, 1fr);
    gap: clamp(4px, 1vw, 6px);
    padding: clamp(5px, 1.2vw, 6px) clamp(8px, 2vw, 12px);
  }
  
  .compact-stat-card {
    padding: clamp(4px, 1vw, 6px) clamp(5px, 1.2vw, 8px);
    min-height: clamp(30px, 4.5vh, 40px);
    gap: clamp(3px, 0.8vw, 5px);
    border-radius: clamp(6px, 1.2vw, 8px);
  }
  
  .compact-stat-icon {
    width: clamp(18px, 3vw, 22px);
    height: clamp(18px, 3vw, 22px);
    border-radius: clamp(3px, 0.8vw, 4px);
  }
  
  .compact-stat-value {
    font-size: clamp(11px, 2.2vw, 14px);
  }
  
  .compact-stat-label {
    font-size: clamp(6px, 1vw, 8px);
    letter-spacing: clamp(0.05px, 0.03vw, 0.1px);
  }
}

/* Fin de estilos responsivos */
</style>
