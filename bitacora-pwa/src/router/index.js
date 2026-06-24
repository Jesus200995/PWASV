import { createRouter, createWebHistory } from 'vue-router'
import { isLoggedIn } from '../services/api.js'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', component: LoginView },
  { path: '/dashboard', component: DashboardView, meta: { auth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _, next) => {
  if (to.meta.auth && !isLoggedIn()) return next('/login')
  if (to.path === '/login' && isLoggedIn()) return next('/dashboard')
  next()
})

export default router
