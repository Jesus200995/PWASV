<template>
  <div class="relative w-8 h-8 sm:w-8 sm:h-8 md:w-8 md:h-8 flex items-center justify-center mr-3">
    <!-- SVG de la Flor de Noche Buena (Poinsettia) girando -->
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 100 100"
      class="w-full h-full animate-spin-slow"
    >
      <!-- Pétalos VERDES externos (más grandes) - Noche Buena Verde -->
      <ellipse cx="50" cy="22" rx="14" ry="20" fill="#22c55e" opacity="0.95" transform="rotate(0 50 50)" />
      <ellipse cx="50" cy="22" rx="14" ry="20" fill="#16a34a" opacity="0.90" transform="rotate(72 50 50)" />
      <ellipse cx="50" cy="22" rx="14" ry="20" fill="#22c55e" opacity="0.95" transform="rotate(144 50 50)" />
      <ellipse cx="50" cy="22" rx="14" ry="20" fill="#16a34a" opacity="0.90" transform="rotate(216 50 50)" />
      <ellipse cx="50" cy="22" rx="14" ry="20" fill="#22c55e" opacity="0.95" transform="rotate(288 50 50)" />

      <!-- Pétalos ROJOS internos pequeños (muy poco rojo) con baja opacidad -->
      <ellipse cx="50" cy="28" rx="11" ry="16" fill="#dc2626" opacity="0.35" transform="rotate(36 50 50)" />
      <ellipse cx="50" cy="28" rx="11" ry="16" fill="#ef4444" opacity="0.30" transform="rotate(108 50 50)" />
      <ellipse cx="50" cy="28" rx="11" ry="16" fill="#dc2626" opacity="0.35" transform="rotate(180 50 50)" />
      <ellipse cx="50" cy="28" rx="11" ry="16" fill="#ef4444" opacity="0.30" transform="rotate(252 50 50)" />
      <ellipse cx="50" cy="28" rx="11" ry="16" fill="#dc2626" opacity="0.35" transform="rotate(324 50 50)" />

      <!-- Hojas verdes medianas complementarias -->
      <ellipse cx="50" cy="32" rx="8" ry="13" fill="#15803d" opacity="0.85" transform="rotate(18 50 50)" />
      <ellipse cx="50" cy="32" rx="8" ry="13" fill="#166534" opacity="0.80" transform="rotate(90 50 50)" />
      <ellipse cx="50" cy="32" rx="8" ry="13" fill="#15803d" opacity="0.85" transform="rotate(162 50 50)" />
      <ellipse cx="50" cy="32" rx="8" ry="13" fill="#166534" opacity="0.80" transform="rotate(234 50 50)" />
      <ellipse cx="50" cy="32" rx="8" ry="13" fill="#15803d" opacity="0.85" transform="rotate(306 50 50)" />

      <!-- Centro amarillo dorado -->
      <circle cx="50" cy="50" r="9" fill="#FFD700" opacity="0.95" />
      <circle cx="50" cy="50" r="7" fill="#FFC700" opacity="0.9" />

      <!-- Pequeños pétalos internos amarillo-naranja para textura -->
      <circle cx="50" cy="42" r="2" fill="#FF8C00" opacity="0.7" />
      <circle cx="56" cy="46" r="2" fill="#FF8C00" opacity="0.7" />
      <circle cx="56" cy="54" r="2" fill="#FF8C00" opacity="0.7" />
      <circle cx="50" cy="58" r="2" fill="#FF8C00" opacity="0.7" />
      <circle cx="44" cy="54" r="2" fill="#FF8C00" opacity="0.7" />
      <circle cx="44" cy="46" r="2" fill="#FF8C00" opacity="0.7" />

      <!-- Brillo en el centro -->
      <circle cx="50" cy="48" r="3" fill="#FFFF00" opacity="0.6" />
    </svg>

    <!-- Efecto de sombra sutil -->
    <div class="absolute inset-0 rounded-full shadow-lg pointer-events-none"></div>
  </div>
</template>

<script setup>
// El componente solo necesita presentar la flor giratoria
// No requiere lógica adicional
</script>

<style scoped>
@keyframes spin-slow {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin-slow {
  animation: spin-slow 8s linear infinite;
}
</style>
