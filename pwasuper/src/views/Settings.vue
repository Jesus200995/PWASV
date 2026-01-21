<template>
  <div class="fixed inset-0 bg-gradient-to-br from-indigo-50 via-blue-50 to-purple-50 overflow-hidden" style="z-index: 0;">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 right-1/4 w-72 h-72 bg-indigo-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute bottom-1/3 left-1/4 w-80 h-80 bg-purple-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute top-2/3 right-1/3 w-64 h-64 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>

    <div class="absolute inset-0 overflow-y-auto pt-16 sm:pt-20 pb-4">
      <div class="page-container relative z-10 px-2 sm:px-3 md:px-4 lg:px-6 xl:px-8 py-3 sm:py-4 lg:py-5 min-h-full max-w-full">
        <div class="w-full max-w-lg mx-auto space-y-4">
        <!-- Header de la página -->
        <div class="glass-card">
          <div class="flex items-center gap-2 mb-2">
            <button
              @click="$router.back()"
              class="p-1.5 rounded-lg hover:bg-white/20 transition-colors flex-shrink-0"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <div class="flex-1 min-w-0">
              <h1 class="text-lg font-bold text-gray-900">Configuración</h1>
              <p class="text-xs text-gray-500">Personaliza tu experiencia</p>
            </div>
          </div>
          <div class="h-1 bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 rounded-full"></div>
        </div>

        <!-- Sección: Almacenamiento en Caché -->
        <div class="glass-card">
          <div class="flex items-center gap-2 mb-4">
            <div class="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-orange-400 to-red-500 flex items-center justify-center shadow-lg">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4m0 0L4 7m16 0l-8 4m0 0l-8-4" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <h2 class="text-base font-bold text-gray-900">Caché de la App</h2>
              <p class="text-xs text-gray-600">Libera espacio en tu dispositivo</p>
            </div>
          </div>
          <div class="green-line mb-4"></div>

          <!-- Información de caché -->
          <div class="bg-white/40 backdrop-filter backdrop-blur-sm rounded-xl p-3 mb-4 border border-white/20">
            <div class="space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-700 font-medium">Tamaño del caché</span>
                <span class="text-sm font-bold text-indigo-600">{{ cacheSize }}</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-1.5 overflow-hidden">
                <div
                  class="h-full bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 transition-all duration-500"
                  :style="{ width: cachePercentage + '%' }"
                ></div>
              </div>
              <p class="text-xs text-gray-600">
                {{ itemCount }} archivo(s) almacenado(s)
              </p>
            </div>
          </div>

          <!-- Descripción de qué se borrará -->
          <div class="bg-blue-50 border-l-4 border-blue-500 rounded-r-lg p-2.5 mb-4 text-sm">
            <div class="flex items-start gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <p class="font-medium text-blue-900 text-xs mb-1">Se eliminará:</p>
                <ul class="text-xs text-blue-800 space-y-0.5">
                  <li>✓ Imágenes en caché</li>
                  <li>✓ Datos temporales offline</li>
                  <li>✓ Archivos de respaldo</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Botón de limpiar caché -->
          <button
            @click="showConfirmDialog = true"
            :disabled="isClearing || itemCount === 0"
            class="w-full py-2.5 px-3 bg-gradient-to-r from-orange-500 via-orange-600 to-red-600 text-white font-bold text-sm rounded-xl hover:shadow-lg transition-all duration-300 transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center justify-center gap-2"
          >
            <svg v-if="!isClearing" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ isClearing ? 'Borrando...' : itemCount === 0 ? 'Caché vacío' : 'Borrar Caché' }}</span>
          </button>
        </div>

        <!-- Sección: Base de Datos Local -->
        <div class="glass-card">
          <div class="flex items-center gap-2 mb-4">
            <div class="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-green-400 to-emerald-600 flex items-center justify-center shadow-lg">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <h2 class="text-base font-bold text-gray-900">Base de Datos Local</h2>
              <p class="text-xs text-gray-600">IndexedDB y LocalStorage</p>
            </div>
          </div>
          <div class="green-line mb-4"></div>

          <!-- Información de BD -->
          <div class="bg-white/40 backdrop-filter backdrop-blur-sm rounded-xl p-3 mb-4 border border-white/20">
            <div class="space-y-2 text-sm text-gray-700">
              <div class="flex justify-between items-center">
                <span class="font-medium">Estado:</span>
                <span class="flex items-center gap-1">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  <span class="text-xs">Disponible</span>
                </span>
              </div>
              <div class="flex justify-between items-center">
                <span class="font-medium">Pendientes:</span>
                <span class="font-bold text-amber-600 text-xs">{{ pendingRecords }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="font-medium">Sincronizados:</span>
                <span class="font-bold text-green-600 text-xs">{{ syncedRecords }}</span>
              </div>
            </div>
          </div>

          <!-- Info de sincronización -->
          <div v-if="pendingRecords > 0" class="bg-amber-50 border-l-4 border-amber-500 rounded-r-lg p-2.5 mb-4 text-sm">
            <div class="flex items-start gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-amber-600 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <p class="text-xs font-medium text-amber-900">{{ pendingRecords }} registro(s) pendiente(s)</p>
                <p class="text-xs text-amber-800 mt-0.5">Se sincronizarán cuando recuperes conexión</p>
              </div>
            </div>
          </div>

          <div v-else class="bg-green-50 border-l-4 border-green-500 rounded-r-lg p-2.5 mb-4 text-sm">
            <div class="flex items-start gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
              <div>
                <p class="text-xs font-medium text-green-900">¡Todo sincronizado!</p>
                <p class="text-xs text-green-800 mt-0.5">Todos tus registros están en la nube</p>
              </div>
            </div>
          </div>

          <!-- Botón para ver información detallada -->
          <button
            @click="showDatabaseInfo = !showDatabaseInfo"
            class="w-full py-2.5 px-3 text-indigo-600 font-medium text-sm rounded-lg border-2 border-indigo-200 hover:bg-indigo-50 transition-colors"
          >
            {{ showDatabaseInfo ? 'Ocultar' : 'Ver' }} Detalles
          </button>

          <!-- Información detallada (expandible) -->
          <transition name="expand">
            <div v-if="showDatabaseInfo" class="mt-3 pt-3 border-t border-white/30 space-y-2.5">
              <div class="bg-blue-50/50 rounded-lg p-3 text-xs">
                <p class="font-medium text-blue-900 mb-1.5">📦 Registros Almacenados</p>
                <ul class="text-blue-800 space-y-1 text-xs">
                  <li>• Actividades de campo y gabinete</li>
                  <li>• Fotografías comprimidas</li>
                  <li>• Coordenadas GPS</li>
                  <li>• Descripción y metadata</li>
                </ul>
              </div>
              <div class="bg-purple-50/50 rounded-lg p-3 text-xs">
                <p class="font-medium text-purple-900 mb-1.5">🔄 Sincronización</p>
                <ul class="text-purple-800 space-y-1 text-xs">
                  <li>• Sincronización automática</li>
                  <li>• Reintentos inteligentes</li>
                  <li>• Validación de datos</li>
                  <li>• Historial completo</li>
                </ul>
              </div>
            </div>
          </transition>
        </div>

        <!-- Sección: Información de la App -->
        <div class="glass-card">
          <div class="flex items-center gap-2 mb-4">
            <div class="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-indigo-400 to-blue-600 flex items-center justify-center shadow-lg">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <h2 class="text-base font-bold text-gray-900">Información</h2>
              <p class="text-xs text-gray-600">Detalles de la aplicación</p>
            </div>
          </div>
          <div class="green-line mb-4"></div>

          <div class="space-y-3">
            <div class="flex justify-between items-center p-3 bg-white/40 backdrop-filter backdrop-blur-sm rounded-lg border border-white/20 text-sm">
              <span class="font-medium text-gray-700">Versión</span>
              <span class="font-bold text-indigo-600 text-xs">v1.0.0</span>
            </div>
            <div class="flex justify-between items-center p-3 bg-white/40 backdrop-filter backdrop-blur-sm rounded-lg border border-white/20 text-sm">
              <span class="font-medium text-gray-700">Compilación</span>
              <span class="text-xs font-mono text-gray-600">{{ buildDate }}</span>
            </div>
            <div class="flex justify-between items-center p-3 bg-white/40 backdrop-filter backdrop-blur-sm rounded-lg border border-white/20 text-sm">
              <span class="font-medium text-gray-700">Navegador</span>
              <span class="text-xs font-mono text-gray-600">{{ browserInfo }}</span>
            </div>
          </div>
        </div>

        <!-- Espaciador final -->
        <div class="h-4"></div>
        </div>
      </div>
    </div>

    <!-- Modal de confirmación -->
    <div v-if="showConfirmDialog" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-3">
      <div class="glass-card max-w-sm w-full transform transition-all">
        <div class="flex items-center gap-2 mb-2">
          <div class="flex-shrink-0 w-8 h-8 rounded-full bg-red-100 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4v2m0 4v2m0-14a9 9 0 100 18 9 9 0 000-18z" />
            </svg>
          </div>
          <h3 class="text-base font-bold text-gray-900">¿Borrar caché?</h3>
        </div>

        <p class="text-xs text-gray-700 mb-3 leading-relaxed">
          Se eliminarán {{ itemCount }} archivo(s) y se liberarán {{ cacheSize }}. Esta acción es irreversible.
        </p>

        <div class="flex gap-2">
          <button
            @click="showConfirmDialog = false"
            class="flex-1 py-2 px-3 rounded-lg border-2 border-gray-300 text-gray-700 font-medium text-sm hover:bg-gray-50 transition-colors"
          >
            Cancelar
          </button>
          <button
            @click="clearCache"
            class="flex-1 py-2 px-3 rounded-lg bg-gradient-to-r from-red-500 to-orange-600 text-white font-medium text-sm hover:shadow-lg transition-all active:scale-95"
          >
            Sí, Borrar
          </button>
        </div>
      </div>
    </div>

    <!-- Toast de notificación -->
    <transition name="slide-up">
      <div v-if="showToast" class="fixed bottom-4 left-3 right-3 max-w-sm mx-auto z-50">
        <div class="glass-card flex items-center gap-2 p-3 rounded-xl border-l-4 text-sm" :class="{
          'border-green-500 bg-green-50/50': toastType === 'success',
          'border-red-500 bg-red-50/50': toastType === 'error',
          'border-blue-500 bg-blue-50/50': toastType === 'info'
        }">
          <svg v-if="toastType === 'success'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
          </svg>
          <svg v-else-if="toastType === 'error'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-red-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="font-medium flex-1" :class="{
            'text-green-900': toastType === 'success',
            'text-red-900': toastType === 'error',
            'text-blue-900': toastType === 'info'
          }">{{ toastMessage }}</span>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import offlineService from '../services/offlineService.js';

