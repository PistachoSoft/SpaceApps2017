# pylint: disable=missing-docstring
from functools import lru_cache
import json
import arrow
import requests
from flyby import CONFIG, LOG
from . import nasa_flights, opensky


API_URL = 'http://{}:{}'.format(CONFIG['main'].get("host", "127.0.0.1"),
                                CONFIG['main'].get("port", "5000"))


def nasa_to_flyby():
    for iwgs in nasa_flights.IWG():
        name = iwgs.name
        for iwg in iwgs:
            if not iwg['Latitude']:
                LOG.debug("Got empty iwg")
                continue

            dates = {
                "flight_name": name,
                "raw": json.dumps(iwg),
                "type": "plane",
                "source": "nasa",
                "date": str(arrow.get(iwg["System_Timestamp"]).timestamp),
                "altitude": iwg['GPS_Altitude'],
                "latlon": json.dumps([iwg['Latitude'], iwg['Longitude']])}
            LOG.debug("Requesting %s", dates)
            result = requests.post("{}/position".format(API_URL), json=dates)
            LOG.debug(result.status_code)
            LOG.debug(result.text)


def opensky_to_flyby():
    @lru_cache()
    def _submit_date(date):
        for element in opensky.OpenSkyApi().get_states(date).states:
            dates = {
                "flight_name": element.callsign,
                "raw": element.__dict__,
                "type": "plane",
                "source": "opensky",
                "date": date,
                "altitude": element.altitude,
                "latlon": [element.latitude, element.longitude]}

            requests.post("{}/position".format(API_URL), json=dates)

    for elem in requests.get("{}/position?where=="
                             "{{\"type\": \"nasa\"}}".format(API_URL)).json():
        _submit_date(elem["date"])
