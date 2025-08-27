import axios from 'axios'
import { API_URL } from '../config/api.js'

console.log('🌐 PermisosService usando API:', API_URL)

// Crear instancia de axios con configuración
const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor para agregar token de autorización
api.interceptors.request.use(
  (config) => {
    // Por ahora no requerir autenticación para estos endpoints
    const token = localStorage.getItem('admin_token')
    if (token) {
      // Solo agregar el token si es necesario
      // config.headers.Authorization = `Bearer ${token}`
      console.log('🔐 Token disponible:', token.substring(0, 20) + '...')
    }
    return config
  },
  (error) => {
    console.error('❌ Error en interceptor de request:', error)
    return Promise.reject(error)
  }
)

// Interceptor para manejar respuestas y errores
api.interceptors.response.use(
  (response) => {
    console.log('✅ Respuesta exitosa:', response.status, response.config.url)
    return response
  },
  (error) => {
    console.error('❌ Error en respuesta:', error.response?.status, error.config?.url)
    console.error('❌ Detalles del error:', error.response?.data)
    
    // Si el token es inválido, redirigir al login
    if (error.response?.status === 401) {
      console.log('🔄 Token inválido, eliminando token y redirigiendo al login')
      localStorage.removeItem('admin_token')
      window.location.href = '/login'
    }
    
    return Promise.reject(error)
  }
)

