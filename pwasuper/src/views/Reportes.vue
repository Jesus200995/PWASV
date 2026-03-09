<template>
  <div class="apple-view-container">
    <!-- Apple Dynamic Background -->
    <div class="apple-dynamic-bg">
      <div class="apple-orb apple-orb-1"></div>
      <div class="apple-orb apple-orb-2"></div>
      <div class="apple-orb apple-orb-3"></div>
    </div>

    <!-- Modal de Confirmación de Firma - Apple Style -->
    <Teleport to="body">
      <Transition name="apple-modal">
        <div 
          v-if="mostrarModalFirma" 
          class="apple-modal-overlay"
          @click.self="!procesandoDescarga && cerrarModalFirma()"
        >
          <Transition name="apple-modal-content">
            <div v-if="mostrarModalFirma" class="apple-modal-container">
              <!-- Drag Handle -->
              <div class="apple-modal-handle"></div>
              
              <!-- Header con icono animado -->
              <div class="apple-modal-header">
                <div class="apple-modal-icon-wrapper">
                  <div class="apple-modal-icon apple-modal-icon-gradient">
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
                    </svg>
                  </div>
                </div>
                <h2 class="apple-modal-title">Generar Reporte</h2>
                <p class="apple-modal-subtitle">Confirma y firma tu reporte de actividades</p>
              </div>

              <!-- Contenido -->
              <div class="apple-modal-body">
                <!-- Info Card del Reporte -->
                <div class="apple-modal-info-card">
                  <div class="apple-modal-info-row">
                    <div class="apple-modal-info-icon apple-icon-blue">
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                      </svg>
                    </div>
                    <div class="apple-modal-info-content">
                      <span class="apple-modal-info-label">Reporte</span>
                      <span class="apple-modal-info-value">{{ mesActual }} {{ anioSeleccionado }}</span>
                    </div>
                  </div>
                  <div class="apple-modal-info-divider"></div>
                  <div class="apple-modal-info-row">
                    <div class="apple-modal-info-icon apple-icon-indigo">
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
                      </svg>
                    </div>
                    <div class="apple-modal-info-content">
                      <span class="apple-modal-info-label">Actividades</span>
                      <span class="apple-modal-info-value">{{ actividades.length }} registros</span>
                    </div>
                  </div>
                  <div class="apple-modal-info-divider"></div>
                  <div class="apple-modal-info-row">
                    <div class="apple-modal-info-icon" :class="formatoSeleccionado === 'pdf' ? 'apple-icon-pdf' : 'apple-icon-csv'">
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                      </svg>
                    </div>
                    <div class="apple-modal-info-content">
                      <span class="apple-modal-info-label">Formato</span>
                      <span class="apple-modal-info-value">{{ formatoSeleccionado.toUpperCase() }}</span>
                    </div>
                  </div>
                </div>

                <!-- Firmante Card -->
                <div class="apple-modal-signer-card">
                  <div class="apple-modal-signer-avatar">
                    <span>{{ iniciales }}</span>
                  </div>
                  <div class="apple-modal-signer-info">
                    <span class="apple-modal-signer-name">{{ usuarioInfo.nombre }}</span>
                    <span class="apple-modal-signer-email">{{ usuarioInfo.correo }}</span>
                  </div>
                  <div class="apple-modal-signer-badge">
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                    </svg>
                  </div>
                </div>

                <!-- Confirmación de firma realizada -->
                <div class="apple-modal-confirmed">
                  <div class="apple-confirmed-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
                    </svg>
                  </div>
                  <p class="apple-confirmed-text">
                    Tu firma digital ha sido registrada. Al continuar, autorizas el envío del reporte.
                  </p>
                </div>
              </div>

              <!-- Footer con botones Apple -->
              <div class="apple-modal-footer">
                <button
                  @click="cerrarModalFirma"
                  :disabled="procesandoDescarga"
                  class="apple-modal-btn apple-modal-btn-secondary"
                >
                  Cancelar
                </button>
                <button
                  @click.stop.prevent="confirmarYDescargar"
                  :disabled="procesandoDescarga"
                  class="apple-modal-btn apple-modal-btn-primary"
                  :class="{ 'apple-modal-btn-disabled': procesandoDescarga }"
                >
                  <div v-if="procesandoDescarga" class="apple-modal-btn-spinner"></div>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                  </svg>
                  <span>{{ procesandoDescarga ? 'Generando...' : 'Generar y Enviar' }}</span>
                </button>
              </div>
            </div>
          </Transition>
        </div>
      </Transition>
    </Teleport>

    <!-- Header Fijo Apple Style -->
    <div class="apple-header-fixed">
      <div class="apple-header-content">
        <div class="apple-compact-header">
          <div class="apple-compact-row">
            <div class="apple-compact-title-group">
              <h1 class="apple-compact-title">Reportes</h1>
              <p class="apple-compact-subtitle">{{ mesActual }} {{ anioSeleccionado }}</p>
            </div>
            <div class="apple-compact-right">
              <!-- Status Stack (dos columnas apiladas) -->
              <div class="apple-status-stack">
                <div class="apple-status-pill apple-pill-sm" :class="reporteExistente ? 'apple-pill-blue' : 'apple-pill-gray'">
                  <div class="apple-pill-dot"></div>
                  <span>{{ reporteExistente ? 'Generado' : 'Sin generar' }}</span>
                </div>
                <div class="apple-status-pill apple-pill-sm" :class="reporteExistente ? (estadoReporte === 'Firmado' ? 'apple-pill-green' : 'apple-pill-amber') : 'apple-pill-muted'">
                  <div class="apple-pill-dot"></div>
                  <span>{{ reporteExistente ? estadoReporte : 'Sin firmar' }}</span>
                </div>
              </div>
              <div class="apple-stat-badge">
                <span class="apple-badge-value">{{ estadisticas.totalActividades }}</span>
                <span class="apple-badge-label">Actividades</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="apple-scroll-container">
      <div class="apple-content-wrapper">
        <div class="apple-sections-container">
          <!-- Selector de Período Apple -->
          <div class="apple-section-card">
            <div class="apple-section-header">
              <div class="apple-section-icon apple-icon-blue">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
              </div>
              <div>
                <h2 class="apple-section-title">Período</h2>
                <p class="apple-section-subtitle">Selecciona mes y año</p>
              </div>
            </div>
            
            <div class="apple-select-grid">
              <div class="apple-select-wrap">
                <label class="apple-select-label">Mes</label>
                <select
                  v-model.number="mesSeleccionado"
                  @change="cambiarPeriodo"
                  class="apple-select"
                >
                  <option v-for="(mes, index) in meses" :key="index" :value="index">
                    {{ mes }}
                  </option>
                </select>
              </div>
              <div class="apple-select-wrap">
                <label class="apple-select-label">Año</label>
                <select
                  v-model.number="anioSeleccionado"
                  @change="cambiarPeriodo"
                  class="apple-select"
                >
                  <option v-for="year in anos" :key="year" :value="year">
                    {{ year }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <!-- Sección de Actividades Apple -->
          <div class="apple-section-card">
            <div class="apple-section-header">
              <div class="apple-section-icon apple-icon-indigo">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
                </svg>
              </div>
              <div>
                <h2 class="apple-section-title">Actividades</h2>
                <p class="apple-section-subtitle">Listado del período seleccionado</p>
              </div>
            </div>

            <!-- Error Message Apple Style -->
            <div v-if="error" class="apple-error-banner">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
              <div class="flex-1">
                <p class="text-sm font-medium">{{ error }}</p>
                <button @click="cargarActividades" class="apple-link-btn mt-1">Reintentar</button>
              </div>
            </div>

            <!-- Loading Apple Style -->
            <div v-else-if="cargando" class="apple-loading-state">
              <div class="apple-spinner"></div>
              <p class="apple-loading-text">Cargando actividades...</p>
            </div>

            <!-- Activities List Apple Style -->
            <div v-else class="apple-activities-container">
              <div v-if="actividades.length > 0" class="apple-activity-list">
                <div
                  v-for="(actividad, index) in actividades"
                  :key="actividad.id || index"
                  class="apple-activity-item"
                >
                  <div class="apple-activity-date">
                    <span class="apple-date-day">{{ formatearFecha(actividad.fecha_hora) }}</span>
                    <span class="apple-date-time">{{ formatearHora(actividad.fecha_hora) }}</span>
                  </div>
                  <div class="apple-activity-type">
                    <span
                      :class="[
                        'apple-type-badge',
                        actividad.tipo_actividad === 'campo' 
                          ? 'apple-badge-green'
                          : actividad.tipo_actividad === 'gabinete'
                          ? 'apple-badge-purple'
                          : 'apple-badge-blue'
                      ]"
                    >
                      {{ capitalizar(actividad.tipo_actividad || 'campo') }}
                    </span>
                  </div>
                </div>
              </div>
              
              <!-- Empty State Apple -->
              <div v-else class="apple-empty-state">
                <div class="apple-empty-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
                  </svg>
                </div>
                <p class="apple-empty-text">Sin actividades en este período</p>
              </div>
            </div>
          </div>

          <!-- Estado del Reporte: Ya Generado -->
          <Transition name="apple-fade" mode="out-in">
            <div v-if="reporteExistente" key="generated" class="apple-section-card apple-generated-card">
              <!-- Header de éxito -->
              <div class="apple-section-header">
                <div class="apple-section-icon apple-icon-green">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <div>
                  <h2 class="apple-section-title">Reporte Generado</h2>
                  <p class="apple-section-subtitle">{{ mesActual }} {{ anioSeleccionado }}</p>
                </div>
              </div>

              <!-- Info del reporte generado -->
              <div class="apple-generated-info">
                <div class="apple-generated-row">
                  <div class="apple-generated-label">
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                    </svg>
                    <span>Fecha de generación</span>
                  </div>
                  <span class="apple-generated-value">{{ formatearFechaReporte(reporteExistente.fecha_generacion) }}</span>
                </div>
                <div class="apple-generated-row">
                  <div class="apple-generated-label">
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    <span>Estado de firma</span>
                  </div>
                  <div class="apple-status-pill apple-pill-sm" :class="reporteExistente.firmado_territorial ? 'apple-pill-green' : 'apple-pill-blue'">
                    <div class="apple-pill-dot"></div>
                    <span>{{ reporteExistente.firmado_territorial ? 'Firmado' : 'Pendiente' }}</span>
                  </div>
                </div>
              </div>

              <!-- Mensaje informativo -->
              <div class="apple-info-box">
                <div class="apple-info-box-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <div class="apple-info-box-content">
                  <p class="apple-info-box-title">¿Necesitas generar uno nuevo?</p>
                  <p class="apple-info-box-text" v-if="!reporteExistente.firmado_territorial">
                    Puedes eliminar este reporte desde el historial y generar uno nuevo con la información actualizada.
                  </p>
                  <p class="apple-info-box-text" v-else>
                    Este reporte ya fue firmado por tu Territorial. Contacta con él para solicitar la eliminación y poder generar uno nuevo.
                  </p>
                </div>
              </div>

              <!-- Acciones -->
              <div class="apple-generated-actions">
                <button 
                  v-if="!reporteExistente.firmado_territorial"
                  @click="scrollToHistorial"
                  class="apple-action-btn apple-action-secondary"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                  </svg>
                  <span>Ir al Historial</span>
                </button>
                <button 
                  v-else
                  class="apple-action-btn apple-action-contact"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
                  </svg>
                  <span>Contactar Territorial</span>
                </button>
              </div>
            </div>

            <!-- Firmar y Generar - Cuando NO hay reporte -->
            <div v-else key="generate" class="apple-section-card apple-generate-card">
              <!-- Header con pasos -->
            <div class="apple-section-header">
              <div class="apple-section-icon apple-icon-green">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
              </div>
              <div>
                <h2 class="apple-section-title">Firmar y Generar</h2>
                <p class="apple-section-subtitle">Firma, selecciona formato y genera tu reporte</p>
              </div>
            </div>

            <!-- Steps Container -->
            <div class="apple-steps-container">
              <!-- Step 1: Firma -->
              <div class="apple-step-card apple-step-firma-layout" :class="{ 'apple-step-completed': tieneFirma }">
                <div class="apple-firma-header-row">
                  <div class="apple-step-number" :class="{ 'apple-step-done': tieneFirma }">
                    <span v-if="!tieneFirma">1</span>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
                    </svg>
                  </div>
                  <div class="apple-step-header">
                    <span class="apple-step-title">Tu Firma</span>
                    <span v-if="tieneFirma" class="apple-step-badge apple-badge-success">Listo</span>
                    <span v-else class="apple-step-badge apple-badge-pending">Pendiente</span>
                  </div>
                </div>
                <div class="apple-firma-area-full">
                  <FirmaDigital
                    ref="firmaComponent"
                    label="Firmar aquí"
                    @firmado="onFirmaRealizada"
                    @borrado="onFirmaBorrada"
                  />
                </div>
              </div>

              <!-- Step 2: Formato -->
              <div class="apple-step-card" :class="{ 'apple-step-active': tieneFirma }">
                <div class="apple-step-number" :class="{ 'apple-step-done': tieneFirma }">
                  <span>2</span>
                </div>
                <div class="apple-step-content">
                  <div class="apple-step-header">
                    <span class="apple-step-title">Formato</span>
                  </div>
                  <div class="apple-format-row">
                    <label class="apple-format-chip" :class="{ 'apple-chip-active': formatoSeleccionado === 'pdf' }">
                      <input type="radio" v-model="formatoSeleccionado" value="pdf" class="sr-only" />
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                      </svg>
                      <span>PDF</span>
                    </label>
                    <label class="apple-format-chip" :class="{ 'apple-chip-active': formatoSeleccionado === 'csv' }">
                      <input type="radio" v-model="formatoSeleccionado" value="csv" class="sr-only" />
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                      </svg>
                      <span>CSV</span>
                    </label>
                  </div>
                </div>
              </div>
            </div>

            <!-- Info del firmante compacta -->
            <div class="apple-signer-strip">
              <div class="apple-signer-avatar-sm">{{ iniciales }}</div>
              <div class="apple-signer-details">
                <span class="apple-signer-name-sm">{{ usuarioInfo.nombre }}</span>
                <span class="apple-signer-meta">{{ mesActual }} {{ anioSeleccionado }} · {{ actividades.length }} actividades</span>
              </div>
            </div>

            <!-- Warning si ya existe -->
            <div v-if="reporteExistente" class="apple-inline-warning">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
              <span>Ya existe un reporte de este mes</span>
            </div>

            <!-- Botón principal unificado -->
            <button
              @click="iniciarDescarga"
              :disabled="cargando || generandoReporte || actividades.length === 0 || reporteExistente || verificandoReporte || !tieneFirma"
              class="apple-btn-generate-unified"
              :class="{ 
                'apple-btn-ready': tieneFirma && actividades.length > 0 && !reporteExistente,
                'apple-btn-disabled': cargando || generandoReporte || actividades.length === 0 || reporteExistente || verificandoReporte || !tieneFirma 
              }"
            >
              <div v-if="verificandoReporte || generandoReporte" class="apple-btn-spinner"></div>
              <template v-else>
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                </svg>
              </template>
              <span>{{ getBotonTexto }}</span>
            </button>
          </div>
          </Transition>

          <!-- Historial de Reportes Apple -->
          <div class="apple-section-card">
            <div class="apple-section-header apple-section-header-between">
              <div class="apple-section-header-left">
                <div class="apple-section-icon apple-icon-amber">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <div>
                  <h2 class="apple-section-title">Historial</h2>
                  <p class="apple-section-subtitle">Reportes generados</p>
                </div>
              </div>
              <button 
                @click="cargarHistorialReportes" 
                :disabled="cargandoHistorial"
                class="apple-refresh-btn"
                title="Recargar historial"
              >
                <svg :class="['w-4 h-4', cargandoHistorial ? 'animate-spin' : '']" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
              </button>
            </div>
            
            <!-- Loading State Apple -->
            <div v-if="cargandoHistorial" class="apple-loading-state">
              <div class="apple-spinner"></div>
              <p class="apple-loading-text">Cargando historial...</p>
            </div>
            
            <!-- Error State Apple -->
            <div v-else-if="errorHistorial" class="apple-error-state">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
              <p class="apple-error-text">{{ errorHistorial }}</p>
              <button @click="cargarHistorialReportes" class="apple-link-btn">Reintentar</button>
            </div>
            
            <!-- Reports List Apple Style -->
            <div v-else-if="reportesGenerados.length > 0" class="apple-reports-list">
              <div
                v-for="reporte in reportesGenerados"
                :key="reporte.id"
                class="apple-report-card"
                :class="reporte.firmado_supervisor ? 'apple-report-signed' : 'apple-report-pending'"
              >
                <!-- Report Header -->
                <div class="apple-report-header">
                  <div class="apple-report-icon" :class="reporte.tipo === 'PDF' ? 'apple-icon-pdf' : 'apple-icon-csv'">
                    <svg v-if="reporte.tipo === 'PDF'" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                  </div>
                  <div class="apple-report-info">
                    <p class="apple-report-name">{{ reporte.nombre }}</p>
                    <p class="apple-report-date">{{ formatearFechaCompleta(reporte.fecha) }}</p>
                  </div>
                  <span class="apple-report-badge" :class="reporte.tipo === 'PDF' ? 'apple-badge-red' : 'apple-badge-green-alt'">
                    {{ reporte.tipo }}
                  </span>
                </div>

                <!-- Status Banner -->
                <div class="apple-status-banner" :class="reporte.firmado_supervisor ? 'apple-status-success' : 'apple-status-warning'">
                  <div class="apple-status-icon">
                    <svg v-if="reporte.firmado_supervisor" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                  </div>
                  <div class="apple-status-text">
                    <p class="apple-status-title">{{ reporte.firmado_supervisor ? 'Firmado por supervisor' : 'Pendiente de firma' }}</p>
                    <p class="apple-status-subtitle">{{ reporte.firmado_supervisor ? `${reporte.nombre_supervisor} • ${formatearFechaFirma(reporte.fecha_firma_supervisor)}` : 'Esperando revisión' }}</p>
                  </div>
                </div>

                <!-- Action Buttons -->
                <div class="apple-report-actions">
                  <button
                    @click="verReporteHistorial(reporte)"
                    :disabled="viendoReporte === reporte.id"
                    class="apple-action-btn apple-action-view"
                  >
                    <div v-if="viendoReporte === reporte.id" class="apple-btn-spinner-sm"></div>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                    </svg>
                    <span>Ver</span>
                  </button>
                  
                  <button
                    @click="descargarReporteHistorial(reporte)"
                    :disabled="descargandoReporte === reporte.id"
                    class="apple-action-btn apple-action-download"
                  >
                    <div v-if="descargandoReporte === reporte.id" class="apple-btn-spinner-sm"></div>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                    </svg>
                    <span>Descargar</span>
                  </button>
                  
                  <button
                    v-if="!reporte.firmado_supervisor"
                    @click="eliminarReporteHistorial(reporte)"
                    :disabled="eliminandoReporte === reporte.id"
                    class="apple-action-btn apple-action-delete"
                  >
                    <div v-if="eliminandoReporte === reporte.id" class="apple-btn-spinner-sm"></div>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                    <span>Eliminar</span>
                  </button>
                  
                  <span v-else class="apple-action-btn apple-action-locked">
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                    </svg>
                    <span>Protegido</span>
                  </span>
                </div>
              </div>
            </div>
            
            <!-- Empty State Apple -->
            <div v-else class="apple-empty-state">
              <div class="apple-empty-icon">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
              </div>
              <p class="apple-empty-text">Sin reportes generados</p>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal Apple Style -->
    <Teleport to="body">
      <Transition name="apple-modal">
        <div
          v-if="mostrarModalEliminar"
          class="apple-confirm-overlay"
          @click.self="cancelarEliminar"
        >
          <Transition name="apple-modal-content">
            <div v-if="mostrarModalEliminar" class="apple-confirm-modal">
              <div class="apple-confirm-icon apple-confirm-danger">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
              </div>
              <h3 class="apple-confirm-title">¿Eliminar reporte?</h3>
              <p class="apple-confirm-subtitle">{{ reporteAEliminar?.nombre }}</p>
              <div class="apple-confirm-actions">
                <button @click="cancelarEliminar" class="apple-confirm-btn apple-confirm-cancel">
                  Cancelar
                </button>
                <button @click="confirmarEliminarReporte" class="apple-confirm-btn apple-confirm-delete">
                  Eliminar
                </button>
              </div>
            </div>
          </Transition>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script>
import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';
import { PDFDocument } from 'pdf-lib';
import FirmaDigital from '../components/FirmaDigital.vue';
import { apiService, api } from '../services/apiService.js';
import { checkInternetConnection, getOfflineMessage } from '../utils/network.js';
import superiorImage from '../../images/superior2.png';

/**
 * Función para limpiar strings base64 que pueden tener prefijos o caracteres inválidos
 */
function limpiarBase64(base64String) {
  if (!base64String) return null;
  
  let base64 = base64String;
  
  // Remover prefijo data URI si existe (ej: data:application/pdf;base64,)
  if (base64.includes(',')) {
    base64 = base64.split(',')[1];
  }
  
  // Remover prefijo específico que puede aparecer
  if (base64.startsWith('data:application/pdf;base64,')) {
    base64 = base64.replace('data:application/pdf;base64,', '');
  }
  
  // Remover espacios en blanco y saltos de línea
  base64 = base64.replace(/\s/g, '');
  
  // Asegurar que solo contiene caracteres válidos de base64
  base64 = base64.replace(/[^A-Za-z0-9+/=]/g, '');
  
  // Agregar padding si es necesario
  while (base64.length % 4 !== 0) {
    base64 += '=';
  }
  
  return base64;
}

