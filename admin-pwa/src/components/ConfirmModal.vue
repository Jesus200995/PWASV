<template>
  <Teleport to="body">
    <div v-if="show" class="confirm-modal-overlay" @click="cancel">
      <div class="confirm-modal" @click.stop>
        <div class="modal-header">
          <div class="modal-icon" :class="iconClass">
            <component :is="iconComponent" />
          </div>
          <h3>{{ title }}</h3>
        </div>
        
        <div class="modal-body">
          <p>{{ message }}</p>
        </div>
        
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
    default: 'warning', // warning, danger, info
    validator: (value) => ['warning', 'danger', 'info'].includes(value)
  }
})

const emit = defineEmits(['confirm', 'cancel'])

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

const iconComponent = computed(() => {
  const icons = {
    warning: 'ExclamationTriangleIcon',
    danger: 'ExclamationTriangleIcon',
    info: 'InformationCircleIcon'
  }
  return icons[props.type]
})

const confirm = () => {
  emit('confirm')
}

const cancel = () => {
  emit('cancel')
}

// Componentes de iconos inline
const ExclamationTriangleIcon = {
  template: `
    <svg viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"/>
    </svg>
  `
}

const InformationCircleIcon = {
  template: `
    <svg viewBox="0 0 24 24" fill="currentColor">
      <path d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm8.706-1.442c1.146-.573 2.437.463 2.126 1.706l-.709 2.836.042-.02a.75.75 0 01.67 1.34l-.04.022c-1.147.573-2.438-.463-2.127-1.706l.71-2.836-.042.02a.75.75 0 11-.671-1.34l.041-.022zM12 9a.75.75 0 100-1.5.75.75 0 000 1.5z"/>
    </svg>
  `
}
</script>

<style scoped>
.confirm-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  padding: 20px;
  animation: overlayFadeIn 0.3s ease-out;
}

.confirm-modal {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  max-width: 400px;
  width: 100%;
  animation: modalSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes overlayFadeIn {
  from { opacity: 0; backdrop-filter: blur(0px); }
  to { opacity: 1; backdrop-filter: blur(8px); }
}

@keyframes modalSlideIn {
  from { opacity: 0; transform: scale(0.8) translateY(30px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

.modal-header {
  padding: 30px 30px 20px;
  text-align: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.modal-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: iconPulse 2s ease-in-out infinite;
}

.modal-icon svg {
  width: 28px;
  height: 28px;
  color: white;
}

.warning-icon {
  background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
}

.danger-icon {
  background: linear-gradient(135deg, #F44336 0%, #D32F2F 100%);
}

.info-icon {
  background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
}

@keyframes iconPulse {
  0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 152, 0, 0.4); }
  50% { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(255, 152, 0, 0); }
}

.modal-header h3 {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #333;
}

.modal-body {
  padding: 20px 30px;
  text-align: center;
}

.modal-body p {
  margin: 0;
  font-size: 16px;
  color: #555;
  line-height: 1.5;
}

.modal-actions {
  padding: 20px 30px 30px;
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-cancel,
.btn-confirm {
  flex: 1;
  padding: 12px 20px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 120px;
}

.btn-cancel {
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  color: #666;
  border: 2px solid rgba(0, 0, 0, 0.1);
}

.btn-cancel:hover {
  background: linear-gradient(135deg, #eeeeee 0%, #d5d5d5 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.warning-btn {
  background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 152, 0, 0.3);
}

.warning-btn:hover {
  background: linear-gradient(135deg, #F57C00 0%, #EF6C00 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 152, 0, 0.4);
}

.danger-btn {
  background: linear-gradient(135deg, #F44336 0%, #D32F2F 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.3);
}

.danger-btn:hover {
  background: linear-gradient(135deg, #D32F2F 0%, #B71C1C 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(244, 67, 54, 0.4);
}

.info-btn {
  background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
}

.info-btn:hover {
  background: linear-gradient(135deg, #1976D2 0%, #1565C0 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(33, 150, 243, 0.4);
}

@media (max-width: 480px) {
  .confirm-modal {
    margin: 10px;
    border-radius: 16px;
  }
  
  .modal-header {
    padding: 24px 20px 16px;
  }
  
  .modal-actions {
    padding: 16px 20px 24px;
    flex-direction: column;
  }
}
</style>
