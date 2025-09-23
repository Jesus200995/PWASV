<template>
  <teleport to="body">
    <!-- Fondo difuminado cuando el panel está abierto -->
    <transition name="backdrop-fade">
      <div
        v-if="isExpanded"
        class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm z-40"
        @click="toggleExpanded"
      ></div>
    </transition>

    <!-- Panel expandido -->
    <transition name="panel-scale">
      <div
        v-if="isExpanded"
        class="fixed z-50"
        :style="panelStyle"
      >
        <div
          class="shadow-2xl p-4 w-80 max-w-[calc(100vw-2rem)]"
          :style="baseStyles"
        >
          <!-- Header del panel -->
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 rounded-full flex items-center justify-center shadow-md" style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);">
                <font-awesome-icon 
                  icon="headset"
                  class="h-4 w-4 text-white"
                />
              </div>
              <div>
                <h3 class="font-semibold text-gray-800 text-sm">Soporte</h3>
                <p class="text-xs text-gray-500">¿Necesitas ayuda?</p>
              </div>
            </div>
          </div>

          <!-- Horario de atención -->
          <div class="p-3 mb-4 shadow-sm" style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.08) 0%, rgba(30, 64, 175, 0.12) 100%); border-radius: 1.5rem; border: 1px solid rgba(30, 58, 138, 0.15);">
            <div class="flex items-center space-x-2 mb-2">
              <div class="w-6 h-6 rounded-full flex items-center justify-center shadow-sm" style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <span class="font-semibold text-xs" :class="isHorarioAbierto ? 'text-green-700' : 'text-red-700'">
                  {{ isHorarioAbierto ? 'Disponible Ahora' : 'Fuera de Horario' }}
                </span>
                <p class="text-xs text-gray-600 mt-0.5">
                  {{ isHorarioAbierto ? 'Te respondemos inmediatamente' : 'Responderemos en horario laboral' }}
                </p>
              </div>
            </div>
            
            <div class="bg-white bg-opacity-60 p-2 space-y-1" style="border-radius: 0.75rem;">
              <div class="flex items-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" style="color: #1e3a8a;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span class="font-medium text-xs" style="color: #1e3a8a;">Lunes a Viernes</span>
              </div>
              <div class="flex items-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" style="color: #1e3a8a;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="font-medium text-xs" style="color: #1e3a8a;">10:00 AM - 6:00 PM</span>
              </div>
            </div>
            
            <!-- Indicador visual de estado -->
            <div class="mt-2 flex items-center justify-center">
              <div class="flex items-center space-x-1">
                <div class="w-2 h-2 rounded-full" :class="isHorarioAbierto ? 'bg-green-400 animate-pulse' : 'bg-red-400'"></div>
                <span class="text-xs font-medium" :class="isHorarioAbierto ? 'text-green-700' : 'text-red-700'">
                  {{ isHorarioAbierto ? 'En línea' : 'Fuera de línea' }}
                </span>
              </div>
            </div>
          </div>

          <!-- Contacto WhatsApp -->
          <div class="space-y-3">
            <a
              href="http://wa.me/525646611850"
              target="_blank"
              rel="noopener noreferrer"
              @click="handleContactClick"
              class="flex items-center space-x-3 p-3 bg-gradient-to-r from-green-500 to-green-600 text-white hover:from-green-600 hover:to-green-700 transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98] shadow-lg"
              style="border-radius: 0.75rem;"
            >
              <div class="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0020.885 3.787"/>
                </svg>
              </div>
              <div class="flex-1">
                <div class="font-semibold text-sm">WhatsApp</div>
                <div class="text-xs opacity-90">Respuesta inmediata</div>
              </div>
              <div class="w-5 h-5">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </div>
            </a>

            <!-- Mensaje adicional -->
            <div class="mt-4 p-3 bg-gray-50 border border-gray-100" style="border-radius: 0.75rem;">
              <div class="flex items-start space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
                <div class="text-xs text-gray-600">
                  <p class="font-medium mb-1">¿Problemas para acceder?</p>
                  <p>Contáctanos si tienes dificultades con tu login o necesitas recuperar tu cuenta.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Burbuja principal (posición fija lado derecho) -->
    <div
      v-if="!props.hideOnLoginPage"
      class="fixed z-50 top-4 right-4"
    >
      <!-- Botón principal de la burbuja -->
      <button
        @click="toggleExpanded"
        class="relative w-12 h-12 text-white rounded-full shadow-2xl hover:shadow-3xl transition-all duration-300 transform hover:scale-110 active:scale-95 flex items-center justify-center group"
        style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%); box-shadow: 0 10px 25px rgba(30, 58, 138, 0.4);"
      >
        <!-- Icono principal -->
        <div class="relative z-10">
          <transition name="rotate-icon" mode="out-in">
            <font-awesome-icon 
              v-if="!isExpanded"
              key="support"
              icon="headset"
              class="h-5 w-5 text-white"
            />
            <svg 
              v-else
              key="minimize"
              xmlns="http://www.w3.org/2000/svg" 
              class="h-5 w-5" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
            </svg>
          </transition>
        </div>
      </button>
    </div>
  </teleport>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  hideOnLoginPage: {
    type: Boolean,
    default: false
  }
})

const isExpanded = ref(false)

// Determinar si estamos en horario de atención
const isHorarioAbierto = computed(() => {
  const now = new Date()
  const currentHour = now.getHours()
  const currentDay = now.getDay() // 0 = Sunday, 1 = Monday, ..., 6 = Saturday
  
  // Lunes a Viernes (1-5) de 10:00 a 18:00
  const esDiaLaboral = currentDay >= 1 && currentDay <= 5
  const estaEnHorario = currentHour >= 10 && currentHour < 18
  
  return esDiaLaboral && estaEnHorario
})

// Estilos del panel
const baseStyles = {
  background: 'linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(248,250,252,1) 100%)',
  backdropFilter: 'blur(15px)',
  border: '2px solid rgba(30, 58, 138, 0.3)',
  borderRadius: '2rem',
  boxShadow: '0 25px 50px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(30, 58, 138, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.9)',
  maxHeight: '80vh',
  overflowY: 'auto',
  overflow: 'hidden'
}

// Posición del panel (siempre en la esquina superior derecha)
const panelStyle = computed(() => {
  return {
    top: '4.5rem',
    right: '1rem',
    ...baseStyles
  }
})

const toggleExpanded = () => {
  isExpanded.value = !isExpanded.value
}

const handleContactClick = () => {
  console.log('Usuario contactó soporte vía WhatsApp desde login')
}
</script>

<style scoped>
/* Animación del fondo difuminado */
.backdrop-fade-enter-active, .backdrop-fade-leave-active {
  transition: all 0.3s ease;
}

.backdrop-fade-enter-from, .backdrop-fade-leave-to {
  opacity: 0;
  backdrop-filter: blur(0px);
}

/* Animaciones específicas para login */
.panel-scale-enter-active, .panel-scale-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: top right;
}

.panel-scale-enter-from, .panel-scale-leave-to {
  opacity: 0;
  transform: scale(0.9) translateY(-10px);
}

.rotate-icon-enter-active, .rotate-icon-leave-active {
  transition: all 0.3s ease;
}

.rotate-icon-enter-from, .rotate-icon-leave-to {
  opacity: 0;
  transform: rotate(180deg) scale(0.8);
}
</style>