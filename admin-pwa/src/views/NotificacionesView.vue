<template>
  <div class="notificaciones-container">
    <Sidebar @logout="logout" />
    
    <main class="main-content">
      <header class="page-header">
        <div class="header-content">
          <div class="header-main">
            <div class="header-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                <circle cx="18" cy="6" r="3" fill="#ff4757" opacity="0.9"/>
                <circle cx="18" cy="6" r="1.5" fill="#ffffff" opacity="0.8"/>
              </svg>
            </div>
            <div class="header-text">
              <h1 class="header-title">Centro de Notificaciones</h1>
              <p class="header-subtitle">Gestiona todas las notificaciones y alertas del sistema</p>
            </div>
          </div>
          <div class="header-actions">
            <div class="connection-status" :class="{ 'online': isOnline, 'offline': !isOnline }">
              <div class="status-indicator"></div>
              <span class="status-text">{{ isOnline ? 'En línea' : 'Sin conexión' }}</span>
            </div>
          </div>
        </div>
      </header>

      <div class="page-content">
        <!-- Mensaje de desarrollo -->
        <div class="development-notice">
          <div class="development-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#4CAF50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 6v6"/>
              <path d="M12 16h.01"/>
              <path d="M8 12l2-2 4 4 6-6"/>
            </svg>
          </div>
          <h2 class="development-title">🚧 Función en Desarrollo</h2>
          <p class="development-description">
            El sistema de notificaciones está actualmente en fase de desarrollo. 
            Próximamente podrás recibir y gestionar notificaciones importantes sobre:
          </p>
          
          <div class="features-grid">
            <div class="feature-card">
              <div class="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 6L9 17l-5-5"/>
                </svg>
              </div>
              <div class="feature-info">
                <h3>Alertas de Asistencia</h3>
                <p>Notificaciones sobre registros de entrada y salida</p>
              </div>
            </div>
            
            <div class="feature-card">
              <div class="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                </svg>
              </div>
              <div class="feature-info">
                <h3>Actualizaciones de Usuario</h3>
                <p>Cambios en perfiles y nuevos registros</p>
              </div>
            </div>
            
            <div class="feature-card">
              <div class="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
              </div>
              <div class="feature-info">
                <h3>Alertas de Ubicación</h3>
                <p>Notificaciones sobre registros fuera de zona</p>
              </div>
            </div>
            
            <div class="feature-card">
              <div class="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12,6 12,12 16,14"/>
                </svg>
              </div>
              <div class="feature-info">
                <h3>Recordatorios</h3>
                <p>Avisos sobre horarios y actividades pendientes</p>
              </div>
            </div>
            
            <div class="feature-card">
              <div class="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14,2 14,8 20,8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                </svg>
              </div>
              <div class="feature-info">
                <h3>Reportes Automáticos</h3>
                <p>Notificaciones sobre informes generados</p>
              </div>
            </div>
            
            <div class="feature-card">
              <div class="feature-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="3"/>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
                </svg>
              </div>
              <div class="feature-info">
                <h3>Configuración del Sistema</h3>
                <p>Alertas sobre cambios importantes en el sistema</p>
              </div>
            </div>
          </div>
          
          <div class="development-status">
            <div class="status-bar">
              <div class="status-progress"></div>
            </div>
            <p class="status-text">Progreso del desarrollo: <strong>75%</strong></p>
            <p class="status-eta">Fecha estimada de lanzamiento: <strong>Próxima actualización</strong></p>
          </div>
          
          <div class="contact-info">
            <p class="contact-text">
              ¿Tienes sugerencias para el sistema de notificaciones? 
              <a href="mailto:soporte@sembrandodatos.com" class="contact-link">Contáctanos</a>
            </p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import Sidebar from '../components/Sidebar.vue'

