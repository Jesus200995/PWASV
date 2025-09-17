<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 flex flex-col p-2 sm:p-3 relative overflow-hidden">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-emerald-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-teal-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>

    <div class="page-container w-full max-w-lg mx-auto relative z-10 pt-0 pb-1 space-y-2">
      <!-- Botones de selección de sección -->
      <div v-if="!modoAsistencia" class="glass-card">
        <div class="text-center mb-3">
          <h1 class="text-xl font-bold text-gray-800 mb-2 modern-title">Panel de Registro</h1>
          <div class="green-line mx-auto mb-2"></div>
          <p class="text-xs text-gray-500 mb-3">Selecciona el tipo de registro que deseas realizar</p>
          
          <!-- Botones de navegación entre secciones -->
          <div class="flex gap-2 section-nav-container p-1 rounded-full">
            <button
              @click="seccionActiva = 'asistencia'"
              :class="[
                'section-nav-button flex-1 px-4 py-2 text-sm font-medium rounded-full transition-all duration-300',
                seccionActiva === 'asistencia' 
                  ? 'active text-white shadow-lg' 
                  : 'text-gray-600 hover:bg-white/30'
              ]"
              :style="seccionActiva === 'asistencia' ? 'background-color: rgb(30, 144, 255);' : ''"
            >
              <div class="flex items-center justify-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>Asistencia</span>
              </div>
            </button>
            
            <button
              @click="(!entradaMarcada || salidaMarcada) ? mostrarModalActividadesBloqueadas() : (seccionActiva = 'actividades')"
              :disabled="false"
              :class="[
                'section-nav-button flex-1 px-4 py-2 text-sm font-medium rounded-full transition-all duration-300 relative',
                seccionActiva === 'actividades' && entradaMarcada && !salidaMarcada
                  ? 'active text-white shadow-lg' 
                  : (!entradaMarcada || salidaMarcada)
                    ? 'bg-gray-300 text-gray-500 cursor-pointer'
                    : 'text-gray-600 hover:bg-white/30'
              ]"
              :style="seccionActiva === 'actividades' && entradaMarcada && !salidaMarcada ? 'background-color: rgb(147, 51, 234);' : ''"
            >
              <div class="flex items-center justify-center space-x-2">
                <!-- Icono de candado cuando está bloqueado -->
                <svg v-if="!entradaMarcada || salidaMarcada" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                <!-- Icono normal de actividades cuando está habilitado -->
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                <span>Actividades</span>
              </div>
            </button>
          </div>
        </div>
      </div>

      <!-- Sistema de Asistencia Integrado -->
      <div v-if="seccionActiva === 'asistencia' || modoAsistencia" class="glass-card relative">
        <!-- Icono de regresar (solo visible en modo asistencia) -->
        <button 
          v-if="modoAsistencia"
          @click="cancelarAsistencia"
          class="absolute top-3 left-3 w-8 h-8 sm:w-9 sm:h-9 bg-white rounded-full shadow-lg border border-gray-200 flex items-center justify-center hover:bg-gray-50 active:scale-95 transition-all duration-200 z-20"
          title="Regresar"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 sm:h-5 sm:w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        
        <div class="text-center mb-2">
          <h2 class="text-lg font-bold text-gray-800 mb-1 modern-title">Registra tu asistencia</h2>
          <div class="green-line mx-auto mb-1"></div>
          <p class="text-xs text-gray-500">
            {{ modoAsistencia ? 'Completa los datos para ' + (tipoAsistencia === 'entrada' ? 'marcar entrada' : 'marcar salida') : 'Marca tu entrada y salida del día' }}
          </p>
        </div>

        <!-- Botones de Asistencia (solo visibles cuando no está en modo asistencia) -->
        <div v-if="!modoAsistencia" class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-2">
        <!-- Botón Marcar Entrada -->
        <button
          @click="mostrarModalEntrada"
          :disabled="entradaMarcada || verificandoAsistencia"
          class="relative overflow-hidden rounded-xl transition-all duration-300 transform min-h-[80px] w-full flex flex-col items-center justify-center p-2"
          :class="{
            'text-white shadow-lg hover:scale-105 active:scale-95': !entradaMarcada && !verificandoAsistencia,
            'bg-gradient-to-r from-gray-100 to-gray-200 text-gray-500 cursor-not-allowed': entradaMarcada || verificandoAsistencia
          }"
          :style="!entradaMarcada && !verificandoAsistencia ? 'background-color: rgb(30, 144, 255); box-shadow: 0 4px 12px rgba(30, 144, 255, 0.3);' : ''"
          @mouseover="!entradaMarcada && !verificandoAsistencia && ($event.target.style.backgroundColor = 'rgb(25, 130, 230)')"
          @mouseout="!entradaMarcada && !verificandoAsistencia && ($event.target.style.backgroundColor = 'rgb(30, 144, 255)')"
        >
          <div v-if="verificandoAsistencia" class="absolute inset-0 bg-white bg-opacity-20 flex items-center justify-center rounded">
            <div class="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-current"></div>
          </div>
          
          <!-- Estado: No marcada - Activo -->
          <template v-if="!entradaMarcada && !verificandoAsistencia">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mb-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <span class="font-semibold text-sm">Marcar Entrada</span>
            <span class="text-xs opacity-90">Registra tu llegada</span>
          </template>
          
          <!-- Estado: Marcada - Completada -->
          <template v-else-if="entradaMarcada">
            <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center mb-0.5">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <span class="font-semibold text-sm text-gray-700">Entrada Registrada</span>
            <span class="text-xs text-gray-500">
              <span v-if="asistenciaHoy && asistenciaHoy.entrada">
                {{ formatearHora(asistenciaHoy.entrada) }}
              </span>
              <span v-else-if="datosEntrada.hora">
                {{ datosEntrada.hora }}
              </span>
            </span>
            <span class="text-xs text-blue-600 font-medium">✓ Completada</span>
          </template>
        </button>

        <!-- Botón Marcar Salida -->
        <button
          @click="mostrarModalSalida"
          :disabled="!entradaMarcada || salidaMarcada || verificandoAsistencia"
          class="relative overflow-hidden rounded-xl transition-all duration-300 transform min-h-[80px] w-full flex flex-col items-center justify-center p-2"
          :class="{
            'text-white shadow-lg hover:scale-105 active:scale-95': entradaMarcada && !salidaMarcada && !verificandoAsistencia,
            'bg-gradient-to-r from-gray-100 to-gray-200 text-gray-500 cursor-not-allowed': !entradaMarcada || salidaMarcada || verificandoAsistencia
          }"
          :style="entradaMarcada && !salidaMarcada && !verificandoAsistencia ? 'background-color: rgb(220, 20, 60); box-shadow: 0 4px 12px rgba(220, 20, 60, 0.3);' : ''"
          @mouseover="entradaMarcada && !salidaMarcada && !verificandoAsistencia && ($event.target.style.backgroundColor = 'rgb(200, 15, 55)')"
          @mouseout="entradaMarcada && !salidaMarcada && !verificandoAsistencia && ($event.target.style.backgroundColor = 'rgb(220, 20, 60)')"
        >
          <div v-if="verificandoAsistencia" class="absolute inset-0 bg-white bg-opacity-20 flex items-center justify-center rounded">
            <div class="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-current"></div>
          </div>
          
          <!-- Estado: Activo para marcar salida -->
          <template v-if="entradaMarcada && !salidaMarcada && !verificandoAsistencia">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mb-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <span class="font-semibold text-sm">Marcar Salida</span>
            <span class="text-xs opacity-90">Registra tu salida</span>
          </template>
          
          <!-- Estado: Bloqueado (sin entrada) -->
          <template v-else-if="!entradaMarcada">
            <div class="w-8 h-8 bg-gray-400 rounded-full flex items-center justify-center mb-0.5">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <span class="font-semibold text-sm text-gray-600">Marcar Salida</span>
            <span class="text-xs text-gray-500">Primero marca tu entrada</span>
            <div class="flex items-center mt-1">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-amber-600 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <span class="text-xs text-amber-600 font-medium">Bloqueado</span>
            </div>
          </template>
          
          <!-- Estado: Salida completada -->
          <template v-else-if="salidaMarcada">
            <div class="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center mb-0.5">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <span class="font-semibold text-sm text-gray-700">Salida Registrada</span>
            <span class="text-xs text-gray-500">
              <span v-if="asistenciaHoy && asistenciaHoy.salida">
                {{ formatearHora(asistenciaHoy.salida) }}
              </span>
              <span v-else-if="datosSalida.hora">
                {{ datosSalida.hora }}
              </span>
            </span>
            <span class="text-xs text-red-600 font-medium">✓ Completada</span>
          </template>
        </button>
      </div>

        <!-- Aviso amigable sobre registro de asistencia -->
        <div v-if="!modoAsistencia" class="text-center mb-2 relative">
          <!-- Ícono suave en esquina izquierda (más pequeño) -->
          <div class="absolute -left-0.5 -top-0.5 w-4 h-4 bg-gradient-to-br from-rose-300/80 via-red-300/70 to-rose-400/60 rounded-full shadow-md backdrop-blur-sm border border-rose-200/50 z-30 overflow-hidden">
            <!-- Efecto vidrio líquido en círculo -->
            <div class="absolute inset-0 bg-gradient-to-br from-white/40 via-transparent to-rose-100/20 pointer-events-none rounded-full"></div>
            
            <!-- Reflejo líquido superior -->
            <div class="absolute top-0 left-0 right-0 h-1/2 bg-gradient-to-b from-white/50 to-transparent rounded-full"></div>
            
            <!-- Ondas líquidas (más pequeñas) -->
            <div class="absolute inset-0 opacity-30">
              <div class="absolute top-0.5 left-0.5 w-1 h-1 bg-white/60 rounded-full animate-ping"></div>
            </div>
            
            <!-- Ícono suave (más pequeño) -->
            <div class="relative z-10 w-full h-full flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 text-rose-700/80 drop-shadow-sm" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          
          <!-- Contenedor principal rediseñado -->
          <div class="relative bg-gradient-to-br from-red-900 via-red-950 to-black backdrop-blur-sm rounded-xl shadow-xl border border-red-800/30 overflow-hidden mx-2">
            <!-- Borde superior rojo elegante -->
            <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-red-500 via-red-400 to-red-500"></div>
            
            <!-- Contenido principal -->
            <div class="relative p-4">
              <!-- Icono y encabezado -->
              <div class="flex items-center justify-center mb-3">
                <div class="flex items-center space-x-2">
                  <div class="w-7 h-7 rounded-full bg-red-500 flex items-center justify-center shadow-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.718 9.168-4.309M6 15a2 2 0 002 2h1.832c4.1 0 7.625 1.718 9.168 4.309" />
                    </svg>
                  </div>
                  <span class="font-semibold text-red-100 tracking-wide uppercase" style="font-size: 0.6rem;">Importante</span>
                </div>
              </div>
              
              <!-- Mensaje principal -->
              <div class="text-center space-y-1">
                <h3 class="text-2xs font-semibold text-white leading-tight" style="font-size: 0.65rem;">
                  Marcar entrada es necesario para usar actividades
                </h3>
                <p class="text-2xs text-red-200 font-medium" style="font-size: 0.6rem;">
                  Al marcar salida se finaliza el acceso del día
                </p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Mensaje de estado de asistencia -->
        <div v-if="mensajeAsistencia && !modoAsistencia" class="text-center mb-3">
          <transition name="fade-slide">
            <div 
              class="inline-flex items-center px-2 py-1.5 rounded-lg text-xs font-medium shadow-sm border backdrop-blur-sm"
              :class="{
                'bg-green-50 text-green-700 border-green-200': mensajeAsistencia.includes('éxito') || mensajeAsistencia.includes('registrada') || mensajeAsistencia.includes('Sincronización exitosa'),
                'bg-red-50 text-red-700 border-red-200': mensajeAsistencia.includes('Error') || mensajeAsistencia.includes('error'),
                'bg-blue-50 text-blue-700 border-blue-200': mensajeAsistencia.includes('Sincronización') || mensajeAsistencia.includes('progreso'),
                'bg-yellow-50 text-yellow-700 border-yellow-200': mensajeAsistencia.includes('Ya') || mensajeAsistencia.includes('offline')
              }"
            >
              <svg v-if="mensajeAsistencia.includes('éxito') || mensajeAsistencia.includes('registrada') || mensajeAsistencia.includes('Sincronización exitosa')" xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
              </svg>
              <svg v-else-if="mensajeAsistencia.includes('Error') || mensajeAsistencia.includes('error')" xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
              </svg>
              <svg v-else-if="mensajeAsistencia.includes('Sincronización') || mensajeAsistencia.includes('progreso')" xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 mr-1.5 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span class="text-xs">{{ mensajeAsistencia }}</span>
            </div>
          </transition>
        </div>

        <!-- Formulario de Asistencia (solo visible en modo asistencia) -->
        <div v-if="modoAsistencia" class="mt-6 border-t border-gray-200 pt-6">
          <div class="text-center mb-4">
            <h2 class="text-lg font-bold text-gray-800 mb-2"
                :class="tipoAsistencia === 'entrada' ? 'entrada-title' : 'salida-title'">
              {{ tipoAsistencia === 'entrada' ? 'ENTRADA' : 'SALIDA' }}
            </h2>
            <p class="text-xs text-gray-500">Completa todos los datos requeridos</p>
          </div>
          
          <!-- Info del usuario -->
          <div class="bg-primary/10 rounded-lg p-2 mb-6">
            <div class="flex items-center">
              <div class="relative w-8 h-8 bg-gradient-to-br from-green-700 via-green-800 to-green-900 rounded-full shadow-xl backdrop-blur-xl border border-white/25 overflow-hidden flex items-center justify-center mr-2">
                <!-- Efecto vidrio en círculo de iniciales -->
                <div class="absolute inset-0 bg-gradient-to-br from-white/15 via-transparent to-black/10 pointer-events-none rounded-full"></div>
                
                <!-- Reflejo superior del círculo -->
                <div class="absolute top-0 left-0 right-0 h-1/2 bg-gradient-to-b from-white/20 to-transparent rounded-full"></div>
                
                <!-- Iniciales con efecto mejorado -->
                <span class="text-white text-xs font-bold drop-shadow-lg filter brightness-110 relative z-10">{{ getUserInitials }}</span>
              </div>
              <div>
                <p class="font-medium text-primary text-sm">{{ user.nombre_completo }}</p>
                <p class="text-xs text-gray-500">{{ user.cargo }}</p>
              </div>
            </div>
          </div>

          <!-- Paso 1: Ubicación -->
          <div class="mb-4">
            <div class="flex items-center justify-between mb-2">
              <h3 class="text-base font-semibold text-gray-800">1. Ubicación</h3>
              <span v-if="latitud && longitud" 
                :class="tipoAsistencia === 'entrada' ? 'text-blue-600' : 'text-green-600'"
                class="text-xs">✓ Completado</span>
            </div>
            
            <!-- Botón de ubicación circular con diseño moderno -->
            <div class="location-container-circular">
              <button
                type="button"
                @click="getUbicacion"
                :disabled="obteniendoUbicacion"
                class="location-button-circular relative flex flex-col items-center justify-center w-28 h-28 sm:w-32 sm:h-32 font-medium text-white rounded-full shadow-2xl transform transition-all duration-500 hover:scale-110 active:scale-95"
                :class="{
                  'opacity-50 cursor-not-allowed': obteniendoUbicacion,
                  'location-button-success-circular': latitud && longitud && !obteniendoUbicacion
                }"
              >
                <!-- Spinner de carga -->
                <div v-if="obteniendoUbicacion" class="flex flex-col items-center">
                  <div class="animate-spin rounded-full h-6 w-6 border-t-3 border-b-3 border-white mb-1"></div>
                  <span class="text-xs font-normal tracking-normal text-center leading-tight">Ubicando...</span>
                </div>
                
                <!-- Estado completado -->
                <div v-else-if="latitud && longitud" class="flex flex-col items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 mb-1 text-emerald-800 glass-icon-circular" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span class="text-xs font-medium tracking-normal glass-text-circular text-center leading-tight">Ubicación Obtenida</span>
                </div>
                
                <!-- Estado inicial -->
                <div v-else class="flex flex-col items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 mb-1 text-white location-icon-circular" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span class="text-xs font-medium tracking-normal text-white location-text-circular text-center leading-tight">Obtener Ubicación</span>
                </div>
              </button>

              <!-- Coordenadas pegadas al botón circular -->
              <div v-if="latitud && longitud" class="coordinates-display-circular">
                <div class="coordinates-grid-circular">
                  <div class="coordinate-item-circular">
                    <span class="coordinate-label-circular">Lat:</span>
                    <span class="coordinate-value-circular">{{ latitud }}</span>
                  </div>
                  <div class="coordinate-item-circular">
                    <span class="coordinate-label-circular">Lon:</span>
                    <span class="coordinate-value-circular">{{ longitud }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Paso 2: Foto -->
          <div class="mb-4">
            <div class="flex items-center justify-between mb-2">
              <h3 class="text-base font-semibold text-gray-800">2. Foto</h3>
              <span v-if="foto" 
                :class="tipoAsistencia === 'entrada' ? 'text-blue-600' : 'text-green-600'"
                class="text-xs">✓ Completado</span>
            </div>
            
            <div class="flex items-center justify-center w-full">
              <label class="flex flex-col w-full h-24 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50 active:bg-gray-100">
                <div v-if="!foto" class="flex flex-col items-center justify-center pt-5">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <p class="pt-1 text-xs text-gray-400">Selecciona una foto</p>
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
          <div class="mb-4">
            <div class="flex items-center justify-between mb-2">
              <h3 class="text-base font-semibold text-gray-800">3. Descripción/Notas</h3>
              <span v-if="descripcion.trim()" 
                :class="tipoAsistencia === 'entrada' ? 'text-blue-600' : 'text-green-600'"
                class="text-xs">✓ Completado</span>
            </div>
            
            <textarea
              v-model="descripcion"
              rows="2"
              class="glass-input w-full text-xs"
              :placeholder="'Describe el lugar donde ' + (tipoAsistencia === 'entrada' ? 'inicias' : 'terminas') + ' tu jornada...'"
            ></textarea>
          </div>

          <!-- Botones de acción -->
          <div class="flex gap-2">
            <button
              @click="cancelarAsistencia"
              class="glass-button-secondary flex-1 text-xs py-2"
            >
              Cancelar
            </button>
            
            <button
              @click="confirmarAsistencia"
              :disabled="!puedeEnviarAsistencia || enviandoAsistencia"
              class="flex-1 relative text-xs py-2"
              :class="[
                'glass-button',
                tipoAsistencia === 'entrada' ? 'glass-button-entrada' : 'glass-button-salida',
                {'opacity-50 cursor-not-allowed': !puedeEnviarAsistencia || enviandoAsistencia}
              ]"
            >
              <div v-if="enviandoAsistencia" class="absolute inset-0 bg-white bg-opacity-20 flex items-center justify-center rounded">
                <div class="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white"></div>
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
      </div>

    <!-- Modal de confirmación para entrada -->
    <ConfirmModal 
      :show="showEntradaModal" 
      title="Registrar Entrada"
      :message="entradaModalMessage"
      type="confirm"
      :showConfirm="true"
      confirmText="Registrar Entrada"
      cancelText="Cancelar"
      @close="closeEntradaModal"
      @confirm="confirmarEntradaModal"
    />
    
    <!-- Modal de confirmación para salida -->
    <ConfirmModal 
      :show="showSalidaModal" 
      title="Registrar Salida"
      :message="salidaModalMessage"
      type="error"
      :showConfirm="true"
      confirmText="Registrar Salida"
      cancelText="Cancelar"
      @close="closeSalidaModal"
      @confirm="confirmarSalidaModal"
    />

    <!-- Modal de información para actividades bloqueadas -->
    <ConfirmModal 
      :show="showActividadesBloqueadasModal" 
      title=""
      :message="actividadesBloqueadasModalMessage"
      type="info"
      :showConfirm="false"
      cancelText="Entendido"
      @close="closeActividadesBloqueadasModal"
    />

    <!-- Formulario de registro normal (solo cuando no está en modo asistencia) -->
    <div v-if="seccionActiva === 'actividades' && !modoAsistencia" class="glass-card">
      <!-- Mensaje de estado de actividades bloqueadas -->
      <div v-if="!entradaMarcada || salidaMarcada" class="mb-4">
        <div class="bg-yellow-100 border-l-4 border-yellow-500 p-3 rounded-lg">
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-600 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
            <div>
              <h3 class="text-sm font-medium text-yellow-800">Registro de actividades bloqueado</h3>
              <p class="text-xs text-yellow-700 mt-1">
                <span v-if="!entradaMarcada">Debes marcar tu entrada primero para registrar actividades.</span>
                <span v-else-if="salidaMarcada">Has marcado tu salida. No puedes registrar más actividades hoy.</span>
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="text-center mb-3">
        <h2 class="text-lg font-bold text-gray-800 mb-1 modern-title"
            :class="{ 'opacity-50': !entradaMarcada || salidaMarcada }">
          Registra tus actividades
        </h2>
        <!-- Línea tipo marcatextos -->
        <div class="green-line mx-auto mb-1" :class="{ 'opacity-50': !entradaMarcada || salidaMarcada }"></div>
        <p class="text-xs text-gray-500" :class="{ 'opacity-50': !entradaMarcada || salidaMarcada }">
          <span v-if="entradaMarcada && !salidaMarcada">Captura tu ubicación actual para el registro</span>
          <span v-else-if="!entradaMarcada">Marca tu entrada primero</span>
          <span v-else>Registro de actividades finalizado</span>
        </p>
      </div>
      
      <!-- Info del usuario -->
      <div class="bg-primary/10 rounded-lg p-2 mb-6">
        <div class="flex items-center">
          <div class="relative w-8 h-8 bg-gradient-to-br from-green-700 via-green-800 to-green-900 rounded-full shadow-xl backdrop-blur-xl border border-white/25 overflow-hidden flex items-center justify-center mr-2">
            <!-- Efecto vidrio en círculo de iniciales -->
            <div class="absolute inset-0 bg-gradient-to-br from-white/15 via-transparent to-black/10 pointer-events-none rounded-full"></div>
            
            <!-- Reflejo superior del círculo -->
            <div class="absolute top-0 left-0 right-0 h-1/2 bg-gradient-to-b from-white/20 to-transparent rounded-full"></div>
            
            <!-- Iniciales con efecto mejorado -->
            <span class="text-white text-xs font-bold drop-shadow-lg filter brightness-110 relative z-10">{{ getUserInitials }}</span>
          </div>
          <div>
            <p class="font-medium text-primary text-sm">{{ user.nombre_completo }}</p>
            <p class="text-xs text-gray-500">{{ user.cargo }}</p>
          </div>
        </div>
      </div>

      <form @submit.prevent="enviarRegistro" :class="{ 'opacity-50 pointer-events-none': !entradaMarcada || salidaMarcada }">
        <!-- Botón para obtener ubicación circular para actividades -->
        <div class="location-container-circular mb-3 flex justify-center">
          <button
            type="button"
            @click="getUbicacionRegistro"
            :disabled="!entradaMarcada || salidaMarcada"
            class="location-button-circular relative flex flex-col items-center justify-center w-28 h-28 sm:w-32 sm:h-32 font-medium text-white rounded-full shadow-2xl transform transition-all duration-500 hover:scale-110 active:scale-95"
            :class="{
              'location-button-success-circular': latitudRegistro && longitudRegistro && entradaMarcada && !salidaMarcada,
              'opacity-50 cursor-not-allowed': !entradaMarcada || salidaMarcada
            }"
          >
            <!-- Estado completado -->
            <div v-if="latitudRegistro && longitudRegistro && entradaMarcada && !salidaMarcada" class="flex flex-col items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 mb-1 text-emerald-800 glass-icon-circular" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span class="text-xs font-medium tracking-normal glass-text-circular text-center leading-tight">Ubicación Obtenida</span>
            </div>
            
            <!-- Estado bloqueado -->
            <div v-else-if="!entradaMarcada || salidaMarcada" class="flex flex-col items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 mb-1 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 15v2m0 0v2m0-2h2m-2 0H9m12-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span class="text-xs font-medium text-gray-400 text-center leading-tight">
                <span v-if="!entradaMarcada">Marca Entrada Primero</span>
                <span v-else>Actividades Bloqueadas</span>
              </span>
            </div>
            
            <!-- Estado inicial -->
            <div v-else class="flex flex-col items-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-7 w-7 mb-1 text-white location-icon-circular"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2.5"
                  d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                />
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2.5"
                  d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                />
              </svg>
              <span class="text-xs font-medium tracking-normal text-white location-text-circular text-center leading-tight">Obtener Ubicación</span>
            </div>
          </button>

          <!-- Coordenadas pegadas al botón circular -->
          <div v-if="latitudRegistro && longitudRegistro && entradaMarcada && !salidaMarcada" class="coordinates-display-circular">
            <div class="coordinates-grid-circular">
              <div class="coordinate-item-circular">
                <span class="coordinate-label-circular">Lat:</span>
                <span class="coordinate-value-circular">{{ latitudRegistro }}</span>
              </div>
              <div class="coordinate-item-circular">
                <span class="coordinate-label-circular">Lon:</span>
                <span class="coordinate-value-circular">{{ longitudRegistro }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Tipo de Actividad - Diseño Vidrio Líquido Compacto -->
        <div class="mb-3">
          <label class="block text-xs font-medium text-gray-700 mb-2 flex items-center"
                 :class="{ 'text-gray-400': !entradaMarcada || salidaMarcada }">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1.5 text-green-600" :class="{ 'text-gray-400': !entradaMarcada || salidaMarcada }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
            Tipo de Actividad <span class="text-red-500 text-sm">*</span>
          </label>
          
          <!-- Contenedor de opciones con estilo vidrio líquido compacto -->
          <div class="relative">
            <div class="grid grid-cols-2 gap-2">
              <!-- Opción Campo -->
              <div 
                @click="entradaMarcada && !salidaMarcada && (tipoActividad = 'campo')"
                :class="[
                  'relative overflow-hidden rounded-xl p-3 cursor-pointer transition-all duration-300 transform hover:scale-[1.02] border',
                  entradaMarcada && !salidaMarcada ? 'cursor-pointer' : 'cursor-not-allowed opacity-50',
                  tipoActividad === 'campo' ? 
                    'bg-gradient-to-br from-green-600/25 via-green-700/20 to-green-800/25 border-green-600/70 shadow-lg shadow-green-600/20' : 
                    'bg-gradient-to-br from-gray-50/80 via-white/60 to-gray-100/40 border-gray-200/60 hover:border-green-300/40 hover:from-green-50/30 hover:via-green-25/20 hover:to-green-50/15'
                ]"
                style="backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);"
              >
                <!-- Efecto de vidrio líquido sutil -->
                <div class="absolute inset-0 bg-gradient-to-br from-white/20 via-transparent to-transparent opacity-60 rounded-xl"></div>
                <div class="absolute bottom-0 right-0 w-12 h-12 bg-gradient-to-tl from-green-600/25 to-transparent rounded-full blur-lg"></div>
                
                <div class="relative z-10 text-center">
                  <div class="flex justify-center mb-1.5">
                    <div :class="[
                      'w-8 h-8 rounded-full flex items-center justify-center transition-all duration-300',
                      tipoActividad === 'campo' ? 
                        'bg-green-700 text-white shadow-md shadow-green-700/40' : 
                        'bg-gray-100 text-gray-500 border border-gray-200'
                    ]">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                      </svg>
                    </div>
                  </div>
                  <h3 :class="[
                    'font-medium text-xs mb-0.5 transition-colors duration-300',
                    tipoActividad === 'campo' ? 'text-green-900' : 'text-gray-600'
                  ]">Campo</h3>
                  <p :class="[
                    'text-xs leading-tight transition-colors duration-300',
                    tipoActividad === 'campo' ? 'text-green-800' : 'text-gray-400'
                  ]">Trabajo en terreno</p>
                </div>
                
                <!-- Indicador de selección pequeño -->
                <div v-if="tipoActividad === 'campo'" class="absolute top-1.5 right-1.5">
                  <div class="w-4 h-4 bg-green-700 rounded-full flex items-center justify-center shadow-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </div>
              </div>

              <!-- Opción Gabinete -->
              <div 
                @click="entradaMarcada && !salidaMarcada && (tipoActividad = 'gabinete')"
                :class="[
                  'relative overflow-hidden rounded-xl p-3 cursor-pointer transition-all duration-300 transform hover:scale-[1.02] border',
                  entradaMarcada && !salidaMarcada ? 'cursor-pointer' : 'cursor-not-allowed opacity-50',
                  tipoActividad === 'gabinete' ? 
                    'bg-gradient-to-br from-orange-600/25 via-red-600/20 to-orange-700/25 border-orange-600/70 shadow-lg shadow-orange-600/20' : 
                    'bg-gradient-to-br from-gray-50/80 via-white/60 to-gray-100/40 border-gray-200/60 hover:border-orange-300/40 hover:from-orange-50/30 hover:via-red-25/20 hover:to-orange-50/15'
                ]"
                style="backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);"
              >
                <!-- Efecto de vidrio líquido sutil -->
                <div class="absolute inset-0 bg-gradient-to-br from-white/20 via-transparent to-transparent opacity-60 rounded-xl"></div>
                <div class="absolute bottom-0 right-0 w-12 h-12 bg-gradient-to-tl from-orange-600/25 to-transparent rounded-full blur-lg"></div>
                
                <div class="relative z-10 text-center">
                  <div class="flex justify-center mb-1.5">
                    <div :class="[
                      'w-8 h-8 rounded-full flex items-center justify-center transition-all duration-300',
                      tipoActividad === 'gabinete' ? 
                        'bg-orange-700 text-white shadow-md shadow-orange-700/40' : 
                        'bg-gray-100 text-gray-500 border border-gray-200'
                    ]">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                  </div>
                  <h3 :class="[
                    'font-medium text-xs mb-0.5 transition-colors duration-300',
                    tipoActividad === 'gabinete' ? 'text-orange-900' : 'text-gray-600'
                  ]">Gabinete</h3>
                  <p :class="[
                    'text-xs leading-tight transition-colors duration-300',
                    tipoActividad === 'gabinete' ? 'text-orange-800' : 'text-gray-400'
                  ]">Trabajo de oficina</p>
                </div>
                
                <!-- Indicador de selección pequeño -->
                <div v-if="tipoActividad === 'gabinete'" class="absolute top-1.5 right-1.5">
                  <div class="w-4 h-4 bg-orange-700 rounded-full flex items-center justify-center shadow-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Mensaje de error si no está seleccionado -->
            <div v-if="!tipoActividad && (entradaMarcada && !salidaMarcada)" class="mt-1.5 text-center">
              <p class="text-xs text-red-500 font-medium animate-pulse">Por favor selecciona el tipo de actividad</p>
            </div>
          </div>
        </div>

        <!-- Input de archivo para foto -->
        <div class="mb-3">
          <label class="block text-sm font-medium text-gray-700 mb-2" 
                 :class="{ 'text-gray-400': !entradaMarcada || salidaMarcada }">Foto</label>
          <div class="flex items-center justify-center w-full">
            <label class="flex flex-col w-full h-32 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50 active:bg-gray-100"
                   :class="{ 'opacity-50 cursor-not-allowed pointer-events-none': !entradaMarcada || salidaMarcada }">
              <div v-if="!fotoRegistro" class="flex flex-col items-center justify-center pt-7">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="w-8 h-8 text-gray-400"
                  :class="{ 'text-gray-300': !entradaMarcada || salidaMarcada }"
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
                <p class="pt-1 text-sm text-gray-400" 
                   :class="{ 'text-gray-300': !entradaMarcada || salidaMarcada }">
                  <span v-if="entradaMarcada && !salidaMarcada">Selecciona una foto</span>
                  <span v-else-if="!entradaMarcada">Marca entrada primero</span>
                  <span v-else>Función bloqueada</span>
                </p>
              </div>
              <div v-else class="flex items-center justify-center h-full">
                <img :src="fotoRegistro" class="h-full object-contain" />
              </div>
              <input
                type="file"
                accept="image/*"
                @change="onFileChangeRegistro"
                :disabled="!entradaMarcada || salidaMarcada"
                class="hidden"
                ref="fileInputRegistro"
              />
            </label>
          </div>
        </div>

        <!-- Descripción -->
        <div class="mb-3">
          <label for="descripcionRegistro" class="block text-sm font-medium text-gray-700 mb-2"
                 :class="{ 'text-gray-400': !entradaMarcada || salidaMarcada }">Descripción</label>
          <textarea
            v-model="descripcionRegistro"
            id="descripcionRegistro"
            rows="3"
            :disabled="!entradaMarcada || salidaMarcada"
            class="glass-input w-full"
            :class="{ 'opacity-50': !entradaMarcada || salidaMarcada }"
            :placeholder="entradaMarcada && !salidaMarcada ? 'Describe el lugar o añade notas...' : !entradaMarcada ? 'Marca entrada primero...' : 'Función bloqueada...'"
          ></textarea>
        </div>

        <!-- Botón enviar -->
        <button
          type="submit"
          :disabled="!latitudRegistro || !longitudRegistro || !fotoRegistro || !tipoActividad || enviando || !entradaMarcada || salidaMarcada"
          :class="['glass-button-registro w-full', (!latitudRegistro || !longitudRegistro || !fotoRegistro || !tipoActividad || enviando || !entradaMarcada || salidaMarcada) ? 'opacity-50 cursor-not-allowed' : '']"
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
          <span v-else-if="!entradaMarcada">Marca entrada primero</span>
          <span v-else-if="salidaMarcada">Actividades finalizadas</span>
          <span v-else>Guardar registro</span>
        </button>
      </form>
    </div>

    <!-- Mensajes de error/información -->
    <transition name="fade">
      <div
        v-if="error"
        :class="isInfoMessage ? 
          'mb-2 bg-green-50 border-l-3 border-green-500 text-green-700 p-2 rounded shadow-sm' : 
          'mb-2 bg-red-100 border-l-3 border-red-500 text-red-700 p-2 rounded'"
        role="alert"
      >
        <p class="font-semibold text-xs flex items-center">
          <svg v-if="isInfoMessage" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          {{ isInfoMessage ? 'Info' : 'Error' }}
        </p>
        <p class="text-xs mt-0.5">{{ error }}</p>
      </div>
    </transition>

    <!-- Historial reciente (solo cuando no está en modo asistencia y sección actividades está activa) -->
    <div v-if="historial.length > 0 && !modoAsistencia && seccionActiva === 'actividades'" class="glass-card">
      <h3 class="text-base font-semibold text-gray-800 mb-2 modern-title">Registros recientes</h3>
      <div class="green-line mb-3"></div>
      <div class="space-y-2">
        <div
          v-for="(r, i) in historial.slice(0, 3)"
          :key="i"
          class="border border-gray-200 rounded-lg p-2 hover:shadow-md transition-shadow relative"
          :class="{ 'border-orange-300 bg-orange-50': r.offline }"
        >
          <!-- Indicador de estado offline -->
          <div v-if="r.offline" class="absolute top-1 right-1">
            <div class="flex items-center text-orange-600 text-xs">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Pendiente
            </div>
          </div>
          
          <div class="flex">
            <div class="w-16 h-16 bg-gray-100 rounded overflow-hidden mr-2">
              <img
                v-if="r.foto"
                :src="r.foto"
                class="w-full h-full object-cover"
              />
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-xs text-gray-500">{{ r.fecha }}</p>
              <p class="text-xs text-gray-800 truncate">
                {{ r.descripcion || 'Sin descripción' }}
              </p>
              <!-- Nuevo: mostrar tipo de actividad -->
              <p v-if="r.tipo_actividad" class="text-xs font-medium">
                <span v-if="r.tipo_actividad === 'campo'" class="text-green-600">🌾 Actividad de Campo</span>
                <span v-else class="text-orange-600">🏢 Actividad de Gabinete</span>
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
          class="text-sm text-primary hover:underline glass-link"
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
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { API_URL, checkInternetConnection, getOfflineMessage } from '../utils/network.js';
import Modal from '../components/Modal.vue';
import ConfirmModal from '../components/ConfirmModal.vue';
import asistenciasService from '../services/asistenciasService.js';
import offlineService from '../services/offlineService.js';
import syncService from '../services/syncService.js';
import geoLocationService from '../services/geoLocationService.js';
import { obtenerUbicacionSimple } from '../services/geoLocationSimple.js';
import { compressImage, blobToFile } from '../utils/imageCompressor.js';

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
const tipoActividad = ref(""); // Nuevo: campo para tipo de actividad

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

