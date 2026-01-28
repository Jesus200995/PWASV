<template>
  <div class="firma-digital-container">
    <div class="firma-label-container">
      <label class="firma-label">
        {{ label }}
      </label>
      <p class="firma-instrucciones">Use el mouse o dedo para firmar en el recuadro</p>
    </div>
    
    <div 
      class="firma-canvas-wrapper"
      :class="{ 'has-firma': hayFirma }"
    >
      <canvas
        ref="canvas"
        :width="canvasWidth"
        :height="canvasHeight"
        class="firma-canvas"
        @mousedown="iniciarFirma"
        @mousemove="dibujarFirma"
        @mouseup="finalizarFirma"
        @mouseleave="finalizarFirma"
        @touchstart="iniciarFirmaTouch"
        @touchmove="dibujarFirmaTouch"
        @touchend="finalizarFirma"
      />
      <div v-if="!hayFirma" class="firma-placeholder">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M12 19l7-7 3 3-7 7-3-3z"/>
          <path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/>
          <path d="M2 2l7.586 7.586"/>
        </svg>
        <span>Firme aquí</span>
      </div>
    </div>
    
    <!-- Indicador de estado de firma -->
    <div class="firma-footer">
      <div class="firma-estado">
        <div 
          class="firma-estado-indicator"
          :class="{ 'firmado': hayFirma }"
        ></div>
        <span class="firma-estado-text" :class="{ 'firmado': hayFirma }">
          {{ hayFirma ? '✓ Firma realizada' : 'Sin firmar' }}
        </span>
      </div>
      <button
        @click="limpiarFirma"
        type="button"
        class="firma-btn-limpiar"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
        </svg>
        Limpiar
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FirmaDigitalAdmin',
  props: {
    label: {
      type: String,
      default: 'Firma del Supervisor'
    }
  },
  data() {
    return {
      isDrawing: false,
      hayFirma: false,
      canvasWidth: 500,
      canvasHeight: 150
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.inicializarCanvas();
    });
  },
  methods: {
    inicializarCanvas() {
      const canvas = this.$refs.canvas;
      if (canvas) {
        const ctx = canvas.getContext('2d');
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#1f2937';
      }
    },
    
    iniciarFirma(e) {
      this.isDrawing = true;
      this.hayFirma = true;
      const canvas = this.$refs.canvas;
      const rect = canvas.getBoundingClientRect();
      const ctx = canvas.getContext('2d');
      
      const x = (e.clientX - rect.left) * (canvas.width / rect.width);
      const y = (e.clientY - rect.top) * (canvas.height / rect.height);
      
      ctx.beginPath();
      ctx.moveTo(x, y);
    },
    
    dibujarFirma(e) {
      if (!this.isDrawing) return;
      
      const canvas = this.$refs.canvas;
      const rect = canvas.getBoundingClientRect();
      const ctx = canvas.getContext('2d');
      
      const x = (e.clientX - rect.left) * (canvas.width / rect.width);
      const y = (e.clientY - rect.top) * (canvas.height / rect.height);
      
      ctx.lineTo(x, y);
      ctx.stroke();
    },
    
    iniciarFirmaTouch(e) {
      e.preventDefault();
      this.isDrawing = true;
      this.hayFirma = true;
      
      const canvas = this.$refs.canvas;
      const rect = canvas.getBoundingClientRect();
      const ctx = canvas.getContext('2d');
      const touch = e.touches[0];
      
      const x = (touch.clientX - rect.left) * (canvas.width / rect.width);
      const y = (touch.clientY - rect.top) * (canvas.height / rect.height);
      
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
      
      const x = (touch.clientX - rect.left) * (canvas.width / rect.width);
      const y = (touch.clientY - rect.top) * (canvas.height / rect.height);
      
      ctx.lineTo(x, y);
      ctx.stroke();
    },
    
    finalizarFirma() {
      this.isDrawing = false;
    },
    
    limpiarFirma() {
      const canvas = this.$refs.canvas;
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      this.hayFirma = false;
      this.$emit('firma-limpiada');
    },
    
    obtenerFirmaBase64() {
      const canvas = this.$refs.canvas;
      return canvas.toDataURL('image/png');
    },
    
    tieneFirma() {
      return this.hayFirma;
    },
    
    // Reinicializar el canvas (útil cuando se abre un modal)
    reinicializar() {
      this.$nextTick(() => {
        this.limpiarFirma();
        this.inicializarCanvas();
      });
    }
  }
};
</script>

<style scoped>
.firma-digital-container {
  width: 100%;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.firma-label-container {
  margin-bottom: 12px;
}

.firma-label {
  display: block;
  font-size: 0.9rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 4px;
}

.firma-instrucciones {
  font-size: 0.8rem;
  color: #6b7280;
  margin: 0;
}

.firma-canvas-wrapper {
  position: relative;
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  overflow: hidden;
  background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%);
  transition: all 0.3s ease;
  min-height: 160px;
}

.firma-canvas-wrapper:hover {
  border-color: #22c55e;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
}

.firma-canvas-wrapper.has-firma {
  border-style: solid;
  border-color: #22c55e;
  background: white;
  box-shadow: 0 2px 8px rgba(34, 197, 94, 0.15);
}

.firma-canvas {
  display: block;
  width: 100%;
  height: 160px;
  cursor: crosshair;
  background: transparent;
  touch-action: none;
}

.firma-placeholder {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #9ca3af;
  pointer-events: none;
  transition: opacity 0.2s;
}

.firma-placeholder svg {
  opacity: 0.5;
}

.firma-placeholder span {
  font-size: 0.85rem;
  font-weight: 500;
}

.firma-canvas-wrapper:hover .firma-placeholder {
  color: #16a34a;
}

.firma-canvas-wrapper:hover .firma-placeholder svg {
  opacity: 0.7;
}

.firma-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e5e7eb;
}

.firma-estado {
  display: flex;
  align-items: center;
  gap: 8px;
}

.firma-estado-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #d1d5db;
  transition: all 0.3s ease;
}

.firma-estado-indicator.firmado {
  background: #22c55e;
  box-shadow: 0 0 8px rgba(34, 197, 94, 0.4);
}

.firma-estado-text {
  font-size: 0.85rem;
  color: #6b7280;
  font-weight: 500;
  transition: color 0.2s;
}

.firma-estado-text.firmado {
  color: #16a34a;
  font-weight: 600;
}

.firma-btn-limpiar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  font-size: 0.8rem;
  font-weight: 500;
  color: #6b7280;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
}

.firma-btn-limpiar:hover {
  background: #fee2e2;
  border-color: #fca5a5;
  color: #dc2626;
}

.firma-btn-limpiar svg {
  transition: color 0.2s;
}

.firma-btn-limpiar:hover svg {
  color: #dc2626;
}
</style>
