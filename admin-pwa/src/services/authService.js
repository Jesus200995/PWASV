// Servicio de autenticación con manejo de roles
import axios from 'axios'

const API_URL = 'https://apipwa.sembrandodatos.com'

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
      formData.append('grant_type', '')
      formData.append('username', credentials.username)
      formData.append('password', credentials.password)
      formData.append('scope', '')
      formData.append('client_id', '')
      formData.append('client_secret', '')

      const response = await axios.post(`${API_URL}/admin/login`, formData, {
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
      // Intentar obtener desde tabla admin_users (usuarios del panel admin)
      const adminUsersResponse = await axios.get(`${API_URL}/admin/usuarios`, {
        headers: {
          'Authorization': `Bearer ${this.token}`
        }
      })

      const adminUser = adminUsersResponse.data.usuarios?.find(user => user.username === username)
      if (adminUser) {
        return {
          id: adminUser.id,
          username: adminUser.username,
          rol: adminUser.rol || 'admin',
          tipo: 'admin_user'
        }
      }

      // Si no se encuentra en admin_users, buscar en usuarios normales
      const usuariosResponse = await axios.get(`${API_URL}/usuarios`)
      const normalUser = usuariosResponse.data.usuarios?.find(user => 
        user.correo === username || user.nombre_completo === username
      )

      if (normalUser) {
        return {
          id: normalUser.id,
          username: normalUser.correo,
          nombre: normalUser.nombre_completo,
          rol: normalUser.rol || 'user',
          tipo: 'usuario_normal'
        }
      }

      // Usuario por defecto si no se encuentra
      return {
        username,
        rol: 'admin', // Por compatibilidad, asumir admin si no se encuentra
        tipo: 'unknown'
      }
    } catch (error) {
      console.error('Error obteniendo info del usuario:', error)
      // Retornar usuario básico como fallback
      return {
        username,
        rol: 'admin',
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
