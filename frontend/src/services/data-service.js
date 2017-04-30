import * as _ from 'lodash'
import {Httpr} from 'httpr'
import {XHRProvider} from 'httpr-provider-xhr'

const http = new Httpr({
  provider: new XHRProvider()
})

const host = 'http://localhost:8000'

export function getFlights(range) {
  return http.get(`${host}/position/flights`, {
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
  if (!flightIds.length) {
    return Promise.resolve([])
  } else {
    return http.get(`${host}/position`, {
      flight_name: JSON.stringify({
        $in: flightIds
      })
    })
    .then((response) => response.data)
  }
}

export function getPositionGeoJson(uri) {
  return http.get(`${host}${uri}/to_geojson`)
  .then((response) => response.data)
}

export function getPositions(points) {
  return http.post(`${host}/position/geojson`, {}, points)
  .then((response) => response.data)
}

export function getDocCount() {
  return http.get(`${host}/position/count`)
  .then((response) => response.data)
}

export function submitFlightData(data) {
  return http.post(`${host}/position/csv`, {}, {
    data
  })
  .then((response) => response.data)
}
