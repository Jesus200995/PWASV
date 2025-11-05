/**
 * Servicio de sincronización para enviar datos offline cuando se recupera la conexión
 */
import offlineService from './offlineService.js';
import asistenciasService from './asistenciasService.js';
import { API_URL, checkInternetConnection } from '../utils/network.js';
import axios from 'axios';

class SyncService {
  constructor() {
    this.isOnline = navigator.onLine;
    this.isSyncing = false;
    this.listeners = [];
    this.setupEventListeners();
  }

  /**
   * Configura los listeners para detectar cambios de conectividad
   */
  setupEventListeners() {
    // Listener para cuando se recupera la conexión
    window.addEventListener('online', async () => {
      console.log('🌐 Conexión recuperada, iniciando sincronización...');
      this.isOnline = true;
      
      // Primero notificar a los componentes que estamos online
      this.notifyListeners('online');
      
      // Verificar que realmente tengamos conexión real con el backend
      const reallyConnected = await checkInternetConnection();
      
      if (reallyConnected) {
        console.log('✅ Conexión con backend confirmada, iniciaremos sincronización en breve...');
        
        // Esperar un poco más para asegurar que la conexión es estable
        setTimeout(async () => {
          try {
            // Verificar si hay elementos pendientes antes de sincronizar
            const pendientes = await offlineService.contarPendientes(true);
            if (pendientes.total > 0) {
              console.log(`🔄 Iniciando sincronización automática de ${pendientes.total} elementos pendientes (${pendientes.registros} registros, ${pendientes.asistencias} asistencias)`);
              
              // Notificar que empieza sincronización
              this.notifyListeners('syncing', true, pendientes);
              
              // Ejecutar sincronización completa
              await this.sincronizarTodo();
            } else {
              console.log('✅ No hay elementos pendientes para sincronizar');
            }
          } catch (error) {
            console.error('❌ Error durante sincronización automática:', error);
          }
        }, 3000); // Aumentar tiempo de espera para mayor estabilidad
      } else {
        console.log('⚠️ Conexión detectada pero no hay respuesta del backend, esperando...');
        // Programar un nuevo intento en 30 segundos
        setTimeout(async () => {
          if (this.isOnline) {
            console.log('🔄 Reintentando sincronización después de espera...');
            await this.sincronizarTodo();
          }
        }, 30000);
      }
    });

    // Listener para cuando se pierde la conexión
    window.addEventListener('offline', () => {
      console.log('📴 Conexión perdida');
      this.isOnline = false;
      this.notifyListeners('offline');
    });

    // Verificar conexión inicial y establecer polling periódico
    this.verificarConexionInicial();
    
    // Establecer verificación periódica de conexión y sincronización
    // Cada 5 minutos verificamos si hay conexión y pendientes para sincronizar
    setInterval(async () => {
      if (this.isOnline && !this.isSyncing) {
        try {
          const pendientes = await offlineService.contarPendientes(true);
          if (pendientes.total > 0) {
            console.log(`🔄 Verificación periódica: ${pendientes.total} elementos pendientes, intentando sincronizar...`);
            await this.sincronizarTodo();
          }
        } catch (error) {
          console.error('❌ Error en verificación periódica:', error);
        }
      }
    }, 5 * 60 * 1000); // 5 minutos
  }

  /**
   * Verifica la conexión inicial al cargar la aplicación
   */
  async verificarConexionInicial() {
    try {
      this.isOnline = await checkInternetConnection();
      this.notifyListeners(this.isOnline ? 'online' : 'offline');
      
      // Si estamos online al iniciar, sincronizar datos pendientes
      if (this.isOnline) {
        setTimeout(async () => {
          await this.sincronizarTodo();
        }, 3000);
      }
    } catch (error) {
      console.error('Error verificando conexión inicial:', error);
      this.isOnline = false;
      this.notifyListeners('offline');
    }
  }

