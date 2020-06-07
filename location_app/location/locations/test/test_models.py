from django.test import TestCase

from ..models import Location

from ..exceptions import LocationExist

from django.contrib.gis.geos import Point

class TestLocationsModels(TestCase):

    def setUp(self):
        self.pkt_warsaw = Point(21.003778,52.212667)
        self.pkt_oslo = Point(10.783329,59.916950)
        pkt_kielce = Point(20.645882,50.862886)
        pkt_piaseczno = Point(21.0238602,52.0811536)
        Location.objects.create(name='warsaw', location=self.pkt_warsaw, elevation=0)
        Location.objects.create(name='oslo', location=self.pkt_oslo, elevation=0)
        Location.objects.create(name='kielce', location=pkt_kielce, elevation=0)
        Location.objects.create(name='piaseczno', location=pkt_piaseczno, elevation=0)

    def test_safe(self):
        with self.assertRaises(LocationExist):
            Location.objects.create(name='Home', location=self.pkt_warsaw, elevation=0)
