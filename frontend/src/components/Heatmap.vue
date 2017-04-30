<template>
  <div class="leaflet-map" ref="map"></div>
</template>

<script>
import MapService from '../services/map-service'

export default {
  name: 'heatmap',
  data() {
    return {
      map: null
    }
  },
  props: ['points'],
  mounted() {
    this.map = new MapService(this.$refs.map)
  },
  watch: {
    points(values) {
      this.map && this.map.setHeatPoints(values.map(({geometry: {coordinates: [lat, lng]}}) => [
        lat, lng, 0.2
      ]))
    }
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
