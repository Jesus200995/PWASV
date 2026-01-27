<template>
  <div class="fixed inset-0 bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 overflow-hidden" style="z-index: 0;">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-emerald-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-teal-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>

    <div class="absolute inset-0 overflow-y-auto pt-16 sm:pt-20 pb-3" style="z-index: 1;">
      <div class="page-container w-full max-w-sm mx-auto relative z-10 p-3 sm:p-4 lg:p-5">
      <!-- Header del perfil -->
      <div class="glass-card mb-2 relative overflow-hidden">
        <!-- Efecto de esquina doblada verde -->
        <div class="absolute top-0 left-0 w-12 h-12 bg-gradient-to-br from-green-700 to-green-600 transform -translate-x-1 -translate-y-1" style="clip-path: polygon(0 0, 100% 0, 0 100%);"></div>
        <div class="absolute top-0 left-0 w-12 h-12 bg-gradient-to-br from-green-500 to-green-400 transform -translate-x-0.5 -translate-y-0.5" style="clip-path: polygon(0 0, 100% 0, 0 100%);"></div>
        
        <div class="text-center mb-3">
          <div class="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-2 glass-avatar-outline border-2 border-green-500">
            <span class="text-2xl font-bold text-green-600">{{ getUserInitials() }}</span>
          </div>
          <h1 class="text-base font-bold text-gray-800 modern-title">{{ user.nombre_completo }}</h1>
          <div class="green-line mx-auto mb-2"></div>
          <p class="text-xs font-semibold text-white bg-green-600 py-0.5 px-2.5 rounded-full border-2 border-green-700 inline-block">{{ user.cargo }}</p>
        </div>
      </div>

      <!-- Información del usuario -->
      <div class="glass-card mb-2">
        <div class="flex justify-between items-center mb-3">
          <h2 class="text-base font-bold text-gray-800 modern-title flex items-center gap-2">
            <span class="inline-flex items-center justify-center w-4.5 h-4.5 rounded-full border-2 border-green-500 flex-shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-2.5 w-2.5 text-green-500" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
              </svg>
            </span>
            Información Personal
          </h2>
          <button @click="openEditModal" class="glass-edit-button">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
        </div>
        <div class="green-line mb-3"></div>
        
        <div class="space-y-1.5">
          <!-- Nombre Completo -->
          <div class="info-item-enhanced">
            <div class="flex items-center gap-2">
              <span class="icon-badge icon-user">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
                </svg>
              </span>
              <div class="flex-1">
                <p class="label-info">Nombre Completo</p>
                <p class="value-info value-name">{{ user.nombre_completo || 'No disponible' }}</p>
              </div>
            </div>
          </div>
          
          <!-- Email -->
          <div class="info-item-enhanced">
            <div class="flex items-center gap-2">
              <span class="icon-badge icon-email">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                </svg>
              </span>
              <div class="flex-1">
                <p class="label-info">Correo Electrónico</p>
                <p class="value-info value-email">{{ user.correo || user.email || 'No disponible' }}</p>
              </div>
            </div>
          </div>
          
          <!-- Cargo -->
          <div class="info-item-enhanced">
            <div class="flex items-center gap-2">
              <span class="icon-badge icon-position">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
              </span>
              <div class="flex-1">
                <p class="label-info">Puesto</p>
                <p class="value-info value-position">{{ user.cargo || 'No disponible' }}</p>
              </div>
            </div>
          </div>
          
          <!-- Supervisor -->
          <div class="info-item-enhanced">
            <div class="flex items-center gap-2">
              <span class="icon-badge icon-supervisor">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M16 11c1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3 1.34 3 3 3zm-8-8c1.66 0 3-1.34 3-3S9.66 0 8 0 5 1.34 5 3s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.89 1.97 1.5 1.97 2.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/>
                </svg>
              </span>
              <div class="flex-1">
                <p class="label-info">Supervisor</p>
                <p class="value-info value-supervisor">{{ (user.supervisor && user.supervisor.trim()) || 'No asignado' }}</p>
              </div>
            </div>
          </div>
          
          <!-- CURP -->
          <div class="info-item-enhanced">
            <div class="flex items-center gap-2">
              <span class="icon-badge icon-curp">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19 2H5c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-5 18H5v-2h9v2zm5-4H5V4h14v12z"/>
                  <path d="M7 9h2v2H7zm4 0h2v2h-2zm4 0h2v2h-2z"/>
                </svg>
              </span>
              <div class="flex-1">
                <p class="label-info">CURP</p>
                <p class="value-info value-curp font-mono">{{ (user.curp && user.curp.trim()) || 'No registrado' }}</p>
              </div>
            </div>
          </div>
          
          <!-- Teléfono -->
          <div class="info-item-enhanced">
            <div class="flex items-center gap-2">
              <span class="icon-badge icon-phone">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19.95 21c-1.05 0-2.08-.4-2.95-1.15C15.38 18.85 13.47 17 11.56 15.08 9.64 13.16 7.75 11.25 5.15 8.95 4.4 8.08 4 6.95 4 5.9c0-.95.4-1.95 1.15-2.95 1.2-1.55 2.35-1.95 3.2-1.95.55 0 1.15.15 1.55.55l2.35 2.35c.4.4.6.95.6 1.55 0 .55-.2 1.05-.55 1.5l-1 1c-.15.15-.25.35-.25.55v.1c.3.65.75 1.4 1.35 2.15.6.75 1.35 1.4 2.15 1.85.15.1.35.15.55.15h.1l1 -1c.45-.35.95-.55 1.5-.55.6 0 1.15.2 1.55.6l2.35 2.35c.4.4.55 1 .55 1.55 0 .85-.4 2-1.95 3.2C22.1 20.6 21.1 21 20.05 21z"/>
                </svg>
              </span>
              <div class="flex-1">
                <p class="label-info">Teléfono</p>
                <p class="value-info value-phone">{{ (user.telefono && user.telefono.trim()) || 'No registrado' }}</p>
              </div>
            </div>
          </div>
          
          <!-- Territorio -->
          <div class="info-item-enhanced">
            <div class="flex items-center gap-2">
              <span class="icon-badge icon-territorio">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                </svg>
              </span>
              <div class="flex-1">
                <p class="label-info">Territorio</p>
                <p class="value-info value-territorio">{{ user.territorio || 'No asignado' }}</p>
              </div>
            </div>
          </div>
          
          <!-- Fecha de registro -->
          <div v-if="user.fecha_registro" class="info-item-enhanced">
            <div class="flex items-center gap-2">
              <span class="icon-badge icon-date">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11z"/>
                </svg>
              </span>
              <div class="flex-1">
                <p class="label-info">Fecha de registro</p>
                <p class="value-info value-date">{{ formatDate(user.fecha_registro) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Cambio de contraseña -->
      <div class="glass-card">
        <h2 class="text-sm font-semibold text-gray-800 mb-2 modern-title flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
          </svg>
          Más Ajustes
        </h2>
        <div class="green-line mb-3"></div>
        <button 
          @click="openPasswordChangeModal"
          class="w-full relative overflow-hidden rounded-lg py-2.5 px-4 font-medium text-green-700 transition-all duration-300 hover:scale-105 active:scale-95"
          style="background: linear-gradient(135deg, rgba(220, 252, 231, 0.8) 0%, rgba(187, 247, 208, 0.6) 100%); border: 2px solid #16a34a;"
        >
          <span class="absolute inset-0 rounded-lg" style="border: 2px solid #16a34a; animation: neon-glow 3s ease-in-out infinite;"></span>
          <span class="relative flex items-center justify-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
            </svg>
            Cambiar Contraseña
          </span>
        </button>
      </div>

    <!-- Modal de cambio de contraseña -->
    <teleport to="body">
      <transition name="fade">
        <!-- Overlay con difuminación -->
        <div 
          v-if="showPasswordChangeModal" 
          class="fixed inset-0 bg-black/30 backdrop-blur-md z-40"
          @click="closePasswordChangeModal"
        ></div>
      </transition>
      
      <transition name="fade">
        <div v-if="showPasswordChangeModal" class="fixed inset-0 flex items-center justify-center p-3 pointer-events-none" style="z-index: 50;">
          <div class="rounded-2xl max-w-xs w-full mx-3 max-h-[85vh] overflow-y-auto edit-modal pointer-events-auto border-2 border-green-400" style="background: linear-gradient(135deg, rgba(240, 253, 244, 0.95) 0%, rgba(220, 252, 231, 0.95) 100%); backdrop-filter: blur(10px);">
            <div class="sticky top-0 rounded-t-2xl border-b-2 border-green-400 p-3" style="background: linear-gradient(135deg, rgba(240, 253, 244, 0.98) 0%, rgba(220, 252, 231, 0.98) 100%); backdrop-filter: blur(10px);">
              <div class="flex justify-between items-center">
                <h3 class="text-sm font-bold text-green-700 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                  Cambiar Contraseña
                </h3>
                <button @click="closePasswordChangeModal" class="w-7 h-7 rounded-full flex items-center justify-center transition-colors" style="background-color: rgba(134, 239, 172, 0.3); border: 1px solid rgba(52, 211, 153, 0.5);">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            <div class="p-3">
              <!-- Paso 1: Verificación de contraseña actual -->
              <div v-if="passwordChangeStep === 1">
                <p class="text-xs text-gray-600 mb-3">Primero, verifica tu contraseña actual para continuar.</p>
                <form @submit.prevent="verifyCurrentPassword" class="space-y-3">
                  <div v-if="passwordErrors.general" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-2 rounded-lg" role="alert">
                    <p class="text-xs">{{ passwordErrors.general }}</p>
                  </div>

                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-1">Contraseña Actual</label>
                    <div class="relative">
                      <input
                        v-model="passwordChangeForm.currentPassword"
                        :type="showCurrentPassword ? 'text' : 'password'"
                        class="glass-input w-full pr-10"
                        placeholder="Ingresa tu contraseña actual"
                        required
                      />
                      <button
                        type="button"
                        @click="showCurrentPassword = !showCurrentPassword"
                        class="absolute right-3 top-2.5 text-gray-500 hover:text-gray-700"
                      >
                        <svg v-if="!showCurrentPassword" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-2.391m5.005-2.905A9.005 9.005 0 0112 5c4.478 0 8.268 2.943 9.543 7a9.974 9.974 0 01-1.564 2.391m0 0A9.005 9.005 0 0112 19" />
                        </svg>
                      </button>
                    </div>
                  </div>

                  <button
                    type="submit"
                    :disabled="isVerifyingPassword"
                    class="glass-button w-full"
                    :class="{ 'opacity-50 cursor-not-allowed': isVerifyingPassword }"
                  >
                    {{ isVerifyingPassword ? 'Verificando...' : 'Verificar' }}
                  </button>
                </form>
              </div>

              <!-- Paso 2: Cambio de contraseña -->
              <div v-if="passwordChangeStep === 2">
                <p class="text-xs text-gray-600 mb-3">Ahora ingresa tu nueva contraseña dos veces.</p>
                <form @submit.prevent="changePasswordNow" class="space-y-3">
                  <div v-if="passwordErrors.general" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-2 rounded-lg" role="alert">
                    <p class="text-xs">{{ passwordErrors.general }}</p>
                  </div>

                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-1">Nueva Contraseña</label>
                    <div class="relative">
                      <input
                        v-model="passwordChangeForm.newPassword"
                        :type="showNewPassword ? 'text' : 'password'"
                        class="glass-input w-full pr-10"
                        :class="{ 'border-red-500': passwordErrors.newPassword }"
                        placeholder="Ingresa tu nueva contraseña"
                        required
                      />
                      <button
                        type="button"
                        @click="showNewPassword = !showNewPassword"
                        class="absolute right-3 top-2.5 text-gray-500 hover:text-gray-700"
                      >
                        <svg v-if="!showNewPassword" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-2.391m5.005-2.905A9.005 9.005 0 0112 5c4.478 0 8.268 2.943 9.543 7a9.974 9.974 0 01-1.564 2.391m0 0A9.005 9.005 0 0112 19" />
                        </svg>
                      </button>
                    </div>
                    <p v-if="passwordErrors.newPassword" class="text-red-500 text-xs mt-1">{{ passwordErrors.newPassword }}</p>
                  </div>

                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-1">Confirmar Contraseña</label>
                    <div class="relative">
                      <input
                        v-model="passwordChangeForm.confirmPassword"
                        :type="showConfirmPassword ? 'text' : 'password'"
                        class="glass-input w-full pr-10"
                        :class="{ 'border-red-500': passwordErrors.confirmPassword }"
                        placeholder="Confirma tu nueva contraseña"
                        required
                      />
                      <button
                        type="button"
                        @click="showConfirmPassword = !showConfirmPassword"
                        class="absolute right-3 top-2.5 text-gray-500 hover:text-gray-700"
                      >
                        <svg v-if="!showConfirmPassword" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-2.391m5.005-2.905A9.005 9.005 0 0112 5c4.478 0 8.268 2.943 9.543 7a9.974 9.974 0 01-1.564 2.391m0 0A9.005 9.005 0 0112 19" />
                        </svg>
                      </button>
                    </div>
                    <p v-if="passwordErrors.confirmPassword" class="text-red-500 text-xs mt-1">{{ passwordErrors.confirmPassword }}</p>
                  </div>

                  <div class="flex gap-2">
                    <button
                      type="button"
                      @click="passwordChangeStep = 1"
                      class="glass-button-secondary w-full"
                    >
                      Atrás
                    </button>
                    <button
                      type="submit"
                      :disabled="isChangingPassword"
                      class="glass-button w-full"
                      :class="{ 'opacity-50 cursor-not-allowed': isChangingPassword }"
                    >
                      {{ isChangingPassword ? 'Guardando...' : 'Guardar Cambios' }}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </teleport>

    <!-- Modal antiguo: Modal de confirmación -->
    <transition name="fade">
      <div v-if="showSuccessModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-3" style="z-index: 60;">
        <div class="glass-card max-w-xs w-full mx-3">
          <div class="text-center">
            <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3 glass-success-icon">
              <svg class="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <h3 class="text-base font-semibold text-gray-900 mb-2 modern-title">¡Contraseña cambiada!</h3>
            <div class="green-line mx-auto mb-2"></div>
            <p class="text-xs text-gray-600 mb-3">Tu contraseña ha sido actualizada exitosamente.</p>
            <button @click="showSuccessModal = false" class="glass-button w-full">
              Entendido
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Modal de edición de información personal -->
    <teleport to="body">
      <transition name="fade">
        <!-- Overlay con difuminación -->
        <div 
          v-if="showEditModal" 
          class="fixed inset-0 bg-black/30 backdrop-blur-md z-40"
          @click="closeEditModal"
        ></div>
      </transition>
      
      <transition name="fade">
        <div v-if="showEditModal" class="fixed inset-0 flex items-center justify-center p-3 pointer-events-none" style="z-index: 50;">
          <div class="rounded-2xl max-w-xs w-full mx-3 max-h-[85vh] overflow-y-auto edit-modal pointer-events-auto border-2 border-green-400" style="background: linear-gradient(135deg, rgba(240, 253, 244, 0.95) 0%, rgba(220, 252, 231, 0.95) 100%); backdrop-filter: blur(10px);">
          <div class="sticky top-0 rounded-t-2xl border-b-2 border-green-400 p-3" style="background: linear-gradient(135deg, rgba(240, 253, 244, 0.98) 0%, rgba(220, 252, 231, 0.98) 100%); backdrop-filter: blur(10px);">
            <div class="flex justify-between items-center">
              <h3 class="text-sm font-bold text-green-700 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Editar Información
              </h3>
              <button @click="closeEditModal" class="w-7 h-7 rounded-full flex items-center justify-center transition-colors" style="background-color: rgba(134, 239, 172, 0.3); border: 1px solid rgba(52, 211, 153, 0.5);">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          
          <div class="p-3">
            <form @submit.prevent="updateUserInfo" class="space-y-3">
              <!-- Mensaje de error general -->
              <div v-if="editErrors.general" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-2 rounded-lg" role="alert">
                <p class="text-xs">{{ editErrors.general }}</p>
              </div>

              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">Nombre completo</label>
                <input
                  v-model="editForm.nombre_completo"
                  type="text"
                  class="edit-input-small w-full"
                  :class="{ 'border-red-500': editErrors.nombre_completo }"
                  placeholder="Ingresa tu nombre completo"
                  @input="editForm.nombre_completo = editForm.nombre_completo.toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')"
                  required
                />
                <p v-if="editErrors.nombre_completo" class="text-red-500 text-xs mt-1">{{ editErrors.nombre_completo }}</p>
              </div>

              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">Email</label>
                <input
                  v-model="editForm.correo"
                  type="email"
                  class="edit-input-small w-full"
                  :class="{ 'border-red-500': editErrors.correo }"
                  placeholder="Ingresa tu email"
                  required
                />
                <p v-if="editErrors.correo" class="text-red-500 text-xs mt-1">{{ editErrors.correo }}</p>
              </div>

              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">Cargo</label>
                <select
                  v-model="editForm.cargo"
                  class="edit-input-small w-full"
                  :class="{ 'border-red-500': editErrors.cargo }"
                  required
                >
                  <option value="" disabled>-- Selecciona tu cargo --</option>
                  <option v-for="cargo in cargosDisponibles" :key="cargo" :value="cargo">
                    {{ cargo }}
                  </option>
                </select>
                <p v-if="editErrors.cargo" class="text-red-500 text-xs mt-1">{{ editErrors.cargo }}</p>
              </div>

              <!-- Campo para cargo personalizado si selecciona OTRO -->
              <div v-if="editForm.cargo === 'OTRO'">
                <label class="block text-xs font-medium text-gray-700 mb-1">Especifica tu cargo</label>
                <input
                  v-model="editForm.cargoOtro"
                  type="text"
                  class="edit-input-small w-full"
                  :class="{ 'border-red-500': editErrors.cargoOtro }"
                  placeholder="Escribe tu cargo"
                  @input="editForm.cargoOtro = editForm.cargoOtro.toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')"
                  required
                />
                <p v-if="editErrors.cargoOtro" class="text-red-500 text-xs mt-1">{{ editErrors.cargoOtro }}</p>
              </div>

              <!-- Territorio (arriba de supervisor para técnicos) -->
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">
                  Territorio de Sembrando Vida
                  <span v-if="esTecnico" class="text-blue-600 text-xs font-normal ml-1">(Define tu supervisor)</span>
                </label>
                <select
                  v-model="editForm.territorio"
                  class="edit-input-small w-full"
                  :class="{ 'border-blue-400 ring-1 ring-blue-200': esTecnico }"
                >
                  <option value="">-- Selecciona un territorio --</option>
                  <option v-for="territorio in territoriosSembrandoVida" :key="territorio" :value="territorio">{{ territorio }}</option>
                </select>
                <p v-if="esTecnico" class="text-xs text-blue-600 mt-1">
                  <svg class="inline w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  Al cambiar territorio, tu supervisor se actualizará automáticamente
                </p>
              </div>

              <!-- Supervisor (para técnicos es automático y readonly) -->
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">
                  Supervisor
                  <span v-if="esTecnico && !buscandoSupervisor" class="text-green-600 text-xs font-normal ml-1">(Automático)</span>
                  <span v-if="buscandoSupervisor" class="text-orange-500 text-xs font-normal ml-1 animate-pulse">(Buscando...)</span>
                </label>
                <div class="relative">
                  <input
                    v-model="editForm.supervisor"
                    type="text"
                    class="edit-input-small w-full pr-8"
                    :style="esTecnico && !buscandoSupervisor ? 'background-color: #d1d5db !important; color: #1f2937; border-color: #9ca3af;' : (buscandoSupervisor ? 'background-color: #fff7ed; border-color: #fdba74;' : '')"
                    :class="{ 'cursor-not-allowed font-medium': esTecnico && !buscandoSupervisor }"
                    :placeholder="esTecnico ? 'Se asigna según territorio' : 'Ingresa el nombre de tu supervisor'"
                    :readonly="esTecnico"
                    @input="!esTecnico && (editForm.supervisor = editForm.supervisor.toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''))"
                  />
                  <!-- Icono de candado para técnicos -->
                  <div v-if="esTecnico && !buscandoSupervisor" class="absolute right-2 top-1/2 -translate-y-1/2">
                    <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                    </svg>
                  </div>
                  <!-- Spinner de carga -->
                  <div v-if="buscandoSupervisor" class="absolute right-2 top-1/2 -translate-y-1/2">
                    <svg class="animate-spin w-4 h-4 text-orange-500" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  </div>
                </div>
                <p v-if="esTecnico && !buscandoSupervisor" class="text-xs text-gray-500 mt-1">
                  <svg class="inline w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  El supervisor territorial se asigna automáticamente
                </p>
              </div>

              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">CURP</label>
                <input
                  v-model="editForm.curp"
                  type="text"
                  class="edit-input-small w-full"
                  :class="{ 'border-red-500': editErrors.curp }"
                  placeholder="Ingresa tu CURP"
                  maxlength="18"
                  @input="editForm.curp = editForm.curp.toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')"
                />
                <p v-if="editErrors.curp" class="text-red-500 text-xs mt-1">{{ editErrors.curp }}</p>
              </div>

              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">Teléfono</label>
                <div class="flex space-x-2">
                  <!-- Selector de código de país -->
                  <div class="relative">
                    <button 
                      type="button"
                      @click="showCountrySelector = !showCountrySelector"
                      class="edit-input-small flex items-center px-2 py-1 min-w-[70px] justify-between text-xs"
                    >
                      <div class="flex items-center">
                        <span class="text-xs mr-1">{{ paises.find(p => p.codigo === editForm.codigoPais)?.bandera || '🌎' }}</span>
                        <span class="text-xs font-medium">{{ editForm.codigoPais }}</span>
                      </div>
                      <svg class="w-2 h-2 ml-1 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                      </svg>
                    </button>
                    
                    <!-- Dropdown para selección de país -->
                    <div 
                      v-if="showCountrySelector" 
                      class="absolute z-50 w-56 top-full left-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-xl overflow-hidden"
                    >
                      <!-- Barra de búsqueda -->
                      <div class="sticky top-0 bg-white p-2 border-b border-gray-200">
                        <input 
                          type="text"
                          v-model="countrySearch"
                          placeholder="Buscar país..."
                          class="w-full px-2 py-1 border border-gray-300 rounded text-xs focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                          @click="$event.stopPropagation()"
                        />
                      </div>
                      
                      <ul class="py-1 max-h-40 overflow-y-auto">
                        <li 
                          v-for="pais in filteredCountries" 
                          :key="pais.codigo"
                          @click="selectCountry(pais)"
                          class="flex items-center px-2 py-1 hover:bg-gray-100 cursor-pointer transition-colors"
                        >
                          <span class="text-xs mr-2">{{ pais.bandera }}</span>
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
                      v-model="editForm.telefonoDigitos"
                      type="tel"
                      class="edit-input-small w-full"
                      placeholder="10 dígitos"
                      maxlength="10"
                      @input="validatePhoneEdit"
                    />
                  </div>
                </div>
                <p class="mt-1 text-xs text-gray-500">Ingresa solo los 10 dígitos de tu número (sin lada)</p>
              </div>

              <div class="flex space-x-2 pt-3">
                <button
                  type="button"
                  @click="closeEditModal"
                  class="flex-1 px-3 py-1.5 border border-gray-300 rounded-lg text-gray-700 bg-white hover:bg-gray-50 text-xs font-medium transition-colors"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  :disabled="isUpdatingUser"
                  class="flex-1 px-3 py-1.5 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg text-xs font-medium hover:from-green-600 hover:to-green-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                >
                  <svg v-if="isUpdatingUser" class="animate-spin h-3 w-3 mr-2" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ isUpdatingUser ? 'Guardando...' : 'Guardar Cambios' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
      </transition>
    </teleport>

    <!-- Modal de éxito para edición -->
    <transition name="fade">
      <div v-if="showEditSuccessModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-3" style="z-index: 70;">
        <div class="bg-white rounded-2xl max-w-xs w-full mx-3 p-6 text-center">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
          <h3 class="text-lg font-bold text-gray-900 mb-2">¡Información actualizada!</h3>
          <p class="text-sm text-gray-600 mb-4">Tus datos personales han sido actualizados correctamente.</p>
          <button @click="showEditSuccessModal = false" class="w-full px-4 py-2 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg font-medium hover:from-green-600 hover:to-green-700 transition-all">
            Entendido
          </button>
        </div>
      </div>
    </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import { API_URL, checkInternetConnection, getOfflineMessage } from '../utils/network.js'
import { apiService } from '../services/apiService.js'

const user = ref({})
const passwordForm = ref({
  newPassword: '',
  confirmPassword: ''
})
const errors = ref({})
const isChangingPassword = ref(false)
const showSuccessModal = ref(false)

// Variables para cambio de contraseña en modal
const showPasswordChangeModal = ref(false)
const passwordChangeStep = ref(1)
const passwordChangeForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const passwordErrors = ref({})
const isVerifyingPassword = ref(false)
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)

// Variables reactivas para edición de información personal
const showEditModal = ref(false)
const showEditSuccessModal = ref(false)
const isUpdatingUser = ref(false)
const buscandoSupervisor = ref(false)
const editErrors = ref({})
const editForm = ref({
  nombre_completo: '',
  correo: '',
  cargo: '',
  cargoOtro: '',
  supervisor: '',
  curp: '',
  telefono: '',
  codigoPais: '+52',
  telefonoDigitos: '',
  territorio: ''
})

// Lista de cargos disponibles
const cargosDisponibles = [
  'TECNICO PRODUCTIVO',
  'TECNICO SOCIAL',
  'FACILITADOR COMUNITARIO',
  'COORDINACION TERRITORIAL C',
  'COORDINACION TERRITORIAL B',
  'COORDINACION TERRITORIAL A',
  'ESPECIALISTAS PRODUCTIVOS Y SOCIALES',
  'SEMBRADOR',
  'OTRO'
]

// Lista de territorios de Sembrando Vida para el selector
const territoriosSembrandoVida = [
  'Acapulco - Centro - Norte - Tierra Caliente',
  'Acayucan',
  'Balancán',
  'Chihuahua / Sonora',
  'Colima',
  'Comalcalco',
  'Córdoba',
  'Costa Chica - Montaña',
  'Costa Grande - Sierra',
  'Durango / Zacatecas',
  'Hidalgo',
  'Istmo',
  'Michoacán',
  'Mixteca',
  'Morelos',
  'Nayarit / Jalisco',
  'Ocosingo',
  'Palenque',
  'Papantla',
  'Pichucalco',
  'Puebla',
  'San Luis Potosí',
  'Sinaloa',
  'Tamaulipas',
  'Tantoyuca',
  'Tapachula',
  'Teapa',
  'Tlaxcala / Estado de México',
  'Tzucacab / Opb',
  'Xpujil',
  'Oficinas Centrales'
]

// Computed para saber si el usuario es técnico (su supervisor es automático)
const esTecnico = computed(() => {
  const cargo = (editForm.value.cargo || '').toUpperCase()
  return cargo === 'TECNICO SOCIAL' || cargo === 'TECNICO PRODUCTIVO'
})

// Función para buscar supervisor territorial por territorio
const buscarSupervisorPorTerritorio = async (territorio) => {
  if (!territorio || !user.value.id) return null
  
  buscandoSupervisor.value = true
  editForm.value.supervisor = 'Buscando...'
  
  try {
    // Necesitamos un endpoint que busque por territorio directamente
    // Mientras tanto, usamos el endpoint existente pero primero actualizamos el territorio temporalmente
    const respuesta = await apiService.obtenerSupervisorTerritorio(territorio)
    
    if (respuesta.success && respuesta.supervisor) {
      editForm.value.supervisor = respuesta.supervisor
      
      // Actualizar también el user.value para que se refleje en Profile
      user.value.supervisor = respuesta.supervisor
      
      // Actualizar localStorage
      const storedUser = JSON.parse(localStorage.getItem('user'))
      storedUser.supervisor = respuesta.supervisor
      localStorage.setItem('user', JSON.stringify(storedUser))
      
      console.log(`✅ Supervisor actualizado: ${respuesta.supervisor}`)
      return respuesta.supervisor
    } else {
      editForm.value.supervisor = 'No hay supervisor asignado'
      console.log(`ℹ️ No se encontró supervisor para: ${territorio}`)
      return null
    }
  } catch (error) {
    console.error('❌ Error buscando supervisor:', error)
    editForm.value.supervisor = 'Error al buscar'
    return null
  } finally {
    buscandoSupervisor.value = false
  }
}

// Watch para actualizar el supervisor automáticamente cuando cambie el territorio (solo para técnicos)
watch(() => editForm.value.territorio, async (nuevoTerritorio, viejoTerritorio) => {
  // Solo si cambió el territorio y es técnico
  if (nuevoTerritorio && nuevoTerritorio !== viejoTerritorio && esTecnico.value) {
    console.log('🔄 Territorio cambió, buscando nuevo supervisor...')
    await buscarSupervisorPorTerritorio(nuevoTerritorio)
  }
})

// Watch para cuando cambie el cargo
watch(() => editForm.value.cargo, async (nuevoCargo, viejoCargo) => {
  if (nuevoCargo !== viejoCargo) {
    const cargoUpper = (nuevoCargo || '').toUpperCase()
    const esNuevoTecnico = cargoUpper === 'TECNICO SOCIAL' || cargoUpper === 'TECNICO PRODUCTIVO'
    
    if (esNuevoTecnico && editForm.value.territorio) {
      // Si ahora es técnico, buscar supervisor automático
      await buscarSupervisorPorTerritorio(editForm.value.territorio)
    }
  }
})

// Variables para selector de país
const showCountrySelector = ref(false)
const countrySearch = ref('')

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
]

