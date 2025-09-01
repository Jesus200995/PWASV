// Servicio para obtener estadísticas del sistema
import axios from 'axios'
import { API_URL } from '../config/api.js'

console.log(`🌐 EstadísticasService usando API: ${API_URL}`)

class EstadisticasService {
  async obtenerEstadisticas() {
    try {
      console.log('🔍 Obteniendo estadísticas desde el servidor...')
      
      const token = localStorage.getItem('admin_token')
      const response = await axios.get(`${API_URL}/estadisticas`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      
      if (response.data && response.data.estadisticas) {
        const stats = response.data.estadisticas
        console.log('✅ Estadísticas obtenidas:', stats)
        
        return {
          totalRegistros: stats.total_registros || 0,
          totalUsuarios: stats.total_usuarios || 0,
          registrosHoy: stats.registros_hoy || 0,
          totalAsistencias: stats.total_asistencias || 0,
          asistenciasHoy: stats.asistencias_hoy || 0,
          usuariosPresentes: stats.usuarios_presentes || 0
        }
      }
      
      throw new Error('Respuesta inválida del servidor')
      
    } catch (error) {
      console.error('❌ Error obteniendo estadísticas:', error)
      
      // Si es error 401, podría ser token expirado
      if (error.response?.status === 401) {
        console.warn('🔓 Token posiblemente expirado, necesita re-login')
        throw new Error('TOKEN_EXPIRED')
      }
      
      // Para otros errores, propagar el mensaje
      throw error
    }
  }

  // Método para obtener estadísticas del día actual en horario CDMX
  async obtenerEstadisticasDiaActual() {
    try {
      console.log('📅 Obteniendo estadísticas del día actual CDMX...')
      
      const token = localStorage.getItem('admin_token')
      const response = await axios.get(`${API_URL}/estadisticas/dia-actual`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      
      if (response.data && response.data.estadisticas) {
        const stats = response.data.estadisticas
        console.log('✅ Estadísticas del día obtenidas:', stats)
        
        return {
          totalUsuariosDia: stats.total_usuarios_dia || 0,
          entradasDia: stats.entradas_dia || 0,
          salidasDia: stats.salidas_dia || 0,
          actividadesDia: stats.actividades_dia || 0,
          fechaCDMX: stats.fecha_cdmx || null
        }
      }
      
      throw new Error('Respuesta inválida del servidor')
      
    } catch (error) {
      console.error('❌ Error obteniendo estadísticas del día:', error)
      
      // Si es error 401, podría ser token expirado
      if (error.response?.status === 401) {
        console.warn('🔓 Token posiblemente expirado, necesita re-login')
        throw new Error('TOKEN_EXPIRED')
      }
      
      // Para otros errores, propagar el mensaje
      throw error
    }
  }

  // Método para obtener total de usuarios únicos del día
  async obtenerUsuariosDia() {
    try {
      console.log('👥 Obteniendo usuarios únicos del día CDMX...')
      
      const token = localStorage.getItem('admin_token')
      const response = await axios.get(`${API_URL}/estadisticas/usuarios-dia`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      
      if (response.data) {
        return response.data.total_usuarios_dia || 0
      }
      
      return 0
      
    } catch (error) {
      console.error('❌ Error obteniendo usuarios del día:', error)
      return 0
    }
  }

  // Método para obtener entradas del día
  async obtenerEntradasDia() {
    try {
      console.log('🚪➡️ Obteniendo entradas del día CDMX...')
      
      const token = localStorage.getItem('admin_token')
      const response = await axios.get(`${API_URL}/estadisticas/entradas-dia`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      
      if (response.data) {
        return response.data.entradas_dia || 0
      }
      
      return 0
      
    } catch (error) {
      console.error('❌ Error obteniendo entradas del día:', error)
      return 0
    }
  }

  // Método para obtener salidas del día
  async obtenerSalidasDia() {
    try {
      console.log('🚪⬅️ Obteniendo salidas del día CDMX...')
      
      const token = localStorage.getItem('admin_token')
      const response = await axios.get(`${API_URL}/estadisticas/salidas-dia`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      
      if (response.data) {
        return response.data.salidas_dia || 0
      }
      
      return 0
      
    } catch (error) {
      console.error('❌ Error obteniendo salidas del día:', error)
      return 0
    }
  }

  // Método para obtener actividades del día
  async obtenerActividadesDia() {
    try {
      console.log('📝 Obteniendo actividades del día CDMX...')
      
      const token = localStorage.getItem('admin_token')
      const response = await axios.get(`${API_URL}/estadisticas/actividades-dia`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      
      if (response.data) {
        return response.data.actividades_dia || 0
      }
      
      return 0
      
    } catch (error) {
      console.error('❌ Error obteniendo actividades del día:', error)
      return 0
    }
  }
  
  // Método para obtener estadísticas con fallback local
  async obtenerEstadisticasConFallback(registros = [], usuarios = [], asistencias = []) {
    try {
      // Intentar obtener desde el servidor primero
      return await this.obtenerEstadisticas()
    } catch (error) {
      console.warn('⚠️ Usando estadísticas locales como fallback')
      
      // Calcular estadísticas localmente como fallback
      const hoy = new Date().toDateString()
      const hoyISO = new Date().toISOString().split('T')[0]
      
      const registrosHoy = registros.filter(r => {
        const fechaRegistro = new Date(r.fecha_hora).toDateString()
        return fechaRegistro === hoy
      }).length
      
      const asistenciasHoy = asistencias.filter(a => a.fecha === hoyISO).length
      
      const usuariosPresentes = new Set()
      asistencias.forEach(a => {
        if (a.fecha === hoyISO && a.hora_entrada) {
          usuariosPresentes.add(a.usuario_id)
        }
      })
      
      return {
        totalRegistros: registros.length,
        totalUsuarios: usuarios.length,
        registrosHoy: registrosHoy,
        totalAsistencias: asistencias.length,
        asistenciasHoy: asistenciasHoy,
        usuariosPresentes: usuariosPresentes.size
      }
    }
  }
}

// Exportar instancia única del servicio
export const estadisticasService = new EstadisticasService()
export default estadisticasService
