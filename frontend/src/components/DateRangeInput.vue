<template>
  <div class="date-range-input">
    <div class="input" @click="showPopup()">
      {{range.startDate.format('YYYY-MM-DD')}} to {{range.endDate.format('YYYY-MM-DD')}}
    </div>
    <div class="overlay" v-if="opened">
      <div class="calendar-wrapper">
        <date-range lang="en" :range="range" @change="handleChange" :first-day-of-week="1"></date-range>
      </div>
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
      },
      opened: false
    }
  },
  methods: {
    handleChange(range) {
      this.opened = false;

      this.onChange(range)
    },
    showPopup() {
      this.opened = true;
    }
  },
  components: {
    DateRange
  }
}
</script>

<style lang="scss" src="../styles/date-range-input.scss"></style>
