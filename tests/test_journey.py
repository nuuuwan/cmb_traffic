import os
import unittest

from test_journey_route import TEST_JOURNEY_ROUTE

from cmb_traffic import Journey

TEST_JOURNEY = Journey.from_route_now(TEST_JOURNEY_ROUTE)


class TestCase(unittest.TestCase):
    @unittest.skip("Slow")
    def test_write_duration(self):
        TEST_JOURNEY.write_journey_info()
        self.assertTrue(os.path.exists(TEST_JOURNEY.data_path))
