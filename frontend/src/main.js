import Vue from 'vue'
import store from './store'
import router from './config/routes'
import './styles/style.scss'

new Vue({
  el: '#app',
  store,
  router
})
