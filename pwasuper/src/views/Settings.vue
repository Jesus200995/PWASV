<template>
  <div class="fixed inset-0 overflow-hidden" style="z-index: 0; background: linear-gradient(135deg, rgba(255, 255, 255, 1) 0%, rgba(240, 253, 244, 0.6) 50%, rgba(220, 252, 231, 0.4) 100%);">
    <!-- Burbujas verdes decorativas -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 right-1/4 w-72 h-72 bg-green-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse-slow"></div>
      <div class="absolute bottom-1/3 left-1/4 w-80 h-80 bg-emerald-300 rounded-full mix-blend-multiply filter blur-3xl opacity-25 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute top-2/3 right-1/3 w-64 h-64 bg-green-200 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse-slow" style="animation-delay: 4s;"></div>
      <div class="absolute top-1/2 left-1/2 w-56 h-56 bg-teal-300 rounded-full mix-blend-multiply filter blur-3xl opacity-15 animate-pulse-slow" style="animation-delay: 1s;"></div>
      <div class="absolute top-10 left-10 w-48 h-48 bg-emerald-200 rounded-full mix-blend-multiply filter blur-2xl opacity-20 animate-pulse-slow" style="animation-delay: 3s;"></div>
      <div class="absolute bottom-20 right-20 w-52 h-52 bg-green-300 rounded-full mix-blend-multiply filter blur-3xl opacity-18 animate-pulse-slow" style="animation-delay: 2.5s;"></div>
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
            <!-- Botón de actualizar -->
            <button
              @click="refreshCache"
              :disabled="isRefreshing"
              class="flex-shrink-0 p-1.5 rounded-lg hover:bg-white/30 transition-colors disabled:opacity-50"
              title="Actualizar caché"
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                class="h-5 w-5 text-gray-700 transition-transform duration-500"
                :class="{ 'animate-spin': isRefreshing }"
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </button>
          </div>
          <div class="green-line mb-4"></div>

          <!-- Información de caché -->
          <div class="bg-white/40 backdrop-filter backdrop-blur-sm rounded-xl p-3 mb-4 border border-white/20">
            <div class="space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-700 font-medium">📊 Caché Usado</span>
                <span class="text-sm font-bold text-orange-600">{{ cacheSize }}</span>
              </div>
              <div class="w-full bg-gray-300 rounded-full h-2.5 overflow-hidden">
                <div
                  class="h-full bg-gradient-to-r from-orange-500 via-orange-600 to-red-600 transition-all duration-500 rounded-full"
                  :style="{ width: cachePercentage + '%' }"
                ></div>
              </div>
              <p class="text-xs text-gray-600">
                {{ itemCount }} elemento(s) | Actualización: tiempo real
              </p>
            </div>
          </div>

          <!-- Descripción detallada de qué se limpiarà -->
          <div class="bg-orange-50 border-l-4 border-orange-500 rounded-r-lg p-3 mb-4 text-sm">
            <div class="flex items-start gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-orange-600 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <p class="font-medium text-orange-900 text-xs mb-1.5">Se limpiará completamente:</p>
                <ul class="text-xs text-orange-800 space-y-0.75">
                  <li>✓ IndexedDB (registros y asistencias offline)</li>
                  <li>✓ localStorage (datos temporales)</li>
                  <li>✓ sessionStorage (sesión)</li>
                  <li>✓ Cache API (archivos en caché)</li>
                  <li>• Datos de usuario y credenciales se preservarán</li>
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
    <div v-if="showConfirmDialog" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 p-3">
      <div class="bg-white rounded-2xl shadow-2xl max-w-sm w-full transform transition-all p-6 border border-gray-100">
        <!-- Header del modal -->
        <div class="flex items-start justify-between mb-4">
          <div class="flex items-start gap-3">
            <div class="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-to-br from-orange-100 to-red-100 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-orange-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900">Limpiar Caché</h3>
              <p class="text-xs text-gray-500 mt-0.5">Esta acción no se puede deshacer</p>
            </div>
          </div>
          <button
            @click="showConfirmDialog = false"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Contenido del modal -->
        <div class="bg-gray-50 rounded-xl p-4 mb-5 border border-gray-200">
          <p class="text-sm text-gray-700 leading-relaxed mb-4">
            Se eliminarán <strong class="text-orange-600">{{ itemCount }} elemento(s)</strong> ocupando <strong class="text-orange-600">{{ cacheSize }}</strong> de espacio:
          </p>
          
          <ul class="space-y-2 text-xs text-gray-700">
            <li class="flex items-start gap-2">
              <span class="text-orange-500 font-bold mt-0.5">•</span>
              <span>IndexedDB (registros offline)</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-orange-500 font-bold mt-0.5">•</span>
              <span>localStorage (datos temporales)</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-orange-500 font-bold mt-0.5">•</span>
              <span>Cache API (archivos cacheados)</span>
            </li>
            <li class="flex items-start gap-2">
              <span class="text-green-500 font-bold mt-0.5">✓</span>
              <span class="text-gray-600">Tu información de usuario será preservada</span>
            </li>
          </ul>
        </div>

        <!-- Botones -->
        <div class="flex gap-2">
          <button
            @click="showConfirmDialog = false"
            class="flex-1 py-2.5 px-3 rounded-lg border-2 border-gray-200 text-gray-700 font-semibold text-sm hover:bg-gray-100 transition-colors duration-200"
          >
            Cancelar
          </button>
          <button
            @click="clearCache"
            :disabled="isClearing"
            class="flex-1 py-2.5 px-3 rounded-lg bg-gradient-to-r from-orange-500 via-orange-600 to-red-600 text-white font-semibold text-sm hover:shadow-lg transition-all duration-200 transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center justify-center gap-2"
          >
            <svg v-if="!isClearing" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ isClearing ? 'Limpiando...' : 'Sí, Limpiar' }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Toast de notificación -->
    <transition name="slide-up">
      <div v-if="showToast" class="fixed bottom-4 left-3 right-3 max-w-sm mx-auto z-50">
        <div v-if="toastType === 'success'" class="bg-white rounded-xl shadow-2xl border-l-4 border-green-500 p-4 flex items-start gap-3 animate-pulse-slow">
          <div class="flex-shrink-0 w-10 h-10 rounded-full bg-green-100 flex items-center justify-center mt-0.5">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="flex-1">
            <p class="font-bold text-green-900">¡Caché limpiado!</p>
            <p class="text-sm text-green-700 mt-0.5">{{ toastMessage }}</p>
          </div>
        </div>
        
        <div v-else-if="toastType === 'error'" class="bg-white rounded-xl shadow-2xl border-l-4 border-red-500 p-4 flex items-start gap-3">
          <div class="flex-shrink-0 w-10 h-10 rounded-full bg-red-100 flex items-center justify-center mt-0.5">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-600" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="flex-1">
            <p class="font-bold text-red-900">Error al limpiar</p>
            <p class="text-sm text-red-700 mt-0.5">{{ toastMessage }}</p>
          </div>
        </div>
        
        <div v-else class="bg-white rounded-xl shadow-2xl border-l-4 border-blue-500 p-4 flex items-start gap-3">
          <div class="flex-shrink-0 w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center mt-0.5">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="flex-1">
            <p class="font-bold text-blue-900">Información</p>
            <p class="text-sm text-blue-700 mt-0.5">{{ toastMessage }}</p>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onActivated } from 'vue';
