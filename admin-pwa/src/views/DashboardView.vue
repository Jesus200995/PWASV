<template>
  <div class="dashboard-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">      <header class="dashboard-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="7" height="7"/>
                <rect x="14" y="3" width="7" height="7"/>
                <rect x="14" y="14" width="7" height="7"/>
                <rect x="3" y="14" width="7" height="7"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Panel Administrativo</h1>
              <p class="header-subtitle">Bienvenido, {{ adminUser }}</p>
            </div>
          </div>
          <div class="connection-status" :class="{ 'online': isOnline, 'offline': !isOnline }">
            <div class="status-indicator"></div>
            <span class="status-text">{{ isOnline ? 'En línea' : 'Sin conexión' }}</span>
          </div>
        </div>
      </header>

      <div class="dashboard-content">
        <!-- Estadísticas -->
        <div class="stats-grid">
          <div class="stat-card animated-card" v-for="stat in statCards" :key="stat.label">
            <div class="stat-icon svg-icon" v-html="stat.icon"></div>
            <div class="stat-info">
              <h3>{{ stat.value }}</h3>
              <p>{{ stat.label }}</p>
            </div>
          </div>
        </div>

        <!-- Registros recientes -->
        <div class="section">
          <div class="section-header">
            <h2>Actividad Reciente</h2>            <button @click="cargarTodosLosDatos" class="refresh-btn" :disabled="loading">
              <svg class="refresh-icon" :class="{ spinning: loading }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="23 4 23 10 17 10"></polyline>
                <polyline points="1 20 1 14 7 14"></polyline>
                <path d="m3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
              </svg>
              {{ loading ? 'Cargando...' : 'Actualizar' }}
            </button>
          </div>

          <!-- Pestañas -->
          <div class="tabs-container">
            <div class="tabs-header">
              <button 
                @click="activeTab = 'registros'" 
                :class="['tab-button', { active: activeTab === 'registros' }]"
              >
                <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 7v10M7 12h10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                Actividades Recientes
              </button>
              <button 
                @click="activeTab = 'entradas'" 
                :class="['tab-button', { active: activeTab === 'entradas' }]"
              >
                <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4M10 17l5-5-5-5M1 12h13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Entradas Recientes
              </button>
              <button 
                @click="activeTab = 'salidas'" 
                :class="['tab-button', { active: activeTab === 'salidas' }]"
              >
                <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l-5-5 5-5M21 12H8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Salidas Recientes
              </button>
            </div>
          </div>
          
          <div v-if="loading && registros.length === 0 && asistencias.length === 0" class="loading-container">
            <div class="spinner-large"></div>
            <p>Cargando datos...</p>
          </div>
          
          <div v-else-if="error" class="error-container">
            <p>{{ error }}</p>
            <button @click="cargarTodosLosDatos" class="retry-btn">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
                <path d="M3 3v5h5"></path>
                <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"></path>
                <path d="M21 21v-5h-5"></path>
              </svg>
              Reintentar
            </button>
          </div>

          <!-- Contenido de Pestaña: Actividades Recientes -->
          <div v-if="activeTab === 'registros'" class="tab-content">
            <div v-if="registros.length === 0" class="empty-state">
              <div class="empty-icon">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                </svg>
              </div>
              <h3>No hay actividades</h3>
              <p>Aún no se han creado actividades en la aplicación.</p>
            </div>
            
            <div v-else class="registros-table-container">
              <table class="registros-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Usuario</th>
                    <th>Foto</th>
                    <th>Ubicación</th>
                    <th>Descripción</th>
                    <th>Fecha</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>                  <tr v-for="registro in registros.slice(0, 10)" :key="registro.id">
                    <td>#{{ registro.id }}</td>
                    <td>
                      <div class="usuario-info">
                        <strong>{{ registro.usuario?.nombre_completo || `Usuario ${registro.usuario_id}` }}</strong>
                        <small>{{ registro.usuario?.correo || 'No disponible' }}</small>
                      </div>
                    </td>
                    <td>
                      <img 
                        v-if="registro.foto_url" 
                        :src="`${API_URL}/${registro.foto_url}`"
                        alt="Foto" 
                        class="foto-mini"
                        @click="abrirFotoCompleta(registro.foto_url)"
                      >
                      <span v-else class="no-foto">Sin foto</span>
                    </td>
                    <td class="ubicacion">
                      {{ parseFloat(registro.latitud).toFixed(6) }},<br>
                      {{ parseFloat(registro.longitud).toFixed(6) }}
                    </td>
                    <td class="descripcion">
                      {{ registro.descripcion || 'Sin descripción' }}
                    </td>
                    <td class="fecha">
                      {{ formatFecha(registro.fecha_hora) }}
                    </td>                    <td>
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
            </div>
          </div>

          <!-- Contenido de Pestaña: Entradas Recientes -->
          <div v-if="activeTab === 'entradas'" class="tab-content">
            <div v-if="entradasRecientes.length === 0" class="empty-state">
              <div class="empty-icon">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4M10 17l5-5-5-5M1 12h13"/>
                </svg>
              </div>
              <h3>No hay entradas recientes</h3>
              <p>Aún no se han registrado entradas en el sistema.</p>
            </div>
            
            <div v-else class="registros-table-container">
              <table class="registros-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Usuario</th>
                    <th>Fecha</th>
                    <th>Hora de Entrada</th>
                    <th>Hora de Salida</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="entrada in entradasRecientes.slice(0, 10)" :key="entrada.id">
                    <td>#{{ entrada.id }}</td>
                    <td>
                      <div class="usuario-info">
                        <strong>{{ entrada.usuario?.nombre_completo || `Usuario ${entrada.usuario_id}` }}</strong>
                        <small>{{ entrada.usuario?.correo || 'No disponible' }}</small>
                      </div>
                    </td>
                    <td class="fecha">{{ formatFechaElegante(entrada.fecha) }}</td>
                    <td class="hora-entrada">
                      <div class="badge-entrada">{{ formatHora12(entrada.hora_entrada) }}</div>
                    </td>
                    <td class="hora-salida">
                      <div v-if="entrada.hora_salida" class="badge-salida">{{ formatHora12(entrada.hora_salida) }}</div>
                      <div v-else class="badge-sin-salida">Sin registrar salida</div>
                    </td>
                    <td>
                      <span :class="['status-badge', entrada.hora_salida ? 'completed' : 'active']">
                        {{ entrada.hora_salida ? 'Completado' : 'Presente' }}
                      </span>
                    </td>
                    <td>
                      <div class="action-container">
                        <button @click="verDetallesAsistencia(entrada, 'entrada')" class="btn-ver" title="Ver detalles de entrada">
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
            </div>
          </div>

          <!-- Contenido de Pestaña: Salidas Recientes -->
          <div v-if="activeTab === 'salidas'" class="tab-content">
            <div v-if="salidasRecientes.length === 0" class="empty-state">
              <div class="empty-icon">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l-5-5 5-5M21 12H8"/>
                </svg>
              </div>
              <h3>No hay salidas recientes</h3>
              <p>Aún no se han registrado salidas en el sistema.</p>
            </div>
            
            <div v-else class="registros-table-container">
              <table class="registros-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Usuario</th>
                    <th>Fecha</th>
                    <th>Hora de Entrada</th>
                    <th>Hora de Salida</th>
                    <th>Tiempo Total</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="salida in salidasRecientes.slice(0, 10)" :key="salida.id">
                    <td>#{{ salida.id }}</td>
                    <td>
                      <div class="usuario-info">
                        <strong>{{ salida.usuario?.nombre_completo || `Usuario ${salida.usuario_id}` }}</strong>
                        <small>{{ salida.usuario?.correo || 'No disponible' }}</small>
                      </div>
                    </td>
                    <td class="fecha">{{ formatFechaElegante(salida.fecha) }}</td>
                    <td class="hora-entrada">
                      <div class="badge-entrada">{{ formatHora12(salida.hora_entrada) }}</div>
                    </td>
                    <td class="hora-salida">
                      <div class="badge-salida">{{ formatHora12(salida.hora_salida) }}</div>
                    </td>
                    <td class="tiempo-total">
                      <div class="badge-tiempo">{{ calcularTiempoTotal(salida.hora_entrada, salida.hora_salida) }}</div>
                    </td>
                    <td>
                      <div class="action-container">
                        <button @click="verDetallesAsistencia(salida, 'salida')" class="btn-ver" title="Ver detalles de salida">
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
                {{ modalType === 'asistencia' && selectedRecord?.tipoRegistro 
                   ? `Detalles de ${selectedRecord.tipoRegistro.charAt(0).toUpperCase() + selectedRecord.tipoRegistro.slice(1)}` 
                   : 'Detalles del Registro' }}
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
            <div v-if="modalType === 'details' && selectedRecord" class="registro-detalles">
              <div class="detail-grid">
                <div class="detail-item">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.94-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">ID del Registro</span>
                    <span class="detail-value highlight">#{{ selectedRecord.id }}</span>
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
                    <span class="detail-value">{{ selectedRecord.usuario?.nombre_completo || `Usuario ${selectedRecord.usuario_id}` }}</span>
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
                    <span class="detail-value">{{ selectedRecord.usuario?.correo || 'No disponible' }}</span>
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
                    <span class="detail-value">{{ formatFecha(selectedRecord.fecha_hora) }}</span>
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
                    <span class="detail-value location">{{ parseFloat(selectedRecord.latitud).toFixed(6) }}, {{ parseFloat(selectedRecord.longitud).toFixed(6) }}</span>
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
                    <span class="detail-value description">{{ selectedRecord.descripcion || 'Sin descripción' }}</span>
                  </div>
                </div>

                <div v-if="selectedRecord.foto_url" class="detail-item full-width">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path fill-rule="evenodd" d="M1.5 6a2.25 2.25 0 012.25-2.25h16.5A2.25 2.25 0 0122.5 6v12a2.25 2.25 0 01-2.25 2.25H3.75A2.25 2.25 0 011.5 18V6zM3 16.06V18c0 .414.336.75.75.75h16.5A.75.75 0 0021 18v-1.94l-2.69-2.689a1.5 1.5 0 00-2.12 0l-.88.879.97.97a.75.75 0 11-1.06 1.06l-5.16-5.159a1.5 1.5 0 00-2.12 0L3 16.061zm10.125-7.81a1.125 1.125 0 112.25 0 1.125 1.125 0 01-2.25 0z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                  <div class="detail-content">
                    <span class="detail-label">Fotografía</span>
                    <div class="photo-container">
                      <img 
                        :src="`${API_URL}/${selectedRecord.foto_url}`" 
                        alt="Foto del registro" 
                        class="detail-photo"
                        @click="abrirFotoCompleta(selectedRecord.foto_url)"
                      >
                    </div>
                  </div>
                </div>

                <div class="detail-item full-width">
                  <div class="detail-icon">
                    <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24">
                      <path fill-rule="evenodd" d="M11.54 22.351l.07.04.028.016a.76.76 0 00.723 0l.028-.015.071-.041a16.975 16.975 0 001.144-.742 19.58 19.58 0 002.683-2.282c1.944-1.99 3.963-4.98 3.963-8.827a8.25 8.25 0 00-16.5 0c0 3.846 2.02 6.837 3.963 8.827a19.58 19.58 0 002.682 2.282 16.975 16.975 0 001.145.742zM12 13.5a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/>
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

            <!-- Vista de detalles de asistencia -->
            <div v-else-if="modalType === 'asistencia' && selectedRecord" class="asistencia-detalles">
              <div class="modal-body-modern">
                <!-- Sección Principal del Usuario -->
                <div class="user-card-main">
                  <div class="user-avatar">
                    <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                    </svg>
                  </div>
                  <div class="user-info-main">
                    <h3>{{ selectedRecord.usuario?.nombre_completo || 'Usuario ' + selectedRecord.usuario_id }}</h3>
                    <p>ID: #{{ selectedRecord.usuario_id }}</p>
                    <span class="user-email">{{ selectedRecord.usuario?.correo || 'No disponible' }}</span>
                  </div>
                </div>

                <!-- Grid de Detalles -->
                <div class="details-grid-modern">
                  <!-- Hora Principal -->
                  <div class="detail-card time-card">
                    <div class="detail-icon-modern">
                      <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22C6.47,22 2,17.5 2,12A10,10 0 0,1 12,2M12.5,7V12.25L17,14.92L16.25,16.15L11,13V7H12.5Z"/>
                      </svg>
                    </div>
                    <div class="detail-content-modern">
                      <span class="detail-label-modern">
                        {{ selectedRecord.tipoRegistro === 'entrada' ? 'Hora de Entrada' : 'Hora de Salida' }}
                      </span>
                      <span class="detail-value-modern time-value-modern">
                        {{ formatHora12(selectedRecord.tipoRegistro === 'entrada' ? selectedRecord.hora_entrada : selectedRecord.hora_salida) }}
                      </span>
                    </div>
                  </div>

                  <!-- Fecha -->
                  <div class="detail-card date-card">
                    <div class="detail-icon-modern">
                      <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M9 11H7v6h2v-6zm4 0h-2v6h2v-6zm4-4v11c0 1.1-.9 2-2 2H7c-1.1 0-2-.9-2-2V7c0-1.1.9-2 2-2h1V3c0-.55.45-1 1-1s1 .45 1 1v2h6V3c0-.55.45-1 1-1s1 .45 1 1v2h1c1.1 0 2 .9 2 2z"/>
                      </svg>
                    </div>
                    <div class="detail-content-modern">
                      <span class="detail-label-modern">Fecha</span>
                      <span class="detail-value-modern">{{ formatFechaElegante(selectedRecord.fecha) }}</span>
                    </div>
                  </div>

                  <!-- Estado -->
                  <div class="detail-card status-card">
                    <div class="detail-icon-modern">
                      <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                      </svg>
                    </div>
                    <div class="detail-content-modern">
                      <span class="detail-label-modern">Estado</span>
                      <span :class="['detail-value-modern', 'status-badge-modern', selectedRecord.tipoRegistro]">
                        {{ selectedRecord.tipoRegistro === 'entrada' ? 'Entrada Registrada' : 'Salida Registrada' }}
                      </span>
                    </div>
                  </div>

                  <!-- Ubicación -->
                  <div class="detail-card location-card">
                    <div class="detail-icon-modern">
                      <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                        <path fill-rule="evenodd" d="M11.54 22.351l.07.04.028.016a.76.76 0 00.723 0l.028-.015.071-.041a16.975 16.975 0 001.144-.742 19.58 19.58 0 002.683-2.282c1.944-1.99 3.963-4.98 3.963-8.827a8.25 8.25 0 00-16.5 0c0 3.846 2.02 6.837 3.963 8.827a19.58 19.58 0 002.682 2.282 16.975 16.975 0 001.145.742zM12 13.5a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/>
                      </svg>
                    </div>
                    <div class="detail-content-modern">
                      <span class="detail-label-modern">
                        Ubicación de {{ selectedRecord.tipoRegistro === 'entrada' ? 'Entrada' : 'Salida' }}
                      </span>
                      <div class="location-info-modern">
                        <span class="coordinates-modern">
                          {{ parseFloat(selectedRecord.latitud || selectedRecord.latitud_entrada || selectedRecord.latitud_salida).toFixed(6) }}, 
                          {{ parseFloat(selectedRecord.longitud || selectedRecord.longitud_entrada || selectedRecord.longitud_salida).toFixed(6) }}
                        </span>
                        <div class="map-container-small" :id="`map-asistencia-${selectedRecord.id}`"></div>
                      </div>
                    </div>
                  </div>

                  <!-- Fotografía -->
                  <div class="detail-card photo-card">
                    <div class="photo-header-modern">
                      <div class="detail-icon-modern">
                        <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                          <path fill-rule="evenodd" d="M1.5 6a2.25 2.25 0 012.25-2.25h16.5A2.25 2.25 0 0122.5 6v12a2.25 2.25 0 01-2.25 2.25H3.75A2.25 2.25 0 011.5 18V6zM3 16.06V18c0 .414.336.75.75.75h16.5A.75.75 0 0021 18v-1.94l-2.69-2.689a1.5 1.5 0 00-2.12 0l-.88.879.97.97a.75.75 0 11-1.06 1.06l-5.16-5.159a1.5 1.5 0 00-2.12 0L3 16.061zm10.125-7.81a1.125 1.125 0 112.25 0 1.125 1.125 0 01-2.25 0z" clip-rule="evenodd"/>
                        </svg>
                      </div>
                      <span class="detail-label-modern">
                        Fotografía de {{ selectedRecord.tipoRegistro === 'entrada' ? 'Entrada' : 'Salida' }}
                      </span>
                    </div>
                    
                    <div class="photo-container-modern">
                      <!-- Foto de Entrada -->
                      <img 
                        v-if="selectedRecord.tipoRegistro === 'entrada' && selectedRecord.foto_entrada_url"
                        :src="`${API_URL}/${selectedRecord.foto_entrada_url}`" 
                        alt="Foto de entrada" 
                        class="detail-photo-modern"
                        @click="abrirFotoCompleta(selectedRecord.foto_entrada_url)"
                      >
                      <!-- Foto de Salida -->
                      <img 
                        v-else-if="selectedRecord.tipoRegistro === 'salida' && selectedRecord.foto_salida_url"
                        :src="`${API_URL}/${selectedRecord.foto_salida_url}`" 
                        alt="Foto de salida" 
                        class="detail-photo-modern"
                        @click="abrirFotoCompleta(selectedRecord.foto_salida_url)"
                      >
                      <!-- Foto única (compatibilidad) -->
                      <img 
                        v-else-if="selectedRecord.foto_url"
                        :src="`${API_URL}/${selectedRecord.foto_url}`" 
                        alt="Foto de registro" 
                        class="detail-photo-modern"
                        @click="abrirFotoCompleta(selectedRecord.foto_url)"
                      >
                      <!-- Sin foto -->
                      <div v-else class="no-photo-modern">
                        <svg width="32" height="32" fill="rgba(76, 175, 80, 0.3)" viewBox="0 0 24 24">
                          <path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/>
                        </svg>
                        <p>Sin fotografía</p>
                      </div>
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
import { ref, reactive, onMounted, onUnmounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Sidebar from '../components/Sidebar_NEW.vue'
import { usuariosService } from '../services/usuariosService.js'
import AsistenciasService from '../services/asistenciasService.js'
import { estadisticasService } from '../services/estadisticasService.js'

const router = useRouter()

const API_URL = 'https://apipwa.sembrandodatos.com'
const adminUser = ref(localStorage.getItem('admin_user') || 'Admin')
const isOnline = ref(navigator.onLine)

const registros = ref([])
const usuarios = ref([])
const asistencias = ref([])
const loading = ref(false)
const error = ref('')
const activeTab = ref('registros') // Nueva variable para las pestañas

const stats = reactive({
  totalRegistros: '-',
  totalUsuarios: '-',
  registrosHoy: '-',
  totalAsistencias: '-',
  asistenciasHoy: '-',
  usuariosPresentes: '-'
})

const showModal = ref(false)
const modalType = ref('details')
const selectedRecord = ref(null)
const showLightbox = ref(false)
const lightboxImageUrl = ref('')

// Variable para el mapa
let map = null

const statCards = computed(() => [
  // TARJETA DOCUMENTADA: Total Actividades - Comentado por solicitud del usuario
  // {
  //   label: 'Total Actividades',
  //   value: stats.totalRegistros,
  //   icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><defs><linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#66BB6A;stop-opacity:1" /><stop offset="100%" style="stop-color:#4CAF50;stop-opacity:0.8" /></linearGradient><filter id="glow1"><feGaussianBlur stdDeviation="2" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><circle cx="12" cy="12" r="10" fill="url(#grad1)" opacity="0.2"/><path d="M12 7v10M7 12h10" stroke="#4CAF50" stroke-width="2.5" stroke-linecap="round" filter="url(#glow1)"/></svg>`
  // },
  {
    label: 'Usuarios Activos',
    value: stats.totalUsuarios,
    icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><defs><linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#66BB6A;stop-opacity:1" /><stop offset="100%" style="stop-color:#4CAF50;stop-opacity:0.8" /></linearGradient><filter id="glow2"><feGaussianBlur stdDeviation="2" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><circle cx="12" cy="12" r="10" fill="url(#grad2)" opacity="0.2"/><path d="M16 7a4 4 0 1 1-8 0 4 4 0 0 1 8 0ZM12 14a7 7 0 0 0-7 7h14a7 7 0 0 0-7-7Z" fill="#4CAF50" filter="url(#glow2)"/></svg>`
  },
  {
    label: 'Actividades de Hoy',
    value: stats.registrosHoy,
    icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><defs><linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#66BB6A;stop-opacity:1" /><stop offset="100%" style="stop-color:#4CAF50;stop-opacity:0.8" /></linearGradient><filter id="glow3"><feGaussianBlur stdDeviation="2" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><circle cx="12" cy="12" r="10" fill="url(#grad3)" opacity="0.2"/><path d="M8 6h8v2H8zM6 10h12v8a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2z" fill="#4CAF50" filter="url(#glow3)"/><circle cx="9" cy="13" r="0.5" fill="#66BB6A"/><circle cx="12" cy="13" r="0.5" fill="#66BB6A"/><circle cx="15" cy="13" r="0.5" fill="#66BB6A"/></svg>`
  },
  // TARJETA DOCUMENTADA: Total Asistencias - Comentado por solicitud del usuario
  // {
  //   label: 'Total Asistencias',
  //   value: stats.totalAsistencias,
  //   icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><defs><linearGradient id="grad4" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#66BB6A;stop-opacity:1" /><stop offset="100%" style="stop-color:#4CAF50;stop-opacity:0.8" /></linearGradient><filter id="glow4"><feGaussianBlur stdDeviation="2" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><circle cx="12" cy="12" r="10" fill="url(#grad4)" opacity="0.2"/><path d="m9 12 2 2 4-4" stroke="#4CAF50" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow4)"/></svg>`
  // },
  {
    label: 'Asistencias Hoy',
    value: stats.asistenciasHoy,
    icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><defs><linearGradient id="grad5" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#66BB6A;stop-opacity:1" /><stop offset="100%" style="stop-color:#4CAF50;stop-opacity:0.8" /></linearGradient><filter id="glow5"><feGaussianBlur stdDeviation="2" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><circle cx="12" cy="12" r="10" fill="url(#grad5)" opacity="0.2"/><circle cx="12" cy="12" r="8" stroke="#4CAF50" stroke-width="2" fill="none" filter="url(#glow5)"/><path d="m12 6 v6 l4 2" stroke="#4CAF50" stroke-width="2.5" stroke-linecap="round" filter="url(#glow5)"/></svg>`
  },
  {
    label: 'Usuarios Presentes',
    value: stats.usuariosPresentes,
    icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><defs><linearGradient id="grad6" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#66BB6A;stop-opacity:1" /><stop offset="100%" style="stop-color:#4CAF50;stop-opacity:0.8" /></linearGradient><filter id="glow6"><feGaussianBlur stdDeviation="2" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><circle cx="12" cy="12" r="10" fill="url(#grad6)" opacity="0.2"/><circle cx="8" cy="8" r="2" fill="#4CAF50" filter="url(#glow6)"/><circle cx="16" cy="8" r="2" fill="#4CAF50" filter="url(#glow6)"/><path d="M4 18v-1a4 4 0 0 1 4-4h0a4 4 0 0 1 4 4v1M16 13a4 4 0 0 1 4 4v1" stroke="#4CAF50" stroke-width="2" stroke-linecap="round" filter="url(#glow6)"/></svg>`
  }
])

// Computed properties para las diferentes pestañas
const entradasRecientes = computed(() => {
  // Mostrar todas las asistencias que tienen hora de entrada (con o sin salida)
  console.log('Calculando entradas recientes:', asistencias.value)
  const resultado = asistencias.value
    .filter(asistencia => asistencia.hora_entrada) // Solo las que tienen entrada registrada
    .sort((a, b) => {
      // Ordenar por fecha y hora más recientes
      const fechaA = new Date(`${a.fecha} ${a.hora_entrada}`)
      const fechaB = new Date(`${b.fecha} ${b.hora_entrada}`)
      return fechaB - fechaA
    })
    .map(asistencia => {
      // Enriquecer con información del usuario
      const usuario = usuarios.value.find(u => u.id === asistencia.usuario_id)
      console.log('Entrada:', {
        hora_entrada: asistencia.hora_entrada,
        hora_salida: asistencia.hora_salida || 'Sin registrar',
        usuario: usuario?.nombre_completo
      })
      return { ...asistencia, usuario }
    })
  
  console.log('Entradas recientes resultado:', resultado.slice(0, 3))
  return resultado
})

const salidasRecientes = computed(() => {
  // Filtrar asistencias que tienen hora de salida y ordenar por fecha más reciente
  console.log('Calculando salidas recientes:', asistencias.value)
  const resultado = asistencias.value
    .filter(asistencia => asistencia.hora_salida)
    .sort((a, b) => {
      // Ordenar por fecha y hora de salida más recientes
      const fechaA = new Date(`${a.fecha} ${a.hora_salida}`)
      const fechaB = new Date(`${b.fecha} ${b.hora_salida}`)
      return fechaB - fechaA
    })
    .map(asistencia => {
      // Enriquecer con información del usuario
      const usuario = usuarios.value.find(u => u.id === asistencia.usuario_id)
      console.log('Salida con horas:', { 
        entrada: asistencia.hora_entrada, 
        salida: asistencia.hora_salida, 
        usuario: usuario?.nombre_completo 
      })
      return { ...asistencia, usuario }
    })
  
  console.log('Salidas recientes resultado:', resultado.slice(0, 3))
  return resultado
})

// Detectar cambios de conexión
window.addEventListener('online', () => { isOnline.value = true })
window.addEventListener('offline', () => { isOnline.value = false })

onMounted(() => {
  cargarTodosLosDatos()
  
  // Agregar event listener para cerrar lightbox con ESC
  window.addEventListener('keydown', handleKeyDown)
  
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

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
})

const cargarRegistros = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const token = localStorage.getItem('admin_token')
    // Para el dashboard, cargar más registros para tener mejor información estadística
    const response = await axios.get(`${API_URL}/registros?limit=1000`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    // La respuesta puede ser directamente un array o tener una propiedad específica
    const registrosRaw = Array.isArray(response.data) ? response.data : (response.data.registros || [])
      // Enriquecer registros con información de usuarios reales
    registros.value = await usuariosService.enriquecerRegistrosConUsuarios(registrosRaw)
    
    // También cargar asistencias cuando se actualicen los registros
    await cargarAsistencias()
    
    await calcularEstadisticas()
    
    console.log('Registros cargados en Dashboard:', registros.value)
  } catch (err) {
    console.error('Error al cargar registros:', err)
    if (err.response?.status === 401) {
      // Token expirado
      logout()
    } else {
      error.value = 'Error al cargar los registros: ' + (err.response?.data?.detail || err.message)
    }
  } finally {
    loading.value = false
  }
}

