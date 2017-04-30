<template>
  <div class="date-range-input">
    <div>

    </div>
    <div class="overlay" v-if="true">
      <date-range lang="en" :range="range" @change="handleChange" :first-day-of-week="1"></date-range>
    </div>
  </div>
</template>

<script>
import { DateRange } from 'vue-date-range'
import moment from 'moment'

export default {
  name: 'date-range-input',
  props: [
    'onChange'
  ],
  data() {
    return {
      range: {
        startDate: moment(),
        endDate: moment().add(7, 'days')
      }
    }
  },
  methods: {
    handleChange(range) {
      console.log(range)

      this.onChange(range)
    }
  },
  components: {
    DateRange
  }
}
</script>

<style lang="scss" src="../styles/date-range-input.scss"></style>
