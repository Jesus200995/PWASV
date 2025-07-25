<template>
  <div class="page-container">
    <!-- Tabs para alternar entre registros normales y asistencias -->
    <div class="card mb-6">
      <div class="flex border-b border-gray-200 mb-6">
        <button 
          @click="cambiarTab('registros')" 
          :class="[
            'px-4 py-2 font-medium text-sm border-b-2 transition-colors',
            tabActiva === 'registros' 
              ? 'border-primary text-primary' 
              : 'border-transparent text-gray-500 hover:text-gray-700'
          ]"
        >
          Registros Normales
        </button>
        <button 
          @click="cambiarTab('asistencias')" 
          :class="[
            'px-4 py-2 font-medium text-sm border-b-2 transition-colors ml-4',
            tabActiva === 'asistencias' 
              ? 'border-primary text-primary' 
              : 'border-transparent text-gray-500 hover:text-gray-700'
          ]"
        >
          Asistencias
        </button>
      </div>

      <!-- Tab de Registros Normales -->
      <div v-show="tabActiva === 'registros'">
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4">
          <div>
            <h2 class="text-2xl font-bold text-gray-800">Historial de registros</h2>
            <p v-if="userInfo" class="text-sm text-gray-600 mt-1">
              Registros de: <span class="font-medium text-primary">{{ userInfo.nombre_completo }}</span>
            </p>
          </div>
          <button @click="cargarRegistros" class="btn btn-secondary text-sm px-3 py-1 mt-2 sm:mt-0">
            <svg v-if="cargando" class="animate-spin h-4 w-4 mr-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span v-else>Actualizar</span>
          </button>
        </div>
      </div>

      <!-- Tab de Asistencias -->
      <div v-show="tabActiva === 'asistencias'">
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4">
          <div>
            <h2 class="text-2xl font-bold text-gray-800">Historial de asistencias</h2>
            <p v-if="userInfo" class="text-sm text-gray-600 mt-1">
              Asistencias de: <span class="font-medium text-primary">{{ userInfo.nombre_completo }}</span>
            </p>
          </div>
          <button @click="cargarAsistencias" class="btn btn-secondary text-sm px-3 py-1 mt-2 sm:mt-0">
            <svg v-if="cargandoAsistencias" class="animate-spin h-4 w-4 mr-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span v-else>Actualizar</span>
          </button>
        </div>
      </div>

      <div v-if="error" class="mb-4 bg-red-100 border-l-4 border-red-500 text-red-700 p-4" role="alert">
        <p>{{ error }}</p>
        <p class="text-sm mt-2">
          <strong>Problema técnico detectado:</strong> El servidor principal está experimentando problemas. 
          El administrador del sistema necesita actualizar el código del servidor.
        </p>
      </div>

      <!-- Lista de registros -->
      <div v-if="tabActiva === 'registros' && registros.length > 0">
        <div class="mb-2 text-xs text-gray-600">
          Total de registros: <span class="font-semibold text-primary">{{ registros.length }}</span>
        </div>
        <div class="space-y-2">
          <div v-for="(registro, index) in registros" :key="index" class="border border-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
            <div class="p-3">
              <div class="flex gap-3">
                <div class="w-16 h-16 flex-shrink-0 bg-gray-100 rounded overflow-hidden relative" :class="{'cursor-pointer': registro.foto_url}" @click="registro.foto_url && verImagen(registro.foto_url)">
                  <img v-if="registro.foto_url" :src="registro.foto_url" class="w-full h-full object-cover" alt="Foto" />
                  <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div v-if="registro.foto_url" class="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-20 flex items-center justify-center transition-opacity">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white opacity-0 hover:opacity-100" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>
                </div>
                
                <div class="flex-1 min-w-0">
                  <div class="flex justify-between items-start">
                    <p class="text-xs text-gray-500 font-medium">{{ formatFecha(registro.fecha_hora) }}</p>
                    <button @click="verEnMapa(registro)" class="text-primary hover:text-primary-dark text-xs flex items-center ml-2 whitespace-nowrap">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                      </svg>
                      Ver mapa
                    </button>
                  </div>
                  
                  <p class="text-xs text-gray-800 mt-1 line-clamp-2">{{ registro.descripcion || "Sin descripción" }}</p>
                  
                  <div class="mt-1 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <div class="text-xs text-gray-600 truncate">
                      {{ registro.latitud }}, {{ registro.longitud }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Lista de asistencias -->
      <div v-if="tabActiva === 'asistencias' && asistencias.length > 0">
        <div class="mb-4 text-sm text-gray-600">
          Total de asistencias: <span class="font-semibold text-primary">{{ asistencias.length }}</span>
        </div>
        <div class="space-y-2">
          <div v-for="(asistencia, index) in asistencias" :key="index" class="border border-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
            <div class="p-3">
              <!-- Información de la fecha -->
              <div class="flex justify-between items-center mb-2">
                <h3 class="text-base font-medium text-gray-800">{{ formatFecha(asistencia.fecha) }}</h3>
                <div class="flex flex-wrap gap-1">
                  <span v-if="asistencia.hora_entrada" class="bg-green-100 text-green-800 text-xs px-1.5 py-0.5 rounded-full whitespace-nowrap">
                    E: {{ formatHora(asistencia.hora_entrada) }}
                  </span>
                  <span v-if="asistencia.hora_salida" class="bg-blue-100 text-blue-800 text-xs px-1.5 py-0.5 rounded-full whitespace-nowrap">
                    S: {{ formatHora(asistencia.hora_salida) }}
                  </span>
                </div>
              </div>

              <!-- Entrada -->
              <div v-if="asistencia.hora_entrada" class="mb-2 bg-green-50 rounded-lg p-2">
                <h4 class="text-xs font-medium text-green-800 mb-1 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                  </svg>
                  Entrada - {{ formatHora(asistencia.hora_entrada) }}
                </h4>
                <div class="flex items-start gap-2">
                  <div v-if="asistencia.foto_entrada_url" class="w-14 h-14 flex-shrink-0 bg-gray-100 rounded overflow-hidden relative cursor-pointer" @click="verImagen(`${API_URL}/${asistencia.foto_entrada_url}`)">
                    <img :src="`${API_URL}/${asistencia.foto_entrada_url}`" class="w-full h-full object-cover" alt="Foto" />
                    <div class="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-20 flex items-center justify-center transition-opacity">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white opacity-0 hover:opacity-100" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                      </svg>
                    </div>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-xs text-gray-700 mb-1 line-clamp-2">{{ asistencia.descripcion_entrada || "Sin descripción" }}</p>
                    <div class="flex flex-wrap gap-2 text-xs text-gray-600">
                      <div class="flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        <button @click="verAsistenciaEnMapa(asistencia, 'entrada')" class="text-green-600 hover:text-green-800 underline">
                          Ver mapa
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Salida -->
              <div v-if="asistencia.hora_salida" class="bg-blue-50 rounded-lg p-2">
                <h4 class="text-xs font-medium text-blue-800 mb-1 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  Salida - {{ formatHora(asistencia.hora_salida) }}
                </h4>
                <div class="flex items-start gap-2">
                  <div v-if="asistencia.foto_salida_url" class="w-14 h-14 flex-shrink-0 bg-gray-100 rounded overflow-hidden relative cursor-pointer" @click="verImagen(`${API_URL}/${asistencia.foto_salida_url}`)">
                    <img :src="`${API_URL}/${asistencia.foto_salida_url}`" class="w-full h-full object-cover" alt="Foto" />
                    <div class="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-20 flex items-center justify-center transition-opacity">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white opacity-0 hover:opacity-100" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                      </svg>
                    </div>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-xs text-gray-700 mb-1 line-clamp-2">{{ asistencia.descripcion_salida || "Sin descripción" }}</p>
                    <div class="flex flex-wrap gap-2 text-xs text-gray-600">
                      <div class="flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        <button @click="verAsistenciaEnMapa(asistencia, 'salida')" class="text-blue-600 hover:text-blue-800 underline">
                          Ver mapa
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Estado incompleto -->
              <div v-if="asistencia.hora_entrada && !asistencia.hora_salida" class="mt-2 bg-yellow-50 border border-yellow-200 rounded-lg p-2">
                <p class="text-xs text-yellow-800 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  En curso - Sin registro de salida
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Estado vacío para registros -->
      <div v-if="tabActiva === 'registros' && registros.length === 0 && !cargando" class="text-center py-8">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <p class="mt-2 text-gray-500">Aún no tienes registros guardados</p>
        <p class="text-sm text-gray-400 mt-1">Crea tu primer registro para verlo aquí</p>
        <router-link to="/" class="btn btn-primary inline-block mt-4 text-sm">Crear nuevo registro</router-link>
      </div>

      <!-- Estado vacío para asistencias -->
      <div v-if="tabActiva === 'asistencias' && asistencias.length === 0 && !cargandoAsistencias" class="text-center py-8">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="mt-2 text-gray-500">Aún no tienes registros de asistencia</p>
        <p class="text-sm text-gray-400 mt-1">Marca tu primera asistencia para verla aquí</p>
        <router-link to="/" class="btn btn-primary inline-block mt-4 text-sm">Marcar asistencia</router-link>
      </div>
      
      <!-- Cargando registros -->
      <div v-if="tabActiva === 'registros' && cargando" class="text-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary mx-auto"></div>
        <p class="mt-4 text-gray-500">Cargando registros...</p>
      </div>

      <!-- Cargando asistencias -->
      <div v-if="tabActiva === 'asistencias' && cargandoAsistencias" class="text-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary mx-auto"></div>
        <p class="mt-4 text-gray-500">Cargando asistencias...</p>
      </div>
    </div>
    
    <!-- Diálogo de mapa -->
    <div v-if="mapaVisible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-2">
      <div class="bg-white rounded-lg shadow-xl w-full max-w-md max-h-[90vh] flex flex-col">
        <div class="p-3 border-b border-gray-200 flex justify-between items-center">
          <h3 class="text-sm font-medium">Ubicación</h3>
          <button @click="mapaVisible = false" class="text-gray-500 hover:text-gray-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="flex-1 min-h-0">
          <div id="detailMap" class="h-full w-full"></div>
        </div>
        <div class="p-2 border-t border-gray-200">
          <button @click="mapaVisible = false" class="btn btn-secondary w-full text-sm py-1.5">Cerrar</button>
        </div>
      </div>
    </div>
    
    <!-- Modal para visualizar imagen -->
    <div v-if="imagenModalVisible" class="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50 p-3">
      <div class="w-full max-w-xs sm:max-w-sm md:max-w-md max-h-[85vh] flex flex-col relative">
        <button @click="imagenModalVisible = false" class="absolute right-1 top-1 bg-black bg-opacity-50 text-white rounded-full p-1 hover:bg-opacity-70 transition-opacity z-10">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <div class="overflow-hidden rounded-lg bg-black bg-opacity-30">
          <img :src="imagenSeleccionada" class="w-full h-auto object-contain max-h-[80vh]" alt="Imagen ampliada" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { API_URL, checkInternetConnection, getOfflineMessage } from '../utils/network.js';

const router = useRouter();
const registros = ref([]);
const asistencias = ref([]);
const cargando = ref(true);
const cargandoAsistencias = ref(false);
const error = ref(null);
const mapaVisible = ref(false);
const registroSeleccionado = ref(null);
const detailMap = ref(null);
const isOnline = ref(true);
const userInfo = ref(null);
const tabActiva = ref('registros');
const imagenModalVisible = ref(false);
const imagenSeleccionada = ref('');

// Comprobar autenticación y cargar datos
onMounted(async () => {
  const userStr = localStorage.getItem('user');
  if (!userStr) {
    router.push('/login');
    return;
  }
  
  userInfo.value = JSON.parse(userStr);
  
  // Verificar conexión a internet
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    error.value = getOfflineMessage();
    cargando.value = false;
    return;
  }
  
  cargarRegistros();
  // Cargar asistencias también al inicio
  cargarAsistencias();
});

