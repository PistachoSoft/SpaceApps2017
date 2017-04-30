<template>
  <div class="flight-view">
    {{flight.substring(0, 25)}}
  </div>
</template>

<script>
export default {
  name: 'flight-view',
  props: ['flight']
}
</script>