const cargarUsuarios = async () => {
  try {
    usuarios.value = await usuariosService.obtenerUsuarios()
    await calcularEstadisticas() // Recalcular con usuarios reales
    console.log('✅ Usuarios reales cargados en Dashboard:', usuarios.value)
  } catch (err) {
    console.error('❌ Error al cargar usuarios desde la base de datos:', err)
    // Si no se pueden cargar usuarios, usar los únicos de registros
    if (registros.value.length > 0) {
      const usuariosUnicos = [...new Set(registros.value.map(r => r.usuario_id))]
      stats.totalUsuarios = usuariosUnicos.length
    }
  }
}

const cargarAsistencias = async () => {
  try {
    asistencias.value = await AsistenciasService.obtenerAsistencias()
    await calcularEstadisticas() // Recalcular con asistencias
    console.log('✅ Asistencias cargadas en Dashboard:', asistencias.value)
  } catch (err) {
    console.error('❌ Error al cargar asistencias:', err)
  }
}

const calcularEstadisticas = async () => {
  try {
    // Usar el nuevo servicio de estadísticas con fallback automático
    const estadisticasReales = await estadisticasService.obtenerEstadisticasConFallback(
      registros.value,
      usuarios.value,
      asistencias.value
    )
    
    // Aplicar las estadísticas obtenidas
    stats.totalRegistros = estadisticasReales.totalRegistros
    stats.totalUsuarios = estadisticasReales.totalUsuarios
    stats.registrosHoy = estadisticasReales.registrosHoy
    stats.totalAsistencias = estadisticasReales.totalAsistencias
    stats.asistenciasHoy = estadisticasReales.asistenciasHoy
    stats.usuariosPresentes = estadisticasReales.usuariosPresentes
    
    console.log('✅ Estadísticas aplicadas:', estadisticasReales)
    
  } catch (error) {
    console.error('❌ Error fatal obteniendo estadísticas:', error)
    
    // Si hay error del token, hacer logout
    if (error.message === 'TOKEN_EXPIRED') {
      logout()
      return
    }
    
    // Como último recurso, usar valores por defecto
    stats.totalRegistros = '-'
    stats.totalUsuarios = '-'
    stats.registrosHoy = '-'
    stats.totalAsistencias = '-'
    stats.asistenciasHoy = '-'
    stats.usuariosPresentes = '-'
  }
}

