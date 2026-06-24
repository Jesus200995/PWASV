<template>
  <div class="shell">
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-header">
        <div class="brand-icon" aria-hidden="true">
          <svg width="26" height="26" viewBox="0 0 32 32" fill="none">
            <rect width="32" height="32" rx="10" fill="#1a6ef5"/>
            <path d="M16 7l7 4v10l-7 4-7-4V11l7-4z" stroke="#fff" stroke-width="1.6" stroke-linejoin="round" fill="none"/>
            <circle cx="16" cy="16" r="2.5" fill="#fff"/>
          </svg>
        </div>
        <span class="brand-name">PWASV · Bitácora</span>
        <button class="close-sidebar" @click="sidebarOpen = false" aria-label="Cerrar menú">
          <i class="ti ti-x" aria-hidden="true"></i>
        </button>
      </div>

      <nav class="sidebar-nav">
        <button class="nav-item active" aria-current="page">
          <i class="ti ti-list-details" aria-hidden="true"></i>
          <span>Todos los eventos</span>
        </button>
        <button class="nav-item" @click="setFilter('login'); sidebarOpen=false">
          <i class="ti ti-login" aria-hidden="true"></i>
          <span>Accesos</span>
        </button>
        <button class="nav-item" @click="setFilter('delete'); sidebarOpen=false">
          <i class="ti ti-trash" aria-hidden="true"></i>
          <span>Eliminaciones</span>
        </button>
        <button class="nav-item" @click="setFilter('download'); sidebarOpen=false">
          <i class="ti ti-download" aria-hidden="true"></i>
          <span>Descargas</span>
        </button>
        <button class="nav-item" @click="setFilter('create'); sidebarOpen=false">
          <i class="ti ti-plus" aria-hidden="true"></i>
          <span>Creaciones</span>
        </button>
      </nav>

      <div class="sidebar-footer">
        <div class="live-row">
          <span class="live-dot" :class="{ on: autoRefresh }" aria-hidden="true"></span>
          <span class="live-label">{{ autoRefresh ? 'En vivo · 15s' : 'Pausado' }}</span>
          <button class="toggle-live" @click="autoRefresh = !autoRefresh" :aria-label="autoRefresh ? 'Pausar actualización' : 'Reanudar'">
            <i :class="autoRefresh ? 'ti ti-player-pause' : 'ti ti-player-play'" aria-hidden="true"></i>
          </button>
        </div>
        <button class="signout-btn" @click="salir">
          <i class="ti ti-logout" aria-hidden="true"></i> Cerrar sesión
        </button>
      </div>
    </aside>

    <!-- Main area -->
    <div class="main" @click.self="sidebarOpen = false">
      <!-- Topbar mobile -->
      <header class="topbar">
        <button class="hamburger" @click="sidebarOpen = !sidebarOpen" aria-label="Menú">
          <i class="ti ti-menu-2" aria-hidden="true"></i>
        </button>
        <span class="topbar-title">Bitácora del sistema</span>
        <div class="topbar-right">
          <span class="last-update">Actualizado {{ lastUpdateLabel }}</span>
          <button class="icon-btn" @click="load()" :disabled="loading" aria-label="Actualizar">
            <i class="ti ti-refresh" :class="{ spinning: loading }" aria-hidden="true"></i>
          </button>
        </div>
      </header>

      <div class="content-scroll">
        <!-- Stats grid -->
        <section class="stats-grid" aria-label="Resumen estadístico">
          <div class="stat-card">
            <i class="ti ti-activity stat-icon blue" aria-hidden="true"></i>
            <div>
              <div class="stat-value">{{ fmtNum(data.total) }}</div>
              <div class="stat-label">Total de eventos</div>
            </div>
          </div>
          <div v-for="s in topStats" :key="s.action" class="stat-card">
            <i :class="`ti ${actionIcon(s.action)} stat-icon ${actionColor(s.action)}`" aria-hidden="true"></i>
            <div>
              <div class="stat-value">{{ fmtNum(s.count) }}</div>
              <div class="stat-label">{{ labelAction(s.action) }}</div>
            </div>
          </div>
        </section>

        <!-- Filtros -->
        <section class="filters-section">
          <div class="filters-row">
            <div class="search-wrap">
              <i class="ti ti-search search-icon" aria-hidden="true"></i>
              <input
                v-model="filters.usr"
                @input="debounceLoad"
                type="text"
                class="search-input"
                placeholder="Buscar por usuario..."
                aria-label="Filtrar por usuario"
              />
            </div>

            <select v-model="filters.action_type" @change="load()" class="f-select" aria-label="Filtrar por acción">
              <option value="">Todas las acciones</option>
              <option v-for="a in filterOpts.actions" :key="a" :value="a">{{ labelAction(a) }}</option>
            </select>

            <select v-model="filters.module" @change="load()" class="f-select" aria-label="Filtrar por módulo">
              <option value="">Todos los módulos</option>
              <option v-for="m in filterOpts.modules" :key="m" :value="m">{{ m }}</option>
            </select>

            <div class="date-group">
              <input v-model="filters.date_from" @change="load()" type="date" class="f-date" aria-label="Desde" />
              <span class="date-sep" aria-hidden="true">→</span>
              <input v-model="filters.date_to" @change="load()" type="date" class="f-date" aria-label="Hasta" />
            </div>

            <button class="clear-btn" @click="resetFilters" :disabled="!hasFilters" aria-label="Limpiar filtros">
              <i class="ti ti-x" aria-hidden="true"></i> Limpiar
            </button>
          </div>

          <!-- Chips de usuarios frecuentes -->
          <div v-if="data.top_users?.length" class="chips-row" aria-label="Usuarios más activos">
            <span class="chips-label">Top usuarios:</span>
            <button
              v-for="u in data.top_users"
              :key="u.usr"
              class="chip"
              :class="{ active: filters.usr === u.usr }"
              @click="filters.usr === u.usr ? (filters.usr = '', load()) : (filters.usr = u.usr, load())"
            >
              <i class="ti ti-user-circle" aria-hidden="true"></i>
              {{ u.usr }} <span class="chip-count">{{ u.count }}</span>
            </button>
          </div>
        </section>

        <!-- Tabla -->
        <section class="table-section">
          <div class="table-header-row">
            <span class="results-count">
              {{ loading ? 'Cargando...' : `${fmtNum(data.total)} registros` }}
            </span>
            <div class="pagination-controls">
              <button class="pag-btn" :disabled="page <= 1" @click="prevPage" aria-label="Página anterior">
                <i class="ti ti-chevron-left" aria-hidden="true"></i>
              </button>
              <span class="pag-label">{{ page }} / {{ totalPages }}</span>
              <button class="pag-btn" :disabled="page >= totalPages" @click="nextPage" aria-label="Página siguiente">
                <i class="ti ti-chevron-right" aria-hidden="true"></i>
              </button>
            </div>
          </div>

          <div class="table-wrap" role="region" aria-label="Tabla de eventos">
            <div v-if="loading && !data.data?.length" class="empty-state">
              <div class="skeleton-rows">
                <div v-for="n in 8" :key="n" class="skeleton-row"></div>
              </div>
            </div>
            <div v-else-if="!data.data?.length" class="empty-state">
              <i class="ti ti-database-off empty-icon" aria-hidden="true"></i>
              <p>Sin eventos con esos filtros</p>
              <button class="clear-btn" @click="resetFilters">Limpiar filtros</button>
            </div>
            <table v-else class="log-table" aria-label="Eventos del sistema">
              <thead>
                <tr>
                  <th scope="col">Fecha y hora</th>
                  <th scope="col">Usuario</th>
                  <th scope="col">Acción</th>
                  <th scope="col">Módulo</th>
                  <th scope="col" class="col-detail">Detalle</th>
                  <th scope="col" class="col-target">Objetivo</th>
                  <th scope="col" class="col-ip">IP</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="row in data.data"
                  :key="row.id"
                  :class="rowClass(row.action_type)"
                  @click="expandedRow = expandedRow === row.id ? null : row.id"
                  style="cursor:pointer"
                >
                  <td class="td-ts">
                    <span class="ts-date">{{ formatDate(row.ts) }}</span>
                    <span class="ts-time">{{ formatTime(row.ts) }}</span>
                  </td>
                  <td class="td-usr">
                    <span class="usr-avatar" :style="usrColor(row.usr)" aria-hidden="true">
                      {{ (row.usr || '?')[0].toUpperCase() }}
                    </span>
                    <span class="usr-name">{{ row.usr || '—' }}</span>
                  </td>
                  <td>
                    <span class="badge" :class="badgeClass(row.action_type)">
                      <i :class="`ti ${actionIcon(row.action_type)}`" aria-hidden="true"></i>
                      {{ labelAction(row.action_type) }}
                    </span>
                  </td>
                  <td class="td-module">{{ row.module || '—' }}</td>
                  <td class="col-detail td-clip" :title="row.detail">{{ row.detail || '—' }}</td>
                  <td class="col-target td-clip" :title="row.target_label || row.target_id">{{ row.target_label || row.target_id || '—' }}</td>
                  <td class="col-ip td-muted">{{ row.ip_hint || '—' }}</td>
                </tr>

                <!-- Row expand -->
                <template v-for="row in data.data" :key="'x'+row.id">
                  <tr v-if="expandedRow === row.id" class="expanded-row">
                    <td colspan="7">
                      <div class="expanded-body">
                        <div class="exp-field"><span>ID</span> {{ row.id }}</div>
                        <div class="exp-field"><span>Sesión</span> {{ row.session_id || '—' }}</div>
                        <div class="exp-field"><span>IP</span> {{ row.ip_hint || '—' }}</div>
                        <div class="exp-field"><span>Detalle completo</span> {{ row.detail || '—' }}</div>
                        <div class="exp-field" v-if="row.ua"><span>User Agent</span> <span class="ua-text">{{ row.ua }}</span></div>
                        <div class="exp-field" v-if="row.extra"><span>Extra</span> <code>{{ JSON.stringify(row.extra) }}</code></div>
                      </div>
                    </td>
                  </tr>
                </template>
              </tbody>
            </table>
          </div>

          <!-- Pagination bottom -->
          <div class="pagination-bottom">
            <button class="pag-btn-lg" :disabled="page <= 1" @click="prevPage">
              <i class="ti ti-chevron-left" aria-hidden="true"></i> Anterior
            </button>
            <div class="pag-pages">
              <button
                v-for="p in pageNumbers"
                :key="p"
                class="pag-num"
                :class="{ active: p === page, ellipsis: p === '…' }"
                @click="p !== '…' && goToPage(p)"
                :disabled="p === '…'"
              >{{ p }}</button>
            </div>
            <button class="pag-btn-lg" :disabled="page >= totalPages" @click="nextPage">
              Siguiente <i class="ti ti-chevron-right" aria-hidden="true"></i>
            </button>
          </div>
        </section>
      </div>
    </div>

    <!-- Sidebar overlay mobile -->
    <div v-if="sidebarOpen" class="sidebar-overlay" @click="sidebarOpen = false" aria-hidden="true"></div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { fetchData, fetchFilters, obsLogout } from '../services/api.js'

