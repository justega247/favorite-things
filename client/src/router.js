import Vue from 'vue'
import VueRouter from 'vue-router'
import Landing from './theme/Landing.vue'
import Category from './theme/Category.vue'
import Favorites from './theme/Favorites.vue'
import NotFound from './theme/NotFound.vue'
import CreateEditFavorite from './theme/CreateEditFavorite.vue'
import { frontendRoutes } from './constants/routes'

Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  linkActiveClass: 'is-active',
  scrollBehavior: (to, from, savedPosition) => ({ y: 0 }),
  routes: [
    { path: frontendRoutes.VIEW_CATEGORIES, name: 'categories', component: Category },
    { path: frontendRoutes.LANDING, name: 'landing', component: Landing },
    { path: frontendRoutes.VIEW_CATEGORY_FAVORITES, name: 'category-favorites', component: Favorites },
    { path: frontendRoutes.CREATE_FAVORITE, name: 'favorite', component: CreateEditFavorite },
    { path: '*', component: NotFound }
  ]
})

export default router
