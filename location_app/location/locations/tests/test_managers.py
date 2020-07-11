from django.test import TestCase

from ..models import Location

from ..factories import LocationFactory

class TestLocationManager(TestCase):
    def setUp(self):
        self.place = LocationFactory()

    def test_check_if_exists_return__false__when_location_does_not_exist(self):
        place_data = LocationFactory.build()
        check = Location.objects.check_if_exists(location=place_data.location)
        self.assertFalse(check)

    def test_check_if_exists_return__true__when_location_exists(self):
        check = Location.objects.check_if_exists(location=self.place.location)
        self.assertTrue(check)

