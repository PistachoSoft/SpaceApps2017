<template>
  <div class="home">
    <div class="sidebar">
      <date-range-input :onChange="getFlights"></date-range-input>
      <div class="flights-list">
        <div v-for="(item, index) in items"
             @click="selectFlight(index)"
             class="flight-item"
             :class="{ active: !!selected[index] }">
          <flight-view :flight="item"></flight-view>
        </div>
      </div>
    </div>
    <div class="main">
      <heatmap :points="points"></heatmap>
      <div class="player"></div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { DateRange } from 'vue-date-range'
import moment from 'moment'
import Heatmap from '../components/Heatmap.vue'
import DateRangeInput from '../components/DateRangeInput.vue'
import FlightView from '../components/FlightView.vue'

export default {
  name: 'home',
  data() {
    return {
      range: {
        startDate: moment(),
        endDate: moment().add(7, 'days')
      }
    }
  },
  components: {
    Heatmap,
    DateRangeInput,
    FlightView
  },
  computed: mapGetters({
    items: 'getFlights',
    selected: 'getSelectedFlights',
    points: 'getFlightPoints'
  }),
  methods: mapActions([
    'selectFlight',
    'getFlights'
  ]),
  created() {
    this.$store.dispatch('getFlights', this.range)
  }
}
</script>

<style lang="scss" src="../styles/home.scss"></style>
