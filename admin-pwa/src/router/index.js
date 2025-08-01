import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import UsuariosView from '../views/UsuariosView.vue'
import HistorialesView from '../views/HistorialesView.vue'
import RegistrosView from '../views/RegistrosView.vue'
import ConfiguracionView from '../views/ConfiguracionView.vue'
import VisorView from '../views/VisorView.vue'
import AsistenciaView from '../views/AsistenciaView.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/usuarios',
    name: 'Usuarios',
    component: UsuariosView,
    meta: { requiresAuth: true }
  },
  {
    path: '/historiales',
    name: 'Historiales',
    component: HistorialesView,
    meta: { requiresAuth: true }
  },
  {
    path: '/asistencia',
    name: 'Asistencia',
    component: AsistenciaView,
    meta: { requiresAuth: true }
  },
  {
    path: '/registros',
    name: 'Registros',
    component: RegistrosView,
    meta: { requiresAuth: true }
  },
  {
    path: '/configuracion',
    name: 'Configuracion',
    component: ConfiguracionView,
    meta: { requiresAuth: true }
  },
  {
    path: '/visor',
    name: 'Visor',
    component: VisorView,
    meta: {
      requiresAuth: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navegación para proteger rutas
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('admin_token')
  const isAuthenticated = !!token
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.name === 'Login' && isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