async function cargarRegistros() {
  cargando.value = true;
  error.value = null;
  
  // Verificar conexión a internet antes de cargar
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    error.value = getOfflineMessage();
    cargando.value = false;
    return;
  }
    try {
    console.log('Cargando registros para usuario:', userInfo.value.id);
    
    // Obtener registros específicos del usuario actual
    const response = await axios.get(`${API_URL}/registros?usuario_id=${userInfo.value.id}`, {
      timeout: 10000, // 10 segundos de timeout
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    console.log('Respuesta del servidor:', response.data);
    
    // Procesar las URLs de las fotos para que sean rutas absolutas
    registros.value = response.data.registros.map(r => ({
      ...r,
      foto_url: r.foto_url ? `${API_URL}/${r.foto_url}` : null
    }));
    
    console.log('Registros procesados:', registros.value.length);
  } catch (err) {
    console.error('Error al cargar registros:', err);
    
    if (err.response) {
      // Error de respuesta del servidor
      if (err.response.status === 500) {
        error.value = 'El servidor está experimentando problemas técnicos. Por favor, inténtalo más tarde.';
      } else {
        error.value = 'Error del servidor: ' + (err.response.data.detail || err.response.statusText);
      }
    } else if (err.request) {
      // Error de conexión
      error.value = 'No se pudo conectar con el servidor. Verifica tu conexión a internet.';
    } else {
      // Error general
      error.value = 'Error al cargar los registros: ' + err.message;
    }
  } finally {
    cargando.value = false;
  }
}

// Función para cargar asistencias
async function cargarAsistencias() {
  cargandoAsistencias.value = true;
  error.value = null;
  
  // Verificar conexión a internet antes de cargar
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    error.value = getOfflineMessage();
    cargandoAsistencias.value = false;
    return;
  }
    try {
    console.log('Cargando asistencias para usuario:', userInfo.value.id);
    
    // Obtener asistencias específicas del usuario actual
    const response = await axios.get(`${API_URL}/asistencias?usuario_id=${userInfo.value.id}`, {
      timeout: 10000, // 10 segundos de timeout
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    console.log('Respuesta del servidor (asistencias):', response.data);
    
    asistencias.value = response.data.asistencias || [];
    
    console.log('Asistencias procesadas:', asistencias.value.length);
  } catch (err) {
    console.error('Error al cargar asistencias:', err);
    
    if (err.response) {
      // Error de respuesta del servidor
      if (err.response.status === 500) {
        error.value = 'El servidor está experimentando problemas técnicos. Por favor, inténtalo más tarde.';
      } else {
        error.value = 'Error del servidor: ' + (err.response.data.detail || err.response.statusText);
      }
    } else if (err.request) {
      // Error de conexión
      error.value = 'No se pudo conectar con el servidor. Verifica tu conexión a internet.';
    } else {
      // Error general
      error.value = 'Error al cargar las asistencias: ' + err.message;
    }
  } finally {
    cargandoAsistencias.value = false;
  }
}

function formatFecha(fechaStr) {
  try {
    const fecha = new Date(fechaStr);
    return fecha.toLocaleDateString();
  } catch (e) {
    return fechaStr;
  }
}

function formatHora(fechaStr) {
  try {
    const fecha = new Date(fechaStr);
    
    // Formato personalizado para hora de 12 horas con am/pm en español
    const hora = fecha.getHours();
    const minutos = fecha.getMinutes();
    
    // Convertir a formato 12 horas
    const hora12 = hora % 12 || 12;
    const ampm = hora >= 12 ? 'pm' : 'am';
    
    // Asegurar que tanto horas como minutos tengan siempre dos dígitos
    const horaStr = hora12 < 10 ? `0${hora12}` : hora12;
    const minutosStr = minutos < 10 ? `0${minutos}` : minutos;
    
    return `${horaStr}:${minutosStr} ${ampm}`;
  } catch (e) {
    return fechaStr;
  }
}

function verEnMapa(registro) {
  registroSeleccionado.value = registro;
  mapaVisible.value = true;
  
  // Esperar a que el DOM se actualice
  setTimeout(() => {
    if (!detailMap.value) {
      detailMap.value = L.map('detailMap').setView([registro.latitud, registro.longitud], 15);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(detailMap.value);
    } else {
      detailMap.value.setView([registro.latitud, registro.longitud], 15);
    }
    
    // Limpiar marcadores anteriores
    detailMap.value.eachLayer(layer => {
      if (layer instanceof L.Marker) {
        detailMap.value.removeLayer(layer);
      }
    });
      // Añadir marcador con icono personalizado
    const customIcon = L.divIcon({
      html: `
        <div class="custom-marker-wrapper">
          <div class="custom-marker"></div>
          <div class="marker-pulse"></div>
        </div>
      `,
      className: 'custom-marker-icon',
      iconSize: [30, 30],
      iconAnchor: [15, 15]
    });
    
    const marker = L.marker([registro.latitud, registro.longitud], { icon: customIcon }).addTo(detailMap.value);
    if (registro.descripcion) {
      marker.bindPopup(registro.descripcion).openPopup();
    }
    
    // Forzar que el mapa se redibuje
    setTimeout(() => {
      detailMap.value.invalidateSize();
    }, 100);
  }, 100);
}

// Función para ver asistencia en el mapa
function verAsistenciaEnMapa(asistencia, tipo) {
  const latitud = tipo === 'entrada' ? asistencia.latitud_entrada : asistencia.latitud_salida;
  const longitud = tipo === 'entrada' ? asistencia.longitud_entrada : asistencia.longitud_salida;
  const descripcion = tipo === 'entrada' ? asistencia.descripcion_entrada : asistencia.descripcion_salida;
  
  // Crear un objeto similar a registro para reutilizar la función existente
  const registroParaMapa = {
    latitud: latitud,
    longitud: longitud,
    descripcion: descripcion || `${tipo.charAt(0).toUpperCase() + tipo.slice(1)} - ${formatFecha(asistencia.fecha)}`
  };
  
  verEnMapa(registroParaMapa);
}

// Cargar asistencias cuando se cambia a esa pestaña
function cambiarTab(tab) {
  tabActiva.value = tab;
  if (tab === 'asistencias' && asistencias.value.length === 0) {
    cargarAsistencias();
  }
}

// Función para abrir una imagen en el modal
function verImagen(url) {
  if (url) {
    imagenSeleccionada.value = url;
    imagenModalVisible.value = true;
    
    // Configurar gestos táctiles para cerrar el modal
    setTimeout(() => {
      const modalElement = document.querySelector('[v-if="imagenModalVisible"]');
      if (modalElement) {
        let startY = 0;
        let distY = 0;
        
        modalElement.addEventListener('touchstart', (e) => {
          startY = e.touches[0].clientY;
        }, { passive: true });
        
        modalElement.addEventListener('touchmove', (e) => {
          distY = e.touches[0].clientY - startY;
          if (distY > 100) {
            imagenModalVisible.value = false;
          }
        }, { passive: true });
        
        // Cerrar modal con un toque en el fondo
        modalElement.addEventListener('click', (e) => {
          if (e.target === modalElement) {
            imagenModalVisible.value = false;
          }
        });
      }
    }, 100);
  }
}
</script>

<style>
/* Para asegurar que el mapa de detalle se muestre correctamente */
#detailMap {
  min-height: 250px;
}

/* Estilos para el marcador personalizado con animación */
.custom-marker-icon {
  background: transparent !important;
  border: none !important;
}

.custom-marker-wrapper {
  position: relative;
  width: 24px;
  height: 24px;
}

.custom-marker {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 10px;
  height: 10px;
  background-color: #3b82f6;
  border: 2px solid white;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  z-index: 2;
}

.marker-pulse {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 24px;
  height: 24px;
  background-color: #3b82f6;
  border-radius: 50%;
  opacity: 0.6;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0% {
    transform: translate(-50%, -50%) scale(0.5);
    opacity: 0.8;
  }
  50% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.3;
  }
  100% {
    transform: translate(-50%, -50%) scale(1.5);
    opacity: 0;
  }
}

