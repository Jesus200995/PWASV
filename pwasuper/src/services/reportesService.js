import { API_URL } from '../utils/network.js';
import axios from 'axios';

/**
 * Servicio para la gestión de reportes
 */
class ReportesService {
  /**
   * Obtiene las actividades del mes actual para un usuario
   * @param {number} usuarioId - ID del usuario
   * @returns {Promise<Array>} Lista de actividades del mes
   */
  async obtenerActividadesMes(usuarioId) {
    try {
      console.log('📊 Obteniendo actividades del mes para usuario:', usuarioId);
      
      // Obtener fecha actual y calcular inicio del mes
      const hoy = new Date();
      const inicioDeMes = new Date(hoy.getFullYear(), hoy.getMonth(), 1);
      
      const fechaInicio = inicioDeMes.toISOString().split('T')[0];
      const fechaFin = hoy.toISOString().split('T')[0];
      
      console.log(`📅 Rango de fechas: ${fechaInicio} a ${fechaFin}`);
      
      const response = await axios.get(`${API_URL}/historial/${usuarioId}`, {
        params: {
          fecha_inicio: fechaInicio,
          fecha_fin: fechaFin,
          limit: 1000
        },
        timeout: 10000
      });
      
      console.log('✅ Actividades del mes obtenidas:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Error obteniendo actividades del mes:', error);
      throw this._procesarError(error);
    }
  }

  /**
   * Obtiene actividades de un mes y año específicos
   * @param {number} usuarioId - ID del usuario
   * @param {number} mes - Mes (0-11)
   * @param {number} anio - Año
   * @returns {Promise<Array>} Lista de actividades del mes especificado
   */
  async obtenerActividadesMesEspecifico(usuarioId, mes, anio) {
    try {
      console.log(`📊 Obteniendo actividades de ${mes + 1}/${anio} para usuario ${usuarioId}`);
      
      const inicioDeMes = new Date(anio, mes, 1);
      const finDelMes = new Date(anio, mes + 1, 0);
      
      const fechaInicio = inicioDeMes.toISOString().split('T')[0];
      const fechaFin = finDelMes.toISOString().split('T')[0];
      
      console.log(`📅 Rango calculado: ${fechaInicio} a ${fechaFin}`);
      console.log(`🔗 URL: ${API_URL}/historial/${usuarioId}`);
      console.log(`📋 Parámetros:`, { fecha_inicio: fechaInicio, fecha_fin: fechaFin, limit: 1000 });
      
      const response = await axios.get(`${API_URL}/historial/${usuarioId}`, {
        params: {
          fecha_inicio: fechaInicio,
          fecha_fin: fechaFin,
          limit: 1000
        },
        timeout: 10000
      });
      
      console.log(`✅ Respuesta del servidor:`, response.data);
      console.log(`📊 Total de actividades obtenidas: ${response.data.historial?.length || 0}`);
      
      return response.data;
    } catch (error) {
      console.error('❌ Error obteniendo actividades:', error.message);
      console.error('📋 Detalles del error:', error.response?.data || error);
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
    if (error.request && !error.response) {
      return new Error('No se pudo conectar con el servidor. Verifica tu conexión a internet.');
    }
    
    if (error.response && error.response.data) {
      return new Error(error.response.data.detail || 'Error en la operación');
    }
    
    return error;
  }
}

export default new ReportesService();
