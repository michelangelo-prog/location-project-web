from django.test import TestCase

from ..models import Location

from django.contrib.gis.geos import Point

class TestLocationModelManager(TestCase):
    """
    Tests Location Model Manager
    """
    def setUp(self):
        pkt_warsaw = Point(21.003778,52.212667)
        pkt_oslo = Point(10.783329,59.916950)
        pkt_kielce = Point(20.645882,50.862886)
        pkt_piaseczno = Point(21.0238602,52.0811536)
        Location.objects.create(name='warsaw', location=pkt_warsaw, elevation=0)
        Location.objects.create(name='oslo', location=pkt_oslo, elevation=0)
        Location.objects.create(name='kielce', location=pkt_kielce, elevation=0)
        Location.objects.create(name='piaseczno', location=pkt_piaseczno, elevation=0)
        self.ref_pkt_tarczyn = Point(20.83374,51.97842)

    def test_find_nearest_location(self):
        near = Location.objects.find_nearest_location(self.ref_pkt_tarczyn[0], self.ref_pkt_tarczyn[1])
        self.assertEquals(near.name, 'piaseczno')

    def test_find_nearest_locations_by_distance(self):
        nearest = Location.objects.find_nearest_locations_by_distance(self.ref_pkt_tarczyn[0], self.ref_pkt_tarczyn[1], 17320)
        self.assertEquals(nearest.count(), 1)
        self.assertEquals(nearest[0].name, 'piaseczno')
