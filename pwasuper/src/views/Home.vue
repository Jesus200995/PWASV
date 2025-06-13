<template>
  <div class="page-container py-4">
    <div class="card mb-4">
      <div class="text-center mb-6">
        <h2 class="text-xl font-bold text-gray-800 mb-2">Registrar ubicación</h2>
        <p class="text-sm text-gray-500">Captura tu ubicación actual para el registro</p>
      </div>
      
      <!-- Info del usuario -->
      <div class="bg-primary/10 rounded-lg p-3 mb-6">
        <div class="flex items-center">
          <div class="w-10 h-10 bg-primary rounded-full flex items-center justify-center mr-3">
            <span class="text-white text-sm font-bold">{{ getUserInitials }}</span>
          </div>
          <div>
            <p class="font-medium text-primary">{{ user.nombre_completo }}</p>
            <p class="text-xs text-gray-500">{{ user.cargo }}</p>
          </div>
        </div>
      </div>

      <form @submit.prevent="enviarRegistro">
        <!-- Botón para obtener ubicación -->
        <button
          type="button"
          @click="getUbicacion"
          class="btn btn-secondary w-full mb-4 flex items-center justify-center"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5 mr-2"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
            />
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
            />
          </svg>
          Obtener ubicación actual
        </button>

        <!-- Mapa -->
        <div
          v-if="mapVisible"
          class="relative h-48 mb-4 bg-gray-100 rounded-lg overflow-hidden shadow-sm"
        >
          <div id="map" class="absolute inset-0"></div>
          <div
            v-if="!mapReady"
            class="absolute inset-0 flex items-center justify-center bg-gray-200 bg-opacity-70"
          >
            <div class="flex flex-col items-center">
              <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary"></div>
              <p class="mt-2 text-sm text-gray-600">Cargando mapa...</p>
            </div>
          </div>
        </div>

        <!-- Coordenadas -->
        <div
          v-if="latitud && longitud"
          class="bg-green-50 border border-green-200 rounded-lg p-3 mb-4"
        >
          <div class="grid grid-cols-2 gap-3">
            <div>
              <p class="text-xs text-gray-500">Latitud</p>
              <p class="font-mono text-sm font-medium text-gray-800">{{ latitud }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Longitud</p>
              <p class="font-mono text-sm font-medium text-gray-800">{{ longitud }}</p>
            </div>
          </div>
        </div>

        <!-- Input de archivo para foto -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">Foto</label>
          <div class="flex items-center justify-center w-full">
            <label class="flex flex-col w-full h-32 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50 active:bg-gray-100">
              <div v-if="!foto" class="flex flex-col items-center justify-center pt-7">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="w-8 h-8 text-gray-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
                <p class="pt-1 text-sm text-gray-400">Selecciona una foto</p>
              </div>
              <div v-else class="flex items-center justify-center h-full">
                <img :src="foto" class="h-full object-contain" />
              </div>
              <input
                type="file"
                accept="image/*"
                @change="onFileChange"
                class="hidden"
                ref="fileInput"
              />
            </label>
          </div>
        </div>

        <!-- Descripción -->
        <div class="mb-4">
          <label for="descripcion" class="block text-sm font-medium text-gray-700 mb-2">Descripción</label>
          <textarea
            v-model="descripcion"
            id="descripcion"
            rows="3"
            class="form-input"
            placeholder="Describe el lugar o añade notas..."
          ></textarea>
        </div>

        <!-- Botón enviar -->
        <button
          type="submit"
          :disabled="!latitud || !longitud || !foto || enviando"
          :class="['btn w-full', !latitud || !longitud || !foto || enviando ? 'bg-gray-400 cursor-not-allowed' : 'btn-primary']"
        >
          <span v-if="enviando" class="flex items-center justify-center">
            <svg
              class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            Enviando...
          </span>
          <span v-else>Guardar registro</span>
        </button>
      </form>
    </div>

    <!-- Mensajes de error -->
    <transition name="fade">
      <div
        v-if="error"
        class="mb-4 bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded"
        role="alert"
      >
        <p class="font-bold">Error</p>
        <p>{{ error }}</p>
      </div>
    </transition>

    <!-- Historial reciente -->
    <div v-if="historial.length > 0" class="card">
      <h3 class="text-lg font-semibold text-gray-800 mb-3">Registros recientes</h3>
      <div class="space-y-3">
        <div
          v-for="(r, i) in historial.slice(0, 3)"
          :key="i"
          class="border border-gray-200 rounded-lg p-3 hover:shadow-md transition-shadow"
        >
          <div class="flex">
            <div class="w-20 h-20 bg-gray-100 rounded overflow-hidden mr-3">
              <img
                v-if="r.foto"
                :src="r.foto"
                class="w-full h-full object-cover"
              />
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-xs text-gray-500">{{ r.fecha }}</p>
              <p class="text-sm text-gray-800 truncate">
                {{ r.descripcion || 'Sin descripción' }}
              </p>
              <p class="text-xs font-mono text-gray-600">
                Lat: {{ r.latitud }}, Lon: {{ r.longitud }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="text-center mt-4">
        <router-link
          to="/historial"
          class="text-sm text-primary hover:underline"
        >
          Ver todos los registros &rarr;
        </router-link>
      </div>
    </div>

    <!-- Modal de confirmación -->
    <Modal 
      :show="showModal" 
      title="¡Éxito!"
      message="¡Registro enviado y guardado correctamente!"
      @close="showModal = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { API_URL, checkInternetConnection, getOfflineMessage } from '../utils/network.js';
import Modal from '../components/Modal.vue';

// Referencias y estado
const latitud = ref(null);
const longitud = ref(null);
const foto = ref(null);
const archivoFoto = ref(null);
const fileInput = ref(null);
const descripcion = ref("");
const historial = ref([]);
const enviando = ref(false);
const error = ref(null);
const mapVisible = ref(false);
const mapReady = ref(false);
const map = ref(null);
const marker = ref(null);
const router = useRouter();
const isOnline = ref(true);
const showModal = ref(false);

// Obtener información del usuario del localStorage
const user = computed(() => {
  const storedUser = localStorage.getItem("user");
  if (!storedUser) {
    router.push("/login");
    return {};
  }
  return JSON.parse(storedUser);
});

// Función para obtener las iniciales del usuario
const getUserInitials = computed(() => {
  if (user.value && user.value.nombre_completo) {
    const names = user.value.nombre_completo.split(' ');
    return names.length >= 2 ? 
      (names[0][0] + names[1][0]).toUpperCase() : 
      names[0].substring(0, 2).toUpperCase();
  }
  return 'US';
});

// Inicializar mapa cuando sea visible
function initMap() {
  if (!mapVisible.value) return;

  setTimeout(() => {
    if (!map.value) {
      map.value = L.map("map").setView([19.432608, -99.133209], 13);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(map.value);

      // Configurar iconos personalizados para los marcadores
      setupCustomIcons();
    }

    mapReady.value = true;

    if (latitud.value && longitud.value) {
      updateMapMarker();
    }
  }, 100);
}

// Configurar iconos personalizados con animación
function setupCustomIcons() {
  // Crear icono personalizado animado
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

  // Almacenar el icono para uso posterior
  window.customMapIcon = customIcon;
}

function updateMapMarker() {
  if (!map.value) return;

  // Si ya existe un marcador, actualizarlo
  if (marker.value) {
    marker.value.setLatLng([latitud.value, longitud.value]);
  } else {
    // Si no existe, crear uno nuevo con el icono personalizado
    const icon = window.customMapIcon || L.divIcon({
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
    
    marker.value = L.marker([latitud.value, longitud.value], { icon: icon }).addTo(map.value);
  }

  // Centrar el mapa en la ubicación con animación
  map.value.setView([latitud.value, longitud.value], 15, {
    animate: true,
    duration: 1
  });
}

function getUbicacion() {
  if (!navigator.geolocation) {
    error.value = "Tu navegador no soporta geolocalización";
    return;
  }

  mapVisible.value = true;
  initMap();

  navigator.geolocation.getCurrentPosition(
    (pos) => {
      latitud.value = pos.coords.latitude;
      longitud.value = pos.coords.longitude;
      error.value = null;

      // Actualizar marcador en el mapa
      updateMapMarker();
    },
    (err) => {
      error.value = "Error obteniendo ubicación: " + err.message;
    },
    { enableHighAccuracy: true }
  );
}

function onFileChange(e) {
  const file = e.target.files[0];
  if (!file) return;

  archivoFoto.value = file;
  const reader = new FileReader();
  reader.onload = (e2) => {
    foto.value = e2.target.result;
  };
  reader.readAsDataURL(file);
}

async function enviarRegistro() {
  if (!latitud.value || !longitud.value || !archivoFoto.value) {
    error.value = "Falta información: necesitas ubicación y foto";
    return;
  }

  // Verificar conexión a internet antes de enviar
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    error.value = getOfflineMessage();
    return;
  }

  enviando.value = true;
  error.value = null;

  try {
    // Crear FormData para enviar al servidor
    const formData = new FormData();
    formData.append("usuario_id", user.value.id.toString());
    formData.append("latitud", latitud.value);
    formData.append("longitud", longitud.value);
    formData.append("descripcion", descripcion.value);
    formData.append("foto", archivoFoto.value);

    // Enviar datos al backend
    const response = await axios.post(`${API_URL}/registro`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      timeout: 15000 // 15 segundos de timeout
    });

    // Guardar en historial local
    historial.value.unshift({
      fecha: new Date().toLocaleString(),
      latitud: latitud.value,
      longitud: longitud.value,
      descripcion: descripcion.value,
      foto: foto.value,
      backend: response.data,
    });

    // Limpiar campos
    descripcion.value = "";
    foto.value = null;
    archivoFoto.value = null;

    // No limpiamos la ubicación para permitir múltiples registros en el mismo lugar

    if (fileInput.value) {
      fileInput.value.value = ""; // Limpiar input file
    }    // Mostrar modal de éxito
    showModal.value = true;
  } catch (err) {
    console.error("Error al enviar datos:", err);
    if (err.response) {
      // Error de respuesta del servidor
      error.value = "Error del servidor: " + (err.response.data.detail || err.response.statusText);
    } else if (err.request) {
      // Error de conexión
      error.value = "No se pudo conectar con el servidor. Verifica tu conexión a internet.";
    } else {
      // Error general
      error.value = "Error al enviar datos: " + err.message;
    }
  } finally {
    enviando.value = false;
  }
}

// Comprobar si el usuario está autenticado y verificar conexión
onMounted(async () => {
  // Verificar si el usuario está autenticado
  if (!user.value.id) {
    router.push("/login");
    return;
  }
  
  // Verificar conexión a internet
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    error.value = getOfflineMessage();
  }
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<style>
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
