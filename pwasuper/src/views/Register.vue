<template>
  <div class="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-emerald-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-teal-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>
    
    <div class="page-container w-full max-w-md relative z-10 px-2">
      <!-- Back to Login Link - Top Left -->
      <div class="flex justify-start mb-3">
        <router-link to="/login" class="text-sm font-medium text-primary hover:text-primary-dark transition-colors duration-200 glass-link">
          ← Volver al inicio de sesión
        </router-link>
      </div>

      <!-- Header Section -->
      <div class="text-center mb-4">
        <h1 class="text-lg font-bold text-primary mb-1 text-center glass-title">Crear Cuenta</h1>
        <h2 class="text-base font-semibold text-gray-700">Registro</h2>
        <p class="mt-1 text-gray-500 text-xs">Completa los datos para crear tu cuenta</p>
      </div>

      <!-- Success Message -->
      <transition name="modal-fade">
        <div v-if="showSuccessModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
          <div class="success-modal-card w-full max-w-sm mx-4 transform transition-all duration-500 animate-bounce-in">
            <div class="p-6 text-center relative overflow-hidden">
              
              <!-- Elementos decorativos de fondo -->
              <div class="absolute inset-0 opacity-10">
                <div class="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-green-400 via-emerald-300 to-teal-400"></div>
                <div class="absolute -top-4 -right-4 w-16 h-16 bg-white/20 rounded-full animate-pulse"></div>
                <div class="absolute -bottom-2 -left-2 w-12 h-12 bg-green-400/30 rounded-full animate-pulse" style="animation-delay: 1s;"></div>
              </div>

              <!-- Icono de éxito animado -->
              <div class="relative z-10 mx-auto mb-4 w-20 h-20 bg-gradient-to-br from-green-400 to-emerald-500 rounded-full flex items-center justify-center shadow-lg animate-success-icon">
                <div class="absolute inset-0 bg-gradient-to-br from-green-300 to-emerald-400 rounded-full animate-ping opacity-20"></div>
                <svg class="w-10 h-10 text-white animate-check-draw" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" class="check-path"></path>
                </svg>
              </div>
              
              <!-- Título -->
              <h3 class="relative z-10 text-xl font-bold text-green-600 mb-2 animate-slide-up">¡Registro Exitoso!</h3>
              
              <!-- Mensaje -->
              <p class="relative z-10 text-gray-700 mb-6 text-sm leading-relaxed animate-slide-up" style="animation-delay: 0.2s;">
                Tu cuenta ha sido creada correctamente.<br>
                <span class="text-green-600 font-medium">Serás redirigido al login...</span>
              </p>
              
              <!-- Barra de progreso mejorada -->
              <div class="relative z-10 w-full bg-gray-200 rounded-full h-2 mb-6 overflow-hidden animate-slide-up" style="animation-delay: 0.4s;">
                <div class="bg-gradient-to-r from-green-400 to-emerald-500 h-2 rounded-full animate-progress-fill shadow-sm relative">
                  <div class="absolute inset-0 bg-white/30 animate-shimmer"></div>
                </div>
              </div>
              
              <!-- Botón mejorado -->
              <button @click="goToLogin" class="relative z-10 success-button animate-slide-up" style="animation-delay: 0.6s;">
                <span class="relative z-10">Ir al Login Ahora</span>
                <div class="absolute inset-0 bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </button>

              <!-- Confeti animado -->
              <div class="absolute inset-0 pointer-events-none">
                <div class="confetti-1"></div>
                <div class="confetti-2"></div>
                <div class="confetti-3"></div>
                <div class="confetti-4"></div>
                <div class="confetti-5"></div>
                <div class="confetti-6"></div>
              </div>
            </div>
          </div>
        </div>
      </transition>

      <!-- Error Message -->
      <transition name="bounce">
        <div v-if="message.text && message.type === 'error'" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg shadow-sm mb-4" role="alert">
          <p class="flex items-center text-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            {{ message.text }}
          </p>
        </div>
      </transition>

      <!-- Register Form -->
      <div class="glass-card">

        <form @submit.prevent="register" @keydown.enter="handleEnterKey">
          <div class="space-y-3">
            <div>
              <label for="email" class="block text-xs font-medium text-gray-800 mb-1">Correo electrónico *</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                </div>
                <input 
                  v-model="form.email" 
                  id="email" 
                  name="email" 
                  type="email" 
                  autocomplete="email" 
                  required 
                  class="glass-input w-full pl-9 pr-3 py-2" 
                  placeholder="ejemplo@correo.com" 
                />
              </div>
            </div>
            
            <!-- Campos separados para nombre completo -->
            <div>
              <label for="nombre" class="block text-xs font-medium text-gray-800 mb-1">Nombre(s) *</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <input 
                  v-model="form.nombre" 
                  @input="formatNombre"
                  id="nombre" 
                  name="nombre" 
                  type="text" 
                  required 
                  class="glass-input w-full pl-9 pr-3 py-2 uppercase" 
                  placeholder="Ej. JOSÉ MARÍA" 
                />
              </div>
              <p class="mt-1 text-xs text-gray-500">Ingresa tu nombre o nombres de pila</p>
            </div>
            
            <div>
              <label for="primerApellido" class="block text-xs font-medium text-gray-800 mb-1">Apellido Paterno *</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <input 
                  v-model="form.primerApellido" 
                  @input="formatPrimerApellido"
                  id="primerApellido" 
                  name="primerApellido" 
                  type="text" 
                  required 
                  class="glass-input w-full pl-9 pr-3 py-2 uppercase" 
                  placeholder="Ej. GARCÍA" 
                />
              </div>
              <p class="mt-1 text-xs text-gray-500">Apellido del padre</p>
            </div>
            
            <div>
              <label for="segundoApellido" class="block text-xs font-medium text-gray-800 mb-1">Apellido Materno *</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <input 
                  v-model="form.segundoApellido" 
                  @input="formatSegundoApellido"
                  id="segundoApellido" 
                  name="segundoApellido" 
                  type="text" 
                  required 
                  class="glass-input w-full pl-9 pr-3 py-2 uppercase" 
                  placeholder="Ej. LÓPEZ" 
                />
              </div>
              <p class="mt-1 text-xs text-gray-500">Apellido de la madre</p>
            </div>
            
            <div>
              <label for="cargo" class="block text-xs font-medium text-gray-800 mb-1">Puesto de Trabajo *</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <input 
                  v-model="form.cargo" 
                  @input="formatCargo"
                  id="cargo" 
                  name="cargo" 
                  type="text" 
                  required 
                  class="glass-input w-full pl-9 pr-3 py-2 uppercase" 
                  placeholder="Ej. TÉCNICO AGRÍCOLA" 
                />
              </div>
              <p class="mt-1 text-xs text-gray-500">Indica tu posición o rol laboral actual</p>
            </div>
            
            <div>
              <label for="curp" class="block text-xs font-medium text-gray-800 mb-1">CURP *</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <input 
                  v-model="form.curp" 
                  @input="formatCurp" 
                  id="curp" 
                  name="curp" 
                  type="text" 
                  required
                  maxlength="18" 
                  placeholder="18 caracteres en mayúsculas"
                  class="glass-input w-full pl-9 pr-3 py-2 uppercase tracking-wide" 
                />
              </div>
              <p v-if="curpError" class="mt-1 text-xs text-red-600">{{ curpError }}</p>
              <p class="mt-1 text-xs text-gray-500">La CURP debe contener exactamente 18 caracteres en mayúsculas</p>
              <p v-if="curpWarning" class="mt-1 text-xs text-green-600">{{ curpWarning }}</p>
            </div>
            
            <div>
              <label for="supervisor" class="block text-xs font-medium text-gray-800 mb-1">Supervisor Inmediato *</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
                <input 
                  v-model="form.supervisor" 
                  @input="formatSupervisor"
                  id="supervisor" 
                  name="supervisor" 
                  type="text" 
                  required
                  class="glass-input w-full pl-9 pr-3 py-2 uppercase" 
                  placeholder="Ej. MARÍA GARCÍA LÓPEZ" 
                />
              </div>
              <p class="mt-1 text-xs text-gray-500">Nombre completo de tu jefe directo o coordinador</p>
            </div>
            
            <div>
              <label for="telefono" class="block text-xs font-medium text-gray-800 mb-1">Número de teléfono *</label>
              <div class="flex space-x-2">
                <!-- Selector de código de país -->
                <div class="relative">
                  <button 
                    type="button"
                    @click="showCountrySelector = !showCountrySelector"
                    class="glass-input flex items-center px-2 py-2 min-w-[80px] justify-between text-sm"
                  >
                    <div class="flex items-center">
                      <span class="text-xs mr-1">{{ paises.find(p => p.codigo === form.codigoPais)?.bandera || '🌎' }}</span>
                      <span class="text-xs font-medium">{{ form.codigoPais }}</span>
                    </div>
                    <svg class="w-3 h-3 ml-1 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                  </button>
                  
                  <!-- Dropdown para selección de país -->
                  <div 
                    v-if="showCountrySelector" 
                    class="absolute z-50 w-64 top-full left-0 mt-1 bg-white/90 backdrop-filter backdrop-blur-lg border border-white/20 rounded-lg shadow-xl overflow-hidden"
                  >
                    <!-- Barra de búsqueda -->
                    <div class="sticky top-0 bg-white/80 backdrop-filter backdrop-blur-lg p-2 border-b border-white/20">
                      <input 
                        type="text"
                        v-model="countrySearch"
                        placeholder="Buscar país..."
                        class="w-full px-2 py-1 border border-gray-300 rounded text-xs focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                        @click="$event.stopPropagation()"
                      />
                    </div>
                    
                    <ul class="py-1 max-h-48 overflow-y-auto">
                      <li 
                        v-for="pais in filteredCountries" 
                        :key="pais.codigo"
                        @click="selectCountry(pais)"
                        class="flex items-center px-2 py-1 hover:bg-white/20 cursor-pointer transition-colors"
                      >
                        <span class="text-sm mr-2">{{ pais.bandera }}</span>
                        <span class="flex-1 text-xs">{{ pais.nombre }}</span>
                        <span class="text-gray-500 font-mono text-xs">{{ pais.codigo }}</span>
                      </li>
                      <li v-if="filteredCountries.length === 0" class="px-2 py-1 text-gray-500 text-center text-xs">
                        No se encontraron países
                      </li>
                    </ul>
                  </div>
                </div>
                
                <!-- Campo de entrada del número -->
                <div class="flex-1">
                  <input 
                    v-model="form.telefono" 
                    id="telefono" 
                    name="telefono" 
                    type="tel" 
                    required
                    maxlength="10"
                    pattern="[0-9]{10}"
                    placeholder="10 dígitos" 
                    class="glass-input w-full py-2 px-3 text-sm"
                    @input="validatePhone"
                  />
                </div>
              </div>
              <p class="mt-1 text-xs text-gray-500">Ingresa solo los 10 dígitos de tu número (sin lada)</p>
            </div>
            
            <div>
              <label for="password" class="block text-xs font-medium text-gray-800 mb-1">Contraseña</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <input 
                  v-model="form.password" 
                  id="password" 
                  name="password" 
                  :type="showPassword ? 'text' : 'password'" 
                  required 
                  class="glass-input w-full pl-9 pr-9 py-2 text-sm" 
                  placeholder="••••••••" 
                  minlength="6"
                />
                <button
                  type="button"
                  @click="togglePasswordVisibility"
                  class="absolute inset-y-0 right-0 flex items-center pr-2 text-primary hover:text-primary-dark focus:outline-none transition-colors duration-200"
                >
                  <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              </div>
              <p class="mt-1 text-xs text-gray-500">Mínimo 6 caracteres</p>
            </div>

            <div>
              <label for="confirmPassword" class="block text-xs font-medium text-gray-800 mb-1">Confirmar contraseña</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <input 
                  v-model="form.confirmPassword" 
                  id="confirmPassword" 
                  name="confirmPassword" 
                  :type="showConfirmPassword ? 'text' : 'password'" 
                  required 
                  class="glass-input w-full pl-9 pr-9 py-2 text-sm" 
                  placeholder="Confirmar contraseña" 
                  minlength="6"
                />
                <button
                  type="button"
                  @click="toggleConfirmPasswordVisibility"
                  class="absolute inset-y-0 right-0 flex items-center pr-2 text-primary hover:text-primary-dark focus:outline-none transition-colors duration-200"
                >
                  <svg v-if="showConfirmPassword" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- AVISO DE PRIVACIDAD -->
          <div class="mt-4 mb-3">
            <div class="glass-card-inner">
              <div class="p-3">
                <h3 class="font-bold text-orange-600 mb-2 text-base bg-gradient-to-r from-yellow-200/80 to-yellow-100/80 px-2 py-1 rounded-lg shadow-sm border border-yellow-300/50 backdrop-filter backdrop-blur-sm">
                  Aviso de Privacidad
                </h3>
                <div class="max-h-32 overflow-y-auto text-xs text-gray-700 space-y-1 pr-2">
                  <div class="font-semibold">AVISO DE PRIVACIDAD PARA EL REGISTRO Y USO DE INFORMACIÓN DE LOS TÉCNICOS DEL PROGRAMA SEMBRANDO VIDA MEDIANTE APLICACIÓN MÓVIL OFICIAL</div>
                  
                  <p>En cumplimiento con lo dispuesto por la Ley General de Transparencia y Acceso a la Información pública y la Ley Federal de Transparencia y Acceso a la Información Pública, se informa a las y los Técnico(a)s del Programa Sembrando Vida que los datos personales recabados serán tratados conforme a los siguientes términos:</p>
                  
                  <div class="font-semibold">1. Identidad y domicilio del responsable</div>
                  <p>El responsable del tratamiento de los datos personales es la Secretaría de Bienestar, Subsecretaria de Inclusión Productiva y Desarrollo Rural con domicilio en: Av. P.º de la Reforma 116, Juárez, Cuauhtémoc, 06600 Ciudad de México, CDMX.</p>
                  
                  <div class="font-semibold">2. Datos personales que se recaban</div>
                  <ul class="list-disc pl-4 space-y-1">
                    <li>Nombre completo, CURP, Número telefónico, Correo electrónico</li>
                    <li>Cargo y supervisor asignado</li>
                    <li>Datos de localización geográfica precisa, capturados a través de coordenadas</li>
                    <li>Actividades realizadas en campo y fotografías</li>
                  </ul>
                  
                  <div class="font-semibold">3. Finalidades del tratamiento</div>
                  <p>Los datos serán utilizados exclusivamente para registrar actividades de técnicos, documentar avances del programa y elaborar reportes internos.</p>
                  
                  <div class="font-semibold">Fecha de última actualización: 12 de agosto del 2025.</div>
                  
                  <p class="font-semibold text-blue-800">Al proporcionar mis datos personales, acepto el tratamiento conforme al Aviso de Privacidad.</p>
                </div>
              </div>
            </div>
            
            <!-- CHECKBOX OBLIGATORIO -->
            <div class="mt-3">
              <div class="flex items-start">
                <div class="flex items-center h-4">
                  <input 
                    v-model="termsAccepted" 
                    @change="clearTermsError"
                    id="terms" 
                    name="terms" 
                    type="checkbox" 
                    class="focus:ring-green-500 h-3 w-3 text-green-600 border-gray-300 rounded"
                    required
                  />
                </div>
                <div class="ml-2 text-xs">
                  <label for="terms" class="font-medium text-gray-700">
                    He leído y acepto el Aviso de Privacidad y los Términos y Condiciones. <span class="text-red-500">*</span>
                  </label>
                </div>
              </div>
              <p v-if="termsError" class="mt-1 text-xs text-red-600">{{ termsError }}</p>
            </div>
          </div>

          <button 
            type="submit" 
            :disabled="loading || !termsAccepted" 
            class="glass-button w-full mt-4 flex items-center justify-center py-2 text-sm"
            :class="{ 'opacity-50 cursor-not-allowed': loading || !termsAccepted }"
          >
            <svg v-if="loading" class="animate-spin h-3 w-3 mr-2" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ loading ? 'Registrando...' : termsAccepted ? 'Registrarme' : 'Debes aceptar los términos' }}</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { apiService } from '../services/apiService.js';
