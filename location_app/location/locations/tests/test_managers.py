from unittest import mock
from unittest.mock import call

import factory
from django.db.models.query import QuerySet
from django.test import TestCase

from ..factories import LocationFactory
from ..models import Location

EXPECTED_ELEVATION = 22.22

from django.contrib.gis.geos import Point


def mocked_adapter_get_elevation(*args, **kwargs):
    return EXPECTED_ELEVATION


class TestLocationManager(TestCase):
    def setUp(self):
        self.warsaw = LocationFactory(
            name="Warsaw", location=Point(21.003778, 52.212667)
        )
        self.oslo = LocationFactory(name="Oslo", location=Point(10.783329, 59.916950))
        self.kielce = LocationFactory(
            name="Kielce", location=Point(20.645882, 50.862886)
        )
        self.point_piaseczno = Point(21.0238602, 52.0811536)
        self.distance = 200000  # meters

    def test_check_if_exists_return__false__when_location_does_not_exist(self):
        place_data = LocationFactory.build()
        check = Location.objects.check_if_exists(location=place_data.location)
        self.assertFalse(check)

    def test_check_if_exists_return__true__when_location_exists(self):
        check = Location.objects.check_if_exists(
            location=Point(self.oslo.location.x, self.oslo.location.y)
        )
        self.assertTrue(check)

    @mock.patch(
        "location.locations.managers.AdapterElevationAPI.get_elevation",
        side_effect=mocked_adapter_get_elevation,
    )
    def test_create_location_when_elevation_not_provided_in_create(
        self, mock_get_elevation
    ):
        data = factory.build(dict, FACTORY_CLASS=LocationFactory)
        data.pop("elevation")

        place = Location.objects.create(**data)

        self.assertEqual(data["name"], place.name)
        self.assertEqual(data["location"], place.location)
        self.assertEqual(EXPECTED_ELEVATION, place.elevation)

    @mock.patch(
        "location.locations.managers.AdapterElevationAPI.get_elevation",
        side_effect=mocked_adapter_get_elevation,
    )
    def test_call_once__get_elevation__when_create_location_and_elevation_not_provided(
        self, mock_get_elevation
    ):
        data = factory.build(dict, FACTORY_CLASS=LocationFactory)
        data.pop("elevation")

        Location.objects.create(**data)

        expected_call = call(data["location"].x, data["location"].y)
        mock_get_elevation.assert_called_once()
        self.assertIn(expected_call, mock_get_elevation.call_args_list)

    @mock.patch(
        "location.locations.managers.AdapterElevationAPI.get_elevation",
        side_effect=mocked_adapter_get_elevation,
    )
    def test_does_not_call__get_elevation__when_create_location_and_elevation_provided(
        self, mock_get_elevation
    ):
        LocationFactory()
        mock_get_elevation.assert_not_called()

    def test_find_closest_return_queryset(self):
        closest_location = Location.objects.find_closest_queryset(
            self.warsaw.location.x, self.warsaw.location.y
        )
        self.assertTrue(isinstance(closest_location, QuerySet))

        closest_locations = Location.objects.find_closest_queryset(
            self.warsaw.location.x, self.warsaw.location.y, self.distance
        )
        self.assertTrue(isinstance(closest_locations, QuerySet))

    def test_find_closest_place(self):

        closest_location = Location.objects.find_closest_queryset(
            self.point_piaseczno.x, self.point_piaseczno.y
        ).all()

        self.assertEqual(1, len(closest_location))

        closest_location = closest_location[0]
        self.assertEqual(self.warsaw.uuid, closest_location.uuid)

    def test_find_closest_places(self):
        closest_locations = Location.objects.find_closest_queryset(
            self.point_piaseczno.x, self.point_piaseczno.y, self.distance
        ).all()

        self.assertEqual(2, len(closest_locations))
        self.assertEqual(self.warsaw.uuid, closest_locations[0].uuid)
        self.assertEqual(self.kielce.uuid, closest_locations[1].uuid)
