import { createRouter, createWebHistory } from 'vue-router'

import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import Historial from '../views/Historial.vue'
import Profile from '../views/Profile.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/historial', name: 'Historial', component: Historial },
  { path: '/profile', name: 'Profile', component: Profile }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navegación para proteger rutas
router.beforeEach((to, from, next) => {
  const user = localStorage.getItem('user')
  const isLoggedIn = !!user
  
  // Si intenta acceder a login o register y ya está logueado, redirigir a home
  if ((to.name === 'Login' || to.name === 'Register') && isLoggedIn) {
    next({ name: 'Home' })
  }
  // Si intenta acceder a rutas protegidas sin estar logueado, redirigir a login
  else if ((to.name === 'Home' || to.name === 'Historial' || to.name === 'Profile') && !isLoggedIn) {
    next({ name: 'Login' })
  }
  // En cualquier otro caso, permitir la navegación
  else {
    next()
  }
})

export default router
