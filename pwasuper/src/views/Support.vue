<template>
  <div class="fixed inset-0 overflow-hidden" style="background: linear-gradient(135deg, rgba(101, 219, 46, 0.05) 0%, rgba(76, 175, 80, 0.08) 50%, rgba(101, 219, 46, 0.05) 100%);">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="background-color: rgba(101, 219, 46, 0.3);"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s; background-color: rgba(76, 175, 80, 0.3);"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s; background-color: rgba(56, 142, 60, 0.3);"></div>
    </div>
    
    <div class="absolute inset-0 overflow-y-auto pt-16 sm:pt-20 pb-4">
      <div class="page-container relative z-10 px-2 sm:px-3 md:px-4 lg:px-6 xl:px-8 py-3 sm:py-4 lg:py-5 min-h-full max-w-full">
        <div class="w-full max-w-lg mx-auto space-y-4">
      <!-- Header de Soporte -->
      <div class="glass-card text-center">
        <div class="flex items-center justify-center mb-3">
          <div class="w-12 h-12 rounded-full flex items-center justify-center shadow-xl" style="background: linear-gradient(135deg, #65DB2E 0%, #4CAF50 100%);">
            <font-awesome-icon 
              icon="headset"
              class="h-6 w-6 text-white"
            />
          </div>
        </div>
        
        <h1 class="text-xl font-bold text-gray-800 mb-2 modern-title">Soporte Técnico</h1>
        <div class="red-line mx-auto mb-2"></div>
        <p class="text-gray-600 text-xs mb-3">Estamos aquí para ayudarte con cualquier problema o duda</p>
        
        <!-- Estado de disponibilidad -->
        <div class="inline-flex items-center px-3 py-1.5 rounded-full text-xs font-medium" 
             :class="isHorarioAbierto ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
          <div class="w-1.5 h-1.5 rounded-full mr-2" :class="isHorarioAbierto ? 'bg-green-400' : 'bg-red-400'"></div>
          {{ isHorarioAbierto ? 'Disponible Ahora' : 'Fuera de Horario' }}
        </div>
      </div>

      <!-- Horario de atención -->
      <div class="glass-card">
        <div class="flex items-center mb-3">
          <div class="w-8 h-8 rounded-full flex items-center justify-center mr-3" style="background-color: rgb(0, 128, 128);">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h2 class="text-base font-semibold text-gray-800">Horario de Atención</h2>
            <p class="text-xs text-gray-500">Te atendemos en estos horarios</p>
          </div>
        </div>
        
        <div class="rounded-xl p-3 border" style="background: linear-gradient(to right, rgba(0, 128, 128, 0.1), rgba(0, 128, 128, 0.15)); border-color: rgba(0, 128, 128, 0.3);">
          <div class="grid grid-cols-1 gap-2">
            <div class="flex items-center space-x-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" style="color: rgb(0, 128, 128);" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span class="font-medium text-sm" style="color: rgb(0, 100, 100);">Lunes a Viernes</span>
            </div>
            <div class="flex items-center space-x-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" style="color: rgb(0, 128, 128);" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span class="font-medium text-sm" style="color: rgb(0, 100, 100);">10:00 - 18:00 horas</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Opciones de contacto -->
      <div class="glass-card">
        <h2 class="text-base font-semibold text-gray-800 mb-3 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="color: #65DB2E;">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
          </svg>
          Opciones de Contacto
        </h2>
        
        <div class="space-y-3">
          <!-- WhatsApp -->
          <a
            href="http://wa.me/525646611850"
            target="_blank"
            rel="noopener noreferrer"
            @click="handleContactClick('whatsapp')"
            class="flex items-center space-x-3 p-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl hover:from-green-600 hover:to-green-700 transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98] shadow-lg"
          >
            <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0020.885 3.787"/>
              </svg>
            </div>
            <div class="flex-1">
              <div class="font-semibold text-base">WhatsApp</div>
              <div class="text-xs opacity-90">Respuesta inmediata • Chat directo</div>
              <div class="text-xs opacity-80 mt-0.5">Recomendado para consultas rápidas</div>
            </div>
            <div class="w-5 h-5">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </div>
          </a>
        </div>
      </div>

      <!-- Información adicional -->
      <div class="glass-card">
        <h2 class="text-base font-semibold text-gray-800 mb-3 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-600 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          ¿Cómo podemos ayudarte?
        </h2>
        
        <div class="space-y-3">
          <div class="flex items-start space-x-2 p-2.5 bg-gray-50 rounded-lg">
            <div class="w-7 h-7 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <div>
              <h3 class="font-medium text-gray-800 mb-1 text-sm">Problemas Técnicos</h3>
              <p class="text-xs text-gray-600">Errores en la aplicación, problemas de conexión, fallos en funcionalidades</p>
            </div>
          </div>
          
          <div class="flex items-start space-x-2 p-2.5 bg-gray-50 rounded-lg">
            <div class="w-7 h-7 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h3 class="font-medium text-gray-800 mb-1 text-sm">Dudas de Uso</h3>
              <p class="text-xs text-gray-600">Cómo usar las funciones, registro de actividades, gestión de asistencia</p>
            </div>
          </div>
          
          <div class="flex items-start space-x-2 p-2.5 bg-gray-50 rounded-lg">
            <div class="w-7 h-7 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
              </svg>
            </div>
            <div>
              <h3 class="font-medium text-gray-800 mb-1 text-sm">Configuración</h3>
              <p class="text-xs text-gray-600">Ajustes de cuenta, permisos, configuración de notificaciones</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Mensaje motivacional -->
      <div class="glass-card text-center border" style="background: linear-gradient(to right, rgba(101, 219, 46, 0.05), rgba(76, 175, 80, 0.08)); border-color: rgba(101, 219, 46, 0.2);">
        <div class="flex items-center justify-center mb-2">
          <div class="w-8 h-8 rounded-full flex items-center justify-center" style="background-color: rgba(101, 219, 46, 0.1);">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="color: #65DB2E;">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </div>
        </div>
        <h3 class="font-semibold text-gray-800 mb-1 text-sm">Estamos aquí para ti</h3>
        <p class="text-xs text-gray-600">
          No dudes en contactarnos. Nuestro equipo de soporte está comprometido a brindarte la mejor experiencia posible.
        </p>
      </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

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

const handleContactClick = (type) => {
  // Emitir evento para analytics si es necesario
  console.log(`Usuario contactó soporte vía: ${type} desde vista de soporte`)
}
</script>

<style scoped>
/* Estilos específicos para la vista de soporte */
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
  color: #052e16;
}

.red-line {
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #65DB2E, #4CAF50);
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

/* Responsive adjustments */
@media (max-width: 640px) {
  .page-container {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}
</style>