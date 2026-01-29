<template>
  <div class="fixed inset-0 overflow-hidden" style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(76, 175, 80, 0.08) 50%, rgba(59, 130, 246, 0.05) 100%);">
    <!-- Elementos decorativos -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="background-color: rgba(59, 130, 246, 0.3);"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s; background-color: rgba(76, 175, 80, 0.3);"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s; background-color: rgba(56, 142, 60, 0.3);"></div>
    </div>

    <!-- Modal de Confirmación de Firma -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div 
          v-if="mostrarModalFirma" 
          class="fixed inset-0 z-50 flex items-center justify-center p-4"
        >
          <!-- Overlay - clic aquí cierra el modal SOLO si no está procesando -->
          <div 
            class="absolute inset-0 bg-black/60 backdrop-blur-sm"
            @click="!procesandoDescarga && cerrarModalFirma()"
          ></div>
          
          <!-- Modal -->
          <div class="relative w-full max-w-md bg-white rounded-2xl shadow-2xl overflow-hidden animate-modal-enter">
            <!-- Header del Modal -->
            <div class="bg-gradient-to-r from-purple-600 to-indigo-600 px-4 py-4 sm:px-6">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25z"/>
                      <path d="M20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                    </svg>
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-white">Firma Requerida</h3>
                    <p class="text-xs text-white/80">Autenticación del reporte</p>
                  </div>
                </div>
                <button 
                  @click="cerrarModalFirma"
                  class="w-8 h-8 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center transition-colors"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
            
            <!-- Contenido del Modal -->
            <div class="px-4 py-5 sm:px-6">
              <!-- Información del Reporte -->
              <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-4 mb-4 border border-blue-100">
                <div class="flex items-start gap-3">
                  <div class="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                  </div>
                  <div class="min-w-0 flex-1">
                    <p class="text-sm font-semibold text-gray-900">Reporte de Actividades</p>
                    <p class="text-xs text-gray-600 mt-0.5">{{ mesActual }} {{ anioSeleccionado }}</p>
                    <div class="flex items-center gap-2 mt-2">
                      <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        {{ actividades.length }} actividades
                      </span>
                      <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium" :class="formatoSeleccionado === 'pdf' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'">
                        {{ formatoSeleccionado.toUpperCase() }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Aviso importante -->
              <div class="bg-amber-50 border border-amber-200 rounded-xl p-4 mb-4">
                <div class="flex gap-3">
                  <div class="flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                    </svg>
                  </div>
                  <div>
                    <h4 class="text-sm font-semibold text-amber-800">Importante</h4>
                    <p class="text-xs text-amber-700 mt-1">
                      Al firmar este reporte, usted certifica que la información contenida es verídica y corresponde a sus actividades realizadas.
                    </p>
                  </div>
                </div>
              </div>
              
              <!-- Datos del firmante -->
              <div class="bg-gray-50 rounded-xl p-4 mb-4">
                <p class="text-xs text-gray-500 font-medium mb-2">FIRMANTE</p>
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-full flex items-center justify-center">
                    <span class="text-white font-bold text-sm">{{ iniciales }}</span>
                  </div>
                  <div class="min-w-0 flex-1">
                    <p class="text-sm font-semibold text-gray-900 truncate">{{ usuarioInfo.nombre }}</p>
                    <p class="text-xs text-gray-500 truncate">{{ usuarioInfo.correo }}</p>
                  </div>
                </div>
              </div>
              
              <!-- Checkbox de confirmación -->
              <label class="flex items-start gap-3 p-3 bg-gray-50 rounded-xl cursor-pointer hover:bg-gray-100 transition-colors">
                <input 
                  type="checkbox" 
                  v-model="confirmarFirma"
                  class="w-4 h-4 mt-0.5 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
                >
                <span class="text-xs text-gray-700">
                  Confirmo que he revisado el contenido del reporte y autorizo su descarga con mi firma digital.
                </span>
              </label>
            </div>
            
            <!-- Footer del Modal -->
            <div class="bg-gray-50 px-4 py-4 sm:px-6 flex flex-col sm:flex-row gap-2 sm:gap-3">
              <button
                @click="cerrarModalFirma"
                :disabled="procesandoDescarga"
                class="flex-1 px-4 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-xl hover:bg-gray-50 transition-colors order-2 sm:order-1"
                :class="{ 'opacity-50 cursor-not-allowed': procesandoDescarga }"
              >
                Cancelar
              </button>
              <button
                @click.stop.prevent="confirmarYDescargar"
                :disabled="!confirmarFirma || procesandoDescarga"
                class="flex-1 px-4 py-2.5 text-sm font-medium text-white rounded-xl transition-all order-1 sm:order-2 flex items-center justify-center gap-2"
                :class="confirmarFirma && !procesandoDescarga
                  ? 'bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 shadow-lg' 
                  : 'bg-gray-300 cursor-not-allowed'"
              >
                <svg v-if="!procesandoDescarga" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                </svg>
                <svg v-else class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ procesandoDescarga ? 'Generando...' : 'Firmar y Descargar' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <div class="absolute inset-0 overflow-y-auto pt-16 sm:pt-20 pb-4">
      <div class="page-container relative z-10 px-2 sm:px-3 md:px-4 lg:px-6 xl:px-8 py-3 sm:py-4 lg:py-5 min-h-full max-w-full">
        <div class="w-full max-w-lg mx-auto space-y-4">
          <!-- Header de Reportes -->
          <div class="glass-card text-center">
            <div class="flex items-center justify-center mb-3">
              <div class="w-12 h-12 rounded-full flex items-center justify-center shadow-xl" style="background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M7 3H4a1 1 0 00-1 1v16a1 1 0 001 1h16a1 1 0 001-1V8.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0015 2H9a1 1 0 00-1 1v2H7a1 1 0 00-1 1v2zm2-2v2h6V2H9z"/>
                </svg>
              </div>
            </div>
            
            <h1 class="text-xl font-bold text-gray-800 mb-2 modern-title">Mis Reportes</h1>
            <div class="red-line mx-auto mb-2"></div>
            <p class="text-gray-600 text-xs mb-3">Genera reportes mensuales de tus actividades</p>
            
            <!-- Estadísticas rápidas -->
            <div class="grid grid-cols-3 gap-2 mt-3">
              <div class="p-2 bg-blue-50 rounded-lg">
                <p class="text-xs text-gray-600 font-medium">Actividades</p>
                <p class="text-lg font-bold text-blue-600">{{ estadisticas.totalActividades }}</p>
              </div>
              <div class="p-2 bg-green-50 rounded-lg">
                <p class="text-xs text-gray-600 font-medium">Período</p>
                <p class="text-xs font-bold text-green-600 truncate">{{ mesActual }}</p>
              </div>
              <div class="p-2 bg-purple-50 rounded-lg">
                <p class="text-xs text-gray-600 font-medium">Estado</p>
                <p class="text-xs font-bold text-purple-600">{{ estadoReporte }}</p>
              </div>
            </div>
          </div>

          <!-- Selector de Período -->
          <div class="glass-card">
            <div class="flex items-center mb-3">
              <div class="w-8 h-8 rounded-full flex items-center justify-center mr-3" style="background-color: #3B82F6;">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
              </div>
              <div>
                <h2 class="text-base font-semibold text-gray-800">Período</h2>
                <p class="text-xs text-gray-500">Selecciona mes y año</p>
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1.5">Mes</label>
                <select
                  v-model.number="mesSeleccionado"
                  @change="cambiarPeriodo"
                  class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option v-for="(mes, index) in meses" :key="index" :value="index">
                    {{ mes }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1.5">Año</label>
                <select
                  v-model.number="anioSeleccionado"
                  @change="cambiarPeriodo"
                  class="w-full px-3 py-2 text-xs border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option v-for="year in anos" :key="year" :value="year">
                    {{ year }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <!-- Sección de Actividades -->
          <div class="glass-card">
            <div class="flex items-center mb-3">
              <div class="w-8 h-8 rounded-full flex items-center justify-center mr-3" style="background-color: #6366F1;">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
                </svg>
              </div>
              <div>
                <h2 class="text-base font-semibold text-gray-800">Actividades</h2>
                <p class="text-xs text-gray-500">Listado del período seleccionado</p>
              </div>
            </div>

            <!-- Mensaje de error/offline -->
            <div v-if="error" class="mb-3 bg-red-100 border-l-4 border-red-500 text-red-700 p-3 rounded" role="alert">
              <p class="text-xs">{{ error }}</p>
              <button 
                @click="cargarActividades" 
                class="mt-2 text-xs px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
              >
                Reintentar
              </button>
            </div>

            <!-- Loading -->
            <div v-else-if="cargando" class="flex justify-center items-center py-8">
              <div class="text-center">
                <div class="inline-block">
                  <svg class="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </div>
                <p class="mt-3 text-xs text-gray-600">Cargando actividades...</p>
              </div>
            </div>

            <!-- Tabla de Actividades -->
            <div v-else class="">
              <table v-if="actividades.length > 0" class="w-full text-xs">
                <thead>
                  <tr class="bg-gradient-to-r from-blue-500 to-indigo-600 text-white">
                    <th class="px-2 py-2 text-left font-semibold">Fecha</th>
                    <th class="px-2 py-2 text-left font-semibold">Hora</th>
                    <th class="hidden sm:table-cell px-2 py-2 text-left font-semibold">Tipo</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(actividad, index) in actividades"
                    :key="actividad.id || index"
                    class="border-b border-gray-200 hover:bg-blue-50 transition-colors"
                  >
                    <td class="px-2 py-2 text-gray-900 font-medium">
                      {{ formatearFecha(actividad.fecha_hora) }}
                    </td>
                    <td class="px-2 py-2 text-gray-700">
                      {{ formatearHora(actividad.fecha_hora) }}
                    </td>
                    <td class="hidden sm:table-cell px-2 py-2">
                      <span
                        :class="[
                          'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium',
                          actividad.tipo_actividad === 'campo' 
                            ? 'bg-green-100 text-green-800'
                            : actividad.tipo_actividad === 'gabinete'
                            ? 'bg-purple-100 text-purple-800'
                            : 'bg-blue-100 text-blue-800'
                        ]"
                      >
                        {{ capitalizar(actividad.tipo_actividad || 'campo') }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
              <div v-else class="text-center py-6">
                <div class="w-12 h-12 mx-auto mb-3 bg-gray-200 rounded-full flex items-center justify-center">
                  <i class="fas fa-inbox text-gray-400 text-lg"></i>
                </div>
                <p class="text-gray-500 text-xs">Sin actividades en este período</p>
              </div>
            </div>
          </div>

          <!-- Firma Digital -->
          <div class="glass-card">
            <div class="flex items-center mb-3">
              <div class="w-8 h-8 rounded-full flex items-center justify-center mr-3" style="background-color: #A855F7;">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25z"/>
                  <path d="M20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                </svg>
              </div>
              <div>
                <h2 class="text-base font-semibold text-gray-800">Firma</h2>
                <p class="text-xs text-gray-500">Autentica tu reporte</p>
              </div>
            </div>
            <FirmaDigital
              ref="firmaComponent"
              label="Firmar aquí"
            />
          </div>

          <!-- Opciones de Descarga -->
          <div class="glass-card">
            <div class="flex items-center mb-3">
              <div class="w-8 h-8 rounded-full flex items-center justify-center mr-3" style="background-color: #10B981;">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                </svg>
              </div>
              <div>
                <h2 class="text-base font-semibold text-gray-800">Descargar</h2>
                <p class="text-xs text-gray-500">Genera tu reporte</p>
              </div>
            </div>

            <!-- Información de Usuario -->
            <div class="rounded-lg p-3 border mb-3" style="background: linear-gradient(to right, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.15)); border-color: rgba(59, 130, 246, 0.3);">
              <div class="mb-2">
                <p class="text-xs text-gray-600 font-medium">Nombre</p>
                <p class="text-sm font-semibold text-gray-900 truncate">{{ usuarioInfo.nombre }}</p>
              </div>
              <div class="mb-2">
                <p class="text-xs text-gray-600 font-medium">Cargo</p>
                <p class="text-sm font-semibold text-gray-900 truncate">{{ usuarioInfo.cargo || 'N/A' }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-600 font-medium">Correo</p>
                <p class="text-xs font-semibold text-gray-900 truncate">{{ usuarioInfo.correo }}</p>
              </div>
            </div>

            <!-- Opciones de Formato -->
            <div class="space-y-2 mb-3">
              <label class="flex items-center p-2.5 border border-gray-300 rounded-lg cursor-pointer hover:bg-blue-50 transition-colors">
                <input
                  type="radio"
                  v-model="formatoSeleccionado"
                  value="pdf"
                  class="w-4 h-4 text-blue-600"
                />
                <span class="ml-2">
                  <span class="text-xs font-medium text-gray-900 block">PDF</span>
                  <p class="text-xs text-gray-500">Con tabla y firma</p>
                </span>
              </label>
              <label class="flex items-center p-2.5 border border-gray-300 rounded-lg cursor-pointer hover:bg-blue-50 transition-colors">
                <input
                  type="radio"
                  v-model="formatoSeleccionado"
                  value="csv"
                  class="w-4 h-4 text-blue-600"
                />
                <span class="ml-2">
                  <span class="text-xs font-medium text-gray-900 block">CSV</span>
                  <p class="text-xs text-gray-500">Para Excel</p>
                </span>
              </label>
            </div>

            <!-- Aviso de reporte existente -->
            <div v-if="reporteExistente" class="bg-amber-50 border border-amber-200 rounded-lg p-3 mb-3">
              <div class="flex items-start gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-amber-500 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>
                <div class="flex-1 min-w-0">
                  <p class="text-xs font-semibold text-amber-800">Ya existe un reporte para {{ mesActual }} {{ anioSeleccionado }}</p>
                  <p class="text-xs text-amber-700 mt-0.5">Para generar uno nuevo, primero elimina el existente desde el historial de abajo.</p>
                </div>
              </div>
            </div>

            <!-- Botón de Descarga -->
            <button
              @click="iniciarDescarga"
              :disabled="cargando || generandoReporte || actividades.length === 0 || reporteExistente || verificandoReporte"
              class="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed text-white font-bold py-2 px-3 rounded-lg transition-all duration-200 flex items-center justify-center gap-2 text-xs sm:text-sm"
            >
              <svg v-if="verificandoReporte" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else-if="!generandoReporte" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
              </svg>
              <svg v-else class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span class="truncate">{{ verificandoReporte ? 'Verificando...' : (generandoReporte ? 'Generando...' : (reporteExistente ? 'Reporte ya generado' : 'Descargar Reporte')) }}</span>
            </button>
          </div>

          <!-- Historial de Reportes -->
          <div class="glass-card">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center">
                <div class="w-8 h-8 rounded-full flex items-center justify-center mr-3" style="background-color: #F59E0B;">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <div>
                  <h2 class="text-base font-semibold text-gray-800">Historial</h2>
                  <p class="text-xs text-gray-500">Reportes generados</p>
                </div>
              </div>
              <!-- Botón de recargar historial -->
              <button 
                @click="cargarHistorialReportes" 
                :disabled="cargandoHistorial"
                class="p-1.5 rounded-lg bg-gray-100 text-gray-600 hover:bg-gray-200 transition-colors disabled:opacity-50"
                title="Recargar historial"
              >
                <svg :class="['h-4 w-4', cargandoHistorial ? 'animate-spin' : '']" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
              </button>
            </div>
            
            <!-- Estado de carga -->
            <div v-if="cargandoHistorial" class="text-center py-4">
              <svg class="animate-spin h-6 w-6 mx-auto text-orange-500 mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <p class="text-xs text-gray-500">Cargando historial...</p>
            </div>
            
            <!-- Error de carga -->
            <div v-else-if="errorHistorial" class="bg-red-50 border border-red-200 rounded-lg p-3 text-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mx-auto text-red-500 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
              <p class="text-xs text-red-600">{{ errorHistorial }}</p>
              <button @click="cargarHistorialReportes" class="mt-2 text-xs text-red-700 underline">Reintentar</button>
            </div>
            
            <!-- Lista de reportes -->
            <div v-else-if="reportesGenerados.length > 0" class="space-y-3">
              <div
                v-for="reporte in reportesGenerados"
                :key="reporte.id"
                class="p-3 border rounded-xl transition-colors text-xs"
                :class="reporte.firmado_supervisor ? 'border-green-400 bg-gradient-to-r from-green-50 to-emerald-50' : 'border-amber-300 bg-gradient-to-r from-amber-50 to-yellow-50'"
              >
                <!-- Fila superior: Nombre y estatus -->
                <div class="flex items-start justify-between gap-2 mb-2">
                  <div class="flex items-center gap-2 min-w-0 flex-1">
                    <div class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center" 
                         :class="reporte.tipo === 'PDF' ? 'bg-red-100' : 'bg-green-100'">
                      <svg v-if="reporte.tipo === 'PDF'" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                      </svg>
                      <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                      </svg>
                    </div>
                    <div class="min-w-0 flex-1">
                      <p class="font-semibold text-gray-900 text-sm truncate">{{ reporte.nombre }}</p>
                      <p class="text-xs text-gray-500">Generado: {{ formatearFechaCompleta(reporte.fecha) }}</p>
                    </div>
                  </div>
                  <!-- Badge de tipo -->
                  <span :class="[
                    'inline-flex items-center px-2 py-1 rounded-lg text-xs font-bold',
                    reporte.tipo === 'PDF' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'
                  ]">
                    {{ reporte.tipo }}
                  </span>
                </div>

                <!-- Estatus de firma - SIEMPRE VISIBLE -->
                <div class="mb-2 p-2 rounded-lg" 
                     :class="reporte.firmado_supervisor ? 'bg-green-100/70' : 'bg-amber-100/70'">
                  <div class="flex items-center gap-2">
                    <!-- Icono de estatus -->
                    <div class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center"
                         :class="reporte.firmado_supervisor ? 'bg-green-500' : 'bg-amber-500'">
                      <svg v-if="reporte.firmado_supervisor" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
                      </svg>
                      <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                    </div>
                    <!-- Texto de estatus -->
                    <div class="flex-1">
                      <p v-if="reporte.firmado_supervisor" class="text-xs font-semibold text-green-800">
                        ✓ Firmado por supervisor
                      </p>
                      <p v-else class="text-xs font-semibold text-amber-800">
                        ⏳ Pendiente de firma
                      </p>
                      <p v-if="reporte.firmado_supervisor" class="text-xs text-green-700">
                        {{ reporte.nombre_supervisor }} • {{ formatearFechaFirma(reporte.fecha_firma_supervisor) }}
                      </p>
                      <p v-else class="text-xs text-amber-700">
                        Esperando revisión del supervisor
                      </p>
                    </div>
                  </div>
                </div>

                <!-- Botones de acción -->
                <div class="flex items-center justify-end gap-2">
                  <!-- Botón de ver (SIEMPRE VISIBLE) -->
                  <button
                    @click="verReporteHistorial(reporte)"
                    :disabled="viendoReporte === reporte.id"
                    class="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-purple-100 text-purple-700 hover:bg-purple-200 transition-colors disabled:opacity-50 text-xs font-medium"
                    :title="'Ver ' + reporte.nombre"
                  >
                    <svg v-if="viendoReporte !== reporte.id" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                    </svg>
                    <svg v-else class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Ver
                  </button>
                  <!-- Botón de descarga (SIEMPRE VISIBLE) -->
                  <button
                    @click="descargarReporteHistorial(reporte)"
                    :disabled="descargandoReporte === reporte.id"
                    class="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-blue-100 text-blue-700 hover:bg-blue-200 transition-colors disabled:opacity-50 text-xs font-medium"
                    :title="'Descargar ' + reporte.nombre"
                  >
                    <svg v-if="descargandoReporte !== reporte.id" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                    </svg>
                    <svg v-else class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Descargar
                  </button>
                  <!-- Botón de eliminar - solo si NO está firmado -->
                  <button
                    v-if="!reporte.firmado_supervisor"
                    @click="eliminarReporteHistorial(reporte)"
                    :disabled="eliminandoReporte === reporte.id"
                    class="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-red-100 text-red-700 hover:bg-red-200 transition-colors disabled:opacity-50 text-xs font-medium"
                    :title="'Eliminar ' + reporte.nombre"
                  >
                    <svg v-if="eliminandoReporte !== reporte.id" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                    <svg v-else class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Eliminar
                  </button>
                  <!-- Indicador de protegido si está firmado -->
                  <span
                    v-else
                    class="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-gray-100 text-gray-500 text-xs cursor-not-allowed"
                    title="No se puede eliminar: Reporte firmado por supervisor"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                    </svg>
                    Protegido
                  </span>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-4">
              <p class="text-xs text-gray-500">Sin reportes generados</p>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- Modal de confirmación para eliminar reporte -->
    <div
      v-if="mostrarModalEliminar"
      class="fixed inset-0 z-50 flex items-center justify-center p-4"
      style="background-color: rgba(0, 0, 0, 0.5);"
      @click.self="cancelarEliminar"
    >
      <div class="bg-white rounded-xl shadow-xl max-w-xs w-full p-4 transform transition-all" style="animation: modalIn 0.15s ease-out;">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center flex-shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
          </div>
          <div>
            <h3 class="text-sm font-semibold text-gray-900">¿Eliminar reporte?</h3>
            <p class="text-xs text-gray-500 mt-0.5">{{ reporteAEliminar?.nombre }}</p>
          </div>
        </div>
        <div class="flex gap-2">
          <button
            @click="cancelarEliminar"
            class="flex-1 px-3 py-2 text-xs font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Cancelar
          </button>
          <button
            @click="confirmarEliminarReporte"
            class="flex-1 px-3 py-2 text-xs font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors"
          >
            Eliminar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';
import { PDFDocument } from 'pdf-lib';
import FirmaDigital from '../components/FirmaDigital.vue';
import { apiService, api } from '../services/apiService.js';
import { checkInternetConnection, getOfflineMessage } from '../utils/network.js';
import superiorImage from '../../images/superior.png';

/**
 * Función para limpiar strings base64 que pueden tener prefijos o caracteres inválidos
 */
function limpiarBase64(base64String) {
  if (!base64String) return null;
  
  let base64 = base64String;
  
  // Remover prefijo data URI si existe (ej: data:application/pdf;base64,)
  if (base64.includes(',')) {
    base64 = base64.split(',')[1];
  }
  
  // Remover prefijo específico que puede aparecer
  if (base64.startsWith('data:application/pdf;base64,')) {
    base64 = base64.replace('data:application/pdf;base64,', '');
  }
  
  // Remover espacios en blanco y saltos de línea
  base64 = base64.replace(/\s/g, '');
  
  // Asegurar que solo contiene caracteres válidos de base64
  base64 = base64.replace(/[^A-Za-z0-9+/=]/g, '');
  
  // Agregar padding si es necesario
  while (base64.length % 4 !== 0) {
    base64 += '=';
  }
  
  return base64;
}

export default {
  name: 'Reportes',
  components: {
    FirmaDigital
  },
  data() {
    return {
      actividades: [],
      todasLasActividades: [],
      cargando: false,
      generandoReporte: false,
      mesSeleccionado: new Date().getMonth(),
      anioSeleccionado: new Date().getFullYear(),
      anos: [],
      formatoSeleccionado: 'pdf',
      usuarioInfo: {
        nombre: '',
        cargo: '',
        correo: '',
        territorio: '',
        curp: '',
        supervisor: ''
      },
      reportesGenerados: [],
      meses: [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
      ],
      // Modal de confirmación de firma
      mostrarModalFirma: false,
      confirmarFirma: false,
      procesandoDescarga: false,
      // Estado de descarga de reportes del historial
      descargandoReporte: null,
      // Estado de visualización de reportes del historial
      viendoReporte: null,
      // Estado de eliminación de reportes del historial
      eliminandoReporte: null,
      // Modal de confirmación para eliminar
      mostrarModalEliminar: false,
      reporteAEliminar: null,
      // Estado de conexión
      isOnline: true,
      error: null,
      // Reporte ya existente para el mes/año seleccionado
      reporteExistente: null,
      verificandoReporte: false,
      // Estado de carga del historial
      cargandoHistorial: false,
      errorHistorial: null,
      // Referencias temporales para PDF generado (para descarga después de guardar en BD)
      _pdfDocumentoGenerado: null,
      _pdfNombreArchivo: null
    };
  },
  computed: {
    mesActual() {
      return this.meses[this.mesSeleccionado];
    },
    dateRange() {
      const inicio = new Date(this.anioSeleccionado, this.mesSeleccionado, 1);
      const fin = new Date(this.anioSeleccionado, this.mesSeleccionado + 1, 0);
      return `${inicio.toLocaleDateString()} - ${fin.toLocaleDateString()}`;
    },
    estadisticas() {
      return {
        totalActividades: this.actividades.length
      };
    },
    estadoReporte() {
      if (this.actividades.length === 0) return 'Sin datos';
      if (this.$refs.firmaComponent?.hayFirma) return 'Firmado';
      return 'Sin firmar';
    },
    // Obtener iniciales del usuario
    iniciales() {
      if (!this.usuarioInfo.nombre) return 'U';
      const partes = this.usuarioInfo.nombre.split(' ');
      if (partes.length >= 2) {
        return (partes[0][0] + partes[1][0]).toUpperCase();
      }
      return partes[0].substring(0, 2).toUpperCase();
    }
  },
  methods: {
    async cargarActividades() {
      this.cargando = true;
      this.error = null;
      
      try {
        const usuario = JSON.parse(localStorage.getItem('user'));
        
        if (!usuario || !usuario.id) {
          console.error('❌ No hay usuario en localStorage');
          throw new Error('Usuario no autenticado');
        }
        
        console.log(`📋 Cargando TODAS las actividades para usuario ${usuario.id}`);
        
        // Usar apiService que auto-detecta servidor (producción si localhost no disponible)
        const response = await apiService.getRecords(usuario.id);

        console.log('✅ Respuesta del servidor:', response);

        if (!response || !response.registros) {
          throw new Error('No se recibió respuesta del servidor');
        }

        // Obtener la URL actual del API para las fotos
        const currentApiUrl = apiService.getCurrentApiUrl();
        
        // Procesar las URLs de las fotos para que sean rutas absolutas
        this.todasLasActividades = response.registros.map(r => ({
          ...r,
          foto_url: r.foto_url ? `${currentApiUrl}/${r.foto_url}` : null
        }));
        
        // Filtrar por mes/año seleccionado
        this.filtrarActividadesPorPeriodo();
        
        console.log(`✅ Total de actividades: ${this.todasLasActividades.length}`);
        console.log(`✅ Actividades en período seleccionado: ${this.actividades.length}`);
        
      } catch (err) {
        console.error('❌ Error cargando actividades:', err);
        this.actividades = [];
        this.todasLasActividades = [];
        
        if (err.response) {
          // Error de respuesta del servidor
          if (err.response.status === 500) {
            this.error = 'El servidor está experimentando problemas técnicos. Por favor, inténtalo más tarde.';
          } else {
            this.error = 'Error del servidor: ' + (err.response.data.detail || err.response.statusText);
          }
        } else if (err.request) {
          // Error de conexión
          this.error = 'No se pudo conectar con el servidor. Verifica tu conexión a internet.';
        } else {
          // Error general
          this.error = 'Error al cargar las actividades: ' + err.message;
        }
      } finally {
        this.cargando = false;
      }
    },

    filtrarActividadesPorPeriodo() {
      // Filtrar actividades por mes y año seleccionado
      const inicioDeMes = new Date(this.anioSeleccionado, this.mesSeleccionado, 1);
      const finDelMes = new Date(this.anioSeleccionado, this.mesSeleccionado + 1, 0, 23, 59, 59);
      
      this.actividades = this.todasLasActividades.filter(actividad => {
        if (!actividad.fecha_hora) return false;
        
        const fechaActividad = new Date(actividad.fecha_hora);
        return fechaActividad >= inicioDeMes && fechaActividad <= finDelMes;
      });
      
      // Ordenar de más antigua a más reciente (inicio del mes primero)
      this.actividades.sort((a, b) => {
        const fechaA = new Date(a.fecha_hora);
        const fechaB = new Date(b.fecha_hora);
        return fechaA - fechaB; // Orden ascendente (más antigua primero)
      });
      
      console.log(`🔍 Filtrado y ordenado: ${this.actividades.length} actividades (inicio del mes primero)`);
    },

    async cambiarPeriodo() {
      // Limpiar estado de reporte existente
      this.reporteExistente = null;
      
      // Solo filtrar si ya tenemos actividades cargadas
      if (this.todasLasActividades && this.todasLasActividades.length > 0) {
        this.filtrarActividadesPorPeriodo();
      } else {
        this.cargarActividades();
      }
      
      // Verificar si ya existe un reporte para este mes/año
      await this.verificarReporteExistente();
    },
    
    async verificarReporteExistente() {
      if (!this.usuarioInfo.id) return;
      
      try {
        this.verificandoReporte = true;
        const response = await api.get(`/reportes/verificar/${this.usuarioInfo.id}`, {
          params: {
            mes: this.mesActual,
            anio: this.anioSeleccionado
          }
        });
        
        if (response.data.existe) {
          this.reporteExistente = response.data.reporte;
          console.log(`📋 Ya existe reporte para ${this.mesActual} ${this.anioSeleccionado}`);
        } else {
          this.reporteExistente = null;
        }
      } catch (error) {
        console.error('⚠️ Error verificando reporte existente:', error);
        this.reporteExistente = null;
      } finally {
        this.verificandoReporte = false;
      }
    },

    formatearFecha(fechaHora) {
      if (!fechaHora) return '-';
      const date = new Date(fechaHora);
      return date.toLocaleDateString('es-MX', {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },

    formatearHora(fechaHora) {
      if (!fechaHora) return '-';
      const date = new Date(fechaHora);
      return date.toLocaleTimeString('es-MX', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      });
    },

    formatearFechaFirma(fechaFirma) {
      if (!fechaFirma) return '';
      const date = new Date(fechaFirma);
      return date.toLocaleDateString('es-MX', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    formatearFechaCompleta(fecha) {
      if (!fecha) return '-';
      const date = new Date(fecha);
      return date.toLocaleDateString('es-MX', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      });
    },

    capitalizar(texto) {
      return texto.charAt(0).toUpperCase() + texto.slice(1);
    },

    // Verificar si hay firma válida (método en lugar de computed para reactividad con refs)
    esFirmaValida() {
      return this.$refs.firmaComponent?.hayFirma || false;
    },

    // Iniciar proceso de descarga - verificar firma primero
    async iniciarDescarga() {
      if (this.actividades.length === 0) {
        alert('No hay actividades para generar el reporte');
        return;
      }

      // Verificar si hay firma
      if (!this.$refs.firmaComponent?.hayFirma) {
        alert('Por favor, firma el reporte antes de descargarlo');
        // Hacer scroll al componente de firma
        const firmaSection = document.querySelector('.glass-card:has([ref="firmaComponent"])') || 
                            document.querySelectorAll('.glass-card')[3];
        if (firmaSection) {
          firmaSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        return;
      }

      // Verificar si ya existe un reporte para este mes/año
      try {
        this.verificandoReporte = true;
        const response = await api.get(`/reportes/verificar/${this.usuarioInfo.id}`, {
          params: {
            mes: this.mesActual,
            anio: this.anioSeleccionado
          }
        });
        
        if (response.data.existe) {
          this.reporteExistente = response.data.reporte;
          const fechaGeneracion = new Date(response.data.reporte.fecha_generacion).toLocaleDateString('es-MX', {
            day: 'numeric',
            month: 'long',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
          });
          alert(`Ya existe un reporte firmado para ${this.mesActual} ${this.anioSeleccionado}.\n\nFue generado el ${fechaGeneracion}.\n\nSolo puedes generar un reporte por mes.`);
          return;
        }
      } catch (error) {
        console.error('⚠️ Error verificando reporte existente:', error);
        // Si hay error de conexión, permitir continuar pero advertir
        if (!navigator.onLine) {
          alert('⚠️ Sin conexión. No se puede verificar si ya existe un reporte para este mes.');
          return;
        }
      } finally {
        this.verificandoReporte = false;
      }

      // Mostrar modal de confirmación
      this.confirmarFirma = false;
      this.mostrarModalFirma = true;
    },

    // Cerrar modal
    cerrarModalFirma() {
      this.mostrarModalFirma = false;
      this.confirmarFirma = false;
    },

    // Confirmar y proceder con la descarga - NO CIERRA EL MODAL HASTA TERMINAR
    async confirmarYDescargar() {
      // Prevenir doble clic
      if (this.procesandoDescarga) {
        console.log('⚠️ Ya se está procesando una descarga');
        return;
      }
      
      if (!this.confirmarFirma) {
        console.log('⚠️ No se ha confirmado la firma');
        return;
      }
      
      // Verificar firma
      const firmaValida = this.$refs.firmaComponent?.hayFirma || false;
      if (!firmaValida) {
        alert('La firma no es válida. Por favor, vuelve a firmar.');
        return;
      }
      
      // Verificar actividades
      if (this.actividades.length === 0) {
        alert('No hay actividades para generar el reporte');
        return;
      }

      console.log('🚀 Iniciando proceso de guardado de reporte...');
      
      // Activar estado de procesamiento - EL MODAL SE MANTIENE ABIERTO
      this.procesandoDescarga = true;
      this.generandoReporte = true;
      
      try {
        console.log('📄 Preparando datos del reporte...');
        
        // NUEVO FLUJO: Guardar datos estructurados, NO generar PDF
        const firmaUsuarioBase64 = this.$refs.firmaComponent.obtenerFirmaBase64();
        
        // Construir objeto con los datos del reporte
        const datosReporte = {
          // Información del usuario
          usuario: {
            id: this.usuarioInfo.id,
            nombre: this.usuarioInfo.nombre,
            cargo: this.usuarioInfo.cargo,
            curp: this.usuarioInfo.curp,
            territorio: this.usuarioInfo.territorio,
            supervisor: this.usuarioInfo.supervisor,
            correo: this.usuarioInfo.correo
          },
          // Período del reporte
          periodo: {
            mes: this.mesSeleccionado,
            mesNombre: this.mesActual,
            anio: this.anioSeleccionado,
            fechaInicio: new Date(this.anioSeleccionado, this.mesSeleccionado, 1).toISOString(),
            fechaFin: new Date(this.anioSeleccionado, this.mesSeleccionado + 1, 0).toISOString()
          },
          // Actividades del período
          actividades: this.actividades.map(act => ({
            id: act.id,
            fecha_hora: act.fecha_hora,
            tipo_actividad: act.tipo_actividad,
            categoria_actividad: act.categoria_actividad,
            descripcion: act.descripcion,
            foto_url: act.foto_url,
            latitud: act.latitud,
            longitud: act.longitud
          })),
          // Estadísticas
          estadisticas: {
            totalActividades: this.actividades.length,
            actividadesCampo: this.actividades.filter(a => (a.tipo_actividad || '').toLowerCase() === 'campo').length,
            actividadesGabinete: this.actividades.filter(a => (a.tipo_actividad || '').toLowerCase() === 'gabinete').length
          },
          // Fecha de generación
          fechaGeneracion: new Date().toISOString()
        };

        console.log('✅ Datos del reporte preparados:', datosReporte.estadisticas);

        // Agregar a historial local con TODOS los campos necesarios
        const fecha = new Date().toLocaleString('es-MX');
        const nombreReporte = `Reporte ${this.mesActual} ${this.anioSeleccionado}`;
        
        // Crear el objeto del reporte con todos los campos
        const nuevoReporte = {
          id: Date.now(), // ID temporal, se actualizará con el de BD
          nombre: nombreReporte,
          mes: this.mesActual,
          anio: this.anioSeleccionado,
          fecha,
          tipo: 'PDF',
          tiene_pdf: true, // Se puede generar PDF desde datos
          firmado_supervisor: false
        };

        // Guardar en la base de datos (datos estructurados + firma usuario)
        try {
          console.log('💾 Guardando reporte en BD (datos estructurados)...');
          
          const datosGuardar = {
            usuario_id: this.usuarioInfo.id,
            nombre_reporte: nombreReporte,
            mes: this.mesActual,
            anio: this.anioSeleccionado,
            tipo: 'PDF',
            // NUEVO: Datos estructurados y firma del usuario
            datos_reporte: datosReporte,
            firma_usuario_base64: firmaUsuarioBase64
            // NO enviamos pdf_base64 - se generará cuando se descargue
          };
          
          console.log('💾 Enviando a /reportes/guardar...');
          const response = await api.post('/reportes/guardar', datosGuardar);
          console.log('✅ Reporte guardado en la base de datos');
          console.log('✅ Respuesta del servidor:', response.data);
          
          // Actualizar el ID del reporte local con el ID real de la BD
          if (response.data && response.data.reporte_id) {
            nuevoReporte.id = response.data.reporte_id;
          }
          
          // Agregar al historial local DESPUÉS de confirmar guardado en BD
          this.reportesGenerados.unshift(nuevoReporte);
          
          // Actualizar localStorage
          localStorage.setItem('reportesGenerados', JSON.stringify(this.reportesGenerados));
          
          // Marcar que ya existe un reporte para este mes (REACTIVO)
          this.reporteExistente = {
            id: nuevoReporte.id,
            nombre: nombreReporte,
            fecha_generacion: new Date().toISOString()
          };
          
          console.log('🔒 reporteExistente establecido - botón se deshabilitará');
          
          // GENERAR Y DESCARGAR EL PDF INMEDIATAMENTE PARA EL USUARIO
          console.log('📄 Generando PDF para descarga inmediata...');
          try {
            const pdfBase64 = await this.generarPDFDesdesDatos(
              datosReporte,
              firmaUsuarioBase64,
              null, // Sin firma de supervisor todavía
              null
            );
            
            // Descargar el PDF
            await this.descargarPDFBase64(pdfBase64, nombreReporte);
            
            console.log('✅ PDF generado y descargado para el usuario');
          } catch (pdfError) {
            console.error('⚠️ Error generando PDF para descarga:', pdfError);
            // No bloquear el flujo si falla la descarga, el usuario puede verlo después en historial
          }
          
          // Mostrar mensaje de éxito
          this.$notify?.({
            type: 'success',
            message: 'Reporte firmado y guardado. Tu supervisor podrá revisarlo y autorizarlo.'
          });
          
        } catch (error) {
          console.error('⚠️ Error guardando reporte en BD:', error);
          console.error('⚠️ Detalles del error:', error.response?.data);
          
          // Si hay error 409 (duplicado), mostrar mensaje y no agregar al historial local
          if (error.response?.status === 409) {
            this.$notify?.({
              type: 'warning',
              message: error.response.data.detail || 'Ya existe un reporte para este mes'
            });
            return; // No continuar si hay duplicado
          }
          
          // Para otros errores de BD
          throw error;
        }
        
      } catch (error) {
        console.error('❌ Error generando reporte:', error);
        this.$notify?.({
          type: 'error',
          message: 'Error al guardar el reporte'
        });
      } finally {
        // AHORA sí cerramos el modal, DESPUÉS de terminar todo
        this.procesandoDescarga = false;
        this.generandoReporte = false;
        this.mostrarModalFirma = false;
        this.confirmarFirma = false;
        console.log('🏁 Proceso de guardado finalizado');
      }
    },

    async generarReporte() {
      // Este método ya no se usa directamente, pero lo mantenemos por compatibilidad
      try {
        if (this.actividades.length === 0) {
          alert('No hay actividades para generar el reporte');
          return;
        }

        this.generandoReporte = true;

        if (this.formatoSeleccionado === 'pdf') {
          const pdfBase64 = await this.generarPDF();
          // Descargar después de generar
          if (this._pdfDocumentoGenerado) {
            await this.descargarPDFSeguro(this._pdfDocumentoGenerado, this._pdfNombreArchivo);
            this._pdfDocumentoGenerado = null;
            this._pdfNombreArchivo = null;
          }
        } else {
          this.generarCSV();
        }

        // Agregar a historial local
        const fecha = new Date().toLocaleString('es-MX');
        const nombreReporte = `Reporte ${this.mesActual} ${this.anioSeleccionado}`;
        
        this.reportesGenerados.unshift({
          id: Date.now(),
          nombre: nombreReporte,
          fecha,
          tipo: this.formatoSeleccionado.toUpperCase()
        });

        // Guardar en la base de datos
        try {
          await api.post('/reportes/guardar', {
            usuario_id: this.usuarioInfo.id,
            nombre_reporte: nombreReporte,
            mes: this.mesActual,
            anio: this.anioSeleccionado,
            tipo: this.formatoSeleccionado.toUpperCase()
          });
          console.log('✅ Reporte guardado en la base de datos');
        } catch (error) {
          console.error('⚠️ Error guardando reporte en BD:', error);
          // No mostramos error al usuario, solo lo registramos
        }

        this.$notify?.({
          type: 'success',
          message: 'Reporte generado correctamente'
        });
      } catch (error) {
        console.error('❌ Error generando reporte:', error);
        this.$notify?.({
          type: 'error',
          message: 'Error al generar el reporte'
        });
      } finally {
        this.generandoReporte = false;
      }
    },

    async generarPDF() {
      try {
        console.log('📄 Iniciando generación de PDF...');
        
        const doc = new jsPDF({
          orientation: 'portrait',
          unit: 'mm',
          format: 'a4'
        });

        const pageHeight = doc.internal.pageSize.getHeight();
        const pageWidth = doc.internal.pageSize.getWidth();
        const margin = 15;
        const contentWidth = pageWidth - (margin * 2);
        let currentY = 10;

        // ========== ENCABEZADO CON IMAGEN DE LOGOS ==========
        console.log('🖼️ Cargando imagen de encabezado...');
        
        // Cargar imagen como base64 para evitar problemas de CORS y formato
        let superiorImageBase64;
        let imgDimensions;
        try {
          const result = await this.cargarImagenComoBase64(superiorImage);
          superiorImageBase64 = result.data;
          imgDimensions = result.dimensions;
        } catch (error) {
          console.warn('⚠️ No se pudo cargar imagen de encabezado, continuando sin ella:', error);
          // Continuar sin imagen de encabezado
          currentY = 10;
        }
        
        if (superiorImageBase64 && imgDimensions) {
          // Calcular dimensiones reales manteniendo aspect ratio
          const realAspectRatio = imgDimensions.height / imgDimensions.width;
          
          // Usar 95% del ancho para que sea grande sin distorsión
          const imgWidth = contentWidth * 0.95;
          const imgHeight = imgWidth * realAspectRatio;
          
          // Centrar la imagen
          const imgX = margin + (contentWidth - imgWidth) / 2;
          
          doc.addImage(superiorImageBase64, 'PNG', imgX, currentY, imgWidth, imgHeight);
          currentY += imgHeight + 5;
          console.log('✅ Imagen de encabezado agregada');
        }
      
      // Recuadro principal con títulos
      doc.setDrawColor(0, 0, 0);
      doc.setLineWidth(0.5);
      doc.rect(margin, currentY, contentWidth, 25);
      
      // Títulos centrados
      doc.setFontSize(9);
      doc.setFont(undefined, 'bold');
      doc.setTextColor(0, 0, 0);
      doc.text('SECRETARÍA DE BIENESTAR', pageWidth / 2, currentY + 6, { align: 'center' });
      doc.text('SUBSECRETARÍA DE INCLUSIÓN PRODUCTIVA Y DESARROLLO RURAL', pageWidth / 2, currentY + 11, { align: 'center' });
      doc.text('FORMATO DE SEGUIMIENTO A ACTIVIDADES PROGRAMADAS', pageWidth / 2, currentY + 16, { align: 'center' });
      
      // Fecha en la esquina superior derecha
      const fechaActual = new Date().toLocaleDateString('es-MX', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      });
      doc.setFontSize(8);
      doc.setFont(undefined, 'normal');
      doc.text('Fecha:', pageWidth - margin - 35, currentY + 21);
      doc.rect(pageWidth - margin - 25, currentY + 18, 25, 5);
      doc.text(fechaActual, pageWidth - margin - 12.5, currentY + 21.5, { align: 'center' });
      
      currentY += 30;
      
      // ========== TABLA DE INFORMACIÓN DEL PRESTADOR ==========
      const tableStartY = currentY;
      const col1Width = contentWidth * 0.5;
      const col2Width = contentWidth * 0.5;
      
      // Fila 1: Nombre del prestador
      doc.setDrawColor(0, 0, 0);
      doc.setLineWidth(0.3);
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      
      doc.setFontSize(8);
      doc.setFont(undefined, 'bold');
      doc.text('Nombre del prestador de Servicios', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      doc.text(this.usuarioInfo.nombre, margin + col1Width + 2, currentY + 4);
      
      currentY += 6;
      
      // Fila 2: CURP
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      
      doc.setFont(undefined, 'bold');
      doc.text('CURP', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      doc.text(this.usuarioInfo.curp || 'No registrado', margin + col1Width + 2, currentY + 4);
      
      currentY += 6;
      
      // Fila 3: Periodo
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      
      doc.setFont(undefined, 'bold');
      doc.text('Periodo', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      const inicioPeriodo = new Date(this.anioSeleccionado, this.mesSeleccionado, 1);
      const finPeriodo = new Date(this.anioSeleccionado, this.mesSeleccionado + 1, 0);
      const periodoTexto = `Del ${inicioPeriodo.toLocaleDateString('es-MX')} al ${finPeriodo.toLocaleDateString('es-MX')}`;
      doc.text(periodoTexto, margin + col1Width + 2, currentY + 4);
      
      currentY += 8;
      
      // Fila 4: Programa Social del Apoyo (celda completa)
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      
      doc.setFont(undefined, 'bold');
      doc.text('Programa Social del Apoyo', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      doc.text('SEMBRANDO VIDA', margin + col1Width + 2, currentY + 4);
      
      currentY += 8;
      
      // Fila 5: Territorio (celda completa)
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      
      doc.setFont(undefined, 'bold');
      doc.text('Territorio y entidad donde presta sus servicios', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      doc.text(this.usuarioInfo.territorio || 'No asignado', margin + col1Width + 2, currentY + 4);
      
      currentY += 10;
      
      // ========== TABLA DE ACTIVIDADES ==========
      // Definir columnas de la tabla
      const tableWidth = contentWidth;
      const tableX = margin;
      const colWidths = [15, 32, 18, 22, 83]; // No., Fecha, Tipo, Hora, Actividad
      
      // Header de la tabla
      doc.setDrawColor(0, 0, 0);
      doc.setLineWidth(0.3);
      doc.setFillColor(255, 255, 255);
      doc.rect(tableX, currentY, tableWidth, 8, 'FD');
      
      doc.setTextColor(0, 0, 0);
      doc.setFontSize(8);
      doc.setFont(undefined, 'bold');
      
      let colX = tableX + 2;
      doc.text('No.', colX + colWidths[0]/2, currentY + 5.5, { align: 'center' });
      doc.line(colX + colWidths[0], currentY, colX + colWidths[0], currentY + 8);
      
      colX += colWidths[0];
      doc.text('Fecha', colX + colWidths[1]/2, currentY + 5.5, { align: 'center' });
      doc.line(colX + colWidths[1], currentY, colX + colWidths[1], currentY + 8);
      
      colX += colWidths[1];
      doc.text('Tipo', colX + colWidths[2]/2, currentY + 5.5, { align: 'center' });
      doc.line(colX + colWidths[2], currentY, colX + colWidths[2], currentY + 8);
      
      colX += colWidths[2];
      doc.text('Hora', colX + colWidths[3]/2, currentY + 5.5, { align: 'center' });
      doc.line(colX + colWidths[3], currentY, colX + colWidths[3], currentY + 8);
      
      colX += colWidths[3];
      doc.text('Actividad desarrollada', colX + colWidths[4]/2, currentY + 5.5, { align: 'center' });

      currentY += 8;
      
      // Filas de datos
      doc.setTextColor(0, 0, 0);
      doc.setFontSize(7);
      doc.setFont(undefined, 'normal');
      
      const baseRowHeight = 8;
      const lineHeight = 3; // Altura de cada línea de texto

      this.actividades.forEach((actividad, index) => {
        // Obtener la descripción completa
        const activDesc = actividad.descripcion || actividad.categoria_actividad || 'Actividad de ' + (actividad.tipo_actividad || 'campo');
        
        // Calcular cuántas líneas necesita la descripción
        const maxTextWidth = colWidths[4] - 4; // Ancho disponible para texto con margen
        const textLines = doc.splitTextToSize(activDesc, maxTextWidth);
        const numLines = textLines.length;
        
        // Calcular altura de fila basada en el número de líneas (mínimo 8, máximo según contenido)
        const rowHeight = Math.max(baseRowHeight, numLines * lineHeight + 3);
        
        // Verificar si necesitamos nueva página
        if (currentY > pageHeight - 50) {
          doc.addPage();
          currentY = 20;
          
          // Re-dibujar header de tabla en nueva página
          doc.setDrawColor(0, 0, 0);
          doc.setLineWidth(0.3);
          doc.setFillColor(255, 255, 255);
          doc.rect(tableX, currentY, tableWidth, 8, 'FD');
          
          doc.setTextColor(0, 0, 0);
          doc.setFontSize(8);
          doc.setFont(undefined, 'bold');
          
          let headerX = tableX + 2;
          doc.text('No.', headerX + colWidths[0]/2, currentY + 5.5, { align: 'center' });
          doc.line(headerX + colWidths[0], currentY, headerX + colWidths[0], currentY + 8);
          
          headerX += colWidths[0];
          doc.text('Fecha', headerX + colWidths[1]/2, currentY + 5.5, { align: 'center' });
          doc.line(headerX + colWidths[1], currentY, headerX + colWidths[1], currentY + 8);
          
          headerX += colWidths[1];
          doc.text('Tipo', headerX + colWidths[2]/2, currentY + 5.5, { align: 'center' });
          doc.line(headerX + colWidths[2], currentY, headerX + colWidths[2], currentY + 8);
          
          headerX += colWidths[2];
          doc.text('Hora', headerX + colWidths[3]/2, currentY + 5.5, { align: 'center' });
          doc.line(headerX + colWidths[3], currentY, headerX + colWidths[3], currentY + 8);
          
          headerX += colWidths[3];
          doc.text('Actividad desarrollada', headerX + colWidths[4]/2, currentY + 5.5, { align: 'center' });
          
          currentY += 8;
          doc.setTextColor(0, 0, 0);
          doc.setFontSize(7);
          doc.setFont(undefined, 'normal');
        }

        // Bordes de la fila
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.3);
        doc.rect(tableX, currentY, tableWidth, rowHeight, 'S');

        const fecha = this.formatearFecha(actividad.fecha_hora);
        const hora = this.formatearHora(actividad.fecha_hora);
        const tipo = this.capitalizar(actividad.tipo_actividad || 'Campo');

        colX = tableX + 2;
        
        // Posición vertical centrada para celdas de una línea
        const textYCenter = currentY + (rowHeight / 2) + 1.5;
        
        // No.
        doc.text(String(index + 1), colX + colWidths[0]/2, textYCenter, { align: 'center' });
        doc.line(colX + colWidths[0], currentY, colX + colWidths[0], currentY + rowHeight);
        
        // Fecha
        colX += colWidths[0];
        doc.text(fecha, colX + 2, textYCenter);
        doc.line(colX + colWidths[1], currentY, colX + colWidths[1], currentY + rowHeight);
        
        // Tipo (Campo/Gabinete)
        colX += colWidths[1];
        doc.text(tipo, colX + colWidths[2]/2, textYCenter, { align: 'center' });
        doc.line(colX + colWidths[2], currentY, colX + colWidths[2], currentY + rowHeight);
        
        // Hora de registro de la actividad
        colX += colWidths[2];
        doc.text(hora, colX + colWidths[3]/2, textYCenter, { align: 'center' });
        doc.line(colX + colWidths[3], currentY, colX + colWidths[3], currentY + rowHeight);
        
        // Actividad - Descripción completa con múltiples líneas
        colX += colWidths[3];
        // Dibujar cada línea de texto
        textLines.forEach((line, lineIndex) => {
          doc.text(line, colX + 2, currentY + 4 + (lineIndex * lineHeight));
        });

        currentY += rowHeight;
      });

      currentY += 15;

      // ========== SECCIÓN DE FIRMAS (Formato oficial) ==========
      if (this.$refs.firmaComponent?.hayFirma) {
        // Verificar si necesitamos nueva página para las firmas
        if (currentY > pageHeight - 70) {
          doc.addPage();
          currentY = 30;
        }

        // Configuración de las dos columnas de firma
        const firmaWidth = 70;
        const firmaHeight = 30;
        const espacioEntreFiremas = 20;
        const firmaUsuarioX = margin + 5;
        const firmaResponsableX = pageWidth - margin - firmaWidth - 5;
        
        const firmaY = currentY;
        
        // ========== ETIQUETAS "Elaboró" y "Aprobó" ==========
        doc.setFillColor(255, 218, 185); // Color durazno/naranja claro
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.3);
        
        // Etiqueta "Elaboró"
        doc.rect(firmaUsuarioX, firmaY - 8, firmaWidth, 7, 'FD');
        doc.setTextColor(0, 0, 0);
        doc.setFontSize(9);
        doc.setFont(undefined, 'bold');
        doc.text('Elaboró', firmaUsuarioX + firmaWidth / 2, firmaY - 3.5, { align: 'center' });
        
        // Etiqueta "Autorizó" - restablecer color de fondo
        doc.setFillColor(255, 218, 185); // Color durazno/naranja claro
        doc.rect(firmaResponsableX, firmaY - 8, firmaWidth, 7, 'FD');
        doc.text('Autorizó', firmaResponsableX + firmaWidth / 2, firmaY - 3.5, { align: 'center' });
        
        // ========== FIRMA DEL PRESTADOR DE SERVICIOS (Izquierda) ==========
        // Imagen de firma del usuario (sin rectángulo contenedor)
        const firmaBase64 = this.$refs.firmaComponent.obtenerFirmaBase64();
        doc.addImage(firmaBase64, 'PNG', firmaUsuarioX, firmaY, firmaWidth, firmaHeight);
        
        // Línea de firma usuario
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.5);
        doc.line(firmaUsuarioX, firmaY + firmaHeight + 5, firmaUsuarioX + firmaWidth, firmaY + firmaHeight + 5);
        
        // Cargo del usuario (primero)
        doc.setTextColor(0, 0, 0);
        doc.setFontSize(8);
        doc.setFont(undefined, 'normal');
        const cargoUsuario = this.usuarioInfo.cargo || 'Facilitador Comunitario';
        doc.text(cargoUsuario, firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' });
        
        // Nombre del usuario (después, en negrita)
        doc.setFontSize(8);
        doc.setFont(undefined, 'bold');
        const nombreUsuario = this.usuarioInfo.nombre || 'Sin nombre';
        doc.text(nombreUsuario, firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 17, { align: 'center' });
        
        // ========== FIRMA DEL RESPONSABLE (Derecha) ==========
        // Sin imagen, solo espacio vacío para firma manual
        
        // Línea de firma responsable
        doc.setLineWidth(0.5);
        doc.line(firmaResponsableX, firmaY + firmaHeight + 5, firmaResponsableX + firmaWidth, firmaY + firmaHeight + 5);
        
        // Cargo del responsable (primero, puede ser en dos líneas)
        doc.setFontSize(7.5);
        doc.setFont(undefined, 'normal');
        doc.text('Encargada de Despacho de la Coordinación', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' });
        doc.text('Territorial ' + (this.usuarioInfo.territorio || ''), firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 16, { align: 'center' });
        
        // Nombre del supervisor/responsable (después, en negrita)
        doc.setFontSize(8);
        doc.setFont(undefined, 'bold');
        const nombreSupervisor = this.usuarioInfo.supervisor || 'Sin asignar';
        doc.text(nombreSupervisor, firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 22, { align: 'center' });
        
        currentY = firmaY + firmaHeight + 30;
      }

      // ========== SEGUNDA PÁGINA: EVIDENCIAS FOTOGRÁFICAS ==========
      try {
        console.log('🖼️ Iniciando generación de página de evidencias fotográficas...');
        
        // Filtrar actividades del mes seleccionado con fotos
        const inicioPeriodo = new Date(this.anioSeleccionado, this.mesSeleccionado, 1);
        const finPeriodo = new Date(this.anioSeleccionado, this.mesSeleccionado + 1, 0);
        
        const actividadesConFoto = this.actividades.filter(actividad => {
          if (!actividad.foto_url) return false;
          const fechaActividad = new Date(actividad.fecha_hora);
          return fechaActividad >= inicioPeriodo && fechaActividad <= finPeriodo;
        });

        console.log(`📸 Actividades con foto encontradas en ${this.mesActual}: ${actividadesConFoto.length}`);
        console.log('🔍 Actividades con foto:', actividadesConFoto.map(a => ({ 
          foto_url: a.foto_url, 
          fecha: a.fecha_hora,
          tipo: a.tipo_actividad 
        })));
        
        console.log('📊 DEBUG - Total actividades cargadas:', this.actividades.length);
        console.log('📊 DEBUG - Actividades con foto_url:', this.actividades.filter(a => a.foto_url).length);

        // SIEMPRE crear la página de evidencias fotográficas
        doc.addPage();
        currentY = 10;

        // ========== ENCABEZADO DE LA PÁGINA DE EVIDENCIAS ==========
        // Cargar imagen de logos (reutilizar la misma imagen cargada)
        if (superiorImageBase64 && imgDimensions) {
          const realAspectRatio = imgDimensions.height / imgDimensions.width;
          const imgWidth = contentWidth * 0.95;
          const imgHeight = imgWidth * realAspectRatio;
          const imgX = margin + (contentWidth - imgWidth) / 2;
          
          doc.addImage(superiorImageBase64, 'PNG', imgX, currentY, imgWidth, imgHeight);
          currentY += imgHeight + 5;
        }
        
        // Título de la sección
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.5);
        doc.rect(margin, currentY, contentWidth, 12);
          
        doc.setFontSize(11);
        doc.setFont(undefined, 'bold');
        doc.setTextColor(0, 0, 0);
        doc.text('EVIDENCIAS FOTOGRÁFICAS DE ACTIVIDADES', pageWidth / 2, currentY + 5, { align: 'center' });
        doc.setFontSize(9);
        doc.setFont(undefined, 'normal');
        doc.text(`${this.mesActual} ${this.anioSeleccionado}`, pageWidth / 2, currentY + 10, { align: 'center' });
        
        currentY += 15;

        // ========== DATOS DEL USUARIO ==========
        doc.setFillColor(240, 240, 240);
        doc.setDrawColor(0, 0, 0);
        doc.setLineWidth(0.3);
        doc.rect(margin, currentY, contentWidth, 18, 'FD');
        
        doc.setFontSize(8);
        doc.setTextColor(0, 0, 0);
        
        // Nombre
        doc.setFont(undefined, 'bold');
        doc.text('Nombre:', margin + 3, currentY + 5);
        doc.setFont(undefined, 'normal');
        doc.text(this.usuarioInfo.nombre || 'Sin nombre', margin + 20, currentY + 5);
        
        // CURP
        doc.setFont(undefined, 'bold');
        doc.text('CURP:', margin + 95, currentY + 5);
        doc.setFont(undefined, 'normal');
        doc.text(this.usuarioInfo.curp || 'No registrado', margin + 107, currentY + 5);
        
        // Cargo
        doc.setFont(undefined, 'bold');
        doc.text('Cargo:', margin + 3, currentY + 11);
        doc.setFont(undefined, 'normal');
        doc.text(this.usuarioInfo.cargo || 'Facilitador Comunitario', margin + 17, currentY + 11);
        
        // Territorio
        doc.setFont(undefined, 'bold');
        doc.text('Territorio:', margin + 95, currentY + 11);
        doc.setFont(undefined, 'normal');
        doc.text(this.usuarioInfo.territorio || 'No asignado', margin + 115, currentY + 11);
        
        // Período
        doc.setFont(undefined, 'bold');
        doc.text('Período:', margin + 3, currentY + 17);
        doc.setFont(undefined, 'normal');
        doc.text(`${this.mesActual} ${this.anioSeleccionado}`, margin + 18, currentY + 17);
        
        currentY += 22;

        // ========== VERIFICAR SI HAY IMÁGENES ==========
        if (actividadesConFoto.length === 0) {
          // Mostrar mensaje cuando no hay fotos disponibles
          currentY += 20;
          doc.setFillColor(255, 243, 205); // Amarillo claro
          doc.setDrawColor(200, 180, 100);
          doc.setLineWidth(0.5);
          doc.rect(margin, currentY, contentWidth, 40, 'FD');
          
          doc.setTextColor(120, 100, 50);
          doc.setFontSize(12);
          doc.setFont(undefined, 'bold');
          doc.text('Sin evidencias fotográficas disponibles', pageWidth / 2, currentY + 15, { align: 'center' });
          
          doc.setFontSize(9);
          doc.setFont(undefined, 'normal');
          doc.text('El reporte fotográfico solo está disponible para el mes en curso;', pageWidth / 2, currentY + 25, { align: 'center' });
          doc.text('al descargar información de meses anteriores, las fotografías no se mostrarán.', pageWidth / 2, currentY + 32, { align: 'center' });
          
          currentY += 50;
        } else {
          // ========== SELECCIÓN DE 6 IMÁGENES: PRIMERO CAMPO, LUEGO GABINETE ==========
          // Separar por tipo
          const actividadesCampo = actividadesConFoto
            .filter(a => (a.tipo_actividad || 'campo').toLowerCase() === 'campo')
            .sort((a, b) => new Date(b.fecha_hora) - new Date(a.fecha_hora)); // Más recientes primero
          
          const actividadesGabinete = actividadesConFoto
            .filter(a => (a.tipo_actividad || '').toLowerCase() === 'gabinete')
            .sort((a, b) => new Date(b.fecha_hora) - new Date(a.fecha_hora)); // Más recientes primero
          
          // Seleccionar imágenes: primero todas las de campo, luego todas las de gabinete
          let imagenesSeleccionadas = [];
          const maxImagenes = 6;
          
          // Calcular cuántas de cada tipo (máximo 3 de campo y 3 de gabinete si hay de ambos)
          let maxCampo = Math.min(actividadesCampo.length, 3);
          let maxGabinete = Math.min(actividadesGabinete.length, 3);
          
          // Si solo hay de un tipo, usar hasta 6 de ese tipo
          if (actividadesCampo.length === 0) {
            maxGabinete = Math.min(actividadesGabinete.length, maxImagenes);
          } else if (actividadesGabinete.length === 0) {
            maxCampo = Math.min(actividadesCampo.length, maxImagenes);
          } else {
            // Hay de ambos - distribuir el espacio restante
            const espacioRestanteCampo = maxImagenes - maxGabinete;
            const espacioRestanteGabinete = maxImagenes - maxCampo;
            maxCampo = Math.min(actividadesCampo.length, espacioRestanteCampo);
            maxGabinete = Math.min(actividadesGabinete.length, maxImagenes - maxCampo);
          }
          
          // Agregar primero las de campo
          for (let i = 0; i < maxCampo; i++) {
            imagenesSeleccionadas.push(actividadesCampo[i]);
          }
          
          // Luego las de gabinete
          for (let i = 0; i < maxGabinete; i++) {
            imagenesSeleccionadas.push(actividadesGabinete[i]);
          }
          
          console.log(`📷 Seleccionadas ${imagenesSeleccionadas.length} imágenes variadas (Campo: ${actividadesCampo.length}, Gabinete: ${actividadesGabinete.length})`);
          
          // ========== GRID DE IMÁGENES ==========
          const imgGridWidth = 55; // Ancho de cada imagen
          const imgGridHeight = 45; // Alto de cada imagen
          const imgsPerRow = 3;
          const imgSpacing = 5;
          const labelHeight = 14; // Aumentado para mejor visualización
          
          // Cargar imágenes y dibujarlas
          let imgIndex = 0;
          const totalImagenes = imagenesSeleccionadas.length;
          
          console.log(`📷 Procesando ${totalImagenes} imágenes...`);
          
          for (let i = 0; i < totalImagenes; i++) {
            const actividad = imagenesSeleccionadas[i];
            
            // Verificar si necesitamos nueva página
            if (currentY + imgGridHeight + labelHeight + 15 > pageHeight - 40) {
              doc.addPage();
              currentY = 20;
              
              // Título continuación
              doc.setFontSize(9);
              doc.setFont(undefined, 'bold');
              doc.setTextColor(0, 0, 0);
              doc.text('EVIDENCIAS FOTOGRÁFICAS (Continuación)', pageWidth / 2, currentY, { align: 'center' });
              currentY += 10;
            }            const col = imgIndex % imgsPerRow;
            const imgX = margin + (col * (imgGridWidth + imgSpacing));
            
            // Si es primera columna de una fila nueva, ajustar Y
            if (col === 0 && imgIndex > 0) {
              currentY += imgGridHeight + labelHeight + 10;
            }
            
            try {
              // La URL ya viene completa del servidor
              const fotoUrl = actividad.foto_url;
              
              console.log(`📷 [${i + 1}/${totalImagenes}] Cargando imagen: ${fotoUrl}`);
              
              // Cargar imagen como base64 con timeout
              const imgResult = await this.cargarImagenComoBase64(fotoUrl);
              const imgData = imgResult.data;
              
              if (imgData) {
                console.log(`✅ [${i + 1}/${totalImagenes}] Imagen cargada exitosamente`);
                
                // Borde de la imagen
                doc.setDrawColor(0, 0, 0);
                doc.setLineWidth(0.3);
                doc.rect(imgX, currentY, imgGridWidth, imgGridHeight);
                
                // Imagen
                doc.addImage(imgData, 'JPEG', imgX + 1, currentY + 1, imgGridWidth - 2, imgGridHeight - 2);
                
                // Etiqueta debajo con información
                const tipoAct = actividad.tipo_actividad || 'campo';
                const tipoTexto = tipoAct.toLowerCase() === 'campo' ? 'CAMPO' : 'GABINETE';
                
                // Formato compacto solo números: DD/MM/AA HH:MM
                const fechaObj = new Date(actividad.fecha_hora);
                const dia = String(fechaObj.getDate()).padStart(2, '0');
                const mes = String(fechaObj.getMonth() + 1).padStart(2, '0');
                const anio = String(fechaObj.getFullYear()).slice(-2);
                const hora = String(fechaObj.getHours()).padStart(2, '0');
                const min = String(fechaObj.getMinutes()).padStart(2, '0');
                const fechaCompacta = `${dia}/${mes}/${anio} ${hora}:${min}`;
                
                // Fondo de etiqueta según tipo
                if (tipoAct.toLowerCase() === 'campo') {
                  doc.setFillColor(34, 197, 94); // Verde para Campo
                } else {
                  doc.setFillColor(147, 51, 234); // Morado para Gabinete
                }
                doc.rect(imgX, currentY + imgGridHeight, imgGridWidth, labelHeight, 'F');
                
                // Borde de la etiqueta
                doc.setDrawColor(0, 0, 0);
                doc.setLineWidth(0.2);
                doc.rect(imgX, currentY + imgGridHeight, imgGridWidth, labelHeight, 'S');
                
                // Tipo de actividad - Grande y en negrita (CAMPO o GABINETE)
                doc.setTextColor(255, 255, 255);
                doc.setFontSize(10);
                doc.setFont(undefined, 'bold');
                doc.text(tipoTexto, imgX + imgGridWidth / 2, currentY + imgGridHeight + 6, { align: 'center' });
                
                // Fecha compacta - Pequeña debajo
                doc.setFont(undefined, 'normal');
                doc.setFontSize(6);
                doc.text(fechaCompacta, imgX + imgGridWidth / 2, currentY + imgGridHeight + 11, { align: 'center' });
              } else {
                throw new Error('No se pudo obtener datos de la imagen');
              }
            } catch (imgError) {
              console.error(`❌ [${i + 1}/${totalImagenes}] Error cargando imagen:`, imgError);
              
              // Dibujar placeholder si falla la carga
              doc.setFillColor(240, 240, 240);
              doc.rect(imgX, currentY, imgGridWidth, imgGridHeight, 'F');
              doc.setDrawColor(200, 200, 200);
              doc.rect(imgX, currentY, imgGridWidth, imgGridHeight, 'S');
              
              doc.setTextColor(150, 150, 150);
              doc.setFontSize(8);
              doc.text('Imagen no', imgX + imgGridWidth / 2, currentY + imgGridHeight / 2 - 3, { align: 'center' });
              doc.text('disponible', imgX + imgGridWidth / 2, currentY + imgGridHeight / 2 + 3, { align: 'center' });
              
              // Etiqueta de información aunque falle la imagen
              const tipoAct = actividad.tipo_actividad || 'campo';
              const tipoTexto = tipoAct.toLowerCase() === 'campo' ? 'CAMPO' : 'GABINETE';
              
              // Formato compacto solo números: DD/MM/AA HH:MM
              const fechaObj = new Date(actividad.fecha_hora);
              const dia = String(fechaObj.getDate()).padStart(2, '0');
              const mes = String(fechaObj.getMonth() + 1).padStart(2, '0');
              const anio = String(fechaObj.getFullYear()).slice(-2);
              const hora = String(fechaObj.getHours()).padStart(2, '0');
              const min = String(fechaObj.getMinutes()).padStart(2, '0');
              const fechaCompacta = `${dia}/${mes}/${anio} ${hora}:${min}`;
              
              if (tipoAct.toLowerCase() === 'campo') {
                doc.setFillColor(34, 197, 94);
              } else {
                doc.setFillColor(147, 51, 234);
              }
              doc.rect(imgX, currentY + imgGridHeight, imgGridWidth, labelHeight, 'F');
              
              // Borde de la etiqueta
              doc.setDrawColor(0, 0, 0);
              doc.setLineWidth(0.2);
              doc.rect(imgX, currentY + imgGridHeight, imgGridWidth, labelHeight, 'S');
              
              doc.setTextColor(255, 255, 255);
              doc.setFontSize(10);
              doc.setFont(undefined, 'bold');
              doc.text(tipoTexto, imgX + imgGridWidth / 2, currentY + imgGridHeight + 6, { align: 'center' });
              doc.setFont(undefined, 'normal');
              doc.setFontSize(6);
              doc.text(fechaCompacta, imgX + imgGridWidth / 2, currentY + imgGridHeight + 11, { align: 'center' });
            }
            
            imgIndex++;
          }
          
          console.log(`✅ Procesadas ${imgIndex} imágenes en total`);
          
          // Ajustar Y después de la última fila
          currentY += imgGridHeight + labelHeight + 15;

          // ========== FIRMA EN PÁGINA DE EVIDENCIAS ==========
          if (this.$refs.firmaComponent?.hayFirma) {
            // Verificar si hay espacio para firmas
            if (currentY > pageHeight - 70) {
              doc.addPage();
              currentY = 30;
            }

            const firmaWidth = 70;
            const firmaHeight = 30;
            const firmaUsuarioX = margin + 5;
            const firmaResponsableX = pageWidth - margin - firmaWidth - 5;
            const firmaY = currentY;
            
            // Etiquetas
            doc.setFillColor(255, 218, 185);
            doc.setDrawColor(0, 0, 0);
            doc.setLineWidth(0.3);
            
            doc.rect(firmaUsuarioX, firmaY - 8, firmaWidth, 7, 'FD');
            doc.setTextColor(0, 0, 0);
            doc.setFontSize(9);
            doc.setFont(undefined, 'bold');
            doc.text('Elaboró', firmaUsuarioX + firmaWidth / 2, firmaY - 3.5, { align: 'center' });
            
            doc.setFillColor(255, 218, 185);
            doc.rect(firmaResponsableX, firmaY - 8, firmaWidth, 7, 'FD');
            doc.text('Autorizó', firmaResponsableX + firmaWidth / 2, firmaY - 3.5, { align: 'center' });
            
            // Firma del usuario
            const firmaBase64 = this.$refs.firmaComponent.obtenerFirmaBase64();
            doc.addImage(firmaBase64, 'PNG', firmaUsuarioX, firmaY, firmaWidth, firmaHeight);
            
            // Líneas de firma
            doc.setLineWidth(0.5);
            doc.line(firmaUsuarioX, firmaY + firmaHeight + 5, firmaUsuarioX + firmaWidth, firmaY + firmaHeight + 5);
            doc.line(firmaResponsableX, firmaY + firmaHeight + 5, firmaResponsableX + firmaWidth, firmaY + firmaHeight + 5);
            
            // Información del usuario
            doc.setTextColor(0, 0, 0);
            doc.setFontSize(8);
            doc.setFont(undefined, 'normal');
            const cargoUsuario = this.usuarioInfo.cargo || 'Facilitador Comunitario';
            doc.text(cargoUsuario, firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' });
            doc.setFont(undefined, 'bold');
            doc.text(this.usuarioInfo.nombre || 'Sin nombre', firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 17, { align: 'center' });
            
            // Información del responsable
            doc.setFontSize(7.5);
            doc.setFont(undefined, 'normal');
            doc.text('Encargada de Despacho de la Coordinación', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' });
            doc.text('Territorial ' + (this.usuarioInfo.territorio || ''), firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 16, { align: 'center' });
            doc.setFontSize(8);
            doc.setFont(undefined, 'bold');
            doc.text(this.usuarioInfo.supervisor || 'Sin asignar', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 22, { align: 'center' });
          }
          
          console.log('✅ Página de evidencias fotográficas completada con imágenes');
        } // Fin del else (cuando hay fotos)
        
        // ========== FIRMA EN PÁGINA DE EVIDENCIAS (para ambos casos) ==========
        if (actividadesConFoto.length === 0 && this.$refs.firmaComponent?.hayFirma) {
          // Agregar firma cuando no hay fotos
          if (currentY > pageHeight - 70) {
            doc.addPage();
            currentY = 30;
          }

          const firmaWidth = 70;
          const firmaHeight = 30;
          const firmaUsuarioX = margin + 5;
          const firmaResponsableX = pageWidth - margin - firmaWidth - 5;
          const firmaY = currentY;
          
          // Etiquetas
          doc.setFillColor(255, 218, 185);
          doc.setDrawColor(0, 0, 0);
          doc.setLineWidth(0.3);
          
          doc.rect(firmaUsuarioX, firmaY - 8, firmaWidth, 7, 'FD');
          doc.setTextColor(0, 0, 0);
          doc.setFontSize(9);
          doc.setFont(undefined, 'bold');
          doc.text('Elaboró', firmaUsuarioX + firmaWidth / 2, firmaY - 3.5, { align: 'center' });
          
          doc.setFillColor(255, 218, 185);
          doc.rect(firmaResponsableX, firmaY - 8, firmaWidth, 7, 'FD');
          doc.text('Autorizó', firmaResponsableX + firmaWidth / 2, firmaY - 3.5, { align: 'center' });
          
          // Firma del usuario
          const firmaBase64 = this.$refs.firmaComponent.obtenerFirmaBase64();
          doc.addImage(firmaBase64, 'PNG', firmaUsuarioX, firmaY, firmaWidth, firmaHeight);
          
          // Líneas de firma
          doc.setLineWidth(0.5);
          doc.line(firmaUsuarioX, firmaY + firmaHeight + 5, firmaUsuarioX + firmaWidth, firmaY + firmaHeight + 5);
          doc.line(firmaResponsableX, firmaY + firmaHeight + 5, firmaResponsableX + firmaWidth, firmaY + firmaHeight + 5);
          
          // Información del usuario
          doc.setTextColor(0, 0, 0);
          doc.setFontSize(8);
          doc.setFont(undefined, 'normal');
          const cargoUsuario = this.usuarioInfo.cargo || 'Facilitador Comunitario';
          doc.text(cargoUsuario, firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' });
          doc.setFont(undefined, 'bold');
          doc.text(this.usuarioInfo.nombre || 'Sin nombre', firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 17, { align: 'center' });
          
          // Información del responsable
          doc.setFontSize(7.5);
          doc.setFont(undefined, 'normal');
          doc.text('Encargada de Despacho de la Coordinación', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' });
          doc.text('Territorial ' + (this.usuarioInfo.territorio || ''), firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 16, { align: 'center' });
          doc.setFontSize(8);
          doc.setFont(undefined, 'bold');
          doc.text(this.usuarioInfo.supervisor || 'Sin asignar', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 22, { align: 'center' });
        }
        
        console.log('✅ Página de evidencias fotográficas completada');
        
      } catch (evidenciasError) {
        console.error('❌ Error CRÍTICO generando página de evidencias:', evidenciasError);
        console.error('Stack trace:', evidenciasError.stack);
        // Continuar con el resto del PDF aunque falle la sección de evidencias
        alert('Advertencia: Hubo un error al generar la página de evidencias fotográficas. Se generará el PDF sin esta sección.');
      }

      // ========== PIE DE PÁGINA CON INFORMACIÓN DE CONTACTO ==========
      const totalPages = doc.internal.getNumberOfPages();
      
      for (let i = 1; i <= totalPages; i++) {
        doc.setPage(i);
        
        // Color guinda: RGB(128, 0, 32) aproximadamente
        doc.setTextColor(128, 0, 32);
        doc.setFontSize(7);
        doc.setFont(undefined, 'normal');
        
        const footerText = 'Paseo de la Reforma # 116, Piso 16, Col. Juárez, Alc. Cuauhtémoc, CDMX C.P. 06600 Tel.: (55) 5328 5000 www.gob.mx/bienestar';
        doc.text(footerText, pageWidth / 2, pageHeight - 10, { align: 'center' });
      }

      // Obtener el PDF como base64 PRIMERO (antes de intentar descargar)
      console.log('📦 Obteniendo PDF como base64...');
      const pdfBase64 = doc.output('datauristring');
      console.log('📦 Base64 obtenido, longitud:', pdfBase64 ? pdfBase64.length : 'NULL');
      
      // Guardar referencia al documento para descarga posterior
      this._pdfDocumentoGenerado = doc;
      this._pdfNombreArchivo = `Reporte_${this.mesActual}_${this.anioSeleccionado}.pdf`;
      
      console.log('✅ PDF generado exitosamente (descarga pendiente)');
      
      // Retornar el base64 para guardarlo en BD
      return pdfBase64;
      
    } catch (error) {
      console.error('❌ Error crítico generando PDF:', error);
      alert('Error al generar el PDF. Por favor, intenta de nuevo.');
      throw error;
    }
  },

    /**
     * Método para descargar el PDF de forma segura en todos los dispositivos (incluyendo móviles)
     * Compatible con iOS Safari, Android Chrome y navegadores de escritorio
     */
    async descargarPDFSeguro(pdfDoc, nombreArchivo) {
      try {
        console.log('💾 Iniciando descarga segura del PDF...');
        console.log('📱 Detectando plataforma...');
        
        // Detectar si es móvil
        const userAgent = navigator.userAgent || navigator.vendor || window.opera;
        const isIOS = /iPad|iPhone|iPod/.test(userAgent) && !window.MSStream;
        const isAndroid = /android/i.test(userAgent);
        const isMobile = isIOS || isAndroid || /mobile/i.test(userAgent);
        
        console.log(`📱 Plataforma: iOS=${isIOS}, Android=${isAndroid}, Mobile=${isMobile}`);
        
        if (isMobile) {
          // En móviles, usar Blob URL con un link temporal
          console.log('📱 Usando método de descarga para móviles...');
          
          // Obtener el PDF como Blob
          const pdfBlob = pdfDoc.output('blob');
          
          // Crear URL del Blob
          const blobUrl = URL.createObjectURL(pdfBlob);
          
          // Crear link temporal
          const link = document.createElement('a');
          link.href = blobUrl;
          link.download = nombreArchivo;
          link.style.display = 'none';
          
          // En iOS Safari, abrir en nueva ventana puede ser más confiable
          if (isIOS) {
            console.log('🍎 iOS detectado - abriendo PDF en nueva ventana...');
            // En iOS, intentar primero abrir en nueva ventana
            const newWindow = window.open(blobUrl, '_blank');
            if (!newWindow) {
              // Si el popup fue bloqueado, intentar con click en link
              console.log('🍎 Popup bloqueado, usando link click...');
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);
            }
          } else {
            // En Android y otros móviles
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          }
          
          // Limpiar URL del Blob después de un delay
          setTimeout(() => {
            URL.revokeObjectURL(blobUrl);
            console.log('🧹 Blob URL limpiado');
          }, 5000);
          
        } else {
          // En escritorio, usar el método estándar de jsPDF
          console.log('💻 Usando método de descarga estándar para escritorio...');
          pdfDoc.save(nombreArchivo);
        }
        
        console.log('✅ PDF descargado exitosamente');
        return true;
        
      } catch (error) {
        console.error('⚠️ Error en descarga de PDF:', error);
        // Intentar método alternativo
        try {
          console.log('🔄 Intentando método de descarga alternativo...');
          const pdfBlob = pdfDoc.output('blob');
          const blobUrl = URL.createObjectURL(pdfBlob);
          window.open(blobUrl, '_blank');
          setTimeout(() => URL.revokeObjectURL(blobUrl), 5000);
          console.log('✅ PDF abierto en nueva ventana');
          return true;
        } catch (altError) {
          console.error('❌ Error en método alternativo:', altError);
          return false;
        }
      }
    },

    // Método auxiliar para cargar imagen como Base64
    async cargarImagenComoBase64(url) {
      return new Promise((resolve, reject) => {
        const img = new Image();
        
        // Configurar CORS
        img.crossOrigin = 'anonymous';
        
        // Timeout
        const timeoutId = setTimeout(() => {
          console.warn(`⏱️ Timeout cargando imagen: ${url}`);
          reject(new Error('Timeout al cargar imagen'));
        }, 15000); // 15 segundos
        
        img.onload = () => {
          clearTimeout(timeoutId);
          
          try {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            // Guardar dimensiones originales
            const originalWidth = img.width;
            const originalHeight = img.height;
            
            // Redimensionar si es muy grande
            const maxSize = 800;
            let width = img.width;
            let height = img.height;
            
            console.log(`📐 Dimensiones originales: ${width}x${height}`);
            
            if (width > maxSize || height > maxSize) {
              if (width > height) {
                height = (height / width) * maxSize;
                width = maxSize;
              } else {
                width = (width / height) * maxSize;
                height = maxSize;
              }
              console.log(`📐 Redimensionado a: ${width}x${height}`);
            }
            
            canvas.width = width;
            canvas.height = height;
            ctx.drawImage(img, 0, 0, width, height);
            
            const dataUrl = canvas.toDataURL('image/png', 0.95);
            console.log(`✅ Imagen convertida a base64 (${(dataUrl.length / 1024).toFixed(2)} KB)`);
            
            resolve({
              data: dataUrl,
              dimensions: {
                width: originalWidth,
                height: originalHeight
              }
            });
          } catch (error) {
            console.error('❌ Error al convertir imagen:', error);
            clearTimeout(timeoutId);
            reject(error);
          }
        };
        
        img.onerror = (error) => {
          clearTimeout(timeoutId);
          console.error(`❌ Error al cargar imagen desde: ${url}`, error);
          reject(new Error(`Error cargando imagen: ${url}`));
        };
        
        console.log(`🔄 Iniciando carga de imagen: ${url}`);
        img.src = url;
      });
    },

    generarCSV() {
      const headers = ['Fecha', 'Hora', 'Tipo', 'Categoría', 'Descripción', 'Usuario', 'CURP', 'Cargo', 'Territorio', 'Correo', 'Supervisor'];
      
      const rows = this.actividades.map(actividad => [
        this.formatearFecha(actividad.fecha_hora),
        this.formatearHora(actividad.fecha_hora),
        this.capitalizar(actividad.tipo_actividad || '-'),
        actividad.categoria_actividad || '-',
        actividad.descripcion || '',
        this.usuarioInfo.nombre,
        this.usuarioInfo.curp || '',
        this.usuarioInfo.cargo || '',
        this.usuarioInfo.territorio || '',
        this.usuarioInfo.correo,
        this.usuarioInfo.supervisor || ''
      ]);

      const csv = [
        headers.join(','),
        ...rows.map(row => row.map(cell => `"${cell}"`).join(',')),
        '',
        '',
        '"NOTA: El reporte fotográfico solo está disponible para el mes en curso; al descargar información de meses anteriores, las fotografías no se mostrarán."'
      ].join('\n');

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);
      
      link.setAttribute('href', url);
      link.setAttribute('download', `Reporte_${this.mesActual}_${this.anioSeleccionado}.csv`);
      link.style.visibility = 'hidden';
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },

    async cargarHistorialReportes() {
      this.cargandoHistorial = true;
      this.errorHistorial = null;
      
      try {
        if (!this.usuarioInfo.id) {
          console.log('⚠️ No hay ID de usuario para cargar historial');
          console.log('📋 Usuario info actual:', JSON.stringify(this.usuarioInfo));
          this.errorHistorial = 'No se pudo identificar al usuario';
          return;
        }

        console.log(`🔍 Cargando historial para usuario ID: ${this.usuarioInfo.id}`);
        // Usar api del apiService que auto-detecta servidor correcto
        const response = await api.get(`/reportes/historial/${this.usuarioInfo.id}`);
        
        console.log('📦 Respuesta del servidor (raw):', JSON.stringify(response.data));
        
        if (response.data.success && response.data.reportes) {
          // Formatear fechas y asegurar que tiene_pdf se preserve
          this.reportesGenerados = response.data.reportes.map(reporte => {
            const reporteFormateado = {
              id: reporte.id,
              nombre: reporte.nombre,
              mes: reporte.mes,
              anio: reporte.anio,
              tipo: reporte.tipo,
              tiene_pdf: reporte.tiene_pdf === true, // Asegurar que sea booleano
              fecha: reporte.fecha ? new Date(reporte.fecha).toLocaleString('es-MX', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
              }) : 'Sin fecha'
            };
            console.log(`   📄 Reporte: ${reporteFormateado.nombre}, tiene_pdf: ${reporteFormateado.tiene_pdf}`);
            return reporteFormateado;
          });
          console.log(`✅ Historial de reportes cargado: ${this.reportesGenerados.length} reportes`);
          
          // Guardar en localStorage como backup
          localStorage.setItem('reportesGenerados', JSON.stringify(this.reportesGenerados));
        } else {
          console.log('⚠️ No se encontraron reportes en la respuesta');
          console.log('   Response success:', response.data.success);
          console.log('   Response reportes:', response.data.reportes);
          this.reportesGenerados = [];
        }
      } catch (error) {
        console.error('❌ Error cargando historial de reportes:', error);
        console.error('   Status:', error.response?.status);
        console.error('   Data:', error.response?.data);
        console.error('   Message:', error.message);
        
        this.errorHistorial = error.response?.data?.detail || error.message || 'Error al cargar historial';
        
        // Si hay error, intentar cargar desde localStorage como fallback
        const reportesGuardados = localStorage.getItem('reportesGenerados');
        if (reportesGuardados) {
          try {
            this.reportesGenerados = JSON.parse(reportesGuardados);
            console.log('📋 Reportes cargados desde localStorage:', this.reportesGenerados.length);
            this.errorHistorial = null; // Limpiar error si cargamos desde cache
          } catch (e) {
            console.error('❌ Error parseando localStorage:', e);
            this.reportesGenerados = [];
          }
        } else {
          this.reportesGenerados = [];
        }
      } finally {
        this.cargandoHistorial = false;
      }
    },

    async descargarReporteHistorial(reporte) {
      // Descargar un reporte previamente generado desde el historial
      // NUEVO FLUJO: Genera el PDF con las firmas disponibles (usuario + supervisor si existe)
      if (this.descargandoReporte) {
        console.log('⚠️ Ya se está descargando un reporte');
        return;
      }

      console.log(`📥 Descargando reporte del historial: ${reporte.nombre}`);
      this.descargandoReporte = reporte.id;

      try {
        // Obtener datos del reporte desde el servidor
        const response = await api.get(`/reportes/descargar/${reporte.id}`);
        
        if (!response.data.success) {
          throw new Error('No se pudo obtener el reporte');
        }
        
        const reporteData = response.data.reporte;
        
        // NUEVO FLUJO: Si hay datos_reporte, generar PDF desde los datos
        if (reporteData.datos_reporte) {
          console.log('📄 Generando PDF desde datos estructurados...');
          
          // Generar PDF con las firmas disponibles
          const pdfBase64 = await this.generarPDFDesdesDatos(
            reporteData.datos_reporte,
            reporteData.firma_usuario_base64,
            reporteData.firmado_supervisor ? reporteData.firma_supervisor_base64 : null,
            reporteData.nombre_supervisor
          );
          
          // Descargar el PDF
          await this.descargarPDFBase64(pdfBase64, reporte.nombre);
          
          console.log('✅ Reporte generado y descargado exitosamente');
          
          this.$notify?.({
            type: 'success',
            message: reporteData.firmado_supervisor 
              ? `${reporte.nombre} descargado (firmado por supervisor)` 
              : `${reporte.nombre} descargado (pendiente de autorización)`
          });
          
        } else if (reporteData.pdf_base64) {
          // COMPATIBILIDAD: Si hay PDF guardado (reportes antiguos)
          console.log('📄 Usando PDF guardado (compatibilidad)...');
          
          let base64Data = limpiarBase64(reporteData.pdf_base64);
          
          if (!base64Data) {
            throw new Error('El PDF tiene formato inválido');
          }
          
          // Si el reporte tiene firma del supervisor, agregarla al PDF
          if (reporteData.firmado_supervisor && reporteData.firma_supervisor_base64) {
            console.log('✍️ Agregando firma del supervisor al PDF...');
            base64Data = await this.agregarFirmaSupervisorPDF(base64Data, reporteData.firma_supervisor_base64);
          }
          
          await this.descargarPDFBase64(base64Data, reporte.nombre);
          
          this.$notify?.({
            type: 'success',
            message: `${reporte.nombre} descargado`
          });
        } else {
          throw new Error('El reporte no tiene datos disponibles para generar el PDF');
        }
        
      } catch (error) {
        console.error('❌ Error descargando reporte:', error);
        
        let mensaje = 'Error al descargar el reporte';
        if (error.response?.status === 404) {
          mensaje = 'El reporte no está disponible';
        }
        
        this.$notify?.({
          type: 'error',
          message: mensaje
        });
      } finally {
        this.descargandoReporte = null;
      }
    },
    
    /**
     * Descarga un PDF desde base64
     */
    async descargarPDFBase64(base64Data, nombreReporte) {
      const byteCharacters = atob(base64Data);
      const byteNumbers = new Array(byteCharacters.length);
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      const blob = new Blob([byteArray], { type: 'application/pdf' });
      
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${nombreReporte.replace(/\s+/g, '_')}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    },
    
    /**
     * Genera un PDF desde los datos estructurados del reporte
     * @param {Object} datos - Datos estructurados del reporte
     * @param {string} firmaUsuario - Firma del usuario en base64
     * @param {string} firmaSupervisor - Firma del supervisor en base64 (opcional)
     * @param {string} nombreSupervisor - Nombre del supervisor que firmó
     * @returns {string} - PDF en base64 (sin prefijo data:)
     */
    async generarPDFDesdesDatos(datos, firmaUsuario, firmaSupervisor, nombreSupervisor) {
      console.log('📄 Generando PDF desde datos estructurados...');
      console.log('   - Actividades:', datos.actividades?.length || 0);
      console.log('   - Firma usuario:', firmaUsuario ? 'Sí' : 'No');
      console.log('   - Firma supervisor:', firmaSupervisor ? 'Sí' : 'No');
      
      const doc = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4'
      });

      const pageHeight = doc.internal.pageSize.getHeight();
      const pageWidth = doc.internal.pageSize.getWidth();
      const margin = 15;
      const contentWidth = pageWidth - (margin * 2);
      let currentY = 10;

      // ========== ENCABEZADO CON IMAGEN DE LOGOS ==========
      let superiorImageBase64 = null;
      let imgDimensions = null;
      
      try {
        const result = await this.cargarImagenComoBase64(superiorImage);
        superiorImageBase64 = result.data;
        imgDimensions = result.dimensions;
      } catch (error) {
        console.warn('⚠️ No se pudo cargar imagen de encabezado');
      }
      
      if (superiorImageBase64 && imgDimensions) {
        const realAspectRatio = imgDimensions.height / imgDimensions.width;
        const imgWidth = contentWidth * 0.95;
        const imgHeight = imgWidth * realAspectRatio;
        const imgX = margin + (contentWidth - imgWidth) / 2;
        doc.addImage(superiorImageBase64, 'PNG', imgX, currentY, imgWidth, imgHeight);
        currentY += imgHeight + 5;
      }
    
      // Recuadro principal con títulos
      doc.setDrawColor(0, 0, 0);
      doc.setLineWidth(0.5);
      doc.rect(margin, currentY, contentWidth, 25);
      
      doc.setFontSize(9);
      doc.setFont(undefined, 'bold');
      doc.setTextColor(0, 0, 0);
      doc.text('SECRETARÍA DE BIENESTAR', pageWidth / 2, currentY + 6, { align: 'center' });
      doc.text('SUBSECRETARÍA DE INCLUSIÓN PRODUCTIVA Y DESARROLLO RURAL', pageWidth / 2, currentY + 11, { align: 'center' });
      doc.text('FORMATO DE SEGUIMIENTO A ACTIVIDADES PROGRAMADAS', pageWidth / 2, currentY + 16, { align: 'center' });
      
      // Fecha en la esquina
      const fechaActual = new Date(datos.fechaGeneracion || new Date()).toLocaleDateString('es-MX', {
        day: '2-digit', month: '2-digit', year: 'numeric'
      });
      doc.setFontSize(8);
      doc.setFont(undefined, 'normal');
      doc.text('Fecha:', pageWidth - margin - 35, currentY + 21);
      doc.rect(pageWidth - margin - 25, currentY + 18, 25, 5);
      doc.text(fechaActual, pageWidth - margin - 12.5, currentY + 21.5, { align: 'center' });
      
      currentY += 30;
      
      // ========== TABLA DE INFORMACIÓN DEL PRESTADOR ==========
      const usuario = datos.usuario || {};
      const periodo = datos.periodo || {};
      const col1Width = contentWidth * 0.5;
      const col2Width = contentWidth * 0.5;
      
      // Fila 1: Nombre
      doc.setDrawColor(0, 0, 0);
      doc.setLineWidth(0.3);
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      doc.setFontSize(8);
      doc.setFont(undefined, 'bold');
      doc.text('Nombre del prestador de Servicios', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      doc.text(usuario.nombre || 'Sin nombre', margin + col1Width + 2, currentY + 4);
      currentY += 6;
      
      // Fila 2: CURP
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      doc.setFont(undefined, 'bold');
      doc.text('CURP', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      doc.text(usuario.curp || 'No registrado', margin + col1Width + 2, currentY + 4);
      currentY += 6;
      
      // Fila 3: Periodo
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      doc.setFont(undefined, 'bold');
      doc.text('Periodo', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      const mesNombre = periodo.mesNombre || 'N/A';
      const anio = periodo.anio || 'N/A';
      doc.text(`${mesNombre} ${anio}`, margin + col1Width + 2, currentY + 4);
      currentY += 8;
      
      // Fila 4: Programa
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      doc.setFont(undefined, 'bold');
      doc.text('Programa Social del Apoyo', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      doc.text('SEMBRANDO VIDA', margin + col1Width + 2, currentY + 4);
      currentY += 8;
      
      // Fila 5: Territorio
      doc.rect(margin, currentY, col1Width, 6);
      doc.rect(margin + col1Width, currentY, col2Width, 6);
      doc.setFont(undefined, 'bold');
      doc.text('Territorio y entidad donde presta sus servicios', margin + 2, currentY + 4);
      doc.setFont(undefined, 'normal');
      doc.text(usuario.territorio || 'No asignado', margin + col1Width + 2, currentY + 4);
      currentY += 10;
      
      // ========== TABLA DE ACTIVIDADES ==========
      const actividades = datos.actividades || [];
      const tableWidth = contentWidth;
      const tableX = margin;
      const colWidths = [15, 32, 18, 22, 83];
      
      // Header
      doc.setFillColor(255, 255, 255);
      doc.rect(tableX, currentY, tableWidth, 8, 'FD');
      doc.setFontSize(8);
      doc.setFont(undefined, 'bold');
      
      let colX = tableX + 2;
      doc.text('No.', colX + colWidths[0]/2, currentY + 5.5, { align: 'center' });
      doc.line(colX + colWidths[0], currentY, colX + colWidths[0], currentY + 8);
      colX += colWidths[0];
      doc.text('Fecha', colX + colWidths[1]/2, currentY + 5.5, { align: 'center' });
      doc.line(colX + colWidths[1], currentY, colX + colWidths[1], currentY + 8);
      colX += colWidths[1];
      doc.text('Tipo', colX + colWidths[2]/2, currentY + 5.5, { align: 'center' });
      doc.line(colX + colWidths[2], currentY, colX + colWidths[2], currentY + 8);
      colX += colWidths[2];
      doc.text('Hora', colX + colWidths[3]/2, currentY + 5.5, { align: 'center' });
      doc.line(colX + colWidths[3], currentY, colX + colWidths[3], currentY + 8);
      colX += colWidths[3];
      doc.text('Actividad desarrollada', colX + colWidths[4]/2, currentY + 5.5, { align: 'center' });
      currentY += 8;
      
      // Filas de datos
      doc.setFontSize(7);
      doc.setFont(undefined, 'normal');
      const baseRowHeight = 8;
      const lineHeight = 3;

      actividades.forEach((actividad, index) => {
        const activDesc = actividad.descripcion || actividad.categoria_actividad || 'Actividad de campo';
        const maxTextWidth = colWidths[4] - 4;
        const textLines = doc.splitTextToSize(activDesc, maxTextWidth);
        const rowHeight = Math.max(baseRowHeight, textLines.length * lineHeight + 3);
        
        if (currentY > pageHeight - 50) {
          doc.addPage();
          currentY = 20;
        }

        doc.rect(tableX, currentY, tableWidth, rowHeight, 'S');

        const fecha = actividad.fecha_hora ? new Date(actividad.fecha_hora).toLocaleDateString('es-MX', { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' }) : '-';
        const hora = actividad.fecha_hora ? new Date(actividad.fecha_hora).toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit', hour12: false }) : '-';
        const tipo = (actividad.tipo_actividad || 'Campo').charAt(0).toUpperCase() + (actividad.tipo_actividad || 'campo').slice(1);

        colX = tableX + 2;
        const textYCenter = currentY + (rowHeight / 2) + 1.5;
        
        doc.text(String(index + 1), colX + colWidths[0]/2, textYCenter, { align: 'center' });
        doc.line(colX + colWidths[0], currentY, colX + colWidths[0], currentY + rowHeight);
        
        colX += colWidths[0];
        doc.text(fecha, colX + 2, textYCenter);
        doc.line(colX + colWidths[1], currentY, colX + colWidths[1], currentY + rowHeight);
        
        colX += colWidths[1];
        doc.text(tipo, colX + colWidths[2]/2, textYCenter, { align: 'center' });
        doc.line(colX + colWidths[2], currentY, colX + colWidths[2], currentY + rowHeight);
        
        colX += colWidths[2];
        doc.text(hora, colX + colWidths[3]/2, textYCenter, { align: 'center' });
        doc.line(colX + colWidths[3], currentY, colX + colWidths[3], currentY + rowHeight);
        
        colX += colWidths[3];
        textLines.forEach((line, lineIndex) => {
          doc.text(line, colX + 2, currentY + 4 + (lineIndex * lineHeight));
        });

        currentY += rowHeight;
      });

      currentY += 15;

      // ========== SECCIÓN DE FIRMAS ==========
      if (currentY > pageHeight - 70) {
        doc.addPage();
        currentY = 30;
      }

      const firmaWidth = 70;
      const firmaHeight = 30;
      const firmaUsuarioX = margin + 5;
      const firmaResponsableX = pageWidth - margin - firmaWidth - 5;
      const firmaY = currentY;
      
      // Etiquetas
      doc.setFillColor(255, 218, 185);
      doc.setLineWidth(0.3);
      
      doc.rect(firmaUsuarioX, firmaY - 8, firmaWidth, 7, 'FD');
      doc.setFontSize(9);
      doc.setFont(undefined, 'bold');
      doc.text('Elaboró', firmaUsuarioX + firmaWidth / 2, firmaY - 3.5, { align: 'center' });
      
      doc.setFillColor(255, 218, 185);
      doc.rect(firmaResponsableX, firmaY - 8, firmaWidth, 7, 'FD');
      doc.text('Autorizó', firmaResponsableX + firmaWidth / 2, firmaY - 3.5, { align: 'center' });
      
      // FIRMA DEL USUARIO (Izquierda)
      if (firmaUsuario) {
        try {
          doc.addImage(firmaUsuario, 'PNG', firmaUsuarioX, firmaY, firmaWidth, firmaHeight);
        } catch (e) {
          console.warn('No se pudo agregar firma del usuario');
        }
      }
      
      doc.setLineWidth(0.5);
      doc.line(firmaUsuarioX, firmaY + firmaHeight + 5, firmaUsuarioX + firmaWidth, firmaY + firmaHeight + 5);
      
      doc.setFontSize(8);
      doc.setFont(undefined, 'normal');
      doc.text(usuario.cargo || 'Facilitador Comunitario', firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' });
      doc.setFont(undefined, 'bold');
      doc.text(usuario.nombre || 'Sin nombre', firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 17, { align: 'center' });
      
      // FIRMA DEL SUPERVISOR (Derecha) - Solo si existe
      if (firmaSupervisor) {
        try {
          doc.addImage(firmaSupervisor, 'PNG', firmaResponsableX, firmaY, firmaWidth, firmaHeight);
          console.log('✅ Firma del supervisor agregada al PDF');
        } catch (e) {
          console.warn('No se pudo agregar firma del supervisor');
        }
      }
      
      doc.setLineWidth(0.5);
      doc.line(firmaResponsableX, firmaY + firmaHeight + 5, firmaResponsableX + firmaWidth, firmaY + firmaHeight + 5);
      
      doc.setFontSize(7.5);
      doc.setFont(undefined, 'normal');
      doc.text('Encargada de Despacho de la Coordinación', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' });
      doc.text('Territorial ' + (usuario.territorio || ''), firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 16, { align: 'center' });
      
      doc.setFontSize(8);
      doc.setFont(undefined, 'bold');
      doc.text(nombreSupervisor || usuario.supervisor || 'Sin asignar', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 22, { align: 'center' });

      // ========== PIE DE PÁGINA ==========
      const totalPages = doc.internal.getNumberOfPages();
      for (let i = 1; i <= totalPages; i++) {
        doc.setPage(i);
        doc.setTextColor(128, 0, 32);
        doc.setFontSize(7);
        doc.setFont(undefined, 'normal');
        const footerText = 'Paseo de la Reforma # 116, Piso 16, Col. Juárez, Alc. Cuauhtémoc, CDMX C.P. 06600 Tel.: (55) 5328 5000 www.gob.mx/bienestar';
        doc.text(footerText, pageWidth / 2, pageHeight - 10, { align: 'center' });
      }

      // Obtener PDF como base64 (sin prefijo data:)
      const pdfOutput = doc.output('datauristring');
      const base64 = pdfOutput.split(',')[1];
      
      console.log('✅ PDF generado desde datos estructurados');
      return base64;
    },
    
    /**
     * Agrega la firma del supervisor a un PDF existente
     * @param {string} pdfBase64 - El PDF original en base64
     * @param {string} firmaBase64 - La firma del supervisor en base64
     * @returns {string} - El PDF modificado en base64
     */
    async agregarFirmaSupervisorPDF(pdfBase64, firmaBase64) {
      try {
        // Convertir base64 del PDF a bytes
        const pdfBytes = Uint8Array.from(atob(pdfBase64), c => c.charCodeAt(0));
        
        // Cargar el PDF existente
        const pdfDoc = await PDFDocument.load(pdfBytes);
        
        // Obtener la primera página (donde están las firmas)
        const pages = pdfDoc.getPages();
        const firstPage = pages[0];
        const { width, height } = firstPage.getSize();
        
        // Preparar la imagen de la firma
        let firmaClean = firmaBase64;
        if (firmaClean.includes(',')) {
          firmaClean = firmaClean.split(',')[1];
        }
        
        // Convertir la firma base64 a bytes
        const firmaBytes = Uint8Array.from(atob(firmaClean), c => c.charCodeAt(0));
        
        // Intentar como PNG primero
        let firmaImage;
        try {
          firmaImage = await pdfDoc.embedPng(firmaBytes);
        } catch (e) {
          // Si falla, intentar como JPEG
          try {
            firmaImage = await pdfDoc.embedJpg(firmaBytes);
          } catch (e2) {
            console.warn('⚠️ No se pudo insertar la imagen de firma:', e2);
            // Retornar el PDF original sin modificar
            return pdfBase64;
          }
        }
        
        // Calcular posición de la firma del supervisor (sección "Autorizó" - lado derecho)
        // Estos valores corresponden a la posición en el PDF generado por jsPDF
        // El PDF usa tamaño carta (215.9 x 279.4 mm)
        const pageWidth = width; // ~612 puntos para carta
        const margin = 15 * 2.83465; // 15mm en puntos
        const firmaWidth = 65 * 2.83465; // 65mm en puntos
        const firmaHeight = 20 * 2.83465; // 20mm en puntos
        
        // Posición X: lado derecho (después del centro)
        const firmaX = pageWidth - margin - firmaWidth;
        // Posición Y: desde abajo (las firmas están cerca del final de la primera página)
        // Ajustamos basándonos en el layout típico del reporte
        const firmaY = 50; // Cerca del fondo de la página
        
        // Dibujar la firma del supervisor
        firstPage.drawImage(firmaImage, {
          x: firmaX,
          y: firmaY,
          width: firmaWidth,
          height: firmaHeight,
        });
        
        console.log('✅ Firma del supervisor agregada al PDF');
        
        // Guardar el PDF modificado
        const modifiedPdfBytes = await pdfDoc.save();
        
        // Convertir a base64
        const modifiedBase64 = btoa(
          modifiedPdfBytes.reduce((data, byte) => data + String.fromCharCode(byte), '')
        );
        
        return modifiedBase64;
        
      } catch (error) {
        console.error('❌ Error agregando firma al PDF:', error);
        // En caso de error, retornar el PDF original
        return pdfBase64;
      }
    },

    async verReporteHistorial(reporte) {
      // Ver un reporte previamente generado - genera PDF y lo abre
      // NUEVO FLUJO: Genera PDF desde datos estructurados con las firmas disponibles
      if (this.viendoReporte) {
        console.log('⚠️ Ya se está cargando un reporte');
        return;
      }

      console.log(`👁️ Visualizando reporte del historial: ${reporte.nombre}`);
      this.viendoReporte = reporte.id;

      try {
        // Obtener datos del reporte desde el servidor
        const response = await api.get(`/reportes/descargar/${reporte.id}`);
        
        if (!response.data.success) {
          throw new Error('No se pudo obtener el reporte');
        }
        
        const reporteData = response.data.reporte;
        let base64Data = null;
        
        // NUEVO FLUJO: Si hay datos_reporte, generar PDF desde los datos
        if (reporteData.datos_reporte) {
          console.log('📄 Generando PDF desde datos estructurados...');
          
          base64Data = await this.generarPDFDesdesDatos(
            reporteData.datos_reporte,
            reporteData.firma_usuario_base64,
            reporteData.firmado_supervisor ? reporteData.firma_supervisor_base64 : null,
            reporteData.nombre_supervisor
          );
          
        } else if (reporteData.pdf_base64) {
          // COMPATIBILIDAD: Si hay PDF guardado (reportes antiguos)
          console.log('📄 Usando PDF guardado (compatibilidad)...');
          
          base64Data = limpiarBase64(reporteData.pdf_base64);
          
          if (reporteData.firmado_supervisor && reporteData.firma_supervisor_base64) {
            console.log('✍️ Agregando firma del supervisor al PDF...');
            base64Data = await this.agregarFirmaSupervisorPDF(base64Data, reporteData.firma_supervisor_base64);
          }
        } else {
          throw new Error('El reporte no tiene datos para generar el PDF');
        }
        
        if (!base64Data) {
          throw new Error('Error generando el PDF');
        }
        
        // Convertir base64 a blob
        const byteCharacters = atob(base64Data);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: 'application/pdf' });
        
        const nombreArchivo = `${reporte.nombre.replace(/\s+/g, '_')}.pdf`;
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        
        if (isMobile) {
          const url = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.download = nombreArchivo;
          link.target = '_blank';
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          
          setTimeout(() => window.URL.revokeObjectURL(url), 2000);
          
          this.$notify?.({
            type: 'success',
            message: reporteData.firmado_supervisor 
              ? 'PDF generado con firma de supervisor' 
              : 'PDF generado (pendiente de autorización)'
          });
        } else {
          const url = window.URL.createObjectURL(blob);
          window.open(url, '_blank');
          setTimeout(() => window.URL.revokeObjectURL(url), 1000);
        }
        
      } catch (error) {
        console.error('❌ Error visualizando reporte:', error);
        
        this.$notify?.({
          type: 'error',
          message: 'Error al abrir el reporte'
        });
      } finally {
        this.viendoReporte = null;
      }
    },

    async eliminarReporteHistorial(reporte) {
      // Mostrar modal de confirmación
      this.reporteAEliminar = reporte;
      this.mostrarModalEliminar = true;
    },

    cancelarEliminar() {
      this.mostrarModalEliminar = false;
      this.reporteAEliminar = null;
    },

    async confirmarEliminarReporte() {
      const reporte = this.reporteAEliminar;
      this.mostrarModalEliminar = false;

      if (!reporte || this.eliminandoReporte) {
        return;
      }

      this.eliminandoReporte = reporte.id;
      console.log(`🗑️ Eliminando reporte: ${reporte.nombre} (mes: ${reporte.mes}, año: ${reporte.anio})`);

      try {
        const response = await api.delete(`/reportes/eliminar/${reporte.id}`);
        
        if (response.data.success) {
          console.log('✅ Reporte eliminado correctamente');
          
          // Eliminar del array local INMEDIATAMENTE
          const index = this.reportesGenerados.findIndex(r => r.id === reporte.id);
          if (index !== -1) {
            this.reportesGenerados.splice(index, 1);
          }
          
          // Actualizar localStorage
          localStorage.setItem('reportesGenerados', JSON.stringify(this.reportesGenerados));
          
          // REACTIVO: Verificar si el reporte eliminado era del mes/año actualmente seleccionado
          // Convertir a string para comparación segura (el mes viene como string, el año puede ser number)
          const mesReporte = String(reporte.mes);
          const anioReporte = Number(reporte.anio);
          const mesActualStr = String(this.mesActual);
          const anioActualNum = Number(this.anioSeleccionado);
          
          console.log(`📊 Comparando: Reporte(${mesReporte}/${anioReporte}) vs Actual(${mesActualStr}/${anioActualNum})`);
          
          if (mesReporte === mesActualStr && anioReporte === anioActualNum) {
            // Limpiar INMEDIATAMENTE el estado de reporte existente
            // Esto habilitará el botón de generar reporte al instante
            this.reporteExistente = null;
            console.log('🔓 Botón de generar reporte habilitado - El reporte del mes actual fue eliminado');
          }
          
          this.$notify?.({
            type: 'success',
            message: 'Reporte eliminado - Ya puedes generar uno nuevo para este mes'
          });
        } else {
          throw new Error('Error al eliminar el reporte');
        }
        
      } catch (error) {
        console.error('❌ Error eliminando reporte:', error);
        
        let mensaje = 'Error al eliminar el reporte';
        if (error.response?.status === 404) {
          mensaje = 'El reporte no fue encontrado';
        }
        
        this.$notify?.({
          type: 'error',
          message: mensaje
        });
      } finally {
        this.eliminandoReporte = null;
        this.reporteAEliminar = null;
      }
    }
  },

  async mounted() {
    console.log('🚀 Reportes.vue montado');
    
    // Generar años disponibles (años pasados y futuros)
    const currentYear = new Date().getFullYear();
    this.anos = Array.from({ length: 5 }, (_, i) => currentYear - 2 + i);

    // Cargar información del usuario
    const usuario = JSON.parse(localStorage.getItem('user'));
    console.log('👤 Usuario desde localStorage:', usuario ? `ID: ${usuario.id}` : 'No encontrado');
    
    if (usuario) {
      this.usuarioInfo = {
        id: usuario.id || null,
        nombre: usuario.nombre_completo || usuario.nombre || 'Usuario',
        cargo: usuario.cargo || '',
        correo: usuario.correo || '',
        territorio: usuario.territorio || 'No asignado',
        curp: usuario.curp || 'No registrada',
        supervisor: usuario.supervisor || 'No asignado'
      };
      
      console.log('✅ Usuario info establecido:', JSON.stringify(this.usuarioInfo));
      
      // Si es técnico, obtener supervisor automático basado en territorio
      const cargoUpper = (usuario.cargo || '').toUpperCase();
      if (cargoUpper === 'TECNICO SOCIAL' || cargoUpper === 'TECNICO PRODUCTIVO') {
        try {
          console.log('🔍 Buscando supervisor automático para técnico...');
          const respuesta = await apiService.obtenerSupervisorAutomatico(usuario.id);
          if (respuesta.success && respuesta.supervisor) {
            this.usuarioInfo.supervisor = respuesta.supervisor;
            
            // Actualizar también el localStorage para que Profile.vue lo muestre
            usuario.supervisor = respuesta.supervisor;
            localStorage.setItem('user', JSON.stringify(usuario));
            
            console.log(`✅ Supervisor automático asignado y guardado: ${respuesta.supervisor}`);
          } else {
            console.log(`ℹ️ No se encontró supervisor automático: ${respuesta.mensaje}`);
          }
        } catch (error) {
          console.error('❌ Error obteniendo supervisor automático:', error);
          // Mantener el supervisor actual si hay error
        }
      }
      
      // Cargar actividades (apiService auto-detecta servidor correcto)
      try {
        await this.cargarActividades();
      } catch (error) {
        console.error('❌ Error cargando actividades:', error);
      }

      // Cargar historial de reportes desde la base de datos
      try {
        await this.cargarHistorialReportes();
      } catch (error) {
        console.error('❌ Error cargando historial:', error);
      }
      
      // Verificar si ya existe un reporte para el mes/año actual
      try {
        await this.verificarReporteExistente();
      } catch (error) {
        console.error('❌ Error verificando reporte existente:', error);
      }
    } else {
      console.warn('⚠️ No hay usuario en localStorage');
    }
  }
};
</script>

<style scoped>
/* Estilos glass-card */
.glass-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 1rem;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
}

.modern-title {
  position: relative;
  overflow: hidden;
  color: #0F172A;
}

.red-line {
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #3B82F6, #2563EB);
  border-radius: 2px;
}

/* Animación para elementos decorativos */
@keyframes pulse-slow {
  0%, 100% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.2;
  }
}

.animate-pulse-slow {
  animation: pulse-slow 4s ease-in-out infinite;
}

/* Animación de aparición */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Animación rápida para modal de eliminar */
@keyframes modalIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-in;
}

/* Modal animations */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

@keyframes modal-enter {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.animate-modal-enter {
  animation: modal-enter 0.3s ease-out forwards;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .page-container {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}
</style>
