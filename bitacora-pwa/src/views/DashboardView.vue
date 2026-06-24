<template>
  <div class="shell">
    <!-- Header -->
    <header class="topbar">
      <div class="topbar-left">
        <span class="logo-dot">📍</span>
        <span class="title">Bitácora del Sistema</span>
      </div>
      <div class="topbar-right">
        <span class="live-badge" :class="{ active: autoRefresh }">
          {{ autoRefresh ? '● EN VIVO' : '○ Pausado' }}
        </span>
        <button class="btn-sm" @click="autoRefresh = !autoRefresh">
          {{ autoRefresh ? 'Pausar' : 'Reanudar' }}
        </button>
        <button class="btn-sm danger" @click="salir">Salir</button>
      </div>
    </header>

    <div class="content">
      <!-- Stats cards -->
      <div class="stats-row">
        <div class="stat-card">
          <div class="stat-num">{{ data.total ?? '—' }}</div>
          <div class="stat-label">Eventos totales</div>
        </div>
        <div v-for="s in (data.stats || []).slice(0,4)" :key="s.action" class="stat-card">
          <div class="stat-num">{{ s.count }}</div>
          <div class="stat-label">{{ labelAction(s.action) }}</div>
        </div>
      </div>

      <!-- Filters -->
      <div class="filters-bar">
        <input v-model="filters.usr" @input="debounceLoad" placeholder="Filtrar por usuario..." class="f-input" />
        <select v-model="filters.action_type" @change="load()" class="f-select">
          <option value="">Todas las acciones</option>
          <option v-for="a in filterOpts.actions" :key="a" :value="a">{{ labelAction(a) }}</option>
        </select>
        <select v-model="filters.module" @change="load()" class="f-select">
          <option value="">Todos los módulos</option>
          <option v-for="m in filterOpts.modules" :key="m" :value="m">{{ m }}</option>
        </select>
        <input v-model="filters.date_from" @change="load()" type="date" class="f-input" />
        <input v-model="filters.date_to" @change="load()" type="date" class="f-input" />
        <button class="btn-sm" @click="resetFilters">Limpiar</button>
      </div>

      <!-- Top usuarios -->
      <div class="top-users" v-if="data.top_users?.length">
        <span class="top-label">Usuarios activos:</span>
        <span v-for="u in data.top_users" :key="u.usr" class="user-chip" @click="filters.usr = u.usr; load()">
          {{ u.usr }} <b>({{ u.count }})</b>
        </span>
      </div>

      <!-- Tabla -->
      <div class="table-wrap">
        <div v-if="loading" class="loading-msg">Cargando...</div>
        <div v-else-if="!data.data?.length" class="empty-msg">Sin registros con esos filtros.</div>
        <table v-else class="log-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Fecha / Hora</th>
              <th>Usuario</th>
              <th>Acción</th>
              <th>Módulo</th>
              <th>Detalle</th>
              <th>Objetivo</th>
              <th>IP</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in data.data" :key="row.id" :class="rowClass(row.action_type)">
              <td class="muted">{{ row.id }}</td>
              <td class="ts">{{ formatTs(row.ts) }}</td>
              <td class="usr">{{ row.usr || '—' }}</td>
              <td><span class="badge" :class="badgeClass(row.action_type)">{{ labelAction(row.action_type) }}</span></td>
              <td class="module">{{ row.module || '—' }}</td>
              <td class="detail" :title="row.detail">{{ row.detail || '—' }}</td>
              <td class="target">{{ row.target_label || row.target_id || '—' }}</td>
              <td class="ip muted">{{ row.ip_hint || '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Paginación -->
      <div class="pagination">
        <button :disabled="page <= 1" @click="prevPage" class="btn-sm">‹ Anterior</button>
        <span>Página {{ page }} / {{ totalPages }}</span>
        <button :disabled="page >= totalPages" @click="nextPage" class="btn-sm">Siguiente ›</button>
        <span class="muted">{{ data.total }} registros</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { fetchData, fetchFilters, obsLogout } from '../services/api.js'

const router = useRouter()
const loading = ref(false)
const autoRefresh = ref(true)
const page = ref(1)
const limit = 50
const data = ref({ total: 0, data: [], stats: [], top_users: [] })
const filterOpts = ref({ actions: [], modules: [] })
const filters = reactive({ usr: '', action_type: '', module: '', date_from: '', date_to: '' })

const totalPages = computed(() => Math.max(1, Math.ceil((data.value.total || 0) / limit)))

let debounceTimer = null
function debounceLoad() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => { page.value = 1; load() }, 400)
}