import { checkInternetConnection, getOfflineMessage } from '../utils/network.js';

const router = useRouter();
const loading = ref(false);
const message = reactive({ text: '', type: '' });
const isOnline = ref(true);
const curpError = ref('');
const curpWarning = ref('');
const currentApiUrl = ref('');
const termsAccepted = ref(false);
const termsError = ref('');
const showSuccessModal = ref(false);
const countrySearch = ref('');
const showPassword = ref(false);
const showConfirmPassword = ref(false);

const form = reactive({
  email: '',
  nombre: '',
  primerApellido: '',
  segundoApellido: '',
  cargo: '',
  curp: '',
  supervisor: '',
  codigoPais: '+52', // Código de país por defecto (México)
  telefono: '', // Solo los dígitos del teléfono
  password: '',
  confirmPassword: ''
});

// Lista de países más comunes con sus códigos y banderas
const paises = [
  { codigo: '+52', nombre: 'México', bandera: '🇲🇽' },
  { codigo: '+1', nombre: 'Estados Unidos', bandera: '🇺🇸' },
  { codigo: '+34', nombre: 'España', bandera: '🇪🇸' },
  { codigo: '+57', nombre: 'Colombia', bandera: '🇨🇴' },
  { codigo: '+56', nombre: 'Chile', bandera: '🇨🇱' },
  { codigo: '+54', nombre: 'Argentina', bandera: '🇦🇷' },
  { codigo: '+51', nombre: 'Perú', bandera: '🇵🇪' },
  { codigo: '+591', nombre: 'Bolivia', bandera: '🇧🇴' },
  { codigo: '+502', nombre: 'Guatemala', bandera: '🇬🇹' },
  { codigo: '+503', nombre: 'El Salvador', bandera: '🇸🇻' }
];

