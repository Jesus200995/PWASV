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
    this.autoSyncInterval = null;
    this.setupEventListeners();
    this.iniciarVerificacionPeriodica();
  }

  /**
   * Configura los listeners para detectar cambios de conectividad
   */
  setupEventListeners() {
    // Listener para cuando se recupera la conexión
    window.addEventListener('online', async () => {
      console.log('🌐 Conexión recuperada, iniciando sincronización inmediata...');
      this.isOnline = true;
      this.notifyListeners('online');
      
      // Sincronizar inmediatamente sin esperar
      await this.sincronizarTodo();
    });

    // Listener para cuando se pierde la conexión
    window.addEventListener('offline', () => {
      console.log('📴 Conexión perdida');
      this.isOnline = false;
      this.notifyListeners('offline');
    });

    // Verificar conexión inicial
    this.verificarConexionInicial();
  }

  /**
   * Verifica la conexión inicial al cargar la aplicación
   */
  async verificarConexionInicial() {
    try {
      this.isOnline = await checkInternetConnection();
      this.notifyListeners(this.isOnline ? 'online' : 'offline');
      
      // Si estamos online al iniciar, sincronizar datos pendientes inmediatamente
      if (this.isOnline) {
        setTimeout(async () => {
          await this.sincronizarTodo();
        }, 1000); // Solo esperar 1 segundo para verificación inicial
      }
    } catch (error) {
      console.error('Error verificando conexión inicial:', error);
      this.isOnline = false;
      this.notifyListeners('offline');
    }
  }

  /**
   * Inicia verificación periódica de conexión y sincronización automática
   */
  iniciarVerificacionPeriodica() {
    // Verificar cada 30 segundos si hay conexión y datos pendientes
    this.autoSyncInterval = setInterval(async () => {
      try {
        const reallyOnline = await checkInternetConnection();
        
        if (reallyOnline && !this.isSyncing) {
          this.isOnline = true;
          
          // Verificar si hay datos pendientes
          const pendientes = await offlineService.contarPendientes(true);
          if (pendientes.total > 0) {
            console.log(`🔄 Verificación periódica: ${pendientes.total} registros pendientes, sincronizando automáticamente...`);
            await this.sincronizarTodo();
          }
        } else if (!reallyOnline) {
          this.isOnline = false;
        }
      } catch (error) {
        console.error('Error en verificación periódica:', error);
      }
    }, 30000); // 30 segundos
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
   */
  notifyListeners(status) {
    this.listeners.forEach(callback => {
      try {
        callback(status, this.isOnline);
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
      return;
    }

    this.isSyncing = true;
    
    try {
      console.log('🔄 Iniciando sincronización completa...');
      
      // Verificar que realmente tengamos conexión
      const reallyOnline = await checkInternetConnection();
      if (!reallyOnline) {
        console.log('❌ Verificación de conexión falló, cancelando sincronización');
        this.isOnline = false;
        this.notifyListeners('offline');
        return;
      }

      // Obtener datos pendientes
      const registrosPendientes = await offlineService.obtenerRegistrosPendientes();
      const asistenciasPendientes = await offlineService.obtenerAsistenciasPendientes();
      
      const totalPendientes = registrosPendientes.length + asistenciasPendientes.length;
      
      if (totalPendientes === 0) {
        console.log('✅ No hay datos pendientes para sincronizar');
        return;
      }
      
      console.log(`📊 Sincronizando ${totalPendientes} elementos (${registrosPendientes.length} registros de actividad, ${asistenciasPendientes.length} asistencias)`);
      
      // Notificar inicio de sincronización
      this.notifyListeners('syncing', true, totalPendientes);
      
      let exitosos = 0;
      let fallidos = 0;
      
      // Sincronizar registros de actividad primero (son más importantes)
      for (const registro of registrosPendientes) {
        try {
          console.log(`📤 Sincronizando registro de actividad ID offline: ${registro.id}`);
          await this.enviarRegistro(registro);
          await offlineService.eliminarRegistro(registro.id);
          exitosos++;
          console.log(`✅ Registro de actividad ${registro.id} sincronizado exitosamente`);
          
          // Notificar progreso
          this.notifyListeners('sync_progress', true, {
            procesados: exitosos + fallidos,
            total: totalPendientes,
            exitosos,
            fallidos
          });
          
        } catch (error) {
          console.error(`❌ Error enviando registro de actividad ${registro.id}:`, error);
          fallidos++;
        }
      }
      
      // Sincronizar asistencias
      for (const asistencia of asistenciasPendientes) {
        try {
          await this.enviarAsistencia(asistencia);
          await offlineService.eliminarAsistencia(asistencia.id);
          exitosos++;
          
          // Notificar progreso
          this.notifyListeners('sync_progress', true, {
            procesados: exitosos + fallidos,
            total: totalPendientes,
            exitosos,
            fallidos
          });
          
        } catch (error) {
          console.error(`❌ Error enviando asistencia ${asistencia.id}:`, error);
          fallidos++;
        }
      }
      
      // Notificar resultado final
      console.log(`✅ Sincronización completada: ${exitosos} exitosos, ${fallidos} fallidos`);
      this.notifyListeners('sync_complete', true, { exitosos, fallidos, total: totalPendientes });
      
    } catch (error) {
      console.error('❌ Error durante la sincronización:', error);
      this.notifyListeners('sync_error', true, error);
    } finally {
      this.isSyncing = false;
    }
  }

  /**
   * Envía un registro general al servidor
   */
  async enviarRegistro(registro) {
    try {
      console.log('📤 Enviando registro de actividad offline:', registro.id);
      console.log('🕐 Timestamp original:', registro.timestamp);
      console.log('📊 Datos del registro:', {
        usuario_id: registro.usuario_id,
        tipo: registro.tipo,
        descripcion: registro.descripcion,
        latitud: registro.latitud,
        longitud: registro.longitud,
        tiene_foto: !!registro.foto_base64
      });
      
      // Obtener timestamp de sincronización (momento actual)
      const syncTimestamp = new Date().toISOString();
      await offlineService.actualizarTimestampSincronizacion(registro.id, 'registro');
      
      // Crear FormData para el envío
      const formData = new FormData();
      formData.append('usuario_id', registro.usuario_id.toString());
      formData.append('latitud', registro.latitud);
      formData.append('longitud', registro.longitud);
      formData.append('descripcion', registro.descripcion || '');
      
      // Usar el timestamp original (hora de creación offline) no el de sincronización
      formData.append('timestamp_offline', registro.timestamp);
      
      // Añadir campos adicionales para que el backend identifique correctamente los datos offline
      formData.append('es_registro_offline', 'true');
      formData.append('sync_timestamp', syncTimestamp);
      formData.append('origen_sync', 'pwa_super');
      // NO enviar id_offline para que el backend genere el ID correcto
      formData.append('tipo', 'actividad'); // Siempre usar 'actividad' para registros de actividad
      
      console.log('📤 Enviando timestamp_offline:', registro.timestamp);
      console.log('📤 Enviando sync_timestamp:', syncTimestamp);
      console.log('📤 Enviando tipo de registro: actividad');
      
      // Convertir foto base64 de vuelta a archivo si existe
      if (registro.foto_base64) {
        const archivo = offlineService.base64ToFile(
          registro.foto_base64,
          registro.foto_filename || `actividad_${registro.id}.jpg`,
          registro.foto_type || 'image/jpeg'
        );
        
        if (archivo) {
          formData.append('foto', archivo);
          console.log('📷 Foto adjunta:', archivo.name, archivo.size, 'bytes');
        }
      }
      
      // Enviar al endpoint de registros con headers adicionales para identificación
      const response = await axios.post(`${API_URL}/registro`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-Offline-Sync': 'true',
          'X-Sync-Timestamp': syncTimestamp,
          'X-Registro-Tipo': 'actividad' // Siempre identificar explícitamente como actividad
        },
        timeout: 30000, // 30 segundos de timeout
        maxContentLength: Infinity,
        maxBodyLength: Infinity
      });
      
      console.log('✅ Registro de actividad enviado exitosamente:', response.data);
      return response.data;
      
    } catch (error) {
      console.error('❌ Error enviando registro de actividad:', error);
      
      // Si es un error de duplicado, lo consideramos éxito (ya existe)
      if (error.response && error.response.status === 400 && 
          error.response.data.detail && 
          error.response.data.detail.includes('ya existe')) {
        console.log('ℹ️ Registro de actividad ya existe en el servidor, marcando como enviado');
        return { mensaje: 'Registro ya existía en el servidor' };
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

  /**
   * Limpia los recursos del servicio
   */
  destroy() {
    if (this.autoSyncInterval) {
      clearInterval(this.autoSyncInterval);
      this.autoSyncInterval = null;
    }
  }
}

// Crear instancia singleton
const syncService = new SyncService();

export default syncService;
