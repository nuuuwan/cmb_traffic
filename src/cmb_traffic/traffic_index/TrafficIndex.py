from datetime import timedelta, timezone

from utils import Log

from cmb_traffic.Journey import Journey
from cmb_traffic.Route import Route
from cmb_traffic.traffic_index.TrafficIndexStandardRouteMixin import (
    TrafficIndexStandardRouteMixin,
)

log = Log("TrafficIndex")

# Sri Lanka timezone (UTC+5:30)
LK_TZ = timezone(timedelta(hours=5, minutes=30))


class TrafficIndex(TrafficIndexStandardRouteMixin):
    ROUND_FACTOR = 1_800

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
        Journey.write_all()

    def __get_ut_start_to_d_list__(self):
        ut_start_to_d_list = {}
        for journey in Journey.list_all():
            ut_start = journey.ut_start
            ut_start_low = (
                int(ut_start / self.ROUND_FACTOR) * self.ROUND_FACTOR
            )
            ut_start_high = ut_start_low + self.ROUND_FACTOR
            w_high = (ut_start - ut_start_low) / self.ROUND_FACTOR

            if ut_start_low not in ut_start_to_d_list:
                ut_start_to_d_list[ut_start_low] = []
            ut_start_to_d_list[ut_start_low].append(
                (journey.direct_speed_kmph, (1 - w_high))
            )

            if ut_start_high not in ut_start_to_d_list:
                ut_start_to_d_list[ut_start_high] = []
            ut_start_to_d_list[ut_start_high].append(
                (journey.direct_speed_kmph, w_high)
            )
        return ut_start_to_d_list

    def get_journey_data_list(self):
        ut_start_to_d_list = self.__get_ut_start_to_d_list__()
        overall_d_list = []
        for ut_start, d_list in ut_start_to_d_list.items():
            w_sum = sum([weight for _, weight in d_list])
            if w_sum == 0:
                continue

            speed_wsum = sum([speed * weight for speed, weight in d_list])
            overall_d_list.append(
                dict(
                    ut_start=ut_start,
                    direct_speed_kmph=speed_wsum / w_sum,
                )
            )
        overall_d_list.sort(key=lambda d: d["ut_start"])
        return overall_d_list
