<template>
  <div class="relative w-9 h-9 flex items-center justify-center mr-3">
    <!-- Círculo solo contorno verde neón -->
    <div class="plant-icon-container w-full h-full rounded-full flex items-center justify-center">
      <!-- SVG de plantita/brote -->
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        class="w-5 h-5"
        fill="none"
      >
        <!-- Tallo principal -->
        <path 
          d="M12 22V13" 
          stroke="#22c55e" 
          stroke-width="2.5" 
          stroke-linecap="round"
        />
        <!-- Hoja izquierda -->
        <path 
          d="M12 16C8.5 16 6 13.5 6 10C9.5 10 12 12.5 12 16Z" 
          fill="none"
          stroke="#22c55e"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
        <!-- Hoja derecha superior -->
        <path 
          d="M12 11C15.5 11 18 8.5 18 5C14.5 5 12 7.5 12 11Z" 
          fill="none"
          stroke="#22c55e"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </div>
    
    <!-- Efecto de brillo neón animado -->
    <div class="absolute inset-0 rounded-full neon-glow pointer-events-none"></div>
  </div>
</template>

<script setup>
// Componente de icono de plantita con efecto neón (solo contorno)
</script>

<style scoped>
.plant-icon-container {
  background: #ffffff;
  border: 3px solid #86efac;
  box-shadow: none;
}

.neon-glow {
  border: 2px solid transparent;
  box-shadow: none;
}

@keyframes neon-pulse {
  0%, 100% {
    box-shadow: 
      0 0 4px #ffffff,
      0 0 8px rgba(255, 255, 255, 0.3);
  }
  50% {
    box-shadow: 
      0 0 8px #f3f4f6,
      0 0 16px rgba(243, 244, 246, 0.5);
  }
}
</style>
