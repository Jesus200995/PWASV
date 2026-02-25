/**
 * Servicio para obtener estadísticas de dispositivos
 */
import axios from 'axios';

// URL base de la API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://apipwa.sembrandodatos.com';

/**
 * Obtiene estadísticas completas de dispositivos
 * @returns {Promise} Promesa con las estadísticas
 */
export async function obtenerEstadisticasDispositivos() {
  try {
    const response = await axios.get(`${API_BASE_URL}/estadisticas/dispositivos`);
    return response.data;
  } catch (error) {
    console.error('Error al obtener estadísticas de dispositivos:', error);
    throw error;
  }
}

/**
 * Formatea los datos para gráficas
 * @param {Object} estadisticas - Estadísticas raw del backend
 * @returns {Object} Datos formateados para Chart.js
 */
export function formatearParaGraficas(estadisticas) {
  const dispositivos = estadisticas.por_dispositivo || [];
  
  // Colores para cada tipo de dispositivo
  const colores = {
    'Android': '#3DDC84',
    'iOS': '#147EFB',
    'Desktop': '#6B7280',
    'desconocido': '#9CA3AF'
  };
  
  const iconos = {
    'Android': '🤖',
    'iOS': '🍎',
    'Desktop': '💻',
    'desconocido': '❓'
  };
  
  return {
    labels: dispositivos.map(d => `${iconos[d.dispositivo] || '📱'} ${d.dispositivo}`),
    datasets: [{
      label: 'Usuarios',
      data: dispositivos.map(d => d.cantidad),
      backgroundColor: dispositivos.map(d => colores[d.dispositivo] || '#9CA3AF'),
      borderColor: dispositivos.map(d => colores[d.dispositivo] || '#9CA3AF'),
      borderWidth: 2
    }]
  };
}

/**
 * Formatea los datos por rol para gráficas
 * @param {Object} estadisticas - Estadísticas raw del backend
 * @returns {Object} Datos formateados para Chart.js
 */
export function formatearPorRol(estadisticas) {
  const porRol = estadisticas.por_rol || [];
  
  // Agrupar por rol
  const roles = {};
  porRol.forEach(item => {
    if (!roles[item.rol]) {
      roles[item.rol] = {
        Android: 0,
        iOS: 0,
        Desktop: 0,
        desconocido: 0
      };
    }
    roles[item.rol][item.dispositivo] = item.cantidad;
  });
  
  return {
    labels: Object.keys(roles),
    datasets: [
      {
        label: '🤖 Android',
        data: Object.values(roles).map(r => r.Android),
        backgroundColor: '#3DDC84',
        borderColor: '#3DDC84',
        borderWidth: 2
      },
      {
        label: '🍎 iOS',
        data: Object.values(roles).map(r => r.iOS),
        backgroundColor: '#147EFB',
        borderColor: '#147EFB',
        borderWidth: 2
      },
      {
        label: '💻 Desktop',
        data: Object.values(roles).map(r => r.Desktop),
        backgroundColor: '#6B7280',
        borderColor: '#6B7280',
        borderWidth: 2
      }
    ]
  };
}

export default {
  obtenerEstadisticasDispositivos,
  formatearParaGraficas,
  formatearPorRol
};
