import unittest

from test_route import TEST_route

from cmb_traffic import TrafficIndex

TEST_TRAFFIC_INDEX = TrafficIndex(undirected_route_list=[TEST_route])


class TestCase(unittest.TestCase):
    @unittest.skip("Slow")
    def test_write_all(self):
        TEST_TRAFFIC_INDEX.write_all()
