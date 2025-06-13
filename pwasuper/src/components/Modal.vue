<template>
  <transition name="modal" appear>
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <!-- Overlay -->
      <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity" @click="$emit('close')"></div>
        <!-- Modal -->
      <div class="relative bg-white rounded-lg shadow-xl max-w-sm w-full mx-auto transform transition-all">
        <div class="p-4 text-center">
          <!-- Icono de éxito -->
          <div class="mx-auto flex items-center justify-center h-10 w-10 rounded-full bg-green-100 mb-3">
            <svg class="h-5 w-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          
          <!-- Título -->
          <h3 class="text-base font-medium text-gray-900 mb-2">
            {{ title }}
          </h3>
          
          <!-- Mensaje -->
          <p class="text-sm text-gray-500 mb-4">
            {{ message }}
          </p>
          
          <!-- Botón -->
          <button
            @click="$emit('close')"
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-3 py-2 bg-green-600 text-sm font-medium text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors"
          >
            Aceptar
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: '¡Éxito!'
  },
  message: {
    type: String,
    default: ''
  }
});

defineEmits(['close']);
</script>

<style scoped>
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-active .bg-white,
.modal-leave-active .bg-white {
  transition: all 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

.modal-enter-from .bg-white,
.modal-leave-to .bg-white {
  transform: scale(0.9) translateY(-20px);
}
</style>
