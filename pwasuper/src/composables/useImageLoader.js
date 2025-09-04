/**
 * Composable para optimizar la carga de imágenes críticas
 * Proporciona funcionalidades de preload, caching y estados de carga
 */

import { ref, onMounted } from 'vue';

export function useImageLoader(imageSrc, options = {}) {
  const imageLoading = ref(true);
  const imageError = ref(false);
  const imageRef = ref(null);
  
  const {
    preload = true,
    eager = true,
    timeout = 5000,
    fallbackSrc = null
  } = options;

  // Función para precargar imagen
  function preloadImage(src) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      
      // Configurar timeout
      const timeoutId = setTimeout(() => {
        reject(new Error('Timeout loading image'));
      }, timeout);
      
      img.onload = () => {
        clearTimeout(timeoutId);
        resolve(img);
      };
      
      img.onerror = () => {
        clearTimeout(timeoutId);
        reject(new Error('Error loading image'));
      };
      
      // Configurar atributos para optimización
      if (eager) {
        img.loading = 'eager';
        img.fetchPriority = 'high';
      }
      
      img.src = src;
    });
  }

  // Función para manejar carga de imagen
  async function loadImage() {
    try {
      imageLoading.value = true;
      imageError.value = false;
      
      // Si ya está en el DOM y cargada, no hacer nada
      if (imageRef.value?.complete && imageRef.value?.naturalHeight !== 0) {
        imageLoading.value = false;
        return;
      }
      
      if (preload) {
        await preloadImage(imageSrc);
      }
      
      imageLoading.value = false;
    } catch (error) {
      console.warn('Error loading image:', error);
      imageError.value = true;
      imageLoading.value = false;
      
      // Intentar cargar imagen de fallback si está disponible
      if (fallbackSrc && imageSrc !== fallbackSrc) {
        try {
          await preloadImage(fallbackSrc);
        } catch (fallbackError) {
          console.warn('Error loading fallback image:', fallbackError);
        }
      }
    }
  }

  // Handlers para eventos del DOM
  function handleImageLoad() {
    imageLoading.value = false;
    imageError.value = false;
  }

  function handleImageError() {
    imageError.value = true;
    imageLoading.value = false;
  }

  // Auto-cargar cuando se monta el componente
  onMounted(() => {
    loadImage();
  });

  // Función para forzar recarga
  function reloadImage() {
    loadImage();
  }

  return {
    imageLoading,
    imageError,
    imageRef,
    handleImageLoad,
    handleImageError,
    reloadImage,
    loadImage
  };
}

// Composable específico para el logo de la aplicación
export function useAppLogo() {
  return useImageLoader('/src/images/icono.png', {
    preload: true,
    eager: true,
    timeout: 3000,
    fallbackSrc: '/pwa-192x192.png' // Usar el ícono PWA como fallback
  });
}

// Función para precargar múltiples imágenes críticas
export function preloadCriticalImages(imageSources = []) {
  const promises = imageSources.map(src => {
    const img = new Image();
    img.loading = 'eager';
    img.fetchPriority = 'high';
    
    return new Promise((resolve) => {
      img.onload = resolve;
      img.onerror = resolve; // No fallar si una imagen no carga
      img.src = src;
    });
  });
  
  return Promise.allSettled(promises);
}

// Función para cachear imágenes en el service worker
export async function cacheImages(imageSources = []) {
  if ('serviceWorker' in navigator && 'caches' in window) {
    try {
      const cache = await caches.open('images-cache-v1');
      const cachePromises = imageSources.map(async (src) => {
        try {
          const response = await fetch(src);
          if (response.ok) {
            await cache.put(src, response);
            console.log(`✅ Imagen cacheada: ${src}`);
          }
        } catch (error) {
          console.warn(`⚠️ Error cacheando imagen ${src}:`, error);
        }
      });
      
      await Promise.allSettled(cachePromises);
    } catch (error) {
      console.warn('Error accediendo al cache:', error);
    }
  }
}
