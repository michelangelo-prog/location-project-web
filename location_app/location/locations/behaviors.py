from django.db import models


class Nameable(models.Model):
    name = models.TextField(max_length=1000)

    class Meta:
        abstract = True