import { useRouter } from 'vue-router';
import offlineService from '../services/offlineService.js';

const router = useRouter();

// Estado reactivo
const isClearing = ref(false);
const isRefreshing = ref(false);
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
    let totalSize = 0;
    let totalItems = 0;

    // ============ localStorage (más rápido, calcularlo primero) ============
    let localStorageSize = 0;
    let localStorageItems = 0;

    try {
      for (let key in localStorage) {
        if (localStorage.hasOwnProperty(key)) {
          const value = localStorage[key];
          localStorageSize += (value ? value.length : 0) + (key ? key.length : 0);
          localStorageItems++;
        }
      }
    } catch (e) {
      console.warn('⚠️ Error calculando localStorage:', e);
    }

    // ============ sessionStorage ============
    let sessionStorageSize = 0;
    let sessionStorageItems = 0;

    try {
      for (let key in sessionStorage) {
        if (sessionStorage.hasOwnProperty(key)) {
          const value = sessionStorage[key];
          sessionStorageSize += (value ? value.length : 0) + (key ? key.length : 0);
          sessionStorageItems++;
        }
      }
    } catch (e) {
      console.warn('⚠️ Error calculando sessionStorage:', e);
    }

    // ============ IndexedDB (más pesado, calcularlo después) ============
    let indexedDbSize = 0;
    let indexedDbItems = 0;

    try {
      await offlineService.initDB();
      const registros = await offlineService.obtenerRegistrosPendientes();
      const asistencias = await offlineService.obtenerAsistenciasPendientes();

      // Contar items y calcular tamaño
      if (registros && registros.items) {
        indexedDbItems += registros.items.length;
        registros.items.forEach(item => {
          indexedDbSize += JSON.stringify(item).length;
        });
      }

      if (asistencias && asistencias.items) {
        indexedDbItems += asistencias.items.length;
        asistencias.items.forEach(item => {
          indexedDbSize += JSON.stringify(item).length;
        });
      }
    } catch (e) {
      console.warn('⚠️ Error calculando IndexedDB:', e);
    }

    // ============ Cache API (más pesado) ============
    let cacheApiSize = 0;
    let cacheApiItems = 0;

    try {
      if ('caches' in window) {
        const cacheNames = await caches.keys();
        for (const cacheName of cacheNames) {
          const cache = await caches.open(cacheName);
          const responses = await cache.keys();
          cacheApiItems += responses.length;
          
          for (const request of responses) {
            try {
              const response = await cache.match(request);
              if (response && response.blob) {
                const blob = await response.blob();
                cacheApiSize += blob.size;
              }
            } catch (e) {
              // Ignorar errores individuales
            }
          }
        }
      }
    } catch (e) {
      console.warn('⚠️ Error calculando Cache API:', e);
    }

    // ============ Calcular total ============
    totalSize = (indexedDbSize + localStorageSize + sessionStorageSize + cacheApiSize) / (1024 * 1024); // MB
    totalItems = indexedDbItems + localStorageItems + sessionStorageItems + cacheApiItems;

    // Actualizar valores reactivos
    itemCount.value = totalItems;
    cacheSize.value = totalSize < 0.01 ? '0 MB' : totalSize.toFixed(2) + ' MB';

    // Obtener registros pendientes para sincronización
    try {
      const pendientes = await offlineService.obtenerResumenPendientes();
      if (pendientes && pendientes.registros) {
        pendingRecords.value = pendientes.registros.total || pendientes.registros.items?.length || 0;
      }
      syncedRecords.value = 0;
    } catch (e) {
      console.warn('⚠️ Error obteniendo resumen:', e);
    }

    // Solo loguear en cambios significativos
    if (totalSize > 0.1) {
      console.log(`📊 Caché: ${cacheSize.value} (${totalItems} items)`);
    }
  } catch (error) {
    console.error('❌ Error al calcular caché:', error);
  }
}

