<template>
  <header>
    PistachoFlights
    <span class="right">Current data: {{count}}</span>
  </header>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'navbar',
  computed: mapGetters({
    count: 'getFlightCount'
  }),
  methods: mapActions([
    'getFlightCount'
  ]),
  created() {
    setInterval(() => {
      this.$store.dispatch('getFlightCount')
    }, 1000)
  }
}
</script>

<style scoped>
  .right {
    float: right;
  }

  header {
    border: 1px solid black;
  }
</style>