const formatFecha = (fechaStr) => {
  try {
    // Si viene una fecha ISO completa (con T), la procesamos
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
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    // Para otros casos, usar el método estándar
    return new Date(fechaStr).toLocaleString('es-ES')
  } catch (e) {
    console.error('Error al formatear fecha:', e, 'Fecha original:', fechaStr)
    return fechaStr
  }
}

// Nueva función para formato de fecha simple
const formatFechaSimple = (fechaStr) => {
  try {
    // Si la fecha viene en formato 'YYYY-MM-DD', crear la fecha directamente sin zona horaria
    if (typeof fechaStr === 'string' && fechaStr.match(/^\d{4}-\d{2}-\d{2}$/)) {
      const [year, month, day] = fechaStr.split('-').map(num => parseInt(num, 10))
      const fecha = new Date(year, month - 1, day) // month - 1 porque los meses en JS van de 0-11
      
      return fecha.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
    }
    
    // Para otros formatos, usar el método tradicional
    const fecha = new Date(fechaStr)
    return fecha.toLocaleDateString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
  } catch (e) {
    console.error('Error al formatear fecha simple:', e, 'Fecha original:', fechaStr)
    return fechaStr
  }
}

// Nueva función para formato de fecha más elegante
const formatFechaElegante = (fechaStr) => {
  try {
    // Si la fecha viene en formato 'YYYY-MM-DD', crear la fecha directamente sin zona horaria
    if (typeof fechaStr === 'string' && fechaStr.match(/^\d{4}-\d{2}-\d{2}$/)) {
      const [year, month, day] = fechaStr.split('-').map(num => parseInt(num, 10))
      const fecha = new Date(year, month - 1, day) // month - 1 porque los meses en JS van de 0-11
      
      return fecha.toLocaleDateString('es-ES', {
        weekday: 'short',
        day: '2-digit',
        month: 'short',
        year: 'numeric'
      })
    }
    
    // Para otros formatos, usar el método tradicional
    const fecha = new Date(fechaStr)
    return fecha.toLocaleDateString('es-ES', {
      weekday: 'short',
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    })
  } catch (e) {
    console.error('Error al formatear fecha elegante:', e, 'Fecha original:', fechaStr)
    return fechaStr
  }
}