// Variables para modales de confirmación
const showEntradaModal = ref(false);
const showSalidaModal = ref(false);
const showActividadesBloqueadasModal = ref(false);
const entradaModalMessage = ref('');
const salidaModalMessage = ref('');
const actividadesBloqueadasModalMessage = ref('');

// Control de secciones activas
const seccionActiva = ref('asistencia'); // 'asistencia' o 'actividades'

// Función para obtener timestamp CDMX exacto (igual que en la barra verde)
function obtenerTimestampCDMX() {
  const now = new Date();
  
  // Configurar para zona horaria de CDMX (America/Mexico_City)
  const formatter = new Intl.DateTimeFormat('sv-SE', {
    timeZone: 'America/Mexico_City',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    fractionalSecondDigits: 3
  });
  
  // Obtener la fecha/hora formateada para CDMX
  const fechaHoraCDMX = formatter.format(now);
  
  // Convertir a formato ISO con zona horaria de México
  // El formato 'sv-SE' nos da: YYYY-MM-DD HH:mm:ss.sss
  // Lo convertimos a: YYYY-MM-DDTHH:mm:ss.sss-06:00
  const isoString = fechaHoraCDMX.replace(' ', 'T') + '-06:00';
  
  console.log(`🕐 Timestamp CDMX generado: ${isoString}`);
  return isoString;
}

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
  if (!error.value) return false;
  
  // Palabras clave para mensajes informativos/positivos
  const infoKeywords = [
    'Sin conexión',
    '¡Excelente!',
    'Buena precisión',
    'Precisión aceptable',
    'Ubicación obtenida',
    'Se usó ubicación',
    'Funciona sin internet',
    'modo offline',
    'caché offline',
    'precisión de',
    'Registro con precisión'
  ];
  
  // Verificar si el mensaje contiene alguna palabra clave informativa
  const isInfo = infoKeywords.some(keyword => 
    error.value.toLowerCase().includes(keyword.toLowerCase())
  );
  
  return isInfo;
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
  
  // Obtener ubicación automáticamente al iniciar el proceso de asistencia
  console.log(`🚀 Iniciando proceso de ${tipo}, obteniendo ubicación automáticamente...`);
  getUbicacion();
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
    
    // Crear FormData para enviar al servidor
    const formData = new FormData();
    formData.append("usuario_id", user.value.id.toString());
    formData.append("latitud", latitud.value);
    formData.append("longitud", longitud.value);
    formData.append("descripcion", descripcion.value);
    formData.append("foto", archivoFoto.value);
    
    // ✅ NUEVO: Agregar timestamp CDMX exacto (igual que la barra verde)
    // Solo enviar timestamp_offline si el servidor lo soporta
    const isLocalDev = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    if (isLocalDev) {
      formData.append("timestamp_offline", obtenerTimestampCDMX());
    }

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
    console.log('🔍 Iniciando obtención de ubicación con máxima precisión (funciona offline)...');
    
    // Estrategia de múltiples intentos para máxima precisión
    const configuraciones = [
      {
        timeout: 30000, // 30 segundos - máxima precisión
        enableHighAccuracy: true,
        maximumAge: 0, // No usar caché, ubicación fresca
        useCache: false
      },
      {
        timeout: 20000, // 20 segundos - buena precisión
        enableHighAccuracy: true,
        maximumAge: 30000, // Máximo 30 segundos de edad
        useCache: false
      },
      {
        timeout: 15000, // 15 segundos - precisión estándar
        enableHighAccuracy: true,
        maximumAge: 60000, // Máximo 1 minuto de edad
        useCache: true
      }
    ];
    
    // Intentar con cada configuración
    for (let i = 0; i < configuraciones.length; i++) {
      try {
        console.log(`🎯 Intento ${i + 1}/${configuraciones.length} - Buscando máxima precisión...`);
        
        const location = await geoLocationService.getCurrentLocation(configuraciones[i]);

        console.log(`✅ Ubicación obtenida en intento ${i + 1}:`, location);

        latitud.value = location.latitude;
        longitud.value = location.longitude;
        
        // Verificar que tenemos coordenadas válidas
        if (!latitud.value || !longitud.value) {
          throw new Error('Coordenadas inválidas recibidas');
        }
        
        // Información de precisión para el usuario
        if (location.accuracy) {
          if (location.accuracy <= 10) {
            console.log('🎯 Excelente precisión obtenida:', location.accuracy + 'm');
            error.value = `¡Excelente! Ubicación obtenida con precisión de ${Math.round(location.accuracy)}m.`;
          } else if (location.accuracy <= 50) {
            console.log('✅ Buena precisión obtenida:', location.accuracy + 'm');
            error.value = `Buena precisión: ${Math.round(location.accuracy)}m.`;
          } else if (location.accuracy <= 200) {
            console.log('📍 Precisión aceptable:', location.accuracy + 'm');
            error.value = `Precisión aceptable: ${Math.round(location.accuracy)}m.`;
          } else {
            console.log('⚠️ Baja precisión:', location.accuracy + 'm');
            error.value = `Precisión baja: ${Math.round(location.accuracy)}m. Intenta moverte a un área más abierta.`;
          }
          setTimeout(() => error.value = null, 5000);
        } else {
          console.log('✅ Ubicación obtenida exitosamente (precisión no disponible)');
        }
        
        return; // Salir exitosamente
        
      } catch (intentoError) {
        console.warn(`⚠️ Intento ${i + 1} falló:`, intentoError.message);
        if (i === configuraciones.length - 1) {
          // Si todos los intentos fallaron, usar fallback
          throw intentoError;
        }
      }
    }
    
  } catch (err) {
    console.warn('⚠️ Todos los intentos de geolocalización fallaron, usando fallback offline:', err);
    
    // Fallback offline: usar servicio simple (funciona sin internet)
    try {
      console.log('🔄 Usando servicio simple para funcionalidad offline...');
      const simpleLocation = await obtenerUbicacionSimple();
      
      latitud.value = simpleLocation.latitude;
      longitud.value = simpleLocation.longitude;
      
      console.log('✅ Ubicación establecida con servicio offline:', simpleLocation);
      
      // Mostrar mensaje según el origen
      if (simpleLocation.source === 'default') {
        error.value = 'Se usó ubicación aproximada (modo offline). Para mayor precisión, permite el acceso a ubicación y asegúrate de estar en un área abierta.';
        setTimeout(() => error.value = null, 8000);
      } else if (simpleLocation.source === 'cache') {
        error.value = 'Se usó ubicación del caché offline. Funciona sin internet.';
        setTimeout(() => error.value = null, 5000);
      } else if (simpleLocation.accuracy && simpleLocation.accuracy > 100) {
        error.value = `Ubicación offline obtenida con precisión de ${Math.round(simpleLocation.accuracy)}m.`;
        setTimeout(() => error.value = null, 5000);
      } else {
        error.value = 'Ubicación obtenida en modo offline.';
        setTimeout(() => error.value = null, 4000);
      }
      
    } catch (offlineError) {
      console.error('❌ Error en servicio offline:', offlineError);
      
      // Último recurso: usar ubicación por defecto (siempre funciona offline)
      console.log('🆘 Aplicando ubicación de emergencia offline...');
      latitud.value = 19.4326; // Ciudad de México
      longitud.value = -99.1332;
      
      error.value = 'Se usó ubicación por defecto (modo offline). Verifica los permisos de ubicación para mayor precisión.';
      setTimeout(() => error.value = null, 10000);
    }
    
  } finally {
    obteniendoUbicacion.value = false;
  }
}

