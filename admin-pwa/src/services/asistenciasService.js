// Servicio para el manejo de asistencias
import axios from 'axios';
import { API_URL } from '../config/api.js';

class AsistenciasService {
  /**
   * Obtiene el historial completo de asistencias de todos los usuarios
   * @returns {Promise<Array>} Lista de asistencias con información de usuarios
   */
  async obtenerAsistencias() {
    let ultimoError = null;
    const maxReintentos = 3;
    
    for (let intento = 1; intento <= maxReintentos; intento++) {
      try {
        console.log(`🔍 Intento ${intento}/${maxReintentos} - Solicitando asistencias desde:`, `${API_URL}/asistencias`);
        
        const response = await fetch(`${API_URL}/asistencias`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          // Timeout de 10 segundos por intento
          signal: AbortSignal.timeout(10000)
        });

        if (!response.ok) {
          throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('✅ Asistencias obtenidas exitosamente:', data);
        
        return data.asistencias || [];
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
    
    console.error('❌ Todos los intentos fallaron:', ultimoError);
    throw ultimoError;
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

      // Enriquecer asistencias con información de usuario y URLs de fotos
      const asistenciasEnriquecidas = asistencias.map(asistencia => {
        const usuario = usuariosMap.get(asistencia.usuario_id);
        
        // Construir URLs completas para las fotos
        const fotoEntradaUrl = asistencia.foto_entrada_url 
          ? this.construirUrlFoto(asistencia.foto_entrada_url)
          : null;
        
        const fotoSalidaUrl = asistencia.foto_salida_url 
          ? this.construirUrlFoto(asistencia.foto_salida_url)
          : null;

        return {
          ...asistencia,
          nombre_usuario: usuario ? usuario.nombre_completo : 'Usuario no encontrado',
          correo_usuario: usuario ? usuario.correo : 'N/A',
          cargo_usuario: usuario ? usuario.cargo : 'N/A',
          foto_entrada_url: fotoEntradaUrl,
          foto_salida_url: fotoSalidaUrl
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
   * Construye la URL completa para una foto
   * @param {string} rutaFoto - Ruta relativa de la foto desde el backend
   * @returns {string} URL completa de la foto
   */
  construirUrlFoto(rutaFoto) {
    if (!rutaFoto) return null;
    
    // Si la ruta ya es una URL completa, devolverla tal como está
    if (rutaFoto.startsWith('http://') || rutaFoto.startsWith('https://')) {
      return rutaFoto;
    }
    
    // Limpiar la ruta: remover prefijos innecesarios y normalizar
    let rutaLimpia = rutaFoto;
    
    // Si la ruta comienza con 'fotos/', mantenerla
    // Si no, pero es solo el nombre del archivo, agregarle 'fotos/'
    if (!rutaLimpia.startsWith('fotos/')) {
      // Si es solo el nombre del archivo, agregamos el prefijo fotos/
      if (!rutaLimpia.includes('/')) {
        rutaLimpia = `fotos/${rutaLimpia}`;
      }
    }
    
    // Construir la URL completa
    const urlCompleta = `${API_URL}/${rutaLimpia}`;
    
    console.log('🖼️ URL de foto construida:', {
      original: rutaFoto,
      limpia: rutaLimpia,
      completa: urlCompleta
    });
    
    return urlCompleta;
  }

  /**
   * Formatea fecha para mostrar
   * @param {string} fecha - Fecha en formato ISO
   * @returns {string} Fecha formateada
   */
  formatearFecha(fecha) {
    if (!fecha) return 'N/A';
    try {
      // Si viene una fecha ISO completa (con T), la procesamos con zona horaria
      if (typeof fecha === 'string' && fecha.includes('T')) {
        return new Date(fecha).toLocaleDateString('es-ES', {
          timeZone: 'America/Mexico_City', // Forzar zona horaria de México
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        });
      }
      
      // Si viene solo una fecha (YYYY-MM-DD), crear la fecha sin zona horaria
      if (typeof fecha === 'string' && fecha.match(/^\d{4}-\d{2}-\d{2}$/)) {
        const [year, month, day] = fecha.split('-').map(num => parseInt(num, 10));
        const fechaObj = new Date(year, month - 1, day); // month - 1 porque los meses en JS van de 0-11
        
        return fechaObj.toLocaleDateString('es-ES', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        });
      }
      
      // Para otros casos, usar el método estándar
      return new Date(fecha).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      });
    } catch (error) {
      console.error('Error formateando fecha:', error, 'Fecha original:', fecha);
      return fecha;
    }
  }

  /**
   * Formatea hora para mostrar en formato 12 horas con AM/PM
   * @param {string} hora - Hora en formato ISO o datetime completo
   * @returns {string} Hora formateada en formato 12 horas
   */
  formatearHora(hora) {
    if (!hora) return 'N/A';
    try {
      let fechaObj;
      
      // Si viene un datetime completo (2025-07-16T12:25:22.626565)
      if (hora.includes('T')) {
        fechaObj = new Date(hora);
      } else {
        // Si viene solo la hora (12:25:22)
        fechaObj = new Date(`1970-01-01T${hora}`);
      }
      
      // Formatear en 12 horas con AM/PM - formato legible con espacio y minúsculas
      return fechaObj.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
      }).toLowerCase();
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

  /**
   * MÉTODOS DE ELIMINACIÓN MASIVA - ¡USO EXTREMO!
   */

  /**
   * Elimina TODAS las asistencias del sistema
   * @returns {Promise<Object>} Resultado de la eliminación
   */
  async eliminarTodasAsistencias() {
    try {
      console.log('🗑️ ELIMINACIÓN MASIVA: Eliminando todas las asistencias...');
      
      const response = await fetch(`${API_URL}/admin/asistencias/all`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        // Timeout de 30 segundos para operaciones masivas
        signal: AbortSignal.timeout(30000)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Error ${response.status}: ${response.statusText} - ${errorText}`);
      }

      const data = await response.json();
      console.log('✅ Asistencias eliminadas exitosamente:', data);
      
      return data;
    } catch (error) {
      if (error.name === 'TimeoutError') {
        console.error('❌ Timeout al eliminar asistencias - La operación está tomando demasiado tiempo');
        throw new Error('La eliminación está tomando demasiado tiempo. Intenta de nuevo en unos momentos.');
      }
      console.error('❌ Error al eliminar todas las asistencias:', error);
      throw error;
    }
  }

  /**
   * Elimina TODOS los registros del sistema
   * @returns {Promise<Object>} Resultado de la eliminación
   */
  async eliminarTodosRegistros() {
    try {
      console.log('🗑️ ELIMINACIÓN MASIVA: Eliminando todos los registros...');
      
      const response = await fetch(`${API_URL}/admin/registros/all`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        // Timeout de 30 segundos para operaciones masivas
        signal: AbortSignal.timeout(30000)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Error ${response.status}: ${response.statusText} - ${errorText}`);
      }

      const data = await response.json();
      console.log('✅ Registros eliminados exitosamente:', data);
      
      return data;
    } catch (error) {
      if (error.name === 'TimeoutError') {
        console.error('❌ Timeout al eliminar registros');
        throw new Error('La eliminación está tomando demasiado tiempo. Intenta de nuevo en unos momentos.');
      }
      console.error('❌ Error al eliminar todos los registros:', error);
      throw error;
    }
  }

  /**
   * Elimina TODOS los usuarios del sistema
   * @returns {Promise<Object>} Resultado de la eliminación
   */
  async eliminarTodosUsuarios() {
    try {
      console.log('🗑️ ELIMINACIÓN MASIVA: Eliminando todos los usuarios...');
      
      const response = await fetch(`${API_URL}/admin/usuarios/all`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        // Timeout de 30 segundos para operaciones masivas
        signal: AbortSignal.timeout(30000)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Error ${response.status}: ${response.statusText} - ${errorText}`);
      }

      const data = await response.json();
      console.log('✅ Usuarios eliminados exitosamente:', data);
      
      return data;
    } catch (error) {
      if (error.name === 'TimeoutError') {
        console.error('❌ Timeout al eliminar usuarios');
        throw new Error('La eliminación está tomando demasiado tiempo. Intenta de nuevo en unos momentos.');
      }
      console.error('❌ Error al eliminar todos los usuarios:', error);
      throw error;
    }
  }
}

export default new AsistenciasService();
