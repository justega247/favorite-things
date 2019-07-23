import Vue from 'vue'
import VueRouter from 'vue-router'
import Landing from './theme/Landing.vue'
import Category from './theme/Category.vue'
import { frontendRoutes } from './constants/routes'

Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  linkActiveClass: 'is-active',
  scrollBehavior: (to, from, savedPosition) => ({ y: 0 }),
  routes: [
    { path: frontendRoutes.VIEW_CATEGORIES, component: Category },
    { path: frontendRoutes.LANDING, name: 'landing', component: Landing }
  ]
})

export default router
