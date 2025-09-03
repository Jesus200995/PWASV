<template>
  <div class="sidebar">
    <!-- Efecto liquid glass background -->
    <div class="sidebar-header">
      <div class="header-content">
        <!-- Animación de flor elegante flotante -->
        <div class="flower-animation">
          <svg class="flower-icon" viewBox="0 0 120 120" fill="none">
            <!-- Pétalos principales mejorados con animación verde -->
            <g class="petals-main">
              <!-- Pétalos exteriores grandes -->
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-1)" opacity="0.9" transform="rotate(0 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="0 60 60;10 60 60;0 60 60" dur="4s" repeatCount="indefinite"/>
              </path>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-2)" opacity="0.85" transform="rotate(36 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="36 60 60;46 60 60;36 60 60" dur="4.2s" repeatCount="indefinite"/>
              </path>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-1)" opacity="0.9" transform="rotate(72 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="72 60 60;82 60 60;72 60 60" dur="3.8s" repeatCount="indefinite"/>
              </path>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-2)" opacity="0.85" transform="rotate(108 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="108 60 60;118 60 60;108 60 60" dur="4.1s" repeatCount="indefinite"/>
              </path>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-1)" opacity="0.9" transform="rotate(144 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="144 60 60;154 60 60;144 60 60" dur="3.9s" repeatCount="indefinite"/>
              </path>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-2)" opacity="0.85" transform="rotate(180 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="180 60 60;190 60 60;180 60 60" dur="4.3s" repeatCount="indefinite"/>
              </path>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-1)" opacity="0.9" transform="rotate(216 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="216 60 60;226 60 60;216 60 60" dur="3.7s" repeatCount="indefinite"/>
              </path>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-2)" opacity="0.85" transform="rotate(252 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="252 60 60;262 60 60;252 60 60" dur="4.4s" repeatCount="indefinite"/>
              </path>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-1)" opacity="0.9" transform="rotate(288 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="288 60 60;298 60 60;288 60 60" dur="3.6s" repeatCount="indefinite"/>
              </path>
              <path d="M60 25 C50 30, 45 45, 60 55 C75 45, 70 30, 60 25 Z" fill="url(#petal-gradient-2)" opacity="0.85" transform="rotate(324 60 60)">
                <animateTransform attributeName="transform" type="rotate" values="324 60 60;334 60 60;324 60 60" dur="4.5s" repeatCount="indefinite"/>
              </path>
            </g>
            
            <!-- Pétalos internos más pequeños con pulsación -->
            <g class="petals-inner">
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(18 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="2.5s" repeatCount="indefinite"/>
              </ellipse>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(54 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="2.8s" repeatCount="indefinite"/>
              </ellipse>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(90 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="2.3s" repeatCount="indefinite"/>
              </ellipse>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(126 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="2.7s" repeatCount="indefinite"/>
              </ellipse>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(162 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="2.4s" repeatCount="indefinite"/>
              </ellipse>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(198 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="2.9s" repeatCount="indefinite"/>
              </ellipse>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(234 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="2.2s" repeatCount="indefinite"/>
              </ellipse>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(270 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="2.6s" repeatCount="indefinite"/>
              </ellipse>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(306 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="2.1s" repeatCount="indefinite"/>
              </ellipse>
              <ellipse cx="60" cy="40" rx="4" ry="12" fill="url(#inner-gradient)" opacity="0.8" transform="rotate(342 60 60)">
                <animate attributeName="opacity" values="0.8;0.5;0.8" dur="3.0s" repeatCount="indefinite"/>
              </ellipse>
            </g>
            
            <!-- Centro con múltiples capas verdes -->
            <circle cx="60" cy="60" r="10" fill="url(#center-gradient)" opacity="0.95">
              <animate attributeName="r" values="10;12;10" dur="3s" repeatCount="indefinite"/>
            </circle>
            <circle cx="60" cy="60" r="7" fill="url(#center-gradient-2)" opacity="0.9">
              <animate attributeName="r" values="7;9;7" dur="2.8s" repeatCount="indefinite"/>
            </circle>
            <circle cx="60" cy="60" r="4" fill="#66BB6A" opacity="0.8">
              <animate attributeName="r" values="4;6;4" dur="2.5s" repeatCount="indefinite"/>
            </circle>
            <circle cx="60" cy="60" r="2" fill="#A5D6A7" opacity="0.9">
              <animate attributeName="r" values="2;3;2" dur="2.2s" repeatCount="indefinite"/>
            </circle>
            
            <!-- Brillos dinámicos en el centro con efecto verde -->
            <circle cx="57" cy="57" r="1.5" fill="#E8F5E8" opacity="0.9">
              <animate attributeName="opacity" values="0.9;0.3;0.9" dur="1.8s" repeatCount="indefinite"/>
              <animate attributeName="r" values="1.5;2.5;1.5" dur="1.8s" repeatCount="indefinite"/>
            </circle>
            <circle cx="63" cy="62" r="1" fill="#F1F8E9" opacity="0.7">
              <animate attributeName="opacity" values="0.7;0.2;0.7" dur="2.3s" repeatCount="indefinite"/>
              <animate attributeName="r" values="1;1.8;1" dur="2.3s" repeatCount="indefinite"/>
            </circle>
            
            <!-- Definiciones de degradados verdes mejorados -->
            <defs>
              <linearGradient id="petal-gradient-1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#C8E6C9;stop-opacity:0.95" />
                <stop offset="30%" style="stop-color:#A5D6A7;stop-opacity:0.9" />
                <stop offset="70%" style="stop-color:#81C784;stop-opacity:0.8" />
                <stop offset="100%" style="stop-color:#66BB6A;stop-opacity:0.7" />
              </linearGradient>
              <linearGradient id="petal-gradient-2" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#E8F5E8;stop-opacity:0.9" />
                <stop offset="30%" style="stop-color:#C8E6C9;stop-opacity:0.85" />
                <stop offset="70%" style="stop-color:#A5D6A7;stop-opacity:0.75" />
                <stop offset="100%" style="stop-color:#81C784;stop-opacity:0.65" />
              </linearGradient>
              <linearGradient id="inner-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#F1F8E9;stop-opacity:0.9" />
                <stop offset="50%" style="stop-color:#E8F5E8;stop-opacity:0.7" />
                <stop offset="100%" style="stop-color:#C8E6C9;stop-opacity:0.5" />
              </linearGradient>
              <radialGradient id="center-gradient" cx="50%" cy="50%" r="50%">
                <stop offset="0%" style="stop-color:#A5D6A7;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#81C784;stop-opacity:0.95" />
                <stop offset="100%" style="stop-color:#66BB6A;stop-opacity:0.8" />
              </radialGradient>
              <radialGradient id="center-gradient-2" cx="50%" cy="50%" r="50%">
                <stop offset="0%" style="stop-color:#C8E6C9;stop-opacity:0.9" />
                <stop offset="100%" style="stop-color:#81C784;stop-opacity:0.7" />
              </radialGradient>
            </defs>
          </svg>
        </div>
        <div class="logo-text">
          <h1 class="brand-title">SEMBRANDO VIDA</h1>
          <p class="brand-subtitle">App de Seguimiento</p>
        </div>
      </div>
    </div>
      <!-- Botón para ir al geoportal -->
    <div class="geoportal-section">
      <a href="https://geoportal.sembrandodatos.com/" target="_blank" class="geoportal-btn">
        <div class="geoportal-icon-wrapper">
          <svg class="geoportal-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <path d="M2 12h20"/>
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
            <path d="M8 12c0-2.5 1.8-4.5 4-4.5s4 2 4 4.5-1.8 4.5-4 4.5-4-2-4-4.5"/>
          </svg>
        </div>
        <span class="geoportal-text">Geoportal</span>
        <div class="geoportal-glow"></div>
      </a>
      
      <!-- Botón para ir a la App Móvil -->
      <a href="https://app.sembrandodatos.com/login" target="_blank" class="mobile-app-btn">
        <div class="mobile-app-icon-wrapper">
          <svg class="mobile-app-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="5" y="2" width="14" height="20" rx="2" ry="2"/>
            <line x1="12" y1="18" x2="12.01" y2="18"/>
          </svg>
        </div>
        <span class="mobile-app-text">App Móvil</span>
        <div class="mobile-app-glow"></div>
      </a>
    </div>
      
      <nav class="sidebar-nav">
      <ul>
        <!-- Dashboard - OCULTO TEMPORALMENTE (NO ELIMINAR - Solo documentado para futura referencia)
        <li class="nav-item" :class="{ active: $route.name === 'Dashboard' }">
          <router-link to="/dashboard" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="7" height="9"/>
                <rect x="14" y="3" width="7" height="5"/>
                <rect x="14" y="12" width="7" height="9"/>
                <rect x="3" y="16" width="7" height="5"/>
              </svg>
            </div>
            <span class="nav-text">Dashboard</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
        -->
        
        <!-- Mapa Optimizado -->
        <li class="nav-item" :class="{ active: $route.name === 'VisorMap' }">
          <router-link to="/visor-map" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <!-- Ícono profesional de seguimiento GPS -->
                <circle cx="12" cy="12" r="8"/>
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 1v6"/>
                <path d="M12 17v6"/>
                <path d="M1 12h6"/>
                <path d="M17 12h6"/>
                <!-- Indicadores direccionales modernos -->
                <path d="M16.24 7.76l-2.12 2.12"/>
                <path d="M9.88 14.12l-2.12 2.12"/>
                <path d="M16.24 16.24l-2.12-2.12"/>
                <path d="M9.88 9.88l-2.12-2.12"/>
                <!-- Pulso de seguimiento -->
                <circle cx="12" cy="12" r="6" opacity="0.2" stroke-dasharray="2,2"/>
                <circle cx="12" cy="12" r="1.5" fill="currentColor" opacity="0.8"/>
              </svg>
            </div>
            <span class="nav-text">Visor de seguimiento</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
        
        <li class="nav-item" :class="{ active: $route.name === 'Asistencia' }">
          <router-link to="/asistencia" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <!-- Ícono profesional de check corporativo -->
                <path d="M9 11l3 3L22 4"/>
                <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
                <!-- Marco profesional -->
                <rect x="3" y="3" width="18" height="18" rx="3" opacity="0.1" fill="currentColor"/>
                <!-- Elementos decorativos empresariales -->
                <circle cx="7" cy="7" r="0.5" opacity="0.6"/>
                <circle cx="17" cy="7" r="0.5" opacity="0.6"/>
                <path d="M7 16h10" opacity="0.3" stroke-width="1.5"/>
                <path d="M7 19h6" opacity="0.2" stroke-width="1"/>
              </svg>
            </div>
            <span class="nav-text">Asistencia</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
        
        <li class="nav-item" :class="{ active: $route.name === 'Registros' }">
          <router-link to="/registros" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <!-- Ícono profesional de documentos empresariales -->
                <rect x="4" y="2" width="16" height="20" rx="3" ry="3" opacity="0.1" fill="currentColor"/>
                <path d="M14 2v6h6"/>
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/>
                <!-- Líneas de contenido profesionales -->
                <line x1="8" y1="13" x2="16" y2="13" stroke-width="1.5"/>
                <line x1="8" y1="16" x2="16" y2="16" stroke-width="1.5"/>
                <line x1="8" y1="19" x2="13" y2="19" stroke-width="1.5"/>
                <!-- Detalles corporativos -->
                <circle cx="10" cy="10" r="1" opacity="0.4" fill="currentColor"/>
                <rect x="12" y="9.5" width="3" height="1" rx="0.5" opacity="0.3" fill="currentColor"/>
              </svg>
            </div>
            <span class="nav-text">Registro de Actividades</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
        
        <li class="nav-item" :class="{ active: $route.name === 'Usuarios' }" v-if="isAdmin">
          <router-link to="/usuarios" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <!-- Ícono profesional de gestión de usuarios -->
                <circle cx="9" cy="7" r="4"/>
                <path d="M3 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2"/>
                <!-- Usuario adicional profesional -->
                <circle cx="16" cy="4" r="2"/>
                <path d="M20 8v2a2 2 0 0 1-2 2h-1"/>
                <!-- Elementos decorativos empresariales -->
                <rect x="17" y="11" width="4" height="2" rx="1" opacity="0.3" fill="currentColor"/>
                <circle cx="19" cy="17" r="1" opacity="0.2" fill="currentColor"/>
                <!-- Indicador de gestión -->
                <path d="M12 12h6" opacity="0.4" stroke-width="1.5"/>
                <path d="M15 9v6" opacity="0.3" stroke-width="1"/>
              </svg>
            </div>
            <span class="nav-text">Usuarios</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>

        <li class="nav-item" :class="{ active: $route.name === 'Historiales' }">
          <router-link to="/historiales" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <!-- Ícono profesional de cronómetro empresarial -->
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12,6 12,12 16,14"/>
                <!-- Marcadores de tiempo profesionales -->
                <path d="M12 2v2" stroke-width="3"/>
                <path d="M12 20v2" stroke-width="3"/>
                <path d="M2 12h2" stroke-width="3"/>
                <path d="M20 12h2" stroke-width="3"/>
                <!-- Detalles de cronómetro premium -->
                <circle cx="12" cy="12" r="2" opacity="0.3" fill="currentColor"/>
                <path d="M15.5 8.5L17 7" opacity="0.6"/>
                <path d="M8.5 15.5L7 17" opacity="0.6"/>
                <!-- Indicadores de medición -->
                <circle cx="12" cy="6" r="0.5" opacity="0.4"/>
                <circle cx="18" cy="12" r="0.5" opacity="0.4"/>
                <circle cx="12" cy="18" r="0.5" opacity="0.4"/>
                <circle cx="6" cy="12" r="0.5" opacity="0.4"/>
              </svg>
            </div>
            <span class="nav-text">Historiales</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
        
        <li class="nav-item" :class="{ active: $route.name === 'Notificaciones' }">
          <router-link to="/notificaciones" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <!-- Ícono profesional de notificaciones empresariales -->
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                <!-- Indicador de notificación premium -->
                <circle cx="19" cy="5" r="3" fill="#4CAF50" opacity="0.9"/>
                <circle cx="19" cy="5" r="1.5" fill="#ffffff" opacity="1"/>
                <!-- Ondas de transmisión profesionales -->
                <path d="M21 8c1 0 2 0.5 2 2s-1 2-2 2" opacity="0.5" stroke-width="1.5"/>
                <path d="M22 6c1.5 0 2.5 1 2.5 4s-1 4-2.5 4" opacity="0.3" stroke-width="1"/>
                <!-- Detalles empresariales -->
                <rect x="8" y="12" width="8" height="1" rx="0.5" opacity="0.2" fill="currentColor"/>
                <rect x="10" y="14" width="4" height="0.5" rx="0.25" opacity="0.15" fill="currentColor"/>
              </svg>
            </div>
            <span class="nav-text">Notificaciones</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
        
        <li class="nav-item" :class="{ active: $route.name === 'Permisos' }" v-if="isAdmin">
          <router-link to="/permisos" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <!-- Ícono profesional de seguridad empresarial -->
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 9v6"/>
                <path d="M9 12h6"/>
                <!-- Elementos de verificación de seguridad -->
                <path d="M9 9l1.5 1.5L13 8" opacity="0.6" stroke-width="1.5"/>
                <!-- Detalles de autorización -->
                <circle cx="8" cy="7" r="0.5" opacity="0.4"/>
                <circle cx="16" cy="7" r="0.5" opacity="0.4"/>
                <circle cx="8" cy="17" r="0.5" opacity="0.4"/>
                <circle cx="16" cy="17" r="0.5" opacity="0.4"/>
                <!-- Marco de seguridad -->
                <rect x="4" y="5" width="16" height="14" rx="2" opacity="0.1" stroke="none" fill="currentColor"/>
              </svg>
            </div>
            <span class="nav-text">Permisos de Usuarios</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
        
        <li class="nav-item" :class="{ active: $route.name === 'Configuracion' }" v-if="isAdmin">
          <router-link to="/configuracion" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"/>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
              </svg>
            </div>
            <span class="nav-text">Configuración</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
      </ul>
    </nav>
      <div class="sidebar-footer">
      <button @click="showLogoutModal = true" class="logout-btn">
        <div class="btn-icon-wrapper">
          <svg class="logout-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <!-- Ícono profesional de logout empresarial -->
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16,17 21,12 16,7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
            <!-- Marco de puerta profesional -->
            <rect x="3" y="3" width="6" height="18" rx="1" opacity="0.1" fill="currentColor"/>
            <!-- Indicador de salida -->
            <circle cx="18.5" cy="8" r="0.5" opacity="0.6"/>
            <circle cx="18.5" cy="16" r="0.5" opacity="0.6"/>
            <!-- Línea de movimiento -->
            <path d="M12 12h6" opacity="0.4" stroke-width="3" stroke-linecap="round"/>
          </svg>
        </div>
        <span class="logout-text">Cerrar Sesión</span>
        <div class="logout-glow"></div>
      </button>
    </div>
    
    <!-- Modal de confirmación de logout -->
    <Teleport to="body">
      <div v-if="showLogoutModal" class="logout-modal-overlay" @click="closeModal">
        <div class="logout-modal" @click.stop>
          <div class="modal-header">          <div class="modal-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline points="16,17 21,12 16,7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
          </div>
            <h3>Cerrar Sesión</h3>
          </div>
          
          <div class="modal-body">
            <p>¿Estás seguro de que quieres cerrar sesión?</p>
          </div>
          
          <div class="modal-actions">
            <button @click="closeModal" class="btn-cancel">
              Cancelar
            </button>
            <button @click="confirmLogout" class="btn-confirm">
              Aceptar
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import authService from '../services/authService'

const router = useRouter()

// Estado del sidebar
const isCollapsed = ref(false)
const showLogoutModal = ref(false)

// Estado del usuario
const currentUser = ref(null)

// Computed properties para el rol
const isAdmin = computed(() => {
  return authService.isAdmin()
})

const isUser = computed(() => {
  return authService.isUser()
})

const userDisplayName = computed(() => {
  if (currentUser.value) {
    return currentUser.value.nombre || currentUser.value.username || 'Usuario'
  }
  return 'Usuario'
})

const roleDisplayName = computed(() => {
  const role = authService.getUserRole()
  return role === 'admin' ? 'Administrador' : 'Usuario'
})

// Funciones del sidebar
const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}

// Funciones del modal de logout
const closeModal = () => {
  showLogoutModal.value = false
}

const confirmLogout = () => {
  showLogoutModal.value = false
  authService.logout()
  router.push('/login')
}

// Cerrar modal con Escape
const handleKeydown = (event) => {
  if (event.key === 'Escape' && showLogoutModal.value) {
    closeModal()
  }
}

// Cargar información del usuario al montar
onMounted(async () => {
  try {
    currentUser.value = authService.getCurrentUser()
    // Refrescar información del usuario desde el servidor
    if (currentUser.value) {
      await authService.refreshUserInfo()
      currentUser.value = authService.getCurrentUser()
    }
  } catch (error) {
    console.error('Error cargando información del usuario:', error)
  }
})

// Agregar listener para Escape
if (typeof window !== 'undefined') {
  window.addEventListener('keydown', handleKeydown)
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700;800;900&family=Source+Sans+Pro:wght@300;400;600;700;900&display=swap');

.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: min(220px, 18vw);
  max-width: 240px;
  min-width: 180px;
  background: linear-gradient(180deg, 
    #1B5E20 0%, 
    #2E7D32 25%,
    #388E3C 50%,
    #2E7D32 75%,
    #1B5E20 100%);
  border-right: 3px solid #0D4E14;
  color: #FFFFFF;
  display: flex;
  flex-direction: column;
  z-index: 1000;
  overflow-y: auto;
  overflow-x: hidden;
  box-shadow: 
    0 8px 24px rgba(0, 0, 0, 0.25),
    0 4px 12px rgba(27, 94, 32, 0.4);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  
  /* Escalado dinámico basado en viewport */
  font-size: clamp(12px, 1.2vw, 16px);
}
.sidebar-header {
  padding: clamp(2px, 0.5vh, 4px) clamp(2px, 0.4vw, 4px) clamp(3px, 0.6vh, 6px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  background: linear-gradient(135deg, 
    rgba(13, 78, 20, 0.8) 0%, 
    rgba(27, 94, 32, 0.6) 100%);
  flex-shrink: 0;
  min-height: fit-content;
  max-height: 8vh;
}

.header-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: clamp(1px, 0.2vh, 2px);
  width: 100%;
  max-width: min(140px, 90%);
}

.sidebar-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 24px;
  right: 24px;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.6) 50%, 
    transparent 100%);
}

.logo {
  width: 56px;
  height: 56px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: transparent;
  border-radius: 18px;
  position: relative;
  overflow: visible;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  margin-bottom: 4px;
}

.logo:hover {
  transform: scale(1.1);
}

/* Estilos para la animación de flor girando */
.flower-animation {
  width: clamp(10px, 1.5vw, 14px);
  height: clamp(10px, 1.5vw, 14px);
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  filter: drop-shadow(0 1px 4px rgba(76, 175, 80, 0.2));
  animation: flowerRotate 8s linear infinite;
}

.flower-animation::before {
  content: '';
  position: absolute;
  width: 130%;
  height: 130%;
  background: radial-gradient(circle, rgba(76, 175, 80, 0.15) 0%, rgba(139, 195, 74, 0.08) 40%, transparent 70%);
  border-radius: 50%;
  animation: flowerAura 4s ease-in-out infinite;
  z-index: -1;
}

.flower-icon {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 3px 12px rgba(76, 175, 80, 0.5));
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  z-index: 1;
  position: relative;
}

.flower-icon:hover {
  transform: scale(1.15);
  filter: drop-shadow(0 6px 25px rgba(76, 175, 80, 0.7));
}

/* Animación de rotación continua para la flor */
@keyframes flowerRotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes flowerAura {
  0%, 100% {
    transform: scale(1);
    opacity: 0.4;
  }
  33% {
    transform: scale(1.1);
    opacity: 0.7;
  }
  66% {
    transform: scale(1.2);
    opacity: 0.5;
  }
}

/* Efectos adicionales para la nueva animación verde */
.flower-animation::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, transparent 60%, rgba(76, 175, 80, 0.1) 80%, transparent 100%);
  border-radius: 50%;
  animation: flowerPulse 3s ease-in-out infinite;
  z-index: -2;
}

@keyframes flowerPulse {
  0%, 100% {
    transform: scale(0.8);
    opacity: 0;
  }
  50% {
    transform: scale(1.4);
    opacity: 0.6;
  }
}

/* Tipografía profesional mejorada */
.logo-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.5px;
  width: 100%;
}

.brand-title {
  margin: 0;
  font-size: clamp(0.5px, 0.05vw, 1px);
  font-weight: 500;
  background: linear-gradient(135deg, 
    #E8F5E8 0%, 
    #A5D6A7 25%,
    #66BB6A 50%,
    #4CAF50 75%,
    #2E7D32 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: clamp(0.001em, 0.005vw, 0.01em);
  line-height: 0.8;
  font-family: 'Source Sans Pro', 'SF Pro Display', 'system-ui', '-apple-system', sans-serif;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-transform: uppercase;
  position: relative;
  white-space: nowrap;
  filter: drop-shadow(0 0.2px 0.5px rgba(76, 175, 80, 0.1));
  padding-bottom: clamp(3px, 0.5vh, 6px);
  margin-bottom: clamp(2px, 0.3vh, 4px);
}

.brand-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    #E8F5E8 10%,
    #A5D6A7 25%,
    #66BB6A 50%,
    #4CAF50 75%,
    #2E7D32 90%,
    transparent 100%);
  border-radius: 1px;
  box-shadow: 
    0 0 4px rgba(76, 175, 80, 0.3),
    0 0 8px rgba(76, 175, 80, 0.2);
  animation: lineGlow 2s ease-in-out infinite;
}

@keyframes lineGlow {
  0%, 100% {
    opacity: 0.6;
    transform: translateX(-50%) scaleX(0.8);
    box-shadow: 
      0 0 4px rgba(76, 175, 80, 0.3),
      0 0 8px rgba(76, 175, 80, 0.2);
  }
  25% {
    opacity: 0.9;
    transform: translateX(-50%) scaleX(1.1);
    box-shadow: 
      0 0 8px rgba(76, 175, 80, 0.5),
      0 0 16px rgba(76, 175, 80, 0.3);
  }
  50% {
    opacity: 1;
    transform: translateX(-50%) scaleX(1.2);
    box-shadow: 
      0 0 12px rgba(76, 175, 80, 0.7),
      0 0 24px rgba(76, 175, 80, 0.4);
  }
  75% {
    opacity: 0.8;
    transform: translateX(-50%) scaleX(1.0);
    box-shadow: 
      0 0 6px rgba(76, 175, 80, 0.4),
      0 0 12px rgba(76, 175, 80, 0.25);
  }
}

.brand-title:hover {
  transform: translateY(-1px);
}

.brand-subtitle {
  margin: 0;
  font-size: clamp(2.5px, 0.25vw, 3.5px);
  color: rgba(255, 255, 255, 0.6);
  font-weight: 300;
  text-shadow: 0 0.5px 0.5px rgba(0, 0, 0, 0.15);
  letter-spacing: clamp(0.03em, 0.04vw, 0.06em);
  text-transform: uppercase;
  font-family: 'Montserrat', 'Inter', 'Source Sans Pro', sans-serif;
  opacity: 0.7;
  transition: all 0.3s ease;
  font-variant: small-caps;
  white-space: nowrap;
  overflow: visible;
  text-overflow: clip;
}

.brand-subtitle:hover {
  opacity: 1;
  transform: translateY(-0.5px);
}

/* Estilos modernos para el botón del geoportal */
.geoportal-section {
  padding: clamp(4px, 0.8vh, 8px) clamp(4px, 0.8vw, 8px) clamp(6px, 1vh, 10px);
  margin-bottom: clamp(2px, 0.4vh, 4px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  position: relative;
  background: linear-gradient(135deg, 
    rgba(13, 78, 20, 0.4) 0%, 
    rgba(27, 94, 32, 0.3) 100%);
  flex-shrink: 0;
  max-height: 12vh;
  display: flex;
  flex-direction: row;
  gap: clamp(2px, 0.5vw, 4px);
}

.geoportal-section::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 24px;
  right: 24px;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.4) 50%, 
    transparent 100%);
}

