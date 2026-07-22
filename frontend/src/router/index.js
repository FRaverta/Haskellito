import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ChallengeView from '../views/ChallengeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/challenge',
    name: 'challenges',
    component: () => import('../views/ChallengesListView.vue')
  },
  {
    path: '/challenge/:id',
    name: 'challenge',
    component: ChallengeView
  },
  {
    path: '/auth/callback',
    name: 'auth-callback',
    component: () => import('../views/AuthCallbackView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
