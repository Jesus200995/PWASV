<template>
  <div class="w-full">
    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700 mb-2">
        {{ label }}
      </label>
      <p class="text-xs text-gray-500 mb-2">Firmar con el mouse o dedo</p>
    </div>
    
    <div 
      class="border-2 rounded-lg overflow-hidden bg-white transition-colors"
      :class="hayFirma ? 'border-green-400 border-solid' : 'border-dashed border-gray-300 hover:border-blue-400'"
    >
      <canvas
        ref="canvas"
        :width="canvasWidth"
        :height="canvasHeight"
        class="w-full cursor-crosshair bg-white"
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
    <div class="flex items-center justify-between mt-2">
      <div class="flex items-center gap-1.5">
        <div 
          class="w-2 h-2 rounded-full"
          :class="hayFirma ? 'bg-green-500' : 'bg-gray-300'"
        ></div>
        <span class="text-xs" :class="hayFirma ? 'text-green-600 font-medium' : 'text-gray-500'">
          {{ hayFirma ? 'Firmado' : 'Sin firmar' }}
        </span>
      </div>
      <button
        @click="limpiarFirma"
        type="button"
        class="px-3 py-1.5 text-xs font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
      >
        Limpiar
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
      canvasWidth: 600,
      canvasHeight: 200
    };
  },
  mounted() {
    this.$nextTick(() => {
      const canvas = this.$refs.canvas;
      if (canvas) {
        // Ajustar resolución del canvas
        const rect = canvas.getBoundingClientRect();
        const ctx = canvas.getContext('2d');
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#1f2937';
      }
    });
  },
  methods: {
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
canvas {
  display: block;
  touch-action: none;
}
</style>