  /**
   * Registra un listener para cambios de conectividad
   */
  addListener(callback) {
    this.listeners.push(callback);
  }

  /**
   * Remueve un listener
   */
  removeListener(callback) {
    this.listeners = this.listeners.filter(listener => listener !== callback);
  }

  /**
   * Notifica a todos los listeners sobre cambios de estado
   * @param {string} status - Estado de sincronización ('online', 'offline', 'syncing', 'sync_complete', etc)
   * @param {boolean} isOnline - Si el dispositivo está online
   * @param {Object} data - Datos adicionales para el evento
   */
  notifyListeners(status, isOnline = this.isOnline, data = null) {
    this.listeners.forEach(callback => {
      try {
        callback(status, isOnline, data);
      } catch (error) {
        console.error('Error en listener de conectividad:', error);
      }
    });
  }

  /**
   * Sincroniza todos los datos pendientes (registros + asistencias)
   */
  async sincronizarTodo() {
    if (this.isSyncing) {
      console.log('⏳ Sincronización ya en progreso...');
      return { mensaje: 'Sincronización ya en progreso', estado: 'en_progreso' };
    }

    this.isSyncing = true;
    
    try {
      console.log('🔄 Iniciando sincronización completa...');
      
      // Verificar que realmente tengamos conexión con timeout corto
      const reallyOnline = await checkInternetConnection(5000); // 5 segundos máximo
      if (!reallyOnline) {
        console.log('❌ Verificación de conexión falló, cancelando sincronización');
        this.isOnline = false;
        this.notifyListeners('offline');
        this.isSyncing = false; // Asegurar que se resetea la bandera
        return { mensaje: 'Sin conexión a Internet', estado: 'error' };
      }

      // MEJORA: Forzar actualización de datos pendientes (sin usar caché)
      const pendientes = await offlineService.contarPendientes(true);
      
      // MEJORA: Obtener datos pendientes con opción de logging detallado
      const registrosPendientes = await offlineService.obtenerRegistrosPendientes(true);
      const asistenciasPendientes = await offlineService.obtenerAsistenciasPendientes();
      
      const totalPendientes = registrosPendientes.length + asistenciasPendientes.length;
      
      // Validar que realmente haya pendientes (doble verificación)
      if (totalPendientes === 0) {
        console.log('✅ No hay datos pendientes para sincronizar');
        // Notificar igualmente para actualizar interfaces
        this.notifyListeners('sync_complete', true, { exitosos: 0, fallidos: 0, total: 0 });
        this.isSyncing = false;
        return { mensaje: 'No hay datos pendientes', estado: 'completado' };
      }
      
      console.log(`📊 Sincronizando ${totalPendientes} elementos (${registrosPendientes.length} registros, ${asistenciasPendientes.length} asistencias)`);
      
      // Notificar inicio de sincronización con detalles
      this.notifyListeners('syncing', true, {
        registros: registrosPendientes.length,
        asistencias: asistenciasPendientes.length,
        total: totalPendientes
      });
      
      let exitosos = 0;
      let fallidos = 0;
      
      // MEJORA: Sincronizar registros generales con mejor gestión de errores
      console.log(`🔄 Iniciando sincronización de ${registrosPendientes.length} REGISTROS DE ACTIVIDADES:`);
      
      for (const registro of registrosPendientes) {
        try {
          console.log(`🔄 Procesando registro ID: ${registro.id}, timestamp: ${registro.timestamp}, tipo: ${registro.tipo || 'actividad'}`);
          
          // MEJORA: Verificar datos críticos antes de intentar enviar
          if (!registro.usuario_id || !registro.latitud || !registro.longitud) {
            console.error(`❌ Registro ${registro.id} incompleto, faltan datos básicos`);
            throw new Error('Datos de registro incompletos');
          }
          
          // MEJORA: Verificar que realmente esté marcado como actividad
          if (!registro.tipo) {
            console.log(`⚠️ Registro ${registro.id} no tiene tipo especificado, asumiendo 'actividad'`);
            registro.tipo = 'actividad';
          }
          
          // Intentar enviar el registro
          console.log(`📤 Enviando registro ${registro.id} al servidor...`);
          await this.enviarRegistro(registro);
          
          // Si llega aquí, el envío fue exitoso, eliminar de pendientes
          console.log(`✅ Registro ${registro.id} enviado exitosamente, eliminando de pendientes`);
          await offlineService.eliminarRegistro(registro.id);
          exitosos++;
          
          // Notificar progreso
          this.notifyListeners('sync_progress', true, {
            procesados: exitosos + fallidos,
            total: totalPendientes,
            exitosos,
            fallidos,
            tipo: 'registro'
          });
          
        } catch (error) {
          console.error(`❌ Error enviando registro ${registro.id}:`, error);
          
          // MEJORA: Mejor manejo de duplicados y otros errores del servidor
          // Si el error indica que el registro ya existe, lo consideramos exitoso
          if (error.response && error.response.status === 400 && 
              error.response.data && error.response.data.detail && 
              (error.response.data.detail.includes('ya existe') || 
               error.response.data.detail.includes('duplicado') ||
               error.response.data.detail.includes('Ya registrado'))) {
            
            console.log(`ℹ️ El registro ${registro.id} ya existe en el servidor, marcando como sincronizado`);
            await offlineService.eliminarRegistro(registro.id);
            exitosos++;
          } else {
            // Incrementar contador de fallidos
            fallidos++;
            
            // MEJORA: Actualizar el registro con información más detallada del error
            try {
              await offlineService.actualizarEstadoSincronizacion(
                registro.id, 
                'registro',
                {
                  ultimo_error: error.message || 'Error desconocido',
                  intentos: (registro.intentos || 0) + 1,
                  ultima_sincronizacion: new Date().toISOString(),
                  detalles_error: error.response ? 
                    `Status: ${error.response.status}, Detail: ${JSON.stringify(error.response.data || {})}` : 
                    'Sin respuesta del servidor'
                }
              );
            } catch (err) {
              console.error('Error actualizando estado de sincronización:', err);
            }
          }
          
          // Notificar progreso incluso con error
          this.notifyListeners('sync_progress', true, {
            procesados: exitosos + fallidos,
            total: totalPendientes,
            exitosos,
            fallidos,
            tipo: 'registro'
          });
        }
      }
      
      // MEJORA: Sincronizar asistencias con mejor gestión de errores
      for (const asistencia of asistenciasPendientes) {
        try {
          console.log(`🔄 Procesando asistencia ID: ${asistencia.id}, tipo: ${asistencia.tipo}, timestamp: ${asistencia.timestamp}`);
          
          // Intentar enviar la asistencia
          await this.enviarAsistencia(asistencia);
          
          // Si llega aquí, el envío fue exitoso, eliminar de pendientes
          await offlineService.eliminarAsistencia(asistencia.id);
          exitosos++;
          
          // Notificar progreso
          this.notifyListeners('sync_progress', true, {
            procesados: exitosos + fallidos,
            total: totalPendientes,
            exitosos,
            fallidos,
            tipo: 'asistencia'
          });
          
        } catch (error) {
          console.error(`❌ Error enviando asistencia ${asistencia.id} (${asistencia.tipo}):`, error);
          
          // Si el error indica que la asistencia ya existe, la consideramos exitosa
          if (error.response && error.response.status === 400 && 
              error.response.data && error.response.data.detail && 
              (error.response.data.detail.includes('Ya existe') || 
               error.response.data.detail.includes('ya registrada'))) {
            
            console.log(`ℹ️ La asistencia ${asistencia.id} (${asistencia.tipo}) ya existe en el servidor, marcando como sincronizada`);
            await offlineService.eliminarAsistencia(asistencia.id);
            exitosos++;
          } else {
            // Incrementar contador de fallidos
            fallidos++;
            
            // Actualizar la asistencia con información del error para retentarlo después
            try {
              await offlineService.actualizarEstadoSincronizacion(
                asistencia.id, 
                'asistencia',
                {
                  ultimo_error: error.message || 'Error desconocido',
                  intentos: (asistencia.intentos || 0) + 1,
                  ultima_sincronizacion: new Date().toISOString()
                }
              );
            } catch (err) {
              console.error('Error actualizando estado de sincronización:', err);
            }
          }
          
          // Notificar progreso incluso con error
          this.notifyListeners('sync_progress', true, {
            procesados: exitosos + fallidos,
            total: totalPendientes,
            exitosos,
            fallidos,
            tipo: 'asistencia'
          });
        }
      }
      
      // Notificar resultado final
      const resultado = { exitosos, fallidos, total: totalPendientes };
      console.log(`✅ Sincronización completada: ${exitosos} exitosos, ${fallidos} fallidos de ${totalPendientes} totales`);
      this.notifyListeners('sync_complete', true, resultado);
      
      // Retornar información detallada
      return {
        mensaje: `Sincronización completada: ${exitosos} exitosos, ${fallidos} fallidos`,
        estado: 'completado',
        ...resultado
      };
      
    } catch (error) {
      console.error('❌ Error durante la sincronización:', error);
      this.notifyListeners('sync_error', true, error);
      return { mensaje: `Error en sincronización: ${error.message || 'Error desconocido'}`, estado: 'error' };
    } finally {
      this.isSyncing = false;
    }
  }

