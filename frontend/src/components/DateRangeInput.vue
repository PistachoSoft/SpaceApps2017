<template>
  <div class="date-range-input">
    <div>

    </div>
    <div class="overlay" v-if="openedPopup">
      <date-range lang="en" :range="range" @change="handleChange" :first-day-of-week="1"></date-range>
    </div>
  </div>
</template>

<script>
export default {
  name: 'date-range-input',
  methods: {
    handleChange(range) {
      console.log(range)
    }
  }
}
</script>

<style lang="scss">
  .date-range-input {

    .overlay {

    }
  }
</style>
