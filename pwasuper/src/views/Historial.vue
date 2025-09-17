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
    <div class="glass-card mb-2">
      <div class="flex justify-center border-b border-white/20 mb-2 pb-3">
        <div class="flex bg-gradient-to-r from-white/10 via-white/15 to-white/10 backdrop-blur-xl rounded-full p-1 gap-1 shadow-2xl border border-white/30 relative overflow-hidden">
          <!-- Indicador de fondo animado -->
          <div 
            class="absolute top-1 bottom-1 rounded-full transition-all duration-700 ease-in-out"
            :style="{
              left: tabActiva === 'asistencias' ? '4px' : '50%',
              width: 'calc(50% - 8px)',
              background: tabActiva === 'asistencias' 
                ? 'linear-gradient(135deg, #3b82f6, #2563eb, #1d4ed8)' 
                : 'linear-gradient(135deg, #8b5cf6, #7c3aed, #6d28d9)',
              boxShadow: tabActiva === 'asistencias'
                ? '0 8px 25px rgba(59, 130, 246, 0.4), 0 4px 15px rgba(37, 99, 235, 0.3), 0 0 20px rgba(59, 130, 246, 0.2)'
                : '0 8px 25px rgba(139, 92, 246, 0.4), 0 4px 15px rgba(124, 58, 237, 0.3), 0 0 20px rgba(139, 92, 246, 0.2)'
            }"
          ></div>
          
          <button 
            @click="cambiarTab('asistencias')" 
            :class="[
              'tab-button-liquid px-12 py-2 font-semibold text-xs rounded-full transition-all duration-700 ease-in-out relative overflow-hidden z-10',
              tabActiva === 'asistencias' 
                ? 'text-white' 
                : 'text-gray-600 hover:text-gray-800'
            ]"
          >
            <span class="relative z-20 font-bold tracking-wide">Asistencias</span>
          </button>
          <button 
            @click="cambiarTab('registros')" 
            :class="[
              'tab-button-liquid px-12 py-2 font-semibold text-xs rounded-full transition-all duration-700 ease-in-out relative overflow-hidden z-10',
              tabActiva === 'registros' 
                ? 'text-white' 
                : 'text-gray-600 hover:text-gray-800'
            ]"
          >
            <span class="relative z-20 font-bold tracking-wide">Actividades</span>
          </button>
        </div>
      </div>

      <!-- Tab de Registros Normales -->
      <div v-show="tabActiva === 'registros'">
        <!-- Título centralizado para Actividades -->
        <div class="text-center mb-1">
          <h2 class="text-sm font-bold text-gray-800 mb-1">Historial de actividades</h2>
          <div class="w-20 h-0.5 bg-gradient-to-r from-purple-400 to-purple-600 mx-auto mb-1"></div>
          <p v-if="userInfo" class="text-xs text-gray-600">
            Registros de: <span class="font-medium text-primary">{{ userInfo.nombre_completo }}</span>
          </p>
        </div>
        
        <div class="flex justify-end items-center mb-1">
          <button @click="cargarRegistros" class="glass-button-refresh text-xs px-2 py-1 flex items-center gap-1">
            <svg :class="['h-2.5 w-2.5 transition-transform duration-500', cargando ? 'animate-spin' : '']" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span class="text-xs">{{ cargando ? 'Cargando...' : 'Actualizar' }}</span>
          </button>
        </div>
      </div>

      <!-- Tab de Asistencias -->
      <div v-show="tabActiva === 'asistencias'">
        <!-- Título centralizado para Asistencias -->
        <div class="text-center mb-1">
          <h2 class="text-sm font-bold text-gray-800 mb-1">Historial de asistencias</h2>
          <div class="w-20 h-0.5 bg-gradient-to-r from-blue-400 to-blue-600 mx-auto mb-1"></div>
          <p v-if="userInfo" class="text-xs text-gray-600">
            Asistencias de: <span class="font-medium text-primary">{{ userInfo.nombre_completo }}</span>
          </p>
        </div>
        
        <div class="flex justify-end items-center mb-1">
          <button @click="cargarAsistencias" class="glass-button-refresh text-xs px-2 py-1 flex items-center gap-1">
            <svg :class="['h-2.5 w-2.5 transition-transform duration-500', cargandoAsistencias ? 'animate-spin' : '']" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span class="text-xs">{{ cargandoAsistencias ? 'Cargando...' : 'Actualizar' }}</span>
          </button>
        </div>
      </div>

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
        <div class="space-y-1.5">
          <div v-for="(registro, index) in registros" :key="index" 
               :class="[
                 'relative overflow-hidden rounded-xl transition-all duration-300 transform hover:scale-[1.01] hover:shadow-lg',
                 'backdrop-filter backdrop-blur-xl border shadow-sm',
                 registro.tipo_actividad === 'campo' 
                   ? 'bg-gradient-to-br from-green-50/80 via-emerald-25/40 to-green-100/60 border-green-200/60 hover:shadow-green-200/50' 
                   : registro.tipo_actividad === 'gabinete'
                   ? 'bg-gradient-to-br from-orange-50/80 via-amber-25/40 to-orange-100/60 border-orange-200/60 hover:shadow-orange-200/50'
                   : 'bg-gradient-to-br from-gray-50/80 via-white/60 to-gray-100/40 border-gray-200/60 hover:shadow-gray-200/50'
               ]"
               style="backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);">
            
            <!-- Efectos decorativos de vidrio líquido más pequeños -->
            <div class="absolute inset-0 bg-gradient-to-br from-white/30 via-transparent to-transparent opacity-60 rounded-xl pointer-events-none"></div>
            <div v-if="registro.tipo_actividad === 'campo'" class="absolute top-0 right-0 w-12 h-12 bg-gradient-to-bl from-green-400/20 to-transparent rounded-full blur-lg"></div>
            <div v-else-if="registro.tipo_actividad === 'gabinete'" class="absolute top-0 right-0 w-12 h-12 bg-gradient-to-bl from-orange-400/20 to-transparent rounded-full blur-lg"></div>
            
            <!-- Borde superior colorido más delgado -->
            <div :class="[
              'absolute top-0 left-0 right-0 h-0.5 rounded-t-xl',
              registro.tipo_actividad === 'campo' 
                ? 'bg-gradient-to-r from-green-500 via-emerald-500 to-green-600' 
                : registro.tipo_actividad === 'gabinete'
                ? 'bg-gradient-to-r from-orange-500 via-amber-500 to-orange-600'
                : 'bg-gradient-to-r from-gray-400 via-gray-500 to-gray-600'
            ]"></div>
            
            <div class="relative z-10 p-2.5">
              <div class="flex gap-2.5">
                <!-- Imagen más pequeña -->
                <div class="w-12 h-12 flex-shrink-0 rounded-lg overflow-hidden relative shadow-md" 
                     :class="{'cursor-pointer': registro.foto_url}" 
                     @click="registro.foto_url && verImagen(registro.foto_url)">
                  <img v-if="registro.foto_url" 
                       :src="registro.foto_url" 
                       class="w-full h-full object-cover transition-transform duration-300 hover:scale-110" 
                       alt="Foto" />
                  <div v-else :class="[
                         'w-full h-full flex items-center justify-center',
                         registro.tipo_actividad === 'campo' 
                           ? 'bg-green-100 text-green-500' 
                           : registro.tipo_actividad === 'gabinete'
                           ? 'bg-orange-100 text-orange-500'
                           : 'bg-gray-100 text-gray-400'
                       ]">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
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
                      Mapa
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
          <div v-for="(asistencia, index) in asistencias" :key="index" class="glass-item border border-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-all">
            <div class="p-2">
              <!-- Información de la fecha -->
              <div class="flex justify-between items-center mb-2">
                <h3 class="text-sm font-medium text-gray-800">{{ formatFecha(asistencia.fecha) }}</h3>
              </div>

              <!-- Diseño dividido: Entrada y Salida en dos columnas -->
              <div class="grid grid-cols-2 gap-2">
                <!-- Columna Entrada -->
                <div class="entrada-bg-light rounded-lg p-2 border-2 shadow-sm">
                  <h4 class="text-xs font-semibold entrada-text-dark mb-1 flex items-center justify-center text-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                    </svg>
                    ENTRADA
                  </h4>
                  
                  <div v-if="asistencia.hora_entrada" class="space-y-2">
                    <div class="text-center">
                      <p class="text-xs font-bold entrada-text">{{ formatHora(asistencia.hora_entrada) }}</p>
                    </div>
                    
                    <div v-if="asistencia.foto_entrada_url" class="flex justify-center">
                      <div class="w-8 h-8 bg-gray-100 rounded overflow-hidden relative cursor-pointer" @click="verImagen(`${API_URL}/${asistencia.foto_entrada_url}`)">
                        <img :src="`${API_URL}/${asistencia.foto_entrada_url}`" class="w-full h-full object-cover" alt="Foto entrada" />
                        <div class="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-20 flex items-center justify-center transition-opacity">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-2 w-2 text-white opacity-0 hover:opacity-100" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                          </svg>
                        </div>
                      </div>
                    </div>
                    
                    <div class="text-center">
                      <button @click="verAsistenciaEnMapa(asistencia, 'entrada')" class="entrada-text hover:entrada-text-dark text-xs font-medium underline">
                        📍 Ver mapa
                      </button>
                    </div>
                    
                    <p class="text-xs text-gray-600 text-center line-clamp-2">{{ asistencia.descripcion_entrada || "Sin descripción" }}</p>
                  </div>
                  
                  <div v-else class="text-center py-4">
                    <p class="text-xs text-gray-400">Sin registro</p>
                  </div>
                </div>

                <!-- Columna Salida -->
                <div :class="[
                  'rounded-lg p-2 border-2 shadow-sm',
                  asistencia.hora_salida 
                    ? 'salida-bg-light' 
                    : 'bg-gray-50 border-gray-200'
                ]">
                  <h4 :class="[
                    'text-xs font-semibold mb-1 flex items-center justify-center text-center',
                    asistencia.hora_salida ? 'salida-text-dark' : 'text-gray-500'
                  ]">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    SALIDA
                  </h4>
                  
                  <div v-if="asistencia.hora_salida" class="space-y-2">
                    <div class="text-center">
                      <p class="text-xs font-bold salida-text">{{ formatHora(asistencia.hora_salida) }}</p>
                    </div>
                    
                    <div v-if="asistencia.foto_salida_url" class="flex justify-center">
                      <div class="w-8 h-8 bg-gray-100 rounded overflow-hidden relative cursor-pointer" @click="verImagen(`${API_URL}/${asistencia.foto_salida_url}`)">
                        <img :src="`${API_URL}/${asistencia.foto_salida_url}`" class="w-full h-full object-cover" alt="Foto salida" />
                        <div class="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-20 flex items-center justify-center transition-opacity">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-2 w-2 text-white opacity-0 hover:opacity-100" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                          </svg>
                        </div>
                      </div>
                    </div>
                    
                    <div class="text-center">
                      <button @click="verAsistenciaEnMapa(asistencia, 'salida')" class="salida-text hover:salida-text-dark text-xs font-medium underline">
                        📍 Ver mapa
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
                    <p class="text-xs text-gray-400 mt-1">Sin registro de salida</p>
                  </div>
                </div>
              </div>

              <!-- Estado incompleto eliminado - ahora se maneja en el recuadro de salida -->
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
    
    <!-- Diálogo de mapa -->
    <div v-if="mapaVisible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-2">
      <div class="glass-modal rounded-lg shadow-xl w-full max-w-sm max-h-[85vh] flex flex-col">
        <div class="p-2 border-b border-gray-200 flex justify-between items-center">
          <h3 class="text-xs font-medium">Ubicación</h3>
          <button @click="mapaVisible = false" class="glass-close-button text-gray-500 hover:text-gray-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="flex-1 min-h-0">
          <div id="detailMap" class="h-full w-full"></div>
        </div>
        <div class="p-2 border-t border-gray-200">
          <button @click="mapaVisible = false" class="glass-button w-full text-xs py-1">Cerrar</button>
        </div>
      </div>
    </div>
    
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
    
    // Procesar asistencias y mostrar información de debug para fechas
    const asistenciasRaw = response.data.asistencias || [];
    
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

