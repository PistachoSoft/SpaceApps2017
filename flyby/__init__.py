"""
Get flight data from multiple sources, normalize it and
expose a JSON API to comprehensively search and filter over it.
"""
import os
import json
import configparser
import logging
import peewee
from flask_potion import Api, ModelResource
from flask_potion.routes import ItemRoute
from flask_potion.contrib.peewee import PeeweeManager
from flask import Flask

logging.basicConfig()

DB = peewee.SqliteDatabase('/tmp/db')

CONFIG = configparser.ConfigParser()
CONFIG.add_section("main")
CONFIG.read(os.path.expanduser('~/.flyby.conf'))
LOG = logging.getLogger(__name__)
LOG.setLevel(CONFIG['main'].get('loglevel', logging.DEBUG))


class Position(peewee.Model):
    """ Position """
    # pylint: disable=too-few-public-methods
    latlon = peewee.TextField()
    flight_name = peewee.TextField()
    source = peewee.TextField()
    date = peewee.TextField()
    type = peewee.TextField()
    altitude = peewee.TextField()
    raw = peewee.TextField()

    class Meta:
        # pylint: disable=missing-docstring, too-few-public-methods
        database = DB

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

    class Meta:
        # pylint: disable=missing-docstring
        model = Position


def run():
    """ Main entry point """
    app = Flask(__name__)
    app.config['DATABASE'] = 'sqlite://'
    # pylint: disable=no-member
    if not Position.table_exists():
        Position.create_table()
    api = Api(app, default_manager=PeeweeManager)
    api.add_resource(PositionResource)
    app.run(debug=True)
