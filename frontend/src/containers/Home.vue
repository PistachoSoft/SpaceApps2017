<template>
  <div class="home">
    <div class="sidebar">
      <div class="date-range-input">
        <date-range lang="en" :range="range" @change="getFlights" :first-day-of-week="1"></date-range>
      </div>
      <div class="flights-list">
        <div v-for="item in items"
             @click="selectFlight(item)">
          {{item}} {{item === selected}}
        </div>
      </div>
    </div>
    <div class="main">
      <heatmap></heatmap>
      <div class="player"></div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { DateRange } from 'vue-date-range'
import moment from 'moment'
import Heatmap from '../components/Heatmap.vue'

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
    DateRange
  },
  computed: mapGetters({
    items: 'getFlights',
    selected: 'getSelectedFlight'
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
