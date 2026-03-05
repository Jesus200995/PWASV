// ========================================
// COMPOSABLE PARA ANIMACIÓN DE NÚMEROS APPLE-STYLE
// Técnica: requestAnimationFrame + easing suave
// ========================================

import { ref, watch } from 'vue';

/**
 * Función de easing suave (ease-out cubic, como Apple)
 * @param {number} t - Progress 0-1
 * @returns {number} Eased value
 */
function easeOutCubic(t) {
  return 1 - Math.pow(1 - t, 3);
}

/**
 * Composable para animar números con transición suave Apple-style
 * @param {Ref} targetValue - Valor objetivo (reactivo)
 * @param {Object} options - Opciones de animación
 * @returns {Object} - displayValue y controles
 */
export function useAnimatedNumber(targetValue, options = {}) {
  const {
    duration = 800, // Duración en ms (Apple usa ~800ms para transiciones)
    easing = easeOutCubic,
    decimals = 0,
    onComplete = null
  } = options;

  const displayValue = ref(0);
  let animationFrameId = null;
  let startValue = 0;
  let startTime = null;

  /**
   * Cancela la animación en progreso
   */
  const cancelAnimation = () => {
    if (animationFrameId) {
      cancelAnimationFrame(animationFrameId);
      animationFrameId = null;
      startTime = null;
    }
  };

  /**
   * Función de animación con requestAnimationFrame
   */
  const animate = (currentTime) => {
    if (!startTime) startTime = currentTime;
    
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    // Aplicar easing
    const easedProgress = easing(progress);
    
    // Calcular valor actual
    const currentValue = startValue + (targetValue.value - startValue) * easedProgress;
    
    // Actualizar displayValue con decimales apropiados
    displayValue.value = decimals > 0 
      ? parseFloat(currentValue.toFixed(decimals))
      : Math.round(currentValue);
    
    // Continuar animación o completar
    if (progress < 1) {
      animationFrameId = requestAnimationFrame(animate);
    } else {
      displayValue.value = targetValue.value; // Asegurar valor exacto al final
      animationFrameId = null;
      startTime = null;
      
      if (onComplete) {
        onComplete();
      }
    }
  };

  /**
   * Inicia la animación hacia el nuevo valor
   */
  const animateTo = (newValue) => {
    // Cancelar animación anterior
    cancelAnimation();
    
    // Si los valores son iguales, no animar
    if (displayValue.value === newValue) {
      return;
    }
    
    startValue = displayValue.value;
    animationFrameId = requestAnimationFrame(animate);
  };

  /**
   * Establece el valor inmediatamente sin animación
   */
  const setValue = (newValue) => {
    cancelAnimation();
    displayValue.value = newValue;
  };

  // Watch para cambios en targetValue
  watch(targetValue, (newValue, oldValue) => {
    // Si el displayValue actual es 0, establecer directo sin animación (entrada inicial)
    // Esto evita la animación de "0 a X" al cargar la página
    if (displayValue.value === 0) {
      displayValue.value = newValue;
      return;
    }
    // Solo animar si el valor es diferente
    if (newValue === displayValue.value) {
      return;
    }
    animateTo(newValue);
  }, { immediate: true });

  return {
    displayValue,
    animateTo,
    setValue,
    cancelAnimation
  };
}

/**
 * Composable simplificado para múltiples contadores
 * @param {Object} targets - Objeto con valores objetivo reactivos
 * @param {Object} options - Opciones globales
 * @returns {Object} - Objeto con displayValues
 */
export function useAnimatedCounters(targets, options = {}) {
  const counters = {};
  const displayValues = {};

  Object.keys(targets).forEach(key => {
    const { displayValue } = useAnimatedNumber(targets[key], options);
    counters[key] = displayValue;
    displayValues[key] = displayValue;
  });

  return displayValues;
}

/**
 * Formatea número con separadores de miles (estilo Apple)
 * @param {number} num - Número a formatear
 * @returns {string} - Número formateado
 */
export function formatNumber(num) {
  return new Intl.NumberFormat('es-MX').format(num);
}

/**
 * Formatea número con animación de entrada (scale + fade)
 * Retorna clases CSS para aplicar
 * @param {boolean} isChanging - Si el valor está cambiando
 * @returns {string} - Clases CSS
 */
export function getCounterClasses(isChanging) {
  return isChanging ? 'counter-updating' : '';
}
