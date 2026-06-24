// Servicio de telemetría de la plataforma.
// Captura eventos que ocurren solo del lado del cliente (navegación entre vistas
// y cierre de sesión). Las acciones de datos (crear/editar/eliminar/descargar)
// se registran de forma autoritativa en el backend mediante middleware.
import { API_URL } from '../config/api.js'

const _ep = `${API_URL}/sys/ping`

let _sid = sessionStorage.getItem('_asid')
if (!_sid) {
  _sid = Math.random().toString(36).slice(2) + Date.now().toString(36)
  sessionStorage.setItem('_asid', _sid)
}

function _identity() {
  try {
    const raw = localStorage.getItem('admin_user_data')
    if (!raw) {
      const u = localStorage.getItem('admin_user')
      return { usr: u || null }
    }
    const d = JSON.parse(raw)
    return {
      usr: d.username || d.correo || null,
      usr_id: d.id || null,
      usr_nombre: d.nombre_completo || null,
      usr_rol: d.rol || null,
      usr_territorio: d.territorio || null,
      usr_cargo: d.cargo || null,
    }
  } catch (_) {
    return { usr: null }
  }
}

async function track(action_type, module, detail = null, opts = {}) {
  try {
    await fetch(_ep, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ..._identity(),
        action_type,
        module,
        detail,
        target_id: opts.target_id != null ? String(opts.target_id) : null,
        target_label: opts.target_label || null,
        session_id: _sid,
        extra: opts.extra || null,
      }),
      keepalive: true,
    })
  } catch (_) {
    // silencioso: la telemetría nunca debe romper la app
  }
}

// Nombres legibles de cada vista para la bitácora
const VIEW_LABELS = {
  'Dashboard': 'Panel principal',
  'Usuarios': 'Gestión de usuarios',
  'Historiales': 'Historiales',
  'Reportes': 'Reportes',
  'Registros': 'Registros',
  'Configuracion': 'Configuración',
  'Asistencia': 'Asistencias',
  'VisorMap': 'Visor de mapa',
  'Notificaciones': 'Notificaciones',
  'Permisos': 'Permisos de administradores',
  'Manuales': 'Manuales',
  'Estadisticas': 'Estadísticas',
}

export default {
  // Acceso/navegación a una vista (solo visible del lado cliente)
  pageView: (route, label) => {
    const nombre = VIEW_LABELS[route] || label || route
    return track('acceso_vista', 'navegacion', `Accedió a la vista: ${nombre}`, {
      target_label: nombre,
      extra: { route },
    })
  },

  // Cierre de sesión (no existe endpoint backend, es 100% cliente)
  logout: (usr) => track('logout', 'acceso', `Cerró sesión${usr ? `: ${usr}` : ''}`),

  // Genérico para uso futuro
  action: (action_type, module, detail, opts) => track(action_type, module, detail, opts),
}
