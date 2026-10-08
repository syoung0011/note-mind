import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import { currentUser, isAuthReady, restoreAuth } from '@/services/auth'

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
    await restoreAuth()
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
