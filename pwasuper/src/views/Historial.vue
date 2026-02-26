<template>
  <div class="fixed inset-0 bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 overflow-hidden">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-emerald-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-teal-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>
    
    <div class="absolute inset-0 overflow-y-auto pt-16 sm:pt-20 pb-4">
      <div class="page-container relative z-10 px-2 sm:px-3 md:px-4 lg:px-6 xl:px-8 py-3 sm:py-4 lg:py-5 min-h-full max-w-full">
    <!-- Tabs para alternar entre registros normales y asistencias -->
    <div class="apple-header-section">
      <!-- Segmented Control estilo Apple -->
      <div class="apple-segmented-control">
        <div 
          class="apple-segment-bg" 
          :class="[
            tabActiva === 'asistencias' ? 'apple-segment-left apple-segment-bg-blue' : 'apple-segment-right apple-segment-bg-purple'
          ]"
        ></div>
        <button 
          @click="cambiarTab('asistencias')" 
          :class="['apple-segment-btn', tabActiva === 'asistencias' ? 'apple-segment-active apple-segment-active-blue' : '']"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="apple-segment-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>Registros</span>
        </button>
        <button 
          @click="cambiarTab('registros')" 
          :class="['apple-segment-btn', tabActiva === 'registros' ? 'apple-segment-active apple-segment-active-purple' : '']"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="apple-segment-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <span>Actividades</span>
        </button>
      </div>

      <!-- Tab de Registros Normales -->
      <div v-show="tabActiva === 'registros'" class="apple-tab-content">
        <div class="apple-title-row">
          <div class="apple-title-group">
            <h2 class="apple-section-title apple-title-purple">Actividades</h2>
            <p class="apple-section-subtitle">Historial de trabajo registrado</p>
          </div>
          <button @click="cargarRegistros" class="apple-refresh-btn apple-refresh-purple">
            <svg :class="['apple-refresh-icon', cargando ? 'apple-spinning' : '']" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Tab de Asistencias -->
      <div v-show="tabActiva === 'asistencias'" class="apple-tab-content">
        <div class="apple-title-row">
          <div class="apple-title-group">
            <h2 class="apple-section-title apple-title-blue">Registros</h2>
            <p class="apple-section-subtitle">Entradas y salidas del día</p>
          </div>
          <button @click="cargarAsistencias" class="apple-refresh-btn apple-refresh-blue">
            <svg :class="['apple-refresh-icon', cargandoAsistencias ? 'apple-spinning' : '']" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <div class="glass-card mb-2">
      <div v-if="error" class="mb-3 bg-red-100 border-l-4 border-red-500 text-red-700 p-3" role="alert">
        <p class="text-xs">{{ error }}</p>
        <p class="text-xs mt-1">
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
          <!-- Agrupar registros por fecha -->
          <div v-for="grupo in agruparRegistrosPorFecha(registros)" :key="grupo.fecha">
            <!-- Separador de fecha -->
            <div class="flex items-center gap-2 my-3 px-2">
              <div class="flex-1 h-px bg-gradient-to-r from-transparent via-purple-400 to-transparent"></div>
              <div class="flex items-center gap-1 px-3 py-1 bg-gradient-to-r from-purple-100 to-violet-100 rounded-full border border-purple-400/60 shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-purple-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h18M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span class="text-xs font-semibold text-purple-800 capitalize">{{ grupo.fecha }}</span>
              </div>
              <div class="flex-1 h-px bg-gradient-to-r from-transparent via-purple-400 to-transparent"></div>
            </div>
            
            <!-- Registros del día - Diseño Apple -->
            <div class="apple-historial-registros pl-1">
              <div v-for="(registro, index) in grupo.registros" :key="`${grupo.fecha}-${index}`" 
               :class="[
                 'apple-activity-card',
                 registro.tipo_actividad === 'campo' 
                   ? 'apple-activity-card-campo' 
                   : registro.tipo_actividad === 'gabinete'
                   ? 'apple-activity-card-gabinete'
                   : 'apple-activity-card-default'
               ]">
            
            <!-- Efecto de brillo superior Apple -->
            <div class="apple-card-shine"></div>
            
            <!-- Indicador lateral de tipo -->
            <div :class="[
              'apple-card-indicator',
              registro.tipo_actividad === 'campo' 
                ? 'apple-indicator-campo' 
                : registro.tipo_actividad === 'gabinete'
                ? 'apple-indicator-gabinete'
                : 'apple-indicator-default'
            ]"></div>
            
            <div class="apple-card-content">
              <div class="flex gap-2.5">
                <!-- Imagen más pequeña -->
                <div class="w-12 h-12 flex-shrink-0 rounded-lg overflow-hidden relative shadow-md" 
                     :class="{'cursor-pointer': registro.foto_url}" 
                     @click="registro.foto_url && verImagen(registro.foto_url)">
                  <img v-if="registro.foto_url" 
                       :src="registro.foto_url" 
                       class="w-full h-full object-cover transition-transform duration-300 hover:scale-110" 
                       alt="Foto" />
                  <div v-else class="flex justify-center">
                    <div :class="[
                      'w-12 h-12 rounded flex items-center justify-center relative group shadow-md border',
                      registro.tipo_actividad === 'campo' 
                        ? 'bg-gradient-to-br from-green-100 to-green-50 border-green-200/50' 
                        : registro.tipo_actividad === 'gabinete'
                        ? 'bg-gradient-to-br from-orange-100 to-orange-50 border-orange-200/50'
                        : 'bg-gradient-to-br from-gray-100 to-gray-50 border-gray-200/50'
                    ]">
                      <div :class="[
                        'flex flex-col items-center justify-center',
                        registro.tipo_actividad === 'campo' 
                          ? 'text-green-600' 
                          : registro.tipo_actividad === 'gabinete'
                          ? 'text-orange-600'
                          : 'text-gray-500'
                      ]">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 transition-transform duration-300 group-hover:scale-110" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"></path>
                        </svg>
                      </div>
                      <div :class="[
                        'absolute top-0 right-0 w-2 h-2 rounded-full',
                        registro.tipo_actividad === 'campo' 
                          ? 'bg-green-500' 
                          : registro.tipo_actividad === 'gabinete'
                          ? 'bg-orange-500'
                          : 'bg-gray-500'
                      ]"></div>
                    </div>
                  </div>
                  <div v-if="registro.foto_url" class="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-20 flex items-center justify-center transition-opacity rounded-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white opacity-0 hover:opacity-100 transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>
                </div>
                
                <div class="flex-1 min-w-0 space-y-1">
                  <!-- Header con fecha y botón de mapa más compacto -->
                  <div class="flex justify-between items-start">
                    <div class="flex flex-col">
                      <p class="text-xs font-semibold text-gray-700 leading-tight">{{ formatFechaCompleta(registro.fecha_hora) }}</p>
                      <p :class="[
                           'text-sm font-bold leading-tight',
                           registro.tipo_actividad === 'campo' 
                             ? 'text-green-700' 
                             : registro.tipo_actividad === 'gabinete'
                             ? 'text-orange-700'
                             : 'text-gray-700'
                         ]">{{ formatHoraCDMX(registro.fecha_hora) }}</p>
                    </div>
                    <button @click="verEnMapa(registro)" 
                            :class="[
                              'text-xs flex items-center px-2 py-1 rounded-lg font-medium transition-all duration-300 hover:scale-105 shadow-sm',
                              registro.tipo_actividad === 'campo' 
                                ? 'bg-green-100 text-green-700 hover:bg-green-200 border border-green-200' 
                                : registro.tipo_actividad === 'gabinete'
                                ? 'bg-orange-100 text-orange-700 hover:bg-orange-200 border border-orange-200'
                                : 'bg-gray-100 text-gray-700 hover:bg-gray-200 border border-gray-200'
                            ]">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      Ubicación
                    </button>
                  </div>
                  
                  <!-- Descripción más compacta -->
                  <p class="text-xs text-gray-800 leading-relaxed line-clamp-2">{{ registro.descripcion || "Sin descripción" }}</p>
                  
                  <!-- Tipo de actividad con diseño más compacto -->
                  <div v-if="registro.tipo_actividad" class="flex items-center justify-between">
                    <div class="flex items-center space-x-2">
                      <!-- Icono circular más pequeño -->
                      <div :class="[
                        'w-7 h-7 rounded-full flex items-center justify-center shadow-md transition-all duration-300 hover:scale-110',
                        registro.tipo_actividad === 'campo' 
                          ? 'bg-gradient-to-br from-green-600 to-green-700 shadow-green-600/40' 
                          : 'bg-gradient-to-br from-orange-600 to-orange-700 shadow-orange-600/40'
                      ]">
                        <!-- Efecto de brillo interno -->
                        <div class="absolute inset-0 bg-gradient-to-br from-white/20 to-transparent rounded-full"></div>
                        
                        <!-- Icono para Campo -->
                        <svg v-if="registro.tipo_actividad === 'campo'" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white relative z-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                        </svg>
                        <!-- Icono para Gabinete -->
                        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white relative z-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                      
                      <!-- Información del tipo de actividad más compacta -->
                      <div class="flex flex-col">
                        <span :class="[
                          'text-xs font-bold leading-tight',
                          registro.tipo_actividad === 'campo' 
                            ? 'text-green-800' 
                            : 'text-orange-800'
                        ]">
                          {{ registro.tipo_actividad === 'campo' ? 'Campo' : 'Gabinete' }}
                        </span>
                        <span :class="[
                          'text-xs leading-tight',
                          registro.tipo_actividad === 'campo' 
                            ? 'text-green-600' 
                            : 'text-orange-600'
                        ]">
                          {{ registro.tipo_actividad === 'campo' ? 'Terreno' : 'Oficina' }}
                        </span>
                      </div>
                    </div>
                    
                    <!-- Coordenadas más pequeñas -->
                    <div :class="[
                      'text-right bg-white/60 backdrop-blur-sm rounded px-1.5 py-0.5 border text-xs',
                      registro.tipo_actividad === 'campo' 
                        ? 'border-green-200/60' 
                        : 'border-orange-200/60'
                    ]">
                      <div class="text-xs text-gray-600 font-mono leading-tight">
                        {{ registro.latitud.toFixed(3) }}
                      </div>
                      <div class="text-xs text-gray-600 font-mono leading-tight">
                        {{ registro.longitud.toFixed(3) }}
                      </div>
                    </div>
                  </div>
                  
                  <!-- Categoría de actividad -->
                  <div v-if="registro.categoria_actividad" class="flex items-center gap-1.5 pt-1 mt-1 border-t border-gray-200/50">
                    <div class="w-5 h-5 rounded-full flex items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600 shadow-sm">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                      </svg>
                    </div>
                    <div class="flex flex-col">
                      <span class="text-xs font-semibold text-indigo-800 leading-tight">
                        {{ registro.categoria_actividad === 'Otro' && registro.categoria_actividad_otro 
                           ? registro.categoria_actividad_otro 
                           : registro.categoria_actividad }}
                      </span>
                      <span v-if="registro.categoria_actividad === 'Otro' && registro.categoria_actividad_otro" class="text-xs text-indigo-500 leading-tight">
                        Categoría: Otro
                      </span>
                    </div>
                  </div>
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
        <div class="mb-3 text-xs text-gray-600">
          Total de asistencias: <span class="font-semibold text-primary">{{ asistencias.length }}</span>
        </div>
        <div class="space-y-2">
          <!-- Agrupar asistencias por fecha -->
          <div v-for="grupo in agruparAsistenciasPorFecha(asistencias)" :key="grupo.fecha">
            <!-- Separador de fecha mejorado -->
            <div class="flex items-center gap-2 my-3 px-2">
              <div class="flex-1 h-px bg-gradient-to-r from-transparent via-blue-500 to-transparent"></div>
              <div class="flex items-center gap-1 px-3 py-1 bg-gradient-to-r from-blue-200 to-cyan-200 rounded-full border border-blue-600/70 shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-blue-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h18M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span class="text-xs font-semibold text-blue-900 capitalize">
                  {{ grupo.fecha || 'Fecha no disponible' }}
                </span>
              </div>
              <div class="flex-1 h-px bg-gradient-to-r from-transparent via-blue-500 to-transparent"></div>
            </div>

            <!-- Asistencias del día -->
            <div class="space-y-2">
              <div v-for="(asistencia, index) in grupo.asistencias" :key="`${grupo.fecha}-${index}`" class="glass-item border border-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-all">
            <div class="p-2">

              <!-- Diseño dividido: Inicio y Término en dos columnas -->
              <div class="grid grid-cols-2 gap-2">
                <!-- Columna Inicio -->
                <div class="entrada-bg-light rounded-lg p-2 border-2 shadow-sm">
                  <h4 class="text-xs font-bold entrada-text-dark mb-1 flex items-center justify-center text-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                    </svg>
                    Inicio
                  </h4>
                  <div class="w-full h-0.5 bg-gradient-to-r from-transparent via-blue-400 to-transparent mb-2"></div>
                  
                  <div v-if="asistencia.hora_entrada" class="space-y-2">
                    <div class="text-center">
                      <p class="text-xs font-bold entrada-text">{{ formatHora(asistencia.hora_entrada) }}</p>
                    </div>
                    
                    <div v-if="asistencia.foto_entrada_url" class="flex justify-center">
                      <div class="w-8 h-8 bg-gray-100 rounded overflow-hidden relative cursor-pointer" @click="verImagen(`${currentApiUrl}/${asistencia.foto_entrada_url}`)">
                        <img :src="`${currentApiUrl}/${asistencia.foto_entrada_url}`" class="w-full h-full object-cover" alt="Foto inicio" />
                        <div class="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-20 flex items-center justify-center transition-opacity">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-2 w-2 text-white opacity-0 hover:opacity-100" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                          </svg>
                        </div>
                      </div>
                    </div>
                    <div v-else class="flex justify-center">
                      <div class="w-8 h-8 rounded bg-gradient-to-br from-blue-100 to-blue-50 flex items-center justify-center relative group shadow-sm border border-blue-200/50">
                        <div class="text-blue-600 flex flex-col items-center justify-center">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transition-transform duration-300 group-hover:scale-110" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"></path>
                          </svg>
                        </div>
                        <div class="absolute top-0 right-0 w-2 h-2 rounded-full bg-blue-500 shadow-md"></div>
                      </div>
                    </div>
                    
                    <div class="flex justify-center">
                      <button @click="verAsistenciaEnMapa(asistencia, 'entrada')" 
                              class="text-xs flex items-center px-2 py-1 rounded-lg font-medium transition-all duration-300 hover:scale-105 shadow-sm bg-blue-100 text-blue-700 hover:bg-blue-200 border border-blue-200">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        <span class="text-xs">Ubicación</span>
                      </button>
                    </div>
                    
                    <p class="text-xs text-gray-600 text-center line-clamp-2">{{ asistencia.descripcion_entrada || "Sin descripción" }}</p>
                  </div>
                  
                  <div v-else class="text-center py-4">
                    <p class="text-xs text-gray-400">Sin registro</p>
                  </div>
                </div>

                <!-- Columna Término -->
                <div :class="[
                  'rounded-lg p-2 border-2 shadow-sm',
                  asistencia.hora_salida 
                    ? 'salida-bg-light' 
                    : 'bg-gray-50 border-gray-200'
                ]">
                  <h4 :class="[
                    'text-xs font-bold mb-1 flex items-center justify-center text-center',
                    asistencia.hora_salida ? 'salida-text-dark' : 'text-gray-500'
                  ]">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    Término
                  </h4>
                  <div :class="[
                    'w-full h-0.5 mb-2',
                    asistencia.hora_salida 
                      ? 'bg-gradient-to-r from-transparent via-red-400 to-transparent' 
                      : 'bg-gradient-to-r from-transparent via-gray-300 to-transparent'
                  ]"></div>
                  
                  <div v-if="asistencia.hora_salida" class="space-y-2">
                    <div class="text-center">
                      <p class="text-xs font-bold salida-text">{{ formatHora(asistencia.hora_salida) }}</p>
                    </div>
                    
                    <div v-if="asistencia.foto_salida_url" class="flex justify-center">
                      <div class="w-8 h-8 bg-gray-100 rounded overflow-hidden relative cursor-pointer" @click="verImagen(`${currentApiUrl}/${asistencia.foto_salida_url}`)">
                        <img :src="`${currentApiUrl}/${asistencia.foto_salida_url}`" class="w-full h-full object-cover" alt="Foto término" />
                        <div class="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-20 flex items-center justify-center transition-opacity">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-2 w-2 text-white opacity-0 hover:opacity-100" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                          </svg>
                        </div>
                      </div>
                    </div>
                    <div v-else class="flex justify-center">
                      <div class="w-8 h-8 rounded bg-gradient-to-br from-red-100 to-red-50 flex items-center justify-center relative group shadow-sm border border-red-200/50">
                        <div class="text-red-600 flex flex-col items-center justify-center">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transition-transform duration-300 group-hover:scale-110" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"></path>
                          </svg>
                        </div>
                        <div class="absolute top-0 right-0 w-2 h-2 rounded-full bg-red-500 shadow-md"></div>
                      </div>
                    </div>
                    
                    <div class="flex justify-center">
                      <button @click="verAsistenciaEnMapa(asistencia, 'salida')" 
                              class="text-xs flex items-center px-2 py-1 rounded-lg font-medium transition-all duration-300 hover:scale-105 shadow-sm bg-red-100 text-red-700 hover:bg-red-200 border border-red-200">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        <span class="text-xs">Ubicación</span>
                      </button>
                    </div>
                    
                    <p class="text-xs text-gray-600 text-center line-clamp-2">{{ asistencia.descripcion_salida || "Sin descripción" }}</p>
                  </div>
                  
                  <div v-else class="text-center py-4">
                    <div class="mb-2">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <p class="text-xs text-gray-500 font-medium">En curso</p>
                    <p class="text-xs text-gray-400 mt-1">Sin registro de término</p>
                  </div>
                </div>
              </div>

              <!-- Estado incompleto eliminado - ahora se maneja en el recuadro de salida -->
            </div>
          </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Estado vacío para registros -->
      <div v-if="tabActiva === 'registros' && registros.length === 0 && !cargando" class="text-center py-6">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <p class="mt-2 text-gray-500 text-sm">Aún no tienes registros guardados</p>
        <p class="text-xs text-gray-400 mt-1">Crea tu primer registro para verlo aquí</p>
        <router-link to="/" class="glass-button inline-block mt-3 text-xs">Crear nuevo registro</router-link>
      </div>

      <!-- Estado vacío para asistencias -->
      <div v-if="tabActiva === 'asistencias' && asistencias.length === 0 && !cargandoAsistencias" class="text-center py-6">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="mt-2 text-gray-500 text-sm">Aún no tienes registros de asistencia</p>
        <p class="text-xs text-gray-400 mt-1">Marca tu primera asistencia para verla aquí</p>
        <router-link to="/" class="glass-button inline-block mt-3 text-xs">Marcar asistencia</router-link>
      </div>
      
      <!-- Cargando registros -->
      <div v-if="tabActiva === 'registros' && cargando" class="text-center py-6">
        <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-primary mx-auto"></div>
        <p class="mt-3 text-gray-500 text-sm">Cargando registros...</p>
      </div>

      <!-- Cargando asistencias -->
      <div v-if="tabActiva === 'asistencias' && cargandoAsistencias" class="text-center py-6">
        <div class="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-primary mx-auto"></div>
        <p class="mt-3 text-gray-500 text-sm">Cargando asistencias...</p>
      </div>
    </div>
  </div>
