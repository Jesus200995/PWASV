<template>
  <div class="reportes-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="20" x2="18" y2="10"/>
                <line x1="12" y1="20" x2="12" y2="4"/>
                <line x1="6" y1="20" x2="6" y2="14"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Gestión de Reportes</h1>
              <p class="header-subtitle">Genera y consulta reportes de actividades y estadísticas</p>
            </div>
          </div>
          <div class="header-actions">
            <button @click="actualizarReportes" class="refresh-btn" :disabled="loading">
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
        <!-- Sección de Generación de Reportes -->
        <div class="reportes-section">
          <div class="reportes-card">
            <div class="reportes-header">
              <h3>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                </svg>
                Generar Reporte
              </h3>
            </div>
            <div class="reportes-content">
              <div class="form-row">
                <div class="form-field">
                  <label>Tipo de Reporte</label>
                  <select v-model="tipoReporte" class="form-select">
                    <option value="">Selecciona un tipo</option>
                    <option value="usuarios">Usuarios</option>
                    <option value="asistencias">Asistencias</option>
                    <option value="actividades">Actividades</option>
                    <option value="territorios">Por Territorio</option>
                  </select>
                </div>
                <div class="form-field">
                  <label>Formato</label>
                  <select v-model="formatoReporte" class="form-select">
                    <option value="excel">Excel (.xlsx)</option>
                    <option value="pdf">PDF</option>
                    <option value="csv">CSV</option>
                  </select>
                </div>
              </div>

              <div class="form-row">
                <div class="form-field">
                  <label>Fecha Inicio</label>
                  <input v-model="fechaInicio" type="date" class="form-input" />
                </div>
                <div class="form-field">
                  <label>Fecha Fin</label>
                  <input v-model="fechaFin" type="date" class="form-input" />
                </div>
              </div>

              <div class="action-buttons">
                <button @click="generarReporte" class="btn-generate" :disabled="!tipoReporte || generando">
                  <svg v-if="!generando" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                  </svg>
                  <div v-else class="spinner-small"></div>
                  {{ generando ? 'Generando...' : 'Generar Reporte' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Sección de Reportes Generados -->
        <div v-if="reportesGenerados.length > 0" class="reportes-list-section">
          <div class="reportes-card">
            <div class="reportes-header">
              <h3>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                  <polyline points="22,6 12,13 2,6"/>
                </svg>
                Reportes Generados
              </h3>
            </div>
            <div class="reportes-table-container">
              <table class="reportes-table">
                <thead>
                  <tr>
                    <th>Tipo</th>
                    <th>Formato</th>
                    <th>Fecha Generación</th>
                    <th>Período</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="reporte in reportesGenerados" :key="reporte.id">
                    <td>{{ reporte.tipo }}</td>
                    <td><span class="badge-formato">{{ reporte.formato }}</span></td>
                    <td>{{ formatearFecha(reporte.fechaGeneracion) }}</td>
                    <td>{{ reporte.periodo }}</td>
                    <td>
                      <button @click="descargarReporte(reporte)" class="btn-action download">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                          <polyline points="7 10 12 15 17 10"/>
                          <line x1="12" y1="15" x2="12" y2="3"/>
                        </svg>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Estado Vacío -->
        <div v-else class="empty-state">
          <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
          </svg>
          <p class="empty-title">No hay reportes generados</p>
          <p class="empty-subtitle">Selecciona los parámetros y genera tu primer reporte</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Sidebar from '../components/Sidebar.vue'

const router = useRouter()

// Estado
const loading = ref(false)
const generando = ref(false)
const tipoReporte = ref('')
const formatoReporte = ref('excel')
const fechaInicio = ref('')
const fechaFin = ref('')
const reportesGenerados = ref([])

// Inicializar fechas por defecto (último mes)
onMounted(() => {
  const hoy = new Date()
  const hace30Dias = new Date(hoy)
  hace30Dias.setDate(hoy.getDate() - 30)
  
  fechaFin.value = hoy.toISOString().split('T')[0]
  fechaInicio.value = hace30Dias.toISOString().split('T')[0]
})

// Funciones
const actualizarReportes = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 1000)
}