const router = useRouter()
const loading = ref(false)
const autoRefresh = ref(true)
const sidebarOpen = ref(false)
const page = ref(1)
const limit = 50
const data = ref({ total: 0, data: [], stats: [], top_users: [] })
const filterOpts = ref({ actions: [], modules: [] })
const expandedRow = ref(null)
const lastUpdate = ref(new Date())
const filters = reactive({ usr: '', action_type: '', module: '', date_from: '', date_to: '' })

const totalPages = computed(() => Math.max(1, Math.ceil((data.value.total || 0) / limit)))
const topStats = computed(() => (data.value.stats || []).slice(0, 3))
const hasFilters = computed(() => !!(filters.usr || filters.action_type || filters.module || filters.date_from || filters.date_to))

const lastUpdateLabel = computed(() => {
  const diff = Math.floor((Date.now() - lastUpdate.value) / 1000)
  if (diff < 5) return 'ahora'
  if (diff < 60) return `hace ${diff}s`
  return `hace ${Math.floor(diff/60)}m`
})

const pageNumbers = computed(() => {
  const total = totalPages.value
  const cur = page.value
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1)
  const pages = []
  if (cur > 3) { pages.push(1); if (cur > 4) pages.push('…') }
  for (let p = Math.max(1, cur - 2); p <= Math.min(total, cur + 2); p++) pages.push(p)
  if (cur < total - 2) { if (cur < total - 3) pages.push('…'); pages.push(total) }
  return pages
})

