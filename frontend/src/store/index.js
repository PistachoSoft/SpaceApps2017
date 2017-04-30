import Vue from 'vue'
import Vuex from 'vuex'
import flights from './modules/flights'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    flights
  }
})