// Filtro de países basado en la búsqueda
const filteredCountries = computed(() => {
  if (!countrySearch.value) return paises
  
  const searchTerm = countrySearch.value.toLowerCase()
  return paises.filter(pais => 
    pais.nombre.toLowerCase().includes(searchTerm) || 
    pais.codigo.includes(searchTerm)
  )
})

// Función para obtener las iniciales del usuario
const getUserInitials = () => {
  if (!user.value.nombre_completo) return 'U'
  
  const nombres = user.value.nombre_completo.trim().split(' ')
  const iniciales = nombres
    .map(nombre => nombre.charAt(0).toUpperCase())
    .slice(0, 2)
    .join('')
  
  return iniciales || 'U'
}

onMounted(() => {
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    user.value = JSON.parse(storedUser)
    
    // Cargar los datos completos del usuario desde el backend
    loadUserData()
  }

  // Event listeners para cerrar el selector de país
  document.addEventListener('click', closeCountrySelector)
  document.addEventListener('keydown', handleEscKey)
})

// Función para cerrar el selector de país al hacer clic fuera
const closeCountrySelector = (e) => {
  if (e.target.closest('button') && e.target.closest('button').contains(document.querySelector('svg')) || 
      e.target.closest('div') && e.target.closest('div').querySelector && e.target.closest('div').querySelector('input[placeholder="Buscar país..."]')) {
    return
  }
  showCountrySelector.value = false
}

