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
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION);

      request.onerror = () => {
        console.error('❌ Error al abrir la base de datos offline');
        reject(request.error);
      };

      request.onsuccess = () => {
        this.db = request.result;
        console.log('✅ Base de datos offline inicializada');
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
   * @param {string} base64String - Cadena base64 con datos de la imagen
   * @param {string} filename - Nombre del archivo a crear
   * @param {string} mimeType - Tipo MIME por defecto si no se puede extraer de base64
   * @returns {File|null} - Archivo creado o null si hay error
   */
  base64ToFile(base64String, filename, mimeType = 'image/jpeg') {
    if (!base64String) {
      console.error('❌ base64ToFile: String base64 vacío o nulo');
      return null;
    }
    
    try {
      console.log(`🔄 Convirtiendo imagen base64 a File (nombre: ${filename})`);
      
      // Verificar formato correcto del base64 (debe tener la estructura data:mime;base64,DATOS)
      if (!base64String.includes('base64,')) {
        console.error('❌ base64ToFile: Formato de base64 inválido, debe incluir "base64,"');
        // Intentar reparar el formato si es posible
        if (!base64String.startsWith('data:')) {
          base64String = `data:${mimeType};base64,${base64String}`;
          console.log('⚠️ Reparando formato de base64, añadiendo encabezado');
        }
      }
      
      // Separar el tipo de datos del contenido base64
      const arr = base64String.split(',');
      let mime = mimeType;
      let b64data = '';
      
      if (arr.length > 1) {
        try {
          // Extraer MIME del encabezado data:tipo/subtipo;base64
          const mimeMatch = arr[0].match(/:(.*?);/);
          if (mimeMatch && mimeMatch.length > 1) {
            mime = mimeMatch[1];
          }
          b64data = arr[1];
        } catch (error) {
          console.error('❌ Error extrayendo MIME del base64:', error);
          b64data = arr[1] || base64String; // Usar la parte de datos o todo si no hay coma
        }
      } else {
        // No tiene formato correcto, asumir que es solo datos
        b64data = base64String;
        console.warn('⚠️ Base64 no tiene formato estándar, asumiendo solo datos');
      }
      
      // Convertir base64 a bytes
      try {
        const bstr = atob(b64data);
        let n = bstr.length;
        const u8arr = new Uint8Array(n);
        
        while (n--) {
          u8arr[n] = bstr.charCodeAt(n);
        }
        
        // Crear y devolver el archivo
        const file = new File([u8arr], filename, { type: mime });
        console.log(`✅ Archivo creado exitosamente: ${filename}, tamaño: ${file.size} bytes, tipo: ${mime}`);
        return file;
      } catch (error) {
        console.error('❌ Error en decodificación base64:', error);
        // Intento de recuperación para base64 mal formateados
        try {
          // Limpiar caracteres no válidos y reintentar
          const cleanBase64 = b64data.replace(/[^A-Za-z0-9+/=]/g, '');
          const bstr = atob(cleanBase64);
          let n = bstr.length;
          const u8arr = new Uint8Array(n);
          
          while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
          }
          
          const file = new File([u8arr], filename, { type: mime });
          console.log(`✅ Archivo recuperado tras limpieza: ${filename}, tamaño: ${file.size} bytes`);
          return file;
        } catch (err) {
          console.error('❌ Falló intento de recuperación de base64:', err);
          return null;
        }
      }
    } catch (error) {
      console.error('❌ Error general convirtiendo base64 a archivo:', error);
      return null;
    }
  }

  /**
   * Guarda un registro general offline
   * @param {number} usuarioId - ID del usuario
   * @param {string} latitud - Latitud de la ubicación
   * @param {string} longitud - Longitud de la ubicación
   * @param {string} descripcion - Descripción del registro
   * @param {File} archivo - Archivo de imagen adjunto
   * @param {string} tipoActividad - Tipo de actividad ('campo' o 'gabinete')
   * @returns {Promise<number>} - ID del registro guardado en IndexedDB
   */
  async guardarRegistroOffline(usuarioId, latitud, longitud, descripcion, archivo, tipoActividad = 'campo', timestampCDMX = null) {
    try {
      console.log('🔄 Guardando registro offline para usuario ID:', usuarioId);
      await this.initDB();
      
      // Convertir archivo a base64 si existe
      let fotoBase64 = null;
      if (archivo) {
        console.log(`🖼️ Convirtiendo foto a base64 (${archivo.name}, ${archivo.size} bytes)...`);
        try {
          fotoBase64 = await this.fileToBase64(archivo);
          console.log(`✅ Foto convertida exitosamente. Longitud base64: ${fotoBase64.length} caracteres`);
          
          // Verificar que el base64 sea válido
          if (!fotoBase64 || fotoBase64.length < 100) {
            console.error('⚠️ La conversión base64 generó datos sospechosos, verificando...');
            if (!fotoBase64.includes('base64') && !fotoBase64.includes(',')) {
              console.warn('⚠️ El string base64 no tiene el formato esperado, intentando reparar...');
              fotoBase64 = `data:${archivo.type};base64,${fotoBase64}`;
            }
          }
        } catch (err) {
          console.error('❌ Error al convertir imagen a base64:', err);
          fotoBase64 = null; // Continuar sin foto
        }
      }
      
      // MEJORA: Crear registro con más metadatos para identificación
      const registro = {
        usuario_id: usuarioId,
        latitud,
        longitud,
        descripcion,
        tipo_actividad: tipoActividad, // Nuevo: agregar tipo de actividad
        foto_base64: fotoBase64,
        foto_filename: archivo ? archivo.name : null,
        foto_type: archivo ? archivo.type : null,
        timestamp: timestampCDMX || new Date().toISOString(), // Usar timestamp CDMX si se proporciona
        sync_timestamp: null, // Se completará cuando se sincronice
        tipo: 'actividad', // Especificar explícitamente que es un registro de actividad
        fecha_creacion: new Date().toISOString(),
        intentos: 0,
        estado: 'pendiente',
        origen: 'pwa_super',
        id_cliente: `reg_${Date.now()}_${Math.floor(Math.random() * 1000)}` // ID único para referencia
      };

      const transaction = this.db.transaction([REGISTROS_STORE], 'readwrite');
      const store = transaction.objectStore(REGISTROS_STORE);
      
      return new Promise((resolve, reject) => {
        const request = store.add(registro);
        
        request.onsuccess = () => {
          const id = request.result;
          console.log(`✅ Registro guardado offline con ID: ${id}`);
          
          // MEJORA: Verificar que el registro realmente se guardó para confirmar
          const getRequest = store.get(id);
          getRequest.onsuccess = () => {
            if (getRequest.result) {
              console.log(`✅ Verificación: Registro ID ${id} guardado correctamente en IndexedDB`);
              resolve(id);
            } else {
              console.error(`❌ Verificación falló: No se encontró el registro ID ${id} recién guardado`);
              reject(new Error('Error de verificación: registro no encontrado después de guardar'));
            }
          };
          getRequest.onerror = () => {
            console.warn(`⚠️ No se pudo verificar el registro guardado, pero parece haberse guardado con ID ${id}`);
            resolve(id); // Resolver de todos modos
          };
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
      await this.initDB();
      
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
        timestamp: new Date().toISOString(), // Hora de creación offline
        sync_timestamp: null, // Se completará cuando se sincronice
        fecha: new Date().toISOString().split('T')[0] // YYYY-MM-DD
      };

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
      });
    } catch (error) {
      console.error('❌ Error en guardarAsistenciaOffline:', error);
      throw error;
    }
  }

  /**
   * Obtiene todos los registros pendientes de envío
   * @param {boolean} logDetails - Si es true, imprime detalles de los registros encontrados para debugging
   * @returns {Promise<Array>} - Arreglo de registros pendientes
   */
  async obtenerRegistrosPendientes(logDetails = false) {
    try {
      // Asegurar que la BD esté inicializada
      if (!this.db) {
        console.log('⚠️ Base de datos no inicializada, inicializando ahora...');
        await this.initDB();
      }
      
      console.log('🔍 Buscando registros pendientes en IndexedDB...');
      
      const transaction = this.db.transaction([REGISTROS_STORE], 'readonly');
      const store = transaction.objectStore(REGISTROS_STORE);
      
      return new Promise((resolve, reject) => {
        const request = store.getAll();
        
        request.onsuccess = () => {
          const registros = request.result || [];
          
          if (logDetails) {
            console.log(`✅ Encontrados ${registros.length} registros pendientes:`);
            registros.forEach((r, idx) => {
              console.log(`📝 Registro #${idx+1} (ID: ${r.id}): Tipo=${r.tipo || 'actividad'}, Timestamp=${r.timestamp}, Usuario=${r.usuario_id}`);
            });
          } else {
            console.log(`✅ Encontrados ${registros.length} registros pendientes`);
          }
          
          resolve(registros);
        };
        
        request.onerror = () => {
          console.error('❌ Error en getAll de registros pendientes:', request.error);
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
   * Actualiza el timestamp de sincronización de un registro
   */
  async actualizarTimestampSincronizacion(id, tipo = 'registro') {
    try {
      await this.initDB();
      
      const storeName = tipo === 'asistencia' ? ASISTENCIAS_STORE : REGISTROS_STORE;
      const transaction = this.db.transaction([storeName], 'readwrite');
      const store = transaction.objectStore(storeName);
      
      return new Promise((resolve, reject) => {
        // Primero obtener el registro
        const getRequest = store.get(id);
        
        getRequest.onsuccess = () => {
          const record = getRequest.result;
          if (record) {
            // Actualizar con timestamp de sincronización
            record.sync_timestamp = new Date().toISOString();
            
            // Guardar el registro actualizado
            const putRequest = store.put(record);
            
            putRequest.onsuccess = () => {
              console.log(`✅ Timestamp de sincronización actualizado para ${tipo} ID:`, id);
              resolve(record);
            };
            
            putRequest.onerror = () => {
              reject(putRequest.error);
            };
          } else {
            reject(new Error(`${tipo} con ID ${id} no encontrado`));
          }
        };
        
        getRequest.onerror = () => {
          reject(getRequest.error);
        };
      });
    } catch (error) {
      console.error(`❌ Error actualizando timestamp de sincronización para ${tipo}:`, error);
      throw error;
    }
  }

  /**
   * Actualiza el estado de sincronización con información adicional
   * @param {number} id - ID del registro o asistencia
   * @param {string} tipo - 'registro' o 'asistencia'
   * @param {object} datos - Datos adicionales para actualizar (intentos, errores, etc.)
   */
  async actualizarEstadoSincronizacion(id, tipo = 'registro', datos = {}) {
    try {
      await this.initDB();
      
      const storeName = tipo === 'asistencia' ? ASISTENCIAS_STORE : REGISTROS_STORE;
      const transaction = this.db.transaction([storeName], 'readwrite');
      const store = transaction.objectStore(storeName);
      
      return new Promise((resolve, reject) => {
        // Primero obtener el registro
        const getRequest = store.get(id);
        
        getRequest.onsuccess = () => {
          const record = getRequest.result;
          if (record) {
            // Actualizar el registro con los nuevos datos
            const updatedRecord = {
              ...record,
              ...datos,
              ultima_actualizacion: new Date().toISOString()
            };
            
            // Guardar el registro actualizado
            const putRequest = store.put(updatedRecord);
            
            putRequest.onsuccess = () => {
              console.log(`✅ Estado de sincronización actualizado para ${tipo} ID:`, id);
              resolve(updatedRecord);
            };
            
            putRequest.onerror = () => {
              reject(putRequest.error);
            };
          } else {
            reject(new Error(`${tipo} con ID ${id} no encontrado`));
          }
        };
        
        getRequest.onerror = () => {
          reject(getRequest.error);
        };
      });
    } catch (error) {
      console.error(`❌ Error actualizando estado de sincronización para ${tipo}:`, error);
      throw error;
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
   * @param {boolean} forceRefresh - Si es true, fuerza una consulta fresca a la base de datos evitando caché
   * @returns {Promise<Object>} - Objeto con conteo de registros, asistencias y total
   */
  async contarPendientes(forceRefresh = false) {
    try {
      // Si se fuerza actualización, renovamos la conexión con IndexedDB
      if (forceRefresh && this.db) {
        console.log('🔄 Forzando actualización de conteo de pendientes...');
        // Cerrar y reabrir la conexión para asegurar datos frescos
        this.db.close();
        this.db = null;
        await this.initDB();
      }
      
      const registros = await this.obtenerRegistrosPendientes();
      const asistencias = await this.obtenerAsistenciasPendientes();
      
      const resultado = {
        registros: registros.length,
        asistencias: asistencias.length,
        total: registros.length + asistencias.length
      };
      
      console.log('📊 Conteo actualizado de pendientes:', resultado);
      return resultado;
    } catch (error) {
      console.error('❌ Error contando pendientes:', error);
      return { registros: 0, asistencias: 0, total: 0 };
    }
  }

  /**
   * Obtiene información detallada de registros pendientes para debugging
   */
  async obtenerResumenPendientes() {
    try {
      const registros = await this.obtenerRegistrosPendientes();
      const asistencias = await this.obtenerAsistenciasPendientes();
      
      return {
        registros: {
          total: registros.length,
          items: registros.map(r => ({
            id: r.id,
            usuario_id: r.usuario_id,
            timestamp: r.timestamp,
            sync_timestamp: r.sync_timestamp,
            tipo: r.tipo,
            tiene_foto: !!r.foto_base64
          }))
        },
        asistencias: {
          total: asistencias.length,
          items: asistencias.map(a => ({
            id: a.id,
            usuario_id: a.usuario_id,
            tipo: a.tipo,
            timestamp: a.timestamp,
            sync_timestamp: a.sync_timestamp,
            fecha: a.fecha,
            tiene_foto: !!a.foto_base64
          }))
        }
      };
    } catch (error) {
      console.error('❌ Error obteniendo resumen de pendientes:', error);
      return { registros: { total: 0, items: [] }, asistencias: { total: 0, items: [] } };
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
