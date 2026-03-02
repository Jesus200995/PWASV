<template>
  <div class="apple-firma-container">
    <div class="apple-firma-header">
      <label class="apple-firma-label">
        {{ label }}
      </label>
      <p class="apple-firma-hint">Firmar con el mouse, trackpad o dedo</p>
    </div>
    
    <div 
      class="apple-firma-canvas-wrapper"
      :class="hayFirma ? 'apple-firma-signed' : 'apple-firma-unsigned'"
    >
      <canvas
        ref="canvas"
        :width="canvasWidth"
        :height="canvasHeight"
        class="apple-firma-canvas"
        @mousedown="iniciarFirma"
        @mousemove="dibujarFirma"
        @mouseup="finalizarFirma"
        @mouseleave="finalizarFirma"
        @touchstart="iniciarFirmaTouch"
        @touchmove="dibujarFirmaTouch"
        @touchend="finalizarFirma"
      />
    </div>
    
    <!-- Indicador de estado de firma -->
    <div class="apple-firma-footer">
      <div class="apple-firma-status">
        <div 
          class="apple-status-dot"
          :class="hayFirma ? 'apple-dot-active' : 'apple-dot-inactive'"
        ></div>
        <span class="apple-status-text" :class="hayFirma ? 'apple-text-active' : 'apple-text-inactive'">
          {{ hayFirma ? 'Firmado' : 'Sin firmar' }}
        </span>
      </div>
      <button
        @click="limpiarFirma"
        type="button"
        class="apple-clear-btn"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
        </svg>
        <span>Limpiar</span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FirmaDigital',
  props: {
    label: {
      type: String,
      default: 'Firma Digital'
    }
  },
  data() {
    return {
      isDrawing: false,
      hayFirma: false,
      canvasWidth: 800,
      canvasHeight: 300
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.ajustarCanvas();
      window.addEventListener('resize', this.ajustarCanvas);
    });
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.ajustarCanvas);
  },
  methods: {
    ajustarCanvas() {
      const canvas = this.$refs.canvas;
      if (!canvas) return;
      
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      
      // Ajustar canvas a su tamaño visual con alta resolución
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      
      // Actualizar data
      this.canvasWidth = canvas.width;
      this.canvasHeight = canvas.height;
      
      const ctx = canvas.getContext('2d');
      ctx.scale(dpr, dpr);
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.lineWidth = 3;
      ctx.strokeStyle = '#1f2937';
    },
    iniciarFirma(e) {
      this.isDrawing = true;
      if (!this.hayFirma) {
        this.hayFirma = true;
        this.$emit('firmado');
      }
      const canvas = this.$refs.canvas;
      const rect = canvas.getBoundingClientRect();
      const ctx = canvas.getContext('2d');
      
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      ctx.beginPath();
      ctx.moveTo(x, y);
    },
    
    dibujarFirma(e) {
      if (!this.isDrawing) return;
      
      const canvas = this.$refs.canvas;
      const rect = canvas.getBoundingClientRect();
      const ctx = canvas.getContext('2d');
      
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      ctx.lineTo(x, y);
      ctx.stroke();
    },
    
    iniciarFirmaTouch(e) {
      e.preventDefault();
      this.isDrawing = true;
      if (!this.hayFirma) {
        this.hayFirma = true;
        this.$emit('firmado');
      }
      
      const canvas = this.$refs.canvas;
      const rect = canvas.getBoundingClientRect();
      const ctx = canvas.getContext('2d');
      const touch = e.touches[0];
      
      const x = touch.clientX - rect.left;
      const y = touch.clientY - rect.top;
      
      ctx.beginPath();
      ctx.moveTo(x, y);
    },
    
    dibujarFirmaTouch(e) {
      e.preventDefault();
      if (!this.isDrawing) return;
      
      const canvas = this.$refs.canvas;
      const rect = canvas.getBoundingClientRect();
      const ctx = canvas.getContext('2d');
      const touch = e.touches[0];
      
      const x = touch.clientX - rect.left;
      const y = touch.clientY - rect.top;
      
      ctx.lineTo(x, y);
      ctx.stroke();
    },
    
    finalizarFirma() {
      this.isDrawing = false;
    },
    
    limpiarFirma() {
      this.ajustarCanvas();
      this.hayFirma = false;
      this.$emit('borrado');
    },
    
    obtenerFirmaBase64() {
      const canvas = this.$refs.canvas;
      return canvas.toDataURL('image/png');
    },
    
    // Método para verificar si hay firma válida
    tieneFirma() {
      return this.hayFirma;
    }
  }
};
</script>