let debounceTimer = null
function debounceLoad() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => { page.value = 1; load() }, 380)
}

async function load() {
  loading.value = true
  try {
    data.value = await fetchData({ ...filters, page: page.value, limit })
    lastUpdate.value = new Date()
  } catch (e) {
    if (e.message === 'session') router.push('/login')
  } finally {
    loading.value = false
  }
}

function setFilter(keyword) {
  filters.action_type = ''
  filters.usr = ''
  const map = {
    login: 'login', delete: 'delete_user', download: 'download_report', create: 'create_user'
  }
  filters.action_type = map[keyword] || ''
  page.value = 1
  load()
}

function prevPage() { if (page.value > 1) { page.value--; load() } }
function nextPage() { if (page.value < totalPages.value) { page.value++; load() } }
function goToPage(p) { page.value = p; load() }

function resetFilters() {
  filters.usr = ''; filters.action_type = ''; filters.module = ''
  filters.date_from = ''; filters.date_to = ''
  page.value = 1; load()
}

function salir() { obsLogout(); router.push('/login') }

function fmtNum(n) { return (n || 0).toLocaleString('es-MX') }

function formatDate(ts) {
  if (!ts) return '—'
  return new Date(ts).toLocaleDateString('es-MX', { timeZone: 'America/Mexico_City', day: '2-digit', month: 'short', year: 'numeric' })
}

