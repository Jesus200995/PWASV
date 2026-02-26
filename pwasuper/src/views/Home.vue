<template>
  <div class="flex flex-col relative">
    <div class="page-container w-full max-w-lg mx-auto relative z-10 pt-0 pb-1 space-y-2">
      <!-- Botones de selección de sección -->
      <div v-if="!modoAsistencia" class="glass-card">
        <div class="text-center mb-3">
          <h1 class="text-xl font-medium text-yellow-600 title-shine" style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; letter-spacing: 0.05em; margin-bottom: -2px;">
            <span style="--char-index: 0">P</span><span style="--char-index: 1">a</span><span style="--char-index: 2">n</span><span style="--char-index: 3">e</span><span style="--char-index: 4">l</span><span class="space-char" style="--char-index: 5"> </span><span style="--char-index: 6">d</span><span style="--char-index: 7">e</span><span class="space-char" style="--char-index: 8"> </span><span style="--char-index: 9">R</span><span style="--char-index: 10">e</span><span style="--char-index: 11">g</span><span style="--char-index: 12">i</span><span style="--char-index: 13">s</span><span style="--char-index: 14">t</span><span style="--char-index: 15">r</span><span style="--char-index: 16">o</span>
          </h1>
          <p class="text-[9px] font-semibold tracking-widest uppercase mb-2" style="color: #EAB308;">Herramienta de apoyo</p>
          <div class="yellow-line mx-auto mb-1.5"></div>
          <p class="text-xs text-gray-500 mb-3">Selecciona el tipo de registro que deseas realizar</p>
          
          <!-- Botones de navegación entre secciones -->
          <div class="flex gap-2 section-nav-container p-1 rounded-full items-center">
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
                <span>Registro</span>
              </div>
            </button>
            
            <button
              @click="(!entradaMarcada || salidaMarcada) ? mostrarModalActividadesBloqueadas() : (seccionActiva = 'actividades')"
              :disabled="false"
              :class="[
                'section-nav-button flex-1 px-4 py-2 text-sm font-medium rounded-full transition-all duration-300',
                seccionActiva === 'actividades' && entradaMarcada && !salidaMarcada
                  ? 'active text-white shadow-lg' 
                  : (!entradaMarcada || salidaMarcada)
                    ? 'bg-gray-200 text-gray-500 cursor-pointer'
                    : 'text-gray-600 hover:bg-white/30'
              ]"
              :style="seccionActiva === 'actividades' && entradaMarcada && !salidaMarcada ? 'background-color: rgb(147, 51, 234);' : ''"
            >
              <div class="flex items-center justify-center space-x-2">
                <!-- Icono de actividades siempre visible -->
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                <span>Actividades</span>
              </div>
            </button>
          </div>
          
          <!-- Etiqueta BLOQUEADO centrada debajo de los botones -->
          <div v-if="!entradaMarcada || salidaMarcada" class="flex justify-end mt-0.5 mr-1">
            <span class="bg-gray-600 text-white text-[7px] font-semibold tracking-wider px-2 rounded-b-lg" style="padding-top: 1px; padding-bottom: 2px;">BLOQUEADO</span>
          </div>
        </div>
      </div>

      <!-- Sistema de Asistencia Integrado -->
      <div v-if="seccionActiva === 'asistencia' || modoAsistencia" :class="modoAsistencia ? (tipoAsistencia === 'entrada' ? 'glass-card-blue relative px-0 py-2' : 'glass-card-red relative px-0 py-2') : 'relative px-0 py-2'">
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
          <h2 class="text-xl font-semibold text-green-700 mb-1" style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; letter-spacing: -0.02em;">Control de Jornada</h2>
          <p class="text-xs text-gray-500">
            {{ modoAsistencia ? 'Completa los datos para ' + (tipoAsistencia === 'entrada' ? 'registro de inicio' : 'registro de término') : 'Registra tu inicio y término de jornada' }}
          </p>
        </div>

        <!-- Botones de Asistencia (solo visibles cuando no está en modo asistencia) -->
        <div v-if="!modoAsistencia" class="flex gap-3 mb-2">
        <!-- Botón Marcar Entrada -->
        <button
          @click="mostrarModalEntrada"
          :disabled="entradaMarcada || verificandoAsistencia"
          class="relative overflow-hidden rounded-2xl transition-all duration-300 transform min-h-[200px] flex-1 flex flex-col items-center justify-center p-4"
          :class="{
            'text-white shadow-xl hover:scale-[1.02] active:scale-[0.98]': !entradaMarcada && !verificandoAsistencia,
            'bg-gradient-to-b from-gray-50 to-gray-100 text-gray-500 cursor-not-allowed border border-gray-200': entradaMarcada || verificandoAsistencia
          }"
          :style="!entradaMarcada && !verificandoAsistencia ? 'background: linear-gradient(135deg, rgb(30, 144, 255) 0%, rgb(0, 119, 230) 100%); box-shadow: 0 10px 30px rgba(30, 144, 255, 0.5);' : ''"
        >
          <!-- Efecto de burbujas de vidrio flotantes -->
          <div v-if="!entradaMarcada && !verificandoAsistencia" class="absolute inset-0 pointer-events-none overflow-hidden rounded-2xl">
            <!-- Burbuja 1 -->
            <div class="absolute w-20 h-20 rounded-full bg-white/10 backdrop-blur-sm animate-bubble-1" style="left: 10%; bottom: -20%;"></div>
            <!-- Burbuja 2 -->
            <div class="absolute w-14 h-14 rounded-full bg-white/15 backdrop-blur-sm animate-bubble-2" style="left: 60%; bottom: -15%;"></div>
            <!-- Burbuja 3 -->
            <div class="absolute w-10 h-10 rounded-full bg-white/10 backdrop-blur-sm animate-bubble-3" style="left: 35%; bottom: -10%;"></div>
            <!-- Burbuja 4 -->
            <div class="absolute w-16 h-16 rounded-full bg-white/12 backdrop-blur-sm animate-bubble-4" style="left: 80%; bottom: -18%;"></div>
            <!-- Brillo superior suave -->
            <div class="absolute top-0 left-0 right-0 h-1/3 bg-gradient-to-b from-white/20 to-transparent"></div>
          </div>
          
          <div v-if="verificandoAsistencia" class="absolute inset-0 bg-white bg-opacity-20 flex items-center justify-center rounded-2xl z-10">
            <div class="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-current"></div>
          </div>
          
          <!-- Estado: No marcada - Activo -->
          <template v-if="!entradaMarcada && !verificandoAsistencia">
            <div class="relative z-10 flex flex-col items-center">
              <div class="w-14 h-14 sm:w-16 sm:h-16 rounded-full bg-white/25 flex items-center justify-center mb-3 backdrop-blur-sm shadow-lg border border-white/30">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 sm:h-9 sm:w-9" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </div>
              <span class="font-bold text-base sm:text-lg tracking-wide leading-tight text-center">Registro de Inicio</span>
              <span class="text-xs sm:text-sm opacity-90 mt-0.5">Inicia tu jornada</span>
            </div>
          </template>
          
          <!-- Estado: Marcada - Completada -->
          <template v-else-if="entradaMarcada">
            <div class="flex flex-col items-center pb-8">
              <div class="w-14 h-14 sm:w-16 sm:h-16 bg-blue-500 rounded-full flex items-center justify-center mb-3 shadow-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 sm:h-8 sm:w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span class="font-bold text-sm sm:text-base text-gray-700 leading-tight text-center">Inicio Registrado</span>
              <span class="text-sm text-gray-500 mt-1">
                <span v-if="asistenciaHoy && asistenciaHoy.entrada">
                  {{ formatearHora(asistenciaHoy.entrada) }}
                </span>
                <span v-else-if="datosEntrada.hora">
                  {{ datosEntrada.hora }}
                </span>
              </span>
            </div>
            <!-- Barra de Completado -->
            <div class="absolute bottom-0 left-0 right-0 py-1.5 rounded-b-2xl" style="background-color: #d4a000;">
              <span class="text-xs text-white font-bold tracking-wider">COMPLETADO</span>
            </div>
          </template>
        </button>

        <!-- Separador vertical decorativo -->
        <div class="w-px bg-gradient-to-b from-transparent via-gray-300 to-transparent self-stretch my-4"></div>

        <!-- Botón Marcar Salida -->
        <button
          @click="mostrarModalSalida"
          :disabled="!entradaMarcada || salidaMarcada || verificandoAsistencia"
          class="relative overflow-hidden rounded-2xl transition-all duration-300 transform min-h-[200px] flex-1 flex flex-col items-center justify-center p-4"
          :class="{
            'text-white shadow-xl hover:scale-[1.02] active:scale-[0.98]': entradaMarcada && !salidaMarcada && !verificandoAsistencia,
            'bg-gradient-to-b from-gray-50 to-gray-100 text-gray-500 cursor-not-allowed border border-gray-200': !entradaMarcada || salidaMarcada || verificandoAsistencia
          }"
          :style="entradaMarcada && !salidaMarcada && !verificandoAsistencia ? 'background: linear-gradient(135deg, rgb(220, 20, 60) 0%, rgb(180, 15, 50) 100%); box-shadow: 0 10px 30px rgba(220, 20, 60, 0.5);' : ''"
        >
          <!-- Efecto de burbujas de vidrio flotantes -->
          <div v-if="entradaMarcada && !salidaMarcada && !verificandoAsistencia" class="absolute inset-0 pointer-events-none overflow-hidden rounded-2xl">
            <!-- Burbuja 1 -->
            <div class="absolute w-20 h-20 rounded-full bg-white/10 backdrop-blur-sm animate-bubble-1" style="left: 10%; bottom: -20%;"></div>
            <!-- Burbuja 2 -->
            <div class="absolute w-14 h-14 rounded-full bg-white/15 backdrop-blur-sm animate-bubble-2" style="left: 60%; bottom: -15%;"></div>
            <!-- Burbuja 3 -->
            <div class="absolute w-10 h-10 rounded-full bg-white/10 backdrop-blur-sm animate-bubble-3" style="left: 35%; bottom: -10%;"></div>
            <!-- Burbuja 4 -->
            <div class="absolute w-16 h-16 rounded-full bg-white/12 backdrop-blur-sm animate-bubble-4" style="left: 80%; bottom: -18%;"></div>
            <!-- Brillo superior suave -->
            <div class="absolute top-0 left-0 right-0 h-1/3 bg-gradient-to-b from-white/20 to-transparent"></div>
          </div>
          
          <div v-if="verificandoAsistencia" class="absolute inset-0 bg-white bg-opacity-20 flex items-center justify-center rounded-2xl z-10">
            <div class="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-current"></div>
          </div>
          
          <!-- Estado: Activo para marcar salida -->
          <template v-if="entradaMarcada && !salidaMarcada && !verificandoAsistencia">
            <div class="relative z-10 flex flex-col items-center">
              <div class="w-14 h-14 sm:w-16 sm:h-16 rounded-full bg-white/25 flex items-center justify-center mb-3 backdrop-blur-sm shadow-lg border border-white/30">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 sm:h-9 sm:w-9" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </div>
              <span class="font-bold text-base sm:text-lg tracking-wide leading-tight text-center">Registro de Término</span>
              <span class="text-xs sm:text-sm opacity-90 mt-0.5">Finaliza tu jornada</span>
            </div>
          </template>
          
          <!-- Estado: Bloqueado (sin entrada) -->
          <template v-else-if="!entradaMarcada">
            <!-- Contenido centrado con padding inferior para la barra -->
            <div class="flex flex-col items-center pb-10">
              <div class="w-14 h-14 sm:w-16 sm:h-16 bg-gray-300 rounded-full flex items-center justify-center mb-2 shadow-inner">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 sm:h-8 sm:w-8 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <span class="font-bold text-sm sm:text-base text-gray-600 leading-tight text-center">Registro de Término</span>
              <span class="text-xs sm:text-sm text-gray-500 mt-0.5">Primero registra tu inicio</span>
            </div>
            <!-- Barra de Bloqueado de lado a lado -->
            <div class="absolute bottom-0 left-0 right-0 bg-gray-500 py-2 rounded-b-2xl">
              <span class="text-sm text-white font-bold tracking-wider">BLOQUEADO</span>
            </div>
          </template>
          
          <!-- Estado: Salida completada -->
          <template v-else-if="salidaMarcada">
            <div class="flex flex-col items-center pb-8">
              <div class="w-14 h-14 sm:w-16 sm:h-16 bg-red-500 rounded-full flex items-center justify-center mb-3 shadow-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 sm:h-8 sm:w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span class="font-bold text-sm sm:text-base text-gray-700 leading-tight text-center">Término Registrado</span>
              <span class="text-xs sm:text-sm text-gray-500 mt-0.5">
                <span v-if="asistenciaHoy && asistenciaHoy.salida">
                  {{ formatearHora(asistenciaHoy.salida) }}
                </span>
                <span v-else-if="datosSalida.hora">
                  {{ datosSalida.hora }}
                </span>
              </span>
            </div>
            <!-- Barra de Completado -->
            <div class="absolute bottom-0 left-0 right-0 py-1.5 rounded-b-2xl" style="background-color: #d4a000;">
              <span class="text-xs text-white font-bold tracking-wider">COMPLETADO</span>
            </div>
          </template>
        </button>
      </div>

        <!-- Aviso amigable sobre registro de asistencia -->
        <div v-if="!modoAsistencia" class="text-center mb-2 relative">
          <!-- Contenedor principal estilo empresarial -->
          <div class="relative bg-white/95 backdrop-blur-lg rounded-xl shadow-lg border border-gray-200/50 overflow-hidden">
            <!-- Barra lateral de acento -->
            <div class="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-amber-500 via-orange-500 to-red-500"></div>
            
            <!-- Contenido principal -->
            <div class="relative p-4 pl-5">
              <!-- Header con icono y título -->
              <div class="flex items-center gap-3 mb-3 pb-3 border-b border-gray-200/60">
                <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-gradient-to-br from-amber-50 to-orange-50 flex items-center justify-center border border-amber-200/50 shadow-sm">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div class="flex-1 text-left">
                  <h3 class="text-sm font-bold text-gray-800 tracking-tight">Información Importante</h3>
                  <p class="text-[10px] text-gray-500 font-medium mt-0.5">Requisitos de jornada</p>
                </div>
              </div>
              
              <!-- Lista de información -->
              <div class="space-y-2.5">
                <!-- Item 1 -->
                <div class="flex items-start gap-3 group">
                  <div class="flex-shrink-0 mt-0.5 w-6 h-6 rounded-md bg-blue-50 flex items-center justify-center border border-blue-200/50 group-hover:bg-blue-100 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div class="flex-1 text-left">
                    <p class="text-xs font-semibold text-gray-700 leading-tight">Registro de inicio requerido</p>
                    <p class="text-[10px] text-gray-500 mt-0.5 leading-relaxed">Debe registrar su inicio para acceder al módulo de actividades</p>
                  </div>
                </div>
                
                <!-- Item 2 -->
                <div class="flex items-start gap-3 group">
                  <div class="flex-shrink-0 mt-0.5 w-6 h-6 rounded-md bg-red-50 flex items-center justify-center border border-red-200/50 group-hover:bg-red-100 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div class="flex-1 text-left">
                    <p class="text-xs font-semibold text-gray-700 leading-tight">Cierre de jornada</p>
                    <p class="text-[10px] text-gray-500 mt-0.5 leading-relaxed">El registro de término finaliza el acceso del día actual</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Mensaje de estado de asistencia -->
        <div v-if="mensajeAsistencia && !modoAsistencia" class="flex justify-center mb-3">
          <transition name="fade-slide">
            <div 
              class="inline-flex items-center px-3 py-1.5 rounded-2xl text-xs font-medium shadow-sm border backdrop-blur-md"
              :class="{
                'bg-gradient-to-r from-emerald-50 to-green-50 text-emerald-700 border-emerald-200': mensajeAsistencia.includes('éxito') || mensajeAsistencia.includes('registrada') || mensajeAsistencia.includes('Sincronización exitosa'),
                'bg-gradient-to-r from-red-50 to-rose-50 text-red-700 border-red-200': mensajeAsistencia.includes('Error') || mensajeAsistencia.includes('error'),
                'bg-gradient-to-r from-slate-50 to-slate-100 text-slate-700 border-slate-300': mensajeAsistencia.includes('Sincronización') || mensajeAsistencia.includes('progreso'),
                'bg-gradient-to-r from-amber-50 to-yellow-50 text-amber-700 border-amber-200': mensajeAsistencia.includes('Ya') || mensajeAsistencia.includes('offline')
              }"
            >
              <svg v-if="mensajeAsistencia.includes('éxito') || mensajeAsistencia.includes('registrada') || mensajeAsistencia.includes('Sincronización exitosa')" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
              </svg>
              <svg v-else-if="mensajeAsistencia.includes('Error') || mensajeAsistencia.includes('error')" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
              </svg>
              <svg v-else-if="mensajeAsistencia.includes('Sincronización') || mensajeAsistencia.includes('progreso')" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1.5 animate-spin text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span class="text-xs tracking-wide">{{ mensajeAsistencia }}</span>
            </div>
          </transition>
        </div>

        <!-- Formulario de Asistencia (solo visible en modo asistencia) -->
        <div v-if="modoAsistencia" class="apple-attendance-container mt-2 pt-2">
          <!-- Header estilo Apple -->
          <div class="apple-header-card mb-3" :class="tipoAsistencia === 'entrada' ? 'apple-header-entrada' : 'apple-header-salida'">
            <div class="flex items-center justify-center">
              <div class="apple-header-icon mr-2">
                <svg v-if="tipoAsistencia === 'entrada'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </div>
              <h2 class="apple-header-title">
                {{ tipoAsistencia === 'entrada' ? 'Registro de Inicio' : 'Registro de Término' }}
              </h2>
            </div>
          </div>
          
          <!-- Info del usuario estilo Apple -->
          <div class="apple-user-card mb-3">
            <div class="flex items-center">
              <div class="apple-avatar" :class="tipoAsistencia === 'entrada' ? 'apple-avatar-blue' : 'apple-avatar-red'">
                <span class="apple-avatar-initials">{{ getUserInitials }}</span>
              </div>
              <div class="ml-3 flex-1">
                <p class="apple-user-name">{{ user.nombre_completo }}</p>
                <p class="apple-user-role">{{ user.cargo }}</p>
              </div>
              <div class="apple-status-badge" :class="tipoAsistencia === 'entrada' ? 'apple-badge-blue' : 'apple-badge-red'">
                {{ tipoAsistencia === 'entrada' ? 'Entrada' : 'Salida' }}
              </div>
            </div>
          </div>

          <!-- Paso 1: Ubicación -->
          <div class="apple-step-card mb-2">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center">
                <div class="apple-step-number">1</div>
                <h3 class="apple-step-title">Ubicación</h3>
              </div>
              <div v-if="latitud && longitud" class="apple-completed-badge">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
                Listo
              </div>
            </div>
            
          <!-- Botón de ubicación Apple circular -->
          <div class="apple-location-container">
            <div class="apple-location-wrapper">
              <!-- Botón circular principal -->
              <button
                type="button"
                @click="getUbicacion"
                :disabled="obteniendoUbicacion"
                class="apple-location-btn"
                :class="{
                  'apple-location-btn-loading': obteniendoUbicacion,
                  'apple-location-btn-success': latitud && longitud && !obteniendoUbicacion,
                  'apple-location-btn-default': !latitud && !longitud && !obteniendoUbicacion
                }"
              >
                <!-- Anillo de progreso animado -->
                <div v-if="obteniendoUbicacion" class="apple-location-ring">
                  <svg class="apple-location-ring-svg" viewBox="0 0 100 100">
                    <circle class="apple-location-ring-bg" cx="50" cy="50" r="45"/>
                    <circle class="apple-location-ring-progress" cx="50" cy="50" r="45"/>
                  </svg>
                </div>
                
                <!-- Pulso de éxito -->
                <div v-if="latitud && longitud && !obteniendoUbicacion" class="apple-location-pulse"></div>
                
                <!-- Icono central -->
                <div class="apple-location-icon">
                  <!-- Loading -->
                  <svg v-if="obteniendoUbicacion" xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <!-- Success -->
                  <svg v-else-if="latitud && longitud" xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                  <!-- Default -->
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
              </button>
              
              <!-- Texto de estado -->
              <div class="apple-location-info">
                <span class="apple-location-title">
                  <span v-if="obteniendoUbicacion">Obteniendo...</span>
                  <span v-else-if="latitud && longitud">Ubicación lista</span>
                  <span v-else>Obtener GPS</span>
                </span>
                <span class="apple-location-subtitle">
                  <span v-if="obteniendoUbicacion">Espera un momento</span>
                  <span v-else-if="latitud && longitud">Coordenadas capturadas</span>
                  <span v-else>Toca para activar</span>
                </span>
              </div>
            </div>
            
            <!-- Coordenadas compactas -->
            <div v-if="latitud && longitud" class="apple-coordinates">
              <div class="apple-coord-item">
                <span class="apple-coord-label">Lat</span>
                <span class="apple-coord-value">{{ parseFloat(latitud).toFixed(6) }}</span>
              </div>
              <div class="apple-coord-divider"></div>
              <div class="apple-coord-item">
                <span class="apple-coord-label">Lon</span>
                <span class="apple-coord-value">{{ parseFloat(longitud).toFixed(6) }}</span>
              </div>
            </div>
          </div>
        </div>

          <!-- Paso 2: Imagen -->
          <div class="apple-step-card mb-2">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center">
                <div class="apple-step-number">2</div>
                <h3 class="apple-step-title">Imagen</h3>
              </div>
              <div v-if="foto" class="apple-completed-badge">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
                Listo
              </div>
            </div>
            
            <!-- Vista previa de la foto -->
            <div v-if="foto" class="mb-3">
              <div class="apple-image-preview">
                <img :src="foto" class="w-full h-full object-cover" />
                <div class="apple-image-overlay">
                  <button
                    @click="eliminarFoto"
                    class="apple-delete-image-btn"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    <span class="ml-1.5">Eliminar</span>
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Botones para capturar foto -->
            <div v-if="!foto" class="apple-photo-buttons">
              <!-- Botón para tomar foto con cámara -->
              <button
                @click="tomarFotoConCamara"
                class="apple-photo-btn apple-photo-btn-camera"
              >
                <div class="apple-photo-btn-content">
                  <div class="apple-photo-btn-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <div class="apple-photo-btn-info">
                    <span class="apple-photo-btn-title">Cámara</span>
                    <span class="apple-photo-btn-subtitle">Tomar foto ahora</span>
                  </div>
                </div>
              </button>
              
              <!-- Botón para seleccionar de galería -->
              <button
                @click="seleccionarDeGaleria"
                class="apple-photo-btn apple-photo-btn-gallery"
              >
                <div class="apple-photo-btn-content">
                  <div class="apple-photo-btn-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div class="apple-photo-btn-info">
                    <span class="apple-photo-btn-title">Galería</span>
                    <span class="apple-photo-btn-subtitle">Seleccionar imagen</span>
                  </div>
                </div>
              </button>
            </div>
            
            <!-- Inputs ocultos para los diferentes tipos de captura -->
            <input
              type="file"
              accept="image/*"
              capture="environment"
              @change="onFileChange"
              class="hidden"
              ref="fileInputCamera"
            />
            <input
              type="file"
              accept="image/*"
              @change="onFileChange"
              class="hidden"
              ref="fileInputGallery"
            />
          </div>

          <!-- Paso 3: Descripción -->
          <div class="apple-step-card mb-2">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center">
                <div class="apple-step-number">3</div>
                <h3 class="apple-step-title">Descripción</h3>
              </div>
              <div v-if="descripcion.trim()" class="apple-completed-badge">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
                Listo
              </div>
            </div>
            
            <textarea
              v-model="descripcion"
              rows="2"
              class="apple-textarea"
              :placeholder="'Describe el lugar donde ' + (tipoAsistencia === 'entrada' ? 'inicias' : 'terminas') + ' tu jornada...'"
            ></textarea>
          </div>

          <!-- Checklist estilo Apple amarillo oscuro -->
          <div v-if="!puedeEnviarAsistencia" class="apple-checklist-card mt-2">
            <div class="apple-checklist-header">
              <div class="apple-checklist-icon">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
              <span class="apple-checklist-title">Completa los pasos</span>
            </div>
            <div class="apple-checklist-items">
              <!-- Ubicación -->
              <div :class="['apple-checklist-item', latitud && longitud ? 'apple-checklist-done' : 'apple-checklist-pending']">
                <div :class="['apple-checklist-check', latitud && longitud ? 'apple-check-done' : 'apple-check-pending']">
                  <svg v-if="latitud && longitud" xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <span>Ubicación</span>
              </div>
              <!-- Imagen -->
              <div :class="['apple-checklist-item', foto ? 'apple-checklist-done' : 'apple-checklist-pending']">
                <div :class="['apple-checklist-check', foto ? 'apple-check-done' : 'apple-check-pending']">
                  <svg v-if="foto" xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <span>Imagen</span>
              </div>
              <!-- Descripción -->
              <div :class="['apple-checklist-item', descripcion.trim() ? 'apple-checklist-done' : 'apple-checklist-pending']">
                <div :class="['apple-checklist-check', descripcion.trim() ? 'apple-check-done' : 'apple-check-pending']">
                  <svg v-if="descripcion.trim()" xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <span>Descripción</span>
              </div>
            </div>
          </div>
          
          <!-- Indicador de listo estilo Apple -->
          <div v-if="puedeEnviarAsistencia && !enviandoAsistencia" class="apple-ready-card mt-2">
            <div class="apple-ready-content">
              <div class="apple-ready-icon">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span class="apple-ready-text">¡Listo para registrar!</span>
            </div>
          </div>

          <!-- Botones de acción estilo Apple -->
          <div class="apple-action-buttons">
            <button
              @click="cancelarAsistencia"
              class="apple-btn-cancel"
            >
              <span>Cancelar</span>
            </button>
            
            <button
              @click="confirmarAsistencia"
              :disabled="!puedeEnviarAsistencia || enviandoAsistencia"
              class="apple-btn-submit"
              :class="[
                tipoAsistencia === 'entrada' ? 'apple-btn-entrada' : 'apple-btn-salida',
                {'apple-btn-disabled': !puedeEnviarAsistencia || enviandoAsistencia}
              ]"
            >
              <div v-if="enviandoAsistencia" class="apple-spinner">
                <div class="apple-spinner-ring"></div>
              </div>
              <template v-else>
                <svg v-if="tipoAsistencia === 'entrada'" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                <span>{{ tipoAsistencia === 'entrada' ? 'Registrar Entrada' : 'Registrar Salida' }}</span>
              </template>
            </button>
          </div>
        </div>
      </div>

    <!-- Modal de confirmación para entrada -->
    <ConfirmModal 
      :show="showEntradaModal" 
      title="Registro de Inicio"
      :message="entradaModalMessage"
      type="confirm"
      :showConfirm="true"
      confirmText="Registrar Inicio"
      cancelText="Cancelar"
      @close="closeEntradaModal"
      @confirm="confirmarEntradaModal"
    />
    
    <!-- Modal de confirmación para salida -->
    <ConfirmModal 
      :show="showSalidaModal" 
      title="Registro de Término"
      :message="salidaModalMessage"
      type="error"
      :showConfirm="true"
      confirmText="Registrar Término"
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
    <div v-if="seccionActiva === 'actividades' && !modoAsistencia" class="apple-activities-container">
      <!-- Mensaje de estado de actividades bloqueadas -->
      <div v-if="!entradaMarcada || salidaMarcada" class="apple-warning-card mb-4">
        <div class="flex items-center">
          <div class="apple-warning-icon">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="apple-warning-title">Registro de actividades bloqueado</h3>
            <p class="apple-warning-text">
              <span v-if="!entradaMarcada">Debes marcar tu entrada primero para registrar actividades.</span>
              <span v-else-if="salidaMarcada">Has marcado tu salida. No puedes registrar más actividades hoy.</span>
            </p>
          </div>
        </div>
      </div>

      <!-- Header estilo Apple morado -->
      <div class="apple-header-card apple-header-purple mb-3">
        <div class="flex items-center justify-center">
          <div class="apple-header-icon mr-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
          </div>
          <h2 class="apple-header-title">
            Registro de Actividades
          </h2>
        </div>
      </div>
      
      <!-- Info del usuario estilo Apple -->
      <div class="apple-user-card mb-3">
        <div class="flex items-center">
          <div class="apple-avatar apple-avatar-purple">
            <span class="apple-avatar-initials">{{ getUserInitials }}</span>
          </div>
          <div class="ml-3 flex-1">
            <p class="apple-user-name">{{ user.nombre_completo }}</p>
            <p class="apple-user-role">{{ user.cargo }}</p>
          </div>
          <div class="apple-status-badge apple-badge-purple">
            Actividades
          </div>
        </div>
      </div>

      <form @submit.prevent="enviarRegistro" :class="{ 'opacity-50 pointer-events-none': !entradaMarcada || salidaMarcada }">
        <!-- Paso 1: Ubicación -->
        <div class="apple-step-card-purple mb-2">
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center">
              <div class="apple-step-number-purple">1</div>
              <h3 class="apple-step-title">Ubicación</h3>
            </div>
            <div v-if="latitudRegistro && longitudRegistro" class="apple-completed-badge">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              Listo
            </div>
          </div>
          
          <!-- Botón de ubicación Apple circular para actividades -->
          <div class="apple-location-container">
            <div class="apple-location-wrapper">
              <!-- Botón circular principal -->
              <button
                type="button"
                @click="getUbicacionRegistro"
                :disabled="!entradaMarcada || salidaMarcada"
                class="apple-location-btn"
                :class="{
                  'apple-location-btn-disabled': !entradaMarcada || salidaMarcada,
                  'apple-location-btn-success': latitudRegistro && longitudRegistro && entradaMarcada && !salidaMarcada,
                  'apple-location-btn-default': entradaMarcada && !salidaMarcada && !latitudRegistro && !longitudRegistro
                }"
              >
                <!-- Pulso de éxito -->
                <div v-if="latitudRegistro && longitudRegistro && entradaMarcada && !salidaMarcada" class="apple-location-pulse"></div>
                
                <!-- Icono central -->
                <div class="apple-location-icon">
                  <!-- Bloqueado -->
                  <svg v-if="!entradaMarcada || salidaMarcada" xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                  <!-- Success -->
                  <svg v-else-if="latitudRegistro && longitudRegistro" xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                  <!-- Default -->
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
              </button>
              
              <!-- Texto de estado -->
              <div class="apple-location-info">
                <span class="apple-location-title">
                  <span v-if="!entradaMarcada">Bloqueado</span>
                  <span v-else-if="salidaMarcada">Cerrado</span>
                  <span v-else-if="latitudRegistro && longitudRegistro">Ubicación lista</span>
                  <span v-else>Obtener GPS</span>
                </span>
                <span class="apple-location-subtitle">
                  <span v-if="!entradaMarcada">Marca entrada primero</span>
                  <span v-else-if="salidaMarcada">Jornada finalizada</span>
                  <span v-else-if="latitudRegistro && longitudRegistro">Coordenadas capturadas</span>
                  <span v-else>Toca para activar</span>
                </span>
              </div>
            </div>
            
            <!-- Coordenadas compactas -->
            <div v-if="latitudRegistro && longitudRegistro && entradaMarcada && !salidaMarcada" class="apple-coordinates">
              <div class="apple-coord-item">
                <span class="apple-coord-label">Lat</span>
                <span class="apple-coord-value">{{ parseFloat(latitudRegistro).toFixed(6) }}</span>
              </div>
              <div class="apple-coord-divider"></div>
              <div class="apple-coord-item">
                <span class="apple-coord-label">Lon</span>
                <span class="apple-coord-value">{{ parseFloat(longitudRegistro).toFixed(6) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Paso 2: Modalidad - Campo o Gabinete -->
        <div class="apple-step-card-purple mb-2">
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center">
              <div class="apple-step-number-purple">2</div>
              <h3 class="apple-step-title">Modalidad</h3>
            </div>
            <div v-if="tipoActividad" class="apple-completed-badge">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              Listo
            </div>
          </div>
          
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
              <p class="text-xs text-red-500 font-medium animate-pulse">Por favor selecciona la modalidad</p>
            </div>
          </div>
        </div>

        <!-- Paso 3: Categoría de Actividad -->
        <div class="apple-step-card-purple mb-2">
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center">
              <div class="apple-step-number-purple">3</div>
              <h3 class="apple-step-title">Categoría</h3>
            </div>
            <div v-if="categoriaActividad && (categoriaActividad !== 'Otro' || categoriaActividadOtro.trim())" class="apple-completed-badge">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              Listo
            </div>
          </div>
          <label class="block text-xs font-medium mb-2 flex items-center"
                 :class="{ 
                   'text-gray-400': !entradaMarcada || salidaMarcada || !tipoActividad,
                   'text-gray-700': entradaMarcada && !salidaMarcada && tipoActividad
                 }">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1.5" :class="{ 'text-gray-400': !entradaMarcada || salidaMarcada || !tipoActividad, 'text-purple-600': entradaMarcada && !salidaMarcada && tipoActividad }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
            Tipo de Actividad <span class="text-red-500 text-sm ml-1">*</span>
          </label>
          
          <div class="relative">
            <select
              v-model="categoriaActividad"
              :disabled="!entradaMarcada || salidaMarcada || !tipoActividad"
              class="apple-select w-full text-sm appearance-none pr-10"
              :class="{ 
                'opacity-50 cursor-not-allowed': !entradaMarcada || salidaMarcada || !tipoActividad,
                'border-red-400': !categoriaActividad && tipoActividad && entradaMarcada && !salidaMarcada
              }"
            >
              <option value="" disabled>{{ !tipoActividad ? '-- Primero selecciona la modalidad --' : '-- Selecciona el tipo de actividad --' }}</option>
              <option v-for="categoria in categoriasActividad" :key="categoria" :value="categoria">
                {{ categoria }}
              </option>
            </select>
            <!-- Icono de flecha para el select -->
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-purple-500">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
          
          <!-- Mensaje de error si no se ha seleccionado tipo de actividad -->
          <div v-if="!categoriaActividad && tipoActividad && entradaMarcada && !salidaMarcada" class="mt-1.5">
            <p class="text-xs text-red-500 font-medium animate-pulse">Por favor selecciona el tipo de actividad</p>
          </div>

          <!-- Campo para especificar "Otro" si se selecciona esa opción -->
          <div v-if="categoriaActividad === 'Otro'" class="mt-3">
            <label class="apple-input-label flex items-center mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1.5 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              Especifica cuál <span class="text-red-500 text-sm ml-1">*</span>
            </label>
            
            <input
              type="text"
              v-model="categoriaActividadOtro"
              :disabled="!entradaMarcada || salidaMarcada"
              class="apple-input w-full text-sm"
              :class="{ 
                'opacity-50 cursor-not-allowed': !entradaMarcada || salidaMarcada,
                'border-red-400': categoriaActividad === 'Otro' && !categoriaActividadOtro.trim() && entradaMarcada && !salidaMarcada
              }"
              placeholder="Escribe el tipo de actividad..."
              maxlength="200"
            />
            
            <!-- Mensaje de error si no se ha especificado el otro tipo -->
            <div v-if="categoriaActividad === 'Otro' && !categoriaActividadOtro.trim() && entradaMarcada && !salidaMarcada" class="mt-1.5">
              <p class="text-xs text-red-500 font-medium animate-pulse">Por favor especifica el tipo de actividad</p>
            </div>
          </div>
        </div>

        <!-- Paso 4: Imagen -->
        <div class="apple-step-card-purple mb-2">
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center">
              <div class="apple-step-number-purple">4</div>
              <h3 class="apple-step-title">Evidencia Fotográfica</h3>
            </div>
            <div v-if="fotoRegistro" class="apple-completed-badge">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              Listo
            </div>
          </div>
          
          <!-- Vista previa de la foto -->
          <div v-if="fotoRegistro" class="apple-photo-preview mb-3">
            <div class="apple-photo-container">
              <img :src="fotoRegistro" class="w-full h-full object-cover" />
              <div class="apple-photo-overlay">
                <button
                  @click="eliminarFotoRegistro"
                  :disabled="!entradaMarcada || salidaMarcada"
                  class="apple-photo-delete-btn"
                  :class="{ 'opacity-50 cursor-not-allowed': !entradaMarcada || salidaMarcada }"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  <span>Eliminar</span>
                </button>
              </div>
            </div>
          </div>
          
          <!-- Botones para capturar foto estilo Apple -->
          <div v-if="!fotoRegistro" class="apple-photo-buttons">
            <!-- Botón para tomar foto con cámara -->
            <button
              @click="tomarFotoConCamaraRegistro"
              :disabled="!entradaMarcada || salidaMarcada"
              class="apple-photo-btn apple-photo-btn-camera-dark"
              :class="{ 'opacity-50 cursor-not-allowed': !entradaMarcada || salidaMarcada }"
            >
              <div class="apple-photo-btn-icon">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <span class="apple-photo-btn-text">
                <span v-if="entradaMarcada && !salidaMarcada">Cámara</span>
                <span v-else-if="!entradaMarcada">Bloqueado</span>
                <span v-else>Bloqueado</span>
              </span>
            </button>
            
            <!-- Botón para seleccionar de galería -->
            <button
              @click="seleccionarDeGaleriaRegistro"
              :disabled="!entradaMarcada || salidaMarcada"
              class="apple-photo-btn apple-photo-btn-gallery-dark"
              :class="{ 'opacity-50 cursor-not-allowed': !entradaMarcada || salidaMarcada }"
            >
              <div class="apple-photo-btn-icon">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <span class="apple-photo-btn-text">
                <span v-if="entradaMarcada && !salidaMarcada">Galería</span>
                <span v-else-if="!entradaMarcada">Bloqueado</span>
                <span v-else>Bloqueado</span>
              </span>
            </button>
          </div>
          
          <!-- Inputs ocultos para los diferentes tipos de captura -->
          <input
            type="file"
            accept="image/*"
            capture="environment"
            @change="onFileChangeRegistro"
            :disabled="!entradaMarcada || salidaMarcada"
            class="hidden"
            ref="fileInputCameraRegistro"
          />
          <input
            type="file"
            accept="image/*"
            @change="onFileChangeRegistro"
            :disabled="!entradaMarcada || salidaMarcada"
            class="hidden"
            ref="fileInputGalleryRegistro"
          />
        </div>

        <!-- Paso 5: Descripción (Obligatorio) -->
        <div class="apple-step-card-purple mb-2">
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center">
              <div class="apple-step-number-purple">5</div>
              <h3 class="apple-step-title">Descripción</h3>
            </div>
            <div v-if="descripcionRegistro.trim()" class="apple-completed-badge">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              <span>Completado</span>
            </div>
            <span v-else class="text-xs text-red-400 font-medium">* Requerido</span>
          </div>
          
          <textarea
            v-model="descripcionRegistro"
            id="descripcionRegistro"
            rows="3"
            :disabled="!entradaMarcada || salidaMarcada"
            class="apple-textarea w-full"
            :class="{ 'opacity-50': !entradaMarcada || salidaMarcada }"
            :placeholder="entradaMarcada && !salidaMarcada ? 'Describe la actividad o añade notas...' : !entradaMarcada ? 'Marca entrada primero...' : 'Función bloqueada...'"
          ></textarea>
        </div>

        <!-- Checklist de progreso estilo Apple amarillo oscuro -->
        <div v-if="entradaMarcada && !salidaMarcada && (!latitudRegistro || !longitudRegistro || !fotoRegistro || !tipoActividad || !categoriaActividad || (categoriaActividad === 'Otro' && !categoriaActividadOtro.trim()) || !descripcionRegistro.trim())" 
             class="apple-checklist-card mb-2">
          <div class="flex items-center mb-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-yellow-700" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
            <span class="apple-checklist-title">Completa estos pasos</span>
          </div>
          <div class="grid grid-cols-2 gap-2">
            <!-- Ubicación -->
            <div :class="['apple-checklist-item', latitudRegistro && longitudRegistro ? 'apple-checklist-item-done' : 'apple-checklist-item-pending']">
              <div :class="['apple-checklist-circle', latitudRegistro && longitudRegistro ? 'apple-checklist-circle-done' : 'apple-checklist-circle-pending']">
                <svg v-if="latitudRegistro && longitudRegistro" xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span>Ubicación</span>
            </div>
            <!-- Imagen -->
            <div :class="['apple-checklist-item', fotoRegistro ? 'apple-checklist-item-done' : 'apple-checklist-item-pending']">
              <div :class="['apple-checklist-circle', fotoRegistro ? 'apple-checklist-circle-done' : 'apple-checklist-circle-pending']">
                <svg v-if="fotoRegistro" xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span>Imagen</span>
            </div>
            <!-- Modalidad -->
            <div :class="['apple-checklist-item', tipoActividad ? 'apple-checklist-item-done' : 'apple-checklist-item-pending']">
              <div :class="['apple-checklist-circle', tipoActividad ? 'apple-checklist-circle-done' : 'apple-checklist-circle-pending']">
                <svg v-if="tipoActividad" xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span>Modalidad</span>
            </div>
            <!-- Categoría -->
            <div :class="['apple-checklist-item', categoriaActividad && (categoriaActividad !== 'Otro' || categoriaActividadOtro.trim()) ? 'apple-checklist-item-done' : 'apple-checklist-item-pending']">
              <div :class="['apple-checklist-circle', categoriaActividad && (categoriaActividad !== 'Otro' || categoriaActividadOtro.trim()) ? 'apple-checklist-circle-done' : 'apple-checklist-circle-pending']">
                <svg v-if="categoriaActividad && (categoriaActividad !== 'Otro' || categoriaActividadOtro.trim())" xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span>Categoría</span>
            </div>
            <!-- Descripción -->
            <div :class="['apple-checklist-item', descripcionRegistro.trim() ? 'apple-checklist-item-done' : 'apple-checklist-item-pending']">
              <div :class="['apple-checklist-circle', descripcionRegistro.trim() ? 'apple-checklist-circle-done' : 'apple-checklist-circle-pending']">
                <svg v-if="descripcionRegistro.trim()" xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span>Descripción</span>
            </div>
          </div>
        </div>

        <!-- Indicador de listo para enviar estilo Apple -->
        <div v-if="entradaMarcada && !salidaMarcada && latitudRegistro && longitudRegistro && fotoRegistro && tipoActividad && categoriaActividad && (categoriaActividad !== 'Otro' || categoriaActividadOtro.trim()) && descripcionRegistro.trim()" 
             class="apple-ready-card mb-2">
          <div class="flex items-center justify-center">
            <div class="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center mr-2 animate-bounce">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <span class="text-sm font-semibold text-green-700">Todo listo para enviar</span>
          </div>
        </div>

        <!-- Botón enviar -->
        <button
          type="submit"
          :disabled="!latitudRegistro || !longitudRegistro || !fotoRegistro || !tipoActividad || !categoriaActividad || (categoriaActividad === 'Otro' && !categoriaActividadOtro.trim()) || !descripcionRegistro.trim() || enviando || !entradaMarcada || salidaMarcada"
          :class="['glass-button-registro w-full', (!latitudRegistro || !longitudRegistro || !fotoRegistro || !tipoActividad || !categoriaActividad || (categoriaActividad === 'Otro' && !categoriaActividadOtro.trim()) || !descripcionRegistro.trim() || enviando || !entradaMarcada || salidaMarcada) ? 'opacity-50 cursor-not-allowed' : '']"
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

