// manualesService.js
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

export const manualesService = {
  /**
   * Crear un nuevo manual
   * @param {Object} manual - Datos del manual
   * @param {File} archivo - Archivo PDF/documento opcional
   * @param {File} imagen - Imagen de portada opcional
   * @param {File} video - Video opcional
   * @returns {Promise} Respuesta de la API
   */
  async crearManual(manual, archivo = null, imagen = null, video = null) {
    try {
      console.log('📚 Creando manual:', manual)
      
      const formData = new FormData()
      formData.append('titulo', manual.titulo)
      
      if (manual.subtitulo) {
        formData.append('subtitulo', manual.subtitulo)
      }
      
      if (manual.descripcion) {
        formData.append('descripcion', manual.descripcion)
      }
      
      if (manual.enlace_url) {
        formData.append('enlace_url', manual.enlace_url)
      }
      
      formData.append('enviado_a_todos', manual.enviado_a_todos)
      
      // Si no es para todos, incluir usuarios seleccionados
      if (!manual.enviado_a_todos && manual.usuario_ids && manual.usuario_ids.length > 0) {
        formData.append('usuario_ids', JSON.stringify(manual.usuario_ids))
      }
      
      // Agregar archivo si existe
      if (archivo) {
        formData.append('archivo', archivo)
        console.log('📎 Archivo adjunto:', archivo.name)
      }
      
      // Agregar imagen si existe
      if (imagen) {
        formData.append('imagen', imagen)
        console.log('🖼️ Imagen adjunta:', imagen.name)
      }
      
      // Agregar video si existe
      if (video) {
        formData.append('video', video)
        console.log('🎬 Video adjunto:', video.name)
      }
      
      const formDataApi = createFormDataApi()
      const response = await formDataApi.post('/manuales', formData)
      
      console.log('✅ Manual creado:', response.data)
      return response.data
      
    } catch (error) {
      console.error('❌ Error creando manual:', error)
      throw error
    }
  },

  /**
   * Listar todos los manuales (para admin)
   * @param {number} limit - Límite de resultados
   * @param {number} offset - Desplazamiento
   * @returns {Promise} Lista de manuales
   */
  async listarManuales(limit = 50, offset = 0) {
    try {
      console.log('📚 Listando manuales...')
      const response = await api.get(`/manuales?limit=${limit}&offset=${offset}`)
      console.log('✅ Manuales obtenidos:', response.data)
      return response.data
    } catch (error) {
      console.error('❌ Error listando manuales:', error)
      throw error
    }
  },

  /**
   * Obtener detalle de un manual
   * @param {number} manualId - ID del manual
   * @returns {Promise} Detalle del manual
   */
  async obtenerManual(manualId) {
    try {
      console.log(`📚 Obteniendo manual ${manualId}...`)
      const response = await api.get(`/manuales/${manualId}`)
      return response.data
    } catch (error) {
      console.error('❌ Error obteniendo manual:', error)
      throw error
    }
  },

  /**
   * Obtener estadísticas de un manual
   * @param {number} manualId - ID del manual
   * @returns {Promise} Estadísticas del manual
   */
  async obtenerEstadisticas(manualId) {
    try {
      console.log(`📊 Obteniendo estadísticas del manual ${manualId}...`)
      const response = await api.get(`/manuales/${manualId}/estadisticas`)
      return response.data
    } catch (error) {
      console.error('❌ Error obteniendo estadísticas:', error)
      throw error
    }
  },

  /**
   * Eliminar un manual
   * @param {number} manualId - ID del manual
   * @returns {Promise} Respuesta de la API
   */
  async eliminarManual(manualId) {
    try {
      console.log(`🗑️ Eliminando manual ${manualId}...`)
      const response = await api.delete(`/manuales/${manualId}`)
      console.log('✅ Manual eliminado:', response.data)
      return response.data
    } catch (error) {
      console.error('❌ Error eliminando manual:', error)
      throw error
    }
  },

  /**
   * Obtener URL del archivo de un manual
   * @param {number} manualId - ID del manual
   * @returns {string} URL del archivo
   */
  getArchivoUrl(manualId) {
    return `${API_URL}/manuales/${manualId}/archivo`
  },

  /**
   * Obtener URL de la imagen de un manual
   * @param {number} manualId - ID del manual
   * @returns {string} URL de la imagen
   */
  getImagenUrl(manualId) {
    return `${API_URL}/manuales/${manualId}/imagen`
  },

  /**
   * Obtener URL del video de un manual
   * @param {number} manualId - ID del manual
   * @returns {string} URL del video
   */
  getVideoUrl(manualId) {
    return `${API_URL}/manuales/${manualId}/video`
  }
}

export default manualesService
