<template>
  <div class="shell">
    <!-- ── Sidebar (escritorio) ───────────────────────── -->
    <aside class="sidebar">
      <div class="sidebar-head">
        <div class="brand-icon" aria-hidden="true">
          <svg width="26" height="26" viewBox="0 0 32 32" fill="none">
            <rect width="32" height="32" rx="10" fill="#1a6ef5"/>
            <path d="M16 7l7 4v10l-7 4-7-4V11l7-4z" stroke="#fff" stroke-width="1.6" stroke-linejoin="round" fill="none"/>
            <circle cx="16" cy="16" r="2.5" fill="#fff"/>
          </svg>
        </div>
        <div class="brand-txt">
          <span class="brand-name">Bitácora</span>
          <span class="brand-sub">PWASV · Auditoría</span>
        </div>
      </div>

      <nav class="sidebar-nav" aria-label="Categorías">
        <button
          v-for="c in categories"
          :key="c.key"
          class="nav-item"
          :class="{ active: activeCat === c.key }"
          @click="selectCategory(c.key)"
        >
          <i :class="`ti ${c.icon}`" aria-hidden="true"></i>
          <span class="nav-label">{{ c.label }}</span>
          <span class="nav-count">{{ catCount(c.key) }}</span>
        </button>
      </nav>

      <div class="sidebar-foot">
        <div class="live-row">
          <span class="live-dot" :class="{ on: autoRefresh }" aria-hidden="true"></span>
          <span>{{ autoRefresh ? 'En vivo' : 'Pausado' }}</span>
          <button class="mini-btn" @click="autoRefresh = !autoRefresh" :aria-label="autoRefresh ? 'Pausar' : 'Reanudar'">
            <i :class="autoRefresh ? 'ti ti-player-pause' : 'ti ti-player-play'" aria-hidden="true"></i>
          </button>
        </div>
        <button class="signout" @click="salir">
          <i class="ti ti-logout" aria-hidden="true"></i> Cerrar sesión
        </button>
      </div>
    </aside>

    <!-- ── Área principal ─────────────────────────────── -->
    <main class="main">
      <!-- Barra superior móvil -->
      <header class="topbar">
        <div class="tb-brand">
          <svg width="22" height="22" viewBox="0 0 32 32" fill="none" aria-hidden="true">
            <rect width="32" height="32" rx="10" fill="#1a6ef5"/>
            <path d="M16 7l7 4v10l-7 4-7-4V11l7-4z" stroke="#fff" stroke-width="1.6" stroke-linejoin="round" fill="none"/>
            <circle cx="16" cy="16" r="2.5" fill="#fff"/>
          </svg>
          <span>Bitácora</span>
        </div>
        <div class="tb-right">
          <button class="icon-btn" @click="load()" :disabled="loading" aria-label="Actualizar">
            <i class="ti ti-refresh" :class="{ spin: loading }" aria-hidden="true"></i>
          </button>
          <button class="icon-btn danger" @click="salir" aria-label="Salir">
            <i class="ti ti-logout" aria-hidden="true"></i>
          </button>
        </div>
      </header>

      <!-- Tabs de categoría (móvil) -->
      <div class="cat-tabs" role="tablist" aria-label="Categorías">
        <button
          v-for="c in categories"
          :key="c.key"
          class="cat-tab"
          :class="{ active: activeCat === c.key }"
          role="tab"
          :aria-selected="activeCat === c.key"
          @click="selectCategory(c.key)"
        >
          <i :class="`ti ${c.icon}`" aria-hidden="true"></i>
          {{ c.label }}
          <span class="cat-tab-count">{{ catCount(c.key) }}</span>
        </button>
      </div>

      <div class="content">
        <!-- Encabezado de la vista actual -->
        <div class="view-head">
          <div class="view-title-row">
            <span class="view-icon" :class="currentCat.color" aria-hidden="true">
              <i :class="`ti ${currentCat.icon}`"></i>
            </span>
            <div>
              <h1 class="view-title">{{ currentCat.label }}</h1>
              <p class="view-desc">{{ currentCat.desc }}</p>
            </div>
          </div>
          <div class="view-meta">
            <span class="last-upd"><i class="ti ti-clock" aria-hidden="true"></i> {{ lastUpdateLabel }}</span>
            <span class="total-pill">{{ fmtNum(data.total) }} registros</span>
          </div>
        </div>

        <!-- Filtros -->
        <div class="filters">
          <div class="search-wrap">
            <i class="ti ti-search" aria-hidden="true"></i>
            <input
              v-model="filters.usr"
              @input="debounceLoad"
              type="text"
              placeholder="Buscar administrador por nombre o usuario..."
              aria-label="Buscar administrador"
            />
            <button v-if="filters.usr" class="clear-x" @click="filters.usr=''; reloadFirst()" aria-label="Limpiar búsqueda">
              <i class="ti ti-x" aria-hidden="true"></i>
            </button>
          </div>
          <div class="filter-controls">
            <select v-if="catActions.length > 1" v-model="filters.action_type" @change="reloadFirst" class="f-ctrl" aria-label="Acción específica">
              <option value="">Toda acción</option>
              <option v-for="a in catActions" :key="a" :value="a">{{ labelAction(a) }}</option>
            </select>
            <input v-model="filters.date_from" @change="reloadFirst" type="date" class="f-ctrl" aria-label="Desde" title="Desde" />
            <input v-model="filters.date_to" @change="reloadFirst" type="date" class="f-ctrl" aria-label="Hasta" title="Hasta" />
            <button v-if="hasExtraFilters" class="reset-btn" @click="resetFilters">
              <i class="ti ti-filter-off" aria-hidden="true"></i> Limpiar
            </button>
          </div>
        </div>

        <!-- Tabla con scroll interno -->
        <div class="table-card">
          <div class="table-scroll">
            <table class="log-table">
              <thead>
                <tr>
                  <th class="c-time">Fecha y hora</th>
                  <th class="c-user">Administrador</th>
                  <th class="c-act">Acción</th>
                  <th class="c-detail">¿Qué hizo?</th>
                  <th class="c-mod">Módulo</th>
                  <th class="c-res">Resultado</th>
                  <th class="c-ip">IP</th>
                </tr>
              </thead>
              <tbody>
                <template v-if="loading && !data.data.length">
                  <tr v-for="n in 10" :key="'sk'+n" class="skeleton">
                    <td colspan="7"><div class="sk-bar"></div></td>
                  </tr>
                </template>

                <tr v-else-if="!data.data.length">
                  <td colspan="7">
                    <div class="empty">
                      <i class="ti ti-mood-empty" aria-hidden="true"></i>
                      <p>Sin eventos en esta vista</p>
                      <button v-if="hasAnyFilter" class="reset-btn" @click="resetFilters">Quitar filtros</button>
                    </div>
                  </td>
                </tr>

                <template v-for="row in data.data" :key="row.id" v-else>
                  <tr class="data-row" :class="rowClass(row.action_type)" @click="toggleRow(row.id)">
                    <td class="c-time">
                      <span class="t-date">{{ formatDate(row.ts) }}</span>
                      <span class="t-time">{{ formatTime(row.ts) }}</span>
                    </td>
                    <td class="c-user">
                      <div class="user-cell">
                        <span class="avatar" :style="usrColor(row.usr_nombre || row.usr)" aria-hidden="true">
                          {{ ((row.usr_nombre || row.usr || '?')[0]).toUpperCase() }}
                        </span>
                        <span class="user-txt">
                          <span class="user-name">{{ row.usr_nombre || row.usr || '—' }}</span>
                          <span class="user-sub">@{{ row.usr || '?' }}<template v-if="row.usr_rol"> · {{ row.usr_rol }}</template></span>
                        </span>
                      </div>
                    </td>
                    <td class="c-act">
                      <span class="badge" :class="badgeClass(row.action_type)">
                        <i :class="`ti ${actionIcon(row.action_type)}`" aria-hidden="true"></i>
                        <span class="badge-txt">{{ labelAction(row.action_type) }}</span>
                      </span>
                    </td>
                    <td class="c-detail">
                      <span class="detail-txt">{{ row.detail || labelAction(row.action_type) }}</span>
                    </td>
                    <td class="c-mod"><span class="mod-pill">{{ row.module || '—' }}</span></td>
                    <td class="c-res">
                      <span v-if="row.http_status" class="res" :class="statusClass(row.http_status)">
                        {{ statusDot(row.http_status) }} {{ statusText(row.http_status) }}
                      </span>
                      <span v-else class="res st-neutral">—</span>
                    </td>
                    <td class="c-ip">{{ row.ip_hint || '—' }}</td>
                  </tr>

                  <tr v-if="expandedRow === row.id" :key="'x'+row.id" class="exp-row">
                    <td colspan="7">
                      <div class="exp-grid">
                        <div class="exp-f"><span>Evento</span> #{{ row.id }}</div>
                        <div class="exp-f wide"><span>Fecha exacta</span> {{ formatFull(row.ts) }}</div>
                        <div class="exp-f"><span>Administrador</span> {{ row.usr_nombre || '—' }} (@{{ row.usr || '?' }})</div>
                        <div class="exp-f"><span>Rol</span> {{ row.usr_rol || '—' }}</div>
                        <div class="exp-f" v-if="row.usr_cargo"><span>Cargo</span> {{ row.usr_cargo }}</div>
                        <div class="exp-f" v-if="row.usr_territorio"><span>Territorio</span> {{ row.usr_territorio }}</div>
                        <div class="exp-f wide"><span>Acción realizada</span> {{ row.detail || labelAction(row.action_type) }}</div>
                        <div class="exp-f"><span>Petición</span> <code v-if="row.http_method">{{ row.http_method }} {{ row.http_path }}</code><span v-else>—</span></div>
                        <div class="exp-f"><span>Resultado</span>
                          <span :class="statusClass(row.http_status)">{{ row.http_status || '—' }} {{ statusText(row.http_status) }}</span>
                        </div>
                        <div class="exp-f"><span>IP</span> {{ row.ip_hint || '—' }}</div>
                        <div class="exp-f"><span>Origen</span>
                          <span :class="row.source === 'backend' ? 'src-ok' : 'src-cl'">
                            {{ row.source === 'backend' ? '🔒 Verificado en servidor' : '○ Reportado por cliente' }}
                          </span>
                        </div>
                        <div class="exp-f wide" v-if="row.ua"><span>Dispositivo</span> <span class="ua">{{ row.ua }}</span></div>
                      </div>
                    </td>
                  </tr>
                </template>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Paginación -->
        <div class="pagination" v-if="totalPages > 1">
          <button class="pg-btn" :disabled="page <= 1" @click="prevPage">
            <i class="ti ti-chevron-left" aria-hidden="true"></i> Anterior
          </button>
          <div class="pg-nums">
            <button
              v-for="p in pageNumbers"
              :key="p"
              class="pg-num"
              :class="{ active: p === page, dots: p === '…' }"
              :disabled="p === '…'"
              @click="p !== '…' && goToPage(p)"
            >{{ p }}</button>
          </div>
          <button class="pg-btn" :disabled="page >= totalPages" @click="nextPage">
            Siguiente <i class="ti ti-chevron-right" aria-hidden="true"></i>
          </button>
        </div>
      </div>
    </main>
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
const expandedRow = ref(null)
const lastUpdate = ref(new Date())
const activeCat = ref('')
const filters = reactive({ usr: '', action_type: '', category: '', module: '', source: '', date_from: '', date_to: '' })

