// Servicio simplificado para probar conectividad
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
console.log('🌐 PermisosService Simple usando API:', API_BASE_URL)

const permisosServiceSimple = {
  async listarUsuarios() {
    try {
      console.log('🔄 Obteniendo usuarios admin (versión simple)...')
      
      const response = await fetch(`${API_BASE_URL}/admin/usuarios`, {
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