function formatTime(ts) {
  if (!ts) return ''
  return new Date(ts).toLocaleTimeString('es-MX', { timeZone: 'America/Mexico_City', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false })
}

const USR_COLORS = ['#1a6ef5','#0ea5e9','#8b5cf6','#10b981','#f59e0b','#ef4444','#ec4899','#14b8a6']
function usrColor(usr) {
  if (!usr) return 'background:#475569'
  const i = usr.split('').reduce((a, c) => a + c.charCodeAt(0), 0) % USR_COLORS.length
  return `background:${USR_COLORS[i]}`
}

const ACTION_LABELS = {
  page_view:'Vista de página', login:'Login', logout:'Logout', login_failed:'Login fallido',
  create_user:'Crear usuario', update_user:'Editar usuario', delete_user:'Eliminar usuario',
  toggle_user:'Activar usuario', download_report:'Descargar reporte', view_report:'Ver reporte',
  delete_report:'Eliminar reporte', delete_photo:'Eliminar foto', view_photo:'Ver foto',
  view_record:'Ver registro', delete_record:'Eliminar registro', export_csv:'Exportar CSV',
  change_permission:'Cambiar permiso', change_config:'Cambiar config',
  send_notification:'Enviar notificación', delete_notification:'Eliminar notificación',
  view_asistencia:'Ver asistencia', upload_manual:'Subir manual',
  delete_manual:'Eliminar manual', download_manual:'Descargar manual',
}
function labelAction(a) { return ACTION_LABELS[a] || a }

const ACTION_ICONS = {
  page_view:'ti-eye', login:'ti-login', logout:'ti-logout', login_failed:'ti-alert-circle',
  create_user:'ti-user-plus', update_user:'ti-user-edit', delete_user:'ti-user-minus',
  toggle_user:'ti-toggle-right', download_report:'ti-download', view_report:'ti-file-text',
  delete_report:'ti-trash', delete_photo:'ti-photo-off', view_photo:'ti-photo',
  view_record:'ti-clipboard', delete_record:'ti-trash', export_csv:'ti-table-export',
  change_permission:'ti-shield', change_config:'ti-settings', send_notification:'ti-bell',
  delete_notification:'ti-bell-off', view_asistencia:'ti-calendar', upload_manual:'ti-upload',
  delete_manual:'ti-trash', download_manual:'ti-download',
}
function actionIcon(a) { return ACTION_ICONS[a] || 'ti-dots' }

function actionColor(a) {
  if (!a) return 'gray'
  if (a.includes('delete') || a === 'login_failed') return 'red'
  if (a === 'login' || a.includes('create')) return 'green'
  if (a.includes('download') || a.includes('export')) return 'blue'
  if (a.includes('update') || a.includes('change') || a === 'toggle_user') return 'amber'
  return 'gray'
}

function badgeClass(a) { return `badge-${actionColor(a)}` }

function rowClass(a) {
  if (a?.startsWith('delete_') || a === 'login_failed') return 'tr-danger'
  if (a === 'login' || a?.includes('create')) return 'tr-success'
  return ''
}

let interval = null
watch(autoRefresh, (val) => {
  clearInterval(interval)
  if (val) interval = setInterval(load, 15000)
})

