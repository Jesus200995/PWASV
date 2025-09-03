import { createRouter, createWebHistory } from 'vue-router'
import authService from '../services/authService'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import UsuariosView from '../views/UsuariosView.vue'
import HistorialesView from '../views/HistorialesView.vue'
import RegistrosView from '../views/RegistrosView.vue'
import ConfiguracionView from '../views/ConfiguracionView.vue'
import AsistenciaView from '../views/AsistenciaView.vue'
import VisorMapView from '../views/VisorMap.vue'
import NotificacionesView from '../views/NotificacionesView.vue'
import PermisosView from '../views/PermisosView.vue'

const routes = [
  {
    path: '/',
    redirect: '/visor-map'
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
    meta: { requiresAuth: true, requiresAdmin: true }
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
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/notificaciones',
    name: 'Notificaciones',
    component: NotificacionesView,
    meta: { requiresAuth: true }
  },
  {
    path: '/permisos',
    name: 'Permisos',
    component: PermisosView,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/visor-map',
    name: 'VisorMap',
    component: VisorMapView,
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
router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('admin_token')
  const isAuthenticated = !!token
  
  // Verificar si la ruta requiere autenticación
  if (to.meta.requiresAuth && !isAuthenticated) {
    console.log('🔒 Redirigiendo a login - No autenticado')
    next('/login')
    return
  }
  
  // Si está autenticado y va al login, redirigir al dashboard
  if (to.name === 'Login' && isAuthenticated) {
    console.log('🔄 Ya autenticado, redirigiendo al mapa')
    next('/visor-map')
    return
  }
  
  // Verificar permisos de admin si la ruta lo requiere
  if (to.meta.requiresAdmin && isAuthenticated) {
    const userRole = authService.getUserRole()
    
    if (userRole !== 'admin') {
      console.log('🚫 Acceso denegado - Se requiere rol de administrador')
      console.log('👤 Rol del usuario:', userRole)
      
      // Redirigir a una ruta accesible
      if (from.path !== '/' && from.path !== '/login') {
        // Si viene de una ruta válida, volver a ella
        next(from.path)
      } else {
        // Si no, ir al visor de mapa
        next('/visor-map')
      }
      return
    }
  }
  
  console.log('✅ Navegación permitida a:', to.path)
  next()
})

export default router