// Nueva función para formatear hora en formato 12 horas con AM/PM
const formatHora12 = (horaStr) => {
  if (!horaStr) return '-'
  
  try {
    console.log('Hora recibida:', horaStr)
    
    // Limpiar la hora y convertir a string
    let horaLimpia = String(horaStr).trim()
    
    // Si la hora tiene más de 5 caracteres, podría estar malformada
    // Buscar el patrón HH:MM
    const match = horaLimpia.match(/(\d{1,2}):(\d{2})/)
    if (!match) {
      console.log('No se pudo hacer match con el patrón de hora')
      return horaStr
    }
    
    const horas = parseInt(match[1], 10)
    const minutos = parseInt(match[2], 10)
    
    console.log('Horas y minutos parseados:', { horas, minutos })
    
    // Verificar que sean números válidos
    if (isNaN(horas) || isNaN(minutos) || horas < 0 || horas > 23 || minutos < 0 || minutos > 59) {
      console.log('Horas o minutos inválidos')
      return horaStr
    }
    
    // Convertir a formato 12 horas
    let hora12 = horas
    let periodo = 'AM'
    
    if (horas === 0) {
      hora12 = 12
      periodo = 'AM'
    } else if (horas === 12) {
      hora12 = 12
      periodo = 'PM'
    } else if (horas > 12) {
      hora12 = horas - 12
      periodo = 'PM'
    }
    
    // Formatear con ceros a la izquierda para minutos
    const minutosFormateados = minutos.toString().padStart(2, '0')
    
    const resultado = `${hora12}:${minutosFormateados} ${periodo}`
    console.log('Resultado formateado:', resultado)
    
    return resultado
  } catch (e) {
    console.error('Error al formatear hora:', e, 'Hora original:', horaStr)
    return horaStr
  }
}

