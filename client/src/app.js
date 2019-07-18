import Vue from 'vue'

const app = new Vue({
  data: {
    hello: 'hi hello vue'
  },
  template: '<div id="app">{{ hello }}</div>'
})

export {
  app
}
