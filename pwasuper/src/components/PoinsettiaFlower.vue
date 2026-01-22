<template>
  <div class="relative w-9 h-9 flex items-center justify-center mr-3">
    <!-- Círculo solo contorno verde neón -->
    <div class="plant-icon-container w-full h-full rounded-full flex items-center justify-center">
      <!-- SVG de plantita/brote - sin xmlns para evitar requests externos -->
      <svg
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
          class="stem-shine"
        />
        <!-- Hoja izquierda -->
        <path 
          d="M12 16C8.5 16 6 13.5 6 10C9.5 10 12 12.5 12 16Z" 
          fill="none"
          stroke="#22c55e"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="leaf-left-shine"
        />
        <!-- Hoja derecha superior -->
        <path 
          d="M12 11C15.5 11 18 8.5 18 5C14.5 5 12 7.5 12 11Z" 
          fill="none"
          stroke="#22c55e"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="leaf-right-shine"
        />
      </svg>
    </div>
    
    <!-- Efecto de brillo ocasional -->
    <div class="absolute inset-0 rounded-full plant-glow-pulse pointer-events-none"></div>
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

/* Animación de brillo suave línea por línea */
@keyframes stem-shine {
  0%, 70% {
    filter: brightness(1) drop-shadow(0 0 1px rgba(34, 197, 94, 0.2));
  }
  75% {
    filter: brightness(1.6) drop-shadow(0 0 6px rgba(34, 197, 94, 0.9)) drop-shadow(0 0 10px rgba(16, 185, 129, 0.6));
  }
  80%, 100% {
    filter: brightness(1) drop-shadow(0 0 1px rgba(34, 197, 94, 0.2));
  }
}

@keyframes leaf-left-shine {
  0%, 75% {
    filter: brightness(1) drop-shadow(0 0 1px rgba(34, 197, 94, 0.2));
  }
  82% {
    filter: brightness(1.6) drop-shadow(0 0 6px rgba(34, 197, 94, 0.9)) drop-shadow(0 0 10px rgba(16, 185, 129, 0.6));
  }
  87%, 100% {
    filter: brightness(1) drop-shadow(0 0 1px rgba(34, 197, 94, 0.2));
  }
}

@keyframes leaf-right-shine {
  0%, 82% {
    filter: brightness(1) drop-shadow(0 0 1px rgba(34, 197, 94, 0.2));
  }
  89% {
    filter: brightness(1.6) drop-shadow(0 0 6px rgba(34, 197, 94, 0.9)) drop-shadow(0 0 10px rgba(16, 185, 129, 0.6));
  }
  94%, 100% {
    filter: brightness(1) drop-shadow(0 0 1px rgba(34, 197, 94, 0.2));
  }
}

@keyframes glow-pulse {
  0%, 70% {
    box-shadow: 0 0 3px rgba(34, 197, 94, 0.15);
  }
  75% {
    box-shadow: 0 0 10px rgba(34, 197, 94, 0.6), 0 0 18px rgba(16, 185, 129, 0.4);
  }
  89% {
    box-shadow: 0 0 12px rgba(34, 197, 94, 0.7), 0 0 20px rgba(16, 185, 129, 0.5);
  }
  94%, 100% {
    box-shadow: 0 0 3px rgba(34, 197, 94, 0.15);
  }
}

.stem-shine {
  animation: stem-shine 5s ease-in-out infinite;
}

.leaf-left-shine {
  animation: leaf-left-shine 5s ease-in-out infinite;
}

.leaf-right-shine {
  animation: leaf-right-shine 5s ease-in-out infinite;
}

.plant-glow-pulse {
  animation: glow-pulse 5s ease-in-out infinite;
}
</style>
