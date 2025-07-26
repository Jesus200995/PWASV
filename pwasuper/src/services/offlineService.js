/**
 * Servicio para gestionar registros offline
 * Utiliza IndexedDB para almacenar datos complejos incluyendo fotos
 */

const DB_NAME = 'PWAOfflineDB';
const DB_VERSION = 1;
const REGISTROS_STORE = 'registros_pendientes';
const ASISTENCIAS_STORE = 'asistencias_pendientes';

class OfflineService {
  constructor() {
    this.db = null;
    this.initDB();
  }

  /**
   * Inicializa la base de datos IndexedDB
   */
  async initDB() {
    if (this.db) {
      return this.db;
    }
    
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION);

      request.onerror = () => {
        console.error('❌ Error al abrir la base de datos offline:', request.error);
        this.db = null;
        reject(request.error);
      };

      request.onsuccess = () => {
        this.db = request.result;
        console.log('✅ Base de datos offline inicializada');
        
        // Agregar manejador de errores globales
        this.db.onerror = (event) => {
          console.error('❌ Error en IndexedDB:', event.target.error);
        };
        
        resolve(this.db);
      };

      request.onupgradeneeded = (event) => {
        const db = event.target.result;

        // Store para registros generales
        if (!db.objectStoreNames.contains(REGISTROS_STORE)) {
          const registrosStore = db.createObjectStore(REGISTROS_STORE, {
            keyPath: 'id',
            autoIncrement: true
          });
          registrosStore.createIndex('timestamp', 'timestamp', { unique: false });
          registrosStore.createIndex('usuario_id', 'usuario_id', { unique: false });
        }

        // Store para asistencias (entrada/salida)
        if (!db.objectStoreNames.contains(ASISTENCIAS_STORE)) {
          const asistenciasStore = db.createObjectStore(ASISTENCIAS_STORE, {
            keyPath: 'id',
            autoIncrement: true
          });
          asistenciasStore.createIndex('timestamp', 'timestamp', { unique: false });
          asistenciasStore.createIndex('usuario_id', 'usuario_id', { unique: false });
          asistenciasStore.createIndex('tipo', 'tipo', { unique: false }); // 'entrada' o 'salida'
        }

        console.log('✅ Estructura de base de datos offline creada');
      };
    });
  }

  /**
   * Convierte un archivo a base64 para almacenamiento
   */
  async fileToBase64(file) {
    if (!file) return null;
    
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = (error) => reject(error);
      reader.readAsDataURL(file);
    });
  }

  /**
   * Convierte base64 de vuelta a File
   */
  base64ToFile(base64String, filename, mimeType) {
    if (!base64String) return null;
    
    try {
      // Separar el tipo de datos del contenido base64
      const arr = base64String.split(',');
      const mime = arr[0].match(/:(.*?);/)[1] || mimeType;
      const bstr = atob(arr[1]);
      let n = bstr.length;
      const u8arr = new Uint8Array(n);
      
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      
      return new File([u8arr], filename, { type: mime });
    } catch (error) {
      console.error('Error convirtiendo base64 a archivo:', error);
      return null;
    }
  }

  /**
   * Guarda un registro general offline
   */
  async guardarRegistroOffline(usuarioId, latitud, longitud, descripcion, archivo) {
    try {
      await this.initDB();
      
      // Convertir archivo a base64 si existe
      const fotoBase64 = archivo ? await this.fileToBase64(archivo) : null;
      
      const registro = {
        usuario_id: usuarioId,
        latitud,
        longitud,
        descripcion,
        foto_base64: fotoBase64,
        foto_filename: archivo ? archivo.name : null,
        foto_type: archivo ? archivo.type : null,
        timestamp: new Date().toISOString(),
        tipo: 'registro_general'
      };

      const transaction = this.db.transaction([REGISTROS_STORE], 'readwrite');
      const store = transaction.objectStore(REGISTROS_STORE);
      
      return new Promise((resolve, reject) => {
        const request = store.add(registro);
        
        request.onsuccess = () => {
          console.log('✅ Registro guardado offline con ID:', request.result);
          resolve(request.result);
        };
        
        request.onerror = () => {
          console.error('❌ Error guardando registro offline:', request.error);
          reject(request.error);
        };
      });
    } catch (error) {
      console.error('❌ Error en guardarRegistroOffline:', error);
      throw error;
    }
  }

  /**
   * Guarda una asistencia (entrada/salida) offline
   */
  async guardarAsistenciaOffline(usuarioId, tipo, latitud, longitud, descripcion, archivo) {
    try {
      console.log(`📝 Intentando guardar asistencia ${tipo} offline para usuario ${usuarioId}`);
      
      // Verificar que la DB esté lista
      if (!this.db) {
        console.log('⚠️ DB no inicializada, inicializando...');
        await this.initDB();
      }
      
      if (!this.db) {
        throw new Error('No se pudo inicializar la base de datos');
      }
      
      // Verificar que el store existe
      if (!this.db.objectStoreNames.contains(ASISTENCIAS_STORE)) {
        console.error(`❌ Store ${ASISTENCIAS_STORE} no existe`);
        throw new Error(`Store ${ASISTENCIAS_STORE} no existe en la base de datos`);
      }
      
      console.log('✅ Base de datos verificada, procediendo a guardar asistencia');
      
      // Convertir archivo a base64 si existe
      const fotoBase64 = archivo ? await this.fileToBase64(archivo) : null;
      
      const asistencia = {
        usuario_id: usuarioId,
        tipo, // 'entrada' o 'salida'
        latitud,
        longitud,
        descripcion,
        foto_base64: fotoBase64,
        foto_filename: archivo ? archivo.name : null,
        foto_type: archivo ? archivo.type : null,
        timestamp: new Date().toISOString(),
        fecha: new Date().toISOString().split('T')[0] // YYYY-MM-DD
      };

      console.log('💾 Datos de asistencia preparados:', {
        usuario_id: asistencia.usuario_id,
        tipo: asistencia.tipo,
        timestamp: asistencia.timestamp,
        tiene_foto: !!asistencia.foto_base64
      });

      const transaction = this.db.transaction([ASISTENCIAS_STORE], 'readwrite');
      const store = transaction.objectStore(ASISTENCIAS_STORE);
      
      return new Promise((resolve, reject) => {
        const request = store.add(asistencia);
        
        request.onsuccess = () => {
          console.log(`✅ Asistencia ${tipo} guardada offline con ID:`, request.result);
          resolve(request.result);
        };
        
        request.onerror = () => {
          console.error(`❌ Error guardando asistencia ${tipo} offline:`, request.error);
          reject(request.error);
        };
        
        transaction.onerror = () => {
          console.error(`❌ Error en transacción de asistencia ${tipo}:`, transaction.error);
          reject(transaction.error);
        };
        
        transaction.onabort = () => {
          console.error(`❌ Transacción abortada para asistencia ${tipo}`);
          reject(new Error('Transacción abortada'));
        };
      });
    } catch (error) {
      console.error('❌ Error en guardarAsistenciaOffline:', error);
      throw error;
    }
  }

  /**
   * Obtiene todos los registros pendientes de envío
   */
  async obtenerRegistrosPendientes() {
    try {
      await this.initDB();
      
      const transaction = this.db.transaction([REGISTROS_STORE], 'readonly');
      const store = transaction.objectStore(REGISTROS_STORE);
      
      return new Promise((resolve, reject) => {
        const request = store.getAll();
        
        request.onsuccess = () => {
          resolve(request.result || []);
        };
        
        request.onerror = () => {
          reject(request.error);
        };
      });
    } catch (error) {
      console.error('❌ Error obteniendo registros pendientes:', error);
      return [];
    }
  }

  /**
   * Obtiene todas las asistencias pendientes de envío
   */
  async obtenerAsistenciasPendientes() {
    try {
      await this.initDB();
      
      const transaction = this.db.transaction([ASISTENCIAS_STORE], 'readonly');
      const store = transaction.objectStore(ASISTENCIAS_STORE);
      
      return new Promise((resolve, reject) => {
        const request = store.getAll();
        
        request.onsuccess = () => {
          resolve(request.result || []);
        };
        
        request.onerror = () => {
          reject(request.error);
        };
      });
    } catch (error) {
      console.error('❌ Error obteniendo asistencias pendientes:', error);
      return [];
    }
  }

  /**
   * Elimina un registro después de enviarlo exitosamente
   */
  async eliminarRegistro(id) {
    try {
      await this.initDB();
      
      const transaction = this.db.transaction([REGISTROS_STORE], 'readwrite');
      const store = transaction.objectStore(REGISTROS_STORE);
      
      return new Promise((resolve, reject) => {
        const request = store.delete(id);
        
        request.onsuccess = () => {
          console.log('✅ Registro eliminado después del envío exitoso:', id);
          resolve();
        };
        
        request.onerror = () => {
          reject(request.error);
        };
      });
    } catch (error) {
      console.error('❌ Error eliminando registro:', error);
      throw error;
    }
  }

  /**
   * Elimina una asistencia después de enviarla exitosamente
   */
  async eliminarAsistencia(id) {
    try {
      await this.initDB();
      
      const transaction = this.db.transaction([ASISTENCIAS_STORE], 'readwrite');
      const store = transaction.objectStore(ASISTENCIAS_STORE);
      
      return new Promise((resolve, reject) => {
        const request = store.delete(id);
        
        request.onsuccess = () => {
          console.log('✅ Asistencia eliminada después del envío exitoso:', id);
          resolve();
        };
        
        request.onerror = () => {
          reject(request.error);
        };
      });
    } catch (error) {
      console.error('❌ Error eliminando asistencia:', error);
      throw error;
    }
  }

  /**
   * Cuenta el total de elementos pendientes
   */
  async contarPendientes() {
    try {
      const registros = await this.obtenerRegistrosPendientes();
      const asistencias = await this.obtenerAsistenciasPendientes();
      
      return {
        registros: registros.length,
        asistencias: asistencias.length,
        total: registros.length + asistencias.length
      };
    } catch (error) {
      console.error('❌ Error contando pendientes:', error);
      return { registros: 0, asistencias: 0, total: 0 };
    }
  }

  /**
   * Limpia todos los registros offline (solo usar en casos de emergencia)
   */
  async limpiarTodo() {
    try {
      await this.initDB();
      
      const transaction = this.db.transaction([REGISTROS_STORE, ASISTENCIAS_STORE], 'readwrite');
      
      await Promise.all([
        new Promise((resolve, reject) => {
          const request = transaction.objectStore(REGISTROS_STORE).clear();
          request.onsuccess = () => resolve();
          request.onerror = () => reject(request.error);
        }),
        new Promise((resolve, reject) => {
          const request = transaction.objectStore(ASISTENCIAS_STORE).clear();
          request.onsuccess = () => resolve();
          request.onerror = () => reject(request.error);
        })
      ]);
      
      console.log('✅ Todos los datos offline han sido limpiados');
    } catch (error) {
      console.error('❌ Error limpiando datos offline:', error);
      throw error;
    }
  }
}

// Crear instancia singleton
const offlineService = new OfflineService();

export default offlineService;