.geoportal-btn {
  width: 50%;
  flex: 1;
  background: linear-gradient(135deg, 
    rgba(27, 94, 32, 0.3) 0%, 
    rgba(46, 125, 50, 0.25) 30%,
    rgba(76, 175, 80, 0.2) 70%,
    rgba(139, 195, 74, 0.15) 100%);
  backdrop-filter: blur(25px) saturate(200%);
  -webkit-backdrop-filter: blur(25px) saturate(200%);
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: rgba(255, 255, 255, 0.95);
  padding: clamp(3px, 0.5vh, 5px) clamp(4px, 0.6vw, 6px);
  border-radius: clamp(6px, 1.2vw, 10px);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: clamp(1px, 0.2vh, 2px);
  font-size: clamp(7px, 0.8vw, 9px);
  font-weight: 500;
  text-decoration: none;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
  overflow: hidden;
  min-height: clamp(32px, 4vh, 40px);
  box-shadow: 
    0 3px 12px rgba(0, 0, 0, 0.15),
    0 1px 4px rgba(0, 0, 0, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.4),
    inset 0 -1px 0 rgba(0, 0, 0, 0.1),
    0 0 20px rgba(76, 175, 80, 0.1);
}

.geoportal-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.3) 50%, 
    transparent 100%);
  transition: left 0.6s ease-in-out;
  z-index: 1;
}

