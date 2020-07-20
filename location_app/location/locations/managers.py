from django.db import models

from .adapters import AdapterElevationAPI

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D


class LocationManager(models.Manager):
    def check_if_exists(self, **kwargs):
        return self.filter(**kwargs).exists()

    def create(self, **kwargs):
        if "elevation" not in kwargs:
            location = kwargs.get("location")
            elevation_api_adapter = AdapterElevationAPI()
            kwargs["elevation"] = elevation_api_adapter.get_elevation(
                location.x, location.y
            )
        return super().create(**kwargs)

    def find_closest_queryset(self, longitude, latitude, distance=None):
        user_location = Point(longitude, latitude, srid=4326)
        if distance:
            return (
                self.filter(location__distance_lte=(user_location, D(m=distance)))
                .annotate(distance=Distance("location", user_location))
                .order_by("distance")
            )
        else:
            return self.annotate(distance=Distance("location", user_location)).order_by(
                "distance"
            )[:1]
