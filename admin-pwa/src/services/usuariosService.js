// Servicio para manejo de usuarios usando la API real con endpoints GET
import { API_URL } from '../config/api.js'

console.log(`🌐 Usando API: ${API_URL}`);

class UsuariosService {
  constructor() {
    this.cache = new Map(); // Cache para mejorar performance
  }

  async obtenerUsuarios() {
    let ultimoError = null;
    const maxReintentos = 3;
    
    for (let intento = 1; intento <= maxReintentos; intento++) {
      try {
        console.log(`🔍 Intento ${intento}/${maxReintentos} - Obteniendo usuarios desde la API real...`);
        
        const response = await fetch(`${API_URL}/usuarios`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          // Timeout de 10 segundos por intento
          signal: AbortSignal.timeout(10000)
        });
        
        if (!response.ok) {
          console.error(`❌ Error HTTP: ${response.status} - ${response.statusText}`);
          throw new Error(`Error HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('✅ Respuesta de la API obtenida exitosamente:', data);
        
        // El endpoint devuelve {usuarios: []} según la implementación del backend
        let usuarios = [];
        if (data.usuarios && Array.isArray(data.usuarios)) {
          usuarios = data.usuarios;
        } else if (Array.isArray(data)) {
          usuarios = data;
        }
        
        // Debug: verificar contraseñas en los datos recibidos
        console.log('🔍 Verificando contraseñas en usuarios recibidos:');
        usuarios.forEach((usuario, index) => {
          console.log(`Usuario ${index + 1}:`, {
            id: usuario.id,
            nombre: usuario.nombre_completo,
            contraseña: usuario.contrasena || 'NO FOUND',
            propiedades: Object.keys(usuario)
          });
        });
        
        // Actualizar cache con los usuarios obtenidos
        usuarios.forEach(usuario => {
          this.cache.set(usuario.id, usuario);
        });
        
        console.log(`✅ ${usuarios.length} usuarios obtenidos desde la base de datos`);
        return usuarios;
        
      } catch (error) {
        ultimoError = error;
        console.error(`❌ Error en intento ${intento}/${maxReintentos}:`, error.message);
        
        if (intento < maxReintentos) {
          const tiempoEspera = Math.min(1000 * Math.pow(2, intento), 5000); // Backoff exponencial
          console.log(`⏳ Esperando ${tiempoEspera}ms antes del siguiente intento...`);
          await new Promise(resolve => setTimeout(resolve, tiempoEspera));
        }
      }
    }
    
    console.error('❌ Todos los intentos fallaron al obtener usuarios:', ultimoError);
    throw ultimoError; // Propagar el último error para manejo en las vistas
  }

  async obtenerUsuario(id) {
    try {
      // Verificar cache primero
      if (this.cache.has(id)) {
        console.log(`📋 Usuario ${id} encontrado en cache`);
        return this.cache.get(id);
      }

      console.log(`🔍 Obteniendo usuario ${id} desde la API real...`);
      const response = await fetch(`${API_URL}/usuarios/${id}`, {
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

  async actualizarUsuario(id, datosUsuario) {
    try {
      console.log(`✏️ Actualizando usuario ${id} en la API...`, datosUsuario);
      const response = await fetch(`${API_URL}/usuarios/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(datosUsuario)
      });
      
      if (!response.ok) {
        if (response.status === 404) {
          console.warn(`⚠️ Usuario ${id} no encontrado para actualizar`);
          throw new Error(`Usuario ${id} no encontrado`);
        }
        if (response.status === 400) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Datos inválidos');
        }
        console.error(`❌ Error HTTP: ${response.status} - ${response.statusText}`);
        throw new Error(`Error HTTP: ${response.status}`);
      }
      
      const resultado = await response.json();
      console.log(`✅ Usuario ${id} actualizado exitosamente:`, resultado);
      
      // Actualizar cache con el usuario actualizado
      if (resultado.usuario) {
        this.cache.set(id, resultado.usuario);
      }
      
      return resultado;
      
    } catch (error) {
      console.error(`❌ Error al actualizar usuario ${id}:`, error);
      throw error; // Propagar el error para manejo en las vistas
    }
  }

  async buscarUsuarios(termino) {
    try {
      if (!termino || termino.trim().length < 2) {
        console.log('🚫 Término muy corto, no se realizará búsqueda:', termino);
        return []; // No buscar con menos de 2 caracteres
      }

      console.log(`🔍 Buscando usuarios con término: "${termino}"`);
      
      // Obtener todos los usuarios desde la API
      console.log('📡 Obteniendo todos los usuarios desde la API...');
      const todosLosUsuarios = await this.obtenerUsuarios();
      console.log('📊 Total de usuarios obtenidos:', todosLosUsuarios.length);
      
      if (todosLosUsuarios.length === 0) {
        console.log('⚠️ No hay usuarios disponibles para filtrar');
        return [];
      }
      
      // Filtrar usuarios localmente
      const terminoLower = termino.toLowerCase().trim();
      console.log('🔎 Filtrando usuarios con término:', terminoLower);
      
      const usuariosFiltrados = todosLosUsuarios.filter(usuario => {
        const nombreCompleto = (usuario.nombre_completo || '').toLowerCase();
        const correo = (usuario.correo || '').toLowerCase();
        const curp = (usuario.curp || '').toLowerCase();
        const cargo = (usuario.cargo || '').toLowerCase();
        
        const coincide = nombreCompleto.includes(terminoLower) || 
                        correo.includes(terminoLower) || 
                        curp.includes(terminoLower) ||
                        cargo.includes(terminoLower);
                        
        if (coincide) {
          console.log('✅ Usuario coincidente:', {
            id: usuario.id,
            nombre: nombreCompleto,
            correo: correo,
            curp: curp
          });
        }
        
        return coincide;
      });

      console.log(`✅ Encontrados ${usuariosFiltrados.length} usuarios que coinciden con "${termino}"`);
      
      // Limitar resultados a 10 para mejor rendimiento
      const resultadosLimitados = usuariosFiltrados.slice(0, 10);
      console.log(`📋 Devolviendo ${resultadosLimitados.length} usuarios (limitado a 10)`);
      
      return resultadosLimitados;
      
    } catch (error) {
      console.error(`❌ Error al buscar usuarios con término "${termino}":`, error);
      return []; // Devolver array vacío en caso de error
    }
  }

  async eliminarUsuario(id) {
    try {
      console.log(`🗑️ Eliminando usuario ${id} desde la API...`);
      const response = await fetch(`${API_URL}/usuarios/${id}`, {
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