.geoportal-btn:hover::before {
  left: 100%;
}

.geoportal-btn i,
.geoportal-btn span {
  position: relative;
  z-index: 2;
}

.geoportal-btn:hover {
  background: linear-gradient(135deg, 
    rgba(27, 94, 32, 0.45) 0%, 
    rgba(46, 125, 50, 0.4) 50%,
    rgba(76, 175, 80, 0.35) 100%);
  backdrop-filter: blur(30px) saturate(250%);
  -webkit-backdrop-filter: blur(30px) saturate(250%);
  border: 1px solid rgba(255, 255, 255, 0.4);
  transform: translateY(-1px) scale(1.02);
  box-shadow: 
    0 6px 20px rgba(0, 0, 0, 0.2),
    0 2px 8px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.5),
    inset 0 -1px 0 rgba(0, 0, 0, 0.15),
    0 0 30px rgba(76, 175, 80, 0.3);
}

.geoportal-btn:hover .geoportal-glow {
  opacity: 1;
  transform: scale(1);
}

.geoportal-btn:hover .arrow-icon {
  transform: translateX(6px) rotate(45deg);
}

.geoportal-btn:active {
  transform: translateY(-1px) scale(1.01);
}

.geoportal-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  flex-shrink: 0;
}

.geoportal-icon {
  width: clamp(12px, 1.4vw, 14px);
  height: clamp(12px, 1.4vw, 14px);
  stroke-width: 2;
  filter: drop-shadow(0 1px 3px rgba(0, 0, 0, 0.15));
  transition: all 0.3s ease;
}

