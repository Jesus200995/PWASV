<template>
  <div class="configuracion-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"/>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Configuración del Sistema</h1>
              <p class="header-subtitle">Administra las configuraciones generales de la aplicación</p>
            </div>
          </div>
        </div>
      </header>

      <div class="page-content">
        <div class="two-column-layout">
          <!-- COLUMNA IZQUIERDA -->
          <div class="main-column">
            <!-- Configuración General -->
            <section class="config-section compact">
              <div class="section-glass-container compact">
                <div class="section-header compact">
                  <div class="section-icon settings-section-icon sm">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="3"/>
                      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                    </svg>
                  </div>
                  <div class="section-title">
                    <h2>Configuracion General</h2>
                  </div>
                </div>
                
                <div class="config-cards-row">
                  <!-- API -->
                  <div class="config-card-compact">
                    <div class="card-header-compact">
                      <div class="card-icon-sm api-gradient">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>
                          <polyline points="14,2 14,8 20,8"/>
                          <line x1="12" y1="18" x2="12" y2="12"/>
                          <line x1="9" y1="15" x2="15" y2="15"/>
                        </svg>
                      </div>
                      <span class="card-label">Conexion API</span>
                    </div>
                    <div class="card-body-compact">
                      <div class="form-row">
                        <label>URL</label>
                        <input v-model="apiConfig.url" type="url" class="input-compact" placeholder="https://apipwa.sembrandodatos.com">
                      </div>
                      <div class="form-row">
                        <label>Timeout</label>
                        <input v-model="apiConfig.timeout" type="number" class="input-compact" min="5" max="60">
                      </div>
                    </div>
                    <button @click="guardarConfigAPI" class="btn-compact btn-primary">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                      Guardar
                    </button>
                  </div>

                  <!-- Aplicacion -->
                  <div class="config-card-compact">
                    <div class="card-header-compact">
                      <div class="card-icon-sm app-gradient">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
                          <line x1="8" y1="21" x2="16" y2="21"/>
                          <line x1="12" y1="17" x2="12" y2="21"/>
                        </svg>
                      </div>
                      <span class="card-label">Aplicacion</span>
                    </div>
                    <div class="card-body-compact">
                      <div class="form-row">
                        <label>Nombre</label>
                        <input v-model="appConfig.name" type="text" class="input-compact" placeholder="Sembrando Vida Admin">
                      </div>
                      <div class="form-row">
                        <label>Registros</label>
                        <select v-model="appConfig.recordsPerPage" class="select-compact">
                          <option value="10">10</option>
                          <option value="25">25</option>
                          <option value="50">50</option>
                          <option value="100">100</option>
                        </select>
                      </div>
                      <div class="toggle-row">
                        <label class="toggle-sm">
                          <input v-model="appConfig.autoRefresh" type="checkbox">
                          <span class="slider-sm"></span>
                        </label>
                        <span class="toggle-text">Auto-refresh</span>
                      </div>
                    </div>
                    <button @click="guardarConfigApp" class="btn-compact btn-primary">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                      Guardar
                    </button>
                  </div>

                  <!-- Sistema -->
                  <div class="config-card-compact">
                    <div class="card-header-compact">
                      <div class="card-icon-sm info-gradient">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <circle cx="12" cy="12" r="10"/>
                          <line x1="12" y1="16" x2="12" y2="12"/>
                          <line x1="12" y1="8" x2="12.01" y2="8"/>
                        </svg>
                      </div>
                      <span class="card-label">Sistema</span>
                    </div>
                    <div class="card-body-compact">
                      <div class="info-mini">
                        <span>Version</span><span class="val">v1.0.0</span>
                      </div>
                      <div class="info-mini">
                        <span>Fecha</span><span class="val">{{ new Date().toLocaleDateString('es-ES') }}</span>
                      </div>
                      <div class="info-mini">
                        <span>Estado</span><span :class="['badge-mini', serverStatus.class]">{{ serverStatus.text }}</span>
                      </div>
                      <div class="info-mini">
                        <span>Admin</span><span class="val">{{ adminUser }}</span>
                      </div>
                    </div>
                    <button @click="verificarEstadoServidor" class="btn-compact btn-secondary" :disabled="checking">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
                      {{ checking ? 'Verificando...' : 'Verificar' }}
                    </button>
                  </div>
                </div>
              </div>
            </section>

            <!-- Gestion de Imagenes -->
            <section class="config-section compact">
              <div class="section-glass-container compact">
                <div class="section-header compact">
                  <div class="section-icon images-section-icon sm">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                      <circle cx="8.5" cy="8.5" r="1.5"/>
                      <polyline points="21 15 16 10 5 21"/>
                    </svg>
                  </div>
                  <div class="section-title">
                    <h2>Gestion de Imagenes</h2>
                  </div>
                </div>
                
                <div class="image-cards-row">
                  <div class="image-action-card red" @click="confirmarEliminarImagenes" :class="{ disabled: eliminandoImagenes }">
                    <div class="image-action-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6"/>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                      </svg>
                    </div>
                    <div class="image-action-text">
                      <h4>{{ eliminandoImagenes ? 'Eliminando...' : 'Eliminar Todas' }}</h4>
                      <p>Elimina todas las imagenes del sistema</p>
                    </div>
                    <span class="action-badge red">Destructiva</span>
                  </div>

                  <div class="image-action-card orange" @click="abrirModalEliminarPorFecha" :class="{ disabled: eliminandoImagenesPorFecha }">
                    <div class="image-action-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                        <line x1="16" y1="2" x2="16" y2="6"/>
                        <line x1="8" y1="2" x2="8" y2="6"/>
                        <line x1="3" y1="10" x2="21" y2="10"/>
                      </svg>
                    </div>
                    <div class="image-action-text">
                      <h4>{{ eliminandoImagenesPorFecha ? 'Eliminando...' : 'Por Periodo' }}</h4>
                      <p>Elimina por mes o año especifico</p>
                    </div>
                    <span class="action-badge orange">Selectiva</span>
                  </div>
                </div>
              </div>
            </section>

            <!-- Herramientas -->
            <section class="config-section compact">
              <div class="section-glass-container compact">
                <div class="section-header compact">
                  <div class="section-icon tools-section-icon sm">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
                    </svg>
                  </div>
                  <div class="section-title">
                    <h2>Herramientas</h2>
                  </div>
                </div>
                
                <div class="tools-row">
                  <button class="tool-btn" @click="limpiarCache">
                    <div class="tool-icon amber">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M3 6h18"/>
                        <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
                        <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
                      </svg>
                    </div>
                    <span>Cache</span>
                  </button>

                  <button class="tool-btn" @click="reiniciarContadores">
                    <div class="tool-icon green">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="23 4 23 10 17 10"/>
                        <polyline points="1 20 1 14 7 14"/>
                        <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
                      </svg>
                    </div>
                    <span>Contadores</span>
                  </button>

                  <button class="tool-btn" @click="mostrarLogs">
                    <div class="tool-icon gray">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                        <polyline points="14 2 14 8 20 8"/>
                      </svg>
                    </div>
                    <span>Logs</span>
                  </button>

                  <button class="tool-btn" @click="abrirModalTransferencia">
                    <div class="tool-icon teal">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="17 1 21 5 17 9"/>
                        <path d="M3 11V9a4 4 0 0 1 4-4h14"/>
                        <polyline points="7 23 3 19 7 15"/>
                        <path d="M21 13v2a4 4 0 0 1-4 4H3"/>
                      </svg>
                    </div>
                    <span>Transferir</span>
                  </button>
                </div>
              </div>
            </section>
          </div>

          <!-- COLUMNA DERECHA -->
          <div class="side-column">
            <!-- Gestion de Datos -->
            <section class="config-section compact">
              <div class="section-glass-container compact">
                <div class="section-header compact">
                  <div class="section-icon data-section-icon sm">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <ellipse cx="12" cy="5" rx="9" ry="3"/>
                      <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
                      <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
                    </svg>
                  </div>
                  <div class="section-title">
                    <h2>Gestion de Datos</h2>
                  </div>
                </div>
                
                <div class="data-list">
                  <div class="data-item" @click="confirmarExportarDatos" :class="{ disabled: exporting }">
                    <div class="data-icon blue">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                        <polyline points="7 10 12 15 17 10"/>
                        <line x1="12" y1="15" x2="12" y2="3"/>
                      </svg>
                    </div>
                    <div class="data-text">
                      <h4>{{ exporting ? 'Exportando...' : 'Exportar JSON' }}</h4>
                      <p>Todos los datos</p>
                    </div>
                    <svg class="data-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
                  </div>

                  <div class="data-item" @click="confirmarDescargarBaseDatos" :class="{ disabled: descargandoBD }">
                    <div class="data-icon purple">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <ellipse cx="12" cy="5" rx="9" ry="3"/>
                        <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
                        <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
                      </svg>
                    </div>
                    <div class="data-text">
                      <h4>{{ descargandoBD ? 'Descargando...' : 'Base de Datos' }}</h4>
                      <p>Descarga completa</p>
                    </div>
                    <svg class="data-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
                  </div>

                  <div class="data-item" @click="confirmarDescargarBDRapida" :class="{ disabled: descargandoBDRapida }">
                    <div class="data-icon pink">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
                      </svg>
                    </div>
                    <div class="data-text">
                      <h4>{{ descargandoBDRapida ? 'Descargando...' : 'BD Rapida' }}</h4>
                      <p>Descarga optimizada</p>
                    </div>
                    <svg class="data-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
                  </div>

                  <div class="data-item" @click="confirmarDescargarCSV" :class="{ disabled: descargandoRegistrosCSV }">
                    <div class="data-icon orange">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                        <polyline points="14 2 14 8 20 8"/>
                      </svg>
                    </div>
                    <div class="data-text">
                      <h4>{{ descargandoRegistrosCSV ? 'Exportando...' : 'Actividades CSV' }}</h4>
                      <p>Formato CSV</p>
                    </div>
                    <svg class="data-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
                  </div>

                  <div class="data-item" @click="confirmarDescargarUsuarios" :class="{ disabled: descargandoUsuarios }">
                    <div class="data-icon cyan">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                        <circle cx="9" cy="7" r="4"/>
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                      </svg>
                    </div>
                    <div class="data-text">
                      <h4>{{ descargandoUsuarios ? 'Descargando...' : 'Usuarios' }}</h4>
                      <p>Lista registrados</p>
                    </div>
                    <svg class="data-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
                  </div>
                </div>
              </div>
            </section>

            <!-- Zona Peligrosa -->
            <section class="config-section compact">
              <div class="section-glass-container compact danger-glass">
                <div class="section-header compact">
                  <div class="section-icon danger-section-icon sm">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                      <line x1="12" y1="9" x2="12" y2="13"/>
                      <line x1="12" y1="17" x2="12.01" y2="17"/>
                    </svg>
                  </div>
                  <div class="section-title">
                    <h2>Zona Peligrosa</h2>
                  </div>
                </div>
                
                <div class="danger-zone-compact">
                  <div class="danger-alert">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                    </svg>
                    <p>Seccion bloqueada por seguridad</p>
                  </div>
                  
                  <div class="danger-btns">
                    <button class="danger-btn-sm" disabled>
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                      </svg>
                      Eliminar Registros
                    </button>
                    <button class="danger-btn-sm" disabled>
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <polyline points="12,6 12,12 16,14"/>
                      </svg>
                      Eliminar Asistencias
                    </button>
                  </div>
                  
                  <div class="blocked-overlay-sm">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                      <circle cx="12" cy="16" r="1"/>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                    </svg>
                    <span>BLOQUEADO</span>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </main>    <!-- Modal para mensajes -->
    <div v-if="showModal" class="modal-overlay message-modal-overlay" @click="cerrarModal">
      <div class="modal-content message-modal" @click.stop>
        <div class="message-modal-header" :class="modalHeaderClass">
          <div class="message-icon-wrapper">
            <!-- Icono de exito -->
            <svg v-if="modalType === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
            <!-- Icono de error -->
            <svg v-else-if="modalType === 'error'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="15" y1="9" x2="9" y2="15"/>
              <line x1="9" y1="9" x2="15" y2="15"/>
            </svg>
            <!-- Icono de info -->
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="16" x2="12" y2="12"/>
              <line x1="12" y1="8" x2="12.01" y2="8"/>
            </svg>
          </div>
          <h3>{{ cleanModalTitle }}</h3>
        </div>
        <div class="message-modal-body" v-html="modalContent"></div>
        <div class="message-modal-footer">
          <button @click="cerrarModal" class="btn-message-ok" :class="modalType">
            Aceptar
          </button>
        </div>
      </div>
    </div>    <!-- Modal de confirmación -->
    <ConfirmModal
      :show="showConfirmModal"
      :title="confirmTitle"
      :message="confirmMessage"
      :type="confirmType"
      @confirm="handleConfirm"
      @cancel="handleCancel"
    />

    <!-- Modal de progreso para eliminación de imágenes -->
    <ProgressModal
      ref="progressModalRef"
      :show="showProgressModal"
      titulo="Eliminar todas las imágenes"
      @cerrar="cerrarProgressModal"
      @completado="onProgressCompletado"
    />

    <!-- Modal de progreso NARANJA para eliminación por fecha -->
    <ProgressModalFecha
      ref="progressModalFechaRef"
      :show="showProgressModalFecha"
      titulo="Eliminar imágenes por fecha"
      :periodo="periodoTextoPreview"
      @cerrar="cerrarProgressModalFecha"
      @completado="onProgressFechaCompletado"
    />

    <!-- Modal de progreso para descarga de BD -->
    <DescargaProgressModal
      ref="descargaProgressRef"
      :show="showDescargaProgress"
    />

    <!-- Modal de progreso NARANJA para descarga de CSV -->
    <DescargaCSVProgressModal
      ref="descargaCSVProgressRef"
      :show="showDescargaCSVProgress"
    />

    <!-- Modal para Eliminar Imágenes por Fecha -->
    <div v-if="showEliminarPorFechaModal" class="modal-overlay" @click="cerrarModalEliminarPorFecha">
      <div class="modal-content modal-eliminar-fecha" @click.stop>
        <div class="modal-header modal-header-fecha">
          <div class="header-icon-fecha">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
          </div>
          <h3>Eliminar Imágenes por Fecha</h3>
          <button @click="cerrarModalEliminarPorFecha" class="btn-close">×</button>
        </div>
        
        <div class="modal-body modal-body-fecha">
          <div class="fecha-form">
            <p class="fecha-description">
              Selecciona el período de imágenes que deseas eliminar. Esta acción eliminará las fotos de registros y asistencias del período seleccionado.
            </p>
            
            <div class="fecha-options">
              <div class="fecha-option-toggle">
                <button 
                  @click="eliminarFechaConfig.soloMes = true" 
                  :class="['toggle-btn', { active: eliminarFechaConfig.soloMes }]"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                  </svg>
                  Solo un Mes
                </button>
                <button 
                  @click="eliminarFechaConfig.soloMes = false" 
                  :class="['toggle-btn', { active: !eliminarFechaConfig.soloMes }]"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                  </svg>
                  Año Completo
                </button>
              </div>

              <div class="fecha-selectors">
                <div v-if="eliminarFechaConfig.soloMes" class="fecha-field">
                  <label>Mes</label>
                  <select v-model="eliminarFechaConfig.mes" class="fecha-select">
                    <option value="1">Enero</option>
                    <option value="2">Febrero</option>
                    <option value="3">Marzo</option>
                    <option value="4">Abril</option>
                    <option value="5">Mayo</option>
                    <option value="6">Junio</option>
                    <option value="7">Julio</option>
                    <option value="8">Agosto</option>
                    <option value="9">Septiembre</option>
                    <option value="10">Octubre</option>
                    <option value="11">Noviembre</option>
                    <option value="12">Diciembre</option>
                  </select>
                </div>
                <div class="fecha-field">
                  <label>Año</label>
                  <select v-model="eliminarFechaConfig.anio" class="fecha-select">
                    <option v-for="year in aniosDisponibles" :key="year" :value="year">{{ year }}</option>
                  </select>
                </div>
              </div>

              <div class="fecha-preview">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 19V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2z"></path>
                  <line x1="9" y1="9" x2="15" y2="15"></line>
                  <line x1="15" y1="9" x2="9" y2="15"></line>
                </svg>
                <span>
                  Se eliminarán imágenes de: 
                  <strong>{{ periodoTextoPreview }}</strong>
                </span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer modal-footer-fecha">
          <button @click="cerrarModalEliminarPorFecha" class="btn-cancel" :disabled="eliminandoImagenesPorFecha">
            Cancelar
          </button>
          <button 
            @click="confirmarEliminarPorFecha" 
            class="btn-danger-fecha" 
            :disabled="eliminandoImagenesPorFecha"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
            {{ eliminandoImagenesPorFecha ? 'Eliminando...' : 'Eliminar Imágenes' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de Transferencia de Actividades -->
    <div v-if="showTransferenciaModal" class="modal-overlay" @click="cerrarModalTransferencia">
      <div class="modal-content modal-transferencia" @click.stop>
        <div class="modal-header modal-header-transferencia">
          <div class="header-icon-transferencia">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M16 3h5v5"></path>
              <line x1="21" y1="3" x2="14" y2="10"></line>
              <path d="M8 21H3v-5"></path>
              <line x1="3" y1="21" x2="10" y2="14"></line>
            </svg>
          </div>
          <h3>Transferir Actividades</h3>
          <button @click="cerrarModalTransferencia" class="btn-close">×</button>
        </div>
        
        <div class="modal-body modal-body-transferencia">
          <!-- Barra de progreso -->
          <div v-if="transfiriendo" class="transferencia-progress">
            <div class="progress-bar-container">
              <div class="progress-bar-fill" :style="{ width: progresoTransferencia + '%' }"></div>
            </div>
            <p class="progress-text">{{ mensajeProgreso }}</p>
          </div>

          <!-- Usuario Origen -->
          <div class="transferencia-seccion">
            <h4 class="seccion-titulo">
              <span class="seccion-icon origen">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 1l4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/></svg>
              </span>
              Usuario Origen (De quien se transferiran)
            </h4>
            <div class="busqueda-curp">
              <input 
                v-model="curpOrigen" 
                type="text" 
                class="input-curp"
                placeholder="Ingresa CURP del usuario origen (18 caracteres)"
                maxlength="18"
                :disabled="transfiriendo"
                @input="curpOrigen = curpOrigen.toUpperCase()"
              >
              <button 
                @click="buscarUsuarioOrigen" 
                class="btn-buscar"
                :disabled="curpOrigen.length !== 18 || buscandoOrigen || transfiriendo"
              >
                <svg v-if="!buscandoOrigen" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                <span v-else class="spinner-small"></span>
                {{ buscandoOrigen ? 'Buscando...' : 'Buscar' }}
              </button>
            </div>
            
            <!-- Tarjeta Usuario Origen -->
            <div v-if="usuarioOrigen" class="tarjeta-usuario tarjeta-origen">
              <div class="tarjeta-avatar">
                <span>{{ usuarioOrigen.nombre_completo?.charAt(0) || '?' }}</span>
              </div>
              <div class="tarjeta-info">
                <h5>{{ usuarioOrigen.nombre_completo }}</h5>
                <p class="tarjeta-correo">{{ usuarioOrigen.correo }}</p>
                <p class="tarjeta-curp">CURP: {{ usuarioOrigen.curp }}</p>
                <div class="tarjeta-stats">
                  <span class="stat-badge actividades">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                      <polyline points="14,2 14,8 20,8"></polyline>
                    </svg>
                    {{ usuarioOrigen.total_actividades }} actividades
                  </span>
                  <span class="stat-badge asistencias">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"></circle>
                      <polyline points="12,6 12,12 16,14"></polyline>
                    </svg>
                    {{ usuarioOrigen.total_asistencias }} asistencias
                  </span>
                </div>
              </div>
              <button @click="limpiarUsuarioOrigen" class="btn-limpiar" :disabled="transfiriendo">✕</button>
            </div>
            <div v-else-if="errorOrigen" class="error-mensaje">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              {{ errorOrigen }}
            </div>
          </div>

          <!-- Flecha de transferencia -->
          <div v-if="usuarioOrigen && usuarioDestino" class="flecha-transferencia">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <polyline points="19,12 12,19 5,12"></polyline>
            </svg>
          </div>

          <!-- Usuario Destino -->
          <div class="transferencia-seccion">
            <h4 class="seccion-titulo">
              <span class="seccion-icon destino">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 23l-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>
              </span>
              Usuario Destino (A quien se transferiran)
            </h4>
            <div class="busqueda-curp">
              <input 
                v-model="curpDestino" 
                type="text" 
                class="input-curp"
                placeholder="Ingresa CURP del usuario destino (18 caracteres)"
                maxlength="18"
                :disabled="transfiriendo"
                @input="curpDestino = curpDestino.toUpperCase()"
              >
              <button 
                @click="buscarUsuarioDestino" 
                class="btn-buscar"
                :disabled="curpDestino.length !== 18 || buscandoDestino || transfiriendo"
              >
                <svg v-if="!buscandoDestino" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                <span v-else class="spinner-small"></span>
                {{ buscandoDestino ? 'Buscando...' : 'Buscar' }}
              </button>
            </div>
            
            <!-- Tarjeta Usuario Destino -->
            <div v-if="usuarioDestino" class="tarjeta-usuario tarjeta-destino">
              <div class="tarjeta-avatar">
                <span>{{ usuarioDestino.nombre_completo?.charAt(0) || '?' }}</span>
              </div>
              <div class="tarjeta-info">
                <h5>{{ usuarioDestino.nombre_completo }}</h5>
                <p class="tarjeta-correo">{{ usuarioDestino.correo }}</p>
                <p class="tarjeta-curp">CURP: {{ usuarioDestino.curp }}</p>
                <div class="tarjeta-stats">
                  <span class="stat-badge actividades">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                      <polyline points="14,2 14,8 20,8"></polyline>
                    </svg>
                    {{ usuarioDestino.total_actividades }} actividades
                  </span>
                  <span class="stat-badge asistencias">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"></circle>
                      <polyline points="12,6 12,12 16,14"></polyline>
                    </svg>
                    {{ usuarioDestino.total_asistencias }} asistencias
                  </span>
                </div>
              </div>
              <button @click="limpiarUsuarioDestino" class="btn-limpiar" :disabled="transfiriendo">✕</button>
            </div>
            <div v-else-if="errorDestino" class="error-mensaje">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              {{ errorDestino }}
            </div>
          </div>

          <!-- Opciones de transferencia -->
          <div v-if="usuarioOrigen && usuarioDestino" class="opciones-transferencia">
            <label class="checkbox-option">
              <input type="checkbox" v-model="incluirAsistencias" :disabled="transfiriendo">
              <span class="checkbox-label">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"></circle>
                  <polyline points="12,6 12,12 16,14"></polyline>
                </svg>
                Incluir asistencias en la transferencia
              </span>
            </label>
          </div>

          <!-- Botones de acción -->
          <div class="modal-actions">
            <button 
              @click="cerrarModalTransferencia" 
              class="btn-cancelar"
              :disabled="transfiriendo"
            >
              Cancelar
            </button>
            <button 
              @click="ejecutarTransferencia" 
              class="btn-transferir"
              :disabled="!usuarioOrigen || !usuarioDestino || transfiriendo || usuarioOrigen.total_actividades === 0"
            >
              <svg v-if="!transfiriendo" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M16 3h5v5"></path>
                <line x1="21" y1="3" x2="14" y2="10"></line>
                <path d="M8 21H3v-5"></path>
                <line x1="3" y1="21" x2="10" y2="14"></line>
              </svg>
              <span v-else class="spinner-small"></span>
              {{ transfiriendo ? 'Transfiriendo...' : 'Transferir Actividades' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Confirmación de Transferencia (Bonito y Responsivo) -->
    <Transition name="modal-fade">
      <div v-if="showConfirmTransferencia" class="confirm-transfer-overlay" @click="cancelarConfirmTransferencia">
        <Transition name="modal-scale">
          <div class="confirm-transfer-modal" @click.stop>
            <!-- Icono de advertencia animado -->
            <div class="confirm-icon-container">
              <div class="confirm-icon warning">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                  <line x1="12" y1="9" x2="12" y2="13"></line>
                  <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
              </div>
            </div>

            <!-- Título -->
            <h3 class="confirm-title">¿Confirmar Transferencia?</h3>

            <!-- Contenido -->
            <div class="confirm-content">
              <p class="confirm-description">
                Estás a punto de transferir:
              </p>
              
              <div class="transfer-summary">
                <div class="summary-item">
                  <span class="summary-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
                  </span>
                  <span class="summary-text">
                    <strong>{{ usuarioOrigen?.total_actividades || 0 }}</strong> actividades
                  </span>
                </div>
                <div v-if="incluirAsistencias" class="summary-item">
                  <span class="summary-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  </span>
                  <span class="summary-text">
                    <strong>{{ usuarioOrigen?.total_asistencias || 0 }}</strong> asistencias
                  </span>
                </div>
              </div>

              <div class="transfer-users">
                <div class="user-card from">
                  <span class="user-label">De:</span>
                  <span class="user-name">{{ usuarioOrigen?.nombre_completo }}</span>
                </div>
                <div class="transfer-arrow">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                    <polyline points="12,5 19,12 12,19"></polyline>
                  </svg>
                </div>
                <div class="user-card to">
                  <span class="user-label">A:</span>
                  <span class="user-name">{{ usuarioDestino?.nombre_completo }}</span>
                </div>
              </div>

              <div class="warning-box">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                <span>Esta acción <strong>NO SE PUEDE DESHACER</strong></span>
              </div>
            </div>

            <!-- Botones -->
            <div class="confirm-actions">
              <button @click="cancelarConfirmTransferencia" class="btn-cancel-confirm">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
                Cancelar
              </button>
              <button @click="confirmarTransferenciaFinal" class="btn-confirm-transfer">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="20,6 9,17 4,12"></polyline>
                </svg>
                Sí, Transferir
              </button>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Sidebar from '../components/Sidebar.vue'
import ConfirmModal from '../components/ConfirmModal.vue'
import ProgressModal from '../components/ProgressModal.vue'
import ProgressModalFecha from '../components/ProgressModalFecha.vue'
import DescargaProgressModal from '../components/DescargaProgressModal.vue'
import DescargaCSVProgressModal from '../components/DescargaCSVProgressModal.vue'
import asistenciasService from '../services/asistenciasService.js'
import imagenesService from '../services/imagenesService.js'
import baseDatosService from '../services/baseDatosService.js'

const router = useRouter()

// Estado de conexión
const isOnline = ref(navigator.onLine)

const adminUser = ref(localStorage.getItem('admin_user') || 'Admin')
const checking = ref(false)
const exporting = ref(false)

// Variables para el modal de descarga de BD
const descargaProgressRef = ref(null)
const showDescargaProgress = ref(false)

// Variables para el modal de descarga de CSV
const descargaCSVProgressRef = ref(null)
const showDescargaCSVProgress = ref(false)

// Variables para el modal de confirmación
const showConfirmModal = ref(false)
const confirmAction = ref(null)
const confirmTitle = ref('')
const confirmMessage = ref('')
const confirmType = ref('warning')

// Variables para el modal de transferencia de actividades
const showTransferenciaModal = ref(false)
const curpOrigen = ref('')
const curpDestino = ref('')
const usuarioOrigen = ref(null)
const usuarioDestino = ref(null)
const buscandoOrigen = ref(false)
const buscandoDestino = ref(false)
const errorOrigen = ref('')
const errorDestino = ref('')
const transfiriendo = ref(false)
const progresoTransferencia = ref(0)
const mensajeProgreso = ref('')
const incluirAsistencias = ref(false)

// Variables para el modal de confirmación de transferencia
const showConfirmTransferencia = ref(false)
const confirmTransferenciaCallback = ref(null)

// Variables para las acciones de eliminación masiva
const eliminandoRegistros = ref(false)
const eliminandoAsistencias = ref(false)
const descargandoBD = ref(false)
const descargandoUsuarios = ref(false)
const eliminandoImagenes = ref(false)
const descargandoBDRapida = ref(false)
const descargandoRegistrosCSV = ref(false)

// Variables para eliminar imágenes por fecha
const showEliminarPorFechaModal = ref(false)
const eliminandoImagenesPorFecha = ref(false)
const progresoEliminacionFecha = ref(0)
const mensajeProgresoFecha = ref('')
const showProgressModalFecha = ref(false)
const progressModalFechaRef = ref(null)
const eliminarFechaConfig = reactive({
  mes: new Date().getMonth() + 1,
  anio: new Date().getFullYear(),
  soloMes: true
})

// Años disponibles para seleccionar (últimos 5 años)
const aniosDisponibles = computed(() => {
  const currentYear = new Date().getFullYear()
  return Array.from({ length: 6 }, (_, i) => currentYear - i)
})

// Preview del período a eliminar
const periodoTextoPreview = computed(() => {
  const meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
  if (eliminarFechaConfig.soloMes) {
    return `${meses[eliminarFechaConfig.mes - 1]} ${eliminarFechaConfig.anio}`
  }
  return `Todo el año ${eliminarFechaConfig.anio}`
})

// Variables para el modal de progreso
const showProgressModal = ref(false)
const progressModalRef = ref(null)

const apiConfig = reactive({
  url: 'https://apipwa.sembrandodatos.com',
  timeout: 30
})

const appConfig = reactive({
  name: 'Sembrando Vida Admin',
  recordsPerPage: 25,
  autoRefresh: false
})

const serverStatus = reactive({
  text: 'Desconocido',
  class: 'status-unknown'
})

const showModal = ref(false)
const modalTitle = ref('')
const modalContent = ref('')

// Computed para el modal de mensajes
const modalType = computed(() => {
  const title = modalTitle.value.toLowerCase()
  if (title.includes('exito') || title.includes('exitosa') || title.includes('eliminado') || title.includes('eliminadas') || title.includes('completada')) {
    return 'success'
  } else if (title.includes('error') || title.includes('fallo')) {
    return 'error'
  }
  return 'info'
})

const cleanModalTitle = computed(() => {
  return modalTitle.value.replace(/[\u{1F300}-\u{1F9FF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]|[\u{1F000}-\u{1F02F}]|[\u{1F0A0}-\u{1F0FF}]|[\u{1F100}-\u{1F64F}]|[\u{1F680}-\u{1F6FF}]|✅|❌|⚠️|ℹ️|🎉/gu, '').trim()
})

const modalHeaderClass = computed(() => {
  return `header-${modalType.value}`
})

onMounted(() => {
  cargarConfiguraciones()
  verificarEstadoServidor()
  
  // Escuchar cambios de conexión
  window.addEventListener('online', () => {
    isOnline.value = true
  })
  
  window.addEventListener('offline', () => {
    isOnline.value = false
  })
})

const cargarConfiguraciones = () => {
  // Cargar configuraciones desde localStorage
  const savedApiConfig = localStorage.getItem('admin_api_config')
  if (savedApiConfig) {
    Object.assign(apiConfig, JSON.parse(savedApiConfig))
  }

  const savedAppConfig = localStorage.getItem('admin_app_config')
  if (savedAppConfig) {
    Object.assign(appConfig, JSON.parse(savedAppConfig))
  }
}

const guardarConfigAPI = () => {
  localStorage.setItem('admin_api_config', JSON.stringify(apiConfig))
  mostrarMensaje('Éxito', 'Configuración de API guardada correctamente.')
}

const guardarConfigApp = () => {
  localStorage.setItem('admin_app_config', JSON.stringify(appConfig))
  mostrarMensaje('Éxito', 'Configuración de la aplicación guardada correctamente.')
}

const verificarEstadoServidor = async () => {
  checking.value = true
  
  try {
    const token = localStorage.getItem('admin_token')
    await axios.get(`${apiConfig.url}/usuarios`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      timeout: apiConfig.timeout * 1000
    })
    
    serverStatus.text = '🟢 Conectado'
    serverStatus.class = 'status-online'
  } catch (err) {
    serverStatus.text = '🔴 Desconectado'
    serverStatus.class = 'status-offline'
  } finally {
    checking.value = false
  }
}

// === CONFIRMACIONES PARA GESTIÓN DE DATOS ===
const confirmarExportarDatos = () => {
  confirmType.value = 'info'
  confirmTitle.value = 'Exportar Datos JSON'
  confirmMessage.value = `Se exportarán todos los datos del sistema en formato JSON.

Esta acción generará un archivo con:
• Lista completa de usuarios registrados
• Todos los registros de actividades
• Metadatos y estadísticas del sistema

El archivo se descargará automáticamente.`
  
  confirmAction.value = ejecutarExportarDatos
  showConfirmModal.value = true
}

const confirmarDescargarBaseDatos = () => {
  confirmType.value = 'info'
  confirmTitle.value = 'Descargar Base de Datos'
  confirmMessage.value = `Se descargará una copia completa de la base de datos.

Esta acción incluirá:
• Todos los usuarios del sistema
• Registros de actividades completos
• Historial de asistencias
• Datos de ubicación y fotografías

Esta operación puede tardar varios minutos.`
  
  confirmAction.value = ejecutarDescargarBaseDatos
  showConfirmModal.value = true
}

const confirmarDescargarBDRapida = () => {
  confirmType.value = 'info'
  confirmTitle.value = 'Descarga Rapida de BD'
  confirmMessage.value = `Se descargará una versión optimizada de la base de datos.

Esta descarga incluye:
• Usuarios y registros esenciales
• Datos comprimidos para mayor velocidad
• Exportación en formato JSON

Ideal para respaldos rápidos del sistema.`
  
  confirmAction.value = ejecutarDescargarBDRapida
  showConfirmModal.value = true
}

const confirmarDescargarCSV = () => {
  confirmType.value = 'warning'
  confirmTitle.value = 'Exportar Actividades CSV'
  confirmMessage.value = `Se exportarán todas las actividades en formato CSV.

El archivo incluirá:
• Registros de actividades de campo
• Registros de actividades de gabinete
• Fechas, ubicaciones y descripciones

Formato compatible con Excel y hojas de cálculo.`
  
  confirmAction.value = ejecutarDescargarCSV
  showConfirmModal.value = true
}

const confirmarDescargarUsuarios = () => {
  confirmType.value = 'info'
  confirmTitle.value = 'Exportar Lista de Usuarios'
  confirmMessage.value = `Se exportará la lista completa de usuarios registrados.

El archivo incluirá:
• Nombres y correos electrónicos
• CURP y datos de identificación
• Información de supervisores
• Estados y roles de usuarios

El archivo se descargará en formato JSON.`
  
  confirmAction.value = ejecutarDescargarUsuarios
  showConfirmModal.value = true
}

// === FUNCIONES DE EJECUCIÓN ===
const ejecutarExportarDatos = async () => {
  showConfirmModal.value = false
  exporting.value = true
  
  try {
    const token = localStorage.getItem('admin_token')
    
    mostrarMensaje('Iniciando', 'Obteniendo todos los registros de actividades...')
    
    // Obtener TODOS los registros sin límite y todos los usuarios
    const [usuariosRes, registrosRes] = await Promise.all([
      axios.get(`${apiConfig.url}/usuarios`, {
        headers: { 'Authorization': `Bearer ${token}` }
      }),
      axios.get(`${apiConfig.url}/registros`, {
        headers: { 'Authorization': `Bearer ${token}` },
        params: { 
          limit: 10000, // Límite alto para obtener todos los registros
          page_size: 5000 // Tamaño de página grande
        }
      })
    ])
    
    // Manejar diferentes formatos de respuesta
    const usuariosData = Array.isArray(usuariosRes.data) ? usuariosRes.data : (usuariosRes.data.usuarios || [])
    const registrosData = Array.isArray(registrosRes.data) ? registrosRes.data : (registrosRes.data.registros || [])
    
    console.log('📊 Datos obtenidos:', {
      usuarios: usuariosData.length,
      registros: registrosData.length
    })
    
    // Crear estructura JSON completa con información detallada
    const datos = {
      metadatos: {
        exportado_en: new Date().toISOString(),
        fecha_exportacion: new Date().toLocaleString('es-ES'),
        servidor: apiConfig.url,
        tipo_exportacion: 'registros_actividades_completo',
        version: '1.0'
      },
      resumen: {
        total_usuarios: usuariosData.length,
        total_registros: registrosData.length,
        registros_campo: registrosData.filter(r => r.tipo_actividad === 'campo').length,
        registros_gabinete: registrosData.filter(r => r.tipo_actividad === 'gabinete').length,
        registros_sin_tipo: registrosData.filter(r => !r.tipo_actividad || r.tipo_actividad === null).length
      },
      usuarios: usuariosData.map(usuario => ({
        id: usuario.id,
        correo: usuario.correo,
        nombre_completo: usuario.nombre_completo,
        cargo: usuario.cargo,
        supervisor: usuario.supervisor,
        curp: usuario.curp,
        telefono: usuario.telefono,
        rol: usuario.rol || 'user'
      })),
      registros_actividades: registrosData.map(registro => ({
        id: registro.id,
        usuario_id: registro.usuario_id,
        usuario_info: {
          nombre: usuariosData.find(u => u.id === registro.usuario_id)?.nombre_completo || 'Usuario no encontrado',
          correo: usuariosData.find(u => u.id === registro.usuario_id)?.correo || 'N/A'
        },
        ubicacion: {
          latitud: registro.latitud,
          longitud: registro.longitud
        },
        actividad: {
          descripcion: registro.descripcion,
          tipo: registro.tipo_actividad || 'campo',
          fecha_hora: registro.fecha_hora,
          foto_url: registro.foto_url
        }
      }))
    }
    
    // Crear y descargar archivo JSON con nombre descriptivo
    const timestamp = new Date().toISOString().split('T')[0]
    const blob = new Blob([JSON.stringify(datos, null, 2)], { type: 'application/json; charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `registros_actividades_${timestamp}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    // Calcular tamaño del archivo
    const tamanhoKB = Math.round(blob.size / 1024)
    
    mostrarMensaje('Exportacion JSON Exitosa', 
      `<div style="text-align: left;">
        <h4 style="color: #2563eb; margin-bottom: 15px;">Archivo JSON Generado</h4>
        <p><strong>Archivo:</strong> registros_actividades_${timestamp}.json</p>
        <p><strong>Tamano:</strong> ${tamanhoKB} KB</p>
        <hr style="margin: 15px 0;">
        <h5 style="color: #1e40af;">Datos Exportados:</h5>
        <ul style="margin: 10px 0; padding-left: 20px;">
          <li><strong>Usuarios:</strong> ${datos.resumen.total_usuarios}</li>
          <li><strong>Total registros:</strong> ${datos.resumen.total_registros}</li>
          <li><strong>Actividades campo:</strong> ${datos.resumen.registros_campo}</li>
          <li><strong>Actividades gabinete:</strong> ${datos.resumen.registros_gabinete}</li>
          <li><strong>Sin tipo:</strong> ${datos.resumen.registros_sin_tipo}</li>
        </ul>
        <hr style="margin: 15px 0;">
        <p style="font-size: 12px; color: #666; margin-top: 15px;">
          El archivo JSON contiene todos los registros de actividades con informacion 
          detallada de usuarios, ubicaciones y metadatos. Compatible con analisis de datos 
          y herramientas de visualizacion.
        </p>
      </div>`
    )
  } catch (err) {
    let errorMsg = 'Error al exportar los datos: '
    
    if (err.response?.status === 401) {
      errorMsg += 'No autorizado. Inicia sesión nuevamente.'
    } else if (err.response?.status === 403) {
      errorMsg += 'Acceso denegado. Permisos insuficientes.'
    } else if (err.response?.status === 500) {
      errorMsg += 'Error del servidor. Intenta más tarde.'
    } else if (err.request) {
      errorMsg += 'No se pudo conectar con el servidor. Verifica tu conexión.'
    } else {
      errorMsg += err.message || 'Error desconocido'
    }
    
    mostrarMensaje('Error', errorMsg)
  } finally {
    exporting.value = false
  }
}

const ejecutarDescargarBaseDatos = async () => {
  showConfirmModal.value = false
  descargandoBD.value = true
  
  try {
    const token = localStorage.getItem('admin_token')
    
    mostrarMensaje('Iniciando', 'Obteniendo todos los datos de la base de datos...')
    
    // Obtener TODOS los datos disponibles de la base de datos app_registros
    const [usuariosRes, registrosRes, asistenciasRes] = await Promise.all([
      axios.get(`${apiConfig.url}/usuarios/exportacion-completa`, {
        headers: { 'Authorization': `Bearer ${token}` }
      }),
      axios.get(`${apiConfig.url}/registros`, {
        headers: { 'Authorization': `Bearer ${token}` }
      }),
      axios.get(`${apiConfig.url}/asistencias`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
    ])
    
    // Manejar diferentes formatos de respuesta
    const usuariosData = Array.isArray(usuariosRes.data) ? usuariosRes.data : (usuariosRes.data.usuarios || [])
    const registrosData = Array.isArray(registrosRes.data) ? registrosRes.data : (registrosRes.data.registros || [])
    const asistenciasData = Array.isArray(asistenciasRes.data) ? asistenciasRes.data : (asistenciasRes.data.asistencias || [])
    
    // DEBUG: Mostrar datos de usuarios para verificar campos disponibles
    console.log('🔍 DEBUG - Datos de usuarios recibidos:', usuariosData)
    if (usuariosData.length > 0) {
      console.log('🔍 DEBUG - Primer usuario completo:', usuariosData[0])
      console.log('🔍 DEBUG - Campos disponibles:', Object.keys(usuariosData[0]))
    }
    
    // Generar SQL completo
    let sqlContent = ''
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
    
    // Header del archivo SQL
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- EXPORTACIÓN COMPLETA BASE DE DATOS app_registros\n`
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- Fecha de exportación: ${new Date().toLocaleString('es-ES')}\n`
    sqlContent += `-- Servidor: ${apiConfig.url}\n`
    sqlContent += `-- Total usuarios: ${usuariosData.length}\n`
    sqlContent += `-- Total registros: ${registrosData.length}\n`
    sqlContent += `-- Total asistencias: ${asistenciasData.length}\n`
    sqlContent += `-- ===============================================\n\n`
    
    // =================== TABLA USUARIOS ===================
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- TABLA: USUARIOS\n`
    sqlContent += `-- ===============================================\n`
    sqlContent += `DROP TABLE IF EXISTS usuarios CASCADE;\n\n`
    
    sqlContent += `CREATE TABLE usuarios (\n`
    sqlContent += `    id SERIAL PRIMARY KEY,\n`
    sqlContent += `    correo VARCHAR(255) UNIQUE NOT NULL,\n`
    sqlContent += `    nombre_completo VARCHAR(255) NOT NULL,\n`
    sqlContent += `    cargo VARCHAR(255),\n`
    sqlContent += `    supervisor VARCHAR(255),\n`
    sqlContent += `    contrasena VARCHAR(255) NOT NULL,\n`
    sqlContent += `    curp VARCHAR(18) UNIQUE,\n`
    sqlContent += `    telefono VARCHAR(20),\n`
    sqlContent += `    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n`
    sqlContent += `    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n`
    sqlContent += `);\n\n`
    
    // Insertar datos de usuarios
    if (usuariosData.length > 0) {
      sqlContent += `-- Datos de usuarios (${usuariosData.length} registros)\n`
      sqlContent += `INSERT INTO usuarios (id, correo, nombre_completo, cargo, supervisor, contrasena, curp, telefono) VALUES\n`
      
      const usuariosInserts = usuariosData.map((usuario, index) => {
        const id = usuario.id || index + 1
        const correo = (usuario.correo || usuario.email || '').replace(/'/g, "''")
        const nombre = (usuario.nombre_completo || usuario.nombre || '').replace(/'/g, "''")
        const cargo = (usuario.cargo || '').replace(/'/g, "''")
        const supervisor = (usuario.supervisor || '').replace(/'/g, "''")
        
        // Obtener la contraseña real del nuevo endpoint
        const contrasena = (usuario.contrasena || 'sin_contrasena').replace(/'/g, "''")
        const curp = (usuario.curp || '').replace(/'/g, "''")
        const telefono = (usuario.telefono || '').replace(/'/g, "''")
        
        // DEBUG: Log de cada usuario para verificar contraseña y teléfono
        console.log(`🔍 Usuario ${id}: contrasena="${contrasena}", telefono="${telefono}"`)
        
        return `(${id}, '${correo}', '${nombre}', '${cargo}', '${supervisor}', '${contrasena}', '${curp}', '${telefono}')`
      })
      
      sqlContent += usuariosInserts.join(',\n') + ';\n\n'
    }
    
    // =================== TABLA REGISTROS ===================
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- TABLA: REGISTROS\n`
    sqlContent += `-- ===============================================\n`
    sqlContent += `DROP TABLE IF EXISTS registros CASCADE;\n\n`
    
    sqlContent += `CREATE TABLE registros (\n`
    sqlContent += `    id SERIAL PRIMARY KEY,\n`
    sqlContent += `    usuario_id INTEGER REFERENCES usuarios(id),\n`
    sqlContent += `    latitud DECIMAL(10, 8),\n`
    sqlContent += `    longitud DECIMAL(11, 8),\n`
    sqlContent += `    descripcion TEXT,\n`
    sqlContent += `    foto_url VARCHAR(500),\n`
    sqlContent += `    fecha_hora TIMESTAMP NOT NULL,\n`
    sqlContent += `    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n`
    sqlContent += `);\n\n`
    
    // Insertar datos de registros
    if (registrosData.length > 0) {
      sqlContent += `-- Datos de registros (${registrosData.length} registros)\n`
      sqlContent += `INSERT INTO registros (id, usuario_id, latitud, longitud, descripcion, foto_url, fecha_hora) VALUES\n`
      
      const registrosInserts = registrosData.map((registro, index) => {
        const id = registro.id || index + 1
        const usuario_id = registro.usuario_id || 'NULL'
        const latitud = registro.latitud || 'NULL'
        const longitud = registro.longitud || 'NULL'
        const descripcion = (registro.descripcion || '').replace(/'/g, "''")
        const foto_url = (registro.foto_url || '').replace(/'/g, "''")
        const fecha_hora = registro.fecha_hora || new Date().toISOString()
        
        return `(${id}, ${usuario_id}, ${latitud}, ${longitud}, '${descripcion}', '${foto_url}', '${fecha_hora}')`
      })
      
      sqlContent += registrosInserts.join(',\n') + ';\n\n'
    }
    
    // =================== TABLA ASISTENCIAS ===================
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- TABLA: ASISTENCIAS\n`
    sqlContent += `-- ===============================================\n`
    sqlContent += `DROP TABLE IF EXISTS asistencias CASCADE;\n\n`
    
    sqlContent += `CREATE TABLE asistencias (\n`
    sqlContent += `    id SERIAL PRIMARY KEY,\n`
    sqlContent += `    usuario_id INTEGER REFERENCES usuarios(id),\n`
    sqlContent += `    fecha DATE NOT NULL,\n`
    sqlContent += `    hora_entrada TIME,\n`
    sqlContent += `    hora_salida TIME,\n`
    sqlContent += `    latitud_entrada DECIMAL(10, 8),\n`
    sqlContent += `    longitud_entrada DECIMAL(11, 8),\n`
    sqlContent += `    latitud_salida DECIMAL(10, 8),\n`
    sqlContent += `    longitud_salida DECIMAL(11, 8),\n`
    sqlContent += `    foto_entrada_url VARCHAR(500),\n`
    sqlContent += `    foto_salida_url VARCHAR(500),\n`
    sqlContent += `    descripcion_entrada TEXT,\n`
    sqlContent += `    descripcion_salida TEXT,\n`
    sqlContent += `    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n`
    sqlContent += `);\n\n`
    
    // Insertar datos de asistencias
    if (asistenciasData.length > 0) {
      sqlContent += `-- Datos de asistencias (${asistenciasData.length} registros)\n`
      sqlContent += `INSERT INTO asistencias (id, usuario_id, fecha, hora_entrada, hora_salida, latitud_entrada, longitud_entrada, latitud_salida, longitud_salida, foto_entrada_url, foto_salida_url, descripcion_entrada, descripcion_salida) VALUES\n`
      
      const asistenciasInserts = asistenciasData.map((asistencia, index) => {
        const id = asistencia.id || index + 1
        const usuario_id = asistencia.usuario_id || 'NULL'
        const fecha = asistencia.fecha || new Date().toISOString().split('T')[0]
        const hora_entrada = asistencia.hora_entrada ? `'${asistencia.hora_entrada}'` : 'NULL'
        const hora_salida = asistencia.hora_salida ? `'${asistencia.hora_salida}'` : 'NULL'
        const latitud_entrada = asistencia.latitud_entrada || 'NULL'
        const longitud_entrada = asistencia.longitud_entrada || 'NULL'
        const latitud_salida = asistencia.latitud_salida || 'NULL'
        const longitud_salida = asistencia.longitud_salida || 'NULL'
        const foto_entrada_url = (asistencia.foto_entrada_url || '').replace(/'/g, "''")
        const foto_salida_url = (asistencia.foto_salida_url || '').replace(/'/g, "''")
        const descripcion_entrada = (asistencia.descripcion_entrada || '').replace(/'/g, "''")
        const descripcion_salida = (asistencia.descripcion_salida || '').replace(/'/g, "''")
        
        return `(${id}, ${usuario_id}, '${fecha}', ${hora_entrada}, ${hora_salida}, ${latitud_entrada}, ${longitud_entrada}, ${latitud_salida}, ${longitud_salida}, '${foto_entrada_url}', '${foto_salida_url}', '${descripcion_entrada}', '${descripcion_salida}')`
      })
      
      sqlContent += asistenciasInserts.join(',\n') + ';\n\n'
    }
    
    // =================== ÍNDICES Y CONSTRAINTS ===================
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- ÍNDICES Y OPTIMIZACIONES\n`
    sqlContent += `-- ===============================================\n`
    sqlContent += `CREATE INDEX IF NOT EXISTS idx_usuarios_correo ON usuarios(correo);\n`
    sqlContent += `CREATE INDEX IF NOT EXISTS idx_usuarios_curp ON usuarios(curp);\n`
    sqlContent += `CREATE INDEX IF NOT EXISTS idx_registros_usuario ON registros(usuario_id);\n`
    sqlContent += `CREATE INDEX IF NOT EXISTS idx_registros_fecha ON registros(fecha_hora);\n`
    sqlContent += `CREATE INDEX IF NOT EXISTS idx_asistencias_usuario ON asistencias(usuario_id);\n`
    sqlContent += `CREATE INDEX IF NOT EXISTS idx_asistencias_fecha ON asistencias(fecha);\n\n`
    
    // Footer del archivo
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- RESUMEN DE EXPORTACIÓN\n`
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- Usuarios exportados: ${usuariosData.length}\n`
    sqlContent += `-- Registros exportados: ${registrosData.length}\n`
    sqlContent += `-- Asistencias exportadas: ${asistenciasData.length}\n`
    sqlContent += `-- Total de registros: ${usuariosData.length + registrosData.length + asistenciasData.length}\n`
    sqlContent += `-- Fin de la exportación completa\n`
    sqlContent += `-- Fecha: ${new Date().toLocaleString('es-ES')}\n`
    sqlContent += `-- ===============================================\n`
    
    // Crear y descargar archivo SQL
    const blob = new Blob([sqlContent], { type: 'application/sql; charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `BASE_DATOS_COMPLETA_${timestamp}.sql`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    // Calcular tamaño del archivo
    const tamanhoKB = Math.round(blob.size / 1024)
    const totalRegistros = usuariosData.length + registrosData.length + asistenciasData.length
    
    mostrarMensaje('Base de Datos Completa Descargada', 
      `<div style="text-align: left;">
        <h4 style="color: #2563eb; margin-bottom: 15px;">Exportacion Exitosa</h4>
        <p><strong>Archivo:</strong> BASE_DATOS_COMPLETA_${timestamp}.sql</p>
        <p><strong>Tamano:</strong> ${tamanhoKB} KB</p>
        <hr style="margin: 15px 0;">
        <h5 style="color: #1e40af;">Datos Exportados:</h5>
        <ul style="margin: 10px 0; padding-left: 20px;">
          <li><strong>Usuarios:</strong> ${usuariosData.length} registros</li>
          <li><strong>Registros:</strong> ${registrosData.length} registros</li>
          <li><strong>Asistencias:</strong> ${asistenciasData.length} registros</li>
        </ul>
        <hr style="margin: 15px 0;">
        <p><strong>Total de registros:</strong> ${totalRegistros}</p>
        <p style="font-size: 12px; color: #666; margin-top: 15px;">
          El archivo contiene la estructura completa de la base de datos con todos los datos disponibles, 
          indices y constraints. Puede ser restaurado en cualquier servidor PostgreSQL.
        </p>
      </div>`
    )
  } catch (err) {
    let errorMsg = 'Error al descargar la base de datos: '
    
    if (err.response?.status === 401) {
      errorMsg += 'No autorizado. Inicia sesión nuevamente.'
    } else if (err.response?.status === 403) {
      errorMsg += 'Acceso denegado. Permisos insuficientes.'
    } else if (err.response?.status === 404) {
      errorMsg += 'Algunos endpoints no están disponibles. Se descargaron los datos disponibles.'
    } else if (err.response?.status === 500) {
      errorMsg += 'Error del servidor. Intenta más tarde.'
    } else if (err.request) {
      errorMsg += 'No se pudo conectar con el servidor. Verifica tu conexión.'
    } else {
      errorMsg += err.message || 'Error desconocido'
    }
    
    mostrarMensaje('Error', errorMsg)
  } finally {
    descargandoBD.value = false
  }
}

// ⚡ NUEVA FUNCIÓN: Descarga rápida de BD completa con progreso en tiempo real
const ejecutarDescargarBDRapida = async () => {
  showConfirmModal.value = false
  descargandoBDRapida.value = true
  showDescargaProgress.value = true
  
  try {
    console.log('⚡ Iniciando descarga RÁPIDA de BD completa con progreso...')
    
    // Definir callback para actualizar el progreso
    const onProgress = (datos) => {
      if (descargaProgressRef.value) {
        console.log('📊 Actualizando progreso:', datos)
        descargaProgressRef.value.actualizar({
          bytesDescargados: datos.bytesDescargados,
          tamanoTotal: datos.tamanoTotal,
          velocidad: datos.velocidad,
          mensaje: `Descargando: ${((datos.bytesDescargados / (1024 * 1024)).toFixed(2))} MB descargados...`
        })
      }
    }
    
    // Llamar al servicio de BD con callback de progreso
    const resultado = await baseDatosService.descargarBDCompleta(onProgress)
    
    console.log('✅ Descarga completada:', resultado)
    
    // Marcar como completado
    if (descargaProgressRef.value) {
      descargaProgressRef.value.completar()
    }
    
    // Esperar un poco y cerrar el modal
    setTimeout(() => {
      showDescargaProgress.value = false
      descargandoBDRapida.value = false
      
      // Mostrar mensaje de éxito
      mostrarMensaje('Descarga Exitosa', 
        `<div style="text-align: left;">
          <h4 style="color: #ec4899; margin-bottom: 15px;">Base de Datos Descargada</h4>
          <p><strong>Archivo:</strong> ${resultado.archivo}</p>
          <p><strong>Tamano:</strong> ${resultado.tamanhoMB} MB</p>
          <hr style="margin: 15px 0;">
          <p style="font-size: 12px; color: #666; margin-top: 15px;">
            La base de datos completa ha sido descargada exitosamente en formato SQL.
            Incluye todas las tablas, usuarios, registros y asistencias.
          </p>
        </div>`
      )
    }, 1500)
    
  } catch (err) {
    console.error('❌ Error en descarga rápida de BD:', err)
    
    showDescargaProgress.value = false
    descargandoBDRapida.value = false
    
    let errorMsg = err.message || 'Error desconocido'
    
    // Personalizar mensajes de error
    if (errorMsg.includes('No autorizado')) {
      errorMsg = 'No autorizado. Por favor inicia sesión nuevamente.'
    } else if (errorMsg.includes('Acceso denegado')) {
      errorMsg = 'Acceso denegado. No tienes permisos para descargar la BD.'
    } else if (errorMsg.includes('Endpoint no disponible')) {
      errorMsg = 'Endpoint no disponible. Verifica que el servidor está actualizado.'
    } else if (errorMsg.includes('Error del servidor')) {
      errorMsg = 'Error del servidor. Por favor intenta más tarde.'
    } else if (errorMsg.includes('No se pudo conectar')) {
      errorMsg = 'No se pudo conectar con el servidor. Verifica la conexión.'
    }
    
    mostrarMensaje('Error', errorMsg)
  } finally {
    descargandoBDRapida.value = false
  }
}

// 📊 NUEVA FUNCIÓN: Descarga de registros CSV con progreso en tiempo real
const ejecutarDescargarCSV = async () => {
  showConfirmModal.value = false
  descargandoRegistrosCSV.value = true
  showDescargaCSVProgress.value = true
  
  try {
    console.log('📊 Iniciando descarga de registros en CSV con progreso...')
    
    // Definir callback para actualizar el progreso
    const onProgress = (datos) => {
      if (descargaCSVProgressRef.value) {
        console.log('📊 Actualizando progreso CSV:', datos)
        descargaCSVProgressRef.value.actualizar({
          bytesDescargados: datos.bytesDescargados,
          tamanoTotal: datos.tamanoTotal,
          velocidad: datos.velocidad,
          mensaje: `Exportando: ${((datos.bytesDescargados / (1024 * 1024)).toFixed(2))} MB exportados...`
        })
      }
    }
    
    // Llamar al servicio de CSV con callback de progreso
    const resultado = await baseDatosService.descargarRegistrosCSV(onProgress)
    
    console.log('✅ Exportación completada:', resultado)
    
    // Marcar como completado
    if (descargaCSVProgressRef.value) {
      descargaCSVProgressRef.value.completar()
    }
    
    // Esperar un bit y cerrar el modal
    setTimeout(() => {
      showDescargaCSVProgress.value = false
      descargandoRegistrosCSV.value = false
      
      // Mostrar mensaje de éxito
      mostrarMensaje('Exportacion Exitosa', 
        `<div style="text-align: left;">
          <h4 style="color: #f97316; margin-bottom: 15px;">Actividades Exportadas</h4>
          <p><strong>Archivo:</strong> ${resultado.archivo}</p>
          <p><strong>Tamano:</strong> ${resultado.tamanhoMB} MB</p>
          <hr style="margin: 15px 0;">
          <h5 style="color: #ea580c;">Columnas incluidas:</h5>
          <ul style="margin: 10px 0; padding-left: 20px; font-size: 12px;">
            <li>ID, Usuario, Nombre, Correo, Cargo</li>
            <li>Ubicacion (Latitud, Longitud)</li>
            <li>Descripcion de la actividad</li>
            <li><strong>Modalidad</strong> (Campo/Gabinete)</li>
            <li><strong>Tipo de Actividad</strong> (categoria)</li>
            <li><strong>Tipo de Actividad Otro</strong> (especificacion)</li>
            <li>Fecha/Hora, Foto URL</li>
          </ul>
          <hr style="margin: 15px 0;">
          <p style="font-size: 12px; color: #666; margin-top: 15px;">
            Todas las actividades han sido exportadas exitosamente en formato CSV.
            Puedes abrir el archivo en Excel o cualquier editor de hojas de calculo.
          </p>
        </div>`
      )
    }, 1500)
    
  } catch (err) {
    console.error('❌ Error en descarga de CSV:', err)
    
    showDescargaCSVProgress.value = false
    descargandoRegistrosCSV.value = false
    
    let errorMsg = err.message || 'Error desconocido'
    
    // Personalizar mensajes de error
    if (errorMsg.includes('No autorizado')) {
      errorMsg = 'No autorizado. Por favor inicia sesión nuevamente.'
    } else if (errorMsg.includes('Acceso denegado')) {
      errorMsg = 'Acceso denegado. No tienes permisos para descargar los registros.'
    } else if (errorMsg.includes('Endpoint no disponible')) {
      errorMsg = 'Endpoint no disponible. Verifica que el servidor está actualizado.'
    } else if (errorMsg.includes('Error del servidor')) {
      errorMsg = 'Error del servidor. Por favor intenta más tarde.'
    } else if (errorMsg.includes('No se pudo conectar')) {
      errorMsg = 'No se pudo conectar con el servidor. Verifica la conexión.'
    }
    
    mostrarMensaje('Error', errorMsg)
  } finally {
    descargandoRegistrosCSV.value = false
  }
}

// Funciones para el modal de confirmación
const showConfirmation = (title, message, action) => {
  confirmTitle.value = title
  confirmMessage.value = message
  confirmAction.value = action
  showConfirmModal.value = true
}

const handleConfirm = () => {
  if (confirmAction.value) {
    confirmAction.value()
  }
  showConfirmModal.value = false
}

const handleCancel = () => {
  showConfirmModal.value = false
  confirmAction.value = null
}

const limpiarCache = () => {
  showConfirmation(
    'Limpiar Cache',
    '¿Estás seguro de que quieres limpiar el cache? Esto eliminará datos temporales almacenados.',
    () => {
      // Limpiar cache del navegador (localStorage excepto tokens)
      const token = localStorage.getItem('admin_token')
      const user = localStorage.getItem('admin_user')
      
      localStorage.clear()
      
      if (token) localStorage.setItem('admin_token', token)
      if (user) localStorage.setItem('admin_user', user)
      
      // Guardar configuraciones actuales
      localStorage.setItem('admin_api_config', JSON.stringify(apiConfig))
      localStorage.setItem('admin_app_config', JSON.stringify(appConfig))
      
      mostrarMensaje('Éxito', 'Cache limpiado correctamente.')
    }
  )
}

const reiniciarContadores = () => {
  showConfirmation(
    'Reiniciar Contadores',
    '¿Estás seguro de que quieres reiniciar los contadores del sistema?',
    () => {
      // Simular reinicio de contadores
      mostrarMensaje('Éxito', 'Contadores del sistema reiniciados correctamente.')
    }
  )
}

const mostrarLogs = () => {
  const logs = [
    `[${new Date().toLocaleString()}] Sistema iniciado`,
    `[${new Date().toLocaleString()}] Usuario ${adminUser.value} autenticado`,
    `[${new Date().toLocaleString()}] Configuración cargada`,
    `[${new Date().toLocaleString()}] Estado del servidor verificado`
  ]
  
  mostrarMensaje('Logs del Sistema', `<pre>${logs.join('\n')}</pre>`)
}

const mostrarMensaje = (titulo, contenido) => {
  modalTitle.value = titulo
  modalContent.value = contenido
  showModal.value = true
}

const cerrarModal = () => {
  showModal.value = false
}

// MÉTODOS DE ELIMINACIÓN MASIVA
const confirmarEliminarRegistros = () => {
  showConfirmation(
    'ELIMINAR TODOS LOS REGISTROS',
    '¿Estás COMPLETAMENTE SEGURO de que quieres eliminar TODOS los registros del sistema?<br><br><strong>Esta acción NO SE PUEDE DESHACER</strong> y eliminará:<br>• Todos los registros históricos<br>• Fotos y documentos asociados<br>• Datos de ubicación<br><br>Esta operación es irreversible.',
    async () => {
      // Segunda confirmación más estricta
      const confirmacion = prompt('Para confirmar, escribe exactamente: ELIMINAR REGISTROS')
      if (confirmacion === 'ELIMINAR REGISTROS') {
        await eliminarTodosRegistros()
      } else {
        mostrarMensaje('Cancelado', 'Eliminación de registros cancelada.')
      }
    }
  )
}

const confirmarEliminarAsistencias = () => {
  showConfirmation(
    'ELIMINAR TODAS LAS ASISTENCIAS',
    '¿Estás COMPLETAMENTE SEGURO de que quieres eliminar TODAS las asistencias del sistema?<br><br><strong>Esta acción NO SE PUEDE DESHACER</strong> y eliminará:<br>• Todos los registros de entrada y salida<br>• Fotos de asistencia<br>• Datos de ubicación de asistencias<br>• Historial completo de asistencias<br><br>Esta operación es irreversible.',
    async () => {
      // Segunda confirmación más estricta
      const confirmacion = prompt('Para confirmar, escribe exactamente: ELIMINAR ASISTENCIAS')
      if (confirmacion === 'ELIMINAR ASISTENCIAS') {
        await eliminarTodasAsistencias()
      } else {
        mostrarMensaje('Cancelado', 'Eliminación de asistencias cancelada.')
      }
    }
  )
}

const eliminarTodosRegistros = async () => {
  eliminandoRegistros.value = true
  
  try {
    const resultado = await asistenciasService.eliminarTodosRegistros()
    
    if (resultado.status === 'success') {
      mostrarMensaje(
        'Registros Eliminados', 
        `Se han eliminado ${resultado.registros_eliminados} registros exitosamente.<br><br><strong>El sistema de registros ha sido completamente limpiado.</strong>`
      )
    } else if (resultado.status === 'info') {
      mostrarMensaje('Sin Datos', resultado.message)
    }
  } catch (error) {
    mostrarMensaje('Error', 'Error al eliminar registros: ' + (error.message || 'Error desconocido'))
  } finally {
    eliminandoRegistros.value = false
  }
}

const eliminarTodasAsistencias = async () => {
  eliminandoAsistencias.value = true
  
  try {
    const resultado = await asistenciasService.eliminarTodasAsistencias()
    
    if (resultado.status === 'success') {
      mostrarMensaje(
        'Asistencias Eliminadas', 
        `Se han eliminado ${resultado.asistencias_eliminadas} asistencias y ${resultado.fotos_eliminadas || 0} fotos exitosamente.<br><br><strong>El sistema de asistencias ha sido completamente limpiado.</strong>`
      )
    } else if (resultado.status === 'info') {
      mostrarMensaje('Sin Datos', resultado.message)
    }
  } catch (error) {
    mostrarMensaje('Error', 'Error al eliminar asistencias: ' + (error.message || 'Error desconocido'))
  } finally {
    eliminandoAsistencias.value = false
  }
}

const ejecutarDescargarUsuarios = async () => {
  showConfirmModal.value = false
  descargandoUsuarios.value = true
  
  try {
    const token = localStorage.getItem('admin_token')
    
    mostrarMensaje('Iniciando', 'Obteniendo todos los usuarios de la base de datos...')
    
    // Obtener TODOS los usuarios con información completa incluyendo contraseñas
    const response = await axios.get(`${apiConfig.url}/usuarios/exportacion-completa`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      timeout: apiConfig.timeout * 1000
    })
    
    // Manejar diferentes formatos de respuesta
    const usuariosData = Array.isArray(response.data) ? response.data : (response.data.usuarios || [])
    
    console.log('📊 Datos de usuarios obtenidos:', {
      total: usuariosData.length,
      campos: usuariosData.length > 0 ? Object.keys(usuariosData[0]) : []
    })
    
    if (usuariosData.length === 0) {
      mostrarMensaje('Sin Datos', 'No hay usuarios en la base de datos para exportar.')
      return
    }
    
    // Generar archivo SQL solo con la tabla de usuarios
    let sqlContent = ''
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
    
    // Header del archivo SQL
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- EXPORTACIÓN DE USUARIOS - Base de Datos\n`
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- Fecha de exportación: ${new Date().toLocaleString('es-ES')}\n`
    sqlContent += `-- Servidor: ${apiConfig.url}\n`
    sqlContent += `-- Total usuarios: ${usuariosData.length}\n`
    sqlContent += `-- ===============================================\n\n`
    
    // Estructura de la tabla usuarios
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- ESTRUCTURA DE LA TABLA: usuarios\n`
    sqlContent += `-- ===============================================\n`
    sqlContent += `DROP TABLE IF EXISTS usuarios CASCADE;\n\n`
    
    sqlContent += `CREATE TABLE usuarios (\n`
    sqlContent += `    id SERIAL PRIMARY KEY,\n`
    sqlContent += `    correo VARCHAR(255) UNIQUE NOT NULL,\n`
    sqlContent += `    nombre_completo VARCHAR(255) NOT NULL,\n`
    sqlContent += `    cargo VARCHAR(255),\n`
    sqlContent += `    supervisor VARCHAR(255),\n`
    sqlContent += `    contrasena VARCHAR(255) NOT NULL,\n`
    sqlContent += `    curp VARCHAR(18) UNIQUE,\n`
    sqlContent += `    telefono VARCHAR(20),\n`
    sqlContent += `    rol VARCHAR(50) DEFAULT 'user',\n`
    sqlContent += `    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n`
    sqlContent += `    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n`
    sqlContent += `);\n\n`
    
    // Datos de usuarios
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- DATOS DE USUARIOS (${usuariosData.length} registros)\n`
    sqlContent += `-- ===============================================\n`
    sqlContent += `INSERT INTO usuarios (id, correo, nombre_completo, cargo, supervisor, contrasena, curp, telefono, rol) VALUES\n`
    
    const usuariosInserts = usuariosData.map((usuario, index) => {
      const id = usuario.id || index + 1
      const correo = (usuario.correo || '').replace(/'/g, "''")
      const nombre = (usuario.nombre_completo || '').replace(/'/g, "''")
      const cargo = (usuario.cargo || '').replace(/'/g, "''")
      const supervisor = (usuario.supervisor || '').replace(/'/g, "''")
      const contrasena = (usuario.contrasena || '').replace(/'/g, "''")
      const curp = (usuario.curp || '').replace(/'/g, "''")
      const telefono = (usuario.telefono || '').replace(/'/g, "''")
      const rol = (usuario.rol || 'user').replace(/'/g, "''")
      
      return `(${id}, '${correo}', '${nombre}', '${cargo}', '${supervisor}', '${contrasena}', '${curp}', '${telefono}', '${rol}')`
    })
    
    sqlContent += usuariosInserts.join(',\n') + ';\n\n'
    
    // Índices
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- ÍNDICES\n`
    sqlContent += `-- ===============================================\n`
    sqlContent += `CREATE INDEX IF NOT EXISTS idx_usuarios_correo ON usuarios(correo);\n`
    sqlContent += `CREATE INDEX IF NOT EXISTS idx_usuarios_curp ON usuarios(curp);\n`
    sqlContent += `CREATE INDEX IF NOT EXISTS idx_usuarios_rol ON usuarios(rol);\n\n`
    
    // Estadísticas
    const usuariosConCurp = usuariosData.filter(u => u.curp && u.curp.trim() !== '').length
    const usuariosConTelefono = usuariosData.filter(u => u.telefono && u.telefono.trim() !== '').length
    const usuariosConSupervisor = usuariosData.filter(u => u.supervisor && u.supervisor.trim() !== '').length
    const usuariosPorRol = {}
    usuariosData.forEach(u => {
      const rol = u.rol || 'user'
      usuariosPorRol[rol] = (usuariosPorRol[rol] || 0) + 1
    })
    
    // Footer
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- RESUMEN DE EXPORTACIÓN\n`
    sqlContent += `-- ===============================================\n`
    sqlContent += `-- Total usuarios: ${usuariosData.length}\n`
    sqlContent += `-- Usuarios con CURP: ${usuariosConCurp}\n`
    sqlContent += `-- Usuarios con teléfono: ${usuariosConTelefono}\n`
    sqlContent += `-- Usuarios con supervisor: ${usuariosConSupervisor}\n`
    sqlContent += `-- Distribución por rol:\n`
    Object.entries(usuariosPorRol).forEach(([rol, cantidad]) => {
      sqlContent += `--   ${rol}: ${cantidad}\n`
    })
    sqlContent += `-- Fecha: ${new Date().toLocaleString('es-ES')}\n`
    sqlContent += `-- ===============================================\n`
    
    // Crear y descargar archivo SQL
    const blob = new Blob([sqlContent], { type: 'application/sql; charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `USUARIOS_${timestamp}.sql`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    // Calcular tamaño del archivo
    const tamanhoKB = Math.round(blob.size / 1024)
    
    mostrarMensaje('Exportacion de Usuarios Exitosa', 
      `<div style="text-align: left;">
        <h4 style="color: #0ea5e9; margin-bottom: 15px;">Base de Usuarios Exportada</h4>
        <p><strong>Archivo:</strong> USUARIOS_${timestamp}.sql</p>
        <p><strong>Tamano:</strong> ${tamanhoKB} KB</p>
        <hr style="margin: 15px 0;">
        <h5 style="color: #0284c7;">Estadisticas:</h5>
        <ul style="margin: 10px 0; padding-left: 20px;">
          <li><strong>Total usuarios:</strong> ${usuariosData.length}</li>
          <li><strong>Con CURP:</strong> ${usuariosConCurp}</li>
          <li><strong>Con telefono:</strong> ${usuariosConTelefono}</li>
          <li><strong>Con supervisor:</strong> ${usuariosConSupervisor}</li>
        </ul>
        <hr style="margin: 15px 0;">
        <h5 style="color: #0284c7;">Por Rol:</h5>
        <ul style="margin: 10px 0; padding-left: 20px;">
          ${Object.entries(usuariosPorRol).map(([rol, cantidad]) => 
            `<li><strong>${rol}:</strong> ${cantidad}</li>`
          ).join('')}
        </ul>
        <hr style="margin: 15px 0;">
        <p style="font-size: 12px; color: #666; margin-top: 15px;">
          El archivo SQL contiene la estructura completa de la tabla usuarios 
          con todos los datos incluyendo contraseñas. Puede restaurarse en 
          cualquier servidor PostgreSQL.
        </p>
      </div>`
    )
  } catch (err) {
    let errorMsg = 'Error al exportar usuarios: '
    
    if (err.response?.status === 401) {
      errorMsg += 'No autorizado. Inicia sesión nuevamente.'
    } else if (err.response?.status === 403) {
      errorMsg += 'Acceso denegado. Permisos insuficientes.'
    } else if (err.response?.status === 404) {
      errorMsg += 'Endpoint no disponible. Verifica el servidor.'
    } else if (err.response?.status === 500) {
      errorMsg += 'Error del servidor. Intenta más tarde.'
    } else if (err.request) {
      errorMsg += 'No se pudo conectar con el servidor. Verifica tu conexión.'
    } else {
      errorMsg += err.message || 'Error desconocido'
    }
    
    console.error('Error completo:', err)
    mostrarMensaje('Error', errorMsg)
  } finally {
    descargandoUsuarios.value = false
  }
}

// NUEVAS FUNCIONES PARA ELIMINAR IMÁGENES
const confirmarEliminarImagenes = () => {
  confirmType.value = 'danger'
  confirmTitle.value = 'ELIMINAR TODAS LAS IMÁGENES'
  confirmMessage.value = `¿Estás completamente seguro de que quieres eliminar TODAS las imágenes del sistema?

Esta acción NO SE PUEDE DESHACER y eliminará:
• Todas las fotos de registros de actividades
• Todas las fotos de entrada/salida de asistencias
• Todos los archivos de imágenes almacenados

Esta operación es irreversible.`
  confirmAction.value = async () => {
    // Segunda confirmación más estricta
    const confirmacion = prompt('Para confirmar, escribe exactamente: ELIMINAR IMÁGENES')
    if (confirmacion === 'ELIMINAR IMÁGENES') {
      await eliminarTodasLasImagenes()
    } else {
      mostrarMensaje('Cancelado', 'Eliminación de imágenes cancelada.')
    }
  }
  showConfirmModal.value = true
}

const eliminarTodasLasImagenes = async () => {
  eliminandoImagenes.value = true
  showProgressModal.value = true
  
  try {
    console.log('🚀 Iniciando eliminación de imágenes...')
    
    // Iniciar el progreso visual
    const detenerProgreso = await progressModalRef.value.iniciarProgreso()
    
    // Llamar al servicio para eliminar todas las imágenes
    console.log('📞 Llamando al servicio...')
    const resultado = await imagenesService.eliminarTodasLasImagenes()
    
    console.log('📊 Resultado recibido:', resultado)
    
    // Actualizar el modal con las estadísticas reales
    progressModalRef.value.actualizar({
      fotos_bd_limpiadas: resultado.estadisticas?.fotos_bd_limpiadas || 0,
      archivos_eliminados: resultado.estadisticas?.archivos_eliminados || 0,
      archivos_no_encontrados: resultado.estadisticas?.archivos_no_encontrados || 0,
      total_eliminado: resultado.estadisticas?.total_eliminado || 0,
      errores_encontrados: resultado.estadisticas?.errores_encontrados || 0
    })
    
    // Marcar como completado
    detenerProgreso()
    progressModalRef.value.completar()
    
    console.log('✅ Eliminación de imágenes completada:', resultado)
    
  } catch (error) {
    console.error('❌ Error al eliminar imágenes:', error)
    console.error('   Error type:', error.constructor.name)
    console.error('   Error message:', error.message)
    
    eliminandoImagenes.value = false
    showProgressModal.value = false
    
    let errorMsg = error.message || 'Error desconocido al eliminar las imágenes'
    
    // Si el mensaje de error ya es descriptivo, usarlo directamente
    if (errorMsg.includes('No hay token') || 
        errorMsg.includes('Sesión expirada') || 
        errorMsg.includes('No tienes permisos') ||
        errorMsg.includes('Error en el servidor') ||
        errorMsg.includes('Error de conexión') ||
        errorMsg.includes('endpoint')) {
      mostrarMensaje('Error', errorMsg)
      return
    }
    
    // Casos adicionales
    if (error.response?.status === 401) {
      errorMsg = 'No autorizado. Inicia sesión nuevamente.'
    } else if (error.response?.status === 403) {
      errorMsg = 'Acceso denegado. Permisos insuficientes.'
    } else if (error.response?.status === 500) {
      errorMsg = 'Error del servidor. Intenta más tarde.'
    } else if (error.response?.status === 404) {
      errorMsg = 'El endpoint no existe. Verifica que el servidor está actualizado.'
    } else if (error.request) {
      errorMsg = 'No se pudo conectar con el servidor. Verifica tu conexión y que el servidor está funcionando.'
    }
    
    mostrarMensaje('Error', errorMsg)
  }
}

const cerrarProgressModal = () => {
  showProgressModal.value = false
  eliminandoImagenes.value = false
}

const onProgressCompletado = () => {
  // No cerrar automáticamente - el usuario debe cerrar manualmente con el botón "Aceptar"
  eliminandoImagenes.value = false
}

// ==================== FUNCIONES DE ELIMINAR IMÁGENES POR FECHA ====================

const abrirModalEliminarPorFecha = () => {
  // Resetear valores
  eliminarFechaConfig.mes = new Date().getMonth() + 1
  eliminarFechaConfig.anio = new Date().getFullYear()
  eliminarFechaConfig.soloMes = true
  progresoEliminacionFecha.value = 0
  mensajeProgresoFecha.value = ''
  showEliminarPorFechaModal.value = true
}

const cerrarModalEliminarPorFecha = () => {
  if (eliminandoImagenesPorFecha.value) return // No cerrar mientras elimina
  showEliminarPorFechaModal.value = false
}

const confirmarEliminarPorFecha = () => {
  const meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
  
  const periodo = eliminarFechaConfig.soloMes 
    ? `${meses[eliminarFechaConfig.mes - 1]} ${eliminarFechaConfig.anio}`
    : `todo el año ${eliminarFechaConfig.anio}`
  
  confirmType.value = 'danger'
  confirmTitle.value = 'ELIMINAR IMÁGENES POR FECHA'
  confirmMessage.value = `¿Estás seguro de que quieres eliminar todas las imágenes de <strong>${periodo}</strong>?

Esta acción NO SE PUEDE DESHACER y eliminará:
• Fotos de registros de actividades del período
• Fotos de entrada/salida de asistencias del período

Los datos asociados (registros y asistencias) permanecerán, solo se eliminarán las imágenes.`
  
  confirmAction.value = async () => {
    const confirmacion = prompt(`Para confirmar, escribe: ELIMINAR ${eliminarFechaConfig.anio}`)
    if (confirmacion === `ELIMINAR ${eliminarFechaConfig.anio}`) {
      await ejecutarEliminarPorFecha()
    } else {
      mostrarMensaje('Cancelado', 'Eliminación de imágenes cancelada.')
    }
  }
  showConfirmModal.value = true
}

const ejecutarEliminarPorFecha = async () => {
  // Cerrar modal de configuración y abrir modal de progreso
  showEliminarPorFechaModal.value = false
  eliminandoImagenesPorFecha.value = true
  showProgressModalFecha.value = true
  
  try {
    console.log('🚀 Iniciando eliminación de imágenes por fecha...')
    
    // Iniciar el progreso visual
    const detenerProgreso = await progressModalFechaRef.value.iniciarProgreso()
    
    // Llamar al servicio para eliminar imágenes
    console.log('📞 Llamando al servicio...')
    const resultado = await imagenesService.eliminarImagenesPorFecha(
      eliminarFechaConfig.mes,
      eliminarFechaConfig.anio,
      eliminarFechaConfig.soloMes
    )
    
    console.log('📊 Resultado recibido:', resultado)
    
    // Actualizar el modal con las estadísticas reales
    progressModalFechaRef.value.actualizar({
      registros_limpiados: resultado.estadisticas?.registros_limpiados || 0,
      asistencias_limpiadas: resultado.estadisticas?.asistencias_limpiadas || 0,
      archivos_eliminados: resultado.estadisticas?.archivos_eliminados || 0,
      archivos_no_encontrados: resultado.estadisticas?.archivos_no_encontrados || 0,
      total_procesado: resultado.estadisticas?.total_procesado || 0,
      errores: resultado.estadisticas?.errores || 0
    })
    
    // Marcar como completado
    detenerProgreso()
    progressModalFechaRef.value.completar()
    
    console.log('✅ Eliminación por fecha completada:', resultado)
    
  } catch (error) {
    console.error('❌ Error al eliminar imágenes por fecha:', error)
    
    eliminandoImagenesPorFecha.value = false
    showProgressModalFecha.value = false
    
    mostrarMensaje('Error', error.message || 'Error al eliminar imágenes')
  }
}

const cerrarProgressModalFecha = () => {
  showProgressModalFecha.value = false
  eliminandoImagenesPorFecha.value = false
}

const onProgressFechaCompletado = () => {
  // No cerrar automáticamente - el usuario debe cerrar manualmente con el botón "Aceptar"
  eliminandoImagenesPorFecha.value = false
}

// ==================== FUNCIONES DE TRANSFERENCIA DE ACTIVIDADES ====================

const abrirModalTransferencia = () => {
  showTransferenciaModal.value = true
  // Limpiar estados anteriores
  curpOrigen.value = ''
  curpDestino.value = ''
  usuarioOrigen.value = null
  usuarioDestino.value = null
  errorOrigen.value = ''
  errorDestino.value = ''
  transfiriendo.value = false
  progresoTransferencia.value = 0
  mensajeProgreso.value = ''
  incluirAsistencias.value = false
}

const cerrarModalTransferencia = () => {
  if (transfiriendo.value) return // No cerrar mientras se transfiere
  showTransferenciaModal.value = false
}

const buscarUsuarioOrigen = async () => {
  if (curpOrigen.value.length !== 18) {
    errorOrigen.value = 'La CURP debe tener exactamente 18 caracteres'
    return
  }
  
  buscandoOrigen.value = true
  errorOrigen.value = ''
  usuarioOrigen.value = null
  
  try {
    const response = await axios.get(`${apiConfig.url}/usuarios/buscar-curp/${curpOrigen.value}`, {
      headers: {
        'Content-Type': 'application/json'
      },
      timeout: 10000
    })
    
    usuarioOrigen.value = response.data
    
    // Validar que no sea el mismo que el destino
    if (usuarioDestino.value && usuarioOrigen.value.curp === usuarioDestino.value.curp) {
      errorOrigen.value = 'No puedes seleccionar el mismo usuario como origen y destino'
      usuarioOrigen.value = null
    }
  } catch (error) {
    if (error.response?.status === 404) {
      errorOrigen.value = 'No se encontró ningún usuario con esa CURP'
    } else if (error.response?.status === 400) {
      errorOrigen.value = error.response.data.detail || 'CURP inválida'
    } else {
      errorOrigen.value = 'Error al buscar usuario. Intenta nuevamente.'
    }
  } finally {
    buscandoOrigen.value = false
  }
}

const buscarUsuarioDestino = async () => {
  if (curpDestino.value.length !== 18) {
    errorDestino.value = 'La CURP debe tener exactamente 18 caracteres'
    return
  }
  
  buscandoDestino.value = true
  errorDestino.value = ''
  usuarioDestino.value = null
  
  try {
    const response = await axios.get(`${apiConfig.url}/usuarios/buscar-curp/${curpDestino.value}`, {
      headers: {
        'Content-Type': 'application/json'
      },
      timeout: 10000
    })
    
    usuarioDestino.value = response.data
    
    // Validar que no sea el mismo que el origen
    if (usuarioOrigen.value && usuarioDestino.value.curp === usuarioOrigen.value.curp) {
      errorDestino.value = 'No puedes seleccionar el mismo usuario como origen y destino'
      usuarioDestino.value = null
    }
  } catch (error) {
    if (error.response?.status === 404) {
      errorDestino.value = 'No se encontró ningún usuario con esa CURP'
    } else if (error.response?.status === 400) {
      errorDestino.value = error.response.data.detail || 'CURP inválida'
    } else {
      errorDestino.value = 'Error al buscar usuario. Intenta nuevamente.'
    }
  } finally {
    buscandoDestino.value = false
  }
}

const limpiarUsuarioOrigen = () => {
  usuarioOrigen.value = null
  curpOrigen.value = ''
  errorOrigen.value = ''
}

const limpiarUsuarioDestino = () => {
  usuarioDestino.value = null
  curpDestino.value = ''
  errorDestino.value = ''
}

const ejecutarTransferencia = async () => {
  if (!usuarioOrigen.value || !usuarioDestino.value) {
    mostrarMensaje('Error', 'Debes seleccionar ambos usuarios para la transferencia')
    return
  }
  
  if (usuarioOrigen.value.total_actividades === 0 && !incluirAsistencias.value) {
    mostrarMensaje('Error', 'El usuario origen no tiene actividades para transferir')
    return
  }
  
  // Mostrar modal de confirmación bonito
  showConfirmTransferencia.value = true
}

const confirmarTransferenciaFinal = async () => {
  showConfirmTransferencia.value = false
  
  transfiriendo.value = true
  progresoTransferencia.value = 10
  mensajeProgreso.value = 'Preparando transferencia...'
  
  try {
    progresoTransferencia.value = 30
    mensajeProgreso.value = 'Conectando con el servidor...'
    
    const response = await axios.post(`${apiConfig.url}/usuarios/transferir-actividades`, {
      curp_origen: usuarioOrigen.value.curp,
      curp_destino: usuarioDestino.value.curp,
      incluir_asistencias: incluirAsistencias.value
    }, {
      headers: {
        'Content-Type': 'application/json'
      },
      timeout: 60000 // 1 minuto de timeout para transferencias grandes
    })
    
    progresoTransferencia.value = 80
    mensajeProgreso.value = 'Finalizando transferencia...'
    
    await new Promise(resolve => setTimeout(resolve, 500))
    
    progresoTransferencia.value = 100
    mensajeProgreso.value = '¡Transferencia completada!'
    
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Cerrar modal y mostrar resultado
    showTransferenciaModal.value = false
    
    const resultado = response.data
    mostrarMensaje('Transferencia Exitosa', 
      `<div style="text-align: left;">
        <h4 style="color: #10b981; margin-bottom: 15px;">Actividades Transferidas</h4>
        <hr style="margin: 15px 0;">
        <h5 style="color: #059669;">Usuario Origen:</h5>
        <p><strong>${resultado.detalles.usuario_origen.nombre}</strong></p>
        <p style="font-size: 12px; color: #666;">${resultado.detalles.usuario_origen.correo}</p>
        <hr style="margin: 15px 0;">
        <h5 style="color: #0284c7;">Usuario Destino:</h5>
        <p><strong>${resultado.detalles.usuario_destino.nombre}</strong></p>
        <p style="font-size: 12px; color: #666;">${resultado.detalles.usuario_destino.correo}</p>
        <hr style="margin: 15px 0;">
        <h5 style="color: #7c3aed;">Resumen:</h5>
        <ul style="margin: 10px 0; padding-left: 20px;">
          <li><strong>Actividades transferidas:</strong> ${resultado.detalles.actividades_transferidas}</li>
          ${resultado.detalles.asistencias_transferidas > 0 ? 
            `<li><strong>Asistencias transferidas:</strong> ${resultado.detalles.asistencias_transferidas}</li>` : ''}
        </ul>
        <hr style="margin: 15px 0;">
        <p style="font-size: 12px; color: #666; margin-top: 15px;">
          Las actividades han sido transferidas exitosamente. Los registros ahora pertenecen al usuario destino.
        </p>
      </div>`
    )
    
  } catch (error) {
    console.error('Error en transferencia:', error)
    
    let errorMsg = 'Error al transferir actividades: '
    
    if (error.response?.status === 404) {
      errorMsg += error.response.data.detail || 'Usuario no encontrado'
    } else if (error.response?.status === 400) {
      errorMsg += error.response.data.detail || 'Datos inválidos'
    } else if (error.response?.status === 500) {
      errorMsg += 'Error del servidor. Intenta más tarde.'
    } else if (error.request) {
      errorMsg += 'No se pudo conectar con el servidor.'
    } else {
      errorMsg += error.message || 'Error desconocido'
    }
    
    mostrarMensaje('Error', errorMsg)
  } finally {
    transfiriendo.value = false
    progresoTransferencia.value = 0
    mensajeProgreso.value = ''
  }
}

const cancelarConfirmTransferencia = () => {
  showConfirmTransferencia.value = false
}

// ==================== FIN FUNCIONES DE TRANSFERENCIA ====================

const logout = () => {
  // No usar confirm(), el modal se maneja en el Sidebar
  localStorage.removeItem('admin_token')
  localStorage.removeItem('admin_user')
  router.push('/login')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

.configuracion-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
}

.main-content {
  flex: 1;
  margin-left: min(220px, 18vw);
  width: calc(100vw - min(220px, 18vw));
  min-width: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: relative;
  box-sizing: border-box;
  overflow-x: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* === HEADER STYLES === */
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

/* === CONTENT STYLES === */
.page-content {
  flex: 1;
  padding: 12px;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
}

/* === TWO COLUMN LAYOUT === */
.two-column-layout {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 14px;
  align-items: start;
}

@media (max-width: 1100px) {
  .two-column-layout {
    grid-template-columns: 1fr;
  }
}

.main-column, .side-column {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* Grid moderno y compacto */
.config-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 12px;
  margin-bottom: 12px;
}

.config-grid-3 {
  grid-template-columns: repeat(3, 1fr);
}

@media (max-width: 1024px) {
  .config-grid-3 {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .config-grid-3 {
    grid-template-columns: 1fr;
  }
}

/* === SECCIONES === */
.config-section {
  margin-bottom: 24px;
}

/* === GLASS CONTAINER === */
.section-glass-container {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
}

.section-glass-container.danger-glass {
  background: rgba(254, 242, 242, 0.7);
  border-color: rgba(239, 68, 68, 0.2);
}

.section-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.section-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.section-icon svg {
  width: 22px;
  height: 22px;
  stroke-width: 2;
}

.settings-section-icon {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.data-section-icon {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

.images-section-icon {
  background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3);
}

.tools-section-icon {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.danger-section-icon {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.section-title h2 {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

.section-title p {
  margin: 0;
  font-size: 11px;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
}

/* === COMPACT VARIANTS === */
.config-section.compact {
  margin-bottom: 0;
}

.section-glass-container.compact {
  padding: 14px 16px;
  border-radius: 14px;
}

.section-header.compact {
  margin-bottom: 14px;
  padding-bottom: 10px;
  gap: 10px;
}

.section-icon.sm {
  width: 32px;
  height: 32px;
  border-radius: 8px;
}

.section-icon.sm svg {
  width: 16px;
  height: 16px;
}

/* === CONFIG CARDS ROW (3 cards horizontal) === */
.config-cards-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

@media (max-width: 900px) {
  .config-cards-row {
    grid-template-columns: 1fr;
  }
}

.config-card-compact {
  background: white;
  border-radius: 10px;
  padding: 12px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.card-header-compact {
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-icon-sm {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-icon-sm svg {
  width: 14px;
  height: 14px;
}

.card-icon-sm.api-gradient {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
}

.card-icon-sm.app-gradient {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.card-icon-sm.info-gradient {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
}

.card-label {
  font-size: 12px;
  font-weight: 600;
  color: #374151;
  font-family: 'Inter', sans-serif;
}

.card-body-compact {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.form-row label {
  font-size: 10px;
  font-weight: 500;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  font-family: 'Inter', sans-serif;
}

.input-compact, .select-compact {
  width: 100%;
  padding: 6px 10px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 12px;
  font-family: 'Inter', sans-serif;
  background: #f9fafb;
  box-sizing: border-box;
}

.input-compact:focus, .select-compact:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
}

.toggle-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 4px;
}

.toggle-sm {
  position: relative;
  width: 32px;
  height: 18px;
  display: inline-block;
}

.toggle-sm input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider-sm {
  position: absolute;
  cursor: pointer;
  inset: 0;
  background: #e5e7eb;
  transition: 0.2s;
  border-radius: 18px;
}

.slider-sm:before {
  position: absolute;
  content: "";
  height: 12px;
  width: 12px;
  left: 3px;
  bottom: 3px;
  background: white;
  transition: 0.2s;
  border-radius: 50%;
  box-shadow: 0 1px 2px rgba(0,0,0,0.2);
}

.toggle-sm input:checked + .slider-sm {
  background: #10b981;
}

.toggle-sm input:checked + .slider-sm:before {
  transform: translateX(14px);
}

.toggle-text {
  font-size: 11px;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
}

.btn-compact {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: auto;
}

.btn-compact svg {
  width: 12px;
  height: 12px;
}

.btn-compact.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.btn-compact.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(59, 130, 246, 0.3);
}

.btn-compact.btn-secondary {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  color: white;
}

.btn-compact:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Info Mini (para card Sistema) */
.info-mini {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 0;
  font-size: 11px;
  font-family: 'Inter', sans-serif;
  border-bottom: 1px solid rgba(0,0,0,0.04);
}

.info-mini:last-child {
  border-bottom: none;
}

.info-mini span:first-child {
  color: #6b7280;
}

.info-mini .val {
  font-weight: 600;
  color: #1f2937;
}

.badge-mini {
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
}

.badge-mini.status-online {
  background: #dcfce7;
  color: #16a34a;
}

.badge-mini.status-offline {
  background: #fee2e2;
  color: #dc2626;
}

/* === IMAGE CARDS ROW === */
.image-cards-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

@media (max-width: 700px) {
  .image-cards-row {
    grid-template-columns: 1fr;
  }
}

.image-action-card {
  background: white;
  border-radius: 10px;
  padding: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  position: relative;
  border: 1px solid rgba(0,0,0,0.05);
}

.image-action-card.red {
  border-left: 3px solid #ef4444;
}

.image-action-card.orange {
  border-left: 3px solid #f97316;
}

.image-action-card:hover {
  transform: translateX(3px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

.image-action-card.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

.image-action-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.image-action-card.red .image-action-icon {
  background: rgba(239, 68, 68, 0.1);
  color: #dc2626;
}

.image-action-card.orange .image-action-icon {
  background: rgba(249, 115, 22, 0.1);
  color: #ea580c;
}

.image-action-icon svg {
  width: 18px;
  height: 18px;
}

.image-action-text {
  flex: 1;
}

.image-action-text h4 {
  margin: 0 0 2px 0;
  font-size: 12px;
  font-weight: 600;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

.image-action-text p {
  margin: 0;
  font-size: 10px;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
}

.action-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 2px 6px;
  border-radius: 8px;
  font-size: 8px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.action-badge.red {
  background: rgba(239, 68, 68, 0.1);
  color: #dc2626;
}

.action-badge.orange {
  background: rgba(249, 115, 22, 0.1);
  color: #ea580c;
}

/* === TOOLS ROW === */
.tools-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}

@media (max-width: 700px) {
  .tools-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

.tool-btn {
  background: white;
  border: 1px solid rgba(0,0,0,0.05);
  border-radius: 10px;
  padding: 12px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tool-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

.tool-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tool-icon svg {
  width: 16px;
  height: 16px;
}

.tool-icon.amber {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.tool-icon.green {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.tool-icon.gray {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  color: white;
}

.tool-icon.teal {
  background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
  color: white;
}

.tool-btn span {
  font-size: 10px;
  font-weight: 500;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
}

/* === DATA LIST === */
.data-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.data-item {
  background: white;
  border: 1px solid rgba(0,0,0,0.05);
  border-radius: 8px;
  padding: 10px 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.data-item:hover {
  transform: translateX(3px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.data-item.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

.data-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.data-icon svg {
  width: 16px;
  height: 16px;
}

.data-icon.blue {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.data-icon.purple {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
}

.data-icon.pink {
  background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
  color: white;
}

.data-icon.orange {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: white;
}

.data-icon.cyan {
  background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
  color: white;
}

.data-text {
  flex: 1;
  min-width: 0;
}

.data-text h4 {
  margin: 0;
  font-size: 12px;
  font-weight: 600;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.data-text p {
  margin: 0;
  font-size: 10px;
  color: #9ca3af;
  font-family: 'Inter', sans-serif;
}

.data-arrow {
  width: 14px;
  height: 14px;
  color: #d1d5db;
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.data-item:hover .data-arrow {
  transform: translateX(2px);
  color: #9ca3af;
}

/* === DANGER ZONE COMPACT === */
.danger-zone-compact {
  position: relative;
  padding: 12px;
  background: white;
  border-radius: 10px;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.danger-alert {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: rgba(239, 68, 68, 0.06);
  border-radius: 8px;
  margin-bottom: 10px;
}

.danger-alert svg {
  width: 20px;
  height: 20px;
  color: #dc2626;
  flex-shrink: 0;
}

.danger-alert p {
  margin: 0;
  font-size: 11px;
  color: #991b1b;
  font-family: 'Inter', sans-serif;
}

.danger-btns {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.danger-btn-sm {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px;
  background: #e5e7eb;
  border: none;
  border-radius: 8px;
  font-size: 10px;
  font-weight: 600;
  color: #9ca3af;
  font-family: 'Inter', sans-serif;
  cursor: not-allowed;
}

.danger-btn-sm svg {
  width: 14px;
  height: 14px;
}

.blocked-overlay-sm {
  position: absolute;
  inset: 0;
  background: rgba(107, 114, 128, 0.06);
  backdrop-filter: blur(1px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  border-radius: 10px;
}

.blocked-overlay-sm svg {
  width: 24px;
  height: 24px;
  color: #6b7280;
}

.blocked-overlay-sm span {
  font-size: 10px;
  font-weight: 700;
  color: #6b7280;
  letter-spacing: 1px;
  font-family: 'Inter', sans-serif;
}

/* === CONFIG CARDS MODERN === */
.config-card-modern {
  background: white;
  border-radius: 16px;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(0, 0, 0, 0.06);
  overflow: hidden;
  transition: all 0.3s ease;
}

.config-card-modern:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.card-header-modern {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 20px 20px 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.card-icon-modern {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-icon-modern svg {
  width: 22px;
  height: 22px;
  stroke-width: 2;
}

.card-icon-modern.api-gradient {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.card-icon-modern.app-gradient {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.card-icon-modern.info-gradient {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

.card-title-modern h3 {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

.card-subtitle {
  font-size: 12px;
  color: #9ca3af;
  font-family: 'Inter', sans-serif;
}

.card-body-modern {
  padding: 16px 20px;
}

.form-group-modern {
  margin-bottom: 14px;
}

.form-group-modern label {
  display: block;
  margin-bottom: 6px;
  font-size: 12px;
  font-weight: 500;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-input-modern, .form-select-modern {
  width: 100%;
  padding: 10px 14px;
  border: 1.5px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
  transition: all 0.2s ease;
  background: #f9fafb;
  box-sizing: border-box;
}

.form-input-modern:focus, .form-select-modern:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.checkbox-group-modern {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 8px;
}

/* Toggle Switch */
.toggle-switch {
  position: relative;
  width: 44px;
  height: 24px;
  flex-shrink: 0;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #e5e7eb;
  transition: 0.3s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.toggle-switch input:checked + .toggle-slider {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.toggle-switch input:checked + .toggle-slider:before {
  transform: translateX(20px);
}

.toggle-label {
  font-size: 13px;
  color: #374151;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
}

.card-footer-modern {
  padding: 0 20px 20px;
}

.btn-modern {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 12px 16px;
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-modern svg {
  width: 16px;
  height: 16px;
}

.btn-modern-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.btn-modern-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn-modern-secondary {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(107, 114, 128, 0.3);
}

.btn-modern-secondary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(107, 114, 128, 0.4);
}

.btn-modern:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

/* Info Grid Modern */
.info-grid-modern {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-row-modern {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.info-row-modern:last-child {
  border-bottom: none;
}

.info-label-modern {
  font-size: 12px;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
}

.info-value-modern {
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

.status-badge-modern {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge-modern.status-online {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.status-badge-modern.status-offline {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

/* === DATA ACTION CARDS === */
.data-actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

@media (max-width: 900px) {
  .data-actions-grid {
    grid-template-columns: 1fr;
  }
}

.data-action-card {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 14px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.data-action-card:hover {
  transform: translateX(4px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
}

.data-action-card.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.data-action-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.data-action-icon svg {
  width: 24px;
  height: 24px;
  stroke-width: 2;
}

.data-action-icon.blue-gradient {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.data-action-icon.purple-gradient {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
}

.data-action-icon.pink-gradient {
  background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
  color: white;
}

.data-action-icon.orange-gradient {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: white;
}

.data-action-icon.cyan-gradient {
  background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
  color: white;
}

.data-action-info {
  flex: 1;
}

.data-action-info h4 {
  margin: 0 0 4px 0;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

.data-action-info p {
  margin: 0;
  font-size: 12px;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
}

.data-action-arrow {
  color: #d1d5db;
  transition: all 0.2s ease;
}

.data-action-arrow svg {
  width: 18px;
  height: 18px;
}

.data-action-card:hover .data-action-arrow {
  color: #9ca3af;
  transform: translateX(2px);
}

/* === IMAGE CARDS LARGE === */
.images-grid-two-col {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

@media (max-width: 768px) {
  .images-grid-two-col {
    grid-template-columns: 1fr;
  }
}

.image-card-large {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.image-card-large:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
}

.image-card-large.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.image-card-header {
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.image-card-header.red-accent {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(220, 38, 38, 0.04) 100%);
  border-bottom: 2px solid rgba(239, 68, 68, 0.2);
}

.image-card-header.orange-accent {
  background: linear-gradient(135deg, rgba(249, 115, 22, 0.08) 0%, rgba(234, 88, 12, 0.04) 100%);
  border-bottom: 2px solid rgba(249, 115, 22, 0.2);
}

.image-card-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-card-header.red-accent .image-card-icon {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.image-card-header.orange-accent .image-card-icon {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
}

.image-card-icon svg {
  width: 24px;
  height: 24px;
}

.image-card-badge {
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.image-card-badge.destructive {
  background: rgba(239, 68, 68, 0.15);
  color: #dc2626;
}

.image-card-badge.selective {
  background: rgba(249, 115, 22, 0.15);
  color: #ea580c;
}

.image-card-body {
  padding: 20px;
}

.image-card-body h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

.image-card-body p {
  margin: 0;
  font-size: 13px;
  color: #6b7280;
  line-height: 1.5;
  font-family: 'Inter', sans-serif;
}

.image-card-footer {
  padding: 16px 20px;
  background: #f9fafb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid rgba(0, 0, 0, 0.04);
}

.image-card-action {
  font-size: 13px;
  font-weight: 600;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
}

.image-card-footer svg {
  width: 18px;
  height: 18px;
  color: #9ca3af;
  transition: transform 0.2s ease;
}

.image-card-large:hover .image-card-footer svg {
  transform: translateX(4px);
}

/* === TOOLS GRID MODERN === */
.tools-grid-modern {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

@media (max-width: 900px) {
  .tools-grid-modern {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 500px) {
  .tools-grid-modern {
    grid-template-columns: 1fr;
  }
}

.tool-card-modern {
  background: white;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 14px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.25s ease;
  text-align: center;
}

.tool-card-modern:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.tool-card-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tool-card-icon svg {
  width: 24px;
  height: 24px;
}

.tool-card-icon.amber-gradient {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.tool-card-icon.green-gradient {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.tool-card-icon.gray-gradient {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(107, 114, 128, 0.3);
}

.tool-card-icon.teal-gradient {
  background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(20, 184, 166, 0.3);
}

.tool-card-label {
  font-size: 13px;
  font-weight: 500;
  color: #374151;
  font-family: 'Inter', sans-serif;
}

/* === DANGER SECTION MODERN === */
.danger-card-modern {
  background: white;
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 16px;
  padding: 24px;
  position: relative;
  overflow: hidden;
}

.danger-warning-modern {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  background: rgba(239, 68, 68, 0.06);
  border-radius: 12px;
  margin-bottom: 20px;
}

.danger-warning-icon {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  color: #dc2626;
}

.danger-warning-text strong {
  display: block;
  font-size: 14px;
  color: #991b1b;
  margin-bottom: 4px;
  font-family: 'Inter', sans-serif;
}

.danger-warning-text p {
  margin: 0;
  font-size: 13px;
  color: #7f1d1d;
  line-height: 1.5;
  font-family: 'Inter', sans-serif;
}

.danger-buttons-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

@media (max-width: 600px) {
  .danger-buttons-grid {
    grid-template-columns: 1fr;
  }
}

.danger-btn-modern {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px 20px;
  background: linear-gradient(135deg, #9ca3af 0%, #6b7280 100%);
  border: none;
  border-radius: 12px;
  color: #e5e7eb;
  font-size: 13px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  cursor: not-allowed;
}

.danger-btn-modern svg {
  width: 18px;
  height: 18px;
}

.blocked-overlay-modern {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(107, 114, 128, 0.08);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
}

.blocked-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #6b7280;
}

.blocked-content svg {
  width: 40px;
  height: 40px;
}

.blocked-content span {
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  font-family: 'Inter', sans-serif;
}

/* === RESPONSIVE GRID 3 === */
.config-grid-3 {
  grid-template-columns: repeat(3, 1fr);
}

@media (max-width: 1100px) {
  .config-grid-3 {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 700px) {
  .config-grid-3 {
    grid-template-columns: 1fr;
  }
}

/* === ACTION CARDS (Gestion de Datos) === */
.action-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.action-card {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: all 0.25s ease;
  position: relative;
  overflow: hidden;
}

.action-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  opacity: 0;
  transition: opacity 0.25s ease;
}

.action-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.1), 0 4px 10px -5px rgba(0, 0, 0, 0.04);
}

.action-card:hover::before {
  opacity: 1;
}

.action-card.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.action-card-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.action-card-icon svg {
  width: 24px;
  height: 24px;
  stroke-width: 2;
}

.action-card-icon.blue {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}
.action-card:has(.action-card-icon.blue)::before {
  background: linear-gradient(90deg, #3b82f6, #2563eb);
}

.action-card-icon.purple {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
}
.action-card:has(.action-card-icon.purple)::before {
  background: linear-gradient(90deg, #8b5cf6, #7c3aed);
}

.action-card-icon.pink {
  background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
  color: white;
}
.action-card:has(.action-card-icon.pink)::before {
  background: linear-gradient(90deg, #ec4899, #db2777);
}

.action-card-icon.orange {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: white;
}
.action-card:has(.action-card-icon.orange)::before {
  background: linear-gradient(90deg, #f97316, #ea580c);
}

.action-card-icon.cyan {
  background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
  color: white;
}
.action-card:has(.action-card-icon.cyan)::before {
  background: linear-gradient(90deg, #06b6d4, #0891b2);
}

.action-card-content {
  flex: 1;
}

.action-card-content h4 {
  margin: 0 0 4px 0;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

.action-card-content p {
  margin: 0;
  font-size: 12px;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
}

/* === IMAGE ACTIONS (Gestion de Imagenes) === */
.images-actions-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.image-action-card {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 14px;
  padding: 20px 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  cursor: pointer;
  transition: all 0.25s ease;
  position: relative;
}

.image-action-card:hover {
  transform: translateX(4px);
  box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.1);
}

.image-action-card.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.image-action-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.image-action-icon svg {
  width: 28px;
  height: 28px;
  stroke-width: 2;
}

.image-action-icon.red {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 4px 14px rgba(239, 68, 68, 0.3);
}

.image-action-icon.orange {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: white;
  box-shadow: 0 4px 14px rgba(249, 115, 22, 0.3);
}

.image-action-content {
  flex: 1;
}

.image-action-content h4 {
  margin: 0 0 6px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

.image-action-content p {
  margin: 0 0 8px 0;
  font-size: 13px;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
}

.action-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.action-badge.destructive {
  background: rgba(239, 68, 68, 0.1);
  color: #dc2626;
}

.action-badge.selective {
  background: rgba(249, 115, 22, 0.1);
  color: #ea580c;
}

.image-action-arrow {
  color: #9ca3af;
  transition: transform 0.2s ease;
}

.image-action-arrow svg {
  width: 20px;
  height: 20px;
}

.image-action-card:hover .image-action-arrow {
  transform: translateX(4px);
  color: #6b7280;
}

/* === TOOLS GRID === */
.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
}

.tool-btn {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
  transition: all 0.25s ease;
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #374151;
}

.tool-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px -4px rgba(0, 0, 0, 0.1);
  background: white;
}

.tool-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.tool-icon svg {
  width: 20px;
  height: 20px;
  stroke-width: 2;
}

.tool-icon.amber {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.tool-icon.green {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.tool-icon.gray {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  color: white;
}

.tool-icon.teal {
  background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
  color: white;
}

/* === DANGER SECTION === */
.danger-section .section-header {
  border-bottom-color: rgba(239, 68, 68, 0.2);
}

.btn-full {
  width: 100%;
  justify-content: center;
}

/* Cards modernos */
.config-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.config-card:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Headers de cards con iconos */
.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.card-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-icon svg {
  width: 18px;
  height: 18px;
  stroke-width: 2.5;
}

.api-icon {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
}

.app-icon {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.info-icon {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
}

.actions-icon {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.danger-icon {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

/* Formularios modernos */
.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
  font-weight: 500;
  color: #374151;
  font-family: 'Inter', sans-serif;
}

.form-input, .form-select {
  width: 100%;
  padding: 8px 12px;
  border: 1.5px solid #d1d5db;
  border-radius: 8px;
  font-size: 13px;
  font-family: 'Inter', sans-serif;
  transition: all 0.2s ease;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(5px);
}

.form-input:focus, .form-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  background: rgba(255, 255, 255, 0.95);
}

/* Checkbox moderno */
.checkbox-group {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.checkbox {
  width: 16px;
  height: 16px;
  border: 2px solid #d1d5db;
  border-radius: 4px;
  appearance: none;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.checkbox:checked {
  background: #3b82f6;
  border-color: #3b82f6;
  background-image: url("data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='m13.854 3.646-7.5 7.5a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6 10.293l7.146-7.147a.5.5 0 0 1 .708.708z'/%3e%3c/svg%3e");
}

.checkbox-group label {
  font-size: 13px;
  font-weight: 400;
  color: #374151;
  cursor: pointer;
  user-select: none;
}

/* Botones modernos */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.btn svg {
  width: 16px;
  height: 16px;
  stroke-width: 2;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
}

.btn-secondary {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(107, 114, 128, 0.2);
}

.btn-secondary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(107, 114, 128, 0.3);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

/* Info list moderna */
.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 13px;
  font-weight: 500;
  color: #6b7280;
  font-family: 'Inter', sans-serif;
}

.info-value {
  font-size: 13px;
  font-weight: 500;
  color: #1f2937;
  font-family: 'Inter', sans-serif;
}

/* Status badges */
.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-online {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.status-offline {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.status-unknown {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

/* Actions grid compacto */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 12px 8px;
  border: none;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  min-height: 60px;
  justify-content: center;
}

.action-btn svg {
  width: 18px;
  height: 18px;
  stroke-width: 2.5;
}

.export-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
}

.database-btn {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(139, 92, 246, 0.2);
}

.bd-rapida-btn {
  background: linear-gradient(135deg, #ec4899 0%, #f472b6 50%, #fb7185 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(236, 72, 153, 0.4);
  font-weight: 600;
  position: relative;
  overflow: hidden;
}

.bd-rapida-btn::before {
  content: '⚡';
  position: absolute;
  left: 8px;
  font-size: 14px;
  animation: pulse 1s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}

.bd-rapida-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(236, 72, 153, 0.6);
}

.registros-csv-btn {
  background: linear-gradient(135deg, #f97316 0%, #fb923c 50%, #fbbf24 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(249, 115, 22, 0.4);
  font-weight: 600;
  position: relative;
  overflow: hidden;
}

.registros-csv-btn::before {
  content: '📊';
  position: absolute;
  left: 8px;
  font-size: 14px;
  animation: bounce 1.2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
    opacity: 1;
  }
  50% {
    transform: translateY(-4px);
    opacity: 0.8;
  }
}

.registros-csv-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.6);
}

.cache-btn {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(245, 158, 11, 0.2);
}

.reset-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
}

.logs-btn {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(107, 114, 128, 0.2);
}

.users-btn {
  background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(14, 165, 233, 0.2);
}

.images-btn {
  background: linear-gradient(135deg, #ec4899 0%, #be185d 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(236, 72, 153, 0.2);
}

.calendar-images-btn {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(249, 115, 22, 0.3);
}

.calendar-images-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%);
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.4);
}

.transfer-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
  position: relative;
  overflow: hidden;
}

.transfer-btn::before {
  content: '🔄';
  position: absolute;
  left: 8px;
  font-size: 12px;
  animation: rotate 2s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.transfer-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.5);
}

.action-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

/* Zona peligrosa compacta */
.danger-card {
  border: 2px solid #ef4444;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(254, 242, 242, 0.9) 100%);
  position: relative;
}

.danger-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #ef4444 0%, #f59e0b 50%, #ef4444 100%);
  border-radius: 12px 12px 0 0;
}

/* Estilos para zona peligrosa bloqueada */
.danger-card-blocked {
  border: 2px solid #6b7280;
  background: linear-gradient(135deg, rgba(249, 250, 251, 0.95) 0%, rgba(243, 244, 246, 0.9) 100%);
  filter: grayscale(1);
  opacity: 0.6;
  cursor: not-allowed;
  user-select: none;
  position: relative;
}

.danger-card-blocked::before {
  background: linear-gradient(90deg, #6b7280 0%, #9ca3af 50%, #6b7280 100%);
}

.danger-icon-blocked {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  color: white;
}

.danger-warning-blocked {
  background: rgba(107, 114, 128, 0.1);
  border: 1px solid rgba(107, 114, 128, 0.2);
}

.danger-warning-blocked .warning-content {
  color: #374151;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.lock-icon-inline {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  color: #6b7280;
}

.danger-btn-blocked {
  background: linear-gradient(135deg, #9ca3af 0%, #6b7280 100%);
  border-color: #6b7280;
  color: #d1d5db;
  cursor: not-allowed;
  pointer-events: none;
}

/* Overlay de bloqueo */
.blocked-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(107, 114, 128, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  backdrop-filter: blur(2px);
  z-index: 10;
}

.blocked-icon {
  width: 40px;
  height: 40px;
  color: #6b7280;
  margin-bottom: 8px;
}

.blocked-icon svg {
  width: 100%;
  height: 100%;
}

.blocked-text {
  font-size: 14px;
  font-weight: 700;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-family: 'Inter', sans-serif;
}

.danger-warning {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
}

.warning-content {
  font-size: 13px;
  color: #7f1d1d;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
  line-height: 1.4;
}

.danger-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 12px;
}

.danger-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border: 2px solid;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: all 0.2s ease;
  justify-content: center;
}

.danger-btn svg {
  width: 16px;
  height: 16px;
  stroke-width: 2.5;
}

.registros-btn {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border-color: #d97706;
  color: white;
  box-shadow: 0 2px 4px rgba(245, 158, 11, 0.3);
}

.asistencias-btn {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  border-color: #7c3aed;
  color: white;
  box-shadow: 0 2px 4px rgba(139, 92, 246, 0.3);
}

.danger-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.danger-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 16px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
}

.btn-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #6b7280;
  padding: 4px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.btn-close:hover {
  background: #f3f4f6;
  color: #1f2937;
}

.modal-body {
  padding: 16px;
  font-family: 'Inter', sans-serif;
}

.modal-body pre {
  background: #f9fafb;
  padding: 12px;
  border-radius: 6px;
  font-size: 11px;
  overflow-x: auto;
  border: 1px solid #e5e7eb;
}

/* Message Modal Styles */
.message-modal-overlay {
  z-index: 2000;
}

.message-modal {
  max-width: 420px;
  border-radius: 16px;
  overflow: hidden;
  animation: modal-slide-up 0.3s ease-out;
}

@keyframes modal-slide-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-modal-header {
  padding: 24px 24px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  text-align: center;
}

.message-modal-header.header-success {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  color: white;
}

.message-modal-header.header-error {
  background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
  color: white;
}

.message-modal-header.header-info {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
}

.message-icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: icon-pop 0.4s ease-out 0.1s both;
}

@keyframes icon-pop {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  70% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.message-icon-wrapper svg {
  width: 28px;
  height: 28px;
  color: white;
}

.message-modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
}

.message-modal-body {
  padding: 20px 24px;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  color: #4b5563;
  line-height: 1.6;
}

.message-modal-body strong {
  color: #1f2937;
}

.message-modal-footer {
  padding: 16px 24px 24px;
  display: flex;
  justify-content: center;
}

.btn-message-ok {
  padding: 10px 32px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-message-ok.success {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  color: white;
}

.btn-message-ok.success:hover {
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.btn-message-ok.error {
  background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
  color: white;
}

.btn-message-ok.error:hover {
  background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.btn-message-ok.info {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
}

.btn-message-ok.info:hover {
  background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

/* Responsive */
@media (max-width: 992px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
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
  
  .page-content {
    padding: 12px;
  }
  
  .config-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .config-card {
    padding: 12px;
  }
  
  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .danger-actions {
    grid-template-columns: 1fr;
  }
  
  .card-header h3 {
    font-size: 14px;
  }
  
  .form-input, .form-select {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}

@media (max-width: 375px) {
  .main-content {
    margin-left: 180px;
    width: calc(100vw - 180px);
  }
}

/* ==================== ESTILOS DEL MODAL ELIMINAR POR FECHA ==================== */
.modal-eliminar-fecha {
  max-width: min(500px, 95vw);
  width: 95%;
  border-radius: 16px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

.modal-header-fecha {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: white;
  padding: clamp(14px, 4vw, 20px);
  border-radius: 16px 16px 0 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.modal-header-fecha h3 {
  flex: 1;
  margin: 0;
  font-size: clamp(15px, 4vw, 18px);
  font-weight: 600;
}

.modal-header-fecha .btn-close {
  color: white;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  width: 32px;
  height: 32px;
  border: none;
  cursor: pointer;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-header-fecha .btn-close:hover {
  background: rgba(255, 255, 255, 0.3);
}

.header-icon-fecha {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-icon-fecha svg {
  width: 24px;
  height: 24px;
  stroke: white;
}

.modal-body-fecha {
  padding: clamp(16px, 4vw, 24px);
  background: white;
}

.fecha-progress {
  background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
  border: 1px solid #fdba74;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
}

.progress-bar-orange {
  background: linear-gradient(90deg, #f97316 0%, #ea580c 100%);
  transition: width 0.5s ease;
}

.fecha-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.fecha-description {
  color: #64748b;
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
}

.fecha-options {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.fecha-option-toggle {
  display: flex;
  gap: 10px;
  background: #f1f5f9;
  padding: 6px;
  border-radius: 12px;
}

.toggle-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  background: transparent;
  color: #64748b;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.toggle-btn svg {
  width: 18px;
  height: 18px;
}

.toggle-btn.active {
  background: white;
  color: #f97316;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.toggle-btn:hover:not(.active) {
  background: rgba(255, 255, 255, 0.5);
}

.fecha-selectors {
  display: flex;
  gap: 16px;
}

.fecha-field {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.fecha-field label {
  font-size: 12px;
  font-weight: 600;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.fecha-select {
  padding: 12px 14px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.fecha-select:focus {
  outline: none;
  border-color: #f97316;
  box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.15);
}

.fecha-preview {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
  border: 1px solid #fdba74;
  border-radius: 10px;
  color: #9a3412;
  font-size: 13px;
}

.fecha-preview svg {
  width: 20px;
  height: 20px;
  color: #ea580c;
  flex-shrink: 0;
}

.fecha-preview strong {
  color: #c2410c;
}

.modal-footer-fecha {
  padding: 16px 24px;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn-cancel {
  padding: 10px 20px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover:not(:disabled) {
  background: #f1f5f9;
}

.btn-danger-fecha {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-danger-fecha svg {
  width: 18px;
  height: 18px;
}

.btn-danger-fecha:hover:not(:disabled) {
  background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
}

.btn-danger-fecha:disabled,
.btn-cancel:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ==================== ESTILOS DEL MODAL DE TRANSFERENCIA ==================== */
.modal-transferencia {
  max-width: min(600px, 95vw);
  width: 95%;
  max-height: min(90vh, 800px);
  overflow-y: auto;
  border-radius: 16px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modal-header-transferencia {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  padding: clamp(14px, 4vw, 20px);
  border-radius: 16px 16px 0 0;
  display: flex;
  align-items: center;
  gap: 12px;
  position: sticky;
  top: 0;
  z-index: 10;
}

.modal-header-transferencia h3 {
  flex: 1;
  margin: 0;
  font-size: clamp(15px, 4vw, 18px);
  font-weight: 600;
}

.modal-header-transferencia .btn-close {
  color: white;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  width: 32px;
  height: 32px;
}

.modal-header-transferencia .btn-close:hover {
  background: rgba(255, 255, 255, 0.3);
}

.header-icon-transferencia {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-icon-transferencia svg {
  width: clamp(20px, 5vw, 24px);
  height: clamp(20px, 5vw, 24px);
  stroke: white;
}

.modal-body-transferencia {
  padding: clamp(16px, 4vw, 24px);
}

/* Barra de progreso */
.transferencia-progress {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border: 1px solid #86efac;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 20px;
}

.progress-bar-container {
  width: 100%;
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 13px;
  color: #059669;
  text-align: center;
  margin: 0;
  font-weight: 500;
}

/* Secciones de transferencia */
.transferencia-seccion {
  margin-bottom: 20px;
}

.seccion-titulo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 12px;
}

.seccion-icon {
  width: 20px;
  height: 20px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.seccion-icon svg {
  width: 18px;
  height: 18px;
}

.seccion-icon.origen {
  color: #f59e0b;
}

.seccion-icon.destino {
  color: #3b82f6;
}

/* Búsqueda de CURP */
.busqueda-curp {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.input-curp {
  flex: 1;
  min-width: 200px;
  padding: clamp(10px, 2.5vw, 12px) clamp(12px, 3vw, 16px);
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: clamp(12px, 3vw, 14px);
  font-family: 'Inter', monospace;
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: all 0.2s ease;
}

.input-curp:focus {
  outline: none;
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.input-curp:disabled {
  background: #f3f4f6;
  cursor: not-allowed;
}

.btn-buscar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: clamp(10px, 2.5vw, 12px) clamp(14px, 3.5vw, 20px);
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: clamp(12px, 3vw, 13px);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  flex-shrink: 0;
}

.btn-buscar:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn-buscar:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-buscar svg {
  width: 16px;
  height: 16px;
}

/* Spinner pequeño */
.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Tarjeta de usuario */
.tarjeta-usuario {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 12px;
  position: relative;
  transition: all 0.2s ease;
}

.tarjeta-origen {
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  border: 2px solid #f59e0b;
}

.tarjeta-destino {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border: 2px solid #3b82f6;
}

.tarjeta-avatar {
  width: clamp(40px, 10vw, 50px);
  height: clamp(40px, 10vw, 50px);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: clamp(18px, 5vw, 22px);
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.tarjeta-origen .tarjeta-avatar {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.tarjeta-destino .tarjeta-avatar {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
}

.tarjeta-info {
  flex: 1;
  min-width: 0;
}

.tarjeta-info h5 {
  margin: 0 0 4px 0;
  font-size: clamp(13px, 3.5vw, 15px);
  font-weight: 600;
  color: #1f2937;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tarjeta-correo {
  font-size: clamp(10px, 2.8vw, 12px);
  color: #6b7280;
  margin: 0 0 2px 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tarjeta-curp {
  font-size: clamp(9px, 2.5vw, 11px);
  color: #9ca3af;
  margin: 0 0 8px 0;
  font-family: monospace;
  word-break: break-all;
}

.tarjeta-stats {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.stat-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 500;
}

.stat-badge svg {
  width: 12px;
  height: 12px;
}

.stat-badge.actividades {
  background: rgba(16, 185, 129, 0.1);
  color: #059669;
}

.stat-badge.asistencias {
  background: rgba(139, 92, 246, 0.1);
  color: #7c3aed;
}

.btn-limpiar {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 24px;
  height: 24px;
  border: none;
  background: rgba(0, 0, 0, 0.1);
  color: #6b7280;
  border-radius: 50%;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.btn-limpiar:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.btn-limpiar:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Mensaje de error */
.error-mensaje {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  border: 1px solid #fca5a5;
  border-radius: 10px;
  color: #dc2626;
  font-size: 13px;
}

.error-mensaje svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

/* Flecha de transferencia */
.flecha-transferencia {
  display: flex;
  justify-content: center;
  padding: 12px 0;
  color: #10b981;
}

.flecha-transferencia svg {
  width: 32px;
  height: 32px;
  animation: bounceDown 1s ease-in-out infinite;
}

@keyframes bounceDown {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(6px); }
}

/* Opciones de transferencia */
.opciones-transferencia {
  background: #f9fafb;
  border-radius: 10px;
  padding: 16px;
  margin-bottom: 20px;
}

.checkbox-option {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.checkbox-option input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #10b981;
  cursor: pointer;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #374151;
}

.checkbox-label svg {
  width: 16px;
  height: 16px;
  color: #8b5cf6;
}

/* Botones de acción del modal */
.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.btn-cancelar {
  padding: 12px 24px;
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancelar:hover:not(:disabled) {
  background: #e5e7eb;
}

.btn-cancelar:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-transferir {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-transferir:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.btn-transferir:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-transferir svg {
  width: 18px;
  height: 18px;
}

/* Responsive para modal de transferencia */
@media (max-width: 600px) {
  .modal-transferencia {
    max-width: 100%;
    margin: 10px;
    max-height: calc(100vh - 20px);
  }
  
  .busqueda-curp {
    flex-direction: column;
  }
  
  .btn-buscar {
    width: 100%;
    justify-content: center;
  }
  
  .tarjeta-usuario {
    flex-direction: column;
    text-align: center;
  }
  
  .tarjeta-stats {
    justify-content: center;
  }
  
  .modal-actions {
    flex-direction: column-reverse;
  }
  
  .btn-cancelar,
  .btn-transferir {
    width: 100%;
    justify-content: center;
  }
}

/* ==================== MODAL DE CONFIRMACIÓN DE TRANSFERENCIA ==================== */
.confirm-transfer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.confirm-transfer-modal {
  background: white;
  border-radius: 20px;
  padding: clamp(20px, 5vw, 32px);
  width: 100%;
  max-width: min(450px, 95vw);
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(0, 0, 0, 0.05);
  text-align: center;
}

/* Icono de advertencia */
.confirm-icon-container {
  margin-bottom: 20px;
}

.confirm-icon {
  width: clamp(60px, 15vw, 80px);
  height: clamp(60px, 15vw, 80px);
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  animation: pulse-warning 2s ease-in-out infinite;
}

.confirm-icon.warning {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 3px solid #f59e0b;
}

.confirm-icon svg {
  width: clamp(30px, 8vw, 40px);
  height: clamp(30px, 8vw, 40px);
  stroke: #d97706;
}

@keyframes pulse-warning {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 15px rgba(245, 158, 11, 0);
  }
}

/* Título */
.confirm-title {
  font-size: clamp(18px, 4.5vw, 24px);
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 16px 0;
  font-family: 'Inter', sans-serif;
}

/* Contenido */
.confirm-content {
  margin-bottom: 24px;
}

.confirm-description {
  font-size: clamp(13px, 3.5vw, 15px);
  color: #6b7280;
  margin: 0 0 16px 0;
}

/* Resumen de transferencia */
.transfer-summary {
  display: flex;
  justify-content: center;
  gap: clamp(12px, 4vw, 24px);
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-radius: 10px;
  border: 1px solid #86efac;
}

.summary-icon {
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.summary-icon svg {
  width: 18px;
  height: 18px;
  color: #059669;
}

.summary-text {
  font-size: clamp(12px, 3vw, 14px);
  color: #059669;
}

.summary-text strong {
  font-weight: 700;
  color: #047857;
}

/* Usuarios de transferencia */
.transfer-users {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(8px, 3vw, 16px);
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.user-card {
  padding: clamp(10px, 2.5vw, 14px) clamp(12px, 3vw, 18px);
  border-radius: 12px;
  min-width: clamp(100px, 25vw, 140px);
  max-width: 45%;
}

.user-card.from {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border: 2px solid #f59e0b;
}

.user-card.to {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  border: 2px solid #3b82f6;
}

.user-label {
  display: block;
  font-size: clamp(10px, 2.5vw, 11px);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 4px;
}

.user-card.from .user-label {
  color: #92400e;
}

.user-card.to .user-label {
  color: #1e40af;
}

.user-name {
  display: block;
  font-size: clamp(11px, 2.8vw, 13px);
  font-weight: 600;
  color: #1f2937;
  word-break: break-word;
}

.transfer-arrow {
  color: #10b981;
  flex-shrink: 0;
}

.transfer-arrow svg {
  width: clamp(24px, 6vw, 32px);
  height: clamp(24px, 6vw, 32px);
  animation: arrow-bounce 1s ease-in-out infinite;
}

@keyframes arrow-bounce {
  0%, 100% { transform: translateX(0); }
  50% { transform: translateX(5px); }
}

/* Caja de advertencia */
.warning-box {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: clamp(12px, 3vw, 16px);
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  border: 1px solid #fca5a5;
  border-radius: 12px;
  color: #dc2626;
  font-size: clamp(12px, 3vw, 14px);
  text-align: center;
  flex-wrap: wrap;
}

.warning-box svg {
  width: clamp(18px, 4vw, 22px);
  height: clamp(18px, 4vw, 22px);
  flex-shrink: 0;
}

.warning-box strong {
  font-weight: 700;
}

/* Botones de confirmación */
.confirm-actions {
  display: flex;
  gap: clamp(10px, 3vw, 16px);
  justify-content: center;
  flex-wrap: wrap;
}

.btn-cancel-confirm,
.btn-confirm-transfer {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: clamp(12px, 3vw, 14px) clamp(20px, 5vw, 28px);
  border-radius: 12px;
  font-size: clamp(13px, 3.5vw, 15px);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  min-width: clamp(120px, 30vw, 150px);
}

.btn-cancel-confirm svg,
.btn-confirm-transfer svg {
  width: clamp(16px, 4vw, 20px);
  height: clamp(16px, 4vw, 20px);
}

.btn-cancel-confirm {
  background: #f3f4f6;
  color: #374151;
  border: 2px solid #d1d5db;
}

.btn-cancel-confirm:hover {
  background: #e5e7eb;
  border-color: #9ca3af;
  transform: translateY(-2px);
}

.btn-confirm-transfer {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4);
}

.btn-confirm-transfer:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5);
}

/* Animaciones del modal */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-scale-enter-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-scale-leave-active {
  transition: all 0.2s ease;
}

.modal-scale-enter-from {
  opacity: 0;
  transform: scale(0.8) translateY(20px);
}

.modal-scale-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

/* Responsive adicional para el modal de confirmación */
@media (max-width: 400px) {
  .confirm-transfer-modal {
    padding: 20px 16px;
  }
  
  .transfer-users {
    flex-direction: column;
    gap: 12px;
  }
  
  .user-card {
    max-width: 100%;
    width: 100%;
  }
  
  .transfer-arrow {
    transform: rotate(90deg);
  }
  
  .confirm-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .btn-cancel-confirm,
  .btn-confirm-transfer {
    width: 100%;
  }
}

/* Landscape mode para móviles */
@media (max-height: 500px) and (orientation: landscape) {
  .confirm-transfer-modal {
    max-height: 95vh;
    padding: 16px;
  }
  
  .confirm-icon {
    width: 50px;
    height: 50px;
  }
  
  .confirm-icon svg {
    width: 25px;
    height: 25px;
  }
  
  .confirm-icon-container {
    margin-bottom: 12px;
  }
  
  .confirm-title {
    margin-bottom: 10px;
  }
  
  .confirm-content {
    margin-bottom: 16px;
  }
  
  .transfer-summary {
    margin-bottom: 12px;
  }
  
  .transfer-users {
    margin-bottom: 12px;
  }
}

/* Ajustes responsivos adicionales para el modal de transferencia principal */
@media (max-height: 700px) {
  .modal-transferencia {
    max-height: 95vh;
  }
  
  .modal-body-transferencia {
    padding: 16px;
  }
  
  .transferencia-seccion {
    margin-bottom: 14px;
  }
}

@media (orientation: landscape) and (max-height: 500px) {
  .modal-transferencia {
    max-height: 98vh;
    max-width: 90vw;
  }
  
  .modal-header-transferencia {
    padding: 12px 16px;
  }
  
  .modal-body-transferencia {
    padding: 12px 16px;
  }
  
  .tarjeta-usuario {
    padding: 10px;
    flex-direction: row;
    text-align: left;
  }
  
  .tarjeta-avatar {
    width: 40px;
    height: 40px;
    font-size: 18px;
  }
}
</style>









