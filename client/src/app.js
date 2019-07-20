import Vue from 'vue'
import router from './router'
import 'bulma/css/bulma.css'
import 'normalize.css/normalize.css'
import './styles/styles.scss'
import AppLayout from './theme/Layout.vue'

const app = new Vue({
  router,
  ...AppLayout
})

export {
  app,
  router
}
