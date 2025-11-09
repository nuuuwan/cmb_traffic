from dataclasses import dataclass
from datetime import timedelta, timezone

from utils import LatLng, Log

from cmb_traffic.Journey import Journey
from cmb_traffic.JourneyRoute import JourneyRoute
from cmb_traffic.traffic_index.TrafficIndexReadMeMixin import \
    TrafficIndexReadMeMixin

log = Log("TrafficIndex")

# Sri Lanka timezone (UTC+5:30)
LK_TZ = timezone(timedelta(hours=5, minutes=30))


@dataclass
class TrafficIndex(TrafficIndexReadMeMixin):
    undirected_journey_route_list: list[JourneyRoute]
    DIR_IMAGES = JourneyRoute.DIR_IMAGES

    README_PATH = "README.md"

    @staticmethod
    def standard_route():
        bambalapitiya = LatLng(6.895572468746244, 79.85483770889027)
        borella = LatLng(6.910882574522934, 79.88789773709671)
        dematagoda = LatLng(6.943175860321491, 79.87820817923517)
        fort = LatLng(6.931424355241801, 79.84220762949998)
        mattakkuliya = LatLng(6.980026983331188, 79.87551282104877)
        pamankada = LatLng(6.871812810816128, 79.88456400975986)
        wellawatte = LatLng(6.863288956321618, 79.86360827087549)
        return TrafficIndex(
            TrafficIndex.build_route_list(
                dict(
                    dematagoda=dematagoda,
                    fort=fort,
                    mattakkuliya=mattakkuliya,
                ),
            )
            + TrafficIndex.build_route_list(
                dict(
                    bambalapitiya=bambalapitiya,
                    borella=borella,
                    dematagoda=dematagoda,
                    fort=fort,
                ),
            )
            + TrafficIndex.build_route_list(
                dict(
                    bambalapitiya=bambalapitiya,
                    borella=borella,
                    pamankada=pamankada,
                    wellawatte=wellawatte,
                ),
            ),
        )

    @staticmethod
    def build_route_list(
        base_location_idx: dict[str, LatLng],
    ) -> "TrafficIndex":
        undirected_journey_route_list = []
        n = len(base_location_idx)
        location_names = list(base_location_idx.keys())
        for i in range(n - 1):
            for j in range(i + 1, n):
                start_name = location_names[i]
                end_name = location_names[j]
                route = JourneyRoute(
                    name=f"{start_name.title()} to {end_name.title()}",
                    start_latlng=base_location_idx[start_name],
                    end_latlng=base_location_idx[end_name],
                )
                undirected_journey_route_list.append(route)
        return undirected_journey_route_list

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
                start_time_to_d_list[start_time].append(d["avg_speed_kmph"])

        overall_d_list = []
        for start_time, speed_list in start_time_to_d_list.items():
            n = len(speed_list)
            avg_speed_kmph = sum(speed_list) / n
            overall_d_list.append(
                dict(
                    start_time=start_time, n=n, avg_speed_kmph=avg_speed_kmph
                )
            )
        overall_d_list.sort(key=lambda d: d["start_time"])
        return overall_d_list
