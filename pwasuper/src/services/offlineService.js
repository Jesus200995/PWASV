// Servicio para manejar registros offline usando IndexedDB
import { openDB } from 'idb';

/**
 * Servicio para gestionar almacenamiento offline con IndexedDB
 * Guarda registros cuando no hay conexión y los sincroniza cuando se recupera
 */
class OfflineService {
  constructor() {
    this.dbName = 'PWAOfflineDB';
    this.version = 1;
    this.db = null;
    this.syncInProgress = false;
  }

  /**
   * Inicializa la base de datos IndexedDB
   */
  async initDB() {
    if (this.db) return this.db;

    try {
      this.db = await openDB(this.dbName, this.version, {
        upgrade(db) {
          // Store para registros de entrada pendientes
          if (!db.objectStoreNames.contains('entradas_pendientes')) {
            const entradasStore = db.createObjectStore('entradas_pendientes', {
              keyPath: 'id',
              autoIncrement: true
            });
            entradasStore.createIndex('timestamp', 'timestamp');
            entradasStore.createIndex('usuario_id', 'usuario_id');
          }

          // Store para registros de salida pendientes
          if (!db.objectStoreNames.contains('salidas_pendientes')) {
            const salidasStore = db.createObjectStore('salidas_pendientes', {
              keyPath: 'id',
              autoIncrement: true
            });
            salidasStore.createIndex('timestamp', 'timestamp');
            salidasStore.createIndex('usuario_id', 'usuario_id');
          }

          // Store para registros generales pendientes (si aplica)
          if (!db.objectStoreNames.contains('registros_pendientes')) {
            const registrosStore = db.createObjectStore('registros_pendientes', {
              keyPath: 'id',
              autoIncrement: true
            });
            registrosStore.createIndex('timestamp', 'timestamp');
            registrosStore.createIndex('tipo', 'tipo');
          }
        }
      });

      console.log('✅ Base de datos offline inicializada correctamente');
      return this.db;
    } catch (error) {
      console.error('❌ Error inicializando base de datos offline:', error);
      throw error;
    }
  }

  /**
   * Guarda un registro de entrada offline
   * @param {FormData|Object} datos - Datos del registro de entrada
   * @param {number} usuarioId - ID del usuario
   */
  async guardarEntradaOffline(datos, usuarioId) {
    try {
      await this.initDB();

      // Convertir FormData a objeto si es necesario
      const datosObj = this._formDataToObject(datos);
      
      const registro = {
        tipo: 'entrada',
        usuario_id: usuarioId,
        datos: datosObj,
        timestamp: new Date().toISOString(),
        intentos: 0,
        estado: 'pendiente'
      };

      const tx = this.db.transaction('entradas_pendientes', 'readwrite');
      const store = tx.objectStore('entradas_pendientes');
      const result = await store.add(registro);

      console.log('💾 Entrada guardada offline con ID:', result);
      return result;
    } catch (error) {
      console.error('❌ Error guardando entrada offline:', error);
      throw error;
    }
  }

  /**
   * Guarda un registro de salida offline
   * @param {FormData|Object} datos - Datos del registro de salida
   * @param {number} usuarioId - ID del usuario
   */
  async guardarSalidaOffline(datos, usuarioId) {
    try {
      await this.initDB();

      // Convertir FormData a objeto si es necesario
      const datosObj = this._formDataToObject(datos);
      
      const registro = {
        tipo: 'salida',
        usuario_id: usuarioId,
        datos: datosObj,
        timestamp: new Date().toISOString(),
        intentos: 0,
        estado: 'pendiente'
      };

      const tx = this.db.transaction('salidas_pendientes', 'readwrite');
      const store = tx.objectStore('salidas_pendientes');
      const result = await store.add(registro);

      console.log('💾 Salida guardada offline con ID:', result);
      return result;
    } catch (error) {
      console.error('❌ Error guardando salida offline:', error);
      throw error;
    }
  }

  /**
   * Obtiene todos los registros pendientes de sincronización
   */
  async obtenerRegistrosPendientes() {
    try {
      await this.initDB();

      const entradas = await this._obtenerPendientes('entradas_pendientes');
      const salidas = await this._obtenerPendientes('salidas_pendientes');

      return {
        entradas,
        salidas,
        total: entradas.length + salidas.length
      };
    } catch (error) {
      console.error('❌ Error obteniendo registros pendientes:', error);
      return { entradas: [], salidas: [], total: 0 };
    }
  }

