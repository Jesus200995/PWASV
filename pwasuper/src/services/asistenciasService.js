// Servicio para el manejo de asistencias en la app PWA
import { API_URL } from '../utils/network.js';
import { checkInternetConnection } from '../utils/network.js';
import axios from 'axios';

/**
 * Servicio para gestionar asistencias con soporte offline
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
      
      // Usar el endpoint de asistencias filtrado por usuario y fecha de hoy exactamente
      const response = await axios.get(`${API_URL}/asistencias?usuario_id=${usuarioId}&fecha=${today}`, {
        // Añadir timeout y manejo de cache para asegurar respuestas actualizadas
        timeout: 10000,
        headers: {
          'Cache-Control': 'no-cache',
          'Pragma': 'no-cache'
        }
      });
      
      console.log('✅ Datos de asistencia obtenidos:', response.data);
      
      // Adaptamos la respuesta al formato esperado
      const asistencias = response.data.asistencias || [];
      
      // Filtramos solo las asistencias de hoy para mayor seguridad
      const asistenciasHoy = asistencias.filter(a => {
        // Convertir fecha de la asistencia a YYYY-MM-DD para comparar
        const fechaAsistencia = a.fecha ? new Date(a.fecha).toISOString().split('T')[0] : null;
        return fechaAsistencia === today;
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
   * Registra la entrada de un usuario con soporte offline
   * @param {Object} datos - Datos de la entrada (usuario_id, latitud, longitud, etc.)
   * @param {Object} options - Opciones adicionales { offlineCallback, usuarioId }
   * @returns {Promise<Object>} Respuesta del servidor o confirmación offline
   */
  async registrarEntrada(datos, options = {}) {
    try {
      // Verificar conectividad antes de intentar el registro
      const isConnected = await checkInternetConnection();
      
      if (!isConnected) {
        // Si no hay conexión y se proporciona callback offline, usarlo
        if (options.offlineCallback && options.usuarioId) {
          console.log('� Sin conexión - guardando entrada offline');
          return await options.offlineCallback(datos, options.usuarioId);
        } else {
          throw new Error('Sin conexión a internet. La entrada no se pudo registrar.');
        }
      }

      console.log('�📝 Registrando entrada para usuario:', datos.get ? datos.get('usuario_id') : datos.usuario_id);
      
      // Agregar la fecha actual a la solicitud
      const formData = new FormData();
      // Copiar todos los campos del FormData original
      if (datos instanceof FormData) {
        // Si es un FormData, iteramos sus entradas
        for (const [key, value] of datos.entries()) {
          formData.append(key, value);
        }
      } else {
        // Si es un objeto normal
        for (const [key, value] of Object.entries(datos)) {
          formData.append(key, value);
        }
      }
      
      // Añadir fecha actual si no está presente (en formato YYYY-MM-DD)
      if (!formData.has('fecha')) {
        const today = new Date().toISOString().split('T')[0];
        formData.append('fecha', today);
      }
      
      const response = await axios.post(`${API_URL}/asistencia/entrada`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        timeout: 15000,
        maxContentLength: Infinity,
        maxBodyLength: Infinity
      });
      
      console.log('✅ Entrada registrada:', response.data);
      return {
        success: true,
        data: response.data,
        message: 'Entrada registrada correctamente'
      };
    } catch (error) {
      console.error('❌ Error al registrar entrada:', error);
      
      // Si es un error de conectividad y tenemos callback offline, intentar offline
      if (this._isConnectionError(error) && options.offlineCallback && options.usuarioId) {
        console.log('📵 Error de conexión - guardando entrada offline');
        return await options.offlineCallback(datos, options.usuarioId);
      }
      
      throw this._procesarError(error);
    }
  }

  /**
   * Registra la salida de un usuario con soporte offline
   * @param {Object} datos - Datos de la salida (usuario_id, latitud, longitud, etc.)
   * @param {Object} options - Opciones adicionales { offlineCallback, usuarioId }
   * @returns {Promise<Object>} Respuesta del servidor o confirmación offline
   */
  async registrarSalida(datos, options = {}) {
    try {
      // Verificar conectividad antes de intentar el registro
      const isConnected = await checkInternetConnection();
      
      if (!isConnected) {
        // Si no hay conexión y se proporciona callback offline, usarlo
        if (options.offlineCallback && options.usuarioId) {
          console.log('� Sin conexión - guardando salida offline');
          return await options.offlineCallback(datos, options.usuarioId);
        } else {
          throw new Error('Sin conexión a internet. La salida no se pudo registrar.');
        }
      }

      console.log('�📝 Registrando salida para usuario:', datos.get ? datos.get('usuario_id') : datos.usuario_id);
      
      // Agregar la fecha actual a la solicitud
      const formData = new FormData();
      // Copiar todos los campos del FormData original
      if (datos instanceof FormData) {
        // Si es un FormData, iteramos sus entradas
        for (const [key, value] of datos.entries()) {
          formData.append(key, value);
        }
      } else {
        // Si es un objeto normal
        for (const [key, value] of Object.entries(datos)) {
          formData.append(key, value);
        }
      }
      
      // Añadir fecha actual si no está presente (en formato YYYY-MM-DD)
      if (!formData.has('fecha')) {
        const today = new Date().toISOString().split('T')[0];
        formData.append('fecha', today);
      }
      
      const response = await axios.post(`${API_URL}/asistencia/salida`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        timeout: 15000,
        maxContentLength: Infinity,
        maxBodyLength: Infinity
      });
      
      console.log('✅ Salida registrada:', response.data);
      return {
        success: true,
        data: response.data,
        message: 'Salida registrada correctamente'
      };
    } catch (error) {
      console.error('❌ Error al registrar salida:', error);
      
      // Si es un error de conectividad y tenemos callback offline, intentar offline
      if (this._isConnectionError(error) && options.offlineCallback && options.usuarioId) {
        console.log('📵 Error de conexión - guardando salida offline');
        return await options.offlineCallback(datos, options.usuarioId);
      }
      
      throw this._procesarError(error);
    }
  }

  /**
   * Verifica si un error es de conectividad
   * @private
   * @param {Error} error - Error a verificar
   * @returns {boolean} True si es error de conectividad
   */
  _isConnectionError(error) {
    return error.code === 'ECONNABORTED' || 
           error.code === 'NETWORK_ERROR' || 
           error.code === 'ERR_NETWORK' ||
           (error.request && !error.response) ||
           error.message.includes('Network Error') ||
           error.message.includes('timeout');
  }

  /**
   * Procesa errores para proporcionar mensajes claros
   * @private
   * @param {Error} error - Error capturado
   * @returns {Error} Error con mensaje apropiado
   */
  _procesarError(error) {
    // Si es un error de conexión
    if (this._isConnectionError(error)) {
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
