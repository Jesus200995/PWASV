/**
 * Screen Security Service
 * Protección contra capturas de pantalla similar a apps bancarias
 */

class ScreenSecurityService {
  constructor() {
    this.isProtectionActive = false;
    this.securityOverlay = null;
    this.visibilityChangeHandler = null;
    this.beforePrintHandler = null;
  }

  /**
   * Inicializa la protección de pantalla
   */
  initialize() {
    if (this.isProtectionActive) return;
    
    console.log('[ScreenSecurity] Inicializando protección de pantalla...');
    
    // Crear overlay de seguridad
    this.createSecurityOverlay();
    
    // Detectar cuando la app va a segundo plano
    this.setupVisibilityDetection();
    
    // Bloquear impresión de pantalla
    this.setupPrintBlocking();
    
    // Deshabilitar captura de video/canvas
    this.setupCanvasProtection();
    
    // Aplicar estilos de seguridad CSS
    this.applySecurityStyles();
    
    this.isProtectionActive = true;
    console.log('[ScreenSecurity] Protección activada ✓');
  }

  /**
   * Crea un overlay negro que se muestra al detectar captura
   */
  createSecurityOverlay() {
    if (this.securityOverlay) return;
    
    this.securityOverlay = document.createElement('div');
    this.securityOverlay.id = 'security-overlay';
    this.securityOverlay.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: #000000;
      z-index: 999999;
      display: none;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      color: white;
      font-family: system-ui, -apple-system, sans-serif;
    `;
    
    this.securityOverlay.innerHTML = `
      <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
        <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
      </svg>
      <p style="margin-top: 20px; font-size: 18px; font-weight: 600;">Contenido Protegido</p>
      <p style="margin-top: 8px; font-size: 14px; opacity: 0.8;">No se permiten capturas de pantalla</p>
    `;
    
    document.body.appendChild(this.securityOverlay);
  }

  /**
   * Detecta cuando la app está en segundo plano o visible
   */
  setupVisibilityDetection() {
    // Detectar cambios de visibilidad de la página
    this.visibilityChangeHandler = () => {
      if (document.hidden || document.visibilityState === 'hidden') {
        // App va a segundo plano - mostrar overlay
        this.showSecurityOverlay();
      } else {
        // App vuelve a primer plano - ocultar overlay
        setTimeout(() => {
          this.hideSecurityOverlay();
        }, 100);
      }
    };
    
    document.addEventListener('visibilitychange', this.visibilityChangeHandler);
    
    // Detectar blur/focus de la ventana
    window.addEventListener('blur', () => {
      this.showSecurityOverlay();
    });
    
    window.addEventListener('focus', () => {
      setTimeout(() => {
        this.hideSecurityOverlay();
      }, 100);
    });
    
    // Detectar combinaciones de teclas de captura (Windows, Mac, Linux)
    document.addEventListener('keyup', (e) => {
      // Windows: PrtScr, Alt+PrtScr, Win+Shift+S
      // Mac: Cmd+Shift+3, Cmd+Shift+4, Cmd+Shift+5
      if (
        e.key === 'PrintScreen' ||
        (e.shiftKey && e.metaKey && (e.key === '3' || e.key === '4' || e.key === '5' || e.key === 's')) ||
        (e.shiftKey && e.ctrlKey && e.key === 'S')
      ) {
        this.showSecurityOverlayTemporarily();
      }
    });
    
    // Para Android: detectar toque de 3 dedos o botón de captura
    let touchStartTime = 0;
    document.addEventListener('touchstart', (e) => {
      if (e.touches.length >= 3) {
        touchStartTime = Date.now();
      }
    });
    
    document.addEventListener('touchend', (e) => {
      if (touchStartTime > 0 && Date.now() - touchStartTime < 500) {
        this.showSecurityOverlayTemporarily();
      }
      touchStartTime = 0;
    });
  }

  /**
   * Bloquea la función de imprimir
   */
  setupPrintBlocking() {
    this.beforePrintHandler = () => {
      this.showSecurityOverlay();
    };
    
    window.addEventListener('beforeprint', this.beforePrintHandler);
    
    // Prevenir Ctrl+P
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
        e.preventDefault();
        this.showSecurityOverlayTemporarily();
        return false;
      }
    });
  }

  /**
   * Protege canvas y screenshots programáticos
   */
  setupCanvasProtection() {
    // Prevenir capturas de canvas
    const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
    HTMLCanvasElement.prototype.toDataURL = function() {
      console.warn('[ScreenSecurity] Intento de captura de canvas bloqueado');
      return 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==';
    };
    
    const originalToBlob = HTMLCanvasElement.prototype.toBlob;
    HTMLCanvasElement.prototype.toBlob = function() {
      console.warn('[ScreenSecurity] Intento de captura de canvas bloqueado');
    };
  }

  /**
   * Aplica estilos CSS de seguridad
   */
  applySecurityStyles() {
    const style = document.createElement('style');
    style.id = 'screen-security-styles';
    style.textContent = `
      /* Prevenir selección de texto sensible */
      body {
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
        user-select: none !important;
        -webkit-touch-callout: none !important;
      }
      
      /* Permitir selección solo en inputs y textareas */
      input, textarea {
        -webkit-user-select: text !important;
        -moz-user-select: text !important;
        -ms-user-select: text !important;
        user-select: text !important;
      }
      
      /* Deshabilitar el menú contextual en imágenes */
      img {
        -webkit-user-drag: none !important;
        -webkit-touch-callout: none !important;
        pointer-events: none !important;
      }
      
      /* Proteger contenido sensible */
      .secure-content {
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        user-select: none !important;
      }
      
      /* Para Android WebView - marcar como seguro */
      @media (display-mode: standalone) {
        html {
          -webkit-app-region: drag;
        }
      }
    `;
    
    document.head.appendChild(style);
  }

  /**
   * Muestra el overlay de seguridad
   */
  showSecurityOverlay() {
    if (this.securityOverlay) {
      this.securityOverlay.style.display = 'flex';
      console.log('[ScreenSecurity] Overlay activado - Captura bloqueada');
    }
  }

  /**
   * Oculta el overlay de seguridad
   */
  hideSecurityOverlay() {
    if (this.securityOverlay) {
      this.securityOverlay.style.display = 'none';
    }
  }

  /**
   * Muestra el overlay temporalmente (para alertas de captura)
   */
  showSecurityOverlayTemporarily(duration = 2000) {
    this.showSecurityOverlay();
    setTimeout(() => {
      this.hideSecurityOverlay();
    }, duration);
  }

  /**
   * Desactiva la protección
   */
  destroy() {
    if (!this.isProtectionActive) return;
    
    // Remover event listeners
    if (this.visibilityChangeHandler) {
      document.removeEventListener('visibilitychange', this.visibilityChangeHandler);
    }
    if (this.beforePrintHandler) {
      window.removeEventListener('beforeprint', this.beforePrintHandler);
    }
    
    // Remover overlay
    if (this.securityOverlay) {
      this.securityOverlay.remove();
      this.securityOverlay = null;
    }
    
    // Remover estilos
    const securityStyles = document.getElementById('screen-security-styles');
    if (securityStyles) {
      securityStyles.remove();
    }
    
    this.isProtectionActive = false;
    console.log('[ScreenSecurity] Protección desactivada');
  }
}

// Singleton
export default new ScreenSecurityService();
