import { getAirborne } from '../../services/data-service'
import { RECEIVE_FLIGHTS, SELECT_FLIGHT } from '../mutation-types'

const state = {
  selected: null,
  airborne: []
}

const getters = {
  getFlights(state) {
    return state.airborne
  },

  getSelectedFlight(state) {
    return state.selected
  }
}

const actions = {
  getFlights({commit}, range) {
    console.log(range)

    getAirborne().then((airborne) => {
      commit(RECEIVE_FLIGHTS, {airborne})
    })
  },

  selectFlight({commit}, flight) {
    commit(SELECT_FLIGHT, {flight})
  }
}

const mutations = {
  [RECEIVE_FLIGHTS](state, {airborne}) {
    state.airborne = airborne;
  },

  [SELECT_FLIGHT](state, {flight}) {
    state.selected = flight;
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
