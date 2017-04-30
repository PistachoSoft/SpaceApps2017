import * as _ from 'lodash'
import {Httpr} from 'httpr'

export function getAirborne() {
  return Promise.resolve(_.range(1, 100).map((value) => `Flight ${value}`))
}