.arrow-icon {
  width: clamp(6px, 0.8vw, 8px);
  height: clamp(6px, 0.8vw, 8px);
  opacity: 0.8;
  stroke-width: 2.2;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  filter: drop-shadow(0 0.5px 1px rgba(0, 0, 0, 0.15));
}

.geoportal-text {
  font-size: clamp(7px, 0.8vw, 9px);
  font-weight: 500;
  text-shadow: 0 0.5px 1px rgba(0, 0, 0, 0.1);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 0;
  text-align: center;
}

.geoportal-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 70%);
  border-radius: 16px;
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  transition: all 0.4s ease;
  pointer-events: none;
}

/* Estilos modernos para el botón de la App Móvil */
.mobile-app-btn {
  width: 50%;
  flex: 1;
  background: linear-gradient(135deg, 
    rgba(21, 101, 192, 0.4) 0%, 
    rgba(25, 118, 210, 0.35) 30%,
    rgba(33, 150, 243, 0.3) 70%,
    rgba(100, 181, 246, 0.25) 100%);
  backdrop-filter: blur(25px) saturate(200%);
  -webkit-backdrop-filter: blur(25px) saturate(200%);
  border: 1px solid rgba(100, 181, 246, 0.3);
  color: rgba(255, 255, 255, 0.95);
  padding: clamp(3px, 0.5vh, 5px) clamp(4px, 0.6vw, 6px);
  border-radius: clamp(6px, 1.2vw, 10px);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: clamp(1px, 0.2vh, 2px);
  font-size: clamp(7px, 0.8vw, 9px);
  font-weight: 500;
  text-decoration: none;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
  overflow: hidden;
  min-height: clamp(32px, 4vh, 40px);
  box-shadow: 
    0 3px 12px rgba(0, 0, 0, 0.15),
    0 1px 4px rgba(0, 0, 0, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.4),
    inset 0 -1px 0 rgba(0, 0, 0, 0.1),
    0 0 20px rgba(33, 150, 243, 0.2);
}

.mobile-app-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.4) 50%, 
    transparent 100%);
  transition: left 0.6s ease-in-out;
  z-index: 1;
}

.mobile-app-btn:hover::before {
  left: 100%;
}

.mobile-app-btn:hover {
  background: linear-gradient(135deg, 
    rgba(21, 101, 192, 0.6) 0%, 
    rgba(25, 118, 210, 0.55) 30%,
    rgba(33, 150, 243, 0.5) 70%,
    rgba(100, 181, 246, 0.45) 100%);
  backdrop-filter: blur(30px) saturate(250%);
  -webkit-backdrop-filter: blur(30px) saturate(250%);
  border: 1px solid rgba(100, 181, 246, 0.5);
  transform: translateY(-1px) scale(1.02);
  box-shadow: 
    0 6px 20px rgba(0, 0, 0, 0.2),
    0 2px 8px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.5),
    inset 0 -1px 0 rgba(0, 0, 0, 0.15),
    0 0 30px rgba(33, 150, 243, 0.5);
}

.mobile-app-btn:hover .mobile-app-glow {
  opacity: 1;
  transform: scale(1);
}

.mobile-app-btn:hover .mobile-arrow-icon {
  transform: translateX(6px) rotate(45deg);
}

.mobile-app-btn i,
.mobile-app-btn span {
  position: relative;
  z-index: 2;
}

.mobile-app-btn:active {
  transform: translateY(-1px) scale(1.01);
}

.mobile-app-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  flex-shrink: 0;
}

.mobile-app-icon {
  width: clamp(12px, 1.4vw, 14px);
  height: clamp(12px, 1.4vw, 14px);
  stroke-width: 2;
  filter: drop-shadow(0 1px 3px rgba(0, 0, 0, 0.15));
  transition: all 0.3s ease;
}

.mobile-arrow-icon {
  width: clamp(6px, 0.8vw, 8px);
  height: clamp(6px, 0.8vw, 8px);
  opacity: 0.8;
  stroke-width: 2.2;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  filter: drop-shadow(0 0.5px 1px rgba(0, 0, 0, 0.15));
}

.mobile-app-text {
  font-size: clamp(7px, 0.8vw, 9px);
  font-weight: 500;
  text-shadow: 0 0.5px 1px rgba(0, 0, 0, 0.1);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 0;
  text-align: center;
}

.mobile-app-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 70%);
  border-radius: 16px;
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  transition: all 0.4s ease;
  pointer-events: none;
}

.sidebar-nav {
  flex: 1;
  padding: clamp(12px, 2vh, 24px) 0 0 0;
  overflow-y: auto;
  overflow-x: hidden;
  min-height: 0;
}

.sidebar-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin-bottom: 0;  /* Eliminado completamente el margin-bottom */
  padding: 0 clamp(2px, 0.3vw, 4px);  /* Padding lateral aún más reducido */
}

.nav-link {
  display: flex;
  align-items: center;
  gap: clamp(6px, 0.8vw, 10px);  /* Añadido espacio entre icono y texto */
  padding: clamp(8px, 1.6vh, 14px) clamp(4px, 0.8vw, 8px);  /* Padding izquierdo más reducido */
  color: rgba(255, 255, 255, 0.75);
  text-decoration: none;
  border-radius: clamp(8px, 1.2vw, 12px);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  margin-bottom: 0;  /* Eliminado el margin-bottom */
  backdrop-filter: blur(5px);
  border: 1px solid transparent;
  min-height: clamp(44px, 5.5vh, 55px);  /* Altura aumentada para mejor proporción */
}

.nav-link:hover {
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.08) 0%, 
    rgba(255, 255, 255, 0.04) 100%);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.9);
  transform: translateX(2px) scale(1.01);
  box-shadow: 
    0 2px 12px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
  border-radius: clamp(6px, 1vw, 10px);
}

.nav-link:hover .nav-glow {
  opacity: 1;
  transform: scale(1);
}