async function getUbicacionRegistro() {
  // Verificar si está habilitado para registrar actividades
  if (!entradaMarcada.value || salidaMarcada.value) {
    if (!entradaMarcada.value) {
      error.value = "Debes marcar tu entrada primero para obtener ubicación y registrar actividades.";
    } else {
      error.value = "Has marcado tu salida. No puedes registrar más actividades hoy.";
    }
    setTimeout(() => error.value = null, 4000);
    return;
  }

  error.value = null;

  try {
    console.log('🔍 Iniciando obtención de ubicación para registro (funciona offline)...');
    
    // Usar la misma estrategia optimizada para registros
    const configuraciones = [
      {
        timeout: 25000, // 25 segundos - alta precisión para registros
        enableHighAccuracy: true,
        maximumAge: 0, // Ubicación fresca para registros importantes
        useCache: false
      },
      {
        timeout: 20000, // 20 segundos
        enableHighAccuracy: true,
        maximumAge: 30000,
        useCache: false
      },
      {
        timeout: 15000, // 15 segundos fallback
        enableHighAccuracy: true,
        maximumAge: 60000,
        useCache: true
      }
    ];
    
    // Intentar con cada configuración
    for (let i = 0; i < configuraciones.length; i++) {
      try {
        console.log(`🎯 Intento ${i + 1}/${configuraciones.length} para registro - Buscando precisión...`);
        
        const location = await geoLocationService.getCurrentLocation(configuraciones[i]);

        console.log(`✅ Ubicación para registro obtenida en intento ${i + 1}:`, location);

        latitudRegistro.value = location.latitude;
        longitudRegistro.value = location.longitude;
        
        // Verificar que tenemos coordenadas válidas
        if (!latitudRegistro.value || !longitudRegistro.value) {
          throw new Error('Coordenadas inválidas para registro');
        }
        
        // Información de precisión para registros
        if (location.accuracy) {
          if (location.accuracy <= 50) {
            console.log('✅ Buena precisión para registro:', location.accuracy + 'm');
          } else {
            console.log('📍 Precisión aceptable para registro:', location.accuracy + 'm');
            error.value = `Registro con precisión de ${Math.round(location.accuracy)}m.`;
            setTimeout(() => error.value = null, 4000);
          }
        }
        
        return; // Salir exitosamente
        
      } catch (intentoError) {
        console.warn(`⚠️ Intento ${i + 1} falló para registro:`, intentoError.message);
        if (i === configuraciones.length - 1) {
          throw intentoError;
        }
      }
    }
    
  } catch (err) {
    console.warn('⚠️ Geolocalización falló para registro, usando fallback offline:', err);
    
    // Fallback offline para registros
    try {
      console.log('🔄 Usando servicio offline para registro...');
      const simpleLocation = await obtenerUbicacionSimple();
      
      latitudRegistro.value = simpleLocation.latitude;
      longitudRegistro.value = simpleLocation.longitude;
      
      console.log('✅ Ubicación para registro establecida con servicio offline:', simpleLocation);
      
      // Mostrar mensaje según el origen
      if (simpleLocation.source === 'default') {
        error.value = 'Registro con ubicación aproximada (modo offline).';
        setTimeout(() => error.value = null, 6000);
      } else if (simpleLocation.source === 'cache') {
        error.value = 'Registro con ubicación del caché offline.';
        setTimeout(() => error.value = null, 4000);
      }
      
    } catch (offlineError) {
      console.error('❌ Error en servicio offline para registro:', offlineError);
      
      // Último recurso para registros
      console.log('🆘 Aplicando ubicación de emergencia para registro...');
      latitudRegistro.value = 19.4326; // Ciudad de México
      longitudRegistro.value = -99.1332;
      
      error.value = 'Registro con ubicación por defecto (modo offline).';
      setTimeout(() => error.value = null, 8000);
    }
  }
}

