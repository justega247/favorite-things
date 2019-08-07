import Vue from 'vue'
import Router from 'vue-router'
import Landing from './views/Landing.vue'
import Category from './views/Category.vue'
import CategoryFavorites from './views/CategoryFavorites.vue'
import NotFound from './views/NotFound.vue'
import CreateFavorite from './views/CreateFavorite.vue'
import EditFavorite from './views/EditFavorite.vue'
import FavoriteDetail from './views/FavoriteDetail.vue'
import { frontendRoutes } from './constants/routes'

Vue.use(Router)

export default new Router({
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
