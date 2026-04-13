// Servicio de autenticación con manejo de roles y verificación en tiempo real
import axios from 'axios'
import { API_URL, API_CONFIG } from '../config/api.js'
import healthCheckService from './healthCheckService.js'

class AuthService {
  constructor() {
    this.token = localStorage.getItem('admin_token')
    this.user = this.getUserFromStorage()
    this.sessionCheckInterval = null
    this.onUserUpdated = null // Callback para notificar cambios
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
   * Registrar callback para cuando el usuario se actualice
   */
  setOnUserUpdated(callback) {
    this.onUserUpdated = callback
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

        // Iniciar verificación en tiempo real de sesión (estado, rol, permisos)
        this.startSessionCheck()

        console.log('✅ Usuario logueado:', userData)
        return { success: true, user: userData }
      }
      
      return { success: false, error: 'Token no recibido' }
    } catch (error) {
      console.error('❌ Error de login:', error)
      
      // Verificar si es error de usuario inactivo
      if (error.response?.status === 403) {
        throw new Error(error.response.data.detail || 'Tu cuenta ha sido desactivada')
      }
      
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
            tipo: 'admin_user',
            session_version: meResponse.data.session_version || 1
          }
        }
      } catch (meError) {
        console.log('Endpoint /auth/me no disponible, usando fallback')
      }

      // Fallback para APIs que no tienen /auth/me implementado
      return {
        username,
        rol: 'admin', // Por defecto admin para usuarios que acceden al panel admin
        tipo: 'admin_user',
        session_version: 1 // Versión por defecto para compatibilidad
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
    // Detener verificación de sesión
    this.stopSessionCheck()
    
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
    // Asegurar que tenemos los datos del usuario
    if (!this.user) {
      this.user = this.getUserFromStorage()
    }
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
   * Verificar si el usuario tiene un permiso específico
   * @param {string} permiso - Nombre del permiso (visor, asistencia, registros, usuarios, etc.)
   * @returns {boolean}
   */
  hasPermission(permiso) {
    // Asegurar que tenemos los datos del usuario
    if (!this.user) {
      this.user = this.getUserFromStorage()
    }
    
    // Si es admin, tiene todos los permisos
    if (this.isAdmin()) {
      return true
    }
    
    // Verificar permisos del usuario
    if (this.user && this.user.permisos) {
      console.log(`🔐 Verificando permiso "${permiso}":`, this.user.permisos[permiso])
      return this.user.permisos[permiso] === true
    }
    
    console.log(`⚠️ Usuario sin permisos definidos, denegando acceso a: ${permiso}`)
    return false
  }

  /**
   * Obtener información del usuario actual
   */
  getCurrentUser() {
    return this.user
  }

  /**
   * Verificar si el admin actual es territorial (restringido a un territorio)
   */
  isTerritorial() {
    if (!this.user) {
      this.user = this.getUserFromStorage()
    }
    return this.user?.es_territorial === true
  }

  /**
   * Obtener el territorio asignado al admin territorial
   * @returns {string|null} - El nombre del territorio o null si es global
   */
  getTerritorio() {
    if (!this.user) {
      this.user = this.getUserFromStorage()
    }
    return this.user?.territorio || null
  }

  /**
   * Obtener filtro de territorio para queries
   * @returns {string|null} - El territorio si es admin territorial, null si es global
   */
  getTerritorioFilter() {
    if (this.isTerritorial()) {
      return this.getTerritorio()
    }
    return null
  }

  /**
   * Verificar si el usuario actual es un FACILITADOR
   */
  isFacilitador() {
    if (!this.user) {
      this.user = this.getUserFromStorage()
    }
    return (this.user?.cargo || '').toUpperCase() === 'FACILITADOR'
  }

  /**
   * Obtener el ID del admin facilitador (id en admin_users)
   * @returns {number|null}
   */
  getFacilitadorAdminId() {
    if (!this.isFacilitador()) return null
    if (!this.user) {
      this.user = this.getUserFromStorage()
    }
    return this.user?.id || null
  }

  /**
   * Obtener token de autenticación
   */
  getToken() {
    return this.token
  }

  /**
   * Refrescar información del usuario desde el backend
   * Obtiene los datos actualizados del usuario incluyendo nombre_completo y cargo
   */
  async refreshUserInfo() {
    try {
      // Si no hay usuario, obtener de localStorage
      if (!this.user) {
        this.user = this.getUserFromStorage()
      }
      
      // Si tenemos el ID del usuario, obtener datos actualizados del backend
      if (this.user?.id) {
        const response = await axios.get(`${API_URL}/admin/usuarios/${this.user.id}`, {
          headers: {
            'Authorization': `Bearer ${this.token}`
          },
          timeout: 5000
        })
        
        if (response.data) {
          // Actualizar datos del usuario con la info del backend
          const updatedUser = {
            ...this.user,
            nombre_completo: response.data.nombre_completo || '',
            curp: response.data.curp || '',
            cargo: response.data.cargo || '',
            rol: response.data.rol || this.user.rol,
            permisos: response.data.permisos || this.user.permisos,
            es_territorial: response.data.es_territorial || false,
            territorio: response.data.territorio || null
          }
          
          this.user = updatedUser
          localStorage.setItem('admin_user_data', JSON.stringify(updatedUser))
          console.log('✅ Info de usuario actualizada desde backend:', updatedUser)
          return updatedUser
        }
      }
      
      return this.user
    } catch (error) {
      console.warn('⚠️ No se pudo refrescar info del usuario:', error.message)
      // En caso de error, devolver los datos guardados
      return this.user
    }
  }

  /**
   * Verificar estado completo del usuario (activo, rol, permisos)
   * Retorna la información actualizada o null si el usuario fue desactivado
   */
  async checkUserSession() {
    if (!this.user?.username) return null
    
    try {
      const response = await axios.get(`${API_URL}/auth/check-session/${this.user.username}`, {
        headers: {
          'Authorization': `Bearer ${this.token}`
        },
        timeout: 5000 // 5 segundos de timeout
      })
      
      return response.data
    } catch (error) {
      console.error('Error verificando sesión:', error)
      // En caso de error de red, intentar con el endpoint básico
      try {
        const fallbackResponse = await axios.get(`${API_URL}/auth/check-active/${this.user.username}`, {
          headers: {
            'Authorization': `Bearer ${this.token}`
          },
          timeout: 5000
        })
        return { active: fallbackResponse.data.active, exists: fallbackResponse.data.exists }
      } catch (fallbackError) {
        // Si falla también, asumir que sigue activo para no cerrar por problemas de red
        return { active: true, exists: true }
      }
    }
  }

  /**
   * Iniciar verificación en tiempo real de sesión (cada 5 segundos)
   */
  startSessionCheck() {
    this.stopSessionCheck() // Limpiar cualquier intervalo previo
    
    // Verificación inicial inmediata
    this.performSessionCheck()
    
    // Verificar cada 5 segundos
    this.sessionCheckInterval = setInterval(() => {
      this.performSessionCheck()
    }, 5000) // 5 segundos para actualizaciones rápidas
    
    console.log('🔄 Verificación de sesión en tiempo real iniciada (cada 5s)')
  }

  /**
   * Realizar verificación de sesión
   */
  async performSessionCheck() {
    // Salir si no hay sesión activa
    if (!this.user || !this.token) return

    const sessionData = await this.checkUserSession()
    
    if (!sessionData) return

    // Guard: puede que el logout haya ocurrido mientras esperábamos la respuesta
    if (!this.user) return
    
    // Si el usuario fue desactivado, cerrar sesión inmediatamente
    if (!sessionData.active) {
      console.log('⚠️ Usuario desactivado, cerrando sesión...')
      this.forceLogout('Tu cuenta ha sido desactivada por el administrador. Si crees que esto es un error, contacta con soporte.', 'deactivated')
      return
    }
    
    // Si el usuario no existe, cerrar sesión
    if (sessionData.exists === false) {
      console.log('⚠️ Usuario eliminado, cerrando sesión...')
      this.forceLogout('Tu cuenta ha sido eliminada del sistema. Si necesitas acceso nuevamente, contacta con el administrador.', 'deleted')
      return
    }
    
    // Verificar si hubo cambios en rol, permisos o territorio
    if (sessionData.rol !== undefined || sessionData.permisos !== undefined || sessionData.territorio !== undefined) {
      const currentUser = this.user
      let hasRolChange = false
      let hasPermisosChange = false
      let hasTerritorioChange = false
      
      // Verificar cambio de rol
      if (sessionData.rol && sessionData.rol !== currentUser.rol) {
        console.log(`🔄 Rol actualizado: ${currentUser.rol} → ${sessionData.rol}`)
        hasRolChange = true
      }
      
      // Verificar cambio de permisos
      if (sessionData.permisos) {
        const currentPermisos = JSON.stringify(currentUser.permisos || {})
        const newPermisos = JSON.stringify(sessionData.permisos)
        
        if (currentPermisos !== newPermisos) {
          console.log('🔄 Permisos actualizados')
          hasPermisosChange = true
        }
      }
      
      // Verificar cambio de territorio
      if (sessionData.territorio !== currentUser.territorio || sessionData.es_territorial !== currentUser.es_territorial) {
        console.log(`🔄 Territorio actualizado: ${currentUser.territorio || 'global'} → ${sessionData.territorio || 'global'}`)
        hasTerritorioChange = true
      }
      
      // Si hubo cambios, actualizar datos locales y notificar
      if (hasRolChange || hasPermisosChange || hasTerritorioChange) {
        this.user = {
          ...this.user,
          rol: sessionData.rol || this.user.rol,
          permisos: sessionData.permisos || this.user.permisos,
          activo: sessionData.active,
          es_territorial: sessionData.es_territorial !== undefined ? sessionData.es_territorial : this.user.es_territorial,
          territorio: sessionData.territorio !== undefined ? sessionData.territorio : this.user.territorio,
          cargo: sessionData.cargo !== undefined ? sessionData.cargo : this.user.cargo
        }
        
        localStorage.setItem('admin_user_data', JSON.stringify(this.user))
        
        // Si cambió el ROL o el territorio, forzar refresh inmediato de la página
        if (hasRolChange || hasTerritorioChange) {
          const reason = hasTerritorioChange ? 'territorio-changed' : 'role-changed'
          const message = hasTerritorioChange 
            ? 'Se ha actualizado tu territorio asignado. Aplicando cambios...'
            : 'Se han actualizado tus permisos de acceso. Aplicando cambios...'
          
          console.log(`⚠️ Cambio de ${hasTerritorioChange ? 'territorio' : 'rol'} detectado - Recargando página inmediatamente...`)
          
          // Mostrar mensaje profesional antes del refresh
          window.dispatchEvent(new CustomEvent('force-refresh', {
            detail: {
              message,
              reason
            }
          }))
          
          // Refresh casi inmediato (500ms solo para mostrar brevemente el mensaje)
          setTimeout(() => {
            window.location.reload()
          }, 500)
          return
        }
        
        // Si solo cambiaron permisos (no rol ni territorio), solo notificar sin refresh
        // Notificar a la aplicación del cambio
        if (this.onUserUpdated) {
          this.onUserUpdated(this.user)
        }
        
        // Disparar evento global para que los componentes reaccionen
        window.dispatchEvent(new CustomEvent('user-session-updated', { 
          detail: this.user 
        }))
        
        console.log('✅ Datos de usuario actualizados en tiempo real')
      }
    }
  }

  /**
   * Detener verificación periódica
   */
  stopSessionCheck() {
    if (this.sessionCheckInterval) {
      clearInterval(this.sessionCheckInterval)
      this.sessionCheckInterval = null
      console.log('⏹️ Verificación de sesión detenida')
    }
  }

  /**
   * Forzar cierre de sesión (cuando el usuario es desactivado/eliminado)
   */
  forceLogout(message = 'Tu sesión ha sido cerrada.', reason = 'deactivated') {
    this.logout()
    
    // Disparar evento para que App.vue muestre el modal profesional
    window.dispatchEvent(new CustomEvent('force-logout', {
      detail: {
        message,
        reason // 'deactivated', 'deleted', 'expired'
      }
    }))
  }
}

// Exportar instancia única
export default new AuthService()
