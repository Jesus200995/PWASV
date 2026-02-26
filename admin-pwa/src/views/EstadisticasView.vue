<template>
  <div class="estadisticas-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 20V10"/>
                <path d="M12 20V4"/>
                <path d="M6 20v-6"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Panel de Estadísticas</h1>
              <p class="header-subtitle">Usuarios, actividad, dispositivos y distribución de cargos</p>
            </div>
          </div>
          <div class="header-actions">
            <div v-if="actualizando" class="updating-indicator">
              <svg class="spin-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M23 4v6h-6"/>
                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
              </svg>
              <span>Actualizando...</span>
            </div>
            <button class="btn-refresh" @click="cargarEstadisticas" :disabled="cargando || actualizando">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ 'spin-icon': actualizando }">
                <path d="M23 4v6h-6"/>
                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
              </svg>
              Actualizar
            </button>
          </div>
        </div>
      </header>

      <div class="page-content">
        <!-- Loading -->
        <div v-if="cargando" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Cargando estadísticas...</p>
        </div>

        <!-- Error -->
        <div v-if="error && !cargando" class="error-state">
          <div class="error-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="8" x2="12" y2="12"/>
              <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
          </div>
          <h3>Error al cargar estadísticas</h3>
          <p>{{ error }}</p>
          <button class="btn-secondary" @click="cargarEstadisticas">Reintentar</button>
        </div>

        <!-- Estadísticas -->
        <div v-if="!cargando && !error && estadisticas" class="stats-wrapper">
          
          <!-- Tarjeta Principal -->
          <section class="main-stat-card animate-fade-in">
            <div class="main-stat-glow"></div>
            <div class="main-stat-content">
              <div class="main-stat-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                </svg>
              </div>
              <div class="main-stat-info">
                <span class="main-stat-label">Usuarios en la Plataforma</span>
                <div class="main-stat-value-wrapper">
                  <span class="main-stat-value">{{ usuariosActivos.toLocaleString() }}</span>
                  <span class="main-stat-divider">/</span>
                  <span class="main-stat-total">{{ estadisticas.total_usuarios.toLocaleString() }}</span>
                </div>
                <span class="main-stat-desc">Activos de {{ estadisticas.total_usuarios.toLocaleString() }} registrados</span>
              </div>
              <div class="main-stat-trend">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
                  <polyline points="17 6 23 6 23 12"/>
                </svg>
              </div>
            </div>
          </section>

          <!-- Grid de Dispositivos -->
          <section class="devices-section">
            <div 
              v-for="(dispositivo, index) in estadisticas.por_dispositivo" 
              :key="dispositivo.dispositivo"
              class="device-card animate-slide-up"
              :class="`device-${dispositivo.dispositivo.toLowerCase()}`"
              :style="{ animationDelay: `${index * 0.1}s` }"
            >
              <div class="device-header">
                <div class="device-icon-wrapper" :class="`bg-${dispositivo.dispositivo.toLowerCase()}`">
                  <!-- Android Icon -->
                  <svg v-if="dispositivo.dispositivo.toLowerCase() === 'android'" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M17.532 15.106a1.003 1.003 0 1 1 .001-2.007 1.003 1.003 0 0 1-.001 2.007zm-11.044 0a1.003 1.003 0 1 1 .001-2.007 1.003 1.003 0 0 1-.001 2.007zm11.4-6.018l2.006-3.459a.413.413 0 1 0-.721-.407l-2.027 3.5a12.243 12.243 0 0 0-5.13-1.108c-1.85 0-3.595.398-5.141 1.098l-2.027-3.49a.413.413 0 1 0-.72.407l1.995 3.458C2.696 10.947.345 14.417 0 18.523h24c-.347-4.106-2.696-7.576-6.112-9.435z"/>
                  </svg>
                  <!-- iOS Icon -->
                  <svg v-else-if="dispositivo.dispositivo.toLowerCase() === 'ios'" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
                  </svg>
                  <!-- Desktop Icon -->
                  <svg v-else-if="dispositivo.dispositivo.toLowerCase() === 'desktop'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="2" y="3" width="20" height="14" rx="2"/>
                    <line x1="8" y1="21" x2="16" y2="21"/>
                    <line x1="12" y1="17" x2="12" y2="21"/>
                  </svg>
                  <!-- Unknown Icon -->
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
                    <line x1="12" y1="17" x2="12.01" y2="17"/>
                  </svg>
                </div>
                <div class="device-data">
                  <h4 class="device-name">{{ capitalizar(dispositivo.dispositivo) }}</h4>
                  <p class="device-count">{{ dispositivo.cantidad.toLocaleString() }} usuarios</p>
                </div>
              </div>
              <div class="device-progress-container">
                <div class="progress-bar-track">
                  <div 
                    class="progress-bar-fill"
                    :class="`fill-${dispositivo.dispositivo.toLowerCase()}`"
                    :style="{ width: dispositivo.porcentaje + '%' }"
                  >
                    <div class="progress-shine"></div>
                  </div>
                </div>
                <span class="progress-percent">{{ dispositivo.porcentaje }}%</span>
              </div>
            </div>
          </section>

          <!-- Gráficas en 2 columnas -->
          <section class="charts-row">
            <!-- Gráfica de Dona -->
            <div class="chart-card donut-chart-card animate-fade-in" style="animation-delay: 0.3s">
              <div class="chart-card-header">
                <div class="chart-header-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 2a10 10 0 0 1 7.07 17.07"/>
                  </svg>
                </div>
                <h3 class="chart-card-title">Distribución por Plataforma</h3>
              </div>
              <div class="chart-card-body">
                <div class="donut-wrapper">
                  <svg viewBox="0 0 200 200" class="donut-svg">
                    <circle
                      v-for="(dispositivo, index) in estadisticas.por_dispositivo"
                      :key="dispositivo.dispositivo"
                      cx="100"
                      cy="100"
                      r="70"
                      fill="none"
                      :stroke="getColorDispositivo(dispositivo.dispositivo)"
                      stroke-width="35"
                      :stroke-dasharray="`${getCircunferencia(dispositivo.porcentaje)} ${440 - getCircunferencia(dispositivo.porcentaje)}`"
                      :stroke-dashoffset="getOffset(index)"
                      class="donut-ring"
                    />
                    <circle cx="100" cy="100" r="50" fill="white"/>
                    <text x="100" y="95" text-anchor="middle" class="donut-center-label">Total</text>
                    <text x="100" y="115" text-anchor="middle" class="donut-center-value">{{ estadisticas.total_usuarios }}</text>
                  </svg>
                </div>
                <div class="donut-legend">
                  <div 
                    v-for="dispositivo in estadisticas.por_dispositivo"
                    :key="dispositivo.dispositivo"
                    class="donut-legend-item"
                  >
                    <span class="legend-dot" :style="{ backgroundColor: getColorDispositivo(dispositivo.dispositivo) }"></span>
                    <span class="legend-name">{{ capitalizar(dispositivo.dispositivo) }}</span>
                    <span class="legend-qty">{{ dispositivo.cantidad }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Gráfica Compacta por Cargo -->
            <div class="chart-card cargo-chart-card animate-fade-in" style="animation-delay: 0.4s">
              <div class="chart-card-header">
                <div class="chart-header-icon cargo-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="2" y="7" width="20" height="14" rx="2" ry="2"/>
                    <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
                  </svg>
                </div>
                <h3 class="chart-card-title">Distribución por Cargo</h3>
              </div>
              <div class="chart-card-body">
                <div v-if="estadisticas.por_cargo && estadisticas.por_cargo.length > 0" class="cargo-compact-list">
                  <div 
                    v-for="(cargo, idx) in estadisticas.por_cargo"
                    :key="cargo.cargo"
                    class="cargo-compact-item"
                  >
                    <div class="cargo-compact-header">
                      <div class="cargo-compact-icon" :style="{ background: getCargoGradient(idx) }">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                          <circle cx="12" cy="7" r="4"/>
                          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                        </svg>
                      </div>
                      <div class="cargo-compact-info">
                        <span class="cargo-compact-name">{{ capitalizar(cargo.cargo) }}</span>
                        <span class="cargo-compact-count">{{ cargo.cantidad.toLocaleString() }} usuarios</span>
                      </div>
                      <span class="cargo-compact-percent" :style="{ color: getCargoColor(idx) }">{{ cargo.porcentaje }}%</span>
                    </div>
                    <div class="cargo-compact-bar-track">
                      <div 
                        class="cargo-compact-bar-fill"
                        :style="{ 
                          width: cargo.porcentaje + '%',
                          background: getCargoGradient(idx)
                        }"
                      >
                        <div class="cargo-bar-shine"></div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="no-cargo-data">
                  <p>No hay datos de cargos disponibles</p>
                </div>
              </div>
            </div>
          </section>

          <!-- Estado de Usuarios (Activos/Inactivos) -->
          <section class="status-section animate-fade-in" style="animation-delay: 0.5s">
            <div class="status-row">
              <!-- Gráfica de Estado -->
              <div class="chart-card status-chart-card">
                <div class="chart-card-header">
                  <div class="chart-header-icon status-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                      <polyline points="22 4 12 14.01 9 11.01"/>
                    </svg>
                  </div>
                  <h3 class="chart-card-title">Estado de Usuarios</h3>
                </div>
                <div class="chart-card-body">
                  <div v-if="estadisticas.estado_usuarios && estadisticas.estado_usuarios.length > 0" class="status-chart-content">
                    <div class="status-donut-wrapper">
                      <svg viewBox="0 0 200 200" class="status-donut-svg">
                        <circle
                          v-for="(estado, index) in estadisticas.estado_usuarios"
                          :key="estado.estado"
                          cx="100"
                          cy="100"
                          r="70"
                          fill="none"
                          :stroke="getColorEstado(estado.estado)"
                          stroke-width="35"
                          :stroke-dasharray="`${getCircunferencia(estado.porcentaje)} ${440 - getCircunferencia(estado.porcentaje)}`"
                          :stroke-dashoffset="getOffsetEstado(index)"
                          class="status-ring"
                        />
                        <circle cx="100" cy="100" r="50" fill="white"/>
                        <text x="100" y="95" text-anchor="middle" class="status-center-label">Total</text>
                        <text x="100" y="115" text-anchor="middle" class="status-center-value">{{ estadisticas.total_usuarios }}</text>
                      </svg>
                    </div>
                    <div class="status-legend">
                      <div 
                        v-for="estado in estadisticas.estado_usuarios"
                        :key="estado.estado"
                        class="status-legend-item"
                        :class="estado.estado === 'Activos' ? 'legend-active' : 'legend-inactive'"
                      >
                        <div class="legend-icon-wrapper">
                          <svg v-if="estado.estado === 'Activos'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                            <polyline points="22 4 12 14.01 9 11.01"/>
                          </svg>
                          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                            <circle cx="12" cy="12" r="10"/>
                            <line x1="15" y1="9" x2="9" y2="15"/>
                            <line x1="9" y1="9" x2="15" y2="15"/>
                          </svg>
                        </div>
                        <div class="legend-info">
                          <span class="legend-estado">{{ estado.estado }}</span>
                          <span class="legend-porcentaje">{{ estado.porcentaje }}%</span>
                        </div>
                        <span class="legend-cantidad">{{ estado.cantidad.toLocaleString() }}</span>
                      </div>
                    </div>
                  </div>
                  <div v-else class="no-status-data">
                    <p>No hay datos de estado de usuarios</p>
                  </div>
                </div>
              </div>

              <!-- Actividad Reciente (30 días) -->
              <div class="chart-card recent-activity-card">
                <div class="chart-card-header">
                  <div class="chart-header-icon pulse-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                    </svg>
                  </div>
                  <h3 class="chart-card-title">Actividad Reciente (30 días)</h3>
                </div>
                <div class="chart-card-body">
                  <div v-if="estadisticas.activos_30_dias && estadisticas.activos_30_dias.length > 0" class="active-content">
                    <div class="active-summary">
                      <div class="active-stat-box">
                        <div class="active-number-wrapper">
                          <span class="active-big-number">{{ usuariosActivos.toLocaleString() }}</span>
                          <span class="active-divider">/</span>
                          <span class="active-total-small">{{ estadisticas.total_usuarios.toLocaleString() }}</span>
                        </div>
                        <span class="active-stat-label">usuarios activos</span>
                      </div>
                      <div class="active-stat-box">
                        <span class="active-big-percent">{{ porcentajeActivos.toFixed(1) }}%</span>
                        <span class="active-stat-label">del total</span>
                      </div>
                    </div>
                    <div class="active-by-device">
                      <div 
                        v-for="activo in estadisticas.activos_30_dias"
                        :key="activo.dispositivo"
                        class="active-device-chip"
                        :class="`chip-${activo.dispositivo.toLowerCase()}`"
                      >
                        <!-- Icon based on device -->
                        <svg v-if="activo.dispositivo.toLowerCase() === 'android'" viewBox="0 0 24 24" fill="currentColor" class="chip-icon">
                          <path d="M17.532 15.106a1.003 1.003 0 1 1 .001-2.007 1.003 1.003 0 0 1-.001 2.007zm-11.044 0a1.003 1.003 0 1 1 .001-2.007 1.003 1.003 0 0 1-.001 2.007zm11.4-6.018l2.006-3.459a.413.413 0 1 0-.721-.407l-2.027 3.5a12.243 12.243 0 0 0-5.13-1.108c-1.85 0-3.595.398-5.141 1.098l-2.027-3.49a.413.413 0 1 0-.72.407l1.995 3.458C2.696 10.947.345 14.417 0 18.523h24c-.347-4.106-2.696-7.576-6.112-9.435z"/>
                        </svg>
                        <svg v-else-if="activo.dispositivo.toLowerCase() === 'ios'" viewBox="0 0 24 24" fill="currentColor" class="chip-icon">
                          <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
                        </svg>
                        <svg v-else-if="activo.dispositivo.toLowerCase() === 'desktop'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="chip-icon">
                          <rect x="2" y="3" width="20" height="14" rx="2"/>
                          <line x1="8" y1="21" x2="16" y2="21"/>
                          <line x1="12" y1="17" x2="12" y2="21"/>
                        </svg>
                        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="chip-icon">
                          <circle cx="12" cy="12" r="10"/>
                          <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
                          <line x1="12" y1="17" x2="12.01" y2="17"/>
                        </svg>
                        <span class="chip-name">{{ capitalizar(activo.dispositivo) }}</span>
                        <span class="chip-count">{{ activo.cantidad }}</span>
                      </div>
                    </div>
                  </div>
                  <div v-else class="no-active-data">
                    <p>No hay datos de actividad reciente</p>
                  </div>
                </div>
              </div>
            </div>
          </section>

        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import Sidebar from '../components/Sidebar.vue';
