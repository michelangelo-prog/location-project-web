from django.test import TestCase

from ..models import Location

import factory
from ..factories import LocationFactory

from unittest import mock
from unittest.mock import call

EXPECTED_ELEVATION = 22.22

def mocked_adapter_get_elevation(*args, **kwargs):
    return EXPECTED_ELEVATION

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

    @mock.patch(
        "location.locations.managers.AdapterElevationAPI.get_elevation",
        side_effect=mocked_adapter_get_elevation,
    )
    def test_create_location_when_elevation_not_provided_in_create(self, mock_get_elevation):
        data = factory.build(dict, FACTORY_CLASS=LocationFactory)
        data.pop("elevation")

        place = Location.objects.create(**data)

        self.assertEqual(data["name"], place.name)
        self.assertEqual(data["location"], place.location)
        self.assertEqual(EXPECTED_ELEVATION, place.elevation)
        self.assertEqual(2, Location.objects.count())

    @mock.patch(
        "location.locations.managers.AdapterElevationAPI.get_elevation",
        side_effect=mocked_adapter_get_elevation,
    )
    def test_call_once__get_elevation__when_create_location_and_elevation_not_provided(self, mock_get_elevation):
        data = factory.build(dict, FACTORY_CLASS=LocationFactory)
        data.pop("elevation")

        Location.objects.create(**data)

        expected_call = call(
            data["location"].x,
            data["location"].y
        )
        mock_get_elevation.assert_called_once()
        self.assertIn(expected_call, mock_get_elevation.call_args_list)

    @mock.patch(
        "location.locations.managers.AdapterElevationAPI.get_elevation",
        side_effect=mocked_adapter_get_elevation,
    )
    def test_does_not_call__get_elevation__when_create_location_and_elevation_provided(self, mock_get_elevation):
        LocationFactory()
        mock_get_elevation.assert_not_called()