  /**
   * Envía un registro general al servidor
   * @param {Object} registro - Objeto con datos del registro a enviar
   * @returns {Promise<Object>} - Respuesta del servidor
   */
  async enviarRegistro(registro) {
    try {
      console.log('📤 Enviando registro offline:', registro.id);
      console.log('🕐 Timestamp original:', registro.timestamp);
      console.log('📊 Datos del registro:', {
        id: registro.id,
        usuario_id: registro.usuario_id,
        tipo: registro.tipo || 'actividad',
        tiene_foto: !!registro.foto_base64,
        timestamp: registro.timestamp
      });
      
      // Validar datos básicos
      if (!registro.usuario_id || !registro.latitud || !registro.longitud) {
        console.error('❌ Registro incompleto, faltan datos básicos');
        throw new Error('Registro incompleto, faltan datos básicos');
      }
      
      // Obtener timestamp de sincronización (momento actual)
      const syncTimestamp = new Date().toISOString();
      await offlineService.actualizarTimestampSincronizacion(registro.id, 'registro');
      
      // Crear FormData para el envío
      const formData = new FormData();
      formData.append('usuario_id', registro.usuario_id.toString());
      formData.append('latitud', registro.latitud);
      formData.append('longitud', registro.longitud);
      formData.append('descripcion', registro.descripcion || '');
      formData.append('tipo_actividad', registro.tipo_actividad || 'campo'); // Nuevo: agregar tipo de actividad
      
      // MEJORA: Asegurar que se envía como tipo actividad explícitamente
      formData.append('tipo', 'actividad');
      
      // Usar el timestamp original (hora de creación offline) no el de sincronización
      formData.append('timestamp_offline', registro.timestamp);
      
      // Añadir campos adicionales para que el backend identifique correctamente los datos offline
      formData.append('es_registro_offline', 'true');
      formData.append('sync_timestamp', syncTimestamp);
      formData.append('origen_sync', 'pwa_super');
      formData.append('id_offline', registro.id.toString());
      
      console.log('📤 Enviando timestamp_offline:', registro.timestamp);
      console.log('📤 Enviando sync_timestamp:', syncTimestamp);
      console.log('📤 Enviando tipo de registro: actividad');
      
      // Convertir foto base64 de vuelta a archivo si existe
      let archivoAdjunto = false;
      if (registro.foto_base64) {
        console.log('🖼️ El registro contiene imagen base64, convirtiendo...');
        // MEJORA: Mayor nivel de logging para la conversión de imágenes
        console.log(`🔍 Longitud del string base64: ${registro.foto_base64.length}`);
        console.log(`🔍 Primeros 50 caracteres: ${registro.foto_base64.substring(0, 50)}...`);
        
        const archivo = offlineService.base64ToFile(
          registro.foto_base64,
          registro.foto_filename || `foto_${registro.id}.jpg`,
          registro.foto_type || 'image/jpeg'
        );
        
        if (archivo) {
          console.log(`🖼️ Imagen convertida correctamente: ${archivo.name}, ${archivo.size} bytes, tipo: ${archivo.type}`);
          formData.append('foto', archivo);
          archivoAdjunto = true;
        } else {
          console.error('❌ Error al convertir imagen base64 a archivo');
          console.log('⚠️ Intentando enviar sin foto debido a error de conversión');
          // Continuar sin foto si hay error en la conversión
        }
      } else {
        console.warn('⚠️ El registro no contiene imagen base64');
      }
      
      console.log(`📤 Enviando registro al backend${archivoAdjunto ? ' con foto adjunta' : ' sin foto'}`);
      
      // Enviar al endpoint de registros con headers adicionales para identificación
      // MEJORA: Headers más explícitos para mejor procesamiento en el backend
      const response = await axios.post(`${API_URL}/registro`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-Offline-Sync': 'true',
          'X-Sync-Timestamp': syncTimestamp,
          'X-Offline-ID': registro.id.toString(),
          'X-Registro-Tipo': 'actividad',
          'X-Retry-After-Error': 'true'
        },
        timeout: 30000, // 30 segundos de timeout
        maxContentLength: Infinity,
        maxBodyLength: Infinity
      });
      
