import L from 'leaflet'
import 'leaflet.heat'

export default class {
  constructor(element) {
    this._map = L.map(element, {
      center: [34.0201812, -118.69192],
      zoom: 4,
      maxZoom: 13
    })

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(this._map)

    this._map.attributionControl.setPrefix('')
  }

  setHeatPoints(points) {
    this._heat && this._map.removeLayer(this._heat)

    this._heat = L.heatLayer(points, {
      maxZoom: 12,
      radius: 5,
      blur: 5,
      // gradient: {'0.4': 'blue', '0.65': 'lime', '1': 'red'}
    })

    this._heat.addTo(this._map)
  }
}