// Nueva función para calcular tiempo total
const calcularTiempoTotal = (horaEntrada, horaSalida) => {
  if (!horaEntrada || !horaSalida) {
    console.log('Faltan datos de entrada o salida:', { horaEntrada, horaSalida })
    return '-'
  }
  
  try {
    // Limpiar y normalizar las horas (quitar espacios, convertir a string)
    const entradaStr = String(horaEntrada).trim()
    const salidaStr = String(horaSalida).trim()
    
    console.log('Calculando tiempo:', { entradaStr, salidaStr })
    
    // Separar horas y minutos
    const [hEntrada, mEntrada] = entradaStr.split(':').map(num => {
      const parsed = parseInt(num, 10)
      return isNaN(parsed) ? 0 : parsed
    })
    
    const [hSalida, mSalida] = salidaStr.split(':').map(num => {
      const parsed = parseInt(num, 10)
      return isNaN(parsed) ? 0 : parsed
    })
    
    console.log('Horas parseadas:', { hEntrada, mEntrada, hSalida, mSalida })
    
    // Verificar que las horas sean válidas
    if (isNaN(hEntrada) || isNaN(mEntrada) || isNaN(hSalida) || isNaN(mSalida)) {
      console.log('Error: Algún valor no es un número válido')
      return '-'
    }
    
    // Convertir todo a minutos
    const entradaMinutos = hEntrada * 60 + mEntrada
    const salidaMinutos = hSalida * 60 + mSalida
    
    // Calcular diferencia
    let diferencia = salidaMinutos - entradaMinutos
    
    // Si la diferencia es negativa, podría ser que cruzó medianoche
    if (diferencia < 0) {
      diferencia += 24 * 60 // Agregar 24 horas en minutos
    }
    
    // Convertir de vuelta a horas y minutos
    const horas = Math.floor(diferencia / 60)
    const minutos = diferencia % 60
    
    const resultado = `${horas}h ${minutos.toString().padStart(2, '0')}m`
    console.log('Resultado calculado:', resultado)
    
    return resultado
  } catch (e) {
    console.error('Error al calcular tiempo total:', e, { horaEntrada, horaSalida })
    return '-'
  }
}

// Nueva función para cargar todos los datos
const cargarTodosLosDatos = async () => {
  await Promise.all([
    cargarRegistros(),
    cargarUsuarios(),
    cargarAsistencias()
  ])
}

// Nueva función para ver detalles de asistencia
const verDetallesAsistencia = async (asistencia, tipo = null) => {
  selectedRecord.value = asistencia
  
  // Determinar el tipo de registro basado en qué tab está activo o parámetro directo
  let tipoRegistro = tipo
  if (!tipoRegistro) {
    if (activeTab.value === 'entradas') {
      tipoRegistro = 'entrada'
    } else if (activeTab.value === 'salidas') {
      tipoRegistro = 'salida'
    } else {
      // Si no hay tab activo, determinar por la presencia de datos
      tipoRegistro = asistencia.hora_salida ? 'salida' : 'entrada'
    }
  }
  
  selectedRecord.value.tipoRegistro = tipoRegistro
  modalType.value = 'asistencia'
  showModal.value = true

  // Esperar a que el modal se renderice
  await nextTick()
  
  // Inicializar el mapa pequeño después de un breve delay
  setTimeout(() => {
    initMapAsistencia(asistencia)
  }, 150)
}

const verDetalles = async (registro) => {
  selectedRecord.value = registro
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
      .bindPopup(`Registro #${selectedRecord.value?.id}<br>Lat: ${lat}<br>Lng: ${lng}`)
      .openPopup()
  } catch (error) {
    console.error('Error al inicializar el mapa:', error)
  }
}

// Variable para el mapa de asistencia
let mapAsistencia = null

const initMapAsistencia = (asistencia) => {
  // Limpiar mapa anterior si existe
  if (mapAsistencia) {
    mapAsistencia.remove()
    mapAsistencia = null
  }
  
  const mapElementId = `map-asistencia-${asistencia.id}`
  const mapElement = document.getElementById(mapElementId)
  if (!mapElement) {
    console.warn('Elemento del mapa de asistencia no encontrado:', mapElementId)
    return
  }
  
  // Verificar que Leaflet esté cargado
  if (!window.L) {
    console.error('Leaflet no está cargado')
    return
  }
  
  // Obtener coordenadas según el tipo de registro
  let lat, lng
  if (asistencia.tipoRegistro === 'entrada') {
    lat = asistencia.latitud_entrada || asistencia.latitud
    lng = asistencia.longitud_entrada || asistencia.longitud
  } else {
    lat = asistencia.latitud_salida || asistencia.latitud
    lng = asistencia.longitud_salida || asistencia.longitud
  }
  
  if (!lat || !lng) {
    console.warn('Coordenadas no disponibles para el mapa de asistencia')
    mapElement.innerHTML = '<div class="no-location-modern">📍 Ubicación no disponible</div>'
    return
  }
  
  try {
    mapAsistencia = window.L.map(mapElementId, {
      zoomControl: false,
      attributionControl: false,
      dragging: false,
      touchZoom: false,
      doubleClickZoom: false,
      scrollWheelZoom: false,
      boxZoom: false,
      keyboard: false
    }).setView([parseFloat(lat), parseFloat(lng)], 16)
    
    window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: false
    }).addTo(mapAsistencia)
    
    // Agregar marcador con diferente color según el tipo
    const iconColor = asistencia.tipoRegistro === 'entrada' ? '#4CAF50' : '#FF9800'
    const popupText = `${asistencia.tipoRegistro === 'entrada' ? 'Entrada' : 'Salida'} registrada<br>
                      Usuario: ${asistencia.usuario?.nombre_completo || 'Usuario ' + asistencia.usuario_id}<br>
                      Lat: ${parseFloat(lat).toFixed(6)}<br>
                      Lng: ${parseFloat(lng).toFixed(6)}`
    
    window.L.marker([parseFloat(lat), parseFloat(lng)])
      .addTo(mapAsistencia)
      .bindPopup(popupText)
  } catch (error) {
    console.error('Error al inicializar el mapa de asistencia:', error)
    mapElement.innerHTML = '<div class="map-error-modern">❌ Error al cargar el mapa</div>'
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
  if (mapAsistencia) {
    mapAsistencia.remove()
    mapAsistencia = null
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
.dashboard-container {
  display: flex;
  min-height: 100vh;
  position: relative;
}

.main-content {
  flex: 1;
  margin-left: min(220px, 18vw);
  background: linear-gradient(135deg, #f8f9fa 0%, #f0fff0 100%);
  min-height: 100vh;
  position: relative;
  width: calc(100vw - min(220px, 18vw));
  max-width: calc(100vw - min(220px, 18vw));
  padding: 0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow-x: hidden;
}

.dashboard-header {
  background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
  border-bottom: none;
  padding: clamp(0.75rem, 2vw, 1.25rem);
  color: white;
  box-shadow: 0 4px 20px rgba(46, 204, 113, 0.15);
  position: relative;
  overflow: hidden;
  width: 100%;
  box-sizing: border-box;
}

.dashboard-header::before {
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
  position: relative;
  z-index: 2;
  flex-wrap: wrap;
  gap: clamp(8px, 2vw, 16px);
  width: 100%;
  max-width: 100%;
}

.header-main {
  display: flex;
  align-items: center;
  gap: clamp(12px, 2vw, 20px);
  flex: 1;
  min-width: 0;
}

.header-icon {
  width: clamp(36px, 5vw, 48px);
  height: clamp(36px, 5vw, 48px);
  background: rgba(255, 255, 255, 0.15);
  border-radius: clamp(8px, 1.5vw, 12px);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: float 3s ease-in-out infinite;
  flex-shrink: 0;
}

.header-icon svg {
  width: clamp(16px, 3vw, 24px);
  height: clamp(16px, 3vw, 24px);
  color: white;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
}

.header-text {
  flex: 1;
}

.header-title {
  font-size: clamp(1.1rem, 3vw, 1.5rem);
  font-weight: 700;
  margin: 0;
  background: linear-gradient(45deg, #ffffff 0%, #e8f5e8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  letter-spacing: -0.5px;
  line-height: 1.2;
}

.header-subtitle {
  margin: clamp(0.15rem, 0.5vw, 0.25rem) 0 0 0;
  color: rgba(255, 255, 255, 0.9);
  font-size: clamp(0.7rem, 1.5vw, 0.85rem);
  line-height: 1.3;
  font-weight: 400;
  letter-spacing: 0.2px;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.connection-status.online {
  background: rgba(39, 174, 96, 0.2);
  border-color: rgba(39, 174, 96, 0.3);
}

.connection-status.offline {
  background: rgba(231, 76, 60, 0.2);
  border-color: rgba(231, 76, 60, 0.3);
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.connection-status.online .status-indicator {
  background: #27ae60;
  box-shadow: 0 0 8px rgba(39, 174, 96, 0.6);
}

.connection-status.offline .status-indicator {
  background: #e74c3c;
  box-shadow: 0 0 8px rgba(231, 76, 60, 0.6);
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.7; }
  100% { transform: scale(1); opacity: 1; }
}

.status-text {
  color: white;
  font-weight: 500;
}

/* Contenido del dashboard */
.dashboard-content {
  padding: 32px 40px;
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

.refresh-btn:hover::before {
  left: 100%;
}

.refresh-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #45a049 0%, #5cb85c 50%, #45a049 100%);
  transform: translateY(-3px) scale(1.08);
  box-shadow: 
    0 12px 32px rgba(76, 175, 80, 0.5),
    0 4px 16px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
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

.dashboard-content {
  padding: clamp(16px, 4vw, 32px) clamp(12px, 3vw, 32px);
  width: 100%;
  box-sizing: border-box;
  max-width: 100%;
  overflow-x: hidden;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(clamp(140px, 20vw, 180px), 1fr));
  gap: clamp(8px, 2vw, 14px);
  margin-bottom: clamp(10px, 2.5vw, 20px);
  width: 100%;
}

.stat-card {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.12) 0%, rgba(76, 175, 80, 0.08) 100%);
  padding: clamp(10px, 2vw, 16px);
  border-radius: clamp(18px, 3vw, 24px);
  box-shadow: 
    0 4px 20px rgba(76, 175, 80, 0.15), 
    0 2px 10px rgba(0,0,0,0.05),
    inset 0 1px 0 rgba(255,255,255,0.6);
  display: flex;
  align-items: center;
  gap: clamp(8px, 2vw, 14px);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  animation: fadeInUp 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  backdrop-filter: blur(12px);
  width: 100%;
  box-sizing: border-box;
  min-height: clamp(55px, 8vh, 75px);
}

.stat-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(128, 0, 32, 0.6), rgba(76, 175, 80, 0.8));
  border-radius: clamp(18px, 3vw, 24px);
  padding: 2px;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: xor;
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  pointer-events: none;
  z-index: 1;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(128, 0, 32, 0.15), rgba(76, 175, 80, 0.2), transparent);
  border-radius: clamp(18px, 3vw, 24px);
  transition: left 0.6s ease;
  z-index: 0;
}

