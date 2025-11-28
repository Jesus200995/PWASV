/**
 * Servicio de sincronización para enviar datos offline cuando se recupera la conexión
 * MEJORAS PARA ANDROID: Sistema de reintentos robusto, timeouts adaptativos,
 * compresión de imágenes y mejor manejo de conexiones inestables
 */
import offlineService from './offlineService.js';
import asistenciasService from './asistenciasService.js';
import { API_URL, checkInternetConnection } from '../utils/network.js';
import axios from 'axios';

// Configuración para reintentos y timeouts adaptativos (especialmente para Android)
const SYNC_CONFIG = {
  maxRetries: 3,                    // Número máximo de reintentos por registro
  baseTimeout: 30000,               // Timeout base de 30 segundos
  maxTimeout: 120000,               // Timeout máximo de 2 minutos
  retryDelayBase: 2000,             // Delay base entre reintentos (2 segundos)
  maxImageSize: 500 * 1024,         // Máximo tamaño de imagen sin comprimir (500KB)
  compressionQuality: 0.5,          // Calidad de compresión para imágenes grandes
  chunkSize: 1,                     // Procesar de 1 en 1 para mayor estabilidad
  connectionCheckBeforeEach: true,  // Verificar conexión antes de cada envío
};

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
    // Cada 2 minutos verificamos si hay conexión y pendientes para sincronizar (más frecuente para mejor UX)
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
    }, 2 * 60 * 1000); // 2 minutos (más frecuente para sincronizar más rápido)
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
   * Comprime una imagen base64 si excede el tamaño máximo (para Android y conexiones lentas)
   * @param {string} base64String - String base64 de la imagen
   * @param {number} maxSizeKB - Tamaño máximo en KB (default 400KB)
   * @param {number} quality - Calidad de compresión (0-1, default 0.5)
   * @returns {Promise<string>} - String base64 comprimido
   */
  async comprimirImagenBase64(base64String, maxSizeKB = 400, quality = 0.5) {
    return new Promise((resolve, reject) => {
      try {
        // Calcular tamaño actual aproximado en KB
        const sizeKB = (base64String.length * 3/4) / 1024;
        console.log(`🖼️ Tamaño actual de imagen: ${sizeKB.toFixed(2)} KB`);
        
        // Si ya está por debajo del límite, devolver sin cambios
        if (sizeKB <= maxSizeKB) {
          console.log('✅ Imagen dentro del límite, no necesita compresión');
          resolve(base64String);
          return;
        }
        
        console.log(`⚠️ Imagen excede ${maxSizeKB}KB, comprimiendo...`);
        
        const img = new Image();
        img.onload = () => {
          // Calcular dimensiones de redimensionamiento
          let width = img.width;
          let height = img.height;
          const maxDimension = 1024; // Máximo 1024px en cualquier dimensión
          
          if (width > maxDimension || height > maxDimension) {
            if (width > height) {
              height = Math.floor(height * (maxDimension / width));
              width = maxDimension;
            } else {
              width = Math.floor(width * (maxDimension / height));
              height = maxDimension;
            }
          }
          
          // Crear canvas para compresión
          const canvas = document.createElement('canvas');
          canvas.width = width;
          canvas.height = height;
          const ctx = canvas.getContext('2d');
          
          // Dibujar imagen redimensionada
          ctx.drawImage(img, 0, 0, width, height);
          
          // Convertir a base64 con compresión
          const compressedBase64 = canvas.toDataURL('image/jpeg', quality);
          const newSizeKB = (compressedBase64.length * 3/4) / 1024;
          
          console.log(`✅ Imagen comprimida: ${sizeKB.toFixed(2)}KB → ${newSizeKB.toFixed(2)}KB (${((1 - newSizeKB/sizeKB) * 100).toFixed(1)}% reducción)`);
          
          resolve(compressedBase64);
        };
        
        img.onerror = (err) => {
          console.error('❌ Error cargando imagen para compresión:', err);
          // En caso de error, devolver la imagen original
          resolve(base64String);
        };
        
        img.src = base64String;
      } catch (error) {
        console.error('❌ Error en compresión de imagen:', error);
        // En caso de error, devolver la imagen original
        resolve(base64String);
      }
    });
  }

  /**
   * Envía un registro general al servidor con sistema de reintentos para Android
   * @param {Object} registro - Objeto con datos del registro a enviar
   * @param {number} intentoActual - Número de intento actual (para reintentos)
   * @returns {Promise<Object>} - Respuesta del servidor
   */
  async enviarRegistro(registro, intentoActual = 1) {
    const maxReintentos = SYNC_CONFIG.maxRetries;
    const tiempoEspera = SYNC_CONFIG.retryDelayBase * intentoActual; // Incrementa con cada intento
    const timeoutActual = Math.min(SYNC_CONFIG.baseTimeout * intentoActual, SYNC_CONFIG.maxTimeout);
    
    console.log(`📤 [Intento ${intentoActual}/${maxReintentos}] Enviando registro offline ID: ${registro.id}`);
    console.log(`⏱️ Timeout configurado: ${timeoutActual/1000}s`);
    
    try {
      // ANDROID FIX: Verificar conexión antes de cada envío individual
      if (SYNC_CONFIG.connectionCheckBeforeEach && intentoActual > 1) {
        console.log('🔍 Verificando conexión antes del reintento...');
        const tieneConexion = await checkInternetConnection(5000);
        if (!tieneConexion) {
          console.warn('⚠️ Sin conexión detectada, abortando reintento');
          throw new Error('Sin conexión a Internet');
        }
        // Pequeña pausa antes del reintento
        await new Promise(resolve => setTimeout(resolve, tiempoEspera));
      }
      
      console.log('🕐 Timestamp original:', registro.timestamp);
      console.log('📊 Datos del registro:', {
        id: registro.id,
        usuario_id: registro.usuario_id,
        tipo: registro.tipo || 'actividad',
        tiene_foto: !!registro.foto_base64,
        timestamp: registro.timestamp,
        categoria: registro.categoria_actividad
      });
      
      // Validar datos básicos
      if (!registro.usuario_id || !registro.latitud || !registro.longitud) {
        console.error('❌ Registro incompleto, faltan datos básicos');
        throw new Error('Registro incompleto: faltan usuario_id, latitud o longitud');
      }
      
      // MEJORA: Validar y asignar valores por defecto para campos obligatorios del backend
      const tipoActividad = registro.tipo_actividad || 'campo';
      let categoriaActividad = registro.categoria_actividad;
      
      // Si categoria_actividad está vacío o no es válido, usar valor por defecto
      const categoriasValidas = [
        'Acompañamiento técnico',
        'Productivas directas',
        'Ahorro y trámites financieros',
        'Capacitación / talleres / cursos',
        'Difusión y comunicación',
        'Eventos comunitarios / ferias / tianguis',
        'Reuniones y asambleas',
        'Trabajo administrativo y captura',
        'Viveros y biofábricas',
        'Otro'
      ];
      
      if (!categoriaActividad || !categoriasValidas.includes(categoriaActividad)) {
        console.warn(`⚠️ Categoría de actividad vacía o inválida: '${categoriaActividad}', usando valor por defecto`);
        // Intentar inferir del tipo de actividad o usar valor genérico
        categoriaActividad = tipoActividad === 'gabinete' ? 'Trabajo administrativo y captura' : 'Acompañamiento técnico';
        console.log(`📝 Categoría asignada automáticamente: ${categoriaActividad}`);
      }
      
      // Obtener timestamp de sincronización (momento actual)
      const syncTimestamp = new Date().toISOString();
      await offlineService.actualizarTimestampSincronizacion(registro.id, 'registro');
      
      // Crear FormData para el envío
      const formData = new FormData();
      formData.append('usuario_id', registro.usuario_id.toString());
      formData.append('latitud', registro.latitud.toString());
      formData.append('longitud', registro.longitud.toString());
      formData.append('descripcion', registro.descripcion || '');
      formData.append('tipo_actividad', tipoActividad);
      
      // Agregar campos de categoría de actividad (ahora siempre tiene valor válido)
      formData.append('categoria_actividad', categoriaActividad);
      if (categoriaActividad === 'Otro' && registro.categoria_actividad_otro) {
        formData.append('categoria_actividad_otro', registro.categoria_actividad_otro);
      }
      
      // Asegurar que se envía como tipo actividad explícitamente
      formData.append('tipo', 'actividad');
      
      // Usar el timestamp original (hora de creación offline) no el de sincronización
      formData.append('timestamp_offline', registro.timestamp);
      
      // Añadir campos adicionales para que el backend identifique correctamente los datos offline
      formData.append('es_registro_offline', 'true');
      formData.append('sync_timestamp', syncTimestamp);
      formData.append('origen_sync', 'pwa_super');
      formData.append('id_offline', registro.id.toString());
      
      console.log('📤 Datos del formulario preparados correctamente');
      
      // ANDROID FIX: Procesar foto con compresión si es necesario
      let archivoAdjunto = false;
      if (registro.foto_base64) {
        console.log('🖼️ Procesando imagen base64...');
        console.log(`🔍 Longitud original del string base64: ${registro.foto_base64.length}`);
        
        // Verificar formato válido de base64
        let fotoBase64Procesada = registro.foto_base64;
        
        // ANDROID FIX: Comprimir imagen si es muy grande para evitar timeouts
        try {
          fotoBase64Procesada = await this.comprimirImagenBase64(registro.foto_base64, 400, 0.5);
        } catch (compressError) {
          console.warn('⚠️ Error en compresión, usando imagen original:', compressError);
          fotoBase64Procesada = registro.foto_base64;
        }
        
        // ANDROID FIX: Asegurar formato correcto del base64
        if (!fotoBase64Procesada.includes('base64,') && !fotoBase64Procesada.startsWith('data:')) {
          console.log('⚠️ Base64 sin cabecera, agregando formato estándar');
          fotoBase64Procesada = `data:image/jpeg;base64,${fotoBase64Procesada}`;
        }
        
        const archivo = offlineService.base64ToFile(
          fotoBase64Procesada,
          registro.foto_filename || `foto_${registro.id}_${Date.now()}.jpg`,
          'image/jpeg'
        );
        
        if (archivo && archivo.size > 0) {
          console.log(`✅ Imagen convertida: ${archivo.name}, ${(archivo.size/1024).toFixed(2)}KB`);
          formData.append('foto', archivo);
          archivoAdjunto = true;
        } else {
          console.error('❌ Error: Archivo de imagen vacío o nulo');
          // ANDROID FIX: Crear imagen placeholder para evitar error de foto requerida
          console.log('🔄 Creando imagen placeholder para evitar error...');
          const placeholderBlob = this.crearImagenPlaceholder();
          if (placeholderBlob) {
            formData.append('foto', placeholderBlob, `placeholder_${registro.id}.jpg`);
            archivoAdjunto = true;
            console.log('✅ Imagen placeholder creada exitosamente');
          }
        }
      } else {
        console.warn('⚠️ Registro sin imagen base64');
        // ANDROID FIX: Crear imagen placeholder
        console.log('🔄 Creando imagen placeholder para registro sin foto...');
        const placeholderBlob = this.crearImagenPlaceholder();
        if (placeholderBlob) {
          formData.append('foto', placeholderBlob, `placeholder_${registro.id}.jpg`);
          archivoAdjunto = true;
        }
      }
      
      console.log(`📤 Enviando registro al backend${archivoAdjunto ? ' con foto' : ' SIN foto'}`);
      
      // ANDROID FIX: Configuración de axios optimizada para móviles
      const response = await axios.post(`${API_URL}/registro`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-Offline-Sync': 'true',
          'X-Sync-Timestamp': syncTimestamp,
          'X-Offline-ID': registro.id.toString(),
          'X-Registro-Tipo': 'actividad',
          'X-Retry-Count': intentoActual.toString(),
          'X-Device-Type': this.detectarTipoDispositivo(),
        },
        timeout: timeoutActual,
        maxContentLength: Infinity,
        maxBodyLength: Infinity,
        // ANDROID FIX: Deshabilitar transformaciones que pueden causar problemas
        transformRequest: [(data) => data],
      });
      
      // Verificar que la respuesta sea válida
      if (!response || !response.data) {
        console.error('❌ El servidor no devolvió una respuesta válida');
        throw new Error('Respuesta del servidor inválida');
      }
      
      console.log('✅ Registro enviado exitosamente:', response.data);
      return response.data;
      
    } catch (error) {
      console.error(`❌ Error en intento ${intentoActual}/${maxReintentos}:`, error.message);
      
      // Verificar errores que no requieren reintento
      if (error.response && error.response.status === 400) {
        const errorDetail = error.response.data?.detail || '';
        
        // Registro duplicado - considerar exitoso
        if (errorDetail.includes('ya existe') || 
            errorDetail.includes('duplicado') || 
            errorDetail.includes('duplicate') || 
            errorDetail.includes('Ya registrado')) {
          console.log('ℹ️ Registro ya existe en el servidor, marcando como enviado');
          return { mensaje: 'Registro ya existía en el servidor', duplicado: true };
        }
        
        // MEJORA: Manejar errores de campos obligatorios como categoria_actividad o tipo_actividad
        if (errorDetail.includes('categoria_actividad') || 
            errorDetail.includes('tipo_actividad') ||
            errorDetail.includes('field required')) {
          console.error('❌ Error de campo obligatorio:', errorDetail);
          console.log('🔄 Intentando corregir y reenviar con valores por defecto...');
          
          // Si es primer intento, intentar con valores por defecto
          if (intentoActual === 1) {
            // Modificar el registro con valores por defecto y reintentar
            const registroCorregido = {
              ...registro,
              tipo_actividad: registro.tipo_actividad || 'campo',
              categoria_actividad: registro.categoria_actividad || 'Acompañamiento técnico'
            };
            console.log('📝 Registro corregido:', registroCorregido);
            return this.enviarRegistro(registroCorregido, intentoActual + 1);
          }
        }
        
        // Error de validación - no reintentar
        console.error('❌ Error de validación del servidor:', errorDetail);
        throw new Error(`Error de validación: ${errorDetail}`);
      }
      
      // ANDROID FIX: Reintentar si es error de red/timeout y quedan intentos
      const esErrorDeRed = !error.response || error.code === 'ECONNABORTED' || 
                          error.code === 'ERR_NETWORK' || error.message.includes('timeout') ||
                          error.message.includes('Network Error');
      
      if (esErrorDeRed && intentoActual < maxReintentos) {
        console.log(`🔄 Error de red detectado, reintentando en ${tiempoEspera/1000}s...`);
        // Reintentar con incremento de intento
        return this.enviarRegistro(registro, intentoActual + 1);
      }
      
      // Log detallado del error final
      console.error('📄 Detalles completos del error final:');
      if (error.response) {
        console.error('- Status:', error.response.status);
        console.error('- Data:', JSON.stringify(error.response.data));
      } else if (error.request) {
        console.error('- Sin respuesta del servidor (timeout o error de red)');
        console.error('- Código de error:', error.code);
      } else {
        console.error('- Error de configuración:', error.message);
      }
      
      throw error;
    }
  }

  /**
   * Detecta el tipo de dispositivo para logging y diagnóstico
   * @returns {string} - Tipo de dispositivo (android, ios, desktop, unknown)
   */
  detectarTipoDispositivo() {
    const ua = navigator.userAgent.toLowerCase();
    if (ua.includes('android')) return 'android';
    if (ua.includes('iphone') || ua.includes('ipad')) return 'ios';
    if (ua.includes('windows') || ua.includes('macintosh') || ua.includes('linux')) return 'desktop';
    return 'unknown';
  }

  /**
   * Crea una imagen placeholder mínima cuando no hay foto disponible
   * @returns {Blob|null} - Blob de imagen placeholder o null si falla
   */
  crearImagenPlaceholder() {
    try {
      const canvas = document.createElement('canvas');
      canvas.width = 100;
      canvas.height = 100;
      const ctx = canvas.getContext('2d');
      
      // Fondo gris claro
      ctx.fillStyle = '#f0f0f0';
      ctx.fillRect(0, 0, 100, 100);
      
      // Texto indicando sin imagen
      ctx.fillStyle = '#999';
      ctx.font = '10px Arial';
      ctx.textAlign = 'center';
      ctx.fillText('Sin imagen', 50, 50);
      
      // Convertir a blob
      return new Promise((resolve) => {
        canvas.toBlob((blob) => {
          resolve(blob);
        }, 'image/jpeg', 0.5);
      });
    } catch (error) {
      console.error('❌ Error creando placeholder:', error);
      return null;
    }
  }

  /**
   * Envía una asistencia al servidor con sistema de reintentos para Android
   * @param {Object} asistencia - Objeto con datos de la asistencia
   * @param {number} intentoActual - Número de intento actual (para reintentos)
   * @returns {Promise<Object>} - Respuesta del servidor
   */
  async enviarAsistencia(asistencia, intentoActual = 1) {
    const maxReintentos = SYNC_CONFIG.maxRetries;
    const tiempoEspera = SYNC_CONFIG.retryDelayBase * intentoActual;
    const timeoutActual = Math.min(SYNC_CONFIG.baseTimeout * intentoActual, SYNC_CONFIG.maxTimeout);
    
    console.log(`📤 [Intento ${intentoActual}/${maxReintentos}] Enviando asistencia ${asistencia.tipo} offline ID: ${asistencia.id}`);
    console.log(`⏱️ Timeout configurado: ${timeoutActual/1000}s`);
    
    try {
      // ANDROID FIX: Verificar conexión antes de cada envío individual
      if (SYNC_CONFIG.connectionCheckBeforeEach && intentoActual > 1) {
        console.log('🔍 Verificando conexión antes del reintento...');
        const tieneConexion = await checkInternetConnection(5000);
        if (!tieneConexion) {
          console.warn('⚠️ Sin conexión detectada, abortando reintento');
          throw new Error('Sin conexión a Internet');
        }
        await new Promise(resolve => setTimeout(resolve, tiempoEspera));
      }
      
      console.log('🕐 Timestamp original:', asistencia.timestamp);
      
      // Validar datos básicos
      if (!asistencia.usuario_id || !asistencia.latitud || !asistencia.longitud) {
        console.error('❌ Asistencia incompleta, faltan datos básicos');
        throw new Error('Asistencia incompleta: faltan usuario_id, latitud o longitud');
      }
      
      // Obtener timestamp de sincronización (momento actual)
      const syncTimestamp = new Date().toISOString();
      await offlineService.actualizarTimestampSincronizacion(asistencia.id, 'asistencia');
      
      // Crear FormData para el envío
      const formData = new FormData();
      formData.append('usuario_id', asistencia.usuario_id.toString());
      formData.append('latitud', asistencia.latitud.toString());
      formData.append('longitud', asistencia.longitud.toString());
      formData.append('descripcion', asistencia.descripcion || '');
      
      // Usar el timestamp original (hora de creación offline) no el de sincronización
      formData.append('timestamp_offline', asistencia.timestamp);
      
      // Añadir campos adicionales para que el backend identifique correctamente los datos offline
      formData.append('es_asistencia_offline', 'true');
      formData.append('sync_timestamp', syncTimestamp);
      formData.append('origen_sync', 'pwa_super');
      formData.append('id_offline', asistencia.id.toString());
      formData.append('fecha_offline', asistencia.fecha || new Date().toISOString().split('T')[0]);
      
      console.log(`📤 Datos preparados para asistencia ${asistencia.tipo}`);
      
      // ANDROID FIX: Procesar foto con compresión si es necesario
      if (asistencia.foto_base64) {
        console.log('🖼️ Procesando imagen de asistencia...');
        
        let fotoBase64Procesada = asistencia.foto_base64;
        
        // Comprimir imagen si es muy grande
        try {
          fotoBase64Procesada = await this.comprimirImagenBase64(asistencia.foto_base64, 400, 0.5);
        } catch (compressError) {
          console.warn('⚠️ Error en compresión, usando imagen original:', compressError);
        }
        
        // Asegurar formato correcto del base64
        if (!fotoBase64Procesada.includes('base64,') && !fotoBase64Procesada.startsWith('data:')) {
          fotoBase64Procesada = `data:image/jpeg;base64,${fotoBase64Procesada}`;
        }
        
        const archivo = offlineService.base64ToFile(
          fotoBase64Procesada,
          asistencia.foto_filename || `${asistencia.tipo}_${asistencia.id}_${Date.now()}.jpg`,
          'image/jpeg'
        );
        
        if (archivo && archivo.size > 0) {
          console.log(`✅ Imagen de asistencia convertida: ${(archivo.size/1024).toFixed(2)}KB`);
          formData.append('foto', archivo);
        } else {
          console.warn('⚠️ Error convirtiendo imagen, creando placeholder...');
          const placeholder = await this.crearImagenPlaceholder();
          if (placeholder) {
            formData.append('foto', placeholder, `placeholder_${asistencia.tipo}_${asistencia.id}.jpg`);
          }
        }
      } else {
        console.log('📷 Asistencia sin foto, creando placeholder...');
        const placeholder = await this.crearImagenPlaceholder();
        if (placeholder) {
          formData.append('foto', placeholder, `placeholder_${asistencia.tipo}_${asistencia.id}.jpg`);
        }
      }
      
      // Configurar headers comunes para la petición - ANDROID FIX
      const requestConfig = {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-Offline-Sync': 'true',
          'X-Sync-Timestamp': syncTimestamp,
          'X-Offline-ID': asistencia.id.toString(),
          'X-Asistencia-Tipo': asistencia.tipo,
          'X-Retry-Count': intentoActual.toString(),
          'X-Device-Type': this.detectarTipoDispositivo(),
        },
        timeout: timeoutActual,
        maxContentLength: Infinity,
        maxBodyLength: Infinity,
        transformRequest: [(data) => data],
      };
      
      // Enviar según el tipo de asistencia
      let response;
      if (asistencia.tipo === 'entrada') {
        response = await asistenciasService.registrarEntrada(formData, requestConfig);
      } else if (asistencia.tipo === 'salida') {
        response = await asistenciasService.registrarSalida(formData, requestConfig);
      } else {
        throw new Error(`Tipo de asistencia desconocido: ${asistencia.tipo}`);
      }
      
      console.log(`✅ Asistencia ${asistencia.tipo} enviada exitosamente:`, response);
      return response;
      
    } catch (error) {
      console.error(`❌ Error en intento ${intentoActual}/${maxReintentos} de asistencia:`, error.message);
      
      // Verificar si es error de duplicado
      if (error.response && error.response.status === 400) {
        const errorDetail = error.response.data?.detail || error.message || '';
        
        if (errorDetail.includes('Ya existe') || 
            errorDetail.includes('ya registrada') ||
            errorDetail.includes('ya tiene registro')) {
          console.log(`ℹ️ Asistencia ${asistencia.tipo} ya existe en el servidor, marcando como enviada`);
          return { mensaje: `Asistencia ${asistencia.tipo} ya existía en el servidor`, duplicado: true };
        }
      }
      
      // ANDROID FIX: Reintentar si es error de red/timeout
      const esErrorDeRed = !error.response || error.code === 'ECONNABORTED' || 
                          error.code === 'ERR_NETWORK' || error.message.includes('timeout') ||
                          error.message.includes('Network Error');
      
      if (esErrorDeRed && intentoActual < maxReintentos) {
        console.log(`🔄 Error de red en asistencia, reintentando en ${tiempoEspera/1000}s...`);
        return this.enviarAsistencia(asistencia, intentoActual + 1);
      }
      
      // Log detallado del error final
      console.error('📄 Error final en envío de asistencia:');
      if (error.response) {
        console.error('- Status:', error.response.status);
        console.error('- Data:', JSON.stringify(error.response.data));
      } else {
        console.error('- Sin respuesta del servidor');
        console.error('- Código:', error.code);
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