  /**
   * Sincroniza todos los registros pendientes con el servidor
   * @param {Object} servicioAsistencias - Instancia del servicio de asistencias
   * @param {Function} onProgress - Callback para mostrar progreso
   * @param {Function} onSuccess - Callback cuando se completa exitosamente
   * @param {Function} onError - Callback cuando hay errores
   */
  async sincronizarRegistros(servicioAsistencias, onProgress = null, onSuccess = null, onError = null) {
    if (this.syncInProgress) {
      console.log('⏳ Sincronización ya en progreso...');
      return;
    }

    this.syncInProgress = true;
    let errores = [];
    let exitosos = 0;

    try {
      const pendientes = await this.obtenerRegistrosPendientes();
      const total = pendientes.total;

      if (total === 0) {
        console.log('✅ No hay registros pendientes para sincronizar');
        this.syncInProgress = false;
        if (onSuccess) onSuccess(0);
        return;
      }

      console.log(`🔄 Iniciando sincronización de ${total} registros...`);
      if (onProgress) onProgress({ total, procesados: 0, errores: 0 });

      // Sincronizar entradas
      for (const entrada of pendientes.entradas) {
        try {
          const formData = this._objectToFormData(entrada.datos);
          await servicioAsistencias.registrarEntrada(formData);
          await this._eliminarRegistro('entradas_pendientes', entrada.id);
          exitosos++;
          console.log(`✅ Entrada sincronizada: ${entrada.id}`);
        } catch (error) {
          console.error(`❌ Error sincronizando entrada ${entrada.id}:`, error);
          errores.push({ tipo: 'entrada', id: entrada.id, error: error.message });
          await this._marcarErrorRegistro('entradas_pendientes', entrada.id);
        }
        
        if (onProgress) onProgress({ total, procesados: exitosos + errores.length, errores: errores.length });
      }

      // Sincronizar salidas
      for (const salida of pendientes.salidas) {
        try {
          const formData = this._objectToFormData(salida.datos);
          await servicioAsistencias.registrarSalida(formData);
          await this._eliminarRegistro('salidas_pendientes', salida.id);
          exitosos++;
          console.log(`✅ Salida sincronizada: ${salida.id}`);
        } catch (error) {
          console.error(`❌ Error sincronizando salida ${salida.id}:`, error);
          errores.push({ tipo: 'salida', id: salida.id, error: error.message });
          await this._marcarErrorRegistro('salidas_pendientes', salida.id);
        }
        
        if (onProgress) onProgress({ total, procesados: exitosos + errores.length, errores: errores.length });
      }

      console.log(`🔄 Sincronización completada: ${exitosos} exitosos, ${errores.length} errores`);
      
      if (errores.length === 0) {
        if (onSuccess) onSuccess(exitosos);
      } else {
        if (onError) onError(errores, exitosos);
      }

    } catch (error) {
      console.error('❌ Error durante la sincronización:', error);
      if (onError) onError([{ tipo: 'general', error: error.message }], exitosos);
    } finally {
      this.syncInProgress = false;
    }
  }

  /**
   * Limpia todos los registros offline (útil para reset)
   */
  async limpiarRegistrosOffline() {
    try {
      await this.initDB();

      const tx = this.db.transaction(['entradas_pendientes', 'salidas_pendientes'], 'readwrite');
      await tx.objectStore('entradas_pendientes').clear();
      await tx.objectStore('salidas_pendientes').clear();
      await tx.done;

      console.log('🗑️ Registros offline limpiados');
    } catch (error) {
      console.error('❌ Error limpiando registros offline:', error);
    }
  }

  /**
   * Obtiene estadísticas de registros offline
   */
  async obtenerEstadisticas() {
    try {
      const pendientes = await this.obtenerRegistrosPendientes();
      return {
        entradas_pendientes: pendientes.entradas.length,
        salidas_pendientes: pendientes.salidas.length,
        total_pendientes: pendientes.total,
        ultimo_registro: pendientes.total > 0 ? 
          Math.max(
            ...pendientes.entradas.map(e => new Date(e.timestamp).getTime()),
            ...pendientes.salidas.map(s => new Date(s.timestamp).getTime())
          ) : null
      };
    } catch (error) {
      console.error('❌ Error obteniendo estadísticas:', error);
      return null;
    }
  }

  // Métodos privados

  /**
   * Convierte FormData a objeto plano
   * @private
   */
  _formDataToObject(formData) {
    if (!formData || typeof formData !== 'object') return formData;

    if (formData instanceof FormData) {
      const obj = {};
      for (const [key, value] of formData.entries()) {
        if (value instanceof File) {
          // Para archivos, guardamos información básica
          obj[key] = {
            name: value.name,
            size: value.size,
            type: value.type,
            lastModified: value.lastModified,
            // Nota: No podemos guardar el archivo completo en IndexedDB de forma sencilla
            // Para implementación completa de archivos offline, se necesitaría FileReader
            isFile: true
          };
        } else {
          obj[key] = value;
        }
      }
      return obj;
    }

    return formData;
  }

  /**
   * Convierte objeto a FormData
   * @private
   */
  _objectToFormData(obj) {
    const formData = new FormData();
    
    for (const [key, value] of Object.entries(obj)) {
      if (value && typeof value === 'object' && value.isFile) {
        // Para archivos guardados offline, necesitaríamos reconstruirlos
        // Por simplicidad, omitimos archivos en la sincronización offline
        console.warn(`⚠️ Archivo ${key} omitido en sincronización offline`);
        continue;
      }
      formData.append(key, value);
    }
    
    return formData;
  }

  /**
   * Obtiene registros pendientes de un store específico
   * @private
   */
  async _obtenerPendientes(storeName) {
    const tx = this.db.transaction(storeName, 'readonly');
    const store = tx.objectStore(storeName);
    return await store.getAll();
  }

  /**
   * Elimina un registro específico
   * @private
   */
  async _eliminarRegistro(storeName, id) {
    const tx = this.db.transaction(storeName, 'readwrite');
    const store = tx.objectStore(storeName);
    await store.delete(id);
  }

  /**
   * Marca un registro con error (incrementa intentos)
   * @private
   */
  async _marcarErrorRegistro(storeName, id) {
    const tx = this.db.transaction(storeName, 'readwrite');
    const store = tx.objectStore(storeName);
    const registro = await store.get(id);
    
    if (registro) {
      registro.intentos = (registro.intentos || 0) + 1;
      registro.ultimo_error = new Date().toISOString();
      await store.put(registro);
    }
  }
}

// Instancia única del servicio
const offlineService = new OfflineService();

export default offlineService;