</div>
    
    <!-- Diálogo de mapa mejorado con fondo transparente -->
    <teleport to="body" v-if="mapaVisible">
      <div class="fixed inset-0 backdrop-blur-md flex items-center justify-center z-[9999] p-2 sm:p-4 animate-fadeInSmooth">
        <!-- Contenedor del modal -->
        <div class="glass-map-modal-green w-full max-w-lg max-h-[90vh] sm:max-h-[85vh] flex flex-col rounded-3xl shadow-2xl overflow-hidden transform transition-all duration-300 animate-scaleInSmooth relative">
          
          <!-- Contenedor del mapa con header integrado -->
          <div class="flex-1 min-h-0 bg-gradient-to-br from-green-600 to-emerald-700 relative overflow-hidden">
            <!-- Efecto de brillo superior -->
            <div class="absolute inset-0 bg-gradient-to-br from-green-400/10 to-emerald-600/5 pointer-events-none z-0"></div>
            
            <!-- Mapa -->
            <div id="detailMap" class="h-full w-full relative z-10"></div>
            
            <!-- Botón cerrar circular - Posición flotante en esquina -->
            <button 
              @click="mapaVisible = false" 
              class="absolute top-4 right-4 sm:top-6 sm:right-6 flex items-center justify-center w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-red-500 hover:bg-red-600 text-white transition-all duration-300 hover:scale-110 active:scale-95 shadow-lg hover:shadow-red-500/50 z-20 group">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 sm:h-6 sm:w-6 group-hover:rotate-90 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </teleport>
    
    <!-- Modal para visualizar imagen -->
    <div v-if="imagenModalVisible" class="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50 p-2">
      <div class="w-full max-w-xs sm:max-w-sm md:max-w-md max-h-[80vh] flex flex-col relative">
        <button @click="imagenModalVisible = false" class="absolute right-1 top-1 bg-black bg-opacity-50 text-white rounded-full p-1 hover:bg-opacity-70 transition-opacity z-10">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <div class="overflow-hidden rounded-lg bg-black bg-opacity-30">
          <img :src="imagenSeleccionada" class="w-full h-auto object-contain max-h-[75vh]" alt="Imagen ampliada" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { apiService } from '../services/apiService.js';
