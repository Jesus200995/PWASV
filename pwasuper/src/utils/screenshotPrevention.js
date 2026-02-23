/**
 * Sistema de Prevención de Capturas de Pantalla para PWA
 * Implementa múltiples capas de protección:
 * 1. Bloqueo de combinaciones de teclas
 * 2. Desactivación de clic derecho
 * 3. Marca de agua dinámica
 * 4. Detección de cambio de foco
 * 5. Modo seguro CSS
 */

class ScreenshotPrevention {
  constructor() {
    this.isEnabled = false;
    this.watermarkElement = null;
    this.userName = '';
    this.userId = '';
  }

  /**
   * Inicializa el sistema de prevención
   */
  init(userData = {}) {
    if (this.isEnabled) return;
    
    this.userName = userData.nombre || 'Usuario';
    this.userId = userData.id || '';
    
    this.preventRightClick();
    this.preventKeyboardShortcuts();
    this.preventDevTools();
    this.addWatermark();
    this.preventScreenCapture();
    this.addSecureStyles();
    
    this.isEnabled = true;
    console.log('🔒 Sistema de prevención de capturas activado');
  }

  /**
   * Desactiva el clic derecho en toda la aplicación
   */
  preventRightClick() {
    document.addEventListener('contextmenu', (e) => {
      e.preventDefault();
      this.showWarning('Acción no permitida por seguridad');
      return false;
    }, false);
  }

  /**
   * Bloquea combinaciones de teclas para captura de pantalla
   */
  preventKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      // Bloquear Print Screen
      if (e.key === 'PrintScreen') {
        e.preventDefault();
        this.showWarning('Las capturas de pantalla están deshabilitadas');
        // Limpiar el clipboard
        this.clearClipboard();
        return false;
      }

      // Bloquear combinaciones comunes de captura
      const blockedCombinations = [
        // Windows: Win + Shift + S, Win + Print Screen
        (e.metaKey || e.key === 'Meta') && e.shiftKey && e.key === 's',
        (e.metaKey || e.key === 'Meta') && e.key === 'PrintScreen',
        
        // Mac: Cmd + Shift + 3, Cmd + Shift + 4, Cmd + Shift + 5
        e.metaKey && e.shiftKey && ['3', '4', '5'].includes(e.key),
        
        // Chrome DevTools (Ctrl+Shift+I, F12, Ctrl+Shift+J, Ctrl+Shift+C)
        (e.ctrlKey && e.shiftKey && ['I', 'J', 'C'].includes(e.key.toUpperCase())),
        e.key === 'F12',
        
        // Guardar página (Ctrl+S)
        e.ctrlKey && e.key.toLowerCase() === 's',
        
        // Ver código fuente (Ctrl+U)
        e.ctrlKey && e.key.toLowerCase() === 'u'
      ];

