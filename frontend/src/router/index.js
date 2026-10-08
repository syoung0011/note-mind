import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import { currentUser, getToken, isAuthReady, restoreAuth } from '@/services/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach(async (to) => {
  if (!isAuthReady.value) {
    try {
      const hadToken = Boolean(getToken())
      const user = await restoreAuth()
      if (hadToken && !user && to.meta.requiresAuth) {
        return { name: 'login', query: { reason: 'expired' } }
      }
    } catch {
      // 暂时无法确认身份时不进入受保护页面；保留 Token 供刷新后重试。
      return { name: 'login', query: { reason: 'unavailable' } }
    }
  }

  if (to.meta.requiresAuth && !currentUser.value) {
    return { name: 'login' }
  }

  if (['login', 'register'].includes(to.name) && currentUser.value) {
    return { name: 'home' }
  }

  return true
})

export default router