async function onFileChange(e) {
  const file = e.target.files[0];
  if (!file) return;

  try {
    // Compresión de imagen con calidad media y formato JPG
    console.log('🖼️ Comprimiendo imagen de asistencia...');
    const compressedBlob = await compressImage(file, 1280, 0.6);
    
    // Convertir el Blob comprimido a un objeto File para mantener compatibilidad
    const compressedFile = blobToFile(compressedBlob, `${tipoAsistencia.value || 'asistencia'}_${Date.now()}.jpg`);
    
    // Usar el archivo comprimido
    archivoFoto.value = compressedFile;
    
    // Mostrar la imagen comprimida en la interfaz
    const reader = new FileReader();
    reader.onload = (e2) => {
      foto.value = e2.target.result;
    };
    reader.readAsDataURL(compressedBlob);
  } catch (err) {
    console.error('Error al comprimir imagen:', err);
    // Fallback: usar la imagen original sin comprimir
    archivoFoto.value = file;
    const reader = new FileReader();
    reader.onload = (e2) => {
      foto.value = e2.target.result;
    };
    reader.readAsDataURL(file);
  }
}

async function onFileChangeRegistro(e) {
  const file = e.target.files[0];
  if (!file) return;

  try {
    // Compresión de imagen con calidad media y formato JPG
    console.log('🖼️ Comprimiendo imagen de registro...');
    const compressedBlob = await compressImage(file, 1280, 0.6);
    
    // Convertir el Blob comprimido a un objeto File para mantener compatibilidad
    const compressedFile = blobToFile(compressedBlob, `actividad_${Date.now()}.jpg`);
    
    // Usar el archivo comprimido
    archivoFotoRegistro.value = compressedFile;
    
    // Mostrar la imagen comprimida en la interfaz
    const reader = new FileReader();
    reader.onload = (e2) => {
      fotoRegistro.value = e2.target.result;
    };
    reader.readAsDataURL(compressedBlob);
  } catch (err) {
    console.error('Error al comprimir imagen:', err);
    // Fallback: usar la imagen original sin comprimir
    archivoFotoRegistro.value = file;
    const reader = new FileReader();
    reader.onload = (e2) => {
      fotoRegistro.value = e2.target.result;
    };
    reader.readAsDataURL(file);
  }
}

