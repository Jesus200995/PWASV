// Servicio para el manejo de asistencias
const API_URL = 'https://apipwa.sembrandodatos.com';

class AsistenciasService {
  /**
   * Obtiene el historial completo de asistencias de todos los usuarios
   * @returns {Promise<Array>} Lista de asistencias con información de usuarios
   */
  async obtenerAsistencias() {
    try {
      console.log('🔍 Solicitando asistencias desde:', `${API_URL}/asistencias`);
      
      const response = await fetch(`${API_URL}/asistencias`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('✅ Asistencias obtenidas:', data);
      
      return data.asistencias || [];
    } catch (error) {
      console.error('❌ Error al obtener asistencias:', error);
      throw error;
    }
  }

  /**
   * Obtiene asistencias de un usuario específico
   * @param {number} usuarioId - ID del usuario
   * @returns {Promise<Array>} Lista de asistencias del usuario
   */
  async obtenerAsistenciasPorUsuario(usuarioId) {
    try {
      console.log('🔍 Solicitando asistencias del usuario:', usuarioId);
      
      const response = await fetch(`${API_URL}/asistencias?usuario_id=${usuarioId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('✅ Asistencias del usuario obtenidas:', data);
      
      return data.asistencias || [];
    } catch (error) {
      console.error('❌ Error al obtener asistencias del usuario:', error);
      throw error;
    }
  }

  /**
   * Obtiene todos los usuarios para mapear información
   * @returns {Promise<Array>} Lista de usuarios
   */
  async obtenerUsuarios() {
    try {
      console.log('🔍 Solicitando usuarios desde:', `${API_URL}/usuarios`);
      
      const response = await fetch(`${API_URL}/usuarios`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('✅ Usuarios obtenidos para mapeo:', data);
      
      return data.usuarios || [];
    } catch (error) {
      console.error('❌ Error al obtener usuarios:', error);
      throw error;
    }
  }

  /**
   * Combina asistencias con información de usuarios
   * @returns {Promise<Array>} Lista de asistencias enriquecidas con datos de usuario
   */
  async obtenerAsistenciasConUsuarios() {
    try {
      const [asistencias, usuarios] = await Promise.all([
        this.obtenerAsistencias(),
        this.obtenerUsuarios()
      ]);

      // Crear un mapa de usuarios para búsqueda rápida
      const usuariosMap = new Map();
      usuarios.forEach(usuario => {
        usuariosMap.set(usuario.id, usuario);
      });

      // Enriquecer asistencias con información de usuario
      const asistenciasEnriquecidas = asistencias.map(asistencia => {
        const usuario = usuariosMap.get(asistencia.usuario_id);
        return {
          ...asistencia,
          nombre_usuario: usuario ? usuario.nombre_completo : 'Usuario no encontrado',
          correo_usuario: usuario ? usuario.correo : 'N/A',
          cargo_usuario: usuario ? usuario.cargo : 'N/A'
        };
      });

      console.log('✅ Asistencias enriquecidas procesadas:', asistenciasEnriquecidas.length);
      return asistenciasEnriquecidas;
    } catch (error) {
      console.error('❌ Error al obtener asistencias con usuarios:', error);
      throw error;
    }
  }

  /**
   * Formatea fecha para mostrar
   * @param {string} fecha - Fecha en formato ISO
   * @returns {string} Fecha formateada
   */
  formatearFecha(fecha) {
    if (!fecha) return 'N/A';
    try {
      return new Date(fecha).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      });
    } catch (error) {
      return fecha;
    }
  }

  /**
   * Formatea hora para mostrar
   * @param {string} hora - Hora en formato ISO o datetime completo
   * @returns {string} Hora formateada
   */
  formatearHora(hora) {
    if (!hora) return 'N/A';
    try {
      // Si viene un datetime completo (2025-07-16T12:25:22.626565)
      if (hora.includes('T')) {
        return new Date(hora).toLocaleTimeString('es-ES', {
          hour: '2-digit',
          minute: '2-digit'
        });
      }
      // Si viene solo la hora (12:25:22)
      return new Date(`1970-01-01T${hora}`).toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch (error) {
      console.error('Error formateando hora:', error, 'Hora original:', hora);
      return hora;
    }
  }

  /**
   * Formatea coordenadas para mostrar
   * @param {number} latitud - Latitud
   * @param {number} longitud - Longitud
   * @returns {string} Coordenadas formateadas
   */
  formatearCoordenadas(latitud, longitud) {
    if (!latitud || !longitud) return 'N/A';
    return `${latitud.toFixed(6)}, ${longitud.toFixed(6)}`;
  }
}

export default new AsistenciasService();
