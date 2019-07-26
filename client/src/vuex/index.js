import Vue from 'vue'
import Vuex from 'vuex'
import categoryModule from './categories'
import favoriteModule from './favorite'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    categoryModule,
    favoriteModule
  }
})

export default store
