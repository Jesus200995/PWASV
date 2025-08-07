import axios from 'axios';
import { getBestApiUrl, checkInternetConnection } from '../utils/network.js';

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

// Funciones específicas para cada endpoint
export const apiService = {
  // Usuarios
  async createUser(userData) {
    const response = await api.post('/usuarios', userData);
    return response.data;
  },

  async acceptTerms(userId) {
    const response = await api.post('/usuarios/aceptar_terminos', { usuario_id: userId });
    return response.data;
  },

  async checkUserTerms(userId) {
    const response = await api.get(`/usuarios/${userId}/terminos`);
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

  // Registros
  async createRecord(formData) {
    const response = await api.post('/registro', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  },

  async getRecords(userId = null) {
    const url = userId ? `/registros?usuario_id=${userId}` : '/registros';
    const response = await api.get(url);
    return response.data;
  },

  // Asistencias
  async markEntry(formData) {
    const response = await api.post('/asistencia/entrada', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  },

  async markExit(formData) {
    const response = await api.post('/asistencia/salida', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  },

  async getAttendances(userId = null) {
    const url = userId ? `/asistencias?usuario_id=${userId}` : '/asistencias';
    const response = await api.get(url);
    return response.data;
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
  }
};

// Exportar también la instancia de axios configurada para casos especiales
export { api };

// Inicializar automáticamente al importar
initializeApiUrl();
