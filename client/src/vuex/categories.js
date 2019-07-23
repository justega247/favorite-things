import appService from '../app.service.js'

const state = {
  categories: []
}

const getters = {
  categories: state => state.categories
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
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
