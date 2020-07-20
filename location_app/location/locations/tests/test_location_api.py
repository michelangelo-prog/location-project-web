from rest_framework.test import APITestCase

from ..factories import LocationFactory

from rest_framework import status

import factory

from unittest import mock

from ..models import Location

from location.users.tests.factories import UserFactory


EXPECTED_ELEVATION = 22.22


def mocked_adapter_get_elevation(*args, **kwargs):
    return EXPECTED_ELEVATION


class TestCreateLocation(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")

    @mock.patch(
        "location.locations.managers.AdapterElevationAPI.get_elevation",
        side_effect=mocked_adapter_get_elevation,
    )
    def test_create_location(self, mocked_adapter_get_elevation):
        data = factory.build(dict, FACTORY_CLASS=LocationFactory)
        data.pop("elevation")
        point = data.pop("location")
        data["location"] = dict()
        data["location"]["longitude"] = point.x
        data["location"]["latitude"] = point.y

        response = self.client.post("/api/v1/locations/", data=data, format="json")

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        locations_in_db = Location.objects.all()
        self.assertEqual(1, len(locations_in_db))
        location_in_db = locations_in_db[0]
        self.assertEqual(data["name"], location_in_db.name)
        self.assertEqual(data["location"]["longitude"], location_in_db.location.x)
        self.assertEqual(data["location"]["latitude"], location_in_db.location.y)
        self.assertEqual(EXPECTED_ELEVATION, location_in_db.elevation)
