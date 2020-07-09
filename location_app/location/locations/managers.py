from django.db import models


class LocationManager(models.Manager):
    def check_if_exists(self, **kwargs):
        return self.filter(**kwargs).exists()
