import axios from 'axios';
import { getBestApiUrl, checkApiConnectivity, connectivityMonitor } from '../utils/network.js';
import offlineService from './offlineService.js';

// Instancia de axios con configuración base
const api = axios.create({
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Variable para almacenar la URL actual
let currentApiUrl = null;

// Función para inicializar la URL de la API
async function initializeApiUrl() {
  if (!currentApiUrl) {
    currentApiUrl = await getBestApiUrl();
    console.log(`🌐 API Service inicializado con: ${currentApiUrl}`);
  }
  return currentApiUrl;
}

// Interceptor para agregar la URL base automáticamente
api.interceptors.request.use(async (config) => {
  if (!currentApiUrl) {
    await initializeApiUrl();
  }
  
  // Si no tiene baseURL, agregarla
  if (!config.baseURL && !config.url.startsWith('http')) {
    config.baseURL = currentApiUrl;
  }
  
  console.log(`📡 API Request: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
  return config;
});

// Interceptor para manejar errores de red y reintentar con servidor alternativo
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    if (error.code === 'ECONNABORTED' || error.code === 'NETWORK_ERROR' || !error.response) {
      console.log('❌ Error de conexión, intentando con servidor alternativo...');
      
      // Reintentar con nueva URL
      try {
        const newUrl = await getBestApiUrl();
        if (newUrl !== currentApiUrl) {
          currentApiUrl = newUrl;
          console.log(`🔄 Reintentando con: ${currentApiUrl}`);
          
          // Reintentar la petición original
          const originalRequest = error.config;
          originalRequest.baseURL = currentApiUrl;
          return api(originalRequest);
        }
      } catch (retryError) {
        console.log('❌ Error en reintento:', retryError);
      }
    }
    
    return Promise.reject(error);
  }
);

// Funciones específicas para cada endpoint con soporte offline
export const apiService = {
  // Usuarios
  async createUser(userData) {
    const response = await api.post('/usuarios', userData);
    return response.data;
  },

  async login(credentials) {
    const response = await api.post('/login', credentials);
    return response.data;
  },

  async changePassword(passwordData) {
    const response = await api.post('/cambiar_contrasena', passwordData);
    return response.data;
  },

  async getUsers() {
    const response = await api.get('/usuarios');
    return response.data;
  },

  async getUser(userId) {
    const response = await api.get(`/usuarios/${userId}`);
    return response.data;
  },

  // Registros con soporte offline
  async createRecord(formData, options = {}) {
    const { forceOffline = false, skipOffline = false } = options;
    
    // Si se fuerza offline o no hay conectividad, guardar offline
    if (forceOffline || (!skipOffline && !(await checkApiConnectivity()))) {
      console.log('📴 Sin conexión - guardando registro offline');
      
      // Convertir FormData a objeto para almacenamiento
      const recordData = {};
      for (let [key, value] of formData.entries()) {
        recordData[key] = value;
      }
      
      const offlineId = await offlineService.saveRecordOffline(recordData);
      
      return {
        success: true,
        offline: true,
        offlineId,
        message: 'Sin conexión. Tu registro ha sido guardado localmente y se enviará cuando recuperes conexión.'
      };
    }

    try {
      const response = await api.post('/registro', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      return response.data;
    } catch (error) {
      // Si falla por conectividad y no se especifica skipOffline, intentar guardar offline
      if (!skipOffline && this.isConnectivityError(error)) {
        console.log('🔄 Error de conexión - guardando registro offline como respaldo');
        
        const recordData = {};
        for (let [key, value] of formData.entries()) {
          recordData[key] = value;
        }
        
        const offlineId = await offlineService.saveRecordOffline(recordData);
        
        return {
          success: true,
          offline: true,
          offlineId,
          fallback: true,
          message: 'Error de conexión. Tu registro ha sido guardado localmente y se enviará cuando la conexión sea estable.'
        };
      }
      throw error;
    }
  },

  async getRecords(userId = null) {
    const url = userId ? `/registros?usuario_id=${userId}` : '/registros';
    const response = await api.get(url);
    return response.data;
  },

  // Asistencias con soporte offline
  async markEntry(formData, options = {}) {
    const { forceOffline = false, skipOffline = false } = options;
    
    // Si se fuerza offline o no hay conectividad, guardar offline
    if (forceOffline || (!skipOffline && !(await checkApiConnectivity()))) {
      console.log('📴 Sin conexión - guardando entrada offline');
      
      // Convertir FormData a objeto para almacenamiento
      const attendanceData = {
        attendanceType: 'entrada'
      };
      for (let [key, value] of formData.entries()) {
        attendanceData[key] = value;
      }
      
      const offlineId = await offlineService.saveAttendanceOffline(attendanceData);
      
      return {
        success: true,
        offline: true,
        offlineId,
        message: 'Sin conexión. Tu entrada ha sido guardada localmente y se enviará cuando recuperes conexión.'
      };
    }

    try {
      const response = await api.post('/asistencia/entrada', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      return response.data;
    } catch (error) {
      // Si falla por conectividad, intentar guardar offline
      if (!skipOffline && this.isConnectivityError(error)) {
        console.log('🔄 Error de conexión - guardando entrada offline como respaldo');
        
        const attendanceData = {
          attendanceType: 'entrada'
        };
        for (let [key, value] of formData.entries()) {
          attendanceData[key] = value;
        }
        
        const offlineId = await offlineService.saveAttendanceOffline(attendanceData);
        
        return {
          success: true,
          offline: true,
          offlineId,
          fallback: true,
          message: 'Error de conexión. Tu entrada ha sido guardada localmente y se enviará cuando la conexión sea estable.'
        };
      }
      throw error;
    }
  },

  async markExit(formData, options = {}) {
    const { forceOffline = false, skipOffline = false } = options;
    
    // Si se fuerza offline o no hay conectividad, guardar offline
    if (forceOffline || (!skipOffline && !(await checkApiConnectivity()))) {
      console.log('📴 Sin conexión - guardando salida offline');
      
      // Convertir FormData a objeto para almacenamiento
      const attendanceData = {
        attendanceType: 'salida'
      };
      for (let [key, value] of formData.entries()) {
        attendanceData[key] = value;
      }
      
      const offlineId = await offlineService.saveAttendanceOffline(attendanceData);
      
      return {
        success: true,
        offline: true,
        offlineId,
        message: 'Sin conexión. Tu salida ha sido guardada localmente y se enviará cuando recuperes conexión.'
      };
    }

    try {
      const response = await api.post('/asistencia/salida', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      return response.data;
    } catch (error) {
      // Si falla por conectividad, intentar guardar offline
      if (!skipOffline && this.isConnectivityError(error)) {
        console.log('🔄 Error de conexión - guardando salida offline como respaldo');
        
        const attendanceData = {
          attendanceType: 'salida'
        };
        for (let [key, value] of formData.entries()) {
          attendanceData[key] = value;
        }
        
        const offlineId = await offlineService.saveAttendanceOffline(attendanceData);
        
        return {
          success: true,
          offline: true,
          offlineId,
          fallback: true,
          message: 'Error de conexión. Tu salida ha sido guardada localmente y se enviará cuando la conexión sea estable.'
        };
      }
      throw error;
    }
  },

  async getAttendances(userId = null) {
    const url = userId ? `/asistencias?usuario_id=${userId}` : '/asistencias';
    const response = await api.get(url);
    return response.data;
  },

  // Utilidades para detectar errores de conectividad
  isConnectivityError(error) {
    return (
      error.code === 'ECONNABORTED' ||
      error.code === 'NETWORK_ERROR' ||
      error.code === 'ERR_NETWORK' ||
      !error.response ||
      (error.response && error.response.status >= 500)
    );
  },

  // Funciones de sincronización manual
  async forceSyncPending() {
    if (!(await checkApiConnectivity())) {
      throw new Error('No hay conexión disponible para sincronizar');
    }
    
    return await offlineService.autoSync();
  },

  async getPendingOfflineItems() {
    return await offlineService.getPendingItems();
  },

  async getOfflineStats() {
    return await offlineService.getStats();
  },

  // Debug endpoints
  async checkUsersStructure() {
    const response = await api.get('/debug/usuarios-estructura');
    return response.data;
  },

  async checkAttendancesStructure() {
    const response = await api.get('/debug/asistencias-estructura');
    return response.data;
  },

  // Utilidades
  getCurrentApiUrl() {
    return currentApiUrl;
  },

  async refreshApiUrl() {
    currentApiUrl = await getBestApiUrl();
    return currentApiUrl;
  },

  getConnectivityStatus() {
    return connectivityMonitor.getStatus();
  },

  addConnectivityListener(callback) {
    return connectivityMonitor.addListener(callback);
  }
};

// Exportar también la instancia de axios configurada para casos especiales
export { api };

// Inicializar automáticamente al importar
initializeApiUrl();
