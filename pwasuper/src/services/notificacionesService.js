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
   * Obtener notificaciones de un usuario específico (MEJORADO CON ESTADOS DE LECTURA)
   */
  async obtenerNotificacionesUsuario(usuarioId, limit = 20, offset = 0) {
    try {
      console.log(`📱 Obteniendo notificaciones para usuario ${usuarioId}`)
      console.log(`🌐 URL: ${API_BASE_URL}/notificaciones/usuario/${usuarioId}`)
      
      const response = await api.get(`/notificaciones/usuario/${usuarioId}`, {
        params: { limit, offset }
      })
      
      console.log(`✅ ${response.data.notificaciones.length} notificaciones obtenidas`)
      return response.data
    } catch (error) {
      console.error('Error obteniendo notificaciones del usuario:', error)
      
      // Si es modo desarrollo y el endpoint no existe, crear datos de prueba
      if (import.meta.env.DEV && (error.response?.status === 404 || error.code === 'ECONNREFUSED')) {
        console.log('🧪 Modo desarrollo: creando notificaciones de prueba')
        return this.crearNotificacionesPrueba(usuarioId)
      }
      
      throw this.handleError(error)
    }
  },

  /**
   * Obtener conteo de notificaciones no leídas
   */
  async obtenerConteoNoLeidas(usuarioId) {
    try {
      console.log(`📊 Obteniendo conteo no leídas para usuario ${usuarioId}`)
      
      const response = await api.get('/notificaciones/unread_count', {
        params: { usuario_id: usuarioId }
      })
      
      console.log(`✅ ${response.data.count} notificaciones no leídas`)
      return response.data.count
    } catch (error) {
      console.error('Error obteniendo conteo no leídas:', error)
      
      // En desarrollo, simular conteo
      if (import.meta.env.DEV) {
        console.log('🧪 Modo desarrollo: simulando conteo no leídas')
        return Math.floor(Math.random() * 5) // 0-4 notificaciones no leídas
      }
      
      throw this.handleError(error)
    }
  },

  /**
   * Obtener lista de notificaciones con filtros
   */
  async obtenerListaNotificaciones(usuarioId, filtro = 'all', limit = 200, offset = 0) {
    try {
      console.log(`📋 Obteniendo lista filtrada para usuario ${usuarioId} (filtro: ${filtro})`)
      
      const response = await api.get('/notificaciones/list', {
        params: {
          usuario_id: usuarioId,
          filtro: filtro,
          limit: limit,
          offset: offset
        }
      })
      
      console.log(`✅ ${response.data.notificaciones.length} notificaciones filtradas obtenidas`)
      return response.data
    } catch (error) {
      console.error('Error obteniendo lista filtrada:', error)
      
      // En desarrollo, usar notificaciones de prueba filtradas
      if (import.meta.env.DEV) {
        console.log('🧪 Modo desarrollo: simulando lista filtrada')
        const datosPrueba = this.crearNotificacionesPrueba(usuarioId)
        
        if (filtro === 'unread') {
          // Simular algunas como no leídas
          datosPrueba.notificaciones = datosPrueba.notificaciones.map((n, i) => ({
            ...n,
            leida: i > 2 // Solo las primeras 3 como no leídas
          })).filter(n => !n.leida)
        } else {
          // Agregar estado de lectura a todas
          datosPrueba.notificaciones = datosPrueba.notificaciones.map((n, i) => ({
            ...n,
            leida: i > 2 // Las primeras 3 como no leídas
          }))
        }
        
        return datosPrueba
      }
      
      throw this.handleError(error)
    }
  },

  /**
   * Marcar notificación como leída
   */
  async marcarComoLeida(notificacionId, usuarioId, deviceId = null) {
    try {
      console.log(`✅ Marcando notificación ${notificacionId} como leída para usuario ${usuarioId}`)
      
      const response = await api.post(`/notificaciones/${notificacionId}/leer`, {
        usuario_id: usuarioId,
        device_id: deviceId
      })
      
      console.log(`✅ Notificación marcada como leída exitosamente`)
      return response.data
    } catch (error) {
      console.error('Error marcando como leída:', error)
      
      // En desarrollo, simular éxito
      if (import.meta.env.DEV) {
        console.log('🧪 Modo desarrollo: simulando marcar como leída')
        return { ok: true }
      }
      
      throw this.handleError(error)
    }
  },

  /**
   * Crear notificaciones de prueba para desarrollo (ACTUALIZADO CON ESTADOS)
   */
  crearNotificacionesPrueba(usuarioId) {
    const notificacionesPrueba = [
      {
        id: 1,
        titulo: 'Bienvenido al sistema de notificaciones',
        subtitulo: 'Sistema configurado correctamente',
        descripcion: 'El sistema de notificaciones de PWASUPER está funcionando correctamente. Aquí recibirás todas las notificaciones enviadas desde el panel de administración.',
        enlace_url: null,
        archivo_nombre: null,
        archivo_tipo: null,
        enviada_a_todos: true,
        fecha_creacion: new Date().toISOString(),
        fecha_envio: new Date().toISOString(),
        tiene_archivo: false,
        leida: false // NUEVO: Estado de lectura
      },
      {
        id: 2,
        titulo: 'Imagen de ejemplo',
        subtitulo: 'Notificación con imagen adjunta',
        descripcion: 'Esta notificación incluye una imagen que se muestra directamente en la vista previa. Las imágenes se muestran en formato cuadrado para mantener consistencia visual.',
        enlace_url: null,
        archivo_nombre: 'imagen_ejemplo.jpg',
        archivo_tipo: 'imagen',
        enviada_a_todos: false,
        fecha_creacion: new Date(Date.now() - 30 * 60 * 1000).toISOString(), // 30 min atrás
        fecha_envio: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
        tiene_archivo: true,
        leida: false // NUEVO: Estado de lectura
      },
      {
        id: 3,
        titulo: 'Video tutorial disponible',
        subtitulo: 'Aprende a usar las nuevas funciones',
        descripcion: 'Hemos preparado un video tutorial que muestra cómo aprovechar al máximo las nuevas funcionalidades del sistema.',
        enlace_url: null,
        archivo_nombre: 'tutorial.mp4',
        archivo_tipo: 'video',
        enviada_a_todos: true,
        fecha_creacion: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(), // 2 horas atrás
        fecha_envio: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        tiene_archivo: true,
        leida: false // NUEVO: Estado de lectura
      },
      {
        id: 4,
        titulo: 'Documento importante',
        subtitulo: 'Política actualizada',
        descripcion: 'Se ha actualizado la política de privacidad. Por favor revisa el documento adjunto para conocer los cambios más importantes.',
        enlace_url: null,
        archivo_nombre: 'politica_privacidad_v2.pdf',
        archivo_tipo: 'pdf',
        enviada_a_todos: true,
        fecha_creacion: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), // 1 día atrás
        fecha_envio: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
        tiene_archivo: true,
        leida: true // NUEVO: Estado de lectura (esta ya fue leída)
      },
      {
        id: 5,
        titulo: 'Funcionalidades disponibles',
        subtitulo: 'Explora todas las características',
        descripcion: 'Puedes ver notificaciones generales y personales, filtrar por fecha, ver archivos adjuntos y mucho más. Las notificaciones se actualizan automáticamente cada 5 minutos.',
        enlace_url: 'https://github.com/tu-repo',
        archivo_nombre: null,
        archivo_tipo: null,
        enviada_a_todos: false,
        fecha_creacion: new Date(Date.now() - 60 * 60 * 1000).toISOString(), // 1 hora atrás
        fecha_envio: new Date(Date.now() - 60 * 60 * 1000).toISOString(),
        tiene_archivo: false,
        leida: true // NUEVO: Estado de lectura (esta ya fue leída)
      }
    ]

    return {
      usuario: {
        id: usuarioId,
        nombre_completo: 'Usuario de Desarrollo'
      },
      notificaciones: notificacionesPrueba,
      total: notificacionesPrueba.length,
      limit: 20,
      offset: 0
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
   * Obtener URL del archivo de una notificación con manejo de errores de encoding
   */
  obtenerUrlArchivo(notificacionId, safe = false) {
    // Si safe=true, usar parámetro safe en el endpoint principal
    if (safe) {
      return `${API_BASE_URL}/notificaciones/${notificacionId}/archivo?safe=true`
    }
    
    // En desarrollo, generar URLs de placeholder para testing
    if (import.meta.env.DEV) {
      switch (notificacionId) {
        case 2: // Imagen
          return 'https://picsum.photos/400/400?random=1'
        case 3: // Video
          return 'https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4'
        default:
          return `${API_BASE_URL}/notificaciones/${notificacionId}/archivo`
      }
    }
    
    return `${API_BASE_URL}/notificaciones/${notificacionId}/archivo`
  },

  /**
   * Obtener contenido del archivo como base64 para evitar problemas de encoding
   */
  async obtenerArchivoBase64(notificacionId) {
    try {
      console.log(`📂 Obteniendo archivo base64 para notificación ${notificacionId}`)
      
      const response = await api.get(`/notificaciones/${notificacionId}/archivo/base64`)
      
      if (response.data.base64 && response.data.mime_type) {
        console.log(`✅ Archivo base64 obtenido: ${response.data.mime_type}`)
        
        // Convertir base64 a blob URL
        const byteCharacters = atob(response.data.base64)
        const byteNumbers = new Array(byteCharacters.length)
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i)
        }
        const byteArray = new Uint8Array(byteNumbers)
        const blob = new Blob([byteArray], { type: response.data.mime_type })
        
        return {
          url: URL.createObjectURL(blob),
          nombre: response.data.archivo_nombre,
          tipo: response.data.archivo_tipo,
          mimeType: response.data.mime_type,
          size: response.data.size,
          esBlob: true
        }
      }
      
      throw new Error('Respuesta de archivo inválida')
    } catch (error) {
      console.error('Error obteniendo archivo base64:', error)
      throw this.handleError(error)
    }
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
    if (!tipoArchivo) return '📎'
    
    const tipo = tipoArchivo.toLowerCase()
    
    // Imágenes
    if (tipo.includes('imagen') || tipo.includes('image') || 
        ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'].includes(tipo)) {
      return '🖼️'
    }
    
    // Videos
    if (tipo.includes('video') || 
        ['mp4', 'webm', 'ogg', 'avi', 'mov'].includes(tipo)) {
      return '🎥'
    }
    
    // Documentos
    if (tipo.includes('pdf')) return '📄'
    if (tipo.includes('doc') || tipo.includes('word')) return '📝'
    if (tipo.includes('xls') || tipo.includes('excel')) return '📊'
    if (tipo.includes('ppt') || tipo.includes('powerpoint')) return '📽️'
    if (tipo.includes('txt')) return '📃'
    if (tipo.includes('zip') || tipo.includes('rar')) return '📦'
    
    // Audio
    if (tipo.includes('audio') || 
        ['mp3', 'wav', 'ogg', 'aac'].includes(tipo)) {
      return '🎵'
    }
    
    return '📎'
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
    console.error('🔥 Error detallado:', error)
    
    if (error.response) {
      // Error con respuesta del servidor
      const status = error.response.status
      const message = error.response.data?.detail || error.response.data?.message || 'Error del servidor'
      
      console.log(`📊 Status: ${status}, Message: ${message}`)
      
      switch (status) {
        case 404:
          return new Error('Usuario no encontrado o endpoint no disponible')
        case 500:
          return new Error('Error interno del servidor')
        case 503:
          return new Error('Servicio no disponible temporalmente')
        default:
          return new Error(message)
      }
    } else if (error.request) {
      // Error de red
      console.log('🌐 Error de red:', error.code)
      if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
        return new Error('No se puede conectar al servidor. Verifica tu conexión a internet.')
      }
      return new Error('Error de conexión. Verifica tu internet.')
    } else if (error.code === 'ENOTFOUND') {
      return new Error('Servidor no encontrado. Verifica la URL de la API.')
    } else {
      // Error desconocido
      console.log('❓ Error desconocido:', error.message)
      return new Error('Error inesperado: ' + error.message)
    }
  }
}

export default notificacionesService