async function load() {
  loading.value = true
  try {
    data.value = await fetchData({ ...filters, page: page.value, limit })
  } catch (e) {
    if (e.message === 'session') router.push('/login')
  } finally {
    loading.value = false
  }
}

function prevPage() { if (page.value > 1) { page.value--; load() } }
function nextPage() { if (page.value < totalPages.value) { page.value++; load() } }

function resetFilters() {
  filters.usr = ''; filters.action_type = ''; filters.module = ''
  filters.date_from = ''; filters.date_to = ''
  page.value = 1
  load()
}

function salir() {
  obsLogout()
  router.push('/login')
}

function formatTs(ts) {
  if (!ts) return '—'
  const d = new Date(ts)
  return d.toLocaleString('es-MX', { timeZone: 'America/Mexico_City', hour12: false,
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

const ACTION_LABELS = {
  page_view: 'Vista de página', login: 'Login', logout: 'Logout', login_failed: 'Intento fallido',
  create_user: 'Crear usuario', update_user: 'Editar usuario', delete_user: 'Eliminar usuario',
  toggle_user: 'Activar/desactivar', download_report: 'Descargar reporte', view_report: 'Ver reporte',
  delete_report: 'Eliminar reporte', delete_photo: 'Eliminar foto', view_photo: 'Ver foto',
  view_record: 'Ver registro', delete_record: 'Eliminar registro', export_csv: 'Exportar CSV',
  change_permission: 'Cambiar permiso', change_config: 'Cambiar configuración',
  send_notification: 'Enviar notificación', delete_notification: 'Eliminar notificación',
  view_asistencia: 'Ver asistencia', upload_manual: 'Subir manual', delete_manual: 'Eliminar manual',
  download_manual: 'Descargar manual',
}
function labelAction(a) { return ACTION_LABELS[a] || a }

function badgeClass(a) {
  if (['delete_user','delete_report','delete_photo','delete_record','delete_manual','delete_notification'].includes(a)) return 'danger'
  if (['login','create_user','upload_manual'].includes(a)) return 'success'
  if (['login_failed'].includes(a)) return 'warn'
  if (['download_report','export_csv','download_manual'].includes(a)) return 'info'
  return 'neutral'
}

function rowClass(a) {
  if (a?.startsWith('delete_')) return 'row-danger'
  if (a === 'login_failed') return 'row-warn'
  return ''
}

let interval = null
watch(autoRefresh, (val) => {
  if (val) interval = setInterval(load, 15000)
  else clearInterval(interval)
})

onMounted(async () => {
  filterOpts.value = await fetchFilters().catch(() => ({ actions: [], modules: [] }))
  load()
  interval = setInterval(load, 15000)
})
onUnmounted(() => clearInterval(interval))
</script>

<style scoped>
.shell { min-height: 100vh; display: flex; flex-direction: column; background: #0f172a; }
.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0.75rem 1.5rem; background: #1e293b; border-bottom: 1px solid #334155;
  position: sticky; top: 0; z-index: 10;
}
.topbar-left { display: flex; align-items: center; gap: 0.6rem; }
.logo-dot { font-size: 1.4rem; }
.title { font-size: 1rem; font-weight: 700; color: #f1f5f9; }
.topbar-right { display: flex; align-items: center; gap: 0.6rem; }
.live-badge { font-size: 0.7rem; font-weight: 700; color: #64748b; letter-spacing: 0.08em; }
.live-badge.active { color: #34d399; }
.content { padding: 1.25rem 1.5rem; display: flex; flex-direction: column; gap: 1rem; }

/* Stats */
.stats-row { display: flex; gap: 0.75rem; flex-wrap: wrap; }
.stat-card {
  background: #1e293b; border: 1px solid #334155; border-radius: 10px;
  padding: 0.85rem 1.2rem; min-width: 120px;
}
.stat-num { font-size: 1.6rem; font-weight: 800; color: #38bdf8; }
.stat-label { font-size: 0.72rem; color: #94a3b8; margin-top: 0.2rem; text-transform: uppercase; }

/* Filters */
.filters-bar { display: flex; gap: 0.6rem; flex-wrap: wrap; align-items: center; }
.f-input, .f-select {
  background: #1e293b; border: 1px solid #334155; border-radius: 8px;
  padding: 0.45rem 0.8rem; color: #e2e8f0; font-size: 0.85rem; outline: none;
}
.f-input:focus, .f-select:focus { border-color: #3b82f6; }
.f-select option { background: #1e293b; }

/* Top users */
.top-users { display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; font-size: 0.8rem; }
.top-label { color: #64748b; font-weight: 600; }
.user-chip {
  background: #1e293b; border: 1px solid #334155; border-radius: 20px;
  padding: 0.2rem 0.7rem; cursor: pointer; transition: border-color 0.2s;
}
.user-chip:hover { border-color: #38bdf8; }

/* Table */
.table-wrap { overflow-x: auto; border-radius: 10px; border: 1px solid #334155; }
.log-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.log-table thead { background: #1e293b; }
.log-table th { padding: 0.6rem 0.8rem; text-align: left; color: #94a3b8; font-weight: 600; font-size: 0.72rem; text-transform: uppercase; border-bottom: 1px solid #334155; white-space: nowrap; }
.log-table td { padding: 0.55rem 0.8rem; border-bottom: 1px solid #1e293b; color: #cbd5e1; vertical-align: middle; }
.log-table tbody tr:hover { background: #1e293b; }
.row-danger td { background: rgba(248,113,113,0.06); }
.row-warn td { background: rgba(251,191,36,0.06); }
.ts { white-space: nowrap; font-size: 0.78rem; color: #94a3b8; }
.usr { font-weight: 600; color: #38bdf8; }
.module { color: #a78bfa; }
.detail { max-width: 220px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.target { max-width: 160px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.ip, .muted { color: #475569; font-size: 0.78rem; }

/* Badges */
.badge { border-radius: 6px; padding: 0.15rem 0.55rem; font-size: 0.72rem; font-weight: 700; white-space: nowrap; }
.badge.danger { background: rgba(248,113,113,0.2); color: #f87171; }
.badge.success { background: rgba(52,211,153,0.2); color: #34d399; }
.badge.warn { background: rgba(251,191,36,0.2); color: #fbbf24; }
.badge.info { background: rgba(56,189,248,0.2); color: #38bdf8; }
.badge.neutral { background: rgba(148,163,184,0.15); color: #94a3b8; }

/* Pagination */
.pagination { display: flex; align-items: center; gap: 0.75rem; font-size: 0.85rem; color: #94a3b8; }

/* Buttons */
.btn-sm {
  background: #334155; border: 1px solid #475569; border-radius: 6px;
  padding: 0.35rem 0.8rem; color: #e2e8f0; font-size: 0.8rem; cursor: pointer; white-space: nowrap;
}
.btn-sm:hover:not(:disabled) { background: #475569; }
.btn-sm:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-sm.danger { background: rgba(248,113,113,0.15); border-color: #f87171; color: #f87171; }
.btn-sm.danger:hover { background: rgba(248,113,113,0.3); }

.loading-msg, .empty-msg { padding: 2rem; text-align: center; color: #475569; }
</style>
