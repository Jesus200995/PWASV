<template>
  <Teleport to="body">
    <div v-if="show" class="confirm-modal-overlay" @click="cancel">
      <div class="confirm-modal" :class="modalClass" @click.stop>
        <!-- Icono principal -->
        <div class="modal-icon-container">
          <div class="modal-icon" :class="iconClass">
            <svg v-if="type === 'danger'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              <line x1="10" y1="11" x2="10" y2="17"/>
              <line x1="14" y1="11" x2="14" y2="17"/>
            </svg>
            <svg v-else-if="type === 'warning'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="7 10 12 15 17 10"/>
              <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
          </div>
        </div>

        <!-- Título -->
        <h3 class="modal-title">{{ cleanTitle }}</h3>
        
        <!-- Cuerpo del mensaje -->
        <div class="modal-body">
          <p class="modal-description" v-html="formattedMessage"></p>
        </div>
        
        <!-- Botones -->
        <div class="modal-actions">
          <button @click="cancel" class="btn-cancel">
            {{ cancelText }}
          </button>
          <button @click="confirm" class="btn-confirm" :class="confirmClass">
            {{ confirmText }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Confirmar acción'
  },
  message: {
    type: String,
    required: true
  },
  confirmText: {
    type: String,
    default: 'Aceptar'
  },
  cancelText: {
    type: String,
    default: 'Cancelar'
  },
  type: {
    type: String,
    default: 'warning',
    validator: (value) => ['warning', 'danger', 'info'].includes(value)
  }
})

const emit = defineEmits(['confirm', 'cancel'])

// Limpiar el título de emojis
const cleanTitle = computed(() => {
  return props.title.replace(/[⚠️🗑️❌⚡]/g, '').trim()
})

// Formatear el mensaje para mejor visualización
const formattedMessage = computed(() => {
  let msg = props.message
  
  // Convertir bullets a lista HTML
  if (msg.includes('•')) {
    const parts = msg.split(/(?=•)/)
    let result = ''
    let listItems = []
    
    parts.forEach(part => {
      if (part.startsWith('•')) {
        listItems.push(part.replace('•', '').trim())
      } else {
        if (listItems.length > 0) {
          result += '<ul class="warning-list">' + listItems.map(item => `<li>${item}</li>`).join('') + '</ul>'
          listItems = []
        }
        result += `<p>${part.trim()}</p>`
      }
    })
    
    if (listItems.length > 0) {
      result += '<ul class="warning-list">' + listItems.map(item => `<li>${item}</li>`).join('') + '</ul>'
    }
    
    return result
  }
  
  return msg
})

const modalClass = computed(() => `modal-${props.type}`)

const iconClass = computed(() => {
  const classes = {
    warning: 'warning-icon',
    danger: 'danger-icon',
    info: 'info-icon'
  }
  return classes[props.type]
})

const confirmClass = computed(() => {
  const classes = {
    warning: 'warning-btn',
    danger: 'danger-btn',
    info: 'info-btn'
  }
  return classes[props.type]
})

const confirm = () => {
  emit('confirm')
}

const cancel = () => {
  emit('cancel')
}
</script>

<style scoped>
.confirm-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(6px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  padding: 20px;
  animation: overlayFadeIn 0.25s ease-out;
}

.confirm-modal {
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
  max-width: 420px;
  width: 100%;
  animation: modalSlideIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  overflow: hidden;
}

@keyframes overlayFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes modalSlideIn {
  from { opacity: 0; transform: scale(0.9) translateY(20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

/* Icon Container */
.modal-icon-container {
  padding: 24px 24px 0;
  display: flex;
  justify-content: center;
}

.modal-icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-icon svg {
  width: 28px;
  height: 28px;
}

.warning-icon {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #d97706;
  border: 2px solid #fbbf24;
}

.danger-icon {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #dc2626;
  border: 2px solid #f87171;
}

.info-icon {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #2563eb;
  border: 2px solid #60a5fa;
}

/* Title */
.modal-title {
  margin: 16px 24px 0;
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  text-align: center;
  font-family: 'Inter', -apple-system, sans-serif;
}

.modal-danger .modal-title {
  color: #991b1b;
}

/* Body */
.modal-body {
  padding: 16px 24px 20px;
  text-align: center;
}

.modal-description {
  margin: 0;
  font-size: 14px;
  color: #4b5563;
  line-height: 1.6;
  font-family: 'Inter', -apple-system, sans-serif;
}

.modal-description :deep(p) {
  margin: 0 0 12px 0;
}

.modal-description :deep(p:last-child) {
  margin-bottom: 0;
}

.modal-description :deep(strong) {
  color: #1f2937;
  font-weight: 600;
}

.modal-description :deep(.warning-list) {
  list-style: none;
  padding: 0;
  margin: 12px 0;
  background: #f9fafb;
  border-radius: 10px;
  padding: 12px 16px;
  text-align: left;
}

.modal-description :deep(.warning-list li) {
  padding: 6px 0;
  padding-left: 24px;
  position: relative;
  font-size: 13px;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
}

.modal-description :deep(.warning-list li:last-child) {
  border-bottom: none;
}

.modal-description :deep(.warning-list li::before) {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 6px;
  height: 6px;
  background: #ef4444;
  border-radius: 50%;
}

.modal-danger .modal-description :deep(.warning-list) {
  background: #fef2f2;
  border: 1px solid #fecaca;
}

.modal-warning .modal-description :deep(.warning-list li::before) {
  background: #f59e0b;
}

.modal-info .modal-description :deep(.warning-list) {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
}

.modal-info .modal-description :deep(.warning-list li::before) {
  background: #3b82f6;
}

/* Actions */
.modal-actions {
  padding: 0 24px 24px;
  display: flex;
  gap: 12px;
}

.btn-cancel,
.btn-confirm {
  flex: 1;
  padding: 12px 20px;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Inter', -apple-system, sans-serif;
}

.btn-cancel {
  background: #f3f4f6;
  color: #4b5563;
  border: 1px solid #e5e7eb;
}

.btn-cancel:hover {
  background: #e5e7eb;
  transform: translateY(-1px);
}

.warning-btn {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
}

.warning-btn:hover {
  background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(217, 119, 6, 0.3);
}

.danger-btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

.danger-btn:hover {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.info-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.info-btn:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

@media (max-width: 480px) {
  .confirm-modal {
    margin: 16px;
  }
  
  .modal-actions {
    flex-direction: column-reverse;
  }
}
</style>