// ── Categorías (vistas separadas) ──────────────────────────────
const categories = [
  { key: '',          label: 'Todos',      icon: 'ti-stack-2',     color: 'c-gray',  desc: 'Toda la actividad registrada en el panel administrativo' },
  { key: 'accesos',   label: 'Accesos',    icon: 'ti-login-2',     color: 'c-blue',  desc: 'Inicios de sesión, intentos fallidos y vistas consultadas' },
  { key: 'creaciones',label: 'Creaciones', icon: 'ti-circle-plus', color: 'c-green', desc: 'Altas de usuarios, administradores y envíos' },
  { key: 'ediciones', label: 'Ediciones',  icon: 'ti-edit',        color: 'c-amber', desc: 'Modificaciones de datos, roles, permisos y contraseñas' },
  { key: 'borrados',  label: 'Borrados',   icon: 'ti-trash',       color: 'c-red',   desc: 'Eliminaciones de usuarios, reportes, imágenes y registros' },
  { key: 'descargas', label: 'Descargas',  icon: 'ti-download',    color: 'c-purple',desc: 'Descargas de reportes y exportaciones de datos' },
]
const currentCat = computed(() => categories.find(c => c.key === activeCat.value) || categories[0])

const ACTION_CATEGORY = {
  login:'accesos', logout:'accesos', login_fallido:'accesos', login_bloqueado:'accesos', acceso_vista:'accesos',
  crear_admin:'creaciones', crear_usuario:'creaciones', enviar_notif:'creaciones', guardar_reporte:'creaciones',
  firmar_reporte:'creaciones', asignar_tecnico:'creaciones', transferir_activ:'creaciones', reset_territorios:'creaciones', crear:'creaciones',
  editar_admin:'ediciones', editar_usuario:'ediciones', editar_registro:'ediciones', editar_asistencia:'ediciones',
  editar_notif:'ediciones', cambiar_rol:'ediciones', cambiar_rol_admin:'ediciones', cambiar_pwd:'ediciones',
  cambiar_pwd_admin:'ediciones', cambiar_cargo:'ediciones', cambiar_territorio:'ediciones', cambiar_facilitador:'ediciones',
  estado_admin:'ediciones', estado_usuario:'ediciones', quitar_firma:'ediciones', desasignar_tecnico:'ediciones', actualizar:'ediciones',
  eliminar_admin:'borrados', eliminar_todos_admin:'borrados', eliminar_usuario:'borrados', eliminar_reporte:'borrados',
  eliminar_notif:'borrados', eliminar_imgs_todas:'borrados', eliminar_imgs_fecha:'borrados', eliminar_registro:'borrados',
  eliminar_regs_todos:'borrados', eliminar_asistencia:'borrados', eliminar_asis_todas:'borrados', eliminar:'borrados',
  descargar_reporte:'descargas', descargar_zip:'descargas', descargar_pdf_stats:'descargas',
  exportar_csv:'descargas', exportar_usuarios:'descargas', descargar_bd:'descargas',
}

