import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../containers/Home.vue'

Vue.use(VueRouter)

export default new VueRouter({
  routes: [
    {
      path: '/',
      component: Home
    }
  ]
})