.stat-card:hover::before {
  left: 100%;
}

.stat-card:hover {
  transform: translateY(-8px) scale(1.03);
  box-shadow: 
    0 16px 36px rgba(76, 175, 80, 0.25), 
    0 6px 18px rgba(128, 0, 32, 0.12),
    inset 0 1px 0 rgba(255,255,255,0.7);
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.18) 0%, rgba(76, 175, 80, 0.12) 100%);
}

.stat-card:hover::after {
  background: linear-gradient(135deg, rgba(128, 0, 32, 0.8), rgba(76, 175, 80, 1));
}

.animated-card {
  opacity: 0;
  animation: fadeInUp 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}

.animated-card:nth-child(1) { animation-delay: 0.1s; }
.animated-card:nth-child(2) { animation-delay: 0.2s; }
.animated-card:nth-child(3) { animation-delay: 0.3s; }

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

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes slideInRight {
  0% { transform: translateX(30px); opacity: 0; }
  100% { transform: translateX(0); opacity: 1; }
}

.svg-icon {
  width: clamp(32px, 6vw, 40px);
  height: clamp(32px, 6vw, 40px);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border-radius: clamp(8px, 1.5vw, 12px);
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.08) 0%, rgba(76, 175, 80, 0.04) 100%);
  position: relative;
  flex-shrink: 0;
  z-index: 2;
}

.svg-icon::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: radial-gradient(circle, rgba(76, 175, 80, 0.2) 0%, transparent 70%);
  border-radius: 50%;
  transition: all 0.4s ease;
  transform: translate(-50%, -50%);
}

.stat-card:hover .svg-icon {
  transform: scale(1.15) rotate(-5deg);
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(76, 175, 80, 0.08) 100%);
}

.stat-card:hover .svg-icon::before {
  width: clamp(50px, 10vw, 60px);
  height: clamp(50px, 10vw, 60px);
}

.stat-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  z-index: 2;
}

.stat-info h3 {
  font-size: clamp(20px, 4vw, 28px);
  color: #4CAF50;
  margin-bottom: clamp(2px, 0.8vw, 4px);
  font-weight: 800;
  letter-spacing: clamp(0.6px, 0.12vw, 1px);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
}

.stat-card:hover .stat-info h3 {
  transform: scale(1.08);
  background: linear-gradient(135deg, #388e3c 0%, #4CAF50 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: pulse 2s ease-in-out infinite;
}

.stat-info p {
  color: #666;
  font-size: clamp(9px, 1.8vw, 12px);
  font-weight: 600;
  margin: 0;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: clamp(0.2px, 0.06vw, 0.4px);
  line-height: 1.3;
}

.stat-card:hover .stat-info p {
  color: #4CAF50;
  transform: translateX(2px);
}

.section {
  background: linear-gradient(135deg, #ffffff 0%, #fafffe 100%);
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.08),
    0 2px 16px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255,255,255,0.8);
  overflow: hidden;
  border: 1px solid rgba(76, 175, 80, 0.1);
  transition: all 0.3s ease;
  animation: slideInRight 0.6s ease-out;
}

.section:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 12px 40px rgba(0, 0, 0, 0.12),
    0 4px 20px rgba(0, 0, 0, 0.06),
    inset 0 1px 0 rgba(255,255,255,0.9);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px;
  border-bottom: 1px solid #e0e0e0;
}

