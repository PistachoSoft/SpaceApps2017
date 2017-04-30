import * as _ from 'lodash';
import L from 'leaflet'
import 'leaflet.heat'

export default class {
  constructor(element) {
    this._map = L.map(element, {
      center: [41.659631, -0.907582],
      zoom: 4,
      maxZoom: 13
    })

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(this._map)

    this._map.attributionControl.setPrefix('')

    const points = _.flatten([
      _.range(1, 100).map((__, index) => [
        50.650 - (0.001 * index),
        30.450,
        0.2
      ]),
      _.range(1, 100).map((__, index) => [
        50.6,
        30.500 - (0.001 * index),
        0.2
      ])
    ])

    L.heatLayer(points, {
      maxZoom: 12,
      radius: 5,
      blur: 5,
      // gradient: {'0.4': 'blue', '0.65': 'lime', '1': 'red'}
    }).addTo(this._map)
  }


}
