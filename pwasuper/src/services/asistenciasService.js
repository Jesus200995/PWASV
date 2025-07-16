// Servicio para el manejo de asistencias en la app PWA
import { API_URL } from '../utils/network.js';
import axios from 'axios';

/**
 * Servicio para gestionar asistencias
 */
class AsistenciasService {
  /**
   * Consulta la asistencia del día actual para un usuario específico
   * @param {number} usuarioId - ID del usuario a consultar
   * @returns {Promise<Object>} Objeto con datos de entrada y salida del día
   */
  async consultarAsistenciaHoy(usuarioId) {
    try {
      console.log('🔍 Consultando asistencia del día para usuario:', usuarioId);
      
      // Usar el endpoint de asistencias filtrado por usuario y fecha de hoy
      const today = new Date().toISOString().split('T')[0]; // Formato YYYY-MM-DD
      const response = await axios.get(`${API_URL}/asistencias?usuario_id=${usuarioId}&fecha=${today}`);
      
      console.log('✅ Datos de asistencia obtenidos:', response.data);
      
      // Adaptamos la respuesta al formato esperado
      const asistencias = response.data.asistencias || [];
      const asistenciaHoy = asistencias.length > 0 ? asistencias[0] : null;
      
      // Crear objeto con el formato esperado
      const resultado = {
        entrada: asistenciaHoy?.hora_entrada || null,
        salida: asistenciaHoy?.hora_salida || null,
        fecha: today
      };
      
      console.log('✅ Datos de asistencia hoy formateados:', resultado);
      return resultado;
    } catch (error) {
      console.error('❌ Error al consultar asistencia del día:', error);
      
      // Si es un error de conexión, proporcionamos un mensaje claro
      if (error.request && !error.response) {
        throw new Error('No se pudo conectar con el servidor. Verifica tu conexión a internet.');
      }
      
      // Si el backend responde con un error, lo propagamos
      if (error.response && error.response.data) {
        throw new Error(error.response.data.detail || 'Error al consultar asistencia');
      }
      
      // Para cualquier otro tipo de error
      throw error;
    }
  }

  /**
   * Registra la entrada de un usuario
   * @param {Object} datos - Datos de la entrada (usuario_id, latitud, longitud, etc.)
   * @returns {Promise<Object>} Respuesta del servidor
   */
  async registrarEntrada(datos) {
    try {
      console.log('📝 Registrando entrada para usuario:', datos.usuario_id);
      
      const response = await axios.post(`${API_URL}/asistencia/entrada`, datos, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        timeout: 15000,
        maxContentLength: Infinity,
        maxBodyLength: Infinity
      });
      
      console.log('✅ Entrada registrada:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Error al registrar entrada:', error);
      throw this._procesarError(error);
    }
  }

  /**
   * Registra la salida de un usuario
   * @param {Object} datos - Datos de la salida (usuario_id, latitud, longitud, etc.)
   * @returns {Promise<Object>} Respuesta del servidor
   */
  async registrarSalida(datos) {
    try {
      console.log('📝 Registrando salida para usuario:', datos.usuario_id);
      
      const response = await axios.post(`${API_URL}/asistencia/salida`, datos, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        timeout: 15000,
        maxContentLength: Infinity,
        maxBodyLength: Infinity
      });
      
      console.log('✅ Salida registrada:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Error al registrar salida:', error);
      throw this._procesarError(error);
    }
  }

  /**
   * Procesa errores para proporcionar mensajes claros
   * @private
   * @param {Error} error - Error capturado
   * @returns {Error} Error con mensaje apropiado
   */
  _procesarError(error) {
    // Si es un error de conexión
    if (error.request && !error.response) {
      return new Error('No se pudo conectar con el servidor. Verifica tu conexión a internet.');
    }
    
    // Si el backend responde con un error
    if (error.response && error.response.data) {
      return new Error(error.response.data.detail || 'Error en la operación');
    }
    
    // Para cualquier otro tipo de error
    return error;
  }
}

// Exportamos una instancia única del servicio
export default new AsistenciasService();
