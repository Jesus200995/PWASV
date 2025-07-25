// Servicio para manejo de usuarios usando la API real con endpoints GET
const API_BASE = 'https://apipwa.sembrandodatos.com'; // Servidor de producción

class UsuariosService {
  constructor() {
    this.cache = new Map(); // Cache para mejorar performance
  }

  async obtenerUsuarios() {
    try {
      console.log('🔍 Obteniendo usuarios desde la API real...');
      const response = await fetch(`${API_BASE}/usuarios`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      if (!response.ok) {
        console.error(`❌ Error HTTP: ${response.status} - ${response.statusText}`);
        throw new Error(`Error HTTP: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('✅ Respuesta de la API:', data);
      
      // El endpoint devuelve {usuarios: []} según la implementación del backend
      let usuarios = [];
      if (data.usuarios && Array.isArray(data.usuarios)) {
        usuarios = data.usuarios;
      } else if (Array.isArray(data)) {
        usuarios = data;
      }
      
      // Actualizar cache con los usuarios obtenidos
      usuarios.forEach(usuario => {
        this.cache.set(usuario.id, usuario);
      });
      
      console.log(`✅ ${usuarios.length} usuarios obtenidos desde la base de datos`);
      return usuarios;
      
    } catch (error) {
      console.error('❌ Error al obtener usuarios desde la base de datos:', error);
      throw error; // Propagar el error para manejo en las vistas
    }
  }

  async obtenerUsuario(id) {
    try {
      // Verificar cache primero
      if (this.cache.has(id)) {
        console.log(`📋 Usuario ${id} encontrado en cache`);
        return this.cache.get(id);
      }

      console.log(`🔍 Obteniendo usuario ${id} desde la API real...`);
      const response = await fetch(`${API_BASE}/usuarios/${id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      if (!response.ok) {
        if (response.status === 404) {
          console.warn(`⚠️ Usuario ${id} no encontrado en la base de datos`);
          return null;
        }
        console.error(`❌ Error HTTP: ${response.status} - ${response.statusText}`);
        throw new Error(`Error HTTP: ${response.status}`);
      }
      
      const usuario = await response.json();
      console.log(`✅ Usuario ${id} obtenido desde la base de datos:`, usuario);
      
      // Guardar en cache
      this.cache.set(id, usuario);
      
      return usuario;
      
    } catch (error) {
      console.error(`❌ Error al obtener usuario ${id}:`, error);
      throw error; // Propagar el error para manejo en las vistas
    }
  }

  async obtenerUsuariosPorIds(ids) {
    try {
      console.log('🔍 Obteniendo múltiples usuarios:', ids);
      const usuarios = [];
      
      for (const id of ids) {
        try {
          const usuario = await this.obtenerUsuario(id);
          if (usuario) {
            usuarios.push(usuario);
          } else {
            // Crear usuario básico si no se encuentra en la base de datos
            usuarios.push({
              id: id,
              nombre_completo: `Usuario ${id}`,
              correo: `usuario${id}@desconocido.com`,
              cargo: 'No disponible',
              supervisor: null,
              _notFound: true // Marcar como no encontrado
            });
          }
        } catch (error) {
          console.warn(`⚠️ No se pudo obtener usuario ${id}, agregando placeholder...`);
          usuarios.push({
            id: id,
            nombre_completo: `Usuario ${id}`,
            correo: `usuario${id}@desconocido.com`,
            cargo: 'Error al cargar',
            supervisor: null,
            _error: true // Marcar como error
          });
        }
      }
      
      return usuarios;
    } catch (error) {
      console.error('❌ Error al obtener múltiples usuarios:', error);
      return [];
    }
  }

  async enriquecerRegistrosConUsuarios(registros) {
    try {
      console.log('🔍 Enriqueciendo registros con datos reales de usuarios...');
      
      // Obtener IDs únicos de usuarios
      const idsUsuarios = [...new Set(registros.map(r => r.usuario_id))];
      
      // Obtener usuarios por IDs
      const usuarios = await this.obtenerUsuariosPorIds(idsUsuarios);
      
      // Crear mapa de usuarios por ID para búsqueda rápida
      const usuariosMap = new Map();
      usuarios.forEach(usuario => {
        usuariosMap.set(usuario.id, usuario);
      });
      
      // Enriquecer registros con datos de usuario
      const registrosEnriquecidos = registros.map(registro => ({
        ...registro,
        usuario: usuariosMap.get(registro.usuario_id) || {
          id: registro.usuario_id,
          nombre_completo: `Usuario ${registro.usuario_id}`,
          correo: 'No disponible',
          cargo: 'Desconocido',
          supervisor: null
        }
      }));
      
      console.log(`✅ ${registrosEnriquecidos.length} registros enriquecidos con datos de usuarios`);
      return registrosEnriquecidos;
      
    } catch (error) {
      console.error('❌ Error al enriquecer registros:', error);
      return registros; // Devolver registros sin enriquecer en caso de error
    }
  }

  // Función para mantener compatibilidad con código existente
  async obtenerUsuarioPorId(usuarioId) {
    return await this.obtenerUsuario(usuarioId);
  }

  // Función para mantener compatibilidad con código existente
  async obtenerTodosLosUsuarios() {
    return await this.obtenerUsuarios();
  }

  limpiarCache() {
    this.cache.clear();
    console.log('🗑️ Cache de usuarios limpiado');
  }

  async eliminarUsuario(id) {
    try {
      console.log(`🗑️ Eliminando usuario ${id} desde la API...`);
      const response = await fetch(`${API_BASE}/usuarios/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      if (!response.ok) {
        if (response.status === 404) {
          console.warn(`⚠️ Usuario ${id} no encontrado para eliminar`);
          throw new Error(`Usuario ${id} no encontrado`);
        }
        console.error(`❌ Error HTTP: ${response.status} - ${response.statusText}`);
        throw new Error(`Error HTTP: ${response.status}`);
      }
      
      // Eliminar del cache si existe
      this.cache.delete(id);
      
      console.log(`✅ Usuario ${id} eliminado exitosamente`);
      return true;
      
    } catch (error) {
      console.error(`❌ Error al eliminar usuario ${id}:`, error);
      throw error; // Propagar el error para manejo en las vistas
    }
  }
}

// Exportar una instancia única del servicio (singleton)
export const usuariosService = new UsuariosService();
export default usuariosService;