onMounted(async () => {
  filterOpts.value = await fetchFilters().catch(() => ({ actions: [], modules: [] }))
  load()
  interval = setInterval(load, 15000)
})
onUnmounted(() => clearInterval(interval))
</script>

<style scoped>
.shell {
  display: flex;
  min-height: 100vh;
  background: #06090f;
  position: relative;
}

/* ── Sidebar ─────────────────────────────── */
.sidebar {
  width: 230px;
  flex-shrink: 0;
  background: #0d1117;
  border-right: 1px solid rgba(255,255,255,0.06);
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow: hidden;
  transition: transform 0.25s ease;
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding: 1.1rem 1rem 1rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.brand-icon { flex-shrink: 0; }

.brand-name {
  font-size: 0.82rem;
  font-weight: 600;
  color: #e2e8f0;
  flex: 1;
  line-height: 1.2;
}

.close-sidebar {
  display: none;
  background: none;
  border: none;
  color: #8b949e;
  cursor: pointer;
  font-size: 18px;
  padding: 0;
}

.sidebar-nav {
  flex: 1;
  padding: 0.75rem 0.6rem;
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.55rem 0.75rem;
  border-radius: 8px;
  background: none;
  border: none;
  color: #8b949e;
  font-size: 0.83rem;
  font-family: inherit;
  cursor: pointer;
  text-align: left;
  transition: background 0.15s, color 0.15s;
  width: 100%;
}

.nav-item i { font-size: 16px; flex-shrink: 0; }
.nav-item:hover { background: rgba(255,255,255,0.05); color: #e2e8f0; }
.nav-item.active { background: rgba(26,110,245,0.15); color: #60a5fa; }

.sidebar-footer {
  padding: 0.75rem 0.75rem 1rem;
  border-top: 1px solid rgba(255,255,255,0.06);
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.live-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.78rem;
  color: #8b949e;
}

.live-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #475569;
  flex-shrink: 0;
}

.live-dot.on {
  background: #22c55e;
  box-shadow: 0 0 0 3px rgba(34,197,94,0.2);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 3px rgba(34,197,94,0.2); }
  50% { box-shadow: 0 0 0 6px rgba(34,197,94,0.08); }
}

.live-label { flex: 1; }

.toggle-live {
  background: none;
  border: none;
  color: #8b949e;
  cursor: pointer;
  font-size: 15px;
  padding: 0;
  display: flex;
}

.toggle-live:hover { color: #e2e8f0; }

.signout-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(248,81,73,0.1);
  border: 1px solid rgba(248,81,73,0.2);
  border-radius: 8px;
  color: #f85149;
  font-size: 0.82rem;
  font-family: inherit;
  padding: 0.45rem 0.75rem;
  cursor: pointer;
  transition: background 0.15s;
  width: 100%;
}

.signout-btn:hover { background: rgba(248,81,73,0.18); }
.signout-btn i { font-size: 15px; }

/* ── Main ─────────────────────────────────── */
.main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.topbar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.85rem 1.25rem;
  background: #0d1117;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  position: sticky;
  top: 0;
  z-index: 20;
}

.hamburger {
  display: none;
  background: none;
  border: none;
  color: #8b949e;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
}

.topbar-title {
  flex: 1;
  font-size: 0.95rem;
  font-weight: 600;
  color: #e2e8f0;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.last-update {
  font-size: 0.72rem;
  color: #475569;
}

.icon-btn {
  background: none;
  border: none;
  color: #8b949e;
  cursor: pointer;
  font-size: 18px;
  padding: 0;
  display: flex;
  transition: color 0.15s;
}

