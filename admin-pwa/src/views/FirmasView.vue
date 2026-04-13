<template>
  <div class="firmas-layout">
    <Sidebar />
    <main class="firmas-main">

      <!-- Header -->
      <header class="page-header">
        <div class="header-left">
          <div class="header-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 20h9M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z"/>
            </svg>
          </div>
          <div>
            <h1>Firmas</h1>
            <p>Reportes de tus técnicos asignados</p>
          </div>
        </div>
        <div class="header-stats">
          <div class="stat-pill orange">
            <span>{{ estadoPendiente }}</span>
            <label>Pendientes</label>
          </div>
          <div class="stat-pill green">
            <span>{{ estadoFirmado }}</span>
            <label>Firmados</label>
          </div>
        </div>
      </header>

      <!-- Filters -->
      <div class="filters-bar">
        <div class="filter-tabs">
          <button
            v-for="tab in tabs"
            :key="tab.value"
            :class="['tab', { active: filtroEstado === tab.value }]"
            @click="setFiltro(tab.value)"
          >{{ tab.label }}</button>
        </div>
        <div class="search-wrap">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
          </svg>
          <input v-model="busqueda" placeholder="Buscar técnico o reporte..." />
        </div>
        <button class="refresh-btn" @click="cargarReportes" :disabled="cargando">
          <svg :class="{ spin: cargando }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0118.8-4.3M22 12.5a10 10 0 01-18.8 4.2"/>
          </svg>
        </button>
      </div>

      <!-- Table -->
      <div class="table-wrap">
        <div v-if="cargando" class="state-center">
          <div class="spinner"></div>
          <p>Cargando reportes...</p>
        </div>

        <div v-else-if="error" class="state-center error">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <p>{{ error }}</p>
          <button @click="cargarReportes">Reintentar</button>
        </div>

        <div v-else-if="reportesFiltrados.length === 0" class="state-center empty">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z"/>
            <path d="M14 2v6h6M16 13H8M16 17H8"/>
          </svg>
          <p>No hay reportes {{ filtroEstado === 'pendiente' ? 'pendientes' : filtroEstado === 'firmado' ? 'firmados' : '' }}</p>
        </div>

        <table v-else>
          <thead>
            <tr>
              <th>Reporte</th>
              <th>Técnico</th>
              <th>Cargo</th>
              <th>Fecha</th>
              <th>Estado</th>
              <th>Acción</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in reportesFiltrados" :key="r.id">
              <td class="col-reporte">
                <span class="reporte-nombre">{{ r.nombre_reporte }}</span>
              </td>
              <td>{{ r.tecnico_nombre }}</td>
              <td><span class="cargo-badge">{{ abrevCargo(r.tecnico_cargo) }}</span></td>
              <td>{{ formatFecha(r.fecha_generado) }}</td>
              <td>
                <span :class="['status-badge', r.firmado_supervisor ? 'firmado' : 'pendiente']">
                  {{ r.firmado_supervisor ? 'Firmado' : 'Pendiente' }}
                </span>
                <div v-if="r.firmado_supervisor && r.nombre_supervisor" class="firmado-por">
                  por {{ r.nombre_supervisor }}
                </div>
              </td>
              <td>
                <button
                  v-if="!r.firmado_supervisor"
                  class="btn-firmar"
                  @click="abrirModalFirma(r)"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M12 20h9M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z"/>
                  </svg>
                  Firmar
                </button>
                <span v-else class="ya-firmado">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M22 11.08V12a10 10 0 11-5.93-9.14"/>
                    <polyline points="22 4 12 14.01 9 11.01"/>
                  </svg>
                  Firmado
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="totalReportes > limite" class="pagination">
        <button :disabled="offset === 0" @click="anterior">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>
        </button>
        <span>{{ paginaActual }} / {{ totalPaginas }}</span>
        <button :disabled="offset + limite >= totalReportes" @click="siguiente">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
        </button>
      </div>
    </main>

    <!-- Modal de firma -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="modalAbierto" class="modal-backdrop" @click.self="cerrarModal">
          <div class="modal-card">
            <div class="modal-header">
              <h3>Firmar reporte</h3>
              <button @click="cerrarModal" class="close-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
              </button>
            </div>

            <div v-if="reporteSeleccionado" class="modal-info">
              <div class="info-row">
                <span class="info-label">Reporte:</span>
                <span>{{ reporteSeleccionado.nombre_reporte }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">Técnico:</span>
                <span>{{ reporteSeleccionado.tecnico_nombre }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">Fechas:</span>
                <span>{{ formatFecha(reporteSeleccionado.fecha_generado) }}</span>
              </div>
            </div>

            <div class="firma-section">
              <label>Firma digital (opcional)</label>
              <div class="canvas-wrap">
                <canvas
                  ref="firmaCanvas"
                  width="400"
                  height="160"
                  @mousedown="startDraw"
                  @mousemove="draw"
                  @mouseup="stopDraw"
                  @mouseleave="stopDraw"
                  @touchstart.prevent="startDrawTouch"
                  @touchmove.prevent="drawTouch"
                  @touchend="stopDraw"
                ></canvas>
                <button class="clear-canvas" @click="limpiarFirma" title="Limpiar firma">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6"/>
                  </svg>
                </button>
              </div>
              <p class="canvas-hint">Dibuja tu firma con el mouse o dedo</p>
            </div>

            <div class="modal-actions">
              <button class="btn-cancel" @click="cerrarModal" :disabled="firmando">Cancelar</button>
              <button class="btn-confirm" @click="confirmarFirma" :disabled="firmando">
                <svg v-if="firmando" class="spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 12a9 9 0 11-6.219-8.56"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M12 20h9M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z"/>
                </svg>
                {{ firmando ? 'Firmando...' : 'Confirmar Firma' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Toast -->
    <Transition name="toast">
      <div v-if="toast.visible" :class="['toast', toast.type]">
        <svg v-if="toast.type === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        {{ toast.message }}
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import facilitadoresService from '../services/facilitadoresService'
import authService from '../services/authService'

// ── State ──────────────────────────────────────────────────────
const reportes        = ref([])
const totalReportes   = ref(0)
const cargando        = ref(false)
const error           = ref(null)
const filtroEstado    = ref(null)
const busqueda        = ref('')
const offset          = ref(0)
const limite          = ref(50)

const modalAbierto        = ref(false)
const reporteSeleccionado = ref(null)
const firmando            = ref(false)

const firmaCanvas  = ref(null)
const dibujando    = ref(false)
const tieneFirma   = ref(false)
let lastX = 0, lastY = 0

const toast = ref({ visible: false, type: 'success', message: '' })

const tabs = [
  { label: 'Todos', value: null },
  { label: 'Pendientes', value: 'pendiente' },
  { label: 'Firmados', value: 'firmado' }
]

// ── Computed ───────────────────────────────────────────────────
const adminId = computed(() => authService.getCurrentUser()?.id)

const reportesFiltrados = computed(() => {
  if (!busqueda.value) return reportes.value
  const q = busqueda.value.toLowerCase()
  return reportes.value.filter(r =>
    r.nombre_reporte?.toLowerCase().includes(q) ||
    r.tecnico_nombre?.toLowerCase().includes(q)
  )
})

const estadoPendiente = computed(() => reportes.value.filter(r => !r.firmado_supervisor).length)
const estadoFirmado   = computed(() => reportes.value.filter(r => r.firmado_supervisor).length)
const totalPaginas    = computed(() => Math.ceil(totalReportes.value / limite.value))
const paginaActual    = computed(() => Math.floor(offset.value / limite.value) + 1)

// ── Methods ───────────────────────────────────────────────────
async function cargarReportes() {
  if (!adminId.value) { error.value = 'Sesión no válida'; return }
  cargando.value = true
  error.value = null
  try {
    const data = await facilitadoresService.misReportes(adminId.value, {
      estado: filtroEstado.value,
      limite: limite.value,
      offset: offset.value
    })
    reportes.value = data.reportes || []
    totalReportes.value = data.total || 0
  } catch (e) {
    error.value = e.message
  } finally {
    cargando.value = false
  }
}

function setFiltro(val) {
  filtroEstado.value = val
  offset.value = 0
  cargarReportes()
}

function anterior() { if (offset.value > 0) { offset.value -= limite.value; cargarReportes() } }
function siguiente() { if (offset.value + limite.value < totalReportes.value) { offset.value += limite.value; cargarReportes() } }

function formatFecha(iso) {
  if (!iso) return '-'
  return new Date(iso).toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' })
}

function abrevCargo(cargo) {
  if (!cargo) return '-'
  if (cargo.toUpperCase().includes('SOCIAL')) return 'T. Social'
  if (cargo.toUpperCase().includes('PRODUCT')) return 'T. Productivo'
  return cargo.slice(0, 14)
}

// ── Modal y canvas ────────────────────────────────────────────
async function abrirModalFirma(reporte) {
  reporteSeleccionado.value = reporte
  modalAbierto.value = true
  tieneFirma.value = false
  await nextTick()
  inicializarCanvas()
}

function cerrarModal() {
  modalAbierto.value = false
  reporteSeleccionado.value = null
  dibujando.value = false
}

function inicializarCanvas() {
  const canvas = firmaCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  ctx.fillStyle = '#f9f9f9'
  ctx.fillRect(0, 0, canvas.width, canvas.height)
  ctx.strokeStyle = '#e0e0e0'
  ctx.setLineDash([4, 4])
  ctx.beginPath()
  ctx.moveTo(20, canvas.height - 30)
  ctx.lineTo(canvas.width - 20, canvas.height - 30)
  ctx.stroke()
  ctx.setLineDash([])
  tieneFirma.value = false
}

function getPos(e, canvas) {
  const rect = canvas.getBoundingClientRect()
  const scaleX = canvas.width / rect.width
  const scaleY = canvas.height / rect.height
  return {
    x: (e.clientX - rect.left) * scaleX,
    y: (e.clientY - rect.top) * scaleY
  }
}

function startDraw(e) {
  const c = firmaCanvas.value; if (!c) return
  dibujando.value = true; tieneFirma.value = true
  const pos = getPos(e, c); lastX = pos.x; lastY = pos.y
}
function draw(e) {
  if (!dibujando.value) return
  const c = firmaCanvas.value; if (!c) return
  const ctx = c.getContext('2d')
  const pos = getPos(e, c)
  ctx.beginPath()
  ctx.moveTo(lastX, lastY)
  ctx.lineTo(pos.x, pos.y)
  ctx.strokeStyle = '#1d1d1f'
  ctx.lineWidth = 2
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
  ctx.stroke()
  lastX = pos.x; lastY = pos.y
}
function stopDraw() { dibujando.value = false }

function startDrawTouch(e) {
  const t = e.touches[0]; const c = firmaCanvas.value; if (!c) return
  dibujando.value = true; tieneFirma.value = true
  const rect = c.getBoundingClientRect()
  lastX = (t.clientX - rect.left) * (c.width / rect.width)
  lastY = (t.clientY - rect.top) * (c.height / rect.height)
}
function drawTouch(e) {
  if (!dibujando.value) return
  const t = e.touches[0]; const c = firmaCanvas.value; if (!c) return
  const ctx = c.getContext('2d')
  const rect = c.getBoundingClientRect()
  const x = (t.clientX - rect.left) * (c.width / rect.width)
  const y = (t.clientY - rect.top) * (c.height / rect.height)
  ctx.beginPath(); ctx.moveTo(lastX, lastY); ctx.lineTo(x, y)
  ctx.strokeStyle = '#1d1d1f'; ctx.lineWidth = 2; ctx.lineCap = 'round'; ctx.stroke()
  lastX = x; lastY = y
}

function limpiarFirma() { inicializarCanvas() }

async function confirmarFirma() {
  if (!reporteSeleccionado.value || !adminId.value) return
  firmando.value = true
  try {
    let firmaB64 = null
    if (tieneFirma.value && firmaCanvas.value) {
      firmaB64 = firmaCanvas.value.toDataURL('image/png').split(',')[1]
    }
    await facilitadoresService.firmarReporte(
      reporteSeleccionado.value.id,
      adminId.value,
      firmaB64
    )
    // Actualizar localmente
    const idx = reportes.value.findIndex(r => r.id === reporteSeleccionado.value.id)
    if (idx !== -1) reportes.value[idx].firmado_supervisor = true
    cerrarModal()
    mostrarToast('Reporte firmado exitosamente', 'success')
  } catch (e) {
    mostrarToast(e.message || 'Error al firmar', 'error')
  } finally {
    firmando.value = false
  }
}

function mostrarToast(message, type = 'success') {
  toast.value = { visible: true, type, message }
  setTimeout(() => { toast.value.visible = false }, 3500)
}

onMounted(cargarReportes)
</script>

<style scoped>
/* ── Layout ─────────────────────────────────────────────────── */
.firmas-layout {
  display: flex;
  min-height: 100vh;
  background: #f5f5f7;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
}

.firmas-main {
  flex: 1;
  margin-left: 264px;
  padding: 32px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ── Header ─────────────────────────────────────────────────── */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-radius: 16px;
  padding: 20px 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,.06);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.header-icon {
  width: 44px; height: 44px;
  background: rgba(52,199,89,.1);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
}
.header-icon svg { width: 22px; height: 22px; color: #34c759; }

.header-left h1 { font-size: 22px; font-weight: 700; color: #1d1d1f; margin: 0; letter-spacing: -.02em; }
.header-left p  { font-size: 13px; color: #86868b; margin: 2px 0 0; }

.header-stats { display: flex; gap: 10px; }
.stat-pill {
  display: flex; flex-direction: column; align-items: center;
  padding: 8px 18px; border-radius: 12px; min-width: 64px;
}
.stat-pill span { font-size: 22px; font-weight: 700; line-height: 1; }
.stat-pill label { font-size: 11px; font-weight: 500; margin-top: 2px; }
.stat-pill.orange { background: rgba(255,149,0,.1); }
.stat-pill.orange span { color: #ff9500; }
.stat-pill.orange label { color: #ff9500; }
.stat-pill.green  { background: rgba(52,199,89,.1); }
.stat-pill.green span  { color: #34c759; }
.stat-pill.green label { color: #34c759; }

/* ── Filters ─────────────────────────────────────────────────── */
.filters-bar {
  display: flex; align-items: center; gap: 12px;
  background: #fff; border-radius: 14px; padding: 12px 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,.06);
  flex-wrap: wrap;
}

.filter-tabs { display: flex; gap: 4px; }
.tab {
  padding: 7px 16px; border: none; background: transparent;
  border-radius: 8px; font-size: 14px; font-weight: 500; color: #86868b;
  cursor: pointer; transition: all .2s;
}
.tab:hover { background: #f5f5f7; color: #1d1d1f; }
.tab.active { background: #007aff; color: #fff; }

.search-wrap {
  flex: 1; display: flex; align-items: center; gap: 8px;
  background: #f5f5f7; border-radius: 10px; padding: 8px 12px; min-width: 200px;
}
.search-wrap svg { width: 16px; height: 16px; color: #86868b; flex-shrink: 0; }
.search-wrap input {
  flex: 1; border: none; background: transparent; font-size: 14px; color: #1d1d1f; outline: none;
}
.search-wrap input::placeholder { color: #aeaeb2; }

.refresh-btn {
  width: 36px; height: 36px; border: none; background: #f5f5f7; border-radius: 10px;
  display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all .2s;
}
.refresh-btn:hover { background: #e8e8ed; }
.refresh-btn svg { width: 18px; height: 18px; color: #1d1d1f; }

/* ── Table ───────────────────────────────────────────────────── */
.table-wrap {
  flex: 1; background: #fff; border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,.06); overflow: hidden;
}

table { width: 100%; border-collapse: collapse; }
thead tr { background: #f5f5f7; }
th {
  padding: 12px 16px; text-align: left; font-size: 11px; font-weight: 700;
  color: #86868b; text-transform: uppercase; letter-spacing: .04em;
}
td {
  padding: 13px 16px; font-size: 14px; color: #1d1d1f;
  border-bottom: 1px solid rgba(0,0,0,.05);
}
tbody tr:last-child td { border-bottom: none; }
tbody tr:hover { background: #fafafa; }

.col-reporte { max-width: 220px; }
.reporte-nombre { font-weight: 500; }

.cargo-badge {
  font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 100px;
  background: rgba(0,122,255,.1); color: #007aff;
}

.status-badge {
  font-size: 12px; font-weight: 600; padding: 3px 10px; border-radius: 100px; display: inline-block;
}
.status-badge.firmado   { background: rgba(52,199,89,.1);  color: #34c759; }
.status-badge.pendiente { background: rgba(255,149,0,.1); color: #ff9500; }
.firmado-por { font-size: 11px; color: #86868b; margin-top: 2px; }

.btn-firmar {
  display: flex; align-items: center; gap: 6px; padding: 7px 14px;
  background: #007aff; color: #fff; border: none; border-radius: 8px;
  font-size: 13px; font-weight: 600; cursor: pointer; transition: all .2s;
}
.btn-firmar:hover { filter: brightness(1.08); }
.btn-firmar svg { width: 14px; height: 14px; }

.ya-firmado {
  display: flex; align-items: center; gap: 5px; font-size: 13px; color: #34c759; font-weight: 500;
}
.ya-firmado svg { width: 14px; height: 14px; }

/* ── States ──────────────────────────────────────────────────── */
.state-center {
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; gap: 12px; padding: 64px 20px; color: #86868b;
}
.state-center svg { width: 40px; height: 40px; }
.state-center p { font-size: 15px; margin: 0; }
.state-center.error { color: #ff3b30; }
.state-center.error svg { color: #ff3b30; }
.state-center button {
  padding: 8px 20px; background: #007aff; color: #fff; border: none; border-radius: 8px;
  font-size: 14px; font-weight: 600; cursor: pointer; margin-top: 4px;
}

.spinner {
  width: 32px; height: 32px; border: 3px solid #e8e8ed; border-top-color: #007aff;
  border-radius: 50%; animation: spin .7s linear infinite;
}

/* ── Pagination ──────────────────────────────────────────────── */
.pagination {
  display: flex; align-items: center; justify-content: center; gap: 16px;
  background: #fff; border-radius: 12px; padding: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,.06);
}
.pagination button {
  width: 32px; height: 32px; border: none; background: #f5f5f7; border-radius: 8px;
  display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all .2s;
}
.pagination button:disabled { opacity: .4; cursor: not-allowed; }
.pagination button:not(:disabled):hover { background: #e8e8ed; }
.pagination button svg { width: 18px; height: 18px; color: #1d1d1f; }
.pagination span { font-size: 14px; font-weight: 500; color: #1d1d1f; min-width: 60px; text-align: center; }

/* ── Modal ───────────────────────────────────────────────────── */
.modal-backdrop {
  position: fixed; inset: 0; background: rgba(0,0,0,.35);
  backdrop-filter: blur(10px); display: flex; align-items: center;
  justify-content: center; z-index: 10000; padding: 20px;
}

.modal-card {
  width: 100%; max-width: 480px; background: #fff; border-radius: 20px;
  padding: 24px; box-shadow: 0 24px 80px rgba(0,0,0,.2);
}

.modal-header {
  display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px;
}
.modal-header h3 { font-size: 18px; font-weight: 700; color: #1d1d1f; margin: 0; }
.close-btn {
  width: 28px; height: 28px; border: none; background: #f5f5f7; border-radius: 8px;
  display: flex; align-items: center; justify-content: center; cursor: pointer;
}
.close-btn svg { width: 14px; height: 14px; color: #86868b; }

.modal-info { background: #f5f5f7; border-radius: 12px; padding: 14px; margin-bottom: 18px; }
.info-row { display: flex; gap: 8px; margin-bottom: 4px; font-size: 14px; }
.info-row:last-child { margin-bottom: 0; }
.info-label { font-weight: 600; color: #1d1d1f; min-width: 64px; }

.firma-section { margin-bottom: 20px; }
.firma-section label { display: block; font-size: 13px; font-weight: 600; color: #1d1d1f; margin-bottom: 8px; }

.canvas-wrap { position: relative; border: 1.5px solid #e0e0e0; border-radius: 12px; overflow: hidden; }
.canvas-wrap canvas { display: block; width: 100%; cursor: crosshair; touch-action: none; }
.clear-canvas {
  position: absolute; top: 8px; right: 8px; width: 28px; height: 28px;
  background: rgba(255,255,255,.9); border: 1px solid #e0e0e0; border-radius: 8px;
  display: flex; align-items: center; justify-content: center; cursor: pointer;
}
.clear-canvas svg { width: 14px; height: 14px; color: #86868b; }
.canvas-hint { font-size: 12px; color: #aeaeb2; margin: 6px 0 0; text-align: center; }

.modal-actions { display: flex; gap: 10px; }
.modal-actions button {
  flex: 1; display: flex; align-items: center; justify-content: center; gap: 7px;
  padding: 13px 20px; border: none; border-radius: 12px; font-size: 15px;
  font-weight: 600; cursor: pointer; transition: all .2s;
}
.modal-actions button:disabled { opacity: .6; cursor: not-allowed; }
.btn-cancel  { background: #f5f5f7; color: #1d1d1f; }
.btn-cancel:hover { background: #e8e8ed; }
.btn-confirm { background: #34c759; color: #fff; }
.btn-confirm:hover { filter: brightness(1.05); }
.btn-confirm svg { width: 16px; height: 16px; }

/* ── Toast ───────────────────────────────────────────────────── */
.toast {
  position: fixed; bottom: 28px; right: 28px; z-index: 99999;
  display: flex; align-items: center; gap: 10px; padding: 14px 20px;
  border-radius: 14px; font-size: 14px; font-weight: 600;
  box-shadow: 0 8px 32px rgba(0,0,0,.15); max-width: 320px;
}
.toast.success { background: #34c759; color: #fff; }
.toast.error   { background: #ff3b30; color: #fff; }
.toast svg { width: 18px; height: 18px; flex-shrink: 0; }

/* ── Animations ──────────────────────────────────────────────── */
.modal-enter-active { transition: all .3s ease-out; }
.modal-leave-active { transition: all .2s ease-in; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-from .modal-card { transform: scale(.95) translateY(10px); }
.modal-leave-to .modal-card { transform: scale(.97); }

.toast-enter-active { transition: all .3s ease-out; }
.toast-leave-active { transition: all .2s ease-in; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateX(20px); }

@keyframes spin { to { transform: rotate(360deg); } }
.spin { animation: spin .7s linear infinite; }

/* ── Responsive ──────────────────────────────────────────────── */
@media (max-width: 768px) {
  .firmas-main { margin-left: 0; padding: 80px 16px 16px; }
  .page-header { flex-direction: column; align-items: flex-start; gap: 12px; }
  .header-stats { align-self: flex-end; }
  th:nth-child(3), td:nth-child(3) { display: none; }
}
</style>
