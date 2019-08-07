import Vue from 'vue'
import 'bulma/css/bulma.css'
import 'normalize.css/normalize.css'
import './styles/styles.scss'
import Vue2Filters from 'vue2-filters'
import Paginate from 'vuejs-paginate'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faPlusSquare, faMinusSquare, faTrashAlt, faEdit, faFileAlt } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import App from './App.vue'
import router from './router'
import store from './vuex/index.js'

Vue.config.productionTip = false
Vue.use(Vue2Filters)

library.add(faPlusSquare, faMinusSquare, faTrashAlt, faEdit, faFileAlt)

Vue.component('paginate', Paginate)
Vue.component('font-awesome-icon', FontAwesomeIcon)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
