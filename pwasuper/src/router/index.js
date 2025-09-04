import { createRouter, createWebHistory } from 'vue-router'
import { isMaintenanceMode } from '../stores/maintenanceStore.js'

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
router.beforeEach((to, from, next) => {
  // PRIORIDAD 1: Verificar modo mantenimiento (bloquea TODA navegación)
  if (isMaintenanceMode.value) {
    console.log('🚫 Navegación bloqueada: Sistema en modo mantenimiento')
    next(false) // Bloquear completamente la navegación
    return
  }

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
