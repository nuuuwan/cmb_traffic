from utils import LatLng

from cmb_traffic.JourneyRoute import JourneyRoute


class TrafficIndexStandardRouteMixin:
    @staticmethod
    def build_route_list(
        base_location_idx: dict[str, LatLng],
    ):
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

    @classmethod
    def standard_route(cls):
        bambalapitiya = LatLng(6.895572468746244, 79.85483770889027)
        borella = LatLng(6.910882574522934, 79.88789773709671)
        dematagoda = LatLng(6.943175860321491, 79.87820817923517)
        fort = LatLng(6.931424355241801, 79.84220762949998)
        mattakkuliya = LatLng(6.980026983331188, 79.87551282104877)
        pamankada = LatLng(6.871812810816128, 79.88456400975986)
        wellawatte = LatLng(6.863288956321618, 79.86360827087549)
        return cls(
            cls.build_route_list(
                dict(
                    dematagoda=dematagoda,
                    fort=fort,
                    mattakkuliya=mattakkuliya,
                ),
            )
            + cls.build_route_list(
                dict(
                    bambalapitiya=bambalapitiya,
                    borella=borella,
                    dematagoda=dematagoda,
                    fort=fort,
                ),
            )
            + cls.build_route_list(
                dict(
                    bambalapitiya=bambalapitiya,
                    borella=borella,
                    pamankada=pamankada,
                    wellawatte=wellawatte,
                ),
            ),
        )