import { checkInternetConnection, getOfflineMessage } from '../utils/network.js';

// Variable reactiva para la URL de la API
const currentApiUrl = ref('');

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
const tabActiva = ref('asistencias');
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
  
  // Inicializar URL de la API
  currentApiUrl.value = apiService.getCurrentApiUrl() || '';
  
  // Verificar conexión a internet
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    error.value = getOfflineMessage();
    cargando.value = false;
    return;
  }
  
  // Ahora que Asistencias es la tab por defecto, cargarla primero
  cargarAsistencias();
  // También cargar registros para que estén disponibles
  cargarRegistros();
});

// Watch para limpiar el mapa cuando se cierra el modal
watch(mapaVisible, (nuevoValor) => {
  if (!nuevoValor && detailMap.value) {
    // Limpiar el mapa cuando se cierra
    detailMap.value.remove();
    detailMap.value = null;
    console.log('🗺️ Mapa limpiado');
  }
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
    
    // Obtener registros específicos del usuario actual usando apiService
    const data = await apiService.getRecords(userInfo.value.id);
    
    console.log('Respuesta del servidor:', data);
    
    // Actualizar la URL de la API actual
    currentApiUrl.value = apiService.getCurrentApiUrl() || '';
    
    // Procesar las URLs de las fotos para que sean rutas absolutas
    registros.value = data.registros.map(r => ({
      ...r,
      foto_url: r.foto_url ? `${currentApiUrl.value}/${r.foto_url}` : null
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
    
    // Obtener asistencias específicas del usuario actual usando apiService
    const data = await apiService.getAttendances(userInfo.value.id);
    
    console.log('Respuesta del servidor (asistencias):', data);
    
    // Actualizar la URL de la API actual
    currentApiUrl.value = apiService.getCurrentApiUrl() || '';
    
    // Procesar asistencias y mostrar información de debug para fechas
    const asistenciasRaw = data.asistencias || [];
    
    asistenciasRaw.forEach((asistencia, index) => {
      console.log(`📅 Asistencia ${index + 1}:`);
      console.log('  - Fecha original de BD:', asistencia.fecha);
      console.log('  - Hora entrada original:', asistencia.hora_entrada);
      console.log('  - Hora salida original:', asistencia.hora_salida);
      
      if (asistencia.fecha) {
        const fechaFormateada = formatFecha(asistencia.fecha);
        console.log('  - Fecha formateada:', fechaFormateada);
      }
      
      if (asistencia.hora_entrada) {
        const entradaFormateada = formatHora(asistencia.hora_entrada);
        console.log('  - Entrada formateada:', entradaFormateada);
      }
      
      if (asistencia.hora_salida) {
        const salidaFormateada = formatHora(asistencia.hora_salida);
        console.log('  - Salida formateada:', salidaFormateada);
      }
    });
    
    asistencias.value = asistenciasRaw;
    
    console.log('✅ Total de asistencias procesadas:', asistencias.value.length);
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
    
    // Usar toLocaleTimeString con configuración específica para México
    return fecha.toLocaleTimeString('es-MX', {
      timeZone: 'America/Mexico_City',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
  } catch (e) {
    console.error('Error al formatear hora:', e, fechaStr);
    return fechaStr;
  }
}

function formatFechaCompleta(fechaStr) {
  try {
    if (!fechaStr) return '';
    
    // ✅ SOLUCIÓN CORRECTA: Extraer fecha directamente del string
    let año, mes, dia;
    
    if (fechaStr.includes('T')) {
      // Formato ISO: "2025-12-08T10:30:00"
      const partesFecha = fechaStr.split('T')[0].split('-');
      año = parseInt(partesFecha[0]);
      mes = parseInt(partesFecha[1]) - 1;
      dia = parseInt(partesFecha[2]);
    } else if (fechaStr.includes('-')) {
      // Formato simple: "2025-12-08"
      const partesFecha = fechaStr.split('-');
      año = parseInt(partesFecha[0]);
      mes = parseInt(partesFecha[1]) - 1;
      dia = parseInt(partesFecha[2]);
    } else {
      // Fallback
      const fecha = new Date(fechaStr);
      if (isNaN(fecha.getTime())) {
        console.error('Fecha inválida:', fechaStr);
        return fechaStr;
      }
      año = fecha.getFullYear();
      mes = fecha.getMonth();
      dia = fecha.getDate();
    }
    
    // Crear fecha local con los valores extraídos
    const fechaLocal = new Date(año, mes, dia, 12, 0, 0);
    
    if (isNaN(fechaLocal.getTime())) {
      console.error('Fecha inválida:', fechaStr);
      return fechaStr;
    }
    
    return fechaLocal.toLocaleDateString('es-MX', {
      weekday: 'short',
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  } catch (e) {
    console.error('Error al formatear fecha completa:', e, fechaStr);
    return fechaStr;
  }
}

// Nueva función para mostrar hora CDMX en formato AM/PM (igual que asistencias)
function formatHoraCDMX(fechaStr) {
  try {
    if (!fechaStr) return '';
    
    // ✅ SOLUCIÓN: Siempre usar timeZone para asegurar hora correcta
    const fecha = new Date(fechaStr);
    
    // Verificar que la fecha sea válida
    if (isNaN(fecha.getTime())) {
      console.error('Fecha inválida para hora:', fechaStr);
      return fechaStr;
    }
    
    // IMPORTANTE: Siempre especificar timeZone para evitar problemas
    return fecha.toLocaleTimeString('es-MX', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true,
      timeZone: 'America/Mexico_City'
    });
  } catch (e) {
    console.error('Error al formatear hora CDMX:', e, fechaStr);
    return fechaStr;
  }
}

// Función para obtener solo la fecha en formato CDMX (sin hora)
function obtenerFechaCDMX(fechaStr) {
  try {
    if (!fechaStr) {
      console.warn('⚠️ obtenerFechaCDMX: fechaStr vacía o null');
      return '';
    }
    
    console.log(`🔍 obtenerFechaCDMX: procesando "${fechaStr}"`);
    
    // ✅ SOLUCIÓN CORRECTA: Extraer la fecha directamente del string
    // para evitar problemas de conversión UTC -> local
    let año, mes, dia;
    
    // Detectar el formato de la fecha
    if (fechaStr.includes('T')) {
      // Formato ISO: "2025-12-08T10:30:00" o "2025-12-08T10:30:00-06:00"
      const partesFecha = fechaStr.split('T')[0].split('-');
      año = parseInt(partesFecha[0]);
      mes = parseInt(partesFecha[1]) - 1; // Meses en JS son 0-11
      dia = parseInt(partesFecha[2]);
    } else if (fechaStr.includes('-')) {
      // Formato simple: "2025-12-08"
      const partesFecha = fechaStr.split('-');
      año = parseInt(partesFecha[0]);
      mes = parseInt(partesFecha[1]) - 1;
      dia = parseInt(partesFecha[2]);
    } else if (fechaStr.includes('/')) {
      // Formato alternativo: "08/12/2025" o "12/08/2025"
      const partesFecha = fechaStr.split('/');
      // Asumimos formato DD/MM/YYYY
      dia = parseInt(partesFecha[0]);
      mes = parseInt(partesFecha[1]) - 1;
      año = parseInt(partesFecha[2]);
    } else {
      // Fallback: intentar parsear directamente
      const fecha = new Date(fechaStr);
      if (isNaN(fecha.getTime())) {
        console.error('❌ Fecha inválida:', fechaStr);
        return '';
      }
      año = fecha.getFullYear();
      mes = fecha.getMonth();
      dia = fecha.getDate();
    }
    
    // Crear fecha local (NO UTC) con los valores extraídos
    const fechaLocal = new Date(año, mes, dia, 12, 0, 0); // Usar mediodía para evitar edge cases
    
    if (isNaN(fechaLocal.getTime())) {
      console.error('❌ Fecha inválida después de parseo:', fechaStr);
      return '';
    }
    
    // Formatear la fecha usando locale español
    const resultado = fechaLocal.toLocaleDateString('es-MX', {
      weekday: 'short',
      day: '2-digit',
      month: 'long',
      year: 'numeric'
    });
    
    console.log(`✅ obtenerFechaCDMX: "${fechaStr}" -> "${resultado}" (año=${año}, mes=${mes+1}, dia=${dia})`);
    return resultado;
  } catch (e) {
    console.error('❌ Error al formatear fecha CDMX:', e, 'Input:', fechaStr);
    return '';
  }
}

// Función para agrupar registros por fecha (CDMX)
function agruparRegistrosPorFecha(registrosLista) {
  const grupos = {};
  
  registrosLista.forEach(registro => {
    const fechaCDMX = obtenerFechaCDMX(registro.fecha_hora);
    if (!grupos[fechaCDMX]) {
      grupos[fechaCDMX] = [];
    }
    grupos[fechaCDMX].push(registro);
  });
  
  // Convertir a array de objetos con fecha y registros, ordenados por fecha descendente
  return Object.entries(grupos)
    .map(([fecha, regs]) => ({
      fecha,
      registros: regs.sort((a, b) => new Date(b.fecha_hora) - new Date(a.fecha_hora))
    }))
    .sort((a, b) => new Date(b.registros[0].fecha_hora) - new Date(a.registros[0].fecha_hora));
}

// Función alternativa para extraer solo la fecha sin hora (fallback)
function extraerFechaSimple(fechaStr) {
  try {
    if (!fechaStr) return '';
    
    // Si es una fecha en formato ISO como "2025-11-05T11:24:00-06:00"
    // Extraer solo la parte de la fecha "2025-11-05"
    const partes = fechaStr.split('T');
    const fechaSola = partes[0];
    
    if (!fechaSola) return '';
    
    // Convertir "2025-11-05" a "mié, 05 de noviembre de 2025"
    // Primero crear un date desde la fecha en formato ISO local
    const [año, mes, dia] = fechaSola.split('-');
    const fecha = new Date(año, parseInt(mes) - 1, dia);
    
    if (isNaN(fecha.getTime())) {
      console.error('❌ extraerFechaSimple: fecha inválida:', fechaStr);
      return fechaSola; // Retornar al menos la fecha en formato simple
    }
    
    // Formatear con el mismo patrón que obtenerFechaCDMX
    const resultado = fecha.toLocaleDateString('es-MX', {
      weekday: 'short',
      day: '2-digit',
      month: 'long',
      year: 'numeric'
    });
    
    console.log(`✅ extraerFechaSimple: "${fechaStr}" -> "${resultado}"`);
    return resultado;
  } catch (e) {
    console.error('❌ Error en extraerFechaSimple:', e);
    return '';
  }
}

// Función para agrupar asistencias por fecha
function agruparAsistenciasPorFecha(asistenciasLista) {
  console.log(`🔍 agruparAsistenciasPorFecha: iniciando con ${asistenciasLista.length} asistencias`);
  
  const grupos = {};
  
  asistenciasLista.forEach((asistencia, idx) => {
    // DEBUG: Verificar estructura de asistencia
    if (!asistencia.fecha) {
      console.warn(`⚠️ Asistencia ${idx} sin fecha:`, asistencia);
      return;
    }
    
    console.log(`  [${idx}] Fecha raw: ${asistencia.fecha}`);
    
    // Intentar obtener fecha, si falla usar alternativa
    let fechaCDMX = obtenerFechaCDMX(asistencia.fecha);
    
    if (!fechaCDMX) {
      console.warn(`⚠️ obtenerFechaCDMX retornó vacío para: ${asistencia.fecha}, usando alternativa...`);
      fechaCDMX = extraerFechaSimple(asistencia.fecha);
    }
    
    console.log(`  ➜ Fecha formateada: "${fechaCDMX}"`);
    
    if (!fechaCDMX) {
      console.error(`❌ No se pudo obtener fecha para asistencia ${idx}:`, asistencia);
      return;
    }
    
    if (!grupos[fechaCDMX]) {
      grupos[fechaCDMX] = [];
      console.log(`  ✨ Nuevo grupo creado: "${fechaCDMX}"`);
    }
    grupos[fechaCDMX].push(asistencia);
  });
  
  console.log(`📊 Total de grupos creados: ${Object.keys(grupos).length}`);
  console.log(`📊 Grupos:`, Object.keys(grupos));
  
  // Convertir a array de objetos con fecha y asistencias, ordenados por fecha descendente
  const resultado = Object.entries(grupos)
    .map(([fecha, asists]) => ({
      fecha,
      asistencias: asists.sort((a, b) => new Date(b.fecha) - new Date(a.fecha))
    }))
    .sort((a, b) => new Date(b.asistencias[0].fecha) - new Date(a.asistencias[0].fecha));
  
  console.log(`✅ Agrupamiento completado:`, resultado);
  return resultado;
}

function verEnMapa(registro) {
  // Validar que tenga coordenadas válidas
  if (!registro.latitud || !registro.longitud) {
    console.error('❌ Ubicación sin coordenadas válidas:', registro);
    alert('Esta ubicación no tiene coordenadas disponibles');
    return;
  }

  registroSeleccionado.value = registro;
  mapaVisible.value = true;
  
  // Destruir el mapa anterior si existe
  if (detailMap.value) {
    detailMap.value.remove();
    detailMap.value = null;
  }
  
  // Esperar a que el DOM se actualice
  setTimeout(() => {
    try {
      // Inicializar mapa nuevo
      detailMap.value = L.map('detailMap').setView([registro.latitud, registro.longitud], 16);
      
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
      }).addTo(detailMap.value);
      
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
        if (detailMap.value) {
          detailMap.value.invalidateSize();
        }
      }, 100);
      
      console.log('✅ Mapa cargado correctamente en:', registro.latitud, registro.longitud);
    } catch (error) {
      console.error('❌ Error al cargar el mapa:', error);
    }
  }, 100);
}

// Función para ver asistencia en el mapa
function verAsistenciaEnMapa(asistencia, tipo) {
  const latitud = tipo === 'entrada' ? asistencia.latitud_entrada : asistencia.latitud_salida;
  const longitud = tipo === 'entrada' ? asistencia.longitud_entrada : asistencia.longitud_salida;
  const descripcion = tipo === 'entrada' ? asistencia.descripcion_entrada : asistencia.descripcion_salida;
  
  // Validar que tenga coordenadas válidas
  if (!latitud || !longitud) {
    console.error(`❌ Sin coordenadas de ${tipo}:`, { latitud, longitud, asistencia });
    alert(`No hay coordenadas de ${tipo} disponibles para esta asistencia`);
    return;
  }
  
  // Crear un objeto similar a registro para reutilizar la función existente
  const registroParaMapa = {
    latitud: latitud,
    longitud: longitud,
    descripcion: descripcion || `${tipo.charAt(0).toUpperCase() + tipo.slice(1)} - ${formatFecha(asistencia.fecha)}`
  };
  
  console.log(`📍 Abriendo mapa de ${tipo}:`, registroParaMapa);
  verEnMapa(registroParaMapa);
}

// Cargar asistencias cuando se cambia a esa pestaña
// Cargar datos cuando se cambia de pestaña
function cambiarTab(tab) {
  tabActiva.value = tab;
  if (tab === 'asistencias' && asistencias.value.length === 0) {
    cargarAsistencias();
  }
  if (tab === 'registros' && registros.value.length === 0) {
    cargarRegistros();
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

/* Efecto de vidrio realista - Glassmorphism */
.glass-card {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
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

/* Ajustes específicos para pantallas pequeñas */
@media (max-width: 320px) {
  .w-12 {
    width: 2.75rem;
  }
  
  .h-12 {
    height: 2.75rem;
  }
  
  .w-10 {
    width: 2.25rem;
  }
  
  .h-10 {
    height: 2.25rem;
  }
  
  .gap-2 {
    gap: 0.375rem;
  }
  
  .text-lg {
    font-size: 1rem !important;
  }
  
  .text-sm {
    font-size: 0.75rem !important;
  }
}

/* Estilos para botones con efecto de vidrio */
.glass-button {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #1f2937;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 16px 0 rgba(31, 38, 135, 0.15),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 30px;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.3);
  padding: 0.375rem 0.75rem;
}

/* Botón de actualizar con efecto vidrio líquido mejorado */
.glass-button-refresh {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.1));
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: #374151;
  font-weight: 600;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 3px 15px 0 rgba(31, 38, 135, 0.15),
    0 1px 6px 0 rgba(0, 0, 0, 0.08),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.4);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
  min-height: 24px;
  font-size: 0.7rem;
}

.glass-button-refresh::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transition: left 0.6s ease;
}

.glass-button-refresh:hover {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.35), rgba(255, 255, 255, 0.15));
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 
    0 4px 20px 0 rgba(31, 38, 135, 0.2),
    0 2px 8px 0 rgba(0, 0, 0, 0.12),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.5);
  transform: translateY(-1px) scale(1.02);
}

