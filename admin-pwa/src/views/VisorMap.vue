<template>
  <div class="visor-map-container">
    <!-- Importar fuentes modernas -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <Sidebar_NEW @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <path d="M8 3h3a7 7 0 0 0 3 18h-3A17 17 0 0 1 8 3z"/>
                <path d="M16 12h3"/>
                <path d="M16 18h2"/>
                <path d="M16 6h2"/>
                <path d="M3 12h3"/>
                <path d="M6 6h2"/>
                <path d="M6 18h2"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Visor de seguimiento diario</h1>
              <p class="header-subtitle">Visualización de registros</p>
            </div>
          </div>
          <div class="header-actions">
            <button @click="recargarMapa" class="refresh-btn-icon" :class="{ loading }" :disabled="loading" title="Actualizar datos">
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
        <!-- Panel de control lateral para el mapa -->
        <div class="controles-panel">
          <div class="panel-header">
            <h3 class="titulo-controles-centrado">Controles del Mapa</h3>
          </div>
          
          <div class="panel-section">
            <div class="section-header-status">
              <h4>Estado</h4>
              <div v-if="!error" class="status-badge-small loading">
                Actualizando<span class="loading-dots"></span>
              </div>
            </div>
            <div v-if="error" class="error-message">
              <p>{{ error }}</p>
              <button @click="recargarMapa" class="retry-btn-small">Reintentar</button>
            </div>
            <div v-else class="status-message">
              <p class="status-info-ubicaciones">{{ totalPuntosEnMapa }} ubicaciones en el mapa</p>
            </div>
          </div>
          
          <div class="panel-section">
            <div class="section-header" @click="toggleFiltros">
              <h4>Clasificador</h4>
              <button class="toggle-btn" :class="{ 'rotated': mostrarFiltros }">
                <svg v-if="mostrarFiltros" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                <svg v-else width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
              </button>
            </div>
            <div v-show="mostrarFiltros" class="filter-controls-compact">
              <div class="filter-group-compact">
                <div class="filter-item-compact">
                  <svg class="filter-icon-small" width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M3 18h6v-2H3v2zM3 6v2h18V6H3zm0 7h12v-2H3v2z"/>
                  </svg>
                  <select v-model="filtroTipo" class="compact-select" @change="aplicarFiltros">
                    <option value="">Todas las actividades</option>
                    <option value="entrada">Solo Entradas</option>
                    <option value="salida">Solo Salidas</option>
                    <option value="campo-hoy">Solo Campo (hoy)</option>
                    <option value="gabinete-hoy">Solo Gabinete (hoy)</option>
                    <option value="actividades-generales">Solo Actividades Total (Hoy)</option>
                    <option value="registro-antiguo">Solo Registros Antiguos</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
          
          <div class="panel-section">
            <h4>Estadísticas</h4>
            <div class="stat-grid">
              <div class="stat-item">
                <span class="stat-label">Total Usuarios</span>
                <span class="stat-value">{{ totalUsuariosRegistrados }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Entradas del día</span>
                <span class="stat-value entrada">{{ estadisticasDiaActual.entradasDia }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Salidas del día</span>
                <span class="stat-value salida">{{ estadisticasDiaActual.salidasDia }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Campo (hoy)</span>
                <span class="stat-value campo">{{ estadisticasDiaActual.campoHoy }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Gabinete (hoy)</span>
                <span class="stat-value gabinete">{{ estadisticasDiaActual.gabineteHoy }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Actividades total (Hoy)</span>
                <span class="stat-value actividades-total">{{ estadisticasDiaActual.campoHoy + estadisticasDiaActual.gabineteHoy }}</span>
              </div>
            </div>
          </div>
          
          <div class="panel-section">
            <h4>Leyenda</h4>
            <div class="leyenda-container">
              <div class="leyenda-grid">
                
                <!-- Subtítulo para Asistencias -->
                <div class="leyenda-subtitle">
                  <h5>Asistencias</h5>
                </div>
                
                <div class="leyenda-item">
                  <div class="color-marker entrada"></div>
                  <span>Entrada (hoy)</span>
                </div>
                <div class="leyenda-item">
                  <div class="color-marker salida"></div>
                  <span>Salida (hoy)</span>
                </div>
                
                <!-- Subtítulo para Actividades (reducido) -->
                <div class="leyenda-subtitle">
                  <h5>Actividades</h5>
                </div>
                
                <div class="leyenda-item">
                  <div class="color-marker campo-hoy"></div>
                  <span>Campo (hoy)</span>
                </div>
                <div class="leyenda-item">
                  <div class="color-marker gabinete-hoy"></div>
                  <span>Gabinete (hoy)</span>
                </div>
                <div class="leyenda-item">
                  <div class="color-marker actividades-generales"></div>
                  <span>Actividades total (Hoy)</span>
                </div>
                
                <!-- Subtítulo para Otros -->
                <div class="leyenda-subtitle">
                  <h5>Otros</h5>
                </div>
                
                <div class="leyenda-item">
                  <div class="color-marker registro-antiguo"></div>
                  <span>Registro antiguo</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="panel-section">
            <h4>Ayuda</h4>
            <div class="help-text">
              <p>• Haz clic en los grupos para expandir</p>
              <p>• Haz clic en los puntos para ver detalles</p>
              <p>• Usa los controles de zoom para acercar/alejar</p>
            </div>
          </div>
        </div>
        
        <!-- Contenedor del mapa con Mapbox -->
        <div class="mapa-container">
          <div v-if="loading" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando mapa optimizado...</p>
          </div>
          <div v-else-if="error" class="error-container">
            <p>{{ error }}</p>
            <button @click="cargarDatos" class="retry-btn">Reintentar</button>
          </div>
          <div id="mapa-principal" class="mapa-area"></div>
          
          <!-- Popup personalizado -->
          <div v-show="showCustomPopup" 
               class="custom-popup" 
               :class="'popup-' + popupData.tipoClase" 
               :style="{ top: popupY + 'px', left: popupX + 'px' }">
            <div class="popup-header">
              <div class="popup-title">
                <!-- Iconos según el tipo de actividad -->
                <svg v-if="popupData.tipoClase === 'entrada'" class="popup-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
                  <polyline points="10 17 15 12 10 7"/>
                  <line x1="15" y1="12" x2="3" y2="12"/>
                </svg>
                <svg v-else-if="popupData.tipoClase === 'salida'" class="popup-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                  <polyline points="16 17 21 12 16 7"/>
                  <line x1="21" y1="12" x2="9" y2="12"/>
                </svg>
                <svg v-else-if="popupData.tipoClase && (popupData.tipoClase.includes('campo') || popupData.tipoActividad === 'campo')" class="popup-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 18h18"/>
                  <path d="M8 14v-4"/>
                  <path d="M12 14v-6"/>
                  <path d="M16 14v-8"/>
                </svg>
                <svg v-else-if="popupData.tipoClase && (popupData.tipoClase.includes('gabinete') || popupData.tipoActividad === 'gabinete')" class="popup-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                </svg>
                <svg v-else-if="popupData.tipoClase === 'actividades-generales' || popupData.tipoActividad === 'actividades-generales'" class="popup-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
                <svg v-else-if="popupData.tipoClase === 'registro-hoy'" class="popup-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                </svg>
                <svg v-else class="popup-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="8" x2="12" y2="12"/>
                  <line x1="12" y1="16" x2="12.01" y2="16"/>
                </svg>
                <strong>{{ 
                  popupData.tipoActividad === 'campo' ? 'Actividad de Campo' :
                  popupData.tipoActividad === 'gabinete' ? 'Actividad de Gabinete' :
                  popupData.tipoActividad === 'entrada' ? 'Entrada' :
                  popupData.tipoActividad === 'salida' ? 'Salida' :
                  popupData.tipoActividad === 'oficina' ? 'Actividad de Oficina' :
                  popupData.tipoActividad === 'registro' ? 'Registro de Actividad' :
                  popupData.tipoActividad === 'actividades-generales' ? 'Actividad General' :
                  popupData.tipoClase === 'campo' || popupData.tipoClase === 'campo-hoy' ? 'Actividad de Campo' :
                  popupData.tipoClase === 'gabinete' || popupData.tipoClase === 'gabinete-hoy' ? 'Actividad de Gabinete' :
                  popupData.tipoClase === 'actividades-generales' ? 'Actividad General' :
                  popupData.tipoClase === 'entrada' ? 'Entrada' :
                  popupData.tipoClase === 'salida' ? 'Salida' :
                  popupData.tipoClase === 'registro-hoy' ? 'Registro de Hoy' :
                  popupData.tipoClase === 'registro-antiguo' || popupData.tipoClase === 'antiguo' ? 'Registro Anterior' :
                  'Actividad'
                }}</strong>
              </div>
              
              <button class="popup-close-btn" @click="cerrarPopup" title="Cerrar">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
            <div class="popup-body">
              <!-- Información básica del usuario -->
              <div class="popup-row">
                <svg class="popup-icon-small" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
                <div class="popup-usuario-info">
                  <div class="popup-usuario">{{ popupData.usuario }}</div>
                  <div class="popup-correo" v-if="popupData.correoUsuario">
                    <span class="popup-correo-texto">{{ popupData.correoUsuario }}</span>
                  </div>
                </div>
              </div>

              <!-- Información expandida -->
              <div v-if="popupData.expandido" class="popup-expanded-content">
                <div class="popup-expanded-layout">
                  <!-- Columna izquierda: Información básica -->
                  <div class="popup-info-column">
                    <!-- Detalles técnicos adicionales -->
                    <div class="popup-details-grid">
                      <!-- ID del registro y Tipo en la misma línea -->
                      <div class="popup-detail-item popup-detail-row">
                        <svg class="popup-icon-small" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M9 12h6M9 16h6M9 8h6m-8 12h8a2 2 0 002-2V6a2 2 0 00-2-2H7a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                        </svg>
                        <div class="popup-detail popup-detail-half">
                          <span class="popup-detail-label">ID Registro:</span>
                          <span class="popup-detail-value">{{ popupData.registroId || 'N/A' }}</span>
                        </div>
                        <svg class="popup-icon-small" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                        </svg>
                        <div class="popup-detail popup-detail-half">
                          <span class="popup-detail-label">Tipo:</span>
                          <span class="popup-detail-value tipo-actividad-value" :class="obtenerClaseTipoActividad(popupData.tipoActividad)">
                            {{ formatearTipoActividad(popupData.tipoActividad) }}
                          </span>
                        </div>
                      </div>

                      <!-- Usuario ID -->
                      <div class="popup-detail-item">
                        <svg class="popup-icon-small" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                          <circle cx="8.5" cy="7" r="4"/>
                          <path d="M20 8v6M23 11h-6"/>
                        </svg>
                        <div class="popup-detail">
                          <span class="popup-detail-label">Usuario ID:</span>
                          <span class="popup-detail-value">{{ popupData.usuarioId || 'N/A' }}</span>
                        </div>
                      </div>
                      
                      <!-- Precisión GPS -->
                      <div v-if="popupData.precision" class="popup-detail-item">
                        <svg class="popup-icon-small" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
                          <circle cx="12" cy="9" r="2.5"/>
                        </svg>
                        <div class="popup-detail">
                          <span class="popup-detail-label">Precisión GPS:</span>
                          <span class="popup-detail-value precision-value">± {{ popupData.precision }}m</span>
                        </div>
                      </div>

                      <!-- Estado de conexión -->
                      <div v-if="popupData.estadoConexion" class="popup-detail-item">
                        <svg class="popup-icon-small" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                          <circle cx="12" cy="12" r="3"/>
                        </svg>
                        <div class="popup-detail">
                          <span class="popup-detail-label">Estado:</span>
                          <span class="popup-detail-value status-value" :class="popupData.estadoConexion.toLowerCase()">{{ popupData.estadoConexion }}</span>
                        </div>
                      </div>
                      
                      <!-- Coordenadas - Solo visible cuando expandido -->
                      <div class="popup-detail-item">
                        <svg class="popup-icon-small" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                          <circle cx="12" cy="10" r="3"/>
                        </svg>
                        <div class="popup-detail">
                          <span class="popup-detail-label">Coordenadas:</span>
                          <span class="popup-detail-value coordinates-value">{{ popupData.coordenadasTexto }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Columna derecha: Imagen y Descripción -->
                  <div class="popup-image-column">
                    <!-- Imagen -->
                    <div v-if="popupData.imagenUrl" class="popup-image-section-compact">
                      <div class="popup-image-container-compact" @click="abrirImagenCompleta" style="cursor: pointer;" title="Click para ver imagen completa">
                        <img :src="popupData.imagenUrl" 
                             alt="Imagen del registro" 
                             class="popup-image-compact" 
                             @error="onImageError"
                             @load="onImageLoad" />
                      </div>
                    </div>
                    <div v-else class="popup-no-image-section-compact">
                      <div class="popup-no-image-placeholder">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <rect x="3" y="3" width="18" height="18" rx="2" ry="2" stroke="currentColor" stroke-width="2"/>
                          <circle cx="8.5" cy="8.5" r="1.5" stroke="currentColor" stroke-width="2"/>
                          <polyline points="21,15 16,10 5,21" stroke="currentColor" stroke-width="2"/>
                        </svg>
                        <span class="no-image-text">Sin imagen</span>
                      </div>
                    </div>
                    
                    <!-- Descripción debajo de la imagen con scroll -->
                    <div v-if="popupData.descripcion" class="popup-description-section-compact">
                      <div class="popup-section-header">
                        <svg class="popup-icon-small" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                          <polyline points="14,2 14,8 20,8"/>
                          <line x1="16" y1="13" x2="8" y2="13"/>
                          <line x1="16" y1="17" x2="8" y2="17"/>
                          <polyline points="10,9 9,9 8,9"/>
                        </svg>
                        <span class="popup-section-title">Descripción</span>
                      </div>
                      <div class="popup-description-scrollable">
                        {{ popupData.descripcion }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Coordenadas (solo visible cuando NO expandido) -->
              <div v-if="!popupData.expandido" class="popup-row">
                <svg class="popup-icon-small" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
                <div class="popup-coordenadas">{{ popupData.coordenadasTexto }}</div>
              </div>
              
              <!-- Fecha y hora con iconos -->
              <div class="popup-datetime-section">
                <div class="popup-row">
                  <svg class="popup-icon-small" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                    <line x1="16" y1="2" x2="16" y2="6"/>
                    <line x1="8" y1="2" x2="8" y2="6"/>
                    <line x1="3" y1="10" x2="21" y2="10"/>
                  </svg>
                  <div class="popup-fecha">{{ popupData.fechaFormateada }}</div>
                </div>
                <div class="popup-row">
                  <svg class="popup-icon-small" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/>
                    <polyline points="12,6 12,12 16,14"/>
                  </svg>
                  <div class="popup-hora">{{ popupData.horaFormateada }}</div>
                </div>
              </div>
            </div>
            <div class="popup-footer">
              <button class="popup-btn" @click="toggleDetallesRegistro">
                <svg class="popup-btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path v-if="!popupData.expandido" d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle v-if="!popupData.expandido" cx="12" cy="12" r="3"/>
                  <path v-else d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                  <path v-if="popupData.expandido" d="M1 1l22 22"/>
                </svg>
                {{ popupData.expandido ? 'Ocultar detalles' : 'Ver más detalles' }}
              </button>
            </div>
            <!-- Flecha indicadora que apunta al punto en el mapa -->
            <div class="popup-arrow"></div>
          </div>
        </div>
      </div>
    </main>
    
    <!-- Modal para ver imagen completa -->
    <div v-if="mostrarImagenCompleta" class="image-modal-overlay" @click="cerrarImagenCompleta">
      <div class="image-modal-container">
        <button class="image-modal-close" @click="cerrarImagenCompleta" title="Cerrar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
        <div class="image-modal-content" @click.stop>
          <img :src="imagenCompletaUrl" alt="Imagen completa" class="image-modal-img" />
          <div class="image-modal-info">
            <div class="image-info-row">
              <strong>Usuario:</strong> {{ popupData.usuario }}
            </div>
            <div class="image-info-row">
              <strong>Fecha:</strong> {{ popupData.fechaFormateada }}
            </div>
            <div class="image-info-row" v-if="popupData.descripcion">
              <strong>Descripción:</strong> {{ popupData.descripcion }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'
import axios from 'axios'
import mapboxgl from 'mapbox-gl'
import { usuariosService } from '../services/usuariosService.js'
import asistenciasService from '../services/asistenciasService.js'
import { estadisticasService } from '../services/estadisticasService.js'
import healthCheckService from '../services/healthCheckService.js'

// Token de acceso de Mapbox - En producción debe estar en variables de entorno
mapboxgl.accessToken = 'pk.eyJ1IjoibWFyaWVsMDgiLCJhIjoiY202emV3MDhhMDN6YjJscHVqaXExdGpjMyJ9.F_ACoKzS_4e280lD0XndEw';

const router = useRouter()
const API_URL = 'https://apipwa.sembrandodatos.com'

// Estado de conexión
const isOnline = ref(navigator.onLine)

// Estado del componente
const loading = ref(true)
const error = ref('')
const totalPuntosEnMapa = ref(0)

// Control de carga para evitar múltiples solicitudes simultáneas
let cargaEnProceso = false
let ultimaCarga = 0
const INTERVALO_MINIMO_CARGA = 5000 // 5 segundos entre cargas

// Referencias al mapa y capas
let map = null
let puntosSource = null
let hasDatosUsuario = ref(false)
const mapInitialized = ref(false)

// Estado del popup personalizado
const showCustomPopup = ref(false)
const popupX = ref(0)
const popupY = ref(0)

// Estado del modal de imagen completa
const mostrarImagenCompleta = ref(false)
const imagenCompletaUrl = ref('')
const popupData = ref({
  coordinates: [],
  usuario: '',
  correoUsuario: '',
  fecha: '',
  fechaFormateada: '',
  horaFormateada: '',
  tipoActividad: '',
  tipoClase: '',
  coordenadasTexto: '',
  expandido: false,
  // Campos adicionales para la vista expandida
  registroId: '',
  usuarioId: '',
  descripcion: '',
  imagenUrl: '',
  precision: null,
  estadoConexion: '',
  datosOriginales: null
})

// Registros y filtrado
const registros = ref([])
const asistencias = ref([])
const usuarios = ref([])

// Variables de filtrado como en VisorView.vue
const filtroTipo = ref('')
const filtroPeriodo = ref('all')

// Estado de mostrar/ocultar filtros
const mostrarFiltros = ref(true)

// Estado de los clusters y horario CDMX
const clusterInfo = reactive({
  total: 0,
  entradas: 0,
  salidas: 0,
  campoHoy: 0,
  gabineteHoy: 0,
  registrosHoy: 0,
  registrosAntiguos: 0
})

// Estado para las estadísticas del día actual en horario CDMX
const estadisticasDiaActual = reactive({
  totalUsuariosDia: 0,
  entradasDia: 0,
  salidasDia: 0,
  actividadesDia: 0,
  campoHoy: 0,
  gabineteHoy: 0,
  fechaCDMX: null
})

// Estado para el total de usuarios registrados en el sistema
const totalUsuariosRegistrados = ref('0')

// Función para obtener la fecha actual en CDMX (tiempo real)
const obtenerFechaCDMX = () => {
  // Horario de Ciudad de México: UTC-6 (normal) o UTC-5 (horario de verano)
  // Para simplificar, usamos -6 como zona horaria fija para CDMX
  const fechaUTC = new Date();
  const offsetCDMX = -6 * 60; // -6 horas en minutos
  const utcOffset = fechaUTC.getTimezoneOffset(); // Offset local en minutos
  const totalOffset = offsetCDMX + utcOffset; // Diferencia entre local y CDMX
  
  const fechaCDMX = new Date(fechaUTC.getTime() + totalOffset * 60000);
  return fechaCDMX;
}

// Función para cargar datos con manejo robusto de errores
const cargarDatos = async () => {
  // Evitar múltiples cargas simultáneas
  const ahora = Date.now()
  if (cargaEnProceso) {
    console.log('🚫 Carga ya en proceso, omitiendo...')
    return
  }
  
  if (ahora - ultimaCarga < INTERVALO_MINIMO_CARGA) {
    console.log('🚫 Demasiado pronto para recargar, omitiendo...')
    return
  }
  
  cargaEnProceso = true
  ultimaCarga = ahora
  loading.value = true
  error.value = ''
  
  try {
    console.log('🔄 Iniciando carga de datos para VisorMap...')
    
    const token = localStorage.getItem('admin_token')
    
    // Cargar datos con manejo individual de errores y reintentos
    const [registrosData, asistenciasData, usuariosData] = await Promise.allSettled([
      cargarRegistrosConReintentos(token),
      cargarAsistenciasConReintentos(),
      cargarUsuariosConReintentos()
    ])
    
    // Procesar resultados de registros
    let registrosEnriquecidos = []
    if (registrosData.status === 'fulfilled') {
      console.log('✅ Registros cargados exitosamente')
      const registrosRaw = Array.isArray(registrosData.value) ? registrosData.value : (registrosData.value.registros || [])
      registrosEnriquecidos = await usuariosService.enriquecerRegistrosConUsuarios(registrosRaw)
      registros.value = registrosEnriquecidos
    } else {
      console.error('❌ Error al cargar registros:', registrosData.reason)
      registros.value = []
    }
    
    // Procesar resultados de asistencias
    let asistenciasResult = []
    if (asistenciasData.status === 'fulfilled') {
      console.log('✅ Asistencias cargadas exitosamente')
      asistenciasResult = asistenciasData.value || []
      asistencias.value = asistenciasResult
    } else {
      console.error('❌ Error al cargar asistencias:', asistenciasData.reason)
      asistencias.value = []
    }
    
    // Procesar resultados de usuarios
    if (usuariosData.status === 'fulfilled') {
      console.log('✅ Usuarios cargados exitosamente')
      usuarios.value = usuariosData.value || []
    } else {
      console.error('❌ Error al cargar usuarios:', usuariosData.reason)
      usuarios.value = []
    }
    
    // Calcular las últimas actividades por usuario
    const ultimasActividades = obtenerUltimasActividadesPorUsuario(registrosEnriquecidos, asistenciasResult)
    console.log(`📊 Últimas actividades calculadas: ${ultimasActividades.length}`)
    
    // Si el mapa ya está cargado, actualizar puntos
    if (map && mapInitialized.value) {
      actualizarPuntosMapa(ultimasActividades)
    } else {
      inicializarMapa(ultimasActividades)
    }
    
    // Cargar estadísticas del día actual en paralelo (sin bloquear)
    cargarEstadisticasDiaActual().catch(err => {
      console.error('⚠️ Error al cargar estadísticas (no crítico):', err)
    })
    
    // Cargar total de usuarios registrados en el sistema (sin bloquear)
    cargarTotalUsuarios().catch(err => {
      console.error('⚠️ Error al cargar total de usuarios (no crítico):', err)
    })
    
    hasDatosUsuario.value = true
    loading.value = false
    totalPuntosEnMapa.value = ultimasActividades.length
    
    console.log('✅ Carga de datos completada exitosamente')
    
  } catch (err) {
    console.error('❌ Error crítico al cargar datos:', err)
    if (err.response?.status === 401) {
      logout()
    } else {
      const errorMessage = err.response?.data?.detail || err.message || 'Error desconocido'
      error.value = 'Error al cargar los datos: ' + errorMessage
      loading.value = false
    }
  } finally {
    cargaEnProceso = false
  }
}

// Función auxiliar para cargar registros con reintentos
const cargarRegistrosConReintentos = async (token, maxReintentos = 3) => {
  // Verificar salud de la API primero
  const endpointDisponible = await healthCheckService.isEndpointAvailable('/registros')
  if (!endpointDisponible) {
    console.log('⚠️ Endpoint de registros no disponible según health check')
  }
  
  for (let intento = 1; intento <= maxReintentos; intento++) {
    try {
      console.log(`🔄 Intento ${intento}/${maxReintentos} - Cargando registros...`)
      
      const response = await axios.get(`${API_URL}/registros`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        timeout: 15000 // Timeout de 15 segundos
      })
      
      return response.data
      
    } catch (err) {
      console.error(`❌ Error en intento ${intento} al cargar registros:`, err.message)
      
      if (intento === maxReintentos) {
        throw err
      }
      
      // Esperar más tiempo entre reintentos
      await new Promise(resolve => setTimeout(resolve, 2000 * intento))
    }
  }
}

// Función auxiliar para cargar asistencias con reintentos
const cargarAsistenciasConReintentos = async (maxReintentos = 3) => {
  // Verificar salud de la API primero
  const endpointDisponible = await healthCheckService.isEndpointAvailable('/asistencias')
  if (!endpointDisponible) {
    console.log('⚠️ Endpoint de asistencias no disponible según health check')
  }
  
  for (let intento = 1; intento <= maxReintentos; intento++) {
    try {
      console.log(`🔄 Intento ${intento}/${maxReintentos} - Cargando asistencias...`)
      
      return await asistenciasService.obtenerAsistenciasConUsuarios()
      
    } catch (err) {
      console.error(`❌ Error en intento ${intento} al cargar asistencias:`, err.message)
      
      if (intento === maxReintentos) {
        throw err
      }
      
      // Esperar más tiempo entre reintentos
      await new Promise(resolve => setTimeout(resolve, 2000 * intento))
    }
  }
}

// Función auxiliar para cargar usuarios con reintentos
const cargarUsuariosConReintentos = async (maxReintentos = 3) => {
  // Verificar salud de la API primero
  const endpointDisponible = await healthCheckService.isEndpointAvailable('/usuarios')
  if (!endpointDisponible) {
    console.log('⚠️ Endpoint de usuarios no disponible según health check')
  }
  
  for (let intento = 1; intento <= maxReintentos; intento++) {
    try {
      console.log(`🔄 Intento ${intento}/${maxReintentos} - Cargando usuarios...`)
      
      return await usuariosService.obtenerUsuarios()
      
    } catch (err) {
      console.error(`❌ Error en intento ${intento} al cargar usuarios:`, err.message)
      
      if (intento === maxReintentos) {
        throw err
      }
      
      // Esperar más tiempo entre reintentos
      await new Promise(resolve => setTimeout(resolve, 2000 * intento))
    }
  }
}

// Función para cargar estadísticas del día actual en horario CDMX
const cargarEstadisticasDiaActual = async () => {
  try {
    console.log('📊 Cargando estadísticas del día actual CDMX...')
    
    // Obtener estadísticas completas del día actual
    const estadisticas = await estadisticasService.obtenerEstadisticasDiaActual()
    
    // Actualizar el objeto reactivo
    estadisticasDiaActual.totalUsuariosDia = estadisticas.totalUsuariosDia || 0
    estadisticasDiaActual.entradasDia = estadisticas.entradasDia || 0
    estadisticasDiaActual.salidasDia = estadisticas.salidasDia || 0
    estadisticasDiaActual.actividadesDia = estadisticas.actividadesDia || 0
    estadisticasDiaActual.fechaCDMX = estadisticas.fechaCDMX
    
    // Obtener estadísticas por tipo de actividad
    try {
      const respuestaTipos = await axios.get(`${API_URL}/estadisticas/tipo-actividad`)
      const estadisticasTipos = respuestaTipos.data.estadisticas_tipo
      
      // Actualizar contadores específicos por tipo
      estadisticasDiaActual.campoHoy = estadisticasTipos.dia_actual?.campo || 0
      estadisticasDiaActual.gabineteHoy = estadisticasTipos.dia_actual?.gabinete || 0
      
      console.log('📊 Estadísticas por tipo cargadas:', {
        campo: estadisticasDiaActual.campoHoy,
        gabinete: estadisticasDiaActual.gabineteHoy
      })
    } catch (errorTipos) {
      console.warn('⚠️ Error cargando estadísticas por tipo:', errorTipos)
      estadisticasDiaActual.campoHoy = 0
      estadisticasDiaActual.gabineteHoy = 0
    }
    
    console.log('✅ Estadísticas del día actualizadas:', estadisticasDiaActual)
    
  } catch (error) {
    console.error('❌ Error cargando estadísticas del día:', error)
    // Si hay error, mantener valores en 0 o usar fallback local
    estadisticasDiaActual.totalUsuariosDia = 0
    estadisticasDiaActual.entradasDia = 0
    estadisticasDiaActual.salidasDia = 0
    estadisticasDiaActual.actividadesDia = 0
    estadisticasDiaActual.campoHoy = 0
    estadisticasDiaActual.gabineteHoy = 0
  }
}

// Función para cargar el total de usuarios registrados en el sistema
const cargarTotalUsuarios = async () => {
  try {
    console.log('👥 Obteniendo total de usuarios registrados...')
    
    // Usar el servicio de usuarios para obtener todos los usuarios
    const usuarios = await usuariosService.obtenerUsuarios()
    
    // Actualizar el contador con formato localizado
    totalUsuariosRegistrados.value = usuarios.length.toLocaleString('es')
    
    console.log(`✅ Total de usuarios registrados: ${totalUsuariosRegistrados.value}`)
    
  } catch (error) {
    console.error('❌ Error obteniendo total de usuarios:', error)
    totalUsuariosRegistrados.value = '0'
  }
}

// Obtener las últimas actividades por usuario (combinando registros y asistencias)
const obtenerUltimasActividadesPorUsuario = (registros, asistencias) => {
  const mapaUsuarios = new Map()
  
  // Procesar registros normales
  registros.forEach(registro => {
    if (!registro.latitud || !registro.longitud) return
    
    const usuarioId = registro.usuario_id
    const fechaHora = new Date(registro.fecha_hora)
    
    const actividad = {
      ...registro,
      // Conservar el tipo_actividad original (campo, gabinete, etc.)
      tipo_actividad: registro.tipo_actividad || 'registro',
      fecha_actividad: fechaHora,
      latitud: parseFloat(registro.latitud),
      longitud: parseFloat(registro.longitud)
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
        latitud: parseFloat(asistencia.latitud_entrada),
        longitud: parseFloat(asistencia.longitud_entrada),
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
        latitud: parseFloat(asistencia.latitud_salida),
        longitud: parseFloat(asistencia.longitud_salida),
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
  return Array.from(mapaUsuarios.values()).filter(a => {
    // Verificar que las coordenadas sean válidas
    return !isNaN(a.latitud) && !isNaN(a.longitud) && 
           Math.abs(a.latitud) <= 90 && Math.abs(a.longitud) <= 180
  })
}

// Determinar el tipo de actividad para colores en el mapa usando horario CDMX
const determinarTipoActividad = (actividad) => {
  // Verificar si la actividad ocurrió hoy en horario CDMX
  const esActividadDeHoy = esUbicacionReciente(actividad.fecha_hora);
  
  // CASO 1: Si la actividad es de tipo entrada
  if (actividad.tipo_actividad === 'entrada') {
    // Si la entrada es de hoy (CDMX): Mediumblue
    if (esActividadDeHoy) {
      return {
        tipo: 'entrada',
        clase: 'entrada',
        descripcion: 'Entrada de Hoy',
        color: 'rgb(0, 0, 205)' // Mediumblue
      };
    } 
    // Si la entrada NO es de hoy (CDMX): Silver (antigua)
    else {
      return {
        tipo: 'registro-antiguo',
        clase: 'antiguo',
        descripcion: 'Entrada Anterior',
        color: 'rgb(192, 192, 192)' // Silver
      };
    }
  }
  
  // CASO 2: Si la actividad es de tipo salida
  else if (actividad.tipo_actividad === 'salida') {
    // Si la salida es de hoy (CDMX): Rojo
    if (esActividadDeHoy) {
      return {
        tipo: 'salida',
        clase: 'salida',
        descripcion: 'Salida de Hoy',
        color: '#DC2626' // Rojo
      };
    }
    // Si la salida NO es de hoy (CDMX): Silver (antigua)
    else {
      return {
        tipo: 'registro-antiguo',
        clase: 'antiguo',
        descripcion: 'Salida Anterior',
        color: 'rgb(192, 192, 192)' // Silver
      };
    }
  }
  
  // CASO 3: Actividades de Campo
  else if (actividad.tipo_actividad === 'campo') {
    // Si la actividad de campo es de hoy (CDMX): Limegreen
    if (esActividadDeHoy) {
      return {
        tipo: 'campo-hoy',
        clase: 'campo-hoy',
        descripcion: 'Actividad de Campo Hoy',
        color: 'rgb(50, 205, 50)' // Limegreen
      };
    }
    // Si la actividad de campo NO es de hoy (CDMX): Silver (antigua)
    else {
      return {
        tipo: 'campo-antiguo',
        clase: 'antiguo',
        descripcion: 'Actividad de Campo Anterior',
        color: 'rgb(192, 192, 192)' // Silver
      };
    }
  }
  
  // CASO 4: Actividades de Gabinete
  else if (actividad.tipo_actividad === 'gabinete') {
    // Si la actividad de gabinete es de hoy (CDMX): Darkorange
    if (esActividadDeHoy) {
      return {
        tipo: 'gabinete-hoy',
        clase: 'gabinete-hoy',
        descripcion: 'Actividad de Gabinete Hoy',
        color: 'rgb(255, 140, 0)' // Darkorange
      };
    }
    // Si la actividad de gabinete NO es de hoy (CDMX): Silver (antigua)
    else {
      return {
        tipo: 'gabinete-antiguo',
        clase: 'antiguo',
        descripcion: 'Actividad de Gabinete Anterior',
        color: 'rgb(192, 192, 192)' // Silver
      };
    }
  }
  
  // CASO 5: Actividades sin tipo específico (por compatibilidad)
  else {
    // Si el registro es de hoy (CDMX): Limegreen (asumir campo por defecto)
    if (esActividadDeHoy) {
      return {
        tipo: 'campo-hoy',
        clase: 'campo-hoy',
        descripcion: 'Actividad de Campo Hoy',
        color: 'rgb(50, 205, 50)' // Limegreen (campo por defecto)
      };
    }
    // Si el registro NO es de hoy (CDMX): Silver (antiguo)
    else {
      return {
        tipo: 'campo-antiguo',
        clase: 'antiguo',
        descripcion: 'Actividad Anterior',
        color: 'rgb(192, 192, 192)' // Silver
      };
    }
  }
}

// Función para inicializar el mapa con Mapbox
const inicializarMapa = (datos) => {
  loading.value = true
  error.value = ''
  
  try {
    // Verificar que el token esté disponible
    if (!mapboxgl.accessToken) {
      console.error('No se ha proporcionado un token de Mapbox');
      error.value = 'Error: No se ha proporcionado un token de Mapbox';
      loading.value = false;
      return;
    }
    
    console.log('Inicializando mapa con token:', mapboxgl.accessToken.substring(0, 10) + '...');
    
    // Verificar validez del token (formato básico)
    if (!mapboxgl.accessToken.startsWith('pk.')) {
      console.error('El token de Mapbox no parece tener el formato correcto');
      error.value = 'Error: El token de Mapbox no tiene el formato correcto';
      loading.value = false;
      return;
    }
    
    // Verificar que el elemento del mapa exista
    const mapElement = document.getElementById('mapa-principal');
    if (!mapElement) {
      console.error('No se encuentra el elemento del mapa con ID "mapa-principal"');
      error.value = 'Error: No se encuentra el contenedor del mapa';
      loading.value = false;
      return;
    }
    
    console.log('Iniciando creación del mapa con token:', mapboxgl.accessToken);
    
    // Crear nuevo mapa de Mapbox con el estilo original
    map = new mapboxgl.Map({
      container: 'mapa-principal',
      style: 'mapbox://styles/mapbox/streets-v11', // Volvemos al estilo original con más detalle
      center: [-99.1332, 19.4326], // Centro inicial en Ciudad de México
      zoom: 5, // Zoom inicial más cercano
      maxZoom: 18,
      pitchWithRotate: false, // Limitar inclinación para mejor rendimiento
      attributionControl: false,
      cooperativeGestures: false, // Desactivamos para permitir scroll normal con el mouse
      scrollZoom: true, // Habilitamos zoom con rueda del mouse
      dragRotate: false, // Desactivamos rotación con arrastre para una experiencia más intuitiva
      fadeDuration: 300   // Transiciones suaves
    });
    
    // Añadir controles de navegación mejorados con zoom visible
    map.addControl(new mapboxgl.NavigationControl({
      showCompass: true, // Mostramos la brújula para orientación
      visualizePitch: false, // No mostrar el control de inclinación para simplificar
      showZoom: true // Asegurarnos que los botones de zoom sean visibles
    }), 'top-right'); // Movemos a la esquina superior derecha para mejor visibilidad
    
    // Añadir mensaje sobre el uso de la rueda del mouse
    const zoomHelpElement = document.createElement('div');
    zoomHelpElement.className = 'mapbox-zoom-help';
    zoomHelpElement.innerHTML = `
      <div class="zoom-help-tooltip">
        <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none">
          <circle cx="12" cy="12" r="10"></circle>
          <path d="M12 16v-4"></path>
          <path d="M12 8h.01"></path>
        </svg>
        <span>Use la rueda del ratón para acercar/alejar</span>
      </div>
    `;
    map.getContainer().appendChild(zoomHelpElement);
    
    // Añadir control de atribución en posición menos intrusiva
    map.addControl(new mapboxgl.AttributionControl({
      compact: true
    }), 'bottom-left');
    
    // Añadir control de escala
    map.addControl(new mapboxgl.ScaleControl({
      maxWidth: 100,
      unit: 'metric'
    }), 'bottom-left');
    
    // Añadir atajos de teclado para zoom
    map.getCanvas().tabIndex = 0; // Hacer que el canvas sea enfocable para eventos de teclado
    map.getCanvas().addEventListener('keydown', (e) => {
      if (e.key === '+' || e.key === '=') {
        map.zoomIn(); // Zoom in con tecla +
      } else if (e.key === '-') {
        map.zoomOut(); // Zoom out con tecla -
      }
    });
    
    // Configurar el comportamiento de zoom con la rueda del ratón para hacerlo más suave
    map.scrollZoom.setWheelZoomRate(1/450); // Velocidad de zoom más suave
    map.scrollZoom.setZoomRate(0.75); // Ajustar la intensidad del zoom
    
    // Esperar a que el mapa se cargue
    map.on('load', () => {
      // Añadir fuente de datos para puntos individuales (sin clustering)
      map.addSource('puntos', {
        type: 'geojson',
        data: {
          type: 'FeatureCollection',
          features: []
        },
        cluster: false
      });
      
      // Modificar fuente de datos para deshabilitar clústeres completamente
      map.addSource('clusters', {
        type: 'geojson',
        data: {
          type: 'FeatureCollection',
          features: []
        },
        cluster: false // Desactivamos el clustering para que no aparezcan círculos con números
      });
      
      // Guardar referencia a la fuente para actualizarla después
      puntosSource = map.getSource('puntos');
      
      // Eliminamos las capas de clústeres para que no aparezcan en el mapa
      
      // Añadir capa para los puntos individuales
      map.addLayer({
        id: 'unclustered-point',
        type: 'circle',
        source: 'puntos',
        filter: ['!', ['has', 'point_count']],
        paint: {
          'circle-color': [
            'match',
            ['get', 'tipo_actividad'],
            'entrada', 'rgb(0, 0, 205)', // Mediumblue para entradas
            'salida', 'rgb(220, 20, 60)', // Crimson para salidas
            'campo-hoy', 'rgb(50, 205, 50)', // Limegreen para campo de hoy
            'gabinete-hoy', 'rgb(255, 140, 0)', // Darkorange para gabinete de hoy
            'actividades-generales', 'rgb(148, 0, 211)', // Darkviolet para actividades generales
            'campo-antiguo', 'rgb(192, 192, 192)', // Silver para campo antiguo
            'gabinete-antiguo', 'rgb(192, 192, 192)', // Silver para gabinete antiguo
            'registro-hoy', 'rgb(34, 139, 34)', // Verde para compatibilidad (campo por defecto)
            'registro-antiguo', 'rgb(192, 192, 192)', // Silver para registros antiguos
            '#A9A9A9' // Gris por defecto (no debería llegar aquí)
          ],
          // Tamaño un poco más grande pero manteniendo proporción según nivel de zoom
          'circle-radius': [
            'interpolate', 
            ['linear'], 
            ['zoom'],
            // A niveles de zoom bajos, puntos más visibles
            3, 3.5,
            // A niveles de zoom medios, puntos de tamaño medio
            8, 5.5,
            // A niveles de zoom altos, puntos más grandes
            14, 7
          ],
          // Borde ligeramente más grueso para mejor definición
          'circle-stroke-width': 1.5,
          'circle-stroke-color': 'white',
          'circle-opacity': 0.9
        }
      });
      
      // Eliminamos los eventos relacionados con clústeres, ya que no los usamos más
      
      // Usaremos las variables del componente principal para el popup

      // Evento al hacer clic en un punto individual
      map.on('click', 'unclustered-point', async (e) => {
        console.log('Click en punto individual', e.features[0]);
        const props = e.features[0].properties;
        const coordinates = e.features[0].geometry.coordinates.slice();
        
        // Asegurar que las coordenadas sean válidas
        if (!isNaN(coordinates[0]) && !isNaN(coordinates[1])) {
          
          // PASO 1: Marcar que el zoom será automático
          zoomAutomatico = true;
          
          // PASO 2: Centrar el mapa con zoom moderado
          console.log('🎯 Centrando mapa en coordenadas:', coordinates);
          
          // Centrar el mapa con un pequeño offset hacia abajo usando padding
          map.flyTo({
            center: coordinates, // Usar coordenadas originales
            zoom: map.getZoom() + 4.0, // Zoom alto
            duration: 800, // Animación suave
            essential: true,
            curve: 1, 
            speed: 0.8,
            // Padding para crear más espacio arriba y posicionar el punto más abajo
            padding: { top: 300, bottom: 50, left: 50, right: 50 }
          });
          
          // PASO 3: Esperar a que termine la animación del mapa
          const esperarCentrado = new Promise((resolve) => {
            map.once('moveend', () => {
              // Resetear la bandera de zoom automático
              zoomAutomatico = false;
              resolve();
            });
          });
          
          await esperarCentrado;
          console.log('✅ Mapa centrado correctamente');
          
          // PASO 4: Preparar datos del popup
          // Obtener información del punto
          const usuario = props.nombre || `Usuario ${props.usuario_id}`;
          const correoUsuario = props.correo || '';
          const fechaCompleta = new Date(props.fecha_hora);
          
          // Formatear fecha y hora por separado
          const fechaFormateada = fechaCompleta.toLocaleDateString('es-ES', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
          });
          
          const horaFormateada = fechaCompleta.toLocaleTimeString('es-ES', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
          }).toLowerCase(); // Convertir am/pm a minúsculas
          
          const tipoActividad = props.tipo_actividad_original || props.tipo_actividad || 'registro';
          
          console.log('🔍 Propiedades del registro completo:', props);
          console.log('🔍 Tipo de actividad detectado:', tipoActividad);
          console.log('🎨 Tipo de actividad para mapa:', props.tipo_actividad);
          
          // Obtener la URL de imagen con logging detallado
          console.log('📝 props.tipo_actividad original:', props.tipo_actividad);
          const imagenUrl = obtenerUrlImagen(props);
          console.log('🖼️ URL de imagen obtenida:', imagenUrl);
          
          // PASO 5: Actualizar variables globales del popup
          popupData.value = {
            coordinates: coordinates,
            usuario: usuario,
            correoUsuario: correoUsuario,
            fecha: fechaCompleta.toLocaleString('es-ES'), // Mantener para compatibilidad
            fechaFormateada: fechaFormateada,
            horaFormateada: horaFormateada,
            tipoActividad: tipoActividad,
            tipoClase: props.tipo_actividad_original || props.tipo_actividad,
            coordenadasTexto: `${coordinates[1].toFixed(6)}, ${coordinates[0].toFixed(6)}`,
            expandido: false,
            // Datos adicionales para la vista expandida
            registroId: props.id || props.registro_id || 'N/A',
            usuarioId: props.usuario_id || 'N/A',
            descripcion: props.descripcion || props.descripcion_entrada || props.descripcion_salida || '',
            imagenUrl: imagenUrl,
            precision: props.precision || props.accuracy || null,
            estadoConexion: props.estado_conexion || (props.offline ? 'Offline' : 'Online'),
            datosOriginales: props
          };
          
          // PASO 6: Posicionar el popup (después del centrado)
          // Convertir coordenadas geográficas a coordenadas de pantalla (actualizado después del flyTo)
          const point = map.project(coordinates);
          
          // Posicionar el popup para que la flecha apunte exactamente al centro del círculo
          // El popup se centra horizontalmente, y verticalmente se posiciona considerando la flecha
          popupX.value = point.x;
          popupY.value = point.y - 15; // Distancia optimizada para alineación perfecta de la flecha con el centro del punto
          showCustomPopup.value = true;
          
          console.log('✅ Popup mostrado en:', popupX.value, popupY.value);
          console.log('📋 Datos del popup:', popupData.value);
          
          // Evitar que se propague el evento para no cerrar el popup inmediatamente
          e.originalEvent.stopPropagation();
        }
      });
      
      // Cerrar el popup al hacer clic en cualquier lugar del mapa
      map.on('click', (e) => {
        // Verificar si el clic fue directamente en el mapa (y no en un punto)
        const features = map.queryRenderedFeatures(e.point, { layers: ['unclustered-point'] });
        if (features.length === 0) {
          console.log('Cerrar popup - clic fuera de punto');
          showCustomPopup.value = false;
        }
      });
      
      // Cambiar cursor a puntero al pasar sobre los puntos
      map.on('mouseenter', 'unclustered-point', () => {
        map.getCanvas().style.cursor = 'pointer';
      });
      
      map.on('mouseleave', 'unclustered-point', () => {
        map.getCanvas().style.cursor = '';
      });
      
      // Actualizar la posición del popup cuando el mapa se mueve
      map.on('move', () => {
        // Si el popup está abierto y hay coordenadas, actualizar su posición
        if (showCustomPopup.value && popupData.value.coordinates && popupData.value.coordinates.length) {
          const point = map.project(popupData.value.coordinates);
          popupX.value = point.x;
          popupY.value = point.y - 15; // Mantener la distancia optimizada para alineación perfecta
          // console.log('Actualizando posición del popup en move:', popupX.value, popupY.value);
        }
      });
      
      // Variable para controlar si el zoom es automático (del click en punto)
      let zoomAutomatico = false;
      
      // Modificar el evento de click para marcar zoom automático
      const clickOriginal = map.getContainer().querySelector('.mapboxgl-canvas');
      
      // Cerrar popup solo en zoom manual (no automático)
      map.on('zoomstart', () => {
        // Solo cerrar si no es zoom automático
        if (!zoomAutomatico && showCustomPopup.value) {
          console.log('Cerrar popup - zoom manual');
          showCustomPopup.value = false;
        }
      });
      
      // Actualizar puntos en el mapa
      if (datos && datos.length > 0) {
        actualizarPuntosMapa(datos);
      }
      
      mapInitialized.value = true
      loading.value = false;
    });
    
    // Manejar errores de carga del mapa
    map.on('error', (e) => {
      console.error('Error en el mapa:', e);
      const errorMsg = e.error ? 
        (e.error.message || e.error.toString()) : 
        (e.message || 'Error desconocido en la carga del mapa');
      
      console.log('Detalles del error:', errorMsg);
      error.value = 'Error al cargar el mapa: ' + errorMsg;
      
      // Intentar con estilos alternativos si el error es relacionado con el estilo
      if (errorMsg.includes('style') || errorMsg.includes('token')) {
        try {
          console.log('Intentando con estilos alternativos...');
          
          // Intentar primero con streets-v11 nuevamente (el estilo preferido)
          map.setStyle('mapbox://styles/mapbox/streets-v11');
          
          // Si aún hay problemas, establecer un temporizador para probar con estilos alternativos
          setTimeout(() => {
            if (error.value) {
              const estilosAlternativos = [
                'mapbox://styles/mapbox/outdoors-v11', 
                'mapbox://styles/mapbox/navigation-day-v1',
                'mapbox://styles/mapbox/light-v10'
              ];
              
              const estiloAleatorio = estilosAlternativos[Math.floor(Math.random() * estilosAlternativos.length)];
              console.log('Probando con estilo alternativo:', estiloAleatorio);
              map.setStyle(estiloAleatorio);
            }
          }, 2000);
          
        } catch (styleError) {
          console.error('Error al cambiar el estilo:', styleError);
        }
      }
      
      loading.value = false;
    });
    
    // Confirmar cuando el mapa está listo
    map.on('styledata', () => {
      console.log('Estilo del mapa cargado correctamente');
    });
    
  } catch (err) {
    console.error('Error al inicializar el mapa:', err);
    const errorMsg = err.message || err.toString() || 'Error desconocido';
    console.log('Detalles del error de inicialización:', errorMsg);
    error.value = 'Error al inicializar el mapa: ' + errorMsg;
    loading.value = false;
  }
}

// Función para actualizar los puntos en el mapa
const actualizarPuntosMapa = (datos) => {
  if (!map || !puntosSource) return;
  
  try {
    // Reiniciar contadores
    clusterInfo.total = 0;
    clusterInfo.entradas = 0;
    clusterInfo.salidas = 0;
    clusterInfo.campoHoy = 0;
    clusterInfo.gabineteHoy = 0;
    clusterInfo.registrosHoy = 0;
    clusterInfo.registrosAntiguos = 0;
    
    // Convertir datos a formato GeoJSON
    const features = datos.map(punto => {
      // Usar la función determinarTipoActividad para clasificar según horario CDMX
      const infoActividad = determinarTipoActividad(punto);
      let tipoActividad = infoActividad.tipo;
      
      // Para el mapa: si el filtro está en "actividades-generales", cambiar campo y gabinete por "actividades-generales"
      let tipoActividadMapa = tipoActividad;
      if (filtroTipo.value === 'actividades-generales') {
        if (tipoActividad === 'campo-hoy' || tipoActividad === 'gabinete-hoy') {
          tipoActividadMapa = 'actividades-generales';
        }
      }
      
      // Verificar si la actividad es de hoy según el horario CDMX
      const esHoy = esUbicacionReciente(punto.fecha_hora);
      
      // Actualizar contadores para las estadísticas
      clusterInfo.total++;
      
      // Actualizar contadores basados en el tipo de actividad del mapa
      if (tipoActividadMapa === 'entrada') {
        clusterInfo.entradas++;
      } else if (tipoActividadMapa === 'salida') {
        clusterInfo.salidas++;
      } else if (tipoActividadMapa === 'campo-hoy') {
        clusterInfo.campoHoy++;
        clusterInfo.registrosHoy++;
      } else if (tipoActividadMapa === 'gabinete-hoy') {
        clusterInfo.gabineteHoy++;
        clusterInfo.registrosHoy++;
      } else if (tipoActividadMapa === 'actividades-generales') {
        // Para actividades generales, no incrementamos contadores específicos
        clusterInfo.registrosHoy++;
      } else if (tipoActividadMapa === 'campo-antiguo' || tipoActividadMapa === 'gabinete-antiguo' || tipoActividadMapa === 'registro-antiguo') {
        clusterInfo.registrosAntiguos++;
      }
      
      return {
        type: 'Feature',
        properties: {
          id: punto.id,
          usuario_id: punto.usuario_id,
          nombre: punto.usuario?.nombre_completo || `Usuario ${punto.usuario_id}`,
          correo: punto.usuario?.correo || '',
          tipo_actividad: tipoActividadMapa, // Para el color del mapa
          tipo_actividad_original: tipoActividad, // Para el popup (mantener original)
          fecha_hora: punto.fecha_hora,
          descripcion: punto.descripcion || '',
          foto_url: punto.foto_url || null,
          foto_entrada_url: punto.foto_entrada_url || null,
          foto_salida_url: punto.foto_salida_url || null
        },
        geometry: {
          type: 'Point',
          coordinates: [punto.longitud, punto.latitud]
        }
      };
    });
    
    // Actualizar solo la fuente de datos para puntos (sin clústeres)
    puntosSource.setData({
      type: 'FeatureCollection',
      features: features
    });
    
    totalPuntosEnMapa.value = features.length;
    
    // Ajustar mapa para mostrar todos los puntos
    if (features.length > 0) {
      // Crear límites para contener todos los puntos
      const bounds = new mapboxgl.LngLatBounds();
      features.forEach(feature => {
        bounds.extend(feature.geometry.coordinates);
      });
      
      // Ajustar vista a los límites calculados
      map.fitBounds(bounds, {
        padding: { top: 50, bottom: 50, left: 50, right: 50 },
        maxZoom: 15
      });
    }
    
  } catch (err) {
    console.error('Error al actualizar puntos en el mapa:', err);
  }
}

// Función auxiliar para determinar si una ubicación es reciente usando horario CDMX
const esUbicacionReciente = (fechaStr) => {
  try {
    // Convertir la cadena de fecha a objeto Date
    const fechaObj = new Date(fechaStr);
    
    // Obtener la fecha actual en CDMX
    const fechaCDMX = obtenerFechaCDMX();
    
    // Ajustar la fecha proporcionada al horario CDMX
    const offsetCDMX = -6 * 60; // -6 horas en minutos
    const utcOffset = fechaObj.getTimezoneOffset(); // Offset local en minutos
    const totalOffset = offsetCDMX + utcOffset; // Diferencia entre local y CDMX
    
    const fechaObjCDMX = new Date(fechaObj.getTime() + totalOffset * 60000);
    
    // Verificar si es del mismo día (hoy en CDMX)
    return (
      fechaCDMX.getFullYear() === fechaObjCDMX.getFullYear() &&
      fechaCDMX.getMonth() === fechaObjCDMX.getMonth() &&
      fechaCDMX.getDate() === fechaObjCDMX.getDate()
    );
  } catch (e) {
    console.error('Error al procesar fecha:', e);
    return false;
  }
}

// Función auxiliar para obtener la URL de imagen correcta
const obtenerUrlImagen = (props) => {
  const API_BASE_URL = 'https://apipwa.sembrandodatos.com';
  
  console.log('🔍 Obteniendo imagen para props:', props);
  
  // Función para construir URL completa
  const construirURL = (path) => {
    if (!path) return null;
    // Si ya es una URL completa, devolverla tal como está
    if (path.startsWith('http')) return path;
    // Si ya tiene la base URL, devolverla tal como está
    if (path.startsWith(API_BASE_URL)) return path;
    // Asegurar que no haya doble slash
    const cleanPath = path.startsWith('/') ? path.slice(1) : path;
    return `${API_BASE_URL}/${cleanPath}`;
  };
  
  // Prioridad 1: Tipo específico de actividad
  if (props.tipo_actividad === 'entrada') {
    if (props.foto_entrada_url) {
      const url = construirURL(props.foto_entrada_url);
      console.log('✅ Imagen entrada encontrada:', url);
      return url;
    }
  } else if (props.tipo_actividad === 'salida') {
    if (props.foto_salida_url) {
      const url = construirURL(props.foto_salida_url);
      console.log('✅ Imagen salida encontrada:', url);
      return url;
    }
  }
  
  // Prioridad 2: Campos de imagen generales
  const camposImagen = [
    'foto_url',
    'imagen_url', 
    'imagen',
    'photo_url',
    'picture_url',
    'foto',
    'picture'
  ];
  
  for (const campo of camposImagen) {
    if (props[campo]) {
      const url = construirURL(props[campo]);
      console.log(`✅ Imagen encontrada en campo '${campo}':`, url);
      return url;
    }
  }
  
  // Prioridad 3: Verificar si hay alguna propiedad que contenga 'foto' o 'imagen'
  for (const [key, value] of Object.entries(props)) {
    if (value && typeof value === 'string' && 
        (key.toLowerCase().includes('foto') || key.toLowerCase().includes('imagen') || 
         key.toLowerCase().includes('photo') || key.toLowerCase().includes('picture'))) {
      const url = construirURL(value);
      console.log(`✅ Imagen encontrada en campo dinámico '${key}':`, url);
      return url;
    }
  }
  
  console.log('❌ No se encontró imagen en:', Object.keys(props));
  return null;
}

// Función para formatear el tipo de actividad para mostrar en el popup
const formatearTipoActividad = (tipoActividad) => {
  if (!tipoActividad) return 'REGISTRO';
  
  // Limpiar sufijos como -hoy, -antiguo, etc.
  let tipoLimpio = tipoActividad.toLowerCase();
  
  // Remover sufijos comunes
  tipoLimpio = tipoLimpio.replace(/-hoy$/, '');
  tipoLimpio = tipoLimpio.replace(/-antiguo$/, '');
  tipoLimpio = tipoLimpio.replace(/^registro-/, ''); // Para casos como "registro-hoy"
  
  let resultado;
  switch (tipoLimpio) {
    case 'campo':
      resultado = 'CAMPO';
      break;
    case 'gabinete':
      resultado = 'GABINETE';
      break;
    case 'oficina':
      resultado = 'OFICINA';
      break;
    case 'registro':
      resultado = 'REGISTRO';
      break;
    case 'entrada':
      resultado = 'ENTRADA';
      break;
    case 'salida':
      resultado = 'SALIDA';
      break;
    case 'hoy':
      resultado = 'REGISTRO';
      break;
    case 'antiguo':
      resultado = 'REGISTRO';
      break;
    default:
      resultado = tipoLimpio.toUpperCase();
  }
  
  return resultado;
}

// Función para obtener la clase CSS correcta para el tipo de actividad
const obtenerClaseTipoActividad = (tipoActividad) => {
  if (!tipoActividad) return 'registro';
  
  // Limpiar sufijos como -hoy, -antiguo, etc.
  let tipoLimpio = tipoActividad.toLowerCase();
  tipoLimpio = tipoLimpio.replace(/-hoy$/, '');
  tipoLimpio = tipoLimpio.replace(/-antiguo$/, '');
  tipoLimpio = tipoLimpio.replace(/^registro-/, '');
  
  switch (tipoLimpio) {
    case 'campo':
      return 'campo';
    case 'gabinete':
      return 'gabinete';
    case 'oficina':
      return 'oficina';
    case 'entrada':
      return 'entrada';
    case 'salida':
      return 'salida';
    case 'hoy':
    case 'antiguo':
    case 'registro':
      return 'registro';
    default:
      return 'registro';
  }
}

// Función para generar títulos amigables en los popups
const generarTituloPopup = (tipoActividad, tipoClase) => {
  console.log('📝 Generando título para:', tipoActividad, 'clase:', tipoClase);
  
  // Priorizar el tipo original (tipoActividad) sobre la clase técnica
  if (tipoActividad) {
    const tipoLower = tipoActividad.toLowerCase();
    console.log('🔍 Procesando tipoActividad:', tipoLower);
    
    switch (tipoLower) {
      case 'entrada':
        console.log('✅ Devolviendo: Entrada');
        return 'Entrada';
      case 'salida':
        console.log('✅ Devolviendo: Salida');
        return 'Salida';
      case 'campo':
        console.log('✅ Devolviendo: Actividad de Campo');
        return 'Actividad de Campo';
      case 'gabinete':
        console.log('✅ Devolviendo: Actividad de Gabinete');
        return 'Actividad de Gabinete';
      case 'oficina':
        console.log('✅ Devolviendo: Actividad de Oficina');
        return 'Actividad de Oficina';
      case 'registro':
        console.log('✅ Devolviendo: Registro de Actividad');
        return 'Registro de Actividad';
      default:
        console.log('⚠️ Tipo no reconocido, usando capitalizado:', tipoActividad);
        return tipoActividad.charAt(0).toUpperCase() + tipoActividad.slice(1);
    }
  }
  
  // Fallback a tipoClase si no hay tipoActividad
  if (tipoClase) {
    console.log('🔍 Procesando tipoClase:', tipoClase);
    switch (tipoClase.toLowerCase()) {
      case 'entrada':
        return 'Entrada';
      case 'salida':
        return 'Salida';
      case 'campo':
      case 'campo-hoy':
        console.log('✅ Devolviendo: Actividad de Campo (desde tipoClase)');
        return 'Actividad de Campo';
      case 'gabinete':
      case 'gabinete-hoy':
        console.log('✅ Devolviendo: Actividad de Gabinete (desde tipoClase)');
        return 'Actividad de Gabinete';
      case 'registro-hoy':
        return 'Registro de Hoy';
      case 'registro-antiguo':
      case 'antiguo':
        return 'Registro Anterior';
      default:
        console.log('⚠️ tipoClase no reconocido:', tipoClase);
        return 'Actividad';
    }
  }
  
  console.log('❌ No hay tipo disponible, devolviendo: Actividad');
  return 'Actividad';
}

// Función para manejar el clic en "Ver más detalles" en el popup
const toggleDetallesRegistro = () => {
  popupData.value.expandido = !popupData.value.expandido;
  console.log('Toggle detalles:', popupData.value.expandido ? 'Expandido' : 'Contraído');
}

// Función para manejar errores de carga de imagen
const onImageError = (event) => {
  console.log('❌ Error al cargar imagen:', event.target.src);
  console.log('📋 Datos originales del registro:', popupData.value.datosOriginales);
  
  // Intentar con URL alternativa si está disponible
  const props = popupData.value.datosOriginales;
  if (props) {
    const urlAlternativa = obtenerImagenAlternativa(props, event.target.src);
    if (urlAlternativa && urlAlternativa !== event.target.src) {
      console.log('🔄 Intentando con URL alternativa:', urlAlternativa);
      event.target.src = urlAlternativa;
      return;
    }
  }
  
  // Si no hay alternativa, ocultar imagen y mostrar placeholder
  event.target.style.display = 'none';
  popupData.value.imagenUrl = null;
}

// Función para obtener URL de imagen alternativa
const obtenerImagenAlternativa = (props, urlFallida) => {
  const API_BASE_URL = 'https://apipwa.sembrandodatos.com';
  
  // Lista de campos alternativos para probar
  const camposAlternativos = [
    'foto_url',
    'imagen_url',
    'imagen',
    'photo_url',
    'picture_url',
    'foto',
    'foto_entrada_url',
    'foto_salida_url'
  ];
  
  for (const campo of camposAlternativos) {
    if (props[campo]) {
      let urlAlternativa = props[campo];
      
      // Construir URL completa si es necesario
      if (!urlAlternativa.startsWith('http')) {
        const cleanPath = urlAlternativa.startsWith('/') ? urlAlternativa.slice(1) : urlAlternativa;
        urlAlternativa = `${API_BASE_URL}/${cleanPath}`;
      }
      
      // Si esta URL es diferente a la que falló, intentar con ella
      if (urlAlternativa !== urlFallida) {
        return urlAlternativa;
      }
    }
  }
  
  return null;
}

// Función para manejar carga exitosa de imagen  
const onImageLoad = (event) => {
  console.log('Imagen cargada correctamente:', event.target.src);
}

// Función para abrir imagen en modal completo
const abrirImagenCompleta = () => {
  if (popupData.value.imagenUrl) {
    imagenCompletaUrl.value = popupData.value.imagenUrl;
    mostrarImagenCompleta.value = true;
    console.log('🖼️ Abriendo imagen completa:', imagenCompletaUrl.value);
    
    // Agregar listener para la tecla Escape
    document.addEventListener('keydown', handleEscapeKey);
  }
}

// Función para cerrar modal de imagen completa
const cerrarImagenCompleta = () => {
  mostrarImagenCompleta.value = false;
  imagenCompletaUrl.value = '';
  console.log('❌ Cerrando imagen completa');
  
  // Remover listener de la tecla Escape
  document.removeEventListener('keydown', handleEscapeKey);
}

// Función para manejar la tecla Escape
const handleEscapeKey = (event) => {
  if (event.key === 'Escape' && mostrarImagenCompleta.value) {
    cerrarImagenCompleta();
  }
}

// Función para cerrar el popup cuando se hace clic en el botón X
const cerrarPopup = () => {
  console.log('Cerrando popup mediante botón X');
  showCustomPopup.value = false;
  // Resetear el estado expandido
  popupData.value.expandido = false;
}

// Función para aplicar filtros y actualizar las capas del mapa
const aplicarFiltros = () => {
  if (!map || !puntosSource) return

  try {
    console.log('🎛️ Aplicando clasificador:', { filtroTipo: filtroTipo.value })
    
    // Obtener las últimas actividades con los filtros aplicados
    const registrosFiltrados = filtrarRegistros()
    const actividadesFiltradas = obtenerUltimasActividadesPorUsuario(registrosFiltrados, asistencias.value)
    
    // Filtrar por tipo de actividad si está especificado
    let actividadesFinales = actividadesFiltradas
    if (filtroTipo.value) {
      actividadesFinales = actividadesFiltradas.filter(actividad => {
        const tipoActividad = determinarTipoActividad(actividad)
        
        switch (filtroTipo.value) {
          case 'entrada':
            return tipoActividad.tipo === 'entrada'
          case 'salida':
            return tipoActividad.tipo === 'salida'
          case 'campo-hoy':
            return tipoActividad.tipo === 'campo-hoy'
          case 'gabinete-hoy':
            return tipoActividad.tipo === 'gabinete-hoy'
          case 'actividades-generales':
            // Para actividades generales, incluir campo y gabinete del día actual
            return tipoActividad.tipo === 'campo-hoy' || tipoActividad.tipo === 'gabinete-hoy'
          case 'registro-hoy':
            return tipoActividad.tipo === 'registro-hoy' || tipoActividad.tipo === 'campo-hoy' || tipoActividad.tipo === 'gabinete-hoy'
          case 'registro-antiguo':
            return tipoActividad.tipo === 'registro-antiguo' || tipoActividad.tipo === 'campo-antiguo' || tipoActividad.tipo === 'gabinete-antiguo'
          default:
            return true
        }
      })
    }
    
    // Actualizar el mapa con los datos filtrados
    actualizarPuntosMapa(actividadesFinales)
    
    console.log(`✅ Clasificador aplicado. Puntos visibles: ${actividadesFinales.length}`)
    
  } catch (error) {
    console.error('❌ Error al aplicar clasificador:', error)
  }
}

// Función para filtrar registros según criterios
const filtrarRegistros = () => {
  // Como ya no tenemos filtro de período, simplemente devolvemos todos los registros
  return [...registros.value]
}

// Función para mostrar/ocultar filtros
const toggleFiltros = () => {
  mostrarFiltros.value = !mostrarFiltros.value
}

// Recargar mapa y datos
const recargarMapa = async () => {
  console.log('🔄 Solicitud de recarga del mapa...')
  
  // Si hay un error grave, reiniciar completamente el mapa
  if (error.value && error.value.includes('token')) {
    // Destruir el mapa actual si existe
    if (map) {
      try {
        map.remove();
        map = null;
        puntosSource = null;
        mapInitialized.value = false;
      } catch (e) {
        console.error('Error al destruir el mapa:', e);
      }
    }
    
    // Limpiar el error y reiniciar
    error.value = '';
    console.log('Reiniciando el mapa con token proporcionado');
    
    // Asegurar que estamos usando el token proporcionado
    mapboxgl.accessToken = 'pk.eyJ1IjoibWFyaWVsMDgiLCJhIjoiY202emV3MDhhMDN6YjJscHVqaXExdGpjMyJ9.F_ACoKzS_4e280lD0XndEw';
  }
  
  // Resetear los controles de carga para permitir una recarga inmediata
  cargaEnProceso = false
  ultimaCarga = 0
  
  // Cargar los datos nuevamente
  await cargarDatos();
  
  // También recargar el total de usuarios
  await cargarTotalUsuarios().catch(err => {
    console.error('⚠️ Error al recargar total de usuarios (no crítico):', err)
  });
  
  console.log('✅ Recarga del mapa completada')
}

// Función de cierre de sesión
const logout = () => {
  localStorage.removeItem('admin_token');
  localStorage.removeItem('admin_user');
  router.push('/login');
}

// Ciclo de vida del componente
onMounted(async () => {
  console.log('🚀 VisorMap iniciando...')
  
  // Asegurar que el CSS de Mapbox esté cargado (por si falla la importación en el estilo)
  const addMapboxCSS = () => {
    if (!document.getElementById('mapbox-gl-css')) {
      const link = document.createElement('link');
      link.id = 'mapbox-gl-css';
      link.rel = 'stylesheet';
      link.href = 'https://api.mapbox.com/mapbox-gl-js/v2.14.1/mapbox-gl.css';
      document.head.appendChild(link);
      console.log('CSS de Mapbox cargado dinámicamente');
    }
  };
  
  addMapboxCSS();
  
  // Esperar un poco para que el DOM esté completamente listo
  await new Promise(resolve => setTimeout(resolve, 100))
  
  // Cargar datos y mapa
  await cargarDatos();
  
  // Escuchar cambios de conexión
  const handleOnline = () => {
    console.log('🌐 Conexión restablecida')
    isOnline.value = true;
  };
  
  const handleOffline = () => {
    console.log('🚫 Conexión perdida')
    isOnline.value = false;
  };
  
  window.addEventListener('online', handleOnline);
  window.addEventListener('offline', handleOffline);
  
  console.log('✅ VisorMap inicializado completamente')
});

onUnmounted(() => {
  // Destruir el mapa para liberar recursos
  if (map) {
    map.remove();
    map = null;
  }
  
  // Limpiar listeners
  window.removeEventListener('online', () => {});
  window.removeEventListener('offline', () => {});
});

// Watcher para aplicar clasificador automáticamente cuando cambie
watch(filtroTipo, () => {
  if (map && mapInitialized.value) {
    aplicarFiltros()
  }
})
</script>

<style scoped>
/* Importación de fuentes */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');

/* Estilos principales */
.visor-map-container {
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, #f0f2f5 0%, #e8f5e8 100%);
  font-family: 'Inter', 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  overflow: hidden;
}

.main-content {
  flex: 1;
  margin-left: min(220px, 18vw);
  width: calc(100vw - min(220px, 18vw));
  background: transparent;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 100vh;
  padding: 0;
  box-sizing: border-box;
  position: relative;
  z-index: 1;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Header con diseño de vidrio líquido verde responsivo */
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

/* Efecto de patrón sutil */
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

/* Estado de conexión con vidrio líquido */
.connection-status {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  border-radius: 16px;
  font-size: clamp(9px, 0.8vw, 11px);
  font-weight: 600;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(12px) saturate(150%);
  -webkit-backdrop-filter: blur(12px) saturate(150%);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
  min-height: clamp(20px, 3vw, 26px);
}

.connection-status:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.online {
  color: rgba(255, 255, 255, 0.95);
}

.offline {
  color: rgba(255, 230, 230, 0.95);
}

.status-indicator {
  width: clamp(6px, 1vw, 8px);
  height: clamp(6px, 1vw, 8px);
  border-radius: 50%;
  transition: all 0.2s ease;
}

.online .status-indicator {
  background-color: #34d399;
  box-shadow: 
    0 0 8px rgba(52, 211, 153, 0.6),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  animation: pulseOnline 2s ease-in-out infinite;
}

.offline .status-indicator {
  background-color: #f87171;
  box-shadow: 
    0 0 8px rgba(248, 113, 113, 0.6),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  animation: pulseOffline 1.5s ease-in-out infinite;
}

@keyframes pulseOnline {
  0%, 100% { 
    box-shadow: 
      0 0 8px rgba(52, 211, 153, 0.6),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }
  50% { 
    box-shadow: 
      0 0 15px rgba(52, 211, 153, 0.8),
      inset 0 1px 0 rgba(255, 255, 255, 0.4);
  }
}

@keyframes pulseOffline {
  0%, 100% { 
    box-shadow: 
      0 0 8px rgba(248, 113, 113, 0.6),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }
  50% { 
    box-shadow: 
      0 0 12px rgba(248, 113, 113, 0.8),
      inset 0 1px 0 rgba(255, 255, 255, 0.4);
  }
}

/* Contador LCD con vidrio líquido */
.lcd-counter {
  background: linear-gradient(135deg, 
    rgba(0, 0, 0, 0.25) 0%, 
    rgba(0, 0, 0, 0.35) 50%,
    rgba(0, 0, 0, 0.3) 100%);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  padding: 4px 8px;
  backdrop-filter: blur(15px) saturate(120%);
  -webkit-backdrop-filter: blur(15px) saturate(120%);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 
    inset 0 1px 3px rgba(0, 0, 0, 0.4),
    0 2px 8px rgba(0, 0, 0, 0.1),
    0 1px 0 rgba(255, 255, 255, 0.1);
  min-height: clamp(20px, 3vw, 26px);
}

.lcd-counter:hover {
  background: linear-gradient(135deg, 
    rgba(0, 0, 0, 0.3) 0%, 
    rgba(0, 0, 0, 0.4) 50%,
    rgba(0, 0, 0, 0.35) 100%);
  transform: translateY(-1px);
  box-shadow: 
    inset 0 1px 3px rgba(0, 0, 0, 0.5),
    0 4px 12px rgba(0, 0, 0, 0.15),
    0 1px 0 rgba(255, 255, 255, 0.15);
}

.lcd-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1px;
}

.lcd-label {
  font-size: clamp(7px, 0.6vw, 9px);
  font-weight: 700;
  color: rgba(255, 255, 255, 0.7);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  text-shadow: 0 1px 1px rgba(0, 0, 0, 0.5);
}

.lcd-number {
  font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
  font-size: clamp(11px, 1.2vw, 15px);
  font-weight: 700;
  color: #34d399;
  letter-spacing: 0.05em;
  text-shadow: 
    0 0 10px rgba(52, 211, 153, 0.8),
    0 0 20px rgba(52, 211, 153, 0.4);
  animation: digitalGlow 3s ease-in-out infinite alternate;
}

@keyframes digitalGlow {
  0% {
    text-shadow: 
      0 0 10px rgba(52, 211, 153, 0.8),
      0 0 20px rgba(52, 211, 153, 0.4);
  }
  100% {
    text-shadow: 
      0 0 15px rgba(52, 211, 153, 1),
      0 0 30px rgba(52, 211, 153, 0.6),
      0 0 40px rgba(52, 211, 153, 0.2);
  }
}

/* Botón de actualización con vidrio líquido */
.refresh-btn-icon {
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
  min-width: auto;
  width: auto;
  height: auto;
}

.refresh-btn-icon::before {
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

.refresh-btn-icon:hover {
  transform: translateY(-2px);
  box-shadow: 
    inset 0 -1px 0 rgba(0, 0, 0, 0.15);
  border-color: rgba(255, 255, 255, 0.4);
}

.refresh-btn-icon:hover::before {
  opacity: 1;
}

.refresh-btn-icon svg {
  width: clamp(12px, 2vw, 14px);
  height: clamp(12px, 2vw, 14px);
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
  z-index: 1;
  position: relative;
  transition: all 0.3s ease;
}

.refresh-btn-icon:hover svg {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
  transform: scale(1.05);
}

.refresh-btn-icon:active {
  transform: translateY(-1px);
}

.refresh-btn-icon:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.refresh-icon {
  color: white;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  width: clamp(14px, 2vw, 16px);
  height: clamp(14px, 2vw, 16px);
  stroke-width: 2;
}

.refresh-btn-icon:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none;
  background: rgba(156, 163, 175, 0.3);
  backdrop-filter: blur(8px);
}

.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Contenido principal */
.page-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  background: transparent;
  position: relative;
  z-index: 1;
  display: flex;
  gap: 16px;
  height: calc(100vh - 60px); /* Altura completa menos el header */
}

/* Panel de control lateral */
.controles-panel {
  width: 260px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex-shrink: 0;
  overflow-y: auto;
  max-height: calc(100vh - 92px);
}

.panel-header {
  display: flex;
  flex-direction: column;
  gap: 10px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  padding-bottom: 12px;
}

.panel-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

/* Título centrado con efecto de luz verde */
.titulo-controles-centrado {
  text-align: center !important;
  color: #166534 !important; /* Verde fuerte */
  font-weight: 700 !important;
  font-size: 14px !important;
  position: relative;
  overflow: hidden;
  background: linear-gradient(90deg, 
    #166534 0%, 
    #166534 40%, 
    #22c55e 50%, 
    #166534 60%, 
    #166534 100%);
  background-size: 200% 100%;
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: luz-verde-deslizante 6s ease-in-out infinite;
}

@keyframes luz-verde-deslizante {
  0% {
    background-position: -200% 0;
  }
  50% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.btn-refresh {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
  background: linear-gradient(135deg, 
    rgba(46, 204, 113, 0.8) 0%, 
    rgba(39, 174, 96, 0.9) 50%,
    rgba(46, 204, 113, 0.8) 100%);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  border-radius: 25px;
  padding: 5px 8px;
  font-size: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 15px rgba(46, 204, 113, 0.2),
    0 2px 8px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  min-height: 30px;
}

.btn-refresh::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(255, 255, 255, 0.4), 
    transparent);
  transition: left 0.6s ease;
}

.btn-refresh:hover {
  background: linear-gradient(135deg, 
    rgba(39, 174, 96, 0.9) 0%, 
    rgba(46, 204, 113, 1) 50%,
    rgba(39, 174, 96, 0.9) 100%);
  transform: translateY(-1px) scale(1.02);
  box-shadow: 
    0 6px 20px rgba(46, 204, 113, 0.3),
    0 4px 12px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.btn-refresh:hover::before {
  left: 100%;
}

.btn-refresh:active {
  transform: translateY(0) scale(0.98);
  box-shadow: 
    0 2px 8px rgba(46, 204, 113, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.btn-refresh:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none;
  background: linear-gradient(135deg, 
    rgba(156, 163, 175, 0.6) 0%, 
    rgba(107, 114, 128, 0.7) 100%);
  backdrop-filter: blur(10px);
}

/* Animación de rotación para el icono de recarga */
.btn-refresh svg {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: center;
  will-change: transform;
}

.btn-refresh.loading svg {
  animation: refreshSpin 0.8s linear infinite;
}

.btn-refresh.loading:hover svg {
  animation: refreshSpin 0.6s linear infinite;
}

@keyframes refreshSpin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Mejoras de rendimiento para la animación */
.btn-refresh.loading {
  pointer-events: none;
}

.btn-refresh.loading::before {
  display: none;
}

.panel-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.panel-section h4 {
  margin: 0;
  font-size: 12px;
  font-weight: 600;
  color: #1f2937;
}

/* Estado del mapa */
.error-message {
  background-color: #fee2e2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 10px;
}

.error-message p {
  color: #dc2626;
  font-size: 12px;
  margin: 0 0 8px 0;
}

.retry-btn-small {
  background-color: #dc2626;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.2s;
}

.retry-btn-small:hover {
  background-color: #b91c1c;
}

.status-message {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.status-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  max-width: fit-content;
}

.status-badge-small {
  display: inline-block;
  padding: 2px 6px;
  border-radius: 8px;
  font-size: 10px;
  font-weight: 500;
  max-width: fit-content;
}

.status-badge.loading,
.status-badge-small.loading {
  background-color: #dbeafe;
  color: #1e40af;
}

.loading-dots::after {
  content: '';
  animation: dots 1.5s steps(4, end) infinite;
}

@keyframes dots {
  0%, 20% { content: ''; }
  40% { content: '.'; }
  60% { content: '..'; }
  80%, 100% { content: '...'; }
}

.status-badge.success {
  background-color: #dcfce7;
  color: #15803d;
}

.status-info {
  font-size: 12px;
  color: #6b7280;
  margin: 0;
}

.status-info-ubicaciones {
  font-size: 10px;
  color: #1e40af;
  font-weight: 600;
  margin: 0;
  margin-top: -4px;
}

/* Estadísticas */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 6px;
}

.stat-item {
  background: #f9fafb;
  padding: 6px 8px;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 10px;
  color: #6b7280;
}

.stat-value {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.stat-value.entrada {
  color: rgb(0, 0, 205); /* Mediumblue para entradas */
}

.stat-value.salida {
  color: #e53e3e;
}

.stat-value.campo {
  color: rgb(50, 205, 50); /* Limegreen para campo */
}

.stat-value.gabinete {
  color: rgb(255, 140, 0); /* Darkorange para gabinete */
}

.stat-value.actividades-total {
  color: rgb(148, 0, 211); /* Darkviolet para actividades total */
  font-weight: 700; /* Hacer más destacado */
}

.stat-value.hoy {
  color: #1e40af;
}

.stat-value.antiguo {
  color: #f59e0b;
}

/* Leyenda del mapa */
.leyenda-container {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 12px;
  box-shadow: 
    0 4px 15px rgba(0, 0, 0, 0.1),
    0 2px 8px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.leyenda-container:hover {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 
    0 6px 20px rgba(0, 0, 0, 0.15),
    0 3px 12px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
}

.leyenda-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 4px;
}

.leyenda-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  padding: 1px 0;
}

.color-marker {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.color-marker.entrada {
  background-color: rgb(0, 0, 205); /* Mediumblue para entrada */
}

.color-marker.salida {
  background-color: rgb(220, 20, 60); /* Crimson para salida */
}

.color-marker.campo-hoy {
  background-color: rgb(50, 205, 50); /* Limegreen para campo */
}

.color-marker.gabinete-hoy {
  background-color: rgb(255, 140, 0); /* Darkorange para gabinete */
}

.color-marker.actividades-generales {
  background-color: rgb(148, 0, 211); /* darkviolet para actividades generales */
}

.color-marker.registro-hoy {
  background-color: #00BFFF; /* Para compatibilidad */
}

.color-marker.registro-antiguo {
  background-color: rgb(192, 192, 192); /* Silver para registros antiguos */
}

/* Subtítulo en la leyenda */
.leyenda-subtitle {
  grid-column: 1 / -1;
  margin: 4px 0 4px 0;
  padding: 6px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  position: relative;
  background: linear-gradient(90deg, 
    rgba(128, 128, 128, 0.15) 0%, 
    rgba(128, 128, 128, 0.25) 50%, 
    rgba(128, 128, 128, 0.15) 100%
  );
  border-radius: 4px;
}

.leyenda-subtitle:first-child {
  margin-top: 0;
  border-top: none;
}

.leyenda-subtitle h5 {
  margin: 0;
  font-size: 0.6rem;
  font-weight: 500;
  color: #B0BEC5;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  opacity: 0.9;
  text-align: center;
}

/* Ayuda */
.help-text {
  font-size: 10px;
  color: #6b7280;
}

.help-text p {
  margin: 3px 0;
}

/* Contenedor del mapa */
.mapa-container {
  flex: 1;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  position: relative;
  min-height: 600px;
  height: 100%;
}

.mapa-area {
  width: 100%;
  height: 100%;
  position: relative;
  z-index: 1;
}

/* Indicadores de carga y error */
.loading-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(4px);
  z-index: 2;
}

.spinner-large {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(46, 204, 113, 0.2);
  border-radius: 50%;
  border-top-color: #2ecc71;
  animation: spin 1s linear infinite;
  margin-bottom: 12px;
}

.error-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.9);
  z-index: 2;
  padding: 20px;
  text-align: center;
}

.error-container p {
  color: #e53e3e;
  margin-bottom: 16px;
  max-width: 400px;
}

.retry-btn {
  padding: 8px 16px;
  background: #2ecc71;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  background: #27ae60;
  transform: translateY(-2px);
}

/* Estilos específicos para Mapbox */
@import url('https://api.mapbox.com/mapbox-gl-js/v2.14.1/mapbox-gl.css');

/* Personalización de popups personalizados */
.custom-popup {
  position: absolute;
  width: 100%;
  max-width: 300px;
  min-width: 250px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  z-index: 10;
  transform: translate(-50%, -100%);
  pointer-events: auto;
  font-family: 'Inter', 'Poppins', sans-serif;
  overflow: visible; /* Permite que la flecha sea visible */
  opacity: 1;
  transition: all 0.3s ease-in-out;
  /* Asegurar que no se salga de la pantalla */
  left: clamp(5px, 50%, calc(100vw - 305px));
  word-wrap: break-word;
  overflow-wrap: break-word;
}

/* Popup expandido - dimensiones rectangulares */
.custom-popup:has(.popup-expanded-content) {
  max-width: 650px;
  min-width: 600px;
  width: auto;
}

/* Colores dinámicos según tipo de registro */
.custom-popup.popup-entrada {
  background-color: #f0f0ff;
  border: 1px solid rgba(0, 0, 205, 0.3);
}

.custom-popup.popup-salida {
  background-color: #fff5f5;
  border: 1px solid rgba(220, 20, 60, 0.3);
}

.custom-popup.popup-campo-hoy {
  background-color: #f0fff0;
  border: 1px solid rgba(50, 205, 50, 0.3);
}

.custom-popup.popup-gabinete-hoy {
  background-color: #fff8dc;
  border: 1px solid rgba(255, 140, 0, 0.3);
}

.custom-popup.popup-registro-hoy {
  background-color: #f0fdf4;
  border: 1px solid rgba(22, 163, 74, 0.3);
}

.custom-popup.popup-registro-antiguo, 
.custom-popup.popup-antiguo,
.custom-popup.popup-campo-antiguo,
.custom-popup.popup-gabinete-antiguo {
  background-color: #f8f8f8;
  border: 1px solid rgba(192, 192, 192, 0.5);
}

/* Estilos para la flecha indicadora */
.popup-arrow {
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 16px;
  height: 8px;
  overflow: hidden;
}

.popup-arrow::after {
  content: '';
  position: absolute;
  width: 12px;
  height: 12px;
  transform: translateY(-50%) rotate(45deg);
  top: 0;
  left: 2px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

/* Colores de la flecha según el tipo */
.popup-entrada .popup-arrow::after {
  background-color: #f0f0ff;
  border-right: 1px solid rgba(0, 0, 205, 0.3);
  border-bottom: 1px solid rgba(0, 0, 205, 0.3);
}

.popup-salida .popup-arrow::after {
  background-color: #fff5f5;
  border-right: 1px solid rgba(220, 20, 60, 0.3);
  border-bottom: 1px solid rgba(220, 20, 60, 0.3);
}

.popup-campo-hoy .popup-arrow::after {
  background-color: #f0fff0;
  border-right: 1px solid rgba(50, 205, 50, 0.3);
  border-bottom: 1px solid rgba(50, 205, 50, 0.3);
}

.popup-gabinete-hoy .popup-arrow::after {
  background-color: #fff8dc;
  border-right: 1px solid rgba(255, 140, 0, 0.3);
  border-bottom: 1px solid rgba(255, 140, 0, 0.3);
}

.popup-registro-hoy .popup-arrow::after {
  background-color: #f0fdf4;
  border-right: 1px solid rgba(22, 163, 74, 0.3);
  border-bottom: 1px solid rgba(22, 163, 74, 0.3);
}

.popup-registro-antiguo .popup-arrow::after,
.popup-antiguo .popup-arrow::after,
.popup-campo-antiguo .popup-arrow::after,
.popup-gabinete-antiguo .popup-arrow::after {
  background-color: #f8f8f8;
  border-right: 1px solid rgba(192, 192, 192, 0.5);
  border-bottom: 1px solid rgba(192, 192, 192, 0.5);
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 14px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.popup-header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.popup-title {
  display: flex;
  align-items: center;
  gap: 6px;
}

.popup-close-btn {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.05);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  padding: 0;
  transition: background-color 0.2s;
}

.popup-close-btn:hover {
  background: rgba(0, 0, 0, 0.1);
}

.popup-close-btn svg {
  width: 14px;
  height: 14px;
  color: rgba(0, 0, 0, 0.5);
}

/* Estilos específicos para el botón X en cada tipo de popup */
.popup-entrada .popup-close-btn:hover svg {
  color: rgb(0, 0, 205); /* Mediumblue */
}

.popup-salida .popup-close-btn:hover svg {
  color: rgb(220, 20, 60);
}

.popup-campo-hoy .popup-close-btn:hover svg {
  color: rgb(50, 205, 50); /* Limegreen para campo */
}

.popup-gabinete-hoy .popup-close-btn:hover svg {
  color: rgb(255, 140, 0); /* Darkorange para gabinete */
}

.popup-registro-hoy .popup-close-btn:hover svg {
  color: #15803D; /* Verde fuerte por defecto */
}

.popup-registro-antiguo .popup-close-btn:hover svg,
.popup-antiguo .popup-close-btn:hover svg,
.popup-campo-antiguo .popup-close-btn:hover svg,
.popup-gabinete-antiguo .popup-close-btn:hover svg {
  color: rgb(192, 192, 192); /* Silver */
}

.popup-icon {
  width: 18px;
  height: 18px;
}

.popup-icon-small {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

/* Colores de iconos y texto según tipo */
.popup-entrada .popup-icon,
.popup-entrada .popup-icon-small,
.popup-entrada strong {
  color: rgb(0, 0, 205); /* Mediumblue */
}

.popup-salida .popup-icon,
.popup-salida .popup-icon-small,
.popup-salida strong {
  color: rgb(220, 20, 60);
}

.popup-campo-hoy .popup-icon,
.popup-campo-hoy .popup-icon-small,
.popup-campo-hoy strong {
  color: rgb(50, 205, 50); /* Limegreen para campo */
}

.popup-gabinete-hoy .popup-icon,
.popup-gabinete-hoy .popup-icon-small,
.popup-gabinete-hoy strong {
  color: rgb(255, 140, 0); /* Darkorange para gabinete */
}

.popup-registro-hoy .popup-icon,
.popup-registro-hoy .popup-icon-small,
.popup-registro-hoy strong {
  color: #15803D; /* Verde fuerte por defecto */
}

.popup-registro-antiguo .popup-icon,
.popup-registro-antiguo .popup-icon-small,
.popup-antiguo .popup-icon,
.popup-antiguo .popup-icon-small,
.popup-campo-antiguo .popup-icon,
.popup-campo-antiguo .popup-icon-small,
.popup-gabinete-antiguo .popup-icon,
.popup-gabinete-antiguo .popup-icon-small,
.popup-registro-antiguo strong,
.popup-antiguo strong,
.popup-campo-antiguo strong,
.popup-gabinete-antiguo strong {
  color: rgb(192, 192, 192); /* Silver */
}

.popup-header strong {
  font-size: 14px;
  font-weight: 600;
}

.popup-fecha {
  font-size: 11px;
  font-weight: 500;
  color: rgba(107, 114, 128, 0.8);
  background-color: rgba(0, 0, 0, 0.04);
  padding: 2px 8px;
  border-radius: 12px;
}

.popup-body {
  padding: 12px 14px;
}

.popup-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.popup-row:last-child {
  margin-bottom: 0;
}

.popup-datetime-section {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.popup-datetime-section .popup-row {
  margin-bottom: 6px;
}

.popup-usuario {
  font-weight: 500;
  font-size: 14px;
  color: #111827;
}

.popup-correo {
  margin-top: 3px;
}

.popup-correo-texto {
  font-weight: 400;
  font-size: 10px;
  color: #6b7280;
  font-style: italic;
  line-height: 1.2;
  word-break: break-all;
  overflow: hidden;
  text-overflow: ellipsis;
}

.popup-email {
  font-weight: 400;
  font-size: 11px;
  color: #6b7280;
  margin-top: 2px;
  margin-left: 24px; /* Alinea con el texto del usuario */
  font-style: italic;
}

.popup-coordenadas {
  font-size: 11px;
  font-family: monospace;
  color: #6b7280;
}

.popup-fecha {
  font-size: 12px;
  color: #374151;
  font-weight: 500;
}

.popup-hora {
  font-size: 12px;
  color: #374151;
  font-weight: 500;
  font-family: monospace;
}

.popup-footer {
  padding: 12px 14px;
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.popup-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  background-color: rgba(0, 0, 0, 0.04);
  border: none;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
  transition: background-color 0.2s;
}

.popup-btn:hover {
  background-color: rgba(0, 0, 0, 0.08);
}

.popup-btn-icon {
  width: 16px;
  height: 16px;
}

/* Estilos para contenido expandido */
.popup-expanded-content {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  animation: expandContent 0.3s ease-out;
}

/* Layout de dos columnas para popup expandido */
.popup-expanded-layout {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  min-height: 200px;
}

.popup-info-column {
  flex: 1;
  width: 50%;
  min-width: 0;
}

.popup-image-column {
  flex: 1;
  width: 50%;
  display: flex;
  flex-direction: column;
}

@keyframes expandContent {
  from {
    opacity: 0;
    max-height: 0;
    padding-top: 0;
    margin-top: 0;
  }
  to {
    opacity: 1;
    max-height: 500px;
    padding-top: 12px;
    margin-top: 12px;
  }
}

.popup-image-section {
  margin-bottom: 16px;
}

/* Estilos para imagen compacta en layout de dos columnas */
.popup-image-section-compact {
  margin-bottom: 0;
}

.popup-image-container-compact {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100px;
  max-height: 120px;
  margin-bottom: 12px;
  transition: all 0.3s ease;
  position: relative;
}

.popup-image-container-compact:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.popup-image-container-compact::after {
  content: '🔍';
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.popup-image-container-compact:hover::after {
  opacity: 1;
}

.popup-image-compact {
  width: 100%;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
}

.popup-no-image-section-compact {
  margin-bottom: 0;
}

.popup-no-image-section-compact .popup-section-header {
  opacity: 0.6;
}

.popup-no-image-placeholder {
  width: 100%;
  height: 100px;
  background: #f9fafb;
  border: 2px dashed #d1d5db;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.popup-no-image-placeholder svg {
  width: 32px;
  height: 32px;
  color: #9ca3af;
  margin-bottom: 4px;
}

.no-image-text {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

/* Descripción con scroll en columna derecha */
.popup-description-section-compact {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.popup-description-scrollable {
  flex: 1;
  max-height: 100px;
  overflow-y: auto;
  padding: 10px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 12px;
  line-height: 1.4;
  color: #374151;
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 #f1f5f9;
}

.popup-description-scrollable::-webkit-scrollbar {
  width: 6px;
}

.popup-description-scrollable::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.popup-description-scrollable::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.popup-description-scrollable::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.popup-no-image-section {
  margin-bottom: 16px;
}

.popup-no-image-section .popup-section-header {
  opacity: 0.6;
}

.popup-description-section {
  margin-bottom: 16px;
}

.popup-description-content {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 10px 12px;
  margin-top: 8px;
  font-size: 12px;
  line-height: 1.5;
  color: #374151;
  font-style: italic;
  min-height: 20px;
}

.popup-description-content:empty::before {
  content: "Sin descripción disponible";
  color: #9ca3af;
  font-style: italic;
}

.popup-section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.popup-section-title {
  font-size: 12px;
  font-weight: 600;
  color: #374151;
}

.popup-image-container {
  width: 100%;
  max-width: 100%;
  border-radius: 8px;
  overflow: hidden;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 120px;
}

.popup-image {
  width: 100%;
  height: auto;
  max-height: 200px;
  object-fit: cover;
  border-radius: 8px;
}

.popup-details-grid {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.popup-detail-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 4px 0;
}

/* Estilo para fila de elementos en línea */
.popup-detail-row {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 0;
  flex-wrap: nowrap;
}

/* Estilo para elemento de mitad de ancho */
.popup-detail-half {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
  min-width: 0;
}

.popup-detail {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
  min-width: 0;
}

.popup-detail-label {
  font-size: 10px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.popup-detail-value {
  font-size: 12px;
  font-weight: 500;
  color: #111827;
  word-break: break-word;
}

/* Estilos específicos para Estado de conexión */
.status-value {
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

/* Estado Online */
.status-value.online {
  background-color: #dcfce7;
  color: #15803d;
  border: 1px solid #bbf7d0;
}

/* Estado Offline */
.status-value.offline {
  background-color: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

/* Estilos específicos para Coordenadas */
.coordinates-value {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  background-color: #eff6ff;
  color: #1d4ed8;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  border: 1px solid #dbeafe;
  letter-spacing: 0.05em;
}

/* Precisión GPS con estilo distintivo */
.precision-value {
  background-color: #fff7ed;
  color: #ea580c;
  padding: 3px 6px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  border: 1px solid #fed7aa;
}

/* Tipo de actividad con colores distintivos */
.tipo-actividad-value {
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.tipo-actividad-value.entrada {
  background-color: #f0f0ff;
  color: rgb(0, 0, 205); /* Mediumblue */
  border: 1px solid rgba(0, 0, 205, 0.3);
}

.tipo-actividad-value.salida {
  background-color: #fff5f5;
  color: rgb(220, 20, 60);
  border: 1px solid rgba(220, 20, 60, 0.3);
}

.tipo-actividad-value.campo {
  background-color: #f0fff0;
  color: rgb(50, 205, 50); /* Limegreen */
  border: 1px solid rgba(50, 205, 50, 0.3);
}

.tipo-actividad-value.gabinete {
  background-color: #fff8dc;
  color: rgb(255, 140, 0); /* Darkorange */
  border: 1px solid rgba(255, 140, 0, 0.3);
}

.tipo-actividad-value.oficina {
  background-color: #fef3c7;
  color: #92400e;
  border: 1px solid #fcd34d;
}

.tipo-actividad-value.registro {
  background-color: #f8f8f8;
  color: rgb(192, 192, 192); /* Silver */
  border: 1px solid rgba(192, 192, 192, 0.5);
}

/* Modal para imagen completa */
.image-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(5px);
  animation: fadeIn 0.3s ease-out;
}

.image-modal-container {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.image-modal-close {
  position: absolute;
  top: 15px;
  right: 15px;
  background: rgba(0, 0, 0, 0.7);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10001;
  transition: all 0.3s ease;
}

.image-modal-close:hover {
  background: rgba(0, 0, 0, 0.9);
  transform: scale(1.1);
}

.image-modal-close svg {
  width: 20px;
  height: 20px;
  color: white;
}

.image-modal-content {
  display: flex;
  flex-direction: column;
  max-height: 90vh;
}

.image-modal-img {
  max-width: 100%;
  max-height: 70vh;
  object-fit: contain;
  background: #f8f9fa;
}

.image-modal-info {
  padding: 20px;
  background: white;
  border-top: 1px solid #e9ecef;
}

.image-info-row {
  margin-bottom: 8px;
  font-size: 14px;
  line-height: 1.4;
}

.image-info-row:last-child {
  margin-bottom: 0;
}

.image-info-row strong {
  color: #495057;
  margin-right: 8px;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Responsive para el modal */
@media (max-width: 768px) {
  .image-modal-container {
    max-width: 95vw;
    max-height: 95vh;
  }
  
  .image-modal-img {
    max-height: 60vh;
  }
  
  .image-modal-info {
    padding: 15px;
  }
  
  .image-info-row {
    font-size: 13px;
  }
}

/* Adaptación para modo móvil */
@media (max-width: 768px) {
  .custom-popup {
    width: 90vw;
    max-width: 320px;
    min-width: 220px;
  }
  
  .custom-popup:has(.popup-expanded-content) {
    max-width: 350px;
    min-width: 300px;
  }
  
  .popup-correo-texto {
    font-size: 9px;
    max-width: 180px;
  }
  
  .popup-usuario {
    font-size: 13px;
  }
  
  .popup-coordenadas {
    font-size: 10px;
  }
  
  .popup-image-container {
    min-height: 100px;
  }
  
  .popup-image {
    max-height: 150px;
  }
  
  .popup-description-content {
    font-size: 11px;
    padding: 8px 10px;
  }
}

@media (max-width: 480px) {
  .custom-popup {
    width: 95vw;
    max-width: 300px;
    min-width: 200px;
  }
  
  .custom-popup:has(.popup-expanded-content) {
    max-width: 320px;
    min-width: 280px;
  }
  
  .popup-header {
    padding: 10px 12px;
  }
  
  .popup-body {
    padding: 10px 12px;
  }
  
  .popup-correo-texto {
    font-size: 8px;
    max-width: 160px;
  }
  
  .popup-usuario {
    font-size: 12px;
  }
  
  .popup-coordenadas {
    font-size: 9px;
  }
  
  .popup-fecha, .popup-hora {
    font-size: 11px;
  }
  
  .popup-image-container {
    min-height: 80px;
  }
  
  .popup-image {
    max-height: 120px;
  }
  
  .popup-detail-label {
    font-size: 9px;
  }
  
  .popup-detail-value {
    font-size: 11px;
  }
  
  .popup-description-content {
    font-size: 10px;
    padding: 6px 8px;
  }
}

/* Estilos para el tooltip de ayuda de zoom */
.mapbox-zoom-help {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1;
  pointer-events: none;
  animation: fadeInOut 5s forwards;
}

.zoom-help-tooltip {
  background-color: rgba(0, 0, 0, 0.75);
  color: white;
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

@keyframes fadeInOut {
  0% { opacity: 0; }
  10% { opacity: 1; }
  80% { opacity: 1; }
  100% { opacity: 0; }
}

.popup-header {
  padding: 10px 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.popup-header.entrada {
  background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
  color: white;
}

.popup-header.salida {
  background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%);
  color: white;
}

.popup-header.registro-hoy {
  background: linear-gradient(135deg, #4682B4 0%, #00BFFF 100%);
  color: white;
}

.popup-header.registro-antiguo {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.popup-header h4 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
}

.popup-fecha {
  font-size: 12px;
  opacity: 0.9;
}

.popup-body {
  padding: 12px 15px;
  background: white;
}

.popup-usuario {
  font-weight: 600;
  font-size: 13px;
  margin-bottom: 5px;
  color: #1f2937;
}

.popup-coordenadas {
  font-size: 11px;
  color: #4b5563;
  font-family: monospace;
}

/* Animación para los puntos del mapa */
@keyframes pulse {
  0% {
    transform: scale(0.8);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.2);
    opacity: 1;
  }
  100% {
    transform: scale(0.8);
    opacity: 0.8;
  }
}

.mapboxgl-ctrl-top-right {
  top: 60px !important;
}

.mapboxgl-ctrl-logo {
  opacity: 0.7;
}

/* Estilos para los controles de filtros compactos y modernos */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  padding: 2px 0;
  transition: all 0.2s ease;
}

.section-header-status {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 0px;
}

.section-header:hover {
  color: #2ecc71;
}

.toggle-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 50%;
  transition: all 0.3s ease;
  color: #6b7280;
}

.toggle-btn:hover {
  background: rgba(46, 204, 113, 0.1);
  color: #2ecc71;
}

.toggle-btn.rotated {
  transform: rotate(180deg);
}

.filter-controls-compact {
  margin-top: 8px;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  0% {
    opacity: 0;
    transform: translateY(-10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.filter-group-compact {
  background: linear-gradient(135deg, #f8fff9 0%, #f0fff4 100%);
  border: 1px solid rgba(76, 175, 80, 0.2);
  border-radius: 10px;
  padding: 12px;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.08);
  transition: all 0.3s ease;
}

.filter-group-compact:hover {
  border-color: rgba(76, 175, 80, 0.3);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.12);
  transform: translateY(-1px);
}

.filter-item-compact {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.filter-item-compact:last-child {
  margin-bottom: 0;
}

.filter-icon-small {
  color: #4CAF50;
  opacity: 0.8;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.filter-item-compact:hover .filter-icon-small {
  opacity: 1;
  transform: scale(1.1);
}

.compact-select {
  flex: 1;
  background: white;
  border: 1px solid rgba(76, 175, 80, 0.2);
  color: #2c3e50;
  font-size: 11px;
  font-weight: 500;
  cursor: pointer;
  padding: 6px 24px 6px 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
  outline: none;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%234CAF50' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 6px center;
  background-repeat: no-repeat;
  background-size: 12px;
}

.compact-select:hover {
  background-color: rgba(76, 175, 80, 0.03);
  border-color: rgba(76, 175, 80, 0.4);
}

.compact-select:focus {
  background-color: rgba(76, 175, 80, 0.05);
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.15);
}

.compact-select option {
  background: white;
  color: #2c3e50;
  padding: 6px 12px;
  font-weight: 500;
}

.compact-select option:hover {
  background: #f0fff4;
}

/* Responsive design para el header y sidebar */
@media (max-width: 992px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
  
  .lcd-counter {
    display: flex; /* Mantener visible en tablets */
  }
  
  .header-content {
    gap: clamp(0.2rem, 0.6vw, 0.4rem);
  }
  
  .header-actions {
    gap: clamp(5px, 0.6vw, 10px);
  }
}

@media (min-width: 481px) and (max-width: 768px) {
  .main-content {
    margin-left: 250px;
    width: calc(100vw - 250px);
  }
}

@media (max-width: 768px) and (orientation: landscape) {
  .main-content {
    margin-left: 160px;
    width: calc(100vw - 160px);
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 240px;
    width: calc(100vw - 240px);
  }
  
  .page-header {
    padding: clamp(0.25rem, 0.6vw, 0.4rem);
  }
  
  .header-content {
    flex-direction: row; /* Mantener horizontal */
    align-items: center;
    gap: clamp(0.2rem, 0.5vw, 0.3rem);
    justify-content: space-between;
  }
  
  .header-main {
    min-width: 100px;
    gap: clamp(0.2rem, 0.6vw, 0.4rem);
  }
  
  .header-actions {
    gap: clamp(4px, 0.5vw, 8px);
  }
  
  .lcd-counter {
    display: none; /* Ocultar en móviles para ahorrar espacio */
  }
  
  .connection-status {
    padding: 2px 6px;
    font-size: clamp(8px, 0.7vw, 10px);
  }
  
  .connection-status span {
    display: none; /* Solo mostrar indicador en móviles */
  }
}

@media (max-width: 480px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
  
  .page-header {
    padding: clamp(0.2rem, 0.4vw, 0.3rem);
  }
  
  .header-content {
    padding: 0 8px;
  }
  
  .header-main {
    min-width: 80px;
  }
  
  .header-title {
    font-size: clamp(10px, 2.5vw, 14px);
  }
  
  .header-subtitle {
    font-size: clamp(7px, 1.8vw, 10px);
  }
  
  .header-icon {
    width: clamp(20px, 4vw, 26px);
    height: clamp(20px, 4vw, 26px);
  }
  
  .header-icon svg {
    width: clamp(10px, 2.5vw, 14px);
    height: clamp(10px, 2.5vw, 14px);
  }
  
  .refresh-btn-icon {
    width: clamp(24px, 5vw, 30px);
    height: clamp(24px, 5vw, 30px);
  }
  
  .refresh-icon {
    width: clamp(12px, 2.5vw, 14px);
    height: clamp(12px, 2.5vw, 14px);
  }
}

@media (max-width: 375px) {
  .main-content {
    margin-left: 180px;
    width: calc(100vw - 180px);
  }
}

/* Breakpoint para pantallas muy pequeñas */
@media (max-width: 320px) {
  .header-subtitle {
    display: none; /* Ocultar subtitle en pantallas muy pequeñas */
  }
}
</style>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
</style>
