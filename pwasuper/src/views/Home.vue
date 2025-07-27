<template>
  <div class="page-container py-4">
    <!-- Sistema de Asistencia Integrado -->
    <div class="card mb-6">
      <div class="text-center mb-4">
        <h2 class="text-xl font-bold text-gray-800 mb-2">Sistema de Asistencia</h2>
        <p class="text-sm text-gray-500">
          {{ modoAsistencia ? 'Completa los datos para ' + (tipoAsistencia === 'entrada' ? 'marcar entrada' : 'marcar salida') : 'Marca tu entrada y salida del día' }}
        </p>
      </div>

      <!-- Botones de Asistencia (solo visibles cuando no está en modo asistencia) -->
      <div v-if="!modoAsistencia" class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
        <!-- Botón Marcar Entrada -->
        <button
          @click="iniciarAsistencia('entrada')"
          :disabled="entradaMarcada || verificandoAsistencia"
          class="relative overflow-hidden flex flex-col items-center justify-center p-6 rounded-xl transition-all duration-300 transform"
          :class="{
            'bg-green-500 text-white shadow-lg hover:bg-green-600 hover:scale-105 active:scale-95': !entradaMarcada && !verificandoAsistencia,
            'bg-gray-300 text-gray-500 cursor-not-allowed': entradaMarcada || verificandoAsistencia
          }"
        >
          <div v-if="verificandoAsistencia" class="absolute inset-0 bg-white bg-opacity-20 flex items-center justify-center rounded">
            <div class="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-current"></div>
          </div>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span class="font-semibold text-lg">
            <span v-if="asistenciaHoy && asistenciaHoy.entrada">
              Entrada: {{ formatearHora(asistenciaHoy.entrada) }}
            </span>
            <span v-else-if="entradaMarcada && datosEntrada.hora">
              Entrada: {{ datosEntrada.hora }}
            </span>
            <span v-else>
              Marcar Entrada
            </span>
          </span>
          <span v-if="entradaMarcada" class="text-xs mt-1 opacity-75">✓ Registrada</span>
          
          <!-- Mostrar resumen de entrada si está marcada -->
          <div v-if="datosEntrada.hora" class="mt-2 text-center">
            <p class="text-xs opacity-75">Entrada registrada:</p>
            <p class="text-sm font-mono font-bold">{{ datosEntrada.hora }}</p>
            <p class="text-xs opacity-75 mt-1">{{ datosEntrada.descripcion }}</p>
          </div>
        </button>

        <!-- Botón Marcar Salida -->
        <button
          @click="iniciarAsistencia('salida')"
          :disabled="!entradaMarcada || salidaMarcada || verificandoAsistencia"
          class="relative overflow-hidden flex flex-col items-center justify-center p-6 rounded-xl transition-all duration-300 transform"
          :class="{
            'bg-red-500 text-white shadow-lg hover:bg-red-600 hover:scale-105 active:scale-95': entradaMarcada && !salidaMarcada && !verificandoAsistencia,
            'bg-gray-300 text-gray-500 cursor-not-allowed': !entradaMarcada || salidaMarcada || verificandoAsistencia
          }"
        >
          <div v-if="verificandoAsistencia" class="absolute inset-0 bg-white bg-opacity-20 flex items-center justify-center rounded">
            <div class="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-current"></div>
          </div>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span class="font-semibold text-lg">
            <span v-if="asistenciaHoy && asistenciaHoy.salida">
              Salida: {{ formatearHora(asistenciaHoy.salida) }}
            </span>
            <span v-else-if="salidaMarcada && datosSalida.hora">
              Salida: {{ datosSalida.hora }}
            </span>
            <span v-else>
              Marcar Salida
            </span>
          </span>
          <span v-if="salidaMarcada" class="text-xs mt-1 opacity-75">✓ Registrada</span>
          <span v-else-if="!entradaMarcada" class="text-xs mt-1 opacity-75">Marca entrada primero</span>
          
          <!-- Mostrar resumen de salida si está marcada -->
          <div v-if="datosSalida.hora" class="mt-2 text-center">
            <p class="text-xs opacity-75">Salida registrada:</p>
            <p class="text-sm font-mono font-bold">{{ datosSalida.hora }}</p>
            <p class="text-xs opacity-75 mt-1">{{ datosSalida.descripcion }}</p>
          </div>
        </button>
      </div>

      <!-- Mensaje de estado de asistencia -->
      <div v-if="mensajeAsistencia && !modoAsistencia" class="text-center mb-4">
        <div 
          class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium"
          :class="{
            'bg-green-100 text-green-800': mensajeAsistencia.includes('éxito') || mensajeAsistencia.includes('registrada'),
            'bg-red-100 text-red-800': mensajeAsistencia.includes('Error') || mensajeAsistencia.includes('error'),
            'bg-yellow-100 text-yellow-800': mensajeAsistencia.includes('Ya')
          }"
        >
          <svg v-if="mensajeAsistencia.includes('éxito') || mensajeAsistencia.includes('registrada')" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <svg v-else-if="mensajeAsistencia.includes('Error') || mensajeAsistencia.includes('error')" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          {{ mensajeAsistencia }}
        </div>
      </div>
    </div>

    <!-- Formulario de Asistencia (solo visible en modo asistencia) -->
    <div v-if="modoAsistencia" class="card mb-4">
      <div class="text-center mb-6">
        <h2 class="text-xl font-bold text-gray-800 mb-2">
          {{ tipoAsistencia === 'entrada' ? 'Registrar Entrada' : 'Registrar Salida' }}
        </h2>
        <p class="text-sm text-gray-500">Completa todos los datos requeridos</p>
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

      <!-- Paso 1: Ubicación -->
      <div class="mb-6">
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-lg font-semibold text-gray-800">1. Ubicación</h3>
          <span v-if="latitud && longitud" class="text-green-600 text-sm">✓ Completado</span>
        </div>
        
        <button
          type="button"
          @click="getUbicacion"
          :disabled="obteniendoUbicacion"
          class="btn btn-secondary w-full mb-4 flex items-center justify-center"
          :class="{'opacity-50 cursor-not-allowed': obteniendoUbicacion}"
        >
          <div v-if="obteniendoUbicacion" class="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-current mr-2"></div>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          {{ obteniendoUbicacion ? 'Obteniendo ubicación...' : 'Obtener ubicación (funciona offline)' }}
        </button>

        <!-- Coordenadas -->
        <div v-if="latitud && longitud" class="bg-green-50 border border-green-200 rounded-lg p-3">
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
      </div>

      <!-- Paso 2: Foto -->
      <div class="mb-6">
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-lg font-semibold text-gray-800">2. Foto</h3>
          <span v-if="foto" class="text-green-600 text-sm">✓ Completado</span>
        </div>
        
        <div class="flex items-center justify-center w-full">
          <label class="flex flex-col w-full h-32 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50 active:bg-gray-100">
            <div v-if="!foto" class="flex flex-col items-center justify-center pt-7">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
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

      <!-- Paso 3: Descripción -->
      <div class="mb-6">
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-lg font-semibold text-gray-800">3. Descripción/Notas</h3>
          <span v-if="descripcion.trim()" class="text-green-600 text-sm">✓ Completado</span>
        </div>
        
        <textarea
          v-model="descripcion"
          rows="3"
          class="form-input"
          :placeholder="'Describe el lugar donde ' + (tipoAsistencia === 'entrada' ? 'inicias' : 'terminas') + ' tu jornada...'"
        ></textarea>
      </div>

      <!-- Botones de acción -->
      <div class="flex gap-3">
        <button
          @click="cancelarAsistencia"
          class="btn btn-secondary flex-1"
        >
          Cancelar
        </button>
        
        <button
          @click="confirmarAsistencia"
          :disabled="!puedeEnviarAsistencia || enviandoAsistencia"
          class="btn btn-primary flex-1 relative"
          :class="{'opacity-50 cursor-not-allowed': !puedeEnviarAsistencia || enviandoAsistencia}"
        >
          <div v-if="enviandoAsistencia" class="absolute inset-0 bg-white bg-opacity-20 flex items-center justify-center rounded">
            <div class="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></div>
          </div>
          <span>{{ tipoAsistencia === 'entrada' ? 'Registrar Entrada' : 'Registrar Salida' }}</span>
        </button>
      </div>

      <!-- Advertencia si faltan datos -->
      <div v-if="!puedeEnviarAsistencia" class="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
        <div class="flex items-center text-yellow-800">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <span class="text-sm font-medium">
            Faltan datos: 
            {{ !latitud || !longitud ? 'Ubicación' : '' }}
            {{ (!latitud || !longitud) && !foto ? ', ' : '' }}
            {{ !foto ? 'Foto' : '' }}
            {{ ((!latitud || !longitud) || !foto) && !descripcion.trim() ? ', ' : '' }}
            {{ !descripcion.trim() ? 'Descripción' : '' }}
          </span>
        </div>
      </div>
    </div>

    <!-- Formulario de registro normal (solo cuando no está en modo asistencia) -->
    <div v-if="!modoAsistencia" class="card mb-4">
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
          @click="getUbicacionRegistro"
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
          Obtener ubicación (funciona offline)
        </button>

        <!-- Coordenadas -->
        <div
          v-if="latitudRegistro && longitudRegistro"
          class="bg-green-50 border border-green-200 rounded-lg p-3 mb-4"
        >
          <div class="grid grid-cols-2 gap-3">
            <div>
              <p class="text-xs text-gray-500">Latitud</p>
              <p class="font-mono text-sm font-medium text-gray-800">{{ latitudRegistro }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Longitud</p>
              <p class="font-mono text-sm font-medium text-gray-800">{{ longitudRegistro }}</p>
            </div>
          </div>
        </div>

        <!-- Input de archivo para foto -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">Foto</label>
          <div class="flex items-center justify-center w-full">
            <label class="flex flex-col w-full h-32 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50 active:bg-gray-100">
              <div v-if="!fotoRegistro" class="flex flex-col items-center justify-center pt-7">
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
                <img :src="fotoRegistro" class="h-full object-contain" />
              </div>
              <input
                type="file"
                accept="image/*"
                @change="onFileChangeRegistro"
                class="hidden"
                ref="fileInputRegistro"
              />
            </label>
          </div>
        </div>

        <!-- Descripción -->
        <div class="mb-4">
          <label for="descripcionRegistro" class="block text-sm font-medium text-gray-700 mb-2">Descripción</label>
          <textarea
            v-model="descripcionRegistro"
            id="descripcionRegistro"
            rows="3"
            class="form-input"
            placeholder="Describe el lugar o añade notas..."
          ></textarea>
        </div>

        <!-- Botón enviar -->
        <button
          type="submit"
          :disabled="!latitudRegistro || !longitudRegistro || !fotoRegistro || enviando"
          :class="['btn w-full', !latitudRegistro || !longitudRegistro || !fotoRegistro || enviando ? 'bg-gray-400 cursor-not-allowed' : 'btn-primary']"
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

    <!-- Mensajes de error/información -->
    <transition name="fade">
      <div
        v-if="error"
        :class="isInfoMessage ? 
          'mb-4 bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4 rounded' : 
          'mb-4 bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded'"
        role="alert"
      >
        <p class="font-bold">{{ isInfoMessage ? 'Información' : 'Error' }}</p>
        <p>{{ error }}</p>
      </div>
    </transition>

    <!-- Historial reciente (solo cuando no está en modo asistencia) -->
    <div v-if="historial.length > 0 && !modoAsistencia" class="card">
      <h3 class="text-lg font-semibold text-gray-800 mb-3">Registros recientes</h3>
      <div class="space-y-3">
        <div
          v-for="(r, i) in historial.slice(0, 3)"
          :key="i"
          class="border border-gray-200 rounded-lg p-3 hover:shadow-md transition-shadow relative"
          :class="{ 'border-orange-300 bg-orange-50': r.offline }"
        >
          <!-- Indicador de estado offline -->
          <div v-if="r.offline" class="absolute top-2 right-2">
            <div class="flex items-center text-orange-600 text-xs">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Pendiente
            </div>
          </div>
          
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
              <p v-if="r.offline" class="text-xs text-orange-600 mt-1 font-medium">
                ⏳ Se enviará al recuperar conexión
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
      :message="modalMessage"
      @close="closeSuccessModal"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { API_URL, checkInternetConnection, getOfflineMessage } from '../utils/network.js';
import Modal from '../components/Modal.vue';
import asistenciasService from '../services/asistenciasService.js';
import offlineService from '../services/offlineService.js';
import syncService from '../services/syncService.js';
import geoLocationService from '../services/geoLocationService.js';
import { obtenerUbicacionSimple } from '../services/geoLocationSimple.js';

// Referencias y estado para asistencia
const modoAsistencia = ref(false);
const tipoAsistencia = ref(''); // 'entrada' o 'salida'
const entradaMarcada = ref(false);
const salidaMarcada = ref(false);
const enviandoAsistencia = ref(false);
const obteniendoUbicacion = ref(false);
const mensajeAsistencia = ref('');
const datosEntrada = ref({});
const datosSalida = ref({});
const asistenciaHoy = ref(null);
const verificandoAsistencia = ref(false);

// Referencias y estado para asistencia (datos del formulario)
const latitud = ref(null);
const longitud = ref(null);
const foto = ref(null);
const archivoFoto = ref(null);
const descripcion = ref("");

// Referencias y estado para registro normal
const latitudRegistro = ref(null);
const longitudRegistro = ref(null);
const fotoRegistro = ref(null);
const archivoFotoRegistro = ref(null);
const descripcionRegistro = ref("");

// Referencias generales
const fileInput = ref(null);
const fileInputRegistro = ref(null);
const historial = ref([]);
const enviando = ref(false);
const error = ref(null);
const router = useRouter();
const isOnline = ref(true);
const showModal = ref(false);
const modalMessage = ref('');

// Obtener información del usuario del localStorage
const user = computed(() => {
  const storedUser = localStorage.getItem("user");
  if (!storedUser) {
    router.push("/login");
    return {};
  }
  return JSON.parse(storedUser);
});

// Determinar si el mensaje es de tipo información (sin conexión) o error
const isInfoMessage = computed(() => {
  return error.value && error.value.includes('Sin conexión');
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

// Computed para verificar si se pueden enviar los datos de asistencia
const puedeEnviarAsistencia = computed(() => {
  return latitud.value && longitud.value && foto.value && descripcion.value.trim();
});

// Funciones para el sistema de asistencia
function iniciarAsistencia(tipo) {
  modoAsistencia.value = true;
  tipoAsistencia.value = tipo;
  limpiarDatosAsistencia();
  error.value = null;
  mensajeAsistencia.value = '';
}

function limpiarDatosAsistencia() {
  latitud.value = null;
  longitud.value = null;
  foto.value = null;
  archivoFoto.value = null;
  descripcion.value = "";
  
  if (fileInput.value) {
    fileInput.value.value = "";
  }
}

function cancelarAsistencia() {
  modoAsistencia.value = false;
  tipoAsistencia.value = '';
  limpiarDatosAsistencia();
}

async function confirmarAsistencia() {
  if (!puedeEnviarAsistencia.value || enviandoAsistencia.value) return;
  
  enviandoAsistencia.value = true;
  error.value = null;
  
  try {
    // Verificar conexión a internet antes de enviar
    isOnline.value = await checkInternetConnection();
    
    if (!isOnline.value) {
      // **MODO OFFLINE: Guardar datos localmente**
      console.log('📴 Sin conexión - Guardando asistencia offline');
      
      // Guardar en almacenamiento offline usando IndexedDB
      await offlineService.guardarAsistenciaOffline(
        user.value.id,
        tipoAsistencia.value,
        latitud.value,
        longitud.value,
        descripcion.value,
        archivoFoto.value
      );
      
      // Simular datos de respuesta para el estado local
      const horaActual = new Date().toLocaleTimeString('es-MX', {
        hour: '2-digit',
        minute: '2-digit',
        timeZone: 'America/Mexico_City'
      });
      
      // Actualizar estado local
      if (tipoAsistencia.value === 'entrada') {
        entradaMarcada.value = true;
        datosEntrada.value = {
          hora: horaActual,
          descripcion: descripcion.value,
          latitud: latitud.value,
          longitud: longitud.value,
          foto_url: foto.value // URL local temporal
        };
      } else {
        salidaMarcada.value = true;
        datosSalida.value = {
          hora: horaActual,
          descripcion: descripcion.value,
          latitud: latitud.value,
          longitud: longitud.value,
          foto_url: foto.value // URL local temporal
        };
      }
      
      // Mostrar mensaje informativo offline
      mensajeAsistencia.value = `${tipoAsistencia.value === 'entrada' ? 'Entrada' : 'Salida'} guardada offline. Se enviará automáticamente cuando tengas conexión.`;
      modalMessage.value = `¡${tipoAsistencia.value === 'entrada' ? 'Entrada' : 'Salida'} guardada! Se sincronizará cuando recuperes la conexión.`;
      showModal.value = true;
      
      // Salir del modo asistencia
      modoAsistencia.value = false;
      tipoAsistencia.value = '';
      limpiarDatosAsistencia();
      
      // Guardar estado en localStorage
      guardarEstadoAsistencia();
      
      // Limpiar mensaje después de 8 segundos (más tiempo para modo offline)
      setTimeout(() => {
        mensajeAsistencia.value = '';
      }, 8000);
      
      return;
    }

    // **MODO ONLINE: Enviar directamente al servidor**
    console.log('🌐 Conexión disponible - Enviando asistencia al servidor');
    
    // Crear timestamp de registro (hora exacta en que se hace el registro)
    const timestampRegistro = new Date().toISOString();
    console.log('🕐 Timestamp de registro online:', timestampRegistro);
    
    // Crear FormData para enviar al servidor
    const formData = new FormData();
    formData.append("usuario_id", user.value.id.toString());
    formData.append("latitud", latitud.value);
    formData.append("longitud", longitud.value);
    formData.append("descripcion", descripcion.value);
    formData.append("foto", archivoFoto.value);
    formData.append("timestamp_registro", timestampRegistro); // Hora exacta del registro

    // Determinar endpoint según tipo de asistencia y usar el servicio
    let response;
    if (tipoAsistencia.value === 'entrada') {
      response = await asistenciasService.registrarEntrada(formData);
    } else {
      response = await asistenciasService.registrarSalida(formData);
    }

    // Procesar respuesta exitosa
    if (tipoAsistencia.value === 'entrada') {
      entradaMarcada.value = true;
      datosEntrada.value = {
        hora: new Date(response.hora_entrada).toLocaleTimeString('es-MX', {
          hour: '2-digit',
          minute: '2-digit',
          timeZone: 'America/Mexico_City'
        }),
        descripcion: response.descripcion,
        latitud: response.latitud,
        longitud: response.longitud,
        foto_url: response.foto_url
      };
    } else {
      salidaMarcada.value = true;
      datosSalida.value = {
        hora: new Date(response.hora_salida).toLocaleTimeString('es-MX', {
          hour: '2-digit',
          minute: '2-digit',
          timeZone: 'America/Mexico_City'
        }),
        descripcion: response.descripcion,
        latitud: response.latitud,
        longitud: response.longitud,
        foto_url: response.foto_url
      };
    }

    // Mostrar mensaje de éxito
    mensajeAsistencia.value = response.mensaje;
    modalMessage.value = `¡${tipoAsistencia.value === 'entrada' ? 'Entrada' : 'Salida'} registrada exitosamente!`;
    showModal.value = true;
    
    // Salir del modo asistencia
    modoAsistencia.value = false;
    tipoAsistencia.value = '';
    limpiarDatosAsistencia();
    
    // Guardar estado en localStorage
    guardarEstadoAsistencia();
    
    // Verificar asistencia con el backend para actualizar datos
    await verificarAsistenciaHoy();
    
    // Limpiar mensaje después de 5 segundos
    setTimeout(() => {
      mensajeAsistencia.value = '';
    }, 5000);

  } catch (err) {
    console.error('Error al enviar asistencia:', err);
    if (err.response) {
      error.value = "Error del servidor: " + (err.response.data.detail || err.response.statusText);
      
      // Si ya existe registro, actualizar estado
      if (err.response.data.detail && err.response.data.detail.includes('Ya existe')) {
        if (tipoAsistencia.value === 'entrada') {
          entradaMarcada.value = true;
        } else {
          salidaMarcada.value = true;
        }
        
        // Actualizar datos desde el servidor
        await verificarAsistenciaHoy();
      }
    } else if (err.request) {
      error.value = "No se pudo conectar con el servidor. Verifica tu conexión a internet.";
    } else {
      error.value = "Error al enviar datos: " + err.message;
    }
  } finally {
    enviandoAsistencia.value = false;
  }
}

async function getUbicacion() {
  obteniendoUbicacion.value = true;
  error.value = null;

  try {
    console.log('🔍 Iniciando obtención de ubicación...');
    
    // Primero intentar con el servicio complejo
    try {
      const location = await geoLocationService.getLocationSmart({
        timeout: 6000, // 6 segundos de timeout
        enableHighAccuracy: true,
        useCache: true
      });

      console.log('📍 Ubicación recibida del servicio principal:', location);

      latitud.value = location.latitude;
      longitud.value = location.longitude;
      
      // Verificar que tenemos coordenadas válidas
      if (!latitud.value || !longitud.value) {
        throw new Error('Coordenadas inválidas del servicio principal');
      }
      
      console.log('✅ Ubicación establecida con servicio principal');
      return;
      
    } catch (serviceError) {
      console.warn('⚠️ Servicio principal falló, usando servicio simple:', serviceError.message);
      
      // Fallback al servicio simple
      const simpleLocation = await obtenerUbicacionSimple();
      
      latitud.value = simpleLocation.latitude;
      longitud.value = simpleLocation.longitude;
      
      console.log('✅ Ubicación establecida con servicio simple:', simpleLocation);
      
      // Mostrar mensaje según el origen
      if (simpleLocation.source === 'default') {
        error.value = 'Se usó una ubicación aproximada. Para mayor precisión, permite el acceso a la ubicación en tu navegador.';
        setTimeout(() => error.value = null, 5000);
      } else if (simpleLocation.source === 'cache') {
        console.log('📍 Ubicación del caché simple usada');
      }
    }
    
  } catch (err) {
    console.error('❌ Todos los servicios fallaron:', err);
    
    // Último recurso: coordenadas fijas
    console.log('🆘 Aplicando ubicación de emergencia final...');
    latitud.value = 19.4326; // Ciudad de México
    longitud.value = -99.1332;
    
    error.value = 'Se usó una ubicación por defecto. Verifica los permisos de ubicación en tu navegador.';
    setTimeout(() => error.value = null, 7000);
    
  } finally {
    obteniendoUbicacion.value = false;
  }
}

async function getUbicacionRegistro() {
  error.value = null;

  try {
    console.log('🔍 Iniciando obtención de ubicación para registro...');
    
    // Primero intentar con el servicio complejo
    try {
      const location = await geoLocationService.getLocationSmart({
        timeout: 6000, // 6 segundos de timeout
        enableHighAccuracy: true,
        useCache: true
      });

      console.log('📍 Ubicación para registro recibida del servicio principal:', location);

      latitudRegistro.value = location.latitude;
      longitudRegistro.value = location.longitude;
      
      // Verificar que tenemos coordenadas válidas
      if (!latitudRegistro.value || !longitudRegistro.value) {
        throw new Error('Coordenadas inválidas del servicio principal');
      }
      
      console.log('✅ Ubicación para registro establecida con servicio principal');
      return;
      
    } catch (serviceError) {
      console.warn('⚠️ Servicio principal falló para registro, usando servicio simple:', serviceError.message);
      
      // Fallback al servicio simple
      const simpleLocation = await obtenerUbicacionSimple();
      
      latitudRegistro.value = simpleLocation.latitude;
      longitudRegistro.value = simpleLocation.longitude;
      
      console.log('✅ Ubicación para registro establecida con servicio simple:', simpleLocation);
      
      // Mostrar mensaje según el origen
      if (simpleLocation.source === 'default') {
        error.value = 'Se usó una ubicación aproximada para el registro.';
        setTimeout(() => error.value = null, 4000);
      }
    }
    
  } catch (err) {
    console.error('❌ Todos los servicios fallaron para registro:', err);
    
    // Último recurso: coordenadas fijas
    console.log('🆘 Aplicando ubicación de emergencia para registro...');
    latitudRegistro.value = 19.4326; // Ciudad de México
    longitudRegistro.value = -99.1332;
    
    error.value = 'Se usó una ubicación por defecto para el registro.';
    setTimeout(() => error.value = null, 4000);
  }
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

function onFileChangeRegistro(e) {
  const file = e.target.files[0];
  if (!file) return;

  archivoFotoRegistro.value = file;
  const reader = new FileReader();
  reader.onload = (e2) => {
    fotoRegistro.value = e2.target.result;
  };
  reader.readAsDataURL(file);
}

async function enviarRegistro() {
  if (!latitudRegistro.value || !longitudRegistro.value || !archivoFotoRegistro.value) {
    error.value = "Falta información: necesitas ubicación y foto";
    return;
  }

  enviando.value = true;
  error.value = null;

  try {
    // Verificar conexión a internet antes de enviar
    isOnline.value = await checkInternetConnection();
    
    if (!isOnline.value) {
      // **MODO OFFLINE: Guardar datos localmente**
      console.log('📴 Sin conexión - Guardando registro offline');
      
      // Guardar en almacenamiento offline usando IndexedDB
      await offlineService.guardarRegistroOffline(
        user.value.id,
        latitudRegistro.value,
        longitudRegistro.value,
        descripcionRegistro.value,
        archivoFotoRegistro.value
      );
      
      // Agregar a historial local con indicador offline
      historial.value.unshift({
        fecha: new Date().toLocaleString(),
        latitud: latitudRegistro.value,
        longitud: longitudRegistro.value,
        descripcion: descripcionRegistro.value,
        foto: fotoRegistro.value,
        offline: true, // Marcador para indicar que está pendiente
        backend: null,
      });

      // Limpiar campos
      descripcionRegistro.value = "";
      fotoRegistro.value = null;
      archivoFotoRegistro.value = null;
      latitudRegistro.value = null;
      longitudRegistro.value = null;

      if (fileInputRegistro.value) {
        fileInputRegistro.value.value = "";
      }

      // Mostrar modal de éxito offline
      modalMessage.value = "¡Registro guardado offline! Se enviará automáticamente cuando recuperes la conexión.";
      showModal.value = true;
      
      return;
    }

    // **MODO ONLINE: Enviar directamente al servidor**
    console.log('🌐 Conexión disponible - Enviando registro al servidor');

    // Crear FormData para enviar al servidor
    const formData = new FormData();
    formData.append("usuario_id", user.value.id.toString());
    formData.append("latitud", latitudRegistro.value);
    formData.append("longitud", longitudRegistro.value);
    formData.append("descripcion", descripcionRegistro.value);
    formData.append("foto", archivoFotoRegistro.value);

    // Enviar datos al backend
    const response = await axios.post(`${API_URL}/registro`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      timeout: 15000,
      maxContentLength: Infinity,
      maxBodyLength: Infinity
    });

    // Guardar en historial local
    historial.value.unshift({
      fecha: new Date().toLocaleString(),
      latitud: latitudRegistro.value,
      longitud: longitudRegistro.value,
      descripcion: descripcionRegistro.value,
      foto: fotoRegistro.value,
      offline: false, // Enviado exitosamente
      backend: response.data,
    });

    // Limpiar campos
    descripcionRegistro.value = "";
    fotoRegistro.value = null;
    archivoFotoRegistro.value = null;
    latitudRegistro.value = null;
    longitudRegistro.value = null;

    if (fileInputRegistro.value) {
      fileInputRegistro.value.value = "";
    }

    // Mostrar modal de éxito
    modalMessage.value = "¡Registro enviado y guardado correctamente!";
    showModal.value = true;
    
  } catch (err) {
    console.error("Error al enviar datos:", err);
    if (err.response) {
      error.value = "Error del servidor: " + (err.response.data.detail || err.response.statusText);
    } else if (err.request) {
      error.value = "No se pudo conectar con el servidor. Verifica tu conexión a internet.";
    } else {
      error.value = "Error al enviar datos: " + err.message;
    }
  } finally {
    enviando.value = false;
  }
}

function closeSuccessModal() {
  showModal.value = false;
  modalMessage.value = '';
}

function verificarEstadoAsistencia() {
  try {
    const ahora = new Date();
    const fechaHoy = ahora.toISOString().split('T')[0];
    
    // Cada día es un nuevo registro, así que primero limpiamos los estados
    entradaMarcada.value = false;
    salidaMarcada.value = false;
    datosEntrada.value = {};
    datosSalida.value = {};
    
    // Verificamos si hay datos guardados para el día de hoy específicamente
    const estadoHoy = localStorage.getItem(`asistencia_${user.value.id}_${fechaHoy}`);
    
    if (estadoHoy) {
      const datos = JSON.parse(estadoHoy);
      entradaMarcada.value = datos.entradaMarcada || false;
      salidaMarcada.value = datos.salidaMarcada || false;
      datosEntrada.value = datos.datosEntrada || {};
      datosSalida.value = datos.datosSalida || {};
    }

    // Limpiamos datos de días anteriores para no acumular basura en localStorage
    limpiarDatosAntiguos();

    // Después de cargar del localStorage, verificar con el backend
    verificarAsistenciaHoy();
  } catch (error) {
    console.error('Error al verificar estado de asistencia:', error);
  }
}

/**
 * Limpia los datos de asistencia de días anteriores del localStorage
 */
function limpiarDatosAntiguos() {
  try {
    const hoy = new Date().toISOString().split('T')[0];
    
    // Recorremos todas las claves del localStorage
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      
      // Si es una clave de asistencia para este usuario pero no de hoy, la eliminamos
      if (key && key.startsWith(`asistencia_${user.value.id}_`) && !key.includes(hoy)) {
        localStorage.removeItem(key);
        console.log(`🧹 Eliminando datos antiguos: ${key}`);
      }
    }
  } catch (error) {
    console.error('Error al limpiar datos antiguos:', error);
  }
}

/**
 * Consulta al backend si el usuario ya registró entrada/salida hoy
 */
async function verificarAsistenciaHoy() {
  verificandoAsistencia.value = true;
  try {
    // Verificar conexión a internet antes de consultar
    isOnline.value = await checkInternetConnection();
    if (!isOnline.value) {
      console.log('Sin conexión, usando datos locales de asistencia');
      return;
    }

    // Obtener la fecha actual para comparar
    const fechaActual = new Date().toISOString().split('T')[0];
    
    const datos = await asistenciasService.consultarAsistenciaHoy(user.value.id);
    asistenciaHoy.value = datos;
    
    // Verificar que los datos correspondan al día actual
    if (datos.fecha && datos.fecha === fechaActual) {
      // Actualizar estado de botones según la respuesta del backend
      if (datos.entrada) {
        entradaMarcada.value = true;
        datosEntrada.value = {
          hora: formatearHora(datos.entrada),
          descripcion: datos.descripcion_entrada || '',
          latitud: datos.latitud_entrada,
          longitud: datos.longitud_entrada,
          foto_url: datos.foto_entrada_url
        };
      } else {
        // Si no hay entrada registrada hoy, resetear estado
        entradaMarcada.value = false;
        datosEntrada.value = {};
      }
      
      if (datos.salida) {
        salidaMarcada.value = true;
        datosSalida.value = {
          hora: formatearHora(datos.salida),
          descripcion: datos.descripcion_salida || '',
          latitud: datos.latitud_salida,
          longitud: datos.longitud_salida,
          foto_url: datos.foto_salida_url
        };
      } else {
        // Si no hay salida registrada hoy, resetear estado de salida
        salidaMarcada.value = false;
        datosSalida.value = {};
      }
      
      // Guardar estado actualizado
      guardarEstadoAsistencia();
    } else {
      console.log('Sin registros para el día de hoy. Reiniciando estados.');
      // Es un nuevo día, reiniciar estados
      entradaMarcada.value = false;
      salidaMarcada.value = false;
      datosEntrada.value = {};
      datosSalida.value = {};
      guardarEstadoAsistencia();
    }
  } catch (error) {
    console.error('Error al verificar asistencia de hoy:', error);
    // Si hay error de conexión pero es un nuevo día, reiniciar estados
    const fechaGuardada = localStorage.getItem(`asistencia_ultima_fecha_${user.value.id}`);
    const fechaActual = new Date().toISOString().split('T')[0];
    
    if (fechaGuardada !== fechaActual) {
      // Es un nuevo día, reiniciar estados incluso sin conexión
      entradaMarcada.value = false;
      salidaMarcada.value = false;
      datosEntrada.value = {};
      datosSalida.value = {};
      guardarEstadoAsistencia();
    }
  } finally {
    verificandoAsistencia.value = false;
  }
}

/**
 * Formatea una fecha ISO a formato de hora local
 */
function formatearHora(fechaISO) {
  if (!fechaISO) return "";
  const hora = new Date(fechaISO);
  return hora.toLocaleTimeString("es-MX", { hour: '2-digit', minute: '2-digit', timeZone: 'America/Mexico_City' });
}

function guardarEstadoAsistencia() {
  const ahora = new Date();
  const fechaHoy = ahora.toISOString().split('T')[0];
  
  const estado = {
    entradaMarcada: entradaMarcada.value,
    salidaMarcada: salidaMarcada.value,
    datosEntrada: datosEntrada.value,
    datosSalida: datosSalida.value,
    ultimaActualizacion: ahora.toISOString()
  };
  
  // Guardar el estado del día actual
  localStorage.setItem(`asistencia_${user.value.id}_${fechaHoy}`, JSON.stringify(estado));
  
  // También guardar la última fecha consultada para comparaciones
  localStorage.setItem(`asistencia_ultima_fecha_${user.value.id}`, fechaHoy);
}

// Comprobar si el usuario está autenticado y verificar conexión
onMounted(async () => {
  // Verificar si el usuario está autenticado
  if (!user.value.id) {
    router.push("/login");
    return;
  }
  
  // Verificar estado de asistencia del día
  verificarEstadoAsistencia();
  
  // Verificar conexión a internet
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    error.value = getOfflineMessage();
  }
  
  // Verificar estado del servicio de geolocalización
  console.log('🔍 Verificando servicio de geolocalización...');
  try {
    const geoStatus = geoLocationService.getStatus();
    console.log('📊 Estado del servicio de geolocalización:', geoStatus);
    
    // Si no hay ubicación conocida, intentar obtenerla de forma silenciosa
    if (!geoStatus.hasLastKnownLocation) {
      console.log('⚠️ No hay ubicación conocida, estableciendo por defecto...');
      geoLocationService.setDefaultLocation();
    }
  } catch (error) {
    console.error('❌ Error verificando servicio de geolocalización:', error);
  }
});

// Watcher para guardar cambios de asistencia en localStorage
watch([entradaMarcada, salidaMarcada, datosEntrada, datosSalida], () => {
  if (user.value.id) {
    guardarEstadoAsistencia();
  }
}, { deep: true });
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