const showCountrySelector = ref(false);

// Filtro de países basado en la búsqueda
const filteredCountries = computed(() => {
  if (!countrySearch.value) return paises;
  
  const searchTerm = countrySearch.value.toLowerCase();
  return paises.filter(pais => 
    pais.nombre.toLowerCase().includes(searchTerm) || 
    pais.codigo.includes(searchTerm)
  );
});

onMounted(async () => {
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    message.text = getOfflineMessage();
    message.type = 'error';
  } else {
    try {
      await apiService.refreshApiUrl();
      currentApiUrl.value = apiService.getCurrentApiUrl();
      console.log(`🌐 Usando servidor: ${currentApiUrl.value}`);
    } catch (error) {
      console.warn('Error inicializando servicio API:', error);
    }
  }

  document.addEventListener('click', closeCountrySelector);
  document.addEventListener('keydown', handleEscKey);
});

function togglePasswordVisibility() {
  showPassword.value = !showPassword.value;
}

function toggleConfirmPasswordVisibility() {
  showConfirmPassword.value = !showConfirmPassword.value;
}

async function register() {
  if (!validateForm()) return;
  
  isOnline.value = await checkInternetConnection();
  if (!isOnline.value) {
    message.text = getOfflineMessage();
    message.type = 'error';
    return;
  }
  
  if (loading.value) return;
  
  loading.value = true;
  message.text = '';
  
  try {
    const telefonoCompleto = `${form.codigoPais}${form.telefono.trim()}`;
    // Construir nombre completo a partir de los campos separados
    const nombreCompleto = `${form.nombre.trim()} ${form.primerApellido.trim()} ${form.segundoApellido.trim()}`.toUpperCase();
    
    const payload = {
      correo: form.email.trim(),
      nombre_completo: nombreCompleto,
      cargo: form.cargo.trim().toUpperCase(),
      supervisor: form.supervisor.trim().toUpperCase(),
      contrasena: form.password,
      curp: form.curp.toUpperCase().trim(),
      telefono: telefonoCompleto
    };
    
    console.log('📤 Enviando payload:', payload);
    
    const response = await apiService.createUser(payload);
    
    console.log('✅ Respuesta del servidor:', response);
    
    currentApiUrl.value = apiService.getCurrentApiUrl();
    
    showSuccessModal.value = true;
    
    setTimeout(() => {
      router.push('/login');
    }, 3000);
    
  } catch (error) {
    console.error('Error de registro:', error);
    
    if (error.response) {
      const status = error.response.status;
      if (status === 400) {
        const detail = error.response.data.detail || '';
        if (detail.includes('correo')) {
          message.text = 'El correo electrónico ya está registrado. Por favor, utiliza otro correo.';
        } else if (detail.includes('CURP')) {
          message.text = 'La CURP ya está registrada. Si ya tienes una cuenta, inicia sesión.';
        } else {
          message.text = detail || 'Los datos proporcionados son inválidos. Verifica la información.';
        }
      } else if (status === 500) {
        message.text = 'Error del servidor. Inténtalo de nuevo en unos minutos.';
      } else {
        message.text = error.response.data.detail || 'Error al crear la cuenta.';
      }
    } else if (error.request) {
      message.text = 'No se pudo conectar con el servidor. Verifica tu conexión a internet.';
    } else if (error.code === 'ECONNABORTED') {
      message.text = 'La conexión tardó demasiado. Verifica tu conexión a internet.';
    } else {
      message.text = 'Error al crear la cuenta: ' + error.message;
    }
    
    message.type = 'error';
  } finally {
    loading.value = false;
  }
}

