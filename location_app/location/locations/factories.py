import random

from django.contrib.gis.geos import Point
from factory import Sequence
from factory.django import DjangoModelFactory
from factory.fuzzy import BaseFuzzyAttribute, FuzzyFloat

from .models import Location


class FuzzyPoint(BaseFuzzyAttribute):
    def fuzz(self):
        return Point(random.uniform(-180.0, 180.0), random.uniform(-90.0, 90.0))


class LocationFactory(DjangoModelFactory):
    class Meta:
        model = Location

    name = Sequence(lambda n: f"name{n}")
    location = FuzzyPoint()
    elevation = FuzzyFloat(0, 100)