import { obtenerEstadisticasDispositivos } from '../services/dispositivosService.js';

const router = useRouter();
const estadisticas = ref(null);
const cargando = ref(false);
const actualizando = ref(false);
const error = ref('');
const primeraVez = ref(true);
let intervaloActualizacion = null;

// Computed para usuarios activos
const usuariosActivos = computed(() => {
  if (!estadisticas.value || !estadisticas.value.estado_usuarios) return 0;
  const activos = estadisticas.value.estado_usuarios.find(e => e.estado === 'Activos');
  return activos ? activos.cantidad : 0;
});

// Computed para porcentaje de usuarios activos
const porcentajeActivos = computed(() => {
  if (!estadisticas.value || !estadisticas.value.total_usuarios) return 0;
  return (usuariosActivos.value / estadisticas.value.total_usuarios) * 100;
});

// Cargar estadísticas (reactivo sin recargar página)
async function cargarEstadisticas() {
  // Solo mostrar loading completo en la primera carga
  if (primeraVez.value) {
    cargando.value = true;
  } else {
    actualizando.value = true;
  }
  error.value = '';
  
  try {
    const nuevosData = await obtenerEstadisticasDispositivos();
    // Actualizar de forma reactiva sin reemplazar todo el objeto
    if (estadisticas.value) {
      // Actualizar cada propiedad individualmente para reactividad suave
      estadisticas.value.total_usuarios = nuevosData.total_usuarios;
      estadisticas.value.por_dispositivo = nuevosData.por_dispositivo;
      estadisticas.value.por_cargo = nuevosData.por_cargo;
      estadisticas.value.activos_30_dias = nuevosData.activos_30_dias;
      estadisticas.value.estado_usuarios = nuevosData.estado_usuarios;
    } else {
      estadisticas.value = nuevosData;
    }
    console.log('Estadísticas actualizadas:', estadisticas.value);
  } catch (err) {
    console.error('Error al cargar estadísticas:', err);
    // Solo mostrar error si es la primera carga
    if (primeraVez.value) {
      error.value = 'No se pudieron cargar las estadísticas. Por favor, intenta de nuevo.';
    }
  } finally {
    cargando.value = false;
    actualizando.value = false;
    primeraVez.value = false;
  }
}

