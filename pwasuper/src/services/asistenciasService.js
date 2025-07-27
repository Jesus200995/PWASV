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
      
      // Obtener la fecha actual en formato YYYY-MM-DD
      const now = new Date();
      const today = now.toISOString().split('T')[0]; // Formato YYYY-MM-DD
      
      console.log(`🔍 Consultando asistencias para la fecha: ${today}`);
      
      // Usar timestamp para evitar cache del navegador
      const timestamp = new Date().getTime();
      const cacheBuster = `_t=${timestamp}`;
      
      // Usar el endpoint de asistencias filtrado por usuario y fecha de hoy exactamente
      const response = await axios.get(`${API_URL}/asistencias?usuario_id=${usuarioId}&fecha=${today}&${cacheBuster}`, {
        // Añadir timeout y manejo de cache para asegurar respuestas actualizadas
        timeout: 10000,
        headers: {
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Pragma': 'no-cache',
          'Expires': '0'
        }
      });
      
      console.log('✅ Datos de asistencia obtenidos:', response.data);
      
      // Adaptamos la respuesta al formato esperado
      const asistencias = response.data.asistencias || [];
      
      // Filtramos solo las asistencias de hoy para mayor seguridad
      const asistenciasHoy = asistencias.filter(a => {
        // Convertir fecha de la asistencia a YYYY-MM-DD para comparar
        const fechaAsistencia = a.fecha ? new Date(a.fecha).toISOString().split('T')[0] : null;
        const matches = fechaAsistencia === today;
        console.log(`🔍 Comparando fechas: ${fechaAsistencia} === ${today} ? ${matches}`);
        return matches;
      });
      
      console.log(`🔍 Asistencias filtradas para hoy (${today}):`, asistenciasHoy);
      
      const asistenciaHoy = asistenciasHoy.length > 0 ? asistenciasHoy[0] : null;
      
      // Crear objeto con el formato esperado asegurando que corresponda al día de hoy
      const resultado = {
        entrada: asistenciaHoy?.hora_entrada || null,
        salida: asistenciaHoy?.hora_salida || null,
        fecha: today,
        descripcion_entrada: asistenciaHoy?.descripcion_entrada || null,
        descripcion_salida: asistenciaHoy?.descripcion_salida || null,
        latitud_entrada: asistenciaHoy?.latitud_entrada || null,
        longitud_entrada: asistenciaHoy?.longitud_entrada || null,
        latitud_salida: asistenciaHoy?.latitud_salida || null,
        longitud_salida: asistenciaHoy?.longitud_salida || null,
        foto_entrada_url: asistenciaHoy?.foto_entrada_url || null,
        foto_salida_url: asistenciaHoy?.foto_salida_url || null
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
   * @param {FormData} formData - FormData con los datos de la entrada
   * @returns {Promise<Object>} Respuesta del servidor
   */
  async registrarEntrada(formData) {
    try {
      console.log('📝 Registrando entrada...');
      
      const response = await axios.post(`${API_URL}/asistencia/entrada`, formData, {
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
   * @param {FormData} formData - FormData con los datos de la salida
   * @returns {Promise<Object>} Respuesta del servidor
   */
  async registrarSalida(formData) {
    try {
      console.log('📝 Registrando salida...');
      
      const response = await axios.post(`${API_URL}/asistencia/salida`, formData, {
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
