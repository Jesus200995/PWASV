<template>
  <div class="w-full">
    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700 mb-2">
        {{ label }}
      </label>
      <p class="text-xs text-gray-500 mb-2">Firmar con el mouse o dedo</p>
    </div>
    
    <div class="border-2 border-dashed border-gray-300 rounded-lg overflow-hidden bg-white hover:border-blue-400 transition-colors">
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
    
    <div class="flex gap-2 mt-3">
      <button
        @click="limpiarFirma"
        type="button"
        class="flex-1 px-3 py-2 text-sm font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 rounded-lg transition-colors"
      >
        Limpiar
      </button>
      <button
        @click="descargarFirma"
        type="button"
        :disabled="!hayFirma"
        class="flex-1 px-3 py-2 text-sm font-medium text-white bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed rounded-lg transition-colors"
      >
        Descargar
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
    
    descargarFirma() {
      const canvas = this.$refs.canvas;
      const link = document.createElement('a');
      link.href = canvas.toDataURL('image/png');
      link.download = `firma_${new Date().getTime()}.png`;
      link.click();
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
