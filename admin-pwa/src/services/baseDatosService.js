// Servicio para descargar la base de datos completa de forma rápida
import { API_URL } from '../config/api.js'

class BaseDatosService {
  constructor() {
    this.onProgress = null // Callback para actualizar progreso
  }
  
  async descargarBDCompleta(onProgress = null) {
    // Descarga toda la base de datos en formato SQL de forma optimizada y rápida.
    // Utiliza streaming para manejo eficiente de memoria.
    // onProgress es una función callback que recibe { bytesDescargados, tamanoTotal, velocidad }
    
    this.onProgress = onProgress
    
    try {
      console.log('🚀 Iniciando descarga rápida de BD completa...');
      
      const token = localStorage.getItem('admin_token');
      
      if (!token) {
        throw new Error('No hay token de autenticación. Por favor inicia sesión.');
      }
      
      console.log(`📡 Conectando a: ${API_URL}/descargar-bd-completa`);
      
      const response = await fetch(`${API_URL}/descargar-bd-completa`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/sql'
        }
      });
      
      if (!response.ok) {
        console.error(`❌ Error HTTP: ${response.status} - ${response.statusText}`);
        
        if (response.status === 401) {
          throw new Error('No autorizado. Sesión expirada. Por favor inicia sesión nuevamente.');
        } else if (response.status === 403) {
          throw new Error('Acceso denegado. No tienes permisos para descargar la BD.');
        } else if (response.status === 404) {
          throw new Error('Endpoint no disponible. Verifica que el servidor está actualizado.');
        } else if (response.status === 500) {
          throw new Error('Error del servidor. Por favor intenta más tarde.');
        } else {
          throw new Error(`Error del servidor: ${response.status}`);
        }
      }
      
      console.log('✅ Conexión establecida');
      
      // Obtener tamaño total del contenido
      const contentLength = response.headers.get('content-length');
      const tamanoTotal = parseInt(contentLength, 10) || 0;
      
      console.log(`📊 Tamaño total: ${this.formatearBytes(tamanoTotal)}`);
      
      // Leer el stream de respuesta
      const reader = response.body.getReader();
      const chunks = [];
      let bytesDescargados = 0;
      let ultimaActualizacion = Date.now();
      let ultimosBytesReportados = 0;
      
      try {
        while (true) {
          const { done, value } = await reader.read();
          
          if (done) break;
          
          chunks.push(value);
          bytesDescargados += value.length;
          
          // Calcular velocidad y notificar cada 200ms
          const ahora = Date.now();
          const deltaTiempo = (ahora - ultimaActualizacion) / 1000; // en segundos
          
          if (deltaTiempo >= 0.2) {
            const deltaBytes = bytesDescargados - ultimosBytesReportados;
            const velocidad = deltaBytes / deltaTiempo; // bytes por segundo
            
            // Notificar progreso
            if (this.onProgress) {
              this.onProgress({
                bytesDescargados,
                tamanoTotal,
                velocidad,
                porcentaje: tamanoTotal > 0 ? Math.round((bytesDescargados / tamanoTotal) * 100) : 0
              });
            }
            
            console.log(`📥 Descargados: ${this.formatearBytes(bytesDescargados)} / ${this.formatearBytes(tamanoTotal)} (${this.formatearBytes(velocidad)}/s)`);
            
            ultimaActualizacion = ahora;
            ultimosBytesReportados = bytesDescargados;
          }
        }
      } catch (streamError) {
        console.error('❌ Error leyendo stream:', streamError);
        throw new Error('Error al descargar el archivo: ' + streamError.message);
      }
      
      console.log(`✅ Contenido descargado - Tamaño final: ${this.formatearBytes(bytesDescargados)}`);
      
      // Combinar chunks en un único blob
      const blob = new Blob(chunks, { type: 'application/sql' });
      console.log(`✅ Blob creado - Tamaño: ${this.formatearBytes(blob.size)}`);
      
      // Obtener nombre del archivo del header Content-Disposition
      const contentDisposition = response.headers.get('content-disposition');
      let nombreArchivo = 'BASE_DATOS_COMPLETA.sql';
      
      if (contentDisposition && contentDisposition.includes('filename=')) {
        nombreArchivo = contentDisposition.split('filename=')[1].replace(/"/g, '');
      }
      
      console.log(`📁 Nombre del archivo: ${nombreArchivo}`);
      
      // Crear URL del blob
      const url = window.URL.createObjectURL(blob);
      
      // Crear elemento anchor para descarga
      const a = document.createElement('a');
      a.href = url;
      a.download = nombreArchivo;
      document.body.appendChild(a);
      
      // Iniciar descarga
      console.log('⬇️ Iniciando descarga del archivo...');
      a.click();
      
      // Limpiar
      setTimeout(() => {
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      }, 100);
      
      console.log('✅ Descarga completada exitosamente');
      
      // Notificación final
      if (this.onProgress) {
        this.onProgress({
          bytesDescargados,
          tamanoTotal,
          velocidad: 0,
          porcentaje: 100,
          completado: true
        });
      }
      
      return {
        status: 'success',
        message: '✅ Base de datos descargada exitosamente',
        archivo: nombreArchivo,
        tamanho: blob.size,
        tamanhoMB: (blob.size / 1024 / 1024).toFixed(2)
      };
      
    } catch (error) {
      console.error('❌ Error al descargar la BD:', error.message);
      
      // Lanzar error con mensaje descriptivo
      throw new Error(error.message || 'Error desconocido al descargar la base de datos');
    }
  }

  formatearBytes(bytes) {
    if (bytes === 0) return '0 B'
    
    const k = 1024
    const tamanios = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    
    return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + tamanios[i]
  }

  async obtenerInfoBD() {
    // Obtiene información sobre el tamaño y cantidad de datos en la BD
    try {
      console.log('📊 Obteniendo información de la BD...');
      
      const token = localStorage.getItem('admin_token');
      
      if (!token) {
        throw new Error('No hay token de autenticación.');
      }
      
      const response = await fetch(`${API_URL}/estadisticas`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) {
        throw new Error(`Error al obtener estadísticas: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('📊 Información obtenida:', data);
      
      return data.estadisticas || data;
      
    } catch (error) {
      console.error('❌ Error obteniendo info de BD:', error);
      throw error;
    }
  }
}

export const baseDatosService = new BaseDatosService();
export default baseDatosService;
