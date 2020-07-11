from django.test import TestCase

from ..exceptions import LocationExists

from django.contrib.gis.geos import Point

from ..factories import LocationFactory

class TestLocationModel(TestCase):
    def setUp(self):
        self.point = Point(21.003778, 52.212667)
        self.elevation = 10.0
        self.point_name = "Warsaw"

        self.location = LocationFactory(
            name=self.point_name, location=self.point, elevation=self.elevation
        )

    def test_create_location_object(self):
        self.assertEquals(self.point_name, self.location.name)
        self.assertEquals(self.point, self.location.location)
        self.assertEquals(self.elevation, self.location.elevation)

    def test_raise_exception_when_try_create_object_with_existed_cooridinates_in_db(
        self,
    ):
        with self.assertRaises(LocationExists):
            LocationFactory(location=self.point)

    def test_not_raise_exception_when_create_object_with_not_existed_coordinates_in_db(
        self,
    ):
        point_2 = Point(10.783329, 59.916950)
        elevation_2 = 100.0
        point_name_2 = "Oslo"

        location_2 = LocationFactory(name=point_name_2, location=point_2, elevation=elevation_2)

        self.assertEquals(point_name_2, location_2.name)
        self.assertEquals(point_2, location_2.location)
        self.assertEquals(elevation_2, location_2.elevation)