const router = useRouter();

// Estado reactivo
const isClearing = ref(false);
const showConfirmDialog = ref(false);
const showDatabaseInfo = ref(false);
const showToast = ref(false);
const toastMessage = ref('');
const toastType = ref('info'); // 'success', 'error', 'info'

const cacheSize = ref('0 MB');
const itemCount = ref(0);
const pendingRecords = ref(0);
const syncedRecords = ref(0);
const buildDate = computed(() => {
  return new Date().toLocaleDateString('es-MX', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
});

const browserInfo = computed(() => {
  return navigator.userAgent.split(' ').slice(-1)[0] || 'Desconocido';
});

const cachePercentage = computed(() => {
  // Extraer número del tamaño del caché
  const sizeStr = cacheSize.value.split(' ')[0];
  const sizeNum = parseFloat(sizeStr) || 0;
  // Asumir máximo de 50MB para la barra
  return Math.min((sizeNum / 50) * 100, 100);
});

// Funciones
async function calculateCacheSize() {
  try {
    // Obtener información de caché de IndexedDB
    let totalSize = 0;
    let totalItems = 0;

    // Obtener información de registros offline
    const pendientes = await offlineService.obtenerResumenPendientes();
    if (pendientes && pendientes.registros) {
      const registrosItems = pendientes.registros.items || [];
      totalItems += registrosItems.length;
      // Estimación de tamaño (cada registro ~1MB aprox con foto)
      totalSize += registrosItems.length * 1;
    }

    // Obtener información de localStorage
    let localStorageSize = 0;
    for (let key in localStorage) {
      if (localStorage.hasOwnProperty(key)) {
        const value = localStorage[key];
        localStorageSize += (value ? value.length : 0) + (key ? key.length : 0);
      }
    }
    totalSize += localStorageSize / (1024 * 1024); // Convertir a MB

    // Obtener contador de registros pendientes y sincronizados
    if (pendientes) {
      pendingRecords.value = pendientes.registros ? (pendientes.registros.items ? pendientes.registros.items.length : 0) : 0;
      syncedRecords.value = 0; // Se podría mejorar con una consulta al backend
    }

    itemCount.value = totalItems;
    cacheSize.value = totalSize.toFixed(2) + ' MB';
  } catch (error) {
    console.error('Error al calcular tamaño del caché:', error);
    cacheSize.value = '0 MB';
    itemCount.value = 0;
  }
}

async function clearCache() {
  isClearing.value = true;
  showConfirmDialog.value = false;

  try {
    // Limpiar IndexedDB
    await offlineService.limpiarTodo();

    // Limpiar localStorage (excepto datos críticos de usuario)
    const userDataKey = 'user';
    const userData = localStorage.getItem(userDataKey);
    localStorage.clear();
    if (userData) {
      localStorage.setItem(userDataKey, userData);
    }

    // Mostrar toast de éxito
    toastMessage.value = '✓ Caché eliminado correctamente. Se liberaron ' + cacheSize.value;
    toastType.value = 'success';
    showToast.value = true;

    // Recalcular el tamaño
    await new Promise(resolve => setTimeout(resolve, 1000));
    await calculateCacheSize();

    // Ocultar toast después de 3 segundos
    setTimeout(() => {
      showToast.value = false;
    }, 3000);
  } catch (error) {
    console.error('Error al limpiar caché:', error);
    toastMessage.value = '✗ Error al limpiar el caché: ' + error.message;
    toastType.value = 'error';
    showToast.value = true;

    setTimeout(() => {
      showToast.value = false;
    }, 4000);
  } finally {
    isClearing.value = false;
  }
}

// Al montar el componente
onMounted(() => {
  calculateCacheSize();
  
  // Recalcular cada 5 segundos
  const interval = setInterval(calculateCacheSize, 5000);
  
  // Limpiar al desmontar
  return () => {
    clearInterval(interval);
  };
});
</script>

<style scoped>
/* Animaciones */
@keyframes pulse-slow {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.05);
  }
}

