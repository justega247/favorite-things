import Vue from 'vue'
import Paginate from 'vuejs-paginate'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faPlusSquare, faMinusSquare } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import 'bulma/css/bulma.css'
import 'normalize.css/normalize.css'
import './styles/styles.scss'
import router from './router'
import store from './vuex/index.js'
import AppLayout from './theme/Layout.vue'

library.add(faPlusSquare, faMinusSquare)

Vue.component('paginate', Paginate)
Vue.component('font-awesome-icon', FontAwesomeIcon)

const app = new Vue({
  router,
  ...AppLayout,
  store
})

export {
  app,
  router,
  store
}