.icon-btn:hover:not(:disabled) { color: #e2e8f0; }
.icon-btn:disabled { opacity: 0.4; }

.spinning { animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Content ──────────────────────────────── */
.content-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* ── Stats grid ──────────────────────────── */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 0.75rem;
}

.stat-card {
  background: #0d1117;
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px;
  padding: 1rem 1.1rem;
  display: flex;
  align-items: center;
  gap: 0.85rem;
  transition: border-color 0.2s;
}

.stat-card:hover { border-color: rgba(255,255,255,0.14); }

.stat-icon {
  font-size: 22px;
  flex-shrink: 0;
}

.stat-icon.blue { color: #60a5fa; }
.stat-icon.green { color: #4ade80; }
.stat-icon.red { color: #f87171; }
.stat-icon.amber { color: #fbbf24; }
.stat-icon.gray { color: #8b949e; }

.stat-value {
  font-size: 1.4rem;
  font-weight: 600;
  color: #e2e8f0;
  line-height: 1.2;
}

.stat-label {
  font-size: 0.73rem;
  color: #8b949e;
  margin-top: 2px;
}

/* ── Filters ──────────────────────────────── */
.filters-section {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.filters-row {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
  align-items: center;
}

.search-wrap {
  position: relative;
  flex: 1;
  min-width: 180px;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #475569;
  font-size: 15px;
  pointer-events: none;
}

.search-input {
  width: 100%;
  background: #0d1117;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 8px;
  padding: 0.55rem 0.85rem 0.55rem 2.2rem;
  font-size: 0.85rem;
  color: #e2e8f0;
  font-family: inherit;
  outline: none;
  transition: border-color 0.18s;
}

.search-input::placeholder { color: #475569; }
.search-input:focus { border-color: rgba(26,110,245,0.5); }

.f-select, .f-date {
  background: #0d1117;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 8px;
  padding: 0.55rem 0.75rem;
  font-size: 0.83rem;
  color: #e2e8f0;
  font-family: inherit;
  outline: none;
  cursor: pointer;
  transition: border-color 0.18s;
}

.f-select:focus, .f-date:focus { border-color: rgba(26,110,245,0.5); }
.f-select option { background: #0d1117; }

.date-group {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.date-sep { color: #475569; font-size: 0.8rem; }

.clear-btn {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 8px;
  padding: 0.55rem 0.85rem;
  font-size: 0.83rem;
  color: #8b949e;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  white-space: nowrap;
}

.clear-btn:hover:not(:disabled) { background: rgba(255,255,255,0.08); color: #e2e8f0; }
.clear-btn:disabled { opacity: 0.35; cursor: not-allowed; }
.clear-btn i { font-size: 13px; }

.chips-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.chips-label {
  font-size: 0.75rem;
  color: #475569;
  font-weight: 500;
  flex-shrink: 0;
}

.chip {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px;
  padding: 0.25rem 0.65rem;
  font-size: 0.78rem;
  color: #8b949e;
  cursor: pointer;
  font-family: inherit;
  transition: background 0.15s, border-color 0.15s, color 0.15s;
}

.chip i { font-size: 13px; }
.chip:hover { background: rgba(255,255,255,0.08); color: #e2e8f0; }
.chip.active { background: rgba(26,110,245,0.12); border-color: rgba(26,110,245,0.3); color: #60a5fa; }
.chip-count { font-weight: 600; color: inherit; }

/* ── Table section ───────────────────────── */
.table-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.table-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.results-count { font-size: 0.82rem; color: #8b949e; }

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.pag-btn {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 6px;
  color: #8b949e;
  padding: 0.3rem 0.5rem;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  transition: background 0.15s, color 0.15s;
}

.pag-btn:hover:not(:disabled) { background: rgba(255,255,255,0.1); color: #e2e8f0; }
.pag-btn:disabled { opacity: 0.35; cursor: not-allowed; }
.pag-label { font-size: 0.8rem; color: #8b949e; white-space: nowrap; }

.table-wrap {
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px;
  overflow: hidden;
  overflow-x: auto;
}

.log-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.82rem;
  min-width: 700px;
}

.log-table thead {
  background: #0d1117;
  border-bottom: 1px solid rgba(255,255,255,0.07);
}

.log-table th {
  padding: 0.65rem 0.875rem;
  text-align: left;
  color: #475569;
  font-weight: 500;
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  white-space: nowrap;
}

.log-table tbody tr {
  border-bottom: 1px solid rgba(255,255,255,0.04);
  transition: background 0.12s;
}

.log-table tbody tr:last-child { border-bottom: none; }
.log-table tbody tr:hover { background: rgba(255,255,255,0.03); }
.log-table td { padding: 0.6rem 0.875rem; color: #cbd5e1; vertical-align: middle; }

.tr-danger { background: rgba(248,81,73,0.04); }
.tr-success { background: rgba(34,197,94,0.03); }

.td-ts { white-space: nowrap; }
.ts-date { display: block; font-size: 0.8rem; color: #e2e8f0; }
.ts-time { display: block; font-size: 0.72rem; color: #475569; margin-top: 1px; }

.td-usr { white-space: nowrap; }
.usr-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  font-size: 0.68rem;
  font-weight: 700;
  color: #fff;
  margin-right: 0.45rem;
  vertical-align: middle;
  flex-shrink: 0;
}

.usr-name { vertical-align: middle; font-weight: 500; color: #93c5fd; }

.td-module { color: #a78bfa; font-size: 0.8rem; }
.td-clip { max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.td-muted { color: #475569; font-size: 0.77rem; }

.col-detail { width: 220px; }
.col-target { width: 160px; }
.col-ip { width: 110px; }

/* Badges */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  border-radius: 6px;
  padding: 0.2rem 0.55rem;
  font-size: 0.72rem;
  font-weight: 500;
  white-space: nowrap;
}
.badge i { font-size: 12px; }

.badge-red { background: rgba(248,81,73,0.15); color: #f87171; }
.badge-green { background: rgba(34,197,94,0.15); color: #4ade80; }
.badge-blue { background: rgba(96,165,250,0.15); color: #60a5fa; }
.badge-amber { background: rgba(251,191,36,0.15); color: #fbbf24; }
.badge-gray { background: rgba(139,148,158,0.12); color: #8b949e; }

/* Expanded row */
.expanded-row td { background: #0d1117; padding: 0; }
.expanded-body {
  padding: 1rem 1rem 1rem 4rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 0.5rem 1.5rem;
}

.exp-field {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.exp-field span:first-child {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #475569;
  font-weight: 500;
}

.exp-field:last-child, .exp-field code {
  font-size: 0.78rem;
  color: #cbd5e1;
  word-break: break-all;
}

.ua-text { font-size: 0.72rem; color: #8b949e; }

code {
  font-family: 'Menlo', 'Monaco', monospace;
  background: rgba(255,255,255,0.05);
  border-radius: 4px;
  padding: 0.1rem 0.3rem;
  font-size: 0.73rem;
  color: #a78bfa;
}

/* Empty / skeleton */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 3rem 1rem;
  color: #475569;
  font-size: 0.85rem;
}

.empty-icon { font-size: 2.5rem; }

.skeleton-rows { width: 100%; display: flex; flex-direction: column; gap: 1px; }
.skeleton-row {
  height: 44px;
  background: linear-gradient(90deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.06) 50%, rgba(255,255,255,0.03) 100%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
}
@keyframes shimmer { to { background-position: -200% 0; } }

/* Pagination bottom */
.pagination-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.pag-btn-lg {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 8px;
  color: #8b949e;
  padding: 0.5rem 0.9rem;
  font-size: 0.82rem;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}

.pag-btn-lg:hover:not(:disabled) { background: rgba(255,255,255,0.1); color: #e2e8f0; }
.pag-btn-lg:disabled { opacity: 0.35; cursor: not-allowed; }

.pag-pages { display: flex; gap: 4px; flex-wrap: wrap; }

.pag-num {
  background: none;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 6px;
  color: #8b949e;
  padding: 0.3rem 0.6rem;
  font-size: 0.8rem;
  font-family: inherit;
  cursor: pointer;
  min-width: 34px;
  text-align: center;
  transition: background 0.12s, color 0.12s, border-color 0.12s;
}

.pag-num:hover:not(:disabled):not(.ellipsis) { background: rgba(255,255,255,0.08); color: #e2e8f0; }
.pag-num.active { background: rgba(26,110,245,0.2); border-color: rgba(26,110,245,0.4); color: #60a5fa; }
.pag-num.ellipsis { cursor: default; border-color: transparent; color: #475569; }

/* Sidebar overlay mobile */
.sidebar-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 30;
}

/* ── Responsive ──────────────────────────── */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    z-index: 40;
    transform: translateX(-100%);
  }

  .sidebar.open { transform: translateX(0); }
  .close-sidebar { display: flex; }
  .hamburger { display: flex; }
  .sidebar-overlay { display: block; }

  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .filters-row { flex-direction: column; align-items: stretch; }
  .search-wrap { min-width: 0; }
  .date-group { flex-wrap: wrap; }
  .f-select, .f-date { width: 100%; }
  .pagination-bottom { justify-content: center; }
  .pag-pages { justify-content: center; }
  .content-scroll { padding: 1rem; }
  .col-detail, .col-target, .col-ip { display: none; }
}

@media (max-width: 480px) {
  .stats-grid { grid-template-columns: 1fr 1fr; }
  .topbar { padding: 0.75rem 1rem; }
  .last-update { display: none; }
}
</style>