const permisosService = {
  /**
   * Obtener lista de todos los usuarios administrativos de la tabla admin_users
   */
  async listarUsuarios() {
    try {
      console.log('🔄 Obteniendo lista de usuarios administrativos...')
      const response = await api.get('/admin/usuarios')
      
      // Procesar usuarios admin
      const usuarios = response.data.usuarios || response.data || []
      console.log('✅ Usuarios administrativos obtenidos:', usuarios.length)
      return { usuarios }
      
    } catch (error) {
      console.error('❌ Error obteniendo usuarios administrativos:', error)
      throw this.manejarError(error)
    }
  },

  /**
   * Crear un nuevo usuario administrativo en la tabla admin_users
   */
  async crearUsuario(datosUsuario) {
    try {
      console.log('🔄 Creando usuario administrativo:', datosUsuario)
      
      // Preparar datos para envío
      const usuarioData = {
        username: datosUsuario.username.trim(),
        password: datosUsuario.password,
        rol: datosUsuario.rol || 'user'
      }
      
      const response = await api.post('/admin/usuarios', usuarioData)
      
      console.log('✅ Usuario administrativo creado exitosamente:', response.data)
      return response.data
      
    } catch (error) {
      console.error('❌ Error creando usuario administrativo:', error)
      throw this.manejarError(error)
    }
  },

  /**
   * Actualizar información de usuario administrativo
   */
  async actualizarUsuario(userId, datosUsuario) {
    try {
      console.log('🔄 Actualizando usuario administrativo:', userId, datosUsuario)
      
      // Preparar datos para envío
      const usuarioData = {
        username: datosUsuario.username.trim(),
        rol: datosUsuario.rol || 'user'
      }

      // Si hay nueva contraseña, incluirla
      if (datosUsuario.password && datosUsuario.password.trim()) {
        usuarioData.password = datosUsuario.password
      }
      
      const response = await api.put(`/admin/usuarios/${userId}`, usuarioData)
      
      console.log('✅ Usuario administrativo actualizado exitosamente:', response.data)
      return response.data
      
    } catch (error) {
      console.error('❌ Error actualizando usuario administrativo:', error)
      throw this.manejarError(error)
    }
  },

  /**
   * Eliminar usuario administrativo del sistema
   */
  async eliminarUsuario(userId) {
    try {
      console.log('🔄 Eliminando usuario administrativo:', userId)
      
      const response = await api.delete(`/admin/usuarios/${userId}`)
      
      console.log('✅ Usuario administrativo eliminado exitosamente')
      return response.data
      
    } catch (error) {
      console.error('❌ Error eliminando usuario administrativo:', error)
      throw this.manejarError(error)
    }
  },

  /**
   * Obtener información detallada de un usuario administrativo específico
   */
  async obtenerUsuario(userId) {
    try {
      console.log('🔄 Obteniendo usuario administrativo:', userId)
      
      const response = await api.get(`/admin/usuarios/${userId}`)
      
      const usuario = response.data
      
      console.log('✅ Usuario administrativo obtenido:', usuario)
      return usuario
      
    } catch (error) {
      console.error('❌ Error obteniendo usuario administrativo:', error)
      throw this.manejarError(error)
    }
  },

  /**
   * Cambiar rol de usuario administrativo (admin/user)
   */
  async cambiarRolUsuario(userId, nuevoRol) {
    try {
      console.log('🔄 Cambiando rol de usuario administrativo:', userId, 'a', nuevoRol)
      
      const response = await api.put(`/admin/usuarios/${userId}/rol`, {
        rol: nuevoRol
      })
      
      console.log('✅ Rol cambiado exitosamente')
      return response.data
      
    } catch (error) {
      console.error('❌ Error cambiando rol:', error)
      throw this.manejarError(error)
    }
  },

  /**
   * Resetear contraseña de usuario administrativo
   */
  async resetearContrasena(userId, nuevaContrasena) {
    try {
      console.log('🔄 Reseteando contraseña de usuario administrativo:', userId)
      
      const response = await api.put(`/admin/usuarios/${userId}/password`, {
        password: nuevaContrasena
      })
      
      console.log('✅ Contraseña reseteada exitosamente')
      return response.data
      
    } catch (error) {
      console.error('❌ Error reseteando contraseña:', error)
      throw this.manejarError(error)
    }
  },

  /**
   * Obtener estadísticas de usuarios administrativos
   */
  async obtenerEstadisticas() {
    try {
      console.log('🔄 Obteniendo estadísticas de usuarios administrativos...')
      
      const response = await api.get('/admin/usuarios/estadisticas')
      
      console.log('✅ Estadísticas obtenidas:', response.data)
      return response.data
      
    } catch (error) {
      console.error('❌ Error obteniendo estadísticas:', error)
      throw this.manejarError(error)
    }
  },

  /**
   * Buscar usuarios administrativos por criterios específicos
   */
  async buscarUsuarios(criterio, valor) {
    try {
      console.log('🔄 Buscando usuarios administrativos:', criterio, valor)
      
      const response = await api.get('/admin/usuarios/buscar', {
        params: {
          [criterio]: valor
        }
      })
      
      const usuarios = response.data.usuarios || response.data || []
      
      console.log('✅ Búsqueda completada:', usuarios.length, 'resultados')
      return { usuarios }
      
    } catch (error) {
      console.error('❌ Error en búsqueda:', error)
      throw this.manejarError(error)
    }
  },

  /**
   * Validar permisos de usuario administrativo actual
   */
  async validarPermisos() {
    try {
      console.log('🔄 Validando permisos de usuario administrativo actual...')
      
      const response = await api.get('/admin/auth/validar')
      
      console.log('✅ Permisos validados:', response.data)
      return response.data
      
    } catch (error) {
      console.error('❌ Error validando permisos:', error)
      throw this.manejarError(error)
    }
  },

  /**
   * Manejar errores de la API de manera consistente
   */
  manejarError(error) {
    let mensaje = 'Error desconocido'
    
    if (error.response) {
      // Error de respuesta del servidor
      const status = error.response.status
      const data = error.response.data
      
      switch (status) {
        case 400:
          mensaje = data.detail || 'Datos inválidos'
          break
        case 401:
          mensaje = 'No autorizado. Inicia sesión nuevamente'
          break
        case 403:
          mensaje = 'No tienes permisos para realizar esta acción'
          break
        case 404:
          mensaje = 'Usuario no encontrado'
          break
        case 409:
          mensaje = data.detail || 'El usuario ya existe'
          break
        case 422:
          if (data.detail && Array.isArray(data.detail)) {
            mensaje = data.detail.map(d => d.msg).join(', ')
          } else {
            mensaje = data.detail || 'Datos inválidos'
          }
          break
        case 500:
          mensaje = 'Error interno del servidor'
          break
        default:
          mensaje = data.detail || `Error del servidor (${status})`
      }
    } else if (error.request) {
      // Error de red o conexión
      mensaje = 'Error de conexión. Verifica tu conexión a internet'
    } else {
      // Error en la configuración de la petición
      mensaje = error.message || 'Error en la petición'
    }
    
    console.error('💥 Error procesado:', mensaje)
    return new Error(mensaje)
  },

  /**
   * Obtener URL base de la API
   */
  getApiBaseUrl() {
    return API_BASE_URL
  },

  /**
   * Verificar conexión con la API
   */
  async verificarConexion() {
    try {
      console.log('🔄 Verificando conexión con la API...')
      
      const response = await api.get('/health', { timeout: 5000 })
      
      console.log('✅ Conexión verificada exitosamente')
      return true
      
    } catch (error) {
      console.error('❌ Error verificando conexión:', error)
      return false
    }
  }
}

export default permisosService