// Nuevos campos para categoría de actividad
const categoriaActividad = ref(""); // Selector de categoría obligatorio
const categoriaActividadOtro = ref(""); // Campo de texto si se selecciona "Otro"

// Lista de opciones de categoría de actividad
const categoriasActividad = [
  "Acompañamiento técnico",
  "Productivas directas",
  "Ahorro y trámites financieros",
  "Capacitación / talleres / cursos",
  "Difusión y comunicación",
  "Eventos comunitarios / ferias / tianguis",
  "Reuniones y asambleas",
  "Trabajo administrativo y captura",
  "Viveros y biofábricas",
  "Otro"
];

// Referencias generales
const fileInput = ref(null);
const fileInputRegistro = ref(null);
// Nuevas referencias para los diferentes tipos de captura
const fileInputCamera = ref(null);
const fileInputGallery = ref(null);
const fileInputCameraRegistro = ref(null);
const fileInputGalleryRegistro = ref(null);
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
  
  // Limpiar todos los inputs de archivo
  if (fileInput.value) {
    fileInput.value.value = "";
  }
  if (fileInputCamera.value) {
    fileInputCamera.value.value = "";
  }
  if (fileInputGallery.value) {
    fileInputGallery.value.value = "";
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
      mensajeAsistencia.value = `${tipoAsistencia.value === 'entrada' ? 'Registro de inicio' : 'Registro de término'} guardado offline. Se enviará automáticamente cuando tengas conexión.`;
      modalMessage.value = `¡${tipoAsistencia.value === 'entrada' ? 'Inicio' : 'Término'} registrado! Se sincronizará cuando recuperes la conexión.`;
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
    
    // ✅ SOLUCIÓN: Agregar SIEMPRE timestamp CDMX exacto (igual que el reloj de la barra verde)
    // El servidor SIEMPRE lo debe recibir y usarlo para garantizar fecha/hora correcta
    formData.append("timestamp_offline", obtenerTimestampCDMX());

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
    modalMessage.value = `¡${tipoAsistencia.value === 'entrada' ? 'Inicio' : 'Término'} registrado exitosamente!`;
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
    console.log('🔍 Iniciando obtención de ubicación con MÁXIMA precisión (funciona offline)...');
    
    // Estrategia optimizada para móviles - usar watchPosition es más preciso
    const configuraciones = [
      {
        timeout: 30000, // 30 segundos - máxima precisión GPS
        enableHighAccuracy: true,
        maximumAge: 0, // CRÍTICO: NO usar caché del navegador
        minAccuracy: 20, // Buscar precisión de 20m o mejor
        maxWaitTime: 10000, // Esperar 10s por mejor precisión
        useCache: false
      },
      {
        timeout: 25000, // 25 segundos - alta precisión
        enableHighAccuracy: true,
        maximumAge: 0,
        minAccuracy: 50, // Precisión de 50m o mejor
        maxWaitTime: 8000,
        useCache: false
      },
      {
        timeout: 20000, // 20 segundos - buena precisión
        enableHighAccuracy: true,
        maximumAge: 0,
        minAccuracy: 100, // Precisión de 100m o mejor
        maxWaitTime: 6000,
        useCache: true // Último intento puede usar caché
      }
    ];
    
    // Intentar con cada configuración
    for (let i = 0; i < configuraciones.length; i++) {
      try {
        console.log(`🎯 Intento ${i + 1}/${configuraciones.length} - Buscando GPS de alta precisión...`);
        
        const location = await geoLocationService.getCurrentLocation(configuraciones[i]);

        console.log(`✅ Ubicación GPS obtenida en intento ${i + 1}:`, location);

        latitud.value = location.latitude;
        longitud.value = location.longitude;
        
        // Verificar que tenemos coordenadas válidas
        if (!latitud.value || !longitud.value) {
          throw new Error('Coordenadas inválidas recibidas');
        }
        
        // Log de precisión solo en consola (sin mostrar al usuario)
        if (location.accuracy) {
          const precision = Math.round(location.accuracy);
          if (location.accuracy <= 10) {
            console.log('🎯 EXCELENTE precisión GPS:', precision + 'm');
          } else if (location.accuracy <= 30) {
            console.log('✅ MUY BUENA precisión GPS:', precision + 'm');
          } else if (location.accuracy <= 50) {
            console.log('✅ BUENA precisión GPS:', precision + 'm');
          } else if (location.accuracy <= 100) {
            console.log('📍 Precisión GPS aceptable:', precision + 'm');
          } else {
            console.log('⚠️ Precisión GPS baja:', precision + 'm');
          }
          
          if (location.fromCache) {
            console.log('📦 Ubicación desde caché');
          }
        } else {
          console.log('✅ Ubicación GPS obtenida (precisión no disponible)');
        }
        
        return; // Salir exitosamente
        
      } catch (intentoError) {
        console.warn(`⚠️ Intento ${i + 1} falló:`, intentoError.message);
        if (i === configuraciones.length - 1) {
          // Si todos los intentos fallaron, usar fallback
          throw intentoError;
        }
        // Esperar un poco antes del siguiente intento
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
    
  } catch (err) {
    console.warn('⚠️ Todos los intentos de GPS fallaron, usando fallback offline:', err);
    
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
    console.log('🔍 Iniciando obtención de ubicación GPS para registro (funciona offline)...');
    
    // Usar la misma estrategia optimizada para registros
    const configuraciones = [
      {
        timeout: 30000, // 30 segundos - máxima precisión para registros
        enableHighAccuracy: true,
        maximumAge: 0, // CRÍTICO: ubicación fresca para registros
        minAccuracy: 20, // Buscar 20m o mejor
        maxWaitTime: 10000,
        useCache: false
      },
      {
        timeout: 25000, // 25 segundos - alta precisión
        enableHighAccuracy: true,
        maximumAge: 0,
        minAccuracy: 50,
        maxWaitTime: 8000,
        useCache: false
      },
      {
        timeout: 20000, // 20 segundos fallback
        enableHighAccuracy: true,
        maximumAge: 0,
        minAccuracy: 100,
        maxWaitTime: 6000,
        useCache: true
      }
    ];
    
    // Intentar con cada configuración
    for (let i = 0; i < configuraciones.length; i++) {
      try {
        console.log(`🎯 Intento ${i + 1}/${configuraciones.length} para registro - Buscando GPS de alta precisión...`);
        
        const location = await geoLocationService.getCurrentLocation(configuraciones[i]);

        console.log(`✅ Ubicación GPS para registro obtenida en intento ${i + 1}:`, location);

        latitudRegistro.value = location.latitude;
        longitudRegistro.value = location.longitude;
        
        // Verificar que tenemos coordenadas válidas
        if (!latitudRegistro.value || !longitudRegistro.value) {
          throw new Error('Coordenadas inválidas para registro');
        }
        
        // Log de precisión solo en consola para registros
        if (location.accuracy) {
          const precision = Math.round(location.accuracy);
          if (location.accuracy <= 30) {
            console.log('✅ EXCELENTE precisión GPS para registro:', precision + 'm');
          } else if (location.accuracy <= 50) {
            console.log('✅ BUENA precisión GPS para registro:', precision + 'm');
          } else if (location.accuracy <= 100) {
            console.log('📍 Precisión GPS aceptable para registro:', precision + 'm');
          } else {
            console.log('⚠️ Precisión GPS baja para registro:', precision + 'm');
          }
          
          if (location.fromCache) {
            console.log('📦 Registro desde caché');
          }
        }
        
        return; // Salir exitosamente
        
      } catch (intentoError) {
        console.warn(`⚠️ Intento ${i + 1} falló para registro:`, intentoError.message);
        if (i === configuraciones.length - 1) {
          throw intentoError;
        }
        // Esperar antes del siguiente intento
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
    
  } catch (err) {
    console.warn('⚠️ GPS falló para registro, usando fallback offline:', err);
    
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

  // IMPORTANTE: Limpiar imagen anterior antes de procesar la nueva
  // Esto evita que queden referencias a la imagen anterior en memoria
  foto.value = null;
  archivoFoto.value = null;

  try {
    // Compresión de imagen con calidad media y formato JPG
    console.log('🖼️ Comprimiendo imagen de asistencia...');
    console.log(`📷 Archivo original: ${file.name}, tamaño: ${(file.size/1024).toFixed(2)}KB`);
    
    const compressedBlob = await compressImage(file, 1280, 0.6);
    
    // Generar nombre único con timestamp + random para evitar colisiones
    const uniqueId = `${Date.now()}_${Math.random().toString(36).substring(2, 8)}`;
    const compressedFile = blobToFile(compressedBlob, `${tipoAsistencia.value || 'asistencia'}_${uniqueId}.jpg`);
    
    console.log(`✅ Imagen comprimida: ${compressedFile.name}, tamaño: ${(compressedFile.size/1024).toFixed(2)}KB`);
    
    // Usar el archivo comprimido
    archivoFoto.value = compressedFile;
    
    // Mostrar la imagen comprimida en la interfaz
    const reader = new FileReader();
    reader.onload = (e2) => {
      foto.value = e2.target.result;
      console.log(`✅ Vista previa de imagen actualizada`);
    };
    reader.readAsDataURL(compressedBlob);
  } catch (err) {
    console.error('Error al comprimir imagen:', err);
    // Fallback: usar la imagen original sin comprimir
    const uniqueId = `${Date.now()}_${Math.random().toString(36).substring(2, 8)}`;
    // Crear un nuevo File con nombre único para evitar caché
    const newFile = new File([file], `${tipoAsistencia.value || 'asistencia'}_${uniqueId}.jpg`, { type: file.type });
    archivoFoto.value = newFile;
    
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

  // IMPORTANTE: Limpiar imagen anterior antes de procesar la nueva
  // Esto evita que queden referencias a la imagen anterior en memoria
  fotoRegistro.value = null;
  archivoFotoRegistro.value = null;

  try {
    // Compresión de imagen con calidad media y formato JPG
    console.log('🖼️ Comprimiendo imagen de registro...');
    console.log(`📷 Archivo original: ${file.name}, tamaño: ${(file.size/1024).toFixed(2)}KB`);
    
    const compressedBlob = await compressImage(file, 1280, 0.6);
    
    // Generar nombre único con timestamp + random para evitar colisiones
    const uniqueId = `${Date.now()}_${Math.random().toString(36).substring(2, 8)}`;
    const compressedFile = blobToFile(compressedBlob, `actividad_${uniqueId}.jpg`);
    
    console.log(`✅ Imagen comprimida: ${compressedFile.name}, tamaño: ${(compressedFile.size/1024).toFixed(2)}KB`);
    
    // Usar el archivo comprimido
    archivoFotoRegistro.value = compressedFile;
    
    // Mostrar la imagen comprimida en la interfaz
    const reader = new FileReader();
    reader.onload = (e2) => {
      fotoRegistro.value = e2.target.result;
      console.log(`✅ Vista previa de imagen actualizada (${fotoRegistro.value.substring(0, 50)}...)`);
    };
    reader.readAsDataURL(compressedBlob);
  } catch (err) {
    console.error('Error al comprimir imagen:', err);
    // Fallback: usar la imagen original sin comprimir
    const uniqueId = `${Date.now()}_${Math.random().toString(36).substring(2, 8)}`;
    // Crear un nuevo File con nombre único para evitar caché
    const newFile = new File([file], `actividad_${uniqueId}.jpg`, { type: file.type });
    archivoFotoRegistro.value = newFile;
    
    const reader = new FileReader();
    reader.onload = (e2) => {
      fotoRegistro.value = e2.target.result;
    };
    reader.readAsDataURL(file);
  }
}

// Nuevas funciones para manejo de fotos con opciones separadas

// Funciones para asistencia (entrada/salida)
function tomarFotoConCamara() {
  // IMPORTANTE: Limpiar el valor del input ANTES de abrir la cámara
  // Esto fuerza al navegador a disparar el evento @change incluso si selecciona la misma imagen
  if (fileInputCamera.value) {
    fileInputCamera.value.value = '';
    fileInputCamera.value.click();
  }
}

function seleccionarDeGaleria() {
  // IMPORTANTE: Limpiar el valor del input ANTES de abrir la galería
  // Esto fuerza al navegador a disparar el evento @change incluso si selecciona la misma imagen
  if (fileInputGallery.value) {
    fileInputGallery.value.value = '';
    fileInputGallery.value.click();
  }
}

function eliminarFoto() {
  foto.value = null;
  archivoFoto.value = null;
  
  // Limpiar ambos inputs
  if (fileInputCamera.value) {
    fileInputCamera.value.value = "";
  }
  if (fileInputGallery.value) {
    fileInputGallery.value.value = "";
  }
}

// Funciones para registro de actividades
function tomarFotoConCamaraRegistro() {
  if (!entradaMarcada.value || salidaMarcada.value) return;
  
  // IMPORTANTE: Limpiar el valor del input ANTES de abrir la cámara
  // Esto fuerza al navegador a disparar el evento @change incluso si selecciona la misma imagen
  if (fileInputCameraRegistro.value) {
    fileInputCameraRegistro.value.value = '';
    fileInputCameraRegistro.value.click();
  }
}

function seleccionarDeGaleriaRegistro() {
  if (!entradaMarcada.value || salidaMarcada.value) return;
  
  // IMPORTANTE: Limpiar el valor del input ANTES de abrir la galería
  // Esto fuerza al navegador a disparar el evento @change incluso si selecciona la misma imagen
  if (fileInputGalleryRegistro.value) {
    fileInputGalleryRegistro.value.value = '';
    fileInputGalleryRegistro.value.click();
  }
}

function eliminarFotoRegistro() {
  if (!entradaMarcada.value || salidaMarcada.value) return;
  
  fotoRegistro.value = null;
  archivoFotoRegistro.value = null;
  
  // Limpiar ambos inputs de registro
  if (fileInputCameraRegistro.value) {
    fileInputCameraRegistro.value.value = "";
  }
  if (fileInputGalleryRegistro.value) {
    fileInputGalleryRegistro.value.value = "";
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

  // Validación silenciosa - el indicador visual ya muestra qué falta
  // El botón está deshabilitado así que esto es solo una protección adicional
  if (!latitudRegistro.value || !longitudRegistro.value || !archivoFotoRegistro.value || !tipoActividad.value) {
    return;
  }

  // Validar categoría de actividad - protección silenciosa
  if (!categoriaActividad.value) {
    return;
  }

  // Validar campo "Otro" si está seleccionado - protección silenciosa
  if (categoriaActividad.value === 'Otro' && !categoriaActividadOtro.value.trim()) {
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
        tipoActividad.value, // tipo de actividad (campo/gabinete)
        timestampCDMX, // timestamp CDMX exacto
        categoriaActividad.value, // NUEVO: categoría de actividad
        categoriaActividad.value === 'Otro' ? categoriaActividadOtro.value.trim() : null // NUEVO: especificación si es "Otro"
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
        tipo_actividad: tipoActividad.value,
        categoria_actividad: categoriaActividad.value, // NUEVO
        categoria_actividad_otro: categoriaActividad.value === 'Otro' ? categoriaActividadOtro.value.trim() : null, // NUEVO
        foto: fotoRegistro.value,
        offline: true, // Marcador para indicar que está pendiente
        backend: null,
        tipo: 'actividad', // Especificar explícitamente el tipo de registro
        id_offline: registroID // Guardar el ID generado para referencia
      });

      // Limpiar campos
      descripcionRegistro.value = "";
      tipoActividad.value = "";
      categoriaActividad.value = ""; // NUEVO: limpiar categoría
      categoriaActividadOtro.value = ""; // NUEVO: limpiar especificación
      fotoRegistro.value = null;
      archivoFotoRegistro.value = null;
      latitudRegistro.value = null;
      longitudRegistro.value = null;

      // Limpiar todos los inputs de archivo de registro
      if (fileInputRegistro.value) {
        fileInputRegistro.value.value = "";
      }
      if (fileInputCameraRegistro.value) {
        fileInputCameraRegistro.value.value = "";
      }
      if (fileInputGalleryRegistro.value) {
        fileInputGalleryRegistro.value.value = "";
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
    formData.append("tipo_actividad", tipoActividad.value);
    formData.append("categoria_actividad", categoriaActividad.value); // NUEVO: categoría de actividad
    // NUEVO: solo enviar categoria_actividad_otro si la categoría es "Otro"
    if (categoriaActividad.value === 'Otro') {
      formData.append("categoria_actividad_otro", categoriaActividadOtro.value.trim());
    }
    formData.append("foto", archivoFotoRegistro.value);
    formData.append("tipo", "actividad"); // Especificar explícitamente que es un registro de actividad
    // ✅ SOLUCIÓN: Agregar SIEMPRE timestamp CDMX exacto (igual que el reloj de la barra verde)
    // El servidor SIEMPRE lo debe recibir y usarlo para garantizar fecha/hora correcta
    formData.append("timestamp_offline", obtenerTimestampCDMX());
    
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
      tipo_actividad: tipoActividad.value,
      categoria_actividad: categoriaActividad.value, // NUEVO
      categoria_actividad_otro: categoriaActividad.value === 'Otro' ? categoriaActividadOtro.value.trim() : null, // NUEVO
      foto: fotoRegistro.value,
      offline: false, // Enviado exitosamente
      backend: response.data,
      tipo: 'actividad' // Especificar explícitamente el tipo de registro
    });

    // Limpiar campos
    descripcionRegistro.value = "";
    tipoActividad.value = "";
    categoriaActividad.value = ""; // NUEVO: limpiar categoría
    categoriaActividadOtro.value = ""; // NUEVO: limpiar especificación
    fotoRegistro.value = null;
    archivoFotoRegistro.value = null;
    latitudRegistro.value = null;
    longitudRegistro.value = null;

    // Limpiar todos los inputs de archivo de registro
    if (fileInputRegistro.value) {
      fileInputRegistro.value.value = "";
    }
    if (fileInputCameraRegistro.value) {
      fileInputCameraRegistro.value.value = "";
    }
    if (fileInputGalleryRegistro.value) {
      fileInputGalleryRegistro.value.value = "";
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
          <h3 class="text-base font-semibold text-gray-900">Registro de Inicio</h3>
          <p class="text-xs text-gray-600">Inicia tu jornada laboral</p>
        </div>
      </div>
      
      <div class="p-3 mb-3 rounded" style="background-color: rgba(30, 144, 255, 0.1); border-left: 4px solid rgba(30, 144, 255, 0.6);">
        <div class="flex items-center">
          <svg class="w-4 h-4 mr-2" style="color: rgb(30, 144, 255);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <p class="font-medium text-sm" style="color: rgb(25, 118, 210);">Al registrar inicio podrás capturar actividades</p>
        </div>
        <p class="text-xs mt-1 ml-6" style="color: rgb(30, 144, 255);">Durante tu jornada podrás documentar todas tus tareas</p>
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
          <span>No se puede cancelar una vez registrado</span>
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
          <h3 class="text-base font-semibold text-gray-900">Registro de Término</h3>
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
      <div class="text-center px-2">
        <!-- Icono principal con animación -->
        <div class="flex justify-center mb-4">
          <div class="w-16 h-16 bg-gradient-to-br from-slate-700 to-slate-900 rounded-2xl flex items-center justify-center shadow-xl transform rotate-3">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
            </svg>
          </div>
        </div>
        
        <!-- Título -->
        <h3 class="text-lg font-bold text-slate-800 mb-2">Acceso Restringido</h3>
        
        <!-- Mensaje principal -->
        <div class="bg-gradient-to-r from-slate-100 to-gray-100 border-l-4 border-slate-600 rounded-r-xl p-4 mb-4 shadow-sm">
          <p class="text-slate-700 text-sm font-semibold mb-1">Registra tu inicio de jornada</p>
          <p class="text-slate-500 text-xs">Presiona "Registro de Inicio" en la sección de Registro para habilitar el registro de actividades</p>
        </div>
        
        <!-- Pasos -->
        <div class="flex items-center justify-center space-x-2 text-xs text-slate-500">
          <span class="flex items-center bg-slate-200 px-3 py-1.5 rounded-full">
            <span class="w-5 h-5 bg-slate-600 text-white rounded-full flex items-center justify-center text-xs font-bold mr-2">1</span>
            Inicio
          </span>
          <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
          <span class="flex items-center bg-slate-100 px-3 py-1.5 rounded-full text-slate-400">
            <span class="w-5 h-5 bg-slate-300 text-slate-500 rounded-full flex items-center justify-center text-xs font-bold mr-2">2</span>
            Actividades
          </span>
        </div>
      </div>
    `;
  } else if (salidaMarcada.value) {
    actividadesBloqueadasModalMessage.value = `
      <div class="text-center px-2">
        <!-- Icono principal -->
        <div class="flex justify-center mb-4">
          <div class="w-16 h-16 bg-gradient-to-br from-gray-600 to-gray-800 rounded-2xl flex items-center justify-center shadow-xl transform -rotate-3">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
          </div>
        </div>
        
        <!-- Título -->
        <h3 class="text-lg font-bold text-gray-800 mb-2">Jornada Finalizada</h3>
        
        <!-- Mensaje principal -->
        <div class="bg-gradient-to-r from-gray-100 to-slate-100 border-l-4 border-gray-500 rounded-r-xl p-4 mb-4 shadow-sm">
          <p class="text-gray-700 text-sm font-semibold mb-1">Término de jornada registrado</p>
          <p class="text-gray-500 text-xs">El acceso a actividades se restablecerá automáticamente mañana con un nuevo registro de inicio</p>
        </div>
        
        <!-- Estado -->
        <div class="inline-flex items-center bg-gray-200 px-4 py-2 rounded-full">
          <div class="w-2 h-2 bg-gray-500 rounded-full mr-2 animate-pulse"></div>
          <span class="text-xs font-medium text-gray-600">Esperando próximo día</span>
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
    tipoActividad.value = "";
    categoriaActividad.value = ""; // NUEVO: limpiar categoría
    categoriaActividadOtro.value = ""; // NUEVO: limpiar especificación
    fotoRegistro.value = null;
    archivoFotoRegistro.value = null;
    latitudRegistro.value = null;
    longitudRegistro.value = null;
    
    // Limpiar todos los inputs de archivo de registro
    if (fileInputRegistro.value) {
      fileInputRegistro.value.value = "";
    }
    if (fileInputCameraRegistro.value) {
      fileInputCameraRegistro.value.value = "";
    }
    if (fileInputGalleryRegistro.value) {
      fileInputGalleryRegistro.value.value = "";
    }
  }
});
</script>

<style scoped>
/* Animaciones de burbujas de vidrio flotantes */
@keyframes bubble-float-1 {
  0% {
    transform: translateY(0) scale(1);
    opacity: 0;
  }
  10% {
    opacity: 0.6;
  }
  90% {
    opacity: 0.6;
  }
  100% {
    transform: translateY(-250px) scale(1.1);
    opacity: 0;
  }
}

@keyframes bubble-float-2 {
  0% {
    transform: translateY(0) scale(1);
    opacity: 0;
  }
  15% {
    opacity: 0.5;
  }
  85% {
    opacity: 0.5;
  }
  100% {
    transform: translateY(-280px) scale(0.9);
    opacity: 0;
  }
}

@keyframes bubble-float-3 {
  0% {
    transform: translateY(0) scale(1);
    opacity: 0;
  }
  20% {
    opacity: 0.4;
  }
  80% {
    opacity: 0.4;
  }
  100% {
    transform: translateY(-220px) scale(1.2);
    opacity: 0;
  }
}

@keyframes bubble-float-4 {
  0% {
    transform: translateY(0) scale(1);
    opacity: 0;
  }
  12% {
    opacity: 0.55;
  }
  88% {
    opacity: 0.55;
  }
  100% {
    transform: translateY(-260px) scale(0.95);
    opacity: 0;
  }
}

.animate-bubble-1 {
  animation: bubble-float-1 8s ease-in-out infinite;
}

.animate-bubble-2 {
  animation: bubble-float-2 10s ease-in-out infinite;
  animation-delay: 2s;
}

.animate-bubble-3 {
  animation: bubble-float-3 7s ease-in-out infinite;
  animation-delay: 4s;
}

.animate-bubble-4 {
  animation: bubble-float-4 9s ease-in-out infinite;
  animation-delay: 1s;
}

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
  background: linear-gradient(135deg, rgba(254, 252, 232, 0.35), rgba(255, 251, 235, 0.3), rgba(254, 249, 195, 0.25));
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(180, 83, 9, 0.15);
  box-shadow: 
    0 8px 32px 0 rgba(22, 163, 74, 0.3),
    0 0 0 1px rgba(180, 83, 9, 0.1);
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
    rgba(254, 240, 138, 0.2),
    transparent
  );
  transform: skewX(-25deg);
  transition: all 0.6s;
}

.glass-card:hover::before {
  left: 150%;
}

/* Efecto de vidrio azul suave para entrada - Liquid Glass */
.glass-card-blue {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.95) 0%, 
    rgba(248, 250, 255, 0.9) 25%,
    rgba(240, 245, 255, 0.85) 50%,
    rgba(248, 250, 255, 0.9) 75%,
    rgba(255, 255, 255, 0.95) 100%) !important;
  backdrop-filter: blur(20px) saturate(180%) !important;
  -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
  border-radius: 24px !important;
  border: 1px solid rgba(59, 130, 246, 0.15) !important;
  box-shadow: 
    0 8px 32px rgba(59, 130, 246, 0.12),
    0 2px 8px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.8),
    inset 0 -1px 0 rgba(59, 130, 246, 0.05) !important;
  padding: 1rem 0.5rem !important;
  position: relative !important;
  overflow: hidden !important;
}