.nav-link:hover .nav-icon {
  filter: drop-shadow(0 1px 6px rgba(255, 255, 255, 0.2));
  transform: scale(1.02);
}

.nav-item.active .nav-link,
.nav-link.router-link-active,
.nav-link.router-link-exact-active {
  /* Efecto de vidrio transparente moderno */
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.15) 0%, 
    rgba(255, 255, 255, 0.08) 50%,
    rgba(255, 255, 255, 0.12) 100%);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.95);
  box-shadow: 
    0 4px 20px rgba(255, 255, 255, 0.1),
    0 2px 10px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.3),
    inset 0 -1px 0 rgba(255, 255, 255, 0.1);
  transform: translateX(2px);
  border-radius: clamp(8px, 1.2vw, 12px);
}

.nav-item.active .nav-link .nav-icon,
.nav-link.router-link-active .nav-icon,
.nav-link.router-link-exact-active .nav-icon {
  filter: drop-shadow(0 1px 4px rgba(255, 255, 255, 0.4)) 
          drop-shadow(0 0 8px rgba(255, 255, 255, 0.2));
  transform: scale(1.1);  /* Aumentado para compensar el tamaño más pequeño */
}

.nav-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: clamp(24px, 3vw, 28px);  /* Aumentado para mejor proporción */
  height: clamp(24px, 3vw, 28px);
  position: relative;
  flex-shrink: 0;
  
  /* Fondo liquid glass circular */
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.2) 0%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0.05) 100%);
  backdrop-filter: blur(12px) saturate(180%);
  border-radius: 50%;  /* Completamente circular */
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 
    0 2px 8px rgba(0, 0, 0, 0.1),
    0 1px 4px rgba(0, 0, 0, 0.05),
    inset 0 1px 2px rgba(255, 255, 255, 0.25);
  
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-item:hover .nav-icon-wrapper {
  background: linear-gradient(135deg, 
    rgba(76, 175, 80, 0.25) 0%,
    rgba(76, 175, 80, 0.15) 50%,
    rgba(76, 175, 80, 0.08) 100%);
  border-color: rgba(76, 175, 80, 0.3);
  box-shadow: 
    0 4px 12px rgba(76, 175, 80, 0.2),
    0 2px 6px rgba(76, 175, 80, 0.1),
    inset 0 1px 3px rgba(255, 255, 255, 0.35);
  transform: translateY(-1px);
}

.nav-item.active .nav-icon-wrapper {
  background: linear-gradient(135deg, 
    rgba(76, 175, 80, 0.3) 0%,
    rgba(76, 175, 80, 0.2) 50%,
    rgba(76, 175, 80, 0.1) 100%);
  border-color: rgba(76, 175, 80, 0.4);
  box-shadow: 
    0 6px 16px rgba(76, 175, 80, 0.25),
    0 3px 8px rgba(76, 175, 80, 0.15),
    inset 0 1px 3px rgba(255, 255, 255, 0.4);
}

.nav-icon {
  width: clamp(14px, 1.8vw, 16px);  /* Aumentado para mejor proporción */
  height: clamp(14px, 1.8vw, 16px);
  stroke-width: 2;  /* Grosor de línea medio */
  transition: all 0.3s ease;
  filter: drop-shadow(0 1px 3px rgba(0, 0, 0, 0.1));  /* Sombra más sutil */
}

.nav-text {
  font-size: clamp(15px, 1.6vw, 18px);  /* Aumentado significativamente el tamaño */
  font-weight: 500;  /* Cambiado a semi-bold para mejor legibilidad */
  font-family: 'Inter', 'Segoe UI', 'Arial', 'Helvetica', sans-serif;
  text-shadow: 0 0.5px 1px rgba(0, 0, 0, 0.1);
  letter-spacing: 0.01em;
  white-space: normal;  /* Permitir múltiples líneas */
  word-wrap: break-word;  /* Romper palabras si es necesario */
  overflow-wrap: break-word;
  line-height: 1.3;  /* Líneas más leíbles */
  flex: 1;
  min-width: 0;
  text-align: left;
  transition: all 0.2s ease;
  max-height: 2.6em;  /* Máximo 2 líneas con más altura */
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;  /* Propiedad estándar */
  -webkit-box-orient: vertical;
  margin-left: clamp(6px, 0.8vw, 10px);  /* Espacio del ícono */
}

.nav-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(27, 94, 32, 0.3) 0%, transparent 70%);
  border-radius: 16px;
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  transition: all 0.4s ease;
  pointer-events: none;
}

.sidebar-footer {
  padding: 0 clamp(8px, 1.6vw, 16px) clamp(2px, 0.4vh, 4px);
  position: relative;
  display: flex;
  justify-content: center;
  background: transparent;
  flex-shrink: 0;
  margin-top: 0;
  max-height: 15vh;
}

/* Línea decorativa eliminada para que no haya separación
.sidebar-footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 24px;
  right: 24px;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.4) 50%, 
    transparent 100%);
}
*/

.logout-btn {
  width: 100%;
  max-width: min(180px, 95%);  /* Mucho más ancho */
  background: linear-gradient(135deg, 
    rgba(220, 38, 127, 0.8) 0%, 
    rgba(244, 67, 54, 0.75) 30%,
    rgba(229, 57, 53, 0.7) 70%,
    rgba(198, 40, 40, 0.65) 100%);  /* Rojo sólido sin difuminar */
  border: 1px solid rgba(244, 67, 54, 0.9);  /* Borde rojo más visible */
  color: rgba(255, 255, 255, 1);  /* Texto completamente blanco */
  padding: clamp(2px, 0.3vh, 3px) clamp(8px, 1.2vw, 12px);  /* Padding vertical mínimo */
  border-radius: clamp(12px, 2vw, 18px);  /* Mucho más redondeado */
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(4px, 0.8vw, 8px);  /* Gap más grande */
  font-size: clamp(9px, 1vw, 12px);  /* Fuente más grande */
  font-weight: 600;  /* Peso más bold */
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
  overflow: hidden;
  min-height: clamp(24px, 2.5vh, 28px);  /* Altura mínima reducida al máximo */
  box-shadow: 
    0 4px 16px rgba(244, 67, 54, 0.4),  /* Sombra roja más intensa */
    0 2px 8px rgba(220, 38, 127, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.3),  /* Brillo interno */
    inset 0 -1px 0 rgba(198, 40, 40, 0.4);
}

.logout-btn:hover {
  background: linear-gradient(135deg, 
    rgba(220, 38, 127, 0.9) 0%, 
    rgba(244, 67, 54, 0.85) 30%,
    rgba(229, 57, 53, 0.8) 70%,
    rgba(198, 40, 40, 0.75) 100%);  /* Rojo más intenso sin blur */
  border: 1px solid rgba(244, 67, 54, 1);  /* Borde rojo sólido */
  transform: translateY(-1px) scale(1.02);
  box-shadow: 
    0 6px 24px rgba(244, 67, 54, 0.6),  /* Sombra roja más intensa */
    0 3px 12px rgba(220, 38, 127, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.4),  /* Brillo interno */
    inset 0 -1px 0 rgba(198, 40, 40, 0.5);
}

.logout-btn:hover .logout-glow {
  opacity: 1;
  transform: scale(1);
}

.logout-btn:hover .logout-icon {
  animation: slideToSide 0.4s ease-in-out;
}

.logout-btn:active {
  transform: translateY(-1px) scale(1.01);
  animation: slideActivation 0.25s ease-out;
}

/* Animación simplificada de lado a lado */
@keyframes slideActivation {
  0% {
    transform: translateX(0) translateY(-1px) scale(1.01);
  }
  33% {
    transform: translateX(-4px) translateY(-1px) scale(1.01);
  }
  66% {
    transform: translateX(4px) translateY(-1px) scale(1.01);
  }
  100% {
    transform: translateX(0) translateY(-1px) scale(1.01);
  }
}

/* Animación simplificada para el icono */
@keyframes slideToSide {
  0%, 100% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(-2px);
  }
}

/* Animación sutil de pulsación para el botón */
@keyframes logoutPulse {
  0%, 100% {
    box-shadow: 
      0 6px 20px rgba(244, 67, 54, 0.2),
      0 0 0 1px rgba(255, 255, 255, 0.05),
      inset 0 1px 0 rgba(255, 255, 255, 0.08);
  }
  50% {
    box-shadow: 
      0 8px 25px rgba(244, 67, 54, 0.3),
      0 0 0 1px rgba(255, 255, 255, 0.08),
      inset 0 1px 0 rgba(255, 255, 255, 0.12);
  }
}

/* Animación de temblor para el icono en hover */
@keyframes logoutShake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-2px); }
  20%, 40%, 60%, 80% { transform: translateX(2px); }
}