function validateForm() {
  curpError.value = '';
  curpWarning.value = '';
  termsError.value = '';
  message.text = '';
  
  // Validación de términos y condiciones
  if (!termsAccepted.value) {
    termsError.value = 'Debes aceptar el Aviso de Privacidad para continuar';
    message.text = 'Debes aceptar el Aviso de Privacidad para continuar';
    message.type = 'error';
    return false;
  }

  // Validación de email obligatorio y formato
  if (!form.email || !form.email.trim()) {
    message.text = 'El correo electrónico es obligatorio';
    message.type = 'error';
    return false;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(form.email.trim())) {
    message.text = 'Por favor ingresa un correo electrónico válido';
    message.type = 'error';
    return false;
  }

  // Validación de nombre obligatorio
  if (!form.nombre || !form.nombre.trim()) {
    message.text = 'El nombre es obligatorio';
    message.type = 'error';
    return false;
  }

  // Validación de primer apellido obligatorio
  if (!form.primerApellido || !form.primerApellido.trim()) {
    message.text = 'El primer apellido es obligatorio';
    message.type = 'error';
    return false;
  }

  // Validación de segundo apellido obligatorio
  if (!form.segundoApellido || !form.segundoApellido.trim()) {
    message.text = 'El segundo apellido es obligatorio';
    message.type = 'error';
    return false;
  }

  // Validación de cargo obligatorio
  if (!form.cargo || !form.cargo.trim()) {
    message.text = 'El puesto de trabajo es obligatorio';
    message.type = 'error';
    return false;
  }

  // Validación de supervisor obligatorio
  if (!form.supervisor || !form.supervisor.trim()) {
    message.text = 'El supervisor inmediato es obligatorio. Debes ingresar el nombre de tu jefe directo';
    message.type = 'error';
    return false;
  }
  
  // Validación de CURP obligatoria
  if (!form.curp || !form.curp.trim()) {
    curpError.value = 'La CURP es obligatoria';
    message.text = 'La CURP es obligatoria';
    message.type = 'error';
    return false;
  }
  
  // Validación de teléfono obligatorio
  if (!form.telefono || !form.telefono.trim()) {
    message.text = 'El número de teléfono es obligatorio';
    message.type = 'error';
    return false;
  }
  
  if (!/^\d{10}$/.test(form.telefono.trim())) {
    message.text = 'El número de teléfono debe contener exactamente 10 dígitos';
    message.type = 'error';
    return false;
  }
  
  // Validación de formato CURP
  const curpClean = form.curp.toUpperCase().trim();
  if (curpClean.length !== 18) {
    curpError.value = 'La CURP debe contener exactamente 18 caracteres';
    message.text = 'La CURP debe contener exactamente 18 caracteres en mayúsculas';
    message.type = 'error';
    return false;
  }
  
  const curpRegex = /^[A-Z0-9]{18}$/;
  if (!curpRegex.test(curpClean)) {
    curpError.value = 'La CURP solo debe contener letras mayúsculas y números';
    message.text = 'La CURP debe contener solo letras mayúsculas y números';
    message.type = 'error';
    return false;
  }
  
  // Validación de contraseñas
  if (form.password !== form.confirmPassword) {
    message.text = 'Las contraseñas no coinciden';
    message.type = 'error';
    return false;
  }
  
  if (form.password.length < 6) {
    message.text = 'La contraseña debe tener al menos 6 caracteres';
    message.type = 'error';
    return false;
  }
  
  return true;
}

