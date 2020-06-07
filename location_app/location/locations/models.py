from .behaviors import Nameable
from django.contrib.gis.db import models

from .managers import LocationManager

from .exceptions import LocationExist

class Location(Nameable, models.Model):

    objects = LocationManager()

    location = models.PointField(srid=4326) # "X and Y coordinates". X is longitude, Y is latitude
    elevation = models.FloatField()

    def save(self, *args, **kwargs):
        if Location.objects.filter(location=self.location).exists():
            raise LocationExist()

        super().save(*args, **kwargs)