// Función para refrescar manualmente el caché
async function refreshCache() {
  isRefreshing.value = true;
  try {
    await calculateCacheSize();
    console.log('🔄 Caché refrescado manualmente');
  } catch (error) {
    console.error('❌ Error refrescando caché:', error);
  } finally {
    isRefreshing.value = false;
  }
}

async function clearCache() {
  isClearing.value = true;
  showConfirmDialog.value = false;

  try {
    const sizeBefore = cacheSize.value;
    const itemsBefore = itemCount.value;

    console.log('🗑️ Iniciando limpieza de caché...');

    // ============ Limpiar IndexedDB ============
    try {
      await offlineService.limpiarTodo();
      console.log('✅ IndexedDB limpiado completamente');
    } catch (e) {
      console.error('❌ Error limpiando IndexedDB:', e);
    }

    // ============ Limpiar localStorage (excepto datos críticos) ============
    try {
      const criticalKeys = ['user', 'theme', 'language'];
      const criticalData = {};
      
      // Guardar datos críticos
      criticalKeys.forEach(key => {
        const value = localStorage.getItem(key);
        if (value) criticalData[key] = value;
      });
      
      // Limpiar todo
      localStorage.clear();
      
      // Restaurar datos críticos
      Object.entries(criticalData).forEach(([key, value]) => {
        localStorage.setItem(key, value);
      });
      
      console.log('✅ localStorage limpiado (datos críticos preservados)');
    } catch (e) {
      console.error('❌ Error limpiando localStorage:', e);
    }

    // ============ Limpiar sessionStorage ============
    try {
      sessionStorage.clear();
      console.log('✅ sessionStorage limpiado');
    } catch (e) {
      console.error('❌ Error limpiando sessionStorage:', e);
    }

    // ============ Limpiar Cache API (Service Worker cache) ============
    try {
      if ('caches' in window) {
        const cacheNames = await caches.keys();
        console.log(`🔍 Encontrados ${cacheNames.length} caches:`, cacheNames);
        
        const deletePromises = cacheNames.map(async (cacheName) => {
          try {
            const deleted = await caches.delete(cacheName);
            console.log(`✅ Cache API "${cacheName}" eliminado`);
            return deleted;
          } catch (e) {
            console.error(`❌ Error eliminando cache "${cacheName}":`, e);
          }
        });
        
        await Promise.all(deletePromises);
        console.log('✅ Todos los Caches API limpiados');
      }
    } catch (e) {
      console.error('❌ Error limpiando Cache API:', e);
    }

    // ============ Mostrar resultado ============
    console.log(`✅ Limpieza completada: Se liberaron ${sizeBefore} (${itemsBefore} items)`);
    
    toastMessage.value = `✓ Se liberaron ${sizeBefore} de espacio (${itemsBefore} elementos eliminados)`;
    toastType.value = 'success';
    showToast.value = true;

    // Esperar un bit y recalcular en tiempo real
    await new Promise(resolve => setTimeout(resolve, 300));
    await calculateCacheSize();
    
    // Recalcular cada 150ms durante 2 segundos para feedback inmediato (verá el cambio en tiempo real)
    for (let i = 0; i < 15; i++) {
      await new Promise(resolve => setTimeout(resolve, 150));
      await calculateCacheSize();
    }

    // Ocultar toast después de 4 segundos
    setTimeout(() => {
      showToast.value = false;
    }, 4000);
  } catch (error) {
    console.error('❌ Error durante limpieza de caché:', error);
    toastMessage.value = '✗ Error al limpiar el caché: ' + error.message;
    toastType.value = 'error';
    showToast.value = true;

    setTimeout(() => {
      showToast.value = false;
    }, 5000);
  } finally {
    isClearing.value = false;
  }
}

