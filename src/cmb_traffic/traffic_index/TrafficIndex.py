from datetime import timedelta, timezone

from utils import Log

from cmb_traffic.Journey import Journey
from cmb_traffic.JourneyRoute import JourneyRoute
from cmb_traffic.traffic_index.TrafficIndexReadMeMixin import \
    TrafficIndexReadMeMixin
from cmb_traffic.traffic_index.TrafficIndexStandardRouteMixin import \
    TrafficIndexStandardRouteMixin

log = Log("TrafficIndex")

# Sri Lanka timezone (UTC+5:30)
LK_TZ = timezone(timedelta(hours=5, minutes=30))


class TrafficIndex(TrafficIndexReadMeMixin, TrafficIndexStandardRouteMixin):

    def __init__(self, undirected_journey_route_list: list[JourneyRoute]):
        lst = undirected_journey_route_list
        idx = {route.name: route for route in lst}
        lst = list(idx.values())
        lst.sort(
            key=lambda route: (
                -route.start_location.latlng.lat,
                route.end_location.latlng.lat,
            ),
        )
        for route in lst:
            print(route)
        self.undirected_journey_route_list = lst

    def get_full_journey_route_list(self) -> list[JourneyRoute]:
        return self.undirected_journey_route_list + [
            route.reverse() for route in self.undirected_journey_route_list
        ]

    def write_all(self):
        for route in self.get_full_journey_route_list():
            journey = Journey.from_route_now(route)
            journey.write_journey_info()

    def get_journey_data_list(self):
        start_time_to_d_list = {}
        for route in self.get_full_journey_route_list():
            d_list = route.get_journey_data_list()
            for d in d_list:
                start_time = d["start_time"]
                if start_time not in start_time_to_d_list:
                    start_time_to_d_list[start_time] = []
                start_time_to_d_list[start_time].append(
                    d["direct_speed_kmph"]
                )

        overall_d_list = []
        for start_time, speed_list in start_time_to_d_list.items():
            n = len(speed_list)
            direct_speed_kmph = sum(speed_list) / n
            overall_d_list.append(
                dict(
                    start_time=start_time,
                    n=n,
                    direct_speed_kmph=direct_speed_kmph,
                )
            )
        overall_d_list.sort(key=lambda d: d["start_time"])
        return overall_d_list
