from dataclasses import dataclass

from cmb_traffic.Journey import Journey
from cmb_traffic.JourneyRoute import JourneyRoute


@dataclass
class TrafficIndex:
    undirected_journey_route_list: list[JourneyRoute]

    def get_full_journey_route_list(self) -> list[JourneyRoute]:
        return self.undirected_journey_route_list + [
            route.transpose() for route in self.undirected_journey_route_list
        ]

    def write_all(self):
        for route in self.get_full_journey_route_list():
            journey = Journey.from_route_now(route)
            journey.write_duration()