// Cuando el componente se activa (vuelve a ser visible)
onActivated(() => {
  console.log('🔄 Settings.vue activado - Refrescando caché');
  calculateCacheSize();
});

// Al montar el componente
onMounted(() => {
  // Calcular inmediatamente
  calculateCacheSize();
  
  // Recalcular cada 300ms para actualización en tiempo real constante
  const interval = setInterval(() => {
    calculateCacheSize();
  }, 300);
  
  // Listener para cambios en localStorage (dispara cada vez que se modifica)
  const handleStorageChange = () => {
    calculateCacheSize();
  };
  
  window.addEventListener('storage', handleStorageChange);
  
  // Interceptar accesos a localStorage para detectar cambios locales
  const originalSetItem = localStorage.setItem;
  const originalRemoveItem = localStorage.removeItem;
  const originalClear = localStorage.clear;
  
  localStorage.setItem = function(key, value) {
    originalSetItem.call(this, key, value);
    calculateCacheSize();
  };
  
  localStorage.removeItem = function(key) {
    originalRemoveItem.call(this, key);
    calculateCacheSize();
  };
  
  localStorage.clear = function() {
    originalClear.call(this);
    calculateCacheSize();
  };
  
  // Recalcular cuando la pestaña vuelve a ser visible
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
      calculateCacheSize();
    }
  });
  
  // Limpiar al desmontar
  return () => {
    clearInterval(interval);
    window.removeEventListener('storage', handleStorageChange);
    // Restaurar métodos originales
    localStorage.setItem = originalSetItem;
    localStorage.removeItem = originalRemoveItem;
    localStorage.clear = originalClear;
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