// Capitalizar primera letra
function capitalizar(texto) {
  if (!texto) return '';
  return texto.charAt(0).toUpperCase() + texto.slice(1).toLowerCase();
}

// Colores por dispositivo
function getColorDispositivo(dispositivo) {
  const colores = {
    'android': '#3DDC84',
    'ios': '#007AFF',
    'desktop': '#6366F1',
    'desconocido': '#94A3B8'
  };
  return colores[dispositivo?.toLowerCase()] || '#94A3B8';
}

// Calcular circunferencia
function getCircunferencia(porcentaje) {
  const radio = 70;
  const circunferencia = 2 * Math.PI * radio;
  return (porcentaje / 100) * circunferencia;
}

// Calcular offset
function getOffset(index) {
  if (!estadisticas.value || index === 0) return 0;
  let offset = 0;
  for (let i = 0; i < index; i++) {
    offset += getCircunferencia(estadisticas.value.por_dispositivo[i].porcentaje);
  }
  return -offset;
}

// Colores para estado de usuarios
function getColorEstado(estado) {
  return estado === 'Activos' ? '#10B981' : '#EF4444';
}

// Calcular offset para gráfica de estados
function getOffsetEstado(index) {
  if (!estadisticas.value || !estadisticas.value.estado_usuarios || index === 0) return 0;
  let offset = 0;
  for (let i = 0; i < index; i++) {
    offset += getCircunferencia(estadisticas.value.estado_usuarios[i].porcentaje);
  }
  return -offset;
}

