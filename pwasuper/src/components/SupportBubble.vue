<template>
  <teleport to="body">
    <!-- Burbuja de soporte flotante -->
    <div
      v-if="!isHidden && !props.hideOnSupportPage"
      class="fixed bottom-6 right-6 z-50 select-none"
      :class="{ 'translate-y-0': isVisible, 'translate-y-20': !isVisible }"
      style="transition: transform 0.3s ease-in-out;"
    >
      <!-- Contenedor principal de la burbuja -->
      <div class="relative">
        <!-- Overlay semitransparente cuando está expandido -->
        <transition name="fade">
          <div
            v-if="isExpanded"
            class="fixed inset-0 bg-black/20 backdrop-blur-sm"
            style="z-index: -1;"
            @click="toggleExpanded"
          ></div>
        </transition>

        <!-- Panel expandido de soporte -->
        <transition name="scale-fade">
          <div
            v-if="isExpanded"
            class="absolute bottom-16 right-0 rounded-2xl shadow-2xl border p-4 w-80 max-w-[calc(100vw-3rem)] backdrop-blur-sm"
            style="background: linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(248,250,252,1) 100%); backdrop-filter: blur(15px); border: 2px solid rgba(148, 30, 67, 0.2); box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(255, 255, 255, 0.8), inset 0 1px 0 rgba(255, 255, 255, 0.9);"
            @click.stop
          >
            <!-- Header del panel -->
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center space-x-3">
                <div class="w-8 h-8 rounded-full flex items-center justify-center shadow-md" style="background: linear-gradient(135deg, #941E43 0%, #7D1A3A 100%);">
                  <font-awesome-icon 
                    icon="headset"
                    class="h-4 w-4 text-white"
                  />
                </div>
                <div>
                  <h3 class="font-semibold text-gray-900 text-sm">Soporte Técnico</h3>
                  <p class="text-xs text-gray-500">Estamos aquí para ayudarte</p>
                </div>
              </div>
              <button
                @click="toggleExpanded"
                class="p-1 hover:bg-gray-100 rounded-full transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- Horario de atención -->
            <div class="rounded-xl p-3 mb-4 border" style="background: linear-gradient(to right, rgba(0, 128, 128, 0.1), rgba(0, 128, 128, 0.15)); border-color: rgba(0, 128, 128, 0.3);">
              <div class="flex items-center space-x-2 mb-2">
                <div class="w-5 h-5 rounded-full flex items-center justify-center" style="background-color: rgb(0, 128, 128);">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <span class="font-medium text-sm" style="color: rgb(0, 100, 100);">Horario de Atención</span>
              </div>
              <div class="text-xs space-y-1" style="color: rgb(0, 100, 100);">
                <div class="flex items-center space-x-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" style="color: rgb(0, 128, 128);" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span>Lunes a Viernes</span>
                </div>
                <div class="flex items-center space-x-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" style="color: rgb(0, 128, 128);" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>10:00 - 18:00 horas</span>
                </div>
                <div class="mt-2 p-2 bg-white/60 rounded-lg">
                  <div class="flex items-center space-x-1">
                    <div class="w-2 h-2 rounded-full" :class="isHorarioAbierto ? 'bg-green-400' : 'bg-red-400'"></div>
                    <span class="text-xs font-medium" :class="isHorarioAbierto ? 'text-green-700' : 'text-red-700'">
                      {{ isHorarioAbierto ? 'Disponible Ahora' : 'Fuera de Horario' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Opciones de contacto -->
            <div class="space-y-3">
              <!-- WhatsApp -->
              <a
                href="http://wa.me/525646611850"
                target="_blank"
                rel="noopener noreferrer"
                @click="handleContactClick('whatsapp')"
                class="flex items-center space-x-3 p-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl hover:from-green-600 hover:to-green-700 transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98] shadow-lg"
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
            </div>

            <!-- Mensaje adicional -->
            <div class="mt-4 p-3 bg-gray-50 rounded-xl border border-gray-100">
              <div class="flex items-start space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div class="text-xs text-gray-600">
                  <p class="font-medium mb-1">¿Necesitas ayuda?</p>
                  <p>Nuestro equipo de soporte está listo para asistirte con cualquier problema técnico o duda sobre la aplicación.</p>
                </div>
              </div>
            </div>
          </div>
        </transition>

        <!-- Botón principal de la burbuja -->
        <button
          @click="toggleExpanded"
          class="relative w-14 h-14 text-white rounded-full shadow-2xl hover:shadow-3xl transition-all duration-300 transform hover:scale-110 active:scale-95 flex items-center justify-center group"
          style="background: linear-gradient(135deg, #941E43 0%, #7D1A3A 100%); box-shadow: 0 10px 25px rgba(148, 30, 67, 0.4);"
          :class="{ 'rotate-45': isExpanded }"
        >
          <!-- Efecto de ondas al hacer hover -->
          <div class="absolute inset-0 rounded-full opacity-75 group-hover:animate-ping" style="background-color: #B8225F;"></div>
          
              <!-- Icono principal -->
              <div class="relative z-10">
                <transition name="rotate-icon" mode="out-in">
                  <font-awesome-icon 
                    v-if="!isExpanded"
                    key="support"
                    icon="headset"
                    class="h-6 w-6 text-white"
                  />
                  <svg 
                    v-else
                    key="close"
                    xmlns="http://www.w3.org/2000/svg" 
                    class="h-6 w-6" 
                    fill="none" 
                    viewBox="0 0 24 24" 
                    stroke="currentColor"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </transition>
              </div>

          <!-- Badge de notificación (opcional) -->
          <div 
            v-if="showNotificationBadge && !isExpanded"
            class="absolute -top-1 -right-1 w-4 h-4 text-white text-xs font-bold rounded-full flex items-center justify-center shadow-md animate-bounce"
            style="background-color: #941E43;"
          >
            !
          </div>
        </button>

        <!-- Botón para ocultar temporalmente -->
        <button
          v-if="!isExpanded"
          @click="hideTemporarily"
          class="absolute -top-2 -left-2 w-6 h-6 bg-gray-600 text-white rounded-full hover:bg-gray-700 transition-colors flex items-center justify-center text-xs shadow-lg"
          title="Ocultar temporalmente"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Botón para mostrar de nuevo cuando está oculto -->
    <transition name="slide-up">
      <div
        v-if="isHidden && !props.hideOnSupportPage"
        class="fixed bottom-6 right-6 z-50"
      >
        <button
          @click="showAgain"
          class="w-12 h-8 bg-gray-600 text-white rounded-t-lg hover:bg-gray-700 transition-colors flex items-center justify-center shadow-lg"
          title="Mostrar soporte"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192L5.636 18.364M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        </button>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  showNotificationBadge: {
    type: Boolean,
    default: false
  },
  autoShow: {
    type: Boolean,
    default: true
  },
  hideOnSupportPage: {
    type: Boolean,
    default: false
  }
})