export default {
  name: 'Reportes',
  components: {
    FirmaDigital
  },
  data() {
    return {
      actividades: [],
      todasLasActividades: [],
      cargando: false,
      generandoReporte: false,
      mesSeleccionado: new Date().getMonth(),
      anioSeleccionado: new Date().getFullYear(),
      anos: [],
      formatoSeleccionado: 'pdf',
      usuarioInfo: {
        nombre: '',
        cargo: '',
        correo: '',
        territorio: '',
        curp: '',
        supervisor: ''
      },
      reportesGenerados: [],
      meses: [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
      ],
      // Modal de confirmación de firma
      mostrarModalFirma: false,
      confirmarFirma: false,
      procesandoDescarga: false,
      // Estado de la firma digital
      tieneFirma: false,
      // Estado de descarga de reportes del historial
      descargandoReporte: null,
      // Estado de visualización de reportes del historial
      viendoReporte: null,
      // Estado de eliminación de reportes del historial
      eliminandoReporte: null,
      // Modal de confirmación para eliminar
      mostrarModalEliminar: false,
      reporteAEliminar: null,
      // Estado de conexión
      isOnline: true,
      error: null,
      // Reporte ya existente para el mes/año seleccionado
      reporteExistente: null,
      verificandoReporte: false,
      // Estado de carga del historial
      cargandoHistorial: false,
      errorHistorial: null,
      // Referencias temporales para PDF generado (para descarga después de guardar en BD)
      _pdfDocumentoGenerado: null,
      _pdfNombreArchivo: null
    };
  },
  computed: {
    mesActual() {
      return this.meses[this.mesSeleccionado];
    },
    dateRange() {
      const inicio = new Date(this.anioSeleccionado, this.mesSeleccionado, 1);
      const fin = new Date(this.anioSeleccionado, this.mesSeleccionado + 1, 0);
      return `${inicio.toLocaleDateString()} - ${fin.toLocaleDateString()}`;
    },
    estadisticas() {
      return {
        totalActividades: this.actividades.length
      };
    },
    estadoReporte() {
      if (this.actividades.length === 0) return 'Sin datos';
      if (this.$refs.firmaComponent?.hayFirma) return 'Firmado';
      return 'Sin firmar';
    },
    // Texto dinámico del botón de generar
    getBotonTexto() {
      if (this.verificandoReporte) return 'Verificando...';
      if (this.generandoReporte) return 'Generando...';
      if (this.reporteExistente) return 'Reporte ya generado';
      if (this.actividades.length === 0) return 'Sin actividades';
      if (!this.tieneFirma) return 'Firma primero';
      return 'Firmar y Generar';
    },
    // Obtener iniciales del usuario
    iniciales() {
      if (!this.usuarioInfo.nombre) return 'U';
      const partes = this.usuarioInfo.nombre.split(' ');
      if (partes.length >= 2) {
        return (partes[0][0] + partes[1][0]).toUpperCase();
      }
      return partes[0].substring(0, 2).toUpperCase();
    }
  },
  methods: {
    async cargarActividades() {
      this.cargando = true;
      this.error = null;
      
      try {
        const usuario = JSON.parse(localStorage.getItem('user'));
        
        if (!usuario || !usuario.id) {
          console.error('❌ No hay usuario en localStorage');
          throw new Error('Usuario no autenticado');
        }
        
        console.log(`📋 Cargando TODAS las actividades para usuario ${usuario.id}`);
        
        // Usar apiService que auto-detecta servidor (producción si localhost no disponible)
        const response = await apiService.getRecords(usuario.id);

        console.log('✅ Respuesta del servidor:', response);

        if (!response || !response.registros) {
          throw new Error('No se recibió respuesta del servidor');
        }

        // Obtener la URL actual del API para las fotos
        const currentApiUrl = apiService.getCurrentApiUrl();
        
        // Procesar las URLs de las fotos para que sean rutas absolutas
        this.todasLasActividades = response.registros.map(r => ({
          ...r,
          foto_url: r.foto_url ? `${currentApiUrl}/${r.foto_url}` : null
        }));
        
        // Filtrar por mes/año seleccionado
        this.filtrarActividadesPorPeriodo();
        
        console.log(`✅ Total de actividades: ${this.todasLasActividades.length}`);
        console.log(`✅ Actividades en período seleccionado: ${this.actividades.length}`);
        
      } catch (err) {
        console.error('❌ Error cargando actividades:', err);
        this.actividades = [];
        this.todasLasActividades = [];
        
        if (err.response) {
          // Error de respuesta del servidor
          if (err.response.status === 500) {
            this.error = 'El servidor está experimentando problemas técnicos. Por favor, inténtalo más tarde.';
          } else {
            this.error = 'Error del servidor: ' + (err.response.data.detail || err.response.statusText);
          }
        } else if (err.request) {
          // Error de conexión
          this.error = 'No se pudo conectar con el servidor. Verifica tu conexión a internet.';
        } else {
          // Error general
          this.error = 'Error al cargar las actividades: ' + err.message;
        }
      } finally {
        this.cargando = false;
      }
    },

    filtrarActividadesPorPeriodo() {
      // Filtrar actividades por mes y año seleccionado
      const inicioDeMes = new Date(this.anioSeleccionado, this.mesSeleccionado, 1);
      const finDelMes = new Date(this.anioSeleccionado, this.mesSeleccionado + 1, 0, 23, 59, 59);
      
      this.actividades = this.todasLasActividades.filter(actividad => {
        if (!actividad.fecha_hora) return false;
        
        const fechaActividad = new Date(actividad.fecha_hora);
        return fechaActividad >= inicioDeMes && fechaActividad <= finDelMes;
      });
      
      // Ordenar de más antigua a más reciente (inicio del mes primero)
      this.actividades.sort((a, b) => {
        const fechaA = new Date(a.fecha_hora);
        const fechaB = new Date(b.fecha_hora);
        return fechaA - fechaB; // Orden ascendente (más antigua primero)
      });
      
      console.log(`🔍 Filtrado y ordenado: ${this.actividades.length} actividades (inicio del mes primero)`);
    },

    async cambiarPeriodo() {
      // Limpiar estado de reporte existente
      this.reporteExistente = null;
      
      // Limpiar firma al cambiar de período
      this.tieneFirma = false;
      if (this.$refs.firmaComponent) {
        this.$refs.firmaComponent.limpiarFirma();
      }
      
      // Solo filtrar si ya tenemos actividades cargadas
      if (this.todasLasActividades && this.todasLasActividades.length > 0) {
        this.filtrarActividadesPorPeriodo();
      } else {
        this.cargarActividades();
      }
      
      // Verificar si ya existe un reporte para este mes/año
      await this.verificarReporteExistente();
    },
    
    async verificarReporteExistente() {
      if (!this.usuarioInfo.id) return;
      
      try {
        this.verificandoReporte = true;
        const response = await api.get(`/reportes/verificar/${this.usuarioInfo.id}`, {
          params: {
            mes: this.mesActual,
            anio: this.anioSeleccionado
          }
        });
        
        if (response.data.existe) {
          this.reporteExistente = response.data.reporte;
          console.log(`📋 Ya existe reporte para ${this.mesActual} ${this.anioSeleccionado}`);
        } else {
          this.reporteExistente = null;
        }
      } catch (error) {
        console.error('⚠️ Error verificando reporte existente:', error);
        this.reporteExistente = null;
      } finally {
        this.verificandoReporte = false;
      }
    },

    formatearFecha(fechaHora) {
      if (!fechaHora) return '-';
      const date = new Date(fechaHora);
      return date.toLocaleDateString('es-MX', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },

    formatearHora(fechaHora) {
      if (!fechaHora) return '-';
      const date = new Date(fechaHora);
      return date.toLocaleTimeString('es-MX', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      });
    },

    formatearFechaFirma(fechaFirma) {
      if (!fechaFirma) return '';
      const date = new Date(fechaFirma);
      return date.toLocaleDateString('es-MX', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    formatearFechaCompleta(fecha) {
      if (!fecha) return '-';
      const date = new Date(fecha);
      return date.toLocaleDateString('es-MX', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      });
    },

    capitalizar(texto) {
      return texto.charAt(0).toUpperCase() + texto.slice(1);
    },

    // Verificar si hay firma válida (método en lugar de computed para reactividad con refs)
    esFirmaValida() {
      return this.$refs.firmaComponent?.hayFirma || false;
    },

    // Iniciar proceso de descarga - verificar firma primero
    async iniciarDescarga() {
      if (this.actividades.length === 0) {
        alert('No hay actividades para generar el reporte');
        return;
      }

      // Verificar si hay firma
      if (!this.tieneFirma || !this.$refs.firmaComponent?.hayFirma) {
        alert('Por favor, firma el reporte antes de descargarlo');
        return;
      }

      // Verificar si ya existe un reporte para este mes/año
      try {
        this.verificandoReporte = true;
        const response = await api.get(`/reportes/verificar/${this.usuarioInfo.id}`, {
          params: {
            mes: this.mesActual,
            anio: this.anioSeleccionado
          }
        });
        
        if (response.data.existe) {
          this.reporteExistente = response.data.reporte;
          const fechaGeneracion = new Date(response.data.reporte.fecha_generacion).toLocaleDateString('es-MX', {
            day: 'numeric',
            month: 'long',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
          });
          alert(`Ya existe un reporte firmado para ${this.mesActual} ${this.anioSeleccionado}.\n\nFue generado el ${fechaGeneracion}.\n\nSolo puedes generar un reporte por mes.`);
          return;
        }
      } catch (error) {
        console.error('⚠️ Error verificando reporte existente:', error);
        // Si hay error de conexión, permitir continuar pero advertir
        if (!navigator.onLine) {
          alert('⚠️ Sin conexión. No se puede verificar si ya existe un reporte para este mes.');
          return;
        }
      } finally {
        this.verificandoReporte = false;
      }

      // Mostrar modal de confirmación rápida
      this.confirmarFirma = true; // Ya está firmado, auto-confirmar
      this.mostrarModalFirma = true;
    },

    // Cerrar modal
    cerrarModalFirma() {
      this.mostrarModalFirma = false;
      this.confirmarFirma = false;
    },

    // Callback cuando se realiza una firma
    onFirmaRealizada() {
      this.tieneFirma = true;
      console.log('✅ Firma realizada');
    },

    // Callback cuando se borra la firma
    onFirmaBorrada() {
      this.tieneFirma = false;
      console.log('🗑️ Firma borrada');
    },

    // Scroll suave al historial de reportes
    scrollToHistorial() {
      // Buscar la sección de historial y hacer scroll
      setTimeout(() => {
        const historialSection = document.querySelector('.apple-reports-list, .apple-section-card:has(.apple-icon-amber)');
        if (historialSection) {
          historialSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
          });
        }
      }, 100);
    },

    // Formatear fecha de generación del reporte
    formatearFechaReporte(fecha) {
      if (!fecha) return 'Fecha no disponible';
      const date = new Date(fecha);
      const options = { 
        day: 'numeric', 
        month: 'short', 
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      };
      return date.toLocaleDateString('es-MX', options);
    },

    // Confirmar y proceder con la descarga - NO CIERRA EL MODAL HASTA TERMINAR
    async confirmarYDescargar() {
      console.log('🔵 [INICIO] confirmarYDescargar() llamado');
      
      // Prevenir doble clic
      if (this.procesandoDescarga) {
        console.log('⚠️ Ya se está procesando una descarga');
        return;
      }
      
      console.log('🔵 [PASO 1] Verificando confirmarFirma:', this.confirmarFirma);
      if (!this.confirmarFirma) {
        console.log('⚠️ No se ha confirmado la firma');
        return;
      }
      
      // Verificar firma
      console.log('🔵 [PASO 2] Verificando componente firma:', this.$refs.firmaComponent);
      const firmaValida = this.$refs.firmaComponent?.hayFirma || false;
      console.log('🔵 [PASO 2.1] Firma válida:', firmaValida);
      if (!firmaValida) {
        alert('La firma no es válida. Por favor, vuelve a firmar.');
        return;
      }
      
      // Verificar actividades
      console.log('🔵 [PASO 3] Total actividades:', this.actividades.length);
      if (this.actividades.length === 0) {
        alert('No hay actividades para generar el reporte');
        return;
      }

      console.log('🚀 [PASO 4] Iniciando proceso de guardado de reporte...');
      
      // Activar estado de procesamiento - EL MODAL SE MANTIENE ABIERTO
      this.procesandoDescarga = true;
      this.generandoReporte = true;
      
      try {
        console.log('📄 [PASO 5] Preparando datos del reporte...');
        
        // NUEVO FLUJO: Guardar datos estructurados, NO generar PDF
        const firmaUsuarioBase64 = this.$refs.firmaComponent.obtenerFirmaBase64();
        
        // NO convertir fotos a base64 para guardar - solo guardar las actividades con foto_url
        console.log('📸 [PASO 6] Preparando actividades sin convertir fotos a base64...');
        const actividadesParaGuardar = this.actividades.map(act => ({
          id: act.id,
          fecha_hora: act.fecha_hora,
          fecha: act.fecha_hora, // También como "fecha" para compatibilidad
          tipo_actividad: act.tipo_actividad,
          tipo: act.tipo_actividad, // También como "tipo" para compatibilidad
          categoria_actividad: act.categoria_actividad,
          descripcion: act.descripcion,
          foto_url: act.foto_url, // Solo guardamos la URL, no el base64
          latitud: act.latitud,
          longitud: act.longitud
        }));
        
        console.log(`📋 [PASO 7] ${actividadesParaGuardar.length} actividades preparadas`);
        console.log(`📸 [PASO 7.1] Actividades con foto: ${actividadesParaGuardar.filter(a => a.foto_url).length}`);
        
        // Construir objeto con los datos del reporte
        console.log('🔵 [PASO 8] Construyendo datos del reporte...');
        const datosReporte = {
          // Información del usuario
          usuario: {
            id: this.usuarioInfo.id,
            nombre: this.usuarioInfo.nombre,
            cargo: this.usuarioInfo.cargo,
            curp: this.usuarioInfo.curp,
            territorio: this.usuarioInfo.territorio,
            supervisor: this.usuarioInfo.supervisor,
            correo: this.usuarioInfo.correo
          },
          // Período del reporte
          periodo: {
            mes: this.mesSeleccionado,
            mesNombre: this.mesActual,
            anio: this.anioSeleccionado,
            fechaInicio: new Date(this.anioSeleccionado, this.mesSeleccionado, 1).toISOString(),
            fechaFin: new Date(this.anioSeleccionado, this.mesSeleccionado + 1, 0).toISOString()
          },
          // Actividades del período (solo con foto_url, no base64)
          actividades: actividadesParaGuardar,
          // Estadísticas
          estadisticas: {
            totalActividades: actividadesParaGuardar.length,
            actividadesCampo: actividadesParaGuardar.filter(a => (a.tipo_actividad || '').toLowerCase() === 'campo').length,
            actividadesGabinete: actividadesParaGuardar.filter(a => (a.tipo_actividad || '').toLowerCase() === 'gabinete').length,
            actividadesConFoto: actividadesParaGuardar.filter(a => a.foto_url).length
          },
          // Fecha de generación
          fechaGeneracion: new Date().toISOString()
        };

        console.log('✅ [PASO 9] Datos del reporte preparados:', datosReporte.estadisticas);
        const jsonSize = JSON.stringify(datosReporte).length;
        console.log(`📦 [PASO 9.1] Tamaño del JSON: ${(jsonSize / 1024).toFixed(2)} KB`);

        // Agregar a historial local con TODOS los campos necesarios
        const fecha = new Date().toLocaleString('es-MX');
        const nombreReporte = `Reporte ${this.mesActual} ${this.anioSeleccionado}`;
        
        // Crear el objeto del reporte con todos los campos
        const nuevoReporte = {
          id: Date.now(), // ID temporal, se actualizará con el de BD
          nombre: nombreReporte,
          mes: this.mesActual,
          anio: this.anioSeleccionado,
          fecha,
          tipo: 'PDF',
          tiene_pdf: true, // Se puede generar PDF desde datos
          firmado_supervisor: false
        };

        // Guardar en la base de datos (datos estructurados + firma usuario)
        try {
          console.log('💾 [PASO 10] Guardando reporte en BD (datos estructurados)...');
          
          const datosGuardar = {
            usuario_id: this.usuarioInfo.id,
            nombre_reporte: nombreReporte,
            mes: this.mesActual,
            anio: this.anioSeleccionado,
            tipo: 'PDF',
            // NUEVO: Datos estructurados y firma del usuario
            datos_reporte: datosReporte,
            firma_usuario_base64: firmaUsuarioBase64
            // NO enviamos pdf_base64 - se generará cuando se descargue
          };
          
          console.log('💾 [PASO 11] Enviando a /reportes/guardar...');
          console.log('💾 [PASO 11.1] Payload:', {
            usuario_id: datosGuardar.usuario_id,
            nombre_reporte: datosGuardar.nombre_reporte,
            mes: datosGuardar.mes,
            anio: datosGuardar.anio,
            tipo: datosGuardar.tipo,
            actividades_count: datosGuardar.datos_reporte.actividades.length,
            firma_length: datosGuardar.firma_usuario_base64?.length || 0
          });
          
          const response = await api.post('/reportes/guardar', datosGuardar);
          console.log('✅ [PASO 12] Reporte guardado en la base de datos');
          console.log('✅ [PASO 12.1] Respuesta del servidor:', response.data);
          
          // Actualizar el ID del reporte local con el ID real de la BD
          if (response.data && response.data.reporte_id) {
            nuevoReporte.id = response.data.reporte_id;
          }
          
          // Agregar al historial local DESPUÉS de confirmar guardado en BD
          this.reportesGenerados.unshift(nuevoReporte);
          
          // Actualizar localStorage
          localStorage.setItem('reportesGenerados', JSON.stringify(this.reportesGenerados));
          
          // Marcar que ya existe un reporte para este mes (REACTIVO)
          this.reporteExistente = {
            id: nuevoReporte.id,
            nombre: nombreReporte,
            fecha_generacion: new Date().toISOString()
          };
          
          console.log('🔒 reporteExistente establecido - botón se deshabilitará');
          
          // GENERAR Y DESCARGAR EL PDF INMEDIATAMENTE PARA EL USUARIO
          console.log('📄 Generando PDF para descarga inmediata...');
          try {
            const pdfBase64 = await this.generarPDFDesdesDatos(
              datosReporte,
              firmaUsuarioBase64,
              null, // Sin firma de supervisor todavía
              null
            );
            
            // Descargar el PDF
            await this.descargarPDFBase64(pdfBase64, nombreReporte);
            
            console.log('✅ PDF generado y descargado para el usuario');
          } catch (pdfError) {
            console.error('⚠️ Error generando PDF para descarga:', pdfError);
            // No bloquear el flujo si falla la descarga, el usuario puede verlo después en historial
          }
          
          // Mostrar mensaje de éxito
          this.$notify?.({
            type: 'success',
            message: 'Reporte firmado y guardado. Tu supervisor podrá revisarlo y autorizarlo.'
          });
          
        } catch (error) {
          console.error('⚠️ Error guardando reporte en BD:', error);
          console.error('⚠️ Detalles del error:', error.response?.data);
          
          // Si hay error 409 (duplicado), mostrar mensaje y no agregar al historial local
          if (error.response?.status === 409) {
            console.log('⚠️ [ERROR 409] Reporte duplicado detectado');
            this.$notify?.({
              type: 'warning',
              message: error.response.data.detail || 'Ya existe un reporte para este mes'
            });
            return; // No continuar si hay duplicado
          }
          
          // Para otros errores de BD
          console.error('❌ [ERROR BD] Error guardando en base de datos:', error);
          throw error;
        }
        
      } catch (error) {
        console.error('❌ [ERROR GENERAL] Error generando reporte:', error);
        console.error('❌ [ERROR STACK]', error.stack);
        console.error('❌ [ERROR RESPONSE]', error.response);
        this.$notify?.({
          type: 'error',
          message: 'Error al guardar el reporte: ' + (error.message || 'Error desconocido')
        });
      } finally {
        console.log('🔵 [FINALLY] Limpiando estados...');
        // AHORA sí cerramos el modal, DESPUÉS de terminar todo
        this.procesandoDescarga = false;
        this.generandoReporte = false;
        this.mostrarModalFirma = false;
        this.confirmarFirma = false;
        console.log('🏁 [FIN] Proceso de guardado finalizado');
      }
    },

    async generarReporte() {
      // Este método ya no se usa directamente, pero lo mantenemos por compatibilidad
      try {
        if (this.actividades.length === 0) {
          alert('No hay actividades para generar el reporte');
          return;
        }

        this.generandoReporte = true;

        if (this.formatoSeleccionado === 'pdf') {
          const pdfBase64 = await this.generarPDF();
          // Descargar después de generar
          if (this._pdfDocumentoGenerado) {
            await this.descargarPDFSeguro(this._pdfDocumentoGenerado, this._pdfNombreArchivo);
            this._pdfDocumentoGenerado = null;
            this._pdfNombreArchivo = null;
          }
        } else {
          this.generarCSV();
        }

        // Agregar a historial local
        const fecha = new Date().toLocaleString('es-MX');
        const nombreReporte = `Reporte ${this.mesActual} ${this.anioSeleccionado}`;
        
        this.reportesGenerados.unshift({
          id: Date.now(),
          nombre: nombreReporte,
          fecha,
          tipo: this.formatoSeleccionado.toUpperCase()
        });

        // Guardar en la base de datos
        try {
          await api.post('/reportes/guardar', {
            usuario_id: this.usuarioInfo.id,
            nombre_reporte: nombreReporte,
            mes: this.mesActual,
            anio: this.anioSeleccionado,
            tipo: this.formatoSeleccionado.toUpperCase()
          });
          console.log('✅ Reporte guardado en la base de datos');
        } catch (error) {
          console.error('⚠️ Error guardando reporte en BD:', error);
          // No mostramos error al usuario, solo lo registramos
        }

        this.$notify?.({
          type: 'success',
          message: 'Reporte generado correctamente'
        });
      } catch (error) {
        console.error('❌ Error generando reporte:', error);
        this.$notify?.({
          type: 'error',
          message: 'Error al generar el reporte'
        });
      } finally {
        this.generandoReporte = false;
      }
    },

    async generarPDF() {
      try {
        console.log('📄 Iniciando generación de PDF...');
        
        const doc = new jsPDF({
          orientation: 'portrait',
          unit: 'mm',
          format: 'a4'
        });

        const pageHeight = doc.internal.pageSize.getHeight();
        const pageWidth = doc.internal.pageSize.getWidth();
        const margin = 15;
        const contentWidth = pageWidth - (margin * 2);
        let currentY = 10;

        // ========== ENCABEZADO CON IMAGEN DE LOGOS ==========
        console.log('🖼️ Cargando imagen de encabezado...');
        
        // Cargar imagen como base64 para evitar problemas de CORS y formato
        let superiorImageBase64;
        let imgDimensions;
        try {
          const result = await this.cargarImagenComoBase64(superiorImage);
          superiorImageBase64 = result.data;
          imgDimensions = result.dimensions;
        } catch (error) {
          console.warn('⚠️ No se pudo cargar imagen de encabezado, continuando sin ella:', error);
          // Continuar sin imagen de encabezado
          currentY = 10;
        }
        
        if (superiorImageBase64 && imgDimensions) {
          // Calcular dimensiones reales manteniendo aspect ratio
          const realAspectRatio = imgDimensions.height / imgDimensions.width;
          
          // Usar 95% del ancho para que sea grande sin distorsión
          const imgWidth = contentWidth * 0.95;
          const imgHeight = imgWidth * realAspectRatio;
          
          // Centrar la imagen
          const imgX = margin + (contentWidth - imgWidth) / 2;
          
          doc.addImage(superiorImageBase64, 'PNG', imgX, currentY, imgWidth, imgHeight);
          currentY += imgHeight + 5;
          console.log('✅ Imagen de encabezado agregada');
        }
      
      // Recuadro principal con títulos
      doc.setDrawColor(0, 0, 0);
      doc.setLineWidth(0.5);
      doc.rect(margin, currentY, contentWidth, 25);
      
      // Títulos centrados
      doc.setFontSize(9);
      doc.setFont(undefined, 'bold');
      doc.setTextColor(0, 0, 0);
      doc.text('SECRETARÍA DE BIENESTAR', pageWidth / 2, currentY + 6, { align: 'center' });
      doc.text('SUBSECRETARÍA DE INCLUSIÓN PRODUCTIVA Y DESARROLLO RURAL', pageWidth / 2, currentY + 11, { align: 'center' });
      doc.text('FORMATO DE SEGUIMIENTO A ACTIVIDADES PROGRAMADAS', pageWidth / 2, currentY + 16, { align: 'center' });
      
      // Fecha en la esquina superior derecha
      const fechaActual = new Date().toLocaleDateString('es-MX', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      });
      doc.setFontSize(8);
      doc.setFont(undefined, 'normal');
      doc.text('Fecha:', pageWidth - margin - 35, currentY + 21);
      doc.rect(pageWidth - margin - 25, currentY + 18, 25, 5);
      doc.text(fechaActual, pageWidth - margin - 12.5, currentY + 21.5, { align: 'center' });
      
      currentY += 30;
      
      // ========== TABLA DE INFORMACIÓN DEL PRESTADOR ==========
      const tableStartY = currentY;
      const col1Width = contentWidth * 0.5;
      const col2Width = contentWidth * 0.5;
      
      // Fila 1: Nombre del prestador
      doc.setDrawColor(0, 0, 0);
      doc.setLineWidth(0.3);
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      
      doc.setFontSize(8);
      doc.setFont(undefined, 'bold');
      doc.text('Nombre del prestador de Servicios', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      doc.text(this.usuarioInfo.nombre, margin + col1Width + 2, currentY + 4);
      
      currentY += 6;
      
      // Fila 2: CURP
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      
      doc.setFont(undefined, 'bold');
      doc.text('CURP', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      doc.text(this.usuarioInfo.curp || 'No registrado', margin + col1Width + 2, currentY + 4);
      
      currentY += 6;
      
      // Fila 3: Periodo
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      
      doc.setFont(undefined, 'bold');
      doc.text('Periodo', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      const inicioPeriodo = new Date(this.anioSeleccionado, this.mesSeleccionado, 1);
      const finPeriodo = new Date(this.anioSeleccionado, this.mesSeleccionado + 1, 0);
      const periodoTexto = `Del ${inicioPeriodo.toLocaleDateString('es-MX')} al ${finPeriodo.toLocaleDateString('es-MX')}`;
      doc.text(periodoTexto, margin + col1Width + 2, currentY + 4);
      
      currentY += 8;
      
      // Fila 4: Programa Social del Apoyo (celda completa)
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      
      doc.setFont(undefined, 'bold');
      doc.text('Programa Social del Apoyo', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      doc.text('SEMBRANDO VIDA', margin + col1Width + 2, currentY + 4);
      
      currentY += 8;
      
      // Fila 5: Territorio (celda completa)
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      
      doc.setFont(undefined, 'bold');
      doc.text('Territorio y entidad donde presta sus servicios', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      doc.text(this.usuarioInfo.territorio || 'No asignado', margin + col1Width + 2, currentY + 4);
      
      currentY += 10;
      
      // ========== TABLA DE ACTIVIDADES ==========
      // Definir columnas de la tabla
      const tableWidth = contentWidth;
      const tableX = margin;
      const colWidths = [15, 32, 18, 22, 83]; // No., Fecha, Tipo, Hora, Actividad
      
      // Header de la tabla
      doc.setDrawColor(0, 0, 0);
      doc.setLineWidth(0.3);
      doc.setFillColor(255, 255, 255);
      doc.rect(tableX, currentY, tableWidth, 8, 'FD');
      
      doc.setTextColor(0, 0, 0);
      doc.setFontSize(8);
      doc.setFont(undefined, 'bold');
      
      let colX = tableX + 2;
      doc.text('No.', colX + colWidths[0]/2, currentY + 5.5, { align: 'center' });
      doc.line(colX + colWidths[0], currentY, colX + colWidths[0], currentY + 8);
      
      colX += colWidths[0];
      doc.text('Fecha', colX + colWidths[1]/2, currentY + 5.5, { align: 'center' });
      doc.line(colX + colWidths[1], currentY, colX + colWidths[1], currentY + 8);
      
      colX += colWidths[1];
      doc.text('Tipo', colX + colWidths[2]/2, currentY + 5.5, { align: 'center' });
      doc.line(colX + colWidths[2], currentY, colX + colWidths[2], currentY + 8);
      
      colX += colWidths[2];
      doc.text('Hora', colX + colWidths[3]/2, currentY + 5.5, { align: 'center' });
      doc.line(colX + colWidths[3], currentY, colX + colWidths[3], currentY + 8);
      
      colX += colWidths[3];
      doc.text('Actividad desarrollada', colX + colWidths[4]/2, currentY + 5.5, { align: 'center' });

      currentY += 8;
      
      // Filas de datos
      doc.setTextColor(0, 0, 0);
      doc.setFontSize(7);
      doc.setFont(undefined, 'normal');
      
      const baseRowHeight = 8;
      const lineHeight = 3; // Altura de cada línea de texto

      this.actividades.forEach((actividad, index) => {
        // Obtener la descripción completa
        const activDesc = actividad.descripcion || actividad.categoria_actividad || 'Actividad de ' + (actividad.tipo_actividad || 'campo');
        
        // Calcular cuántas líneas necesita la descripción
        const maxTextWidth = colWidths[4] - 4; // Ancho disponible para texto con margen
        const textLines = doc.splitTextToSize(activDesc, maxTextWidth);
        const numLines = textLines.length;
        
        // Calcular altura de fila basada en el número de líneas (mínimo 8, máximo según contenido)
        const rowHeight = Math.max(baseRowHeight, numLines * lineHeight + 3);
        
        // Verificar si necesitamos nueva página
        if (currentY > pageHeight - 50) {
          doc.addPage();
          currentY = 20;
          
          // Re-dibujar header de tabla en nueva página
          doc.setDrawColor(0, 0, 0);
          doc.setLineWidth(0.3);
          doc.setFillColor(255, 255, 255);
          doc.rect(tableX, currentY, tableWidth, 8, 'FD');
          
          doc.setTextColor(0, 0, 0);
          doc.setFontSize(8);
          doc.setFont(undefined, 'bold');
          
          let headerX = tableX + 2;
          doc.text('No.', headerX + colWidths[0]/2, currentY + 5.5, { align: 'center' });
          doc.line(headerX + colWidths[0], currentY, headerX + colWidths[0], currentY + 8);
          
          headerX += colWidths[0];
          doc.text('Fecha', headerX + colWidths[1]/2, currentY + 5.5, { align: 'center' });
          doc.line(headerX + colWidths[1], currentY, headerX + colWidths[1], currentY + 8);
          
          headerX += colWidths[1];
          doc.text('Tipo', headerX + colWidths[2]/2, currentY + 5.5, { align: 'center' });
          doc.line(headerX + colWidths[2], currentY, headerX + colWidths[2], currentY + 8);
          
          headerX += colWidths[2];
          doc.text('Hora', headerX + colWidths[3]/2, currentY + 5.5, { align: 'center' });
          doc.line(headerX + colWidths[3], currentY, headerX + colWidths[3], currentY + 8);
          
          headerX += colWidths[3];
          doc.text('Actividad desarrollada', headerX + colWidths[4]/2, currentY + 5.5, { align: 'center' });
          
          currentY += 8;
          doc.setTextColor(0, 0, 0);
          doc.setFontSize(7);
          doc.setFont(undefined, 'normal');
        }

        // Bordes de la fila
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.3);
        doc.rect(tableX, currentY, tableWidth, rowHeight, 'S');

        const fecha = this.formatearFecha(actividad.fecha_hora);
        const hora = this.formatearHora(actividad.fecha_hora);
        const tipo = this.capitalizar(actividad.tipo_actividad || 'Campo');

        colX = tableX + 2;
        
        // Posición vertical centrada para celdas de una línea
        const textYCenter = currentY + (rowHeight / 2) + 1.5;
        
        // No.
        doc.text(String(index + 1), colX + colWidths[0]/2, textYCenter, { align: 'center' });
        doc.line(colX + colWidths[0], currentY, colX + colWidths[0], currentY + rowHeight);
        
        // Fecha
        colX += colWidths[0];
        doc.text(fecha, colX + 2, textYCenter);
        doc.line(colX + colWidths[1], currentY, colX + colWidths[1], currentY + rowHeight);
        
        // Tipo (Campo/Gabinete)
        colX += colWidths[1];
        doc.text(tipo, colX + colWidths[2]/2, textYCenter, { align: 'center' });
        doc.line(colX + colWidths[2], currentY, colX + colWidths[2], currentY + rowHeight);
        
        // Hora de registro de la actividad
        colX += colWidths[2];
        doc.text(hora, colX + colWidths[3]/2, textYCenter, { align: 'center' });
        doc.line(colX + colWidths[3], currentY, colX + colWidths[3], currentY + rowHeight);
        
        // Actividad - Descripción completa con múltiples líneas
        colX += colWidths[3];
        // Dibujar cada línea de texto
        textLines.forEach((line, lineIndex) => {
          doc.text(line, colX + 2, currentY + 4 + (lineIndex * lineHeight));
        });

        currentY += rowHeight;
      });

      currentY += 15;

      // ========== SECCIÓN DE FIRMAS (Formato oficial) ==========
      if (this.$refs.firmaComponent?.hayFirma) {
        // Verificar si necesitamos nueva página para las firmas
        if (currentY > pageHeight - 70) {
          doc.addPage();
          currentY = 30;
        }

        // Configuración de las dos columnas de firma
        const firmaWidth = 70;
        const firmaHeight = 30;
        const espacioEntreFiremas = 20;
        const firmaUsuarioX = margin + 5;
        const firmaResponsableX = pageWidth - margin - firmaWidth - 5;
        
        const firmaY = currentY;
        
        // ========== ETIQUETAS "Elaboró" y "Aprobó" ==========
        doc.setFillColor(255, 218, 185); // Color durazno/naranja claro
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.3);
        
        // Etiqueta "Elaboró"
        doc.rect(firmaUsuarioX, firmaY - 8, firmaWidth, 7, 'FD');
        doc.setTextColor(0, 0, 0);
        doc.setFontSize(9);
        doc.setFont(undefined, 'bold');
        doc.text('Elaboró', firmaUsuarioX + firmaWidth / 2, firmaY - 3.5, { align: 'center' });
        
        // Etiqueta "Autorizó" - restablecer color de fondo
        doc.setFillColor(255, 218, 185); // Color durazno/naranja claro
        doc.rect(firmaResponsableX, firmaY - 8, firmaWidth, 7, 'FD');
        doc.text('Autorizó', firmaResponsableX + firmaWidth / 2, firmaY - 3.5, { align: 'center' });
        
        // ========== FIRMA DEL PRESTADOR DE SERVICIOS (Izquierda) ==========
        // Imagen de firma del usuario (sin rectángulo contenedor)
        const firmaBase64 = this.$refs.firmaComponent.obtenerFirmaBase64();
        doc.addImage(firmaBase64, 'PNG', firmaUsuarioX, firmaY, firmaWidth, firmaHeight);
        
        // Línea de firma usuario
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.5);
        doc.line(firmaUsuarioX, firmaY + firmaHeight + 5, firmaUsuarioX + firmaWidth, firmaY + firmaHeight + 5);
        
        // Cargo del usuario (primero)
        doc.setTextColor(0, 0, 0);
        doc.setFontSize(8);
        doc.setFont(undefined, 'normal');
        const cargoUsuario = this.usuarioInfo.cargo || 'Facilitador Comunitario';
        doc.text(cargoUsuario, firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' });
        
        // Nombre del usuario (después, en negrita)
        doc.setFontSize(8);
        doc.setFont(undefined, 'bold');
        const nombreUsuario = this.usuarioInfo.nombre || 'Sin nombre';
        doc.text(nombreUsuario, firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 17, { align: 'center' });
        
        // ========== FIRMA DEL RESPONSABLE (Derecha) ==========
        // Sin imagen, solo espacio vacío para firma manual
        
        // Línea de firma responsable
        doc.setLineWidth(0.5);
        doc.line(firmaResponsableX, firmaY + firmaHeight + 5, firmaResponsableX + firmaWidth, firmaY + firmaHeight + 5);
        
        // Cargo del responsable (primero, puede ser en dos líneas)
        doc.setFontSize(7.5);
        doc.setFont(undefined, 'normal');
        doc.text('Encargada de Despacho de la Coordinación', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' });
        doc.text('Territorial ' + (this.usuarioInfo.territorio || ''), firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 16, { align: 'center' });
        
        // Nombre del supervisor/responsable (después, en negrita)
        doc.setFontSize(8);
        doc.setFont(undefined, 'bold');
        const nombreSupervisor = this.usuarioInfo.supervisor || 'Sin asignar';
        doc.text(nombreSupervisor, firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 22, { align: 'center' });
        
        currentY = firmaY + firmaHeight + 30;
      }

      // ========== SEGUNDA PÁGINA: EVIDENCIAS FOTOGRÁFICAS ==========
      try {
        console.log('🖼️ Iniciando generación de página de evidencias fotográficas...');
        
        // Filtrar actividades del mes seleccionado con fotos
        const inicioPeriodo = new Date(this.anioSeleccionado, this.mesSeleccionado, 1);
        const finPeriodo = new Date(this.anioSeleccionado, this.mesSeleccionado + 1, 0);
        
        const actividadesConFoto = this.actividades.filter(actividad => {
          if (!actividad.foto_url) return false;
          const fechaActividad = new Date(actividad.fecha_hora);
          return fechaActividad >= inicioPeriodo && fechaActividad <= finPeriodo;
        });

        console.log(`📸 Actividades con foto encontradas en ${this.mesActual}: ${actividadesConFoto.length}`);
        console.log('🔍 Actividades con foto:', actividadesConFoto.map(a => ({ 
          foto_url: a.foto_url, 
          fecha: a.fecha_hora,
          tipo: a.tipo_actividad 
        })));
        
        console.log('📊 DEBUG - Total actividades cargadas:', this.actividades.length);
        console.log('📊 DEBUG - Actividades con foto_url:', this.actividades.filter(a => a.foto_url).length);

        // SIEMPRE crear la página de evidencias fotográficas
        doc.addPage();
        currentY = 10;

        // ========== ENCABEZADO DE LA PÁGINA DE EVIDENCIAS ==========
        // Cargar imagen de logos (reutilizar la misma imagen cargada)
        if (superiorImageBase64 && imgDimensions) {
          const realAspectRatio = imgDimensions.height / imgDimensions.width;
          const imgWidth = contentWidth * 0.95;
          const imgHeight = imgWidth * realAspectRatio;
          const imgX = margin + (contentWidth - imgWidth) / 2;
          
          doc.addImage(superiorImageBase64, 'PNG', imgX, currentY, imgWidth, imgHeight);
          currentY += imgHeight + 5;
        }
        
        // Título de la sección
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.5);
        doc.rect(margin, currentY, contentWidth, 12);
          
        doc.setFontSize(11);
        doc.setFont(undefined, 'bold');
        doc.setTextColor(0, 0, 0);
        doc.text('EVIDENCIAS FOTOGRÁFICAS DE ACTIVIDADES', pageWidth / 2, currentY + 5, { align: 'center' });
        doc.setFontSize(9);
        doc.setFont(undefined, 'normal');
        doc.text(`${this.mesActual} ${this.anioSeleccionado}`, pageWidth / 2, currentY + 10, { align: 'center' });
        
        currentY += 15;

        // ========== DATOS DEL USUARIO ==========
        doc.setFillColor(240, 240, 240);
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.3);
        doc.rect(margin, currentY, contentWidth, 18, 'FD');
        
        doc.setFontSize(8);
        doc.setTextColor(0, 0, 0);
        
        // Nombre
        doc.setFont(undefined, 'bold');
        doc.text('Nombre:', margin + 3, currentY + 5);
        doc.setFont(undefined, 'normal');
        doc.text(this.usuarioInfo.nombre || 'Sin nombre', margin + 20, currentY + 5);
        
        // CURP
        doc.setFont(undefined, 'bold');
        doc.text('CURP:', margin + 95, currentY + 5);
        doc.setFont(undefined, 'normal');
        doc.text(this.usuarioInfo.curp || 'No registrado', margin + 107, currentY + 5);
        
        // Cargo
        doc.setFont(undefined, 'bold');
        doc.text('Cargo:', margin + 3, currentY + 11);
        doc.setFont(undefined, 'normal');
        doc.text(this.usuarioInfo.cargo || 'Facilitador Comunitario', margin + 17, currentY + 11);
        
        // Territorio
        doc.setFont(undefined, 'bold');
        doc.text('Territorio:', margin + 95, currentY + 11);
        doc.setFont(undefined, 'normal');
        doc.text(this.usuarioInfo.territorio || 'No asignado', margin + 115, currentY + 11);
        
        // Período
        doc.setFont(undefined, 'bold');
        doc.text('Período:', margin + 3, currentY + 17);
        doc.setFont(undefined, 'normal');
        doc.text(`${this.mesActual} ${this.anioSeleccionado}`, margin + 18, currentY + 17);
        
        currentY += 22;

        // ========== VERIFICAR SI HAY IMÁGENES ==========
        if (actividadesConFoto.length === 0) {
          // Se mostrará mensaje después de las firmas
        } else {
          // ========== SELECCIÓN DE 6 IMÁGENES: PRIMERO CAMPO, LUEGO GABINETE ==========
          // Separar por tipo
          const actividadesCampo = actividadesConFoto
            .filter(a => (a.tipo_actividad || 'campo').toLowerCase() === 'campo')
            .sort((a, b) => new Date(b.fecha_hora) - new Date(a.fecha_hora)); // Más recientes primero
          
          const actividadesGabinete = actividadesConFoto
            .filter(a => (a.tipo_actividad || '').toLowerCase() === 'gabinete')
            .sort((a, b) => new Date(b.fecha_hora) - new Date(a.fecha_hora)); // Más recientes primero
          
          // Seleccionar imágenes: primero todas las de campo, luego todas las de gabinete
          let imagenesSeleccionadas = [];
          const maxImagenes = 6;
          
          // Calcular cuántas de cada tipo (máximo 3 de campo y 3 de gabinete si hay de ambos)
          let maxCampo = Math.min(actividadesCampo.length, 3);
          let maxGabinete = Math.min(actividadesGabinete.length, 3);
          
          // Si solo hay de un tipo, usar hasta 6 de ese tipo
          if (actividadesCampo.length === 0) {
            maxGabinete = Math.min(actividadesGabinete.length, maxImagenes);
          } else if (actividadesGabinete.length === 0) {
            maxCampo = Math.min(actividadesCampo.length, maxImagenes);
          } else {
            // Hay de ambos - distribuir el espacio restante
            const espacioRestanteCampo = maxImagenes - maxGabinete;
            const espacioRestanteGabinete = maxImagenes - maxCampo;
            maxCampo = Math.min(actividadesCampo.length, espacioRestanteCampo);
            maxGabinete = Math.min(actividadesGabinete.length, maxImagenes - maxCampo);
          }
          
          // Agregar primero las de campo
          for (let i = 0; i < maxCampo; i++) {
            imagenesSeleccionadas.push(actividadesCampo[i]);
          }
          
          // Luego las de gabinete
          for (let i = 0; i < maxGabinete; i++) {
            imagenesSeleccionadas.push(actividadesGabinete[i]);
          }
          
          console.log(`📷 Seleccionadas ${imagenesSeleccionadas.length} imágenes variadas (Campo: ${actividadesCampo.length}, Gabinete: ${actividadesGabinete.length})`);
          
          // ========== GRID DE IMÁGENES ==========
          const imgGridWidth = 55; // Ancho de cada imagen
          const imgGridHeight = 45; // Alto de cada imagen
          const imgsPerRow = 3;
          const imgSpacing = 5;
          const labelHeight = 14; // Aumentado para mejor visualización
          
          // Cargar imágenes y dibujarlas
          let imgIndex = 0;
          const totalImagenes = imagenesSeleccionadas.length;
          
          console.log(`📷 Procesando ${totalImagenes} imágenes...`);
          
          for (let i = 0; i < totalImagenes; i++) {
            const actividad = imagenesSeleccionadas[i];
            
            // Verificar si necesitamos nueva página
            if (currentY + imgGridHeight + labelHeight + 15 > pageHeight - 40) {
              doc.addPage();
              currentY = 20;
              
              // Título continuación
              doc.setFontSize(9);
              doc.setFont(undefined, 'bold');
              doc.setTextColor(0, 0, 0);
              doc.text('EVIDENCIAS FOTOGRÁFICAS (Continuación)', pageWidth / 2, currentY, { align: 'center' });
              currentY += 10;
            }            const col = imgIndex % imgsPerRow;
            const imgX = margin + (col * (imgGridWidth + imgSpacing));
            
            // Si es primera columna de una fila nueva, ajustar Y
            if (col === 0 && imgIndex > 0) {
              currentY += imgGridHeight + labelHeight + 10;
            }
            
            try {
              // La URL ya viene completa del servidor
              const fotoUrl = actividad.foto_url;
              
              console.log(`📷 [${i + 1}/${totalImagenes}] Cargando imagen: ${fotoUrl}`);
              
              // Cargar imagen como base64 con timeout
              const imgResult = await this.cargarImagenComoBase64(fotoUrl);
              const imgData = imgResult.data;
              
              if (imgData) {
                console.log(`✅ [${i + 1}/${totalImagenes}] Imagen cargada exitosamente`);
                
                // Borde de la imagen
                doc.setDrawColor(0, 0, 0);
                doc.setLineWidth(0.3);
                doc.rect(imgX, currentY, imgGridWidth, imgGridHeight);
                
                // Imagen
                doc.addImage(imgData, 'JPEG', imgX + 1, currentY + 1, imgGridWidth - 2, imgGridHeight - 2);
                
                // Etiqueta debajo con información
                const tipoAct = actividad.tipo_actividad || 'campo';
                const tipoTexto = tipoAct.toLowerCase() === 'campo' ? 'CAMPO' : 'GABINETE';
                
                // Formato compacto solo números: DD/MM/AA HH:MM
                const fechaObj = new Date(actividad.fecha_hora);
                const dia = String(fechaObj.getDate()).padStart(2, '0');
                const mes = String(fechaObj.getMonth() + 1).padStart(2, '0');
                const anio = String(fechaObj.getFullYear()).slice(-2);
                const hora = String(fechaObj.getHours()).padStart(2, '0');
                const min = String(fechaObj.getMinutes()).padStart(2, '0');
                const fechaCompacta = `${dia}/${mes}/${anio} ${hora}:${min}`;
                
                // Fondo de etiqueta según tipo
                if (tipoAct.toLowerCase() === 'campo') {
                  doc.setFillColor(34, 197, 94); // Verde para Campo
                } else {
                  doc.setFillColor(147, 51, 234); // Morado para Gabinete
                }
                doc.rect(imgX, currentY + imgGridHeight, imgGridWidth, labelHeight, 'F');
                
                // Borde de la etiqueta
                doc.setDrawColor(0, 0, 0);
                doc.setLineWidth(0.2);
                doc.rect(imgX, currentY + imgGridHeight, imgGridWidth, labelHeight, 'S');
                
                // Tipo de actividad - Grande y en negrita (CAMPO o GABINETE)
                doc.setTextColor(255, 255, 255);
                doc.setFontSize(10);
                doc.setFont(undefined, 'bold');
                doc.text(tipoTexto, imgX + imgGridWidth / 2, currentY + imgGridHeight + 6, { align: 'center' });
                
                // Fecha compacta - Pequeña debajo
                doc.setFont(undefined, 'normal');
                doc.setFontSize(6);
                doc.text(fechaCompacta, imgX + imgGridWidth / 2, currentY + imgGridHeight + 11, { align: 'center' });
              } else {
                throw new Error('No se pudo obtener datos de la imagen');
              }
            } catch (imgError) {
              console.error(`❌ [${i + 1}/${totalImagenes}] Error cargando imagen:`, imgError);
              
              // Dibujar placeholder si falla la carga
              doc.setFillColor(240, 240, 240);
              doc.rect(imgX, currentY, imgGridWidth, imgGridHeight, 'F');
              doc.setDrawColor(200, 200, 200);
              doc.rect(imgX, currentY, imgGridWidth, imgGridHeight, 'S');
              
              doc.setTextColor(150, 150, 150);
              doc.setFontSize(8);
              doc.text('Imagen no', imgX + imgGridWidth / 2, currentY + imgGridHeight / 2 - 3, { align: 'center' });
              doc.text('disponible', imgX + imgGridWidth / 2, currentY + imgGridHeight / 2 + 3, { align: 'center' });
              
              // Etiqueta de información aunque falle la imagen
              const tipoAct = actividad.tipo_actividad || 'campo';
              const tipoTexto = tipoAct.toLowerCase() === 'campo' ? 'CAMPO' : 'GABINETE';
              
              // Formato compacto solo números: DD/MM/AA HH:MM
              const fechaObj = new Date(actividad.fecha_hora);
              const dia = String(fechaObj.getDate()).padStart(2, '0');
              const mes = String(fechaObj.getMonth() + 1).padStart(2, '0');
              const anio = String(fechaObj.getFullYear()).slice(-2);
              const hora = String(fechaObj.getHours()).padStart(2, '0');
              const min = String(fechaObj.getMinutes()).padStart(2, '0');
              const fechaCompacta = `${dia}/${mes}/${anio} ${hora}:${min}`;
              
              if (tipoAct.toLowerCase() === 'campo') {
                doc.setFillColor(34, 197, 94);
              } else {
                doc.setFillColor(147, 51, 234);
              }
              doc.rect(imgX, currentY + imgGridHeight, imgGridWidth, labelHeight, 'F');
              
              // Borde de la etiqueta
              doc.setDrawColor(0, 0, 0);
              doc.setLineWidth(0.2);
              doc.rect(imgX, currentY + imgGridHeight, imgGridWidth, labelHeight, 'S');
              
              doc.setTextColor(255, 255, 255);
              doc.setFontSize(10);
              doc.setFont(undefined, 'bold');
              doc.text(tipoTexto, imgX + imgGridWidth / 2, currentY + imgGridHeight + 6, { align: 'center' });
              doc.setFont(undefined, 'normal');
              doc.setFontSize(6);
              doc.text(fechaCompacta, imgX + imgGridWidth / 2, currentY + imgGridHeight + 11, { align: 'center' });
            }
            
            imgIndex++;
          }
          
          console.log(`✅ Procesadas ${imgIndex} imágenes en total`);
          
          // Ajustar Y después de la última fila
          currentY += imgGridHeight + labelHeight + 15;

          // ========== FIRMA EN PÁGINA DE EVIDENCIAS ==========
          if (this.$refs.firmaComponent?.hayFirma) {
            // Verificar si hay espacio para firmas
            if (currentY > pageHeight - 70) {
              doc.addPage();
              currentY = 30;
            }

            const firmaWidth = 70;
            const firmaHeight = 30;
            const firmaUsuarioX = margin + 5;
            const firmaResponsableX = pageWidth - margin - firmaWidth - 5;
            const firmaY = currentY;
            
            // Etiquetas
            doc.setFillColor(255, 218, 185);
            doc.setDrawColor(0, 0, 0);
            doc.setLineWidth(0.3);
            
            doc.rect(firmaUsuarioX, firmaY - 8, firmaWidth, 7, 'FD');
            doc.setTextColor(0, 0, 0);
            doc.setFontSize(9);
            doc.setFont(undefined, 'bold');
            doc.text('Elaboró', firmaUsuarioX + firmaWidth / 2, firmaY - 3.5, { align: 'center' });
            
            doc.setFillColor(255, 218, 185);
            doc.rect(firmaResponsableX, firmaY - 8, firmaWidth, 7, 'FD');
            doc.text('Autorizó', firmaResponsableX + firmaWidth / 2, firmaY - 3.5, { align: 'center' });
            
            // Firma del usuario
            const firmaBase64 = this.$refs.firmaComponent.obtenerFirmaBase64();
            doc.addImage(firmaBase64, 'PNG', firmaUsuarioX, firmaY, firmaWidth, firmaHeight);
            
            // Líneas de firma
            doc.setLineWidth(0.5);
            doc.line(firmaUsuarioX, firmaY + firmaHeight + 5, firmaUsuarioX + firmaWidth, firmaY + firmaHeight + 5);
            doc.line(firmaResponsableX, firmaY + firmaHeight + 5, firmaResponsableX + firmaWidth, firmaY + firmaHeight + 5);
            
            // Información del usuario
            doc.setTextColor(0, 0, 0);
            doc.setFontSize(8);
            doc.setFont(undefined, 'normal');
            const cargoUsuario = this.usuarioInfo.cargo || 'Facilitador Comunitario';
            doc.text(cargoUsuario, firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' });
            doc.setFont(undefined, 'bold');
            doc.text(this.usuarioInfo.nombre || 'Sin nombre', firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 17, { align: 'center' });
            
            // Información del responsable
            doc.setFontSize(7.5);
            doc.setFont(undefined, 'normal');
            doc.text('Encargada de Despacho de la Coordinación', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' });
            doc.text('Territorial ' + (this.usuarioInfo.territorio || ''), firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 16, { align: 'center' });
            doc.setFontSize(8);
            doc.setFont(undefined, 'bold');
            doc.text(this.usuarioInfo.supervisor || 'Sin asignar', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 22, { align: 'center' });
          }
          
          console.log('✅ Página de evidencias fotográficas completada con imágenes');
        } // Fin del else (cuando hay fotos)
        
        // ========== FIRMA EN PÁGINA DE EVIDENCIAS (para ambos casos) ==========
        if (actividadesConFoto.length === 0 && this.$refs.firmaComponent?.hayFirma) {
          // Agregar firma cuando no hay fotos
          if (currentY > pageHeight - 70) {
            doc.addPage();
            currentY = 30;
          }

          const firmaWidth = 70;
          const firmaHeight = 30;
          const firmaUsuarioX = margin + 5;
          const firmaResponsableX = pageWidth - margin - firmaWidth - 5;
          const firmaY = currentY;
          
          // Etiquetas
          doc.setFillColor(255, 218, 185);
          doc.setDrawColor(0, 0, 0);
          doc.setLineWidth(0.3);
          
          doc.rect(firmaUsuarioX, firmaY - 8, firmaWidth, 7, 'FD');
          doc.setTextColor(0, 0, 0);
          doc.setFontSize(9);
          doc.setFont(undefined, 'bold');
          doc.text('Elaboró', firmaUsuarioX + firmaWidth / 2, firmaY - 3.5, { align: 'center' });
          
          doc.setFillColor(255, 218, 185);
          doc.rect(firmaResponsableX, firmaY - 8, firmaWidth, 7, 'FD');
          doc.text('Autorizó', firmaResponsableX + firmaWidth / 2, firmaY - 3.5, { align: 'center' });
          
          // Firma del usuario
          const firmaBase64 = this.$refs.firmaComponent.obtenerFirmaBase64();
          doc.addImage(firmaBase64, 'PNG', firmaUsuarioX, firmaY, firmaWidth, firmaHeight);
          
          // Líneas de firma
          doc.setLineWidth(0.5);
          doc.line(firmaUsuarioX, firmaY + firmaHeight + 5, firmaUsuarioX + firmaWidth, firmaY + firmaHeight + 5);
          doc.line(firmaResponsableX, firmaY + firmaHeight + 5, firmaResponsableX + firmaWidth, firmaY + firmaHeight + 5);
          
          // Información del usuario
          doc.setTextColor(0, 0, 0);
          doc.setFontSize(8);
          doc.setFont(undefined, 'normal');
          const cargoUsuario = this.usuarioInfo.cargo || 'Facilitador Comunitario';
          doc.text(cargoUsuario, firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' });
          doc.setFont(undefined, 'bold');
          doc.text(this.usuarioInfo.nombre || 'Sin nombre', firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 17, { align: 'center' });
          
          // Información del responsable
          doc.setFontSize(7.5);
          doc.setFont(undefined, 'normal');
          doc.text('Encargada de Despacho de la Coordinación', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' });
          doc.text('Territorial ' + (this.usuarioInfo.territorio || ''), firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 16, { align: 'center' });
          doc.setFontSize(8);
          doc.setFont(undefined, 'bold');
          doc.text(this.usuarioInfo.supervisor || 'Sin asignar', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 22, { align: 'center' });
        }
        
        console.log('✅ Página de evidencias fotográficas completada');
        
      } catch (evidenciasError) {
        console.error('❌ Error CRÍTICO generando página de evidencias:', evidenciasError);
        console.error('Stack trace:', evidenciasError.stack);
        // Continuar con el resto del PDF aunque falle la sección de evidencias
        alert('Advertencia: Hubo un error al generar la página de evidencias fotográficas. Se generará el PDF sin esta sección.');
      }

      // ========== PIE DE PÁGINA CON INFORMACIÓN DE CONTACTO ==========
      const totalPages = doc.internal.getNumberOfPages();
      
      for (let i = 1; i <= totalPages; i++) {
        doc.setPage(i);
        
        // Color guinda: RGB(128, 0, 32) aproximadamente
        doc.setTextColor(128, 0, 32);
        doc.setFontSize(7);
        doc.setFont(undefined, 'normal');
        
        const footerText = 'Paseo de la Reforma # 116, Piso 16, Col. Juárez, Alc. Cuauhtémoc, CDMX C.P. 06600 Tel.: (55) 5328 5000 www.gob.mx/bienestar';
        doc.text(footerText, pageWidth / 2, pageHeight - 10, { align: 'center' });
      }

      // Obtener el PDF como base64 PRIMERO (antes de intentar descargar)
      console.log('📦 Obteniendo PDF como base64...');
      const pdfBase64 = doc.output('datauristring');
      console.log('📦 Base64 obtenido, longitud:', pdfBase64 ? pdfBase64.length : 'NULL');
      
      // Guardar referencia al documento para descarga posterior
      this._pdfDocumentoGenerado = doc;
      this._pdfNombreArchivo = `Reporte_${this.mesActual}_${this.anioSeleccionado}.pdf`;
      
      console.log('✅ PDF generado exitosamente (descarga pendiente)');
      
      // Retornar el base64 para guardarlo en BD
      return pdfBase64;
      
    } catch (error) {
      console.error('❌ Error crítico generando PDF:', error);
      alert('Error al generar el PDF. Por favor, intenta de nuevo.');
      throw error;
    }
  },

    /**
     * Método para descargar el PDF de forma segura en todos los dispositivos (incluyendo móviles)
     * Compatible con iOS Safari, Android Chrome y navegadores de escritorio
     */
    async descargarPDFSeguro(pdfDoc, nombreArchivo) {
      try {
        console.log('💾 Iniciando descarga segura del PDF...');
        console.log('📱 Detectando plataforma...');
        
        // Detectar si es móvil
        const userAgent = navigator.userAgent || navigator.vendor || window.opera;
        const isIOS = /iPad|iPhone|iPod/.test(userAgent) && !window.MSStream;
        const isAndroid = /android/i.test(userAgent);
        const isMobile = isIOS || isAndroid || /mobile/i.test(userAgent);
        
        console.log(`📱 Plataforma: iOS=${isIOS}, Android=${isAndroid}, Mobile=${isMobile}`);
        
        if (isMobile) {
          // En móviles, usar Blob URL con un link temporal
          console.log('📱 Usando método de descarga para móviles...');
          
          // Obtener el PDF como Blob
          const pdfBlob = pdfDoc.output('blob');
          
          // Crear URL del Blob
          const blobUrl = URL.createObjectURL(pdfBlob);
          
          // Crear link temporal
          const link = document.createElement('a');
          link.href = blobUrl;
          link.download = nombreArchivo;
          link.style.display = 'none';
          
          // En iOS Safari, abrir en nueva ventana puede ser más confiable
          if (isIOS) {
            console.log('🍎 iOS detectado - abriendo PDF en nueva ventana...');
            // En iOS, intentar primero abrir en nueva ventana
            const newWindow = window.open(blobUrl, '_blank');
            if (!newWindow) {
              // Si el popup fue bloqueado, intentar con click en link
              console.log('🍎 Popup bloqueado, usando link click...');
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);
            }
          } else {
            // En Android y otros móviles
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          }
          
          // Limpiar URL del Blob después de un delay
          setTimeout(() => {
            URL.revokeObjectURL(blobUrl);
            console.log('🧹 Blob URL limpiado');
          }, 5000);
          
        } else {
          // En escritorio, usar el método estándar de jsPDF
          console.log('💻 Usando método de descarga estándar para escritorio...');
          pdfDoc.save(nombreArchivo);
        }
        
        console.log('✅ PDF descargado exitosamente');
        return true;
        
      } catch (error) {
        console.error('⚠️ Error en descarga de PDF:', error);
        // Intentar método alternativo
        try {
          console.log('🔄 Intentando método de descarga alternativo...');
          const pdfBlob = pdfDoc.output('blob');
          const blobUrl = URL.createObjectURL(pdfBlob);
          window.open(blobUrl, '_blank');
          setTimeout(() => URL.revokeObjectURL(blobUrl), 5000);
          console.log('✅ PDF abierto en nueva ventana');
          return true;
        } catch (altError) {
          console.error('❌ Error en método alternativo:', altError);
          return false;
        }
      }
    },

    // Método auxiliar para cargar imagen como Base64
    // Mejorado para dispositivos móviles (iOS/Android) usando proxy del backend
    async cargarImagenComoBase64(url) {
      console.log(`🔄 Iniciando carga de imagen: ${url}`);
      
      // Obtener URL base del API
      const currentApiUrl = apiService.getCurrentApiUrl();
      
      // Verificar si es una URL de foto del servidor (para usar el proxy)
      const esFotoDelServidor = url && (
        url.includes('/fotos/') || 
        url.includes(currentApiUrl)
      );
      
      if (esFotoDelServidor) {
        // MÉTODO 1: Usar proxy del backend (mejor para dispositivos móviles)
        try {
          // Extraer solo el nombre del archivo de la URL completa
          // Ejemplo: https://api.example.com/fotos/archivo.jpg -> archivo.jpg
          let nombreArchivo = url;
          
          // Si es una URL completa, extraer la parte después de /fotos/
          if (url.includes('/fotos/')) {
            nombreArchivo = url.split('/fotos/').pop();
          }
          
          console.log(`📥 Usando proxy para imagen: ${nombreArchivo}`);
          
          const proxyUrl = `${currentApiUrl}/fotos-base64/${nombreArchivo}`;
          const response = await api.get(proxyUrl, { timeout: 30000 });
          
          if (response.success && response.data) {
            console.log(`✅ Imagen cargada vía proxy (${(response.size_bytes / 1024).toFixed(2)} KB)`);
            
            // Obtener dimensiones de la imagen
            return new Promise((resolve, reject) => {
              const img = new Image();
              img.onload = () => {
                resolve({
                  data: response.data,
                  dimensions: {
                    width: img.width,
                    height: img.height
                  }
                });
              };
              img.onerror = () => {
                // Devolver sin dimensiones si falla
                resolve({
                  data: response.data,
                  dimensions: { width: 800, height: 600 }
                });
              };
              img.src = response.data;
            });
          }
        } catch (proxyError) {
          console.warn('⚠️ Error usando proxy, intentando métodos alternativos:', proxyError.message);
        }
      }
      
      // MÉTODO 2: Usar fetch con blob (más compatible que Image con CORS)
      try {
        console.log('📥 Intentando cargar imagen con fetch/blob...');
        const response = await fetch(url, {
          mode: 'cors',
          credentials: 'omit',
          headers: {
            'Accept': 'image/*'
          }
        });
        
        if (response.ok) {
          const blob = await response.blob();
          
          return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => {
              const base64data = reader.result;
              
              // Obtener dimensiones
              const img = new Image();
              img.onload = () => {
                console.log(`✅ Imagen cargada con fetch/blob (${(blob.size / 1024).toFixed(2)} KB)`);
                resolve({
                  data: base64data,
                  dimensions: {
                    width: img.width,
                    height: img.height
                  }
                });
              };
              img.onerror = () => {
                resolve({
                  data: base64data,
                  dimensions: { width: 800, height: 600 }
                });
              };
              img.src = base64data;
            };
            reader.onerror = reject;
            reader.readAsDataURL(blob);
          });
        }
      } catch (fetchError) {
        console.warn('⚠️ Error con fetch/blob, intentando método Image:', fetchError.message);
      }
      
      // MÉTODO 3: Método tradicional con Image (fallback)
      return new Promise((resolve, reject) => {
        const img = new Image();
        
        // Configurar CORS
        img.crossOrigin = 'anonymous';
        
        // Timeout extendido para conexiones móviles lentas
        const timeoutId = setTimeout(() => {
          console.warn(`⏱️ Timeout cargando imagen: ${url}`);
          reject(new Error('Timeout al cargar imagen'));
        }, 30000); // 30 segundos para móviles
        
        img.onload = () => {
          clearTimeout(timeoutId);
          
          try {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            // Guardar dimensiones originales
            const originalWidth = img.width;
            const originalHeight = img.height;
            
            // Redimensionar si es muy grande
            const maxSize = 800;
            let width = img.width;
            let height = img.height;
            
            console.log(`📐 Dimensiones originales: ${width}x${height}`);
            
            if (width > maxSize || height > maxSize) {
              if (width > height) {
                height = (height / width) * maxSize;
                width = maxSize;
              } else {
                width = (width / height) * maxSize;
                height = maxSize;
              }
              console.log(`📐 Redimensionado a: ${width}x${height}`);
            }
            
            canvas.width = width;
            canvas.height = height;
            ctx.drawImage(img, 0, 0, width, height);
            
            const dataUrl = canvas.toDataURL('image/png', 0.95);
            console.log(`✅ Imagen convertida a base64 (${(dataUrl.length / 1024).toFixed(2)} KB)`);
            
            resolve({
              data: dataUrl,
              dimensions: {
                width: originalWidth,
                height: originalHeight
              }
            });
          } catch (error) {
            console.error('❌ Error al convertir imagen:', error);
            clearTimeout(timeoutId);
            reject(error);
          }
        };
        
        img.onerror = (error) => {
          clearTimeout(timeoutId);
          console.error(`❌ Error al cargar imagen desde: ${url}`, error);
          reject(new Error(`Error cargando imagen: ${url}`));
        };
        
        img.src = url;
      });
    },

    generarCSV() {
      const headers = ['Fecha', 'Hora', 'Tipo', 'Categoría', 'Descripción', 'Usuario', 'CURP', 'Cargo', 'Territorio', 'Correo', 'Supervisor'];
      
      const rows = this.actividades.map(actividad => [
        this.formatearFecha(actividad.fecha_hora),
        this.formatearHora(actividad.fecha_hora),
        this.capitalizar(actividad.tipo_actividad || '-'),
        actividad.categoria_actividad || '-',
        actividad.descripcion || '',
        this.usuarioInfo.nombre,
        this.usuarioInfo.curp || '',
        this.usuarioInfo.cargo || '',
        this.usuarioInfo.territorio || '',
        this.usuarioInfo.correo,
        this.usuarioInfo.supervisor || ''
      ]);

      const csv = [
        headers.join(','),
        ...rows.map(row => row.map(cell => `"${cell}"`).join(',')),
        '',
        '',
        '"NOTA: El reporte fotográfico solo está disponible para el mes en curso; al descargar información de meses anteriores, las fotografías no se mostrarán."'
      ].join('\n');

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);
      
      link.setAttribute('href', url);
      link.setAttribute('download', `Reporte_${this.mesActual}_${this.anioSeleccionado}.csv`);
      link.style.visibility = 'hidden';
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },

    async cargarHistorialReportes() {
      this.cargandoHistorial = true;
      this.errorHistorial = null;
      
      try {
        if (!this.usuarioInfo.id) {
          console.log('⚠️ No hay ID de usuario para cargar historial');
          console.log('📋 Usuario info actual:', JSON.stringify(this.usuarioInfo));
          this.errorHistorial = 'No se pudo identificar al usuario';
          return;
        }

        console.log(`🔍 Cargando historial para usuario ID: ${this.usuarioInfo.id}`);
        // Usar api del apiService que auto-detecta servidor correcto
        const response = await api.get(`/reportes/historial/${this.usuarioInfo.id}`);
        
        console.log('📦 Respuesta del servidor (raw):', JSON.stringify(response.data));
        
        if (response.data.success && response.data.reportes) {
          // Formatear fechas y asegurar que tiene_pdf se preserve
          this.reportesGenerados = response.data.reportes.map(reporte => {
            const reporteFormateado = {
              id: reporte.id,
              nombre: reporte.nombre,
              mes: reporte.mes,
              anio: reporte.anio,
              tipo: reporte.tipo,
              tiene_pdf: reporte.tiene_pdf === true, // Asegurar que sea booleano
              firmado_supervisor: reporte.firmado_supervisor === true, // Estado de firma
              fecha_firma_supervisor: reporte.fecha_firma_supervisor, // Fecha de firma
              nombre_supervisor: reporte.nombre_supervisor, // Nombre del supervisor
              fecha: reporte.fecha || null // Guardar fecha original sin formatear
            };
            console.log(`   📄 Reporte: ${reporteFormateado.nombre}, tiene_pdf: ${reporteFormateado.tiene_pdf}, firmado: ${reporteFormateado.firmado_supervisor}`);
            return reporteFormateado;
          });
          console.log(`✅ Historial de reportes cargado: ${this.reportesGenerados.length} reportes`);
          
          // Guardar en localStorage como backup
          localStorage.setItem('reportesGenerados', JSON.stringify(this.reportesGenerados));
        } else {
          console.log('⚠️ No se encontraron reportes en la respuesta');
          console.log('   Response success:', response.data.success);
          console.log('   Response reportes:', response.data.reportes);
          this.reportesGenerados = [];
        }
      } catch (error) {
        console.error('❌ Error cargando historial de reportes:', error);
        console.error('   Status:', error.response?.status);
        console.error('   Data:', error.response?.data);
        console.error('   Message:', error.message);
        
        this.errorHistorial = error.response?.data?.detail || error.message || 'Error al cargar historial';
        
        // Si hay error, intentar cargar desde localStorage como fallback
        const reportesGuardados = localStorage.getItem('reportesGenerados');
        if (reportesGuardados) {
          try {
            this.reportesGenerados = JSON.parse(reportesGuardados);
            console.log('📋 Reportes cargados desde localStorage:', this.reportesGenerados.length);
            this.errorHistorial = null; // Limpiar error si cargamos desde cache
          } catch (e) {
            console.error('❌ Error parseando localStorage:', e);
            this.reportesGenerados = [];
          }
        } else {
          this.reportesGenerados = [];
        }
      } finally {
        this.cargandoHistorial = false;
      }
    },

    async descargarReporteHistorial(reporte) {
      // Descargar un reporte previamente generado desde el historial
      // NUEVO FLUJO: Genera el PDF con las firmas disponibles (usuario + supervisor si existe)
      if (this.descargandoReporte) {
        console.log('⚠️ Ya se está descargando un reporte');
        return;
      }

      console.log(`📥 Descargando reporte del historial: ${reporte.nombre}`);
      this.descargandoReporte = reporte.id;

      try {
        // Obtener datos del reporte desde el servidor
        const response = await api.get(`/reportes/descargar/${reporte.id}`);
        
        if (!response.data.success) {
          throw new Error('No se pudo obtener el reporte');
        }
        
        const reporteData = response.data.reporte;
        
        // NUEVO FLUJO: Si hay datos_reporte, generar PDF desde los datos
        if (reporteData.datos_reporte) {
          console.log('📄 Generando PDF desde datos estructurados...');
          
          // Generar PDF con las firmas disponibles
          const pdfBase64 = await this.generarPDFDesdesDatos(
            reporteData.datos_reporte,
            reporteData.firma_usuario_base64,
            reporteData.firmado_supervisor ? reporteData.firma_supervisor_base64 : null,
            reporteData.nombre_supervisor
          );
          
          // Descargar el PDF
          await this.descargarPDFBase64(pdfBase64, reporte.nombre);
          
          console.log('✅ Reporte generado y descargado exitosamente');
          
          this.$notify?.({
            type: 'success',
            message: reporteData.firmado_supervisor 
              ? `${reporte.nombre} descargado (firmado por supervisor)` 
              : `${reporte.nombre} descargado (pendiente de autorización)`
          });
          
        } else if (reporteData.pdf_base64) {
          // COMPATIBILIDAD: Si hay PDF guardado (reportes antiguos)
          console.log('📄 Usando PDF guardado (compatibilidad)...');
          
          let base64Data = limpiarBase64(reporteData.pdf_base64);
          
          if (!base64Data) {
            throw new Error('El PDF tiene formato inválido');
          }
          
          // Si el reporte tiene firma del supervisor, agregarla al PDF
          if (reporteData.firmado_supervisor && reporteData.firma_supervisor_base64) {
            console.log('✍️ Agregando firma del supervisor al PDF...');
            base64Data = await this.agregarFirmaSupervisorPDF(base64Data, reporteData.firma_supervisor_base64);
          }
          
          await this.descargarPDFBase64(base64Data, reporte.nombre);
          
          this.$notify?.({
            type: 'success',
            message: `${reporte.nombre} descargado`
          });
        } else {
          throw new Error('El reporte no tiene datos disponibles para generar el PDF');
        }
        
      } catch (error) {
        console.error('❌ Error descargando reporte:', error);
        
        let mensaje = 'Error al descargar el reporte';
        if (error.response?.status === 404) {
          mensaje = 'El reporte no está disponible';
        }
        
        this.$notify?.({
          type: 'error',
          message: mensaje
        });
      } finally {
        this.descargandoReporte = null;
      }
    },
    
    /**
     * Descarga un PDF desde base64
     */
    async descargarPDFBase64(base64Data, nombreReporte) {
      const byteCharacters = atob(base64Data);
      const byteNumbers = new Array(byteCharacters.length);
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      const blob = new Blob([byteArray], { type: 'application/pdf' });
      
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${nombreReporte.replace(/\s+/g, '_')}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    },
    
    /**
     * Genera un PDF desde los datos estructurados del reporte
     * @param {Object} datos - Datos estructurados del reporte
     * @param {string} firmaUsuario - Firma del usuario en base64
     * @param {string} firmaSupervisor - Firma del supervisor en base64 (opcional)
     * @param {string} nombreSupervisor - Nombre del supervisor que firmó
     * @returns {string} - PDF en base64 (sin prefijo data:)
     */
    async generarPDFDesdesDatos(datos, firmaUsuario, firmaSupervisor, nombreSupervisor) {
      console.log('📄 Generando PDF desde datos estructurados...');
      console.log('   - Actividades:', datos.actividades?.length || 0);
      console.log('   - Firma usuario:', firmaUsuario ? 'Sí' : 'No');
      console.log('   - Firma supervisor:', firmaSupervisor ? 'Sí' : 'No');
      
      const doc = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4'
      });

      const pageHeight = doc.internal.pageSize.getHeight();
      const pageWidth = doc.internal.pageSize.getWidth();
      const margin = 15;
      const contentWidth = pageWidth - (margin * 2);
      let currentY = 10;

      // ========== ENCABEZADO CON IMAGEN DE LOGOS ==========
      let superiorImageBase64 = null;
      let imgDimensions = null;
      
      try {
        const result = await this.cargarImagenComoBase64(superiorImage);
        superiorImageBase64 = result.data;
        imgDimensions = result.dimensions;
      } catch (error) {
        console.warn('⚠️ No se pudo cargar imagen de encabezado');
      }
      
      if (superiorImageBase64 && imgDimensions) {
        const realAspectRatio = imgDimensions.height / imgDimensions.width;
        const imgWidth = contentWidth * 0.95;
        const imgHeight = imgWidth * realAspectRatio;
        const imgX = margin + (contentWidth - imgWidth) / 2;
        doc.addImage(superiorImageBase64, 'PNG', imgX, currentY, imgWidth, imgHeight);
        currentY += imgHeight + 5;
      }
    
      // Recuadro principal con títulos
      doc.setDrawColor(0, 0, 0);
      doc.setLineWidth(0.5);
      doc.rect(margin, currentY, contentWidth, 25);
      
      doc.setFontSize(9);
      doc.setFont(undefined, 'bold');
      doc.setTextColor(0, 0, 0);
      doc.text('SECRETARÍA DE BIENESTAR', pageWidth / 2, currentY + 6, { align: 'center' });
      doc.text('SUBSECRETARÍA DE INCLUSIÓN PRODUCTIVA Y DESARROLLO RURAL', pageWidth / 2, currentY + 11, { align: 'center' });
      doc.text('FORMATO DE SEGUIMIENTO A ACTIVIDADES PROGRAMADAS', pageWidth / 2, currentY + 16, { align: 'center' });
      
      // Fecha en la esquina
      const fechaActual = new Date(datos.fechaGeneracion || new Date()).toLocaleDateString('es-MX', {
        day: '2-digit', month: '2-digit', year: 'numeric'
      });
      doc.setFontSize(8);
      doc.setFont(undefined, 'normal');
      doc.text('Fecha:', pageWidth - margin - 35, currentY + 21);
      doc.rect(pageWidth - margin - 25, currentY + 18, 25, 5);
      doc.text(fechaActual, pageWidth - margin - 12.5, currentY + 21.5, { align: 'center' });
      
      currentY += 30;
      
      // ========== TABLA DE INFORMACIÓN DEL PRESTADOR ==========
      const usuario = datos.usuario || {};
      const periodo = datos.periodo || {};
      const col1Width = contentWidth * 0.5;
      const col2Width = contentWidth * 0.5;
      
      // Fila 1: Nombre
      doc.setDrawColor(0, 0, 0);
      doc.setLineWidth(0.3);
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      doc.setFontSize(8);
      doc.setFont(undefined, 'bold');
      doc.text('Nombre del prestador de Servicios', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      doc.text(usuario.nombre || 'Sin nombre', margin + col1Width + 2, currentY + 4);
      currentY += 6;
      
      // Fila 2: CURP
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      doc.setFont(undefined, 'bold');
      doc.text('CURP', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      doc.text(usuario.curp || 'No registrado', margin + col1Width + 2, currentY + 4);
      currentY += 6;
      
      // Fila 3: Periodo
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      doc.setFont(undefined, 'bold');
      doc.text('Periodo', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      const mesNombre = periodo.mesNombre || 'N/A';
      const anio = periodo.anio || 'N/A';
      doc.text(`${mesNombre} ${anio}`, margin + col1Width + 2, currentY + 4);
      currentY += 8;
      
      // Fila 4: Programa
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      doc.setFont(undefined, 'bold');
      doc.text('Programa Social del Apoyo', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      doc.text('SEMBRANDO VIDA', margin + col1Width + 2, currentY + 4);
      currentY += 8;
      
      // Fila 5: Territorio
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      doc.setFont(undefined, 'bold');
      doc.text('Territorio y entidad donde presta sus servicios', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      doc.text(usuario.territorio || 'No asignado', margin + col1Width + 2, currentY + 4);
      currentY += 10;
      
      // ========== TABLA DE ACTIVIDADES ==========
      const actividades = datos.actividades || [];
      const tableWidth = contentWidth;
      const tableX = margin;
      const colWidths = [15, 32, 18, 22, 83];
      
      // Header
      doc.setFillColor(255, 255, 255);
      doc.rect(tableX, currentY, tableWidth, 8, 'FD');
      doc.setFontSize(8);
      doc.setFont(undefined, 'bold');
      
      let colX = tableX + 2;
      doc.text('No.', colX + colWidths[0]/2, currentY + 5.5, { align: 'center' });
      doc.line(colX + colWidths[0], currentY, colX + colWidths[0], currentY + 8);
      colX += colWidths[0];
      doc.text('Fecha', colX + colWidths[1]/2, currentY + 5.5, { align: 'center' });
      doc.line(colX + colWidths[1], currentY, colX + colWidths[1], currentY + 8);
      colX += colWidths[1];
      doc.text('Tipo', colX + colWidths[2]/2, currentY + 5.5, { align: 'center' });
      doc.line(colX + colWidths[2], currentY, colX + colWidths[2], currentY + 8);
      colX += colWidths[2];
      doc.text('Hora', colX + colWidths[3]/2, currentY + 5.5, { align: 'center' });
      doc.line(colX + colWidths[3], currentY, colX + colWidths[3], currentY + 8);
      colX += colWidths[3];
      doc.text('Actividad desarrollada', colX + colWidths[4]/2, currentY + 5.5, { align: 'center' });
      currentY += 8;
      
      // Filas de datos
      doc.setFontSize(7);
      doc.setFont(undefined, 'normal');
      const baseRowHeight = 8;
      const lineHeight = 3;

      actividades.forEach((actividad, index) => {
        const activDesc = actividad.descripcion || actividad.categoria_actividad || 'Actividad de campo';
        const maxTextWidth = colWidths[4] - 4;
        const textLines = doc.splitTextToSize(activDesc, maxTextWidth);
        const rowHeight = Math.max(baseRowHeight, textLines.length * lineHeight + 3);
        
        if (currentY > pageHeight - 50) {
          doc.addPage();
          currentY = 20;
        }

        doc.rect(tableX, currentY, tableWidth, rowHeight, 'S');

        const fecha = actividad.fecha_hora ? new Date(actividad.fecha_hora).toLocaleDateString('es-MX', { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' }) : '-';
        const hora = actividad.fecha_hora ? new Date(actividad.fecha_hora).toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit', hour12: false }) : '-';
        const tipo = (actividad.tipo_actividad || 'Campo').charAt(0).toUpperCase() + (actividad.tipo_actividad || 'campo').slice(1);

        colX = tableX + 2;
        const textYCenter = currentY + (rowHeight / 2) + 1.5;
        
        doc.text(String(index + 1), colX + colWidths[0]/2, textYCenter, { align: 'center' });
        doc.line(colX + colWidths[0], currentY, colX + colWidths[0], currentY + rowHeight);
        
        colX += colWidths[0];
        doc.text(fecha, colX + 2, textYCenter);
        doc.line(colX + colWidths[1], currentY, colX + colWidths[1], currentY + rowHeight);
        
        colX += colWidths[1];
        doc.text(tipo, colX + colWidths[2]/2, textYCenter, { align: 'center' });
        doc.line(colX + colWidths[2], currentY, colX + colWidths[2], currentY + rowHeight);
        
        colX += colWidths[2];
        doc.text(hora, colX + colWidths[3]/2, textYCenter, { align: 'center' });
        doc.line(colX + colWidths[3], currentY, colX + colWidths[3], currentY + rowHeight);
        
        colX += colWidths[3];
        textLines.forEach((line, lineIndex) => {
          doc.text(line, colX + 2, currentY + 4 + (lineIndex * lineHeight));
        });

        currentY += rowHeight;
      });

      currentY += 15;

      // ========== SECCIÓN DE FIRMAS (PRIMERA PÁGINA) ==========
      if (currentY > pageHeight - 70) {
        doc.addPage();
        currentY = 30;
      }

      let firmaWidth = 65;
      const firmaHeight = 25;
      const firmaUsuarioX = margin + 5;
      const firmaResponsableX = pageWidth - margin - firmaWidth - 5;
      const firmaY = currentY;
      
      // Etiquetas
      doc.setFillColor(255, 218, 185);
      doc.setLineWidth(0.3);
      
      doc.rect(firmaUsuarioX, firmaY - 8, firmaWidth, 7, 'FD');
      doc.setFontSize(9);
      doc.setFont(undefined, 'bold');
      doc.text('Elaboró', firmaUsuarioX + firmaWidth / 2, firmaY - 3.5, { align: 'center' });
      
      doc.setFillColor(255, 218, 185);
      doc.rect(firmaResponsableX, firmaY - 8, firmaWidth, 7, 'FD');
      doc.text('Autorizó', firmaResponsableX + firmaWidth / 2, firmaY - 3.5, { align: 'center' });
      
      // FIRMA DEL USUARIO (Izquierda)
      if (firmaUsuario) {
        try {
          doc.addImage(firmaUsuario, 'PNG', firmaUsuarioX, firmaY, firmaWidth, firmaHeight);
        } catch (e) {
          console.warn('No se pudo agregar firma del usuario');
        }
      }
      
      doc.setLineWidth(0.5);
      doc.line(firmaUsuarioX, firmaY + firmaHeight + 5, firmaUsuarioX + firmaWidth, firmaY + firmaHeight + 5);
      
      doc.setFontSize(8);
      doc.setFont(undefined, 'normal');
      doc.text(usuario.cargo || 'Facilitador Comunitario', firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' });
      doc.setFont(undefined, 'bold');
      doc.text(usuario.nombre || 'Sin nombre', firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 17, { align: 'center' });
      
      // FIRMA DEL SUPERVISOR (Derecha) - Solo si existe
      if (firmaSupervisor) {
        try {
          doc.addImage(firmaSupervisor, 'PNG', firmaResponsableX, firmaY, firmaWidth, firmaHeight);
          console.log('✅ Firma del supervisor agregada al PDF');
        } catch (e) {
          console.warn('No se pudo agregar firma del supervisor');
        }
      }
      
      doc.setLineWidth(0.5);
      doc.line(firmaResponsableX, firmaY + firmaHeight + 5, firmaResponsableX + firmaWidth, firmaY + firmaHeight + 5);
      
      doc.setFontSize(7.5);
      doc.setFont(undefined, 'normal');
      doc.text('Encargada de Despacho de la Coordinación', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' });
      doc.text('Territorial ' + (usuario.territorio || ''), firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 16, { align: 'center' });
      
      doc.setFontSize(8);
      doc.setFont(undefined, 'bold');
      doc.text(nombreSupervisor || usuario.supervisor || 'Sin asignar', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 22, { align: 'center' });

      // ========== SEGUNDA PÁGINA: EVIDENCIAS FOTOGRÁFICAS ==========
      try {
        console.log('🖼️ Iniciando generación de página de evidencias fotográficas...');
        
        // Filtrar actividades con fotos del período
        const actividadesConFoto = (datos.actividades || []).filter(act => 
          act.foto_base64 || act.foto_url
        );
        
        console.log(`📸 Actividades con foto encontradas: ${actividadesConFoto.length}`);
        
        // SIEMPRE crear la página de evidencias fotográficas
        doc.addPage();
        currentY = 10;

        // ========== ENCABEZADO DE LA PÁGINA DE EVIDENCIAS ==========
        if (superiorImageBase64 && imgDimensions) {
          const realAspectRatio = imgDimensions.height / imgDimensions.width;
          const imgWidth = contentWidth * 0.95;
          const imgHeight = imgWidth * realAspectRatio;
          const imgX = margin + (contentWidth - imgWidth) / 2;
          
          doc.addImage(superiorImageBase64, 'PNG', imgX, currentY, imgWidth, imgHeight);
          currentY += imgHeight + 5;
        }
        
        // Título de la sección
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.5);
        doc.rect(margin, currentY, contentWidth, 12);
          
        doc.setFontSize(11);
        doc.setFont(undefined, 'bold');
        doc.setTextColor(0, 0, 0);
        doc.text('EVIDENCIAS FOTOGRÁFICAS DE ACTIVIDADES', pageWidth / 2, currentY + 5, { align: 'center' });
        doc.setFontSize(9);
        doc.setFont(undefined, 'normal');
        doc.text(`${periodo.mesNombre || ''} ${periodo.anio || ''}`, pageWidth / 2, currentY + 10, { align: 'center' });
        
        currentY += 15;

        // ========== DATOS DEL USUARIO ==========
        doc.setFillColor(240, 240, 240);
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.3);
        doc.rect(margin, currentY, contentWidth, 18, 'FD');
        
        doc.setFontSize(8);
        doc.setTextColor(0, 0, 0);
        
        // Nombre
        doc.setFont(undefined, 'bold');
        doc.text('Nombre:', margin + 3, currentY + 5);
        doc.setFont(undefined, 'normal');
        doc.text(usuario.nombre || 'Sin nombre', margin + 20, currentY + 5);
        
        // CURP
        doc.setFont(undefined, 'bold');
        doc.text('CURP:', margin + 95, currentY + 5);
        doc.setFont(undefined, 'normal');
        doc.text(usuario.curp || 'No registrado', margin + 107, currentY + 5);
        
        // Cargo
        doc.setFont(undefined, 'bold');
        doc.text('Cargo:', margin + 3, currentY + 11);
        doc.setFont(undefined, 'normal');
        doc.text(usuario.cargo || 'Facilitador Comunitario', margin + 17, currentY + 11);
        
        // Territorio
        doc.setFont(undefined, 'bold');
        doc.text('Territorio:', margin + 95, currentY + 11);
        doc.setFont(undefined, 'normal');
        doc.text(usuario.territorio || 'No asignado', margin + 115, currentY + 11);
        
        // Período
        doc.setFont(undefined, 'bold');
        doc.text('Período:', margin + 3, currentY + 17);
        doc.setFont(undefined, 'normal');
        doc.text(`${periodo.mesNombre || ''} ${periodo.anio || ''}`, margin + 18, currentY + 17);
        
        currentY += 22;

        // ========== VERIFICAR SI HAY IMÁGENES ==========
        if (actividadesConFoto.length === 0) {
          // Se mostrará mensaje después de las firmas
        } else {
          // Función para seleccionar imágenes de diferentes días
          const seleccionarImagenesDiversas = (actividades, maxImagenes) => {
            const imagenesSeleccionadas = [];
            const diasUsados = new Set();
            
            // Ordenar por fecha más reciente
            const actividadesOrdenadas = [...actividades].sort((a, b) => new Date(b.fecha_hora) - new Date(a.fecha_hora));
            
            // Primera pasada: una imagen por día
            for (const act of actividadesOrdenadas) {
              if (imagenesSeleccionadas.length >= maxImagenes) break;
              const dia = new Date(act.fecha_hora).toISOString().split('T')[0];
              if (!diasUsados.has(dia)) {
                imagenesSeleccionadas.push(act);
                diasUsados.add(dia);
              }
            }
            
            // Segunda pasada: si no hay suficientes, agregar las restantes
            if (imagenesSeleccionadas.length < maxImagenes) {
              for (const act of actividadesOrdenadas) {
                if (imagenesSeleccionadas.length >= maxImagenes) break;
                if (!imagenesSeleccionadas.includes(act)) {
                  imagenesSeleccionadas.push(act);
                }
              }
            }
            
            return imagenesSeleccionadas;
          };
          
          // ========== SELECCIÓN DE 6 IMÁGENES: PRIMERO CAMPO, LUEGO GABINETE ==========
          const actividadesCampoDisponibles = actividadesConFoto
            .filter(a => (a.tipo_actividad || 'campo').toLowerCase() === 'campo');
          const actividadesGabineteDisponibles = actividadesConFoto
            .filter(a => (a.tipo_actividad || '').toLowerCase() === 'gabinete');
          
          const actividadesCampo = seleccionarImagenesDiversas(actividadesCampoDisponibles, 3);
          const actividadesGabinete = seleccionarImagenesDiversas(actividadesGabineteDisponibles, 3);
          
          const imagenesSeleccionadas = [...actividadesCampo, ...actividadesGabinete].slice(0, 6);
          console.log(`📷 Procesando ${imagenesSeleccionadas.length} imágenes para el PDF`);
          
          // Grid de imágenes
const imgGridWidth = 55;
        const imgGridHeight = 45;
        const imgsPerRow = 3;
        const imgSpacing = 5;
        const labelHeight = 14;
          
          for (let i = 0; i < imagenesSeleccionadas.length; i++) {
            const actividad = imagenesSeleccionadas[i];
            const col = i % imgsPerRow;
            const row = Math.floor(i / imgsPerRow);
            
            const imgX = margin + (col * (imgGridWidth + imgSpacing));
          const imgY = currentY + (row * (imgGridHeight + labelHeight + 5));
            
            // Borde de la imagen
            doc.setDrawColor(0, 0, 0);
            doc.setLineWidth(0.3);
            doc.rect(imgX, imgY, imgGridWidth, imgGridHeight);
            
            // Intentar agregar imagen
            try {
              let imgData = null;
              
              // Primero intentar con foto_base64
              if (actividad.foto_base64) {
                let imgBase64 = actividad.foto_base64;
                if (!imgBase64.startsWith('data:')) {
                  imgBase64 = 'data:image/jpeg;base64,' + imgBase64;
                }
                imgData = imgBase64;
                console.log(`✅ Usando foto_base64 para imagen ${i + 1}`);
              }
              // Si no tiene foto_base64, intentar cargar desde foto_url
              else if (actividad.foto_url) {
                console.log(`📥 Cargando imagen ${i + 1} desde URL: ${actividad.foto_url}`);
                try {
                  const result = await this.cargarImagenComoBase64(actividad.foto_url);
                  imgData = result.data;
                  console.log(`✅ Imagen ${i + 1} cargada desde URL`);
                } catch (loadError) {
                  console.warn(`⚠️ No se pudo cargar imagen ${i + 1} desde URL:`, loadError);
                }
              }
              
              // Si tenemos imagen, agregarla
              if (imgData) {
                doc.addImage(imgData, 'JPEG', imgX + 1, imgY + 1, imgGridWidth - 2, imgGridHeight - 2);
                console.log(`✅ Imagen ${i + 1} agregada al PDF`);
              } else {
                // Placeholder gris
                doc.setFillColor(220, 220, 220);
                doc.rect(imgX + 1, imgY + 1, imgGridWidth - 2, imgGridHeight - 2, 'F');
                doc.setDrawColor(200, 200, 200);
                doc.rect(imgX, imgY, imgGridWidth, imgGridHeight, 'S');
                
                doc.setTextColor(150, 150, 150);
                doc.setFontSize(8);
                doc.text('Imagen no', imgX + imgGridWidth / 2, imgY + imgGridHeight / 2 - 3, { align: 'center' });
                doc.text('disponible', imgX + imgGridWidth / 2, imgY + imgGridHeight / 2 + 3, { align: 'center' });
                console.log(`⚠️ Imagen ${i + 1} sin datos`);
              }
            } catch (imgError) {
              console.warn(`❌ Error agregando imagen ${i + 1}:`, imgError);
              
              // Placeholder en caso de error
              doc.setFillColor(240, 240, 240);
              doc.rect(imgX, imgY, imgGridWidth, imgGridHeight, 'F');
              doc.setDrawColor(200, 200, 200);
              doc.rect(imgX, imgY, imgGridWidth, imgGridHeight, 'S');
              
              doc.setTextColor(150, 150, 150);
              doc.setFontSize(8);
              doc.text('Imagen no', imgX + imgGridWidth / 2, imgY + imgGridHeight / 2 - 3, { align: 'center' });
              doc.text('disponible', imgX + imgGridWidth / 2, imgY + imgGridHeight / 2 + 3, { align: 'center' });
            }
            
            // Etiqueta con tipo y fecha
            const tipoAct = actividad.tipo_actividad || actividad.tipo || 'campo';
            const tipoTexto = tipoAct.toLowerCase() === 'campo' ? 'CAMPO' : 'GABINETE';
            
            // Fondo según tipo
            if (tipoAct.toLowerCase() === 'campo') {
              doc.setFillColor(34, 197, 94); // Verde
            } else {
              doc.setFillColor(147, 51, 234); // Morado
            }
            doc.rect(imgX, imgY + imgGridHeight, imgGridWidth, labelHeight, 'F');
            doc.setDrawColor(0, 0, 0);
            doc.setLineWidth(0.2);
            doc.rect(imgX, imgY + imgGridHeight, imgGridWidth, labelHeight, 'S');
            
            // Texto tipo
            doc.setTextColor(255, 255, 255);
            doc.setFontSize(10);
            doc.setFont(undefined, 'bold');
            doc.text(tipoTexto, imgX + imgGridWidth / 2, imgY + imgGridHeight + 6, { align: 'center' });
            
            // Fecha compacta
            if (actividad.fecha_hora || actividad.fecha) {
              const fechaObj = new Date(actividad.fecha_hora || actividad.fecha);
              const dia = String(fechaObj.getDate()).padStart(2, '0');
              const mes = String(fechaObj.getMonth() + 1).padStart(2, '0');
              const anio = String(fechaObj.getFullYear()).slice(-2);
              const hora = String(fechaObj.getHours()).padStart(2, '0');
              const min = String(fechaObj.getMinutes()).padStart(2, '0');
              const fechaCompacta = `${dia}/${mes}/${anio} ${hora}:${min}`;
              
              doc.setFont(undefined, 'normal');
              doc.setFontSize(6);
              doc.text(fechaCompacta, imgX + imgGridWidth / 2, imgY + imgGridHeight + 11, { align: 'center' });
            }
          }
          
          // Calcular currentY después del grid de imágenes
          const numRows = Math.ceil(imagenesSeleccionadas.length / imgsPerRow);
          currentY += (numRows * (imgGridHeight + labelHeight + 3)) + 20;
        }
        
        // ========== FIRMAS EN PÁGINA DE EVIDENCIAS ==========
        if (firmaUsuario) {
          // Verificar si hay espacio para firmas
          if (currentY > pageHeight - 70) {
            doc.addPage();
            currentY = 30;
          }

          firmaWidth = 70;
          const firmaHeight = 30;
          const firmaUsuarioX = margin + 5;
          const firmaResponsableX = pageWidth - margin - firmaWidth - 5;
          const firmaY = currentY;
          
          // Etiquetas "Elaboró" y "Autorizó"
          doc.setFillColor(255, 218, 185);
          doc.setDrawColor(0, 0, 0);
          doc.setLineWidth(0.3);
          
          doc.rect(firmaUsuarioX, firmaY - 8, firmaWidth, 7, 'FD');
          doc.setTextColor(0, 0, 0);
          doc.setFontSize(9);
          doc.setFont(undefined, 'bold');
          doc.text('Elaboró', firmaUsuarioX + firmaWidth / 2, firmaY - 3.5, { align: 'center' });
          
          doc.setFillColor(255, 218, 185);
          doc.rect(firmaResponsableX, firmaY - 8, firmaWidth, 7, 'FD');
          doc.text('Autorizó', firmaResponsableX + firmaWidth / 2, firmaY - 3.5, { align: 'center' });
          
          // FIRMA DEL USUARIO (Izquierda)
          try {
            doc.addImage(firmaUsuario, 'PNG', firmaUsuarioX, firmaY, firmaWidth, firmaHeight);
          } catch (e) {
            console.warn('No se pudo agregar firma del usuario en página de evidencias');
          }
          
          // Líneas de firma
          doc.setLineWidth(0.5);
          doc.line(firmaUsuarioX, firmaY + firmaHeight + 5, firmaUsuarioX + firmaWidth, firmaY + firmaHeight + 5);
          doc.line(firmaResponsableX, firmaY + firmaHeight + 5, firmaResponsableX + firmaWidth, firmaY + firmaHeight + 5);
          
          // Información del usuario
          doc.setTextColor(0, 0, 0);
          doc.setFontSize(8);
          doc.setFont(undefined, 'normal');
          const cargoUsuario = usuario.cargo || 'Facilitador Comunitario';
          doc.text(cargoUsuario, firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' });
          doc.setFont(undefined, 'bold');
          doc.text(usuario.nombre || 'Sin nombre', firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 17, { align: 'center' });
          
          // FIRMA DEL SUPERVISOR (Derecha) - Si existe
          if (firmaSupervisor) {
            try {
              doc.addImage(firmaSupervisor, 'PNG', firmaResponsableX, firmaY, firmaWidth, firmaHeight);
            } catch (e) {
              console.warn('No se pudo agregar firma del supervisor en página de evidencias');
            }
          }
          
          // Información del responsable
          doc.setFontSize(7.5);
          doc.setFont(undefined, 'normal');
          doc.text('Encargada de Despacho de la Coordinación', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' });
          doc.text('Territorial ' + (usuario.territorio || ''), firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 16, { align: 'center' });
          doc.setFontSize(8);
          doc.setFont(undefined, 'bold');
          const nombreSupervisorFinal = nombreSupervisor || usuario.supervisor || 'Sin asignar';
          doc.text(nombreSupervisorFinal, firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 22, { align: 'center' });
        }
        
        console.log('✅ Página de evidencias fotográficas completada');
        
      } catch (evidenciasError) {
        console.error('❌ Error generando página de evidencias:', evidenciasError);
      }

      // ========== PIE DE PÁGINA ==========
      const totalPages = doc.internal.getNumberOfPages();
      for (let i = 1; i <= totalPages; i++) {
        doc.setPage(i);
        doc.setTextColor(128, 0, 32);
        doc.setFontSize(7);
        doc.setFont(undefined, 'normal');
        const footerText = 'Paseo de la Reforma # 116, Piso 16, Col. Juárez, Alc. Cuauhtémoc, CDMX C.P. 06600 Tel.: (55) 5328 5000 www.gob.mx/bienestar';
        doc.text(footerText, pageWidth / 2, pageHeight - 10, { align: 'center' });
      }

      // Obtener PDF como base64 (sin prefijo data:)
      const pdfOutput = doc.output('datauristring');
      const base64 = pdfOutput.split(',')[1];
      
      console.log('✅ PDF generado desde datos estructurados');
      return base64;
    },
    
    /**
     * Agrega la firma del supervisor a un PDF existente
     * @param {string} pdfBase64 - El PDF original en base64
     * @param {string} firmaBase64 - La firma del supervisor en base64
     * @returns {string} - El PDF modificado en base64
     */
    async agregarFirmaSupervisorPDF(pdfBase64, firmaBase64) {
      try {
        // Convertir base64 del PDF a bytes
        const pdfBytes = Uint8Array.from(atob(pdfBase64), c => c.charCodeAt(0));
        
        // Cargar el PDF existente
        const pdfDoc = await PDFDocument.load(pdfBytes);
        
        // Obtener la primera página (donde están las firmas)
        const pages = pdfDoc.getPages();
        const firstPage = pages[0];
        const { width, height } = firstPage.getSize();
        
        // Preparar la imagen de la firma
        let firmaClean = firmaBase64;
        if (firmaClean.includes(',')) {
          firmaClean = firmaClean.split(',')[1];
        }
        
        // Convertir la firma base64 a bytes
        const firmaBytes = Uint8Array.from(atob(firmaClean), c => c.charCodeAt(0));
        
        // Intentar como PNG primero
        let firmaImage;
        try {
          firmaImage = await pdfDoc.embedPng(firmaBytes);
        } catch (e) {
          // Si falla, intentar como JPEG
          try {
            firmaImage = await pdfDoc.embedJpg(firmaBytes);
          } catch (e2) {
            console.warn('⚠️ No se pudo insertar la imagen de firma:', e2);
            // Retornar el PDF original sin modificar
            return pdfBase64;
          }
        }
        
        // Calcular posición de la firma del supervisor (sección "Autorizó" - lado derecho)
        // Estos valores corresponden a la posición en el PDF generado por jsPDF
        // El PDF usa tamaño carta (215.9 x 279.4 mm)
        const pageWidth = width; // ~612 puntos para carta
        const margin = 15 * 2.83465; // 15mm en puntos
        const firmaWidth = 65 * 2.83465; // 65mm en puntos
        const firmaHeight = 20 * 2.83465; // 20mm en puntos
        
        // Posición X: lado derecho (después del centro)
        const firmaX = pageWidth - margin - firmaWidth;
        // Posición Y: desde abajo (las firmas están cerca del final de la primera página)
        // Ajustamos basándonos en el layout típico del reporte
        const firmaY = 50; // Cerca del fondo de la página
        
        // Dibujar la firma del supervisor
        firstPage.drawImage(firmaImage, {
          x: firmaX,
          y: firmaY,
          width: firmaWidth,
          height: firmaHeight,
        });
        
        console.log('✅ Firma del supervisor agregada al PDF');
        
        // Guardar el PDF modificado
        const modifiedPdfBytes = await pdfDoc.save();
        
        // Convertir a base64
        const modifiedBase64 = btoa(
          modifiedPdfBytes.reduce((data, byte) => data + String.fromCharCode(byte), '')
        );
        
        return modifiedBase64;
        
      } catch (error) {
        console.error('❌ Error agregando firma al PDF:', error);
        // En caso de error, retornar el PDF original
        return pdfBase64;
      }
    },

    async verReporteHistorial(reporte) {
      // Ver un reporte previamente generado - genera PDF y lo abre
      // NUEVO FLUJO: Genera PDF desde datos estructurados con las firmas disponibles
      if (this.viendoReporte) {
        console.log('⚠️ Ya se está cargando un reporte');
        return;
      }

      console.log(`👁️ Visualizando reporte del historial: ${reporte.nombre}`);
      this.viendoReporte = reporte.id;

      try {
        // Obtener datos del reporte desde el servidor
        const response = await api.get(`/reportes/descargar/${reporte.id}`);
        
        if (!response.data.success) {
          throw new Error('No se pudo obtener el reporte');
        }
        
        const reporteData = response.data.reporte;
        let base64Data = null;
        
        // NUEVO FLUJO: Si hay datos_reporte, generar PDF desde los datos
        if (reporteData.datos_reporte) {
          console.log('📄 Generando PDF desde datos estructurados...');
          
          base64Data = await this.generarPDFDesdesDatos(
            reporteData.datos_reporte,
            reporteData.firma_usuario_base64,
            reporteData.firmado_supervisor ? reporteData.firma_supervisor_base64 : null,
            reporteData.nombre_supervisor
          );
          
        } else if (reporteData.pdf_base64) {
          // COMPATIBILIDAD: Si hay PDF guardado (reportes antiguos)
          console.log('📄 Usando PDF guardado (compatibilidad)...');
          
          base64Data = limpiarBase64(reporteData.pdf_base64);
          
          if (reporteData.firmado_supervisor && reporteData.firma_supervisor_base64) {
            console.log('✍️ Agregando firma del supervisor al PDF...');
            base64Data = await this.agregarFirmaSupervisorPDF(base64Data, reporteData.firma_supervisor_base64);
          }
        } else {
          throw new Error('El reporte no tiene datos para generar el PDF');
        }
        
        if (!base64Data) {
          throw new Error('Error generando el PDF');
        }
        
        // Convertir base64 a blob
        const byteCharacters = atob(base64Data);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: 'application/pdf' });
        
        const nombreArchivo = `${reporte.nombre.replace(/\s+/g, '_')}.pdf`;
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        
        if (isMobile) {
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.download = nombreArchivo;
          link.target = '_blank';
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          
          setTimeout(() => window.URL.revokeObjectURL(url), 2000);
          
          this.$notify?.({
            type: 'success',
            message: reporteData.firmado_supervisor 
              ? 'PDF generado con firma de supervisor' 
              : 'PDF generado (pendiente de autorización)'
          });
        } else {
          const url = window.URL.createObjectURL(blob);
          window.open(url, '_blank');
          setTimeout(() => window.URL.revokeObjectURL(url), 1000);
        }
        
      } catch (error) {
        console.error('❌ Error visualizando reporte:', error);
        
        this.$notify?.({
          type: 'error',
          message: 'Error al abrir el reporte'
        });
      } finally {
        this.viendoReporte = null;
      }
    },

    async eliminarReporteHistorial(reporte) {
      // Mostrar modal de confirmación
      this.reporteAEliminar = reporte;
      this.mostrarModalEliminar = true;
    },

    cancelarEliminar() {
      this.mostrarModalEliminar = false;
      this.reporteAEliminar = null;
    },

    async confirmarEliminarReporte() {
      const reporte = this.reporteAEliminar;
      this.mostrarModalEliminar = false;

      if (!reporte || this.eliminandoReporte) {
        return;
      }

      this.eliminandoReporte = reporte.id;
      console.log(`🗑️ Eliminando reporte: ${reporte.nombre} (mes: ${reporte.mes}, año: ${reporte.anio})`);

      try {
        const response = await api.delete(`/reportes/eliminar/${reporte.id}`);
        
        if (response.data.success) {
          console.log('✅ Reporte eliminado correctamente');
          
          // Eliminar del array local INMEDIATAMENTE
          const index = this.reportesGenerados.findIndex(r => r.id === reporte.id);
          if (index !== -1) {
            this.reportesGenerados.splice(index, 1);
          }
          
          // Actualizar localStorage
          localStorage.setItem('reportesGenerados', JSON.stringify(this.reportesGenerados));
          
          // REACTIVO: Verificar si el reporte eliminado era del mes/año actualmente seleccionado
          // Convertir a string para comparación segura (el mes viene como string, el año puede ser number)
          const mesReporte = String(reporte.mes);
          const anioReporte = Number(reporte.anio);
          const mesActualStr = String(this.mesActual);
          const anioActualNum = Number(this.anioSeleccionado);
          
          console.log(`📊 Comparando: Reporte(${mesReporte}/${anioReporte}) vs Actual(${mesActualStr}/${anioActualNum})`);
          
          if (mesReporte === mesActualStr && anioReporte === anioActualNum) {
            // Limpiar INMEDIATAMENTE el estado de reporte existente
            // Esto habilitará el botón de generar reporte al instante
            this.reporteExistente = null;
            console.log('🔓 Botón de generar reporte habilitado - El reporte del mes actual fue eliminado');
          }
          
          this.$notify?.({
            type: 'success',
            message: 'Reporte eliminado - Ya puedes generar uno nuevo para este mes'
          });
        } else {
          throw new Error('Error al eliminar el reporte');
        }
        
      } catch (error) {
        console.error('❌ Error eliminando reporte:', error);
        
        let mensaje = 'Error al eliminar el reporte';
        if (error.response?.status === 404) {
          mensaje = 'El reporte no fue encontrado';
        }
        
        this.$notify?.({
          type: 'error',
          message: mensaje
        });
      } finally {
        this.eliminandoReporte = null;
        this.reporteAEliminar = null;
      }
    }
  },

  async mounted() {
    console.log('🚀 Reportes.vue montado');
    
    // Generar años disponibles (años pasados y futuros)
    const currentYear = new Date().getFullYear();
    this.anos = Array.from({ length: 5 }, (_, i) => currentYear - 2 + i);

    // Cargar información del usuario
    const usuario = JSON.parse(localStorage.getItem('user'));
    console.log('👤 Usuario desde localStorage:', usuario ? `ID: ${usuario.id}` : 'No encontrado');
    
    if (usuario) {
      this.usuarioInfo = {
        id: usuario.id || null,
        nombre: usuario.nombre_completo || usuario.nombre || 'Usuario',
        cargo: usuario.cargo || '',
        correo: usuario.correo || '',
        territorio: usuario.territorio || 'No asignado',
        curp: usuario.curp || 'No registrada',
        supervisor: usuario.supervisor || 'No asignado'
      };
      
      console.log('✅ Usuario info establecido:', JSON.stringify(this.usuarioInfo));
      
      // Obtener datos actualizados del usuario desde la BD (incluyendo CURP)
      try {
        console.log('🔄 Actualizando datos del usuario desde la BD...');
        const usuarioActualizado = await apiService.getUser(usuario.id);
        if (usuarioActualizado) {
          // Actualizar usuarioInfo con datos frescos
          if (usuarioActualizado.curp) {
            this.usuarioInfo.curp = usuarioActualizado.curp;
            usuario.curp = usuarioActualizado.curp;
          }
          if (usuarioActualizado.nombre_completo) {
            this.usuarioInfo.nombre = usuarioActualizado.nombre_completo;
            usuario.nombre_completo = usuarioActualizado.nombre_completo;
          }
          if (usuarioActualizado.territorio) {
            this.usuarioInfo.territorio = usuarioActualizado.territorio;
            usuario.territorio = usuarioActualizado.territorio;
          }
          if (usuarioActualizado.cargo) {
            this.usuarioInfo.cargo = usuarioActualizado.cargo;
            usuario.cargo = usuarioActualizado.cargo;
          }
          // Actualizar localStorage con datos frescos
          localStorage.setItem('user', JSON.stringify(usuario));
          console.log('✅ Datos del usuario actualizados desde BD, CURP:', this.usuarioInfo.curp);
        }
      } catch (error) {
        console.warn('⚠️ No se pudieron actualizar datos del usuario desde BD:', error.message);
        // Continuar con los datos del localStorage
      }
      
      // Si es técnico, obtener supervisor automático basado en territorio
      const cargoUpper = (usuario.cargo || '').toUpperCase();
      if (cargoUpper === 'TECNICO SOCIAL' || cargoUpper === 'TECNICO PRODUCTIVO') {
        try {
          console.log('🔍 Buscando supervisor automático para técnico...');
          const respuesta = await apiService.obtenerSupervisorAutomatico(usuario.id);
          if (respuesta.success && respuesta.supervisor) {
            this.usuarioInfo.supervisor = respuesta.supervisor;
            
            // Actualizar también el localStorage para que Profile.vue lo muestre
            usuario.supervisor = respuesta.supervisor;
            localStorage.setItem('user', JSON.stringify(usuario));
            
            console.log(`✅ Supervisor automático asignado y guardado: ${respuesta.supervisor}`);
          } else {
            console.log(`ℹ️ No se encontró supervisor automático: ${respuesta.mensaje}`);
          }
        } catch (error) {
          console.error('❌ Error obteniendo supervisor automático:', error);
          // Mantener el supervisor actual si hay error
        }
      }
      
      // Cargar actividades (apiService auto-detecta servidor correcto)
      try {
        await this.cargarActividades();
      } catch (error) {
        console.error('❌ Error cargando actividades:', error);
      }

      // Cargar historial de reportes desde la base de datos
      try {
        await this.cargarHistorialReportes();
      } catch (error) {
        console.error('❌ Error cargando historial:', error);
      }
      
      // Verificar si ya existe un reporte para el mes/año actual
      try {
        await this.verificarReporteExistente();
      } catch (error) {
        console.error('❌ Error verificando reporte existente:', error);
      }
    } else {
      console.warn('⚠️ No hay usuario en localStorage');
    }
  }
};
</script>

<style scoped>
/* ================================================
   APPLE DESIGN SYSTEM - REPORTES
   ================================================ */

/* View Container */
.apple-view-container {
  position: fixed;
  inset: 0;
  overflow: hidden;
  background: linear-gradient(180deg, #f0fdf4 0%, #ecfdf5 50%, #f0fdf4 100%);
}

/* Dynamic Background */
.apple-dynamic-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
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
  background: linear-gradient(135deg, rgba(52, 211, 153, 0.4), rgba(16, 185, 129, 0.3));
}

.apple-orb-2 {
  width: 250px;
  height: 250px;
  top: 50%;
  left: 10%;
  background: linear-gradient(135deg, rgba(110, 231, 183, 0.35), rgba(52, 211, 153, 0.2));
  animation-delay: -7s;
}

.apple-orb-3 {
  width: 280px;
  height: 280px;
  bottom: 15%;
  left: 25%;
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.35), rgba(16, 185, 129, 0.25));
  animation-delay: -14s;
}

@keyframes appleOrbFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(20px, -30px) scale(1.05); }
  50% { transform: translate(-10px, 20px) scale(0.95); }
  75% { transform: translate(30px, 10px) scale(1.02); }
}

/* Scroll Container - Compacto */
.apple-scroll-container {
  position: absolute;
  inset: 0;
  overflow-y: auto;
  overflow-x: hidden;
  padding-top: 9.75rem;
  padding-bottom: 1rem;
  -webkit-overflow-scrolling: touch;
}

@media (min-width: 640px) {
  .apple-scroll-container {
    padding-top: 10.25rem;
  }
}

.apple-content-wrapper {
  position: relative;
  z-index: 10;
  padding: 0 0.75rem;
  min-height: 100%;
  max-width: 28rem;
  margin: 0 auto;
}

@media (min-width: 640px) {
  .apple-content-wrapper {
    padding: 0 1rem;
  }
}

.apple-sections-container {
  width: 100%;
  max-width: 28rem;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding-top: 0;
}

/* Header Card */
.apple-header-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 
    0 1px 3px rgba(0, 0, 0, 0.04),
    0 8px 24px rgba(0, 0, 0, 0.08);
}

