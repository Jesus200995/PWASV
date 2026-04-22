/**
 * Servicio para el módulo de Firmas (Facilitadores Comunitarios)
 */
import { API_URL } from '../config/api'

const facilitadoresService = {
  /**
   * Obtener reportes de mis técnicos asignados
   */
  async misReportes(adminId, { estado = null, limite = 50, offset = 0 } = {}) {
    const params = new URLSearchParams({ admin_id: adminId, limite, offset })
    if (estado) params.append('estado', estado)
    const res = await fetch(`${API_URL}/reportes/facilitador/mis-reportes?${params}`)
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `Error ${res.status}`)
    }
    return res.json()
  },

  /**
   * Obtener mis técnicos asignados
   */
  async misTecnicos(adminId) {
    const res = await fetch(`${API_URL}/facilitadores/mis-tecnicos?admin_id=${adminId}`)
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `Error ${res.status}`)
    }
    return res.json()
  },

  /**
   * Obtener PDF de un reporte
   */
  async obtenerPDF(reporteId) {
    const res = await fetch(`${API_URL}/reportes/${reporteId}/pdf`)
    if (!res.ok) throw new Error(`Error ${res.status}`)
    return res.json()
  },

  /**
   * Firmar un reporte (flujo facilitador)
   * @param {number} reporteId
   * @param {number} adminId - ID del admin_users del facilitador
   * @param {string|null} firmaBase64 - Firma digital en base64 (opcional)
   */
  async firmarReporte(reporteId, adminId, firmaBase64 = null) {
    const body = {
      admin_id: adminId,
      supervisor_id: 0,
      nombre_supervisor: '',
      firma_base64: firmaBase64
    }
    const res = await fetch(`${API_URL}/reportes/firmar/${reporteId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `Error ${res.status}`)
    }
    return res.json()
  },

  /**
   * Listar técnicos de pwasuper disponibles para asociar
   * (solo técnicos sin facilitador asignado)
   */
  async listarTecnicosDisponibles(adminId, { q = '', territorio = '', limite = 50 } = {}) {
    const params = new URLSearchParams({ admin_id: adminId, limite })
    if (q) params.append('q', q)
    if (territorio) params.append('territorio', territorio)
    const res = await fetch(`${API_URL}/facilitadores/tecnicos-disponibles?${params}`)
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `Error ${res.status}`)
    }
    return res.json()
  },

  /**
   * Asociar un técnico al facilitador (origen='manual')
   */
  async asignarTecnico(adminId, tecnicoUsuarioId) {
    const res = await fetch(`${API_URL}/facilitadores/asignar-tecnico`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ admin_id: adminId, tecnico_usuario_id: tecnicoUsuarioId })
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `Error ${res.status}`)
    }
    return res.json()
  },

  /**
   * Desasociar un técnico del facilitador (solo origen='manual')
   */
  async desasignarTecnico(adminId, tecnicoUsuarioId) {
    const params = new URLSearchParams({ admin_id: adminId, tecnico_usuario_id: tecnicoUsuarioId })
    const res = await fetch(`${API_URL}/facilitadores/asignar-tecnico?${params}`, {
      method: 'DELETE'
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || `Error ${res.status}`)
    }
    return res.json()
  }
}

export default facilitadoresService