.glass-button-refresh:hover::before {
  left: 100%;
}

.glass-button-refresh:active {
  transform: translateY(0) scale(0.98);
  box-shadow: 
    0 1px 8px 0 rgba(31, 38, 135, 0.15),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
}

/* Estilos modernos para pestañas con efecto vidrio líquido */
.tab-button-liquid {
  position: relative;
  cursor: pointer;
  font-weight: 600;
  letter-spacing: 0.05em;
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  min-width: 160px;
  text-align: center;
  background: transparent;
  border: none;
  outline: none;
  will-change: transform, color;
  -webkit-font-smoothing: antialiased;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
}

.tab-button-liquid:hover {
  backdrop-filter: blur(35px);
  -webkit-backdrop-filter: blur(35px);
  transform: translateY(-2px);
  transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.tab-button-liquid:active {
  transform: translateY(1px);
  transition: all 0.1s ease;
}

/* Animación suave para el contenedor de pestañas */
.glass-card .flex.bg-gradient-to-r {
  position: relative;
  overflow: hidden;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
}

/* Animación de pulso suave para elementos activos */
@keyframes pulse-gentle {
  0%, 100% {
    opacity: 0.8;
  }
  50% {
    opacity: 1;
  }
}

.animate-pulse-gentle {
  animation: pulse-gentle 3s ease-in-out infinite;
}

/* Estilos para elementos individuales con efecto de vidrio */
.glass-item {
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 
    0 4px 20px 0 rgba(31, 38, 135, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.15);
  position: relative;
}

.glass-item:hover {
  background: rgba(255, 255, 255, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 30px 0 rgba(31, 38, 135, 0.15),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

/* Estilos para modales con efecto de vidrio */
.glass-modal {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 8px 32px 0 rgba(31, 38, 135, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
}

.glass-modal .border-b,
.glass-modal .border-t {
  border-color: rgba(255, 255, 255, 0.2);
}

/* Botón de cerrar con efecto de vidrio */
.glass-close-button {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 4px;
  transition: all 0.3s ease;
}

.glass-close-button:hover {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

/* Responsividad mejorada */
@media (max-width: 640px) {
  .page-container {
    padding-left: 0.75rem !important;
    padding-right: 0.75rem !important;
  }
  
  .glass-card {
    margin: 0.25rem 0;
    padding: 0.75rem;
    border-radius: 16px;
  }
  
  .tab-button-liquid {
    font-size: 0.65rem;
    padding: 6px 28px;
    min-width: 130px;
  }
  
  .tab-button-liquid span {
    font-size: 0.65rem;
  }
  
  .glass-button {
    font-size: 0.7rem;
    padding: 4px 8px;
    min-height: 26px;
  }
  
  .glass-item {
    margin: 0.2rem 0;
  }
  
  .glass-modal {
    margin: 0.25rem;
    max-width: calc(100vw - 0.5rem);
    border-radius: 12px;
  }
}

/* Optimización para móviles extra pequeños */
@media (max-width: 480px) {
  .page-container {
    padding-left: 0.5rem !important;
    padding-right: 0.5rem !important;
  }
  
  .glass-card {
    margin: 0.125rem 0;
    padding: 0.625rem;
  }
  
  .tab-button-liquid {
    font-size: 0.6rem;
    padding: 4px 24px;
    min-width: 110px;
  }
  
  .tab-button-liquid span {
    font-size: 0.6rem;
    font-weight: 600;
  }
}

/* Optimización para tablets */
@media (min-width: 641px) and (max-width: 1024px) {
  .page-container {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
  }
  
  .tab-button-liquid {
    min-width: 180px;
    padding: 8px 36px;
    font-size: 0.75rem;
  }
}

/* Optimización para pantallas grandes */
@media (min-width: 1025px) {
  .page-container {
    max-width: 1200px;
    margin: 0 auto;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
  }
  
  .tab-button-liquid {
    min-width: 220px;
    padding: 8px 48px;
    font-size: 0.8rem;
  }
}

/* Estilos adicionales para el historial moderno */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Animaciones suaves para las tarjetas del historial más compactas */
@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.space-y-1\.5 > * {
  animation: slideInUp 0.3s ease-out;
}

.space-y-1\.5 > *:nth-child(1) { animation-delay: 0s; }
.space-y-1\.5 > *:nth-child(2) { animation-delay: 0.05s; }
.space-y-1\.5 > *:nth-child(3) { animation-delay: 0.1s; }
.space-y-1\.5 > *:nth-child(4) { animation-delay: 0.15s; }
.space-y-1\.5 > *:nth-child(5) { animation-delay: 0.2s; }

/* Efectos de hover mejorados para los iconos más pequeños */
.hover\:scale-110:hover {
  transform: scale(1.1);
}

.hover\:scale-105:hover {
  transform: scale(1.05);
}

.hover\:scale-\[1\.01\]:hover {
  transform: scale(1.01);
}

/* Estilos específicos para fondos con transparencia */
.bg-gradient-to-br {
  position: relative;
}

/* Mejoras específicas para móviles en el historial compacto */
@media (max-width: 640px) {
  .space-y-1\.5 > * {
    margin-bottom: 0.5rem;
  }
  
  .space-y-1\.5 > div {
    padding: 0.625rem;
  }
  
  .w-12.h-12 {
    width: 2.75rem;
    height: 2.75rem;
  }
  
  .w-7.h-7 {
    width: 1.5rem;
    height: 1.5rem;
  }
  
  .text-xs {
    font-size: 0.65rem;
  }
}

/* Efectos de profundidad y sombras dinámicas más sutiles */
.hover\:shadow-lg:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.hover\:shadow-green-200\/50:hover {
  box-shadow: 0 10px 15px -3px rgba(34, 197, 94, 0.1), 0 4px 6px -2px rgba(34, 197, 94, 0.05);
}

.hover\:shadow-orange-200\/50:hover {
  box-shadow: 0 10px 15px -3px rgba(251, 146, 60, 0.1), 0 4px 6px -2px rgba(251, 146, 60, 0.05);
}

.hover\:shadow-gray-200\/50:hover {
  box-shadow: 0 10px 15px -3px rgba(156, 163, 175, 0.1), 0 4px 6px -2px rgba(156, 163, 175, 0.05);
}

/* Colores personalizados para entrada y salida que coincidan con Home.vue */
.entrada-colors {
  background-color: rgb(30, 144, 255) !important;
  border-color: rgb(25, 130, 230) !important;
  color: white !important;
}

.entrada-bg-light {
  background-color: rgba(30, 144, 255, 0.1) !important;
  border-color: rgba(30, 144, 255, 0.3) !important;
}

.entrada-text {
  color: rgb(30, 144, 255) !important;
}

.entrada-text-dark {
  color: rgb(25, 130, 230) !important;
}

.salida-colors {
  background-color: rgb(220, 20, 60) !important;
  border-color: rgb(200, 15, 55) !important;
  color: white !important;
}

.salida-bg-light {
  background-color: rgba(220, 20, 60, 0.1) !important;
  border-color: rgba(220, 20, 60, 0.3) !important;
}

.salida-text {
  color: rgb(220, 20, 60) !important;
}

.salida-text-dark {
  color: rgb(200, 15, 55) !important;
}

/* Estilos para iconos de "GUARDADO" cuando no hay imagen */
.guardado-icon-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.guardado-icon-container::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0));
  pointer-events: none;
}

.guardado-icon-container:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  transform: scale(1.05);
}

/* Animación de pulsación para el distintivo de seguridad */
@keyframes pulseCheck {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.8;
  }
}