.apple-header-icon {
  width: 56px;
  height: 56px;
  margin: 0 auto 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, #3b82f6, #2563eb);
  border-radius: 16px;
  color: white;
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.35);
}

.apple-header-title {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  color: rgba(0, 0, 0, 0.9);
  margin: 0 0 0.375rem;
}

.apple-header-subtitle {
  font-size: 0.8125rem;
  color: rgba(0, 0, 0, 0.5);
  margin: 0;
}

/* Stats Row */
.apple-stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
  margin-top: 1.25rem;
}

.apple-stat-pill {
  padding: 0.75rem 0.5rem;
  border-radius: 14px;
  text-align: center;
}

.apple-stat-blue {
  background: linear-gradient(145deg, rgba(59, 130, 246, 0.12), rgba(59, 130, 246, 0.08));
}

.apple-stat-green {
  background: linear-gradient(145deg, rgba(16, 185, 129, 0.12), rgba(16, 185, 129, 0.08));
}

.apple-stat-purple {
  background: linear-gradient(145deg, rgba(168, 85, 247, 0.12), rgba(168, 85, 247, 0.08));
}

.apple-stat-value {
  display: block;
  font-size: 1.25rem;
  font-weight: 700;
  color: rgba(0, 0, 0, 0.85);
}

.apple-stat-value.apple-stat-small {
  font-size: 0.75rem;
  font-weight: 600;
}

