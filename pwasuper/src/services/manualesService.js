import axios from 'axios'
import { API_URL } from '../utils/network.js'

// URL base de la API (relativa en producción para usar el mismo dominio y certificado)
const API_BASE_URL = API_URL

// Crear instancia de axios con configuración
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor para manejo de errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('Error en API de manuales:', error)
    return Promise.reject(error)
  }
)

export const manualesService = {
  /**
   * Obtener manuales de un usuario específico
   * Incluye manuales enviados a todos y los enviados específicamente al usuario
   */
  async obtenerManualesUsuario(usuarioId, limit = 50, offset = 0) {
    try {
      console.log(`📚 Obteniendo manuales para usuario ${usuarioId}`)
      console.log(`🌐 URL: ${API_BASE_URL}/manuales/usuario/${usuarioId}`)
      
      const response = await api.get(`/manuales/usuario/${usuarioId}`, {
        params: { limit, offset }
      })
      
      console.log(`✅ ${response.data.manuales?.length || 0} manuales obtenidos`)
      return response.data
    } catch (error) {
      console.error('Error obteniendo manuales del usuario:', error)
      
      // Si es modo desarrollo y el endpoint no existe, crear datos de prueba
      if (import.meta.env.DEV && (error.response?.status === 404 || error.code === 'ECONNREFUSED')) {
        console.log('🧪 Modo desarrollo: creando manuales de prueba')
        return this.crearManualesPrueba()
      }
      
      throw this.handleError(error)
    }
  },

  /**
   * Obtener conteo de manuales no leídos
   */
  async obtenerConteoNoLeidos(usuarioId) {
    try {
      console.log(`📊 Obteniendo conteo manuales no leídos para usuario ${usuarioId}`)
      
      const response = await api.get(`/manuales/usuario/${usuarioId}/no-leidos`)
      
      const conteo = response.data.total || response.data.no_leidos || 0
      console.log(`✅ ${conteo} manuales no leídos`)
      return conteo
    } catch (error) {
      console.error('Error obteniendo conteo no leídos:', error)
      
      // En desarrollo, simular conteo
      if (import.meta.env.DEV) {
        console.log('🧪 Modo desarrollo: simulando conteo no leídos')
        return Math.floor(Math.random() * 3)
      }
      
      return 0
    }
  },

  /**
   * Obtener detalle de un manual específico
   */
  async obtenerManual(manualId) {
    try {
      console.log(`📖 Obteniendo detalle del manual ${manualId}`)
      
      const response = await api.get(`/manuales/${manualId}`)
      
      return response.data
    } catch (error) {
      console.error('Error obteniendo manual:', error)
      throw this.handleError(error)
    }
  },

  /**
   * Marcar un manual como leído
   */
  async marcarComoLeido(manualId, usuarioId) {
    try {
      console.log(`✅ Marcando manual ${manualId} como leído por usuario ${usuarioId}`)
      
      const response = await api.post(`/manuales/${manualId}/leer`, null, {
        params: { usuario_id: usuarioId }
      })
      
      console.log('✅ Manual marcado como leído')
      return response.data
    } catch (error) {
      console.error('Error marcando manual como leído:', error)
      // No lanzar error para que no interrumpa la experiencia del usuario
      return { success: false, error: error.message }
    }
  },

  /**
   * Obtener URL del archivo adjunto
   */
  getArchivoUrl(manualId) {
    return `${API_BASE_URL}/manuales/${manualId}/archivo`
  },

  /**
   * Obtener URL de la imagen de portada
   */
  getImagenUrl(manualId) {
    return `${API_BASE_URL}/manuales/${manualId}/imagen`
  },

  /**
   * Obtener URL del video
   */
  getVideoUrl(manualId) {
    return `${API_BASE_URL}/manuales/${manualId}/video`
  },

  /**
   * Manejo de errores
   */
  handleError(error) {
    if (error.response) {
      // Error del servidor
      const message = error.response.data?.detail || error.response.data?.message || 'Error del servidor'
      return new Error(message)
    } else if (error.request) {
      // Error de red
      return new Error('Error de conexión. Por favor verifica tu internet.')
    } else {
      // Otro error
      return new Error(error.message || 'Error desconocido')
    }
  },

  /**
   * Crear manuales de prueba (solo desarrollo)
   */
  crearManualesPrueba() {
    return {
      manuales: [
        {
          id: 1,
          titulo: 'Manual de Usuario - PWA Super',
          subtitulo: 'Guía completa de uso de la aplicación',
          descripcion: 'Este manual contiene toda la información necesaria para utilizar correctamente la aplicación PWA Super. Incluye instrucciones para registro de asistencia, reportes y más.',
          enlace_url: null,
          archivo_nombre: 'manual_usuario_v1.pdf',
          imagen_nombre: 'portada_manual.jpg',
          enviado_a_todos: true,
          fecha_creacion: new Date().toISOString(),
          leido: false,
          fecha_lectura: null
        },
        {
          id: 2,
          titulo: 'Protocolo de Seguridad',
          subtitulo: 'Procedimientos de emergencia',
          descripcion: 'Documento con los protocolos de seguridad y procedimientos en caso de emergencia.',
          enlace_url: 'https://ejemplo.com/seguridad',
          archivo_nombre: null,
          imagen_nombre: null,
          enviado_a_todos: true,
          fecha_creacion: new Date(Date.now() - 86400000).toISOString(),
          leido: true,
          fecha_lectura: new Date(Date.now() - 43200000).toISOString()
        },
        {
          id: 3,
          titulo: 'Actualización de Políticas',
          subtitulo: 'Nuevas políticas 2025',
          descripcion: 'Documento con las nuevas políticas de la empresa para el año 2025.',
          enlace_url: null,
          archivo_nombre: 'politicas_2025.pdf',
          imagen_nombre: 'banner_politicas.png',
          enviado_a_todos: false,
          fecha_creacion: new Date(Date.now() - 172800000).toISOString(),
          leido: false,
          fecha_lectura: null
        }
      ],
      total: 3
    }
  }
}

export default manualesService