// Nueva función para mostrar fecha completa pero más compacta
function formatFechaCompleta(fechaStr) {
  try {
    if (!fechaStr) return '';
    
    const fecha = new Date(fechaStr);
    
    // Verificar que la fecha sea válida
    if (isNaN(fecha.getTime())) {
      console.error('Fecha inválida:', fechaStr);
      return fechaStr;
    }
    
    // Formatear fecha en español mexicano de forma compacta
    return fecha.toLocaleDateString('es-MX', {
      timeZone: 'America/Mexico_City',
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
    
    const fecha = new Date(fechaStr);
    
    // Verificar que la fecha sea válida
    if (isNaN(fecha.getTime())) {
      console.error('Fecha inválida para hora:', fechaStr);
      return fechaStr;
    }
    
    // Mostrar hora en formato AM/PM (igual que las asistencias)
    return fecha.toLocaleTimeString('es-MX', {
      timeZone: 'America/Mexico_City',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
  } catch (e) {
    console.error('Error al formatear hora CDMX:', e, fechaStr);
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
  letter-spacing: 0.025em;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  min-width: 160px;
  text-align: center;
  background: transparent;
  border: none;
  outline: none;
}

.tab-button-liquid:not(.tab-active-liquid):hover {
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  transform: translateY(-1px);
}

/* Animación suave para el contenedor de pestañas */
.glass-card .flex.bg-gradient-to-r {
  position: relative;
  overflow: hidden;
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
</style>