.apple-stat-label {
  display: block;
  font-size: 0.6875rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.5);
  margin-top: 0.125rem;
}

/* ================================================
   APPLE HEADER FIJO - STICKY TOP
   ================================================ */

.apple-header-fixed {
  position: fixed;
  top: 3.75rem;
  left: 0;
  right: 0;
  z-index: 20;
  padding: 0.625rem 0.75rem;
}

@media (min-width: 640px) {
  .apple-header-fixed {
    top: 4.75rem;
    padding: 0.75rem 1rem;
  }
}

.apple-header-content {
  max-width: 28rem;
  margin: 0 auto;
}

/* ================================================
   APPLE COMPACT HEADER - ESTILO MANUALES
   ================================================ */

.apple-compact-header {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.95) 0%, 
    rgba(255, 255, 255, 0.88) 100%);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-radius: 18px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  padding: 0.625rem 0.875rem;
  box-shadow: 
    0 4px 24px rgba(0, 0, 0, 0.06),
    0 1px 4px rgba(0, 0, 0, 0.04);
  animation: appleHeaderFadeIn 0.5s cubic-bezier(0.32, 0.72, 0, 1);
}

@keyframes appleHeaderFadeIn {
  from {
    opacity: 0;
    transform: scale(0.96) translateY(-8px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.apple-compact-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.apple-compact-title-group {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.apple-compact-title {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  color: #7D1D3F;
  margin: 0;
  line-height: 1.2;
}

.apple-compact-subtitle {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.75rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.45);
  margin: 0;
}

.apple-compact-right {
  display: flex;
  align-items: stretch;
  gap: 0.375rem;
}

/* Status Stack - Columnas apiladas */
.apple-status-stack {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  min-width: 64px;
}

/* Status Pill */
.apple-status-pill {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  border-radius: 100px;
  font-size: 0.75rem;
  font-weight: 600;
  transition: all 0.25s cubic-bezier(0.32, 0.72, 0, 1);
  width: 100%;
  text-align: center;
}

.apple-pill-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.6875rem;
  gap: 0.25rem;
}

.apple-pill-sm .apple-pill-dot {
  width: 5px;
  height: 5px;
}

.apple-pill-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  animation: dotPulse 2s ease-in-out infinite;
}

.apple-pill-muted {
  background: rgba(156, 163, 175, 0.08);
  color: rgba(107, 114, 128, 0.6);
}

.apple-pill-muted .apple-pill-dot {
  background: rgba(156, 163, 175, 0.4);
  animation: none;
}

@keyframes dotPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(0.85); }
}

