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
        throw new Error('No hay token de autenticación')
      }

      const response = await axios.delete(
        `${API_URL}/imagenes/eliminar-todas`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      )

      return response.data
    } catch (error) {
      console.error('Error al eliminar imágenes:', error)
      throw error
    }
  }
}

export default imagenesService