function formatCurp() {
  form.curp = form.curp.toUpperCase();
  
  if (curpError.value) {
    curpError.value = '';
  }
  if (curpWarning.value) {
    curpWarning.value = '';
  }
  if (termsError.value) {
    termsError.value = '';
  }
  
  if (form.curp.length > 0 && form.curp.length < 18) {
    curpError.value = `Faltan ${18 - form.curp.length} caracteres`;
  } else if (form.curp.length === 18) {
    const curpRegex = /^[A-Z0-9]{18}$/;
    if (!curpRegex.test(form.curp)) {
      curpError.value = 'La CURP solo debe contener letras mayúsculas y números';
    } else {
      curpError.value = '';
      curpWarning.value = 'CURP válida ✓';
    }
  }
}

function formatNombre() {
  form.nombre = form.nombre.toUpperCase();
}

function formatPrimerApellido() {
  form.primerApellido = form.primerApellido.toUpperCase();
}

function formatSegundoApellido() {
  form.segundoApellido = form.segundoApellido.toUpperCase();
}

function formatSupervisor() {
  form.supervisor = form.supervisor.toUpperCase();
}

function formatCargo() {
  form.cargo = form.cargo.toUpperCase();
}

function validatePhone() {
  form.telefono = form.telefono.replace(/\D/g, '');
  
  if (form.telefono.length > 10) {
    form.telefono = form.telefono.slice(0, 10);
  }
}