.apple-pill-green {
  background: rgba(16, 185, 129, 0.12);
  color: #059669;
}

.apple-pill-green .apple-pill-dot {
  background: #10b981;
}

.apple-pill-amber {
  background: rgba(245, 158, 11, 0.12);
  color: #b45309;
}

.apple-pill-amber .apple-pill-dot {
  background: #f59e0b;
}

.apple-pill-blue {
  background: rgba(59, 130, 246, 0.12);
  color: #2563eb;
}

.apple-pill-blue .apple-pill-dot {
  background: #3b82f6;
}

.apple-pill-gray {
  background: rgba(107, 114, 128, 0.1);
  color: #6b7280;
}

.apple-pill-gray .apple-pill-dot {
  background: #9ca3af;
}

/* Stat Badge */
.apple-stat-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0.25rem 0.5rem;
  background: linear-gradient(145deg, rgba(59, 130, 246, 0.1), rgba(99, 102, 241, 0.06));
  border-radius: 8px;
  min-width: 56px;
  align-self: stretch;
}

.apple-badge-value {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: #3b82f6;
  line-height: 1;
}

.apple-badge-label {
  font-size: 0.5625rem;
  font-weight: 600;
  color: rgba(59, 130, 246, 0.7);
  text-transform: uppercase;
  letter-spacing: 0.02em;
  margin-top: 0.1875rem;
}

