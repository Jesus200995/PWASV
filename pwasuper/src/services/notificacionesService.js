import axios from 'axios'

// Configuración de la API
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://apipwa.sembrandodatos.com' 
  : 'http://localhost:8000'

// Crear instancia de axios con configuración
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor para manejo de errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('Error en API de notificaciones:', error)
    return Promise.reject(error)
  }
)

export const notificacionesService = {
  /**
   * Obtener notificaciones de un usuario específico
   */
  async obtenerNotificacionesUsuario(usuarioId, limit = 20, offset = 0) {
    try {
      console.log(`📱 Obteniendo notificaciones para usuario ${usuarioId}`)
      const response = await api.get(`/notificaciones/usuario/${usuarioId}`, {
        params: { limit, offset }
      })
      
      console.log(`✅ ${response.data.notificaciones.length} notificaciones obtenidas`)
      return response.data
    } catch (error) {
      console.error('Error obteniendo notificaciones del usuario:', error)
      throw this.handleError(error)
    }
  },

  /**
   * Obtener detalles de una notificación específica
   */
  async obtenerDetalleNotificacion(notificacionId) {
    try {
      console.log(`🔍 Obteniendo detalles de notificación ${notificacionId}`)
      const response = await api.get(`/notificaciones/${notificacionId}`)
      
      console.log(`✅ Detalles de notificación obtenidos`)
      return response.data
    } catch (error) {
      console.error('Error obteniendo detalles de notificación:', error)
      throw this.handleError(error)
    }
  },

  /**
   * Obtener URL del archivo de una notificación
   */
  obtenerUrlArchivo(notificacionId) {
    return `${API_BASE_URL}/notificaciones/${notificacionId}/archivo`
  },

  /**
   * Verificar si una notificación tiene archivo adjunto
   */
  tieneArchivo(notificacion) {
    return !!(notificacion.archivo_nombre && notificacion.archivo_tipo)
  },

  /**
   * Obtener icono según el tipo de archivo
   */
  obtenerIconoArchivo(tipoArchivo) {
    const iconos = {
      'imagen': '🖼️',
      'pdf': '📄',
      'video': '🎥'
    }
    return iconos[tipoArchivo] || '📎'
  },

  /**
   * Formatear fecha de notificación
   */
  formatearFecha(fechaISO) {
    if (!fechaISO) return 'Fecha no disponible'
    
    const fecha = new Date(fechaISO)
    const ahora = new Date()
    const diferencia = ahora - fecha
    
    // Menos de 1 minuto
    if (diferencia < 60000) {
      return 'Ahora'
    }
    
    // Menos de 1 hora
    if (diferencia < 3600000) {
      const minutos = Math.floor(diferencia / 60000)
      return `Hace ${minutos} min`
    }
    
    // Menos de 24 horas
    if (diferencia < 86400000) {
      const horas = Math.floor(diferencia / 3600000)
      return `Hace ${horas}h`
    }
    
    // Menos de 7 días
    if (diferencia < 604800000) {
      const dias = Math.floor(diferencia / 86400000)
      return `Hace ${dias}d`
    }
    
    // Más de 7 días - mostrar fecha
    return fecha.toLocaleDateString('es-MX', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
  },

  /**
   * Formatear fecha completa
   */
  formatearFechaCompleta(fechaISO) {
    if (!fechaISO) return 'Fecha no disponible'
    
    const fecha = new Date(fechaISO)
    return fecha.toLocaleDateString('es-MX', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  },

  /**
   * Verificar conectividad con la API
   */
  async verificarConectividad() {
    try {
      console.log('🔍 Verificando conectividad con API de notificaciones...')
      const response = await api.get('/health', { timeout: 5000 })
      console.log('✅ Conectividad con API verificada')
      return true
    } catch (error) {
      console.error('❌ Error de conectividad con API:', error)
      return false
    }
  },

  /**
   * Manejo centralizado de errores
   */
  handleError(error) {
    if (error.response) {
      // Error con respuesta del servidor
      const status = error.response.status
      const message = error.response.data?.detail || error.response.data?.message || 'Error del servidor'
      
      switch (status) {
        case 404:
          return new Error('Recurso no encontrado')
        case 500:
          return new Error('Error interno del servidor')
        case 503:
          return new Error('Servicio no disponible')
        default:
          return new Error(message)
      }
    } else if (error.request) {
      // Error de red
      return new Error('Error de conexión. Verifica tu internet.')
    } else {
      // Error desconocido
      return new Error('Error inesperado')
    }
  }
}

export default notificacionesService
