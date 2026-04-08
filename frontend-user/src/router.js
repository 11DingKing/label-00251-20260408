import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from './stores/auth'

const routes = [
  { path: '/', component: () => import('./views/Landing.vue'), meta: { guest: true } },
  { path: '/login', component: () => import('./views/Auth.vue'), meta: { guest: true } },
  { path: '/register', component: () => import('./views/Auth.vue'), meta: { guest: true } },
  { path: '/dashboard', component: () => import('./views/Dashboard.vue'), meta: { auth: true } },
  { path: '/wiki', component: () => import('./views/wiki/Index.vue'), meta: { auth: true } },
  { path: '/wiki/new', component: () => import('./views/wiki/Edit.vue'), meta: { auth: true } },
  { path: '/wiki/:slug', component: () => import('./views/wiki/View.vue'), meta: { auth: true } },
  { path: '/wiki/:slug/edit', component: () => import('./views/wiki/Edit.vue'), meta: { auth: true } },
  { path: '/ideas', component: () => import('./views/ideas/Index.vue'), meta: { auth: true } },
  { path: '/ideas/new', component: () => import('./views/ideas/Edit.vue'), meta: { auth: true } },
  { path: '/ideas/:id', component: () => import('./views/ideas/View.vue'), meta: { auth: true } },
  { path: '/ideas/:id/edit', component: () => import('./views/ideas/Edit.vue'), meta: { auth: true } },
  { path: '/chat', component: () => import('./views/chat/Index.vue'), meta: { auth: true } },
  { path: '/chat/room/:id', component: () => import('./views/chat/Room.vue'), meta: { auth: true } },
  { path: '/chat/private/:id', component: () => import('./views/chat/Private.vue'), meta: { auth: true } },
  { path: '/ai', component: () => import('./views/AI.vue'), meta: { auth: true } },
  { path: '/admin', component: () => import('./views/admin/Index.vue'), meta: { auth: true, admin: true } },
  { path: '/admin/users', component: () => import('./views/admin/Users.vue'), meta: { auth: true, admin: true } },
  { path: '/admin/ai', component: () => import('./views/admin/AISettings.vue'), meta: { auth: true, admin: true } },
  { path: '/profile', component: () => import('./views/Profile.vue'), meta: { auth: true } },
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()
  if (auth.token && !auth.user) await auth.fetchUser()
  
  if (to.meta.auth && !auth.isLoggedIn) return next('/login')
  if (to.meta.guest && auth.isLoggedIn) return next('/dashboard')
  if (to.meta.admin && !auth.isAdmin) return next('/dashboard')
  next()
})

export default router
