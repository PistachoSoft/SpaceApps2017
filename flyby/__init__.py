"""
Get flight data from multiple sources, normalize it and
expose a JSON API to comprehensively search and filter over it.
"""
import io
import os
import csv
import json
import configparser
import logging
import peewee
from flask_potion import Api, ModelResource, fields
from flask_potion.routes import ItemRoute, Route
from flask_potion.contrib.peewee import PeeweeManager
from flask import Flask

logging.basicConfig()

DB = peewee.SqliteDatabase('/tmp/db')

CONFIG = configparser.ConfigParser()
CONFIG.add_section("main")
CONFIG.read(os.path.expanduser('~/.flyby.conf'))
LOG = logging.getLogger(__name__)
LOG.setLevel(CONFIG['main'].get('loglevel', logging.DEBUG))


class Search(peewee.Model):
    """ Position """
    # pylint: disable=too-few-public-methods
    search = peewee.TextField()
    comment = peewee.TextField()

    class Meta:
        # pylint: disable=missing-docstring, too-few-public-methods
        database = DB


class Position(peewee.Model):
    """ Position """
    # pylint: disable=too-few-public-methods
    latlon = peewee.TextField()
    flight_name = peewee.TextField()
    source = peewee.TextField()
    weight = peewee.IntegerField(default=1)
    link = peewee.TextField()
    date = peewee.TextField()
    type = peewee.TextField()
    altitude = peewee.TextField()
    raw = peewee.TextField()

    class Meta:
        # pylint: disable=missing-docstring, too-few-public-methods
        database = DB

    @staticmethod
    def from_csv(data):
        """ Import Data from CSV """
        dataio = io.StringIO()
        dataio.write(data)
        dataio.seek(0)
        reader = csv.DictReader(
            dataio, ["lat", "lon", "weight", "link", "date", "altitude",
                     "name"])
        for row in reader:
            result = {
                'latlon': json.dumps([row['lat'], row['lon']]),
                'flight_name': row['name'],
                'source': "user",
                'raw': json.dumps(row),
                'weight': row['weight'],
                'link': row['link'],
                'date': row['date'],
                'type': 'flight',
                'altitude': row['altitude']
            }
            Position.create(**result)

    def to_geojson(self):
        """ Convert to geojson format """
        return {
            "type": "Feature",
            "geometry": {
                "type": "MultiPoint",
                "coordinates": json.loads(self.latlon),
                },
            "properties": {
                # 'raw': self.raw,
                'date': self.date,
                'flight_name': self.flight_name,
                'altitude': self.altitude,
                'type': self.type,
                'source': self.source
            }}


class PositionResource(ModelResource):
    """ Position APIResource """
    # pylint: disable=too-few-public-methods
    @ItemRoute.GET('/to_geojson')
    def to_geojson(self, flight):
        """ To geo json """
        # pylint: disable=no-self-use
        return flight.to_geojson()

    @Route.POST('/csv')
    def from_csv(self, data: fields.String()):
        return Position.from_csv(data)

    class Meta:
        # pylint: disable=missing-docstring
        model = Position


class SearchResource(ModelResource):
    """ Position APIResource """
    # pylint: disable=too-few-public-methods
    class Meta:
        # pylint: disable=missing-docstring
        model = Search


def run():
    """ Main entry point """
    app = Flask(__name__, static_path='')
    app.config['DATABASE'] = 'sqlite://'
    # pylint: disable=no-member
    if not Position.table_exists():
        Position.create_table()

    if not Search.table_exists():
        Search.create_table()

    api = Api(app, default_manager=PeeweeManager)
    api.add_resource(PositionResource)
    api.add_resource(SearchResource)
    app.run(debug=True, host="0.0.0.0", port=8000)
