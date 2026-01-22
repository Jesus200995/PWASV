<template>
  <div class="relative w-9 h-9 flex items-center justify-center mr-3">
    <!-- Círculo solo contorno verde neón -->
    <div class="plant-icon-container w-full h-full rounded-full flex items-center justify-center">
      <!-- SVG de plantita/brote -->
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        class="w-5 h-5 plant-grow absolute"
        fill="none"
      >
        <!-- Tallo principal -->
        <path 
          d="M12 22V13" 
          stroke="#22c55e" 
          stroke-width="2.5" 
          stroke-linecap="round"
          class="stem-grow"
        />
        <!-- Hoja izquierda -->
        <path 
          d="M12 16C8.5 16 6 13.5 6 10C9.5 10 12 12.5 12 16Z" 
          fill="none"
          stroke="#22c55e"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="leaf-left"
        />
        <!-- Hoja derecha superior -->
        <path 
          d="M12 11C15.5 11 18 8.5 18 5C14.5 5 12 7.5 12 11Z" 
          fill="none"
          stroke="#22c55e"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="leaf-right"
        />
      </svg>
      
      <!-- Flor girando (aparece cuando la planta desaparece) -->
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        class="w-5 h-5 flower-spin absolute"
        fill="none"
      >
        <!-- Pétalos de la flor -->
        <circle cx="12" cy="12" r="2.5" fill="#fbbf24" class="flower-center"/>
        <circle cx="12" cy="7" r="3.5" fill="#22c55e" opacity="0.8" class="petal"/>
        <circle cx="17" cy="12" r="3.5" fill="#22c55e" opacity="0.8" class="petal"/>
        <circle cx="12" cy="17" r="3.5" fill="#22c55e" opacity="0.8" class="petal"/>
        <circle cx="7" cy="12" r="3.5" fill="#22c55e" opacity="0.8" class="petal"/>
        <circle cx="15" cy="9" r="2.8" fill="#10b981" opacity="0.7" class="petal"/>
        <circle cx="15" cy="15" r="2.8" fill="#10b981" opacity="0.7" class="petal"/>
        <circle cx="9" cy="15" r="2.8" fill="#10b981" opacity="0.7" class="petal"/>
        <circle cx="9" cy="9" r="2.8" fill="#10b981" opacity="0.7" class="petal"/>
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

/* Animación de crecimiento de la planta */
@keyframes plant-grow {
  0% {
    transform: scale(0.3) translateY(8px);
    opacity: 0;
  }
  30% {
    transform: scale(0.6) translateY(4px);
    opacity: 0.5;
  }
  60% {
    transform: scale(1.05) translateY(0);
    opacity: 1;
  }
  80% {
    transform: scale(0.98) translateY(0);
    opacity: 1;
  }
  100% {
    transform: scale(1) translateY(0);
    opacity: 1;
  }
}

@keyframes stem-grow {
  0% {
    stroke-dasharray: 15;
    stroke-dashoffset: 15;
    opacity: 0;
  }
  40% {
    stroke-dasharray: 15;
    stroke-dashoffset: 0;
    opacity: 1;
  }
  100% {
    stroke-dasharray: 15;
    stroke-dashoffset: 0;
    opacity: 1;
  }
}

@keyframes leaf-appear {
  0%, 40% {
    opacity: 0;
    transform: scale(0) rotate(-20deg);
  }
  70% {
    opacity: 1;
    transform: scale(1.1) rotate(5deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

.plant-grow {
  animation: plant-grow 4.5s ease-in-out infinite alternate;
  transform-origin: center bottom;
}

.stem-grow {
  animation: stem-grow 4.5s ease-in-out infinite alternate;
}

.leaf-left {
  animation: leaf-appear 4.5s ease-in-out infinite alternate;
  animation-delay: 0.6s;
  transform-origin: right center;
}

.leaf-right {
  animation: leaf-appear 4.5s ease-in-out infinite alternate;
  animation-delay: 0.9s;
  transform-origin: left bottom;
}

/* Animación de flor girando */
@keyframes flower-spin-rotate {
  0% {
    transform: rotate(0deg) scale(0);
    opacity: 0;
  }
  40% {
    transform: rotate(0deg) scale(0);
    opacity: 0;
  }
  50% {
    transform: rotate(180deg) scale(1);
    opacity: 1;
  }
  90% {
    transform: rotate(540deg) scale(1);
    opacity: 1;
  }
  100% {
    transform: rotate(720deg) scale(0);
    opacity: 0;
  }
}

.flower-spin {
  animation: flower-spin-rotate 4.5s ease-in-out infinite alternate-reverse;
  transform-origin: center;
}

.flower-center {
  animation: pulse 1s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}
</style>
