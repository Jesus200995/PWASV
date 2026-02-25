<template>
  <div class="estadisticas-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
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
              <h1 class="header-title">📊 Estadísticas de Dispositivos</h1>
              <p class="header-subtitle">Análisis de plataformas utilizadas por los usuarios</p>
            </div>
          </div>
          <div class="header-actions">
            <button class="btn-refresh" @click="cargarEstadisticas" :disabled="cargando">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M23 4v6h-6"/>
                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
              </svg>
              Actualizar
            </button>
          </div>
        </div>
      </header>

      <div class="page-content">
        <!-- Mensaje de carga -->
        <div v-if="cargando" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Cargando estadísticas...</p>
        </div>

        <!-- Mensaje de error -->
        <div v-if="error && !cargando" class="error-state">
          <div class="error-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
        <div v-if="!cargando && !error && estadisticas" class="estadisticas-grid">
          
          <!-- Tarjeta de Total de Usuarios -->
          <div class="stat-card total-card">
            <div class="stat-icon total-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </div>
            <div class="stat-content">
              <h3 class="stat-label">Total de Usuarios</h3>
              <p class="stat-value total-value">{{ estadisticas.total_usuarios.toLocaleString() }}</p>
            </div>
          </div>

          <!-- Tarjetas por Dispositivo -->
          <div 
            v-for="dispositivo in estadisticas.por_dispositivo" 
            :key="dispositivo.dispositivo"
            class="stat-card"
            :class="`card-${dispositivo.dispositivo.toLowerCase()}`"
          >
            <div class="stat-icon" :class="`icon-${dispositivo.dispositivo.toLowerCase()}`">
              <span class="device-emoji">{{ getIconoDispositivo(dispositivo.dispositivo) }}</span>
            </div>
            <div class="stat-content">
              <h3 class="stat-label">{{ dispositivo.dispositivo }}</h3>
              <p class="stat-value">{{ dispositivo.cantidad.toLocaleString() }}</p>
              <div class="stat-progress">
                <div 
                  class="progress-bar" 
                  :class="`progress-${dispositivo.dispositivo.toLowerCase()}`"
                  :style="{ width: dispositivo.porcentaje + '%' }"
                >
                  <span class="progress-label">{{ dispositivo.porcentaje }}%</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Gráfica de Dona (Distribución General) -->
          <div class="chart-card donut-card">
            <div class="chart-header">
              <h3 class="chart-title">📱 Distribución por Plataforma</h3>
            </div>
            <div class="chart-content">
              <div class="donut-chart">
                <svg viewBox="0 0 200 200" class="donut-svg">
                  <circle
                    v-for="(dispositivo, index) in estadisticas.por_dispositivo"
                    :key="dispositivo.dispositivo"
                    cx="100"
                    cy="100"
                    r="70"
                    fill="none"
                    :stroke="getColorDispositivo(dispositivo.dispositivo)"
                    stroke-width="40"
                    :stroke-dasharray="`${getCircunferencia(dispositivo.porcentaje)} ${440 - getCircunferencia(dispositivo.porcentaje)}`"
                    :stroke-dashoffset="getOffset(index)"
                    class="donut-segment"
                    :class="`segment-${dispositivo.dispositivo.toLowerCase()}`"
                  />
                  <text x="100" y="95" text-anchor="middle" class="donut-total-label">Total</text>
                  <text x="100" y="115" text-anchor="middle" class="donut-total-value">
                    {{ estadisticas.total_usuarios }}
                  </text>
                </svg>
              </div>
              <div class="donut-legend">
                <div 
                  v-for="dispositivo in estadisticas.por_dispositivo"
                  :key="dispositivo.dispositivo"
                  class="legend-item"
                >
                  <div 
                    class="legend-color" 
                    :style="{ backgroundColor: getColorDispositivo(dispositivo.dispositivo) }"
                  ></div>
                  <span class="legend-label">
                    {{ getIconoDispositivo(dispositivo.dispositivo) }} {{ dispositivo.dispositivo }}
                  </span>
                  <span class="legend-value">{{ dispositivo.cantidad }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Gráfica de Barras (Por Rol) -->
          <div class="chart-card bars-card">
            <div class="chart-header">
              <h3 class="chart-title">👥 Distribución por Rol</h3>
            </div>
            <div class="chart-content">
              <div class="bars-chart">
                <div 
                  v-for="rol in getRolesSummary()"
                  :key="rol.nombre"
                  class="bar-group"
                >
                  <div class="bar-label">{{ rol.nombre }}</div>
                  <div class="bar-container">
                    <div class="bar-wrapper">
                      <div 
                        v-for="dispositivo in rol.dispositivos"
                        :key="dispositivo.tipo"
                        class="bar-segment"
                        :class="`bar-${dispositivo.tipo.toLowerCase()}`"
                        :style="{ 
                          width: (dispositivo.cantidad / rol.total * 100) + '%',
                          backgroundColor: getColorDispositivo(dispositivo.tipo)
                        }"
                        :title="`${dispositivo.tipo}: ${dispositivo.cantidad}`"
                      >
                        <span v-if="dispositivo.cantidad > 0" class="bar-value">{{ dispositivo.cantidad }}</span>
                      </div>
                    </div>
                    <span class="bar-total">{{ rol.total }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Usuarios Activos (Últimos 30 días) -->
          <div class="chart-card active-users-card">
            <div class="chart-header">
              <h3 class="chart-title">🔥 Usuarios Activos (30 días)</h3>
            </div>
            <div class="chart-content">
              <div v-if="estadisticas.activos_30_dias && estadisticas.activos_30_dias.length > 0">
                <div class="active-stats">
                  <div class="active-total">
                    <span class="active-number">{{ getTotalActivos() }}</span>
                    <span class="active-label">usuarios activos</span>
                  </div>
                  <div class="active-percentage">
                    {{ ((getTotalActivos() / estadisticas.total_usuarios) * 100).toFixed(1) }}%
                    <span class="percentage-label">del total</span>
                  </div>
                </div>
                <div class="active-devices">
                  <div 
                    v-for="activo in estadisticas.activos_30_dias"
                    :key="activo.dispositivo"
                    class="active-device-item"
                  >
                    <span class="active-emoji">{{ getIconoDispositivo(activo.dispositivo) }}</span>
                    <span class="active-device-name">{{ activo.dispositivo }}</span>
                    <span class="active-device-count">{{ activo.cantidad }}</span>
                  </div>
                </div>
              </div>
              <div v-else class="no-active-data">
                <p>No hay datos de usuarios activos en los últimos 30 días</p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import Sidebar from '../components/Sidebar.vue';
import { obtenerEstadisticasDispositivos } from '../services/dispositivosService.js';

const router = useRouter();
const estadisticas = ref(null);
const cargando = ref(false);
const error = ref('');

// Cargar estadísticas
async function cargarEstadisticas() {
  cargando.value = true;
  error.value = '';
  
  try {
    estadisticas.value = await obtenerEstadisticasDispositivos();
    console.log('📊 Estadísticas cargadas:', estadisticas.value);
  } catch (err) {
    console.error('Error al cargar estadísticas:', err);
    error.value = 'No se pudieron cargar las estadísticas. Por favor, intenta de nuevo.';
  } finally {
    cargando.value = false;
  }
}

// Iconos por dispositivo
function getIconoDispositivo(dispositivo) {
  const iconos = {
    'Android': '🤖',
    'iOS': '🍎',
    'Desktop': '💻',
    'desconocido': '❓'
  };
  return iconos[dispositivo] || '📱';
}

// Colores por dispositivo
function getColorDispositivo(dispositivo) {
  const colores = {
    'Android': '#3DDC84',
    'iOS': '#147EFB',
    'Desktop': '#6B7280',
    'desconocido': '#9CA3AF'
  };
  return colores[dispositivo] || '#9CA3AF';
}

// Calcular circunferencia para gráfica de dona
function getCircunferencia(porcentaje) {
  const radio = 70;
  const circunferencia = 2 * Math.PI * radio;
  return (porcentaje / 100) * circunferencia;
}

// Calcular offset para gráfica de dona
function getOffset(index) {
  if (!estadisticas.value || index === 0) return 0;
  
  let offset = 0;
  for (let i = 0; i < index; i++) {
    offset += getCircunferencia(estadisticas.value.por_dispositivo[i].porcentaje);
  }
  return -offset;
}

// Obtener resumen por roles
function getRolesSummary() {
  if (!estadisticas.value || !estadisticas.value.por_rol) return [];
  
  const roles = {};
  estadisticas.value.por_rol.forEach(item => {
    if (!roles[item.rol]) {
      roles[item.rol] = {
        nombre: item.rol,
        total: 0,
        dispositivos: []
      };
    }
    roles[item.rol].total += item.cantidad;
    roles[item.rol].dispositivos.push({
      tipo: item.dispositivo,
      cantidad: item.cantidad
    });
  });
  
  return Object.values(roles);
}

// Obtener total de usuarios activos
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

// Cargar al montar
onMounted(() => {
  cargarEstadisticas();
  
  // Auto-refresh cada 30 segundos
  const interval = setInterval(() => {
    cargarEstadisticas();
  }, 30000);
  
  // Limpiar interval al desmontar
  return () => clearInterval(interval);
});
</script>

<style scoped>
/* Contenedor principal */
.estadisticas-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* Contenido principal */
.main-content {
  flex: 1;
  margin-left: 280px;
  transition: margin-left 0.3s ease;
}

@media (max-width: 1024px) {
  .main-content {
    margin-left: 80px;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }
}

/* Header de página */
.page-header {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 1.5rem 2rem;
  position: sticky;
  top: 0;
  z-index: 10;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-main {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 6px rgba(34, 197, 94, 0.3);
}

.header-icon svg {
  width: 24px;
  height: 24px;
}

.header-text {
  flex: 1;
}

.header-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.header-subtitle {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0.25rem 0 0;
}

.header-actions {
  display: flex;
  gap: 0.75rem;
}

/* Botones */
.btn-refresh {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  color: #374151;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-refresh:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #22c55e;
  color: #22c55e;
}

.btn-refresh:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  color: #374151;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

/* Contenido de página */
.page-content {
  padding: 2rem;
}

/* Estados de carga y error */
.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top-color: #22c55e;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-icon {
  width: 64px;
  height: 64px;
  background: #fee2e2;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.error-icon svg {
  width: 32px;
  height: 32px;
  color: #dc2626;
}

.error-state h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 0.5rem;
}

