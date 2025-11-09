
from cmb_traffic.JourneyRoute import JourneyRoute
from cmb_traffic.Location import Location


class TrafficIndexStandardRouteMixin:
    @staticmethod
    def build_route_list(*location_list: list[Location]):
        undirected_journey_route_list = []
        n = len(location_list)
        for i in range(n - 1):
            location_i = location_list[i]
            for j in range(i + 1, n):
                location_j = location_list[j]
                route = JourneyRoute(
                    start_location=location_i,
                    end_location=location_j,
                )
                undirected_journey_route_list.append(route)
        return undirected_journey_route_list

    @classmethod
    def standard_route(cls):
        return cls(
            cls.build_route_list(
                Location.DEMATAGODA,
                Location.FORT,
                Location.MATTAKKULIYA,
            )
            + cls.build_route_list(
                Location.BAMBALAPITIYA,
                Location.BORELLA,
                Location.DEMATAGODA,
                Location.FORT,
            )
            + cls.build_route_list(
                Location.BAMBALAPITIYA,
                Location.BORELLA,
                Location.PAMANKADA,
                Location.WELLAWATTE,
            ),
        )