.btn-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: clamp(20px, 2.2vw, 24px);  /* Más grande para el botón más ancho */
  height: clamp(20px, 2.2vw, 24px);
  flex-shrink: 0;
  position: relative;
  z-index: 2;  /* Por encima del efecto de onda */
  
  /* Fondo sólido sin blur */
  background: linear-gradient(135deg, 
    rgba(255, 255, 255, 0.25) 0%,
    rgba(244, 67, 54, 0.2) 50%,  /* Toque de rojo */
    rgba(255, 255, 255, 0.1) 100%);
  border-radius: 50%;  /* Completamente circular */
  border: 1px solid rgba(244, 67, 54, 0.4);  /* Borde rojo más visible */
  box-shadow: 
    0 2px 6px rgba(244, 67, 54, 0.2),  /* Sombra con tinte rojo */
    0 1px 3px rgba(0, 0, 0, 0.15),
    inset 0 1px 2px rgba(255, 255, 255, 0.3);  /* Brillo interno */
  
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.logout-btn:hover .btn-icon-wrapper {
  background: linear-gradient(135deg, 
    rgba(244, 67, 54, 0.3) 0%,  /* Rojo más intenso */
    rgba(244, 67, 54, 0.2) 50%,
    rgba(244, 67, 54, 0.1) 100%);
  border-color: rgba(244, 67, 54, 0.5);  /* Borde rojo más brillante */
  box-shadow: 
    0 4px 12px rgba(244, 67, 54, 0.25),  /* Sombra roja más intensa */
    0 2px 6px rgba(244, 67, 54, 0.15),
    inset 0 1px 3px rgba(255, 255, 255, 0.4);  /* Brillo interno más fuerte */
  transform: translateY(-1px);
}

.logout-icon {
  width: clamp(12px, 1.3vw, 16px);  /* Más grande para el botón más ancho */
  height: clamp(12px, 1.3vw, 16px);
  stroke-width: 2;  /* Línea un poco más fina */
  transition: all 0.3s ease;
  filter: drop-shadow(0 0.5px 2px rgba(0, 0, 0, 0.2));  /* Sombra más sutil */
  position: relative;
  z-index: 2;  /* Por encima del efecto de onda */
}

.logout-text {
  font-size: clamp(7px, 0.7vw, 9px);  /* Letra mucho más pequeña */
  font-family: 'Arial', sans-serif;  /* Fuente Arial */
  font-weight: 500;  /* Peso reducido */
  text-shadow: 0 0.5px 1px rgba(0, 0, 0, 0.15);  /* Sombra más sutil */
  letter-spacing: 0.01em;  /* Espaciado más positivo para mejor legibilidad */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
  min-width: 0;
  position: relative;
  z-index: 2;  /* Por encima del efecto de onda */
}

.logout-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.2) 0%, transparent 70%);
  border-radius: 12px;
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  transition: all 0.3s ease;
  pointer-events: none;
}

/* Responsive Design para tablets */
@media (max-width: 1024px) and (min-width: 769px) {
  .sidebar {
    width: 260px;
  }
  
  .sidebar-header {
    padding: 20px 16px 24px;
  }
  
  .flower-animation {
    width: 40px;
    height: 40px;
  }
  
  .brand-title {
    font-size: 14px;
    letter-spacing: 0.1em;
  }
  
  .brand-subtitle {
    font-size: 11px;
  }
  
  .geoportal-section {
    padding: 12px 12px 16px;
  }
  
  .geoportal-btn,
  .mobile-app-btn {
    padding: 8px 12px;
    font-size: 12px;
  }
  
  .nav-link {
    padding: 12px 14px;
    gap: 0px;  /* Eliminado completamente el espacio entre icono y texto en tablets */
    min-height: 50px;
  }
  
  .nav-text {
    font-size: 13px;  /* Aumentado significativamente el tamaño de fuente para tablets */
    font-weight: 400;  /* Normal (sin negritas) para tablets */
    font-family: 'Arial', 'Helvetica', 'Segoe UI', sans-serif;  /* Cambiado a Arial */
    white-space: normal;
    word-wrap: break-word;
    line-height: 1.2;
    max-height: 2.4em;
  }
  
  .logout-btn {
    padding: 10px 14px;
    font-size: 12px;
  }
}

/* Responsive Design para móviles landscape */
@media (max-width: 768px) and (orientation: landscape) {
  .sidebar {
    width: 240px;
    height: 100vh;
    overflow-y: auto;
    overflow-x: hidden;
    position: fixed;
    z-index: 1001;
  }
  
  .sidebar-header {
    padding: 12px 12px 16px;
    min-height: auto;
  }
  
  .header-content {
    gap: 8px;
  }
  
  .flower-animation {
    width: 32px;
    height: 32px;
  }
  
  .brand-title {
    font-size: 12px;
    letter-spacing: 0.08em;
    line-height: 1.1;
  }
  
  .brand-subtitle {
    font-size: 9px;
  }
  
  .geoportal-section {
    padding: 8px 8px 12px;
  }
  
  .geoportal-btn,
  .mobile-app-btn {
    padding: 6px 10px;
    font-size: 11px;
    gap: 6px;
    margin-top: 8px;
  }
  
  .geoportal-icon,
  .mobile-app-icon {
    width: 14px;
    height: 14px;
  }
  
  .arrow-icon,
  .mobile-arrow-icon {
    width: 10px;
    height: 10px;
  }
  
  .sidebar-nav {
    padding: 12px 0;
  }
  
  .nav-item {
    margin-bottom: 4px;
    padding: 0 8px;
  }
  
  .nav-link {
    padding: 8px 12px;
    gap: 0px;  /* Eliminado completamente el espacio */
    min-height: 48px;
  }
  
  .nav-icon {
    width: 14px;  /* Ajustado para móviles */
    height: 14px;
  }
  
  .nav-text {
    font-size: 12px;  /* Aumentado significativamente el tamaño para landscape móvil */
    font-weight: 400;  /* Normal (sin negritas) para landscape */
    font-family: 'Arial', 'Helvetica', 'Segoe UI', sans-serif;
    white-space: normal;
    word-wrap: break-word;
    line-height: 1.2;
    max-height: 2.4em;
  }
  
  .sidebar-footer {
    padding: 8px 8px 12px;
  }
  
  .logout-btn {
    padding: 8px 12px;
    font-size: 11px;
    gap: 8px;
  }
  
  .logout-icon {
    width: 14px;
    height: 14px;
  }
}

/* Responsive Design para móviles portrait */
@media (max-width: 768px) and (orientation: portrait) {
  .sidebar {
    width: 100%;
    height: 100vh;
    overflow-y: auto;
    overflow-x: hidden;
    position: fixed;
    z-index: 1001;
    display: flex;
    flex-direction: column;
  }
  
  .sidebar-header {
    padding: 16px 16px 20px;
    flex-shrink: 0;
  }
  
  .header-content {
    gap: 12px;
  }
  
  .flower-animation {
    width: 36px;
    height: 36px;
  }
  
  .brand-title {
    font-size: 13px;
    letter-spacing: 0.1em;
  }
  
  .brand-subtitle {
    font-size: 10px;
  }
  
  .geoportal-section {
    padding: 12px 16px 16px;
    flex-shrink: 0;
  }
  
  .geoportal-btn,
  .mobile-app-btn {
    padding: 10px 16px;
    font-size: 12px;
    gap: 10px;
  }
  
  .mobile-app-btn {
    margin-top: 10px;
  }
  
  .sidebar-nav {
    flex: 1;
    padding: 16px 0;
    overflow-y: auto;
  }
  
  .nav-item {
    margin-bottom: 6px;
    padding: 0 16px;
  }
  
  .nav-link {
    padding: 12px 16px;
    gap: 0px;  /* Eliminado completamente el espacio */
    min-height: 52px;
  }
  
  .nav-icon {
    width: 14px;  /* Ajustado para móviles portrait */
    height: 14px;
  }
  
  .nav-text {
    font-size: 13px;  /* Aumentado significativamente el tamaño para móvil portrait */
    font-weight: 400;  /* Normal (sin negritas) para portrait */
    font-family: 'Arial', 'Helvetica', 'Segoe UI', sans-serif;
    white-space: normal;
    word-wrap: break-word;
    line-height: 1.2;
  }
  
  .sidebar-footer {
    padding: 16px 16px 20px;
    flex-shrink: 0;
  }
  
  .logout-btn {
    padding: 12px 16px;
    font-size: 12px;
    gap: 10px;
  }
  
  .logout-icon {
    width: 16px;
    height: 16px;
  }
}

