import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import IncomeView from '../views/IncomeView.vue'
import ExpenseView from '../views/ExpenseView.vue'
const routes = [
  {
    path: '/',
    name: 'home',
    component: LoginView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/main',
    name: 'main',
    component: HomeView
  },
  {
    path: '/income',
    name: 'income',
    component: IncomeView
  },
  {
    path: '/expense',
    name: 'expense',
    component: ExpenseView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