/* Responsive Compact Header - Sin wrap para altura fija */
@media (max-width: 400px) {
  .apple-compact-header {
    padding: 0.625rem 0.75rem;
  }
  
  .apple-compact-row {
    flex-wrap: nowrap;
    gap: 0.5rem;
  }
  
  .apple-compact-title {
    font-size: 1.125rem;
  }
  
  .apple-compact-subtitle {
    font-size: 0.6875rem;
  }
  
  .apple-compact-right {
    flex-shrink: 0;
    gap: 0.375rem;
  }
  
  .apple-status-stack {
    flex-direction: column;
    gap: 0.125rem;
    min-width: 56px;
  }
  
  .apple-status-pill {
    min-width: 0;
    padding: 0.125rem 0.375rem;
    font-size: 0.5625rem;
  }
  
  .apple-stat-badge {
    min-width: auto;
    flex-shrink: 0;
  }
}

@media (min-width: 401px) {
  .apple-compact-right {
    flex-shrink: 0;
  }
}

/* Section Card */
.apple-section-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 18px;
  padding: 1.25rem;
  box-shadow: 
    0 1px 3px rgba(0, 0, 0, 0.04),
    0 6px 20px rgba(0, 0, 0, 0.06);
}

.apple-section-header {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  margin-bottom: 1rem;
}

