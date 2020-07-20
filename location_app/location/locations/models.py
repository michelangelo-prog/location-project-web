import uuid as uuid_lib
from .behaviors import Nameable
from django.contrib.gis.db import models

from .exceptions import LocationExists

from .managers import LocationManager


class Location(Nameable, models.Model):

    objects = LocationManager()

    uuid = models.UUIDField(db_index=True, default=uuid_lib.uuid4, editable=False,)
    location = models.PointField(
        srid=4326, unique=True
    )  # "X and Y coordinates". X is longitude, Y is latitude
    elevation = models.FloatField()

    def save(self, *args, **kwargs):
        if Location.objects.check_if_exists(location=self.location):
            raise LocationExists()

        super().save(*args, **kwargs)
