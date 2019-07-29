import appService from '../app.service.js'

const state = {
  favorite: {},
  historyLog: []
}

const getters = {
  favorite: state => state.favorite,
  historyLog: state => state.historyLog
}

const actions = {
  addFavorite ({ commit }, favoriteData) {
    return appService.addFavorite(favoriteData).then(() => {})
  },
  getFavorite ({ commit }, favoriteId) {
    return appService.getFavorite(favoriteId).then(favorite => {
      commit('getFavorite', favorite)
    })
  },
  getFavoriteAudit ({ commit }, favoriteId) {
    return appService.getFavoriteAudit(favoriteId).then(auditLog => {
      commit('getFavoriteAudit', auditLog)
    })
  }
}

const mutations = {
  getFavorite (state, favorite) {
    state.favorite = favorite
  },
  getFavoriteAudit (state, auditLog) {
    state.historyLog = auditLog
  }
}

export default {
  namespaced: true,
  state,
  actions,
  mutations,
  getters
}
