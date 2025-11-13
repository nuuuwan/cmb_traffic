from cmb_traffic.Location import Location
from cmb_traffic.Route import Route


class TrafficIndexStandardRouteMixin:
    @staticmethod
    def build_route_list(*location_list: list[Location]):
        undirected_route_list = []
        n = len(location_list)
        for i in range(n - 1):
            location_i = location_list[i]
            for j in range(i + 1, n):
                location_j = location_list[j]
                route = Route(
                    start_location=location_i,
                    end_location=location_j,
                )
                if not route.is_location_order_north_south():
                    route = route.reverse()

                undirected_route_list.append(route)
        return undirected_route_list

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