/* Responsive para pantallas muy pequeñas (móviles pequeños) */
@media (max-width: 480px) {
  .sidebar {
    width: 100%;
  }
  
  .sidebar-header {
    padding: 12px 12px 16px;
  }
  
  .flower-animation {
    width: 30px;
    height: 30px;
  }
  
  .brand-title {
    font-size: 11px;
    letter-spacing: 0.08em;
  }
  
  .brand-subtitle {
    font-size: 9px;
  }
  
  .geoportal-section {
    padding: 10px 12px 14px;
  }
  
  .geoportal-btn,
  .mobile-app-btn {
    padding: 8px 12px;
    font-size: 11px;
    gap: 8px;
    border-radius: 16px;
  }
  
  .geoportal-icon,
  .mobile-app-icon {
    width: 14px;
    height: 14px;
  }
  
  .arrow-icon,
  .mobile-arrow-icon {
    width: 10px;
    height: 10px;
  }
  
  .sidebar-nav {
    padding: 14px 0;
  }
  
  .nav-item {
    margin-bottom: 4px;
    padding: 0 12px;
  }
  
  .nav-link {
    padding: 10px 14px;
    gap: 0px;  /* Eliminado completamente el espacio */
    border-radius: 10px;
    min-height: 46px;
  }
  
  .nav-icon {
    width: 14px;  /* Ajustado para móvil pequeño */
    height: 14px;
  }
  
  .nav-text {
    font-size: 12px;  /* Aumentado significativamente el tamaño para móvil pequeño */
    font-weight: 400;  /* Normal (sin negritas) para móvil pequeño */
    font-family: 'Arial', 'Helvetica', 'Segoe UI', sans-serif;
    white-space: normal;
    word-wrap: break-word;
    line-height: 1.2;
  }
  
  .sidebar-footer {
    padding: 12px 12px 16px;
  }
  
  .logout-btn {
    padding: 10px 14px;
    font-size: 11px;
    gap: 8px;
    border-radius: 10px;
  }
  
  .logout-icon {
    width: 14px;
    height: 14px;
  }
}

/* Ajustes para pantallas extra pequeñas */
@media (max-width: 320px) {
  .sidebar-header {
    padding: 10px 8px 12px;
  }
  
  .flower-animation {
    width: 28px;
    height: 28px;
  }
  
  .brand-title {
    font-size: 10px;
    letter-spacing: 0.06em;
  }
  
  .brand-subtitle {
    font-size: 8px;
  }
  
  .geoportal-section {
    padding: 8px 8px 12px;
  }
  
  .geoportal-btn,
  .mobile-app-btn {
    padding: 6px 10px;
    font-size: 10px;
    gap: 6px;
  }
  
  .nav-item {
    padding: 0 8px;
  }
  
  .nav-link {
    padding: 8px 10px;
    gap: 0px;  /* Eliminado completamente el espacio */
    min-height: 44px;
  }
  
  .nav-icon {
    width: 12px;  /* Ajustado para móviles muy pequeños */
    height: 12px;
  }
  
  .nav-text {
    font-size: 11px;  /* Aumentado significativamente el tamaño para móvil muy pequeño */
    font-weight: 400;  /* Normal (sin negritas) para móvil muy pequeño */
    font-family: 'Arial', 'Helvetica', 'Segoe UI', sans-serif;
    white-space: normal;
    word-wrap: break-word;
    line-height: 1.2;
  }
  
  .sidebar-footer {
    padding: 8px 8px 12px;
  }
  
  .logout-btn {
    padding: 8px 10px;
    font-size: 10px;
    gap: 6px;
  }
  
  .logout-icon {
    width: 12px;
    height: 12px;
  }
}

/* Mejoras para scrolling en móviles */
@media (max-width: 768px) {
  .sidebar {
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    -ms-overflow-style: none;
  }
  
  .sidebar::-webkit-scrollbar {
    display: none;
  }
  
  .sidebar-nav {
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    -ms-overflow-style: none;
  }
  
  .sidebar-nav::-webkit-scrollbar {
    display: none;
  }
}

/* Estilos del Modal de Logout */
.logout-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  padding: 20px;
  animation: overlayFadeIn 0.3s ease-out;
}

@keyframes overlayFadeIn {
  from {
    opacity: 0;
    backdrop-filter: blur(0px);
  }
  to {
    opacity: 1;
    backdrop-filter: blur(8px);
  }
}

.logout-modal {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  max-width: 400px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  animation: modalSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.8) translateY(30px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  padding: 30px 30px 20px;
  text-align: center;
  border-bottom: 1px solid rgba(76, 175, 80, 0.1);
}

.modal-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto 16px;
  background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: iconPulse 2s ease-in-out infinite;
}

@keyframes iconPulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 0 10px rgba(76, 175, 80, 0);
  }
}

.modal-icon svg {
  width: 28px;
  height: 28px;
  color: white;
}

.modal-header h3 {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #2E7D32;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.modal-body {
  padding: 20px 30px;
  text-align: center;
}

.modal-body p {
  margin: 0;
  font-size: 16px;
  color: #555;
  line-height: 1.5;
}

