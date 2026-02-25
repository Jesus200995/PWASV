import { createRouter, createWebHistory } from 'vue-router'
import authService from '../services/authService'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import UsuariosView from '../views/UsuariosView.vue'
import HistorialesView from '../views/HistorialesView.vue'
import ReportesView from '../views/ReportesView.vue'
import RegistrosView from '../views/RegistrosView.vue'
import ConfiguracionView from '../views/ConfiguracionView.vue'
import AsistenciaView from '../views/AsistenciaView.vue'
import VisorMapView from '../views/VisorMap.vue'
import NotificacionesView from '../views/NotificacionesView.vue'
// import NotificacionesIndividualesView from '../views/NotificacionesIndividualesView.vue' // YA NO SE USA - Fusionado en NotificacionesView con pestañas
import PermisosView from '../views/PermisosView.vue'
import ManualesView from '../views/ManualesView.vue'
import EstadisticasView from '../views/EstadisticasView.vue'

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
    path: '/reportes',
    name: 'Reportes',
    component: ReportesView,
    meta: { requiresAuth: true, requiredPermission: 'reportes' }
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
    path: '/debug-buscador',
    name: 'DebugBuscador',
    component: () => import('../views/DebugBuscadorView.vue'),
    meta: { requiresAuth: true }
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
  // {
  //   path: '/notificaciones-individuales',
  //   name: 'NotificacionesIndividuales',
  //   component: NotificacionesIndividualesView,
  //   meta: { requiresAuth: true, requiredPermission: 'notificaciones' }
  // }, // YA NO SE USA - Fusionado en NotificacionesView con pestañas
  {
    path: '/manuales',
    name: 'Manuales',
    component: ManualesView,
    meta: { requiresAuth: true, requiredPermission: 'manuales' }
  },
  {
    path: '/estadisticas',
    name: 'Estadisticas',
    component: EstadisticasView,
    meta: { requiresAuth: true, requiredPermission: 'estadisticas' }
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
  const rutasPorPrioridad = ['visor', 'asistencia', 'registros', 'historiales', 'notificaciones', 'manuales', 'usuarios', 'permisos', 'configuracion', 'reportes']
  const rutasMap = {
    'visor': '/visor-map',
    'asistencia': '/asistencia',
    'registros': '/registros',
    'historiales': '/historiales',
    'notificaciones': '/notificaciones',
    'manuales': '/manuales',
    'usuarios': '/usuarios',
    'permisos': '/permisos',
    'configuracion': '/configuracion',
    'reportes': '/reportes'
  }
  
  for (const permiso of rutasPorPrioridad) {
    if (authService.hasPermission(permiso)) {
      return rutasMap[permiso]
    }
  }
  
  return null
}

// Listener para cambios de permisos en tiempo real
if (typeof window !== 'undefined') {
  window.addEventListener('user-session-updated', (event) => {
    console.log('🔄 Router: Detectado cambio de permisos en tiempo real')
    
    // Actualizar authService.user desde localStorage
    authService.user = authService.getUserFromStorage()
    
    // Verificar si el usuario sigue teniendo acceso a la ruta actual
    const currentRoute = router.currentRoute.value
    const requiredPermission = currentRoute.meta?.requiredPermission
    
    if (requiredPermission) {
      const hasPermission = authService.hasPermission(requiredPermission)
      
      if (!hasPermission) {
        console.log(`🚫 Router: Permiso removido para ruta actual: ${requiredPermission}`)
        console.log('🔄 Router: Redirigiendo a ruta accesible...')
        
        // Buscar una ruta accesible
        const rutaAccesible = encontrarRutaAccesible()
        
        if (rutaAccesible) {
          router.push(rutaAccesible)
        } else {
          // Si no tiene acceso a nada, cerrar sesión
          console.log('⚠️ Router: Usuario sin permisos, cerrando sesión')
          authService.logout()
          router.push('/login')
        }
      } else {
        console.log(`✅ Router: Usuario mantiene acceso a ruta: ${requiredPermission}`)
      }
    }
  })
}

export default router
