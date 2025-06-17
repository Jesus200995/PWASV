// Servicio de usuarios alternativo usando endpoints existentes
// SOLO USAR SI NO SE PUEDE DESPLEGAR EL BACKEND ACTUALIZADO

const API_BASE = 'https://apipwa.sembrandodatos.com';

class UsuariosServiceAlternativo {
  constructor() {
    this.cache = new Map();
  }

  async obtenerUsuarios() {
    try {
      console.log('🔍 Obteniendo usuarios usando método alternativo...');
      
      // Método 1: Obtener registros y extraer IDs únicos de usuario
      const response = await fetch(`${API_BASE}/registros`);
      
      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }
      
      const data = await response.json();
      const registros = data.registros || [];
      
      // Extraer IDs únicos de usuarios de los registros
      const idsUnicos = [...new Set(registros.map(r => r.usuario_id))];
      
      console.log(`📊 Encontrados ${idsUnicos.length} usuarios únicos en registros`);
      
      // Generar estructura básica de usuarios
      const usuarios = idsUnicos.map(id => ({
        id: id,
        correo: `usuario${id}@empresa.com`,
        nombre_completo: `Usuario ${id}`,
        cargo: 'Empleado',
        supervisor: 'Por asignar',
        _fromRegistros: true // Marca que viene de registros
      }));
      
      return usuarios;
      
    } catch (error) {
      console.error('❌ Error en método alternativo:', error);
      throw error;
    }
  }

  async obtenerUsuario(id) {
    // Intentar obtener de la lista completa
    const usuarios = await this.obtenerUsuarios();
    return usuarios.find(u => u.id === id) || null;
  }

  async obtenerUsuariosPorIds(ids) {
    const usuarios = await this.obtenerUsuarios();
    return usuarios.filter(u => ids.includes(u.id));
  }

  async enriquecerRegistrosConUsuarios(registros) {
    // Para este método alternativo, simplemente agregar datos básicos
    return registros.map(registro => ({
      ...registro,
      usuario: {
        id: registro.usuario_id,
        nombre_completo: `Usuario ${registro.usuario_id}`,
        correo: `usuario${registro.usuario_id}@empresa.com`,
        cargo: 'Empleado',
        supervisor: 'Por asignar'
      }
    }));
  }

  // Métodos de compatibilidad
  async obtenerUsuarioPorId(usuarioId) {
    return await this.obtenerUsuario(usuarioId);
  }

  async obtenerTodosLosUsuarios() {
    return await this.obtenerUsuarios();
  }

  limpiarCache() {
    this.cache.clear();
    console.log('🗑️ Cache limpiado');
  }
}

// Exportar
export const usuariosServiceAlternativo = new UsuariosServiceAlternativo();
export default usuariosServiceAlternativo;
