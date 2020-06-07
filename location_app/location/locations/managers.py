from django.db import models

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from .helpers import get_elevation_from_api

class LocationManager(models.Manager):

    def create_get_elevation_from_from_api(self, name, location):
        elevation = get_elevation_from_api(location)
        self.create(name=name,location=location,elevation=elevation)

    def find_nearest_location(self, longitude, latitude):
        user_location = Point(longitude, latitude, srid=4326)
        return self.annotate(distance=Distance('location', user_location)).order_by('distance').first()

    def find_nearest_locations_by_distance(self, longitude, latitude, distance):
        user_location = Point(longitude, latitude, srid=4326)
        return self.filter(location__distance_lte=(user_location, D(m=distance))).annotate(distance=Distance("location",user_location)).order_by("distance")
