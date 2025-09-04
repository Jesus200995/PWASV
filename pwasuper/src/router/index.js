import { createRouter, createWebHistory } from 'vue-router'
import maintenanceCheckService from '../services/maintenanceCheckService.js'

import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import ForgotPassword from '../views/ForgotPassword.vue'
import Home from '../views/Home.vue'
import Historial from '../views/Historial.vue'
import Profile from '../views/Profile.vue'
import Notificaciones from '../views/Notificaciones.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/forgot-password', name: 'ForgotPassword', component: ForgotPassword },
  { path: '/historial', name: 'Historial', component: Historial },
  { path: '/profile', name: 'Profile', component: Profile },
  { path: '/notificaciones', name: 'Notificaciones', component: Notificaciones }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navegación para proteger rutas
router.beforeEach(async (to, from, next) => {
  console.log(`🧭 Navegando de ${from.name || 'unknown'} a ${to.name || 'unknown'}`);
  
  // PRIMERA PRIORIDAD: Verificar modo mantenimiento
  try {
    const maintenanceStatus = await maintenanceCheckService.checkMaintenanceStatus();
    console.log('🔧 Estado de mantenimiento en router:', maintenanceStatus);
    
    if (maintenanceStatus.enabled) {
      console.log('🚨 MODO MANTENIMIENTO ACTIVO - Bloqueando navegación');
      
      // Si estamos en modo mantenimiento, almacenar el estado globalmente
      window.maintenanceMode = {
        enabled: true,
        message: maintenanceStatus.message
      };
      
      // NO permitir navegación a ninguna vista
      // La pantalla de mantenimiento se mostrará desde App.vue
      next(false); // Bloquear la navegación
      return;
    } else {
      // Si no hay mantenimiento, limpiar el estado global
      window.maintenanceMode = {
        enabled: false,
        message: ''
      };
    }
  } catch (error) {
    console.error('❌ Error verificando mantenimiento en router:', error);
    // En caso de error, asumir que NO hay mantenimiento para permitir funcionamiento
    window.maintenanceMode = {
      enabled: false,
      message: ''
    };
  }
  
  // SEGUNDA PRIORIDAD: Verificar autenticación (solo si no hay mantenimiento)
  const user = localStorage.getItem('user')
  const isLoggedIn = !!user
  
  // Si intenta acceder a login, register o forgot-password y ya está logueado, redirigir a home
  if ((to.name === 'Login' || to.name === 'Register' || to.name === 'ForgotPassword') && isLoggedIn) {
    next({ name: 'Home' })
  }
  // Si intenta acceder a rutas protegidas sin estar logueado, redirigir a login
  else if ((to.name === 'Home' || to.name === 'Historial' || to.name === 'Profile' || to.name === 'Notificaciones') && !isLoggedIn) {
    next({ name: 'Login' })
  }
  // En cualquier otro caso, permitir la navegación
  else {
    next()
  }
})

export default router