.guardado-icon-container .absolute.top-0.right-0 {
  animation: pulseCheck 2.5s ease-in-out infinite;
}

/* Animación suave de aparición para los iconos */
@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.guardado-icon-container {
  animation: fadeInScale 0.4s ease-out;
}

/* ============ Estilos del Modal de Mapa Mejorado ============ */

/* Modal de mapa verde fuerte con efecto glassmorphism */
.glass-map-modal-green {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.95), rgba(5, 150, 105, 0.95));
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border: 2px solid rgba(16, 185, 129, 0.5);
  box-shadow: 
    0 25px 70px 0 rgba(16, 185, 129, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
}

/* Animación de entrada suave y fluida para el modal */
@keyframes fadeInSmooth {
  from {
    opacity: 0;
    backdrop-filter: blur(0px);
  }
  to {
    opacity: 1;
    backdrop-filter: blur(12px);
  }
}

@keyframes scaleInSmooth {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.animate-fadeInSmooth {
  animation: fadeInSmooth 0.5s ease-out;
}

.animate-scaleInSmooth {
  animation: scaleInSmooth 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* Responsividad mejorada para el modal de mapa verde */
@media (max-width: 640px) {
  .glass-map-modal-green {
    max-width: calc(100vw - 1rem);
    max-height: calc(100vh - 4rem);
  }
  
  .glass-map-modal-green #detailMap {
    min-height: 320px;
  }
}

@media (min-width: 641px) and (max-width: 1024px) {
  .glass-map-modal-green {
    max-width: 500px;
    max-height: calc(100vh - 3rem);
  }
}

@media (min-width: 1025px) {
  .glass-map-modal-green {
    max-width: 600px;
    max-height: calc(100vh - 2rem);
  }
}

/* Mejoras para la visibilidad del mapa */
#detailMap {
  background: linear-gradient(135deg, rgba(5, 150, 105, 0.9), rgba(16, 185, 129, 0.9)) !important;
}

