import unittest

from test_journey_route import TEST_JOURNEY_ROUTE

from cmb_traffic import TrafficIndex

TEST_TRAFFIC_INDEX = TrafficIndex(
    undirected_journey_route_list=[TEST_JOURNEY_ROUTE]
)


class TestCase(unittest.TestCase):
    @unittest.skip("Slow")
    def test_write_all(self):
        TEST_TRAFFIC_INDEX.write_all()
