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
          @click.self="cerrarModalFirma"
        >
          <!-- Overlay -->
          <div class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>
          
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
                class="flex-1 px-4 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-xl hover:bg-gray-50 transition-colors order-2 sm:order-1"
              >
                Cancelar
              </button>
              <button
                @click="confirmarYDescargar"
                :disabled="!confirmarFirma"
                class="flex-1 px-4 py-2.5 text-sm font-medium text-white rounded-xl transition-all order-1 sm:order-2 flex items-center justify-center gap-2"
                :class="confirmarFirma 
                  ? 'bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 shadow-lg' 
                  : 'bg-gray-300 cursor-not-allowed'"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                </svg>
                Firmar y Descargar
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

            <!-- Loading -->
            <div v-if="cargando" class="flex justify-center items-center py-8">
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

            <!-- Botón de Descarga -->
            <button
              @click="iniciarDescarga"
              :disabled="cargando || generandoReporte || actividades.length === 0"
              class="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed text-white font-bold py-2 px-3 rounded-lg transition-all duration-200 flex items-center justify-center gap-2 text-xs sm:text-sm"
            >
              <svg v-if="!generandoReporte" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
              </svg>
              <svg v-else class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span class="truncate">{{ generandoReporte ? 'Generando...' : 'Descargar Reporte' }}</span>
            </button>
          </div>

          <!-- Historial de Reportes -->
          <div class="glass-card">
            <div class="flex items-center mb-3">
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
            <div v-if="reportesGenerados.length > 0" class="space-y-2">
              <div
                v-for="reporte in reportesGenerados"
                :key="reporte.id"
                class="flex items-center justify-between p-2.5 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-xs"
              >
                <div class="flex items-center gap-2 min-w-0">
                  <div class="flex-shrink-0 w-7 h-7 bg-orange-100 rounded flex items-center justify-center">
                    <i class="fas fa-file text-orange-600 text-xs"></i>
                  </div>
                  <div class="min-w-0">
                    <p class="font-medium text-gray-900 text-xs truncate">{{ reporte.nombre }}</p>
                    <p class="text-xs text-gray-500 truncate">{{ reporte.fecha }}</p>
                  </div>
                </div>
                <span :class="[
                  'inline-flex items-center px-2 py-0.5 rounded text-xs font-medium flex-shrink-0',
                  reporte.tipo === 'PDF' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                ]">
                  {{ reporte.tipo }}
                </span>
              </div>
            </div>
            <div v-else class="text-center py-4">
              <p class="text-xs text-gray-500">Sin reportes generados</p>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { jsPDF } from 'jspdf';
