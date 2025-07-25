/**
 * Servicio para manejar datos offline usando IndexedDB
 * Implementa un sistema robusto de cache y sincronización
 */

class OfflineService {
  constructor() {
    this.dbName = 'PWASuperOfflineDB';
    this.dbVersion = 1;
    this.db = null;
    this.syncInProgress = false;
    this.listeners = new Set();
    
    // Configuración de stores
    this.stores = {
      pendingRecords: 'pending_records',
      pendingAttendances: 'pending_attendances', 
      offlineQueue: 'offline_queue',
      syncLog: 'sync_log'
    };

    this.initDB();
    this.setupEventListeners();
  }

  /**
   * Inicializa la base de datos IndexedDB
   */
  async initDB() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.dbVersion);

      request.onerror = () => {
        console.error('❌ Error al abrir IndexedDB:', request.error);
        reject(request.error);
      };

      request.onsuccess = () => {
        this.db = request.result;
        console.log('✅ IndexedDB inicializada correctamente');
        resolve(this.db);
      };

      request.onupgradeneeded = (event) => {
        const db = event.target.result;

        // Store para registros pendientes
        if (!db.objectStoreNames.contains(this.stores.pendingRecords)) {
          const recordsStore = db.createObjectStore(this.stores.pendingRecords, { 
            keyPath: 'id', 
            autoIncrement: true 
          });
          recordsStore.createIndex('timestamp', 'timestamp');
          recordsStore.createIndex('status', 'status');
          recordsStore.createIndex('type', 'type');
        }

        // Store para asistencias pendientes
        if (!db.objectStoreNames.contains(this.stores.pendingAttendances)) {
          const attendancesStore = db.createObjectStore(this.stores.pendingAttendances, { 
            keyPath: 'id', 
            autoIncrement: true 
          });
          attendancesStore.createIndex('timestamp', 'timestamp');
          attendancesStore.createIndex('status', 'status');
          attendancesStore.createIndex('attendanceType', 'attendanceType');
        }

        // Store para cola de operaciones offline
        if (!db.objectStoreNames.contains(this.stores.offlineQueue)) {
          const queueStore = db.createObjectStore(this.stores.offlineQueue, { 
            keyPath: 'id', 
            autoIncrement: true 
          });
          queueStore.createIndex('priority', 'priority');
          queueStore.createIndex('createdAt', 'createdAt');
        }

        // Store para log de sincronización
        if (!db.objectStoreNames.contains(this.stores.syncLog)) {
          const logStore = db.createObjectStore(this.stores.syncLog, { 
            keyPath: 'id', 
            autoIncrement: true 
          });
          logStore.createIndex('date', 'date');
          logStore.createIndex('status', 'status');
        }

        console.log('🗄️ Estructura de IndexedDB creada/actualizada');
      };
    });
  }

  /**
   * Configura event listeners para detectar cambios de conectividad
   */
  setupEventListeners() {
    // Escuchar cambios de conectividad
    window.addEventListener('online', () => {
      console.log('🌐 Conexión restaurada - iniciando sincronización automática');
      this.notifyListeners('connection', { online: true });
      this.autoSync();
    });

    window.addEventListener('offline', () => {
      console.log('📴 Conexión perdida - modo offline activado');
      this.notifyListeners('connection', { online: false });
    });

    // Sincronización periódica cuando la app esté activa
    setInterval(() => {
      if (navigator.onLine && !this.syncInProgress) {
        this.autoSync();
      }
    }, 30000); // Cada 30 segundos
  }

  /**
   * Verifica si hay conexión a internet
   */
  async isOnline() {
    if (!navigator.onLine) return false;

    try {
      // Verificar conectividad real con un endpoint ligero
      const response = await fetch('/ping', { 
        method: 'HEAD',
        timeout: 5000,
        cache: 'no-store'
      });
      return response.ok;
    } catch {
      return false;
    }
  }

  /**
   * Guarda un registro offline
   */
  async saveRecordOffline(recordData) {
    try {
      await this.initDB();
      
      const record = {
        ...recordData,
        id: undefined, // Se auto-generará
        status: 'pending',
        type: 'record',
        timestamp: new Date().toISOString(),
        createdAt: Date.now(),
        retryCount: 0,
        lastError: null
      };

      const transaction = this.db.transaction([this.stores.pendingRecords], 'readwrite');
      const store = transaction.objectStore(this.stores.pendingRecords);
      const result = await this.promisifyRequest(store.add(record));

      console.log('💾 Registro guardado offline:', result);
      
      this.notifyListeners('recordSaved', { 
        id: result, 
        type: 'record',
        message: 'Sin conexión. Tu registro ha sido guardado localmente y se enviará cuando recuperes conexión.' 
      });

      return result;
    } catch (error) {
      console.error('❌ Error guardando registro offline:', error);
      throw error;
    }
  }

  /**
   * Guarda una asistencia offline
   */
  async saveAttendanceOffline(attendanceData) {
    try {
      await this.initDB();
      
      const attendance = {
        ...attendanceData,
        id: undefined, // Se auto-generará
        status: 'pending',
        timestamp: new Date().toISOString(),
        createdAt: Date.now(),
        retryCount: 0,
        lastError: null
      };

      const transaction = this.db.transaction([this.stores.pendingAttendances], 'readwrite');
      const store = transaction.objectStore(this.stores.pendingAttendances);
      const result = await this.promisifyRequest(store.add(attendance));

      console.log('💾 Asistencia guardada offline:', result);
      
      this.notifyListeners('attendanceSaved', { 
        id: result, 
        type: 'attendance',
        attendanceType: attendanceData.attendanceType,
        message: 'Sin conexión. Tu asistencia ha sido guardada localmente y se enviará cuando recuperes conexión.' 
      });

      return result;
    } catch (error) {
      console.error('❌ Error guardando asistencia offline:', error);
      throw error;
    }
  }

  /**
   * Obtiene todos los elementos pendientes de sincronización
   */
  async getPendingItems() {
    try {
      await this.initDB();
      
      const [records, attendances] = await Promise.all([
        this.getAllFromStore(this.stores.pendingRecords),
        this.getAllFromStore(this.stores.pendingAttendances)
      ]);

      return {
        records: records.filter(r => r.status === 'pending'),
        attendances: attendances.filter(a => a.status === 'pending'),
        total: records.length + attendances.length
      };
    } catch (error) {
      console.error('❌ Error obteniendo elementos pendientes:', error);
      return { records: [], attendances: [], total: 0 };
    }
  }

  /**
   * Sincronización automática de elementos pendientes
   */
  async autoSync() {
    if (this.syncInProgress || !(await this.isOnline())) {
      return;
    }

    this.syncInProgress = true;
    console.log('🔄 Iniciando sincronización automática...');

    try {
      const pending = await this.getPendingItems();
      
      if (pending.total === 0) {
        console.log('✅ No hay elementos pendientes de sincronización');
        return;
      }

      console.log(`📤 Sincronizando ${pending.total} elementos pendientes...`);
      
      // Sincronizar registros
      for (const record of pending.records) {
        await this.syncRecord(record);
      }

      // Sincronizar asistencias
      for (const attendance of pending.attendances) {
        await this.syncAttendance(attendance);
      }

      console.log('✅ Sincronización automática completada');
      
      this.notifyListeners('syncCompleted', { 
        syncedCount: pending.total,
        message: 'Sincronización completada. Todos los registros han sido enviados.' 
      });

    } catch (error) {
      console.error('❌ Error en sincronización automática:', error);
    } finally {
      this.syncInProgress = false;
    }
  }

  /**
   * Sincroniza un registro específico
   */
  async syncRecord(record) {
    try {
      const { apiService } = await import('./apiService.js');
      
      // Preparar FormData si hay archivos
      const formData = new FormData();
      Object.keys(record).forEach(key => {
        if (key !== 'id' && key !== 'status' && key !== 'timestamp' && 
            key !== 'createdAt' && key !== 'retryCount' && key !== 'lastError') {
          formData.append(key, record[key]);
        }
      });

      const response = await apiService.createRecord(formData);
      
      // Marcar como sincronizado y eliminar
      await this.markAsSynced(this.stores.pendingRecords, record.id);
      
      console.log('✅ Registro sincronizado:', response);
      
      this.notifyListeners('itemSynced', {
        type: 'record',
        id: record.id,
        response,
        message: 'Registro enviado con éxito.'
      });

    } catch (error) {
      console.error('❌ Error sincronizando registro:', error);
      await this.markSyncError(this.stores.pendingRecords, record.id, error.message);
      
      this.notifyListeners('syncError', {
        type: 'record',
        id: record.id,
        error: error.message
      });
    }
  }

  /**
   * Sincroniza una asistencia específica
   */
  async syncAttendance(attendance) {
    try {
      const { apiService } = await import('./apiService.js');
      
      // Preparar FormData
      const formData = new FormData();
      Object.keys(attendance).forEach(key => {
        if (key !== 'id' && key !== 'status' && key !== 'timestamp' && 
            key !== 'createdAt' && key !== 'retryCount' && key !== 'lastError') {
          formData.append(key, attendance[key]);
        }
      });

      let response;
      if (attendance.attendanceType === 'entrada') {
        response = await apiService.markEntry(formData);
      } else {
        response = await apiService.markExit(formData);
      }
      
      // Marcar como sincronizado y eliminar
      await this.markAsSynced(this.stores.pendingAttendances, attendance.id);
      
      console.log('✅ Asistencia sincronizada:', response);
      
      this.notifyListeners('itemSynced', {
        type: 'attendance',
        attendanceType: attendance.attendanceType,
        id: attendance.id,
        response,
        message: `${attendance.attendanceType === 'entrada' ? 'Entrada' : 'Salida'} enviada con éxito.`
      });

    } catch (error) {
      console.error('❌ Error sincronizando asistencia:', error);
      await this.markSyncError(this.stores.pendingAttendances, attendance.id, error.message);
      
      this.notifyListeners('syncError', {
        type: 'attendance',
        id: attendance.id,
        error: error.message
      });
    }
  }

  /**
   * Marca un elemento como sincronizado y lo elimina
   */
  async markAsSynced(storeName, id) {
    try {
      const transaction = this.db.transaction([storeName], 'readwrite');
      const store = transaction.objectStore(storeName);
      await this.promisifyRequest(store.delete(id));
      
      // Log de sincronización exitosa
      await this.logSync(id, 'success', storeName);
    } catch (error) {
      console.error('❌ Error marcando como sincronizado:', error);
    }
  }

  /**
   * Marca un error de sincronización
   */
  async markSyncError(storeName, id, errorMessage) {
    try {
      const transaction = this.db.transaction([storeName], 'readwrite');
      const store = transaction.objectStore(storeName);
      const item = await this.promisifyRequest(store.get(id));
      
      if (item) {
        item.retryCount = (item.retryCount || 0) + 1;
        item.lastError = errorMessage;
        item.lastRetry = new Date().toISOString();
        
        // Si hay demasiados intentos, marcar como error permanente
        if (item.retryCount >= 5) {
          item.status = 'failed';
        }
        
        await this.promisifyRequest(store.put(item));
      }

      // Log de error
      await this.logSync(id, 'error', storeName, errorMessage);
    } catch (error) {
      console.error('❌ Error marcando error de sincronización:', error);
    }
  }

  /**
   * Registra en el log de sincronización
   */
  async logSync(itemId, status, storeName, error = null) {
    try {
      const logEntry = {
        itemId,
        status,
        storeName,
        error,
        date: new Date().toISOString()
      };

      const transaction = this.db.transaction([this.stores.syncLog], 'readwrite');
      const store = transaction.objectStore(this.stores.syncLog);
      await this.promisifyRequest(store.add(logEntry));
    } catch (error) {
      console.error('❌ Error registrando log:', error);
    }
  }

  /**
   * Utilidades para manejar IndexedDB con Promises
   */
  promisifyRequest(request) {
    return new Promise((resolve, reject) => {
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async getAllFromStore(storeName) {
    const transaction = this.db.transaction([storeName], 'readonly');
    const store = transaction.objectStore(storeName);
    return this.promisifyRequest(store.getAll());
  }

  /**
   * Sistema de eventos para notificar cambios
   */
  addListener(callback) {
    this.listeners.add(callback);
    return () => this.listeners.delete(callback);
  }

  notifyListeners(event, data) {
    this.listeners.forEach(callback => {
      try {
        callback({ event, data });
      } catch (error) {
        console.error('❌ Error en listener:', error);
      }
    });
  }

  /**
   * Limpia datos antiguos (más de 30 días)
   */
  async cleanupOldData() {
    try {
      const thirtyDaysAgo = Date.now() - (30 * 24 * 60 * 60 * 1000);
      
      for (const storeName of Object.values(this.stores)) {
        const transaction = this.db.transaction([storeName], 'readwrite');
        const store = transaction.objectStore(storeName);
        const items = await this.promisifyRequest(store.getAll());
        
        for (const item of items) {
          if (item.createdAt && item.createdAt < thirtyDaysAgo) {
            await this.promisifyRequest(store.delete(item.id));
          }
        }
      }
      
      console.log('🧹 Limpieza de datos antiguos completada');
    } catch (error) {
      console.error('❌ Error en limpieza de datos:', error);
    }
  }

  /**
   * Obtiene estadísticas del almacenamiento offline
   */
  async getStats() {
    try {
      const pending = await this.getPendingItems();
      const logs = await this.getAllFromStore(this.stores.syncLog);
      
      return {
        pendingRecords: pending.records.length,
        pendingAttendances: pending.attendances.length,
        totalPending: pending.total,
        syncLogs: logs.length,
        lastSync: logs.length > 0 ? logs[logs.length - 1].date : null
      };
    } catch (error) {
      console.error('❌ Error obteniendo estadísticas:', error);
      return {
        pendingRecords: 0,
        pendingAttendances: 0,
        totalPending: 0,
        syncLogs: 0,
        lastSync: null
      };
    }
  }
}

// Instancia singleton
const offlineService = new OfflineService();

export { offlineService };
export default offlineService;