const isExpanded = ref(false)
const isVisible = ref(false)
const isHidden = ref(false)

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

const toggleExpanded = () => {
  isExpanded.value = !isExpanded.value
}

const hideTemporarily = () => {
  isExpanded.value = false
  isVisible.value = false
  setTimeout(() => {
    isHidden.value = true
  }, 300)
}

const showAgain = () => {
  isHidden.value = false
  setTimeout(() => {
    isVisible.value = true
  }, 100)
}

const handleContactClick = (type) => {
  // Emitir evento para analytics si es necesario
  console.log(`Usuario contactó soporte vía: ${type}`)
  
  // Cerrar el panel después de un breve delay
  setTimeout(() => {
    isExpanded.value = false
  }, 500)
}

// Cerrar panel al hacer clic fuera
const handleClickOutside = (event) => {
  if (isExpanded.value && !event.target.closest('.fixed.bottom-6.right-6')) {
    isExpanded.value = false
  }
}

onMounted(() => {
  if (props.autoShow) {
    setTimeout(() => {
      isVisible.value = true
    }, 1000) // Mostrar después de 1 segundo
  }
  
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* Animaciones personalizadas */
.scale-fade-enter-active,
.scale-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: bottom right;
}

.scale-fade-enter-from,
.scale-fade-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(10px);
}

.rotate-icon-enter-active,
.rotate-icon-leave-active {
  transition: all 0.2s ease;
}

.rotate-icon-enter-from,
.rotate-icon-leave-to {
  opacity: 0;
  transform: rotate(-90deg);
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(100%);
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Animación de hover mejorada */
.group:hover .group-hover\:animate-ping {
  animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite;
}

@keyframes ping {
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}

/* Sombra personalizada */
.shadow-3xl {
  box-shadow: 0 20px 40px rgba(148, 30, 67, 0.6);
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .w-80 {
    width: calc(100vw - 2rem);
    max-width: 320px;
  }
}
</style>