async function enviarRegistro() {
  // Verificar estado de asistencia
  if (!entradaMarcada.value) {
    error.value = "❌ Debes marcar tu entrada primero para poder registrar actividades.";
    setTimeout(() => error.value = null, 5000);
    return;
  }
  
  if (salidaMarcada.value) {
    error.value = "❌ Has marcado tu salida. No puedes registrar más actividades hoy.";
    setTimeout(() => error.value = null, 5000);
    return;
  }

  if (!latitudRegistro.value || !longitudRegistro.value || !archivoFotoRegistro.value || !tipoActividad.value) {
    error.value = "Falta información: necesitas ubicación, foto y tipo de actividad";
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
      
      // MEJORA: Guardar con información más completa para garantizar sincronización
      const timestampCDMX = obtenerTimestampCDMX();
      const registroID = await offlineService.guardarRegistroOffline(
        user.value.id,
        latitudRegistro.value,
        longitudRegistro.value,
        descripcionRegistro.value,
        archivoFotoRegistro.value,
        tipoActividad.value, // Nuevo: incluir tipo de actividad
        timestampCDMX // Nuevo: usar timestamp CDMX exacto
      );
      
      console.log(`✅ Registro offline guardado con ID: ${registroID}`);
      
      // Notificar al servicio de sincronización que hay registros pendientes
      // Esto ayuda a asegurar que el sistema está consciente del nuevo registro
      syncService.notifyListeners('pending_update', false, {
        tipo: 'registro', 
        id: registroID,
        timestamp: timestampCDMX
      });
      
      // Agregar a historial local con indicador offline
      historial.value.unshift({
        fecha: new Date(timestampCDMX).toLocaleString('es-MX', {
          timeZone: 'America/Mexico_City',
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        }),
        latitud: latitudRegistro.value,
        longitud: longitudRegistro.value,
        descripcion: descripcionRegistro.value,
        tipo_actividad: tipoActividad.value, // Nuevo: agregar tipo de actividad
        foto: fotoRegistro.value,
        offline: true, // Marcador para indicar que está pendiente
        backend: null,
        tipo: 'actividad', // Especificar explícitamente el tipo de registro
        id_offline: registroID // Guardar el ID generado para referencia
      });

      // Limpiar campos
      descripcionRegistro.value = "";
      tipoActividad.value = ""; // Nuevo: limpiar tipo de actividad
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
    formData.append("tipo_actividad", tipoActividad.value); // Nuevo: agregar tipo de actividad
    formData.append("foto", archivoFotoRegistro.value);
    formData.append("tipo", "actividad"); // Especificar explícitamente que es un registro de actividad
    // ✅ SOLUCIÓN: Agregar timestamp CDMX exacto (igual que en la barra verde)
    // Solo enviar timestamp_offline si el servidor lo soporta
    const isLocalDev = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    if (isLocalDev) {
      formData.append("timestamp_offline", obtenerTimestampCDMX());
    }

    // Enviar datos al backend
    const response = await axios.post(`${API_URL}/registro`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        "X-Registro-Tipo": "actividad" // Identificar explícitamente el tipo de registro
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
      tipo_actividad: tipoActividad.value, // Nuevo: agregar tipo de actividad
      foto: fotoRegistro.value,
      offline: false, // Enviado exitosamente
      backend: response.data,
      tipo: 'actividad' // Especificar explícitamente el tipo de registro
    });

    // Limpiar campos
    descripcionRegistro.value = "";
    tipoActividad.value = ""; // Nuevo: limpiar tipo de actividad
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

// Funciones para modales de confirmación
function mostrarModalEntrada() {
  entradaModalMessage.value = `
    <div class="text-left">
      <div class="flex items-center mb-3">
        <div class="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center mr-3" style="background-color: rgba(30, 144, 255, 0.1);">
          <svg class="w-5 h-5" style="color: rgb(30, 144, 255);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
          </svg>
        </div>
        <div>
          <h3 class="text-base font-semibold text-gray-900">Registrar Entrada</h3>
          <p class="text-xs text-gray-600">Inicia tu jornada laboral</p>
        </div>
      </div>
      
      <div class="p-3 mb-3 rounded" style="background-color: rgba(30, 144, 255, 0.1); border-left: 4px solid rgba(30, 144, 255, 0.6);">
        <div class="flex items-center">
          <svg class="w-4 h-4 mr-2" style="color: rgb(30, 144, 255);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <p class="font-medium text-sm" style="color: rgb(25, 118, 210);">Al registrar tu entrada podrás registrar actividades</p>
        </div>
        <p class="text-xs mt-1 ml-6" style="color: rgb(30, 144, 255);">Durante tu jornada podrás capturar todas tus actividades</p>
      </div>

      <div class="space-y-2 text-xs text-gray-600">
        <div class="flex items-start">
          <svg class="w-3 h-3 mr-2 mt-0.5 flex-shrink-0" style="color: rgb(30, 144, 255);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
          </svg>
          <span>Se capturará ubicación y fotografía</span>
        </div>
        
        <div class="flex items-start">
          <svg class="w-3 h-3 text-purple-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0"/>
          </svg>
          <span>Funciona offline</span>
        </div>
        
        <div class="flex items-start">
          <svg class="w-3 h-3 text-amber-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"/>
          </svg>
          <span>No se puede cancelar una vez registrada</span>
        </div>
      </div>
    </div>
  `;
  showEntradaModal.value = true;
}

function mostrarModalSalida() {
  salidaModalMessage.value = `
    <div class="text-left">
      <div class="flex items-center mb-3">
        <div class="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center mr-3" style="background-color: rgba(220, 20, 60, 0.1);">
          <svg class="w-5 h-5" style="color: rgb(220, 20, 60);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
          </svg>
        </div>
        <div>
          <h3 class="text-base font-semibold text-gray-900">Registrar Salida</h3>
          <p class="text-xs text-gray-600">Finaliza tu jornada laboral</p>
        </div>
      </div>
      
      <div class="p-3 mb-3 rounded" style="background-color: rgba(220, 20, 60, 0.1); border-left: 4px solid rgba(220, 20, 60, 0.6);">
        <div class="flex items-center">
          <svg class="w-4 h-4 mr-2" style="color: rgb(220, 20, 60);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728L5.636 5.636m12.728 12.728L18 21l-5.197-5.197m0 0L12 12.803m0 0L5.196 17.996M12 12.803l5.198-5.197L21 3"/>
          </svg>
          <p class="font-medium text-sm" style="color: rgb(185, 15, 50);">No podrás registrar más actividades</p>
        </div>
        <p class="text-xs mt-1 ml-6" style="color: rgb(220, 20, 60);">El registro se bloqueará hasta mañana</p>
      </div>

      <div class="space-y-3 text-sm text-gray-600">
        <div class="flex items-start">
          <svg class="w-4 h-4 mr-3 mt-0.5 flex-shrink-0" style="color: rgb(220, 20, 60);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
          </svg>
          <span>Se capturará tu ubicación actual y una fotografía</span>
        </div>
        
        <div class="flex items-start">
          <svg class="w-4 h-4 text-purple-500 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0"/>
          </svg>
          <span>Funciona sin conexión (se sincroniza automáticamente)</span>
        </div>
        
        <div class="flex items-start">
          <svg class="w-4 h-4 text-amber-500 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"/>
          </svg>
          <span>Una vez registrada no se puede cancelar</span>
        </div>
      </div>
    </div>
  `;
  showSalidaModal.value = true;
}

function closeEntradaModal() {
  showEntradaModal.value = false;
  entradaModalMessage.value = '';
}

function closeSalidaModal() {
  showSalidaModal.value = false;
  salidaModalMessage.value = '';
}

function confirmarEntradaModal() {
  closeEntradaModal();
  iniciarAsistencia('entrada');
}

function confirmarSalidaModal() {
  closeSalidaModal();
  iniciarAsistencia('salida');
}

function mostrarModalActividadesBloqueadas() {
  if (!entradaMarcada.value) {
    actividadesBloqueadasModalMessage.value = `
      <div class="text-center">
        <div class="flex items-center justify-center mb-3">
          <div class="w-8 h-8 bg-amber-100 rounded-full flex items-center justify-center mr-2">
            <svg class="w-4 h-4 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
            </svg>
          </div>
          <h3 class="text-sm font-semibold text-gray-900">Acceso Bloqueado</h3>
        </div>
        
        <div class="bg-amber-50 border border-amber-200 rounded-lg p-2 mb-2">
          <p class="text-amber-800 text-xs font-medium">Inicia tu jornada laboral primero</p>
          <p class="text-amber-600 text-xs mt-1">Marca tu entrada en "Asistencia"</p>
        </div>
      </div>
    `;
  } else if (salidaMarcada.value) {
    actividadesBloqueadasModalMessage.value = `
      <div class="text-center">
        <div class="flex items-center justify-center mb-3">
          <div class="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center mr-2">
            <svg class="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
          </div>
          <h3 class="text-sm font-semibold text-gray-900">Salida Registrada</h3>
        </div>
        
        <div class="bg-red-50 border border-red-200 rounded-lg p-2 mb-2">
          <p class="text-red-800 text-xs font-medium">Salida de jornada ya marcada</p>
          <p class="text-red-600 text-xs mt-1">Se restaurará el siguiente día</p>
        </div>
      </div>
    `;
  }
  
  showActividadesBloqueadasModal.value = true;
}

function closeActividadesBloqueadasModal() {
  showActividadesBloqueadasModal.value = false;
  actividadesBloqueadasModalMessage.value = '';
}

function verificarEstadoAsistencia() {
  try {
    // *** CORREGIDO: Usar fecha CDMX consistente ***
    const fechaHoyCDMX = new Date().toLocaleString("en-CA", {
      timeZone: "America/Mexico_City",
      year: "numeric",
      month: "2-digit", 
      day: "2-digit"
    });
    
    console.log(`🔍 Verificando estado de asistencia para ${fechaHoyCDMX}`);
    
    // Reiniciar estados por defecto (suponemos que no hay registros)
    entradaMarcada.value = false;
    salidaMarcada.value = false;
    datosEntrada.value = {};
    datosSalida.value = {};
    
    // Verificamos si hay datos guardados para el día de hoy específicamente
    const estadoHoy = localStorage.getItem(`asistencia_${user.value.id}_${fechaHoyCDMX}`);
    
    if (estadoHoy) {
      const datos = JSON.parse(estadoHoy);
      
      // *** CORREGIDO: Verificar expiración en zona horaria CDMX ***
      const ahoraCDMX = new Date().toLocaleString("sv-SE", { timeZone: "America/Mexico_City" });
      const fechaCompletaCDMX = new Date(ahoraCDMX);
      
      const expiraEn = datos.expiraEn ? new Date(datos.expiraEn) : new Date(fechaHoyCDMX + 'T23:59:59');
      const esValido = fechaCompletaCDMX < expiraEn;
      
      console.log(`📊 Datos locales encontrados para hoy:`, {
        entrada: !!datos.entradaMarcada,
        salida: !!datos.salidaMarcada,
        expiraEn: expiraEn.toLocaleString("es-MX", { timeZone: "America/Mexico_City" }),
        esValido,
        horaActualCDMX: fechaCompletaCDMX.toLocaleString("es-MX", { timeZone: "America/Mexico_City" })
      });
      
      if (esValido) {
        // Los datos son válidos (todavía estamos en el mismo día antes de las 23:59:59 CDMX)
        console.log(`✅ Usando datos locales válidos (expiran a las 23:59:59 CDMX)`);
        entradaMarcada.value = datos.entradaMarcada || false;
        salidaMarcada.value = datos.salidaMarcada || false;
        datosEntrada.value = datos.datosEntrada || {};
        datosSalida.value = datos.datosSalida || {};
      } else {
        console.log(`⚠️ Datos locales expirados, reiniciando estados`);
      }
    } else {
      console.log(`ℹ️ No hay datos guardados para hoy, consultando backend`);
    }

    // Limpiamos datos de días anteriores para no acumular basura en localStorage
    limpiarDatosAntiguos();

    // Después de cargar del localStorage, verificar con el backend para tener datos actualizados
    verificarAsistenciaHoy();
  } catch (error) {
    console.error('Error al verificar estado de asistencia:', error);
  }
}

// Función para asegurar que los estados se mantengan correctamente hasta las 23:59:59 CDMX
function asegurarEstadosConsistentes() {
  if (!user.value.id) return;
  
  // *** CORREGIDO: Usar fecha CDMX consistente ***
  const fechaHoyCDMX = new Date().toLocaleString("en-CA", {
    timeZone: "America/Mexico_City",
    year: "numeric",
    month: "2-digit", 
    day: "2-digit"
  });
  
  console.log('🔐 Verificando consistencia de estados de asistencia...');
  
  try {
    const estadoHoy = localStorage.getItem(`asistencia_${user.value.id}_${fechaHoyCDMX}`);
    
    if (estadoHoy) {
      const datos = JSON.parse(estadoHoy);
      
      // *** CORREGIDO: Verificar expiración en zona horaria CDMX ***
      const ahoraCDMX = new Date().toLocaleString("sv-SE", { timeZone: "America/Mexico_City" });
      const fechaCompletaCDMX = new Date(ahoraCDMX);
      
      const expiraEn = datos.expiraEn ? new Date(datos.expiraEn) : new Date(fechaHoyCDMX + 'T23:59:59');
      
      if (fechaCompletaCDMX < expiraEn) {
        console.log('✅ Asegurando estados hasta las 23:59:59 CDMX');
        
        // Si en localStorage indica que la entrada fue marcada, asegurar que se refleje en el estado
        if (datos.entradaMarcada && !entradaMarcada.value) {
          console.log('🔄 Restaurando estado de entrada marcada');
          entradaMarcada.value = true;
          datosEntrada.value = datos.datosEntrada || {};
        }
        
        // Si en localStorage indica que la salida fue marcada, asegurar que se refleje en el estado
        if (datos.salidaMarcada && !salidaMarcada.value) {
          console.log('🔄 Restaurando estado de salida marcada');
          salidaMarcada.value = true;
          datosSalida.value = datos.datosSalida || {};
        }
      }
    }
  } catch (error) {
    console.error('❌ Error al asegurar estados consistentes:', error);
  }
}

/**
 * Limpia los datos de asistencia de días anteriores del localStorage
 */
function limpiarDatosAntiguos() {
  try {
    // *** CORREGIDO: Usar fecha CDMX consistente ***
    const hoyCDMX = new Date().toLocaleString("en-CA", {
      timeZone: "America/Mexico_City",
      year: "numeric",
      month: "2-digit", 
      day: "2-digit"
    });
    
    // Recorremos todas las claves del localStorage
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      
      // Si es una clave de asistencia para este usuario pero no de hoy, la eliminamos
      if (key && key.startsWith(`asistencia_${user.value.id}_`) && !key.includes(hoyCDMX)) {
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
  async function verificarAsistenciaHoy(forceRefresh = false) {
    verificandoAsistencia.value = true;
    try {
      // Verificar conexión a internet antes de consultar
      isOnline.value = await checkInternetConnection();
      if (!isOnline.value) {
        console.log('Sin conexión, usando datos locales de asistencia');
        return;
      }

      // *** CORREGIDO: Obtener fecha actual en zona horaria de CDMX ***
      const ahoraCDMX = new Date().toLocaleString("en-CA", {
        timeZone: "America/Mexico_City",
        year: "numeric",
        month: "2-digit", 
        day: "2-digit"
      });
      const fechaActual = ahoraCDMX; // Formato YYYY-MM-DD en CDMX
      
      console.log(`🔍 Consultando asistencia del día con forceRefresh=${forceRefresh}`);
      console.log(`📅 Fecha actual CDMX: ${fechaActual}`);
      const datos = await asistenciasService.consultarAsistenciaHoy(user.value.id, forceRefresh);
      asistenciaHoy.value = datos;
      
      console.log(`📊 Datos recibidos del backend - fecha: ${datos.fecha}, entrada: ${!!datos.entrada}, salida: ${!!datos.salida}`);
      
      // Verificar que los datos correspondan al día actual EN ZONA CDMX
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
        
        console.log(`✅ Estados actualizados para fecha ${fechaActual}: entrada=${entradaMarcada.value}, salida=${salidaMarcada.value}`);
      } else {
        console.log(`ℹ️ Fecha del backend (${datos.fecha}) ≠ fecha actual CDMX (${fechaActual})`);
        
        // *** CORREGIDO: Solo reiniciar estados si realmente es un día diferente ***
        // Verificar si realmente es un nuevo día comparando fechas correctamente
        const fechaGuardadaLocal = localStorage.getItem(`asistencia_ultima_fecha_${user.value.id}`);
        
        if (fechaGuardadaLocal !== fechaActual) {
          console.log(`📆 Nuevo día detectado (guardado: ${fechaGuardadaLocal}, actual: ${fechaActual}). Reiniciando estados.`);
          // Es realmente un nuevo día, reiniciar estados
          entradaMarcada.value = false;
          salidaMarcada.value = false;
          datosEntrada.value = {};
          datosSalida.value = {};
          guardarEstadoAsistencia();
        } else {
          console.log(`⚠️ Manteniendo estados actuales - posible diferencia de zona horaria entre frontend y backend`);
          // No reiniciar estados si el día guardado coincide con el actual
        }
      }
    } catch (error) {
      console.error('Error al verificar asistencia de hoy:', error);
      // *** CORREGIDO: Solo reiniciar estados en caso de verdadero cambio de día ***
      const fechaGuardada = localStorage.getItem(`asistencia_ultima_fecha_${user.value.id}`);
      
      // Obtener fecha actual CDMX correctamente
      const fechaActualCDMX = new Date().toLocaleString("en-CA", {
        timeZone: "America/Mexico_City",
        year: "numeric",
        month: "2-digit", 
        day: "2-digit"
      });
      
      if (fechaGuardada !== fechaActualCDMX) {
        console.log(`📆 Nuevo día detectado durante error (guardado: ${fechaGuardada}, actual: ${fechaActualCDMX}). Reiniciando estados.`);
        // Es un nuevo día, reiniciar estados incluso sin conexión
        entradaMarcada.value = false;
        salidaMarcada.value = false;
        datosEntrada.value = {};
        datosSalida.value = {};
        guardarEstadoAsistencia();
      } else {
        console.log(`⚠️ Error de conexión, pero manteniendo estados del mismo día (${fechaActualCDMX})`);
      }
    } finally {
      verificandoAsistencia.value = false;
    }
  }/**
 * Formatea una fecha ISO a formato de hora local
 */
function formatearHora(fechaISO) {
  if (!fechaISO) return "";
  const hora = new Date(fechaISO);
  return hora.toLocaleTimeString("es-MX", { hour: '2-digit', minute: '2-digit', timeZone: 'America/Mexico_City' });
}

function guardarEstadoAsistencia() {
  // *** CORREGIDO: Usar fecha CDMX consistente ***
  const fechaHoyCDMX = new Date().toLocaleString("en-CA", {
    timeZone: "America/Mexico_City",
    year: "numeric",
    month: "2-digit", 
    day: "2-digit"
  });
  
  // Configurar expiración a las 23:59:59 del día actual EN CDMX
  const ahoraCDMX = new Date().toLocaleString("sv-SE", { timeZone: "America/Mexico_City" });
  const fechaCompletaCDMX = new Date(ahoraCDMX);
  const finDelDiaCDMX = new Date(fechaCompletaCDMX);
  finDelDiaCDMX.setHours(23, 59, 59, 999);
  
  const estado = {
    entradaMarcada: entradaMarcada.value,
    salidaMarcada: salidaMarcada.value,
    datosEntrada: datosEntrada.value,
    datosSalida: datosSalida.value,
    ultimaActualizacion: new Date().toISOString(),
    // Guardar hora de expiración a las 23:59:59 del día actual EN CDMX
    expiraEn: finDelDiaCDMX.toISOString()
  };
  
  console.log(`💾 Guardando estado de asistencia para el día ${fechaHoyCDMX}`);
  console.log(`   ⏰ Entrada marcada: ${entradaMarcada.value}`);
  console.log(`   ⏰ Salida marcada: ${salidaMarcada.value}`);
  console.log(`   📅 Expira a las: ${finDelDiaCDMX.toLocaleString("es-MX", { timeZone: "America/Mexico_City" })} (23:59:59 CDMX)`);
  
  // Guardar el estado del día actual
  localStorage.setItem(`asistencia_${user.value.id}_${fechaHoyCDMX}`, JSON.stringify(estado));
  
  // También guardar la última fecha consultada para comparaciones EN CDMX
  localStorage.setItem(`asistencia_ultima_fecha_${user.value.id}`, fechaHoyCDMX);
}

/**
 * Carga los registros de actividades para el historial
 * @param {boolean} forceRefresh - Si es true, fuerza una actualización desde el servidor
 */
async function cargarHistorial(forceRefresh = false) {
  try {
    console.log(`🔄 Cargando historial de registros${forceRefresh ? ' (forzando actualización)' : ''}...`);
    
    // Verificar conexión a internet
    const isConnected = await checkInternetConnection();
    if (!isConnected) {
      console.log('📴 Sin conexión, mostrando solo registros offline');
      // Mostrar registros offline si hay
      const pendientes = await offlineService.obtenerResumenPendientes();
      if (pendientes && pendientes.registros && pendientes.registros.items) {
        historial.value = pendientes.registros.items.map(r => ({
          fecha: new Date(r.timestamp).toLocaleString(),
          latitud: r.latitud,
          longitud: r.longitud,
          descripcion: r.descripcion || 'Sin descripción',
          offline: true,
          tipo: r.tipo || 'actividad'
        }));
      }
      return;
    }
    
    // Si hay conexión, intentar obtener del servidor
    // Siempre incluir un parámetro de tiempo para forzar nueva petición sin cache
    const cacheParam = `&_nocache=${Date.now()}`;
    const response = await axios.get(
      `${API_URL}/registros?usuario_id=${user.value.id}${cacheParam}`, 
      {
        headers: {
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Pragma': 'no-cache',
          'X-Force-Refresh': 'true'
        }
      }
    );
    
    // Procesamos los registros del servidor
    const registrosOnline = response.data.map(r => ({
      fecha: new Date(r.timestamp).toLocaleString(),
      latitud: r.latitud,
      longitud: r.longitud,
      descripcion: r.descripcion || 'Sin descripción',
      foto: r.foto_url,
      offline: false,
      backend: r,
      tipo: r.tipo || 'actividad'
    }));
    
    // Obtenemos registros pendientes offline
    const pendientes = await offlineService.obtenerResumenPendientes();
    let registrosOffline = [];
    
    if (pendientes && pendientes.registros && pendientes.registros.items) {
      registrosOffline = pendientes.registros.items.map(r => ({
        fecha: new Date(r.timestamp).toLocaleString(),
        latitud: r.latitud,
        longitud: r.longitud,
        descripcion: r.descripcion || 'Sin descripción',
        offline: true,
        tipo: r.tipo || 'actividad'
      }));
    }
    
    // Combinar registros online y offline, los offline primero
    historial.value = [...registrosOffline, ...registrosOnline];
    
    // Ordenar por fecha más reciente primero
    historial.value.sort((a, b) => new Date(b.fecha) - new Date(a.fecha));
    
    console.log(`✅ Historial actualizado: ${historial.value.length} registros (${registrosOffline.length} offline, ${registrosOnline.length} online)`);
    
  } catch (error) {
    console.error('❌ Error cargando historial:', error);
    // En caso de error, intentar mostrar datos offline
    try {
      const pendientes = await offlineService.obtenerResumenPendientes();
      if (pendientes && pendientes.registros && pendientes.registros.items) {
        historial.value = pendientes.registros.items.map(r => ({
          fecha: new Date(r.timestamp).toLocaleString(),
          latitud: r.latitud,
          longitud: r.longitud,
          descripcion: r.descripcion || 'Sin descripción',
          offline: true,
          tipo: r.tipo || 'actividad'
        }));
      }
    } catch (err) {
      console.error('Error cargando datos offline:', err);
    }
  }
}

// Forzar sincronización manual
async function forzarSincronizacion() {
  try {
    isOnline.value = await checkInternetConnection();
    if (!isOnline.value) {
      error.value = "No hay conexión a internet para sincronizar.";
      return;
    }
    
    console.log('🔄 Forzando sincronización manual');
    const resultado = await syncService.sincronizarManual();
    
    // Mostrar mensaje de sincronización en progreso
    mensajeAsistencia.value = "Sincronización en progreso...";
    
    // Esperar un poco para que el backend procese los datos y luego actualizar el historial
    setTimeout(async () => {
      try {
        // Forzar actualización del historial después de sincronizar
        await cargarHistorial(true);
        console.log('✅ Historial actualizado después de sincronización manual');
        
        // Verificar asistencia y actualizar UI
        await verificarAsistenciaHoy(true);
        
        // Mostrar mensaje de éxito
        if (resultado && resultado.exitosos > 0) {
          mensajeAsistencia.value = `Sincronización exitosa. ${resultado.exitosos} registro(s) enviado(s).`;
        } else {
          mensajeAsistencia.value = "Sincronización completada. No había registros pendientes.";
        }
        
        // Limpiar mensaje después de un tiempo
        setTimeout(() => {
          mensajeAsistencia.value = '';
        }, 5000);
        
      } catch (err) {
        console.error('Error actualizando historial después de sincronización manual:', err);
        mensajeAsistencia.value = "Error al actualizar registros después de sincronizar.";
      }
    }, 2000);
    
  } catch (error) {
    console.error('Error al forzar sincronización:', error);
    error.value = `Error al sincronizar: ${error.message}`;
    mensajeAsistencia.value = "Error en la sincronización.";
  }
}

// Manejador de eventos de sincronización
function handleSyncEvent(event, online, data) {
  console.log(`🔄 Evento de sincronización recibido: ${event}`);
  
  // Actualizar estado de conexión
  isOnline.value = online;
  
  switch (event) {
    case 'online':
      console.log('🌐 Conectado en Home.vue');
      error.value = null;
      
      // MEJORA: Verificar pendientes y sincronizar de manera más robusta
      // Al recuperar conexión, siempre verificar ambos tipos de pendientes (registros y asistencias)
      offlineService.contarPendientes(true).then(async pendientes => {
        console.log(`📊 Estado de pendientes al recuperar conexión:`, pendientes);
        
        // Si hay pendientes, mostrar más detalles para debugging
        if (pendientes.total > 0) {
          console.log(`🔄 Conexión recuperada con ${pendientes.total} pendientes (${pendientes.registros} registros, ${pendientes.asistencias} asistencias), sincronizando automáticamente...`);
          
          // Verificar los registros pendientes con más detalle
          if (pendientes.registros > 0) {
            // Solicitar detalle de registros pendientes para debugging
            const registrosPendientes = await offlineService.obtenerRegistrosPendientes(true);
            console.log(`🧪 DEBUGGING - Registros pendientes encontrados: ${registrosPendientes.length}`);
          }
          
          // Mostrar un mensaje informativo sobre la sincronización automática
          mensajeAsistencia.value = `Sincronizando ${pendientes.total} registro(s) pendiente(s)...`;
          
          // MEJORA: Usar un tiempo de espera mayor para asegurar conexión estable
          setTimeout(() => {
            // Usar sincronizarTodo directamente para asegurar sincronización completa
            syncService.sincronizarTodo()
              .then(resultado => {
                console.log('✅ Resultado de sincronización:', resultado);
                if (resultado.exitosos > 0) {
                  mensajeAsistencia.value = `Sincronización exitosa. ${resultado.exitosos} registro(s) enviado(s).`;
                } else if (resultado.fallidos > 0) {
                  mensajeAsistencia.value = `Sincronización parcial. ${resultado.fallidos} registro(s) con error.`;
                }
                
                // Verificar nuevamente el estado de pendientes después de sincronizar
                setTimeout(async () => {
                  const pendientesDespues = await offlineService.contarPendientes(true);
                  console.log('📊 Estado de pendientes después de sincronización:', pendientesDespues);
                }, 1000);
              })
              .catch(err => {
                console.error('❌ Error en sincronización automática al recuperar conexión:', err);
                mensajeAsistencia.value = "Error al sincronizar. Intente nuevamente.";
                setTimeout(() => {
                  mensajeAsistencia.value = '';
                }, 5000);
              });
          }, 2500); // Esperar un poco más para asegurar conexión estable
        } else {
          console.log('✅ No hay pendientes que sincronizar al recuperar conexión');
          // No mostrar mensaje si no hay pendientes
        }
      }).catch(err => {
        console.error('❌ Error verificando pendientes al recuperar conexión:', err);
      });
      break;
      
    case 'offline':
      console.log('📴 Desconectado en Home.vue');
      error.value = getOfflineMessage();
      break;
      
    case 'syncing':
      console.log('🔄 Sincronizando...');
      // Mostrar mensaje de sincronización en progreso
      mensajeAsistencia.value = "Sincronizando datos pendientes...";
      break;
      
    case 'sync_complete':
      console.log('✅ Sincronización completada:', data);
      
      // MEJORA: Verificar si hay más pendientes después de la sincronización
      offlineService.contarPendientes(true).then(pendientesDespues => {
        console.log('📊 Pendientes después de sincronización:', pendientesDespues);
        
        // Si todavía hay pendientes después de la sincronización, puede ser un problema
        if (pendientesDespues.total > 0) {
          console.warn(`⚠️ Todavía quedan ${pendientesDespues.total} registros pendientes después de sincronizar`);
          
          // Intentar un segundo ciclo de sincronización para registros difíciles
          if (data && data.exitosos > 0) {
            console.log('🔄 Intentando un segundo ciclo de sincronización para registros persistentes...');
            setTimeout(() => {
              syncService.sincronizarTodo();
            }, 5000); // Esperar 5 segundos antes de reintentar
          }
        }
      });
      
      // MEJORA: Siempre actualizar los datos después de una sincronización, incluso si no hay exitosos
      // Esto ayuda a mantener la UI siempre actualizada
      setTimeout(async () => {
        try {
          console.log('🔄 Actualizando datos después de sincronización');
          
          // Primero actualizar datos de asistencia
          await verificarAsistenciaHoy(true);
          
          // Luego actualizar el historial completo
          await cargarHistorial(true);
          
          // Mostrar mensaje de éxito según los resultados
          if (data && data.exitosos > 0) {
            mensajeAsistencia.value = `Sincronización exitosa. ${data.exitosos} registro(s) enviado(s).`;
          } else if (data && data.fallidos > 0) {
            mensajeAsistencia.value = `Hubo problemas al sincronizar ${data.fallidos} registro(s). Se reintentará automáticamente.`;
          } else {
            // Comprobar si realmente no había registros o si hubo un problema
            offlineService.contarPendientes(true).then(pendientesActuales => {
              if (pendientesActuales.total > 0) {
                mensajeAsistencia.value = `Atención: Hay ${pendientesActuales.total} registro(s) pendiente(s) que no se pudieron sincronizar.`;
              } else {
                mensajeAsistencia.value = "Sincronización completada. No había registros pendientes.";
              }
            });
          }
          
          // Limpiar mensaje después de un tiempo
          setTimeout(() => {
            mensajeAsistencia.value = '';
          }, 8000); // Aumentar tiempo de visualización
          
        } catch (error) {
          console.error('❌ Error actualizando datos después de sincronización:', error);
          mensajeAsistencia.value = "Error actualizando datos después de sincronizar.";
          setTimeout(() => {
            mensajeAsistencia.value = '';
          }, 5000);
        }
      }, 2000); // Esperar 2 segundos para dar tiempo al backend
      break;
      
    case 'sync_error':
      console.log('❌ Error en sincronización:', data);
      // Mostrar mensaje de error
      mensajeAsistencia.value = "Error en la sincronización.";
      setTimeout(() => {
        mensajeAsistencia.value = '';
      }, 5000);
      break;
  }
}

// Añadir una verificación periódica para asegurar que el estado de los botones se mantenga consistente
let verificacionPeriodica;

// Comprobación si un horario está dentro del día actual (antes de las 23:59:59 CDMX)
function esHorarioDentroDelDiaActual() {
  // *** CORREGIDO: Usar zona horaria CDMX consistente ***
  const ahoraCDMX = new Date().toLocaleString("sv-SE", { timeZone: "America/Mexico_City" });
  const fechaCompletaCDMX = new Date(ahoraCDMX);
  
  const finDelDiaCDMX = new Date(fechaCompletaCDMX);
  finDelDiaCDMX.setHours(23, 59, 59, 999);
  
  const horaActualCDMX = fechaCompletaCDMX.toLocaleString("es-MX", { timeZone: "America/Mexico_City" });
  const finDelDiaTexto = finDelDiaCDMX.toLocaleString("es-MX", { timeZone: "America/Mexico_City" });
  
  console.log(`⏰ Verificación de horario CDMX: ${horaActualCDMX} < ${finDelDiaTexto} = ${fechaCompletaCDMX < finDelDiaCDMX}`);
  
  return fechaCompletaCDMX < finDelDiaCDMX;
}

onMounted(async () => {
  // Verificar si el usuario está autenticado
  if (!user.value.id) {
    router.push("/login");
    return;
  }
  
  // *** DEBUGGING: Hacer función disponible globalmente ***
  if (typeof window !== 'undefined') {
    window.debugAsistencia = debugEstadoAsistencia;
    console.log('🔬 Función de debugging disponible: window.debugAsistencia()');
  }
  
  // Registrar manejador de eventos de sincronización
  syncService.addListener(handleSyncEvent);
  
  console.log('🚀 Inicializando componente Home, verificando estado de asistencia');
  
  // Verificar estado de asistencia del día inmediatamente
  verificarEstadoAsistencia();
  
  // Verificar conexión a internet
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    error.value = getOfflineMessage();
  }
  
  // Cargar historial de registros
  cargarHistorial();
  
  // Verificar estado del servicio de geolocalización
  console.log('🔍 Verificando servicio de geolocalización...');
  try {
    const geoStatus = geoLocationService.getStatus();
    console.log('📊 Estado del servicio de geolocalización:', geoStatus);
    
    // Pre-cargar ubicación de manera silenciosa en segundo plano
    console.log('🌍 Pre-cargando ubicación en segundo plano...');
    setTimeout(async () => {
      try {
        await geoLocationService.getLocationSmart({
          timeout: 15000,
          enableHighAccuracy: true,
          useCache: true
        });
        console.log('✅ Ubicación pre-cargada exitosamente');
      } catch (error) {
        console.log('⚠️ No se pudo pre-cargar ubicación:', error.message);
        // Establecer ubicación por defecto si no se puede obtener
        geoLocationService.setDefaultLocation();
      }
    }, 2000); // Esperar 2 segundos antes de pre-cargar
    
  } catch (error) {
    console.error('❌ Error verificando servicio de geolocalización:', error);
  }
  
  // Realizar una verificación inicial de consistencia
  asegurarEstadosConsistentes();
  
  // *** NUEVA FUNCIÓN DE DEBUGGING MEJORADA ***
  async function debugEstadoAsistencia() {
    console.log('🔬 === DEBUGGING COMPLETO ESTADO ASISTENCIA ===');
    
    // 1. Información de tiempo actual
    const fechaHoyCDMX = new Date().toLocaleString("en-CA", {
      timeZone: "America/Mexico_City",
      year: "numeric",
      month: "2-digit", 
      day: "2-digit"
    });
    
    const ahoraCDMX = new Date().toLocaleString("sv-SE", { timeZone: "America/Mexico_City" });
    const fechaCompletaCDMX = new Date(ahoraCDMX);
    
    console.log('📅 Tiempo actual:');
    console.log(`   🇲🇽 Fecha CDMX: ${fechaHoyCDMX}`);
    console.log(`   ⏰ Hora completa CDMX: ${fechaCompletaCDMX.toLocaleString("es-MX", { timeZone: "America/Mexico_City" })}`);
    
    // 2. Estado actual de variables reactivas
    console.log('📊 Estado actual variables:');
    console.log(`   ✅ entradaMarcada: ${entradaMarcada.value}`);
    console.log(`   🚪 salidaMarcada: ${salidaMarcada.value}`);
    console.log(`   📝 datosEntrada:`, datosEntrada.value);
    console.log(`   📝 datosSalida:`, datosSalida.value);
    
    // 3. Estado localStorage
    const estadoHoy = localStorage.getItem(`asistencia_${user.value.id}_${fechaHoyCDMX}`);
    console.log('💾 Estado localStorage:');
    if (estadoHoy) {
      const datos = JSON.parse(estadoHoy);
      console.log(`   📦 Datos guardados para hoy:`, datos);
      
      const expiraEn = datos.expiraEn ? new Date(datos.expiraEn) : null;
      if (expiraEn) {
        console.log(`   ⏰ Expira en: ${expiraEn.toLocaleString("es-MX", { timeZone: "America/Mexico_City" })}`);
        console.log(`   ✅ Es válido: ${fechaCompletaCDMX < expiraEn}`);
      }
    } else {
      console.log('   ❌ No hay datos guardados para hoy');
    }
    
    // 4. Consultar backend
    try {
      console.log('🌐 Consultando backend...');
      const datosBackend = await asistenciasService.consultarAsistenciaHoy(user.value.id, true);
      console.log('📊 Respuesta del backend:', datosBackend);
    } catch (error) {
      console.error('❌ Error consultando backend:', error);
    }
    
    console.log('🔬 === FIN DEBUGGING ===');
  }
  
  // Realizar verificación periódica del estado de asistencia
  // Esta verificación asegura que los estados se mantengan correctos durante todo el día
  // *** CORREGIDO: Verificación menos frecuente y más inteligente ***
  // Esta verificación asegura que los estados se mantengan correctos durante todo el día
  verificacionPeriodica = setInterval(() => {
    console.log('🔄 Verificación periódica de estado de asistencia');
    // Verificar si todavía estamos en el mismo día (antes de 23:59:59 CDMX)
    if (esHorarioDentroDelDiaActual()) {
      // Asegurar consistencia local primero
      asegurarEstadosConsistentes();
      
      // *** CORREGIDO: Solo verificar con backend ocasionalmente para evitar resets ***
      // Estamos en el mismo día, verificar estados con backend solo si hay conexión
      // y sin forceRefresh para evitar problemas de sincronización
      if (navigator.onLine) {
        console.log('🔄 Verificación suave de estados con backend (sin forceRefresh)');
        verificarAsistenciaHoy(false); // *** IMPORTANTE: false para no forzar reset ***
      } else {
        console.log('📴 Sin conexión, manteniendo estados actuales');
      }
    } else {
      console.log('📆 Día finalizado (después de 23:59:59 CDMX), esperando cambio de fecha');
    }
  }, 10 * 60 * 1000); // *** CORREGIDO: Verificar cada 10 minutos en lugar de 3 ***
});

// Limpiar recursos al desmontar el componente
onUnmounted(() => {
  syncService.removeListener(handleSyncEvent);
  
  // Limpiar verificación periódica
  if (verificacionPeriodica) {
    clearInterval(verificacionPeriodica);
    console.log('🧹 Limpiado intervalo de verificación de asistencia');
  }
});

// Watcher para guardar cambios de asistencia en localStorage
watch([entradaMarcada, salidaMarcada, datosEntrada, datosSalida], () => {
  if (user.value.id) {
    guardarEstadoAsistencia();
    // Asegurar consistencia después de guardar
    asegurarEstadosConsistentes();
  }
}, { deep: true });

// Watcher para limpiar campos de registro cuando se bloquean las actividades
watch([entradaMarcada, salidaMarcada], () => {
  // Si las actividades se bloquean (no hay entrada o hay salida), limpiar campos de actividades
  if (!entradaMarcada.value || salidaMarcada.value) {
    console.log('🚫 Actividades bloqueadas, limpiando campos de registro');
    descripcionRegistro.value = "";
    fotoRegistro.value = null;
    archivoFotoRegistro.value = null;
    latitudRegistro.value = null;
    longitudRegistro.value = null;
    
    if (fileInputRegistro.value) {
      fileInputRegistro.value.value = "";
    }
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

.bounce-enter-active {
  animation: bounce-in 0.5s;
}
.bounce-leave-active {
  animation: bounce-in 0.5s reverse;
}
@keyframes bounce-in {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.5;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
  20%, 40%, 60%, 80% { transform: translateX(5px); }
}

.animate-shake {
  animation: shake 0.6s cubic-bezier(.36,.07,.19,.97) both;
}

/* Efecto de vidrio realista - Glassmorphism */
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
  padding: 1.25rem;
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

.glass-input {
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  font-size: 0.875rem;
  color: #1f2937;
  transition: all 0.3s ease;
  box-shadow: 
    0 4px 16px 0 rgba(31, 38, 135, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  min-height: 36px;
  padding: 0.75rem;
}

.glass-input:focus {
  outline: none;
  border: 1px solid rgba(76, 175, 80, 0.4);
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 0 0 3px rgba(76, 175, 80, 0.1),
    0 8px 25px 0 rgba(31, 38, 135, 0.15),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

.glass-input::placeholder {
  color: rgba(75, 85, 99, 0.6);
}

.glass-button {
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(76, 175, 80, 0.3);
  background: linear-gradient(135deg, 
    rgba(76, 175, 80, 0.8) 0%, 
    rgba(56, 142, 60, 0.8) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 20px 0 rgba(76, 175, 80, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.glass-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 30px 0 rgba(76, 175, 80, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
  background: linear-gradient(135deg, 
    rgba(76, 175, 80, 0.9) 0%, 
    rgba(56, 142, 60, 0.9) 100%);
}

.glass-button:active:not(:disabled) {
  transform: translateY(0px);
  box-shadow: 
    0 4px 15px 0 rgba(76, 175, 80, 0.3),
    inset 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}

.glass-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: left 0.5s;
}

.glass-button:hover::before {
  left: 100%;
}

.glass-button-secondary {
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(156, 163, 175, 0.3);
  background: linear-gradient(135deg, 
    rgba(156, 163, 175, 0.6) 0%, 
    rgba(107, 114, 128, 0.6) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 20px 0 rgba(156, 163, 175, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.glass-button-secondary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 30px 0 rgba(156, 163, 175, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
}

.glass-button-action {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.1) 0%, 
    rgba(255, 255, 255, 0.05) 100%);
}

.glass-button-action:hover:not(:disabled) {
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  box-shadow: 
    0 8px 32px 0 rgba(31, 38, 135, 0.25),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
}

/* Estilos específicos para botones de entrada (azul) */
.glass-button-entrada {
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(30, 144, 255, 0.3);
  background: linear-gradient(135deg, 
    rgba(30, 144, 255, 0.8) 0%, 
    rgba(25, 118, 210, 0.8) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 20px 0 rgba(30, 144, 255, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.glass-button-entrada:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 30px 0 rgba(30, 144, 255, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
  background: linear-gradient(135deg, 
    rgba(30, 144, 255, 0.9) 0%, 
    rgba(25, 118, 210, 0.9) 100%);
}

.glass-button-entrada:active:not(:disabled) {
  transform: translateY(0px);
  box-shadow: 
    0 4px 15px 0 rgba(30, 144, 255, 0.3),
    inset 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}

.glass-button-entrada::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: left 0.5s;
}

.glass-button-entrada:hover::before {
  left: 100%;
}

/* Estilos específicos para botones de salida (rojo) */
.glass-button-salida {
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(220, 20, 60, 0.3);
  background: linear-gradient(135deg, 
    rgba(220, 20, 60, 0.8) 0%, 
    rgba(183, 28, 28, 0.8) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 20px 0 rgba(220, 20, 60, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.glass-button-salida:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 30px 0 rgba(220, 20, 60, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
  background: linear-gradient(135deg, 
    rgba(220, 20, 60, 0.9) 0%, 
    rgba(183, 28, 28, 0.9) 100%);
}

.glass-button-salida:active:not(:disabled) {
  transform: translateY(0px);
  box-shadow: 
    0 4px 15px 0 rgba(220, 20, 60, 0.3),
    inset 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}

.glass-button-salida::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: left 0.5s;
}

.glass-button-salida:hover::before {
  left: 100%;
}

/* Estilos específicos para botones de registro (morado) */
.glass-button-registro {
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  border: 1px solid rgba(128, 0, 128, 0.3);
  background: linear-gradient(135deg, 
    rgba(128, 0, 128, 0.8) 0%, 
    rgba(102, 16, 242, 0.8) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 20px 0 rgba(128, 0, 128, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.glass-button-registro:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 30px 0 rgba(128, 0, 128, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
  background: linear-gradient(135deg, 
    rgba(128, 0, 128, 0.9) 0%, 
    rgba(102, 16, 242, 0.9) 100%);
}

.glass-button-registro:active:not(:disabled) {
  transform: translateY(0px);
  box-shadow: 
    0 4px 15px 0 rgba(128, 0, 128, 0.3),
    inset 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}

.glass-button-registro::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: left 0.5s;
}

.glass-button-registro:hover::before {
  left: 100%;
}

.glass-link {
  position: relative;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.glass-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #4CAF50, #81C784);
  transition: width 0.3s ease;
  border-radius: 1px;
}

.glass-link:hover::after {
  width: 100%;
}

/* Estilos para títulos de entrada y salida con franja de fondo */
.entrada-title {
  color: rgb(30, 144, 255);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  letter-spacing: -0.01em;
  font-weight: 700;
  position: relative;
  padding: 0.75rem 1.5rem;
  margin: -0.75rem -1.25rem 0.5rem -1.25rem;
  background: linear-gradient(
    135deg, 
    rgba(30, 144, 255, 0.15) 0%,    /* Azul dodgerblue suave en bordes */
    rgba(30, 144, 255, 0.10) 25%,   /* Azul dodgerblue muy suave */
    rgba(30, 144, 255, 0.08) 50%,   /* Azul dodgerblue suave en el centro */
    rgba(30, 144, 255, 0.10) 75%,   /* Azul dodgerblue muy suave */
    rgba(30, 144, 255, 0.15) 100%   /* Azul dodgerblue suave en bordes */
  );
  border-left: 4px solid rgba(30, 144, 255, 0.6);
  border-radius: 0 8px 8px 0;
  box-shadow: 0 2px 8px rgba(30, 144, 255, 0.1);
}

.salida-title {
  color: rgb(220, 20, 60);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  letter-spacing: -0.01em;
  font-weight: 700;
  position: relative;
  padding: 0.75rem 1.5rem;
  margin: -0.75rem -1.25rem 0.5rem -1.25rem;
  background: linear-gradient(
    135deg, 
    rgba(220, 20, 60, 0.15) 0%,    /* Crimson fuerte suave en bordes */
    rgba(220, 20, 60, 0.10) 25%,   /* Crimson medio muy suave */
    rgba(220, 20, 60, 0.08) 50%,   /* Crimson suave en el centro */
    rgba(220, 20, 60, 0.10) 75%,   /* Crimson medio muy suave */
    rgba(220, 20, 60, 0.15) 100%   /* Crimson fuerte suave en bordes */
  );
  border-left: 4px solid rgba(220, 20, 60, 0.6);
  border-radius: 0 8px 8px 0;
  box-shadow: 0 2px 8px rgba(220, 20, 60, 0.1);
}

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
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  letter-spacing: -0.015em;
  font-weight: 500;
  position: relative;
}

.green-line {
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, #16a34a, #22c55e, #16a34a);
  border-radius: 1px;
  animation: line-glow 2s ease-in-out infinite alternate;
}

@keyframes gradient-wave {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
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

/* Animación para elementos decorativos */
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

/* Respaldo para navegadores que no soportan background-clip: text */
@supports not (-webkit-background-clip: text) {
  .modern-title {
    color: #166534;
    animation: none;
  }
}

/* Mejoras de responsividad para pantallas móviles */
@media (max-width: 480px) {
  .page-container {
    padding-left: 0.375rem;
    padding-right: 0.375rem;
    max-width: 100%;
  }
  
  .glass-card {
    padding: 0.75rem;
    margin: 0 0.125rem;
  }
  
  .glass-input {
    font-size: 14px; /* Evita zoom en iOS */
    min-height: 36px;
  }
  
  .text-xl {
    font-size: 1rem;
  }
  
  .text-lg {
    font-size: 0.875rem;
  }
  
  .text-base {
    font-size: 0.8rem;
  }
}

@media (max-height: 600px) {
  .page-container {
    max-width: 320px;
  }
  
  .glass-card {
    padding: 1rem;
  }
}

@media (max-height: 500px) {
  .glass-card {
    padding: 0.875rem;
  }
}

/* Para pantallas muy pequeñas como iPhone SE */
@media (max-width: 375px) and (max-height: 667px) {
  .page-container {
    max-width: 100%;
    padding-left: 0.25rem;
    padding-right: 0.25rem;
  }
  
  .glass-card {
    padding: 0.625rem;
    margin: 0;
  }
}

@media (max-height: 600px) {
  .page-container {
    max-width: 320px;
  }
  
  .glass-card {
    padding: 1rem;
  }
}

@media (max-height: 500px) {
  .glass-card {
    padding: 0.875rem;
  }
  
  .glass-input {
    font-size: 14px;
    min-height: 34px;
  }
}

/* Para pantallas grandes */
@media (min-width: 768px) {
  .page-container {
    max-width: 380px;
  }
  
  .glass-card {
    padding: 1.5rem;
  }
}

/* Soporte adicional para navegadores que no soportan backdrop-filter */
@supports not (backdrop-filter: blur(20px)) {
  .glass-card {
    background: rgba(255, 255, 255, 0.85);
  }
  
  .glass-input {
    background: rgba(255, 255, 255, 0.7);
  }
  
  .glass-button {
    background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%);
  }
  
  .glass-button-secondary {
    background: linear-gradient(135deg, #9CA3AF 0%, #6B7280 100%);
  }
}

/* Animación sutil para el botón de ubicación */
@keyframes pulse-subtle {
  0%, 100% {
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    transform: translateY(0);
  }
  50% {
    box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
    transform: translateY(-1px);
  }
}

/* Mejora de espaciado para evitar que se encimen las secciones */
.space-y-2 > * + * {
  margin-top: 0.5rem !important;
}

/* Asegurar que cada glass-card tenga su espacio definido */
.glass-card + .glass-card {
  margin-top: 0.5rem;
}

/* Espaciado específico para secciones condicionales */
.glass-card {
  margin-bottom: 0 !important; /* Remover margins bottom para usar space-y-2 */
  position: relative;
  z-index: 1;
}

/* Separación clara entre formulario de asistencia y actividades */
.page-container > .glass-card:not(:first-child) {
  clear: both;
  margin-top: 0.5rem;
}

/* Mensajes de estado sin interferir con otros elementos */
.text-center.mb-2 {
  position: relative;
  z-index: 2;
  margin-bottom: 0.5rem !important;
}

/* Estilos para botones de navegación entre secciones */
.section-nav-button {
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.section-nav-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.section-nav-button:hover::before {
  left: 100%;
}

.section-nav-button.active {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.section-nav-container {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 4px 16px 0 rgba(31, 38, 135, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
}

/* Nuevos estilos para botones de ubicación circulares con diseño moderno */
.location-container-circular {
  position: relative;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.location-button-circular {
  background: linear-gradient(135deg, 
    rgba(255, 200, 0, 1) 0%,         /* Gold más intenso */
    rgba(238, 180, 34, 1) 40%,       /* Goldenrod más saturado */
    rgba(204, 149, 11, 1) 100%       /* Gold profundo más intenso */
  );
  border: 3px solid rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: 
    0 8px 25px 0 rgba(0, 0, 0, 0.2),
    inset 0 2px 0 0 rgba(255, 255, 255, 0.5),
    inset 0 -2px 0 0 rgba(0, 0, 0, 0.2);
  position: relative;
  overflow: hidden;
  font-family: 'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  font-weight: 600;
  letter-spacing: 0.01em;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.location-button-circular:hover:not(:disabled) {
  transform: translateY(-3px) scale(1.12);
  box-shadow: 
    0 12px 35px 0 rgba(0, 0, 0, 0.3),
    inset 0 3px 0 0 rgba(255, 255, 255, 0.7),
    inset 0 -2px 0 0 rgba(0, 0, 0, 0.2);
  background: linear-gradient(135deg, 
    rgba(255, 180, 0, 1) 0%,
    rgba(255, 165, 0, 1) 40%,
    rgba(224, 140, 0, 1) 100%
  );
  border-color: rgba(255, 255, 255, 0.8);
}

.location-button-circular:active:not(:disabled) {
  transform: translateY(-1px) scale(1.06);
  box-shadow: 
    0 6px 25px 0 rgba(255, 215, 0, 0.45),
    inset 0 2px 4px 0 rgba(0, 0, 0, 0.15);
}

/* Estado de éxito circular - versión simple sin efectos excesivos */
.location-button-success-circular {
  background: linear-gradient(135deg, 
    rgba(154, 255, 0, 0.9) 0%,
    rgba(124, 230, 0, 0.9) 50%,
    rgba(100, 200, 0, 0.9) 100%
  ) !important;
  backdrop-filter: blur(10px) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  border: 2px solid rgba(154, 255, 0, 0.8) !important;
  box-shadow: 
    0 4px 12px 0 rgba(0, 0, 0, 0.15),
    0 0 4px 1px rgba(154, 255, 0, 0.2) !important;
  position: relative;
  overflow: hidden;
}

.location-button-success-circular:hover:not(:disabled) {
  background: linear-gradient(135deg, 
    rgba(140, 240, 0, 0.9) 0%,
    rgba(115, 215, 0, 0.9) 50%,
    rgba(95, 185, 0, 0.9) 100%
  ) !important;
  border: 2px solid rgba(140, 240, 0, 0.8) !important;
  box-shadow: 
    0 6px 16px 0 rgba(0, 0, 0, 0.2),
    0 0 6px 1px rgba(140, 240, 0, 0.3) !important;
  transform: translateY(-1px) scale(1.02);
}

/* Efecto de ondas para el botón normal circular */
.location-button-circular::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.4) 0%, transparent 70%);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.6s ease, height 0.6s ease, opacity 0.6s ease;
  opacity: 0;
}

.location-button-circular:hover::before {
  width: 120%;
  height: 120%;
  opacity: 1;
}

/* Contenedor y estilos para las coordenadas circulares */
.coordinates-display-circular {
  margin-top: 0.5rem;
  background: linear-gradient(135deg, 
    rgba(21, 128, 61, 0.25) 0%,
    rgba(15, 118, 110, 0.35) 100%
  );
  border: 1px solid rgba(34, 197, 94, 0.6);
  border-radius: 12px;
  padding: 0.5rem;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 
    0 3px 12px 0 rgba(34, 197, 94, 0.3),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.15);
  animation: slide-down-circular 0.4s ease-out;
  max-width: 160px;
  width: 100%;
}

.coordinates-grid-circular {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.coordinate-item-circular {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 0.25rem;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 6px;
  border: 1px solid rgba(173, 255, 47, 0.15);
}

.coordinate-label-circular {
  font-size: 0.5rem;
  font-weight: 600;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 0.125rem;
  font-family: 'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.coordinate-value-circular {
  font-family: 'SF Mono', 'Monaco', 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
  font-size: 0.5rem;
  font-weight: 600;
  color: rgb(21, 128, 61);
  background: rgba(255, 255, 255, 0.7);
  padding: 0.125rem 0.25rem;
  border-radius: 4px;
  border: 1px solid rgba(34, 197, 94, 0.25);
  word-break: break-all;
  line-height: 1.1;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.08);
}

/* Estilos para los elementos dentro del botón circular de vidrio */
.glass-text-circular {
  color: rgba(6, 78, 59, 0.95);
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.6);
  letter-spacing: 0.02em;
  font-weight: 500;
  line-height: 1.1;
  font-family: 'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.glass-icon-circular {
  filter: drop-shadow(0 1px 2px rgba(255, 255, 255, 0.6));
  color: rgba(6, 78, 59, 0.8) !important;
  opacity: 0.95;
}

/* Efectos para el botón circular Obtener Ubicación */
.location-text-circular {
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
  transition: all 0.3s ease;
  line-height: 1.1;
  font-family: 'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  font-weight: 500;
}

.location-icon-circular {
  filter: drop-shadow(0 1px 3px rgba(0, 0, 0, 0.4));
  transition: all 0.3s ease;
}

.location-button-circular:hover .location-text-circular {
  letter-spacing: 0.03em;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.location-button-circular:hover .location-icon-circular {
  transform: scale(1.1);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.5));
}

/* Animaciones para botones circulares */
@keyframes slide-down-circular {
  0% {
    opacity: 0;
    transform: translateY(-15px) scale(0.9);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Responsive para botones circulares */
@media (max-width: 480px) {
  .location-button-circular {
    width: 6rem !important; /* 24 - más grande */
    height: 6rem !important; /* 24 - más grande */
  }
  
  .location-icon-circular,
  .glass-icon-circular {
    width: 1.5rem !important; /* h-6 w-6 */
    height: 1.5rem !important;
  }
  
  .location-text-circular,
  .glass-text-circular {
    font-size: 0.625rem !important; /* text-xs */
    line-height: 1 !important;
  }
  
  .coordinates-display-circular {
    padding: 0.375rem;
    max-width: 160px;
  }
  
  .coordinate-label-circular {
    font-size: 0.4rem;
    color: white;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  }
  
  .coordinate-value-circular {
    font-size: 0.4rem;
    padding: 0.125rem 0.1875rem;
    font-weight: 600;
    color: rgb(21, 128, 61);
  }
  
  .coordinates-grid-circular {
    gap: 0.375rem;
  }
}

/* Nuevos estilos para botones de ubicación con diseño azul moderno */
.location-container {
  position: relative;
  margin-bottom: 1rem;
}

.location-button {
  background: linear-gradient(135deg, 
    rgba(255, 200, 0, 1) 0%,      /* Gold más intenso */
    rgba(238, 180, 34, 1) 50%,    /* Goldenrod más fuerte */
    rgba(204, 149, 11, 1) 100%    /* Gold oscuro más saturado */
  );
  border: 3px solid rgba(255, 215, 0, 1);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  box-shadow: 
    0 6px 20px 0 rgba(0, 0, 0, 0.2),
    inset 0 2px 0 0 rgba(255, 255, 255, 0.4),
    inset 0 -2px 0 0 rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  font-weight: 600;
  letter-spacing: 0.025em;
  text-shadow: 0 2px 3px rgba(0, 0, 0, 0.4);
}

.location-button:hover:not(:disabled) {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 
    0 10px 25px 0 rgba(0, 0, 0, 0.3),
    inset 0 2px 0 0 rgba(255, 255, 255, 0.5),
    inset 0 -2px 0 0 rgba(0, 0, 0, 0.15);
  background: linear-gradient(135deg, 
    rgba(255, 180, 0, 1) 0%,
    rgba(255, 165, 0, 1) 50%,
    rgba(224, 140, 0, 1) 100%
  );
  border-color: rgba(255, 215, 0, 1);
}

.location-button:active:not(:disabled) {
  transform: translateY(-1px) scale(1.01);
  box-shadow: 
    0 6px 20px 0 rgba(255, 215, 0, 0.4),
    inset 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}

/* Estado de éxito con efecto de vidrio (glassmorphism) y color greenyellow */
.location-button-success {
  background: rgba(154, 255, 0, 0.8) !important; /* Verde más intenso */
  backdrop-filter: blur(15px) !important;
  -webkit-backdrop-filter: blur(15px) !important;
  border: 3px solid rgba(154, 255, 0, 1) !important;
  border-top: 3px solid rgba(255, 255, 255, 0.7) !important;
  border-left: 3px solid rgba(255, 255, 255, 0.7) !important;
  box-shadow: 
    0 8px 25px 0 rgba(0, 0, 0, 0.25),
    0 0 6px 1px rgba(154, 255, 0, 0.25),
    inset 0 2px 0 0 rgba(255, 255, 255, 0.6),
    inset 0 -2px 0 0 rgba(0, 0, 0, 0.15);
  color: rgba(0, 40, 20, 0.9) !important;
  text-shadow: 0 2px 2px rgba(255, 255, 255, 0.7) !important;
  animation: glass-shine 3s ease-in-out infinite;
  position: relative;
  overflow: hidden;
}

/* Efecto de brillo para botones con efecto de vidrio */
@keyframes glass-shine {
  0% {
    background: rgba(154, 255, 0, 0.8);
    box-shadow: 
      0 8px 25px 0 rgba(0, 0, 0, 0.25),
      0 0 6px 1px rgba(154, 255, 0, 0.25);
  }
  50% {
    background: rgba(127, 255, 0, 1);
    box-shadow: 
      0 10px 30px 0 rgba(0, 0, 0, 0.3),
      0 0 10px 2px rgba(127, 255, 0, 0.35);
  }
  100% {
    background: rgba(154, 255, 0, 0.8);
    box-shadow: 
      0 8px 25px 0 rgba(0, 0, 0, 0.25),
      0 0 6px 1px rgba(154, 255, 0, 0.25);
  }
}

.location-button-success:hover:not(:disabled) {
  background: rgba(127, 255, 0, 1) !important;
  border: 3px solid rgba(127, 255, 0, 1) !important;
  border-top: 3px solid rgba(255, 255, 255, 0.8) !important;
  border-left: 3px solid rgba(255, 255, 255, 0.8) !important;
  box-shadow: 
    0 10px 30px 0 rgba(0, 0, 0, 0.3),
    inset 0 2px 0 0 rgba(255, 255, 255, 0.7);
  transform: translateY(-3px) scale(1.03);
}

/* Efecto de reflejos para el botón de ubicación obtenida */
.location-button-success::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    to right,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  transform: rotate(30deg);
  animation: glass-sweep 6s infinite linear;
}

@keyframes glass-sweep {
  0% {
    transform: rotate(30deg) translateX(-100%);
  }
  50% {
    transform: rotate(30deg) translateX(100%);
  }
  100% {
    transform: rotate(30deg) translateX(100%);
  }
}

/* Efecto de brillo para el botón normal */
.location-button::before {
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
  transition: left 0.6s;
}

.location-button:hover::before {
  left: 100%;
}

/* Contenedor y estilos para las coordenadas */
.coordinates-display {
  margin-top: 0.5rem;
  background: linear-gradient(135deg, 
    rgba(255, 215, 0, 0.08) 0%,
    rgba(218, 165, 32, 0.12) 100%
  );
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: 8px;
  padding: 0.5rem;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 
    0 2px 8px 0 rgba(255, 215, 0, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
  animation: slide-down 0.3s ease-out;
}

.coordinates-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.coordinate-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.coordinate-label {
  font-size: 0.5rem;
  font-weight: 600;
  color: rgba(255, 215, 0, 0.8);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.125rem;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.coordinate-value {
  font-family: 'SF Mono', 'Monaco', 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
  font-size: 0.6rem;
  font-weight: 600;
  color: rgba(218, 165, 32, 0.9);
  background: rgba(255, 255, 255, 0.6);
  padding: 0.125rem 0.25rem;
  border-radius: 4px;
  border: 1px solid rgba(255, 215, 0, 0.15);
  word-break: break-all;
  line-height: 1.1;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);
}

/* Estilos para los elementos dentro del botón de vidrio */
.glass-text {
  color: rgba(0, 40, 20, 0.9);
  text-shadow: 0 1px 1px rgba(255, 255, 255, 0.5);
  letter-spacing: 0.05em;
  font-weight: 600;
}

.glass-icon {
  filter: drop-shadow(0 1px 1px rgba(255, 255, 255, 0.5));
  color: rgba(0, 40, 20, 0.7) !important;
  opacity: 0.9;
}

.text-dark-green {
  color: rgba(0, 40, 20, 0.8);
}

/* Efectos para el botón Obtener Ubicación */
.location-text {
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
}

.location-icon {
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.3));
  transition: all 0.3s ease;
}

.location-button:hover .location-text {
  letter-spacing: 0.05em;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
}

.location-button:hover .location-icon {
  transform: scale(1.1);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.4));
}

/* Animaciones */
@keyframes success-pulse {
  0%, 100% {
    box-shadow: 
      0 8px 32px 0 rgba(63, 222, 153, 0.4),
      0 0 0 1px rgba(255, 255, 255, 0.2),
      inset 0 1px 0 0 rgba(255, 255, 255, 0.4);
  }
  50% {
    box-shadow: 
      0 8px 32px 0 rgba(63, 222, 153, 0.6),
      0 0 0 2px rgba(63, 222, 153, 0.3),
      inset 0 1px 0 0 rgba(255, 255, 255, 0.5);
  }
}

@keyframes slide-down {
  0% {
    opacity: 0;
    transform: translateY(-10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive para coordenadas */
@media (max-width: 480px) {
  .coordinates-display {
    padding: 0.375rem;
  }
  
  .coordinate-label {
    font-size: 0.45rem;
  }
  
  .coordinate-value {
    font-size: 0.55rem;
    padding: 0.1rem 0.2rem;
  }
  
  .coordinates-grid {
    gap: 0.375rem;
  }
  
  .location-button {
    padding: 0.75rem 1rem;
  }
}

/* Animaciones para el efecto vidrio líquido */
@keyframes float {
  0%, 100% {
    transform: translateY(0px) scale(1);
    opacity: 0.6;
  }
  50% {
    transform: translateY(-4px) scale(1.1);
    opacity: 0.8;
  }
}

@keyframes shimmer {
  0% {
    transform: skew(6deg) translateX(-200%);
  }
  100% {
    transform: skew(6deg) translateX(200%);
  }
}

@keyframes liquid-float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  33% {
    transform: translateY(-2px) rotate(1deg);
  }
  66% {
    transform: translateY(1px) rotate(-1deg);
  }
}

/* Clases para las animaciones */
.animate-float {
  animation: float 3s ease-in-out infinite;
}

.animate-shimmer {
  animation: shimmer 3s ease-in-out infinite;
}

.animate-liquid-float {
  animation: liquid-float 4s ease-in-out infinite;
}

/* Efectos adicionales para el vidrio líquido */
.glass-liquid {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.2),
    rgba(255, 255, 255, 0.1)
  );
}

.liquid-glow {
  box-shadow: 
    0 4px 20px rgba(244, 63, 94, 0.15),
    0 0 40px rgba(244, 63, 94, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.soft-pulse {
  animation: soft-pulse 4s ease-in-out infinite;
}

@keyframes soft-pulse {
  0%, 100% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
}

/* Animación elegante para el mensaje de estado */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-5px) scale(0.98);
}

.fade-slide-enter-to,
.fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}

/* Estilos responsivos mejorados para botones de asistencia */
@media (min-width: 768px) {
  .grid.md\\:grid-cols-2 {
    align-items: stretch;
  }
  
  .grid.md\\:grid-cols-2 button {
    min-height: 140px;
  }
}

@media (max-width: 767px) {
  .grid button {
    min-height: 120px;
  }
}

/* Asegurar que los botones tengan diseño consistente */
.grid button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  box-sizing: border-box;
}

/* Mejorar transiciones y hover effects */
.grid button:not(:disabled):hover {
  transform: scale(1.02);
}

.grid button:not(:disabled):active {
  transform: scale(0.98);
}
</style>