export default {
  name: 'NotificacionesView',
  components: {
    Sidebar
  },
  data() {
    return {
      isOnline: navigator.onLine
    }
  },
  mounted() {
    this.configurarEventosConexion()
  },
  methods: {
    configurarEventosConexion() {
      window.addEventListener('online', () => {
        this.isOnline = true
      })
      
      window.addEventListener('offline', () => {
        this.isOnline = false
      })
    },
    
    logout() {
      localStorage.removeItem('admin_token')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

.notificaciones-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fffe 0%, #e8f5e8 100%);
}

.main-content {
  flex: 1;
  margin-left: min(220px, 18vw);
  max-width: calc(100vw - min(220px, 18vw));
  min-width: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* === HEADER STYLES === */
.page-header {
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 50%, #2E7D32 100%);
  color: white;
  padding: 16px 24px;
  box-shadow: 
    0 2px 8px rgba(76, 175, 80, 0.3),
    0 4px 16px rgba(76, 175, 80, 0.15);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
}

.header-main {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.header-icon svg {
  width: 20px;
  height: 20px;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

.header-icon:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 12px 48px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.header-text {
  flex: 1;
}

.header-title {
  font-size: 20px;
  font-weight: 700;
  margin: 0 0 4px 0;
  background: linear-gradient(135deg, #ffffff 0%, #e8f5e8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-family: 'Inter', sans-serif;
}

.header-subtitle {
  font-size: 13px;
  opacity: 0.9;
  margin: 0;
  font-weight: 400;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  font-family: 'Inter', sans-serif;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.status-indicator {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.connection-status.online .status-indicator {
  background: #66BB6A;
  box-shadow: 0 0 8px rgba(102, 187, 106, 0.6);
}

.connection-status.offline .status-indicator {
  background: #FF7043;
  box-shadow: 0 0 8px rgba(255, 112, 67, 0.6);
}

.status-text {
  font-size: 12px;
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* === CONTENT STYLES === */
.page-content {
  flex: 1;
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.development-notice {
  background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
  border-radius: 16px;
  padding: 32px;
  text-align: center;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.08),
    0 4px 16px rgba(0, 0, 0, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(76, 175, 80, 0.1);
  position: relative;
  overflow: hidden;
}

.development-notice::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #4CAF50 0%, #45a049 50%, #2E7D32 100%);
}

.development-icon {
  margin: 0 auto 16px;
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.15);
}

.development-title {
  font-size: 22px;
  font-weight: 700;
  color: #2E7D32;
  margin: 0 0 12px 0;
  font-family: 'Inter', sans-serif;
}

.development-description {
  font-size: 15px;
  color: #666;
  line-height: 1.6;
  margin: 0 0 24px 0;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
  font-family: 'Inter', sans-serif;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
  margin: 24px 0;
}

.feature-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
  padding: 16px;
  border-radius: 12px;
  border: 1px solid rgba(76, 175, 80, 0.1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  display: flex;
  gap: 12px;
  text-align: left;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  border-color: rgba(76, 175, 80, 0.2);
}

.feature-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.feature-info h3 {
  font-size: 14px;
  font-weight: 600;
  color: #2E7D32;
  margin: 0 0 6px 0;
  font-family: 'Inter', sans-serif;
}

.feature-info p {
  font-size: 13px;
  color: #666;
  margin: 0;
  line-height: 1.4;
  font-family: 'Inter', sans-serif;
}

.development-status {
  margin: 24px 0;
  padding: 20px;
  background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
  border-radius: 16px;
  border: 1px solid rgba(76, 175, 80, 0.2);
}

.status-bar {
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 3px;
  overflow: hidden;
  margin: 0 0 12px 0;
}

.status-progress {
  height: 100%;
  width: 75%;
  background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
  border-radius: 3px;
  animation: progressGlow 2s ease-in-out infinite;
}

@keyframes progressGlow {
  0%, 100% { box-shadow: 0 0 6px rgba(76, 175, 80, 0.4); }
  50% { box-shadow: 0 0 12px rgba(76, 175, 80, 0.6); }
}

.status-text, .status-eta {
  font-size: 14px;
  color: #2E7D32;
  margin: 6px 0;
  font-family: 'Inter', sans-serif;
}

.contact-info {
  margin-top: 20px;
  padding: 16px;
  background: linear-gradient(135deg, #ffffff 0%, #f0fff4 100%);
  border-radius: 12px;
  border: 1px solid rgba(76, 175, 80, 0.1);
}

.contact-text {
  font-size: 14px;
  color: #666;
  margin: 0;
  font-family: 'Inter', sans-serif;
}

.contact-link {
  color: #4CAF50;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.contact-link:hover {
  color: #2E7D32;
  text-decoration: underline;
}

/* === RESPONSIVE DESIGN === */
@media (max-width: 1200px) {
  .main-content {
    margin-left: 260px;
    max-width: calc(100vw - 260px);
  }
}

@media (max-width: 1024px) {
  .main-content {
    margin-left: 240px;
    max-width: calc(100vw - 240px);
  }
  
  .page-content {
    padding: 24px;
  }
  
  .development-notice {
    padding: 32px 24px;
  }
  
  .features-grid {
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
  }
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    max-width: 100vw;
  }
  
  .page-header {
    padding: 12px 16px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
  
  .header-main {
    flex-direction: column;
    gap: 8px;
  }
  
  .header-title {
    font-size: 18px;
  }
  
  .header-subtitle {
    font-size: 12px;
  }
  
  .page-content {
    padding: 16px;
  }
  
  .development-notice {
    padding: 20px 16px;
  }
  
  .development-title {
    font-size: 20px;
  }
  
  .development-description {
    font-size: 14px;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .feature-card {
    padding: 12px;
  }
  
  .development-status {
    padding: 16px;
  }
}

@media (max-width: 480px) {
  .page-header {
    padding: 12px;
  }
  
  .header-icon {
    width: 32px;
    height: 32px;
  }
  
  .header-icon svg {
    width: 16px;
    height: 16px;
  }
  
  .development-notice {
    padding: 16px 12px;
  }
  
  .development-icon {
    width: 48px;
    height: 48px;
  }
  
  .development-title {
    font-size: 18px;
  }
  
  .development-description {
    font-size: 13px;
  }
  
  .feature-card {
    padding: 12px;
    gap: 10px;
  }
  
  .feature-icon {
    width: 32px;
    height: 32px;
  }
  
  .feature-info h3 {
    font-size: 13px;
  }
  
  .feature-info p {
    font-size: 12px;
  }
}
</style>