// Función para cerrar con tecla Escape
const handleEscKey = (event) => {
  if (event.key === 'Escape' && showCountrySelector.value) {
    showCountrySelector.value = false
  }
}

const loadUserData = async () => {
  try {
    console.log('🔍 Cargando datos del usuario ID:', user.value.id)
    console.log('📋 Datos iniciales del user:', user.value)
    
    const online = await checkInternetConnection()
    if (!online) {
      console.log('❌ Sin conexión, usando datos del localStorage')
      return
    }
    
    console.log('🌐 Haciendo petición a:', `${API_URL}/usuarios/${user.value.id}`)
    
    const response = await axios.get(`${API_URL}/usuarios/${user.value.id}`, {
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    console.log('📡 Respuesta status:', response.status)
    
    if (response.status === 200) {
      const userData = response.data
      console.log('📊 Datos RAW del backend:', userData)
      console.log('👀 Supervisor:', userData.supervisor)
      console.log('� CURP:', userData.curp)
      console.log('👀 Teléfono:', userData.telefono)
      
      // No incluir la contraseña para seguridad
      delete userData.contrasena
      
      // Actualizar los datos del usuario
      user.value = {
        ...user.value,
        ...userData
      }
      
      console.log('✅ Datos del usuario FINALES:', user.value)
      console.log('🔎 user.supervisor final:', user.value.supervisor)
      console.log('🔎 user.curp final:', user.value.curp)
      console.log('🔎 user.telefono final:', user.value.telefono)
      
      // Actualizar también el localStorage con los datos completos
      localStorage.setItem('user', JSON.stringify(user.value))
      
      console.log('✅ Datos del usuario actualizados desde el backend')
    }
  } catch (error) {
    console.error('❌ Error al cargar datos completos del usuario:', error)
    if (error.response) {
      console.error('📡 Error response:', error.response.status, error.response.data)
    } else if (error.request) {
      console.error('📡 Error request:', error.request)
    } else {
      console.error('📡 Error message:', error.message)
    }
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'No disponible'
  try {
    // Si viene una fecha ISO completa (con T), la procesamos
    if (typeof dateString === 'string' && dateString.includes('T')) {
      return new Date(dateString).toLocaleDateString('es-ES', {
        timeZone: 'America/Mexico_City', // Forzar zona horaria de México
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    // Si viene solo una fecha (YYYY-MM-DD), crear la fecha sin zona horaria
    if (typeof dateString === 'string' && dateString.match(/^\d{4}-\d{2}-\d{2}$/)) {
      const [year, month, day] = dateString.split('-').map(num => parseInt(num, 10))
      const fecha = new Date(year, month - 1, day) // month - 1 porque los meses en JS van de 0-11
      
      return fecha.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    // Para otros casos, usar el método estándar
    return new Date(dateString).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch (e) {
    console.error('Error al formatear fecha:', e, 'Fecha original:', dateString)
    return 'No disponible'
  }
}

const validateForm = () => {
  errors.value = {}
  
  if (passwordForm.value.newPassword.length < 6) {
    errors.value.newPassword = 'La nueva contraseña debe tener al menos 6 caracteres'
  }
  
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    errors.value.confirmPassword = 'Las contraseñas no coinciden'
  }
  
  return Object.keys(errors.value).length === 0
}

const changePassword = async () => {
  if (!validateForm()) return
  
  isChangingPassword.value = true
  errors.value = {}
  
  try {
    // Verificar conexión a internet
    const online = await checkInternetConnection()
    if (!online) {
      errors.value.general = getOfflineMessage()
      return
    }
    
    // Llamada a la API para cambiar contraseña
    const response = await axios.post(`${API_URL}/cambiar_contrasena`, {
      usuario_id: user.value.id,
      nueva_contrasena: passwordForm.value.newPassword
    }, {
      timeout: 10000, // 10 segundos de timeout
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    // Verificar respuesta exitosa
    if (response.status === 200) {
      // Limpiar el formulario
      passwordForm.value = {
        newPassword: '',
        confirmPassword: ''
      }
      
      // Mostrar modal de éxito
      showSuccessModal.value = true
    }
    
  } catch (error) {
    console.error('Error al cambiar contraseña:', error)
    
    if (error.response) {
      // El servidor respondió con un estado de error
      const errorMsg = error.response.data?.detail || 
                      error.response.data?.message || 
                      'Error al cambiar la contraseña'
      errors.value.general = errorMsg
    } else if (error.request) {
      // La solicitud fue hecha pero no se recibió respuesta
      errors.value.general = 'No se pudo conectar con el servidor. Verifica tu conexión.'
    } else {
      // Algo ocurrió al configurar la solicitud
      errors.value.general = 'Error al cambiar la contraseña: ' + error.message
    }
  } finally {
    isChangingPassword.value = false
  }
}

// ==================== FUNCIONES PARA MODAL DE CAMBIO DE CONTRASEÑA ====================

const openPasswordChangeModal = () => {
  showPasswordChangeModal.value = true
  passwordChangeStep.value = 1
  passwordChangeForm.value = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
  passwordErrors.value = {}
  showCurrentPassword.value = false
  showNewPassword.value = false
  showConfirmPassword.value = false
}

const closePasswordChangeModal = () => {
  showPasswordChangeModal.value = false
  passwordChangeStep.value = 1
  passwordChangeForm.value = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
  passwordErrors.value = {}
}

const verifyCurrentPassword = async () => {
  passwordErrors.value = {}
  
  if (!passwordChangeForm.value.currentPassword.trim()) {
    passwordErrors.value.general = 'Ingresa tu contraseña actual'
    return
  }
  
  isVerifyingPassword.value = true
  
  try {
    // Verificar conexión a internet
    const online = await checkInternetConnection()
    if (!online) {
      passwordErrors.value.general = getOfflineMessage()
      return
    }
    
    // Verificar contraseña actual (endpoint simple para verificación)
    const response = await axios.post(`${API_URL}/verificar_contrasena`, {
      usuario_id: user.value.id,
      contrasena: passwordChangeForm.value.currentPassword
    }, {
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    if (response.status === 200 && response.data.success) {
      // Contraseña verificada, pasar al paso 2
      passwordChangeStep.value = 2
    } else {
      passwordErrors.value.general = 'Contraseña incorrecta'
    }
    
  } catch (error) {
    console.error('Error verificando contraseña:', error)
    
    if (error.response?.status === 401) {
      passwordErrors.value.general = 'Contraseña incorrecta'
    } else if (error.response?.status === 404) {
      passwordErrors.value.general = 'Usuario no encontrado'
    } else if (error.code === 'ERR_NETWORK' || !error.response) {
      passwordErrors.value.general = 'No se pudo conectar con el servidor'
    } else {
      passwordErrors.value.general = 'Error al verificar la contraseña'
    }
  } finally {
    isVerifyingPassword.value = false
  }
}

const changePasswordNow = async () => {
  passwordErrors.value = {}
  
  // Validaciones
  if (!passwordChangeForm.value.newPassword.trim()) {
    passwordErrors.value.newPassword = 'Ingresa una nueva contraseña'
    return
  }
  
  if (passwordChangeForm.value.newPassword.length < 6) {
    passwordErrors.value.newPassword = 'La contraseña debe tener al menos 6 caracteres'
    return
  }
  
  if (!passwordChangeForm.value.confirmPassword.trim()) {
    passwordErrors.value.confirmPassword = 'Confirma tu nueva contraseña'
    return
  }
  
  if (passwordChangeForm.value.newPassword !== passwordChangeForm.value.confirmPassword) {
    passwordErrors.value.confirmPassword = 'Las contraseñas no coinciden'
    return
  }
  
  isChangingPassword.value = true
  
  try {
    // Verificar conexión a internet
    const online = await checkInternetConnection()
    if (!online) {
      passwordErrors.value.general = getOfflineMessage()
      return
    }
    
    // Cambiar contraseña
    const response = await axios.post(`${API_URL}/cambiar_contrasena`, {
      usuario_id: user.value.id,
      nueva_contrasena: passwordChangeForm.value.newPassword
    }, {
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    })
    
    if (response.status === 200 && response.data.success) {
      // Éxito
      closePasswordChangeModal()
      showSuccessModal.value = true
      
      // Limpiar formulario antiguo
      passwordForm.value = {
        newPassword: '',
        confirmPassword: ''
      }
    }
    
  } catch (error) {
    console.error('Error al cambiar contraseña:', error)
    
    if (error.response?.status === 400) {
      passwordErrors.value.general = error.response.data?.detail || 'Error al cambiar la contraseña'
    } else if (error.code === 'ERR_NETWORK' || !error.response) {
      passwordErrors.value.general = 'No se pudo conectar con el servidor'
    } else {
      passwordErrors.value.general = 'Error al cambiar la contraseña'
    }
  } finally {
    isChangingPassword.value = false
  }
}

// Función para abrir el modal de edición
const openEditModal = () => {
  // Extraer código de país y dígitos del teléfono actual
  let codigoPais = '+52'
  let telefonoDigitos = ''
  
  if (user.value.telefono) {
    const telefonoCompleto = user.value.telefono.toString()
    // Buscar coincidencia con códigos de país conocidos
    const paisEncontrado = paises.find(pais => telefonoCompleto.startsWith(pais.codigo))
    if (paisEncontrado) {
      codigoPais = paisEncontrado.codigo
      telefonoDigitos = telefonoCompleto.slice(paisEncontrado.codigo.length)
    } else {
      // Si no encuentra coincidencia, asumir que es completo sin código
      telefonoDigitos = telefonoCompleto
    }
  }
  
  // Cargar los datos actuales en el formulario
  editForm.value = {
    nombre_completo: user.value.nombre_completo || '',
    correo: user.value.correo || '',
    cargo: user.value.cargo || '',
    supervisor: user.value.supervisor || '',
    curp: user.value.curp || '',
    telefono: user.value.telefono || '',
    codigoPais: codigoPais,
    telefonoDigitos: telefonoDigitos,
    territorio: user.value.territorio || ''
  }
  
  // Resetear errores
  editErrors.value = {}
  
  showEditModal.value = true
}

// Función para cerrar el modal de edición
const closeEditModal = () => {
  showEditModal.value = false
  showCountrySelector.value = false
  countrySearch.value = ''
  editForm.value = {
    nombre_completo: '',
    correo: '',
    cargo: '',
    supervisor: '',
    curp: '',
    telefono: '',
    codigoPais: '+52',
    telefonoDigitos: '',
    territorio: ''
  }
  editErrors.value = {}
}

// Función para actualizar la información del usuario
const updateUserInfo = async () => {
  try {
    console.log('Iniciando actualización de información personal...')
    
    // Resetear errores
    editErrors.value = {}
    
    // Validaciones
    if (!editForm.value.nombre_completo?.trim()) {
      editErrors.value.nombre_completo = 'El nombre completo es obligatorio'
      return
    }
    
    if (!editForm.value.correo?.trim()) {
      editErrors.value.correo = 'El email es obligatorio'
      return
    }
    
    // Validar formato de email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(editForm.value.correo)) {
      editErrors.value.correo = 'El formato del email no es válido'
      return
    }
    
    if (!editForm.value.cargo?.trim()) {
      editErrors.value.cargo = 'El cargo es obligatorio'
      return
    }
    
    // Validar cargoOtro si seleccionó OTRO
    if (editForm.value.cargo === 'OTRO' && !editForm.value.cargoOtro?.trim()) {
      editErrors.value.cargoOtro = 'Debes especificar tu cargo'
      return
    }
    
    // Validar CURP si se proporciona
    if (editForm.value.curp && editForm.value.curp.trim().length > 0) {
      const curpTrimmed = editForm.value.curp.trim().toUpperCase()
      
      // Validar formato: 18 caracteres alfanuméricos
      if (curpTrimmed.length !== 18) {
        editErrors.value.curp = 'El CURP debe tener exactamente 18 caracteres'
        return
      }
      
      // Validar que solo contenga letras y números
      if (!/^[A-Z0-9]{18}$/.test(curpTrimmed)) {
        editErrors.value.curp = 'El CURP debe contener solo letras y números'
        return
      }
      
      editForm.value.curp = curpTrimmed
    }
    
    // Validar teléfono si se proporciona
    if (editForm.value.telefonoDigitos && editForm.value.telefonoDigitos.trim().length > 0) {
      const telTrimmed = editForm.value.telefonoDigitos.trim()
      
      // Validar que solo contenga números
      if (!/^\d+$/.test(telTrimmed)) {
        editErrors.value.telefonoDigitos = 'El teléfono solo debe contener números'
        return
      }
      
      // Validar que tenga entre 7 y 15 dígitos (estándar internacional)
      if (telTrimmed.length < 7 || telTrimmed.length > 15) {
        editErrors.value.telefonoDigitos = 'El teléfono debe tener entre 7 y 15 dígitos'
        return
      }
      
      editForm.value.telefonoDigitos = telTrimmed
    }
    
    isUpdatingUser.value = true
    
    // Verificar conexión a internet
    const online = await checkInternetConnection()
    if (!online) {
      editErrors.value.general = getOfflineMessage()
      isUpdatingUser.value = false
      return
    }
    
    const storedUser = JSON.parse(localStorage.getItem('user'))
    
    // Construir teléfono completo
    const telefonoCompleto = editForm.value.telefonoDigitos ? 
      `${editForm.value.codigoPais}${editForm.value.telefonoDigitos.trim()}` : null
    
    try {
      console.log('📡 Enviando solicitud PATCH a:', `${API_URL}/usuarios/${storedUser.id}/info`)
      
      // Determinar el cargo final (si es OTRO, usar cargoOtro)
      const cargoFinal = editForm.value.cargo === 'OTRO' 
        ? editForm.value.cargoOtro.trim() 
        : editForm.value.cargo.trim()
      
      const response = await axios.patch(
        `${API_URL}/usuarios/${storedUser.id}/info`,
        {
          nombre_completo: editForm.value.nombre_completo.trim(),
          correo: editForm.value.correo.trim(),
          cargo: cargoFinal,
          supervisor: editForm.value.supervisor?.trim() || null,
          curp: editForm.value.curp?.trim() || null,
          telefono: telefonoCompleto,
          territorio: editForm.value.territorio || null
        },
        {
          timeout: 15000,
          headers: {
            'Content-Type': 'application/json'
          }
        }
      )
      
      console.log('✅ Respuesta del servidor:', response.data)
      
      if (response.status === 200 && response.data.success) {
        // Actualizar los datos del usuario en el estado local
        user.value = {
          ...user.value,
          nombre_completo: editForm.value.nombre_completo,
          correo: editForm.value.correo,
          cargo: cargoFinal,
          supervisor: editForm.value.supervisor,
          curp: editForm.value.curp,
          telefono: telefonoCompleto,
          territorio: editForm.value.territorio
        }
        
        // Actualizar localStorage
        const updatedUser = { 
          ...storedUser, 
          nombre_completo: editForm.value.nombre_completo,
          correo: editForm.value.correo,
          cargo: cargoFinal,
          supervisor: editForm.value.supervisor,
          curp: editForm.value.curp,
          telefono: telefonoCompleto,
          territorio: editForm.value.territorio
        }
        localStorage.setItem('user', JSON.stringify(updatedUser))
        
        // Cerrar modal de edición
        closeEditModal()
        
        // Mostrar modal de éxito
        showEditSuccessModal.value = true
        
        // Recargar datos del usuario para asegurar sincronización
        setTimeout(() => {
          loadUserData()
        }, 1000)
        
        // Si es técnico y tiene territorio, actualizar supervisor automáticamente en la base de datos
        const cargoUpper = (cargoFinal || '').toUpperCase()
        if ((cargoUpper === 'TECNICO SOCIAL' || cargoUpper === 'TECNICO PRODUCTIVO') && editForm.value.territorio) {
          try {
            console.log('🔄 Actualizando supervisor automático en BD después de guardar...')
            const respuestaSupervisor = await apiService.obtenerSupervisorAutomatico(storedUser.id)
            if (respuestaSupervisor.success && respuestaSupervisor.supervisor) {
              console.log(`✅ Supervisor actualizado en BD: ${respuestaSupervisor.supervisor}`)
              // Actualizar en memoria también
              user.value.supervisor = respuestaSupervisor.supervisor
              updatedUser.supervisor = respuestaSupervisor.supervisor
              localStorage.setItem('user', JSON.stringify(updatedUser))
            }
          } catch (error) {
            console.error('⚠️ Error actualizando supervisor automático:', error)
          }
        }
      }
    } catch (error) {
      console.error('❌ Error completo:', error)
      console.error('Estado:', error.response?.status)
      console.error('Datos de error:', error.response?.data)
      console.error('Código de error:', error.code)
      
      if (error.response?.status === 400) {
        // Error de validación
        const detail = error.response.data?.detail || 'Error de validación'
        editErrors.value.general = detail
      } else if (error.response?.status === 404) {
        editErrors.value.general = 'Usuario no encontrado en el servidor'
      } else if (error.response?.status === 500) {
        editErrors.value.general = 'Error interno del servidor. Por favor intenta más tarde'
      } else if (error.code === 'ECONNABORTED') {
        editErrors.value.general = 'La solicitud tardó demasiado tiempo. Verifica tu conexión'
      } else if (error.code === 'ERR_NETWORK' || !error.response) {
        editErrors.value.general = 'No se pudo conectar con el servidor. Verifica tu conexión a internet'
      } else {
        editErrors.value.general = error.response?.data?.message || 
                                  error.response?.data?.detail ||
                                  'Error desconocido al actualizar la información'
      }
    } finally {
      isUpdatingUser.value = false
    }
  } catch (error) {
    console.error('❌ Error general en actualización de usuario:', error)
    editErrors.value.general = 'Error inesperado al actualizar la información'
    isUpdatingUser.value = false
  }
}

// Función para seleccionar país
const selectCountry = (pais) => {
  editForm.value.codigoPais = pais.codigo
  showCountrySelector.value = false
}

// Función para validar teléfono
const validatePhoneEdit = () => {
  editForm.value.telefonoDigitos = editForm.value.telefonoDigitos.replace(/\D/g, '')
  
  if (editForm.value.telefonoDigitos.length > 10) {
    editForm.value.telefonoDigitos = editForm.value.telefonoDigitos.slice(0, 10)
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Efecto de vidrio realista - Glassmorphism */
.glass-card {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 6px 25px 0 rgba(31, 38, 135, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  padding: 0.875rem;
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
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  font-size: 0.8rem;
  color: #1f2937;
  transition: all 0.3s ease;
  box-shadow: 
    0 3px 12px 0 rgba(31, 38, 135, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  min-height: 30px;
  padding: 0.5rem;
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
  padding: 0.625rem 1rem;
  border-radius: 10px;
  border: 1px solid rgba(76, 175, 80, 0.3);
  background: linear-gradient(135deg, 
    rgba(76, 175, 80, 0.8) 0%, 
    rgba(56, 142, 60, 0.8) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  color: white;
  font-weight: 600;
  font-size: 0.8rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 3px 15px 0 rgba(76, 175, 80, 0.3),
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

.glass-button-secondary {
  padding: 0.625rem 1rem;
  border-radius: 10px;
  border: 1px solid rgba(156, 163, 175, 0.5);
  background: linear-gradient(135deg, 
    rgba(229, 231, 235, 0.8) 0%, 
    rgba(209, 213, 219, 0.8) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  color: #374151;
  font-weight: 600;
  font-size: 0.8rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 3px 15px 0 rgba(156, 163, 175, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
}

.glass-button-secondary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 30px 0 rgba(156, 163, 175, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
  background: linear-gradient(135deg, 
    rgba(243, 244, 246, 0.9) 0%, 
    rgba(229, 231, 235, 0.9) 100%);
}

.glass-button-secondary:active:not(:disabled) {
  transform: translateY(0px);
  box-shadow: 
    0 4px 15px 0 rgba(156, 163, 175, 0.2),
    inset 0 2px 4px 0 rgba(0, 0, 0, 0.05);
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

.glass-avatar {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px 0 rgba(76, 175, 80, 0.3),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
}

.glass-avatar-outline {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 
    0 8px 32px 0 rgba(76, 175, 80, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.glass-avatar-outline::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    135deg,
    transparent 0%,
    rgba(255, 255, 255, 0.1) 50%,
    transparent 100%
  );
  animation: shine 3s infinite;
}

@keyframes shine {
  0% {
    transform: rotate(0deg) translate(-100%, -100%);
  }
  100% {
    transform: rotate(360deg) translate(-100%, -100%);
  }
}

.glass-avatar-outline:hover {
  border-color: rgba(76, 175, 80, 0.6);
  box-shadow: 
    0 8px 32px 0 rgba(76, 175, 80, 0.4),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2),
    0 0 20px rgba(76, 175, 80, 0.3);
}

.glass-success-icon {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 2px solid rgba(34, 197, 94, 0.2);
  box-shadow: 
    0 8px 32px 0 rgba(34, 197, 94, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
}

.glass-info-row {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  padding: 0.5rem 0;
  transition: all 0.3s ease;
}

.glass-info-row:hover {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding-left: 0.5rem;
  padding-right: 0.5rem;
}

.glass-info-row:last-child {
  border-bottom: none;
}

.modern-title {
  color: #16a34a;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  letter-spacing: -0.015em;
  font-weight: 500;
  position: relative;
}

.green-line {
  width: 40px;
  height: 1.5px;
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
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
  }
  
  .glass-card {
    padding: 0.625rem;
    margin-bottom: 0.375rem;
    border-radius: 12px;
  }
  
  .glass-input {
    font-size: 14px; /* Evita zoom en iOS */
    min-height: 28px;
    padding: 0.375rem;
  }
  
  .text-base {
    font-size: 0.8rem;
  }
  
  .text-sm {
    font-size: 0.75rem;
  }
  
  .w-12, .h-12 {
    width: 2.75rem;
    height: 2.75rem;
  }
  
  .h-6, .w-6 {
    height: 1.25rem;
    width: 1.25rem;
  }
  
  .mb-2 {
    margin-bottom: 0.375rem;
  }
  
  .mb-3 {
    margin-bottom: 0.5rem;
  }
  
  .space-y-3 > * + * {
    margin-top: 0.5rem;
  }
  
  .space-y-2 > * + * {
    margin-top: 0.375rem;
  }
}

@media (max-width: 375px) {
  .page-container {
    padding-left: 0.375rem;
    padding-right: 0.375rem;
    max-width: calc(100vw - 0.75rem);
  }
  
  .glass-card {
    padding: 0.5rem;
    margin-bottom: 0.25rem;
    border-radius: 10px;
  }
  
  .glass-input {
    font-size: 14px;
    min-height: 26px;
    padding: 0.25rem 0.375rem;
  }
  
  .glass-button {
    padding: 0.375rem 0.75rem;
    font-size: 0.75rem;
  }
  
  .text-base {
    font-size: 0.75rem;
  }
  
  .text-sm {
    font-size: 0.7rem;
  }
  
  .text-xs {
    font-size: 0.65rem;
  }
}

@media (max-height: 700px) {
  .page-container {
    padding-top: 0.375rem;
    padding-bottom: 0.375rem;
  }
  
  .glass-card {
    margin-bottom: 0.25rem;
    padding: 0.5rem;
  }
  
  .mb-2 {
    margin-bottom: 0.25rem;
  }
  
  .mb-3 {
    margin-bottom: 0.375rem;
  }
  
  .space-y-3 > * + * {
    margin-top: 0.375rem;
  }
  
  .space-y-2 > * + * {
    margin-top: 0.25rem;
  }
}

@media (max-height: 600px) {
  .page-container {
    max-width: 280px;
    padding: 0.25rem 0.375rem;
  }
  
  .glass-card {
    padding: 0.5rem;
    margin-bottom: 0.125rem;
  }
  
  .w-12, .h-12 {
    width: 2.5rem;
    height: 2.5rem;
  }
  
  .text-base {
    font-size: 0.75rem;
  }
  
  .text-sm {
    font-size: 0.7rem;
  }
}

@media (max-height: 500px) {
  .glass-card {
    padding: 0.375rem;
  }
  
  .mb-1, .mb-2, .mb-3 {
    margin-bottom: 0.125rem;
  }
  
  .space-y-3 > * + * {
    margin-top: 0.25rem;
  }
  
  .space-y-2 > * + * {
    margin-top: 0.125rem;
  }
}

/* Para pantallas grandes */
@media (min-width: 768px) {
  .page-container {
    max-width: 350px;
    padding: 0.75rem;
  }
  
  .glass-card {
    padding: 1rem;
    margin-bottom: 0.75rem;
  }
}

@media (min-width: 1024px) {
  .page-container {
    max-width: 380px;
    padding: 1rem 0.75rem;
  }
  
  .glass-card {
    padding: 1.125rem;
    margin-bottom: 1rem;
  }
}

/* Prevenir superposición de elementos */
.glass-card {
  position: relative;
  z-index: 2;
  clear: both;
}

/* Asegurar que los modales estén por encima de todo */
.fixed[style*="z-index: 60"] {
  z-index: 60 !important;
}

/* Z-index hierarchy para elementos principales */
.page-container {
  position: relative;
  z-index: 2;
}

/* Contenedor de fondo con z-index bajo */
.fixed.inset-0[style*="z-index: 0"] {
  z-index: 0 !important;
}

/* Contenedor scrollable */
.absolute.inset-0[style*="z-index: 1"] {
  z-index: 1 !important;
}

/* Mejoras para el contenedor scrollable */
.absolute.inset-0.overflow-y-auto {
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}

/* Espaciado optimizado para evitar superposición */
.space-y-3 > * + * {
  margin-top: 0.75rem;
}

.space-y-4 > * + * {
  margin-top: 1rem;
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
}

/* Estilos para modales de edición */
.edit-modal {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Inputs del modal de edición */
.edit-input {
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  background-color: #f9fafb;
}

.edit-input:focus {
  outline: none;
  border-color: #10b981;
  background-color: white;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.edit-input.border-red-500 {
  border-color: #ef4444;
}

.edit-input.border-red-500:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

/* Versión pequeña de inputs para móviles */
.edit-input-small {
  padding: 0.5rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.75rem;
  transition: all 0.2s ease;
  background-color: #f9fafb;
}

.edit-input-small:focus {
  outline: none;
  border-color: #10b981;
  background-color: white;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1);
}

.edit-input-small.border-red-500 {
  border-color: #ef4444;
}

.edit-input-small.border-red-500:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.1);
}

/* Botón de edición circular mejorado */
.glass-edit-button {
  width: 2rem;
  height: 2rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #374151;
  transition: all 0.2s ease;
  cursor: pointer;
}

.glass-edit-button:hover {
  background: rgba(16, 185, 129, 0.1);
  border-color: rgba(16, 185, 129, 0.3);
  color: #10b981;
  transform: scale(1.05);
}

.glass-edit-button:active {
  transform: scale(0.95);
}

/* Estilos mejorados para la información del usuario */
.info-item-enhanced {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 10px;
  padding: 0.5rem 0.625rem;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
  overflow: hidden;
}

.info-item-enhanced::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, transparent 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.info-item-enhanced:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(76, 175, 80, 0.2);
  box-shadow: 
    0 4px 15px rgba(76, 175, 80, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.info-item-enhanced:hover::before {
  opacity: 1;
}

/* Estilos para iconos de insignia */
.icon-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  flex-shrink: 0;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: currentColor;
}

.icon-user {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.3), rgba(147, 197, 253, 0.2));
  border-color: rgba(59, 130, 246, 0.4);
  color: #3b82f6;
}

.icon-email {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.3), rgba(196, 181, 253, 0.2));
  border-color: rgba(139, 92, 246, 0.4);
  color: #8b5cf6;
}

.icon-position {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.3), rgba(187, 247, 208, 0.2));
  border-color: rgba(34, 197, 94, 0.4);
  color: #22c55e;
}

.icon-supervisor {
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.3), rgba(244, 194, 213, 0.2));
  border-color: rgba(236, 72, 153, 0.4);
  color: #ec4899;
}

.icon-curp {
  background: linear-gradient(135deg, rgba(249, 115, 22, 0.3), rgba(254, 215, 170, 0.2));
  border-color: rgba(249, 115, 22, 0.4);
  color: #f97316;
}

.icon-phone {
  background: linear-gradient(135deg, rgba(14, 165, 233, 0.3), rgba(186, 230, 253, 0.2));
  border-color: rgba(14, 165, 233, 0.4);
  color: #0ea5e9;
}

.icon-territorio {
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.3), rgba(251, 207, 232, 0.2));
  border-color: rgba(236, 72, 153, 0.4);
  color: #ec4899;
}

.icon-date {
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.3), rgba(233, 213, 255, 0.2));
  border-color: rgba(168, 85, 247, 0.4);
  color: #a855f7;
}

.info-item-enhanced:hover .icon-badge {
  transform: scale(1.1) translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Estilos para labels e información */
.label-info {
  font-size: 0.65rem;
  font-weight: 600;
  text-transform: capitalize;
  letter-spacing: 0.02em;
  color: #9ca3af;
  margin: 0;
  transition: color 0.3s ease;
  line-height: 1;
}

.info-item-enhanced:hover .label-info {
  color: #6b7280;
}

/* Estilos para valores de información - diferenciados por tipo */
.value-info {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0.25rem 0 0 0;
  transition: all 0.3s ease;
  word-break: break-word;
  line-height: 1.1;
}

.value-name {
  background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 500;
  font-family: 'Segoe UI', 'Roboto', sans-serif;
}

.value-email {
  background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 600;
}

.value-position {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
}

.value-supervisor {
  background: linear-gradient(135deg, #db2777 0%, #be185d 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 600;
}

.value-curp {
  background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 600;
  font-family: 'Courier New', monospace;
}

.value-phone {
  background: linear-gradient(135deg, #0369a1 0%, #0c4a6e 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 600;
}

.value-territorio {
  background: linear-gradient(135deg, #db2777 0%, #be185d 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 600;
}

.value-date {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 600;
}

.info-item-enhanced:hover .value-info {
  transform: translateX(2px);
}

/* Animación de borde neon giratorio */
@keyframes neon-glow {
  0%, 100% {
    box-shadow: 0 0 5px rgba(22, 163, 74, 0.5), inset 0 0 5px rgba(22, 163, 74, 0.2);
  }
  50% {
    box-shadow: 0 0 15px rgba(22, 163, 74, 0.9), inset 0 0 15px rgba(22, 163, 74, 0.4), 0 0 30px rgba(22, 163, 74, 0.6);
  }
}

@keyframes spin-border {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Fallback para navegadores que no soportan background-clip */
@supports not (-webkit-background-clip: text) {
  .value-name {
    color: #1f2937;
  }
  
  .value-email {
    color: #7c3aed;
  }
  
  .value-position {
    color: #059669;
  }
  
  .value-supervisor {
    color: #db2777;
  }
  
  .value-curp {
    color: #ea580c;
  }
  
  .value-phone {
    color: #0369a1;
  }
  
  .value-date {
    color: #8b5cf6;
  }
}
</style>