.glass-card-blue::before {
  content: '' !important;
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  height: 50% !important;
  background: linear-gradient(180deg, 
    rgba(255, 255, 255, 0.4) 0%, 
    rgba(255, 255, 255, 0) 100%) !important;
  pointer-events: none !important;
  border-radius: 24px 24px 0 0 !important;
}

/* Efecto de vidrio rojo suave para término - Liquid Glass */
.glass-card-red {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.95) 0%, 
    rgba(255, 250, 250, 0.9) 25%,
    rgba(255, 245, 245, 0.85) 50%,
    rgba(255, 250, 250, 0.9) 75%,
    rgba(255, 255, 255, 0.95) 100%) !important;
  backdrop-filter: blur(20px) saturate(180%) !important;
  -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
  border-radius: 24px !important;
  border: 1px solid rgba(239, 68, 68, 0.15) !important;
  box-shadow: 
    0 8px 32px rgba(239, 68, 68, 0.12),
    0 2px 8px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.8),
    inset 0 -1px 0 rgba(239, 68, 68, 0.05) !important;
  padding: 1rem 0.5rem !important;
  position: relative !important;
  overflow: hidden !important;
}

.glass-card-red::before {
  content: '' !important;
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  height: 50% !important;
  background: linear-gradient(180deg, 
    rgba(255, 255, 255, 0.4) 0%, 
    rgba(255, 255, 255, 0) 100%) !important;
  pointer-events: none !important;
  border-radius: 24px 24px 0 0 !important;
}

