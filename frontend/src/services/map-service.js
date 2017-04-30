import L from 'leaflet'
import 'leaflet.heat'

export default class {
  constructor(element) {
    this._map = L.map(element, {
      center: [41.659631, -0.907582],
      zoom: 10,
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
