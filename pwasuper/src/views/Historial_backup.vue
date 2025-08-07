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
        <div class="mb-4 text-sm text-gray-600">
          Total de registros: <span class="font-semibold text-primary">{{ registros.length }}</span>
        </div>
        <div class="space-y-4">
          <div v-for="(registro, index) in registros" :key="index" class="border border-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
            <div class="p-4">
              <div class="flex flex-col sm:flex-row">
                <div class="sm:w-24 sm:h-24 h-32 w-full bg-gray-100 rounded overflow-hidden mb-3 sm:mb-0 sm:mr-4">
                  <img v-if="registro.foto_url" :src="registro.foto_url" class="w-full h-full object-cover" alt="Foto del registro" />
                  <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                </div>
                
                <div class="flex-1">
                  <div class="flex justify-between">
                    <p class="text-sm text-gray-500">{{ formatFecha(registro.fecha_hora) }}</p>
                    <button @click="verEnMapa(registro)" class="text-primary hover:text-primary-dark text-sm flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                      </svg>
                      Ver en mapa
                    </button>
                  </div>
                  
                  <p class="text-gray-800 mt-1">{{ registro.descripcion || "Sin descripción" }}</p>
                  
                  <div class="mt-2 flex space-x-4">
                    <div class="text-xs font-mono text-gray-600">
                      Lat: {{ registro.latitud }}
                    </div>
                    <div class="text-xs font-mono text-gray-600">
                      Lon: {{ registro.longitud }}
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
        <div class="space-y-4">
          <div v-for="(asistencia, index) in asistencias" :key="index" class="border border-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
            <div class="p-4">
              <!-- Información de la fecha -->
              <div class="flex justify-between items-center mb-3">
                <h3 class="text-lg font-semibold text-gray-800">{{ formatFecha(asistencia.fecha) }}</h3>
                <div class="flex space-x-2">
                  <span v-if="asistencia.hora_entrada" class="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                    Entrada: {{ formatHora(asistencia.hora_entrada) }}
                  </span>
                  <span v-if="asistencia.hora_salida" class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                    Salida: {{ formatHora(asistencia.hora_salida) }}
                  </span>
                </div>
              </div>

              <!-- Entrada -->
              <div v-if="asistencia.hora_entrada" class="mb-4 bg-green-50 rounded-lg p-3">
                <h4 class="text-sm font-medium text-green-800 mb-2 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                  </svg>
                  Entrada - {{ formatHora(asistencia.hora_entrada) }}
                </h4>
                <div class="flex flex-col sm:flex-row">
                  <div v-if="asistencia.foto_entrada_url" class="sm:w-20 sm:h-20 h-24 w-full bg-gray-100 rounded overflow-hidden mb-2 sm:mb-0 sm:mr-3">
                    <img :src="`${API_URL}/${asistencia.foto_entrada_url}`" class="w-full h-full object-cover" alt="Foto de entrada" />
                  </div>
                  <div class="flex-1">
                    <p class="text-sm text-gray-700 mb-1">{{ asistencia.descripcion_entrada || "Sin descripción" }}</p>
                    <div class="flex space-x-4 text-xs text-gray-600">
                      <span>Lat: {{ asistencia.latitud_entrada }}</span>
                      <span>Lon: {{ asistencia.longitud_entrada }}</span>
                      <button @click="verAsistenciaEnMapa(asistencia, 'entrada')" class="text-green-600 hover:text-green-800">
                        Ver ubicación
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Salida -->
              <div v-if="asistencia.hora_salida" class="bg-blue-50 rounded-lg p-3">
                <h4 class="text-sm font-medium text-blue-800 mb-2 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  Salida - {{ formatHora(asistencia.hora_salida) }}
                </h4>
                <div class="flex flex-col sm:flex-row">
                  <div v-if="asistencia.foto_salida_url" class="sm:w-20 sm:h-20 h-24 w-full bg-gray-100 rounded overflow-hidden mb-2 sm:mb-0 sm:mr-3">
                    <img :src="`${API_URL}/${asistencia.foto_salida_url}`" class="w-full h-full object-cover" alt="Foto de salida" />
                  </div>
                  <div class="flex-1">
                    <p class="text-sm text-gray-700 mb-1">{{ asistencia.descripcion_salida || "Sin descripción" }}</p>
                    <div class="flex space-x-4 text-xs text-gray-600">
                      <span>Lat: {{ asistencia.latitud_salida }}</span>
                      <span>Lon: {{ asistencia.longitud_salida }}</span>
                      <button @click="verAsistenciaEnMapa(asistencia, 'salida')" class="text-blue-600 hover:text-blue-800">
                        Ver ubicación
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Estado incompleto -->
              <div v-if="asistencia.hora_entrada && !asistencia.hora_salida" class="mt-3 bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                <p class="text-sm text-yellow-800 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Asistencia en curso - Sin registro de salida
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
                
                <p class="text-gray-800 mt-1">{{ registro.descripcion || "Sin descripción" }}</p>
                
                <div class="mt-2 flex space-x-4">
                  <div class="text-xs font-mono text-gray-600">
                    Lat: {{ registro.latitud }}
                  </div>
                  <div class="text-xs font-mono text-gray-600">
                    Lon: {{ registro.longitud }}
                  </div>
                </div>
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
    <div v-if="mapaVisible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-lg w-full max-h-[90vh] flex flex-col">
        <div class="p-4 border-b border-gray-200 flex justify-between items-center">
          <h3 class="text-lg font-medium">Ubicación del registro</h3>
          <button @click="mapaVisible = false" class="text-gray-500 hover:text-gray-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="flex-1 min-h-0">
          <div id="detailMap" class="h-full w-full"></div>
        </div>
        <div class="p-4 border-t border-gray-200">
          <button @click="mapaVisible = false" class="btn btn-secondary w-full">Cerrar</button>
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
    
    console.log('Registros procesados:', registros.value.length);  } catch (err) {
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
    if (!fechaStr) return '';
    
    let fecha;
    
    // PROBLEMA IDENTIFICADO: Fechas YYYY-MM-DD se interpretan como UTC
    // SOLUCION: Forzar interpretación como fecha local de México
    if (fechaStr.includes('T') || fechaStr.includes(' ')) {
      // Fecha con hora, usar constructor normal y convertir a zona horaria de México
      fecha = new Date(fechaStr);
    } else {
      // Solo fecha YYYY-MM-DD - SOLUCION MEJORADA
      // Parsear manualmente para evitar problemas de zona horaria
      const partesFecha = fechaStr.split('-');
      if (partesFecha.length === 3) {
        // Crear fecha usando constructor Date(año, mes-1, día)
        // Esto crea la fecha en la zona horaria local, no UTC
        fecha = new Date(parseInt(partesFecha[0]), parseInt(partesFecha[1]) - 1, parseInt(partesFecha[2]));
        console.log(`📅 Fecha parseada localmente: ${fechaStr} -> ${fecha.toDateString()}`);
      } else {
        fecha = new Date(fechaStr + 'T12:00:00'); // Agregar hora para evitar problemas UTC
      }
    }
    
    // Verificar que la fecha sea válida
    if (isNaN(fecha.getTime())) {
      console.error('Fecha inválida:', fechaStr);
      return fechaStr;
    }
    
    // Formatear fecha en español mexicano usando la fecha local parseada
    const fechaFormateada = fecha.toLocaleDateString('es-MX', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      timeZone: 'America/Mexico_City' // Asegurar que se use zona horaria de México
    });
    
    // Capitalizar solo la primera letra
    const resultado = fechaFormateada.charAt(0).toUpperCase() + fechaFormateada.slice(1);
    console.log(`📅 Formato final: ${fechaStr} -> ${resultado}`);
    return resultado;
  } catch (e) {
    console.error('Error al formatear fecha:', e, fechaStr);
    return fechaStr;
  }
}

