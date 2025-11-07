import unittest

from utils import LatLng, Time, TimeDelta

from cmb_traffic import Journey

TEST_JOURNEY = Journey(
    name="Test Journey",
    start_latlng=LatLng(6.91169017313128, 79.86456199881907),
    end_latlng=LatLng(6.89763623570068, 79.85997608991968),
    start_time=Time.now(),
)


class TestCase(unittest.TestCase):
    def test_url(self):
        self.assertEqual(
            TEST_JOURNEY.url,
            "https://www.google.com/maps/dir"
            + "/6.91169,79.86456/6.89764,79.85998/",
        )

    def test_get_duration(self):
        duration = TEST_JOURNEY.get_duration()
        self.assertEqual(duration, TimeDelta(240))