.animate-pulse-slow {
  animation: pulse-slow 4s ease-in-out infinite;
}

@keyframes expand {
  from {
    opacity: 0;
    max-height: 0;
  }
  to {
    opacity: 1;
    max-height: 500px;
  }
}

.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
}

@keyframes slide-up {
  from {
    transform: translateY(100px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100px);
  opacity: 0;
}

/* Glass Morphism */
.glass-card {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow:
    0 8px 32px 0 rgba(31, 38, 135, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  padding: 1rem;
  position: relative;
  overflow: hidden;
}

.glass-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -50%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  transform: skewX(-25deg);
  transition: all 0.6s;
}

.glass-card:hover::before {
  left: 150%;
}

/* Línea verde */
.green-line {
  width: 60px;
  height: 1px;
  background: linear-gradient(90deg, #15803d, #16a34a, #15803d);
  border-radius: 0.5px;
  animation: line-glow 2s ease-in-out infinite alternate;
}

@keyframes line-glow {
  0% {
    box-shadow: 0 0 5px rgba(34, 197, 94, 0.3);
    opacity: 0.8;
  }
  100% {
    box-shadow: 0 0 15px rgba(34, 197, 94, 0.6);
    opacity: 1;
  }
}

/* Títulos modernos */
.modern-title {
  background: linear-gradient(
    90deg,
    #166534 0%,
    #15803d 25%,
    #86efac 50%,
    #15803d 75%,
    #166534 100%
  );
  background-size: 300% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: gradient-wave 3s ease-in-out infinite;
  font-weight: 500;
}

@keyframes gradient-wave {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

/* Responsividad para móviles */
@media (max-width: 480px) {
  .page-container {
    padding-left: 0;
    padding-right: 0;
  }

  .glass-card {
    padding: 0.75rem;
    margin: 0 0.375rem;
    border-radius: 16px;
  }
}

@media (max-width: 375px) {
  .glass-card {
    padding: 0.625rem;
    border-radius: 12px;
    margin: 0;
  }
}

@supports not (backdrop-filter: blur(20px)) {
  .glass-card {
    background: rgba(255, 255, 255, 0.85);
  }
}
</style>
