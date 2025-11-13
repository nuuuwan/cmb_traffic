from datetime import timedelta, timezone

from utils import Log

from cmb_traffic.Journey import Journey
from cmb_traffic.Route import Route
from cmb_traffic.traffic_index.TrafficIndexStandardRouteMixin import \
    TrafficIndexStandardRouteMixin

log = Log("TrafficIndex")

# Sri Lanka timezone (UTC+5:30)
LK_TZ = timezone(timedelta(hours=5, minutes=30))


class TrafficIndex(TrafficIndexStandardRouteMixin):

    @staticmethod
    def __dedupe_and_sort_route_list__(lst) -> list[Route]:
        idx = {route.name: route for route in lst}
        lst = list(idx.values())
        lst.sort(
            key=lambda route: (
                -route.start_location.latlng.lat,
                route.end_location.latlng.lat,
            ),
        )
        return lst

    def __init__(self, undirected_route_list: list[Route]):
        self.undirected_route_list = (
            TrafficIndex.__dedupe_and_sort_route_list__(undirected_route_list)
        )

    def get_full_route_list(self) -> list[Route]:
        return self.undirected_route_list + [
            route.reverse() for route in self.undirected_route_list
        ]

    def write_all(self):
        for route in self.get_full_route_list():
            Journey.from_route(route).write()

    def get_journey_data_list(self):
        ut_start_to_d_list = {}
        for journey in Journey.list_all():
            ut_start = journey.get_utc_ut_start()
            if ut_start not in ut_start_to_d_list:
                ut_start_to_d_list[ut_start] = []
            ut_start_to_d_list[ut_start].append(d["direct_speed_kmph"])

        overall_d_list = []
        for ut_start, speed_list in ut_start_to_d_list.items():
            n = len(speed_list)
            direct_speed_kmph = sum(speed_list) / n
            overall_d_list.append(
                dict(
                    ut_start=ut_start,
                    n=n,
                    direct_speed_kmph=direct_speed_kmph,
                )
            )
        overall_d_list.sort(key=lambda d: d["ut_start"])
        return overall_d_list
