// Servicio para manejo de historial de usuarios
const API_BASE = 'http://localhost:8000'; // Usar localhost para desarrollo

class HistorialService {
  constructor() {
    this.cache = new Map(); // Cache para mejorar performance
  }

  /**
   * Obtener historial de un usuario con filtros opcionales
   */
  async obtenerHistorial(usuarioId, filtros = {}) {
    try {
      const params = new URLSearchParams();
      
      if (filtros.fechaInicio) {
        params.append('fecha_inicio', filtros.fechaInicio);
      }
      
      if (filtros.fechaFin) {
        params.append('fecha_fin', filtros.fechaFin);
      }
      
      if (filtros.tipo) {
        params.append('tipo', filtros.tipo);
      }
      
      if (filtros.limit) {
        params.append('limit', filtros.limit);
      }

      const url = `${API_BASE}/historial/${usuarioId}?${params.toString()}`;
      console.log('🔍 Obteniendo historial desde:', url);

      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ Error response:', errorText);
        
        if (response.status === 404) {
          throw new Error('Usuario no encontrado');
        }
        
        if (response.status === 500) {
          throw new Error('Error del servidor');
        }
        
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Historial obtenido:', data);

      // Guardar en cache
      const cacheKey = `${usuarioId}_${JSON.stringify(filtros)}`;
      this.cache.set(cacheKey, data);

      return data;

    } catch (error) {
      console.error('❌ Error al obtener historial:', error);
      throw error;
    }
  }

  /**
   * Crear un nuevo registro en el historial
   */
  async crearRegistro(registro) {
    try {
      console.log('📝 Creando registro de historial:', registro);

      const response = await fetch(`${API_BASE}/historial`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(registro)
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Error HTTP: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Registro creado:', data);

      // Limpiar cache para forzar recarga
      this.limpiarCache();

      return data;

    } catch (error) {
      console.error('❌ Error al crear registro:', error);
      throw error;
    }
  }

  /**
   * Obtener resumen estadístico del historial de un usuario
   */
  async obtenerResumen(usuarioId) {
    try {
      console.log('📊 Obteniendo resumen de historial para usuario:', usuarioId);

      const response = await fetch(`${API_BASE}/historial/resumen/${usuarioId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Usuario no encontrado');
        }
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Resumen obtenido:', data);

      return data;

    } catch (error) {
      console.error('❌ Error al obtener resumen:', error);
      throw error;
    }
  }

  /**
   * Generar datos para exportar a Excel
   */
  generarDatosExcel(historial, usuario) {
    const datos = historial.map(registro => ({
      'ID': registro.id,
      'Usuario': registro.usuario_nombre || 'N/A',
      'Correo': registro.usuario_correo || 'N/A',
      'Tipo': this.formatearTipo(registro.tipo),
      'Descripción': registro.descripcion || 'N/A',
      'Fecha': this.formatearFecha(registro.fecha),
      'Hora': this.formatearHora(registro.hora),
      'Creado en': this.formatearFechaHora(registro.creado_en)
    }));

    return {
      datos,
      nombreArchivo: `historial_${usuario}_${new Date().toISOString().split('T')[0]}.xlsx`,
      nombreHoja: 'Historial'
    };
  }

  /**
   * Formatear tipo de registro para mostrar
   */
  formatearTipo(tipo) {
    const tipos = {
      'entrada': 'Entrada',
      'salida': 'Salida',
      'actividad': 'Actividad'
    };
    return tipos[tipo] || tipo;
  }

  /**
   * Formatear fecha para mostrar
   */
  formatearFecha(fecha) {
    if (!fecha) return 'N/A';
    
    try {
      return new Date(fecha).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      });
    } catch (error) {
      return fecha;
    }
  }

  /**
   * Formatear hora para mostrar
   */
  formatearHora(hora) {
    if (!hora) return 'N/A';
    
    try {
      // Si la hora viene como string "HH:MM:SS", extraer solo HH:MM
      if (typeof hora === 'string' && hora.includes(':')) {
        const partes = hora.split(':');
        return `${partes[0]}:${partes[1]}`;
      }
      return hora;
    } catch (error) {
      return hora;
    }
  }

  /**
   * Formatear fecha y hora completa
   */
  formatearFechaHora(fechaHora) {
    if (!fechaHora) return 'N/A';
    
    try {
      return new Date(fechaHora).toLocaleString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch (error) {
      return fechaHora;
    }
  }

  /**
   * Obtener fechas de la semana actual
   */
  obtenerSemanaActual() {
    const hoy = new Date();
    const diaSemana = hoy.getDay(); // 0 = domingo, 1 = lunes, etc.
    const lunes = new Date(hoy);
    lunes.setDate(hoy.getDate() - diaSemana + 1); // Ajustar al lunes
    
    const domingo = new Date(lunes);
    domingo.setDate(lunes.getDate() + 6);

    return {
      inicio: lunes.toISOString().split('T')[0],
      fin: domingo.toISOString().split('T')[0]
    };
  }

  /**
   * Obtener fechas del año actual
   */
  obtenerAnoActual() {
    const hoy = new Date();
    return {
      inicio: `${hoy.getFullYear()}-01-01`,
      fin: `${hoy.getFullYear()}-12-31`
    };
  }

  /**
   * Probar conectividad con el backend
   */
  async probarConectividad() {
    try {
      console.log('🔍 Probando conectividad con:', `${API_BASE}/historial`);
      
      const response = await fetch(`${API_BASE}/historial`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Conectividad OK - Datos de prueba:', data);
      return data;

    } catch (error) {
      console.error('❌ Error de conectividad:', error);
      throw error;
    }
  }

  /**
   * Limpiar cache
   */
  limpiarCache() {
    this.cache.clear();
    console.log('🗑️ Cache de historial limpiado');
  }

  /**
   * Obtener color para el tipo de registro
   */
  obtenerColorTipo(tipo) {
    const colores = {
      'entrada': '#27ae60',    // Verde
      'salida': '#e74c3c',     // Rojo
      'actividad': '#3498db'   // Azul
    };
    return colores[tipo] || '#6c757d';
  }

  /**
   * Obtener icono para el tipo de registro
   */
  obtenerIconoTipo(tipo) {
    const iconos = {
      'entrada': '🟢',
      'salida': '🔴',
      'actividad': '🔵'
    };
    return iconos[tipo] || '⚪';
  }
}

// Instancia singleton del servicio
const historialService = new HistorialService();

export default historialService;
