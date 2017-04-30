import * as _ from 'lodash'
import { getFlights, showHeader, getFlightPoints, getPositionGeoJson } from '../../services/data-service'
import { RECEIVE_FLIGHTS, RECEIVE_FLIGHT_COUNT, RECEIVE_FLIGHT_POINTS, SELECT_FLIGHT } from '../mutation-types'

const state = {
  count: "None",
  selected: {},
  airborne: [],
  points: null
}

const getters = {
  getFlights(state) {
    return state.airborne
  },

  getFlightCount(state) {
    return state.count
  },

  getSelectedFlights(state) {
    return state.selected
  },

  getFlightPoints(state) {
    return state.points
  }
}

const actions = {
  getFlights({commit}, range) {
    getFlights(range).then((airborne) => {
      commit(RECEIVE_FLIGHTS, {airborne})
    })
  },

  getFlightCount({commit}) {
    showHeader().then((count) => {
      commit(RECEIVE_FLIGHT_COUNT, {count})
    })
  },

  selectFlight({commit}, index) {
    commit(SELECT_FLIGHT, {index})

    getFlightPoints(Object.keys(state.selected).map((index) => state.airborne[index]))
    .then((points) => Promise.all(points.map(({$uri}) => getPositionGeoJson($uri))))
    .then((points) => {
      commit(RECEIVE_FLIGHT_POINTS, {points})
    })
  }
}

const mutations = {
  [RECEIVE_FLIGHTS](state, {airborne}) {
    state.airborne = airborne
    state.selected = {}
    state.points = null
  },

  [SELECT_FLIGHT](state, {index}) {
    if (state.selected[index]) {
      delete state.selected[index]
    } else {
      state.selected[index] = true
    }

    state.selected = _.clone(state.selected)
  },

  [RECEIVE_FLIGHT_POINTS](state, {points}) {
    state.points = points
  },

  [RECEIVE_FLIGHT_COUNT](state, {count}) {
    state.count = count
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