/* Overlay transparente difuminado */
.fixed.inset-0.backdrop-blur-md {
  background-color: transparent !important;
  backdrop-filter: blur(8px) !important;
  -webkit-backdrop-filter: blur(8px) !important;
}

/* Animación del botón cerrar con rotación */
@keyframes buttonPulseGreen {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(239, 68, 68, 0);
  }
}

/* ================================================
   ESTILOS APPLE PARA HISTORIAL - LIQUID GLASS 
   ================================================ */

/* ============================================
   HEADER APPLE - SEGMENTED CONTROL
   ============================================ */

.apple-header-section {
  background: linear-gradient(180deg, 
    rgba(255, 255, 255, 0.98) 0%,
    rgba(249, 250, 251, 0.95) 100%);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-radius: 20px;
  padding: 1rem;
  margin-bottom: 0.75rem;
  border: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 
    0 2px 16px rgba(0, 0, 0, 0.04),
    0 1px 4px rgba(0, 0, 0, 0.02);
  animation: appleFadeInScale 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Segmented Control estilo iOS */
.apple-segmented-control {
  display: flex;
  position: relative;
  background: rgba(118, 118, 128, 0.12);
  border-radius: 10px;
  padding: 2px;
  margin-bottom: 0.75rem;
}

/* Indicador del segmento activo */
.apple-segment-bg {
  position: absolute;
  top: 2px;
  bottom: 2px;
  width: calc(50% - 2px);
  background: white;
  border-radius: 8px;
  box-shadow: 
    0 3px 8px rgba(0, 0, 0, 0.12),
    0 1px 3px rgba(0, 0, 0, 0.08);
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-segment-left {
  left: 2px;
}

.apple-segment-right {
  left: calc(50%);
}

/* Colores del indicador */
.apple-segment-bg-blue {
  background: linear-gradient(135deg, #0a84ff 0%, #2563eb 100%);
  box-shadow: 
    0 4px 12px rgba(10, 132, 255, 0.35),
    0 2px 4px rgba(10, 132, 255, 0.2);
}

.apple-segment-bg-purple {
  background: linear-gradient(135deg, #9333ea 0%, #7c3aed 100%);
  box-shadow: 
    0 4px 12px rgba(147, 51, 234, 0.35),
    0 2px 4px rgba(147, 51, 234, 0.2);
}

/* Botones del segmento */
.apple-segment-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  padding: 0.5rem 1rem;
  font-size: 0.8125rem;
  font-weight: 600;
  letter-spacing: -0.01em;
  color: rgba(0, 0, 0, 0.5);
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  position: relative;
  z-index: 2;
  transition: color 0.25s ease;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', sans-serif;
}

.apple-segment-btn:active {
  transform: scale(0.97);
}

.apple-segment-active {
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);
}

.apple-segment-active-blue {
  color: white;
}

.apple-segment-active-purple {
  color: white;
}

.apple-segment-icon {
  width: 1rem;
  height: 1rem;
  stroke-width: 2.5;
  transition: transform 0.3s ease;
}

.apple-segment-active .apple-segment-icon {
  transform: scale(1.1);
}

/* Tab content */
.apple-tab-content {
  animation: appleSlideUp 0.3s ease-out;
}

@keyframes appleSlideUp {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Fila del título */
.apple-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Título de sección */
.apple-section-title {
  font-size: 1.125rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
  margin: 0;
}

.apple-title-purple {
  background: linear-gradient(135deg, #9333ea 0%, #7c3aed 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.apple-title-blue {
  background: linear-gradient(135deg, #0a84ff 0%, #2563eb 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Grupo de título con subtítulo */
.apple-title-group {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

/* Subtítulo de sección */
.apple-section-subtitle {
  font-size: 0.75rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.45);
  letter-spacing: -0.01em;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', sans-serif;
}

/* Botón de actualizar */
.apple-refresh-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  background: rgba(0, 0, 0, 0.04);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.25s ease;
}

.apple-refresh-btn:hover {
  background: rgba(0, 0, 0, 0.08);
  transform: scale(1.05);
}

.apple-refresh-btn:active {
  transform: scale(0.95);
}

.apple-refresh-icon {
  width: 1rem;
  height: 1rem;
  color: rgba(0, 0, 0, 0.5);
  transition: all 0.25s ease;
}

.apple-refresh-btn:hover .apple-refresh-icon {
  color: rgba(0, 0, 0, 0.7);
}

/* Botón refresh azul (Registros) */
.apple-refresh-blue {
  background: rgba(10, 132, 255, 0.12);
}

.apple-refresh-blue .apple-refresh-icon {
  color: #0a84ff;
}

.apple-refresh-blue:hover {
  background: rgba(10, 132, 255, 0.2);
}

.apple-refresh-blue:hover .apple-refresh-icon {
  color: #0066cc;
}

/* Botón refresh morado (Actividades) */
.apple-refresh-purple {
  background: rgba(147, 51, 234, 0.12);
}

.apple-refresh-purple .apple-refresh-icon {
  color: #9333ea;
}

.apple-refresh-purple:hover {
  background: rgba(147, 51, 234, 0.2);
}

.apple-refresh-purple:hover .apple-refresh-icon {
  color: #7c3aed;
}

.apple-spinning {
  animation: appleSpin 1s linear infinite;
}

@keyframes appleSpin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ============================================
   FIN HEADER APPLE
   ============================================ */

/* Contenedor de registros de actividades */
.apple-historial-registros {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Tarjeta de actividad estilo Apple */
.apple-activity-card {
  position: relative;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.95) 0%, 
    rgba(255, 255, 255, 0.85) 50%,
    rgba(255, 255, 255, 0.9) 100%);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-radius: 16px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 
    0 4px 24px rgba(0, 0, 0, 0.06),
    0 1px 4px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  animation: appleCardSlideIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) backwards;
}

.apple-activity-card:nth-child(1) { animation-delay: 0s; }
.apple-activity-card:nth-child(2) { animation-delay: 0.05s; }
.apple-activity-card:nth-child(3) { animation-delay: 0.1s; }
.apple-activity-card:nth-child(4) { animation-delay: 0.15s; }
.apple-activity-card:nth-child(5) { animation-delay: 0.2s; }

@keyframes appleCardSlideIn {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.apple-activity-card:hover {
  transform: translateY(-2px) scale(1.01);
  box-shadow: 
    0 12px 40px rgba(0, 0, 0, 0.12),
    0 4px 12px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.apple-activity-card:active {
  transform: scale(0.99);
}

/* Efecto de brillo superior Apple */
.apple-card-shine {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(180deg, 
    rgba(255, 255, 255, 0.5) 0%, 
    rgba(255, 255, 255, 0) 100%);
  pointer-events: none;
  border-radius: 16px 16px 0 0;
}

/* Indicador lateral de tipo */
.apple-card-indicator {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  border-radius: 16px 0 0 16px;
}

.apple-indicator-campo {
  background: linear-gradient(180deg, #30d158 0%, #28a745 100%);
  box-shadow: 2px 0 12px rgba(48, 209, 88, 0.3);
}

.apple-indicator-gabinete {
  background: linear-gradient(180deg, #ff9500 0%, #ff6b00 100%);
  box-shadow: 2px 0 12px rgba(255, 149, 0, 0.3);
}

.apple-indicator-default {
  background: linear-gradient(180deg, #8e8e93 0%, #636366 100%);
}

/* Contenido de la tarjeta */
.apple-card-content {
  position: relative;
  z-index: 10;
  padding: 1rem;
  padding-left: 1.25rem;
}

/* Variante Campo - Verde Apple */
.apple-activity-card-campo {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.95) 0%, 
    rgba(240, 255, 244, 0.85) 50%,
    rgba(255, 255, 255, 0.9) 100%);
  border-color: rgba(48, 209, 88, 0.15);
}

.apple-activity-card-campo:hover {
  border-color: rgba(48, 209, 88, 0.3);
  box-shadow: 
    0 12px 40px rgba(48, 209, 88, 0.15),
    0 4px 12px rgba(48, 209, 88, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

/* Variante Gabinete - Naranja Apple */
.apple-activity-card-gabinete {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.95) 0%, 
    rgba(255, 248, 240, 0.85) 50%,
    rgba(255, 255, 255, 0.9) 100%);
  border-color: rgba(255, 149, 0, 0.15);
}

.apple-activity-card-gabinete:hover {
  border-color: rgba(255, 149, 0, 0.3);
  box-shadow: 
    0 12px 40px rgba(255, 149, 0, 0.15),
    0 4px 12px rgba(255, 149, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

/* Imagen de actividad estilo Apple */
.apple-activity-image {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-activity-image:hover {
  transform: scale(1.05);
  box-shadow: 
    0 8px 20px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.4);
}

.apple-activity-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-activity-image:hover img {
  transform: scale(1.1);
}

/* Botón de ubicación estilo Apple */
.apple-location-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 0.875rem;
  border-radius: 100px;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: -0.01em;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  cursor: pointer;
}

.apple-location-btn-campo {
  background: linear-gradient(180deg, #30d158 0%, #28a745 100%);
  color: white;
  box-shadow: 
    0 4px 12px rgba(48, 209, 88, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.apple-location-btn-gabinete {
  background: linear-gradient(180deg, #ff9500 0%, #ff6b00 100%);
  color: white;
  box-shadow: 
    0 4px 12px rgba(255, 149, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.apple-location-btn:hover {
  transform: translateY(-1px) scale(1.02);
}

.apple-location-btn:active {
  transform: scale(0.98);
}

/* Badge de tipo estilo Apple */
.apple-type-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 0.75rem;
  border-radius: 10px;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
  font-size: 0.6875rem;
  font-weight: 500;
}

.apple-type-badge-campo {
  background: rgba(48, 209, 88, 0.12);
  color: #1d7a34;
}

.apple-type-badge-gabinete {
  background: rgba(255, 149, 0, 0.12);
  color: #995a00;
}

/* Coordenadas estilo Apple */
.apple-coords {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  background: rgba(142, 142, 147, 0.08);
  border-radius: 6px;
  font-family: 'SF Mono', 'Menlo', monospace;
  font-size: 0.625rem;
  color: #636366;
}

/* ========================================
   TARJETAS DE ASISTENCIAS ESTILO APPLE
   ======================================== */

/* Tarjeta de asistencia - Liquid Glass */
.glass-item {
  position: relative;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.95) 0%, 
    rgba(255, 255, 255, 0.85) 50%,
    rgba(255, 255, 255, 0.9) 100%) !important;
  backdrop-filter: blur(20px) saturate(180%) !important;
  -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
  border-radius: 16px !important;
  border: 1px solid rgba(0, 0, 0, 0.06) !important;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
  box-shadow: 
    0 4px 24px rgba(0, 0, 0, 0.06),
    0 1px 4px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
  animation: appleCardSlideIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) backwards;
}

.glass-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(180deg, 
    rgba(255, 255, 255, 0.5) 0%, 
    rgba(255, 255, 255, 0) 100%);
  pointer-events: none;
  border-radius: 16px 16px 0 0;
}

.glass-item:hover {
  transform: translateY(-2px) scale(1.005) !important;
  box-shadow: 
    0 12px 40px rgba(0, 0, 0, 0.12),
    0 4px 12px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
}

/* Columnas de Inicio y Término mejoradas */
.entrada-bg-light {
  background: linear-gradient(135deg, 
    rgba(10, 132, 255, 0.08) 0%, 
    rgba(10, 132, 255, 0.04) 100%) !important;
  border: 1.5px solid rgba(10, 132, 255, 0.2) !important;
  border-radius: 14px !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.entrada-bg-light:hover {
  background: linear-gradient(135deg, 
    rgba(10, 132, 255, 0.12) 0%, 
    rgba(10, 132, 255, 0.06) 100%) !important;
  border-color: rgba(10, 132, 255, 0.3) !important;
}

.salida-bg-light {
  background: linear-gradient(135deg, 
    rgba(255, 69, 58, 0.08) 0%, 
    rgba(255, 69, 58, 0.04) 100%) !important;
  border: 1.5px solid rgba(255, 69, 58, 0.2) !important;
  border-radius: 14px !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.salida-bg-light:hover {
  background: linear-gradient(135deg, 
    rgba(255, 69, 58, 0.12) 0%, 
    rgba(255, 69, 58, 0.06) 100%) !important;
  border-color: rgba(255, 69, 58, 0.3) !important;
}

/* Títulos estilo Apple */
.entrada-text-dark {
  color: #0a84ff !important;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
  font-weight: 600 !important;
  letter-spacing: -0.01em;
}

.salida-text-dark {
  color: #ff453a !important;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
  font-weight: 600 !important;
  letter-spacing: -0.01em;
}

.entrada-text {
  color: #0a84ff !important;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
  font-weight: 700 !important;
  font-size: 1rem !important;
}

.salida-text {
  color: #ff453a !important;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
  font-weight: 700 !important;
  font-size: 1rem !important;
}

/* glass-card mejorado para tabs */
.glass-card {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.9) 0%, 
    rgba(255, 255, 255, 0.7) 50%,
    rgba(255, 255, 255, 0.85) 100%) !important;
  backdrop-filter: blur(25px) saturate(200%) !important;
  -webkit-backdrop-filter: blur(25px) saturate(200%) !important;
  border-radius: 20px !important;
  border: 1px solid rgba(255, 255, 255, 0.5) !important;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.08),
    0 2px 8px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
  padding: 1rem !important;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* Separadores de fecha mejorados */
.flex.items-center.gap-2.my-3 {
  animation: appleFadeInScale 0.4s ease-out backwards;
}

@keyframes appleFadeInScale {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Botón de actualizar mejorado */
.glass-button-refresh {
  background: linear-gradient(180deg, 
    rgba(255, 255, 255, 0.9) 0%, 
    rgba(245, 245, 247, 0.9) 100%) !important;
  border: 1px solid rgba(0, 0, 0, 0.08) !important;
  border-radius: 100px !important;
  padding: 0.5rem 1rem !important;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif !important;
  font-weight: 600 !important;
  color: #1d1d1f !important;
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.06),
    inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.glass-button-refresh:hover {
  transform: translateY(-1px) scale(1.02) !important;
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
}

/* ================================================
   RESPONSIVIDAD APPLE
   ================================================ */

/* Móviles pequeños */
@media (max-width: 374px) {
  .apple-header-section {
    padding: 0.75rem;
    border-radius: 16px;
  }
  
  .apple-segmented-control {
    border-radius: 8px;
  }
  
  .apple-segment-btn {
    padding: 0.4rem 0.75rem;
    font-size: 0.75rem;
  }
  
  .apple-segment-icon {
    width: 0.875rem;
    height: 0.875rem;
  }
  
  .apple-section-title {
    font-size: 1rem;
  }
  
  .apple-refresh-btn {
    width: 1.75rem;
    height: 1.75rem;
  }
  
  .apple-refresh-icon {
    width: 0.875rem;
    height: 0.875rem;
  }
  
  .apple-activity-card {
    border-radius: 14px;
  }
  
  .apple-card-content {
    padding: 0.75rem;
    padding-left: 1rem;
  }
  
  .apple-activity-image {
    width: 44px;
    height: 44px;
    border-radius: 10px;
  }
  
  .apple-location-btn {
    padding: 0.375rem 0.625rem;
    font-size: 0.625rem;
  }
  
  .glass-item {
    border-radius: 14px !important;
  }
  
  .glass-card {
    border-radius: 16px !important;
    padding: 0.75rem !important;
  }
  
  .entrada-bg-light,
  .salida-bg-light {
    border-radius: 12px !important;
    padding: 0.5rem !important;
  }
  
  .entrada-text,
  .salida-text {
    font-size: 0.875rem !important;
  }
}

/* Móviles medianos */
@media (min-width: 375px) and (max-width: 428px) {
  .apple-activity-card {
    border-radius: 16px;
  }
  
  .apple-card-content {
    padding: 0.875rem;
    padding-left: 1.125rem;
  }
  
  .apple-activity-image {
    width: 52px;
    height: 52px;
    border-radius: 11px;
  }
}

/* Tablets y Desktop */
@media (min-width: 429px) {
  .apple-activity-card {
    border-radius: 18px;
  }
  
  .apple-card-content {
    padding: 1.125rem;
    padding-left: 1.375rem;
  }
  
  .apple-activity-image {
    width: 64px;
    height: 64px;
    border-radius: 14px;
  }
  
  .apple-location-btn {
    padding: 0.5rem 1rem;
    font-size: 0.75rem;
  }
  
  .glass-item {
    border-radius: 18px !important;
  }
  
  .glass-card {
    border-radius: 22px !important;
    padding: 1.25rem !important;
  }
  
  .entrada-bg-light,
  .salida-bg-light {
    border-radius: 16px !important;
  }
}

/* Tablets grandes */
@media (min-width: 768px) {
  .apple-activity-card {
    border-radius: 20px;
  }
  
  .apple-historial-registros {
    gap: 1rem;
  }
  
  .glass-item {
    border-radius: 20px !important;
  }
}

/* Animación de scroll suave */
.apple-historial-registros > *,
.space-y-2 > * {
  will-change: transform, opacity;
}
</style>
