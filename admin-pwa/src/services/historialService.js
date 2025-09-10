// Servicio para manejo de historial completo de usuarios
import { API_URL } from '../config/api.js'

class HistorialService {
  constructor() {
    this.cache = new Map(); // Cache para mejorar performance
  }

  /**
   * Obtener historial completo de un usuario (historial + registros + asistencias)
   */
  async obtenerHistorialCompleto(usuarioId, filtros = {}) {
    try {
      console.log('🔍 Obteniendo historial completo para usuario:', usuarioId, 'con filtros:', filtros);

      // Ejecutar todas las consultas en paralelo, incluyendo datos del usuario
      const [historialResp, registrosResp, asistenciasResp, usuarioData] = await Promise.all([
        this.obtenerHistorial(usuarioId, filtros),
        this.obtenerRegistros(usuarioId),
        this.obtenerAsistencias(usuarioId),
        this.obtenerDatosUsuario(usuarioId)
      ]);

      console.log('📊 Datos obtenidos:', {
        historial: historialResp?.historial?.length || 0,
        registros: registrosResp?.registros?.length || 0,
        asistencias: asistenciasResp?.asistencias?.length || 0,
        usuario: usuarioData ? 'OK' : 'Error'
      });

      // Convertir todos los datos a un formato unificado
      const historialUnificado = [];

      // Agregar registros del historial
      if (historialResp?.historial) {
        historialResp.historial.forEach(item => {
          historialUnificado.push({
            id: `hist_${item.id}`,
            tipo: item.tipo,
            descripcion: item.descripcion,
            fecha: item.fecha,
            hora: item.hora,
            detalles: item.detalles,
            creado_en: item.creado_en,
            fecha_hora_combinada: this.combinarFechaHora(item.fecha, item.hora),
            origen: 'historial',
            // DATOS DE USUARIO - usar datos del historial o del usuario obtenido
            usuario_nombre: item.usuario_nombre || usuarioData?.nombre_completo,
            usuario_correo: item.usuario_correo || usuarioData?.correo,
            usuario_curp: item.usuario_curp || usuarioData?.curp,
            usuario_cargo: item.usuario_cargo || usuarioData?.cargo
          });
        });
      }

      // Agregar registros de actividades
      if (registrosResp?.registros) {
        registrosResp.registros.forEach(item => {
          historialUnificado.push({
            id: `reg_${item.id}`,
            tipo: 'actividad',
            descripcion: item.descripcion || 'Registro de actividad',
            fecha: item.fecha_hora ? item.fecha_hora.split('T')[0] : null,
            hora: item.fecha_hora ? item.fecha_hora.split('T')[1]?.substring(0, 8) : null,
            detalles: JSON.stringify({
              latitud: item.latitud,
              longitud: item.longitud,
              foto_url: item.foto_url
            }),
            creado_en: item.fecha_hora,
            fecha_hora_combinada: item.fecha_hora,
            origen: 'registros',
            // AGREGAR DATOS DE USUARIO
            usuario_nombre: usuarioData?.nombre_completo,
            usuario_correo: usuarioData?.correo,
            usuario_curp: usuarioData?.curp,
            usuario_cargo: usuarioData?.cargo
          });
        });
      }

      // Agregar asistencias (entradas y salidas)
      if (asistenciasResp?.asistencias) {
        asistenciasResp.asistencias.forEach(item => {
          // Agregar entrada si existe
          if (item.hora_entrada) {
            historialUnificado.push({
              id: `asist_entrada_${item.id}`,
              tipo: 'entrada',
              descripcion: item.descripcion_entrada || 'Entrada registrada',
              fecha: item.fecha,
              hora: item.hora_entrada,
              detalles: JSON.stringify({
                latitud: item.latitud_entrada,
                longitud: item.longitud_entrada,
                foto_url: item.foto_entrada_url
              }),
              creado_en: this.combinarFechaHora(item.fecha, item.hora_entrada),
              fecha_hora_combinada: this.combinarFechaHora(item.fecha, item.hora_entrada),
              origen: 'asistencias',
              // AGREGAR DATOS DE USUARIO
              usuario_nombre: usuarioData?.nombre_completo,
              usuario_correo: usuarioData?.correo,
              usuario_curp: usuarioData?.curp,
              usuario_cargo: usuarioData?.cargo
            });
          }

          // Agregar salida si existe
          if (item.hora_salida) {
            historialUnificado.push({
              id: `asist_salida_${item.id}`,
              tipo: 'salida',
              descripcion: item.descripcion_salida || 'Salida registrada',
              fecha: item.fecha,
              hora: item.hora_salida,
              detalles: JSON.stringify({
                latitud: item.latitud_salida,
                longitud: item.longitud_salida,
                foto_url: item.foto_salida_url
              }),
              creado_en: this.combinarFechaHora(item.fecha, item.hora_salida),
              fecha_hora_combinada: this.combinarFechaHora(item.fecha, item.hora_salida),
              origen: 'asistencias',
              // AGREGAR DATOS DE USUARIO
              usuario_nombre: usuarioData?.nombre_completo,
              usuario_correo: usuarioData?.correo,
              usuario_curp: usuarioData?.curp,
              usuario_cargo: usuarioData?.cargo
            });
          }
        });
      }

      // Aplicar filtros
      let historialFiltrado = historialUnificado;

      if (filtros.tipo) {
        historialFiltrado = historialFiltrado.filter(item => item.tipo === filtros.tipo);
      }

      if (filtros.fechaInicio) {
        historialFiltrado = historialFiltrado.filter(item => item.fecha >= filtros.fechaInicio);
      }

      if (filtros.fechaFin) {
        historialFiltrado = historialFiltrado.filter(item => item.fecha <= filtros.fechaFin);
      }

      // Ordenar por fecha y hora más reciente primero
      historialFiltrado.sort((a, b) => {
        const fechaA = new Date(a.fecha_hora_combinada || a.creado_en);
        const fechaB = new Date(b.fecha_hora_combinada || b.creado_en);
        return fechaB - fechaA;
      });

      // Calcular estadísticas
      const estadisticas = {
        total_registros: historialFiltrado.length,
        entradas: historialFiltrado.filter(item => item.tipo === 'entrada').length,
        salidas: historialFiltrado.filter(item => item.tipo === 'salida').length,
        actividades: historialFiltrado.filter(item => item.tipo === 'actividad').length
      };

      console.log('✅ Historial completo procesado:', {
        total: historialFiltrado.length,
        estadisticas
      });

      return {
        historial: historialFiltrado,
        total: historialFiltrado.length,
        usuario: historialResp?.usuario || { id: usuarioId },
        estadisticas
      };

    } catch (error) {
      console.error('❌ Error al obtener historial completo:', error);
      throw error;
    }
  }