import html2canvas from 'html2canvas';
import FirmaDigital from '../components/FirmaDigital.vue';
import axios from 'axios';
import { API_URL } from '../utils/network.js';
import superiorImage from '../../images/superior.png';

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
      confirmarFirma: false
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
      try {
        this.cargando = true;
        const usuario = JSON.parse(localStorage.getItem('user'));
        
        if (!usuario || !usuario.id) {
          console.error('❌ No hay usuario en localStorage');
          throw new Error('Usuario no autenticado');
        }
        
        console.log(`📋 Cargando TODAS las actividades para usuario ${usuario.id}`);
        
        // Usar el endpoint /registros igual que en Historial.vue
        const response = await axios.get(`${API_URL}/registros?usuario_id=${usuario.id}`, {
          timeout: 10000,
          headers: {
            'Content-Type': 'application/json'
          }
        });

        console.log('✅ Respuesta del servidor:', response.data);

        if (!response.data || !response.data.registros) {
          throw new Error('No se recibió respuesta del servidor');
        }

        // Guardar TODAS las actividades sin filtrar
        this.todasLasActividades = response.data.registros || [];
        
        // Filtrar por mes/año seleccionado
        this.filtrarActividadesPorPeriodo();
        
        console.log(`✅ Total de actividades: ${this.todasLasActividades.length}`);
        console.log(`✅ Actividades en período seleccionado: ${this.actividades.length}`);
        
      } catch (error) {
        console.error('❌ Error cargando actividades:', error);
        this.actividades = [];
        this.todasLasActividades = [];
        if (error.response) {
          alert(`Error del servidor: ${error.response.data.detail || error.response.statusText}`);
        } else if (error.request) {
          alert('No se pudo conectar con el servidor');
        } else {
          alert(`Error: ${error.message}`);
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
      
      console.log(`🔍 Filtrado: ${this.actividades.length} actividades entre ${inicioDeMes.toLocaleDateString()} y ${finDelMes.toLocaleDateString()}`);
    },

    cambiarPeriodo() {
      // Solo filtrar si ya tenemos actividades cargadas
      if (this.todasLasActividades && this.todasLasActividades.length > 0) {
        this.filtrarActividadesPorPeriodo();
      } else {
        this.cargarActividades();
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

    capitalizar(texto) {
      return texto.charAt(0).toUpperCase() + texto.slice(1);
    },

    calcularHoraTermino(fechaHora) {
      if (!fechaHora) return '-';
      const date = new Date(fechaHora);
      date.setHours(date.getHours() + 1); // Suma 1 hora
      return date.toLocaleTimeString('es-MX', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      });
    },

    // Verificar si hay firma válida (método en lugar de computed para reactividad con refs)
    esFirmaValida() {
      return this.$refs.firmaComponent?.hayFirma || false;
    },

    // Iniciar proceso de descarga - verificar firma primero
    iniciarDescarga() {
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

      // Mostrar modal de confirmación
      this.confirmarFirma = false;
      this.mostrarModalFirma = true;
    },

    // Cerrar modal
    cerrarModalFirma() {
      this.mostrarModalFirma = false;
      this.confirmarFirma = false;
    },

    // Confirmar y proceder con la descarga
    async confirmarYDescargar() {
      if (!this.confirmarFirma) return;
      
      // Esperar un tick para asegurar que el estado de la firma esté actualizado
      await this.$nextTick();
      
      // Verificar firma de manera más robusta
      const firmaValida = this.$refs.firmaComponent?.hayFirma || false;
      if (!firmaValida) {
        alert('La firma no es válida. Por favor, vuelve a firmar.');
        return;
      }
      
      this.cerrarModalFirma();
      
      // Pequeña pausa para asegurar que todo esté listo
      setTimeout(async () => {
        await this.generarReporte();
      }, 100);
    },

    async generarReporte() {
      try {
        if (this.actividades.length === 0) {
          alert('No hay actividades para generar el reporte');
          return;
        }

        this.generandoReporte = true;

        if (this.formatoSeleccionado === 'pdf') {
          await this.generarPDF();
        } else {
          this.generarCSV();
        }

        // Agregar a historial
        const fecha = new Date().toLocaleString('es-MX');
        this.reportesGenerados.unshift({
          id: Date.now(),
          nombre: `Reporte ${this.mesActual} ${this.anioSeleccionado}`,
          fecha,
          tipo: this.formatoSeleccionado.toUpperCase()
        });

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
      // Cargar imagen y obtener dimensiones reales para mantener proporción
      const img = new Image();
      img.src = superiorImage;
      
      // Calcular dimensiones manteniendo aspect ratio
      const imgOriginalWidth = img.naturalWidth || img.width;
      const imgOriginalHeight = img.naturalHeight || img.height;
      const aspectRatio = imgOriginalHeight / imgOriginalWidth;
      
      // Establecer ancho al contenido y calcular altura proporcionalmente
      const imgWidth = contentWidth;
      const imgHeight = imgWidth * aspectRatio;
      
      doc.addImage(superiorImage, 'PNG', margin, currentY, imgWidth, imgHeight);
      
      currentY += imgHeight + 5;
      
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
      const colWidths = [15, 32, 18, 22, 22, 61]; // No., Fecha, Tipo, Inicio, Término, Actividad
      
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
      doc.text('Hora Inicio', colX + colWidths[3]/2, currentY + 5.5, { align: 'center' });
      doc.line(colX + colWidths[3], currentY, colX + colWidths[3], currentY + 8);
      
      colX += colWidths[3];
      doc.text('Hora Término', colX + colWidths[4]/2, currentY + 5.5, { align: 'center' });
      doc.line(colX + colWidths[4], currentY, colX + colWidths[4], currentY + 8);
      
      colX += colWidths[4];
      doc.text('Actividad desarrollada', colX + colWidths[5]/2, currentY + 5.5, { align: 'center' });

      currentY += 8;
      
      // Filas de datos
      doc.setTextColor(0, 0, 0);
      doc.setFontSize(7);
      doc.setFont(undefined, 'normal');
      
      const rowHeight = 8;

      this.actividades.forEach((actividad, index) => {
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
          doc.text('Hora Inicio', headerX + colWidths[3]/2, currentY + 5.5, { align: 'center' });
          doc.line(headerX + colWidths[3], currentY, headerX + colWidths[3], currentY + 8);
          
          headerX += colWidths[3];
          doc.text('Hora Término', headerX + colWidths[4]/2, currentY + 5.5, { align: 'center' });
          doc.line(headerX + colWidths[4], currentY, headerX + colWidths[4], currentY + 8);
          
          headerX += colWidths[4];
          doc.text('Actividad desarrollada', headerX + colWidths[5]/2, currentY + 5.5, { align: 'center' });
          
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
        const activDesc = (actividad.descripcion || actividad.categoria_actividad || 'Actividad de ' + (actividad.tipo_actividad || 'campo')).substring(0, 50);

        colX = tableX + 2;
        
        // No.
        doc.text(String(index + 1), colX + colWidths[0]/2, currentY + 5.5, { align: 'center' });
        doc.line(colX + colWidths[0], currentY, colX + colWidths[0], currentY + rowHeight);
        
        // Fecha
        colX += colWidths[0];
        doc.text(fecha, colX + 2, currentY + 5.5);
        doc.line(colX + colWidths[1], currentY, colX + colWidths[1], currentY + rowHeight);
        
        // Tipo (Campo/Gabinete)
        colX += colWidths[1];
        doc.text(tipo, colX + colWidths[2]/2, currentY + 5.5, { align: 'center' });
        doc.line(colX + colWidths[2], currentY, colX + colWidths[2], currentY + rowHeight);
        
        // Hora Inicio
        colX += colWidths[2];
        doc.text(hora, colX + colWidths[3]/2, currentY + 5.5, { align: 'center' });
        doc.line(colX + colWidths[3], currentY, colX + colWidths[3], currentY + rowHeight);
        
        // Hora Término (estimado +1 hora)
        colX += colWidths[3];
        const horaTermino = this.calcularHoraTermino(actividad.fecha_hora);
        doc.text(horaTermino, colX + colWidths[4]/2, currentY + 5.5, { align: 'center' });
        doc.line(colX + colWidths[4], currentY, colX + colWidths[4], currentY + rowHeight);
        
        // Actividad
        colX += colWidths[4];
        doc.text(activDesc, colX + 2, currentY + 5.5);

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

      // Descargar
      doc.save(`Reporte_${this.mesActual}_${this.anioSeleccionado}.pdf`);
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
        ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
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
    }
  },

  mounted() {
    // Generar años disponibles (años pasados y futuros)
    const currentYear = new Date().getFullYear();
    this.anos = Array.from({ length: 5 }, (_, i) => currentYear - 2 + i);

    // Cargar información del usuario
    const usuario = JSON.parse(localStorage.getItem('user'));
    if (usuario) {
      this.usuarioInfo = {
        nombre: usuario.nombre_completo || usuario.nombre || 'Usuario',
        cargo: usuario.cargo || '',
        correo: usuario.correo || '',
        territorio: usuario.territorio || 'No asignado',
        curp: usuario.curp || 'No registrada',
        supervisor: usuario.supervisor || 'No asignado'
      };
    }

    // Cargar actividades
    this.cargarActividades();

    // Cargar reportes del localStorage si existen
    const reportesGuardados = localStorage.getItem('reportesGenerados');
    if (reportesGuardados) {
      this.reportesGenerados = JSON.parse(reportesGuardados);
    }
  },

  beforeUnmount() {
    // Guardar reportes generados
    localStorage.setItem('reportesGenerados', JSON.stringify(this.reportesGenerados));
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
