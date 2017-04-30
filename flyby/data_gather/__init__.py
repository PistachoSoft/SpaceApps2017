# pylint: disable=missing-docstring
from functools import lru_cache
import json
import sys
import csv
import datetime
import arrow
import requests
from flyby import CONFIG, LOG
from . import nasa_flights, opensky


API_URL = 'http://{}:{}'.format(CONFIG['main'].get("host", "127.0.0.1"),
                                CONFIG['main'].get("port", "5000"))


def nasa_to_flyby():
    link = None
    if len(sys.argv) > 1:
        # Manual link input.
        # We used this to priorize
        link = sys.argv[1]
    for iwgs in nasa_flights.IWG(link):
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
        LOG.debug("Getting opensky data for %s", date)
        osky = opensky.OpenSkyApi("dfrancosspaceapps", "spaceapps123").get_states(
            datetime.datetime.fromtimestamp(date))
        if not osky:
            LOG.debug("No data found")
            return

        for element in osky.states:
            dates = {
                "flight_name": element.callsign,
                "raw": json.dumps(element.__dict__),
                "type": "plane",
                "source": "opensky",
                "date": str(date),
                "altitude": element.altitude,
                "latlon": json.dumps([element.latitude, element.longitude])}

            requests.post("{}/position".format(API_URL), json=dates)
    req = requests.get("{}/position".format(API_URL))
    for elem in req.json():
        _submit_date(elem["date"])


def openflights_to_flyby():
    """
    Get openflights data from files in sys.argv[1] and 2
    (airports and routes) and add it to flyby
    """
    airheads = ["ID", "name", "city", "country", "iata", "icao", "lat", "lon",
                "alt", "tz", "dst", "type", "source"]
    routeheads = ["A", "AID", "so", "source", "de", "dest", "c", "s", "e"]
    airports = csv.DictReader(open(sys.argv[1]), airheads)
    routes = csv.DictReader(open(sys.argv[2]), routeheads)

    results = []
    for route in routes:
        if route['dest'] in airports and route['source'] in airports:
            results.append([airports[route['source']],
                            airports[route['dest']]])

    for number, result_ in enumerate(results):
        for result in result_:
            dates = {"flight_name": "route{}".format(number),
                     "raw": "",
                     "type": "route",
                     "source": "openflights",
                     "date": str(0),
                     "altitude": str(0),
                     "latlon": json.dumps(result)}
            requests.post('http://localhost:5000/positions', json=dates)