<style scoped>
.apple-firma-container {
  width: 100%;
  max-width: 100%;
}

.apple-firma-header {
  margin-bottom: 1rem;
  padding: 0 0.5rem;
}

@media (max-width: 480px) {
  .apple-firma-header {
    padding: 0 0.25rem;
  }
}

.apple-firma-label {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
  font-size: 0.875rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
  display: block;
  margin-bottom: 0.375rem;
}

.apple-firma-hint {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.75rem;
  color: rgba(0, 0, 0, 0.5);
  margin: 0;
}

.apple-firma-canvas-wrapper {
  position: relative;
  width: 100%;
  min-height: 220px;
  border-radius: 14px;
  overflow: hidden;
  background: #ffffff;
  transition: all 0.3s cubic-bezier(0.32, 0.72, 0, 1);
}

.apple-firma-unsigned {
  border: 2px dashed rgba(0, 0, 0, 0.15);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.apple-firma-unsigned:hover {
  border-color: rgba(59, 130, 246, 0.4);
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.12);
}

.apple-firma-signed {
  border: 2px solid rgba(16, 185, 129, 0.4);
  box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15);
}

.apple-firma-canvas {
  display: block;
  width: 100%;
  min-height: 220px;
  cursor: crosshair;
  touch-action: none;
  background: #ffffff;
}

.apple-firma-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 0.875rem;
  padding: 0 0.5rem;
}

@media (max-width: 480px) {
  .apple-firma-footer {
    padding: 0 0.25rem;
  }
}

.apple-firma-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.apple-status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  transition: all 0.3s cubic-bezier(0.32, 0.72, 0, 1);
}

.apple-dot-active {
  background: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
}

.apple-dot-inactive {
  background: rgba(0, 0, 0, 0.2);
}

.apple-status-text {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.8125rem;
  transition: all 0.3s cubic-bezier(0.32, 0.72, 0, 1);
}

.apple-text-active {
  color: #059669;
  font-weight: 600;
}

.apple-text-inactive {
  color: rgba(0, 0, 0, 0.5);
  font-weight: 500;
}

.apple-clear-btn {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 0.875rem;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #ef4444;
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.32, 0.72, 0, 1);
}

.apple-clear-btn:hover {
  background: rgba(239, 68, 68, 0.15);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
}

.apple-clear-btn:active {
  transform: translateY(0);
}

/* Responsive */
@media (max-width: 768px) {
  .apple-firma-canvas-wrapper {
    border-radius: 12px;
    min-height: 200px;
  }
  
  .apple-firma-canvas {
    min-height: 200px;
  }
  
  .apple-firma-label {
    font-size: 0.8125rem;
  }
  
  .apple-firma-hint {
    font-size: 0.6875rem;
  }
  
  .apple-clear-btn {
    padding: 0.4375rem 0.75rem;
    font-size: 0.75rem;
  }
}

@media (min-width: 769px) {
  .apple-firma-canvas-wrapper {
    min-height: 190px;
  }
  
  .apple-firma-canvas {
    min-height: 190px;
  }
}

@media (min-width: 1024px) {
  .apple-firma-canvas-wrapper {
    min-height: 200px;
  }
  
  .apple-firma-canvas {
    min-height: 200px;
  }
}
</style>