const generarReporte = async () => {
  if (!tipoReporte.value) return
  
  generando.value = true
  
  try {
    // Simular generación de reporte
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Agregar reporte a la lista
    const nuevoReporte = {
      id: Date.now(),
      tipo: tipoReporte.value.charAt(0).toUpperCase() + tipoReporte.value.slice(1),
      formato: formatoReporte.value.toUpperCase(),
      fechaGeneracion: new Date().toISOString(),
      periodo: `${fechaInicio.value} a ${fechaFin.value}`
    }
    
    reportesGenerados.value.unshift(nuevoReporte)
    
    alert('Reporte generado exitosamente')
  } catch (error) {
    console.error('Error generando reporte:', error)
    alert('Error al generar el reporte')
  } finally {
    generando.value = false
  }
}

const descargarReporte = (reporte) => {
  alert(`Descargando reporte: ${reporte.tipo} (${reporte.formato})`)
  // Aquí iría la lógica de descarga real
}

const formatearFecha = (fecha) => {
  return new Date(fecha).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const logout = () => {
  localStorage.removeItem('adminToken')
  router.push('/login')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

.reportes-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
}

.main-content {
  flex: 1;
  margin-left: min(220px, 18vw);
  width: calc(100vw - min(220px, 18vw));
  background: linear-gradient(135deg, #f8f9fa 0%, #f0fff0 100%);
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

.header-actions {
  display: flex;
  gap: clamp(0.25rem, 0.5vw, 0.4rem);
  align-items: center;
  margin-right: clamp(0.3rem, 1vw, 0.6rem);
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: clamp(0.2rem, 0.4vw, 0.3rem);
  padding: clamp(0.25rem, 0.5vw, 0.35rem) clamp(0.5rem, 1vw, 0.7rem);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 50px;
  font-size: clamp(10px, 1.9vw, 12px);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: 'Inter', sans-serif;
  white-space: nowrap;
  box-shadow: 
    0 2px 4px rgba(0, 0, 0, 0.1),
    inset 0 -1px 0 rgba(0, 0, 0, 0.1);
}

.refresh-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.35) 0%, rgba(255, 255, 255, 0.25) 100%);
  transform: translateY(-1px);
  box-shadow: 
    0 4px 8px rgba(0, 0, 0, 0.15),
    inset 0 -1px 0 rgba(0, 0, 0, 0.1);
}

