import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'
import 'dayjs/locale/es-mx'

// Extender dayjs con los plugins necesarios
dayjs.extend(utc)
dayjs.extend(timezone)
dayjs.locale('es-mx')

// Zona horaria de Ciudad de México
const CDMX_TIMEZONE = 'America/Mexico_City'

/**
 * Formatea una fecha para mostrar en Ciudad de México
 * @param {string|Date} fecha - La fecha a formatear
 * @param {string} formato - El formato deseado (opcional)
 * @returns {string} La fecha formateada en horario de Ciudad de México
 */
export const formatearFechaCDMX = (fecha, formato = 'DD/MM/YYYY HH:mm:ss') => {
  if (!fecha) return ''
  
  try {
    let fechaParsed = dayjs(fecha)
    
    // Siempre convertir a timezone CDMX, sin importar el timezone original
    if (typeof fecha === 'string') {
      // Si es string, parsearlo como UTC primero si tiene indicadores de timezone
      if (fecha.includes('Z') || fecha.includes('+') || fecha.includes('-')) {
        fechaParsed = dayjs.utc(fecha).tz(CDMX_TIMEZONE)
      } else {
        // Si no tiene timezone info, asumir que ya está en CDMX
        fechaParsed = dayjs.tz(fecha, CDMX_TIMEZONE)
      }
    } else {
      // Si es Date object, convertir a CDMX
      fechaParsed = dayjs(fecha).tz(CDMX_TIMEZONE)
    }
    
    return fechaParsed.format(formato)
  } catch (error) {
    console.error('Error al formatear fecha:', error, 'Fecha original:', fecha)
    // Fallback usando Date nativo
    try {
      return new Date(fecha).toLocaleString('es-MX', { 
        timeZone: 'America/Mexico_City',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    } catch (fallbackError) {
      console.error('Error en fallback:', fallbackError)
      return fecha
    }
  }
}

/**
 * Obtiene la fecha/hora actual en Ciudad de México
 * @returns {dayjs.Dayjs} Objeto dayjs con la fecha actual en CDMX
 */
export const obtenerFechaActualCDMX = () => {
  return dayjs().tz(CDMX_TIMEZONE)
}

/**
 * Convierte una fecha UTC a horario de Ciudad de México
 * @param {string|Date} fechaUTC - La fecha en UTC
 * @returns {dayjs.Dayjs} La fecha convertida a CDMX
 */
export const convertirUTCAcdmx = (fechaUTC) => {
  return dayjs.utc(fechaUTC).tz(CDMX_TIMEZONE)
}

/**
 * Formatos predefinidos para fechas
 */
export const FORMATOS_FECHA = {
  COMPLETO: 'DD/MM/YYYY HH:mm:ss',
  FECHA_HORA: 'DD/MM/YYYY HH:mm',
  SOLO_FECHA: 'DD/MM/YYYY',
  SOLO_HORA: 'HH:mm:ss',
  RELATIVO: 'relativo' // Para usar con dayjs().fromNow()
}

/**
 * Formatea una fecha de manera relativa (hace X minutos, hace X horas, etc.)
 * @param {string|Date} fecha - La fecha a formatear
 * @returns {string} La fecha en formato relativo
 */
export const formatearFechaRelativa = (fecha) => {
  if (!fecha) return ''
  
  try {
    let fechaParsed = dayjs(fecha)
    
    // Asegurar conversión a CDMX
    if (typeof fecha === 'string') {
      if (fecha.includes('Z') || fecha.includes('+') || fecha.includes('-')) {
        fechaParsed = dayjs.utc(fecha).tz(CDMX_TIMEZONE)
      } else {
        fechaParsed = dayjs.tz(fecha, CDMX_TIMEZONE)
      }
    } else {
      fechaParsed = dayjs(fecha).tz(CDMX_TIMEZONE)
    }
    
    return fechaParsed.fromNow()
  } catch (error) {
    console.error('Error al formatear fecha relativa:', error)
    // Fallback
    try {
      return dayjs(fecha).fromNow()
    } catch (fallbackError) {
      return fecha
    }
  }
}

/**
 * Valida si una fecha está correctamente en timezone CDMX
 * @param {string|Date} fecha - La fecha a validar
 * @returns {boolean} True si está en CDMX o se puede convertir
 */
export const validarFechaCDMX = (fecha) => {
  try {
    const fechaConvertida = formatearFechaCDMX(fecha)
    return fechaConvertida !== fecha // Si se pudo formatear, es válida
  } catch (error) {
    return false
  }
}
