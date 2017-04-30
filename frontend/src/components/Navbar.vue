<template>
  <header>
    PistachoFlights
    <span class="right">
      <span>Current data: {{count}}</span>
      <button @click="openPopup()">Upload flight data</button>
    </span>
    <div class="overlay" v-if="opened">
      <form class="data-form" @submit="handleSubmit">
        <div class="headers">
          CSV data should follow the order:
          <div>
            {{["lat", "lon", "weight", "link", "date", "altitude",
            "name"].join(', ')}}
          </div>
        </div>
        <div class="textarea">
          <textarea ref="data"></textarea>
        </div>
        <div class="buttons">
          <button type="submit">Send</button>
          <button @click="hidePopup">Cancel</button>
        </div>
      </form>
    </div>
  </header>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'navbar',
  data() {
    return {
      opened: false
    }
  },
  computed: mapGetters({
    count: 'getFlightCount'
  }),
  methods: Object.assign({}, mapActions([
    'getFlightCount',
    'submitFlightData'
  ]), {
    openPopup() {
      this.opened = true
    },
    hidePopup(event) {
      event && event.preventDefault()

      this.opened = false
    },
    handleSubmit(event) {
      event && event.preventDefault()

      this.submitFlightData(this.$refs.data.value)

      this.hidePopup()
    }
  }),
  created() {
    setInterval(() => {
      this.$store.dispatch('getFlightCount')
    }, 20000)
  }
}
</script>

<style lang="scss" scoped src="../styles/navbar.scss"></style>
