from cmb_traffic.Location import Location
from cmb_traffic.Route import Route


class TrafficIndexStandardRouteMixin:
    @staticmethod
    def build_route_list(*location_list: list[Location]) -> list[Route]:
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
    def for_cmc_index(cls):
        return cls(
            "Colombo Traffic Index",
            "An index measuring traffic conditions"
            + " within the Colombo Municipal Council (CMC) area.",
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
            is_default=True,
        )

    @classmethod
    def for_int_cmc(cls):
        return cls(
            "Colombo Suburban Traffic Index",
            "An index measuring traffic conditions"
            + " between Colombo and its immediate suburbs.",
            [
                Route(
                    Location.DEMATAGODA,
                    Location.RAGAMA,
                ),
                Route(
                    Location.DEMATAGODA,
                    Location.KIRIBATHGODA,
                ),
                Route(
                    Location.BORELLA,
                    Location.KADUWELA,
                ),
                Route(
                    Location.PAMANKADA,
                    Location.KOTTAWA,
                ),
                Route(
                    Location.WELLAWATTE,
                    Location.MORATUWA,
                ),
            ],
            is_default=False,
        )

    @classmethod
    def all(cls) -> list:
        return [
            cls.for_cmc_index(),
            cls.for_int_cmc(),
        ]