function catCount(key) {
  const stats = data.value.stats || []
  if (!key) return stats.reduce((s, x) => s + x.count, 0)
  return stats.filter(x => ACTION_CATEGORY[x.action] === key).reduce((s, x) => s + x.count, 0)
}

const catActions = computed(() => {
  if (!activeCat.value) return []
  return (filterOpts.value.actions || []).filter(a => ACTION_CATEGORY[a] === activeCat.value)
})

const totalPages = computed(() => Math.max(1, Math.ceil((data.value.total || 0) / limit)))
const hasExtraFilters = computed(() => !!(filters.action_type || filters.date_from || filters.date_to))
const hasAnyFilter = computed(() => !!(filters.usr || filters.action_type || filters.date_from || filters.date_to))

const lastUpdateLabel = computed(() => {
  const d = Math.floor((Date.now() - lastUpdate.value) / 1000)
  if (d < 5) return 'Actualizado ahora'
  if (d < 60) return `Hace ${d}s`
  return `Hace ${Math.floor(d / 60)} min`
})

const pageNumbers = computed(() => {
  const total = totalPages.value, cur = page.value
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1)
  const pages = []
  if (cur > 3) { pages.push(1); if (cur > 4) pages.push('…') }
  for (let p = Math.max(1, cur - 1); p <= Math.min(total, cur + 1); p++) pages.push(p)
  if (cur < total - 2) { if (cur < total - 3) pages.push('…'); pages.push(total) }
  return pages
})

