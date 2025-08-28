// Servicio simplificado para probar conectividad
import { API_URL } from '../config/api.js'

console.log('🌐 PermisosService Simple usando API:', API_URL)

const permisosServiceSimple = {
  async listarUsuarios() {
    try {
      console.log('🔄 Obteniendo usuarios admin (versión simple)...')
      
      const response = await fetch(`${API_URL}/admin/usuarios`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      console.log('✅ Usuarios obtenidos con fetch:', data)
      
      return { usuarios: data.usuarios || data || [] }
      
    } catch (error) {
      console.error('❌ Error con fetch:', error)
      throw new Error(error.message)
    }
  }
}

export default permisosServiceSimple