.section-header h2 {
  color: #333;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 50%, #4CAF50 100%);
  color: white;
  border: none;
  padding: 14px 24px;
  border-radius: 50px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 700;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 
    0 6px 20px rgba(76, 175, 80, 0.35),
    0 2px 8px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  min-width: 140px;
  justify-content: center;
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

.loading-container, .empty-state {
  text-align: center;
  padding: 80px 32px;
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

.error-container {
  text-align: center;
  padding: 32px;
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

.registros-table-container {
  overflow-x: auto;
  animation: fadeInUp 0.6s ease-out 0.2s both;
}

.registros-table {
  width: 100%;
  border-collapse: collapse;
  position: relative;
}

.registros-table th,
.registros-table td {
  padding: 16px 12px;
  text-align: center;
  vertical-align: middle;
  border-bottom: 1px solid rgba(224, 224, 224, 0.6);
  transition: all 0.3s ease;
}

.registros-table th {
  background: linear-gradient(135deg, #f8f9fa 0%, #f0f8f0 100%);
  font-weight: 700;
  color: #4CAF50;
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.5px;
  position: sticky;
  top: 0;
  z-index: 10;
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
  width: 48px;
  height: 48px;
  object-fit: cover;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 2px solid rgba(76, 175, 80, 0.2);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: block;
  margin: 0 auto;
}

.foto-mini:hover {
  transform: scale(1.1) rotate(2deg);
  border-color: #4CAF50;
  box-shadow: 0 8px 24px rgba(76, 175, 80, 0.3);
}

.no-foto {
  color: #999;
  font-size: 12px;
  text-align: center;
  display: block;
}

.ubicacion, .fecha {
  font-size: 12px;
  color: #666;
}

.usuario-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.usuario-info strong {
  font-size: 14px;
  color: #2c3e50;
}

.usuario-info small {
  font-size: 12px;
  color: #666;
  font-style: italic;
}

.descripcion {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.btn-ver {
  width: clamp(32px, 6vw, 36px);
  height: clamp(32px, 6vw, 36px);
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

/* Estilos del modal mejorados */
.modal-overlay {
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
  z-index: 1000;
  padding: 20px;
  animation: modalFadeIn 0.3s ease-out;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    backdrop-filter: blur(0px);
  }
  to {
    opacity: 1;
    backdrop-filter: blur(4px);
  }
}

.modal-content {
  background: white;
  border-radius: 16px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
  max-width: 850px;
  width: 95vw;
  max-height: 90vh;
  height: 80vh;
  overflow: hidden;
  position: relative;
  animation: modalSlideIn 0.3s ease-out;
  display: flex;
  flex-direction: column;
}

/* Modal optimizado para asistencia */
.modal-content:has(.asistencia-detalles) {
  max-width: 900px;
  width: 95vw;
  max-height: 85vh;
  aspect-ratio: unset;
}

@keyframes modalSlideIn {
  from {
    transform: translateY(30px) scale(0.95);
    opacity: 0;
  }
  to {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}

.modal-header {
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
  color: white;
  padding: 20px 24px;
  border-radius: 16px 16px 0 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

.modal-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='20' cy='20' r='1.5'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
  z-index: 1;
}

.modal-header-content {
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
  z-index: 2;
}

.modal-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.modal-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: white;
}

.btn-close {
  background: rgba(255, 255, 255, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 10px;
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 2;
}

.btn-close:hover {
  background: rgba(255, 255, 255, 0.35);
  transform: scale(1.1);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.modal-body {
  padding: 16px;
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
}

.modal-body::-webkit-scrollbar {
  width: 6px;
}

.modal-body::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.modal-body::-webkit-scrollbar-thumb {
  background: #4CAF50;
  border-radius: 3px;
}

.modal-body::-webkit-scrollbar-thumb:hover {
  background: #45a049;
}

/* Estilos para detalles del registro */
.registro-detalles {
  animation: contentFadeIn 0.4s ease-out 0.1s both;
}

@keyframes contentFadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #f8fffe 0%, #f0fff4 100%);
  border: 1px solid rgba(76, 175, 80, 0.1);
  border-radius: 10px;
  transition: all 0.2s ease;
}

.detail-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.08);
  border-color: rgba(76, 175, 80, 0.2);
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.detail-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  font-size: 12px;
  font-weight: 600;
  color: #4CAF50;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.detail-value {
  font-size: 14px;
  color: #2c3e50;
  line-height: 1.3;
  font-weight: 500;
}

.detail-value.highlight {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
  font-size: 16px;
}

.detail-value.location {
  font-family: 'Courier New', monospace;
  background: #f0f0f0;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
}

.detail-value.description {
  background: #f8f9fa;
  padding: 8px;
  border-radius: 6px;
  border-left: 3px solid #4CAF50;
  font-style: italic;
  font-size: 13px;
}

/* Estilos para fotografías */
.photo-container {
  position: relative;
  display: inline-block;
  border-radius: 12px;
  overflow: hidden;
  margin-top: 8px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.photo-container:hover {
  transform: scale(1.02);
}

.detail-photo {
  width: 100%;
  max-width: 250px;
  height: auto;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.detail-photo:hover {
  box-shadow: 0 8px 25px rgba(76, 175, 80, 0.2);
}

/* Estilos para el mapa */
.map-container {
  margin-top: 8px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.leaflet-map {
  height: 200px;
  width: 100%;
}

/* Footer del modal */
.modal-footer {
  padding: 0;
  background: transparent;
  border: none;
  height: 0;
}

/* Estilos modernos para el modal de asistencia */
.asistencia-detalles {
  width: 100%;
  height: 100%;
}

.modal-body-modern {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 0;
  height: 100%;
}

/* Tarjeta principal del usuario */
.user-card-main {
  display: flex;
  align-items: center;
  gap: 16px;
  background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
  color: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(76, 175, 80, 0.3);
  /* Remover todas las animaciones y transiciones */
  animation: none !important;
  transition: none !important;
  transform: none !important;
}

.user-avatar {
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  /* Sin animaciones */
  animation: none !important;
  transition: none !important;
  transform: none !important;
}

.user-avatar svg {
  width: 24px;
  height: 24px;
  color: white;
}

.user-info-main h3 {
  margin: 0 0 4px 0;
  font-size: 18px;
  font-weight: 600;
  color: white;
  /* Sin animaciones */
  animation: none !important;
  transition: none !important;
  transform: none !important;
}

.user-info-main p {
  margin: 0 0 4px 0;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
  /* Sin animaciones */
  animation: none !important;
  transition: none !important;
  transform: none !important;
}

.user-email {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  background: rgba(255, 255, 255, 0.1);
  padding: 4px 8px;
  border-radius: 6px;
  display: inline-block;
  /* Sin animaciones */
  animation: none !important;
  transition: none !important;
  transform: none !important;
}

/* Grid moderno de detalles */
.details-grid-modern {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
  flex: 1;
}

/* Tarjetas de detalle modernas */
.detail-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
  border: 2px solid rgba(76, 175, 80, 0.1);
  border-radius: 12px;
  padding: 16px;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  min-height: 120px;
}

.detail-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(76, 175, 80, 0.15);
  border-color: rgba(76, 175, 80, 0.3);
}

.detail-icon-modern {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}

.detail-icon-modern svg {
  width: 20px;
  height: 20px;
  color: white;
}

.detail-content-modern {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label-modern {
  font-size: 12px;
  font-weight: 600;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.detail-value-modern {
  font-size: 16px;
  font-weight: 600;
  color: #2E7D32;
  line-height: 1.3;
}

/* Valores especiales */
.time-value-modern {
  font-size: 20px;
  font-weight: 700;
  color: #1B5E20;
  text-shadow: 0 1px 2px rgba(76, 175, 80, 0.1);
}

.status-badge-modern {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.status-badge-modern.entrada {
  background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%);
  color: #1B5E20;
  border: 1px solid rgba(76, 175, 80, 0.3);
}

.status-badge-modern.salida {
  background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
  color: #E65100;
  border: 1px solid rgba(255, 152, 0, 0.3);
}

/* Tarjeta de ubicación */
.location-card {
  grid-column: span 2;
  min-height: 180px;
}

.location-info-modern {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.coordinates-modern {
  font-size: 14px;
  color: #666;
  background: rgba(76, 175, 80, 0.1);
  padding: 6px 10px;
  border-radius: 6px;
  font-family: 'Courier New', monospace;
  border: 1px solid rgba(76, 175, 80, 0.2);
}

.map-container-small {
  width: 100%;
  height: 120px;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid rgba(76, 175, 80, 0.2);
  background: #f8f9fa;
  position: relative;
}

.no-location-modern,
.map-error-modern {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
  font-size: 14px;
  text-align: center;
}

.map-error-modern {
  color: #e74c3c;
}

/* Tarjeta de foto especial */
.photo-card {
  grid-column: span 2;
  min-height: 200px;
}

.photo-header-modern {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.photo-container-modern {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8f9fa 0%, #f0fff0 100%);
  border-radius: 8px;
  padding: 16px;
  min-height: 140px;
}

.detail-photo-modern {
  max-width: 100%;
  max-height: 200px;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease;
}

.detail-photo-modern:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.no-photo-modern {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #999;
  min-height: 120px;
}

.no-photo-modern svg {
  opacity: 0.5;
}

.no-photo-modern p {
  margin: 0;
  font-size: 14px;
  color: #999;
}

/* Responsive para móviles */
@media (max-width: 768px) {
  .details-grid-modern {
    grid-template-columns: 1fr;
  }
  
  .photo-card,
  .location-card {
    grid-column: span 1;
  }
  
  .user-card-main {
    padding: 16px;
  }
  
  .user-info-main h3 {
    font-size: 16px;
  }
  
  .detail-card {
    padding: 12px;
    min-height: 100px;
  }
  
  .detail-icon-modern {
    width: 36px;
    height: 36px;
  }
  
  .time-value-modern {
    font-size: 18px;
  }
}

@media (max-width: 480px) {
  .modal-body-modern {
    gap: 16px;
  }
  
  .user-card-main {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
  
  .detail-card {
    padding: 12px;
  }
  
  .photo-container-modern {
    min-height: 100px;
  }
  
  .map-container-small {
    height: 100px;
  }
}

.time-worked {
  color: #1B5E20 !important;
  font-weight: 700;
  font-size: 16px;
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.photo-container-large {
  width: 100%;
  height: 140px;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid rgba(76, 175, 80, 0.2);
  background: rgba(76, 175, 80, 0.05);
}

.photo-container-single {
  width: 100%;
  height: 180px;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid rgba(76, 175, 80, 0.3);
  background: rgba(76, 175, 80, 0.05);
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
}

.detail-photo-large {
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.detail-photo-single {
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: pointer;
  transition: all 0.3s ease;
}

.detail-photo-large:hover,
.detail-photo-single:hover {
  transform: scale(1.05);
}

/* Sección de fotos */
.photo-section {
  max-height: 220px;
  overflow-y: auto;
}

.photo-item {
  margin-bottom: 12px;
}

.photo-item:last-child {
  margin-bottom: 0;
}

.photo-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #2e7d32;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.photo-container-small {
  width: 100%;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid rgba(76, 175, 80, 0.2);
  background: rgba(76, 175, 80, 0.05);
}

.detail-photo-small {
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.detail-photo-small:hover {
  transform: scale(1.05);
}

.no-photos {
  text-align: center;
  padding: 20px;
  color: rgba(76, 175, 80, 0.6);
  font-size: 0.85rem;
}

.no-photos svg {
  margin-bottom: 8px;
}

.no-photos p {
  margin: 0;
  font-style: italic;
}

/* Nuevos estilos para badges de estado específicos */
.status-badge.entrada {
  background: linear-gradient(135deg, #66BB6A, #4CAF50);
  color: white;
  border: 1px solid #4CAF50;
}

.status-badge.salida {
  background: linear-gradient(135deg, #FF9800, #F57C00);
  color: white;
  border: 1px solid #FF9800;
}

/* Responsividad */
@media (max-width: 992px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
    max-width: calc(100vw - 200px);
  }
}

/* Tablet portrait - 481px a 768px */
@media (min-width: 481px) and (max-width: 768px) {
  .main-content {
    margin-left: 250px;
    width: calc(100vw - 250px);
    max-width: calc(100vw - 250px);
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 240px;
    width: calc(100vw - 240px);
    max-width: calc(100vw - 240px);
  }
  
  .dashboard-content {
    padding: 14px;
  }
  
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 10px;
  }
  
  .stat-card {
    padding: 8px 10px;
    min-height: 50px;
    gap: 8px;
  }
  
  .svg-icon {
    width: 30px;
    height: 30px;
  }
  
  .stat-info h3 {
    font-size: 16px;
    margin-bottom: 1px;
  }
  
  .stat-info p {
    font-size: 8px;
  }
  
  .section-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .modal-overlay {
    padding: 10px;
  }
  
  .modal-content {
    max-height: 95vh;
    border-radius: 12px;
  }
  
  .modal-header {
    padding: 20px;
    border-radius: 12px 12px 0 0;
  }
  
  .modal-title {
    font-size: 18px;
  }
  
  .modal-body {
    padding: 16px;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .detail-item {
    padding: 12px;
    flex-direction: row;
    align-items: flex-start;
    text-align: left;
  }
  
  .detail-icon {
    width: 28px;
    height: 28px;
  }
  
  .modal-footer {
    display: none;
  }
  
  /* Modal de asistencia responsive */
  .asistencia-detalles .detail-grid {
    grid-template-columns: 1fr;
    grid-template-areas: 
      "user"
      "attendance"
      "photo";
    gap: 12px;
  }
  
  .detail-section {
    padding: 12px;
  }
  
  .section-header h4 {
    font-size: 11px;
  }
  
  .detail-photo-large {
    max-height: 150px;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }
  
  .stat-card {
    padding: 8px 10px;
    min-height: 50px;
    gap: 8px;
  }
  
  .svg-icon {
    width: 30px;
    height: 30px;
    border-radius: 8px;
  }
  
  .stat-info h3 {
    font-size: 16px;
    letter-spacing: 0.5px;
  }
  
  .stat-info p {
    font-size: 9px;
    letter-spacing: 0.2px;
  }
}

@media (max-width: 320px) {
  .stat-card {
    padding: 6px 8px;
    min-height: 45px;
    gap: 6px;
  }
  
  .svg-icon {
    width: 26px;
    height: 26px;
  }
  
  .stat-info h3 {
    font-size: 14px;
  }
  
  .stat-info p {
    font-size: 8px;
  }
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

/* Responsive para lightbox */
@media (max-width: 768px) {
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

/* Estilos para las pestañas */
.tabs-container {
  padding: 0 32px 24px;
}

.tabs-header {
  display: flex;
  gap: 8px;
  border-bottom: 2px solid #f0f0f0;
  margin-bottom: 24px;
}

.tab-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  border: none;
  padding: 12px 20px;
  border-radius: 12px 12px 0 0;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  color: #666;
  transition: all 0.3s ease;
  position: relative;
  border-bottom: 3px solid transparent;
}

.tab-button:hover {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.05) 0%, rgba(102, 187, 106, 0.08) 100%);
  color: #4CAF50;
  transform: translateY(-2px);
}

.tab-button.active {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(102, 187, 106, 0.15) 100%);
  color: #4CAF50;
  border-bottom-color: #4CAF50;
  font-weight: 700;
}

.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #4CAF50, #66BB6A);
  border-radius: 2px;
}

.tab-content {
  padding: 0;
  margin-top: -24px;
}

/* Estilos para badges de entradas y salidas */
.badge-entrada {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  color: white;
  padding: 8px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  display: inline-block;
  min-width: 80px;
  text-align: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
}

.badge-salida {
  background: linear-gradient(135deg, #ff5722, #ff7043);
  color: white;
  padding: 8px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  display: inline-block;
  min-width: 80px;
  text-align: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 8px rgba(255, 87, 34, 0.3);
}

.badge-tiempo {
  background: linear-gradient(135deg, #2196F3, #42A5F5);
  color: white;
  padding: 8px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  display: inline-block;
  min-width: 70px;
  text-align: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.3);
}

.badge-sin-salida {
  background: linear-gradient(135deg, #FFC107, #FFD54F);
  color: #333;
  padding: 8px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  display: inline-block;
  min-width: 120px;
  text-align: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  letter-spacing: 0.3px;
  box-shadow: 0 2px 8px rgba(255, 193, 7, 0.3);
  border: 1px solid rgba(255, 152, 0, 0.2);
}

.status-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  display: inline-block;
}

.status-badge.active {
  background: linear-gradient(135deg, #4CAF50, #66BB6A);
  color: white;
}

.status-badge.completed {
  background: linear-gradient(135deg, #607D8B, #78909C);
  color: white;
}

/* Mejoras para las columnas de fecha y hora */
.registros-table .fecha {
  font-weight: 600;
  color: #555;
  font-size: 14px;
  text-align: center;
}

.registros-table .hora-entrada,
.registros-table .hora-salida,
.registros-table .tiempo-total {
  text-align: center;
  vertical-align: middle;
}

.registros-table th {
  text-align: center;
  font-weight: 700;
  color: #333;
}

.registros-table td {
  vertical-align: middle;
  text-align: center;
}

/* Centrar contenido específico de usuario */
.registros-table .usuario-info {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

/* Centrar ubicación */
.registros-table .ubicacion {
  text-align: center;
  font-family: 'Courier New', monospace;
  font-size: 12px;
}

/* Centrar descripción */
.registros-table .descripcion {
  text-align: center;
  max-width: 200px;
  margin: 0 auto;
}

/* Tablet landscape */
@media (max-width: 768px) and (orientation: landscape) {
  .main-content {
    margin-left: 160px;
    width: calc(100vw - 160px);
    max-width: calc(100vw - 160px);
  }
}

@media (max-width: 480px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
    max-width: calc(100vw - 200px);
  }
}

@media (max-width: 375px) {
  .main-content {
    margin-left: 180px;
    width: calc(100vw - 180px);
    max-width: calc(100vw - 180px);
  }
}
</style>