.apple-section-header-between {
  justify-content: space-between;
}

.apple-section-header-left {
  display: flex;
  align-items: center;
  gap: 0.875rem;
}

.apple-section-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  color: white;
  flex-shrink: 0;
}

.apple-icon-blue { background: linear-gradient(145deg, #3b82f6, #2563eb); }
.apple-icon-indigo { background: linear-gradient(145deg, #6366f1, #4f46e5); }
.apple-icon-purple { background: linear-gradient(145deg, #a855f7, #9333ea); }
.apple-icon-green { background: linear-gradient(145deg, #10b981, #059669); }
.apple-icon-amber { background: linear-gradient(145deg, #f59e0b, #d97706); }
.apple-icon-pdf { background: linear-gradient(145deg, #ef4444, #dc2626); }
.apple-icon-csv { background: linear-gradient(145deg, #22c55e, #16a34a); }

.apple-section-title {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
  font-size: 1rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.9);
  margin: 0;
}

.apple-section-subtitle {
  font-size: 0.75rem;
  color: rgba(0, 0, 0, 0.5);
  margin: 0.125rem 0 0;
}

/* Select Grid */
.apple-select-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.apple-select-wrap {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.apple-select-label {
  font-size: 0.6875rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.5);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.apple-select {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.85);
  background: rgba(0, 0, 0, 0.04);
  border: none;
  border-radius: 12px;
  appearance: none;
  cursor: pointer;
  transition: all 0.2s ease;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23666' d='M6 8L2 4h8z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.875rem center;
  padding-right: 2.5rem;
}

.apple-select:focus {
  outline: none;
  background-color: rgba(59, 130, 246, 0.08);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

/* Error Banner */
.apple-error-banner {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(239, 68, 68, 0.08);
  border-radius: 14px;
  color: #dc2626;
  margin-bottom: 1rem;
}

.apple-link-btn {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #2563eb;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  text-decoration: underline;
}

/* Loading State */
.apple-loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}

.apple-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(59, 130, 246, 0.2);
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: appleSpinner 0.8s linear infinite;
}

@keyframes appleSpinner {
  to { transform: rotate(360deg); }
}

.apple-loading-text {
  margin-top: 0.75rem;
  font-size: 0.8125rem;
  color: rgba(0, 0, 0, 0.5);
}

/* Activity List */
.apple-activities-container {
  max-height: 280px;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  background: #f5f5f7;
  border-radius: 14px;
  padding: 0.75rem;
  margin: -0.5rem 0 0 0;
}

/* macOS-style Scrollbar */
.apple-activities-container::-webkit-scrollbar {
  width: 6px;
}

.apple-activities-container::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 10px;
}

.apple-activities-container::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.15);
  border-radius: 10px;
  transition: background 0.2s ease;
}

.apple-activities-container::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.25);
}

.apple-activities-container::-webkit-scrollbar-thumb:active {
  background: rgba(0, 0, 0, 0.35);
}

/* Firefox scrollbar */
.apple-activities-container {
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 0, 0, 0.15) transparent;
}

.apple-activity-list {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.apple-activity-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.625rem 0.75rem;
  background: #ffffff;
  border-radius: 10px;
  transition: all 0.25s cubic-bezier(0.32, 0.72, 0, 1);
  border: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.apple-activity-item:hover {
  background: #ffffff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: rgba(0, 0, 0, 0.1);
}

.apple-activity-date {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.apple-date-day {
  font-size: 0.8125rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
}

.apple-date-time {
  font-size: 0.6875rem;
  color: rgba(0, 0, 0, 0.5);
}

.apple-type-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.1875rem 0.5rem;
  font-size: 0.625rem;
  font-weight: 600;
  border-radius: 100px;
}

.apple-badge-green {
  background: rgba(16, 185, 129, 0.12);
  color: #059669;
}

.apple-badge-purple {
  background: rgba(168, 85, 247, 0.12);
  color: #9333ea;
}

.apple-badge-blue {
  background: rgba(59, 130, 246, 0.12);
  color: #2563eb;
}

/* Empty State */
.apple-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}

.apple-empty-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.04);
  border-radius: 16px;
  color: rgba(0, 0, 0, 0.25);
  margin-bottom: 0.75rem;
}

.apple-empty-text {
  font-size: 0.8125rem;
  color: rgba(0, 0, 0, 0.45);
}

/* User Info Card */
.apple-user-info-card {
  background: linear-gradient(145deg, rgba(59, 130, 246, 0.08), rgba(59, 130, 246, 0.04));
  border-radius: 14px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.apple-user-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.apple-user-row + .apple-user-row {
  border-top: 0.5px solid rgba(0, 0, 0, 0.06);
}

.apple-info-label {
  font-size: 0.75rem;
  color: rgba(0, 0, 0, 0.5);
}

.apple-info-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
  text-align: right;
  max-width: 60%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.apple-info-value.apple-info-small {
  font-size: 0.75rem;
}

/* Format Options */
.apple-format-options {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  margin-bottom: 1rem;
}

.apple-format-option {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 0.875rem 1rem;
  background: rgba(0, 0, 0, 0.03);
  border: 2px solid transparent;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.apple-format-option:hover {
  background: rgba(0, 0, 0, 0.05);
}

.apple-format-selected {
  background: rgba(59, 130, 246, 0.06);
  border-color: #3b82f6;
}

.apple-format-radio {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(0, 0, 0, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.apple-format-selected .apple-format-radio {
  border-color: #3b82f6;
  background: #3b82f6;
}

.apple-format-check {
  width: 8px;
  height: 8px;
  background: white;
  border-radius: 50%;
  opacity: 0;
  transform: scale(0);
  transition: all 0.2s ease;
}

.apple-format-selected .apple-format-check {
  opacity: 1;
  transform: scale(1);
}

.apple-format-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  color: white;
  flex-shrink: 0;
}

.apple-format-pdf {
  background: linear-gradient(145deg, #ef4444, #dc2626);
}

.apple-format-csv {
  background: linear-gradient(145deg, #22c55e, #16a34a);
}

.apple-format-text {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.apple-format-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
}

.apple-format-desc {
  font-size: 0.75rem;
  color: rgba(0, 0, 0, 0.5);
}

/* Warning Banner */
.apple-warning-banner {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(245, 158, 11, 0.08);
  border-radius: 14px;
  margin-bottom: 1rem;
}

.apple-warning-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(245, 158, 11, 0.15);
  border-radius: 8px;
  color: #d97706;
  flex-shrink: 0;
}

.apple-warning-content {
  flex: 1;
  min-width: 0;
}

.apple-warning-title {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #92400e;
  margin: 0 0 0.25rem;
}

.apple-warning-text {
  font-size: 0.75rem;
  color: #b45309;
  line-height: 1.5;
  margin: 0;
}

/* Primary Button */
.apple-btn-primary {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  background: linear-gradient(145deg, #10b981, #059669);
  border: none;
  border-radius: 14px;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.9375rem;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
}

.apple-btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(5, 150, 105, 0.4);
}

.apple-btn-primary:active:not(:disabled) {
  transform: scale(0.98);
}

.apple-btn-disabled {
  background: linear-gradient(145deg, #9ca3af, #6b7280);
  cursor: not-allowed;
  box-shadow: none;
}

/* ================================================
   UNIFIED GENERATE CARD - FIRMAR Y GENERAR
   ================================================ */

/* ================================================
   REPORTE YA GENERADO - CARD DE ESTADO
   ================================================ */

.apple-generated-card {
  background: #ffffff;
  border: 1px solid rgba(16, 185, 129, 0.2);
  box-shadow: 
    0 4px 20px rgba(16, 185, 129, 0.1),
    0 2px 8px rgba(0, 0, 0, 0.04);
}

.apple-generated-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid rgba(16, 185, 129, 0.15);
}

.apple-generated-icon-wrap {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.apple-generated-icon {
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, #10b981, #059669);
  border-radius: 16px;
  color: white;
  z-index: 2;
  box-shadow: 
    0 4px 16px rgba(16, 185, 129, 0.4),
    0 2px 6px rgba(0, 0, 0, 0.1);
  animation: icon-success-pulse 2s ease-in-out infinite;
}

@keyframes icon-success-pulse {
  0%, 100% { 
    box-shadow: 0 4px 16px rgba(16, 185, 129, 0.4), 0 2px 6px rgba(0, 0, 0, 0.1);
    transform: scale(1);
  }
  50% { 
    box-shadow: 0 6px 24px rgba(16, 185, 129, 0.55), 0 3px 8px rgba(0, 0, 0, 0.08);
    transform: scale(1.02);
  }
}

.apple-generated-ring {
  position: absolute;
  width: 64px;
  height: 64px;
  border-radius: 20px;
  border: 2px solid rgba(16, 185, 129, 0.2);
  animation: ring-pulse 2.5s ease-out infinite;
}

@keyframes ring-pulse {
  0% { 
    opacity: 0.8;
    transform: scale(1);
  }
  100% { 
    opacity: 0;
    transform: scale(1.4);
  }
}

.apple-generated-title-group {
  flex: 1;
}

.apple-generated-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #065f46;
  margin: 0 0 0.25rem 0;
  letter-spacing: -0.02em;
}

.apple-generated-subtitle {
  font-size: 0.875rem;
  color: #059669;
  margin: 0;
  font-weight: 500;
  text-transform: capitalize;
}

.apple-generated-info {
  background: #f0fdf4;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1rem;
  border: 1px solid rgba(16, 185, 129, 0.15);
}

.apple-generated-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.625rem 0;
}

.apple-generated-row:not(:last-child) {
  border-bottom: 1px solid rgba(16, 185, 129, 0.08);
}

.apple-generated-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
  font-size: 0.8125rem;
  font-weight: 500;
}

.apple-generated-label svg {
  color: #10b981;
}

.apple-generated-value {
  color: #1f2937;
  font-size: 0.875rem;
  font-weight: 600;
}

/* Status Pills Small */
.apple-pill-sm {
  font-size: 0.6875rem;
  padding: 0.25rem 0.625rem;
}

.apple-pill-sm .apple-pill-dot {
  width: 5px;
  height: 5px;
}

/* Info Box */
.apple-info-box {
  display: flex;
  gap: 0.875rem;
  padding: 1rem;
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid rgba(59, 130, 246, 0.2);
  margin-bottom: 1.25rem;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.08);
}

.apple-info-box-icon {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(59, 130, 246, 0.15);
  border-radius: 8px;
  color: #3b82f6;
}

.apple-info-box-content {
  flex: 1;
}

.apple-info-box-title {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #1e40af;
  margin: 0 0 0.375rem 0;
}

.apple-info-box-text {
  font-size: 0.8125rem;
  color: #3b82f6;
  margin: 0;
  line-height: 1.5;
  font-weight: 450;
}

/* Actions del reporte generado */
.apple-generated-actions {
  display: flex;
  gap: 0.75rem;
}

.apple-action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: all 0.32s cubic-bezier(0.32, 0.72, 0, 1);
  font-family: inherit;
}

.apple-action-secondary {
  background: linear-gradient(145deg, 
    rgba(251, 146, 60, 0.15) 0%, 
    rgba(251, 146, 60, 0.1) 100%);
  color: #c2410c;
  border: 1px solid rgba(251, 146, 60, 0.25);
}

.apple-action-secondary:hover {
  background: linear-gradient(145deg, 
    rgba(251, 146, 60, 0.25) 0%, 
    rgba(251, 146, 60, 0.18) 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(251, 146, 60, 0.2);
}

.apple-action-secondary:active {
  transform: translateY(0);
}

.apple-action-contact {
  background: linear-gradient(145deg, 
    rgba(139, 92, 246, 0.15) 0%, 
    rgba(139, 92, 246, 0.1) 100%);
  color: #6d28d9;
  border: 1px solid rgba(139, 92, 246, 0.25);
}

.apple-action-contact:hover {
  background: linear-gradient(145deg, 
    rgba(139, 92, 246, 0.25) 0%, 
    rgba(139, 92, 246, 0.18) 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);
}

.apple-action-contact:active {
  transform: translateY(0);
}

/* Fade transition for cards */
.apple-fade-enter-active,
.apple-fade-leave-active {
  transition: all 0.4s cubic-bezier(0.32, 0.72, 0, 1);
}

.apple-fade-enter-from,
.apple-fade-leave-to {
  opacity: 0;
  transform: translateY(12px) scale(0.98);
}

.apple-fade-enter-to,
.apple-fade-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}

/* ================================================
   GENERATE CARD STYLES
   ================================================ */

.apple-generate-card {
  background: linear-gradient(145deg, 
    rgba(255, 255, 255, 0.95) 0%, 
    rgba(255, 255, 255, 0.88) 100%);
}

.apple-generate-header {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  margin-bottom: 1.25rem;
}

.apple-generate-icon-wrap {
  position: relative;
}

.apple-generate-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, #10b981, #059669);
  border-radius: 12px;
  color: white;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
}

.apple-generate-title-group {
  flex: 1;
}

.apple-generate-title {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
  font-size: 1.125rem;
  font-weight: 700;
  color: rgba(0, 0, 0, 0.88);
  margin: 0;
}

.apple-generate-subtitle {
  font-size: 0.8125rem;
  color: rgba(0, 0, 0, 0.45);
  margin: 0.125rem 0 0;
}

/* Steps Container */
.apple-steps-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.apple-step-card {
  display: flex;
  gap: 0.75rem;
  padding: 1.5rem;
  background: rgba(0, 0, 0, 0.03);
  border-radius: 14px;
  transition: all 0.3s cubic-bezier(0.32, 0.72, 0, 1);
}

@media (max-width: 768px) {
  .apple-step-card {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .apple-step-card {
    padding: 0.75rem;
  }
}

.apple-step-card.apple-step-completed {
  background: rgba(16, 185, 129, 0.08);
  border: 1px solid rgba(16, 185, 129, 0.15);
}

.apple-step-card.apple-step-active {
  background: rgba(59, 130, 246, 0.06);
}

.apple-step-number {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.08);
  border-radius: 50%;
  font-size: 0.8125rem;
  font-weight: 700;
  color: rgba(0, 0, 0, 0.5);
  flex-shrink: 0;
}

.apple-step-number.apple-step-done {
  background: linear-gradient(145deg, #10b981, #059669);
  color: white;
}

.apple-step-content {
  flex: 1;
  width: 100%;
}

.apple-step-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.apple-step-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.8);
}

.apple-step-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.1875rem 0.5rem;
  border-radius: 100px;
  font-size: 0.625rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.apple-badge-success {
  background: rgba(16, 185, 129, 0.15);
  color: #059669;
}

.apple-badge-pending {
  background: rgba(245, 158, 11, 0.12);
  color: #b45309;
}

.apple-firma-area {
  margin-top: 0.5rem;
  margin-left: calc(-0.75rem - 28px - 1.5rem);
  margin-right: -1.5rem;
  padding: 0;
  width: calc(100% + 0.75rem + 28px + 1.5rem + 1.5rem);
}

/* Layout especial para el step de firma */
.apple-step-firma-layout {
  flex-direction: column;
  gap: 0.75rem;
}

.apple-firma-header-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
}

.apple-firma-header-row .apple-step-header {
  flex: 1;
  margin-bottom: 0;
}

.apple-firma-area-full {
  width: 100%;
  margin-top: 0.25rem;
}

@media (max-width: 768px) {
  .apple-firma-area {
    margin-left: calc(-0.75rem - 28px - 1rem);
    margin-right: -1rem;
    width: calc(100% + 0.75rem + 28px + 1rem + 1rem);
  }
}

@media (max-width: 480px) {
  .apple-firma-area {
    margin-left: calc(-0.75rem - 28px - 0.75rem);
    margin-right: -0.75rem;
    width: calc(100% + 0.75rem + 28px + 0.75rem + 0.75rem);
  }
}

/* Format Row */
.apple-format-row {
  display: flex;
  gap: 0.5rem;
}

.apple-format-chip {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  padding: 0.625rem 0.75rem;
  background: rgba(0, 0, 0, 0.04);
  border: 2px solid transparent;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.8125rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.6);
}

