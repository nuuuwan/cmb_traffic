import unittest

from utils import LatLng

from cmb_traffic import Route

TEST_route = Route(
    name="Test Journey",
    start_latlng=LatLng(6.91169017313128, 79.86456199881907),
    end_latlng=LatLng(6.89763623570068, 79.85997608991968),
)


class TestCase(unittest.TestCase):
    def test_url(self):
        self.assertEqual(
            TEST_route.url,
            "https://www.google.com/maps/dir"
            + "/6.91169,79.86456/6.89764,79.85998/",
        )

    def test_reverse(self):
        reverse = TEST_route.reverse()
        self.assertEqual(
            reverse.url,
            "https://www.google.com/maps/dir"
            + "/6.89764,79.85998/6.91169,79.86456/",
        )
