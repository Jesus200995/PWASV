<template>
  <transition name="modal">
    <div v-if="show" class="modal-overlay" @click="$emit('close')">
      <div class="modal-container" :class="{ 'compact': type === 'info', 'compact-confirm': type === 'confirm' }" 
           :data-modal-type="title && title.includes('Entrada') ? 'entrada' : title && title.includes('Salida') ? 'salida' : ''" 
           @click.stop>
        <!-- Header más elegante - Solo mostrar en tipos info, success, warning -->
        <div v-if="title && type !== 'confirm' && type !== 'error'" class="modal-header">
          <div class="flex items-center">
            <div v-if="type === 'confirm'" class="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
              <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <h3 class="modal-title">{{ title }}</h3>
          </div>
          <button @click="$emit('close')" class="modal-close group">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 transition-colors group-hover:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <!-- Botón de cierre para modales de confirmación (confirm y error) -->
        <div v-if="type === 'confirm' || type === 'error'" class="absolute top-2 right-2 z-10">
          <button @click="$emit('close')" class="modal-close group">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transition-colors group-hover:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <!-- Body más espacioso -->
        <div class="modal-body">
          <!-- Iconos principales más grandes - Ocultos para confirm y error -->
          <div class="confirm-icon" v-if="type === 'confirm' && false">
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
          </div>
          
          <div class="success-icon" v-else-if="type === 'success'">
            <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
            </div>
          </div>
          
          <div class="warning-icon" v-else-if="type === 'warning'">
            <div class="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"/>
              </svg>
            </div>
          </div>
          
          <div class="error-icon" v-else-if="type === 'error' && false">
            <div class="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3" 
                 style="background-color: rgba(220, 20, 60, 0.1);">
              <svg class="w-6 h-6" style="color: rgb(220, 20, 60);" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </div>
          </div>
          
          <div class="modal-message" v-html="message"></div>
        </div>
        
        <!-- Footer mejorado -->
        <div class="modal-footer">
          <div v-if="showConfirm" class="flex gap-3">
            <button @click="$emit('close')" class="btn btn-secondary flex-1">
              {{ cancelText }}
            </button>
            <button @click="$emit('confirm')" class="btn btn-primary flex-1">
              {{ confirmText }}
            </button>
          </div>
          <button v-else @click="$emit('close')" class="btn btn-primary w-full">
            {{ cancelText || 'Entendido' }}
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
    default: 'Notificación'
  },
  message: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'success', // 'success', 'confirm', 'warning', 'error', 'info'
    validator: (value) => ['success', 'confirm', 'warning', 'error', 'info'].includes(value)
  },
  showConfirm: {
    type: Boolean,
    default: false
  },
  confirmText: {
    type: String,
    default: 'Confirmar'
  },
  cancelText: {
    type: String,
    default: 'Cancelar'
  }
});

defineEmits(['close', 'confirm']);
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.6));
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999 !important;
  padding: 1rem;
  animation: overlay-appear 0.3s ease-out;
}

@keyframes overlay-appear {
  0% {
    background: rgba(0, 0, 0, 0);
    backdrop-filter: blur(0px);
  }
  100% {
    background: linear-gradient(135deg, rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.6));
    backdrop-filter: blur(8px);
  }
}

.modal-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
  box-shadow: 
    0 20px 40px -12px rgba(0, 0, 0, 0.25),
    0 8px 32px -8px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(255, 255, 255, 0.2);
  max-width: 520px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid rgba(255, 255, 255, 0.3);
  position: relative;
}

/* Tamaño compacto para modales de información */
.modal-container.compact {
  max-width: 280px;
  border-radius: 12px;
}

.modal-container.compact .modal-header {
  padding: 0.75rem 1rem 0 1rem;
}

.modal-container.compact .modal-body {
  padding: 0.75rem 1rem;
}

.modal-container.compact .modal-footer {
  padding: 0 1rem 1rem 1rem;
}

.modal-container.compact .modal-title {
  font-size: 0.875rem;
}

.modal-container.compact .btn {
  padding: 0.5rem 1rem;
  font-size: 0.75rem;
}

/* Ajustes para modales compactos sin header */
.modal-container.compact .modal-body:first-child {
  padding-top: 1rem;
}

/* Tamaño compacto para modales de confirmación */
.modal-container.compact-confirm {
  max-width: 420px;
  border-radius: 14px;
}

.modal-container.compact-confirm .modal-header {
  padding: 1rem 1.5rem 0 1.5rem;
}

.modal-container.compact-confirm .modal-body {
  padding: 1rem 1.5rem;
}

.modal-container.compact-confirm .modal-footer {
  padding: 0 1.5rem 1.5rem 1.5rem;
}

.modal-container.compact-confirm .modal-title {
  font-size: 1rem;
}

.modal-container.compact-confirm .btn {
  padding: 0.7rem 1.2rem;
  font-size: 0.85rem;
}

.modal-container.compact-confirm .confirm-icon > div {
  width: 12rem;
  height: 3rem;
  margin-bottom: 1rem;
}

.modal-container.compact-confirm .confirm-icon svg {
  width: 1.5rem;
  height: 1.5rem;
}

