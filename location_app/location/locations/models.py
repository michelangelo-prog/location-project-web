from .behaviors import Nameable
from django.contrib.gis.db import models

from .exceptions import LocationExists

from .managers import LocationManager


class Location(Nameable, models.Model):

    objects = LocationManager()

    location = models.PointField(
        srid=4326
    )  # "X and Y coordinates". X is longitude, Y is latitude
    elevation = models.FloatField()

    def save(self, *args, **kwargs):
        if Location.objects.check_if_exists(location=self.location):
            raise LocationExists()

        super().save(*args, **kwargs)
