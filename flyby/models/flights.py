import peewee
import json

DATABASE = peewee.SqliteDatabase("/tmp/db")


class Flight(peewee.Model):
    coordinates = peewee.TextField(null=True, unique=False)

    def to_geojson(self):
        return {
            "type": "Feature",
            "geometry": {
                "type": "MultiPoint",
                "coordinates": json.loads(self.coordinates)
            }}


DATABASE.create_tables([Flight])
