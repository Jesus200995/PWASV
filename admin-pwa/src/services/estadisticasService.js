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
          // ==================== NUEVAS ESTADÍSTICAS PARA VISOR MAP ====================
          totalUsuarios: stats.total_usuarios_unicos || 0,
          entradasDelDia: stats.entradas_del_dia || 0,
          salidasDelDia: stats.salidas_del_dia || 0,
          actividadesDeHoy: stats.actividades_de_hoy || 0,
          
          // ==================== ESTADÍSTICAS LEGACY (para compatibilidad) ====================
          totalRegistros: stats.total_registros || 0,
          totalUsuariosLegacy: stats.total_usuarios || 0,
          registrosHoy: stats.registros_hoy || 0,
          totalAsistencias: stats.total_asistencias || 0,
          asistenciasHoy: stats.asistencias_hoy || 0,
          usuariosPresentes: stats.usuarios_presentes || 0,
          
          // ==================== INFORMACIÓN ADICIONAL ====================
          fechaConsultaCDMX: stats.fecha_consulta_cdmx || null,
          rangoConsulta: stats.rango_utc_consulta || null
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
      
      // Calcular entradas y salidas del día para fallback
      const entradasHoy = asistencias.filter(a => a.fecha === hoyISO && a.hora_entrada).length
      const salidasHoy = asistencias.filter(a => a.fecha === hoyISO && a.hora_salida).length
      
      return {
        // ==================== NUEVAS ESTADÍSTICAS PARA VISOR MAP ====================
        totalUsuarios: usuarios.length,
        entradasDelDia: entradasHoy,
        salidasDelDia: salidasHoy,
        actividadesDeHoy: registrosHoy,
        
        // ==================== ESTADÍSTICAS LEGACY ====================
        totalRegistros: registros.length,
        totalUsuariosLegacy: usuarios.length,
        registrosHoy: registrosHoy,
        totalAsistencias: asistencias.length,
        asistenciasHoy: asistenciasHoy,
        usuariosPresentes: usuariosPresentes.size,
        
        // ==================== INFORMACIÓN ADICIONAL ====================
        fechaConsultaCDMX: hoyISO,
        rangoConsulta: null
      }
    }
  }
}

// Exportar instancia única del servicio
export const estadisticasService = new EstadisticasService()
export default estadisticasService
