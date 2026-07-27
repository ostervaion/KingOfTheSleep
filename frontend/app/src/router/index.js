import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '../views/HomeView.vue'
import DashboardView from '../views/DashboardView.vue'
import AdminView from '../views/AdminView.vue'
import PrivacyPolicy from '@/views/PrivacyPolicy.vue'
import TermsUse from '@/views/TermsUse.vue'
import DashboardTourView from '../views/DashboardTourView.vue'
import ApiPlayground from '@/views/ApiPlayground.vue'
import ApiDocs from '@/views/ApiDocs.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/privacy',
      name: 'privacy',
      component: PrivacyPolicy,
    },
    {
      path: '/terms',
      name: 'terms',
      component: TermsUse,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true },
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
      meta: { requiresAuth: true },
    },
      {
      path: '/dashboard-tour',
      name: 'dashboard-tour',
      component: DashboardTourView,
      meta: { requiresAuth: true },
    },
    {
      path: '/public_api',
      name: 'public_api',
      component: ApiPlayground,
      meta: { requiresAuth: true },
    },
    {
      path: '/api_docs',
      name: 'api_docs',
      component: ApiDocs,
    },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