function selectCountry(pais) {
  form.codigoPais = pais.codigo;
  showCountrySelector.value = false;
}

function closeCountrySelector(e) {
  if (e.target.closest('button') && e.target.closest('button').contains(document.querySelector('svg')) || 
      e.target.closest('div') && e.target.closest('div').querySelector && e.target.closest('div').querySelector('input[placeholder="Buscar país..."]')) {
    return;
  }
  showCountrySelector.value = false;
}

function handleEscKey(event) {
  if (event.key === 'Escape' && showCountrySelector.value) {
    showCountrySelector.value = false;
  }
}

function clearTermsError() {
  if (termsError.value) {
    termsError.value = '';
  }
  if (message.text && message.text.includes('Aviso de Privacidad')) {
    message.text = '';
  }
}

function handleEnterKey(event) {
  if (!termsAccepted.value) {
    event.preventDefault();
    termsError.value = 'Debes aceptar el Aviso de Privacidad para continuar';
    message.text = 'Debes aceptar el Aviso de Privacidad para continuar';
    message.type = 'error';
  }
}

function goToLogin() {
  showSuccessModal.value = false;
  router.push('/login');
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
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

.glass-card-inner {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 4px 16px 0 rgba(31, 38, 135, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
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

.glass-title {
  color: #2e7d32;
  text-shadow: 
    0 1px 2px rgba(46, 125, 50, 0.3),
    0 0 8px rgba(46, 125, 50, 0.2);
  filter: drop-shadow(0 1px 1px rgba(255, 255, 255, 0.3));
  position: relative;
}

.glass-title::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.2) 0%, 
    rgba(255, 255, 255, 0.05) 50%,
    rgba(255, 255, 255, 0.2) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  z-index: 1;
  pointer-events: none;
}

/* Estilos específicos para los botones del ojo */
button[type="button"] {
  background: transparent !important;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  min-height: 32px;
  transition: all 0.2s ease;
  box-shadow: none !important;
}

button[type="button"]:focus {
  outline: none;
  background: transparent !important;
  box-shadow: none !important;
}

button[type="button"]:hover {
  background: transparent !important;
  box-shadow: none !important;
}

button[type="button"] svg {
  transition: all 0.2s ease;
}

button[type="button"]:hover svg {
  transform: scale(1.1);
}

/* Estilos para el scroll del aviso de privacidad */
.max-h-40.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.max-h-40.overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(241, 245, 249, 0.5);
  border-radius: 3px;
}

