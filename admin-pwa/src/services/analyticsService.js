// Servicio de métricas y telemetría de la plataforma
import { API_URL } from '../config/api.js'
import authService from './authService.js'

const _ep = `${API_URL}/sys/ping`

let _sid = sessionStorage.getItem('_asid')
if (!_sid) {
  _sid = Math.random().toString(36).slice(2) + Date.now().toString(36)
  sessionStorage.setItem('_asid', _sid)
}

function _getCtx() {
  const u = authService.user
  return {
    usr: u?.username || u?.correo || null,
    usr_id: u?.id || null,
    session_id: _sid,
  }
}

async function track(action_type, module, detail = null, opts = {}) {
  try {
    const ctx = _getCtx()
    await fetch(_ep, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...ctx,
        action_type,
        module,
        detail,
        target_id: opts.target_id ? String(opts.target_id) : null,
        target_label: opts.target_label || null,
        extra: opts.extra || null,
      }),
      keepalive: true,
    })
  } catch (_) {
    // silencioso
  }
}

export default {
  // Navegación
  pageView: (route, label) => track('page_view', route, label),

  // Autenticación
  login: (usr) => track('login', 'auth', `Login: ${usr}`),
  logout: (usr) => track('logout', 'auth', `Logout: ${usr}`),
  loginFailed: (usr) => track('login_failed', 'auth', `Intento fallido: ${usr}`),

  // Usuarios
  createUser: (label) => track('create_user', 'usuarios', label, { target_label: label }),
  updateUser: (id, label) => track('update_user', 'usuarios', label, { target_id: id, target_label: label }),
  deleteUser: (id, label) => track('delete_user', 'usuarios', label, { target_id: id, target_label: label }),
  toggleUser: (id, label, active) => track('toggle_user', 'usuarios', `${label} → ${active ? 'activo' : 'inactivo'}`, { target_id: id }),

  // Reportes
  downloadReport: (id, label) => track('download_report', 'reportes', label, { target_id: id, target_label: label }),
  viewReport: (id, label) => track('view_report', 'reportes', label, { target_id: id, target_label: label }),
  deleteReport: (id, label) => track('delete_report', 'reportes', label, { target_id: id, target_label: label }),

  // Fotos / imágenes
  deletePhoto: (id, label) => track('delete_photo', 'imagenes', label, { target_id: id, target_label: label }),
  viewPhoto: (label) => track('view_photo', 'imagenes', label),

  // Registros / historiales
  viewRecord: (id, label) => track('view_record', 'registros', label, { target_id: id }),
  deleteRecord: (id, label) => track('delete_record', 'registros', label, { target_id: id }),
  exportCSV: (module, label) => track('export_csv', module, label),

  // Configuración / permisos
  changePermission: (usr, detail) => track('change_permission', 'permisos', `${usr}: ${detail}`),
  changeConfig: (key, val) => track('change_config', 'configuracion', `${key}=${val}`),

  // Notificaciones
  sendNotification: (label) => track('send_notification', 'notificaciones', label),
  deleteNotification: (id) => track('delete_notification', 'notificaciones', null, { target_id: id }),

  // Asistencias
  viewAsistencia: (label) => track('view_asistencia', 'asistencia', label),

  // Manuales
  uploadManual: (label) => track('upload_manual', 'manuales', label),
  deleteManual: (id, label) => track('delete_manual', 'manuales', label, { target_id: id }),
  downloadManual: (id, label) => track('download_manual', 'manuales', label, { target_id: id }),

  // Genérico
  action: (action_type, module, detail, opts) => track(action_type, module, detail, opts),
}
