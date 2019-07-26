import appService from '../app.service.js'

const state = {
  favorite: {}
}

const actions = {
  addFavorite ({ commit }, favoriteData) {
    return appService.addFavorite(favoriteData).then(() => {})
  }
}

export default {
  namespaced: true,
  state,
  actions
}
