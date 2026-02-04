/**
 * Servicio para gestionar reportes en admin-pwa
 */
import { API_URL } from '../config/api'
import { generarPDFDesdesDatos } from '../utils/pdfGenerator'

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
   * Limpiar y normalizar el base64
   * @param {string} base64String - String base64 que puede contener prefijos o espacios
   * @returns {string} - Base64 limpio
   */
  _limpiarBase64(base64String) {
    if (!base64String) return ''
    
    // Remover el prefijo data:application/pdf;base64, si existe
    let limpio = base64String
    if (limpio.includes('data:application/pdf;base64,')) {
      limpio = limpio.split('data:application/pdf;base64,')[1]
    } else if (limpio.includes('base64,')) {
      limpio = limpio.split('base64,')[1]
    }
    
    // Remover espacios, saltos de línea y otros caracteres no base64
    limpio = limpio.replace(/\s/g, '')
    limpio = limpio.replace(/[^A-Za-z0-9+/=]/g, '')
    
    return limpio
  },

  /**
   * Obtener datos de un reporte específico
   * @param {number} reporteId - ID del reporte
   * @returns {Object} - Datos del reporte
   */
  async obtenerReporte(reporteId) {
    try {
      const url = `${API_URL}/reportes/descargar/${reporteId}`
      console.log('📊 [ReportesService] Obteniendo reporte:', reporteId)
      
      const response = await fetch(url)
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`)
      }
      
      const data = await response.json()
      console.log('✅ [ReportesService] Reporte obtenido:', data)
      
      return data
    } catch (error) {
      console.error('❌ [ReportesService] Error obteniendo reporte:', error)
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
        // Limpiar el base64
        const base64Limpio = this._limpiarBase64(data.reporte.pdf_base64)
        
        if (!base64Limpio) {
          throw new Error('El PDF está vacío o mal formado')
        }
        
        // Convertir base64 a blob y descargar
        const byteCharacters = atob(base64Limpio)
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
   * NUEVO FLUJO: Genera PDF desde datos estructurados si existen
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
      
      if (!data.success || !data.reporte) {
        throw new Error('Reporte no encontrado')
      }
      
      const reporte = data.reporte
      let pdfBlob = null
      
      // NUEVO FLUJO: Si hay datos_reporte, generar PDF desde datos estructurados
      if (reporte.datos_reporte) {
        console.log('📄 Generando PDF desde datos_reporte...')
        
        try {
          const pdfBase64 = await generarPDFDesdesDatos(
            reporte.datos_reporte,
            reporte.firma_usuario_base64,
            reporte.firma_supervisor_base64,
            reporte.nombre_supervisor
          )
          
          // Convertir base64 a blob
          const byteCharacters = atob(pdfBase64)
          const byteNumbers = new Array(byteCharacters.length)
          for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i)
          }
          const byteArray = new Uint8Array(byteNumbers)
          pdfBlob = new Blob([byteArray], { type: 'application/pdf' })
          
          console.log('✅ PDF generado desde datos_reporte')
        } catch (error) {
          console.error('❌ Error generando PDF desde datos:', error)
          throw new Error('No se pudo generar el PDF: ' + error.message)
        }
      }
      // COMPATIBILIDAD: Si hay PDF guardado (reportes antiguos o con pdf_base64)
      else if (reporte.pdf_base64) {
        const base64Limpio = this._limpiarBase64(reporte.pdf_base64)
        
        if (!base64Limpio) {
          throw new Error('El PDF está vacío o mal formado')
        }
        
        // Convertir a blob
        const byteCharacters = atob(base64Limpio)
        const byteNumbers = new Array(byteCharacters.length)
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i)
        }
        const byteArray = new Uint8Array(byteNumbers)
        pdfBlob = new Blob([byteArray], { type: 'application/pdf' })
      } else {
        throw new Error('PDF no disponible')
      }
      
      if (pdfBlob) {
        // Abrir en nueva pestaña
        const urlBlob = window.URL.createObjectURL(pdfBlob)
        window.open(urlBlob, '_blank')
        
        console.log('✅ [ReportesService] Reporte abierto en nueva pestaña')
        return { success: true }
      } else {
        throw new Error('No se pudo generar el PDF')
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
  },

  /**
   * Firmar un reporte como supervisor
   * @param {number} reporteId - ID del reporte
   * @param {Object} firmaData - Datos de la firma
   * @param {number} firmaData.supervisor_id - ID del supervisor
   * @param {string} firmaData.nombre_supervisor - Nombre del supervisor
   * @param {string} firmaData.firma_base64 - Firma en base64 (opcional)
   */
  async firmarReporte(reporteId, firmaData) {
    try {
      const url = `${API_URL}/reportes/firmar/${reporteId}`
      console.log('✍️ [ReportesService] Firmando reporte:', reporteId)
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(firmaData)
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`)
      }
      
      const data = await response.json()
      console.log('✅ [ReportesService] Reporte firmado:', data)
      
      return data
    } catch (error) {
      console.error('❌ [ReportesService] Error firmando reporte:', error)
      throw error
    }
  },

  /**
   * Firmar múltiples reportes
   * @param {Array} reporteIds - Array de IDs de reportes a firmar
   * @param {Object} firmaData - Datos de la firma
   */
  async firmarMultiplesReportes(reporteIds, firmaData) {
    const resultados = {
      exitosos: [],
      fallidos: []
    }

    for (const reporteId of reporteIds) {
      try {
        await this.firmarReporte(reporteId, firmaData)
        resultados.exitosos.push(reporteId)
      } catch (error) {
        resultados.fallidos.push({ id: reporteId, error: error.message })
      }
    }

    return resultados
  },

  /**
   * Quitar firma de un reporte
   * @param {number} reporteId - ID del reporte
   * @param {number} supervisorId - ID del supervisor
   */
  async quitarFirmaReporte(reporteId, supervisorId) {
    try {
      const url = `${API_URL}/reportes/quitar-firma/${reporteId}?supervisor_id=${supervisorId}`
      console.log('🔓 [ReportesService] Quitando firma del reporte:', reporteId)
      
      const response = await fetch(url, { method: 'DELETE' })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `Error ${response.status}`)
      }
      
      const data = await response.json()
      console.log('✅ [ReportesService] Firma removida')
      
      return data
    } catch (error) {
      console.error('❌ [ReportesService] Error quitando firma:', error)
      throw error
    }
  },

  /**
   * Descargar múltiples reportes en formato ZIP
   * @param {URLSearchParams} params - Parámetros de filtro (mes, anio, tipo_descarga)
   */
  async descargarReportesZip(params) {
    try {
      const url = `${API_URL}/reportes/admin/descargar-zip?${params.toString()}`
      console.log('📦 [ReportesService] Descargando ZIP:', url)
      
      const response = await fetch(url)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`)
      }
      
      // Obtener el blob del ZIP
      const blob = await response.blob()
      
      // Obtener nombre del archivo desde headers o usar uno por defecto
      const contentDisposition = response.headers.get('Content-Disposition')
      let filename = 'Reportes.zip'
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/)
        if (filenameMatch && filenameMatch[1]) {
          filename = filenameMatch[1]
        }
      }
      
      // Crear enlace de descarga
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(downloadUrl)
      
      console.log('✅ [ReportesService] ZIP descargado:', filename)
      
      return { success: true, filename }
    } catch (error) {
      console.error('❌ [ReportesService] Error descargando ZIP:', error)
      throw error
    }
  }
}

export default reportesService
