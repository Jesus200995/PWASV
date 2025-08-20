/**
 * Servicio para gestionar notificaciones
 * Maneja todas las operaciones CRUD de notificaciones y Web Push
 */

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class NotificacionesService {
  
  /**
   * Obtener todas las notificaciones con filtros opcionales
   */
  async obtenerNotificaciones(filtros = {}) {
    try {
      const params = new URLSearchParams()
      
      if (filtros.status) params.append('status', filtros.status)
      if (filtros.type) params.append('type', filtros.type)
      if (filtros.search) params.append('search', filtros.search)
      if (filtros.limit) params.append('limit', filtros.limit)
      if (filtros.offset) params.append('offset', filtros.offset)
      
      const url = `${BASE_URL}/notifications${params.toString() ? '?' + params.toString() : ''}`
      
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      })
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
      
    } catch (error) {
      console.error('Error obteniendo notificaciones:', error)
      throw error
    }
  }
  
  /**
   * Obtener una notificación específica por ID
   */
  async obtenerNotificacion(id) {
    try {
      const response = await fetch(`${BASE_URL}/notifications/${id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      })
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
      
    } catch (error) {
      console.error('Error obteniendo notificación:', error)
      throw error
    }
  }
  
  /**
   * Crear una nueva notificación
   */
  async crearNotificacion(notificacionData) {
    try {
      const response = await fetch(`${BASE_URL}/notifications`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(notificacionData)
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
      
    } catch (error) {
      console.error('Error creando notificación:', error)
      throw error
    }
  }
  
  /**
   * Enviar una notificación específica
   */
  async enviarNotificacion(id) {
    try {
      const response = await fetch(`${BASE_URL}/notifications/${id}/send`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
      
    } catch (error) {
      console.error('Error enviando notificación:', error)
      throw error
    }
  }
  
  /**
   * Eliminar una notificación
   */
  async eliminarNotificacion(id) {
    try {
      const response = await fetch(`${BASE_URL}/notifications/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        }
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
      
    } catch (error) {
      console.error('Error eliminando notificación:', error)
      throw error
    }
  }
  
  /**
   * Marcar notificación como leída por un usuario
   */
  async marcarComoLeida(notificationId, userId) {
    try {
      const response = await fetch(`${BASE_URL}/notifications/${notificationId}/read?user_id=${userId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
      
    } catch (error) {
      console.error('Error marcando como leída:', error)
      throw error
    }
  }
  
  /**
   * Obtener estadísticas del sistema de notificaciones
   */
  async obtenerEstadisticas() {
    try {
      const response = await fetch(`${BASE_URL}/notifications/stats`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      })
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
      
    } catch (error) {
      console.error('Error obteniendo estadísticas:', error)
      throw error
    }
  }
  
  /**
   * Registrar suscripción para Web Push notifications
   */
  async suscribirDispositivo(subscriptionData) {
    try {
      const response = await fetch(`${BASE_URL}/push/subscribe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(subscriptionData)
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
      
    } catch (error) {
      console.error('Error suscribiendo dispositivo:', error)
      throw error
    }
  }
  
  /**
   * Eliminar suscripción de Web Push
   */
  async desuscribirDispositivo(endpoint) {
    try {
      const response = await fetch(`${BASE_URL}/push/unsubscribe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ endpoint })
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
      
    } catch (error) {
      console.error('Error desuscribiendo dispositivo:', error)
      throw error
    }
  }
  
  /**
   * Enviar notificación de prueba a un usuario específico
   */
  async enviarNotificacionPrueba(userId) {
    try {
      const response = await fetch(`${BASE_URL}/push/test/${userId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
      
    } catch (error) {
      console.error('Error enviando notificación de prueba:', error)
      throw error
    }
  }
  
  /**
   * Obtener lista de usuarios para selección de destinatarios
   */
  async obtenerUsuarios() {
    try {
      const response = await fetch(`${BASE_URL}/usuarios`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      })
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
      
    } catch (error) {
      console.error('Error obteniendo usuarios:', error)
      throw error
    }
  }
}

// Instancia única del servicio
const notificacionesService = new NotificacionesService()

export default notificacionesService
