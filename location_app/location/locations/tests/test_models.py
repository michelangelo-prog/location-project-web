from collections import namedtuple

from django.test import TestCase

from ..models import Location

from ..exceptions import LocationExists

from django.contrib.gis.geos import Point


class TestLocationModel(TestCase):
    def setUp(self):
        self.point = Point(21.003778, 52.212667)
        self.elevation = 10.0
        self.point_name = "Warsaw"

        self.location = self._create_location_object(
            self.point_name, self.point, self.elevation
        )

    def _create_location_object(self, name, location, elevation):
        return Location.objects.create(
            name=name, location=location, elevation=elevation
        )

    def test_create_location_object(self):
        self.assertEquals(self.point_name, self.location.name)
        self.assertEquals(self.point, self.location.location)
        self.assertEquals(self.elevation, self.location.elevation)

    def test_raise_exception_when_try_create_object_with_existed_cooridinates_in_db(
        self,
    ):
        with self.assertRaises(LocationExists):
            self._create_location_object(self.point_name, self.point, self.elevation)

    def test_not_raise_exception_when_create_object_with_not_existed_coordinates_in_db(
        self,
    ):
        self.point_2 = Point(10.783329, 59.916950)
        self.elevation_2 = 100.0
        self.point_name_2 = "Oslo"

        self.location_2 = self._create_location_object(
            self.point_name_2, self.point_2, self.elevation_2
        )

        self.assertEquals(self.point_name_2, self.location_2.name)
        self.assertEquals(self.point_2, self.location_2.location)
        self.assertEquals(self.elevation_2, self.location_2.elevation)
