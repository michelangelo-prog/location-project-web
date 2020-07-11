from rest_framework.test import APITestCase

from ..factories import LocationFactory

from rest_framework import status

import factory

from ..models import Location

class TestCreateLocation(APITestCase):

    def test_create_location(self):
        data = factory.build(dict, FACTORY_CLASS=LocationFactory)
        point = data.pop("location")
        data.pop("elevation")
        data["longitude"] = point.x
        data["latitude"] = point.y

        response = self.client.post("/api/v1/location", data=data, format='json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Location.objects.count())
