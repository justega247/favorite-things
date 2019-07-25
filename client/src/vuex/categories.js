import appService from '../app.service.js'

const state = {
  categories: [],
  categoryFavorites: [],
  category: {}
}

const getters = {
  categories: state => state.categories,
  categoryFavorites: state => state.categoryFavorites
}

const actions = {
  addCategory ({ commit }, categoryData) {
    return appService.addCategory(categoryData).then(data => {
      commit('addCategory', { category: data })
    })
  },
  getCategories ({ commit }) {
    return appService.getCategories().then(categories => {
      commit('getCategories', categories)
    })
  },
  getCategoryFavorites ({ commit }, categoryId) {
    return appService.getCategoryFavorites(categoryId).then(data => {
      commit('getCategoryFavorites', { categoryFavorites: data })
    })
  },
  getCategory ({ commit }, categoryId) {
    return appService.getCategory(categoryId).then(category => {
      commit('getCategory', category)
    })
  },
  deleteFavorite ({ commit }, favoriteId) {
    return appService.deleteFavorite(favoriteId).then(() => {})
  }
}

const mutations = {
  addCategory (state, category) {
    state.categories = [
      ...state.categories, category.category
    ]
  },
  getCategories (state, categories) {
    state.categories = categories
  },
  getCategoryFavorites (state, categories) {
    state.categoryFavorites = categories.categoryFavorites
  },
  getCategory (state, category) {
    state.category = category
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
