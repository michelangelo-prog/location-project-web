from django.db import models

from .adapters import AdapterElevationAPI

class LocationManager(models.Manager):
    def check_if_exists(self, **kwargs):
        return self.filter(**kwargs).exists()

    def create(self, **kwargs):
        if not "elevation" in kwargs:
            location = kwargs.get("location")
            elevation_api_adapter = AdapterElevationAPI()
            kwargs["elevation"] = elevation_api_adapter.get_elevation(
                location.x, location.y
            )
        return super().create(**kwargs)