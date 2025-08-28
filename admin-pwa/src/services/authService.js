// Servicio de autenticación con manejo de roles
import axios from 'axios'
import { API_URL, API_CONFIG } from '../config/api.js'
import healthCheckService from './healthCheckService.js'

class AuthService {
  constructor() {
    this.token = localStorage.getItem('admin_token')
    this.user = this.getUserFromStorage()
  }

  /**
   * Obtener usuario desde localStorage
   */
  getUserFromStorage() {
    try {
      const userString = localStorage.getItem('admin_user_data')
      if (userString) {
        return JSON.parse(userString)
      }
      // Fallback para compatibilidad con versión anterior
      const username = localStorage.getItem('admin_user')
      return username ? { username, rol: 'admin' } : null
    } catch (error) {
      console.error('Error parsing user from localStorage:', error)
      return null
    }
  }

  /**
   * Iniciar sesión
   */
  async login(credentials) {
    try {
      const formData = new URLSearchParams()
      formData.append('grant_type', 'password')
      formData.append('username', credentials.username)
      formData.append('password', credentials.password)
      formData.append('scope', '')
      formData.append('client_id', '')
      formData.append('client_secret', '')

      const loginUrl = `${API_URL}${API_CONFIG.endpoints.adminLogin}`
      console.log(`🔐 Intentando login en: ${loginUrl}`)

      const response = await axios.post(loginUrl, formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })

      if (response.data.access_token) {
        // Guardar token
        this.token = response.data.access_token
        localStorage.setItem('admin_token', this.token)
        
        // Obtener información del usuario desde la respuesta o fetchear
        let userData
        if (response.data.user_info) {
          userData = response.data.user_info
          console.log('📋 Info de usuario desde respuesta de login:', userData)
        } else {
          userData = await this.fetchUserInfo(credentials.username)
        }
        
        // Guardar información del usuario
        this.user = userData
        localStorage.setItem('admin_user_data', JSON.stringify(userData))
        localStorage.setItem('admin_user', credentials.username) // Para compatibilidad

        console.log('✅ Usuario logueado:', userData)
        return { success: true, user: userData }
      }
      
      return { success: false, error: 'Token no recibido' }
    } catch (error) {
      console.error('❌ Error de login:', error)
      throw error
    }
  }

  /**
   * Obtener información del usuario del backend
   */
  async fetchUserInfo(username) {
    try {
      // Intentar primero con el endpoint /auth/me si existe
      try {
        const meUrl = `${API_URL}${API_CONFIG.endpoints.authMe}`
        console.log(`📋 Obteniendo info de usuario desde: ${meUrl}`)
        
        const meResponse = await axios.get(meUrl, {
          headers: {
            'Authorization': `Bearer ${this.token}`
          }
        })

        if (meResponse.data && meResponse.data.username) {
          return {
            id: meResponse.data.id,
            username: meResponse.data.username,
            rol: meResponse.data.rol || 'admin',
            tipo: 'admin_user'
          }
        }
      } catch (meError) {
        console.log('Endpoint /auth/me no disponible, usando fallback')
      }

      // Fallback para APIs que no tienen /auth/me implementado
      return {
        username,
        rol: 'admin', // Por defecto admin para usuarios que acceden al panel admin
        tipo: 'admin_user'
      }
    } catch (error) {
      console.error('Error obteniendo info del usuario:', error)
      // Retornar usuario básico como fallback
      return {
        username,
        rol: 'admin', // Por defecto admin para acceso al panel
        tipo: 'fallback'
      }
    }
  }

  /**
   * Cerrar sesión
   */
  logout() {
    this.token = null
    this.user = null
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_user')
    localStorage.removeItem('admin_user_data')
  }

  /**
   * Verificar si el usuario está autenticado
   */
  isAuthenticated() {
    return !!this.token
  }

  /**
   * Obtener el rol del usuario actual
   */
  getUserRole() {
    return this.user?.rol || 'user'
  }

  /**
   * Verificar si el usuario tiene rol de admin
   */
  isAdmin() {
    return this.getUserRole() === 'admin'
  }

  /**
   * Verificar si el usuario tiene rol de user
   */
  isUser() {
    return this.getUserRole() === 'user'
  }

  /**
   * Verificar si el usuario tiene acceso a una funcionalidad
   */
  hasAccess(requiredRole) {
    const userRole = this.getUserRole()
    
    if (requiredRole === 'admin') {
      return userRole === 'admin'
    }
    
    if (requiredRole === 'user') {
      return ['admin', 'user'].includes(userRole)
    }
    
    return true // Por defecto permitir acceso
  }

  /**
   * Obtener información del usuario actual
   */
  getCurrentUser() {
    return this.user
  }

  /**
   * Obtener token de autenticación
   */
  getToken() {
    return this.token
  }

  /**
   * Refrescar información del usuario
   */
  async refreshUserInfo() {
    if (this.user?.username) {
      try {
        const userData = await this.fetchUserInfo(this.user.username)
        this.user = userData
        localStorage.setItem('admin_user_data', JSON.stringify(userData))
        return userData
      } catch (error) {
        console.error('Error refreshing user info:', error)
        return this.user
      }
    }
    return this.user
  }
}

// Exportar instancia única
export default new AuthService()