.modal-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 60%;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.3) 0%,
    rgba(255, 255, 255, 0.1) 50%,
    transparent 100%
  );
  border-radius: 16px 16px 0 0;
  pointer-events: none;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 2rem 0 2rem;
  position: relative;
  z-index: 1;
}

.modal-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}

.modal-close {
  color: #6b7280;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(229, 231, 235, 0.8);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.modal-close:hover {
  background: rgba(249, 250, 251, 0.9);
  border-color: rgba(209, 213, 219, 0.8);
  transform: scale(1.05);
}

.modal-body {
  padding: 1.5rem 2rem;
  text-align: center;
  position: relative;
  z-index: 1;
}

.confirm-icon,
.success-icon,
.warning-icon,
.error-icon {
  margin-bottom: 1rem;
}

.modal-message {
  color: #374151;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}

.modal-footer {
  padding: 0 2rem 2rem 2rem;
  position: relative;
  z-index: 1;
}

.btn {
  padding: 0.875rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  position: relative;
  overflow: hidden;
}

.btn::before {
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

.btn:hover::before {
  left: 100%;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

/* Estilo específico para modal de entrada */
.modal-container[data-modal-type="entrada"] .btn-primary {
  background: linear-gradient(135deg, rgb(30, 144, 255) 0%, rgb(25, 118, 210) 100%) !important;
  box-shadow: 0 4px 12px rgba(30, 144, 255, 0.3) !important;
}

/* Estilo específico para modal de salida */
.modal-container[data-modal-type="salida"] .btn-primary {
  background: linear-gradient(135deg, rgb(220, 20, 60) 0%, rgb(180, 15, 50) 100%) !important;
  box-shadow: 0 4px 12px rgba(220, 20, 60, 0.3) !important;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
  transform: translateY(-1px);
}

/* Hover específico para modal de entrada */
.modal-container[data-modal-type="entrada"] .btn-primary:hover {
  background: linear-gradient(135deg, rgb(25, 118, 210) 0%, rgb(21, 101, 192) 100%) !important;
  box-shadow: 0 6px 20px rgba(30, 144, 255, 0.4) !important;
  transform: translateY(-1px);
}

/* Hover específico para modal de salida */
.modal-container[data-modal-type="salida"] .btn-primary:hover {
  background: linear-gradient(135deg, rgb(200, 15, 55) 0%, rgb(160, 10, 45) 100%) !important;
  box-shadow: 0 6px 20px rgba(220, 20, 60, 0.4) !important;
  transform: translateY(-1px);
}

.btn-primary:active {
  transform: translateY(0px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-secondary {
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  color: #374151;
  border: 1px solid rgba(209, 213, 219, 0.8);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.btn-secondary:hover {
  background: linear-gradient(135deg, #e5e7eb 0%, #d1d5db 100%);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  transform: translateY(-1px);
}

.btn-secondary:active {
  transform: translateY(0px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.flex {
  display: flex;
}

.flex-1 {
  flex: 1;
}

.gap-3 {
  gap: 0.75rem;
}

.w-full {
  width: 100%;
}

/* Animaciones mejoradas */
.modal-enter-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-leave-active {
  transition: all 0.3s ease-in;
}

.modal-enter-from {
  opacity: 0;
  transform: scale(0.8) translateY(20px);
}

.modal-leave-to {
  opacity: 0;
  transform: scale(0.9) translateY(-10px);
}

.modal-enter-to,
.modal-leave-from {
  opacity: 1;
  transform: scale(1) translateY(0);
}

/* Responsive mejorado */
@media (max-width: 480px) {
  .modal-container {
    max-width: calc(100% - 1rem);
    margin: 0 0.5rem;
    border-radius: 12px;
  }
  
  .modal-header,
  .modal-body,
  .modal-footer {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
  
  .modal-header {
    padding-top: 1.25rem;
  }
  
  .modal-body {
    padding-top: 1.25rem;
    padding-bottom: 1.25rem;
  }
  
  .modal-footer {
    padding-bottom: 1.5rem;
  }
  
  .modal-title {
    font-size: 1rem;
  }
  
  .btn {
    padding: 0.75rem 1.25rem;
    font-size: 0.8rem;
  }
  
  .modal-message {
    font-size: 0.875rem;
  }
}

/* Efectos adicionales para elementos interactivos */
.group:hover .group-hover\:text-gray-500 {
  color: #6b7280;
}

/* Animación sutil para los iconos de estado */
.confirm-icon > div,
.success-icon > div,
.warning-icon > div,
.error-icon > div {
  animation: pulse-soft 2s ease-in-out infinite;
}

@keyframes pulse-soft {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.9;
  }
}

/* Mejoras para mejor contraste y legibilidad */
.modal-message h3 {
  color: #111827;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.modal-message p {
  color: #4b5563;
  margin-bottom: 0.5rem;
}

.modal-message .bg-green-50,
.modal-message .bg-red-50,
.modal-message .bg-blue-50,
.modal-message .bg-yellow-50 {
  border-radius: 8px;
}

/* Estilos especiales para los badges de información */
.modal-message .border-l-4 {
  border-left-width: 4px;
}

.modal-message .border-green-400 {
  border-color: #34d399;
}

.modal-message .border-red-400 {
  border-color: #f87171;
}
</style>