.error-state p {
  color: #6b7280;
  margin: 0 0 1.5rem;
}

/* Grid de estadísticas */
.estadisticas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

@media (min-width: 1280px) {
  .estadisticas-grid {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .total-card {
    grid-column: span 4;
  }
  
  .donut-card {
    grid-column: span 2;
  }
  
  .bars-card {
    grid-column: span 2;
  }
  
  .active-users-card {
    grid-column: span 4;
  }
}

/* Tarjetas de estadísticas */
.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.total-card {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  flex-shrink: 0;
}

.total-icon {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.total-icon svg {
  width: 28px;
  height: 28px;
}

.card-android .stat-icon { background: #e8f8f0; }
.card-ios .stat-icon { background: #e8f4ff; }
.card-desktop .stat-icon { background: #f3f4f6; }
.card-desconocido .stat-icon { background: #f9fafb; }

.device-emoji {
  font-size: 2rem;
  line-height: 1;
}

.stat-content {
  flex: 1;
  min-width: 0;
}

.stat-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  margin: 0 0 0.5rem;
  text-transform: capitalize;
}

.total-card .stat-label {
  color: rgba(255, 255, 255, 0.9);
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
  line-height: 1;
}

.total-value {
  color: white;
  font-size: 2.5rem;
}

/* Barra de progreso */
.stat-progress {
  margin-top: 1rem;
  background: #f3f4f6;
  border-radius: 999px;
  height: 8px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: 999px;
  transition: width 0.6s ease;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 0.5rem;
  position: relative;
}

.progress-android { background: #3DDC84; }
.progress-ios { background: #147EFB; }
.progress-desktop { background: #6B7280; }
.progress-desconocido { background: #9CA3AF; }

.progress-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

/* Tarjetas de gráficas */
.chart-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-header {
  margin-bottom: 1.5rem;
}

.chart-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

/* Gráfica de Dona */
.donut-chart {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.donut-svg {
  width: 200px;
  height: 200px;
  transform: rotate(-90deg);
}

.donut-segment {
  transition: stroke-width 0.3s;
}

.donut-segment:hover {
  stroke-width: 45;
}

.donut-total-label {
  font-size: 14px;
  fill: #6b7280;
  font-weight: 500;
}

.donut-total-value {
  font-size: 24px;
  fill: #111827;
  font-weight: 700;
}

/* Leyenda */
.donut-legend {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  flex-shrink: 0;
}

.legend-label {
  flex: 1;
  font-size: 0.875rem;
  color: #374151;
}

.legend-value {
  font-weight: 600;
  color: #111827;
}

/* Gráfica de Barras */
.bars-chart {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.bar-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.bar-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  text-transform: capitalize;
}

.bar-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.bar-wrapper {
  flex: 1;
  display: flex;
  height: 32px;
  background: #f3f4f6;
  border-radius: 6px;
  overflow: hidden;
}

.bar-segment {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  position: relative;
}

.bar-segment:hover {
  filter: brightness(1.1);
}

.bar-value {
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.bar-total {
  font-size: 0.875rem;
  font-weight: 600;
  color: #111827;
  min-width: 40px;
  text-align: right;
}

/* Usuarios Activos */
.active-stats {
  display: flex;
  justify-content: space-around;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-radius: 12px;
}

.active-total {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.active-number {
  font-size: 3rem;
  font-weight: 700;
  color: #16a34a;
  line-height: 1;
}

.active-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 0.5rem;
}

.active-percentage {
  font-size: 2rem;
  font-weight: 700;
  color: #22c55e;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.percentage-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  margin-top: 0.25rem;
}

.active-devices {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.active-device-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.active-emoji {
  font-size: 1.5rem;
}

.active-device-name {
  flex: 1;
  font-weight: 500;
  color: #374151;
  text-transform: capitalize;
}

.active-device-count {
  font-weight: 700;
  color: #111827;
  font-size: 1.125rem;
}

.no-active-data {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    padding: 1rem;
  }
  
  .header-title {
    font-size: 1.25rem;
  }
  
  .page-content {
    padding: 1rem;
  }
  
  .estadisticas-grid {
    grid-template-columns: 1fr;
  }
  
  .active-stats {
    flex-direction: column;
    gap: 1.5rem;
  }
}
</style>
