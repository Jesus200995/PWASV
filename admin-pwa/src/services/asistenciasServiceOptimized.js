// Servicio OPTIMIZADO para asistencias con técnicas Apple de performance
import axios from 'axios';
import { API_URL } from '../config/api.js';
import authService from './authService.js';

class AsistenciasServiceOptimized {
  constructor() {
    // Cache en memoria para resultados
    this.cache = new Map();
    this.cacheTimeout = 30000; // 30 segundos
    
    // Queue para request batching
    this.requestQueue = [];
    this.batchTimeout = null;
    
    // AbortController para cancelar requests
    this.abortControllers = new Map();
  }

  /**
   * Obtiene asistencias con caché inteligente
   * @param {number} limite - Número máximo de registros
   * @param {number} offset - Offset para paginación
   * @returns {Promise<Array>} Lista de asistencias
   */
  async obtenerAsistencias(limite = null, offset = 0) {
    const cacheKey = `asistencias_${limite}_${offset}`;
    
    // Check cache primero
    if (this.cache.has(cacheKey)) {
      const cached = this.cache.get(cacheKey);
      if (Date.now() - cached.timestamp < this.cacheTimeout) {
        console.log('✅ Asistencias obtenidas del caché (ultra rápido)');
        return cached.data;
      }
    }
    
    // Cancelar request anterior si existe
    if (this.abortControllers.has(cacheKey)) {
      this.abortControllers.get(cacheKey).abort();
    }
    
    // Crear nuevo AbortController
    const controller = new AbortController();
    this.abortControllers.set(cacheKey, controller);
    
    try {
      const territorioFilter = authService.getTerritorioFilter();
      let url = `${API_URL}/asistencias?`;
      const params = new URLSearchParams();
      
      if (limite !== null) params.append('limit', limite);
      if (offset > 0) params.append('offset', offset);
      if (territorioFilter) params.append('territorio', territorioFilter);
      
      url += params.toString();
      
      console.time('⚡ Fetch asistencias');
      
      const response = await fetch(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        signal: controller.signal,
        // Usar fetch con prioridad alta
        priority: 'high'
      });
      
      console.timeEnd('⚡ Fetch asistencias');
      
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      const asistencias = data.asistencias || [];
      
      // Guardar en caché
      this.cache.set(cacheKey, {
        data: asistencias,
        timestamp: Date.now()
      });
      
      console.log(`✅ ${asistencias.length} asistencias cargadas y cacheadas`);
      return asistencias;
      
    } catch (error) {
      if (error.name === 'AbortError') {
        console.log('⚠️ Request anterior cancelado');
        throw error;
      }
      console.error('❌ Error al obtener asistencias:', error);
      throw error;
    } finally {
      this.abortControllers.delete(cacheKey);
    }
  }

  /**
   * Combina asistencias con usuarios usando Promise.all para máxima velocidad
   * @param {number} limite - Número máximo de registros
   * @param {number} offset - Offset para paginación
   * @returns {Promise<Array>} Asistencias enriquecidas
   */
  async obtenerAsistenciasConUsuarios(limite = null, offset = 0) {
    console.time('⚡ Total con usuarios');
    
    try {
      // Cargar asistencias y usuarios en paralelo (Apple-style)
      const [asistencias, usuarios] = await Promise.all([
        this.obtenerAsistencias(limite, offset),
        this.obtenerUsuarios()
      ]);

      // Crear Map para búsqueda O(1)
      const usuariosMap = new Map(usuarios.map(u => [u.id, u]));

      // Enriquecer datos de forma eficiente
      const asistenciasEnriquecidas = asistencias.map(asistencia => {
        const usuario = usuariosMap.get(asistencia.usuario_id);
        
        return {
          ...asistencia,
          nombre_usuario: usuario?.nombre_completo || 'Usuario no encontrado',
          correo_usuario: usuario?.correo || 'N/A',
          cargo_usuario: usuario?.cargo || 'N/A',
          curp_usuario: usuario?.curp || null,
          foto_entrada_url: this.construirUrlFoto(asistencia.foto_entrada_url),
          foto_salida_url: this.construirUrlFoto(asistencia.foto_salida_url)
        };
      });

      console.timeEnd('⚡ Total con usuarios');
      console.log(`✅ ${asistenciasEnriquecidas.length} asistencias procesadas`);
      
      return asistenciasEnriquecidas;
      
    } catch (error) {
      console.error('❌ Error al obtener asistencias con usuarios:', error);
      throw error;
    }
  }

  /**
   * Obtiene usuarios con caché
   * @returns {Promise<Array>} Lista de usuarios
   */
  async obtenerUsuarios() {
    const cacheKey = 'usuarios';
    
    // Check cache
    if (this.cache.has(cacheKey)) {
      const cached = this.cache.get(cacheKey);
      // Usuarios se cachean por más tiempo (5 minutos)
      if (Date.now() - cached.timestamp < 300000) {
        console.log('✅ Usuarios obtenidos del caché');
        return cached.data;
      }
    }
    
    try {
      const territorioFilter = authService.getTerritorioFilter();
      let url = `${API_URL}/usuarios`;
      if (territorioFilter) {
        url += `?territorio=${encodeURIComponent(territorioFilter)}`;
      }
      
      const response = await fetch(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        priority: 'high'
      });

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      const usuarios = data.usuarios || [];
      
      // Guardar en caché por más tiempo
      this.cache.set(cacheKey, {
        data: usuarios,
        timestamp: Date.now()
      });
      
      console.log(`✅ ${usuarios.length} usuarios cargados y cacheados`);
      return usuarios;
      
    } catch (error) {
      console.error('❌ Error al obtener usuarios:', error);
      throw error;
    }
  }

  /**
   * Construye URL de foto de forma optimizada
   * @param {string} rutaFoto - Ruta de la foto
   * @returns {string} URL completa
   */
  construirUrlFoto(rutaFoto) {
    if (!rutaFoto) return null;
    
    if (rutaFoto.startsWith('http://') || rutaFoto.startsWith('https://')) {
      return rutaFoto;
    }
    
    let rutaLimpia = rutaFoto;
    if (!rutaLimpia.startsWith('fotos/')) {
      if (!rutaLimpia.includes('/')) {
        rutaLimpia = `fotos/${rutaLimpia}`;
      }
    }
    
    return `${API_URL}/${rutaLimpia}`;
  }

  /**
   * Formatea fecha con caché de resultados
   */
  formatearFecha(fecha) {
    if (!fecha) return 'N/A';
    
    try {
      if (typeof fecha === 'string' && fecha.includes('T')) {
        return new Date(fecha).toLocaleDateString('es-ES', {
          timeZone: 'America/Mexico_City',
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        });
      }
      
      if (typeof fecha === 'string' && fecha.match(/^\d{4}-\d{2}-\d{2}$/)) {
        const [year, month, day] = fecha.split('-').map(num => parseInt(num, 10));
        const fechaObj = new Date(year, month - 1, day);
        
        return fechaObj.toLocaleDateString('es-ES', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        });
      }
      
      return new Date(fecha).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      });
    } catch (error) {
      console.error('Error formateando fecha:', error);
      return fecha;
    }
  }

  /**
   * Formatea hora
   */
  formatearHora(hora) {
    if (!hora) return 'N/A';
    
    try {
      let fechaObj;
      
      if (hora.includes('T')) {
        fechaObj = new Date(hora);
      } else {
        fechaObj = new Date(`1970-01-01T${hora}`);
      }
      
      return fechaObj.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
      }).toLowerCase();
    } catch (error) {
      console.error('Error formateando hora:', error);
      return hora;
    }
  }

  /**
   * Formatea coordenadas
   */
  formatearCoordenadas(latitud, longitud) {
    if (!latitud || !longitud) return 'N/A';
    return `${latitud.toFixed(6)}, ${longitud.toFixed(6)}`;
  }

  /**
   * Limpia el caché manualmente
   */
  limpiarCache() {
    this.cache.clear();
    console.log('🗑️ Caché limpiado');
  }

  /**
   * Pre-carga datos en segundo plano (Apple-style prefetching)
   */
  async precargarDatos() {
    try {
      console.log('🚀 Precargando datos en segundo plano...');
      
      // Precargar usuarios primero (son más estables)
      await this.obtenerUsuarios();
      
      // Luego precargar primera página de asistencias
      await this.obtenerAsistencias(50, 0);
      
      console.log('✅ Datos precargados exitosamente');
    } catch (error) {
      console.warn('⚠️ Error al precargar datos:', error);
    }
  }
}

export default new AsistenciasServiceOptimized();
