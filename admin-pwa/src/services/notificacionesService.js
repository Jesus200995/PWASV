// notificacionesService.js
import axios from 'axios'
import { API_URL } from '../config/api.js'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Crear FormData API para archivos
const createFormDataApi = () => axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'multipart/form-data'
  }
})

export const notificacionesService = {
  /**
   * Crear una nueva notificación
   * @param {Object} notificacion - Datos de la notificación
   * @param {File} archivo - Archivo adjunto opcional
   * @returns {Promise} Respuesta de la API
   */
  async crearNotificacion(notificacion, archivo = null) {
    try {
      console.log('📤 Enviando notificación:', notificacion)
      
      // Crear FormData para enviar datos y archivo
      const formData = new FormData()
      formData.append('titulo', notificacion.titulo)
      
      if (notificacion.subtitulo) {
        formData.append('subtitulo', notificacion.subtitulo)
      }
      
      if (notificacion.descripcion) {
        formData.append('descripcion', notificacion.descripcion)
      }
      
      if (notificacion.enlace_url) {
        formData.append('enlace_url', notificacion.enlace_url)
      }
      
      formData.append('enviada_a_todos', notificacion.enviada_a_todos)
      
      // Si no es para todos, incluir usuarios seleccionados
      if (!notificacion.enviada_a_todos && notificacion.usuario_ids && notificacion.usuario_ids.length > 0) {
        formData.append('usuario_ids', JSON.stringify(notificacion.usuario_ids))
      }
      
      // Agregar archivo si existe
      if (archivo) {
        formData.append('archivo', archivo)
      }
      
      const response = await createFormDataApi().post('/notificaciones', formData)
      
      console.log('✅ Notificación creada:', response.data)
      return response.data
      
    } catch (error) {
      console.error('❌ Error creando notificación:', error)
      
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail)
      }
      
      throw new Error('Error al crear la notificación. Verifica tu conexión e intenta de nuevo.')
    }
  },

  /**
   * Listar todas las notificaciones
   * @param {number} limit - Límite de resultados
   * @param {number} offset - Offset para paginación
   * @param {string} tipo - Filtro por tipo: 'todas', 'individuales', 'grupales'
   * @returns {Promise} Lista de notificaciones
   */
  async listarNotificaciones(limit = 50, offset = 0, tipo = 'todas') {
    try {
      console.log(`📋 Obteniendo notificaciones (limit: ${limit}, offset: ${offset}, tipo: ${tipo})`)
      
      const params = { limit, offset }
      if (tipo !== 'todas') {
        params.tipo = tipo
      }
      
      const response = await api.get('/notificaciones', {
        params
      })
      
      console.log(`✅ ${response.data.notificaciones.length} notificaciones obtenidas`)
      return response.data
      
    } catch (error) {
      console.error('❌ Error obteniendo notificaciones:', error)
      throw new Error('Error al obtener las notificaciones')
    }
  },

  /**
   * Obtener una notificación específica
   * @param {number} id - ID de la notificación
   * @returns {Promise} Datos de la notificación
   */
  async obtenerNotificacion(id) {
    try {
      console.log(`🔍 Obteniendo notificación ${id}`)
      
      const response = await api.get(`/notificaciones/${id}`)
      
      console.log('✅ Notificación obtenida:', response.data)
      return response.data
      
    } catch (error) {
      console.error(`❌ Error obteniendo notificación ${id}:`, error)
      
      if (error.response?.status === 404) {
        throw new Error('Notificación no encontrada')
      }
      
      throw new Error('Error al obtener la notificación')
    }
  },

  /**
   * Actualizar una notificación existente
   * @param {number} id - ID de la notificación a actualizar
   * @param {Object} notificacion - Datos de la notificación
   * @param {File} archivo - Archivo adjunto opcional
   * @returns {Promise} Respuesta de la API
   */
  async actualizarNotificacion(id, notificacion, archivo = null) {
    try {
      console.log(`✏️ Actualizando notificación ${id}:`, notificacion)
      
      // Crear FormData para enviar datos y archivo
      const formData = new FormData()
      formData.append('titulo', notificacion.titulo)
      
      if (notificacion.subtitulo) {
        formData.append('subtitulo', notificacion.subtitulo)
      }
      
      if (notificacion.descripcion) {
        formData.append('descripcion', notificacion.descripcion)
      }
      
      if (notificacion.enlace_url) {
        formData.append('enlace_url', notificacion.enlace_url)
      }
      
      formData.append('enviada_a_todos', notificacion.enviada_a_todos)
      
      // Si no es para todos, incluir usuarios seleccionados
      if (!notificacion.enviada_a_todos && notificacion.usuario_ids && notificacion.usuario_ids.length > 0) {
        formData.append('usuario_ids', JSON.stringify(notificacion.usuario_ids))
      }
      
      // Agregar archivo si existe
      if (archivo) {
        formData.append('archivo', archivo)
      }
      
      const response = await createFormDataApi().put(`/notificaciones/${id}`, formData)
      
      console.log('✅ Notificación actualizada:', response.data)
      return response.data
      
    } catch (error) {
      console.error(`❌ Error actualizando notificación ${id}:`, error)
      
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail)
      }
      
      throw new Error('Error al actualizar la notificación. Verifica tu conexión e intenta de nuevo.')
    }
  },

  /**
   * Eliminar una notificación
   * @param {number} id - ID de la notificación
   * @returns {Promise} Confirmación de eliminación
   */
  async eliminarNotificacion(id) {
    try {
      console.log(`🗑️ Eliminando notificación ${id}`)
      
      const response = await api.delete(`/notificaciones/${id}`)
      
      console.log('✅ Notificación eliminada:', response.data)
      return response.data
      
    } catch (error) {
      console.error(`❌ Error eliminando notificación ${id}:`, error)
      
      if (error.response?.status === 404) {
        throw new Error('Notificación no encontrada')
      }
      
      throw new Error('Error al eliminar la notificación')
    }
  },

  /**
   * Obtener URL del archivo adjunto
   * @param {number} id - ID de la notificación
   * @returns {string} URL del archivo
   */
  obtenerUrlArchivo(id) {
    return `${API_BASE_URL}/notificaciones/${id}/archivo`
  },

  /**
   * Descargar archivo adjunto
   * @param {number} id - ID de la notificación
   * @returns {Promise} Blob del archivo
   */
  async descargarArchivo(id) {
    try {
      console.log(`📎 Descargando archivo de notificación ${id}`)
      
      const response = await api.get(`/notificaciones/${id}/archivo`, {
        responseType: 'blob'
      })
      
      console.log('✅ Archivo descargado exitosamente')
      return response
      
    } catch (error) {
      console.error(`❌ Error descargando archivo de notificación ${id}:`, error)
      
      if (error.response?.status === 404) {
        throw new Error('Archivo no encontrado')
      }
      
      throw new Error('Error al descargar el archivo')
    }
  },

  /**
   * Obtener estadísticas de lectura de una notificación
   * @param {number} id - ID de la notificación
   * @returns {Promise} Estadísticas de lectura
   */
  async obtenerEstadisticasNotificacion(id) {
    try {
      console.log(`📊 Obteniendo estadísticas de notificación ${id}`)
      
      const response = await api.get(`/notificaciones/${id}/estadisticas`)
      
      console.log('✅ Estadísticas obtenidas:', response.data)
      return response.data
      
    } catch (error) {
      console.error(`❌ Error obteniendo estadísticas de notificación ${id}:`, error)
      
      if (error.response?.status === 404) {
        throw new Error('Notificación no encontrada')
      }
      
      throw new Error('Error al obtener las estadísticas de la notificación')
    }
  }
}

export default notificacionesService
