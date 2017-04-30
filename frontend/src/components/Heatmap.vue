<template>
  <div class="leaflet-map" ref="map"></div>
</template>

<script>
import MapService from '../services/map-service'

export default {
  name: 'heatmap',
  mounted: function() {
    new MapService(this.$refs.map)
  }
}
</script>

<style lang="scss">
  @import "../../node_modules/leaflet/dist/leaflet.css";
  @import "../styles/_mixins.scss";

  .leaflet-map {
    @include full-viewport;
  }
</style>
