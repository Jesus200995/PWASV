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
    meta: { requiresAuth: true, requiredPermission: 'usuarios' }
  },
  {
    path: '/historiales',
    name: 'Historiales',
    component: HistorialesView,
    meta: { requiresAuth: true, requiredPermission: 'historiales' }
  },
  {
    path: '/asistencia',
    name: 'Asistencia',
    component: AsistenciaView,
    meta: { requiresAuth: true, requiredPermission: 'asistencia' }
  },
  {
    path: '/registros',
    name: 'Registros',
    component: RegistrosView,
    meta: { requiresAuth: true, requiredPermission: 'registros' }
  },
  {
    path: '/configuracion',
    name: 'Configuracion',
    component: ConfiguracionView,
    meta: { requiresAuth: true, requiredPermission: 'configuracion' }
  },
  {
    path: '/notificaciones',
    name: 'Notificaciones',
    component: NotificacionesView,
    meta: { requiresAuth: true, requiredPermission: 'notificaciones' }
  },
  {
    path: '/permisos',
    name: 'Permisos',
    component: PermisosView,
    meta: { requiresAuth: true, requiredPermission: 'permisos' }
  },
  {
    path: '/visor-map',
    name: 'VisorMap',
    component: VisorMapView,
    meta: {
      requiresAuth: true,
      requiredPermission: 'visor'
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
  
  // Verificar permisos específicos si la ruta lo requiere
  if (to.meta.requiredPermission && isAuthenticated) {
    const hasPermission = authService.hasPermission(to.meta.requiredPermission)
    
    if (!hasPermission) {
      console.log(`🚫 Acceso denegado - No tiene permiso para: ${to.meta.requiredPermission}`)
      console.log('👤 Rol del usuario:', authService.getUserRole())
      console.log('📋 Permisos del usuario:', authService.getCurrentUser()?.permisos)
      
      // Buscar una ruta accesible para el usuario
      const rutaAccesible = encontrarRutaAccesible()
      
      if (from.path !== '/' && from.path !== '/login' && from.path !== to.path) {
        // Si viene de una ruta válida, volver a ella
        next(from.path)
      } else if (rutaAccesible) {
        // Si tiene acceso a alguna ruta, ir ahí
        next(rutaAccesible)
      } else {
        // Si no tiene acceso a nada, cerrar sesión
        console.log('⚠️ Usuario sin permisos, cerrando sesión')
        authService.logout()
        next('/login')
      }
      return
    }
  }
  
  console.log('✅ Navegación permitida a:', to.path)
  next()
})

// Función auxiliar para encontrar una ruta accesible
function encontrarRutaAccesible() {
  const rutasPorPrioridad = ['visor', 'asistencia', 'registros', 'historiales', 'notificaciones', 'usuarios', 'permisos', 'configuracion']
  const rutasMap = {
    'visor': '/visor-map',
    'asistencia': '/asistencia',
    'registros': '/registros',
    'historiales': '/historiales',
    'notificaciones': '/notificaciones',
    'usuarios': '/usuarios',
    'permisos': '/permisos',
    'configuracion': '/configuracion'
  }
  
  for (const permiso of rutasPorPrioridad) {
    if (authService.hasPermission(permiso)) {
      return rutasMap[permiso]
    }
  }
  
  return null
}

export default router