/* Mejoras generales para responsividad */
.btn {
  transition: all 0.2s ease;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Ajustes para pantallas muy pequeñas */
@media (max-width: 320px) {
  .w-16 {
    width: 3.5rem;
  }
  
  .h-16 {
    height: 3.5rem;
  }
  
  .w-14 {
    width: 3rem;
  }
  
  .h-14 {
    height: 3rem;
  }
  
  .gap-3 {
    gap: 0.5rem;
  }
  
  .gap-2 {
    gap: 0.375rem;
  }
}

/* Estilos para el modal de imagen */
[v-if="imagenModalVisible"] {
  animation: fadeIn 0.2s ease-out;
  touch-action: pan-y pinch-zoom;
}

[v-if="imagenModalVisible"] img {
  max-height: 80vh;
  max-width: 95vw;
  object-fit: contain;
  animation: scaleIn 0.25s cubic-bezier(0.19, 1, 0.22, 1);
  border-radius: 0.375rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleIn {
  from { transform: scale(0.85); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

/* Estilos para efecto de hover en las imágenes */
.cursor-pointer {
  transition: transform 0.2s ease;
}

.cursor-pointer:hover {
  transform: scale(1.05);
}

/* Ajustes específicos para modal en móvil */
@media (max-width: 480px) {
  [v-if="imagenModalVisible"] .max-w-xs {
    max-width: 90vw;
  }
  
  [v-if="imagenModalVisible"] img {
    max-height: 70vh;
  }
}
</style>
