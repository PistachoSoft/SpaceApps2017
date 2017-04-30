import * as _ from 'lodash'
import {Httpr} from 'httpr'
import {XHRProvider} from 'httpr-provider-xhr'

const http = new Httpr({
  provider: new XHRProvider()
})

export function getFlights(range) {
  return http.get('http://localhost:8000/position/flights', {
    date: JSON.stringify({
      $between: [range.startDate.valueOf(), range.endDate.valueOf()]
    })
  })
  .then((response) => {
    if (response.status >= 400 || !response.data.length) {
      return _.range(1, 100).map((value) => `Flight ${value}`)
    } else {
      return response.data
    }
  })
}

export function getFlightPoints(flightIds) {
  return http.get('http://localhost:8000/position', {
    flight_name: JSON.stringify({
      $in: flightIds
    })
  })
  .then((response) => response.data)
}

export function getPositionGeoJson(uri) {
  return http.get(`http://localhost:8000${uri}/to_geojson`)
  .then((response) => response.data)
}

export function showHeader() {
  return http.get('http://localhost:8000/position/count')
  .then((response) => {
    return response.data
  })
}

export function retrieveCountRec() {
}