.max-h-40.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(203, 213, 225, 0.8);
  border-radius: 3px;
}

.max-h-40.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(148, 163, 184, 0.8);
}

/* Mejoras visuales para el checkbox */
input[type="checkbox"]:checked {
  background-color: #10b981;
  border-color: #10b981;
}

/* Animación de la barra de progreso */
@keyframes progress {
  0% { width: 0%; }
  100% { width: 100%; }
}

.animate-progress {
  animation: progress 3s linear forwards;
}

/* Nuevas animaciones para el modal de éxito */
.success-modal-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.9));
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 2px solid rgba(16, 185, 129, 0.2);
  box-shadow: 
    0 20px 40px rgba(16, 185, 129, 0.15),
    0 10px 20px rgba(0, 0, 0, 0.1),
    inset 0 1px 2px rgba(255, 255, 255, 0.8);
  position: relative;
  overflow: hidden;
}

.success-modal-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(16, 185, 129, 0.6), transparent);
  animation: scan 2s infinite;
}

@keyframes scan {
  0% { left: -100%; }
  100% { left: 100%; }
}

.success-button {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  font-weight: 600;
  border-radius: 12px;
  padding: 12px 24px;
  border: none;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
  min-width: 140px;
}

.success-button:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
}

.success-button:active {
  transform: translateY(0) scale(0.98);
}

.success-button:focus {
  outline: 2px solid #059669;
  outline-offset: 2px;
}