  /**
   * Obtener registros de actividades
   */
  async obtenerRegistros(usuarioId) {
    try {
      const url = `${API_URL}/registros?usuario_id=${usuarioId}`;
      console.log('🔍 Obteniendo registros desde:', url);

      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Registros obtenidos:', data);
      return data;

    } catch (error) {
      console.error('❌ Error al obtener registros:', error);
      throw error;
    }
  }

  /**
   * Obtener asistencias (entradas/salidas)
   */
  async obtenerAsistencias(usuarioId) {
    try {
      const url = `${API_URL}/asistencias?usuario_id=${usuarioId}`;
      console.log('🔍 Obteniendo asistencias desde:', url);

      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Asistencias obtenidas:', data);
      return data;

    } catch (error) {
      console.error('❌ Error al obtener asistencias:', error);
      throw error;
    }
  }

  /**
   * Combinar fecha y hora en formato ISO
   */
  combinarFechaHora(fecha, hora) {
    if (!fecha) return null;
    
    if (hora) {
      return `${fecha}T${hora}`;
    } else {
      return `${fecha}T00:00:00`;
    }
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

      const url = `${API_URL}/historial/${usuarioId}?${params.toString()}`;
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

      const response = await fetch(`${API_URL}/historial`, {
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

      const response = await fetch(`${API_URL}/historial/resumen/${usuarioId}`, {
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
      let fechaObj;
      
      // PROBLEMA IDENTIFICADO: Fechas YYYY-MM-DD se interpretan como UTC
      // SOLUCION: Forzar interpretación como fecha local de México
      if (fecha.includes('T') || fecha.includes(' ')) {
        // Fecha con hora, usar constructor normal
        fechaObj = new Date(fecha);
      } else {
        // Solo fecha YYYY-MM-DD - SOLUCION MEJORADA
        // Parsear manualmente para evitar problemas de zona horaria
        const partesFecha = fecha.split('-');
        if (partesFecha.length === 3) {
          // Crear fecha usando constructor Date(año, mes-1, día)
          // Esto crea la fecha en la zona horaria local, no UTC
          fechaObj = new Date(parseInt(partesFecha[0]), parseInt(partesFecha[1]) - 1, parseInt(partesFecha[2]));
        } else {
          fechaObj = new Date(fecha + 'T12:00:00'); // Agregar hora para evitar problemas UTC
        }
      }
      
      // Verificar que la fecha sea válida
      if (isNaN(fechaObj.getTime())) {
        console.error('Fecha inválida en historialService:', fecha);
        return fecha;
      }
      
      return fechaObj.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        timeZone: 'America/Mexico_City' // Asegurar zona horaria de México
      });
    } catch (error) {
      console.error('Error al formatear fecha en historialService:', error, fecha);
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
   * Obtener lista de usuarios
   */
  async obtenerUsuarios() {
    try {
      const url = `${API_URL}/usuarios`;
      console.log('🔍 Obteniendo usuarios desde:', url);

      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Usuarios obtenidos:', data);
      return data;

    } catch (error) {
      console.error('❌ Error al obtener usuarios:', error);
      throw error;
    }
  }

  /**
   * Probar conectividad con el backend
   */
  async probarConectividad() {
    try {
      console.log('🔍 Probando conectividad con:', `${API_URL}/historial`);
      
      const response = await fetch(`${API_URL}/historial`, {
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
   * Formatear tipo de actividad
   */
  formatearTipo(tipo) {
    const tipos = {
      entrada: 'Entrada',
      salida: 'Salida',
      actividad: 'Actividad',
      registro: 'Registro'
    }
    return tipos[tipo] || tipo
  }

  /**
   * Formatear fecha
   */
  formatearFecha(fecha) {
    if (!fecha) return 'N/A'
    
    try {
      let fechaObj;
      
      // PROBLEMA IDENTIFICADO: Fechas YYYY-MM-DD se interpretan como UTC
      // SOLUCION: Forzar interpretación como fecha local de México
      if (fecha.includes('T') || fecha.includes(' ')) {
        // Fecha con hora, usar constructor normal
        fechaObj = new Date(fecha);
      } else {
        // Solo fecha YYYY-MM-DD - SOLUCION MEJORADA
        // Parsear manualmente para evitar problemas de zona horaria
        const partesFecha = fecha.split('-');
        if (partesFecha.length === 3) {
          // Crear fecha usando constructor Date(año, mes-1, día)
          // Esto crea la fecha en la zona horaria local, no UTC
          fechaObj = new Date(parseInt(partesFecha[0]), parseInt(partesFecha[1]) - 1, parseInt(partesFecha[2]));
        } else {
          fechaObj = new Date(fecha + 'T12:00:00'); // Agregar hora para evitar problemas UTC
        }
      }
      
      // Verificar que la fecha sea válida
      if (isNaN(fechaObj.getTime())) {
        console.error('Fecha inválida en historialService:', fecha);
        return fecha;
      }
      
      return fechaObj.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        timeZone: 'America/Mexico_City' // Asegurar zona horaria de México
      });
    } catch (error) {
      console.error('Error al formatear fecha en historialService:', error, fecha);
      return fecha
    }
  }

  /**
   * Formatear hora
   */
  formatearHora(hora) {
    if (!hora) return 'N/A'
    
    try {
      // Si la hora viene con formato completo ISO, extraer solo la parte de hora
      if (hora.includes('T')) {
        hora = hora.split('T')[1]
      }
      
      // Tomar solo HH:mm:ss o HH:mm
      const partes = hora.split(':')
      if (partes.length >= 2) {
        return `${partes[0]}:${partes[1]}`
      }
      
      return hora
    } catch (error) {
      return hora
    }
  }

  /**
   * Generar datos para Excel
   */
  generarDatosExcel(historial, nombreUsuario) {
    const fecha = new Date()
    const fechaStr = fecha.toISOString().split('T')[0]
    
    return {
      datos: historial.map(registro => ({
        ID: registro.id,
        Origen: this.formatearOrigen(registro.origen),
        Tipo: this.formatearTipo(registro.tipo),
        Descripcion: registro.descripcion || 'Sin descripción',
        Fecha: this.formatearFecha(registro.fecha),
        Hora: this.formatearHora(registro.hora),
        'Creado en': registro.creado_en
      })),
      nombreArchivo: `historial_${nombreUsuario.replace(/\s+/g, '_')}_${fechaStr}.xlsx`,
      nombreHoja: 'Historial'
    }
  }

  /**
   * Formatear origen de datos
   */
  formatearOrigen(origen) {
    const origenes = {
      historial: 'Historial',
      registros: 'Actividades',
      asistencias: 'Asistencia'
    }
    return origenes[origen] || origen
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

  /**
   * Obtener datos básicos de un usuario
   */
  async obtenerDatosUsuario(usuarioId) {
    try {
      console.log('🔍 Obteniendo datos del usuario:', usuarioId);

      const response = await fetch(`${API_URL}/usuarios/${usuarioId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const data = await response.json();
      console.log('✅ Datos del usuario obtenidos:', data);
      return data;

    } catch (error) {
      console.error('❌ Error al obtener datos del usuario:', error);
      // No lanzar error, solo devolver null para que el resto funcione
      return null;
    }
  }
}

// Instancia singleton del servicio
const historialService = new HistorialService();

export default historialService;