      if (blockedCombinations.some(combo => combo)) {
        e.preventDefault();
        e.stopPropagation();
        this.showWarning('Combinación de teclas deshabilitada por seguridad');
        return false;
      }
    }, true);

    // Bloquear eventos de tecla en window
    window.addEventListener('keyup', (e) => {
      if (e.key === 'PrintScreen') {
        this.clearClipboard();
      }
    }, false);
  }

  /**
   * Prevenir apertura de DevTools
   */
  preventDevTools() {
    // Detectar si DevTools está abierto (cambio de tamaño de ventana)
    const threshold = 160;
    let devtoolsOpen = false;

    const detectDevTools = () => {
      const widthThreshold = window.outerWidth - window.innerWidth > threshold;
      const heightThreshold = window.outerHeight - window.innerHeight > threshold;
      
      if (widthThreshold || heightThreshold) {
        if (!devtoolsOpen) {
          devtoolsOpen = true;
          this.handleDevToolsOpen();
        }
      } else {
        devtoolsOpen = false;
      }
    };

    window.addEventListener('resize', detectDevTools);
    setInterval(detectDevTools, 1000);

    // Prevenir debugger
    setInterval(() => {
      const before = new Date();
      debugger;
      const after = new Date();
      if (after - before > 100) {
        this.handleDevToolsOpen();
      }
    }, 1000);
  }

  /**
   * Maneja cuando se detecta que DevTools está abierto
   */
  handleDevToolsOpen() {
    // Opcional: Redirigir o mostrar advertencia
    console.log('⚠️ Herramientas de desarrollo detectadas');
    // document.body.style.filter = 'blur(10px)';
  }

  /**
   * Limpia el clipboard para evitar capturas
   */
  clearClipboard() {
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText('').catch(() => {});
      }
    } catch (err) {
      // Silencioso
    }
  }

  /**
   * Agrega marca de agua dinámica
   */
  addWatermark() {
    // Crear elemento de marca de agua
    this.watermarkElement = document.createElement('div');
    this.watermarkElement.id = 'security-watermark';
    
    const now = new Date();
    const timestamp = now.toLocaleString('es-MX');
    
    this.watermarkElement.innerHTML = `
      <div class="watermark-item">${this.userName}</div>
      <div class="watermark-item">ID: ${this.userId}</div>
      <div class="watermark-item">${timestamp}</div>
    `;
    
    document.body.appendChild(this.watermarkElement);

    // Actualizar timestamp cada minuto
    setInterval(() => {
      const now = new Date();
      const items = this.watermarkElement.querySelectorAll('.watermark-item');
      if (items[2]) {
        items[2].textContent = now.toLocaleString('es-MX');
      }
    }, 60000);
  }

  /**
   * Previene captura de pantalla desenFOCANDO al cambiar de ventana
   */
  preventScreenCapture() {
    let blurTimeout;

    // Detectar cuando la ventana pierde foco
    window.addEventListener('blur', () => {
      // Opcional: Desenfocar contenido sensible
      blurTimeout = setTimeout(() => {
        document.body.classList.add('security-blur');
      }, 100);
    });

    window.addEventListener('focus', () => {
      clearTimeout(blurTimeout);
      document.body.classList.remove('security-blur');
    });

    // Detectar cambio de visibilidad de la página
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        document.body.classList.add('security-blur');
      } else {
        document.body.classList.remove('security-blur');
      }
    });
  }

  /**
   * Agrega estilos CSS de seguridad
   */
  addSecureStyles() {
    const style = document.createElement('style');
    style.textContent = `
      /* Prevenir selección de texto */
      body {
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
        user-select: none !important;
        -webkit-touch-callout: none !important;
      }

      /* Permitir selección en inputs y textareas */
      input, textarea, [contenteditable="true"] {
        -webkit-user-select: text !important;
        -moz-user-select: text !important;
        -ms-user-select: text !important;
        user-select: text !important;
      }

      /* Marca de agua */
      #security-watermark {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-45deg);
        pointer-events: none;
        z-index: 999999;
        opacity: 0.08;
        font-size: 24px;
        font-weight: bold;
        color: #000000;
        text-align: center;
        line-height: 1.8;
        white-space: nowrap;
        font-family: Arial, sans-serif;
        text-shadow: 0 0 2px rgba(255,255,255,0.5);
      }

      .watermark-item {
        margin: 5px 0;
      }

      /* Blur de seguridad cuando pierde foco */
      body.security-blur > *:not(#security-watermark) {
        filter: blur(20px) !important;
        transition: filter 0.2s ease;
      }

      /* Prevenir arrastrar imágenes */
      img {
        -webkit-user-drag: none;
        -khtml-user-drag: none;
        -moz-user-drag: none;
        -o-user-drag: none;
        user-drag: none;
        pointer-events: none;
      }

      /* Prevenir copia de imágenes */
      img::selection {
        background: transparent;
      }
    `;
    
    document.head.appendChild(style);
  }

  /**
   * Muestra advertencia visual
   */
  showWarning(message) {
    // Crear toast de advertencia
    const warning = document.createElement('div');
    warning.className = 'screenshot-warning';
    warning.textContent = message;
    warning.style.cssText = `
      position: fixed;
      top: 20px;
      left: 50%;
      transform: translateX(-50%);
      background: #f44336;
      color: white;
      padding: 12px 24px;
      border-radius: 8px;
      z-index: 1000000;
      font-size: 14px;
      font-weight: 600;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      animation: slideDown 0.3s ease;
    `;

    // Agregar animación
    if (!document.querySelector('#screenshot-warning-styles')) {
      const animStyle = document.createElement('style');
      animStyle.id = 'screenshot-warning-styles';
      animStyle.textContent = `
        @keyframes slideDown {
          from {
            transform: translateX(-50%) translateY(-100px);
            opacity: 0;
          }
          to {
            transform: translateX(-50%) translateY(0);
            opacity: 1;
          }
        }
      `;
      document.head.appendChild(animStyle);
    }

    document.body.appendChild(warning);

    // Remover después de 3 segundos
    setTimeout(() => {
      warning.style.animation = 'slideDown 0.3s ease reverse';
      setTimeout(() => warning.remove(), 300);
    }, 3000);
  }

  /**
   * Desactiva el sistema de prevención
   */
  disable() {
    this.isEnabled = false;
    if (this.watermarkElement) {
      this.watermarkElement.remove();
    }
    document.body.classList.remove('security-blur');
    console.log('🔓 Sistema de prevención desactivado');
  }
}

// Exportar instancia singleton
const screenshotPrevention = new ScreenshotPrevention();
export default screenshotPrevention;