.modal-actions {
  padding: 20px 30px 30px;
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-cancel,
.btn-confirm {
  flex: 1;
  padding: 12px 20px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  min-width: 120px;
}

.btn-cancel {
  background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
  color: #666;
  border: 2px solid rgba(0, 0, 0, 0.1);
}

.btn-cancel:hover {
  background: linear-gradient(135deg, #eeeeee 0%, #d5d5d5 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-confirm {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}

.btn-confirm:hover {
  background: linear-gradient(135deg, #45a049 0%, #388e3c 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.btn-confirm::before,
.btn-cancel::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn-confirm:hover::before,
.btn-cancel:hover::before {
  left: 100%;
}

.btn-confirm:active,
.btn-cancel:active {
  transform: translateY(0);
}

/* Responsive Design para modal de logout */
@media (max-width: 480px) {
  .logout-modal {
    margin: 10px;
    border-radius: 16px;
    max-width: calc(100vw - 20px);
  }
  
  .modal-header {
    padding: 20px 16px 12px;
  }
  
  .modal-icon {
    width: 50px;
    height: 50px;
    margin-bottom: 12px;
  }
  
  .modal-icon svg {
    width: 24px;
    height: 24px;
  }
  
  .modal-header h3 {
    font-size: 18px;
  }
  
  .modal-body {
    padding: 12px 16px;
  }
  
  .modal-body p {
    font-size: 14px;
  }
  
  .modal-actions {
    padding: 12px 16px 20px;
    flex-direction: column;
    gap: 8px;
  }
  
  .btn-cancel,
  .btn-confirm {
    min-width: auto;
    padding: 12px 16px;
    font-size: 14px;
  }
}

@media (max-width: 360px) {
  .logout-modal {
    margin: 8px;
  }
  
  .modal-header {
    padding: 16px 12px 10px;
  }
  
  .modal-icon {
    width: 45px;
    height: 45px;
    margin-bottom: 10px;
  }
  
  .modal-icon svg {
    width: 22px;
    height: 22px;
  }
  
  .modal-header h3 {
    font-size: 16px;
  }
  
  .modal-body {
    padding: 10px 12px;
  }
  
  .modal-body p {
    font-size: 13px;
  }
  
  .modal-actions {
    padding: 10px 12px 16px;
  }
  
  .btn-cancel,
  .btn-confirm {
    padding: 10px 14px;
    font-size: 13px;
  }
}

/* Mejoras para accesibilidad táctil */
@media (max-width: 768px) {
  .nav-link,
  .geoportal-btn,
  .mobile-app-btn,
  .logout-btn {
    min-height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .btn-cancel,
  .btn-confirm {
    min-height: 44px;
    touch-action: manipulation;
  }
}

/* Reglas para zoom extremo y alta densidad de píxeles */
@media (max-width: 100vw) and (max-height: 100vh) {
  .sidebar {
    font-size: clamp(8px, 1vw, 16px);
    width: clamp(160px, 20vw, 240px);
  }
  
  .sidebar-header {
    padding: clamp(6px, 1.5vh, 28px) clamp(4px, 1vw, 20px) clamp(8px, 2vh, 32px);
    max-height: clamp(80px, 20vh, 160px);
  }
  
  .flower-animation {
    width: clamp(20px, 3vw, 48px);
    height: clamp(20px, 3vw, 48px);
  }
  
  .brand-title {
    font-size: clamp(8px, 1.2vw, 16px);
    letter-spacing: clamp(0.05em, 0.1vw, 0.15em);
  }
  
  .brand-subtitle {
    font-size: clamp(6px, 0.8vw, 12px);
  }
  
  .geoportal-section {
    padding: clamp(4px, 1vh, 16px) clamp(4px, 1vw, 16px) clamp(6px, 1.5vh, 20px);
    max-height: clamp(60px, 15vh, 120px);
  }
  
  .geoportal-btn,
  .mobile-app-btn {
    padding: clamp(4px, 0.8vh, 10px) clamp(6px, 1vw, 14px);
    font-size: clamp(8px, 0.9vw, 13px);
    min-height: clamp(28px, 3.5vh, 44px);
    border-radius: clamp(8px, 1.5vw, 20px);
  }
  
  .geoportal-icon,
  .mobile-app-icon {
    width: clamp(10px, 1.2vw, 16px);
    height: clamp(10px, 1.2vw, 16px);
  }
  
  .arrow-icon,
  .mobile-arrow-icon {
    width: clamp(8px, 1vw, 12px);
    height: clamp(8px, 1vw, 12px);
  }
  
  .sidebar-nav {
    padding: clamp(8px, 1.5vh, 24px) 0;
    min-height: clamp(200px, 40vh, 400px);
  }
  
  .nav-item {
    margin-bottom: clamp(2px, 0.5vh, 8px);
    padding: 0 clamp(4px, 1vw, 16px);
  }
  
  .nav-link {
    padding: clamp(6px, 1vh, 16px) clamp(8px, 1.5vw, 18px);
    gap: clamp(8px, 1.2vw, 16px);
    min-height: clamp(32px, 4vh, 52px);
    border-radius: clamp(6px, 1vw, 12px);
  }
  
  .nav-icon {
    width: clamp(11px, 1.4vw, 14px);  /* Ajustado para zoom */
    height: clamp(11px, 1.4vw, 14px);
  }
  
  .nav-text {
    font-size: clamp(8px, 1vw, 12px);  /* Ajustado para desktop amplio */
    font-family: 'Daytona', Arial, Helvetica, sans-serif;
  }
  
  .sidebar-footer {
    padding: clamp(6px, 1.2vh, 16px) clamp(6px, 1.2vw, 16px) clamp(8px, 1.6vh, 20px);
    max-height: clamp(60px, 12vh, 100px);
  }
  
  .logout-btn {
    padding: clamp(6px, 1vh, 12px) clamp(8px, 1.4vw, 16px);
    font-size: clamp(8px, 0.9vw, 13px);
    min-height: clamp(32px, 4vh, 48px);
    border-radius: clamp(6px, 1vw, 12px);
    gap: clamp(4px, 0.8vw, 10px);
  }
  
  .logout-icon {
    width: clamp(10px, 1.2vw, 16px);
    height: clamp(10px, 1.2vw, 16px);
  }
}

/* Ajustes para zoom de navegador */
@media screen and (-webkit-min-device-pixel-ratio: 1.25), 
       screen and (min-resolution: 120dpi) {
  .sidebar {
    font-size: clamp(10px, 1.1vw, 15px);
  }
  
  .brand-title {
    font-size: clamp(9px, 1.3vw, 15px);
  }
  
  .nav-text,
  .geoportal-text,
  .mobile-app-text,
  .logout-text {
    font-size: clamp(7px, 0.8vw, 10px);  /* Reducido para alta resolución */
    font-family: 'Daytona', Arial, Helvetica, sans-serif;  /* Cambiado a Daytona */
  }
}

/* Ajustes para zoom muy alto */
@media screen and (-webkit-min-device-pixel-ratio: 2), 
       screen and (min-resolution: 192dpi) {
  .sidebar {
    font-size: clamp(8px, 1vw, 14px);
    width: clamp(140px, 18vw, 220px);
  }
  
  .flower-animation {
    width: clamp(18px, 2.5vw, 40px);
    height: clamp(18px, 2.5vw, 40px);
  }
  
  .brand-title {
    font-size: clamp(7px, 1.1vw, 14px);
  }
  
  .brand-subtitle {
    font-size: clamp(5px, 0.7vw, 10px);
  }
  
  .nav-text,
  .geoportal-text,
  .mobile-app-text,
  .logout-text {
    font-size: clamp(5px, 0.7vw, 9px);  /* Reducido para zoom muy alto */
    font-family: 'Daytona', Arial, Helvetica, sans-serif;  /* Cambiado a Daytona */
  }
}

/* Manejo de contenido que se desborda */
@media (max-height: 500px) {
  .sidebar {
    font-size: clamp(8px, 1vw, 12px);
  }
  
  .sidebar-header {
    padding: clamp(4px, 1vh, 16px) clamp(6px, 1vw, 16px);
    max-height: 15vh;
  }
  
  .flower-animation {
    width: clamp(16px, 2.5vw, 32px);
    height: clamp(16px, 2.5vw, 32px);
  }
  
  .brand-title {
    font-size: clamp(7px, 1vw, 12px);
    padding-bottom: clamp(2px, 0.5vh, 6px);
  }
  
  .brand-subtitle {
    font-size: clamp(5px, 0.7vw, 9px);
  }
  
  .geoportal-section {
    padding: clamp(3px, 0.8vh, 12px) clamp(6px, 1vw, 12px);
    max-height: 12vh;
  }
  
  .geoportal-btn,
  .mobile-app-btn {
    padding: clamp(3px, 0.6vh, 8px) clamp(6px, 1vw, 12px);
    font-size: clamp(6px, 0.8vw, 10px);
    min-height: clamp(24px, 3vh, 36px);
    margin-top: clamp(3px, 0.8vh, 8px);
  }
  
  .nav-link {
    padding: clamp(4px, 0.8vh, 12px) clamp(8px, 1.2vw, 14px);
    min-height: clamp(28px, 3.5vh, 44px);
  }
  
  .nav-text {
    font-size: clamp(4px, 0.7vw, 10px);  /* Reducido para pantallas ultra anchas */
    font-family: 'Daytona', Arial, Helvetica, sans-serif;  /* Cambiado a Daytona */
  }
  
  .nav-icon {
    width: clamp(10px, 1.3vw, 12px);  /* Ajustado para pantallas ultra bajas */
    height: clamp(10px, 1.3vw, 12px);
  }
  
  .sidebar-footer {
    padding: clamp(4px, 1vh, 12px) clamp(6px, 1vw, 12px);
    max-height: 10vh;
  }
  
  .logout-btn {
    padding: clamp(4px, 0.8vh, 10px) clamp(6px, 1.2vw, 14px);
    font-size: clamp(6px, 0.8vw, 11px);
    min-height: clamp(28px, 3.5vh, 40px);
  }
}

/* Prevención de contenido oculto */
@media (max-height: 400px) {
  .sidebar {
    overflow-y: auto !important;
    height: 100vh;
  }
  
  .sidebar-header,
  .geoportal-section,
  .sidebar-footer {
    flex-shrink: 0;
  }
  
  .sidebar-nav {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
  }
  
  .brand-title {
    font-size: clamp(6px, 0.9vw, 10px);
    line-height: 1.1;
  }
  
  .brand-subtitle {
    font-size: clamp(4px, 0.6vw, 8px);
  }
  
  .nav-text,
  .geoportal-text,
  .mobile-app-text,
  .logout-text {
    font-size: clamp(3px, 0.5vw, 7px);  /* Reducido para pantallas mega anchas */
    font-family: 'Daytona', Arial, Helvetica, sans-serif;  /* Cambiado a Daytona */
  }
}

/* Animación de cierre */
.logout-modal-overlay.fade-out {
  animation: overlayFadeOut 0.3s ease-in;
}

.logout-modal-overlay.fade-out .logout-modal {
  animation: modalSlideOut 0.3s ease-in;
}

@keyframes overlayFadeOut {
  from {
    opacity: 1;
    backdrop-filter: blur(8px);
  }
  to {
    opacity: 0;
    backdrop-filter: blur(0px);
  }
}

@keyframes modalSlideOut {
  from {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
  to {
    opacity: 0;
    transform: scale(0.8) translateY(30px);
  }
}

/* Optimizaciones finales para escalado dinámico */
.sidebar * {
  box-sizing: border-box;
}

/* Asegurar que el texto nunca se corte */
.nav-text,
.geoportal-text,
.mobile-app-text,
.logout-text,
.brand-title,
.brand-subtitle {
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
}

/* Scroll suave en toda la aplicación */
.sidebar,
.sidebar-nav {
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.sidebar::-webkit-scrollbar,
.sidebar-nav::-webkit-scrollbar {
  display: none;
}

/* Mejora de rendimiento para animaciones */
.flower-animation,
.flower-icon,
.nav-glow,
.geoportal-glow,
.mobile-app-glow,
.logout-glow {
  transform: translateZ(0);
  backface-visibility: hidden;
  perspective: 1000px;
}

.sidebar {
  will-change: transform;
  contain: layout style paint;
}

/* Estados hover optimizados para zoom */
@media (hover: hover) and (pointer: fine) {
  .nav-link:hover,
  .geoportal-btn:hover,
  .mobile-app-btn:hover,
  .logout-btn:hover {
    transform: translateX(2px) scale(1.01);
  }
}

/* Estados activos para touch */
@media (hover: none) and (pointer: coarse) {
  .nav-link:active,
  .geoportal-btn:active,
  .mobile-app-btn:active,
  .logout-btn:active {
    transform: scale(0.98);
  }
}

/* Prevención de zoom accidental en iOS */
@media screen and (-webkit-min-device-pixel-ratio: 0) {
  .sidebar input,
  .sidebar button,
  .sidebar select,
  .sidebar textarea {
    font-size: clamp(16px, 1.2vw, 16px);
  }
}
</style>