function selectCategory(key) {
  activeCat.value = key
  filters.category = key
  filters.action_type = ''
  page.value = 1
  expandedRow.value = null
  load()
}

let debounceTimer = null
function debounceLoad() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => { page.value = 1; load() }, 380)
}
function reloadFirst() { page.value = 1; load() }

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

function toggleRow(id) { expandedRow.value = expandedRow.value === id ? null : id }
function prevPage() { if (page.value > 1) { page.value--; load() } }
function nextPage() { if (page.value < totalPages.value) { page.value++; load() } }
function goToPage(p) { page.value = p; load() }

function resetFilters() {
  filters.usr = ''; filters.action_type = ''; filters.date_from = ''; filters.date_to = ''
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
function formatFull(ts) {
  if (!ts) return '—'
  return new Date(ts).toLocaleString('es-MX', { timeZone: 'America/Mexico_City', weekday: 'long',
    day: '2-digit', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }) + ' (CDMX)'
}

function statusClass(s) {
  if (!s) return 'st-neutral'
  if (s >= 200 && s < 300) return 'st-ok'
  if (s >= 400 && s < 500) return 'st-warn'
  if (s >= 500) return 'st-err'
  return 'st-neutral'
}
function statusDot(s) {
  if (s >= 200 && s < 300) return '●'
  if (s >= 400) return '●'
  return '○'
}
function statusText(s) {
  if (!s) return ''
  if (s >= 200 && s < 300) return 'Exitoso'
  if (s === 400 || s === 401 || s === 403) return 'Denegado'
  if (s === 404) return 'No encontrado'
  if (s === 422) return 'Datos inválidos'
  if (s >= 500) return 'Error'
  return ''
}

const USR_COLORS = ['#1a6ef5','#0ea5e9','#8b5cf6','#10b981','#f59e0b','#ef4444','#ec4899','#14b8a6']
function usrColor(usr) {
  if (!usr) return 'background:#475569'
  const i = usr.split('').reduce((a, c) => a + c.charCodeAt(0), 0) % USR_COLORS.length
  return `background:${USR_COLORS[i]}`
}

const ACTION_LABELS = {
  login:'Inició sesión', logout:'Cerró sesión', login_fallido:'Acceso fallido', login_bloqueado:'Acceso bloqueado', acceso_vista:'Accedió a vista',
  crear_admin:'Creó administrador', editar_admin:'Editó administrador', eliminar_admin:'Eliminó administrador',
  eliminar_todos_admin:'Eliminó TODOS los admin', cambiar_rol_admin:'Cambió rol de admin', cambiar_pwd_admin:'Cambió contraseña admin', estado_admin:'Activó/desactivó admin',
  crear_usuario:'Creó usuario', editar_usuario:'Editó usuario', eliminar_usuario:'Eliminó usuario',
  cambiar_rol:'Cambió rol', cambiar_pwd:'Cambió contraseña', cambiar_cargo:'Cambió cargo',
  estado_usuario:'Activó/desactivó usuario', cambiar_territorio:'Cambió territorio',
  cambiar_facilitador:'Cambió facilitador', transferir_activ:'Transfirió actividades', exportar_usuarios:'Exportó usuarios',
  eliminar_reporte:'Eliminó reporte', descargar_reporte:'Descargó reporte', descargar_zip:'Descargó ZIP', descargar_pdf_stats:'Descargó PDF',
  firmar_reporte:'Firmó reporte', quitar_firma:'Quitó firma', guardar_reporte:'Guardó reporte',
  asignar_tecnico:'Asignó técnico', desasignar_tecnico:'Desasignó técnico',
  enviar_notif:'Envió notificación', editar_notif:'Editó notificación', eliminar_notif:'Eliminó notificación',
  eliminar_imgs_todas:'Eliminó todas las imágenes', eliminar_imgs_fecha:'Eliminó imágenes por fecha',
  editar_registro:'Editó registro', eliminar_registro:'Eliminó registro', eliminar_regs_todos:'Eliminó todos los registros',
  exportar_csv:'Exportó CSV', editar_asistencia:'Editó asistencia', eliminar_asistencia:'Eliminó asistencia', eliminar_asis_todas:'Eliminó todas las asistencias',
  descargar_bd:'Descargó base de datos', reset_territorios:'Reinició territorios',
  crear:'Creó', actualizar:'Actualizó', eliminar:'Eliminó',
}
function labelAction(a) { return ACTION_LABELS[a] || a }

const ACTION_ICONS = {
  login:'ti-login-2', logout:'ti-logout-2', login_fallido:'ti-alert-triangle', login_bloqueado:'ti-lock', acceso_vista:'ti-eye',
  crear_admin:'ti-user-shield', editar_admin:'ti-user-cog', eliminar_admin:'ti-user-x', eliminar_todos_admin:'ti-users-minus',
  cambiar_rol_admin:'ti-shield-cog', cambiar_pwd_admin:'ti-key', estado_admin:'ti-toggle-right',
  crear_usuario:'ti-user-plus', editar_usuario:'ti-user-edit', eliminar_usuario:'ti-user-minus',
  cambiar_rol:'ti-id-badge', cambiar_pwd:'ti-key', cambiar_cargo:'ti-briefcase', estado_usuario:'ti-toggle-right',
  cambiar_territorio:'ti-map-pin', cambiar_facilitador:'ti-arrows-exchange', transferir_activ:'ti-transfer', exportar_usuarios:'ti-table-export',
  eliminar_reporte:'ti-file-x', descargar_reporte:'ti-download', descargar_zip:'ti-file-zip', descargar_pdf_stats:'ti-file-type-pdf',
  firmar_reporte:'ti-signature', quitar_firma:'ti-eraser', guardar_reporte:'ti-file-text',
  asignar_tecnico:'ti-user-check', desasignar_tecnico:'ti-user-off',
  enviar_notif:'ti-bell', editar_notif:'ti-bell-cog', eliminar_notif:'ti-bell-off',
  eliminar_imgs_todas:'ti-photo-off', eliminar_imgs_fecha:'ti-photo-minus',
  editar_registro:'ti-edit', eliminar_registro:'ti-trash', eliminar_regs_todos:'ti-trash-x',
  exportar_csv:'ti-table-export', editar_asistencia:'ti-calendar-cog', eliminar_asistencia:'ti-calendar-minus', eliminar_asis_todas:'ti-calendar-x',
  descargar_bd:'ti-database-export', reset_territorios:'ti-refresh-alert',
  crear:'ti-plus', actualizar:'ti-edit', eliminar:'ti-trash',
}
function actionIcon(a) { return ACTION_ICONS[a] || 'ti-point' }

const _DANGER = new Set(['login_fallido','login_bloqueado','eliminar_admin','eliminar_todos_admin','eliminar_usuario','eliminar_reporte','eliminar_notif','eliminar_imgs_todas','eliminar_imgs_fecha','eliminar_registro','eliminar_regs_todos','eliminar_asistencia','eliminar_asis_todas','quitar_firma','descargar_bd','reset_territorios','eliminar'])
const _SUCCESS = new Set(['login','crear_admin','crear_usuario','crear','firmar_reporte','asignar_tecnico','enviar_notif','guardar_reporte'])
const _BLUE = new Set(['descargar_reporte','descargar_zip','descargar_pdf_stats','exportar_csv','exportar_usuarios'])
const _AMBER = new Set(['editar_admin','editar_usuario','editar_registro','editar_asistencia','editar_notif','cambiar_rol','cambiar_rol_admin','cambiar_pwd','cambiar_pwd_admin','cambiar_cargo','cambiar_territorio','cambiar_facilitador','estado_admin','estado_usuario','actualizar','transferir_activ'])
function actionColor(a) {
  if (!a) return 'gray'
  if (_DANGER.has(a)) return 'red'
  if (_SUCCESS.has(a)) return 'green'
  if (_BLUE.has(a)) return 'blue'
  if (_AMBER.has(a)) return 'amber'
  return 'gray'
}
function badgeClass(a) { return `badge-${actionColor(a)}` }
function rowClass(a) {
  if (_DANGER.has(a)) return 'r-danger'
  if (_SUCCESS.has(a)) return 'r-success'
  return ''
}

let interval = null
watch(autoRefresh, (v) => { clearInterval(interval); if (v) interval = setInterval(load, 15000) })

onMounted(async () => {
  filterOpts.value = await fetchFilters().catch(() => ({ actions: [], modules: [] }))
  load()
  interval = setInterval(load, 15000)
})
onUnmounted(() => clearInterval(interval))
</script>

<style scoped>
.shell { display: flex; min-height: 100vh; max-height: 100vh; background: #06090f; overflow: hidden; }

/* ── Sidebar ─────────────────────────── */
.sidebar { width: 244px; flex-shrink: 0; background: #0b0f16; border-right: 1px solid rgba(255,255,255,0.06); display: flex; flex-direction: column; }
.sidebar-head { display: flex; align-items: center; gap: 0.7rem; padding: 1.15rem 1rem; border-bottom: 1px solid rgba(255,255,255,0.06); }
.brand-txt { display: flex; flex-direction: column; line-height: 1.25; }
.brand-name { font-size: 0.95rem; font-weight: 600; color: #f1f5f9; }
.brand-sub { font-size: 0.68rem; color: #64748b; }
.sidebar-nav { flex: 1; padding: 0.75rem 0.55rem; display: flex; flex-direction: column; gap: 3px; overflow-y: auto; }
.nav-item { display: flex; align-items: center; gap: 0.7rem; padding: 0.62rem 0.7rem; border-radius: 9px; background: none; border: none; color: #94a3b8; font-size: 0.86rem; font-family: inherit; cursor: pointer; text-align: left; width: 100%; transition: background .15s, color .15s; }
.nav-item i { font-size: 18px; flex-shrink: 0; }
.nav-label { flex: 1; }
.nav-count { font-size: 0.72rem; font-weight: 600; color: #64748b; background: rgba(255,255,255,0.05); padding: 1px 8px; border-radius: 10px; min-width: 24px; text-align: center; }
.nav-item:hover { background: rgba(255,255,255,0.04); color: #e2e8f0; }
.nav-item.active { background: rgba(26,110,245,0.14); color: #60a5fa; }
.nav-item.active .nav-count { background: rgba(26,110,245,0.25); color: #93c5fd; }
.sidebar-foot { padding: 0.75rem; border-top: 1px solid rgba(255,255,255,0.06); display: flex; flex-direction: column; gap: 0.6rem; }
.live-row { display: flex; align-items: center; gap: 0.5rem; font-size: 0.78rem; color: #94a3b8; }
.live-dot { width: 7px; height: 7px; border-radius: 50%; background: #475569; flex-shrink: 0; }
.live-dot.on { background: #22c55e; box-shadow: 0 0 0 3px rgba(34,197,94,.18); animation: pulse 2s infinite; }
@keyframes pulse { 50% { box-shadow: 0 0 0 6px rgba(34,197,94,.05); } }
.live-row span:nth-child(2) { flex: 1; }
.mini-btn { background: none; border: none; color: #94a3b8; cursor: pointer; font-size: 15px; display: flex; }
.mini-btn:hover { color: #e2e8f0; }
.signout { display: flex; align-items: center; justify-content: center; gap: 0.5rem; background: rgba(248,81,73,0.1); border: 1px solid rgba(248,81,73,0.2); border-radius: 8px; color: #f87171; font-size: 0.82rem; font-family: inherit; padding: 0.5rem; cursor: pointer; transition: background .15s; }
.signout:hover { background: rgba(248,81,73,0.18); }

/* ── Main ─────────────────────────────── */
.main { flex: 1; min-width: 0; display: flex; flex-direction: column; max-height: 100vh; }
.topbar { display: none; align-items: center; justify-content: space-between; padding: 0.7rem 1rem; background: #0b0f16; border-bottom: 1px solid rgba(255,255,255,0.06); }
.tb-brand { display: flex; align-items: center; gap: 0.5rem; font-size: 0.95rem; font-weight: 600; color: #f1f5f9; }
.tb-right { display: flex; gap: 0.4rem; }
.icon-btn { width: 34px; height: 34px; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #94a3b8; font-size: 17px; cursor: pointer; }
.icon-btn.danger { color: #f87171; border-color: rgba(248,81,73,0.25); }
.icon-btn:disabled { opacity: .4; }
.spin { animation: spin .8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.cat-tabs { display: none; gap: 6px; padding: 0.6rem 0.75rem; overflow-x: auto; background: #0b0f16; border-bottom: 1px solid rgba(255,255,255,0.06); -webkit-overflow-scrolling: touch; }
.cat-tabs::-webkit-scrollbar { height: 0; }
.cat-tab { display: flex; align-items: center; gap: 5px; white-space: nowrap; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; padding: 0.4rem 0.8rem; font-size: 0.8rem; color: #94a3b8; font-family: inherit; cursor: pointer; flex-shrink: 0; }
.cat-tab i { font-size: 15px; }
.cat-tab.active { background: rgba(26,110,245,0.16); border-color: rgba(26,110,245,0.4); color: #60a5fa; }
.cat-tab-count { font-size: 0.7rem; font-weight: 600; opacity: .8; }

.content { flex: 1; min-height: 0; display: flex; flex-direction: column; gap: 1rem; padding: 1.25rem; overflow: hidden; }

/* Encabezado de vista */
.view-head { display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }
.view-title-row { display: flex; align-items: center; gap: 0.85rem; }
.view-icon { width: 44px; height: 44px; flex-shrink: 0; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 22px; }
.view-icon.c-gray { background: rgba(148,163,184,.14); color: #cbd5e1; }
.view-icon.c-blue { background: rgba(56,189,248,.14); color: #38bdf8; }
.view-icon.c-green { background: rgba(74,222,128,.14); color: #4ade80; }
.view-icon.c-amber { background: rgba(251,191,36,.14); color: #fbbf24; }
.view-icon.c-red { background: rgba(248,113,113,.14); color: #f87171; }
.view-icon.c-purple { background: rgba(167,139,250,.14); color: #a78bfa; }
.view-title { font-size: 1.25rem; font-weight: 600; color: #f1f5f9; line-height: 1.2; }
.view-desc { font-size: 0.82rem; color: #64748b; margin-top: 2px; max-width: 540px; }
.view-meta { display: flex; align-items: center; gap: 0.6rem; }
.last-upd { display: flex; align-items: center; gap: 4px; font-size: 0.74rem; color: #475569; }
.last-upd i { font-size: 13px; }
.total-pill { font-size: 0.78rem; font-weight: 600; color: #93c5fd; background: rgba(26,110,245,0.12); border: 1px solid rgba(26,110,245,0.2); padding: 0.25rem 0.7rem; border-radius: 8px; }

/* Filtros */
.filters { display: flex; gap: 0.6rem; flex-wrap: wrap; align-items: center; }
.search-wrap { position: relative; flex: 1; min-width: 220px; display: flex; align-items: center; }
.search-wrap > i { position: absolute; left: 0.8rem; color: #475569; font-size: 16px; pointer-events: none; }
.search-wrap input { width: 100%; background: #0d1117; border: 1px solid rgba(255,255,255,0.08); border-radius: 9px; padding: 0.6rem 2.2rem; font-size: 0.86rem; color: #e2e8f0; font-family: inherit; outline: none; transition: border-color .18s; }
.search-wrap input::placeholder { color: #475569; }
.search-wrap input:focus { border-color: rgba(26,110,245,0.5); }
.clear-x { position: absolute; right: 0.6rem; background: none; border: none; color: #64748b; cursor: pointer; font-size: 15px; display: flex; }
.clear-x:hover { color: #e2e8f0; }
.filter-controls { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.f-ctrl { background: #0d1117; border: 1px solid rgba(255,255,255,0.08); border-radius: 9px; padding: 0.55rem 0.7rem; font-size: 0.82rem; color: #e2e8f0; font-family: inherit; outline: none; cursor: pointer; }
.f-ctrl:focus { border-color: rgba(26,110,245,0.5); }
.f-ctrl option { background: #0d1117; }
.reset-btn { display: flex; align-items: center; gap: 5px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 9px; padding: 0.55rem 0.8rem; font-size: 0.82rem; color: #94a3b8; font-family: inherit; cursor: pointer; }
.reset-btn:hover { background: rgba(255,255,255,0.08); color: #e2e8f0; }

/* Tabla con scroll interno */
.table-card { flex: 1; min-height: 0; background: #0a0e15; border: 1px solid rgba(255,255,255,0.07); border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; }
.table-scroll { flex: 1; min-height: 0; overflow: auto; }
.table-scroll::-webkit-scrollbar { width: 10px; height: 10px; }
.table-scroll::-webkit-scrollbar-track { background: transparent; }
.table-scroll::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 6px; border: 2px solid #0a0e15; }
.table-scroll::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.18); }

.log-table { width: 100%; border-collapse: collapse; font-size: 0.83rem; min-width: 920px; }
.log-table thead th { position: sticky; top: 0; z-index: 2; background: #0d1219; padding: 0.7rem 0.9rem; text-align: left; color: #64748b; font-weight: 500; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.06em; white-space: nowrap; border-bottom: 1px solid rgba(255,255,255,0.08); }
.data-row { border-bottom: 1px solid rgba(255,255,255,0.04); cursor: pointer; transition: background .12s; }
.data-row:hover { background: rgba(255,255,255,0.025); }
.data-row.r-danger { background: rgba(248,81,73,0.045); }
.data-row.r-danger:hover { background: rgba(248,81,73,0.075); }
.data-row.r-success { background: rgba(34,197,94,0.03); }
.log-table td { padding: 0.6rem 0.9rem; color: #cbd5e1; vertical-align: middle; }

.c-time { white-space: nowrap; width: 140px; }
.t-date { display: block; font-size: 0.8rem; color: #e2e8f0; }
.t-time { display: block; font-size: 0.72rem; color: #475569; margin-top: 1px; font-variant-numeric: tabular-nums; }

.c-user { width: 200px; }
.user-cell { display: flex; align-items: center; gap: 0.55rem; }
.avatar { width: 30px; height: 30px; flex-shrink: 0; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.78rem; font-weight: 700; color: #fff; }
.user-txt { display: flex; flex-direction: column; line-height: 1.25; min-width: 0; }
.user-name { font-weight: 500; color: #e2e8f0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 150px; }
.user-sub { font-size: 0.68rem; color: #475569; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 150px; }

.c-act { width: 180px; }
.badge { display: inline-flex; align-items: center; gap: 0.35rem; border-radius: 7px; padding: 0.28rem 0.6rem; font-size: 0.74rem; font-weight: 500; white-space: nowrap; }
.badge i { font-size: 13px; }
.badge-red { background: rgba(248,81,73,0.15); color: #f87171; }
.badge-green { background: rgba(34,197,94,0.15); color: #4ade80; }
.badge-blue { background: rgba(96,165,250,0.15); color: #60a5fa; }
.badge-amber { background: rgba(251,191,36,0.15); color: #fbbf24; }
.badge-gray { background: rgba(148,163,184,0.12); color: #94a3b8; }

.c-detail { min-width: 200px; }
.detail-txt { color: #cbd5e1; }
.c-mod { width: 130px; }
.mod-pill { font-size: 0.74rem; color: #a78bfa; background: rgba(167,139,250,0.1); padding: 0.18rem 0.55rem; border-radius: 6px; white-space: nowrap; }
.c-res { width: 130px; white-space: nowrap; }
.res { font-size: 0.76rem; font-weight: 500; }
.st-ok { color: #4ade80; }
.st-warn { color: #fbbf24; }
.st-err { color: #f87171; }
.st-neutral { color: #64748b; }
.c-ip { width: 120px; font-size: 0.76rem; color: #475569; font-variant-numeric: tabular-nums; white-space: nowrap; }

/* Fila expandida */
.exp-row td { background: #0d1219; padding: 0; }
.exp-grid { padding: 1rem 1.25rem; display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 0.65rem 1.5rem; }
.exp-f { display: flex; flex-direction: column; gap: 2px; font-size: 0.8rem; color: #cbd5e1; }
.exp-f.wide { grid-column: 1 / -1; }
.exp-f span:first-child { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.05em; color: #475569; font-weight: 500; }
.exp-f code { font-family: 'Menlo','Monaco',monospace; background: rgba(255,255,255,0.05); border-radius: 5px; padding: 0.12rem 0.4rem; font-size: 0.74rem; color: #93c5fd; word-break: break-all; }
.ua { font-size: 0.72rem; color: #64748b; word-break: break-word; }
.src-ok { color: #4ade80; font-weight: 500; }
.src-cl { color: #94a3b8; }

/* Skeleton / vacío */
.skeleton td { padding: 0.55rem 0.9rem; }
.sk-bar { height: 28px; border-radius: 6px; background: linear-gradient(90deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.07) 50%, rgba(255,255,255,0.03) 100%); background-size: 200% 100%; animation: shimmer 1.4s infinite; }
@keyframes shimmer { to { background-position: -200% 0; } }
.empty { display: flex; flex-direction: column; align-items: center; gap: 0.7rem; padding: 3.5rem 1rem; color: #475569; }
.empty i { font-size: 2.6rem; }
.empty p { font-size: 0.9rem; }

/* Paginación */
.pagination { display: flex; align-items: center; justify-content: center; gap: 0.6rem; flex-wrap: wrap; }
.pg-btn { display: flex; align-items: center; gap: 4px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #94a3b8; padding: 0.45rem 0.85rem; font-size: 0.82rem; font-family: inherit; cursor: pointer; }
.pg-btn:hover:not(:disabled) { background: rgba(255,255,255,0.08); color: #e2e8f0; }
.pg-btn:disabled { opacity: .35; cursor: not-allowed; }
.pg-nums { display: flex; gap: 4px; }
.pg-num { min-width: 34px; background: none; border: 1px solid rgba(255,255,255,0.08); border-radius: 7px; color: #94a3b8; padding: 0.4rem 0.55rem; font-size: 0.8rem; font-family: inherit; cursor: pointer; }
.pg-num:hover:not(:disabled):not(.dots) { background: rgba(255,255,255,0.08); color: #e2e8f0; }
.pg-num.active { background: rgba(26,110,245,0.2); border-color: rgba(26,110,245,0.4); color: #60a5fa; }
.pg-num.dots { border-color: transparent; cursor: default; }

/* ── Responsive ──────────────────────── */
@media (max-width: 900px) {
  .sidebar { display: none; }
  .topbar { display: flex; }
  .cat-tabs { display: flex; }
  .content { padding: 0.9rem; }
  .view-icon { width: 38px; height: 38px; font-size: 18px; }
  .view-title { font-size: 1.05rem; }
  .view-desc { display: none; }
}
@media (max-width: 560px) {
  .filter-controls { width: 100%; }
  .f-ctrl { flex: 1; }
  .view-meta { width: 100%; justify-content: space-between; }
  .log-table { min-width: 560px; }
  .c-mod, .c-ip { display: none; }
}
</style>
