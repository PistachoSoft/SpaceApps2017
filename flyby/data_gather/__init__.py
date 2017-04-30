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
                                CONFIG['main'].get("port", "8000"))


def adjust(position):
    """ Round to 8 numbers """
    return round(float(position), 8)


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
                "type": "plane",
                "source": "nasa",
                "date": {
                    "$date": arrow.get(
                        iwg["System_Timestamp"]).timestamp * 1000},
                "link": "",
                "altitude": iwg['GPS_Altitude'],
                "latlon": json.dumps([adjust(iwg['Latitude']),
                                      adjust(iwg['Longitude'])])}
            LOG.debug("Requesting %s", dates)
            result = requests.post("{}/position".format(API_URL), json=dates)
            LOG.debug(result.status_code)
            LOG.debug(result.text)


def opensky_to_flyby():
    @lru_cache()
    def _submit_date(date):
        LOG.debug("Getting opensky data for %s", date)
        osky = opensky.OpenSkyApi(
            "dfrancosspaceapps", "spaceapps123").get_states(
                    datetime.datetime.fromtimestamp(date))
        if not osky:
            LOG.debug("No data found")
            return

        for element in osky.states:
            dates = {
                "flight_name": element.callsign,
                "type": "plane",
                "source": "opensky",
                "link": "",
                "date": {"$date": date * 1000},
                "altitude": element.altitude,
                "latlon": json.dumps([adjust(element.latitude),
                                      adjust(element.longitude)])}

            requests.post("{}/position".format(API_URL), json=dates)
    if len(sys.argv) > 1:
        _submit_date(int(sys.argv[1]))
    else:
        req = requests.get("{}/position".format(API_URL))
        for elem in req.json():
            try:
                _submit_date(int(elem["date"]["$date"]) / 1000)
            except Exception as err:
                LOG.exception(err)


def openflights_to_flyby():
    """
    Get openflights data from files in sys.argv[1] and 2
    (airports and routes) and add it to flyby
    """
    airheads = ["ID", "name", "city", "country", "iata", "icao", "lat", "lon",
                "alt", "tz", "dst", "type", "source"]
    routeheads = ["A", "AID", "so", "source", "de", "dest", "c", "s", "e"]
    airports = {a["ID"]: a for a in csv.DictReader(
        open(sys.argv[1]), airheads)}
    routes = list(csv.DictReader(open(sys.argv[2]), routeheads))

    results = []
    for route in routes:
        try:
            results.append([airports[route['source']],
                            airports[route['dest']]])
        except:
            pass

    for number, result_ in enumerate(results):
        for result in result_:
            dates = {"flight_name": "route{}".format(number),
                     "type": "route",
                     "source": "openflights",
                     "date": {"$date": 0},
                     "altitude": str(0),
                     "link": "",
                     "latlon": json.dumps(adjust(result[0]),
                                          adjust(result[1]))}
            res = requests.post('http://localhost:8000/position', json=dates)
            LOG.debug(res.status_code)
            LOG.debug(res.text)
