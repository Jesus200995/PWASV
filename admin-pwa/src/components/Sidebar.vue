<template>
  <div class="sidebar">
    <!-- Efecto liquid glass background -->
    <div class="liquid-bg">
      <div class="liquid-shape shape-1"></div>
      <div class="liquid-shape shape-2"></div>
      <div class="liquid-shape shape-3"></div>
    </div>
    
    <div class="sidebar-header">
      <div class="logo">🌱</div>
      <div class="logo-text">
        <h2>Sembrando Vida</h2>
        <p>Admin Panel</p>
      </div>
    </div>
      <nav class="sidebar-nav">
      <ul>
        <li class="nav-item" :class="{ active: $route.name === 'Dashboard' }">
          <router-link to="/dashboard" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
              </svg>
            </div>
            <span class="nav-text">Dashboard</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
        
        <li class="nav-item" :class="{ active: $route.name === 'Registros' }">
          <router-link to="/registros" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
              </svg>
            </div>
            <span class="nav-text">Registros</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
        
        <li class="nav-item" :class="{ active: $route.name === 'Usuarios' }">
          <router-link to="/usuarios" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M16 17V19H2V17S2 13 9 13 16 17 16 17M12.5 7.5A3.5 3.5 0 1 0 9 11A3.5 3.5 0 0 0 12.5 7.5M15.94 13A5.32 5.32 0 0 1 18 17V19H22V17S22 13.37 15.94 13M15 4A3.39 3.39 0 0 0 13.07 4.59A5 5 0 0 1 13.07 10.41A3.39 3.39 0 0 0 15 11A3.5 3.5 0 0 0 15 4Z"/>
              </svg>
            </div>
            <span class="nav-text">Usuarios</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
        
        <li class="nav-item" :class="{ active: $route.name === 'Configuracion' }">
          <router-link to="/configuracion" class="nav-link">
            <div class="nav-icon-wrapper">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.22,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.22,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.68 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"/>
              </svg>
            </div>
            <span class="nav-text">Configuración</span>
            <div class="nav-glow"></div>
          </router-link>
        </li>
      </ul>
    </nav>
    
    <div class="sidebar-footer">
      <button @click="$emit('logout')" class="logout-btn">
        <div class="btn-icon-wrapper">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M16,17V14H9V10H16V7L21,12L16,17M14,2A2,2 0 0,1 16,4V6H14V4H5V20H14V18H16V20A2,2 0 0,1 14,22H5A2,2 0 0,1 3,20V4A2,2 0 0,1 5,2H14Z"/>
          </svg>
        </div>
        <span class="nav-text">Cerrar Sesión</span>
        <div class="btn-glow"></div>
      </button>
    </div>
  </div>
</template>

<script setup>
defineEmits(['logout'])
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 280px;
  background: linear-gradient(135deg, 
    rgba(76, 175, 80, 0.95) 0%, 
    rgba(56, 142, 60, 0.95) 50%, 
    rgba(46, 125, 50, 0.95) 100%);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  display: flex;
  flex-direction: column;
  z-index: 1000;
  overflow: hidden;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

/* Efecto liquid glass background */
.liquid-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: -1;
}

.liquid-shape {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(45deg, 
    rgba(255, 255, 255, 0.1) 0%, 
    rgba(255, 255, 255, 0.05) 100%);
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 200px;
  height: 200px;
  top: -50px;
  right: -50px;
  animation-delay: 0s;
}

.shape-2 {
  width: 150px;
  height: 150px;
  bottom: 100px;
  left: -30px;
  animation-delay: 2s;
}

.shape-3 {
  width: 100px;
  height: 100px;
  top: 50%;
  right: -20px;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% { 
    transform: translateY(0px) scale(1);
    opacity: 0.7;
  }
  50% { 
    transform: translateY(-20px) scale(1.1);
    opacity: 1;
  }
}

.sidebar-header {
  padding: 32px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
}

.sidebar-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 24px;
  right: 24px;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.3) 50%, 
    transparent 100%);
}

.logo {
  font-size: 36px;
  min-width: 36px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.logo-text h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.logo-text p {
  margin: 0;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.sidebar-nav {
  flex: 1;
  padding: 24px 0;
}

.sidebar-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin-bottom: 8px;
  padding: 0 16px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 16px;
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  border-radius: 12px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  transform: translateX(4px);
}

.nav-link:hover .nav-glow {
  opacity: 1;
  transform: scale(1);
}

.nav-item.active .nav-link {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  color: white;
  box-shadow: 
    0 4px 15px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

/* Estilos específicos para router-link */
.nav-link.router-link-active,
.nav-link.router-link-exact-active {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  color: white;
  box-shadow: 
    0 4px 15px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.nav-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  position: relative;
}

.nav-icon {
  width: 20px;
  height: 20px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.nav-text {
  font-size: 15px;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.nav-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  border-radius: 12px;
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  transition: all 0.3s ease;
  pointer-events: none;
}

.sidebar-footer {
  padding: 20px 16px 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  display: flex;
  justify-content: center;
}

.sidebar-footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 24px;
  right: 24px;
  height: 1px;
  background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.3) 50%, 
    transparent 100%);
}

.logout-btn {
  width: 100%;
  background: linear-gradient(135deg, 
    rgba(244, 67, 54, 0.9) 0%, 
    rgba(211, 47, 47, 0.9) 100%);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 14px 16px;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 15px rgba(244, 67, 54, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.logout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 6px 20px rgba(244, 67, 54, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.logout-btn:hover .btn-glow {
  opacity: 1;
  transform: scale(1);
}

.logout-btn:active {
  transform: translateY(0);
}

.btn-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
}

.btn-glow {
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

/* Scrollbar personalizado */
.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* Responsive para pantallas muy pequeñas */
@media (max-width: 480px) {
  .sidebar {
    width: 100%;
  }
}

.logout-btn {
  color: white;
  padding: 14px 16px;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 4px 15px rgba(244, 67, 54, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.logout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 6px 20px rgba(244, 67, 54, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.logout-btn:hover .btn-glow {
  opacity: 1;
  transform: scale(1);
}

.logout-btn:active {
  transform: translateY(0);
}

.btn-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
}

.btn-glow {
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

.mobile-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 999;
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    width: 280px;
  }
  
  .sidebar.collapsed {
    transform: translateX(-100%);
  }
  
  .sidebar:not(.collapsed) {
    transform: translateX(0);
  }
  
  .mobile-overlay {
    display: block;
  }
  
  .sidebar-toggle {
    display: block;
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 1002;
  }
}

/* Scrollbar personalizado para la navegación */
.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>
