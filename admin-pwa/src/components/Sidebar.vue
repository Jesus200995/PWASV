<template>
  <aside class="sidebar" :class="{ 'active': isOpen }">
    <div class="sidebar-header">
      <div class="sidebar-logo">
        <span class="logo-icon">🌱</span>
        <span class="logo-text">Sembrando Vida</span>
      </div>
      <button class="sidebar-close" @click="$emit('close')">
        <span>×</span>
      </button>
    </div>
    
    <nav class="sidebar-nav">
      <ul class="sidebar-menu">
        <li :class="{ 'active': activeSection === 'dashboard' }">
          <a href="#" @click.prevent="navigate('dashboard')">
            <span class="menu-icon">📊</span>
            <span class="menu-text">Dashboard</span>
          </a>
        </li>
        <li :class="{ 'active': activeSection === 'registros' }">
          <a href="#" @click.prevent="navigate('registros')">
            <span class="menu-icon">📋</span>
            <span class="menu-text">Registros</span>
          </a>
        </li>
        <li :class="{ 'active': activeSection === 'usuarios' }">
          <a href="#" @click.prevent="navigate('usuarios')">
            <span class="menu-icon">👥</span>
            <span class="menu-text">Usuarios</span>
          </a>
        </li>
        <li class="menu-separator"></li>
        <li class="logout-item">
          <a href="#" @click.prevent="$emit('logout')">
            <span class="menu-icon">🚪</span>
            <span class="menu-text">Cerrar Sesión</span>
          </a>
        </li>
      </ul>
    </nav>
  </aside>
</template>

<script setup>
// Props
defineProps({
  isOpen: Boolean,
  activeSection: String
})

// Emits
defineEmits(['toggle', 'close', 'navigate', 'logout'])

// Métodos
const navigate = (section) => {
  emit('navigate', section)
}

// Obtener emit function
const emit = defineEmits(['navigate', 'logout'])
</script>

<style scoped>
.sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #e2e8f0;
  box-shadow: 2px 0 8px rgba(0,0,0,0.1);
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
  z-index: 1000;
  transform: translateX(0);
  transition: transform 0.3s ease;
  overflow-y: auto;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 32px;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  color: #1a202c;
}

.sidebar-close {
  display: none;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #718096;
  padding: 4px;
  border-radius: 4px;
}

.sidebar-close:hover {
  background: #f7fafc;
  color: #2d3748;
}

.sidebar-nav {
  padding: 20px 0;
}

.sidebar-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-menu li {
  margin: 0;
}

.sidebar-menu li a {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  text-decoration: none;
  color: #4a5568;
  transition: all 0.2s ease;
  border-left: 3px solid transparent;
}

.sidebar-menu li:hover a,
.sidebar-menu li.active a {
  background: linear-gradient(90deg, #f0fff4, #f7fafc);
  color: #4CAF50;
  border-left-color: #4CAF50;
}

.menu-icon {
  font-size: 18px;
  width: 20px;
  text-align: center;
}

.menu-text {
  font-weight: 500;
  font-size: 14px;
}

.menu-separator {
  height: 1px;
  background: #e2e8f0;
  margin: 20px 20px;
}

.logout-item a {
  color: #e53e3e !important;
}

.logout-item:hover a {
  background: linear-gradient(90deg, #fff5f5, #f7fafc) !important;
  border-left-color: #e53e3e !important;
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
  }
  
  .sidebar.active {
    transform: translateX(0);
  }
  
  .sidebar-close {
    display: block;
  }
}
</style>