.apple-format-chip:hover {
  background: rgba(0, 0, 0, 0.06);
}

.apple-format-chip.apple-chip-active {
  background: rgba(59, 130, 246, 0.1);
  border-color: #3b82f6;
  color: #2563eb;
}

/* Signer Strip */
.apple-signer-strip {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.75rem;
  background: rgba(0, 0, 0, 0.03);
  border-radius: 12px;
  margin-bottom: 0.75rem;
}

.apple-signer-avatar-sm {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, #6366f1, #4f46e5);
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.apple-signer-details {
  flex: 1;
  min-width: 0;
}

.apple-signer-name-sm {
  display: block;
  font-size: 0.8125rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.8);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.apple-signer-meta {
  display: block;
  font-size: 0.6875rem;
  color: rgba(0, 0, 0, 0.45);
}

/* Inline Warning */
.apple-inline-warning {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 0.75rem;
  background: rgba(245, 158, 11, 0.1);
  border-radius: 10px;
  color: #b45309;
  font-size: 0.75rem;
  font-weight: 500;
  margin-bottom: 0.75rem;
}

/* Unified Generate Button */
.apple-btn-generate-unified {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: linear-gradient(145deg, #9ca3af, #6b7280);
  border: none;
  border-radius: 14px;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.9375rem;
  font-weight: 600;
  color: white;
  cursor: not-allowed;
  transition: all 0.3s cubic-bezier(0.32, 0.72, 0, 1);
  box-shadow: none;
}

.apple-btn-generate-unified.apple-btn-ready {
  background: linear-gradient(145deg, #10b981, #059669);
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(16, 185, 129, 0.35);
}

.apple-btn-generate-unified.apple-btn-ready:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4);
}

.apple-btn-generate-unified.apple-btn-ready:active {
  transform: scale(0.98) translateY(0);
}

.apple-btn-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: appleSpinner 0.8s linear infinite;
}

/* Refresh Button */
.apple-refresh-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.04);
  border: none;
  border-radius: 10px;
  color: rgba(0, 0, 0, 0.5);
  cursor: pointer;
  transition: all 0.2s ease;
}

.apple-refresh-btn:hover:not(:disabled) {
  background: rgba(0, 0, 0, 0.08);
  color: rgba(0, 0, 0, 0.7);
}

.apple-refresh-btn:disabled {
  opacity: 0.5;
}

/* Error State */
.apple-error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1.5rem 1rem;
  text-align: center;
  color: #dc2626;
}

.apple-error-text {
  font-size: 0.8125rem;
  margin: 0.5rem 0;
}

/* Reports List */
.apple-reports-list {
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
}

.apple-report-card {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid;
  border-radius: 16px;
  padding: 1rem;
  transition: all 0.2s ease;
}

.apple-report-signed {
  border-color: rgba(16, 185, 129, 0.3);
  background: linear-gradient(145deg, rgba(16, 185, 129, 0.04), rgba(16, 185, 129, 0.02));
}

.apple-report-pending {
  border-color: rgba(245, 158, 11, 0.3);
  background: linear-gradient(145deg, rgba(245, 158, 11, 0.04), rgba(245, 158, 11, 0.02));
}

.apple-report-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.apple-report-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  color: white;
  flex-shrink: 0;
}

.apple-report-info {
  flex: 1;
  min-width: 0;
}

.apple-report-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.apple-report-date {
  font-size: 0.75rem;
  color: rgba(0, 0, 0, 0.5);
  margin: 0.125rem 0 0;
}

.apple-report-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.625rem;
  font-size: 0.6875rem;
  font-weight: 700;
  border-radius: 8px;
  flex-shrink: 0;
}

.apple-badge-red {
  background: rgba(239, 68, 68, 0.12);
  color: #dc2626;
}

.apple-badge-green-alt {
  background: rgba(34, 197, 94, 0.12);
  color: #16a34a;
}

/* Status Banner */
.apple-status-banner {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 12px;
  margin-bottom: 0.75rem;
}

.apple-status-success {
  background: rgba(16, 185, 129, 0.1);
}

.apple-status-warning {
  background: rgba(245, 158, 11, 0.1);
}

.apple-status-icon {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: white;
  flex-shrink: 0;
}

.apple-status-success .apple-status-icon {
  background: #10b981;
}

.apple-status-warning .apple-status-icon {
  background: #f59e0b;
}

.apple-status-text {
  flex: 1;
  min-width: 0;
}

.apple-status-title {
  font-size: 0.8125rem;
  font-weight: 600;
  margin: 0;
}

.apple-status-success .apple-status-title {
  color: #047857;
}

.apple-status-warning .apple-status-title {
  color: #92400e;
}

.apple-status-subtitle {
  font-size: 0.75rem;
  margin: 0.125rem 0 0;
}

.apple-status-success .apple-status-subtitle {
  color: #059669;
}

.apple-status-warning .apple-status-subtitle {
  color: #b45309;
}

/* Action Buttons */
.apple-report-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.apple-action-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.apple-action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.apple-action-view {
  background: rgba(168, 85, 247, 0.1);
  color: #9333ea;
}

.apple-action-view:hover:not(:disabled) {
  background: rgba(168, 85, 247, 0.18);
}

.apple-action-download {
  background: rgba(59, 130, 246, 0.1);
  color: #2563eb;
}

.apple-action-download:hover:not(:disabled) {
  background: rgba(59, 130, 246, 0.18);
}

.apple-action-delete {
  background: rgba(239, 68, 68, 0.1);
  color: #dc2626;
}

.apple-action-delete:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.18);
}

.apple-action-locked {
  background: rgba(0, 0, 0, 0.05);
  color: rgba(0, 0, 0, 0.4);
  cursor: not-allowed;
}

.apple-btn-spinner-sm {
  width: 14px;
  height: 14px;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: appleSpinner 0.8s linear infinite;
  opacity: 0.7;
}

/* Confirm Modal */
.apple-confirm-overlay {
  position: fixed;
  inset: 0;
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.apple-confirm-modal {
  width: 100%;
  max-width: 280px;
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
}

.apple-confirm-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.apple-confirm-danger {
  background: rgba(239, 68, 68, 0.12);
  color: #dc2626;
}

.apple-confirm-title {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
  font-size: 1.0625rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.9);
  margin: 0 0 0.25rem;
}

.apple-confirm-subtitle {
  font-size: 0.8125rem;
  color: rgba(0, 0, 0, 0.5);
  margin: 0 0 1.25rem;
}

.apple-confirm-actions {
  display: flex;
  gap: 0.625rem;
}

.apple-confirm-btn {
  flex: 1;
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.apple-confirm-cancel {
  background: rgba(0, 0, 0, 0.06);
  color: rgba(0, 0, 0, 0.65);
}

.apple-confirm-cancel:hover {
  background: rgba(0, 0, 0, 0.1);
}

.apple-confirm-delete {
  background: linear-gradient(145deg, #ef4444, #dc2626);
  color: white;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

.apple-confirm-delete:hover {
  box-shadow: 0 6px 16px rgba(220, 38, 38, 0.4);
}

/* Modal Transitions */
.apple-modal-enter-active {
  animation: appleOverlayIn 0.35s cubic-bezier(0.32, 0.72, 0, 1) forwards;
}

.apple-modal-leave-active {
  animation: appleOverlayOut 0.25s cubic-bezier(0.32, 0.72, 0, 1) forwards;
}

@keyframes appleOverlayIn {
  0% { opacity: 0; }
  100% { opacity: 1; }
}

@keyframes appleOverlayOut {
  0% { opacity: 1; }
  100% { opacity: 0; }
}

.apple-modal-content-enter-active {
  animation: appleModalIn 0.45s cubic-bezier(0.32, 0.72, 0, 1) forwards;
}

.apple-modal-content-leave-active {
  animation: appleModalOut 0.25s cubic-bezier(0.32, 0.72, 0, 1) forwards;
}

@keyframes appleModalIn {
  0% {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes appleModalOut {
  0% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
  100% {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
  }
}

/* Modal Fade for existing modals */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

/* ================================================
   APPLE MODAL - GENERAR REPORTE
   ================================================ */

.apple-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 10000;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

@media (min-width: 640px) {
  .apple-modal-overlay {
    align-items: center;
    padding: 1.5rem;
  }
}

.apple-modal-container {
  width: 100%;
  max-width: 400px;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(40px) saturate(200%);
  -webkit-backdrop-filter: blur(40px) saturate(200%);
  border-radius: 24px 24px 0 0;
  box-shadow: 
    0 -1px 0 rgba(255, 255, 255, 0.5),
    0 25px 80px rgba(0, 0, 0, 0.35);
  overflow: hidden;
  max-height: calc(100vh - 40px);
  display: flex;
  flex-direction: column;
}

@media (min-width: 640px) {
  .apple-modal-container {
    border-radius: 24px;
    max-height: 85vh;
    box-shadow: 
      0 0 0 1px rgba(0, 0, 0, 0.05),
      0 25px 80px rgba(0, 0, 0, 0.25);
  }
}

.apple-modal-handle {
  width: 36px;
  height: 5px;
  background: rgba(0, 0, 0, 0.15);
  border-radius: 100px;
  margin: 8px auto 0;
  flex-shrink: 0;
}

@media (min-width: 640px) {
  .apple-modal-handle {
    display: none;
  }
}

.apple-modal-header {
  padding: 1.5rem 1.5rem 1rem;
  text-align: center;
  flex-shrink: 0;
}

.apple-modal-icon-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.apple-modal-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  color: white;
  animation: appleIconPulse 2s ease-in-out infinite;
}

.apple-modal-icon-gradient {
  background: linear-gradient(145deg, #a855f7, #6366f1);
  box-shadow: 
    0 8px 24px rgba(139, 92, 246, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.2) inset;
}

@keyframes appleIconPulse {
  0%, 100% { transform: scale(1); box-shadow: 0 8px 24px rgba(139, 92, 246, 0.4); }
  50% { transform: scale(1.02); box-shadow: 0 12px 32px rgba(139, 92, 246, 0.5); }
}

.apple-modal-title {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
  font-size: 1.375rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  color: rgba(0, 0, 0, 0.9);
  margin: 0 0 0.25rem;
}

.apple-modal-subtitle {
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.5);
  margin: 0;
}

.apple-modal-body {
  padding: 0 1.5rem;
  overflow-y: auto;
  flex: 1;
  -webkit-overflow-scrolling: touch;
}

/* Info Card */
.apple-modal-info-card {
  background: rgba(0, 0, 0, 0.03);
  border-radius: 16px;
  padding: 0.25rem;
  margin-bottom: 1rem;
}

.apple-modal-info-row {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 0.875rem 1rem;
}

.apple-modal-info-divider {
  height: 0.5px;
  background: rgba(0, 0, 0, 0.08);
  margin: 0 1rem;
}

.apple-modal-info-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  color: white;
  flex-shrink: 0;
}

.apple-modal-info-content {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  flex: 1;
  min-width: 0;
}

.apple-modal-info-label {
  font-size: 0.75rem;
  color: rgba(0, 0, 0, 0.5);
}

.apple-modal-info-value {
  font-size: 0.9375rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
}

/* Signer Card */
.apple-modal-signer-card {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 1rem;
  background: linear-gradient(145deg, rgba(139, 92, 246, 0.08), rgba(99, 102, 241, 0.05));
  border-radius: 16px;
  margin-bottom: 1rem;
}

.apple-modal-signer-avatar {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, #a855f7, #6366f1);
  border-radius: 50%;
  color: white;
  font-weight: 700;
  font-size: 0.9375rem;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

.apple-modal-signer-info {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  flex: 1;
  min-width: 0;
}

.apple-modal-signer-name {
  font-size: 0.9375rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.apple-modal-signer-email {
  font-size: 0.8125rem;
  color: rgba(0, 0, 0, 0.5);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.apple-modal-signer-badge {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(16, 185, 129, 0.15);
  border-radius: 50%;
  color: #059669;
  flex-shrink: 0;
}

/* Notice */
.apple-modal-notice {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  background: rgba(245, 158, 11, 0.08);
  border-radius: 14px;
  margin-bottom: 1rem;
}

.apple-modal-notice-icon {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(245, 158, 11, 0.15);
  border-radius: 50%;
  color: #d97706;
  flex-shrink: 0;
}

.apple-modal-notice-text {
  font-size: 0.8125rem;
  color: #92400e;
  line-height: 1.5;
  margin: 0;
}

/* Confirmación de firma realizada */
.apple-modal-confirmed {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 1rem;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 14px;
}

.apple-confirmed-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, #10b981, #059669);
  border-radius: 50%;
  color: white;
  flex-shrink: 0;
  animation: checkPop 0.4s cubic-bezier(0.32, 0.72, 0, 1);
}

@keyframes checkPop {
  0% { transform: scale(0); }
  60% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.apple-confirmed-text {
  font-size: 0.8125rem;
  color: #047857;
  line-height: 1.5;
  margin: 0;
}

/* Checkbox Apple */
.apple-modal-checkbox {
  display: flex;
  align-items: flex-start;
  gap: 0.875rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.03);
  border: 2px solid transparent;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.32, 0.72, 0, 1);
  margin-bottom: 0.5rem;
}

.apple-modal-checkbox:hover {
  background: rgba(0, 0, 0, 0.05);
}

.apple-modal-checkbox-checked {
  background: rgba(139, 92, 246, 0.08);
  border-color: #a855f7;
}

.apple-checkbox-indicator {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  flex-shrink: 0;
  transition: all 0.25s cubic-bezier(0.32, 0.72, 0, 1);
}

.apple-modal-checkbox-checked .apple-checkbox-indicator {
  background: linear-gradient(145deg, #a855f7, #6366f1);
  border-color: transparent;
  color: white;
}

.apple-checkbox-text {
  font-size: 0.8125rem;
  color: rgba(0, 0, 0, 0.7);
  line-height: 1.5;
  padding-top: 0.125rem;
}

/* Footer */
.apple-modal-footer {
  padding: 1rem 1.5rem 1.5rem;
  display: flex;
  gap: 0.75rem;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.8);
}

@media (min-width: 640px) {
  .apple-modal-footer {
    padding-bottom: 1.5rem;
  }
}

.apple-modal-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1.25rem;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.9375rem;
  font-weight: 600;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.32, 0.72, 0, 1);
}

.apple-modal-btn-secondary {
  background: rgba(0, 0, 0, 0.06);
  color: rgba(0, 0, 0, 0.65);
}

.apple-modal-btn-secondary:hover:not(:disabled) {
  background: rgba(0, 0, 0, 0.1);
}

.apple-modal-btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.apple-modal-btn-primary {
  background: linear-gradient(145deg, #a855f7, #6366f1);
  color: white;
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.4);
}

.apple-modal-btn-primary:hover:not(:disabled):not(.apple-modal-btn-disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5);
}

.apple-modal-btn-primary:active:not(:disabled):not(.apple-modal-btn-disabled) {
  transform: scale(0.98);
}

.apple-modal-btn-disabled {
  background: linear-gradient(145deg, #9ca3af, #6b7280);
  cursor: not-allowed;
  box-shadow: none;
}

.apple-modal-btn-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: appleSpinner 0.8s linear infinite;
}

/* Safe area for mobile */
@supports (padding-bottom: env(safe-area-inset-bottom)) {
  .apple-modal-footer {
    padding-bottom: calc(1.5rem + env(safe-area-inset-bottom));
  }
}
</style>
