from flask_potion import Api, ModelResource
from flask_potion.routes import ItemRoute
from flask_potion.contrib.peewee import PeeweeManager
from flask import Flask
from flyby.models.flights import Flight


class FlightResource(ModelResource):
    @ItemRoute.GET('/to_geojson')
    def to_geojson(self, flight):
        return flight.to_geojson()

    class Meta:
        model = Flight


def run():
    app = Flask(__name__)
    api = Api(app, default_manager=PeeweeManager)
    api.add_resource(FlightResource)
    app.run()