function formatHora(fechaStr) {
  try {
    const fecha = new Date(fechaStr);
    return fecha.toLocaleTimeString();
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

// Modificar el onMounted para cargar asistencias si es necesario
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
</script>

<style>
/* Para asegurar que el mapa de detalle se muestre correctamente */
#detailMap {
  min-height: 300px;
}

/* Estilos para el marcador personalizado con animación */
.custom-marker-icon {
  background: transparent !important;
  border: none !important;
}

.custom-marker-wrapper {
  position: relative;
  width: 30px;
  height: 30px;
}

.custom-marker {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  background: #4CAF50;
  border: 3px solid white;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  transform: translate(-50%, -50%);
  z-index: 2;
  animation: markerBounce 1s ease-out;
}

.marker-pulse {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 30px;
  height: 30px;
  border: 2px solid #4CAF50;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: markerPulse 2s infinite;
  z-index: 1;
}

@keyframes markerBounce {
  0% {
    transform: translate(-50%, -50%) scale(0);
  }
  50% {
    transform: translate(-50%, -50%) scale(1.2);
  }
  100% {
    transform: translate(-50%, -50%) scale(1);
  }
}

@keyframes markerPulse {
  0% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(2);
    opacity: 0;
  }
}

/* Efecto hover para el marcador */
.custom-marker:hover {
  transform: translate(-50%, -50%) scale(1.1);
  transition: transform 0.2s ease;
}
</style>
