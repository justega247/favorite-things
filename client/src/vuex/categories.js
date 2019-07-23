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
      console.log('#####$$$', data)
    })
  }
}

const mutations = {
  addCategory (state, category) {
    state.categories = [
      ...state.categories, category.category
    ]
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