/* Efecto de vidrio morado para actividades */
.glass-card-purple {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.95) 0%, 
    rgba(252, 250, 255, 0.9) 25%,
    rgba(248, 245, 255, 0.85) 50%,
    rgba(252, 250, 255, 0.9) 75%,
    rgba(255, 255, 255, 0.95) 100%) !important;
  backdrop-filter: blur(20px) saturate(180%) !important;
  -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
  border-radius: 24px !important;
  border: 1px solid rgba(168, 85, 247, 0.15) !important;
  box-shadow: 
    0 8px 32px rgba(168, 85, 247, 0.12),
    0 2px 8px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.8),
    inset 0 -1px 0 rgba(168, 85, 247, 0.05) !important;
  padding: 1rem 0.5rem !important;
  position: relative !important;
  overflow: hidden !important;
}

.glass-card-purple::before {
  content: '' !important;
  position: absolute !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  height: 50% !important;
  background: linear-gradient(180deg, 
    rgba(255, 255, 255, 0.4) 0%, 
    rgba(255, 255, 255, 0) 100%) !important;
  pointer-events: none !important;
  border-radius: 24px 24px 0 0 !important;
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

/* ===== BOTONES ESTILO APPLE ===== */

/* Botón secundario (Cancelar) - Estilo Apple */
.glass-button-secondary {
  padding: 0.875rem 1.5rem;
  border-radius: 14px;
  border: none;
  background: linear-gradient(180deg, 
    #f5f5f7 0%, 
    #e8e8ed 100%);
  color: #1d1d1f;
  font-weight: 600;
  font-size: 1rem;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
  letter-spacing: -0.01em;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 1px 3px rgba(0, 0, 0, 0.12),
    0 1px 2px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
}

.glass-button-secondary:hover:not(:disabled) {
  transform: scale(1.02);
  background: linear-gradient(180deg, 
    #ffffff 0%, 
    #f0f0f5 100%);
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.15),
    0 2px 4px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 1);
}

.glass-button-secondary:active:not(:disabled) {
  transform: scale(0.98);
  background: linear-gradient(180deg, 
    #e8e8ed 0%, 
    #d4d4d9 100%);
  box-shadow: 
    0 1px 2px rgba(0, 0, 0, 0.1),
    inset 0 2px 4px rgba(0, 0, 0, 0.05);
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

/* Botón Entrada (Azul) - Estilo Apple */
.glass-button-entrada {
  padding: 0.875rem 1.5rem;
  border-radius: 14px;
  border: none;
  background: linear-gradient(180deg, 
    #0a84ff 0%, 
    #0071e3 100%);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
  letter-spacing: -0.01em;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 16px rgba(10, 132, 255, 0.4),
    0 2px 4px rgba(0, 112, 227, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.25);
}

.glass-button-entrada:hover:not(:disabled) {
  transform: scale(1.02) translateY(-1px);
  background: linear-gradient(180deg, 
    #3399ff 0%, 
    #0a84ff 100%);
  box-shadow: 
    0 8px 24px rgba(10, 132, 255, 0.5),
    0 4px 8px rgba(0, 112, 227, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.35);
}

.glass-button-entrada:active:not(:disabled) {
  transform: scale(0.98);
  background: linear-gradient(180deg, 
    #0071e3 0%, 
    #005bb5 100%);
  box-shadow: 
    0 2px 8px rgba(10, 132, 255, 0.3),
    inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.glass-button-entrada::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transition: left 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-button-entrada:hover::before {
  left: 100%;
}

/* Estados deshabilitados estilo Apple - todos los botones */
.glass-button-entrada:disabled,
.glass-button-salida:disabled,
.glass-button-registro:disabled,
.glass-button-secondary:disabled {
  opacity: 0.5 !important;
  cursor: not-allowed !important;
  transform: none !important;
  filter: saturate(0.8);
}

.glass-button-entrada:disabled::before,
.glass-button-salida:disabled::before,
.glass-button-registro:disabled::before {
  display: none;
}

.glass-button-entrada:disabled:hover,
.glass-button-salida:disabled:hover,
.glass-button-registro:disabled:hover,
.glass-button-secondary:disabled:hover {
  transform: none !important;
  box-shadow: inherit !important;
}

/* Botón Salida (Rojo) - Estilo Apple */
.glass-button-salida {
  padding: 0.875rem 1.5rem;
  border-radius: 14px;
  border: none;
  background: linear-gradient(180deg, 
    #ff453a 0%, 
    #d70015 100%);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
  letter-spacing: -0.01em;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 16px rgba(255, 69, 58, 0.4),
    0 2px 4px rgba(215, 0, 21, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.25);
}

.glass-button-salida:hover:not(:disabled) {
  transform: scale(1.02) translateY(-1px);
  background: linear-gradient(180deg, 
    #ff6961 0%, 
    #ff453a 100%);
  box-shadow: 
    0 8px 24px rgba(255, 69, 58, 0.5),
    0 4px 8px rgba(215, 0, 21, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.35);
}

.glass-button-salida:active:not(:disabled) {
  transform: scale(0.98);
  background: linear-gradient(180deg, 
    #d70015 0%, 
    #a50000 100%);
  box-shadow: 
    0 2px 8px rgba(255, 69, 58, 0.3),
    inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.glass-button-salida::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transition: left 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-button-salida:hover::before {
  left: 100%;
}

/* Botón Registro (Morado) - Estilo Apple */
.glass-button-registro {
  padding: 0.875rem 1.5rem;
  border-radius: 14px;
  border: none;
  background: linear-gradient(180deg, 
    #bf5af2 0%, 
    #9d4edd 100%);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
  letter-spacing: -0.01em;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 16px rgba(191, 90, 242, 0.4),
    0 2px 4px rgba(157, 78, 221, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.25);
}

.glass-button-registro:hover:not(:disabled) {
  transform: scale(1.02) translateY(-1px);
  background: linear-gradient(180deg, 
    #d17df5 0%, 
    #bf5af2 100%);
  box-shadow: 
    0 8px 24px rgba(191, 90, 242, 0.5),
    0 4px 8px rgba(157, 78, 221, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.35);
}

.glass-button-registro:active:not(:disabled) {
  transform: scale(0.98);
  background: linear-gradient(180deg, 
    #9d4edd 0%, 
    #7b2cbf 100%);
  box-shadow: 
    0 2px 8px rgba(191, 90, 242, 0.3),
    inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.glass-button-registro::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  transition: left 0.6s cubic-bezier(0.4, 0, 0.2, 1);
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
  color: white;
  font-family: 'Poppins', 'DM Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  letter-spacing: -0.01em;
  font-weight: 700;
  position: relative;
  padding: 0.5rem 1rem;
  margin: -0.5rem -1rem 0.25rem -1rem;
  background: linear-gradient(
    90deg, 
    rgba(15, 55, 140, 0.9) 0%,
    rgba(15, 55, 140, 1) 50%,
    rgba(15, 55, 140, 0.9) 100%
  );
  border-left: 3px solid rgba(10, 40, 120, 1);
  border-right: 3px solid rgba(10, 40, 120, 1);
  border-radius: 0 6px 6px 0;
  box-shadow: 0 4px 16px rgba(15, 55, 140, 0.5);
}

.salida-title {
  color: white;
  font-family: 'Poppins', 'DM Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  letter-spacing: -0.01em;
  font-weight: 700;
  position: relative;
  padding: 0.5rem 1rem;
  margin: -0.5rem -1rem 0.25rem -1rem;
  background: linear-gradient(
    90deg, 
    rgba(155, 25, 45, 0.9) 0%,
    rgba(155, 25, 45, 1) 50%,
    rgba(155, 25, 45, 0.9) 100%
  );
  border-left: 3px solid rgba(120, 15, 35, 1);
  border-right: 3px solid rgba(120, 15, 35, 1);
  border-radius: 0 6px 6px 0;
  box-shadow: 0 4px 16px rgba(155, 25, 45, 0.5);
}

.purple-title {
  background: linear-gradient(
    90deg, 
    #6b21a8 0%, 
    #7c3aed 25%, 
    #c4b5fd 50%, 
    #7c3aed 75%, 
    #6b21a8 100%
  );
  background-size: 300% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: gradient-wave 3s ease-in-out infinite;
  font-family: 'Poppins', 'DM Sans', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  letter-spacing: -0.015em;
  font-weight: 700;
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
  height: 1px;
  background: linear-gradient(90deg, #15803d, #16a34a, #15803d);
  border-radius: 0.5px;
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
    padding-left: 0.125rem;
    padding-right: 0.125rem;
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
    padding-left: 0.125rem;
    padding-right: 0.125rem;
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

/* Estilos corporativos modernos para botones de ubicación */
.location-container-corporate {
  position: relative;
  margin-bottom: 1rem;
}

/* Botón principal con gradiente corporativo - Estilo Apple */
.location-button-corporate {
  background: linear-gradient(180deg, 
    #0a84ff 0%,
    #0071e3 100%
  );
  border: none;
  position: relative;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
  letter-spacing: -0.01em;
  box-shadow: 
    0 4px 16px rgba(10, 132, 255, 0.4),
    0 2px 4px rgba(0, 112, 227, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.25);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.location-button-corporate:hover:not(:disabled) {
  transform: scale(1.02) translateY(-2px);
  background: linear-gradient(180deg, 
    #3399ff 0%,
    #0a84ff 100%
  );
  box-shadow: 
    0 10px 28px rgba(10, 132, 255, 0.5),
    0 4px 8px rgba(0, 112, 227, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.35);
}

.location-button-corporate:active:not(:disabled) {
  transform: scale(0.98);
  box-shadow: 
    0 2px 8px rgba(10, 132, 255, 0.3),
    inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Efecto de brillo superior - Apple shine effect */
.location-button-shine {
  position: absolute;
  top: 0;
  left: -150%;
  width: 150%;
  height: 100%;
  background: linear-gradient(120deg, 
    transparent 0%,
    transparent 40%, 
    rgba(255, 255, 255, 0.4) 50%,
    transparent 60%,
    transparent 100%
  );
  transition: left 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.location-button-corporate:hover .location-button-shine {
  left: 150%;
}

/* Icono wrapper con círculo de fondo */
.location-icon-wrapper {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.location-button-corporate:hover .location-icon-wrapper {
  transform: scale(1.1);
}

/* Wrapper para estado exitoso - Apple checkmark animation */
.location-icon-wrapper-success {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(48, 209, 88, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #30d158;
  animation: apple-success-bounce 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.location-icon-wrapper-success svg {
  filter: drop-shadow(0 0 8px rgba(48, 209, 88, 0.6));
}

/* Animación de aparición del icono de éxito estilo Apple */
@keyframes apple-success-bounce {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.15);
  }
  70% {
    transform: scale(0.95);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Wrapper para estado deshabilitado */
.location-icon-wrapper-disabled {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
}

/* Flecha indicadora */
.location-arrow {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.location-button-corporate:hover .location-arrow {
  background: rgba(255, 255, 255, 0.2);
  transform: translateX(4px);
}

/* Botón en estado de éxito - Estilo Apple verde */
.location-button-success-corporate {
  background: linear-gradient(180deg, 
    #30d158 0%,
    #28a745 100%
  ) !important;
  border: none !important;
  box-shadow: 
    0 4px 16px rgba(48, 209, 88, 0.4),
    0 2px 4px rgba(40, 167, 69, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.location-button-success-corporate:hover:not(:disabled) {
  transform: scale(1.02) translateY(-2px) !important;
  background: linear-gradient(180deg, 
    #4ade80 0%,
    #30d158 100%
  ) !important;
  box-shadow: 
    0 10px 28px rgba(48, 209, 88, 0.5),
    0 4px 8px rgba(40, 167, 69, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.35) !important;
}

.location-button-success-corporate:active:not(:disabled) {
  transform: scale(0.98) !important;
  box-shadow: 
    0 2px 8px rgba(48, 209, 88, 0.3),
    inset 0 2px 4px rgba(0, 0, 0, 0.1) !important;
}

/* Botón deshabilitado - Estilo Apple */
.location-button-disabled-corporate {
  background: linear-gradient(180deg, 
    #f5f5f7 0%,
    #e8e8ed 100%
  ) !important;
  border: none !important;
  cursor: not-allowed !important;
  opacity: 0.5 !important;
  filter: saturate(0.7);
  color: #86868b !important;
}

.location-button-disabled-corporate:hover {
  transform: none !important;
  box-shadow: inherit !important;
}

/* Tarjeta de coordenadas estilo Apple */
.coordinates-card-corporate {
  margin-top: 0;
  background: linear-gradient(180deg, #30d158 0%, #28a745 100%);
  border-radius: 0 0 14px 14px;
  padding: 0.75rem 1rem;
  animation: slide-in-corporate 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  box-shadow: 
    0 4px 12px rgba(48, 209, 88, 0.3),
    0 2px 4px rgba(0, 0, 0, 0.08);
}

/* Badge de coordenadas - verde con blanco */
.coordinate-badge {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background: transparent;
  padding: 0;
  min-width: 0;
  flex-shrink: 1;
}

.coordinate-label-corp {
  font-size: 0.625rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  text-transform: uppercase;
  letter-spacing: 0.03em;
  font-family: 'Inter', sans-serif;
  white-space: nowrap;
  flex-shrink: 0;
}

.coordinate-value-corp {
  font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
  font-size: 0.625rem;
  font-weight: 600;
  color: #ffffff;
  letter-spacing: -0.01em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* Animación de entrada */
@keyframes slide-in-corporate {
  0% {
    opacity: 0;
    transform: translateY(-10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 640px) {
  .location-button-corporate {
    padding: 1rem 1.25rem;
  }
  
  .location-icon-wrapper,
  .location-icon-wrapper-success,
  .location-icon-wrapper-disabled {
    width: 44px;
    height: 44px;
  }
  
  .location-icon-wrapper-success {
    width: 52px;
    height: 52px;
  }
  
  .location-icon-wrapper svg,
  .location-icon-wrapper-disabled svg {
    width: 2rem;
    height: 2rem;
  }
  
  .location-icon-wrapper-success svg {
    width: 2.5rem !important;
    height: 2.5rem !important;
  }
  
  .coordinates-card-corporate {
    padding: 0.5rem 0.75rem;
  }
  
  .coordinate-value-corp {
    font-size: 0.5625rem;
    max-width: 80px;
  }
  
  .coordinate-label-corp {
    font-size: 0.5625rem;
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

/* Animación de brillo para el título Panel de Registro */
.title-shine {
  position: relative;
}

.title-shine span {
  display: inline-block;
  animation: letter-shine 4s ease-in-out infinite;
  animation-delay: calc(var(--char-index) * 0.1s);
}

.title-shine .space-char {
  min-width: 0.5em;
  display: inline-block;
}

@keyframes letter-shine {
  0%, 70% {
    text-shadow: none;
    filter: brightness(1);
    transform: scale(1);
  }
  75% {
    text-shadow: 
      0 0 8px rgba(234, 179, 8, 0.8),
      0 0 15px rgba(234, 179, 8, 0.6),
      0 0 20px rgba(234, 179, 8, 0.4);
    filter: brightness(1.5);
    transform: scale(1.1);
  }
  80% {
    text-shadow: none;
    filter: brightness(1);
    transform: scale(1);
  }
  100% {
    text-shadow: none;
    filter: brightness(1);
    transform: scale(1);
  }
}

/* Línea amarilla para Panel de Registro */
.yellow-line {
  width: 180px;
  height: 2px;
  background: linear-gradient(90deg, #eab308, #f59e0b, #eab308);
  border-radius: 1px;
  box-shadow: 0 1px 3px rgba(234, 179, 8, 0.3);
}

/* Botones de foto con efecto liquid glass */
.photo-button-glass {
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  -webkit-tap-highlight-color: transparent;
  font-size: 0.95rem;
  letter-spacing: 0.3px;
}

.photo-button-glass::before {
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
  transition: left 0.5s ease;
}

.photo-button-glass:hover::before {
  left: 100%;
}

/* Botón de cámara - rosa fuerte liquid glass */
.photo-button-pink {
  background: linear-gradient(
    135deg,
    rgba(236, 72, 153, 0.65) 0%,
    rgba(219, 39, 119, 0.7) 50%,
    rgba(190, 24, 93, 0.75) 100%
  );
}

.photo-button-pink:hover:not(:disabled) {
  background: linear-gradient(
    135deg,
    rgba(236, 72, 153, 0.75) 0%,
    rgba(219, 39, 119, 0.8) 50%,
    rgba(190, 24, 93, 0.85) 100%
  );
  transform: translateY(-2px);
}

.photo-button-pink:active:not(:disabled) {
  transform: translateY(0);
}

/* Botón de galería - gris liquid glass */
.photo-button-gallery {
  background: linear-gradient(
    135deg,
    rgba(75, 85, 99, 0.65) 0%,
    rgba(55, 65, 81, 0.7) 50%,
    rgba(31, 41, 55, 0.75) 100%
  );
}

.photo-button-gallery:hover:not(:disabled) {
  background: linear-gradient(
    135deg,
    rgba(75, 85, 99, 0.75) 0%,
    rgba(55, 65, 81, 0.8) 50%,
    rgba(31, 41, 55, 0.85) 100%
  );
  transform: translateY(-2px);
}

.photo-button-gallery:active:not(:disabled) {
  transform: translateY(0);
}

/* Efecto disabled para botones de foto */
.photo-button-glass:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.photo-button-glass:disabled::before {
  display: none;
}

/* ===== ESTILOS APPLE PARA REGISTRO DE ASISTENCIA ===== */

/* Contenedor principal del formulario */
.apple-form-container,
.apple-attendance-container {
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  animation: apple-fade-in 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes apple-fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Header card - estilo Apple */
.apple-header-card {
  padding: 0.625rem 0.875rem !important;
  border-radius: 16px;
  position: relative;
  overflow: hidden;
}

.apple-header-entrada {
  background: linear-gradient(135deg, #0a84ff 0%, #0066cc 100%);
  box-shadow: 
    0 8px 24px rgba(10, 132, 255, 0.35),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.apple-header-salida {
  background: linear-gradient(135deg, #ff453a 0%, #cc3333 100%);
  box-shadow: 
    0 8px 24px rgba(255, 69, 58, 0.35),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.apple-header-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.apple-header-icon svg {
  width: 18px;
  height: 18px;
}

.apple-header-title {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
  font-size: 0.9375rem;
  font-weight: 600;
  color: white;
  letter-spacing: -0.02em;
  margin: 0;
  white-space: nowrap;
}

/* User card estilo Apple */
.apple-user-card {
  background: linear-gradient(180deg, #ffffff 0%, #f9fafb 100%);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 14px;
  padding: 0.625rem 0.875rem !important;
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.04),
    0 1px 2px rgba(0, 0, 0, 0.02);
}

.apple-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
}

.apple-avatar-blue {
  background: linear-gradient(180deg, #e1f0ff 0%, #cce4ff 100%);
  border: 2px solid #0a84ff;
}

.apple-avatar-red {
  background: linear-gradient(180deg, #ffe5e5 0%, #ffcccc 100%);
  border: 2px solid #ff453a;
}

.apple-avatar-initials {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1d1d1f;
}

.apple-user-name {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
  font-size: 0.875rem;
  font-weight: 600;
  color: #1d1d1f;
  letter-spacing: -0.01em;
}

.apple-user-role {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
  font-size: 0.75rem;
  color: #86868b;
}

.apple-status-badge {
  padding: 0.25rem 0.625rem;
  border-radius: 100px;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
  font-size: 0.6875rem;
  font-weight: 500;
  letter-spacing: 0.02em;
}

.apple-badge-blue {
  background: rgba(10, 132, 255, 0.1);
  color: #0a84ff;
}

.apple-badge-red {
  background: rgba(255, 69, 58, 0.1);
  color: #ff453a;
}

/* Step cards estilo Apple */
.apple-step-card {
  background: linear-gradient(180deg, #ffffff 0%, #fafafa 100%);
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 12px;
  padding: 0.5rem 0.875rem !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-step-card:hover {
  border-color: rgba(0, 0, 0, 0.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.apple-step-number {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: linear-gradient(180deg, #0a84ff 0%, #0071e3 100%);
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
  font-size: 0.6875rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.5rem;
  box-shadow: 0 2px 6px rgba(10, 132, 255, 0.3);
  flex-shrink: 0;
}

.apple-step-title {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #1d1d1f;
  letter-spacing: -0.01em;
}

.apple-completed-badge {
  display: flex;
  align-items: center;
  padding: 0.25rem 0.625rem;
  border-radius: 100px;
  background: rgba(48, 209, 88, 0.1);
  color: #30d158;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
  font-size: 0.6875rem;
  font-weight: 500;
  animation: apple-badge-pop 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes apple-badge-pop {
  0% { transform: scale(0.8); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

/* Image preview estilo Apple */
.apple-image-preview {
  position: relative;
  width: 100%;
  height: 140px;
  border-radius: 12px;
  overflow: hidden;
  background: #f5f5f7;
  box-shadow: 
    0 4px 12px rgba(0, 0, 0, 0.1),
    inset 0 0 0 1px rgba(0, 0, 0, 0.05);
}

.apple-image-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 0.75rem;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.6));
  display: flex;
  justify-content: flex-end;
}

.apple-delete-image-btn {
  display: flex;
  align-items: center;
  padding: 0.375rem 0.75rem;
  border-radius: 100px;
  background: rgba(255, 69, 58, 0.9);
  backdrop-filter: blur(10px);
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
  font-size: 0.75rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-delete-image-btn:hover {
  background: rgba(255, 69, 58, 1);
  transform: scale(1.05);
}

.apple-delete-image-btn:active {
  transform: scale(0.95);
}

/* Photo buttons estilo Apple */
.apple-photo-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.apple-photo-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 0.5rem;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  min-height: 70px;
}

.apple-photo-btn-camera {
  background: linear-gradient(180deg, #d6214c 0%, #a81839 100%);
  color: white;
  box-shadow: 
    0 4px 14px rgba(214, 33, 76, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
}

.apple-photo-btn-gallery {
  background: linear-gradient(180deg, #4442a8 0%, #362f8c 100%);
  color: white;
  box-shadow: 
    0 4px 14px rgba(68, 66, 168, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
}

.apple-photo-btn:hover {
  transform: scale(1.02) translateY(-2px);
  box-shadow: 
    0 8px 20px rgba(0, 0, 0, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.apple-photo-btn:active {
  transform: scale(0.98);
}

.apple-photo-btn-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.375rem;
}

.apple-photo-btn-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.apple-photo-btn-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.apple-photo-btn-title {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
  font-size: 0.875rem;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.apple-photo-btn-subtitle {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
  font-size: 0.6875rem;
  opacity: 0.85;
}

/* Textarea estilo Apple */
.apple-textarea {
  width: 100%;
  padding: 0.875rem 1rem;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: linear-gradient(180deg, #ffffff 0%, #fafafa 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
  font-size: 0.875rem;
  color: #1d1d1f;
  resize: none;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.04);
}

.apple-textarea:focus {
  outline: none;
  border-color: #0a84ff;
  box-shadow: 
    0 0 0 3px rgba(10, 132, 255, 0.15),
    inset 0 1px 2px rgba(0, 0, 0, 0.02);
}

.apple-textarea::placeholder {
  color: #86868b;
}

/* Action buttons estilo Apple */
.apple-action-buttons {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.apple-btn-cancel {
  flex: 0.4;
  padding: 0.875rem 1rem;
  border-radius: 12px;
  border: none;
  background: linear-gradient(180deg, #f5f5f7 0%, #e8e8ed 100%);
  color: #1d1d1f;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 
    0 2px 6px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
}

.apple-btn-cancel:hover {
  background: linear-gradient(180deg, #ffffff 0%, #f0f0f5 100%);
  transform: scale(1.02);
}

.apple-btn-cancel:active {
  transform: scale(0.98);
  background: linear-gradient(180deg, #e8e8ed 0%, #d8d8de 100%);
}

.apple-btn-submit {
  flex: 0.6;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.875rem 1.25rem;
  border-radius: 12px;
  border: none;
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  position: relative;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-btn-entrada {
  background: linear-gradient(180deg, #0a84ff 0%, #0071e3 100%);
  box-shadow: 
    0 4px 14px rgba(10, 132, 255, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.apple-btn-salida {
  background: linear-gradient(180deg, #ff453a 0%, #d70015 100%);
  box-shadow: 
    0 4px 14px rgba(255, 69, 58, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.apple-btn-submit:hover:not(.apple-btn-disabled) {
  transform: scale(1.02) translateY(-1px);
}

.apple-btn-submit:active:not(.apple-btn-disabled) {
  transform: scale(0.98);
}

.apple-btn-disabled {
  opacity: 0.5;
  cursor: not-allowed;
  filter: saturate(0.8);
}

/* Spinner estilo Apple */
.apple-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
}

.apple-spinner-ring {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: apple-spin 0.8s linear infinite;
}

@keyframes apple-spin {
  to { transform: rotate(360deg); }
}

/* Checklist card estilo Apple - Amarillo oscuro */
.apple-checklist-card {
  background: linear-gradient(135deg, #fef9e7 0%, #fcf3cf 100%);
  border: 1px solid rgba(180, 140, 0, 0.2);
  border-radius: 14px;
  padding: 0.75rem 0.875rem !important;
  box-shadow: 0 2px 8px rgba(180, 140, 0, 0.1);
}

.apple-checklist-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}

.apple-checklist-icon {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: linear-gradient(180deg, #d4a000 0%, #b8860b 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: 0.625rem;
  box-shadow: 0 2px 6px rgba(180, 134, 11, 0.35);
}

.apple-checklist-title {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #1d1d1f;
  letter-spacing: -0.01em;
}

.apple-checklist-items {
  display: flex;
  gap: 0.5rem;
}

.apple-checklist-item {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 0.5rem 0.625rem;
  border-radius: 10px;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
  font-size: 0.6875rem;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Estados del item del checklist */
.apple-checklist-done,
.apple-checklist-item-done {
  background: rgba(48, 209, 88, 0.1);
  color: #30d158;
  border: 1px solid rgba(48, 209, 88, 0.2);
}

.apple-checklist-pending,
.apple-checklist-item-pending {
  background: rgba(142, 142, 147, 0.1);
  color: #8e8e93;
  border: 1px solid rgba(142, 142, 147, 0.15);
}

/* Círculo de check */
.apple-checklist-check,
.apple-checklist-circle {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.375rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
}

.apple-check-done,
.apple-checklist-circle-done {
  background: linear-gradient(180deg, #30d158 0%, #28a745 100%);
  box-shadow: 0 2px 4px rgba(48, 209, 88, 0.3);
}

.apple-check-pending,
.apple-checklist-circle-pending {
  background: #c7c7cc;
}

/* Ready card estilo Apple */
.apple-ready-card {
  background: linear-gradient(135deg, rgba(48, 209, 88, 0.1) 0%, rgba(52, 199, 89, 0.15) 100%);
  border: 1px solid rgba(48, 209, 88, 0.25);
  border-radius: 14px;
  padding: 0.75rem 0.5rem;
  animation: apple-ready-pop 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes apple-ready-pop {
  0% {
    transform: scale(0.95);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.apple-ready-content {
  display: flex;
  align-items: center;
  justify-content: center;
}

.apple-ready-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(180deg, #30d158 0%, #28a745 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.5rem;
  animation: apple-pulse-icon 1.5s ease-in-out infinite;
  box-shadow: 0 3px 8px rgba(48, 209, 88, 0.4);
}

@keyframes apple-pulse-icon {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.apple-ready-text {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #30d158;
  letter-spacing: -0.01em;
}

/* ========================================
   ESTILOS APPLE PARA SECCIÓN ACTIVIDADES (MORADO)
   ======================================== */

/* Contenedor principal actividades - Liquid Glass */
.apple-activities-container {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.95) 0%, 
    rgba(252, 250, 255, 0.9) 25%,
    rgba(248, 245, 255, 0.85) 50%,
    rgba(252, 250, 255, 0.9) 75%,
    rgba(255, 255, 255, 0.95) 100%) !important;
  backdrop-filter: blur(20px) saturate(180%) !important;
  -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
  border: 1px solid rgba(147, 51, 234, 0.15);
  border-radius: 24px;
  padding: 0.5rem 0 !important;
  box-shadow: 
    0 8px 32px rgba(147, 51, 234, 0.12),
    0 2px 8px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.8),
    inset 0 -1px 0 rgba(147, 51, 234, 0.05);
  animation: apple-fade-in 0.4s ease-out;
  position: relative;
  overflow: hidden;
}

.apple-activities-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(180deg, 
    rgba(255, 255, 255, 0.4) 0%, 
    rgba(255, 255, 255, 0) 100%);
  pointer-events: none;
  border-radius: 24px 24px 0 0;
}

/* Header morado */
.apple-header-purple {
  background: linear-gradient(180deg, #9333ea 0%, #7c3aed 100%);
  box-shadow: 
    0 4px 14px rgba(147, 51, 234, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

/* Avatar morado */
.apple-avatar-purple {
  background: linear-gradient(180deg, rgba(147, 51, 234, 0.1) 0%, rgba(124, 58, 237, 0.15) 100%);
  border-color: #9333ea;
}

.apple-avatar-purple .apple-avatar-initials {
  color: #7c3aed;
}

/* Badge morado */
.apple-badge-purple {
  background: rgba(147, 51, 234, 0.1);
  color: #9333ea;
}

/* Step card morado */
.apple-step-card-purple {
  background: linear-gradient(180deg, #ffffff 0%, #fdfaff 100%);
  border: 1px solid rgba(147, 51, 234, 0.1);
  border-radius: 12px;
  padding: 0.5rem 0.875rem !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-step-card-purple:hover {
  border-color: rgba(147, 51, 234, 0.2);
  box-shadow: 0 4px 12px rgba(147, 51, 234, 0.08);
}

/* Step number morado */
.apple-step-number-purple {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: linear-gradient(180deg, #9333ea 0%, #7c3aed 100%);
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
  font-size: 0.6875rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.5rem;
  box-shadow: 0 2px 6px rgba(147, 51, 234, 0.3);
  flex-shrink: 0;
}

/* Warning card estilo Apple */
.apple-warning-card {
  background: linear-gradient(135deg, rgba(255, 214, 10, 0.15) 0%, rgba(255, 149, 0, 0.1) 100%);
  border: 1px solid rgba(255, 149, 0, 0.3);
  border-left: 4px solid #ff9500;
  border-radius: 12px;
  padding: 0.75rem 0.5rem;
  animation: apple-fade-in 0.3s ease-out;
}

.apple-warning-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255, 149, 0, 0.15);
  color: #ff9500;
  display: flex;
  align-items: center;
  justify-content: center;
}

.apple-warning-title {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #995a00;
  letter-spacing: -0.01em;
}

.apple-warning-text {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
  font-size: 0.75rem;
  color: #996600;
  margin-top: 0.25rem;
}

/* Select estilo Apple */
.apple-select {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
  font-size: 0.875rem;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  border: 1px solid rgba(147, 51, 234, 0.15);
  background: linear-gradient(180deg, #ffffff 0%, #fdfaff 100%);
  color: #1d1d1f;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  outline: none;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.apple-select:focus {
  border-color: #9333ea;
  box-shadow: 0 0 0 3px rgba(147, 51, 234, 0.15);
}

/* Input estilo Apple */
.apple-input {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
  font-size: 0.875rem;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: linear-gradient(180deg, #ffffff 0%, #fafafa 100%);
  color: #1d1d1f;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  outline: none;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.apple-input:focus {
  border-color: #9333ea;
  box-shadow: 0 0 0 3px rgba(147, 51, 234, 0.15);
  background: #ffffff;
}

.apple-input-label {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
  font-size: 0.75rem;
  font-weight: 500;
  color: #86868b;
}

/* Textarea estilo Apple */
.apple-textarea {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
  font-size: 0.875rem;
  padding: 0.875rem 1rem;
  border-radius: 12px;
  border: 1px solid rgba(147, 51, 234, 0.12);
  background: linear-gradient(180deg, #ffffff 0%, #fdfaff 100%);
  color: #1d1d1f;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  outline: none;
  resize: vertical;
  min-height: 80px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.apple-textarea:focus {
  border-color: #9333ea;
  box-shadow: 0 0 0 3px rgba(147, 51, 234, 0.15);
  background: #ffffff;
}

.apple-textarea::placeholder {
  color: #86868b;
  font-weight: 400;
}

/* Botones de foto oscuros para actividades */
.apple-photo-btn-camera-dark {
  background: linear-gradient(180deg, #d6214c 0%, #a81839 100%);
  color: white;
  box-shadow: 
    0 4px 14px rgba(214, 33, 76, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
}

.apple-photo-btn-gallery-dark {
  background: linear-gradient(180deg, #4442a8 0%, #362f8c 100%);
  color: white;
  box-shadow: 
    0 4px 14px rgba(68, 66, 168, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
}

.apple-photo-btn-text {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
  font-size: 0.8125rem;
  font-weight: 600;
  letter-spacing: -0.01em;
  margin-top: 0.5rem;
}

/* Vista previa de foto estilo Apple */
.apple-photo-preview {
  position: relative;
  animation: apple-fade-in 0.3s ease-out;
}

.apple-photo-container {
  width: 100%;
  height: 140px;
  border-radius: 14px;
  overflow: hidden;
  background: #f5f5f7;
  border: 1px solid rgba(147, 51, 234, 0.15);
  box-shadow: 
    0 4px 12px rgba(147, 51, 234, 0.1),
    inset 0 0 0 1px rgba(0, 0, 0, 0.05);
}

.apple-photo-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 0.75rem;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.5));
  display: flex;
  justify-content: flex-end;
  border-radius: 0 0 14px 14px;
}

.apple-photo-delete-btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  border-radius: 100px;
  background: rgba(255, 69, 58, 0.9);
  backdrop-filter: blur(10px);
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
  font-size: 0.6875rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.apple-photo-delete-btn:hover {
  background: rgba(255, 69, 58, 1);
  transform: scale(1.05);
}

.apple-photo-delete-btn:active {
  transform: scale(0.95);
}

/* ========================================
   MEDIA QUERIES RESPONSIVAS ESTILO APPLE
   ======================================== */

/* Pantallas pequeñas (móviles) */
@media (max-width: 374px) {
  .apple-header-card {
    padding: 0.5rem 0.75rem !important;
    border-radius: 12px;
  }
  
  .apple-header-icon {
    width: 28px;
    height: 28px;
    border-radius: 6px;
    margin-right: 0.5rem;
  }
  
  .apple-header-icon svg {
    width: 16px;
    height: 16px;
  }
  
  .apple-header-title {
    font-size: 0.8125rem;
  }
  
  .apple-step-card,
  .apple-step-card-purple {
    padding: 0.5rem 0.75rem !important;
    border-radius: 12px;
  }

  .apple-step-number,
  .apple-step-number-purple {
    width: 18px;
    height: 18px;
    font-size: 0.625rem;
    margin-right: 0.375rem;
  }

  .apple-step-title {
    font-size: 0.75rem;
  }

  .apple-user-card {
    padding: 0.5rem 0.75rem !important;
    border-radius: 12px;
  }
  
  .apple-avatar,
  .apple-avatar-purple {
    width: 36px;
    height: 36px;
  }
  
  .apple-avatar-initials {
    font-size: 0.6875rem;
  }
  
  .apple-photo-buttons {
    gap: 0.375rem;
  }
  
  .apple-photo-btn {
    padding: 0.625rem 0.375rem;
    min-height: 60px;
  }
  
  .apple-checklist-card {
    padding: 0.5rem 0.375rem;
  }
}

/* Pantallas medianas (móviles grandes) */
@media (min-width: 375px) and (max-width: 428px) {
  .apple-header-card {
    padding: 0.5rem 0.875rem !important;
  }
  
  .apple-header-icon {
    width: 30px;
    height: 30px;
  }
  
  .apple-header-icon svg {
    width: 17px;
    height: 17px;
  }
  
  .apple-header-title {
    font-size: 0.875rem;
  }
  
  .apple-step-number,
  .apple-step-number-purple {
    width: 19px;
    height: 19px;
  }
  
  .apple-step-title {
    font-size: 0.8125rem;
  }
}

/* Pantallas grandes (tablets y desktop) */
@media (min-width: 429px) {
  .apple-header-card {
    padding: 0.625rem 1rem !important;
  }
  
  .apple-header-icon {
    width: 34px;
    height: 34px;
    border-radius: 10px;
  }
  
  .apple-header-icon svg {
    width: 20px;
    height: 20px;
  }
  
  .apple-header-title {
    font-size: 1rem;
  }
  
  .apple-step-number,
  .apple-step-number-purple {
    width: 22px;
    height: 22px;
    font-size: 0.75rem;
  }
  
  .apple-step-title {
    font-size: 0.875rem;
  }
  
  .apple-step-card,
  .apple-step-card-purple {
    padding: 0.5rem 1rem !important;
  }
}

/* Tablets */
@media (min-width: 768px) {
  .apple-activities-container,
  .apple-attendance-container {
    max-width: 500px;
    margin: 0 auto;
  }
  
  .apple-header-title {
    font-size: 1.0625rem;
  }
}

/* ========================================
   BOTÓN DE UBICACIÓN APPLE CIRCULAR
   ======================================== */

.apple-location-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.875rem;
  padding: 0.5rem 0;
}

.apple-location-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.625rem;
}

/* Botón circular principal */
.apple-location-btn {
  position: relative;
  width: 72px;
  height: 72px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  outline: none;
  -webkit-tap-highlight-color: transparent;
}

/* Estado default - azul Apple */
.apple-location-btn-default {
  background: linear-gradient(180deg, #0a84ff 0%, #0071e3 100%);
  box-shadow: 
    0 6px 20px rgba(10, 132, 255, 0.4),
    0 2px 6px rgba(10, 132, 255, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.apple-location-btn-default:hover {
  transform: scale(1.05);
  box-shadow: 
    0 8px 28px rgba(10, 132, 255, 0.5),
    0 4px 10px rgba(10, 132, 255, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.25);
}

.apple-location-btn-default:active {
  transform: scale(0.95);
  box-shadow: 
    0 3px 12px rgba(10, 132, 255, 0.4),
    inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Estado loading */
.apple-location-btn-loading {
  background: linear-gradient(180deg, #5ac8fa 0%, #34aadc 100%);
  box-shadow: 
    0 6px 20px rgba(90, 200, 250, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  cursor: wait;
}

/* Estado success - verde Apple */
.apple-location-btn-success {
  background: linear-gradient(180deg, #30d158 0%, #28a745 100%);
  box-shadow: 
    0 6px 20px rgba(48, 209, 88, 0.4),
    0 2px 6px rgba(48, 209, 88, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.apple-location-btn-success:hover {
  transform: scale(1.02);
}

/* Estado disabled - gris Apple */
.apple-location-btn-disabled {
  background: linear-gradient(180deg, #8e8e93 0%, #636366 100%);
  box-shadow: 
    0 4px 12px rgba(142, 142, 147, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  cursor: not-allowed;
  opacity: 0.7;
}

/* Icono central */
.apple-location-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  z-index: 2;
}

/* Anillo de progreso animado estilo Apple */
.apple-location-ring {
  position: absolute;
  inset: -6px;
  z-index: 1;
  animation: apple-ring-rotate 1s linear infinite;
}

.apple-location-ring-svg {
  width: 100%;
  height: 100%;
}

.apple-location-ring-bg {
  fill: none;
  stroke: rgba(255, 255, 255, 0.15);
  stroke-width: 4;
}

.apple-location-ring-progress {
  fill: none;
  stroke: white;
  stroke-width: 4;
  stroke-linecap: round;
  /* Circunferencia = 2 * PI * r = 2 * 3.14159 * 45 = 282.74 */
  /* Mostrar ~25% del arco visible */
  stroke-dasharray: 70 213;
  stroke-dashoffset: 0;
  transform-origin: center;
}

@keyframes apple-ring-rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Pulso de éxito */
.apple-location-pulse {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: rgba(48, 209, 88, 0.3);
  animation: apple-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  z-index: 0;
}

@keyframes apple-pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.6;
  }
  50% {
    transform: scale(1.15);
    opacity: 0;
  }
}

/* Información de ubicación */
.apple-location-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.125rem;
}

.apple-location-title {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #1d1d1f;
  letter-spacing: -0.01em;
}

.apple-location-subtitle {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
  font-size: 0.6875rem;
  font-weight: 400;
  color: #86868b;
}

/* Coordenadas compactas */
.apple-coordinates {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(48, 209, 88, 0.08) 0%, rgba(52, 199, 89, 0.12) 100%);
  border: 1px solid rgba(48, 209, 88, 0.2);
  border-radius: 100px;
  padding: 0.25rem 0.5rem;
  animation: apple-coords-appear 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  max-width: 100%;
  overflow: hidden;
}

@keyframes apple-coords-appear {
  from {
    opacity: 0;
    transform: translateY(-8px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.apple-coord-item {
  display: flex;
  align-items: center;
  gap: 0.125rem;
  min-width: 0;
  flex-shrink: 1;
}

.apple-coord-label {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
  font-size: 0.5rem;
  font-weight: 600;
  color: #30d158;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  flex-shrink: 0;
}

.apple-coord-value {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Mono', 'Menlo', monospace;
  font-size: 0.5625rem;
  font-weight: 500;
  color: #1d1d1f;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 80px;
}

.apple-coord-divider {
  width: 1px;
  height: 10px;
  background: rgba(48, 209, 88, 0.3);
  margin: 0 0.375rem;
  flex-shrink: 0;
}

/* Responsividad del botón de ubicación */
@media (max-width: 374px) {
  .apple-location-btn {
    width: 64px;
    height: 64px;
  }
  
  .apple-location-icon svg {
    width: 24px;
    height: 24px;
  }
  
  .apple-location-title {
    font-size: 0.75rem;
  }
  
  .apple-location-subtitle {
    font-size: 0.625rem;
  }
  
  .apple-coordinates {
    padding: 0.1875rem 0.375rem;
  }
  
  .apple-coord-label {
    font-size: 0.4375rem;
  }
  
  .apple-coord-value {
    font-size: 0.5rem;
    max-width: 60px;
  }
  
  .apple-coord-divider {
    margin: 0 0.25rem;
    height: 8px;
  }
}

@media (min-width: 375px) and (max-width: 428px) {
  .apple-coord-value {
    max-width: 70px;
  }
}

@media (min-width: 429px) {
  .apple-location-btn {
    width: 80px;
    height: 80px;
  }
  
  .apple-location-icon svg {
    width: 32px;
    height: 32px;
  }
  
  .apple-location-title {
    font-size: 0.875rem;
  }
  
  .apple-location-subtitle {
    font-size: 0.75rem;
  }
  
  .apple-coord-value {
    max-width: 100px;
    font-size: 0.625rem;
  }
  
  .apple-coord-label {
    font-size: 0.5625rem;
  }
}
</style>