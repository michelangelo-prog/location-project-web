from django.test import TestCase

from .. serializers import CreateLocationSerializer

from nose.tools import eq_, ok_

from django.contrib.gis.geos import Point

class TestCreateUserSerializer(TestCase):

    def test_serializer_with_empty_data(self):
        serializer = CreateLocationSerializer(data={})
        eq_(serializer.is_valid(), False)
