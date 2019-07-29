import Vue from 'vue'
import VueRouter from 'vue-router'
import Landing from './theme/Landing.vue'
import Category from './theme/Category.vue'
import CategoryFavorites from './theme/CategoryFavorites.vue'
import NotFound from './theme/NotFound.vue'
import CreateFavorite from './theme/CreateFavorite.vue'
import EditFavorite from './theme/EditFavorite.vue'
import FavoriteDetail from './theme/FavoriteDetail.vue'
import { frontendRoutes } from './constants/routes'

Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  linkActiveClass: 'is-active',
  scrollBehavior: (to, from, savedPosition) => ({ y: 0 }),
  routes: [
    { path: frontendRoutes.VIEW_CATEGORIES, name: 'categories', component: Category },
    { path: frontendRoutes.LANDING, name: 'landing', component: Landing },
    { path: frontendRoutes.VIEW_CATEGORY_FAVORITES, name: 'category-favorites', component: CategoryFavorites },
    { path: frontendRoutes.CREATE_FAVORITE, name: 'favorite', component: CreateFavorite },
    { path: frontendRoutes.EDIT_FAVORITE, name: 'favorite-edit', component: EditFavorite },
    { path: frontendRoutes.VIEW_FAVORITE, name: 'favorite-detail', component: FavoriteDetail },
    { path: '*', component: NotFound }
  ]
})

export default router
