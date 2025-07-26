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
      this.notifyListeners('online');
      
      // Esperar un poco para asegurar que la conexión es estable
      setTimeout(async () => {
        await this.sincronizarTodo();
      }, 2000);
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
      
      console.log(`📊 Sincronizando ${totalPendientes} elementos (${registrosPendientes.length} registros, ${asistenciasPendientes.length} asistencias)`);
      
      // Notificar inicio de sincronización
      this.notifyListeners('syncing', true, totalPendientes);
      
      let exitosos = 0;
      let fallidos = 0;
      
      // Sincronizar registros generales
      for (const registro of registrosPendientes) {
        try {
          await this.enviarRegistro(registro);
          await offlineService.eliminarRegistro(registro.id);
          exitosos++;
          
          // Notificar progreso
          this.notifyListeners('sync_progress', true, {
            procesados: exitosos + fallidos,
            total: totalPendientes,
            exitosos,
            fallidos
          });
          
        } catch (error) {
          console.error(`❌ Error enviando registro ${registro.id}:`, error);
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
      console.log('📤 ============ INICIANDO ENVÍO DE REGISTRO ============');
      console.log('📤 Registro ID:', registro.id);
      console.log('🕐 Timestamp original del registro:', registro.timestamp);
      
      // Actualizar el timestamp de sincronización antes de enviar
      await offlineService.actualizarTimestampSincronizacion(registro.id, 'registro');
      
      // Crear FormData para el envío
      const formData = new FormData();
      
      // CAMPOS BÁSICOS
      formData.append('usuario_id', String(registro.usuario_id));
      formData.append('latitud', String(registro.latitud));
      formData.append('longitud', String(registro.longitud));
      formData.append('descripcion', String(registro.descripcion || ''));
      
      // CAMPO CRÍTICO - TIMESTAMP OFFLINE
      if (registro.timestamp) {
        formData.append('timestamp_offline', String(registro.timestamp));
        console.log('📤 ✅ ✅ ✅ AGREGANDO timestamp_offline al FormData:', registro.timestamp);
      } else {
        console.log('❌❌❌ NO HAY timestamp en el registro:', registro);
      }
      
      // FOTO
      if (registro.foto_base64) {
        const archivo = offlineService.base64ToFile(
          registro.foto_base64,
          registro.foto_filename || `foto_${registro.id}.jpg`,
          registro.foto_type || 'image/jpeg'
        );
        
        if (archivo) {
          formData.append('foto', archivo);
          console.log('📷 Foto agregada al FormData:', archivo.name);
        }
      }
      
      // VERIFICAR CONTENIDO DEL FORMDATA
      console.log('📋 ============ CONTENIDO COMPLETO DEL FORMDATA ============');
      for (let [key, value] of formData.entries()) {
        if (key === 'foto') {
          console.log(`   ${key}: [File object] ${value.name}`);
        } else {
          console.log(`   ${key}: "${value}" (tipo: ${typeof value})`);
        }
      }
      console.log('📋 ============ FIN CONTENIDO FORMDATA ============');
      
      // ENVIAR AL SERVIDOR
      console.log('🚀 Enviando POST a /registro...');
      const response = await axios.post(`${API_URL}/registro`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000,
        maxContentLength: Infinity,
        maxBodyLength: Infinity
      });
      
      console.log('✅ ============ RESPUESTA DEL SERVIDOR ============');
      console.log('✅ Registro enviado exitosamente:', response.data);
      console.log('✅ ============ FIN RESPUESTA ============');
      return response.data;
      
    } catch (error) {
      console.error('❌ Error enviando registro:', error);
      
      // Si es un error de duplicado, lo consideramos éxito (ya existe)
      if (error.response && error.response.status === 400 && 
          error.response.data.detail && 
          error.response.data.detail.includes('ya existe')) {
        console.log('ℹ️ Registro ya existe en el servidor, marcando como enviado');
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
      
      // Actualizar el timestamp de sincronización antes de enviar
      await offlineService.actualizarTimestampSincronizacion(asistencia.id, 'asistencia');
      
      // Crear FormData para el envío
      const formData = new FormData();
      formData.append('usuario_id', asistencia.usuario_id.toString());
      formData.append('latitud', asistencia.latitud.toString());
      formData.append('longitud', asistencia.longitud.toString());
      formData.append('descripcion', asistencia.descripcion || '');
      
      // VERIFICAR que el timestamp se esté enviando correctamente
      if (asistencia.timestamp) {
        formData.append('timestamp_offline', asistencia.timestamp);
        console.log(`📤 ✅ ENVIANDO timestamp_offline para ${asistencia.tipo}:`, asistencia.timestamp);
      } else {
        console.log(`❌ NO HAY timestamp en la asistencia ${asistencia.tipo}:`, asistencia);
      }
      
      // Log de todos los campos del FormData
      console.log(`📋 Campos del FormData para ${asistencia.tipo}:`);
      for (let [key, value] of formData.entries()) {
        console.log(`   ${key}: ${value}`);
      }
      
      // Convertir foto base64 de vuelta a archivo si existe
      if (asistencia.foto_base64) {
        const archivo = offlineService.base64ToFile(
          asistencia.foto_base64,
          asistencia.foto_filename || `${asistencia.tipo}_${asistencia.id}.jpg`,
          asistencia.foto_type || 'image/jpeg'
        );
        
        if (archivo) {
          formData.append('foto', archivo);
          console.log(`📷 Foto agregada al FormData para ${asistencia.tipo}:`, archivo.name);
        }
      }
      
      // Enviar según el tipo de asistencia
      let response;
      console.log(`🚀 Enviando ${asistencia.tipo} al servidor...`);
      if (asistencia.tipo === 'entrada') {
        response = await asistenciasService.registrarEntrada(formData);
      } else if (asistencia.tipo === 'salida') {
        response = await asistenciasService.registrarSalida(formData);
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
   */
  async obtenerPendientes() {
    return await offlineService.contarPendientes();
  }
}

// Crear instancia singleton
const syncService = new SyncService();

export default syncService;
