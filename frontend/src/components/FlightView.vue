<template>
  <div class="flight-view">
    <span class="icon">
      <span v-if="selected" class="fa fa-check"></span>
      <span v-else class="fa fa-times"></span>
    </span>
    {{flight.substring(0, 25)}}
  </div>
</template>

<script>
export default {
  name: 'flight-view',
  props: ['flight', 'selected']
}
</script>

<style scoped>
  .icon {
    float: left;
    width: 10px;
  }
</style>