.refresh-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.refresh-icon {
  width: clamp(11px, 2vw, 13px);
  height: clamp(11px, 2vw, 13px);
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* === CONTENT STYLES === */
.page-content {
  flex: 1;
  padding: 16px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.reportes-section,
.reportes-list-section {
  margin-bottom: 16px;
}

.reportes-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  overflow: hidden;
}

.reportes-card:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.reportes-header {
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  padding: 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.reportes-header h3 {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #15803d;
  font-family: 'Inter', sans-serif;
}

.reportes-header svg {
  width: 20px;
  height: 20px;
  color: #16a34a;
  stroke-width: 2.5;
}

.reportes-content {
  padding: 16px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-field label {
  font-size: 13px;
  font-weight: 500;
  color: #374151;
  font-family: 'Inter', sans-serif;
}

.form-select,
.form-input {
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

.form-select:focus,
.form-input:focus {
  outline: none;
  border-color: #16a34a;
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1);
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 16px;
}

.btn-generate {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'Inter', sans-serif;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.btn-generate svg {
  width: 16px;
  height: 16px;
}

.btn-generate:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(22, 163, 74, 0.3);
}

.btn-generate:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* Tabla de Reportes */
.reportes-table-container {
  overflow-x: auto;
}

.reportes-table {
  width: 100%;
  border-collapse: collapse;
}

.reportes-table thead {
  background: #f9fafb;
}

.reportes-table th {
  padding: 12px;
  text-align: left;
  font-size: 12px;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
  font-family: 'Inter', sans-serif;
}

.reportes-table td {
  padding: 12px;
  font-size: 13px;
  color: #4b5563;
  border-bottom: 1px solid #f3f4f6;
  font-family: 'Inter', sans-serif;
}

.reportes-table tbody tr {
  transition: background 0.15s;
}

.reportes-table tbody tr:hover {
  background: #f9fafb;
}

.badge-formato {
  display: inline-block;
  padding: 4px 10px;
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  color: #15803d;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  font-family: 'Inter', sans-serif;
  border: 1px solid rgba(22, 163, 74, 0.2);
}

.btn-action {
  padding: 6px;
  background: transparent;
  border: 1.5px solid #d1d5db;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-action:hover {
  background: #f3f4f6;
  border-color: #16a34a;
  transform: translateY(-1px);
}

.btn-action svg {
  width: 14px;
  height: 14px;
  color: #16a34a;
}

/* Estado Vacío */
.empty-state {
  text-align: center;
  padding: 60px 32px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  margin: 16px 0;
}

.empty-state svg {
  color: #d1d5db;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-title {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 8px;
  font-family: 'Inter', sans-serif;
}

.empty-subtitle {
  font-size: 13px;
  color: #6b7280;
  margin: 0;
  font-family: 'Inter', sans-serif;
}

/* === RESPONSIVE DESIGN === */

/* Tablets grandes y laptops pequeñas */
@media (max-width: 1200px) {
  .main-content {
    margin-left: min(200px, 16vw);
    width: calc(100vw - min(200px, 16vw));
  }

  .form-row {
    gap: 12px;
  }
}

/* Tablets */
@media (max-width: 1024px) {
  .main-content {
    margin-left: 200px;
    width: calc(100vw - 200px);
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .reportes-table th,
  .reportes-table td {
    padding: 10px;
    font-size: 12px;
  }
}

/* Landscape en tablets/móviles */
@media (max-width: 768px) and (orientation: landscape) {
  .main-content {
    margin-left: 160px;
    width: calc(100vw - 160px);
  }
  
  .page-header {
    padding: clamp(8px, 1.5vw, 12px);
  }
}

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

/* Móviles grandes */
@media (max-width: 768px) {
  .main-content {
    margin-left: 240px;
    width: calc(100vw - 240px);
  }

  .page-content {
    padding: 12px;
  }

  .page-header {
    padding: clamp(12px, 3vw, 20px);
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: clamp(8px, 2vw, 12px);
  }

  .header-main {
    width: 100%;
    margin-left: 0;
  }

  .header-actions {
    width: 100%;
    justify-content: space-between;
    margin-right: 0;
  }

  .reportes-content {
    padding: 12px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn-generate {
    width: 100%;
    justify-content: center;
  }

  .reportes-table {
    font-size: 11px;
  }

  .reportes-table th,
  .reportes-table td {
    padding: 8px;
  }
}

/* Móviles pequeños */
@media (max-width: 480px) {
  .main-content {
    margin-left: 60px;
    width: calc(100vw - 60px);
  }

  .page-content {
    padding: 8px;
  }

  .header-main {
    gap: 8px;
  }

  .header-icon {
    width: 28px;
    height: 28px;
  }

  .header-icon svg {
    width: 14px;
    height: 14px;
  }

  .refresh-btn {
    font-size: 10px;
    padding: 6px 10px;
  }

  .reportes-card {
    border-radius: 8px;
  }

  .reportes-header,
  .reportes-content {
    padding: 12px;
  }

  .form-field label {
    font-size: 12px;
  }

  .form-select,
  .form-input {
    font-size: 12px;
    padding: 7px 10px;
  }

  .empty-state {
    padding: 40px 20px;
  }

  .empty-state svg {
    width: 60px;
    height: 60px;
  }
}

/* Extra pequeño - teléfonos muy pequeños */
@media (max-width: 360px) {
  .main-content {
    margin-left: 60px;
    width: calc(100vw - 60px);
  }

  .page-header {
    padding: clamp(8px, 2vw, 12px);
  }

  .header-title {
    font-size: clamp(14px, 3.5vw, 18px) !important;
  }

  .header-subtitle {
    font-size: clamp(10px, 2.5vw, 12px) !important;
  }
}
</style>
