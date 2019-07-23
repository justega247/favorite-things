import Vue from 'vue'
import Vuex from 'vuex'
import categoryModule from './categories'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    categoryModule
  }
})

export default store