// Colores para cargos
function getCargoColor(index) {
  const colores = ['#8B5CF6', '#06B6D4', '#F59E0B', '#EC4899', '#10B981', '#6366F1', '#EF4444', '#14B8A6', '#F97316', '#84CC16'];
  return colores[index % colores.length];
}

// Gradientes para cargos
function getCargoGradient(index) {
  const gradientes = [
    'linear-gradient(135deg, #8B5CF6, #7C3AED)',
    'linear-gradient(135deg, #06B6D4, #0891B2)',
    'linear-gradient(135deg, #F59E0B, #D97706)',
    'linear-gradient(135deg, #EC4899, #DB2777)',
    'linear-gradient(135deg, #10B981, #059669)',
    'linear-gradient(135deg, #6366F1, #4F46E5)',
    'linear-gradient(135deg, #EF4444, #DC2626)',
    'linear-gradient(135deg, #14B8A6, #0D9488)',
    'linear-gradient(135deg, #F97316, #EA580C)',
    'linear-gradient(135deg, #84CC16, #65A30D)'
  ];
  return gradientes[index % gradientes.length];
}

// Total activos
function getTotalActivos() {
  if (!estadisticas.value || !estadisticas.value.activos_30_dias) return 0;
  return estadisticas.value.activos_30_dias.reduce((sum, item) => sum + item.cantidad, 0);
}