/* Animaciones específicas para el modal de éxito */
@keyframes bounce-in-success {
  0% {
    opacity: 0;
    transform: scale(0.3) translateY(-100px);
  }
  50% {
    opacity: 1;
    transform: scale(1.05) translateY(0);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes success-icon {
  0% {
    transform: scale(0) rotate(0deg);
    opacity: 0;
  }
  50% {
    transform: scale(1.2) rotate(180deg);
    opacity: 1;
  }
  100% {
    transform: scale(1) rotate(360deg);
    opacity: 1;
  }
}

@keyframes check-draw {
  0% {
    stroke-dasharray: 0 50;
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    stroke-dasharray: 50 0;
    opacity: 1;
  }
}

@keyframes slide-up {
  0% {
    opacity: 0;
    transform: translateY(30px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes progress-fill {
  0% {
    width: 0%;
  }
  100% {
    width: 100%;
  }
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

@keyframes confetti-fall {
  0% {
    transform: translateY(-100vh) rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: translateY(100vh) rotate(720deg);
    opacity: 0;
  }
}

/* Confeti animado */
.confetti-1, .confetti-2, .confetti-3, .confetti-4, .confetti-5, .confetti-6 {
  position: absolute;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  animation: confetti-fall 3s linear infinite;
}

.confetti-1 {
  background: #10b981;
  left: 10%;
  animation-delay: 0s;
  animation-duration: 2.5s;
}

.confetti-2 {
  background: #34d399;
  left: 20%;
  animation-delay: 0.3s;
  animation-duration: 3s;
}

.confetti-3 {
  background: #ffffff;
  left: 80%;
  animation-delay: 0.6s;
  animation-duration: 2.8s;
}

.confetti-4 {
  background: #059669;
  left: 90%;
  animation-delay: 0.9s;
  animation-duration: 3.2s;
}

.confetti-5 {
  background: #6ee7b7;
  left: 50%;
  animation-delay: 0.2s;
  animation-duration: 2.7s;
}

.confetti-6 {
  background: #d1fae5;
  left: 70%;
  animation-delay: 0.5s;
  animation-duration: 3.1s;
}

/* Clases de animación */
.animate-bounce-in {
  animation: bounce-in-success 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.animate-success-icon {
  animation: success-icon 1s ease-out 0.3s both;
}

.animate-check-draw {
  stroke-dasharray: 50;
  stroke-dashoffset: 50;
  animation: check-draw 0.8s ease-out 0.8s both;
}

.animate-slide-up {
  animation: slide-up 0.6s ease-out both;
}

.animate-progress-fill {
  animation: progress-fill 3s ease-out;
}

.animate-shimmer {
  animation: shimmer 2s ease-in-out infinite;
}

/* Transiciones del modal */
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-fade-enter-from {
  opacity: 0;
  backdrop-filter: blur(0px);
}

.modal-fade-leave-to {
  opacity: 0;
  backdrop-filter: blur(0px);
}

.modal-fade-enter-active .success-modal-card,
.modal-fade-leave-active .success-modal-card {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-fade-enter-from .success-modal-card {
  transform: scale(0.8) translateY(-100px);
  opacity: 0;
}

.modal-fade-leave-to .success-modal-card {
  transform: scale(0.8) translateY(100px);
  opacity: 0;
}

.uppercase {
  text-transform: uppercase;
}

.tracking-wide {
  letter-spacing: 0.025em;
}

/* Mejoras de responsividad para pantallas móviles */
@media (max-width: 480px) {
  .page-container {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }
  
  .glass-card {
    padding: 1rem;
    margin: 0 0.25rem;
  }
  
  .glass-input {
    font-size: 14px; /* Evita zoom en iOS */
    min-height: 36px;
  }
  
  .text-lg {
    font-size: 1rem;
  }
  
  .text-base {
    font-size: 0.875rem;
  }
  
  .w-64 {
    max-width: 75vw;
  }
  
  /* Responsividad específica para el modal de éxito */
  .success-modal-card {
    margin: 16px;
    max-width: calc(100vw - 32px);
    border-radius: 20px;
  }
  
  .success-modal-card .p-6 {
    padding: 20px;
  }
  
  .success-button {
    padding: 10px 20px;
    font-size: 14px;
    min-width: 120px;
  }
  
  .confetti-1, .confetti-2, .confetti-3, .confetti-4, .confetti-5, .confetti-6 {
    width: 4px;
    height: 4px;
  }
}

@media (max-height: 600px) {
  .page-container {
    max-width: 320px;
  }
  
  .text-center.mb-4 {
    margin-bottom: 0.75rem;
  }
  
  .glass-card {
    padding: 1rem;
  }
}

/* Para pantallas muy pequeñas como iPhone SE */
@media (max-width: 375px) and (max-height: 667px) {
  .page-container {
    max-width: 300px;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }
  
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
    max-width: 420px;
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
  
  .glass-card-inner {
    background: rgba(255, 255, 255, 0.7);
  }
  
  .success-modal-card {
    background: rgba(255, 255, 255, 0.95);
  }
}

/* Mejoras en accesibilidad */
@media (prefers-reduced-motion: reduce) {
  .animate-bounce-in,
  .animate-success-icon,
  .animate-check-draw,
  .animate-slide-up,
  .animate-progress-fill,
  .animate-shimmer,
  .confetti-1,
  .confetti-2,
  .confetti-3,
  .confetti-4,
  .confetti-5,
  .confetti-6 {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }
  
  .modal-fade-enter-active,
  .modal-fade-leave-active,
  .success-button {
    transition-duration: 0.01ms !important;
  }
}
</style>