      // Verificar que la respuesta sea válida
      if (!response || !response.data) {
        console.error('❌ El servidor no devolvió una respuesta válida');
        throw new Error('Respuesta del servidor inválida');
      }
      
      console.log('✅ Registro enviado exitosamente:', response.data);
      return response.data;
      
    } catch (error) {
      console.error('❌ Error enviando registro:', error);
      
      // MEJORA: Verificación más robusta de errores de duplicado
      // Verificar error de duplicado de diferentes formas posibles
      if (error.response && error.response.status === 400) {
        const errorDetail = error.response.data?.detail || '';
        
        // Verificar diferentes mensajes de duplicado
        if (errorDetail.includes('ya existe') || 
            errorDetail.includes('duplicado') || 
            errorDetail.includes('duplicate') || 
            errorDetail.includes('Ya registrado')) {
          console.log('ℹ️ Registro ya existe en el servidor, marcando como enviado');
          return { mensaje: 'Registro ya existía en el servidor' };
        }
      }
      
      // MEJORA: Mejor logging de errores para debugging
      console.error('📄 Detalles completos del error:');
      if (error.response) {
        console.error('- Status:', error.response.status);
        console.error('- Headers:', error.response.headers);
        console.error('- Data:', error.response.data);
      } else if (error.request) {
        console.error('- Sin respuesta del servidor:', error.request);
        console.error('- Datos de la solicitud:', error.config?.data?.substring(0, 100) + '...');
      } else {
        console.error('- Error de configuración:', error.message);
      }
      
      throw error;
    }
  }

  /**
   * Envía una asistencia al servidor
   */
  async enviarAsistencia(asistencia) {
    try {
      console.log(`📤 Enviando asistencia ${asistencia.tipo} offline:`, asistencia.id);
      console.log('🕐 Timestamp original:', asistencia.timestamp);
      
      // Obtener timestamp de sincronización (momento actual)
      const syncTimestamp = new Date().toISOString();
      await offlineService.actualizarTimestampSincronizacion(asistencia.id, 'asistencia');
      
      // Crear FormData para el envío
      const formData = new FormData();
      formData.append('usuario_id', asistencia.usuario_id.toString());
      formData.append('latitud', asistencia.latitud);
      formData.append('longitud', asistencia.longitud);
      formData.append('descripcion', asistencia.descripcion || '');
      
      // Usar el timestamp original (hora de creación offline) no el de sincronización
      formData.append('timestamp_offline', asistencia.timestamp);
      
      // Añadir campos adicionales para que el backend identifique correctamente los datos offline
      formData.append('es_asistencia_offline', 'true');
      formData.append('sync_timestamp', syncTimestamp);
      formData.append('origen_sync', 'pwa_super');
      formData.append('id_offline', asistencia.id.toString());
      formData.append('fecha_offline', asistencia.fecha || new Date().toISOString().split('T')[0]);
      
      console.log(`📤 Enviando timestamp_offline para ${asistencia.tipo}:`, asistencia.timestamp);
      console.log(`📤 Enviando sync_timestamp:`, syncTimestamp);
      
      // Convertir foto base64 de vuelta a archivo si existe
      if (asistencia.foto_base64) {
        const archivo = offlineService.base64ToFile(
          asistencia.foto_base64,
          asistencia.foto_filename || `${asistencia.tipo}_${asistencia.id}.jpg`,
          asistencia.foto_type || 'image/jpeg'
        );
        
        if (archivo) {
          formData.append('foto', archivo);
        }
      }
      
      // Configurar headers comunes para la petición
      const requestConfig = {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-Offline-Sync': 'true',
          'X-Sync-Timestamp': syncTimestamp,
          'X-Offline-ID': asistencia.id.toString(),
          'X-Asistencia-Tipo': asistencia.tipo
        },
        timeout: 30000, // 30 segundos de timeout
        maxContentLength: Infinity,
        maxBodyLength: Infinity
      };
      
      // Enviar según el tipo de asistencia
      let response;
      if (asistencia.tipo === 'entrada') {
        // Pasar la configuración de headers a registrarEntrada
        response = await asistenciasService.registrarEntrada(formData, requestConfig);
      } else if (asistencia.tipo === 'salida') {
        // Pasar la configuración de headers a registrarSalida
        response = await asistenciasService.registrarSalida(formData, requestConfig);
      } else {
        throw new Error(`Tipo de asistencia desconocido: ${asistencia.tipo}`);
      }
      
      console.log(`✅ Asistencia ${asistencia.tipo} enviada exitosamente:`, response);
      return response;
      
    } catch (error) {
      console.error(`❌ Error enviando asistencia ${asistencia.tipo}:`, error);
      
      // Si es un error de duplicado, lo consideramos éxito (ya existe)
      if (error.response && error.response.status === 400 && 
          error.response.data.detail && 
          (error.response.data.detail.includes('Ya existe') || 
           error.response.data.detail.includes('ya registrada'))) {
        console.log(`ℹ️ Asistencia ${asistencia.tipo} ya existe en el servidor, marcando como enviada`);
        return { mensaje: `Asistencia ${asistencia.tipo} ya existía en el servidor` };
      }
      
      throw error;
    }
  }

  /**
   * Obtiene el estado de conectividad actual
   */
  getConnectionStatus() {
    return {
      isOnline: this.isOnline,
      isSyncing: this.isSyncing
    };
  }

  /**
   * Fuerza una sincronización manual
   */
  async sincronizarManual() {
    if (!this.isOnline) {
      throw new Error('No hay conexión a internet');
    }
    
    return await this.sincronizarTodo();
  }

  /**
   * Obtiene el número de elementos pendientes
   * @param {boolean} forceRefresh - Si es true, fuerza una consulta fresca a la base de datos
   * @returns {Promise<number>} - Número total de elementos pendientes de sincronización
   */
  async obtenerPendientes(forceRefresh = false) {
    return await offlineService.contarPendientes(forceRefresh);
  }
}

// Crear instancia singleton
const syncService = new SyncService();

export default syncService;
