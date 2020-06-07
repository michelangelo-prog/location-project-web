from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from location_project.users.test.factories import UserFactory
from nose.tools import ok_, eq_
import json

from mock import patch

import requests


class TestLocationCreateTestCase(APITestCase):
    """
    Tests /locations create new location
    """

    def setUp(self):
        self.user = UserFactory()
        self.url = reverse('api:locations')

    def test_post_request_create_location(self):
        data = {
            "name": "Warsaw",
            "location": {
                "latitude": 11.4,
                "longitude": 51.2
            }
        }

        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        eq_(response.status_code, 403)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        eq_(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

    class TestLocationFindLocationTestCase(APITestCase):
        """
        Tests /locations/find
        """

        def setUp(self):
            self.user = UserFactory()
            self.url = reverse('api:locations_find')
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')

        def test_get_request_get_location(self):
            payload = {}
            payload['username'] = self.user.username
            payload['longitude'] = 21
            payload['latitude'] = 15

            response = self.client.get(self.url, payload)
            eq_(response.status_code, status.HTTP_200_OK)

            payload['username'] = "nick"
            response = self.client.get(self.url, payload)

            eq_(response.status_code, status.HTTP_400_BAD_REQUEST)