// Logout
function logout() {
  localStorage.removeItem('admin_token');
  localStorage.removeItem('admin_user');
  router.push('/login');
}

onMounted(() => {
  cargarEstadisticas();
  // Actualizar cada 30 segundos de forma silenciosa
  intervaloActualizacion = setInterval(() => cargarEstadisticas(), 30000);
});

onUnmounted(() => {
  if (intervaloActualizacion) {
    clearInterval(intervaloActualizacion);
  }
});
</script>

<style scoped>
/* === ANIMATIONS === */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

@keyframes shine {
  0% { left: -100%; }
  100% { left: 100%; }
}

@keyframes glow {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 0.8; }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
  opacity: 0;
}

.animate-slide-up {
  animation: slideUp 0.5s ease-out forwards;
  opacity: 0;
}

/* === CONTAINER === */
.estadisticas-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%);
}

.main-content {
  flex: 1;
  margin-left: min(220px, 18vw);
  width: calc(100vw - min(220px, 18vw));
  min-width: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  transition: all 0.3s ease;
}

/* === HEADER === */
.page-header {
  background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
  color: white;
  padding: clamp(0.4rem, 1vw, 0.6rem) clamp(1rem, 2vw, 1.5rem);
  box-shadow: 0 4px 20px rgba(76, 175, 80, 0.3);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.header-main {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-icon {
  width: 36px;
  height: 36px;
  background: rgba(255,255,255,0.2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-icon svg {
  width: 20px;
  height: 20px;
}

.header-title {
  font-size: clamp(14px, 2.5vw, 18px);
  font-weight: 700;
  margin: 0;
}

.header-subtitle {
  font-size: clamp(10px, 1.5vw, 12px);
  opacity: 0.9;
  margin: 2px 0 0;
}

.btn-refresh {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: rgba(255,255,255,0.2);
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 10px;
  color: white;
  font-weight: 600;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-refresh:hover:not(:disabled) {
  background: rgba(255,255,255,0.3);
  transform: translateY(-2px);
}

.btn-refresh:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.updating-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: rgba(34, 197, 94, 0.2);
  border: 1px solid rgba(34, 197, 94, 0.4);
  border-radius: 8px;
  color: #86efac;
  font-size: 11px;
  font-weight: 500;
  animation: pulse 1.5s ease-in-out infinite;
}

.spin-icon {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* === PAGE CONTENT === */
.page-content {
  flex: 1;
  padding: clamp(16px, 2.5vw, 24px);
}

.stats-wrapper {
  display: flex;
  flex-direction: column;
  gap: clamp(16px, 2.5vw, 24px);
}

/* === LOADING/ERROR === */
.loading-state, .error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e0e0e0;
  border-top-color: #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.error-icon {
  width: 64px;
  height: 64px;
  background: #fee2e2;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.error-icon svg {
  width: 32px;
  height: 32px;
  color: #dc2626;
}

.btn-secondary {
  padding: 10px 20px;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

/* === MAIN STAT CARD === */
.main-stat-card {
  background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
  border-radius: 20px;
  padding: clamp(24px, 3vw, 36px);
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 10px 40px rgba(76, 175, 80, 0.3),
    0 4px 12px rgba(0,0,0,0.1);
}

.main-stat-glow {
  position: absolute;
  top: -50%;
  right: -20%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
  animation: glow 3s ease-in-out infinite;
}

.main-stat-content {
  display: flex;
  align-items: center;
  gap: clamp(16px, 3vw, 32px);
  position: relative;
  z-index: 1;
}

.main-stat-icon {
  width: clamp(60px, 8vw, 80px);
  height: clamp(60px, 8vw, 80px);
  background: rgba(255,255,255,0.2);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.main-stat-icon svg {
  width: 50%;
  height: 50%;
  color: white;
}

.main-stat-info {
  flex: 1;
  color: white;
}

.main-stat-label {
  display: block;
  font-size: clamp(11px, 1.5vw, 13px);
  text-transform: uppercase;
  letter-spacing: 1px;
  opacity: 0.9;
  margin-bottom: 4px;
}

.main-stat-value-wrapper {
  display: flex;
  align-items: baseline;
  gap: 4px;
  margin-bottom: 4px;
}

.main-stat-value {
  font-size: clamp(36px, 6vw, 56px);
  font-weight: 800;
  line-height: 1;
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.main-stat-value:hover {
  transform: scale(1.02);
}

.main-stat-divider {
  font-size: clamp(20px, 3vw, 28px);
  font-weight: 300;
  opacity: 0.5;
  margin: 0 2px;
  transform: rotate(-15deg);
  display: inline-block;
}

.main-stat-total {
  font-size: clamp(18px, 2.5vw, 24px);
  font-weight: 600;
  opacity: 0.6;
  position: relative;
  top: -2px;
}

.main-stat-desc {
  display: block;
  font-size: clamp(11px, 1.5vw, 13px);
  opacity: 0.85;
}

.main-stat-trend {
  width: 48px;
  height: 48px;
  background: rgba(255,255,255,0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-stat-trend svg {
  width: 24px;
  height: 24px;
  color: white;
}

/* === DEVICES SECTION === */
.devices-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: clamp(12px, 2vw, 20px);
}

.device-card {
  background: white;
  border-radius: 16px;
  padding: clamp(18px, 2.5vw, 24px);
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid transparent;
}

.device-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 32px rgba(0,0,0,0.12);
}

.device-card.device-android:hover { border-color: #3DDC84; }
.device-card.device-ios:hover { border-color: #007AFF; }
.device-card.device-desktop:hover { border-color: #6366F1; }
.device-card.device-desconocido:hover { border-color: #94A3B8; }

.device-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 18px;
}

.device-icon-wrapper {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
}

.device-card:hover .device-icon-wrapper {
  transform: scale(1.1) rotate(5deg);
}

.device-icon-wrapper svg {
  width: 26px;
  height: 26px;
  color: white;
}

.device-icon-wrapper.bg-android { background: linear-gradient(135deg, #3DDC84, #2BC470); }
.device-icon-wrapper.bg-ios { background: linear-gradient(135deg, #007AFF, #0056B3); }
.device-icon-wrapper.bg-desktop { background: linear-gradient(135deg, #6366F1, #4F46E5); }
.device-icon-wrapper.bg-desconocido { background: linear-gradient(135deg, #94A3B8, #64748B); }

.device-data {
  flex: 1;
}

.device-name {
  font-size: clamp(15px, 2vw, 17px);
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 4px;
}

.device-count {
  font-size: clamp(12px, 1.6vw, 13px);
  color: #64748b;
  margin: 0;
}

/* === PROGRESS BAR === */
.device-progress-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-bar-track {
  flex: 1;
  height: 12px;
  background: #f1f5f9;
  border-radius: 20px;
  overflow: hidden;
  position: relative;
}

.progress-bar-fill {
  height: 100%;
  border-radius: 20px;
  position: relative;
  transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.progress-bar-fill.fill-android { background: linear-gradient(90deg, #3DDC84, #2BC470); }
.progress-bar-fill.fill-ios { background: linear-gradient(90deg, #007AFF, #0056B3); }
.progress-bar-fill.fill-desktop { background: linear-gradient(90deg, #6366F1, #4F46E5); }
.progress-bar-fill.fill-desconocido { background: linear-gradient(90deg, #94A3B8, #64748B); }

.progress-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  animation: shine 2s infinite;
}

.progress-percent {
  font-size: clamp(12px, 1.6vw, 14px);
  font-weight: 700;
  color: #475569;
  min-width: 45px;
  text-align: right;
}

/* === CHARTS ROW (2 COLUMNS) === */
.charts-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: clamp(16px, 2.5vw, 24px);
}

@media (max-width: 900px) {
  .charts-row {
    grid-template-columns: 1fr;
  }
}

/* === CHART CARD === */
.chart-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  overflow: hidden;
  transition: all 0.3s ease;
}

.chart-card:hover {
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.chart-card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: clamp(16px, 2vw, 20px);
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  border-bottom: 1px solid #e2e8f0;
}

.chart-header-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #4CAF50, #2E7D32);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-header-icon svg {
  width: 20px;
  height: 20px;
  color: white;
}

.chart-header-icon.pulse-icon {
  animation: pulse 2s ease-in-out infinite;
}

.chart-card-title {
  font-size: clamp(14px, 2vw, 16px);
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.chart-card-body {
  padding: clamp(16px, 2.5vw, 24px);
}

/* === DONUT CHART === */
.donut-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.donut-svg {
  width: 180px;
  height: 180px;
  transform: rotate(-90deg);
}

.donut-ring {
  transition: all 0.5s ease;
  cursor: pointer;
}

.donut-ring:hover {
  stroke-width: 40;
  filter: brightness(1.1);
}

.donut-center-label {
  font-size: 14px;
  fill: #64748b;
  font-weight: 500;
  transform: rotate(90deg);
  transform-origin: 100px 100px;
}

.donut-center-value {
  font-size: 22px;
  fill: #1e293b;
  font-weight: 800;
  transform: rotate(90deg);
  transform-origin: 100px 100px;
}

.donut-legend {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.donut-legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  background: #f8fafc;
  border-radius: 10px;
  transition: all 0.2s ease;
}

.donut-legend-item:hover {
  background: #f1f5f9;
  transform: translateX(4px);
}

.legend-dot {
  width: 14px;
  height: 14px;
  border-radius: 4px;
}

.legend-name {
  flex: 1;
  font-size: 14px;
  font-weight: 600;
  color: #334155;
}

.legend-qty {
  font-size: 14px;
  font-weight: 700;
  color: #1e293b;
}

/* === CARGO CHART COMPACT === */
.cargo-icon {
  background: linear-gradient(135deg, #8B5CF6, #7C3AED) !important;
}

.cargo-compact-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 320px;
  overflow-y: auto;
  padding-right: 8px;
}

.cargo-compact-list::-webkit-scrollbar {
  width: 6px;
}

.cargo-compact-list::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.cargo-compact-list::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #8B5CF6, #7C3AED);
  border-radius: 10px;
}

.cargo-compact-list::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #7C3AED, #6D28D9);
}

.cargo-compact-item {
  background: linear-gradient(135deg, #fafbfc, #f8fafc);
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 12px 14px;
  transition: all 0.3s ease;
}

.cargo-compact-item:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  border-color: #c7d2fe;
}

.cargo-compact-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.cargo-compact-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.cargo-compact-icon svg {
  width: 16px;
  height: 16px;
  color: white;
}

.cargo-compact-info {
  flex: 1;
  min-width: 0;
}

.cargo-compact-name {
  display: block;
  font-size: 13px;
  font-weight: 700;
  color: #1e293b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cargo-compact-count {
  display: block;
  font-size: 11px;
  color: #64748b;
}

.cargo-compact-percent {
  font-size: 15px;
  font-weight: 800;
  flex-shrink: 0;
}

.cargo-compact-bar-track {
  height: 8px;
  background: #f1f5f9;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.cargo-compact-bar-fill {
  height: 100%;
  border-radius: 8px;
  position: relative;
  transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.cargo-bar-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  animation: shine 2s infinite;
}

.no-cargo-data {
  text-align: center;
  padding: 30px 20px;
  color: #64748b;
}

/* === ACTIVE USERS === */
.active-section {
  width: 100%;
}

.active-card {
  width: 100%;
}

.active-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.active-summary {
  display: flex;
  justify-content: center;
  gap: clamp(24px, 5vw, 48px);
  padding: clamp(20px, 3vw, 32px);
  background: linear-gradient(135deg, #ecfdf5, #d1fae5);
  border-radius: 16px;
}

.active-stat-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.active-number-wrapper {
  display: flex;
  align-items: baseline;
  gap: 3px;
}

.active-big-number {
  font-size: clamp(36px, 5vw, 52px);
  font-weight: 800;
  color: #059669;
  line-height: 1;
}

.active-divider {
  font-size: clamp(18px, 2.5vw, 24px);
  font-weight: 300;
  color: #94a3b8;
  transform: rotate(-15deg);
  display: inline-block;
  margin: 0 2px;
}

.active-total-small {
  font-size: clamp(16px, 2vw, 20px);
  font-weight: 600;
  color: #94a3b8;
  position: relative;
  top: -2px;
}

.active-big-percent {
  font-size: clamp(32px, 4.5vw, 44px);
  font-weight: 800;
  color: #10b981;
  line-height: 1;
}

.active-stat-label {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.15));
  border: 1px solid rgba(16, 185, 129, 0.25);
  border-radius: 12px;
  font-size: 10px;
  color: #047857;
  font-weight: 600;
  letter-spacing: 0.2px;
  text-transform: uppercase;
  box-shadow: 0 1px 4px rgba(16, 185, 129, 0.1);
}

.active-by-device {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
}

.active-device-chip {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 18px;
  background: white;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;
}

.active-device-chip:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}

.active-device-chip.chip-android:hover { border-color: #3DDC84; }
.active-device-chip.chip-ios:hover { border-color: #007AFF; }
.active-device-chip.chip-desktop:hover { border-color: #6366F1; }
.active-device-chip.chip-desconocido:hover { border-color: #94A3B8; }

.chip-icon {
  width: 22px;
  height: 22px;
  color: #64748b;
}

.chip-android .chip-icon { color: #3DDC84; }
.chip-ios .chip-icon { color: #007AFF; }
.chip-desktop .chip-icon { color: #6366F1; }

.chip-name {
  font-size: 14px;
  font-weight: 600;
  color: #475569;
}

.chip-count {
  font-size: 16px;
  font-weight: 800;
  color: #1e293b;
  background: #f1f5f9;
  padding: 4px 10px;
  border-radius: 8px;
}

.no-active-data {
  text-align: center;
  padding: 40px 20px;
  color: #64748b;
}

/* === STATUS SECTION === */
.status-section {
  width: 100%;
}

.status-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: clamp(16px, 2.5vw, 24px);
}

@media (max-width: 900px) {
  .status-row {
    grid-template-columns: 1fr;
  }
}

.status-chart-card,
.recent-activity-card {
  height: 100%;
}

.status-icon {
  background: linear-gradient(135deg, #10B981, #059669) !important;
}

.status-chart-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.status-donut-wrapper {
  display: flex;
  justify-content: center;
}

.status-donut-svg {
  width: 180px;
  height: 180px;
  transform: rotate(-90deg);
}

.status-ring {
  transition: all 0.5s ease;
  cursor: pointer;
}

.status-ring:hover {
  stroke-width: 40;
  filter: brightness(1.1);
}

.status-center-label {
  font-size: 14px;
  fill: #64748b;
  font-weight: 500;
  transform: rotate(90deg);
  transform-origin: 100px 100px;
}

.status-center-value {
  font-size: 22px;
  fill: #1e293b;
  font-weight: 800;
  transform: rotate(90deg);
  transform-origin: 100px 100px;
}

.status-legend {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.status-legend-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.status-legend-item.legend-active {
  background: linear-gradient(135deg, #ecfdf5, #d1fae5);
  border: 2px solid #10B981;
}

.status-legend-item.legend-inactive {
  background: linear-gradient(135deg, #fef2f2, #fee2e2);
  border: 2px solid #EF4444;
}

.status-legend-item:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.legend-icon-wrapper {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.legend-active .legend-icon-wrapper {
  background: #10B981;
}

.legend-inactive .legend-icon-wrapper {
  background: #EF4444;
}

.legend-icon-wrapper svg {
  width: 20px;
  height: 20px;
  color: white;
}

.legend-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.legend-estado {
  font-size: 15px;
  font-weight: 700;
  color: #1e293b;
}

.legend-porcentaje {
  font-size: 13px;
  color: #64748b;
}

.legend-cantidad {
  font-size: 20px;
  font-weight: 800;
  color: #1e293b;
}

.no-status-data {
  text-align: center;
  padding: 40px 20px;
  color: #64748b;
}

/* === RESPONSIVE === */
@media (max-width: 992px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 240px;
    width: calc(100vw - 240px);
  }
  
  .main-stat-content {
    flex-direction: column;
    text-align: center;
  }
  
  .main-stat-trend {
    display: none;
  }
  
  .devices-section {
    grid-template-columns: 1fr;
  }
  
  .active-summary {
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }
}

@media (max-width: 480px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }
  
  .devices-section {
    grid-template-columns: 1fr;
  }
  
  .donut-svg {
    width: 150px;
    height: 150px;
  }
}
</style>
