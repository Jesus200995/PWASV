/**
 * Servicio para gestionar reportes en admin-pwa
 */
import { API_URL } from '../config/api'

const reportesService = {
  /**
   * Obtener todos los reportes de todos los usuarios
   * @param {Object} filtros - Filtros opcionales
   * @param {number} filtros.limite - Cantidad por página
   * @param {number} filtros.offset - Desplazamiento
   * @param {string} filtros.mes - Filtrar por mes
   * @param {number} filtros.anio - Filtrar por año
   * @param {string} filtros.territorio - Filtrar por territorio
   * @param {number} filtros.usuario_id - Filtrar por usuario
   */
  async obtenerTodosReportes(filtros = {}) {
    try {
      const params = new URLSearchParams()
      
      if (filtros.limite) params.append('limite', filtros.limite)
      if (filtros.offset !== undefined) params.append('offset', filtros.offset)
      if (filtros.mes) params.append('mes', filtros.mes)
      if (filtros.anio) params.append('anio', filtros.anio)
      if (filtros.territorio) params.append('territorio', filtros.territorio)
      if (filtros.usuario_id) params.append('usuario_id', filtros.usuario_id)
      
      const url = `${API_URL}/reportes/admin/todos?${params.toString()}`
      console.log('📊 [ReportesService] Obteniendo reportes:', url)
      
      const response = await fetch(url)
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`)
      }
      
      const data = await response.json()
      console.log('✅ [ReportesService] Reportes obtenidos:', data)
      
      return data
    } catch (error) {
      console.error('❌ [ReportesService] Error obteniendo reportes:', error)
      throw error
    }
  },

  /**
   * Obtener estadísticas de reportes
   */
  async obtenerEstadisticas() {
    try {
      const url = `${API_URL}/reportes/admin/estadisticas`
      console.log('📊 [ReportesService] Obteniendo estadísticas...')
      
      const response = await fetch(url)
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`)
      }
      
      const data = await response.json()
      console.log('✅ [ReportesService] Estadísticas obtenidas:', data)
      
      return data
    } catch (error) {
      console.error('❌ [ReportesService] Error obteniendo estadísticas:', error)
      throw error
    }
  },

  /**
   * Descargar un reporte específico
   * @param {number} reporteId - ID del reporte
   */
  async descargarReporte(reporteId) {
    try {
      const url = `${API_URL}/reportes/descargar/${reporteId}`
      console.log('📥 [ReportesService] Descargando reporte:', reporteId)
      
      const response = await fetch(url)
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`)
      }
      
      const data = await response.json()
      
      if (data.success && data.reporte?.pdf_base64) {
        // Convertir base64 a blob y descargar
        const byteCharacters = atob(data.reporte.pdf_base64)
        const byteNumbers = new Array(byteCharacters.length)
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i)
        }
        const byteArray = new Uint8Array(byteNumbers)
        const blob = new Blob([byteArray], { type: 'application/pdf' })
        
        // Crear link de descarga
        const urlBlob = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = urlBlob
        a.download = data.reporte.nombre || `reporte_${reporteId}.pdf`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(urlBlob)
        document.body.removeChild(a)
        
        console.log('✅ [ReportesService] Reporte descargado')
        return { success: true }
      } else {
        throw new Error('PDF no disponible')
      }
    } catch (error) {
      console.error('❌ [ReportesService] Error descargando reporte:', error)
      throw error
    }
  },

  /**
   * Ver reporte en nueva pestaña
   * @param {number} reporteId - ID del reporte
   */
  async verReporte(reporteId) {
    try {
      const url = `${API_URL}/reportes/descargar/${reporteId}`
      console.log('👁️ [ReportesService] Visualizando reporte:', reporteId)
      
      const response = await fetch(url)
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`)
      }
      
      const data = await response.json()
      
      if (data.success && data.reporte?.pdf_base64) {
        // Abrir en nueva pestaña
        const byteCharacters = atob(data.reporte.pdf_base64)
        const byteNumbers = new Array(byteCharacters.length)
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i)
        }
        const byteArray = new Uint8Array(byteNumbers)
        const blob = new Blob([byteArray], { type: 'application/pdf' })
        
        const urlBlob = window.URL.createObjectURL(blob)
        window.open(urlBlob, '_blank')
        
        console.log('✅ [ReportesService] Reporte abierto en nueva pestaña')
        return { success: true }
      } else {
        throw new Error('PDF no disponible')
      }
    } catch (error) {
      console.error('❌ [ReportesService] Error visualizando reporte:', error)
      throw error
    }
  },

  /**
   * Eliminar un reporte
   * @param {number} reporteId - ID del reporte
   */
  async eliminarReporte(reporteId) {
    try {
      const url = `${API_URL}/reportes/eliminar/${reporteId}`
      console.log('🗑️ [ReportesService] Eliminando reporte:', reporteId)
      
      const response = await fetch(url, { method: 'DELETE' })
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`)
      }
      
      const data = await response.json()
      console.log('✅ [ReportesService] Reporte eliminado')
      
      return data
    } catch (error) {
      console.error('❌ [ReportesService] Error eliminando reporte:', error)
      throw error
    }
  },

  /**
   * Obtener territorios únicos de los reportes
   */
  async obtenerTerritorios() {
    try {
      const url = `${API_URL}/territorios`
      const response = await fetch(url)
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}`)
      }
      
      const data = await response.json()
      return data.territorios || []
    } catch (error) {
      console.error('❌ Error obteniendo territorios:', error)
      return []
    }
  }
}

export default reportesService
