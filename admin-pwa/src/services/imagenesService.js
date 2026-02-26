import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'https://apipwa.sembrandodatos.com'

const imagenesService = {
  /**
   * Elimina todas las imágenes de la base de datos
   * @returns {Promise} Respuesta del servidor con estadísticas de eliminación
   */
  async eliminarTodasLasImagenes() {
    try {
      const token = localStorage.getItem('admin_token')
      
      if (!token) {
        throw new Error('No hay token de autenticación. Por favor inicia sesión.')
      }

      console.log('📸 Iniciando eliminación de imágenes...')
      console.log('🔗 URL del endpoint:', `${API_URL}/imagenes/eliminar-todas`)
      console.log('🔐 Token presente:', !!token)

      const response = await axios.delete(
        `${API_URL}/imagenes/eliminar-todas`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          timeout: 60000 // 60 segundos de timeout
        }
      )

      console.log('✅ Respuesta del servidor:', response.data)
      return response.data
    } catch (error) {
      console.error('❌ Error completo:', error)
      console.error('   Mensaje:', error.message)
      console.error('   Response status:', error.response?.status)
      console.error('   Response data:', error.response?.data)
      
      let mensajeError = 'Error al eliminar imágenes'
      
      if (error.response?.status === 401) {
        mensajeError = 'Sesión expirada. Por favor inicia sesión nuevamente.'
      } else if (error.response?.status === 403) {
        mensajeError = 'No tienes permisos para eliminar imágenes.'
      } else if (error.response?.status === 404) {
        mensajeError = 'El servidor no reconoce este endpoint.'
      } else if (error.response?.status === 500) {
        mensajeError = 'Error en el servidor. Intenta más tarde.'
      } else if (error.message === 'Network Error') {
        mensajeError = 'Error de conexión. Verifica tu conexión a internet.'
      }
      
      throw new Error(mensajeError)
    }
  },

  /**
   * Elimina imágenes filtradas por mes/año
   * @param {number} mes - Mes (1-12)
   * @param {number} anio - Año (ej: 2025)
   * @param {boolean} soloMes - Si true, solo el mes especificado. Si false, todo el año
   * @returns {Promise} Respuesta del servidor con estadísticas de eliminación
   */
  async eliminarImagenesPorFecha(mes, anio, soloMes = true) {
    try {
      const token = localStorage.getItem('admin_token')
      
      if (!token) {
        throw new Error('No hay token de autenticación. Por favor inicia sesión.')
      }

      const periodo = soloMes ? `${mes}/${anio}` : `año ${anio}`
      console.log(`📸 Iniciando eliminación de imágenes del período: ${periodo}`)
      console.log('🔗 URL del endpoint:', `${API_URL}/imagenes/eliminar-por-fecha`)

      const response = await axios.delete(
        `${API_URL}/imagenes/eliminar-por-fecha`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          data: {
            mes: mes,
            anio: anio,
            solo_mes: soloMes
          },
          timeout: 120000 // 2 minutos de timeout
        }
      )

      console.log('✅ Respuesta del servidor:', response.data)
      return response.data
    } catch (error) {
      console.error('❌ Error completo:', error)
      
      let mensajeError = 'Error al eliminar imágenes por fecha'
      
      if (error.response?.status === 400) {
        mensajeError = error.response?.data?.detail || 'Parámetros de fecha inválidos.'
      } else if (error.response?.status === 401) {
        mensajeError = 'Sesión expirada. Por favor inicia sesión nuevamente.'
      } else if (error.response?.status === 403) {
        mensajeError = 'No tienes permisos para eliminar imágenes.'
      } else if (error.response?.status === 404) {
        mensajeError = 'El servidor no reconoce este endpoint.'
      } else if (error.response?.status === 500) {
        mensajeError = 'Error en el servidor. Intenta más tarde.'
      } else if (error.message === 'Network Error') {
        mensajeError = 'Error de conexión. Verifica tu conexión a internet.'
      }
      
      throw new Error(mensajeError)
    }
  }
}

export default imagenesService
