import * as _ from 'lodash'
import {Httpr} from 'httpr'
import {XHRProvider} from 'httpr-provider-xhr'

const http = new Httpr({
  provider: new XHRProvider()
})

export function getAirborne() {
  return Promise.resolve(_.range(1, 100).map((value) => `Flight ${value}`))
}

export function showHeader() {
  http.get('http://localhost:8000/position')
  .then((response) => {
    console.log(response.headers)
  });
}
